# Nivel 4 — El harness de verdad

En el nivel 3 construiste un agente. **Funciona.** Este nivel no lo hace más
inteligente: lo hace **confiable**, que es una cosa distinta y es la que se cobra.

Antes de empezar, desde la raíz:

```powershell
.\.venv\Scripts\Activate.ps1
cd 04-harness-real
```

---

## La idea, antes del código

Tu agente del nivel 3 funcionaba porque **nada salió mal**. Open-Meteo respondió
siempre. El wifi nunca se cayó. El modelo nunca pidió veinte herramientas seguidas.
Y nadie le dio una herramienta capaz de borrar cosas.

**Analogía:** un carro con motor y ruedas ya anda. Lo que lo convierte en un carro
que sacas a la calle son los frenos, el cinturón, el limpiaparabrisas y el
odómetro. Ninguna de esas piezas lo hace avanzar. Todas existen para el momento
en que algo salga mal — y algo va a salir mal.

El nivel 3 dejó escrita la lista de lo que faltaba, al final de `03_agente_real.py`:

> - no reintenta si la red falla, solo reporta el error
> - no tiene timeout global ni tope de gasto
> - no pide permiso antes de actuar
> - no guarda ningún registro de lo que hizo

Este nivel es esa lista, tachada.

---

## 4.1 — Los errores tienen nombre y apellido

```powershell
python 01_errores.py
```

Este script provoca **cinco fallas a propósito** y mira qué lanza cada una.
No cuesta nada: ninguna de las cinco llega a generar tokens.

### La corrida real

```
=== 1. Llave mala
    AuthenticationError (HTTP 401) — la llave no sirve
    reintentar? NO. invalid x-api-key  [request_id: req_011CdV34h8bX...]
=== 2. Modelo que no existe
    NotFoundError (HTTP 404) — ese modelo o esa ruta no existe
    reintentar? NO. model: claude-opus-9-mil  [request_id: req_011CdV34kB...]
=== 3. max_tokens absurdo
    ValueError — el SDK se nego a mandar la peticion
    reintentar? NO, no salio de tu maquina. Streaming is required for
    operations that may take longer than 10 minutes
=== 4. Parametro que este modelo ya no acepta
    BadRequestError (HTTP 400) — tu peticion esta mal armada
    reintentar? NO. `temperature` is deprecated for this model.
=== 5. Sin red (dominio inexistente)
    APIConnectionError — no hubo respuesta, ni siquiera un error
    reintentar? SI. causa: ConnectError
```

**Esta es la primera cosa determinista del curso.** Las cinco clasificaciones
salieron idénticas en dos máquinas distintas. Llevabas tres niveles midiendo que
nada se repite — pero aquí **el modelo nunca genera nada**, las cinco peticiones
mueren antes. Lo no determinista siempre fue *lo que produce el modelo*; la
infraestructura de alrededor sí es predecible. Eso es justo lo que hace posible
el nivel 5: **el harness se puede probar de forma determinista aunque el modelo
no.** (Lo único que cambia entre corridas es el `request_id`.)

### Reintentar o no reintentar

| Excepción | HTTP | ¿Reintentar? | Por qué |
|---|---|---|---|
| `ValueError` | — | **No** | Ni salió de tu máquina |
| `AuthenticationError` | 401 | **No** | Tu llave está mala. En 5 minutos sigue mala |
| `NotFoundError` | 404 | **No** | Ese modelo no existe hoy ni mañana |
| `BadRequestError` | 400 | **No** | Tu petición está mal armada |
| `RateLimitError` | 429 | **Sí**, esperando | Vas muy rápido |
| `InternalServerError` | 5xx | **Sí** | Se cayó el servidor de Anthropic |
| `APIConnectionError` | — | **Sí** | Se cayó la red |

Los cuatro primeros son **culpa tuya y permanentes**. Los tres últimos son
**ajenos y temporales**. Reintentar un 401 es esperar a que tu llave se arregle sola.

### Lo que no está en la tabla

**Hay tres fronteras, no una.** El caso 3 murió **en tu máquina** (el SDK revisó
antes de mandar). El caso 5 murió **en la red** (nunca hubo servidor). Los casos
1, 2 y 4 murieron **en el servidor** (hubo respuesta, con código HTTP). Casi el
mismo síntoma, tres sitios distintos donde buscar.

**El caso 3 fue una sorpresa mientras escribía este nivel.** Yo esperaba un 400
del servidor por pedir 99 millones de tokens. Lo que salió fue un `ValueError`
normal de Python: el SDK calcula cuánto tardaría esa respuesta, ve que pasa de
10 minutos y **se niega a mandarla**. La petición nunca existió. Por eso el
caso 4 está en el script: para tener también un 400 de verdad, del servidor, y
poder comparar los dos.

