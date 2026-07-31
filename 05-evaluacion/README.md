# Nivel 5 — Evaluación

> **Qué vas a poder hacer al terminar:** decir *"el rioplatense sale en 7 de 30"*
> en vez de *"a veces contesta raro"*. Y saber si un cambio tuyo mejoró o empeoró
> el agente, con un número, no con una corazonada.

Este nivel existe porque el curso lleva desde el nivel 1 acumulando una pregunta
que no se podía contestar todavía:

> **¿Cómo se prueba algo que nunca responde igual dos veces?**

---

## 5.0 — Qué es evaluar (la lección conceptual)

*(Esta sección se escribió al empezar el nivel, antes de cualquier código.
Es la explicación que da sentido a todo lo que viene después.)*

### La analogía

Imagina que contratas a alguien para atender el teléfono de tu empresa.

El primer día lo escuchas atender una llamada. Lo hace bien. ¿Ya sabes que sirve?

No. Sabes que **esa** llamada salió bien. Nada más.

Para saber si sirve necesitas otra cosa: escuchar **cincuenta** llamadas, con una
hoja al lado donde anotas cosas concretas — ¿saludó?, ¿dio el precio correcto?,
¿fue grosero? Al final tienes números: *"saludó en 50 de 50, dio el precio mal en
3 de 50"*.

Eso segundo es **evaluar**. La hoja con las preguntas se llama **rúbrica**, y
cada llamada de prueba se llama **caso**.

### Por qué hace falta aquí y no en un programa normal

Un programa normal es determinista. Si `2+2` te da `4` una vez, te da `4`
siempre. Lo pruebas una vez y ya.

**Tu agente no.** Lo viste siete veces en este curso, y todos estos datos son
tuyos, de tus propias corridas:

| Lo que viste | Dónde |
|---|---|
| El mismo script devolvió 1 bloque en una máquina y 2 en la otra | Nivel 3 (L3.1) |
| "Haiku cuesta 55x menos"… y a la semana, 30.9x | Niveles 1 y 3 |
| La primera palabra tardó 8.6, 5.8, 7.1 y 4.23 segundos | Nivel 4 (§4.4) |
| El rioplatense: 1 de 3, y en respuesta distinta cada vez | Niveles 3 y 4 (L4.23) |

Ese último caso es el que rompe el método de *"correr y mirar"*. Si el defecto
sale 1 de cada 3 veces, **una corrida limpia no prueba nada**: tienes un 66% de
probabilidad de no verlo aunque esté ahí.

Y al revés, que es peor: si "lo arreglas" y la siguiente corrida sale limpia,
tampoco sabes si lo arreglaste. Podría ser el 66%.

> **La frase que resume el nivel:** cuando el resultado no se repite, un solo
> resultado no es evidencia. Solo la cuenta lo es.

### Qué aporta, en concreto

**1. Convierte una impresión en un número.**
Hoy dirías *"a veces contesta raro"*. Después dirás *"sale rioplatense en 7 de
30"*. Lo segundo se puede comparar con la medición de la semana que viene; lo
primero no.

**2. Te dice si un cambio mejoró o empeoró.**
Esta es la que más vale. Cambias el `SYSTEM` para arreglar el dialecto.
¿Funcionó? Sin evaluación, tu respuesta es una corazonada. Con evaluación: 7 de
30 antes, 1 de 30 después.

**3. Te avisa cuando rompes algo sin querer.**
Arreglas el dialecto y sin darte cuenta el agente deja de llamar bien a las
herramientas. Eso se llama **regresión**: arreglar A y romper B. Es lo más común
y lo más invisible. La única defensa es tener una lista de casos que se corren
**enteros** cada vez.

**4. Te deja bajar de modelo sin miedo.**
Opus 5 cuesta 25x lo que Haiku en salida. ¿Te sirve Haiku para tu agente de
divisas? Sin evaluación es una apuesta. Con evaluación corres los mismos 30 casos
con los dos y comparas. **Esto es dinero directo en tu SaaS.**

**5. Separa "el modelo falló" de "mi código falló".**
Ya tienes la mitad medida: en el nivel 4 descubriste que **la infraestructura sí
es determinista** (L4.14). Los 5 errores salieron idénticos en las dos máquinas.
Eso significa que tu harness se puede probar como cualquier programa normal.
Lo movedizo es solo **la generación**.

### Los dos tipos de pregunta

No todo se comprueba igual, y confundirlos es el error clásico.

**Tipo 1 — se comprueba con un `if`.** Hay una respuesta correcta y punto.

- ¿Llamó a `obtener_clima` y no a `hora_utc`?
- ¿`stop_reason` fue `tool_use`?
- ¿100 USD × 3.205,80 dio 320.580 COP?
- ¿Se pasó del presupuesto?

Barato, rápido, y no necesita a nadie juzgando. Es el suelo del nivel.

