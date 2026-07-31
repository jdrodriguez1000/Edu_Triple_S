"""
Nivel 3.2 — El bucle agentico completo.

El script 1 se detuvo cuando el modelo pidio la herramienta. Aqui cerramos el
circulo: ejecutamos la funcion de verdad, le devolvemos el resultado, y el
modelo escribe la respuesta final.

El clima de aqui es INVENTADO (un diccionario). A proposito: en este script el
protagonista es el bucle, no el clima. La API real llega en el script 3.

Correr con:  python 02_bucle.py
Cuesta:      ~$0.030 medido (3 preguntas x 2 llamadas cada una, con Opus 5)
"""

import json
import sys
from pathlib import Path

import anthropic
from dotenv import load_dotenv

# La consola de Windows imprime en cp1252, que no conoce el simbolo de grados
# ni las tildes que Claude usa al responder. Sin esta linea el script CORRE
# BIEN y revienta al final, al imprimir. El agente no fallo: fallo la pantalla.
sys.stdout.reconfigure(encoding="utf-8")

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
cliente = anthropic.Anthropic()

MODELO = "claude-opus-5"

# ---------------------------------------------------------------------------
# 1) LA FUNCION DE VERDAD
# Esta si es codigo Python normal. El modelo nunca la ve ni la ejecuta.
# ---------------------------------------------------------------------------
CLIMA_FALSO = {
    "bogota": {"temperatura_c": 14, "estado": "lloviznando"},
    "medellin": {"temperatura_c": 24, "estado": "despejado"},
    "cartagena": {"temperatura_c": 32, "estado": "humedo y soleado"},
}


def obtener_clima(ciudad: str) -> str:
    """Busca la ciudad en el diccionario. Devuelve SIEMPRE un string."""
    dato = CLIMA_FALSO.get(ciudad.strip().lower())
    if dato is None:
        # Ojo: no lanzamos una excepcion. Devolvemos un texto explicativo.
        # El modelo lee este texto y sabe reaccionar. Un crash no lo lee nadie.
        return f"No tengo datos de '{ciudad}'. Ciudades disponibles: Bogota, Medellin, Cartagena."
    return f"{dato['temperatura_c']} grados centigrados, {dato['estado']}."


# ---------------------------------------------------------------------------
# 2) EL MENU que ve el modelo (identico al del script 1)
# ---------------------------------------------------------------------------
HERRAMIENTAS = [
    {
        "name": "obtener_clima",
        "description": (
            "Devuelve el clima actual de una ciudad. Usala siempre que te "
            "pregunten por el clima, la temperatura o si llueve en algun lugar."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "ciudad": {
                    "type": "string",
                    "description": "Nombre de la ciudad, por ejemplo: Bogota",
                }
            },
            "required": ["ciudad"],
        },
    }
]

# El puente entre el nombre que dice el modelo y la funcion real de Python.
# Sin este diccionario, 'obtener_clima' seria solo un string sin dueno.
FUNCIONES = {"obtener_clima": obtener_clima}


def ejecutar_agente(pregunta: str, max_vueltas: int = 5) -> str:
    """El bucle agentico. Estas 40 lineas son el corazon de todo agente."""
    historial = [{"role": "user", "content": pregunta}]

    for vuelta in range(1, max_vueltas + 1):
        respuesta = cliente.messages.create(
            model=MODELO,
            max_tokens=2048,
            tools=HERRAMIENTAS,
            messages=historial,
        )

        entrada = respuesta.usage.input_tokens
        salida = respuesta.usage.output_tokens
        print(f"  [vuelta {vuelta}] stop_reason={respuesta.stop_reason} "
              f"entrada={entrada} salida={salida}")

        # -- CASO A: el modelo termino. Salimos del bucle.
        if respuesta.stop_reason != "tool_use":
            return next((b.text for b in respuesta.content if b.type == "text"), "")

        # -- CASO B: el modelo pidio herramientas.

        # B.1 Guardar la peticion del modelo TAL CUAL vino.
        # Se guarda respuesta.content entero, no solo el texto. Si le quitas
        # los bloques tool_use, la API rechaza el siguiente mensaje.
        historial.append({"role": "assistant", "content": respuesta.content})

        # B.2 Ejecutar cada herramienta pedida. Pueden ser varias en un turno.
        resultados = []
        for bloque in respuesta.content:
            if bloque.type != "tool_use":
                continue

            funcion = FUNCIONES[bloque.name]
            salida_herramienta = funcion(**bloque.input)   # aqui corre TU codigo
            print(f"     -> ejecuto {bloque.name}({json.dumps(bloque.input, ensure_ascii=False)})")
            print(f"        devolvio: {salida_herramienta}")

            resultados.append({
                "type": "tool_result",
                "tool_use_id": bloque.id,      # el ticket del script 1
                "content": salida_herramienta,
            })

        # B.3 Devolver los resultados. Van con role 'user', aunque no los
        # escribiste tu: para la API, todo lo que entra al modelo es 'user'.
        # TODOS los resultados van en UN solo mensaje.
        historial.append({"role": "user", "content": resultados})

    return "(el agente se quedo dando vueltas y se corto el limite)"


PREGUNTAS = [
    "Que clima hace en Medellin?",
    "Me llevo paraguas si voy a Bogota?",
    "Que clima hace en Tokio?",
]

for pregunta in PREGUNTAS:
    print(f"\n=== {pregunta}")
    print(f"RESPUESTA: {ejecutar_agente(pregunta)}")

print("""

Lectura del resultado
---------------------
Mira las lineas [vuelta N] de cada pregunta. El patron es siempre el mismo:

  vuelta 1 -> stop_reason=tool_use   (el modelo pide)
  ...ejecuta tu codigo...
  vuelta 2 -> stop_reason=end_turn   (el modelo responde con el dato en mano)

Una pregunta = DOS llamadas a la API. Un agente cuesta al menos el doble que
un chat. Y fijate en la 'entrada' de la vuelta 2: subio, porque ahora tambien
se paga el menu de herramientas, la peticion y el resultado. Es el nivel 2
otra vez: todo lo que pasa se reenvia.

Tres cosas para no olvidar:
1. La tercera pregunta (Tokio) no esta en el diccionario. La funcion devolvio
   un texto de error en vez de reventar, el modelo lo LEYO y te contesto algo
   util. Un agente que lanza excepciones se muere; uno que devuelve texto se
   recupera.
2. El limite max_vueltas no es adorno. Sin el, un modelo confundido puede
   pedir la misma herramienta para siempre y vaciarte la cuenta.
3. Este bucle es literalmente lo que hace Claude Code. Cambia el diccionario
   FUNCIONES por leer_archivo, escribir_archivo y correr_comando, y tienes un
   agente de programacion. El bucle no cambia. Cambian las herramientas.
""")
