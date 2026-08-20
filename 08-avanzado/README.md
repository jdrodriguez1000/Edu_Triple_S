# NIVEL 8 — MULTI-AGENTE: orquestador y workers

> **Un orquestador es un agente cuyas herramientas son otros agentes.**
> No es un concepto nuevo. Es el bucle del nivel 3 **anidado**.

Último nivel del mapa. Es el único que **abre sellando una predicción**, porque la
pregunta que de verdad importa aquí no se puede contestar al final.

---

## 🎯 QUÉ ES ESTE NIVEL, Y QUÉ NO

**Esto es un estudio del esquema multi-agente. No es construir una aplicación
multi-agente.**

> **Reencuadre del 2026-08-20 (sesión 90), y lo pidió él.** La primera versión de este
> plan estaba organizada alrededor del **duelo** (orquestador contra agente de una
> capa). Consecuencia: solo sobrevivían las piezas del esquema que el duelo
> necesitaba, y **el resto se caía sin que nadie lo notara**. La prueba: el mapa del
> curso promete *«orquestación, **agentes programados**, memoria y skills
> compartidas, y cuándo NO usar varios agentes»* — y *agentes programados* **no
> aparecía en el plan**. 🔑 **Un plan organizado alrededor de una medición no es un
> temario: es la lista de lo que hace falta para medir.**

Lo que cambia en la práctica:

- **El temario manda.** Se recorre pieza por pieza del esquema, y ninguna se salta.
- **Divisas es el vehículo, no el destino.** Algunas piezas se estudian con demos
  chicas sobre el agente de divisas. No hay que terminar un producto.
- **El duelo sigue vivo, pero es un hilo, no el eje.** Se sella al principio y se abre
  al final. Deja de ser el que decide qué se estudia.

---

## 📋 EL TEMARIO — las 21 piezas, en 7 bloques

Cada bloque **produce código que corre**. Ninguno es solo lectura.

| Bloque | Qué se estudia | Piezas |
|---|---|:-:|
| **0** | 🔒 El sobre: rúbrica, predicción y línea base — ✅ **CERRADO** (sesión 90) | 4 |
| **A** | Las piezas: worker, orquestador, y el contrato entre capas — ✅ **CERRADO** (sesión 91) | 4 |
| **B** | Las topologías: las formas que puede tomar un multi-agente | 5 |
| **C** | El harness a dos capas: lo que impide que explote | 6 |
| **D** | Lo compartido: memoria y skills entre workers | 2 |
| **E** | Agentes programados: el que corre sin nadie mirando | 2 |
| **F** | Medir y decidir: evals de dos capas, y se abre el sobre | 3 |
| **G** | Cierre del nivel y del curso | — |

---

### 🔒 BLOQUE 0 — El sobre sellado

**Corto a propósito.** Es el peaje que se paga para que el bloque F valga; no es un
proyecto en sí mismo. Cuatro piezas y un commit.

| # | Pieza | Produce | Estado |
|---|---|---|---|
| 0.1 | El **mapa mínimo** del esquema — lo justo para poder apostar | *(se lee)* | ✅ **hecha** — la cubrió la revisión del temario del 2026-08-20 |
| 0.2 | La **apuesta**: dónde gana, dónde pierde, y qué sería *«me equivoqué»* | `SOBRE.md` | |
| 0.3 | La **rúbrica corta** del duelo — la vara con la que *«aciertos»* significa algo | `rubrica_duelo.md` | |
| 0.4 | La **línea base** del agente de una capa: tiempo, coste, aciertos | `linea_base_*.jsonl` | |

### 🎯 La tarea del duelo ✅ DECIDIDA (2026-08-20)

> **«Tengo 1.000 dólares, 1.000 euros y 1.000 dólares canadienses. Dime cuánto es cada
> uno en pesos hoy, con la fuente y la fecha de cada cifra, y guárdame el reporte.»**

Cada moneda necesita `tasa` y después `convertir`, sin depender de las otras dos: **son
tres pedazos de verdad independientes.** Y el `guardar_reporte` del final es un fan-in
real — juntar tres resultados en un texto es el *contrato entre capas* de A.3 en su
forma más simple.

🐛 **Esta NO era la tarea original, y el motivo hay que conservarlo.** La primera
decisión fue *«compárame USD, EUR y CAD contra el peso en los últimos 30 días»*, y **no
se puede hacer con las seis herramientas**: `historial(dias)` pega contra
`datos.gov.co` y devuelve `"unidad": "COP por 1 USD"` — **la TRM es del dólar y de
nadie más**. No hay histórico de euro ni de canadiense en ninguna de las dos fuentes.
🔑 **La respuesta correcta a aquella tarea era admitir un límite**, así que la línea
base habría medido honestidad ante una frontera en vez de la tarea, y el duelo del
bloque F habría comparado otra cosa. El propio `rubrica.md` del 5b ya tenía la pregunta
que lo delataba (*«¿a cómo está el euro oficial en Colombia?»*, cuya respuesta correcta
es corregir la premisa) y aun así se escogió la tarea imposible.

⚠️ **Lo que se pierde, dicho en voz alta:** la tarea nueva es **más chica** — tres
workers con dos llamadas cada uno—, así que el fan-out tiene menos margen para ganar
tiempo. Se acepta a sabiendas: **agrandarla artificialmente sería amañar el duelo a
favor del esquema que el sobre existe para juzgar.**

### 🔒 Qué cubre el sello

El sello no protege *«una predicción sobre multi-agente»*. Protege un **trío**:

> **tarea + contendientes + tramos**

🚨 **Si cualquiera de los tres se mueve después del commit, el sello queda ANULADO** —
no corregido. Y el peligro no es hoy: es el día que se abra el sobre y el resultado no
guste. La frase que aparece sola en la cabeza es *«bueno, con otra tarea habría
ganado»*. **Cambiar la tarea después de medir es esa frase con más pasos.**

📌 Por eso cambiar la tarea **hoy** es gratis: no hay nada sellado todavía. Es
exactamente el motivo de que la tarea vaya antes que la apuesta.

### 📝 Notas de las piezas

**0.2 — la apuesta tiene DOS mitades, y aguantan cosas distintas:**

| Mitad | Qué dice | ¿Sobrevive a un cambio de tarea? |
|---|---|---|
| **General** | en qué clase de trabajo gana el esquema y en cuál pierde, con razones | **Sí.** Habla del esquema. Es lo que se quiere aprender |
| **Concreta** | los tramos de tiempo, coste y aciertos **de esta tarea** | **No.** Muere con la tarea |

Se escribe en dos pasadas: la general **ahora**, los tramos **después de 0.3** — no se
le pueden poner tramos a *«aciertos»* mientras no exista la escala que los define.

**0.3 — la rúbrica se escribe CORTA:** cuatro o cinco criterios, una página, partiendo
del `rubrica.md` del 5b. No es un rediseño. **La rúbrica completa de dos capas es del
bloque F**, y añadirla allá no rompe el sello: en el bloque 0 todavía no existe un
orquestador al que favorecer.

**0.4 — mismo modelo en los dos lados del duelo.** Si la línea base corre con haiku y
el orquestador con opus, lo medido es el modelo, no el esquema.

**Cierre:** `git commit`. La fecha del commit es lo que hace que la apuesta valga.

---

### 🧩 BLOQUE A — Las piezas

| # | Pieza | La pregunta que contesta |
|---|---|---|
| A.1 | **Worker**: un agente de una capa llamable como función ✅ **hecha** (`worker.py`) | ¿qué tiene un worker que no tenga tu agente del 5b? |
| A.2 | **Orquestador**: sus herramientas son workers ✅ **hecha** (`orquestador.py`) | ¿cómo se le da un agente a otro agente como herramienta? |
| A.3 | **El contrato entre capas** ✅ **hecha** (`contrato_divisa`) | ¿qué viaja del worker al orquestador, y qué se pierde? |
| A.4 | **Aislamiento de contexto** ✅ **hecha** (`aislamiento.py`) | ¿por qué cada worker tiene su propia conversación? |

⭐ El descubrimiento de A.1: **un worker no es una cosa nueva.** Es tu `ejecutar_agente`
con otro system prompt y menos herramientas. Media confusión del multi-agente se cae
sola el día que lo ves.

📌 A.3 es la pieza que más respuestas da del nivel: **la frontera entre las dos capas
es un texto.** El worker no le pasa su conversación al orquestador, le pasa un resumen.
Todo lo que no quepa ahí, se pierde.

**Corre:** `worker.py` y `orquestador.py`, en su versión más tonta: un worker, en serie.

#### ✅ A.1 — hecha el 2026-08-20 (sesión 91). `worker.py`

**Lo que se construyó:** `correr_worker(encargo, …)` → devuelve un **diccionario**.
Caja de dos herramientas (`tasa`, `convertir`), system prompt de especialista, su
propia conversación, su propio presupuesto y su propio registro.

**Corrida de demostración** (`1000 USD → COP`): **3 vueltas · 4,47 s · $0,007218**,
llamó `tasa` y `convertir`, en ese orden.

⭐ **El descubrimiento, y es el que se venía anunciando:** un worker **no es una cosa
nueva**. Es `ejecutar_agente` con otro system prompt y menos herramientas. Lo único de
verdad distinto es que **devuelve en vez de imprimir** — y esa línea es la que lo
vuelve usable como herramienta de otro agente.

🔑 **En un worker el sistema de permisos deja de ser una pregunta y se vuelve la caja
de herramientas.** No hay `input()` ni `pedir_permiso`: a un worker lo llama un
programa, no una persona, así que **no hay dónde decir que no**. Este worker no lleva
`guardar_reporte`, y por eso no puede escribir en el disco — no porque se le pregunte
antes. ⚠️ **Y el precio se dice en voz alta:** el usuario ya no ve pasar las
decisiones. La caja es la única defensa que queda, y por eso es diseño y no
configuración.

📌 **El menú y el puente se recortan LOS DOS.** El menú es lo que el modelo *ve*; el
puente (`FUNCIONES`) es lo que de verdad *puede correr*. Si solo se recortara el menú,
un modelo que pidiera `trm` "de memoria" **la encontraría y se ejecutaría**. El que
manda es el puente.

📊 **Un número que salió gratis** (con `count_tokens`, que no se cobra): el menú de A
con sus seis herramientas pesa **3.631 tokens por vuelta**; el del worker, con dos,
**1.815**. **La mitad, y se repaga en cada vuelta.** Es el impuesto permanente del
nivel 5b, ahora como palanca de diseño.

🚨 **Se decidió NO tocar `05b-proyecto/agente.py`, y la razón va escrita en el propio
`worker.py`.** Reutilizar su bucle exigía parametrizarlo, o sea editarlo — y ese
archivo **es el contendiente A, ya medido**. El sello del bloque 0 protege *tarea +
contendientes + tramos*. Se acepta repetir el bucle **a sabiendas**, y se repite lo
menos posible: de `agente` se importan las piezas que son **dato** (modelo, menú,
puente, cálculo del costo, política de reintentos). 📌 Copiar las `description` de las
herramientas habría sido peor que copiar el bucle: **el duelo del bloque F mediría
redacción de prompts y lo llamaría arquitectura.** 📌 Deuda anotada: los dos bucles se
pueden unificar **después** de abrir el sobre.

⚠️ **Una señal temprana, y NO se toca nada por ella.** Un worker costó $0,007218; tres
serían ~$0,0217 **antes** de sumar el orquestador, y el tramo del sobre es ≤ $0,046.
Cabe, pero el margen es más estrecho de lo que parecía. **Es una corrida, no una
medición** — y el sobre se abre en F.3, no aquí.

📌 **Lo que la predicción sellada dice y esta corrida NO prueba:** el worker citó su
fuente (*"tasa de mercado de open.er-api.com"*), que es justo lo que A no siempre hizo.
Una corrida no es un resultado — y la sesión 90 ya enseñó que **el mismo agente elige
herramientas distintas entre corridas**.

#### ✅ A.2 — hecha el 2026-08-20 (sesión 91). `orquestador.py`

**Lo que se construyó:** un agente con **UNA** herramienta, `consultar_moneda`, que por
dentro corre un worker. Su `tool` es un bloque JSON normal y corriente: `name`,
`description`, `input_schema`. **Nada en él dice que sea un agente.**

⭐ **La definición operativa, y decepciona a propósito:** un orquestador es *un agente
que llama a una función que resulta ser un agente*. En el 5b, `FUNCIONES["tasa"]` era
una función que pegaba contra una API; aquí `FUNCIONES_ORQ["consultar_moneda"]` es una
función que corre otro bucle. **El modelo de arriba no se entera, y no le hace falta.**

⚠️ **El orquestador NO lleva ni una herramienta de verdad** (ni `tasa`, ni `convertir`),
y no es minimalismo: **un orquestador que puede resolver la tarea él solo, la resuelve
él solo** — delegar le sale más caro que llamar a `tasa`. Lo medido en el bloque F sería
entonces el contendiente A disfrazado de B. 📌 Adelanta a medias la pieza **C.3**, que
llega a la misma decisión por seguridad y no por el experimento.

**Corrida de demostración** (las tres monedas, sin guardar el reporte):

```
arriba (orquestador):  $0,004418   ( 2 llamadas API,  2.343 entrada /  415 salida)
abajo  (3 workers):    $0,021647   ( 9 llamadas API, 18.002 entrada /  729 salida)
TOTAL:                 $0,026065   en 20,02 s
```

##### 🐛 Hallazgo 1 — pidió tres a la vez, y corrieron una detrás de otra

**Importancia: alta · Urgencia: no bloqueante.**

El orquestador pidió las tres monedas **en un solo turno** (`vuelta 1`, tres bloques
`tool_use`). Y aun así tardó 20 s, porque abajo se ejecutan en un `for`.

🔑 **«Pidió tres a la vez» y «corrieron tres a la vez» son cosas distintas.** Quien
decide si algo corre en paralelo es **el harness, nunca el modelo**. Es la misma forma
del desmentido de la sesión 90 (*A ya paraleliza*), ahora del otro lado: allá el modelo
paralelizaba y yo no lo sabía; aquí el modelo paraleliza y **el harness lo deshace**.
→ Es exactamente el hueco que abre el **bloque B.2**, y ahora tiene un número al lado.

##### 🐛 Hallazgo 2 — la fuente del CAD se perdió EN LA FRONTERA

**Importancia: alta · Urgencia: no bloqueante.**

La tabla final dice, para el dólar canadiense, fuente *«Tasa de mercado»* — sin nombre.
Para USD y EUR dice `open.er-api.com`.

**Y el dato SÍ existía.** La herramienta le devolvió al worker del CAD
`'fuente': 'mercado (open.er-api.com)'`. El worker respondió *«2.241.559 COP según la
tasa de mercado del 20 de agosto de 2026»* — **se comió el nombre al redactar**. El
orquestador no podía recuperarlo: solo recibió esa frase.

🔑 **Esto es A.3 ocurriendo en vivo, no nombrado: la frontera entre capas es un texto, y
lo que no quepa en él no se pierde con un error — se pierde en silencio.** El de arriba
ni siquiera puede echarlo de menos, porque no sabe que existía. Es `LM.15` con una capa
más: **un dato que falta no da un fallo, da una casilla que parece llena.**

📌 Y la causa raíz está a la vista: **los tres workers, con el mismo system prompt y la
misma tarea, redactaron de tres formas distintas.** La sesión 90 ya lo había medido —
*un agente no es una función*—; aquí se ve **lo que cuesta**. → El arreglo no es pedirle
al worker que redacte mejor: es que la frontera deje de ser prosa libre. **Eso es A.3.**