**Tipo 2 — no hay `if` que sirva.** No existe una respuesta correcta única.

- ¿Respetó el español colombiano?
- ¿Dijo de dónde sacó la tasa?
- ¿Fue útil la respuesta?
- ¿Está bien escrita?

Aquí defines una escala (por ejemplo 0, 1 o 2) y **quien califica es otro
modelo**. Eso se llama **LLM-as-judge**. Suena raro —un modelo calificando a
otro— y tiene sus trampas, que se ven más adelante en este nivel.

> Tu duda del dialecto es del **tipo 2**. Por eso el curso la ha estado guardando
> desde el nivel 3.

### En qué momento se evalúa

Cuatro momentos, y son distintos:

| Cuándo | Para qué |
|---|---|
| **Antes de escribir el agente** | Si no sabes escribir los casos, es que no tienes claro qué debe hacer. Escribir 10 casos primero te obliga a definirlo. |
| **Cada vez que cambias algo** | Tocas el prompt, cambias de modelo, agregas una herramienta → corres los casos. Esto es lo que caza las regresiones. |
| **Antes de soltarlo a usuarios reales** | El portero. Si no pasa los casos, no sale. |
| **Ya en producción** | ⚠️ Esto **ya no es evaluación**: es **observabilidad**, y es el nivel 7. |

La diferencia entre las dos, en una línea:

> **Evaluación** pregunta *"¿mi agente funciona?"* antes de soltarlo, con casos
> que escribiste tú.
> **Observabilidad** pregunta *"¿qué está haciendo ahora mismo?"*, con tráfico
> real que no controlas.

Tu `registro.jsonl` del nivel 4 fue el primer ladrillo de la segunda.

### Lo que cuesta

Evaluar cuesta plata, y hay que decirlo. Correr 30 casos son 30 llamadas. Si
además usas un juez, son 60.

Por eso el orden importa: primero los evals del **tipo 1**, que son casi gratis,
y el juez solo donde de verdad no hay `if` posible. Es la misma lógica del nivel
2 con el resumen: **se paga solo si lo vas a usar bastante.**

---

## Las cuatro preguntas propias que llegan a este nivel

Este nivel no se escribe contra ejemplos inventados. Se escribe contra dudas que
salieron de tus propias corridas y que quedaron anotadas en `PROGRESO.md`:

1. **¿Por qué sigue apareciendo el rioplatense con el dialecto anclado?**
   1 de 3, en 3 corridas, en 2 máquinas, y **en respuesta distinta cada vez**
   (L4.23). Es el caso de rúbrica del curso.
2. **¿Una instrucción en el turno del usuario pesa más que la misma instrucción
   en el `SYSTEM`?** Marcador actual: `SYSTEM` 3 de 9, turno del usuario 0 de 4.
   Con esos números no prueba nada — **pero es exactamente el tipo de pregunta
   que este nivel sabe responder.**
3. **¿Borrar el turno `assistant` afecta la longitud de la respuesta?** Quedó sin
   resolver en el nivel 2 porque el experimento tenía 3 variables, no 1.
4. **¿Cómo se prueba algo que nunca responde igual dos veces?** La pregunta madre,
   abierta desde el nivel 1.

---

## 5.1 — Probar el detector antes de gastar (`00_probar_detector.py`)

Antes de medir al modelo hay que medir **tu propio medidor**. Si el detector
miente, el experimento entero miente — y con toda la apariencia de rigor, porque
igual imprime un número bonito.

Este script no llama a la API ni una vez. **Cuesta $0.00 y da idéntico siempre**,
porque se apoya en L4.14: sin modelo de por medio, el código se comporta como
cualquier programa normal.

> Esta es la línea que parte el nivel 5 en dos. Lo que se puede probar gratis y
> con certeza, se prueba primero. La API se deja para lo único que la necesita.

**La técnica: pares mínimos.** Dos frases que dicen lo mismo y se diferencian en
una sola cosa. Si las dos dan el mismo veredicto, el detector no mira lo que
crees que mira.

| | |
|---|---|
| `"Llevá campera"` | debe dar rioplatense |
| `"Lleva sombrilla"` | **no** debe darlo — solo cambia la tilde |
| `"Ponte una chaqueta"` | tuteo |
| `"Póngase una chaqueta"` | ustedeo |
| `"Estas cosas pasan"` | ninguno — trampa: `estas` sin tilde es demostrativo |
| `"Nosotros vamos"` | ninguno — trampa: `vos` vive dentro de `nosotros` |

Es la misma idea del ejercicio 9 del nivel 4: para aislar un efecto, cambias una
cosa y dejas todo lo demás igual.

### El bug que apareció escribiendo el detector

La primera versión normalizaba (quitaba tildes) antes de comparar. Pero:

