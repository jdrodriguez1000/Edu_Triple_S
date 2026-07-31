# Nivel 6b — Memoria persistente y Skills

> **Parte 1: los conceptos.** Este documento no tiene una línea de código, y es a
> propósito. Aquí se entiende *qué* es la memoria y *por qué* es difícil.
> Las decisiones de diseño y el código vienen después.

**Escrito en la sesión 18.** Nace de una conversación entera de preguntas suyas,
antes de tocar el teclado.

---

## ⚠️ Nota de orden: este nivel se adelantó al 6

El plan original decía **6 (TypeScript) → 6b (memoria)**. Se invirtió, y la
decisión fue suya en la sesión 18.

**Su razón fue:** *"mejor 6b mientras tengo más dominio de agentes"*.
**La razón buena es otra**, y vale la pena dejarla escrita porque es de método:

> TypeScript **no se vuelve más fácil por saber más de agentes**. Son cosas
> independientes. Esperar no lo abarata.

Lo que sí es cierto, y es lo que decidió el cambio:

| | Qué enseña |
|---|---|
| Nivel 6 (TS) | **cero conceptos nuevos** de agentes — traduce lo que ya funciona |
| Nivel 6b | **dos conceptos que no tiene**: memoria persistente y Skills |

TypeScript no se aplaza para siempre: se aplaza **un nivel**. El nivel 7 es la
web, y **el navegador solo habla JavaScript**. El orden queda:
**6b → 6 (TS) → 7**.

---

## 1. El problema

```
Tú:      ¿A cómo está el dólar?
Agente:  3.207,64 pesos. Fuente: Banco de la República, 30 de julio.
Tú:      ¿Y cuánto son 500 mil pesos?
Agente:  155,93 dólares.          <- se acordó
```

Cierras la consola. Mañana vuelves:

```
Tú:      ¿Y cuánto son 500 mil pesos?
Agente:  ¿500 mil pesos de qué moneda, y a cuál?    <- no se acuerda de nada
```

**Su agente tiene la memoria de un pez.** Cada arranque nace de cero.

⚠️ **Y esto NO lo arregla un modelo más caro.** Opus tiene la misma amnesia que
Haiku. **No es un problema del modelo: es un problema del harness.**

| | Dónde vive | Cuánto dura |
|---|---|---|
| Memoria de la corrida (el `historial` del nivel 2) | RAM | muere al cerrar |
| **Memoria persistente** | **el disco** | sobrevive |

---

## 2. 🚨 El hecho que lo explica todo: la API NO tiene memoria. Nunca.

> **Cada llamada a `messages.create` es la primera vez.** El servidor de
> Anthropic no guarda nada entre una llamada y la siguiente. Ni entre corridas.
> **Ni dentro de la misma conversación.**

En el nivel 2, cuando el agente "se acordó" del dólar, el modelo no recordó
nada. **Su código le volvió a mandar todo el historial.**

```
Vuelta 1:  usted manda → [pregunta 1]
Vuelta 2:  usted manda → [pregunta 1, respuesta 1, pregunta 2]
```

⭐ **La memoria nunca estuvo en el modelo. Siempre estuvo en su código** — desde
el nivel 2, sin que se le llamara así.

### Los tres pisos

| Piso | ¿Existe? | Quién manda |
|---|---|---|
| **El modelo** | ❌ **no existe, jamás** | nadie. Es amnésico por diseño |
| **El harness** | ✅ | **quien escribió el harness** |
| **La aplicación** | ✅ | **usted, en este nivel** |

**Todo lo que parece memoria vive en el piso de en medio. Siempre.**
Por eso este nivel es de harness, no de IA. **No va a hacer que el modelo
recuerde: va a construir el mecanismo que le repite las cosas.**

---

## 3. Ya usó memoria persistente: es este curso

Claude también nace de cero en cada sesión. No "recuerda" el nivel 5b. Lo que
pasa al arrancar es:

1. El harness lee `CLAUDE.md` del disco.
2. **Pega el texto dentro del primer mensaje.**
3. Después Claude usa una herramienta para leer `PROGRESO.md`.

**Es el mismo truco del nivel 2, estirado en el tiempo: texto que sale del disco
y termina dentro del prompt.**

Y fíjese que no es *una* memoria: **son cuatro, con cuatro políticas distintas**,
y esa separación fue una decisión de diseño, no un accidente.

