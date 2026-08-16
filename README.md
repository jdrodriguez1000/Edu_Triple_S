# Edu_TripleS — De cero a agentes de IA en producción

Recorrido práctico para aprender a construir **harnesses** (los arneses que rodean a un
modelo y lo convierten en un agente confiable) empezando desde los fundamentos.

- **Nivel de partida:** principiante en programación.
- **Stack:** Python primero (es el estándar de facto para agentes), luego TypeScript
  en el nivel 6, cuando lleguemos a la parte web/producto.
- **Proveedor:** Claude API (Anthropic).
- **Regla del recorrido:** cada nivel produce algo que *corre* y que puedes tocar.
  Nada de teoría sin código.

---

## Qué es un "harness" (la idea central de todo el curso)

Un modelo de lenguaje (LLM) solo hace una cosa: recibe texto y devuelve texto.
No recuerda, no ejecuta nada, no consulta nada, no verifica nada.

El **harness** es todo el código que tú escribes alrededor:

```
        ┌──────────────── TU HARNESS ────────────────┐
Usuario │  memoria · herramientas · permisos ·        │   ┌─────────┐
  ───►  │  reintentos · límites de costo · logs ·     │──►│  LLM    │
  ◄───  │  validación · evaluación · el bucle         │◄──│ (Claude)│
        └────────────────────────────────────────────┘   └─────────┘
```

Un "agente de IA" **es** un LLM + un harness. Cuando alguien dice "construí un agente",
el 90% del trabajo real fue el harness. Eso es lo que vamos a aprender.

---

## Mapa del recorrido

Cada nivel es una carpeta. Se hacen en orden.

| Nivel | Carpeta | Qué construyes | Concepto nuevo |
|---|---|---|---|
| 0 | `00-setup/` | Entorno funcionando, API key verificada | Entorno virtual, variables de entorno, secretos |
| 1 | `01-primera-llamada/` | Tu primer programa que habla con Claude | Mensajes, roles, tokens, costo |
| 2 | `02-conversacion/` | Chat que recuerda el contexto | Estado, historial, ventana de contexto |
| 3 | `03-primer-agente/` | **Agente del clima** — el bucle de herramientas a mano | Tool use, el bucle agéntico, `stop_reason` |
| 4 | `04-harness-real/` | El mismo agente, pero robusto | Errores, reintentos, timeouts, límites, logs, streaming |
| 5 | `05-evaluacion/` | Medir si tu agente funciona | Evals deterministas, **rúbricas y LLM-as-judge**, defectos intermitentes, regresiones |
| 5b | `05b-proyecto/` | **Proyecto integrador: agente de divisas y TRM**, desde un archivo vacío | Construir sin plantilla: harness + 5 herramientas + evals |
| 6b | `06b-memoria-skills/` | Que tu agente **recuerde** y **sepa cosas** | Memoria persistente, **Skills** (habilidades cargadas a demanda) |
| 6c | `06c-typescript/` | Portar **tu** agente a TypeScript | El mismo modelo mental en otro lenguaje |
| 7 | `07-produccion/` 🌉 | API web + frontend con el agente adentro — **el código vive en otro repo**; aquí está el puente | **Observabilidad**, **seguridad del agente**, auth, costos por usuario, despliegue en **AWS** |
| 8 | `08-avanzado/` | Multi-agente: orquestador y workers | Orquestación, agentes programados, memoria y skills **compartidas** |
| 📌 | `METODO.md` (raíz) | **Al terminar los 8:** el método destilado, para llevárselo a proyectos de verdad | — |

📌 **`METODO.md` es la tarea final del recorrido**, apartada en la sesión 21. Un
archivo **corto** con lo que sobrevive al cambio de proyecto, pensado para
copiarse a un repo nuevo. Va al final por una razón: **para destilar hay que
tener qué destilar**, y el nivel 7 es el que más método nuevo va a aportar.
El detalle completo está en `PROGRESO.md`.

> ⚠️ Y la advertencia que lo hace necesario: **este repo no se exporta tal cual.**
> Sus cuatro archivos de memoria pesan ~445 KB y `PROGRESO.md` es el estado de
> *este* curso. Meterlos en otro proyecto es pagar contexto por historia ajena.
> **Lo reutilizable no son las piezas: es el criterio.**

