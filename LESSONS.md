# LESSONS.md — Lecciones aprendidas

> El **diario** del curso. Aquí va el *por qué*: las ideas que sobreviven aunque
> cambie el lenguaje, la librería o el proyecto.
>
> Este archivo **solo crece**. Nunca se borra una lección vieja: se le agrega un
> bloque nuevo por cada nivel terminado.
>
> ¿Buscas comandos y pasos? Eso está en `GUIDE.md`.

---

## Nivel 0 — Setup

### L0.1 — "Está configurado" y "funciona" son cosas distintas

Puedes tener la librería instalada, el archivo `.env` creado y la llave bien leída
por el programa... y aun así fallar. Sin saldo. Mal copiada. Un firewall en medio.

**Solo una llamada real lo demuestra.** Por eso `verificar.py` gasta 0.0002 centavos
en preguntarle una tontería a Claude. Es girar la llave del carro, no solo mirar el
tanque.

> Vale la pena gastar un poco para saber la verdad, en vez de asumirla gratis.

### L0.2 — Falla temprano, falla claro

Si algo esencial está mal, el programa debe reventar **al arrancar**, con un mensaje
útil. No a mitad de camino con un error críptico.

Un programa malo dice `Error`. Un programa bueno dice **qué pasó y qué hacer**:

```python
def fallar(mensaje, solucion):
    print(f"[FALTA] {mensaje}")
    print(f"        -> {solucion}")
    sys.exit(1)
```

Cada error del script trae las dos partes: diagnóstico + solución.

> Es la diferencia entre quedarte sin gasolina en el garaje o en la autopista.

### L0.3 — Cada falla distinta merece un mensaje distinto

Tres cosas pueden salir mal al llamar a la API, y cada una se arregla diferente:

| Error | Qué pasó | Qué hace el usuario |
|---|---|---|
| `AuthenticationError` | La llave está mal escrita | Volver a copiarla |
| `PermissionDeniedError` | La llave sirve, no hay saldo | Cargar crédito |
| `APIConnectionError` | No hay conexión | Revisar internet / VPN |

Agruparlas todas en un `except Exception` genérico destruye información que el
usuario necesita.

> **Esto ya es harness.** Manejar errores por tipo es la primera pieza real.

### L0.4 — Revisa de lo barato a lo caro

`verificar.py` chequea en este orden: versión de Python → librerías → existe la
llave → la llave funciona.

No al revés. Si Python es viejo, no tiene sentido gastar dinero llamando a la API
para descubrirlo.

> Ordena las validaciones por costo. La más barata primero.

### L0.5 — Un secreto nunca vive en el código

Una API key es una contraseña: quien la tenga gasta tu saldo.

Tres reglas que no se negocian:

1. **Nunca** dentro de un `.py`. Va en `.env`.
2. `.env` va en `.gitignore`, para que nunca salga de tu máquina.
3. **Nunca se imprime completa.** Solo lo justo para reconocerla:

```python
print(f"{api_key[:14]}...{api_key[-4:]}")
```

Así puedes decir *cuál* llave es, pero nadie la roba de una captura de pantalla.

### L0.6 — El código no debería ni tocar la llave

```python
cliente = anthropic.Anthropic()   # va vacío, a propósito
```

El SDK la busca solo en la variable de entorno. Si el código nunca la nombra, es
imposible que se te escape en un commit.

> El código más seguro es el que no existe.

### L0.7 — La respuesta de un LLM son bloques, no texto

Esto sorprende a todo el mundo:

```python
respuesta.content          # ❌ es una lista
respuesta.content[0].text  # ⚠️ funciona a veces — y por eso engaña
```

Piensa en un sobre de correo: adentro puede venir una carta, una factura y una foto.
Hay que mirar de qué tipo es cada papel.

La forma correcta es filtrar por tipo:

```python
texto = next(b.text for b in respuesta.content if b.type == "text")
```

**Por qué importa:** cuando el modelo *piensa* antes de responder, el bloque 0 es
razonamiento, no texto. El código que asumió `[0]` se rompe ese día.

### L0.8 — Suscripción y créditos de API son facturas distintas

| | Suscripción (Claude Pro / Code) | Créditos de API |
|---|---|---|
| Para qué | Que Claude **te ayude a ti** | Que **tus programas** hablen con Claude |
| Cómo se paga | Mensualidad fija | Por token consumido |
| Interfaz | App, terminal | Solo código |

La analogía: la suscripción es el electricista que te ayuda a instalar. La API key
es el **contador de luz** del aparato que instalaste.

Los $5 USD cargados en console.anthropic.com son lo segundo, no lo primero.

### L0.9 — El entorno virtual aísla el proyecto

`.venv` es una carpeta con las librerías **de este proyecto y nada más**.

Sin él, todo se instala globalmente: el proyecto A pide la versión 1 de una librería,
el proyecto B pide la versión 2, y algo se rompe sin que sepas por qué.

> El error más común del mundo: abrir una terminal nueva y **olvidar activarlo**.
> Si un `import` falla de repente, revisa eso primero.

---

## Nivel 1 — Primera llamada

### L1.1 — Comprobado en carne propia: el bloque 0 NO es texto

Con `max_tokens=30`, la respuesta de `claude-opus-5` fue:

```
stop_reason: max_tokens
numero de bloques: 1
  bloque[0] type='thinking'
```

**Un solo bloque, de tipo `thinking`. Cero bloques de texto.** El modelo gastó los
30 tokens pensando y no alcanzó a escribir ni una letra.

`respuesta.content[0].text` habría reventado con `AttributeError`.

> Esto ya no es teoría (ver L0.7): pasó en esta máquina, con este modelo, hoy.
> Opus 5 piensa antes de responder. Filtra por `type` **siempre**.

### L1.2 — Salida vacía no es lo mismo que error

No hubo excepción. La API respondió bien y cobró sus 30 tokens. Simplemente no
había nada de tipo `text` que imprimir.

Un programa que solo mira `content` le muestra una pantalla en blanco al usuario
y no sabe por qué. **`stop_reason` era el único que tenía la respuesta.**

> Revisa `stop_reason` **antes** de leer el contenido. Ese es el orden correcto.

### L1.3 — `max_tokens` es un cortacircuitos, no una sugerencia de longitud

No pide "una versión más corta". Corta en seco: a media palabra, o antes de que el
modelo llegue siquiera a empezar.

Si quieres respuestas breves, **pídelo en el prompt**. `max_tokens` es para que un
error tuyo no genere 50.000 tokens cobrados.

### L1.4 — La salida cuesta mucho más que la entrada

Medición real (Opus 5, misma llamada):

| | Tokens | $/1M | Costo |
|---|---|---|---|
| Entrada | 32 | $5 | $0.00016 |
| Salida | 205 | $25 | $0.00513 |

La salida fue **6x más larga** en tokens y **32x más cara**.

> Para controlar costo, mira primero cuánto **generas**, no cuánto envías.

### L1.5 — El modelo devuelve un formato; tu programa decide qué hacer con él

Claude escribe en Markdown por costumbre. En una terminal los `**asteriscos**` salen
crudos, porque la terminal no los interpreta.

No es un error del modelo: es una decisión que le toca al harness. O lo renderizas,
o lo limpias, o le pides en el `system` que no use Markdown.

### L1.6 — El mismo prompt no da la misma respuesta

Los LLM no son deterministas. Correr dos veces lo mismo produce textos distintos.

> Por eso probar un agente "a ojo" no sirve, y existe el nivel 5 (evaluación).

### L1.7 — El `system` es configuración, y se ve funcionando

Con `display: "summarized"` puedes **leer** cómo el modelo absorbe tus reglas antes
de responder. Medición real:

`SYSTEM` = *"profesor para principiantes, analogías primero, máx 4 frases, nunca
asumas inglés técnico"* → el pensamiento dijo: *"start with an analogy, keep it
brief, use straightforward language rather than jargon"*, y la respuesta cumplió
las 3 reglas.

Nada de eso estaba en el mensaje del usuario.

> Curiosidad comprobada: el modelo **piensa en inglés y responde en español**.
> El razonamiento interno no está atado al idioma de la conversación.

### L1.8 — El `system` controla el COSTO, no solo el tono

Misma conversación, solo cambiando el `SYSTEM`:

| `SYSTEM` | Entrada | Salida | Costo |
|---|---|---|---|
| Profesor (con "máx 4 frases") | 164 | 157 | $0.0039 |
| Pirata (sin esa regla) | 166 | **639** | **$0.016** |

**4x más caro sin tocar una sola línea del resto del programa.**

> El `system` no se edita por partes: es un texto entero. Al reemplazarlo se van
> todas las reglas viejas, incluidas las que no querías tocar.

### L1.9 — Las instrucciones pueden chocar, y la personalidad gana

En la corrida del pirata, el pensamiento decía explícitamente *"keeps it brief"*...
y aun así escribió 639 tokens con listas y bloque de código.

Dos órdenes contradictorias — *"sé un pirata teatral que regaña"* vs *"sé breve"* —
y el modelo resolvió el empate solo. Ganó el teatro.

> No es un fallo del modelo: le diste órdenes en conflicto.
> **Instrucciones medibles ganan a instrucciones vagas.** "Sé breve" es vago;
> "máximo 4 frases, sin listas, sin bloques de código" es verificable.

### L1.10 — Sin historial, la pregunta anterior simplemente no existe

Con dos preguntas seguidas del usuario y **sin** el turno `assistant` intermedio,
el modelo respondió **solo la última**. La primera quedó sin responder.

Los tokens de entrada bajaron de 166 a 137. Ojo: ese −29 es el **neto** de quitar
el turno `assistant` y añadir una regla nueva al `SYSTEM` a la vez — no mide el
costo del recuerdo por sí solo (ver L1.11).

> No se "olvida". La conversación entera es el archivo de texto que le mandas.
> Si ese archivo tiene un hueco, el hueco **es** la realidad para el modelo.

### L1.11 — Un experimento con 3 variables no prueba nada

La salida pasó de 639 a 333 tokens y por fin respetó el límite de frases.
Tentador concluir: *"borrar el turno `assistant` causó la brevedad"*.

**Falso.** Entre las dos corridas cambiaron **tres** cosas:

1. Se borró el turno `assistant`.
2. Se añadió al `SYSTEM` la regla medible *"máximo 4 frases, sin listas, sin
   bloques de código"*.
3. El azar — el modelo no es determinista (ver L1.6).

La hipótesis más fuerte es (2), y el pensamiento del modelo la respalda: pasó de
decir *"keeps it brief"* a decir *"keeping it to **four sentences maximum**"*.
Eso confirma L1.9. Pero **hipótesis fuerte ≠ prueba**, con n=1 de cada lado.

> Dos errores distintos, ambos fáciles de cometer:
> **(a)** mover varias variables a la vez y atribuírselo a una;
> **(b)** correr una sola vez un sistema no determinista y llamarlo resultado.
>
> El experimento correcto: mover **una** variable, y correr cada versión
> 5+ veces comparando promedios. **Eso ya es una evaluación** (nivel 5).

### L1.12 — El costo real = precio por token × tokens generados

Misma tarea trivial (clasificar un comentario), tres modelos:

| Modelo | Entrada | Salida | Costo |
|---|---|---|---|
| `claude-opus-5` | 70 | 161 | $0.004375 |
| `claude-sonnet-5` | 70 | 130 | $0.002160 |
| `claude-haiku-4-5` | 50 | **6** | **$0.000080** |

La diferencia de precio por token entre Opus y Haiku es 5x.
**La factura real fue 55x.**

Porque Opus generó **27 veces más tokens** para decir la misma palabra: en Opus 5
y Sonnet 5 **pensar está activado por defecto** (ver L1.1), y Haiku 4.5 no piensa
salvo que se lo pidas.

