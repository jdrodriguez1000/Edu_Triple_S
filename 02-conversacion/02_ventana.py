"""
Nivel 2.2 — La ventana de contexto se llena, y la factura crece sola.

Simula una conversacion de 6 turnos y mide, turno por turno, cuantos tokens
de ENTRADA se pagan. Los mensajes son todos igual de cortos: lo unico que
crece es el historial.

Correr con:  python 02_ventana.py
Cuesta:      menos de 1 centavo (usa Haiku)
"""

from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
cliente = anthropic.Anthropic()

MODELO = "claude-haiku-4-5"
PRECIO_ENTRADA = 1.00 / 1_000_000   # dolares por token de entrada, Haiku 4.5
PRECIO_SALIDA = 5.00 / 1_000_000

SYSTEM = "Eres un guia de viajes. Responde en 2 frases como maximo."

# Seis preguntas cortas, todas de largo parecido. Ninguna depende de otra:
# el crecimiento que veras NO viene de las preguntas, viene del historial.
PREGUNTAS = [
    "Recomiendame una ciudad para visitar en Colombia.",
    "Que se come alli?",
    "Cuanto cuesta una noche de hotel?",
    "Que clima hace en julio?",
    "Como llego desde Bogota?",
    "Que llevo en la maleta?",
]

historial = []
acumulado_entrada = 0
acumulado_costo = 0.0

print(f"{'turno':>5} {'entrada':>9} {'salida':>8} {'costo turno':>13} {'acumulado':>12}")
print("-" * 52)

for numero, pregunta in enumerate(PREGUNTAS, start=1):
    historial.append({"role": "user", "content": pregunta})

    respuesta = cliente.messages.create(
        model=MODELO,
        max_tokens=256,
        system=SYSTEM,
        messages=historial,
    )

    texto = next((b.text for b in respuesta.content if b.type == "text"), "")
    historial.append({"role": "assistant", "content": texto})

    entrada = respuesta.usage.input_tokens
    salida = respuesta.usage.output_tokens
    costo = entrada * PRECIO_ENTRADA + salida * PRECIO_SALIDA

    acumulado_entrada += entrada
    acumulado_costo += costo

    print(f"{numero:>5} {entrada:>9} {salida:>8} ${costo:>12.6f} ${acumulado_costo:>11.6f}")

print("-" * 52)
print(f"Tokens de ENTRADA pagados en total: {acumulado_entrada}")
print(f"Costo total: ${acumulado_costo:.6f}")

# La comparacion que importa: cuanto habria costado la entrada si cada
# pregunta se hubiera mandado sola, sin historial (o sea, sin memoria).
print(f"""
Lectura del resultado
---------------------
Tus 6 preguntas eran igual de cortas. Aun asi la columna 'entrada' subio en
cada turno, porque cada llamada reenvia toda la conversacion anterior.

  turno 1 paga:  pregunta 1
  turno 2 paga:  pregunta 1 + respuesta 1 + pregunta 2
  turno 3 paga:  pregunta 1 + respuesta 1 + pregunta 2 + respuesta 2 + pregunta 3
  ...

De que tamano es cada escalon? Del tamano de la respuesta anterior. Y como
este SYSTEM pide "maximo 2 frases", las respuestas salen todas parecidas y los
escalones quedan mas o menos IGUALES: la entrada por turno crece en linea recta.

Quita ese limite de 2 frases y cambia la forma: si Claude se va alargando turno
a turno, cada escalon es mas alto que el anterior y la entrada se dispara.

Pase lo que pase con la forma, el ACUMULADO siempre crece mas rapido que los
turnos, porque cada turno paga por todos los anteriores. En una conversacion
de 100 turnos, el turno 100 paga por los 99 previos.

Y hay un efecto que se ve mejor comparando dos corridas: cada token que Claude
genera hoy se vuelve a pagar en TODOS los turnos siguientes. En 6 turnos,
27 tokens de salida de mas costaron 145 tokens de entrada de mas (~5x).
Por eso pedir respuestas cortas en el SYSTEM no ahorra una vez: ahorra siempre.

Y hay un segundo limite, mas duro que el dinero: la ventana de contexto.
{MODELO} aguanta 200.000 tokens de entrada. Cuando el historial los pasa, la
API ya no responde: falla.

Por eso todo agente serio necesita una politica para recortar el historial.
Eso es lo que hace el script 3.
""")
