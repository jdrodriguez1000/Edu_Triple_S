"""
Nivel 2.1 — El chat que recuerda.

Este es tu primer harness de verdad: un bucle que administra el historial.
El modelo sigue sin memoria. La memoria la pones TU, en una lista de Python.

Correr con:  python 01_chat.py
Salir con:   salir   (o Ctrl+C)
"""

from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
cliente = anthropic.Anthropic()

# Usamos Haiku a proposito: un chat reenvia TODO el historial en cada turno,
# asi que es el lugar donde el modelo caro sale mas caro. Puedes cambiarlo a
# "claude-opus-5" cuando quieras comparar la calidad de las respuestas.
MODELO = "claude-haiku-4-5"

SYSTEM = "Eres un tutor de programacion. Explicas en espanol, claro y en pocas frases."

# ---------------------------------------------------------------------------
# EL HISTORIAL. Esta lista ES la memoria del chat.
# Empieza vacia. Crece de a dos elementos por turno: lo que dices tu, y lo
# que responde Claude. En cada llamada la mandamos ENTERA.
# ---------------------------------------------------------------------------
historial = []

print("Chat con memoria. Escribe 'salir' para terminar.\n")

gasto_total_tokens = 0

# Contamos los turnos con una variable propia.
# ANTES este contador era len(historial) // 2, y estaba MAL: daba por hecho que
# cada turno mete 2 mensajes al historial. En cuanto haces el ejercicio 1 (dejar
# de guardar las respuestas) entra 1 por turno, y el contador imprimia 0, 1, 1, 2.
# Regla: si quieres contar turnos, cuenta turnos. No los deduzcas de la forma
# de una estructura que puede cambiar.
turno = 0

while True:
    entrada = input("Tu:  ").strip()

    if entrada.lower() in ("salir", "exit", "quit"):
        break
    if not entrada:
        continue

    turno += 1

    # 1. Tu mensaje entra al historial.
    historial.append({"role": "user", "content": entrada})

    # 2. Mandamos el historial COMPLETO. No hay forma de mandar "solo lo nuevo".
    respuesta = cliente.messages.create(
        model=MODELO,
        max_tokens=1024,
        system=SYSTEM,
        messages=historial,
    )

    # 3. Sacamos el texto filtrando por tipo (L0.7: nunca content[0]).
    texto = next((b.text for b in respuesta.content if b.type == "text"), "")

    # 4. La respuesta de Claude TAMBIEN entra al historial.
    #    OJO, aqui yo habia escrito que si te saltas este paso "cada turno
    #    empieza de cero". Es FALSO, y se comprobo corriendolo: tus mensajes
    #    siguen entrando en el paso 1, asi que Claude recuerda todo lo que TU
    #    dijiste y nada de lo que dijo EL. Ver el ejercicio 1 del README.
    historial.append({"role": "assistant", "content": texto})

    entrada_tok = respuesta.usage.input_tokens
    salida_tok = respuesta.usage.output_tokens
    gasto_total_tokens += entrada_tok + salida_tok

    print(f"\nClaude: {texto}\n")
    print(
        f"   [turno {turno} | "
        f"entrada {entrada_tok} tok | salida {salida_tok} tok | "
        f"historial: {len(historial)} mensajes]\n"
    )

print(f"\nFin. Mensajes en el historial: {len(historial)}")
print(f"Tokens gastados en toda la sesion: {gasto_total_tokens}")
print("\nMira la columna 'entrada': crecio en cada turno aunque tus mensajes")
print("fueran igual de cortos. Eso es la ventana de contexto llenandose.")