| Archivo | Política |
|---|---|
| `PROGRESO.md` | **se actualiza** — lo viejo se reemplaza |
| `LESSONS.md` | **solo crece** — nunca se borra nada |
| `GUIDE.md` | **se corrige** — lo obsoleto se borra |
| `CLAUDE.md` | casi nunca cambia |

⭐ **Este nivel no enseña algo nuevo: enseña a hacer, para su agente, lo que
usted ya hizo para Claude.**

### ¿Y por qué su agente no tiene memoria? Por nada especial.

**Porque nadie escribió ese código.** No falta una función del SDK ni un modelo
mejor: en `agente.py` no hay una línea que abra un archivo al arrancar.

De hecho, **su agente ya escribe en disco desde la sesión 15**:
`registro.jsonl`, con costos y permisos.

> **A su agente no le falta memoria: le falta LEER.** Escribe un diario todos los
> días y jamás lo abre.

---

## 4. La respuesta obvia, y por qué está mal

> *"Fácil: guardo la conversación completa y mañana se la mando toda."*

**Problema 1 — el costo.** Usted midió que la entrada es el **88-90%** de lo que
paga, con una relación de **27:1**. Pegar la charla de ayer y la de la semana
pasada se paga **en cada vuelta del bucle**. Ya vio lo que cuestan 3 herramientas
que nadie llamó: el 40% del menú.

**Problema 2 — el techo.** La conversación crece sin parar; la ventana de
contexto no. Un día no cabe.

**Problema 3 — y es el bueno.** El 95% de lo que se dijo **no valía la pena.**
Que preguntó el dólar el martes es basura. Que **siempre** pregunta en pesos
colombianos, eso vale oro.

> ### 🎯 El principio central del nivel
> **Memoria no es historial. Memoria es lo que quedó DESPUÉS de olvidar casi
> todo.**
>
> Recordar todo no es tener buena memoria: es no tener criterio.

---

## 5. Qué se guarda: no es una memoria, son varias

| Tipo | Ejemplo | Caducidad |
|---|---|---|
| **a) Perfil** — hechos estables | *"es colombiano, trabaja en pesos, quiere la TRM oficial"* | años |
| **b) Resumen** — la conclusión, no el transcript | *"en junio consultó el histórico del euro"* | meses |
| **c) Preferencias de trato** | *"prosa, sin selectores"* ← lo que dice `PROGRESO.md` de usted | años |
| **d) Estado de una tarea** | *"quedó pendiente el reporte de julio"* | días |

⚠️ **Cada tipo tiene una regla de caducidad distinta. Meterlas en el mismo saco
es el primer error de diseño.**

---

## 6. Las cuatro preguntas de todo diseño de memoria

| | La pregunta | La tensión |
|---|---|---|
| **QUÉ** | ¿qué merece guardarse? | lo estable, no lo dicho |
| **CUÁNDO se escribe** | ¿al terminar? ¿al vuelo? | |
| **CUÁNDO se lee** | ¿siempre, o solo si hace falta? | leer siempre = pagar siempre |
| **QUIÉN decide** | ⭐ **la decisión grande** | su código, o el modelo |

### Las dos escuelas de QUIÉN decide

**Escuela A — decide su código.** *"Al terminar, guarda la moneda que más usó."*
Predecible, barato, probable con evals. Pero **solo recuerda lo que usted
alcanzó a anticipar.**

**Escuela B — decide el modelo.** Una herramienta más en el menú, tipo
`recordar`. El modelo juzga qué vale la pena y la llama.

⭐ **La escuela B no necesita nada nuevo: es su bucle del nivel 3 y su menú del
5b, idénticos. La memoria es una herramienta más.** El modelo no sabe que está
"recordando": pidió una función y le llegó un `tool_result`.

Su precio ya lo conoce: **el modelo decide, y sus decisiones no son
deterministas** (paso 9).

### ⭐ Y en este curso las dos funcionan al tiempo

- **El CUÁNDO es del harness:** `CLAUDE.md` obliga a actualizar `PROGRESO.md` al
  cerrar. Es una regla fija. **Escuela A.**
- **El QUÉ es del modelo:** nadie dictó que el hallazgo de los `3.209,64` fuera
  en negrita arriba. **Escuela B.**

---

## 7. 🚨 Los peligros — memoria convierte errores temporales en permanentes