```
"Lleva sombrilla"   <- Colombia, correcto
"Llevá sombrilla"   <- rioplatense
```

**La única diferencia es la tilde**, así que normalizar borraba justo la señal
que se buscaba: el detector habría marcado la forma colombiana correcta como
defecto.

Arreglo: **dos listas**. Los imperativos voseantes se buscan sin normalizar,
porque ahí la tilde *es* el dato. El léxico (`campera`, `sos`) sí se normaliza,
porque esas formas no existen en el español colombiano y no chocan con nada.

> Ya lo habías visto dos veces: el `[:30]` del nivel 1 y el `[:80]` del nivel 4.
> **El preprocesamiento destruye el dato antes de que llegues a verlo.**

Y hay tres palabras **descartadas a propósito** en cada detector: `acá`, `plata`,
`ahorita` (se usan igual en Colombia) y `le`, `se`, `su` (ambiguas con la tercera
persona). **Perder señal es mejor que inventarla:** un detector que adivina
produce una cifra que parece exacta y no lo es.

---

## 5.2 — Correr N veces y contar (`01_contar.py`, `02_contar_v2.py`)

### El primer intento salió 0 de 10, y el error era del experimento

La pregunta fue *"¿qué ropa me pongo hoy en Bogotá si está lloviendo?"*, hecha a
un modelo **sin herramientas**. Resultado: **0 de 10**, contra un histórico de
3 de 9.

Pero al leer las respuestas:

```
 3. No puedo consultar el clima ahora mismo, así que...
 6. No puedo verificar el clima ahora mismo, así que...
 7. No puedo consultar el clima de hoy, así que...
 8. No tengo acceso al clima en tiempo real, así que...
```

**Seis de las diez se gastaron disculpándose.** El modelo nunca llegaba a dar
consejo, que es donde el defecto vivía.

> **`0 de 10` no refuta `3 de 9` si no midieron lo mismo.** Un experimento que
> cambia las condiciones y sale limpio no demuestra que arreglaste algo:
> demuestra que dejaste de mirar donde estaba.

Es el error de `03_recortar.py` del nivel 2 con otra ropa: una prueba que corre,
que no revienta, y que no prueba lo que dice probar.

**El arreglo:** dar el clima por hecho en la pregunta.
*"Está lloviendo en Bogotá y hace 14 grados. ¿Qué ropa me pongo?"*

### Lo que apareció sin buscarlo

Leyendo esas mismas 10 respuestas se vio otra cosa: el modelo trataba de **tú**
en 4 y de **usted** en 5, con el mismo prompt. Nadie iba a buscar eso.

> **Contar N veces te enseña cosas que no fuiste a buscar.**

De ahí salió el segundo detector, con **cuatro salidas** en vez de dos:

| salida | qué significa |
|---|---|
| `tu` / `usted` | clasificado |
| `mixto` | **se contradice dentro de la misma respuesta** |
| `indeterminado` | el detector dice *"no sé"* |

Las dos últimas importan más que las dos primeras. Forzar un binario cuando no
hay evidencia es inventarse el dato: **un detector honesto tiene que poder
abstenerse.**

### El resultado: 9 de 30, y el defecto vive en UN verbo

Con el clima dado, **9 de 30 = 30%**. El histórico era 3 de 9 = 33%. Dos
estimaciones independientes, condiciones distintas, y coinciden.

Y entonces el hallazgo del nivel. Casi todas las respuestas dicen lo mismo:

> *"[Ponte] una chaqueta impermeable o rompevientos sobre un buso, con jean y
> zapatos cerrados. [Lleva] paraguas, que en Bogotá el aguacero coge
> desprevenido."*

Lo único que baila es **cómo conjuga el primer verbo**:

| forma | cuántas | qué es |
|---|---|---|
| `ponte` | 18 de 30 | tú, colombiano correcto |
| `ponete` | **9 de 30** | **rioplatense — el defecto entero** |
| `póngase` | 2 de 30 | usted |

**Los 9 rioplatenses son exactamente las 9 respuestas con `ponete`.** Los 2
ustedeos son los 2 `póngase`. Los 3 `llevá` acompañan siempre a un `ponete`.

O sea que el fantasma que se perseguía desde el nivel 3 —*"a veces habla
argentino"*— es en realidad esto:

> **Al escribir la primera palabra, el modelo elige entre tres conjugaciones del
> mismo verbo, y una de las tres es rioplatense.**

Las tres son español correcto. **Por eso ningún `SYSTEM` que dijera "responde en
español de Colombia" lo mataba:** las tres *son* español. El problema nunca fue
el idioma, fue la **variedad**.

Y explica el 0 de 10 de la v1: allí la respuesta empezaba con *"no puedo
consultar…"*, así que **la bifurcación nunca ocurría**.

---

## 5.3 — Cerrar el ciclo: cambiar y volver a medir (`03_contar_v3.py`)

