"""worker.py — A.1 del nivel 8: un agente de UNA capa, llamable como función.

    QUÉ ES UN WORKER, EN UNA FRASE

Es tu agente del 5b con otro system prompt, menos herramientas, y una boca
distinta: no habla contigo por pantalla — DEVUELVE UN VALOR.

⭐ ESE ES TODO EL DESCUBRIMIENTO DE A.1, y conviene decirlo antes que nada:
   un worker NO es una cosa nueva. Media confusión del multi-agente se cae
   sola el día que ves que el "sub-agente" es el mismo bucle del nivel 3.


    LAS CUATRO DIFERENCIAS DE VERDAD (y ninguna es de tecnología)

1. ENCARGO ESTRECHO. El del 5b es "un asistente de tasas de cambio" y atiende
   lo que le caiga. Este sabe hacer UNA cosa: pasar UN monto de UNA moneda a
   pesos, con fuente y fecha.

2. MENOS HERRAMIENTAS. Dos, no seis. Y esto no es ahorro de tokens (que
   también): es la decisión de diseño que el sobre del bloque 0 dejó sellada
   como predicción. Ver el apartado LA CAJA DE HERRAMIENTAS, abajo.

3. NO PIDE PERMISO — Y NO PUEDE. El del 5b para el bucle y hace un input().
   Aquí no hay nadie mirando: al worker lo va a llamar un programa, no una
   persona. 🔑 En un worker el sistema de permisos DEJA DE SER UNA PREGUNTA Y
   SE VUELVE LA CAJA DE HERRAMIENTAS: lo que no puede hacer, no lo lleva.
   → Por eso este worker no lleva `guardar_reporte`. No es que se le pregunte
     antes de escribir: es que no sabe escribir.

4. DEVUELVE UN DICCIONARIO, NO IMPRIME UNA FRASE. Un agente que solo imprime
   se puede leer; uno que devuelve se puede USAR. Esta es la línea que lo
   convierte en herramienta de otro agente, y es lo que abre A.2.


    LA CAJA DE HERRAMIENTAS: `tasa` y `convertir`. Y lo que eso cuesta.

🔒 Está sellado en `SOBRE.md` como predicción, escrita ANTES de medir nada:

   "Si el worker del dólar lleva solo `tasa` y `convertir`, NO PUEDE cometer
    el error de A (mezclar TRM oficial y mercado sin decirlo), pero TAMPOCO
    puede levantar la frontera de C4, porque no sabe que `trm` existe."

⚠️ Léelo dos veces, porque es la trampa entera del multi-agente en dos
   renglones: EL AISLAMIENTO QUE LO HACE BUENO ES EL MISMO QUE LE QUITA EL
   CONTEXTO PARA AVISAR. Dar menos contexto no sale gratis: se paga en
   silencios, que es la forma de error más difícil de ver (LM.15).
   Aquí solo se NOMBRA. Se mide en el bloque F, cuando se abra el sobre.


    POR QUÉ ESTE ARCHIVO REPITE EL BUCLE EN VEZ DE IMPORTARLO

`agente.ejecutar_agente()` tiene su system prompt y su menú CLAVADOS en
variables del módulo. Para reutilizarlo habría que parametrizarlo, o sea
EDITAR `05b-proyecto/agente.py`.

🚨 Y ese archivo es EL CONTENDIENTE A: ya está medido, y su medición es lo que
   el sobre del bloque 0 protege. Aunque el cambio fuera inofensivo, la línea
   base costó dinero y su valor entero depende de que A siga siendo A.
   → Se acepta la repetición A SABIENDAS, con la razón escrita aquí.

📌 Y se repite lo MENOS posible: de `agente` se importan las piezas que son
   DATO y no comportamiento — el modelo, el menú de herramientas, el puente a
   las funciones, el cálculo del costo y la política de reintentos. Copiar las
   descripciones de las herramientas sería peor que copiar el bucle: si el
   worker las describiera con otras palabras, el duelo del bloque F mediría
   redacción de prompts, no arquitectura.

📌 Deuda anotada, no olvidada: cuando el sobre esté abierto (bloque F), los dos
   bucles se pueden unificar sin riesgo. Antes, no.


    CÓMO SE CORRE

    python worker.py                 # una demo: el worker del dólar, una vez

💰 CUESTA DINERO. Poco (centavos), pero cuesta: llama al modelo de verdad.
"""

import json
import random
import sys
import threading
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

import anthropic

sys.stdout.reconfigure(encoding="utf-8")

AQUI = Path(__file__).resolve().parent

# El contendiente A vive en otra carpeta. Se importa, no se copia — la misma
# regla que ya usa `linea_base.py`. Importar `agente` NO corre su corrida: eso
# está detrás de su `if __name__ == "__main__"`.
sys.path.insert(0, str(AQUI.parent / "05b-proyecto"))

import agente          # noqa: E402
import contexto        # noqa: E402


# ---------------------------------------------------------------------------
# 1) LA CONFIGURACIÓN DEL WORKER
# ---------------------------------------------------------------------------

# ⚠️ EL MISMO MODELO EN LOS DOS LADOS DEL DUELO. Está escrito en la pieza 0.4:
#    si A corre con haiku y B con opus, lo medido es el modelo, no el esquema.
#    Por eso no se escribe un nombre aquí: se toma el de A.
MODELO = agente.MODELO

# Un worker da MENOS vueltas que el agente completo, y no es por prudencia: es
# que tiene menos que hacer. Su encargo es tasa -> convertir -> responder, o
# sea 3 vueltas. Con 5 sobra, y el freno sigue mordiendo si algo se descarrila.
MAX_VUELTAS_WORKER = 5

