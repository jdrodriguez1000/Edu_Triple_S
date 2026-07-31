# GUIDE.md — Guía de trabajo

> El **manual** del curso. Aquí va el *cómo*: comandos, rutas, errores comunes y
> plantillas para copiar.
>
> Este archivo **se corrige**. Si un comando cambia, se reemplaza — un comando
> desactualizado es peor que ninguno.
>
> ¿Buscas el *por qué* de las cosas? Eso está en `LESSONS.md`.

---

## 1. Arrancar una sesión de trabajo

Los dos comandos de siempre. Desde la raíz del proyecto:

```powershell
cd C:\Users\USUARIO\Documents\Company_TripleS\Edu_TripleS
.\.venv\Scripts\Activate.ps1
```

**Sabes que funcionó** porque tu prompt cambia a `(.venv) PS C:\...`.

> Hay que hacerlo en **cada terminal nueva**. Es lo que más se olvida.

Luego entras al nivel en el que vas:

```powershell
cd 01-primera-llamada
python 01_hola_claude.py
```

---

## 2. Mapa de archivos de la raíz

| Archivo | Qué es | ¿Se sube a Git? |
|---|---|---|
| `README.md` | El mapa de los 9 niveles | Sí |
| `CLAUDE.md` | Instrucciones permanentes para Claude | Sí |
| `PROGRESO.md` | Bitácora: dónde vas, dudas, errores | Sí |
| `LESSONS.md` | Lecciones aprendidas (el *por qué*) | Sí |
| `GUIDE.md` | Esta guía (el *cómo*) | Sí |
| `requirements.txt` | Lista de librerías del proyecto | Sí |
| `.env.example` | Plantilla de la llave, **sin** la llave | Sí |
| `.env` | **Tu llave real** | ❌ **NUNCA** |
| `.venv/` | Las librerías instaladas | ❌ Nunca |
| `memoria.json` | Lo que tu agente recuerda de una persona | ❌ **Nunca** (nivel 6b) |
| `memoria_de_prueba.json` | Basura del eval. Se borra solo, salvo si el eval revienta | ❌ Nunca |

Regla: `.venv` y `.env` son **compartidos** y viven en la raíz. No se crea uno por nivel.

⚠️ **Git no olvida.** Borrar un archivo después **no lo borra del historial**.
Por eso lo que nunca debe subir se decide **antes** del primer commit, no después:
llaves, datos de usuarios y cualquier memoria persistente.

---

## 3. Errores comunes y cómo salir de ellos

| Lo que ves | Qué pasó | Solución |
|---|---|---|
| `ModuleNotFoundError: anthropic` | No activaste el entorno virtual | `.\.venv\Scripts\Activate.ps1` |
| `execution policy` al activar | PowerShell bloquea scripts | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` (una sola vez) |
| `AuthenticationError` | La llave está mal copiada | Vuelve a pegarla completa, sin espacios |
| `PermissionDeniedError` | No hay saldo | Carga crédito en console.anthropic.com |
| `APIConnectionError` | Sin conexión | Revisa internet, VPN o firewall |
| `ANTHROPIC_API_KEY esta vacia` | El `.env` tiene el texto de ejemplo | Reemplázalo por tu llave real |
| La respuesta se corta a mitad | `max_tokens` muy bajo | Súbelo y revisa `stop_reason` |
| `UnicodeEncodeError: 'charmap' codec...` | La consola de Windows es `cp1252` y Claude respondió con `°`, tildes o emojis. **El programa funcionó; falló el `print`.** | `sys.stdout.reconfigure(encoding="utf-8")` al inicio del script |
| `tool_use_id ... not found` | El id del `tool_result` no coincide con el del `tool_use` | Copia `bloque.id` tal cual, no lo inventes |
| La API rechaza el mensaje después de una herramienta | Guardaste solo el texto en vez de `respuesta.content` entero | Al usar `tools`, guarda siempre `{"role": "assistant", "content": respuesta.content}` |
| `ValueError: Streaming is required for operations...` | `max_tokens` tan alto que el SDK calcula más de 10 min. **La petición nunca salió de tu máquina** | Baja `max_tokens`, o usa `cliente.messages.stream(...)` |
| `BadRequestError: 'temperature' is deprecated for this model` | Parámetro que existía en modelos viejos y en Opus 5 ya no (`temperature`, `top_p`, `top_k`, `budget_tokens`) | Quítalo. Se guía con el `SYSTEM`, no con parámetros |
| El programa se cuelga varios minutos y luego falla | El `timeout` es **por intento** y el SDK reintenta. Por defecto: 10 min × 3 = media hora | Pon `timeout=30.0` y `max_retries` explícitos al crear el cliente |
| Un `create()` gastó el triple de lo esperado | Tus reintentos × los del SDK (2 por defecto) se **multiplican** | Si pones reintentos propios, crea el cliente con `max_retries=0` |
| Un dato sale cortado, ilegible o en mitad de un `{` | Casi siempre lo cortó **tu propio `print`**, no el modelo ni el servidor. Ya pasó 3 veces en el curso: `texto.strip()[:30]`, la fila "cortada" de Sonnet, y `e.message[:80]` | Antes de sospechar de la API, mira qué le hace tu código al dato. Para errores, usa `e.body` (ver §3.b) |

---

## 4. Plantilla: script nuevo del curso

Todo script de este repo empieza igual. Copia esto:

```python
"""
Nivel N — Para qué sirve este script, en una línea.
"""
import os
from pathlib import Path

from dotenv import load_dotenv
import anthropic

# El .env vive en la raíz, una carpeta arriba de este archivo.
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

cliente = anthropic.Anthropic()   # lee ANTHROPIC_API_KEY del entorno solo

respuesta = cliente.messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hola"}],
)

# La respuesta son BLOQUES: filtra por tipo, nunca asumas [0].
for bloque in respuesta.content:
    if bloque.type == "text":
        print(bloque.text)

# Un harness siempre vigila estos dos datos.
print(f"stop_reason: {respuesta.stop_reason}")
print(f"tokens: {respuesta.usage.input_tokens} in / {respuesta.usage.output_tokens} out")
```

---

## 4.b Plantilla: el bucle agéntico

El esqueleto mínimo de cualquier agente. Cambia `HERRAMIENTAS` y `FUNCIONES` y
tienes otro agente; el bucle no se toca.

```python
HERRAMIENTAS = [{                      # lo que VE el modelo (una descripción)
    "name": "mi_tool",
    "description": "Qué hace y CUÁNDO usarla. Este campo decide el comportamiento.",
    "input_schema": {
        "type": "object",
        "properties": {"arg": {"type": "string", "description": "..."}},
        "required": ["arg"],
    },
}]
FUNCIONES = {"mi_tool": mi_funcion_python}   # el puente nombre -> función real

historial = [{"role": "user", "content": pregunta}]

for vuelta in range(6):                      # SIEMPRE un tope de vueltas
    r = cliente.messages.create(
        model="claude-opus-5", max_tokens=2048,
        tools=HERRAMIENTAS, messages=historial,
    )
    if r.stop_reason != "tool_use":           # terminó
        break

    historial.append({"role": "assistant", "content": r.content})   # ENTERO

    resultados = []
    for b in r.content:                       # puede pedir VARIAS a la vez
        if b.type == "tool_use":
            resultados.append({
                "type": "tool_result",
                "tool_use_id": b.id,          # el id, tal cual
                # Si tu función devuelve un DICT, aquí va json.dumps (regla 5).
                "content": FUNCIONES[b.name](**b.input),
            })
    historial.append({"role": "user", "content": resultados})  # todos en UNO