Medir solo sirve si después comparas:

```
medir  →  cambiar UNA cosa  →  medir otra vez  →  comparar
```

Tres versiones, **intercaladas** A,B,C,A,B,C… en cada vuelta (la técnica del
ejercicio 9 del nivel 4, aplicada a tres), 30 corridas cada una:

| | qué cambia |
|---|---|
| **A** | control: el `SYSTEM` de siempre, sin tocar |
| **B** | prohibir el voseo **por su nombre**: *"nunca uses 'ponete', 'llevá'…"* |
| **C** | la misma instrucción de A, **movida al turno del usuario** |

### El control no se replicó, y es la lección más cara

| | rioplatense | rango creíble |
|---|---|---|
| v2 | 9/30 = 30% | 13.6% – 46.4% |
| **v3-A** | **3/30 = 10%** | 0% – 20.7% |
| las 60 juntas | 12/60 = **20%** | 9.9% – 30.1% |

Mismo prompt exacto (entrada 108 en las dos), misma máquina, veinte minutos
después. Los rangos se tocan, así que **el azar basta para explicarlo**. Pero:

> Con N=30, el mismo prompt dio 30% y 10%. **N=30 no era suficiente — y solo se
> supo porque había un control.**

Sin la versión A se habría comparado B y C contra el 30% de antes, y se habrían
concluido cosas más grandes de las que aguantan los datos. **El control no es
relleno: es lo que te dice si tu regla de medir sigue siendo la misma regla.**

### La métrica binaria no tenía poder. La fina sí

El script declaró, correctamente, *"A vs B: los rangos se solapan"*. Y es verdad
para la pregunta binaria *¿hubo rioplatense, sí o no?*: con tasas bajas hace
falta muchísimo N.

Pero el defecto vive en un verbo. Así que en vez de preguntar *"¿hubo defecto?"*
—que solo tiene señal en las 3 respuestas malas— se pregunta *"¿qué forma del
verbo usó?"*, que tiene señal en **las 30**:

| | dijo `ponte` (la forma correcta) | rango |
|---|---|---|
| A (control) | 19/30 = 63% | 46% – 81% |
| B (prohibir) | **30/30 = 100%** | 90% – 100% |
| C (mover) | 28/30 = 93% | 84% – 100% |

**A vs B: separados. A vs C: separados. B vs C: se solapan.**

> **No hizo falta gastar más: hizo falta medir mejor.** Mismos datos, mismo
> dinero, otra pregunta. Si tu métrica solo mira los fallos, tiras a la basura la
> información que traen los aciertos.

⚠️ **La salvedad honesta:** elegir la métrica *después* de ver los datos es una
trampa clásica — buscas hasta que algo salga significativo. Aquí no aplica,
porque `forma_verbal()` se escribió **antes** de correr la v3, con los datos de
la v2. Pero había que decirlo, y hay que desconfiar siempre que alguien cambie de
métrica justo cuando la primera no le dio lo que quería.

### El bug de la función que medía la confianza

La primera versión de `margen()` devolvía `±0.0` cuando salían 0 aciertos. O sea:
*"0 de 30 significa defecto eliminado, con certeza total"*. **Es falso** — un
defecto del 5% tiene ~21% de probabilidad de no aparecer ni una vez en 30.

Arreglado con la **regla de tres**: si no viste ninguno en `n` intentos, el tope
al 95% es `3/n`. Con n=30 eso es 10%, no 0%. Y la función se renombró a `rango()`
porque dejó de ser simétrica.

> **Es el peor tipo de bug que puede tener un eval: no revienta, solo miente, y
> miente con cara de matemática.**

Esa misma función, aplicada hacia atrás, valida todo el trabajo del día:

| dato | rango | qué significa |
|---|---|---|
| `0/10` (la v1) | 0% – **30%** | aquel cero era compatible con el 30% real |
| `3/9` (nivel 4) | 2.5% – **64%** | el famoso "1 de 3" servía para sospechar, no para afirmar |
| `12/60` (hoy) | **9.9% – 30.1%** | ya excluye el cero: el defecto existe |

### Y el premio, que es de ingeniería

Los dos arreglos funcionan. Pero no cuestan lo mismo:

| | tokens de entrada | sobrecosto por 1.000 llamadas |
|---|---|---|
| B | 188 (+80) | **$0.40** |
| C | 111 (+3) | **$0.015** |

**26 veces más barato por el mismo efecto**, y ese sobrecosto es **permanente**:
se paga en cada llamada, para siempre, igual que el menú de `tools` del nivel 3.

Lo que **no** se puede afirmar: que C sea *mejor* que B. Se solapan. Lo que sí:
que es igual de bueno hasta donde alcanzan 30 corridas, y muchísimo más barato.

---