### a) Memoria envenenada
Hoy el agente inventa un dato —como los `3.209,64` del paso 10— y eso arruina
**una** respuesta. **Con memoria, si ese número se guarda, arruina todas las
conversaciones futuras** — y mañana lo dirá con más seguridad, porque "lo
recuerda".

> **Sin memoria, un error dura una corrida. Con memoria, dura hasta que alguien
> lo encuentre** — y nadie lo va a encontrar, porque vive en un archivo que nadie
> lee.

### b) Memoria obsoleta
*"El usuario vive en Bogotá"*. Se muda. **Nada se entera.** El dato no está
corrupto: está **vencido**, que es peor, porque parece bueno.
→ Es el precio de sonnet con fecha de vencimiento, otra vez. **Un dato guardado
sin fecha es un dato que no sabe si creerle.**

### c) La memoria vuelve a crecer
Es el nivel 2, pero peor: allá el historial moría al cerrar. **La memoria crece
entre corridas y no se muere nunca.**
→ **Un sistema de memoria sin política de olvido no está terminado.**

### d) ⭐ Los evals no la ven
Sus 121 evals corren sobre funciones puras: entran datos, sale un número. **La
memoria no es eso**: es un efecto que aparece *mañana*, en otra corrida, ante
otra pregunta.

> Es exactamente el defecto de los `3.209,64`: **pasó fuera del alcance de los
> evals.** Lo vio la rúbrica.

**Probar memoria exige lo del paso 10: correr, guardar la evidencia, y leerla.**

### e) Privacidad
Guardar datos de una persona en disco deja de ser un tema técnico. **Vale la pena
decidir desde ahora qué NO se guarda jamás.**

---

## 8. Cómo se articulan Git, RAG y Skills

### Git / GitHub — se cruza poco, pero donde se cruza es serio

**Git** guarda fotos (*commits*) de **su código** a lo largo del tiempo.
**GitHub** es un sitio donde subirlas. **Git funciona sin GitHub.**

| | Qué recuerda | Para quién |
|---|---|---|
| **Git** | la historia de **su código** | para **usted**, el que programa |
| **Memoria persistente** | hechos sobre **el usuario** | para **el agente**, en cada corrida |

**Su agente jamás va a leer el historial de Git.** No le sirve.

⚠️ **Donde SÍ se tocan:** si la memoria de sus usuarios vive en el proyecto, Git
la guarda y GitHub la publica. **Borrar el archivo después NO la borra del
historial.**
→ **Dónde vive el archivo de memoria es una decisión de seguridad, no de
comodidad.**

📌 **Estado del repo:** ~~(sesión 18) hay `.gitignore` pero no hay repositorio
Git: un extintor sin edificio~~ → **resuelto en la sesión 19.** El curso vive en
`https://github.com/jdrodriguez1000/Edu_Triple_S` (público, rama `main`), con un
commit por sesión. `.env`, `memoria.json` y `.venv/` siguen fuera del historial.

### RAG — es casi la misma idea que la memoria

**RAG = Retrieval Augmented Generation.** El nombre es horrible; la idea cabe en
una línea:

> **En vez de mandarle todo lo que sabe, busca el pedacito que hace falta y le
> manda solo eso.**

**Y la parte esencial ya la vio funcionar:** Claude no se carga el curso entero;
**lee `PROGRESO.md`**. Eso *es* recuperación.

> **RAG no es una tecnología nueva. Es "no mandes todo, manda lo que sirve".
> Todo lo demás es cómo buscas.**

**Lo único realmente nuevo: buscar por SIGNIFICADO.** *"¿cuánto me devuelven si
me arrepiento?"* y *"política de reembolso"* **no comparten una palabra**. Los
**embeddings** convierten cada texto en coordenadas de significado; lo parecido
queda cerca. Se guarda en una **base de datos vectorial** — que hoy puede ser
**PostgreSQL** con una extensión.

⭐ **RAG no es el hermano de la memoria persistente: es la memoria persistente
cuando ya no cabe.** Al principio son 5 datos y se leen todos. Con 3.000
conversaciones, leerlos todos es el problema del principio otra vez. **Ahí la
memoria deja de leerse y empieza a buscarse. Y buscarse es RAG.**

⚠️ **RAG está muy sobrevendido.** La regla honesta:

```
¿Cabe todo en el prompt sin arruinarse?   →  no necesita RAG. Mándelo.
¿Son pocos y sabe cuál sirve?             →  léalo con una herramienta.
¿Son muchos y no sabe cuál sirve?         →  ahora sí, RAG.
```