```

Las cinco reglas que rompen el programa si las ignoras:

1. Guarda `r.content` **entero**, no solo el texto.
2. El `tool_use_id` debe ser **idéntico** al del `tool_use`.
3. El resultado va con `role: "user"` (todo lo que *entra* al modelo es user).
4. **Todos** los resultados de una vuelta van en **un solo** mensaje.
5. **`content` tiene que ser TEXTO.** Si tu herramienta devuelve un
   diccionario, va `json.dumps(salida, ensure_ascii=False)`. Sin eso, la API
   rechaza el mensaje.
   Y el `ensure_ascii=False` no es cosmético: sin él `"día"` viaja como
   `"día"` — más caracteres, más tokens, y para nada.

Y dos de sentido común: la función siempre `return "Error: ..."` en vez de
lanzar excepciones, y siempre un tope de vueltas.

⚠️ **Estas dos líneas confían en el modelo, y ninguna plantilla lo dice:**

```python
FUNCIONES[b.name]        # nombre inventado  -> KeyError
funcion(**b.input)       # argumento que no existe -> TypeError
```

Reventar **ahí** tumba el bucle entero, aunque cada función esté blindada por
dentro. El `try` va en el harness: ver §4.c.

---

## 4.c Los diez frenos del harness

El bucle de §4.b es el motor. Esto son los frenos. Vienen de tres sitios y
protegen de cosas distintas:

| # | Freno | Te protege de |
|---|---|---|
| 1–6 | timeout+reintentos · errores tipados · presupuesto · tope de vueltas · permisos · registro | **el mundo** y **tu cuenta de cobro** |
| 7–9 | ¿existe la herramienta? · ¿acepta esos argumentos? · la red final | **el modelo** |
| 10 | ¿ese modelo existe en tu catálogo? | **ti mismo** |

Los frenos 7–9 solo aparecen cuando el agente tiene **varias** herramientas: con
una sola, que el modelo invente un nombre es casi imposible.
→ **Más herramientas no es solo más capacidad: es más formas de equivocarse.**

El 10 apareció al meter varios modelos en una tabla: `MODELO` se valida contra
el catálogo **antes de gastar un centavo**. Sin él, un nombre mal escrito
revienta con un `KeyError` feo o —peor— llega a la API para que te conteste un
**404** después de armar la petición.
→ **Misma familia del 7 y el 8 —no confíes en un nombre solo porque alguien lo
escribió— salvo que aquí el que escribe eres tú, no el modelo.**

Ejemplos corriendo: los 6 primeros en `04-harness-real/03_harness.py`, los diez
en `05b-proyecto/agente.py`.

### 1 y 2 — Timeout y reintentos (se eligen juntos)

```python
cliente = anthropic.Anthropic(
    timeout=30.0,      # POR INTENTO, no en total
    max_retries=0,     # apagado porque el reintento propio está más abajo
)
```

Valores de fábrica: `timeout=600` (10 min) y `max_retries=2`. Peor caso real =
`timeout × (max_retries + 1)`. Con los de fábrica: media hora colgado.

### 3 — Reintentar solo lo temporal

```python
REINTENTABLES = (
    anthropic.RateLimitError,        # 429
    anthropic.InternalServerError,   # 5xx
    anthropic.APIConnectionError,    # red (incluye APITimeoutError)
)
```

Todo lo demás (`AuthenticationError`, `NotFoundError`, `BadRequestError`) es
permanente: cortar de inmediato. La espera crece — 2 s, 4 s, 8 s — más un
número al azar (*jitter*).

**Clasifica por clase, nunca por el texto del mensaje.** Los mensajes son de
calidad desigual: un 404 dice solo `model: claude-opus-9-mil` (repite lo que
mandaste), un 400 dice `` `temperature` is deprecated for this model `` (te dice
qué hacer). Y el proveedor los cambia sin avisar. La clase, no.

**El caso general atrapa hijos que no conoces.** `APITimeoutError` hereda de
`APIConnectionError`, por eso la tupla de arriba no lo lista y aun así lo cubre.
Medido: el mismo script lanza `APIConnectionError` cuando el dominio no existe y
`APITimeoutError` cuando la dirección no responde. Los dos se reintentan.

### 3.b — Leer el mensaje limpio de un error

`e.message` trae el JSON crudo entero. Cortarlo con `[:80]` parte el JSON justo
antes del dato útil. El SDK ya te lo dio parseado en **`e.body`**:

```python
def motivo(e) -> str:
    cuerpo = getattr(e, "body", None)   # APIConnectionError no tiene body
    if isinstance(cuerpo, dict):
        texto = cuerpo.get("error", {}).get("message", "")
        pedido = cuerpo.get("request_id")
        if texto:
            return texto + (f"  [request_id: {pedido}]" if pedido else "")
    return e.message
```

El **`request_id`** (`req_011CdV34h8bX...`) es el número que le das a soporte de
Anthropic para que encuentren tu petición exacta. Regístralo cuando falle algo.

### 4 — Presupuesto y tope de vueltas (se revisan ANTES)

```python
if gastado_usd >= PRESUPUESTO_USD:      # antes de llamar, no después
    raise PresupuestoAgotado(...)

costo = (u.input_tokens * 5.00 + u.output_tokens * 25.00) / 1_000_000  # opus-5
```

⚠️ **Recalcula el presupuesto para CADA agente. No lo copies del anterior.**
`PRESUPUESTO_USD = 0.10` servía para el agente del nivel 4 (3 herramientas). El
del 5b tiene 6, y su menú pesa 3.447 tokens **que se repagan en cada vuelta**:
la misma corrida de 3 preguntas costó **$0.1496**. Ese 0.10 copiado la habría
cortado a mitad de la tercera pregunta, y el síntoma —"el agente se detuvo
solo"— no se parece en nada a la causa.
→ **Un límite heredado sin recalcular no es un freno: es una trampa.**
Estímalo antes de correr: `vueltas × tokens_de_entrada × precio`.

### 5 — Permisos (en tu código, no en el prompt)

```python
PERMISOS = {"obtener_clima": "permitir", "borrar_archivo": "preguntar"}
politica = PERMISOS.get(nombre, "prohibir")   # lo desconocido se prohíbe
```

Y si niegas, **díselo al modelo**:

```python
resultado = f"PERMISO DENEGADO: el usuario no autorizo {bloque.name}."
```

Con silencio, el modelo cree que se hizo y le dice al usuario que ya lo hizo.

Dos principios que se llevan a cualquier otro sitio (no solo a agentes):

- **Denegar por defecto.** El `.get(nombre, "prohibir")` hace que una herramienta
  nueva sin política **no corra**. Diseña para que el olvido falle hacia el lado
  seguro: lista lo permitido, nunca lo prohibido (esa lista siempre queda corta).
- **Dos candados para la misma puerta.** Además del permiso, la herramienta se
  defiende sola (`borrar_archivo` comprueba que el archivo esté dentro de
  `caja/`). El permiso lo puede dar un humano distraído.

**Con varias herramientas, dos respuestas no bastan: van tres.**

```python
[s] sí, esta vez  ·  [t] sí, toda la corrida  ·  [n] no
```

La `t` no es comodidad, es seguridad. Preguntar lo mismo cinco veces hace que el
usuario diga que sí **por reflejo**, sin leer — y un permiso que no se lee no es
un permiso. Guarda las `t` en un `set()` que viva **fuera** del bucle de cada
pregunta, y **por herramienta**: autorizar `trm` no debe autorizar
`guardar_reporte`.

⚠️ **Devuelve el MOTIVO, no solo `True`/`False`.** Un `True` pelado tapa tres
situaciones distintas —el usuario dijo que sí, estaba autorizada de antes, o la
herramienta es libre y nunca se pregunta— y en el registro las tres se ven
iguales. El día que un agente haga algo que no debía, vas a leer
`"concedido": true` y vas a creer que lo autorizaste tú.

```python
return True, "libre"                          # nunca se preguntó
return True, "autorizada_antes"               # la 't' de una vuelta anterior
return True, "usuario_dijo_si"                # miró la pantalla y aceptó
return False, "usuario_dijo_no"
```

Y el motivo va **siempre**, también cuando se concede. Es el mismo patrón de
§8.l: **un motivo es un dato estable que se puede filtrar y contar; una frase,
no.** (Defecto real, encontrado por el propio registro en su primera corrida.)

### 6 — Registro (una línea de JSON por evento)

```python
def anotar(evento: str, **datos):
    linea = {"hora": datetime.now(timezone.utc).isoformat(timespec="seconds"),
             "evento": evento, **datos}
    with open(REGISTRO, "a", encoding="utf-8") as f:
        f.write(json.dumps(linea, ensure_ascii=False) + "\n")
