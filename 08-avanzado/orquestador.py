"""orquestador.py — A.2 y A.3 del nivel 8.

    A.2: un agente cuyas herramientas son otros agentes.
    A.3: lo que cruza entre las dos capas es un CONTRATO, no una frase.

    LA FRASE QUE HAY QUE VER, Y DECEPCIONA A PROPÓSITO

Un orquestador **no tiene nada nuevo**. Es el mismo bucle otra vez. Lo único que
cambia es qué hay del otro lado de `FUNCIONES[nombre]`:

    en el 5b   ->  "tasa"             ->  una función que pega contra una API
    aquí       ->  "consultar_moneda" ->  una función que corre OTRO AGENTE

⭐ Y el modelo de arriba NO SE ENTERA. Para él `consultar_moneda` es una
   herramienta como `tasa`: la pide por nombre, con unos argumentos, y le llega
   un texto de vuelta. No sabe que detrás hubo un system prompt, tres vueltas y
   dos llamadas a la API. Ni le hace falta saberlo.

🔑 Esa es la definición operativa de un orquestador: **un agente que llama a una
   función que resulta ser un agente.** Todo lo demás del multi-agente
   —topologías, presupuestos repartidos, trazas anidadas— son consecuencias de
   esta línea, no cosas aparte.


    POR QUÉ EL ORQUESTADOR NO LLEVA NI UNA HERRAMIENTA DE VERDAD

Su caja tiene UNA cosa: `consultar_moneda`. No lleva `tasa`, ni `trm`, ni
`convertir`. Y no es minimalismo:

⚠️ Un orquestador que puede resolver la tarea él solo, LA VA A RESOLVER ÉL
   SOLO. Es más barato para el modelo llamar a `tasa` que delegar. Y entonces
   lo que se mediría en el bloque F sería un agente de una capa con pasos de
   más — o sea, el contendiente A disfrazado de B.
   → Si el de arriba puede hacer el trabajo de abajo, no hay dos capas: hay una
     capa con ruido.

📌 Esto adelanta a medias la pieza **C.3** (*el orquestador no toca herramientas
   reales*). Aquí se aplica por necesidad del experimento; allá se estudia como
   regla de seguridad, que es otra razón para la misma decisión.


    LO QUE ESTA PIEZA NO HACE, Y ES DELIBERADO

1. **No guarda el reporte.** La tarea del duelo termina con `guardar_reporte`, y
   aquí no está: la demo se queda en juntar las tres monedas. Guardar es una
   decisión de **quién puede escribir en el disco**, o sea la pieza **C.3**, y
   meterla hoy sería estudiar dos cosas a la vez.
   📌 Corrección del 2026-08-20: esta nota decía que el fan-in "es el contenido
      de A.3". No lo era. A.3 resultó ser **la forma de lo que cruza**, y llegó
      empujada por un defecto medido, no por el plan. Se deja escrito porque el
      plan se equivocó y el defecto no.

2. **No corre nada en paralelo.** Los workers se llaman en un `for`, uno detrás
   de otro. Que el modelo pida las tres monedas en un mismo turno **no las hace
   paralelas**: quien decide si se ejecutan a la vez es el harness, no él. Eso
   es el **bloque B**.

3. **ESTO NO ES EL DUELO.** Los números que imprime son de una demo. El duelo se
   corre y se juzga en **F.3**, con la rúbrica y el juez ciego. Un número
   bonito hoy no se anota como resultado, se anota como demo.


    CÓMO SE CORRE

    python orquestador.py            # GRATIS: dice qué haría y qué ha costado
    python orquestador.py --pagar    # la demo de verdad, con sus tres workers

💰 La segunda CUESTA DINERO, y más que `worker.py`: paga las vueltas del de
   arriba MÁS las de los tres de abajo. La factura de las dos capas se imprime
   al final, separada por capa, que es la única forma de ver dónde se fue.

🚨 La bandera se puso en la sesión 101, después de que `worker.py` cobrara sin
   que nadie quisiera pagar. Aquí no había pasado todavía, y se pone igual: **la
   lista de §6.e nombraba dos archivos de cuatro, y el que faltaba fue el que
   cobró.** Esperar a que muerda para arreglarlo es lo que ya salió mal una vez.
   → `GUIDE.md` §6.e y `LM.76`.
"""

import json
import random
import sys
import contextlib
import tempfile
import threading
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

import anthropic

sys.stdout.reconfigure(encoding="utf-8")

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "05b-proyecto"))

import agente          # noqa: E402
import contexto        # noqa: E402
import modelos         # noqa: E402
import presupuesto     # noqa: E402
import worker          # noqa: E402


# ---------------------------------------------------------------------------
# 1) CONFIGURACIÓN
# ---------------------------------------------------------------------------

# El mismo modelo arriba y abajo, y el mismo que A. Pieza 0.4 del sobre.
# ⚠️ Y aquí la tentación es mayor que en `worker.py`: "el orquestador piensa
#    más, dale un modelo mejor". Sería razonable en un producto y es veneno en
#    un experimento — lo medido dejaría de ser el esquema.
MODELO = agente.MODELO

# ⭐ C.6 — LA CONFIGURACIÓN DE ESTA CAPA, y la de la de abajo. Las dos por
#    defecto son las de siempre: `Capa()` es `agente.MODELO` sin esfuerzo.
# 🔑 Y son DOS variables y no una a propósito: toda la pieza C.6 consiste en
#    que arriba y abajo puedan ser distintas. Una sola sería el estado de hoy
#    con un nombre nuevo.
# 📊 Y ya hay número para elegir, medido en `modelos.py` sobre 374.217 tokens
#    pagados: subir ARRIBA a opus cuesta +$0,30; subir ABAJO, +$1,56. Los
#    tokens están abajo (86,4 %), y ahí es donde el modelo caro arruina.
CAPA_ORQ = modelos.Capa()
CAPA_WORKERS = modelos.Capa()

# El de arriba da pocas vueltas: pedir tres monedas y responder. Con 8 sobra.
MAX_VUELTAS_ORQ = 8

# Presupuesto de la capa de ARRIBA solamente. Cada worker trae el suyo.
# ⭐ Y esto ya es media pieza C.2: en dos capas no hay "un" presupuesto. Hay uno
#    por capa, y el de arriba NO cubre lo que gasten los de abajo. Un tope único
#    para todo se lo come el primer worker que se descarrile.
PRESUPUESTO_ORQ_USD = 0.05

REGISTRO = AQUI / f"registro_orquestador_{MODELO}.jsonl"


# --- EL SYSTEM PROMPT DEL DE ARRIBA ----------------------------------------
# Compara los tres que ya existen y verás que cada capa habla distinto:
#   A  (5b)         -> "eres un asistente de tasas de cambio"   (hace)
#   worker          -> "eres un especialista en UNA moneda"     (hace, estrecho)
#   orquestador     -> "tú no averiguas nada: repartes y juntas" (NO hace)
#
# ⚠️ La frase "no tienes forma de averiguar tasas por tu cuenta" no es humildad
#    decorativa: es la que evita que se invente un número cuando un worker
#    falle. Un modelo sin herramienta y con presión por responder, RESPONDE.
SISTEMA_ORQ = (
    "Eres un coordinador. Tú NO averiguas tasas de cambio: no tienes forma de "
    "hacerlo por tu cuenta. Para cada moneda que te pidan, llama a "
    "`consultar_moneda` UNA vez y usa lo que te devuelva. "
    "Nunca inventes ni estimes una cifra: si un especialista no te dio el dato, "
    "di que esa moneda no se pudo consultar y sigue con las demás. "
    "Al final entrega una respuesta corta con las tres monedas, conservando de "
    "cada una el monto en pesos, la fuente y la fecha tal como te las dieron. "
    "Responde en español."
)


