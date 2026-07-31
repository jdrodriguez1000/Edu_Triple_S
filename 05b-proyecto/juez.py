"""juez.py — el juez del paso 10.

Lee las respuestas que dejó `examen.py` y las califica con `rubrica.md`.

⭐ ES LA LLAMADA MÁS SIMPLE DE TODO EL NIVEL, Y ESO SORPRENDE.
   Sin `tools`, sin bucle agéntico, sin permisos, sin frenos de herramienta.
   Una pregunta, una respuesta. Es el nivel 1 otra vez.
   → Juzgar no necesita un agente. Necesita un buen texto.

⚠️ Este archivo NO corre el agente ni gasta un centavo en el examinado. Solo
   lee un archivo y le pregunta a otro modelo. Si el examen salió mal, se
   vuelve a correr `examen.py`; esto no lo arregla.

Correr con:  python juez.py
"""

import json
import sys
from pathlib import Path

import agente          # se reutilizan su cliente, su catálogo y su anotar()

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent


# ---------------------------------------------------------------------------
# 1) QUIÉN JUZGA
# ---------------------------------------------------------------------------
# ⭐ El juez NO es el mismo modelo que se está examinando, y hay dos razones
#    distintas — la segunda es la que casi nadie tiene en mente:
#
#      1. ASIMETRÍA. Si el mismo modelo contesta y califica, le estás
#         preguntando a alguien si su propio trabajo está bien hecho.
#
#      2. EL JUEZ ES BARATO AUNQUE SEA EL CARO. El agente paga miles de tokens
#         de entrada en CADA vuelta porque RELEE el menú de 6 herramientas.
#         El juez no ve menú y no tiene bucle: lee una vez y contesta.
#         → El costo de un agente está en lo que RELEE. El juez no relee nada.
#
# Decisión de la sesión 17: sonnet juzga a haiku. Opus también servía y costaba
# ~$0,28 en vez de ~$0,17; se escogió sonnet para la primera pasada, que es la
# que existe para DEPURAR LA RÚBRICA, no para producir el número final.
# → Depurar el instrumento con el modelo caro es pagar dos veces por el mismo
#   aprendizaje.
MODELO_JUEZ = "claude-sonnet-5"

# El freno 10, reutilizado tal cual. Un nombre mal escrito muere aquí y no
# después de armar la petición.
if MODELO_JUEZ not in agente.CATALOGO:
    raise SystemExit(
        f"\n❌ MODELO_JUEZ = {MODELO_JUEZ!r} no está en el catálogo.\n"
        f"   Los que hay son: {', '.join(agente.CATALOGO)}\n"
    )

PRECIO_ENTRADA = agente.CATALOGO[MODELO_JUEZ]["entrada"]
PRECIO_SALIDA = agente.CATALOGO[MODELO_JUEZ]["salida"]

# 10 casos × (~2.000 de entrada + ~700 de salida) en sonnet ≈ $0,17.
# Se pone el doble largo: un juez que se corta a la mitad deja una evaluación
# incompleta que PARECE completa.
PRESUPUESTO_JUEZ = 0.40
gastado_usd = 0.0

# --- 🚨 max_tokens: LA PRIMERA CORRIDA DEL JUEZ SE ROMPIÓ AQUÍ ---------------
# Estaba en 1500 y dos de los diez casos salieron ilegibles. Medidos:
#
#   caso 4   stop_reason=end_turn     salida=1484   bloques: thinking + text
#   caso 5   stop_reason=max_tokens   salida=1500   bloques: SOLO thinking
#
# El modelo RAZONA antes de contestar, y ese razonamiento gasta los mismos
# tokens que la respuesta. En el caso 5 pensó tanto que se quedó sin cupo para
# hablar: 1.500 tokens de pensamiento y CERO caracteres de texto.
#
# ⭐ max_tokens NO es "cuánto quiero que escriba". Es el techo de TODO lo que
#    produce, incluido lo que piensa y que tú nunca ves.
#
# ⚠️ Y lo grave no fue que fallara, sino CUÁLES fallaron: el 4 (el domingo) y
#    el 5 (el número inventado) — los dos casos más difíciles del examen.
#    No es mala suerte, es causa: entre más difícil el caso, más largo el
#    razonamiento, más probable quedarse sin cupo.
#    → El instrumento se rompió justo donde más falta hacía. Y eso es PEOR que
#      uno que no funciona nunca: las fallas parecen ruido al azar, pero están
#      sesgadas hacia los casos que sí podían reprobar. Sin mirarlas, la
#      conclusión habría sido "C1, C2, C3: 100%" — un 100% que se debía a que
#      las dos preguntas peligrosas no se calificaron.
MAX_TOKENS_JUEZ = 4000