##### 🐛 Hallazgo 3 — el orquestador hizo aritmética de cabeza

**Importancia: media · Urgencia: no bloqueante.**

Nadie le pidió un total, y lo dio: *«en total… 8.951.248 pesos»*. La suma **está bien**
(3.099.309 + 3.610.380 + 2.241.559). Pero la hizo **sin herramienta**, y su propio
system prompt dice *«nunca inventes ni estimes una cifra»*.

🔑 **Salió bien, y ese es el problema:** un número correcto no distingue *«lo calculó
bien»* de *«acertó»*. Un orquestador sin herramientas no se queda callado — **rellena**.
📌 Se anota y no se corrige hoy: tocar el system prompt del de arriba después de ver una
corrida es apretar la vara con el resultado a la vista, que es justo lo que el bloque 0
decidió no hacer con la rúbrica.

##### ⚠️ Y el número incómodo, dicho entero

La demo costó **$0,026065 en 20,02 s**. La línea base de A fue **$0,023194 en 11,11 s** —
y eso que la demo **ni siquiera guardó el reporte**, que la tarea del duelo sí exige.

**Es UNA corrida contra una mediana de tres, y no es el duelo.** No se anota como
resultado y no se toca nada. 📌 Pero la dirección coincide con el desmentido sellado de
la sesión 90: **el margen que se le suponía al paralelo, A ya lo tenía cobrado.**
📌 Dónde se fue el dinero está a la vista en la factura por capa: **18.002 tokens de
entrada abajo contra 2.343 arriba.** Cada worker repaga su menú en cada una de sus
vueltas, y son tres workers. **El impuesto del nivel 5b, multiplicado por la capa.**

#### ✅ A.3 — hecha el 2026-08-20 (sesión 91). `contrato_divisa` en `worker.py`

🔑 **Esta pieza NO la pidió el plan: la pidió un defecto medido.** El hallazgo 2 de A.2
—la fuente del CAD perdida en la frontera— es literalmente el motivo por el que se
construyó, y se construyó apuntándole.

**Lo que se construyó:** el worker deja de entregar una frase y entrega **seis campos**
con nombre — `moneda, monto, pesos, tasa, fuente, fecha` — más una lista, `faltan`, con
los que no pudo llenar. El orquestador ya no recibe prosa.

⭐ **Y el contrato NO se le pide al modelo: se arma con lo que YA pasó por el harness.**
`fuente` y `fecha` venían exactas dentro del `tool_result` de `tasa`. Estaban en Python.
Pedírselas otra vez al modelo sería **pagar tokens para que nos repita, de memoria y con
sus palabras, algo que ya teníamos exacto**.
→ **Regla:** antes de pedirle un dato al modelo, mira si ya pasó por tu harness. Lo que
pasa por el harness es exacto y gratis; lo que pasa por el modelo es aproximado y se paga.

##### ✅ La prueba de que mordió, y es la parte bonita

En la corrida nueva, el worker del CAD **volvió a comerse el nombre de la fuente en su
frase** (*«según la tasa de mercado del 20 de agosto de 2026»*, otra vez sin
`open.er-api.com`). Y la respuesta final del orquestador, en cambio, dice:

```
1.000 CAD = $2.241.559 COP
  Fuente: mercado (open.er-api.com)
```

🔑 **No se arregló al worker: se le quitó la decisión.** El defecto de redacción sigue
ahí y ya no importa, porque la prosa dejó de ser lo que cruza. **Un arreglo que necesita
que el modelo se porte bien no es un arreglo — es una petición.**

##### ⚠️ Lo que el contrato SÍ pierde, y es la mitad que no se puede olvidar

La prosa del worker **ya no sube**. Si el worker hubiera notado algo raro —*«esta tasa
parece de anteayer»*— esa advertencia no llega arriba: **no hay campo donde quepa**.

🔑 **UN CONTRATO NO ES UNA FORMA DE NO PERDER NADA: ES ELEGIR QUÉ PERDER.** La prosa
perdía cosas al azar y sin avisar; el contrato pierde **lo que decidimos**, y `faltan`
dice cuándo. Esa es toda la diferencia, y no es pequeña: es la diferencia entre una
pérdida y un silencio.

📌 Comprobado gratis, sin modelo, dándole salidas de herramienta a mano: si `tasa` falla,
el contrato devuelve `faltan: ['tasa', 'fuente', 'fecha']` y sigue trayendo los pesos.
**Una frase no sabe qué le falta; un contrato, sí.**

##### 💰 Lo que costó el arreglo

```
A.2 (prosa):     $0,026065   ·  orquestador 2.343 tokens de entrada
A.3 (contrato):  $0,026295   ·  orquestador 2.544 tokens de entrada
```

**+$0,00023 y +201 tokens.** El contrato es *ligeramente* más largo que la prosa, y no
al revés. 📌 El tiempo bajó de 20,02 s a 15,34 s y **eso NO es mérito del contrato**: la
sesión 90 midió ±12 % de ruido en el tiempo sin tocar nada. Atribuirlo al arreglo sería
`LM.16` — quedarse con el titular que gusta.

##### 🐛 Y el hallazgo 3 de A.2 no se repitió — lo cual es peor, no mejor

**Importancia: media · Urgencia: no bloqueante.**

En A.2 el orquestador sumó las tres monedas de cabeza sin que nadie se lo pidiera. En
esta corrida **no lo hizo**, y no se tocó su system prompt.

🔑 **Un defecto que aparece en 1 de 2 corridas no está arreglado: es intermitente.** Y es
justo el que se marca como resuelto por error, porque la corrida siguiente sale limpia.
Es *«un agente no es una función»* (sesión 90) del lado que hace daño: **medido una vez,
un defecto también se mide una sola de sus posibilidades.**

#### ✅ A.4 — hecha el 2026-08-20 (sesión 91). `aislamiento.py`

**La respuesta habitual —*«cada worker tiene su conversación para ahorrar tokens»*— es
FALSA**, y los números propios lo dicen:

```
A (una conversación):  ~17.850 tokens de entrada,  4 vueltas
B (tres aisladas):     ~20.540 tokens de entrada, 11 llamadas
```

**El aislamiento salió más caro.** Si la razón fuera el ahorro, la respuesta correcta a
A.4 sería *«no lo hagas»*.

##### 🐛 Tres hipótesis, dos falsas, y las dos eran mías

Se dejan escritas con sus números, porque **el camino equivocado es la mitad de la
lección** y borrarlo dejaría una conclusión que parecería obvia sin serlo.

| | Hipótesis | Resultado |
|---|---|---|
| ① | *«B gana con MÁS piezas»* | ❌ con 12 monedas, B cuesta **3×** lo de A |
| ② | *«B gana con piezas MÁS GORDAS»* | ❌ con documentos de 2.000 tokens, B solo gana en el caso más chico |
| ③ | *«B gana con MÁS VUELTAS POR PIEZA»* | ✅ con 8 pasos por pieza: **A = 140.796, B = 69.544** |

```
① MÁS PIEZAS (~150 tokens por herramienta — el caso de divisas)
   piezas    A: una capa    B: dos capas         B − A
        3         17.404         20.440       +  3.036   A más barato
        6         19.866         38.918       + 19.052   A más barato
       12         24.790         75.874       + 51.084   A más barato

② PIEZAS MÁS GORDAS (~2.000 tokens por herramienta)
        3         33.838         31.396       −  2.442   B MÁS BARATO
        6         52.734         60.830       +  8.096   A más barato

③ MÁS VUELTAS POR PIEZA (3 piezas fijas)   ←── AQUÍ ESTÁ LA PALANCA
  vueltas/pieza
        2         29.013         20.323       −  8.690   B MÁS BARATO
        4         60.326         34.742       − 25.584   B MÁS BARATO
        8        140.796         69.544       − 71.252   B MÁS BARATO
```

📌 **Todo medido con `count_tokens`, que no se cobra: $0,00.** Con salidas de herramienta
reales copiadas del registro — una simulación con datos amables no mide, adorna.

##### ⭐ El mecanismo, y es una multiplicación

> **lo que cuesta una conversación ≈ (lo que hay dentro) × (cuántas vueltas)**

Las piezas y su tamaño mueven el **primer** factor. Solo las vueltas mueven el
**segundo** — y el segundo **multiplica**. Por eso ① y ② no despegaban: estaban
empujando el factor que suma.

🚨 **Y ahí apareció lo que de verdad salva a la conversación única: EL LOTE.** En ① el
modelo pide las tres `tasa` en un mismo turno, así que tres monedas caben en cuatro
vueltas. En ③ los pasos van encadenados, **no se pueden agrupar**, y tres piezas de ocho
pasos son 25 vueltas — cada una releyendo las otras dos piezas enteras.

🔑 **Lo que hace explotar una conversación compartida no es el trabajo: es la DEPENDENCIA
entre pasos**, que es justo lo que impide agruparlos. 📌 Es el desmentido de la sesión 90
(*«A ya paraleliza»*) visto desde el otro lado: **esto explica por qué aquello le
bastaba.**

⚠️ **Consecuencia para el duelo, dicha ANTES de abrir el sobre:** la tarea de divisas es
**el terreno más hostil posible para B** — pasos independientes y agrupables, dos por
moneda. **No se cambia.** Cambiarla ahora sería amañarla, y es exactamente la frase
contra la que existe el sello.

##### 🔬 La otra mitad de A.4: la contaminación. Medida, y NO ocurrió.

Se le metió al worker del EUR la conversación del USD ya hecha, para ver si tomaba
prestada la tasa ajena (3099,31) en vez de pedir la suya.

**No lo hizo.** Llamó a `tasa` para el euro con normalidad y dio el mismo resultado que
el worker limpio. Lo único que cambió fue la factura:

```
limpio     : 6.011 tokens de entrada · $0,007231
contaminado: 7.175 tokens de entrada · $0,008345      (+19 % · +$0,0011)
```

🔑 **Se anota tal cual, sin adornarlo: una alarma que no suena también es un resultado.**
El daño medido no fue una respuesta mala — fue **pagar un 19 % más por cargar la
conversación de otro sin usarla para nada**.

⚠️ **Y lo que este experimento NO demuestra**, dicho para que nadie lo lea de más: que
la contaminación *no pueda* ocurrir. Es **una corrida**, sobre un caso donde la respuesta
correcta era evidente (pedir la tasa del euro). Un caso donde el dato ajeno *sirviera a
medias* es otro experimento. **Queda nombrado, no demostrado.**

---

### 🔀 BLOQUE B — Las topologías

**Este bloque es el que contesta *«cuándo se usa multi-agente»* de verdad**, porque la
respuesta no es sí o no: es *cuál forma*.

| # | Forma | Cuándo tiene sentido |
|---|---|---|
| B.1 | **Pipeline** (en serie): la salida de uno entra al siguiente — ✅ **hecha** (sesión 92) | pasos que dependen unos de otros |
| B.2 | **Fan-out / fan-in** (en paralelo) — ✅ **hecha** (sesión 93) | pedazos independientes ← *la tarea del duelo* |
| B.3 | **Router**: elige UN worker, no varios — ✅ **hecha** (sesión 94) | muchos casos distintos, uno a la vez |
| B.4 | **Supervisor**: el orquestador juzga y reenvía — ✅ **hecha** (sesión 94) | cuando la primera respuesta puede no servir |
| B.5 | **Profundidad > 2**: un worker que a su vez orquesta | casi nunca — y hay que saber por qué |

**Corre:** las cuatro primeras sobre el agente de divisas, con la misma tarea, para
poder verlas una al lado de la otra.

---

#### ✅ B.1 — EL PIPELINE (sesión 92) → `pipeline.py` + `verificador.py`

**Lo primero, porque es lo que más se confunde.** El agente del 5b ya tenía pasos en
orden: `tasa` corre antes que `convertir`, y la prueba está en la firma —
`def convertir(monto, de, a, tasa)`, la tasa **entra como parámetro**. Es una
dependencia de verdad. **Y aun así no es un pipeline.**

🔑 **La pregunta de una topología no es *«¿hay pasos en orden?»* —eso lo tiene casi
cualquier agente—. Es *«¿QUÉ está encadenado: herramientas o agentes?»*.**

| | Quién decide el orden | Qué viaja |
|---|---|---|
| herramienta → herramienta | **el modelo**, en una conversación | un dato exacto, en un `tool_result` |
| agente → agente | **tu código**, entre dos conversaciones | lo que el primero **entendió** |

**Por eso la tarea del duelo no sirve para B.1** y hubo que inventar otro trabajo con
las mismas seis herramientas: recolector → redactor → archivista. Las tres monedas son
independientes; el euro no espera al dólar.

🚨 **EL DESCUBRIMIENTO: NO HAY ORQUESTADOR.** El orden es fijo, y un orden fijo son tres
líneas seguidas de Python. **Una topología no necesita un agente que la dirija** — lo
necesita cuando el camino DEPENDE de lo que se encuentre (router B.3, supervisor B.4).
📌 Dicho al revés, que es como se recuerda: **el modelo se paga por decidir. Si no hay
nada que decidir, no hay nada que pagar.**

⏱️ **El tiempo de un pipeline es la SUMA, nunca el máximo**, y eso no es un defecto
optimizable: es la definición. **El paralelismo que sí existe vive DENTRO de un
eslabón** —la etapa 1 hace 6 llamadas en 3 vueltas— **nunca ENTRE eslabones**.

##### 🐛 El defecto medido, y el arreglo mal hecho antes del bueno

Primera corrida. Sigue un solo campo cruzando dos fronteras:

```
harness    "actualizado": "Thu, 20 Aug 2026 00:02:31 +0000"
etapa 1    "— 20 de agosto de 2026"
etapa 2    "**Fecha de consulta:** 20 de agosto de 2026"
```

La etapa 2 **le puso una etiqueta que nadie le dio**. `actualizado` es cuándo la fuente
movió la tasa; *«fecha de consulta»* es cuándo preguntamos nosotros. Si la API llevara
tres días sin actualizar, el informe diría *«consultado hoy»* sobre una tasa vieja.

🚨 **Y el primer arreglo fue una PETICIÓN.** Se le mandó al archivista la verdad cruda
del harness pidiéndole que comparara. Contestó **«coinciden exactamente con los datos
verificados»** teniendo `actualizado` en pantalla al lado del borrador que decía *fecha
de consulta*. Costó **+907 tokens (+34 % en esa etapa) para no encontrar nada**, y los
dos informes salieron **idénticos byte a byte** (mismo `md5`).

⭐ **UNA COMPARACIÓN ES UN `if`, NO UNA INSTRUCCIÓN EN UN PROMPT.** Es la frase de A.3
—*un arreglo que necesita que el modelo se porte bien no es un arreglo*— repetida un día
después por quien la había escrito. → `verificador.py`: cuesta $0,00, corre **siempre**
entre la etapa 2 y la 3 (sin parámetro para saltárselo, que es la sesión 83 de TEAPP), y
**bloquea el archivado** si hay una cifra que ninguna herramienta devolvió.

📉 Medido: la etapa 3 pasó de **$0,008272 a $0,004671 (−44 %)** y de 4027 a 2946 tokens
de entrada. **Más barato Y más correcto** — porque el trabajo se movió al sitio donde era
determinista.

##### 🚨 Y en la corrida siguiente el freno nuevo NO vio nada. Las tres deudas.