## 5.4 — Evals deterministas del harness (`04_evals_harness.py`)

Hasta aquí todo lo probado fue **el modelo**: caro, lento, y nunca igual dos
veces. Pero tu agente son dos cosas pegadas:

| | qué decide | cómo se prueba |
|---|---|---|
| **El modelo** | qué herramienta pedir, qué texto escribir | caro, N veces, contando |
| **El harness** | presupuesto, permisos, timeouts, topes, registro | **es código normal** |

Los seis frenos del nivel 4 no tienen nada de probabilístico. `PRESUPUESTO_USD`
o corta o no corta. `PERMISOS.get(nombre, "prohibir")` o deniega o no deniega.

> **La mitad de tu agente se puede probar sin llamar a la API ni una vez.**

### El muro que apareció al intentarlo

`03_harness.py` **no se podía importar sin ejecutarse**. No tenía
`if __name__ == "__main__"`, así que cargarlo para probar sus piezas lo arrancaba
entero: creaba `caja/`, hacía las 3 preguntas, gastaba $0.03 y se quedaba
esperando que alguien tecleara `s`.

> El `if __name__` no es decoración: separa **"este archivo *es* un programa"** de
> **"este archivo *ofrece* piezas"**. Es un defecto que solo se descubre el día
> que intentas probar.

Arreglado en el nivel 4 (todo lo ejecutable se movió dentro de `main()`).

### Los 24 evals

| Grupo | Qué comprueba |
|---|---|
| **dinero** | `costo()` exacto; la salida cuesta 5x la entrada |
| **permisos** | denegar por defecto; el sí y el no del humano; 13 teclas hostiles |
| **candado** | `../` no sale de `caja/`; rutas absolutas; **y que sí borre lo que debe** |
| **coherencia** | que no se te olvide nada al añadir una herramienta |
| **registro** | que `anotar()` escriba JSON válido **y con hora** |
| **topes** | `MAX_VUELTAS > 1`; que el SDK no reintente encima del tuyo |

Corren **gratis** y dan **idéntico siempre** — se comprobó en dos máquinas.

### El agujero de seguridad que encontraron

```python
if respuesta.startswith("s"):     # el permiso para borrar archivos
```

**Cualquier palabra que empiece por `s` autorizaba el borrado.** Y ahora piensa
qué teclea alguien que quiere abortar:

| teclea | quería | pasaba |
|---|---|---|
| `salir` | irse | **borra** |
| `stop` | parar | **borra** |
| `suspende` | cancelar | **borra** |

**Las palabras para abortar en español empiezan por `s`.** El freno más
importante del harness se abría con la palabra que uno escribe para cerrarlo.

Y lo que falló de fondo: **denegar por defecto** estaba aplicado perfectamente en
`PERMISOS.get(nombre, "prohibir")`… y no en la lectura del teclado, **tres líneas
más abajo**, en la misma función. Nadie lo vio en dos sesiones leyendo ese
archivo.

> Un eval vale por sus **casos hostiles**. Probar `"s"` y `"n"` habría pasado.

Arreglado: `if respuesta in {"s", "si", "sí"}`.

---

## 5.5 — El juez (`05_juez.py`)

El detector del script 1 es una lista de palabras escrita por un humano. Lo que
no esté en la lista no existe. Y hay preguntas que **ninguna lista** puede
responder: *¿fue útil? ¿citó la fuente? ¿suena natural?*

Para eso se usa otro modelo como juez, con una escala que defines tú: la
**rúbrica**.

> **¿Y quién juzga al juez?** El juez es un modelo: no da lo mismo dos veces,
> tiene sesgos, y puede equivocarse con total seguridad.
> **Un juez que nadie validó es una opinión con formato de número.**

### Primer intento: el juez pierde contra el `if`

Se le pidió detectar dialecto. Tres versiones de la rúbrica:

| rúbrica | qué se le añadió | acuerdo con el detector |
|---|---|---|
| v1 | la escala básica | 83% |
| v2 | + regla de desempate | 75% |
| v3 | + tabla de pares mínimos | **42%** |

Cada arreglo rompía otra cosa. Y seguir tuneando hasta que el número quedara
bonito habría sido exactamente la trampa que §5.3 advierte.

**El diagnóstico no era la rúbrica: era la tarea.** Detectar si aparecen palabras
de una lista es comparación de cadenas, y ahí el `if` gana en todo:

| | detector (`if`) | juez (Haiku) |
|---|---|---|
| costo | $0.00 | cuesta |
| estabilidad | 100% | 92% |
| acierto | validado con pares mínimos | 42% |

El error del juez era siempre el mismo: no distingue `lleva` de `lleve`, ni
`ponte` de `ponete`. **Una letra.**

> **Si un `if` puede responder la pregunta, no uses un juez.**
> Distinciones ortográficas: `if`. Comprensión del contexto: juez.