> No es solo "usa el modelo barato para tareas fáciles". Es que **el modelo caro
> aplica su capacidad aunque no la necesites, y te la cobra.** Le pagaste a Opus
> por deliberar si un comentario positivo es positivo.

**Añadido en la sesión 3 (no borres lo de arriba, es lo que se midió ese día):**
al repetir el MISMO script sin tocar una línea, la razón dio **30.9x**, no 55x.
Opus generó 85 tokens en vez de 133 esa vez. Lección de segundo orden: el costo
de un modelo que piensa **no es determinista**. Un solo experimento te da un
número, no *el* número. Quédate con el orden de magnitud —decenas de veces— y
si necesitas la cifra de verdad, mide varias corridas y promedia (nivel 5).

### L1.13 — Un número escrito a mano miente con confianza

El propio script imprimía *"Haiku cuesta 5x menos"* — texto fijo, escrito
razonando sobre la tabla de precios, sin medir. La medición dio 55x.

Lo mismo aplica al diccionario `PRECIOS`: está escrito a mano. Si Anthropic
cambia sus tarifas, el script mentirá con seis decimales de precisión.

> **Precisión no es exactitud.** Seis decimales bonitos no vuelven cierto un
> número. Todo dato fijo dentro del código es una mentira con fecha de
> caducidad — y no avisa cuando caduca.

### L1.14 — "Se cortó la respuesta" vs "mi código no la mostró"

La fila de Sonnet parecía truncada a media frase. No lo estaba: el script hacía
`texto.strip()[:30]` — **el propio código la recortaba** para la tabla.

Dos causas distintas que en pantalla se ven idénticas:

| Se ve | Causa real | Cómo distinguirlas |
|---|---|---|
| Texto cortado | El modelo topó `max_tokens` | `stop_reason == "max_tokens"` |
| Texto cortado | Tu código lo truncó al imprimir | `stop_reason == "end_turn"` |

> `stop_reason` es lo único que las separa — y ese script no lo imprimía.
> **Antes de culpar al modelo, revisa tu capa de presentación.**

Bonus del mismo caso: la respuesta traía saltos de línea en el medio y rompió la
tabla en tres renglones. `.strip()` limpia los extremos, no el interior.

### L1.15 — Cada familia de modelos cuenta tokens distinto

Exactamente el mismo texto de entrada:

| Modelo | Tokens de entrada |
|---|---|
| `claude-opus-5` | 70 |
| `claude-sonnet-5` | 70 |
| `claude-haiku-4-5` | **50** |

> Nunca estimes el costo de un modelo con tokens medidos en otro.
> Para contar de verdad existe el endpoint `count_tokens`, con el modelo real.

### L1.16 — "Acertaron" es una afirmación sin respaldo

Los tres respondieron POSITIVO a *"El envío llegó tarde **pero** el producto es
excelente"*. ¿Es positivo? ¿Neutro? **Nadie escribió nunca la respuesta correcta.**

Sin una respuesta esperada por escrito, "mi agente funciona" es una opinión.

Y hay una trampa práctica encima: Sonnet respondió `**POSITIVO**` con asteriscos
de Markdown. Un `if respuesta == "POSITIVO"` habría fallado con ese modelo.

> Escribir la respuesta esperada **antes** de correr = un caso de prueba.
> Muchos casos de prueba = una evaluación (nivel 5).

---

## Nivel 2 — La conversación con memoria

### L2.1 — La memoria es una lista, y es tuya

El modelo no recuerda nada. Lo que llamamos "memoria" es una lista de Python que
tú administras, y que se reenvía completa en cada llamada.

```python
historial.append({"role": "user", "content": entrada})
respuesta = cliente.messages.create(messages=historial)
historial.append({"role": "assistant", "content": texto})
```

Ese último `append` **es** la memoria. Bórralo y el chat pierde el hilo.

> El modelo es un sabio con amnesia encerrado en un cuarto. Cada vez le pasas
> por debajo de la puerta la transcripción completa. Él lee, responde y olvida.
> La transcripción la guardas tú, afuera.

### L2.2 — Si reenvías todo cada vez, pagas todo cada vez

Medido con preguntas de largo fijo: la entrada pasó de 43 a 511 tokens en seis
turnos. Las preguntas no crecieron; el historial sí.

La fórmula se comprueba restando:

```
entrada(n) = entrada(n-1) + salida(n-1) + tu mensaje
```

Cuadró en todos los saltos, en dos corridas independientes. No hay cobro oculto:
la entrada de un turno es literalmente todo lo anterior sumado.

### L2.3 — La forma del crecimiento la deciden las respuestas, no los turnos

Primero escribí que la entrada "crece como una escalera cada vez más alta".
Falso como regla general. **Cada escalón mide lo que mida la respuesta anterior.**

| | `SYSTEM` sin límite | `SYSTEM` con "máx. 2 frases" |
|---|---|---|
| respuestas | 99 → 217, crecen | ~71–93, planas |
| incrementos de entrada | 124, 177, 208, 238 | 99, 101, 81, 82, 105 |
| forma | acelerada | **recta** |

El acumulado sí crece más rápido que los turnos en ambos casos, porque cada
turno paga por todos los anteriores.

> Yo había generalizado desde un solo script. Un caso no es una ley.

### L2.4 — Un token de salida se vuelve a pagar como entrada, muchas veces

Dos corridas del mismo script: 27 tokens de salida de más costaron **145 tokens
de entrada de más**. Factor ~5x en una conversación de 6 turnos.

Lógico al verlo: lo que el modelo genera en el turno 1 se reenvía en los turnos
2, 3, 4, 5 y 6.

> Por eso un `SYSTEM` que pida respuestas cortas no ahorra una vez.
> **Ahorra en todos los turnos que vengan después.** La brevedad es una
> decisión de arquitectura, no de estilo.

### L2.5 — La entrada es determinista; la salida no

Tres scripts, dos máquinas, el mismo patrón: todo lo que es **texto que ya
existe** cuenta idéntico; todo lo que **genera el modelo** varía.

| | corrida A | corrida B |
|---|---|---|
| entrada del turno 1 | 43 | **43** |
| historial completo (`count_tokens`) | 418 | **418** |
| ventana deslizante | 127 | **127** |
| resumen (lo genera el modelo) | 308 | 293 |

> Sirve para depurar: si un número que debería ser determinista cambia entre
> corridas, **tú cambiaste algo**. Y si uno generado no cambia, sospecha.

### L2.6 — La ventana de contexto es un techo, no una pendiente

El dinero avisa poco a poco. La ventana no avisa: cuando el historial la pasa,
la llamada **falla**. No hay respuesta peor, hay error.

| Modelo | Ventana |
|---|---|
| `claude-opus-5` / `claude-sonnet-5` | 1.000.000 tokens |
| `claude-haiku-4-5` | 200.000 tokens |

Por eso un agente que corre horas necesita una política de recorte **antes** de
necesitarla.

### L2.7 — Olvidar no es un fallo del modelo: es una decisión de tu código

Al preguntarle a la ventana deslizante por un dato del primer turno:

> *"No tengo esa información. En esta conversación solo me has preguntado sobre
> errores de sintaxis y cómo leer mensajes de error."*

Esos dos temas son **exactamente** los últimos 4 mensajes del historial. No
alucinó ni se confundió: describió con precisión la lista que recibió.

> Su memoria *es* esa lista. Nada más. Lo que no le mandas, no existe.

### L2.8 — Cuatro políticas de recorte, ninguna correcta

| Estrategia | Costo | Qué conserva |
|---|---|---|
| Historial completo | crece sin techo | todo |
| Solo mensajes del usuario | mínimo | los hechos, no la coherencia |
| Ventana deslizante | bajo y estable | lo reciente |
| Resumen + recientes | medio | lo importante de todo |

La segunda apareció sola al hacer un ejercicio: el modelo recordaba los datos
del usuario y saludaba de nuevo en cada turno, porque no veía sus propias
respuestas.

> Elegir entre estas cuatro **es** el trabajo de harness. El modelo no participa
> en la decisión. Se elige por lo que tu producto no puede permitirse perder.

### L2.9 — Toda optimización tiene un costo que la tabla no muestra

La comparación decía que el resumen ahorra 30%. Pero **no incluía lo que costó
generar el resumen**: una llamada extra que no aparecía en ninguna columna.

Al medirla:

| | |
|---|---|
| Generar el resumen | $0.001077 |
| Ahorro por turno | $0.000117 |
| **Se paga solo en** | **~9 turnos** |

Si la conversación acaba en el turno 3, resumir fue tirar dinero.

> Convierte una intuición ("resumir ahorra") en una pregunta de ingeniería:
> **¿cuánto va a durar esta conversación?** Si no lo sabes, no sabes si tu
> optimización es una optimización.
>
> Regla general: cuando una tabla te convenza de algo, pregunta qué columna falta.

### L2.10 — El resumen es un prompt que tú escribes

Si el prompt de compactación pide "lista los temas", pierdes el nombre del
usuario. Si pide "conserva los datos concretos", lo mantiene.

Mismo código, misma estrategia, memoria distinta.

> La calidad de la memoria de tu agente es la calidad de un prompt tuyo.
> Cuando falle, el bug no está en el modelo.

### L2.11 — Un experimento tiene que poder fallar

La primera versión de la prueba de memoria preguntaba *"¿qué es una variable?"*.
Las tres estrategias respondieron bien — **incluida la que había borrado el
historial** — porque eso el modelo ya lo sabía.

El experimento no podía distinguir memoria de conocimiento general. No demostraba
nada, y aun así el texto afirmaba que sí.

La versión que funciona pregunta por un dato inventado (un nombre, un oficio) que
el modelo **no puede** saber de otro modo.

> Antes de correr un experimento: **¿qué resultado lo desmentiría?** Si no hay
> ninguno, no es un experimento. Es una demostración disfrazada.

### L2.12 — Un contador mal derivado no falla: miente

```python
f"[turno {len(historial) // 2}]"   # asume 2 mensajes por turno
```

Al cambiar la forma del historial, imprimió `0, 1, 1, 2`. Sin excepción, sin
error, sin aviso.

> Si quieres contar turnos, **cuenta turnos**. No deduzcas un dato de la forma de
> una estructura que puede cambiar.
> Los bugs que no revientan son los caros: sobreviven porque nadie los busca.

### L2.13 — Medir gratis existe, y tiene letra pequeña

`count_tokens` cuenta la entrada sin generar nada. Es gratis porque generar es
trabajo de GPU token a token, y contar es partir texto con un diccionario fijo.
Pesar el paquete es gratis; enviarlo se paga por peso.

Tres matices que solo aparecieron **al verificar una afirmación que era cierta**:

1. Es un **estimado**: el conteo real puede diferir un poco
2. Gratis ≠ ilimitado: tope de peticiones por minuto, independiente del de `create`
3. Solo cuenta la **entrada** — la salida no existe hasta que el modelo responde

> Verificar no sirve solo para cazar mentiras. Una afirmación verdadera pero
> incompleta te deja construir sobre supuestos falsos.

### L2.14 — Datos de prueba a mano: el ahorro más fuerte y el más traicionero

Hay dos categorías de ahorro, y no valen igual:

| | Ejemplos |
|---|---|
| Abaratar la llamada | modelo barato, `max_tokens` bajo |
| **Evitar la llamada** | `count_tokens`, historial fijo en el código |

Un historial escrito a mano no cuesta nada **y no vuelve a costar nada** por más
veces que corras el script. Repetible y gratis a la vez.

El precio se paga en otra moneda: lo escribes tú, así que sale demasiado limpio
—frases completas, sin erratas, sin divagaciones—. Las conversaciones reales no
se parecen.

> Puedes medir con precisión una situación que nunca ocurre, y que tu agente pase
> todas las pruebas y falle con el primer usuario. Usa datos falsos; pregúntate
> siempre si son representativos.

