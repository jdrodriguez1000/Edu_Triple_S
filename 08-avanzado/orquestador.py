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

    python orquestador.py

💰 CUESTA DINERO, y más que `worker.py`: paga las vueltas del de arriba MÁS las
   de los tres de abajo. La factura de las dos capas se imprime al final,
   separada por capa, que es la única forma de ver dónde se fue.
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
import worker          # noqa: E402


# ---------------------------------------------------------------------------
# 1) CONFIGURACIÓN
# ---------------------------------------------------------------------------

# El mismo modelo arriba y abajo, y el mismo que A. Pieza 0.4 del sobre.
# ⚠️ Y aquí la tentación es mayor que en `worker.py`: "el orquestador piensa
#    más, dale un modelo mejor". Sería razonable en un producto y es veneno en
#    un experimento — lo medido dejaría de ser el esquema.
MODELO = agente.MODELO

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
    linea = {
        "hora": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "evento": evento,
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

    resultado = worker.correr_worker(encargo, nombre=moneda.lower(),
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

    # `pesos` es el campo sin el cual la consulta no sirvió de nada. Que no esté
    # NO es "un campo vacío más": es que esta moneda no se resolvió.
    if not resultado["ok"] or datos.get("pesos") is None:
        return {"error": f"No se pudo consultar {moneda}.",
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

def correr_orquestador(tarea, max_vueltas=MAX_VUELTAS_ORQ,
                       presupuesto_usd=PRESUPUESTO_ORQ_USD, verboso=True,
                       reparto=None, sistema=None, tools=None, funciones=None,
                       nombre="orquestador"):
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

    # ⭐ B.5 — LAS TRES PIEZAS QUE HACÍAN DE ESTE BUCLE «EL» ORQUESTADOR Y AHORA
    #    LO HACEN «UN» ORQUESTADOR: con qué habla, qué menú ve y qué hay detrás.
    #    Con esto, la capa de en medio de B.5 no es un archivo nuevo: es esta
    #    misma función llamada con otros tres argumentos.
    #    📌 Los tres por defecto son los de A.2. Si algún día uno de estos
    #       `or` se pone en verde por accidente, A.2 se entera por sus números.
    sistema = sistema or SISTEMA_ORQ
    tools = tools if tools is not None else TOOLS_ORQ

    gastado_usd = 0.0
    entrada_tokens = 0
    salida_tokens = 0
    llamadas_api = 0

    contabilidad = {
        "capa": nombre,
        "workers": 0,
        "coste_workers_usd": 0.0,
        "llamadas_api_workers": 0,
        "entrada_workers": 0,
        "salida_workers": 0,
        "detalle": [],
    }

    arranque = time.monotonic()
    anotar("orquestador_inicio", capa=nombre, tarea=tarea)

    if verboso:
        print(f"\n🧠 orquestador ← {tarea}")

    historial = [{"role": "user", "content": tarea}]

    def hablar_con_el_modelo(mensajes):
        nonlocal gastado_usd, entrada_tokens, salida_tokens, llamadas_api

        if gastado_usd >= presupuesto_usd:
            raise PresupuestoAgotado(
                f"llevas ${gastado_usd:.4f} de ${presupuesto_usd:.2f}")

        for intento in range(1, agente.REINTENTOS_PROPIOS + 1):
            try:
                respuesta = agente.cliente.messages.create(
                    model=MODELO,
                    max_tokens=2048,
                    system=sistema,
                    tools=tools,
                    messages=mensajes,
                )
                este_costo = agente.costo(respuesta.usage)
                gastado_usd += este_costo
                entrada_tokens += respuesta.usage.input_tokens
                salida_tokens += respuesta.usage.output_tokens
                llamadas_api += 1
                anotar("llamada_api", capa=nombre, intento=intento,
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

if __name__ == "__main__":
    print("=" * 70)
    print("A.2 — UN ORQUESTADOR. Sus herramientas son otros agentes.")
    print("A.3 — Y lo que cruza entre las dos capas es un CONTRATO, no una frase.")
    print("=" * 70)
    print("⚠️  Esto es una DEMO, no el duelo. El duelo se corre y se juzga en F.3.")

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
