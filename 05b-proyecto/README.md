# Nivel 5b — Proyecto integrador: agente de divisas y TRM

> **Este nivel es distinto a todos los anteriores.** Los otros se leen y se corren.
> Este se **escribe desde archivos vacíos**. No trae código hecho.

---

## §5b.0 — Qué es un proyecto integrador

Aprender a manejar tiene dos partes. Una es la clase: el instructor va al lado y
te dice *"ahora el embrague", "ahora primera"*. La otra es el día que te dan las
llaves y tienes que ir del punto A al punto B tú solo. **Nadie te dice cuándo
frenar.**

Los niveles 0 al 5 fueron la clase. Este es el día de las llaves.

| Niveles 0–5 | Nivel 5b |
|---|---|
| El código ya existe; lo **lees y lo corres** | Empiezas con **archivos vacíos** |
| Cada nivel enseña **una** cosa nueva | Ninguna cosa nueva: **todas juntas** |
| La estructura del programa la decidí yo | La estructura es una **decisión tuya** |
| Si algo falla, el README dice qué esperar | Si algo falla, **no hay respuesta al lado** |

### Por qué existe

Porque **entender un programa y ser capaz de producirlo son dos habilidades
distintas**, y hasta el nivel 5 solo se practicó la primera. Es la diferencia
entre leer una receta y cocinar sin mirarla.

Y hay una razón práctica: cuando construyas los agentes de tu empresa, nadie te
va a dar un README. Vas a tener una carpeta vacía.

### Cómo se trabaja aquí — formato mixto

Decidido por el estudiante en la sesión 9, y la razón importa más que la regla:

- **Lo mecánico se dicta** literal: carpetas, `import`, estructura de archivos.
  No hay nada que aprender ahí.
- **Lo conceptual lo escribes tú**: el bucle, los frenos, los evals. Primero se
  dice **qué** y **por qué**, lo intentas, y después se compara con mi versión.

> **La razón:** si se dicta todo, terminas con un agente que funciona **y que no
> sabrías rehacer**. Sería el único nivel donde el código no pasó por tu cabeza.

---

## §5b.1 — Qué piezas entran, y de dónde sale cada una

Lo importante de un proyecto integrador: **no vas a aprender nada nuevo.** Todo
lo que necesitas ya está escrito en algún nivel. Lo que cambia es que te toca
sacarlo tú.

| Pieza | Viene del nivel | Qué aporta al agente de divisas |
|---|---|---|
| `client.messages.create()`, `usage`, `stop_reason` | **1** | La llamada básica y saber qué costó |
| Historial de mensajes | **2** | Que puedas decir *"y en euros?"* y sepa de qué hablas |
| El **bucle agéntico** a mano (`tool_use` → ejecutar → `tool_result` → repetir) | **3** | El corazón del programa. Sin esto no hay agente |
| `SYSTEM` con el dialecto anclado | **3 y 5** | Ya sabes que sin ancla sale rioplatense, y ya sabes **cuál** ancla funciona |
| Los **6 frenos**: timeout, errores tipados, presupuesto en dólares, tope de vueltas, permisos, registro JSONL | **4** | Que no se cuelgue media hora ni se gaste tu saldo |
| ⭐ **3 frenos que NO vienen de ningún nivel**: ¿existe la herramienta?, ¿acepta esos argumentos?, la red final | **ninguno** | Con 6 herramientas aparecen errores que con 1 no existían. **Único renglón sin nivel de origen: hay que inventarlo aquí** |
| `sys.stdout.reconfigure(encoding="utf-8")` | **3** | Windows con `°`, `€`, emojis |
| **Evals deterministas** | **5** | `100 × 3.205,80 = 320.580` se verifica con una resta |
| **LLM-as-judge / rúbrica** | **5** | *"¿dijo de qué fuente sacó la tasa?"* no se verifica con un `if` |
| `PRECIOS[MODELO]` en vez del precio suelto | **5 (L5.23)** | El bug que quedó armado en 6 scripts. Aquí se hace bien de entrada |

**Lo que hay que ver en esa tabla:** la columna del medio casi no tiene huecos.
Cada pieza tiene un nivel donde ya la corriste y donde ya la rompiste. Cuando te
trabes, la pregunta no es *"¿cómo se hace esto?"* sino **"¿en qué nivel vi
esto?"**.

