"""
Nivel 4.3 — El harness de verdad.

Es el mismo agente del nivel 3. La diferencia esta toda alrededor del modelo:

  1. TIMEOUT y REINTENTOS elegidos a mano, no los que vienen de fabrica.
  2. ERRORES tipados: cada falla se maneja distinta y ninguna revienta el bucle.
  3. PRESUPUESTO en dolares: el agente se detiene cuando gasta de mas.
  4. TOPE DE VUELTAS: el agente se detiene si se queda dando vueltas.
  5. PERMISOS: hay una herramienta que borra archivos. Pregunta antes.
  6. REGISTRO: todo queda escrito en registro.jsonl, una linea por evento.

Ninguna de las 6 hace al agente mas inteligente. Las 6 lo hacen confiable,
que es otra cosa y es la que se cobra.

Este script CREA una carpeta 'caja/' con dos archivos de mentira, para que la
herramienta de borrar tenga algo real que borrar sin tocar nada tuyo.

Correr con:  python 03_harness.py
Cuesta:      ~$0.05 (tope duro de $0.10 puesto en el codigo)
Es INTERACTIVO: te va a pedir permiso antes de borrar. Responde s o n.
"""

import json
import random
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import anthropic
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")

AQUI = Path(__file__).resolve().parent
load_dotenv(AQUI.parent / ".env")

# ---------------------------------------------------------------------------
# 1. LA CONFIGURACION DEL HARNESS
# Todo numero que gobierna el comportamiento vive aqui arriba, con nombre.
# Un limite escondido a la mitad del archivo es un limite que nadie ajusta.
# ---------------------------------------------------------------------------
MODELO = "claude-opus-5"

TIMEOUT_SEGUNDOS = 30.0     # por INTENTO (ver script 2)
REINTENTOS_SDK = 0          # apagado: el nuestro esta mas abajo
REINTENTOS_PROPIOS = 3
MAX_VUELTAS = 6             # vueltas del bucle agentico por pregunta
PRESUPUESTO_USD = 0.10      # para TODA la corrida, no por pregunta

# Precios de claude-opus-5, por millon de tokens (ver README de la raiz).
PRECIO_ENTRADA = 5.00
PRECIO_SALIDA = 25.00

REGISTRO = AQUI / "registro.jsonl"
CAJA = AQUI / "caja"

cliente = anthropic.Anthropic(
    timeout=TIMEOUT_SEGUNDOS,
    max_retries=REINTENTOS_SDK,
)

gastado_usd = 0.0   # se va sumando en cada llamada


class PresupuestoAgotado(Exception):
    """No es un error de la API. Es una decision nuestra."""


# ---------------------------------------------------------------------------
# 6. EL REGISTRO
# Una linea de JSON por evento. Formato .jsonl: se puede leer con los ojos,
# se puede abrir a mitad de escritura, y se procesa linea por linea sin
# cargar el archivo entero. Es lo que usa media industria para logs.
#
# Sin esto, cuando el agente haga algo raro solo tienes tu memoria.
# ---------------------------------------------------------------------------
def anotar(evento: str, **datos) -> None:
    linea = {
        "hora": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "evento": evento,
        **datos,
    }
    with open(REGISTRO, "a", encoding="utf-8") as f:
        f.write(json.dumps(linea, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# LAS HERRAMIENTAS (dos del nivel 3, una nueva y peligrosa)
# ---------------------------------------------------------------------------
TIEMPO = {
    0: "despejado", 1: "casi despejado", 2: "parcialmente nublado", 3: "nublado",
    45: "niebla", 51: "llovizna debil", 53: "llovizna", 55: "llovizna fuerte",
    61: "lluvia debil", 63: "lluvia", 65: "lluvia fuerte", 80: "chubascos",
    95: "tormenta electrica",
}


def _pedir_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=10) as r:
        return json.loads(r.read().decode("utf-8"))


def obtener_clima(ciudad: str) -> str:
    try:
        q = urllib.parse.quote(ciudad)
        geo = _pedir_json(
            f"https://geocoding-api.open-meteo.com/v1/search?name={q}&count=1&language=es"
        )
        if not geo.get("results"):
            return f"No encontre ninguna ciudad llamada '{ciudad}'."
        lugar = geo["results"][0]
        datos = _pedir_json(
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lugar['latitude']}&longitude={lugar['longitude']}"
            f"&current=temperature_2m,weather_code"
        )
        actual = datos["current"]
        cielo = TIEMPO.get(actual["weather_code"], "condicion desconocida")
        return f"{lugar['name']}: {actual['temperature_2m']} C, {cielo}."
    except Exception as e:
        # La herramienta NUNCA revienta: devuelve el error como texto para que
        # el modelo lo lea y decida. Un agente no se cae porque falle una API.
        return f"Error consultando el clima de '{ciudad}': {type(e).__name__}."