**`APIConnectionError` no tiene `status_code`.** Todos los demás heredan de
`APIStatusError`, que existe *porque hubo una respuesta HTTP*. En el caso 5
nunca hubo respuesta. Si escribes `except anthropic.APIStatusError` creyendo que
atrapa todo, el día que se caiga el wifi tu programa revienta igual.

**El orden de los `except` es el programa.** Van de específico a general. Si
mueves `APIStatusError` arriba, los casos 1, 2 y 4 caen ahí y pierdes justo la
información que necesitabas para arreglarlos.

**El mensaje limpio no está en `e.message`.** Ahí viene el JSON crudo entero
(`Error code: 401 - {'type': 'error', ...}`). La primera versión de este script
lo cortaba con `e.message[:80]` y el corte caía **a mitad del JSON**, justo antes
del dato útil. Era el mismo defecto de `texto.strip()[:30]` del nivel 1: *el
script mutila el dato y luego culpas al servidor*. El SDK ya te da el JSON
parseado en **`e.body`**; la función `motivo()` entra ahí y saca
`body["error"]["message"]`.

**De ahí salió gratis el `request_id`.** Cada petición que llega al servidor
tiene un número (`req_011CdV34h8bX...`). Es lo que le das a soporte de Anthropic
para que encuentren tu petición exacta. Estaba en el JSON desde siempre,
escondido detrás del corte.

**El mensaje de error no siempre sirve; la clase sí.** Compara el caso 2
(`model: claude-opus-9-mil` — solo repite lo que mandaste) con el caso 4
(`` `temperature` is deprecated for this model `` — te dice qué hacer). Los
mensajes son de calidad desigual y el proveedor los cambia sin avisar. Por eso
el harness clasifica por **clase de excepción**, nunca leyendo el texto del
mensaje.

---

## 4.2 — Reintentos y timeouts: el SDK ya lo hacía

```powershell
python 02_reintentos.py
```

Tarda ~30 segundos, casi todos esperando a propósito.

### A. Un error temporal sí se reintenta

Mismo error (no hay servidor), cambiando cuántos reintentos permitimos.
Dos corridas, en dos máquinas y dos redes distintas:

| `max_retries` | Corrida A | Corrida B |
|---|---|---|
| 0 | 0.22 s | 0.31 s |
| 1 | 0.39 s | 0.50 s |
| 2 | **1.34 s** ← el valor por defecto | 1.34 s |
| 3 | 3.39 s | 3.00 s |

El error es idéntico en los cuatro. Lo que crece es el **tiempo**, porque entre
intento e intento el SDK espera cada vez más (espera exponencial).

**Los números no se repiten; la forma sí.** Una red más lenta desplaza todo
hacia arriba, pero el orden y las proporciones aguantan. Eso es lo reproducible
de una medición de tiempos, y por eso este script se lee comparando filas entre
sí, no contra un número fijo.

> El `1.34 s` idéntico en ambas corridas **es casualidad** — los otros seis
> números difieren. Conviene notarlo porque en este curso ya hubo coincidencias
> al token que **no** eran casualidad (las entradas deterministas de los niveles
> 2 y 3). Aquellas tenían una causa mecánica: el texto de entrada era el mismo.
> Aquí no hay ninguna razón para que dos redes distintas coincidan.

**Y no imprimió nada mientras reintentaba.** Lo hace en silencio.

> **Esto ya te estaba pasando.** `max_retries=2` es el valor de fábrica. Cada
> `messages.create()` que escribiste en los niveles 1, 2 y 3 podía hacer **hasta
> 3 peticiones**, no una. Nunca lo viste porque nunca falló nada.

### B. Un error permanente no se reintenta

| Configuración | Corrida A | Corrida B |
|---|---|---|
| `max_retries=5`, llave mala | 0.39 s | 0.41 s |

Pedimos 5 reintentos y tardó lo que tarda **una** petición. El SDK sabe que un
401 no se arregla esperando. Reintenta 408, 409, 429, 5xx y errores de red;
todo lo demás lo lanza de una.

**Cómo se sabe que no reintentó:** comparándolo con la fila de arriba. Con 3
reintentos, la sección A tardó 3 segundos. Aquí pedimos 5 y tardó 0.41 s — el
mismo orden que `max_retries=0`. Una sola ida y vuelta. El número solo significa
algo **al lado de otro número**.

### C. El timeout se multiplica

| Configuración | Corrida A | Corrida B |
|---|---|---|
| `timeout=1s`, `max_retries=0` | 1.00 s | 1.02 s |
| `timeout=1s`, `max_retries=2` | **4.20 s** | 4.36 s |

`timeout=1s` significa **1 segundo por intento**, no 1 segundo en total.

### Esta sección mide la espera del SDK mejor que la A

En la sección A no puedes separar dos cosas: lo que tarda cada intento en fallar
y lo que el SDK espera entre intentos. Van sumadas.

Aquí sí, porque **cada intento cuesta exactamente 1.00 s** — lo fija el timeout,
no la red:

```
3 intentos × 1.00 s de timeout  =  3.00 s
medido                          =  4.36 s
                                  ───────
espera del SDK entre intentos   =  1.36 s   (repartida en 2 pausas)
```

En la otra corrida ese resto dio **1.20 s**. Casi igual en dos redes distintas —
y tiene sentido: las esperas son un `sleep` que decide el SDK, no algo que
dependa de tu conexión.

Es la misma técnica de resta con la que en el nivel 2 se aisló el peso de las
preguntas: `entrada − (entrada previa + salida previa)`. **Cuando no puedes
medir algo directamente, fija todo lo demás y réstalo.**

### El error cambió de nombre y aun así se reintentó

La sección A lanza `APIConnectionError`; la C lanza **`APITimeoutError`**. Dos
nombres, dos secciones — y las dos se reintentaron igual, porque
`APITimeoutError` **hereda de** `APIConnectionError`.

En el script 1 aprendiste que los `except` van de específico a general. Aquí se
ve **para qué sirve la parte general**: atrapa hijos que no sabías que existían.
Por eso `REINTENTABLES` no lista `APITimeoutError` — ya está cubierto.

> **Peor caso = `timeout × (max_retries + 1)` + las esperas entre intentos.**
> Con los valores de fábrica del SDK eso son **10 minutos × 3 = media hora**.
> Si tu agente le responde a un usuario, media hora no es un timeout: es un cuelgue.
> Los dos números se eligen juntos, nunca por separado.

### D. Tu propio reintento

El SDK reintenta **la llamada**. Tú reintentas **la operación**: una vuelta
entera del bucle, con su herramienta, su log y su descuento de presupuesto.
El SDK no sabe nada de eso.

Tres detalles de la función `con_reintentos()`:

- **Usa las clases de excepción**, no una lista de códigos HTTP escrita a mano.
- **La espera crece** (2 s, 4 s, 8 s). Si el servidor está saturado, volver cada
  segundo es empujar a alguien que ya se está cayendo.
- **Le suma un número al azar** (*jitter*), para que mil programas que fallaron
  en el mismo instante no vuelvan todos juntos en el mismo segundo.

> ⚠️ **Si pones el tuyo, baja el del SDK.** 3 reintentos tuyos × 3 del SDK = **9
> peticiones** y el triple de factura. Por eso `03_harness.py` usa
> `max_retries=0` en el cliente.

---

## 4.3 — El harness completo

```powershell
python 03_harness.py
```

**Es interactivo:** te va a pedir permiso antes de borrar. Responde `s` o `n`.

Mismo agente del clima, con seis piezas nuevas alrededor:

| Pieza | Para qué |
|---|---|
| timeout + reintentos | que un problema ajeno no cuelgue tu programa |
| errores tipados | reintentar lo temporal, cortar lo permanente |
| **presupuesto** en dólares | que un bucle no te vacíe la cuenta |
| **tope de vueltas** | que un bucle no sea infinito |
| **permisos** | que el modelo no decida solo lo irreversible |
| **registro** JSONL | poder explicar después qué fue lo que pasó |

El script crea una carpeta `caja/` con dos archivos de mentira, para que la
herramienta de borrar tenga algo real que borrar sin tocar nada tuyo.

### La corrida real (permiso concedido)

```
=== Borra el archivo borrador.txt, ya no lo necesito.
  vuelta 1: stop_reason=tool_use  gastado=$0.0152

     PERMISO: el agente quiere ejecutar borrar_archivo({"nombre": "borrador.txt"})
     Lo dejas? [s/n] s
     borrar_archivo({"nombre": "borrador.txt"})  [autorizada por el usuario]
       -> Borrado 'borrador.txt'.
  vuelta 2: stop_reason=end_turn  gastado=$0.0204
RESPUESTA: Listo, ya borré borrador.txt de tu caja. Recuerda que esa acción
no se puede deshacer.
```

### La misma corrida, diciendo que no

```
     Lo dejas? [s/n] n
     borrar_archivo({"nombre": "borrador.txt"})  [rechazada por el usuario]
       -> PERMISO DENEGADO: el usuario no autorizo borrar_archivo.
  vuelta 2: stop_reason=end_turn
RESPUESTA: No pude borrarlo: el sistema negó el permiso porque la acción no
está autorizada. Si querés, autorizá el permiso de borrado y lo intento de nuevo.
```

**El archivo sigue ahí.** Y el modelo lo dice bien, porque se enteró.

### Dónde vive cada decisión

**El permiso no está en la descripción de la herramienta.** Está en el
diccionario `PERMISOS`, en tu código:

```python
PERMISOS = {
    "obtener_clima": "permitir",
    "hora_utc": "permitir",
    "listar_archivos": "permitir",
    "borrar_archivo": "preguntar",
}
```

Lo que el modelo *lee*, el modelo lo puede ignorar — o lo pueden convencer de
ignorarlo. Lo que está en tu `if`, no. Además, lo desconocido se prohíbe:
`PERMISOS.get(nombre, "prohibir")`. Si mañana añades una herramienta y se te
olvida darle política, no corre.