**`D-B1.1` — el límite declarado se disparó en la primera corrida en vivo.**
El verificador trae un test, el nº 7, que comprueba **que falla**: *«una paráfrasis no se
caza»*. La corrida siguiente escribió **`Fecha del informe:`** en vez de *fecha de
consulta*, y el freno pasó de largo. 🔑 **Lo grave no es el hueco: es que el cero era
compatible con dos mundos** —*«el borrador está limpio»* y *«mi freno es estrecho»*
pintan la misma pantalla— **y solo leerlo a mano los separó**, que es justo lo que el
freno existía para evitar. (Esta vez el borrador **sí** estaba bien: la fecha correcta
viajaba en la Nota.) → **`LM.15` con el instrumento ciego siendo el propio, escrito ese
mismo día.**

**`D-B1.2` — el defecto es intermitente: 1 de 2 corridas.**
Mismo prompt, mismo modelo, misma entrada, etiqueta distinta. Ya estaba escrito en
`PROGRESO.md` desde la sesión 91: *un defecto que aparece en 1 de 2 corridas no está
arreglado, es intermitente — y es justo el que se marca como resuelto por error, porque
la siguiente sale limpia*. **Es exactamente lo que pasó.** Sin la corrida anterior
delante, hoy la frontera quedaría marcada como resuelta.

**`D-B1.3` — el archivista no guarda el borrador: lo vuelve a teclear.**
El archivo guardado termina en `---`, que era **el separador del encargo**, no del
informe. 345 tokens de salida copiando un texto **que Python ya tenía en una variable**,
y el `---` es la prueba barata de que copiar por el modelo pierde. 🔑 Es *el modelo se
paga por decidir* apuntando a esta misma etapa: quitada la verificación, al archivista no
le queda nada que decidir — guardar un texto con un nombre dado es un `write_text`.
⚠️ **Y deja una pregunta que el bloque B debe contestar antes de cerrar: ¿un pipeline de
3 agentes que en realidad necesita 2 sigue siendo un pipeline de 3?**

📌 **Las tres se anotan y no se pagan hoy, a sabiendas:** son variaciones de lecciones ya
medidas, y B.2 entra con una deuda que lleva dos sesiones esperando **con su número al
lado**.

---

#### ✅ B.2 — EL FAN-OUT / FAN-IN (sesión 93) → `fan_out.py`

**B.1 era una línea de montaje. B.2 es repartir sobres.**

Tres encargos que **no se necesitan entre sí**, tres mensajeros que salen por la puerta
**al mismo tiempo**, y alguien que junta lo que traen. Son dos movimientos con dos
nombres: **fan-out** (abrir el abanico, repartir) y **fan-in** (cerrarlo, juntar).

**La condición es una sola, y sin ella no hay nada que discutir: los pedazos tienen que
ser INDEPENDIENTES.** El dólar no necesita saber nada del euro. Si el segundo encargo
necesitara el resultado del primero, no hay fan-out posible: eso es un pipeline, y su
tiempo es la suma **por definición**.

📌 Por eso la tarea del duelo **sí** sirve aquí y **no** servía en B.1, donde hubo que
inventar otro trabajo. **La forma de la tarea decide la topología, no al revés** — que es
la frase con la que abrió el bloque B.

---

##### ⭐ La frase del día, y ya estaba medida desde la sesión 91

En la corrida de A.2 el orquestador pidió las **tres monedas en un solo turno**: tres
bloques `tool_use` en la vuelta 1. **El modelo hizo el fan-out perfecto.** Y aun así
tardó **20,02 s**, porque abajo se ejecutaban en un `for`.

> 🔑 **«Pidió tres a la vez» y «corrieron tres a la vez» son cosas distintas.**
> Quien decide si algo corre en paralelo es **el harness, nunca el modelo.** El modelo
> solo puede *pedirlo*.

Todo B.2 es el harness contestando que sí.

---

##### 💰 Lo que el fan-out compra, y lo que NO

| | compra | no compra |
|---|---|---|
| ⏱️ **Tiempo** | de la **suma** al **máximo**: manda el más lento | — |
| 💰 **Coste** | — | **exactamente las mismas llamadas**, los mismos tokens, el mismo precio |

⚠️ **Confundir esas dos es el error clásico del tema.** El paralelismo no es una
optimización de costo: es una optimización de **reloj**. Si lo que duele es la factura,
el fan-out no sirve para nada — eso es **C.6** (modelo y esfuerzo por capa), que es 5×.

📌 Y de ahí sale la regla para leer el resultado: **si el tiempo bajó mucho y el coste no
se movió, eso no es que algo salió mal — es la definición.** Si el coste **sí** se movió
mucho, el experimento está sucio: el modelo dio otro número de vueltas, y entonces no
cambió una variable, cambiaron dos.

---

##### 🔓 El descubrimiento de B.2: el paralelismo no se AÑADE, se DESBLOQUEA

Lo que había que arreglar **no era la velocidad**. Era **lo compartido**. En serie,
«compartido» y «mío» no se distinguen, porque solo hay uno. **El paralelismo no crea los
recursos compartidos: los DESTAPA.** Eran tres, y las tres estaban ahí desde A.2:

| # | Lo compartido | Qué se rompe | Arreglo |
|---|---|---|---|
| 1 | **el archivo de registro** | dos líneas se entrelazan y el `.jsonl` deja de ser `.jsonl` | `_CANDADO_REGISTRO` |
| 2 | **la contabilidad** | `d[k] += x` son **tres** operaciones (leer, sumar, escribir); una suma se pierde **sin dar error** | `_CANDADO_CONTABILIDAD` |
| 3 | **la pantalla** | tres conversaciones encimadas, ilegibles | ⚠️ **no se arregla con un candado** |

🔑 **La tercera es la que enseña.** Un candado sobre la pantalla vuelve a poner en fila
justo lo que querías en paralelo — el arreglo no es proteger el recurso, es **dejar de
usarlo en vivo**: los workers corren con `verboso=False` y al final se dibuja la **línea
de tiempo**, que además es el único sitio donde el solapamiento **se ve**.

📌 **Y fíjate en el precio de los candados: en serie no cuestan NADA**, porque nunca hay
que esperar a nadie. Por eso se ponen siempre, no «cuando haga falta».

⚠️ **La nº 2 es la peor de las tres, y es la más callada.** Lo que se pierde cuando una
suma se evapora **es la factura** — el dato por el que existe todo el bloque F. Es `LM.15`
otra vez: no da un número falso con una alarma, da un número **menor** con la pantalla
igual de verde.

---

##### 🔧 El refactor: la topología dejó de ser una línea de código y pasó a ser un parámetro

El `for` de `orquestador.py` salió del bucle y se convirtió en dos funciones sueltas —
`ejecutar_un_bloque()` y `reparto_en_serie()` — y el bucle ahora recibe `reparto` **por la
puerta**.

```python
bloques = [b for b in respuesta.content if b.type == "tool_use"]
resultados = reparto(bloques, contabilidad, verboso)
```

⭐ **Y `ejecutar_un_bloque` NO SABE si es uno de tres en fila o uno de tres a la vez.**
Esa ignorancia es lo que hace que el reparto sea intercambiable: si supiera de hilos,
cambiar la topología obligaría a reescribirla.

📌 **Es un parámetro y no un `if`** a propósito. Con `if paralelo:` dentro del bucle, cada
topología nueva del bloque B (router, supervisor) añadiría una rama ahí dentro. Entrando
por la puerta, **el bucle no crece nunca.**

✅ **Por defecto sigue siendo `reparto_en_serie`**, así que A.2 corre exactamente igual que
antes y **sus números medidos siguen siendo suyos**.

---

##### 🪤 La trampa que `pool.map` desactiva, y que nadie habría visto

`pool.map` devuelve **en el orden en que se entregaron**, no en el que terminaron.

Si el CAD termina primero, su resultado **no** debe adelantarse al del USD. Los
`tool_use_id` protegerían la correspondencia —el modelo no confundiría las cifras— pero el
registro y el informe quedarían **barajados**, y eso no lo caza nadie hasta leer una tabla
con las filas cambiadas de sitio.

> 🔑 **En paralelo, el orden de LLEGADA deja de ser el orden de SALIDA.** Si tu código
> daba las dos por hechas, ahora son dos cosas.

---

##### ⚠️ Un tope de hilos, y no es decorativo: `MAX_EN_VUELO = 4`

«Paralelo» sin tope significa que si el modelo pide 40 monedas, **salen 40 peticiones a la
vez**. Eso es un `429`, y peor: es una forma **nueva** de quemar dinero que en serie no
existía. En fila, el presupuesto de arriba te frena antes de la número 20; **a la vez, las
40 ya salieron.**

🔑 **El paralelismo mueve el gasto de «poco a poco» a «todo de golpe», y un tope que se
mira ANTES no es lo mismo que uno que se mira DESPUÉS.** 📌 Es media pieza **C.2** asomando,
igual que A.2 asomó C.3.

---

##### 🆓 Las pruebas — sin modelo, sin red y sin gastar un centavo

`python fan_out.py --test` → **las 8 en verde** (la nº 8 llegó con `D-B2.1`, más abajo). Igual que `verificador.py` en B.1: el
archivo que más enseña vuelve a costar **$0,00**.

| # | Qué prueba | Por qué está |
|---|---|---|
| 1 | el orden se conserva **aunque el primero sea el más lento** | si el orden se rompiera, se rompería justo así |
| 2 | un `tool_result` por cada `tool_use`, ni uno más | — |
| 3 | ⭐ **en serie = la suma (0,45 s); en paralelo = el máximo (0,31 s)** | **demuestra la afirmación central del bloque, con relojes de verdad y factura cero** |
| 4 | la contabilidad cuadra con hilos: 3 workers, $0,003, 9 llamadas | es lo que el candado nº 2 protege |
| 5 | 🔓 **sin candado, dos sumas se convierten en una** | enseña **por qué** existe el candado |
| 6 | un worker que revienta **no tumba a los otros dos** | en paralelo la apuesta sube: una excepción que escapara del hilo mataría la tanda entera |
| 7 | el registro escrito desde hilos **sigue siendo JSONL válido** | es lo que el candado nº 1 protege |
| 8 | dos vueltas de reparto **se acumulan en la línea de tiempo, no se pisan** | llegó con `D-B2.1`, que la corrida pagada destapó |

⭐ **La nº 3 es la joya del archivo.** Con tres workers falsos que duermen `0,30 / 0,10 /
0,05 s`, mide **lo que de otro modo habría que pagar para ver**: serie `0,45 s` (la suma
exacta), paralelo `0,31 s` (el máximo). **La afirmación del bloque dejó de ser una
afirmación.**

⚠️ **Y la nº 5 dice exactamente lo que es: DEMUESTRA EL MECANISMO, no caza una carrera al
vuelo.** Una carrera de verdad es intermitente, y una prueba intermitente es peor que
ninguna (`D-B1.2`, sesión 92). Así que las tres operaciones que esconde `+=` se separan a
mano. 🔑 **Nombrar un mecanismo no es haberlo medido**, y una prueba que finge medir lo
que solo ilustra es `LM.15` con bata de laboratorio.

📌 **Las pruebas desvían el registro a un archivo temporal**, y es deliberado: es la
lección de la sesión 50 de TEAPP (`T-072`), donde **el instrumento de medida escribía en
los datos de verdad**. Unas pruebas que ensucian el `.jsonl` real convierten el registro de
las corridas **pagadas** en una mezcla de pagadas e inventadas — y eso no se nota nunca.

📌 **Y sin argumentos, `fan_out.py` corre las PRUEBAS, no la demo.** Lo que cuesta dinero
se pide con todas las letras.

---

##### 📊 LA MEDICIÓN — `--ambos`, dos corridas seguidas, una sola variable

|  | TIEMPO | COSTE | LLAMADAS API |
|---|---|---|---|
| **serie** | **18,22 s** | $0,026387 | 11 |
| **paralelo** | **8,91 s** | $0,026984 | 11 |
| | **−51 %** | **+2,3 %** | **iguales** |

**Once llamadas a cada lado.** Es la primera cosa que hay que mirar: si ese número se
hubiera movido, no habría cambiado una variable, habrían cambiado dos, y el tiempo no
valdría nada.

---

##### ⭐ Y no fue solo «más rápido»: LA ARITMÉTICA CIERRA EN LOS DOS LADOS

Esto es lo mejor de la corrida, y no estaba planeado.

```
capa de arriba (2 llamadas del orquestador):   3,61 s  en serie
                                               3,68 s  en paralelo   <- constante
workers:  serie     6,11 + 4,72 + 3,78  = SUMA 14,61 s
          paralelo  3,67 / 4,09 / 5,22  = MÁX   5,22 s

predicho serie    = 3,61 + 14,61 = 18,22 s   ·   MEDIDO 18,22 s
predicho paralelo = 3,68 +  5,22 =  8,90 s   ·   MEDIDO  8,91 s
```

🔑 **No se midió que el paralelo fuera más rápido: se midió que cada uno tarda EXACTAMENTE
lo que su modelo predice.** Uno es la suma, el otro es el máximo, y las dos cuentas cuadran
al centésimo. Un número más bajo cabe en muchas explicaciones; **una cuenta que cierra en
los dos lados, en una sola.**

📌 **La capa de arriba salió constante (3,61 contra 3,68 s) sin que nadie la vigilara**, y
eso es una comprobación independiente: confirma que lo único que cambió está abajo.

---

##### 🖼️ La línea de tiempo — donde el solapamiento SE VE

```
{'moneda': 'USD', ...} |####################################                |  0.02 ->  3.69s
{'moneda': 'EUR', ...} |#########################################           |  0.02 ->  4.11s
{'moneda': 'CAD', ...} |####################################################|  0.02 ->  5.23s
                       +----------------------------------------------------+
suma de los trozos: 12.98s   el más lento: 5.22s   reloj de pared: 5.23s
```

Los tres arrancan en `0,02 s`. **Suma 12,98 s de trabajo, reloj de pared 5,23 s.**

🔑 Sin este dibujo, «corrieron a la vez» sería una afirmación: un total más bajo es
compatible con *se solaparon* y con *hoy la API estuvo rápida*. **Es `D-B1.1` de la sesión
92 evitado por construcción** — allí un cero cabía en dos mundos y hubo que leer a mano
para separarlos; aquí las barras los separan solas.

---

##### 🐛 Hallazgo 1 — el coste SÍ se movió, y NO fue la topología

**Importancia: alta · Urgencia: no bloqueante.**

El propio informe avisa: *«si la de coste se movió mucho, el experimento está sucio»*.
Se movió **+2,3 %**. Así que la alarma sonó y hubo que ir a mirar en vez de creerse el
titular. Repartida por capas:

| capa | serie | paralelo | |
|---|---|---|---|
| abajo (9 llamadas de los workers) | $0,021726 | $0,021751 | **+0,1 %** |
| arriba (2 llamadas del orquestador) | $0,004661 | $0,005233 | **+12,3 %** |

**Todo el delta está arriba, y la causa se ve a simple vista en la salida:** en serie el
orquestador respondió con una **lista**; en paralelo, con una **tabla de markdown**. Más
tokens de salida. **La topología no tocó la factura — la redacción sí.**

✅ **La capa de abajo se movió un 0,1 %**, que es exactamente lo que debía pasar: mismas
9 llamadas, mismos tokens, mismo precio. **El fan-out compró reloj y no compró nada más.**

🔑 **Y se anota como hallazgo aunque el veredicto sea «no pasa nada», porque una alarma que
se apaga antes de entregarse también es un dato** (sesión 84). El reflejo que la apagó —ir
a mirar el reparto por capas en vez de reportar el 2,3 %— es el que hacía falta.

---