```

Anota como mínimo: cada llamada (tokens, costo, duración, `stop_reason`), cada
herramienta (nombre, entrada, resultado, permiso) y cada parada (motivo).

**Anota siempre la hora, aunque no la vayas a usar.** Restando las horas de dos
eventos seguidos sale el tiempo que NO fue de la API — el humano que tardó en dar
un permiso, un disco lento, tu propio código. Es la única forma de responder
"¿por qué se demoró?" sin adivinar. (En una corrida real: 47 s entre la llamada
y la herramienta, de los cuales 3.98 fueron de la API.)

**Cómo leerlo después.** El archivo **acumula** entre corridas; no se
sobreescribe. Para procesarlo:

```python
import json
with open("registro.jsonl", encoding="utf-8") as f:
    eventos = [json.loads(linea) for linea in f]

llamadas = [e for e in eventos if e["evento"] == "llamada_api"]
print(sum(e["costo_usd"] for e in llamadas))
```

### 7, 8 y 9 — No confiar en lo que pide el modelo

Estas dos líneas son la puerta abierta de todo agente con varias herramientas:

```python
funcion = FUNCIONES[bloque.name]     # nombre inventado -> KeyError
salida = funcion(**bloque.input)     # argumento que no existe -> TypeError
```

Y reventar **aquí** tumba el bucle entero, con todo lo que ya pagaste adentro.
Da igual lo blindadas que estén tus funciones por dentro:
**una función a prueba de balas no sirve si el modelo no entra por la puerta.**

```python
funcion = FUNCIONES.get(bloque.name)            # 7. .get(), no [ ]
if funcion is None:
    salida = {"error": f"No existe '{bloque.name}'. Tienes: {', '.join(FUNCIONES)}."}
else:
    try:
        salida = funcion(**bloque.input)
    except TypeError as fallo:                  # 8. argumentos que no acepta
        traceback.print_exc()
        salida = {"error": f"'{bloque.name}' no acepta esos argumentos ({fallo})."}
    except Exception:                           # 9. defecto NUESTRO
        traceback.print_exc()                   #    a ti: el traceback
        salida = {"error": "Falló por un defecto interno. No es culpa de tu "
                           "petición: reintentarlo igual no va a servir."}
```

**Por qué `.get()` separado del `try` y no todo junto:** si envuelves la
búsqueda y la llamada en el mismo `try`, un `KeyError` nacido **dentro** de una
función se disfraza de "nombre inventado". Un defecto tuyo tapado como error del
modelo es un defecto que vive para siempre.

⭐ **La categoría de error que aparece aquí y no existía antes.** Hasta el nivel
4 había dos: falla el **mundo** (información: se le cuenta al modelo) y falla
**tu código** (defecto: tiene que doler y verse). Un nombre inventado es una
tercera: **falla el modelo** — y es la única de las tres que **se arregla sola**,
porque él lee el error y reintenta. Por eso vuelve al modelo en vez de reventar.

**Regla de reparto, y sirve para los nueve frenos:**

| Quién falló | A ti | Al modelo |
|---|---|---|
| el mundo (red, 503) | nada | `{"error": ...}`, que reintente |
| **el modelo** (nombre, argumentos) | nada | `{"error": ...}` con la lista correcta |
| **tú** (un `except` genérico salta) | **traceback completo** | "defecto interno, no reintentes" |

---

## 4.d Streaming

```python
with cliente.messages.stream(model=MODELO, max_tokens=1000, messages=[...]) as s:
    for trozo in s.text_stream:
        print(trozo, end="", flush=True)
    final = s.get_final_message()   # el Message completo: usage, stop_reason...
```

- `with` porque la conexión queda abierta y hay que cerrarla.
- `flush=True` o el texto se queda en el buffer y no verás nada. `end=""` para
  que los trozos se peguen en vez de saltar de línea.
- No acelera el total; adelanta la primera palabra (medido con el orden
  controlado: **~6.3 s** de adelanto. Sin controlar el orden salía 7.4 s — ver
  la trampa 1 más abajo).
- **Obligatorio** para `max_tokens` grande (si no: `ValueError`).
- ⚠️ **`text_stream` entrega solo bloques de texto.** Si el modelo empieza
  razonando, ese `thinking` no sale por ahí y la pantalla sigue quieta aunque el
  stream ya esté recibiendo. **Streaming reduce la espera en blanco, no la
  elimina.** Verificado midiendo el stream crudo (ejercicio 8 del nivel 4):
  `thinking` de 1.97 a 4.22 s, `text` desde 4.23 s.

### Cómo se llaman estas métricas

| Nombre | Qué mide |
|---|---|
| **TTFT** (*Time To First Token*) | cuánto tarda en aparecer el primer token |
| **TPOT** (*Time Per Output Token*) | cuánto tarda cada token después del primero |
| **ITL** (*Inter-Token Latency*) | el hueco entre token y token |
| Latencia *end-to-end* | de la petición a la última palabra |

`latencia total = TTFT + (tokens × TPOT)`.

⚠️ Con modelos que razonan hay **dos TTFT distintos** y hay que decir cuál: el
primer token *de cualquier tipo* (1.97 s en la corrida del nivel 4) y el primer
token *de texto*, que es lo que ve el usuario (4.23 s). `text_stream` mide el
segundo. No los mezcles en la misma tabla.

(**TTFB**, *Time To First Byte*, es otra cosa: la métrica de redes de siempre.
Aquí sería el `message_start`, a los 1.95 s.)

### Al medir tiempos de streaming, tres trampas

1. **El orden.** La primera llamada del programa paga la apertura de la conexión
   —**medido: ~1 s**—; la segunda no. Si siempre mides sin-streaming primero, le
   regalas ese segundo al streaming. **El control es correr cada forma en las dos
   posiciones**: por filas sale el sesgo, por columnas el efecto limpio.
2. **Los totales no son comparables si las respuestas tienen distinto largo.**
   Normaliza a **tokens/segundo** antes de concluir nada.
3. **Normalizar no arregla que n=1.** La razón tok/s dio 52.3 vs 58.6 en una
   corrida y 56.6 vs 52.8 en la siguiente — direcciones opuestas. Era ruido.
   Antes de darle dirección a una diferencia, mídela dos veces.

---

## 5. Elegir modelo

| Modelo | Input $/1M | Output $/1M | Úsalo para |
|---|---|---|---|
| `claude-opus-5` | $5.00 | $25.00 | Razonar, código, agentes |
| `claude-sonnet-5` | $3.00 | $15.00 | Volumen alto con buena calidad |
| `claude-haiku-4-5` | $1.00 | $5.00 | Clasificar, extraer, *pings* |

Dos reglas:

1. **La salida cuesta ~5x más que la entrada.** Mandar contexto es barato; generar
   texto largo, no.
   **Y en una conversación se multiplica otra vez:** lo que el modelo genera hoy
   se reenvía como entrada en todos los turnos siguientes. Medido en el nivel 2:
   27 tokens de salida de más costaron 145 tokens de entrada de más en 6 turnos.
   Por eso un `SYSTEM` que pida respuestas cortas no ahorra una vez, ahorra
   siempre. Ver `02-conversacion/README.md` → §2.2.
2. **Usa el más barato que resuelva bien la tarea.** Y ojo: la diferencia real es
   mucho mayor que la de la tabla, porque el modelo caro además **genera más
   tokens**. Medido en este curso al clasificar un comentario: Opus 5 costó
   **55x** más que Haiku 4.5 en una corrida y **31x** en otra — mismo script,
   mismo precio por token. Lo que cambia es cuánto razona Opus cada vez.
   Quédate con el orden de magnitud (decenas de veces), no con el número.
   Ver `LESSONS.md` → L1.12.

### Pensamiento (`thinking`) y su costo

| Modelo | ¿Piensa si no digo nada? |
|---|---|
| `claude-opus-5` | **Sí**, por defecto |
| `claude-sonnet-5` | **Sí**, por defecto |
| `claude-haiku-4-5` | No |

El razonamiento **se cobra como tokens de salida**, lo veas o no. Para leerlo:

```python
thinking={"type": "adaptive", "display": "summarized"},
```

Sin `display`, el bloque `thinking` llega igual pero con el texto **vacío** — y si
`max_tokens` es bajo, puede consumirse entero pensando y no dejar ni una letra de
respuesta (L1.1). Por eso: **siempre filtrar bloques por `type`, nunca `content[0]`.**

---

## 5.b Medir tokens sin pagar (`count_tokens`)

Cuenta los tokens de entrada de una llamada **sin generar nada**. Es gratis.

```python
n = cliente.messages.count_tokens(
    model="claude-opus-5",
    system=SYSTEM,          # opcional, pero cuenta
    tools=TOOLS,            # opcional, y CUENTA MUCHO (ver abajo)
    messages=historial,
).input_tokens
```

Úsalo para:

- saber cuánto vas a pagar **antes** de pagarlo
- comparar dos versiones de un prompt sin gastar
- decidir si toca recortar el historial (nivel 2)
- **pesar el menú de herramientas**, que es lo más caro y lo menos visible

### ⚠️ NUNCA estimes tokens dividiendo caracteres entre 4

Medido el 2026-07-30 con el menú de 6 herramientas del nivel 5b:

| Método | Resultado |
|---|---|
| A ojo | "~700-900" |
| 6.231 caracteres / 4 | ~1.557 |
| **`count_tokens` con `tools=`** | **3.049** |

Los dos estimados se quedaron cortos, y **en el mismo sentido**. La regla de
"4 caracteres por token" viene del inglés en prosa; **JSON en español tokeniza
mucho peor** (llaves, comillas, tildes).

Aislar el costo del menú es una resta de tres llamadas gratis:

```python
solo_msg = count_tokens(messages=msg)                      # 8
con_sys  = count_tokens(system=SYSTEM, messages=msg)       # 171  -> system: 163
todo     = count_tokens(system=SYSTEM, tools=TOOLS, ...)   # 3220 -> MENÚ: 3.049
```

→ **El único contador que vale es el de la API.** Y es gratis, así que no hay
excusa para estimar.

⚠️ **Y ese número se paga en CADA vuelta de CADA conversación, se llame o no
una herramienta.** Una herramienta de más es un impuesto permanente que se paga
aunque nunca la uses.

### ⚠️ Dos trampas de `count_tokens`, las dos medidas el 2026-07-30

**1. El resultado depende DEL MODELO.** Con la entrada byte a byte idéntica
(mismo system, mismo menú de 6, misma pregunta):

```
claude-opus-5     3.634
claude-sonnet-5   3.702      <- 159 tokens más que haiku
claude-haiku-4-5  3.543
```

→ **Un token no es una unidad universal: es la unidad de medida DE ESE MODELO.**
Contar con uno y presupuestar con otro es medir en pulgadas y pagar en
centímetros. **Pasa siempre el mismo `model=` que vas a usar de verdad.**

**2. Medir las partes por separado y sumarlas NO da el todo.** Pesando cada
herramienta sola y sumando las seis salen **4.877**; el menú completo pesa
**3.447**. La diferencia es un **costo fijo por TENER herramientas** (~286
tokens en opus, ~497 en haiku) que se estaba cobrando seis veces. Se paga
completo con la primera; la segunda ya no lo repite.

→ **La medición honesta no es sumar, es QUITAR:** mides la configuración real,
mides la alternativa, y restas.

```python
base  = count_tokens(system=SISTEMA, messages=msg)                  # sin menú
tres  = count_tokens(system=SISTEMA, tools=SOLO_LAS_USADAS, ...)    # alternativa
seis  = count_tokens(system=SISTEMA, tools=TOOLS, ...)              # la real
sobra = seis - tres        # <- ESTE es el número que te ahorrarías
```

### Tres letras pequeñas (verificadas en la documentación oficial)

1. **Es gratis, pero no ilimitado.** Tiene tope de peticiones por minuto según tu
   nivel de uso: 2.000/min en el nivel inicial. Ese límite es **independiente**
   del de `messages.create` — gastar uno no consume el otro.
2. **Es un estimado, no un número exacto.** La doc dice que el conteo real al
   crear el mensaje "puede diferir en una cantidad pequeña". Sirve para decidir,
   no para facturar.
3. **Solo cuenta la ENTRADA.** Los tokens de salida no existen hasta que el
   modelo responde, así que nadie puede contarlos por adelantado. Puedes
   calcular gratis la mitad barata de tu factura; la mitad cara solo la sabes
   pagándola.

Fuente: `https://platform.claude.com/docs/en/build-with-claude/token-counting`