⭐ **Y el único hueco enseña más que las nueve filas llenas** (se descubrió en la
sesión 15, construyéndolo). Un proyecto integrador no es solo juntar piezas
viejas: al juntarlas aparecen problemas que ninguna tenía por separado. El
agente del nivel 4 no necesitaba preguntarse *"¿existe esa herramienta?"*
porque solo tenía una.

---

## §5b.2 — Las cinco herramientas, y por qué son de tipos distintos

Este agente se podría hacer con **una sola** herramienta (`obtener_tasa`) y
funcionaría. Son cinco porque **cada una obliga a resolver un problema
diferente**.

| Herramienta | Tipo | Lo difícil de ella |
|---|---|---|
| `obtener_tasa(de, a)` | API en vivo | el dato cambia → cómo evaluar lo **no** determinista |
| `convertir(monto, de, a)` | cálculo puro, sin red | el modelo no debe calcular → cómo evaluar lo **sí** determinista |
| `trm_oficial(fecha)` | API con fecha, fuente autoritativa | **dos verdades a la vez**, y días sin dato |
| `historial(de, a, dias)` | serie de tiempo | el resultado es **grande** y se paga muchas veces |
| `guardar_reporte(...)` | **escribe en disco** | es **irreversible** → permisos |

### `obtener_tasa(de, a)` — API en vivo
Le pregunta a internet cuánto vale hoy el dólar. **El dato cambia entre
corridas**, así que no puedes escribir un eval que diga *"debe dar 3.205,87"*.
Es el caso más difícil de evaluar — y ya sabes por qué, desde el nivel 5.

### `convertir(monto, de, a)` — cálculo puro
Multiplica. Nada más. No toca internet. **Es el centro de todo el proyecto:**

> **La herramienta calcula. El modelo solo decide a cuál llamar.**

Un modelo de lenguaje predice el siguiente token; no calcula. Puede equivocarse
multiplicando. Y como esto es pura aritmética, es **100% determinista**: el eval
perfecto, y cuesta **$0.00** probarlo — igual que `00_probar_detector.py`.

### `trm_oficial(fecha)` — la fuente autoritativa
La TRM que publica la Superfinanciera de Colombia. Aquí aparece algo que ningún
nivel anterior tuvo: **dos fuentes que no coinciden, y las dos correctas.**
Ninguna está mal. Cuál sirve depende de para qué preguntas — si es para una
declaración de renta, la única válida es la oficial.

Segundo problema que trae: **¿qué pasa si pides la TRM de un domingo?** No
existe. Un agente serio tiene que responder algo sensato.

### `historial(dias)` — serie de tiempo
Devuelve los últimos N registros. Aquí vuelve el hallazgo de la sesión 4: **lo que
devuelve una herramienta se reenvía en cada vuelta siguiente**. 30 días en JSON
crudo es un texto grande que pagas otra vez, y otra. Te toca decidir qué recortar
antes de devolverlo. Es recortar historial del nivel 2, pero del lado de las
herramientas.

⚠️ **CORREGIDO en la sesión 13. Antes decía `historial(de, a, dias)`**, o sea el
histórico de cualquier par de monedas. **Eso no se puede hacer con las fuentes de
§5b.4**, y se ve al ponerlas al lado:

| Fuente | Qué tiene | Qué NO tiene |
|---|---|---|
| Mercado (er-api) | 166 monedas | **solo el día de hoy** |
| TRM (datos.gov.co) | 30 años de historia | **solo USD→COP** |

Una tiene las monedas y no el pasado; la otra tiene el pasado y una sola moneda.
→ **Este párrafo se escribió antes de elegir las fuentes.** No estaba mal
razonado: era *anterior a la información*. Un plan hecho antes de mirar los datos
se corrige con los datos, no se defiende.

⚠️ **Y `dias` no es exacto tampoco, medido el 2026-07-30:** pedir 30 filas
devolvió desde el 12 de junio, o sea **48 días de calendario**. La fuente guarda
un registro por *vigencia*, no por día: la TRM del viernes vale también sábado y
domingo. Por eso el dict devuelve `registros`, `desde` y `hasta`, y la función
**nunca afirma "los últimos 30 días"** — si lo dijera, el modelo repetiría la
mentira con total confianza.

### `guardar_reporte(...)` — la irreversible
Las otras cuatro **leen**; esta **modifica tu computador**. Vuelve todo el nivel
4: el permiso se pide **fuera** de la herramienta (en el harness), se **deniega
por defecto**, y cuando se niega hay que devolver un `tool_result` que diga
`PERMISO DENEGADO` — porque si niegas en silencio, el agente dice *"ya lo
guardé"* y no guardó nada (L4.9).

