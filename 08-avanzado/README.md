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

##### 📊 `D-B5.1` — LO QUE SALIÓ, el 2026-08-20 (sesión 96). **$0,016262** · 9 llamadas

**🎯 Marcador: 3 de 3 acertadas** — una de ellas **con el mecanismo solo a medias**.

**1️⃣ El worker SE NEGÓ, y el punto flojo NO disparó — con prueba.** Dijo:
*«Ese encargo no es para mí: el usuario pidió la conversión de **euros (moneda de Alemania)**,
no de dólares estadounidenses.»* ⭐ **El paréntesis es la prueba: hizo la inferencia en voz
alta.** Se avisó antes de correr que el cebo era débil porque el contexto nunca dice «euros»;
el modelo cerró el hueco solo. **1 vuelta, CERO herramientas, $0,002115.**
📌 Segunda vez en el bloque que un sospechoso nombrado antes no dispara (B.4 fue la primera),
y **la prueba es del mismo tipo: quedó grabado el texto exacto.**

**2️⃣ LA QUEJA MUERE EN EL SALTO 2→1, exactamente donde se apostó.** La misma queja, tres
capas, misma corrida:

| capa | qué dijo | qué cruza |
|---|---|---|
| **3** worker | *«no es para mí: el usuario pidió **euros**, no dólares»* | — |
| **2** intermediario | *«el especialista reporta que no es para él: **euros, no dólares**. Por lo tanto, no tengo el dato»* | **contrato** ✅ llega entera |
| **1** arriba | *«No se pudo resolver… **el especialista no tiene el dato de conversión**»* | **prosa** 🚨 muere |

🔑 **Y CÓMO murió es más fino que la predicción.** La capa 2 dijo **dos** cosas: la **causa**
(*mandaron dólares donde iban euros*) y la **consecuencia** (*por lo tanto no tengo el dato*).
**La capa 1 conservó la consecuencia y tiró la causa** — y se quedó con **la mitad inútil**:
*«no tiene el dato»* no le dice a nadie qué arreglar.
📌 La apuesta sellada el día antes —*«sobrevive el "algo salió mal" y muere el "qué"»*— queda
**pagada y acertada**, y ahora con el sitio exacto.

**⭐ EL HALLAZGO DEL DÍA, Y NADIE LO MONTÓ: LA RED SE CAYÓ SOLA.** El worker de Norteamérica
no pudo consultar la tasa (`URLError`) en mitad de la corrida. Eso regaló **un grupo de
control gratis**, igual que en B.5. Quedaron **dos fallos de naturaleza opuesta**:

- **Europa** → **culpa nuestra y arreglable**: enrutamos mal.
- **Norteamérica** → **transitorio y ajeno**: se cayó la red; se reintenta y ya.

Y así llegaron los dos a la capa 1: *«Ninguna de las dos se pudo convertir **por falta de
datos de conversión**»*.
🚨 **INDISTINGUIBLES.** Un bug propio y un hipo de la red, fusionados en una frase con el
mismo tono. Es el `correct: bool` de la sesión 83 de TEAPP —causas contrarias en la misma
casilla— pero **en PROSA y a tres capas**, y aquí es **peor que un booleano: suena
informativo.** → **`D-B5.3`**, y es material de `C.4`.

**3️⃣ EL COSTE: dirección acertada, número inflado — la CUARTA seguida.** Apostado ~$0,020
contra los $0,0247 de la corrida sana; salió **$0,016262**. ⚠️ **Y parte del ahorro no es
mío:** el fallo de red le quitó una vuelta al worker de Norteamérica. **Acertar la casilla no
es haber acertado el mecanismo** — segunda vez en dos sesiones que se anota esta misma frase.

**📌 LA CONTABILIDAD CUADRÓ AL CENTAVO POR TERCERA VEZ** ($0,016262 = $0,016262). La apuesta 3
de la sesión 95 sigue **fallada**, ahora con una corrida más y **con un fallo dentro**.

> ✅ **`D-B5.1` PAGADA. El bloque B queda cerrado sin la apuesta 2 en blanco.**
> ⚠️ **Lo que NO se midió:** el coste quedó **contaminado** por la caída de red, y no se
> vuelve a correr — la pregunta de la deuda se contestó, y con más nitidez de la esperada.
> **Volver a correr por un número limpio sería pagar $0,02 por decorar un dato que ya no
> decide nada.**

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
| C.1 | ✅ **Traza anidada**: quién llamó a quién, y a qué profundidad | sin ella, depurar es mirar una caja negra dentro de otra |
| C.2 | ✅ **Presupuesto repartido** entre las dos capas | el tope del nivel 4 solo sabe contar una capa |
| C.3 | ✅ **Permisos**: quién puede qué | el orquestador **no toca herramientas reales** — y el permiso **no dice si te contestaron TU pregunta** |
| C.4 | ✅ **Fallos del worker**: se cae, se demora, no contesta | un worker mudo no debe colgar al orquestador |
| C.5 | ✅ **Tope de recursión**: el bucle orquestador ↔ worker | dos agentes pueden pasarse la pelota para siempre |
| C.6 | ✅ **Modelo y esfuerzo por capa** | es la palanca de costo más grande del esquema: **5×** entre la config más barata y la más cara |

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

#### 🎲 C.1 — LA APUESTA, sellada el **2026-08-21** (sesión 97) **antes de la primera línea de código**

> **El estudiante:** *«sello con la tuya»* — se sella la de esta terminal tal cual.
> Lo que se cuenta abajo se contó **antes** de escribir las apuestas, sobre registros que
> ya existían: es gratis, no hace falta correr nada y no contamina lo apostado.

##### 📏 LO QUE SE CONTÓ ANTES DE APOSTAR — $0,00, y no era una apuesta

📌 **Se cuenta a propósito, y el motivo es un vicio propio:** van **cuatro estimaciones de
coste infladas seguidas** en el bloque B, y las cuatro eran **contables antes de correr**.
La corrección no es estimar mejor. Es contar lo que se puede contar y apostar solo lo demás.

**1. Las dos capas escriben en ARCHIVOS DISTINTOS.** `registro_orquestador_{MODELO}.jsonl`
(82 líneas) y `registro_workers_{MODELO}.jsonl` (225 líneas). **Ni un solo campo los une.**
🔑 El árbol de la traza no está aplastado en una lista: está **partido en dos**, y la costura
no se guardó en ningún sitio.

**2. El campo que dice *quién* se llama distinto en cada lado.** Arriba `capa`; abajo
`worker`. Lo mismo con dos nombres, y ninguno apunta al otro. **No existe `id`, ni `padre`,
ni `profundidad`, ni identificador de corrida** en ningún registro del nivel 8.

**3. El reloj está a SEGUNDOS** (`isoformat(timespec="seconds")`), y este es el número:

| | |
|---|---|
| Arranques de worker grabados | **35** |
| Segundos con más de un arranque | **1** → `2026-08-20T19:21:11`, con **3 workers** |

🔑 **Y dice dos cosas opuestas a la vez.** El pegamento pobre —*«los uno por la hora»*—
acertaría **32 de 35** veces. Y falla **exactamente en el fan-out paralelo**, que es la
pieza de la que el bloque B está más orgulloso. ⭐ **La traza plana no se rompe al azar: se
rompe en el sitio que se construyó para presumir.** Es `LM.15` con otra cara — el
instrumento no da un dato falso el 91 % del tiempo, y por eso el 9 % restante se lee como
ruido en vez de como avería.

**4. Los 35 arranques son de corridas DISTINTAS** —B.1 a B.5— apiladas en el mismo archivo,
y **tampoco hay campo que diga a cuál pertenece cada línea**.

##### 🎯 QUÉ MIDE C.1, entonces

Ya no es *«construir una traza anidada»* a ciegas: es **ponerle al registro `id`, `padre` y
`profundidad`, reconstruir el árbol de una corrida real, y ver si dice algo que la traza
plana no decía.** El criterio de éxito **no** es que el árbol se dibuje: es
**¿habría cazado antes alguno de los bichos que YA se pagaron?**

---

**1️⃣ EL ÁRBOL NO CAMBIARÁ NINGUNA CONCLUSIÓN YA PAGADA DEL BLOQUE B — pero habría abaratado
la de la sesión 95. Se apuesta con ~80 %.**

Aquel defecto se cazó mirando una tabla de gasto y viendo **dos líneas `usd` y ninguna
`eur`**: eso es un árbol leído a mano, sin árbol. Con `padre` grabado, el mismo defecto salta
**sin tener que sospechar nada**, porque la rama `eur` sencillamente **no existe**.
⭐ Sirve en las dos direcciones: si el árbol **sí** cambia una conclusión pagada, eso es peor
noticia y mejor dato — querría decir que algo del bloque B se cerró sobre un número mal
atribuido.

**2️⃣ C.1 CUESTA $0,00.** Todo sale de releer registros que ya existen y de pruebas
deterministas.

📌 **Esta apuesta está puesta para poder fallar, y se anota que se sabía.** Si al final hace
falta una corrida nueva para validar el parentesco de punta a punta, **está fallada** — y
entonces la quinta estimación seguida no habrá sido inflada sino corta, que es un vicio
nuevo y también cuenta.

**3️⃣ LA `capa` DE HOY ES UNA ETIQUETA DECORATIVA: AL TORCERLA NO SE ROMPE NADA.**

Predicción concreta y falsable: si se cambia a mano el `capa=` de una línea del registro,
**ninguna prueba se pone roja, ninguna suma cambia, ningún informe protesta.**
🔑 **Es literalmente el bicho de la sesión 95** —`nombre=` era solo una etiqueta y torcerla
no enrutó nada mal— **y se apuesta a que sigue vivo, en otro campo, sin que nadie lo haya
tocado.** ⚠️ Si esta apuesta gana, el hallazgo no es *«hay que añadir `padre`»*: es que
**el nivel 8 lleva cinco piezas creyendo que sabe quién hizo qué, y lo que tiene son
adjetivos.**

##### ⚠️ El sospechoso de estar ciego, nombrado antes de escribirlo

Van **siete sesiones** en que el instrumento ciego ha sido lo escrito **ese mismo día**.
Nombrarlo antes lo desarmó las dos últimas veces. El candidato de hoy:

🚨 **El que escribe `padre=` es el mismo que ya sabe quién es el padre.**

Esa línea va a ir justo donde el código tiene la respuesta delante. **El árbol va a salir
perfecto — y eso no probará que el harness conozca el parentesco: probará que lo dibujé yo.**
Un árbol bonito escrito por quien ya lo conocía **mide al que lo escribió**, igual que un
cebo redactado por quien monta el experimento (B.4).

→ **La defensa, y se sella como obligación, no como intención:** una prueba que **tuerce el
parentesco a propósito** y exige que algo se ponga **rojo**. 🔑 **Si esa prueba no se puede
escribir, `padre` es una etiqueta más y C.1 no midió nada** — y entonces la apuesta 3 se
habría cumplido dos veces: en el campo viejo y en el que se escribió hoy para arreglarlo.

---

##### 📊 C.1 · PASO 1 — LO QUE SALIÓ, el 2026-08-21. **$0,00 · apuesta 3 CONFIRMADA**

`traza.py` · 6 pruebas gratis · el experimento no llamó a la API ni una vez.

**Qué se hizo:** sobre los **307 renglones** de los dos registros reales, se renombró el
dueño `eur` → `usd`. **35 renglones cambiaron de dueño y no se tocó ni un número:** ni un
costo, ni un token, ni una hora, ni el orden.

| Lo que el auditor ve | sano | torcido | ¿lo notó? |
|---|---:|---:|:-:|
| total en dólares | 0,278603 | 0,278603 | 🚨 **NO** |
| llamadas a la API | 117 | 117 | 🚨 **NO** |
| `eur` | 0,036617 | **0,000000** | *desapareció* |
| `usd` | 0,105773 | **0,142390** | *se quedó con el gasto ajeno* |

**Y las 14 pruebas de `profundidad.py`, corridas contra el registro torcido: 14 verdes, 0
rojas, código de salida 0.** Nada se puso rojo en todo el nivel.

🔑 **LA APUESTA 3 GANA, Y EL NÚMERO ES PEOR QUE LA APUESTA: $0,036617 cambiaron de dueño y
el total no se movió ni una millonésima.** El campo `capa` no es un dato del harness: es
un adjetivo que se escribe una vez y **nadie vuelve a mirar**. El único lector que tiene en
todo el nivel 8 es `auditar()`, y lo usa para *imprimir* un reparto, no para comprobarlo.

⭐ **PERO EL HALLAZGO DEL DÍA NO ES ESE, Y ES INCÓMODO: el experimento reprodujo, a mano y
gratis, EXACTAMENTE el síntoma con el que se cazó el hallazgo de la sesión 95.**

Aquel día el defecto se destapó porque la tabla de gasto tenía **dos líneas `usd` y ninguna
`eur`**. Hoy, sin tocar el enrutado ni llamar a nadie, se ha fabricado esa misma tabla
—`eur` en cero, `usd` con el gasto de los dos— **solo renombrando etiquetas**.

🚨 **Es decir: el síntoma que produjo el mejor hallazgo del bloque B tiene DOS causas
posibles —un enrutado realmente torcido, o un simple error de etiqueta— y el harness no
sabe distinguirlas.** Aquella vez la causa era real, y se comprobó leyendo el texto del
encargo. **Pero se comprobó a mano, y solo porque alguien sospechó.**

🔑 **Y hay una tercera cosa, que es la que de verdad duele:** *«la contabilidad cuadró al
centavo»* se ha declarado **tres sesiones seguidas** (94, 95, 96) como prueba de que las
cuentas están sanas. Hoy queda medido que **ese número es ciego a quién gastó**. No está
mal: está contestando una pregunta más pequeña de la que parecía. Cuadrar la suma **no es
haber atribuido nada.**

📌 **Y esto NO es un defecto de `auditar()`.** Su trabajo es la aritmética y la hace bien —
la prueba 3 de `profundidad.py` lo vigila contra un registro cuyo total se sabe. El defecto
es que **la atribución no tiene dueño**: `por_capa` se calcula, se imprime, se usa para
sacar conclusiones, y **no hay una sola prueba en el nivel que la compruebe**.
🔑 Es `LM.15` otra vez, y de la peor forma: no es un instrumento que dé un dato falso — es
un instrumento **al que nadie le pregunta nunca si acertó**.

➡️ **Lo que esto le cambia al paso 2, antes de escribirlo:** añadir `padre` no arregla
nada por sí solo. Si `padre` nace sin nadie que lo compruebe, será el tercer adjetivo del
registro —después de `capa` y `worker`— y C.1 habrá cambiado una etiqueta por otra más
larga. **La obligación sellada en el sobre deja de ser una precaución y pasa a ser la
pieza:** la prueba que tuerce el parentesco y exige rojo.

---

##### 🐛 EL BICHO LATERAL DE C.1, MUERTO EL MISMO DÍA — y salió sin buscarlo

**Importancia: media · Urgencia: no bloqueante.** No rompía ningún número —queda medido más
abajo— pero era una mina cebada.

**Qué pasaba:** la prueba 2 de `profundidad.py` llama a `ejecutar_un_bloque`, que llama a
`anotar`, que escribe **donde diga `orquestador.REGISTRO`** — o sea, en el archivo de las
corridas **PAGADAS**. Cada vez que se corrían las pruebas *gratis*, el registro de verdad
crecía una línea inventada. Había **cuatro** dentro, y **una está commiteada en `e3ee1ba`**.

🔑 **Y lo peor no es el bicho: el arreglo ya estaba escrito en el repo, un archivo más allá.**
`fan_out.py` (sesión 93) hacía exactamente esta desviación **a mano**, con un comentario
citando la sesión 50 de TEAPP. `profundidad.py`, escrito **dos sesiones después**, no lo
alcanzó. **Es `LM.20` por cuarta vez: la corrección existía y nadie llegó a ella.**

##### 🔧 Cómo se mató — en el ORIGEN, y con portero encima

| | |
|---|---|
| **El origen** | `orquestador.registro_desviado()` — un `with` que manda a un temporal todo lo que se anote dentro, y restaura en el `finally`. Vive donde vive `anotar`, no en cada archivo que se acuerde de copiarlo. |
| **El uso** | `profundidad.py` prueba 2, envuelta. |
| **El portero** | `traza.portero()` — corre las pruebas gratis de **los cinco módulos** del nivel y exige que los registros reales **no crezcan ni una línea**. |

⭐ **El portero es el arreglo de verdad; el `with` solo arregla un archivo.** El portero
arregla la **clase**: cualquier prueba de cualquier módulo —**incluidos los que todavía no
existen**— que escriba en el registro pagado, lo pone rojo. Es la sesión 49 de TEAPP: se
arregla en el origen **y encima** se pone un portero sobre los datos enteros.

🚨 **Y SE VIO MORDER, que es lo que lo separa de una nota (`LM.13`).** La prueba 7 de
`traza.py` **le quita el arreglo a `profundidad.py`** —anula el desviador— y exige que el
portero **se ponga rojo**. Todo sobre **copias**: el experimento que comprueba que nadie
ensucia los datos de verdad sería un chiste si ensuciara los datos de verdad.

##### 🧹 Las cuatro líneas, retiradas — y por qué se puede afirmar que no movieron nada

Se retiraron del registro `2026-08-20T20:31:14`, `20:36:17`, `20:43:45` y `2026-08-21T14:20:23`.
**Las cuatro eran `evento: "herramienta"`, ninguna era `llamada_api`** — y `auditar()` solo
suma `llamada_api`. Medido antes y después de quitarlas:

| | antes | después |
|---|---:|---:|
| total auditado | 0,278603 | **0,278603** |
| llamadas | 117 | **117** |
| líneas del registro | 83 | **79** |

📌 **No se borra historia: se retira basura del instrumento.** Y se anota aquí lo que se quitó,
para que la retirada quede en el sitio donde sí es historia. ⚠️ **Lo que sí hay que decir:
hoy no hacía daño por suerte, no por diseño.** Bastaba una prueba futura que registrara una
`llamada_api` para meter dinero inventado en la factura del bloque F.

🔑 **Y es C.1 puro, no una anécdota de higiene: esto pasa porque el registro no tiene
identificador de corrida.** Una línea de prueba y una línea pagada viven en el mismo archivo
sin nada que las separe — **el punto 4 de lo que se contó al abrir la sesión, mordiendo el
mismo día en que se escribió.**

---

##### 🌳 C.1 · PASO 2 — EL PARENTESCO, el 2026-08-21. **$0,00 · 20 pruebas**

`contexto.py` (nuevo) · `traza.arbol()` · `traza.demo()`. Ni una llamada a la API.

**Lo que se añadió al registro:** `corrida`, `id`, `padre`, `profundidad` y `tramo`.

🔑 **Y lo primero, porque desarma el sospechoso del sobre: NO HAY UNA SOLA LÍNEA EN TODO EL
NIVEL 8 QUE PASE UN `padre=`.** El sobre avisó que *«el que escribe `padre=` es el mismo que
ya sabe quién es el padre»*, y un árbol dibujado por quien lo conocía mide al que lo dibujó.
→ El parentesco **se deduce de dónde está el programa cuando anota**, con `contextvars`, y
quien lo deduce es la librería estándar. Una variable de contexto no es una carta que va de
mano en mano: **es la luz de la habitación.** Quien entra la tiene; quien sale la pierde.

##### 🚨 Y la trampa muerde EXACTAMENTE donde ya mordía la traza plana

**Un hilo nuevo no hereda el contexto.** `ThreadPoolExecutor` no lo copia. Sin arreglo, los
tres workers del fan-out de B.2 anotarían con `padre: null` y `profundidad: 0` — **el árbol
saldría plano y con pinta de correcto**, sin un solo error.

⭐ **Es el mismo sitio donde falla unir por el reloj** (un segundo con tres arranques, contado
esta mañana). 🔑 **El paralelo es el único lugar donde *«lo que pasó justo antes»* deja de
significar *«quien me llamó»*** — y por eso es donde se rompe **toda** forma barata de saber
quién es quién. → `contexto.atado()`, una copia del contexto **por tarea**.

📌 **Y se ve morder, no se promete:** la prueba 12 corre tres hilos **sin** `atado` y exige
que los tres salgan huérfanos; la 13 los corre **con** `atado` y exige que los tres cuelguen
del padre correcto. El bicho y su arreglo, los dos en verde, en la misma corrida.

##### 🌳 El árbol, dibujado — `python traza.py --demo`, $0,00

```
capa:orquestador          t2   total $0.016410   propio $0.001989
   tool:consultar_moneda  t3   total $0.004807   propio $0.000000
      worker:usd          t4   total $0.004807   propio $0.004807
   tool:consultar_moneda  t5   total $0.004807   propio $0.000000
      worker:eur          t6   total $0.004807   propio $0.004807
   tool:consultar_moneda  t7   total $0.004807   propio $0.000000
      worker:cad          t8   total $0.004807   propio $0.004807
```

📌 Los workers son falsos —lo que se mide es el parentesco, no el modelo— pero **el camino
es el de verdad**: `reparto_en_paralelo`, `ejecutar_un_bloque` y los dos `anotar`. Un árbol
dibujado por un camino de mentira mediría al camino de mentira.

⭐ **Y ya dice algo que la tabla plana no decía: `propio $0.000000` en los tres escalones de
en medio.** El *«38,6 % del gasto en capas que no averiguan ni un dato»* de B.5 dejó de ser
una cuenta a mano: **es la forma del árbol.**

##### ⚠️ Y una limitación que CAMBIA EL PLAN DEL PASO 4, dicha en cuanto se supo

**Los registros pagados de las sesiones 92 a 96 no se pueden convertir en árbol.** No es que
sea caro: **es imposible.** `id` y `padre` no están ahí, y no hay de dónde sacarlos — unir
por el reloj falla justo en el paralelo.

🔑 **La traza es la única pieza del harness que no se puede añadir hacia atrás.** Un test se
escribe después. Un presupuesto se pone después. Un árbol, **no**: o la línea nació sabiendo
de quién era hija, o esa línea ya nunca lo va a saber. **Lo que no se instrumentó, no
ocurrió.** 📌 Queda como **prueba 20**, para que no se olvide y para que el paso 4 se
replantee: reconstruir *una corrida ya grabada* solo puede significar **una corrida nueva**.

##### 🧾 Lo que el paso 2 dejó, y lo que decide del paso 3

| | |
|---|---|
| `contexto.py` | `tramo` · `marca` · `atado` · `envuelto` — sin dependencias, lo comparten las dos capas sin importarse entre sí |
| Tocado | los dos `anotar`, `correr_orquestador`, `correr_worker`, `ejecutar_un_bloque`, `reparto_en_paralelo` |
| Pruebas | **20 en verde**, y las 14 de `profundidad.py` + las de router, supervisor, fan_out y verificador **siguen verdes** |
| Registro | 79 + 225 líneas, **sin crecer** — el portero sigue mordiendo |

🔑 **Y queda dicho cuál de los cinco campos nuevos es estructura y cuál es decoración:**
`corrida`, `id`, `padre` y `profundidad` **aguantan el peso**; `tramo` es **una etiqueta**,
de la misma clase que la `capa` que el paso 1 midió que se podía torcer impunemente. Se
incluye igual, porque sin nombre legible el árbol no se lee. **El paso 1 no enseñó que las
etiquetas sobren: enseñó que hay que saber cuáles lo son.**

➡️ **El paso 3 sigue siendo la obligación sellada, y ahora tiene blanco concreto:** la prueba
que tuerce el parentesco y exige rojo. Las pruebas 12 y 18 ya son media pieza —una tuerce el
mecanismo, la otra el resultado—; **falta torcer el `padre` de un registro grabado**, que es
la forma exacta en que el paso 1 mató a `capa`.

---

#### 🎲 C.1 · PASO 3 — LA APUESTA, sellada el **2026-08-21** (sesión 97) **antes de la primera línea de código**

> ⚠️ Se escribe y se **commitea antes** de escribir `torcer_padre`. Una apuesta en un archivo
> sin commitear se puede retocar sin dejar rastro, y entonces no es una apuesta: es un
> comentario. Es la quinta sesión seguida que se sella así.

##### 📏 Lo que ya se sabe, y NO es la apuesta

Dos cosas quedaron medidas antes de apostar, así que no cuentan:

1. **No existe ningún registro grabado con parentesco.** Los pagados de las sesiones 92-96 no
   tienen `id` ni `padre` (prueba 20, y `LM.65`). → El paso 3 tiene que **fabricar** el
   registro que va a torcer, con `demo()`, que ya recorre el camino de verdad y cuesta $0,00.
   📌 Eso no es un rodeo: **es el paso 4 asomando.** «Reconstruir una corrida ya grabada» solo
   puede significar **una corrida nueva**, y aquí es donde se estrena.
2. **`padre` no tiene hoy ni un solo lector que lo compruebe.** `arbol()` lo lee para *dibujar*,
   igual que `auditar()` leía `capa` para *imprimir*. Ese es exactamente el defecto que el paso
   1 midió, un campo más allá.

---

##### 4️⃣ LAS CINCO TORCEDURAS, Y LA PREDICCIÓN ES QUE **CUATRO SE CAZAN Y UNA NO**

Un `padre` no se puede torcer de una sola manera. Caben cinco mentiras, y **no son
equivalentes** — esa es la apuesta:

| # | La mentira | ¿se caza? |
|---|---|---|
| 1 | el `padre` apunta a un `id` **que no existe** | **sí** |
| 2 | **ciclo**: el abuelo acaba colgando de su nieto | **sí** |
| 3 | se cambia el `padre` y se deja la **`profundidad` vieja** | **sí** |
| 4 | la línea cuelga de un padre **de otra corrida** | **sí** |
| 5 | una rama se mueve **a su hermana de al lado**, cuadrando todo lo demás | 🚨 **NO** |

**Se apuesta con ~75 %**, y lo que se apuesta es la tabla entera, incluida la última fila.

🚨 **Y la quinta no es una torcedura cualquiera: es, palabra por palabra, la mentira del paso
1.** El gasto del `eur` figurando como del `usd`, con el total sin moverse ni una millonésima.
La diferencia es que ahora se hace en el campo que se escribió **hoy para arreglarlo**.

🔑 **Si la apuesta gana, el titular no es «`padre` funciona».** Es este: **`padre` es
estructura, pero la estructura solo caza las mentiras que rompen la forma.** Mover una rama a
su hermana produce un árbol **perfectamente válido** — no hay nada en el registro que lo
desmienta, porque ese árbol podría haber ocurrido de verdad.

⭐ **Se apuesta también en la dirección incómoda:** si la 5 **sí** se cazara, la apuesta está
fallada y es mejor noticia. Y si alguna de las cuatro primeras **no** se caza, entonces la
obligación del sobre está a medio pagar y hay que decirlo así, no redondear hacia arriba.

---

##### 5️⃣ EL QUE CAZA **NO ES `padre`**, Y ESO ES LO QUE DE VERDAD SE APRENDE HOY

Predicción por separado, y más fina que la anterior. De las cuatro que se cazan:

- las **1 y 2** las caza `padre` **solo** — son integridad del propio campo: apunta a algo que
  no está, o se muerde la cola;
- la **3** solo la caza **`profundidad`**;
- la **4** solo la caza **`corrida`**.

🔑 **O sea: la mitad de la vigilancia no viene de `padre`, viene de tener OTRO campo escrito en
el mismo instante que puede contradecirlo.** `profundidad` y `corrida` no son adornos del
árbol: son **testigos independientes**. El apuntador dice *«mi padre es t5»*; el contador dice
*«yo estoy en el escalón 2»*. Si t5 está en el escalón 7, uno de los dos miente — **y no hace
falta saber cuál para saber que algo se rompió.**

⭐ **Y ahí está la respuesta a por qué `capa` no podía estar mal nunca:** estaba **sola** en su
renglón. Un dato que nadie puede contradecir no es que sea correcto — es que **no es
comprobable**, que es una cosa distinta y mucho peor, porque se parece a la primera.

📌 Es la misma forma que `LM.10` (dos observadores independientes, dos redes, mismo `308`) y la
misma que la prueba 3 de `profundidad.py` (auditar contra un total que se sabe de antemano).
**Aquí se aplica a un campo del registro y no a una medición**, y por eso vale la pena
anotarlo: la regla era más general de lo que parecía.

##### ⚠️ El sospechoso de estar ciego — cuarta sesión seguida nombrándolo

Las dos veces anteriores, nombrarlo lo desarmó. El candidato de hoy es distinto y más difícil:

🚨 **El que elige las cinco torceduras es el mismo que sabe cuáles su auditor puede cazar.**