### Por qué es gratis

Generar texto es trabajo de GPU, token a token: eso es lo caro. Contar tokens es
partir tu texto según un diccionario fijo — una tabla de búsqueda, sin modelo
pensando. Pesar el paquete es gratis; enviarlo se paga por peso.

---

## 5.b.2 Cómo experimentar barato

Dos categorías distintas. La segunda vale mucho más que la primera.

**Abaratar la llamada:**

- Usar `claude-haiku-4-5` en vez de `claude-opus-5` (medido: 31x más barato en
  una tarea trivial)
- Bajar `max_tokens` a lo que la tarea necesite de verdad

**Evitar la llamada:**

- `count_tokens` en vez de `create`, cuando solo necesitas medir la entrada
- **Datos de prueba escritos a mano** en vez de generarlos conversando

La última es la más subestimada. Un historial fijo dentro del script no cuesta
nada **y no vuelve a costar nada** por más veces que lo corras. Si vas a repetir
un experimento 50 veces para promediar, es la diferencia entre 1x y 50x.

Bonus: al no haber humano ni generación, el experimento mide siempre lo mismo.
Repetible y gratis a la vez.

> ⚠️ **El costo escondido de los datos falsos:** los escribes tú, así que salen
> demasiado limpios — frases completas, sin erratas, sin divagaciones. Las
> conversaciones reales no se parecen. Puedes acabar midiendo con precisión una
> situación que nunca ocurre, y que tu agente pase todas las pruebas y falle con
> el primer usuario. Usa datos falsos, pero pregúntate siempre si son
> representativos. (Se trabaja a fondo en el nivel 5.)

---

## 5.c Ventanas de contexto (el techo duro)

| Modelo | Ventana de entrada |
|---|---|
| `claude-opus-5` | 1.000.000 tokens |
| `claude-sonnet-5` | 1.000.000 tokens |
| `claude-haiku-4-5` | 200.000 tokens |

Pasarse **no degrada la respuesta: falla la llamada.** Por eso un agente largo
necesita una política de recorte (ver `02-conversacion/README.md`).

---

## 6. Checklist: proyecto nuevo desde cero

Cuando montes algo tuyo, fuera del curso, este es el orden:

- [ ] Carpeta del proyecto
- [ ] `python -m venv .venv` y activarlo
- [ ] `requirements.txt` con las librerías
- [ ] `.gitignore` que incluya `.env` y `.venv/`
- [ ] `.env.example` con los nombres de las variables, **sin valores reales**
- [ ] `.env` con los valores reales
- [ ] Un script de verificación que falle temprano y claro (ver §7)
- [ ] Correrlo y ver que pasa **antes** de escribir la primera línea del producto

---

## 7. Patrón: script de verificación (*preflight*)

La idea de `00-setup/verificar.py`, generalizada. En el mundo real esto se llama
**healthcheck**, **smoke test** o **preflight check**.

El molde, en orden de **más barato a más caro**:

```
1. ¿La versión del lenguaje sirve?
2. ¿Están las librerías?          -> try / except ImportError
3. ¿Existe la configuración?      -> ¿el .env existe y no tiene el texto de ejemplo?
4. ¿La configuración FUNCIONA?    -> una llamada real, mínima, al servicio
```

Y cada falla imprime **dos cosas**: qué pasó y qué hacer.

```python
def fallar(mensaje: str, solucion: str) -> None:
    print(f"[FALTA] {mensaje}")
    print(f"        -> {solucion}")
    sys.exit(1)
```

> El paso 4 es el que casi todos se saltan, y es el único que prueba la verdad.
> Ver `LESSONS.md` → L0.1.

---

## 8. Evaluar un agente

### 8.a La pregunta que se hace primero: ¿de qué lado cae?

Antes de escribir un eval, decide qué estás probando. La respuesta cambia todo:

| Lo decide… | Ejemplos | Cómo se prueba | Cuesta |
|---|---|---|---|
| **Tu código** | presupuesto, permisos, topes, timeouts, parseo, registro | casos con respuesta conocida | **$0.00** |
| **El modelo** | qué herramienta pidió, qué texto escribió | correr N veces y contar | plata |