# ---------------------------------------------------------------------------
# 2) EL MENÚ: UNA sola herramienta, y es un agente
# ---------------------------------------------------------------------------
# ⭐ MÍRALO BIEN: es un `tool` normal y corriente. Mismas tres partes que las
#    seis del 5b —name, description, input_schema—. NADA en este bloque dice
#    "esto es un agente". Desde arriba no se distingue, y esa es la gracia.
#
# ⚠️ La `description` es el contrato visto desde arriba, y es lo único que el
#    orquestador lee para decidir. Por eso dice QUÉ DEVUELVE, no solo qué hace:
#    si el de arriba no sabe qué forma tiene la respuesta, la reescribe "por si
#    acaso" — y reescribir es donde se pierden las fuentes y las fechas.
TOOLS_ORQ = [
    {
        "name": "consultar_moneda",
        "description": (
            "Consulta a un especialista a cuántos pesos colombianos equivale un "
            "monto de UNA moneda. Úsala una vez por cada moneda que necesites; "
            "las monedas son independientes entre sí. "
            "Devuelve campos exactos: moneda, monto, pesos, tasa, fuente y fecha. "
            "Copia `fuente` y `fecha` TAL CUAL vienen, sin resumirlas ni "
            "reescribirlas. Si trae `faltan`, esos campos no se pudieron "
            "averiguar: dilo, no los rellenes. Si trae `error`, esa moneda no se "
            "pudo consultar: NO inventes la cifra."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "monto": {
                    "type": "number",
                    "description": "Cuánto se quiere convertir. Ej: 1000",
                },
                "moneda": {
                    "type": "string",
                    "description": "El código de la moneda de origen. Ej: USD, EUR, CAD",
                },
            },
            "required": ["monto", "moneda"],
        },
    },
]


class PresupuestoAgotado(Exception):
    """Del orquestador. La de `worker` es otra clase, y a propósito: un worker
    que se queda sin plata no es lo mismo que la capa de arriba quedándose sin
    plata, y confundirlas haría que un fallo local pareciera uno global."""


# 🔒 B.2 — EL CANDADO DEL REGISTRO.
#    En serie sobra: solo hay UN hilo escribiendo. En paralelo hay TRES workers
#    abriendo el mismo archivo a la vez, y sin candado dos líneas se entrelazan
#    y el `.jsonl` deja de ser `.jsonl`.
#    🔑 Fíjate en el precio: en serie no cuesta NADA, porque nunca hay que
#       esperar a nadie. Por eso se pone SIEMPRE, no "cuando haga falta".
_CANDADO_REGISTRO = threading.Lock()
_CANDADO_CONTABILIDAD = threading.Lock()


def anotar(evento, **datos):
    # ⭐ C.1 · PASO 2 — `contexto.marca()` es lo único que hay que añadir para
    #    que la traza deje de ser plana. NO recibe el padre: lo mira. En todo el
    #    nivel 8 no hay una sola línea que pase un `padre=` como argumento, y
    #    eso es a propósito (ver la cabecera de `contexto.py`).
    linea = {
        "hora": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "evento": evento,
        **contexto.marca(),
        **datos,
    }
    with _CANDADO_REGISTRO:
        with open(REGISTRO, "a", encoding="utf-8") as f:
            f.write(json.dumps(linea, ensure_ascii=False) + "\n")


@contextlib.contextmanager
def registro_desviado(modulos=None):
    """Manda a un archivo temporal TODO lo que se anote aquí dentro.

    🚨 EXISTE POR UN BICHO REAL, CAZADO EN LA SESIÓN 97, CON CUATRO LÍNEAS DE
       PRUEBA YA COMMITEADAS DENTRO DEL REGISTRO DE VERDAD.
       La prueba 2 de `profundidad.py` llama a `ejecutar_un_bloque`, que llama a
       `anotar`, que escribía en `registro_orquestador_*.jsonl` — el archivo que
       guarda las corridas PAGADAS. Unas pruebas gratis ensuciando el registro
       convierten las corridas medidas en una mezcla de medidas e inventadas, y
       eso no se nota nunca: la línea de prueba se parece a las demás.

    🔑 Y LO PEOR NO ES EL BICHO: EL ARREGLO YA ESTABA ESCRITO EN EL REPO.
       `fan_out.py` (sesión 93) hacía esta misma desviación a mano, con un
       comentario citando la sesión 50 de TEAPP. `profundidad.py`, escrito DOS
       sesiones después, no lo alcanzó. Es `LM.20` otra vez: la corrección
       existía y nadie llegó a ella. Por eso ahora vive AQUÍ, en el origen, y no
       en cada archivo que se acuerde de copiarla.

    Desvía el registro de este módulo y el del worker — los dos que forman
    `REGISTROS`. Devuelve la carpeta temporal, por si la prueba quiere leerla.
    """
    global REGISTRO
    modulos = modulos if modulos is not None else [sys.modules[__name__], worker]
    carpeta = Path(tempfile.mkdtemp())
    reales = [(m, m.REGISTRO) for m in modulos]
    try:
        for m, _ in reales:
            m.REGISTRO = carpeta / f"registro_de_pruebas_{m.__name__}.jsonl"
        yield carpeta
    finally:
        # 🔒 En el `finally`, no al final del `try`. Un instrumento que se queda
        #    encendido tras un fallo es peor que uno que nunca se usó.
        for m, real in reales:
            m.REGISTRO = real


# ---------------------------------------------------------------------------
# 3) EL PUENTE — LA LÍNEA DONDE UN AGENTE SE VUELVE UNA HERRAMIENTA
# ---------------------------------------------------------------------------