No hay peligro de que el árbol salga bonito —eso lo cerró el paso 2— sino de que **la lista de
mentiras esté escrita a la medida del detector**. Cuatro de cinco cazadas es un resultado
sospechosamente cómodo si yo elegí las cinco.

→ **La defensa, y se sella como obligación, no como intención:** la torcedura 5 **entra en la
lista con su rojo esperado en blanco**, y su prueba se escribe exigiendo que el auditor **la
deje pasar**. Una prueba que exige que el instrumento **falle** es la única que no se puede
escribir a la medida del instrumento. 🔑 Si mañana alguien enseña a cazar la 5, esa prueba se
pondrá roja y habrá que venir aquí a tacharla — **y eso es exactamente lo que tiene que pasar.**

---

##### 📊 C.1 · PASO 3 — LO QUE SALIÓ, el 2026-08-21. **$0,00 · 28 pruebas · la apuesta 4 sale EXACTA**

`traza.grabar_demo()` · `traza.auditar_arbol()` · las cinco mentiras · `python traza.py --padre`.

**Lo primero, y no estaba en el plan: hubo que FABRICAR el registro que se iba a torcer.**
No existía ninguno con parentesco — los pagados no lo tienen y nunca lo tendrán (`LM.65`).
`grabar_demo()` vuelca una corrida de la demo a `registro_demo_c1.jsonl`: **13 líneas, 13 con
parentesco, $0,00.** 📌 Y con eso se estrenó la forma del paso 4 sin querer: *«reconstruir una
corrida ya grabada»* solo puede significar **una corrida nueva**, y aquí está la primera.

##### 🎯 EL MARCADOR — cuatro de cinco, y la quinta pasa

| # | La mentira | Predicho | Salió | Quién la cazó |
|---|---|---|---|---|
| 1 | padre fantasma | sí | 🚨 **cazada** | `padre` solo |
| 2 | ciclo | sí | 🚨 **cazada** | `ciclo` **y** `profundidad` |
| 3 | escalón viejo | sí | 🚨 **cazada** | **solo `profundidad`** |
| 4 | otra corrida | sí | 🚨 **cazada** | **solo `corrida`** |
| 5 | a la hermana | **no** | 😶 **pasa sin más** | nadie, y no se puede |

✅ **LA OBLIGACIÓN DEL SOBRE QUEDA PAGADA: torcer `padre` pone algo rojo.** `padre` **no** es
el tercer adjetivo del registro. Y se pagó de la única forma que valía: no diciéndolo, sino
con cuatro pruebas que se ponen rojas y **una que exige que el auditor falle**.

---

##### 🥇 HALLAZGO 1 — `padre` es estructura, pero la estructura solo caza lo que rompe la forma

🚨 **La mentira 5 es la del paso 1, palabra por palabra**, hecha en el campo que se escribió
**hoy para arreglar aquello**: el gasto del `eur` pasa a colgar de la rama del `usd`, y el
total no se mueve ni una millonésima. **Y el auditor la deja pasar.**

🔑 **Y hace bien, que es lo incómodo.** El árbol que sale es **perfectamente válido**: el padre
existe, el escalón cuadra, la corrida cuadra, no hay ciclo. No hay nada en el registro que lo
desmienta **porque esa corrida pudo haber ocurrido de verdad**. Un detector que la cazara
estaría inventándose una regla que el mundo no tiene.

> ⭐ **El titular del paso 3 no es «`padre` funciona». Es esto: añadir estructura sube el
> listón de la mentira, no lo cierra.** Antes de `padre`, cualquier mentira pasaba. Ahora
> pasan solo las que producen una corrida que **habría podido pasar**. Eso es una mejora
> enorme y es un techo, y las dos cosas hay que decirlas juntas.

📌 **Lo que esto le hace al hallazgo de la sesión 95:** aquel defecto se cazó viendo *dos líneas
`usd` y ninguna `eur`*. Con el árbol se ve **sin sospechar**, porque la rama `eur` no existe.
Pero si el enrutado hubiera mandado el trabajo del `eur` al worker del `usd` **y el registro lo
hubiera anotado así**, el árbol saldría impecable. 🔑 **El árbol dice fielmente lo que pasó; no
dice si lo que pasó era lo que se pedía.** Para eso hace falta el encargo al lado — que es F.1.

---

##### 🥈 HALLAZGO 2 — la mitad de la vigilancia NO la pone `padre` (apuesta 5, confirmada)

De las cuatro cazadas, **dos las caza `padre` por sí mismo** (el fantasma y el ciclo: son
integridad de su propio campo). Las otras dos, no:

- la **3** —padre real, escalón viejo— **solo la caza `profundidad`**;
- la **4** —hija de otra corrida, con el escalón cuadrado a mano— **solo la caza `corrida`**.

Las dos están escritas en su **versión astuta**: se les reparó a mano todo lo demás que podría
delatarlas, para que solo quedara en pie el testigo que se estaba midiendo.

🔑 **`profundidad` y `corrida` no son adornos del dibujo: son testigos independientes escritos
en el mismo instante.** El apuntador dice *«mi padre es t2»*; el contador dice *«yo estoy en el
escalón 2»*. Si t2 está en el escalón 0, **uno de los dos miente — y no hace falta saber cuál
para saber que algo se rompió.**

> ⭐ **Y de aquí sale, por fin, la respuesta a por qué `capa` no podía estar mal nunca: estaba
> SOLA en su renglón.** Un dato que nadie puede contradecir no es que sea correcto — es que
> **no es comprobable**, que es otra cosa y bastante peor, porque se le parece mucho.
>
> 🔑 La regla general, y vale fuera de este archivo: **un campo se vuelve comprobable el día
> que hay otro que puede desmentirlo.** No cuando se le añade una prueba: cuando se le añade un
> testigo. → `LM.66`.

📌 Es la misma forma que `LM.10` (dos observadores, dos redes, el mismo `308`) y que la prueba 3
de `profundidad.py` (auditar contra un total sabido de antemano). **Aquí se aplica a un campo
del registro y no a una medición**, y por eso valía la pena verlo: la regla era más general de
lo que parecía cuando se aprendió.

---

##### 🥉 HALLAZGO 3 — hay mentiras que un segundo testigo delata SIEMPRE, y no por suerte

La mentira 2 —el ciclo— es **la única de las cinco que no se puede escribir en versión astuta**,
y el motivo es aritmético, no un descuido: **en un ciclo no hay escalones que cuadren.** Alguien
tendría que estar un peldaño por debajo de alguien que está por debajo de él.

Por eso salta **dos veces**: por `ciclo` y por `profundidad`. La prueba 23 exige las dos, y el
motivo de exigir la segunda es que **es la que no se puede esquivar**. 🔑 Un dato redundante no
solo caza mentiras: caza una clase entera de mentiras **por imposibilidad**, no por vigilancia.

⚠️ Y hay una razón práctica además de la bonita: sin el detector de ciclos, `arbol()` entraría
en **recursión infinita** y el síntoma sería un `RecursionError` — un error que no dice nada de
lo que pasó.

---

##### ⚠️ Lo que este auditor NO comprueba, dicho aquí y no escondido en el código

**Que dos líneas con el mismo `id` declaren el mismo padre.** Es integridad de verdad y falta.
Se dejó fuera **a propósito**: ninguna de las cinco torceduras la ejercita, y **un detector que
nunca se ve morder es una nota, no un detector** (`LM.13`). Queda apuntado para el paso 4, con
su torcedura al lado el día que se escriba.

##### 🧾 Lo que el paso 3 dejó

| | |
|---|---|
| `grabar_demo()` | fabrica el registro con parentesco que no existía — 13 líneas, $0,00 |
| `auditar_arbol()` | el lector que `capa` nunca tuvo: 4 quejas, escrito y congelado **antes** de las mentiras |
| Las 5 mentiras | `m1`…`m5`, cada una en su versión más astuta |
| Pruebas | **28 en verde** (21-28 son de hoy), y los otros cinco módulos siguen verdes |
| Registro pagado | **79 + 225 líneas, sin moverse** — prueba 28 y el portero |

📌 **La defensa contra el sospechoso de hoy funcionó, y se puede señalar dónde:** la prueba 26
exige que el auditor **deje pasar** la mentira 5. Es la única de las 28 que **no se puede
escribir a la medida del instrumento**, porque pide que el instrumento falle. Si mañana alguien
enseña a cazar la 5, esa prueba se pone roja y hay que volver aquí a tacharla.

➡️ **Lo que esto le cambia al paso 4, antes de escribirlo:** el árbol ya es fiable como
**relato de lo que pasó**, y queda medido que **no** es un juez de si lo que pasó era lo
correcto. El paso 4 —el árbol de una corrida nueva— hereda las dos cosas.

---

#### 🎲 C.1 · PASO 4 — LA APUESTA, sellada el **2026-08-21** (sesión 97) **antes de correr nada**

> ⚠️ Se escribe y se **commitea antes** de gastar el primer centavo. Sexta seguida.

##### 🔴 Y lo primero es una apuesta PERDIDA, que se anota antes que nada

**LA APUESTA 2 —«C.1 CUESTA $0,00»— ESTÁ FALLADA.** El paso 4 exige pagar, y no hay forma
honesta de esquivarlo:

La demo recorre el camino de verdad en su tramo de en medio —`reparto_en_paralelo`,
`ejecutar_un_bloque`, los dos `anotar`— pero **sus workers son falsos**. Nunca se han ejecutado
`correr_orquestador` ni `correr_worker`: los bucles de agente de verdad, donde el modelo decide
qué herramienta llamar. Y el paso 4 es, literalmente, *«el árbol de una corrida de verdad»*.
🔑 **Un árbol dibujado sobre un camino de mentira mide al camino de mentira** — está escrito en
el docstring de `demo()` desde el paso 2, y aplicarlo aquí obliga a pagar.

⭐ **Se anota como fallada y NO se redefine** (`LM.21`), y lo que importa es el modo de fallo,
que estaba predicho palabra por palabra en la propia apuesta 2:

> *«Si al final hace falta una corrida nueva para validar el parentesco de punta a punta, está
> fallada — y entonces la quinta estimación seguida no habrá sido inflada sino corta, que es un
> vicio nuevo y también cuenta.»*

🔑 **Cinco sesiones estimando de más, y la sexta se queda corta.** El error no fue el número:
fue **contar el coste de lo que se iba a escribir y no el de lo que haría falta para creérselo.**
Los pasos 1, 2 y 3 costaron $0,00 de verdad. El que cuesta es el que **valida** los otros tres.

##### 💰 Lo que cuesta, MEDIDO y no estimado

`python fan_out.py --paralelo` es el único camino real de dos capas. Medido en la sesión 93:
**$0,026984 · 8,91 s · 11 llamadas a la API.** El coste ha variado **menos del 3 %** entre
corridas (la 91 lo midió), así que la horquilla honesta es **$0,024 – $0,030**.

---

##### ⚠️ El sospechoso de estar ciego — quinta sesión seguida nombrándolo, y este da más miedo

🚨 **La demo y la corrida real comparten casi todo el camino, así que voy a mirar el árbol de
verdad buscando confirmar la forma que ya vi.**

Los cuatro anteriores eran instrumentos ciegos. Este no: **este es sesgo de confirmación sobre
un dibujo.** Un árbol de once llamadas es lo bastante bonito como para asentir con la cabeza, y
«se ve bien» no es una medición. La defensa no puede ser *mirar con cuidado*.

→ **La defensa, y se sella como obligación, no como intención: la forma esperada se escribe
AQUÍ, con números, y se comprueba a máquina.** Seis afirmaciones, cada una falsable por
separado:

| # | Lo que tiene que salir | Falla si… |
|---|---|---|
| 1 | **exactamente 1 raíz**, profundidad máxima **2** | hay huérfanos, o una capa de más |
| 2 | **3 tramos `tool:consultar_moneda` con `propio $0,000000`** | alguno gasta por su cuenta |
| 3 | **3 tramos `worker:*` con `propio > 0`** | un worker no paga nada |
| 4 | `auditar_arbol()` → **cero quejas** sobre un registro que nadie torció | grita sin mentira |
| 5 | 🔑 **la suma del árbol == el total de la factura de `auditar()`** | dos caminos, un número, y no cuadran |
| 6 | **al menos un tramo con varias `llamada_api` dentro** (el bucle del agente) | la corrida real se parece a la demo más de lo esperado |

🔑 **La 5 es la que de verdad se apuesta, y es `LM.66` aplicado a sí mismo.** El árbol suma
hacia arriba desde `padre`; `auditar()` suma en plano sin mirar el parentesco. **Son dos caminos
independientes hasta el mismo número.** Si no cuadran, uno de los dos miente y ese es el
hallazgo del día — mejor que cualquier árbol bonito.

📌 **La 6 está puesta para poder fallar sola.** La demo tenía una `llamada_api` por worker
porque yo la escribí así; un agente de verdad puede dar varias vueltas. Si la corrida real sale
idéntica en forma a la demo, **eso es sospechoso, no tranquilizador**.

##### ❌ Lo que NO se apuesta

**Que el árbol salga limpio a la primera.** La corrida real pisa dos funciones que ningún árbol
ha visto nunca. Si sale torcido, el paso 4 no ha fracasado: **ha hecho su trabajo**, que es la
primera vez que este parentesco se mira fuera del laboratorio.

---

##### 📊 C.1 · PASO 4 — LO QUE SALIÓ, el 2026-08-21. **$0,026390 · las 6 afirmaciones cumplidas · y un hallazgo BLOQUEANTE que ninguna miraba**

`python fan_out.py --paralelo` (pagado, una vez) · `python traza.py --paso4` (gratis, repetible).

**El coste, contra la horquilla sellada:** $0,026390 · 11 llamadas · 8,34 s. Se apostó
**$0,024 – $0,030**. Dentro, y la horquilla venía de un dato medido, no de una intuición.

##### ✅ Las seis afirmaciones del sobre, cumplidas

```
capa:orquestador       t2   total $0.026390   propio $0.004604
   tool:consultar_moneda  t5   total $0.007289   propio $0.000000
      worker:eur          t6   total $0.007289   propio $0.007289
   tool:consultar_moneda  t7   total $0.007257   propio $0.000000
      worker:cad          t8   total $0.007257   propio $0.007257
   tool:consultar_moneda  t3   total $0.007240   propio $0.000000
      worker:usd          t4   total $0.007240   propio $0.007240
```

| # | Lo que se pedía | Lo que salió |
|---|---|---|
| 1 | 1 raíz, profundidad máx. 2 | ✅ `[('c1','t2')]`, prof. 2 |
| 2 | 3 tramos `tool:` con propio $0,000000 | ✅ los tres a cero |
| 3 | 3 tramos `worker:` con propio > 0 | ✅ 0,007240 · 0,007289 · 0,007257 |
| 4 | cero quejas del auditor | ✅ `[]` |
| 5 | 🔑 la suma del árbol == la factura plana | ✅ **$0,026390 == $0,026390** |
| 6 | algún tramo con varias `llamada_api` | ✅ orquestador 2 · cada worker 3 |

🔑 **La 5 es la que valía, y cuadró.** El árbol suma **hacia arriba desde `padre`**; `auditar()`
suma **en plano y sin mirar el parentesco**. Dos caminos independientes hasta el mismo número.
Es `LM.66` aplicado al propio instrumento, y esta vez el segundo testigo confirmó en vez de
desmentir — que es el otro trabajo de un testigo.

📌 **La 6 tenía permiso para fallar sola y no falló:** el agente de verdad da **tres vueltas por
worker** donde la demo daba una. El árbol lo absorbió sin cambiar de forma, y eso responde algo
que la demo no podía: **el parentesco no depende de cuántas veces hable el modelo.**

---

##### 🚨 EL HALLAZGO DEL DÍA — y es lo que las seis afirmaciones NO miraban

> **Importancia: alta · Urgencia: BLOQUEANTE.**
> **Qué bloquea y qué se rompe:** bloquea el **paso 5**. Al correr `fan_out.py --paralelo` una
> segunda vez, el árbol declara que **una sola corrida costó el doble**, sin una queja. Y el
> paso 5 consiste exactamente en comparar ramas de corridas distintas.

**El identificador de corrida no era único.** El contador de `contexto.py` vive en el proceso, y
al arrancar Python vuelve a 1:

```
proceso A -> c1
proceso B -> c1
```

Las dos corridas se llaman `c1` **y sus tramos se llaman `t2`…`t8`, los mismos**. No es que se
parezcan: son **indistinguibles**. Medido, con las líneas reales duplicadas:

```
capa:orquestador   t2   total $0.052780   propio $0.009208     ← dos corridas de $0,026390
quejas del auditor: []
```

⭐ **Es la SEXTA mentira, y es la primera que no escribí yo.** Las cinco del paso 3 las inventé;
esta **la escribe el harness solo**, cada vez que se corre dos veces. 🔑 Y no se parece a la
quinta: **la quinta pasa porque describe un mundo posible; esta describía un mundo que no
ocurrió.**

##### 💀 Y lo que de verdad duele: el comentario que lo justificaba nombró el riesgo equivocado

Esto estaba en `contexto.py`, escrito **esa misma mañana**:

> *«Se prefiere a un `uuid` a propósito: los ids salen cortos y en orden … este archivo no sale
> de una máquina.»*

**El razonamiento nombró el riesgo que asumía —irse a otra máquina— y se equivocó en cuál era.**
El peligro nunca fue otra máquina: era **el mismo archivo, mañana**. 🔑 Un «a propósito» escrito
en un comentario **se lee como si alguien lo hubiera medido**, y aquí no se había medido nada.
→ `LM.67`.

📌 **Y es el bicho de esta misma mañana por tercera vez en un día.** `corrida` se añadió en el
paso 2 para cerrarlo, y el README lo llamó *«cerrado por diseño»*. Estaba cerrado **a medias**:
separaba una corrida de las de otro día, no de la de mañana.

##### 🔧 Cómo se mató — en el origen, y son DOS arreglos porque son DOS fallos

| | |
|---|---|
| **El que escribe** | `contexto._corrida_nueva()` — fecha legible + 6 caracteres de azar. Los **tramos siguen con contador**: solo tienen que ser únicos dentro de su corrida. |
| **El que lee** | `arbol()` y `auditar_arbol()` indexan por **`(corrida, id)`**, no por `id`. Aunque mañana llegue un registro con ids repetidos, no se funden. |

🔑 **Hacían falta los dos, y saber por qué separa un parche de un arreglo.** Arreglar solo al que
escribe deja ciego al lector ante todos los registros **ya grabados**; arreglar solo al lector
deja el archivo lleno de nombres repetidos. Es la sesión 49 de TEAPP otra vez: **origen y
portero**.

##### 🎁 Un regalo del arreglo, y va en contra de la intuición

Al pasar la clave a `(corrida, id)`, **la comprobación de `corrida` del auditor se quedó sin
forma de dispararse**: padre e hijo son de la misma corrida por construcción. Un detector
correcto quedó **muerto por un arreglo correcto**.

🚨 **Y no lo vi yo: lo cazó la prueba 25 poniéndose roja en el acto.** El caso no desapareció —
subió un nivel, donde ahora se distinguen dos cosas que antes eran una: *«tu padre se perdió»* y
*«tu padre es de otra corrida»*. **El diagnóstico salió mejor que antes del arreglo.**

⚠️ **Y esto obliga a corregir un número del paso 3, aquí y no en silencio:** se escribió que *«de
las cuatro cazadas, dos las caza `padre` solo y dos necesitan un segundo testigo»*. Con la clave
arreglada, **`corrida` dejó de ser un testigo y pasó a ser parte de la identidad.** El único
segundo testigo que queda es **`profundidad`**. `LM.66` no cambia —sigue haciendo falta un campo
que pueda desmentir— pero **el recuento sí, y era mío.**

##### 🧾 Lo que el paso 4 dejó

| | |
|---|---|
| Pagado | **$0,026390**, una sola corrida, dentro de la horquilla |
| `comprobar_forma()` | las 6 afirmaciones a máquina, **commiteada antes de pagar** (`f2c30f4`) |
| Arreglos | `_corrida_nueva()` en el que escribe · clave `(corrida, id)` en el que lee |
| Pruebas | **31 en verde** (29, 30 y 31 son del arreglo), y los otros cinco módulos verdes |
| Reescritas | la **20** (se puso roja porque ya HAY una corrida pagada con parentesco) y la **18** |

📌 **La defensa contra el sospechoso se puede señalar, y esta vez sirvió de verdad.** El sobre
avisó: *«voy a mirar el árbol buscando confirmar la forma que ya vi»*. Y eso es exactamente lo
que habría pasado: **las seis salieron verdes a la primera.** Lo que encontró el fallo no fue
mirar el dibujo — fue que el dibujo decía `c1` y `c1` es un nombre demasiado corto para ser
único. 🔑 **Una lista de comprobaciones que se cumple entera no dice que no haya nada roto: dice
que no hay nada roto EN LA LISTA.**

➡️ **Lo que esto le cambia al paso 5:** estaba bloqueado y ya no lo está. Y hereda una pieza que
no existía esta mañana: **dos corridas se pueden comparar en el mismo archivo sin mezclarse**,
que es justo lo que el paso 5 necesita para llevarle el árbol al defecto de la sesión 95.

---

#### 🎲 C.1 · PASO 5 — LA APUESTA, sellada el **2026-08-21** (sesión 97) **antes de la primera línea**

> ⚠️ Séptima seguida. Y esta se sella **después de leer código pero antes de escribirlo**, así
> que lo leído va aparte, abajo, y **no cuenta como apuesta**.

##### 📏 LO QUE SE CONTÓ ANTES DE APOSTAR — tres hechos, $0,00, y ninguno es una predicción

**1. El defecto de la sesión 95 NO era un enrutado torcido.** El README de B.5 lo dice con todas
las letras: *«No hubo enrutado equivocado.»* La inyección torcía `nombre=`, el encargo seguía
diciendo `400 EUR`, y **el worker hizo el trabajo bien**. Lo que se cazó fue *dos líneas `usd` y
ninguna `eur`*: **un síntoma con dos causas posibles**, y hubo que leer el encargo **a mano**
para saber cuál era.

**2. El árbol bautiza sus nodos con ese MISMO campo.** `worker.py:299`:

```python
@contexto.envuelto("nombre", prefijo="worker:")
def correr_worker(encargo, nombre="divisa", ...):
```

`nombre` es exactamente el argumento que la inyección de la 95 torcía, y exactamente el campo
que el **paso 1** midió como adjetivo.

**3. La estructura del árbol nunca estuvo en duda aquel día.** Hubo dos encargos y se hicieron
dos trabajos: el árbol diría *«dos ramas»* y **acertaría**. Lo que mentía eran los **nombres**.

---

##### 7️⃣ LA APUESTA 1 SE VA A CAER POR SU SEGUNDA MITAD, Y POR LO QUE EL PASO 3 PREDIJO

La apuesta 1 decía: *«el árbol no cambiará ninguna conclusión ya pagada del bloque B — pero
habría abaratado la de la sesión 95»*.

**Predicción concreta y falsable: la primera mitad se sostiene y la segunda falla. ~85 %.**
Replicar la inyección de la 95 con el árbol encendido dará **dos ramas `worker:usd` y ninguna
`eur`** — el mismo síntoma ambiguo, las mismas dos causas, el mismo trabajo a mano. El árbol
**no** habría abaratado nada.

🔑 **Y el motivo es `LM.66` mordiendo donde no lo esperaba: un árbol cuyos nodos se bautizan con
un adjetivo hereda la mentira del adjetivo.** El paso 2 dejó escrito que `tramo` *«es una
etiqueta, de la misma clase que `capa`»* — y se incluyó igual porque sin nombre legible el árbol
no se lee. **Aquí se cobra esa decisión:** el árbol es honesto en su forma y mentiroso en sus
rótulos, y lo que un humano mira primero son los rótulos.

⭐ **Se apuesta en la dirección incómoda a propósito.** Ganar esta apuesta significa **perder la
apuesta 1**, que es mía y del bloque C. Si el árbol **sí** cazara la 95 sin ayuda, la apuesta 1
se paga y esta se falla — y sería mejor noticia.

##### 8️⃣ Y LA PARTE CONSTRUCTIVA: UN TERCER TESTIGO CIERRA LA AMBIGÜEDAD DE LA 95

Si el tramo del worker se bautizara con **lo que el worker hizo** —la moneda del contrato, que
es un dato— en vez de con **lo que alguien dijo que era** —`nombre=`, que es un adjetivo—, torcer
la etiqueta produciría un nodo `worker:usd` **cuyo contrato dice `EUR`**. Contradicción, y roja.

**Predicción: con ese testigo, el síntoma de la 95 deja de tener dos causas. ~75 %.** El harness
podría por fin distinguir *«el enrutado está torcido»* de *«solo la etiqueta miente»*, que es
literalmente la pregunta que el paso 1 declaró sin dueño.

⚠️ **Lo que puede salir mal, y se dice antes:** puede que el contrato **no** esté disponible en
el momento de abrir el tramo —el tramo se abre al entrar en la función y el contrato existe al
salir—. Si es así, el testigo **no se puede poner donde hace falta**, y eso es un hallazgo sobre
`envuelto` y no una excusa. Se anotaría como fallada.

##### 💰 Coste apostado: **$0,00**

La inyección de etiqueta es determinista y no necesita modelo; el cebo ya está pagado desde la
sesión 94. ⚠️ **Y la lección del paso 4 se aplica aquí:** si a mitad de camino hiciera falta
pagar para creérselo, **se para y se dice antes de gastar**, no después.

##### ⚠️ El sospechoso de estar ciego — sexta sesión seguida

🚨 **Estoy a punto de reproducir un defecto usando la MISMA inyección que lo produjo, y el que
decide qué se inyecta es el que ya sabe qué va a salir.**

Es el bicho del cebo de B.4 (*«un cebo demasiado fácil mide al cebo, no al cazador»*) con una
vuelta más: aquí el cebo **ya existe**, grabado en `cebo_mal_enrutado_*.json`, producido por un
worker real en la sesión 94.

→ **La defensa, sellada como obligación:** la reproducción se hace **con el cebo grabado**, no
con uno nuevo redactado hoy, y el nodo torcido se compara contra **el contrato que ese cebo ya
trae dentro** (`moneda: USD`, `monto: 400`), que nadie puede retocar sin que se vea en el
`git diff`.

---

##### 📊 C.1 · PASO 5 — LO QUE SALIÓ, el 2026-08-21. **$0,00 · 36 pruebas · la apuesta 1 se parte por la mitad, y el hallazgo es MEJOR que la apuesta**

`traza.auditar_etiquetas()` · `python traza.py --paso5`. No se llamó a la API.

##### 🅰️ EL VEREDICTO DE LA APUESTA 1 — primera mitad PAGADA, segunda mitad FALLADA

La apuesta 1 decía: *«el árbol no cambiará ninguna conclusión ya pagada del bloque B — pero
habría abaratado la de la sesión 95»*.

| mitad | veredicto |
|---|---|
| *«no cambia ninguna conclusión ya pagada»* | ✅ **se paga** — ninguna cifra del bloque B se movió |
| *«habría abaratado la caza de la 95»* | ❌ **FALLADA** |

🚨 **Y está demostrado en código, no en prosa** (prueba 36). El mismo encargo, `«Convierte 400
EUR a pesos»`, pasado por el decorador **real** del worker:

```
nombre="eur"  →  tramo «worker:eur»
nombre="usd"  →  tramo «worker:usd»      ← el mismo trabajo, otro rótulo
```

🔑 **El árbol bautiza sus nodos con `envuelto("nombre")`, que es EXACTAMENTE el argumento que la
inyección de la 95 torcía.** Un árbol dibujado sobre aquella corrida habría enseñado **dos ramas
`worker:usd` y ninguna `eur`** — el mismo síntoma ambiguo, las mismas dos causas, el mismo
trabajo a mano.

⭐ **Un árbol cuyos nodos se bautizan con un adjetivo hereda la mentira del adjetivo.** El paso 2
dejó escrito que `tramo` *«es una etiqueta, de la misma clase que `capa`»*, y se incluyó igual
porque sin nombre legible el árbol no se lee. **Aquí se cobró esa decisión:** el árbol es honesto
en su **forma** y mentiroso en sus **rótulos** — y lo que un humano mira primero son los rótulos.

---

##### 🥇 Y EL HALLAZGO DEL PASO 5 ES OTRO, Y ES MEJOR: EL TERCER TESTIGO YA ESTABA GRABADO

Se sellaba *«habría que añadir un tercer testigo»*. **No hubo que añadir nada.** Cada línea
`worker_fin` lleva desde la **sesión 93** dos cosas que hablan de la misma moneda por caminos que
no se pueden coordinar:

- **`worker` / `tramo`** → *el adjetivo*: cómo se llamó a quien trabajó. Sale de `nombre=`.
- **`datos.moneda`** → *el hecho*: qué moneda salió del contrato de A.3, producida por la
  herramienta que hizo la cuenta.

Y esto es lo que salió al preguntarles, sobre el registro **pagado**, sin correr nada:

```
Líneas `worker_fin` comprobadas ..... 23
No comprobables (y se dice) ......... 15
🚨 Contradicciones .................. 1

  2026-08-20T20:32:23+00:00
    se llama ....... worker «usd»
    pero hizo ...... EUR
    encargo ........ Convierte 400 EUR a pesos colombianos.
```

🚨 **Esa línea es la sesión 95. No es una reproducción, no es un cebo nuevo: es la línea que se
escribió el 20 de agosto a las 20:32:23, que costó dinero, y que lleva en el repositorio desde
entonces.** La contradicción estuvo ahí todo el tiempo, y era comprobable **por una máquina, en
un segundo, gratis**.

> ⭐ **Lo que faltaba no era un campo. Era un lector.** → `LM.68`.
>
> 🔑 Y eso le pone precio a la sesión 95: aquel día se leyó el encargo **a mano** para decidir
> cuál de las dos causas era. El registro ya contenía la respuesta.

📌 **Y las 22 líneas sanas pasaron limpias** (prueba 33). Eso es lo que separa un auditor de un
detector escrito para encontrar la línea que ya habías visto — el sospechoso que el sobre nombró.
📌 **Las 15 no comprobables se declaran como tales**, no como verdes (prueba 35): son líneas sin
contrato —los workers del pipeline, que devuelven prosa—. **Un auditor que calla lo que no sabe
mirar miente por omisión.**

##### 🧾 Lo que el paso 5 dejó, y qué le hace al paso 1

| | |
|---|---|
| `auditar_etiquetas()` | el adjetivo contra el hecho, sobre cualquier registro ya grabado |
| Coste | **$0,00** — la apuesta de coste del paso 5 se cumple |
| Pruebas | **36 en verde** (32-36 son de hoy), los cinco módulos verdes |
| Apuesta 1 | mitad pagada, mitad fallada, **con la prueba 36 como veredicto** |

⭐ **Y cierra el agujero que el paso 1 dejó sin dueño.** El paso 1 midió que el síntoma *«dos
líneas `usd` y ninguna `eur`»* tiene **dos causas posibles** —enrutado torcido o etiqueta
mentirosa— y que *«el harness no sabe distinguirlas»*. **Ya sabe.** Si el contrato dice EUR bajo
un worker llamado `usd`, es la etiqueta; si el contrato dice USD y el encargo pedía euros, es el
enrutado. 🔑 Y no hizo falta instrumentar más: **hizo falta cruzar dos campos que ya estaban.**

➡️ **Lo que queda de C.1:** nada. Los cinco pasos están hechos. Lo que sigue abierto y con dueño
es el detector de un mismo `id` con dos padres distintos, que **entra con su torcedura al lado o
no entra** (`LM.13`).

---

#### 🎲 C.2 — LA APUESTA, sellada el **2026-08-21** (sesión 98) **antes de la primera línea de código**

> **El estudiante:** eligió el **candidato 2 — bolsa común repartida a la entrada** entre tres
> esquemas propuestos, y *«voy con el sello de tu apuesta»*. Se sella la de esta terminal.
> Lo que se cuenta abajo se contó **antes** de escribir las apuestas, sobre los registros que
> ya estaban pagados: es $0,00 y no contamina lo apostado.

##### 📏 LO QUE SE CONTÓ ANTES DE APOSTAR — $0,00, y no era una apuesta

**1. C.2 no arranca de cero: está MEDIO CONSTRUIDO desde el bloque A, y el propio código lo
dice.** En `orquestador.py:109`, escrito en la sesión 91: *«⭐ **Y esto ya es media pieza
C.2**: en dos capas no hay "un" presupuesto. Hay uno por capa»*. Existe
`PRESUPUESTO_ORQ_USD = 0.05`, existe `PRESUPUESTO_WORKER_USD = 0.05`, existe una excepción
`PresupuestoAgotado` **en las dos capas**, y existe un `motivo="presupuesto"` que sale en el
informe de cierre. **El esquema de hoy es el candidato 1, y lleva siete sesiones puesto.**

**2. Y NUNCA HA MORDIDO. Ni una vez.** Sobre los seis registros pagados del nivel:

| registro | cierres | `motivo="presupuesto"` | `motivo="max_vueltas"` |
|---|---:|---:|---:|
| workers | 38 | **0** | 0 |
| orquestador | 14 | **0** | 0 |
| línea base · pipeline · router · supervisor | 13 | **0** | 0 |
| **total** | **65** | **0** | **0** |

🔑 **65 cierres pagados y el campo `motivo` vale `None` en los 65.** Es `LM.13` con el número
delante: no es que el freno esté mal — es que **nadie lo ha visto morder**, así que es una
nota.

**3. Y no podía morder, porque el tope está fuera de alcance.** `acumulado_usd` es lo que el
freno vigila de verdad. El máximo jamás alcanzado en todo el nivel:

| capa | tope puesto | máximo real alcanzado | veces cubierto |
|---|---:|---:|---:|
| worker (monedas) | $0,05 | $0,007960 | **6,3×** |
| worker (cualquiera) | $0,05 | $0,010568 | **4,7×** |
| orquestador | $0,05 | $0,005233 | **9,6×** |

Es el patrón de la sesión 74 de TEAPP — *«el presupuesto va 112 veces cubierto y mudo»*—
repetido aquí sin que nadie lo trajera.

**4. El total no está acotado por nada, y nadie decidió el número que sale.** Tres workers y
un orquestador a $0,05 cada uno son **$0,20 de techo**. La corrida real del paso 4 costó
**$0,026390**. 🔑 **El que paga la factura no puede nombrar su límite**, porque no existe un
límite del encargo: solo existen los límites de las piezas, y el techo sale de multiplicar.

**5. 🚨 Y AQUÍ SE MURIÓ UNA APUESTA ANTES DE ESCRIBIRLA.** Iba a apostar que el reparto ciego
a tercios **desperdicia** —un worker se para mientras sobra dinero en el trozo del vecino—.
Se contó, y en esta tarea **no desperdicia casi nada**. Las cinco corridas con los tres
workers de moneda:

| corrida | usd | eur | cad | dispersión |
|---|---:|---:|---:|---:|
| 2026-08-20T14:58 | 0,007199 | 0,007267 | 0,007181 | **1,01×** |
| 2026-08-20T15:03 | 0,007219 | 0,007231 | 0,007196 | **1,00×** |
| 2026-08-20T19:21 | 0,007315 | 0,007200 | 0,007236 | **1,02×** |
| 2026-08-21 (`c1`) | 0,007240 | 0,007289 | 0,007257 | **1,01×** |

⭐ **Los tres workers cuestan lo mismo hasta la tercera cifra.** El reparto a tercios no es un
compromiso en esta tarea: es **casi óptimo**. 🔑 **Y eso NO absuelve al candidato 2 — dice que
la tarea del duelo no puede medir su defecto.** Tres encargos gemelos hacen que *todos* los
repartos se parezcan. **Una tarea que no puede distinguir dos esquemas no es una tarea fácil:
es un instrumento ciego**, y esta vez se vio antes de pagar.

##### 🎯 QUÉ MIDE C.2, entonces

Ya no es *«construir un presupuesto»*: eso está construido y mudo. Es **pasar del tope por
pieza al presupuesto DEL ENCARGO repartido a la entrada, y verlo morder** — con el criterio de
éxito puesto no en que corte, sino en **qué queda encima de la mesa cuando corta**.

---

**1️⃣ CUANDO EL FRENO MUERDA, EL ENCARGO NO FALLARÁ: VOLVERÁ A MEDIAS. Se apuesta con ~75 %.**

Predicción concreta y falsable: con un presupuesto de encargo repartido en tres trozos por
debajo de lo que un worker gasta, **al menos un worker cerrará con `motivo="presupuesto"`, el
orquestador NO reventará, y entregará una respuesta con las monedas que sí llegaron.**

⚠️ **Y lo que de verdad se mide es la línea siguiente: ¿la respuesta AVISA de que está
incompleta?** El system prompt del orquestador dice *«si un especialista no te dio el dato, di
que esa moneda no se pudo consultar»* — o sea, **hay una instrucción escrita que debería
salvarlo, y nunca se ha ejercitado**. Se apuesta a que **sí avisa** (esa frase se escribió
para esto), y si no aviso, el hallazgo es mucho peor que el freno: es una respuesta
**parcial disfrazada de completa**, que es la forma más cara de fallar de un agente.

**2️⃣ EL REPARTO A TERCIOS NO SE PODRÁ DISTINGUIR DEL TOPE POR PIEZA EN ESTA TAREA, y por eso
hace falta un encargo DESIGUAL. Se apuesta con ~85 %, y es una apuesta contra mí mismo.**

Ya está contado arriba: dispersión 1,00×–1,02×. Con encargos gemelos, el candidato 1 y el
candidato 2 dan **el mismo resultado**, y elegir entre ellos sería una preferencia estética.
🔑 **Para que la diferencia exista tiene que haber un worker que necesite más que su trozo
mientras a otro le sobra** — y en la tarea del duelo eso no ocurre nunca.

📌 **Se apuesta a que la diferencia aparece si un worker recibe trabajo más pesado**, y **eso
es una obligación sellada, no una intención**: C.2 no se da por hecha sin una corrida con
encargos desiguales. Si no se puede construir, se **tacha con la razón escrita** (regla del
nivel) y C.2 admite que midió el freno pero no el reparto.

**3️⃣ EL TOTAL DEL ENCARGO SERÁ UN NÚMERO DECIDIDO, Y AL SUMARLO DARÁ MENOS QUE EL TECHO DE
HOY.** Falsable en una línea: hoy el techo son **$0,20** y nadie lo eligió; al cerrar C.2
tiene que existir **una sola constante** que se pueda leer en voz alta como *«este encargo no
puede costar más de X»*, con X **medido** contra los $0,026390 de la corrida real, no
inventado.

##### ⚠️ El sospechoso de estar ciego, nombrado antes de escribirlo

Van **cinco sesiones** nombrándolo, y las cinco lo desarmaron. El candidato de hoy:

🚨 **El que elige el número del presupuesto es el mismo que ya sabe lo que cuesta una
corrida.**

Acabo de contar que un worker gasta $0,0073. Si ahora pongo el tope en $0,005, **el freno va a
morder — y no habrá medido nada, porque lo afiné para que mordiera.** Un freno ajustado
contra el dato que ya tenía delante es una **demostración**, no una medición. Es el mismo
bicho que el árbol dibujado por quien conocía el parentesco (C.1) y el cebo redactado por
quien monta el experimento (B.4).

→ **La defensa, y se sella como obligación, no como intención — son DOS y hacen falta las
dos:**

1. **El número sale de una REGLA escrita antes de mirar**, no de un dedo: el presupuesto del
   encargo se calcula como una fracción declarada del coste medido, y **la fracción se escribe
   en el código con su motivo** antes de correr nada.
2. **Tiene que existir una prueba que exija que el freno NO muerda con un presupuesto normal.**
   🔑 Es la única que **no se puede escribir a la medida del instrumento, porque pide que el
   instrumento se calle** — el papel que en C.1 hizo la prueba 26. Un freno que muerde siempre
   es tan inútil como uno que no muerde nunca, y **solo la segunda mitad se estaba vigilando**.

---

##### 📊 C.2 — LO QUE SALIÓ, el 2026-08-21. **$0,045113 · 15 pruebas gratis + 2 corridas pagadas**

`presupuesto.py` · las once afirmaciones estaban commiteadas **antes** de lanzar nada
(`f770838`), y **dos salieron rojas**. Las dos rojas son el día entero.

**La corrida NORMAL: 5 de 5 cumplidas.** El freno **se calló**, que era la obligación sellada
por la mañana. Ningún worker cortó, el orquestador tampoco, las tres monedas salieron con su
fuente y su fecha, y el total fue **$0,026725 contra un techo de $0,039585** — margen
$0,012860. 🔑 **Y esto es lo que convierte `P1` de aritmética en hecho:** hasta hoy *«no
muerde en operación normal»* era una comparación de constantes.

**La corrida APRETADA: el freno mordió a los tres, y el resultado fue peor de lo apostado.**

| | |
|---|---|
| workers cortados | **3 de 3**, todos por `motivo="presupuesto"` |
| dónde cayó el corte | tras la **2ª** llamada, con `tasa` y `convertir` **ya ejecutadas** |
| monedas entregadas | **cero** |
| gasto | **$0,018388** contra un techo de **$0,014424** |

---

**🚨 HALLAZGO 1 — EL TECHO NO ERA UN TECHO. Se pasó un 27,5 % y el harness lo dijo solo.**
**Importancia: alta · Urgencia: no bloqueante** (nada se rompe hoy; C.2 no se puede cerrar sin
esto).

`dentro_del_presupuesto` salió **`False`**, y esa afirmación —la 3— estaba escrita antes de
correr. El mecanismo es de una línea y estaba a la vista desde el bloque A:

```python
if gastado_usd >= presupuesto_usd:      # se comprueba ANTES de llamar
    raise PresupuestoAgotado(...)       # pero no se sabe cuánto costará la llamada
```

⭐ **Un freno que autoriza sin saber el precio sólo puede acotar el gasto en
`techo + N × coste_de_una_llamada`.** Aquí los cuatro participantes se pasaron: cada worker
llevaba $0,00484 con un trozo de $0,003606, y el orquestador $0,003936 con una reserva de
$0,003606. **Cuatro de cuatro.**

🔑 **Y aquí está lo que más enseña, porque me lo comí al elegir el esquema.** En este mismo
archivo escribí que el defecto del **candidato 3** (bolsa común) era *«hay que ESTIMAR lo que
va a costar una llamada antes de hacerla»*, y lo usé como motivo para descartarlo.
**El candidato 2 tiene exactamente el mismo problema — sólo que lo escondía.** Repartir a la
entrada no libra de estimar: aplaza la estimación al momento de autorizar, donde no se ve.
⚠️ **Descarté un esquema por un defecto que el elegido también tenía, y no lo vi hasta pagar.**

---

**🚨 HALLAZGO 2, Y ES EL MAYOR — EL WORKER TENÍA LA RESPUESTA Y MURIÓ ANTES DE PODER DECIRLA.**

Los tres cortados habían ejecutado **`tasa` y `convertir`**. La tasa estaba consultada, la
cifra en pesos calculada, el dato **dentro del harness**. El corte cayó en la llamada que
sólo servía para **redactar** lo que ya se sabía.

⭐ **El corte no ahorró el trabajo: lo pagó y lo tiró.** $0,014452 gastados abajo compraron
tres datos correctos que nadie llegó a leer, porque el contrato de A.3 se llena con lo que el
worker **dice**, no con lo que el harness **tiene**.

🔑 **De aquí sale la pregunta que C.2 no sabía que tenía que hacerse:** un presupuesto no sólo
decide *cuánto*, decide **dónde puede caer el corte** — y hay sitios donde cortar convierte
todo lo ya pagado en cero. Cortar antes de empezar cuesta $0. Cortar al final cuesta todo.
**El peor momento posible para quedarse sin dinero es el penúltimo paso.**

---

**🅰️ LA APUESTA 1 DEL SOBRE: FALLADA en su predicción central, y el motivo estaba MEDIDO ESA
MISMA MAÑANA.**

Se apostó *«volverá a medias, con las monedas que sí llegaron»*. **Volvió vacía: cero
monedas.** Y no fue mala suerte:

> por la mañana se contó que los tres workers de moneda cuestan lo mismo hasta la tercera
> cifra (dispersión **1,00×–1,02×**), y se usó ese dato para decir que el reparto ciego era
> casi óptimo.

⭐ **El mismo dato predecía esto y no lo leí en esa dirección: workers idénticos + trozos
iguales = mueren todos en el mismo sitio.** Un reparto ciego y simétrico sobre tareas gemelas
**no produce resultados parciales — produce todo o nada.** El dato estaba contado, escrito y
commiteado, y le hice una sola pregunta de las dos que respondía. Es `LM.68` otra vez: **lo
que faltaba no era un dato, era un lector.**

📌 Y la mitad de la apuesta que **sí** se paga: el orquestador **no reventó** (377 caracteres
de respuesta) y **avisó** de que no había datos, en vez de inventarse tres cifras. La frase
*«no tienes forma de averiguar tasas por tu cuenta»* del system prompt se ganó el sueldo por
primera vez.

---

**⚠️ LA AFIRMACIÓN 6 DIO UN FALSO ROJO, Y ESTABA DECLARADA DÉBIL ANTES DE CORRER.**

El indicio buscaba palabras como *«no se pudo»* y no encontró ninguna. La respuesta real
decía: *«no puedo completar tu solicitud… no logró consultar ninguna de las tres monedas»*.
**Avisa perfectamente, con otras palabras.** 🔑 Que estuviera marcada como **indicio y no como
veredicto antes de pagar** es lo que hizo que el rojo costara diez segundos en vez de una
discusión: **declarar débil un instrumento por adelantado es más barato que defenderlo
después.**

🚨 **Y al leerla a ojo apareció lo que ningún campo cazaba: la respuesta inventó la CAUSA.**
Dijo que las monedas fallaron *«debido a limitaciones en el servicio»*. **El servicio estaba
perfecto — el que se quedó sin dinero fui yo.** El modelo no mintió sobre el *qué*: mintió
sobre el *por qué*, y lo hizo porque **el harness no le dijo el porqué**: arriba llegaba
`{"error": "No se pudo consultar USD"}`, sin causa. ⚠️ **Un agente al que no le das la causa
se la inventa, y suena razonable.** Es el mismo agujero que `motivo` acababa de tapar entre
el worker y la contabilidad, **una frontera más arriba**.

---

##### ⏭️ LO QUE C.2 DEJA ABIERTO, con dueño

- 🔲 **El techo tiene que acotar de verdad**: comprobar `gastado + coste_estimado > techo`
  antes de autorizar. Exige una estimación —la que se le echó en cara al candidato 3— y con
  ella el esquema 2 deja de ser *«sin estimar»* y pasa a ser *«estimando una vez por
  llamada»*. **Entra con su medición al lado o no entra** (`LM.13`).
- 🔲 **La causa tiene que cruzar la frontera hacia arriba**: `{"error": ..., "motivo":
  "presupuesto"}` en vez de un error mudo, para que el orquestador no tenga que inventarse por
  qué falló su especialista.
- 🔲 **Y sigue en pie la obligación del sobre:** sin un encargo **desigual**, C.2 midió el
  freno y no midió el reparto. Con tareas gemelas, el esquema 1 y el 2 son indistinguibles —
  y ahora, además, se sabe que producen **todo o nada**.

---

#### 🎲 C.2 · CIERRE — LA APUESTA, sellada el **2026-08-21** (sesión 99) **antes de la primera línea de código**

> Van **siete** sesiones sellando antes de teclear y las seis anteriores han cobrado. Hoy la
> sesión no abre una pieza nueva: **cierra los tres pendientes con dueño que la 98 dejó**, y
> por eso la apuesta es más incómoda — dos de las tres predicciones dicen que **arreglar algo
> va a empeorar otra cosa**, y eso sólo se puede apostar antes de verlo.

##### 📏 LO QUE YA SE SABE, y por tanto NO se apuesta

Estos tres números salen de la corrida pagada de ayer y del código que está en el repositorio.
No cuestan nada y no son predicciones:

| dato | valor | de dónde |
|---|---:|---|
| trozo del presupuesto apretado | **$0,003606** | `$0,014424 × 0,75 ÷ 3` |
| coste medido de una llamada de worker | **$0,002404** | media de la demo C.1 |
| llamadas que cabían con el freno viejo | **3** | autoriza si `gastado ≥ techo`, y en la 3ª `gastado` ya iba $0,0048 |

🔑 Con el freno arreglado —`gastado + estimado > techo`— la aritmética cambia sola y **no hace
falta correr nada para verla**: la llamada 2 pide $0,0024 + $0,0024 = **$0,0048 > $0,003606**,
así que **se bloquea la 2, no la 3**. Eso es una consecuencia, no una apuesta.

---

**1️⃣ ARREGLAR EL TECHO VA A EMPEORAR EL HALLAZGO 2, Y ESE ES EL PRECIO. Se apuesta con ~70 %.**

Ayer el worker murió **con la respuesta en la mano**: ya tenía `tasa` y `convertir`, y el corte
cayó en la llamada que sólo servía para redactar. Con el freno acotando de verdad, el corte se
adelanta una llamada entera.

Predicción concreta y falsable, sobre la corrida apretada de hoy: **los workers cortados
habrán ejecutado MENOS herramientas que ayer** — cero o una, no las dos. En particular
**`convertir` no aparecerá** en la lista de herramientas de al menos un worker cortado.

⭐ Si se cumple, la lección no es que el arreglo esté mal: es que **un techo honesto compra
exactitud pagando con trabajo desperdiciado antes.** Un freno que autoriza a ciegas se pasa del
techo pero llega más lejos; uno que estima corta a tiempo y tira más. **No hay una tercera
opción sin cambiar de esquema**, y por eso el candidato 3 vuelve a asomar aquí.

---

**2️⃣ DARLE LA CAUSA AL MODELO LE QUITARÁ LA CAUSA INVENTADA. Se apuesta con ~65 %, y es la
más floja de las tres.**

Ayer la respuesta dijo *«debido a limitaciones en el servicio»* con el servicio perfecto.
Hoy sube `motivo` por la frontera.

Predicción concreta y falsable, sobre el texto final de la corrida apretada:

- ✅ **NO** aparecerá ninguna atribución a un tercero — ni *servicio*, ni *proveedor*, ni
  *API*, ni *no disponible*, como causa del fallo.
- ✅ **SÍ** aparecerá una palabra de la familia del dinero: *presupuesto*, *límite*, *coste*.

⚠️ **Se apuesta al 65 % y no más alto por un motivo que ya cobró ayer:** esto se comprueba
buscando palabras, y buscar palabras dio un falso rojo en la afirmación 6. **La afirmación
queda declarada INDICIO otra vez**, y el veredicto lo pone la lectura a ojo. Declarar débil un
instrumento por adelantado costó diez segundos ayer; defenderlo después habría costado la
sesión.

---

**3️⃣ CON UN ENCARGO DESIGUAL, EL REPARTO CIEGO ENSEÑARÁ SU DEFECTO: DINERO SIN GASTAR AL LADO
DE UN WORKER MUERTO DE HAMBRE. Se apuesta con ~80 %.**

Es la obligación del sobre, la que lleva dos sesiones sin pagarse. Ayer no se pudo medir el
reparto porque los tres encargos eran gemelos (dispersión **1,00×–1,02×**) y **todos los
esquemas dan lo mismo sobre tareas gemelas**.

Predicción concreta y falsable: con un encargo donde **un worker necesite claramente más que
su trozo y los otros claramente menos**, en la misma corrida se verán **las dos cosas a la
vez**:

- el worker caro cerrará con `motivo="presupuesto"`, **y**
- los baratos cerrarán bien dejando **sobrante sin usar en sus trozos**.

🔑 **Ese sobrante es el número que C.2 lleva dos sesiones sin poder enseñar**, y es la
diferencia entera entre el candidato 1 y el 2: con tope por pieza el desperdicio es invisible
porque no hay total; con reparto a la entrada el total existe, **y por eso el desperdicio se
puede contar**. 📌 La predicción no dice cuánto sobrará — decirlo sería inventar un número —,
dice que **sobrará y será contable**.

⚠️ **Y el modo de fallo de esta apuesta está nombrado antes de correr:** que el encargo
«desigual» no lo sea de verdad. Si el worker caro cuesta sólo un 20 % más, la corrida no
distingue nada y **el resultado no será «apuesta fallada», será «instrumento ciego otra vez»**.
Por eso la desigualdad se diseña **con un número delante**, no con un adjetivo.

---

##### 🚧 LO QUE ESTA SESIÓN NO VA A HACER, dicho ahora

- **No se toca C.3.** Los tres pendientes primero, que es la línea con la que abrió el día.
- **No se afloja ninguna vara de ayer.** Si `P2b` se pone roja porque el corte se adelantó,
  **se corrige la regla y se dice**, no se ajusta el umbral hasta que vuelva a verde: eso es
  mover la portería (`LM.21`).
- **El pendiente viejo de C.1** —un mismo `id` con dos padres— sigue con dueño y **entra con
  su torcedura al lado o no entra**.

---

##### 🏁 C.2 · CIERRE — EL RESULTADO DE LA CORRIDA DESIGUAL ($0,035567, sesión 99)

**Se pagó UNA corrida y salió el hallazgo más grande del bloque C — y nadie lo había
apostado.** Las tres apuestas de la mañana se resuelven abajo; ninguna se redefinió después
de ver el resultado.

###### 📊 Lo que pasó, en números

| worker | encargo | llamadas | coste | de su trozo $0,019699 |
|---|---|---:|---:|---:|
| usd | barato | 3 | $0,007198 | 37 % |
| eur | barato | 3 | $0,007201 | 37 % |
| **cad** | **caro (cadena de 3)** | **5** | **$0,016504** | **84 %** |

Total $0,035567 de un techo de $0,078797 · `estimaciones_cortas = 0` en las cuatro piezas.

---

###### 🚨 EL HALLAZGO: EL CONTRATO SE LLENÓ ENTERO, CON LOS NÚMEROS DE OTRA PREGUNTA

**Importancia: alta · Urgencia: no bloqueante** (no rompe nada hoy; el modelo de arriba lo
tapó por casualidad).

El orquestador pidió CAD. Esto es lo que le subió, palabra por palabra del registro:

```
PIDIÓ:  {"moneda": "CAD", "monto": 1000}
SUBIÓ:  {"moneda": "USD", "monto": 725.65, "pesos": 621.18,
         "tasa": 0.856037, "fuente": "mercado (open.er-api.com)", ...}
```

**Los seis campos llenos. `faltan: []`. `ok: True`. `motivo: None`.** Y todo mal: la moneda
no es la que se pidió, el monto no es el que se pidió, y `pesos: 621.18` **no son pesos —
son euros**, el último eslabón de la cadena que el encargo caro pedía.

⭐ **El worker hizo exactamente lo que se le mandó.** El encargo desigual decía *«convierte a
pesos, luego ESE resultado a dólares, luego ESE a euros»*, y el contrato de A.3 se llena con
**la última llamada a `convertir` que pasó por el harness**. La última era la de euros.

🔑 **Y ésta es la frase que se lleva C.2 entera: `faltan` responde a «¿qué campo quedó
vacío?» y nunca respondió a «¿este campo habla de lo que yo pregunté?». UN CONTRATO COMPLETO
NO ES UN CONTRATO CORRECTO.** El harness lo dio por bueno —`datos["pesos"]` no era `None`, que
es lo único que se comprobaba— y lo pasó hacia arriba como dato válido.

🚨 **Lo único que lo cazó fue el modelo de arriba, leyendo.** Dijo: *«la respuesta que obtuve
no tiene el formato esperado para una conversión de 1.000 CAD, por lo que no puedo darte una
cifra confiable»*. ⚠️ **Un guardarraíl hecho de prosa atrapó lo que el contrato tipado dejó
pasar**, y eso es exactamente al revés de por qué existe A.3. No se puede confiar en que
vuelva a pasar: fue suerte de que los números fueran *absurdos* (621 «pesos» por 1.000 CAD).
**Con una cifra verosímil habría subido a la respuesta final sin que nadie tosiera.**

📌 Es el mismo defecto que la sesión 99 ya cazó dos veces en pequeño —las pruebas gratis
ensuciando el registro pagado, y ahí también **lo que salvó fue que los números falsos eran
reconocibles**. Tres veces el mismo mecanismo en un día: *lo que detecta el error no es el
sistema, es que el error era llamativo.*

🔲 **PENDIENTE CON DUEÑO, y es de C.3:** el contrato tiene que comprobar que **responde a lo
que se preguntó** —al menos `datos["moneda"] == moneda_pedida`—, no sólo que no tiene huecos.
**Entra con su torcedura al lado o no entra.**

---

###### 🎲 LAS TRES APUESTAS, resueltas

**🅰️ APUESTA 1 — el techo arreglado adelantaría el corte: NO SE PUDO EVALUAR, y decirlo es
el resultado.** Nadie cortó en esta corrida, así que la corrida pagada **no ejercitó la
predicción**. ✅ Lo que sí está medido, y gratis, es `P11b`: con el trozo apretado el worker
hace **1 llamada donde antes hacía 2**. La predicción tiene su número; lo que no tiene es el
sello de haberse visto con dinero real. ⚠️ **No se cuenta como ganada.** Que una medición
gratis diga lo mismo no convierte una apuesta no ejercitada en una apuesta cobrada.

