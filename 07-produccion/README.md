# Nivel 7 — Producción 🌉

> ⚠️ **Este nivel no tiene código aquí.** Es el primero que rompe la forma de los
> demás (`README.md` + script). El código vive en **otro repositorio**, y este
> archivo es el **puente**: dice qué se está construyendo, dónde, y por qué se
> decidió así.
>
> Si abres esta carpeta buscando un `07_script.py`, no falta nada: es a propósito.

**Estado:** 🔨 **TEAPP contesta por la red.** Pasos **0, 1 y 2 cerrados**
(sesión 31). El análisis de las 7 piezas quedó completo en las sesiones 28 y 29.
**$0,00 en las cuatro sesiones.** Última: 2026-08-02.

**Siguiente:** el paso 3 — la pantalla (`index.html` + `app.ts`) contra
`/practice` local. Lo primero que va a fallar es **CORS**.

⚠️ **Pero antes: el paso 2 quedó SIN COMMITEAR en TEAPP.** El `session-closer`
se lanzó y no dejó nada. Ver §7.9.

> 📌 Y eso es deliberado, no lentitud: **en producción lo caro no es teclear. Es
> equivocarse de estructura y darse cuenta con el servidor encendido.**

---

## Dónde vive el proyecto

```
Nombre:   TEAPP  (Teaching English Application)
Ruta:     C:\Users\USUARIO\Documents\Company_TripleS\Test_Edu_TripleS\TEAPP
Repo:     https://github.com/jdrodriguez1000/TEAPP_Aplication  (privado)
Creado:   sesión 30 — 2026-08-02
```

⚠️ **Está FUERA de `Edu_TripleS`**, y eso es el punto: si viviera dentro, el Git
de este repo se lo tragaría y se perdería la separación entera.

📌 **Esta línea se mantiene al día.** Es lo único de este archivo que no puede
quedar desactualizado: es la dirección del proyecto.

## 🔑 Cómo se trabaja: dos terminales

Decisión del estudiante, sesión 30. Cambia el método de aquí en adelante:

| terminal | papel |
|---|---|
| **Edu_TripleS** | **orienta.** Decide, explica, revisa y guarda el porqué |
| **TEAPP** | **construye.** Ahí vive el código y se hacen sus commits |

*"Me dices qué hacer y yo te digo cómo va todo."*

Esta terminal **no construye** en TEAPP — pero **sí lo lee para revisar**, y ahí
está su valor: los tres defectos del paso 1 los encontró la revisión desde aquí,
no quien escribió el código.

📌 Consecuencia: **TEAPP se explica solo.** No lleva ni una referencia al curso
ni vocabulario de niveles. Se le quitó a propósito, para que el proyecto no
dependa de una carpeta que el servidor nunca va a ver.

---

## Qué se va a construir

Un agente para **practicar inglés escrito**, puesto en producción de verdad.

> Escribes una frase en inglés. El agente **cuenta las palabras con Python**,
> **juzga la gramática con el modelo**, te responde en tono positivo, y lleva tu
> marcador — que sigue ahí mañana. En el navegador, con identidad, desde AWS.

**Alcance de la v1** (recortado a propósito del documento original de la idea):

| Entra | Queda fuera de la v1 |
|---|---|
| Nivel A1, tres temas | los niveles A2 a C2 |
| **Escrito** | la voz (*"obligación de hablar"*) |
| 3 herramientas | los 25 temas |
| memoria por persona | preguntas sorpresa y repaso express |

### Por qué esta app y no otra

Se evaluaron dos ideas propias. Ganó la de inglés, por tres razones:

1. **No necesita fuente de datos externa.** Ni llave, ni API de terceros, ni PDFs.
   Probar no cuesta.
2. **El documento de la idea ya estaba diseñado como un agente**, sin saberlo:
   validar longitud = herramienta de Python; juzgar gramática = LLM-as-judge con
   rúbrica; matriz de temas críticos = memoria por persona; conectores por nivel
   = una Skill; feedback en sándwich = el `SYSTEM`.
3. 🔑 **La primera vez que despliegas algo, el dato que pones adentro debe ser el
   más aburrido que tengas.** La otra idea (entendimiento de extractos bancarios)
   habría puesto **extractos reales** en un servidor mientras se aprende a
   asegurarlo. Asegurar un servidor y proteger datos financieros son dos cosas
   nuevas a la vez — justo lo que este curso evita siempre.

📌 La BankApp **no se descartó, se aplazó**: es candidata para después del nivel
8. Y quedó dicho algo que la aclara: su mejor parte —el simulador *"si pagas el
mínimo tardas 8 años"*— es **matemática determinista, no IA**.

---

## El análisis, en seis piezas

### Pieza 1 — Qué cambia al salir de tu máquina

En los 7 niveles anteriores tres cosas fueron ciertas **siempre**: el único
usuario eras tú, el único que podía gastar tu plata eras tú, y si algo se rompía
lo veías en tu pantalla. **Producción es donde las tres dejan de ser ciertas.**

