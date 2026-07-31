"""
Nivel 3.3 — Un agente con datos de verdad, y con dos herramientas.

Dos cambios frente al script 2:
  1. El clima ya no es inventado: sale de una API publica real (Open-Meteo,
     gratis y sin llave). Ahora el modelo de verdad NO PODIA saber la respuesta.
  2. Hay DOS herramientas. Nadie le dice al modelo cual usar: elige solo,
     leyendo tu pregunta y las descripciones que escribiste.

Necesita internet. Si no hay, la herramienta devuelve un texto de error y el
agente lo maneja (esa parte tambien es la leccion).

Correr con:  python 03_agente_real.py
Cuesta:      ~$0.037 medido (4 preguntas, 7 llamadas en total, con Opus 5)
"""

import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import anthropic
from dotenv import load_dotenv

# Ver nota en 02_bucle.py: sin esto, la consola de Windows revienta al imprimir
# tildes o el simbolo de grados que devuelve Claude.
sys.stdout.reconfigure(encoding="utf-8")

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
cliente = anthropic.Anthropic()

MODELO = "claude-opus-5"

# Codigos WMO -> texto. La API devuelve un numero; el modelo entiende mejor
# una palabra. Traducir el dato antes de entregarlo es trabajo del harness.
TIEMPO = {
    0: "despejado", 1: "casi despejado", 2: "parcialmente nublado", 3: "nublado",
    45: "niebla", 48: "niebla con escarcha", 51: "llovizna debil",
    53: "llovizna", 55: "llovizna fuerte", 61: "lluvia debil", 63: "lluvia",
    65: "lluvia fuerte", 71: "nieve debil", 73: "nieve", 75: "nieve fuerte",
    80: "chubascos", 81: "chubascos fuertes", 82: "chubascos violentos",
    95: "tormenta electrica", 96: "tormenta con granizo", 99: "tormenta con granizo fuerte",
}


def _pedir_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=10) as r:
        return json.loads(r.read().decode("utf-8"))


# ---------------------------------------------------------------------------
# HERRAMIENTA 1 — clima real. Son DOS llamadas HTTP: primero traducimos el
# nombre de la ciudad a coordenadas, despues pedimos el clima de ese punto.
# El modelo no sabe nada de esto. Solo dijo "Bogota".
# ---------------------------------------------------------------------------
def obtener_clima(ciudad: str) -> str:
    try:
        q = urllib.parse.quote(ciudad)
        geo = _pedir_json(
            f"https://geocoding-api.open-meteo.com/v1/search?name={q}&count=1&language=es"
        )
        if not geo.get("results"):
            return f"No encontre ninguna ciudad llamada '{ciudad}'."

        lugar = geo["results"][0]
        lat, lon = lugar["latitude"], lugar["longitude"]

        datos = _pedir_json(
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
            "&current=temperature_2m,weather_code,wind_speed_10m"
        )
        actual = datos["current"]
        estado = TIEMPO.get(actual["weather_code"], "estado desconocido")

        return (
            f"{lugar['name']} ({lugar.get('country', '?')}): "
            f"{actual['temperature_2m']} C, {estado}, "
            f"viento {actual['wind_speed_10m']} km/h."
        )
    except Exception as e:
        # Nunca dejamos que una excepcion suba al bucle: la convertimos en texto.
        return f"Error consultando el clima de '{ciudad}': {type(e).__name__}."


# ---------------------------------------------------------------------------
# HERRAMIENTA 2 — la hora. Dato trivial para ti, imposible para el modelo:
# el no tiene reloj. Sirve para ver como ELIGE entre dos herramientas.
# ---------------------------------------------------------------------------
def hora_utc() -> str:
    return datetime.now(timezone.utc).strftime("Ahora son las %H:%M UTC del %d/%m/%Y.")


HERRAMIENTAS = [
    {
        "name": "obtener_clima",
        "description": (
            "Devuelve el clima actual real de una ciudad: temperatura, estado "
            "del cielo y viento. Usala para cualquier pregunta sobre clima, "
            "temperatura, lluvia o viento en un lugar."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "ciudad": {"type": "string", "description": "Nombre de la ciudad"}
            },
            "required": ["ciudad"],
        },
    },
    {
        "name": "hora_utc",
        "description": (
            "Devuelve la fecha y hora actual en UTC. Usala cuando te pregunten "
            "que hora es o que dia es hoy."
        ),
        "input_schema": {"type": "object", "properties": {}},
    },
]