# El presupuesto es POR LLAMADA AL WORKER, no de la corrida entera.
# ⭐ Y esta diferencia importa: en A el presupuesto era global porque había UNA
#    conversación. Aquí va a haber tres workers, y un tope global se lo comería
#    el primero que se descarrile, dejando a los otros dos sin gasolina por un
#    problema que no era suyo. Un tope por worker AÍSLA EL DAÑO.
PRESUPUESTO_WORKER_USD = 0.05

# ⭐ C.4 — EL PLAZO. La tercera cosa que se le puede acabar a un worker, después
#    del dinero y de las vueltas: EL TIEMPO DE QUIEN LO ESPERA.
#
# 🚨 ANTES DE ESTA LÍNEA EL PLAZO EXISTÍA, PERO NADIE LO HABÍA DECIDIDO. Salía
#    de multiplicar tres constantes escogidas por otros motivos —5 vueltas × 3
#    intentos × 30 s de timeout, más las esperas del reintento— y daba **490
#    segundos: 8,2 minutos por worker**, medido en `fallos.py`. Un plazo que
#    nadie eligió no es un plazo: es un residuo.
#
# 📌 Y EL NÚMERO SALE DE UN DATO, NO DE UNA INTUICIÓN. Los 99 workers pagados
#    del curso: mediana **2,28 s**, p90 **5,73 s**, el peor de todos **17,94 s**.
#    90 s son **5 veces el peor caso jamás visto** — o sea, un freno que no
#    puede morder a uno legítimo — y a la vez **5,4 veces menos** que el residuo
#    que había.
# 🔑 Aquí sí se elige por arriba a propósito, y es la lección de ayer al revés:
#    el p90 era el precio equivocado para un instrumento porque le perdonaba la
#    vida al que se quería ver ahogarse. **Esto no es un instrumento, es un
#    freno**, y en un freno equivocarse por arriba solo cuesta espera.
LIMITE_WORKER_SEGUNDOS = 90.0

# ---------------------------------------------------------------------------
# 🚨 C.2 · CIERRE — EL PRECIO DE LA PRÓXIMA LLAMADA, Y POR QUÉ HAY QUE ADIVINARLO
# ---------------------------------------------------------------------------
# Hasta la sesión 98 el freno preguntaba `if gastado >= presupuesto`. Suena bien
# y NO ACOTA NADA, y se vio con un número: la corrida apretada gastó $0,018388
# contra un techo de $0,014424 — **un 27,5 % por encima**, y se pasaron los
# CUATRO participantes.
#
# El mecanismo cabe en una línea: la comprobación es ANTERIOR a la llamada, pero
# **nadie sabe cuánto va a costar la llamada que está autorizando**. Un freno así
# no acota en `techo`: acota en `techo + N × coste_de_una_llamada`.
#
# ⭐ Y LO QUE MÁS ENSEÑA ES QUE ESTE DEFECTO SE DESCARTÓ EN OTRO CANDIDATO.
#    Al elegir esquema (sesión 98) se rechazó la bolsa común escribiendo que su
#    pega era «hay que ESTIMAR lo que costará una llamada antes de hacerla».
#    El esquema elegido tenía la misma pega — sólo que **escondida**: repartir a
#    la entrada no libra de estimar, **aplaza la estimación al momento de
#    autorizar, que es donde no se ve**. 🔑 Un defecto que sabes nombrar en la
#    opción que descartas puede estar entero en la que elegiste.
#
# → Así que se estima, y la estimación se declara con sus dos partes, LAS DOS
#   MEDIDAS sobre las 170 llamadas pagadas que hay en los registros del nivel:
#
# 🚨 Y LA PRIMERA VERSIÓN DE ESTA CONSTANTE ESTABA MAL, con el motivo escrito
#    tres líneas más abajo en el archivo de al lado. Se puso $0,002404 — *la
#    MEDIA de las dos llamadas de la demo C.1*. Al contarlas todas:
#
#        170 llamadas pagadas · min $0,000991 · mediana $0,002432 · max $0,007066
#        **96 de las 170 (el 56 %) costaron MÁS que $0,002404**
#
#    Una estimación que se queda corta más de la mitad de las veces no es una
#    estimación: es la media disfrazada de tope. Y `presupuesto.py` ya lo tenía
#    escrito desde ayer —*«un presupuesto se calcula con el precio malo, no con
#    el medio»*— sobre la holgura, sin que nadie lo aplicara aquí.
# 🔑 `LM.68` otra vez: **lo que faltaba no era un dato, era un lector.**
COSTE_ESTIMADO_LLAMADA_USD = 0.004546   # MEDIDO: p90 de las 170 llamadas pagadas
#
# ⚠️ Se toma el **p90 y no el máximo** ($0,007066), y la razón va escrita porque
#    es una decisión, no un descuido: con el máximo el freno de operación normal
#    empezaría a morder por una llamada rara que se vio UNA vez. Un tope que
#    cubre el peor caso imaginable **es una avería con buena intención**. El p90
#    cubre nueve de cada diez y deja el resto a la holgura.

# El segundo dato: dentro de una misma corrida, ¿cuánto crece una llamada
# respecto de la anterior? Medido sobre 108 pares consecutivos:
#     min 0,51x · mediana 1,08x · p90 1,22x · max 1,51x
# ⭐ Que la mediana sea >1 no es casualidad ni ruido: cada vuelta reenvía todo el
#    historial, así que la entrada SÓLO CRECE. Por eso la peor llamada ya pagada
#    sirve de suelo para la siguiente — pero hay que **subirla**, no copiarla.
CRECIMIENTO_POR_VUELTA = 1.22           # MEDIDO: p90 de 108 pares consecutivos