**Dos candados para la misma puerta.** Aparte del permiso, `borrar_archivo()`
se defiende sola: comprueba que el archivo esté dentro de `caja/`. Si el modelo
pidiera `../../.env`, eso lo para. El permiso lo puede dar un humano distraído.

**Cuando dices que no, el modelo tiene que enterarse.** Le devolvemos
`"PERMISO DENEGADO: el usuario no autorizo borrar_archivo."` como resultado de
la herramienta. Si le devolvieras silencio o texto vacío, seguiría creyendo que
se hizo y le diría al usuario *"listo, ya lo borré"*. **Un agente que miente sin
querer sigue mintiendo.**

**El presupuesto se revisa antes de gastar**, no después. Revisarlo después es
contar el dinero que ya no tienes.

### El registro

Una línea de JSON por evento, en `registro.jsonl`:

```json
{"hora": "...", "evento": "llamada_api", "intento": 1, "segundos": 4.31,
 "entrada": 724, "salida": 38, "costo_usd": 0.00457, "acumulado_usd": 0.00457,
 "stop_reason": "tool_use"}
{"hora": "...", "evento": "herramienta", "nombre": "listar_archivos",
 "entrada": {}, "permiso": "permitida por politica",
 "resultado": "En la caja hay: borrador.txt, notas.txt."}
```

El formato `.jsonl` (una línea = un JSON) se lee con los ojos, se puede abrir a
mitad de escritura y se procesa línea por línea sin cargar el archivo entero.
Es lo que usa media industria.

Costo de la corrida completa: **$0.0319** de un tope de $0.10.

### Las dos corridas del estudiante (sesión 7)

Corrió el script dos veces, una concediendo y otra negando, y de comparar los
dos `registro.jsonl` salieron cuatro cosas que en pantalla no se veían.

| | con `s` | con `n` |
|---|---|---|
| Total | $0.0323 | $0.0328 |
| `borrador.txt` al final | borrado | **sigue ahí** |

**1. Decir que NO cuesta más que decir que sí.** La vuelta 2 de la pregunta del
borrado, desglosada con el registro:

| | entrada | salida | costo |
|---|---|---|---|
| con `s` | 823 | 35 | $0.00499 |
| con `n` | **838** | **54** | $0.00554 |

Los dos lados se mueven: `PERMISO DENEGADO: el usuario no autorizo
borrar_archivo.` pesa **15 tokens más** que `Borrado 'borrador.txt'.`, y el
agente gastó **19 tokens más** en explicarse. La cuenta cuadra exacta:
15 × $5/M + 19 × $25/M = **$0.00055**, que es la diferencia medida.

→ **El camino de error cuesta más que el camino feliz.** Cuenta al presupuestar.
Y de paso queda confirmado el precio de Opus 5 con aritmética propia, no de
memoria: **$5 por millón de entrada, $25 por millón de salida.**

**2. Las entradas de vuelta 1 coincidieron al token en las dos corridas**
(724, 735, 736 en las tres preguntas). Séptima confirmación del curso.
Y la única divergencia se propagó exacta: la pregunta 3 dio 93 vs 94 tokens de
salida en v1, y 934 vs 935 de entrada en v2. **El mismo token.**

**3. Este harness no tiene memoria entre preguntas** — y eso no se había dicho.
Mira las entradas de vuelta 1: 724, 735, 736. Si hubiera historial, la pregunta 3
arrancaría en ~1.600. Cada pregunta es una conversación nueva. Es una decisión de
diseño, no un bug, y es la razón de que el costo por pregunta se mantenga plano
en vez de dispararse como en el nivel 2.

**4. El hallazgo que solo existe en el registro.** Dos líneas seguidas:

```
11:03:14  llamada_api   segundos: 3.98
11:04:01  herramienta   borrar_archivo
```

**47 segundos.** La API tardó 3.98; los otros 43 fue el humano decidiendo si
daba el permiso. Si mañana alguien reporta que "el agente es lentísimo", el
registro dice que el modelo no tuvo la culpa. Ese diagnóstico es imposible sin
el archivo. Es la primera vez en el curso que la observabilidad responde algo
que ninguna otra pieza podía responder — y es el anticipo del **nivel 7**.

(`"intento": 1` en las 12 llamadas: ningún reintento se disparó. Ese campo está
ahí para el día que diga `3`.)

### Hallazgo de esta corrida: el dialecto volvió

Mira otra vez la respuesta del permiso denegado: **"Si querés, autorizá"**.
Eso es español rioplatense, otra vez — y esta vez el `SYSTEM` **sí** dice
*"Responde en español de Colombia"*.

En el nivel 3 la conclusión fue que el `SYSTEM` decía solo *"en español"* y por
eso no anclaba la variedad (ver ejercicio 7 del nivel 3). **Esa explicación se
queda corta:** con el ancla puesta, apareció igual en 1 de 3 respuestas de esta
corrida. Un defecto intermitente no se arregla probando una vez, y **tampoco se
diagnostica probando una vez**. Medirlo de verdad es material del nivel 5.