### Dónde el `if` sí se había rendido

En el detector de tratamiento se dejaron fuera **a propósito** las palabras `le`,
`se` y `su`: son ambiguas con la tercera persona (*"su chaqueta"* puede ser de
él). Resolver eso **requiere entender la frase**.

Ahí se reorientó el juez: ¿el texto trata al lector de forma consistente, o
mezcla tú y usted?

### El balance, sobre 120 respuestas

| | |
|---|---|
| mezclas conocidas que cazó | **3 de 3** |
| mezclas **nuevas y reales** | **4** |
| falsas alarmas | 36 |
| citas fabricadas | 9 de 451 (2%) |

Una de cada seis alarmas era real. Pero esas 4 valían la pena: todas eran la
construcción **`"No olvide el paraguas"`** junto a **`"ponte"`** — ustedeo
inequívoco que **no estaba en ninguna lista y que nunca se me habría ocurrido
buscar**.

```
120 respuestas → el juez marca 43 → lees 43 → encuentras 4 defectos
                                              invisibles para el `if`
```

> 📊 **Estos números son los de Haiku 4.5.** El ejercicio 1 repitió todo con
> Sonnet 5: encontró **las mismas 4 mezclas**, pero marcando **8 respuestas en
> vez de 43**. La comparación completa está en **§5.6** — y ahí se ve que "una
> de cada seis alarmas era real" no era una propiedad de los jueces, sino de
> *ese* juez.

> **Un juez es buen filtro y mal decisor.** Puede permitirse falsas alarmas
> porque el que decide al final eres tú. Úsalo para reducir lo que tienes que
> leer, no para sustituir que lo leas.

### Lo más grave: el juez fabrica evidencia

```
texto : "...que no se te empapen. Lleva paraguas por si el aguacero arrecia..."
juez  : ['ponte', 'te', 'lleva', 'lleve']   ← 'lleve' NO está en el texto
razón : "Mezcla tuteo al inicio con ustedeo al final"
```

El texto dice `Lleva` —tuteo, consistente con `ponte`— y el juez cita **las dos
formas a la vez** para sostener una mezcla que no existe. Tres veces.

No es que se equivoque: es que **inventa el dato que hace que su error parezca
fundamentado**, y eso pasa cualquier revisión por encima.

### La decisión de diseño que permitió descubrirlo

La rúbrica pedía `{"nota": …, "razon": …, "palabras": […]}`.

Si solo hubiera pedido el número, tendríamos *"43 respuestas con mezcla"* y nos
lo habríamos creído.

> **Un juez que solo devuelve una nota es incomprobable.** Pídele siempre las
> palabras exactas en que se apoya, y compruébalas contra el texto **con código,
> no leyendo**. Son cuatro líneas.

⚠️ Y al comprobarlas, **normaliza tildes en los dos lados**: la primera versión de
esa comprobación acusaba al juez de inventarse `pongase` cuando había dicho
`póngase`. Es el bug de la tilde de §5.1, por cuarta vez en la misma sesión.

### Sobre el jurado de varios jueces

Correr **el mismo** modelo dos veces mide **estabilidad**, no sesgo: te da el
mismo punto ciego dos veces. La primera pasada repitió la nota en 6 de 6 —
perfectamente estable, y equivocada.

> **Consistencia no es corrección.** Para medir sesgo hace falta un juez de otra
> familia; para medir verdad, etiquetas humanas. Y lo primero es siempre validar
> contra tus propias etiquetas, no diversificar proveedores.

---

## 5.6 — Haiku contra Sonnet: el ejercicio 1, resuelto

> Esta sección **no estaba planeada**. Sale del ejercicio 1, que el estudiante
> hizo. Está aquí porque tumbó tres afirmaciones de este mismo README —
> dos mías y una del código.

Las mismas 120 respuestas, la misma rúbrica, el mismo script. Lo único que
cambió fue `MODELO_JUEZ`.

### El resultado

| | Haiku 4.5 | Sonnet 5 |
|---|---|---|
| acuerdo con el detector | 66.4% | **95.8%** |
| marcó como mezcla | 43 de 120 | **8 de 120** |
| **mezclas reales cazadas** | **4 de 4** | **4 de 4** |
| falsas alarmas | 39 | **4** |
| precisión | 9% | **50%** |
| citas fabricadas | 9 de 451 (2.0%) | **1 de 323 (0.3%)** |
| estabilidad | 18/20 | **20/20** |
| respuestas sin formato válido | 1 | **0** |
| costo real | $0.127 | $0.306 |

**La fila que importa es la tercera, y hay que leerla con la cuarta.** Los dos
jueces encontraron las **mismas 4 mezclas reales**. El caro no vio nada que el
barato se perdiera. Lo que cambió no fue lo que encuentra: fue lo que te cobra
por encontrarlo.