def estimar_proxima_llamada(peor_vista_usd=0.0):
    """Cuánto va a costar la llamada que estoy a punto de autorizar.

    Dos fuentes, y se toma **la mayor de las dos** a propósito:

      · el p90 medido, que es lo único que hay antes de la 1ª llamada;
      · la peor llamada que ESTE worker ya pagó hoy, **multiplicada por el
        crecimiento medido**.

    ⭐ La segunda no es un adorno: dentro de un worker el historial sólo crece,
       así que cada llamada manda más tokens de entrada que la anterior. La peor
       vista no es una media — es un **suelo** para la siguiente, y el 1,22x es
       lo que hace que sea un suelo de la SIGUIENTE y no de la anterior.

    ⚠️ Y AQUÍ VA LA HONESTIDAD DEL ARREGLO, ESCRITA ANTES DE MEDIRLO: una
       estimación puede quedarse corta. Si la llamada real cuesta más de lo
       estimado, el techo se pasa igual — menos, pero se pasa. El freno arreglado
       acota en `techo + error_de_estimación`, no en `techo`.
       🔑 Por eso el worker **cuenta cuántas veces se quedó corto** y lo devuelve
          en `estimaciones_cortas`. Un arreglo que no trae cómo se comprueba a sí
          mismo es la nota que `LM.13` prohíbe. Ese contador es lo que puso `P12`
          en rojo y destapó que la constante era una media.
    """
    return max(COSTE_ESTIMADO_LLAMADA_USD, peor_vista_usd * CRECIMIENTO_POR_VUELTA)

# --- El registro, y vive AQUÍ a propósito ----------------------------------
# 🚨 ES LA LECCIÓN DE LA SESIÓN 50 DE TEAPP, APLICADA ANTES DE QUE MUERDA: allá
#    el que estaba ensuciando los datos de verdad era el instrumento de medida.
#    Si el worker escribiera en `05b-proyecto/registro_*.jsonl`, sus líneas
#    caerían dentro del registro del CONTENDIENTE A, mezcladas con las de la
#    línea base y sin decir nada. Sin error. Sin aviso.
REGISTRO = AQUI / f"registro_workers_{MODELO}.jsonl"


# --- LA CAJA: qué herramientas lleva este worker ---------------------------
# Dos nombres. Nada más. Y fíjate en lo que NO está:
#   trm, historial, trm_en_fecha -> no sabe que existe la TRM oficial
#   guardar_reporte              -> no sabe escribir en el disco
HERRAMIENTAS_DIVISA = ["tasa", "convertir"]


# ---------------------------------------------------------------------------
# EL CONTRATO — llegó en A.3, y llegó por un defecto MEDIDO
# ---------------------------------------------------------------------------
# 🐛 EL DEFECTO, tal como salió en la demo de A.2 (2026-08-20):
#    la herramienta `tasa` le devolvió al worker del CAD
#        'fuente': 'mercado (open.er-api.com)'
#    y el worker respondió "…según la tasa de mercado del 20 de agosto".
#    SE COMIÓ EL NOMBRE AL REDACTAR. El orquestador ya no podía recuperarlo:
#    solo había recibido esa frase.
#
# 🔑 LA CAUSA NO ERA EL WORKER, ERA LA FRONTERA. Mientras lo que viaje entre
#    capas sea prosa libre, cada worker decide qué cabe — y tres workers con el
#    MISMO system prompt redactaron de tres formas distintas.
#    → Un contrato no es "pedirle al modelo que redacte mejor". Es quitarle la
#      decisión.
#
# ⭐ Y AQUÍ ESTÁ LO QUE MÁS ENSEÑA DE TODA LA PIEZA:
#    el dato NO se le vuelve a pedir al modelo. `fuente` y `actualizado` YA
#    pasaron por este harness, dentro del `tool_result` de `tasa`. Estaban en
#    Python. Pedírselos otra vez al modelo sería pagar tokens para que nos
#    repita, de memoria y con sus palabras, algo que ya teníamos exacto.
#    → REGLA: antes de pedirle un dato al modelo, mira si ya pasó por tu
#      harness. Lo que pasó por el harness es exacto y gratis; lo que pasa por
#      el modelo es aproximado y se paga.
#
# ⚠️ EL PRECIO, DICHO ENTERO: esto ACOPLA el contrato a estas dos herramientas.
#    Si mañana el worker usara `trm`, esta función habría que tocarla. Se paga
#    a sabiendas, y por eso el acoplamiento vive en UN sitio con nombre y no
#    repartido por el bucle.

CAMPOS_DIVISA = ["moneda", "monto", "pesos", "tasa", "fuente", "fecha"]