**Confirmado en otra máquina, y además se mueve de sitio.** En las dos corridas
del estudiante volvió a salir 1 de 3 — pero no en la misma respuesta: con `s`
apareció en la segunda (*"Recordá que esta acción no se puede deshacer"*) y con
`n` en la primera (*"¿Querés que haga algo con alguno de ellos?"*).

→ El defecto es intermitente **y cambia de posición**. Una corrida limpia no
prueba nada, y una corrida sucia tampoco te dice dónde mirar. Es el argumento
entero del nivel 5, servido por el propio material del nivel 4.

---

## 4.4 — Streaming

```powershell
python 04_streaming.py
```

La misma pregunta, pedida de dos formas. **La misma pregunta** es toda la
metodología del experimento: si la cambias, no sabes si la diferencia la puso el
streaming o la puso la pregunta.

Dos corridas, en dos máquinas distintas:

| Forma | Primera palabra | Todo | Salida |
|---|---|---|---|
| **Corrida A** — sin streaming | 11.9 s | 11.9 s | — |
| **Corrida A** — con streaming | **8.6 s** | 17.0 s | 787 tok |
| **Corrida B** — sin streaming | 13.2 s | 13.2 s | 691 tok |
| **Corrida B** — con streaming | **5.8 s** | 13.9 s | 814 tok |
| **Corrida C** *(orden invertido)* — con streaming | **7.1 s** | 15.2 s | 802 tok |
| **Corrida C** *(orden invertido)* — sin streaming | 12.3 s | 12.3 s | 696 tok |

Sin streaming, la primera palabra y el final son **el mismo instante**: todo
aparece de golpe. Por eso la primera columna repite el número — no es un
descuido del script, es el concepto escrito como código.

**Los números no se repiten entre máquinas (1.38x contra 2.3x de adelanto), pero
la dirección sí.** Es la misma lectura del script 2: se compara la forma, no el
valor.

### Cómo se llaman estas cosas

Las dos columnas que estás midiendo tienen nombre propio en la industria, y
conviene aprenderlos porque los vas a ver en toda la documentación de LLMs.

| Nombre | Qué mide | Lo que mediste |
|---|---|---|
| **TTFT** — *Time To First Token* | cuánto tarda en aparecer lo primero | 8.6 / 5.8 / 7.1 / **4.23 s** |
| **TPOT** — *Time Per Output Token* | cuánto tarda cada token después del primero | ~52–59 tok/s (es su inverso) |
| **ITL** — *Inter-Token Latency* | el hueco entre un token y el siguiente | los huecos del stream crudo |
| **Latencia end-to-end** | de la petición a la última palabra | 12.1 s |

Y la fórmula que las amarra:

```
latencia total  =  TTFT  +  (tokens de salida × TPOT)
```

Léela una vez más, porque explica todo el nivel: **el streaming no toca ninguno
de los dos sumandos.** No baja el TTFT ni el TPOT. Lo único que cambia es que
puedes *empezar a leer* después del primer sumando en vez de esperar a los dos.

⚠️ **Y con modelos que razonan hay dos TTFT distintos.** Hay que decir cuál:

| | Cuándo | Qué es |
|---|---|---|
| TTFT "del sistema" | **1.97 s** | el primer token de cualquier tipo — aquí, `thinking` |
| TTFT "del usuario" | **4.23 s** | el primer token de **texto**, lo único que la persona ve |

`text_stream` mide el segundo. Mezclarlos en la misma tabla es cómo se publica un
número de latencia que nadie puede reproducir.

> No confundas TTFT con **TTFB** (*Time To First Byte*), que es la métrica de
> redes de siempre: el primer byte que llega por el socket. En tu corrida es el
> `message_start`, a los **1.95 s**.

### Los totales no son comparables — pero se pueden normalizar

13.2 vs 13.9 parece "casi igual", y esa lectura está mal hecha: **no midieron lo
mismo.** La respuesta con streaming fue de 814 tokens y la otra de 691.

Divide y quedan comparables:

| Corrida | sin streaming | con streaming |
|---|---|---|
| B | 691 / 13.2 = **52.3 tok/s** | 814 / 13.9 = **58.6 tok/s** |
| C | 696 / 12.3 = **56.6 tok/s** | 802 / 15.2 = **52.8 tok/s** |

**La dirección se invierte entre corridas.** Las cuatro llamadas caen entre 52 y
59 tok/s sin patrón: **el rendimiento es el mismo dentro del margen de error.**

> ⚠️ **Corrección.** La primera versión de esta sección decía *"con streaming se
> generó más texto por segundo"*, con los datos de la corrida B únicamente. Era
> el error del nivel 1 otra vez: **sacar una dirección de una sola medición.**
> La corrida C la invirtió. La conclusión honesta es la de arriba — el streaming
> no cuesta velocidad real —, que es más débil y es la que aguanta.

