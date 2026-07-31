"""
Nivel 2.3 — Tres politicas para que el historial no te ahogue.

Compara cuanto pesa el mismo historial con tres estrategias distintas.
Casi todo el script es GRATIS: usa /v1/messages/count_tokens, que cuenta
tokens sin generar nada y no se cobra.

Correr con:  python 03_recortar.py
Cuesta:      menos de 1 centavo (solo la llamada que hace el resumen)
"""

from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
cliente = anthropic.Anthropic()

MODELO = "claude-haiku-4-5"
SYSTEM = "Eres un tutor de programacion. Explicas en espanol."

# Un historial ya vivido, de 8 turnos. Lo escribimos a mano para que el script
# corra rapido y siempre mida lo mismo.
#
# Fijate en el PRIMER turno: trae un dato que el modelo no puede adivinar
# (el taller de bicicletas). Ese dato es la prueba de fuego del final:
# si una estrategia lo borra, el modelo no tiene de donde sacarlo.
HISTORIAL = [
    {"role": "user", "content": "Hola. Me llamo Marta y estoy aprendiendo Python para automatizar el inventario de mi taller de bicicletas."},
    {"role": "assistant", "content": "Hola Marta. Buen objetivo: un inventario es perfecto para empezar. Preguntame lo que necesites."},
    {"role": "user", "content": "Que es una variable?"},
    {"role": "assistant", "content": "Una variable es una caja con nombre donde guardas un valor. En Python: edad = 30."},
    {"role": "user", "content": "Y una lista?"},
    {"role": "assistant", "content": "Una lista es una caja que guarda varios valores en orden: numeros = [1, 2, 3]."},
    {"role": "user", "content": "Como recorro una lista?"},
    {"role": "assistant", "content": "Con un for: 'for n in numeros:' ejecuta el bloque una vez por cada elemento."},
    {"role": "user", "content": "Que es un diccionario?"},
    {"role": "assistant", "content": "Un diccionario guarda pares clave-valor: persona = {'nombre': 'Ana', 'edad': 30}."},
    {"role": "user", "content": "Y una funcion?"},
    {"role": "assistant", "content": "Una funcion es un bloque de codigo con nombre que puedes reutilizar. Se define con def."},
    {"role": "user", "content": "Que hace return?"},
    {"role": "assistant", "content": "return devuelve un valor al lugar que llamo la funcion, y termina la funcion ahi mismo."},
    {"role": "user", "content": "Que es un error de sintaxis?"},
    {"role": "assistant", "content": "Es cuando Python no entiende como esta escrito el codigo: falta un parentesis, dos puntos, comillas."},
    {"role": "user", "content": "Como leo un mensaje de error?"},
    {"role": "assistant", "content": "De abajo hacia arriba: la ultima linea dice QUE fallo, y las de arriba DONDE."},
]

# Esta pregunta solo se puede responder con informacion del PRIMER turno.
# El modelo no la sabe: o esta en el historial, o no esta.
PREGUNTA_NUEVA = {"role": "user", "content": "Recuerdame: como me llamo y para que dije que queria aprender Python?"}


def contar(mensajes: list[dict]) -> int:
    """Cuenta los tokens de entrada SIN llamar al modelo. Esta operacion es gratis."""
    resultado = cliente.messages.count_tokens(
        model=MODELO,
        system=SYSTEM,
        messages=mensajes,
    )
    return resultado.input_tokens


def ventana_deslizante(historial: list[dict], ultimos: int) -> list[dict]:
    """Se queda solo con los ultimos N mensajes.

    Detalle importante: la API exige que el primer mensaje sea del usuario.
    Si el corte deja un 'assistant' al principio, lo descartamos.
    """
    recorte = historial[-ultimos:]
    while recorte and recorte[0]["role"] != "user":
        recorte = recorte[1:]
    return recorte


PRECIO_ENTRADA = 1.00 / 1_000_000    # Haiku 4.5, dolares por token
PRECIO_SALIDA = 5.00 / 1_000_000


def resumir(viejos: list[dict]) -> tuple[str, float]:
    """Pide al modelo un resumen de la parte antigua de la conversacion.

    Devuelve (texto, costo). El costo importa: resumir NO es gratis, y la
    tabla de comparacion no lo muestra por ningun lado.
    """
    transcripcion = "\n".join(f"{m['role']}: {m['content']}" for m in viejos)
    respuesta = cliente.messages.create(
        model=MODELO,
        max_tokens=300,
        messages=[{
            "role": "user",
            "content": (
                # Un buen prompt de resumen conserva los DATOS del usuario,
                # no solo los temas. Si solo pides temas, pierdes el nombre.
                "Resume esta conversacion en 4 lineas. Conserva cualquier dato "
                "concreto que haya dado el usuario (nombre, objetivo, contexto) "
                "y luego lista los temas explicados.\n\n" + transcripcion
            ),
        }],
    )
    texto = next((b.text for b in respuesta.content if b.type == "text"), "")
    costo = (respuesta.usage.input_tokens * PRECIO_ENTRADA
             + respuesta.usage.output_tokens * PRECIO_SALIDA)
    return texto, costo


