# Nivel 3 — Tu primer agente

En el nivel 2 le diste memoria al modelo. Aquí le das **manos**.

Hasta ahora tu programa hacía una sola cosa: mandar texto y recibir texto. En
este nivel el modelo empieza a **pedirte que hagas cosas por él**, y tu código
las hace. Ese ida y vuelta es lo que convierte un chat en un agente.

Antes de empezar, desde la raíz:

```powershell
.\.venv\Scripts\Activate.ps1
cd 03-primer-agente
```

---

## La idea, antes del código

Claude no sabe qué temperatura hace ahora mismo en Bucaramanga. No es que sea
tonto: es que **no tiene forma de mirar**. No tiene internet, no tiene reloj, no
puede abrir archivos. Solo recibe texto y devuelve texto.

Entonces le damos un **menú**: una lista de cosas que puede pedir.

**Analogía:** imagina a un experto encerrado en un cuarto sin ventanas, con un
teléfono que solo recibe cartas. Le mandas una pregunta y, con ella, un menú de
restaurante. Él te devuelve una carta que dice *"pido: obtener_clima, ciudad:
Bogotá"*. Esa carta **no es comida**. Alguien tiene que ir a la cocina, cocinar,
y meterle el plato por debajo de la puerta. Ese alguien eres tú.

Ese ciclo tiene 5 pasos y se llama **el bucle agéntico**:

```
   1. Tú mandas: pregunta + menú de herramientas
                       ↓
   2. Claude responde: "necesito obtener_clima(ciudad='Bogotá')"
      stop_reason = "tool_use"
                       ↓
   3. TU CÓDIGO ejecuta la función de verdad     ← aquí no hay IA, es Python normal
                       ↓
   4. Tú mandas de vuelta: el resultado
                       ↓
   5. Claude responde al usuario, ya con el dato en la mano
      stop_reason = "end_turn"
```

Y si en el paso 5 vuelve a pedir otra herramienta, se repite. Por eso es un
bucle y no una escalera.

---

## 3.1 — El modelo pide, no ejecuta

```powershell
python 01_pedir_herramienta.py
```

Este script se detiene a propósito en el paso 2. Le da a Claude una herramienta
llamada `obtener_clima`... que **no existe**. No hay ninguna función con ese
nombre en el archivo. Aun así funciona, porque el modelo nunca la ejecuta.

### Lo que salió de verdad — y por qué salió distinto dos veces

**Corrida A:**

```
stop_reason: tool_use
bloques en content: 1

--- bloque 0: type = tool_use
  id     : toolu_01WQq8k5dtdg8MPqaQ4E8EM4
  name   : obtener_clima
  input  : {"ciudad": "Bogota"}
```

**Corrida B (mismo script, minutos después):**

```
stop_reason: tool_use
bloques en content: 2

--- bloque 0: type = thinking
(razonamiento interno; puede venir vacio)

--- bloque 1: type = tool_use
  id     : toolu_01KvkCDg75oUZ8DAPB1tbW7a
  name   : obtener_clima
  input  : {"ciudad": "Bogota"}
```

**Un bloque en una, dos en la otra.** Nada cambió en el código. Opus 5 tiene
*pensamiento adaptativo*: decide llamada por llamada si le conviene razonar
antes de responder. En la corrida B decidió que sí.

Esto es la lección L1.6 (nada es determinista) en un lugar nuevo: **no solo
cambia el texto entre corridas, cambia la ESTRUCTURA de la respuesta.**

Y por eso el atajo ingenuo es una bomba de tiempo:

```python
bloque = respuesta.content[0]
print(bloque.name)      # corrida A: funciona
                        # corrida B: revienta, content[0] es thinking
```

El mismo código pasa en una máquina y falla en otra, sin que nadie haya tocado
nada. Recorrer `content` con un `for` filtrando por `bloque.type` no es estilo:
es lo único que sobrevive.

*(El bloque `thinking` sale vacío porque la API no devuelve el texto del
razonamiento por defecto. Pero existe, ocupa un lugar en `content` y se paga.)*

Tres cosas nuevas, todas importantes:

| Cosa | Qué es |
|---|---|
| `stop_reason: "tool_use"` | La señal. En el nivel 1 solo habías visto `end_turn` y `max_tokens`. Este significa: *"no terminé, te estoy esperando"*. |
| `type: "tool_use"` | Un tipo de bloque nuevo dentro de `content`. Por eso nunca se lee `content[0].text` a ciegas (lección L0.7, otra vez). |
| `id: "toolu_..."` | Un **número de ticket**. Cuando devuelvas el resultado tendrás que citar ese id exacto. Si no coincide, la API rechaza el mensaje. |

Fíjate también en `input`: tú escribiste *"Que clima hace ahora mismo en
Bogota?"* y el modelo sacó solo `{"ciudad": "Bogota"}`. Eso lo hizo leyendo el
`input_schema` que escribiste. Nadie programó ese parseo.

### La herramienta no es código

```python
{
    "name": "obtener_clima",
    "description": "Devuelve el clima actual de una ciudad. Úsala siempre que...",
    "input_schema": {...},
}
```

Es un diccionario. Es **una descripción**, no una implementación. Se manda en
cada llamada, dentro del parámetro `tools`, y se paga como tokens de entrada
igual que todo lo demás.

De los tres campos, el que más manda es `description`. Es el que decide *cuándo*
el modelo pedirá la herramienta. Cambiarlo cambia el comportamiento del agente
sin tocar una línea de código.

---

## 3.2 — El bucle completo

```powershell
python 02_bucle.py
```

Aquí sí hay una función `obtener_clima` de verdad (un diccionario con tres
ciudades) y el bucle se cierra.

### Las 5 líneas que lo son todo

```python
if respuesta.stop_reason != "tool_use":
    return texto                                          # (A) terminó

historial.append({"role": "assistant", "content": respuesta.content})   # (B)

resultados = []
for bloque in respuesta.content:
    if bloque.type == "tool_use":
        salida = FUNCIONES[bloque.name](**bloque.input)   # (C) corre TU código
        resultados.append({
            "type": "tool_result",
            "tool_use_id": bloque.id,                     # (D) el ticket
            "content": salida,
        })

historial.append({"role": "user", "content": resultados})  # (E)
```

Cuatro detalles que rompen el programa si los haces mal:

- **(B) se guarda `respuesta.content` entero**, no solo el texto. En el nivel 2
  guardabas `texto`; aquí no puedes. Si le quitas los bloques `tool_use`, la API
  rechaza el mensaje siguiente porque hay un resultado sin petición.
- **(D) el `tool_use_id` debe ser idéntico.** Es lo que empareja pregunta y
  respuesta cuando hay varias herramientas en vuelo.
- **(E) el resultado va con `role: "user"`.** Aunque no lo escribiste tú. Para la
  API, todo lo que *entra* al modelo es `user`; todo lo que *sale* es `assistant`.
  El resultado de una herramienta entra, así que es `user`.
- **Todos los resultados van en UN solo mensaje.** Si el modelo pidió dos
  herramientas y les mandas dos mensajes separados, la API se queja.

### Lo que salió de verdad (corrida real)

```
=== Que clima hace en Medellin?
  [vuelta 1] stop_reason=tool_use entrada=452 salida=73
     -> ejecuto obtener_clima({"ciudad": "Medellin"})
        devolvio: 24 grados centigrados, despejado.
  [vuelta 2] stop_reason=end_turn entrada=543 salida=82
RESPUESTA: En Medellín hay 24 °C y el cielo está despejado.
```

**Una pregunta = dos llamadas a la API.** Un agente cuesta como mínimo el doble
que un chat, siempre. Y mira la entrada: 452 → 543. Subió, porque la vuelta 2
paga otra vez el menú de herramientas, la petición del modelo *y* el resultado.
Es el nivel 2 otra vez: todo lo que pasa se reenvía.

### Dos corridas comparadas: qué es determinista aquí

| | v1 entrada | v1 salida | v2 entrada |
|---|---|---|---|
| Medellín (A / B) | 452 / 452 | 73 / 73 | 543 / 543 |
| Bogotá (A / B) | 458 / 458 | 102 / **106** | 580 / **584** |
| Tokio (A / B) | 452 / 452 | 79 / 79 | 577 / 577 |