def discrepancias_divisa(datos, pedido):
    """¿El contrato responde A LO QUE SE PREGUNTÓ? — C.3, y nació de una mentira.

    🐛 EL DEFECTO, medido en la corrida pagada de la sesión 99:
       se pidió **CAD**, el modelo llamó a `tasa("USD")`, y el contrato subió
       entero —seis campos llenos, `faltan: []`— **con los números de otra
       pregunta**. Nadie gritó. Lo cazó un humano leyendo la salida.

    🔑 LA CAUSA NO ERA QUE FALTARA UN CAMPO: era que `moneda` ESTABA SOLA EN SU
       RENGLÓN. Se llenaba con lo que la herramienta devolvió, y no había
       ningún otro dato que pudiera contradecirla. Es `LM.66` exacto: *un dato
       que nadie puede contradecir no es que sea correcto — es que no es
       comprobable*, y las dos cosas dan el mismo verde.
       → El testigo que faltaba no estaba en la respuesta. Estaba en la
         PREGUNTA, y el contrato no la recibía.

    ⭐ DEVUELVE TRES COSAS DISTINTAS, Y LA DIFERENCIA ES LA LECCIÓN:
       · `None` — NO SE COMPROBÓ (nadie pasó `pedido`).
       · `[]`   — se comprobó y cuadra.
       · lista  — se comprobó y NO cuadra, con la frase de qué no cuadra.
       `None` y `[]` se ven casi igual en pantalla y significan lo contrario.
       Confundirlos es `LM.15`: un instrumento ciego no da un dato falso, da
       **silencio**, y el silencio se lee como confirmación.
    """
    if not pedido:
        return None                      # ⚠️ no comprobado ≠ comprobado y bien

    fallos = []

    esperada = (pedido.get("moneda") or "").upper()
    traida = (datos.get("moneda") or "").upper()
    # Si `traida` está vacía, eso YA lo dice `faltan`: no se cuenta dos veces.
    if esperada and traida and traida != esperada:
        fallos.append(f"moneda: se pidió {esperada} y el contrato trae {traida}")

    # El monto se comprueba por lo mismo: un worker puede convertir 100 cuando
    # le pidieron 250 y devolver un contrato completo y coherente consigo mismo.
    esperado = pedido.get("monto")
    tenido = datos.get("monto")
    if esperado is not None and tenido is not None:
        try:
            if float(tenido) != float(esperado):
                fallos.append(f"monto: se pidió {esperado} y el contrato trae {tenido}")
        except (TypeError, ValueError):
            fallos.append(f"monto: no se pudo comparar {tenido!r} con {esperado!r}")

    return fallos


def contrato_divisa(llamadas, pedido=None):
    """Arma el contrato leyendo lo que las herramientas YA devolvieron.

    `llamadas` es la lista de lo que pasó por el harness: cada elemento trae
    el nombre de la herramienta, lo que se le pidió y lo que devolvió.

    `pedido` es LO QUE SE PREGUNTÓ (C.3): un diccionario con `moneda` y, si se
    quiere, `monto`. Sin él el contrato solo puede decir si está COMPLETO;
    con él puede decir además si está CONTESTANDO LO QUE SE LE PREGUNTÓ.

    Devuelve TRES cosas:
      · `datos`    — el contrato
      · `faltan`   — qué campos NO pudo llenar  → un HUECO
      · `discrepa` — en qué NO coincide con lo pedido → una CONTRADICCIÓN

    ⚠️ `faltan` y `discrepa` son dos listas y NO se juntaron a propósito.
       Un hueco es un campo vacío; una discrepancia es un campo LLENO con el
       dato de otra pregunta. El que llama corta distinto ante cada uno: ante
       un hueco puede seguir con lo que hay; ante una discrepancia, lo que hay
       es justamente lo que no puede usar.
    """
    datos = {campo: None for campo in CAMPOS_DIVISA}

    for llamada in llamadas:
        salida = llamada["salida"]
        # Una herramienta que devolvió un error no llena nada. Y ojo: NO se
        # descarta la llamada entera, solo esa. El worker pudo llamar dos veces
        # a `tasa` —fallar la primera y acertar la segunda— y lo bueno cuenta.
        if not isinstance(salida, dict) or "error" in salida:
            continue

        # ⭐ C.3 · SE GUARDA EL PRIMERO, NO EL ÚLTIMO — y esto cambió por una
        #    corrida pagada, no por una idea.
        # 🐛 Antes cada llamada SOBRESCRIBÍA. Con un encargo de un solo paso da
        #    igual; con uno encadenado —«convierte CAD a pesos, ESE resultado a
        #    dólares, y ESE a euros»— el contrato acababa guardando el ÚLTIMO
        #    tramo: `moneda: COP, monto: 2219774`. El worker había hecho
        #    exactamente lo que se le pidió, y el contrato describía **el final
        #    del camino en vez de la pregunta**.
        # 🔑 El primer paso es el que responde a lo que se preguntó; los demás
        #    son trabajo derivado. Por eso gana el primero que llega con dato
        #    bueno. Los errores ya se saltaron arriba, así que «el primero» es
        #    **el primer acierto**: un worker que falla y reintenta sigue
        #    contando lo bueno, como antes.
        # ⚠️ Y el precio, dicho entero: esto describe bien la PRIMERA conversión
        #    y **no describe la cadena**. Un contrato de un solo renglón no puede
        #    contar una tarea de tres pasos, y fingir que sí es lo que hacía la
        #    versión de ayer. Los pasos intermedios siguen en el registro.
        def poner(campo, valor):
            """Llena el campo sólo si está vacío: el primero gana."""
            if datos[campo] is None and valor is not None:
                datos[campo] = valor

        if llamada["nombre"] == "tasa":
            poner("moneda", salida.get("de"))
            poner("tasa", salida.get("tasa"))
            poner("fuente", salida.get("fuente"))
            poner("fecha", salida.get("actualizado"))

        elif llamada["nombre"] == "convertir":
            poner("monto", salida.get("monto"))
            poner("pesos", salida.get("resultado"))
            poner("moneda", salida.get("de"))

    faltan = [campo for campo, valor in datos.items() if valor is None]
    return datos, faltan, discrepancias_divisa(datos, pedido)


