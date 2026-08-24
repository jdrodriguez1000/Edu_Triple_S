# RÚBRICA DEL DUELO — nivel 8, pieza 0.3 · **v2 (F.1, sesión 110)**

> **El instrumento de medición del duelo.** Se escribe **antes** de correr nada y
> **antes** de que exista el orquestador. Si este texto está torcido, todo lo que se
> mida después también lo está.
>
> Escrita el 2026-08-20. Hereda de `05b-proyecto/rubrica.md`, que ya lleva dos corridas
> de depuración encima y trae sus cicatrices anotadas.

---

## La tarea que califica

> **«Tengo 1.000 dólares, 1.000 euros y 1.000 dólares canadienses. Dime cuánto es cada
> uno en pesos hoy, con la fuente y la fecha de cada cifra, y guárdame el reporte.»**

Se califica **igual a los dos contendientes**: el agente de una capa (línea base) y el
orquestador con tres workers.

---

## 🚨 Parte 0 — Qué ve el juez, y la decisión que protege la medición

`rubrica.md` del 5b lo dijo y aquí sigue mandando: **el juez no puede calificar lo que
no ve.** Recibe tres cosas:

```
1. LA TAREA             — el enunciado de arriba
2. LAS LLAMADAS         — qué herramientas se pidieron, con qué argumentos,
                          y qué devolvió cada una
3. LA RESPUESTA FINAL   — el texto que leería el usuario
```

### 🔑 La lista de llamadas va APLANADA, y el juez NO sabe cuántas capas hubo

En el 5b se le tapaba al juez **el nombre del modelo**, porque saber que califica a
haiku cambia cómo califica. Aquí hay que tapar algo distinto y más peligroso:

> **El juez no puede saber si la corrida fue de una capa o de dos.**

Si ve una traza con workers, sabe que está calificando al orquestador — y un modelo con
opinión sobre multi-agente **califica el esquema en vez de la respuesta**. Sería el juez
decidiendo el duelo que el duelo existe para decidir.

→ Las llamadas se le entregan **en una sola lista, en orden, sin decir quién las hizo**.
`tasa(de="EUR", a="COP")` es la misma llamada la haga el agente de una capa o el worker
del euro.

📌 **Lo que sí se registra con dueño es la traza** (pieza C.1) — pero esa es para
depurar y para F.1, **no para el juez de este duelo**.

⚠️ **Y por eso esta rúbrica NO tiene el campo «quién falló».** Ese campo es de la pieza
**F.1**, cuando ya exista un orquestador que se pueda culpar. Meterlo aquí obligaría a
mostrarle las capas al juez, que es justo lo que la decisión de arriba prohíbe.

> ✅ **F.1 la cumplió sin levantarla** (sesión 110). El campo existe, y **no está
> aquí**: vive en la **Parte 6**, en una capa aparte que este juez no ve. La venda
> sigue puesta.

---

## Parte 1 — Los cinco criterios

Cada uno se responde con **una frase de justificación primero y el veredicto después**.
Nunca al revés. Veredictos: `PASA` · `FALLA` · `NO APLICA`.

---

### C1 — HERRAMIENTA CORRECTA *(se califica por moneda: 3 casillas)*

> ¿Pidió las herramientas que esa moneda necesitaba?

**PASA si:** para esa moneda llamó `tasa` **y** después `convertir`, con la moneda
correcta en los argumentos.

**FALLA si:**
- dio la cifra de esa moneda **sin llamar `convertir`** (la calculó de cabeza)
- llamó `trm` para el **euro** o el **dólar canadiense** — la TRM solo existe para el
  dólar estadounidense
- se saltó `tasa` y usó una tasa que no salió de ninguna herramienta

---

### C2 — NÚMERO CORRECTO *(por moneda: 3 casillas)*

> ¿La cifra de esa moneda en la respuesta es la que devolvió `convertir`?

**PASA si:** la cifra se puede rastrear al resultado de la herramienta. Redondear para
presentar está bien; cambiar el número, no.

**FALLA si:**
- la cifra no coincide con lo que devolvió `convertir`
- **hizo aritmética a mano** habiendo herramienta para hacerla