##### 🐛 Hallazgo 2 — el más lento manda, y CUÁL es el más lento cambia de corrida

**Importancia: alta · Urgencia: no bloqueante.**

El worker del **CAD** fue **el más rápido en serie (3,78 s)** y **el más lento en paralelo
(5,22 s)**. No hay nada especial en el CAD: es ruido de latencia.

🔑 **Pero en un fan-out el ruido no se promedia: se acumula en el peor.** El tiempo total
no es la latencia *media* de un worker, es **el máximo de tres sorteos** — que es peor que
la media, y **más variable** que ella. Cuantos más pedazos repartas, más probable es que
al menos uno salga lento, y ese arrastra a todos.

📌 Consecuencia práctica para el bloque C: **un fan-out ancho necesita un tope de tiempo
por worker (`C.4`) más que uno estrecho**, y por una razón que no es la fiabilidad — es
aritmética.

---

##### ✅ ¿Y si el ruido explicara el resultado? Se comprobó, y no

Los workers del paralelo sumaron 12,98 s y los de la serie 14,61 s: un 11 % de diferencia,
**dentro del ±12 % de ruido medido en la sesión 90**. Así que la pregunta es legítima:
¿ganó el paralelo, o le tocaron workers más rápidos?

**Se hace la cuenta en el caso peor.** Si los del paralelo hubieran sido tan lentos como
los de la serie, el máximo habría subido de 5,22 a ~5,88 s y el total a **9,56 s**: sigue
siendo un **−48 %**.

🔑 **La conclusión no depende del ruido, y eso se dice DESPUÉS de comprobarlo, no antes.**

---

##### 🐛 D-B2.1 — un defecto que la corrida destapó, arreglado el mismo día

**Importancia: media · Urgencia: no bloqueante.**

`ULTIMA_LINEA_DE_TIEMPO` se **asignaba**, así que guardaba solo la **última** vuelta de
reparto. En esta corrida el orquestador dio **una sola** vuelta de herramientas — así que
el dibujo salió correcto **por casualidad**.

Con dos vueltas, la línea de tiempo habría enseñado la mitad del trabajo **sin avisar de
que faltaba la otra mitad**. 🔑 **No habría dado un dato falso: habría dado silencio sobre
lo que faltaba, y un dibujo incompleto se lee como uno completo.** Es `LM.15` con el
instrumento ciego siendo, otra vez, el que se escribió ese mismo día — igual que en B.1.

→ Arreglado: se **acumula**, y cada tramo se etiqueta con su vuelta (`v1`, `v2`) para que
dos vueltas se distingan de una. → Y con **prueba nº 8**, porque
**⚠️ un arreglo que no se ha visto morder es una nota, no un arreglo (`LM.13`)**: en esta
tarea el orquestador siempre da una vuelta, así que en vivo sigue sin verse.

---

##### 🆓 Las pruebas quedaron en 8, y siguen costando $0,00

`python fan_out.py --test` → **las 8 en verde.** La nº 8 es la que cubre `D-B2.1`.

📌 **Y el registro real se verificó después de la corrida pagada**, no solo el de las
pruebas: 28 líneas en el del orquestador y 151 en el de los workers, **ninguna rota**,
escritas desde tres hilos. Los candados mordieron de verdad.

---

#### ⏭️ EL ARRANQUE DE B.3 — escrito al cerrar la 93, **sin una línea de código**

⚠️ **Aquí no hay lección de B.3, y es deliberado.** Esto es la pista de aterrizaje: qué
pregunta abre, qué hereda y qué hay que sellar **antes** de construir — el mismo orden que
funcionó en la 90, donde la apuesta se sellaba antes de teclear.

---

##### 🔑 Por qué B.3 es distinta de las dos anteriores

| | quién decide el camino | ¿hace falta un orquestador? |
|---|---|---|
| **B.1 pipeline** | está fijo de antemano | **no** — un orden fijo son tres líneas seguidas |
| **B.2 fan-out** | está fijo de antemano | **no** — un reparto fijo son diez líneas |
| **B.3 router** | **depende de lo que llegue** | **sí, y es la primera vez** |

> ⭐ **El modelo se paga por decidir. En B.1 y B.2 no había nada que decidir — y por eso
> ninguna de las dos necesitaba un agente dirigiendo.** B.3 es la primera topología donde
> el camino no se puede escribir por adelantado, y por tanto la primera que **compra algo
> con el dinero que gasta arriba.**

📌 Esa frase salió de B.1 y B.2 **midiendo**, no del temario. Es la que hay que poner a
prueba en B.3: si un router también resultara ser un `if`, el bloque B tendría que decirlo.

---

##### 🎲 LA APUESTA — ✅ SELLADA el 2026-08-20 (sesión 94), antes de la primera línea de código

Las tres se contestaron **al empezar la sesión de B.3**, por escrito y antes de teclear.
Estaban en blanco a propósito: una predicción escrita después de ver el resultado no es una
predicción.

⚠️ **Nadie edita este bloque cuando lleguen los resultados.** Lo que salga se escribe
**debajo**, en su propio apartado, y se compara. Una apuesta que se retoca deja de ser una
apuesta.

1. **¿Un router necesita un modelo, o le basta un `if` sobre el texto de entrada?**
   Y si le basta un `if` en el caso fácil, **¿dónde está la frontera** en la que deja de
   bastar?
2. **¿Cuánto cuesta la decisión de enrutar?** El orquestador de A.2 gastó ~$0,0047 en dos
   llamadas solo para repartir y juntar. Un router hace *menos* trabajo que eso.
   **¿Sale a cuenta pagar por elegir, comparado con llamar a todos y descartar?**
3. **¿Qué pasa cuando el router se equivoca?** Un worker que se equivoca trae un número
   malo y una rúbrica lo caza. **Un router que se equivoca manda el trabajo entero al
   especialista equivocado, que lo hace impecablemente.** ¿Se detecta? ¿Con qué?

---

###### 🅰️ APUESTA 1 — ¿modelo o `if`?

| quién | apuesta |
|---|---|
| **estudiante** | **le basta un `if`** |
| **esta terminal** | **lo mismo, en esta tarea** — y la mitad que importa es *dónde deja de bastar* |

> 🔑 **LA FRONTERA APOSTADA: un `if` basta mientras la clave de enrutado se pueda EXTRAER
> del texto. Deja de bastar cuando hay que INFERIRLA.**

| lo que llega | ¿gana el `if`? | por qué |
|---|---|---|
| *"convierte 100 dólares"* | ✅ sí | la palabra está ahí, literal |
| *"convierte 100 USD"* | ✅ sí | sinónimo → **la lista se alarga, la idea no cambia** |
| *"cuánto es la factura de Alemania"* | ✅ sí, con trabajo | tabla país→moneda: sigue siendo enumerar |
| *"pásalo a la moneda del cliente"* | ❌ **no** | **no hay nada que extraer** |

📌 **La frontera no es cuántos destinos hay.** Se puede enrutar a cincuenta especialistas
con un `dict` y una palabra clave. La cruza que la respuesta deje de estar *escrita* en la
entrada.

⚠️ **Y el veneno, apostado el mismo día:** un `if` **no falla a gritos**. Cuando nada
coincide cae al `else`, y el especialista equivocado hace el trabajo **impecablemente**.
🔑 **Las preguntas 1 y 3 son la misma vista desde dos lados:** elegir el `if` no es elegir
"más simple", es elegir **un modo de fallo silencioso** en vez de uno caro (`LM.15`).

---

###### 🅱️ APUESTA 2 — ¿sale a cuenta pagar por elegir?

**Primero el dato, MEDIDO del registro de B.2** — corrida paralela de las `19:21`, aislada
de las otras tres corridas del mismo archivo:

```
ARRIBA (repartir + juntar)   2 llamadas   $0,005233
ABAJO  (3 workers × 3)       9 llamadas   $0,021751
                                          ─────────
                                          $0,026984   ← cuadra con la cifra de B.2 ✓
```

**Un worker completo cuesta $0,00724.** (usd $0,007315 · cad $0,007236 · eur $0,007200 —
casi idénticos, que es lo que debía pasar.)

```
enrutar          =  R + 1 worker  =  R + $0,00724
llamar a los 3   =  3 workers     =      $0,02175

sale a cuenta si   R < 2 × $0,00724  =  $0,0145
```

> 🔑 **EL UMBRAL SON DOS WORKERS.** La decisión puede costar hasta el doble de un
> especialista y aún así ganar.

| quién | apuesta |
|---|---|
| **estudiante** | **"hace más"** — el router no hace menos trabajo que repartir |
| **esta terminal** | **R ≈ $0,00043**, unas 34× por debajo del umbral: en dinero, enrutar gana holgado |

Razonamiento de la cifra: la llamada de enrutado **no lleva herramientas** y escribe **una
palabra** (`"eur"`), no 217 tokens. La 1.ª llamada del orquestador fue 1003 entrada → 217
salida = $0,002088; un router sería ~400 → ~5.

📌 **Las dos apuestas pueden ganar a la vez y no es empate:** "la decisión cuesta poco" y
"el router **como sistema** hace más que repartir, porque además carga el fallback" son
compatibles. Lo que hay que mirar al medir es **cuál de las dos lecturas era**.

🚨 **Y la cuenta destapó algo que la pista de aterrizaje NO tenía:** *"Tengo 1.000 dólares,
1.000 euros y 1.000 canadienses"* necesita **los tres** workers, legítimamente. **Ahí no
hay nada que enrutar.** Enrutar solo ahorra cuando la tarea necesita **uno de N**.
→ **B.3 arranca escribiendo una tarea nueva.** No es un extra: sin eso el bloque no puede
demostrar su propia tesis.

---

###### 🅲 APUESTA 3 — ¿quién caza al router equivocado?

| quién | apuesta |
|---|---|
| **estudiante** | **"no sé"** — y se sella tal cual, porque es honesto |
| **esta terminal** | **no lo caza nadie** |

Razonamiento: **todo lo que hay vigilando mira la SALIDA** — la rúbrica, el verificador, el
juez. Y la salida del especialista equivocado es impecable: bien escrita, con fuente y
fecha, **correcta en su tema**. El error solo existe en la **relación entre la entrada y la
decisión**, y ahí no hay nadie mirando.

📌 **"No sé" es la apuesta más valiosa de las tres**, porque es la única que nadie ha
medido: es la que paga el bloque.

⚠️ Y el callejón al que lleva: para cazarlo hace falta un **segundo juicio sobre la
decisión**, que es otro modelo. **¿Y quién vigila a ese?** B.3 tiene que contestarlo con
**un artefacto que exista**, no con una nota.

---

##### 📊 LOS RESULTADOS — medidos el 2026-08-20, DESPUÉS de sellar

⚠️ **Este apartado se escribió después de correr.** La apuesta de arriba no se tocó ni una
coma: se compara contra ella, que es lo único que hace que apostar sirva de algo.

**La corrida:** `python router.py --ambos`. Ocho entradas, dos routers, el mismo juez.
**Coste total del día: $0,001688.** El router de `if`, $0,00 exactos.

---

###### 📋 La tabla, por nivel — que es donde vive la frontera

| nivel | qué pide | `if` | modelo |
|---|---|---|---|
| **1** literal (×2) | *"250 dólares"*, *"300 euros"* | ✅ ✅ | ✅ ✅ |
| **2** sinónimo (×2) | *"250 USD"*, *"el billete verde"* | ✅ ✅ | ✅ ✅ |
| **3** inferir (×2) | *"una factura de Alemania"*, *"un taller de Toronto"* | ⚪ ⚪ | ✅ ✅ |
| **4** nada que extraer | *"la moneda del cliente"* | ✅ | ✅ |
| **5** ambigua 🤔 | *"un dólar canadiense en dólares americanos"* | 🔥 `cad` | 🔥 `cad` |

```
                     if      modelo
aciertos              5           7    de 7 puntuables
hacen daño            0           0
abstenciones          2           0
gasto         $0.000000   $0.001688
tiempo             0,00 s      6,02 s
```

---

###### 🅰️ APUESTA 1 — la frontera cayó AL MILÍMETRO, y el marcador engaña

✅ **La predicción de DÓNDE se rompe el `if` acertó exactamente.** Los cuatro casos de
nivel 1 y 2 (la clave está escrita), verdes. **Los dos casos de nivel 3** —los únicos que
piden inferir Alemania→euro y Toronto→dólar canadiense— **son exactamente los dos que se
cayeron.** Ni uno de más ni uno de menos.

> 🔑 **La frontera apostada era «extraer vs inferir» y resultó ser un corte limpio, no una
> pendiente.** El `if` no se degrada poco a poco: funciona perfecto hasta el borde y se
> apaga entero al cruzarlo.

⚠️ **PERO `5/7` contra `7/7` NO ES LA COMPARACIÓN QUE IMPORTA, y esto es el hallazgo.**
Mira la fila de abajo: **hacen daño, 0 y 0.** Los dos fallos del `if` fueron
**abstenciones** — dijo *"no sé"*, que es lo seguro. **Ni una sola vez mandó el trabajo al
especialista equivocado.**

> ⭐ **La pregunta no es «¿cuál acierta más?», es «¿cuál se equivoca PEOR?» — y en ese eje
> empataron a cero.** Un router que abstiene 2 de 7 te deja con dos casos sin resolver y
> te avisa. Uno que se equivoca 2 de 7 te deja con dos respuestas impecables y falsas.

📌 **Y ese eje solo existe porque `juzgar()` tiene cuatro veredictos.** Con un booleano, el
`if` habría salido *"5 aciertos, 2 fallos"* y el modelo *"7 aciertos"* — y la conclusión
habría sido *"el modelo es mejor"*, borrando lo único que separa un fallo seguro de uno
peligroso. **El instrumento que se declaró sospechoso al escribirlo es el que salvó la
lectura.**

**Veredicto de la apuesta:** las dos partes ganaron algo. *«Le basta un `if`»* es **cierto
dentro de la frontera y falso fuera**, y la frontera está donde se apostó. Lo que ninguno
de los dos dijo es que **el `if` falla del lado seguro**, y eso cambia cuándo elegirlo.

---

###### 🅱️ APUESTA 2 — dirección acertada, número fallado por 2×

| | apostado | medido |
|---|---|---|
| coste por decisión | **$0,000430** | **$0,000211** |
| tokens de salida | ~5 | **5** ✅ exacto |
| tokens de entrada | ~400 | **186** ❌ el doble de lo real |

**La conclusión no se movió, y con margen absurdo:**

```
enrutar          =  $0,000211 + $0,00724  =  $0,007451
llamar a los 3   =  3 × $0,00724          =  $0,021720
umbral (2 workers)                        =  $0,014480
→ SÍ sale a cuenta, con 69× de margen
```

📌 **Se anota el fallo aunque no cambie nada:** predije 400 tokens de entrada y son 186.
Inflé el tamaño del system prompt del router al doble. **Es el mismo error de la sesión 80
en pequeño — estimar por sensación un número que la pieza escribe sola.** El de salida sí
lo clavé, y no por mérito: la salida es una palabra, y eso no había que estimarlo.

🆕 **Y LA APUESTA 2 SE DEJÓ UN EJE FUERA, que la medición destapó: EL RELOJ.**
El router del modelo tardó **6,02 s en 8 decisiones = 0,75 s por decisión**. El `if`:
**0,00 s.**

> 🔑 **Enrutar con un modelo es barato en dinero y caro en tiempo.** La pregunta estaba
> escrita como *"¿cuánto CUESTA?"* y el dinero se comió la palabra. Es la lección de B.2 al
> revés: allí el paralelismo compró 51 % de reloj sin tocar la factura; aquí el router
> compra precisión pagando reloj.