# --- EL SYSTEM PROMPT DEL WORKER -------------------------------------------
# Compáralo con el de A (`agente.SISTEMA`): aquel dice "eres un asistente";
# este dice "eres un especialista, haz ESTO y devuelve ESTO".
#
# ⚠️ Las dos últimas frases no son decoración: son la mitad del CONTRATO de
#    A.3. Un worker cuya respuesta es una charla obliga al que lo llama a
#    adivinar; uno que responde en una forma fija se puede juntar con otros.
SISTEMA_DIVISA = (
    "Eres un especialista en UNA sola moneda. Tu único trabajo es averiguar a "
    "cuántos pesos colombianos equivale el monto que te pidan, y decirlo. "
    "Nunca inventes un número: si no tienes el dato, pídelo con una herramienta. "
    "Di siempre de dónde salió la cifra y de qué fecha es. "
    "Si una herramienta te devuelve un 'error', léelo y, si tiene arreglo, "
    "vuelve a intentarlo corregido; si no lo tiene, dilo claramente. "
    "No saludes, no ofrezcas ayuda extra y no hagas preguntas: nadie te va a "
    "contestar. "
    "Responde en UNA sola frase con el monto en pesos, la fuente y la fecha."
)


# ---------------------------------------------------------------------------
# 2) LO QUE SE REUTILIZA DE `agente`, Y POR QUÉ CADA COSA
# ---------------------------------------------------------------------------

def menu_para(nombres):
    """Recorta el menú de las 6 herramientas de A a las que lleve el worker.

    ⭐ SE FILTRA EL MENÚ DE A, NO SE ESCRIBE UNO NUEVO. Las `description` de
       esas herramientas son lo único que el modelo lee para decidir cuál
       usar. Si aquí se reescribieran "parecidas", el duelo del bloque F
       compararía redacciones de prompt y lo llamaría arquitectura.

    Freno de casa: si pides un nombre que no está en el menú de A, muere aquí
    y no en mitad de una corrida pagada.
    """
    del_menu = {h["name"]: h for h in agente.TOOLS}
    faltan = [n for n in nombres if n not in del_menu]
    if faltan:
        raise SystemExit(
            f"\n❌ Este worker pide herramientas que no existen en el menú de A: "
            f"{', '.join(faltan)}\n   Las que hay son: {', '.join(del_menu)}\n"
        )
    return [del_menu[n] for n in nombres]


def puente_para(nombres):
    """El puente del nombre a la función real, recortado igual que el menú.

    ⚠️ SE RECORTAN LOS DOS, Y ESTO NO ES SIMETRÍA BONITA. Si el menú llevara
       dos herramientas pero el puente siguiera teniendo las seis, un modelo
       que pidiera `trm` "de memoria" LA ENCONTRARÍA y se ejecutaría. El menú
       es lo que el modelo VE; el puente es lo que de verdad PUEDE correr.
       El que manda es el puente.
    """
    return {n: agente.FUNCIONES[n] for n in nombres}


# 🔒 B.2 — EL CANDADO DEL REGISTRO.
#    En serie sobra: solo hay UN hilo escribiendo. En paralelo hay TRES workers
#    abriendo el mismo archivo a la vez, y sin candado dos líneas se entrelazan
#    y el `.jsonl` deja de ser `.jsonl`.
#    🔑 Fíjate en el precio: en serie no cuesta NADA, porque nunca hay que
#       esperar a nadie. Por eso se pone SIEMPRE, no "cuando haga falta".
_CANDADO_REGISTRO = threading.Lock()


def anotar(evento, **datos):
    """Igual que el `anotar` de A, pero escribiendo en el registro del nivel 8."""
    # ⭐ C.1 · PASO 2 — la MISMA línea que en `orquestador.anotar`, y por eso el
    #    árbol cruza la frontera entre los dos archivos sin que ninguno de los
    #    dos sepa del otro. El worker no recibe quién lo llamó: lo mira.
    linea = {
        "hora": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "evento": evento,
        **contexto.marca(),
        **datos,
    }
    with _CANDADO_REGISTRO:
        with open(REGISTRO, "a", encoding="utf-8") as f:
            f.write(json.dumps(linea, ensure_ascii=False) + "\n")


class PresupuestoAgotado(Exception):
    """Como en A: no es un fallo, es una decisión nuestra."""


# ---------------------------------------------------------------------------
# 3) EL BUCLE DEL WORKER
# ---------------------------------------------------------------------------