---

## Nivel 3 — Tu primer agente

### L3.1 — El modelo no ejecuta: pide

Es la idea que sostiene todo lo demás. Le das a Claude una lista de herramientas
y él devuelve **una petición escrita**: *"quiero `obtener_clima` con
`ciudad='Bogota'`"*. Nada más. No corre código, no abre una conexión, no toca un
archivo.

La prueba está en `01_pedir_herramienta.py`: declara la herramienta
`obtener_clima` y **en ese archivo no existe ninguna función con ese nombre**.
Funciona igual, porque nadie la ejecutó.

> Un agente no es un modelo más listo. Es un modelo más un programa que atiende
> sus peticiones. Ese programa es el harness, y lo escribes tú.

### L3.2 — Una herramienta es una descripción, no una implementación

Lo que se manda en `tools` es un diccionario con `name`, `description` e
`input_schema`. La función de Python vive aparte y el modelo nunca la ve.

Son dos mundos que solo se tocan en un punto: un diccionario que traduce el
nombre que dijo el modelo a la función real. Sin ese puente, `"obtener_clima"`
es un string sin dueño.

> Lo que el modelo conoce de tu herramienta es exactamente lo que escribiste en
> la descripción. Ni una línea del código real.

### L3.3 — Las descripciones son el programa

Con dos herramientas disponibles, el agente acertó las cuatro veces: usó
`hora_utc` para la hora, `obtener_clima` para el clima, lo pidió **dos veces**
para comparar dos ciudades, y **no usó ninguna** para una multiplicación.

No hay un solo `if` en el archivo que decida eso. Lo único que existe son las
`description`.

> Cambiar una descripción cambia el comportamiento del agente sin tocar una
> línea de código. Es la parte del programa que se escribe en español.

### L3.4 — `stop_reason` es el control de flujo del agente

En el nivel 1 era un dato curioso. Aquí es la condición del bucle:
`tool_use` significa *sigue*, cualquier otra cosa significa *para*.

> El modelo no solo devuelve contenido: devuelve el estado en el que quedó. Un
> harness que ignora `stop_reason` no sabe si terminó o si lo dejaron esperando.

### L3.5 — El `tool_use_id` es pegamento, no un registro

Parece un número de log. No lo es: es lo que empareja cada resultado con su
petición. Existe porque el modelo puede pedir varias herramientas a la vez y tú
puedes ejecutarlas en cualquier orden.

Inventar el id da un 400 inmediato.

> Cuando un identificador parece redundante, casi siempre es porque todavía no
> viste el caso donde hay más de uno.

### L3.6 — Lo que ve la API no es tu lista de Python

Dos descubrimientos que van juntos:

1. Al devolver un resultado hay que guardar **`respuesta.content` entero**, no
   solo el texto. En el nivel 2 bastaba el texto; aquí eso borra los bloques
   `tool_use` y rompe la conversación.
2. La API **fusiona los mensajes consecutivos del mismo rol**. Al quitar el turno
   `assistant` quedaron dos `user` seguidos, y la API los unió en uno: el
   resultado apareció como `content[1]` del mensaje 0.

> Tu estructura de datos y la que procesa la API se parecen, pero no son la
> misma. Cuando un error señale una posición que no cuadra con tu lista, esa es
> la pista.

### L3.7 — El texto de un error miente; la coordenada no

Los dos ejercicios de sabotaje dieron **la misma frase** —*cada `tool_result`
necesita un `tool_use` en el mensaje anterior*— con causas opuestas:

| Qué se rompió | Qué faltaba de verdad | Dirección |
|---|---|---|
| el id | el emparejamiento (había `tool_use`, con otro id) | `messages.2` |
| el turno `assistant` | el `tool_use` entero (no había ninguno) | `messages.0` |

En el segundo caso el id era **real y correcto**. El problema era que no había
ningún pedido al cual corresponder.

> Un 400 trae una dirección exacta dentro del JSON que mandaste. Léela antes que
> la frase: la frase es genérica, la coordenada es tu caso.

### L3.8 — En un bucle, el síntoma va una vuelta por delante de la causa

El id malo se escribe procesando la vuelta 1. El error estalla en la llamada de
la vuelta 2, cuando ese historial por fin se manda.

Y para entonces ya pagaste la vuelta 1 sin obtener nada.

> Un agente roto gasta antes de fallar. El punto donde revienta no es el punto
> donde te equivocaste.

### L3.9 — Una herramienta que lanza excepciones mata al agente

Al preguntar por una ciudad que no estaba en los datos, la función devolvió un
texto explicando el problema en vez de un `raise`. El modelo **lo leyó**, avisó
al usuario y ofreció alternativas. Nadie programó ese caso.

Una excepción no la lee nadie: mata el proceso.

> Todo `except` dentro de una herramienta debería terminar en
> `return "Error: ..."`. Un error convertido en texto es información que el
> modelo puede usar; un crash es el final de la conversación.

### L3.10 — Un agente cuesta el doble, como mínimo

Una pregunta con herramienta son **dos** llamadas a la API. Y la segunda es más
cara, porque reenvía el menú, la petición del modelo y el resultado.

Tres preguntas con Opus costaron ~$0,030. Seis preguntas del nivel 2 con Haiku
costaron $0,0041: **7 veces menos con el doble de preguntas.** Dos
multiplicadores apilados, el modelo y el bucle.

> "Convertirlo en agente" no es una mejora gratis: es como mínimo duplicar la
> factura de cada interacción.

### L3.11 — Lo que devuelve tu herramienta se reenvía para siempre

Restando `entrada(v2) − entrada(v1) − salida(v1)` se ve el peso exacto del
resultado: 18 tokens un dato normal, **46 un mensaje de error largo**.

Y ese texto viaja en todas las vueltas siguientes, igual que el historial del
nivel 2.

> Recortar lo que devuelven las herramientas es trabajo de harness, exactamente
> igual que recortar el historial. Una herramienta que devuelve un JSON gigante
> sale cara para siempre, no una sola vez.

### L3.12 — El menú de `tools` es una suscripción fija

La pregunta "¿cuánto es 17 por 23?" no usó ninguna herramienta y aun así pagó
605 tokens de entrada. La pregunta pesa ~10; el resto es el `SYSTEM` y las **dos
descripciones**, que viajan en cada llamada se usen o no.

Dos herramientas ≈ 600 tokens. Cuarenta herramientas, miles — en cada pregunta,
incluso en las que no tienen nada que ver.

> Agregar una herramienta no es gratis: es un costo que pagas en todas las
> llamadas futuras del agente.

### L3.13 — Con datos reales, el costo deja de ser determinista

Con el clima falso (un diccionario), el peso del `tool_result` era idéntico entre
corridas. Con la API real, dos corridas de la misma pregunta dieron 709 y 714
tokens de entrada — y la salida del modelo había sido **la misma** (59 en las
dos).

La diferencia la puso el cielo: `nublado` contra `parcialmente nublado`.

> El costo de un agente depende de datos que no controlas. No se puede
> presupuestar exacto; solo se puede acotar cuánto devuelven las herramientas.

### L3.14 — La estructura de la respuesta tampoco es determinista

El mismo script, corrido dos veces, devolvió **1 bloque** una vez y **2** la
otra: en la segunda el modelo decidió razonar antes de pedir, y apareció un
bloque `thinking` delante del `tool_use`.

Eso convierte el atajo `content[0]` en un bug intermitente:

```python
respuesta.content[0].name    # corrida A: funciona
                             # corrida B: revienta
```

> L1.6 decía que el texto cambia entre corridas. Esto es peor: cambia la
> **forma**. El mismo código pasa en una máquina y falla en otra sin que nadie
> haya tocado nada.

### L3.15 — "Español" no es una especificación

Se puso `SYSTEM: "Responde en espanol"` esperando anclar la voz, y el modelo
respondió en rioplatense a un usuario colombiano (*"si me decís tu ciudad"*).
El `SYSTEM` pedía un idioma; el dialecto lo siguió eligiendo él.

Peor: pasó en **1 de 4** respuestas. Un defecto que aparece el 25% de las veces
no se detecta probando una vez.

> Una instrucción vaga no es una instrucción a medias: es una decisión que le
> delegaste al modelo sin darte cuenta. Y los defectos intermitentes son más
> caros de encontrar que los constantes.

### L3.16 — El tope de vueltas es el único freno que tiene el agente

`max_vueltas` es un número escrito a mano en un `range()`. Es lo único que impide
que un modelo confundido pida la misma herramienta indefinidamente, pagando una
llamada cada vez.

> Todo bucle agéntico necesita un tope desde la primera versión. Es débil, pero
> la alternativa es un bucle infinito que factura.

---

## Nivel 4 — El harness real

### L4.1 — Reintentar solo sirve para lo que es temporal

Un `AuthenticationError` (401) dentro de cinco minutos sigue siendo un 401. Un
`APIConnectionError` puede desaparecer solo. La diferencia no es de gravedad:
es de **quién tiene la culpa y si el tiempo la arregla**.

- Permanente (401, 404, 400): arregla el código. Reintentar solo gasta tiempo.
- Temporal (429, 5xx, red): espera y vuelve.

> No escribas tu propia lista de códigos HTTP. Las clases de excepción del SDK
> ya hacen esa división, y la mantienen ellos.

### L4.2 — Un error puede morir en tres sitios distintos

Provocando cinco fallas seguidas aparecieron tres fronteras, no una:

1. **En tu máquina** — `ValueError`. El SDK revisó la petición y se negó a
   mandarla. No hubo red ni cuenta ni factura.
2. **En la red** — `APIConnectionError`. Salió, no llegó a ningún lado, nadie
   contestó. No hay código HTTP que mirar.
3. **En el servidor** — `AuthenticationError`, `NotFoundError`,
   `BadRequestError`. Hubo respuesta, con su número.

> "Falló la API" es tres diagnósticos distintos con el mismo nombre. Antes de
> buscar la causa, decide en cuál de las tres fronteras murió.

### L4.3 — El orden de los `except` es el programa

Van de lo más específico a lo más general. Python entra al primero que coincida.
Si `APIStatusError` va arriba, se traga los 401, 404 y 400, y pierdes justo la
información con la que ibas a arreglarlos.

Y `APIConnectionError` **no** es hijo de `APIStatusError`: cuando no hubo
respuesta HTTP no hay estado que reportar. Un `except APIStatusError` que
crees que atrapa todo, no atrapa el día que se cae el wifi.

### L4.4 — Lo que ya estaba pasando sin que lo vieras

`max_retries=2` es el valor de fábrica del SDK. Cada `messages.create()` de los
niveles 1, 2 y 3 podía hacer **hasta 3 peticiones**, en silencio, sin imprimir
nada. Nunca se notó porque nunca falló nada.

> Los valores por defecto de una librería son decisiones que alguien tomó por
> ti. Siguen ahí aunque no las hayas leído.

### L4.5 — El timeout es por intento, no por operación

Medido: `timeout=1s` con `max_retries=0` tarda 1.00 s en fallar; con
`max_retries=2` tarda 4.20 s. Tu paciencia real es
`timeout × (max_retries + 1)` más las esperas entre intentos.

Con los valores de fábrica (10 minutos, 2 reintentos) eso es **media hora**.

> Los dos números se eligen juntos. Un timeout corto con muchos reintentos no
> es un timeout corto.

### L4.6 — Reintentos anidados se multiplican

3 reintentos tuyos × 3 del SDK = **9 peticiones** y el triple de factura, por
una sola llamada que escribiste. Si pones el tuyo, apaga el suyo
(`max_retries=0`).

> Antes de escribir una protección, averigua si ya existe. Dos protecciones
> para lo mismo no suman: se multiplican.

### L4.7 — El presupuesto se revisa antes de gastar