📌 **Y ese 0,75 s no se paga igual en todas partes:** una vez por tarea es invisible;
dentro de un bucle que enruta en cada vuelta, se multiplica. Cuándo duele es una pregunta
de **topología**, no de router.

---

###### 🅲 APUESTA 3 — SIGUE SIN RESPUESTA, y decirlo es el resultado

❌ **No se contestó, y una corrida verde no la contesta.** Ninguno de los dos routers se
equivocó en nada puntuable, así que **no hubo ningún error que cazar**. Un cazador que
nunca vio pasar a su presa no está probado: está sin estrenar (`LM.13`).

🚨 **Y hay algo peor, que solo se ve mirando el juez que acabo de construir:**

> **`juzgar()` solo funciona porque yo escribí las respuestas correctas ANTES.**
> En producción no hay etiquetas de oro. Nadie sabe a qué especialista había que mandar
> el mensaje — **esa es la razón entera por la que existe el router.**

🔑 **Lo que se construyó hoy es un instrumento de laboratorio, no un cazador.** Sirve para
comparar dos routers sobre casos conocidos, y no sirve **en absoluto** para detectar un
error de enrutado en vivo. La apuesta de esta terminal (*"no lo caza nadie"*) sigue en pie
y **ahora con una razón mecánica en vez de una intuición**: el error de un router solo se
define contra una respuesta correcta, y en vivo no la hay.

📌 **Eso deja la pregunta apuntando a un sitio concreto:** si no hay etiqueta de oro, el
único testigo posible es **el propio especialista diciendo «esto no es lo mío»**. Y eso ya
no es un router: es **el destinatario devolviendo el trabajo.** B.4 en adelante.

---

###### 🚨 EL HALLAZGO DEL DÍA — el sospechoso marcado DISPARÓ

El archivo `router.py` declara en su cabecera, antes de una línea de código, que el segundo
candidato a estar ciego son **las etiquetas de oro escritas a mano**. Ocurrió.

**`n5-a`** (*"¿Cuánto es un dólar canadiense en dólares americanos?"*) fue **el único rojo
de toda la corrida** — y salió rojo **en los dos routers, con la misma respuesta: `cad`.**

> ⭐ **Dos decisores independientes, uno de ellos sin nada de inteligencia, coincidiendo
> contra mi etiqueta. Eso no es evidencia de que fallaran: es evidencia de que la etiqueta
> estaba mal.**

⚠️ **Y mira lo que se evitó.** Si `n5-a` no llevara la marca `discutible`, el informe
diría: *«los dos routers cometen 1 invención (🔥)»* — el veredicto más grave de los cuatro,
**en los dos a la vez**, y el titular del día habría sido un peligro inventado por mí.

🔑 **Es `LM.15` con el instrumento ciego siendo la RESPUESTA CORRECTA, no el medidor.**
Tercera sesión seguida en que lo escrito ese mismo día es lo que estaba ciego (B.1 el
verificador, B.2 la línea de tiempo, B.3 la etiqueta de oro) — pero **la primera en que se
marcó ANTES y por eso no hizo daño.**

📌 La regla que se lleva: **un caso cuya respuesta correcta el autor no tiene clara no se
resuelve poniendo la que le parece mejor. Se marca y se saca del marcador.** La duda es un
dato; convertirla en etiqueta la borra.

---

###### ✅ Lo que B.3 deja construido

| pieza | qué es | coste |
|---|---|---|
| `router.py` | los dos routers, el banco de 8, el juez de 4 veredictos | — |
| **13 pruebas** | pasan sin tocar la red | **$0,00** |
| `registro_router_*.jsonl` | 30 líneas: cada decisión con su crudo, tokens y `stop_reason` | — |

⭐ **La prueba nº 4 es la rara y conviene mirarla:** afirma un **LÍMITE**, no una capacidad
—*«el `if` NO infiere Alemania → eur»*—. Si algún día se pone verde sola, es que alguien
amplió el router y **hay que volver a apostar**. Un test que vigila una frontera envejece
al revés que los demás.

📌 **Los 8 `stop_reason` salieron `end_turn` y los 8 crudos fueron la palabra limpia.** El
formato se respetó 8 de 8, así que la normalización de la salida del modelo **no se vio
morder** — está, y sigue siendo una nota (`LM.13`).

---

##### 🧾 Lo que B.3 hereda, y su estado real

**Deudas abiertas, anotadas y NO pagadas a sabiendas:**

| # | Qué es | Estado |
|---|---|---|
| `D-B1.1` | el freno del verificador no caza una paráfrasis (`Fecha del informe:`) | **abierta** |
| `D-B1.2` | el defecto de la frontera es **intermitente: 1 de 2 corridas** | **abierta** |
| `D-B1.3` | el archivista **reteclea** el borrador en vez de guardarlo (345 tokens) | **abierta** |
| `D-B2.1` | la línea de tiempo se pisaba entre vueltas | ✅ arreglada + prueba nº 8, ⚠️ **no vista morder en vivo** (`LM.13`) |

**Preguntas abiertas que el bloque B debe contestar antes de cerrar:**

- ⚠️ **¿Un pipeline de 3 agentes que en realidad necesita 2 sigue siendo un pipeline de
  3?** (viene de `D-B1.3`: quitada la verificación, al archivista no le queda nada que
  decidir).
- 🆕 **¿Un router que resulta ser un `if` sigue siendo una topología?** Es la misma
  pregunta con otro traje, y B.3 la hereda porque B.1 y B.2 la ganaron las dos veces.

**Lo que B.3 ya se encuentra hecho y no tiene que construir:**

- ✅ `reparto` es **un parámetro** del bucle del orquestador. Una topología nueva **no
  toca `orquestador.py`**: se escribe aparte y se pasa por la puerta.
- ✅ Los tres candados de lo compartido (registro, contabilidad, pantalla) ya están, y
  **en serie no cuestan nada**.
- ✅ El patrón de las pruebas gratis: workers falsos que duermen, registro desviado a un
  temporal, y `--test` como comportamiento por defecto del archivo.

---

##### 📌 La regla que se repitió dos sesiones seguidas, y conviene tenerla delante

En B.1 y en B.2, **el instrumento de medida escrito ese mismo día resultó ser el ciego**:
el verificador que no vio la paráfrasis (`D-B1.1`) y la línea de tiempo que se pisaba
(`D-B2.1`). Las dos veces el defecto **no dio un dato falso: dio silencio**, y el silencio
se lee como confirmación.

🔑 **En B.3, el primer sospechoso de estar ciego es lo que se escriba para vigilar al
router.**

---

---

#### 🎲 B.4 — EL SUPERVISOR: la apuesta, sellada el 2026-08-20 (sesión 94) antes de teclear

⚠️ **Nadie edita este bloque cuando lleguen los números.** Lo que salga se escribe debajo.

**El estudiante apostó *«no tengo una respuesta clara»*, y se sella tal cual.** Ayer quedó
dicho por qué eso vale: es la única forma de apuesta que **no puede contaminar la lectura**,
y B.3 demostró que un *«no sé»* honesto apunta mejor que una intuición adornada.

---

##### 🔑 Lo que B.3 le cambió a B.4 ANTES de empezar

El plan del bloque B, escrito hace sesiones, dice: *«B.4 Supervisor: el orquestador juzga y
reenvía»*. Pero B.3 midió que **un juez solo funciona con la respuesta correcta escrita de
antemano**, y en vivo no la hay.

> ⭐ **Así que B.4 no arranca preguntando cómo se construye un supervisor. Arranca
> preguntando si un supervisor puede saber algo que el juez de B.3 no podía.**

---

##### 🅰️ APUESTA 1 — ¿qué puede juzgar de verdad un supervisor sin herramientas?

El orquestador **no lleva herramientas reales** (decisión de A.2, no descuido). No puede
consultar una tasa. Entonces no puede comprobar si el número es **cierto**.

> 🔑 **APUESTA: un supervisor sin herramientas no puede verificar la VERDAD, pero sí la
> COHERENCIA — y coherencia es más de lo que suena.**

Lo que apuesto que SÍ puede cazar, sin tocar la red:

| | qué comprueba | con qué |
|---|---|---|
| **campos** | ¿trae monto, fuente y fecha? | el contrato de A.3 |
| **encaje** | ¿contesta lo que se preguntó? | comparar pregunta y respuesta |
| **aritmética** | ¿`monto × tasa` da el resultado que dice? | multiplicar |

⭐ **La tercera es la que no esperaba y es la buena:** la coherencia aritmética **se
comprueba sin ninguna herramienta**. Si el worker dice *«1.000 USD son 4.200.000 COP a una
tasa de 4.200»*, el supervisor puede multiplicar. No sabe si 4.200 es la tasa real — **pero
sabe si la cuenta cierra**.

⚠️ **Y lo que apuesto que NO caza, que es lo importante: un número inventado pero coherente
consigo mismo.** Un modelo que se saca una tasa de la manga hace bien la multiplicación con
su tasa inventada. La aritmética caza errores de aritmética, **no fabricación**.

🔑 **Y eso encaja exactamente con B.3: lo que se escapa es lo impecable.**

---

##### 🅱️ APUESTA 2 — ¿cuántas vueltas, y de dónde sale ese número?

Un worker cuesta **$0,00724** (medido en B.2). Un reenvío **duplica la capa de abajo**.

> 🔑 **APUESTA A: la regla de parada honesta no es un número de vueltas, es un
> PRESUPUESTO.** *«Reintenta 2 veces»* es un número que alguien puso a ojo. *«Reintenta
> mientras quede presupuesto de la capa de abajo»* sale de una cantidad real. El primero
> hay que defenderlo; el segundo se defiende solo.

> 🚨 **APUESTA B, y es la que quiero medir: un reintento CIEGO casi no vale nada.**
> Reenviar el mismo prompt al mismo modelo es pagar dos veces por el mismo billete de
> lotería. **Si el segundo intento no lleva escrito QUÉ estuvo mal, la única fuente de
> mejora es el azar.**

📌 Eso da el experimento entero de B.4: **reintento ciego** (mismo encargo) contra
**reintento informado** (encargo + motivo del rechazo). Una sola variable.

---

##### 🅲 APUESTA 3 — ¿caza el supervisor el error de enrutado de B.3?

Llega un trabajo **impecable del especialista equivocado**. El supervisor lo mira.

> 🔑 **APUESTA: NO lo caza — y por una razón mecánica de una sola línea.** El supervisor
> juzga *«¿esta respuesta sirve?»* contra **el encargo que se le dio al worker**, no contra
> **el mensaje original del usuario**. Si el router mandó *«una factura de Alemania»* al
> worker del dólar, el encargo decía «dólares», la respuesta habla de dólares, y **encaja
> perfectamente con su encargo**.

> ⭐ **Y la condición que lo cambia todo, que es una decisión de diseño de una línea:
> el supervisor lo caza SOLO SI VE EL MENSAJE ORIGINAL.** No el encargo. El original.

📌 Segundo experimento, también de una variable: **supervisor ciego** (ve encargo +
respuesta) contra **supervisor con el original** (ve además lo que el usuario escribió), con
un enrutado equivocado **metido a propósito** para que haya presa que cazar — que es
exactamente lo que le faltó a B.3.

---

##### ⚠️ El sospechoso de estar ciego, nombrado antes de escribirlo

Cuatro sesiones seguidas lo ciego ha sido **lo escrito ese mismo día**: el verificador
(B.1), la línea de tiempo (B.2), la etiqueta de oro (B.3).

🚨 **En B.4 el primer sospechoso es el ERROR INYECTADO.** Si el enrutado equivocado que meto
a mano es más burdo que uno real, el supervisor lo cazará por lo obvio y el resultado no
dirá nada del caso que importa. **Un cebo demasiado fácil mide al cebo, no al cazador.**


---

##### 📊 B.4 — LOS RESULTADOS, medidos el 2026-08-20 DESPUÉS de sellar

⚠️ **La apuesta de arriba no se tocó.** Todo lo de aquí abajo se escribió después de correr.

**Gasto de B.4: $0,025565.** Reparto: cebo `$0,007285` · exp1 `$0,000990` ·
exp2 `$0,014969` · exp3 `$0,002321`. **13 pruebas que cuestan $0,00.**

---

###### 🅰️ APUESTA 1 — se rompió sola ANTES de correr, y para mejor

La apuesta decía: *«un supervisor sin herramientas no puede verificar la verdad, pero sí la
coherencia — y la aritmética se comprueba multiplicando»*. Al abrir `worker.py` para
escribir el revisor apareció que **el contrato de A.3 ya trae `monto`, `tasa` y `pesos` en
campos separados.**

> ⭐ **Entonces la comprobación aritmética no necesita un modelo: son tres líneas de Python
> y cuesta $0,00.**

> 🔑 **Y eso reordena la pregunta del bloque: la parte del juicio que se puede VERIFICAR es
> exactamente la parte que NO necesita un modelo. La parte que necesita un modelo es
> exactamente la que no se puede verificar.**

📌 Misma forma que B.1 (*«el pipeline eran tres líneas»*), B.2 (*«el reparto eran diez»*) y
B.3 (*«el router era un `if`»*), una capa más arriba. **Cuarta vez seguida en el bloque B.**

🚨 **Y la parte del juicio que sí usa modelo se midió, con un resultado feo.** Sobre el
mismo cebo:

| quién | veredicto | por qué |
|---|---|---|
| **revisor determinista** ($0,00) | ✅ sin objeciones | correcto: campos completos, la cuenta cierra |
| **supervisor ciego** ($0,000456) | ❌ no sirve | *«la fecha (20 de agosto de 2026) es futura y no puede ser real»* |

⚠️ **La fecha era la de hoy.** El supervisor sin herramientas **no puede comprobar la
verdad, intentó hacerlo igual, y fabricó una objeción.** La apuesta decía que no podría
verificar; midió algo peor: **que lo intenta y se inventa el resultado.**

---

###### 🅲 APUESTA 3 — CONFIRMADA, y solo se ve leyendo los motivos

**Los dos supervisores rechazaron.** Y ahí casi se pierde todo:

| supervisor | veredicto | motivo |
|---|---|---|
| **ciego** | no sirve | *«la fecha es futura»* ← **nada que ver con el enrutado** |
| **con el original** | no sirve | *«el usuario preguntó por una factura en euros (Alemania), pero convirtió dólares»* ← **exacto** |

> ⭐ **El ciego no cazó nada: acertó la casilla por el motivo equivocado.** Solo el que ve
> el mensaje original nombra el error de enrutado — y la diferencia entre los dos es **una
> sección de texto en el sobre.**

🚨 **Y AQUÍ ESTÁ EL FALLO DEL DÍA, QUE ES MÍO.** La función que evalúa el experimento
comparaba `sirve_ciego` y `sirve_original`: **dos booleanos.** Vio *«los dos rechazan»* e
imprimió **«la apuesta falla»**. Era falso.

> 🔑 **Un rechazo no es un dato; el dato es POR QUÉ.** Dos rechazos por motivos opuestos
> caen en la misma casilla booleana.

📌 **Y el agravante:** es el mismo defecto que `router.py` evitó **ayer, a propósito**,
construyendo un juez de cuatro veredictos y escribiendo en su docstring por qué un booleano
miente. Veinticuatro horas después se coló **en la función que juzga mi propia apuesta**.
**Quinta sesión seguida en que lo ciego es lo escrito ese mismo día.**

