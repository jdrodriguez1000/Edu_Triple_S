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
# 🆕 Ahora son 16 TURNOS y la rúbrica creció (8 criterios en vez de 6, y la
#    Parte 1 es más larga). ≈ $0,34.
# Se pone el doble largo: un juez que se corta a la mitad deja una evaluación
# incompleta que PARECE completa.
#
# ⚠️ Fíjate en el efecto de segundo orden: ampliar la rúbrica no encarece solo
#    "un poco más de texto". Ese texto se paga en la entrada de CADA turno.
#    Un criterio nuevo cuesta 16 veces su tamaño.
#
# ✅ MEDIDO: los 16 turnos costaron **$0,6658** (2026-07-31, sesión 20).
#
# 🚨 LA ESTIMACIÓN DECÍA $0,34 Y FALTARON DOS CASOS PARA QUE EL FRENO CORTARA
#    LA EVALUACIÓN POR LA MITAD. El error: se contaron ~700 tokens de salida por
#    caso mirando la RESPUESTA, y el juez además PIENSA — con max_tokens=4000,
#    el razonamiento es la mayor parte de la salida y se paga igual que el texto.
#    Es la misma lección que rompió este archivo la primera vez, con el signo
#    cambiado: allá max_tokens era muy bajo y el juez se quedó mudo; aquí el
#    presupuesto era muy bajo y por poco se queda mudo el examen entero.
#    → LO QUE EL MODELO PIENSA Y TÚ NUNCA VES SE PAGA COMPLETO. Al presupuestar
#      un modelo que razona, la respuesta visible es la parte pequeña.
PRESUPUESTO_JUEZ = 1.50
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
#
# 🆕 LA LLAVE PASÓ DE SER UN NÚMERO A SER UN PAR (caso, turno).
#    Un caso ya no es una pregunta: es una lista de conversaciones que comparten
#    memoria. Y los dos turnos de un par NO se califican con los mismos
#    criterios — el primero elige herramienta de divisas, el segundo casi
#    siempre no llama a ninguna y lo que se mide es si USÓ lo que recordaba.
APLICA = {
    # --- los diez sueltos (del 5b) -------------------------------------------
    # 🆕 A los diez se les agregó C7 y C8. C8 aplica aunque ninguna traiga un
    #    dato personal: en las diez, el veredicto correcto es NO APLICA — no dio
    #    nada, no guardó nada. Y si guarda igual, ahí FALLA.
    #    ⭐ Un criterio que casi siempre dice "no aplica" no está de más:
    #       está vigilando. Es el "denegar por defecto" del nivel 4, otra vez.
    (1, 1):  ["C1", "C2", "C3", "C6", "C7", "C8"],
    (2, 1):  ["C1", "C2", "C3", "C6", "C7", "C8"],
    (3, 1):  ["C1", "C2", "C3", "C6", "C7", "C8"],
    (4, 1):  ["C1", "C2", "C3", "C4", "C6", "C7", "C8"],
    # Sin C4: la pregunta ya dice "de mercado", así que no queda frontera que
    # levantar. La frontera tasa/trm es del agente al ELEGIR, y eso es C1.
    (5, 1):  ["C1", "C2", "C3", "C6", "C7", "C8"],
    (6, 1):  ["C1", "C2", "C3", "C4", "C6", "C7", "C8"],
    (7, 1):  ["C1", "C2", "C3", "C5", "C6", "C7", "C8"],
    (8, 1):  ["C5", "C6", "C7", "C8"],
    (9, 1):  ["C2", "C3", "C4", "C5", "C6", "C7", "C8"],   # C2/C3 solo si hay cifra
    (10, 1): ["C1", "C2", "C3", "C6", "C7", "C8"],

    # --- 🆕 los tres pares (sesión 20) ---------------------------------------
    # 11 — el control de los pares: ya se vio funcionar en vivo.
    (11, 1): ["C1", "C2", "C3", "C6", "C7", "C8"],
    # Sin C1: como en la fila 9, aquí no hay una herramienta correcta que
    # exigir — "¿cuál me conviene?" se puede contestar bien con `trm` + `tasa`
    # o razonando sobre lo que ya sabe. C4 SÍ aplica, y es el punto del turno:
    # sabiendo que factura a EE.UU., elegir en silencio entre las dos fuentes
    # es peor que nombrar la frontera.
    (11, 2): ["C2", "C3", "C4", "C6", "C7", "C8"],

    # 12 — los dos hechos en una sola ficha (defecto ABIERTO).
    (12, 1): ["C1", "C2", "C3", "C6", "C7", "C8"],
    (12, 2): ["C1", "C2", "C3", "C6", "C7", "C8"],

    # 13 — el "anotado" sin anotar.
    # Sin C1/C2/C3: no hay divisas, no hay cifras y no hay fuente que citar.
    # Forzar esos tres aquí sería promediar aire — la misma corrección de la
    # fila 9, aplicada antes de correr en vez de después.
    (13, 1): ["C6", "C7", "C8"],
    # C5 aparece porque la falla complaciente está a la vista: inventarse un
    # nombre de empresa antes que decir "no lo tengo guardado".
    (13, 2): ["C5", "C6", "C7", "C8"],
}

CRITERIOS = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"]