`if gastado >= PRESUPUESTO: parar` va **antes** de la llamada, no después.
Revisarlo después es contar el dinero que ya no tienes. Vale igual para el tope
de vueltas: los frenos se pisan antes de la curva.

### L4.8 — Los permisos viven en tu código, no en el prompt

La política es un diccionario de Python (`PERMISOS`), no una frase en la
`description` de la herramienta.

Lo que el modelo **lee**, el modelo lo puede ignorar, malinterpretar, o lo
pueden convencer de ignorar. Lo que está en tu `if`, no.

Corolario: lo desconocido se prohíbe (`PERMISOS.get(nombre, "prohibir")`). Si
mañana agregas una herramienta y olvidas darle política, no corre. El olvido
falla hacia el lado seguro.

### L4.9 — Negar en silencio convierte al agente en mentiroso

Al rechazar un permiso hay que devolverle al modelo un `tool_result` que lo
diga: *"PERMISO DENEGADO"*. Con ese texto, el modelo contestó *"no pude
borrarlo: el sistema negó el permiso"*. Con silencio o texto vacío, habría
seguido creyendo que se hizo y le habría dicho al usuario **"listo, ya lo borré"**
con el archivo intacto.

> El modelo solo sabe lo que le devuelves. Un fallo que no le cuentas se
> convierte en una afirmación falsa dicha con total confianza.

### L4.10 — Dos candados para la misma puerta

Además del permiso, `borrar_archivo()` comprueba por su cuenta que el archivo
esté dentro de `caja/`. El permiso protege contra un modelo equivocado; la
comprobación protege contra un **humano distraído** que dio permiso sin leer.

> Las capas de seguridad se ponen suponiendo que la anterior va a fallar.

### L4.11 — Sin registro, solo tienes tu memoria

`registro.jsonl` guarda una línea por evento: cada llamada con su costo y su
duración, cada herramienta con lo que pidió y lo que le contestamos, cada
permiso con quién lo dio. Formato JSONL porque se lee con los ojos, se puede
abrir a mitad de escritura y se procesa sin cargarlo entero.

> El día que el agente haga algo raro, el registro es la diferencia entre
> explicarlo y adivinarlo.

### L4.12 — Streaming no acelera: adelanta

Medido en una corrida: primera palabra a los 11.9 s sin streaming, a los 8.6 s
con streaming. El total depende del largo de la respuesta; **el arranque no**.
Lo que se gana no es velocidad, es que el programa deje de parecer colgado.

> **Números corregidos después** (ver L4.24): con el orden del experimento
> controlado, el adelanto real es **~6.3 s**. Esa métrica se llama **TTFT**
> (*Time To First Token*), y con modelos que razonan hay dos —el primer token de
> cualquier tipo y el primero de texto— que hay que distinguir (L4.25).

Y no es solo estética: para respuestas grandes el SDK **se niega** a hacer la
petición sin streaming.

> Toda pieza del harness es un intercambio. Streaming cuesta un caso más que
> manejar: el stream que se corta a la mitad.

### L4.13 — La explicación cómoda no es la explicación correcta

En el nivel 3 el modelo respondió en rioplatense a un usuario colombiano y la
conclusión fue: *el `SYSTEM` decía solo "en español", faltó anclar la variedad*
(L3.15). En el nivel 4 el `SYSTEM` dice **"español de Colombia"** — y apareció
igual, en 1 de 3 respuestas.

La explicación del nivel 3 era razonable, encajaba con los datos, y no era
suficiente. Lo que la delató fue volver a medir con la causa supuestamente
arreglada.

> Una hipótesis que explica lo que viste no está confirmada hasta que arregles
> la causa y el defecto desaparezca. Si arreglas la causa y sigue ahí, la
> hipótesis era incompleta. Repetido: los defectos intermitentes tampoco se
> **diagnostican** con una sola corrida.

### L4.14 — La infraestructura sí es determinista, aunque el modelo no

Las 5 clasificaciones de `01_errores.py` salieron **idénticas** en dos máquinas
distintas. Es la primera cosa perfectamente repetible del curso, y tiene
explicación: en ese script el modelo nunca genera nada — las 5 peticiones mueren
antes de llegar a él. Lo único que cambia entre corridas es el `request_id`.

Lo no determinista siempre fue **la generación**, no la infraestructura.

> Y de ahí sale que el nivel 5 sea posible: tu harness sí se puede probar de
> forma repetible, aunque lo que el modelo escribe no.

### L4.15 — Clasifica por clase de excepción, nunca por el texto del mensaje

Los mensajes de error son de calidad muy desigual. El 404 dice solo
`model: claude-opus-9-mil` — te repite lo que mandaste y no ayuda. El 400 dice
`` `temperature` is deprecated for this model `` — te dice qué hacer.

Y el texto lo cambia el proveedor cuando quiera, sin avisar. La clase de la
excepción, no.

> Un `if "not found" in str(e)` se rompe el día que cambien una palabra. Un
> `except NotFoundError` no.

### L4.16 — Antes de recortar un error, mira si el SDK ya te lo dio parseado

`01_errores.py` imprimía `e.message[:80]` y el corte caía a mitad del JSON crudo,
justo antes del mensaje útil: los casos 401 y 404 salían ilegibles. La solución
no fue subir el número — fue entrar a `e.body`, el JSON **ya parseado** que el
SDK te entrega, y sacar `body["error"]["message"]`.

Regalo inesperado: ahí venía también el **`request_id`**, el número que se le da
a soporte de Anthropic para que encuentren tu petición. Estaba desde siempre,
escondido detrás del corte.

> Tercera vez que el mismo patrón aparece en el curso (ver L1.14). **Cuando un
> dato salga truncado o raro, sospecha primero de tu propio `print`.** Y recortar
> a mano suele ser señal de que no buscaste el campo bueno.

### L4.17 — Un número solo significa algo al lado de otro número

Los tiempos de `02_reintentos.py` no se repitieron entre máquinas (0.22 / 0.39 /
1.34 / 3.39 contra 0.31 / 0.50 / 1.34 / 3.00). El orden y las proporciones,
enteros. La conclusión sobrevivió; los valores no.

Lo mismo con el streaming: 1.38x de adelanto en una máquina, 2.3x en otra, misma
dirección. Y lo mismo con `max_retries=5` sobre un 401: los 0.41 s solo
significan algo puestos al lado de los 3.00 s de tres reintentos reales.

> Un script de tiempos se lee comparando filas entre sí, nunca contra un número
> fijo. Y hay que saber cuándo una coincidencia es mecánica (el mismo texto de
> entrada da el mismo conteo) y cuándo es casualidad — el `1.34 s` que salió
> igual en las dos corridas es casualidad.

### L4.18 — Lo que no puedes medir directo: fija todo lo demás y réstalo

La espera del backoff del SDK no se puede leer en ningún sitio. Pero con
`timeout=1s` cada intento cuesta exactamente 1.00 s, así que la resta la deja
sola: **4.36 − 3.00 = 1.36 s** en una máquina, 1.20 s en la otra. Casi igual en
dos redes distintas, porque es un `sleep` del SDK y no depende de la red.

Misma técnica que en el nivel 2 para pesar las preguntas dentro del historial.

> Cuando una medición mezcla dos cosas, no busques una herramienta mejor:
> **construye un caso donde todo lo demás sea constante** y resta.

### L4.19 — El caso general del `except` atrapa hijos que no sabías que existían

En `02_reintentos.py` apareció `APITimeoutError`, que no había salido nunca en el
script 1. Y se reintenta igual que `APIConnectionError` — porque **hereda de
ella**.

> Es la contraparte de L4.3 (el orden de los `except` es el programa): el orden
> importa porque el caso general **sí** atrapa cosas que no enumeraste. Eso es un
> peligro cuando va primero y una red de seguridad cuando va último.

### L4.20 — El camino de error cuesta más que el camino feliz

Negar el permiso de borrado costó **más** que concederlo. Desglosado con el
registro, la vuelta siguiente al rechazo:

- **+15 tokens de entrada** — `PERMISO DENEGADO: ...` es un texto más largo que
  `Borrado 'borrador.txt'.`
- **+19 tokens de salida** — el agente tiene que **explicarse**, y explicarse es
  más largo que confirmar.

Los dos lados suben a la vez. La cuenta cuadra exacta: 15 × $5/M + 19 × $25/M =
$0.00055, la diferencia medida.

> Al presupuestar un agente es tentador calcular con el caso que funciona. El
> caso que falla es el caro, y es el que se repite cuando algo va mal.

### L4.21 — El registro contesta preguntas que ninguna otra pieza puede contestar

Dos líneas seguidas de `registro.jsonl`:

```
11:03:14  llamada_api   segundos: 3.98
11:04:01  herramienta   borrar_archivo
```

47 segundos entre las dos. La API tardó 3.98; los otros 43 fue **el humano**
decidiendo si daba el permiso.

Si mañana alguien reporta que "el agente es lentísimo", ninguna de las otras
cinco piezas del harness puede decirte que el cuello de botella no era el modelo.
El registro sí, y sin que nadie lo hubiera previsto al escribirlo.

> Un registro se escribe antes de saber qué pregunta le vas a hacer. Ese es
> justamente el motivo de escribirlo: los eventos que anotas hoy son las
> preguntas que podrás responder dentro de seis meses.

### L4.22 — Cuando dos mediciones no son comparables, busca una razón

Streaming: 13.2 s contra 13.9 s parece "casi igual". Mal leído: las dos
respuestas no midieron lo mismo (691 contra 814 tokens de salida).

Dividiendo quedan comparables: **52.3 contra 58.6 tokens por segundo**.

> Comparar totales de cosas que no hicieron el mismo trabajo es la forma más
> fácil de sacar una conclusión falsa con datos verdaderos. Normaliza: por token,
> por llamada, por segundo.

**Y la segunda mitad de la lección, que costó una corrección:** de esa razón
concluí *"con streaming se genera más texto por segundo"*. La corrida siguiente
dio **56.6 contra 52.8** — al revés. Las cuatro llamadas caen entre 52 y 59
tok/s: la diferencia era **ruido**, y yo le puse dirección.

> Normalizar arregla que las magnitudes sean comparables. **No arregla que n=1.**
> Son dos defectos distintos y hay que arreglar los dos. → L1.13 otra vez, ahora
> disfrazada de aritmética.

### L4.23 — Un defecto intermitente además se mueve de sitio

El rioplatense apareció en **1 de 3** respuestas en cada una de las tres corridas
del harness — pero nunca en la misma. En una salió en la respuesta 2, en la otra
en la respuesta 1.

> No basta con repetir para *ver* el defecto: hay que repetir para saber **dónde**
> aparece. Un caso de prueba que solo mira la respuesta 2 lo habría declarado
> arreglado. Contar es el nivel 5.

### L4.24 — Para separar un efecto de su sesgo, cruza las dos posiciones

El experimento del streaming corría la forma sin streaming **primera**, y la
primera llamada del programa paga la apertura de la conexión. Sospecha razonable:
parte de la ventaja no era del streaming.

No se resuelve discutiéndolo. Se corre **cada forma en cada posición** — cuatro
datos en vez de dos:

| | primera | segunda |
|---|---|---|
| sin streaming | 13.2 s | 12.3 s |
| con streaming | 7.1 s | 5.8 s |

- **Por filas** sale el sesgo: +0.9 s y +1.3 s de castigo por ir primero. Abrir
  la conexión cuesta ~1 s.
- **Por columnas** sale el efecto limpio: 6.1 s y 6.5 s de ventaja del streaming.

Resultado: la conclusión aguantó y **la magnitud estaba inflada ~15%** (7.4 s
medidos contra ~6.3 s reales).