→ **Cuando dos mediciones no son comparables, busca una razón en vez de comparar
los totales crudos.** Es la misma técnica de la resta del backoff en §4.2. Pero
la razón tampoco significa nada con n=1.

### ¿Y qué pasa en esos 5.8 segundos de silencio?

Con streaming la pantalla **igual estuvo quieta 5.8 s**. ¿Por qué, si los
pedazos deberían llegar enseguida?

**Hipótesis:** `stream.text_stream` entrega **solo bloques de texto**. Opus 5
puede empezar generando un bloque `thinking` (se vio en el nivel 1 y en el 3).
Mientras razona, el modelo está generando y transmitiendo — pero `text_stream`
no suelta nada, porque eso no es texto.

Si es cierto: **el streaming no elimina la espera en blanco, la reduce.** Con un
modelo que razone mucho podrías tener streaming y aun así una pantalla quieta.

**Tres cosas comprobadas en la documentación oficial del SDK** (no de memoria):

1. **En Opus 5 el razonamiento está encendido por defecto.** Si no pasas el
   parámetro `thinking`, el modelo razona igual. Este script no lo pasa.
2. **`text_stream` entrega solo texto**, confirmado. Para ver los demás bloques
   hay que iterar el stream crudo.
3. Y la frase que cierra el caso, sobre el valor por defecto de `display`:
   > *"si transmites el razonamiento a los usuarios, el valor por defecto
   > **parece una pausa larga antes de la salida**"*

   Está descrito como un efecto conocido.

**Matiz que hay que saber:** `display` viene en `"omitted"` por defecto. Los
bloques `thinking` **llegan por el stream con el texto vacío** — el modelo razona
y se te cobra igual, simplemente no te muestran el contenido. Para verlo:
`thinking={"type": "adaptive", "display": "summarized"}`. Nunca ves el
razonamiento crudo, solo un resumen.

### Medido (ejercicio 8): confirmada, y a medias

Se comprobó iterando el stream crudo con cronómetro (`04b_eventos.py`).

```
  1.95s  message_start
  1.97s  EMPIEZA bloque tipo 'thinking'
  3.77s     <- primer pedazo de tipo 'thinking_delta'
  4.20s     <- primer pedazo de tipo 'signature_delta'
  4.22s  TERMINA bloque
  4.23s  EMPIEZA bloque tipo 'text'
  4.23s     <- primer pedazo de tipo 'text_delta'
 12.06s  TERMINA bloque
```

**El mecanismo es exactamente el de la hipótesis.** El bloque `thinking` va
primero y el de texto no empieza hasta que aquel cierra; `text_stream` habría
soltado su primer trozo a los 4.23 s porque hasta ese instante **no existía un
solo token de texto**. La respuesta final lo confirma por otra vía:
`content` trae `['thinking', 'text']`.

**Pero la hipótesis estaba incompleta.** El silencio se parte en dos:

| Tramo | Duración | Qué es |
|---|---|---|
| 0 → 1.95 s | **1.95 s** | nada todavía: abrir conexión + petición + arranque del servidor |
| 1.95 → 4.23 s | **2.28 s** | el bloque `thinking` |
| 4.23 → 12.06 s | 7.83 s | el texto llegando |

Decir *"el silencio es el thinking"* era falso a medias: **el thinking es la
mitad del silencio.** La otra mitad es que la respuesta aún no había empezado a
existir. Y encaja con §4.4: el ~1 s de apertura de conexión medido en el
ejercicio 9 vive dentro de esos 1.95 s. **El número de un experimento apareció
dentro de otro.**

→ Es L4.13 otra vez —*una hipótesis que explica lo que viste puede seguir siendo
incompleta*— pero atrapada al medirla, no tres niveles después.

**Dos detalles que solo se ven aquí:**

- **1.8 s entre que el bloque `thinking` se anuncia y llega su primer pedazo.**
  El `content_block_start` dice "viene razonamiento", y el contenido tarda. Ni
  con el stream crudo llega algo todo el tiempo: hay huecos reales.
- **`signature_delta`**: cada bloque `thinking` viene **firmado**. Sirve para
  verificar que no lo modificaste si se lo devuelves al modelo en otro turno. Es
  integridad, no contenido.

### Y esto explica la variación de "primera palabra"

A lo largo de las corridas dio **8.6 · 5.8 · 7.1 · 4.23 s**, sin explicación.

Ahora la hay: **el silencio dura lo que dure el razonamiento de esa corrida**, y
cuánto razona Opus 5 no es determinista (L3.14). Esta corrida pensó poco —el
resumen es una sola frase— y por eso el texto arrancó a los 4.23 s. No fue la
red: **fue que el modelo pensó menos.**

### Estás pagando razonamiento que casi no ves

`usage: 52 in / 654 out`. La respuesta son ~200 palabras ≈ 350 tokens; los otros
~300 fueron **pensamiento facturado**, del que `display: "summarized"` te muestra
un resumen de una línea.