# ⭐ C.2 · CIERRE — LAS CAUSAS, EN LAS PALABRAS QUE EL MODELO VA A REPETIR.
#
# Cada frase se escribe pensando en que el orquestador la va a copiar casi tal
# cual a su respuesta final. Por eso dicen QUÉ pasó y QUÉ hacer, y por eso
# ninguna culpa a un tercero: la mentira de ayer fue exactamente esa.
#
# 📌 Fíjate en que las tres terminan diciéndole si reintentar o no. Un agente al
#    que le dices «falló» sin decirle «no insistas» reintenta, y reintentar sin
#    dinero es gastar el poco que queda en fallar otra vez.
_CAUSAS = {
    "presupuesto": ("El especialista de {moneda} se quedó sin el presupuesto "
                    "que se le asignó para esta consulta y se detuvo a medias. "
                    "No es un fallo del servicio de tasas: es nuestro límite de "
                    "coste. No lo reintentes."),
    "max_vueltas": ("El especialista de {moneda} agotó su número máximo de "
                    "vueltas sin llegar a una respuesta. No lo reintentes."),
    # 🚨 C.4 — LAS DOS CARAS DEL CRASH, Y SON DOS FRASES PORQUE SON DOS
    #    CONSEJOS CONTRARIOS. Hasta hoy las dos caían en el `except Exception`
    #    de `ejecutar_un_bloque` y al modelo le llegaba **la misma frase**:
    #    *«falló por un defecto interno del programa. No lo llames otra vez
    #    igual»*. Medido en `fallos.py`: idénticas, carácter por carácter.
    # 🔑 Y para el reintentable esa frase no es imprecisa, es **dañina**: le
    #    prohíbe justo lo único que lo arreglaba. Es `LM.71` con otra ropa —
    #    el mensaje que llega primero entierra la causa real.
    # ✅ CERRADO EN LA SESIÓN 102 — y así estaba escrito el problema:
    #    ⚠️ ESTA FRASE INVITABA A UN REINTENTO QUE LA CAPA DE AL LADO
    #       RECHAZABA, y el hueco lo abrió el arreglo de la sesión 101.
    #    Si el modelo acepta la invitación y vuelve a pedir esa moneda,
    #    `reparto.tomar()` ya no tiene trozo —el encargo se repartió para tres—
    #    y le contesta: *«es uno de más. No lo reintentes.»* Comprobado a $0,00
    #    con el instrumento de C.4: la 4ª llamada devuelve `sin_trozo: true`.
    # 🔑 Son DOS INSTRUCCIONES CONTRARIAS DEL MISMO HARNESS en dos turnos
    #    seguidos, y la segunda además dice algo falso: no es que el worker
    #    sobre, es que se le acabó el sitio. Es `LM.71` por TERCERA vez en tres
    #    sesiones —un arreglo reabre el que tiene al lado— y ninguna prueba lo
    #    vio porque **cada una vigila su mitad**: la de la causa comprueba el
    #    mensaje, la del reparto comprueba el cuarto worker, y nadie miraba la
    #    frase que va entre las dos.
    # 📌 Y no se ha visto nunca con dinero delante: `crash_temporal` necesita
    #    una caída real de la API. Es un modo de fallo que sólo asoma el día peor.
    # ✅ SE ELIGIÓ (a) + (b), Y LAS DOS HICIERON FALTA — decisión de la 102.
    #    Se descartaron los dos bolsillos «gratis», y los descartó un DATO:
    #      · prestar de la bolsa de arriba: su holgura real era 0,47 trozos.
    #        No llega, y dejaría al que responde de la factura a $0,000001.
    #      · media ración: sólo 12 de 57 workers pagados caben en $0,004948.
    #        El reintento moriría de presupuesto el 79 % de las veces, y morir
    #        de presupuesto produce «No lo reintentes» — o sea, fabricaríamos
    #        la TERCERA orden contraria seguida para tapar la segunda.
    #      · un trozo entero cubre a 53 de 57 (93 %). Es la única ración que
    #        de verdad reintenta.
    # 🔑 Conclusión: reservar CUESTA y no hay bolsillo gratis. La reserva no se
    #    descuenta de nadie — se AUTORIZA y hace crecer el total del encargo,
    #    con su línea en el informe (`reintentos_reservados`/`_usados`).
    # ⭐ Y (a) SOLA NO BASTABA: la reserva es finita, así que al segundo
    #    reintento volvía la contradicción intacta. Por eso la frase de abajo
    #    se eligió mirando `quedan_reintentos()`. Reservar movió el problema un
    #    turno; condicionar la invitación es lo que lo cerró.
    "crash_temporal": ("El especialista de {moneda} se cayó por un problema "
                       "PASAJERO de conexión con el servicio, y ya reintentó "
                       "por su cuenta sin suerte. Queda presupuesto reservado "
                       "para un reintento: esta es de las que sí puede salir "
                       "bien al segundo intento."),
    # ⭐ SESIÓN 102 · LA MISMA CAUSA, SIN INVITACIÓN — Y ES LA SALIDA (b)
    #    MONTADA ENCIMA DE LA (a). El fallo es idéntico y el consejo es el
    #    contrario, porque lo que cambió no es el fallo: es si queda con qué.
    # 🔑 Fíjate en que NO se le miente al modelo diciéndole que es permanente.
    #    Se le dice la verdad entera: fue pasajero Y no hay con qué volver. Un
    #    harness que oculta el motivo real para simplificar el consejo es
    #    exactamente `LM.71`, y ya nos costó tres sesiones seguidas.
    "crash_temporal_sin_reserva": (
        "El especialista de {moneda} se cayó por un problema PASAJERO de "
        "conexión con el servicio, y ya reintentó por su cuenta sin suerte. "
        "No queda presupuesto reservado para otro intento, así que no lo "
        "reintentes: di que esa moneda no se pudo consultar."),
    "crash": ("El especialista de {moneda} se cayó por un defecto interno de "
              "nuestro programa, no del servicio de tasas. Volver a llamarlo "
              "igual daría el mismo fallo. No lo reintentes."),
    # C.4 — el plazo. Se parece al presupuesto y no es el mismo: allí se acabó
    # el dinero, aquí el tiempo de quien espera.
    "plazo": ("El especialista de {moneda} tardó más del plazo que se le dio y "
              "se le cortó a medias. No es un fallo del servicio: es nuestro "
              "límite de tiempo. No lo reintentes."),
    None: ("El especialista de {moneda} terminó sin el dato de la conversión. "
           "No lo reintentes."),
    # 🚨 C.3 — la causa MÁS RARA de todas, y la que más falta hacía: el
    #    especialista no falló, TERMINÓ BIEN. Solo que contestó otra pregunta.
    #    Por eso la frase no dice «falló»: dice qué trajo y qué se había pedido.
    "discrepancia": ("El especialista de {moneda} devolvió un resultado "
                     "completo pero que NO corresponde a lo que se le pidió, "
                     "así que se descartó. No inventes el dato de {moneda} ni "
                     "uses el de otra moneda en su lugar: di que esa moneda no "
                     "se pudo consultar. No lo reintentes."),
}


