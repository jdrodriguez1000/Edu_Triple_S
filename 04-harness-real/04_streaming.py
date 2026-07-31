"""
Nivel 4.4 — Streaming: que el usuario no mire una pantalla quieta.

Hasta ahora cada llamada era: mandas, esperas callado, aparece todo de golpe.
Con una respuesta larga, esa espera son 20 o 30 segundos de nada. El usuario
no sabe si el programa esta pensando o si se colgo.

Streaming es pedir la respuesta por pedacitos, segun se van generando. No es
mas rapido en total — es mas rapido en EMPEZAR, que es lo que se siente.

Y ademas es obligatorio para respuestas grandes: el error 3 del script 1
(ValueError, 'Streaming is required...') era exactamente esto.

Medimos dos cosas en las dos formas:
  - cuanto tarda en aparecer la PRIMERA palabra
  - cuanto tarda en estar TODO

Correr con:  python 04_streaming.py
Cuesta:      ~$0.02 (dos respuestas largas)
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


# ---------------------------------------------------------------------------
# FORMA 1 — sin streaming. Lo que veniamos haciendo.
# ---------------------------------------------------------------------------
print("=== Sin streaming (esperando en silencio...)")
inicio = time.monotonic()

respuesta = cliente.messages.create(
    model=MODELO,
    max_tokens=1000,
    messages=[{"role": "user", "content": PREGUNTA}],
)

total_sin = time.monotonic() - inicio
texto = next((b.text for b in respuesta.content if b.type == "text"), "")
print(texto)
print(f"\n  primera palabra a los {total_sin:.1f}s | todo a los {total_sin:.1f}s")
print(f"  usage: {respuesta.usage.input_tokens} in / {respuesta.usage.output_tokens} out")



# ---------------------------------------------------------------------------
# FORMA 2 — con streaming.
#
# 'with' porque la conexion queda abierta mientras llegan los pedazos, y hay
# que cerrarla al final. El with lo hace solo, incluso si algo revienta.
#
# stream.text_stream va soltando trocitos de texto. end="" para que no salte
# de linea, flush=True para que aparezca YA y no se quede en el buffer.
# ---------------------------------------------------------------------------
print("\n\n=== Con streaming (mira como va apareciendo)")
inicio = time.monotonic()
primera = None
ejer
with cliente.messages.stream(
    model=MODELO,
    max_tokens=1000,
    messages=[{"role": "user", "content": PREGUNTA}],
) as stream:
    for trozo in stream.text_stream:
        if primera is None:
            primera = time.monotonic() - inicio
        print(trozo, end="", flush=True)

    # Al terminar el bucle, el SDK ya junto todos los pedazos por ti.
    # get_final_message() te devuelve el mismo objeto de siempre, con usage
    # y stop_reason. No pierdes nada por hacer streaming.
    final = stream.get_final_message()

total_con = time.monotonic() - inicio
print(f"\n\n  primera palabra a los {primera:.1f}s | todo a los {total_con:.1f}s")
print(f"  usage: {final.usage.input_tokens} in / {final.usage.output_tokens} out")


print(f"""

Lectura del resultado
---------------------
  sin streaming: primera palabra a los {total_sin:.1f}s
  con streaming: primera palabra a los {primera:.1f}s

El total se parece en las dos. Lo que cambia es la espera EN BLANCO. Esa
diferencia es la que separa un programa que parece vivo de uno que parece
colgado. No es un truco de velocidad: es un truco de percepcion, y cuenta.

Tres cosas que no se ven en los numeros:

1. get_final_message() te devuelve el objeto Message completo, igual que
   messages.create(). Los tokens, el stop_reason, el content: todo esta.
   Hacer streaming no te quita informacion.

2. Para respuestas grandes no es opcional. El SDK se niega a hacer una
   peticion sin streaming que calcule que va a tardar mas de 10 minutos
   (ese fue el ValueError del script 1). Con streaming la conexion recibe
   datos todo el rato y no se muere de aburrimiento.

3. Un stream se puede cortar a la mitad: se cae la red y te quedas con media
   respuesta y ningun error claro. Ganas la sensacion de rapidez y pagas con
   un caso mas que manejar. Todo en el harness es un intercambio.
""")