> Un control bien hecho casi nunca tumba el resultado: lo **corrige**. Y cuando
> el mismo número te sale por dos caminos distintos —dos filas, dos columnas—
> deja de ser casualidad. Es la misma idea de L4.18 (fija todo lo demás y resta),
> con una variable más.

### L4.25 — Una hipótesis puede ser correcta y aun así estar incompleta

La hipótesis del silencio del streaming era: *"la pantalla está quieta porque
`text_stream` no entrega los bloques `thinking`"*. Al medirla con el stream crudo,
el mecanismo salió exacto: el `thinking` va primero, el texto no empieza hasta
que cierra.

Y aun así estaba a medias. El silencio se parte en dos:

```
0.00 → 1.95 s   nada todavia (conexion + peticion + arranque del servidor)
1.95 → 4.23 s   el bloque thinking
```

El thinking explica **la mitad**. Confirmar el mecanismo no era confirmar que
fuera *toda* la causa.

Y hay un premio por medir: el **~1 s de apertura de conexión** que salió del
ejercicio 9 vive dentro de esos 1.95 s. **El número de un experimento apareció
dentro de otro** — que es la señal más fuerte de que los dos midieron algo real.

> "Encaja con lo que veo" y "es la explicación completa" son dos afirmaciones
> distintas, y la primera no implica la segunda. → L4.13, pero esta vez atrapada
> al medirla en vez de tres niveles después.

### L4.26 — Un costo invisible sigue estando en la factura

`usage: 52 in / 654 out` para una respuesta de ~200 palabras (unos 350 tokens).
Los otros **~300 fueron razonamiento facturado**, del que solo se ve un resumen
de una línea — y solo si pides `display: "summarized"`.

Lo grave no es eso: es que **las corridas anteriores lo pagaban igual**. 691,
814, 802 y 696 tokens de salida para la misma pregunta, con `display` en su
valor de fábrica `"omitted"`. Nadie lo vio nunca.

> El parámetro decide si te lo **enseñan**, no si **ocurre** ni si **se cobra**.
> Un gasto que no aparece en ninguno de tus logs no es un gasto que no existe —
> es uno que no sabes explicar cuando llegue la factura. Es el argumento del
> `registro.jsonl` (L4.21) llevado a su conclusión: solo puedes auditar lo que
> decidiste anotar, y solo puedes anotar lo que sabes que existe.

---

## Nivel 5 — Evaluación

### L5.1 — Cuando el resultado no se repite, un solo resultado no es evidencia

La pregunta madre del curso, abierta desde el nivel 1 (L1.6, L1.11, L1.16), se
cierra aquí. Y la respuesta cabe en cuatro pasos: **corre N veces, cuenta, pon un
control al lado, y mira si los rangos se solapan antes de declarar nada.**

Los números lo dicen mejor que cualquier explicación. Las mismas mediciones,
convertidas en rango creíble al 95%:

| dato | de dónde salió | rango real |
|---|---|---|
| `3/9` | el "1 de cada 3" de los niveles 3 y 4 | **2.5% – 64%** |
| `0/10` | el primer experimento de este nivel | **0% – 30%** |
| `12/60` | las 60 corridas del mismo prompt | **9.9% – 30.1%** |

> Durante dos niveles enteros, el "1 de cada 3" era compatible con casi
> cualquier cosa. Servía para **sospechar**, nunca para **afirmar**. Y el `0/10`
> era perfectamente compatible con un defecto del 30% — que resultó ser el real.

### L5.2 — Prueba tu medidor antes de medir, y hazlo gratis

Si el detector miente, el experimento entero miente — y con toda la apariencia
de rigor, porque igual imprime un número bonito.

`00_probar_detector.py` no llama a la API ni una vez: **cuesta $0.00 y da
idéntico siempre**. Ese hábito se pagó solo dos veces en una sola sesión (ver
L5.4 y L5.10), encontrando dos bugs antes de gastar un peso.

> Primero prueba lo que puedes probar gratis y con certeza. Deja la API para lo
> único que de verdad la necesita.

### L5.3 — Pares mínimos: dos frases que se diferencian en una sola cosa

Es la forma de probar un detector. `"Llevá campera"` contra `"Lleva sombrilla"`.
`"Ponte"` contra `"Póngase"`. `"Estas cosas"` contra `"Si estás"`.

> **Si los dos miembros del par dan el mismo veredicto, tu detector no está
> mirando lo que crees que mira.**

Es la misma técnica del ejercicio 9 del nivel 4 (L4.24): para aislar un efecto,
cambias una cosa y dejas todo lo demás igual.

### L5.4 — El preprocesamiento puede destruir justo la señal que buscas

```
"Lleva sombrilla"   <- Colombia, correcto
"Llevá sombrilla"   <- rioplatense
```

La única diferencia es la tilde. La primera versión del detector **quitaba
tildes antes de comparar**, así que habría marcado la forma colombiana correcta
como defecto.

Es la tercera cara del mismo error: el `[:30]` del nivel 1 **cortaba** el dato,
el `[:80]` del nivel 4 lo **escondía**, y aquí `normalizar()` lo **borraba**.
Y volvió a aparecer una cuarta vez en la misma sesión, cuando mi propio análisis
del juez comparaba `pongase` contra `póngase` y estuvo a punto de acusarlo de
inventarse lo que sí había dicho.

> Antes de comparar, mira qué le hiciste al dato para poder compararlo.

### L5.5 — Un experimento que cambia las condiciones y sale limpio no prueba nada

El primer intento dio **0 de 10**, contra un histórico de 3 de 9. Parecía que el
defecto había desaparecido. Pero seis de esas diez respuestas eran
*"no puedo consultar el clima"*: se le preguntó por el clima de hoy a un modelo
**sin herramientas**, y nunca llegaba a la parte donde el defecto vivía.

> **`0 de 10` no refuta `3 de 9` si no midieron lo mismo.** No demuestra que
> arreglaste algo: demuestra que dejaste de mirar donde estaba.

Es el error de `03_recortar.py` del nivel 2 (L2.11) con otra ropa: una prueba que
corre, que no revienta, y que no prueba lo que dice probar.

### L5.6 — Contar N veces te enseña cosas que no fuiste a buscar

Leyendo esas mismas 10 respuestas apareció un defecto que nadie perseguía: el
modelo trataba de **tú** en 4 y de **usted** en 5, con el mismo prompt. Y en 2 de
30 llegaba a mezclar los dos **dentro de una misma respuesta**.

> El valor de correr N veces no es solo el número que ibas a buscar. Es que N
> respuestas puestas en columna hacen visible lo que una sola esconde.

### L5.7 — Un defecto difuso puede vivir en una sola palabra

*"A veces habla argentino"* sonaba a problema de estilo, de voz, de
personalidad. Contando 30 corridas resultó ser esto:

| forma | cuántas | qué es |
|---|---|---|
| `ponte` | 18 de 30 | tú, colombiano correcto |
| `ponete` | **9 de 30** | rioplatense |
| `póngase` | 2 de 30 | usted |

**Los 9 rioplatenses eran exactamente las 9 respuestas con `ponete`.** La
respuesta era casi idéntica siempre; lo único que bailaba era la conjugación del
primer verbo.

Y ahí está por qué dos niveles de "arreglos" no funcionaron: **las tres formas
son español correcto.** Decir *"responde en español de Colombia"* no elige entre
ellas. El problema nunca fue el idioma, fue la **variedad**.

> Un defecto que parece difuso muchas veces es un defecto concreto que todavía no
> has localizado. Búscalo antes de intentar arreglarlo.

### L5.8 — El control no es relleno

Correr la versión sin cambios, al lado de las versiones nuevas, parecía gasto
inútil. Dio esto:

| | mismo prompt exacto | rioplatense |
|---|---|---|
| v2 | entrada 108 tokens | 9/30 = **30%** |
| v3-A | entrada 108 tokens | 3/30 = **10%** |

Misma máquina, mismo modelo, veinte minutos de diferencia. Los rangos se tocan,
así que el azar basta para explicarlo — pero la lección es que **con N=30 el
mismo prompt dio 30% y 10%**, y eso solo se supo porque había un control.

> El control es lo que te dice si tu regla de medir sigue siendo la misma regla.
> Sin él, habrías comparado los arreglos contra un número viejo y habrías
> concluido de más.

### L5.9 — No hace falta gastar más: hace falta medir mejor

La pregunta binaria *(¿hubo rioplatense, sí o no?)* no separaba las versiones:
los rangos se solapaban y el script decía, correctamente, "no demostrado".

Cambiando la pregunta a *(¿qué forma del verbo usó?)* —que tiene señal en las 30
respuestas y no solo en las 3 malas— todo se separó:

| | dijo `ponte` | rango |
|---|---|---|
| A (control) | 19/30 = 63% | 46% – 81% |
| B (prohibir voseo) | 30/30 = 100% | 90% – 100% |
| C (mover al usuario) | 28/30 = 93% | 84% – 100% |

Mismos datos, mismo dinero, otra pregunta.

> **Si tu métrica solo mira los fallos, tiras a la basura la información que
> traen los aciertos.** Una métrica que gradúa siempre tiene más poder que una
> que solo dice sí/no.

⚠️ Con una salvedad: elegir la métrica *después* de ver los datos es una trampa
clásica — buscas hasta que algo salga significativo. Aquí no aplicaba porque la
métrica se escribió antes de correr el experimento, pero hay que desconfiar
siempre que alguien cambie de métrica justo cuando la primera no le dio lo que
quería.

### L5.10 — El peor bug de un eval no revienta: miente con cara de matemática

La primera versión de la función que calculaba la confianza devolvía `±0.0`
cuando salían 0 aciertos. Es decir: *"0 de 30 significa defecto eliminado, con
certeza total"*.

Es falso. Un defecto del 5% tiene ~21% de probabilidad de no aparecer ni una vez
en 30 corridas. La fórmula normal se cae justo en los extremos — que es
precisamente donde cae un arreglo que funciona.

Se arregló con la **regla de tres**: si no viste ninguno en `n` intentos, el tope
al 95% es `3/n`. Con n=30, eso es **10%, no 0%**.

> Un eval roto que lanza una excepción se arregla en cinco minutos. Un eval roto
> que devuelve un número plausible te miente durante meses.

### L5.11 — La mitad de tu agente se prueba gratis

Tu agente son dos cosas pegadas, y se prueban de formas opuestas:

| | qué decide | cómo se prueba |
|---|---|---|
| **El modelo** | qué herramienta pedir, qué texto escribir | caro, N veces, contando |
| **El harness** | presupuesto, permisos, timeouts, topes, registro | **gratis, con certeza, mil veces** |

Los seis frenos del nivel 4 no tienen nada de probabilístico: `PRESUPUESTO_USD`
o corta o no corta; `PERMISOS` o deniega o no deniega. Se apoya en L4.14, que se
midió en el nivel anterior.

> Esa frontera vale para todo lo que construyas después. Antes de escribir un
> eval, pregunta de qué lado cae lo que quieres probar.

### L5.12 — Para poder probar tu código, tiene que poder cargarse sin ejecutarse

`03_harness.py` no tenía `if __name__ == "__main__"`. Importarlo para probar sus
piezas lo arrancaba entero: creaba carpetas, hacía las 3 preguntas, gastaba los
$0.03 y se quedaba esperando que alguien tecleara `s`.

> El `if __name__` no es decoración: separa **"este archivo *es* un programa"** de
> **"este archivo *ofrece* piezas"**. Es un defecto que solo aparece el día que
> intentas probar.

### L5.13 — Un eval vale por sus casos hostiles, no por los felices

Los 24 evals del harness encontraron un agujero de seguridad real:

```python
if respuesta.startswith("s"):     # <- el permiso para borrar archivos
```

**Cualquier palabra que empiece por `s` autorizaba el borrado**, incluidas justo
las que teclea alguien que quiere abortar: `salir`, `stop`, `suspende`,
`sal de ahí`. El freno se abría con la palabra que uno escribe para cerrarlo.

