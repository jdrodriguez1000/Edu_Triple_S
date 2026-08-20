# 🔒 EL SOBRE — la apuesta del nivel 8, escrita antes de construir nada

> **Este archivo se escribe ANTES de que exista una sola línea del orquestador.**
> Su valor entero está en la fecha de su commit: prueba que la predicción se escribió
> sin conocer el resultado.
>
> Se abre en la pieza **F.3**, al final del nivel. **En medio no se mira.**

---

## Por qué existe

Un criterio escrito **después** de tres sesiones construyendo se dobla solo para
justificar lo ya construido. No por deshonestidad: por cómo funciona la cabeza. Es
`LM.61` y `[D-100]` del nivel 7 — *los tramos del resultado se sellan antes de pagar la
medición, o el número se reinterpreta cuando llega*.

## 🚨 Qué cubre el sello, y cómo se anula

El sello protege un **trío**:

> **tarea + contendientes + tramos**

**Si cualquiera de los tres se mueve después del commit, el sello queda ANULADO**, no
corregido. El peligro no es al escribirlo: es el día que se abra y el resultado no
guste. La frase que aparece sola en la cabeza es *«bueno, con otra tarea habría
ganado»*. **Cambiar la tarea después de medir es esa frase con más pasos.**

---

## La tarea

> **«Tengo 1.000 dólares, 1.000 euros y 1.000 dólares canadienses. Dime cuánto es cada
> uno en pesos hoy, con la fuente y la fecha de cada cifra, y guárdame el reporte.»**

Decidida el 2026-08-20. El motivo del cambio respecto a la tarea original está en
`README.md` del nivel: la primera no se podía hacer con las seis herramientas.

## Los contendientes

**A — UNA CAPA.** El agente del 5b/6b. Una sola conversación, seis herramientas en el
menú. Siete llamadas seguidas: `tasa`+`convertir` por cada moneda, y `guardar_reporte`.
Todo lo que va ocurriendo se queda en la conversación y **se reenvía en cada vuelta**.

> ✏️ **CORRECCIÓN MEDIDA el 2026-08-20, antes de medir a B.** La frase *«siete llamadas
> **seguidas**»* es **falsa**, y la línea original se deja en pie porque un registro
> corregido hacia atrás deja de ser un registro.
>
> 🚨 **A ya paraleliza.** Las tres corridas de la línea base gastaron **4 vueltas**, no
> ocho: el modelo pide las **tres `tasa` en un solo turno**, las **tres `convertir` en
> el siguiente**, `guardar_reporte` en el tercero y redacta en el cuarto. Son siete
> llamadas, sí — pero en **cuatro** viajes al modelo.
>
> 🔑 **Esto desmiente la premisa de la que colgaba la expectativa de tiempo de la
> Parte 1-bis** (*«A hace ~8 vueltas seguidas; B hace ~6, luego B es más rápido»*). El
> margen que se le suponía al paralelo **ya estaba cobrado por el contendiente A**.
>
> ⚠️ **Y aun así NO se toca nada:** ni la Parte 1, ni la Parte 1-bis, ni los tramos. Es
> `LM.21` — *un sello protege de decidir tarde, no de que el mundo desmienta lo que
> sellaste*. Se **anota** el desmentido con su fecha; **mover el tramo del 75% ahora que
> se sabe que a B le queda cuesta arriba sería exactamente el fraude que el sobre existe
> para impedir.**

**B — DOS CAPAS.** Un orquestador y tres workers, uno por moneda. Cada worker tiene
**dos herramientas, no seis**, hace sus dos llamadas y devuelve un párrafo. El
orquestador junta los tres y llama `guardar_reporte`. **Cada worker tiene su propia
conversación y no ve la de los otros.**

🚨 **El mismo modelo en los dos lados.** Si A corre con haiku y B con opus, lo medido es
el modelo, no el esquema.

---

## PARTE 1 — La apuesta, mitad general

> **Escrita por el estudiante el 2026-08-20, textual y sin retocar.** Esta mitad habla
> del **esquema**, no de esta tarea: sobrevive aunque la tarea cambie.

**1. ¿Cuándo gana el esquema multi-agente?**

> *«Gana cuando el trabajo lo podemos independizar minimizando el uso de herramientas,
> el número de vueltas.»*

**2. ¿Cuándo pierde?**

> *«Pierde en el caso contrario a lo dicho en el punto 1.»*

**3. ¿Qué sería «me equivoqué»?**

> *«Que realice la misma tarea pero cueste mucho más, o se demore mucho más, o el
> reporte salga peor: que pierda la fuente, la fecha, o la precisión en alguna de las
> tres monedas.»*

> ✏️ **Ampliado el mismo día, antes de medir nada.** La primera redacción decía solo
> *«cueste mucho más o se demore mucho más»* — coste y tiempo, y **faltaba la tercera
> vara**. El agujero era concreto: B podía salir más rápido y más barato **y devolver
> un reporte con una cifra sin fuente**, y eso habría contado como *«acerté»*.
> 🔑 Se amplía porque no se ha corrido nada; **después de medir, esto mismo sería
> amañar la apuesta.**