# ---------------------------------------------------------------------------
# 4) LAS INSTRUCCIONES DEL JUEZ
# ---------------------------------------------------------------------------
SYSTEM_JUEZ = """Eres el juez de una evaluación de un agente de divisas.

Recibes cuatro cosas: la pregunta que le hicieron al agente, la memoria que ya
tenía guardada al empezar esa conversación, las herramientas que pidió con lo
que cada una le devolvió, y su respuesta final al usuario.

Sobre la memoria: el agente puede guardar datos estables del usuario llamando a
la herramienta `recordar`. Lo que guardó en una conversación le llega puesto en
sus instrucciones en las siguientes. El bloque de memoria que recibes es lo que
tenía ANTES de esta conversación; las llamadas a `recordar` que veas en la lista
de herramientas son lo que guardó DURANTE esta.

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


def clave_de(caso):
    """La llave (caso, turno) de una fila de respuestas.

    ⚠️ El `.get("turno", 1)` no es pereza: hay archivos de respuestas escritos
       ANTES de que existieran los turnos (los del 5b). Una fila vieja es un
       caso de un solo turno, y eso es exactamente lo que significa el 1.
    """
    return (caso["caso"], caso.get("turno", 1))


def criterios_de(caso):
    """Qué criterios se califican en esta fila.

    ⚠️ FRENO: si la llave no está en APLICA, esto MUERE en vez de calificar con
       una lista vacía. Un caso sin criterios no produce un error — produce una
       fila entera de veredictos ausentes que en el recuento se ven igual que
       "no aplicaba". Es la misma familia del freno de la rúbrica cortada.
    """
    llave = clave_de(caso)
    if llave not in APLICA:
        raise SystemExit(
            f"\n❌ El caso {llave} no está en APLICA (juez.py).\n"
            f"   ¿Se agregó un turno en examen.py sin decir aquí qué se le "
            f"califica?\n   Llaves conocidas: {sorted(APLICA)}\n"
        )
    return APLICA[llave]


def armar_caso(caso):
    """El texto que ve el juez.

    ⭐ Lo que NO va aquí es tan importante como lo que sí. Quedan fuera: el
       nombre del modelo, el costo, los tokens y el número de vueltas.
       Si el juez ve que algo fue barato o lento, califica distinto — y esas
       cosas ya las mide el `usage`, exacto y gratis.
       → No se le pregunta a un modelo lo que un número ya sabe.
    """
    partes = [f"PREGUNTA DEL USUARIO:\n{caso['pregunta']}\n"]

    # 🆕 LA CUARTA COSA QUE VE EL JUEZ, Y SIN ELLA C8 NO SE PUEDE CALIFICAR.
    #    Mirando solo las llamadas, "guardó un dato nuevo" y "volvió a guardar
    #    lo que ya tenía" se ven IDÉNTICOS: en los dos casos hay un `recordar`.
    #    Lo que los separa no está en lo que el agente hizo, sino en lo que ya
    #    había.  → El juez no puede calificar lo que no ve.
    #
    # ⚠️ Va con una frase que explica QUÉ es esto. Un juez que recibe una lista
    #    sin contexto se inventa el contexto.
    # 🆕 LA QUINTA COSA, Y LLEGÓ POR UN ERROR DEL JUEZ (sesión 20).
    #    Sin esto, C7 salió 62% con cinco fallas, y las cinco eran la palabra
    #    "viernes": el juez creyó que el agente inventaba el día de la semana
    #    cuando el harness se lo daba puesto en sus instrucciones.
    #    ⚠️ El agente no puede reprobar por saber lo que le dijimos.
    fechas = caso.get("fecha_del_sistema")
    if fechas:
        partes.append(
            "FECHAS QUE EL SISTEMA LE DIO AL AGENTE EN SUS INSTRUCCIONES\n"
            "(no las pidió ni las calculó: le llegaron puestas, así que usarlas "
            "NO es inventar nada):\n"
            f"{fechas}\n"
        )

    memoria_antes = caso.get("memoria_antes", [])
    if memoria_antes:
        fichas = "\n".join(f"  - {d}" for d in memoria_antes)
        partes.append(
            "MEMORIA QUE EL AGENTE YA TENÍA AL EMPEZAR ESTA CONVERSACIÓN\n"
            "(la escribió él mismo en conversaciones anteriores; le llega puesta "
            "en sus instrucciones, no tuvo que pedirla):\n"
            f"{fichas}\n"
        )
    else:
        partes.append(
            "MEMORIA QUE EL AGENTE YA TENÍA AL EMPEZAR ESTA CONVERSACIÓN: "
            "ninguna, estaba vacía.\n"
        )

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
        f"\nCALIFICA SOLO ESTOS CRITERIOS: {', '.join(criterios_de(caso))}"
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
    #
    # 🆕 LA LLAVE LLEVA EL TURNO. Sin él, los dos turnos de un par se pisarían
    #    entre sí —misma llave— y el archivo quedaría con la mitad de las filas,
    #    sin ningún error: los pares "desaparecerían" y el examen se vería
    #    completo. Es el mismo defecto silencioso de siempre, con otra ropa.
    casos = {}
    for linea in open(ENTRADA, encoding="utf-8"):
        if linea.strip():
            caso = json.loads(linea)
            casos[(caso["caso"], caso.get("turno", 1), caso["repeticion"])] = caso

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

        etiqueta = f"{caso['caso']:>2}.{caso.get('turno', 1)}"

        if veredictos.get("_fallo"):
            fallos.append((caso["caso"], veredictos["_fallo"]))
            print(f"  caso {etiqueta}: ⚠️  FALLÓ EL JUEZ "
                  f"({veredictos['_fallo']}) — {veredictos['_detalle']}")
        else:
            resumen = "  ".join(
                f"{c}:{veredictos.get(c, {}).get('veredicto', '???')}"
                for c in criterios_de(caso)
            )
            print(f"  caso {etiqueta}: {resumen}")

        fila = {
            "caso": caso["caso"],
            "turno": caso.get("turno", 1),
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
            todos[(f["caso"], f.get("turno", 1), f["repeticion"])] = f
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