> La mitad de tu agente se prueba gratis y da idéntico siempre. Empieza por ahí.

Y dentro de lo que decide el modelo, hay otra división:

| Pregunta | Herramienta |
|---|---|
| ¿Llamó `obtener_clima`? ¿`stop_reason` fue `tool_use`? ¿100×3205,8 = 320.580? | **`if`** |
| ¿Respetó el dialecto? ¿Citó la fuente? ¿Fue útil? ¿Suena natural? | **juez** |

**Regla dura:** si un `if` puede responderla, no uses un juez. Los modelos fallan
justo en lo que un `if` hace perfecto (distinguir `lleva` de `lleve`). Ver L5.15.

### 8.b Plantilla: eval determinista

```python
CASOS = []

def caso(grupo, descripcion):
    def envolver(fn):
        CASOS.append((grupo, descripcion, fn))
        return fn
    return envolver

@caso("permisos", "una herramienta desconocida se prohibe")
def _():
    ok, motivo = h.pedir_permiso("formatear_disco", {})
    return ok is False, f"ok={ok}, motivo={motivo!r}"
```

Cada caso devuelve `(paso, detalle)`. El detalle solo se imprime si falla.

**Cuatro reglas que hacen que un eval sirva:**

1. **Casos hostiles, no felices.** Probar `"s"` y `"n"` no encuentra nada.
   Probar `salir`, `stop`, `""`, `"S I"` encontró un agujero real (L5.13).
2. **Pares mínimos.** Dos entradas que se diferencian en una sola cosa. Si las
   dos dan el mismo veredicto, no estás midiendo lo que crees (L5.3).
3. **Prueba también el caso positivo.** Un candado que no deja pasar nada
   tampoco sirve: hay que comprobar que la función *hace* su trabajo.
4. **Cállale la boca al código probado.** Si lo que pruebas imprime, captura su
   salida y enséñala **solo si el caso falla**:

```python
capturado = io.StringIO()
with contextlib.redirect_stdout(capturado):
    ok, detalle = fn()
# ... si falla: print(capturado.getvalue())
```

### 8.c Evals de coherencia (los que cazan olvidos)

No prueban comportamiento; prueban que no se te olvidó nada al añadir una pieza:

```python
anunciadas = {t["name"] for t in HERRAMIENTAS}
assert not anunciadas - set(FUNCIONES)   # anunciada sin funcion
assert not set(FUNCIONES) - anunciadas   # funcion no anunciada
assert not anunciadas - set(PERMISOS)    # sin politica de permiso
```

Su momento llega cuando agregas la herramienta número seis y se te olvida el
permiso. Cuestan cero y avisan en un segundo.

### 8.d Para poder probar, el archivo tiene que ser importable

```python
if __name__ == "__main__":
    main()
```

Sin esto, importar el módulo para probar sus piezas **ejecuta el programa
entero**: crea carpetas, hace llamadas, gasta, y se queda esperando un `input()`.
Todo lo que ejecute va dentro de `main()`. Ver L5.12.

### 8.e Plantilla: correr N veces y contar

```
1. Escribe el detector.
2. PRUEBA EL DETECTOR sin llamar a la API (pares mínimos).
3. Corre N veces el MISMO prompt, con un CONTROL al lado.
4. Guarda cada respuesta completa en JSON.
5. Mira los rangos antes de concluir.
```

**Reglas:**

- **Copia el prompt literal** del sitio donde apareció el defecto, no uno
  parecido. Si lo cambias, ya no mides lo mismo (L5.5).
- **Intercala las versiones** (A,B,C,A,B,C…) en vez de correrlas en bloque, para
  que cualquier deriva se reparta por igual.
- **Comprueba que las entradas salgan idénticas al token** dentro de cada
  versión. Si no, el prompt no era el mismo.
- **Siempre un control**, aunque parezca gasto inútil. Es lo único que te dice si
  tu regla de medir sigue siendo la misma (L5.8).

### 8.f Cuánta confianza merece tu número

```python
def rango(exitos, total):
    """(minimo, maximo) creibles al 95%, en porcentaje."""
    if total == 0:
        return 0.0, 0.0
    p = exitos / total * 100
    if exitos == 0:                          # REGLA DE TRES
        return 0.0, 3 / total * 100
    if exitos == total:
        return 100 - 3 / total * 100, 100.0
    m = 1.96 * math.sqrt((p/100) * (1 - p/100) / total) * 100
    return max(0.0, p - m), min(100.0, p + m)
```

⚠️ **Los dos extremos necesitan la regla de tres.** La fórmula normal devuelve
`±0` cuando salen 0 aciertos, o sea *"eliminado con certeza total"*, que es
falso. Con `n=30` y cero apariciones, el tope real es **10%**, no 0%. Ver L5.10.

**Cómo se lee:** si los rangos de dos versiones **se solapan**, la diferencia no
está demostrada. No significa que no exista: significa que tu N no alcanza.

| N | 0 aciertos | ¿qué puedes afirmar? |
|---|---|---|
| 10 | 0% – 30% | casi nada |
| 30 | 0% – 10% | que es poco frecuente |
| 100 | 0% – 3% | que es raro de verdad |

**Y si tu métrica es binaria y no separa, cambia la métrica antes que el N.** Una
métrica que gradúa usa las 30 respuestas; una de sí/no solo usa las que fallan
(L5.9).

### 8.g Plantilla: rúbrica para un juez

```
Eres un evaluador de <UNA SOLA COSA>. No evalues nada mas.

0 = <nivel malo>.  Señales concretas: <palabras exactas>
1 = <nivel medio>. Señales concretas: <palabras exactas>
2 = <nivel bueno>. Señales concretas: <palabras exactas>

REGLA DE DESEMPATE:
Si aparecen señales de varios niveles, manda <la mas baja / la mayoria / ...>.
Ejemplo resuelto: "<texto real>" -> nota <n>, porque <razon>.

COMO TRATAR LO AMBIGUO:
<que hacer con las palabras que pueden significar dos cosas>

Responde SOLO con JSON:
{"nota": 0, "razon": "max 12 palabras", "palabras": ["las","que","lo","delatan"]}
```

**Lo que hace utilizable una rúbrica:**

1. **Un solo eje.** Mezclar "dialecto" y "utilidad" en una nota da un número que
   no se puede interpretar.
2. **Niveles separables.** Si dos niveles se confunden, ningún juez —ni humano—
   dará notas estables.
3. **Ejemplos concretos, no adjetivos.** Palabras exactas, no "suena bien".
4. **Regla de desempate.** Sin ella el juez decide por mayoría, que casi nunca es
   lo que querías (L5.16).
5. **Pide siempre `palabras`.** Es lo que te deja auditarlo (ver 8.h).

### 8.h Validar al juez (esto no es opcional)

> Un juez que nadie validó es una opinión con formato de número.

Tres comprobaciones, en este orden:

**1. ¿Coincide con lo que ya sabes?** Ponlo a calificar casos cuya etiqueta
conoces (los de tu detector determinista, o los que etiquetaste a mano).

**2. ¿Se contradice consigo mismo?** Vuelve a juzgar una submuestra y compara.
⚠️ Esto mide **estabilidad, no sesgo**: el mismo modelo dos veces tiene el mismo
punto ciego. Un juez puede ser 100% consistente y estar 100% equivocado (L5.17).

**3. ¿Se inventa la evidencia?** Cuatro líneas, y es la más importante:

```python
faltan = [p for p in dato["palabras"] if norm(p) not in norm(texto)]
```

En una corrida real, **9 de 451 citas (2%) no estaban en el texto** — y eran
justo las que sostenían los veredictos. El juez citaba `lleve` en textos que
decían `lleva`, para justificar una mezcla inexistente (L5.18).

⚠️ Al comparar, **normaliza tildes en los dos lados**. Si no, acusarás al juez de
inventarse `pongase` cuando dijo `póngase`.

**4. ¿Contestó siquiera?** Añadido tras el paso 10 del 5b, y es el que faltaba.
Un juez puede fallar sin devolver un veredicto malo: puede no devolver nada.
Ver 8.h.2, porque tiene su propia sección.