---

## PARTE 1-bis — La expectativa de la terminal que supervisa

> ⚠️ **Esto NO es la apuesta del nivel.** La apuesta es la de arriba. Esto se guarda
> aparte, con su dueño escrito, porque él la pidió y porque en F.3 se pueden comparar
> las dos. **No vale más por venir de esta terminal: aquí tampoco se ha medido nada**,
> y el historial de este proyecto tiene varias correcciones en la dirección contraria.

**Tiempo:** B algo más rápido, **por poco margen**. Los tres workers corren a la vez,
pero el orquestador añade sus propias vueltas (repartir, recibir, guardar, contestar).
Con dos llamadas por worker, lo que ahorra el paralelo casi se lo come la capa de
arriba.

**Coste: no se sabe, y es lo más interesante del duelo.** 🔑 Lo caro de un agente de una
capa **no son las llamadas, es el menú**: `rubrica.md` del 5b midió ~26.000 tokens de
entrada por corrida **porque relee las seis herramientas en cada vuelta**. Un worker
relee **dos**. Puede que la duplicación de capas se pague sola con menús más chicos.
📌 **Aquí esta terminal discrepa del estudiante**, que da por hecho que costará mucho
más.

**Aciertos: B igual o peor**, con una falla concreta esperada. El orquestador **nunca ve
lo que devolvió `tasa`**: solo lee tres párrafos. Si un worker escribe *«1.000 euros son
X pesos»* sin arrastrar la fuente y la fecha, ese dato **ya no existe en ninguna parte**
cuando el orquestador redacta — no puede recuperarlo ni sabe que le falta. Es la pieza
**A.3**, y el criterio que caería es *citó la fuente*.

**En conjunto, en esta tarea:** se espera que B no compense. La tarea es chica a
propósito, y eso juega en su contra.

---

## PARTE 2 — Los tramos

> ⚠️ **Autoría, y hay que dejarla clara:** estos tres números los **propuso esta
> terminal** y el estudiante los **adoptó** tras oír el razonamiento. La Parte 1 es
> suya; esta parte es adoptada. El día que se abra el sobre hay que poder saber de
> quién era el juicio que se está probando.

Escritos **en relativo (B contra A)**, no en absoluto: la línea base todavía no existe
cuando se escriben, y así siguen valiendo cuando se mida.

### ⏱️ Tiempo — **B gana si tarda el 75% o menos de lo que tardó A**

Tiene que sacarle **al menos una cuarta parte**.

**Por qué no *«gana si tarda menos»* a secas:** el umbral tiene que ser **más grande que
el ruido del instrumento**. Estas corridas dependen de la red y de la latencia de la
API, que varían solas entre una corrida y otra. Con un umbral de 3% no sabrías si ganó
el esquema o si esa vez internet estuvo mejor.

**De dónde sale el 25%:** A hace ~8 vueltas seguidas; B hace ~3 del orquestador más ~3
de los workers, que corren a la vez. Si el paralelo sirve de algo, tiene que verse ahí.
**Menos que eso no es una victoria, es una casualidad.**

### 💰 Coste — **se acepta que B cueste hasta 2 veces lo que costó A**

**Por qué no 1× (que el coste descalifique):** sería una vara más dura que la que el
propio esquema se pone. Multi-agente **nunca prometió ser más barato**: promete ser más
rápido y aguantar trabajos que una capa no sostiene. Exigirle que además sea más barato
es reprobarlo por algo que no dijo.

**Por qué no 3× o 4×** — y esta es la razón que manda:

> 🔑 **El rival del multi-agente no es solo el agente de una capa. Es el agente de una
> capa con un modelo mejor, pagado con la diferencia.**

Si se acepta pagar el triple, ese triple también alcanza para correr **una sola capa con
un modelo más caro y más listo** — más simple, más fácil de depurar, menos partes que
fallan. **Pasado el doble, el multi-agente compite contra una alternativa que casi
siempre gana.**

### ✅ Aciertos — **B no puede perder más de 1 casilla respecto de A**

Sobre las **11 casillas** de `rubrica_duelo.md`. Una casilla ≈ 9%.

**Por qué exactamente 1:** porque ya está predicho **cuál** va a caer —**C4, la frontera
del dólar**— y está escrito **por qué**: el worker del dólar no sabe que existen otras
dos monedas. Es una pérdida **estructural y entendida**, parte del trato de partir el
trabajo.

🔑 El umbral queda puesto justo ahí: **la falla predicha no descalifica; una segunda
falla sí.** Una segunda casilla significa que se rompió algo que **no** se había
previsto, y esa es la señal que vale la pena escuchar.

**El argumento en contra, que también es bueno y se deja escrito:** perder C4 es una
pérdida real para quien lee el reporte. Se le está perdonando al esquema un defecto que
el usuario sí paga.