FUNCIONES = {"obtener_clima": obtener_clima, "hora_utc": hora_utc}

SYSTEM = (
    "Eres un asistente breve. Responde en espanol, en 2 o 3 frases. "
    "Nunca inventes datos de clima ni de hora: usa siempre las herramientas."
)


def ejecutar_agente(pregunta: str, max_vueltas: int = 6) -> str:
    """Mismo bucle del script 2. No cambio ni una linea de logica."""
    historial = [{"role": "user", "content": pregunta}]

    for vuelta in range(1, max_vueltas + 1):
        respuesta = cliente.messages.create(
            model=MODELO,
            max_tokens=2048,
            system=SYSTEM,
            tools=HERRAMIENTAS,
            messages=historial,
        )
        print(f"  [vuelta {vuelta}] stop_reason={respuesta.stop_reason} "
              f"entrada={respuesta.usage.input_tokens} "
              f"salida={respuesta.usage.output_tokens}")

        if respuesta.stop_reason != "tool_use":
            return next((b.text for b in respuesta.content if b.type == "text"), "")

        historial.append({"role": "assistant", "content": respuesta.content})

        resultados = []
        for bloque in respuesta.content:
            if bloque.type != "tool_use":
                continue
            resultado = FUNCIONES[bloque.name](**bloque.input)
            print(f"     -> {bloque.name}({json.dumps(bloque.input, ensure_ascii=False)})")
            print(f"        {resultado}")
            resultados.append({
                "type": "tool_result",
                "tool_use_id": bloque.id,
                "content": resultado,
            })

        historial.append({"role": "user", "content": resultados})

    return "(se acabaron las vueltas)"


PREGUNTAS = [
    "Que hora es?",                                   # deberia usar solo hora_utc
    "Que clima hace ahora en Bucaramanga?",           # deberia usar solo obtener_clima
    "Compara el clima de Bogota y el de Cartagena.",  # deberia pedir la herramienta 2 veces
    "Cuanto es 17 por 23?",                           # no deberia usar ninguna
]

for pregunta in PREGUNTAS:
    print(f"\n=== {pregunta}")
    print(f"RESPUESTA: {ejecutar_agente(pregunta)}")

print("""

Lectura del resultado
---------------------
Revisa, pregunta por pregunta, QUE herramienta eligio y CUANTAS veces:

- "Que hora es?"           -> hora_utc. Ignoro el clima.
- "Clima en Bucaramanga"   -> obtener_clima. Ignoro la hora.
- "Compara Bogota y Cartagena" -> pidio obtener_clima DOS veces. Fijate si las
  dos peticiones vinieron en la MISMA vuelta (dos bloques tool_use en un solo
  turno) o en vueltas separadas. Las dos formas son validas y las dos las
  maneja el bucle, porque recorremos todos los bloques con un for.
- "17 por 23"              -> ninguna. stop_reason fue 'end_turn' en la vuelta 1.

Nadie programo esas decisiones. No hay un solo if en este archivo que diga
"si la pregunta menciona hora, llama a hora_utc". Lo unico que hay son las
descripciones que escribiste en HERRAMIENTAS. Esas descripciones SON el
programa. Cambialas y cambias el comportamiento sin tocar una linea de codigo.

Y ahora si es informacion que el modelo no podia tener: la temperatura de
Bucaramanga de este minuto no estaba en sus datos de entrenamiento. Salio de
tu funcion. Eso es un agente: un modelo mas un puente hacia el mundo real.

Lo que TODAVIA no tiene este agente (y llega en el nivel 4):
  - no reintenta si la red falla, solo reporta el error
  - no tiene timeout global ni tope de gasto
  - no pide permiso antes de actuar (aqui da igual, pero imagina borrar_archivo)
  - no guarda ningun registro de lo que hizo
Eso es el harness de verdad.
""")
