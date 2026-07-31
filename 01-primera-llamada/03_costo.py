"""
Nivel 1.3 — Cuanto cuesta esto realmente.

Compara el mismo trabajo en tres modelos e imprime el costo exacto en dolares.
Esta es la primera pieza de harness que escribes: medir el gasto.

Correr con:  python 03_costo.py
"""

from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
cliente = anthropic.Anthropic()


# Precios en dolares por MILLON de tokens. (input, output)
PRECIOS = {
    "claude-opus-5":   (5.00, 25.00),
    "claude-sonnet-5": (3.00, 15.00),
    "claude-haiku-4-5": (1.00, 5.00),
}


def costo_usd(modelo: str, tokens_entrada: int, tokens_salida: int) -> float:
    """Convierte tokens a dolares. Los precios son por millon, de ahi el 1_000_000."""
    precio_in, precio_out = PRECIOS[modelo]
    return (tokens_entrada / 1_000_000 * precio_in) + (tokens_salida / 1_000_000 * precio_out)


TAREA = "Clasifica este comentario como POSITIVO, NEGATIVO o NEUTRO. Responde solo con la palabra: 'El envio llego tarde pero el producto es excelente.'"

print(f"Tarea: clasificar un comentario\n")
print(f"{'modelo':<20} {'entrada':>8} {'salida':>8} {'costo':>12}   respuesta")
print("-" * 78)

total = 0.0
costos = {}          # guardamos el costo de cada modelo para comparar al final
for modelo in PRECIOS:
    respuesta = cliente.messages.create(
        model=modelo,
        max_tokens=256,          # tarea deliberadamente corta: una sola palabra
        messages=[{"role": "user", "content": TAREA}],
    )

    entrada = respuesta.usage.input_tokens
    salida = respuesta.usage.output_tokens
    precio = costo_usd(modelo, entrada, salida)
    total += precio
    costos[modelo] = precio

    texto = next((b.text for b in respuesta.content if b.type == "text"), "")
    # " ".join(texto.split()) aplasta saltos de linea y espacios dobles en uno solo,
    # para que una respuesta multilinea no rompa la tabla.
    limpio = " ".join(texto.split())
    print(f"{modelo:<20} {entrada:>8} {salida:>8} ${precio:>11.6f}   {limpio[:30]}")

print("-" * 78)
print(f"{'TOTAL de este script':<20} {'':>8} {'':>8} ${total:>11.6f}")

# NO escribimos "5x" a mano: lo calculamos con los numeros de ESTA corrida.
# Un numero fijo dentro del codigo miente en cuanto cambia la realidad.
caro = max(costos, key=costos.get)
barato = min(costos, key=costos.get)
veces = costos[caro] / costos[barato]

print(f"""
Lectura del resultado
---------------------
En esta corrida, {caro} costo {veces:.1f}x mas que {barato}
para la MISMA tarea trivial.

Ojo: la diferencia de precio POR TOKEN entre esos dos modelos es solo 5x.
El resto sale de que el modelo caro genero muchos mas tokens: en Opus 5 y
Sonnet 5 el razonamiento esta activado por defecto, y se cobra.

  costo real = precio por token  x  tokens generados

Por eso la decision de arquitectura mas rentable es usar el modelo mas barato
que resuelva bien CADA tarea, no el mas caro para todo.

Opus 5 se justifica cuando la tarea es dificil: razonar, escribir codigo, o
encadenar muchos pasos con herramientas (o sea: agentes, el nivel 3).
""")
