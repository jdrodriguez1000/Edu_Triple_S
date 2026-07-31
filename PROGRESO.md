# PROGRESO — Bitácora del curso

> Este es el archivo de memoria del curso. Claude lo lee al empezar cada sesión y lo
> actualiza al terminar. Tú también puedes escribir aquí lo que quieras.

**Última actualización:** 2026-07-31 (sesión 22)

---

# 📍 NIVEL 6b — **PASO 6 (SKILLS) TERMINADO, MEDIDO Y VERIFICADO. EL NIVEL 6b QUEDA CERRADO SALVO UNA DEUDA.**

Sesión 22. Costo total: **$0,1796**.

## 🚨 LO PRIMERO DE LA PRÓXIMA SESIÓN: **LAS LECCIONES DE LA MEMORIA (L6b.1–L6b.29)**

Es la única deuda que queda del nivel 6b, y está dicha en voz alta dentro de
`LESSONS.md`: el bloque del nivel **está a medias**.

- Las lecciones de **Skills** ya están escritas: **L6b.30 a L6b.46** (17).
- Las de **memoria** (pasos 1 a 5, sesiones 16 a 21) **no**. Siguen sueltas
  dentro de este archivo. Se numerarán **L6b.1 a L6b.29** — el hueco ya está
  reservado a propósito, para no renumerar nada.

Cuesta **$0,00**: es leer las sesiones 16–21 de aquí y destilarlas. Cuando eso
esté, el nivel 6b se cierra y sigue el **nivel 7**.

---

## Lo que se hizo en la sesión 22: SKILLS, de cero a medido

### Las 4 skills (`06b-memoria-skills/skills/`)

| Skill | Qué contiene |
|---|---|
| `reporte-mensual.md` | 5 secciones en orden, redondeos, `cierre-AAAA-MM.md`, nota al pie textual |
| `normas-cambiarias.md` | tramos de 5.000 y 20.000 USD, márgenes 0,4 % / 0,7 %, monedas permitidas |
| `explicar-a-un-cliente.md` | palabras prohibidas y 3 respuestas modelo (la única sin cifras) |
| `cierre-de-ano.md` | una sola tasa para todos los saldos, sección 6, archivo aparte |

Todas rotuladas **⚠️ reglas de una empresa ficticia**. Ninguna se presenta como
normativa colombiana. Y todas llenas de **datos arbitrarios a propósito**: si el
modelo pudiera adivinarlos, no se podría medir nada.

### El código

| Archivo | Qué |
|---|---|
| `skills.py` | **nuevo.** Funciones puras: partir ficha/cuerpo, armar el menú, `leer_skill`. No conoce la API |
| `linea_base.py` | **nuevo.** Las 5 preguntas, en dos modos (`--con` / sin) |
| `agente.py` | menú al SYSTEM, `leer_skill` en TOOLS/FUNCIONES/PERMISOS, freno de doble carga, `menu_skills` como parámetro |
| `skills/*.md` | las 4 |

**228 evals (121 + 107) siguen en verde**, y `memoria.json` quedó byte por byte
igual.

### 🚨 LA LÍNEA BASE, que fue lo primero y hay que insistir en ella

Antes de conectar nada se corrieron las 4 preguntas **sin** skills ($0,0405).
Resultado: **el agente no inventó ni un umbral** — se declaró fuera de alcance
(*"no soy de regulaciones bancarias, pregunte en su banco"*) o pidió más datos.

Eso probó lo único que había que probar antes de gastar: **las skills tienen
algo que aportar.** Es el error del *"¿qué es una variable?"* de la sesión 3,
evitado esta vez **comprobando** en vez de suponiendo.

### 💰 Los números, y uno de ellos es un estreno

| | tokens por vuelta |
|---|---|
| Sin skills | 4.894 |
| **Impuesto del menú + la herramienta** | **+849 (+17,3 %)** |
| Los 4 cuerpos completos | 3.906 |

⭐ **`count_tokens` predijo +849 GRATIS, y la corrida real dio +849 exacto.**
Primera vez en el curso que un costo se predice en vez de descubrirse.

**El punto de equilibrio:** cargando **una** skill sale ~6.700/vuelta; pegando
todo el conocimiento siempre, 8.800; **cargando las cuatro, 9.649 — peor que no
tener el mecanismo.** Skills gana solo si el modelo es selectivo, y eso lo
deciden **las descripciones**, no el código.

### Lo que hizo el agente con las skills puestas ($0,0777, 4 preguntas)

| Pregunta | Cargó | |
|---|---|---|
| 200 dólares | **nada** | ✅ el control no se dejó tentar |
| el cliente reclama | `explicar-a-un-cliente` | ✅ |
| 50 millones | `normas-cambiarias` → `trm` → `convertir` | ✅ **la skill lo mandó a usar herramientas** |
| reporte de diciembre | `cierre-de-ano` **+** `reporte-mensual` | ⭐ **las dos en la MISMA vuelta** |

El par confundible se resolvió, y era lo más dudoso del diseño. Funcionaron las
**notas de frontera en las dos direcciones**, copiadas de lo que se hizo con C9.
Y el "goloso" no apareció: nunca cargó de más.

### 🐛 Los cuatro defectos de la sesión, y de quién fue cada uno

1. **Mío, de diseño del examen:** *"ármame el reporte de diciembre"* un 31 de
   julio. El agente contestó **"esa fecha está en el futuro"** y tenía razón.
   La pregunta era imposible. → Cambiada a diciembre de 2025.
2. **Mío, de rótulo:** el script gritaba `🚨 SEÑALES ENCONTRADAS SIN SKILL` en la
   corrida **con** skills. El detector no cambió; cambió **qué significa** lo
   que detecta. Rotulé el éxito como alarma.
3. **Mío, de orden:** `--con` se leía a mitad del archivo y `anotar("inicio")`
   lo necesitaba 30 líneas antes → `NameError`.
4. **Del agente, y el importante:** con la skill puesta hizo **una división de
   cabeza** para aplicar el margen del 0,4 % y **falló por 14,15 USD (~44.000
   pesos)**, teniendo `convertir` disponible.

### ⭐ EL RESULTADO DE FONDO DEL PASO 6

El defecto 4 se corrigió **editando `normas-cambiarias.md`**: se pasó de "margen
sobre la tasa" (que obliga a dividir) a "**factor sobre el resultado**" (que
`convertir` sí puede hacer, porque multiplica).

**Cero líneas de Python.** En la corrida siguiente: **dos llamadas a
`convertir`** y la cifra exacta, **15.898,25**.

> Esa es la ganancia de verdad del paso, y no es el ahorro de tokens: **el
> conocimiento salió del `.py` y lo puede editar quien sepa del negocio.**

### La verificación honesta del arreglo

La primera re-corrida **no sirvió**: la pregunta 3 mezcla dos cosas (¿autorizo?
y ¿cotizo?), así que "no aplicó el margen" admitía dos explicaciones. Se agregó
la **pregunta 5** (*"cotízame… con el margen aplicado"*), que solo tiene dos
salidas posibles. Ahí sí se confirmó.

⚠️ **Y con la letra pequeña:** es **una** corrida. El defecto salió 1 de 1 y el
arreglo funcionó 1 de 1. Eso es *"no se reprodujo"*, no *"quedó arreglado"*.

### Las cuentas

| Corrida | |
|---|---|
| Línea base (4 preguntas) | $0,0344 |
| Repetir la 4 arreglada | $0,0061 |
| Con skills (4 preguntas) | $0,0777 |
| La 3 después del arreglo | $0,0303 |
| La 5 (cotización limpia) | $0,0311 |
| **Total** | **$0,1796** |

### Dónde quedó escrito lo reutilizable

📌 **`GUIDE.md` §12 — "Skills: conocimiento que vive fuera del código".** Es la
sección **más portable de la guía**: no depende de este curso ni del agente de
divisas. Tiene el árbol de decisión de cuándo usar una skill, la plantilla del
`.md`, las reglas de la descripción, las 4 decisiones del harness, el candado de
seguridad, los modos de falla y el procedimiento en 6 pasos.

**`LESSONS.md`: L6b.30 a L6b.46** (17 lecciones).

### Deudas anotadas del paso 6

- Agregar un `.md` a la carpeta **exige reiniciar**: el menú se arma al importar.
- El tramo se decidió con el monto **bruto** (15.962,10), no con el neto. El
  `.md` dice *"el equivalente en dólares"* y no aclara cuál. Es una ambigüedad
  real, sin consecuencia en este caso.
- Las skills nunca se han **saboteado** (como sí se hizo con `memoria.py`).
  Nadie ha visto en rojo el mecanismo de carga.

---

## Lo que se hizo en la sesión 21: C9 — USÓ LO QUE RECORDABA

El hueco que dejó la corrida de ayer (caso 12.2: la peor respuesta del examen no
sacó un solo FALLA) ya tiene criterio.

⚠️ **Y va marcado en TRES sitios como "escrito y NUNCA corrido":** encabezado de
`rubrica.md`, el criterio mismo, y la tabla de pendientes de la Parte 8. C1–C8
tienen una corrida detrás; C9 no tiene ninguna.

> **Una rúbrica puede contener a la vez cosas medidas y cosas supuestas, siempre
> que se distingan a simple vista.**

### La decisión de entrada, que fue del estudiante y hay que dejarla escrita

Yo abrí la sesión diciendo *"lo siguiente es C9"*, como si fuera obligatorio. Él
preguntó **por qué no pasar ya a Skills**, y la pregunta estaba bien hecha.

Lo que la resolvió no fue quién tenía razón, sino un dato: **escribir C9 cuesta
$0; saber qué DA C9 cuesta ~$0,25 y una auditoría entera.** Son dos cosas
distintas y estaban pegadas en una sola recomendación. Se hizo la barata.

> Es la misma distinción de ayer (arreglar el código vs. volver a correr),
> aplicada esta vez **antes** de gastar en vez de después.

### Las dos preguntas previas de `GUIDE.md` §11, respondidas

**1. ¿Qué evidencia necesita? ⭐ NINGUNA NUEVA — y es el mejor hallazgo del día.**
C7 y C8 llegaron pidiendo cosas que el juez no veía, y a C7 le costó un **62%
falso**. C9 se califica con la pieza 2 que ya se construyó para C8.
> **C8 y C9 miran el mismo dato desde los dos lados: qué se escribió y qué se
> leyó.** Un criterio que reutiliza evidencia es más barato y más seguro que uno
> que la inventa.

**2. ¿Con qué se solapa? Con tres — y los dos peores no eran solapamiento, sino
PREMIOS OPUESTOS.** Que es el defecto que rompió C6, con otra cara:

| | el choque | dónde quedó la línea |
|---|---|---|
| **C4** | *"¿a qué moneda?"* = levantó la frontera (`PASA`) **y** ignoró la ficha (`FALLA`) | si la memoria ya resuelve la ambigüedad, **no hay frontera**: es C9 |
| **C5** | *"no lo sé"* = admitió el límite (`PASA`) **y** desconoció lo que tenía (`FALLA`) | la línea es *"¿podía saberlo?"*. Si estaba en su memoria, **podía**: es C9 |
| **C7** | ¿una afirmación que sale de una ficha es *afirmar sin fuente*? | **no.** La memoria llega en el system prompt → **una ficha ES fuente**. Distorsionarla es C9 |

Y una que parecía choque y no lo era: **mencionar un dato del usuario no es
relleno** (la lista de C6 es cerrada). Lo que sí lo sigue siendo es **narrar que
lo fue a buscar**. → *Usar el dato, sí; contar el mecanismo, no.*

### ⚠️ El número incómodo, dicho ANTES de correr: C9 nace con 3 casillas

Solo se puede calificar en 11.2, 12.2 y 13.2. En las diez sueltas y en los tres
turnos 1 **la memoria arranca vacía**: no hay nada que ignorar.

**Es el criterio peor medido del examen**, por debajo de C4 y C5 (4 cada uno).
Un solo fallo lo tumba al 67%.

> ⭐ **Pero ese 3 es el dato útil, porque dice qué hacer: la memoria no se mide
> mejor agregando CRITERIOS, sino agregando PARES.** Un criterio nuevo no crea
> evidencia — solo mira la que ya hay. Las 3 casillas son las 3 únicas
> conversaciones segundas que existen: **el techo es la forma del examen, no la
> rúbrica.**

Y la comparación que lo resume: **C8 tiene 16 casillas y C9 tiene 3.** Es la
misma memoria. **Guardar se puede vigilar en todas partes; usar solo se ve en la
conversación siguiente.**

📌 **Lo que subiría C9 de verdad:** un par nuevo donde la ficha **cambie la
respuesta sin ser la única forma de contestar**. El 11 y el 13 taparon el hueco
por suerte de diseño (ahí usar la memoria era el único camino); el 12 fue el
único con otra salida, y es justo el que se escapó.

### Lo que se tocó

| Archivo | Qué |
|---|---|
| `06b-memoria-skills/rubrica.md` | **C9 completo**; notas de frontera en C4, C5 y C6; columna C9 en las dos matrices; conteo de casillas; Parte 0 (no pidió evidencia nueva); Parte 8; encabezado |
| `06b-memoria-skills/juez.py` | C9 cableado en `APLICA` (11.2, 12.2, 13.2) y en `CRITERIOS`; nota de presupuesto |

**Verificado sin gastar:** la Parte 1 sigue recortándose bien (18.205 caracteres,
los 9 criterios dentro), `juez.py` compila, y `APLICA` da **16 turnos con 3
casillas de C9**, exactamente donde dice la matriz del `.md`.

⭐ **Y un detalle que salió solo: `cargar_rubrica()` no se tocó al agregar C7, C8
ni C9.** Es justo lo que buscaba esa decisión — **el instrumento vive en el
`.md`, el código solo lo transporta.** Tres criterios después, sigue aguantando.

### 💰 El efecto de segundo orden, anotado en el código

C9 **se califica en 3 turnos, pero su texto viaja en la entrada de los 16**.
Se paga 16 veces y se cobra 3.

> No es razón para no escribirlo. Es razón para **no estimar la próxima corrida
> copiando el $0,6658 de ayer**: ese número nació con ocho criterios. (Errores
> de costo 5 y 6 del curso: *un número heredado arrastra los supuestos con los
> que nació*.)

---

## 📌 TAREA APARTADA — `METODO.md`, **al terminar TODOS los niveles**

**No es para la próxima sesión.** Va después del nivel 8, y por eso queda aquí
escrita: para que no se pierda y para que no se adelante.

**De dónde salió:** al cerrar la sesión 21 el estudiante preguntó si este repo
sirve de base para construir apps —su próximo proyecto es una **app del clima**
que compara ciudades y recomienda qué ponerse o si salir— y si podía decirle a
un Claude Code de otra terminal que leyera `GUIDE.md`, `LESSONS.md`,
`PROGRESO.md` y `README.md`.

**Qué se respondió, y es lo que justifica la tarea:**

1. **El código de este repo NO es una librería.** Está escrito para enseñar:
   comentarios largos, el bucle a mano en vez del `tool_runner`, nombres en
   español. **Lo reutilizable no son las piezas, es el criterio.**
2. **Cargar los cuatro archivos en otro proyecto es mala idea**, y por la lección
   del nivel 2. Pesan ~445 KB ≈ **110.000 tokens** *(estimado por caracteres, NO
   medido — se puede medir gratis con el conteo de tokens de `GUIDE.md` §5.b)*,
   y entrarían en **cada** sesión del otro proyecto.
3. **Y `PROGRESO.md` es lo peor de los cuatro para exportar:** es el estado de
   ESTE curso. Un agente trabajando en la app del clima leería *"lo siguiente es
   Skills"* y *"C9 quedó sin correr"*. **Ruido con autoridad.**

| archivo | ¿se exporta? |
|---|---|
| `GUIDE.md` | **sí** — el *cómo*. Sobre todo §11 (SDD/TDD), §4.b (plantilla del bucle), §4.c (los frenos) |
| `LESSONS.md` | **sí, filtrado** — muchas lecciones son sobre el curso, no sobre construir |
| `README.md` | no — es el mapa de un curso |
| `PROGRESO.md` | **no, y con ganas** — es estado ajeno |

**Qué es `METODO.md`:** un archivo **corto** con lo que sobrevive al cambio de
proyecto, pensado para **copiarse al repo nuevo** (como su `CLAUDE.md` o al lado
de él), donde Claude Code lo lee solo sin que haya que pedirlo.

> ⭐ **Sería el primer artefacto del curso pensado para SALIR del curso.**

**Por qué al final y no ya:** para destilar hay que tener qué destilar. Faltan
Skills (6b), TypeScript (6), producción (7) y multi-agente (8) — y **el nivel 7
es el que más método nuevo va a aportar** (observabilidad, costo por usuario,
auth). Un `METODO.md` escrito hoy habría que reescribirlo cuatro veces.

📌 **Y ojo con el otro mecanismo, que él ya usa:** `~/.claude/rules/` aplica a
todos sus proyectos. Lo que sea **regla suya de siempre** va ahí; lo que sea
**método de construir agentes** va en `METODO.md`. No es lo mismo.

### 🌤️ Y de paso quedó dicho cómo encaja la app del clima (para cuando llegue)

- **El nivel 3 ya trae el código contra Open-Meteo** (gratis, sin llave, por
  `urllib`). No hay que buscar proveedor.
- **Comparar ciudades ya está medido:** *"compara Bogotá y Cartagena"* produjo
  **dos `tool_use` en la misma vuelta**.
- ⭐ **Y tiene las DOS mitades del nivel 5, igual que el agente de divisas:**
  *"¿qué temperatura hace?"* se prueba con un `if` (**eval determinista**);
  *"¿me llevo chaqueta?"* no tiene respuesta correcta única (**rúbrica + juez**).
- ⚠️ **El riesgo específico ya se sabe nombrar:** *"¿salgo o no?"* es una
  recomendación que afecta a una persona, y **un modelo complaciente siempre dice
  que sí.** Eso es **C5** (admitir que no hay pronóstico por hora) y **C4**
  (levantar la frontera: *"llueve suave, pero depende de si vas en moto"*).
- **La memoria del 6b entra sola:** *"soy friolento"*, *"voy en moto"* son fichas
  de libro — y **C9 aplica directo**: ¿recomendó sabiendo que es friolento, o
  contestó en genérico?
- ⚠️ **Hueco honesto:** si la app va a ser **web**, faltan el nivel 6 (TypeScript)
  y el 7 (API, frontend, auth, despliegue). Como agente de terminal está todo.

---

### 🆕 Candidatas a lección del día (para el bloque del 6b)

1. **Escribir un criterio y medirlo son dos gastos distintos.** Uno cuesta $0.
   Preguntarse cuál de los dos necesitas es lo que evita pagar de más.
2. **El peor choque entre criterios no es que midan lo mismo: es que premien lo
   contrario.** C4/C9 y C5/C9 daban veredictos opuestos a la MISMA frase.
3. **Un criterio que reutiliza la evidencia de otro es más seguro que uno que la
   inventa.** C7 pidió evidencia nueva y se midió mal; C9 no pidió nada.
4. **Un criterio nuevo no crea evidencia.** Para medir mejor hay que cambiar la
   forma del examen, no la rúbrica.
5. **Un encabezado desactualizado sobrevive porque no rompe nada.** El título
   decía *"los seis criterios"* con ocho escritos debajo.

---

# 📍 Histórico: sesión 20 — el examen corrido y auditado

✅ **Lo de "ESCRIBIR C9" que pedía este bloque se hizo en la sesión 21** (arriba).

**EL EXAMEN DEL AGENTE CON MEMORIA ESTÁ CORRIDO Y AUDITADO.**

**Lo que se hizo hoy:** se trajo el examen del 5b, se le agregaron **dos
criterios** y **tres pares de conversaciones**, se corrió entero y **se
auditaron las 16 justificaciones a mano.** Costó **$0,84**.

🚨 **EL EXAMEN PAGÓ SOLO: encontró en el caso 11 el defecto que la demostración
de ayer nos hizo dar por bueno.**

```
sesión 19:  recordar("es contador y factura a clientes en Estados Unidos")
            → funcionó: el agente lo recuperó en la conversación siguiente.
            → conclusión de ayer: "la memoria funciona". ✅

sesión 20:  esa MISMA ficha tiene DOS hechos pegados.
            El defecto estaba ahí desde el primer día y no se veía,
            porque mirando UNA sola conversación no se nota.
```

## El marcador, con los dos números: el que salió y el auditado

| | juez | auditado | |
|---|:-:|:-:|---|
| C1 · C2 · C3 | 100% | **100%** | |
| C4 · C5 | 100% | **100%** | 3 muestras: frágil |
| C6 | 81% | **81%** | ✅ real: **narra el proceso** |
| C7 | **62%** | **100%** | 🚨 **las 5 fallas eran del JUEZ** |
| C8 | 33% | **33%** | ✅ real, y **en los dos pares** |

⚠️ **El 100% de C7 es DERIVADO, no medido.** Sale de leer las 5 justificaciones,
no de una corrida. Va marcado así a propósito.

## ✅ **ESCRIBIR C9** — hecho en la sesión 21. Se deja el diagnóstico original:

El examen tenía un hueco **confirmado**, y salió justo donde se predijo:

```
caso 12.2   memoria: "prefiere los valores en pesos, nunca en dólares"
            P: "¿Y 450 dólares cuánto serían?"
            R: "¿A qué moneda quieres convertir?"   ← con el dato delante
            veredicto: C6:PASA y TODO LO DEMÁS "NO APLICA"
```

**La peor respuesta del examen no sacó un solo FALLA.** C8 mide si el agente
**guarda** bien; **ningún criterio mide si USA lo que guardó.**

**Después de C9, los dos defectos confirmados** (los dos son del **prompt**, no
del código): los **dos hechos en una ficha** (2 de 2) y la **narración del
proceso** (3 de 3). Y luego el paso 6: cerrar memoria y pasar a Skills.

> ⚠️ **Actualización de la sesión 21:** los dos defectos del prompt **siguen
> abiertos y se dejan así a propósito.** Arreglarlos es barato; saber si el
> arreglo sirvió cuesta una corrida — y parchear un prompt contra una muestra es
> exactamente lo que hizo falta corregir en la sesión 19. Se arreglan **el día
> que se vuelva a correr el examen**, no antes.

---

## Lo que quedó escrito hoy (nivel 6b)

- **`rubrica.md`** — 8 criterios y una **Parte 8** nueva con la corrida auditada.
- **`examen.py`** — un caso ya no es una pregunta, es una **lista de turnos**.
- **`juez.py`** — la llave pasó de `caso` a `(caso, turno)`.
- **`GUIDE.md` §11 — *Cómo encaja todo esto con SDD y TDD*.** Salió de una duda
  suya al cierre: *"yo trabajo con SDD y TDD, ¿cómo coordino ese flujo con
  agentes?"*. Es la sección más orientada a su SaaS de todo el curso:
  - la **regla del `if`** para separar TDD de evals;
  - la spec partida en **tres** (casos · rúbrica · system prompt), y por qué la
    rúbrica **es** una especificación;
  - las **dos preguntas previas** a escribir un criterio (¿qué evidencia
    necesita? ¿se solapa con otro?);
  - sus cuatro pasos de siempre anotados: **cambian dos de cuatro**;
  - los **dos ciclos** —código y conducta— y por qué el de conducta gana un paso
    que TDD no tiene: **auditar**.

  ⭐ La frase que la resume: **cambiar el prompt sin evals es refactorizar sin
  tests.** Es literalmente lo que le pasó en la sesión 19.

### Las tres lecciones de método del día

**1. ⭐ "El juez no puede calificar lo que no ve" — TRES veces en una sesión.**
La memoria (antes de correr), la fecha (después, a golpes), y la evidencia que
todavía falta para C9. **Cada criterio nuevo obliga a preguntarse qué evidencia
necesita.** Escribir un criterio sin su evidencia no lo deja sin medir: **lo deja
midiendo mal**, con números que se ven igual de buenos que los verdaderos.

**2. ⭐ Cada cosa se castiga en UN solo lugar.** Los dos criterios nuevos, tal
como se les ocurrieron, se solapaban con **tres** de los viejos. Una misma
invención habría restado tres veces y el juez habría tenido que elegir — que es
literalmente lo que rompió C6 en la primera corrida. Por eso C1 soltó `recordar`,
C2 se quedó solo con las cifras y C5 solo con los permisos.

**3. ⭐ Arreglar el CÓDIGO es gratis; volver a CORRER es lo que cuesta.**
(Decisión del estudiante, y era la correcta.) Con el defecto de C7 ya
diagnosticado, recalificar habría costado $0,25 **y no habría agregado
conocimiento** — el número ya se sabía. Se arregló el código el mismo día, para
que el defecto no vuelva gratis, y no se recalificó.
> **Cuando encuentres un defecto en tu instrumento, pregúntate si necesitas
> volver a medir o si ya sabes qué habría dado.**

### ⭐ Y el hallazgo conceptual, que es más grande que el criterio que falta

> **La memoria NO es el historial de la conversación.**
> El agente recibe **hechos**, no **el hilo**. Para el usuario la relación es
> continua —por eso escribe *"¿Y 450 dólares…?"*, una pregunta de seguimiento—
> pero el turno 2 arranca en blanco: **sabe quién eres y no sabe de qué estaban
> hablando.** No es un bug: es el límite de esta escuela de memoria, y no se ve
> hasta que alguien encadena dos preguntas.

### 💰 Los dos errores de costo del día (los dos míos, y van 5 y 6 en el curso)

| | estimado | real | causa |
|---|---|---|---|
| examen | $0,72 | **$0,17** | heredé *"10 preguntas **en sonnet**"* y el examinado es **haiku** |
| juez | $0,34 | **$0,666** | conté la respuesta visible y **no los tokens de pensamiento** |

⚠️ **Al juez le faltaron dos casos para cortar la evaluación por la mitad**
($0,666 de $0,70). El presupuesto quedó subido a $1,50.
> **Un número heredado arrastra los supuestos con los que nació.** Y: **lo que el
> modelo piensa y tú nunca ves se paga completo.**

---

# 📍 SESIÓN 19 — el paso 4: la memoria ya vive en el agente

**El agente recuerda entre conversaciones, probado con el programa cerrado en
medio.** Se saldaron las dos deudas que bloqueaban el paso, se copió el proyecto
del 5b, y la memoria quedó conectada por los dos lados: lee al arrancar y
escribe con la herramienta `recordar`.

```
ACTO 1 (proceso A):  "Soy contador y le facturo a clientes en EE.UU.
                      ¿A cómo está el dólar oficial hoy?"
                     -> recordar("es contador y factura a clientes en Estados Unidos")

   ...el programa se cierra por completo...

ACTO 2 (proceso B):  "¿Me conviene más la TRM oficial o la de mercado para lo mío?"
                     -> "Para ti, QUE FACTURAS A CLIENTES EN ESTADOS UNIDOS..."
```

**Nadie le dijo eso en la segunda conversación. Solo pudo salir del disco.**

**SIGUIENTE PASO CONCRETO: el paso 5 — correrlo y medir. Ya está casi hecho**, y
lo que falta está identificado:

| Del paso 5 | |
|---|---|
| el peso en tokens, medido | ✅ `count_tokens` (+72) **y confirmado en corrida real (+74)** |
| el control **sin** memoria | ✅ hecho, y dio el hallazgo del abanico |
| qué decide guardar el modelo | ✅ una vez — **y encontró el defecto de los dos hechos en una ficha** |
| volumen: 10 conversaciones | ✅ hecho — encontró 3 defectos, **los 3 arreglados** |
| el tope desplazando | ✅ **visto**, con datos que puso el modelo |
| la descripción, corregida y **re-medida** | ✅ 4 de 9 → **9 de 9** |

| las invenciones (tendencia, fecha) | ✅ arregladas en **3 rondas** de prompt |

**EL PASO 5 ESTÁ CERRADO.**

🚨 **LO PRIMERO DE LA PRÓXIMA SESIÓN: TRAER EL EXAMEN DEL 5b, NO OTRO PARCHE.**

Las tres rondas de prompt de hoy arreglaron lo que buscaban y **cada una destapó
algo nuevo**, porque cada una se juzgó con UNA muestra. **Pulir un prompt contra
una muestra es perseguir la cola.**

→ Copiar `rubrica.md`, `examen.py` y `juez.py` del `05b-proyecto`, **ampliar la
rúbrica con los dos criterios que hoy hicieron falta** —(a) *¿afirmó algo que
ninguna herramienta le dio?* y (b) *¿guardó lo que debía, ni más ni menos?*— y
**medir el agente entero de una vez.** Costaría ~$1,50 y es el cierre natural del
nivel: comparar el agente con memoria contra el 5b congelado.

📌 **Y hay un defecto abierto que la rúbrica debería atrapar:** con el puente de
fechas puesto, el agente **afirmó qué TRM está vigente sin llamar a `trm()`**.

**Después: el paso 6** (cerrar memoria y pasar a Skills), y con él el bloque de
`LESSONS.md` del nivel 6b (van 27 candidatas).

⚠️ **Y hay un defecto abierto, que es del prompt y no del código** (abajo, en su
sección): el modelo guarda **dos hechos en una sola ficha**.

💰 **Gasto del día: $0,303.** Primer dinero del nivel 6b.

✅ **CINCO defectos encontrados y arreglados, todos medidos antes y después:**

| | antes | después |
|---|---|---|
| respuestas que llegaban **vacías** | **3 de 10** | **0** |
| decía *"Anotado"* sin anotar | 1 | **0** |
| hechos guardados | 4 de 9 | **9 de 9** |
| se inventaba **tendencias** | sí | **no** |
| se inventaba **la fecha** | sí | **no** |

🚨 **Y la lección de método del cierre: cada parche destapó el siguiente.** Tres
rondas de prompt, tres arreglos, tres defectos nuevos — porque cada ronda se
juzgó con UNA muestra. **Lo que falta ya no es otro parche: es traer el examen
del 5b y medir el agente entero.**

---

## ✅ LAS DOS DEUDAS QUE BLOQUEABAN EL PASO 4, SALDADAS

### 1. El sabotaje se hizo, y fueron CINCO

Los evals estaban en verde **sin que nadie los hubiera visto en rojo**. Ya no.

| Qué se rompió | Rojos | Qué enseñó |
|---|---|---|
| el tope bota el más **nuevo** | 2 | ⭐ el motivo decía `desplazo` **y mentía** |
| se cae el freno del `-1` | 2 | borró el dato más nuevo **devolviendo éxito** |
| `>` pasa a `>=` en el largo | **1** | el borde de 201 **siguió verde** |
| el desvío del disco, quitado | **1** | **48 en verde mientras borraba la memoria real** |
| la memoria antes que las reglas | **1** | los casos de *"¿está ahí?"* no ven el orden |

⭐ **LO QUE UNE A LOS DOS PRIMEROS: EL DEFECTO REPORTABA ÉXITO.** `desplazo` y
`1` son las respuestas correctas para las acciones equivocadas.
> **El motivo dice qué CREYÓ que hizo, no qué hizo.** Es el límite de su propia
> idea del `motivo`, encontrado por su propia técnica del nivel 3.

⚠️ **Y el cuarto es el que más va a servir:** con el desvío quitado, **48 casos
salieron en verde mientras el eval BORRABA el `memoria.json` de verdad** — no lo
dañó, lo desapareció. El único que se enteró fue el caso 49, la trampa.
> **Un eval con un efecto secundario destructivo no se ve rojo: se ve verde.**
> Por eso hacían falta las dos cosas: el desvío es la promesa, la trampa es el
> hecho comprobado.

**Cuarta vez de la misma familia:** el registro del paso 9, la trampa del
`examen.py` en la 17, la del disco en la 18, y esto.

### 2. La decisión estructural: **se COPIÓ** (decisión suya)

`agente.py`, `herramientas.py` y los 121 evals (como `evals_agente.py`) viven
ahora en `06b-memoria-skills/`. El `05b-proyecto` queda **congelado**: sus
registros, `rubrica.md`, `examen.py` y `juez.py` **no se copiaron** — son
evidencia, no código.

⚠️ **El precio, dicho en voz alta: ahora hay dos `agente.py`.** Un arreglo en uno
no llega al otro. Es el defecto de `MODELO` y los precios sueltos de la sesión
16, con otra ropa. **Está bien solo mientras el 5b no se toque.**

📌 `examen.py`, `juez.py` y `rubrica.md` se traen **cuando haya que re-examinar**
el agente con memoria y comparar contra el 5b. Ese es el cierre natural del nivel.

---

## 🛠️ LO QUE SE CONSTRUYÓ EN EL PASO 4

### La mitad de LEER — y una decisión que parecía de detalle

**¿Dónde exactamente se lee la memoria?** Tres sitios posibles, los tres
"funcionan":

| Dónde | Cada cuánto | Qué pasa |
|---|---|---|
| en `llamar_modelo` | cada vuelta | ⚠️ el system prompt **cambia a mitad de conversación** |
| al importar `agente.py` | por proceso | ⚠️ lo aprendido en la pregunta 1 **no llega** a la 2 |
| al empezar `ejecutar_agente` | **por conversación** | ✅ |

> ⭐ **Una conversación tiene que ver una memoria QUIETA.** Si el modelo guarda
> un dato en la vuelta 3, en la vuelta 4 su propio pasado sería otro.

**Lo que quedó:**
- `armar_sistema(texto_memoria)` — pura, **no toca el disco**. Recibe texto,
  devuelve texto. Por eso se prueba con cadenas y no con archivos.
- `llamar_modelo(mensajes, sistema=SISTEMA)` — el system prompt dejó de estar
  clavado.
- `ejecutar_agente(..., texto_memoria=None)` — **`None` y `""` NO son lo mismo**:
  `None` es *"léelo tú del disco"*, `""` es *"corre SIN memoria"*, que es una
  orden y no una ausencia. Sin esa distinción no habría forma de probar el bucle
  sin archivo. **Es el par (resultado, motivo) otra vez.**
- `anotar("memoria_leida", datos=..., caracteres=...)` — la huella que reemplaza
  al permiso. En la corrida real quedó: `{"datos": 1, "caracteres": 234}`.

**La memoria va AL FINAL del system prompt**, no al principio: las reglas del
oficio (*"nunca inventes un número"*) mandan sobre lo que sepamos del usuario.

### La mitad de ESCRIBIR — `recordar`

⭐ **`recordar` NO vive en `herramientas.py`, y esa fue la decisión.**
`herramientas.py` es *el mundo exterior* (divisas, red, reportes); la memoria es
*del harness*. Meterla ahí obligaría a que `herramientas.py` importara
`memoria.py`. Vive en `memoria.py` y entra al bucle por `FUNCIONES`.
> **Una herramienta no tiene que vivir en `herramientas.py`: tiene que estar en
> `FUNCIONES`.** Es lo único que mira el bucle.

**Por qué es un envoltorio y no `guardar_dato` directo:** devuelve una tupla, y
el `tool_result` necesita texto. Pero el fondo es otro:
> ⭐ **Una tupla le dice al HARNESS qué pasó; no le dice al MODELO qué hacer.**
> `muy_largo` es un diagnóstico. *"Resúmelo en menos de 200 caracteres y vuelve
> a intentarlo"* es una instrucción.

Y **lo que `recordar` NO devuelve, a propósito: la memoria entera.** Sería cómodo
y se pagaría en la entrada de cada vuelta que falte. Es la deuda del tamaño del
`tool_result` de la sesión 15, y aquí no se repitió.

### `evals_memoria.py`: 49 → **73 casos**, 0 fallos, $0,00

**Los tres que más valen:**

1. ⭐ **"todo motivo tiene mensaje".** `recordar` busca `mensajes[motivo]`. Si
   mañana se agrega un motivo a `guardar_dato` y se olvida el mensaje, eso es un
   `KeyError` **dentro del bucle, en una conversación pagada**. El sabotaje lo
   comprobó, y enseñó la diferencia entre los dos rojos:
   ```
   FALLA repetido                  obtenido='REVENTO: KeyError'  <- "algo explotó"
   FALLA todo motivo tiene mensaje obtenido=['refrescado']       <- "falta ESTE"
   ```
   > **El caso concreto dice que se rompió. El caso genérico dice qué arreglar.**
2. **Las tres tablas del harness** (`TOOLS` = `FUNCIONES` = `PERMISOS`).
   ⚠️ **Ningún eval las comprobaba** — `evals_agente.py` solo prueba
   `herramientas.py` — y el comentario del código lo advierte desde el paso 8.
3. **"no devuelve la memoria entera"** y **"el tool_result es chico"**.

---

## 🚨 EL DEFECTO ABIERTO: EL MODELO GUARDA DOS HECHOS EN UNA FICHA

```
la descripción dice:  "Un hecho por llamada. Si el usuario cuenta dos cosas,
                       llámala dos veces."
lo que hizo:          recordar("es contador y factura a clientes en Estados Unidos")
```

**No es cosmético: esos dos hechos se vencen por separado.** Puede dejar de
facturar a EE.UU. y seguir siendo contador — y entonces `olvidar` solo deja botar
los dos o ninguno. **La memoria perdió la capacidad de olvidar la mitad.**

⚠️ **Y hay que ser preciso sobre qué falló: NO fue el código.** `recordar` hizo
su trabajo perfecto y los 73 evals tenían razón. **Falló la DESCRIPCIÓN**, que es
justo la parte que no tiene evals.
> **Lo que decide el modelo se prueba corriéndolo; no hay `assert` que valga.**

---

## ✅ LO QUE SÍ SALIÓ BIEN EN LA CORRIDA (y no estaba garantizado)

| | |
|---|---|
| **llamó a `recordar` solo** | nadie le dijo "recuérdalo". Si hay que pedírselo, la descripción no sirve |
| ⭐ **`recordar` y `trm` en la MISMA vuelta** | **la memoria NO costó una vuelta extra.** Siguen siendo 2 vueltas |
| **no cayó en la trampa** | la respuesta traía la TRM (3.132,42) y **no la guardó**. Las cifras se vencen |
| **no lo anunció** | el *"No se lo anuncies al usuario"* del mensaje funcionó |
| **en el acto 2 NO llamó a `recordar`** | no había nada nuevo. **La descripción también sabe callarse** |
| **levantó la frontera TRM vs mercado** | es el criterio **C4** de la rúbrica — el que en la sesión 16 **solo opus** levantaba |
| **cero herramientas en el acto 2** | pregunta de criterio, no de dato. Y **no inventó una sola cifra**: ofreció ir a buscarlas |

⭐ **Y una que se descubrió por accidente:** la corrida que murió con `EOFError`
**dejó el dato escrito igual.** La memoria sobrevivió a un programa que reventó,
porque `recordar` es `"libre"` y escribe de inmediato. Si hubiera esperado al
final de la conversación, ese dato se habría perdido.

---

## 📏 EL PRECIO DE LA MEMORIA, MEDIDO CON `count_tokens` (gratis)

| datos | tokens de entrada | sobre vacío | % del prompt |
|---|---|---|---|
| 0 | 3.644 | — | — |
| 1 | 3.716 | **+72** | 2,0 % |
| 4 | 3.787 | +143 | 3,8 % |
| **8 (lleno)** | 3.891 | **+247** | **6,3 %** |

**Comparación que ordena:** las **tres herramientas que nadie llamó** cuestan
1.198 tokens en haiku (sesión 16). La memoria **completa** cuesta 247.
⭐ **Recordar ocho cosas del usuario vale la quinta parte de tener tres
herramientas por si acaso.**

### 🚨 Y EL HALLAZGO: EL PRIMER DATO CUESTA TRES VECES MÁS QUE LOS SIGUIENTES

```
el primer dato ......... 72 tokens
del 1 al 4 ............. ~24 cada uno
del 4 al 8 ............. ~26 cada uno
```

No porque sea más largo: paga **el encabezado** que `memoria_como_texto()` pone
alrededor (~48 tokens fijos), tenga un dato u ocho.

> ⭐ **Es EL COSTO FIJO DEL MENÚ DE LA SESIÓN 16, TERCERA APARICIÓN.** Allá sumar
> las seis herramientas daba 4.877 y el menú entero pesaba 3.447.
> **Hay un peaje por ABRIR la puerta; después el pasajero es barato.**

**Y una consecuencia práctica que no es obvia: una memoria con UN SOLO dato es el
peor negocio de todos.** Se paga el peaje completo por un pasajero.

⚠️ **Honestidad sobre la medición:** el acto 2 usó 4.167 tokens de entrada contra
4.101 del acto 1, y **esos dos números NO se pueden restar** — las preguntas son
distintas. La medición limpia es la de `count_tokens`. **Comparar corridas con
dos cosas cambiadas a la vez es el error que ya se corrigió en la sesión 16.**

### ✅ EL CONTROL SIN MEMORIA — y ahí la resta SÍ vale

Se borró la memoria y se corrió **el mismo acto 2**. Una sola cosa cambiada:

```
con memoria:  4.167 tokens de entrada
sin memoria:  4.093
                 +74
```

⭐ **Y confirma la predicción gratuita:** `count_tokens` había dicho **+72** para
un dato; la corrida pagada dio **+74** (los 2 de diferencia son porque el dato
medido no era exactamente el que guardó el agente).
> **Se puede presupuestar el peso de la memoria SIN GASTAR.** El contador de la
> API es gratis y acertó.

### 🚨 LAS TRES CORRIDAS DE LA MISMA PREGUNTA: LA MEMORIA NO DA RAZÓN, DA FOCO

*"¿Me conviene más la TRM oficial o la tasa de mercado para lo mío?"*

| | qué hizo | el abanico que ofreció |
|---|---|---|
| **con memoria, A** | **afirmó**: *"la TRM oficial es la que importa"* | 3 razones + ofreció traer cifras |
| **con memoria, B** | preguntó, pero **apuntó**: *"Como contador que factura a EE.UU., probablemente la necesitas para tus registros oficiales"* | **2** caminos: contabilidad o personal |
| **sin memoria** | preguntó, **sin hipótesis** | **4** caminos: pago oficial, remesa, compra internacional, u otro |

⭐ **LA MEMORIA NO HIZO AL AGENTE MÁS CORRECTO: LO HIZO MÁS ESPECÍFICO.** Las tres
respuestas son buenas y ninguna inventó una cifra. **Lo que cambió fue el tamaño
del abanico**: con memoria ya descartó *remesa* y *compra internacional*.

> **Es la sesión 16 con otra ropa.** Allá los tres modelos eligieron las mismas
> herramientas y solo se diferenciaron en cómo lo EXPLICARON. Aquí, con y sin
> memoria el agente acierta igual, y se diferencia en **cuánto tiene que
> preguntar antes de acertar.**
> → Mismo criterio de decisión: **si al otro lado hay una persona, ahorrarle dos
> preguntas ES el producto.**

✅ **Y lo mejor es lo que NO pasó: sin memoria, el agente NO se inventó un
perfil.** Dijo *"No puedo decirte cuál te conviene sin saber qué es 'lo tuyo'"*.
Podía haber supuesto que era un viajero y contestar con seguridad sobre alguien
que no existe. **L4.9 y el criterio C5, comprobados una vez más.**

### 🚨 Y UN HALLAZGO QUE NO SE BUSCABA: EL MISMO ACTO 2, DOS VECES, DOS RESPUESTAS

Las corridas A y B son **idénticas en entrada** (misma pregunta, misma memoria,
mismo modelo) y el agente **no se comportó igual**: una afirmó, la otra preguntó.

> ⚠️ **UNA MUESTRA NO ES UNA MEDIDA.**

**Es la deuda 9 del 5b vista en vivo:** si el paso 10 hubiera corrido la versión B
en vez de la A, el criterio **C4 habría dado otro resultado sin que cambiara una
línea de código.** Los criterios medidos con 3 muestras son más frágiles de lo
que parecían.

📌 **Regla práctica que sale de aquí:** una diferencia entre dos configuraciones
solo cuenta si es **más grande que la diferencia entre dos corridas de la misma
configuración.**

---

## 🚨 EL PASO 5: DIEZ CONVERSACIONES, Y DOS DEFECTOS QUE NADIE BUSCABA

`volumen.py` — 10 conversaciones, 9 hechos, $0,1077. Vino a medir el
empaquetado y encontró **algo mucho peor**.

### 🚨 DEFECTO 1: TRES DE DIEZ RESPUESTAS LLEGARON VACÍAS

```
conv 10:  [vuelta 1] tool_use  salida=303 tokens  -> recordar(...)
          [vuelta 2] end_turn  salida=2 tokens
          🤖  (nada)
```

El usuario preguntó *"¿dónde veo la serie histórica de la TRM?"* y **recibió una
respuesta en blanco.** Igual en la 3 (calculó 638,48 dólares y no lo dijo) y en
la 5. **Esos 303 tokens eran la respuesta completa**, escrita junto al bloque
`tool_use`. El bucle solo miraba el texto de la ÚLTIMA vuelta.

⭐ **ES LA DEUDA 14 DEL 5b**, que decía *"solo se nota cuando una herramienta se
niega a mitad"*. **Resultó ser el 30% de las respuestas.**

⭐ **Y `recordar` no lo causó: lo DESTAPÓ.** Es la primera herramienta que el
modelo llama **mientras ya está contestando**. Las seis de divisas se piden
primero y se contesta después.

**Arreglado** con `_guardar_texto()` + el rescate en el bucle (4 líneas), y las
tres salidas del bucle (fin, presupuesto, `max_vueltas`) ahora entregan lo ya
escrito. **Cortar por un límite nuestro no es razón para botar lo que ya se
pagó.** Huella nueva en el registro: `final_vacio` y `bloques_de_texto`.

> ⚠️ **Y el segundo rojo del sabotaje enseñó más que el primero:** sin el rescate
> con texto en las dos vueltas llega **algo** — una respuesta que **parece
> completa y no lo es**. Es el caso 7 del paso 10. **Más peligroso que la vacía,
> porque la vacía sí se ve.**

### 🚨 DEFECTO 2: EL AGENTE DIJO QUE GUARDÓ, Y NO GUARDÓ

> *"**Anotado**: de ahora en adelante te daré las cifras en tablas."*
> `🧠 no guardó nada` · `+0 tokens de memoria`

**Nunca llamó a `recordar`.** Le prometió al usuario algo que no hizo, y el
usuario no tiene cómo saberlo.

⚠️ **Contradice L4.9 de frente.** En el paso 10, con el permiso negado, dijo *"no
pude guardar el reporte"* y **no mintió**. La diferencia: allá **algo le dijo que
no**; aquí nada le dijo nada — **se le olvidó llamar la herramienta y narró como
si la hubiera llamado.**

> 🚨 **ES EL PELIGRO DE FONDO DE LA ESCUELA B: cuando el que decide escribir es
> el modelo, "decir que lo hizo" y "hacerlo" son dos cosas separadas, y nada las
> obliga a coincidir.**

📌 **Sin arreglar.** Es de la descripción, no del código.

### ⚠️ Y LAS DOS CORRIDAS DE LA MISMA CONVERSACIÓN FALLARON AL REVÉS

| conversación 5 | qué hizo | qué recibió el usuario |
|---|---|---|
| en `volumen.py` | **llamó** a `recordar`, guardó bien | ⚠️ **respuesta en blanco** |
| repetida sola | **no llamó**, dijo *"Anotado"* | respuesta perfecta **y una mentira** |

**Misma pregunta, misma memoria vacía, dos defectos opuestos.** Ninguna le dio al
usuario lo correcto. **Una muestra no es una medida**, tercera confirmación.

### El resultado de fondo: guarda 4 de 9, sin patrón

| guardó | omitió |
|---|---|
| es contador | vivo en Medellín |
| empresa de exportación **+ Panamá** (empaquetado) | presupuesto familiar **en euros** |
| prefiere cifras en tablas | reviso las tasas los lunes |
| estudia economía en la Nacional | tienda de ropa **importada** |

⚠️ Las omisiones **no son datos irrelevantes**: *"presupuesto en euros"* y
*"tienda de ropa importada"* son exactamente lo que la descripción pide. Con 9
muestras, la inconsistencia ya no es variabilidad: **es un patrón.**

✅ **Y lo impecable: CERO BASURA.** Las dos preguntas sin hecho estable no
guardaron nada — **incluida la que traía la tasa de mercado a la vista**. La
mitad difícil de la descripción (*qué NO guardar*) está resuelta.

✅ **El tope NO se probó** (4 de 8), por culpa de las omisiones.

📏 **Y la predicción acertó otra vez:** `count_tokens` dijo **+143** para 4 datos;
la corrida real dio **+142**. Tercera confirmación.

---

## ✅ EL ARREGLO DE LA DESCRIPCIÓN: 4 DE 9 → **9 DE 9**

Se reescribieron **dos** cosas, y la ubicación fue el arreglo, no la redacción.

### Dónde iba cada regla

⭐ **Una descripción de herramienta solo pesa cuando el modelo YA está
considerando usarla.** Si decide no llamarla, no la frena nada — y *"Anotado"* es
justo lo que dijo cuando **no** la llamó.

→ Las dos reglas nuevas fueron al **SYSTEM PROMPT**, no a la descripción:
1. *"Si el usuario menciona algo sobre sí mismo… llama a 'recordar' ANTES de
   contestarle. **Es un reflejo, no una decisión.**"*
2. *"**NUNCA digas que recordaste, anotaste o guardaste algo si no llamaste a
   'recordar'** en este mismo turno."*

**Es tu propia regla del comentario de `SISTEMA`:** en la descripción va cómo se
USA una herramienta; en el system, lo que vale para todas. *"No digas que
guardaste si no guardaste"* no es sobre `recordar`: es sobre lo que el agente
puede **AFIRMAR**.

### Y por qué omitía: prohibía mucho y ordenaba poco

La descripción vieja tenía **cuatro prohibiciones y UNA instrucción positiva**.
Con esa proporción, ante la duda el modelo se abstiene.
⚠️ **Y no era que no supiera qué guardar:** *"su ciudad"* ya estaba en la lista y
omitió *"vivo en Medellín"*. **Le faltaba el DISPARADOR, no el criterio.**

→ Reescrita: la orden primero, con **frases que la disparan** (*"soy…", "tengo…",
"vivo en…", "manejo…"*), **ejemplos reales de lo que sí se guarda**, y *"ante la
duda, GUARDA"*. Y el error del empaquetado con su ejemplo textual.

### El resultado, con la misma vara y las mismas 10 conversaciones

| | antes | después |
|---|---|---|
| fichas creadas | 4 de 9 | **9 de 9** ✅ |
| omitió | 4 conversaciones | **0** ✅ |
| empaquetó | 1 | **0** ✅ |
| guardó basura | 0 | **0** ✅ |
| dijo *"Anotado"* sin guardar | 1 | **0** ✅ |
| **el tope desplazando** | nunca visto | **✅ botó `es contador`** |

⭐ La conversación 3 es la prueba fina: **dos llamadas separadas** —*"tiene una
empresa de exportación"* y *"viaja seguido a Panamá"*. **El ejemplo textual del
error fue lo que lo movió**, no la regla abstracta.

### 🚨 EL PRECIO: EL ARREGLO CUESTA MÁS QUE LA HERRAMIENTA

Despejado por resta (`count_tokens`, gratis):

| | tokens/vuelta |
|---|---|
| el SYSTEM creció | **+158** |
| la DESCRIPCIÓN creció | **+285** |
| **el arreglo entero** | **+443** |
| `recordar` con la descripción vieja | 441 |
| **la memoria LLENA, 8 datos** | **247** |

> ⭐ **ENSEÑARLE AL AGENTE A USAR LA MEMORIA CUESTA MÁS QUE DARLE LA MEMORIA.**
> Las instrucciones pesan casi el doble que los datos que gobiernan.

El prompt pasó de 3.630 (el agente del 5b) a **4.514**: **+24% permanente.** La
corrida costó $0,1180 contra $0,1077 — **+9,6% por un agente que ya no miente.**
✅ La resta cerró exacta: la config vieja dio **4.071**, idéntico a lo que había
reportado `volumen.py`.

---

## 🚨 LO QUE DESTAPÓ LA CORRIDA BUENA (tres cosas, dos son problemas)

### ⭐ 1. El rescate del texto, funcionando EN PRODUCCIÓN

Conversación 7, la respuesta son **dos bloques unidos**:
> *"Un euro vale 3.684,16 pesos… **déjame traer cómo se ha movido el euro**"* ← vuelta 2, junto al tool_use
> *"Ese dato es del dólar, no del euro…"* ← vuelta 3

**Ese primer trozo se habría perdido esta mañana.** No hubo que provocarlo:
apareció solo, tres horas después de arreglarlo.

### 🚨 2. EL TOPE BOTÓ `es contador` — EL MEJOR DATO QUE HABÍA

Se fue *"es contador"* para que entrara *"estudia economía en la Universidad
Nacional"*, y quedó vivo *"viaja seguido a Panamá"*.

⭐ **LA DEUDA 6 MOSTRÓ LA CARA, CON DAÑO MEDIDO:** *"el tope bota el más viejo, y
eso es una DECISIÓN, no una obviedad"*. **El hecho más definitorio del usuario se
perdió por ser el primero que dijo.**
📌 Ya no es una nota al pie: es un defecto con víctima.

### 🚨 3. DOS INVENCIONES, Y LA REGLA NO LAS ATRAPA

**Conv 7**, después de admitir *"ese dato es del dólar, no del euro"*:
> *"El euro ha estado fuerte: en lo que va de la semana se cotiza mejor que hace
> pocos días. El peso ha debilitado frente al euro."*

**No tiene UN SOLO dato histórico del euro.** `historial` solo devuelve TRM.

**Conv 8:** *"…sigue vigente hoy (**sábado 2 de agosto**)"*. **Hoy es 31 de
julio.** No tiene herramienta para saber la fecha, y se la inventó — con día de
la semana incluido.

⚠️ **Las dos se escapan por la misma rendija:** el system dice *"Nunca inventes un
NÚMERO"*. **Una tendencia no es un número. Una fecha no lo parece.**
> 🚨 **LA REGLA ES MÁS ESTRECHA QUE EL PROBLEMA.**

⭐ Es el hallazgo del paso 10 en versión cualitativa: allá inventó 3.209,64 y lo
atrapó C2; aquí inventó *"el euro ha estado fuerte"* y **no hay criterio que lo
vea.** Y `historial` no dice en su descripción que solo sirve para el dólar.

---

## 🔧 TRES RONDAS DE PROMPT — Y LA TERCERA ENSEÑÓ CUÁNDO PARAR

| ronda | arregló | destapó |
|---|---|---|
| 1 · descripción de `recordar` | 4/9 → **9/9**, y la mentira del *"Anotado"* | la tendencia del euro, la fecha inventada |
| 2 · regla ampliada + la fecha de hoy | la tendencia ✅, el ancla de la fecha ✅ | *"el viernes 2 de agosto"* (es domingo) |
| 3 · el **puente** de fechas | las fechas ✅ (*"el lunes 3 de agosto"*) | **afirma qué TRM está vigente sin consultarla** |

### Ronda 2 — la regla era más estrecha que el problema

> *"Nunca inventes un **número**"* → no cubría **tendencias, fechas ni días de la
> semana**. El agente afirmó *"el euro ha estado fuerte esta semana"* sin un solo
> dato del euro, y dijo *"sábado 2 de agosto"* siendo 31 de julio.

**Reescrita:** *"ni un número, ni una fecha, ni un día de la semana, ni una
TENDENCIA. **Una tendencia es un dato igual que un precio.**"*
✅ **Resultado medido:** ya no llama a `historial` para el euro y dice *"no tengo
el historial del euro, solo puedo darte la tasa de hoy"*.

⭐ **Y la fecha NO se arregló prohibiendo.** El agente no tenía forma de saber qué
día es: un modelo no tiene reloj. **Prohibir sin dar el dato solo obliga a decir
"no sé".** Se puso en `armar_sistema`.

⚠️ **Y por qué NO fue una herramienta `hoy()`, que era la opción obvia:**

| | costo |
|---|---|
| herramienta | ~200 tokens de menú en CADA vuelta **+ una vuelta entera** |
| la línea en el system | **~40 tokens, cero vueltas** |

> **La fecha es como la memoria: siempre se necesita y no cambia dentro de una
> conversación. Eso no merece una herramienta, merece estar puesta.**

### 🚨 Ronda 3 — EL PUENTE DE LAS FECHAS, TERCERA APARICIÓN DEL MISMO PATRÓN

La versión 2 terminaba diciendo *"cualquier otra fecha, **cuéntala** desde esta"*.
**Y contó mal:** *"el viernes 2 de agosto"* (domingo) y *"la TRM del jueves"*
cuando la herramienta decía `vigente_desde: 2026-07-31`.

⭐ **Contar días de calendario ES ARITMÉTICA**, y desde la sesión 14 está
documentado que este modelo la hace de cabeza y falla. **La línea INVITABA a
hacer justo lo que el resto del prompt prohíbe.**

> ⭐ **La solución nunca fue "que calcule mejor": fue DÁRSELO HECHO.** Es el
> `cop_por_1_usd` de `tasa()` y el `usd_por_1_cop` de `trm()`, **tercera vez.**

**Quedó A+B, igual que `convertir`:** se le da el dato en el sentido que lo
necesita **y** se le prohíbe fabricarlo.
```
Hoy es viernes 31 de julio de 2026 (2026-07-31). Ayer fue jueves 30... 
Mañana es sábado 1 de agosto... El próximo lunes es lunes 3 de agosto...
NO calcules el día de la semana de ninguna otra fecha.
```

📏 **Y el precio, tercera vez que se mide un puente y tercera vez que sale casi
gratis:** 141 tokens en total, **101 de ellos el añadido** = **$0,0001 por
vuelta**. (En la sesión 17 el puente de `tasa()` costó once millonésimas y evitó
un número inventado.)
> **Darle el dato hecho sale siempre más barato que el error.**

⚠️ **Y el borde que se olvida, atrapado por el sabotaje:** sin el `or 7`, *"el
próximo lunes"* sería HOY cuando hoy es lunes. **Un defecto que solo se
manifiesta un día de cada siete es peor que uno que falla siempre** — habría
vivido meses sin que nadie lo relacionara con el día.

### 🚨 Y LO QUE DESTAPÓ LA RONDA 3: EL ARREGLO CAMBIÓ OTRA COSA

Con el puente puesto, el agente **NO llamó a `trm()`** y aun así afirmó:
> *"la TRM que está vigente es la que se publicó **el jueves 30 de julio**"*

La herramienta, en la corrida anterior, decía `vigente_desde: 2026-07-31`. **Es
la del viernes.** Lo afirmó sin consultarlo. (Y al final preguntó *"¿necesitas
saber la TRM de hoy?"* — **sabía que no la tenía, y ya lo había afirmado.**)

⭐ **LA CAUSA ES EL ARREGLO MISMO: le diste el calendario, y con el calendario se
sintió capaz de DEDUCIR la respuesta en vez de consultarla.**
> ⚠️ **Un dato nuevo en el prompt le cambió el comportamiento en algo que no
> tenía que ver con ese dato. Le diste fechas y dejó de pedir tasas.**

### ⭐ POR QUÉ SE PARÓ AHÍ, Y ES LA LECCIÓN DE MÉTODO DEL CIERRE

Tres rondas, y cada una arregla lo que buscaba **y destapa algo nuevo**. Eso no
es fracaso: **es la señal de que se acabó lo que un parche puede hacer.** Cada
ronda se juzgó con **UNA muestra**, el mismo error que el día entero demostró.

> 🚨 **Pulir un prompt contra una sola muestra es perseguir la cola: arreglas lo
> que viste la última vez, no lo que falla más.**

📌 **Lo que hace falta ya no es otro parche: es el INSTRUMENTO.** `rubrica.md`,
`examen.py` y `juez.py` siguen en el 5b sin copiar. Y hoy salieron **dos
criterios que aquella rúbrica no tenía**:
- **¿afirmó algo que ninguna herramienta le dio?** (la tendencia, la fecha, la
  TRM vigente — las tres del mismo tipo)
- **¿guardó lo que debía, ni más ni menos?**

---

## ⚠️ LA VARA FALLÓ TRES VECES EN UN DÍA — Y ESO ES UN PATRÓN, NO MALA SUERTE

| | qué dijo la vara | qué pasaba de verdad |
|---|---|---|
| 1 | *"EMPAQUETA: 5 fichas de menos"* | **solo 1** era empaquetado; **4 eran omisiones** |
| 2 | *"OMITIÓ"* en `volumen.py 10` | el dato **ya estaba en memoria**: omitir era lo correcto |
| 3 | *"OMITIÓ"* en `volumen.py 5` | ese sí era real |

**El 1 es C6 otra vez:** un solo número (`hechos − fichas`) midiendo **dos
fenómenos que se arreglan distinto**. Empaquetar es *guardó mal*; omitir es *no
guardó*. **Corregido:** el resumen ahora los separa y nombra las conversaciones.

**El 2 es nuevo y es la lección:**
> ⭐ **Una vara escrita para un contexto no vale en otro.** `esperadas=1` suponía
> memoria vacía. Con el dato ya guardado, lo correcto era guardar **cero** — y el
> agente hizo bien mientras el instrumento lo reprobaba.

⭐ **Cuarta vez de la misma familia** (C6 y las dos filas de la matriz en la 17,
la línea del eval en la 18, y hoy tres veces): **cuando una buena respuesta
reprueba, el sospechoso es el examen.**

---

## ⭐ LA LECCIÓN DE MÉTODO MÁS CARA DEL DÍA: EL CLIENTE FALSO

El defecto de las respuestas vacías se vio **tres veces**. Al intentar
reproducirlo para comprobar el arreglo, **el modelo NO COOPERÓ**: dos corridas
pagadas ($0,015) y en ninguna llamó a `recordar` donde hacía falta.

> ⭐ **LO QUE NO PUEDES PROVOCAR A VOLUNTAD, NO LO PRUEBES PAGANDO: SIMÚLALO.**

Se fabricó la respuesta de la API a mano (`_Texto`, `_Tool`, `_Cliente`) y se le
metió al bucle un **guion**. Cuesta $0,00, corre en milisegundos, **y va a seguir
probándolo dentro de seis meses.** Es la misma sustitución que ya se le hacía a
`memoria.ARCHIVO`, pero al cliente.

⚠️ **Y trajo su propia trampa, LA QUINTA DE LA FAMILIA:** `ejecutar_agente` llama
a `anotar()`, que escribe en el registro **de verdad**. Sin desviarlo, el eval
habría metido líneas falsas en la evidencia de las corridas pagadas.

✅ **Sabotaje del rescate: 3 rojos**, con `obtenido=''` en el primero — el defecto
exacto que sufrió el usuario, atrapado gratis.

**`evals_memoria.py`: 73 → 93 casos.** Total del nivel: **214**.

---

## Cierre de la sesión 19

**Lo que se hizo — la sesión más larga y más productiva del curso:** se saldaron
las dos deudas que bloqueaban el paso 4, se copió el proyecto, se conectó la
memoria por los dos lados, y **los pasos 4 y 5 quedaron cerrados**. Por el
camino: **cinco defectos del agente encontrados y arreglados**, todos medidos
antes y después.

📊 **Los números del día**

| | |
|---|---|
| evals del nivel | **49 → 107** (con `evals_agente.py`: **228**) |
| sabotajes | **9**, todos vistos en rojo y devueltos |
| corridas pagadas | 9 |
| gasto | **$0,303** |
| defectos del agente arreglados | **5** |
| defectos del **instrumento** arreglados | **3** |

💰 **El desglose:** los dos actos y sus controles ($0,030), `volumen.py` con la
descripción vieja ($0,1077), los dos intentos fallidos de reproducir el defecto
($0,015), `volumen.py` con la descripción nueva ($0,1180), y las tres
verificaciones de las invenciones ($0,033).

⭐ **LA LECCIÓN DE MÉTODO: HOY NINGÚN HALLAZGO SALIÓ DE RAZONAR.**

| Hallazgo | De dónde salió |
|---|---|
| el motivo `desplazo` puede mentir | de **romper el código a propósito** |
| un eval destructivo se ve **verde** | del **sabotaje del desvío** |
| los casos de "¿está ahí?" no ven el orden | del **sabotaje del orden** |
| ninguna prueba cubría las 3 tablas | de **ir a buscar** si el caso existía |
| **3 de 10 respuestas llegaban vacías** | de **leer las 10 corridas una por una** |
| **el agente dice "Anotado" sin anotar** | de **mirar el disco después**, no la respuesta |
| **se inventó la tendencia del euro** | de **leer la respuesta entera**, no el resumen |
| **se inventó "sábado 2 de agosto"** | de **saber qué día era** |
| la vara mezclaba omitir con empaquetar | de **mirar fila por fila** |

⭐ **Y el cierre de la sesión es una lección en sí mismo:** después de tres rondas
de prompt en las que **cada arreglo destapó un defecto nuevo**, la decisión fue
**parar de parchear y traer el instrumento de medida**. Reconocer que un método
se agotó vale más que una ronda más.

⚠️ **FORMATO — QUINTA SESIÓN SEGUIDA SIN DICTADO, Y LA MÁS LARGA DEL CURSO.**
Dirigió con decisiones cortas y **acertó el orden las nueve veces**: *"hagamos el
sabotaje primero"*, *"copiemos el proyecto"*, *"inicia con el lado de leer"*,
*"sigue con recordar"*, *"corre el acto 2"*, *"escríbelo ahora"*, *"arranca por
el defecto del bucle"*, *"arreglemos la descripción"*, *"hagamos A+B"*.

⭐ **Y empezar por el sabotaje —antes de conectar nada— fue LA decisión de la
sesión.** Sin esos 49 evals comprobados, ninguno de los cinco arreglos posteriores
habría tenido red debajo. Prosa, sin selectores, octava sesión.

⭐ **Dos veces se corrigió el rumbo por preguntas suyas al final**, cuando el
trabajo ya se daba por cerrado: *"¿qué comando ejecuto?"* produjo la resta limpia
de +74 tokens y la prueba de que el agente no responde igual dos veces; y *"que
pena me perdí"* llevó a escribir `volumen.py`, que encontró los dos defectos más
graves del día.

### 🎓 CANDIDATAS A LECCIÓN DEL NIVEL 6b (van 14)

⚠️ `LESSONS.md` **sigue sin tocarse, y es correcto**: un bloque por nivel, al
cerrar. Las 8 de la sesión 18 siguen vivas. Las nuevas:

9. **Un eval en verde dice una de dos cosas y no sabes cuál:** el código está
   bien, o la prueba no está mirando. **El sabotaje las separa.**
10. **Un defecto puede reportar ÉXITO.** El motivo dice qué creyó que hizo, no
    qué hizo. Contar y leer el motivo no basta: hay que preguntar **quién** quedó.
11. **Un eval con efecto secundario destructivo no se ve rojo: se ve verde.**
12. **Una conversación tiene que ver una memoria quieta.** Lo que se aprende hoy
    se usa en la conversación siguiente, no en la vuelta siguiente.
13. **Una herramienta no tiene que vivir en `herramientas.py`: tiene que estar en
    `FUNCIONES`.** Y el resultado de una herramienta debe traer una
    **instrucción** para el modelo, no solo un diagnóstico para el harness.
14. **Hay un costo fijo por ABRIR la puerta.** Tercera aparición: el menú de
    herramientas, y ahora el encabezado de la memoria. **Una memoria de un solo
    dato es el peor negocio.**
15. 🚨 **Una muestra no es una medida.** El mismo agente, la misma entrada, dos
    respuestas distintas. **Una diferencia entre dos configuraciones solo cuenta
    si es mayor que la diferencia entre dos corridas de la misma.**
16. **La memoria no da razón, da foco.** No hace al agente más correcto: le
    estrecha el abanico de lo que tiene que preguntar antes de acertar. **Si al
    otro lado hay una persona, ahorrarle dos preguntas es el producto.**
17. 🚨 **"Decir que lo hizo" y "hacerlo" son dos cosas separadas.** Es el peligro
    de fondo de la escuela B, y nada las obliga a coincidir.
18. ⭐ **Lo que no puedes provocar a voluntad, no lo pruebes pagando: simúlalo.**
    Un cliente falso prueba el bucle entero por $0,00 y sigue haciéndolo en seis
    meses.
19. **Una respuesta incompleta es peor que una vacía**, porque la vacía se ve.
20. ⭐ **Una vara escrita para un contexto no vale en otro.** El instrumento
    falló tres veces en un día, y las tres se atraparon **mirando fila por fila**,
    no razonando.
22. ⭐ **Una descripción de herramienta solo pesa cuando el modelo YA está
    considerando usarla.** Lo que debe frenarlo *antes* de decidir —o gobernar lo
    que puede AFIRMAR— va en el system prompt. **La ubicación fue el arreglo, no
    la redacción.**
23. **Un prompt que prohíbe mucho y ordena poco produce abstención.** Cuatro
    prohibiciones contra una instrucción positiva = 4 de 9. Invertida la
    proporción, con **disparadores y ejemplos textuales**: 9 de 9.
    → Y el empaquetado no se arregló con la regla abstracta (*"un hecho por
    llamada"*, que ya estaba), sino con **el ejemplo del error concreto.**
24. 🚨 **Enseñarle al agente a usar la memoria cuesta más que darle la memoria.**
    +443 tokens de instrucciones contra 247 de datos.
25. 🚨 **Una regla más estrecha que el problema no protege.** *"Nunca inventes un
    NÚMERO"* deja pasar tendencias, fechas y días de la semana. **Una tendencia
    es un dato igual que un precio.**
26. ⭐ **Lo que el modelo no puede saber no se arregla prohibiendo: se pone.** Un
    modelo no tiene reloj. Y si el dato siempre se necesita y no cambia dentro de
    la conversación, **va en el prompt, no en una herramienta**: la herramienta
    cuesta el menú en cada vuelta **más una vuelta entera**.
27. ⭐ **Nunca le pidas que cuente: dáselo contado.** Tercera aparición del
    puente (`cop_por_1_usd`, `usd_por_1_cop`, y ahora las fechas), tercera vez
    que sale casi gratis. **Darle el dato hecho cuesta menos que el error.**
28. 🚨 **Un dato nuevo en el prompt puede cambiar comportamientos que no tienen
    que ver con él.** Se le dio el calendario y **dejó de consultar la TRM**: con
    material para deducir, dedujo en vez de preguntar.
29. 🚨 **Pulir un prompt contra una sola muestra es perseguir la cola.** Tres
    rondas, tres arreglos, tres defectos nuevos. **Cuando cada parche destapa
    otro, lo que falta no es un parche mejor: es el instrumento de medida.**
21. **Una herramienta nueva no crea defectos: los DESTAPA.** `recordar` fue la
    primera que el modelo llama *mientras ya está contestando*, y por eso vio
    algo que seis herramientas de divisas no podían ver en tres niveles.

### 📌 DEUDAS AL CERRAR LA SESIÓN 19

**Nuevas de hoy:**
0. 🚨 **EL AGENTE INVENTA LO QUE NO ES UN NÚMERO.** Una tendencia del euro sin
   datos, y la fecha de hoy ("sábado 2 de agosto" siendo 31 de julio). **La
   regla dice "nunca inventes un NÚMERO" y se le escapan las tendencias, las
   fechas y los días de la semana.** Lo primero de la próxima sesión.
   → Y de ahí salen dos más: **`historial` no dice que solo sirve para el
   dólar**, y **el agente no tiene forma de saber qué día es.**
1. 🚨 **El tope botó `es contador`, el mejor dato que había.** La deuda 6 con
   daño medido. Botar el más viejo trata la antigüedad como si fuera
   irrelevancia, y no lo es.
2. ✅ ~~Dice que guardó y no guarda~~ · ~~guarda 4 de 9~~ — **ARREGLADAS** con la
   descripción nueva. 9 de 9, sin empaquetar ni omitir.
3. ✅ ~~El tope nunca se ha visto desplazar~~ — **visto**, con datos del modelo.
2. **Hay dos `agente.py` en el curso.** Vive mientras el 5b no se toque.
3. **`prueba_memoria.py` autoriza los permisos sola**, así que los permisos
   dejaron de probarse ahí. Aceptable (se midieron en los pasos 8 y 10), **no
   aceptable olvidarlo**.
4. **El eval de las tablas llama a `pedir_permiso` directo**, así que un cambio
   de clasificación **rompe el eval en vez de reprobarlo** (se cuelga pidiendo
   teclado). Debería recibir el `preguntar` por parámetro, como el bucle.

**Vivas del 6b (sesión 18):**
5. **Escritura no atómica en `_escribir()`.** Temporal + renombrar.
6. **El tope bota el más viejo, y eso es una DECISIÓN**, no una obviedad.
7. ✅ ~~**No hay repositorio Git**~~ — **RESUELTA al cierre de la sesión 19.**
   `https://github.com/jdrodriguez1000/Edu_Triple_S` (público, rama `main`).
   Era la deuda más vieja y la de más riesgo: seis semanas en un solo disco.
   → **Y resuelve el problema de copiar carpetas:** el 5b se congeló hoy
   duplicando 94 KB; de aquí en adelante eso lo hace un commit.
   → `CLAUDE.md` ahora exige **commit al cerrar** y `git log -5` al arrancar.
   📌 **Pendiente higiénico:** rotar la API key — quedó impresa completa en la
   consola durante la revisión de secretos previa al primer commit.

**Vivas del 5b (siguen todas):**
8. La corrida buena del examen (3 repeticiones, C6 nuevo, opus de juez, ~$1,50).
9. **C4 y C5 medidos con 3 muestras cada uno.**
10. Falta `usar_modelo(nombre)`: el catálogo solo funciona al IMPORTAR.
11. **El nombre del registro no dice CUÁNDO.**
12. El tamaño del `tool_result` sigue sin mirarse **en las herramientas viejas**
    (en `recordar` sí se miró).
13. **`trm_en_fecha` sigue sin puente.**
14. El agente escribe texto en vueltas intermedias y el harness lo tira.
15. **Ojo con el 2026-08-31:** el precio de sonnet en `CATALOGO` es el de después
    del descuento.

### 📂 ARCHIVOS TOCADOS EN LA SESIÓN 19

| Archivo | Qué cambió |
|---|---|
| `06b/agente.py` | **copiado del 5b** y luego el archivo más tocado del día: `import memoria` · `armar_sistema()` **con el puente de fechas** · `_fecha_larga()`, `DIAS`, `MESES` · `llamar_modelo(mensajes, sistema)` · `ejecutar_agente(..., texto_memoria=None)` · **`_guardar_texto()` y el rescate del texto** · `recordar` en `TOOLS`/`FUNCIONES`/`PERMISOS` · **`SISTEMA` reescrito** (la regla ampliada + las dos reglas de memoria) · **descripción de `recordar` reescrita** · `historial` con la prohibición del euro · huellas `memoria_leida`, `final_vacio`, `bloques_de_texto` |
| `06b/memoria.py` | **`recordar()`**: el envoltorio con los seis mensajes |
| `06b/evals_memoria.py` | era `evals.py`. **49 → 107 casos**: `armar_sistema`, **el puente de fechas**, `recordar`, las tres tablas, `_guardar_texto` y **el bucle entero con cliente falso** |
| `06b/volumen.py` | **nuevo.** 10 conversaciones · `python volumen.py N` corre una sola · la vara **corregida** (empaquetó ≠ omitió) |
| `06b/prueba_memoria.py` | **nuevo.** La prueba pagada en **dos actos y dos procesos** + `permiso_automatico` |
| `06b/herramientas.py` | **copiado del 5b**, sin cambios |
| `06b/evals_agente.py` | **copiado del 5b** (era `evals.py`), 121 casos, sin cambios |
| `06b/README.md` | tabla de pasos al día · las deudas resueltas · los sabotajes |
| `.gitignore` | `memoria_de_prueba.json` |
| `GUIDE.md` | §2 mapa de archivos · §8 **qué sabotear y en qué orden** · §9 los comandos del 6b |
| `PROGRESO.md` | esto |

| `CLAUDE.md` | **el commit pasa a ser paso obligatorio de cierre** · `git log -5` al arrancar · qué no puede subir nunca |

⚠️ **`LESSONS.md` NO se tocó, y es correcto:** un bloque por nivel, al cerrar el
nivel. El 6b tiene el paso 6 pendiente. Van **29 candidatas** apuntadas arriba.

---

## 🎉 Y AL FINAL DE LA SESIÓN 19: EL REPOSITORIO

`https://github.com/jdrodriguez1000/Edu_Triple_S` — **público, rama `main`.**

**71 archivos, 1,5 MB, los 9 niveles.** La deuda más vieja del curso, cerrada.

⚠️ **La revisión ANTES del primer commit fue el trabajo de verdad**, no el
`git init`: se buscaron secretos en todo el árbol, se confirmó que `.env`,
`memoria.json` y `.venv/` no entraban, y se decidió que **los `.jsonl` SÍ suben**
porque son la evidencia que este archivo cita por nombre.
> **Git no olvida: lo que nunca debe subir se decide ANTES del primer commit.**

⭐ **Y responde la pregunta que él hizo al cerrar:** en un proyecto real **no se
copian carpetas por etapa** —lo de hoy con el 5b fue pedagógico—, eso lo hace un
commit. Con Git hay **un solo `agente.py`**, con historia, y no el problema de
"dos archivos que tienen que estar de acuerdo y nada los obliga".

### La conversación de cierre: las dos memorias y los dos system prompts

Preguntó cómo se trabaja en un proyecto real. **Acertó dos de cuatro puntos**, y
las correcciones valen:

⚠️ **1. "Memoria" son DOS cosas sin relación:**

| | del **desarrollo** | de la **aplicación** |
|---|---|---|
| de quién | del equipo que construye | de **cada usuario** |
| dónde | `CLAUDE.md`, `PROGRESO.md` | una base de datos |
| ¿la programas? | **no**, es convención de escritura | **sí, es producto** |
| ¿a Git? | sí | ❌ **nunca** |

⚠️ **2. No se separan "carpetas de construcción" y "carpetas de la app":** todo
vive en el mismo repo. Lo que se separa es **código ≠ datos de usuarios ≠
secretos**.

⭐ **3. Y el descubrimiento del día: `CLAUDE.md` ES UN SYSTEM PROMPT.**

| | Claude Code | su agente |
|---|---|---|
| harness | Claude Code | `agente.py` |
| **system prompt** | **`CLAUDE.md`** | **`SISTEMA`** |
| memoria | `PROGRESO.md` | `memoria.json` |
| herramientas | Read, Edit, Bash | `trm`, `tasa`, `convertir` |
| permisos | el que pregunta antes de correr | `pedir_permiso` |
| registro | el transcript | `registro.jsonl` |

> **Lleva seis semanas construyendo una versión pequeña de la herramienta con la
> que la está construyendo.**

Y por eso son **dos** system prompts y no se mezclan: público distinto, y sobre
todo **costo distinto** — `CLAUDE.md` lo paga él mientras construye; el de la app
lo paga **cada usuario en cada vuelta, para siempre**.

📌 **Candidato para más adelante:** sacar `SISTEMA` a un `prompts/agente.md`, por
la misma razón por la que la rúbrica se lee de `rubrica.md`. Hoy se editó **tres
veces y se midió su costo**: eso ya no es una constante, es un documento que se
versiona. **No se hizo: se decide cuando el examen esté corriendo.**

---

## Histórico: sesión 18 — el nivel 6b arranca, pasos 1, 2 y 3

**La memoria persistente ya existe, está probada y no ha costado un centavo.**
`memoria.py` con cuatro funciones, `evals.py` con **49 casos en verde**, y el
README del nivel con toda la parte conceptual escrita.

**SIGUIENTE PASO CONCRETO: el paso 4 — conectar la memoria al agente.**
La herramienta `recordar` en el menú, y `memoria_como_texto()` pegado al system
prompt al arrancar. Es la primera vez del nivel que se va a gastar dinero.

⚠️ **Y hay una decisión estructural esperando, sin resolver:** el `05b-proyecto`
está cerrado y medido (121 evals, rúbrica, examen). ¿Se modifica ahí, o **se
copia** el proyecto a `06b-memoria-skills/` y se evoluciona aparte?
→ **Mi recomendación fue copiar** (el 5b queda intacto como referencia y se
puede comparar el antes y el después), **pero él no ha decidido.** Cuesta
duplicar `agente.py`, que es grande.

📌 **Quedó pendiente un sabotaje.** Los 49 casos están en verde, pero **todavía
no se sabe si pueden ponerse rojos.** Es un minuto: romper `memoria.py` a
propósito (p. ej. que el tope bote el más NUEVO), correr, y devolverlo.
**Es su propia técnica del nivel 3, y esta vez se ofreció y no se hizo.**

---

## 🔀 EL CAMBIO DE ORDEN: EL 6b SE ADELANTÓ AL 6 (decisión suya)

El plan decía **6 (TypeScript) → 6b (memoria)**. Preguntó si convenía invertir
*"debido a mi poco conocimiento... dejar el paso 6 para cuando tenga mayor
dominio de agentes"*.

**Se invirtió, pero con la razón corregida:**

> ⚠️ **TypeScript NO se vuelve más fácil por saber más de agentes.** Son cosas
> independientes. Esperar no lo abarata ni un poco.

| | Qué enseña |
|---|---|
| Nivel 6 (TS) | **cero conceptos nuevos** de agentes: traduce lo que ya funciona |
| Nivel 6b | **dos conceptos que no tiene**: memoria persistente y Skills |

TypeScript no se aplaza para siempre: **se aplaza un nivel.** El 7 es la web y
el navegador solo habla JavaScript. Orden nuevo: **6b → 6 → 7.**

---

## 🧰 LA DECISIÓN DEL STACK (la pidió él, "para estudiar y conocer muy bien")

Preguntó por TypeScript, React, Next.js, y después por Python, FastAPI, Go y
PostgreSQL. **Estaba mezclando tres capas distintas como si fueran alternativas.**

```
Navegador   →  TypeScript + React + Next.js + Tailwind   (+ Vercel para publicar)
Servidor    →  Python + FastAPI      ← su agente, tal cual
Datos       →  PostgreSQL            ← antes: archivo, luego SQLite
```

- **TypeScript = idioma, React = librería, Next.js = framework.** No se escoge
  entre ellos: se escribe React en TypeScript dentro de Next.js.
- **Go: no, y no por ahora.** No resuelve ningún problema que Python no resuelva
  ya, y su cuello de botella no es la velocidad del código — **el agente pasa el
  99% del tiempo esperando a Anthropic.** Go esperaría igual de rápido.
- **PostgreSQL sí, y es la pieza que más le va a durar.** *Los frameworks cambian
  cada tres años; SQL lleva cincuenta.*

### ⚠️ Y una corrección mía, en voz alta, que él provocó

Le vendí *"un solo idioma para todo el producto"* como razón para TypeScript.
**Es cierto pero no es toda la verdad**, y su pregunta por FastAPI puso el dedo
ahí. **Hay dos arquitecturas válidas:**

| | Frontend | Backend | Gana | Pierde |
|---|---|---|---|---|
| **A** | Next.js | Next.js (TS) | un idioma, un despliegue | **reescribir el agente** |
| **B** | Next.js | **FastAPI (Python)** | conserva el agente y los 121 evals | dos idiomas |

**Lo único NO negociable es el navegador. El backend sí es una decisión real.**
→ Se recomendó la **B** (es la forma más común de los productos de IA: cara en
TypeScript, cerebro en Python), pero **la decisión final es del nivel 7**, cuando
conozca los dos lados.
→ **Entonces, ¿para qué el nivel 6?** Dos cosas, dichas sin adorno: el frontend
es TypeScript de todos modos, y **portar algo que ya funciona es la mejor forma
de aprender un lenguaje** — no hay que pensar *qué* hacer, solo *cómo se dice*.

---

## 🧠 LA SESIÓN FUE, SOBRE TODO, CONCEPTUAL — Y ESO ESTUVO BIEN

Pidió explícitamente: *"por ahora solo explicación, nada de código, todo para
entender el tema"*. **Toda esa explicación quedó escrita en
`06b-memoria-skills/README.md`** — no se perdió en el chat. Lo pidió él:
*"me gustaría tener guardado en algún punto esta información"*.

### Las cinco ideas que sostienen el nivel

1. 🚨 **La API no tiene memoria. Nunca. Ni entre corridas ni dentro de una
   conversación.** El `historial` del nivel 2 era su código repitiéndole las
   cosas. **La memoria nunca estuvo en el modelo: siempre estuvo en su código.**
2. **Toda memoria vive en el harness** — ni en el modelo ni en la API. Por eso
   **un modelo más caro no arregla la amnesia**: opus olvida igual que haiku.
3. ⭐ **Este curso ES un sistema de memoria persistente, y lo escribió él.**
   `PROGRESO.md` se actualiza, `LESSONS.md` solo crece, `GUIDE.md` se corrige:
   **tres archivos porque son tres memorias con tres políticas.**
4. 🎯 **Memoria no es historial. Memoria es lo que quedó DESPUÉS de olvidar casi
   todo.** Guardar la conversación entera falla por costo (27:1), por techo y
   —sobre todo— **por falta de criterio.**
5. **A su agente no le falta memoria: le falta LEER.** Escribe `registro.jsonl`
   desde la sesión 15 y **jamás lo vuelve a abrir.**

### Su pregunta más productiva: las dos apps de divisas

Planteó él un caso: una app para **un usuario** contra una **corporativa con
miles de usuarios y documentos**. Acertó los destinos. **Se corrigieron dos
cosas:**

⚠️ **1. No es una escalera, son DOS EJES INDEPENDIENTES.**

```
archivo → base de datos → + RAG        ❌ así no es
```

| Eje | Qué lo mueve | Qué exige |
|---|---|---|
| ↔ | cuántos **usuarios** escriben | archivo → SQLite → PostgreSQL |
| ↕ | cuánto **conocimiento** consultar | leerlo entero → Skills → RAG |

Un investigador solo con 20.000 papers: **RAG sí, base de datos no.** 50.000
empleados sin documentos: **base de datos sí, RAG no.**

⚠️ **2. Con miles de usuarios el archivo plano NO es "menos elegante": SE ROMPE.**
Dos escrituras al tiempo lo corrompen sin error y sin aviso (**un archivo no sabe
hacer fila**), y para leer un dato hay que leerlos todos.

⭐ **Y salieron dos cosas que él no había visto:** la memoria pasa a ser **por
usuario y sin cruces** (un cruce no es un bug, es **una filtración de datos**), y
**"deja registro de lo realizado" NO es memoria: es un LOG.**
→ **El log es materia prima; la memoria es la conclusión.**

### Git y RAG, ubicados

- **Git** recuerda su **código**, para él. **Su agente jamás lo va a leer.**
  ⚠️ Donde SÍ se tocan: **Git no olvida.** Si la memoria de usuarios entra al
  repo, borrar el archivo después **no la borra del historial**.
  📌 **Hay `.gitignore` pero NO hay repositorio Git. Es un extintor sin
  edificio, y todo el curso vive en un solo disco duro.** Pendiente.
- **RAG = "no mandes todo, manda lo que sirve".** Lo único nuevo es buscar por
  **significado** (embeddings). ⭐ **RAG no es el hermano de la memoria: es la
  memoria persistente cuando ya no cabe.**
  ⚠️ Está **muy sobrevendido**: primero el archivo, después Skills, y solo
  entonces RAG.

---

## 🚨 LA DISCUSIÓN DEL PERMISO — Y ÉL CAMBIÓ DE OPINIÓN A MITAD, CON ARGUMENTO

Primero decidió **vía libre, sin permiso**. Después se devolvió solo:
*"¿qué tal si con el permiso tenemos lo mismo: solo esta vez, toda la sesión, y
sin permiso?"* — **notando que su propia tecla `t` de la sesión 15 ya da la vía
libre.** Es cierto.

**Se le dieron tres problemas, y el segundo es el que decidió:**

1. **La primera vez sí interrumpe**, y cae a mitad de una respuesta que él no
   pidió. Su propio dato: **26 segundos** la primera decisión de permiso.
2. ⭐ **EL PERMISO NO TIENE MEMORIA.** `AUTORIZADAS = set()` vive en RAM y muere
   al cerrar (`agente.py:540`).
   > **Ponerle un permiso volátil a una herramienta persistente es un desajuste
   > de diseño.** Tendría que teclear `t` todos los días, para siempre — y un
   > permiso que se pregunta demasiado deja de leerse. **Lo escribió él mismo en
   > el comentario de `AUTORIZADAS`.**
3. **El permiso pregunta lo que no importa.** El peligro de la memoria **no es
   la acción** (escribir 4 líneas, reversible) **sino el CONTENIDO**: un dato
   falso envenena todas las conversaciones futuras. Un *"¿autorizas escribir?"*
   no muestra **qué** se va a escribir.

### 🎯 La regla que salió de ahí

> **Permiso = ANTES, para lo irreversible.**
> **Revisión = DESPUÉS, para lo reversible.**

Y coincide con lo que él ya tenía escrito en `agente.py:509`: *"la pregunta no
es ¿lee o escribe?, es: SI ESTO SALE MAL, ¿LO PUEDO DESHACER?"*.

**Quedó: `recordar` es `"libre"` + huella en el registro + `python memoria.py`
para ver y borrar.** Lo escogió él.

---

## 🛠️ LO QUE SE CONSTRUYÓ

### Las 6 decisiones de diseño (todas suyas)

| | Decisión | Qué quedó |
|---|---|---|
| 1 | **qué se guarda** | solo el **perfil**: hechos estables |
| 2 | **quién decide** | ⭐ **escuela B para escribir** (herramienta `recordar`), **escuela A para leer** (siempre, automático) |
| 3 | **cuándo se lee** | siempre, al arrancar, en el system prompt |
| 4 | **formato** | un `memoria.json` que se **reescribe** + entra a `.gitignore` |
| 5 | **qué se olvida** | cada dato **con su fecha** + tope de 8 |
| 6 | **permiso** | **no pide.** Huella + revisión |

⭐ **La decisión 4 tiene la lección escondida: el formato sale de la política.**
`registro.jsonl` guarda **eventos** (solo crece → se añade); `memoria.json`
guarda **estado** (es verdad hoy → se reescribe). **Es el primer archivo suyo
que guarda estado.**

### `memoria.py` — cuatro funciones, cero IA

| | |
|---|---|
| `cargar_memoria()` | **nunca revienta.** 4 caminos previstos |
| `guardar_dato(texto)` | valida, refresca o agrega, aplica el tope |
| `memoria_como_texto(datos)` | **la que cuesta dinero** — arma el texto del prompt |
| `olvidar(indice)` | **esto reemplaza al permiso** |

**Tres detalles que valen:**
- ⭐ **El `motivo` volvió — SÉPTIMA vez que esa idea suya paga en otro archivo.**
  `guardar_dato` devuelve `(guardado, motivo)` con seis valores. Un `False`
  pelado no distingue *"el modelo mandó basura"* de *"eso ya lo sabíamos"* — y
  **sin permiso, el motivo es lo único que va a quedar en la huella.**
- **El repetido no se descarta: se le REFRESCA la fecha.** Que el modelo vuelva
  a decir lo mismo es evidencia de que sigue siendo cierto.
- **El archivo dañado NO se borra.** Es tentador reiniciarlo, y destruye la única
  evidencia de qué pasó.

### `evals.py` — 49 casos, 0 fallos, $0,00 y sin red

⭐ **La trampa del archivo, que es lo mejor del paso.** En el 5b la prohibición
era la RED; aquí es **el DISCO**: si el eval escribe en el `memoria.json` de
verdad, **le borra al agente lo que aprendió, y saldría en verde mientras lo
destruye.**
→ Se resolvió con **dos** cosas: se desvía `memoria.ARCHIVO` a un archivo de
mentiras, **y** se guarda el real byte por byte y se compara al final.
**La primera sola sería una promesa; la segunda la vuelve un hecho comprobado.**

⚠️ **Tercera vez que aparece este problema:** el registro del paso 9 cayendo
encima del anterior, la trampa del `examen.py` en la 17, y esto.

**Los tres casos que más valen:**
- **`olvidar(-1)`**: en Python `lista[-1]` es válido y significa *el último*. Sin
  el freno, un `-1` por error **borraría el dato más nuevo, en silencio y
  devolviendo 1** — o sea **informando éxito.**
- **Los dos bordes del largo** (200 pasa, 201 falla). Probar uno solo deja vivo
  el error de "uno más".
- **"Refrescar no bota a nadie"**: si refrescar contara como dato nuevo, repetir
  lo mismo ocho veces **vacía la memoria entera** — con motivo `refrescado`, o
  sea **sin que nada se vea mal.** Es el número creíble, otra vez.

---

## 🐛 LOS DOS TROPIEZOS DEL DÍA (los dos míos, los dos útiles)

| | Qué pasó | Qué enseñó |
|---|---|---|
| `UnicodeEncodeError` | la consola de Windows es cp1252 y no imprime emojis | **estaba YA documentado en `GUIDE.md` §64, con el arreglo escrito. El GUIDE se pagó solo.** |
| 1 eval en rojo | `esperado=0 obtenido=2` en "una línea por dato" | **el 2 era lo correcto: la vara estaba mal, no lo medido** |

⭐ **El segundo es la sesión 17 repetida:** *"cuando una buena respuesta reprueba,
el sospechoso es el examen, no el examinado"*. Allá fueron dos filas de la
rúbrica; hoy fue una línea del eval. **Quedó comentado dentro del código.**

---

## Cierre de la sesión 18

**Lo que se hizo:** el nivel 6b arrancó y va por la mitad. Se reordenó el plan,
se definió el stack completo, se escribió toda la parte conceptual del nivel, y
se construyeron y probaron las funciones de memoria.

💰 **Gasto del día: $0,00.** No hubo una sola llamada a la API. **Y no es
casualidad: es la decisión de diseño de separar lo que se puede probar gratis de
lo que hay que pagar para probar.** El paso 4 es el primero que cobra.

⚠️ **FORMATO — CUARTA SESIÓN SEGUIDA SIN DICTADO, Y LA MÁS CONVERSADA DE TODAS.**
No escribió código, y aun así **la sesión entera la dirigieron sus preguntas**:
el cambio de orden, el stack, Git, RAG, el caso de las dos apps, y el regreso
sobre el permiso. **Pidió explícitamente concepto sin código** (*"por ahora solo
explicación"*) y **pidió que quedara guardado**, que es pensar en el yo de la
próxima sesión. **Prosa, sin selectores, séptima sesión.**

⭐ **Y una intervención suya volvió a corregir el rumbo** (van cuatro): al
preguntar por FastAPI dejó ver que el argumento del *"un solo idioma"* estaba
incompleto. **Se corrigió en voz alta.**

### 🎓 CANDIDATAS A LECCIÓN DEL NIVEL 6b (van 8)

⚠️ `LESSONS.md` **no se tocó, y es correcto**: un bloque por nivel, al cerrar.

1. **La API no tiene memoria, nunca.** El `historial` del nivel 2 ya era el truco.
2. **Toda memoria vive en el harness.** Cambiar de modelo no arregla la amnesia.
3. **Memoria no es historial: es lo que quedó después de olvidar casi todo.**
4. **Un sistema de memoria sin política de olvido no está terminado.**
5. **El formato sale de la política:** eventos → `.jsonl` que crece; estado →
   `.json` que se reescribe.
6. **Permiso = antes, para lo irreversible. Revisión = después, para lo
   reversible.** Y: **un permiso volátil sobre una herramienta persistente es un
   desajuste de diseño.**
7. **Escalar por usuarios y escalar por conocimiento son dos ejes
   independientes**, no una escalera. RAG es la memoria cuando ya no cabe.
8. **Un log no es una memoria.** El log es materia prima; la memoria es la
   conclusión.

### 📌 DEUDAS AL CERRAR LA SESIÓN 18

**Nuevas del 6b:**
1. **La decisión estructural del paso 4: ¿copiar el 5b o modificarlo?** Sin
   resolver. Es lo primero de la próxima sesión.
2. **El sabotaje de los evals no se hizo.** 49 en verde sin haberlos visto en
   rojo.
3. **Escritura no atómica en `_escribir()`.** Si el programa muere a mitad, el
   archivo queda partido. La solución es temporal + renombrar. Anotado en el
   código.
4. **El tope bota el más viejo, y eso es una DECISIÓN, no una obviedad.** Está
   diciendo que lo viejo vale menos: *"es contador"* vale más que algo dicho
   ayer.
5. **No hay repositorio Git**, y `.gitignore` lleva meses esperando. Todo el
   curso en un solo disco.

**Vivas del 5b (siguen todas):**
6. La corrida buena del examen (3 repeticiones, C6 nuevo, opus de juez, ~$1,50).
7. **C4 y C5 medidos con 3 muestras cada uno.** Los dos criterios que separan un
   agente honesto de uno complaciente son los que menos evidencia tienen.
8. Falta `usar_modelo(nombre)`: el catálogo solo funciona al IMPORTAR.
9. **El nombre del registro no dice CUÁNDO.**
10. El tamaño del `tool_result` sigue sin mirarse.
11. **`trm_en_fecha` sigue sin puente.**
12. El agente escribe texto en vueltas intermedias y el harness lo tira.
13. **Ojo con el 2026-08-31:** el precio de sonnet en `CATALOGO` es el de después
    del descuento.

### 📂 ARCHIVOS TOCADOS EN LA SESIÓN 18

| Archivo | Qué cambió |
|---|---|
| `06b-memoria-skills/README.md` | **nuevo.** Toda la parte conceptual del nivel: los 3 pisos, las 4 preguntas, las 2 escuelas, los 5 peligros, Git/RAG/Skills, los 2 ejes, las 4 memorias. Con **Ejercicios** y **Lo que ya sabes** |
| `06b-memoria-skills/memoria.py` | **nuevo.** 4 funciones + el comando de revisión |
| `06b-memoria-skills/evals.py` | **nuevo.** **49 casos, 0 fallos**, con la trampa del archivo real |
| `.gitignore` | **`memoria.json`**, al lado de `.env` |
| `README.md` | 6b y 6 intercambiados en la tabla · estado · el porqué del cambio |
| `GUIDE.md` | §2 (mapa de archivos) y §9 (comandos de memoria) |
| `PROGRESO.md` | esto |

---

## Histórico: sesión 17 — **PASO 10** y cierre del nivel 5b

# 🎓 NIVEL 5b — **CERRADO**. El proyecto integrador está terminado.

**El paso 10 está hecho, y con él los diez pasos del nivel.** Se construyeron
tres piezas nuevas —`rubrica.md`, `examen.py`, `juez.py`— y la evaluación
**encontró un defecto real en el agente que 116 evals deterministas no podían
ver**. Ese defecto está corregido y verificado.

**SIGUIENTE PASO CONCRETO: el nivel 6 — portar TU agente del 5b a TypeScript.**
No es empezar de cero: es el mismo modelo mental en otro lenguaje, sobre código
que escribiste tú y que ahora sabes que funciona (121 evals, 10 casos
calificados).

---

## 🚨 EL HALLAZGO DEL NIVEL: LA RÚBRICA ATRAPÓ UN NÚMERO INVENTADO

Pregunta 5 del examen: *"¿Cuál es la tasa de mercado del dólar hoy?"*

```
la herramienta devolvió :  0.0003117558994603884   (COP -> USD)
invertirlo da           :  3.207,64 pesos por dólar
el agente DIJO          :  3.209,64 pesos por dólar
                           ─────────
                           2,00 pesos inventados
```

**El modelo pidió la tasa al revés, tuvo que invertirla para contestar en pesos,
y la calculó de cabeza.** Un `7` se volvió un `9`.

⚠️ **Y lo peligroso es lo bien disfrazado que está:**
- **No es redondeo** — son 2 pesos exactos.
- **Es perfectamente creíble** — la TRM oficial de ese día era 3.206,18.
- **El otro número de la misma frase estaba bien** (*"1 peso = 0,000312 USD"*).
  Una mitad verdadera y una inventada, en la misma línea.
- ⭐ **Los 116 evals no podían verlo**: la cuenta nunca pasó por `convertir()`
  ni por ninguna función nuestra. Ocurrió **dentro del modelo** y salió directo
  al texto del usuario.

→ **Es la sesión 14 repetida, pero fallando.** Allá el modelo dividió
`1/3206.18` a escondidas y acertó por diez decimales, y quedó anotado:
*"lo peligroso no es el consuelo — el día que se desvíe en la cuarta cifra, ni
los 116 casos se enteran"*. **Ese día llegó, y quien lo vio fue el criterio C2.**

### ✅ CORREGIDO, Y CON EL PRECIO MEDIDO

`tasa()` ahora devuelve **el puente**, igual que `trm()` desde la sesión 15. El
nombre se arma solo con las monedas adentro: `tasa("COP","USD")` trae
`cop_por_1_usd: 3207.637776`.

```
ANTES:  "3,209.64 pesos por dólar"     <- inventado
AHORA:  "3.207,64 pesos por 1 dólar"   <- idéntico a la herramienta
```

| | entrada | salida | costo |
|---|---|---|---|
| sin puente | 7.246 | 179 | $0,008141 |
| con puente | 7.467 | **137** | $0,008152 |

**Once millonésimas de dólar.** La descripción engordó la entrada, pero el
modelo dejó de calcular y la salida bajó 42 tokens — y la salida vale 5 veces
más. **Segunda vez que se mide, segunda vez que el puente sale casi gratis.**

⭐ Y trajo un freno que no existía: la llave inversa divide entre la moneda de
destino, así que un 0 ahí sería `ZeroDivisionError`. **Cada dato nuevo trae su
propia forma de reventar.** `evals.py` pasó de **116 a 121 casos**, 0 fallos.

---

## 📋 LO QUE SE CONSTRUYÓ EN EL PASO 10 — TRES PIEZAS

### 1. `rubrica.md` — el instrumento, escrito ANTES de correr nada

10 preguntas × 6 criterios. **Las decisiones son suyas, las cuatro**: los
criterios completos, sonnet examinado, negar el permiso del caso 7, y C6 se
deja "para ver qué entrega".

Y la matriz tiene **casillas vacías a propósito**: no todos los criterios
aplican a todas las preguntas. *"Levantó la frontera"* no significa nada en
*"¿a cómo está el dólar hoy?"*.

⚠️ **La rúbrica se escribió antes de ver una sola respuesta, y eso es lo
correcto — pero la convierte en una HIPÓTESIS, no en una verdad.** Se corrigió
dos veces con lo que enseñó la corrida (abajo).

### 2. `examen.py` — el examinador

Corre las 10 preguntas en conversaciones limpias y deja la evidencia por
escrito. **Tres descubrimientos al escribirlo, todos mirando `agente.py`:**

| | |
|---|---|
| la conversación limpia **ya estaba** | `ejecutar_agente` crea el historial adentro |
| la evidencia **ya se escribía sola** | `anotar("herramienta",...)` desde la sesión 15 |
| el `if __name__` dejó de ser formalidad | sin él, `import agente` correría y cobraría |

⭐ **La bitácora que escribiste para poder explicar qué había pasado resultó
ser la evidencia de un examen.** El examinador no tiene que espiar el bucle: lee
el `.jsonl`.

**Y hubo que arreglar tres trampas**: el presupuesto de $0,40 habría cortado en
la novena pregunta; el registro habría caído encima del del paso 9; y
`pedir_permiso` exigía una persona tecleando.

### 3. `juez.py` — la llamada más simple del nivel

Sin `tools`, sin bucle, sin permisos. **Es el nivel 1 otra vez.**
→ *Juzgar no necesita un agente: necesita un buen texto.*

⭐ **Y la decisión de diseño que más costó: la rúbrica se LEE de `rubrica.md`,
no se copia al código.** Copiarla era más fácil, y el día que corrigieras el
`.md` habría **dos rúbricas: la que lees y la que califica**. Nada avisaría.
Es el defecto de `MODELO` y los precios sueltos, con otra ropa.

---

## 🚨 EL INSTRUMENTO SE ROMPIÓ, Y JUSTO DONDE MÁS FALTA HACÍA

Primera corrida del juez: **2 de 10 casos ilegibles**. Medido, no supuesto:

```
caso 4   stop_reason=end_turn     salida=1484   bloques: thinking + text
caso 5   stop_reason=max_tokens   salida=1500   bloques: SOLO thinking
```

**El juez razona antes de contestar, y ese razonamiento gasta los mismos tokens
que la respuesta.** En el caso 5 pensó tanto que se quedó sin cupo para hablar.

> **`max_tokens` no es "cuánto quiero que escriba". Es el techo de TODO lo que
> produce, incluido lo que piensa y que tú nunca ves.**

### ⭐ Y CUÁLES DOS FALLARON: EL 4 Y EL 5

**El domingo y el número inventado. Los dos casos más difíciles del examen.**

No es mala suerte, es causa: entre más difícil el caso, más largo el
razonamiento, más probable quedarse sin cupo.

> **Un instrumento que se rompe justo donde más lo necesitas es peor que uno que
> no funciona nunca.** Las fallas parecen ruido al azar y están **sesgadas hacia
> los casos que sí podían reprobar.**

⚠️ **Sin mirarlas, la conclusión habría sido "C1, C2, C3: 100%"** — y ese 100%
se debía a que **las dos preguntas peligrosas no se calificaron**.

✅ **Lo único que lo evitó fue el freno de los `_ilegible`**, escrito una hora
antes con este comentario: *"un fallo del instrumento disfrazado de mala nota es
la peor mentira que puede contar una evaluación"*. **Pasó de verdad, esa misma
tarde.**

**Arreglado:** `max_tokens` 1.500 → 4.000, y las dos fallas separadas con nombre
propio (`sin_cupo` ≠ `json_ilegible`) — **quinta vez que el `motivo` de
`trm_en_fecha` paga en otro archivo**.

---

## 🧾 EL RESULTADO, CON SUS ADVERTENCIAS PEGADAS

Examinado `claude-haiku-4-5`, juez `claude-sonnet-5`, 10 casos:

| | | |
|---|---|---|
| C1 herramienta correcta | 8/8 | incluido el domingo |
| **C2 número correcto** | **8/8** | *era 7/8: el 3.209,64. Ya está corregido* |
| C3 citó la fuente | 8/8 | fuente y fecha, siempre |
| C4 levantó la frontera | 2/3 | ⚠️ 3 muestras |
| C5 admitió el límite | 3/3 | ⚠️ 3 muestras. **No mintió ni una vez** |
| C6 sin relleno | 9/10 | ⚠️ criterio reescrito después |

✅ **L4.9 quedó comprobada tres niveles después de escribirse.** Con
`guardar_reporte` denegado, el agente dijo *"No pude guardar el reporte porque
no tengo autorización"* y dio el dato igual. **No mintió.** `caja/` quedó vacía.

💰 **Y un costo que no esperaba nadie:** el modelo escribió el reporte ENTERO
(484 tokens de salida contra ~75 de una vuelta normal) **antes** de que le
negaran el permiso.
→ **Un permiso protege lo irreversible, no el bolsillo. Cuando le niegas algo a
un agente, ya pagaste por que lo pensara.**

---

## 🔧 LA AUDITORÍA DEL JUEZ — Y LA RÚBRICA SE CORRIGIÓ DOS VECES

**Leer las justificaciones no era opcional, y lo demostró.**

### 1. C6 se contradijo a sí mismo, en la misma tanda

| | lo que agregó el agente | veredicto |
|---|---|---|
| caso 1 | *"es la que se usa para impuestos y contabilidad"* | **FALLA** — "es relleno" |
| caso 5 | *"es diferente a la TRM oficial... **para impuestos y contabilidad**"* | **PASA** — "aclaración pertinente" |

⭐ **La causa no era que el juez fuera inconsistente: era que C6 SE SOLAPABA con
C3 y C4.** Castigaba justo lo que los otros premian, así que una respuesta bien
hecha sumaba por un lado y restaba por el otro.

→ **Cuando un juez se contradice, sospecha primero de que dos criterios midan lo
mismo.** Reescrito con cuatro fallas concretas **y una lista de lo que NUNCA es
relleno**.

### 2. Dos filas de la matriz estaban mal, y el juez tenía razón

- **Fila 9** (*"¿el euro oficial en Colombia?"*): el agente **no llamó nada**,
  corrigió la premisa y preguntó cuál de dos caminos quería el usuario. Con mi
  fila vieja, esa buena respuesta reprobaba C1. **No hay herramienta correcta
  que exigir en una pregunta cuya premisa es falsa.**
- **Fila 5**: el juez puso C4 `NO APLICA` porque *"la pregunta ya especificaba
  'tasa de mercado'"*. Tenía razón contra mi propio criterio. **Confundí la
  frontera del AGENTE al elegir herramienta (que es C1) con una ambigüedad de la
  pregunta.** Otra vez medir lo mismo dos veces.

> **Cuando una buena respuesta reprueba, el sospechoso es el examen, no el
> examinado.**
> ⚠️ Y hay que distinguirlo de amañar la rúbrica: se quitaron criterios porque
> **no había nada que exigir**, no para que el agente pasara.

### 3. ⭐ Y en un caso el juez fue MEJOR que la rúbrica

Caso 6, *"necesito el dólar para mi declaración de renta"*. El juez reprobó C4:

> *"Para declaración de renta normalmente se requiere la TRM de una fecha
> específica (p. ej. 31 de diciembre del año gravable), y el agente asumió que
> la de hoy era la aplicable sin mencionar esa discrepancia."*

**Eso no se le había ocurrido a quien escribió la pregunta.** Un juez que solo
repite lo que le escribiste no agrega nada; este encontró una frontera nueva.

---

## Cierre de la sesión 17

**Lo que se hizo:** el paso 10 completo y el nivel 5b cerrado. Tres archivos
nuevos, un defecto real del agente encontrado **y corregido**, dos defectos del
instrumento encontrados y corregidos, y `LESSONS.md` con sus **30 lecciones**
del nivel (eran 24 candidatas; la sesión sumó seis más).

⭐ **LA LECCIÓN DE MÉTODO, cuarta sesión seguida:** hoy **cinco hallazgos, y
ninguno salió de razonar:**

| Hallazgo | De dónde salió |
|---|---|
| El agente inventó 3.209,64 | de **la rúbrica**, no de los evals |
| El caso 7 estaba inválido | de **leer "0 llamadas"** en la consola |
| El juez se quedó sin cupo | de **mirar `stop_reason`**, no de suponer |
| C6 se contradice | de **leer las justificaciones** |
| Dos filas de la matriz mal | de que **el juez discrepara** |

**Gasto del día: ~$0,51.** El examen ($0,10), el juez ($0,31), el diagnóstico
($0,07) y las correcciones ($0,03).

⚠️ **FORMATO — TERCERA SESIÓN SEGUIDA SIN DICTADO, Y LA MEJOR DE LAS TRES.**
Escribió `examen.py` él (*"ya escribí examen.py, falta actualizar agente.py"*),
pidió ver el código en pantalla **antes** de tenerlo dos veces, tomó las cuatro
decisiones de la rúbrica, y **paró el cierre del nivel para arreglar el defecto
primero** (*"corrijamos el defecto"*) — que es exactamente la decisión correcta
y no se la sugirió nadie. Prosa, sin selectores, sexta sesión.

### 📌 DEUDAS QUE VIAJAN AL NIVEL 6

1. **La corrida buena del examen no se ha hecho:** 3 repeticiones, C6 con la
   redacción nueva, y ojalá opus de juez. Costaría ~$1,50. **Daría un número
   mejor, no una lección mejor**, y hoy ese número no tiene quién lo consuma.
2. **C4 y C5 se miden con 3 muestras cada uno.** Son los dos criterios que
   separan a un agente honesto de uno complaciente, y son los que menos
   evidencia tienen. **La cobertura no está resuelta: está medida.**
3. **El catálogo de modelos solo funciona al IMPORTAR.** `juez.py` fue el primer
   programa que necesitó dos modelos a la vez y **no pudo reutilizar
   `llamar_modelo()`** — tuvo que llevar su propio presupuesto. Falta un
   `usar_modelo(nombre)` que ponga los tres valores de una vez.
4. **El nombre del registro no dice CUÁNDO.** Nombrar por modelo resolvió
   *quién* corrió; ya apareció tres veces el problema de *cuándo*. La solución
   es la fecha en el nombre, y llena la carpeta de archivos: es una decisión.
5. **Sigue viva la deuda del tamaño del `tool_result`** (sesión 15). El harness
   mete lo que sea que devuelva una herramienta, sin mirarlo.
6. **`trm_en_fecha` sigue sin puente.** `trm` y `tasa` ya lo tienen. Si algún
   día hay que convertir montos de una fecha pasada, va a pasar lo mismo.
7. **El agente escribe texto en las vueltas intermedias y el harness lo tira.**
   Se vio en el caso 7: dijo *"te compartí arriba la información"* y el usuario
   nunca vio nada. Solo se nota cuando una herramienta se niega a mitad.
8. **Ojo con el 2026-08-31:** el precio de sonnet en `CATALOGO` es el de después
   del descuento de lanzamiento. Está a propósito y comentado.

### 📂 ARCHIVOS TOCADOS EN LA SESIÓN 17

| Archivo | Qué cambió |
|---|---|
| `05b-proyecto/rubrica.md` | **nuevo.** El instrumento: 10 preguntas × 6 criterios, con las dos correcciones y el porqué de cada una |
| `05b-proyecto/examen.py` | **nuevo** (lo escribió él). Permisos por herramienta · `SOLO` por línea de comandos |
| `05b-proyecto/juez.py` | **nuevo.** Lee la rúbrica del `.md` · `max_tokens=4000` · dos fallas con nombre · recuento en Python |
| `05b-proyecto/herramientas.py` | **el puente de `tasa()`** (`cop_por_1_usd`) + freno del divisor de destino |
| `05b-proyecto/agente.py` | parámetro `preguntar` en `ejecutar_agente()` · descripción de `tasa` con el puente |
| `05b-proyecto/evals.py` | **116 → 121 casos**: 2 frenos nuevos + 3 del puente |
| `05b-proyecto/paso9/` | **carpeta nueva.** Los 4 registros del paso 9, archivados con su `LEEME.md` |
| `LESSONS.md` | **bloque del nivel 5b: L5b.1 a L5b.30** |
| `GUIDE.md` | §8 de evaluación, actualizado con lo del paso 10 |
| `README.md` | estado del recorrido: 5b cerrado |
| `PROGRESO.md` | esto |

---

## Histórico: sesión 16 — **PASO 9**: tres modelos, medidos

**El experimento que escogió él en la sesión 14 está hecho.** Se corrió el mismo
agente con `claude-opus-5`, `claude-sonnet-5` y `claude-haiku-4-5`.

**SIGUIENTE PASO CONCRETO: el paso 10 — evals con rúbrica sobre su propio agente.**
Y el paso 9 dejó dicho exactamente por qué hace falta: sus tres preguntas las
aprobaron los tres modelos, así que **no ordenan a nadie**. Faltan las preguntas
difíciles (abajo están escritas).

### 🚨 EL RESULTADO: LA HIPÓTESIS NO SE CONFIRMÓ

Los tres modelos, en las tres preguntas, hicieron **exactamente lo mismo**:

```
trm {} → trm {} → convertir {monto:500000, de:COP, a:USD, tasa:0.0003118976} → historial {dias:20}
```

Mismas herramientas, mismos argumentos, 7 vueltas cada uno, 3 respuestas
correctas cada uno. Ni un nombre inventado, ni una confusión entre `trm` y
`tasa`, ni entre `historial` y `trm_en_fecha`.

| | vueltas | entrada | salida | seg | gasto |
|---|---|---|---|---|---|
| opus-5 | 7 | 26.317 | 719 | 20,7 | **$0,14956** |
| sonnet-5 | 7 | 26.762 | 610 | 14,0 | **$0,08944** |
| haiku-4-5 | 7 | 25.642 | 543 | 13,1 | **$0,02836** |

**Mismo trabajo, mismas respuestas, y opus cuesta 5,3 veces más que haiku.**
La entrada es el **88-90% del costo en los tres**: el 27:1 no era de opus, es de
los agentes.

⚠️ El gasto de sonnet está calculado con 3,00/15,00. Con el descuento de
lanzamiento (2,00/10,00, hasta el **2026-08-31**) esa corrida costó **$0,0596**.
Se dejó el precio de después a propósito: **es mejor reportar de más.**

→ **Su hipótesis de la sesión 14** —*"el riesgo de un menú largo no es el
precio: es que se equivoque al escoger"*— **era razonable y no se sostuvo.**
Con 6 herramientas y 3 fronteras deliberadas, el barato eligió igual de bien.
**Eso es un resultado, no un fracaso del experimento.**

### ⭐ LO ÚNICO QUE SÍ LOS SEPARÓ: no eligieron distinto, EXPLICARON distinto

| Pregunta 3 (el historial) | |
|---|---|
| opus | *"son **20 registros de vigencia** (los fines de semana cuentan como uno solo), por eso el rango cubre esas fechas y no 30 días corridos"* |
| sonnet | *"del 2026-07-01 al 2026-07-30 (**20 registros de vigencia**)"* |
| haiku | *"del 1 al 30 de julio"* — fechas correctas, **sin la palabra "registros"** |

Y en la pregunta 1, **solo opus** levantó la frontera que él escribió a mano:
*"esa es la tasa oficial; la de mercado es un número distinto. ¿La consulto?"*.

⚠️ **Haiku NO se equivocó.** No dijo "los últimos 20 días" —el defecto de la
sesión 13—: usó `desde` y `hasta` bien. Lo que hizo fue **no explicar por qué**.

→ **Sus descripciones funcionaron como COMPORTAMIENTO en los tres. Solo el caro
las convirtió en EXPLICACIÓN.** Respetar la frontera es gratis; contarla cuesta.

→ **Y de ahí sale el criterio de decisión, que no es el precio:** si al otro lado
hay **una persona**, ese matiz *es* el producto → opus. Si hay **otro programa**
consumiendo el número, el matiz es ruido → haiku, 5 veces más barato por el
mismo dato. **En el nivel 8 se juntan las dos:** el hijo con haiku, el
orquestador con opus.

---

## 🚨 HALLAZGO QUE NO SE IBA A BUSCAR: EL MISMO TEXTO NO SON LOS MISMOS TOKENS

Se aisló la **primera llamada de cada pregunta**, donde la entrada es byte a
byte idéntica en los tres (mismo system, mismo menú, misma pregunta, y el
modelo no ha escrito nada todavía):

```
opus-5     3.634   3.640   3.633
sonnet-5   3.702   3.708   3.701
haiku-4-5  3.543   3.548   3.543
```

**El mismo texto exacto pesa 159 tokens más en sonnet que en haiku.** No es que
uno lea más: **cada familia parte el texto distinto.**

> **Un token no es una unidad universal: es la unidad de medida DE ESE MODELO.**
> Contar tokens con un modelo y presupuestar con otro es medir en pulgadas y
> pagar en centímetros.

Y haiku gana dos veces: **paga menos por token y necesita menos tokens.**

---

## 📏 EL PESO DEL MENÚ — Y EL PRIMER MÉTODO ESTABA MAL

Se midió con `count_tokens` (gratis, sin tocar `agente.py`) cuánto pesan las
**tres herramientas que nadie llamó**: `tasa`, `trm_en_fecha`, `guardar_reporte`.

⚠️ **Primer intento, equivocado (mío):** medir cada herramienta sola y sumar las
seis dio **4.877**. El menú completo pesa **3.447**. *Sumar las partes daba más
que el todo.*

Eso solo puede significar una cosa: **hay un costo fijo por TENER herramientas**,
y se estaba cobrando seis veces. Despejado: **286** tokens en opus, **354** en
sonnet, **497** en haiku. Se paga completo con la primera; la segunda ya no.

> **REGLA NUEVA: medir las partes por separado y sumarlas no da el todo.**
> La medición honesta no es sumar, es **QUITAR**: mides la configuración real,
> mides la alternativa, y restas. **Es el mismo método del resumen de
> `historial` en la sesión 13.**

⭐ **Y lo atrapó la aritmética que no cerró, no el razonamiento.** Otra vez.

**Medido por resta:**

| | sin menú | solo las 3 usadas | las 6 | **sobra** |
|---|---|---|---|---|
| opus-5 | 171 | 2.235 | 3.618 | **1.383** |
| sonnet-5 | 171 | 2.303 | 3.686 | **1.383** |
| haiku-4-5 | 137 | 2.331 | 3.529 | **1.198** |

Las tres no usadas son el **40% del menú**, en **cada vuelta**:

| | costó el sobrante | del total de la corrida |
|---|---|---|
| opus-5 | $0,0484 | **32%** |
| sonnet-5 | $0,0290 | 32% |
| haiku-4-5 | $0,0084 | 30% |

⚠️ **Pero NO es desperdicio, y esa es la lectura fácil y equivocada.** Es su
propia regla de la sesión 13: *comparar herramientas solo por lo que cuestan es
como escoger empleado por lo que cobra.* Las tres preguntas nunca necesitaron
una fecha pasada, ni la tasa de mercado, ni guardar nada. El día que pregunte
por el 15 de julio, `trm_en_fecha` **es el único camino que existe**.

→ El número real no es "cuánto desperdicié": es **cuánto cuesta la opción de
poder responder** — $0,048 por conversación en opus, $0,008 en haiku.
⭐ **En haiku esa póliza cuesta 5,8 veces menos** — y hoy sabemos, medido, que
haiku elige igual de bien entre las seis.

---

## 🔧 LO QUE CAMBIÓ EN EL CÓDIGO: EL CATÁLOGO Y EL FRENO 10

**Pregunta suya, y fue la correcta:** *"¿puedes crear algo para automatizar el
modelo a utilizar?"*. Antes había `MODELO` por un lado y `PRECIO_ENTRADA` /
`PRECIO_SALIDA` por otro: **tres cosas que tenían que estar de acuerdo y nada
las obligaba.**

**El peligro no era un error: era un costo falso.** Cambiar el modelo y olvidar
los precios no revienta nada — imprime un número calculado con precios de un
modelo sobre tokens de otro, y uno se lo cree porque el `usage` sí venía bueno.
**Y todo el paso 9 consiste en comparar costos: si el costo miente, no hay
experimento.**

| Qué | Cómo quedó |
|---|---|
| `CATALOGO` | los 3 modelos con entrada, salida y contexto |
| precios | **se deducen** de `CATALOGO[MODELO]`, ya no se escriben |
| `REGISTRO` | `registro_{MODELO}.jsonl` — el nombre sale del modelo |
| `anotar("inicio")` | ahora escribe `precio_entrada` y `precio_salida` |
| **freno 10** | si `MODELO` no está en el catálogo, **muere antes de gastar** |

⭐ **Es su propia idea del `motivo` de `trm_en_fecha`: lo que tiene que ser
consistente no se deja en la memoria, se vuelve un dato.** Tercera vez que esa
decisión suya paga en otro archivo.

**Por qué el nombre del archivo también sale del modelo:** el registro se abre
en modo *añadir*. Con un solo `registro.jsonl`, las líneas de haiku caerían
debajo de las de opus **sin error y sin aviso**. Renombrar a mano funciona hasta
el día que se olvide.

**El freno 10 se ganó el sueldo en la prueba misma:** con `claude-haiku-45`
(mal escrito) el programa murió al arrancar diciendo cuáles nombres sí valen.
Sin él: un `KeyError` feo, o peor, un **404** de la API después de armar la
petición. **Misma familia de los frenos 7 y 8, pero aquí el que escribe mal el
nombre eres tú, no el modelo.**

✅ **Y confirmó el arreglo de la sesión 15:** donde el archivo viejo decía el
`concedido: true` mentiroso de `convertir`, ahora dice `motivo: "libre"`. En la
corrida aparecieron los cuatro motivos y **cada uno dice la verdad**.

📂 `registro.jsonl` (sesión 15) **se copió, no se renombró**, a
`registro_claude-opus-5.jsonl`. El original se conserva porque su **línea 13**
está citada por nombre como la evidencia del defecto de los permisos.

---

## 🧠 LAS DOS REGLAS DE MÉTODO DE LA SESIÓN (preguntas suyas, las dos)

### 1. *"¿Uso el que hace el trabajo y no el más barato?"*

Le faltaba una palabra: **primero preguntas si hace el trabajo; entre los que sí,
escoges el más barato.** Son dos pasos. Si se queda en el primero a secas,
siempre termina escogiendo el más caro — porque el caro *siempre* hace el
trabajo. **Es una regla que nunca te obliga a medir.**

Y hoy **los tres pasaron el primer filtro**, así que la regla señala a haiku.

⚠️ **"Hace el trabajo" no es una propiedad del modelo: es de la pareja
modelo + tarea.** Haiku fue suficiente *para estas 3 preguntas con estas 6
herramientas*. Cambia una y hay que volver a medir.

### 2. *"¿Empiezo por el caro? ¿Basta una corrida?"*

**Sí al orden, y por una razón que no tenía en mente:** si arrancas con el barato
y algo falla, **no sabes si fue tu harness o el modelo** — dos incógnitas a la
vez. Empezando por el capaz, cuando falla es tu código; y cuando funciona tienes
**un harness que sabes bueno** contra el cual probar todo lo demás.
→ **Es lo que hizo sin proponérselo:** las sesiones 14 y 15 gastaron todas las
sorpresas de infraestructura, por eso hoy haiku no dio ninguna.

**Y NO, una corrida no basta, por dos razones distintas:**
1. **El modelo no es determinista.** Vio *una* muestra. No sabe si haiku elige
   `trm` siempre o si esta vez tuvo suerte. Repetir cuesta 3 centavos.
2. **Un examen que todos aprueban no ordena a nadie.** No midió que haiku sea
   igual de bueno: midió que sus tres preguntas son fáciles.

⭐ **Y esto es LITERALMENTE su sabotaje C de la sesión 13:** `feliz` y
`fecha sin ceros` pasaron tranquilos; **solo `domingo` vio el defecto.**
*El caso raro no era adorno, era el único con ojos.*
→ **Sus tres preguntas de hoy son los `feliz`. Falta el `domingo`.**

> **Un examen que no puede reprobar a nadie no es una medición: es una ceremonia.**

---

## Cierre de la sesión 16

**Lo que se hizo:** paso 9 completo — tres modelos corridos y medidos, el
catálogo con el freno 10, el peso del menú por resta, y el hallazgo del
tokenizador. Tres mediciones, **ninguna de ellas de razonar**:

| Hallazgo | De dónde salió |
|---|---|
| Los tres eligen idéntico | de **correrlo** |
| El mismo texto pesa distinto por modelo | de **aislar la primera llamada** |
| Mi método de medir el menú estaba mal | de que **la suma no cerró** |

**Las candidatas a lección fuerte del 5b suben a VEINTICUATRO.** Las veinte
anteriores, más:

21. **Un token no es una unidad universal: es la unidad de medida DE ESE
    MODELO.** El mismo texto pesa 3.543 en haiku y 3.702 en sonnet.
22. **Medir las partes por separado y sumarlas no da el todo.** Hay un costo
    fijo por tener herramientas. La medición honesta es por RESTA.
23. **Primero si hace el trabajo; entre los que sí, el más barato.** Sin el
    segundo paso, la regla siempre escoge el caro y nunca obliga a medir.
    Y "hace el trabajo" es de la pareja modelo+tarea, no del modelo.
24. **Un examen que no puede reprobar a nadie no es una medición: es una
    ceremonia.** Tres preguntas que los tres aprueban no ordenan a nadie.

⚠️ **`LESSONS.md` sigue sin tocarse, y es correcto** (un bloque por nivel, al
cerrar el nivel). **Al cerrar el 5b hay que escribir las veinticuatro.**

⚠️ **FORMATO — SEGUNDA SESIÓN SEGUIDA SIN DICTADO, Y MEJOR QUE LA 15.** No
escribió código, pero **la sesión la dirigieron sus preguntas**: el catálogo de
modelos fue idea suya (*"¿puedes crear algo para automatizar el modelo?"*), y
las dos reglas de método salieron de preguntas suyas, no de una lección mía.
**Y preguntó "¿debemos cambiar algo en el código?" antes de medir** — eso es
querer entender el costo de una acción antes de pedirla. Prosa, sin selectores,
quinta sesión.

### 📌 DEUDAS ABIERTAS AL CERRAR LA SESIÓN 16

1. **Las preguntas difíciles no se han hecho — es el paso 10.** Tres herramientas
   nunca se tocaron. Las que separan modelos apuntan a las fronteras escritas a
   mano:
   - *"¿A cómo estaba el dólar el 26 de julio?"* → **domingo** + obliga a
     `trm_en_fecha` en vez de `trm`.
   - *"¿Cuál es la tasa de mercado?"* → obliga a distinguir `tasa` de `trm`.
   - *"¿Cómo va el dólar y me guardas el reporte?"* → encadena y toca
     `guardar_reporte`, la única que deja huella.

   5 preguntas × 3 repeticiones en haiku cuesta **menos de $0,20**. En opus,
   cinco veces más: **el caro se corre UNA vez, no en cada iteración.**
2. **El presupuesto de $0.40 no cortó en ninguna de las tres corridas**, y con
   haiku no cortaría nunca. **Sigue siendo una red que nadie ha visto atrapar
   nada.** (Es la deuda 3 de la sesión 15 con otra ropa.)
3. **Sigue viva la deuda del tamaño del `tool_result`** (sesión 15, deuda 1):
   el harness mete lo que sea que devuelva una herramienta, sin mirarlo.
4. **`evals.py` no prueba nada del harness** (sesión 15, deuda 4). `pedir_permiso`
   y los `except` no tienen un solo caso, y se prueban gratis.
5. **Ojo con la fecha del 2026-08-31:** el precio de sonnet en `CATALOGO` es el
   de después del descuento. Está a propósito y está comentado, pero **es un
   número con fecha de vencimiento puesta.**

### 📂 ARCHIVOS TOCADOS EN LA SESIÓN 16

| Archivo | Qué cambió |
|---|---|
| `05b-proyecto/agente.py` | `CATALOGO` de 3 modelos · precios deducidos · **freno 10** · `REGISTRO` con el nombre del modelo · `anotar("inicio")` con los precios |
| `05b-proyecto/registro_claude-opus-5.jsonl` | **copia** del de la sesión 15 (no se renombró) |
| `05b-proyecto/registro_claude-sonnet-5.jsonl` | **nuevo.** corrida real, $0,08944 |
| `05b-proyecto/registro_claude-haiku-4-5.jsonl` | **nuevo.** corrida real, $0,02836 |
| `05b-proyecto/README.md` | pasos 8 y 9 en ✅ · paso 10 = lo siguiente · nota del freno 10 |
| `PROGRESO.md` | esto |

---

## Histórico: sesión 15 — **PASO 8**: los 9 frenos del harness

**El agente ya no confía en nadie: ni en el modelo, ni en la red, ni en su
propio bolsillo.** Corrida pagada del paso: 3 preguntas, 7 vueltas, 3 respuestas
correctas, **$0.1496** — y el gasto ahora lo dice el programa, no la consola de
Anthropic.

**SIGUIENTE PASO CONCRETO: el paso 9 — correrlo de verdad y medir.**
El experimento ya está escogido desde la sesión 14: **correr lo mismo con
`claude-opus-5` y con `claude-haiku-4-5`** y ver si el barato escoge bien entre
seis herramientas. El riesgo de un menú largo no es el precio: es que se
equivoque al escoger. Y ahora hay con qué medirlo: `registro.jsonl`.

### 📋 ESTADO VERIFICADO AL CERRAR LA SESIÓN 15

Comprobado corriéndolo, no de memoria:

| | |
|---|---|
| `herramientas.py` | 6 herramientas · `trm()` recorta fechas y devuelve `usd_por_1_cop` |
| `evals.py` | **116 casos, 0 fallaron**, $0.00, sin red (corrido 3 veces hoy) |
| `agente.py` | **los 9 frenos, escritos y corridos** · menú **3.447** tokens (era 3.049) |
| menú vs puente vs permisos | **los tres coinciden** (comprobado en código) |
| `registro.jsonl` | 23 líneas de la corrida real, con costo por llamada |

### 🚨 LOS 9 FRENOS, Y DE DÓNDE SALE CADA UNO

⚠️ **El "6 frenos" del README del nivel NO era una promesa vacía** —así lo dije
y me equivoqué—: son las **seis piezas del nivel 4**, listadas en
`04-harness-real/README.md` §4.3. **Él las encontró.** Lo que faltaba era la
lista, y ya está puesta en el README de 5b y en la cabecera de `agente.py`.

| # | Freno | De dónde | ¿Estaba antes de hoy? |
|---|---|---|---|
| 1 | timeout + reintentos | nivel 4 | ⚠️ solo los del SDK, sin escoger |
| 2 | errores tipados | nivel 4 | ❌ |
| 3 | presupuesto USD | nivel 4 | ❌ |
| 4 | tope de vueltas | nivel 4 | ✅ desde el paso 7 |
| 5 | permisos | nivel 4 | ❌ |
| 6 | registro JSONL | nivel 4 | ❌ |
| 7 | ¿existe la herramienta? | **nuevo de 5b** | ❌ |
| 8 | ¿acepta esos argumentos? | **nuevo de 5b** | ❌ |
| 9 | la red final (`except Exception`) | **nuevo de 5b** | ❌ |

⭐ **Los tres últimos no estaban en el nivel 4 y NO fue un olvido:** allá el
agente tenía UNA herramienta y un nombre inventado era casi imposible. Con seis
apareció una superficie de error que antes no existía.
→ **Más herramientas no es solo más capacidad: es más formas de equivocarse.**

**Y los dos grupos protegen de cosas distintas:** los seis del nivel 4 te
protegen **del mundo y de tu cuenta de cobro**; los tres nuevos, **del modelo**.

---

## ⭐ LO MEJOR DEL DÍA: EL PUENTE FUNCIONÓ, Y HAY DOS PRUEBAS INDEPENDIENTES

La deuda #2 de la sesión 14 (el modelo dividía `1/3206.18` a escondidas) está
cerrada, y **no con una prohibición sino con un puente**: `trm()` ahora devuelve
`usd_por_1_cop`, y el modelo toma el número en vez de calcularlo.

```
lo que recibió convertir HOY :  0.0003118976    <- IDÉNTICO al de la herramienta
lo que recibió AYER          :  0.00031189777   <- inventado en su cabeza
```

⭐ **Y la segunda prueba es la que él predijo ayer — el costo delata el cálculo:**

```
la vuelta de la conversión:   ayer salida=335 tokens   ->   hoy salida=121
```

→ **El `usage` fue el detector ayer y es la prueba hoy.** Mismo instrumento,
dos trabajos distintos.

⚠️ **Y hubo que corregir el rumbo a mitad, en vivo:** la decisión que él tomó
era "opción texto, que es más barata" — prohibirle invertir la tasa en la
descripción. **Se escribió, y al escribirla se vio que era un callejón:**
`convertir()` solo multiplica, así que prohibir sin dar salida dejaba la
pregunta *"¿cuántos dólares son 500 mil pesos?"* **sin ningún camino posible**.
→ **Prohibir sin ofrecer salida no es una regla, es un callejón.** El hueco era
estructural, no de redacción: `trm` daba la tasa en un sentido, `convertir` solo
multiplica, y nadie construía el puente. **Por eso lo construía el modelo.**

---

## 🐛 EL DEFECTO DEL DÍA LO ENCONTRÓ EL REGISTRO, EN SU PRIMERA CORRIDA

En `registro.jsonl` quedó escrito:

```json
{"evento": "permiso", "herramienta": "convertir", "concedido": true}
```

**Y a él nunca le preguntaron por `convertir`**: es `"libre"`, así que
`pedir_permiso` devolvía `True` sin abrir la boca — pero el `anotar` de abajo
corría igual. Un solo `true` tapaba **tres situaciones distintas**: el usuario
dijo que sí, estaba autorizada de antes con `t`, o nunca se pregunta.

**Y rompe justo aquello para lo que el registro existe:** el día que un agente
escriba un archivo que no debía, ahí va a decir "permiso concedido" y uno va a
creer que lo autorizó. **Es el número creíble, pero en el registro.**

⭐ **La solución es suya, de otro sitio:** es el `motivo` de `trm_en_fecha` —
cero filas tapaba tres casos y él decidió separarlos con un **dato estable**.
Ahora `pedir_permiso` devuelve `(permitida, motivo)` con cinco valores:
`libre`, `autorizada_antes`, `usuario_dijo_si`, `usuario_dijo_toda_la_corrida`,
`usuario_dijo_no`.
→ **Segunda vez que esa decisión suya paga en otro archivo.**

---

## 📏 LA MEDICIÓN DEL DÍA — Y LA FORMA DE LA CUENTA VALE MÁS QUE EL RESULTADO

```
AYER: 7 vueltas · entrada 23.710 · salida 887 · $0.1407
HOY : 7 vueltas · entrada 26.317 · salida 719 · $0.1496
```

| | tokens | dólares |
|---|---|---|
| entrada | **+2.607** | +$0.0130 — el menú engordó 398 por vuelta |
| salida | **−168** | −$0.0042 — el modelo dejó de calcular |
| **neto** | | **+$0.0088** |

> **El texto que le agregas al menú se paga en la ENTRADA de todas las vueltas.
> Lo que le ahorras de pensar se descuenta de la SALIDA, que vale 5 veces más
> por token.** Por eso una regla corta que evita un cálculo largo puede salir
> casi gratis.

### 🚨 EL PRESUPUESTO DEL NIVEL 4 ERA UNA TRAMPA

`PRESUPUESTO_USD = 0.10` allá. La corrida de ayer costó **$0.1407**. Copiado tal
cual **habría cortado a mitad de la tercera pregunta**, y se habrían perdido
horas buscando un defecto en el bucle que no existe.
→ **Un límite heredado sin recalcular no es un freno: es una trampa.**
Quedó en `0.40`, y la corrida real gastó $0.1496 (37% del tope).

### ⏱️ Y UN COSTO QUE NO ESTÁ EN TOKENS

Las llamadas a la API sumaron **20,7 s**. La corrida duró **59 s**. Los otros
**38 segundos fue él decidiendo permisos** — la primera decisión le tomó 26.
No aparece en ningún `usage`, y es el argumento más fuerte a favor de la tecla
`t`: tres permisos idénticos de 26 segundos es cuando el usuario deja de leer y
dice que sí por reflejo.

---

## ⭐ LO QUE PASÓ CON EL FORMATO, Y ES LA NOTICIA DE LA SESIÓN

**SE CORTÓ LA RACHA DE 7 PIEZAS DICTADAS — pero no escribiendo código.**

Él dijo: *"primero explícame sin código alguno en qué consiste el paso 8,
después me dices cuáles son las decisiones abiertas y yo te respondo"*.
**Y respondió las cuatro.** El código lo escribí yo, pero **el diseño es suyo**:
error del modelo como tercera categoría, negar no corta el bucle, permiso por
herramienta, y las tres opciones s/t/n fueron **idea suya**, no del nivel 4.

⚠️ **Y a mitad de sesión frenó otra vez, como en la 13:** *"revisa el README de
04-harness-real, creo que en ese archivo se describen"*. **Tenía razón y yo
estaba equivocado** — yo había dicho que el "6" era una promesa sin lista.
→ **Tercera vez que una intervención suya corrige el rumbo** (las anteriores:
`trm(dias=1)` y *"no es una decisión fácil, podemos analizarlo mejor"*).

⚠️ **Preferencia de formato, confirmada por cuarta sesión:** prosa, sin
selectores de opciones. Y una nueva: **pide el concepto sin código primero.**
Cuando se le explicó el paso 8 con la analogía del mesero y sin una línea de
Python, respondió las cuatro decisiones seguidas.

---

## 💬 SU PREGUNTA DE CIERRE: MULTI-AGENTE (nivel 8, contestada corta)

*"1. ¿Cada agente es un archivo .py? 2. ¿El orquestador sería un bucle externo
y cada agente un bucle interior?"*

Se le contestó corto y se le devolvió al paso 9, pero **la pregunta 2 estaba a
una pieza de la respuesta correcta y la pieza la acababa de construir él**:

> **El agente hijo es una HERRAMIENTA del orquestador.** En su `FUNCIONES`,
> `"trm"` apunta a una función que por dentro tiene `urllib`. En el nivel 8,
> `"investigador"` apunta a una función que por dentro tiene **otro
> `ejecutar_agente()`**. El orquestador no sabe que llamó a un agente: recibe un
> `tool_result` como cualquier otro. **Su puente ya es el mecanismo completo.**

Y a la 1: **un agente no es un archivo.** Son tres cosas —system prompt, menú y
bucle—; tres agentes pueden vivir en un archivo compartiendo `ejecutar_agente()`.

⭐ **Esto cierra su pregunta de la sesión 14** (*"¿puede usar un modelo diferente
según la herramienta?"*), que tal como la hizo no existía. Así sí: el hijo corre
su bucle con `haiku-4-5` y el orquestador con `opus-5`.

**Y el motivo real son sus propios números:** cada agente tiene **su propio
`historial`**, y el del hijo se muere cuando la función retorna. Con 27:1 de
entrada contra salida, los sub-agentes existen sobre todo **para que el bucle de
arriba no repague el trabajo sucio del de abajo**.

→ **Anotado para el nivel 8. No adelantar más.**

---

## Cierre de la sesión 15

**Lo que se hizo:** paso 8 completo — los 9 frenos, escritos y **corridos**.
Dos deudas viejas cerradas (`trm()` ya no manda `T00:00:00.000`; la aritmética
a escondidas, cerrada con un puente). Un defecto nuevo encontrado **por el
registro en su primera corrida** y arreglado con el `motivo`. README del nivel
corregido: la fila del paso 8 ya dice **cuáles** son los frenos.

⭐ **LA LECCIÓN DE MÉTODO, tercera sesión seguida y cada vez más clara:**
hoy **tres cosas salieron de correr o de medir, ninguna de razonar**:

| Hallazgo | De dónde salió |
|---|---|
| Prohibir la división era un callejón | de **escribirlo** y ver que no había salida |
| El registro miente sobre `convertir` | de **leer el `.jsonl`**, no la pantalla |
| El presupuesto del nivel 4 no alcanzaba | de **multiplicar**, no de suponer |

**Las candidatas a lección fuerte del 5b suben a VEINTE.** Las dieciséis
anteriores, más:
17. **Prohibir sin ofrecer salida no es una regla, es un callejón.** Cuando el
    modelo hace algo indebido, primero pregúntate si le falta un puente.
18. **Un límite heredado sin recalcular no es un freno: es una trampa**
    ($0.10 del nivel 4 contra $0.1407 reales).
19. **Un registro que no distingue POR QUÉ pasó algo puede afirmar lo falso.**
    El `motivo` de `trm_en_fecha`, aplicado a los permisos.
20. **Más herramientas no es solo más capacidad: es más formas de
    equivocarse.** Los frenos 7, 8 y 9 no existían en el nivel 4 porque allá
    había una sola herramienta.

⚠️ **`LESSONS.md` sigue sin tocarse, y es correcto** (un bloque por nivel, al
cerrar el nivel). **Al cerrar el 5b hay que escribir las veinte.**

### 📌 DEUDAS ABIERTAS AL CERRAR LA SESIÓN 15

1. **El freno del tamaño del `tool_result`** — se habló y no se hizo. Hoy el
   harness mete en el `tool_result` lo que sea que devuelva una herramienta,
   sin mirarlo. La inyección de la sesión 13 (1 → 1000 filas ≈ 31.000 tokens)
   está cerrada **dentro de `trm_en_fecha`**, no en el harness: una séptima
   herramienta sin ese freno vuelve a abrir la puerta.
2. **`trm_en_fecha` no tiene `usd_por_1_cop`** — mismo hueco del puente, se
   dejó a propósito (cada llave se repaga en cada vuelta). Si algún día hay que
   convertir montos de una fecha pasada, se agrega.
3. **Los caminos 7 y 8 no se han visto atrapar nada.** El modelo no inventó
   nombres en la corrida. La forma barata de forzarlo es el sabotaje de
   siempre: cambiarle el `name` a una herramienta en `TOOLS` sin tocar
   `FUNCIONES`. **Una red que nunca viste atrapar nada no es una red: es un
   comentario.**
4. **`evals.py` no prueba nada del harness.** Los 116 casos son de
   `herramientas.py`. `pedir_permiso` y los tres `except` no tienen un solo
   caso — y se pueden probar gratis, sin red y sin modelo.

### 📂 ARCHIVOS TOCADOS EN LA SESIÓN 15 (para no buscarlos la próxima vez)

| Archivo | Qué cambió |
|---|---|
| `05b-proyecto/agente.py` | los 9 frenos · `PERMISOS` · `anotar()` · `llamar_modelo()` · `pedir_permiso()` con motivo · descripciones de `convertir` y `trm` |
| `05b-proyecto/herramientas.py` | `trm()`: fechas a 10 caracteres + `usd_por_1_cop` |
| `05b-proyecto/README.md` | plan: paso 7 ✅, paso 8 = **9 frenos** ✅, con la lista · fila nueva en la tabla de piezas |
| `05b-proyecto/registro.jsonl` | **nuevo.** 23 líneas de la corrida real. **NO borrarlo:** la línea 13 es la evidencia del defecto del permiso |
| `GUIDE.md` | §4.c pasó de 6 a **9 frenos** · presupuesto que no se hereda · permisos s/t/n con motivo · frenos 7-8-9 nuevos |
| `PROGRESO.md` | esto |

---

## Histórico: sesión 14 — **PASO 7**: `agente.py` CORRE. Claude ya usa sus 6 herramientas

**El agente existe y funciona.** Primera corrida pagada del nivel: 3 preguntas,
**7 vueltas, las 3 respuestas correctas**. Las 6 herramientas dejaron de ser
código que solo él podía llamar.

✅ **Las tres deudas que dejó esta sesión se cerraron en la 15.** Lo que sigue es
el histórico de cómo se veían entonces.

### 📋 ESTADO VERIFICADO AL CERRAR LA SESIÓN 14

Comprobado corriéndolo, no de memoria:

| | |
|---|---|
| `herramientas.py` | 41.374 bytes · **6 herramientas** + **5 ayudantes** · sin tocar hoy |
| `evals.py` | 44.412 bytes · **116 casos, 0 fallaron**, $0.00, sin red · sin tocar hoy |
| `agente.py` | **escrito y corrido** · `TOOLS` (6) + `FUNCIONES` (6) + `ejecutar_agente()` |
| menú vs puente | **coinciden: los 6 `name` = las 6 llaves de `FUNCIONES`** (comprobado) |

### 🚨 LAS 3 DEUDAS DEL PASO 8 (las tres ya están escritas en `agente.py`)

1. **`FUNCIONES[bloque.name]` y `funcion(**bloque.input)` confían en el modelo.**
   Nombre inventado → `KeyError`. Argumento que no existe (`trm(dias=1)`, el que
   corrigió él) → `TypeError`. **Y reventar ahí tumba el bucle entero** — justo
   lo que costó tanto trabajo evitar DENTRO de cada función. El `try` del
   harness le dice al modelo "falló por un defecto interno" y a nosotros nos
   imprime el traceback. Misma forma que el permiso del nivel 4.
2. **⭐ EL MODELO HACE ARITMÉTICA A MANO** (hallazgo de la primera corrida, abajo).
3. **Los permisos por herramienta** — pregunta suya de hoy, ver más abajo.

**Deuda chica que sigue sin decidirse (van 2 sesiones):** `trm()` devuelve las
fechas con `T00:00:00.000`; `historial` y `trm_en_fecha` las recortan a 10.
**Hoy se vio en la corrida real** (`'vigente_desde': '2026-07-30T00:00:00.000'`):
son 56 caracteres de relleno por llamada a `trm`. Una línea, pero es cambio de
comportamiento: se decide, no se hace de paso.

---

## 🚨 EL HALLAZGO DE LA SESIÓN: EL MODELO DIVIDE A ESCONDIDAS

De la pregunta *"¿cuántos dólares son 500 mil pesos colombianos?"*:

```
trm() devolvió       ->  3206.18        (COP por 1 USD)
convertir() recibió  ->  0.00031189777  (USD por 1 COP)
```

**Ese número no salió de ninguna herramienta.** El modelo calculó `1/3206.18`
en su cabeza.

**El hueco de diseño, y es real:** `convertir()` se escribió justamente para que
el modelo NO hiciera aritmética. Pero `trm` entrega la tasa en un sentido y la
pregunta iba en el otro. **Nadie construyó ese puente, así que lo construyó él
— calculando.**

Verificado: se desvió en la **10ª cifra decimal** (`1.2e-10`) y el resultado
salió idéntico. **Y eso es lo peligroso, no el consuelo:** el día que se desvíe
en la 4ª, `convertir()` recibe una tasa perfectamente válida y **ni los 116
casos se enteran**. Es el número creíble en su forma más difícil de ver.

⭐ **La pista que lo delata está en el `usage`:** esa vuelta gastó
**`salida=335`** tokens contra ~60 de las otras. **El costo delata el cálculo.**

→ **Decisión del paso 8, sin tomar:** o `convertir()` voltea la tasa ella misma,
o la descripción le prohíbe invertirla a mano. Las dos tienen costo.

---

## ✅ PASO 7.1 — EL MENÚ (`TOOLS`), Y LO QUE ENSEÑÓ ESCRIBIRLO

⚠️ **DICTADO.** Se le dieron `convertir` y `trm` como ejemplos y se le propuso
escribir las otras cuatro; pidió el archivo completo. **Séptima pieza seguida.**
Se le dijo **una sola vez** y él acotó el encargo por su cuenta —
*"no quiero que escribas el archivo completo, solo la presentación de las
herramientas"*—, y **ya había pegado a mano las dos del ejemplo en el archivo.**
Es menos que escribirlo, pero es más que las 6 anteriores. **Anotarlo como
movimiento en la dirección correcta.**

**El patrón que salió al escribirlas, y es la lección del paso:**

> **Casi toda una buena descripción no dice QUÉ hace la herramienta: dice
> CUÁNDO NO usarla y CON CUÁL NO CONFUNDIRLA.** Decir qué hace es lo fácil.
> Las fronteras son las que evitan el error — y un error de elección cuesta una
> vuelta entera, o sea >3.000 tokens.

Las tres fronteras que se marcaron a propósito:
- **`trm` vs `trm_en_fecha`** — las dos descripciones se nombran mutuamente.
  A `trm_en_fecha` se le PROHÍBE explícitamente usarse para hoy o ayer: *"tú no
  sabes qué día es hoy, pondrías una fecha imaginada y devolverías un número
  real del día equivocado"*.
- **`trm` vs `tasa`** — con los dos números del 2026-07-30 metidos en el texto
  (3206,18 y 3207,64) para que no parezcan intercambiables.
- **`historial` vs `trm_en_fecha`** — tendencia contra día puntual.

---

## ✅ LAS 3 COSAS QUE FUNCIONARON, MEDIDAS EN LA CORRIDA REAL

### ⭐ 1. La advertencia de `historial` FUNCIONÓ. Es la mejor noticia del día

El modelo contestó: *"entre el 1 y el 30 de julio... (20 registros de vigencia)"*.

**NO dijo "en los últimos 20 días".** Usó `desde` y `hasta`, exactamente como se
lo ordenó la descripción.

→ **El defecto que él descubrió midiendo en la sesión 13 —30 registros son 48
días— no llegó a la respuesta del usuario. Y se cerró CON TEXTO, sin una sola
línea de código.** Es la prueba de que la lista `tools` no es documentación:
es comportamiento.

### 2. La cadena de 3 vueltas ocurrió, como estaba previsto

`trm` → `convertir` → responder. **El modelo no se inventó la tasa**: pidió el
número real primero. La frontera de `convertir` (*"esta herramienta NO busca la
tasa"*) hizo su trabajo.

### 3. El modelo admitió que no tiene reloj

*"si hoy ya es un día posterior, la TRM vigente podría ser otra"*.
Honestidad forzada por la descripción — **y la prueba de que la deuda de
`hora_utc` es real**: tiene que andar con esa muletilla porque no sabe qué día es.

---

## 📏 MEDICIÓN — Y ME EQUIVOQUÉ DOS VECES SEGUIDAS, EN EL MISMO SENTIDO

| Método | Resultado |
|---|---|
| A ojo, en el comentario | "~700-900 tokens" |
| Caracteres / 4 | 6.231 / 4 = **~1.557** |
| **`count_tokens(tools=TOOLS)`** | **3.049 exactos, y GRATIS** |

Los dos estimados cortos, **y en el mismo sentido**. La regla de "4 caracteres
por token" viene del inglés en prosa; **JSON en español tokeniza mucho peor**.

⚠️⚠️ **Y lo incómodo: `GUIDE.md` §5.b YA documentaba `count_tokens` desde el
nivel 5.** La herramienta que me habría evitado equivocarme dos veces estaba
escrita en su propia guía y no la usé — estimé. Lo que faltaba en la guía era
**decir que acepta `tools=`**, que es justo lo caro. Ya está corregido.
→ **Tener la herramienta documentada no es lo mismo que acordarse de usarla.**

**Aislar el costo del menú son tres llamadas gratis y una resta:**

```
solo el mensaje  :     8
+ system         :   171   -> el system cuesta   163
+ system + tools : 3.220   -> EL MENÚ CUESTA   3.049
```

→ **REGLA NUEVA: el único contador que vale es el de la API. Y es gratis, así
que no hay excusa para estimar.**

**Y la proporción de la corrida completa dice lo que hay que entender de un
agente:**

```
7 vueltas · entrada 23.710 tokens · salida 887 tokens
```

> **La entrada es 27 veces la salida. Un agente no paga por lo que dice: paga
> por lo que RELEE en cada vuelta.**

Y pone en perspectiva media sesión 13: el resumen de `historial` ahorra **143
tokens por vuelta**; el menú cuesta **~2.900**. **Veinte veces más que la
decisión que costó media sesión analizar.** No invalida aquel análisis (el
método sigue siendo el bueno) — pero dice **dónde está el dinero de verdad**.

---

## 💬 SUS DOS PREGUNTAS DE HOY (las dos buenas, las dos anotadas)

### 1. *"¿deberíamos poder configurar los permisos que le asignamos?"*

**Sí, y es del paso 8.** Es su propia decisión del nivel 4 (el permiso de
`borrar_archivo()` va en el harness, no dentro de la función) aplicada a seis
herramientas en vez de una.

Lo que se le mostró, y es la parte que enseña — **no son dos categorías, son tres:**

| Herramientas | Qué tocan | |
|---|---|---|
| `convertir` | nada | libre |
| `tasa`, `trm`, `historial`, `trm_en_fecha` | leen un servidor **ajeno** | cuesta, no rompe |
| **`guardar_reporte`** | **escribe en el disco** | **deja huella** |

> **La pregunta no es "¿lee o escribe?", es: si esto sale mal, ¿lo puedo
> deshacer?**

⭐ **Y el detalle que lo conecta con lo que él ya mide:** el permiso **no le
cuesta un solo token al modelo** — la tabla vive en Python y el modelo nunca la
ve. Explicárselo en la descripción sí se pagaría en cada vuelta.
→ **Lo que puede vivir en el harness, que viva en el harness: es gratis ahí e
impuesto permanente allá.**

### 2. *"¿puede usar un modelo diferente según la herramienta?"*

**Hubo que corregirle una pieza, y es de las que se quedan mal puestas:**

> **El modelo no ejecuta la herramienta. La ejecuta el harness.** Dentro de sus
> seis funciones no hay ningún modelo: hay `urllib` y unos `if`. **Por eso
> `evals.py` corre 116 casos por $0.00.**

Tal como la preguntó, no existe. Pero su intuición apunta a tres cosas reales
que sí existen y son de más adelante: un modelo distinto para el bucle (eso sí,
es una línea), una herramienta que por dentro llama a otro modelo, y el
enrutamiento (modelo barato decide, caro ejecuta).

→ **Lo que sí le toca ya: escoger el modelo del bucle.** Y hay un experimento
honesto para el paso 9: correr lo mismo con `claude-opus-5` y con
`claude-haiku-4-5` y ver **si el barato escoge bien entre seis herramientas**.
El riesgo de un menú largo no es el precio: es que se equivoque al escoger.

---

## Cierre de la sesión 14

**Lo que se hizo:** paso 7 completo. `agente.py` pasó de **0 bytes** a un agente
que corre: menú de 6, puente de 6, bucle con `usage` por vuelta. Primera corrida
pagada del nivel — **7 vueltas, 3 respuestas correctas**. Tres deudas del paso 8
anotadas DENTRO del código, en el sitio donde se leerán solas.

⭐ **LA LECCIÓN DE MÉTODO DE LA SESIÓN, y es la misma de la 13 con otra ropa:**
hoy se encontraron **tres cosas, y ninguna salió de razonar**:

| Hallazgo | De dónde salió |
|---|---|
| El modelo divide a escondidas | de **correrlo** |
| El menú pesa el doble de lo estimado | del **`usage`** |
| Su advertencia de "registros, no días" funciona | de **leer la respuesta** |

→ **Las tres las habría jurado de otra forma.** Es *"verificar también lo que
uno acaba de escribir con toda seguridad"*, segunda sesión seguida.

**Las candidatas a lección fuerte del 5b suben a DIECISÉIS.** Las trece
anteriores, más:
14. **Una buena descripción de herramienta dice sobre todo CUÁNDO NO usarla y
    con cuál no confundirla.** Y el menú es comportamiento, no documentación:
    el defecto del `dias` se cerró con texto, sin código.
15. **El modelo hace aritmética a escondidas cuando falta un puente entre dos
    herramientas** — y el `usage` de salida lo delata.
16. **El único contador de tokens que vale es el `usage` de la API.** Dos
    estimados seguidos, los dos cortos, en el mismo sentido.
    Y: **un agente paga por lo que RELEE, no por lo que dice** (27:1).

⚠️ **`LESSONS.md` sigue sin tocarse, y es correcto** (un bloque por nivel, al
cerrar el nivel). **Al cerrar el 5b hay que escribir las dieciséis.**

⚠️ **DEUDA DE FORMATO — VAN 7 PIEZAS SEGUIDAS DICTADAS**, pero **hoy se movió**:
acotó el encargo por su cuenta ("solo la presentación de las herramientas, no el
archivo completo"), **pegó a mano en el archivo las dos descripciones de
ejemplo**, y **pidió ver el bucle en pantalla antes de escribirlo**
(*"pero primero lo muestras para entenderlo"*). Eso último es nuevo y es bueno:
es querer entender antes que tener. Se le dijo una vez y no se repitió.

**Dónde cortar la racha, y el paso 8 es mejor sitio que el 7:** las tres deudas
son **decisiones**, no transcripción — y decidir es justo lo que él hace bien
(lleva dos diseños míos corregidos). Empezar preguntándole **qué debería pasar**
cuando el modelo pide una herramienta que no existe, antes de escribir el `try`.

⚠️ **Preferencia de formato, confirmada otra vez:** se le habló en prosa toda la
sesión, sin un solo selector de opciones, y respondió largo y con criterio.

---

## Histórico: sesión 13 (pasos 6 y 6b — las 6 herramientas terminadas)

Al cerrar la sesión 13: `herramientas.py` 41.374 bytes con las 6 herramientas y
5 ayudantes; `evals.py` 44.412 bytes con **116 casos, 0 fallos**, $0.00 y sin
red; `agente.py` en 0 bytes.

---

## ⭐ LA IDEA DE LA SESIÓN ES SUYA, Y ES MEJOR QUE LAS TRES MÍAS

Contexto: se decidió que `historial` devuelve un **resumen**, no las filas. Eso
abre un hueco — si el usuario pregunta *"¿cuánto valió el 15 de julio?"*, el
modelo no lo sabe **y no tiene cómo averiguarlo**, así que o se rinde o se lo
inventa (y con máximo, mínimo y promedio en la mano, puede inventar algo muy
creíble). Se le ofrecieron 3 salidas, las tres **metiendo el día puntual DENTRO
de `historial`**: respuesta de tamaño variable, un parámetro `detalle`, o
confiar en que el modelo lea la descripción.

**Él propuso una cuarta: una herramienta aparte que lea UNA fecha del pasado.**

Y es la aplicación de **su propia regla**, la que salió al corregir mi
`trm(dias=1)` en la sesión 12: *dos herramientas que se pisan obligan al modelo a
elegir entre dos caminos para lo mismo; una cosa cada una.* Mis tres opciones
parchaban `historial`; él aplicó la regla que ya estaba establecida.
→ **Vale la pena decírselo: es la segunda vez que corrige un diseño mío** (la
primera fue `trm(dias=1)`), y esta vez sin que se le pidiera.

**Las 5 pruebas contra la fuente ya están corridas (2026-07-30), no hay que
volverlas a hacer.** La fuente acepta `$where` con rango de fechas:

```
$where=vigenciadesde <= 'FECHA' AND vigenciahasta >= 'FECHA'   (espacios como %20)
```

| Fecha pedida | Resultado |
|---|---|
| 2026-07-30 (jueves) | 1 fila ✅ |
| **2026-07-26 (DOMINGO)** | **1 fila: la vigente 25→27, `3210.56`** ✅ |
| 2024-03-05 (hace 2 años) | 1 fila, `3948.67` ✅ |
| 2027-01-01 (futuro) | **0 filas**, sin error |
| 1990-01-01 | **0 filas**, sin error |

⭐ **El domingo se resuelve solo.** No hay que calcular nada de calendario: se
pregunta por rango y **la fuente sabe qué fila cubre qué días**. Es la misma
idea que ya estaba en `trm()`, pero ahora usada para *buscar*, no solo para
informar.

**Los 3 problemas nuevos que traerá (material del paso):**
1. **La fecha la escribe el modelo:** va a mandar `"15 de julio"`, `"15/07/2026"`,
   `"2026-7-5"`. Freno de formato, clase que él no ha hecho.
2. **0 filas NO es error de red.** Y el mensaje tiene que decir *por qué*:
   ¿futura? ¿anterior al dataset? Son cosas distintas para el modelo.
3. **Una URL armada con texto que viene de afuera.** Hasta hoy todas sus URLs
   eran constantes. Esto tiene nombre propio en seguridad.

⚠️ **Y algo que su idea deja claro sin querer: `trm()` NO queda redundante.** No
se puede reemplazar por `trm_en_fecha("hoy")` porque **el modelo no sabe qué día
es** — no tiene reloj, pondría la fecha que se imagine, y volvemos al número
creíble. Es la misma razón por la que `trm()` no mira el reloj.

---

## ✅ `trm_en_fecha(fecha)` — LA 6ª HERRAMIENTA, IDEA SUYA. 27 casos + corrida real

⚠️ **DICTADA.** Se le dio el esqueleto con 6 huecos y un ejemplo desechable
(`validar_hora`, con `"25:99"` como el caso que justifica `strptime`), y pidió
*"escribe la herramienta completa y después me la explicas"*. **Sexta seguida.**
Se le había dicho una vez en esta misma sesión; no se repitió (repetir es
regañar). Ver la deuda de formato al final.

**Decisión suya:** *"que distinga el porqué, para que el modelo pueda
explicar"*. Cero filas tapa tres situaciones distintas y ahora se separan.

### 🚨 LO MÁS IMPORTANTE DEL DÍA: LA INYECCIÓN, DEMOSTRADA EN VIVO

Primera URL del proyecto que se arma con **texto de afuera** (todas las demás
eran constantes). La consulta pone el dato entre comillas simples:

```
$where=vigenciadesde <= 'LA_FECHA' AND ...
```

Se probó contra **la fuente real** con `2026-07-30' OR '1'='1`:

```
filas devueltas: 1000
```

La comilla **cerró** la que abría el dato, y lo que seguía dejó de ser dato:
se volvió **parte de la pregunta**. Pedimos un día y trajo el dataset entero
(1000 = el tope del servidor).

**Y el daño es DOBLE, y el segundo casi nadie lo ve:**
| | |
|---|---|
| Respuesta equivocada | el agente reporta cualquier cosa |
| **Bomba de tokens** | 1000 filas ≈ **125.000 caracteres ≈ 31.000 tokens**, repagados en CADA vuelta |

→ Un `tool_result` de 175 caracteres se vuelve uno de 125.000. Por una comilla.
→ **La defensa es su LISTA DE PERMITIDOS de `guardar_reporte`**, no una lista de
prohibidos: no se pregunta "¿tiene comillas?" (siempre falta un carácter), se
exige la forma exacta `AAAA-MM-DD`. **Lo que no se nos ocurrió también queda
afuera.** Y no hubo que escribir una sola línea pensando en comillas.

⚠️ **Distinción que hay que conservar: `quote()` NO es el freno.** Codifica para
transportar; codificar una comilla no la rechaza, la transporta intacta.
**El freno decide QUÉ entra; `quote()` solo lo lleva sin romperse.** Confiar en
`quote()` para la seguridad es confiar en el bus para decidir quién viaja.

### 🐛 DEFECTO REAL ENCONTRADO POR LA PRIMERA CORRIDA (no por razonar)

`strptime` con `%Y-%m-%d` **NO exige el cero a la izquierda**: `"2026-7-5"` le
encaja igual que `"2026-07-05"`. Yo escribí ese freno convencido de lo
contrario. **Lo dijo la corrida, no el análisis.**

Y el defecto no era cosmético: se **validaba una cosa y se mandaba otra** (a la
URL iba el texto original). Eso rompe la comparación de fechas como texto:

```
"2026-7-5" > "2026-07-30"   ->   True   (en el 6º carácter, "7" > "0")
```

El agente diría **"todavía no hay TRM para esa fecha"** de un día que ya pasó,
con toda seguridad. → Arreglado con `fecha = dia.strftime(FORMATO_FECHA)`.
→ **REGLA NUEVA: después de validar, usa lo VALIDADO, no lo que llegó.**

### ⭐ EL TRUCO DEL CALENDARIO: no le preguntes al reloj, pregúntale a la fuente

Para decir "esa fecha es futura" hacía falta saber qué día es hoy — y una
función que mira el reloj **deja de poderse probar con datos fijos** (la razón
por la que `trm()` no calcula "¿es de hoy?"). La salida: `URL_TRM_RANGO`, una
consulta con `$select=min(vigenciadesde),max(vigenciahasta)`.

**Verificado: la fuente cubre del `1991-12-02` al `2026-07-30`.**

→ **La fuente es su propio calendario.** Determinista, probable, sin reloj. Y la
segunda llamada solo ocurre **en el camino del fallo**, que es raro.

**Los 4 motivos** (`futura`, `muy_antigua`, `hueco`, `desconocido`). El último
importa: **si la consulta del rango también falla, NO se inventa el motivo.**
Un motivo inventado es peor que ninguno — familia del número creíble.

### 🎨 Y EL EVAL MEJORÓ EL DISEÑO: el `motivo` como DATO

Al escribir los casos apareció el choque: **¿cómo pruebo que los tres motivos
son distintos, si su propia regla del paso 5 prohíbe comparar el texto de un
error?** Salida: que el motivo sea un **dato estable** (`"futura"`,
`"muy_antigua"`, `"hueco"`, `"desconocido"`) al lado de la frase, que se puede
reescribir cuando se quiera.
→ **La prueba no solo verificó el código: lo mejoró.** El modelo también gana:
ramifica por un valor fijo y no por cómo esté redactada una frase.

### 🎭 PIEZA NUEVA EN `evals.py`: el doble de DOS RESPUESTAS

Primera herramienta que hace **dos consultas distintas** (el dato y el rango).
Un doble que conteste siempre lo mismo no sirve: para probar "es futura" hace
falta que la primera devuelva vacío **y** la segunda devuelva el rango.
`servidor_dos_respuestas()` mira si la URL trae `$select` y escoge.
→ **El actor ahora tiene dos parlamentos y escoge según la pregunta.**

### LOS 4 SABOTAJES — 3 predicciones exactas y ⚠️ UNA FALLADA (mía)

| | Predicho | Real |
|---|---|---|
| **A** quitar la normalización | 1 | ✅ 1 |
| **B** quitar el freno `strptime` | 7 | ⚠️ **13** |
| **C** juntar `fecha_pedida` con `vigente_desde` | 1 | ✅ 1 |
| **D** `>` por `>=` en "es futura" | 1 | ✅ 1 |

⚠️ **La predicción B falló y se deja escrita con la razón**, como la del paso 5.
Dos causas, y son distintas: (1) conté 7 y eran **8** — se me pasó
`fecha vacia`; (2) los otros **5 fueron efecto secundario de CÓMO saboteé**:
reemplacé `strptime` por una fecha fija, y como la normalización usa lo que él
devuelve, **todas las fechas se volvieron `2026-07-30`**.
→ Lo que sí enseña, y no estaba previsto: **romper un freno no rompe solo el
freno.** El resto de la función depende de lo que produce. Está encadenado.

**Lo que B sí demostró, que era el objetivo:** las dos inyecciones salieron con
`REVENTO: AssertionError`, o sea **llegaron a la red**. Con el freno puesto
mueren limpias y **la consulta ni se arma**.

⭐ **EL SABOTAJE C ES EL MÁS INSTRUCTIVO: falló SOLO el caso `domingo`.**
`feliz` y `fecha sin ceros` pasaron tranquilos, porque en un día normal la fecha
pedida y la vigencia **son la misma** y el defecto es invisible.
→ **Misma forma que el `feliz con filas al reves` de `historial`: el caso raro
no era adorno, era el único con ojos.** Un eval hecho solo de días normales
habría dado verde con el agente diciendo "el 26 la TRM fue X" de un día en que
no se publicó nada.

**El sabotaje D** también se ganó el sueldo: un carácter (`>` → `>=`) y el
agente diría "todavía no hay TRM para hoy" del día que sí la tiene.

### La corrida real (2026-07-30) — lo que el doble no puede dar

```
2026-07-30 (jueves)  -> 3206.18   vigente 2026-07-30 a 2026-07-30
2026-07-26 (DOMINGO) -> 3210.56   vigente 2026-07-25 a 2026-07-27  ⭐
2024-03-05 (2 anios) -> 3948.67
2027-01-01 (futura)  -> "el dato más reciente que publica la fuente es del 2026-07-30"
1990-01-01           -> "la serie oficial empieza el 1991-12-02"
```

**175 caracteres, ~43 tokens: la más barata de las seis herramientas.**

⚠️ **Inconsistencia menor anotada, sin resolver:** `trm_en_fecha` e `historial`
recortan las fechas a 10 caracteres; **`trm()` todavía devuelve el
`T00:00:00.000` completo** (28 caracteres de relleno). Arreglarlo es una línea
y no rompe ningún caso — pero es cambio de comportamiento, así que se anota y
se decide, no se hace de paso.

---

## 🧠 CÓMO SE DECIDIÓ EL RECORTE — el método vale más que la decisión

⚠️ **Él frenó la decisión:** se le presentaron 3 opciones y contestó
*"amigo no es una decisión fácil, podemos analizarlo mejor"*. **Tenía razón y
hay que anotarlo**: la iba a tomar a ojo. De ahí salió todo lo bueno del día.

**Se midió con los 30 días reales**, no con estimados:

| Opción | Caracteres | Tokens | vs. crudo |
|---|---|---|---|
| Crudo, sin recortar | 3.808 | ~952 | — |
| **A resumen** | **238** | ~59 | **16x** |
| B filas recortadas | 811 | ~202 | 4,7x |
| C resumen + filas | 997 | ~249 | 3,8x |

**Lo primero que salió al medir: botar el ruido no está en discusión.**
`"unidad":"COP"` repetido 30 veces y `T00:00:00.000` repetido 60 no lo necesita
nadie. La pregunta de verdad era solo **A contra B: 143 tokens por vuelta.**

**Y ahí el número solo no alcanzaba.** Se puso al lado de otro: **una vuelta
extra del bucle** (repagar SYSTEM + menú de 5 herramientas + historial) cuesta
**más de 1.000 tokens**. O sea que ahorrar 143 puede salir carísimo si obliga a
una segunda llamada.

**La pregunta se le devolvió convertida en una sobre SU agente:** *"¿qué vas a
preguntar más: cómo va el dólar, o cuánto valió tal día?"*. Contestó **"cómo va
el dólar"** → gana A.

⭐ **Y lo que hay que conservar del método es el punto de equilibrio:**

```
236 + (p × 1.000) = 808   →   p = 0,57
```

> **A gana mientras necesite el día puntual menos del 57% de las veces.**

No se decidió con un pálpito ni con un "creo que casi siempre": se decidió con un
número que dice **cuánto puede estar equivocado y seguir teniendo razón**. Aunque
se haya quedado corto y sea 40%, A sigue ganando. **La decisión es robusta, y eso
es un resultado distinto de "la decisión es correcta".**

### 🆕 EL CONCEPTO NUEVO: el menú también se paga

Al evaluar su idea salió algo que no se había tocado en todo el curso:

| Qué | Cuándo se paga |
|---|---|
| Un `tool_result` gordo | desde la vuelta en que se llamó, en adelante |
| **Una herramienta en la lista `tools`** | **desde la vuelta 1 de TODAS las conversaciones, aunque nunca se llame** |

Una herramienta bien descrita son ~100–150 tokens **por vuelta, siempre**.
→ **Un `tool_result` es un impuesto permanente; una herramienta de más es un
impuesto permanente que se paga aunque nunca la uses.** Y peor que los tokens:
**un menú largo hace que el modelo se equivoque más al escoger** (medible en el
paso 9).

⚠️ **Se le dijo el resultado incómodo sin maquillarlo: en puros tokens su idea
NO gana.** A + 6ª herramienta ≈ 960 tokens en una conversación de 6 vueltas;
B sola ≈ 810. **Gana en otra cosa:** B no puede contestar por el 3 de marzo de
2024 **nunca**, pida lo que pida. → **Comparar herramientas solo por lo que
cuestan es como escoger empleado por lo que cobra: primero se pregunta si hace
el trabajo.**

---

## 🚨 EL DEFECTO QUE SOLO APARECIÓ POR MEDIR: `dias` MIENTE

Al traer los 30 días de verdad, el resumen salió con `desde: 2026-06-12`.
**30 filas = 48 días de calendario.** Y `historial(5)` dio 7 días.

La fuente **no guarda un registro por día: guarda uno por VIGENCIA.** La TRM del
viernes vale también sábado y domingo, así que un fin de semana entero es UNA
fila. 7 fines de semana + festivos ≈ los 18 días que faltaban.

Si el parámetro se llama `dias`, el modelo diría *"en los últimos 30 días el
dólar bajó 8,75%"* y **sería falso**: fueron 48. El número está bien; **la frase
que lo acompaña miente**. Es su lección de la sesión 11 (el *"solo letras y
números"* que prometía lo que no cumplía) aplicada a un nombre de parámetro.

**Cómo quedó (decisión mía, revocable, y se le dijo):** el parámetro se sigue
llamando `dias` —el modelo y el usuario piensan en días; con `filas` el modelo
tendría que *adivinar* cuántas filas son un mes, y adivinar es lo que no
queremos— pero el dict devuelve `registros`, `desde` y `hasta`, así que **la
función nunca afirma "los últimos 30 días"**. La alternativa (recortar de verdad
a N días de calendario) se puede y **queda anotada como deuda**: pide aritmética
de fechas, un tema nuevo a mitad de otro. README del nivel corregido.

→ **Esto no se sabía 10 minutos antes. Salió de medir en vez de suponer.**

---

## ✅ `historial(dias)` — escrita, 27 casos, corrida real, 248 caracteres

⚠️ **DICTADA.** Se le dio primero el esqueleto con **6 huecos numerados** en el
archivo y se le pidió empezar por el 1; contestó *"escribe los 6 huecos por favor
y la herramienta completa y después me la explicas"*. **Quinta pieza seguida
dictada.** Se le dijo una vez, sin insistir, y se le propuso el trato de que
`trm_en_fecha` sea suya.

**Lo nuevo que trajo esta función, y ninguna anterior tenía:**

1. **Un tope que protege a un TERCERO.** `MAX_REGISTROS = 400`. Y el comentario
   dice lo importante: **este tope no protege nuestros tokens** (el resumen pesa
   igual con 30 filas que con 400), protege **al servidor del gobierno** y al
   usuario que se queda esperando. `100000` no es basura: es un número
   perfectamente válido con el que el modelo hace un destrozo sin querer.
   → Primer freno del curso que no defiende al propio programa.
2. **`.is_integer()` en vez de `int()`.** `3.5` se rechaza, `30.0` se acepta
   (es un 30 con decimales; rechazarlo sería castigar al modelo por una coma).
   **`int(3.5)` daría 3 en silencio** — haría algo distinto de lo pedido sin
   avisarle a nadie. Es la categoría del número creíble, otra vez.
3. **`continue` en vez de `return`** dentro del bucle: los mismos frenos de
   `trm()`, pero una fila que se cae no tumba a las otras 29.
4. **`serie.sort()` y el regalo del formato ISO.** Se ordena aquí en vez de
   confiar en el `$order` de la URL. Y ordenar es **gratis** porque la fecha es
   `"AAAA-MM-DD"`: el ISO se ordena solo como texto, sin convertirlo a fecha.
   → **Por eso se recortó a 10 caracteres y no a 4 ni a 7: el corte no fue
   estético, se escogió el punto donde la fecha todavía se ordena bien.**
5. **`if not serie: return error`** — un promedio de cero números no existe
   (`sum([])/len([])` es `ZeroDivisionError`).
6. **Los redondeos son de PRESENTACIÓN**, al final y nunca sobre un número que
   se vuelve a usar. Es la trampa de `tasa()` (`0.00031` → `0.0`) ya interiorizada.

**LA DECISIÓN DEL HUECO 4 (mía, revocable): una fila podrida se salta y se
cuenta, no tumba la respuesta.** 29 días buenos siguen contestando "¿cómo va el
dólar?". **Pero el descarte no se esconde:** se devuelve `descartados`, porque
decidir si 29 de 30 sirven **es criterio, o sea del modelo** — la misma regla del
domingo en `trm()`. Callarlo sería el `except Exception` que no se puso en
`pedir_json`: un problema real disfrazado de respuesta normal.

⚠️ **Y la llave `descartados` solo aparece si hubo descartes.** Un
`"descartados": 0` fijo sería ruido que se repaga en cada vuelta.

**Corrida real 2026-07-30:** `historial(30)` → 248 caracteres (~62 tokens),
30 registros del 12-jun al 30-jul, promedio 3334.44, **cambio -8,75%**.
El estimado era 238; el real 248.

---

## 🪤 LOS 27 CASOS, Y UNA PIEZA NUEVA EN `evals.py`

**8 rechazos sin red** (con la trampa puesta: hacen doble trabajo, comprueban el
rechazo **y** demuestran que los frenos están antes de la red) + **19 con
servidor de mentira**.

### La pieza nueva: el `esperado` puede ser un DICCIONARIO

`historial` devuelve muchas cosas y varias vale la pena mirarlas a la vez. Los
casos nuevos comparan **solo las llaves que se nombran**, no el dict entero.
→ **Misma razón por la que nunca se compara el texto de un error:** el día que se
le agregue una llave al resumen, no se tienen que romper 10 casos. La prueba
tiene que dejar mejorar el código.

**Truco:** `r.get(k)` da `None` cuando la llave no está, así que un esperado con
`"descartados": None` **comprueba que la llave NO exista.**

### ⚠️ Y ESO DESTAPÓ UN DEFECTO VIEJO ESCONDIDO UN PISO MÁS ABAJO

```python
{"promedio": 4000.0} == {"promedio": 4000}   # True
```

El `==` de los diccionarios compara los valores con `==`, y **`4.0 == 4` es
True**. O sea: la comparación estricta de tipos que él endureció en el paso 5
**se perdía en cuanto el esperado dejaba de ser un número suelto.** Es su propio
defecto del `4.0 == 4`, reaparecido en otra forma.
→ Se escribió `igual_estricto(a, b)`, que compara tipo **y** valor, y en los
dicts va llave por llave. **Tercera vez que ese hallazgo del paso 5 paga.**

### LOS 3 SABOTAJES — predicción escrita antes de correr, las 3 exactas

Se predijo **2, 9 y 1**. Salió **2, 9 y 1**.

**A — quitar `serie.sort()` → 2 rojos. EL HALLAZGO DEL DÍA:**

```
esperado  'desde':'2026-07-01'  'cambio_pct': 33.33
obtenido  'desde':'2026-07-03'  'cambio_pct': -25.0
```

Sin ordenar, la función dice que el dólar **bajó 25%** cuando **subió 33%**. No
revienta, no avisa: devuelve un número creíble **con el signo al revés**.
→ **Cuarta aparición del patrón hoy** (con `monto=True → 3900`,
`moneda=[] → 39000`, `tasa<0 → -4000.0`), y **el peor de los cuatro**: un −25% en
una serie de dólares no le llama la atención a nadie.

⭐ **Y el detalle que más enseña, también predicho:** el caso
`feliz con filas al reves` **pasó tranquilo** con el sabotaje puesto. Con el
`sort()` roto la función acierta **solo cuando el servidor manda al revés de como
manda hoy**. Con un solo caso feliz —el que copia el orden real— habría habido
verde con la función rota.
→ **Dos casos con los MISMOS datos en distinto orden no son un caso repetido:
son la única forma de ver una dependencia oculta del orden.**

**B — que `descartados` nunca se informe → 9 rojos.** Una línea rota, 9 casos.
Y `registros: 3` estaba **bien** en los nueve: la función devolvía 3 días
correctos **y se callaba que botó uno**. Solo lo cazó la llave del descarte —
igual que el sabotaje del `write_text`, donde las dos primeras columnas
coincidían.

**C — quitar el freno de decimales → 1 rojo, con `REVENTO: AssertionError`.**
`3.5` pasa el freno, `int(3.5)` da 3 en silencio y la función **sale a la red**:
**saltó la trampa**. Segundo trabajo de la trampa confirmado otra vez: no solo
documenta que el eval es gratis, **detecta un freno movido de sitio**.

**Restaurado y verificado: `88 casos, 0 fallaron`.**

---

## Cierre de la sesión 13

**Lo que se hizo:** pasos 6 **y** 6b cerrados. `historial(dias)` y
`trm_en_fecha(fecha)` escritas, 27 casos cada una, las dos corridas contra la
fuente real. `evals.py` de **61 a 116 casos**, sigue en **0 fallos**, **$0.00** y
**sin red**. Dos defectos reales corregidos en el README (`historial(de,a,dias)`
era imposible con estas fuentes; el `dias` que miente). Dos defectos reales
encontrados **corriendo** (la normalización de la fecha; y el `4.0 == 4`
escondido en la comparación de dicts, tapado con `igual_estricto`).
**Y una vulnerabilidad de inyección demostrada en vivo y cerrada.**

**Los 7 sabotajes de la sesión:** 3 sobre `historial` (2, 9, 1 — las tres
predicciones exactas) y 4 sobre `trm_en_fecha` (1, 13, 1, 1 — tres exactas y
**una fallada, escrita con su razón**). Ninguna prueba de hoy se dio por buena
sin verla ponerse roja primero.

**Las candidatas a lección fuerte del 5b suben a TRECE.** Las seis de la sesión
12, más:
7. **Un plan escrito antes de mirar los datos se corrige con los datos**
   (`historial(de,a,dias)`, y el `dias` que miente).
8. **Decidir con el punto de equilibrio, no con la respuesta:** el 57% dice
   cuánto puedes equivocarte y seguir teniendo razón.
9. **El menú también se paga:** una herramienta de más cuesta en cada vuelta de
   cada conversación, aunque nunca se llame.
10. **INYECCIÓN — la primera vez que un dato de afuera entra a una consulta.**
    Demostrada en vivo (1 → 1000 filas). La defensa es la lista de PERMITIDOS,
    no la de prohibidos. Y `quote()` transporta, no decide.
11. **Después de validar, usa lo validado, no lo que llegó** (`2026-7-5`).
12. **El caso raro no es adorno: suele ser el único con ojos.** Dos pruebas
    independientes del mismo patrón hoy — `feliz con filas al reves` y
    `domingo` fueron los únicos que vieron su sabotaje.
13. **Escribir la prueba mejora el diseño**, no solo lo verifica: el `motivo`
    como dato nació de no poder comparar el texto del error.

⚠️ **Y una candidata de método, distinta de las técnicas:** hoy **dos defectos
reales salieron de CORRER, no de razonar** (la normalización, y que 30 filas
eran 48 días). Los dos los escribí yo convencido de lo contrario.
→ **"Verificar también lo que resultó ser verdad" tiene un hermano: verificar
también lo que uno acaba de escribir con toda seguridad.**

⚠️ **`LESSONS.md` sigue sin tocarse, y es correcto** (un bloque por nivel, al
cerrar el nivel). **Al cerrar el 5b hay que escribir las nueve.**

**Su intervención del día:** *"no es una decisión fácil, podemos analizarlo
mejor"* — frenó una decisión que se iba a tomar a ojo. De ahí salieron la
medición, el punto de equilibrio, el defecto del `dias` y su propia idea de
`trm_en_fecha`. **Segunda sesión seguida en que una pregunta suya cambia el rumbo
para bien** (la anterior fue *"¿la función tasa ya está totalmente
implementada?"*). Vale la pena decírselo.

⚠️⚠️ **DEUDA DE FORMATO — VAN 6 PIEZAS SEGUIDAS DICTADAS.** `pedir_json`,
`tasa`, la ampliación de `evals.py`, `trm`, `historial` y `trm_en_fecha`.
**Las dos veces de hoy se le dio el esqueleto con huecos numerados PRIMERO** (y
con `trm_en_fecha`, además, un ejemplo desechable sobre otra función), y las dos
veces pidió que se llenaran igual. Se le dijo una vez por sesión y no se repitió
— repetir es regañar, y esto es su curso.

**El dato duro para la próxima sesión: desde `convertir()` y `guardar_reporte()`
(sesiones 10 y 11) no ha escrito una línea de código él.** Lo que sí conserva:
lee, entiende, corrige diseños ajenos y toma buenas decisiones — hoy dos.

**Dónde cortar la racha, y hay una oportunidad natural en el paso 7:** el bucle
agéntico del nivel 3 **ya lo escribió una vez**. `agente.py` no es material
nuevo, es material que él ya tocó. Es el mejor sitio del nivel para que vuelva a
escribir. **Ofrecérselo así: "este ya lo hiciste una vez".**

⚠️ **Preferencia de formato observada (nueva):** rechazó **dos veces** el
selector de opciones y en cambio respondió largo y bien cuando las opciones se
le pusieron en texto normal. **Preguntarle en prosa, no con menús.**

---

## Histórico: sesión 12 (pasos 6 al 75%)

### URLs revisadas hoy 2026-07-30: las dos HTTP 200. Tercer dato de la brecha

| Día | Mercado | TRM oficial | Brecha |
|---|---|---|---|
| 2026-07-28 | 3.215,61 | 3.205,80 | ~10 pesos |
| 2026-07-29 | 3.206,17 | 3.205,87 | 0,30 pesos |
| **2026-07-30** | **3.207,64** | **3.206,18** | **1,46 pesos** |

Tres observaciones, tres brechas. **Confirma con datos** lo que el README decía
como sospecha: lo estable es *que son fuentes distintas*, nunca la magnitud.

### 🐛 DEFECTO REAL DEL README, CORREGIDO HOY

§5b.4 decía `?$order=vigenciadesde DESC` **con un espacio de verdad**. Verificado
con `curl` en la sesión 9 (y funcionaba: `curl` codifica el espacio solo). Pegado
en `urllib` **revienta**: `http.client.InvalidURL: URL can't contain control
characters`. Va `%20`. → **Una URL verificada con una herramienta no está
verificada para otra.** Es *"verificar también lo que resultó ser verdad"* otra vez.

### La decisión del "hueco 3" — y se validó POR ACCIDENTE a los 10 minutos

`pedir_json` **no tiene `except Exception`**. Razón dada: hay dos clases de falla
que se parecen y no son lo mismo.

| Falla | Qué es | Qué merece |
|---|---|---|
| No hay red, 503 | El **mundo** falló | `{"error": ...}` → conversación |
| `NameError`, un typo | **Nuestro código** está roto | Que se caiga fuerte y visible |

Un error del mundo es información; un error nuestro es un **defecto**, y taparlo
lo deja vivo para siempre disfrazado de "problemas de conexión".

⚠️ **Y pasó de verdad:** el espacio de la URL lanzó `InvalidURL`, que **no** es
hijo de `URLError` ni de `OSError` (comprobado). No lo atrapó nadie → salió el
traceback con la línea exacta y el motivo real. **Con `except Exception` habría
dicho "no pude conectarme" tras 3s de espera, y él se habría puesto a revisar el
router por un espacio en un texto.** → **Candidata a lección fuerte del 5b.**

⚠️ **Deuda que esto abre, apuntada en el código:** el contrato del archivo dice
"ninguna lanza excepciones". La red de seguridad va **en el harness** (paso 8):
un `try` alrededor de cualquier herramienta que le diga al modelo "falló por un
defecto interno" y a nosotros nos imprima el traceback — el bucle sobrevive **y**
el bug se ve. Misma forma que el permiso del nivel 4, que se pedía en el harness
y no dentro de `borrar_archivo()`.

### La regla del paso 6 (salió de una respuesta suya)

Se le preguntó quién debe reintentar cuando se cae el internet: A la función,
B el modelo, C el harness. **Contestó B, "porque el modelo decide si vale la
pena".** Buena razón, opción cara: cada reintento del modelo es **una vuelta más
del bucle** (se repaga SYSTEM + menú de 5 herramientas + historial) para preguntar
lo mismo. Un bucle dentro de la función cuesta **$0.00**. Es el mismo precio que
él ya aceptó a conciencia con `"usd"` en minúscula.

Su razón **no se descartó, se afiló** — la regla quedó así:

> **Reintenta donde sea más barato. Que el modelo decida solo lo que necesita
> criterio.** Falla mecánica (red, timeout, 503) → reintenta la función, gratis.
> Falla con juicio (es domingo y no hay TRM, la moneda no existe) → `{"error"}`
> y decide el modelo. Es lo que hace el SDK, que él ya midió: con 401 **no
> reintentó ni una vez**.

⚠️ **Antes había contestado "un mensaje de no conexión y que lo seguirá
intentando".** La primera mitad, perfecta. La segunda escondía **su propio
defecto de la sesión 11**: si el mensaje promete reintentos y la función ya
terminó, **el mensaje miente** — igual que el *"solo letras y números"* de
`guardar_reporte`. Se le señaló con su propia lección.

### `HTTPError` es HIJO de `URLError`: el orden de dos líneas decide todo

Se le demostró **corriéndolo** contra un 404 real, con las dos versiones:

```
padre primero : PASAJERO -> reintentaria 3 veces  (HTTPError)
hijo primero  : PERMANENTE -> corta de una  (codigo 404)
```

Detalle que más enseñó: en la versión mala `type(e).__name__` **dice `HTTPError`**
y trae el 404 adentro. → **La excepción no te mintió; tú no preguntaste bien.**
**Es la imagen en espejo de L4.x del nivel 4** (*"el caso general atrapa hijos que
no sabías que existían"*, `APITimeoutError` hija de `APIConnectionError`): allá la
herencia **ayudaba** porque querías tratarlos igual; aquí **traiciona** porque los
quieres tratar distinto. **Regla: cuando dos excepciones son familia y las tratas
distinto, el hijo va primero.**

### La corrida de `pedir_json` — 7 casos, $0.00, sin Claude

| Caso | Tiempo | Resultado |
|---|---|---|
| 1. feliz: mercado | 0.32s | datos OK |
| 2. feliz: TRM (con `%20`) | 0.52s | datos OK, `valor 3206.18` |
| 3. permanente: 404 | **0.54s** | `error HTTP 404` |
| 4. pasajero: host inexistente | **3.11s** | `URLError` tras 3 intentos |
| 5. pasajero: `timeout=0.001` | 3.27s | `URLError` |
| 6. borde: `intentos=0` | 0.00s | mensaje, **no `NameError`** |
| 7. espacio en la URL | — | **REVENTÓ** con `InvalidURL` ✅ |

Lo que hay que conservar de esta tabla:

1. **El par 3 vs 4 (0.54s vs 3.11s) PRUEBA que el permanente no reintenta.** No
   se supone: se mide. De los 3.11s, **3 son puro `sleep`** (1s + 2s). Es su
   técnica del nivel 4 (`max_retries=5` con 401 = 0.39s vs 3 reintentos = 3.00s)
   aplicada a su propio código. → **Un número solo significa algo al lado de otro.**
2. **Caso 5: `timeout=0.001` tardó 3.27s.** El timeout limita **cada intento**,
   no el total; las esperas se suman aparte. Tercera confirmación de que
   `timeout` × `intentos` se multiplican.
3. **Inicializar `ultimo` antes del `for` se ganó el sueldo en la primera
   corrida** (caso 6). Era un defecto de MI esqueleto: con `intentos=0` el `for`
   no da vueltas y el `return` final usaba una variable que nunca nació.

⚠️ **HALLAZGO INCÓMODO SIN RESOLVER: `TimeoutError` nunca disparó.** El caso 5 se
diseñó para provocarlo y salió `URLError` — `urllib` envuelve el vencimiento de
tiempo **al conectar**. Nuestro `except` lo menciona sin prueba de que atrape algo:
**es el freno 3 de `guardar_reporte()` otra vez.** Sospecha *no medida* (se le dijo
que era sospecha): saldría pelado si el tiempo se vence **leyendo** la respuesta,
no conectando. → **Pendiente medible**, como los 278.916 nombres.

⚠️ **Formato: esta pieza fue DICTADA.** Se le dio el esqueleto con 3 huecos para
que llenara los 2 primeros y pidió *"amgio escribelo, muestralo y explicalo"*. Se
dictó y **queda anotado** para no perder la cuenta de qué código pasó por su cabeza.
Antes pidió *"escribeme un ejemplo primero"* (tercera vez que usa esa muletilla, y
funciona): se le dio sobre **otra** función desechable (`leer_config`, con
`FileNotFoundError` permanente vs `PermissionError` pasajero, las dos hijas de
`OSError`) **diciendo explícitamente que no va en su archivo** — la advertencia que
faltó con `doblar` en la sesión 11. Se le dejó un `SyntaxError` a propósito en el
ejemplo (el mismo suyo de la sesión 11: coma en vez de dos puntos).

### `tasa()` — escrita y probada (8 casos + 12 pares, $0.00 de Claude)

**Dictada** (pidió *"escribelo y despues me explicas paso a paso"*). Se le avisó
que era la 2ª pieza seguida dictada y **se le ofreció un trato: `tasa` dictada,
`trm` la escribe él.** Aún no lo confirma.

**El concepto del día: la triangulación.** La API entrega TODO contra el dólar
(`base_code = "USD"`), 166 monedas. Un par como EUR→COP **no existe en el JSON**.

```
tasa(de, a) = rates[a] / rates[de]
```

Verificado numéricamente por los dos caminos: paso a paso (1/0.875576 = 1.1421
USD, × 3207.637776) da `3663.460140524637`; la fórmula da `3663.4601405246376`.
Iguales hasta el decimal 12 (la diferencia es `float` — la deuda de `Decimal`).
**Regalo:** como `rates["USD"] = 1`, la misma fórmula cubre los 12 pares **sin
un `if` especial para el dólar**. `USD→USD` dio `1.0` en la corrida.

**El recorte, y él dio la razón correcta antes de que se la dijera:** se le
preguntó qué devolver y contestó *"algo mas pequeño, solo la tasa, porque se
reenvia en cada vuelta"* — o sea aplicó solo su medición del nivel 3 (los
`tool_result` de 18/20/46 tokens). **2.967 caracteres → ~130. Unas 22x.**
→ **Lo que devuelve una herramienta no se paga una vez: se paga en cada vuelta
que le quede a la conversación. Un `tool_result` gordo es un impuesto permanente.**

⚠️ **Se le afinó "solo la tasa":** se conserva `time_last_update_utc` porque **sí
se gana sus tokens**. Mercado y TRM dan números distintos para el mismo día
(3207,64 vs 3206,18), así que una tasa sin fecha ni fuente es **correcta e
inútil a la vez** — y es la rúbrica "¿citó la fuente?" del paso 10.
→ **La regla no es "devuelve lo mínimo", es "devuelve lo que se gana sus tokens".**

**Lo nuevo estructural: hay un SEGUNDO desconocido.** Hasta hoy se desconfiaba
solo del modelo. Ahora el dato lo manda **un servidor ajeno**, que puede cambiar
de formato, quitar una moneda o mandar `null` sin avisar. Por eso `tasa` tiene
frenos **sobre la respuesta**, no solo sobre los argumentos.
- `rates.get(de)` + `es_numero()` → **un solo freno cubre tres desastres**
  (llave ausente, `null`, texto). Reusa el `es_numero()` que él escribió.
- `if valor_de <= 0` evita `ZeroDivisionError`. Es su propio `tasa <= 0` de
  `convertir()`, pero apuntando al servidor en vez de al modelo.

⚠️ **LA TRAMPA DEL REDONDEO (se le dijo "no redondees, quiero que la veas").**
`COP→USD` dio `0.0003117558994603884`. Redondear la tasa a 2 decimales "para que
no sea tan larga" da **`0.0`**, y entonces su propio freno `tasa <= 0` la
rechazaría: la herramienta correcta destruida por un cambio cosmético.
→ **`DECIMALES` redondea el RESULTADO en dinero, nunca la TASA.** Son dos números
con precisiones distintas: uno es plata que alguien paga, el otro es un factor.

⚠️ **Decisión mía, revocable:** `USD→USD` se acepta y devuelve `1.0`, gastando una
llamada de red para averiguar que un dólar es un dólar. Se podría cortar con
`if de == a`. Se dejó simple a propósito. Mismo patrón que `monto cero`.

### 🐛 HALLAZGO GRANDE DEL DÍA: las 3 funciones incumplían el contrato

Salió de una corazonada al ver que `tasa(123, "COP")` se rechazaba bien. **Seis
funerales**, comprobados corriéndolos:

```
convertir       de=[]        -> TypeError: unhashable type: 'list'
convertir       a={}         -> TypeError: unhashable type: 'dict'
guardar_reporte nombre=[]    -> AttributeError: 'list' has no attribute 'endswith'
guardar_reporte nombre=5     -> AttributeError: 'int' has no attribute 'endswith'
guardar_reporte contenido=None -> TypeError: data must be str, not NoneType
tasa            de=[]        -> TypeError: unhashable type: 'list'
```

**La causa:** `x in un_diccionario` funciona con cualquier valor **hashable**
(números, texto, `None`, booleanos), así que la prueba de pertenencia hacía **de
paso** un control de tipo. Con una lista Python no dice "no está": dice
`TypeError`. **Funcionaba por casualidad, y la casualidad tenía un borde.**

⚠️⚠️ **LO IMPORTANTE NO ES EL BUG: `evals.py` tenía 26 casos, 0 fallos, y NO VE
NINGUNO DE LOS SEIS.** Es la segunda prueba —y más filosa que la del banker's
rounding— de la lección que ya estaba anotada: *el eval no dice "tu código está
bien"; dice "estas 26 cosas se comportan como dijiste"*. **Los 26 en verde
mientras el contrato del archivo estaba roto en tres sitios.**
→ **Candidata a LECCIÓN FUERTE del 5b, junto con la del hueco 3.**
Y no es un caso raro: el modelo manda **JSON**, donde una lista se escribe igual
de fácil que un número. Es `monto="10"` otra vez.

**El arreglo: lo decidió él, opción B.** Se le dieron A (un `if` en cada función)
y B (ayudante compartido) y contestó *"B, porque una regla en un solo sitio"* —
consistente con sus dos precedentes (`es_numero`, `MONEDAS = tuple(DECIMALES)`).
Se implementaron **dos** ayudantes porque son dos reglas, y el segundo se
construye sobre el primero:
- `es_texto(x)` → `isinstance(x, str)`. Lo usa `guardar_reporte` (nombre y contenido).
- `es_moneda(x)` → `es_texto(x) and x in DECIMALES`. Lo usan `convertir` y `tasa`
  (4 sitios). **Junta las dos preguntas** que antes estaban implícitas en una.
- En `guardar_reporte` el nuevo bloque es el **freno 0** y va **antes** de todo:
  los frenos 1 y 2 usan métodos de texto, y un método de texto sobre una lista
  no devuelve `False`, **lanza**. Mismo orden forma→contenido de `convertir()`.
- Los mensajes dicen **"entre comillas"**: es el **espejo** del *"sin comillas"*
  de los frenos numéricos. Al modelo hay que decirle la FORMA del JSON.

**Verificado:** `9 casos, 0 funerales` · `evals.py` sigue en `26 casos, 0 fallaron`.

### ✅ Y una decisión suya de la sesión 11 que se pagó HOY

Se reescribió la **redacción de 4 mensajes de error** de sus dos funciones y **no
se rompió ni uno de los 26 casos**. Pudo pasar porque en el paso 5 él decidió que
el eval compara `"error"` contra un número y **nunca el texto del mensaje**
(*"si comparas el texto, mejorar el mensaje rompe la prueba"*).
→ **Una prueba bien diseñada te deja mejorar el código; una mal diseñada te lo
congela.** Vale la pena decírselo: fue su decisión y le pagó una sesión después.

### ✅ `evals.py` AMPLIADO: **35 casos, 0 fallos**, $0.00 y sin red (DEMOSTRADO)

**Dictado** (pidió *"trabja en lso nueve casos, llevalso a evals.py"*). Tercera
pieza seguida dictada — **ver la deuda de formato al final de esta sección.**

**La decisión de diseño se resolvió sola: 7 de los 9 casos entraron en sus dos
listas existentes** sin tocar el bucle; solo se agregaron filas. Solo `tasa`
necesitó lista y bucle nuevos.
→ **Las pruebas se agrupan por la función que prueban, no por el bug que las
descubrió.** La tentación era una lista "casos del contrato": habría repartido
las pruebas de `guardar_reporte` por fecha de descubrimiento en vez de por función.

### 🪤 LA PIEZA NUEVA: la TRAMPA DE RED

El archivo prometía en su docstring *"no usa internet y cuesta $0.00"*. Meter
`tasa` ponía eso en riesgo. El razonamiento era: sus casos son todos de RECHAZO y
los frenos de moneda van ANTES de pedir el dato, así que mueren sin salir de la
máquina. **Pero eso era un razonamiento, no una prueba** (su lección del freno 3).

```python
def trampa_de_red(*args, **kwargs):
    raise AssertionError("un caso llego a la red: este eval debe costar $0.00")
herramientas.pedir_json = trampa_de_red
```

→ Antes: *"creo que no toca la red"*. Ahora: **"si toca la red, se ve"**.
Es **su técnica del sabotaje al revés**: con el `write_text` comentado rompió **el
código** para ver si la prueba lo notaba; aquí se rompe **el camino prohibido**
para ver si alguien lo pisa.

⚠️ **El camino feliz de `tasa` NO cabe en `evals.py` y está dicho en el archivo:**
no se puede exigir un número fijo a una tasa que cambia a diario ni depender de
que el servidor esté vivo. Eso es de los pasos 9 y 10. **Aquí solo rechazos.**

### Los DOS sabotajes que comprueban que todo esto sirve

**A — la trampa:** con la trampa puesta se pidió `tasa("USD","COP")` (camino
feliz, necesita red) → **saltó `AssertionError`** ✅. Y `tasa([],"COP")` pasó
tranquilo sin saltar ✅. Los dos comportamientos buscados.

**B — los 9 casos nuevos:** se rompieron `es_moneda` y `es_texto` para que
**siempre devolvieran `True`** y se corrió el eval → **`35 casos, 12 fallaron`**
(los 9 nuevos + 3 viejos que también dependen de `es_moneda`). Archivo restaurado
y verificado de vuelta en 35/0. **Los casos nuevos no son adorno.**

⚠️⚠️ **EL HALLAZGO QUE DA MIEDO, del sabotaje B:**

```
FALLA moneda lista    esperado='error'    obtenido=39000
```

Con el freno roto, `convertir(10, [], "COP", 3900)` **devolvió 39000**. Convertir
10 de *lista vacía* a pesos entregó **una cantidad de dinero perfectamente
creíble**. Es idéntico a `monto=True → 3900`.
→ **Un error que revienta te avisa; un error que devuelve un número creíble no.**
Es la categoría más peligrosa del proyecto. **Candidata a lección fuerte.**

**Y aquí se ve el valor concreto de su respuesta "B":** un sabotaje de **dos
líneas** puso rojos **12 casos en 3 funciones**. Si la regla vive en un sitio,
romperla se ve en todas partes.

**Regalo no buscado:** en el sabotaje B la sección de `tasa` dio
`REVENTO: AssertionError` — **la trampa de red disparó**, porque con el freno roto
`tasa([],"COP")` sí llegó a buscar internet. La trampa hace **dos** trabajos:
documenta que el eval es gratis **y detecta un freno roto** por la puerta de atrás.

### ⚠️ DECISIÓN PENDIENTE PARA ÉL (anotada en el código, no resuelta)

El tercer bucle es **casi idéntico** al de `convertir`: solo cambian la función
llamada y la llave del resultado (`"resultado"` vs `"tasa"`). Con
`guardar_reporte` el bucle aparte SÍ estaba justificado (revisa el disco, es otro
trabajo); aquí no. **Su propio argumento *"una regla en un solo sitio"* ahora
apunta al otro lado.** Se dejó separado para no tocar el bucle que escribió él.
Las dos respuestas son defendibles y la decisión es suya.

### ⚠️⚠️ DEUDA DE FORMATO — HAY QUE ATAJARLA LA PRÓXIMA SESIÓN

**Tres piezas seguidas dictadas** en la sesión 12: `pedir_json`, `tasa` y la
ampliación de `evals.py`. Todas las pidió él (*"escribelo"*, *"trabja en los nueve
casos"*), se le avisó y se le ofreció un trato explícito (**`tasa` dictada, `trm`
la escribe él**) que **no confirmó**. El README del nivel dice por qué importa:
*"si se le dicta todo, termina con un agente que funciona y que no sabría
rehacer — sería el único nivel donde el código no pasó por su cabeza."*
→ **`trm` debería escribirla él**, con `tasa` delante como modelo (son casi la
misma forma). Si vuelve a pedir dictado, dictarlo — es su curso —, pero **decirlo
una vez más y seguir contando**. Lo que sí funciona y hay que conservar: darle un
esqueleto con **huecos numerados** y un ejemplo sobre **otra** función desechable.

### ✅ `tasa()` CERRADA BIEN: `evals.py` en **45 casos, 0 fallos**, $0.00 y sin red

Él eligió la opción **A** ("cerrar `tasa` bien") sobre la B ("seguir y anotarlo"),
después de que se le dijera qué le faltaba de verdad a la función. Preguntó
*"¿la función tasa ya está totalmente implementada?"* y **la respuesta honesta era
NO**: la lógica funcionaba, pero **3 de sus 5 caminos jamás se habían ejecutado**
(los dos frenos sobre la respuesta del servidor y el camino de error de red).
Escritos, legibles, y sin correr una sola vez — podían tener un typo.

### 🎭 LA PIEZA NUEVA: el DOBLE (servidor de mentira)

Sale de la trampa de red: **si se puede reemplazar `pedir_json` por uno que
revienta, se puede reemplazar por uno que finge ser un servidor con problemas.**

```python
def servidor_falso(respuesta):
    def falso(url, **kwargs):
        return respuesta
    return falso
```

10 casos nuevos (`CASOS_TASA_FUENTE`), cada uno con la respuesta falsa que
`pedir_json` va a devolver, en su misma forma `(datos, error)`: sin llave `rates`,
moneda ausente, `null`, valor de texto, divisor cero, divisor negativo, error de
red, y **tres felices**.

### ⭐ EL HALLAZGO CONCEPTUAL DEL PASO — corrige una nota del propio plan

El plan del nivel decía que estas tres herramientas *"no se pueden probar como las
otras dos, dependen de un servidor ajeno"*. **Resultó medio falso: lo que estaba
mal era la pregunta.** Había DOS metidas en una:

| Pregunta | ¿Necesita internet? |
|---|---|
| ¿Mi aritmética está bien? ¿Los frenos atrapan? | ❌ **No.** Los datos los pongo yo |
| ¿El servidor sigue vivo y con el mismo formato? | ✅ Sí, sin remedio |

→ **No es que una herramienta de red no se pueda probar: es que hay que separar
"¿mi código está bien?" de "¿el mundo está como creo?".** La primera se prueba en
tu máquina siempre; la segunda nunca. **Candidata a lección fuerte del 5b.**

**Y el camino feliz SÍ cabe, determinista:** con `1 EUR = 2 USD` y
`1 USD = 4000 COP`, la triangulación **tiene que** dar 8000 y se verifica a ojo.
Con la fuente real era imposible: la tasa cambia a diario, no hay esperado fijo.
```
feliz USD->COP    esperado=4000.0    obtenido=4000.0
feliz EUR->COP    esperado=8000.0    obtenido=8000.0
```

### El sabotaje, con PREDICCIÓN ACERTADA (y la cuenta se lleva en los dos sentidos)

Se predijo por escrito **antes de correr**: *"6 FALLA, cinco reventones y uno que
devuelve un número creíble: `divisor negativo` daría `-4000.0`"*. **Salió exacto.**

```
FALLA sin llave rates   -> REVENTO: TypeError
FALLA moneda ausente    -> REVENTO: TypeError
FALLA valor null        -> REVENTO: TypeError
FALLA valor texto       -> REVENTO: TypeError
FALLA divisor cero      -> REVENTO: ZeroDivisionError
FALLA divisor negativo  -> -4000.0
45 casos, 6 fallaron
```

⚠️ **Tercera aparición HOY del mismo patrón:** con el freno apagado, la tasa
negativa **no revienta**, devuelve `-4000.0`. Menos creíble que el `39000` porque
el signo canta, pero **el agente lo reportaría como respuesta, no como falla**.
(Los tres del día: `monto=True → 3900`, `moneda=[] → 39000`, `tasa<0 → -4000.0`.)

### Dos detalles del código, dichos en la explicación

1. **`servidor_falso` es una función que fabrica funciones**, no un `lambda` en el
   bucle: un `lambda` ahí se acordaría de la **última** respuesta del bucle, no de
   la de su caso. Trampa clásica de Python, evitada a propósito.
2. **`4000 / 1` da `4000.0`, no `4000`** — en Python 3 `/` siempre devuelve float.
   Por eso el esperado es `4000.0`. **Lo detectó su comparación estricta de tipos**,
   la que endureció en el paso 5 tras el `4.0 == 4`. **Segunda vez que le paga.**

### ⚠️ EL LÍMITE DEL DOBLE, dicho explícitamente (patrón de la casa)

**Un doble prueba tu código contra TUS SUPOSICIONES sobre el servidor, no contra
el servidor.** El nuestro asume que el mercado manda números; si mañana manda
texto, los 10 casos siguen verdes y el agente se rompe en producción. Por eso el
caso `valor texto` existe (es el formato real de datos.gov.co: `"3206.18"`) y por
eso en el paso 9 hace falta **una** corrida contra las fuentes de verdad.
Mismo espíritu que *"el eval no puede demostrar que no escribió fuera de caja/"*.

### Lo que a `tasa()` le sigue faltando (y no es código)

1. Una corrida real contra la fuente viva → **paso 9**.
2. `USD→USD` gasta una llamada de red para saber que un dólar es un dólar
   (decisión mía, revocable, sin resolver).
3. **El modelo todavía no sabe que existe:** falta describirla en la lista `tools`
   → **paso 7**.

### ✅ `trm()` — escrita, probada (16 casos) y corrida contra la fuente real

**Dictada** (pidió *"armala y despues cierra la sesion"*). Cuarta seguida — la
deuda de formato de más abajo sigue viva y **es lo primero de la próxima sesión**.

⚠️ **CAMBIO DE DISEÑO, y lo corregí sobre mi propia propuesta:** yo había dicho
`trm(dias=1)`. **Va SIN parámetro.** Si `trm` supiera traer varios días haría a
medias el trabajo de `historial`, y **dos herramientas que se pisan obligan al
modelo a elegir entre dos caminos para lo mismo.** `trm()` = la más reciente;
`historial(dias)` = la serie. Una cosa cada una.

**Las tres cosas nuevas de `trm`, y las tres dieron material:**

1. **La fuente devuelve una LISTA de filas**, no un diccionario como la de
   mercado. → **Dos fuentes, dos formas: cada herramienta conoce la suya.** Sin
   el freno, `datos[0]` sobre una lista vacía es un funeral.
2. **`valor` viene como TEXTO** (`"valor":"3206.18"`, con comillas en el JSON).
   Van **dos frenos porque son dos preguntas**, igual que en `convertir()`:
   - **FORMA** (`es_texto` o `es_numero`) → descarta `None`, listas, dicts y
     booleanos.
   - **CONTENIDO** (`try: float(...) except ValueError`) → descarta `"abc"`, `""`
     y ⚠️ **`"3.206,18"`**, que es **cómo se escribe la plata en Colombia**:
     coma decimal y punto de miles. `float()` lo rechaza. Es el caso más
     realista de la lista y está escrito como prueba.
3. **EL DOMINGO — resuelto con su propia regla.** `trm()` **no decide**: devuelve
   `vigente_desde` y `vigente_hasta` bien visibles y **la decisión sube al
   modelo** (usar la del viernes y avisar, o decir que espere). El caso de prueba
   **no se inventó**: la TRM del viernes 24 vigente hasta el domingo 26.
   → Primera vez en el curso que la regla *"que el modelo decida solo lo que
   necesita criterio"* se aplica **al diseño de una herramienta**, no a un error.

⚠️ **Decisión de diseño con razón que no hay que perder: `trm()` NO calcula
"¿es de hoy?".** Para eso tendría que mirar el reloj, y entonces dependería de
**dos mundos** (la fuente y la hora de la máquina) y **dejaría de ser probable con
datos fijos** — el eval no podría afirmar nada estable. Si el agente necesita la
fecha de hoy, **eso es otra herramienta**, como `hora_utc` en el nivel 3.
→ **Una función que mira el reloj deja de ser determinista, y con eso se pierde
la única forma barata de probarla.**

**Los 16 casos** (`CASOS_TRM`) van **todos** con servidor de mentira: `trm()` no
recibe argumentos, así que **no hay nada que rechazar antes de salir a la red**.
Sin el doble, esta función no se podía probar en absoluto.

✅ **LA CORRIDA REAL (la que el doble no puede reemplazar), 2026-07-30:**

```
trm()   -> 3206.18   vigente_desde/hasta = 2026-07-30   (llegó como texto, salió número)
tasa()  -> 3207.637776                                   brecha = 1.46 pesos
```

La brecha coincide con la medida al empezar la sesión. **Las dos fuentes vivas y
con el formato que suponíamos** — que es exactamente lo único que el doble no
podía decirnos.

---

## Cierre de la sesión 12

**Lo que se hizo:** paso 6 al 75%. `pedir_json` + `tasa` + `trm`, las tres
probadas. `evals.py` pasó de **26 a 61 casos**, sigue en **0 fallos**, **$0.00** y
**sin red demostrado** (la trampa). Un defecto real corregido en el README.
El contrato del archivo reparado en las 3 funciones que lo incumplían.

**Los 4 sabotajes de la sesión** (la técnica que más rindió): la trampa de red,
`es_moneda`/`es_texto` siempre True (12 rojos), y los dos frenos de `tasa` sobre
la respuesta del servidor (6 rojos, **con predicción acertada**). Ninguna prueba
de hoy se dio por buena sin verla ponerse roja primero.

**⚠️ `LESSONS.md` NO se tocó, y es correcto:** su regla es **un bloque por nivel**,
al cerrar el nivel. Las candidatas a lección fuerte del 5b están acumuladas en
esta bitácora y son ya **seis**: (1) el hueco 3 / no tapes tus propios bugs,
(2) los 26 verdes con el contrato roto, (3) el número creíble es peor que el
reventón, (4) separar "¿mi código está bien?" de "¿el mundo está como creo?",
(5) el doble prueba tus suposiciones, no el servidor, (6) el `tool_result` es un
impuesto permanente. **Al cerrar el nivel 5b hay que escribirlas.**

**Dudas suyas de hoy:** una sola, y muy buena — *"¿la función `tasa` ya está
totalmente implementada?"*. **Preguntó justo cuando yo iba a seguir de largo**, y
de ahí salió todo el trabajo del doble. Vale la pena decírselo: esa pregunta
cambió el rumbo de la sesión para bien.

---

## Histórico del paso 6: notas previas

**Lo que decía antes este bloque: `trm(dias=1)`** — la TRM oficial de datos.gov.co, con
`URL_TRM` (ya en el archivo, con el `%20`). Sus problemas propios, y son nuevos:
1. **El domingo no hay TRM nueva.** Aquí SÍ manda su razón (*"el modelo decide si
   vale la pena"*): usar la del viernes y avisar que es del viernes, o decir que
   espere, **necesita criterio** → `{"error"}` o un dict con la fecha bien visible.
   El dato lo trae la fuente: `vigenciadesde`/`vigenciahasta` (la del 25 de julio
   valió hasta el 27). **El caso de prueba no hay que inventarlo.**
2. **`valor` viene como TEXTO** (`"3206.18"`, con comillas en el JSON). Hay que
   convertirlo, y esa conversión puede fallar → otro freno sobre la respuesta.
3. Después `historial`: **recortar el JSON de 30 días ANTES de devolverlo**.

---

## Histórico: paso 5 (sesión 11)

**SIGUIENTE PASO (ya cumplido en la sesión 12): paso 6 — las 3 herramientas que SÍ tocan la red**
(`tasa`, `trm`, `historial`), formato **mixto**. Las 2 URLs están verificadas en
`05b-proyecto/README.md` §5b.4 (HTTP 200 el 2026-07-29) — ⚠️ **volver a
comprobarlas**, ya pasaron varios días. Aquí aparecen problemas nuevos que las dos
primeras herramientas no tenían: el domingo sin TRM, el JSON de 30 días que se
reenvía en cada vuelta (recortar la salida ANTES de devolverla), y que **estas
tres no se pueden probar como las otras dos** — dependen de un servidor ajeno.

### Las dos decisiones abiertas: CERRADAS (las dos se rechazan)

Lo decidió él: `"10"` como texto **no** se convierte a número, y `"usd"` **no** se
pasa a mayúsculas. ⚠️ **Se le dijo lo que cuesta la segunda y hay que medirlo en el
paso 9:** cada minúscula gasta **una vuelta extra del bucle** (manda `"usd"`, lee el
error, reintenta con `"USD"`) = 2 llamadas a la API en vez de 1. Con `.upper()`
habría sido gratis. Si aparece mucho en `registro.jsonl`, se revisa **con datos**.

### Los arreglos a `convertir()` (los pidió dictados: *"realiza los cambios directamente"*)

Se aplicaron **de uno en uno, corriendo `evals.py` después de cada uno**: 8 fallos
→ 4 → (se agregan los booleanos) 6 → 4 → **0**. El orden fue de lo más grave a lo
más pequeño: primero lo que tumba el bucle, de último lo cosmético.

1. **Frenos de FORMA vs frenos de CONTENIDO**, agrupados y rotulados. Los de tipo
   van primero porque si el dato no es número la función no puede hacer *nada*;
   los de moneda son sobre el significado. Dos `if` separados (uno por parámetro)
   para que el mensaje **nombre al culpable** — con uno solo, el modelo reintenta
   a ciegas. Los mensajes dicen el tipo que llegó (`type(x).__name__`) y traen
   ejemplo **"sin comillas"**, que es lo que de verdad corrige el `"10"`.
2. ✅ **Los booleanos: los pidió él** (*"agrega también el caso de los booleanos"*),
   después de que se le señalara el hueco. **Primero se vieron fallar:**
   `monto=True` → **3900** y `tasa=True` → **10**, o sea una cantidad de dinero
   creíble. `isinstance(True, int)` es `True` porque en Python `True` vale 1.
   → Se sacó a un ayudante `es_numero(x)` en vez de repetir la condición:
   **una regla, un sitio.** Mismo motivo que `MONEDAS = tuple(DECIMALES)`.
   `es_numero` va en un bloque rotulado como **ayudante interno, no herramienta**
   (el modelo nunca la llama, no entra en `tools`) — distinción que importa en el paso 7.
3. **`monto < 0`** rechaza; **el cero se acepta** y devuelve 0. Esa decisión llevaba
   colgando desde la pregunta *"¿monto=0 es accidente o es válido?"*, que nunca se
   contestó: **la tomé yo y se le dijo que era mía y revocable.** Se escribió como
   **caso de prueba** (`("monto cero", ..., 0)`) → *un caso de prueba es la forma
   más duradera de escribir una decisión: un comentario se ignora, un caso rojo no.*
4. **`tasa <= 0`** en un solo `if`: tasa cero y negativa son **la misma idea** (una
   tasa siempre es positiva). ⚠️ **La asimetría `monto < 0` vs `tasa <= 0` parece
   un descuido y no lo es** — está anotada en el código: la forma del `if` sale del
   mundo real, no de la simetría. Aquí murió el fallo más silencioso de la función
   (tasa 0 devolvía `0`, y un `0` se ve legítimo).
5. **El `round`:** `round(3.7, 0)` → `4.0` (decimal) pero `round(3.7)` → `4`
   (entero). **No son la misma llamada.** Por eso hay un `if decimales == 0`.

### ⚠️ DEFECTO CONOCIDO, SIN ARREGLAR: banker's rounding

Con los 16 casos en verde, se le mostró que **verde no significa correcto**:

```
0.5 -> 0    1.5 -> 2    2.5 -> 2    3.5 -> 4    4.5 -> 4
```

Python redondea **al par más cercano** cuando el número cae justo en la mitad
(para no sesgar sumas grandes hacia arriba). Para estadística está bien; **para
dinero la norma contable suele ser "medio para arriba"**. Los 16 casos no lo
detectan porque **ninguno cae en `.5`** — el eval contesta exactamente las 16
preguntas que se le hicieron y nada más.

→ **Ejercicio del nivel:** agregar los casos `.5`, verlos fallar, y arreglarlo con
**`Decimal`** (el tipo que Python trae para dinero) en vez de `float`. No es un
`if`, es un tema entero — por eso se dejó anotado y no hecho.

→ Candidata a lección fuerte: *el eval no dice "tu código está bien"; dice "estas
16 cosas se comportan como dijiste". Todo lo demás sigue sin explorar.*

### Los 10 casos de `guardar_reporte` — el problema nuevo: el EFECTO SECUNDARIO

`convertir()` es pura: solo devuelve, así que revisar lo devuelto es revisar todo.
`guardar_reporte()` **cambia el mundo**, y lo que devuelve es apenas un recibo.
Se le mostró con un experimento mental: si alguien comenta el `write_text`, la
función **devuelve exactamente lo mismo** y no guarda nada. Es L4.9 del otro lado —
allá el agente decía *"ya lo borré"* con el archivo intacto; aquí es **la prueba**
la que dice *"ya lo guardó"*.

**Las tres respuestas se las dio él, una por pregunta** (la regla de una pregunta a
la vez funcionó otra vez):

1. *"que el archivo estuviera en la ruta"* → hay que comprobar que **existe**.
2. *"que el contenido sea el que se le pasó"* → y que **coincida** (podría crearlo
   vacío, o escribirlo dos veces).
3. Se le mostró que `caja/reporte-trm-2026-07-30.txt` **seguía vivo desde la
   mañana**, así que "el archivo existe" pasaría aunque la función ya no escribiera.
   Contestó: *"borrar el archivo antes de la prueba o marcarlo como no actual"*.
   → La primera es la estándar; la segunda (comparar la fecha) depende del reloj y
   de la precisión del sistema de archivos: más frágil por más trabajo.
   **Nombre del concepto que se le dio: la prueba arranca de un ESTADO CONOCIDO.**
   No "probablemente vacío": vacío porque tú lo vaciaste.

**Cómo quedó implementado:**
- `limpiar_caja()` corre **antes de cada caso**, no una vez al principio → **cada
  caso independiente de los demás.** Si el orden importa, son 10 casos encadenados,
  no 10 pruebas. Solo borra dentro de `caja/`, nunca sube.
- El veredicto tiene **dos mitades**: `ok = (obtenido == esperado) and (pero == "")`.
  `obtenido` = ¿dijo lo correcto? · `pero` = ¿el disco quedó como debe? El texto
  del `pero` se imprime, así que al fallar se ve **cuál** mitad se rompió.
- **Bucle aparte**, no un `if` dentro del primero: dos trabajos distintos, dos
  bucles. Con banderas quedaba ilegible.
- Los 7 casos que esperan `error` comprueban además que **`caja/` quedó vacía** —
  una función podría escribir y *después* devolver error, que es peor que no validar.
- `limpiar_caja()` también al final: el eval no deja basura (verificado: 0 archivos).

✅ **SE COMPROBÓ QUE LAS PRUEBAS SIRVEN, con sabotaje.** Se comentó el
`write_text` a propósito y salieron **3 FALLA** con el mensaje
`esperado='guardado' obtenido='guardado' PERO NO HAY ARCHIVO` — o sea las dos
primeras columnas **coincidían** y lo atrapó solo la revisión del disco. Se
restauró la línea y volvió a 26/0. Es la técnica del nivel 3 (ejercicios de
sabotaje) aplicada a un eval.

⚠️ **Límite conocido de este eval, dicho explícitamente:** comprueba que no
escribió *dentro* de `caja/`, pero **no puede demostrar que no escribió fuera**.
Si `../../.env` pasara los frenos, el archivo caería en la raíz y el eval no lo
vería. Para eso se confía en los 3 frenos + la prueba de fuerza bruta de 278.916
nombres. **La prueba es parcial, y saber dónde acaba es parte de tenerla.**

**Decisión nueva del día (mía, revocable, escrita como caso):** contenido vacío
**se acepta** — un reporte sin datos es raro pero no es un error de formato. Mismo
patrón que `monto cero`.


El nivel 5 quedó cerrado en la sesión 9 (detalle más abajo). La sesión 10 arrancó
el 5b: se creó `05b-proyecto/`, se escribió el `README.md` del nivel completo
(§5b.0 a §5b.5, con **el plan de los 10 pasos y quién escribe cada uno**), y
**él escribió `convertir()` entera** — la primera función del curso que sale de su
cabeza y no de un dictado. La sesión 11 cerró el paso 4 con `guardar_reporte()`,
**también escrita por él**.

**Estado de los archivos del 5b:**

| Archivo | Estado |
|---|---|
| `README.md` | ✅ completo hasta §5b.5 (Ejercicios y "Lo que ya sabes" vacíos a propósito) |
| `herramientas.py` | ✅ las 2 que no tocan internet (`convertir`, `guardar_reporte`) + el ayudante `es_numero`. Faltan las 3 de red |
| `evals.py` | ✅ 26 casos (16 de `convertir` + 10 de `guardar_reporte`), 2 bucles, **0 fallos** |
| `agente.py` | ⬜ vacío (0 bytes) |

### Paso 5 — `evals.py` (sesión 11)

**Lo escribió él: los casos, el bucle y la tabla.** El diseño quedó así: cada caso
es **un dato de tres partes** `(etiqueta, argumentos, esperado)`, y `esperado` es
un número (se compara contra `r["resultado"]`) o el texto `"error"` (solo importa
QUE rechace, **nunca la redacción** del mensaje — si comparas el texto, mejorar el
mensaje rompe la prueba). Un bucle recorre todo y cuenta.

**Cómo salieron los casos, y esto es lo que hay que conservar del método:** se le
enseñaron las **tres familias** (camino feliz / bordes / lo malo) y se le dijo que
la familia que todo el mundo se salta es la de **los bordes**. Los propuso él.

- ⚠️ **Confusión suya que hay que recordar:** propuso *"valores negativos para
  `monto`, `de` y `a`"*. `de` y `a` son **texto** (nombres de moneda), no números.
  Se corrigió y de ahí salió que **el número que se le había pasado era `tasa`**.
- ✅ **Decisión de diseño suya:** monto negativo → **rechazar**, *"porque un monto
  negativo siempre es un accidente"*. Correcta y bien razonada (el modelo traduce
  lo que escribió un humano).
- ✅ **Segunda decisión suya, y la contestó completa: los DOS candados.** ¿Dónde se
  validan los no-números? *"Inicialmente A (la herramienta), pero además en el
  agente, o sea B"*. Es `guardar_reporte` otra vez. Se le añadió el argumento que
  decide el orden: **A se prueba por $0.00 y sin red; B necesita llamadas pagadas.**
- ⚠️ **Error suyo, el mismo que él me corrigió a mí en el nivel 1:** el caso
  `"tasa cero"` lo escribió con `monto=-100` (copiado del caso anterior) → **dos
  variables en un caso**. Ese caso habría pasado a verde al arreglar el monto, con
  la tasa cero **todavía rota**. Regla escrita en el archivo: **un caso, una
  variable.** (Lo corrigió solo antes de que lo revisáramos.)
- ⚠️ **No entendió que `doblar` era un ejemplo desechable** y preguntó cómo
  "convertirla" para el ejercicio. → **Al dar un ejemplo con función de mentira,
  decir explícitamente que no va en su archivo.** La técnica sirve (funcionó con
  `poner_apodo`), la advertencia faltaba.

#### Los 3 hallazgos de la corrida

1. **`4.0 == 4` es `True` en Python** — el `==` compara valor, no tipo. El caso
   `"redondeo a COP"` salía **en verde con el defecto puesto**. Se endureció la
   comparación a `(obtenido == esperado) and (type(obtenido) is type(esperado))`
   y pasó a FALLA. → **Una prueba en verde no dice que no haya problema; dice que
   tu comparación no lo ve.** Es *"una corrida limpia no prueba nada"* (nivel 5)
   un piso más abajo. Candidata a lección fuerte del 5b.
2. ⚠️ **PREDICCIÓN MÍA FALLADA:** dije "se esperan 8 FALLA" y salieron **7**,
   justo por lo de arriba. Se le planteó como pregunta antes de correr (*"¿4.0 == 4
   es verdadero?"*) y **la contestó bien**: "hay que preguntar si es entero". Con
   la comparación estricta salieron los 8. La predicción no se borró del archivo:
   se corrigió con la razón.
3. **El `try/except` se ganó el sueldo.** 4 de los 13 casos dan
   `REVENTO: TypeError` (`tasa=None`, `monto=""`, `monto="10"`, `monto=None`).
   Sin el `try`, el eval moría en el caso 5 y **nunca se veían los 8 siguientes**.
   Se anota el reventón **como si fuera un resultado más**, alineado en la tabla:
   reventar *es* un comportamiento. → *"una prueba que se cae con lo que estaba
   probando no es una prueba, es otra víctima"*.

#### El hallazgo conceptual más importante del día

**`convertir()` incumple el contrato que está escrito en su propio archivo**
(*"ninguna lanza excepciones"*). Y la razón de por qué importa, en sus términos:
**un `{"error": ...}` es una conversación; un `TypeError` es un funeral.** Con el
dict el modelo lee el error y reintenta; con la excepción se cae el bucle del
agente y con él la conversación. `monto="10"` no es un caso raro: el modelo manda
**JSON**, donde `10` y `"10"` son cosas distintas.

#### Reorganización de `herramientas.py` (pedida por él: *"que se vea más profesional"*)

Se hizo **y se volvió a correr la misma prueba antes y después** para comprobar que
no cambió comportamiento. Cambios: `import` juntos arriba (PEP 8), constantes en un
solo bloque, separadores de sección, docstrings en las dos funciones, frenos
numerados con su *por qué*, y el comentario que **salva el freno 3** (con el número
278.916). **Lo más valioso no fue código: fue escribir el CONTRATO** del archivo en
el docstring de arriba (*"todas devuelven dict; ninguna lanza excepciones"*). Sus
dos funciones ya lo cumplían, pero en ningún sitio decía que era una regla.
**No se pusieron anotaciones de tipo** a propósito: las conoce en el nivel 6 con
TypeScript, y aquí serían un tema nuevo a mitad de otro.

⚠️ **Regla de método confirmada dos veces hoy: UNA pregunta a la vez.** Tres
preguntas encadenadas no son tres veces más difíciles, son un muro. Cada vez que
se reformuló a una sola pregunta, la contestó bien de inmediato. También pide
**"escríbeme un ejemplo primero"** — dárselo sobre **otra** función funciona.

**Siguiente paso concreto: paso 5 — `evals.py`**, probando las dos funciones que
no tocan internet. **$0.00 y sin red.** Ese es el orden y tiene razón: si
`convertir()` está mal, saberlo antes de pagar llamadas. Buena parte del material
ya existe: en la sesión 11 se probó `guardar_reporte` a mano con 6 casos en un
archivo temporal. **El paso 5 es dejar eso escrito y repetible**, no inventarlo.

### Lo que pasó con `guardar_reporte()` (sesión 11)

- ⚠️ **No entendió las tres preguntas cuando se las hice juntas.** Lo dijo él:
  *"no entendí las preguntas"*. Se reformularon a **una sola**, con analogía del
  portero (lista de prohibidos vs lista de autorizados) y **la contestó bien de
  inmediato**: *"el portero A, porque no conoce al nuevo peligroso"*.
  → **Regla de método para lo que queda del curso: una pregunta a la vez.**
  Tres preguntas encadenadas no son tres veces más difíciles, son un muro.
- También pidió **"escríbeme un ejemplo primero"**. Se le dio el patrón completo
  sobre **otra función** (`poner_apodo`, nada de archivos) para no regalarle la
  suya. Funcionó: copió la estructura, no la respuesta. **Conservar esa técnica.**
- Escribió los 3 frenos. Dos defectos suyos, los dos didácticos:
  1. `{"error". "..."}` con **punto en vez de dos puntos** → `SyntaxError`.
  2. **El mensaje de error mentía:** copió *"solo letras y números"* del ejemplo,
     pero su `PERMITIDOS` también acepta `-`, `_` y `.`. → **el mensaje de error
     es la instrucción de reintento que le das al agente**; si es incompleto,
     reintenta peor de lo que podría. Es L4.9 en espejo (allá era negar en
     silencio, aquí es negar con una explicación equivocada).
- **Corrida real, 6 casos, $0.00:** `reporte-trm-2026-07-30.txt` guardado;
  `../../.env`, `C:/Windows/x.txt`, `reporte.md`, `mi reporte.txt` y `..txt`
  rechazados. En `caja/` quedó un solo archivo.
  - **Hallazgo que no esperaba:** `../../.env` **no lo paró la allowlist**, lo
    paró el freno 1 (no termina en `.txt`). Tres candados apilados y al ladrón lo
    atrapó el que menos parecía de seguridad.
- ✅ **Se midió si el freno 3 sirve, en vez de suponerlo.** Fuerza bruta sobre
  **278.916 nombres** (todos los armables con `PERMITIDOS` + `.txt`): los que
  llevan `..` **y además escapan de `caja/` son 0**. **El freno 3 hoy no bloquea
  nada** — escapar necesita un separador y el freno 2 ya prohíbe `/` y `\`.
  - Se le planteó como decisión consciente: quitarlo (código muerto) o dejarlo
    con comentario (seguro para el día que alguien agregue `/` a `PERMITIDOS`).
    Recomendación dada: **dejarlo con la nota** — un candado sin nota se borra en
    la siguiente limpieza. ⚠️ **Él no había contestado todavía.**
  - → Candidata a lección L5b.x: **no des por bueno un candado sin probar que
    atrapa algo.** Y aquí la prueba se pudo hacer **entera** (278.916 casos, $0.00,
    sin red) porque la herramienta no sabe que Claude existe. Es el argumento más
    fuerte que ha dado el curso a favor de separar `herramientas.py`.

✅ **URLs YA VERIFICADAS el 2026-07-29** (sesión 9), las dos con HTTP 200, y están
copiadas en `05b-proyecto/README.md` §5b.4 con sus campos y la advertencia de la
brecha variable. **No hace falta volver a comprobarlas** si la próxima sesión es
pronto; sí conviene si pasan varios días.

⚠️ **Formato del 5b, decidido por él y con una razón que no hay que perder:
MIXTO.** Lo mecánico se dicta (carpetas, `import`, estructura); lo conceptual lo
escribe él (bucle, frenos, evals): se le dice *qué* y *por qué*, lo intenta, y
después compara con mi versión. **La razón:** si se le dicta todo, termina con un
agente que funciona y que no sabría rehacer — sería el único nivel donde el
código no pasó por su cabeza.

---

**Lo que queda vivo del nivel 5** (todo voluntario, nada bloquea el 5b — igual
que los pendientes de los niveles 2 y 3):

- ⚠️ **Ejercicio 4, el mejor que quedó sin hacer.** Meter `"No olvide"` en el
  detector. Las 4 mezclas reales lo llevaban **todas**, así que un `if` de una
  línea le gana a los dos jueces ($0.00, 100% estable, cero citas fabricadas).
  Es la demostración más limpia de L5.15 que ha dado el curso.
  ⚠️ Si lo retoma: **límites de palabra** (`\bolvide\b`) — `'olvide' in
  "no olvides"` es `True` y `"No olvides"` es tuteo correcto (L5.24).
- ⚠️ **Los 6 scripts con el precio suelto siguen con el bug armado.** Hoy no
  mienten (modelo y precio coinciden), pero mienten el día que se cambie
  `MODELO`: `01/02/03_contar.py`, `04-harness-real/03_harness.py`,
  `02-conversacion/02_ventana.py` y `03_recortar.py`. Se le ofreció arreglarlos
  y prefirió avanzar. → aplicar el patrón `PRECIOS[MODELO]` de L5.23 cuando toque.
- ⚠️ **Él no leyó a mano ninguna de las 8 respuestas** que marcó Sonnet. Las
  analizó un script con reglas mías: comparte **mi** punto ciego, no el del
  modelo. Son 8, es barato.
- ⚠️ **El defecto del TRATAMIENTO (tú/usted) está medido pero sin arreglar.**
  En la v2: 26 tú / 2 usted / 2 mixto. En la v3-A: 6 de 30 `póngase`. **Ni B ni C
  lo arreglaron.** → ejercicio 2.
- ⚠️ **B vs C sigue sin resolverse:** se solapan con N=30. → ejercicio 3.

**Dos dudas viejas cerradas en el nivel 5:** *"¿cómo se prueba algo que nunca
responde igual dos veces?"* (abierta desde el nivel 1) y *"¿por qué aparece el
rioplatense?"* (abierta desde el nivel 3).

**Detalle del nivel 5 (histórico):**

- ✅ **RESUELTO en la sesión 9 (ejercicio 1).** Antes decía: *"los 43 marcados
  por el juez no se revisaron uno por uno"*. El juez de Sonnet redujo la lista a
  **8**, y las 8 se revisaron con código: **4 mezclas reales** (todas con
  `"No olvide"` + `"ponte"`), **3 falsas alarmas** y **1 cita fabricada**.
  Los dos jueces cazaron **las mismas 4** → el conteo real de mezclas en las
  120 respuestas es **4**, no 43 ni 46. Ver §5.6.
- El detalle del defecto del tratamiento (v2: 26 tú / 2 usted / 2 mixto; v3-A:
  6 de 30 `póngase`) y el solape B vs C están en la bitácora de la sesión 8.

**Cómo trabaja este estudiante** (confirmado otra vez en la sesión 8): pide la
explicación **antes** de ejecutar, y después compara sus números con los del
README. Mantener el ritmo: explicar → predecir → correr → comparar → escribir.
**Novedad de esta sesión, que hay que conservar: se le pidió una predicción por
escrito antes de cada corrida.** Funcionó muy bien — acertó el número de
respuestas `mixto` (2 de 30) y falló el del dialecto (dijo 5, salió 9), y las
dos cosas enseñaron. También hace **preguntas conceptuales espontáneas de mucho
nivel** (guardrails, jurado de jueces, evaluación en multi-agente); vale la pena
responderlas bien y anotarlas.

**Cómo trabaja este estudiante** (confirmado en la sesión 6): pide la
explicación **antes** de ejecutar, y después compara sus números con los del
README. De esa comparación es de donde han salido los mejores hallazgos del
curso. Mantener ese ritmo: explicar → correr → comparar → escribir.

---

## Estado de los niveles

| Nivel | Nombre | Material escrito | Estudiante lo completó |
|---|---|---|---|
| 0 | Setup | ✅ | ✅ |
| 1 | Primera llamada | ✅ | ✅ |
| 2 | Conversación con memoria | ✅ | ✅ |
| 3 | Primer agente (clima) | ✅ | ✅ |
| 4 | Harness real | ✅ | ✅ |
| 5 | Evaluación (evals + rúbricas) | ✅ | ✅ |
| **5b** | **Proyecto integrador (divisas/TRM)** ← **EN CURSO** | 🔄 README ✅ | 🔄 paso 6/10 |
| 6 | TypeScript | ⬜ | ⬜ |
| 6b | Memoria persistente y Skills | ⬜ | ⬜ |
| 7 | Producción (incl. observabilidad) | ⬜ | ⬜ |
| 8 | Multi-agente (orquestador + workers) | ⬜ | ⬜ |

> ⚠️ **Los niveles 5 y 6 se intercambiaron en la sesión 6.** Antes: 5 = TypeScript,
> 6 = Evaluación. Ahora: **5 = Evaluación, 6 = TypeScript**. Las entradas de la
> bitácora anteriores a la sesión 6 usan la numeración vieja — cuando digan
> "nivel 6" refiriéndose a evaluación, hoy es el **nivel 5**.

Leyenda: ⬜ pendiente · 🔄 en curso · ✅ hecho

---

## Bitácora de sesiones

### Sesión 1 — 2026-07-28
- Definimos el plan: 9 niveles, Python primero, TypeScript desde el nivel 5.
- Escribí el material de los niveles 0 y 1.
- Creé `CLAUDE.md` y este archivo para que la memoria sobreviva entre sesiones.
- **Verificado:** los 4 scripts compilan sin errores de sintaxis.
- **NO verificado:** ningún script se ha ejecutado de verdad todavía — falta la API key.
- Pendiente del estudiante: hacer el nivel 0.

### Sesión 2 — 2026-07-28
- **Nivel 0 COMPLETADO.** Creamos `.venv` en la raíz e instalamos `anthropic 0.120.0`
  y `python-dotenv`. El estudiante consiguió su API key y la guardó en `.env`.
- `verificar.py` corrió de verdad: `TODO LISTO`, con llamada real a la API
  (17 tokens entrada / 5 salida). **Primera ejecución real del curso.**
- Duda resuelta: diferencia entre **suscripción** (Claude Pro/Code, mensualidad, para
  que Claude te ayude) y **créditos de API** (pago por token, lo que consumen tus
  propios programas). Son facturas separadas.
- Explicamos `verificar.py` línea por línea. El estudiante pidió dejar registro.
- **Creamos `LESSONS.md` y `GUIDE.md`** (separados a propósito: el *por qué* vs el
  *cómo*). Nivel 0 documentado con 9 lecciones (L0.1–L0.9).
- Actualizamos `CLAUDE.md` con las reglas de mantenimiento de esos archivos.
- **Nivel 1 COMPLETADO.** Corrió los 3 scripts y los 3 ejercicios.
- Hallazgos propios del estudiante (16 lecciones, L1.1–L1.16). Los mejores:
  - Con `max_tokens=30`, Opus 5 devolvió **solo un bloque `thinking`** y cero texto.
    `content[0].text` habría reventado. L0.7 comprobada en su máquina.
  - Cambiar solo el `SYSTEM` (profesor → pirata) **cuadruplicó la factura**.
  - El script `03_costo.py` **imprimía "Haiku cuesta 5x menos"** — la medición real
    dio **55x**. Corregimos el script para que calcule la razón en vez de fijarla.
  - Detectó que la fila de Sonnet no estaba cortada por el modelo sino por
    `texto.strip()[:30]` del propio script. Arreglado con `" ".join(texto.split())`.
- **El estudiante corrigió un análisis mío**: avisó que había añadido la regla
  "máx 4 frases" antes del ejercicio 3, así que el experimento tenía 3 variables,
  no 1. Reescribimos L1.10 y L1.11.
- Costo total del nivel: menos de $0.05 USD.

### Sesión 3 — 2026-07-28
- **Pendiente de la sesión 2 resuelto:** corrimos `03_costo.py` ya corregido.
  La tabla sale entera (la fila de Sonnet ya no rompe el formato) y la razón se
  calcula de verdad. **Pero dio 30.9x, no 55x** como la vez pasada. Mismo script,
  mismo precio por token: lo único que cambió fue cuánto razonó Opus esa corrida.
  → El costo tampoco es determinista. Corregimos `GUIDE.md`, que afirmaba "55x"
  como si fuera un dato fijo.
- **Nivel 2 escrito y verificado** (`02-conversacion/`): README + 3 scripts.
  - `01_chat.py` — bucle de chat con historial. Interactivo, **no ejecutado**
    (lo corre el estudiante). Usa Haiku a propósito: en un bucle se reenvía todo.
  - `02_ventana.py` — **ejecutado.** 6 preguntas cortas: la entrada pasó de
    43 a 469 tokens (11x) sin que las preguntas crecieran. Costo: $0.0038.
  - `03_recortar.py` — **ejecutado.** Compara historial completo (418 tok) vs
    ventana deslizante (127 tok) vs resumen+recientes (308 tok).
- **Error mío detectado y corregido antes de entregar:** la primera versión de
  `03_recortar.py` probaba el olvido preguntando "¿qué es una variable?". Las
  tres estrategias respondieron bien —el modelo ya sabe qué es una variable—,
  así que la prueba no demostraba nada, pero el texto afirmaba que sí. Era L1.13
  otra vez. Lo cambié por un dato inventado (el nombre "Marta" y su taller de
  bicicletas) que solo existe en el turno 1. Ahora la ventana deslizante
  responde *"No tengo esa información"* y la demostración es real.
- **Segundo texto falso corregido:** el cierre decía que el resumen cuesta
  "casi lo mismo que la ventana". La medición dice 308 vs 127 tokens (2.4x más).
  Reescrito para explicar por qué: con 8 turnos el resumen no gana; gana con 80,
  porque su tamaño se mantiene fijo mientras el historial crece.
- `GUIDE.md` ampliado: `count_tokens` (§5.b) y tabla de ventanas de contexto (§5.c).
- **El estudiante corrió `01_chat.py`.** 5 turnos: entrada 61 → 808 tok (13x).
  Verificamos con su propia tabla que `entrada(n) = entrada(n-1) + salida(n-1)
  + su mensaje`; cuadra en los 4 saltos. Hallazgo suyo del análisis: **el
  historial crece sobre todo por lo que responde Claude (~200 tok/turno), no
  por lo que escribe el usuario (~25 tok/turno).**
- **BUG encontrado por el estudiante en `01_chat.py`:** el contador imprimía
  `len(historial) // 2`, que asume 2 mensajes por turno. Al hacer el ejercicio 1
  entra 1 por turno y el contador salió `0, 1, 1, 2`. Arreglado con una variable
  `turno` propia. **Regla:** no deduzcas un dato de la forma de una estructura
  que puede cambiar.
- **Comentario mío falso, corregido en el código:** decía que sin guardar el
  turno `assistant` "cada turno empieza de cero". Falso. Los mensajes del
  usuario siguen entrando, así que Claude **recuerda los datos y olvida el
  diálogo**: contestó bien "vives en Sabaneta, estás en Bucaramanga", pero
  saludó "¡Hola Juan!" 4 veces y repitió la misma recomendación 3 veces.
- Ejercicio 1 completado. Entrada con memoria completa vs sin respuestas:
  570 vs 116 tokens en el turno 4 (~5x más barato, y coherencia destruida).
- **`02-conversacion/README.md` actualizado** con todo lo anterior: nueva sección
  **2.1b** (tabla de la corrida real, la fórmula verificada con restas, el
  resultado del ejercicio 1, y el bug del contador). Ejercicio 1 marcado como
  hecho. Nuevo ejercicio 6: medir la "cuarta estrategia".
- **El estudiante corrió `02_ventana.py`.** Entrada 43 → 511; total 1.669 tok,
  $0.0041. Tres hallazgos al comparar sus números con los míos:
  1. **El turno 1 dio 43 en las dos corridas.** La entrada es determinista
     (system + pregunta ya existen); lo que varía es la salida.
  2. **Medimos el defecto que yo había confesado.** Restando
     `entrada − (entrada previa + salida previa)` en ambas corridas, las
     preguntas pesan 10, 14, 10, 11, 12 tokens — **idéntico en las dos**.
     El historial aporta ~90/turno, o sea 7x más. El defecto era real pero
     irrelevante, y ahora está medido en vez de supuesto.
  3. **Amplificación de la salida:** 27 tokens de salida de más costaron 145
     tokens de entrada de más (~5x). Un token generado en el turno 1 se
     reenvía 5 veces. → Pedir respuestas cortas en el SYSTEM ahorra en todos
     los turnos siguientes, no solo en uno.
- **Cuarto texto falso mío, corregido:** `02_ventana.py` afirmaba que la entrada
  "crece como una escalera cada vez más alta". Los incrementos reales son
  planos (99, 101, 81, 82, 105) porque el SYSTEM limita a 2 frases. Yo había
  generalizado desde `01_chat.py`, que no tiene ese límite y ahí sí aceleraban
  (124, 177, 208, 238). **El escalón mide lo que mida la respuesta anterior.**
  Corregido en el script y explicado en el README con la comparación de ambos.
- **El estudiante corrió `03_recortar.py`.** Resultados: completo 418, ventana
  127, resumen 293 (el mío dio 308).
  1. **Confirmada la determinismo por tercera vez:** las estrategias 1 y 2
     coinciden AL TOKEN entre corridas (texto preexistente); solo la 3 varía,
     porque el resumen lo genera el modelo. Ya es una propiedad, no casualidad.
  2. **Mejor evidencia que la mía:** su ventana deslizante respondió *"solo me
     has preguntado sobre errores de sintaxis y cómo leer mensajes de error"* —
     que es EXACTAMENTE el contenido de los últimos 4 mensajes. El modelo
     recita su propia ventana. No alucina: describe la lista que recibió.
- **Cerrado el hueco de honestidad que yo mismo había señalado:** la tabla
  comparaba tokens pero no incluía el costo de GENERAR el resumen. En vez de
  estimarlo, modifiqué `03_recortar.py` para medirlo. Resultado: resumen
  $0.001077, ahorro $0.000117/turno → **se paga solo a los ~9 turnos**.
  Generar el resumen cuesta 9x lo que ahorra en un turno. Convierte "resumir
  ahorra" en "¿cuánto va a durar esta conversación?".
- **El estudiante preguntó "¿cómo se prueba gratis?"** Yo había escrito "es
  gratis" en 3 sitios **sin verificarlo** — salía de mi memoria. Lo comprobé en
  `platform.claude.com/docs/.../token-counting`. Era cierto, pero aparecieron
  dos letras pequeñas que yo ignoraba y que ahora están en `GUIDE.md` §5.b y en
  el README del nivel:
  1. **Es un estimado**, no exacto: el conteo real "puede diferir en una
     cantidad pequeña".
  2. **Gratis ≠ ilimitado:** 2.000 peticiones/minuto en el nivel inicial, con
     límite propio e independiente del de `messages.create`.
  Lección de método: *verificar también lo que resultó ser verdad* — la
  comprobación trajo dos matices que la afirmación correcta escondía.
- **NIVEL 2 CERRADO.** 14 lecciones escritas en `LESSONS.md` (L2.1–L2.14).
  Costo total del nivel: menos de $0.03 USD entre todas las corridas.
  Ejercicios hechos: el 1 (y de él salieron un bug y una cuarta estrategia).
  Pendientes voluntarios si quiere retomarlos algún día: ejercicios 2, 3, 4, 5, 6.
  El 4 (romper el prompt del resumen) y el 6 (medir la cuarta estrategia) son
  los que más enseñan.
- **Auditoría pedida por el estudiante** ("revisa que todo esté actualizado").
  Aparecieron 3 huecos que yo había dado por cerrados:
  1. La frase falsa de la "escalera cada vez más alta" **seguía viva** en la
     sección *Lo que ya sabes* del README. La corregí en el script y en el
     cuerpo del README, pero no en el resumen. → **Al corregir una afirmación,
     buscarla en TODOS los archivos, no solo donde la viste.**
  2. La tabla de §2.2 decía "lo que se midió de verdad" sin aclarar que era una
     de dos corridas. Etiquetada como *corrida A*.
  3. `GUIDE.md` decía solo "la salida cuesta ~5x más que la entrada", sin el
     segundo multiplicador (la salida se recobra como entrada en cada turno
     siguiente). Agregado.
- **Recaída mía en el mismo error, atajada en el momento:** metí una fila con
  "~180 tokens" para la cuarta estrategia dentro de la tabla titulada
  *"Resultados reales de la corrida"*. Nadie la midió: me la inventé. La quité y
  la convertí en el ejercicio 6, para que el número salga de una medición.
  Tercera vez en la sesión que aparece el mismo patrón (ver L1.13).

### Sesión 4 — 2026-07-28
- **Nivel 3 escrito y verificado** (`03-primer-agente/`): README + 3 scripts.
  Los **tres se ejecutaron de verdad**, no solo compilan.
  - `01_pedir_herramienta.py` — **ejecutado.** Define una herramienta que *no
    existe* como función, y aun así funciona: `stop_reason=tool_use`, un bloque
    `type=tool_use` con `id=toolu_01WQq8...`, `name=obtener_clima`,
    `input={"ciudad": "Bogota"}`. El modelo extrajo "Bogota" de la frase solo.
    - **El estudiante lo corrió y le salió DISTINTO:** 2 bloques
      (`thinking` + `tool_use`) donde a mí me salió 1 (solo `tool_use`). Mismo
      script, mismo modelo. Opus 5 decide por llamada si razona. → No solo el
      texto es no determinista: **la estructura de `content` también lo es**.
      Es la mejor prueba posible de L0.7: `content[0].name` habría funcionado
      en mi máquina y reventado en la suya. README corregido: la salida ya no
      se presenta como un hecho fijo, sino como corrida A vs corrida B.
  - `02_bucle.py` — **ejecutado.** Bucle agéntico completo con clima falso
    (diccionario). Medellín: vuelta 1 `tool_use` (452 in / 73 out) → vuelta 2
    `end_turn` (543 in / 82 out). **Una pregunta = 2 llamadas.**
    - **El estudiante lo corrió.** Comparando sus números con los míos salieron
      cuatro cosas, todas medidas:
      1. **Las 3 entradas de vuelta 1 coincidieron AL TOKEN** (452, 458, 452)
         entre dos corridas distintas. El menú de `tools` es texto fijo.
      2. **La única divergencia se propagó exacta:** Bogotá dio 102 vs 106 de
         salida en v1, y la entrada de v2 dio 580 vs 584. Los mismos 4 tokens.
         Confirma la fórmula del nivel 2 con herramientas:
         `entrada(v2) = entrada(v1) + salida(v1) + tool_result`.
      3. **El peso del `tool_result` es determinista** y dio idéntico en ambas
         corridas: 18 tokens (Medellín), 20 (Bogotá), **46 (el mensaje de error
         de Tokio)**. Lógico: ese texto lo escribe la función, no el modelo.
         → Lo que devuelve una herramienta se reenvía en cada vuelta siguiente.
         Un JSON gigante sale caro para siempre. Recortar salidas de
         herramientas es harness, igual que recortar historial.
      4. **Costo:** 3 preguntas ≈ $0,030 (3.062 in / 590 out). En el nivel 2,
         6 preguntas costaron $0,0041 → **7x más caro con la mitad de
         preguntas**, por dos multiplicadores apilados: Opus vs Haiku, y dos
         llamadas por pregunta en vez de una.
    - **Hallazgo que no es de tokens:** las respuestas salieron en español
      rioplatense ("Querés", "llevá paraguas", "campera") y el estudiante es
      colombiano. Este script no tiene `SYSTEM`. **Sin ancla de voz, el modelo
      elige una** — bug visible para el usuario que ninguna prueba automática
      detecta. Anotado en el README; el script 3 sí tiene `SYSTEM` para comparar.
  - `03_agente_real.py` — **ejecutado.** Clima real vía Open-Meteo (gratis, sin
    llave, por `urllib`) + una segunda herramienta `hora_utc`.
- **Las 4 predicciones del script 3 se cumplieron todas** en la corrida real:
  "¿qué hora es?" → solo `hora_utc`; "clima en Bucaramanga" → solo
  `obtener_clima` (26.4 C, parcialmente nublado — dato que el modelo no podía
  tener); "compara Bogotá y Cartagena" → **`obtener_clima` dos veces en la MISMA
  vuelta** (dos bloques `tool_use` en un turno); "17 por 23" → **ninguna
  herramienta**, `end_turn` en la vuelta 1. Nadie programó esas decisiones: solo
  existen las `description`.
- **Error real encontrado al ejecutar `02_bucle.py`:** `UnicodeEncodeError:
  'charmap' codec`. El agente había funcionado perfecto — lo que reventó fue el
  `print`, porque la consola de Windows es `cp1252` y Claude respondió con `°` y
  emojis. Arreglado con `sys.stdout.reconfigure(encoding="utf-8")` en los tres
  scripts. **El traceback apuntaba a `print`, no a la API.** Documentado en
  `GUIDE.md` §3 y en el README del nivel.
- `GUIDE.md` ampliado: 3 filas nuevas en la tabla de errores (encoding,
  `tool_use_id` que no coincide, guardar solo el texto en vez de
  `respuesta.content`) y una sección **§4.b — plantilla del bucle agéntico**
  con las 4 reglas que rompen el programa si se ignoran.
- **Decisión de diseño del nivel:** bucle **manual**, no el `tool_runner` del
  SDK. El SDK tiene un helper que hace todo esto solo, pero esconde justo lo que
  hay que entender. El `tool_runner` se puede mencionar en el nivel 4, ya con el
  bucle entendido a mano.
- Costo de escribir y verificar el nivel: unos pocos centavos.
- **El estudiante corrió los 3 scripts y los ejercicios 1 y 2.** Hallazgos suyos
  al comparar sus números con los míos, además de los ya anotados arriba:
  - **Las 4 entradas de vuelta 1 de `03_agente_real.py` coincidieron al token**
    (598, 610, 612, 605). Cuarta confirmación de que la entrada es determinista.
  - **Con API real el costo deja de ser determinista.** Bucaramanga dio 709 vs
    714 de entrada en v2 con la MISMA salida de v1 (59). La diferencia de 5
    tokens la puso el cielo: `nublado` vs `parcialmente nublado`. En el script 2,
    con diccionario fijo, el peso del `tool_result` era idéntico entre corridas.
  - **El menú de `tools` es una suscripción fija:** "¿cuánto es 17 por 23?" no
    usó ninguna herramienta y pagó 605 tokens de entrada. La pregunta pesa ~10;
    el resto es `SYSTEM` + las 2 descripciones, que viajan siempre.
  - Las 4 predicciones del script 3 se cumplieron en su corrida también,
    incluidas las dos peticiones en la misma vuelta.
- **Predicción MÍA que falló, y era mi error de diseño:** le dije que mirara si
  el `SYSTEM` arreglaba el dialecto rioplatense. No lo arregló — el `SYSTEM`
  decía *"Responde en espanol"*, que **no especifica cuál español**. Le pedí un
  idioma, no una variedad. Y apareció en **1 de 4** respuestas: un defecto
  intermitente, que no se detecta probando una vez. Convertido en ejercicio 7
  (con nota de que una corrida limpia no prueba nada → guiño al nivel 6).
- **NIVEL 3 CERRADO.** 16 lecciones escritas en `LESSONS.md` (L3.1–L3.16).
  Ejercicios hechos: 1 y 2 (los dos de sabotaje). Pendientes voluntarios: 3, 4,
  5, 6, 7, 8. El 7 (anclar el dialecto y medirlo en varias corridas) y el 8
  (medir el costo del menú con `tools=[]`) son los que más enseñan.
  Costo total del nivel para el estudiante: unos $0,06.

### Sesión 5 — 2026-07-28
- **Nivel 4 escrito y verificado** (`04-harness-real/`): README + 4 scripts.
  Los **cuatro se ejecutaron de verdad**, con sus números en el README.
  - `01_errores.py` — **ejecutado.** Provoca 5 fallas: 401, 404, `ValueError`,
    400 y `APIConnectionError`. Cuesta $0.00 (ninguna genera tokens).
    - **Sorpresa mía al escribirlo:** puse `max_tokens=99_999_999` esperando un
      400 del servidor y salió un **`ValueError` de Python**. El SDK calcula que
      la respuesta tardaría más de 10 minutos y **se niega a mandar la petición**.
      Nunca hubo red. Agregué un quinto caso (`temperature=0.5`, que Opus 5 ya
      no acepta) para tener también un 400 real y poder comparar los dos.
    - De ahí salió **L4.2: un error puede morir en tres sitios** — tu máquina,
      la red, o el servidor. "Falló la API" son tres diagnósticos distintos.
  - `02_reintentos.py` — **ejecutado.** Cuatro mediciones con cronómetro:
    1. Mismo error de red, subiendo `max_retries`: **0.22s / 0.39s / 1.34s /
       3.39s** para 0, 1, 2 y 3 reintentos. El error es idéntico; lo que crece
       es el tiempo, y **el SDK reintenta en silencio**.
    2. `max_retries=5` con llave mala: **0.39s**. No reintentó ni una vez. El
       SDK ya sabe que un 401 es permanente.
    3. `timeout=1s` con 0 reintentos: **1.00s**. Con 2 reintentos: **4.20s**.
       El timeout es **por intento**. Con los valores de fábrica (10 min, 2
       reintentos) el peor caso es **media hora colgado**.
    4. Reintento propio con espera exponencial + jitter, sobre una llamada real.
    - **Hallazgo retroactivo importante:** `max_retries=2` es el valor de
      fábrica, así que **todos los scripts de los niveles 1, 2 y 3 podían hacer
      hasta 3 peticiones por cada `create()`**. Nunca se notó porque nunca falló
      nada. → L4.4.
  - `03_harness.py` — **ejecutado dos veces** (concediendo y negando el permiso).
    El agente del clima con las 6 piezas: timeout, errores tipados, presupuesto
    en dólares, tope de vueltas, permisos y registro JSONL.
    Nueva herramienta peligrosa `borrar_archivo`, que borra de verdad dentro de
    una carpeta `caja/` que el script crea con dos archivos de mentira.
    - Corrida completa: **$0.0319** de un tope de $0.10, 3 preguntas, 6 llamadas.
    - **Con permiso:** borró y contestó *"Listo, ya borré borrador.txt"*.
    - **Sin permiso:** el archivo siguió ahí y contestó *"No pude borrarlo: el
      sistema negó el permiso"*. Funcionó porque le devolvemos un `tool_result`
      que dice `PERMISO DENEGADO`. → L4.9: negar en silencio haría que el
      agente dijera "ya lo borré" con el archivo intacto.
  - `04_streaming.py` — **ejecutado.** Primera palabra a los **11.9s** sin
    streaming vs **8.6s** con streaming. Anotado en el README que es **una sola
    corrida y las dos respuestas no midieron lo mismo** (la de streaming salió
    de 787 tokens, por eso su total es mayor): lo único comparable ahí es
    cuándo aparece la primera palabra.
- **Predicción del nivel 3 que se cayó (mía):** en L3.15 concluí que el
  rioplatense aparecía porque el `SYSTEM` decía solo *"Responde en espanol"*,
  sin especificar la variedad. En el harness el `SYSTEM` dice **"español de
  Colombia"** y aun así salió *"Si querés, autorizá"* en **1 de 3** respuestas.
  La explicación del nivel 3 era razonable y encajaba con los datos, pero era
  **incompleta**. Escrito como L4.13: una hipótesis no está confirmada hasta
  que arreglas la causa y el defecto desaparece. Medirlo en serio es nivel 6.
- `GUIDE.md` ampliado: 4 filas nuevas en la tabla de errores (el `ValueError` de
  streaming, `temperature` deprecado, el timeout multiplicado, los reintentos
  anidados) y dos secciones nuevas: **§4.c — los seis frenos del harness** y
  **§4.d — streaming**.
- `LESSONS.md`: 13 lecciones nuevas (L4.1–L4.13).
- **Decisión de diseño:** el permiso se pide **fuera** de la herramienta, en el
  harness. La función `borrar_archivo()` solo obedece; quien decide es el
  diccionario `PERMISOS` y, si toca, el humano. Además la herramienta se
  defiende sola (solo borra dentro de `caja/`): dos candados, porque el permiso
  lo puede dar un humano distraído.
- Costo de escribir y verificar el nivel: unos $0.08 en total.

### Sesión 6 — 2026-07-28
- **El estudiante corrió `01_errores.py`.** Las 5 clasificaciones salieron
  **idénticas** a las mías.
  - **Primera cosa determinista del curso**, y tiene explicación: en este script
    el modelo nunca genera nada, las 5 peticiones mueren antes. Lo no
    determinista siempre fue *la generación*, no la infraestructura. → Es lo que
    hace posible el nivel 5: el harness sí se puede probar de forma repetible.
    Lo único que cambia entre corridas es el `request_id`.
  - El caso 5 mostró la causa envuelta: `causa: ConnectError`. `APIConnectionError`
    es una etiqueta de Anthropic encima de un error de `httpx`.
- **Defecto mío encontrado al leer la salida, y arreglado antes de seguir:**
  el script imprimía `e.message[:80]`, y el corte caía **a mitad del JSON crudo**,
  justo antes del mensaje útil. Los casos 1 y 2 eran ilegibles. Es el mismo
  patrón de `texto.strip()[:30]` del nivel 1: **el script mutila el dato y luego
  parece culpa del servidor.**
  - Arreglo: función `motivo(e)` que entra a `e.body` (el JSON ya parseado que
    el SDK te da) y saca `body["error"]["message"]`. Verificado ejecutando, no
    supuesto.
  - **Regalo inesperado:** ahí venía también el `request_id`, el número que se
    le da a soporte de Anthropic para que encuentren tu petición. Estaba desde
    siempre, escondido detrás del corte.
- **Hallazgo nuevo al poder leer los mensajes:** son de calidad muy desigual.
  El 404 dice solo `model: claude-opus-9-mil` (repite lo que mandaste, no ayuda);
  el 400 dice `` `temperature` is deprecated for this model `` (te dice qué hacer).
  → **Clasificar por clase de excepción, nunca por el texto del mensaje.** El
  texto lo cambia el proveedor sin avisar; la clase no.
- `04-harness-real/README.md` §4.1 actualizado con todo lo anterior.
- **El estudiante corrió `02_reintentos.py`.** Sus tiempos: A 0.31/0.50/1.34/3.00,
  B 0.41, C 1.02 y 4.36. Los míos: A 0.22/0.39/1.34/3.39, B 0.39, C 1.00 y 4.20.
  - **Los números no se repiten pero la forma sí.** Su red es más lenta; el orden
    y las proporciones aguantaron enteros. → Un script de tiempos se lee
    comparando filas entre sí, nunca contra un número fijo.
  - El `1.34s` idéntico en A **es casualidad** y lo anoté como tal en el README.
    Importa distinguirlo de las coincidencias al token de los niveles 2 y 3, que
    sí tenían causa mecánica (el texto de entrada era el mismo).
  - **Hallazgo nuevo: la sección C aísla el backoff mejor que la A.** En A el
    tiempo mezcla "lo que tarda el intento en fallar" con "lo que espera el SDK".
    En C cada intento cuesta exactamente 1.00s (lo fija el timeout), así que
    restando sale la espera pura: **4.36 − 3.00 = 1.36s** en su corrida, 1.20s en
    la mía. Casi igual en dos redes distintas, porque es un `sleep` del SDK.
    → Misma técnica de resta del nivel 2. **Lo que no puedes medir directo, lo
    fijas todo lo demás y lo restas.**
  - **Hallazgo nuevo: apareció `APITimeoutError`**, que no salió en el script 1.
    La sección A da `APIConnectionError` y la C da `APITimeoutError` — y las dos
    se reintentan porque **una hereda de la otra**. Es la contraparte de la
    lección del orden de los `except`: ahí se ve para qué sirve el caso general.
  - B confirmado por comparación: 0.41s con `max_retries=5` es el mismo orden que
    `max_retries=0` (0.31s), no el de 3 reintentos (3.00s). **Un número solo
    significa algo al lado de otro número.**
  - D: 37 in / 47 out ≈ $0.0013, sin reintentos (la llamada funcionó). La
    respuesta salió en español neutro, sin rioplatense — pero **n=1, no prueba
    nada** sobre el defecto del dialecto (L4.13).
  - `README.md` §4.2 actualizado: tablas con las dos corridas, la resta del
    backoff, y la sección de la herencia de excepciones.
- **Candidatas a lección, para cuando se cierre el nivel 4** (irían como L4.14 en
  adelante; el material ya está en esta bitácora y en el README del nivel):
  1. **La infraestructura sí es determinista, aunque el modelo no.** Es la base
     de que el nivel 5 sea posible: se puede probar el harness de forma repetible
     aunque no se pueda probar la generación.
  2. **Clasificar por clase de excepción, nunca por el texto del mensaje.** Los
     mensajes son de calidad desigual (comparar el 404 con el 400) y el proveedor
     los cambia sin avisar.
  3. **Antes de recortar un error, mira si el SDK ya te lo dio parseado**
     (`e.body`). Y de ahí salió gratis el `request_id`.
  4. **Un número solo significa algo al lado de otro número.** Los tiempos no se
     reproducen entre máquinas; la forma sí. Y hay que saber cuándo una
     coincidencia es mecánica y cuándo es casualidad.
  5. **Lo que no puedes medir directo: fija todo lo demás y réstalo.** La espera
     del SDK salió de `4.36 − 3.00`. Misma técnica que el nivel 2.
  6. **El caso general del `except` atrapa hijos que no sabías que existían**
     (`APITimeoutError` hereda de `APIConnectionError`).

### Sesión 7 — 2026-07-29
**NIVEL 4 CERRADO, sin cabos sueltos.** Se corrieron los 2 scripts que faltaban
**y los 2 ejercicios abiertos (8 y 9)**. Las dos hipótesis pendientes quedaron
medidas.

- **`03_harness.py`, dos corridas** (concediendo y negando). Totales $0.0323 y
  $0.0328 contra mis $0.0319. Con `s` el archivo desapareció; con `n`
  `borrador.txt` seguía ahí y el agente dijo la verdad.
- **Se leyó `registro.jsonl` con él**, que era el objetivo pedagógico del paso.
  Cuatro hallazgos, todos de comparar los dos registros:
  1. **Negar cuesta más que conceder.** v2 de la pregunta del borrado: 823/35
     con `s` contra 838/54 con `n`. Los **dos** lados suben: el texto
     `PERMISO DENEGADO` pesa 15 tokens más y el agente gasta 19 más
     explicándose. La cuenta cuadró exacta (15×$5/M + 19×$25/M = $0.00055) y de
     paso **confirmó el precio de Opus 5 con aritmética propia: $5/M in,
     $25/M out.** → L4.20.
  2. Entradas de vuelta 1 idénticas al token en las dos corridas (724, 735, 736)
     y la única divergencia propagada exacta (93/94 out → 934/935 in).
     Séptima confirmación.
  3. **El harness no tiene memoria entre preguntas** — no se había dicho nunca.
     Las tres vueltas 1 arrancan en ~730, no acumulan. Explica por qué el costo
     por pregunta es plano, al revés que en el nivel 2.
  4. **El hallazgo que solo existe en el registro:** 47 s entre `llamada_api`
     (3.98 s) y `herramienta`. Los otros 43 fueron **el humano** decidiendo el
     permiso. Ninguna de las otras cinco piezas del harness puede decir eso.
     Primera vez que la observabilidad responde algo que nada más responde.
     → L4.21, y es el anticipo directo del nivel 7.
- **`04_streaming.py` corrido.** Primera palabra a los **13.2 s** sin streaming
  contra **5.8 s** con streaming (2.3x de adelanto; el mío fue 1.38x). Números
  distintos, dirección idéntica.
  - **Los totales no eran comparables** (691 vs 814 tokens de salida) y se
    normalizaron a **52.3 vs 58.6 tokens/segundo**: con streaming se generó
    *más* texto por segundo. Sin normalizar, la conclusión se invierte. → L4.22.
  - **Hipótesis nueva, escrita COMO hipótesis:** los 5.8 s de silencio con
    streaming podrían ser un bloque `thinking`, porque `text_stream` entrega
    solo texto. Si es cierto, streaming **reduce** la espera en blanco, no la
    elimina. **Sin verificar** → ejercicio 8 (iterar los eventos crudos).
  - **Sesgo de orden que sigue sin medir:** la forma sin streaming corre primera
    y paga la apertura de la conexión. → ejercicio 9 (invertir el orden).
  - **El dialecto NO apareció aquí** (0 de 2, usted colombiano limpio). Y hay
    una diferencia de diseño: en este script el "español de Colombia" va en el
    **mensaje del usuario**, no en el `SYSTEM`. → **hipótesis nueva para el
    nivel 5**, con n=2 no prueba nada pero es medible.
  - El emoji 🕐 se imprimió sin reventar: `sys.stdout.reconfigure` del nivel 3
    trabajando en silencio.
- **Defecto mío corregido:** el docstring de `04_streaming.py` decía
  `Cuesta ~$0.02`. El costo real medido fue **$0.038**, casi el doble. Era un
  estimado mío sin medir — mismo patrón del "5x" del nivel 1. Corregido con el
  número medido y con la nota de que antes decía otra cosa.
- **`03_harness.py` NO se volvió a explicar** (ya estaba explicado en la sesión
  6). Se pasó directo a correr, como decía este archivo. Funcionó bien.
- **El dialecto, tercera y cuarta observación:** 1 de 3 en las dos corridas del
  harness, **pero en respuestas distintas** (con `s` en la 2ª, con `n` en la 1ª).
  El defecto es intermitente **y se mueve de sitio**. → L4.23.
- **Archivos actualizados:** `04-harness-real/README.md` (§4.3 con las dos
  corridas y el desglose del registro; §4.4 reescrita entera con las dos
  máquinas, la normalización, las dos hipótesis y el costo real; ejercicios 8 y
  9 nuevos), `04_streaming.py` (docstring), `LESSONS.md` (**L4.14–L4.23**, 10
  lecciones: las 6 candidatas de la sesión 6 más 4 de esta), `GUIDE.md` (§6 del
  registro: anotar siempre la hora + cómo leer el `.jsonl`; §4.d de streaming:
  `text_stream` solo da texto, y las dos trampas al medir tiempos).
- **EJERCICIO 9 HECHO — lo modificó él y salió el mejor resultado del nivel.**
  Invirtió el orden de `04_streaming.py` (streaming primero). Eso da cuatro
  datos: dos formas × dos posiciones.

  | | primera | segunda |
  |---|---|---|
  | sin streaming | 13.2 s | 12.3 s |
  | con streaming | 7.1 s | 5.8 s |

  1. **Por filas sale el sesgo:** +0.9 s y +1.3 s de castigo por ir primero.
     **Dos mediciones independientes del mismo fenómeno, casi idénticas** →
     abrir la conexión cuesta ~1 s. (Mi predicción antes de correr era "unos
     cientos de milisegundos": me quedé corto al doble.)
  2. **Por columnas sale el efecto limpio:** 6.1 s y 6.5 s. **La ventaja real
     del streaming es ~6.3 s, no los 7.4 s medidos con el experimento sesgado.**
     El control no tumbó la conclusión: **la corrigió, un ~15%.**
  3. → **L4.24**, y la técnica generalizable: cuando la posición contamina una
     medición, corre las dos cosas en las dos posiciones y lee filas y columnas.
- **CORRECCIÓN MÍA, encontrada por esta corrida.** En §4.4 yo había escrito
  *"con streaming se genera más texto por segundo"* con los datos de una sola
  corrida (52.3 vs 58.6 tok/s). La corrida invertida dio **56.6 vs 52.8 — al
  revés**. Las cuatro llamadas caen entre 52 y 59 tok/s: **era ruido y yo le
  puse dirección.** Es L1.13 disfrazada de aritmética: normalizar arregló que
  las magnitudes fueran comparables, pero **no arregla que n=1**. Corregido en
  el README y en L4.22, que ahora tiene las dos mitades.
- **El dialecto sigue limpio: 0 de 4** en el script de streaming. Y no solo
  evita el rioplatense — elige léxico colombiano: *"un **tinto**"*, *"la
  **plata**"*, *"el **freno de mano**"*. Marcador actualizado: `SYSTEM` 3 de 9,
  turno del usuario 0 de 4. Sigue sin probar nada (prompts distintos), pero
  aguantó otra corrida.
- **EJERCICIO 8 HECHO.** Escribió `04b_eventos.py` (archivo nuevo, no toca el
  script original) que itera el stream **crudo** con cronómetro.
  - **Defecto mío en el código que le dicté, atrapado antes de correr:**
    `messages.stream()` no es el stream pelado — es un ayudante que además de
    los eventos de la API emite **los suyos propios, uno por pedazo**
    (`text_stream` está hecho con esos). Mi rama `else` los imprimía: ~800
    líneas de ruido tapando los 4 renglones que importaban. Arreglado
    contándolos con prefijo `sdk:` en vez de imprimirlos. **Mismo patrón del
    `[:80]`, en espejo: allá el print escondía el dato cortándolo, aquí lo
    habría ahogado.**
  - **Hipótesis CONFIRMADA en el mecanismo:** `thinking` a los 1.97 s, cierra a
    las 4.22 s, `text` empieza a las 4.23 s. `content` final = `['thinking',
    'text']`. `text_stream` no podía dar nada antes porque **no existía texto**.
  - **Pero INCOMPLETA, y ese es el hallazgo:** `message_start` no llegó hasta
    los **1.95 s**. El silencio son dos tramos — 1.95 s de "nada todavía" y
    2.28 s de thinking. **El thinking es la mitad.** → L4.25.
  - **El ~1 s de apertura de conexión del ejercicio 9 vive dentro de esos
    1.95 s.** El número de un experimento apareció dentro de otro.
  - **Explica la variación que nunca entendimos:** "primera palabra" dio 8.6,
    5.8, 7.1 y 4.23 s. **El silencio dura lo que dure el razonamiento de esa
    corrida**, y eso no es determinista (L3.14). Esta corrida pensó poco (el
    resumen es una sola frase) y por eso arrancó a los 4.23 s. No fue la red.
  - **Costo invisible:** 654 tokens de salida para ~200 palabras (~350 tokens).
    Unos **300 fueron razonamiento facturado**. Y las corridas anteriores lo
    pagaban igual (691, 814, 802, 696) con `display` en `"omitted"`. **El
    parámetro decide si te lo enseñan, no si ocurre ni si se cobra.** → L4.26.
  - Detalles nuevos: 1.8 s entre que el bloque `thinking` se anuncia y llega su
    primer pedazo (hay huecos reales aun con el stream crudo), y apareció
    `signature_delta` — los bloques `thinking` vienen **firmados** para poder
    verificar que no los modificaste al devolverlos.
- **Métricas nombradas** (lo preguntó él al final, y pidió que quedaran
  registradas para conocerlas): **TTFT** (*Time To First Token*), **TPOT**
  (*Time Per Output Token*), **ITL** (*Inter-Token Latency*) y **latencia
  end-to-end**, más **TTFB** como la métrica de redes que no hay que confundir.
  Quedaron en **dos sitios a propósito**: `GUIDE.md` §4.d como referencia rápida,
  y `04-harness-real/README.md` §4.4 como lección, **con sus propios números al
  lado de cada nombre** (que es como se aprende un término, no como lista suelta).
  Incluye la fórmula `total = TTFT + (tokens × TPOT)` y la advertencia de los
  **dos TTFT** cuando el modelo razona (1.97 s el del sistema, 4.23 s el que ve
  el usuario).
- **Auditoría de cierre pedida por él** ("revisa que todo esté listo"). Aparecieron
  4 huecos, los 4 míos, todos corregidos:
  1. `GUIDE.md` §4.d seguía diciendo *"hipótesis con buena pinta, sin verificar"*
     del thinking — ya estaba medido. **Es la regla de la sesión 3: al cambiar
     una afirmación, buscarla en TODOS los archivos.**
  2. `GUIDE.md` decía "1.4x y 2.3x de adelanto" — números del experimento
     sesgado. Corregido a ~6.3 s con el orden controlado.
  3. La sección *"Lo que ya sabes"* del README del nivel 4 tenía el resumen
     viejo, sin nada de los ejercicios 8 y 9. **Exactamente el hueco de la
     auditoría de la sesión 3, repetido.**
  4. **L4.23 había quedado escrita DESPUÉS de L4.26** (yo inserté las nuevas en
     el sitio equivocado). Reordenado.
  - También: la cabecera de este archivo decía "10 lecciones (L4.14–L4.23)"
    cuando ya son 13 (L4.14–L4.26). Y L4.12 quedó con una nota que apunta a los
    números corregidos de L4.24.
- Costo del estudiante en la sesión: **~$0.17** ($0.0323 + $0.0328 + $0.038 +
  ~$0.04 del ejercicio 9 + ~$0.017 del ejercicio 8). Es la sesión más cara hasta
  ahora, por las respuestas largas del streaming.

**NIVEL 6b NUEVO — pedido por el estudiante al final de la sesión.** Preguntó si
el curso contemplaba *(1) multi-agente con memoria persistente* y *(2) multi-agente
con Skills*. Al revisar el repo:

1. **"Memoria persistente" aparecía UNA vez en todo el repo**: como palabra suelta
   en la celda "Concepto nuevo" del nivel 8. Sin sección, sin ejercicios, sin nada.
   **Es el mismo defecto que observabilidad en la sesión 6** — nombrada de pasada
   dentro de una lista y no desarrollada. Segunda vez que aparece el patrón.
2. **"Skills" no aparecía en ningún archivo.** Hueco completo, cero menciones.

**Corrección conceptual que se le dio, y que decide la ubicación:** ninguna de las
dos es un tema multi-agente. Memoria persistente es que el agente recuerde
**después de que el proceso se cierra**; Skills es conocimiento empaquetado que el
modelo **carga solo cuando le hace falta**. Un agente solo ya necesita las dos. El
multi-agente las *amplifica*, pero aprenderlas ahí sería mezclarlas con
orquestación — dos cosas nuevas a la vez.

**Y sale un tercer hueco de ahí:** el nivel 2 enseñó que el historial crece
*dentro de una corrida*. **Nadie cubría qué pasa cuando el programa termina.**
Memoria persistente es la continuación natural de esa pregunta, y estaba
huérfana.

**Decisión (la eligió él entre tres opciones): nivel `6b — Memoria persistente y
habilidades`**, después de TypeScript y antes de producción.

- Se construye **sobre su propio agente de divisas** del 5b, ya portado en el 6.
- Va antes del 7 porque ahí el agente pasa a tener usuarios reales y "recordar a
  cada usuario" deja de ser curiosidad y se vuelve requisito.
- Se usó sufijo `b` en vez de renumerar: **renumerar costó 12 referencias vivas en
  la sesión 6** y no vale la pena repetirlo.

**Archivos actualizados por el cambio:** `README.md` (fila nueva en el mapa +
sección *"Memoria persistente y habilidades (nivel 6b)"* + la celda del nivel 8
ahora dice *"memoria y skills **compartidas**"*), `CLAUDE.md` (las dos menciones a
"el mapa de los 9 niveles"), y este archivo.

⚠️ **Cuando se llegue al 6b: verificar la API antes de escribir nada.** Memoria y
Skills son de las partes que más rápido cambian del SDK. Es la regla de la sesión
3 (afirmar "es gratis" sin comprobarlo) y la misma nota que ya tiene el 5b con
sus dos URLs.

### Sesión 8 — 2026-07-29

**NIVEL 5 ARRANCADO.** Se creó `05-evaluacion/` con el README (§5.0) y cuatro
scripts, **los cuatro corridos por el estudiante**. Se cerró la duda que venía
abierta desde el nivel 3.

**Lo primero que pidió, y hay que anotarlo como método:** antes de escribir una
línea de código preguntó *"explícame qué es la evaluación, para qué sirve, qué
aporta, en qué momento se hace"*. Y después: *"¿todo esto va a quedar
registrado?"*. Por eso §5.0 del README se escribió **antes** que cualquier
script, no al final.

**Orden del nivel, elegido por él:** duda del dialecto → evals deterministas →
LLM-as-judge.

#### Los cuatro scripts

- **`00_probar_detector.py`** — prueba los detectores **sin llamar a la API**.
  16 casos, $0.00. Salió **idéntico en las dos máquinas**, como los errores del
  nivel 4. Es un eval determinista de verdad, aunque todavía no se llame así.
- **`01_contar.py`** — el mismo prompt N veces, con detector de rioplatense.
- **`02_contar_v2.py`** — la versión corregida + detector de tratamiento.
- **`03_contar_v3.py`** — tres versiones intercaladas (control / prohibición /
  posición), con rangos de confianza.

#### Experimento 1 (v1): 0 de 10 — y el error de diseño era mío

Preguntó *"¿qué ropa me pongo hoy en Bogotá si está lloviendo?"* a un modelo
**sin herramientas**. Resultado: **0 de 10**, contra un histórico de 3 de 9.

- **La causa: 6 de las 10 respuestas se gastaron disculpándose** (*"no puedo
  consultar el clima"*). El modelo nunca llegaba a dar consejo, que es donde el
  defecto vive. Yo había escrito en el código que la pregunta "provoca consejo".
  Provoca consejo **y también** disculpa, y no lo pensé.
- Es el error de `03_recortar.py` del nivel 2 con otra ropa: una prueba que
  corre, que no revienta, y que no prueba lo que dice probar.
- → **`0 de 10` no refuta `3 de 9` si no midieron lo mismo.** Un experimento que
  cambia las condiciones y sale limpio no demuestra que arreglaste algo:
  demuestra que dejaste de mirar donde estaba.
- **Hallazgo lateral que nadie buscaba:** al leer las 10 respuestas se vio que el
  modelo trataba de **tú** en 4 y de **usted** en 5, con el mismo prompt. De ahí
  salió el segundo detector. **Contar N veces te enseña cosas que no fuiste a
  buscar.**
- **Novena confirmación de la entrada determinista:** las 10 dieron 102 tokens.
  Es la más fuerte hasta ahora (antes eran 3 o 4 datos, aquí 10 de 10).

#### Dos bugs míos en los detectores, cazados antes de gastar

1. **`normalizar()` borraba la señal que buscaba.** `"Llevá"` y `"Lleva"` se
   diferencian solo en la tilde, y yo quitaba tildes antes de comparar. El
   detector habría marcado la forma **colombiana correcta** como rioplatense.
   Arreglo: dos listas, y los imperativos voseantes se buscan **sin normalizar**.
   → Mismo patrón del `[:30]` del nivel 1 y del `[:80]` del nivel 6: **el
   preprocesamiento destruye el dato antes de que lo veas.**
2. **`margen()` mentía en los extremos.** Con 0 de 30 devolvía `±0.0`, o sea
   *"defecto eliminado, con certeza total"*. Falso: un defecto del 5% tiene ~21%
   de probabilidad de no salir ni una vez en 30. Arreglado con la **regla de
   tres** (si no viste ninguno en n intentos, el tope al 95% es 3/n) y renombrado
   a `rango()`, porque dejó de ser simétrico. → **El peor bug posible en un eval:
   no revienta, solo miente, y miente con cara de matemática.**

Los dos se encontraron **corriendo las pruebas offline antes de pagar nada**.
Ese hábito ya se pagó solo dos veces en una sesión.

#### Experimento 2 (v2): 9 de 30 — el defecto vive en UN verbo

Con el clima **dado** en la pregunta, el modelo entra directo a aconsejar.

- **9 de 30 = 30%**, contra el histórico de 3 de 9 = 33%. **Dos estimaciones
  independientes, condiciones distintas, y coinciden.** El defecto pasó de
  sospecha a número reproducible.
- **EL HALLAZGO DEL NIVEL.** Casi todas las respuestas dicen lo mismo; lo único
  que baila es cómo conjuga el primer verbo:

  | forma | cuántas | qué es |
  |---|---|---|
  | `ponte` | 18 de 30 | tú, colombiano correcto |
  | `ponete` | **9 de 30** | **rioplatense — el defecto entero** |
  | `póngase` | 2 de 30 | usted |

  **Los 9 rioplatenses son exactamente las 9 respuestas con `ponete`**, y los 2
  ustedeos son los 2 `póngase`. Los 3 `llevá` acompañan siempre a un `ponete`.
  → El fantasma que se perseguía desde el nivel 3 no es "a veces habla
  argentino": es **una bifurcación en una sola palabra**, entre tres formas que
  son todas español correcto. Por eso ningún `SYSTEM` que diga "español de
  Colombia" lo mata: las tres *son* español.
- Y explica la v1: allí la respuesta empezaba con *"no puedo consultar…"*, así
  que **la bifurcación nunca ocurría**.
- **Los 2 `mixto` son reales**, verificados leyendo el texto completo: *"**Ponte**
  una chaqueta… **Lleve** paraguas"*. Cambia de tú a usted entre la primera y la
  segunda frase, **las dos veces en el mismo sitio**.
- Predicciones del estudiante: rioplatense 4 (salió 9), mixto 2 (**salió 2,
  clavado**), usted 4 (salieron 2).
- Costo $0.1273 contra mi estimación de $0.14. Le pegué, después de fallar dos.

#### Experimento 3 (v3): el control NO se replicó

Tres versiones **intercaladas** A,B,C,A,B,C… (la técnica del ejercicio 9 del
nivel 4, aplicada a tres), 30 corridas cada una, $0.3191.

- ⚠️ **A (control) dio 3 de 30 = 10%, no el 30% de la v2.** Mismo prompt exacto
  (entrada 108 en las dos), misma máquina, veinte minutos después.
  - Los rangos se tocan (13.6–46.4 vs 0–20.7), así que **el azar basta**: no hace
    falta suponer que cambió algo del lado de Anthropic.
  - **Pero la lección es grande: con N=30 el mismo prompt dio 30% y 10%.**
    N=30 no era suficiente, y solo se supo **porque había un control**.
  - Como el prompt es idéntico, las 60 corridas se pueden juntar:
    **12 de 60 = 20%, entre 9.9% y 30.1%.** Es la mejor estimación que hay.
  - → **El control no es relleno. Es lo que te dice si tu regla de medir sigue
    siendo la misma regla.**
- **La métrica binaria no tenía poder; la fina sí.** El script declaró
  correctamente "no demostrado" para *¿hubo rioplatense sí/no?*. Al preguntar en
  cambio *¿qué forma del verbo usó?* —que tiene señal en las 30 respuestas y no
  solo en las 3 malas— todo se separa:

  | | dijo `ponte` | rango |
  |---|---|---|
  | A | 19/30 = 63% | 46–81% |
  | B | **30/30 = 100%** | 90–100% |
  | C | 28/30 = 93% | 84–100% |

  A vs B **separados**. A vs C **separados**. B vs C **se solapan**.
  → **No hizo falta gastar más: hizo falta medir mejor.** Mismos datos, mismo
  dinero, otra pregunta. Si tu métrica solo mira los fallos, tiras la información
  de los aciertos.
  - Salvedad anotada: elegir la métrica después de ver los datos es una trampa
    clásica. Aquí no aplica porque `forma_verbal()` se escribió **antes** de
    correr la v3, con los datos de la v2. Pero había que decirlo.
- **La hipótesis del estudiante (nivel 4) sobrevive.** C —mover *"español de
  Colombia"* del `SYSTEM` al turno del usuario— funciona, y es indistinguible de
  prohibir el voseo con nombre propio. **Lo que NO se demostró es que C sea
  mejor que B**: se solapan.
- **El premio es de ingeniería:** B cuesta **+80 tokens de entrada por llamada**
  ($0.40 por cada 1.000 llamadas, para siempre); C cuesta **+3** ($0.015).
  **26x más barato por el mismo efecto.** Mismo tipo de costo permanente que el
  menú de `tools` del nivel 3.

#### Paso 2 — Evals deterministas del harness (`04_evals_harness.py`)

**24 evals, $0.00, idénticos en las dos máquinas.** Prueban los seis frenos del
nivel 4: dinero, permisos, candado de ruta, coherencia, registro y topes.

- **Muro previo, y es lección:** `03_harness.py` **no se podía importar sin
  ejecutarse** (no tenía `if __name__ == "__main__"`). Cargarlo para probar sus
  piezas creaba la caja, hacía las 3 preguntas, gastaba $0.03 y esperaba un
  `input()`. **Arreglado**: todo lo ejecutable se movió dentro de `main()`.
  → **Para poder probar tu código, tiene que poder cargarse sin ejecutarse.**
- **AGUJERO DE SEGURIDAD REAL encontrado por un eval**, y es el hallazgo del
  paso: el permiso decía `if respuesta.startswith("s")`, así que **cualquier
  palabra que empezara por `s` autorizaba el borrado** — incluidas `salir`,
  `stop`, `suspende`, `sal de ahí`. **Las palabras para abortar en español
  empiezan por s.** El freno se abría con la palabra que uno escribe para
  cerrarlo.
  - **Lo que falló de fondo:** *denegar por defecto* estaba perfecto en
    `PERMISOS.get(nombre, "prohibir")` y **no** en la lectura del teclado,
    **tres líneas más abajo, en la misma función**. Nadie lo vio en dos sesiones
    leyendo ese archivo. → L5.14.
  - Arreglado: `if respuesta in {"s", "si", "sí"}`.
  - Lo encontró el caso que probaba **13 teclas hostiles**. Probar `"s"` y `"n"`
    habría pasado. → **Un eval vale por sus casos hostiles.**
- **Defecto mío de presentación, cuarta vez del mismo patrón:** los evals
  llamaban a `pedir_permiso()`, que imprime, y 20 líneas de `PERMISO:` ahogaban
  la salida. Arreglado capturando `stdout` — **y guardándolo para mostrarlo solo
  si el caso falla**. Callado cuando va bien, hablador cuando se rompe.

#### Paso 3 — El juez (`05_juez.py`), y por qué perdió contra el `if`

- **Primer intento: detectar dialecto. Tres rúbricas, empeorando: 83% → 75% →
  42%** de acuerdo con el detector determinista.
  - v1 falló porque no tenía **regla de desempate**: el texto era una mezcla real
    (`ponete` junto a `buso`, `harto`, `sombrilla`) y el juez desempató por
    mayoría. **El fallo era de la rúbrica, no del juez.** → L5.16.
  - v2 y v3 fallaron porque el juez **no distingue `lleva` de `lleve` ni `ponte`
    de `ponete`** — una letra.
  - **Se paró de tunear a propósito**, porque seguir ajustando hasta que el
    número quedara bonito es la trampa que el propio §5.3 advierte.
  - → **Si un `if` puede responder la pregunta, no uses un juez.** Distinciones
    ortográficas: `if`. Comprensión del contexto: juez. El detector gana en
    costo ($0 vs cuesta), estabilidad (100% vs 92%) y acierto.
- **Reorientado a donde el `if` SÍ se había rendido:** la consistencia del
  tratamiento, donde `le`/`se`/`su` se habían dejado fuera por ambiguos.
- **Balance sobre 120 respuestas:** cazó **3 de 3** mezclas conocidas, encontró
  **4 reales nuevas** y soltó **36 falsas alarmas**. Una de cada seis alarmas era
  real.
  - Las 4 reales eran todas `"No olvide el paraguas"` junto a `"ponte"` —
    **ustedeo que no estaba en ninguna lista y que no se me habría ocurrido
    buscar.** Eso es lo que un `if` no puede hacer.
  - → **Un juez es buen filtro y mal decisor.** 120 respuestas → marca 43 → lees
    43 → encuentras 4 defectos invisibles.
- **LO MÁS GRAVE: el juez fabrica evidencia.** En textos que decían `Lleva`
  (tuteo consistente), citó `['ponte','te','lleva','lleve']` — **`lleve` no
  estaba en el texto** — para sostener una mezcla inexistente. Tres veces.
  En total **9 de 451 citas (2%) no estaban**, y eran justo las que sostenían los
  veredictos. → L5.18.
  - **Se descubrió solo porque la rúbrica pedía `"palabras"` además de la nota.**
    Con solo el número, habríamos creído "43 respuestas con mezcla".
    → **Un juez que solo devuelve una nota es incomprobable.**
  - ⚠️ **Mi primera comprobación de las citas tenía el bug de la tilde** (comparaba
    `pongase` contra `póngase`) y estuvo a punto de acusar al juez de inventarse
    lo que sí había dicho. **Cuarta aparición del mismo patrón en una sesión.**
- **Estabilidad:** el juez repitió la misma nota en 6 de 6 en la primera versión
  — **100% consistente y equivocado**. → **Consistencia no es corrección**, y por
  eso correr el mismo modelo dos veces no protege de nada (L5.17).
- **Decisión de diseño anotada:** elegí Haiku razonando "clasificar es tarea
  fácil". **Los datos lo contradicen** y quedó convertido en el ejercicio 1.

#### Tres preguntas conceptuales suyas (respondidas, vale la pena conservarlas)

1. **"¿Esto son guardrails?"** — No exactamente: el **guardrail** es la
   protección (vive en el agente, corriendo); el **eval** es la prueba de que
   funciona (vive en el banco de pruebas). El freno del carro vs la revisión
   técnico-mecánica. De los seis frenos del nivel 4, cinco son guardrails; el
   registro **no** (no impide nada, solo cuenta: eso es observabilidad).
2. **"¿Sería mejor un juez de otro proveedor?"** — Conceptualmente sí para la
   autopreferencia, pero **lo primero es validar contra tus propias etiquetas**,
   no diversificar proveedores. Un juez de otra empresa sin validar sigue siendo
   una opinión sin validar.
3. **"Con 5 agentes, ¿hay que evaluar cada uno?"** — Sí, y el número que lo
   justifica: cinco agentes al 90% dan `0.9^5 = 59%` de acierto en el sistema.
   Aparece además el problema de **atribución** (¿cuál de los cinco falló?), que
   es lo que convierte el registro del nivel 4 en obligatorio. El resto, nivel 8.

#### Costo del estudiante en la sesión

$0.0459 (v1) + $0.1273 (v2) + $0.3191 (v3) + $0.1268 (juez Haiku)
= **~$0.62**. La sesión más cara del curso, con diferencia, y la primera en que
dos preguntas suyas se responden con evidencia en vez de con una explicación
plausible.

⚠️ **CORREGIDO en la sesión 9:** esta línea decía *"~$0.06 (juez, 140 llamadas
Haiku)"* y el total *"~$0.55"*. Los **$0.06 eran un estimado mío sin medir**; el
JSON de la corrida dice **$0.1268**, más del doble. Total real ~$0.62. → L5.23.

**Nota de costo que vale la pena recordar:** el juez calificó texto **ya
generado**, leído de `resultados/*.json` — los $0.49 de generarlo ya estaban
pagados, así que juzgarlo costó una fracción. → L5.20.

### Sesión 9 — 2026-07-29

**EJERCICIO 1 DEL NIVEL 5 HECHO.** Corrió `05_juez.py` con `MODELO_JUEZ =
"claude-sonnet-5"` sobre las mismas 120 respuestas. Fue el ejercicio que más
enseñó del nivel, como estaba previsto — pero **enseñó cosas distintas de las
que yo había anticipado**, y las tres correcciones son mías.

#### El resultado

| | Haiku 4.5 | Sonnet 5 |
|---|---|---|
| acuerdo con el detector | 66.4% | **95.8%** |
| marcó como mezcla | 43 de 120 | **8 de 120** |
| **mezclas reales cazadas** | **4 de 4** | **4 de 4** |
| falsas alarmas | 39 | 4 |
| precisión | 9% | **50%** |
| citas fabricadas | 9/451 (2.0%) | **1/323 (0.3%)** |
| estabilidad | 18/20 | **20/20** |
| sin formato válido | 1 | **0** |
| costo real | $0.1268 | **$0.3060** |

- **El hallazgo central, y no es el que la pregunta del ejercicio buscaba:**
  los dos jueces cazaron **las mismas 4 mezclas reales**. El caro **no encontró
  nada** que el barato se perdiera. Lo que cambió fue el trabajo humano: 43
  respuestas que leer contra 8. **$0.18 más = 35 respuestas menos.** → L5.21.
  Yo había escrito el ejercicio preguntando *"¿sube el acuerdo?"*, como si la
  pregunta fuera de exactitud. Era de **cuánto te queda por leer**.
- **Sonnet TAMBIÉN fabricó una cita** (`lleve` por `lleva`, la misma
  alucinación de Haiku) y en otra alarma **se contradijo dentro de su propia
  `razon`**: *"Mezcla tuteo (ponte) con ustedeo (lleva es tuteo, pero revis..."*.
  → L5.22: un modelo mejor vuelve el defecto **raro**, no lo elimina — y eso es
  más peligroso, porque desactiva la costumbre de comprobar.

#### Tres correcciones, las tres mías

1. **BUG REAL en `05_juez.py`.** Los precios estaban quemados a mano con los de
   Haiku (`PRECIO_ENTRADA = 1.00 / 1_000_000  # Haiku`). Al cambiar el modelo
   **el costo impreso quedó a la mitad**: dijo `$0.1530`, real `$0.3060`.
   Sin excepción, sin aviso, y en la línea que dice `COSTO REAL`.
   **Arreglado**: diccionario `PRECIOS[MODELO]` que **revienta** si el modelo no
   está; el precio aplicado ahora se imprime al lado del total y se guarda en el
   JSON junto con los tokens (un costo suelto no se puede auditar). → L5.23.
2. **Mis dos estimados de costo eran inventados.** El README decía *"~$0.18 en
   vez de ~$0.06"*. Medido: **$0.306 y $0.127**. La *razón* entre modelos quedó
   cerca (~2.4x contra el 3x que dije); las **magnitudes** las inventé las dos.
   Mismo patrón del `"55x"` (nivel 1) y del `"~$0.02"` (nivel 4).
3. **Un cuarto bug del preprocesamiento, cometido por mí en vivo al analizar sus
   datos.** Escribí `if 'olvide' in texto`, y `'olvide' in "no olvides"` es
   `True` — pero `"No olvides"` es tuteo **correcto**. Dio **46** mezclas; con
   `\bolvide\b` da **4**. **El 91% del hallazgo era el bug.** Cuarta aparición de
   la misma familia (`[:30]`, `[:80]`, `normalizar()`, `in`). → L5.24, con tabla
   de las cuatro.

#### Verificado, no recordado

Se comprobaron los precios en la documentación oficial antes de tocar el código
(regla de la sesión 3). Apareció una letra pequeña que yo no tenía: **Sonnet 5
está en precio de lanzamiento ($2/$10 por millón) hasta el 2026-08-31**; desde
septiembre, $3/$15, y esa misma corrida costará **~$0.46** sin cambiar una
línea. Está escrito **en el código con la fecha**, no en la memoria de nadie.

#### Archivos actualizados

- `05_juez.py` — diccionario `PRECIOS` + guarda que revienta + precio impreso +
  `precio_usado` y `tokens` en el JSON.
- `05-evaluacion/README.md` — **§5.6 nueva** (la comparación entera, las tres
  afirmaciones caídas, el cuarto bug, y la conclusión honesta); nota en §5.5
  aclarando que sus números son los de Haiku; ejercicio 1 marcado ✅ con
  resumen; ejercicio 4 reescrito y ascendido.
- `LESSONS.md` — **L5.21–L5.24** (4 nuevas; el nivel 5 va por 24).
- `GUIDE.md` §8.j — tabla de costos con los números **medidos** en vez de los
  estimados, + cómo atar precios al modelo, + la caducidad del precio de
  lanzamiento.
- `PROGRESO.md` — este bloque, la cabecera, el costo de la sesión 8 corregido, y
  el punto de "los 43 marcados" cerrado.

#### NIVEL 5 CERRADO + APIs del 5b reverificadas

Se le ofrecieron los ejercicios que quedaban y **eligió cerrar el nivel 5 y
pasar al 5b**. También se le ofreció arreglar los 6 scripts con el precio suelto
y prefirió avanzar (queda anotado arriba como pendiente vivo).

**Las dos URLs del 5b se reverificaron con `curl` el 2026-07-29**, cumpliendo la
nota que dejó la sesión 8. Las dos responden **HTTP 200**:

| Fuente | URL | 29 jul | 28 jul |
|---|---|---|---|
| Mercado | `https://open.er-api.com/v6/latest/USD` | 3.206,17 | 3.215,61 |
| TRM oficial | `https://www.datos.gov.co/resource/32sa-8pi3.json` | 3.205,87 | 3.205,80 |

- La TRM acepta `?$order=vigenciadesde DESC&$limit=N` y devuelve los campos
  `valor`, `unidad`, `vigenciadesde`, `vigenciahasta`. La API de mercado sigue
  trayendo `time_last_update_utc` / `time_next_update_utc`.
- **HALLAZGO NUEVO, y corrige un supuesto de la sesión 8:** la brecha entre las
  dos fuentes **no es fija**. El 28 de julio eran ~10 pesos; el 29 son **0,30
  pesos**. La sesión 8 anotó *"no coinciden (~10 pesos)"* con **una sola
  observación** detrás. Lo estable es **que son fuentes distintas**, no cuánto se
  separan. → El material del 5b debe enseñar *"pueden no coincidir"*, nunca una
  magnitud. Es L1.13 otra vez, atajada antes de escribir nada.
- El hueco del fin de semana sigue vivo en los datos (la TRM del 25 valió hasta
  el 27): el caso de prueba no hay que inventarlo.

#### Método del estudiante — confirmado otra vez

- **Pidió las dos cosas** ("arregla el bug y escribe el análisis") en vez de
  elegir una. Prefiere cerrar el ciclo completo antes de pasar a lo siguiente.
  **Ofrecerle las dos juntas en vez de hacerle escoger.**
- Cuando decide avanzar, avanza: no se queda puliendo pendientes opcionales.
  Anotarlos como vivos y no insistir.

### Sesión 10 — 2026-07-29

**NIVEL 5b ARRANCADO.** Y arrancó como él pidió: **explicación primero, cero
teclado**. Los tres temas que había dejado anotados se explicaron antes de crear
un solo archivo.

#### Lo que se hizo

- **Carpeta creada por él:** `05b-proyecto/` en la raíz, hermana de las otras.
  Se le explicó **por qué ahí y no dentro de `05-evaluacion/`**: además de que es
  un nivel propio, `parent.parent / ".env"` deja de encontrar la key si se anida
  un nivel más. Creó los 4 archivos vacíos (`README.md`, `herramientas.py`,
  `agente.py`, `evals.py`).
- **`README.md` del nivel escrito completo** (§5b.0 a §5b.5): qué es un proyecto
  integrador, la tabla de piezas heredadas nivel por nivel, las 5 herramientas con
  *lo difícil de cada una*, la estructura de archivos con su porqué, las dos APIs
  con la advertencia de la brecha variable, y **el plan de los 10 pasos con quién
  escribe cada uno**.
- **Decisión de estructura, dictada y con su razón:** `herramientas.py` separado de
  `agente.py`. La razón es la del nivel 5 (`00_probar_detector.py`): **separar lo
  que se puede probar gratis de lo que cuesta dinero probar.** De las 5
  herramientas, 3 necesitan internet y 2 no.

#### `convertir()` — la primera función que escribe él solo

Se le planteó como **decisión de diseño**, no como dictado: ¿la tasa la busca la
función (opción A) o se la pasan por parámetro (opción B)? **Eligió B** y contestó
bien las tres preguntas de control (no se puede probar sin internet con A; el
error de la tasa y el de la multiplicación solo se distinguen en B).

- **Se le completó la respuesta 2**, que tenía a medias. Dijo *"yo le paso el
  número"* — cierto para `evals.py`, pero cuando el agente corre **el que consigue
  la tasa es el modelo**, encadenando dos herramientas en tres vueltas
  (`obtener_tasa` → `convertir` → responder). **Nadie programa esa cadena**; solo
  existen las dos `description`. Es el nivel 3 otra vez. → Su opción B no solo hace
  la función probable gratis: **le da al modelo algo que decidir.**
- **Se le enseñó a construir el `dict` de retorno**, que era lo que no sabía hacer.
  El punto que confunde a todos: `"monto": monto` son dos cosas distintas (etiqueta
  fija vs valor que cambia).

#### Los cuatro defectos de su primera versión, y qué lección tenía cada uno

Los encontró él corrigiéndolos, no se los reescribí. **Tres de los cuatro son
patrones que ya aparecieron antes en el curso:**

1. **Validaba solo `a`, no `de`.** Y salió el *por qué* se escapa, que es lo
   valioso: `de` es **el único parámetro que no participa en ningún cálculo** —
   entra y sale directo al `dict`. → **Los parámetros que solo se transportan son
   los que nadie valida.** No fallan, no dan señales, y son los que dejan pasar la
   basura. Y es el peor: si `de` está mal, la multiplicación es perfecta y el
   resultado falso. *(Se le pasó una vez más incluso después de señalarlo — se
   corrigió a la tercera pasada.)*
2. **Dos listas que tenían que coincidir** (`MONEDAS` y `DECIMALES`) y nada las
   obligaba. **Es L5.23 exacta** — el precio suelto al lado del `MODELO`: hoy no
   miente, miente el día que cambies uno solo. Se resolvió con **una sola fuente de
   verdad**: `MONEDAS = tuple(DECIMALES)`. Eligió esa opción sobre la de validar
   contra `MONEDAS`.
3. **`DECIMALES` estaba declarado dentro de la función.** Dos razones para subirlo:
   `evals.py` no puede verlo, y `MAYÚSCULAS` es la convención de "constante del
   archivo" — una constante dentro de una función se contradice.
4. **La multiplicación estaba dos veces**, y la primera **calculaba antes de
   validar**. Hoy no duele (multiplicar no revienta), pero el hábito es el que
   importa: **primero se revisa, después se calcula.**

**Más un regalo:** su mensaje de error decía solo *"No manejo la moneda BTC"* —
que es **el 404 de la sesión 6**: repite lo que le mandaron y no dice qué hacer.
Se le recordó **quién lo va a leer** (el modelo, como `tool_result`) y lo cambió a
`f"... Solo: {', '.join(MONEDAS)}."`, que sí permite que se corrija solo en la
vuelta siguiente.

#### Pregunta suya que se volvió media lección: **`if` o `try/except`**

La hizo sin que nadie la provocara (*"¿podría ser un try except o un if? ayúdame
explicando"*). Se le dio con la analogía primero:

- **`if` = mirar antes de cruzar la calle.** La información está ahí antes de
  moverte.
- **`try/except` = ponerse el cinturón.** No sabes si va a haber choque, pero si
  hay, no te mata.
- **La pregunta que decide:** *¿puedes saber la respuesta antes de intentarlo?*
  Sí → `if`. No, depende de algo que no controlas → `try/except`. Y ese "algo" casi
  siempre es **internet, el disco, o lo que escribió un humano**.
- **Segunda razón, más práctica:** el `try/except` equivalente aquí habría envuelto
  tres operaciones en una línea, así que `except KeyError` no distinguiría cuál
  falló. → **Un `try` debe envolver lo menos posible.** Es el nivel 3 otra vez
  (*"lee la coordenada antes que la frase"*): un `try` ancho borra la coordenada.
- **Y se le dijo dónde SÍ lo va a usar:** el paso 6, las tres herramientas de
  internet. *No hay ningún `if` que te diga si internet va a funcionar dentro de
  200 ms.* Lo normal es tener **los dos en la misma función**: el `if` arriba
  revisando argumentos, el `try` abajo envolviendo la línea peligrosa.

→ **Candidata fuerte a lección del nivel** (L5b.x) cuando se cierre el 5b.

#### Un despiste que vale anotarlo

Me pegó la versión corregida en el chat, pero **el archivo en disco seguía con la
versión vieja** — no había guardado. Se detectó porque leí el archivo en vez de
creerle al chat. Si hubiera pasado en el paso 5, `evals.py` habría fallado sobre
código viejo y el rato perdido habría sido buscando un bug ya arreglado.
→ **Leer el archivo antes de opinar sobre él**, aunque me acaben de pegar el
contenido.

#### Costo de la sesión: **$0.00**

No se hizo ni una llamada a la API. Y eso **es el diseño del nivel, no una
casualidad**: los pasos 4 y 5 son gratis a propósito.

---

**Cambio de plan pedido por el estudiante (sesión 6).** Preguntó dos cosas que el
plan no cubría bien: *(1) ¿y los harnesses con orquestador y workers?* y
*(2) ¿dónde entran observabilidad, rúbricas y evaluación?* Al revisar el mapa
aparecieron tres huecos reales, dos míos:

1. El nivel 6 decía solo *"evals, casos de prueba, regresiones"* — eso cubre lo
   que se comprueba con un `if`, y **dejaba fuera las rúbricas / LLM-as-judge**,
   que es justo lo que hace falta para su propia duda del dialecto.
2. Observabilidad estaba **nombrada de pasada** en una lista del nivel 7, no
   desarrollada como pieza.
3. Al explicarle el nivel 5 (que no está escrito, solo planeado) salió una
   pregunta que yo no tenía resuelta: **si el nivel 5 pasa a TypeScript, ¿en qué
   lenguaje se hace el nivel 6?** Cualquiera de las dos respuestas tenía costo.

**Decisión: se intercambian los niveles 5 y 6.** Nuevo orden: harness →
**evaluación** → **TypeScript** → producción → multi-agente. Él eligió esta
opción entre tres que le planteé. Ver *Decisiones tomadas* para el porqué.

Archivos actualizados por el cambio de numeración (12 referencias vivas, buscadas
en todo el repo antes de editar — la regla de la sesión 3): `README.md` (mapa
nuevo + sección "Los tres temas que se preguntan siempre"), `CLAUDE.md`,
`LESSONS.md` (4), `GUIDE.md` (1), `03-primer-agente/README.md` (1),
`04-harness-real/README.md` (2), y este archivo.

**El nivel 8 también se precisó:** ahora dice *"Multi-agente: orquestador y
workers"*. La respuesta corta que se le dio, y que quedó escrita en el
`README.md`: **un orquestador es un agente cuyas herramientas son otros agentes**
— el bucle del nivel 3 anidado, por eso va al final.

---

**Nivel 5b propuesto por el estudiante (sesión 6).** Pidió un proyecto práctico
donde construya un harness con varias herramientas **desde un archivo vacío**,
con instrucciones paso a paso, hasta la evaluación.

- **Diagnóstico que lo justifica:** en 6 sesiones ha leído, corrido y analizado
  mis scripts — y muy bien: encontró dos bugs míos y corrigió un análisis mal
  atribuido. Pero **nunca ha empezado desde un archivo vacío**. Entender código y
  producirlo no son la misma habilidad, y hasta ahora solo se practica la primera.
- **Ubicación:** después del nivel 5 (evaluación), antes del 6 (TypeScript).
  Carpeta `05b-proyecto/` para que ordene bien. La eligió él y es correcta:
  cierra todo el Python de un tirón, y el nivel 6 pasa a portar **su** agente en
  vez del mío.
- **Formato elegido: mixto.** Dictado literal en lo mecánico (entorno, imports,
  estructura de carpetas); guiado en lo conceptual (bucle, frenos, evals), donde
  se dice *qué* y *por qué*, lo escribe él, y después se compara con mi versión.
  - ⚠️ **La razón del formato mixto, para no olvidarla:** el paso a paso dictado
    tiene el riesgo de que teclee sin pensar y termine con un agente que funciona
    y que no sabría rehacer. Sería el único nivel donde el código no pasó por su
    cabeza. Pero crear el `.venv` o escribir los `import` es mecánico y ahí
    dictarlo está bien. **Separar lo mecánico de lo conceptual.**
- **Tema elegido por él: agente de divisas y TRM.** COP ↔ USD, EUR, CAD en ambos
  sentidos, más TRM oficial de Colombia. Es mejor que las tres opciones que yo
  había propuesto, por cuatro razones:
  1. **Tiene verdad comprobable** — la conversión se verifica con una
     multiplicación. Casi ningún agente tiene ground truth; este sí. Los evals
     deterministas del nivel 5 salen solos.
  2. **Y también tiene el caso de rúbrica** — "¿dijo de qué fuente sacó la tasa?"
     no se comprueba con un `if`.
  3. **Trae la trampa central:** un LLM puede equivocarse multiplicando.
     **La herramienta calcula; el modelo solo decide a cuál llamar.** Y aquí se
     puede *medir* que pasa.
  4. Da para 5 herramientas de tipos distintos (API en vivo, cálculo puro, API
     con fecha, serie de tiempo, y una que escribe en disco y pide permiso).

### Verificado el 2026-07-28 (revisar de nuevo AL LLEGAR al 5b)

Las dos APIs son gratis y **sin llave**. Comprobadas con `curl`, no de memoria:

| Fuente | URL | Dato de hoy |
|---|---|---|
| Mercado | `https://open.er-api.com/v6/latest/USD` | 1 USD = 3.215,61 COP |
| TRM oficial | `https://www.datos.gov.co/resource/32sa-8pi3.json` | 1 USD = 3.205,80 COP |

Tres hallazgos que salieron de esa verificación y que ya son material del nivel:

1. **Las dos fuentes no coinciden (~10 pesos) y las dos son correctas.** Para una
   factura en Colombia la respuesta legal es la TRM; para saber cuánto te cobran
   de verdad, la del mercado. → *"¿A cuánto está el dólar?"* no tiene una sola
   respuesta correcta. Es material de rúbrica servido en bandeja.
2. **El plan gratis actualiza una vez al día.** La respuesta trae
   `time_last_update_utc` y `time_next_update_utc`, así que el agente **puede
   saber qué tan vieja es su información**. Obliga a dos piezas de harness real:
   caché y avisar de datos rancios. No lo busqué: venía en la respuesta.
3. **La TRM no cambia el fin de semana.** La de hoy vale del 28 al 28; la
   anterior valía **del 25 al 27**. Preguntar por un sábado es un caso de prueba
   que no hubo que inventar.

> ⚠️ Las URLs funcionaban el 2026-07-28. **Volver a comprobarlas antes de escribir
> nada encima** — es la lección de la sesión 3 (afirmar "es gratis" sin verificar).

---

**`03_harness.py` explicado (final de la sesión 6), pero NO corrido todavía.**
Se hizo en las tres partes acordadas y **no hay que repetirlo**:

1. *Los seis frenos*, planteados como "¿qué pasa si falta?" en vez de "¿qué
   hace?". La idea que los amarra: **ninguno de los seis confía en el modelo.
   El modelo decide qué hacer; tu código decide qué está permitido.**
2. *El recorrido por el código*, por zonas (A–G): la configuración arriba del
   todo, `PresupuestoAgotado` como error-que-no-es-error, el `**datos` de
   `anotar()`, la herramienta que atrapa su propio error y lo devuelve como
   texto, los tres detalles de los permisos, la llamada blindada y el bucle con
   tope.
3. *Qué se aprende*: la diferencia entre "funciona" y "es confiable"; dónde vive
   cada decisión; **denegar por defecto**; que los errores se degradan en tres
   capas en vez de propagarse; y que estas seis piezas son lo más directamente
   aplicable a su SaaS de todo el curso.

Dos cosas que se le señalaron y que conviene retomar cuando lo corra:

- **Trampa latente que él podría cazar:** si alguien pusiera
  `REINTENTOS_PROPIOS = 0`, el `for` de `llamar_modelo()` (línea 247) no se
  ejecutaría nunca y la función devolvería `None` en silencio. Hoy no molesta
  —está en 3— pero es del mismo tipo que el contador roto de `01_chat.py`.
- **Denegar por defecto** (`PERMISOS.get(nombre, "prohibir")`) se presentó como
  principio general, no como detalle: diseñar para que **el olvido falle hacia
  el lado seguro**. Vuelve a aparecer en el nivel 7.

---

**Sesión 6 cerrada aquí.** Lo hecho: scripts 1 y 2 corridos y analizados, un
defecto de presentación arreglado y verificado, README §4.1 y §4.2 actualizados,
el mapa del curso reordenado, un nivel nuevo (5b) diseñado con sus APIs
verificadas, y `03_harness.py` explicado.
Costo del estudiante en la sesión: ~$0.0013 (solo la llamada real del script 2).

---

### Sesión 11 — 2026-07-30

**PASOS 4 y 5 DEL NIVEL 5b CERRADOS.** El detalle completo está arriba, en la
cabecera del 5b (no se duplica aquí). Resumen de lo que se produjo:

- **`guardar_reporte()` escrita por él**, con 3 frenos y la **allowlist** razonada
  desde cero (la analogía del portero A/B). Costo: $0.00.
- **`herramientas.py` reorganizado** a petición suya (*"que se vea más
  profesional"*), con el **contrato** del archivo escrito arriba. Se corrió la
  misma prueba antes y después: comportamiento idéntico.
- **`evals.py` completo: 26 casos, 2 bucles, 0 fallos, $0.00 y sin red.**
  16 casos de `convertir()` + 10 de `guardar_reporte()`.
- **Cinco defectos reales encontrados y arreglados** en `convertir()`: 4 `TypeError`
  que tumbaban el bucle del agente, la tasa 0 que devolvía `0`, el monto negativo,
  los booleanos colándose como números, y el `4.0` en pesos.
- **Un defecto encontrado y NO arreglado, a propósito:** *banker's rounding*
  (`round(2.5)` → 2). Necesita `Decimal` y es un tema entero → ejercicio del nivel.
- **`GUIDE.md` §8.l nueva:** *Probar tus propias funciones (sin modelo, sin red,
  $0.00)* — la plantilla del bucle, las tres familias de casos, las 6 reglas, las
  **4 trampas de Python** (`4.0 == 4`, `round(x, 0)`, `isinstance(True, int)`,
  banker's rounding) y cómo se prueban las funciones con **efecto secundario**.
- **Ningún gasto de API en toda la sesión.** Es la primera sesión del curso que
  cuesta exactamente **$0.00**, y no por casualidad: era el objetivo del paso 5.

**Método — dos cosas que hay que conservar:**

1. ⚠️ **UNA pregunta a la vez.** Se confirmó dos veces: con tres preguntas juntas
   dijo *"no entendí las preguntas"*; reformuladas a una sola, las contestó bien
   de inmediato, todas.
2. **Pide "escríbeme un ejemplo primero"**, y funciona dárselo **sobre otra
   función** (`poner_apodo`, `doblar`) para no regalarle su ejercicio.
   ⚠️ Pero hay que **decir explícitamente que la función del ejemplo no va en su
   archivo**: preguntó cómo "convertir `doblar`" para el ejercicio.

**Lo que hizo bien y conviene reconocerle:** las decisiones de diseño del día
salieron de él (allowlist, rechazar el monto negativo, los **dos candados**, dejar
el freno 3, rechazar minúsculas y textos, borrar antes de probar, comprobar
existencia **y** contenido). El código mecánico lo pidió dictado; **el criterio no.**

---

## Dudas abiertas

_(Aquí anotamos preguntas que quedaron sin resolver, para retomarlas después.)_

> Las tres primeras se abrieron antes del nivel 5 y **dos ya están cerradas**
> (sesión 8). Llegar al nivel 5 con preguntas propias sin resolver funcionó
> exactamente como se esperaba: el nivel se escribió contra ellas.

- ~~**¿Cómo se prueba algo que nunca responde igual dos veces?**~~ →
  **RESUELTO en la sesión 8**, y la respuesta cabe en cuatro pasos: se corre N
  veces, se cuenta, se pone un **control** al lado, y se mira si los **rangos**
  se solapan antes de declarar nada. La pregunta madre del curso, abierta desde
  el nivel 1 (L1.6, L1.11, L1.16).
- **¿Borrar el turno `assistant` afecta la longitud de la respuesta?** Quedó sin
  resolver porque el experimento tenía 3 variables. Se podría medir de verdad en
  el nivel 5, con 5 corridas por versión.
- ~~**¿Por qué sigue apareciendo el rioplatense con el dialecto anclado?**~~ →
  **RESUELTO en la sesión 8.** Abierto desde el nivel 3, cerrado con 130
  corridas.
  - **La causa:** el modelo elige entre tres conjugaciones del mismo verbo
    (`ponte` / `ponete` / `póngase`) y **las tres son español correcto**. Por eso
    decir "español de Colombia" no lo mataba: no es un problema de idioma sino de
    **variedad**, y el modelo no sabe cuál es la tuya hasta que se la nombras.
  - **La tasa:** 12 de 60 = **20%** (entre 9.9% y 30.1%) con el `SYSTEM` viejo.
  - **El arreglo, demostrado:** tanto prohibir el voseo por su nombre (B) como
    mover la instrucción al turno del usuario (C) suben el uso de la forma
    correcta de 63% a 100% y 93%. Las dos diferencias están demostradas contra
    el control; **B vs C sigue sin resolverse** (se solapan con N=30).
  - **La hipótesis del estudiante sobrevivió:** la posición sí importa, y además
    C cuesta 26x menos que B (+3 tokens contra +80, por llamada, para siempre).
- ⚠️ **DUDA NUEVA, abierta en la sesión 8: el tratamiento tú/usted.** Apareció
  sola al contar. Con el mismo prompt el modelo trata de tú, de usted, o **mezcla
  los dos dentro de una misma respuesta** (2 de 30, verificados a mano). **Ni B
  ni C lo arreglan.** Es el mismo tipo de defecto que el dialecto, en otra
  dimensión, y está medido pero sin resolver.
- **¿Qué llega en los primeros segundos de un stream?** Con streaming la pantalla
  estuvo quieta 5.8 s. La hipótesis es que `text_stream` no entrega los bloques
  `thinking`. **Sin verificar** — es el ejercicio 8 del nivel 4 y se resuelve en
  una corrida barata.

---

## ⚠️ PENDIENTE DE VERIFICAR (leer al abrir la próxima sesión)

- 🔴 **LO PRIMERO DEL PASO 6: volver a comprobar las 2 URLs del 5b.** Están
  verificadas con HTTP 200 el **2026-07-29** y copiadas en
  `05b-proyecto/README.md` §5b.4 con sus campos. **No se escribe código encima sin
  volver a comprobarlas** — es la lección de la sesión 3 (afirmar "es gratis" sin
  verificar). Son `open.er-api.com/v6/latest/USD` (mercado) y
  `datos.gov.co/resource/32sa-8pi3.json` (TRM oficial).
- ⚠️ **`convertir()` tiene un defecto conocido sin arreglar:** *banker's rounding*
  (`round(2.5)` → 2, `round(3.5)` → 4). Los 26 casos del eval **no lo detectan**
  porque ninguno cae en `.5`. El arreglo es `Decimal` en vez de `float` → ejercicio
  del nivel, y empieza por **agregar los casos `.5` y verlos fallar**.
- ⚠️ **Hueco conocido del eval de `guardar_reporte`:** comprueba que no se escribió
  *dentro* de `caja/`, pero **no puede demostrar que no se escribió fuera**. Se
  confía en los 3 frenos + la prueba de fuerza bruta de 278.916 nombres.
- **El manejo de error de red nunca se vio ocurrir con el wifi apagado.** En el
  nivel 4 sí vimos `APIConnectionError` de verdad (apuntando a un dominio que no
  existe), pero nadie ha desconectado el internet y corrido el agente completo.
  Es el **ejercicio 7 del nivel 4**.
- ~~**La hipótesis del `thinking` en el stream**~~ → **medida (ejercicio 8).**
  Mecanismo confirmado, hipótesis **incompleta**: el thinking es la mitad del
  silencio. Ver §4.4, L4.25 y `04b_eventos.py`.
- ~~**El sesgo de orden de `04_streaming.py`**~~ → **medido (ejercicio 9).**
  ~1 s, y la ventaja del streaming corregida a ~6.3 s. Ver §4.4 y L4.24.
  ⚠️ **`04_streaming.py` quedó con el orden invertido** (streaming primero).
  Es el orden correcto para el ejercicio, pero **los números del README §4.4
  están etiquetados por corrida** — al releerlos, mirar la etiqueta.
- ~~**Faltan por correr 2 de los 4 scripts del nivel 4**~~ → **los 4 corridos.**
  - ~~`01_errores.py`~~ → **corrido en la sesión 6.** Idéntico al mío. Encontró
    un defecto de presentación (ver bitácora).
  - ~~`02_reintentos.py`~~ → **corrido en la sesión 6.** Tiempos distintos,
    forma idéntica. Salieron dos hallazgos nuevos (la resta del backoff en la
    sección C y la herencia de `APITimeoutError`).
  - ~~`03_harness.py`~~ → **corrido dos veces en la sesión 7** (`s` y `n`), con
    lectura del `registro.jsonl`. Cuatro hallazgos nuevos.
  - ~~`04_streaming.py`~~ → **corrido en la sesión 7.** Encontró que mi
    estimación de costo del docstring estaba al doble.

### Resuelto en la sesión 4
- ~~`02_bucle.py` con los sabotajes de los ejercicios 1 y 2 aplicados~~ →
  **restaurado por el estudiante y verificado**: línea 107 (`historial.append`
  del turno `assistant`) activa, línea 122 con `"tool_use_id": bloque.id`.

### Resuelto
- ~~`02-conversacion/01_chat.py` sin ejecutar~~ → **corrido por el estudiante**
  en dos versiones (normal y ejercicio 1). Encontró un bug (ver abajo).
- ~~`01-primera-llamada/03_costo.py` modificado y sin ejecutar~~ → **corrido en
  la sesión 3.** Tabla entera, razón calculada = 30.9x. Costo $0.0039.

---

## Errores que encontramos y cómo se resolvieron

_(Este historial vale oro: los mismos errores reaparecen. Anótalos aunque parezcan tontos.)_

- **Pantalla vacía sin ningún error.** `max_tokens=30` en Opus 5: los 30 tokens se
  fueron enteros en el bloque `thinking` y no hubo bloque `text`. No fue un bug —
  `stop_reason: max_tokens` lo decía. → L1.1, L1.2
- **Tabla rota en 3 renglones + respuesta aparentemente cortada** en `03_costo.py`.
  Causa real: el propio script hacía `texto.strip()[:30]`, y la respuesta traía
  saltos de línea internos que `.strip()` no limpia. **No era del modelo.**
  Solución: `" ".join(texto.split())`. → L1.14
- **Dato falso impreso con confianza:** el script decía "Haiku cuesta 5x menos"
  (texto fijo) cuando la medición real dio 55x. Solución: calcular, no fijar. → L1.13
- **Contador roto que no falla, solo miente** (sesión 3, `01_chat.py`):
  `len(historial) // 2` asumía 2 mensajes por turno. Al cambiar la forma del
  historial imprimió `0, 1, 1, 2` sin lanzar ningún error. → Contar con una
  variable propia, no deducir de la estructura.
- **Demostración que no demostraba nada** (sesión 3, `03_recortar.py`): para
  probar que la ventana deslizante "olvida", le preguntábamos algo de cultura
  general (*¿qué es una variable?*). Las tres estrategias acertaron, porque el
  modelo ya lo sabía sin historial. **Regla:** para probar memoria, pregunta un
  dato que el modelo no pueda saber de otro modo (un nombre inventado).
- **Mismo texto de error, causas opuestas** (sesión 4, ejercicios 1 y 2 del
  nivel 3). Los dos dan el mismo mensaje —*"Each `tool_result` block must have a
  corresponding `tool_use` block in the previous message"*— pero:
  - `tool_use_id` inventado → `messages.2.content.0` (había `tool_use`, no
    emparejaba).
  - Sin el turno `assistant` → `messages.0.content.1` (no había `tool_use`
    **ninguno**; y el id era real y correcto).
  → **Lee la coordenada antes que la frase.** El texto no distingue los casos;
  la dirección sí.
- **La API fusiona mensajes consecutivos del mismo rol.** Descubierto sin
  buscarlo en el ejercicio 2: al quitar el turno `assistant` quedaron dos `user`
  seguidos y la API los unió en uno solo, por eso el `tool_result` apareció como
  `content[1]` del mensaje 0. **Tu lista de Python y lo que ve la API no tienen
  siempre la misma forma.**
- **En un bucle agéntico el síntoma va una vuelta por delante de la causa.** El
  id malo se escribe procesando la vuelta 1; el 400 sale en la llamada de la
  vuelta 2. Y para entonces ya pagaste la vuelta 1 sin obtener respuesta:
  un agente roto gasta antes de fallar.
- **El programa funcionó y aun así reventó** (sesión 4, `02_bucle.py`):
  `UnicodeEncodeError: 'charmap' codec`. Las 2 llamadas a la API salieron bien,
  la herramienta se ejecutó, el modelo respondió — y el `print` de esa respuesta
  murió porque la consola de Windows es `cp1252` y el texto traía `°` y emojis.
  → `sys.stdout.reconfigure(encoding="utf-8")`. **Lee a qué línea apunta el
  traceback antes de sospechar de la API.**
- **El error que no era de la API** (sesión 5, `01_errores.py`): pedir
  `max_tokens=99_999_999` no da un 400. Da un `ValueError` de Python — el SDK
  calcula que tardaría más de 10 minutos y **se niega a mandar la petición**.
  Ni red, ni servidor, ni factura. → Antes de buscar la causa, decide en cuál de
  las tres fronteras murió: tu máquina, la red, o el servidor.
- **La protección duplicada que multiplica** (sesión 5): si escribes tu propio
  reintento y dejas el del SDK (`max_retries=2` por defecto), 3 × 3 = **9
  peticiones** por una sola llamada. Solución: `max_retries=0` en el cliente
  cuando el reintento propio existe.
- **El corte que esconde el dato, por tercera vez** (sesión 6, `01_errores.py`):
  `e.message[:80]` partía el JSON del error justo antes del mensaje real, así que
  los casos 401 y 404 salían ilegibles. Ya había pasado con `texto.strip()[:30]`
  (nivel 1) y con la respuesta "cortada" de Sonnet. → **Cuando un dato salga
  truncado o raro, sospecha primero de tu propio `print`.** Y: antes de recortar
  un error, busca si el SDK te lo da ya parseado (`e.body`).
- **Costo estimado en vez de medido, cuarta vez** (sesión 7, `04_streaming.py`):
  el docstring anunciaba `~$0.02` y la corrida real dio **$0.038**. Nadie lo
  había medido; salió de mi cabeza al escribir el archivo. Es el mismo patrón del
  "Haiku cuesta 5x menos" (nivel 1) y de la fila inventada de la cuarta
  estrategia (nivel 2). → **Un número escrito en el material tiene que venir de
  una corrida, o venir marcado como estimación.**
- **Análisis mal atribuido (mío, no del estudiante):** concluí que borrar el turno
  `assistant` causó la brevedad, sin saber que él también había añadido una regla
  al `SYSTEM`. Lección: preguntar **qué se tocó** antes de interpretar. → L1.11

---

## Decisiones tomadas

- **Python antes que TypeScript.** Python tiene los ejemplos y librerías de agentes más
  maduros; TypeScript entra cuando lleguemos a la parte web (**nivel 6**).
- **Evaluación antes que TypeScript** (decidido en la sesión 6, a petición del
  estudiante). Evaluar es el concepto difícil del curso. Aprenderlo al mismo
  tiempo que un lenguaje nuevo sería **cargar dos cosas nuevas a la vez**, que es
  justo lo que este recorrido evita en todos los demás niveles. Así se mide en
  Python —que ya maneja— y TypeScript entra pegado al momento en que tiene razón
  de ser: el nivel 7, donde hay navegador.
- **Rúbricas y LLM-as-judge se nombran aparte de los evals deterministas**
  (nivel 5). No son lo mismo: un `if` comprueba "¿llamó la herramienta correcta?";
  "¿respetó el dialecto?" necesita una escala y otro modelo juzgando. El plan
  antes decía solo "evals, casos de prueba, regresiones" y el segundo tipo
  quedaba fuera.
- **Observabilidad es una pieza propia del nivel 7**, no un ítem de lista.
  Evaluación pregunta *"¿funciona?"* antes de soltarlo; observabilidad pregunta
  *"¿qué está haciendo ahora?"* con usuarios encima. El `registro.jsonl` del
  nivel 4 es su primer ladrillo.
- **Un nivel a la vez.** No se escriben lecciones futuras por adelantado, para que el
  material se ajuste al ritmo real del estudiante.
- **El agente del clima como primer agente** (nivel 3), porque es el caso mínimo donde
  el modelo no puede responder solo y obliga a construir el bucle completo.