✅ **Arreglado con `habla_del_enrutado()` + pruebas 11-13, que usan los motivos REALES
copiados del registro.** Y el arreglo se comprobó con `--releer`: **$0,00**, porque
*arreglar el código es gratis; volver a correr es lo que cuesta* — y además una corrida
nueva habría dado motivos distintos y no se sabría si cambió la conclusión por el arreglo o
por el modelo. **Releer mantiene la variable quieta.**

---

###### 🅱️ APUESTA 2 — confirmada, y peor de lo apostado

Aposté que **un reintento ciego casi no vale nada**. Medido:

| brazo | qué se le dio | resultado | coste |
|---|---|---|---|
| **A ciego** | el mismo encargo | la misma respuesta, en dólares | $0,007259 |
| **B informado** | encargo + el mensaje original + *«si no corresponde, dilo en vez de responderlo»* | **la misma respuesta, en dólares** | **$0,007710** |

🚨 **El reintento informado tampoco valió nada — y costó 6 % MÁS.** Se le dio el contexto
entero y una instrucción explícita para negarse, y **respondió igual.**

⚠️ **La explicación cómoda sería *«le faltaba contexto»*, y es FALSA:** el contexto se lo
dimos completo. Escribirlo así habría sido la sesión 80 otra vez — nombrar un mecanismo en
vez de medirlo.

🔑 **La causa real: el system prompt del worker le manda responder siempre** (*«no hagas
preguntas: nadie te va a contestar. Responde en UNA sola frase con el monto en pesos»*).
**Una instrucción metida en el encargo compite con el system prompt y pierde.**

---

###### ⭐ EL HALLAZGO DE B.4 — el permiso de negarse se CONSTRUYE, no se pide

Experimento 3, **no planeado**: lo pidió el resultado del 2. Mismo encargo, mismo worker,
**una sola variable — una frase añadida al system prompt.**

```
exp2 informado  (system prompt normal)      → convirtió dólares    3 vueltas  $0,007710
exp3 con derecho(system prompt + 1 frase)   → DEVOLVIÓ EL TRABAJO  1 vuelta   $0,002321
```

> *«Este encargo no es para mí: el usuario pidió convertir 400 euros (de Alemania), no 400
> dólares estadounidenses…»*

**Nombró el error exacto. Usó CERO herramientas. Una vuelta en vez de tres. Un 70 % más
barato.**

> 🔑 **B.3 cerró diciendo que el único testigo posible era el especialista devolviendo el
> trabajo. B.4 lo midió: ese testigo EXISTE — pero no se le pide, se le construye.**

⭐ **Y negarse no es solo correcto: es más barato.** El worker se negó **antes** de llamar a
ninguna herramienta, así que el rechazo cuesta menos que el trabajo equivocado. **Es el
único freno del curso que ahorra dinero en vez de gastarlo.**

📌 Esto toca el sobre sellado de A.1, y con una corrección importante. El sobre dice: *«el
aislamiento que lo hace bueno es el mismo que le quita el contexto para avisar»*. **No era
el contexto.** El contexto se lo dimos y no sirvió de nada. **Era el permiso.** La frase del
sobre se cumple en el resultado y falla en el mecanismo, y eso se anota tal cual.

---

###### 🎯 Y el sospechoso nombrado antes de escribirlo: el cebo NO era demasiado fácil

Se avisó que *«un cebo más burdo que un fallo real mide al cebo, no al cazador»*. **No pasó,
y hay prueba:** el supervisor ciego **no lo cazó**. Si el cebo hubiera sido obvio, los dos lo
habrían nombrado y el experimento no habría distinguido nada.

📌 Lo que lo salvó fue la decisión de **no escribir yo la respuesta**: la produjo un worker
de verdad, corriendo de verdad, y quedó grabada en `cebo_mal_enrutado_*.json` para que los
dos supervisores vieran **el mismo texto**.

---

###### 🧾 Lo que B.4 deja, y lo que queda abierto

| pieza | qué es | coste |
|---|---|---|
| `supervisor.py` | revisor determinista, dos supervisores, tres experimentos | — |
| **13 pruebas** | sin tocar la red | **$0,00** |
| `--releer` | recalcula la conclusión sobre el registro grabado | **$0,00** |
| `cebo_mal_enrutado_*.json` | la presa, producida por un worker real | $0,007285 |

**Abierto:** `D-B4.1` — el «derecho a negarse» se midió **una vez, en un caso**. No se sabe
si un worker con esa frase se vuelve **quisquilloso** y devuelve trabajo que sí era suyo.
**Un freno que solo se ha visto morder en el caso que lo justifica no está medido: está
estrenado** (`LM.13`).


---

###### 🎲 PAGANDO `D-B4.1` — ✅ APUESTA SELLADA el 2026-08-21 (sesión 95), antes de la primera línea de código

> 🔑 **La deuda en una frase:** el «derecho a negarse» se vio morder **en el único caso que
> lo justifica**. Un freno probado solo donde tenía razón no está medido: está **estrenado**.
> La pregunta que falta es la contraria — **¿devuelve también trabajo que SÍ era suyo?**

**El estudiante:** *«voy a la tuya»* — se sella la de esta terminal tal cual.

**DOS BRAZOS, no uno**, porque el encargo del experimento 3 traía dos cosas pegadas —el
encargo equivocado **y** un aviso de rechazo— y no se sabe cuál de las dos lo hizo negarse.

| | qué cambia | qué mide |
|---|---|---|
| **Brazo A** | el gemelo EXACTO del exp. 3, con el **mismo aviso literal**, pero el mensaje original ahora **sí es de dólares** (factura de EE. UU., no de Alemania) | ¿se niega por **verificar**, o por **sugestión**? |
| **Brazo B** | el encargo normal (`Convierte 1000 USD a pesos`), **sin aviso y sin mensaje original**. Solo el system prompt nuevo | ¿el freno **estorba en el tráfico normal**? Es lo que pide la deuda, y tiene línea base: la demo de A.1 |

**LA APUESTA, en tres números falsables:**

1. **El brazo B hace el trabajo.** Confianza **alta**: la frase añadida es *condicional*
   —*«si el encargo no corresponde…»*— y no hay nada en el encargo que la dispare.
2. **El brazo A también hace el trabajo**, y con **menos confianza**. B.4 midió que una
   instrucción del encargo **pierde** contra el system prompt; pero aquí los dos **no se
   contradicen**, dicen lo mismo. 🔑 **Lo que decide es si el modelo VERIFICA que el encargo
   corresponde, o si le basta el «te rechazaron» como prueba de que algo va mal.**
3. **El brazo A cuesta MÁS que el B**, porque el aviso son tokens extra y probablemente
   conteste mencionándolo. **Brazo B ≈ $0,0073 · brazo A ≈ $0,0078.**

**Y lo que la deuda cobra:** si los **dos** trabajan, el freno **discrimina** y el hallazgo
de la 94 se sostiene. Si **alguno** se niega, el freno es un **cascarrabias** y el hallazgo
se matiza.

**EL JUEZ — y no va a haber un booleano, que fue el fallo del día anterior.** El veredicto
sale **del harness, no de la prosa**: `herramientas` y `vueltas` (exactos, ya pasaron por
aquí) y `faltan` del contrato — quien trabajó llena los **6** campos; quien se negó, **cero**.
Tres casillas, no dos: `trabajo` · `negativa_gratis` · `mixto` (usó herramientas y el
contrato no cerró → **se mira a mano**).
📌 **Y el texto se imprime ENTERO para leerlo con los ojos.** Que una frase sea una negativa
no lo decide un `in`. Esa parte necesita ojos, y **se dice en voz alta en vez de disfrazarla
de medición** — es la lección de B.4: *la parte del juicio que se puede verificar es la que
no necesita un modelo*.

**⚠️ EL SOSPECHOSO DE ESTAR CIEGO, nombrado antes de escribirlo.** Cinco sesiones seguidas
lo ciego ha sido lo escrito ese mismo día. Hoy el candidato es **el `AVISO` del brazo A**:
si es más sugestivo de lo que un supervisor real escribiría, mide **mi redacción**, no el
freno — el mismo bicho del cebo. **Lo que lo salva a medias: el aviso NO se redacta de
nuevo, es copia literal del que ya usó el experimento 3.** Si el brazo A sale raro, se mira
aquí primero.


---

###### ✅ `D-B4.1` PAGADA — lo que salió, el 2026-08-21. **$0,015387**

**LOS DOS BRAZOS TRABAJARON.** `tasa, convertir` · 3 vueltas · contrato completo, los dos.

| brazo | veredicto | herramientas | apostado | medido | desvío |
|---|---|---|---|---|---|
| **A** — con el aviso mentiroso | 🔨 `trabajo` | `tasa, convertir` | $0,0078 | **$0,007960** | **+2 %** |
| **B** — tráfico normal | 🔨 `trabajo` | `tasa, convertir` | $0,0073 | **$0,007427** | **+2 %** |

⭐ **LA DEUDA QUEDA SALDADA: el freno DISCRIMINA.** El worker con derecho a negarse se
niega cuando el encargo no le corresponde y **trabaja cuando sí** — incluso cuando se le
dice que un supervisor acaba de rechazarlo. **No es un cascarrabias, y el hallazgo de la
sesión 94 se sostiene.** El brazo A además mata el confundido: no se negó por sugestión,
porque con el mismo aviso y el encargo correcto **no se negó**.

📌 **Y la apuesta acertó los tres puntos, pero el 3 por la razón EQUIVOCADA.** Predije que
A costaría más *«porque probablemente conteste mencionando el aviso»*. **No lo mencionó ni
una vez.** El sobrecosto vino entero de los tokens de **entrada** (6520 contra 6167), no de
la respuesta. 🔑 Es la sesión 84 otra vez: **acertar la casilla no es haber acertado el
mecanismo**, y un número que sale bien tapa un porqué que salió mal.

---

###### 🚨 LO QUE NADIE FUE A BUSCAR — y es el hallazgo del día

> **Importancia: alta · Urgencia: no bloqueante.** No rompe nada hoy **porque el contrato de
> A.3 lo está tapando** — y ese es justamente el punto.

**La frase del derecho a negarse le hizo PERDER LA FUENTE a la prosa.** Los dos textos de
hoy dicen *«según la tasa de mercado de 20 de agosto de 2026»*, **sin `open.er-api.com`**.
El registro entero, leído después:

| system prompt | corridas | ¿la prosa conserva la fuente? |
|---|---|---|
| `SISTEMA_DIVISA` (el de siempre) | 5 | **5 de 5 sí** |
| `SISTEMA_DIVISA_CON_DERECHO_A_NEGARSE` | 2 | **0 de 2** |

🔑 **El mecanismo es el de B.4 al revés.** El system prompt viejo dice *«Di siempre de dónde
salió la cifra»*; la frase nueva **compite con esa y le gana**. En B.4 se midió que una
instrucción del ENCARGO pierde contra el system prompt. Aquí se ve la otra mitad: **una
frase añadida al system prompt desplaza a la que ya estaba dentro.** Un freno no se suma
gratis — **empuja**. Y nadie lo pidió, y nadie lo habría notado.

⭐ **PERO LO QUE DE VERDAD PASÓ HOY ES ESTO: EL CONTRATO DE A.3 SE VIO MORDER.** `fuente`
llegó completa en las **2 de 2**, porque no sale de lo que el modelo redacta — sale de lo
que la herramienta devolvió y **el harness guardó**. Es el defecto de A.2 reapareciendo
**solo, sin que nadie lo provocara**, y el arreglo aguantándolo.
🔑 Por `LM.13`, un freno que no has visto morder es una nota. **Este dejó de ser una nota
hoy, y de rebote: lo destapó un experimento que iba a otra cosa.**

⚠️ **NO ESTÁ MEDIDO, y se dice antes de que suene a dato:** son **2 corridas contra 5**, y
las 2 llevan el system prompt nuevo. El reparto es limpio pero pequeño.

**`D-B4.2` ABIERTA (~$0,007):** una corrida con el system prompt nuevo **añadiéndole** el
énfasis de la fuente. Si la recupera, la causa era **el desplazamiento**; si no, es otra
cosa. Se deja abierta a sabiendas: la deuda del día ya está pagada, el contrato tapa el
agujero, y **el registro queda escrito, así que el rastro no se enfría.**

---

###### 🧾 Lo que costó, y lo que quedó vigilando

| pieza | coste |
|---|---|
| `experimento_4()` — dos brazos | **$0,015387** |
| `veredicto_negativa()` — 3 casillas, del harness | — |
| **5 pruebas nuevas** (14-18), suite de 13 → **18** | **$0,00** |
| `con_aviso()` — el aviso, que estaba **COPIADO** en el exp. 2 y el 3 | **$0,00** |

📌 **`con_aviso` no es limpieza cosmética.** El aviso estaba escrito **dos veces, palabra por
palabra**. El brazo A necesita EXACTAMENTE ese texto: si lo hubiera reescrito «parecido»,
habría comparado **dos redacciones mías** y lo habría llamado medición — el bicho del cebo.
Con una función, que sea el mismo texto **deja de ser una promesa de la documentación y pasa
a ser una propiedad del programa**, y la prueba 14 la vigila.

📌 **La prueba 18 afirma un LÍMITE**, como la 5: un caso a medias —llamó a `tasa` y luego se
negó— **cae en `mixto` y no se fuerza** a ninguna casilla limpia. Si un día se pone roja
sola, alguien colapsó el juez a un booleano otra vez.


---

#### ⏭️ EL ARRANQUE DE B.5 — escrito al cerrar la 94, **sin una línea de código**

⚠️ **Aquí no hay lección de B.5, y es deliberado.** Esto es la pista de aterrizaje: qué
pregunta abre, qué hereda y qué hay que sellar **antes** de construir.

---

##### 🔑 Por qué B.5 llega con la pregunta ya cargada

El plan la define como *«profundidad > 2: un worker que a su vez orquesta — **casi nunca**,
y hay que saber por qué»*. **Es la única fila del bloque B que viene con la respuesta
insinuada en el propio plan**, y eso es una trampa: invita a construirla para confirmar.

Y B.4 le dejó una pregunta concreta encima:

> ⭐ **Si el único testigo fiable de un error es un worker CONSTRUIDO para negarse
> (medido en B.4), ¿qué le pasa a esa queja cuando el que se niega está DOS capas abajo y
> tiene que subir por un intermediario que fue construido para RESPONDER?**

📌 No es retórica: en B.4 se midió que **una instrucción metida en el encargo pierde contra
el system prompt**. Un intermediario cuyo system prompt dice *«junta lo que te den y
responde»* es exactamente el que puede tragarse un *«esto no es lo mío»* y devolver un
resumen educado hacia arriba.

---

##### 🎲 LA APUESTA — ✅ **SELLADA el 2026-08-21 (sesión 95)**, antes de la primera línea de código

> Las tres preguntas de abajo se escribieron al cerrar la 94 y quedaron **en blanco a
> propósito**. Se responden en el bloque que sigue, y **sin haber tecleado nada**.

Una predicción escrita después de ver el resultado no es una predicción. Es el orden que ya
funcionó en las sesiones 90, 93 y 94 — y en la 94 se aprendió además que **hay que
commitearla**: una apuesta en un archivo sin commitear se puede retocar sin dejar rastro.

1. **¿Es B.5 la primera topología del bloque que NO se colapsa?** B.1 resultó ser tres
   líneas, B.2 diez, B.3 un `if`, B.4 tres líneas de aritmética. **Cuatro de cuatro.**
   ¿Un worker que orquesta es una topología, o es un worker con más herramientas?
   Y la que de verdad importa: **¿cuál es la señal que distingue las dos?**