1. **Las entradas de vuelta 1 coincidieron al token** en las dos corridas. El
   menú de `tools` es texto fijo: pesa lo mismo siempre.
2. **La única diferencia se propagó exacta.** Bogotá varió 4 tokens de salida
   en la vuelta 1, y la entrada de la vuelta 2 varió esos mismos 4.

### Cuánto pesa el resultado de una herramienta

Restando `entrada(v2) − entrada(v1) − salida(v1)` queda el peso del
`tool_result`. Dio **lo mismo en las dos corridas**:

| Pregunta | Cuenta | Peso del resultado |
|---|---|---|
| Medellín | 543 − 452 − 73 | **18 tokens** |
| Bogotá | 580 − 458 − 102 | **20 tokens** |
| Tokio (mensaje de error) | 577 − 452 − 79 | **46 tokens** |

Es determinista porque ese texto lo escribió **tu función**, no el modelo.

**La consecuencia práctica:** lo que devuelve tu herramienta se reenvía en cada
vuelta siguiente. El mensaje de error de Tokio costó más del doble que un dato
normal. Una herramienta que devuelve un JSON gigante te sale cara para siempre,
no solo una vez. Recortar lo que devuelven las herramientas es trabajo de
harness, igual que recortar el historial en el nivel 2.

### El precio del agente

3 preguntas = 3.062 tokens de entrada + 590 de salida ≈ **$0,030**.

En el nivel 2, **6** preguntas costaron $0,0041. Aquí **3** costaron 7 veces más,
por dos multiplicadores apilados: el modelo (Opus 5 cuesta 5x Haiku a la
entrada) y el agente (dos llamadas por pregunta, la segunda más cara).

### El detalle que no se ve en los tokens

Las respuestas salieron en español rioplatense: *"¿Querés que consulte...?"*,
*"llevá paraguas"*, *"una campera"*.

Este script **no tiene `SYSTEM`**. Cuando no anclas la voz, el modelo elige una.
En un producto real eso es un bug que ve el usuario y que ninguna prueba
automática detecta. El script 3 sí tiene `SYSTEM`: compara.

### El caso que más enseña: Tokio

```
     -> ejecuto obtener_clima({"ciudad": "Tokio"})
        devolvio: No tengo datos de 'Tokio'. Ciudades disponibles: Bogota, Medellin, Cartagena.
  [vuelta 2] stop_reason=end_turn
RESPUESTA: No pude obtener el clima de Tokio: la herramienta que tengo solo cubre
ciudades de Colombia. Si te sirve, puedo darte el clima de alguna de esas tres.
```

La función **no lanzó una excepción**: devolvió un texto explicando el problema.
El modelo lo leyó y se recuperó solo, sin que nadie programara ese caso.

> **Regla:** una herramienta que lanza excepciones mata al agente. Una que
> devuelve texto lo deja pensar. Todo `except` en una herramienta debería
> terminar en un `return "Error: ..."`.

---

## 3.2b — Los dos errores que salieron al romperlo a propósito

Ejercicios 1 y 2, hechos y medidos. Los dos dan `BadRequestError` (HTTP **400**:
*petición mal formada* — culpa tuya, y por eso reparable). La petición se rechaza
**antes de llegar al modelo**: no se genera ni un token de esa llamada.

### Cómo se lee un traceback

**De abajo hacia arriba.** Las líneas del medio son las tripas del SDK. La última
línea es el error; las de arriba solo cuentan cómo llegaste ahí.

### Ejercicio 1 — `tool_use_id` inventado

```
messages.2.content.0: unexpected `tool_use_id` found in `tool_result` blocks:
toolu_inventado. Each `tool_result` block must have a corresponding `tool_use`
block in the previous message.
```

`messages.2.content.0` **es una dirección**, no texto decorativo. Son coordenadas
del JSON que mandaste:

| Índice | Qué es | Quién lo puso |
|---|---|---|
| `messages[0]` | la pregunta | tú |
| `messages[1]` | la petición del modelo (`tool_use`) | Claude |
| **`messages[2]`** | los resultados ← el problema | tú |

### Ejercicio 2 — sin el turno `assistant`

```
messages.0.content.1: unexpected `tool_use_id` found in `tool_result` blocks:
toolu_01D9HtV82NiE47whGKRBoW2i. Each `tool_result` block must have a
corresponding `tool_use` block in the previous message.
```

**Mensaje CERO.** Al quitar el `assistant`, el historial quedó con dos mensajes
`user` seguidos — y la API **fusiona los mensajes consecutivos del mismo rol** en
un solo turno:

```python
{"role": "user", "content": [
    {texto: "Que clima hace en Medellin?"},   # content[0]
    {tool_result...},                          # content[1]  ← aquí quedó
]}
```

> **Regla nueva:** mensajes consecutivos del mismo rol se fusionan. Tu lista de
> Python y lo que ve la API no tienen siempre la misma forma.

### La lección de método: el texto miente, la dirección no

Los dos ejercicios dieron **el mismo texto de error**, con causas opuestas:

| | Qué rompiste | Qué faltaba | Dirección |
|---|---|---|---|
| Ej. 1 | el id | el **emparejamiento** (había `tool_use`, con otro id) | `messages.2` |
| Ej. 2 | el turno `assistant` | el **`tool_use` entero** (no había ninguno) | `messages.0` |

En el ejercicio 2 el id era **real y correcto** — el problema era que no había
ningún `tool_use` antes. Un recibo de un pedido que nunca se hizo.

**Lee la coordenada antes que la frase.** Con un historial de 40 mensajes, esa
costumbre es la diferencia entre 2 minutos y 2 horas.

### Y el detalle que se repite en todo bucle agéntico

El bug se escribe en la vuelta 1. **El error aparece en la vuelta 2**, cuando ese
historial por fin se manda. El síntoma va siempre un paso por delante de la
causa. Y mientras tanto ya pagaste la vuelta 1 completa sin obtener respuesta:
**un agente roto gasta antes de fallar.**

---

## 3.3 — Un agente con datos reales y dos herramientas

```powershell
python 03_agente_real.py
```

Dos cambios:

1. El clima sale de **Open-Meteo**, una API pública gratis y sin llave. Ahora sí
   es información que el modelo no podía tener de ninguna forma.
2. Hay **dos** herramientas: `obtener_clima` y `hora_utc`. Nadie le dice cuál
   usar.

### Lo que salió de verdad

| Pregunta | Qué eligió | Vueltas |
|---|---|---|
| "¿Qué hora es?" | `hora_utc` | 2 |
| "¿Qué clima hace en Bucaramanga?" | `obtener_clima` | 2 |
| "Compara Bogotá y Cartagena" | `obtener_clima` **dos veces, en la misma vuelta** | 2 |
| "¿Cuánto es 17 por 23?" | **ninguna** | 1 |

```
=== Compara el clima de Bogota y el de Cartagena.
  [vuelta 1] stop_reason=tool_use entrada=612 salida=111
     -> obtener_clima({"ciudad": "Bogotá"})
        Bogotá (Colombia): 21.1 C, despejado, viento 14.8 km/h.
     -> obtener_clima({"ciudad": "Cartagena"})
        Cartagena de Indias (Colombia): 31.2 C, nublado, viento 14.2 km/h.
  [vuelta 2] stop_reason=end_turn entrada=855 salida=118
```

### Lo que cambió entre dos corridas (con una hora de diferencia)

**Las cuatro entradas de vuelta 1 coincidieron al token:** 598, 610, 612, 605.
Cuarta confirmación de que la entrada es determinista.

Pero las entradas de **vuelta 2** no:

| | corrida A | corrida B | de dónde salió la diferencia |
|---|---|---|---|
| hora | 654 | 675 | la salida de v1 (28 vs 49): se propagó exacta, +21 |
| Bucaramanga | 714 | 709 | **el clima**: `parcialmente nublado` vs `nublado` |
| compara | 855 | 860 | **el clima**: `despejado`+`nublado` vs `casi despejado`+`llovizna debil` |