### Skills — el mismo problema, resuelto más barato

| | Quién escoge qué entra al prompt |
|---|---|
| **Skills** | el **modelo**, de una lista corta que **usted** cura |
| **RAG** | un **buscador automático**, por parecido de significado |

**Skills es más simple, más predecible y más barato.** Para la mayoría de casos
reales alcanza. **RAG es cuando el volumen ya no deja curar a mano.**

---

## 9. 🎯 Los dos ejes — el error de modelo mental más común

El caso que planteó usted: una app de divisas para **un usuario** contra otra
para **una corporación con miles de usuarios y documentos**.

Su conclusión fue correcta, pero la forma era una escalera:

```
archivo  →  base de datos  →  + RAG          ❌ así no es
```

**No es una escalera. Son DOS ejes independientes:**

```
                    ↑ MUCHO conocimiento
                    │
        RAG solo    │    RAG + base de datos
   (1 investigador, │    (la app corporativa
    20.000 papers)  │     completa)
                    │
    ────────────────┼────────────────→  MUCHOS usuarios
                    │
     archivo plano  │    base de datos
      (la app 1)    │    (app 2 sin documentos)
                    │
                    ↓ POCO conocimiento
```

| Eje | Qué lo mueve | Qué exige |
|---|---|---|
| **↔ horizontal** | cuántos **usuarios** escriben | archivo → SQLite → PostgreSQL |
| **↕ vertical** | cuánto **conocimiento** consultar | leerlo entero → Skills → RAG |

**No se determinan uno al otro:**
- Un investigador solo con 20.000 papers → **RAG sí, base de datos no.**
- 50.000 empleados y cero documentos → **base de datos sí, RAG no.**

> **Uno crece por gente. El otro crece por conocimiento.**

### Y el archivo plano NO es la opción pobre

Un usuario nunca escribe dos veces al tiempo, los datos caben, buscar es leer.
**Es la respuesta correcta**, por su propia regla de la sesión 16: *primero si
hace el trabajo; entre los que sí, el más barato.*

### Por qué con miles de usuarios el archivo NO es una opción

No es "menos elegante": **se rompe**, por dos razones distintas.

1. **Dos escrituras al tiempo corrompen el archivo.** El último que guarda borra
   al otro, o quedan entrelazadas. **Sin error y sin aviso. Un archivo no sabe
   hacer fila.**
2. **Para leer un dato hay que leerlo todo.** Buscar al usuario 4.312 recorre los
   10.000, en cada conversación.

> **La base de datos no es "lo profesional": es lo que sabe hacer fila y sabe
> buscar sin leer todo.**

### Dos cosas que aparecen solo con muchos usuarios

**a) La memoria es POR USUARIO, y jamás se pueden cruzar.** Si el 4.312 ve la
memoria del 887, no hay un error de programación: **hay una filtración de
datos.**

**b) "Deja registro de lo realizado" NO es memoria: es un LOG.**

| | Log (registro) | Memoria |
|---|---|---|
| Guarda | **todo** lo que pasó | **lo poco** que vale la pena |
| Crece | sin parar, solo se añade | poco, se corrige y se olvida |
| Lo lee | **usted**, después | **el agente**, en la próxima corrida |

**Su agente ya tiene el log —`registro.jsonl`— y nunca lo relee.** Y así debe
ser: pegarlo al prompt sería el error del principio.
→ **El log es materia prima; la memoria es la conclusión.**

### ⚠️ El peligro de RAG en una empresa

Los documentos son de la empresa, pero **no todo empleado puede ver todo
documento.** Un RAG que busca por significado en todo el montón le entrega al
pasante el contrato del gerente — bien redactado y con la fuente citada.

> **RAG no es solo "buscar bien": es "buscar solo en lo que esta persona tiene
> derecho a ver".** Es su freno de permisos del paso 8, aplicado a la **lectura**
> en vez de a la escritura.

---

## 10. ⭐ La conclusión: "memoria" no es un componente, son cuatro

La app corporativa del ejercicio, terminada:

| | Qué guarda | Dónde vive |
|---|---|---|
| **1. Perfil** | *"trabaja en pesos, TRM oficial"* | base de datos, **por usuario** |
| **2. Conocimiento** | manuales, políticas, procesos | RAG, **compartido y con permisos** |
| **3. Log** | cada llamada, costo, permiso | archivo o tabla, **nunca va al prompt** |
| **4. Historial de la charla** | la conversación en curso | RAM — **muere al cerrar, y está bien** |