# ⚠️ POR QUÉ NO SE USA agente.llamar_modelo(), QUE YA TIENE LOS FRENOS PUESTOS:
#    porque esa función tiene MODELO clavado adentro, y aquí hace falta otro.
#    Es exactamente la deuda que apareció en esta misma sesión: el CATÁLOGO
#    logró que el precio y el modelo estén siempre de acuerdo, pero solo en el
#    momento de IMPORTAR. El primer programa que necesita dos modelos a la vez
#    no puede reutilizar el freno.
#    → Anotado como deuda. Hoy se paga con un presupuesto propio, aquí abajo.


# ---------------------------------------------------------------------------
# 2) LA RÚBRICA SE LEE DEL ARCHIVO. NO SE COPIA AQUÍ.
# ---------------------------------------------------------------------------
# ⭐ ESTA ES LA DECISIÓN IMPORTANTE DE TODO EL ARCHIVO.
#
#    Lo fácil era pegar los seis criterios aquí como un texto largo. Y el día
#    que corrigieras rubrica.md —como se corrigió la fila 9 el mismo día que se
#    escribió— habría DOS rúbricas: la que TÚ lees y la que de verdad califica.
#    Nada te avisaría. Los veredictos seguirían saliendo, con buena cara.
#
#    Es el mismo defecto de MODELO y los precios sueltos, con otra ropa: dos
#    cosas que TIENEN que estar de acuerdo y nada las obliga.
#    → El instrumento vive en UN solo sitio, y es el que puedes leer con los ojos.
def cargar_rubrica():
    """Saca de rubrica.md la Parte 1: los seis criterios, y nada más.

    No se manda el archivo entero a propósito. Las partes 3 a 7 son el porqué
    del examen —para ti—, no instrucciones para el juez, y se pagarían en cada
    uno de los diez casos.
    """
    texto = (AQUI / "rubrica.md").read_text(encoding="utf-8")
    inicio = texto.index("## Parte 1")
    fin = texto.index("## Parte 2")
    trozo = texto[inicio:fin]

    # ⚠️ FRENO: si alguien renumera las secciones del .md, esto tiene que MORIR,
    #    no calificar con media rúbrica. Un juez con el instrumento incompleto
    #    produce números que se ven igual de buenos que los verdaderos.
    #    Misma familia del freno 10: no confíes en que algo salió bien solo
    #    porque no reventó.
    if len(trozo) < 1000:
        raise SystemExit(
            "\n❌ La Parte 1 de rubrica.md salió demasiado corta "
            f"({len(trozo)} caracteres).\n"
            "   ¿Se renumeraron las secciones? El juez no puede calificar con "
            "media rúbrica.\n"
        )
    return trozo


# ---------------------------------------------------------------------------
# 3) QUÉ CRITERIO APLICA A CUÁL PREGUNTA
# ---------------------------------------------------------------------------
# Copiado de la matriz de rubrica.md (Parte 2). Las casillas vacías NO se
# califican: promediar casillas que no aplican es promediar aire.
#
# ⚠️ La fila 9 no tiene C1 y eso fue una CORRECCIÓN, no un descuido: en una
#    pregunta cuya premisa es falsa ("el euro oficial en Colombia") no hay una
#    herramienta correcta que exigir. Se descubrió corriendo, no pensando.
APLICA = {
    1:  ["C1", "C2", "C3", "C6"],
    2:  ["C1", "C2", "C3", "C6"],
    3:  ["C1", "C2", "C3", "C6"],
    4:  ["C1", "C2", "C3", "C4", "C6"],
    # Sin C4: la pregunta ya dice "de mercado", así que no queda frontera que
    # levantar. La frontera tasa/trm es del agente al ELEGIR, y eso es C1.
    5:  ["C1", "C2", "C3", "C6"],
    6:  ["C1", "C2", "C3", "C4", "C6"],
    7:  ["C1", "C2", "C3", "C5", "C6"],
    8:  ["C5", "C6"],
    9:  ["C2", "C3", "C4", "C5", "C6"],   # C2 y C3, solo si la respuesta trae cifra
    10: ["C1", "C2", "C3", "C6"],
}