**🅱️ APUESTA 2 — la causa quitaría la causa inventada: TAMPOCO SE PUDO EVALUAR.** No hubo
ningún fallo por presupuesto, así que `causa` **nunca se disparó**. Las dos afirmaciones
salieron en rojo por motivos que no acusan al arreglo:

- La 7 dio un **falso rojo de manual**: buscaba la palabra `api` como señal de culpar a un
  tercero, y la encontró dentro de **`open.er-api.com`**, que es la fuente legítima de las
  *otras dos* monedas. 🔑 Segundo día seguido en que buscar palabras da un rojo falso, y
  segundo día en que **estaba declarada INDICIO antes de correr** y por eso costó diez
  segundos en vez de una discusión.
- La 8 salió roja por **ausencia de la condición**, no por fallo: no se nombra el dinero
  porque el dinero no falló.

**🅲 APUESTA 3 — el caro cortaría mientras sobra dinero al lado: FALLADA en su mitad central,
y la mitad que se pagó salió CLAVADA.**

- ❌ **El caro NO cortó.** Gastó $0,016504 de su trozo de $0,019699 — se quedó al 84 %.
- ✅ **Pero la desigualdad diseñada funcionó con una precisión que no esperaba: 2,29× medido
  contra 2,33× predicho.** El instrumento sirve; el umbral de 1,8× se cumplió de sobra.

🚨 **Y EL MOTIVO DEL FALLO ES UNA LECCIÓN SOBRE MEDIR, NO SOBRE PRESUPUESTOS.** El techo se
calculó con **7 vueltas × el p90 de $0,004546**. El caro hizo **5 llamadas** (el modelo pidió
las tres tasas **en la misma vuelta**, que es justo el mecanismo de batching que yo mismo
había escrito tres horas antes al diseñar la cadena) y costó $0,016504. **Sobreestimé el
encargo caro en 1,93×, y esa generosidad es exactamente lo que salvó al worker que quería ver
ahogarse.**

🔑 **El p90 es el precio CORRECTO para un freno y el precio EQUIVOCADO para un instrumento.**
Un freno se equivoca hacia arriba a propósito: prefiere sobrar. Una medición que se equivoca
hacia arriba **se anula a sí misma**: paga un techo demasiado grande y luego no ve el corte
que fue a buscar. **El mismo número, correcto en un papel y ciego en el otro** — y lo usé en
los dos sin darme cuenta de que había cambiado de papel.

---

###### ✅ Lo que C.2 deja cerrado, y lo que deja abierto

**Cerrado:**
- El techo acota: `gastado + estimado > techo`, en las DOS capas, con `estimaciones_cortas`
  como báscula propia. En la corrida real: **0 estimaciones cortas de 11 llamadas**.
- La causa cruza la frontera (`motivo` + `causa` en español). Construido y probado en `P14`;
  **sin ejercitar con dinero**.
- El encargo desigual existe, está medido (2,29×) y **el reparto ciego desperdició $0,024999
  reales** parados en los baratos — el número que C.2 llevaba dos sesiones sin poder enseñar.

**Abierto, con dueño:**
- 🔲 El contrato debe comprobar que **responde a lo que se preguntó** (el hallazgo de arriba).
- 🔲 Volver a correr la desigual con el techo dimensionado con el **coste esperado**, no con
  el p90, para ver por fin al caro ahogarse. Es barato y ahora se sabe con qué número.
- 🔲 El detector de un mismo `id` con dos padres distintos, arrastrado de C.1.

---


#### ✅ C.3 — LOS PERMISOS *(construida en las sesiones 100 y 101 · **escrita aquí en la 105**)*

⚠️ **Este bloque llega CUATRO SESIONES TARDE, y eso no es un detalle de formato.** El código
de C.3 se escribió el 2026-08-21 y funcionó; el bloque que lo explica no existía. Entre medias
el nivel siguió a C.4, C.4b, C.5 y C.6 con una pieza marcada como hecha **cuya lección no
estaba en ninguna parte**. 🔑 **Lo que no está escrito no se enseñó** — y el aviso estuvo
anotado en las tres sesiones siguientes sin que nadie lo alcanzara, que es `LM.20` otra vez.

---

##### 🔓 La mitad de C.3 ya estaba resuelta ANTES de empezar — y no se resolvió por seguridad

La tabla del bloque prometía *«Permisos: quién puede qué»* con la trampa *«el orquestador no
toca herramientas reales»*. Al llegar aquí resultó que **eso ya estaba hecho desde A.1 y A.2**,
y por motivos que no eran de seguridad:

- **En un worker el permiso deja de ser una pregunta y se vuelve la caja** (A.1). No hay
  `input()` ni `pedir_permiso` porque **a un worker lo llama un programa, no una persona: no
  hay dónde decir que no.** Este worker no lleva `guardar_reporte`, y por eso no puede escribir
  en el disco. El menú y el puente se recortan **los dos** — si sólo se recortara el menú, un
  modelo que pidiera `trm` de memoria la encontraría y se ejecutaría. **El que manda es el
  puente.**
- **El orquestador no lleva ni una herramienta de verdad** (A.2), y la razón que se escribió
  entonces era del experimento, no de la seguridad: *un orquestador que puede resolver la
  tarea él solo, la resuelve él solo*, y el bloque F estaría midiendo al contendiente A
  disfrazado de B.

⭐ **Y ahí está el hallazgo de esta mitad: la decisión correcta ya estaba tomada, pero por el
motivo de al lado.** C.3 llega a la misma línea de código por seguridad. Una decisión que sólo
tiene el motivo del experimento **se cae el día que el experimento termina**; con los dos
motivos escritos, aguanta.

---

##### 🪤 La mitad que SÍ faltaba: un permiso dice quién puede llamar, no si te contestaron TU pregunta

El pendiente que C.2 dejó abierto y era de C.3: **el contrato comprobaba que la respuesta
estuviera COMPLETA y no que fuera LA TUYA.**

El caso venía pagado de la sesión 99: se pidió **CAD**, las herramientas trajeron **USD**, y el
contrato salió sin un solo hueco. `faltan: []`. Verde.

🔑 **Los permisos son una defensa de entrada: quién puede llamar a qué.** No dicen nada sobre
lo que vuelve. Un worker con la caja perfectamente recortada puede devolver, con todos los
permisos en regla, **el dato de otra pregunta**.

---

##### 🔧 El arreglo — el contrato pasó a devolver TRES cosas, y la tercera es nueva

`contrato_divisa(llamadas)` → `contrato_divisa(llamadas, pedido)`, y devuelve:

| | qué significa | cómo se corta |
|---|---|---|
| `datos` | el contrato | — |
| `faltan` | qué campos **no pudo llenar** → un **HUECO** | se puede seguir con lo que hay |
| `discrepa` | en qué **no coincide** con lo pedido → una **CONTRADICCIÓN** | lo que hay es justo lo que no sirve |

📌 **`pedido` viaja en Python, al lado del encargo en prosa, y no dentro de él.** El encargo no
puede delatar al modelo que lo ignoró: **él mismo es la frase que se ignoró.** El testigo tiene
que venir por fuera de lo que se está juzgando.

📌 **`None` no es `[]`.** Sin `pedido`, `discrepa` vale `None` = **no comprobado**, que no es lo
mismo que `[]` = comprobado y cuadra. Se ven casi igual y significan lo contrario (`P21`).

---

##### 🥇 Hallazgo 1 — un hueco y una contradicción se cortan en SITIOS DISTINTOS → `LM.69`

Se apostó que meter la discrepancia dentro de `faltan` **no frenaría nada**, y se ganó con el
número delante. El corte del orquestador era `datos.get("pesos") is None`; con la respuesta
torcida, **`pesos` valía 1.025.625: estaba lleno.** El filtro buscaba huecos y ahí no había
ninguno.

Hicieron falta **un campo aparte y un corte aparte**. Dos pruebas, y la primera es la que duele:

- `P19` — la respuesta torcida **no tiene ningún hueco** (`faltan` vacío).
- `P20` — **y aun así se caza**: `discrepa: ['moneda: se pidió CAD y el contrato trae USD']`.

🔑 **Sin `P19`, `P20` podría estar cazando un hueco y creerse que caza una contradicción.**
Una prueba que demuestra que el detector viejo estaba ciego vale tanto como la que demuestra
que el nuevo muerde.

---

##### 🥈 Hallazgo 2 — el detector que cazaba la mentira LLEVABA UNA NOCHE MORDIENDO → `LM.70`

Salió de comprobar que no se había roto nada. **`traza.py` estaba en rojo ANTES de tocar
código** (verificado con `git stash`). Su prueba decía *«y no caza nada más: `len(contra) == 1`»*
— y cazaba **dos**. La segunda era
`{'hora': '2026-08-21T19:41:33', 'se_llama': 'cad', 'hizo': 'USD'}`: **la mentira de la corrida
pagada del día anterior.**

`auditar_etiquetas` existe desde C.1 · paso 5 y **la cazó en el segundo en que se grabó**. Aquel
día el hallazgo lo hizo un humano leyendo la salida a ojo.

⭐ **No faltaba el detector: el detector mordió y su mordisco se quedó en un archivo que nadie
abrió.** Es `LM.13` girado del revés — un freno que muerde sin testigo produce **exactamente el
mismo silencio** que uno que no muerde.

📌 **Y el segundo filo, sobre cómo se escriben las pruebas:** `len(contra) == 1` es **un número
pelado, y los números pelados envejecen**. Bastó que el mundo grabara una segunda mentira de
verdad para ponerla roja **sin que nada se hubiera roto**. Corregida a comprobar **por hora,
nombrando las conocidas**: una tercera sí la pone roja, que es lo que se quería vigilar.

📌 **De aquí salió un paso de rutina que no existía:** correr `traza.py` **DESPUÉS de cada
corrida pagada**, no sólo antes de commitear código. Cobró al día siguiente — cazó en el acto
una tercera contradicción, `cad → COP`, la huella del contrato viejo. **Se deja en la lista de
conocidas: el registro no se reescribe, y borrarla sería borrar la evidencia.**

---

##### 🥉 Hallazgo 3 — un arreglo puede REABRIR el que tiene al lado → `LM.71`

La corrida pagada de C.3 ($0,028745) destapó que **el arreglo de la mañana rompió el de la
víspera**.

El worker `cad` se quedó sin presupuesto a mitad de una cadena de tres conversiones. Su
contrato quedó a medias y **por eso** discrepaba. Como el corte de discrepancia iba **primero**,
arriba subió `motivo="discrepancia"`, y el modelo lo repitió tal cual:

> *«no se pudo consultar por discrepancia en los datos del especialista»*

**Falso: se quedó sin dinero.**

🔑 **La discrepancia sólo significa algo en un worker que TERMINÓ.** En uno que se paró a
medias, la discrepancia **no es la causa: es el rastro de haberse parado.** Una consecuencia no
puede ir delante de su causa.

🚨 **Ninguna prueba lo vio, porque cada una vigilaba su mitad.** Apareció **sólo al pagar una
corrida entera y leer lo que el modelo dijo al final.** Hoy lo clavan `P27` y `P27b`: un worker
cortado sube `motivo="presupuesto"` y una causa en español que **vuelve a nombrar el dinero**.

---

##### 🎁 Hallazgo 4 — el falso positivo era del MISMO TIPO que el defecto que venía a cazar → `LM.72`

Debajo había un defecto que no era de ese día. El encargo caro pide una **cadena** (CAD→COP,
ese resultado a USD, ese a EUR) y `contrato_divisa` **sobrescribía en cada llamada**: se
quedaba con `moneda: COP, monto: 2219774` — **el final del camino en vez de la pregunta.** El
worker había hecho exactamente lo que se le pidió, y el detector nuevo gritaba.

⭐ **Ayer «completo» sin ser correcto; hoy «incorrecto» sin que nadie mienta.** El detector daba
un falso positivo de la misma familia que el defecto que venía a matar.

✅ **Arreglado a decisión del estudiante: gana el PRIMERO** — y «el primero» es **el primer
acierto**, no la primera línea: los errores ya se saltan antes, así que un worker que falla y
reintenta sigue contando lo bueno (`P29`). Comprobado sobre las llamadas **reales** de la
corrida pagada: `{'moneda': 'CAD', 'monto': 1000, 'pesos': 2219774}` con `discrepa: []`.

⚠️ **El precio, dicho entero y no escondido:** un contrato de un renglón describe bien el primer
paso y **sigue sin contar la cadena**. Los pasos intermedios sólo viven en el registro.
**Fingir que sí era lo que hacía la versión anterior.**

---

##### ⚠️ El error caro de C.3, con el número delante: **$0,087297 tirados**

Se corrieron `pipeline.py` ($0,016859) y `linea_base.py` ($0,070438) **en pelado**, dando por
hecho que eran suites gratis como `traza.py` o `router.py`. **No lo son: pagan sin preguntar.**
Es **2,5×** lo que costó la corrida legítima del día.

🚨 **Y el daño caro no fue el dinero:** `linea_base.py` **reescribió su medición sellada** — la
línea base del duelo del bloque F, medida el 2026-08-20. **Recuperada con `git checkout` porque
estaba en Git.**

🔑 **Un script que mide y guarda en el mismo sitio cada vez que corre no tiene medición: tiene
la última.** → de aquí salió la lista de `GUIDE.md` §6.e, con el molde bueno señalado
(`presupuesto.py`) y los dos malos escritos con nombre.

---

##### 📋 Resumen de C.3

| | |
|---|---|
| Archivos | `worker.py` (`contrato_divisa(llamadas, pedido)`) · `orquestador.py` (corte propio + `descartado`) · `presupuesto.py` (**26 → 40 pruebas**) · `traza.py` (36 → **41**) |
| Lecciones | `LM.69`, `LM.70`, `LM.71`, `LM.72` |
| 💸 Coste | **$0,116042** — $0,028745 la corrida legítima · **$0,087297 tirados** |

**Cerrado:**
- El contrato comprueba que **responde a lo que se preguntó**, no sólo que no tiene huecos.
- Hueco y contradicción son **dos listas y dos cortes**, y el dato descartado se conserva como
  `descartado` — nunca como `datos`.
- La causa que sube al modelo **nombra el motivo real** del worker que se paró.

**Abierto, con dueño** *(y sigue abierto hoy)*:
- 🔲 **El contrato de una CADENA** (`LM.72`): hoy guarda el primer paso; los intermedios sólo
  viven en el registro. **Decidir si entra o se declara fuera de alcance.**
  *Importancia: media · Urgencia: no bloqueante.*
- 🔲 **`profundidad.py:213`** sigue con la copia ciega del corte (`pesos is None`, sin `pedido`).
  **No se arregló a propósito:** ahí la discrepancia **es el objeto de estudio**. ❓ *¿El
  experimento quiere que el harness cace su propia torcedura, o la necesita pasando?* Sin esa
  respuesta, tocarlo es romper el instrumento.
  *Importancia: media · Urgencia: no bloqueante.*

---

#### 🎲 C.4 — LA APUESTA, sellada el **2026-08-21** (sesión 101) **antes de la primera línea de código**

⚠️ **Y esta la escribió Claude, no el estudiante.** Se dice arriba del todo porque cambia lo
que vale: el sospechoso que llevaba cinco sesiones nombrado —*«el que apuesta es el mismo que
evalúa»*— aquí está en su forma más pura. La única defensa es que **las cinco se falsifican
con un comando y no con una opinión**, y que cuatro de las cinco cuestan **$0,00**.

Lo apostado, en corto:

1. el crash ya no tumba al orquestador, **pero se lleva su gasto del libro**
2. el árbol no ve un tramo que se abrió y no cerró
3. el mensaje que sube al modelo **miente para los fallos pasajeros**
4. *«se demora»* no tiene freno propio, y su tope real nadie lo ha calculado
5. 💸 la corrida desigual con todo arreglado (~$0,03) sube la causa limpia

**Resultado: las cinco ganadas.** Y la que más enseñó no fue ninguna de las cinco.

---

##### La pregunta de C.4, y por qué las tres patas *parecen* resueltas

Un worker es un agente dentro de otro. Hasta aquí siempre terminó — bien, sin presupuesto o
sin vueltas, pero terminó. **C.4 es el día en que no termina**, y son tres cosas distintas:

```
SE CAE      -> revienta a mitad. Excepción, traceback, adiós.
SE DEMORA   -> no revienta: se queda ahí. El que espera no sabe si sigue.
NO CONTESTA -> da vueltas y nunca llega a una respuesta.
```

🚨 **La trampa es que las tres tenían ya su freno escrito**: un `except Exception` en la
frontera desde B.2, un `motivo="max_vueltas"` desde A.1, y un timeout del SDK desde el nivel
5b. `fallos.py` no da por bueno nada de eso: **lo hace morder y mira qué queda en pie.**

📌 **Y todo el paso cuesta $0,00**, porque el modelo es de mentira y el harness no. Un
`ClienteDeMentira` devuelve respuestas con `usage` inventado y revienta cuando se le dice; el
bucle del worker, la contabilidad, el registro y el árbol son los de verdad. 🔑 **Lo falso es
el que habla, no el instrumento.** Si el instrumento fuera falso, mediríamos al instrumento.

---

##### Los cuatro agujeros, medidos antes de tocarlos

| # | Lo apostado | Lo medido |
|---|---|---|
| 1 | el crash se lleva su gasto del libro | gastó **$0,004000**, en la factura **$0,000000** |
| 2 | el árbol no ve el nodo abierto | 1 `worker_inicio`, 0 `worker_fin`, **0 quejas** |
| 3 | el mensaje miente para los pasajeros | las dos frases, **idénticas carácter por carácter** |
| 4 | «se demora» no tiene freno propio | techo real **490 s = 8,2 min**, nunca calculado |

🔑 **El agujero 1 es el que hay que entender, porque no es donde se mira.** El `except
Exception` de la frontera SÍ atrapaba el crash y el orquestador SÍ seguía vivo — eso funciona
desde B.2 y nadie lo había roto. El daño estaba en otro sitio: `correr_worker` que **lanza**
nunca devuelve, así que las seis líneas de `contabilidad[...] += resultado[...]` no llegan a
correr. **El dinero se gastó y no está en ningún libro.**

> ⭐ **El gasto no se pierde por gastarse mal: se pierde por no volver por donde se cuenta.**
> Un fallo que sale por una puerta distinta a la del éxito se lleva consigo todo lo que se
> apuntaba en la puerta del éxito. → `LM.73`

📌 Y el comentario que había justo encima del `except` llevaba dos bloques diciendo *«un
worker devuelve su fracaso COMO DATO»*. Era verdad **sólo para el presupuesto**. Cualquier
otra excepción se lanzaba hacia arriba, y el comentario no distinguía.

---

##### Los cuatro arreglos, y el rojo que los prueba

- **El worker cierra siempre.** `except agente.REINTENTABLES` y `except Exception` devuelven
  `motivo="crash_temporal"` / `"crash"` como dato. El dinero cuadra al céntimo.
- **La frontera distingue.** `_CAUSAS` gana tres entradas. Al fallo pasajero **se le deja
  reintentar**; al defecto nuestro, no. Antes las dos recibían *«No lo llames otra vez
  igual»* — que para el pasajero no era impreciso, era **dañino**: le prohibía justo lo
  único que lo arreglaba. Es `LM.71` con otra ropa.
- **El plazo se decide.** `LIMITE_WORKER_SEGUNDOS = 90`, mirado antes de cada vuelta, igual
  que el presupuesto. Y el número **sale de un dato**: los 99 workers pagados del curso dan
  mediana 2,28 s, p90 5,73 s y peor caso 17,94 s. **90 s son 5× el peor visto** — un freno
  que no puede morder a uno legítimo — y 5,4× menos que el residuo que había.
- **El árbol gana una queja**: `nodo_abierto`, con su torcedura al lado (`traza.py` 41 → 46).

> ⭐ **Un plazo que nadie decidió no es un plazo: es un residuo.** Los 490 segundos existían
> —eran ciertos, eran el tope real— pero salían de multiplicar tres constantes escogidas por
> otros motivos. Nadie los había escrito nunca. → `LM.75`

⚠️ **Y el precio del plazo se dice entero:** corta **entre vueltas**, no dentro de una. Una
llamada colgada sigue acotada sólo por el timeout del SDK. Lo que este freno mata es la
**suma**, que era lo que no tenía dueño.

🚨 **CÓMO SE SABE QUE LOS ARREGLOS ARREGLAN LO QUE SE MIDIÓ.** Las pruebas 7 a 13 de
`fallos.py` existieron **en verde describiendo el daño**: *«el dinero NO llega a la
factura»*, *«el auditor no se queja»*, *«las dos frases son la misma»*. Al meter los
arreglos **se pusieron rojas las seis de golpe**, y sólo entonces se reescribieron para
vigilar lo arreglado. 🔑 **Un arreglo que no pone roja ninguna prueba vieja no está
arreglando nada medido: está arreglando algo que nadie vio romperse.**

---

##### La queja que no se parece a las otras cinco

Las cinco quejas del auditor del árbol se disparan porque **dos datos se contradicen**.
`nodo_abierto` no: se dispara porque **falta uno**. Un worker que revienta anota su
`worker_inicio` y muere antes del `worker_fin`, y el árbol que sale es impecable — el
`padre` existe, la `profundidad` cuadra, la `corrida` es la misma, no hay ciclo.

> ⭐ **`LM.66` al revés, y es peor.** Aquella decía que un dato que nadie puede desmentir no
> es correcto, es **no comprobable**. Aquí no hay dato ninguno, y **la ausencia no contradice
> a nadie**. Medido antes de escribir la comprobación: 1 inicio, 0 fines, **0 quejas**.
> → `LM.74`

📌 **Se mira por el sufijo del evento, no por el nombre del tramo** —los cinco pares del repo
usan `_inicio`/`_fin`—, y **sólo en una dirección**: un `_fin` huérfano NO se denuncia,
porque los hay legítimos. Denunciarlos sería el falso positivo de `LM.72` otra vez.

🎁 **Y el detector cazó dos montajes descuidados el día que nació — los dos míos**, en el
propio `fallos.py`: una raíz que abría tramo sin anotar, y un cierre que faltaba. **Un
instrumento mal montado no da silencio: da una queja creíble sobre otra cosa.**

---

##### «No contesta»: el freno completo que nunca había mordido

`max_vueltas` existe desde A.1. Tiene su motivo, tiene su frase para el modelo, cruza la
frontera. Contados los cierres de worker de **todos** los registros del curso:

```
102 cierres:  28 por presupuesto  ·  74 terminaron bien  ·  max_vueltas: CERO
```

🚨 **Y el docstring de `fallos.py`, escrito esa misma mañana, decía de esta pata: «esta ya
está».** El archivo que venía a decir que un freno sin morder es una nota lo dio por resuelto
en su tercer renglón. **Se da por resuelto lo que está escrito, no lo que está probado.**
Hoy muerde: 5 vueltas, `motivo="max_vueltas"`, causa en prosa arriba y gasto cuadrado.

---

##### El crash en PARALELO, que es la topología que importa

Todo lo anterior se midió con **un** worker, **en serie**. `orquestador.py` lleva escrito
desde B.2 que atrapar la excepción **en el sitio que no sabe de hilos** hace que dé igual — y
nadie lo había visto. Tres workers, tres hilos, el CAD revienta a media faena:

- **USD y EUR entregan su dato.** El CAD sube `motivo="crash"` con su causa.
- **Los tres entran en la factura** ($0,016000 de registro = $0,016000 de libro).
- **El árbol aguanta**: 3 tramos `worker:`, **ninguno huérfano**, 0 quejas. Eso es `atado()`
  cumpliendo con un hilo muerto dentro.

⚠️ Pero eso solo **no prueba que la red sirva de algo** — podría ser que en paralelo un crash
nunca fuera peligroso. Así que se corrió el contrafactual, mismos bloques, misma excepción:

| | Resultados que llegan |
|---|---|
| **Con** la red (`ejecutar_un_bloque`) | **3 de 3** |
| **Sin** la red (`pool.map` pelado) | **0 de 3**, `RuntimeError` al recoger |

> ⭐ **Sin red no llega ninguno — ni los dos que iban bien.** Terminaron su trabajo, gastaron
> su dinero, y su resultado se pierde al recoger la tanda. **La excepción no mata al que
> falló: mata a los que iban bien.** Por eso el `except` está en el sitio que no sabe de
> hilos: así el paralelo no tiene que acordarse de nada.

---

##### 💸 La corrida pagada — $0,027482

| | |
|---|---|
| Total | $0,027482 de un techo de $0,048689 |
| El caro (`cad`) | cortó por presupuesto en **$0,008207** de $0,012172 |
| Parado en los baratos | **$0,009781** mientras el que lo necesitaba se ahogaba |

✅ **La apuesta 5, ganada.** El modelo dijo: *«No se pudo consultar. El especialista se quedó
sin presupuesto para esta consulta.»* — **la causa que le dio el harness, repetida sin
adornos.** Ninguna causa inventada. Las afirmaciones 7 y 8 llevaban dos sesiones sin poder
cobrarse; la 8 cobró.

✅ Y `LM.72` aguantó con dinero delante: el contrato del CAD salió `{'moneda': 'CAD',
'monto': 1000}` con `discrepa: []`. Ayer, en este mismo sitio, decía `{'moneda': 'COP',
'monto': 2219774}`.

❌ **La afirmación 7 salió roja, y el culpable es el medidor.** Buscaba palabras que
indicaran culpar a un tercero y encontró **`api`** — dentro de **`open.er-api.com`**, que es
la *fuente* de los dos workers que terminaron bien. 📌 El propio archivo había declarado ese
indicio débil **antes** de correr, con la frase *«buscar palabras ya dio un falso rojo una
vez»*. Segunda vez, mismo modo. **El número no se toca** —moverlo con el resultado delante es
mover la portería—, pero queda dicho por qué está rojo.

---

##### ✅ Lo que C.4 deja cerrado, y lo que deja abierto

**Cerrado:**
- El worker **siempre cierra**: se caiga, se demore o no conteste. Cuatro motivos nuevos
  (`crash`, `crash_temporal`, `plazo`) y la contabilidad cuadra en los cuatro.
- Las tres patas **vistas morder**, y las tres con su contrafactual al lado.
- El crash en paralelo, medido: la tanda sobrevive y el árbol también.
- `nodo_abierto` en el auditor, con torcedura y con vigilancia sobre los registros reales.
- La corrida pagada: la causa sube limpia y el modelo la repite.

**Abierto, con dueño:**
- ✅ 🚨 **CERRADA EN LA 102 CON (a)+(b) — ver `C.4b` más abajo.** Era la única
  deuda que era de C.4, y la abrió el arreglo de C.4. Se deja escrito el problema
  tal como estaba, porque el enunciado es la mitad de la lección. La causa
  `crash_temporal` le dice al modelo *«esta sí puede salir bien al segundo
  intento»* — y si acepta la invitación, `reparto.tomar()` **ya no tiene trozo**
  y le contesta *«es uno de más. No lo reintentes»*. Comprobado a $0,00: la 4ª
  llamada devuelve `sin_trozo: true`. 🔑 **Dos instrucciones contrarias del mismo
  harness en dos turnos seguidos**, y la segunda además dice algo falso: no es
  que el worker sobre, es que se le acabó el sitio. Es `LM.71` **por tercera vez
  en tres sesiones** —un arreglo reabre el que tiene al lado— y ninguna prueba lo
  vio porque **cada una vigila su mitad**: una comprueba el mensaje, otra el
  cuarto worker, y nadie miraba la frase que va entre las dos. 📌 Nunca se ha
  visto con dinero delante: `crash_temporal` necesita una caída real de la API.
  **Tres salidas, y es decisión de diseño:** (a) reservar un trozo para
  reintentos, (b) condicionar la invitación a que quede trozo, (c) retirar la
  invitación. **(c) es la más honesta y la más pobre.**
  ➡️ **Se eligieron (a) Y (b), y las dos hicieron falta:** (a) sola movía la
  contradicción un turno —gastada la reserva, volvía intacta—. Y de los dos
  bolsillos «gratis» no quedó ninguno: **reservar cuesta** (`LM.77`).