```
Haiku : 120 respuestas → marca 43 → lees 43 → 4 reales
Sonnet: 120 respuestas → marca  8 → lees  8 → 4 reales
```

Por **$0.18 más** te ahorras leer **35 respuestas**.

> **El valor de un juez no es su exactitud: es cuánto trabajo humano te quita.**
> Y esa medida no aparece en "acuerdo %". Un juez con 9% de precisión no es un
> filtro — es una lista de tareas con otro nombre.

### Lo que NO arregló el modelo caro

Esto es lo que impide concluir *"usa siempre el caro y listo"*.

**1. Sigue fabricando citas.** Una de las 8. Sonnet marcó una respuesta citando
`['ponte', 'te', 'lleve']` — y `lleve` **no está en el texto**, que dice
`lleva`. Es la misma alucinación de Haiku, el mismo par `lleva`/`lleve`.
Bajó de 2.0% a 0.3%. **No a cero.**

**2. Una alarma donde el juez se contradice solo.** Su propia `razon` decía:

```
"Mezcla tuteo (ponte) con ustedeo (lleva es tuteo, pero revis..."
```

Marcó mezcla y en la misma frase escribió por qué no la había.

> **Un juez mejor no elimina el defecto: lo vuelve raro.** Y un defecto raro es
> más peligroso que uno frecuente, porque dejas de revisar. **La comprobación de
> citas contra el texto sigue siendo obligatoria con el modelo caro** — fue ella
> la que cazó la fabricación, no la lectura.

### Tres afirmaciones caídas

**(a) Mi elección de Haiku estaba mal, y la tomé sin medir.** Razoné
*"clasificar es una tarea fácil"*. Los datos: 9% vs 50% de precisión, 6x más
citas fabricadas, y una respuesta con el formato roto. Es exactamente el error
que §5.3 enseña a no cometer, cometido dentro del archivo que lo enseña.

**(b) Mis dos estimados de costo eran inventados.** Este README decía
*"~$0.18 en vez de ~$0.06"*:

| | escrito aquí | medido |
|---|---|---|
| Haiku | ~$0.06 | **$0.127** |
| Sonnet | ~$0.18 | **$0.306** |

La *razón* entre modelos sí quedó cerca (~2.4x contra el 3x que dije). Las
**magnitudes** las inventé las dos. Mismo patrón del `"55x"` del nivel 1.

**(c) El script mentía sobre el costo.** `05_juez.py` tenía los precios
quemados a mano:

```python
PRECIO_ENTRADA = 1.00 / 1_000_000     # Haiku
PRECIO_SALIDA = 5.00 / 1_000_000
```

Al cambiar `MODELO_JUEZ` a Sonnet, **los precios siguieron siendo los de
Haiku**. El script imprimió `COSTO REAL: $0.1530`. El real era **$0.3060**.

El bug no revienta ni avisa, y sale impreso en la línea que dice "COSTO REAL".

> **Si el modelo es una variable, el precio también tiene que serlo.** Un dato
> que depende de otro no se guarda suelto: se guarda junto. Arreglado con un
> diccionario `PRECIOS`, que además **revienta a propósito** si le pones un
> modelo que no conoce — preferimos fallar antes que imprimir un número falso.

⚠️ Y una letra pequeña que apareció al verificar: **Sonnet 5 está en precio de
lanzamiento ($2/$10 por millón) hasta el 2026-08-31.** Desde septiembre sube a
$3/$15 y esta misma corrida costará **~$0.46** sin que cambies una línea. Está
escrito en el código, con fecha, y no en la memoria de nadie.

### Y un cuarto bug, en el análisis de los resultados

Al revisar cuántas mezclas reales había, el chequeo decía:

```python
if 'olvide' in texto:      # MAL
```

`'olvide' in "no olvides"` → **`True`**. Y `"No olvides"` es tuteo, *correcto*.

Dio **46 mezclas reales**. Con límites de palabra (`\bolvide\b`) da **4**. Las
otras 42 eran `"no olvides"`: **el 91% del hallazgo era el bug.**

Es el bug de la tilde de §5.1 con otro disfraz, y **el cuarto de la misma
familia en este nivel**: `[:30]` (nivel 1), `[:80]` (nivel 4), `normalizar()`
(§5.1), y ahora `in` sin límites de palabra.

> **La familia se llama igual las cuatro veces: el código toca el dato antes de
> que tú lo veas.** Cortar, normalizar y buscar subcadenas parecen operaciones
> inocentes. Las cuatro destruyeron la señal que se estaba buscando, y ninguna
> lanzó un error.

### La conclusión honesta del ejercicio

No es *"usa el modelo caro"*. Es:

1. **Mide, no razones.** "Clasificar es fácil" sonaba bien y era falso.
2. **Elige por trabajo humano ahorrado**, no por % de acuerdo.
3. **Las comprobaciones no se relajan con un modelo mejor**, porque el defecto
   raro es el que se cuela.