> **Ninguna de las cinco está ahí porque el agente la necesite para funcionar.**
> Están porque cada una fuerza a resolver algo que las demás no.

---

## §5b.3 — La estructura de archivos, y por qué

Todos los niveles anteriores tenían esta forma:

```
NN-nivel/
├── README.md      ← se lee
└── NN_script.py   ← se corre
```

Un proyecto no cabe en un archivo. Este tiene cuatro:

```
05b-proyecto/
├── README.md          ← esta guía
├── herramientas.py    ← las 5 funciones. Python puro, sin modelo, sin API de Claude
├── agente.py          ← el harness + el bucle. Este es el que se corre
├── evals.py           ← las pruebas deterministas (116 casos, $0.00)
└── rubrica.md         ← el instrumento del paso 10: qué hace buena a una RESPUESTA
```

⚠️ **`rubrica.md` es texto, no código, y eso es el punto.** Los 116 casos de
`evals.py` preguntan *"¿esta función devuelve el número correcto?"*. La rúbrica
pregunta *"¿esta **respuesta** estuvo bien?"* — y eso no lo decide un `if`, lo
decide otro modelo leyendo un texto que escribiste tú. **El texto ES el
instrumento**, por eso vive en su propio archivo y se escribió antes de correr
nada.

Y dos cosas que **no se crean a mano** — las crea el programa al correr:

```
├── caja/              ← donde escribe guardar_reporte (como en el nivel 4)
└── registro.jsonl     ← la bitácora del harness
```

### Por qué `herramientas.py` está separado de `agente.py`

No es estética. Es la lección del nivel 5.

`00_probar_detector.py` probaba los detectores **sin llamar a la API**: 16 casos,
**$0.00**, y ahí se cazaron dos bugs *antes* de pagar un centavo. Salió idéntico
en las dos máquinas. Eso solo fue posible porque los detectores eran funciones de
Python normales, **separadas de la llamada al modelo**.

| Archivo | ¿Necesita internet? | ¿Necesita la API key? | ¿Cuesta probarlo? |
|---|---|---|---|
| `herramientas.py` | solo 3 de las 5 | **no** | **$0.00** |
| `agente.py` | sí | sí | sí |

> **Regla:** separa lo que puedes probar gratis de lo que cuesta dinero probar.

Por eso `evals.py` empieza importando `herramientas` y probando **sin tocar
Claude**. El modelo entra después.

---

## §5b.4 — Las dos fuentes de datos

Las dos son **gratis y sin llave**. Verificadas con `curl` el **2026-07-29**
(HTTP 200 las dos):

| Fuente | URL |
|---|---|
| Mercado | `https://open.er-api.com/v6/latest/USD` |
| TRM oficial | `https://www.datos.gov.co/resource/32sa-8pi3.json` |

Detalles verificados, no recordados:

- La TRM acepta `?$order=vigenciadesde%20DESC&$limit=N` y devuelve los campos
  `valor`, `unidad`, `vigenciadesde`, `vigenciahasta`. **De ahí sale también
  `historial`**: pedir N filas ordenadas es una serie de tiempo.
  - ⚠️ **CORREGIDO en la sesión 12.** Antes esta línea decía
    `?$order=vigenciadesde DESC`, con un **espacio de verdad**. Así se verificó
    con `curl` en la sesión 9 y funcionó, porque `curl` codifica el espacio solo.
    Pegado en `urllib` **revienta** con
    `http.client.InvalidURL: URL can't contain control characters`.
    El espacio va como `%20`. → **Una URL verificada con una herramienta no
    está verificada para otra.**
- La API de mercado trae `time_last_update_utc` y `time_next_update_utc` — o sea
  **te dice de cuándo es el dato**. Eso importa para la rúbrica de "¿citó la
  fuente?".
- **La TRM no cambia el fin de semana.** La del 25 de julio valió hasta el 27.
  El caso de prueba del domingo no hay que inventarlo: está en los datos.

### ⚠️ Una advertencia que ya costó una corrección

La brecha entre las dos fuentes **no es fija**:

| Día | Mercado | TRM oficial | Brecha |
|---|---|---|---|
| 2026-07-28 | 3.215,61 | 3.205,80 | ~10 pesos |
| 2026-07-29 | 3.206,17 | 3.205,87 | **0,30 pesos** |