def hora_utc() -> str:
    return datetime.now(timezone.utc).strftime("Son las %H:%M UTC del %d/%m/%Y.")


def listar_archivos() -> str:
    nombres = sorted(p.name for p in CAJA.iterdir())
    return f"En la caja hay: {', '.join(nombres)}." if nombres else "La caja esta vacia."


def borrar_archivo(nombre: str) -> str:
    """La herramienta peligrosa. Fijate que aqui NO hay ninguna pregunta:
    el permiso se pide afuera, en el harness. La funcion solo obedece."""
    objetivo = CAJA / nombre
    # Aun con permiso, la herramienta se defiende: solo borra dentro de caja/.
    # Si el modelo pide "../../.env", esto lo para.
    if objetivo.parent.resolve() != CAJA.resolve() or not objetivo.exists():
        return f"No existe ningun archivo '{nombre}' en la caja."
    objetivo.unlink()
    return f"Borrado '{nombre}'."


HERRAMIENTAS = [
    {
        "name": "obtener_clima",
        "description": "Clima actual de una ciudad. Usala cuando pregunten por el tiempo.",
        "input_schema": {
            "type": "object",
            "properties": {"ciudad": {"type": "string", "description": "Nombre de la ciudad"}},
            "required": ["ciudad"],
        },
    },
    {
        "name": "hora_utc",
        "description": "La hora y fecha actuales en UTC.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "listar_archivos",
        "description": "Lista los archivos guardados en la caja del usuario.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "borrar_archivo",
        "description": "Borra un archivo de la caja del usuario. La accion no se puede deshacer.",
        "input_schema": {
            "type": "object",
            "properties": {"nombre": {"type": "string", "description": "Nombre exacto del archivo"}},
            "required": ["nombre"],
        },
    },
]

FUNCIONES = {
    "obtener_clima": obtener_clima,
    "hora_utc": hora_utc,
    "listar_archivos": listar_archivos,
    "borrar_archivo": borrar_archivo,
}

# ---------------------------------------------------------------------------
# 5. LOS PERMISOS
# La politica NO vive en la descripcion de la herramienta (eso lo lee el
# modelo, y el modelo se puede equivocar o lo pueden convencer). Vive en tu
# codigo, donde el modelo no llega.
#
#   permitir  -> corre sola
#   preguntar -> el humano decide, en el momento
#   prohibir  -> ni preguntamos
# ---------------------------------------------------------------------------
PERMISOS = {
    "obtener_clima": "permitir",
    "hora_utc": "permitir",
    "listar_archivos": "permitir",
    "borrar_archivo": "preguntar",
}


def pedir_permiso(nombre: str, entrada: dict) -> tuple[bool, str]:
    politica = PERMISOS.get(nombre, "prohibir")   # lo desconocido se prohibe
    if politica == "permitir":
        return True, "permitida por politica"
    if politica == "prohibir":
        return False, "prohibida por politica"

    argumentos = json.dumps(entrada, ensure_ascii=False)
    print(f"\n     PERMISO: el agente quiere ejecutar {nombre}({argumentos})")
    respuesta = input("     Lo dejas? [s/n] ").strip().lower()

    # ANTES DECIA:  if respuesta.startswith("s")
    # Y era un agujero de seguridad de verdad, encontrado por un eval del
    # nivel 5. Con startswith, CUALQUIER palabra que empiece por 's'
    # autorizaba el borrado -- incluidas justo las que teclea alguien que
    # quiere abortar: "salir", "stop", "suspende", "sal de ahi".
    # El freno se abria con la palabra que uno escribe para cerrarlo.
    #
    # Denegar por defecto tambien se aplica AQUI, no solo al diccionario
    # PERMISOS: solo un si explicito es un si. Todo lo demas es no.
    if respuesta in {"s", "si", "sí"}:
        return True, "autorizada por el usuario"
    return False, "rechazada por el usuario"


