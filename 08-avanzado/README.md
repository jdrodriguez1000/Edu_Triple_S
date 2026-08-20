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

## 📋 EL TEMARIO — las 20 piezas, en 7 bloques

Cada bloque **produce código que corre**. Ninguno es solo lectura.

| Bloque | Qué se estudia | Piezas |
|---|---|:-:|
| **0** | 🔒 El sobre: rúbrica, predicción y línea base — ✅ **CERRADO** (sesión 90) | 4 |
| **A** | Las piezas: worker, orquestador, y el contrato entre capas | 4 |
| **B** | Las topologías: las formas que puede tomar un multi-agente | 5 |
| **C** | El harness a dos capas: lo que impide que explote | 5 |
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
| A.1 | **Worker**: un agente de una capa llamable como función | ¿qué tiene un worker que no tenga tu agente del 5b? |
| A.2 | **Orquestador**: sus herramientas son workers | ¿cómo se le da un agente a otro agente como herramienta? |
| A.3 | **El contrato entre capas** | ¿qué viaja del worker al orquestador, y qué se pierde? |
| A.4 | **Aislamiento de contexto** | ¿por qué cada worker tiene su propia conversación? |

⭐ El descubrimiento de A.1: **un worker no es una cosa nueva.** Es tu `ejecutar_agente`
con otro system prompt y menos herramientas. Media confusión del multi-agente se cae
sola el día que lo ves.

📌 A.3 es la pieza que más respuestas da del nivel: **la frontera entre las dos capas
es un texto.** El worker no le pasa su conversación al orquestador, le pasa un resumen.
Todo lo que no quepa ahí, se pierde.

**Corre:** `worker.py` y `orquestador.py`, en su versión más tonta: un worker, en serie.

---

### 🔀 BLOQUE B — Las topologías

**Este bloque es el que contesta *«cuándo se usa multi-agente»* de verdad**, porque la
respuesta no es sí o no: es *cuál forma*.

| # | Forma | Cuándo tiene sentido |
|---|---|---|
| B.1 | **Pipeline** (en serie): la salida de uno entra al siguiente | pasos que dependen unos de otros |
| B.2 | **Fan-out / fan-in** (en paralelo) | pedazos independientes ← *la tarea del duelo* |
| B.3 | **Router**: elige UN worker, no varios | muchos casos distintos, uno a la vez |
| B.4 | **Supervisor**: el orquestador juzga y reenvía | cuando la primera respuesta puede no servir |
| B.5 | **Profundidad > 2**: un worker que a su vez orquesta | casi nunca — y hay que saber por qué |

**Corre:** las cuatro primeras sobre el agente de divisas, con la misma tarea, para
poder verlas una al lado de la otra.

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