La sesión 8 había anotado *"no coinciden (~10 pesos)"* con **una sola
observación** detrás. Lo estable es **que son fuentes distintas**, no cuánto se
separan.

> Este material enseña *"pueden no coincidir"*, **nunca una magnitud**. Es L1.13
> otra vez (el "Haiku cuesta 5x menos"), atajada antes de escribir código.

---

## §5b.5 — El plan del nivel

Se va llenando a medida. Un paso por vez, como siempre.

| Paso | Qué se hace | Quién escribe | Estado |
|---|---|---|---|
| 1 | Explicar qué es un proyecto integrador, las piezas y las 5 herramientas | — (se lee) | ✅ |
| 2 | Crear la carpeta y los archivos vacíos | dictado | ✅ |
| 3 | Este README | mío | ✅ |
| 4 | `herramientas.py`: las 2 que no tocan internet | **tú** | ✅ `convertir()` · `guardar_reporte()` |
| 5 | `evals.py`: probar esas 2 gratis, antes de gastar nada | **tú** | ✅ **116 casos, 0 fallos, $0.00** (eran 26; la sesión 12 sumó los 9 del contrato, la trampa de red y los dobles de `tasa` y `trm`; la 13 sumó 27 de `historial` y 27 de `trm_en_fecha`) |
| 6 | `herramientas.py`: las 3 que sí tocan internet | mixto | ✅ `pedir_json()` · `tasa()` (12 casos) · `trm()` (16) · `historial()` (27) |
| 6b | `trm_en_fecha(fecha)` — **idea suya**, la 6ª herramienta | dictado | ✅ 27 casos. Cerró una **inyección** demostrada en vivo (1 → 1000 filas) |
| 7 | `agente.py`: el bucle agéntico | dictado | ✅ menú de 6 (3.049 tokens medidos) + puente + bucle. **7 vueltas, 3 respuestas correctas** |
| 8 | `agente.py`: **los 10 frenos** del harness | **decisiones suyas** | ✅ escrito **y corrido** · $0.1496, 7 vueltas, 3 respuestas correctas |
| 9 | Correrlo de verdad y medir | **tú** | ✅ **3 modelos medidos**: eligieron idéntico · opus $0.1496, sonnet $0.0894, haiku $0.0284 |
| 10 | Evals con rúbrica / LLM-as-judge sobre tu propio agente | mixto | ✅ **10 casos calificados.** `rubrica.md` + `examen.py` + `juez.py`. **Encontró un defecto real que los 121 evals no podían ver** |

# 🎓 NIVEL CERRADO — los diez pasos están hechos.

> 🆕 **El freno 10 llegó en el paso 9, y no estaba planeado.** Al meter los tres
> modelos en un catálogo con sus precios, apareció una forma nueva de
> equivocarse: escribir mal el nombre del modelo. `MODELO` se valida contra el
> catálogo **antes de gastar un centavo**, y si no está, el programa muere ahí
> diciéndote cuáles sí valen. Es la misma familia de los frenos 7 y 8 —*no
> confíes en un nombre solo porque alguien lo escribió*— salvo que aquí el que
> escribe eres tú, no el modelo.

> ⚠️ **Cuáles son los 9 frenos, en una lista.** Esta tabla decía antes *"los 6
> frenos"* sin decir cuáles, y eso confundió en la sesión 15. **Seis vienen del
> nivel 4** y están en `04-harness-real/README.md` §4.3: timeout+reintentos,
> errores tipados, presupuesto, tope de vueltas, permisos y registro. **Tres son
> nuevos de este nivel** porque aquí hay seis herramientas y allá había una:
> ¿existe la herramienta?, ¿acepta esos argumentos?, y la red final.
> La lista completa, con el porqué de cada uno, está en la cabecera de
> `agente.py`. **Un plan que promete un número sin lista no es un plan.**

**Por qué en ese orden y no otro:** los pasos 4 y 5 no cuestan **un centavo** y
no necesitan internet. Se empieza por lo que se puede probar gratis. Si
`convertir()` está mal, quieres saberlo antes de que el modelo entre en escena —
no después de pagar 20 llamadas persiguiendo un bug de multiplicación.

---

## Ejercicios

Los cuatro se pueden hacer con lo que ya está escrito. Los tres primeros
**cuestan $0,00**.

### 1. Sabotea el puente (gratis)