**Cuatro dueños, cuatro vidas, cuatro políticas de olvido distintas.**

Que es justo lo que este repo descubrió sin proponérselo: **`PROGRESO.md` se
actualiza, `LESSONS.md` solo crece, `GUIDE.md` se corrige. Tres archivos porque
son tres memorias.**

Y las tres técnicas del nivel —memoria, Skills, RAG— responden a **una sola
pregunta**, que es la pregunta central de todo el curso:

> # ¿Qué texto merece estar en el prompt en este momento, y qué no?

---

## Ejercicios

Todos son de papel y lápiz. Ninguno necesita código.

1. **El pez.** Escriba en una frase por qué su agente no recuerda nada, sin usar
   las palabras "memoria" ni "modelo".

2. **Las cuatro memorias de este repo.** Para `PROGRESO.md`, `LESSONS.md`,
   `GUIDE.md` y `CLAUDE.md`: ¿quién escribe cada uno, cuándo, y qué se borra?

3. **Clasifique.** ¿Perfil, resumen, preferencia, estado de tarea, log — o
   basura que no se guarda?
   - *"El 12 de julio preguntó por el euro."*
   - *"Siempre pide la fuente."*
   - *"Está armando el cierre contable de julio."*
   - *"La TRM del 30 de julio fue 3.207,64."*
   - *"Es contador."*

4. **El dato vencido.** Invente un dato de memoria que dentro de seis meses sea
   falso **sin que nada lo avise**. Luego proponga cómo lo detectaría.

5. **Los dos ejes.** Ubique en el diagrama: (a) un abogado solo con 5.000
   sentencias; (b) un call center de 300 agentes sin documentos; (c) su propio
   agente de divisas hoy.

6. **El envenenamiento.** Si el agente hubiera guardado los `3.209,64` como
   memoria: ¿qué habría pasado en las 10 preguntas del examen del paso 10? ¿Lo
   habría visto la rúbrica?

---

## Lo que ya sabe

- La API **no tiene memoria, nunca**. Ni entre corridas ni dentro de una
  conversación. El `historial` del nivel 2 era su código repitiéndole las cosas.
- **Toda memoria vive en el harness.** Ni en el modelo ni en la API. Por eso
  cambiar de modelo no arregla la amnesia.
- La memoria de un harness (este curso) y la de una aplicación (su agente) son
  **la misma técnica** —leer disco y meterlo en el prompt— con **dueños,
  usuarios y archivos distintos**.
- **Memoria no es historial**: es lo que queda después de olvidar casi todo.
  Guardar la conversación completa falla por costo, por techo y por criterio.
- Hay **varios tipos** de memoria con caducidades distintas: perfil, resumen,
  preferencias, estado de tarea.
- Todo diseño responde cuatro preguntas: **qué, cuándo se escribe, cuándo se lee
  y quién decide**. La cuarta es la grande: **escuela A (su código) o escuela B
  (el modelo, con una herramienta)**.
- **La memoria convierte errores temporales en permanentes**, y los **evals no la
  ven** — es el defecto de los `3.209,64` otra vez.
- **Un sistema de memoria sin política de olvido no está terminado.**
- **Git** recuerda su código, para usted; casi no se cruza con la memoria del
  agente **excepto en que nunca debe subir secretos ni datos de usuarios.**
- **RAG es la memoria persistente cuando ya no cabe.** Está sobrevendido: primero
  el archivo, después Skills, y solo entonces RAG.
- **Skills vs RAG:** en Skills escoge el modelo de una lista que usted cura; en
  RAG escoge un buscador por significado.
- Escalar por **usuarios** (archivo → base de datos) y escalar por
  **conocimiento** (leer todo → RAG) son **dos ejes independientes**, no una
  escalera.
- Con muchos usuarios el archivo plano **se rompe**: no sabe hacer fila y obliga
  a leer todo. Y la memoria pasa a ser **por usuario**, sin cruces.
- **Un log no es una memoria.** El log es materia prima; la memoria es la
  conclusión.
- **"Memoria" no es un componente: son cuatro**, con cuatro políticas de olvido.

---

## Parte 2 — las decisiones, tomadas (sesión 18)

Las seis son suyas. Quedaron así:

| | Decisión | Qué quedó |
|---|---|---|
| 1 | **qué se guarda** | solo el **perfil**: hechos estables del usuario |
| 2 | **quién decide** | ⭐ **escuela B para escribir** (herramienta `recordar`); **escuela A para leer** (siempre, automático) |
| 3 | **cuándo se lee** | siempre, al arrancar, pegado al system prompt |
| 4 | **formato** | un `memoria.json` que se **reescribe** · entra a `.gitignore` |
| 5 | **qué se olvida** | cada dato **con su fecha** + tope de 8 |
| 6 | **permiso** | **no pide.** A cambio: huella + revisión |

### ⭐ Sobre la 6: cambió de opinión a mitad, y con argumento

Primero decidió vía libre. Después se devolvió: *"¿qué tal si con el permiso
tenemos lo mismo — solo esta vez, toda la sesión, y sin permiso?"*, notando que
**su propia tecla `t` de la sesión 15 ya da la vía libre.** Es cierto.

**Lo que decidió el asunto fue el segundo de tres problemas:**

1. La primera vez **sí** interrumpe, y cae a mitad de una respuesta que nadie
   pidió. Su propio dato: **26 segundos** la primera decisión de permiso.
2. 🚨 **EL PERMISO NO TIENE MEMORIA.** `AUTORIZADAS = set()` vive en RAM y muere
   al cerrar (`agente.py:540`).
   > **Un permiso volátil sobre una herramienta persistente es un desajuste de
   > diseño.** Habría que teclear `t` todos los días, para siempre — y él mismo
   > escribió que *"un permiso que se pregunta demasiado deja de leerse"*.
3. **El permiso pregunta lo que no importa.** El peligro no es la acción
   (escribir 4 líneas, reversible): **es el contenido.** Un *"¿autorizas
   escribir?"* no muestra **qué** se va a escribir.

> ### 🎯 Permiso = ANTES, para lo irreversible.
> ### Revisión = DESPUÉS, para lo reversible.

Y coincide con lo que ya estaba escrito en `agente.py:509`: *"la pregunta no es
¿lee o escribe?, es: SI ESTO SALE MAL, ¿LO PUEDO DESHACER?"*.

⚠️ **Quitar el permiso no es renunciar a protegerse: es cambiar de protección.**
El permiso también **avisaba**. Sin él, la obligación **se muda al registro**:
cada escritura deja huella. **Permiso → observabilidad.**

---

## Parte 3 — lo construido (pasos 2 y 3)

### `memoria.py` — cuatro funciones, cero IA

| | |
|---|---|
| `cargar_memoria()` | **nunca revienta.** 4 caminos previstos |
| `guardar_dato(texto)` | valida, refresca o agrega, aplica el tope |
| `memoria_como_texto(datos)` | **la que cuesta dinero** — arma el texto del prompt |
| `olvidar(indice)` | **esto reemplaza al permiso** |

```powershell
python memoria.py                 # ver qué recuerda
python memoria.py borrar 0        # olvidar uno
python memoria.py borrar todo
python evals.py                   # 49 casos, $0.00, sin red
```

### `evals.py` — 49 casos, 0 fallos

⭐ **La trampa del archivo es lo mejor del paso.** En el 5b la prohibición era la
RED; aquí es **el DISCO**: un eval que escribe en el `memoria.json` de verdad
**le borra al agente lo que aprendió — y sale en verde mientras lo destruye.**

Se resolvió con **dos** cosas: se desvía `memoria.ARCHIVO` a un archivo de
mentiras, **y** se guarda el real byte por byte y se compara al final.
**La primera sola es una promesa; la segunda la vuelve un hecho comprobado.**

⚠️ **Tercera vez que aparece este problema** (el registro del paso 9, el
`examen.py` de la sesión 17, y esto): **un programa de prueba que escribe donde
escribe el de verdad.**

**Los tres casos que más valen:**
- **`olvidar(-1)`** — en Python `lista[-1]` es válido y significa *el último*.
  Sin el freno, un `-1` por error **borra el dato más nuevo, en silencio y
  devolviendo 1**: informando éxito.
- **Los dos bordes del largo** (200 pasa, 201 falla). Probar uno solo deja vivo
  el error de "uno más".
- **"Refrescar no bota a nadie"** — si refrescar contara como dato nuevo,
  repetir lo mismo ocho veces **vacía la memoria entera**, con motivo
  `refrescado`: **sin que nada se vea mal.**

