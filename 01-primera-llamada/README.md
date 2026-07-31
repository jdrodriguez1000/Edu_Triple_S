# Nivel 1 — Tu primera llamada

Objetivo: entender qué es exactamente una llamada a un LLM, porque **todo agente
del mundo es una pila de estas llamadas**. Sin esto claro, los niveles siguientes
son magia.

Antes de empezar, activa el entorno (desde la raíz):

```powershell
.\.venv\Scripts\Activate.ps1
cd 01-primera-llamada
```

---

## 1.1 — El programa mínimo

```powershell
python 01_hola_claude.py
```

Son 15 líneas reales. Fíjate en tres cosas:

**a) El cliente no recibe la key.** `anthropic.Anthropic()` va vacío: el SDK la busca
solo en la variable de entorno. Así la key nunca aparece en tu código.

**b) `content` es una lista, no un string.** Esto sorprende a todo el mundo:

```python
respuesta.content        # ❌ no es texto
respuesta.content[0].text  # ⚠️ funciona a veces, y por eso es peligroso
```

La respuesta viene en **bloques**, y puede haber bloques de razonamiento antes del
texto. Si asumes que el bloque 0 es texto, tu código se rompe el día que el modelo
piense antes de responder. La forma correcta siempre es filtrar por tipo:

```python
for bloque in respuesta.content:
    if bloque.type == "text":
        print(bloque.text)
```

**c) `usage` te dice cuánto gastaste.** Cada respuesta trae la cuenta exacta.

---

## 1.2 — Anatomía: los 5 parámetros

```powershell
python 02_anatomia.py
```

| Parámetro | Qué controla |
|---|---|
| `model` | Qué cerebro. Calidad ↔ velocidad ↔ precio |
| `system` | Quién es y qué reglas sigue. Configuración, no conversación |
| `messages` | La conversación completa, en orden |
| `max_tokens` | Techo duro de generación. Si lo topa, **corta a mitad de frase** |
| `thinking` | Razonamiento interno antes de responder |

### El concepto más importante del nivel: **la API no tiene memoria**

Cada llamada es independiente y amnésica. Claude no recuerda la llamada anterior.

Cuando conversas con un chatbot y "te recuerda", es porque **el programa le está
reenviando toda la conversación completa en cada mensaje**. Míralo en el script:

```python
MENSAJES = [
    {"role": "user",      "content": "Que es una variable?"},
    {"role": "assistant", "content": "Una variable es como una caja..."},  # ← lo escribimos NOSOTROS
    {"role": "user",      "content": "Y una funcion?"},
]
```

Ese turno `assistant` lo pusimos a mano. Al modelo le llega como si él lo hubiera
dicho, y por eso responde en el mismo estilo y entiende que "y una función?" sigue
el mismo hilo.

**La memoria es una función del harness, no del modelo.** Esa es la primera pieza
de harness que vas a construir, en el nivel 2.

### `stop_reason`: por qué se detuvo

Un harness serio **siempre** lo revisa antes de leer el contenido:

| Valor | Significa | Qué haces |
|---|---|---|
| `end_turn` | Terminó normal | Todo bien |
| `max_tokens` | Se quedó sin espacio | La respuesta está **cortada** — sube `max_tokens` |
| `tool_use` | Quiere ejecutar una herramienta | Ejecutas y le devuelves el resultado (nivel 3) |
| `refusal` | Se negó por seguridad | `content` puede venir vacío — no indexes a ciegas |

---

## 1.3 — El costo real

```powershell
python 03_costo.py
```

Hace la misma tarea en Opus, Sonnet y Haiku, e imprime el costo exacto de cada una.

Dos reglas que salen de ahí:

1. **Los tokens de salida cuestan ~5x más que los de entrada.** Mandar mucho contexto
   es barato; generar mucho texto no.
2. **Usa el modelo más barato que resuelva bien cada tarea.** Clasificar un comentario
   con Opus 5 es pagar 5x de más por el mismo resultado. Opus se justifica cuando la
   tarea es difícil: razonar, escribir código, encadenar herramientas.

---

## Ejercicios (haz al menos 2 antes de seguir)

1. En `01_hola_claude.py`, cambia `max_tokens` a `30` y corre. Mira cómo la respuesta
   se corta y `stop_reason` pasa a `max_tokens`.
2. En `02_anatomia.py`, cambia el `SYSTEM` para que responda como pirata. Observa que
   no tuviste que tocar los mensajes.
3. En `02_anatomia.py`, borra el turno `assistant` de la lista. ¿Cambia la respuesta a
   "Y una función?" Eso es la falta de memoria en acción.
4. En `03_costo.py`, cambia `TAREA` por algo que exija razonar de verdad (por ejemplo:
   "Un tren sale a las 14:20 y tarda 3h 50min, ¿a qué hora llega?"). Sube `max_tokens`
   a 2048 y compara si los tres modelos siguen acertando.

---

## Lo que ya sabes

- Una llamada = `model` + `system` + `messages` + `max_tokens`
- La respuesta son **bloques**, no texto
- La API **no tiene memoria**: el historial lo administras tú
- `stop_reason` y `usage` son los dos datos que todo harness vigila

**Siguiente:** nivel 2 — convertir esto en un chat real que recuerda, y descubrir el
primer problema serio de los agentes: la ventana de contexto se llena.
