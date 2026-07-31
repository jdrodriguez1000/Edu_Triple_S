"""
Nivel 5 - Script 5: el juez (LLM-as-judge), y como se valida.

EL PROBLEMA QUE VIENE A RESOLVER
--------------------------------
El detector del script 1 es una lista de palabras que escribi yo. Lo que
no este en la lista no existe para el programa. Y hay preguntas que
NINGUNA lista puede responder por muchas palabras que le metas:

    ¿la respuesta fue util?
    ¿dijo de donde saco el dato?
    ¿suena natural para un colombiano, o suena a traduccion?

Para eso se usa otro modelo como juez, con una escala que defines tu.
Esa escala es la RUBRICA, y es la parte que importa: una rubrica vaga da
notas vagas. "Califica del 1 al 10 que tan buena es" no sirve para nada.

LA PREGUNTA INCOMODA: ¿Y QUIEN JUZGA AL JUEZ?
---------------------------------------------
El juez es un modelo. Todo lo que aprendiste en este nivel le aplica: no
da lo mismo dos veces, tiene sesgos, y puede equivocarse con seguridad.

    -> Un juez que nadie valido es una opinion con formato de numero.

Asi que este script hace TRES cosas, y solo la primera es "juzgar":

  A. JUZGA respuestas cuya etiqueta ya conocemos (las del detector
     determinista, que se valido con pares minimos en el script 0).
     Si el juez no coincide ahi, no sirve para nada mas dificil.

  B. MIDE SI EL JUEZ SE CONTRADICE CONSIGO MISMO: vuelve a juzgar una
     submuestra y compara. Es la version barata de la idea del "jurado
     de jueces". OJO: correr el mismo modelo dos veces mide ESTABILIDAD,
     no sesgo -- te da el mismo punto ciego dos veces.

  C. SACA LOS DESACUERDOS a la luz para que los mires TU. Eres colombiano;
     para "¿esto suena colombiano?" tu criterio vale mas que el del
     modelo, y eres el unico juez que no comparte su punto ciego.

EL SESGO QUE HAY QUE TENER PRESENTE TODO EL RATO
------------------------------------------------
El juez es un modelo de Anthropic calificando texto de un modelo de
Anthropic. Se llama AUTOPREFERENCIA. Lo honesto seria un juez de otra
familia; como aqui solo hay Claude, se compensa con A y con C.

POR QUE HAIKU Y NO OPUS
-----------------------
El juez solo clasifica: no razona ni escribe. Es el caso de libro de
Haiku, 25x mas barato en salida. Juzgar cuesta centavos.

LAS RESPUESTAS YA ESTAN EN DISCO
--------------------------------
Se juzga texto YA generado, de resultados/*.json. Los $0.49 de generar
ese texto ya se pagaron; reanalizarlo cuesta solo el juicio.
    -> Por eso los scripts guardaban.

COSTO: ESTIMADO ~$0.07 juzgando las 130 + 20 repeticiones, con Haiku.
       Anotar el real al correr.

USO:
    python 05_juez.py           # las 130 guardadas
    python 05_juez.py 30        # solo 30, para probar barato
"""

import glob
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

import anthropic
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
load_dotenv(AQUI.parent / ".env")

MODELO_JUEZ = "claude-sonnet-5"

# ---------------------------------------------------------------------------
# LOS PRECIOS VAN ATADOS AL MODELO. No los sueltes en dos constantes.
# ---------------------------------------------------------------------------
# Este bloque nacio de un BUG REAL del ejercicio 1. Antes decia:
#
#     PRECIO_ENTRADA = 1.00 / 1_000_000     # Haiku
#     PRECIO_SALIDA = 5.00 / 1_000_000
#
# El estudiante cambio MODELO_JUEZ a Sonnet... y los precios siguieron siendo
# los de Haiku. El script imprimio "COSTO REAL: $0.1530" con toda confianza.
# El costo verdadero era $0.3060 -- el doble.
#
# El bug no revienta, no avisa, y aparece justo en la linea que dice
# "COSTO REAL". Es el mismo patron del "55x" del nivel 1 y del "~$0.02" del
# nivel 4: un numero afirmado que nadie midio.
#
# REGLA: si el modelo es una variable, el precio tambien tiene que serlo.
# Un dato que depende de otro no se guarda suelto: se guarda junto.
#
# Dolares por millon de tokens (entrada, salida). Verificado 2026-07-29.
# OJO: Sonnet 5 esta en precio de lanzamiento ($2/$10) hasta el 2026-08-31.
# Despues sube a $3/$15 y esta misma corrida costara ~$0.46 sin que cambies
# una sola linea. Por eso la fecha esta escrita aqui y no en tu memoria.
PRECIOS = {
    "claude-haiku-4-5": (1.00, 5.00),
    "claude-sonnet-5": (2.00, 10.00),   # lanzamiento; desde 2026-09-01: (3.00, 15.00)
    "claude-opus-5": (5.00, 25.00),
}