- Pierdes el control de **quién pregunta**.
- Pierdes el control del **gasto**.
- Pierdes **la pantalla**: el agente corre donde nadie está mirando. *Si no lo
  escribiste, no pasó.*

> 🔑 De las tres juntas sale la regla que gobierna el nivel: **la API key jamás
> toca el navegador.** Todo lo que llega al navegador el usuario lo puede leer.

Y la diferencia que da nombre a dos niveles: **el 5 (evaluación) pregunta
*¿funciona?* antes de soltarlo; el 7 (observabilidad) pregunta *¿qué está
haciendo?* con gente encima.** El `registro.jsonl` del nivel 4 fue su primer
ladrillo.

### Pieza 2 — Qué agente va adentro

Se descartó portar el de divisas: el nivel 7 no es sobre el agente, es sobre lo
que lo rodea. **Agente nuevo, de cero, pequeño (2–3 herramientas).**

**De cero no significa igual de grande.** Reconstruir las 9 herramientas del 5b
habría gastado el 80% del nivel repitiendo lo ya sabido, y habría llegado a AWS
sin fuerzas.

### Pieza 3 — La arquitectura

Decisión que estaba **aplazada desde la sesión 18**, ahora tomada: **camino B**.

| | Frontend | Backend |
|---|---|---|
| A (descartado) | Next.js | Next.js (TS) — obligaría a reescribir el agente |
| **B ✅** | TypeScript | **FastAPI (Python)** |

```
   NAVEGADOR                    TU SERVIDOR
                           ┌──────────────────────────┐
   pantalla TS    ──────►  │  FastAPI (el portero)    │
                           │      ▼                   │
   ◄────  respuesta        │  el agente en Python     │
                           │      ▼                   │
                           │  API de Claude 💰        │
                           │  memoria de cada persona │
                           │  skills/*.md · registro  │
                           └──────────────────────────┘
                              ⬆ la llave vive AQUÍ
```

> 🔑 **FastAPI no es un framework de agentes: es un recepcionista.** Recibe texto
> de afuera, llama a una función tuya que ya existía, devuelve el resultado.

### Pieza 4 — Inventario, y los permisos

El permiso interactivo del 5b (`input()` en la terminal) **no se traduce: se
sustituye.** En un servidor no hay teclado — y el problema de fondo no es
técnico: **quien usa la app no es dueño del servidor**, así que no tiene con qué
decidir.

> 🔑 En la terminal el freno preguntaba **en el momento**. En producción el freno
> se escribe **de antemano**: el código decide a qué archivo puede escribir cada
> persona. Es más fuerte, no más débil — y es *denegar por defecto* otra vez.

### Pieza 5 — El costo

**No hay números todavía, y es a propósito.** Se marcan como predicción para
medirlas (`L6c.15`: *un número tiene que venir de una corrida o venir marcado
como estimación*).

| Predicción sin medir | Cómo se comprueba |
|---|---|
| una frase = **2 o 3 vueltas** del bucle | contando en el `registro.jsonl` |
| un tema (20 frases) = **~50 llamadas** | lo mismo |
| el *system* + la Skill se pagan **en cada vuelta** | `count_tokens`, **$0,00** |

🚨 **Lo que sí es nuevo es la FORMA del costo:** hasta hoy fue *una pregunta, una
respuesta, un costo*. Aquí **el gasto no crece con el número de usuarios: crece
con cuánto practican.** Un estudiante aplicado cuesta más que diez perezosos.

**Lo que es gratis:** contar palabras, los frenos, los evals deterministas,
`count_tokens`, y —lo que abarata el nivel entero— **la puerta, la pantalla, la
identidad y el despliegue completos, probados contra un agente falso.** El modelo
se enchufa al final.

### Pieza 6 — AWS, y el reloj que nadie esperaba

**Verificado en la documentación oficial el 2026-08-02.** Fuentes al pie.

🚨 **Lo primero: "12 meses gratis" ya no existe.** Cambió a mediados de 2025.
Es lo que dicen todos los tutoriales, y es lo que yo habría dicho de memoria.
Una cuenta nueva hoy elige entre **dos planes**:

| | **Plan Free** ✅ elegido | Plan Paid |
|---|---|---|
| Créditos | **$100** al abrir + hasta **$100** más por tareas = **$200** | los mismos |
| Duración | **6 meses**, o hasta gastar los créditos — lo primero | no expira |
| ¿Pueden cobrarte? | **nunca, cero** | sí, pasado el crédito |
| Al terminar | 🚨 **la cuenta se cierra sola** | no pasa nada |
| Servicios | solo algunos | todos |

Textual de la documentación:

> *"After your free account plan expires, your account closes automatically, and
> you lose access to your resources and data. AWS retains your content for 90
> days before permanently deleting your account."*

📌 Los **créditos expiran a los 12 meses** de abrir la cuenta, con cualquier plan.

**Por qué esto cambia el proyecto, y no es un detalle de factura:**

> 🔑 **Hasta hoy el tiempo era gratis en este curso.** Un script que no corres no
> gasta. En AWS no: el reloj de 6 meses arranca el día que abres la cuenta,
> corras o no corras el proyecto. **La nube no solo cobra por estar encendida —
> en el plan Free cobra en tiempo.**