**5. ¿Se contradice entre casos parecidos?** Si califica casi igual dos
respuestas y les da veredictos opuestos, **sospecha primero de tu rúbrica, no
del modelo**: casi siempre son dos criterios que se solapan y lo obligan a
elegir una frontera que tú no le diste (L5b.24).

### 8.h.2 Cuando el que falla es el instrumento, no el examinado

> **Un fallo del juez que se cuenta como cero es indistinguible de un defecto
> del agente en la tabla final — y los dos exigen arreglos opuestos.**

#### 🚨 `max_tokens` incluye lo que el modelo PIENSA

Es la trampa que más caro sale y no se ve en ningún sitio. Los modelos que
razonan devuelven un bloque `thinking` **antes** del texto, y ese bloque gasta
los mismos tokens de salida.

Medido en una corrida real de un juez con `max_tokens=1500`:

```
caso fácil    stop_reason=end_turn     salida=1484   bloques: thinking + text
caso difícil  stop_reason=max_tokens   salida=1500   bloques: SOLO thinking
```

El segundo pensó tanto que **se quedó sin cupo para hablar**: cero caracteres de
respuesta.

⚠️ **Y lo peor no es que falle, sino cuáles fallan:** los casos difíciles
producen razonamientos largos, así que **las fallas están sesgadas hacia
exactamente las preguntas que sí podían reprobar**. El resultado parece un
`100%` limpio y en realidad le faltan los casos duros.

→ **Para un juez, ponle a `max_tokens` 3 o 4 veces lo que ocupa la respuesta
que esperas.** Y mira siempre `stop_reason`.

#### Separa las fallas por causa, no las juntes en "no se pudo leer"

```python
if respuesta.stop_reason == "max_tokens":
    return {"_fallo": "sin_cupo", ...}
try:
    veredictos = json.loads(crudo)
except (ValueError, json.JSONDecodeError):
    return {"_fallo": "json_ilegible", ...}
```

En pantalla las dos se ven iguales y **piden arreglos distintos**: una es subir
el cupo, la otra es aclarar el formato. Guarda siempre el texto crudo.

#### Y el recuento tiene que decir en voz alta lo que le falta

Un porcentaje calculado sin los casos que el juez no pudo calificar es un
porcentaje optimista. Dilo en la misma línea, junto al número.

### 8.h.3 Tres reglas de diseño para un juez

**1. La rúbrica vive en UN solo sitio, y es el que puedes leer.**
Léela del archivo `.md`; no la copies al código. Si están en dos sitios, el día
que corrijas el `.md` habrá **dos rúbricas: la que lees y la que califica**, y
nada te avisará. Pon un freno que muera si el trozo leído sale demasiado corto.

**2. No todos los criterios aplican a todos los casos.**
Declara por caso cuáles se califican. Promediar casillas que no aplican es
promediar aire — y una casilla que solo aparece 3 veces produce un "67%" que no
ordena a nadie. **El conteo de casillas por criterio te dice dónde te falta
cobertura, antes de gastar un peso.**

**3. El juez no calcula el promedio: lo calcula Python.**
Es la misma regla de las herramientas de un agente. Pedirle que además promedie
es darle una oportunidad más de equivocarse a cambio de nada.

**Y lo que el juez NO debe ver:** el nombre del modelo examinado, el costo, los
tokens y el número de vueltas. Si sabe que algo fue barato o lento califica
distinto, y esas cosas ya las mide el `usage` — exacto y gratis.
→ *No se le pregunta a un modelo lo que un número ya sabe.*

### 8.i Elegir el modelo juez

| | |
|---|---|
| Por defecto | el más barato que **pase la validación de 8.h** |
| Nunca | el más barato porque sí — "clasificar es fácil" no siempre es cierto |
| Autopreferencia | un modelo tiende a aprobar texto de su propia familia |
| Jurado de 2+ | útil, pero **solo si son de familias distintas** |

**Lo primero es validar contra tus etiquetas, no diversificar proveedores.** Un
juez de otra empresa que nadie comparó contra tu criterio sigue siendo una
opinión sin validar.

### 8.j Cuánto cuesta evaluar

| | costo **medido** |
|---|---|
| Eval determinista (cualquier cantidad) | **$0.00** |
| 30 corridas de Opus 5, respuestas cortas | ~$0.13 |
| 90 corridas (3 versiones × 30) | ~$0.32 |
| Juzgar 120 respuestas con **Haiku 4.5** | **$0.127** |
| Juzgar 120 respuestas con **Sonnet 5** | **$0.306** |

⚠️ Las dos últimas filas decían antes *"140 respuestas con Haiku, ~$0.06"*. Era
un **estimado mío sin medir** y salió a menos de la mitad del costo real. Los
números de arriba son medidos. Mismo patrón del `"55x"` (§1) y del `"~$0.02"`
del streaming (§4.d): **si la tabla dice "aproximado", desconfía; si nadie
corrió nada, el número es una opinión.**

**Guarda siempre las respuestas completas en JSON.** Juzgar y reanalizar sale
casi gratis comparado con volver a generarlas — y la pregunta interesante casi
siempre se te ocurre después de correr el experimento (L5.20).

**Ata los precios al modelo, nunca a dos constantes sueltas.** Un script con

```python
MODELO = "claude-sonnet-5"
PRECIO_ENTRADA = 1.00 / 1_000_000   # Haiku   ← quedó del modelo anterior
```

imprime un costo **falso y sin avisar**, justo en la línea que dice "COSTO
REAL". Usa un diccionario `PRECIOS[MODELO]` y haz que **reviente** si el modelo
no está: fallar es mejor que mentir. Imprime el precio aplicado al lado del
total, y guárdalo en el JSON junto con los tokens — un costo suelto no se puede
auditar después.

⚠️ **Los precios de lanzamiento caducan.** Sonnet 5 está a $2/$10 por millón
hasta el **2026-08-31**; después, $3/$15. Escribe la fecha en el código.

### 8.k Errores comunes al evaluar

| Síntoma | Causa real | Salida |
|---|---|---|
| El defecto "desapareció" al probarlo aparte | cambiaste las condiciones, no el defecto | copia el prompt literal del sitio original |
| El detector marca lo correcto como defecto | normalizaste y borraste la señal (tildes) | dos listas: una que normaliza y otra que no |
| `0 de 30` presentado como "eliminado" | fórmula normal en el extremo | regla de tres: el tope es `3/n` |
| Los rangos siempre se solapan | métrica binaria con pocos fallos | cambia a una métrica que gradúe |
| El juez no devuelve JSON | pasa; cuéntalo, no lo escondas | `re.search(r"\{.*\}", crudo, re.S)` y contar los fallos |
| El juez cita palabras que no están | fabrica evidencia | comprobar las citas contra el texto |
| El script se rompe la segunda vez que corre | lee y escribe en la misma carpeta | filtra sus propios archivos al leer |
| `KeyError` al importar tu propio módulo | el archivo se ejecuta al importarse | `if __name__ == "__main__": main()` |

---

## 8.l Probar tus propias funciones (sin modelo, sin red, $0.00)

Esto es lo primero que se prueba de un agente: las herramientas son Python normal.
Si el archivo de herramientas no importa `anthropic`, se prueba **entero** gratis —
y ese es el argumento de peso para tenerlo separado del harness.

### El caso de prueba es un DATO, no código repetido

```python
CASOS = [
    # (etiqueta,        argumentos,                   esperado)
    ("camino feliz",    (10, "USD", "COP", 3900),     39000),
    ("monto negativo",  (-100, "USD", "COP", 3900),   "error"),
]

fallos = 0
for etiqueta, args, esperado in CASOS:
    try:
        r = mi_funcion(*args)                    # el * desempaqueta
    except Exception as e:
        obtenido = f"REVENTO: {type(e).__name__}"
    else:
        obtenido = "error" if "error" in r else r["resultado"]

    ok = (obtenido == esperado) and (type(obtenido) is type(esperado))
    if not ok:
        fallos += 1
    print(f"{'ok   ' if ok else 'FALLA'} {etiqueta:22} "
          f"esperado={esperado!r:10} obtenido={obtenido!r}")

print(f"\n{len(CASOS)} casos, {fallos} fallaron")
```