if MODELO_JUEZ not in PRECIOS:
    # Preferimos reventar AHORA a imprimir un costo inventado despues.
    raise SystemExit(
        f"\nNo tengo el precio de '{MODELO_JUEZ}'.\n"
        f"Agregalo al diccionario PRECIOS antes de correr, o el script\n"
        f"te va a mentir sobre cuanto gastaste.\n"
    )

PRECIO_ENTRADA, PRECIO_SALIDA = (p / 1_000_000 for p in PRECIOS[MODELO_JUEZ])

LIMITE = int(sys.argv[1]) if len(sys.argv) > 1 else None
REPETIR = 20            # cuantas se vuelven a juzgar para medir estabilidad


# ---------------------------------------------------------------------------
# ZONA A - LA RUBRICA
# ---------------------------------------------------------------------------
# Esta es la pieza que de verdad importa. Tres cosas la hacen utilizable:
#
#  1. NIVELES SEPARABLES. Si dos niveles se pueden confundir, ningun juez
#     -- ni humano -- va a dar notas estables. El desacuerdo entre jueces
#     casi siempre es culpa de la rubrica, no de los jueces.
#  2. EJEMPLOS CONCRETOS de palabras en cada nivel, no adjetivos.
#  3. UN SOLO EJE. Aqui se califica dialecto y NADA MAS: ni si el consejo
#     es bueno, ni si esta bien escrita. Mezclar ejes en una nota da un
#     numero que no se puede interpretar.

RUBRICA = """Eres un evaluador de coherencia en el trato. Tu unico trabajo es
decir si el texto trata al lector de forma CONSISTENTE de principio a fin.
No evalues si el consejo es bueno, ni la ortografia, ni si es util.
SOLO la coherencia del trato.

En espanol hay dos formas de dirigirse a alguien, y mezclarlas en un mismo
mensaje suena mal y descuidado:

  TUTEO  : ponte, lleva, tienes, puedes, te conviene, tu chaqueta, contigo
  USTEDEO: pongase, lleve, tiene, puede, le conviene, su chaqueta, con usted

Escala:

0 = MEZCLA LOS DOS. Empieza tuteando y termina ustedeando, o al contrario.
    Ejemplo real que es 0:
      "Ponte una chaqueta... que no se te empapen. Lleve paraguas."
      ("ponte" y "te" son tuteo; "lleve" es ustedeo -> mezcla)

1 = USTEDEO consistente de principio a fin.

2 = TUTEO consistente de principio a fin.

COMO DESEMPATAR CUANDO UNA PALABRA ES AMBIGUA:
"le", "se" y "su" sirven para usted Y para tercera persona. Decide por el
contexto a quien se refieren:
  "su chaqueta" hablandole al lector      -> ustedeo
  "el aguacero coge a cualquiera, su ..." -> tercera persona, NO cuenta
Si una palabra ambigua no se refiere al lector, ignorala.

Las notas 1 y 2 son las dos BUENAS: no hay una mejor que la otra.
La unica mala es la 0.

Responde SOLO con un objeto JSON, sin nada mas antes ni despues:
{"nota": 0, "razon": "maximo 12 palabras", "palabras": ["las", "que", "lo", "delatan"]}"""


# ---------------------------------------------------------------------------
# ZONA B - Cargar lo que ya esta en disco
# ---------------------------------------------------------------------------

