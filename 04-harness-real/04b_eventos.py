"""
Ejercicio 8 del nivel 4 — ¿Que llega en el silencio del streaming?

En 04_streaming.py la pantalla estuvo quieta ~6 segundos aunque el streaming
ya estaba corriendo. Hipotesis: text_stream entrega SOLO texto, y lo primero
que genera el modelo es un bloque 'thinking'.

Aqui iteramos el stream CRUDO en vez de text_stream, con cronometro, para ver
que llega y cuando.
"""

import sys
import time
from pathlib import Path

import anthropic
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

cliente = anthropic.Anthropic(timeout=60.0)
MODELO = "claude-opus-5"
PREGUNTA = ("Explicale a un principiante, en unas 200 palabras, por que un "
            "agente de IA necesita un timeout. Espanol de Colombia.")


print("=== Eventos crudos del stream\n")
inicio = time.monotonic()

primera_vez = {}   # tipo de pedazo -> segundo en que llego el primero
conteo = {}        # tipo de pedazo -> cuantos llegaron
razonamiento = []  # el resumen del thinking, si viene

with cliente.messages.stream(
    model=MODELO,
    max_tokens=1500,
    thinking={"type": "adaptive", "display": "summarized"},
    messages=[{"role": "user", "content": PREGUNTA}],
) as stream:

    for evento in stream:
        t = time.monotonic() - inicio

        if evento.type == "content_block_start":
            print(f"{t:6.2f}s  EMPIEZA bloque tipo '{evento.content_block.type}'")

        elif evento.type == "content_block_delta":
            tipo = evento.delta.type
            conteo[tipo] = conteo.get(tipo, 0) + 1
            if tipo not in primera_vez:
                primera_vez[tipo] = t
                print(f"{t:6.2f}s     <- primer pedazo de tipo '{tipo}'")
            if tipo == "thinking_delta":
                razonamiento.append(evento.delta.thinking)

        elif evento.type == "content_block_stop":
            print(f"{t:6.2f}s  TERMINA bloque")

        elif evento.type in ("message_start", "message_delta", "message_stop"):
            print(f"{t:6.2f}s  {evento.type}")

        else:
            # messages.stream() no es el stream pelado: es un AYUDANTE que el SDK
            # pone encima, y ademas de los eventos crudos de la API emite los
            # suyos propios (uno por cada pedacito). text_stream esta hecho con
            # esos. Aqui los contamos pero NO los imprimimos: son cientos, y
            # taparian los 4 renglones que importan.
            tipo = "sdk:" + evento.type
            conteo[tipo] = conteo.get(tipo, 0) + 1
            primera_vez.setdefault(tipo, t)

    final = stream.get_final_message()

total = time.monotonic() - inicio

print(f"\n{'-' * 60}")
print("Cuando llego el primer pedazo de cada tipo (los 'sdk:' son los eventos")
print("de conveniencia que agrega el SDK, no vienen de la API):\n")
for tipo, cuando in sorted(primera_vez.items(), key=lambda x: x[1]):
    print(f"  {tipo:16} -> {cuando:5.2f}s   ({conteo[tipo]} pedazos en total)")

print(f"\n  total: {total:.1f}s")
print(f"  usage: {final.usage.input_tokens} in / {final.usage.output_tokens} out")
print(f"  bloques en la respuesta final: {[b.type for b in final.content]}")

if razonamiento:
    print(f"\n{'-' * 60}")
    print("Lo que estuvo razonando (resumen):\n")
    print("".join(razonamiento))