Y las corridas anteriores lo pagaban igual: 691, 814, 802 y 696 tokens de salida
para la misma pregunta, con `display` en su valor de fábrica `"omitted"`.

> **El razonamiento nunca fue gratis ni opcional aquí: era invisible.** `display`
> decide si te lo enseñan, no si ocurre ni si se cobra. Un costo que no aparece
> en ningún log tuyo sigue estando en la factura.

### El sesgo de orden, medido (ejercicio 9)

La forma 1 corría **primera**, y la primera llamada del programa paga la apertura
de la conexión con la API — tiempo que la forma 2 ya no paga. Así que parte de la
ventaja del streaming podía no ser del streaming.

**Se midió invirtiendo el orden del script.** Con eso hay cuatro datos: dos
formas × dos posiciones.

| | corre **primera** | corre **segunda** |
|---|---|---|
| sin streaming | 13.2 s | 12.3 s |
| con streaming | 7.1 s | 5.8 s |

**Por filas — el costo de ir primero:**

```
sin streaming:  13.2 − 12.3  =  +0.9 s
con streaming:   7.1 −  5.8  =  +1.3 s
```

Dos mediciones independientes del mismo fenómeno, y casi coinciden: **abrir la
conexión cuesta alrededor de 1 segundo.** (La predicción escrita antes de correr
era "unos cientos de milisegundos". Se quedó corta al doble.)

**Por columnas — la ventaja real del streaming, con las dos formas en igualdad
de condiciones:**

```
ambas en la posición 1:  13.2 − 7.1  =  6.1 s
ambas en la posición 2:  12.3 − 5.8  =  6.5 s
```

Otra vez, dos caminos y casi el mismo resultado: **la ventaja del streaming es
~6.3 s**, no los 7.4 s del experimento sesgado. El orden le regalaba **un
segundo largo**.

→ La conclusión sobrevivió intacta y **la magnitud estaba inflada ~15%**. Eso es
exactamente para lo que sirve un control: no tumbó el resultado, lo corrigió.

> **La técnica, que vale más que el número:** cuando sospechas que la posición
> de una medición la contamina, **corre las dos en las dos posiciones.** La
> tabla de 2×2 te da el efecto y el sesgo por separado, leyendo filas y
> columnas. Y si el mismo número te sale por dos caminos distintos, deja de ser
> casualidad.

### El dialecto, aquí, no apareció

Las cuatro respuestas de las corridas B y C salieron en usted colombiano limpio.
Y no solo evitando el rioplatense — eligiendo léxico colombiano:

> *"le pide a un amigo que le traiga **un tinto**"* · *"se gastan **plata**"* ·
> *"el **freno de mano**"* · *"**Imagínese**"*

**Tinto** es café negro en Colombia y en ningún otro país hispanohablante.

| | Dónde va "español de Colombia" | Respuestas | Rioplatense |
|---|---|---|---|
| `03_harness.py` | en el `SYSTEM` | 9 | **3** |
| `04_streaming.py` | en el **mensaje del usuario** | 4 | **0** |

**Hipótesis:** una instrucción en el turno del usuario pesa más que la misma
instrucción en el `SYSTEM`.

Con 13 respuestas y dos prompts distintos **no prueba nada** — el experimento
correcto es el *mismo* prompt en las dos posiciones, N corridas, contando. Pero
la hipótesis aguantó una corrida más en vez de morirse, y eso ya la convierte en
el mejor candidato para el primer experimento del **nivel 5**.

### Un detalle que pasa desapercibido

La respuesta sin streaming terminó con un emoji (🕐) y **no reventó nada**. En el
nivel 3 eso mismo mató el programa con `UnicodeEncodeError`, porque la consola de
Windows es `cp1252`. La línea `sys.stdout.reconfigure(encoding="utf-8")` está
haciendo su trabajo en silencio. **Un arreglo bueno es el que no vuelves a notar.**

### Lo que costó de verdad

| | entrada | salida | costo |
|---|---|---|---|
| sin streaming | 52 | 691 | $0.0175 |
| con streaming | 52 | 814 | $0.0206 |
| | | | **$0.038** |

El docstring del script decía `~$0.02`. **Era un estimado mío, sin medir, y se
quedó corto por la mitad** — el mismo patrón del "5x" del nivel 1. Corregido en
el script con el número medido.

(52 tokens de entrada en las dos llamadas, idéntico. Otra vez.)

Tres cosas que no se ven en los números:

1. **`get_final_message()` te devuelve el objeto `Message` completo**, igual que
   `messages.create()`: `usage`, `stop_reason`, `content`. Hacer streaming no te
   quita información.
2. **Para respuestas grandes no es opcional.** El `ValueError` del script 1 era
   exactamente esto: el SDK se niega a hacer una petición sin streaming que
   calcule que va a tardar más de 10 minutos.
