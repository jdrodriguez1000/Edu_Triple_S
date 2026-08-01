# Nivel 7 — Producción 🌉

> ⚠️ **Este nivel no tiene código aquí.** Es el primero que rompe la forma de los
> demás (`README.md` + script). El código vive en **otro repositorio**, y este
> archivo es el **puente**: dice qué se está construyendo, dónde, y por qué se
> decidió así.
>
> Si abres esta carpeta buscando un `07_script.py`, no falta nada: es a propósito.

**Estado:** análisis hecho (piezas 1 a 5 de 7). **Cero código, cero llamadas a la
API.** Sesión 28, 2026-08-01.

---

## Dónde vive el proyecto

```
Ruta:     ⏳ SIN DECIDIR — es la primera tarea de la próxima sesión
Nombre:   ⏳ sin decidir
Repo:     privado (guarda progreso personal y, después, configuración de AWS)
```

📌 Cuando se decida, **esta línea se llena y se mantiene al día**. Es lo único de
este archivo que no puede quedar desactualizado: es la dirección del proyecto.

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

## El análisis, en cinco piezas

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

## ⏭️ Siguiente paso

1. **Decidir ruta y nombre del repo nuevo**, y llenar la línea de arriba.
2. **Pieza 6 — AWS.** La más pesada: qué da la capa gratis y por cuánto tiempo,
   con **documentación oficial y fecha** (no de memoria — es la lección de las
   últimas cinco sesiones). La alarma de facturación va **antes** que todo.
3. **Pieza 7 — el orden de los pasos** del proyecto. Y ahí termina el análisis.

## Lo que ya sabes (antes de escribir una línea)

- Que producción rompe **suposiciones**, no código — y ya tienes las cuatro.
- Que la llave nunca sale del servidor, y **por qué**.
- Que la tubería entera se construye y se prueba **sin pagar un centavo**.
- Que el costo de un agente conversacional crece con el **uso**, no con los
  usuarios.
- Que un número sin corrida detrás no se escribe.