# ---------------------------------------------------------------------------
# 2, 3 y 4. LA LLAMADA BLINDADA
# Una sola funcion se encarga de: revisar presupuesto, medir gasto, reintentar
# lo reintentable, y traducir lo irreintentable a algo que el bucle entienda.
# ---------------------------------------------------------------------------
REINTENTABLES = (
    anthropic.RateLimitError,
    anthropic.InternalServerError,
    anthropic.APIConnectionError,
)


def costo(usage) -> float:
    return (usage.input_tokens * PRECIO_ENTRADA
            + usage.output_tokens * PRECIO_SALIDA) / 1_000_000


def llamar_modelo(historial: list) -> anthropic.types.Message:
    global gastado_usd

    # El presupuesto se revisa ANTES de gastar. Revisarlo despues es contar
    # el dinero que ya no tienes.
    if gastado_usd >= PRESUPUESTO_USD:
        raise PresupuestoAgotado(f"llevas ${gastado_usd:.4f}")

    for intento in range(1, REINTENTOS_PROPIOS + 1):
        try:
            inicio = time.monotonic()
            respuesta = cliente.messages.create(
                model=MODELO,
                max_tokens=1024,
                system=(
                    "Eres un asistente breve. Responde en espanol de Colombia, "
                    "en dos frases como maximo. Si una herramienta te dice que "
                    "no pudo hacer algo, dilo con claridad en vez de inventar."
                ),
                tools=HERRAMIENTAS,
                messages=historial,
            )
            demora = time.monotonic() - inicio

            este_costo = costo(respuesta.usage)
            gastado_usd += este_costo
            anotar(
                "llamada_api",
                intento=intento,
                segundos=round(demora, 2),
                entrada=respuesta.usage.input_tokens,
                salida=respuesta.usage.output_tokens,
                costo_usd=round(este_costo, 6),
                acumulado_usd=round(gastado_usd, 6),
                stop_reason=respuesta.stop_reason,
            )
            return respuesta

        except REINTENTABLES as e:
            anotar("error_temporal", intento=intento, tipo=type(e).__name__)
            if intento == REINTENTOS_PROPIOS:
                raise
            espera = 2.0 * (2 ** (intento - 1)) + random.uniform(0, 1)
            print(f"     red o servidor fallo ({type(e).__name__}), "
                  f"reintento en {espera:.1f}s")
            time.sleep(espera)

        except anthropic.APIStatusError as e:
            # 400, 401, 403, 404... esperar no arregla nada. Cortamos ya.
            anotar("error_permanente", tipo=type(e).__name__, codigo=e.status_code)
            raise


# ---------------------------------------------------------------------------
# EL BUCLE, ahora con dos frenos: presupuesto y vueltas.
# ---------------------------------------------------------------------------
def ejecutar_agente(pregunta: str) -> str:
    anotar("pregunta", texto=pregunta)
    historial = [{"role": "user", "content": pregunta}]

    for vuelta in range(1, MAX_VUELTAS + 1):
        try:
            respuesta = llamar_modelo(historial)
        except PresupuestoAgotado as e:
            anotar("detenido", motivo="presupuesto", detalle=str(e))
            return f"(me detuve: se acabo el presupuesto — {e})"
        except anthropic.APIError as e:
            anotar("detenido", motivo="api", detalle=type(e).__name__)
            return f"(me detuve: la API fallo con {type(e).__name__})"

        print(f"  vuelta {vuelta}: stop_reason={respuesta.stop_reason}  "
              f"gastado=${gastado_usd:.4f}")

        if respuesta.stop_reason != "tool_use":
            texto = next((b.text for b in respuesta.content if b.type == "text"), "")
            anotar("respuesta_final", vueltas=vuelta, texto=texto)
            return texto

        historial.append({"role": "assistant", "content": respuesta.content})

        resultados = []
        for bloque in respuesta.content:
            if bloque.type != "tool_use":
                continue

            permitida, motivo = pedir_permiso(bloque.name, bloque.input)
            if permitida:
                resultado = FUNCIONES[bloque.name](**bloque.input)
            else:
                # Clave: el modelo TIENE que enterarse de que le dijimos que no.
                # Si no, cree que se hizo y le miente al usuario.
                resultado = f"PERMISO DENEGADO: el usuario no autorizo {bloque.name}."

            anotar("herramienta", nombre=bloque.name, entrada=bloque.input,
                   permiso=motivo, resultado=resultado)
            print(f"     {bloque.name}({json.dumps(bloque.input, ensure_ascii=False)})"
                  f"  [{motivo}]")
            print(f"       -> {resultado}")

            resultados.append({
                "type": "tool_result",
                "tool_use_id": bloque.id,
                "content": resultado,
            })

        historial.append({"role": "user", "content": resultados})

    # Si llegamos aqui, el modelo pidio herramientas MAX_VUELTAS veces seguidas
    # sin dar una respuesta. Puede ser un bucle infinito. Cortamos nosotros.
    anotar("detenido", motivo="max_vueltas", vueltas=MAX_VUELTAS)
    return f"(me detuve: {MAX_VUELTAS} vueltas sin llegar a una respuesta)"