**Estado actual (2026-08-01):** niveles 0 a 5 cerrados, el 5b también, el
**6b CERRADO** (sus 6 pasos, con sus 46 lecciones escritas) y el **6c
(TypeScript) CERRADO** — sus 7 pasos corridos y medidos, con las lecciones
`L6c.1–L6c.29` escritas y `GUIDE.md` §13. Costó **$0,1084**.

**El nivel 7 arrancó** con su análisis: 5 de 7 piezas, sin escribir código y sin
gastar un centavo. Todo está en **`07-produccion/README.md`** — el proyecto se
construirá en **otro repositorio**, y esa carpeta es el puente.

El proyecto integrador está terminado: 6 herramientas, **121 evals que corren en
$0,00**, un harness con 10 frenos, tres modelos comparados con datos, y una
evaluación con rúbrica y juez que **encontró un defecto real que ningún eval
determinista podía ver** (el agente inventó una tasa de 3.209,64 cuando la
correcta era 3.207,64). El defecto está corregido y verificado.

**Y desde la sesión 19 el agente tiene memoria persistente**, con una copia del
proyecto en `06b-memoria-skills/` (el `05b-proyecto` queda **congelado** como
referencia). Recuerda entre conversaciones distintas, decide él qué guardar,
olvida por antigüedad, y **107 evals más** cubren esa memoria — total **228**.

⚠️ Y el paso 5 dejó una lección cara: **medir el agente con conversaciones de
verdad encontró cinco defectos que 228 evals no podían ver** — respuestas que
llegaban vacías, un agente que decía *"Anotado"* sin anotar, y datos inventados
que no eran números (una tendencia, una fecha). Los cinco están corregidos.

**Y el 6b se cerró con dos cosas más.** El **examen con rúbrica y juez**, que
midió el agente entero en vez de parchearlo conversación por conversación (y
encontró el hueco de *"¿usa lo que recordó?"*, hoy el criterio C9). Y las
**Skills**: el conocimiento de negocio salió del `.py` a cuatro archivos `.md`
que carga a demanda. La prueba de que eso valía la pena: un error de $14 USD del
agente se arregló **editando un `.md`, sin tocar una línea de Python**.

**Lo siguiente es el nivel 7** (producción: API web + frontend). El 6c
(TypeScript) quedó cerrado en la sesión 28.

Vamos avanzando de a uno: cuando termines uno, me dices y construimos el
siguiente.

### ⚠️ El 6b se adelantó al 6 (sesión 18)

El plan decía **6 (TypeScript) → 6b (memoria)**. Se invirtió. La razón no es que
TypeScript sea difícil —**TypeScript no se vuelve más fácil por saber más de
agentes**, son cosas independientes— sino de rendimiento por sesión:

| | Qué enseña |
|---|---|
| Nivel 6 (TS) | **cero conceptos nuevos** de agentes: traduce lo que ya funciona |
| Nivel 6b | **dos conceptos que no están**: memoria persistente y Skills |

TypeScript no se aplaza para siempre: se aplaza **un nivel**. El nivel 7 es la
web, y el navegador solo habla JavaScript. El orden queda: **6b → 6 → 7**.

### Por qué evaluación va antes que TypeScript

En el plan original TypeScript era el nivel 5 y evaluación el 6. Se cambiaron de
puesto por una razón: **evaluar es el concepto difícil del curso**, y aprenderlo
al mismo tiempo que un lenguaje nuevo sería cargar dos cosas nuevas a la vez —
justo lo que este recorrido evita en todos los demás niveles.

Así aprendes a medir en Python, que ya manejas, y TypeScript entra pegado al
momento en que tiene una razón de ser: el nivel 7, donde hay navegador.

---

## Los tres temas que se preguntan siempre

Estos tres aparecen apenas alguien construye un agente de verdad. Están en el
plan, cada uno en su sitio, y ninguno se puede adelantar sin que salga humo.

> 🔄 **Cambiados en la sesión 77, a petición del estudiante.** El tercero era *el
> proyecto integrador* (nivel 5b) — y dejó de ser una pregunta el día que lo
> construyó. Su sitio lo ocupa **seguridad**, que era el único de los tres que no
> tenía lugar en el mapa. Las tres se declaran ahora en cualquier proyecto nuevo
> antes de la primera línea: ver `CLAUDE.md`, `GUIDE.md` §6.b y `LESSONS.md` →
> `LM.48`. La descripción del proyecto integrador **sigue abajo**, intacta.

### Evaluación y rúbricas (nivel 5)

Son dos cosas distintas y por eso se nombran aparte:

- **Evals deterministas** — lo que se comprueba con un `if`: ¿llamó la herramienta
  correcta? ¿respetó el presupuesto? ¿el `stop_reason` fue el esperado?
- **Rúbricas y LLM-as-judge** — lo que **no** tiene una respuesta correcta única:
  ¿está bien escrita? ¿respetó el dialecto? ¿fue útil? Se califica con una escala
  que defines tú, y quien puntúa es otro modelo.
- **Defectos intermitentes** — los que aparecen unas veces sí y otras no. No se
  diagnostican probando una vez: hay que correr lo mismo N veces, contar, **poner
  un control al lado** y mirar los rangos antes de concluir.

**Ya resuelto aquí (sesión 8):** el dialecto rioplatense, que venía abierto desde
el nivel 3. Salía en **12 de 60** corridas (20%, entre 9.9% y 30.1%), y la causa
resultó ser que el modelo elige entre `ponte` / `ponete` / `póngase` — **las tres
son español correcto**. Nunca fue un problema de idioma, sino de *variedad*: por
eso decir "responde en español de Colombia" no lo tocaba.

También se cerró la pregunta madre del curso, abierta desde el nivel 1:
*"¿cómo se prueba algo que nunca responde igual dos veces?"*

### Observabilidad (nivel 7)

**No es lo mismo que evaluación.** La evaluación pregunta *"¿mi agente funciona?"*
antes de soltarlo. La observabilidad pregunta *"¿qué está haciendo ahora mismo?"*
con usuarios reales encima.

El `registro.jsonl` del nivel 4 es el primer ladrillo. El nivel 7 lo convierte en
trazas, métricas, costo por usuario y alertas.

### Seguridad del agente (nivel 7)

Añadido en la **sesión 77**, a petición del estudiante. Era el hueco real del
plan: llevaba todo el curso apareciendo **en pedazos, y siempre cuando algo se
rompía** — los cinco guardrails del nivel 4, la inyección demostrada en vivo del
5b (`L5b.9`), el grupo de seguridad de AWS del nivel 7 (`LM.22`). Nunca tuvo un
sitio que los juntara.

**Son dos cosas distintas con el mismo miedo, y confundirlas es el dolor de cabeza
típico:**

- Un **guardrail** es un **freno** que pones tú, contra accidentes: gasto, bucles,
  respuestas gigantes. No hay enemigo.
- Una **inyección** es un **ataque**: alguien escribe texto a propósito para que
  tu agente haga lo que tú no querías.

Intentar frenar lo segundo con instrucciones al modelo no funciona. La regla es:
**el modelo nunca es la barrera; la barrera vive en tu código, fuera del modelo.**

Aterriza en el nivel 7 porque es el primer sitio donde el agente recibe texto de
desconocidos, con una tarjeta pagando los tokens. **Va después de observabilidad,
por dependencia:** sin registro no puedes ver morder un freno de seguridad.

### El proyecto integrador (nivel 5b)

Todos los demás niveles se **leen y se corren**. Este se **escribe desde un
archivo vacío**, paso a paso, y es el único que no trae código hecho.

Existe porque entender un programa y ser capaz de producirlo no son la misma
habilidad, y hasta el nivel 5 solo se practica la primera.

**Qué se construye:** un agente de divisas y TRM. Convierte entre COP, USD, EUR
y CAD en ambos sentidos, consulta la TRM oficial de Colombia, mira el histórico y
guarda reportes.

**Por qué ese tema y no otro:**

- **Tiene verdad comprobable.** Si el agente dice que 100 USD son 320.580 COP,
  eso se verifica con una multiplicación. Casi ningún agente tiene una respuesta
  correcta contra la cual compararse; este sí. Los evals deterministas del nivel
  5 salen solos.
- **Y también tiene el caso de rúbrica.** *"¿Dijo de qué fuente sacó la tasa?"*
  no se comprueba con un `if`. Las dos mitades del nivel 5 en un mismo proyecto.
- **Dos fuentes que no coinciden, y las dos correctas.** El mercado y la TRM
  oficial de la Superfinanciera dan cifras distintas (medido el 2026-07-28:
  3.215,61 vs 3.205,80). Cuál es "la buena" depende de para qué se pregunta.
- **Trae la trampa central de los agentes:** un modelo puede equivocarse
  multiplicando. **La herramienta calcula; el modelo solo decide a cuál llamar.**

**Las cinco herramientas**, elegidas para que sean de tipos distintos:

| Herramienta | Tipo |
|---|---|
| `obtener_tasa(de, a)` | API en vivo |
| `convertir(monto, de, a)` | cálculo puro, sin red |
| `trm_oficial(fecha)` | API con fecha, fuente autoritativa |
| `historial(de, a, dias)` | serie de tiempo |
| `guardar_reporte(...)` | **escribe en disco → pide permiso** |

**Cómo se trabaja:** formato mixto. Dictado literal en lo mecánico (entorno,
imports, estructura); guiado en lo conceptual (el bucle, los frenos, los evals),
donde primero se dice *qué* y *por qué*, lo escribes tú, y después se compara.

### Memoria persistente y habilidades (nivel 6b)

Añadido en la sesión 7, a petición del estudiante. Cubre dos huecos reales del
plan: **memoria persistente** estaba nombrada de pasada en una celda del nivel 8,
y **Skills** no aparecía en ningún lado.

**Ninguna de las dos es un tema multi-agente**, y por eso no podían quedarse en
el nivel 8:

- **Memoria persistente** es que tu agente recuerde **después de que el programa
  se cierra**. Un solo agente ya la necesita.
- **Skills** son instrucciones y conocimiento empaquetados que el modelo **carga
  solo cuando le hacen falta**. Un solo agente ya las aprovecha.

El multi-agente las *amplifica* (varios workers compartiendo una memoria, varias
skills compartidas), pero aprenderlas ahí sería mezclarlas con orquestación: dos
cosas nuevas a la vez, justo lo que este recorrido evita.

**Memoria persistente cierra además un hueco que venía del nivel 2.** Allí
aprendiste que el historial crece *dentro de una corrida* y hay que recortarlo.
Nadie cubría qué pasa cuando **el proceso termina y todo se pierde**. Es la
continuación natural de esa pregunta.

**Sobre qué se construye:** sobre tu propio agente de divisas del 5b, ya portado
en el 6. No sobre un ejemplo de juguete.

**Por qué justo aquí, antes de producción:** en el nivel 7 el agente pasa a tener
usuarios reales, y "recordar a cada usuario" deja de ser una curiosidad para
volverse un requisito.

### Orquestador y workers (nivel 8)

La idea cabe en una línea:

> **Un orquestador es un agente cuyas herramientas son otros agentes.**

Por eso va al final: no es un concepto nuevo, es el bucle del nivel 3 **anidado**.
Sin haber construido a mano el de una capa, el de dos capas es humo. Y sin el
harness del nivel 4, un orquestador es una máquina de quemar dinero — cada worker
multiplica las llamadas.

---

## Por qué "el agente del clima" en el nivel 3

Porque es el ejemplo mínimo donde el modelo **no puede** responder solo. Claude no sabe
qué temperatura hace ahora mismo en Bogotá — tiene que pedirle a tu código que lo
averigüe. Eso te obliga a construir el bucle agéntico completo:

1. Le das a Claude una lista de herramientas que puede pedir.
2. Claude responde: "necesito llamar `obtener_clima(ciudad="Bogotá")`".
3. **Tu código** ejecuta esa función de verdad (llama a una API del clima).
4. Le devuelves el resultado a Claude.
5. Claude escribe la respuesta final para el usuario.

Ese ciclo de 5 pasos es literalmente cómo funciona Claude Code, Cursor, y cualquier
agente que hayas usado. Cambia la lista de herramientas y cambia el producto.

---

## Cómo trabajar en este repo

```powershell
# Cada nivel se corre desde su propia carpeta
cd 00-setup
python verificar.py
```

Las dependencias y la API key son compartidas (raíz del proyecto), no hay que
reinstalar nada por nivel.

## Costos

Aprender aquí cuesta centavos, no dólares — pero conviene entenderlo desde el día 1.
Se paga por **token** (≈ 0.75 palabras), separado entre lo que envías (input) y lo que
el modelo genera (output).

| Modelo | Input $/1M tokens | Output $/1M tokens | Cuándo usarlo |
|---|---|---|---|
| `claude-opus-5` | $5.00 | $25.00 | El más capaz. Tareas difíciles, agentes, código |
| `claude-sonnet-5` | $3.00 | $15.00 | Buen balance para volumen alto |
| `claude-haiku-4-5` | $1.00 | $5.00 | Barato y rápido. Clasificar, extraer |

Un ejercicio típico de este curso ≈ 1.000 tokens ≈ **menos de un centavo**.
En el nivel 1 vas a imprimir el costo real de cada llamada para que lo veas tú mismo.