### 🔗 Cómo se combinan — **B gana solo si cumple los TRES**

Si falla uno solo, es *«me equivoqué»*.

🚨 Se escribe ahora aunque parezca obvio, porque es **lo primero que se reinterpreta**
con el resultado delante: *«bueno, falló en coste pero ganó en los otros dos, así que
empató»*. **Un empate que no estaba definido antes no es un empate: es una
negociación.**

### 📐 Y cómo se mide: **tres corridas de cada contendiente, y se toma la MEDIANA**

Con una sola corrida el tramo de tiempo **no se puede evaluar**: no se sabría cuánto
varía A consigo mismo, así que no se puede saber si el 25% es señal o suerte. Con haiku
y siete llamadas, las seis corridas cuestan centavos. **Es la diferencia entre un número
y una anécdota.**

---

## 📊 LA LÍNEA BASE — medida el 2026-08-20, antes de que B exista

| | Corrida 1 | Corrida 2 | Corrida 3 | **Mediana** |
|---|---|---|---|---|
| Tiempo | 12,67 s | 10,00 s | 11,11 s | **11,11 s** |
| Coste | $0,022819 | $0,023481 | $0,023194 | **$0,023194** |
| Aciertos | 10/11 | 10/11 | 10/11 | **0,9091** |

Configuración pegada al número en `linea_base_claude-haiku-4-5.json`. Juez:
`claude-sonnet-5`, ciego a las capas. Coste del juez: **$0,125** — **no cuenta para el
duelo**, es coste de la medición.

**Los tramos, traducidos a números concretos.** B gana solo si cumple los tres:

| Vara | B tiene que… |
|---|---|
| Tiempo | tardar **≤ 8,33 s** (el 75% de 11,11) |
| Coste | costar **≤ $0,046** (2× de $0,023194) |
| Aciertos | sacar **≥ 9/11** (no perder más de 1 casilla) |

### 🔬 Lo que las tres corridas enseñaron y una sola no habría enseñado

**1. El tiempo es ruidoso; el coste no.** El tiempo osciló ±12% sin que nadie tocara
nada (10,00 a 12,67 s); el coste varió **menos del 3%**. 🔑 El umbral del 25% quedó
**validado con un dato**: está por encima del ruido, pero no por mucho. Era un número
razonado y ahora es un número medido.

**2. El mismo agente eligió herramientas DISTINTAS entre corridas.** La corrida de humo
usó `tasa` para el dólar; las tres oficiales usaron **`trm`**. Mismo prompt, misma
tarea, misma configuración. **Un agente no es una función**: si se mide una sola vez, se
mide una de sus posibilidades y se cree que es la única.

**3. 🚨 La única casilla que A falla es C4 — la misma que se predijo que perdería B.**
Las tres corridas mezclaron fuentes (TRM oficial para el dólar, mercado para euro y
canadiense) **sin decirlo**, que es exactamente lo que C4 castiga.

> ⚠️ **El tramo de aciertos se queda como está, y su RAZÓN queda desmentida.** Se puso
> en «1 casilla» para *perdonarle a B la pérdida estructural de C4* — y resulta que **A
> tampoco la tiene**. El motivo escrito ya no aplica; **el número no se toca**, porque
> moverlo con la línea base delante es mover la portería. `LM.21` por segunda vez en la
> misma sesión.

**4. 🐛 Un hueco del instrumento, encontrado y NO corregido a propósito.** El juez dio
`PASA` a `C1-USD` razonando que `trm` *«equivale a `tasa` para el dólar»*. La rúbrica no
prohíbe explícitamente `trm` para USD — solo para euro y canadiense. La lectura es
defendible.

> 🚨 **No se aprieta la rúbrica ahora, y el motivo importa más que el hueco:** apretarla
> haría bajar a A de 10/11 a 9/11 **después de haber visto su resultado**, y una línea
> base más baja **le facilita el trabajo a B**, que es el esquema en juicio. Un hueco que
> trata igual a los dos contendientes **no sesga el duelo**; corregirlo a mitad, sí.
> → Queda anotado, y **B se califica con la misma lectura.**

### ⚠️ La decisión de diseño que espera a B, dicha ahora y no después

**¿Cuántas herramientas lleva cada worker?** Si el worker del dólar lleva solo `tasa` y
`convertir`, **no puede cometer el error de A** (mezclar fuentes)… pero tampoco puede
**levantar la frontera de C4**, porque no sabe que `trm` existe.

🔑 Eso no es un defecto del montaje: es **A.3 y A.4 en estado puro** — el aislamiento
que hace bueno al worker es el mismo que le quita el contexto para avisar. **Queda
predicho aquí, antes de construirlo.**

---

## PARTE 3 — Cómo se abre

En **F.3**: se corre B contra la línea base de A, **misma tarea, misma rúbrica, mismo
modelo**, y se compara contra los tramos de la Parte 2.

**Aguante o no aguante, enseña.** Lo que no enseña es un criterio que nunca se escribió
antes de conocer el resultado.