En `herramientas.py`, cámbiale el nombre a la llave del puente de `tasa()`: que
diga `inversa` en vez de armarse con las monedas. Corre `python evals.py`.

**Deberían ponerse rojos 3 casos.** Si no se ponen rojos, tus pruebas no están
mirando lo que crees. *(Es la comprobación de L5b.13: una red que nunca viste
atrapar nada no es una red, es un comentario.)*

### 2. Rompe al juez a propósito (gratis, y es el más instructivo)

En `juez.py`, baja `MAX_TOKENS_JUEZ` de 4000 a 300 y **no corras nada todavía**:
escribe primero, en un papel, **qué casos crees que van a fallar**.

Después corre `python juez.py 4 8`. El 4 es el difícil, el 8 es el fácil.
→ Lo que estás midiendo es si el fallo del instrumento está **sesgado** hacia
los casos duros (L5b.26).

### 3. Cuenta las casillas de tu propia rúbrica (gratis)

Sin correr nada: cuenta a mano cuántas casillas `●` tiene cada criterio en la
matriz de `rubrica.md`. Compáralas con el `APLICA` de `juez.py`.

**Tienen que dar lo mismo.** El día que no den, tienes dos rúbricas otra vez —
y esa es justo la razón por la que el texto se lee del `.md` y no se copia.

### 4. La corrida buena (≈$1,50 — solo si quieres el número)

`REPETICIONES = 3`, `MODELO = "claude-sonnet-5"` en `agente.py`,
`MODELO_JUEZ = "claude-opus-5"` en `juez.py`. Corre `examen.py` y después
`juez.py`.

⚠️ **Antes de gastarlo, pregúntate quién va a usar ese número.** Si la respuesta
es "nadie", el ejercicio ya lo hiciste al leer esta línea.

---

## Lo que ya sabes

Con los números de tus propias corridas, no de un ejemplo.

### Construiste, desde archivos vacíos

| Archivo | Qué es |
|---|---|
| `herramientas.py` | **6 herramientas** + 5 ayudantes. Python puro: sin modelo, sin API |
| `evals.py` | **121 casos, 0 fallos, $0,00, sin red** |
| `agente.py` | el bucle agéntico + **10 frenos** + catálogo de 3 modelos |
| `examen.py` | el examinador: 10 preguntas en conversaciones limpias |
| `juez.py` | el juez: una llamada, sin bucle, sin herramientas |
| `rubrica.md` | el instrumento: 10 × 6, escrito **antes** de correr nada |

### Y sabes, porque lo mediste tú

- **Un agente paga por lo que RELEE**: 23.710 de entrada contra 887 de salida.
  **27 a 1.**
- **Los tres modelos eligieron idéntico** y costaron $0,1496 · $0,0894 · $0,0284.
  El caro no eligió mejor: **explicó** mejor.
- **El menú pesa 3.447 tokens** en cada vuelta, y las herramientas que nunca se
  llaman son el 40% — que **no es desperdicio: es la opción de poder responder**.
- **El mismo texto pesa distinto en cada familia de modelos** (3.543 vs 3.702).
- **Sumar las partes no da el todo**: hay un costo fijo por tener herramientas.
  Se mide **restando**.
- **Un puente cuesta casi nada**: +221 de entrada, −42 de salida, +$0,000011 —
  y evita que el modelo invente un número.

### Lo que sabes hacer y no sabías al empezar el nivel

1. Escribir una herramienta que **no revienta nunca** y devuelve errores que el
   modelo puede leer y usar.
2. Probar la mitad de tu agente **gratis, sin red y sin modelo**.
3. **Sabotear tus propias pruebas** para comprobar que sirven.
4. Reconocer una **inyección** cuando un dato de afuera entra a una consulta.
5. Poner **diez frenos** y saber de qué protege cada uno: del mundo, de tu
   cuenta de cobro, o del modelo.
6. **Medir tokens y dólares** con el contador de la API, que es gratis y es el
   único que vale.
7. **Comparar modelos con un experimento honesto** y decidir con dos pasos, no
   con el precio.
8. Escribir una **rúbrica** y un **juez**, y —lo más importante— **auditar al
   juez**: distinguir un fallo del instrumento de una mala nota del examinado.

> **Y la que resume el nivel:** un `if` prueba tu código. Para lo que el modelo
> hace en su cabeza hace falta una rúbrica. **Tus 121 evals no podían ver el
> 3.209,64; el criterio C2 lo vio en la primera pasada.**