# --- Estrategia 1: no recortar nada -----------------------------------------
completo = HISTORIAL + [PREGUNTA_NUEVA]
tokens_completo = contar(completo)

# --- Estrategia 2: ventana deslizante ---------------------------------------
recortado = ventana_deslizante(HISTORIAL, ultimos=4) + [PREGUNTA_NUEVA]
tokens_recortado = contar(recortado)

# --- Estrategia 3: resumen + los ultimos mensajes ----------------------------
viejos = HISTORIAL[:-4]
recientes = ventana_deslizante(HISTORIAL, ultimos=4)
resumen, costo_resumen = resumir(viejos)

# El resumen se mete como PRIMER turno de usuario, con una etiqueta que le
# aclara al modelo que es un resumen y no algo que el usuario dijo.
con_resumen = (
    [{"role": "user", "content": f"[Resumen de lo que ya hablamos]\n{resumen}"},
     {"role": "assistant", "content": "Entendido, tengo el contexto."}]
    + recientes
    + [PREGUNTA_NUEVA]
)
tokens_resumen = contar(con_resumen)

# --- Resultados --------------------------------------------------------------
print(f"{'estrategia':<28} {'mensajes':>9} {'tokens':>8} {'ahorro':>9}")
print("-" * 58)
for nombre, mensajes, tokens in [
    ("1. historial completo", completo, tokens_completo),
    ("2. ventana deslizante (4)", recortado, tokens_recortado),
    ("3. resumen + ultimos 4", con_resumen, tokens_resumen),
]:
    ahorro = (1 - tokens / tokens_completo) * 100
    print(f"{nombre:<28} {len(mensajes):>9} {tokens:>8} {ahorro:>8.0f}%")

# --- Lo que la tabla de arriba NO muestra ------------------------------------
# La estrategia 3 necesita una llamada extra para generar el resumen. Esa
# llamada no aparece en ninguna columna, asi que la tabla la hace parecer mas
# barata de lo que es. Aqui la medimos y calculamos cuando se paga sola.
ahorro_por_turno = (tokens_completo - tokens_resumen) * PRECIO_ENTRADA

print("\n" + "-" * 58)
print(f"Costo de generar el resumen (llamada extra): ${costo_resumen:.6f}")
print(f"Ahorro por turno frente al historial completo: ${ahorro_por_turno:.6f}")

if ahorro_por_turno > 0:
    turnos = costo_resumen / ahorro_por_turno
    print(f"=> El resumen se paga solo despues de ~{turnos:.0f} turnos.")
    print("   (Y es un techo: el historial completo sigue creciendo, asi que")
    print("    el ahorro real por turno tambien crece. En la practica se paga antes.)")
else:
    print("=> En esta corrida el resumen no ahorro nada. Historial demasiado corto.")

print("\nResumen que genero el modelo:")
print("  " + "\n  ".join(resumen.strip().splitlines()))

# La prueba de fuego: le preguntamos algo que solo estaba al PRINCIPIO.
print("\n" + "=" * 58)
print("Prueba: la pregunta pide un dato que SOLO existe en el turno 1")
print("(el nombre 'Marta' y el taller de bicicletas).")
print("Que responde cada version?\n")

for nombre, mensajes in [
    ("1. completo", completo),
    ("2. ventana deslizante", recortado),
    ("3. resumen + recientes", con_resumen),
]:
    r = cliente.messages.create(model=MODELO, max_tokens=150, system=SYSTEM, messages=mensajes)
    t = next((b.text for b in r.content if b.type == "text"), "")
    print(f"{nombre}:\n  {' '.join(t.split())[:160]}\n")

print("""
Lectura del resultado
---------------------
No hay una estrategia "correcta": hay un intercambio.

  completo    -> recuerda todo, pero el costo crece sin freno y un dia revienta
  ventana     -> el mas barato, pero OLVIDA (mira la respuesta 2: no sabe
                 quien es Marta, porque ese turno ya no se le manda)
  resumen     -> mas caro que la ventana pero recuerda lo importante

Ojo con la columna 'ahorro', que engana: aqui el resumen ahorra MENOS que la
ventana. Es logico, la conversacion es cortita: el resumen mide casi lo mismo
que lo que resume. La ventaja del resumen aparece cuando el historial es
largo, porque su tamano se queda mas o menos fijo mientras el historial
completo sigue creciendo. Con 8 turnos no se nota; con 80 es la diferencia
entre funcionar y no funcionar.

Y ojo con la columna 'ahorro' por segunda vez: no incluye lo que costo GENERAR
el resumen. Ese numero esta medido arriba, junto con los turnos que tarda en
pagarse solo. Pagas tokens hoy para no pagar la conversacion entera manana.

Elegir entre estas tres ES trabajo de harness. El modelo no participa en la
decision: tu codigo decide que se le manda y que no.

Claude Code, ChatGPT y cualquier agente largo hacen la version 3 automatica.
Cuando ves 'compactando conversacion', es exactamente esto.
""")