- 🔲 🚨 **Teníamos la respuesta del CAD y la tiramos.** El worker cortó a media cadena, pero
  su contrato salió completo y correcto: `pesos: 2.219.774`, `faltan: []`, `discrepa: []`. La
  pregunta del usuario era *«1.000 CAD, ¿cuánto es en pesos?»* — **eso lo teníamos**. Lo que
  faltaba eran los eslabones siguientes, que son del encargo artificial. La frontera lo
  descarta en un `if not resultado["ok"] or datos.get("pesos") is None`: **es un `or`**, y
  basta con que el worker no terminara para tirar un contrato lleno. 🔑 **`ok` es una
  pregunta sobre el PROCESO; `pesos` es una pregunta sobre el RESULTADO** — el harness las
  trata como una sola y se queda con la más pesimista. ⚠️ **Es una decisión de diseño, no un
  bug obvio:** entregar un resultado parcial puede ser peor que no entregar nada si el de
  arriba no sabe que es parcial. **Anotado a decisión del estudiante, no arreglado.**
- 🔲 **El contrato de una CADENA** (`LM.72`), arrastrado de C.3: hoy es un renglón y una
  cadena necesita una lista. Entra o se declara fuera de alcance.
- 🔲 **`profundidad.py:213`** sigue con la copia ciega del corte, y su pregunta sin
  contestar: *¿el experimento quiere que el harness cace su propia torcedura, o la necesita
  pasando?*
- 🔲 **C.3 nunca tuvo su bloque en este README.** El código está y la lección no. Se anota
  aquí para que no se pierda: lo que no está escrito, no se enseñó.
- ✅ **La bandera `--pagar` en `worker.py` y `orquestador.py`** — hecha en la 101
  (ver `GUIDE.md` §6.e).

#### 🔧 C.4b — LA RESERVA DE REINTENTOS *(sesión 102 · todo a $0,00)*

**El problema, en una frase:** el arreglo de C.4 dejó al harness dando **dos órdenes
contrarias en dos turnos seguidos** — *«esta sí puede salir bien al segundo intento»*
y, cuando el modelo aceptaba, *«es uno de más. No lo reintentes.»*

La salida parecía obvia —reservar presupuesto para el reintento— pero **la pregunta
real no era esa**: era **de dónde sale ese dinero**. Se propusieron dos bolsillos
que parecían gratis y **los mató un dato**:

| bolsillo | lo que se midió | veredicto |
|---|---|---|
| la bolsa del orquestador (25 %) | su holgura real, en 10 corridas pagadas: **0,47 trozos** | no llega |
| media ración ($0,004948) | sólo **12 de 57** workers pagados caben ahí | mata al reintento el **79 %** de las veces |
| ración entera ($0,009896) | cubre **53 de 57** (93 %) | la única que de verdad reintenta |

🔑 **Y morir de presupuesto produce *«no lo reintentes»***: media ración habría
fabricado **la tercera orden contraria para tapar la segunda**. Un compromiso que
dobla el problema no es un compromiso.

**Lo que se decidió:** la reserva **no se descuenta de nadie**. Es una bolsa aparte,
**hace crecer el total del encargo** y va con nombre propio en el informe
(`reintentos_reservados` / `reintentos_usados`). Los tres workers conservan sus
$0,009896 y el orquestador su bolsa; el total pasa de **$0,039585 a $0,049481**, y
ese crecimiento **se ve**. → `LM.77`: **no hay bolsillo gratis.**

**El efecto secundario que se evitó sin buscarlo:** `n_workers` sigue valiendo **3**,
así que la frase que rechaza al de más —*«se repartió para 3»*— **sigue siendo
verdad**. Un reparto de cuatro trozos le habría hablado al modelo de un reparto que
él nunca pidió.

**La distinción que faltaba, y no es un contador:**

```python
if self._trozos:                                    # un worker normal
elif nombre in self.entregados and self._reserva:   # un REINTENTO
elif nombre in self.entregados:                     # reintento, reserva gastada
else:                                               # un worker de MÁS
```

`cad` pidiendo por segunda vez es un reintento. `jpy` pidiendo por primera es uno de
más. **Hasta hoy las dos caían en el mismo `raise`, y por eso una tapaba a la otra.**

🐛 **Y ahí abajo había un defecto contable que nadie había podido ver.** El libro
guardaba `entregados[nombre] = trozo`: correcto durante todo el curso, porque cada
nombre pedía **una** vez. Con sitio para el reintento salían **cuatro** raciones de
la caja y quedaban **tres** apuntadas — **$0,007422 desaparecidos, sin excepción y
sin aviso**. → `LM.78`: *una clave contesta «a quién», y la pregunta era «cuántas
veces»*.

⭐ **No se descubrió leyendo la línea culpable.** Se descubrió porque
`cuadra()` —*repartido + guardado == total*— dejó de cumplirse. **Un invariante
sirve precisamente el día que el defecto es invisible a la vista.**

⚠️ **Y por qué llevaba ahí sin morder:** las 50+ pruebas pedían raciones con nombres
**siempre distintos** (`usd`, `eur`, `cad`, y 24 `w0..w23` en la de hilos). Ninguna
pedía dos veces lo mismo. El caso no estaba escondido: estaba **fuera del campo de
visión del instrumento**, que es peor.

**(a) sola no bastaba, y por eso entró también (b).** La reserva es finita: gastada,
volvía la contradicción intacta. Así que la causa **se elige mirando
`quedan_reintentos()`**, y las dos frases se ven morder en `P37`:

> **con reserva:** *«...un problema PASAJERO... Queda presupuesto reservado para un
> reintento: esta es de las que sí puede salir bien al segundo intento.»*
>
> **sin reserva:** *«...un problema PASAJERO... No queda presupuesto reservado para
> otro intento, así que no lo reintentes.»*

🚨 **El atajo que se descartó a propósito:** bastaba mandar el crash pasajero a la
frase de `crash` para que dejara de invitar. Habría funcionado, y el modelo habría
oído *«defecto interno nuestro»* — **mentira**. `P37c` existe para impedirlo:
**el consejo cambia con las circunstancias; el diagnóstico, no.** Es `LM.71` sin
volver a caer.

📌 **Por defecto `reintentos=0`**, y es deliberado: encender la reserva sola
cambiaría el total del encargo y con él **todas las facturas ya medidas** de C.2 y
C.3. `P35` lo vigila.

📊 `presupuesto.py` **40 → 58** pruebas. `traza.py` (46) y `fallos.py` (26), intactas.
💸 Coste del día: **$0,000000**.


---

#### 🛡️ C.5 — EL TOPE DE RECURSIÓN *(sesión 103 · `recursion.py` · todo a $0,00)*

**La pregunta, en una frase:** un orquestador llama a un worker. ¿Y si el worker es
otro orquestador? **Dos agentes pueden pasarse la pelota para siempre**, y cada pase
es una llamada que se paga.

⚠️ **Y hoy la trampa era peor que en C.4, porque había DOS frenos y los dos parecían
valer:** `max_vueltas` («el bucle no puede dar vueltas infinitas») y el presupuesto
(«cuando se acabe el dinero, para»). Los dos existen, los dos están medidos y los dos
cierran corridas de verdad todos los días. C.5 les preguntó si paraban **ésta**.

##### 🚨 Fabricar la pelota no costó ni una línea rara, y eso ES el hallazgo

`herramienta_delegar` es `orquestador.herramienta_consultar_moneda` con
`correr_orquestador` donde aquélla tiene `correr_worker`. **Esa única palabra es toda
la diferencia entre un árbol y una pelota.** No hace falta escribir nada raro: basta
con la puerta que B.5 le abrió al orquestador —`sistema`, `tools`, `funciones`—.
🔑 **La recursión no es una avería que se cuela: es lo que pasa por defecto cuando una
capa puede abrir capas.**

📌 El modelo es de mentira (`ClienteQueDelega` pide siempre delegar) y **una sola
delegación por capa**, a propósito: si delegara varias, la pelota crecería a lo ancho
y a lo hondo a la vez y el número final no diría cuál de las dos cosas la hizo crecer.

##### 🎲 Las cinco apuestas, selladas antes de medir — y la que falló es la mejor

| # | Lo apostado | Resultado |
|---|---|---|
| 1 | la pelota la para Python quedándose sin pila, **como una avería visible** | 🔴 **FALLADA** |
| 2 | `max_vueltas` no frena nada: **cero** cierres por vueltas | ✅ |
| 3 | el dinero sí para, mucho antes, pero con `motivo="presupuesto"` — falso | ✅ *y con el adjetivo corregido* |
| 4 | una capa de agente cuesta **dos** escalones de `profundidad` | ✅ exacto |
| 5 | profundidad y repetición **no cazan lo mismo** | ✅ |

##### 🔴 La apuesta 1 falló, y el modo de fallo es el hallazgo del día

Sin ningún freno y sin el corte del laboratorio: **166 capas, 330 llamadas al modelo.**
Python se quedó sin pila y lanzó `RecursionError` a profundidad 327 — hasta ahí, lo
apostado. Lo que no se apostó es lo que pasó después.

🚨 **`RecursionError` es una `Exception`**, así que **la red de seguridad de C.4 se lo
tragó**: la convirtió en un `tool_result` que decía *«el especialista falló por un
defecto interno del programa»*, el modelo obedeció, cerró su turno, y **las 164 capas
de encima cerraron una a una y en verde**. La corrida de arriba devolvió `ok=True`,
`motivo=None` y un texto tranquilo.

🔑 **La red no distingue «se cayó uno de tres» de «el sistema se está comiendo a sí
mismo».** Las dos cosas entran por el mismo `except` y salen con la misma forma de
dato. → `LM.79`.

🚨 **Y del desastre entero quedó UNA línea de registro entre 823.** Existió, quedó
grabado, y estaba a la vista de nadie — porque nadie audita un verde (`LM.15`).

📌 De ahí sale la forma del freno, y es diseño y no gusto: **el freno devuelve un
diccionario, no lanza una excepción.** Una excepción lanzada en la frontera se la come
la propia red que hace posible el problema. Medido con su contrafactual (prueba 23):
el mismo corte como `Exception` corriente → `ok=True` y cinco capas cerradas en verde;
como `BaseException` → el aviso sale. **Es la única diferencia.**

##### ✅ La apuesta 2, exacta: `max_vueltas` cuenta a lo ancho y la pelota crece a lo hondo

40 capas abiertas con `max_vueltas=8` activo en todas, y **ninguna cerró**: `motivos`
vacío del todo. Cada capa nueva **estrena su contador en cero**, así que un freno que
cuenta vueltas dentro de una capa no ve nunca una escalera de capas.

##### ✅ La apuesta 3, y el adjetivo que hubo que corregir con un número

Con el presupuesto repartido de C.2 encendido, la misma pelota murió en **2 capas**.
El freno funcionó: paró, pronto y barato. Y cerró con `motivo="presupuesto"` — verdad
y mentira a la vez: es verdad que se acabó el dinero, es mentira lo que ese motivo da
a entender (*el encargo era caro*). **El encargo no era caro: había un bucle.**

🔑 **De un freno sobrevive el diagnóstico, no la parada.** → `LM.80`.

⚠️ **Pero el adjetivo de la apuesta se midió, y estaba exagerado.** Decía que el
consejo deducido —«dale más presupuesto»— era *«el peor posible»*. Se obedeció:

| presupuesto | capas | motivos |
|---|---|---|
| ×1 ($0,039585) | 2 | `presupuesto` |
| ×10 | 4 | `presupuesto` |
| ×100 | 5 | `presupuesto` |
| ×1000 ($39,58) | **7** | `presupuesto` |

El reparto parte el dinero en cada escalón: **el dinero frena como un logaritmo**, y
nunca deja que la pelota se dispare. **La apuesta acertó en lo falsable y exageró en
el adjetivo, y se deja escrito con el número al lado.**

📌 Y el corolario que sí vale: **el presupuesto sólo frena si se REPARTE hacia abajo.**
Con el tope por pieza de A.2 —cada capa estrenando el suyo— la misma pelota llegó a 40
capas sin una queja.

##### ✅ La apuesta 4: `profundidad` no cuenta capas, y por eso no sirve de tope

```
profundidad 0  ->  capa:coordinador-raiz   <- capa
profundidad 1  ->  tool:delegar
profundidad 2  ->  capa:coordinador        <- capa
```

**Una capa de agente cuesta DOS escalones**: la herramienta y la capa. 40 capas dan
profundidad **78**. Un tope escrito contra `profundidad` permitiría capa y media.

🔑 El árbol de C.1 se dibujó para **leerse después**; este número se pregunta para
**decidir ahora**. El mismo dato no sirve para las dos cosas sin traducirlo, y
traducirlo es `capas_abiertas()`.

##### 🛠️ El freno: son DOS topes, y no miden lo mismo

| tope | pregunta | qué caza |
|---|---|---|
| **repetición** | ¿ya hay una capa con mi nombre abierta encima? | la pelota `A→B→A`, aunque sea cortísima |
| **profundidad** | ¿cuántas capas hay abiertas en total? | la escalera `A→B→C→D…`, aunque no se repita un nombre |

🔑 **El orden importa: primero la repetición.** Las dos pararían la corrida, pero dan
diagnósticos distintos, y el de la repetición es más preciso: dice *estás dentro de ti
mismo*, no *bajaste mucho*. Al revés, una pelota se reportaría como «demasiadas capas»,
que **invita a subir el tope** — y subir el tope de una pelota sólo la hace más cara.

✅ **La apuesta 5, medida sobre la cadena real de B.5** (`orquestador → región →
worker`): con el tope en 3 **pasa sin una queja**; con el tope en 2 **la mata por
profundidad**; y una pelota corta en la misma cadena cae por **repetición** aunque el
tope esté en 9. **Los dos topes hacen falta, y hacen falta separados.**

📌 `TOPE_CAPAS = 3` porque tres es lo que llegó a usar el nivel. **Un tope que mata la
topología más grande que ya corriste no es un freno: es una avería.**

##### 🎁 Y el auditor de C.4 ya veía la pelota sin saber que existía

`traza.auditar_arbol()` sobre el registro de la pelota sin freno: **40 quejas
`nodo_abierto`**, una por capa. Con el freno puesto, **ninguna**. La comprobación se
escribió en C.4 para un worker que se cae a media faena, y caza una recursión que
entonces no existía. 🔑 **Un invariante bien elegido caza cosas que su autor no había
imaginado** — que es lo contrario de un detector escrito para la línea que ya viste.

##### 🐛 Dos errores míos, medidos y dichos

1. **El tope no viajaba hacia abajo.** Los topes entraban por la firma de la frontera,
   y **quien llama a una herramienta es el bucle del agente**, que pasa sólo los
   argumentos que el modelo pidió. En cuanto la corrida bajaba una capa, volvían a su
   valor por defecto. 🔑 **Y cómo se cazó vale más que el fallo: dos experimentos que
   debían diferir dieron el mismo número** —40 capas, profundidad 78, el mismo corte—.
   Es `LM.15` con otra cara: el instrumento ciego no dio silencio, dio **la misma cifra
   dos veces**, que se lee como confirmación. → `LM.81`.
2. **La báscula del escalón contestaba otra pregunta.** `profundidad / capas` dio
   **1,5** — la media entre un salto real de 2 y una cola suelta. Se corrigió midiendo
   la distancia entre capas consecutivas. `LM.17` otra vez: **el cociente contestaba
   una pregunta parecida, y por eso salió creíble.**

##### ⚠️ Y una prueba que no podía fallar, corregida dentro del archivo que va de eso

La prueba 15 nació como `check(..., True, "medido en el experimento 3b")`: una nota con
forma de prueba. **`LM.13` cometido dentro del archivo escrito para `LM.13`.** Ahora
corre el experimento y compara los dos extremos de la tabla.

##### 📊 Lo que deja C.5

| | |
|---|---|
| Código | `recursion.py` (nuevo) · `contexto.py` gana `cadena()` |
| Pruebas | **26 en verde**, y la 11 está verde **comprobando que la apuesta 1 falló** |
| Vigilancia | la prueba 3 exige que `marca()` siga bajando **cinco** campos: `cadena` **no entra al registro**, así que ninguna corrida pagada se movió |
| Suites vecinas | `traza`, `profundidad`, `presupuesto`, `fallos`, `fan_out`, `router`, `supervisor`, `verificador`: verdes |
| Lecciones | `LM.79`, `LM.80`, `LM.81` |
| 💸 Coste | **$0,000000** |

**Abierto, con dueño:**
- 🔲 **El freno nunca se ha visto morder con un modelo de verdad.** Está medido contra
  un modelo que *siempre* delega, que es el peor caso — y el peor caso es lo único
  contra lo que se puede dimensionar un freno, pero **no dice si un modelo real llega
  a hacer esto solo**. Es la misma deuda que `crash_temporal` en C.4.
- 🔲 **La red de C.4 sigue tragándose todo lo que suba desde abajo** (`LM.79`). Hoy se
  midió y se rodeó por fuera; **no se tocó**. Estrecharla es una decisión de diseño con
  su propio riesgo —volvería a matar la tanda entera— y se anota, no se improvisa.


---

#### 🎲 C.6 — LA APUESTA, sellada el **2026-08-23** (sesión 104) **antes de la primera línea de código**

> **El estudiante:** *«iniciemos con C.6 y tomo tus apuestas»* — se sellan las de esta
> terminal tal cual, como en la 97 y la 102.
>
> Lo de abajo se escribió **después de leer el código y antes de tocarlo**. Los tres
> hechos del primer apartado están **contados, no adivinados**: son lecturas de archivos
> que ya existen, cuestan $0,00 y **no contaminan lo apostado** — apostar sobre código
> que no he leído no vale nada, pero contar lo que ya está escrito tampoco es apostar.

##### Los tres hechos leídos (no son apuestas)

| # | Dónde | Qué dice |
|---|---|---|
| 1 | `05b-proyecto/agente.py:155-156` | `PRECIO_ENTRADA` y `PRECIO_SALIDA` son **constantes de módulo**, calculadas UNA vez al importar, con `agente.MODELO` como llave. `costo(usage)` las usa a ellas, **no al modelo de la llamada**. |
| 2 | `orquestador.py:111` · `worker.py:118` | Las dos capas dicen `MODELO = agente.MODELO`. **Un solo modelo arriba y abajo — y no por elección de C.6: por herencia.** |
| 3 | `worker.py:611-618` | La línea `llamada_api` del registro anota `entrada`, `salida`, `costo_usd`, `estimado_usd`, `acumulado_usd`, `stop_reason`… **y no anota `modelo`.** |

##### Las seis apuestas

**🎲 1 — El precio está pegado al MÓDULO, no a la llamada.**
Con `opus-5` arriba y `haiku` abajo, la contabilidad entera del nivel 8 seguirá
facturando **a precio de haiku, sin una sola queja**. Y el error no será aproximado:
será **exactamente 5,0×** en la capa de arriba, que es `opus_entrada / haiku_entrada`.
🔑 Es `LM.15` con otra cara — el instrumento no da un dato falso ruidoso, da uno
**plausible**: ~$0,0046 donde de verdad hubo ~$0,023.

**🎲 2 — El registro NO podrá decirlo después.**
En C.1 (sesión 97) el tercer testigo **ya estaba grabado** y no hubo que añadir nada.
Aquí apuesto **lo contrario**: ninguna línea dice qué modelo hizo esa llamada, así que
**ni siquiera pagando la corrida se podrá auditar cuál costó qué**. 📌 Y el nombre del
archivo —`registro_orquestador_{MODELO}.jsonl`— **mentirá por el mismo motivo**: un
rótulo para dos modelos. El caso simétrico de la 97, y por eso vale medirlo.

**🎲 3 — El presupuesto en dólares es lo único de C.2 que sobrevive intacto… y se cae con la 1.**
`PRESUPUESTO_ORQ_USD = 0.05` está escrito en **la unidad correcta**, así que **no hay
que tocarlo** al cambiar de modelo: el margen pasa de 11× a 2,2× y **no corta**.
🔑 Pero si la 1 gana, ese techo está vigilando **dólares falsos**. Los dos frenos no son
independientes: **el presupuesto solo vale lo que valga la tabla de precios.**

**🎲 4 — `effort` es una palanca de SEGUNDO orden, y va con número.**
`effort: low` no baja la tarifa: baja **cuántos tokens de salida** se producen. Y en un
agente con herramientas la entrada manda, porque **el menú se repaga en cada vuelta**.
Apuesto: `high → low` ahorra **menos del 10 %** de la capa; `opus → haiku` ahorra
**~80 %**. 🚨 Con la trampa ya anotada arriba: `effort` **no funciona en
`claude-haiku-4-5`**, y apuesto que da un **400** y no un silencio — **y que eso es una
suerte**, porque un parámetro ignorado en silencio sería mucho peor que un error.

**🎲 5 — «Modelo caro arriba» NO se puede demostrar con la tarea de hoy, y se va a ver.**
El orquestador de hoy **solo reparte y pega**. Apuesto que subirlo a opus **no cambia ni
una decisión**: mismo fan-out de tres monedas, mismo número de llamadas, y el árbol de
C.1 de las dos corridas saldrá **isomorfo**. Solo cambia la factura. 🔑 Así el README
deja de *afirmar* que ahí pagar opus es tirar dinero y pasa a **medirlo**.

**🎲 6 — La del coste, que es la que falló en la 97.**
Los pasos de código cuestan **$0,00**. El que cuesta es **el que valida**: una corrida
real con opus arriba ≈ **$0,045**, más las pruebas de `effort` en sonnet ≈ **$0,005**.
Horquilla sellada: **$0,045–$0,060 el día entero.**
📌 Y se sella también **el modo de fallo**, porque ya mordió una vez: *contar el coste de
lo que voy a escribir y no el de lo que hace falta para creérmelo.*

##### 🎁 Un dato que juega a favor, encontrado leyendo

La solución de la apuesta 1 **ya está escrita en este repo**, en el único archivo que hoy
usa dos modelos: `juez_duelo.py:50-51` se saca sus propios `PRECIO_ENTRADA` y
`PRECIO_SALIDA` **del catálogo, con su modelo como llave**, precisamente porque no puede
usar los globales. **Nadie lo generalizó.** Es `LM.20` esperando turno: la corrección ya
estaba escrita y nadie la alcanzó.

##### 🔒 Lo que NO se toca en C.6

El duelo corre con **el mismo modelo en los dos lados** (pieza 0.4 del sobre). Nada de lo
que se mida aquí puede cambiar la configuración del duelo: **C.6 se estudia con demos
propias**, no reconfigurando el experimento sellado.

---

#### 📊 C.6 · PASOS 1 y 1b — LO QUE SALIÓ *(sesión 104 · `modelos.py` · **$0,000000**)*

##### Las tres apuestas del paso 1, resueltas

| # | Lo apostado | Resultado |
|---|---|---|
| 1 | el precio está pegado al MÓDULO; el error es exacto | ✅ **5,0000000000×** |
| 2 | el registro no puede decirlo después | ✅ 0 de 191 líneas |
| 3 | el techo en dólares sobrevive… y se cae con la 1 | ✅ las dos mitades |

🚨 **Y lo peor de la apuesta 1 no es el factor: es que la mentira es LIMPIA.** Los tres
modelos del catálogo tienen la salida a **5× la entrada**, así que tarifar mal **escala
toda la factura por una constante**. Las partes siguen sumando el total (prueba 15), el
árbol de C.1 sigue cuadrando hacia arriba con lo que `auditar()` suma en plano, y **todos
los controles internos salen verdes — porque todos usan la misma tabla mala.**
🔑 **No hay segundo testigo posible dentro de la contabilidad.** Es `LM.66` del revés: en
C.1 los dos caminos eran independientes y por eso uno podía desmentir al otro; aquí
comparten la fuente del error y **confirman la mentira en coro**.

🔑 **Y por qué el registro sí lo tenía en C.1 y aquí no, que no es mala suerte:**
`datos.moneda` se grababa porque era **la SALIDA de una herramienta**, y el registro
guarda salidas. El modelo es **una ENTRADA de la petición**, y de la petición el registro
no guardaba nada.

✅ **El techo de C.2 no hay que tocarlo, y el motivo es LA UNIDAD**: está escrito en
dólares, no en tokens ni en llamadas, así que el precio ya va dentro del número. Un tope
en tokens habría que recalcularlo con cada modelo. **La unidad de un freno decide si
viaja o no.** 🚨 Pero se compara contra `gastado_usd`, que salía de `agente.costo()`:
**vería un 9 % donde hay un 46 %.** Los dos frenos no son independientes — **el
presupuesto solo vale lo que valga la tabla de precios.**

##### La tabla, ahora medida sobre 374.217 tokens ya pagados

Reparto real: **arriba 13,6 % · abajo 86,4 %** (la estimación anterior decía 12/88, y
salía de una sola corrida).

| configuración | total | vs. |
|---|---|---|
| todo haiku *(lo medido)* | $0,465889 | 1,00× |
| sonnet arriba + haiku abajo | $0,616585 | 1,32× |
| opus arriba + haiku abajo | $0,767281 | 1,65× |
| haiku arriba + **opus abajo** | $2,028053 | **4,35×** |
| todo opus | $2,329445 | 5,00× |

Subir el ORQUESTADOR a opus: **+$0,30**. Subir los WORKERS: **+$1,56** — **5,2× más**.

##### ⚠️ Un error mío, medido antes de pagar: razoné en tokens y la factura es en dólares

La apuesta 4 decía que el esfuerzo es palanca de segundo orden **«porque la salida es una
fracción pequeña del gasto»**. Medido: la salida es **6,1 % de los tokens** pero
**24,6 % del gasto**, porque cada token de salida cuesta **5×**. La apuesta no está
falsada —predecía el ahorro real, no el techo— **pero su motivo escrito era malo**, y el
techo del esfuerzo es cuatro veces más alto de lo que esa frase sugería.
🔑 **Contar tokens y contar dólares no dan la misma intuición cuando la salida vale 5× la
entrada.** Es `LM.30`: un motivo que suena medido sin estarlo.

##### El paso 1b — el cableado, y nada de lo medido cambió de número

`Capa(modelo, esfuerzo)` entra **por la puerta** en las dos capas, como `reparto` en C.2 y
`contrato` en A.3: `correr_worker(..., capa=)` y `correr_orquestador(..., capa=,
capa_workers=)`. La configuración de abajo **viaja dentro de `contabilidad`**, por el
mismo camino que `reparto` y `encargos` — al modelo no le sube, porque no le sirve para
decidir y le costaría tokens en cada vuelta. `agente.costo()` sale de los dos bucles y
entra `modelos.costo_de(usage, capa.modelo)`. El registro gana `modelo` y `esfuerzo`.

📌 **`None` en todo = la conducta de siempre**, y por eso las siete suites del nivel
siguen verdes con sus números intactos y los `.jsonl` pagados no se tocaron.

##### 🚨 Y el defecto que se llevó el día: escribí una prueba que no podía fallar, en el archivo donde se cuenta esa lección

Las pruebas 12 y 13 del paso 1 se dejaron con esta promesa por escrito: *«se pondrán
ROJAS cuando C.6 se arregle»*. **Se cableó C.6 entero y siguieron verdes.**

La 12 interroga a `agente.costo`, **que nadie tocó** — el arreglo fue dejar de LLAMARLA en
los dos bucles, no cambiarla. La 13 interroga a **191 líneas ya grabadas**, que son
historia. 🔑 **Las dos son ciertas y las dos son inútiles como vigilancia: describen el
mundo de ayer, y el mundo de ayer nunca se pone rojo.** Es la prueba que no podía fallar
de la sesión 103 por segunda vez.

✅ Se quedan —son el registro de las apuestas— **rebautizadas para que digan lo que de
verdad miden**, y sin la promesa. Y se añadieron las **17 a 22**, con un cliente espía que
apunta con qué se le pidió: ésas sí se ponen rojas si alguien deshace el cableado.
🔑 **La 20 es la que mata el agujero**: el mismo gasto de tokens, tarifado a 5× —
$0,010000 con opus contra $0,002000 con haiku—. **Antes del cableado esas dos cifras eran
idénticas, y eso era la apuesta 1 entera.**

##### 📋 Resumen

| | |
|---|---|
| Archivo | `modelos.py` (**22 pruebas** al cerrar el 1b; **23** al final del día) · `worker.py` y `orquestador.py` cableados |
| Apuestas | 1, 2 y 3 ✅ · la 4 con su motivo corregido · 5 y 6 abiertas |
| 💸 Coste | **$0,000000** |

**Abierto, con dueño:**
- 🔲 **El nombre del archivo de registro sigue llevando UN solo modelo.**
  `registro_orquestador_{MODELO}.jsonl` nombra a uno, y en una corrida con dos capas
  distintas las líneas de la otra caen dentro. **Ya no es una ceguera** —desde hoy cada
  línea dice su `modelo`, así que el dato es auditable—, pero **el rótulo puede seguir
  mintiendo** y es `LM.17` con otra ropa: el rótulo del contenedor no describe el
  contenido. *Importancia: media · Urgencia: no bloqueante* — no para el paso 3 porque el
  testigo está dentro; muerde el día que alguien filtre por nombre de archivo en vez de
  por campo.
