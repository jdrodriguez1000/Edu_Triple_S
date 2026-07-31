"""
Nivel 3.1 — El modelo PIDE. No ejecuta.

Este script le da a Claude una herramienta y le hace una pregunta que no puede
responder solo. Y luego SE DETIENE, a proposito, sin ejecutar nada.

El objetivo es que veas con tus ojos que el modelo no hizo nada: solo devolvio
un papelito diciendo "necesito que llames a obtener_clima con ciudad=Bogota".

Correr con:  python 01_pedir_herramienta.py
Cuesta:      menos de 1 centavo
"""

import json
import sys
from pathlib import Path

import anthropic
from dotenv import load_dotenv

# La consola de Windows imprime en cp1252 y revienta con tildes o el simbolo
# de grados. Esta linea la pone en utf-8. Ver la nota larga en 02_bucle.py.
sys.stdout.reconfigure(encoding="utf-8")

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
cliente = anthropic.Anthropic()

MODELO = "claude-opus-5"

# ---------------------------------------------------------------------------
# LA HERRAMIENTA
#
# Esto NO es codigo que se ejecuta. Es una DESCRIPCION en JSON que se manda
# junto con el mensaje. Es un menu: le dices al modelo que puede pedir.
#
# Los tres campos son obligatorios y los tres importan:
#   name         -> como se llama (tu codigo lo usara para saber a que funcion ir)
#   description  -> CUANDO usarla. Es lo que mas influye en el comportamiento.
#   input_schema -> que argumentos acepta, en formato JSON Schema
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

PREGUNTA = "Que clima hace ahora mismo en Bogota?"

respuesta = cliente.messages.create(
    model=MODELO,
    max_tokens=2048,
    tools=HERRAMIENTAS,          # <- la unica linea nueva frente al nivel 2
    messages=[{"role": "user", "content": PREGUNTA}],
)

print(f"Pregunta: {PREGUNTA}\n")
print(f"stop_reason: {respuesta.stop_reason}")
print(f"bloques en content: {len(respuesta.content)}\n")

# Recorremos los bloques. Igual que en el nivel 1: NUNCA asumas que content[0]
# es texto. Aqui hay un tipo de bloque nuevo: 'tool_use'.
for i, bloque in enumerate(respuesta.content):
    print(f"--- bloque {i}: type = {bloque.type}")
    if bloque.type == "text":
        print(bloque.text)
    elif bloque.type == "thinking":
        print("(razonamiento interno; puede venir vacio)")
    elif bloque.type == "tool_use":
        print(f"  id     : {bloque.id}")
        print(f"  name   : {bloque.name}")
        print(f"  input  : {json.dumps(bloque.input, ensure_ascii=False)}")
    print()

print(f"""
Lectura del resultado
---------------------
1. stop_reason es 'tool_use', no 'end_turn'. Esa es la senal. Significa:
   "no termine, estoy esperando algo tuyo".

2. Aparecio un bloque nuevo: type = 'tool_use'. Trae tres cosas:
   - name  : cual herramienta quiere
   - input : con que argumentos (fijate que saco 'Bogota' de tu frase solo)
   - id    : un numero de ticket. Cuando le devuelvas el resultado tendras que
             citar ESE id exacto, o la API te rechaza el mensaje.

3. NO PASO NADA MAS. No hay temperatura. No se llamo a ninguna API del clima.
   No existe ninguna funcion obtener_clima en este archivo. El modelo escribio
   una peticion y se callo.

Aqui esta la idea central del nivel: el modelo no ejecuta. El modelo PIDE.
Quien ejecuta eres tu. Ese es el trabajo del harness.

Analogia: le pasaste a alguien encerrado en un cuarto un menu de restaurante.
El te devolvio el pedido escrito en un papel. El papel no es comida. Alguien
tiene que ir a la cocina. Ese alguien es tu codigo, y eso es el script 2.
""")