def cargar_respuestas():
    """Junta las corridas de todos los resultados/*.json.

    Cada una trae la etiqueta que le puso el detector determinista, que
    es contra lo que se va a comparar al juez."""
    items = []
    for archivo in sorted(glob.glob(str(AQUI / "resultados" / "*.json"))):
        # El script GUARDA su informe en esta misma carpeta, asi que en la
        # segunda corrida se encontraba a si mismo e intentaba juzgar su
        # propio resultado (KeyError: 'corridas'). Un programa que lee y
        # escribe en el mismo sitio se contamina solo.
        # Dos defensas, no una: por nombre y por forma del contenido.
        if Path(archivo).name.startswith("juez-"):
            continue
        datos = json.loads(Path(archivo).read_text(encoding="utf-8"))
        if "corridas" not in datos:
            continue
        for c in datos["corridas"]:
            if not c.get("texto"):
                continue
            # El experimento v1 no tenia detector de tratamiento, asi que
            # sus 10 respuestas no sirven para comparar aqui. Se saltan:
            # mejor 120 respuestas con etiqueta que 130 con huecos.
            if not c.get("tratamiento"):
                continue
            items.append({
                "origen": Path(archivo).name,
                "version": c.get("version", "-"),
                "n": c["n"],
                "texto": c["texto"],
                "detector_trato": c["tratamiento"],   # la etiqueta conocida
                "marcas_tu": c.get("marcas_tu", []),
                "marcas_ud": c.get("marcas_ud", []),
            })
    return items


# ---------------------------------------------------------------------------
# ZONA C - El juez
# ---------------------------------------------------------------------------

cliente = anthropic.Anthropic(max_retries=2, timeout=60.0)

gasto = {"entrada": 0, "salida": 0}


def juzgar(texto):
    """Devuelve (nota, razon, palabras) o (None, motivo, []) si fallo.

    Que el juez no siga el formato NO se esconde: se cuenta. Un juez que
    devuelve basura el 5% de las veces es un dato del juez, no un
    accidente que haya que tapar con un try/except silencioso."""
    respuesta = cliente.messages.create(
        model=MODELO_JUEZ,
        max_tokens=300,
        system=RUBRICA,
        messages=[{"role": "user", "content": f"Texto a evaluar:\n\n{texto}"}],
    )
    gasto["entrada"] += respuesta.usage.input_tokens
    gasto["salida"] += respuesta.usage.output_tokens

    crudo = "".join(b.text for b in respuesta.content if b.type == "text").strip()

    # El modelo a veces envuelve el JSON en ```json ... ```. Se limpia
    # antes de parsear, en vez de darlo por perdido.
    bloque = re.search(r"\{.*\}", crudo, re.S)
    if not bloque:
        return None, f"sin JSON: {crudo[:60]}", []
    try:
        dato = json.loads(bloque.group(0))
    except json.JSONDecodeError as e:
        return None, f"JSON invalido: {e}", []

    nota = dato.get("nota")
    if nota not in (0, 1, 2):
        return None, f"nota fuera de la escala: {nota!r}", []
    return nota, str(dato.get("razon", ""))[:60], dato.get("palabras", [])


# ---------------------------------------------------------------------------
# ZONA D - El programa
# ---------------------------------------------------------------------------