Agregar el caso 27 es **una línea**. Con `assert` suelto son dos líneas por caso,
y el primer fallo mata el programa: te enteras de un problema por corrida.

### Las tres familias, y la que todo el mundo se salta

| Familia | Qué es |
|---|---|
| camino feliz | la entrada normal |
| **bordes** | el cero, el vacío, lo negativo, lo enorme, el `.5` |
| lo malo | lo que **debe** ser rechazado |

Los bordes. El camino feliz se prueba solo mientras escribes, y lo malo se prueba
porque acabas de escribir los `if`. **Los bordes no se le ocurren a nadie hasta
que un usuario los encuentra.**

### Reglas

1. **Imprimir no es probar.** Si tú miras la salida y decides, el juez eres tú y no
   hay prueba. La prueba dice `ok`/`FALLA` sola.
2. **Un caso, una variable.** Un caso con dos defectos pasa a verde cuando arreglas
   uno, con el otro todavía roto.
3. **`try/except` obligatorio.** Sin él, el eval muere en el caso que revienta y no
   ves los siguientes. Anota `REVENTO: TypeError` **como un resultado más**, en la
   misma tabla: reventar *es* un comportamiento.
4. **No compares el texto del error, solo que haya error.** Si comparas la
   redacción, mejorar el mensaje rompe la prueba. (Igual que clasificar por clase
   de excepción y no por su texto, §3.b.)
5. **Cada caso independiente.** Si el orden importa, son N casos encadenados, no N
   pruebas.
6. **Un caso de prueba es la forma más duradera de escribir una decisión.** El
   comentario se ignora; el caso rojo pregunta "¿seguro?". Si aceptas el monto
   cero, escribe el caso que lo dice.

### Cuatro trampas de Python que se cazan aquí

| Trampa | Qué pasa | Salida |
|---|---|---|
| `4.0 == 4` es `True` | el `==` compara **valor, no tipo**; el caso pasa en verde con el defecto puesto | añade `and type(obtenido) is type(esperado)` |
| `round(3.7, 0)` → `4.0` | pedir 0 decimales **no** es lo mismo que no pedir decimales | `round(x)` sin segundo argumento devuelve `int` |
| `isinstance(True, int)` es `True` | `True` vale 1: `True * 3900` da 3900 y parece dinero | `isinstance(x,(int,float)) and not isinstance(x,bool)` |
| `round(2.5)` → `2` y `round(3.5)` → `4` | *banker's rounding*: al par más cercano. Para dinero la norma suele ser medio arriba | `Decimal`, no `float` |

Las cuatro dan un resultado **creíble**. Ninguna revienta.

### Funciones que cambian el mundo (efectos secundarios)

Si la función escribe un archivo, manda un correo o borra algo, **lo que devuelve
es un recibo, no la verdad**. Comenta la línea que escribe: la función devuelve
exactamente lo mismo y tu prueba dice `ok`.

```python
def limpiar_caja():
    """Estado CONOCIDO antes de cada caso. Solo borra dentro de la caja."""
    CAJA.mkdir(exist_ok=True)
    for p in CAJA.iterdir():
        if p.is_file():
            p.unlink()
```

- **Limpia antes de CADA caso**, no una vez al principio. El archivo que dejó la
  corrida de ayer hace pasar "el archivo existe" aunque la función ya no escriba.
- **Comprueba dos cosas:** que exista **y** que el contenido coincida (podría
  crearlo vacío o escribirlo dos veces).
- **En los casos que esperan rechazo, comprueba que el disco quedó intacto.** Una
  función puede escribir y *después* devolver error.
- **Veredicto en dos mitades**, y que el mensaje diga cuál se rompió:
  `ok = (obtenido == esperado) and (pero == "")`.
- **Limpia también al terminar**: un eval no deja basura.

### Comprueba que tus pruebas sirven: sabotea

Rompe a propósito la línea que hace el trabajo y **exige ver el rojo**. Si sigue
en verde, la prueba no estaba mirando lo que creías. Restaura y confirma el verde.

> Una prueba en rojo dice dónde está el problema. Una prueba en verde **no** dice
> que no haya problema: dice que tu comparación no lo ve.

**Qué sabotear, en orden de lo que más enseña** (los cinco de la sesión 19):

| Rompe esto | Y mira si el eval ve que… |
|---|---|
| **quién** sale de una lista (`pop(0)` → `pop()`) | no basta contar cuántos quedaron |
| un **freno** (`0 <= i` → `i <`) | lo prohibido sigue prohibido |
| un **borde** (`>` → `>=`) | probaste los DOS lados, no uno |
| el **orden** de dos textos unidos | *"¿está ahí?"* no es *"¿en qué orden?"* |
| el **desvío** del archivo de pruebas | tu trampa del disco de verdad salta |

**Las tres cosas que enseñaron, y ninguna se ve razonando:**

1. ⭐ **Un defecto puede reportar ÉXITO.** Con el tope botando el más nuevo, el
   motivo seguía diciendo `desplazo` y el conteo seguía dando 8. Solo lo vieron
   los casos que preguntaban **quién** quedó adentro.
2. ⚠️ **Un eval con efecto secundario destructivo no se ve rojo: se ve verde.**
   Sin el desvío, 48 casos pasaron **mientras borraban el archivo de verdad**.
3. **El caso genérico vale más que el concreto.** Al faltar un mensaje, el caso
   concreto dijo `REVENTO: KeyError` (se rompió) y el genérico dijo
   `['refrescado']` (**qué** arreglar). Prefiere los que recorren una tabla
   entera a los que prueban una entrada.

⚠️ **Y una trampa del sabotaje mismo:** si al romper algo el eval **se cuelga o
revienta** en vez de ponerse rojo, no lo ignores. Suele significar que el caso
llama a algo que exige un humano (un `input()`). Un rojo que dice *"me colgué"*
no dice *"la tabla está mal"*.

### Y el límite, que hay que saber decir

Un eval no dice *"mi código está bien"*. Dice *"estas 26 cosas se comportan como
dije"*. Todo lo demás sigue sin explorar — y anotar **dónde acaba** la prueba es
parte de tenerla.

---

## 9. Memoria persistente (nivel 6b)

### Los comandos

```powershell
cd 06b-memoria-skills

python memoria.py                 # ver qué recuerda el agente
python memoria.py borrar 0        # olvidar un dato por su número
python memoria.py borrar todo     # vaciar la memoria

python evals_memoria.py           # 73 casos, $0.00, sin red
python evals_agente.py            # 121 casos, $0.00, sin red

python prueba_memoria.py 1        # 💰 SÍ GASTA (~$0.01) — cuenta algo suyo
python memoria.py                 #    ...míralo en el disco...
python prueba_memoria.py 2        # 💰 SÍ GASTA — proceso NUEVO: ¿se acuerda?

python volumen.py                 # 💰 ~$0.12 — 10 conversaciones, con diagnóstico
python volumen.py 7               # 💰 ~$0.01 — SOLO la conversación 7
```

⚠️ **Antes de cualquier prueba de memoria: `python memoria.py borrar todo`.** Si
quedan datos de antes, los números mienten — un hecho que el agente ya sabía sale
como "omitido" cuando en realidad hizo bien en no guardarlo.

⚠️ **Los dos actos se corren por separado, y es el punto entero.** Si corrieran
en el mismo proceso, el acto 2 podría estar leyendo lo que quedó en la RAM.
**La única prueba honesta de que algo es persistente es cerrar el programa.**

📌 **Desde el nivel 6b hay dos `evals`**, porque el proyecto del 5b se copió aquí:
`evals_memoria.py` prueba la memoria y su unión con el agente; `evals_agente.py`
son los 121 del 5b, sin cambios.

### La regla de una línea

> **La API no tiene memoria. Nunca.** Ni entre corridas, ni dentro de una
> conversación. Todo lo que parece memoria lo pone **tu harness** en el prompt.

Por eso cambiar de modelo **no** arregla la amnesia: opus olvida igual que haiku.

### El formato sale de la política, no del gusto

| Qué guarda | Formato | Cómo se escribe |
|---|---|---|
| **Eventos** — lo que pasó (`registro.jsonl`) | `.jsonl` | se **añade** al final |
| **Estado** — lo que es verdad hoy (`memoria.json`) | `.json` | se **reescribe** entero |