# ⭐ C.1 · PASO 2 — cada worker es un TRAMO. No recibe a su padre: lo mira.
@contexto.envuelto("nombre", prefijo="worker:")
def correr_worker(encargo,
                  nombre="divisa",
                  sistema=SISTEMA_DIVISA,
                  permitidas=HERRAMIENTAS_DIVISA,
                  max_vueltas=MAX_VUELTAS_WORKER,
                  presupuesto_usd=PRESUPUESTO_WORKER_USD,
                  # C.4 — el plazo de pared. `None` lo apaga, y eso es para las
                  # pruebas: en una corrida de verdad un worker sin plazo es el
                  # residuo de 8,2 minutos que este archivo acaba de matar.
                  limite_segundos=LIMITE_WORKER_SEGUNDOS,
                  contrato=contrato_divisa,
                  # C.3 — LO QUE SE PREGUNTÓ, en Python y no en la prosa del
                  # encargo. El worker no lo usa para nada: lo pasa al contrato
                  # para que el contrato pueda desmentirse. Por defecto `None`,
                  # y eso significa NO COMPROBADO, no «todo bien».
                  pedido=None,
                  historial_previo=None,
                  verboso=True):
    """Corre UN worker de principio a fin y DEVUELVE lo que pasó.

    Recibe un encargo en texto. Devuelve un diccionario. No imprime nada
    imprescindible: lo que se imprime es para que TÚ lo veas hoy, y por eso se
    puede apagar con `verboso=False` — el orquestador de A.2 va a llamar a esto
    tres veces y no quiere tres conversaciones encimadas en pantalla.

    ⭐ FÍJATE EN LO QUE NO ESTÁ: no hay `pedir_permiso`, no hay `input()`, no
       hay `autorizadas`. Todo el sistema de permisos de A desapareció, y no
       porque este agente sea más confiado: porque LO QUE NO PUEDE HACER NO LO
       LLEVA. Un permiso que se pregunta necesita una persona; una caja de
       herramientas recortada, no.

    ⚠️ Y aquí queda dicho el precio, que es real: el usuario ya NO ve pasar las
       decisiones. En A, una llamada a la red se anunciaba en pantalla y él
       podía decir que no. Aquí no hay dónde decir que no. La única defensa que
       queda es la caja — y por eso la caja es una decisión de diseño y no un
       detalle de configuración.
    """
    menu = menu_para(permitidas)
    puente = puente_para(permitidas)

    # El gasto es de ESTA llamada al worker. No hay variable global: si la
    # hubiera, tres workers compartirían una bolsa y el aislamiento sería
    # mentira.
    gastado_usd = 0.0
    entrada_tokens = 0
    salida_tokens = 0
    llamadas_api = 0
    # C.2 · cierre — las dos cifras que el techo arreglado necesita:
    peor_llamada_usd = 0.0      # el suelo de la próxima estimación
    estimaciones_cortas = 0     # veces que la real costó MÁS que la estimada
    usadas = []          # qué herramientas pidió, en orden. Es evidencia.
    # Lo que pasó por el harness, entero. De aquí sale el contrato de A.3, y
    # por eso se guarda la SALIDA y no solo el nombre: el nombre dice que se
    # llamó, la salida dice qué trajo.
    llamadas = []

    arranque = time.monotonic()
    anotar("worker_inicio", worker=nombre, encargo=encargo, herramientas=permitidas)

    if verboso:
        print(f"\n🔧 worker[{nombre}] ← {encargo}")

    # ⭐ SU PROPIA CONVERSACIÓN, Y EMPIEZA VACÍA. Esto es A.4 en una línea: el
    #    worker no hereda ni un renglón de lo que hablaron otros. Hoy no se
    #    nota porque solo hay uno; el día que haya tres, esta lista vacía es la
    #    diferencia entre tres conversaciones cortas y una gigante que se
    #    repaga entera en cada vuelta.
    #
    # ⚠️ `historial_previo` existe SOLO para poder medir A.4: es la forma de
    #    darle a un worker la conversación de otro y ver qué hace. En el
    #    esquema de verdad nadie lo usa, y por eso el valor por defecto es
    #    `None`. Un instrumento de medida que puede quedarse encendido en
    #    producción es la sesión 50 de TEAPP otra vez.
    historial = list(historial_previo or []) + [{"role": "user", "content": encargo}]

    def hablar_con_el_modelo(mensajes):
        """La llamada a la API con sus frenos. Es la de A, con dos cambios: el
        system prompt y el menú son los del WORKER, y el presupuesto que vigila
        es el de esta llamada, no el de la corrida.
        """
        nonlocal gastado_usd, entrada_tokens, salida_tokens, llamadas_api
        nonlocal peor_llamada_usd, estimaciones_cortas

        # ⭐ C.2 · CIERRE — EL TECHO ACOTA DE VERDAD, Y LA DIFERENCIA ES UN `+`.
        #    Antes: `if gastado >= presupuesto` — autorizar sin saber el precio.
        #    Ahora: se pregunta si el dinero alcanza para la llamada CONCRETA
        #    que se está a punto de hacer.
        # 📌 El precio de este `+` está dicho arriba y hay que decirlo en voz
        #    alta: el corte se ADELANTA. Con el freno viejo el worker llegaba
        #    más lejos y se pasaba del techo; con este corta a tiempo y llega
        #    menos lejos. **No hay una tercera opción sin cambiar de esquema.**
        estimado_usd = estimar_proxima_llamada(peor_llamada_usd)
        if gastado_usd + estimado_usd > presupuesto_usd:
            raise PresupuestoAgotado(
                f"llevas ${gastado_usd:.6f} de ${presupuesto_usd:.6f} y la "
                f"siguiente llamada cuesta ~${estimado_usd:.6f}: no cabe")

        for intento in range(1, agente.REINTENTOS_PROPIOS + 1):
            try:
                # ⚠️ `tools` SE OMITE CUANDO LA CAJA ESTÁ VACÍA, y no es un
                #    capricho: un worker sin ninguna herramienta es legítimo
                #    —lo estrena la etapa REDACTORA del pipeline (B.1)— y
                #    mandar una lista vacía no es lo mismo que no mandar nada.
                #    Se añadió en la sesión 92; A.1 no cambia de conducta,
                #    porque con menú lleno el `if` no se toma.
                peticion = {
                    "model": MODELO,
                    "max_tokens": 1024,
                    "system": sistema,
                    "messages": mensajes,
                }
                if menu:
                    peticion["tools"] = menu
                respuesta = agente.cliente.messages.create(**peticion)
                este_costo = agente.costo(respuesta.usage)
                gastado_usd += este_costo
                # La comprobación de la estimación contra la realidad. Es gratis
                # —el dato ya está pagado— y es lo único que convierte el arreglo
                # de arriba en algo medido y no en algo prometido.
                if este_costo > estimado_usd:
                    estimaciones_cortas += 1
                peor_llamada_usd = max(peor_llamada_usd, este_costo)
                entrada_tokens += respuesta.usage.input_tokens
                salida_tokens += respuesta.usage.output_tokens
                llamadas_api += 1
                anotar("llamada_api", worker=nombre, intento=intento,
                       entrada=respuesta.usage.input_tokens,
                       salida=respuesta.usage.output_tokens,
                       costo_usd=round(este_costo, 6),
                       estimado_usd=round(estimado_usd, 6),
                       acumulado_usd=round(gastado_usd, 6),
                       stop_reason=respuesta.stop_reason)
                return respuesta

            except agente.REINTENTABLES as fallo:
                anotar("error_temporal", worker=nombre, intento=intento,
                       tipo=type(fallo).__name__)
                if intento == agente.REINTENTOS_PROPIOS:
                    raise
                espera = 2.0 * (2 ** (intento - 1)) + random.uniform(0, 1)
                if verboso:
                    print(f"     {type(fallo).__name__}, reintento en {espera:.1f}s")
                time.sleep(espera)

            except anthropic.APIStatusError as fallo:
                anotar("error_permanente", worker=nombre,
                       tipo=type(fallo).__name__, codigo=fallo.status_code)
                raise

    def cerrar(texto, ok, motivo, vueltas):
        """Arma el diccionario de salida. Un solo sitio, para que TODAS las
        salidas del worker tengan exactamente la misma forma — también las que
        salen mal. Un resultado de error con otra forma obliga al que llama a
        tratarlo aparte, y ahí es donde se olvida tratarlo.
        """
        # --- EL CONTRATO (A.3). Se arma con lo que pasó por el harness, no
        #     con lo que el modelo dijo. Si no hay función de contrato, el
        #     worker sigue funcionando como en A.1: solo prosa.
        datos, faltan, discrepa = (contrato(llamadas, pedido) if contrato
                                   else (None, None, None))

        resultado = {
            "worker":         nombre,
            "encargo":        encargo,
            # ⚠️ EL TEXTO YA NO ES "lo único que verá el orquestador". En A.1
            #    lo era, y por eso se perdió la fuente del CAD. Ahora viaja el
            #    contrato; el texto se conserva para que un humano lo lea y
            #    para poder comparar los dos.
            "texto":          texto,
            "datos":          datos,      # <- lo que viaja entre capas
            "faltan":         faltan,     # <- lo que el contrato NO pudo llenar
            # 🚨 C.3 — LO QUE EL CONTRATO SÍ LLENÓ, PERO CON OTRA PREGUNTA.
            #    None = no se comprobó · [] = comprobado y cuadra · lista = no cuadra.
            "discrepa":       discrepa,
            "ok":             ok,
            "motivo":         motivo,     # None | "max_vueltas" | "presupuesto"
            "vueltas":        vueltas,
            "llamadas_api":   llamadas_api,
            "herramientas":   usadas,
            "entrada_tokens": entrada_tokens,
            "salida_tokens":  salida_tokens,
            "coste_usd":      round(gastado_usd, 6),
            # C.2 · cierre — el arreglo del techo, con su propia báscula al lado.
            "peor_llamada_usd":     round(peor_llamada_usd, 6),
            "estimaciones_cortas":  estimaciones_cortas,
            "segundos":       round(time.monotonic() - arranque, 2),
        }
        anotar("worker_fin", **resultado)
        if verboso:
            estado = "✅" if ok else "⚠️"
            print(f"{estado} worker[{nombre}] → {texto}")
            print(f"   ({resultado['vueltas']} vueltas · "
                  f"{resultado['segundos']}s · ${resultado['coste_usd']:.6f} · "
                  f"herramientas: {', '.join(usadas) or 'ninguna'})")
            if datos is not None:
                print(f"   contrato: {json.dumps(datos, ensure_ascii=False)}")
                if faltan:
                    print(f"   ⚠️ sin llenar: {', '.join(faltan)}")
                if discrepa:
                    for fallo in discrepa:
                        print(f"   🚨 NO RESPONDE A LO PEDIDO → {fallo}")
                elif discrepa is None:
                    # Se dice en voz alta. Un contrato sin `pedido` no está
                    # bien: está SIN COMPROBAR, y eso hay que poder verlo.
                    print("   ⚪ contra-lo-pedido: sin comprobar (no se pasó `pedido`)")
        return resultado

    for vuelta in range(1, max_vueltas + 1):
        # ⭐ C.4 — EL PLAZO, Y SE MIRA ANTES DE HABLAR. Es el mismo sitio y la
        #    misma forma que el presupuesto: preguntar si alcanza ANTES de
        #    gastar. Aquí lo que se gasta es tiempo de quien espera.
        # ⚠️ Y su precio, dicho entero: este reloj corta ENTRE vueltas, no
        #    dentro de una. Una llamada que se cuelga sigue acotada solo por el
        #    timeout del SDK — que es de verdad, pero no es este freno. Lo que
        #    este plazo mata es la SUMA, que era lo que no tenía dueño.
        if limite_segundos is not None:
            llevado = time.monotonic() - arranque
            if llevado > limite_segundos:
                return cerrar(
                    f"(me detuve: llevaba {llevado:.1f}s de un plazo de "
                    f"{limite_segundos:.0f}s)",
                    ok=False, motivo="plazo", vueltas=vuelta)

        try:
            respuesta = hablar_con_el_modelo(historial)
        except PresupuestoAgotado as fallo:
            # ⚠️ NO SE LANZA HACIA ARRIBA. Un worker que revienta tumba al
            #    orquestador que lo llamó, y con él a los otros dos workers que
            #    no hicieron nada malo. Un worker devuelve su fracaso COMO
            #    DATO. Es el mismo criterio del "permiso negado" de A: el que
            #    llama decide qué hacer con un no.
            return cerrar(f"(me detuve: se acabó el presupuesto — {fallo})",
                          ok=False, motivo="presupuesto", vueltas=vuelta)

        # 🚨 C.4 — EL CRASH TAMBIÉN VUELVE COMO DATO, Y ESTE `except` ES EL
        #    ARREGLO ENTERO DEL PRIMER AGUJERO DE C.4.
        #    El comentario de aquí arriba llevaba dos bloques diciendo *«un
        #    worker devuelve su fracaso como dato»* — y solo era verdad para el
        #    presupuesto. Cualquier otra excepción SÍ se lanzaba hacia arriba.
        # 🔑 Y el daño no era que tumbara al orquestador (la frontera ya lo
        #    atrapaba desde B.2): era que `correr_worker` que LANZA nunca
        #    devuelve, así que **el dinero ya gastado no llegaba a la
        #    contabilidad**. Medido en `fallos.py`: $0,004000 gastados,
        #    $0,000000 en el libro. El gasto no se pierde por gastarse mal: se
        #    pierde por no volver por donde se cuenta.
        # ⭐ Y se distinguen DOS motivos, no uno. Es la diferencia entre «no
        #    insistas» y «esto se arreglaba solo reintentando»:
        except agente.REINTENTABLES as fallo:
            traceback.print_exc()
            return cerrar(f"(me caí: {type(fallo).__name__} — {fallo})",
                          ok=False, motivo="crash_temporal", vueltas=vuelta)
        except Exception as fallo:
            traceback.print_exc()
            return cerrar(f"(me caí: {type(fallo).__name__} — {fallo})",
                          ok=False, motivo="crash", vueltas=vuelta)

        # -- CASO A: terminó.
        if respuesta.stop_reason != "tool_use":
            final = next((b.text for b in respuesta.content if b.type == "text"), "")
            return cerrar(final, ok=True, motivo=None, vueltas=vuelta)

        # -- CASO B: pidió herramientas.
        historial.append({"role": "assistant", "content": respuesta.content})

        resultados = []
        for bloque in respuesta.content:
            if bloque.type != "tool_use":
                continue

            usadas.append(bloque.name)

            # Freno 7 de A, y aquí muerde MÁS: el modelo tiene seis
            # herramientas en la cabeza de su entrenamiento y solo dos en la
            # caja. Pedir una que no lleva es el error esperable, no el raro.
            funcion = puente.get(bloque.name)
            if funcion is None:
                salida = {
                    "error": f"No tienes ninguna herramienta llamada '{bloque.name}'. "
                             f"Las tuyas son: {', '.join(puente)}. "
                             f"Resuelve con esas o di que no puedes."
                }
            else:
                try:
                    salida = funcion(**bloque.input)
                except TypeError as fallo:
                    traceback.print_exc()
                    salida = {
                        "error": f"Llamaste a '{bloque.name}' con argumentos que no "
                                 f"acepta ({fallo}). Revisa los nombres y reintenta."
                    }
                except Exception:
                    traceback.print_exc()
                    salida = {
                        "error": "Esa herramienta falló por un defecto interno del "
                                 "programa. Llamarla otra vez igual no va a servir."
                    }

            if verboso:
                print(f"     -> {bloque.name}"
                      f"({json.dumps(bloque.input, ensure_ascii=False)})")
                print(f"        devolvió: {salida}")
            anotar("herramienta", worker=nombre, nombre=bloque.name,
                   entrada=bloque.input, salida=salida)

            # El harness se queda con lo que la herramienta devolvió, EXACTO.
            # Es de aquí de donde el contrato saca `fuente` y `fecha` — no de
            # la frase que el modelo escriba después.
            llamadas.append({"nombre": bloque.name,
                             "entrada": bloque.input,
                             "salida": salida})

            resultados.append({
                "type": "tool_result",
                "tool_use_id": bloque.id,
                "content": json.dumps(salida, ensure_ascii=False),
            })

        historial.append({"role": "user", "content": resultados})

    return cerrar("(se acabaron las vueltas: el worker no llegó a una respuesta)",
                  ok=False, motivo="max_vueltas", vueltas=max_vueltas)


# ---------------------------------------------------------------------------
# 4) LA DEMO — un worker, una vez, en serie. La versión más tonta que funciona.
# ---------------------------------------------------------------------------
# 📌 A propósito NO hay tres workers aquí, ni nada corriendo a la vez. Tres
#    cosas nuevas a la vez y, cuando falle, no sabes cuál falló.
#      "puede ser herramienta de otro"  -> A.2
#      "pueden ser varios"              -> final del bloque A
#      "pueden correr a la vez"         -> bloque B, y es otra historia
if __name__ == "__main__":
    print("=" * 70)
    print("A.1 — UN WORKER. Un agente de una capa, llamado como función.")
    print("=" * 70)

    resultado = correr_worker("Convierte 1000 USD a pesos colombianos.",
                              nombre="usd")

    print("\n" + "-" * 70)
    print("LO QUE DEVOLVIÓ, tal cual. Esto es un DATO, no una pantalla:")
    print("-" * 70)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    print(f"\n📄 registro: {REGISTRO.name}")