2. **¿Sobrevive una queja a dos capas?** Un worker de la capa 3 se niega. El de la capa 2
   fue construido para responder. **¿Llega el «esto no es lo mío» hasta arriba, llega
   deformado, o no llega?**
3. **¿Qué le hace la profundidad a la factura y al reloj?** B.2 midió que un fan-out paga
   **el máximo** de sus ramas, no la media. A tres capas, ¿se multiplica, se suma, o hay
   un número que todavía no hemos visto?

---

##### ✅ LO APOSTADO — sellado el 2026-08-21, sin una línea de código

**El estudiante:** *«voy a la tuya»* — se sella la de esta terminal tal cual.

**📌 Y lo primero, porque cambia por qué el orden del día fue el correcto:** pagar `D-B4.1`
antes no era prolijidad. **B.5 necesita provocar una queja REAL en la capa de abajo**, y el
único modo fiable de producirla es el worker con derecho a negarse. Si hubiera resultado un
cascarrabias, una queja llegando arriba **no querría decir nada** —¿se quejó porque el
encargo estaba mal, o porque se queja de todo?—. 🔑 **La deuda de ayer es el instrumento de
hoy.** Se saldó a las 9 de la mañana y a las 10 ya estaba midiendo.

**QUÉ SE MONTA — tres capas de verdad, ninguna decorativa:**

| capa | quién | qué es |
|---|---|---|
| 1 | el orquestador | *«Prepara el informe de estas facturas»* |
| 2 | **un worker que a su vez orquesta** | reparte cada factura a su especialista. **Worker para el de arriba, orquestador para los de abajo** |
| 3 | los workers de divisa (A.1) | con el **derecho a negarse** ya construido y ya medido |

**El experimento:** se enruta **mal** una factura en la capa 3. El de abajo se niega —eso ya
no es una suposición, se midió hoy—. **La pregunta es qué le llega al de arriba.**

---

**1️⃣ ¿ES B.5 LA PRIMERA TOPOLOGÍA QUE NO SE COLAPSA? → Sí se colapsa, y aun así SÍ es una
topología de verdad.** Las dos cosas, y no es una contradicción.

Las cuatro anteriores se colapsaron porque **el código resultó trivial** (tres líneas, diez,
un `if`, tres de aritmética). B.5 se colapsa **peor**: no necesita código nuevo **en
absoluto**. `correr_orquestador` llamando a algo que llama a `correr_worker` **ya está
escrito**.

🔑 **Y DE AHÍ SALE LA SEÑAL QUE EL SOBRE PEDÍA, que es lo que de verdad se apuesta:**
**una topología es real cuando aparece un MODO DE FALLO que antes no existía — no cuando el
código crece.** El router era un `if`, cero líneas interesantes, y aun así **inventó el error
de enrutado**, que no existía en B.1 ni en B.2. Por esa vara B.5 **sí** es una topología:
trae un fallo que ninguna de B.1–B.4 podía tener.
⭐ **Contar líneas era la vara equivocada todo el tiempo, y el bloque B entero lo estuvo
haciendo.**

**2️⃣ ¿SOBREVIVE UNA QUEJA A DOS CAPAS? → Llega DEFORMADA: sobrevive el «algo salió mal» y
muere el «qué».**

No es intuición, son **dos cosas ya medidas**: B.4 mostró que el system prompt del
intermediario **gana** a lo que venga dentro del encargo; y **hoy mismo** (`D-B4.2`) que una
frase añadida al system prompt **desplaza** a la que ya estaba dentro. Un intermediario cuyo
system prompt dice *«junta lo que te den y responde»* **va a resumir**.
📌 Es `open.er-api.com` desapareciendo de la prosa **otra vez, una capa más arriba**.
⭐ **Y se apuesta también el arreglo: no es un prompt mejor, es un CONTRATO** — lo mismo que
ya funcionó en A.3. Si el arreglo resulta ser «pedírselo mejor», la apuesta falla entera.

**3️⃣ ¿QUÉ LE HACE LA PROFUNDIDAD A LA FACTURA Y AL RELOJ? → La contabilidad de arriba va a
contar de MENOS, y sin dar un solo error.**

Es la más falsable de las tres, y es el sospechoso nº 1 nombrado abajo **disparando**:
`sumar_worker` suma el `coste_usd` del **hijo inmediato**; el gasto de la capa 3 vive en el
diccionario **del intermediario**, que es **otro** diccionario. **Nadie baja a buscarlo.**

Y el peaje del reloj y del bolsillo: **el intermediario cuesta más o menos lo que un worker
(~$0,007) sin producir NI UN DATO NUEVO** — solo re-dice lo que abajo ya dijo.
🔑 **Ese número es el «casi nunca» del plan MEDIDO en vez de supuesto**, que es exactamente
la diferencia entre ilustrar y medir.

💰 **Coste estimado de B.5: ~$0,05** (dos corridas de tres capas). **Es la pieza más cara del
bloque B**, y se dice antes de gastarla, no después.


---

##### 🧾 Lo que B.5 hereda, y su estado real

**Deudas abiertas, anotadas y NO pagadas a sabiendas:**

| # | Qué es | Estado |
|---|---|---|
| `D-B1.1` | el verificador no caza una paráfrasis (`Fecha del informe:`) | **abierta** |
| `D-B1.2` | el defecto de la frontera es **intermitente: 1 de 2 corridas** | **abierta** |
| `D-B1.3` | el archivista **reteclea** el borrador en vez de guardarlo | **abierta** |
| `D-B2.1` | la línea de tiempo se pisaba entre vueltas | ✅ arreglada + prueba, ⚠️ **no vista morder** |
| `D-B3.1` | la normalización de la salida del router | ⚠️ **no vista morder** (8 de 8 limpios) |
| `D-B3.2` | la etiqueta de oro de `n5-a`, marcada discutible | **sin resolver** (la corrida sugiere `cad`) |
| `D-B4.1` | el «derecho a negarse» **visto morder una sola vez** | ✅ **PAGADA** (sesión 95): el freno **discrimina** |
| `D-B4.2` | la frase del derecho a negarse **le quita la fuente a la prosa** (0 de 2 contra 5 de 5) | **abierta** — el contrato la tapa, ~$0,007 |

> ✅ **PAGADA en la sesión 95, y costó DOS corridas ($0,015387), no una.** El segundo brazo
> se añadió al ver que el encargo del experimento 3 traía dos cosas pegadas. Salió que el
> freno **discrimina**. 🔑 Y de rebote destapó `D-B4.2`. La pregunta original decía: La pregunta es si un worker con la frase del derecho a negarse se
> vuelve **quisquilloso** y devuelve trabajo que sí era suyo. Un freno visto morder solo en
> el caso que lo justifica no está medido: **está estrenado** (`LM.13`).
> → Se corre pasándole al worker `usd` un encargo **correcto** con el system prompt de
>   `SISTEMA_DIVISA_CON_DERECHO_A_NEGARSE`. Si lo responde, el freno discrimina.

**Preguntas abiertas que el bloque B debe contestar ANTES de cerrar:**

- ⚠️ **¿Un pipeline de 3 agentes que en realidad necesita 2 sigue siendo un pipeline de 3?**
  (de `D-B1.3`).
- ⚠️ **¿Un router que resulta ser un `if` sigue siendo una topología?** — B.3 la contestó a
  medias: el `if` gana **dentro de la frontera** y falla **del lado seguro**. Falta decidir
  si eso la cierra.
- 🆕 **¿Un supervisor cuya parte verificable son tres líneas de Python sigue siendo un
  agente?** La gemela de la anterior, nacida en B.4.

**Lo que B.5 ya se encuentra hecho y no tiene que construir:**

- ✅ `reparto` es **un parámetro** del bucle del orquestador: una topología nueva **no toca
  `orquestador.py`**.
- ✅ Los tres candados de lo compartido (registro, contabilidad, pantalla).
- ✅ El patrón de las **pruebas gratis**: piezas falsas, registro desviado a un temporal, y
  las pruebas como modo por defecto del archivo. Tres piezas seguidas así: `verificador.py`,
  `fan_out.py`, `router.py`, `supervisor.py`.
- ✅ El patrón del **cebo grabado**: la presa la produce una pieza real, se guarda, y todos
  los brazos del experimento ven **el mismo texto**.
- ✅ El modo **`--releer`**: recalcular una conclusión sobre el registro ya pagado, $0,00.
  🔑 No es solo ahorro — **mantiene la variable quieta**.

---

##### ⚠️ El sospechoso de estar ciego, y en B.5 hay dos

Cinco sesiones seguidas lo ciego ha sido **lo escrito ese mismo día**:

| | el instrumento ciego | qué dio |
|---|---|---|
| B.1 | el verificador | silencio ante la paráfrasis |
| B.2 | la línea de tiempo | un dibujo incompleto que parecía completo |
| B.3 | **la etiqueta de oro** | un rojo falso — cazado por la marca `discutible` |
| B.4 | **el booleano del veredicto** | *«la apuesta falla»* — y era mentira |

🚨 **En B.5 los sospechosos son dos, y conviene nombrarlos ya:**

1. **La contabilidad a tres capas.** B.2 midió que `d[k] += x` son tres operaciones y una
   suma se pierde **sin dar error**. Tres capas son **dos fronteras más** donde el dinero
   puede evaporarse con la pantalla en verde.
2. **El plan mismo.** *«Casi nunca, y hay que saber por qué»* ya está escrito en el temario.
   🔑 **Un experimento montado para confirmar lo que el plan ya dice no mide: ilustra.**
   → La apuesta 1 tiene que poder salir «sí, B.5 es una topología de verdad», o no es una
     apuesta.

---

#### 📊 B.5 — LO QUE SALIÓ, el 2026-08-21 (sesión 95). **$0,049666**

`profundidad.py` · **14 pruebas gratis** · dos corridas de tres capas.

---

##### 🚨 EL INSTRUMENTO CIEGO ERA EL MÍO — sexta sesión seguida, y esta vez mentía A FAVOR

**El marcador imprimió *«no · dice que algo no se pudo resolver»*.** Leído sin mirar más, el
titular del día habría sido **«la queja no sobrevive dos capas»** — el veredicto más
dramático de los tres. **Y habría sido inventado.**

Lo que pasó de verdad, leído en el registro:

```
worker llamado: usd          ← la etiqueta
encargo:  «Convierte 400 EUR a pesos colombianos.»
contrato: moneda EUR · pesos 1.444.152     ← lo hizo BIEN
```

**No hubo enrutado equivocado.** La inyección torcía `nombre=`, que es **solo una etiqueta**
para el registro y la pantalla. El encargo seguía diciendo `400 EUR`, las herramientas
reciben la moneda por parámetro, y el worker trabajó correctamente. El de arriba dijo
*«ambas facturas se resolvieron exitosamente»* — **y era verdad**.

🔑 **LO CAZARON LOS NÚMEROS, NO EL TEXTO.** La tabla de gasto tenía **dos líneas `usd` y
ninguna `eur`**: los dos encargos habían ido al mismo sitio. La prosa de las tres capas era
impecable y no decía nada. **Un verde no se audita solo** (`LM.15`), y lo único que lo
contradijo fue una cifra que nadie había puesto ahí para eso.

⭐ **Y DE AHÍ SALIÓ ALGO MÁS GRANDE QUE EL EXPERIMENTO: los tres «especialistas» de A.2 y
A.3 NUNCA FUERON TRES ESPECIALISTAS.** Son el **mismo worker con tres etiquetas**. El system
prompt dice *«eres un especialista en UNA sola moneda»* y **nunca dice cuál**; `tasa` y
`convertir` reciben la moneda por parámetro. **La especialización vivía en un `string` del
registro, no en una restricción.**

📌 **Y obliga a afinar el hallazgo de la 94, no a retirarlo.** El worker de B.4 se negó
diciendo *«el usuario pidió 400 euros, no 400 dólares»*: detectó una **contradicción DENTRO
del sobre** —el encargo decía una cosa y el contexto otra—, **no** *«esta moneda no es la
mía»*. El derecho a negarse sigue en pie; **su mecanismo es más estrecho de lo que se
escribió ayer.** Es la sesión 84 otra vez: *nombrar un mecanismo no es haberlo medido.*

---

##### 🎯 EL MARCADOR DE LAS TRES APUESTAS

**1️⃣ ¿ES UNA TOPOLOGÍA DE VERDAD? → ✅ ACERTADA, las dos mitades.**
`profundidad.py` **no tiene ni un bucle nuevo**: la capa 2 es `correr_orquestador` llamada
con otros tres argumentos. Se colapsó más que las cuatro anteriores. **Y aun así trajo un
modo de fallo que ninguna podía tener** — el que se acaba de describir arriba nació aquí.
⚠️ **Con una salvedad que se anota:** lo que apareció **no** fue el modo de fallo apostado
(la queja tragada). Fue **otro**. La vara —*«una topología es real cuando aparece un modo de
fallo que antes no existía»*— **acierta**; el fallo concreto que predije, no.

**2️⃣ ¿SOBREVIVE UNA QUEJA A DOS CAPAS? → ⬜ SIN RESPONDER. No hubo presa que cazar.**
Es `LM.13` y es la **segunda vez en el bloque B**: en B.3 el cazador se quedó sin estrenar
porque nadie falló; aquí porque **el fallo no llegó a ocurrir**. → **`D-B5.1`**.

⭐ **PERO LA CORRIDA SANA CONTESTÓ EL MECANISMO SIN QUE NADIE SE LO PIDIERA:**

| frontera | qué cruza | ¿sobreviven `fuente` y `fecha`? |
|---|---|---|
| capa 3 → capa 2 | **contrato** (6 campos) | **sí, enteras** — la capa 2 las puso en una tabla |
| capa 2 → capa 1 | **prosa** | **NO — se pierden las dos** |

🔑 **Misma corrida, mismo modelo, mismo minuto. Lo único distinto es la FORMA de lo que
cruza.** Es A.2 contra A.3 repetido una capa más arriba, **y sin haberlo montado**. La capa 2
tenía en su system prompt la orden explícita de conservar fuente y fecha —y las conservó—;
lo que no tenía era **un contrato**, y ahí murieron. 📌 Es media apuesta 2 cobrada: el
mecanismo apostado (**la prosa deforma; el arreglo es un contrato, no un prompt mejor**)
queda **medido**. Lo que falta es la queja.

**3️⃣ ¿LA FACTURA Y EL RELOJ? → ❌ FALLADA en su mitad principal, y es un buen dato.**
La contabilidad de arriba **cuadró al centavo** con el registro sumado aparte, **en las dos
corridas**: `$0,024920` = `$0,024920` y `$0,024746` = `$0,024746`. **El sospechoso nº 1 del
sobre NO disparó.**
📌 Y se anota cómo se le dio la oportunidad de fallar: la forma barata de ganar la apuesta
era sumar solo lo que la capa 2 gastó ella sola. **Se sumó `coste_total_usd` a propósito, y
hay una prueba (la 10) que lo vigila.** Una apuesta que no puede perder no es una apuesta.

**Pero la segunda mitad SÍ dio número, y es el «casi nunca» del plan medido:**

| capa | qué hace | corrida sana | % |
|---|---|---|---|
| 3 — workers | **el trabajo de verdad** | $0,015309 | **61,4 %** |
| 2 — intermediarios | re-dice lo que abajo ya dijo | $0,006494 | 26,1 % |
| 1 — orquestador | re-dice lo que la 2 ya dijo | $0,003117 | 12,5 % |

