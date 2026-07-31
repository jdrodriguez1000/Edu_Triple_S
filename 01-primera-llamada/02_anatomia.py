"""
Nivel 1.2 — Anatomia de una llamada: los 5 parametros que controlan todo.

Este script hace UNA llamada y luego te muestra, pieza por pieza, que fue lo que
enviaste y que fue lo que recibiste.

Correr con:  python 02_anatomia.py
"""

import os
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
cliente = anthropic.Anthropic()


# ---------------------------------------------------------------------------
# 1. SYSTEM PROMPT — quien es el modelo y como debe comportarse.
#    No es un mensaje del usuario. Es la configuracion de la personalidad y las
#    reglas. Es lo primero que se procesa y aplica a TODA la conversacion.
# ---------------------------------------------------------------------------
SYSTEM = """Eres un profesor de programacion para principiantes.
 Reglas:
 - Explicas con analogias del mundo real antes de usar terminos tecnicos.
 - Maximo 4 frases por respuesta.
 - Nunca asumes que la persona ya sabe ingles tecnico."""


# ---------------------------------------------------------------------------
# 2. MESSAGES — la conversacion. Una lista, en orden, de turnos.
#    Solo hay dos roles que tu escribes: "user" y "assistant".
#    La API es SIN MEMORIA: si no mandas el historial completo, no existe.
# ---------------------------------------------------------------------------
MENSAJES = [
    {"role": "user", "content": "Que es una variable?"},
    {"role": "assistant", "content": "Una variable es como una caja con etiqueta: guardas algo adentro y despues lo pides por el nombre de la etiqueta."},
    {"role": "user", "content": "Y una funcion?"},   # <- esta es la pregunta real
]
# Fijate que le "recordamos" a Claude su propia respuesta anterior.
# Ese turno 'assistant' lo escribimos NOSOTROS. El modelo no lo recordaba.


respuesta = cliente.messages.create(
    # 3. MODEL — que cerebro usar. Cambia calidad, velocidad y precio.
    model="claude-opus-5",

    # 4. MAX_TOKENS — techo duro de cuanto puede generar. Si lo alcanza, corta
    #    a mitad de frase y stop_reason sera "max_tokens".
    max_tokens=2048,

    # 5. THINKING — razonamiento interno antes de responder. En Opus 5 esta
    #    activo por defecto. "summarized" nos deja ver un resumen de ese
    #    razonamiento; sin esto, el bloque llega vacio.
    thinking={"type": "adaptive", "display": "summarized"},

    system=SYSTEM,
    messages=MENSAJES,
)


# ---------------------------------------------------------------------------
# LA RESPUESTA, desarmada
# ---------------------------------------------------------------------------
print("=" * 70)
print("BLOQUES DE CONTENIDO")
print("=" * 70)
for i, bloque in enumerate(respuesta.content):
    print(f"\n[bloque {i}] tipo = {bloque.type}")
    if bloque.type == "thinking":
        print(f"  (razonamiento interno)\n  {bloque.thinking[:400]}")
    elif bloque.type == "text":
        print(f"  (lo que ve el usuario)\n  {bloque.text}")

print("\n" + "=" * 70)
print("METADATOS")
print("=" * 70)
print(f"  modelo real usado : {respuesta.model}")
print(f"  stop_reason       : {respuesta.stop_reason}")
print(f"  tokens entrada    : {respuesta.usage.input_tokens}")
print(f"  tokens salida     : {respuesta.usage.output_tokens}")

# stop_reason te dice POR QUE se detuvo. En un harness de verdad, siempre
# se revisa antes de leer el contenido:
#   end_turn   -> termino normal
#   max_tokens -> se quedo sin espacio, la respuesta esta cortada
#   tool_use   -> quiere que ejecutes una herramienta  (nivel 3)
#   refusal    -> se nego por seguridad, content puede venir vacio