- 🔲 **`agente.costo()` sigue tarifando con constantes de módulo**, y sigue viva en
  `router.py:298` y `supervisor.py:258`. Hoy no miente, porque esas dos topologías corren
  con una sola capa de modelo — **miente el día que no**. Es el mismo bicho con dos
  dueños que aún no lo saben.
- 🔲 **`recursion.py` no pasa la capa hacia abajo** en `herramienta_delegar`: una pelota
  de agentes correría entera con la configuración por defecto. Gratis de arreglar, y sin
  dueño hasta que C.6 tenga que medirse sobre una cadena.
---

---

#### 💸 C.6 · PASOS 2 y 3 — LA CORRIDA QUE COSTÓ *(sesión 104 · **$0,058556** el día entero)*

##### Las seis apuestas, cerradas

| # | Lo apostado | Resultado |
|---|---|---|
| 1 | el precio pegado al MÓDULO, factor exacto | ✅ **5,0×**, y ahora en factura real |
| 2 | el registro no puede decirlo después | ✅ 0 de 191 líneas |
| 3 | el techo en dólares sobrevive… y se cae con la 1 | ✅ las dos mitades |
| 4 | el esfuerzo es palanca de segundo orden | 🟡 **el número confirma; el instrumento no basta** |
| 5 | el árbol no cambia al cambiar el modelo de arriba | ✅ **6 de 6** |
| 6 | horquilla $0,045–$0,060 | ✅ **$0,058451** |

##### La factura, con cada capa a su precio

```
arriba (opus-5) : $0.024075   (2 llamadas ·  2.445 entrada /  474 salida)
abajo  (haiku)  : $0.021662   (9 llamadas · 17.997 entrada /  733 salida)
TOTAL           : $0.045737   en 20,48 s

🚨 Lo que el harness de AYER habría reportado arriba: $0.004815
   Lo que costó de verdad:                            $0.024075
   Diferencia no vista:                               $0.019260
```

🔑 **Dos llamadas arriba costaron más que nueve abajo.** Es C.6 en una línea, y es la
apuesta 1 vista en una factura y no en un recálculo. → `LM.82`.

##### 🎯 La apuesta 5 sale total: 6 de 6, y por eso la afirmación deja de ser una opinión

Las **seis** corridas de dos capas ya pagadas —todas haiku— y la de hoy con opus arriba
tienen **exactamente la misma forma de árbol**: `((0,1), (1,3), (2,3))`. Cero quejas del
auditor de C.1.

🔑 **El modelo de arriba cambió la factura y no cambió ni una decisión.** El README
*afirmaba* que con un orquestador que solo reparte y pega, pagar opus es tirar dinero;
ahora está **medido**: son $0,019 por corrida a cambio de nada.

🎁 **Y solo hubo que pagar UNA corrida, no dos.** La de haiku estaba pagada desde la
sesión 97, con su árbol grabado. **Comparar contra lo ya pagado fue la mitad del ahorro
del día**, y lo hizo posible C.1 — la única pieza del harness que no se puede añadir hacia
atrás. Hoy se cobró el interés de haberla puesto entonces.

##### 🚨 La trampa del `effort`, vista morder — y la mitad mala salió GRATIS

```
→ claude-haiku-4-5 con effort='low'
   HTTP 400 — "This model does not support the effort parameter."
   💸 $0,000000
→ claude-sonnet-5 con effort='low'   (el control)
   ✅ 15 entrada · 4 salida · $0,000105
```

Se apostó **un 400 y no un silencio**, y salió un 400 que además dice el motivo. Es una
suerte de verdad: un `effort` ignorado en silencio te dejaría creyendo que ahorraste.

🎁 **Una petición rechazada con 400 no se factura** — no hubo tokens que cobrar. Lo único
que se paga es el **control**, y sin él no habría medición: un error podría venir de que
`effort` no exista en haiku **o** de que lo estemos mandando mal. **Un experimento con una
sola celda no distingue la hipótesis del instrumento.**

##### 🟡 Y la apuesta 4 se deja SIN RESOLVER aunque el número la confirme

```
effort=high  · 984 entrada · 227 salida · $0.006357 · tool_use
effort=low   · 984 entrada · 227 salida · $0.006357 · tool_use
Ahorro: 0,0 %
```

Se predijo *«menos del 10 %»* y salió **0 %**: una victoria en el papel y la menos
informativa posible. Un 0 % es compatible con dos mundos —*«llegó y no tenía nada que
recortar»*, porque el turno medido era un despacho puro sin razonamiento, y *«llegó y no
hizo nada»*— y **este experimento no los separa**. → `LM.84`.

⚠️ Es la trampa que este mismo paso nombró, del otro lado: allí un `effort` ignorado te
haría creer que ahorraste; aquí me haría creer **que medí**.

##### ⚠️ Tres errores míos, los tres medidos y dichos con el número al lado

1. **Razoné en tokens y la factura se cobra en dólares.** La apuesta 4 decía «la salida es
   una fracción pequeña del gasto». Es **6,1 % de los tokens** y **24,6 % del gasto**,
   porque cada token de salida cuesta 5×. El motivo escrito era malo aunque la predicción
   no lo fuera.
2. **Escribí una prueba que no podía fallar**, dentro del archivo donde se cuenta esa
   lección. Las 12 y 13 prometían ponerse rojas al arreglar C.6 y no lo hicieron:
   interrogan a una función que nadie tocó y a 191 líneas que son historia. **Describen el
   mundo de ayer, y el mundo de ayer nunca se pone rojo.** Entraron las **17 a 22**, con un
   cliente espía; la **20** es la que mata el agujero.
3. **`ESFUERZOS` tenía cuatro valores y son cinco.** Faltaba `xhigh`, escrito de memoria y
   corregido por la documentación — y es el recomendado para trabajo agéntico, o sea **el
   que faltaba era el útil**. 🔑 El modo de fallo iba en la dirección peligrosa: un
   validador con la lista corta **no deja pasar basura, rechaza cosas buenas diciendo que
   son basura**, y con un mensaje que suena a verdad.
4. **El comparador de árboles tomaba «hoy» como la última corrida en ORDEN DE ARCHIVO.**
   Aquí se concatenan dos registros, así que la última del montón era una corrida vieja de
   solo workers: dibujó un árbol de un nodo y lo llamó «hoy». **No dio error** — dibujó una
   tabla correcta con la fila equivocada resaltada. `LM.15` con ropa de índice: **el orden
   de un archivo no es el orden del tiempo**, y solo coinciden mientras haya un archivo.

##### 🎁 Y la corrección del paso 1b resultó ser ELLA MISMA imprecisa — lo dijo una prueba en rojo

Al terminar el paso 1b se corrigió una promesa mía diciendo que las pruebas 12 y 13
*«describen el mundo de ayer, y el mundo de ayer nunca se pone rojo»*. **La 13 se puso roja
en cuanto la corrida pagada tocó el registro**, junto con la 11.

🔑 Y las dos rojas eran **correctas**: el archivo dejó de ser homogéneo. Sumarlo entero y
tarifarlo a precio de haiku había dado exactamente lo grabado durante trece sesiones —
porque **todas las líneas eran de un solo modelo**— y esa suposición no estaba escrita en
ninguna parte. ⭐ **El pasado no cambia; el archivo donde está guardado, sí.** Un dato
histórico solo es inmutable si tiene **cómo separarse de lo que se le añade encima**, y
aquí la marca es la ausencia del campo `modelo` (`antes_de_c6`).

📌 La 13 partida en dos deja las dos mitades a la vista: **`13` — ninguna línea anterior a
C.6 anota el modelo** (la apuesta, 191 líneas) y **`13b` — toda línea posterior SÍ lo
anota** (el arreglo, verde con la primera corrida pagada). Un agujero medido y su tapa, en
renglones separados.

##### 📋 Resumen de C.6

| | |
|---|---|
| Archivos | `modelos.py` (**23 pruebas** · 4 modos) · `worker.py` y `orquestador.py` cableados |
| Lecciones | `LM.82`, `LM.83`, `LM.84` |
| 💸 Coste | **$0,058556** — $0,000105 la trampa · $0,045737 la corrida · $0,012714 el esfuerzo |

**Abierto, con dueño:**
- 🔲 **La apuesta 4 sigue sin medirse de verdad.** Hace falta un turno donde el modelo
  **razone**, no donde despache. *Importancia: media · Urgencia: no bloqueante.*
- 🔲 Las tres deudas del paso 1b siguen en pie: el nombre del archivo de registro,
  `agente.costo()` viva en `router.py` y `supervisor.py`, y `recursion.py` sin pasar la
  capa hacia abajo.
### 🧠 BLOQUE D — Lo compartido

| # | Pieza | La trampa |
|---|---|---|
| ✅ D.1 | **Memoria compartida** entre workers · `compartida.py` (sesión 106) | dos workers escribiendo a la vez sobre el mismo archivo |
| ✅ D.2 | **Skills compartidas** · `skills_compartidas.py` (sesión 107) | el menú entero en cada worker se paga en cada worker |

Se apoya en `memoria.py` y `skills.py` del 6b, que ya existen para una capa.

---

#### 🎲 D.1 — LA APUESTA, sellada el **2026-08-23** (sesión 106) **antes de la primera línea de código**

> **El estudiante:** *«escribe la apuesta, yo me uno a tu apuesta y trabaja en D.1»* — se
> sellan las de esta terminal tal cual, como en la 97, la 102 y la 104. Van **once sesiones
> seguidas** con este orden.
>
> Lo de abajo se escribió **después de leer `memoria.py`, `worker.py`, `orquestador.py`,
> `fan_out.py`, `contexto.py` y `presupuesto.py`, y antes de tocar ninguno**. Los cuatro
> hechos del primer apartado están **contados, no adivinados**: cuestan $0,00 y no
> contaminan lo apostado.

##### Los cuatro hechos leídos (no son apuestas)

| # | Dónde | Qué dice |
|---|---|---|
| 1 | `06b-memoria-skills/memoria.py` (338 líneas) | **No importa `threading`. Cero candados.** Y `guardar_dato()` es un **leer → modificar → escribir** de manual: `cargar_memoria()`, `datos.append(...)`, `_escribir(datos)`. |
| 2 | `memoria.py` → `_escribir()` | Es un `ARCHIVO.write_text(...)`: **trunca y escribe**. Su propia cabecera ya anota la deuda —*«si el programa muere justo aquí, el archivo queda a medias»*— y la solución —*«escribir en un temporal y renombrar»*. **Escrita pensando en morir, no en dos escritores.** |
| 3 | `worker.py:252` | `HERRAMIENTAS_DIVISA = ["tasa", "convertir"]`. **Los workers de hoy no tienen memoria.** No hay nada roto todavía: D.1 tiene que **traer el problema**, no encontrarlo. |
| 4 | `orquestador.py:211` · `worker.py:468` · `contexto.py:65` | El nivel 8 **ya sabe** hacer esto: tres `threading.Lock()`. Pero son **tres objetos distintos**, uno por módulo. Y en `presupuesto.py:823-824` hay `orquestador.REGISTRO = w.REGISTRO`: **un archivo con dos candados.** |

##### Las seis apuestas

**🎲 1 — Un candado no protege un archivo: protege un MÓDULO. Y el caso ya está en el repo.**
El hecho 4 no es la apuesta; la apuesta es qué pasa si lo ejercito. Monto dos hilos, uno
entrando por `orquestador.anotar()` y otro por `worker.anotar()`, sobre el archivo único de
`presupuesto.py`. Apuesto que **con líneas cortas NO se rompe nada** —el `write` de una línea
pequeña sale de un tirón y los dos candados sobran— y que **hay que engordar la línea para
verlo romperse**. ~60 %.
🔑 Si acierto, el titular no es *«está mal»*: es que **el defecto lleva sesiones ahí, y lo que
falta para que muerda no es el candado, es el tamaño.** `LM.13` con una vuelta más — un freno
que no se ve morder es una nota, y este ni siquiera es un freno: son dos cerraduras en dos
puertas de la misma habitación.
📌 Y se sella el modo de fallo: si no consigo romperlo **ni con líneas grandes**, la apuesta
no es «ganada», es **instrumento ciego** — y se dice así.

**🎲 2 — La memoria se rompe de forma DISTINTA al registro, y peor: sin romper el archivo.**
El registro **añade** (`open(..., "a")`); la memoria **lee, modifica y reescribe entera**. Son
dos problemas distintos con la misma etiqueta. Apuesto: dos workers guardando **dos datos
distintos a la vez** dejan un `memoria.json` **perfectamente válido, con un solo dato dentro**.
Sin excepción, sin línea rota, sin aviso — y `cargar_memoria()` lo lee feliz. ~90 %.
🔑 **Un `.jsonl` roto grita; un estado pisado calla.** Por eso el candado del registro **no se
puede copiar y ya**: el de allá evita que dos frases se mezclen, el de aquí tiene que evitar
que una lectura vieja pise una escritura nueva.

**🎲 3 — El `threading.Lock` arregla los hilos y NO arregla nada en cuanto haya dos procesos.**
Un `Lock` es un objeto en la memoria de **un** proceso: dos procesos tienen dos, y ninguno ve
al otro. Apuesto que la misma pérdida de la apuesta 2 **vuelve intacta** con dos `subprocess`,
**con el candado puesto y verde**. ~85 %, y se mide hoy y gratis.
⚠️ Y no es un caso de laboratorio: **el bloque E es exactamente eso** —agentes programados, y
su primera pregunta escrita es *«¿qué pasa si se dispara dos veces?»*. La respuesta de D.1
tiene que aguantar hasta allá o se paga dos veces.

**🎲 4 — El arreglo de verdad son TRES arreglos, no uno, y el repo ya tiene uno escrito con el
riesgo equivocado al lado.**
`_escribir()` propone `os.replace()` para el caso *«el programa muere a media escritura»*.
Apuesto que ese cambio **resuelve además un caso que su comentario no nombra** —el archivo a
medias visto por otro proceso— **y que sigue sin resolver la actualización perdida**, que es la
de D.1. ~80 %. Tres cosas en la misma bolsa de «concurrencia», y tres arreglos:

| El fallo | El arreglo | ¿Lo cubre el candado? |
|---|---|---|
| dos escrituras se entrelazan | candado | sí |
| el archivo se ve a medias | escribir en temporal + `os.replace()` | no |
| una lectura vieja pisa lo nuevo | **releer DENTRO del candado** | no, si el candado se pone mal |

🪤 Y es `LM.67` por segunda vez: en la 97 el comentario de `contexto.py` decía *«a propósito»*
pensando en el **espacio** cuando el peligro estaba en el **tiempo**. Aquí la deuda de
`_escribir()` nombra **la muerte del proceso** cuando el peligro es **el proceso de al lado**.
🔑 **Un motivo escrito blinda la decisión contra el siguiente lector — incluso cuando el motivo
apunta al riesgo equivocado.**

**🎲 5 — «Memoria compartida» es una decisión de PRODUCTO, y se va a colar disfrazada de plomería.**
Hoy la decisión 1 de la sesión 18 dice: *«solo el PERFIL: hechos estables sobre el usuario»* —
un agente, una persona. Apuesto que en cuanto tres workers escriben ahí, el archivo deja de ser
*«lo que sé del usuario»* y se vuelve *«lo que sabe el equipo»*, y que esa política **no
sobrevive el contacto sin una regla nueva de quién puede escribir qué**. ~75 %.
📌 Falsable y con fecha: si al cerrar D.1 el archivo tiene **la misma forma y la misma
política** que hoy, la apuesta falló y se dice.
🔑 El `TOPE = 8` es la prueba barata: con un escritor es una política de olvido; con tres es
**tres workers desalojándose el trabajo entre ellos**, y el código no cambió una línea.

**🎲 6 — La del coste, que es la que falló en la 97 y la que se cobró en la 105.**
D.1 es Python plano: abrir archivos, hilos, procesos. Apuesto **$0,00 en todos los pasos de
código**, y que la única tentación de pagar —*«que un worker de verdad llame a `recordar`»*—
**no hace falta para medir nada de D.1**, porque la carrera ocurre **por debajo del modelo**.
Horquilla sellada: **$0,00–$0,010 el día entero.**
🚨 Modo de fallo sellado, y es literal el de la sesión 105: **creer que correr una suite es
gratis.** `presupuesto.py` y `traza.py` lo son; `pipeline.py` y `linea_base.py` **no** —
`GUIDE.md` §6.e, que costó $0,087297 aprender.

##### 🔒 Lo que NO se toca en D.1

- **`06b-memoria-skills/memoria.py` no se edita.** Es código medido de otro nivel, y su
  `memoria.json` tiene datos de una persona. D.1 trabaja sobre una **copia propia** en
  `08-avanzado/`, con su propio archivo de datos y su propia línea en `.gitignore`.
  🔑 Mismo motivo por el que `worker.py` repitió el bucle en vez de editar `agente.py`: **el
  valor de una medición vieja depende de que su código siga siendo el mismo.**
- El **sobre del bloque 0** sigue cerrado. Nada de D.1 puede cambiar la configuración del duelo.

---

#### 📊 D.1 — LO QUE SALIÓ *(sesión 106 · `compartida.py` · **28 pruebas** · **$0,000000**)*

##### 🚨 EL HALLAZGO DEL DÍA, y ninguna de las seis apuestas lo estaba mirando

`06b/memoria.py` promete, con estas palabras: *«En (b) y (c) NO se borra el archivo. Es
tentador y es un error: el archivo dañado es la única evidencia de qué pasó.»*

**La promesa es del lector. Quien la rompe es el escritor, tres líneas más abajo.**
`guardar_dato()` llama a `cargar_memoria()`, recibe el `[]` que significa *«no pude
leer»*, le añade el dato nuevo y **reescribe el archivo entero**. Medido:

| | El archivo | `cargar` | Lo que devuelve |
|---|---|---|---|
| 3 datos sanos | válido | 3 | — |
| se daña (lo que deja una carrera) | roto | avisa, 0, **y no lo borra** ✅ | — |
| **UNA escritura después** | **válido, con 1 dato** 💀 | 1 | **`(True, "guardado")`** 🟢 |

🔑 **Nadie mintió: las dos funciones hacen exactamente lo que dice su comentario. Lo que
no existía era el comentario que las mirara juntas.** Un archivo puede tener todas sus
piezas correctas y una contradicción entre dos de ellas, y esa contradicción **no vive en
ninguna de las dos**, así que no hay dónde leerla.
⭐ Y explica un número que salió idéntico en las cuatro filas de la tabla de abajo: **«JSON
roto» y «quedó vacío» dieron siempre el mismo valor** (0, 0, 3, 49 sobre 200). No es
casualidad. Cada vez que la carrera rompe el archivo, la defensa escrita para ser prudente
—*«nunca revientes, sigue sin memoria»*— convierte *«esto está dañado»* en *«aquí no había
nada»*. **Una defensa correcta contra UN escritor es un borrador silencioso con dos.**
🪤 Es la cuarta cara de `LM.15`, y la peor: el instrumento ciego no da un dato falso, da
silencio — **y aquí el silencio además limpia la escena.**
📌 Y es `LM.19` con su forma exacta: *la lista de pendientes dice qué falta por construir,
nunca dijo qué falta por saber.* Las seis apuestas eran una lista. Esto estaba al lado.

##### La medición, con su control al lado

N hilos guardando N datos distintos a la vez, 200 vueltas por fila, `TOPE = 8`:

| hilos | JSON roto | quedó vacío | **datos perdidos** |
|---|---|---|---|
| **2** | 0/200 (0,0 %) | 0/200 | **198/400 (49,5 %)** |
| 3 | 0/200 (0,0 %) | 0/200 | 383/600 (63,8 %) |
| 6 | 3/200 (1,5 %) | 3/200 | 872/1200 (72,7 %) |
| 12 | 49/200 (24,5 %) | 49/200 | 1310/1600 (81,9 %) |

🚨 **La primera fila es literal la trampa que el temario le puso a D.1** —*«dos workers
escribiendo a la vez sobre el mismo archivo»*— y sale así: **pierden la mitad de lo que
escriben y dejan el archivo perfectamente válido.** Cero excepciones, cero avisos.
🔑 **Un `.jsonl` roto grita; un estado pisado calla.** Y por eso el candado de B.2 no se
podía copiar y ya: allá el síntoma es un archivo ilegible, aquí es uno legible que miente.

Con el arreglo puesto, las cuatro filas dan **0/480 perdidos y 0 archivos rotos**.

##### Las seis apuestas, resueltas

**🔴 APUESTA 1 — FALLADA en su mitad falsable, y el modo de fallo es mejor que la apuesta.**
Aposté que dos candados sobre un archivo **no romperían nada con líneas cortas**. Se rompen:

| candados | relleno | líneas rotas | **registros perdidos** |
|---|---|---|---|
| DOS | 60 B | 0 | **16/2400 (0,67 %)** |
| DOS | 4 kB | 10 | **102/2400 (4,25 %)** |
| DOS | 20 kB | 3 | **77/2400 (3,21 %)** |
| **UNO** | 60 B · 4 kB · 20 kB | **0** | **0/2400 (0,00 %)** |

La mitad que sí acertó: **el tamaño manda** (0,67 % → 4,25 %). La que falló: *«corto es
seguro»*. 🔑 Y hay algo que no aposté y es lo que vale: **el síntoma dominante no son
líneas rotas, son líneas que DESAPARECEN ENTERAS** — con 60 bytes hubo 0 rotas y 16
perdidas. El comentario de `orquestador.py:206` predice el síntoma ruidoso —*«dos líneas se
entrelazan y el `.jsonl` deja de ser `.jsonl`»*— y el que ocurre de verdad es el mudo.
📌 **La fila de UN candado es lo que convierte esto en una medición y no en una anécdota.**
La primera versión del experimento no la tenía, y sin ella *«se rompió»* no dice si fue la
falta de candado o que el experimento apretara de más.

**🟢 APUESTA 2 — GANADA exactamente donde la puse, e incompleta un paso más allá.**
Dije: dos workers → **archivo válido con un solo dato dentro**, sin excepción y sin aviso.
Es la fila 1 de la tabla: 0 % roto, 49,5 % perdido. ⚠️ Pero dije *«sin romper el archivo»*
sin poner número de hilos, y a 12 hilos se rompe el 24,5 % de las veces. **La afirmación
era verdadera en su escala y falsa fuera de ella, y yo no escribí la escala.**

**🟢 APUESTA 3 — GANADA, y con más margen del que pedí.** La misma carrera con procesos:

| modo | qué lleva puesto | **perdidos** |
|---|---|---|
| `ingenuo` | nada | 46/60 (76,7 %) |
| **`solo_hilos`** | **candado de hilos + relectura dentro + escritura atómica** | **48/60 (80,0 %)** |
| `arreglado` | lo anterior **+ candado DE ARCHIVO** | **0/60 (0,0 %)** |

🚨 `solo_hilos` lleva **todo lo que una revisión de código llamaría correcto**, pasa las 18
pruebas de hilos sin despeinarse, y entre procesos **pierde más que no hacer nada**.
🔑 **El modo de fallo peor de este archivo no se ve leyendo el código, ni corriendo las
pruebas que cualquiera escribiría. Solo se ve lanzando dos `python`.** Por eso `P19` está
en la suite aunque tarde 15 s: es la única que puede morderlo.

**🟢 APUESTA 4 — GANADA en las tres partes, y con un cuarto caso que no aposté.**
`os.replace()` resolvió el caso que su comentario nombra (morir a media escritura) **y** el
que no nombra (que otro lo vea a medias), **y no resolvió la actualización perdida** —
`solo_hilos` la lleva puesta y pierde el 80 %. Las tres, como estaban escritas.
🚨 **Lo que no aposté: en Windows `os.replace()` puede NEGARSE.** Si otro proceso tiene el
destino abierto —aunque sea leyéndolo— da `PermissionError [WinError 5]`. Medido: **26 de
60 procesos caídos con traceback**, y los 16 clasificados eran ese error, **sin una sola
excepción de otra clase**. 🔑 **«Atómico» quiere decir «no queda a medias», no «siempre se
puede».** En Linux esto no pasa, y esa es justo la razón por la que hay que decirlo.

**🟢 APUESTA 5 — GANADA. La política de la sesión 18 no sobrevivió al segundo escritor.**
Dije que el archivo dejaría de ser *«lo que sé del usuario»* y que el `TOPE = 8` pasaría de
política de olvido a **workers desalojándose entre ellos**. Las dos cosas: cada dato lleva
ahora `quien`, y el desalojo tiene una **reserva** —no se saca el último dato de un worker
si otro tiene más de uno—.
🔑 **Y la reserva no se inventó hoy: es `RepartoDeEntrada` de C.2 con otro recurso.** Un
recurso compartido y escaso se reparte con una reserva por participante o se lo lleva el
primero que llegue. Que la misma forma sirva para **dólares** y para **renglones de
memoria** es la señal de que era estructura y no un truco del presupuesto.
⚠️ Y su límite queda escrito y probado (`P13`): si los ocho datos son de ocho workers
distintos, la reserva **no se puede cumplir** y sale el más viejo. Prometía un reparto, no
un milagro — igual que C.2 cuando el presupuesto no alcanza.

**🟢 APUESTA 6 — GANADA. $0,000000 el día entero**, dentro de la horquilla $0,00–$0,010.
Ni una llamada al modelo. La carrera ocurre **por debajo** de él, y medirla con un worker
de verdad habría pagado por mirar otra cosa.

##### 📎 Un arreglo mío que se llevó un síntoma y dejó el otro — y se dice

Al ponerle reintentos al `os.replace()`, la columna de **procesos caídos** de `solo_hilos`
pasó de **26/60 a 0/60** y la de pérdidas **no se movió**. El reintento era correcto —cubre
al lector que no pide el candado, que es el hueco que queda incluso con todo bien puesto—
pero hay que decir lo que hizo: **se llevó el síntoma ruidoso y dejó intacto el silencioso.**
🔑 Un `0` en esa columna se lee como *«ya no pasa nada»*, y lo que pasa es que **ya no se
oye**. Tercera vez en el día que la misma forma aparece, y la tercera es mía.

##### 📋 Resumen de D.1

| | |
|---|---|
| Archivo | `compartida.py` — **28 pruebas**, 3 modos (`ingenuo` · `solo_hilos` · `arreglado`) |
| Los cuatro arreglos | candado de hilos · candado **de archivo** · **releer dentro** · `os.replace()` |
| Lecciones | `LM.85`, `LM.86`, `LM.87`, `LM.88` |
| 💸 Coste | **$0,000000** |

**Abierto, con dueño:**
- 🔲 **El candado rancio tiene un supuesto dentro: que nadie tarda 30 s en guardar un
  renglón.** Está escrito en `_CandadoDeArchivo`, no medido. *Importancia: media ·
  Urgencia: no bloqueante.*
- 🔲 **`cargar()` no pide el candado.** Un lector puede ver el estado justo antes de una
  escritura. Para leer un perfil da igual; para decidir sobre él, no. *Importancia: baja ·
  Urgencia: no bloqueante.*
- 🔲 **Ningún worker llama a `recordar()` todavía.** D.1 midió la plomería, que es donde
  estaba el fallo. Cablearlo al `worker.py` es trabajo de D.2 o del bloque F.
  *Importancia: media · Urgencia: no bloqueante.*
- 🔲 **`presupuesto.py:823` sigue apuntando dos candados al mismo archivo.** Hoy no muerde
  porque esas pruebas no corren en paralelo — medido, no supuesto. *Importancia: media ·
  Urgencia: no bloqueante.*

---

---

#### 🎲 D.2 — LA APUESTA, sellada el **2026-08-23** (sesión 107) **antes de la primera línea de código**

> **El estudiante:** *«me uno a tu apuesta y trabajemos en D.2»* — se sellan las de esta
> terminal tal cual. Van **doce sesiones seguidas** con este orden.
>
> Lo de abajo se escribió **después de leer `06b-memoria-skills/skills.py`, sus cuatro
> `.md`, `worker.py`, `orquestador.py` y `fan_out.py`, y después de correr `skills.py` y
> de contar los tokens del último fan-out pagado — y antes de tocar ninguno**. Los cinco
> hechos del primer apartado están **contados, no adivinados**: cuestan $0,00 y no
> contaminan lo apostado.

##### Los cinco hechos contados (no son apuestas)