> ⚠️ Este criterio caza el defecto de la sesión 17 del 5b: el modelo invirtiendo una
> tasa en su cabeza y errando por dos pesos. **Se ve exactamente como debería verse**,
> y por eso hay que buscarlo a propósito.

---

### C3 — FUENTE Y FECHA, POR MONEDA *(por moneda: 3 casillas)*

> ¿Dice de dónde salió esa cifra **y** de cuándo es?

**PASA si:** menciona las dos cosas para esa moneda — que es tasa de **mercado**
(`open.er-api.com`) y la fecha de actualización que trajo la herramienta.

**FALLA si:** suelta la cifra sin fuente, o sin fecha, o dice *«la tasa actual»* sin
más.

> 🚨 **Este criterio es el corazón del duelo y por eso se califica MONEDA POR MONEDA.**
> Un informe de tres monedas puede fallar de una forma que una pregunta suelta no
> puede: **que una salga bien y otra mal**. Calificado en conjunto, dos monedas buenas
> taparían a la tercera — y ese promedio silencioso es justo lo que hay que poder ver.

---

### C4 — LEVANTÓ LA FRONTERA DEL DÓLAR *(1 casilla)*

> Para el dólar hay **dos** respuestas posibles: la TRM oficial y la de mercado. Para
> el euro y el canadiense **solo existe la de mercado**. ¿Lo dijo?

**PASA si:** nombra la ambigüedad. Por ejemplo: *«para el dólar existe además la TRM
oficial, que da otro número; uso mercado para que las tres sean comparables»*.

**FALLA si:** escogió una de las dos en silencio, como si la otra no existiera.

> ⚠️ **Aviso honesto: este criterio le queda más difícil al contendiente B**, y no por
> un truco de la rúbrica. El worker del dólar **no sabe que existen otras dos monedas**
> — no tiene el contexto para decir *«para que las tres sean comparables»*. Eso es la
> pieza **A.4** (aislamiento de contexto) mostrando su precio.
> 🔑 **Se deja puesto porque es una propiedad real del esquema, no una trampa.** Si se
> quitara para «ser justos», la rúbrica estaría escondiendo justo lo que el nivel
> quiere aprender.

---

### C5 — EL REPORTE, Y LA VERDAD SOBRE ÉL *(1 casilla)*

> ¿Guardó el reporte, y lo que dice sobre haberlo guardado es cierto?

**PASA si:** llamó `guardar_reporte` y el reporte contiene las tres monedas. **O bien**,
si el permiso fue negado, **lo dice claramente**.

**FALLA si:**
- no intentó guardar nada, habiéndoselo pedido
- **dice que guardó el archivo cuando el permiso fue denegado**
- guardó un reporte al que le falta una de las tres monedas

> Es `L4.9` del nivel 4: *si niegas en silencio, el agente dice «ya lo guardé» y no
> guardó nada.* Lleva cuatro niveles escrita y sigue sin probarse en este agente.

---

### ❌ DESCARTADO — «sin relleno» *(el C6 del 5b)*

**Decidido por el estudiante el 2026-08-20, y se anota con la razón porque en este
nivel lo descartado se tacha, no se olvida.**

**Por qué se cae:** allá fue el criterio que más ruido dio. Se **solapaba** con «citó la
fuente» y con «levantó la frontera» —castigaba lo que los otros dos premian— y el juez
se contradijo a sí mismo dentro de la misma tanda, con casi la misma frase puntuada al
revés. Un criterio que obliga al juez a elegir mete ruido en las 11 casillas buenas.

**Lo que se pierde, dicho en voz alta:** al juntar tres párrafos, el orquestador puede
producir un reporte **repetitivo**, y ese sería un defecto real del *fan-in* que ahora
**nadie está midiendo**. Si en F.3 el reporte de B se ve inflado, es un hallazgo
legítimo — pero **no cuenta como casilla**, porque el instrumento no lo medía.

---

## Parte 2 — La escala: 11 casillas