Probar `"s"` y `"n"` habría pasado. Lo encontró el caso que probaba trece teclas
hostiles.

> Escribir un eval es preguntarse *"¿cómo rompería esto alguien que no me quiere
> bien — o alguien nervioso?"*.

### L5.14 — Un principio aplicado en un sitio no se aplica solo en el de al lado

`PERMISOS.get(nombre, "prohibir")` es denegar-por-defecto perfecto.
`respuesta.startswith("s")` es exactamente lo contrario. **Están en la misma
función, con tres líneas de diferencia**, y nadie lo vio en dos sesiones de leer
ese archivo.

> Cuando adoptes un principio, búscalo en todos los sitios donde debería estar.
> Es la regla de la sesión 3 ("al corregir una afirmación, búscala en todos los
> archivos") aplicada al diseño en vez de al texto.

### L5.15 — Si un `if` puede responder la pregunta, no uses un juez

Se intentó usar un modelo para detectar dialecto. Tres versiones de la rúbrica,
y el acuerdo con el detector determinista fue empeorando: **83% → 75% → 42%**.

El diagnóstico no era la rúbrica: era la tarea. Detectar si aparecen palabras de
una lista es **comparación de cadenas**, y ahí el `if` gana en todo:

| | detector (`if`) | juez (Haiku) |
|---|---|---|
| costo | $0.00 | cuesta |
| estabilidad | 100% | 92% |
| acierto en dialecto | validado con pares mínimos | 42% |

Y el error del juez era siempre el mismo: no distingue `lleva` de `lleve`, ni
`ponte` de `ponete` — **una letra**.

> **Distinciones ortográficas: `if`. Comprensión del contexto: juez.** Los
> modelos son malos precisamente en lo que un `if` hace perfecto.

### L5.16 — Cuando dos evaluadores discrepan, sospecha primero de la rúbrica

El juez calificó como *"colombiano"* un texto que decía `ponete`, y **citó
`ponete` como prueba de que era colombiano**. Parecía autopreferencia pura.

No lo era del todo: el texto era una mezcla real —`ponete` junto a `buso`,
`harto`, `sombrilla`— y **la rúbrica no decía qué hacer cuando hay señales de
varios niveles a la vez**. El juez desempató por mayoría, que es razonable y era
lo contrario de lo que se quería.

> Una rúbrica sin regla de desempate no es una rúbrica: es una lista de deseos.
> Y el desacuerdo entre jueces es, casi siempre, un detector de ambigüedad en tu
> escala.

### L5.17 — Consistencia no es corrección

La primera pasada del juez repitió la misma nota en **6 de 6** al volver a
juzgar. 100% estable… equivocándose.

> Si usas "el mismo modelo dos veces" como control de calidad, un acuerdo alto te
> dará **más** confianza en una nota que está mal. Correr el mismo juez dos veces
> mide **estabilidad**; para medir **sesgo** hace falta un juez distinto, y para
> medir **verdad** hacen falta etiquetas humanas.

### L5.18 — Pide al juez la evidencia, y compruébala con código

La rúbrica pedía `{"nota": …, "razon": …, "palabras": […]}`. Esa tercera clave
fue lo que permitió auditarlo, y destapó lo más grave de todo:

```
texto : "...que no se te empapen. Lleva paraguas por si el aguacero arrecia..."
juez  : ['ponte', 'te', 'lleva', 'lleve']   <- 'lleve' NO está en el texto
razón : "Mezcla tuteo al inicio con ustedeo al final"
```

**El juez fabricó la evidencia**: citó las dos formas a la vez para sostener una
mezcla que no existía. Tres veces. En total, 9 de 451 citas (2%) no estaban en el
texto, y eran justo las que sostenían los veredictos.

> Un juez que solo devuelve una nota es **incomprobable**. Pídele siempre las
> palabras exactas en que se apoya, y verifícalas contra el texto **con código,
> no leyendo**. Son cuatro líneas, y convierten una opinión en una afirmación
> auditable.

### L5.19 — Un juez es buen filtro y mal decisor

Balance del juez sobre 120 respuestas:

| | |
|---|---|
| mezclas conocidas que cazó | 3 de 3 |
| mezclas **nuevas y reales** | **4** |
| falsas alarmas | 36 |

De cada 6 alarmas, 1 era real. Como decisor automático es inservible. Pero:

```
120 respuestas → el juez marca 43 → lees 43 → encuentras 4 defectos
                                              invisibles para el `if`
```

Y esos 4 valían la pena: la construcción `"No olvide el paraguas"` combinada con
`"ponte"` **no estaba en ninguna lista y nunca se me habría ocurrido buscarla**.

> Un juez puede permitirse falsas alarmas porque el que decide al final eres tú.
> Úsalo para **reducir lo que tienes que leer**, no para sustituir que lo leas.

### L5.20 — Guardar los resultados te deja reanalizar sin volver a pagar

Los tres experimentos guardaron cada respuesta completa en `resultados/*.json`.
Gracias a eso, el juez calificó 120 respuestas **sin generarlas otra vez**: los
$0.49 de generar ese texto ya estaban pagados, y juzgarlo costó centavos.

Todo el análisis del verbo `ponete`, la comprobación de las citas inventadas y la
suma de las 60 corridas del mismo prompt salieron de releer disco, no de la API.

> Una medición que no guardaste es una medición que vas a volver a pagar. Y casi
> siempre, la pregunta más interesante se te ocurre **después** de haber corrido
> el experimento.

---

> Las cuatro lecciones siguientes salieron del **ejercicio 1** (comparar Haiku
> contra Sonnet como juez). Están numeradas después porque se aprendieron
> después — y las cuatro corrigen algo que estaba escrito antes.

### L5.21 — El valor de un juez es el trabajo humano que te quita

Los dos jueces sobre las mismas 120 respuestas:

| | Haiku 4.5 | Sonnet 5 |
|---|---|---|
| acuerdo con el detector | 66.4% | 95.8% |
| marcó como mezcla | 43 | 8 |
| **mezclas reales cazadas** | **4 de 4** | **4 de 4** |
| precisión | 9% | 50% |

La tercera fila es la que rompe la intuición: **el juez caro no encontró nada
que el barato se perdiera.** Los dos cazaron las mismas 4. Lo que cambió fue
cuánto había que leer para llegar a ellas — 43 respuestas contra 8.

Por $0.18 más, 35 respuestas menos que revisar.

"Acuerdo 66% vs 96%" suena a que uno acierta más. No es eso: **aciertan igual y
uno te hace perder seis veces más tiempo.**

> El número que decide si un juez sirve no es su exactitud, es **cuánto reduce
> lo que un humano tiene que leer**. Un juez con 9% de precisión no es un
> filtro: es una lista de tareas disfrazada de medición.

### L5.22 — Un modelo mejor vuelve el defecto raro, no lo elimina

Sonnet **también fabricó una cita**: marcó una respuesta apoyándose en `lleve`,
palabra que no está en el texto (dice `lleva`). La misma alucinación de Haiku,
en el mismo par de palabras. Pasó del 2.0% al 0.3% de las citas.

Y en otra alarma se contradijo dentro de su propia explicación: *"Mezcla tuteo
(ponte) con ustedeo (**lleva es tuteo**, pero revis..."*.

Lo peligroso no es el número: es lo que el número te invita a hacer. Con 2% de
citas falsas revisas siempre. Con 0.3% dejas de revisar — y justo entonces la
que se cuela pasa sin que nadie la mire.

> Un defecto raro es más peligroso que uno frecuente, porque desactiva la
> costumbre de comprobar. **Pagar por un modelo mejor no te compra el derecho a
> quitar la comprobación** — la comprobación automática de citas (L5.18) es la
> que cazó esta, y cuesta cuatro líneas.

### L5.23 — Si el modelo es una variable, el precio también tiene que serlo

`05_juez.py` tenía esto:

```python
MODELO_JUEZ = "claude-sonnet-5"
PRECIO_ENTRADA = 1.00 / 1_000_000     # Haiku
PRECIO_SALIDA = 5.00 / 1_000_000
```

Al cambiar el modelo, **los precios se quedaron en los de Haiku**. El script
imprimió `COSTO REAL: $0.1530`. El costo real era **$0.3060**: el doble.

No hubo excepción, ni aviso, ni nada raro en la salida. El error se imprimió
con dos decimales y la etiqueta "COSTO REAL", que es lo más parecido a una
promesa que puede hacer un programa.

Es el mismo bug de forma que el contador `len(historial) // 2` del nivel 2:
**un dato derivado de otro, guardado como si fuera independiente.** El día que
el original cambia, el derivado miente.

Arreglo: un diccionario `PRECIOS[MODELO]`, que además **revienta** si el modelo
no está — fallar es mejor que inventar. Y el precio aplicado se imprime al lado
del total y se guarda en el JSON con los tokens, porque **un costo suelto no se
puede auditar**: sin los tokens, un JSON viejo con el precio malo miente para
siempre y no hay forma de recalcularlo.

> Los datos que dependen unos de otros se guardan juntos. Si tienes que acordarte
> de cambiar dos cosas a la vez, algún día vas a cambiar una sola — y el
> programa no te lo va a decir.

### L5.24 — Cuatro bugs distintos, una sola familia: tocar el dato antes de verlo

Al contar cuántas mezclas reales había, el chequeo decía:

```python
if 'olvide' in texto:      # MAL
```

`'olvide' in "no olvides"` es `True`. Y `"No olvides"` es tuteo **correcto**, o
sea lo contrario de un defecto. Resultado: **46 mezclas**. Con `\bolvide\b`:
**4**. Las otras 42 eran el bug — el **91% del hallazgo**.

Cuarta vez en el curso que aparece la misma forma:

| dónde | qué hizo | qué escondió |
|---|---|---|
| `texto.strip()[:30]` (nivel 1) | cortó | la fila de Sonnet, y pareció culpa del modelo |
| `e.message[:80]` (nivel 4) | cortó | el mensaje útil **y** el `request_id` |
| `normalizar()` (§5.1) | quitó tildes | `llevá` vs `lleva`: la señal entera |
| `'olvide' in t` (§5.6) | buscó subcadena | `olvides` ≠ `olvide`: infló 4 a 46 |

Ninguno lanzó un error. Los cuatro son operaciones que parecen inocentes:
cortar, normalizar, buscar. Y las cuatro **modifican el dato entre que llega y
que tú lo miras**, así que lo que revisas ya no es lo que pasó.

> Antes de creerte un resultado, pregúntate qué le hizo tu código al dato en el
> camino. **Un preprocesamiento silencioso es indistinguible de un hallazgo.**
> Los cuatro se cazaron igual: mirando los casos concretos uno por uno, no el
> número agregado.

---

## Nivel 5b — Proyecto integrador: el agente de divisas

> Nueve sesiones (9 a 17), cuatro archivos escritos desde cero, **121 evals
> gratis** y una evaluación con rúbrica que encontró un defecto que ningún `if`
> podía ver. Es el único nivel sin código de partida.

### L5b.1 — Un proyecto integrador no es juntar piezas viejas

La promesa era *"no vas a aprender nada nuevo, todo está en algún nivel"*. Salió
falsa, y el hueco enseñó más que las diez filas llenas.

Al juntar seis herramientas aparecieron **tres frenos que ningún nivel tenía**:
¿existe la herramienta?, ¿acepta esos argumentos?, y la red final. En el nivel 4
el agente tenía **una** herramienta: que el modelo inventara un nombre era casi
imposible.

> **Al juntar piezas aparecen problemas que ninguna tenía por separado.** Y son
> los únicos que no puedes copiar de ningún lado.

### L5b.2 — Casi toda una buena descripción dice CUÁNDO NO usar la herramienta

Decir qué hace es lo fácil. Lo que evita el error es marcar las fronteras: con
cuál no confundirla, y en qué caso está prohibida.

Las tres que se escribieron a propósito: `trm` vs `trm_en_fecha` (nombrándose
mutuamente), `trm` vs `tasa` (con los dos números reales metidos en el texto
para que no parezcan intercambiables), `historial` vs `trm_en_fecha`.

> Un error de elección cuesta una vuelta entera — más de 3.000 tokens. Una
> frontera bien escrita cuesta veinte palabras.

### L5b.3 — La lista `tools` no es documentación: es comportamiento

`historial` devolvía 30 registros que abarcaban 48 días de calendario, y el
agente decía *"los últimos 30 días"*. Se arregló **escribiendo una advertencia
en la descripción**, sin tocar una línea de código. En la corrida siguiente el
modelo usó `desde` y `hasta` y dijo *"20 registros de vigencia"*.

> El texto que le das al modelo se ejecuta igual que el código. La diferencia es
> que se paga en cada vuelta.

### L5b.4 — El menú también se paga, aunque nadie lo llame

Seis herramientas pesan 3.447 tokens **en cada vuelta de cada conversación**.
Las tres que nunca se usaron eran el 40% del menú y el 32% del costo total.

⚠️ Pero llamarlo desperdicio es la lectura fácil y equivocada. El día que
pregunten por una fecha pasada, `trm_en_fecha` es el único camino que existe.

> El número real no es *"cuánto desperdicié"*: es **cuánto cuesta la opción de
> poder responder**. $0,048 por conversación en opus, $0,008 en haiku.

### L5b.5 — Un agente no paga por lo que dice: paga por lo que RELEE

```
7 vueltas · entrada 23.710 tokens · salida 887 tokens
```

**27 a 1.** Todo lo que entra a la conversación —el system, el menú, cada
`tool_result`— se reenvía completo en cada vuelta siguiente.

Por eso una regla corta que le evita pensar puede salir casi gratis: engorda la
entrada un poco y adelgaza la salida, que vale cinco veces más por token.

### L5b.6 — El único contador de tokens que vale es el de la API, y es gratis

Dos estimaciones seguidas, las dos cortas y en el mismo sentido: *"~700-900"* a
ojo, *"~1.557"* dividiendo caracteres entre 4. El valor real: **3.049**.

La regla de los 4 caracteres viene del inglés en prosa. **JSON en español
tokeniza mucho peor.** Y `count_tokens` acepta `tools=`, cuesta $0.00, y estaba
documentado en la guía desde el nivel 5.

> Tener la herramienta documentada no es lo mismo que acordarse de usarla.

### L5b.7 — Un token no es una unidad universal: es la unidad DE ESE MODELO

El mismo texto, byte a byte idéntico, medido en la primera llamada de cada
pregunta:

```
opus-5     3.634      sonnet-5   3.702      haiku-4-5  3.543
```

**159 tokens de diferencia por el mismo texto.** No es que uno lea más: cada
familia parte el texto distinto.

> Contar tokens con un modelo y presupuestar con otro es medir en pulgadas y
> pagar en centímetros.

### L5b.8 — Medir las partes por separado y sumarlas no da el todo

Medir cada herramienta sola y sumar las seis dio **4.877**. El menú completo
pesa **3.447**. La suma daba más que el todo — porque hay un **costo fijo por
tener herramientas**, y se estaba cobrando seis veces.

> La medición honesta no es sumar: es **QUITAR**. Mides la configuración real,
> mides la alternativa, y restas.

⭐ Y lo atrapó la aritmética que no cerró, no el razonamiento.

### L5b.9 — Un dato de afuera dentro de una consulta es una inyección

`trm_en_fecha` armaba una URL con texto que venía del modelo. Demostrado en
vivo: una entrada preparada convirtió una consulta de 1 fila en una de 1.000
(≈31.000 tokens).

La defensa es la **lista de permitidos**, nunca la de prohibidos. Y `quote()`
transporta, no decide: **escapar no es validar**.

### L5b.10 — Después de validar, usa lo validado, no lo que llegó

`2026-7-5` se normaliza a `2026-07-05`, y a partir de ahí **se usa el
normalizado**. Validar una cosa y seguir trabajando con otra es no haber
validado.

### L5b.11 — Un plan escrito antes de mirar los datos se corrige con los datos

El README prometía `historial(de, a, dias)` para cualquier par de monedas. Con
las fuentes reales es imposible: una tiene 166 monedas y solo el día de hoy; la
otra tiene 30 años de historia y solo USD→COP.

No estaba mal razonado: era **anterior a la información**. Un plan así se
corrige con los datos, no se defiende.

### L5b.12 — El caso raro no es adorno: suele ser el único con ojos

Siete sabotajes deliberados en una sesión. En dos ocasiones independientes, los
casos felices pasaron tranquilos y **solo el caso raro** —el domingo, las filas
al revés— vio el defecto.

> Un examen que todos aprueban no mide a nadie. Mide que tus preguntas son
> fáciles.

### L5b.13 — Escribir la prueba mejora el diseño, no solo lo verifica

`trm_en_fecha` devolvía cero filas en tres situaciones distintas (fecha futura,
muy antigua, hueco en la fuente) y no había forma de compararlas en un eval sin
comparar el texto del mensaje.

De ahí nació el `motivo` como **dato estable**. Y esa decisión terminó pagando
**cinco veces** en archivos que aún no existían: los permisos, el catálogo de
modelos, la política del examinador, y las dos fallas del juez.

> Lo que tiene que ser consistente no se deja en la memoria: se vuelve un dato.
> **Un `sí/no` que tapa tres situaciones distintas siempre acaba mintiendo.**

### L5b.14 — Más herramientas no es solo más capacidad: es más formas de equivocarse

Los frenos 7, 8 y 9 protegen **del modelo**; los seis del nivel 4 protegen **del
mundo y de tu cuenta de cobro**. Son dos familias distintas y llegaron por
razones distintas.

Y hay un décimo que apareció solo: validar que el **nombre del modelo** exista
en el catálogo, porque ahí el que escribe mal eres tú.

### L5b.15 — Un límite heredado sin recalcular no es un freno: es una trampa

`PRESUPUESTO_USD = 0.10` funcionaba en el nivel 4. La primera corrida de este
agente costó **$0,1407**. Copiado tal cual habría cortado a mitad de la tercera
pregunta, y habrías buscado durante horas un defecto en el bucle que no existe.

### L5b.16 — Un registro que no distingue POR QUÉ pasó algo puede afirmar lo falso

En la primera corrida del registro quedó escrito
`{"evento":"permiso","herramienta":"convertir","concedido":true}` — y a nadie le
preguntaron por `convertir`: es libre.

**Rompe justo aquello para lo que el registro existe.** El día que un agente
escriba un archivo que no debía, vas a leer *"permiso concedido"* y vas a creer
que lo autorizaste.

### L5b.17 — El modelo hace aritmética a escondidas cuando le falta un puente

Ocurrió **dos veces, en dos herramientas distintas**:

| | qué le faltaba | qué inventó | ¿acertó? |
|---|---|---|---|
| `trm` (sesión 14) | la tasa invertida | `1/3206.18` | sí, por 10 decimales |
| `tasa` (sesión 17) | la tasa invertida | 3.209,64 en vez de 3.207,64 | **NO** |

La primera vez acertó, y **eso fue lo peligroso, no el consuelo**. La segunda se
desvió dos pesos y el número resultante era perfectamente creíble.

> Cuando el modelo hace algo indebido, pregúntate primero si le falta un puente.
> Casi nunca calcula por vicio: calcula porque nadie le dio el número.

### L5b.18 — Prohibir sin ofrecer salida no es una regla, es un callejón

La primera solución fue prohibirle invertir la tasa en la descripción. Al
escribirla se vio que dejaba la pregunta *"¿cuántos dólares son 500 mil pesos?"*
**sin ningún camino posible**: `convertir()` solo multiplica.

El arreglo bueno fue construir el puente (`usd_por_1_cop`, `cop_por_1_usd`). Y
el precio, medido las dos veces, fue **prácticamente cero**: la entrada engorda,
la salida adelgaza, y la salida vale cinco veces más.

### L5b.19 — Lo que puede vivir en el harness, que viva en el harness

La tabla de permisos vive en Python y **el modelo nunca la ve: no cuesta un solo
token.** Explicárselo en las descripciones se pagaría en cada vuelta de cada
conversación.

> Es gratis en el harness e impuesto permanente en el prompt.

### L5b.20 — Primero si hace el trabajo; entre los que sí, el más barato

Son **dos pasos**, y la regla falla si te quedas en el primero: el caro
*siempre* hace el trabajo, así que *"usa el que sirve"* siempre escoge el caro y
nunca te obliga a medir.

⚠️ Y "hace el trabajo" no es una propiedad del modelo: es de la pareja
**modelo + tarea**. Haiku fue suficiente para estas preguntas con estas seis
herramientas. Cambia una y hay que volver a medir.

**Empieza siempre por el capaz.** Si arrancas con el barato y algo falla, no
sabes si fue tu harness o el modelo: dos incógnitas a la vez.

### L5b.21 — Lo que el modelo ELIGE es estable; lo que DICE, no

Dos corridas de haiku sobre las mismas tres preguntas:

| | resultado |
|---|---|
| herramientas y argumentos | **idénticos, dígito por dígito** |
| costo | −0,57% |
| **las tres respuestas** | **las tres, distintas** |

Y eso decide cuántas repeticiones necesitas: los criterios de elección y de
número casi no varían; los de redacción, sí.

### L5b.22 — Un examen que no puede reprobar a nadie es una ceremonia

Tres modelos, tres preguntas, tres aprobados. Eso **no** midió que haiku fuera
igual de bueno: midió que las preguntas eran fáciles.

Un examen se cubre por dimensiones, no por cantidad: cada herramienta al menos
una vez, cada frontera al menos una vez, **al menos un caso que deba negarse**,
al menos un caso de datos raros, y controles fáciles para saber que un cero es
del modelo y no de tu harness.

### L5b.23 — Cuando una buena respuesta reprueba, el sospechoso es el examen

Pasó dos veces con la misma rúbrica, en la misma tanda. La rúbrica se escribe
**antes** de ver las respuestas —eso es lo correcto—, pero eso la convierte en
una **hipótesis**, no en una verdad.

⚠️ Y hay que distinguirlo de amañarla: se quitó un criterio porque **no había
nada que exigir**, no para que el agente pasara. Los criterios que sí podían
reprobar siguieron puestos.

### L5b.24 — Cuando un juez se contradice, sospecha de que dos criterios midan lo mismo

Casi la misma frase, veredictos opuestos en la misma tanda: "relleno" en un
caso, "aclaración pertinente" en otro.

La causa no era ruido del modelo: **el criterio de estilo castigaba justo lo que
los criterios de fuente y frontera premian.** Una respuesta bien hecha sumaba
por un lado y restaba por el otro, y el juez tenía que elegir.

> Criterios que se solapan miden lo mismo dos veces, y obligan al juez a
> inventar una frontera que tú no le diste.

### L5b.25 — `max_tokens` es el techo de TODO lo que produce, incluido lo que piensa

El juez razona antes de contestar, y ese razonamiento gasta los mismos tokens
que la respuesta.

```
caso 4   stop_reason=end_turn     salida=1484   bloques: thinking + text
caso 5   stop_reason=max_tokens   salida=1500   bloques: SOLO thinking
```

Pensó tanto que se quedó sin cupo para hablar: 1.500 tokens de razonamiento y
**cero caracteres de respuesta**.

### L5b.26 — Un instrumento que falla en los casos difíciles es peor que uno que no funciona

Los dos casos que el juez no pudo calificar fueron **el domingo y el número
inventado**: los dos más difíciles del examen.

No fue mala suerte, fue causa: **entre más difícil el caso, más largo el
razonamiento, más probable quedarse sin cupo.**

> Las fallas parecen ruido al azar y están **sesgadas hacia los casos que sí
> podían reprobar**. Sin mirarlas, la conclusión habría sido "100%" — un 100%
> que se debía a que las dos preguntas peligrosas no se calificaron.

### L5b.27 — Un fallo del instrumento nunca puede parecerse a una mala nota

Si el juez devuelve algo ilegible y eso se cuenta como cero, **el defecto de tu
medidor se ve exactamente igual que un defecto del examinado** en la tabla
final. Y las dos cosas exigen arreglos opuestos.

Por eso las fallas del juez se marcan aparte, con su causa (`sin_cupo` no es lo
mismo que `json_ilegible`), y se excluyen del porcentaje diciéndolo en voz alta.

### L5b.28 — Lo que recibes desde afuera se puede probar; lo clavado adentro, no

El bucle tenía dentro **cómo** se pide un permiso: imprimir y esperar un
`input()`. Con una persona sentada funciona; para correr diez preguntas
seguidas y medir, no.

Cambiarlo por un parámetro con el mismo valor por defecto no cambió nada para
quien lo corre a mano — y volvió los permisos **probables gratis, sin red y sin
modelo**, que llevaban dos sesiones sin un solo caso.

### L5b.29 — Un eval determinista prueba tu código, no lo que el modelo hace en su cabeza

121 casos, 0 fallos, $0.00 — y **ninguno podía ver** que el agente dijera
3.209,64. La cuenta no pasó por ninguna función nuestra: ocurrió dentro del
modelo y salió directo al texto del usuario.

> Esa es la frontera exacta entre las dos mitades del nivel 5. Un `if` prueba tu
> código. Para lo que el modelo hace por su cuenta hace falta una rúbrica.

### L5b.30 — Un permiso protege lo irreversible, no el bolsillo

Cuando se le negó `guardar_reporte`, el modelo ya había escrito el reporte
entero: **484 tokens de salida contra ~75 de una vuelta normal**. Negarlo salvó
el disco; el gasto ya estaba hecho.

> Cuando le niegas algo a un agente, ya pagaste por que lo pensara.

---

## Nivel 6b — Memoria persistente y Skills

> ⚠️ **Este bloque está a medias, y se dice para que no se olvide.**
> Las lecciones de la **memoria** (pasos 1 a 5, sesiones 16 a 21) siguen
> pendientes de escribir: están sueltas dentro de `PROGRESO.md`. Se numerarán
> **L6b.1 a L6b.29**.
> Las de **Skills** (paso 6, sesión 22) empiezan en **L6b.30**, para no tener
> que renumerar nada después.

### L6b.30 — Una herramienta extiende lo que el agente HACE; una skill, lo que SABE

Y lo que las confunde es que la skill llega **montada en** una herramienta
(`leer_skill`). No es la misma cosa: esa herramienta no consulta el mundo, no
cambia nada, no puede fallar por red y no necesita permiso. Solo trae texto.

> **La herramienta es el camión. La skill es lo que va en el camión.**

La prueba de que son cosas distintas: una skill puede llegar **sin ninguna
herramienta** — un `CLAUDE.md` que se carga entero al arrancar también es
conocimiento en un `.md`. Lo que aporta la herramienta no es la skill: es el
**bajo demanda**.

### L6b.31 — Una skill no solo agrega datos: cambia de qué es RESPONSABLE el agente

Sin la skill, ante *"¿necesito autorización para cambiar 50 millones?"* el
agente contestó: *"soy un asistente de tasas de cambio, **no de regulaciones
bancarias**; consulte con su banco"*.

Con `normas-cambiarias` cargada, la misma pregunta **entra en su trabajo** y la
resuelve completa.

> Al escribir una skill no estás rellenando un hueco de información. Estás
> **ampliando el alcance** de lo que el agente acepta atender.

### L6b.32 — Una skill que el modelo puede adivinar es una skill que no se puede medir

Es el error del *"¿qué es una variable?"* de la sesión 3, con otra ropa: si el
modelo contesta igual de bien sin el archivo, la prueba no demuestra nada
aunque el texto afirme que sí.

Por eso las cuatro skills se llenaron de **datos arbitrarios**: umbrales de
5.000 y 20.000, margen de 0,4 %, un nombre de archivo `cierre-AAAA-MM`. Nadie
los puede deducir.

> **Antes de medir una skill, comprueba que el modelo no la sepa ya.** Y
> compruébalo corriendo, no razonando.

### L6b.33 — Una medición "antes" deja de ser el antes en el instante en que cambias lo que mide, y no avisa

`linea_base.py` se escribió sin skills y llamaba al agente a secas. Al conectar
el menú al system prompt **por defecto**, ese mismo archivo, con el mismo
nombre, habría seguido corriendo y midiendo otra cosa. Nada habría fallado.

El arreglo fue un modo explícito (`--con`) que se imprime en pantalla y queda
escrito en el registro.

> **Guarda la CONFIGURACIÓN junto al número.** Un número sin su configuración
> miente por su cuenta, sin que nadie mienta.

### L6b.34 — La misma señal puede significar lo contrario según el modo

El script buscaba pedacitos de texto que solo existen dentro de los `.md`. Sin
skills, encontrarlos significa **"se lo inventó"**. Con skills, encontrarlos
significa **"funcionó"**.

El detector no cambió ni una línea — y aun así el rótulo llegó a gritar
`🚨 SEÑALES ENCONTRADAS SIN SKILL` sobre un acierto.

> **Lo que cambia al cambiar la configuración no es la medición: es lo que la
> medición SIGNIFICA.** Los rótulos también son parte del instrumento.

### L6b.35 — El impuesto de un menú se puede predecir gratis, y sale exacto

`count_tokens` dijo que el menú de 4 fichas más la herramienta costaría
**+849 tokens por vuelta**. La corrida real: 4.913 → 5.762. **+849.**

> Primera vez en el curso que un costo se **predice** en vez de descubrirse en
> la factura. Y costó $0,00.

### L6b.36 — Skills solo es más barato si el modelo es selectivo, y eso depende de un texto que escribes tú

| Estrategia | tokens por vuelta |
|---|---|
| pegar todo el conocimiento siempre | 8.800 |
| skills, cargando una | ~6.700 |
| skills, cargando las cuatro | **9.649** |

Cargar casi todas sale **más caro que no haber hecho nada**: pagaste el menú de
más.

> ⭐ **El punto de equilibrio no lo decide el código: lo deciden las
> descripciones.** Es la primera vez que la calidad de un texto tuyo tiene un
> precio calculable.

### L6b.37 — Entre dos skills que se pisan, la frontera se escribe en las DOS direcciones

`reporte-mensual` dice *"no cubre el cierre de año"*; `cierre-de-ano` dice *"el
formato está en reporte-mensual"*. Ante *"ármame el reporte de diciembre"* el
modelo cargó **las dos en la misma vuelta**.

Es exactamente lo que se hizo con los criterios C4, C5 y C7 al escribir C9: dos
cosas que se solapan no se separan eligiendo una, sino **escribiendo dónde está
la línea, en cada una de las dos**.

### L6b.38 — El texto que escribe el modelo nunca se convierte en una ruta

La versión obvia de `leer_skill` pega el nombre a la carpeta. Con eso,
`leer_skill("../../.env")` **devuelve la API key**.

El nombre solo sirve para BUSCAR en la lista que ya se leyó. Lo que no está en
la lista, no existe.

> **Todo argumento escrito por el modelo que termina tocando el disco se valida
> contra una lista blanca, no contra una ruta.**

### L6b.39 — Un archivo de texto puede hacer que el agente llame a una función

`normas-cambiarias.md` decía *"convierte a dólares con la TRM ANTES de decidir
el tramo"*, y el agente fue a buscar `trm()` y `convertir()`. Cuatro vueltas,
encadenadas por una frase que **no es código**.

> El conocimiento no solo responde preguntas: **dirige el uso de las
> herramientas.**

### L6b.40 — Una skill puede crear una necesidad de cálculo que el harness no cubre

El margen del 0,4 % lo trajo el `.md`. No existía antes. Y el modelo **hizo esa
división de cabeza y falló por 14,15 USD** (~44.000 pesos), teniendo `convertir`
disponible en la misma vuelta.

> ⭐ **Al agregar conocimiento, pregúntate qué cuentas nuevas implica y si hay
> herramienta para ellas.** Una regla que exige aritmética mental es una regla
> que se va a incumplir en silencio.

### L6b.41 — Un defecto de comportamiento arreglado sin tocar una línea de código

El margen se corrigió editando `normas-cambiarias.md`: se pasó de *"margen
sobre la tasa"* (que obliga a dividir) a *"factor sobre el resultado"* (que
`convertir` sí puede hacer). Cero Python.

En la corrida siguiente aparecieron **dos llamadas a `convertir`** y la cifra
exacta, 15.898,25.

> Esa es la ganancia de fondo del paso 6, y no es el ahorro de tokens: **el
> conocimiento salió del `.py` y ahora lo puede editar quien sepa del negocio.**

### L6b.42 — Un examen que mezcla dos preguntas no mide ninguna de las dos

*"¿Puedo hacerlo de una o necesito autorización?"* pregunta por el permiso,
**no** pide una cotización. Cuando el agente dejó de aplicar el margen, había
dos explicaciones que encajaban igual de bien: se abstuvo, o juzgó bien que ahí
no tocaba cotizar. **Con esa pregunta era imposible distinguirlas.**

La pregunta 5 —*"cotízame… con el margen aplicado"*— solo tiene dos salidas
posibles, y por eso sí sirvió.

> **Una prueba que admite dos explicaciones no es una prueba: es una anécdota.**

### L6b.43 — Dos veces en la misma sesión, la prueba estaba mal y el agente tenía razón

- *"Ármame el reporte de diciembre"*, un 31 de julio → **"esa fecha está en el
  futuro"**. Cierto: la pregunta era imposible.
- La pregunta 3 mezclaba dos cosas (L6b.42).

Las dos las encontró **la corrida**, no la revisión.

> Es la sesión 17 otra vez: **cuando una respuesta razonable reprueba, el
> sospechoso es el examen.** Y el que escribe el examen es el mismo que revisa —
> por eso hay que correrlo.

### L6b.44 — Lo que decide CÓMO va a correr el programa se lee antes de que el programa empiece

`--con` se leía a mitad del archivo, y `anotar("inicio")`, treinta líneas más
arriba, ya lo necesitaba: `NameError` apenas arrancaba.

> Si un parámetro configura la corrida, **siempre habrá algo más arriba que ya
> lo quería.** Los argumentos se leen de primeras.

### L6b.45 — "¿Ya la cargué?" es una propiedad de la conversación, no de la skill

El freno de la doble carga vive en `ejecutar_agente`, no dentro de
`skills.leer_skill()`. La misma skill, en la conversación siguiente, hay que
volverla a cargar.

Si el freno viviera dentro de la función, la función tendría memoria entre
llamadas — y una función pura dejaría de serlo, con todo lo que eso cuesta para
probarla gratis.

> **Antes de poner un estado dentro de una función, pregunta a qué pertenece de
> verdad.**

### L6b.46 — Que el costo suba no es una regresión

Con skills, las tres preguntas que las necesitaban pasaron de $0,0344 a $0,0777
en total. Pero antes eran baratas **porque no hacían nada**: la del umbral
costaba una vuelta y decía *"pregunte en su banco"*; después costó cuatro y
entregó tramo, margen y cifra final.

> **Un agente que empieza a hacer el trabajo empieza a costar.** Escríbelo
> ANTES de medir, o mañana leerás "subió el costo" y sacarás la conclusión
> contraria.