CRITERIOS = ["C1", "C2", "C3", "C4", "C5", "C6"]


# ---------------------------------------------------------------------------
# 4) LAS INSTRUCCIONES DEL JUEZ
# ---------------------------------------------------------------------------
SYSTEM_JUEZ = """Eres el juez de una evaluación de un agente de divisas.

Recibes tres cosas: la pregunta que le hicieron al agente, las herramientas que
pidió con lo que cada una le devolvió, y su respuesta final al usuario.

NO sabes qué modelo produjo esa respuesta, y no debes intentar adivinarlo.

Tu trabajo es calificar SOLO los criterios que se te indiquen, aplicando la
rúbrica de abajo al pie de la letra.

REGLAS:
- Para cada criterio escribes PRIMERO la justificación (una frase, concreta,
  citando lo que viste) y DESPUÉS el veredicto. Nunca al revés.
- Veredictos válidos, exactamente estos tres: "PASA", "FALLA", "NO APLICA".
- Si dudas entre PASA y FALLA, mira la lista de "FALLA si" del criterio: si la
  respuesta no cae en ninguno de esos casos, es PASA.
- Puedes responder "NO APLICA" en un criterio que sí te pidieron, cuando la
  condición del propio criterio no se cumple (por ejemplo, C2 si la respuesta
  no contiene ninguna cifra).
- Verifica las cifras: cada número de la respuesta tiene que poder rastrearse
  a lo que devolvió alguna herramienta. Si un número no sale de ahí, el agente
  lo calculó por su cuenta y eso es exactamente lo que C2 busca.
- NO calculas promedios, notas globales ni resúmenes. Eso lo hace un programa.
- NO opinas sobre nada que la rúbrica no pregunte.

Devuelves ÚNICAMENTE un objeto JSON, sin texto antes ni después y sin bloques
de código:
{"C1": {"justificacion": "...", "veredicto": "PASA"},
 "C2": {"justificacion": "...", "veredicto": "FALLA"}}

=== LA RÚBRICA ===
"""


def armar_caso(caso):
    """El texto que ve el juez.

    ⭐ Lo que NO va aquí es tan importante como lo que sí. Quedan fuera: el
       nombre del modelo, el costo, los tokens y el número de vueltas.
       Si el juez ve que algo fue barato o lento, califica distinto — y esas
       cosas ya las mide el `usage`, exacto y gratis.
       → No se le pregunta a un modelo lo que un número ya sabe.
    """
    partes = [f"PREGUNTA DEL USUARIO:\n{caso['pregunta']}\n"]

    if caso["llamadas"]:
        partes.append("HERRAMIENTAS QUE PIDIÓ EL AGENTE:")
        for i, llamada in enumerate(caso["llamadas"], 1):
            partes.append(
                f"{i}. {llamada['herramienta']}("
                f"{json.dumps(llamada['argumentos'], ensure_ascii=False)})\n"
                f"   devolvió: "
                f"{json.dumps(llamada['devolvio'], ensure_ascii=False)}"
            )
    else:
        partes.append("HERRAMIENTAS QUE PIDIÓ EL AGENTE: ninguna.")

    if caso["negados"]:
        negadas = ", ".join(n["herramienta"] for n in caso["negados"])
        partes.append(
            f"\nPERMISO DENEGADO para: {negadas}\n"
            f"(el agente pidió usar esa herramienta y el sistema no lo dejó; "
            f"la herramienta NO llegó a ejecutarse)"
        )

    partes.append(f"\nRESPUESTA FINAL DEL AGENTE:\n{caso['respuesta']}")
    partes.append(
        f"\nCALIFICA SOLO ESTOS CRITERIOS: {', '.join(APLICA[caso['caso']])}"
    )
    return "\n".join(partes)