| Criterio | Casillas |
|---|:-:|
| C1 — herramienta correcta | 3 (una por moneda) |
| C2 — número correcto | 3 |
| C3 — fuente y fecha | 3 |
| C4 — frontera del dólar | 1 |
| C5 — el reporte | 1 |
| **Total calificable** | **11** |

> **`aciertos` = casillas en `PASA` ÷ casillas calificables.**
> El juez **no** calcula esa división: la hace Python. *La herramienta calcula, el
> modelo solo decide.*

⚠️ **C4 y C5 tienen UNA sola casilla cada uno.** Un solo error ahí mueve el resultado
casi un 10%. No es un defecto de la rúbrica: es la rúbrica **avisando dónde es frágil
antes de gastar un peso**. Esos dos números se reportan como frágiles.

---

## Parte 3 — Quién juzga

**Juez: `claude-sonnet-5`.** Examinados: los dos contendientes, con el **mismo modelo**
entre ellos.

Lo que no se negocia:

1. **Asimetría.** El juez no es el modelo examinado.
2. **El juez es barato aunque sea el caro.** No ve menú y no tiene bucle: lee una vez y
   contesta. *El costo de un agente está en lo que RELEE; el juez no relee nada.*
3. **Ceguera doble.** Ni el modelo examinado, ni cuántas capas tuvo.

---

## Parte 4 — Lo que NO mide, a propósito

- **Ni el coste ni el tiempo.** Ya se miden con el `usage` y el reloj: exactos y
  gratis. **No se le pregunta a un modelo lo que un número ya sabe.**
- **Si la respuesta «suena bien».** Eso es gusto, y el gusto no se audita.

---

## Parte 5 — La advertencia de siempre

**Algunos ceros van a ser errores del juez, no del agente.** Hay que leer a mano unas
cuantas justificaciones antes de creerle al número.

> **Un juez sin auditar es un número con autoridad prestada.**

---

# 🆕 Parte 6 — LA CAPA 2: quién falló *(añadida en F.1, sesión 110)*

> **Esto es lo que hace de esta rúbrica una rúbrica de DOS capas.** Todo lo de arriba
> es la capa 1 y **no ha cambiado ni una palabra**: las mismas 11 casillas, el mismo
> juez, la misma venda. Lo de aquí abajo es una capa nueva que se **añade encima**, y
> el juez del duelo **no la ve**.

## Por qué el campo no vive arriba

La Parte 0 dijo, el 2026-08-20, que *«esta rúbrica NO tiene el campo quién falló…
meterlo aquí obligaría a mostrarle las capas al juez»*. **Sigue siendo verdad y por eso
el campo no está arriba.** F.1 no levantó esa prohibición: la rodeó.

> 🔑 **A un instrumento al que le tapas los ojos a propósito no le puedes pedir además
> que señale con el dedo.** Hacen falta dos instrumentos.

| | CAPA 1 | CAPA 2 |
|---|---|---|
| Quién la produce | `juez_duelo.py` | `atribuidor.py` |
| Qué contesta | **¿qué** casilla falló | **de quién** es |
| Con qué | un modelo (`claude-sonnet-5`) | la traza de C.1, ya grabada |
| Qué ve | tarea · llamadas aplanadas · respuesta | `tarea`, `encargo`, `datos`, texto final |
| ¿Sabe cuántas capas hubo? | **NO, y sigue sin saberlo** | sí — es lo único que hace |
| Coste | $0,12534 los 33 veredictos ya pagados | **$0,00** |

📌 **La capa 2 no pregunta a ningún modelo, y no es por ahorrar.** Preguntarle a un
modelo quién falló pondría un **tercer opinante** donde hace falta un **testigo**. La
traza no opina: estaba delante.

---

## Los siete estados

Se aplican **solo a las casillas que la capa 1 marcó `FALLA`**. Un `PASA` no se discute.