| # | Dónde | Qué dice |
|---|---|---|
| 1 | `skills.py` corrido hoy | **El menú pesa 1961 caracteres** y los cuatro cuerpos pesan **11 928**. El menú es el **14 %** del conocimiento total… y es el único que **viaja en cada vuelta**. |
| 2 | `skills.py` → `menu_como_texto()` | Su propio comentario ya lo dice: *«esto se paga en CADA vuelta»*. Está escrito pensando en **un agente**. La palabra «worker» no aparece en las 213 líneas. |
| 3 | `registro_workers_*.jsonl`, corrida `c20260823T231228` | El fan-out real son **3 workers × 3 vueltas = 9 llamadas**, con **17 997 tokens de entrada** en total (1828 → 1994 → 2166 por worker). Ese es el denominador contra el que se mide todo lo de abajo. |
| 4 | `worker.py:252` y todo el nivel 8 | **Ningún worker tiene skills.** No hay `leer_skill` en ninguna caja de herramientas. Igual que en D.1: **D.2 tiene que TRAER el problema, no encontrarlo.** |
| 5 | `grep cache_control 08-avanzado/*.py` | **Cero coincidencias.** El nivel 8 entero paga el system prompt completo en cada llamada, trece sesiones seguidas. Y los tres workers comparten `SISTEMA_DIVISA` **carácter por carácter**. |

##### Las seis apuestas

**🎲 1 — El menú repetido cuesta MÁS que todo el conocimiento que reparte.**
El menú existe para no pagar los cuerpos. La apuesta es que en este fan-out **se paga el
truco más caro que la cosa que evita**: 1961 caracteres × 9 llamadas ≈ **17 600 caracteres
de menú**, contra **11 928 de los cuatro cuerpos leídos una vez cada uno**. Si sale,
la frase *«el menú es barato porque es el 14 %»* es verdadera por ficha y **falsa por
corrida**. Se mide gratis, con `count_tokens` y con caracteres. **Pronóstico: sale, y por
encima de 1,4×.**

**🎲 2 — Recortar el menú por worker ahorra poco y reproduce la predicción del SOBRE.**
Lo obvio es copiar `HERRAMIENTAS_DIVISA`: que el worker del dólar vea solo su ficha. Apuesto
**las dos mitades**: (a) el ahorro es **menor del 15 % de la entrada total**, porque el menú
no es lo que domina los 17 997 tokens — las herramientas y el historial sí; y (b) el worker
recortado **pierde exactamente lo que el `SOBRE.md` predijo para las herramientas**: no puede
avisar de una regla que no ve. 🔑 **Es A.3 y A.4 otra vez, y en la capa que nadie miraba:
hasta hoy el aislamiento se había medido en lo que el worker puede HACER; esta es la primera
vez en lo que el worker SABE.**

**🎲 3 — Compartir desde arriba sale MÁS CARO que no compartir, y con este fan-out siempre.**
La solución elegante —que el orquestador lea la skill una vez y baje el cuerpo a los tres
workers— **pierde** cuando los que la necesitan son menos de dos. En el fan-out de divisas
cada worker atiende **una moneda independiente**: o ninguno necesita `normas-cambiarias`, o
la necesita uno. Bajarla a los tres paga **3× un cuerpo que dos tiran**. 🔑 Apuesto que el
punto de equilibrio es **≥ 2 workers que la pidan**, y que este fan-out **nunca lo alcanza**.
Si sale, el titular es feo y útil: **un mecanismo de compartir que en el caso real cuesta
más que la duplicación que venía a arreglar.**

**🎲 4 — El caché de prompt le cambia el signo a las tres anteriores, y por eso las tres
anteriores se miden ANTES de tocarlo.** Los tres workers comparten el system prompt carácter
por carácter (hecho 5). Apuesto que con el menú dentro de un bloque cacheado, **de las 9
llamadas solo la primera lo paga entero** y las otras 8 lo leen barato. ⚠️ Y apuesto también
el borde que lo puede tumbar: **hay un mínimo de tokens por debajo del cual el caché
sencillamente no se activa**, y el system prompt del worker **puede estar por debajo**. Si el
mínimo muerde, la apuesta 4 falla **sin que nadie vea un error** — el caché no da un aviso
cuando no se aplica, da una factura igual. **`LM.15` con forma de descuento que no llegó.**

**🎲 5 — Lo que en D.1 rompía, aquí no rompe — y el motivo es que aquí nadie escribe.**
`leer_skill()` **relee los cuatro archivos del disco en cada llamada**. Apuesto que 12 hilos
llamándola en paralelo dan **0 errores y 0 cuerpos equivocados**, contra el 49,5 % de datos
perdidos que dio la memoria compartida con dos escritores. 🔑 **La asimetría es el titular
del bloque D entero: D.1 era escribir y D.2 es leer, y lo compartido solo duele cuando
alguien lo cambia.** El coste de releer 12 000 caracteres del disco 480 veces **es real y es
invisible**, porque no sale en la factura de la API.

**🎲 6 — Y la deuda que va a aparecer no es de dinero: dos workers de la MISMA corrida
pueden leer versiones DISTINTAS de la misma skill, y el registro no lo dice.**
Nada en `skills.py` fija una versión: cada `leer_skill()` abre el `.md` **otra vez**. Si el
archivo cambia a mitad del fan-out, el worker del dólar y el del euro trabajan con reglas
distintas **y los dos devuelven contratos completos, verdes y coherentes consigo mismos**.
🔑 Es `LM.66` en la capa del conocimiento: **el cuerpo de la skill está SOLO en su renglón —
ningún otro dato del contrato puede desmentirlo.** Apuesto que se puede provocar en una
prueba gratis, y que hoy **no hay dónde leer que pasó**.

##### 🔒 Lo que NO se toca en D.2

- **`06b-memoria-skills/skills.py` no se edita, ni sus cuatro `.md`.** Mismo motivo que
  `memoria.py` en D.1 y que `agente.py` en A.1: es código medido de otro nivel, y **el valor
  de una medición vieja depende de que su código siga siendo el mismo.** D.2 trabaja sobre
  una pieza propia en `08-avanzado/`.
- **El sobre del bloque 0 sigue cerrado.** Nada de D.2 puede cambiar la configuración del duelo.
- **Las apuestas 1, 2 y 3 se miden ANTES de que exista una línea de caché.** Si el caché entra
  primero, los tres números de arriba dejan de ser comparables con las trece sesiones anteriores.

---

#### 📊 D.2 — LO QUE SALIÓ *(sesión 107 · `skills_compartidas.py` · **28 pruebas** · **$0,000000**)*

##### 🚨 EL HALLAZGO DEL DÍA: escribí una comparación que solo podía dar una respuesta

`coste_de_repartir()` existía para decidir la apuesta 3. Devolvía `gana_compartir: False`.

Y lo devolvía **con cualquier número que se le metiera.** Con 1 worker o con 20. Con 1 vuelta o con
20. No porque compartir perdiera: porque la cuenta que escribí **no podía dar la otra respuesta**.

```
vueltas  1 -> compartir  6000   cada uno  3000   gana compartir: False
vueltas  2 -> compartir  9000   cada uno  6000   gana compartir: False
vueltas  8 -> compartir 27000   cada uno 24000   gana compartir: False
vueltas 20 -> compartir 63000   cada uno 60000   gana compartir: False
```

**Faltaba el término que decide de verdad:** pedir una skill **es una llamada a herramienta**, o sea
**una vuelta entera de API** — y una vuelta más re-manda el prompt completo, **1 828 tokens** aquí.
Yo solo estaba comparando cuerpos. Con el término puesto, la cuenta se da la vuelta y **compartir
gana cuando la piden los tres**.

🚨 **No lo vi leyéndola.** Lo cazó `P15` en rojo — una prueba que exigía el resultado contrario en un
caso extremo, y se puso roja *porque el caso extremo tampoco podía darse*.

🔑 Es **`LM.66` en la capa del instrumento**. Allá el defecto era un **dato** solo en su renglón, que
nada podía contradecir; aquí es un **cálculo** solo en su renglón: nada en las entradas puede
moverlo, así que su verde no informa. **Las dos cosas dan el mismo verde que la versión correcta.**
→ `LM.91`, y la pregunta que lo caza no es *«¿está bien la cuenta?»* sino **«¿con qué entradas daría
lo contrario?»**.

📌 Por eso **`P16` no comprueba un resultado: comprueba que la función produce las DOS respuestas**
sobre el rango de entradas. Es la única de las 28 que la versión rota no habría podido pasar.

##### La medición, en la unidad que se factura

| llamadas | menú pagado (tok) | vs cuerpos | *en caracteres* | quién gana |
|---:|---:|---:|---:|---|
| 1 | 622 | 0,15× | *0,16×* | el menú |
| 3 | 1 866 | 0,45× | *0,49×* | el menú |
| 6 | 3 732 | 0,89× | *0,99×* | el menú |
| **7** | 4 354 | **1,04×** | *1,15×* | 🚨 los cuerpos |
| **9** ← el fan-out real | 5 598 | **1,34×** | *1,48×* | 🚨 los cuerpos |
| 18 ← con dos rondas | 11 196 | 2,68× | *2,96×* | 🚨 los cuerpos |

Menú: **622 tokens** (1 961 car.). Los cuatro cuerpos: **4 183 tokens** (11 928 car.).

##### Las seis apuestas, resueltas

**🎲 1 — ✅ en la dirección, 🔴 en el número. Y la unidad me estaba dando la razón.**
El menú repetido **sí** cuesta más que todo el conocimiento que reparte: **5 598 contra 4 183
tokens** en el fan-out real. Pero sellé *«por encima de 1,4×»* y sale **1,34×**. En **caracteres**
habría dado **1,48×** y habría cantado victoria.
🔑 **Los caracteres no se reparten igual entre dos textos:** el menú es prosa larga, los cuerpos
llevan listas, cifras y viñetas, que se parten en más tokens por carácter. → `LM.90`.
⭐ **Y el titular útil no es el 1,34×, es el vuelco: la 7ª llamada.** No hace falta un fan-out para
cruzarlo — **un solo agente con siete vueltas ya lo cruza**. La frase *«el menú es barato, es el
14 % del total»* es verdadera **por ficha** y falsa **por corrida**.

**🎲 2 — ✅ las dos mitades.** Recortar a una ficha deja el menú en **779 de 1 961 caracteres**, y
el worker recortado **deja de ver tres fichas**. El ahorro es real y pequeño contra los ~17 997
tokens de entrada de la corrida. Y reproduce el `SOBRE.md` palabra por palabra: **no puede avisar de
una regla que no ve.**
🔑 **Primera vez que el aislamiento se mide en lo que el worker SABE**, no en lo que puede HACER.
Hasta hoy A.3 y A.4 vivían en la caja de herramientas.

**🎲 3 — 🟡 la mitad correcta, la mitad equivocada, y el arreglo la partió así.**
Aposté *«el equilibrio es ≥ 2 workers, y este fan-out nunca lo alcanza»*. **El equilibrio es 3, y el
fan-out lo alcanza justo en el último escalón posible.**

| la piden | cada uno lee | bajar a todos | gana |
|---:|---:|---:|---|
| 1 | 4 282 | 11 043 | que cada uno lea |
| 2 | 8 564 | 11 043 | que cada uno lea |
| **3** | **12 846** | **11 043** | **compartir** |

🔑 **Y lo que decide no es el cuerpo de la skill: es la vuelta extra.** Con 1 227 tokens de cuerpo,
el que manda es el prefijo de **1 828** que cuesta pedirla. *Un mecanismo de compartir que gana o
pierde por lo que cuesta preguntar, no por lo que pesa la respuesta.*

**🎲 4 — 🔴 la mitad principal FALLA, ✅ y falla exactamente por el borde que sellé con ella.**
El nivel 8 corre en **`claude-haiku-4-5`**, cuyo mínimo de caché es **4 096 tokens**. El prefijo de
un worker son **1 828**. **Faltan 2 268 — y ni sumándole el menú entero llega.** El caché **no se
activaría**, y la API **no lo diría**: se manda el `cache_control`, se acepta, y
`cache_creation_input_tokens` vuelve en 0.

| modelo | mínimo |
|---|---:|
| Opus 5 | 512 |
| Opus 4.8 · Sonnet 5 · Sonnet 4.6 | 1 024 |
| Opus 4.7 | 2 048 |
| **Haiku 4.5** · Opus 4.6 · Opus 4.5 | **4 096** |

🚨 **El mínimo NO baja con la generación.** El mismo prefijo de 1 828 tokens **sí** cachearía en
Opus 5 y **no** en Haiku 4.5 — el modelo más barato tiene el listón **ocho veces más alto**.
🔑 Es `LM.15` con forma de descuento que no llegó: **el instrumento no da un dato falso, da
silencio**, y el silencio se lee como *«ya está cacheado»*. Lo único que prueba que el caché
funciona es leer `usage.cache_read_input_tokens` — **no haber escrito `cache_control`.**

**🎲 5 — ✅ exacta, y es el titular del bloque D entero.**
12 hilos × 40 lecturas = **480 lecturas: 0 errores, 0 cuerpos equivocados.** Donde D.1 perdía el
**49,5 %** escribiendo, D.2 no pierde nada leyendo. Sin un solo candado.
🔑 **Lo compartido solo duele cuando alguien lo CAMBIA.** Cuando nadie lo cambia, no duele:
**cuesta.** Y el coste no desapareció, cambió de sitio — esas 480 lecturas fueron **2 400 aperturas
de archivo**, porque `leer_skill()` relee la carpeta entera para buscar un nombre. Nada se rompe,
nada avisa, **y no sale en ninguna factura porque el disco no manda factura**. → `LM.89`.

**🎲 6 — ✅ y la deuda queda escrita, no escondida.**
Dos lecturas de la **misma** skill dan **cuerpos distintos** si el `.md` cambia entre medias
(`9ca468e0cbf6` ≠ `127a4faf595e`), y **las dos devuelven un cuerpo válido, sin error ni aviso**.
🔑 Es `LM.66` en la capa del conocimiento: **el cuerpo de la skill está solo en su renglón** —
ningún otro dato del contrato puede desmentirlo. `P23` deja la deuda como prueba: **el registro de
hoy no tiene dónde decir cuál se leyó.**

##### 📋 Resumen de D.2

| | |
|---|---|
| Archivos | `skills_compartidas.py` (**28 pruebas** · 2 modos) · `GUIDE.md` §6.e con su fila |
| Lecciones | `LM.89`, `LM.90`, `LM.91` |
| 💸 Coste | **$0,000000** — segunda sesión seguida a cero. `count_tokens` no cobra |

**Abierto, con dueño:**
- 🔲 **Ningún worker lleva skills todavía.** D.2 midió la aritmética, que es donde estaba la
  sorpresa; cablearlo a `worker.py` es del bloque F. *Importancia: media · Urgencia: no bloqueante.*
- 🔲 **La huella de la skill no se anota en el registro** (`P23`). Sin ella no se puede decir si dos
  workers de la misma corrida leyeron lo mismo. *Importancia: media · Urgencia: no bloqueante.*
- 🔲 **El modelo de la apuesta 3 supone que el cuerpo se lee en la primera vuelta.** Si se leyera en
  la segunda, el equilibrio se mueve y no está medido. *Importancia: baja · Urgencia: no bloqueante.*
- 🔲 **`TOKENS_MEDIDOS` es una foto del 2026-08-23.** Si cambia un `.md`, la tabla miente y nada lo
  comprueba. *Importancia: media · Urgencia: no bloqueante.*

### ⏰ BLOQUE E — Agentes programados

**El que se había caído del plan.** Y no es un adorno: es la única parte del nivel
donde **no hay nadie mirando la pantalla**.

| # | Pieza | La pregunta |
|---|---|---|
| E.1 ✅ | **El disparador**: qué lo enciende y en qué ventana corre | ¿qué pasa si se dispara dos veces? |
| E.2 ✅ | **Fallar sin público**: cómo se entera alguien | un fallo mudo a las 3 a.m. no existe hasta la factura |

✅ **El bloque E cerró entero el 2026-08-24** (sesiones 108 y 109): `disparador.py` y `avisador.py`,
105 pruebas entre los dos y **$0,000000**.

📌 Esto ya lo viviste en TEAPP: `D-045` (la ventana horaria), y el ajuste
`stop`/`terminate` que **una pieza automática ejecuta todas las noches sin que nadie
lea nada**. Aquí se estudia como pieza del esquema, no como accidente de la nube.

---

#### 🎲 E.1 — LA APUESTA, sellada el **2026-08-24** (sesión 108) **antes de la primera línea de código**

> **El estudiante:** *«sella por favor y yo tomo esas apuestas, e inicia con E.1»* — se sellan
> las de esta terminal tal cual. Van **trece sesiones seguidas** con este orden, y en la 107 esa
> costumbre además fue la copia de seguridad que salvó `PROGRESO.md`.
>
> Lo de abajo se escribió **después de leer `compartida.py`, `contexto.py`, `orquestador.py` y
> `worker.py`, y después de contar los 1 352 renglones de los ocho `registro_*.jsonl` — y antes
> de tocar ninguno**. Los cinco hechos del primer apartado están **contados, no adivinados**:
> cuestan $0,00 y no contaminan lo apostado.

##### Los cinco hechos contados (no son apuestas)

| # | Dónde | Qué dice |
|---|---|---|
| 1 | `grep` de `schedule`, `apscheduler`, `crontab`, `schtasks`, `systemd` sobre los 19 `.py` | **Cero coincidencias.** No hay disparador en el nivel. **E.1 tiene que TRAER el problema**, igual que D.1 trajo la carrera y D.2 trajo las skills. |
| 2 | `contexto.py:73` → `_corrida_nueva()` | Fecha + 6 caracteres de azar. Garantiza que dos corridas **se distingan**; no garantiza —ni puede— que **solo haya una**. 🔑 El campo que arregló la sesión 97 hace el disparo doble **más invisible**, no menos: dos nombres distintos parecen dos trabajos legítimos. |
| 3 | Los 8 `registro_*.jsonl`, **1 352 renglones** | Todos llevan `hora` = **cuándo ocurrió**. **Ninguno lleva un campo que diga cuándo DEBÍA ocurrir**, ni a qué disparo pertenece, ni qué turno cubría. Cero campos de ventana. |
| 4 | Corrida `c20260823T231228-c2bdd0`, medida de punta a punta | Un trabajo completo dura **21 s**; las seis corridas con `corrida` van de **7 s a 21 s**. Contra las dos constantes del único candado que cruza procesos (`compartida.py:166-167`): **`ESPERA_MAXIMA_S = 5.0`** y **`CANDADO_RANCIO_S = 30.0`**. **El trabajo dura 4× la espera y el 70 % de la caducidad.** |
| 5 | `LM.87`, medido en la sesión 106 | Cinco procesos con `threading.Lock` pierden el **80 %** — peor que no poner nada (76,7 %); con candado de disco, **0 %**. 🔑 **El bloque E es ese mismo experimento sin nadie que lo provoque:** ahí lancé dos `python` a propósito; aquí los lanza el reloj. |

##### Las seis apuestas

**🎲 1 — El candado que SÍ funciona no sirve para esto, y sus dos constantes ya lo dicen.**
`_CandadoDeArchivo` se escribió para proteger **un renglón** —milisegundos—. Un trabajo dura
**21 s**. Apuesto **las dos mitades**: (a) usarlo tal cual para proteger un trabajo entero hace
que el segundo disparo muera con `CandadoOcupado` **a los 5 s, con el primero todavía
trabajando** — y eso está *bien*, es el comportamiento correcto; pero (b) si el trabajo pasa de
**30 s**, el candado **se declara rancio y el segundo lo rompe solo**, y los dos corren a la vez
**sin un solo error, sin una excepción y sin un renglón que lo diga**.
🔑 **El titular que apuesto: un candado con caducidad convierte «tardar mucho» en «no había
candado».** Se reproduce con un trabajo falso de 35 s. **$0,00, sin API.**
📌 Y si sale, la deuda viva *«el candado rancio de 30 s sin medir»* —abierta en la 106— deja de
ser una nota y pasa a tener un modo de fallo con nombre.

**🎲 2 — «Idempotente» van a ser DOS cosas distintas, y van a hacer falta las dos.**
No solaparse **no es** no repetir el efecto. Apuesto que el candado resuelve solo la primera, y
que el disparo **secuencial** —a las 3:00 falla, a las 3:05 el reloj reintenta— repite el trabajo
entero **sin que el candado se entere**, porque para entonces ya está libre y no queda rastro de
que hubo un primer intento. Hace falta una **marca de trabajo hecho**, que es otra pieza y otro
archivo. Pronóstico: el candado sale **necesario y no suficiente**, y se puede enseñar el renglón
exacto donde deja de servir.

**🎲 3 — La marca de «ya corrí» NO puede llamarse `corrida`, y su requisito es el OPUESTO.**
Apuesto que hay que inventar un identificador nuevo —**el turno**: `2026-08-24T03:00`— y que su
regla es exactamente la contraria a la de `corrida`. `corrida` **tiene que ser única**; el turno
**tiene que repetirse a propósito**, porque solo así el segundo disparo puede preguntar *«¿este
turno ya se hizo?»* y encontrarse a sí mismo. 🔑 **Dos identificadores en el mismo renglón con
requisitos opuestos, y confundirlos es el bicho entero.**

**🎲 4 — El disparo que NO ocurre es peor que el doble, y hoy es literalmente indetectable.**
Apuesto que con los ocho registros de hoy **se puede escribir en código** «esto se disparó dos
veces» —basta contar corridas— **y NO se puede escribir** «esto no se disparó», ni con trampas,
porque **un disparo que no ocurrió no deja renglón** y ningún archivo dice cuándo se le esperaba.
Es `LM.15` con forma de calendario: el instrumento no da un dato falso, **da silencio**, y seis
días parado se ven igual que seis días perfectos. Pronóstico: la comprobación necesita un dato que
**no existe en ninguno de los 1 352 renglones**, y por eso E.1 tiene que escribirlo.

**🎲 5 — El disparo doble no pone roja NI UNA de las pruebas que ya existen.**
Hoy el nivel tiene **292 comprobaciones** contadas en diez archivos (`presupuesto.py` 64,
`traza.py` 47, `compartida.py` 29, `skills_compartidas.py` 29, `recursion.py` 27, `fallos.py` 26,
`modelos.py` 23, `supervisor.py` 20, `profundidad.py` 14, `router.py` 13). Apuesto que **ninguna**
se pone roja cuando el trabajo se dispara dos veces, porque **las 292 corren dentro de un solo
`python`**. Es `LM.87` —*«solo se ve lanzando dos `python`»*— en su forma de recuento, y es un
número que se puede enseñar. ⚠️ **Permiso para fallar sola:** si alguna se pone roja, mejor para
el nivel y peor para la apuesta, y se dice cuál.

**🎲 6 — Va a costar $0,00, y digo AHORA por qué eso es una trampa.**
Tercera sesión seguida a cero: todo lo de E.1 se mide con un trabajo falso, sin una sola llamada
a la API. Pero el modo de fallo real del bloque E **cuesta dinero de verdad** —dos disparos son
dos facturas— y medirlo gratis significa que **el número que más importa, el coste del disparo
doble, va a salir de una multiplicación y no de una medición**. Lo dejo escrito antes de que sea
una excusa: si al cerrar E.1 digo *«y costaría el doble»*, esa frase es **aritmética, no un
dato**, y hay que marcarla como tal. 🔑 Es `LM.66` aplicado por adelantado a mi propia conclusión:
**¿qué otro dato tendría que estar en desacuerdo con este, si estuviera mal?**

##### 🔒 Lo que NO se toca en E.1

- **`compartida.py` no se edita.** Es código medido en la sesión 106, y el valor de aquella
  medición depende de que su código siga siendo el mismo. Si la apuesta 1 sale, la conclusión se
  escribe **aquí**, y el arreglo —si lo hay— vive en la pieza nueva de E.1.
- **`contexto.py` tampoco.** `corrida` se queda como está: el turno es un campo **nuevo**, no una
  reforma del que ya funciona.
- **El sobre del bloque 0 sigue cerrado.** Nada de E.1 puede tocar la configuración del duelo.
- **Ningún registro existente se reescribe.** Los 1 352 renglones son la prueba del hecho 3: si
  les añado el campo que les falta, **borro la evidencia de que faltaba**.


---

---

#### 📊 E.1 — LO QUE SALIÓ *(sesión 108 · `disparador.py` · **67 pruebas** · **$0,000000**)*

Cuatro escalones, cada uno rompiendo al anterior. **Tercera sesión seguida a cero.**

##### 🚨 EL HALLAZGO DEL DÍA: `open(ruta, "a")` NO es atómico entre procesos en Windows

*Importancia: alta · Urgencia: no bloqueante* — hoy no muerde en código pagado, y el
motivo está medido, no supuesto.

El escalón 1 iba a enseñar el trabajo repetido, y lo enseñó. Pero la prueba `P21` —escrita
para comprobar que el coste sale al doble— **se puso roja**, y el motivo era mejor que la
prueba: al solaparse **faltaban renglones del registro**, con **cero líneas rotas y cero
excepciones**. Y la fila secuencial no perdía ninguno: **la pérdida es del solapamiento, no
del trabajo.**

Ahí había dos explicaciones que producen el mismo archivo —el renglón se pierde de camino,
o llega y otro lo pisa— y con renglones del mismo largo son **indistinguibles**. Se separan
con tamaños distintos (`atomico_o_no()`, 800 renglones, dos procesos):

| | |
|---|---:|
| esperados | 800 |
| en el archivo | 754 |
| **MIXTOS** (A y B revueltos) | **0** |
| **de LONGITUD IMPOSIBLE** | **46** → todos de **178** |
| huecos sin escribir | 0 |
| bytes en disco = bytes de lo que queda | ✓ |

🔑 **La huella es el 178.** Un renglón de B ocupa 20 + 2 = 22 bytes; 200 − 22 = 178. Esos 46
renglones son **la cola de una A a la que otro proceso le escribió encima los 22 primeros
bytes**. El renglón llegó al disco y luego lo pisaron.

⭐ **Y la forma del fallo importa tanto como el fallo:** no se entrelazan a mitad de renglón
—cero mixtos—, **se pisan**. Por eso con renglones del mismo largo, que es el caso real de un
`.jsonl`, el pisotón es **exactamente invisible**: ni mixtos, ni longitudes raras, ni huecos.
Solo un renglón que no está. **Es `LM.66` en la capa del sistema de archivos: el renglón
perdido está solo en su renglón, y nada puede desmentirlo.**

⚠️ **Segunda vez que Windows cambia un resultado de este nivel, y en el sentido contrario.**
En `LM.87` Windows **negó** un `os.replace()` que POSIX permite: hizo **ruido** —26 procesos
caídos—. Aquí POSIX garantiza que un `O_APPEND` es atómico y Windows no, así que hace
**silencio**. La misma diferencia de sistema operativo, una vez con traceback y otra sin nada.

📌 **Dónde muerde en código que ya existe:** `orquestador.py:228`, `worker.py:483`,
`router.py:192`, `supervisor.py:120` y `pipeline.py:176` usan ese mismo `open(REGISTRO, "a")`.
**Hoy no muerde, y está medido por qué:** los cinco escriben dentro de un `threading.Lock` y el
fan-out usa **hilos**. Muerde el día que haya **dos procesos** — que es el tema del bloque E.

##### ⚠️ Y la propia `P21` se puso roja sola media hora después de escribirla

Pedía `perdidos > 0` en **una** corrida. La pérdida **no ocurre siempre**: `[0, 2, 2, 0]` en
cuatro rondas, 5,0 % en total. 🔑 **Y esa es la razón por la que un fallo así vive años en un
programa: no se reproduce a la primera, así que el que lo ve una vez concluye que se equivocó.
Una prueba de algo probabilístico tiene que medir la TASA, no el suceso.**

##### 🎲 LAS APUESTAS, UNA POR UNA

**🎲 1 — 🟡 (a) ✅ · (b) 🔴, y el motivo del fallo es mejor que la apuesta.**

| el trabajo dura | espera | rancio | hicieron | cedieron | corridas |
|---|---:|---:|---:|---:|---:|
| 2 s (corto) | 5,0 | 30,0 | **2** | 0 | 2 |
| 8 s (> espera) | 5,0 | 30,0 | 1 | 1 | 1 |
| 35 s (> rancio) | 5,0 | 30,0 | **1** | 1 | 1 |
| 35 s, **espera 60** | 60,0 | 30,0 | **2** | 0 | 2 |

🚨 **FILA 1 — el candado funcionó y no sirvió de nada.** El trabajo dura menos que la espera,
así que el segundo **no se rinde: espera su turno y hace el trabajo entero igual.** Cero
renglones perdidos ✅, dos corridas ❌. 🔑 **Un candado SERIALIZA; no DEDUPLICA.**

🔴 **FILA 3 — la apuesta 1(b) falló.** Sellé que un trabajo de más de 30 s haría que el segundo
rompiera el candado por rancio. **No pasa:** el que espera se rinde a los 5 s y `_rancio()`
**solo se comprueba mientras se espera**. Con `ESPERA_MAXIMA_S (5) < CANDADO_RANCIO_S (30)`, la
caducidad es **inalcanzable** durante un solapamiento.