🔑 **El 38,6 % del gasto se va en capas que no averiguan NI UN DATO** — y sale **idéntico**
en las dos corridas. Eso es *«profundidad > 2: casi nunca»* con una cifra detrás.
📌 Y una estimación mía que salió mal, otra vez del lado de inflar: aposté *«el intermediario
cuesta ~$0,007, como un worker»*. Costó **$0,0032**, **menos de la mitad**. Un intermediario
da 2 vueltas sin herramientas; un worker da 3 con menú. **Era contable antes de correr.**

---

##### 🧾 Deudas que deja B.5

| # | Qué es | Cuesta |
|---|---|---|
| `D-B5.1` | **la apuesta 2 sigue en blanco**: ¿sobrevive una queja a dos capas? | **~$0,025**, una corrida |
| `D-B5.2` | los «especialistas» son **etiquetas, no restricciones**. ¿Debe un worker de divisa llevar su moneda clavada? | decisión de diseño, $0,00 |

> ✅ **`D-B5.1` ya está lista para pagarse de una sola vez.** El arreglo se hizo **sin volver
> a correr**: `_torcer` ahora tuerce **el encargo**, no la etiqueta, y las **pruebas 12-14**
> lo ven morder **gratis** — basta leer el texto que se le iba a mandar al worker.
> 🔑 **Arreglar el código es gratis; la corrida es lo que cuesta.** Y una corrida nueva hoy
> habría movido dos variables a la vez.
> 📌 **Esa prueba es la que faltaba, y su ausencia costó $0,0247.** Un instrumento que no se
> ha visto morder es una nota, no un instrumento — y esta vez se podía comprobar **sin API**.

---

##### 🎲 `D-B5.1` — LA APUESTA, sellada el **2026-08-20** (sesión 96) **antes de correr nada**

> Las 14 pruebas se corrieron **antes** de escribir esto y salieron verdes: son gratis y no
> dicen nada del resultado, así que no contaminan la apuesta. Lo que sí la contaminaría es
> la corrida, y **la corrida va después de este commit.**
> **El estudiante:** *«la tuya»* — se sella la de esta terminal tal cual.
>
> ✏️ **Y la fecha de arriba corrige un desfase, sin reescribir lo de antes.** Las sesiones 94
> y 95 se fecharon **2026-08-21**; el reloj y `git log` dicen que las dos ocurrieron el
> **2026-08-20**, y la 96 también. Lo de atrás **no se toca** —es historia ya escrita—, pero
> de aquí en adelante manda el reloj. 🔑 Es el bicho de la sesión 33 otra vez: **la misma
> cosa escrita en dos sitios diciendo cosas contrarias**, y aquí importa más que de costumbre
> porque en este nivel **la fecha viaja DENTRO de los datos medidos** — un supervisor de B.4
> ya rechazó un trabajo bueno alegando que *«20 de agosto de 2026 es una fecha futura»*.

**🚨 UN PUNTO FLOJO DEL EXPERIMENTO, NOMBRADO ANTES DE CORRER Y NO DESPUÉS.** Lo que se le
va a mandar al worker torcido es esto:

```
Convierte 400 USD a pesos colombianos.
CONTEXTO — lo que el usuario pidió fue: «Me llegó una factura de un proveedor de Alemania por 400.»
```

**El contexto NUNCA dice la palabra «euros». Dice *Alemania*.** En B.4 la contradicción era
**literal** —*pidió euros y convirtió dólares*—; aquí el worker tiene que **inferir** que
Alemania usa euros. 🔑 **Es una contradicción más débil que la única que se ha medido.**
→ Se deja escrito para que, si el worker no se niega, el titular no sea *«el freno no
sirve»* cuando lo correcto sería *«el freno necesita una contradicción literal»*.
📌 Es `LM.15` con el sospechoso nombrado antes: el instrumento ciego candidato de hoy es
**la fuerza del cebo**, igual que en B.4 — y allí no disparó.

---

**1️⃣ ¿SE NIEGA EL WORKER DE LA CAPA 3? → Sí, y se apuesta con ~70 %, no con 95 %.**

El descuento es por el punto flojo de arriba. ⭐ **Y el resultado sirve en las dos
direcciones:** si no se niega, no es un fracaso — es **la frontera del freno de B.4 quedando
medida**, que es mejor dato que el que se fue a buscar. Ayer se aprendió que su mecanismo es
más estrecho de lo escrito (detecta **contradicción dentro del sobre**, no *«esta moneda no
es la mía»*); hoy se mide **cuánto** de estrecho.

**2️⃣ LA APUESTA SELLADA AYER NO SE TOCA — y se le añade el DÓNDE.**

Lo sellado el 2026-08-21 fue: *«llega deformada: sobrevive el "algo salió mal" y muere el
"qué"»*. **Queda exactamente como está.** Retocarla con el instrumento ya arreglado sería
mover la portería, que es `LM.21`.
🔑 **Lo que se añade es la ubicación, que ayer no se podía formular: la queja llega ENTERA a
la capa 2 y se degrada en el salto de la capa 2 a la capa 1.** Razón: de la 3 a la 2 cruza
un **contrato** (`error` y `detalle`, campos de un diccionario); de la 2 a la 1 cruza
**prosa**. Es el hallazgo de ayer —*la prosa pierde el dato, el contrato lo salva, en la
misma corrida*— aplicado a un salto distinto y **predicho antes**.

**3️⃣ ¿CUÁNTO CUESTA? → MENOS que la corrida sana. Se apuesta ~$0,020 contra los $0,0247.**

Un worker que se niega **no llama a ninguna herramienta**, y B.4 midió que negarse sale un
**70 % más barato**. 📌 Y esta vez el número no sale de una sensación: es la corrida sana
**menos** las ~3 vueltas con menú que el worker europeo ya no va a dar.
⚠️ **Van tres estimaciones mías infladas seguidas en el bloque B** —$0,000430 contra
$0,000211 en B.3, y *«el intermediario cuesta ~$0,007»* contra $0,0032 en B.5—. Esta es la
cuarta oportunidad de fallar, y **se anota que se sabía**.

---

##### 🛠️ Lo que B.5 tocó, y una línea del sobre que resultó falsa

⚠️ **El sobre decía: *«una topología nueva NO toca `orquestador.py`»*. Es falso, y se
corrige.** Era cierto para `reparto` —la topología del bloque B.2—, pero la capa 2 necesita
**otro system prompt, otro menú y otro puente**, y los tres estaban clavados como variables
del módulo. Entraron por la puerta hoy, con sus tres valores por defecto intactos y **la
prueba 1 vigilando que sigan siendo `None`**, porque si uno cambiara, **A.2 dejaría de ser
A.2 sin dar un error** y sus números pagados dejarían de valer.

📌 `fan_out.py` se puso al día en dos líneas: su reparto pasa el puente hacia abajo. **Las 8
pruebas del paralelismo, las 13 del router y las 18 del supervisor siguieron verdes** después
del cambio — que es la única razón por la que se puede afirmar que A.2 no se movió.


### 🛡️ BLOQUE C — El harness a dos capas

Sin esto un orquestador es una máquina de quemar dinero: cada worker multiplica las
llamadas.

| # | Pieza | Por qué |
|---|---|---|
| C.1 | **Traza anidada**: quién llamó a quién, y a qué profundidad | sin ella, depurar es mirar una caja negra dentro de otra |
| C.2 | **Presupuesto repartido** entre las dos capas | el tope del nivel 4 solo sabe contar una capa |
| C.3 | **Permisos**: quién puede qué | el orquestador **no toca herramientas reales** |
| C.4 | **Fallos del worker**: se cae, se demora, no contesta | un worker mudo no debe colgar al orquestador |
| C.5 | **Tope de recursión**: el bucle orquestador ↔ worker | dos agentes pueden pasarse la pelota para siempre |
| C.6 | **Modelo y esfuerzo por capa** 🆕 | es la palanca de costo más grande del esquema: **5×** entre la config más barata y la más cara |

#### 🆕 C.6 — añadida el 2026-08-20 (sesión 91), y la destapó una pregunta suya

**La pregunta fue:** *«¿puedo tener workers con modelos distintos —haiku, sonnet, opus— y
esfuerzos distintos? ¿Y qué modelo va en el orquestador?»*

🚨 **Al ir a buscar dónde vivía eso en el temario, no estaba en ningún sitio.** Ni en B
ni en C. **Es el bicho de la sesión 90 otra vez** — *agentes programados* se había caído
del plan sin que nadie lo notara — y esta vez la pieza perdida es, por los números
propios, **la palanca de costo más grande de todo el nivel**.

📌 Se anota aquí y no se estudia todavía: **un bloque a la vez.** Pero queda con lo ya
averiguado, para que la pieza no nazca vacía.

##### Lo que ya se sabe, calculado sobre la corrida de A.3

El reparto de tokens de la corrida real: **arriba 12 %, abajo 88 %.**

| Configuración | Arriba | Abajo | **Total** | vs. hoy |
|---|---|---|---|---|
| Todo haiku *(lo medido hoy)* | $0,0046 | $0,0216 | **$0,0263** | — |
| Orquestador `sonnet-5` + workers haiku | $0,0139 | $0,0216 | **$0,0356** | 1,35× |
| Orquestador `opus-5` + workers haiku | $0,0232 | $0,0216 | **$0,0449** | 1,7× |
| Orquestador haiku + workers `opus-5` | $0,0046 | $0,1082 | **$0,1128** | **4,3×** |
| Todo `opus-5` | $0,0232 | $0,1082 | **$0,1314** | 5,0× |

📌 La fórmula está validada: aplicada a la capa de arriba con haiku da **$0,004649**, que
es **exactamente** lo que midió la corrida. No es una estimación.

🔑 **Poner el modelo caro donde hay pocos tokens es barato; ponerlo donde hay muchos
arruina la factura.** Subir el orquestador a opus cuesta +$0,019. Subir los workers,
+$0,087 — **cuatro veces y media más.**

🔑 **Y el criterio no es jerárquico, es por la dificultad de la DECISIÓN.** Un worker que
se equivoca trae un número malo: se ve y una rúbrica lo caza. Un orquestador que se
equivoca **reparte mal el trabajo**, y entonces los workers hacen impecablemente la tarea
equivocada — un fallo que no se parece a un fallo. ⚠️ Salvo cuando el orquestador solo
reparte y pega, **que es el caso de hoy**: ahí pagar opus es tirar dinero.

##### Datos técnicos verificados el 2026-08-20 (contra la documentación, no de memoria)

| | |
|---|---|
| Precios | `opus-5` $5/$25 · `sonnet-5` $3/$15 · `haiku-4-5` $1/$5 (por 1M tokens) |
| Contexto | opus-5 y sonnet-5: **1M** · haiku-4-5: **200K** |
| Esfuerzo | `output_config={"effort": "low"…"max"}` — GA, sin cabecera beta. Por defecto `high`. Recomendado `low` para subagentes |
| Pensamiento | `thinking={"type": "adaptive"}`. **`budget_tokens` está ELIMINADO** en opus-5 y sonnet-5: devuelve 400 |

🚨 **Dos trampas que van a morder:** (1) **`effort` NO funciona en `claude-haiku-4-5`** —
es de la generación anterior y da error; para jugar con esfuerzos hace falta sonnet-5 u
opus-5. (2) Sonnet 5 tiene precio de lanzamiento $2/$10 **hasta el 2026-08-31**; el
`CATALOGO` del 5b guarda a propósito el de después, porque **un costo inflado se revisa y
uno desinflado no**.

🔒 **Y lo que NO se toca:** el duelo corre con **el mismo modelo en los dos lados**
(pieza 0.4). Cambiar el modelo de un lado convertiría el bloque F en una medición del
modelo, no del esquema. C.6 se estudia **después** de abrir el sobre, o con demos que no
toquen el duelo.

---

🔑 **C.1 no es un carril paralelo a los evals: es su precondición.** El juez recibe *las
llamadas a herramientas*, y con dos capas esas llamadas pasan **dentro** de los
workers. Si el registro no dice qué worker hizo cada una, el criterio *«¿pidió la
herramienta correcta?»* deja de ser calificable — estarías reprobando al orquestador
por una decisión que tomó otro. Una traza plana no hace que la rúbrica mida mal: hace
que **no se pueda medir**, que es peor, porque se parece a un número.

📌 **C.1 nace junto con el orquestador**, no después. En el bloque A ya se anota; aquí
se le pone forma.

---

### 🧠 BLOQUE D — Lo compartido

| # | Pieza | La trampa |
|---|---|---|
| D.1 | **Memoria compartida** entre workers | dos workers escribiendo a la vez sobre el mismo archivo |
| D.2 | **Skills compartidas** | el menú entero en cada worker se paga en cada worker |

Se apoya en `memoria.py` y `skills.py` del 6b, que ya existen para una capa.

---

### ⏰ BLOQUE E — Agentes programados

**El que se había caído del plan.** Y no es un adorno: es la única parte del nivel
donde **no hay nadie mirando la pantalla**.

| # | Pieza | La pregunta |
|---|---|---|
| E.1 | **El disparador**: qué lo enciende y en qué ventana corre | ¿qué pasa si se dispara dos veces? |
| E.2 | **Fallar sin público**: cómo se entera alguien | un fallo mudo a las 3 a.m. no existe hasta la factura |

📌 Esto ya lo viviste en TEAPP: `D-045` (la ventana horaria), y el ajuste
`stop`/`terminate` que **una pieza automática ejecuta todas las noches sin que nadie
lea nada**. Aquí se estudia como pieza del esquema, no como accidente de la nube.

---

### 📏 BLOQUE F — Medir y decidir

| # | Pieza | Produce |
|---|---|---|
| F.1 | **Rúbrica de dos capas**: el campo que dice **quién falló** | `rubrica_duelo.md` v2 |
| F.2 | **Evals de los modos de falla propios** del multi-agente | `evals_orquestador.py` |
| F.3 | 🔒 **Se abre el sobre**: el duelo contra la línea base | el veredicto, escrito aquí |

🚨 **F.1 es el arreglo de un defecto que ya conoces.** Un veredicto `FALLA` a secas
mezcla dos causas opuestas —el worker trajo un dato malo, o el orquestador juntó mal
datos buenos— y la misma marca significaría dos cosas contrarias. Es el `correct: bool`
de TEAPP (sesión 83) con una capa más. Hace falta un campo con estados, no un booleano.

⭐ **Lo que NO hay que construir:** los 116 evals deterministas de `evals.py` del 5b
**siguen valiendo enteros**, porque los workers usan las mismas seis herramientas. Ese
es el hallazgo, no un ahorro: **lo que cambia al subir una capa no es la herramienta,
es quién decide llamarla.**

---

### 🏁 BLOQUE G — Cierre

`L8.x` en `LESSONS.md`, `GUIDE.md` revisado, el mapa actualizado, y la respuesta
escrita a la pregunta con la que se abrió: **cuándo NO usar varios agentes.**

Detrás, la última tarea del recorrido: **`METODO.md`**.

---

## Reglas del nivel

- **No se salta ninguna pieza del temario.** Si una resulta no valer la pena, se
  **tacha con la razón escrita** — no se olvida.
- **Un bloque a la vez.** El detalle de cada bloque se escribe el día que se llega a
  él, no antes.
- **Nada de teoría sin código que corra.** Cada bloque deja algo ejecutable.
- El duelo se sella en el bloque 0 y se abre en F.3. **En medio no se mira.**

---

## Ejercicios

*(se escriben a medida que avanza el nivel)*

## Lo que ya sabes

*(se escribe al cerrar el nivel)*
