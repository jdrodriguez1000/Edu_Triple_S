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
| B.3 | **Router**: elige UN worker, no varios | muchos casos distintos, uno a la vez |
| B.4 | **Supervisor**: el orquestador juzga y reenvía | cuando la primera respuesta puede no servir |
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
