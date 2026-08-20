# RÚBRICA DEL DUELO — nivel 8, pieza 0.3

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
