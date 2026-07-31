"""
Nivel 1.1 — El programa mas pequeño posible que habla con Claude.

Correr con:  python 01_hola_claude.py
"""

import os
from pathlib import Path

import anthropic
from dotenv import load_dotenv

# Cargamos el .env de la raíz del proyecto (una carpeta más arriba).
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# El cliente es tu conexión a la API. Lee ANTHROPIC_API_KEY del entorno solo.
cliente = anthropic.Anthropic()

respuesta = cliente.messages.create(
    model="claude-opus-5",
    max_tokens=2048,
    messages=[
        {"role": "user", "content": "Explica que es una API en 2 frases, para alguien que empieza a programar."}
    ],
)

# respuesta.content NO es texto: es una LISTA de bloques.
# Un bloque puede ser texto, razonamiento, o una peticion de herramienta.
# Por eso siempre filtramos por tipo antes de leer .text
for bloque in respuesta.content:
    if bloque.type == "text":
        print(bloque.text)

print()
print(f"[tokens] entrada: {respuesta.usage.input_tokens} | salida: {respuesta.usage.output_tokens}")
print(f"[fin]    stop_reason: {respuesta.stop_reason}")