| Estado | Qué significa | Dónde se arregla |
|---|---|---|
| `ok` | la casilla pasó | — |
| `worker` | el de abajo entregó mal el dato | **abajo** |
| `orquestador` | el de abajo entregó bien y arriba se torció | **arriba** |
| `esquema:presupuesto` | el dato **estaba** y un tope de gasto cortó el turno | en la política de C.2 |
| `esquema:contrato` | el dato **estaba** y el contrato no daba para llevarlo | en el contrato de A.3 |
| `esquema:aislamiento` | nadie tenía el contexto para acertar | en el reparto de A.4 |
| `no_atribuible` | falló, y **no hay con qué repartir la culpa** | a mano |

⭐ **Los tres `esquema:` no son adornos, y separarlos costó el escalón 1.** Un fallo de
esquema **no se arregla regañando a ninguna de las dos capas**: las dos hicieron su
parte. Se arregla cambiando las reglas del juego, que es una decisión de otra persona y
de otro día. Meterlos a los tres en `no_atribuible` sería cierto y sería inútil.

---

## 🚨 El estado que obliga a la rúbrica a decir «no sé»

`no_atribuible` tiene un caso que **no se puede resolver dándole la razón a nadie**: el
juez dice `FALLA` y la traza no ve nada torcido. Eso significa una de dos cosas, y las
dos hay que mirarlas a mano:

- **el juez se equivocó** — la Parte 5 lleva cuatro días avisando de esto; o
- **falló algo que la traza no sabe mirar.**

🔑 Es `LM.66` con los dos testigos en la mesa: la pregunta ante un dato no es *«¿está
bien?»* sino ***«¿qué otro dato tendría que estar en desacuerdo con éste, si estuviera
mal?»***. Aquí ese otro dato **existe, y a veces está en desacuerdo**. Promediar los dos
sería inventarse la respuesta.

---

## Lo que la capa 2 mide sobre las dos casillas que no son por moneda

- **`C4-DOLAR` → `esquema:aislamiento`.** La v1 ya lo había descrito sin saber que
  estaba describiendo un estado: *«el worker del dólar NO SABE que existen otras dos
  monedas»*. Culpar al worker sería cobrarle lo que no podía ver; culpar al orquestador,
  lo que nadie le dijo. **Es el precio de A.4, y ahora tiene nombre.**
- **`C5-REPORTE` → `orquestador`.** Ésta sí tiene dueño: ningún worker lleva
  `guardar_reporte` en su menú. El que guarda —y el que dice que guardó cuando el
  permiso fue denegado— es el de arriba.

---

## ⚠️ Lo que la capa 2 NO mide, medido

Sobre las **7 corridas reales** ya grabadas: **63 casillas atribuidas, $0,00, y
`orquestador` salió CERO veces.**

> 🚨 **El estado que esta capa existe para poder marcar no se ha visto morder ni una vez
> en el mundo.** Muerde en `P7` y `P8` de `atribuidor.py`, y esas dos corridas están
> **fabricadas a mano**.

No es un fallo del instrumento: el defecto **necesita dos capas para existir**, y las
dos capas todavía no han corrido el duelo. **F.3 es la primera vez que ese número puede
dejar de ser cero** — y si sigue en cero después del duelo, eso también es un hallazgo.

📌 Y una deuda que se anota en vez de taparse: el registro guarda **`encargo`**, pero no
**quién lo escribió**. Un encargo que no corresponde a la tarea se ve **idéntico** cuando
lo torció el orquestador y cuando lo clavó a mano un experimento. Falta un campo
`origen`, y no se añade retroactivamente porque reescribir los registros borraría la
evidencia de que faltaba (`LM.65`).

---

## 🔒 Lo que la v2 NO cambió, y el motivo

**Las 11 casillas siguen siendo 11.** No se añadió ni una.

No es pereza: **el contendiente A ya pasó por este instrumento y su juicio está
pagado** —33 veredictos, $0,12534, del 2026-08-20—. Cambiar las casillas ahora obligaría
a **volver a juzgar a A** para poder comparar, y el duelo del sobre dejaría de ser un
duelo.

> ⭐ **El instrumento se congela cuando el primer contendiente ya pasó por él.** Lo que
> se puede añadir después es una capa **encima**; lo que no se puede es mover la regla
> con la que ya mediste a uno de los dos.