def herramienta_consultar_moneda(monto, moneda, contabilidad, verboso=True):
    """Esta función ES el orquestador entero, conceptualmente.

    Recibe argumentos como cualquier herramienta. Corre un worker. Devuelve un
    diccionario. Entre la primera y la última línea hay un agente completo, y
    el que la llamó no se entera.

    ⭐ AQUÍ SE DECIDE QUÉ CRUZA LA FRONTERA, Y ES LA PIEZA A.3 ENTERA.

       El worker devuelve CATORCE campos. Al modelo de arriba le suben SEIS: el
       contrato. El resto —coste, vueltas, tokens, segundos, herramientas— se
       queda en `contabilidad`, que es NUESTRA, no del modelo.

    🐛 EN A.2 ESTA FUNCIÓN DEVOLVÍA `{"respuesta": <la frase del worker>}`, Y ESO
       PERDIÓ UN DATO MEDIDO: la fuente del CAD (`open.er-api.com`) existía en
       el `tool_result` y el worker no la puso en su frase. Arriba llegó
       "tasa de mercado", a secas, y ya no había de dónde sacarla.
       → Ahora cruza el contrato, que sale del harness y no de la redacción.

    ⚠️ Y LA PROSA DEL WORKER YA NO SUBE. Se decidió a propósito, y cuesta algo:
       si el worker hubiera notado una rareza —"esta tasa parece vieja"—, esa
       advertencia NO llega arriba, porque no hay campo donde quepa.
       🔑 UN CONTRATO NO ES UNA FORMA DE NO PERDER NADA: ES ELEGIR QUÉ PERDER.
          La prosa perdía cosas al azar y sin avisar; el contrato pierde lo que
          decidimos, y `faltan` dice cuándo.

    📌 El reparto de la contabilidad es el correcto y no el cómodo: al modelo no
       le sirve para decidir y le costaría tokens en cada vuelta. A nosotros nos
       hace falta entero: sin él no hay factura por capa, y sin factura por capa
       el bloque F no tiene qué comparar.
    """
    # El encargo se arma en Python, no lo escribe el modelo de arriba. Es
    # deliberado: así el worker recibe siempre la misma forma de petición y las
    # tres monedas son comparables entre sí.
    encargo = f"Convierte {monto} {moneda} a pesos colombianos."

    # ⭐ C.2 · CIERRE — EL ENCARGO DESIGUAL, Y ES LA OBLIGACIÓN QUE LLEVABA DOS
    #    SESIONES SIN PAGARSE.
    #    Hasta hoy los tres workers recibían EXACTAMENTE la misma frase con otra
    #    moneda, y por eso costaban lo mismo hasta la tercera cifra (dispersión
    #    medida: 1,00x-1,02x en cinco corridas). Con encargos gemelos, el reparto
    #    a tercios y el tope por pieza dan el mismo resultado: **la tarea no podía
    #    distinguir los dos esquemas.** No es una tarea fácil, es un instrumento
    #    ciego para esta pregunta.
    # 🔑 Si no hay `encargos`, no cambia nada: A.2 y todo el bloque B siguen con
    #    la frase de siempre. La desigualdad es un instrumento que se enchufa,
    #    no una conducta nueva del orquestador.
    encargos = contabilidad.get("encargos")
    if encargos and moneda.upper() in encargos:
        encargo = encargos[moneda.upper()].format(monto=monto, moneda=moneda.upper())

    # ⭐ C.2 — AQUÍ SE ENTREGA EL TROZO, Y ES EL SITIO EXACTO DONDE EL DINERO
    #    CRUZA LA FRONTERA. Si no hay reparto —A.2 y todo el bloque B— el worker
    #    usa su tope de siempre y nada cambia de conducta.
    #    🔑 Fíjate en que el trozo se pide JUSTO ANTES de arrancar al worker y no
    #       al principio de la corrida: es el único momento en que ya se sabe
    #       CUÁNTOS especialistas pidió el modelo. El reparto se calculó a la
    #       entrada; la entrega ocurre cuando aparece cada uno.
    reparto = contabilidad.get("reparto")
    presupuesto_worker = worker.PRESUPUESTO_WORKER_USD
    if reparto is not None:
        try:
            presupuesto_worker = reparto.tomar(moneda.lower())
        except presupuesto.SinTrozo as fallo:
            # ⚠️ El modo de fallo que el tope-por-pieza NO tenía: no es que se
            #    acabara el dinero, es que este worker no estaba en el reparto.
            #    Se le dice al modelo con todas las letras, porque es él quien
            #    pidió uno de más y es el único que puede no volver a pedirlo.
            anotar("sin_trozo", capa=contabilidad.get("capa", "orquestador"),
                   worker=moneda.lower(), detalle=str(fallo))
            return {
                "error": f"No hay presupuesto para '{moneda}': el encargo se "
                         f"repartió para {reparto.n_workers} especialistas y "
                         f"este es uno de más. No lo reintentes.",
                "sin_trozo": True,
            }

    # ⭐ C.3 — LO QUE SE PREGUNTÓ VIAJA HACIA ABAJO EN PYTHON, al lado del
    #    encargo en prosa. No es repetir el encargo: el encargo es la frase que
    #    lee el modelo, y `pedido` es el dato contra el que se comprueba la
    #    respuesta. Si el modelo se despista y consulta otra moneda, el encargo
    #    no puede delatarlo —él mismo es la frase que se ignoró—; `pedido`, sí.
    resultado = worker.correr_worker(encargo, nombre=moneda.lower(),
                                     presupuesto_usd=presupuesto_worker,
                                     pedido={"moneda": moneda.upper(),
                                             "monto": monto},
                                     # ⭐ C.6 — y aquí baja. `None` si nadie la
                                     #    puso, y entonces el worker usa la
                                     #    suya de siempre.
                                     capa=contabilidad.get("capa_workers"),
                                     verboso=verboso)

    # --- La contabilidad de la capa de abajo. Se suma aquí y no dentro del
    #     worker, porque el worker no sabe —ni tiene por qué— que alguien lo
    #     está orquestando.
    # 🔒 B.2 — EL CANDADO DE LA CONTABILIDAD.
    #    `contabilidad[k] += x` NO es una operación: son TRES (leer, sumar,
    #    escribir). Con tres hilos, dos pueden leer el mismo valor viejo y
    #    una de las dos sumas se pierde. No da error: da un número menor.
    #    🔑 Y ese es el peor defecto posible aquí, porque lo que se pierde es
    #       LA FACTURA — el dato por el que existe todo el bloque F.
    with _CANDADO_CONTABILIDAD:
        contabilidad["workers"] += 1
        contabilidad["coste_workers_usd"] += resultado["coste_usd"]
        contabilidad["llamadas_api_workers"] += resultado["llamadas_api"]
        contabilidad["entrada_workers"] += resultado["entrada_tokens"]
        contabilidad["salida_workers"] += resultado["salida_tokens"]
        contabilidad["detalle"].append({
            "worker": resultado["worker"],
            "ok": resultado["ok"],
            "vueltas": resultado["vueltas"],
            "segundos": resultado["segundos"],
            "coste_usd": resultado["coste_usd"],
            "herramientas": resultado["herramientas"],
            # 🐛 C.2 — ESTOS DOS FALTABAN, Y SE NOTÓ AL ESCRIBIR LAS
            #    COMPROBACIONES DE LA CORRIDA PAGADA, NO ANTES.
            #    El worker sabía por qué se paró —`motivo`: presupuesto,
            #    max_vueltas o `None`— y **ese dato moría en la frontera**.
            #    Arriba llegaba `ok=False` a secas, que dice que salió mal y no
            #    dice de qué. 🔑 Un `ok` sin causa obliga a mirar el registro a
            #    mano, que es exactamente lo que C.1 acaba de quitar de en medio.
            "motivo": resultado["motivo"],
            "llamadas_api": resultado["llamadas_api"],
            # C.2 · cierre — la báscula del techo arreglado también tiene que
            # cruzar: si se queda arriba, el informe no puede decir si el techo
            # se respetó. Es `motivo` otra vez, un día después.
            "estimaciones_cortas": resultado.get("estimaciones_cortas", 0),
        })

    # --- LO QUE CRUZA. Seis campos y, si hace falta, la lista de lo que no se
    #     pudo llenar.
    #
    # ⚠️ SE DEVUELVE UN VALOR TAMBIÉN CUANDO EL WORKER FALLÓ, no una excepción.
    #    Un worker caído no debe tumbar al orquestador ni a las otras dos
    #    monedas (eso es C.4). El de arriba lee el fallo y decide.
    #
    # ⭐ Y el fallo viaja EN LA MISMA FORMA que el éxito —un diccionario, no una
    #    excepción— por la razón de siempre: un resultado de error con otra
    #    forma obliga al que llama a tratarlo aparte, y ahí es donde se olvida.
    datos = resultado["datos"] or {}
    faltan = resultado["faltan"] or []
    # 🐛 C.3 · ARREGLO DE LA CORRIDA PAGADA — **UNA CONSECUENCIA NO PUEDE IR
    #    DELANTE DE SU CAUSA.** Esta línea es el arreglo entero y hay que leerla
    #    con lo que pasó al pagar:
    #    El worker `cad` se quedó sin presupuesto a mitad de una cadena de tres
    #    conversiones. Su contrato quedó a medias y **por eso** discrepaba. El
    #    corte de abajo iba primero, así que arriba subió `motivo="discrepancia"`
    #    y el modelo lo repitió tal cual: *«no se pudo consultar por discrepancia
    #    en los datos del especialista»*. **Falso: se quedó sin dinero.**
    # 🔑 La discrepancia sólo significa algo en un worker que TERMINÓ. En uno que
    #    se paró a medias no es la causa: es el rastro de haberse parado. Poner
    #    el detector nuevo delante enterró la causa verdadera — y era exactamente
    #    el agujero que la sesión 99 acababa de tapar, reabierto por el arreglo
    #    de la mañana siguiente. **Un arreglo puede reabrir el que está al lado.**
    discrepa = (resultado.get("discrepa") or []) if resultado.get("ok") else []

    # 🚨 C.3 — EL CORTE DE LA DISCREPANCIA, Y VA **ANTES** Y **APARTE**.
    #    Aquí está lo que la corrida pagada de la 99 enseñó y costó una mentira:
    #    el corte de abajo pregunta `datos.get("pesos") is None`, y con la
    #    respuesta equivocada **`pesos` ESTÁ LLENO** — con el número de otra
    #    moneda. Un contrato que contesta otra pregunta pasa entero por ese
    #    filtro, porque el filtro busca HUECOS y aquí no hay ninguno.
    # 🔑 Por eso `discrepa` no podía meterse dentro de `faltan`: no es que
    #    faltara un dato, es que sobra el que hay. **Un hueco y una
    #    contradicción se ven distinto y se cortan distinto.**
    if discrepa:
        anotar("contrato_discrepa", moneda=moneda.upper(),
               pedido={"moneda": moneda.upper(), "monto": monto},
               discrepa=discrepa, recibido=datos)
        if verboso:
            print(f"   🚨 se DESCARTA la respuesta de {moneda.upper()}: "
                  f"{'; '.join(discrepa)}")
        return {"error": f"No se pudo consultar {moneda}.",
                "motivo": "discrepancia",
                "causa": _CAUSAS["discrepancia"].format(moneda=moneda),
                "detalle": "; ".join(discrepa),
                # ⭐ EL DATO EQUIVOCADO SE CONSERVA, y fue una decisión, no un
                #    descuido: **tirarlo es tirar la evidencia**, y el hallazgo
                #    de la 99 salió justamente de poder leer qué había subido.
                #    Viaja bajo un nombre que nadie puede confundir con un
                #    resultado bueno: `descartado`, no `datos`.
                "descartado": datos,
                "faltan": faltan}

    # `pesos` es el campo sin el cual la consulta no sirvió de nada. Que no esté
    # NO es "un campo vacío más": es que esta moneda no se resolvió.
    #
    # 🔲 C.4 — PENDIENTE CON DUEÑO, ANOTADO Y **NO ARREGLADO A PROPÓSITO**
    #    (decisión del estudiante, sesión 101). Míralo antes de tocarlo:
    #
    #    🚨 EN LA CORRIDA PAGADA DE HOY TENÍAMOS LA RESPUESTA DEL CAD Y LA
    #       TIRAMOS. El worker cortó por presupuesto a media cadena, pero su
    #       contrato salió **completo y correcto**: `pesos: 2.219.774`,
    #       `faltan: []`, `discrepa: []`. La pregunta del usuario era «1.000 CAD,
    #       ¿cuánto es en pesos?» — **eso lo teníamos**. Lo que faltaba eran los
    #       eslabones siguientes, que son del encargo artificial que lo hacía caro.
    #
    # 🔑 FÍJATE EN QUE ES UN `or`: basta con que el worker no TERMINARA para
    #    tirar un contrato lleno. `ok` es una pregunta sobre el PROCESO;
    #    `pesos` es una pregunta sobre el RESULTADO. Aquí se tratan como una
    #    sola y se gana la más pesimista de las dos.
    #
    # ⚠️ Y NO ES UN BUG OBVIO, ES UNA DECISIÓN DE DISEÑO SIN TOMAR: entregar un
    #    resultado parcial puede ser PEOR que no entregar nada si el de arriba
    #    no sabe que es parcial. Arreglarlo sin resolver eso cambia una pérdida
    #    silenciosa por una mentira silenciosa. → README del nivel, «lo que C.4
    #    deja abierto».
    if not resultado["ok"] or datos.get("pesos") is None:
        # 🚨 C.2 · CIERRE — LA CAUSA CRUZA LA FRONTERA, Y ES UN ARREGLO QUE
        #    COSTÓ UNA MENTIRA VERLO.
        #    Hasta ayer aquí subía `{"error": "No se pudo consultar USD."}` y
        #    nada más. El modelo de arriba, sin causa, se la inventó: dijo que
        #    las monedas fallaron «debido a limitaciones en el servicio».
        #    El servicio estaba perfecto — el que se quedó sin dinero fui yo.
        # 🔑 No mintió sobre el QUÉ: mintió sobre el POR QUÉ, y lo hizo porque
        #    nadie se lo dijo. **A un agente al que no le das la causa se la
        #    inventa, y suena razonable.** Es el mismo agujero que `motivo`
        #    acababa de tapar entre el worker y la contabilidad, UNA FRONTERA
        #    MÁS ARRIBA. Un arreglo no se propaga solo a la siguiente costura.
        # ⚠️ Y sube en DOS formas a propósito, porque tienen dos lectores:
        #    · `motivo` — la etiqueta corta, para nosotros y para las pruebas.
        #    · `causa`  — la frase en español, para el MODELO, que no lee
        #      diccionarios de estados: lee prosa y la repite.
        # ⭐ SESIÓN 102 — LA CAUSA SE ELIGE MIRANDO SI QUEDA CON QUÉ.
        #    Hasta hoy `motivo` entraba directo al diccionario y salía una
        #    frase fija. `crash_temporal` invitaba SIEMPRE a reintentar, y el
        #    reparto rechazaba ese reintento al turno siguiente: dos órdenes
        #    contrarias del mismo harness en dos turnos seguidos.
        # 🔑 Sin reparto —A.2 y todo el bloque B— no hay nada que rechazar, así
        #    que la invitación es honesta y se mantiene. La condición no es
        #    «¿hay reserva?» sino «¿puede alguien rechazarme luego?».
        clave_causa = resultado["motivo"]
        if clave_causa == "crash_temporal":
            hay_con_que = reparto is None or reparto.quedan_reintentos() > 0
            if not hay_con_que:
                clave_causa = "crash_temporal_sin_reserva"

        return {"error": f"No se pudo consultar {moneda}.",
                "motivo": resultado["motivo"],
                "causa": _CAUSAS.get(clave_causa,
                                     _CAUSAS[None]).format(moneda=moneda),
                "detalle": resultado["texto"],
                "faltan": faltan}

    cruza = {campo: datos[campo] for campo in worker.CAMPOS_DIVISA}
    if faltan:
        cruza["faltan"] = faltan
    return cruza