> 🚨 **Regla que sale de ahí: NO abrir la cuenta de AWS hasta tener algo que
> subir.** Abrirla "para ir mirando" quema semanas del reloj sin construir nada.

**Decisión: plan Free.** La restricción número uno del proyecto dice *minimizar
factura manda sobre todo lo demás*, y el plan Free hace la factura **imposible**,
no improbable: es el `PRESUPUESTO_USD` del nivel 4 impuesto por AWS en vez de por
tu código. Seis meses alcanzan para el nivel 7 y el 8. Si TEAPP resulta que vale
la pena, se pasa a Paid ya sabiendo lo que gasta.

⚠️ **La API de Claude no es AWS.** Esos créditos **no** pagan a Anthropic. Las
llamadas del agente se siguen pagando aparte, como en todo el curso.

⏳ **Lo que quedó SIN verificar, a propósito:** los límites exactos de los
servicios *Always Free* (cuántas peticiones, cuántos GB al mes). AWS los publica
en una tabla que se arma con JavaScript y no se puede leer desde aquí. **No se
escriben de memoria** — es la lección de las últimas cinco sesiones, y esta misma
pieza acaba de demostrar por qué (habría escrito "12 meses gratis"). Se verifican
el día que se abra la cuenta, en **Billing → Free Tier** de la consola, que
además muestra el consumo real. Mejor evidencia que cualquier página.