4. **Un `if` que resuelva el caso sigue ganándole a los dos.** Las 4 mezclas
   reales llevaban todas `"No olvide"`: eso es una línea de código, $0.00, y
   100% de estabilidad. → ejercicio 4.

---

## Ejercicios

1. ~~**¿Un juez más caro acierta más?**~~ ✅ **HECHO** — resultados y análisis en
   **§5.6**. Resumen: sí, pero no por la razón que yo esperaba. Los dos jueces
   cazaron las mismas 4 mezclas reales; lo que cambió fue que Sonnet marcó 8
   respuestas en vez de 43, o sea **35 respuestas menos que leer por $0.18 más**.
   Sonnet **sigue fabricando citas** (0.3% en vez de 2.0%: raro, no cero).
   De paso destapó **un bug en `05_juez.py`** (los precios estaban quemados a los
   de Haiku, así que el costo impreso era la mitad del real) y **dos estimados
   míos inventados**. Fue el ejercicio que más enseñó del nivel, como estaba
   previsto — pero enseñó cosas distintas de las que yo había anticipado.
2. **Arregla el defecto del tratamiento.** Está medido y sin arreglar: el modelo
   trata de tú, de usted, o mezcla. Escribe una versión D del `SYSTEM` que fije
   el tratamiento, córrela con `03_contar_v3.py` y comprueba si baja.
3. **Resuelve B vs C.** Se solapan con N=30. Sube el N solo de esas dos, o mide
   la forma verbal en lugar del binario, y mira si se separan.
4. **Añade `"No olvide"` al detector** y vuelve a correr el juez. Es el ciclo
   completo: el juez encontró algo, tú lo conviertes en `if`, y a partir de ahí
   sale gratis y estable para siempre. **Ahora es el mejor ejercicio que queda**,
   porque §5.6 mostró que **las 4 mezclas reales llevaban todas `"No olvide"`** —
   o sea que un `if` de una línea le gana a los dos jueces: $0.00, 100% de
   estabilidad, y cero citas fabricadas. Ojo al escribirlo: usa **límites de
   palabra** (`\bolvide\b`), porque `"olvide" in "no olvides"` es `True` y
   `"No olvides"` es tuteo **correcto** — ese error infló un análisis de 4
   a 46 (§5.6).
5. **Rompe un eval a propósito.** Cambia `MAX_VUELTAS` a `1` o
   `REINTENTOS_SDK` a `2` en el harness y corre `04_evals_harness.py`. Comprueba
   que el eval te lo dice, y con qué mensaje.
6. **Mide el desacuerdo del juez consigo mismo con N alto.** Sube `REPETIR` a 50.
   ¿Sigue en 92%? ¿En qué respuestas cambia de opinión — son las ambiguas?
7. **Escribe una rúbrica para tu propio caso.** Para el agente de divisas del
   nivel 5b: *"¿dijo de qué fuente sacó la tasa?"*. Un solo eje, tres niveles,
   ejemplos concretos, regla de desempate.

---

## Lo que ya sabes

Después de este nivel puedes:

- **Convertir "a veces falla" en un número que otro puede reproducir.** Correr N
  veces, contar, y decir *"20%, entre 9.9% y 30.1%"* en vez de *"me parece que"*.
- **Saber cuándo tu número no significa nada.** `0/10` va de 0% a 30%; `3/9` va
  de 2.5% a 64%. La regla de tres para los extremos.
- **Poner un control**, y entender que no es relleno: el mismo prompt te dio 30%
  y 10% con veinte minutos de diferencia.
- **Elegir una métrica con poder.** La binaria solo usa los fallos; una que
  gradúa usa las 30 respuestas. Medir mejor sale más barato que medir más.
- **Probar tu medidor antes de medir**, con pares mínimos y gratis.
- **Separar lo que prueba tu código de lo que prueba el modelo**, y probar la
  primera mitad sin gastar un peso.
- **Escribir evals con casos hostiles**, que es lo único que encuentra agujeros
  como `startswith("s")`.
- **Escribir una rúbrica** con un solo eje, niveles separables, ejemplos
  concretos y regla de desempate.
- **Validar un juez** en tres pasos: contra etiquetas conocidas, contra sí mismo,
  y comprobando que no fabrica la evidencia.
- **Saber cuándo NO usar un juez**: si un `if` puede responderlo, el `if` gana en
  costo, en estabilidad y en acierto.

Y una duda vieja cerrada: **por qué aparecía el rioplatense.** El modelo elige
entre `ponte` / `ponete` / `póngase`, y **las tres son español correcto**. Nunca
fue un problema de idioma, sino de variedad — por eso dos niveles de "arreglos"
no lo tocaron.