# ---------------------------------------------------------------------------
# PREPARAR LA CAJA Y CORRER
# ---------------------------------------------------------------------------
PREGUNTAS = [
    "Que archivos tengo guardados?",
    "Borra el archivo borrador.txt, ya no lo necesito.",
    "Que clima hace en Bucaramanga y que hora es en UTC?",
]


def main():
    """Todo lo que EJECUTA vive aqui dentro. Antes estaba suelto en el
    cuerpo del archivo, y por eso el harness no se podia importar sin
    que arrancara solo: creaba la caja, hacia las 3 preguntas, gastaba
    los $0.03 y se quedaba esperando que alguien tecleara s/n.

    Se descubrio en el nivel 5, al intentar PROBAR estas piezas.
    -> Para poder probar tu codigo, tiene que poder cargarse sin
       ejecutarse. Eso es lo que hace el 'if __name__' de abajo, y no
       es decoracion: separa "este archivo ES un programa" de "este
       archivo OFRECE piezas"."""
    CAJA.mkdir(exist_ok=True)
    (CAJA / "notas.txt").write_text("apuntes del curso\n", encoding="utf-8")
    (CAJA / "borrador.txt").write_text("esto es basura\n", encoding="utf-8")

    anotar("inicio", modelo=MODELO, presupuesto_usd=PRESUPUESTO_USD,
           max_vueltas=MAX_VUELTAS, timeout=TIMEOUT_SEGUNDOS)

    for pregunta in PREGUNTAS:
        print(f"\n=== {pregunta}")
        print(f"RESPUESTA: {ejecutar_agente(pregunta)}")

    anotar("fin", gastado_usd=round(gastado_usd, 6))

    print(f"""

Gasto total de la corrida: ${gastado_usd:.4f} de ${PRESUPUESTO_USD:.2f}
Quedaron en la caja: {', '.join(sorted(p.name for p in CAJA.iterdir())) or '(nada)'}
Registro escrito en: {REGISTRO.name}

Lectura del resultado
---------------------
Mira el registro.jsonl. Ahi esta TODO: cada llamada con su costo, cada
herramienta con lo que pidio y lo que le contestamos, cada permiso con quien
lo dio. Eso es lo que te va a salvar el dia que el agente haga algo raro.

Las 6 piezas y para que sirve cada una:

  timeout + reintentos  -> que un problema ajeno no cuelgue tu programa
  errores tipados       -> reintentar lo temporal, cortar lo permanente
  presupuesto           -> que un bucle no te vacie la cuenta
  tope de vueltas       -> que un bucle no sea infinito
  permisos              -> que el modelo no decida solo lo irreversible
  registro              -> poder explicar despues que fue lo que paso

Fijate donde vive cada decision:

- El PERMISO no esta en la descripcion de la herramienta. Esta en el
  diccionario PERMISOS, en tu codigo. Lo que el modelo lee, el modelo lo
  puede ignorar; lo que esta en tu 'if', no.

- La herramienta borrar_archivo se defiende SOLA ademas del permiso: revisa
  que el archivo este dentro de caja/. Dos candados para la misma puerta,
  porque el permiso lo puede dar un humano distraido.

- Cuando dices que NO, el resultado que le devuelves al modelo es
  'PERMISO DENEGADO'. Tiene que enterarse. Si le devuelves silencio o un
  texto vacio, sigue como si lo hubiera hecho y le dice al usuario 'listo,
  ya lo borre'. Un agente que miente sin querer sigue mintiendo.
""")


# Esta linea es la que decide si el archivo corre o solo se deja usar.
# Si lo ejecutas ("python 03_harness.py"), __name__ vale "__main__" y
# main() arranca. Si otro archivo lo importa, __name__ vale "harness" y
# no pasa nada: solo quedan disponibles las funciones y las constantes.
if __name__ == "__main__":
    main()