def juzgar(caso, rubrica):
    """Una llamada. Sin bucle, sin herramientas, sin permisos."""
    global gastado_usd

    if gastado_usd >= PRESUPUESTO_JUEZ:
        raise SystemExit(
            f"\n❌ Presupuesto del juez agotado: ${gastado_usd:.4f} "
            f"de ${PRESUPUESTO_JUEZ:.2f}\n"
        )

    respuesta = agente.cliente.messages.create(
        model=MODELO_JUEZ,
        max_tokens=MAX_TOKENS_JUEZ,
        system=SYSTEM_JUEZ + rubrica,
        messages=[{"role": "user", "content": armar_caso(caso)}],
    )

    gastado_usd += (respuesta.usage.input_tokens * PRECIO_ENTRADA
                    + respuesta.usage.output_tokens * PRECIO_SALIDA) / 1_000_000

    texto = next((b.text for b in respuesta.content if b.type == "text"), "")

    # ⚠️ EL JUEZ PUEDE FALLAR, Y ESO NO PUEDE CONVERTIRSE EN UN CERO SILENCIOSO.
    #    → Un fallo del INSTRUMENTO disfrazado de mala nota del EXAMINADO es la
    #      peor mentira que puede contar una evaluación: las dos cosas se ven
    #      exactamente igual en la tabla final.
    #
    # ⭐ Y SON DOS FALLAS DISTINTAS, NO UNA. En la primera corrida las dos se
    #    veían iguales en pantalla ("no devolvió JSON legible") y tenían causas
    #    diferentes: una se quedó sin cupo, la otra escribió algo ilegible.
    #    Separarlas es tu propia regla del `motivo`, quinta vez: un registro que
    #    no distingue POR QUÉ pasó algo no sirve para arreglarlo.
    if respuesta.stop_reason == "max_tokens":
        return {
            "_fallo": "sin_cupo",
            "_detalle": f"se acabaron los {MAX_TOKENS_JUEZ} tokens "
                        f"(gastó {respuesta.usage.output_tokens}); "
                        f"bloques: {[b.type for b in respuesta.content]}",
            "_texto": texto,
            "_stop_reason": respuesta.stop_reason,
        }, respuesta.usage

    try:
        crudo = texto[texto.index("{"):texto.rindex("}") + 1]
        veredictos = json.loads(crudo)
    except (ValueError, json.JSONDecodeError):
        return {
            "_fallo": "json_ilegible",
            "_detalle": f"terminó bien (stop_reason={respuesta.stop_reason}) "
                        f"pero el texto no se pudo leer como JSON",
            "_texto": texto,
            "_stop_reason": respuesta.stop_reason,
        }, respuesta.usage

    return veredictos, respuesta.usage