En Bucaramanga la salida de v1 fue **59 en las dos corridas** — la diferencia de
5 tokens no la puso el modelo, la puso el cielo.

> **Con una API real, el costo depende de datos que no controlas.** En el script
> 2 el peso del `tool_result` era fijo (18, 20, 46) porque salía de un
> diccionario. Aquí no se puede presupuestar exacto; solo se puede acotar cuánto
> devuelven las herramientas.

### El menú se paga siempre, se use o no

```
=== Cuanto es 17 por 23?
  [vuelta 1] stop_reason=end_turn entrada=605 salida=56
```

Ninguna herramienta usada. Y aun así **605 tokens de entrada**: la pregunta pesa
unos 10, los otros ~595 son el `SYSTEM` y las **dos descripciones**, que viajan
en cada llamada.

> El menú de `tools` es una **suscripción fija por llamada**. Cada herramienta
> que agregas la pagas en todas las preguntas, incluso en las que no tienen nada
> que ver. Con 2 herramientas son ~600 tokens; con 40, miles.

### El `SYSTEM` no arregló el dialecto

Predicción fallida: pusimos `SYSTEM` en este script esperando anclar la voz, y
volvió a salir *"si me **decís** tu ciudad"*.

El `SYSTEM` dice *"Responde en espanol"*. **"Español" no es una especificación**
— hay veinte españoles. Se pidió un idioma, no una variedad.

Y solo pasó en **1 de las 4** respuestas. Un bug que aparece el 25% de las veces
es peor que uno que aparece siempre: no lo detectas probando una vez. El arreglo
es una palabra (`"español de Colombia"`) y es el ejercicio 7.

### Tres hallazgos más de esa corrida:

1. **Dos peticiones en un solo turno.** El modelo pidió las dos ciudades a la
   vez, no una tras otra. Por eso el bucle recorre `respuesta.content` con un
   `for` en vez de buscar un solo bloque: puede haber varios. Si hubiera venido
   en vueltas separadas, el bucle también lo habría manejado.
2. **La multiplicación NO usó herramienta.** `stop_reason` fue `end_turn` en la
   vuelta 1. El modelo sabe multiplicar; no necesita ayuda y no la pidió. Tener
   herramientas disponibles no obliga a usarlas.
3. **Nadie programó esas decisiones.** No hay un solo `if` que diga *"si la
   pregunta menciona hora, llama a hora_utc"*. Lo único que existe son las
   `description` que escribiste. **Las descripciones son el programa.**

### El error de Windows que vas a ver (y ya está arreglado)

La primera corrida de `02_bucle.py` reventó así, después de haber funcionado:

```
UnicodeEncodeError: 'charmap' codec can't encode characters in position 70-71
```

El agente funcionó perfecto. Lo que falló fue **la pantalla**: la consola de
Windows imprime en `cp1252`, que no conoce el símbolo `°` ni los emojis que
Claude usó al responder. Por eso los tres scripts empiezan con:

```python
sys.stdout.reconfigure(encoding="utf-8")
```

Vale la pena grabarse el patrón: *el traceback apuntaba a `print`, no a la API*.
El error estaba en la última línea del programa, no en la lógica.

---

## Lo que este agente todavía NO tiene

Todo esto llega en el nivel 4, y es la diferencia entre un ejemplo y un producto:

- Si Open-Meteo se cae, **no reintenta**: solo reporta el error.
- No hay **tope de gasto** ni timeout global. `max_vueltas=6` es lo único que te
  protege de un bucle infinito, y es un número escrito a mano.
- No **pide permiso** antes de actuar. Con `obtener_clima` da igual; con una
  herramienta `borrar_archivo` no.
- No **guarda ningún registro**. Si mañana el agente hace algo raro, no hay forma
  de saber qué herramientas llamó.

---

## Ejercicios

1. ~~**Rompe el ticket.**~~ ✅ **hecho** — ver §3.2b
2. ~~**Quita el `assistant`.**~~ ✅ **hecho** — ver §3.2b
3. **La descripción es el programa.** En `03_agente_real.py`, cambia la
   `description` de `hora_utc` por algo vago como `"Devuelve informacion."` y
   vuelve a preguntar la hora. ¿La sigue usando?