FUNCIONES_ORQ = {
    "consultar_moneda": herramienta_consultar_moneda,
}


# ---------------------------------------------------------------------------
# 3.b) EL REPARTO — la pieza que el bloque B convierte en variable
# ---------------------------------------------------------------------------
# Hasta A.3 esto era un `for` metido dentro del bucle, y por eso no se veía.
# Sacarlo aquí no cambia nada de lo que hace: cambia QUIÉN LO DECIDE.
#
# ⭐ LA FRASE DE B.2:
#    «Pidió tres a la vez» y «corrieron tres a la vez» son cosas distintas.
#    El modelo solo puede PEDIR. Quien decide si algo corre en paralelo es el
#    harness — o sea, estas veinte líneas.

# ⭐ C.1 · PASO 2 — cada LLAMADA A HERRAMIENTA es un tramo. Sin esto el árbol
#    saltaría de la capa al worker y se perdería el escalón de en medio: qué
#    herramienta pidió el modelo. Es el escalón donde vive el enrutado, o sea
#    justo lo que la sesión 95 tuvo que deducir a mano.
@contexto.envuelto("bloque", prefijo="tool:", atributo="name")
def ejecutar_un_bloque(bloque, contabilidad, verboso=True, funciones=None):
    """Ejecuta UN `tool_use` y devuelve su `tool_result`.

    ⭐ Y LO IMPORTANTE ES LO QUE NO SABE: no sabe si es el primero de tres en
       fila o uno de tres a la vez. Esa ignorancia es lo que permite que el
       reparto sea intercambiable — si esta función supiera de hilos, cambiar
       la topología obligaría a reescribirla.

    ⭐ B.5 — `funciones` entra por la puerta, igual que `reparto` en B.2, y por
       la misma razón: la capa de en medio de B.5 es OTRO orquestador con OTRO
       puente. Si el puente siguiera siendo el global, la única forma de tener
       dos menús sería copiar este archivo.
       📌 Por defecto es `FUNCIONES_ORQ`, así que A.2 no cambia de conducta.
    """
    funciones = funciones if funciones is not None else FUNCIONES_ORQ
    funcion = funciones.get(bloque.name)
    if funcion is None:
        salida = {
            "error": f"No existe la herramienta '{bloque.name}'. "
                     f"Las tuyas son: {', '.join(funciones)}."
        }
    else:
        try:
            salida = funcion(**bloque.input,
                             contabilidad=contabilidad, verboso=verboso)
        except TypeError as fallo:
            traceback.print_exc()
            salida = {
                "error": f"Llamaste a '{bloque.name}' con argumentos que no "
                         f"acepta ({fallo}). Revisa los nombres y reintenta."
            }
        except Exception:
            # Un defecto NUESTRO en la capa de abajo. Al modelo se le dice
            # honestamente que no es culpa suya; a nosotros, el traceback. Y el
            # orquestador sigue vivo: las otras monedas no tienen por qué morir
            # con esta.
            #
            # ⚠️ B.2 SUBE LA APUESTA DE ESTE `except`. En serie, un worker que
            #    revienta ya no tumbaba a los otros dos. En paralelo, si la
            #    excepción escapara del hilo, el `Future` la guardaría y saltaría
            #    al recogerla — matando la tanda entera. Que se atrape AQUÍ, en
            #    el sitio que no sabe de hilos, es lo que hace que dé igual.
            traceback.print_exc()
            salida = {
                "error": "El especialista falló por un defecto interno del "
                         "programa. No lo llames otra vez igual."
            }

    anotar("herramienta", capa=contabilidad.get("capa", "orquestador"),
           nombre=bloque.name, entrada=bloque.input, salida=salida)

    return {
        "type": "tool_result",
        "tool_use_id": bloque.id,
        "content": json.dumps(salida, ensure_ascii=False),
    }