**Fuentes (leídas 2026-08-02):**
[aws.amazon.com/free](https://aws.amazon.com/free/) ·
[Choosing a plan (docs)](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier-plans.html) ·
[Blog oficial del cambio](https://aws.amazon.com/blogs/aws/aws-free-tier-update-new-customers-can-get-started-and-explore-aws-with-up-to-200-in-credits/)

---

## Decisiones tomadas

1. **Backend FastAPI + frontend TypeScript** (camino B).
2. **La memoria es por persona**; el conocimiento compartido de la empresa es una
   **Skill**. *Cada cosa ya tiene su archivo; el error sería pedirle a la memoria
   que haga los dos trabajos.*
3. **Cada visita empieza limpia.** Solo sobrevive la memoria, no la conversación.
4. **Los permisos se escriben de antemano**, no se preguntan.
5. **Proyecto nuevo, en repo aparte y privado.**
6. **Dominio:** práctica de inglés escrito, A1, 3 temas, sin voz.
7. **El 6b se congela** como línea base. No se toca.
8. **La pantalla es TypeScript puro** — sin React, sin Next.js, sin Tailwind
   (sesión 29). Las tres razones, en orden de peso:
   - **Next.js trae su propio servidor de Node.** Serían **dos** servidores
     encendidos en AWS en vez de uno, y *la nube cobra por estar encendida*. Con
     TS puro la pantalla son **archivos quietos** (`.html` + `.css` + `.js`).
   - **Una cosa nueva a la vez.** El nivel 7 ya trae cinco (FastAPI, identidad,
     HTTP, AWS, despliegue). React sería la sexta, y es un tema entero.
   - 🔑 **React sin haber sufrido el problema que resuelve no se entiende.**
     Existe para no enloquecer actualizando la pantalla a mano; si nunca lo
     hiciste a mano, parece burocracia sin motivo.

   📌 **Es la única decisión reversible de la lista**, y por eso se toma barata:
   React/Next/Tailwind viven **dentro** de la caja "pantalla". No mueven la
   llave, no tocan FastAPI, no tocan el agente.
   **La señal para que React entre** (v2 o nivel 8): cuando `app.ts` se llene de
   *"borra esto, pinta aquello, esconde lo otro"* y ya no sepas qué hay en
   pantalla. Ese dolor es exactamente el que React quita.

## 🚨 Suposiciones que producción rompe

Las cuatro salieron de **leer el código**, no de teoría. Es la firma del nivel:

> **Producción no rompe el agente. Rompe las suposiciones que el agente tenía
> derecho a hacer.**

| El agente supone… | Por qué es falso en la web |
|---|---|
| que hay **un solo usuario** | `memoria.json` es un archivo: tres personas se pisan |
| que el historial vive en **una variable** | cada petición HTTP es nueva e independiente |
| que **hay alguien tecleando** (`input()`) | en un servidor no hay teclado: se cuelga para siempre |
| que existe **"la corrida"** con su tope | un servidor no termina nunca. El tope va **por persona y por día** |

⏳ **Sin verificar:** cuánto cuesta una frase · cuántas vueltas por frase · qué
da exactamente la capa gratis de AWS · el factor de ahorro del *prompt caching*.

## Restricciones

- **El objetivo máximo es aprender.** Minimizar factura manda sobre todo lo demás.
- La API key **jamás** toca el navegador.
- Herramienta interna, **pero con URL pública** → la identidad es requisito de
  despliegue, no un adorno.
- **La nube cobra por estar encendida, no por uso.** Distinto de todo lo medido
  hasta hoy.
- 🚨 **Antes de encender nada en AWS: alarma de facturación.** Es el
  `PRESUPUESTO_USD` del nivel 4, aplicado a la nube.

---

## Cómo se reparten los archivos entre los dos repos

**La regla, en una línea:**

> 🔑 **Aquí va el porqué y lo que aprendiste. Allá va lo que el programa hace.**
> ¿Dudas? Pregunta: *¿esto seguiría siendo verdad si el proyecto se borra?*
> Si sí, va aquí.

| Repo del proyecto | Repo del curso (este) |
|---|---|
| `CLAUDE.md` — contrato del **producto** | `CLAUDE.md` — contrato del **curso** |
| `README.md` — qué es y cómo se corre | `README.md` — el mapa del currículum |
| **`_persistence/`** (ver abajo) | `PROGRESO.md` — la bitácora del aprendizaje |
| el código, los tests | `LESSONS.md` — las lecciones `L7.x` |
| | `GUIDE.md` — el manual transferible |
| | **`07-produccion/README.md`** — este puente |

`GUIDE.md` y `LESSONS.md` **no se duplican**. Dos copias en dos repos = una de
las dos miente en tres semanas.

### `_persistence/` — la convención del estudiante, adoptada tal cual

Carpeta que él usa en **todos** sus proyectos. Es la memoria de **construcción**
del proyecto — no la memoria de la app funcionando.

| archivo | qué guarda |
|---|---|
| `progress.md` | estado general |
| `tasks.md` | hechas y siguientes |
| `lessons.md` | lecciones del proyecto (**candidatas**) |
| `decisions.md` | decisiones |
| `assumptions.md` | suposiciones |
| `constraints.md` | restricciones |

**Protocolos, escritos en el `CLAUDE.md` de ese repo:**
- **Inicio:** leer `progress.md` + `tasks.md` (y `git log --oneline -5`); los
  otros, a demanda.
- **Cierre:** actualizar siempre `progress.md` y `tasks.md`; los otros, a demanda.

📌 Es el mismo principio de los 4 archivos de la raíz de este repo —*cada archivo
tiene un trabajo, no mezclarlos*— con más grano fino. **Se adopta el suyo.**

**Dos reglas añadidas:**
1. **Las suposiciones se mueren ascendiendo.** Cuando una se comprueba o se
   decide, **sale de `assumptions.md`** y entra en `decisions.md` o
   `lessons.md`. No vive en dos sitios.
2. **`lessons.md` de allá guarda candidatas; `LESSONS.md` de aquí, las que
   sobreviven al proyecto**, numeradas `L7.x` al cerrar el nivel. Es el mismo
   flujo de siempre, con la primera mitad en el otro repo.

**Cuándo viaja algo para acá:** al cerrar cada paso, con una sola pregunta —
*¿esto le serviría a un proyecto distinto?* Y **en la otra dirección no viaja
código**: los diez frenos de `GUIDE.md` §4.c se **releen, no se copian.** Esa es
justamente la prueba que le queremos hacer a estos archivos.

---

## Los dos agentes de sesión (anotados, sin construir)

Idea del estudiante: dos subagentes de Claude Code que ejecuten los protocolos.

**Formato: Markdown en `~/.claude/agents/`** (nivel usuario, porque
`_persistence` es su convención para todos los proyectos). Verificado en la
documentación oficial: `name` y `description` obligatorios; `tools` y `model`
opcionales; el cuerpo es el system prompt.

> 🔑 Un `.md` en `.claude/agents/` **es una Skill del nivel 6b con otro nombre**:
> conocimiento en markdown que un programa carga a demanda. No hay que escribir
> un `.py`: eso sería construir un segundo harness al lado del que ya se usa.

| | modelo | de dónde saca el contenido |
|---|---|---|
| **Inicio** | Haiku | `progress.md` + `tasks.md` + `git log` |
| **Cierre** | Sonnet | **el `git diff`** + un traspaso corto de la sesión principal |

🚨 **La objeción que hay que tener presente: un subagente arranca en frío y no ve
la conversación.** Para el de inicio da igual. Para el de cierre no: lo que hay
que escribir al final del día está en el chat, no en un archivo.

→ **Solución, y deja el protocolo mejor que antes: el agente de cierre escribe
desde la EVIDENCIA (`git diff`), no desde el relato.** No puede escribir *"se
hizo X"* si X no está en el diff.

- **Restringir herramientas:** el de inicio solo `Read` y `Bash`. **Sin `Edit`**
  — un agente que solo informa no tiene por qué poder escribir.
- **La regla para saber si sobra:** *si el traspaso te queda tan largo como los
  archivos, el agente no está ahorrando: estás escribiendo dos veces.*
- **Y no se cree: se mide.** El `usage` de cada llamada, con su modelo, queda en
  el transcript `.jsonl` de la sesión. **Si el ahorro no aparece ahí, no existe.**

📌 Hallazgo de la sesión 28: Claude Code ya escribe un `registro.jsonl` — el
transcript en `~/.claude/projects/<ruta>/*.jsonl`, con el `usage` de cada
respuesta. **Es el registro del nivel 4, llevaba 28 sesiones escribiéndose solo.**
Y enseñó algo nuevo: en una respuesta real de esta sesión, `input_tokens: 2` y
`cache_read_input_tokens: 336.229`. Casi todo es **caché**.

---

## Pieza 7 — El orden de los pasos

La regla que decide el orden entero, y sale de la pieza 5:

> 🔑 **La tubería completa se construye y se prueba con un agente FALSO. El
> modelo se enchufa al final.**

Un *agente falso* es una función de Python que devuelve siempre lo mismo, sin
llamar a Claude. Y la razón de peso **no es el dinero**: es que el modelo es la
única pieza que no responde igual dos veces. Sacarlo del camino mientras
construyes lo demás te quita la variable ruidosa — **es el control del nivel 5**.

| # | Paso | Qué rompe / qué enseña | Costo |
|---|---|---|---|
| **0** | Repo y esqueleto: `git init`, `CLAUDE.md` del producto, `_persistence/` | se monta el protocolo | $0 |
| **1** | El agente en terminal, **falso**. 3 herramientas: contar (Python), juzgar (falso), marcador (archivo) | lo conocido, dominio nuevo | $0 |
| **2** | **FastAPI** encima. Una ruta, local, mismo resultado que el paso 1 | 🚨 muere `input()` | $0 |
| **3** | **La pantalla**: `index.html` + `app.ts` contra FastAPI local | el 6c aplicado | $0 |
| **4** | **Memoria por persona** | 🚨 "un solo usuario" + "historial en variable" | $0 |
| **5** | **Identidad** | requisito de despliegue, no adorno | $0 |
| **6** | **Frenos de producción**: tope por persona y por día, timeouts, permisos de antemano | 🚨 "existe la corrida" | $0 |
| **7** | **AWS.** ⚠️ **alarma de facturación PRIMERO**, luego subir | la tubería entera, falsa | $0 |
| **8** | **Enchufar el modelo.** Se borra el agente falso | 💰 el primero |
| **9** | **Observabilidad y evals** con rúbrica | bajo |

**Hasta el paso 7 —TEAPP en internet, con URL pública— no cuesta un centavo.**

**Dos cosas del orden que no son casualidad:**

1. **El paso 8 cae casi al final.** Si algo falla ahí, la puerta, la pantalla, la
   identidad, la memoria, los frenos y AWS funcionaban ayer. **El sospechoso
   queda solo.**
2. **AWS va en el 7, no en el 1.** Por el reloj de 6 meses de la pieza 6: los
   pasos 0 a 6 se hacen enteros **sin cuenta de AWS**. El día que se abra, ya
   habrá algo que subir.

---

## Pieza 8 — Observabilidad y evals: el paso 9

> Escrita en la **sesión 82**, con lo que dejaron las sesiones **79, 80, 81 y 82**.
> Es la pieza que faltaba: el mapa le asignaba a este puente **la pregunta de
> seguridad** desde la 77, y esa pregunta apareció aquí — no donde se esperaba.

Las piezas 1 a 7 preguntan *cómo se construye*. Esta pregunta algo distinto:
**cómo se sabe qué está pasando cuando ya nadie está mirando la pantalla.**

---

### 8.1 — Un registro se diseña por la pregunta, no por lo que es fácil escribir

El paso 9 no arrancó escribiendo un registro nuevo. Arrancó **interrogando los que
ya existían**: los `registro.jsonl` del nivel 4 y del 5b. Ocho preguntas, **$0,00 y
sin llamar a Claude**.

Contestaron **dos**: cuánto costó, y cuánto tardó en total. Las otras seis
fallaron.

> 🔑 **La regla que salió de ahí:** un registro se diseña por **la pregunta que
> alguien va a hacer el día que algo se rompa**, no por lo que es cómodo escribir
> mientras nada se rompe. Y mientras nadie le haya hecho una pregunta de verdad,
> **es un archivo, no observabilidad**.

Es `LM.13` con otro traje: *un freno que no has visto morder es una nota*. Un
registro que nadie ha interrogado es un archivo con buena intención.

**Y el hallazgo peor fue cuál era el hueco**, encontrado por las dos terminales a
la vez y por caminos distintos —ellos leyendo el `return` de `api.py`, esta
interrogando el archivo—:

> 🚨 **El caso más frecuente de la app —que funcione— no escribía nada.** El
> registro solo hablaba cuando algo iba mal. Así no se puede responder *"¿alguien
> está usando esto?"*, que es la pregunta 1 de cualquier producto.

**Y una salvedad que salvó un titular** (`LM.16`): los 385 s del nivel 4 no eran la
app siendo lenta — era una persona autorizando permisos a mano. **Un registro que
no marca la espera humana entrega un 89% cierto e inútil.**

---

### 8.2 — Repartir el tiempo, y el tropiezo que enseñó más que el reparto

El descenso de modelo (`[D-049]`: Opus 5 → Sonnet 5 → Haiku 4.5) **solo acelera la
parte de Claude**. Sin saber qué fracción del tiempo es Claude, no se puede juzgar
si el descenso sirvió. En una corrida del 5b: **20,7 s de Claude sobre 59 s
totales** — el principio viaja, el número no.

**Esta terminal propuso el reparto equivocado, y el error es la lección.** Propuso
escribir `connect` / `write` / `pool` / `read`, *"porque la arquitectura ya piensa
en fases y el registro no las escribe"*.

Esos cuatro nombres son `anthropic.Timeout(...)`: **un presupuesto que se le
entrega a la librería, no un cronómetro.** Los números **no existen** — `httpx`
devuelve un solo `elapsed`, el total. Comprobado en la librería del disco, no en la
documentación.

> 🔑 **Un tope no es un reloj.** Declarar cuánto se le permite durar a algo no es
> haber medido cuánto duró.

📌 **Y el agravante:** la tabla de las cuatro fases estaba abierta y leída entera.
No fue por no mirar — **se leyó bien y se clasificó mal.**

⚠️ **Y la frase que lo empujó era cierta y venenosa.** *"El registro no las
escribe"* es verdad, y se lee como *"están ahí, solo falta apuntarlos"*. **Una
afirmación verdadera puede mandar a construir algo imposible si el lector completa
la mitad que no dice.**

**El reparto que sí decide resultó más barato que el descartado**, y son **tres
números, no dos**:

| campo | qué mide | por qué hace falta |
|---|---|---|
| `seconds` | lo que espera la persona, de punta a punta | es el número que le importa al usuario |
| `model_seconds` | la llamada a Claude, cronometrada alrededor | es lo único que el descenso de modelo cambia |
| `queue_seconds` | lo que la práctica esperó en la cola antes de empezar | **sin separarla, el descenso parecería inútil cuando el culpable sería la cola** |

El reloj de la ruta arranca **antes** de encolar, a propósito: mide lo que espera la
persona, no lo que tarda el código.

---

### 8.3 — La cuarta pregunta: quién puede leerlo

Las tres preguntas de siempre sobre un dato son *qué se guarda, dónde vive, cuánto
tiempo*. Falta una, y `.gitignore` **no la cubre**:

> 🚨 **¿Quién puede leerlo?**

`data/` está en `.gitignore` y tapado. El flanco abierto es otro: **una frase escrita
por una persona, copiada a mano dentro de una lección como ejemplo.**
`_persistence/` **sí** va a Git, y el repo **es público**. Ninguna herramienta valida
esa prosa.

**Es la clase muda de fallo** — la misma por la que una fecha equivocada viajó a 17
archivos sin que nada se pusiera rojo. De ahí salió **`PI-8`**, y el reparto en tres
filas:

| dónde | qué puede entrar | qué no |
|---|---|---|
| **traza operativa** | la **forma**: cuántas palabras, si acertó, cuánto tardó | **nunca la frase** |
| **material de evals** | frases **inventadas** a propósito (hay 60, elegidas para A1) | cosecha de gente real |
| **`_persistence/`** | decisiones, lecciones, tareas | **ninguna frase de nadie, nunca, ni como ejemplo** |

**Y la tensión evals ↔ privacidad era falsa**, resuelta por secuencia y no por
principio: no hay frases que recolectar, porque la pregunta 1 sigue siendo *"¿alguien
está usando esto?"*. Inventarlas **ya era la práctica y fue buena** — un conjunto de
prueba es una cosecha fija, no una llave abierta.

---

### 8.4 — Los evals: por dónde se empieza, y por qué no por lo que suena a eval

La rúbrica del tutor le pide **siete** cosas al modelo. Tres necesitan que **una
persona** lea la respuesta y opine: *¿acertó el veredicto? ¿corrigió un error o
tres? ¿se fue del tema?*. Las otras cuatro **las comprueba un programa sin opinar**.

**Se empezó por las cuatro mecánicas, y eso parece lo cómodo. No lo es:**

> 🔑 **Un modelo pequeño no deja de ver que una frase A1 está mal** —eso es gramática
> de primer año—. **Lo que se le va es la forma.** Y la forma **sale a la pantalla**,
> porque la web pinta ese texto tal cual.

📌 **Y por el camino apareció un agujero que vale más que el eval:** cuando el modelo
rompe el formato, el código hacía lo correcto —no dar el punto— **pero no se lo
contaba a nadie**. La traza escribía `correct: bool`, así que *"el juez rompió el
formato"* y *"el alumno se equivocó"* llegaban al cuaderno **como el mismo
`correct=False`**.

Dos causas opuestas, un número, y arreglos en direcciones contrarias: uno va a la
rúbrica, el otro a la clase de inglés. **Es `LM.15` dentro del paso que se llama
Observabilidad: no da un dato falso, da uno ambiguo — y la ambigüedad no se ve en la
gráfica.**

---

### 8.5 — Lo que enseñó la primera medición de verdad (sesión 82)

La primera corrida real —60 llamadas, ~$0,18— midió que **18 de 60** respuestas
rompían la forma, casi todas por escribir tres frases donde la rúbrica pedía dos.
De ahí salieron cuatro cosas que no estaban en el plan.

**1. Un detector saturado no es un detector.**

La propuesta era subir el tope a tres frases porque *"la rúbrica se contradice"*.
Leída entera, **la rúbrica pedía dos cosas, no tres** — el aliento salía de la línea
de personaje, que es **tono, no un renglón**.

El sí era correcto. **El porqué escrito, no** — y el porqué es lo que sobrevive,
porque un motivo equivocado no molesta hoy y se cita mañana como precedente.

> 🔑 **El motivo que sí decide:** una promesa que **el mejor modelo rompe casi
> siempre** no es un instrumento, es una constante. Y `[D-049]` existe para bajar de
> modelo **midiendo cuándo se les va la forma**. Un detector ya rojo no distingue
> *"el modelo nuevo se rompió"* de *"esto ya estaba rojo"*.

**2. Un instrumento tiene que ser más estable que lo que mide.**

La otra mitad: el corrector marcaba **cualquier** comilla, y la rúbrica solo prohibía
las que envuelven la corrección. Afinarlo exigía que el programa supiera **qué trozo
es la corrección** — y en las respuestas medidas la corrección entraba de **cinco
formas distintas**, una de ellas sin ninguna entradilla.

> 🔑 **El ancla que ese detector necesitaba era justo lo que `[D-049]` va a mover.**
> Al cambiar de modelo cambia el fraseo, y nadie podría distinguir *el modelo se
> rompió* de *la heurística resbaló*.

Se endureció la rúbrica en vez del corrector: **una sola regla dicha igual en los dos
sitios.**

**3. Un instrumento que cuenta y tira la evidencia obliga a pagar dos veces.**

La primera corrida contó 18 fallos **y tiró el texto**. El número sorprendente llegó
*después* del gasto, sin forma de investigarlo sin volver a pagar. Se añadió el
guardado — y se perdió otra vez, porque el archivo tiene **un nombre fijo** y se
sobrescribe: una tanda de diagnóstico de 10 se comió la línea base de 60.

> ⚠️ **El arreglo no era dejar de sobrescribir.** El motivo de sobrescribir era
> correcto: dos corridas mezcladas serían dos modelos revueltos. **Lo que fallaba es
> que el nombre del archivo no distinguía lo que la sobrescritura existía para no
> mezclar** — modelo y fecha, que es justo lo que `[D-049]` va a mover tres veces.

**4. Un comentario equivocado es peor que ningún comentario.**

El precio por llamada estaba escrito en **dos** archivos, y el aviso de que había
caducado se puso en uno — mientras el que iba a gastar era el otro. La copia estaba
**tres líneas debajo** de un comentario que decía *"esto se importa, no se copia"*.

> 🔑 **El daño no es que mienta: es que resuelve la duda del lector en la dirección de
> no mirar.** Quien fuera a corregir el número leía que había una sola copia y dejaba
> de buscar la segunda.

---

### 8.6 — Lo que todavía NO está probado, dicho aquí y no descubierto luego

| | estado |
|---|---|
| La traza escribiendo con el **servidor levantado y una llamada real** | 🔲 **no visto.** Solo probada con cliente de test y juez de mentira. No hay `trace.jsonl` en disco — verificado |
| El **precio por llamada** | 🔴 **caducado y sin corregir**, hacia el lado malo: tres frases son más tokens, así que el coste real sube y el número guardado se queda por debajo |
| El **corpus de 60 respuestas** | 🔴 **no existe.** Se pierde con la siguiente tanda hasta que el nombre del archivo lo distinga |
| El corrector **cableado a producción** | 🔲 escrito a propósito **fuera** de la ruta; que la traza apunte el fallo de formato es un cambio aparte |

> 📌 **Que esta tabla exista es la pieza haciendo su trabajo.** Un puente que solo
> cuenta lo que salió bien es el mismo defecto que el registro que solo hablaba
> cuando algo fallaba, con el signo cambiado.

---

## ⏭️ Siguiente paso

> 🔴 **Corregido en la sesión 82.** Este bloque decía *"pasos 0, 1 y 2 cerrados
> (sesión 31), sigue el paso 3: la pantalla"* — y llevaba así **más de cincuenta
> sesiones**, en el apartado que se titula *Siguiente paso*, que es el primero que
> alguien lee para saber qué hacer. 🔑 **Es `LM.24`: en un archivo que crece por
> enmiendas, el texto viejo se queda arriba, que es donde cae el ojo primero.** Y
> habría mandado a construir algo terminado hace meses, que es `LM.30`.

**Pasos 0 a 8 cerrados.** En curso el **paso 9: observabilidad y evals con
rúbrica** — el que cuenta la **Pieza 8**.

El estado vivo **no vive aquí**: vive en `_persistence/` del repo de TEAPP, que se
actualiza cada sesión. Este puente guarda **el porqué y lo aprendido**; el qué
exacto está allá. 📌 **Un puente que intenta llevar la cuenta se queda viejo sin
avisar** — acaba de demostrarlo.

---

## §7.9 — Lo que dejó la sesión 31: el paso 2, y la revisión cruzada trabajando

**El paso 2 quedó así:** `app/api.py` con una sola ruta `POST /practice`,
`respond` devolviendo tres piezas sueltas en vez de un texto armado (`D-008`),
Pydantic parando lo que no encaja con un 422, y **53 tests** (eran 30).
`input()` sigue existiendo, pero ya no es la única puerta.

### 🚨 La revisión desde esta terminal encontró dos defectos que 45 tests no veían

**Uno: el servidor se caía con varias personas a la vez.** 50 peticiones
simultáneas → entre **31 y 39 fallos 500**, y de 50 puntos el marcador guardaba
**8**. Eran **dos** defectos con el mismo síntoma: todas las peticiones escribían
el mismo archivo temporal, y además `add_point` leía y escribía con un hueco en
medio.

> 🔑 **La escritura atómica y el candado resuelven cosas distintas.** La atómica
> protege de UNA escritura cortada por la mitad. El candado protege de DOS
> escrituras pisándose. Tener la primera no da la segunda.

Después: **300 peticiones simultáneas, 0 fallos, la secuencia 1…300 completa.**

> 🔑 **Un test en verde no dice "el código está bien". Dice "el código está bien
> para lo que este test hace".** `TestClient` manda las peticiones de una en una:
> ningún test creó nunca el estado que rompía.

**Dos: el 500 regalaba la ruta absoluta del servidor** — el pendiente que la
sesión 30 dejó escrito para el paso 2, y que se pasó por alto. Cerrado con
`D-010`: *el detalle al log, al navegador un mensaje corto y sin rutas*.

⚠️ **La nota existía y no bastó.** Lo que lo cazó fue **volver a medirlo**.

### ⭐ `L-004` es suya, y es la lección más transferible del proyecto

Montó la prueba de carga, dio 50 de 50 — y descubrió que **contestaba el servidor
viejo** por el puerto ocupado, y que el viejo *también* daba 50 de 50.

> 🔑 **Antes de fiarte de una prueba, comprueba que falla con el código roto.**

### 🚨 Tercer fallo del harness: el `session-closer` no cerró nada

Se lanzó (18:38:09, consta en el transcript) y **no dejó commit ni tocó
`progress.md`**. El paso 2 entero sigue sin commitear en TEAPP.

> 🔑 **Un protocolo que se lanza no es un protocolo que se cumple.** El `starter`
> inventó porque nadie comprobó lo que leyó; el `closer` no guardó porque nadie
> comprobó lo que escribió. Es `PI-4` —*terminado = visto funcionando*— aplicada
> al harness en vez de al código.

⏳ **Propuesta anotada:** que el protocolo de cierre **termine imprimiendo el
hash del commit**. Si no hay hash, no hubo cierre.

📌 Y los dos fallos del harness se encontraron igual: **leyendo desde aquí el
transcript `.jsonl` de la otra terminal.** Sigue el hueco de la sesión 30 — el
trabajo interno del subagente no queda ahí.

### `assumptions.md` pasó de 0 a 3

`A-001` (practicadas vs. correctas, paso 8) · `A-002` (un solo proceso escribe el
marcador, paso 7) · `A-003` (el log se ve, paso 7).

**`A-002` hubo que corregirla el mismo día**: nació diciendo "sin `--workers`",
que es el peligro que *se ve venir*, cuando el probable es tener `main.py` y el
servidor encendidos a la vez. Medido: de 400 puntos llegaron **169**.

> 🔑 **Registrar algo no sirve si señala al sitio equivocado.**

---

### Lo que dejó la sesión 30, y no se repite en `PROGRESO.md`

**El primer defecto de TEAPP no apareció en el código: apareció en el harness.**
`session-starter` corrió en frío y **se inventó las tres herramientas**, porque
`protocol-start` nunca le mandó abrir `_context/scope.md`.

> 🔑 **Un puntero que nadie sigue es peor que no tener puntero.** Si el agente no
> abre el archivo, no se queda sin la información: **se la inventa**, y suena
> convincente. Es el precio del `CLAUDE.md` agnóstico, y se paga con lecturas
> obligatorias.

Se encontró **leyendo el transcript `.jsonl` de la otra terminal** — el hallazgo
de la sesión 28 puesto a trabajar. Con un hueco anotado: el trabajo interno del
subagente **no queda ahí**, así que no se pudo saber si inventó el subagente en
Haiku o la sesión principal al reescribir.

**Y el patrón de los arreglos del paso 1:** ninguno hace que el programa haga
algo *más*. Los dos hacen que **falle mejor** — que es casi todo lo que separa un
script de un producto, y lo que los pasos 6 y 7 van a repetir.

~~⏳ **Para el paso 2, anotado y sin arreglar:** el mensaje de error trae la ruta
absoluta del servidor.~~ → **cerrado en la sesión 31 con `D-010`** (ver §7.9).
⚠️ Pero no lo cerró la nota: lo cerró volver a medirlo.

## Lo que ya sabes (antes de escribir una línea)

- Que producción rompe **suposiciones**, no código — y ya tienes las cuatro.
- Que la llave nunca sale del servidor, y **por qué**.
- Que la tubería entera se construye y se prueba **sin pagar un centavo**.
- Que el costo de un agente conversacional crece con el **uso**, no con los
  usuarios.
- Que un número sin corrida detrás no se escribe.