4. **Una herramienta tuya.** Agrega `calcular(expresion)` que haga
   `eval(expresion)` y vuelve a preguntar "¿cuánto es 17 por 23?". ¿Ahora sí la
   usa? ¿Por qué antes no? *(Y de paso: `eval` con texto que viene de un modelo
   es una idea terrible en producción. Piensa por qué.)*
5. **Cuenta la factura.** Suma la entrada de las dos vueltas de una pregunta y
   compárala con lo que costaría la misma pregunta sin herramientas. ¿Cuánto te
   cobra el menú de `tools` solo por existir?
6. **Fuerza una vuelta extra.** Inventa una pregunta que obligue a dos vueltas de
   herramientas seguidas (no dos herramientas en la misma vuelta). ¿Lo lograste?
7. **Ancla la voz.** En `03_agente_real.py`, cambia el `SYSTEM` de
   `"Responde en espanol"` a `"Responde en espanol de Colombia"`. Corre las 4
   preguntas **dos o tres veces**. ¿Desapareció el voseo? (Ojo: como aparecía
   solo 1 de cada 4 veces, una corrida limpia no prueba nada. Este ejercicio es
   en realidad una probadita del nivel 5: cómo se prueba algo que no responde
   igual dos veces.)
8. **Mide la suscripción.** Corre "¿cuánto es 17 por 23?" con `tools=[]` y
   compara la entrada contra los 605 tokens de la corrida con dos herramientas.
   Eso es lo que cuesta tener el menú abierto.

---

## Lo que ya sabes

- La **estructura** de la respuesta también varía entre corridas: el mismo script
  devolvió 1 bloque una vez y 2 la siguiente, porque el modelo decidió pensar.
  `content[0]` a ciegas es un bug que solo aparece a veces.
- El modelo **no ejecuta nada**. Solo escribe peticiones. Quien ejecuta es tu
  código, y eso es el harness.
- Una herramienta es un **diccionario con `name`, `description` e `input_schema`**,
  no una función. La función vive aparte, en tu Python.
- `stop_reason: "tool_use"` es la señal de que el bucle debe seguir;
  `"end_turn"` es la de que terminó.
- El bucle agéntico: **pide → ejecutas → devuelves → responde**. Se repite hasta
  que deja de pedir, y siempre con un tope de vueltas.
- Al devolver: se guarda `respuesta.content` **entero**, el `tool_use_id` debe
  ser idéntico, y todos los resultados van en **un solo** mensaje `user`.
- Un **400 / `BadRequestError`** es culpa tuya y trae una **dirección**
  (`messages.N.content.M`). Léela antes que la frase: el mismo texto de error
  puede tener causas opuestas.
- **Mensajes consecutivos del mismo rol se fusionan** del lado de la API.
- En un bucle, el error aparece **una vuelta después** de donde lo escribiste.
- Un agente cuesta **como mínimo el doble** que un chat: dos llamadas por
  pregunta, y la segunda es más cara.
- **Lo que devuelve tu herramienta se reenvía en cada vuelta siguiente**, y pesa
  siempre lo mismo (lo escribió tu función, no el modelo). Devolver poco y
  limpio es una decisión de costo, no de estilo.
- **Sin `SYSTEM` no hay ancla de voz**: el modelo elige dialecto y tono por su
  cuenta, y puede cambiar entre corridas. Y un `SYSTEM` vago tampoco basta:
  *"responde en español"* no especifica **cuál** español.
- El **menú de `tools` se paga en cada llamada**, se use o no. Agregar
  herramientas no es gratis.
- Con una API real, **el peso del `tool_result` ya no es determinista**: depende
  de datos del mundo que tú no controlas.
- Las herramientas deben **devolver texto de error**, nunca lanzar excepciones.
- El modelo decide solo qué herramienta usar, cuántas veces, o ninguna. **Las
  descripciones son el programa.**
- Este mismo bucle, con otras herramientas, es Claude Code.