def reparto_en_serie(bloques, contabilidad, verboso=True, funciones=None):
    """El reparto de toda la vida: uno detrás de otro.

    Es el `for` de A.2 sin una coma de diferencia, y sigue siendo el valor por
    defecto para que los números de A.2 sigan valiendo.

    ⏱️ Su tiempo es la SUMA de los tres. No es un defecto que se pueda
       optimizar dentro de esta función: es lo que significa "en serie".
    """
    return [ejecutar_un_bloque(b, contabilidad, verboso, funciones)
            for b in bloques]



# ---------------------------------------------------------------------------
# 4) EL BUCLE DE ARRIBA — es el mismo bucle. Otra vez.
# ---------------------------------------------------------------------------

# ⭐ C.1 · PASO 2 — cada capa es un TRAMO. La de más arriba funda la corrida;
#    las de en medio (B.5) heredan la suya y se cuelgan de quien las llamó.
@contexto.envuelto("nombre", prefijo="capa:")
def correr_orquestador(tarea, max_vueltas=MAX_VUELTAS_ORQ,
                       presupuesto_usd=PRESUPUESTO_ORQ_USD, verboso=True,
                       reparto=None, sistema=None, tools=None, funciones=None,
                       nombre="orquestador", presupuesto_encargo=None,
                       encargos=None, reintentos_reservados=0,
                       # ⭐ C.6 — las dos capas, por la puerta. `None` en las
                       #    dos = lo de siempre, y por eso A.2 y todo el bloque
                       #    B conservan sus números.
                       capa=None, capa_workers=None):
    """Corre la capa de arriba y devuelve un diccionario con LAS DOS capas.

    Si comparas este bucle con el de `worker.correr_worker`, verás que son el
    mismo: mandar, mirar `stop_reason`, ejecutar lo pedido, devolver
    `tool_result`, repetir. Cambian el system prompt, el menú y qué hay detrás
    del puente. **Nada más.**

    ⭐ B.2 — `reparto` es la topología, y por eso es un parámetro y no un `if`.
       Si fuera `if paralelo:` dentro del bucle, cada topología nueva del
       bloque B (router, supervisor) añadiría una rama aquí dentro. Entrando
       por la puerta, el bucle no crece nunca.
    """
    # Por defecto, en serie: A.2 no cambia de comportamiento por este refactor.
    reparto = reparto or reparto_en_serie
    capa = capa or CAPA_ORQ
    capa_workers = capa_workers or CAPA_WORKERS

    # ⭐ B.5 — LAS TRES PIEZAS QUE HACÍAN DE ESTE BUCLE «EL» ORQUESTADOR Y AHORA
    #    LO HACEN «UN» ORQUESTADOR: con qué habla, qué menú ve y qué hay detrás.
    #    Con esto, la capa de en medio de B.5 no es un archivo nuevo: es esta
    #    misma función llamada con otros tres argumentos.
    #    📌 Los tres por defecto son los de A.2. Si algún día uno de estos
    #       `or` se pone en verde por accidente, A.2 se entera por sus números.
    sistema = sistema or SISTEMA_ORQ
    tools = tools if tools is not None else TOOLS_ORQ

    # ⭐ C.2 — EL PRESUPUESTO DEL ENCARGO. Entra por la puerta como `reparto` y
    #    `funciones`, y por el mismo motivo: si fuera un `if` aquí dentro, el
    #    esquema viejo y el nuevo convivirían como dos ramas.
    #    📌 Por defecto es `None`, así que A.2 y todo el bloque B siguen con su
    #       tope por pieza y sus números siguen valiendo.
    # 🔑 Y esta es la línea que resume C.2: cuando hay presupuesto de encargo, el
    #    orquestador DEJA DE TENER TOPE PROPIO y pasa a tener una RESERVA — un
    #    trozo del mismo dinero que reparte, no una bolsa aparte.
    reparto_presupuesto = None
    if presupuesto_encargo is not None:
        reparto_presupuesto = (
            presupuesto_encargo
            if isinstance(presupuesto_encargo, presupuesto.RepartoDeEntrada)
            else presupuesto.RepartoDeEntrada(
                total_usd=presupuesto_encargo,
                # ⭐ SESIÓN 102 — por defecto CERO, y es a propósito. Encender
                #    la reserva sola cambiaría el total del encargo y con él
                #    todas las facturas ya medidas de C.2 y C.3. Una reserva
                #    que se enciende sin que nadie la pida no es un freno: es
                #    un gasto que aparece.
                reintentos=reintentos_reservados))
        presupuesto_usd = reparto_presupuesto.arriba_usd

    gastado_usd = 0.0
    entrada_tokens = 0
    salida_tokens = 0
    llamadas_api = 0
    # C.2 · cierre — las dos cifras del techo arreglado, iguales que en el worker.
    peor_llamada_usd = 0.0      # suelo de la próxima estimación
    estimaciones_cortas = 0     # veces que la real costó MÁS que la estimada

    contabilidad = {
        "capa": nombre,
        "workers": 0,
        "coste_workers_usd": 0.0,
        "llamadas_api_workers": 0,
        "entrada_workers": 0,
        "salida_workers": 0,
        "detalle": [],
        # C.2 — viaja en la contabilidad porque es NUESTRA y ya llega a la
        # herramienta. Al modelo no le sube: no es asunto suyo cuánto le queda a
        # nadie, y decírselo sólo le daría con qué negociar.
        "reparto": reparto_presupuesto,
        # C.2 · cierre — el encargo POR WORKER, para poder hacerlos desiguales.
        # Vacío por defecto: sin esto, los tres reciben la misma frase y la
        # corrida no puede distinguir un reparto de otro.
        "encargos": encargos,
        # ⭐ C.6 — LA CONFIGURACIÓN DE LA CAPA DE ABAJO VIAJA AQUÍ, y no en la
        #    firma de `herramienta_consultar_moneda`. Es el mismo camino que ya
        #    usan `reparto` y `encargos`, y por el mismo motivo: la herramienta
        #    tiene la forma de una herramienta cualquiera, y lo que el harness
        #    necesita pasarle por debajo va en la contabilidad, que es NUESTRA.
        # 🔑 Al modelo no le sube, y eso es A.3: saber con qué modelo corre su
        #    especialista no le sirve para decidir nada y le costaría tokens en
        #    cada vuelta.
        "capa_workers": capa_workers,
    }

    arranque = time.monotonic()
    anotar("orquestador_inicio", capa=nombre, tarea=tarea,
           modelo=capa.modelo, esfuerzo=capa.esfuerzo,
           modelo_workers=capa_workers.modelo)

    if verboso:
        print(f"\n🧠 orquestador ← {tarea}")

    historial = [{"role": "user", "content": tarea}]

    def hablar_con_el_modelo(mensajes):
        nonlocal gastado_usd, entrada_tokens, salida_tokens, llamadas_api
        nonlocal peor_llamada_usd, estimaciones_cortas

        # ⭐ C.2 · CIERRE — EL MISMO ARREGLO QUE EL WORKER, Y AQUÍ HACE MÁS FALTA.
        #    Ayer se pasaron del techo LOS CUATRO participantes, y arreglar sólo
        #    al worker habría dejado la mitad del defecto en pie: el orquestador
        #    tenía el `>=` ciego idéntico, tres capas más arriba.
        # 🐛 AQUÍ SE ESCRIBIÓ UNA AFIRMACIÓN FALSA Y SE CAZÓ EL MISMO DÍA, POR
        #    IR A CONTARLA. Decía: «las llamadas del orquestador son LAS CARAS,
        #    porque lleva la tarea entera más los contratos de los tres
        #    especialistas». Suena mecánico y es mentira. Los registros pagados:
        #
        #        orquestador   32 llamadas · mediana $0,001844 · max $0,003145
        #        worker       115 llamadas · mediana $0,002438 · max $0,005480
        #
        # ⭐ El orquestador es el MÁS BARATO de los dos, y no por casualidad: es
        #    A.3 cobrando. Lo que le sube de los workers son SEIS CAMPOS, no la
        #    conversación de cada uno. El worker, en cambio, se traga su propio
        #    historial completo vuelta tras vuelta.
        # 🔑 El contrato no sólo evitó perder la fuente del CAD: **abarató la capa
        #    de arriba**, y eso no estaba escrito en ningún sitio hasta hoy.
        # 📌 La lección de método es la de siempre: nombrar un mecanismo
        #    plausible no es haberlo medido. Costó una consulta de $0,00.
        # 🔑 La función de estimar vive en `worker.py` y se usa desde los dos
        #    sitios. Copiarla aquí habría sido el bicho de siempre: dos copias del
        #    precio de una llamada, y una de las dos se queda vieja.
        estimado_usd = worker.estimar_proxima_llamada(peor_llamada_usd)
        if gastado_usd + estimado_usd > presupuesto_usd:
            raise PresupuestoAgotado(
                f"llevas ${gastado_usd:.6f} de ${presupuesto_usd:.6f} y la "
                f"siguiente llamada cuesta ~${estimado_usd:.6f}: no cabe")

        for intento in range(1, agente.REINTENTOS_PROPIOS + 1):
            try:
                peticion_orq = {
                    # ⭐ C.6 — el modelo de ARRIBA sale de su capa.
                    "model": capa.modelo,
                    "max_tokens": 2048,
                    "system": sistema,
                    "tools": tools,
                    "messages": mensajes,
                }
                peticion_orq.update(capa.extras_de_peticion())
                respuesta = agente.cliente.messages.create(**peticion_orq)
                # 🚨 C.6 — el mismo arreglo que en el worker, y aquí es donde
                #    más se notaba: la capa de arriba es la candidata natural a
                #    llevar el modelo caro, y era la que peor se contaba.
                este_costo = modelos.costo_de(respuesta.usage, capa.modelo)
                gastado_usd += este_costo
                # La báscula del arreglo, igual que en el worker: la estimación
                # se compara con la realidad y las veces que se queda corta se
                # cuentan. Es gratis —el dato ya está pagado— y sin ella el
                # arreglo sería una promesa.
                if este_costo > estimado_usd:
                    estimaciones_cortas += 1
                peor_llamada_usd = max(peor_llamada_usd, este_costo)
                entrada_tokens += respuesta.usage.input_tokens
                salida_tokens += respuesta.usage.output_tokens
                llamadas_api += 1
                anotar("llamada_api", capa=nombre, intento=intento,
                       # ⭐ C.6 — el testigo que la apuesta 2 midió que faltaba.
                       modelo=capa.modelo, esfuerzo=capa.esfuerzo,
                       entrada=respuesta.usage.input_tokens,
                       salida=respuesta.usage.output_tokens,
                       costo_usd=round(este_costo, 6),
                       acumulado_usd=round(gastado_usd, 6),
                       stop_reason=respuesta.stop_reason)
                return respuesta

            except agente.REINTENTABLES as fallo:
                anotar("error_temporal", capa=nombre, intento=intento,
                       tipo=type(fallo).__name__)
                if intento == agente.REINTENTOS_PROPIOS:
                    raise
                espera = 2.0 * (2 ** (intento - 1)) + random.uniform(0, 1)
                if verboso:
                    print(f"     {type(fallo).__name__}, reintento en {espera:.1f}s")
                time.sleep(espera)

            except anthropic.APIStatusError as fallo:
                anotar("error_permanente", capa=nombre,
                       tipo=type(fallo).__name__, codigo=fallo.status_code)
                raise

    def cerrar(texto, ok, motivo, vueltas):
        resultado = {
            "texto":   texto,
            "ok":      ok,
            "motivo":  motivo,
            "vueltas": vueltas,
            "segundos": round(time.monotonic() - arranque, 2),

            # --- LA FACTURA, SEPARADA POR CAPA. Y separada a propósito:
            #     un total solo dice cuánto; el reparto dice DÓNDE, que es lo
            #     único con lo que se puede hacer algo.
            "coste_orquestador_usd": round(gastado_usd, 6),
            # C.2 · cierre — la báscula del techo arreglado, también arriba.
            "peor_llamada_usd": round(peor_llamada_usd, 6),
            "estimaciones_cortas": estimaciones_cortas,
            "coste_workers_usd":     round(contabilidad["coste_workers_usd"], 6),
            "coste_total_usd":       round(gastado_usd
                                           + contabilidad["coste_workers_usd"], 6),
            "llamadas_api_orquestador": llamadas_api,
            "llamadas_api_workers":     contabilidad["llamadas_api_workers"],
            "entrada_orquestador":      entrada_tokens,
            "salida_orquestador":       salida_tokens,
            "entrada_workers":          contabilidad["entrada_workers"],
            "salida_workers":           contabilidad["salida_workers"],
            "workers_usados":           contabilidad["workers"],
            "detalle_workers":          contabilidad["detalle"],
        }

        # ⭐ C.2 — LA PREGUNTA QUE ANTES NO SE PODÍA HACER: ¿se pasó del techo?
        #    Hasta hoy no había techo del encargo contra el que comparar, así que
        #    el total era un dato sin veredicto. Ahora tiene uno.
        if reparto_presupuesto is not None:
            resultado["presupuesto"] = reparto_presupuesto.informe()
            resultado["dentro_del_presupuesto"] = (
                resultado["coste_total_usd"] <= reparto_presupuesto.total_usd)

        anotar("orquestador_fin", capa=nombre, **resultado)
        return resultado

    for vuelta in range(1, max_vueltas + 1):
        try:
            respuesta = hablar_con_el_modelo(historial)
        except PresupuestoAgotado as fallo:
            return cerrar(f"(me detuve: se acabó el presupuesto de arriba — {fallo})",
                          ok=False, motivo="presupuesto", vueltas=vuelta)

        if verboso:
            pedidos = [b.name for b in respuesta.content if b.type == "tool_use"]
            print(f"\n  [orq · vuelta {vuelta}] stop_reason={respuesta.stop_reason}"
                  f" · pidió: {', '.join(pedidos) or '—'} ({len(pedidos)})")

        if respuesta.stop_reason != "tool_use":
            final = next((b.text for b in respuesta.content if b.type == "text"), "")
            return cerrar(final, ok=True, motivo=None, vueltas=vuelta)

        historial.append({"role": "assistant", "content": respuesta.content})

        # ⭐ B.2 — AQUÍ ESTABA EL `for`, Y AHORA ES UN PARÁMETRO.
        #    Este bucle ya no decide si los bloques corren en fila o a la vez.
        #    Lo decide `reparto`, que entra por la puerta de la función.
        #    🔑 Cambiar la topología dejó de ser editar este archivo — y esa es
        #       la forma de todo el bloque B: la topología es una PIEZA DEL
        #       HARNESS que se puede cambiar sin tocar ni el prompt ni el bucle.
        #    📌 Por defecto sigue siendo `reparto_en_serie`, así que A.2 corre
        #       EXACTAMENTE igual que antes y sus números siguen siendo suyos.
        #       El reparto en paralelo lo trae `fan_out.py`.
        bloques = [b for b in respuesta.content if b.type == "tool_use"]
        resultados = reparto(bloques, contabilidad, verboso, funciones)

        historial.append({"role": "user", "content": resultados})

    return cerrar("(se acabaron las vueltas: el orquestador no llegó a una respuesta)",
                  ok=False, motivo="max_vueltas", vueltas=max_vueltas)