def main():
    items = cargar_respuestas()
    if LIMITE:
        # Se toman repartidas, no las primeras: las primeras son todas
        # del mismo experimento y sesgarian la muestra.
        paso = max(1, len(items) // LIMITE)
        items = items[::paso][:LIMITE]

    print("=" * 78)
    print(f"  EL JUEZ ({MODELO_JUEZ})")
    print("=" * 78)
    print(f"  respuestas a juzgar : {len(items)}  (ya generadas, de resultados/)")
    print(f"  etiqueta conocida   : la del detector determinista")
    print("=" * 78)
    print()

    # ---- A. JUZGAR ------------------------------------------------------
    print("  [A] juzgando...")
    for i, it in enumerate(items, 1):
        nota, razon, palabras = juzgar(it["texto"])
        it["nota"] = nota
        it["razon"] = razon
        it["palabras_juez"] = palabras
        if i % 10 == 0 or i == len(items):
            print(f"      {i}/{len(items)}", flush=True)

    rotos = [it for it in items if it["nota"] is None]
    buenos = [it for it in items if it["nota"] is not None]

    print()
    print("-" * 78)
    print("  DISTRIBUCION DE NOTAS")
    print("-" * 78)
    cuenta = Counter(it["nota"] for it in buenos)
    etiquetas = {0: "0 MEZCLA (mala)", 1: "1 usted", 2: "2 tu"}
    for nota in (0, 1, 2):
        c = cuenta.get(nota, 0)
        print(f"    {etiquetas[nota]:<16} {c:>4} de {len(buenos)}  {'#' * (c * 40 // max(1, len(buenos)))}")
    if rotos:
        print(f"    {'sin formato':<16} {len(rotos):>4}  <- el juez no devolvio JSON valido")

    # ---- ¿COINCIDE CON EL DETECTOR? -------------------------------------
    # El juez dice 0 = mezcla. El detector dice tratamiento == "mixto".
    #
    # OJO A LA ASIMETRIA: aqui el detector NO es la verdad absoluta como
    # lo era en el dialecto. Su lista de marcadores es corta a proposito
    # ("le", "se", "su" se dejaron fuera por ambiguos), asi que se le
    # escapan mezclas de verdad. Un desacuerdo puede darle la razon al
    # juez -- que es justamente por lo que se trajo un juez a esta tarea.
    print()
    print("-" * 78)
    print("  ¿EL JUEZ COINCIDE CON EL DETECTOR?")
    print("-" * 78)
    matriz = Counter()
    for it in buenos:
        matriz[(it["detector_trato"] == "mixto", it["nota"] == 0)] += 1

    aa = matriz[(True, True)]     # los dos ven mezcla
    bb = matriz[(False, False)]   # los dos ven consistencia
    fp = matriz[(False, True)]    # solo el juez ve mezcla
    fn = matriz[(True, False)]    # solo el detector ve mezcla

    print(f"                        juez: mezcla    juez: consistente")
    print(f"    detector: mixto          {aa:>6}            {fn:>6}")
    print(f"    detector: consistente    {fp:>6}            {bb:>6}")
    acuerdo = (aa + bb) / max(1, len(buenos)) * 100
    print()
    print(f"    ACUERDO: {aa + bb} de {len(buenos)}  ({acuerdo:.1f}%)")
    print(f"    mezclas que SOLO vio el juez     : {fp}")
    print(f"    mezclas que SOLO vio el detector : {fn}")

    if fp:
        print()
        print("    Las que solo vio el juez son las interesantes: si al")
        print("    leerlas resulta que tiene razon, encontro defectos que")
        print("    una lista de palabras no podia ver. Eso es para lo que")
        print("    sirve un juez.")
    if fn:
        print()
        print("    Las que solo vio el detector son sospechosas del juez:")
        print("    ahi habia marcadores explicitos y no los vio.")

    # ---- tambien: ¿coincide en la etiqueta completa, no solo en mezcla?
    equivalente = {0: "mixto", 1: "usted", 2: "tu"}
    exactos = sum(1 for it in buenos
                  if equivalente[it["nota"]] == it["detector_trato"])
    indets = sum(1 for it in buenos if it["detector_trato"] == "indeterminado")
    print()
    print(f"    coincidencia EXACTA de etiqueta: {exactos} de {len(buenos)}")
    print(f"    (el detector dijo 'indeterminado' en {indets}; el juez no")
    print(f"     tiene esa opcion, asi que ahi nunca puede coincidir)")

    # ---- B. ¿EL JUEZ SE CONTRADICE CONSIGO MISMO? -----------------------
    submuestra = buenos[:REPETIR]
    print()
    print("-" * 78)
    print(f"  [B] MISMO JUEZ, SEGUNDA PASADA sobre {len(submuestra)} respuestas")
    print("-" * 78)
    print("  Mide ESTABILIDAD, no sesgo: el mismo modelo dos veces tiene el")
    print("  mismo punto ciego. Pero si ni consigo mismo coincide, la rubrica")
    print("  esta mal escrita.")
    print()
    iguales, distintas = 0, []
    for it in submuestra:
        nota2, _r, _p = juzgar(it["texto"])
        if nota2 == it["nota"]:
            iguales += 1
        else:
            distintas.append((it, nota2))
    print(f"    repitio la misma nota en {iguales} de {len(submuestra)}"
          f"  ({iguales / max(1, len(submuestra)) * 100:.0f}%)")
    for it, nota2 in distintas[:5]:
        print(f"      cambio {it['nota']} -> {nota2}: "
              f"{' '.join(it['texto'].split())[:52]}...")

    # ---- C. LOS DESACUERDOS, PARA QUE LOS MIRES TU ----------------------
    print()
    print("=" * 78)
    print("  [C] DESACUERDOS - los tienes que juzgar TU")
    print("=" * 78)
    desacuerdos = [it for it in buenos
                   if (it["nota"] == 0) != (it["detector_trato"] == "mixto")]
    if not desacuerdos:
        print("    Ninguno. El juez y el detector coinciden en todo.")
    print("  Lee el texto y decide TU quien tiene razon. Eres el unico juez")
    print("  que no comparte el punto ciego del modelo.")
    for it in desacuerdos[:10]:
        quien = "SOLO EL JUEZ ve mezcla" if it["nota"] == 0 \
            else "SOLO EL DETECTOR ve mezcla"
        print(f"\n    [{quien}]")
        print(f"    {' '.join(it['texto'].split())[:170]}")
        print(f"    detector: {it['detector_trato']}"
              f"   (tu: {it['marcas_tu'] or '-'} | usted: {it['marcas_ud'] or '-'})")
        print(f"    juez ({it['nota']}): {it['razon']}  {it['palabras_juez']}")

    # ---- lo que el detector NO podia ver ---------------------------------
    print()
    print("-" * 78)
    print("  DONDE EL 'IF' SE HABIA RENDIDO")
    print("-" * 78)
    print("  En el detector de tratamiento se dejaron FUERA a proposito las")
    print("  palabras 'le', 'se' y 'su', porque son ambiguas: 'su chaqueta'")
    print("  puede ser de usted o de el. Un if no puede desambiguar eso.")
    print("  El juez si: lee la frase y decide a quien se refiere.")
    print()
    indeterminadas = [it for it in buenos
                      if it["detector_trato"] == "indeterminado"]
    print(f"  El detector no supo clasificar {len(indeterminadas)} respuestas.")
    print(f"  El juez les puso nota a todas. Estas son unas cuantas:")
    for it in indeterminadas[:4]:
        print(f"\n    {' '.join(it['texto'].split())[:150]}")
        print(f"    juez ({etiquetas[it['nota']]}): {it['razon']}")

    # ---- costo y guardado ------------------------------------------------
    costo = gasto["entrada"] * PRECIO_ENTRADA + gasto["salida"] * PRECIO_SALIDA
    print()
    print("=" * 78)
    print(f"  llamadas al juez: {len(items) + len(submuestra)}")
    print(f"  tokens: {gasto['entrada']} entrada / {gasto['salida']} salida")
    # Imprimimos el precio USADO al lado del costo. Si algun dia vuelve a
    # estar mal, se ve a simple vista en vez de esconderse en una constante.
    _pe, _ps = PRECIOS[MODELO_JUEZ]
    print(f"  precio aplicado: ${_pe:.2f}/M entrada, ${_ps:.2f}/M salida ({MODELO_JUEZ})")
    print(f"  COSTO REAL: ${costo:.4f}")
    print("=" * 78)

    sello = datetime.now().strftime("%Y%m%d-%H%M%S")
    destino = AQUI / "resultados" / f"juez-{sello}.json"
    destino.write_text(json.dumps({
        "juez": MODELO_JUEZ,
        "rubrica": RUBRICA,
        "juzgadas": len(items),
        "acuerdo_con_detector_pct": round(acuerdo, 1),
        "matriz": {"ambos_rio": aa, "ambos_limpio": bb,
                   "solo_juez": fp, "solo_detector": fn},
        "estabilidad": f"{iguales}/{len(submuestra)}",
        "sin_formato": len(rotos),
        "costo": round(costo, 4),
        # Guardamos el precio y los tokens, no solo el total. Un costo suelto
        # no se puede auditar: si el precio estaba mal, el JSON viejo miente
        # para siempre y no hay forma de recalcularlo.
        "precio_usado": {"entrada_por_millon": PRECIOS[MODELO_JUEZ][0],
                         "salida_por_millon": PRECIOS[MODELO_JUEZ][1]},
        "tokens": {"entrada": gasto["entrada"], "salida": gasto["salida"]},
        "items": buenos,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  guardado en: resultados/{destino.name}")

    print("""
  COMO LEER ESTO
  --------------
  1. Mira primero el ACUERDO. Si es bajo, el juez no sirve todavia y hay
     que arreglar la RUBRICA, no cambiar de modelo.
  2. Mira los desacuerdos UNO POR UNO. Ahi es donde se aprende: a veces
     el equivocado es el juez, y a veces resulta que tu detector tenia un
     hueco que el juez si vio.
  3. Recuerda el sesgo de fondo: es un modelo de Anthropic juzgando texto
     de un modelo de Anthropic. Por eso el ultimo juez eres tu.
""")


if __name__ == "__main__":
    main()