# ---------------------------------------------------------------------------
# 5) LA CORRIDA
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    EXAMINADO = agente.MODELO          # a quién se está calificando
    ENTRADA = AQUI / f"respuestas_{EXAMINADO}.jsonl"
    SALIDA = AQUI / f"veredictos_{EXAMINADO}.jsonl"

    if not ENTRADA.exists():
        raise SystemExit(
            f"\n❌ No existe {ENTRADA.name}. Corre primero:  python examen.py\n"
        )

    rubrica = cargar_rubrica()

    # ⚠️ LA ÚLTIMA LÍNEA DE CADA CASO GANA, y hay una razón concreta:
    #    el caso 7 está DOS veces en el archivo. La primera corrida quedó
    #    inválida porque el examinador negaba TODO en vez de solo
    #    guardar_reporte, y el agente se quedó sin datos.
    #    Esa línea NO se borró —es la evidencia del defecto, igual que la línea
    #    13 del registro de la sesión 15— pero no se juzga.
    #    → La evidencia de un error se guarda; lo que no se hace es medirla.
    casos = {}
    for linea in open(ENTRADA, encoding="utf-8"):
        if linea.strip():
            caso = json.loads(linea)
            casos[(caso["caso"], caso["repeticion"])] = caso

    # Recalificar solo unos casos, sin volver a pagar los diez:
    #     python juez.py        -> todos
    #     python juez.py 4 5    -> solo esos dos
    # Igual que en examen.py, se pasa por la línea de comandos y no editando el
    # archivo: un ajuste temporal guardado en un archivo deja de ser temporal.
    SOLO = [int(a) for a in sys.argv[1:]]
    if SOLO:
        casos = {k: v for k, v in casos.items() if v["caso"] in SOLO}

    print(f"Examinado : {EXAMINADO}")
    print(f"Juez      : {MODELO_JUEZ}  (max_tokens={MAX_TOKENS_JUEZ})")
    print(f"Casos     : {len(casos)}   (leídos de {ENTRADA.name})"
          + (f"   SOLO {SOLO}" if SOLO else ""))
    print(f"Rúbrica   : {len(rubrica)} caracteres, leídos de rubrica.md")
    print(f"Veredictos: {SALIDA.name}\n")

    filas = []
    fallos = []

    for clave in sorted(casos):
        caso = casos[clave]
        veredictos, uso = juzgar(caso, rubrica)

        if veredictos.get("_fallo"):
            fallos.append((caso["caso"], veredictos["_fallo"]))
            print(f"  caso {caso['caso']:>2}: ⚠️  FALLÓ EL JUEZ "
                  f"({veredictos['_fallo']}) — {veredictos['_detalle']}")
        else:
            resumen = "  ".join(
                f"{c}:{veredictos.get(c, {}).get('veredicto', '???')}"
                for c in APLICA[caso["caso"]]
            )
            print(f"  caso {caso['caso']:>2}: {resumen}")

        fila = {
            "caso": caso["caso"],
            "repeticion": caso["repeticion"],
            "examinado": EXAMINADO,
            "juez": MODELO_JUEZ,
            "pregunta": caso["pregunta"],
            "veredictos": veredictos,
        }
        filas.append(fila)
        with open(SALIDA, "a", encoding="utf-8") as f:
            f.write(json.dumps(fila, ensure_ascii=False) + "\n")

    # -----------------------------------------------------------------------
    # 6) EL RECUENTO LO HACE PYTHON, NO EL JUEZ
    # -----------------------------------------------------------------------
    # ⭐ Es la regla central de todo el nivel 5b: la herramienta calcula, el
    #    modelo solo decide. Pedirle al juez que además promedie es darle una
    #    oportunidad más de equivocarse a cambio de absolutamente nada.
    # ⚠️ EL RECUENTO SE HACE SOBRE EL ARCHIVO COMPLETO, NO SOBRE ESTA CORRIDA.
    #    Si recalificas dos casos con `python juez.py 4 5`, el recuento tiene
    #    que seguir siendo el de los diez — si no, verías "C2: 1/1 = 100%" y
    #    creerías que ese es el resultado del examen.
    #    Y aquí también gana la ÚLTIMA línea de cada caso: recalificar no borra
    #    el veredicto viejo (es la evidencia de que el juez falló), lo sustituye.
    todos = {}
    for linea in open(SALIDA, encoding="utf-8"):
        if linea.strip():
            f = json.loads(linea)
            todos[(f["caso"], f["repeticion"])] = f
    filas = [todos[k] for k in sorted(todos)]

    print(f"\n{'=' * 60}")
    print(f"RECUENTO POR CRITERIO  ({len(filas)} casos de {SALIDA.name})")
    for c in CRITERIOS:
        pasa = sum(1 for f in filas
                   if f["veredictos"].get(c, {}).get("veredicto") == "PASA")
        falla = sum(1 for f in filas
                    if f["veredictos"].get(c, {}).get("veredicto") == "FALLA")
        total = pasa + falla

        if total == 0:
            print(f"  {c}: sin casillas calificadas")
            continue

        # ⚠️ El porcentaje va SIEMPRE con su denominador al lado. "67%" solo,
        #    sacado de 2 de 3, es un número con más autoridad de la que se ganó.
        aviso = "   ⚠️ pocas muestras: este % no ordena a nadie" if total < 4 else ""
        print(f"  {c}: {pasa}/{total} PASA   ({pasa / total * 100:.0f}%){aviso}")

    # Los fallos también se cuentan sobre el archivo entero: un caso que falló
    # en una corrida anterior y hoy no se recalificó SIGUE sin calificar.
    fallos = [(f["caso"], f["veredictos"]["_fallo"])
              for f in filas if f["veredictos"].get("_fallo")]

    if fallos:
        print(f"\n  ⚠️ EL JUEZ FALLÓ EN {len(fallos)} CASO(S): "
              + ", ".join(f"#{n} ({m})" for n, m in fallos))
        print("     NO cuentan como fallos del agente, y los porcentajes de")
        print("     arriba están calculados SIN ellos. Un porcentaje al que le")
        print("     faltan los casos difíciles es un porcentaje optimista.")
        print("     Vuelve a calificarlos:  python juez.py "
              + " ".join(str(n) for n, _ in fallos))

    print(f"\nGasto del juez: ${gastado_usd:.4f} de ${PRESUPUESTO_JUEZ:.2f}")
    print(f"Veredictos en : {SALIDA.name}")

    # ⚠️ La línea más importante de la salida, y es una instrucción para ti.
    print("\n⚠️ AHORA VIENE LO INCÓMODO, Y ES EL PASO QUE LA GENTE SE SALTA:")
    print("   abre ese archivo y LEE LAS JUSTIFICACIONES.")
    print("   Algunos veredictos van a ser errores del juez, no del agente.")
    print("   Un juez sin auditar es un número con autoridad prestada.")