# ---------------------------------------------------------------------------
# 5) LA DEMO
# ---------------------------------------------------------------------------
# ⚠️ La tarea NO pide guardar el reporte, y la del duelo sí. Es a propósito:
#    el `guardar_reporte` final es el fan-in, y el fan-in es A.3.
TAREA_DEMO = (
    "Tengo 1.000 dólares, 1.000 euros y 1.000 dólares canadienses. "
    "Dime cuánto es cada uno en pesos hoy, con la fuente y la fecha de cada cifra."
)

def _precio_medido():
    """Lo que han costado las corridas de este archivo, según su registro.

    ⭐ SE LEE DEL REGISTRO Y NO SE ESCRIBE A MANO. Un número copiado aquí sería
       verdad hoy y mentira el día que cambie el modelo — y a un aviso nadie
       vuelve a mirarlo para actualizarlo.
    """
    costes = []
    try:
        with open(REGISTRO, encoding="utf-8") as f:
            for renglon in f:
                try:
                    d = json.loads(renglon)
                except ValueError:
                    continue
                if d.get("evento") == "orquestador_fin" and d.get("coste_total_usd"):
                    costes.append(d["coste_total_usd"])
    except OSError:
        return None
    if not costes:
        return None
    costes.sort()
    return {"n": len(costes), "mediana": costes[len(costes) // 2],
            "peor": costes[-1]}


if __name__ == "__main__":
    print("=" * 70)
    print("A.2 — UN ORQUESTADOR. Sus herramientas son otros agentes.")
    print("A.3 — Y lo que cruza entre las dos capas es un CONTRATO, no una frase.")
    print("=" * 70)
    print("⚠️  Esto es una DEMO, no el duelo. El duelo se corre y se juzga en F.3.")

    if "--pagar" not in sys.argv:
        # 💸 EN PELADO NO SE PAGA — §6.e de `GUIDE.md`, sesión 101.
        #    Aquí muerde MÁS que en `worker.py`: la demo de A.2 arranca TRES
        #    workers, así que la factura de un despiste sale al triple.
        print()
        print("La demo llama al modelo de verdad y arranca TRES workers.")
        print("Por eso no arranca sola.")
        print()
        precio = _precio_medido()
        if precio:
            print(f"  Lo que costaron las {precio['n']} corridas registradas:")
            print(f"    mediana ${precio['mediana']:.6f}  ·  "
                  f"la peor ${precio['peor']:.6f}")
        else:
            print("  (aún no hay corridas registradas de las que sacar el precio)")
        print()
        print("  Para correrla de verdad:")
        print("      python orquestador.py --pagar")
        print()
        print("  📌 Si venías a comprobar que el archivo sigue sano, esto ya lo")
        print("     hizo. Y si buscabas pruebas, están en `presupuesto.py`,")
        print("     `traza.py`, `profundidad.py` y `fallos.py` — todas gratis.")
        raise SystemExit(0)

    r = correr_orquestador(TAREA_DEMO)

    print("\n" + "=" * 70)
    print("RESPUESTA FINAL")
    print("=" * 70)
    print(r["texto"])

    print("\n" + "=" * 70)
    print("LA FACTURA DE LAS DOS CAPAS")
    print("=" * 70)
    print(f"  arriba (orquestador): ${r['coste_orquestador_usd']:.6f}  "
          f"({r['llamadas_api_orquestador']} llamadas API, "
          f"{r['entrada_orquestador']} entrada / {r['salida_orquestador']} salida)")
    print(f"  abajo  ({r['workers_usados']} workers):  ${r['coste_workers_usd']:.6f}  "
          f"({r['llamadas_api_workers']} llamadas API, "
          f"{r['entrada_workers']} entrada / {r['salida_workers']} salida)")
    print(f"  ─────────────────────────────────")
    print(f"  TOTAL:                ${r['coste_total_usd']:.6f}   "
          f"en {r['segundos']} s")

    print("\n  Detalle de la capa de abajo:")
    for d in r["detalle_workers"]:
        print(f"    · {d['worker']:>4}  {d['vueltas']} vueltas · {d['segundos']}s · "
              f"${d['coste_usd']:.6f} · {', '.join(d['herramientas'])}")

    print(f"\n📄 registros: {REGISTRO.name}  +  {worker.REGISTRO.name}")