### 🐛 Y un eval salió en rojo — el defecto era de la prueba

```
FALLA una línea por dato    esperado=0    obtenido=2
```

**El 2 era lo correcto**: dos datos, dos líneas. La vara estaba mal.
→ Es la sesión 17 otra vez: **cuando una buena respuesta reprueba, el sospechoso
es el examen, no el examinado.** Quedó comentado dentro de `evals.py`.

---

## Lo que sigue

| Paso | | Estado |
|---|---|---|
| 1 | Los conceptos y las decisiones | ✅ |
| 2 | `memoria.py` — las funciones puras | ✅ |
| 3 | `evals.py` — 49 casos, $0,00 | ✅ |
| 4 | **Conectar al agente**: `recordar` + leer al arrancar | ✅ **sesión 19** |
| 5 | Correrlo y **medir** | ✅ `volumen.py` — 3 defectos hallados, **los 3 arreglados y re-medidos: 4 de 9 → 9 de 9** |
| 5b | El examen con rúbrica y juez | ✅ sesiones 20–21 — 9 criterios, C9 escrito y **nunca corrido** |
| **6** | **Skills** | ✅ **sesión 22** — 4 skills, `skills.py`, `leer_skill`, línea base y medición |
| 7 | Las lecciones de la MEMORIA en `LESSONS.md` | ✅ **sesión 23** — L6b.1–L6b.29, $0,00. Con Skills (L6b.30–L6b.46), **46 seguidas** |

🎓 **Con el paso 7 el nivel 6b queda CERRADO.** Lo siguiente es el **nivel 6
(TypeScript)**.

### Paso 6 — Skills, en cuatro líneas

- **Qué son:** conocimiento en `.md`. La **ficha** viaja siempre; el **cuerpo**,
  solo cuando el modelo lo pide con `leer_skill`.
- **Qué costó:** +849 tokens por vuelta, **predichos gratis con `count_tokens` y
  confirmados exactos**. Cargar 3 o más sale peor que no tener el mecanismo.
- **Qué se ganó:** un defecto real del agente (una división hecha de cabeza, con
  14 USD de error) se arregló **editando un `.md`, sin tocar Python**.
- **Dónde está lo reutilizable:** `GUIDE.md` §12 y `LESSONS.md` L6b.30–L6b.46.

### ✅ Las dos cosas que estaban pendientes antes del paso 4, resueltas

1. **La decisión estructural: se COPIÓ.** `agente.py`, `herramientas.py` y los
   121 evals (como `evals_agente.py`) viven ahora en esta carpeta. El
   `05b-proyecto` queda **congelado** como referencia para comparar el antes y
   el después.
   ⚠️ **Y el precio de esa decisión, dicho en voz alta:** ahora hay dos
   `agente.py` en el curso. Un arreglo en uno no llega al otro. Está bien
   **solo mientras el 5b no se toque**; el día que se le meta mano, la decisión
   se vuelve mala.
2. **El sabotaje se hizo, y fueron cinco.** Los 49 casos (hoy 73) se vieron en
   rojo. Lo que enseñó está abajo.

### 🔨 Lo que enseñaron los cinco sabotajes

| Qué se rompió | Rojos | La lección |
|---|---|---|
| el tope bota el más **nuevo** | 2 | el motivo decía `desplazo` **y mentía**: contar y leer el motivo no basta, hay que preguntar **quién** quedó |
| se cae el freno del `-1` | 2 | borró el dato más nuevo **devolviendo éxito** |
| `>` pasa a `>=` en el largo | 1 | el borde de 201 siguió verde: **un solo borde no sirve** |
| el desvío del disco, quitado | 1 | **48 casos en verde mientras borraba la memoria real** |
| la memoria antes que las reglas | 1 | los casos de *"¿está ahí?"* **no ven el orden** |

⭐ **Lo que tienen en común los dos primeros: el defecto reportaba ÉXITO.**
`desplazo` y `1` son las respuestas correctas para las acciones equivocadas.
**El motivo dice qué creyó que hizo, no qué hizo.**

### Deudas anotadas dentro del código

- **`_escribir()` no es atómica.** Si el programa muere a mitad, el archivo queda
  partido. La solución es archivo temporal + renombrar.
- **El tope bota el más viejo, y eso es una DECISIÓN, no una obviedad.** Está
  diciendo que lo viejo vale menos: *"es contador"* vale más que algo dicho ayer.