🚨 **FILA 4 — el bicho de verdad, y es peor.** Un solo cambio: la espera sube de 5 a 60. Ahora
el segundo aguanta hasta los 30 s, declara el candado abandonado **con su dueño vivo y
trabajando**, lo borra y entra. Medido: 66 s, `["hizo","hizo"]`, 0 reventados.
🔑 **El fallo no lo dispara un trabajo largo: LO DISPARA SER MÁS PACIENTE.** Subir la espera
—justo lo que cualquiera haría para arreglar la fila 2— es lo que rompe el candado.

**🎲 2 — ✅ entera.** El disparo **secuencial** repite el trabajo entero sin que el candado se
entere, porque para entonces ya está libre. El candado sale **necesario y no suficiente**, con
el renglón exacto donde deja de servir.

**🎲 3 — ✅ entera.** La marca de «ya corrí» necesita un identificador con el requisito
**opuesto** al de `corrida`: el **turno**, que se repite a propósito porque describe la
**ranura**, no la ejecución. Con él, las tres filas que el candado no podía —incluida la
secuencial— dan **una sola corrida y una sola marca**.
🔑 Y el detalle que enseña la pieza: el segundo **no cede**, se entera de que **ya está hecho**.
`cedio` y `ya_estaba` son estados distintos. **El candado se borra al soltarlo; la marca se
queda.**

**🚨 SEGUNDO HALLAZGO, de la misma familia que el primero.** La marca se guardaba como
`2026-08-24T03:00.json`. En Linux es legal; en Windows los dos puntos **separan el archivo de un
flujo alterno de NTFS**. `dir /r`: `0 bytes 2026-08-24T03` + `73 bytes …json:$DATA`. **Y el
veneno es que funcionaba** —`exists()` encontraba el flujo, `O_EXCL` seguía deduplicando, las
pruebas verdes—. Lo único que fallaba era **listar**: `glob("*.json")` daba **cero** con todas
las marcas puestas, que es justo lo que el escalón 4 necesita. → `_nombre_de_marca()`, vigilado
por `P43`.
⭐ **Un identificador que se usa como nombre de archivo tiene que pasar por una puerta.**

**🚨 LA PREGUNTA QUE NO TIENE RESPUESTA BUENA: ¿marcar ANTES o DESPUÉS?**

| qué le pasa al primer disparo | marcar | se rehace | veredictos |
|---|---|---|---|
| se rompe a mitad | antes | **NO** | `fallo, ya_estaba` |
| se rompe a mitad | después | sí | `fallo, hizo` |
| la máquina se apaga | antes | NO | `murio, ya_estaba` |
| la máquina se apaga | después | **NO** | `murio, cedio` |
| se apaga, **rancio 1 s** | después | **sí** | `murio, hizo` |

🔑 **No existe «exactamente una vez».** Marcar **antes** = *como mucho una vez*: si el trabajo se
rompe, nadie lo reintenta nunca. Marcar **después** = *al menos una vez*: el reintento funciona,
pero **los renglones a medias del primero se quedan**.
⭐ La elección **es del negocio, no técnica**, y hay que hacerla antes: **el que no elige ya
eligió** — el escalón 1 marcaba «después» sin saberlo.

⭐ **Y aquí se entiende por fin para qué sirve `CANDADO_RANCIO_S`:** el que muere no suelta el
candado, y el reintento cede **sin llegar a mirar la marca**. 🔑 **La caducidad no es para el
solape —ahí es inalcanzable—: ES PARA EL CADÁVER.** Y eso ordena los tres números: **mayor que
el trabajo** (o rompes a un vivo) y **menor que el hueco entre disparos** (o el muerto bloquea
el turno siguiente). Hoy: 21 s · 30 s · 3 600 s. **Cuadra por casualidad, y ahora está escrito.**
📌 Eso cierra la deuda «el candado rancio de 30 s sin medir» de la 106: no era un número suelto,
era una **relación entre tres**.

**🎲 4 — ✅ y con el matiz que importa.**

| turno | ¿marca? | intentos | de verdad |
|---|---:|---:|---|
| 03:00 | sí | 1 | salió bien |
| 04:00 | no | 2 | vinieron dos y ninguno pudo |
| 05:00 | no | **0** | **no se disparó nunca** |

«Se disparó dos veces» se escribe contando corridas. **«No se disparó» no se puede escribir con
el registro, porque el que no corre no escribe.** 🔑 **Un registro solo prueba lo que SÍ pasó;
para lo que no pasó hace falta algo escrito ANTES, y es de otra clase: el registro lo escribe el
que trabaja, el calendario lo escribe el que prometió.**
⭐ Y la fila del medio casi se escapa: sin anotar los intentos, «vino y no pudo» se ve igual que
«no vino». **Son tres estados, no dos** — `LM.88` por tercera vez en el día. Por eso
`anotar_intento()` se llama **también cuando el disparo cede**, y con eso queda pagada la deuda
que abrió el escalón 2 (`P65`).

**🎲 5 — 🟡 la letra ✅, el espíritu 🔴, y la diferencia es el hallazgo.**
Medido: los diez módulos del nivel, primero solos y luego **dos procesos a la vez**, arrancados
en el mismo instante. **Cero comprobaciones rojas en las dos columnas** — la letra de la apuesta
se cumple. 🚨 **Pero `traza` reventó 1 de 2 procesos**, y una suite que muere **no reporta rojo:
no reporta nada.** La causa está en código existente: `profundidad.py:594` usa un nombre de
archivo **fijo** en la carpeta del nivel (`_prueba_registro.jsonl`), y dos procesos chocan con
`PermissionError [Errno 13]` — **la misma clase de error de `LM.87`**.
🔑 **Aposté que nada se pondría rojo y acerté por el motivo equivocado: no es que aguanten, es
que ni siquiera llegan a quejarse.** Tercera cara del silencio en un día.
📌 Y el medidor tuvo **tres defectos propios antes de dar un dato**, los tres cazados porque
reventaba también corriendo SOLO: sustituía `sys.stdout` por un `StringIO` (los módulos hacen
`reconfigure()`), pedía `len()` a un valor de retorno que en unos módulos es lista y en otros
booleano, y por eso acabó contando **lo que el módulo imprime**, que es lo único que significa
lo mismo en los diez.

**🎲 6 — ✅ y la trampa que anuncié SE CUMPLIÓ.** $0,000000, sin una llamada al modelo. Y el
coste del disparo doble sigue siendo **una multiplicación, no una medición** — está dicho aquí
porque lo dejé escrito en el sobre antes de poder usarlo como excusa.

##### 📎 Deudas nuevas de E.1

- 🔲 **`profundidad.py:594` usa un nombre de archivo fijo en la carpeta del nivel.** Dos procesos
  corriendo las pruebas chocan con `PermissionError`. *Importancia: media · Urgencia: no
  bloqueante* — solo muerde al correr las pruebas en paralelo, que es lo que hizo la apuesta 5.
- 🔲 **`skills_compartidas.py:586` tiene el `reconfigure()` dentro de `__main__`.** Importarlo y
  llamar a `_pruebas()` revienta con emoji. *Importancia: baja · Urgencia: no bloqueante.*
- 🔲 **Los cinco `open(REGISTRO, "a")` del nivel siguen sin candado de disco.** Hoy no muerden
  —hilos, no procesos—, y el día que E.2 lance un proceso, sí. *Importancia: alta · Urgencia: no
  bloqueante.*
- 🔲 **El disparador no está cableado a ningún agente real.** E.1 midió la mecánica, que es donde
  estaba la sorpresa. *Importancia: media · Urgencia: no bloqueante.*
- 🔲 **El coste del disparo doble no está medido, está multiplicado.** *Importancia: media ·
  Urgencia: no bloqueante.*

---

#### 🎲 E.2 — LA APUESTA, sellada el **2026-08-24** (sesión 109) **antes de la primera línea de código**

> **Catorce sesiones seguidas** con este orden: se sella, se commitea sola, y luego se escribe
> el código. En la 107 esa costumbre además fue la copia de seguridad que salvó `PROGRESO.md`.
>
> Lo de abajo se escribió **después de contar los 1 468 renglones de los ocho `registro_*.jsonl`,
> los 1 108 `print(` de los 19 `.py`, y de leer el `__main__` y el `_pruebas()` de las diez
> suites — y antes de tocar ninguno**. Los seis hechos del primer apartado están **contados, no
> adivinados**: cuestan $0,00 y no contaminan lo apostado.

##### Los seis hechos contados (no son apuestas)

| # | Dónde | Qué dice |
|---|---|---|
| 1 | `grep` de `smtplib`, `sendmail`, `webhook`, `slack`, `telegram`, `twilio`, `requests.post`, `urllib.request` sobre los 20 `.py` | **Cero coincidencias de código.** Los 11 aciertos son la palabra *«avisar»* **dentro de comentarios**. No hay ningún canal de aviso en el nivel: **E.2 tiene que TRAER el problema**, igual que E.1 trajo el disparador. |
| 2 | Los 19 `.py` | **1 108 `print(`. `import logging`: CERO. `sys.stderr`: 4 usos, y los cuatro son `recursion.py:437-458` para SILENCIARLO** (`open(os.devnull)`). 🔑 El único canal del nivel es **la pantalla**, y la única vez que se toca el canal de errores es **para taparlo**. |
| 3 | `disparador.py:1520` y `disparador.py:1533` | `_pruebas()` **devuelve** `fallos` (la lista) y `__main__` **lo llama pelado, descartando el valor**. 🚨 Las **67 comprobaciones en rojo saldrían con código de salida 0** — y es justo el módulo del bloque donde **no hay nadie mirando la pantalla**. |
| 4 | El `_pruebas()` de las diez suites | **Tres convenciones incompatibles de «¿falló?», dos de ellas con la polaridad INVERTIDA:** `return fallos` — lista, truthy = **FALLÓ** — (`compartida`, `disparador`, `skills_compartidas`, `verificador`); `return not fallos` — True = **TODO BIEN** — (`fallos`, `modelos`, `recursion`); `return 0/1` — código de salida — (`router`, `supervisor`, `profundidad`, `traza`). Mismo nivel, misma mano, mismo mes. |
| 5 | Los 8 `registro_*.jsonl`, **1 468 renglones**, **100 nombres de campo distintos** | **Ninguno se llama `nivel`, `gravedad` ni `severidad`.** El único campo que juzga es `ok`, y solo lo llevan **194 renglones (13 %)**. 🔑 Un vigilante que llegara hoy **no tiene por dónde filtrar**: el registro cuenta lo que pasó, no dice cuál de todo eso es malo. |
| 6 | Esos mismos renglones, filtrados a mano | **Ya hay 163 renglones que gritan y llevan días sin que nadie los oiga:** `worker_fin` con `ok:False` × **61**, `contrato_discrepa` × **44**, `sin_trozo` × **58**. ⚠️ Y el matiz que lo hace útil: **la mayoría se provocaron a propósito** (A.3, C.4). **El registro no distingue el fallo provocado del real** — y eso, no la falta de canal, es lo que hace imposible avisar sin ahogar al que recibe el aviso. |

##### Las seis apuestas

**🎲 1 — El canal es lo barato. Apuesto que menos del 10 % del trabajo de E.2 es «mandar el aviso».**
Lo que cuesta está **antes**: qué merece un aviso, a quién, cada cuánto, y qué se hace con el
aviso número 200. Falsificable con una cuenta, no con una impresión: al cerrar E.2 se cuentan las
líneas de la función que **emite** contra las de las que **deciden**. Pronóstico: **1 a 10 o peor.**
🔑 El titular que apuesto: *«no tenemos alertas» casi nunca significa que falte el emisor.*

**🎲 2 — La primera regla que a cualquiera se le ocurre tiene 100 % de falsos positivos, y lo enseño con los renglones que YA existen.**
Un avisador ingenuo —*«un aviso por cada renglón con `ok:False` o `contrato_discrepa` o
`sin_trozo`»*— dispara **163 avisos** sobre los registros de hoy. Apuesto que **ni uno solo**
corresponde a un fallo que nadie supiera: los 163 son experimentos que provoqué yo y cuyo
resultado ya está escrito en este README. ⭐ **Avisar de todo es exactamente igual de mudo que no
avisar**, y aquí sale con un número en vez de con una frase de póster.

**🎲 3 — El MUDO no se puede avisar con el registro, y eso NO es un descuido del registro.**
Es la apuesta 4 de E.1 cobrada en la pieza siguiente. Apuesto que el avisador necesita **dos
entradas de naturaleza distinta** —lo que escribe **el que trabaja** y lo que prometió **el
calendario**— y que si solo se le da el registro, el turno mudo es invisible **por construcción**.
🔑 Y la consecuencia incómoda que apuesto con ella: **el avisador no puede vivir dentro del
proceso que vigila.** El que se murió no manda el aviso de que se murió.

**🎲 4 — El avisador va a tener EL MISMO bicho que vigila: va a fallar mudo.**
Apuesto que la primera versión escrita sin pensar mete el envío en un `try/except: pass` —igual
que `anotar_intento` en `disparador.py:1035`, que ya lo tiene y lo dice— y que entonces **quien
vigila el silencio se queda en silencio**. ⭐ Y apuesto también la salida, para que no valga
inventarla después: **no se arregla con otro `try`.** Se arregla porque **alguien tiene que estar
esperando el aviso**. Un aviso que solo se manda no se puede comprobar; uno que se **espera**, sí.
🔑 Es el **latido**, y es lo contrario de la alarma: **la alarma la manda el que falla; el latido
lo echa de menos el que escucha.**

**🎲 5 — El código de salida 0 de `disparador.py` es un fallo de verdad, y lo demuestro rompiendo una comprobación a propósito.**
Apuesto que con una prueba torcida a mano, `python disparador.py` seguido de `echo $?` da **0**, y
que el mismo experimento sobre `router.py` da **1**. Dos módulos del mismo nivel, la misma mano,
la misma semana, **resultado opuesto ante el mismo fallo**. ⚠️ **Permiso para fallar sola:** si da
1, la apuesta cae, y mejor para el nivel. 📌 Y el orden importa y queda escrito aquí: **primero se
mide, después se arregla.** Al revés se pierde el dato y queda la anécdota.

**🎲 6 — Va a costar $0,00 otra vez, y esta vez la trampa es OTRA y es peor que la de E.1.**
Cuarta sesión seguida a cero. Pero E.2 trata de **a quién se avisa**, y el destinatario real es
una persona a las 3 de la mañana. Apuesto que **todo** lo que se mida hoy será sobre el **emisor**
—¿se generó el aviso?, ¿llegó al archivo?, ¿con qué texto?— y **nada** sobre el **receptor**
—¿lo leyó?, ¿a tiempo?, ¿hizo algo?—. Y ese hueco **no se cierra con código**. Lo dejo escrito
antes de que sea una excusa: si al cerrar E.2 escribo *«y así alguien se entera»*, esa frase **no
está medida**, y es justamente la del título del bloque. 🔑 `LM.66` por adelantado contra mi propia
conclusión: **¿qué otro dato tendría que estar en desacuerdo con esta, si estuviera mal?**

##### 🔒 Lo que NO se toca en E.2

- **El `_pruebas()` pelado de `disparador.py:1533` NO se arregla al pasar.** Es **el sujeto** de
  la apuesta 5, no una deuda que corregir de camino. Se mide primero y se arregla después, **en
  ese orden**, o el dato se pierde y queda la anécdota.
- **Ningún registro existente se reescribe.** Los 1 468 renglones son la prueba de los hechos 5 y
  6: si les añado hoy el campo `gravedad` que les falta, **borro la evidencia de que faltaba**.
- **`compartida.py` y `contexto.py` no se editan**, por el mismo motivo que en D.1 y E.1: son
  código medido, y el valor de aquellas mediciones depende de que sigan siendo el mismo código.
- **No se manda un aviso de verdad a ningún sitio.** Ni correo, ni webhook, ni red. El canal se
  simula en disco. ⚠️ Y esto **no es una limitación escondida en una nota al pie: es la apuesta 6
  convertida en regla**, escrita antes de poder usarla como excusa.
- **El sobre del bloque 0 sigue cerrado.**

---


#### 📊 E.2 — LO QUE SALIÓ *(sesión 109 · `avisador.py` · **38 pruebas** · **$0,000000**)*

**Cuarta sesión seguida a cero**, y el bloque E cierra entero. Cinco escalones, cada uno
destapando lo que el anterior daba por hecho.

##### 🚨 EL HALLAZGO DEL DÍA: la gravedad no es una propiedad del renglón

El escalón 1 corrió la regla ingenua sobre los **1 468 renglones reales y pagados** del nivel:

```
163 avisos    ·    NOTICIA: 0    ·    FALSOS POSITIVOS: 100,0 %
```

| origen | avisos | qué era |
|---|---|---|
| PRUEBAS | **155** | lo escribieron las suites del nivel al correr |
| EXPERIMENTO | **8** | fallos provocados a propósito, con su resultado ya escrito en este README |
| NOTICIA | **0** | — |

Y la regla **no está mal**. Sus tres condiciones (`ok:False`, `contrato_discrepa`, `sin_trozo`)
son las únicas señales de problema que el registro sabe dar, porque el hecho 5 del sobre ya había
contado que **ninguno de los 100 nombres de campo dice gravedad**.

🚨 **El 95 % sale de un solo archivo, y el archivo se llama `registro_pruebas_gratis.jsonl`.** El
filtro obvio —*«ignora ese archivo»*— es **una línea** y mata el 95 % del ruido de golpe.
🔑 **Y no sirve: ese filtro no lee un campo, lee un NOMBRE DE ARCHIVO.** Ningún renglón dice de sí
mismo *«soy una prueba»*. La separación entre lo real y lo provocado es un **accidente de cómo se
guardó**, no una propiedad de lo que se guardó — el día que una suite escriba en el registro de al
lado, el filtro se cae y nadie se entera.

⭐ **De ahí sale el titular, y es `LM.92`:** un `ok:False` con motivo `presupuesto` es **idéntico
renglón por renglón** cuando lo provocó una prueba y cuando arruinó la corrida de un cliente. No se
distinguen **porque no son distintos**: lo distinto es el mundo alrededor, y de ese mundo solo
tiene noticia **el que estaba dentro**. La gravedad es una propiedad **del momento en que se
escribió**, y por eso solo se puede escribir *entonces*, nunca deducir *después*.

⚠️ Y el precio, con el número al lado: **los 1 468 renglones ya pagados no tendrán `entorno`
jamás.** No es que sea trabajoso añadírselo — es que añadírselo sería **inventármelo**. `LM.65`
cobrada otra vez, y esta vez sobre un campo de una línea.

📌 **La columna «¿era noticia?» no sale de ningún campo: la puse yo**, leyendo este README. Está
dicho en el código y no escondido, porque es justamente el hallazgo: **el único que sabe si un
renglón era noticia es alguien que ya sabía la respuesta**, y ese alguien es el que no está
despierto a las 3 de la mañana.

##### 🎲 LAS APUESTAS, UNA POR UNA

**✅ 1 — «menos del 10 % del trabajo es mandar el aviso». Sale 6,8 %.**
Contado con `ast` sobre sentencias ejecutables, no sobre renglones: **5 sentencias emiten · 69
deciden**. El pronóstico decía *«1 a 10 o peor»* y salió **1 a 13,8**. ⚠️ Y lo que la cuenta no es,
dicho en el propio informe: **yo elegí qué funciones van en cada columna**, y lo elegí después de
escribirlas. El reparto vive en las listas `EMITEN` y `DECIDEN` del código, para que se pueda
discutir renglón por renglón. 🔑 **Una cuenta cuyo criterio se puede leer se discute; una impresión,
no.** ⭐ **El titular: «no tenemos alertas» casi nunca significa que falte el emisor.** `mandar()`
son nueve renglones y no fue el problema **ni una sola vez** en los cinco escalones.

**✅ 2 — «163 avisos y ni uno era noticia». Sale exacta: 163 y 0.**
Es la tabla de arriba. ⭐ **Avisar de todo es exactamente igual de mudo que no avisar**, y aquí sale
con un número en vez de con una frase de póster. 📌 Y el control que la hace medición y no truco:
`P13` exige que la regla **deje pasar el 89 %** de los renglones. Una regla que marcara todo daría
un 163 igual de redondo y no diría nada.

**✅ 3 — «el MUDO no se puede avisar con el registro». Sale entera, y con su control.**
Tres turnos de una noche: `hecho`, `sin_exito`, y el de las 05:00 que **nadie intentó**. El
avisador que solo lee renglones ve los dos primeros y **no puede ver el tercero** — no por
descuido, **por construcción**: el que no corre no escribe. 🔑 **Hacen falta dos entradas de
naturaleza distinta:** el registro lo escribe **el que trabaja** (lo que sí pasó); el calendario lo
escribe **el que prometió** (lo que debía pasar). **Ningún volumen de la primera produce la
segunda.** ⭐ Y `P23` la hace falsificable: **alargar el calendario mueve los mudos de 1 a 3** sin
tocar un solo renglón. Si el dato saliera del registro, no se movería. 🚨 **Y de ahí sale dónde
tiene que vivir el código: este avisador no puede correr dentro del proceso que vigila.** El que se
murió a las 3:04 no manda el aviso de que se murió.

**✅ 4 — «el avisador tendrá el mismo bicho que vigila: fallará mudo». Sale, y la salida también.**
Con la red caída, la versión con `try/except: pass` manda **0 avisos, 0 errores, ningún rastro**, y
el proceso sale con código 0. **El avisador no se rompió: se calló.** Y el segundo `try` no arregla
nada — **viajaría por el mismo canal caído**. ⭐ **LA ALARMA LA MANDA EL QUE FALLA; EL LATIDO LO
ECHA DE MENOS EL QUE ESCUCHA** (`LM.93`). El latido invierte quién actúa, y por eso las tres
situaciones producen tres quejas distintas:

| situación | qué dice el que escucha |
|---|---|
| `except: pass` | *no late: nunca ha latido — ¿alguien lo arrancó?* |
| latido, red caída | *late mal: vivo, pero 2 avisos no salieron* |
| latido, 3 h sin correr | *no late: el último latido tiene 10 800 s* |

🔑 **La tercera fila es el `MUDO` del escalón 3 aplicado al vigilante**: se comprueba una
**ausencia** contra un **ritmo prometido de antemano**, igual que el calendario promete un turno.
🚨 Y el campo `fallos_envio` es la mitad que casi nadie escribe: **un latido que dice «vivo» pase lo
que pase es un `except: pass` con mejor prensa.** ⚠️ Y lo que esto **no** arregla, dicho en el
informe y no en una nota al pie: alguien tiene que escuchar el latido, y ese alguien puede callarse
también. **La cadena no se cierra con más código — termina fuera, en algo que no controlas.** Cada
capa mueve el silencio un escalón hacia arriba; ninguna lo borra.

**✅ 5 — «`disparador.py` sale 0 y `router.py` sale 1». Medido antes de arreglar nada.**

```
2026-08-24, sesión 109, ANTES del arreglo:
  disparador.py  →  código 0   (`_pruebas()` llamada pelada)
  router.py      →  código 1   (`sys.exit(main(sys.argv[1:]))`)
```

Mismo nivel, misma mano, la misma semana, el mismo fallo: **uno gritaba y el otro decía que todo
había ido bien.** 🔑 Y no era un descuido de estilo: **`disparador.py` es precisamente el módulo
pensado para correr SIN NADIE DELANTE.** Sus 67 comprobaciones en rojo se imprimían en una pantalla
que nadie mira, y lo único que sí llegaba al que lo arrancó —el código de salida— decía **0**.
⭐ **El aviso más barato del mundo ya estaba ahí, y se tiraba en la última línea del archivo. No
hacía falta escribir un canal: hacía falta no tirar el que había.**

**✅ 6 — «$0,00, y la trampa es que todo será sobre el emisor». Las dos mitades se cumplen.**
Cuarta sesión seguida a cero. Y la trampa se cumplió palabra por palabra: **las 38 pruebas miden el
emisor** —¿se generó el aviso?, ¿llegó al archivo?, ¿con qué texto?, ¿se echó de menos el latido?—
y **ni una sola mide al receptor**: si lo leyó, si a tiempo, si hizo algo. 🔑 **Ese hueco no se
cierra con código, y es el del título del bloque.** Queda dicho aquí, donde no puede disfrazarse de
conclusión.

##### 🎁 EL MEDIDOR TUVO DOS VECES EL BICHO QUE VENÍA A MEDIR

La primera versión del escalón 5 dio **código 1 en los dos módulos**, y la apuesta 5 se habría
declarado fallada con un número en la mano. Las dos veces el `1` era un **reventón**, no una prueba
en rojo:

1. `NameError` — sustituí las llamadas a los informes por un nombre inventado (`_nada_`).
2. `ModuleNotFoundError` — copié el módulo a una carpeta temporal, y `router.py` hace
   `sys.path.insert(0, AQUI.parent / "05b-proyecto")`: desde una temporal ese vecino no existe.

🔑 **UN CÓDIGO 1 NO DICE «FALLÓ LA PRUEBA»: DICE «ALGO PASÓ»** (`LM.95`). Y lo cazó **pedirle el
`stderr` en vez de creerle el número** — por eso `codigo_de_salida_con_prueba_rota()` devuelve los
dos, y `P34` exige que el `stderr` esté **vacío** en ambos. ⭐ Sin ese control, el instrumento
habría dado un dato falso con la forma exacta de un dato bueno, que es `LM.66` en la capa del
medidor.

##### ⭐ EL ARREGLO MATÓ A LA PRUEBA QUE LO MIDIÓ

`P31` medía que `disparador.py` salía con **0**. Se arregló `disparador.py` en esta misma sesión —
después de medir, que era la regla escrita en el sobre— y `P31` se puso **roja al instante**.

🔑 **Una prueba que describe el estado roto muere el día que lo arreglas**, y lo que queda es una
anécdota en un README. Por eso `P31` pasó a su forma *«ahora sale 1»* —el 0 medido vive arriba con
su fecha— y entró **`P35`, que es de otra clase: un detector de la FORMA del bicho.** Lee con `ast`
el `__main__` de los **14 módulos con suite** del nivel y pregunta *«¿alguno llama a sus pruebas y
tira el resultado?»*. Hoy: **ninguno**. ⭐ **Es la diferencia entre arreglar un fallo y cerrar una
clase de fallos** (`LM.94`) — este detector es para el archivo que alguien escriba en la sesión 130.
📌 Y `P36` lo obliga a morder sobre un archivo torcido fabricado a propósito: **un detector que
nunca se ve morder es una nota, no un detector** (`LM.13`).

##### 📎 Deudas nuevas de E.2

- 🔲 **Ningún módulo del nivel escribe el campo `entorno`.** E.2 midió que hace falta y lo demostró
  sobre una demo; cablearlo a `worker.py` y `orquestador.py` es del bloque F. *Importancia: alta ·
  Urgencia: no bloqueante* — sin él, cualquier avisador que se conecte mañana vuelve al 100 % de
  falsos positivos del escalón 1.
- 🔲 **El latido no está cableado a ningún proceso real**, igual que el disparador de E.1. Vive en
  `avisador.py` y nadie lo escribe todavía. *Importancia: media · Urgencia: no bloqueante.*
- 🔲 **Nadie escucha el latido.** `echa_de_menos()` existe y funciona; no hay proceso que lo llame
  cada hora. *Importancia: media · Urgencia: no bloqueante* — y la cadena termina fuera del
  repositorio por definición, así que esto no se cierra aquí del todo nunca.
- 🔲 **El escalón 2 y el 3 se miden sobre demos fabricadas**, no sobre renglones pagados. No hay
  alternativa honesta —el campo no existe en ninguno de los 1 468— pero la diferencia de peso con
  el escalón 1 es real. *Importancia: baja · Urgencia: no bloqueante.*
- 🔲 **`_copia_con_prueba_rota()` escribe un archivo temporal DENTRO de la carpeta del nivel.** Se
  borra en un `finally`, pero un `kill -9` a media medición lo dejaría ahí. *Importancia: baja ·
  Urgencia: no bloqueante.*

##### 📋 Resumen de E.2

| | |
|---|---|
| Archivo | `avisador.py`, 1 180 renglones |
| Pruebas | **38, todas verdes**, y el proceso **sale con 1 si alguna se pone roja** |
| Coste | **$0,000000** — cuarta sesión seguida |
| Apuestas | **6 de 6** ✅ |
| Arreglos | `disparador.py` propaga su código de salida (medido antes) |
| Lecciones | `LM.92`, `LM.93`, `LM.94`, `LM.95` |

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