3. **Un stream se puede cortar a la mitad**: se cae la red y te quedas con media
   respuesta y ningún error claro. Ganas sensación de rapidez y pagas con un
   caso más que manejar. Todo en el harness es un intercambio.

---

## Ejercicios

1. **Rompe el presupuesto.** Baja `PRESUPUESTO_USD` a `0.01` en `03_harness.py`
   y corre. ¿En qué pregunta se detiene? ¿Qué le contesta al usuario? Mira qué
   quedó en `registro.jsonl`.
2. **Rompe el tope de vueltas.** Pon `MAX_VUELTAS = 1`. El agente pide una
   herramienta y nunca llega a responder. ¿Qué pasa? Ese es el mensaje que vería
   tu usuario un día real.
3. **Prohíbe algo.** Cambia `"obtener_clima": "permitir"` por `"prohibir"` y
   pregunta por el clima. Fíjate en qué hace el modelo con el rechazo: ¿lo dice,
   se lo inventa, intenta otra herramienta?
4. **Quita el aviso de denegación.** Cambia el texto `"PERMISO DENEGADO..."` por
   `""` (vacío) y niega el borrado. Mira si el modelo le dice al usuario que
   borró el archivo. Este ejercicio da miedo a propósito.
5. **Cuenta los reintentos escondidos.** En `01_errores.py`, quita
   `max_retries=0` del caso 5 y cronometra. ¿Cuánto tarda ahora en fallar?
6. **Lee tu propio registro.** Escribe un script de 10 líneas que abra
   `registro.jsonl` y sume `costo_usd` de todas las líneas con
   `evento == "llamada_api"`. Compáralo con el total que imprime el harness.
7. **Mata el wifi.** Desconecta el internet y corre `03_harness.py`. Es la
   prueba que quedó pendiente desde el nivel 3: ver el `except` de red
   ocurriendo de verdad, no imaginado.
8. ~~**¿Qué llega en el silencio del streaming?**~~ ✅ **HECHO** — ver §4.4 y
   `04b_eventos.py`. El mecanismo se confirmó; la hipótesis resultó **incompleta**
   (el thinking es solo la mitad del silencio) y de ahí salieron L4.25 y L4.26.
9. ~~**Invierte el orden.**~~ ✅ **HECHO** — ver §4.4. El sesgo resultó de ~1 s
   (medido dos veces) y la ventaja real del streaming bajó de 7.4 s a ~6.3 s.
   De aquí salió la técnica de la tabla 2×2 (L4.24).

---

## Lo que ya sabes

- Que el SDK **ya reintentaba** desde el nivel 1, en silencio, hasta 3 peticiones
  por cada `create()`.
- Que los errores se dividen en **temporales** (reintenta) y **permanentes**
  (arregla el código), y que las clases de excepción del SDK ya hacen esa división.
- Que un error puede morir en **tres sitios**: tu máquina, la red, o el servidor.
- Que el **timeout es por intento**, y que tu paciencia real es
  `timeout × (max_retries + 1)`.
- Que reintentos tuyos + reintentos del SDK se **multiplican**, no se suman.
- Que un agente serio necesita **un tope de gasto y un tope de vueltas**, porque
  un bucle roto gasta antes de fallar.
- Que los **permisos viven en tu código**, no en la descripción que lee el modelo,
  y que **negar en silencio hace que el agente mienta**.
- Que sin **registro** solo tienes tu memoria para explicar qué hizo el agente.
- Que **streaming** no acelera el total: acelera el arranque (**~6.3 s**, con el
  orden controlado), y es obligatorio para respuestas grandes.
- Que las métricas de latencia de un LLM se llaman **TTFT** (*Time To First
  Token*), **TPOT** (*Time Per Output Token*), **ITL** (*Inter-Token Latency*) y
  **latencia end-to-end**; que se amarran con
  `total = TTFT + (tokens × TPOT)`; y que el streaming **no baja ninguno de los
  dos sumandos** — solo te deja empezar a leer antes.
- Que con modelos que razonan hay **dos TTFT** y hay que decir cuál: el primer
  token de cualquier tipo (1.97 s) y el primero de texto (4.23 s), que es el
  único que la persona ve.
- Que **el silencio del streaming es mitad arranque y mitad razonamiento**, y que
  dura lo que dure el razonamiento de esa corrida — por eso el TTFT varió entre
  4.2 y 8.6 s sin que nadie cambiara nada.
- Que **pagaste razonamiento invisible todo el nivel**: `display` decide si te lo
  enseñan, no si ocurre ni si se cobra.
- Que para medir algo cuya posición lo contamina, **corres las dos cosas en las
  dos posiciones**: por filas sale el sesgo, por columnas el efecto limpio.
- Que **normalizar (tok/s) no arregla que n=1** — y que una diferencia medida una
  sola vez puede ser ruido con dirección inventada.
- Que **una hipótesis puede ser correcta en el mecanismo y aun así incompleta**
  en la causa.