Si dudas de cuál usar, pregúntate si una línea vieja puede volverse falsa. Si
puede, es estado.

### Los cuatro frenos que no se pueden olvidar

1. **`cargar_memoria()` NUNCA revienta.** Corre al arrancar el agente: si lanza
   una excepción, el agente no existe. La memoria es un lujo; la respuesta es el
   producto.
2. **El archivo dañado NO se borra.** Es la única evidencia de qué pasó.
3. **Cada dato lleva su fecha.** *Un dato guardado sin fecha es un dato que no
   sabes si creerle.* Un dato no se daña: se **vence**, y vencido parece bueno.
4. **Tiene que haber un tope.** Sin política de olvido, el sistema no está
   terminado — y lo que crece se paga en la **entrada** de cada vuelta.

### ¿Permiso o revisión?

> **Permiso = ANTES, para lo irreversible.**
> **Revisión = DESPUÉS, para lo reversible.**

Un archivo de texto que puedes abrir y corregir **no necesita permiso**: necesita
que puedas verlo y borrarlo. Y ojo con esto:

⚠️ **Un permiso volátil sobre una herramienta persistente es un desajuste de
diseño.** `AUTORIZADAS` vive en RAM y muere al cerrar; la memoria sobrevive. Te
preguntaría lo mismo todos los días, y **un permiso que se pregunta demasiado
deja de leerse.**

Si quitas el permiso, **la obligación se muda al registro**: cada escritura deja
huella. Permiso → observabilidad.

### ⚠️ Al probar memoria: la trampa del archivo real

Un eval que escribe en el `memoria.json` de verdad **le borra al agente lo que
aprendió** — y sale en verde mientras lo destruye. Se resuelve con **dos** cosas,
no una:

```python
ARCHIVO_REAL = memoria.ARCHIVO
ANTES = ARCHIVO_REAL.read_bytes() if ARCHIVO_REAL.exists() else None
memoria.ARCHIVO = ARCHIVO_REAL.parent / "memoria_de_prueba.json"   # 1) desviar
...
# 2) al final: comprobar que el real quedó byte por byte igual
```

La 1 sola es una promesa. La 2 la convierte en un hecho comprobado.

### Cuándo NO necesitas base de datos ni RAG

Son **dos ejes independientes**, no una escalera:

| Eje | Qué lo mueve | Camino |
|---|---|---|
| **Usuarios** | cuántos escriben a la vez | archivo → SQLite → PostgreSQL |
| **Conocimiento** | cuánto hay que consultar | leerlo entero → Skills → RAG |

Un archivo plano es la respuesta **correcta** para un usuario. Con miles no es
"menos elegante": **se rompe** — dos escrituras al tiempo lo corrompen sin error
y sin aviso, y para leer un dato hay que leerlos todos.

```
¿Cabe todo en el prompt sin arruinarte?  ->  no necesitas RAG. Mándalo.
¿Son pocos y sabes cuál sirve?           ->  léelo con una herramienta.
¿Son muchos y no sabes cuál sirve?       ->  ahora sí, RAG.
```

---

## 10. Cuando el defecto está en el PROMPT, no en el código

Los evals prueban tu código. **Un prompt no se prueba con `assert`: se prueba
corriéndolo.** Esta sección salió de arreglar cinco defectos reales en la sesión
19 — todos medidos antes y después.

### Primero: ¿dónde va la regla?

⚠️ **Una descripción de herramienta solo pesa cuando el modelo YA está
considerando usarla.** Si decide no llamarla, no lo frena nada.

| La regla dice… | Va en |
|---|---|
| cómo se USA esta herramienta, cuándo sí y cuándo no | su **descripción** |
| qué puede AFIRMAR el agente, qué debe hacer siempre | el **system prompt** |

**El caso real:** el agente dijo *"Anotado: de ahora en adelante te daré las
cifras en tablas"* **sin llamar a `recordar`**. Ninguna descripción podía
frenarlo, porque nunca consideró la herramienta. La regla *"no digas que
guardaste si no guardaste"* fue al system y el defecto desapareció.

> ⭐ **La ubicación fue el arreglo, no la redacción.**

### Ordena más de lo que prohíbes

Una descripción con **cuatro prohibiciones y una instrucción positiva** guardó
**4 de 9** hechos: ante la duda, el modelo se abstiene.

Invertida la proporción —la orden primero, con **frases que la disparan**
(*"soy…", "tengo…", "vivo en…"*), **ejemplos de lo que sí se guarda**, y *"ante
la duda, GUARDA"*— pasó a **9 de 9**.

⭐ **Y el empaquetado (dos hechos en una ficha) NO lo arregló la regla abstracta**
—*"un hecho por llamada"* ya estaba escrita— **sino el ejemplo del error
concreto**: *"ante 'tengo una empresa y viajo a Panamá' van DOS llamadas, no
una"*.

> **Un ejemplo del error vale más que la regla que lo prohíbe.**

### Describir no es prohibir

`historial` decía *"la TRM oficial"*. El modelo la llamó **para el euro**, vio
que le llegaban datos del dólar, **lo dijo en voz alta**, y siguió igual.

La descripción era **verdadera y no frenaba nada**. Hubo que escribir *"SOLO
EXISTE PARA EL DÓLAR… si te preguntan por el euro, NO llames a esta"*.

### Que la regla no sea más estrecha que el problema

*"Nunca inventes un **número**"* deja pasar tendencias, fechas y días de la
semana. El agente afirmó *"el euro ha estado fuerte esta semana"* sin un solo
dato del euro — y no violó la regla.

> 🚨 **Una regla más estrecha que el problema da la sensación de estar cubierto
> donde no lo estás.** Una tendencia es un dato igual que un precio.

### Lo que el modelo no puede saber, no se prohíbe: se pone

Un modelo **no tiene reloj**. Prohibirle inventar la fecha solo lo obliga a decir
"no sé". Hay que dársela.

⚠️ **Y casi nunca merece una herramienta:**

| | costo |
|---|---|
| herramienta `hoy()` | ~200 tokens de menú **en cada vuelta** + **una vuelta entera** |
| una línea en el system | **~40 tokens, cero vueltas** |

> **Si el dato siempre se necesita y no cambia dentro de la conversación, va en
> el prompt.** (La fecha y la memoria son el mismo caso.)

### Nunca le pidas que cuente: dáselo contado

La primera versión decía *"cualquier otra fecha, **cuéntala** desde esta"*. Y
contó mal: *"el viernes 2 de agosto"* (es domingo).

**Contar días de calendario es aritmética**, y este modelo la hace de cabeza y
falla — igual que cuando inventó `3.209,64` dividiendo a escondidas.

⭐ **Tercera aparición del mismo patrón, y tercera vez que sale casi gratis:**

| puente | qué evitó | costo |
|---|---|---|
| `cop_por_1_usd` en `tasa()` | un número inventado | 11 millonésimas de dólar |
| `usd_por_1_cop` en `trm()` | la división a escondidas | ~0 |
| ayer / mañana / próximo lunes | una fecha inventada | $0,0001 por vuelta |

Y va con las dos cosas, como `convertir`: **se le da el dato hecho Y se le
prohíbe fabricarlo.**

### ⚠️ Un dato nuevo puede cambiar lo que no tenía que ver con él

Con el calendario puesto, el agente **dejó de llamar a `trm()`** y afirmó qué
tasa estaba vigente **deduciéndolo del calendario**. Le diste fechas y dejó de
pedir tasas.

> **Después de tocar un prompt, revisa lo que YA funcionaba.** No solo lo que
> venías a arreglar.

### 🚨 Cuándo parar de parchear

Tres rondas de prompt en un día: cada una arregló lo que buscaba **y destapó algo
nuevo**. Y cada una se juzgó con **una sola muestra**.

> 🚨 **Pulir un prompt contra una muestra es perseguir la cola: arreglas lo que
> viste la última vez, no lo que falla más.**

**Cuando cada parche destapa el siguiente, lo que falta no es un parche mejor: es
el instrumento de medida** — la rúbrica y el juez de §8. Reconocer que un método
se agotó vale más que una ronda más.
