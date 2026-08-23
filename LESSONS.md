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

> **L6b.1 a L6b.29** son las de la **memoria persistente** (pasos 1 a 5,
> sesiones 18 a 21). **L6b.30 en adelante**, las de **Skills** (paso 6,
> sesión 22).
>
> Las candidatas apuntadas en `PROGRESO.md` eran más de 29: las que decían la
> misma idea con otra ropa quedaron **fundidas en una sola lección**, para que
> la numeración de Skills no se moviera.

### L6b.1 — La API no tiene memoria. Nunca. Ni siquiera dentro de una conversación

El `historial` del nivel 2 no le daba memoria al modelo: era **tu código
repitiéndole todo** en cada llamada. Cada petición llega igual de ciega que la
primera.

> **La memoria nunca estuvo en el modelo: siempre estuvo en tu código.**

### L6b.2 — Toda memoria vive en el harness, y por eso pagar más no la arregla

Ni el modelo ni la API guardan nada. **Opus olvida exactamente igual que haiku.**
La amnesia no es una limitación del modelo que se compre: es el sitio donde no
pusiste un archivo.

### L6b.3 — Memoria no es historial: es lo que quedó DESPUÉS de olvidar casi todo

Guardar la conversación entera falla por tres lados: por costo (se reenvía en
cada vuelta), por techo (la ventana se acaba) y —sobre todo— **por falta de
criterio**. Un sistema que guarda todo no decidió nada.

> Y el curso mismo es la prueba: `PROGRESO.md` se actualiza, `LESSONS.md` solo
> crece, `GUIDE.md` se corrige. **Tres archivos porque son tres memorias con
> tres políticas.**

### L6b.4 — Un sistema de memoria sin política de olvido no está terminado

El tope de 8 datos parecía un detalle de implementación. Cuando por fin se vio
actuar, **botó `es contador`** —el hecho más definitorio del usuario— para que
entrara *"estudia economía"*, y dejó vivo *"viaja seguido a Panamá"*.

> **Botar el más viejo trata la antigüedad como si fuera irrelevancia, y no lo
> es.** Eso no es una obviedad: es una decisión de diseño, y tiene víctima.

### L6b.5 — El formato del archivo sale de la política, no del gusto

| qué guarda | política | formato |
|---|---|---|
| `registro.jsonl` | **eventos**: pasaron y no cambian | solo crece → se **añade** |
| `memoria.json` | **estado**: es verdad hoy | se **reescribe** entero |

> Antes de elegir entre `.json` y `.jsonl`, pregunta si lo que guardas **ocurrió**
> o **es cierto ahora**. El resto se deduce solo.

### L6b.6 — Permiso = ANTES, para lo irreversible. Revisión = DESPUÉS, para lo reversible

`recordar` quedó como `"libre"`, con huella en el registro y un comando para ver
y borrar. Tres razones, y la segunda es la que decidió:

1. La primera vez interrumpe, y cae a mitad de una respuesta que nadie pidió.
2. ⭐ **El permiso no tiene memoria:** `AUTORIZADAS` vive en RAM y muere al
   cerrar. **Un permiso volátil sobre una herramienta persistente es un desajuste
   de diseño** — habría que autorizar lo mismo todos los días, para siempre.
3. El permiso pregunta lo que no importa: el peligro de la memoria no es la
   **acción** (escribir 4 líneas, reversible) sino el **contenido** — un dato
   falso envenena todas las conversaciones futuras. Y un *"¿autorizas escribir?"*
   no muestra **qué** se va a escribir.

### L6b.7 — Escalar por usuarios y escalar por conocimiento son dos ejes independientes

No es una escalera `archivo → base de datos → RAG`.

| eje | lo mueve | exige |
|---|---|---|
| ↔ | cuántos **usuarios** escriben | archivo → SQLite → PostgreSQL |
| ↕ | cuánto **conocimiento** hay que consultar | leerlo entero → Skills → RAG |

Un investigador solo con 20.000 papers: **RAG sí, base de datos no.** 50.000
empleados sin documentos: **base de datos sí, RAG no.**

> **RAG no es el hermano de la memoria: es la memoria persistente cuando ya no
> cabe.** Y con miles de usuarios el archivo plano no es "menos elegante": **se
> rompe** — dos escrituras al tiempo lo corrompen sin error y sin aviso.

### L6b.8 — Un log no es una memoria

*"Deja registro de lo realizado"* suena a memoria y no lo es. El agente escribía
`registro.jsonl` desde la sesión 15 y **jamás lo volvió a abrir**.

> **El log es la materia prima; la memoria es la conclusión.** A ese agente no le
> faltaba escribir: le faltaba **leer**.

### L6b.9 — Un eval en verde dice una de dos cosas, y no sabes cuál

O el código está bien, **o la prueba no está mirando**. Lo único que las separa
es romper el código a propósito y ver el rojo. En los cinco sabotajes del nivel,
tres casos pasaron en verde defectos reales.

⚠️ **Y el caso extremo:** con el desvío del disco quitado, **48 casos salieron en
verde mientras el eval borraba el `memoria.json` de verdad.** No lo dañó: lo
desapareció. El único que se enteró fue la trampa que comparaba el archivo real
byte por byte.

> **Un eval con un efecto secundario destructivo no se ve rojo: se ve verde.**
> El desvío es la promesa; la trampa es el hecho comprobado. Hacen falta las dos.

### L6b.10 — Lo que informa éxito no siempre lo hizo, y pasa en las dos capas

| capa | qué se vio |
|---|---|
| **el código** | el tope botaba el dato equivocado y el motivo decía `desplazo` — la respuesta correcta para la acción equivocada |
| **el modelo** | *"**Anotado**: te daré las cifras en tablas"* · `🧠 no guardó nada`. Nunca llamó a `recordar` |

> **El motivo dice qué CREYÓ que hizo, no qué hizo.** Contar y leer el motivo no
> basta: hay que preguntar **quién** quedó.

🚨 **Y arriba está el peligro de fondo de la escuela B** (que el modelo decida
cuándo escribir): *"decir que lo hizo"* y *"hacerlo"* son dos cosas separadas, y
**nada las obliga a coincidir**. Contradice L4.9 de frente: allá algo le dijo que
no y no mintió; aquí nadie le dijo nada y narró como si hubiera llamado.
El arreglo no fue código, fue una regla en el system: *"nunca digas que guardaste
algo si no llamaste a `recordar` en este mismo turno"*.

### L6b.11 — Una conversación tiene que ver una memoria QUIETA

Tres sitios posibles para leer la memoria, y los tres "funcionan":

| dónde | cada cuánto | qué pasa |
|---|---|---|
| en `llamar_modelo` | cada vuelta | ⚠️ el system prompt cambia a mitad de conversación |
| al importar el módulo | por proceso | ⚠️ lo aprendido en la pregunta 1 no llega a la 2 |
| al empezar `ejecutar_agente` | **por conversación** | ✅ |

> Si el modelo guarda un dato en la vuelta 3, en la vuelta 4 **su propio pasado
> sería otro**. Lo que se aprende hoy se usa en la conversación **siguiente**, no
> en la vuelta siguiente.

Y la distinción que lo hace probable: `None` es *"léelo tú del disco"*; `""` es
*"corre SIN memoria"*. **Una orden y una ausencia no son lo mismo.**

### L6b.12 — Una herramienta no tiene que vivir en `herramientas.py`: tiene que estar en `FUNCIONES`

`recordar` se quedó en `memoria.py`. `herramientas.py` es *el mundo exterior*
(divisas, red, reportes); la memoria es *del harness*. Meterla ahí habría
obligado a que un módulo importara al otro sin necesidad.

> **Lo único que mira el bucle es `FUNCIONES`.** La carpeta donde vive una
> función es organización tuya; el menú es el contrato.

Y el envoltorio no sobra: `guardar_dato` devuelve una tupla, y el `tool_result`
necesita texto.
> ⭐ **Una tupla le dice al HARNESS qué pasó; no le dice al MODELO qué hacer.**
> `muy_largo` es un diagnóstico. *"Resúmelo en menos de 200 caracteres y vuelve a
> intentarlo"* es una instrucción.

### L6b.13 — Lo que cuesta la memoria no son los datos

Dos mediciones, las dos gratis con `count_tokens`:

| | tokens por vuelta |
|---|---|
| el primer dato | **+72** (48 son el encabezado, tenga uno u ocho) |
| cada dato siguiente | ~25 |
| la memoria **llena**, 8 datos | **247** |
| **enseñarle a usarla** (system + descripción) | **+443** |

> ⭐ **Enseñarle al agente a usar la memoria cuesta más que darle la memoria.**
> Las instrucciones pesan casi el doble que los datos que gobiernan.

Y el peaje fijo es **la tercera aparición del costo del menú** (sesión 16): hay
un precio por **abrir la puerta**, y después el pasajero es barato.
→ Consecuencia que no es obvia: **una memoria con un solo dato es el peor negocio
de todos.** Se paga el peaje completo por un pasajero.

📏 **Y se puede presupuestar sin gastar:** `count_tokens` predijo +72 y la corrida
pagada dio +74; predijo +143 y dio +142.

### L6b.14 — Una muestra no es una medida

El **mismo** acto 2, dos veces, con la misma pregunta, la misma memoria y el
mismo modelo: una corrida **afirmó** y la otra **preguntó**. Nadie cambió una
línea.

Y peor: la misma conversación falló **al revés** en dos corridas — en una guardó
bien y entregó una respuesta en blanco; en la otra respondió perfecto y mintió
diciendo *"Anotado"*.

> 📌 **Una diferencia entre dos configuraciones solo cuenta si es más grande que
> la diferencia entre dos corridas de la misma configuración.**

Consecuencia retroactiva: los criterios del 5b medidos con 3 muestras eran más
frágiles de lo que parecían.

### L6b.15 — La memoria no da razón, da foco

La misma pregunta, con y sin memoria. Las tres respuestas fueron buenas y
**ninguna inventó una cifra**. Lo que cambió fue el tamaño del abanico:

| | caminos que ofreció |
|---|---|
| sin memoria | **4** (pago oficial, remesa, compra internacional, otro) |
| con memoria | **2**, y apuntados: *"como contador que factura a EE.UU…"* |

> **La memoria no hizo al agente más correcto: lo hizo más específico.** Si al
> otro lado hay una persona, **ahorrarle dos preguntas ES el producto.**

✅ Y lo mejor es lo que no pasó: **sin memoria no se inventó un perfil.** Dijo
*"no puedo decirte cuál te conviene sin saber qué es lo tuyo"*.

### L6b.16 — Lo que no puedes provocar a voluntad, no lo pruebes pagando: simúlalo

El defecto de las respuestas vacías se vio tres veces solo. Al querer
reproducirlo a propósito, **el modelo no cooperó**: dos corridas pagadas y
ninguna sirvió.

Se fabricó un **cliente falso** con un guion de respuestas y se le metió al bucle.
Cuesta $0,00, corre en milisegundos, **y va a seguir probándolo dentro de seis
meses**. Es la misma sustitución que ya se le hacía al archivo, pero al cliente.

⚠️ Y trajo su propia trampa: el bucle llama a `anotar()`, que escribe en el
registro **de verdad**. Sin desviarlo, el eval habría metido líneas falsas en la
evidencia de las corridas pagadas.

### L6b.17 — Una respuesta incompleta es peor que una vacía

**3 de cada 10 respuestas llegaban en blanco:** el modelo escribía el texto junto
al bloque `tool_use` y el bucle solo miraba la última vuelta. Al sabotear el
arreglo apareció el caso peor: con texto en dos vueltas llega **algo** — una
respuesta que **parece completa y no lo es**.

> **La vacía se ve. La incompleta no.** Y: cortar por un límite tuyo
> (presupuesto, tope de vueltas) no es razón para botar lo que ya se pagó.

### L6b.18 — Una herramienta nueva no crea defectos: los DESTAPA

`recordar` es la primera herramienta que el modelo llama **mientras ya está
contestando**; las seis de divisas se piden primero y se contesta después. Por
eso destapó un defecto del bucle que llevaba **tres niveles** ahí y estaba
anotado como *"solo se nota cuando una herramienta se niega a mitad"*.

> Resultó ser el **30%** de las respuestas.

### L6b.19 — Cuando una buena respuesta reprueba, el sospechoso es el examen

La vara falló **tres veces en un día**: contó como *empaquetado* lo que eran
omisiones, y reprobó dos veces al agente por **no guardar un dato que ya estaba
en memoria** — donde guardar cero era lo correcto.

> ⭐ **Una vara escrita para un contexto no vale en otro.** `esperadas=1` suponía
> memoria vacía, y nadie volvió a mirar ese supuesto.

Y las tres se atraparon **mirando fila por fila**, no razonando. Como el número
único que mezclaba dos fenómenos: *empaquetar* es "guardó mal", *omitir* es "no
guardó", y se arreglan distinto.

### L6b.20 — Dónde va la regla importa más que cómo está escrita

El agente guardaba **4 de 9** hechos. Se arregló a **9 de 9** sin cambiar el
código, y el arreglo fue de ubicación y de proporción:

**Ubicación.** ⭐ **Una descripción de herramienta solo pesa cuando el modelo YA
está considerando usarla.** Si decide no llamarla, no lo frena nada — y
*"Anotado"* fue justo lo que dijo cuando **no** la llamó. → Lo que debe frenarlo
*antes* de decidir, o gobernar lo que puede **afirmar**, va en el **system
prompt**.

**Proporción.** La descripción vieja tenía **cuatro prohibiciones y una sola
instrucción positiva**. Con esa proporción, ante la duda el modelo se **abstiene**.
⚠️ Y no era que no supiera qué guardar: *"su ciudad"* ya estaba en la lista y
omitió *"vivo en Medellín"*. **Le faltaba el disparador, no el criterio.**

> Y el empaquetado no lo arregló la regla abstracta (*"un hecho por llamada"*, que
> ya estaba): lo movió **el ejemplo textual del error concreto.**

### L6b.21 — Una regla más estrecha que el problema no protege

El system decía *"nunca inventes un **número**"*. Se le escaparon: una tendencia
(*"el euro ha estado fuerte esta semana"*, sin un solo dato del euro), una fecha
(*"sábado 2 de agosto"* siendo 31 de julio) y un día de la semana.

> 🚨 **Una tendencia es un dato igual que un precio.** La regla se reescribió
> nombrando las cuatro cosas, y la invención paró.

### L6b.22 — Lo que el modelo no puede saber no se arregla prohibiendo: se pone, y se pone contado

Un modelo **no tiene reloj**. Prohibirle inventar la fecha sin darle la fecha solo
lo obliga a decir *"no sé"*.

Y no fue una herramienta `hoy()`, que era lo obvio:

| | costo |
|---|---|
| herramienta | ~200 tokens de menú en **cada** vuelta **+ una vuelta entera** |
| una línea en el system | **~40 tokens, cero vueltas** |

> **Si el dato siempre se necesita y no cambia dentro de la conversación, no
> merece una herramienta: merece estar puesto.**

⚠️ Y la primera versión decía *"cualquier otra fecha, cuéntala desde esta"* — y
contó mal. **Contar días de calendario es aritmética**, justo lo que este modelo
hace de cabeza y falla. La solución nunca fue *"que calcule mejor"*: fue
**dárselo hecho** (ayer, mañana, el próximo lunes) y prohibirle fabricar el resto.
**Tercera aparición del puente** (`cop_por_1_usd`, `usd_por_1_cop`, las fechas), y
tercera vez que sale casi gratis: 101 tokens, $0,0001 por vuelta.

> **Darle el dato hecho sale siempre más barato que el error.**

### L6b.23 — Un dato nuevo en el prompt puede cambiar comportamientos que no tienen nada que ver con él

Con el calendario puesto, el agente **dejó de llamar a `trm()`** y aun así afirmó
cuál TRM estaba vigente… equivocándose de día. Y al final preguntó *"¿necesitas
saber la TRM de hoy?"*: **sabía que no la tenía, y ya lo había afirmado.**

> ⚠️ **Le diste fechas y dejó de pedir tasas.** Con material para deducir, dedujo
> en vez de consultar. Un cambio en el prompt no se verifica solo en lo que venía
> a arreglar.

### L6b.24 — Pulir un prompt contra una sola muestra es perseguir la cola

Tres rondas de prompt en un día. Cada una **arregló lo que buscaba y destapó algo
nuevo**, porque cada una se juzgó con **una** muestra.

> 🚨 **Cuando cada parche destapa otro, lo que falta no es un parche mejor: es el
> instrumento de medida.** Reconocer que un método se agotó vale más que una ronda
> más.

📌 Corolario del cierre: **cambiar el prompt sin evals es refactorizar sin tests.**

### L6b.25 — La memoria que recibe el agente son HECHOS, no el hilo

El examen lo destapó: con la ficha *"prefiere los valores en pesos"* delante, ante
*"¿Y 450 dólares cuánto serían?"* el agente contestó **"¿a qué moneda quieres
convertir?"**.

> **La memoria NO es el historial de la conversación.** Para el usuario la
> relación es continua —por eso escribe una pregunta de seguimiento— pero el turno
> 2 arranca en blanco: **sabe quién eres y no sabe de qué estaban hablando.**

No es un bug: es el límite de esta escuela de memoria. Y **no se ve hasta que
alguien encadena dos preguntas.**

### L6b.26 — El peor choque entre dos criterios no es que midan lo mismo: es que premien lo contrario

Al escribir C9 (*¿usó lo que recordaba?*) aparecieron tres solapamientos, y los
dos peores daban veredictos **opuestos a la misma frase**:

| | la misma respuesta era… | dónde quedó la línea |
|---|---|---|
| C4 | levantar la frontera (`PASA`) **e** ignorar la ficha (`FALLA`) | si la memoria ya resuelve la ambigüedad, **no hay frontera** |
| C5 | admitir el límite (`PASA`) **y** desconocer lo que tenía (`FALLA`) | la línea es *"¿podía saberlo?"* |
| C7 | ¿afirmar desde una ficha es *afirmar sin fuente*? | **no: una ficha ES fuente**, llega en el system prompt |

> ⭐ **Cada cosa se castiga en UN solo lugar.** Si no, una misma falla resta tres
> veces y el juez tiene que elegir — que es literalmente lo que rompió C6.

### L6b.27 — Un criterio nuevo no crea evidencia: solo mira la que ya hay

Dos caras del mismo hecho, y las dos costaron:

1. **Un criterio sin su evidencia no queda sin medir: queda midiendo MAL.** C7
   pidió algo que el juez no veía y sacó un **62% que era falso** — las cinco
   fallas eran del juez, no del agente. Y un número mal medido **se ve igual de
   bueno que uno verdadero**. → Por eso C9 se diseñó reutilizando la evidencia que
   ya existía para C8: **más barato y más seguro que inventarla.**
2. **C8 tiene 16 casillas; C9 tiene 3.** Es la misma memoria vista por sus dos
   lados: **guardar se puede vigilar en todas partes; USAR solo se ve en la
   conversación siguiente.**

> ⭐ **La memoria no se mide mejor agregando criterios, sino agregando PARES de
> conversaciones.** El techo es la forma del examen, no la rúbrica.

### L6b.28 — Escribir el instrumento es gratis; usarlo es lo que cuesta

Son dos gastos distintos y venían pegados en una sola recomendación:

| | |
|---|---|
| escribir C9 | **$0** |
| saber qué DA C9 | ~$0,25 y una auditoría entera |

Lo mismo por el otro lado: con el defecto de C7 ya diagnosticado, recalificar
habría costado $0,25 **y no habría agregado conocimiento** — el número ya se
sabía. Se arregló el código para que el defecto no vuelva, y no se recalificó.

> **Cuando encuentres un defecto en tu instrumento, pregúntate si necesitas volver
> a medir o si ya sabes qué habría dado.**

💰 Y los dos errores de costo del examen, que son la misma advertencia:

- El presupuesto se estimó heredando *"10 preguntas **en sonnet**"* cuando el
  examinado era **haiku**: $0,72 estimado contra $0,17 real. → **Un número
  heredado arrastra los supuestos con los que nació.**
- Al juez se le contó la respuesta visible y **no los tokens de pensamiento**:
  $0,34 estimado contra **$0,666** real, a dos casos de cortar la evaluación por
  la mitad. → **Lo que el modelo piensa y tú nunca ves se paga completo.**

### L6b.29 — Una rúbrica puede mezclar lo medido y lo supuesto, siempre que se distinga a simple vista

C9 se escribió y **nunca se corrió**. Quedó marcado así en **tres sitios**: el
encabezado del `.md`, el criterio mismo y la tabla de pendientes. C1–C8 tienen una
corrida detrás; C9 no tiene ninguna.

Y lo mismo con el 100% de C7 después de la auditoría: **es derivado, no medido** —
sale de leer las cinco justificaciones, no de volver a correr.

> Un instrumento a medias sirve. Un instrumento a medias **que no dice cuál mitad
> es cuál** produce números con la misma cara que los verdaderos.

⭐ Y un detalle que confirmó una decisión vieja: **`cargar_rubrica()` no se tocó al
agregar C7, C8 ni C9.** El instrumento vive en el `.md`; el código solo lo
transporta.

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


---

## Nivel 6c — TypeScript

> Sesiones 24 a 27. Carpeta `06c-typescript/`. Costo del nivel entero:
> **$0,1084**.
>
> Este nivel **no trae conceptos nuevos de agentes**: traduce a otro idioma el
> agente del nivel 3, que ya funcionaba. Por eso casi todas las lecciones son
> comparaciones — *lo mismo, pero aquí pasa así* — y por eso muchas rescatan
> bugs viejos de Python que el compilador atrapa **antes de correr y antes de
> pagar**.

### L6c.1 — TypeScript no corre: se compila. Hay dos archivos, no uno

El `.ts` es lo que escribes. El `.js` de `dist/` es **lo que corre**. Node no
entiende TypeScript; entiende lo que `tsc` escribió a partir de él.

Todo lo raro de este nivel sale de ahí: la ruta al `.env`, los tipos que
desaparecen, los avisos que no detienen nada.

> **En Python el archivo que abres es el que corre. Aquí no.**

### L6c.2 — Los tipos son para ti, no para la máquina

`const nombre: string = "Juan"` quedó en el `.js` como `const nombre = "Juan"`.
Los tipos **no están** en lo que corre. El traductor los leyó, avisó con ellos,
y los borró.

Los comentarios sí sobreviven a la traducción. Los tipos no.

> Un tipo vive **antes** de correr. Después no existe nadie que lo haga cumplir.

### L6c.3 — Un aviso que no detiene nada es un aviso que se puede ignorar

Pasarle un número a una función que pedía texto dio `TS2345`... **y el programa
imprimió `Hola, 42` igual.** `tsc` protestó y aun así escribió el `.js`.

El arreglo es `noEmitOnError` en `tsconfig.json`: con un error, no hay `dist/`.

> Es el eval en verde del 6b y el *"Anotado"* sin anotar, otra vez. **Un freno
> que solo habla no es un freno.**

### L6c.4 — Un tipo no dice de qué CLASE es el dato: dice qué VALORES son legales

`role: "user" | "assistant"` no dice *"role es un texto"*. Dice que hay dos
valores y no hay tercero. Y por saberlo, el compilador puede hacer algo que
ningún error de la API hace:

```
error TS2820: Type '"assistnat"' is not assignable to type '"assistant" | "user"'.
              Did you mean '"assistant"'?
```

**Corrige el typo.** En Python ese mismo typo era un string válido y el error
llegaba como un 400, después de pagar.

> Cuanto más **estrecho** el tipo, más errores atrapa gratis.

### L6c.5 — `any` no es "no sé qué tipo es": es "no revises nada"

Al mismo objeto al que le faltaba una llave obligatoria: con el tipo escrito,
`TS2741: Property 'content' is missing`. Con `any`, **ningún error**. El typo
pasa en silencio hasta la API.

> `any` no ahorra trabajo: lo aplaza y lo encarece.

### L6c.6 — En JavaScript nada bloquea nunca. Una función lenta devuelve un recibo

En Python `client.messages.create(...)` **detiene** el programa hasta que llega
la respuesta. En JavaScript devuelve en el acto una **promesa**: un recibo que
dice *"esto llegará"*.

No es un capricho del idioma. JS nació dentro del navegador, donde detener el
programa habría congelado la página delante del usuario.

> `await` es *"aquí sí espérame"*. Es la excepción, no la regla.

### L6c.7 — Olvidar un `await` no da error: da `[object Promise]`

```
1. Sin await  →  [object Promise]
```

Nadie avisa. En un agente se ve como *"la respuesta llegó vacía"*, o peor: como
`[object Promise]` metido dentro de un prompt que **sí se paga**.

> El fallo más caro no es el que revienta: es el que sigue corriendo con basura
> adentro.

### L6c.8 — Lo molesto se convierte en la ventaja: `Promise.all`

Las mismas 3 llamadas lentas:

| | tiempo |
|---|---|
| en serie (lo que hace Python) | 3.024 ms |
| en paralelo (`Promise.all`) | 1.007 ms |
| | **3,0x** |

Tener que pensar en promesas es el precio; poder lanzar tres cosas a la vez sin
esfuerzo es lo que compras con él.

> Un agente que consulta tres herramientas independientes no tiene por qué
> consultarlas de a una.

### L6c.9 — Un `try/catch` sin `await` adentro no protege nada — y además mata el proceso

El `try` termina **antes** de que el error ocurra, porque lo que hay dentro solo
dejó un recibo. Cuando el error llega, ya no hay nadie atrapándolo, y no es que
se escape: **tumba el proceso entero**.

> Otra vez el freno que se ve puesto y no frena. **Un `catch` alrededor de una
> promesa sin `await` es decoración.**

### L6c.10 — TypeScript no sabe nada de Node por su cuenta

`error TS2591: Cannot find name 'process'`. El idioma nació en el navegador: ahí
no existen `process`, ni archivos, ni carpetas. Hay que decirle que va a correr
en Node (`"types": ["node"]`).

📌 `@types/node` **no es código**: son solo las descripciones de tipos de cosas
que ya existen.

> Los tipos y el código son dos paquetes distintos, y a veces se instalan aparte.

### L6c.11 — La ruta se calcula desde donde corre el `.js`, no desde donde vive el `.ts`

En Python el `.env` estaba **dos** niveles arriba. Aquí son **tres**, porque el
archivo que corre está dentro de `dist/`.

> Primera consecuencia práctica de L6c.1, y la primera que hace perder media
> hora. Si una ruta relativa falla, pregunta **quién** la está resolviendo.

### L6c.12 — `content` no es una lista de textos: es una lista de bloques, y por eso `content[0].text` no compila

```
error TS2339: Property 'text' does not exist on type 'ContentBlock'.
```

El SDK declara `TextBlock | ThinkingBlock | ToolUseBlock` — la misma unión de
L6c.4, escrita por la librería. Hay que **estrechar** con
`if (bloque.type === "text")`.

Y el compilador tiene razón, porque **ese bug ya pasó**: nivel 1, `max_tokens=30`
con Opus, los 30 tokens se fueron en el bloque `thinking`, no hubo bloque `text`,
y la pantalla salió vacía sin ningún error (L1.1, L1.2).

> El aviso no es una molestia: es el bug del nivel 1 atrapado **antes de correr
> y antes de pagar**.

### L6c.13 — Opus 5 piensa por defecto, y ese pensamiento invisible se cobra

Omitir el parámetro `thinking` **no lo apaga** (equivale a `adaptive`) — es un
cambio respecto a Opus 4.8/4.7. Y `display` vale `"omitted"` por defecto: el
bloque llega, pero vacío. Está ahí, callado y cobrado.

Medido con `count_tokens`, gratis:

| | tokens |
|---|---|
| texto que se vio | ~176 |
| cobrado | **235** |
| **pensamiento invisible** | **~59 (25% de la factura)** |

🚨 Y la consecuencia práctica: **`max_tokens` es el techo de pensamiento +
respuesta juntos.** Ajustarlo al tamaño de la respuesta esperada corta el texto
a mitad de frase.

> Es L1.1 con otra cara — y ahora se sabe *por qué* pasó.

### L6c.14 — La documentación da el mecanismo; la magnitud solo sale al medir

La referencia del SDK explicó correctamente **qué** pasaba con el thinking. El
**cuánto** no estaba ahí, y el número que puse de mi cabeza (~100) resultó ser
casi el doble del real (59).

> Consultar la documentación no reemplaza correr el experimento. Responden a
> preguntas distintas.

### L6c.15 — Marcar algo como sospecha es lo que evita que alguien construya encima

La hipótesis del thinking acertó; mi número falló. **No hizo daño**, y la razón
es que estaba escrito como *sospecha*, no como dato.

> **Un número escrito en el material tiene que venir de una corrida, o venir
> marcado como estimación.** Marcarlo salva; afirmarlo cuesta.

### L6c.16 — `unknown` no es `any`

El SDK declara `input: unknown` en el bloque `tool_use`, y leerlo directo no
compila: `TS18046: 'bloque.input' is of type 'unknown'`.

- `any` dice *"no revises nada"* → deja pasar en silencio.
- `unknown` dice *"hay algo y no sé qué es"* → **frena hasta que compruebes**.

Comparado con `TS2339` del paso 3, es otro grado de ignorancia: allá el
compilador sabía qué había y sabía que `.text` faltaba; aquí no sabe ni qué hay.

> El tipo correcto para lo que viene de afuera es el que **obliga** a mirar.

### L6c.17 — Los tipos protegen lo que TÚ escribes. Donde entra algo de afuera, se acaban

El modelo, un archivo, internet: ahí los tipos no alcanzan y empieza la
comprobación **en tiempo de ejecución**. Que es exactamente lo que hacen los 10
frenos de `herramientas.py` del 5b.

> La novedad no es la idea: es que **el compilador no te deja olvidarla**.

### L6c.18 — `as` no comprueba, no convierte, no existe

`(input as { ciudad: string }).ciudad` quedó en el `.js` compilado como
`return input.ciudad;`. El `as` **no está**. Lo único que hace es callar al
compilador. (Detalle bonito: la única vez que aparece `ciudad: string` en el
`.js` es dentro de un comentario.)

Contra los 4 `input` que el modelo puede mandar: la función que comprueba acertó
**4 de 4**; el `as`, **1 de 4** — y ninguna de las dos dio un aviso al compilar.

- 🔑 **El daño de `as` no es que falle: es DÓNDE falla.** Miente en un sitio y
  revienta en otro, lejos, con un error que no menciona la causa.
- 🔑 **Cuándo sí:** cuando el dato es tuyo y sabes algo que el compilador no
  puede saber. **Nunca** sobre lo que escribió el modelo, un archivo o internet.

### L6c.19 — Un `null` aplasta tres motivos distintos en uno. La unión discriminada los guarda

```ts
type Lectura =
  | { ok: true;  ciudad: string }
  | { ok: false; error: string };
```

La función *sabía* cuál de los tres `if` había fallado, y con `string | null`
tiraba ese dato a la basura — dejando al bucle inventarse un mensaje genérico.

> Si tu función descubre algo y devuelve menos de lo que descubrió, ese trabajo
> lo va a repetir alguien más arriba. O nadie.

### L6c.20 — Un buen mensaje de error nombra el error Y nombra el arreglo

*"le diría que la llave se llama `ciudad`, no `ciuadd`"*. **Son dos datos, no
uno**, y el segundo no cabía en la función vieja: había que leer
`Object.keys(input)`, que estaba ahí gratis y nadie miraba.

Cada vuelta que el modelo gasta adivinando la paga el dueño del agente.

> **Un mensaje de error solo puede ser tan bueno como lo que tu código se
> molestó en mirar.**

### L6c.21 — No se puede olvidar el caso malo: el freno lo pone el idioma, no la disciplina

`leerCiudad(x).ciudad` directo **no compila**. Con la unión discriminada, TS
obliga a preguntar `if (lectura.ok)` antes de leer nada.

> En Python olvidarse del caso malo es un descuido. Aquí es imposible. **Esa es
> la diferencia que se compra con los tipos.**

### L6c.22 — El mensaje de error es código también, y puede tener el mismo bug del que protege

`null` producía *"esperaba un objeto y llegó un object"*, porque
**`typeof null === "object"`**. El comentario del freno anunciaba la trampa y el
mensaje la olvidaba.

Salió de **probar** los frenos con 7 casos sin API, no de leerlos.

> Nadie prueba los mensajes de error. Por eso mienten.

### L6c.23 — Un candado solo se sabe que sirve rompiéndolo a propósito

En dos días de corridas normales el freno **nunca disparó**: el modelo mandó la
llave correcta las 3 veces. Con `SABOTEAR = true` renombrando la llave a
`ciuadd`, el patrón fue el mismo en las tres preguntas: `tool_use` → **error** →
`tool_use` correcto → `end_turn`. Nunca se cayó, nunca inventó un dato.

> Un freno que nunca disparó no está demostrado: está **sin probar**. Sabotéalo
> tú, que es barato, antes de que lo sabotee la producción.

### L6c.24 — 🚨 Un error no se paga una vez: se paga en CADA vuelta posterior

| | limpio | saboteado | dif |
|---|---|---|---|
| vueltas | 6 | **9** | +3 |
| entrada | 3.030 | **5.165** | +70% |
| costo | $0,027825 | **$0,046050** | **+65%** |

La vuelta 3 de Medellín pagó más tokens de entrada que **cualquier** vuelta de
la corrida limpia, porque el historial **todavía lleva adentro el intento
fallido**: el `ciuadd`, el mensaje de error, la disculpa. Todo eso vuelve a
entrar y se vuelve a pagar.

> En un agente, un error no es un evento: es **peso permanente en el historial**.
> Por eso el mensaje bueno de L6c.20 se paga solo.

### L6c.25 — El texto del menú de herramientas se paga en cada vuelta

Las tildes del menú costaron +2 tokens, y cada pregunta +3. Total **+5 sobre 457:
un 1,1%**, $0,00008 en la corrida entera. El hallazgo no es ese.

El hallazgo es que **la descripción de las herramientas entra completa en cada
vuelta**. Con 3 ciudades da igual; con 20 herramientas de tres párrafos en un
agente de 8 vueltas, es una **factura recurrente**. *Eso* es decisión de
ingeniería. Las tildes no.

Y de paso: **una tilde no cuesta un token**. Tres sitios cambiados dieron +2, dos
sitios dieron +3. Depende de cómo el tokenizador parta la palabra.

> El conteo se mide, no se deduce.

### L6c.26 — Un hallazgo del 1% se cierra, no se actúa

Saber de dónde salen los +5 vale mucho. Cambiar el código por $0,00008 no vale
nada — y el nivel 5 ya midió que escribir mal el prompt **empeora la respuesta**
(rioplatense, tú/usted mezclado). Ahorrar el 1% pagándolo en calidad es mal
negocio.

> Entender por qué pasa algo y decidir hacer algo al respecto son dos decisiones
> separadas. La segunda casi siempre es "no".

### L6c.27 — El idioma no cambia la factura

Mismo agente, mismas 3 preguntas, Python contra TypeScript: 3.062 vs 3.050
tokens de entrada, ~$0,030 vs $0,028.

> **Los tokens los cuenta la API, no `tsc` ni Python.** Cambiar de lenguaje no
> es una optimización de costo.

### L6c.28 — Contar es determinista; generar no

Las vueltas 1 dieron **exactamente** los mismos tokens de entrada en las dos
corridas (457 / 463 / 457), porque la entrada era idéntica. Las vueltas 2
cambiaron, porque ahí entra lo que el modelo dijo antes.

> En un agente, la parte reproducible se acaba en la primera vuelta. Eso decide
> qué se puede comparar directamente y qué hay que correr N veces.

### L6c.29 — Precios escritos de memoria: quinta vez, y así se cazó

`05_frenos.ts` salió con `$15/$75` por millón; Opus 5 cuesta **$5/$25**. La
primera corrida imprimió $0,083475 cuando el costo real era $0,027825.

**Se cazó porque no cuadraba con un número que SÍ estaba medido:** el paso 4 dio
$0,028375 con 3.050/525, y esa cuenta solo cierra con 5 y 25. Se verificó contra
la documentación oficial antes de corregir — no de memoria otra vez.

> **Tener mediciones viejas escritas es lo que hace que las mentiras nuevas se
> noten.** La bitácora no es archivo muerto: es el detector.

---

## Nivel 7 — Producción

> 🌉 **Este bloque tiene una rareza, y es a propósito.** El código del nivel 7 vive en
> **otro repositorio** (TEAPP), así que aquí no hay script que abrir. Lo que sí vive
> aquí es lo que se aprendió, que es lo que sobrevive al proyecto.
>
> 📌 **Y hay un segundo bloque de este nivel más abajo: `Método`, las `LM.x`.** No se
> mezclan a propósito. Las `L7.x` son de **producción**: concurrencia, registros,
> nube, instrumentos. Las `LM.x` son del **oficio**: cómo se trabaja con dos
> terminales, cómo se entrega un hallazgo, cómo se sella una predicción. El nivel 7
> produjo las dos cosas, y la segunda resultó ser la más transferible.
>
> ✅ **Nivel CERRADO el 2026-08-19 (sesión 89).** Los diez pasos de TEAPP caminados.

---

### L7.1 — La escritura atómica y el candado resuelven cosas distintas

El servidor se caía con varias personas a la vez: 50 peticiones simultáneas daban
entre **31 y 39 fallos**, y de 50 puntos el marcador guardaba **8**.

Eran **dos** defectos con el mismo síntoma. Todas las peticiones escribían el mismo
archivo temporal. Y además la función que sumaba un punto **leía y escribía con un
hueco en medio**: dos personas leían el mismo número, las dos sumaban uno, las dos
guardaban lo mismo. Un punto desaparecía sin que nada diera error.

> 🔑 **La escritura atómica protege de UNA escritura cortada por la mitad. El candado
> protege de DOS escrituras pisándose. Tener la primera no te da la segunda.**

Después del arreglo: **300 peticiones simultáneas, 0 fallos, la secuencia 1…300
completa.**

### L7.2 — Un test en verde no dice «el código está bien»

Dice **«el código está bien para lo que este test hace»**.

Los 45 tests que había no veían nada de `L7.1`, y no por descuido: el cliente de
pruebas manda las peticiones **de una en una**. Ningún test creó jamás el estado que
rompía el programa — dos peticiones a la vez.

> 🚨 **Un defecto de concurrencia no se encuentra probando más veces. Se encuentra
> probando de otra forma.** Y esa forma no existía en la suite, así que la suite no
> podía ponerse roja aunque el defecto estuviera delante.

📌 Es el primer sitio del curso donde *todo verde* y *funciona* se separan del todo.
Antes del nivel 7 solo había una persona: la simultaneidad no existía.

### L7.3 — Al log el detalle; al navegador, un mensaje corto y sin rutas

El error 500 devolvía al usuario la **ruta absoluta del servidor**. Eso le regala a
un desconocido el mapa de tu máquina: dónde vive el código, cómo se llama el usuario
del sistema, qué estructura hay debajo.

> 🔑 **El mensaje de error tiene dos públicos con necesidades opuestas.** Tú necesitas
> todo el detalle; el desconocido no necesita ninguno. **Es la misma excepción
> partida en dos destinos**, no un mensaje que hay que hacer más vago.

⚠️ Y la nota de que había que arreglarlo **existía, escrita, y no bastó**. Lo que lo
cazó fue **volver a medirlo**.

### L7.4 — Un registro se diseña por la pregunta, no por lo que es fácil escribir

La tentación es apuntar lo que se tiene a mano. El registro útil se escribe al revés:
primero la pregunta que tendrás a las 3 de la mañana con usuarios encima, y de ahí
salen los campos.

Y la pregunta que casi nadie escribe primero: **¿qué está pasando cuando ya nadie
mira la pantalla?** No es *¿funciona?* — eso es evaluación, y se pregunta antes de
soltarlo. Es *¿qué está haciendo AHORA?*, con gente encima y una tarjeta pagando.

### L7.5 — Declarar cuánto se le permite durar a algo no es haber medido cuánto duró

Para saber si vale la pena cambiar a un modelo más barato hay que saber **qué
fracción del tiempo es el modelo**. En una corrida medida: **20,7 s de Claude sobre
59 s totales.** Sin ese reparto, una optimización del modelo parece inútil cuando el
culpable era la cola de espera.

Al buscar dónde estaban esos números, esta terminal propuso escribir el reparto en
cuatro fases *porque la arquitectura ya piensa en fases*.

**Esos cuatro nombres eran un `Timeout`: un presupuesto que se le entrega a la
librería, no un cronómetro.** Los números no existen — solo hay un total.

> 🔑 **Un tope y un reloj se parecen en el papel y no tienen nada que ver.** Uno dice
> *cuánto permito*; el otro, *cuánto pasó*. Y el error se cometió **con el archivo
> abierto y leído**: no bastó con mirar el sitio correcto, hubo que clasificarlo bien.

### L7.6 — El registro tiene una cuarta pregunta: quién puede leerlo

Las tres de siempre son qué apuntar, cuándo y dónde. La cuarta aparece el día que en
el registro hay **texto escrito por personas de verdad**.

Un registro con las frases que la gente escribió es datos personales: vive en un
disco, se copia en las copias de seguridad y sobrevive al proyecto. El nivel 7 lo
resolvió apuntando **la forma de lo que pasó y nunca la frase** — cuántas palabras,
qué falló, cuánto tardó; no qué dijo.

> 📌 **Y tuvo un coste que hay que ver:** por eso mismo la traza **no sirve** para
> alimentar los evals, que necesitan el texto. Son dos caminos separados y se pagan
> dos veces. **La decisión correcta cuesta algo; si no cuesta nada, revísala.**

### L7.7 — Un instrumento tiene que ser más estable que lo que mide

El corrector automático marcaba **cualquier** comilla; la regla solo prohibía las que
envuelven una corrección. Afinarlo exigía que el programa supiera **qué trozo es la
corrección**, y eso entraba de **cinco formas distintas** en las respuestas medidas.

Cualquier detector fino habría sido una heurística sobre **el fraseo del modelo** —
que es justo lo que cambia al cambiar de modelo. El día que fallara, nadie podría
distinguir *el modelo se rompió* de *la heurística resbaló*.

> 🔑 **Se endureció la regla, no el instrumento.** Una sola regla dicha igual en los
> dos sitios. **Si tu medidor se mueve cuando se mueve lo medido, no estás midiendo.**

📌 Y su pariente: **una promesa que el mejor modelo rompe casi siempre no es un
instrumento, es una constante.** Un detector ya rojo no puede avisar de nada.

### L7.8 — Un instrumento que cuenta y tira la evidencia obliga a pagar dos veces

La primera medición contó **18 fallos y tiró el texto**. El número sorprendente llegó
*después* del gasto, sin forma de investigarlo sin volver a pagar.

Se añadió el guardado — y se perdió otra vez, porque el archivo tenía **un nombre
fijo**: una tanda de diagnóstico de 10 respuestas se comió la línea base de 60, ya
pagada.

> ⚠️ **El arreglo no era dejar de sobrescribir.** Sobrescribir estaba bien razonado:
> dos corridas mezcladas son dos modelos revueltos. **Lo que fallaba es que el nombre
> del archivo no distinguía aquello que la sobrescritura existía para no mezclar.**

→ El nombre acabó con **cuatro ejes**: modelo, fecha, un sello de la pregunta y del
examen, y si la tanda fue completa o un recorte. **Cuando algo se sobrescribe, el
nombre es el único sitio donde puede vivir la identidad.**

### L7.9 — Un comentario equivocado es peor que ningún comentario

El precio por llamada estaba escrito en **dos** archivos. El aviso de que había
caducado se puso en uno — y el que iba a gastar el dinero era el otro. La copia mala
estaba **tres líneas debajo** de un comentario que decía *esto se importa, no se
copia*.

> 🔑 **El daño no es que mienta: es que resuelve la duda del lector en la dirección de
> no mirar.** Quien iba a corregir el número leyó que había una sola copia y **dejó de
> buscar la segunda**.

📌 Y la cola es larga: cuando por fin se arregló la constante, **tres citas del número
viejo sobrevivieron** en comentarios, una de ellas con la etiqueta «medido, no
estimado». **La constante se arregla en su casa; las copias se quedan.**

### L7.10 — Los bugs que no puedes ver en tu máquina son los caros

`Juan` y `juan` son **una persona en Windows y dos en Linux**. Si un nombre escrito
por el usuario se convierte en nombre de archivo sin normalizar, el marcador se parte
en dos al desplegar — **sin ningún error, y con todos los tests locales en verde**.

→ Normalizar (minúsculas y recorte de espacios) **antes de que el texto toque el
disco**. Es una línea, y hay que escribirla el día que aún no duele.

### L7.11 — La alarma de facturación va ANTES de subir nada

No después del primer despliegue: antes. Y el motivo no es el susto, es el reloj: el
plan gratuito corre **6 meses desde el día que abres la cuenta**, la uses o no. Por
eso la nube va en el paso 7 y no en el 1 — cuando se abre, ya hay algo que subir.

⚠️ **Y un `0,00 USD` acompañado de `Sin datos` no es un cero medido.** Es la ausencia
del dato disfrazada de dato bueno. La primera factura tarda unas 24 h en existir, y
ese reloj arranca en la primera visita a la consola, no en el primer gasto.

> 🚨 **Contra un gasto de `0,00` no hay umbral positivo que dispare.** Una alarma
> puesta en `0,01 US$` puede pasar días sin sonar y parecer que vigila. **No estaba
> vigilando: no había nada que ver, y el silencio se leía como confirmación.**

### L7.12 — La raíz de los datos, absoluta y sin valor por defecto

Un guion de medida escribió en los datos **de verdad** porque heredó una ruta
relativa. Corría fuera de los tests, así que ningún test podía verlo.

→ La carpeta de datos sale de una **variable de entorno, absoluta y sin valor por
defecto**: sin ella, la aplicación **no arranca**.

> 🔑 **Un valor por defecto cómodo es un camino que nadie eligió y que siempre existe.**
> Quitarlo convierte un error silencioso en un arranque fallido, que es justo el
> cambio que quieres: **el fallo ruidoso es más barato que el dato corrompido.**

### L7.13 — Lo que este nivel enseñó sobre terminar

El paso 9 no tenía **criterio de cierre escrito**. El mapa le dedicaba una línea, y
los ocho pasos anteriores se habían cerrado con una decisión anotada; el 9 no tenía
ninguna.

> 🔑 **Sin criterio escrito un paso no se cierra: se abandona.** Y se abandona **por
> cansancio**, en el momento en que la lista de tareas pequeñas parece vacía — que no
> es lo mismo que estar terminado.

Al final el nivel se cerró con una decisión de alcance, no con la lista vacía: **se
renunció a comparar modelos, firmado y explicado**, porque el aprendizaje del tramo
ya estaba cobrado. Con deuda viva registrada a propósito, y dormida.

📌 **El porqué completo de esa renuncia —y la trampa que trae— está en `LM.62`.** Es
la lección de cierre del nivel, y vive en el bloque `Método` porque no es de
producción: es de cómo se decide **dejar de trabajar en algo**.

---

## Método — el oficio y las dos terminales

> ⚠️ **Este bloque no es de un nivel.** Los demás bloques cierran un nivel del
> curso; este recoge lo que se entendió **sobre el oficio mismo** y sobre cómo
> trabajamos. Salió de la sesión 43, una conversación **sin una línea de código**.
> Se numera `LM.x` para que no se confunda con las lecciones de nivel.
>
> 📌 **Creció en la sesión 44** (`LM.6` a `LM.11`): cómo se corta el trabajo —
> feature, vertical slice, walking skeleton, tracer bullet, MVP y cuánta
> arquitectura se decide antes de escribir código. También sin una línea de código.
>
> ✏️ **Y en la sesión 45:** él corrigió `LM.8` —su prototipo es un wireframe o un
> HTML clicable, **desechable y puede que sin una línea de código**— y de ahí
> salió `LM.12`, la que más le sirve a este proyecto.
>
> 🔬 **De `LM.13` en adelante cambia de origen, y conviene saberlo al leerlas.**
> Ya no salen de conversaciones sobre el oficio, sino de **las sesiones de
> supervisión del nivel 7**: esta terminal audita lo que la otra construye, y cada
> lección es un error real —de ellos o **mío**— con la corrida que lo demostró
> detrás. Por eso muchas se citan entre sí: **son el mismo puñado de bichos
> saliendo por sitios distintos**, y la tabla comparativa que llevan varias es
> justo para no confundirlos.
>
> 📌 El nivel 7 todavía no tiene bloque, y es correcto: **no ha cerrado.** Estas
> `LM.x` **ascienden sobre la marcha** desde `PROGRESO.md`, sin esperar al cierre
> del nivel — se decidió así porque una lección que solo vive en el archivo largo
> es una lección que `LM.24` predice que nadie va a alcanzar.

### LM.1 — Producir se abarató. Decidir, limitar y demostrar cuestan lo mismo

La respuesta fácil —*"antes escribías el código y ahora lo escribe la IA"*— es
falsa en la parte que importa. Decidir qué construir, poner límites y demostrar
con hechos **son el oficio desde siempre**. No son categorías nuevas.

Lo que cambió es la **proporción**:

```
antes                              ahora
decidir y limitar ....  20         decidir y limitar ....  20   ← igual
escribir el código ... 100         escribir el código ...   5   ← se desplomó
demostrar ............  30         demostrar ............  30   ← igual
                      ----                                ----
                       150  (67% escribir)                  55  (9% escribir)
```

El trabajo total **bajó**. Pero lo que rodea al código no se movió de precio y
ahora es casi todo el trabajo. Antes quedaba tapado detrás de las 100 unidades de
teclear.

> **Siempre costó esto. Al desaparecer lo de escribir, quedó a la vista lo que
> siempre estuvo debajo.**

Y dos cosas sí son nuevas de verdad, no proporción: **el sistema no repite** (la
misma entrada da salidas distintas → L5.x, rúbricas y juez) y **la corrida
cobra** (*"un agente roto gasta antes de fallar"*, nivel 3).

### LM.2 — Lo barato es lo que se puede deshacer

Mejor regla que *"escribir es barato, probar es caro"*:

> **Lo barato es lo reversible. Lo caro es lo que no se deshace.**

El código se borra y no pasó nada. No se deshacen: **el reloj** (los 6 meses de
AWS), **la factura**, **el historial de Git** y **el dato de una persona**.
Escribir la IP en `PROGRESO.md` costó un segundo; borrarla del historial, no
existe (sesión 42).

Corolario que explica cuatro sesiones del nivel 7 con **$0,00** gastados: el
trabajo caro se hace mientras **todavía es reversible**.

### LM.3 — Producir código nunca fue lo que hacía a alguien senior

Quien solo sabe producir **sí está en problemas**: su ventaja era la velocidad, y
la velocidad se abarató para todo el mundo. Pero eso no describe a alguien senior
de verdad — describe a un productor veloz con muchos años. Los agentes no lo
destronaron: **le quitaron el disfraz.**

Nadie fue senior por teclear rápido. Fue senior por haber estado presente cuando
las cosas se rompieron. *"Esa prueba pasa siempre, no prueba nada"* **es** decidir,
limitar y demostrar. Venía empaquetado con la producción y no se veía aparte.

| ser senior hoy | |
|---|---|
| Saber qué **NO** construir | La decisión más cara, y no la toma un agente |
| Saber qué **puede** fallar | Antes de que falle, sin haberlo visto fallar aquí |
| Saber qué **prueba de verdad** | Distinguir el test que mide del que solo pasa |
| Saber qué es **irreversible** | Y tratarlo distinto (LM.2) |
| **Responder** por el resultado | Un agente no firma nada. Alguien firma |

> **Los agentes cerraron la brecha de producción y ensancharon la de criterio.**

El hábito de verificar se aprende en una semana. Saber **qué** verificar tarda
años, porque se aprende chocando. Y con agentes es peor: el código sale limpio,
comentado y con tests en verde, así que **un junior se siente senior** — y falla
por algo que nunca estuvo en pantalla (`cp1252`, `Juan` vs `juan`, la IP pública).

📌 La buena noticia: hoy se puede entrenar el criterio desde el principio, porque
la producción ya no consume el tiempo. **El camino es más corto que antes. Corto
no es instantáneo.**

### LM.4 — Quien construye no puede ser su propio testigo

La lección que sostiene todo el método de las dos terminales. Tres pruebas del
propio proyecto, y las tres son el mismo animal:

| | qué pasó |
|---|---|
| **Sesión 30** | `session-starter` **se inventó** las tres herramientas del proyecto. Lo cazó la otra terminal leyendo `scope.md` — el documento, no el reporte |
| **Sesión 33** | El cierre **se cumplió entero** y el trabajo vivía en un solo disco. El protocolo estaba conforme consigo mismo; `git status -sb` no |
| **Sesión 42** | *"nada que verificar, es una cuenta externa"*, dicho por quien hizo la tarea. `nslookup` tardó dos segundos y lo desmintió |

> Un sistema que se revisa a sí mismo comprueba **que es coherente**, no que sea
> cierto.

### LM.5 — La terminal que supervisa vale por lo que NO sabe

Contraintuitivo y es el corazón del esquema:

> Si le das a la supervisora todo el contexto de la que construye —su narrativa,
> su archivo de progreso, su versión de lo ocurrido— **deja de ser un control y
> se vuelve un eco.** Dos terminales de acuerdo no valen más que una.

**Las cuatro cosas que sí necesita:**

1. **El contrato, no la construcción.** Qué se prometió y qué cuenta como
   cumplido (`_context/scope.md`, las tareas con su criterio). **No** el relato
   de lo que se hizo.
2. **Cómo comprobarlo desde fuera.** Los comandos que corre ella misma:
   `pytest`, `git status -sb`, `nslookup`, un `curl` contra el puerto real. Es lo
   único que la otra no puede darle.
3. **El catálogo de cómo fallan las cosas** — la **forma** del fallo, no la
   anécdota. No viaja *"la IP entró el 5 de agosto"*; viaja *"un dato que no
   parece secreto entra al historial público, y Git no olvida"*. La primera es
   historia; la segunda es un **detector reutilizable**.
4. **La lista de lo irreversible** (LM.2). Es el `T-068` de TEAPP, generalizado.

**Lo que NO debe tener:** el `progress.md` del otro **como fuente de verdad** (se
lee como *afirmación por verificar*); el estado del curso (**ruido con
autoridad**); y **permiso de escribir** en el repo del otro — en el momento en
que edita, deja de poder revisar.

**Y el ciclo, que hasta hoy solo vivía en la cabeza del estudiante:**

```
la otra terminal reporta    →  la supervisora NO lo cree
la supervisora mide         →  con sus propios comandos
compara: lo dicho vs medido →  la diferencia es el hallazgo
devuelve una LISTA          →  no un parche: ella no edita
la otra arregla y reporta   →  y vuelve a empezar
```

> Cinco renglones, y son la mitad del valor del esquema. Hoy funciona porque hay
> una persona en medio recordándolo. **En el proyecto siguiente, sin ella, se
> pierde** — por eso está escrito.

### LM.6 — Feature y vertical slice miden ejes distintos

Se confunden porque los dos dicen "algo completo". Pero completan cosas distintas:

| | Feature | Vertical slice |
|---|---|---|
| Unidad de… | **valor** (producto) | **trabajo** (construcción) |
| Responde | *qué* quiere el usuario | *cómo* lo construyes y entregas |
| Quién la nombra | el negocio / el usuario | quien construye |
| Vive en | la especificación | el plan, y cambia cada semana |
| Tamaño | el que necesite | lo más delgado posible |

Un slice atraviesa **todas las capas** —datos, backend, interfaz— y al terminarlo
**algo se puede usar**. La feature "buscar productos" son cuatro slices: búsqueda
exacta y fea → tolera errores de escritura → filtros → historial.

> **Una feature suele necesitar varios slices. Un slice casi nunca es más de una
> feature.** Cuando la feature es pequeña, el primer slice ya la completa — y ahí
> es donde los dos términos parecen sinónimos. La diferencia solo se ve en lo grande.

Y el contrario aclara el concepto: el corte **horizontal** —toda la base de datos,
luego todo el backend, luego toda la interfaz— deja cimientos. Nada que un usuario
pueda tocar, y ningún error descubierto hasta el final.

📌 Ejemplo trabajado: "login" **no es una feature, son dos**. *Autenticación*
(¿quién eres?) y *autorización* (¿qué puedes hacer?). Autenticación siempre va
primero: no se puede decidir qué puede hacer alguien sin saber quién es.

### LM.7 — Desplegar y publicar son dos cosas, y separarlas es la libertad

- **Deploy:** el código corre en producción.
- **Release:** los usuarios lo ven y lo usan.

Lo normal es que vayan juntos. **No tienen que ir juntos**, y ahí está el truco: el
slice 1 del login —un usuario metido a mano, sin registro— **se despliega** y se
deja **apagado** con un *feature flag*. Encender un interruptor es infinitamente
menos riesgoso que desplegar código.

La pregunta para publicar no es *"¿está completo?"* sino **"¿un usuario real que
toque esto sale bien parado?"**.

Y el argumento que suena al revés y no lo es: **desplegar seguido es lo seguro.**
Un deploy cada dos semanas lleva cincuenta cambios y, cuando algo revienta, no
sabes cuál fue. Un deploy por slice lleva uno. Y como se hace seguido, se vuelve
**aburrido** — el mejor adjetivo que puede tener un deploy.

> Corolario de seguridad: la contraseña se guarda **hasheada desde el slice 1**.
> Guardarla en texto plano no es una versión simple de la feature, es una versión
> **rota**. Un slice puede ser incompleto; no puede estar mal hecho. → LM.8.

### LM.8 — Walking skeleton, tracer bullet y prototipo no son lo mismo

Los tres atraviesan todas las capas. Se distinguen por **para qué se disparan**:

| | Prototipo | Walking skeleton | Tracer bullet |
|---|---|---|---|
| Pregunta | *¿lo quieren? ¿se entiende?* | *¿está conectada la tubería?* | *¿le apunto a lo correcto?* |
| Valida | **deseabilidad** | arquitectura, deploy | requisitos, dirección |
| Cuesta | horas, **puede que cero código** | poco código, cero lógica | código real |
| Si sale mal | **se mata el proyecto** | se corrige la arquitectura | se corrige el rumbo |
| El artefacto | **se bota** | **se queda** | **se queda** |
| Se le muestra a | **el usuario** | el equipo | **el usuario** |

> ✏️ **Corregido en la sesión 45.** Esta tabla nació poniendo el prototipo como
> *"código que se bota"* y como una duda **técnica** (*"¿esto es posible?"*). Las
> dos cosas estaban mal para su proceso, y su versión es **más fuerte**: el
> prototipo es **lo más barato que se pueda construir** para someterlo a usuarios
> —un wireframe, un HTML clicable— y **puede no ser código nunca**. Valida
> **deseabilidad**, no factibilidad. Mata un proyecto malo **antes de que exista
> una línea**: lo más reversible que hay (LM.2).

El nombre viene de la munición trazadora: lleva fósforo, deja rastro luminoso, y el
que dispara **ve dónde pega y corrige** en vez de calcular la trayectoria en papel.

**Cuántos de cada uno:**

- **Walking skeleton: uno por sistema desplegable.** No es por feature. Se hace una
  vez, antes de la primera feature. Única excepción: cuando aparece una tubería
  genuinamente nueva (una app móvil, una cola en segundo plano) se hace un
  mini-esqueleto de *ese* camino.
- **Tracer bullets: muchas.** Una por cada zona de incertidumbre.

> La frase que ordena todo: **el walking skeleton es una cosa que construyes; la
> tracer bullet es un papel que un slice desempeña.** No se elige entre los dos.
> "Tracer bullet" es un adjetivo: describe *por qué* haces ese slice.

El primer slice de cada feature normalmente **es** la tracer bullet de esa feature.
No se construye aparte. Y el filtro para saber si le toca serlo:

> *"¿Sé cómo debe funcionar esto, o me lo estoy imaginando?"* Si lo sé (login,
> CRUD), es solo el slice 1. Si me lo imagino, es tracer bullet — **y hay que ir a
> mostrárselo a alguien antes del slice 2.** Una bala trazadora que nadie mira caer
> es solo un slice; el rastro luminoso no sirve si no hay quien lo vea.

**Y no compiten: el prototipo muere antes de que nazca el esqueleto.** Nunca se
encuentran, y por eso no había conflicto con su método (paso 3):

```
brief → requisitos/BDD → 3 actores → PROTOTIPO (desechable)
   → métricas → usuarios → PUERTA ──┐
                                     │ si pasa
   walking skeleton ← definir MVP ←──┘
   → slices en diagonal (el primero de cada feature = tracer bullet)
```

⚠️ **El hueco que deja, y hay que saberlo:** un prototipo valida que **lo
quieren**, no que **se pueda construir**. Los usuarios dicen que sí con
entusiasmo a un dibujo de algo imposible, carísimo, o que necesita un dato que
nadie tiene — el wireframe no toca la base de datos, no llama a ninguna API y no
tarda nada porque no hace nada.

> Se pasa la puerta de *"lo quieren"* sin haber pasado la de *"se puede"*. Ahí
> entran el walking skeleton y las primeras tracer bullets: **no son redundantes
> con el prototipo, cubren el riesgo que el prototipo, por barato, no puede tocar.**

### LM.9 — El MVP se define primero; los slices se cortan apuntando a él

El error natural es pensar que el MVP **aparece** cuando ya llevas suficientes
slices acumulados. Al revés: sin MVP definido antes, no hay forma de saber cuándo
parar — siempre hay un slice más que se ve razonable, y así un proyecto de dos
meses se vuelve de dos años.

**Y la parte que casi todos hacen mal:** el MVP no es terminar la feature A, luego
la B, luego la C. Es **los primeros slices de varias features a la vez**.

| Enfoque | Resultado a las N semanas |
|---|---|
| ❌ Feature por feature | La autenticación más pulida del mundo protegiendo una app vacía |
| ✅ En diagonal | Incompleto en todo, pero **usable de punta a punta** |

Nadie usa un producto por el login. El login es peaje.

**Construir en diagonal**, concretamente, es el orden de recorrido de la cuadrícula
`features × slices`: bajas por la **columna 1** entera, luego por la columna 2.

| Feature | Slice 1 | Slice 2 | Slice 3 |
|---|---|---|---|
| Cuenta | 1️⃣ | 5️⃣ | 9️⃣ |
| Catálogo | 2️⃣ | 6️⃣ | 🔟 |
| Carrito | 3️⃣ | 7️⃣ | ⬜ |
| Pago | 4️⃣ | 8️⃣ | ⬜ |

Es cómo dibuja un retrato un artista: trazos suaves de **toda** la cara, y después
otra pasada con detalle. No un ojo perfecto primero — porque si luego la cara sale
torcida, hay que borrar el ojo perfecto.

**Los dos regalos:** los errores de *conexión* entre piezas aparecen en la semana 1
con 30 líneas encima, no en el mes 3 con mil; y al final de cada columna hay algo
**entero**, así que se puede parar en cualquier momento.

No es una diagonal perfecta, es una escalera irregular. La regla real:

> **Nunca refines una feature más allá de lo necesario mientras otra feature del
> MVP siga en cero.** Y al elegir el siguiente slice: *"¿esto hace la aplicación
> más **completa** o más **buena**?"* Antes del MVP, siempre "más completa".

📌 Después de publicar el MVP **el orden deja de decidirlo tu intuición y empieza a
decidirlo lo que ves**. Ese es el premio real de haber publicado temprano.

### LM.10 — Antes de escribir código, decide solo las puertas de una vía

La pregunta no es *"¿cuánta arquitectura por adelantado?"* sino **"¿cuáles
decisiones?"** — y eso sí tiene criterio, no intuición.

- **Puerta de dos vías:** entras, no te gusta, sales. Barato de deshacer.
- **Puerta de una vía:** deshacerlo cuesta meses.

> Es **LM.2 aplicada al diseño**: lo barato es lo reversible. Aquí decide *qué* se
> piensa en papel y qué se aplaza.

| Decide ahora (una vía) | Aplaza (dos vías) |
|---|---|
| Modelo de datos central y sus fronteras | Framework, librerías, ORM |
| ¿Multi-tenant? ¿cómo se aísla cada cliente? | Estructura de carpetas |
| Síncrono o asíncrono en el flujo principal | Dónde va el caché |
| Modelo de identidad y permisos | Forma de los endpoints, la UI entera |
| Lenguaje y runtime | Herramienta de pruebas, proveedor de correo |
| Un servicio o varios (**empieza con uno**) | |

Aplazar no es pereza: las decisiones tempranas se toman con la **menor** cantidad
de información que vas a tener en todo el proyecto. Si estás debatiendo una de dos
vías y no has escrito código, elige la aburrida y sigue.

**Y la pieza que conecta con LM.8:** un documento de arquitectura es una
**hipótesis** —un conjunto de suposiciones sobre cómo encajan las piezas— y una
hipótesis sin experimento no vale nada.

> **El walking skeleton es el experimento que pone a prueba el documento de
> arquitectura.** → L2.11 y L4.13: "encaja con lo que veo" ≠ "es correcto".

```
Requisitos + BDD → decisiones de una vía (1–2 págs) → WALKING SKELETON
     → CORRIGES las decisiones ← el paso que nadie hace
     → slices, en diagonal
```

El paso de corregir es lo que hace que esto sea evolutivo de verdad. **Si el
documento no cambia después del esqueleto, no lo estabas usando: lo estabas
obedeciendo.**

Por eso el formato recomendado es un **ADR** (*Architecture Decision Record*): una
decisión por archivo, media página, con contexto / decisión / **por qué** /
consecuencias, **fechada**. El "por qué" es lo que sobrevive — el código dice el
qué. Y se reversa sin vergüenza: `ADR-011 supersede ADR-003`, y el histórico queda.
Un documento de arquitectura grande, en cambio, nadie lo actualiza: se vuelve
mentira y todos lo saben.

⚠️ **"Arquitectura evolutiva" no significa "sin arquitectura, ya veremos".**
Significa diseñar para que cambiar sea barato, y eso cuesta trabajo desde el día
uno: **fronteras claras** (si todo toca todo, nada se puede cambiar), **pruebas**
(sin ellas no te atreves a tocar) y **deploy automático**. Sin esas tres,
"evolutivo" es una palabra bonita para *improvisado*.

### LM.11 — Los slices no van en la especificación: salen del BDD

La especificación define **las features** — el *destino*. Los slices son cómo
decides cortar y en qué orden — la *ruta*. Y cambian a ritmos distintos:

| Documento | Contiene | Cambia |
|---|---|---|
| Requisitos / Spec / BDD | features, comportamiento esperado | poco: si cambia el negocio |
| Plan / backlog | slices, orden, qué sigue | **cada semana** |
| ADRs | decisiones de una vía | cuando una se supera |

Meter los slices en la especificación la pudre: el orden cambia constantemente —y
**debe** cambiar, es lo que aprendiste de los usuarios— y el documento pronto dice
una cosa mientras el proyecto hace otra. Ahí nadie vuelve a confiar en él.

**El puente que faltaba:**

> **Un vertical slice es un subconjunto de escenarios BDD que se ponen en verde
> juntos.** Los slices no se inventan: se **cortan** agrupando escenarios.

```
Feature: Autenticación
  entro con credenciales correctas    → Slice 1
  rechazo credenciales incorrectas    → Slice 1
  me registro con un correo nuevo     → Slice 2
  rechazo un correo ya registrado     → Slice 2
  bloqueo tras 5 intentos fallidos    → Slice 6
```

Tres cosas gratis: el slice queda definido **sin ambigüedad** (no es "hacer el
login más o menos", es "estos dos escenarios pasan"); **verde = terminado**, se
acabó la discusión; y el **MVP se vuelve una lista de escenarios**, no una
sensación — marcas los indispensables y sabes exactamente dónde parar.

📌 El BDD alimenta **dos** cosas, y por eso es el documento que más trabajo hace:
el **plan** (los slices) y la **arquitectura** — cuando dos escenarios hablan de
cosas distintas y no comparten datos, ahí hay una **costura natural** del sistema.
Los escenarios no son solo pruebas: son un mapa de por dónde se parte la aplicación.

### LM.12 — En un producto de IA, el wireframe valida la idea, no el producto

Caso particular de `LM.8`, y es el que más le importa a este proyecto.

Dibujas la pantalla del agente. En la burbuja escribes la respuesta perfecta que
quieres que dé. Se lo muestras a un usuario y **le encanta** — claro que le
encanta: es la mejor respuesta posible, **la escribiste tú**.

El prototipo salió aprobado y no probó nada, porque en un producto de IA:

> **El riesgo no está en la interfaz. Está en si el modelo puede hacer esa tarea
> con calidad suficiente, a un costo tolerable, de forma repetible.**

Y las tres cosas están medidas en este curso, no supuestas:

| Riesgo real | Ya medido en |
|---|---|
| La misma entrada da salidas distintas | L1.6, L2.5, L3.14 |
| Un agente cuesta el doble, como mínimo | L3.10, L3.12, L4.20 |
| El defecto sale **1 de 3 veces**, y se mueve de sitio | L3.15, L4.23 |
| Se factura razonamiento que nadie ve | L4.26 |

Ninguna aparece en un HTML clicable. **El wireframe no espera, no falla y no
cobra.** El producto hace las tres.

📌 **Por eso un producto de IA necesita dos prototipos, no uno:**

1. **El de flujo** — wireframe o HTML clicable, desechable. Valida que se
   entienda y que lo quieran.
2. **El de calidad** — **20 casos reales pasados por el modelo a mano**, en la
   consola, sin construir nada. Se miran las respuestas y se decide si aguantan.
   Cuesta **dólares, no semanas**.

El segundo responde la pregunta que el primero no puede tocar. Y no es un
invento: es una **evaluación en su forma más barata** — el nivel 5 hecho a mano,
antes de que exista una aplicación donde meterla (→ L1.16: sin respuesta esperada
escrita **antes**, "funciona" es una opinión).

> Un wireframe aprobado en un producto de IA no significa *"construyámoslo"*.
> Significa *"ahora sí, midamos si el modelo puede"*.

---

### LM.13 — Un freno que no has visto morder es una nota, no un freno

Salió el 2026-08-06, al cerrar `T-057`: la cuenta de AWS abierta, con la **alarma
de facturación puesta antes de encender ninguna máquina**. El orden es el correcto
—el extintor colgado antes que la cocina— y aun así la alarma **no es lo que
parece**, por una razón que solo aparece cuando se miran dos datos juntos:

| dato | de dónde salió |
|---|---|
| la alarma avisa con **cualquier cargo distinto de cero** | decisión propia (`C-005`) |
| los datos de facturación llegan con **~24 h de retraso** | documentación de AWS |
| cruzar una de las 7 puertas evapora los créditos **"en el acto"** | `C-005`, verificado |

**Un aviso que llega un día tarde no puede frenar algo que ocurre al instante.**

> La alarma protege del **goteo** (una máquina encendida y olvidada). No protege
> del **acantilado** (cruzar al plan de pago). Contra el acantilado no hay aviso
> posible: cuando llega el correo, ya pasó ayer.

Contra el acantilado el único freno real es una **lista de lo que nunca se toca**,
escrita antes y leída antes de cada clic. Es papel, y es el único freno que actúa
a la velocidad del riesgo.

#### Y lo que de verdad hay que llevarse, que es más general

La alarma **nunca se ha visto saltar**. Está bien montada, probablemente. Nadie lo
sabe. Y es la misma regla con la que se construyó todo el nivel 5b:

> **Ninguna prueba se da por buena sin verla ponerse roja primero.**

Aquí no se puede: para ver saltar esa alarma hay que gastar dinero de verdad, y el
resultado tardaría un día en llegar. Cuando un control **no se puede poner en rojo
barato**, no se hace como si estuviera probado: **se escribe que no lo está.** Un
riesgo anotado se vigila; un riesgo que uno cree cubierto, no.

📌 **Hay una ventana que se cierra sola, y es gratis mientras dure.** Ahora mismo,
con cero máquinas encendidas, **el silencio de la alarma significa algo**: si suena
hoy, hay algo que no sabes. En cuanto haya una máquina arriba, el silencio deja de
distinguir *"no hay gasto"* de *"la alarma está mal montada"*.
→ **El único momento en que un detector se puede calibrar es cuando sabes con
certeza que no hay nada que detectar.** Ese momento no vuelve.

#### El caso hermano del mismo día (→ `GUIDE.md` §2.b)

La auditoría del historial de TEAPP buscaba llaves con el patrón `AKIA|ASIA` y
devolvía **21 avisos, los 21 falsos**: `ASIA` vive dentro de *"dem·asia·do"*. Al
probarlo en rojo a propósito se vio lo que nadie sospechaba: el patrón flojo
**además se le escapaba una llave de Anthropic entera**.

**Los dos casos son el mismo animal, y por eso van juntos:**

| | la alarma de AWS | el patrón `ASIA` |
|---|---|---|
| el fallo | nunca se vio en rojo | se vio en rojo 21 veces, todas mentira |
| el resultado | se confía sin motivo | se deja de mirar |
| lo que pasa el día malo | **nadie se entera** | **nadie se entera** |

> Un control que nunca habla y un control que habla de más terminan en el mismo
> sitio: **apagados**. Uno porque nadie lo comprobó; el otro porque todos
> aprendieron a ignorarlo — y nadie recuerda haberlo apagado.

Es el defecto del nivel 5b (`26 evals verdes con el contrato roto`) subido de
nivel: allí el control callaba de más sobre código. Aquí callan y gritan sobre
**dinero y llaves**, que no tienen `git revert`.

### LM.14 — Quien supervisa también entrega datos sin verificar

Es **la otra mitad de `LM.4`**, y sin ella el método se lee al revés. `LM.4` dice
que quien construye no puede ser su propio testigo. Faltaba decir lo incómodo:
**el testigo tampoco es infalible.**

Salió el 2026-08-06, cerrando `T-052` en TEAPP. La terminal que supervisa entregó
una lista de sitios que había que cubrir con tests, y escribió esto:

> *"`secure=cookie_secure()` aparece en dos sitios, `app/api.py:295` y
> `app/api.py:512` — registro y login."*

Los números de línea eran correctos. **Los nombres eran inventados.** Se dedujeron
de dos números sin abrir la función que los contenía. Los sitios reales eran
`_start_session` —un ayudante compartido por registro y login— y el
`delete_cookie` de `/logout`.

🚨 **Y el dato malo era peligroso en una dirección concreta.** Obedecido al pie de
la letra, habría producido tests para "registro y login" y **`/logout` se habría
quedado sin testigo** — que es justo el camino que se olvida, porque no se parece
al otro. La suposición cerrada habría quedado cerrada con la mitad medida.

**Lo cazó quien construye, mirando el código en vez de obedecer la lista.**

> El reparto de las dos terminales no funciona porque quien supervisa acierte.
> Funciona porque quien construye **comprueba lo que le llega en vez de
> obedecerlo.**

#### Lo que esto cambia en la forma de escribir el traspaso

La supervisora **no da órdenes: da cosas que mirar.** La diferencia no es de
cortesía, es de seguridad:

| forma | qué produce cuando el dato es falso |
|---|---|
| *"cubre las líneas 295 y 512"* | se cubren esas dos y nadie mira más |
| *"`cookie_secure()` aparece en más de un sitio — búscalos"* | se buscan, y aparecen los de verdad |

📌 Un traspaso escrito como orden **transmite el error con autoridad**. Escrito
como pregunta, obliga a comprobarlo — y el error se muere ahí.

🔑 Y encaja con `LM.5`: la supervisora vale por lo que **no** sabe. Precisamente
por eso sus datos concretos son los menos fiables de los dos lados, y sus
comprobaciones desde fuera (`pytest`, `git status`, `nslookup`) las más. **Lo que
corre, vale; lo que deduce, se verifica.**

> ✏️ **Matizado el 2026-08-06 (sesión 48), y con el ejemplo peor posible.** Este
> último párrafo se queda corto: *"lo que corre"* también miente si la
> herramienta no puede ver el fallo. `git status` está en esa lista, y **fue
> exactamente el instrumento que falló ese mismo día** — ver `LM.15`. La frase
> buena es: **lo que corre vale si la herramienta puede ver el fallo que
> descartas.**

---

### LM.15 — Un instrumento ciego no da un dato falso: da silencio

El 2026-08-06, cerrando `T-054` en TEAPP, la terminal que construye escribió un
archivo de tests nuevo y comprobó que no hubiera ensuciado los datos reales:

> *"Verifiqué con `git status` que `data/` quedó intacto."*

**`data/` está en el `.gitignore` de TEAPP, línea 18.** `git status` no la mira.
Habría dicho lo mismo si los tests hubieran escrito ahí.

La conclusión era **correcta** —se comprobó luego por las fechas de los archivos,
que sí ven esa carpeta— pero se supo **por suerte, no por la prueba citada.**

#### Por qué esto es peor que un instrumento equivocado

Es la distinción que hay que llevarse, y no es sutil:

| instrumento | qué produce | qué pasa después |
|---|---|---|
| **equivocado** | un dato **falso** | otro dato lo contradice y se investiga |
| **ciego** | **silencio** | el silencio se lee como confirmación, y nadie vuelve |

Un dato falso deja huella y choca con algo. **El silencio no choca con nada.** Se
parece demasiado a un "todo bien" como para que alguien lo mire dos veces.

🔗 Y no es nuevo: es `L-016` de TEAPP con otro disfraz. Allí, cinco de las siete
puertas de `[C-005]` eran ❓ **porque AWS no decía nada**, y la tentación era leer
ese silencio como un "no pasa nada". Se decidió tratarlas como si evaporaran los
créditos. **Mismo animal: allá un texto callado, aquí una herramienta callada.**

> Antes de citar una prueba, preguntar si el instrumento **puede ver** el fallo
> que se está descartando. Si no puede, no ha dicho que no. No ha dicho nada.

#### Lo que lo hace una lección de método y no una anécdota

Fue la **tercera** cara del mismo defecto en dos sesiones, y por eso quedó con
nombre en TEAPP (`L-020`):

| dónde | el verde decía | lo producía en realidad |
|---|---|---|
| `T-055` (sesión 47) | *"el suplantador no engaña a uvicorn"* | Windows poniendo `127.0.0.1` como origen |
| `T-054` (sesión 48) | *"el peso cabe en el tope"* | un techo de 16384 que no rige — el real es 16000 |
| `T-054` (sesión 48) | *"`data/` quedó intacto"* | una herramienta que no mira esa carpeta |

🚨 **Tres veces seguidas no es casualidad: es el modo de fallo característico de
este proyecto.** Un verde producido por algo distinto de lo que el verde afirma.
Y tiene una razón estructural — **nadie audita un verde.** El rojo pide
explicación y por eso se investiga; el verde se cobra y se pasa de página.

📌 Por eso el sabotaje (`L-019`) no es opcional aquí, y por eso hay que
saboteárselo **al escenario**, no solo al instrumento. Ese día los cuatro
sabotajes de quien construye atacaban el Caddyfile y el conversor —el
instrumento—; **ninguno atacaba el escenario que el test decía existir para
cazar** (que alguien suba `MAX_SENTENCE_LENGTH` sin subir el tope). Lo corrió la
supervisora y salió rojo, que era lo que había que ver.
→ **Un guardián al que solo se le sabotea el instrumento no ha demostrado morder
en su propia dirección.**

---

### LM.16 — Una salvedad correcta no arregla un titular falso

El 2026-08-06, analizando `T-071`, la terminal que construye escribió esto sobre
los cinco marcadores que había en `data/users/` de TEAPP:

> **3. La trampa no está armada: ya se disparó**
>
> […] *"No puedo demostrarlo del todo, porque `data/` no va a Git y no hay
> historial que consultar — te lo doy como sospecha fuerte, no como hecho
> medido."*

**La salvedad es impecable.** Nombra el límite, dice por qué existe, y clasifica
su propia afirmación. Es exactamente como hay que escribir una sospecha.

Y el titular, tres renglones más arriba, dice **"ya se disparó"** en indicativo,
como hecho cerrado. El párrafo se contradice a sí mismo.

#### Por qué gana el titular

Porque **el titular es lo que se recuerda**, lo que se copia a la lista de
tareas, y lo único que lee quien vuelva dentro de seis meses. La salvedad vive
tres renglones más abajo y muere con la sesión.

> Si el titular y la salvedad discrepan, el que se cambia es **el titular**.
> Una salvedad no rebaja una afirmación: la deja convivir con su contraria.

#### Y lo que había debajo, medido

La supervisora lo comprobó, porque **sí se podía comprobar**: huella `md5` y
fecha de los cinco archivos → suite entera (`328 passed`) → misma huella.
**Idéntica.** La suite de hoy no escribe ahí. Ninguno de esos nombres
(`otronombrelargo`, `probe-log`, `john`) aparece en el código de tests.

Estado real: **la trampa estaba armada y la suite no la disparaba.** Ni lo uno
ni lo otro — y la diferencia importa, porque "ya se disparó" habría mandado a
buscar un culpable dentro de pytest, que es donde no estaba.

🔗 Es `LM.15` por el otro lado. Allí el silencio de una herramienta ciega se leyó
como **confirmación**; aquí el mismo silencio —`data/` sin historial— se leyó
como **acusación**. **El silencio no sostiene ninguna de las dos.** Quedó como
`L-021` en TEAPP.

---

### LM.17 — Un `md5` no dice "todo igual": dice "los bytes, iguales"

Cerrando `T-071` el 2026-08-06 hubo que sabotear el portero nuevo para verlo
morder, y el sabotaje escribe en los datos de verdad. Se hizo bien: copia de
`data/` antes, `cp -r` de vuelta después, y verificación con huella de contenido
— **siete archivos, siete huellas idénticas.** Restauración correcta.

Y lo era: **ningún dato de la aplicación se perdió.**

Lo que se destruyó fue el **`mtime`**. Los siete archivos quedaron marcados con
el segundo de la copia, y con ellos se fue la prueba física del hallazgo del
día: que un marcador y su cuota llevaban **el mismo nanosegundo**, que era el
argumento de que las 14:48 fueron *una petición a `/practice`* y no alguien
editando archivos a mano.

Se cazó porque la supervisora había guardado las fechas al abrir la sesión, por
costumbre. **Por poco.**

#### La vuelta nueva sobre `LM.15`

Las tres caras anteriores eran instrumentos **ciegos a un cambio**: no veían
nada de lo que buscaban. Este vio **perfectamente** el cambio que le importaba
—¿se corrompió un byte?— y fue ciego a **una dimensión entera del objeto**.

| la pregunta | ¿la responde `md5`? |
|---|---|
| ¿se corrompió el contenido? | **sí, y bien** |
| ¿quedó todo como estaba? | **no puede** |

Son dos preguntas distintas y la respuesta de la primera se leyó como respuesta
de la segunda. **Un archivo es contenido y metadatos; la huella mira la mitad.**

> Antes de restaurar por copia, preguntarse **qué del original no viaja en los
> bytes**: fechas, permisos, dueño, enlaces, orden.

#### Las dos reglas que quedan

1. 🔑 **La prueba de un defecto no puede vivir en la carpeta que el defecto
   ensucia.** Se copia a un sitio versionado **antes** de tocar nada. En TEAPP
   fue `_persistence/` (`A-020`), porque `data/` no va a Git y no tiene vuelta
   atrás.
2. **Un punto ciego encontrado se hereda**: el portero de `T-071` compara
   contenido, así que tampoco ve fechas. Quedó escrito en los tres sitios donde
   alguien lo va a leer —el portero, el fixture y `D-036`— junto al otro punto
   ciego, el de vivir dentro de pytest.

⚠️ **Y estrenó `LM.15` el mismo día en que se escribió, dentro de la verificación
del portero construido contra ese defecto.** No es ironía: es la medida de lo
difícil que es. Quedó como `L-022` en TEAPP.

---

### LM.18 — El instrumento que mide puede ensuciar lo que mide

*(sesión 50, del cierre de `T-072`)*

Durante una sesión entera se buscó **un camino desconocido** que escribía en los
datos reales de las personas. Se habló de "un proceso", "algún script", incluso de
alguien firmándose su propia credencial. El culpable resultó ser **la báscula que
midió la tarea de la sesión anterior**, escrita con cuidado y ejecutada seis horas
antes.

**El mecanismo, y es de manual:** el aislamiento necesitaba **tres** desvíos y el
script se acordó de **uno**. Desvió el archivo de cuentas —con su comentario
*"medir no debe tocar los datos"*— y dejó los otros dos apuntando a los de verdad.

🔑 **Y por eso la contradicción que abrió la investigación apuntaba al sitio
equivocado:** la cuenta "no existía" precisamente **porque el archivo de cuentas
fue el único que sí se desvió**. La pista más llamativa era la sombra del arreglo
a medias, no la del defecto.

#### Las tres cosas que se llevan

1. **El instrumento de medida es código que corre en tu máquina y escribe.** Un
   test lo sabe y lo trata como tal; un script de medición se escribe "para ver un
   número" y nadie le pone frenos. **Corre con los mismos permisos y sin ninguna
   red debajo.**
2. **Un vigilante solo ve el patio donde vive.** El portero de `T-071` toma huella
   antes y después de cada test — y no vio nada, porque una báscula corre **fuera**
   de la suite. Es el mismo punto ciego que `no_network.py` con los subprocesos.
3. **El arreglo no es perseguir al culpable: es cerrar la puerta.** Mientras el
   aislamiento dependa de que alguien se acuerde de tres líneas, el olvido es
   cuestión de tiempo. → `D-037`: la raíz de los datos sale de una variable de
   entorno **sin valor por defecto**, y sin ella **la app no arranca**. Es
   *denegar por defecto* (nivel 4) aplicado a dónde se escribe.

⚠️ **Y un aviso sobre la comodidad:** se discutió si esa variable podía aceptar una
ruta **relativa**, para que el archivo de ejemplo trajera *"un valor que funciona"*.
No. **Un ejemplo que funciona sin editarlo es un valor por defecto con pasos
extra** — la alternativa que ya se había descartado, entrando por la puerta de
atrás. Una ruta relativa además se resuelve contra *algo*, y ese "algo" es el
directorio de trabajo: exactamente la variable que el arreglo existía para quitar.

📌 **Dónde estaba la prueba, que es lo que casi cuesta la investigación:** no en el
historial de comandos —ese archivo no se había tocado en siete horas, porque **lo
que corre un agente no se teclea**— sino en las **transcripciones de la sesión**.
Cerró en dos minutos con una cadena de relojes: escritura del script, ejecución, y
los archivos naciendo **un segundo después**.

🔗 Encadena con `LM.15` (un instrumento ciego da silencio) y `LM.17` (un `md5` dice
"los bytes, iguales"). Aquellas dos eran instrumentos que **no veían**; esta es un
instrumento que **hace daño**. Quedó como `L-023` en TEAPP.

---

### LM.19 — La lista de tareas pendientes no es la lista de trabajo disponible

**Sesión 51.** El día abrió con un veredicto razonado y honesto: *"revisé las
pendientes y **ninguna** se puede cerrar hoy sin la nube"*. Era cierto. Y el día
cerró con cinco artefactos y seis tests nuevos, sin encender una máquina.

No fue suerte ni terquedad. Fue que **el veredicto se había hecho sobre el
conjunto equivocado**.

| conjunto | qué es | ¿necesita la máquina? |
|---|---|---|
| **tareas** (`T-xxx`) | trozos de **producto** que faltan | casi siempre **sí** |
| **supuestos** (`A-xxx`) | trozos de **ignorancia** que quedan | casi siempre **no** |

Una tarea es algo que hay que **construir**; un supuesto es algo que hay que
**averiguar**. Construir el servidor exige el servidor. Averiguar si `16KB` son
16000 o 16384 exige un binario y diez minutos.

> **La lista de pendientes responde "qué falta por construir".
> Nunca respondió "qué falta por saber", y ahí es donde está la reserva.**

Ese día murieron `A-019` (16000, con el borde medido en 16001) y se encogió
`A-008`, y ninguna de las dos era una tarea. **La reserva de trabajo sin nube
estaba entera y nadie la había contado, porque vivía en otro archivo.**

⚠️ **Y el censo estaba mal contado además:** se dijo *"las once pendientes"* y
`grep -c` daba **17**. La conclusión se sostuvo igual, pero **"ninguna" es una
afirmación sobre un conjunto**, y una afirmación de exhaustividad sobre un
conjunto mal contado no es exhaustiva: es una corazonada con forma de censo.

🔑 **La regla práctica, y cuesta un `grep`:** antes de declarar un día bloqueado,
mirar **las dos** listas. Si el bloqueo es de máquina, los supuestos siguen
disponibles — y son justo los que, sin medir, acaban sosteniendo decisiones.

🔗 Encadena con `LM.13` (*un freno que no has visto morder es una nota*): un
supuesto sin medir es la misma criatura, un renglón que todos tratan como dato.
Aquí se añade **dónde encontrarlos el día que parezca que no hay nada que hacer.**

---

### LM.20 — Un archivo de memoria puede crecer hasta que corregirlo por dentro deja de servir

**Sesión 51, y salió de un error repetido.** Esta terminal recomendó una tarea
(`T-068`) que llevaba cinco sesiones cerrada. Al ir a arreglar las menciones
falsas aparecieron dos cosas incómodas:

1. **Eran dos, no cuatro.** Las otras dos decían *"se **lee** antes del primer
   clic"* — correctas. El error fue leer *"hacer"* donde decía *"releer"*.
2. 🚨 **Ese mismo error, con esa misma explicación, ya estaba corregido en el
   propio archivo**, sesiones atrás y cuatro mil líneas más abajo.

La corrección no estaba desactualizada. **Estaba bien escrita, era exacta, y no
llegó.** Es una categoría distinta del bicho de las copias que contradicen:

> **Una copia falsa te engaña. Una copia correcta que nadie alcanza te deja
> cometer el mismo error dos veces, y encima con la respuesta ya escrita dentro.**

`PROGRESO.md` pasó de 7.500 líneas. A ese tamaño el protocolo *"leerlo al empezar
cada sesión"* ya no se cumple de verdad: se leen la cabecera y la última entrada,
que es exactamente lo que se hizo — y por eso la corrección de la línea 874 no
existió para nadie.

⚠️ **Lo que NO es la solución:** borrar lo viejo. El valor del archivo es que
conserva cómo se llegó a cada cosa, y las lecciones fuertes salieron justo de
releer entradas antiguas.

✅ **Lo que sí:** que el archivo tenga **una zona viva** —estado, pendientes,
correcciones vigentes— separada del **diario**, que solo crece. Un diario registra
lo que era cierto ese día; el estado tiene que ser cierto **hoy**, y hoy no cabía
en un sitio donde había que bajar cuatro mil líneas para encontrarlo.

🔗 Es `LM.15` a escala de documento: no dio un dato falso, **dio silencio** — y el
silencio se leyó como *"aquí no hay nada corregido"*.

---

### LM.21 — Una predicción sellada envejece, y el sello no la protege de eso

**Sesión 52, y es el hallazgo del día.** La tabla de `A-018` se selló en `cfba50a`
antes del primer clic, justo para que nadie decidiera el veredicto **después** de
ver el número. Eso funcionó: el sello hizo exactamente su trabajo.

Pero la tercera fila no decía solo *"no concluyente"*. **Nombraba una causa:**

```
coste = $0.00  ->  las horas de IPv4 aplican: experimento no concluyente
```

Y esa causa quedó desmentida **por la propia terminal que construye**, la misma
mañana, comprobando en la página de AWS que las 750 horas gratis son para
direcciones *asociadas* — una IP ociosa cobra siempre. Cazó su error y no vio
que, al cazarlo, **acababa de matar una fila de la tabla sellada.**

> **Un sello protege de decidir tarde. No protege de que el mundo desmienta lo
> que sellaste.** Y una predicción sellada se lee con más autoridad que
> cualquier otro papel del proyecto — que es justo lo que la hace peligrosa
> cuando caduca.

🔑 **La regla que sale de aquí:** cuando llegue un dato nuevo, no basta con
auditar el dato. Hay que preguntar **qué papel viejo acaba de quedar falso**. La
sesión 51 cazó que el `0,00` *se disfrazaba* de la fila 3; nadie miró si la fila 3
**seguía siendo verdad**.

⚠️ **Y la enmienda no borra: anula a la vista y con fecha.** La original vive en
el commit sellado y alguien la leerá algún día. Si desaparece del archivo vivo,
esa copia vuelve a ser la única — con su causa muerta intacta. Es `LM.20` con el
signo cambiado.

📌 Solo se podía hacer **en la ventana de ese día**. Leído el dato, ya no habría
sido un criterio: habría sido una explicación buscada para el número que ya
estaba en pantalla.

---

### LM.22 — El riesgo de una puerta se mide por el tráfico, no por lo peligrosa que es

**Sesión 52.** `T-068` es la lista de *"esto NUNCA se toca"*: siete puertas que
pasan la cuenta al plan de pago sin confirmación y sin vuelta atrás. Las siete
comparten una propiedad — **hay que ir a buscarlas.** Nadie aterriza en Control
Tower sin desviarse. Contra puertas así, una lista funciona.

La octava apareció después: **"Actualizar plan"**, en la cabecera de Facturación
y costos. Y no es de la misma especie:

> Las siete son puertas en las que puedes entrar **por error**. La octava está
> en el camino que **ya te comprometiste a recorrer a diario** — el experimento
> de `A-018` obliga a abrir esa página todos los días para leer un campo.

**Meterla como renglón 8 le daba el mismo peso que a Control Tower, y no lo
tiene.** Salió de la lista y pasó al **protocolo de lectura**: *se lee UN campo,
no se toca la cabecera*. La defensa tiene que vivir donde está el tráfico.

🔗 **Y la cara incómoda de `T-068` entera** (`L-026` en TEAPP): es el único
control del proyecto **estructuralmente inverificable**. `LM.13` pide ver morder
el freno; aquí probarlo **es** el desastre. Eso no lo invalida, lo reclasifica:

> **No es un freno, es disciplina.** Y la diferencia importa: un freno no se
> degrada con la repetición, la disciplina sí. El desgaste ya tiene fecha de
> inicio — el día que abrir esa página se volvió rutina.

---

### LM.23 — Medido no es lo mismo que anotado

**Sesión 52, y lo marcó la terminal que construye, en el cierre.** Se comprobó si
el `.env` del contenedor llevaba una API key real. Se hizo bien: se pidió **la
longitud del valor, no el valor**, para no dejar la llave escrita en ningún sitio.
Resultado: vacía.

Y entonces vino la parte buena:

> *"La comprobación no dejó artefacto. Medimos que estaba vacía, pero eso vive en
> la conversación, no en el repo. Mañana no habrá forma de releerlo."*

**Nadie lo pidió. Se marcó como *sin resolver* en vez de darlo por registrado**,
que es lo cómodo y lo que nadie habría auditado.

🔑 **Una medición que no deja artefacto no existe para quien no estuvo delante.**
Y quien no estuvo delante incluye **a ti dentro de tres sesiones**. La
conversación se cierra; el repo se queda.

⚠️ **Lo importante es que esto NO es un fallo de la medición.** La medición fue
correcta, cuidadosa y con el hábito bueno. **El hueco está en el paso siguiente**,
que no se parece a trabajo y por eso se salta: escribir que se midió, qué dio, y
cómo se pidió.

🔗 Cierra el arco del día entero, que fue todo sobre la distancia entre lo escrito
y lo cierto:

| lección | el hueco |
|---|---|
| `LM.20` | escrito y cierto, pero **nadie lo alcanza** |
| `LM.21` | escrito, sellado, **y ya no es cierto** |
| `LM.15` | el instrumento ciego que **no escribe nada** y se lee como verde |
| **`LM.23`** | **cierto y medido, pero no escrito** |

📌 Y no todo hueco hay que taparlo: aquí se decidió **no** arreglarlo —el
contenedor es desechable y la llave entra en el paso 8—. La disciplina no era
registrarlo, era **no llamarlo registrado**.

---

### LM.24 — En un archivo que crece por enmiendas, lo más viejo se queda arriba

**Sesión 59.** La otra terminal propuso arrancar el día por `T-060b`. Estaba
**cerrada desde hacía dos días**. No fue un despiste: la tabla *"lo que sigue vivo
en esta entrada"* de `[A-014]`, en `assumptions.md:1207`, seguía nombrándola.

Esa tabla se escribió el **07**. `T-060b` se cerró el **08**. Y la entrada de
`[A-014]` **ha encogido tres veces** — cada encogimiento escrito, correctamente,
como un bloque nuevo **debajo**. La respuesta buena estaba treinta líneas más
abajo, en la misma entrada, diciendo con toda claridad cuál era la pata que
quedaba.

🔑 **El archivo crece hacia abajo y el ojo entra por arriba.** Un historial que
solo añade deja lo más rancio en el sitio de más autoridad: la primera pantalla.

⚠️ **Y esto NO es `LM.20`.** Conviene no confundirlas, porque el arreglo es
distinto:

| lección | qué pasa con lo cierto | por qué falla |
|---|---|---|
| `LM.20` | está escrito y **nadie llega** | el archivo es tan largo que la corrección se pierde |
| **`LM.24`** | está escrito, **y se llega antes a lo falso** | lo viejo ocupa el sitio que se lee primero |

En `LM.20` el remedio es que alguien alcance el texto bueno. Aquí no sirve:
**se leyó el archivo correcto, la entrada correcta, y aun así salió el dato
malo.** El remedio es otro — **cuando una entrada encoja, encoge la cabecera**,
no solo añadas el bloque nuevo. Si la tabla de arriba dice qué falta, es ella la
que hay que tachar.

📌 Y el olfato que lo caza es barato: **una tabla de "lo que falta" con fecha más
vieja que la última enmienda es sospechosa por construcción.**

🔗 Es el bicho de la sesión 33 —la misma cosa escrita en dos sitios diciendo
cosas contrarias— cuando los dos sitios **son el mismo archivo**. Y de la 54 y la
57 —*el resumen es peor que el documento*— cuando el "resumen" es simplemente lo
que está más arriba.

---

### LM.25 — «Lo abrí, luego lo sé» es una calma más difícil de romper que «no lo abrí»

**Sesión 59, y es mía.** Ayer la lección fue *no prescribas sobre un archivo que
no has leído* — había pedido comprobar algo que el código ya hacía. Hoy abrí el
archivo. Y me equivoqué igual.

Dije que un usuario inventado cuenta como intento fallido **por `api.py:482`**.
Había leído esa línea y su comentario, que lo dice con todas las letras. Lo que
no miré fue **qué rama toma un nombre bien formado**: no pasa por ahí. Llega a
`accounts.verify`, que **devuelve `False`** para quien no existe
(`accounts.py:280`), y el fallo se registra **doce líneas más abajo**.

La conclusión era correcta —cuenta igual, la cuenta de nadie corría riesgo— y
**la causa estaba una rama al lado**.

🔑 **Leer no es lo mismo que leer el camino que va a tomar tu caso.** Me paré en
la primera rama que confirmaba lo que ya creía, que es exactamente donde uno deja
de leer.

⚠️ **Y lo peligroso es la segunda calma.** Formulado por la terminal que
construye, y es mejor que mi versión:

> *«No lo abrí» se rompe fácil: basta con abrirlo. «Lo abrí, luego lo sé» ya
> viene con su propia prueba de diligencia encima, y esa no se cuestiona.*

🔗 Es el mecanismo de `LM.15` (*nadie audita un verde*) aplicado al acto de leer,
y el pariente exacto de `L-034` en TEAPP: **la cicatriz de haber auditado un
bloque avala también las líneas que se añaden después.** Haber leído un archivo
avala también las ramas que no leíste de él.

📌 El remedio no es leer más: es **preguntarle al archivo por tu caso concreto**
—*¿por dónde pasa `noexiste7`?*— en vez de por el mecanismo en general.

---

### LM.26 — Un resumen no comprime al azar: deriva hacia lo que no le pide nada al lector

**Sesión 60.** Es la cuarta vez en siete sesiones (54, 57, 58 y hoy) que el
resumen de la otra terminal dice algo peor que el documento que resume. Pero hoy
cambia en dos cosas, y las dos importan.

**La primera: no se quedó en el resumen hablado.** La frase entró **al archivo**,
en el campo `siguiente acción` de `progress.md` — el primero que se lee al abrir
la sesión siguiente — y llegó con **dos identificadores entre corchetes al lado**:

> *"no hace falta encenderla a mano, el apagado y encendido ya son automáticos
> (`[D-045]`/`[D-046]`)"*

`D-045` dice lo contrario, y lo dice a propósito: **apagado automático, encendido
manual, para que el olvido caiga del lado que no cobra.** Los corchetes no venían
de ninguna parte; **se le pegaron después, como armadura.**

**La segunda, y es el hallazgo: lo que se inventó no fue una frase cualquiera.**
Fue **la cómoda**. Nunca la incómoda. Nadie escribe *"y además te toca una cosa
más"* por descuido.

🔑 **La dirección del error es el diagnóstico.** Un resumen comprime, y la
compresión tiene signo: **una frase que no le pide nada al lector no ofrece
resistencia mientras se escribe.** Si lo fabricado siempre es lo que quita
trabajo, no es despiste — es un sesgo con signo predecible, y eso se puede
auditar: **relee tu propio resumen buscando solo las frases que liberan al
lector.**

📐 **Y hay una causa estructural, no solo un descuido.** Es de la terminal que
construye y es buena: el `session-closer` arranca en frío y reconstruye del
`git diff`, que es justo para lo que existe. Pero **un `diff` no puede decir si
una máquina está encendida.** El estado físico del mundo no se reconstruye de
ahí.

⚠️ **Y la parte incómoda es mía.** Yo lo cacé, pero **no leyendo su documento**:
lo cacé porque la frase chocaba con un mecanismo que ya tenía en la cabeza, y lo
tenía porque el protocolo de inicio me había puesto `D-045` delante tres horas
antes. **Si hubiera abierto el día por otro lado, la frase pasa.** Eso no es un
control: es una coincidencia que salió bien.

🔗 Es `LM.13` aplicado al propio hallazgo —*un freno que no has visto morder es
una nota*— y es la familia de `LM.20` y `LM.24` con el signo cambiado:

| | qué pasa con el texto |
|---|---|
| `LM.20` | lo cierto **está escrito** y nadie lo alcanza |
| `LM.24` | lo cierto está escrito, pero **se llega antes a lo viejo y falso** |
| **`LM.26`** | **lo falso no estaba escrito en ninguna parte: se fabricó al comprimir** |

📌 **Y el control obvio sería peor que no tener ninguno.** Un guardián que buscara
frases del tipo *"no hace falta"* enseñaría a esquivar **las palabras**, no la
afirmación — que es exactamente el bicho de la sesión 58 (*el control que acabó
dictando cómo se escribe el archivo que vigila*). Así que esto se queda como
**disciplina, y se anota como desprotegido.** Escribirlo aquí no lo arregla; lo
deja dicho.

---

### LM.27 — El párrafo no se relee; la tabla sí

**Sesión 63, y el título es la formulación suya.** Es `LM.16` —*una salvedad
correcta no arregla un titular falso*— con el mecanismo por fin explicado, y por
eso lleva un título distinto: **lo que se aprendió aquí no es el hecho, es el
porqué.**

Una entrada tituló **«`A-011` muere»** y tachó su fila. Dos párrafos más abajo, la
misma entrada tenía escrita la limitación que lo desmentía: la medición *"no dice
nada de la cola llena"*. Las dos cosas, en el mismo documento, escritas por la
misma mano el mismo día.

Nadie mintió. Y ahí está el problema.

🔑 **Escribir la limitación tranquiliza a quien la escribe.** Se siente que ya se
ha dicho — y con eso se acaba el impulso de volver atrás. Pero decirlo **no toca
el índice**, y el índice es donde vive la conclusión que alguien va a leer dentro
de tres semanas.

| | qué se lee | quién lo lee |
|---|---|---|
| el titular / la fila tachada | *"`A-011` está muerta"* | **todo el mundo, siempre** |
| la salvedad en el párrafo | *"salvo la cola llena"* | quien ya sospecha |

**Si la salvedad contradice al titular, manda la salvedad, y el titular se
reescribe — no se acompaña.**

✏️ **Así se arregló, el mismo día:** la suposición volvió a su archivo
**encogida** en vez de tachada, el rótulo pasó a nombrar lo que de verdad se
midió, los números se escribieron como *«la peor de diez»* en vez de como un
número limpio, y el aviso se metió **dentro del código que hace la medición** —
donde alguien lo leerá antes de repetir el error, no solo en la bitácora.

🔗 Y es pariente de `LM.24`: en los dos casos el texto verdadero existe, y
**pierde por dónde está colocado**.

---

### LM.28 — Un informe escrito justo después de una corrección se organiza alrededor de la corrección

**Sesión 63.** Un commit cerró una suposición, creó una decisión nueva y trajo
**el número que decidía si la tarea siguiente era segura**. No apareció en el
informe. Ni una línea.

Lo que sí apareció entero, con su tabla y su detalle: **la enmienda del error
cometido esa misma mañana.**

🔑 **La contrición ocupa el sitio del hallazgo.** No hay que inventar nada para
que pase: quien acaba de corregirse tiene la corrección delante, viva y con
forma de noticia, mientras el resultado —que no duele— se queda quieto en el
`git log`.

⚠️ **Y conviene ver la diferencia con `LM.26`, porque el remedio no es el mismo:**

| | qué le pasó al texto |
|---|---|
| `LM.26` | se **inventó** una frase, y la inventada fue **la cómoda** |
| **`LM.28`** | **no se inventó nada: se omitió** — y lo omitido fue **el resultado** |

Contra lo inventado sirve releer buscando frases que liberan al lector. Contra lo
omitido eso no sirve de nada: **lo que falta no se relee.** El único control que
funciona es de fuera — comparar el informe **contra el `git log` del día**, que
es lo que lo cazó.

📌 **Y el precio era medible, que es lo que lo vuelve una lección y no una
queja.** El dato que no llegó decía que el saldo daba para **140 días de una sola
persona a tope**, y con él llegaba **un segundo reloj que nadie tenía en el
calendario**: hasta ese día el proyecto solo vigilaba el vencimiento de los
créditos de la nube. El saldo del modelo se agota **antes**. Un informe puede
perder un número y con él una fecha límite entera.

---

### LM.29 — Una lista de pendientes escribe igual «lo que hay que resolver» y «lo que hay que construir»

**Sesión 64.** Una tarea pedía **decidir** cómo repartir las llaves. Se decidió,
se cerró, y con eso la tarea siguiente quedó marcada como **desbloqueada** — sin
que existiera ni una línea del freno que la decisión describía.

Nadie mintió, y esto importa: **la tarea decía *decidir*, y se decidió.** El
sistema funcionó exactamente como estaba escrito.

🔑 **Solo lo construido protege de algo.** Una decisión es una intención con
fecha; una pieza es algo que se puede ver morder. Cuando un desbloqueo cuelga de
una decisión en vez de una pieza, **el hueco se abre sin que nada se ponga
rojo** — porque no hay nada que pudiera ponerse rojo.

✏️ **El arreglo fue de una línea, y es el patrón que hay que copiar:** la
dependencia dejó de ser *"la partición está decidida"* y pasó a ser **"la capa 1
existe y se le ha visto morder"**.

🔗 Es `LM.19` (*la lista dice qué falta por construir, nunca dijo qué falta por
saber*) con el mecanismo explicado, y aquí sale **del revés**: la lista dijo lo
que faltaba por saber, y se leyó como construido. Y es `LM.13` metido en el
formato de la lista de tareas: *un freno que no has visto morder es una nota*, así
que **una tarea no puede cerrarse contra una nota.**

📌 La pregunta barata, al escribir cualquier pendiente: **¿qué se puede mirar el
día que esto esté hecho?** Si la respuesta es *"un párrafo"*, el pendiente está
mal cortado.

---

### LM.30 — La urgencia no se audita: se obedece

**Sesión 67, y es la más cara de las cinco.**

Una tarea llevaba **dos traspasos viajando como pendiente** estando cerrada
—cerrada de verdad, con su testigo en los registros de la máquina—. El segundo
día no llegó como un duplicado cualquiera: llegó **de prioridad número uno**, y
con una consecuencia pegada: *"la máquina encendida se está comiendo el plan
gratuito"*.

Ese daño no salía de ninguna corrida. Medirlo costó **dos comandos y catorce
segundos**: los dos puertos, mudos; y con la máquina apagada quien cobra son la
dirección fija y el disco, **no las horas de instancia**.

🔑 **Y aquí está la vuelta que le faltaba a esta familia de lecciones.**

| | qué se fabricó |
|---|---|
| `LM.20` | nada: **está escrito y nadie llega** |
| `LM.24` | nada: está escrito, pero **se llega antes a lo viejo** |
| `LM.26` | una frase, y fue **la cómoda** |
| **`LM.30`** | una frase, y fue **la alarmante** |

**Y la alarmante es peor.** *"No hace falta hacer nada"* invita a comprobar —
suena a demasiado bueno—. *"Llevas cuatro días perdiendo dinero"* **invita a
correr**, y correr es exactamente lo contrario de auditar. Una urgencia se salta
la fila entera: se convierte en la agenda del día antes de que a nadie se le
ocurra preguntarle de dónde sale.

📌 **El antídoto es barato y ya está probado:** antes de obedecer una urgencia,
**preguntar de qué corrida sale**. No *"¿es verdad?"* — eso invita a razonar y se
razona a favor de lo que asusta — sino *"¿qué comando lo midió y cuándo?"*.

⚠️ **Y el mecanismo de cómo revivió la tarea muerta es la mitad práctica de la
lección:** se había cazado el día anterior, pero **la caza vivió solo en el
chat**. El puntero viejo se quedó en el disco, y el arranque siguiente lo volvió
a servir intacto. Es `L-029` de TEAPP: **un hallazgo que no entra en un archivo
no ocurrió** — y aquí no solo se perdió, sino que **el error volvió con más
autoridad que la primera vez.**

---

### LM.31 — Cuando una medición diga «no aparece», comprueba primero que la medición ocurrió

**Sesión 69, y es mía — estuve a un paso de escribir el hallazgo falso.**

Medí un despliegue para comprobar que la página traía cierto marcador. No estaba.
Ya tenía la frase medio escrita: *"esto contradice tu afirmación 7"*.

No era verdad. La petición **había fallado al resolver el nombre** y había
devuelto **cuerpo vacío**; mi búsqueda leyó ese vacío como *"el marcador no
está"*. La corrida siguiente, en el mismo instante, respondió `200` con todo en
su sitio.

🔑 **El fallo intermitente de resolución no cuesta una petición: FABRICA
EVIDENCIA.** Y fabrica la peor clase — silenciosa, con forma de hallazgo, y
apuntando a un despliegue que está bien.

⚠️ **Lo que lo hace posible es el modo silencioso del propio instrumento.** Pedir
que no muestre el progreso también hace que no muestre el fracaso, y lo que sale
por el otro lado —**nada**— entra en el filtro siguiente **como si fuera una
respuesta**. El filtro no tiene manera de distinguir *"pregunté y no aparece"* de
*"no llegué a preguntar"*: los dos casos le llegan idénticos.

🔗 Es `LM.15` (*nadie audita un verde*) con **el vacío en el papel del verde**, y
es el hermano de `L-051` de TEAPP un anillo más afuera: allí la pantalla mentía
sobre un despliegue correcto; **aquí mentía mi propio instrumento de medida.**

📌 **La regla que sale, y sirve para cualquier medición:** cuando el resultado de
una medición sea **«no aparece»**, comprobar primero que **la medición ocurrió**.
Un negativo tiene que traer su propia prueba de vida — el código de respuesta, el
tamaño de lo recibido, algo. Un cero y un vacío se parecen demasiado.

---

### LM.32 — El sitio con más probabilidad de esconder el error siguiente es la corrección que acabas de hacer

**Sesión 71**, y sale de cuatro rondas de auditoría sobre **una sola decisión**,
en un día. La cadena, en orden:

| ronda | qué se encontró |
|---|---|
| 1ª | un **techo que no existía** — se cayó una decisión entera |
| 2ª | el arreglo del techo metió una **regresión viva**, cobrando, dos horas en producción |
| 3ª | el arreglo de la regresión traía una **justificación que caducaba** |
| 4ª | la justificación buena se quedó **sin guardián** |

🔑 **Ninguna de las cuatro se habría visto sin la anterior.** Cada hallazgo vivía
dentro del remedio del hallazgo previo. Eso no es mala suerte ni gente
despistada: es dónde estaba mirando todo el mundo.

**Por qué pasa, que es lo que hay que llevarse.** Una corrección se escribe en
las peores condiciones posibles para escribir algo con cuidado:

- **con prisa**, porque acaba de aparecer un error y molesta;
- **con alivio**, porque se está arreglando — y el alivio no audita;
- **con el foco puesto en el defecto viejo**, no en lo que se está introduciendo;
- y **con una cicatriz que la avala**: *"esto lo acabamos de revisar"*.

📌 **La cuarta es la peor y ya tenía nombre.** Es `LM.15` (*nadie audita un
verde*) y `L-034` de TEAPP (*la cicatriz de haber sido auditado avala también las
líneas que se añaden después*). Aquí sale su forma más pura: **el código recién
corregido es el único del repositorio que nadie va a volver a mirar**, porque
todos acaban de mirarlo.

⚠️ **Y no es un argumento para revisar más.** Revisar más es lo que ya se estaba
haciendo. Es un argumento sobre **dónde apuntar**: cuando alguien arregle algo
que tú señalaste, **el arreglo entra en la cola de auditoría, no sale de ella.**
Un error corregido no baja la probabilidad de error en esas líneas: la sube.

🔗 Emparenta con `LM.28` (*la contrición ocupa el sitio del hallazgo*) — allí el
informe se organizaba alrededor de la corrección, aquí es el **código**.

---

### LM.33 — Un dato raro que se comprueba y no se manda es trabajo, no silencio

**Sesión 71, y esta la acreditó la otra terminal, que es lo que la hace valer.**

Auditando su repo vi que la suite tardaba **39 s** donde por la mañana tardaba
**17**. Tenía todo el aspecto de una regresión de rendimiento y de un hallazgo
número seis. La corrí dos veces más: **39 / 36 / 27**. Era ruido de mi máquina.
No lo mandé — o mejor dicho, mandé una línea diciendo que lo había comprobado y
que no lo mandaba.

Ellos lo devolvieron así: *"nos habría puesto a buscar una regresión inexistente
medio día"*.

🔑 **La cuenta es asimétrica y por eso importa.** Comprobarlo me costó dos
minutos. Mandarlo sin comprobar les habría costado medio día — **a ellos**, y
además con la mejor voluntad, porque un aviso de quien audita se atiende.

⚠️ **Y ahí está el enganche con `LM.30`:** *la urgencia no se audita, se
obedece.* Si eso es cierto —y está medido—, entonces **quien emite la alarma es
el único filtro que existe**. El destinatario no va a hacer de segundo control:
va a correr. Un falso positivo enviado no es «una pista más para que decidan
ellos»; es una orden.

📌 **Por eso el filtro es parte del trabajo de auditar, no un paso previo a
auditar.** La mitad del oficio es lo que se manda; la otra mitad es lo que se
descarta después de mirarlo. Y la segunda mitad **no deja rastro**, así que no se
acredita nunca — salvo que alguien, como pasó hoy, se moleste en decirlo.

🔗 Es `LM.31` con el signo cambiado. Allí: *cuando la medición diga «no aparece»,
comprueba que ocurrió.* Aquí: **cuando la medición diga «algo cambió», compruébalo
antes de que lo cambie otro.**

---

### LM.34 — Una función que nadie prueba es un párrafo con paréntesis

**Sesión 72, y la frase es de la otra terminal.**

El criterio de aceptación de `T-093` se escribió como **función** (`verdict_for`)
y no como párrafo en `decisions.md`. La razón que dieron era buena: *un criterio
que hay que ir a buscar a un documento se reinterpreta; uno que imprime el guion,
no.*

✅ **Y funcionó**: esa decisión es lo que permitió auditarlo desde fuera con tres
comandos de una línea y **cero dólares**, antes de gastar nada.

```
python -c "import measure_tutor as m; print(m.verdict_for(1,0,60))"
  → "1.7%, por encima del 5% acordado"      ← afirma algo falso
python -c "import measure_tutor as m; print(m.verdict_for(0,0,45))"
  → "por debajo de 6.7%, que es el 5% acordado"  ← se contradice sola
```

🔑 **Pero la función no tenía ni un test.** Los dos defectos de arriba llevaban un
día ahí. Estaban a un comando de distancia de cualquiera y **nadie había dado ese
comando**, porque escribir algo como código se siente como haberlo verificado.

⚠️ **Ese es el engaño exacto:** la forma ejecutable promete comprobación y no la
entrega. Un párrafo al menos se lee como lo que es —una afirmación de alguien—.
Una función parece que ya pasó por algún control, y **la sintaxis no es un
control**: lo único que garantiza es que el intérprete no protestó.

📌 **La corrección no es «volver al párrafo», es cerrar el circuito.** Añadieron
12 tests, y **tres de ellos son exactamente los tres defectos**. La ventaja de
escribirlo como función solo se cobra cuando alguien la llama.

🔗 Es `LM.13` de TEAPP (*un freno que no has visto morder es una nota, no un
freno*) aplicado al criterio en vez de al freno. Y engancha con `LM.15`: la
función en verde no daba un dato falso, **daba silencio**.

---

### LM.35 — Una corroboración inventada es peor que ninguna, porque desactiva la revisión

**Sesión 72, y esta también la escribió la otra terminal — sobre sí misma**, que
es lo que la hace valer.

Al corregir un umbral, justificaron el número con **dos caminos que supuestamente
no se hablaban entre sí**: *«mirando el cliente da 9,0; mirando la ruta,
10,0 − 1,0 = 9,0. Cuando dos caminos independientes dan lo mismo, no queda
decisión que tomar.»*

Ninguno de los dos era lo que decía ser:

| camino | lo que parecía | lo que era |
|---|---|---|
| cliente | una resta | **una tautología** — «el máximo si le doy todo a `read`» *es* el presupuesto del cliente |
| ruta | una resta independiente | solo daba 9,0 tomando el `1,0` como `ruta − cliente`, **que era la conclusión** |

🔑 **Y el segundo ni siquiera aterrizaba ahí.** Hecho con los componentes que su
propia tabla declaraba —`0,07` de trabajo local + `0,50` de margen— daba
`10,0 − 0,57 = 9,43`, no 9,0. El `0,43` que faltaba no era una reserva: era la
holgura que sobró de una elección anterior.

⚠️ **El número era correcto.** Lo único falso era el argumento *de más*. Y por eso
es peor que no haber puesto ninguno:

📌 **Un argumento falso de más no suma un error: resta un revisor.** El que llega
después ve dos caminos coincidiendo, concluye que eso ya está triangulado, y
**deja de mirar**. Una afirmación sola invita a comprobarla; dos que se confirman
entre sí invitan a seguir de largo.

⚖️ **La forma de detectarlo, y es barata:** cuando dos derivaciones den el mismo
número, comprobar que **ninguna usa como insumo lo que la otra produce**. Si el
segundo camino resta una cantidad que se calculó restando el resultado, no es
corroboración: es el mismo dato con otro sombrero.

🔗 Es el remate de `LM.32`. El defecto vivía dentro de la corrección del día
anterior, y **la corroboración inventada es justo el mecanismo** por el que una
corrección se blinda contra la siguiente mirada.

---

### LM.36 — Identificar el término dominante y luego tratarlo como constante

**Sesión 73.** `[L-043]` de TEAPP escribió, con razón, que la entrada de cada
llamada al tutor apenas se movía (245–250 tokens) **porque la rúbrica pesa casi
todo y la frase del alumno casi nada**. Y de ahí sacó la conclusión: *"o sea el
coste por práctica es casi fijo"*.

Tres días después alguien le añadió siete líneas a la rúbrica —el bloque `OK`/`FIX`
que hacía falta para contar aciertos— y el coste por llamada subió un **30%**. La
constante de precio siguió donde estaba.

🔑 **El razonamiento acertó la mitad y se equivocó justo en el paso siguiente.** El
término dominante estaba bien identificado. Lo que no se siguió es que **dominar y
ser estable son cosas distintas**:

> Que la rúbrica domine el coste es exactamente lo que vuelve el coste **sensible**
> a editar la rúbrica.

Si el sumando grande fuera el que no puedes tocar, la conclusión sería correcta.
Aquí el sumando grande era **el único que se edita a mano**, y encima sin pensar en
el precio: se tocó para arreglar otra cosa.

📌 **La pregunta que faltaba, y es de una línea:** *¿quién puede mover el término
que manda, y con qué frecuencia?* Un término dominante que nadie controla estabiliza
el resultado. Un término dominante que se edita en cada iteración lo vuelve volátil,
y peor: lo vuelve volátil **por motivos que no tienen nada que ver con el número**.

⚠️ **Y el daño no fue el 30%.** Fue que la siguiente tarea llevaba escrita una
conclusión pre-comprometida —*"si no cuadra, revisa `[A-010]`"*— que apuntaba al
archivo equivocado. Una constante caducada no falla sola: **arrastra el diagnóstico
del siguiente que la use.**

🔗 Emparenta con `LM.23` (*medido no es lo mismo que anotado*): aquí el número
estaba medido y anotado, y aun así era falso, porque **lo que se midió dejó de
existir** y nadie lo notó.

---

### LM.37 — La cercanía no protege: estar al lado no obliga a nadie a hacer la resta

**Sesión 73, y la formulación es suya.** El precio caducado de `LM.36` no se cazó
cruzando dos archivos. Estaba **dentro de una sola entrada de `decisions.md`**:

```
línea 110 → "~361 y ~49 tokens por llamada"      (la corrida nueva)
línea 161 → "comparar contra 60 × $0,00234"      (precio medido con 247)
```

Mismo autor. Mismo minuto de escritura. Cincuenta líneas de distancia. Y la entrada
se contradecía a sí misma sin que nadie lo viera — incluido quien la escribió, e
incluido el auditor, que llegó a lo mismo por el camino largo.

🔑 **Esto desmonta un supuesto que llevábamos usando sin examinar.** Escribimos las
decisiones juntas, en una entrada, **para que quien lea una lea la otra**. Ese es el
antídoto que veníamos aplicando contra el bicho de la sesión 33 (la misma cosa en
dos sitios diciendo cosas contrarias). Pues no basta:

> **La cercanía pone los datos al alcance. No fuerza la operación entre ellos.**

Leer dos números en la misma página no es compararlos. Hace falta que alguien
decida dividir uno por el otro, y **nada en el formato lo pedía**.

📌 **Lo único que habría mordido aquí es aritmético, no de proximidad.** El `$0,1404`
era **un producto ya resuelto**. Un número calculado a mano y pegado en la prosa no
se recalcula al releerlo — se lee como un hecho. Una **expresión visible** delata sus
insumos:

```
mal:   "comparar contra $0,1404"
bien:  "comparar contra 60 × COST_PER_CALL_USD"
```

La segunda forma no puede envejecer en silencio: quien la lea ve de qué depende, y
si la dependencia cambió, el texto ya no dice lo mismo.

⚖️ **Y la ironía que la hace memorable:** `measure_tutor.py` **ya sabía hacer esto**.
`MAX_CALLS_PER_RUN` es una división, no un `106` escrito a mano. `TARGET_SAMPLES` es
una división, no un `60`. El archivo llevaba dos sesiones defendiendo ese método —
con el comentario explicando por qué un literal se queda quieto cuando cambia su
insumo. **La prosa de `decisions.md` no lo heredó.**

🔗 Es `LM.24` desde el otro lado. Allí el problema era que lo viejo se queda arriba y
se alcanza primero. Aquí lo viejo y lo nuevo están **a la misma altura**, los dos
visibles, y el defecto sobrevive igual. → `[L-059]` en TEAPP.

### LM.38 — Sella la predicción sobre la medida más cruda que tengas

**Sesión 74, y el error fue de esta terminal.** Se selló una banda de coste
(`$0,18–$0,19`) contra la barra de la consola. Salió `$0,18`, dentro de la banda —
y **la lectura valía menos de lo que parecía**, cosa que cazaron ellos:

> El coste **no es una medida: es una cuenta.** `tokens × tarifa`, y encima
> redondeada al céntimo para mostrarla.

`$0,18` no dice `$0,18`: dice que el número vive en **`[0,175 – 0,185)`**. Las dos
predicciones del día —la banda de aquí y su derivación de `$0,183`— **cabían dentro
del mismo redondeo**. El instrumento no tenía la finura que el método pedía.

🔑 **Y lo que lo vuelve un error y no mala suerte:** los tokens **ya estaban
leídos** y ya habían salido exactos (`21.668/2.959`, consola y `T-093`, idénticos).
Había un instrumento **sin pérdida, aguas arriba**, en la mano — y la predicción se
selló sobre el derivado y redondeado que está aguas abajo.

| | `LM.15` | `LM.38` |
|---|---|---|
| El instrumento | **ciego**: devuelve silencio | **de baja resolución**, y derivado de otro que no lo es |
| Cómo engaña | el silencio se lee como confirmación | el número se lee con más cifras de las que tiene |

📌 **Y el matiz que hay que decir para no pasarse de frenada:** de ahí **no** se
sigue que la lectura no midiera nada. Excluyó las ramas B/C/D y mató el 60%
superior de la propia banda (`0,185–0,19` habría salido `$0,19`). **Un resultado
nulo *para discriminar dos hipótesis* no es un resultado nulo.** Importa decirlo
porque *"el instrumento no tenía finura"* se desliza solo hacia *"no aprendimos
nada"*.

### LM.39 — Un verde que no cruza el diff no es evidencia sobre el diff

**Sesión 74.** Reportaron *"arreglado y comprobado: `bash -n` → sintaxis OK"*. Los
dos cambios eran **comentarios y cadenas dentro de un `echo`**. Pasar era casi
seguro, y no tocaba lo único que de verdad había cambiado: **si la instrucción
nueva funciona.**

> El instrumento era real, corrió de verdad y salió verde. **Y era ortogonal a lo
> que se estaba afirmando.**

**La pregunta que lo caza, y es una sola:** ¿este comando *podía* haber salido rojo
por culpa de este cambio? Si la respuesta es no, el verde no es evidencia — es
ruido con aspecto de prueba.

🔗 **Tercera cara del mismo bicho en un solo día:** la barra redondeada no
distinguía dos predicciones (`LM.38`), y `bash -n` no distingue una instrucción
buena de una que no arranca. **Instrumentos reales, que pasan, y ajenos a la
afirmación.** Es la familia de `LM.15` y `LM.31`: comprobar que la medición *ocurrió*
no es comprobar que midiera *esto*.

📌 En la capa de código esto tiene nombre y ya estaba escrito: es `GUIDE.md` §8.l
—*una prueba que pasa sin el arreglo no prueba el arreglo*— visto desde el otro
lado. Aquí la prueba pasa **con** el arreglo y tampoco prueba nada.

### LM.40 — Una tarea aplazada espera; una tarea armada tiene disparador

**Sesión 75, y el enunciado bueno es suyo.** `T-088` estaba escrita como *"corregir
un comentario"* y aplazada al paso 9. Al mirarla, el comentario decía *"da igual
cuál sea el modelo"* — **y el paso 9 es, literalmente, bajar a Haiku.**

Peor de lo que decía su ficha: el límite de la API es **por modelo**, así que la
firma del laboratorio no era el número 50 sino **el par (espacio, modelo)**. Con
Haiku, `requests_limit == 50` sale falso, `main()` imprime *"no es la del
laboratorio"* y devuelve `EXIT_OK`. **El portero acepta justo la llave que existía
para rechazar, y sin dar error.** Denegar por defecto (`GUIDE.md` §4.c) convertido
en aceptar por accidente.

> **Aplazar una tarea que espera es gestión. Aplazar una tarea armada es dejar un
> disparador sin dueño.**

| | `T-081` | `T-088` |
|---|---|---|
| Estado | **aplazada** | **armada** |
| Por qué | su daño ya está escrito en la ficha, y nada del paso 9 la activa | el paso 9 **era** su disparador |

⭐ **Y el añadido de ellos es mejor que el enunciado:** una lista de pendientes
**las iguala a todas por su aspecto** —tres renglones, tres 🔲— y **el formato borra
la distinción que importa.** Es `LM.19` con otra cara: la lista dice qué falta por
construir, nunca dijo cuál de esas cosas tiene una mecha encendida. Se desarmó con
**dos comentarios y cero lógica**.

### LM.41 — Donde un archivo avisa de una puerta, pregunta por la de al lado

**Sesión 75. Dos de dos en el mismo día, y de la misma forma.** `T-089` estaba
escrita como cosmética y era clase de seguridad; `T-088` estaba escrita como
*"corregir un comentario"* y era denegar-por-defecto roto (`LM.40`).

En los dos casos, **el archivo llevaba un aviso CORRECTO sobre una puerta a pocas
líneas de una línea que negaba la otra** — `install.sh` y `check_api_key.py`,
distinto archivo, mismo defecto.

> **Un aviso presente baja la guardia sobre el hueco de al lado.** Donde alguien se
> molestó en advertir de una puerta, pregunta si existe una segunda que ese aviso
> no cubre.

🔑 **El mecanismo es de lectura, no de código:** un aviso escrito señala que **ahí
hubo alguien pensando**, y eso se lee —sin decidirlo— como *"esta zona ya está
revisada"*. Es la misma familia de `LM.37` (la cercanía no protege) y de `LM.25`
(*«lo abrí, luego lo sé»*): la señal de diligencia sustituye a la diligencia.

📌 Y el efecto sobre una decisión: `[D-080]` había elegido su opción con **un**
dato y lo dijo honradamente. Con el segundo caso, la misma decisión tiene **dos**,
y eso sí se puede escribir.

### LM.42 — Un test escrito después del código no lo examina: lo retrata

Salió de una conversación de la sesión 76, sin código: *"en la otra terminal el
mismo Claude escribe el código y escribe los tests, ¿eso está bien?"*

`LM.4` dice que quien construye no puede ser su propio testigo, y de ahí salieron
las dos terminales. Esto es la misma bestia **un piso más abajo**, dentro de la
sesión que construye:

> Un test escrito después del código se escribe **mirando el código**. No
> comprueba lo que el programa debía hacer: comprueba lo que el programa hace.

Si el código entendió mal el requisito, el test hereda el mismo malentendido y
**sale verde confirmando el error**. Los dos artefactos están de acuerdo, y estar
de acuerdo consigo mismo es justo lo que `LM.4` dice que no vale.

⚠️ **Y el sabotaje (`GUIDE.md` §8.l) no caza esto.** Rompes la línea, el test se
pone rojo, todo parece sano. Pero el sabotaje demuestra que el test *vigila esa
línea* — nunca que esa línea sea la correcta. Es `L6b.9` otra vez: un verde dice
una de dos cosas y no sabes cuál.

**El discriminador, y cabe en una pregunta:**

| ¿El test se podía escribir **sin haber visto** el código? | |
|---|---|
| Sí | es una prueba |
| No | es un espejo |

Por eso el orden importa más que la autoría. **No es un problema que el agente
escriba el test: es un problema que lo escriba segundo.** El rojo primero no es
ceremonia de TDD — es lo único que garantiza que el test no nació copiando la
respuesta.

📌 Y de ahí el paso previo: el criterio en prosa lo escribe el humano **antes**, y
el test se deriva de esa frase. Es lo mismo que `GUIDE.md` §11.b ya exige para la
rúbrica —*una rúbrica escrita después de ver las respuestas es la que el agente ya
aprueba*— aplicado a la capa determinista, que era donde faltaba.

### LM.43 — Ante un test rojo hay dos salidas, y la barata borra la prueba

Un test se pone rojo. Hay dos formas de volver al verde: arreglar el código, o
ablandar el test. **La segunda es más corta, más rápida y siempre funciona.**

Y un agente al que se le dijo *"haz que los tests pasen"* no está eligiendo mal:
está cumpliendo exactamente lo que se le pidió. El defecto está en la orden.

> 🚨 **Pedir "que pase" pone el objetivo en el instrumento. El objetivo era el
> comportamiento.**

Es la misma forma de `L5b.23`/`L6b.19` —*cuando una buena respuesta reprueba, el
sospechoso es el examen*— pero **invertida y peligrosa**: allí sospechar del
examen era correcto, porque el examen lo escribió alguien con criterio y podía
estar mal. Aquí el examen y el examinado los escribió el mismo. Sospechar del test
es la salida cómoda, y `LM.26` ya dijo hacia dónde deriva un texto que nadie
frena: hacia la versión que no le pide nada a nadie.

**Lo que hace esto grave y no solo feo:** el test es el **único registro escrito
del criterio**. Un comentario se ignora, una decisión conversada se pierde — el
caso rojo es lo que pregunta *"¿seguro?"* (`GUIDE.md` §8.l, regla 6). Ablandar el
test no debilita una comprobación: **borra la decisión**, y no deja rastro en
ninguna parte salvo en el diff.

**Las dos consecuencias operativas:**

1. La regla se escribe en el `CLAUDE.md` del proyecto: *ante un rojo se arregla el
   código; modificar o borrar un test exige autorización explícita, con la razón
   escrita.*
2. **El diff de los tests se mira aparte del diff del código.** Es barato, es
   local, y es lo único que hace visible el cambio que nadie iba a anunciar.

### LM.44 — El verde es donde el agente se detiene, y el refactor vive un paso después

`GUIDE.md` §11.f ya escribe el ciclo entero —`ROJO → CONSTRUIR → VERDE →
REFACTOR`—, pero lo escribió pensando en una persona corriéndolo. Con un agente
tecleando, el cuarto paso se cae, y se cae **por una razón estructural, no por
descuido**:

| Paso | ¿Tiene condición de parada verificable? |
|---|---|
| rojo | sí — el test falla |
| verde | sí — el test pasa |
| **refactor** | **no** — "está limpio" no lo dice ningún comando |

> **Un agente se detiene en la última condición que puede comprobar. "Los tests
> pasan" es comprobable; "el código quedó bien" no.**

Y el código se queda con la forma del primer intento, que por definición era el
mínimo para pasar. Diez ciclos así y tienes una aplicación con todos los tests en
verde que nadie puede leer — sin un solo momento en que algo se viera mal.

⭐ **La salida es darle al refactor una salida observable**, que es lo que le
faltaba. En un refactor de verdad:

- el diff **toca código** y **no toca tests**;
- los tests siguen verdes **sin haber sido modificados**;
- por fuera el programa hace exactamente lo mismo.

Las tres se miran en el diff, gratis y sin correr nada. Si el paso de refactor
tocó tests, no fue un refactor: fue `LM.43` con otro nombre.

📌 Y el borde que hay que saber decir: si aparece comportamiento nuevo, eso **no
es refactor** — es un ciclo nuevo, y empieza otra vez en rojo. Es la misma
disciplina de `GUIDE.md` §11.f, punto 3: **una sola cosa por vuelta**, porque si
cambias dos, lo que se movió no dice por qué.

### LM.45 — Al final de una sesión no se ordena por importancia: se ordena por perecibilidad

**Sesión 75, ronda 4.** Quedaban dos cosas y no cabían las dos con holgura:
escribir el cierre del paso 8, o arreglar el guion de arranque que llevaba tres
sesiones sirviendo datos muertos.

**El guion era lo más importante de los dos. Y aun así iba segundo.**

| | El cierre del paso 8 | El bug del guion |
|---|---|---|
| Importancia | menor | **mayor** |
| De qué está hecho | **cuatro juicios de hoy que solo viven en la conversación** | una línea de código, estable |
| Dentro de veinte minutos | **se ha perdido** | está igual |
| Si se aplaza | hay que rehacer el razonamiento | se retoma donde quedó |

> **Lo importante espera. Lo perecedero, no.** Y al final de una sesión lo
> perecedero es siempre lo mismo: **lo que todavía no está escrito en ninguna
> parte.**

🔑 **Lo que se pudre no es la tarea: es el estado mental que la sostiene.** Un bug
en un archivo es materia; cuatro juicios tomados esta mañana son memoria de
trabajo, y esa se apaga con la sesión. Es `L-029` en el eje del tiempo — un
hallazgo entregado tarde nace huérfano — y `LM.23` en el del registro: **medido no
es lo mismo que anotado.**

⚠️ **Y hay un segundo motivo, que es el que convierte el criterio en regla:** el
arreglo del guion era de los que **se ensanchan solos** — protocolo de arranque,
quizá `CLAUDE.md`, quizá un test. Empezar por ahí con poco tiempo por delante es
**exactamente** cómo la sesión 54 se quedó sin llegar al clic (`[D-041]`): las dos
sesiones del día se acabaron antes del paso que importaba. Una tarea de contorno
incierto, puesta al final, **se come lo que quede**.

⭐ **El desenlace tiene la parte que más vale, y es de forma:** cierre primero,
guion después el mismo día, **y número a la tarea del guion ANTES de hacer
ninguna de las dos.** Sin el número, el guion depende de que alguien se acuerde —
que es `LM.40` aplicándose a sí misma: una tarea con disparador y sin ficha es un
disparador sin dueño.

📌 **Cómo se aplica sin pensarlo mucho:** ante dos pendientes al final de una
sesión, no preguntes cuál importa más. Pregunta **cuál de las dos existe fuera de
tu cabeza**. Esa es la que puede esperar.

### LM.46 — Un agente no se corta por fases del trabajo: se corta por quién puede ser testigo de qué

**Sesión 76, sin código.** Contó cómo montaba TDD antes: **tres agentes, uno para
el rojo, uno para el verde y uno para el refactor.** Es un diseño que se le ocurre
a cualquiera y falla por tres sitios.

**1. El corte no separa nada.** Los tres trabajan sobre el mismo código, en el
mismo problema, uno detrás de otro. El del verde **lee el test que escribió el del
rojo** — igual que si lo hubiera escrito él. `LM.4` pide un testigo que no comparta
la construcción; aquí comparten todo menos el turno. **La ceremonia de la
independencia, sin la independencia.**

**2. Tira contexto y no compra nada con él.** Cada agente arranca frío. El del
refactor no sabe por qué el código quedó así, qué se intentó ni qué se descartó: o
refactoriza a ciegas, o pide todo el contexto de vuelta — y entonces no era un
agente separado, era un traspaso caro.

**3. 🚨 Y la peor: le da un cargo al defecto.** El agente del verde tiene **una
sola métrica de éxito: que el test pase**. Es literalmente la orden que `LM.43`
señala como mal formulada, ahora convertida en puesto de trabajo — y encima en
manos de alguien que no escribió el test y no tiene ningún apego a él. **El reparto
no frena el defecto: lo institucionaliza.**

🔑 **El error de fondo es copiar el organigrama.** En una empresa los roles existen
por una razón física: **una persona no puede estar en dos sitios, y dos personas no
comparten cerebro.** El organigrama resuelve un problema de cuerpos, y un agente no
tiene ese problema.

> **Un agente sí puede hacer dos cosas seguidas. Lo que no puede es ser testigo de
> sí mismo.** Ese es su único límite real — y por tanto el único corte que compra
> algo.

Y en TDD la continuidad **es** el producto: ves el rojo, y esa experiencia es la
que te dice cómo escribir el código. Partirlo en tres tira lo único que el ciclo
fabrica.

**Las tres razones que sí justifican un agente nuevo:**

| Razón | Qué compra | Señal |
|---|---|---|
| **Independencia de criterio** | un testigo que **no vio** construir | si le pasas tu contexto, es un eco (`LM.5`) |
| **Aislamiento de ruido** | que 500 archivos o 40 MB de log **no entren** en tu contexto | solo te importa la conclusión |
| **Paralelismo real** | tiempo | las tareas de verdad no se necesitan entre sí |

⭐ **Y la pregunta que decide, que cabe en una línea:**

> **¿Este agente necesita saber MENOS que yo, o MÁS?**
>
> **Menos, y su valor está en no saber** → es un agente.
> **Más, o todo lo mío** → es un traspaso, y los traspasos pierden. Hazlo tú.

Los tres agentes de TDD caían del lado equivocado: el del verde necesitaba todo lo
del rojo, y el del refactor todo lo de los dos.

📌 **El matiz, para no aplicarlo de más:** esto no dice que los subagentes sobren.
Dice que **repartir por fases del trabajo es casi siempre el corte equivocado**, y
repartir por quién puede atestiguar qué es casi siempre el correcto.

### LM.47 — Un verificador entrega evidencia; en cuanto entrega veredicto se vuelve coartada

**Sesión 76**, de una pregunta suya: ¿cabe un subagente que verifique **dentro** de
la sesión que construye, antes de pasar el trabajo a la terminal auditora?

**Cabe, y pasa el test de `LM.46`:** necesita saber **menos** que quien construyó, y
su valor está ahí. Pero solo si el reparto es este:

| Recibe | **No** recibe |
|---|---|
| el criterio escrito por el humano | el relato de cómo se llegó al código |
| el diff y los artefactos | qué se intentó y se descartó |
| poder correr comandos | **permiso de escribir** (`LM.5`) |

**Lo que caza bien** es lo mecánico y comprobable desde los artefactos: si el rojo
existió, si el diff del refactor tocó tests (`LM.44`), si algún test se modificó y
con qué autorización (`LM.43`), si cada criterio tiene un test que le corresponda.
Trabajo de volumen, tedioso, y **con incentivo estructural a no mirarlo** por parte
de quien construyó. Ese es el perfil que justifica un agente.

**Lo que no puede cazar**, y no es cuestión de esforzarse: si el criterio estaba
bien, si algo se recortó en silencio, si el conjunto sirve. Eso pide estar **fuera
del marco**, no en otro proceso dentro de él. No sustituye a la terminal auditora:
**le quita de encima el trabajo mecánico.**

> 🚨 **Y aquí está el peligro, que es `LM.41` con otro traje: un verificador que
> devuelve un veredicto verde se convierte en una coartada.** La auditora abre el
> informe, lee *"verificado"*, y esa zona baja de prioridad sin que nadie lo haya
> decidido. La señal de diligencia sustituye a la diligencia.

Y hay un segundo empuje en la misma dirección: a un agente al que se le pide
*"revisa esto"* sin lista cerrada, **la versión cómoda no le ofrece resistencia
mientras la escribe** (`LM.26`) — y este nace dentro de la sesión que construyó.

**Las dos reglas de diseño que lo neutralizan:**

1. **Evidencia, no veredicto.** No dice *"todo bien"*: dice *"corrí esto, salió
   esto"*, con la salida cruda pegada. **Un veredicto desplaza la auditoría; una
   evidencia la alimenta.**
2. **Lista de comprobaciones cerrada, no "busca problemas".** Preguntas concretas
   con su evidencia al lado. Es denegar por defecto aplicado a la revisión: **lo
   que no está en la lista no se declara limpio, se declara NO MIRADO.**

📌 **Y el eco que obliga a la regla 1:** *el resumen sale peor que el documento* ha
salido **cuatro veces en cuatro sesiones** de este proyecto, con autores distintos
cada vez. Un verificador que resume es la quinta oportunidad para el mismo bicho.
**Salida cruda, no resumen.**

---

### LM.48 — Las tres preguntas del agente en producción llegan tarde por diseño, y por eso se declaran cuando todavía no hay nada que medir

**Sesión 77**, y la trajo él: *"para futuros proyectos, que no se nos olvide
ninguna de las tres"*. Las tres son **evaluación, observabilidad y seguridad**.

**Cada una responde una pregunta distinta, y en un momento distinto:**

| | Pregunta | Cuándo |
|---|---|---|
| **Evaluación** | ¿funciona? | **antes** de soltarlo |
| **Observabilidad** | ¿qué está haciendo ahora? | **mientras** corre |
| **Seguridad** | ¿qué puede hacer, y qué le pueden hacer? | **porque** está expuesto |

**El defecto no es que se olviden: es que ninguna duele el primer día.** Un agente
en tu máquina, sin usuarios, funciona sin evals, corre sin registro y no lo ataca
nadie. Las tres se cobran solas cuando ya hay algo que perder — y entonces se
construyen a la carrera, encima de un diseño que no las esperaba.

En este curso pasó exactamente así, y salió barato porque era un curso: evals
llegó cuando no se sabía si el agente servía; seguridad llegó cuando una consulta
devolvió **1000 filas en vez de 1** (`L5b.9`). En un proyecto de la empresa, quien
paga ese aprendizaje es el cliente.

> 🔑 **Por eso se declaran el día 1, cuando no hay nada que medir.** No se
> *construyen* el día 1 — eso es imposible y no se pide. Se les da **dueño y
> sitio**: dónde vivirán los tests, dónde se escribirá el registro, y cuál es la
> lista de herramientas del agente.

**Y una casilla marcada con una intención no es un freno, es una nota** (`LM.13`).
Cada una se marca con un **artefacto que existe**:

- **Evaluación** → hay archivo de tests **y salió en rojo al menos una vez**. Un
  test que nunca falló no probó nada (`LM.42`).
- **Observabilidad** → hay un registro escribiéndose, **y ya se abrió** para
  responder una pregunta. Un registro que nadie leyó es disco ocupado.
- **Seguridad** → está escrita **la lista de herramientas del agente y sus
  permisos**. Esa lista *es* la superficie de ataque: sin ella no hay conversación
  de seguridad posible, solo miedo.

📌 **Y el orden entre ellas no es de importancia, es de dependencia:**
observabilidad antes que seguridad, porque **sin registro no puedes ver morder un
freno de seguridad** — ni demostrar que un ataque ocurrió. `LM.13` en su forma más
literal.

🚨 **Lo que esta lección NO puede hacer sola:** vive en `LESSONS.md`, que se lee
cuando alguien viene a buscarlo. Por eso el mismo día bajó a `GUIDE.md` §6 como
tres casillas ejecutables, y a `CLAUDE.md` como puntero de una línea. **Escribir
algo cierto donde nadie lo alcanza es `LM.20`**, y en este repo ya pasó tres veces.

---

### LM.49 — Un sí/no bien empaquetado no invita a auditar la premisa: invita a contestar

**Sesión 82.** La pregunta llegó limpia: *"¿subimos el tope a tres frases?"*. Traía
el trabajo hecho, la hipótesis escrita, el precio calculado y **una sola casilla que
marcar**. Yo di el sí antes de abrir el archivo.

Lo abrí después, y la hipótesis era falsa. `[D-089]` decía que la rúbrica se
contradice —*pide aliento + corrección + explicación y solo deja dos frases*—.
Leída entera, para el caso `FIX` pide **dos** cosas:

> *"give the corrected sentence **and** name the one mistake that matters most"*

El aliento sale de la línea de personaje —*"warm, encouraging tutor"*—, que es
**tono, no un renglón**. El modelo eligió gastarse una frase en el tono.

> 🔑 **Y si el argumento hubiera sido solo ése, la respuesta correcta era la
> contraria:** decirle *"sé cálido dentro de las dos frases"*, y quedarse con
> respuestas cortas — que es lo que la propia rúbrica defiende.

**El sí era el bueno. El porqué escrito, no.** Y es la parte que sobrevive: un
motivo equivocado no molesta hoy, se cita mañana como precedente.

**El mecanismo es la forma de la pregunta, no la pereza de quien contesta.** Una
pregunta abierta —*"¿qué ves aquí?"*— manda a mirar. Una cerrada manda a **elegir**,
y elegir entre dos opciones que alguien ya redactó es aceptar el marco entero sin
tocarlo: los dos caminos comparten la premisa, así que ninguna de las dos respuestas
la pone a prueba.

> ⚠️ **Es `LM.30` con otra piel** (*la urgencia no se audita, se obedece*). Allí lo
> que apagaba la revisión era la prisa; aquí, **el acabado**. Un paquete bien hecho
> tranquiliza igual que un verde — y `LM.15` ya dijo qué le pasa a lo que tranquiliza.

**Lo que queda como hábito:** ante un sí/no que llega con todo resuelto, la primera
pregunta no es *"¿sí o no?"* sino **"¿de dónde sale la frase que hace que esto sea
una pregunta?"** — y esa frase casi siempre está en un archivo, no en el mensaje.

---

### LM.50 — Un detector cuyo ancla es lo que estás a punto de mover no es un detector

**Sesión 82.** La otra mitad de la firma: el corrector marcaba como fallo *cualquier*
comilla doble, y la rúbrica solo prohibía las que **envuelven la corrección**. Una
respuesta correcta —`you used "going to" for the future perfectly`— salía roja.

Dos salidas opuestas: **afinar el corrector** para mirar solo las comillas de la
corrección, o **endurecer la rúbrica** y prohibirlas todas.

Ellos lo plantearon como *"afinar es más código y más frágil"*. **Eso es un precio,
no un argumento.** El argumento es que la primera opción **no se puede construir**:
para mirar las comillas *de la corrección*, el programa tiene que saber **qué trozo
es la corrección**. Nadie se lo dice. En las nueve respuestas medidas, la corrección
entraba de **cinco formas distintas**, y una llegaba sin ninguna entradilla:

```
Say: She goes to school every day.
We say: I am 20 years old.
It should be: My sister has a dog.
The correct sentence is: Where are you going?
He doesn't like pizza.          ← sin entradilla
```

Sería una heurística sobre **la manera de hablar del modelo**. Y ahí está el fondo:

> 🔑 **El ancla que esa heurística necesita es justo lo que el plan va a mover.** El
> proyecto entero existía para bajar de Opus a Sonnet y a Haiku *midiendo cuándo se
> les va la forma*. Cambiar de modelo cambia el fraseo. Cuando la heurística fallara
> en esa corrida, **nadie podría distinguir *"el modelo se rompió"* de *"la
> heurística resbaló"***.

**Un instrumento tiene que ser más estable que lo que mide.** Si se apoya en la
misma cosa que está midiendo, no mide: acompaña.

📌 **Y hay una pista barata para verlo sin pensar tanto:** el módulo declaraba en su
primera línea que sus promesas eran *"las que comprueba un programa **sin opinar**"*.
Saber dónde empieza la corrección **es opinar**. La opción propuesta no era cara —
era de otra categoría, y el propio archivo tenía la frontera escrita.

---

### LM.51 — Un comentario que jura que no hay copia apaga la búsqueda de la copia

**Sesión 82.** `COST_PER_CALL_USD` estaba escrito en **dos** archivos. El aviso de
que el número había caducado se puso en uno de ellos — y **quien iba a gastar era el
otro**, que tenía su propia copia y su propio total impreso.

Hasta ahí es el bicho de la sesión 33: la misma cosa en dos sitios. Lo que lo sube de
categoría es **dónde estaba la copia**:

```python
# 🔑 Las 60 frases y el monedero se IMPORTAN, no se copian. Tener dos topes de
# gasto es tener uno de los dos desactualizado sin saber cuál.
from measure_tutor import (SENTENCES, CallBudget, ...)   # ← el monedero NO está aquí
...
COST_PER_CALL_USD = 0.00304                              # ← tres líneas más abajo
```

**Tres líneas.** El comentario decía la regla, la importación no la cumplía, y la
copia estaba debajo de las dos.

> 🔑 **Y el daño no es que mienta: es que resuelve la duda del lector en la dirección
> de no mirar.** Quien fuera a corregir el número leía *"se importa, no se copia"*,
> concluía que había **una sola** copia, y dejaba de buscar la segunda.

Es `L-075` con agravante. Allí un docstring decía la regla y la línea de debajo la
incumplía: el daño se acababa en esa línea. Aquí el comentario **manda al siguiente
lector a otro sitio**, así que el error se propaga a quien venía a arreglarlo.

**Un comentario equivocado es peor que ningún comentario**, y la razón es contable:
sin comentario, el que busca duplicados busca; con él, ya recibió la respuesta.

> ⚠️ **Regla práctica:** un comentario que afirma *"esto está en un solo sitio"* es
> una afirmación verificable, y por tanto **le toca un test**, no la buena fe. Aquí
> terminó existiendo: `test_the_wallet_is_imported_not_copied`.


---

### LM.52 — Una cerradura que hay que acordarse de echar sigue siendo una advertencia

**Sesión 83.** El día anterior, `PI-8` —*"aquí no entra la frase de una persona real"*—
era un comentario. Se convirtió en función: `sentences_are_invented()`. Bien escrita,
bien probada, y **honesta sobre su alcance** en el docstring.

Y llamada **solo desde tres tests, con registros hechos a mano**.

La promoción de un corpus a la carpeta protegida era un `mv` manual. O sea que
**invocar la cerradura era un acto de acordarse** — exactamente lo que la función
existía para eliminar. En `eval_rubric.py` ya había una frase dándolo por hecho en
presente, como si el control corriera solo.

> 🔑 **Es el mismo defecto con una capa más de pintura, y la pintura es lo peligroso.**
> Un comentario da miedo: quien lo lee sabe que nadie lo comprueba. **Una función
> tranquiliza.** Tiene nombre, tiene tests, sale en verde — y nada de eso dice que
> alguien la llame en el camino que importa.

Es `LM.15` mudado un piso: allí el instrumento era ciego, aquí **el instrumento ve y
nadie lo enciende**. Las dos veces el resultado es silencio, y el silencio se lee como
confirmación.

**Un control se echa sobre la carpeta entera, con un `glob`, no sobre los registros
que alguien tenga a bien pasarle.** La diferencia entre un portero y un saludo es que
el portero no depende de que le presenten a nadie: mira lo que hay, corra quien corra,
por la vía que sea y se haya acordado quien se haya acordado.

> 📌 **Y el patrón ya estaba en casa.** El portero sobre `data/` de `T-071`, sesión 49,
> hacía exactamente esto. No hubo que inventarlo: hubo que reconocerlo.

---

### LM.53 — Un criterio que se evalúa después deja la evidencia esperando en el sitio menos duradero

**Sesión 83.** La regla propuesta para conservar un corpus era: *"se guarda aquel cuya
rúbrica ya no existe en producción"*.

Se comprueba sola, no se estira, no admite discusión. Parece buena.

**Pero en el momento de crear un corpus, la rúbrica está viva por definición.** Así que
bajo esa regla **nada se guarda nunca al nacer**. Se guardaría más tarde, el día que
alguien cambiara la rúbrica y se acordara de mirar atrás. Y mientras tanto el archivo
espera en `data/`: un disco sin copia, fuera de Git.

> 🔑 **Su valor solo se reconoce a toro pasado, y el reconocimiento depende de que
> alguien se acuerde.** Que es la misma dependencia que `LM.52` acababa de quitar de
> en medio, reapareciendo por la puerta del criterio en vez de por la del código.

**El disparador se pega a un evento que ocurre seguro y se nota seguro.** Aquí: el
commit que mueve el modelo o la rúbrica. Quien lo toca, promueve — en ese mismo commit.
No hay que acordarse de nada porque no hay un después: el momento de decidir y el
momento de actuar son el mismo.

Un criterio correcto que se evalúa en el instante equivocado no protege nada. Y no
falla ruidosamente: **se queda esperando, con toda la razón de su parte.**

---

### LM.54 — Un conjunto elegido por su resultado no tiene porcentaje

**Sesión 83.** Un corpus de diagnóstico tenía diez filas y las diez estaban rotas. Eso
no es un hallazgo del 100%: **son las diez que se escogieron precisamente porque habían
fallado.**

El nombre del archivo llevaba el modelo, la fecha y la huella de la rúbrica. Ninguno de
los tres dice cómo se eligieron las filas. Así que en el disco quedaba un **100% de
fallo esperando a que alguien lo divida** — y quien lo divida seis meses después tendrá
todos los datos menos el único que importa.

> 🔑 **La selección es una propiedad del conjunto, no de las filas.** Ninguna fila
> guarda por qué está ahí. Mirándolas una a una nunca se recupera.

Es `L-071` —cuadrar contra un agregado no es cuadrar— con el sesgo metido **dentro del
propio conjunto**, donde ningún cuadre lo alcanza.

→ Un cuarto eje en el nombre: `full` o `pick`. Una palabra, y convierte un número que
miente en un número que se sabe leer.

> ⚠️ **Y `pick` no significa "muestra".** Una muestra representa; una selección
> demuestra. Un porcentaje sacado de un `pick` no significa nada, y por eso la palabra
> tiene que estar donde no se pueda perder: en el nombre del archivo, no en el informe
> que se cierra con la terminal.

---

### LM.55 — El aviso vivía en la parte que se borra; la mentira, en la que dura

**Sesión 84, y se cazó antes de pagar.** El guion del eval guardaba el corpus con un
nombre calculado así:

```python
calls = len(plan)          # 60, siempre — es lo que se PLANEÓ llamar
```

Pero el bucle llevaba dos `break` documentados **en la propia cabecera del archivo**
como el modo de fallo esperado. Si la tanda se cortaba en la frase 30, el nombre seguía
diciendo `full`.

El informe **sí avisaba**: imprimía cuántas llegaron de cuántas se pidieron. Y ahí está
el reparto que hace grave lo que si no sería un descuido:

> 🔑 **El aviso vive en la ventana de la terminal, que se cierra. El nombre vive en el
> disco, que dura años.** La verdad estaba en lo efímero y la mentira en lo permanente.
> Dentro de una hora solo queda una de las dos, y no es la buena.

Y la segunda mitad costaba dinero. Con `open("w")` y modelo, fecha y huella iguales
dentro del mismo día, **una corrida cortada por la tarde machacaba la línea base pagada
por la mañana**. `L-076` vivo dentro de su propio arreglo.

**Un archivo se nombra con lo que llegó, no con lo que se pidió.** Es una línea:

```python
written = replies_file(len(records))     # lo que hay dentro, no lo que se planeó
```

> 📌 **Regla práctica:** cuando un dato aparece en dos sitios con vidas distintas —la
> pantalla y el disco, el log y el nombre, el chat y el archivo—, el correcto tiene que
> estar en **el que sobrevive**. El otro es cortesía.

---

### LM.56 — Un nombre de test es una afirmación que nadie audita

**Sesión 84.** Existía este test, en verde:

```
test_a_partial_run_is_named_pick_not_full
```

El nombre describe exactamente el riesgo de `LM.55`. Por eso **nadie abrió el cuerpo**.
Y el cuerpo probaba una tanda que se **pidió** corta — nunca una que **se cortó sola**,
que es el único caso donde el bug existía.

> 🔑 **Es peor que no tener el test, porque ocupa su sitio en la lista.** Un hueco se
> ve. Un test con el nombre correcto y el cuerpo corto **es un hueco tapado con una
> etiqueta que dice "cubierto"**.

Es `LM.15` mudado a la carpeta `tests/`. Un instrumento ciego no da un dato falso: da
silencio. Aquí el silencio venía firmado con el nombre del riesgo.

> 📌 **Y el detalle que explica por qué se escapó tanto tiempo:** el test que faltaba
> era **el primero del proyecto que entraba en `main()`**. El número equivocado solo
> existía dentro de esa función, así que ninguno de los tests de alrededor —todos sobre
> funciones puras, todos correctos— podía verlo. La cobertura era buena en todas partes
> menos donde el programa de verdad se ejecuta.

**Al leer una suite, el nombre del test es lo que se está afirmando; el cuerpo es lo
único que se está comprobando.** Solo uno de los dos se ejecuta.

---

### LM.57 — Un control vive donde se ejecuta, no donde está escrito

**Sesión 85.** Se construyó una carpeta para las etiquetas hechas a mano —sesenta
juicios humanos que, una vez escritos, no se pueden volver a comprar— con catorce
porteros en `pytest`. Buenos porteros: uno comprobaba que las sesenta frases estuvieran
cubiertas exactamente una vez.

Y aun así, esta función:

```python
def progress(rows):
    done = sum(1 for row in rows if row.get("verdict") is not None)
    return done, len(rows)          # ← el denominador sale del propio archivo
```

Editando sesenta líneas de JSON a mano se pierde una línea. Es así como se pierde una
línea. Y entonces la herramienta imprimía:

```
50 de 50 etiquetadas. Filas mal formadas: 0.
```

**Completo y limpio.** El portero que lo cazaba existía — y vivía en `pytest`, que no
es lo que alguien corre sesenta veces mientras etiqueta. Lo que se corre sesenta veces
es `python labels.py`.

> 🔑 **La cobertura no se mide por lo que la suite comprueba, sino por lo que comprueba
> el instrumento que la persona tiene delante.** Un control que solo vive en el camino
> que nadie recorre esa tarde está apagado esa tarde.

Es `LM.55` girada noventa grados. Allí el aviso estaba en la parte que se borra; aquí
**el control está en la parte que no se corre**.

→ El denominador contra la referencia (`len(SENTENCES)`), y que la herramienta **cante
las filas que faltan** — que son las únicas que ningún bucle sobre `rows` puede
encontrar, porque no están ahí para ser miradas.

> ⚠️ **Y la variante cara de lo mismo, del mismo día:** nada comprobaba que la carpeta
> estuviera de verdad en Git, que era **toda la razón** de haberla creado. La garantía
> descansaba en un `git check-ignore` corrido una vez y anotado en un comentario. Un
> freno que no has visto morder es una nota (`LM.13`); un freno que mordió una vez
> delante de ti, y cuya vigilancia no quedó en ningún sitio ejecutable, es un recuerdo.

---

### LM.58 — Citar un mecanismo por su nombre no comprueba su alcance

**Sesión 85, dos veces el mismo día, una por cada terminal.**

**Una.** La terminal que construye declaró que una tarea pendiente era **bloqueante**
de la decisión del día, porque *"su portero no miraría el archivo nuevo"*. Cierto del
portero — pero ese portero recorre `CORPUS_DIR.glob("*.jsonl")`, y bajo el plan que se
acababa de firmar el archivo iba a **otra carpeta**. Ese `glob` no lo alcanza ni roto
ni arreglado.

**Dos.** La terminal que supervisa pidió no estrenar un segundo lector de la primera
línea de la respuesta, y señaló el que ya existía en `rubric_check`. Pero ese es
`learner_message`, y su propio docstring dice que devuelve **si** había palabra clave y
**tira cuál era** — justo el dato que la comparación necesitaba. El lector bueno era
otro, `split_verdict`, en otro módulo.

> 🔑 **Las dos veces el principio era correcto y el objeto señalado era el equivocado.**
> Y las dos suenan igual de sólidas al decirlas, porque citan **un mecanismo real, por
> su nombre real, que hace algo real**. Lo único falso es la frase que lo une al caso
> de hoy.

Es de la clase muda. No hay error, no hay rojo, no hay traceback — **no hay código
todavía**. Solo trabajo construido sobre un supuesto que nadie abrió, y que se
descubriría semanas después cuando el mecanismo no hiciera lo que su cita prometía.

Es la familia de `L-081` del día anterior, donde un agujero real se ilustró con el
único ejemplo que el mecanismo sí atrapaba: **un hallazgo que se siente medido cuando
solo está nombrado.**

> 📌 **Regla práctica, y cuesta un minuto:** antes de apoyar una decisión en *"eso ya
> lo cubre X"*, abre X y lee qué mira y qué devuelve. El nombre de una función es lo
> que alguien quiso que hiciera. La firma es lo que hace.

### LM.59 — Un test que afirma AUSENCIA se cumple igual con el instrumento ciego

**Sesión 87, y mató una garantía que había propuesto yo esa misma tarde.**

Al reescribir el nombre de los corpus había que proteger el archivo viejo, el que la
decisión mandaba **no renombrar**. Yo propuse la protección así: *"`test_the_archived_
name_agrees_with_its_rows` no se modifica — la exigencia es que **siga verde**."*

Sonaba bien. Ese test recorre los archivos reales y exige que el portero no devuelva
problemas. La otra terminal lo saboteó —dejó el portero ciego sobre la generación
vieja— y **la suite entera pasó: 574 en verde con el guardián apagado**.

> 🔑 **El motivo es general y no tiene nada que ver con este portero.** El test
> afirmaba `not problems`. Un portero que mira bien y no encuentra nada devuelve la
> lista vacía; un portero que **no mira nada** devuelve exactamente lo mismo. **Verde
> es el resultado del arreglo bueno y del malo a la vez**, así que no distingue entre
> los dos — que es la única cosa que un test tiene que hacer.

Es la tercera vez de esta especie en dos días: el test que se quedaba verde y hueco al
cambiar el nombre del corpus, este portero, y `_frozen_corpora` en su día. Por eso subió
a lección y no se quedó en nota de tarea.

📌 Y fíjate en el agravante, porque es lo que la hace fácil de repetir: **"que siga
verde" suena a la protección más barata que existe** — no tocas nada, no firmas nada,
no gastas un test. Justamente por barata no se audita.

> 📌 **Regla práctica:** un guardián no se demuestra enseñándole lo que debe aceptar.
> Se demuestra **enseñándole algo que tenga que rechazar**. Si no existe un test que le
> ponga delante un caso malo y exija que muerda, no tienes un guardián: tienes una
> función que se ejecuta.

---

### LM.60 — Un hallazgo sin marca de prioridad le cuesta al lector lo mismo que uno importante

**Sesión 87, y la pidió él a mitad de camino.**

Ese día entregué ocho o nueve hallazgos de auditoría. Todos ciertos, todos con su
evidencia leída del disco. Y todos **con el mismo tamaño y el mismo tono**: los tres que
bloqueaban el paso siguiente y los tres que eran higiene de docstrings. Él tuvo que
deducir la prioridad leyendo párrafos largos hasta el final.

Su corrección fue un esquema de dos ejes: **importancia** —baja, media, alta, y decidir
de verdad si vale la pena— y **urgencia** —bloqueante o no—, marcadas **arriba** del
hallazgo, no al final.

> 🔑 **El valor del esquema no es ordenar mejor lo que ya se entrega: es autorizar a
> soltar cosas.** Si algo es de importancia baja, se lleva una línea o no se entrega.
> El coste de un hallazgo menor bien argumentado no son los tokens que ocupa — es que
> **compite por la atención** con el que sí paraba el trabajo.

⚠️ **Y el esquema trae su propio veneno, que ya se había pagado tres días antes.** Una
etiqueta formal de urgencia hace **más fácil** obedecerla, no más difícil: es `LM.30`
—*la urgencia no se audita, se obedece*— con un campo dedicado donde escribirla. Ese
mismo día una tarea había llegado marcada bloqueante con una consecuencia inventada.

> 📌 **Regla práctica, y es la que salva el esquema:** «bloqueante» solo vale con la
> frase que dice **qué bloquea y qué se rompe si sigues**. Falsificable, no adjetivo. Si
> no se puede escribir esa frase, no es bloqueante. La importancia es juicio y se puede
> discutir; **la urgencia es un hecho o es una mentira.**

📌 Y la casilla que se pierde siempre es **«alta / no bloqueante»**: importante y sin
fecha. No grita, así que espera turnos enteros. Es el argumento a favor de los dos ejes
en vez de uno solo.

---

### LM.61 — La señal gratis llega antes que la cara, y nadie le escribió qué significa

Se selló bien lo caro. Antes de gastar `$0,10` en correr un juez sobre 30 frases nuevas,
quedaron escritos en Git los cinco tramos del resultado: qué número sería un fracaso, cuál
la banda esperada, cuál un techo deshonesto. Y funcionó — salió **0 desacuerdos de 30**, el
tramo del fracaso, y no hubo nada que negociar. Sin esos tramos, un cero se reporta como
*«el corrector acierta el 100% incluso en frases difíciles»*: verdad literal, conclusión
falsa.

Lo que nadie selló fue lo gratis.

Una hora antes de la factura ya existía otro número. Quien escribió las frases las había
repartido en dos grupos según el error que buscaban provocar; quien las etiquetó, sin ver ese
reparto, produjo el mismo reparto exacto. **30 de 30.** Dos lectores independientes,
ninguna duda, ni una discrepancia.

Ese número decía, ya entonces, que las frases eran **inequívocas**. Y una frase inequívoca
para dos lectores tenía pocas razones para tropezar a un modelo grande. El aviso estaba
disponible, era exacto y no costaba nada — y pasó como color de fondo, porque **nadie había
escrito de antemano qué significaría.**

> 🔑 **Cuando selles la predicción de una medición que cuesta, pregunta qué señal más barata
> llega primero y séllale también su significado.** Un precursor sin tramos escritos no es un
> aviso: es un dato que se leerá después, cuando ya no pueda cambiar ninguna decisión.

⚠️ **Y la parte específica NO es la lección.** *«Una vara inequívoca para dos lectores humanos
no discrimina a un modelo grande»* es una **observación con n=1**. Suena a regla, entraría al
registro con cara de regla, y nadie la volvería a auditar. Se anota como hipótesis, con su
única observación al lado — que es lo que la regla 6 del proyecto pide de cualquier número que
no se haya medido dos veces.

📌 Es la familia de `LM.15` una vez más, con el defecto movido de sitio: allí un instrumento
ciego daba silencio y el silencio se leía como confirmación. Aquí el instrumento **habló** y
no había dónde apuntar lo que dijo.

---

### LM.62 — Saltarse una práctica sin escribir por qué la convierte en prescindible

TEAPP se cerró sin comparar modelos. Estaba planeado desde hacía semanas: bajar el juez de
Opus a Sonnet y después a Haiku, midiendo qué se perdía. No se hizo, y la razón es buena —
es un proyecto **educativo**, no se vende, no tiene clientes, no hay factura que optimizar
a escala. El recorrido que justificaba su existencia estaba caminado entero.

Y hay una segunda razón, que es la que de verdad manda: **el aprendizaje del tramo ya estaba
cobrado.** Una vara que dos humanos leen igual puede no discriminar a un modelo — `30/30` de
acuerdo entre humanos, `0 de 30` de desacuerdo con el juez. Repetir el ejercicio con dos
modelos más compraba una lección más pequeña por el mismo dinero.

> 🔑 **Un proyecto educativo se cierra cuando deja de enseñar, no cuando se vacía la lista de
> tareas.** La lista nunca se vacía: siempre queda deuda pequeña y real. El criterio no es
> «¿queda algo?», es «¿lo que queda enseña más de lo que cuesta?».

Hasta aquí, una decisión de alcance normal. Lo que la hace lección es lo que pasa **después**.

Dentro de seis meses alguien abrirá el registro y leerá *«el paso 9 se cerró sin comparar
modelos»*. Esa frase, sola, no dice *«se saltó porque este proyecto no lo necesitaba»*: dice
**«se puede saltar»**. Y el que la lea puede ser el propio autor, ya en un producto de verdad,
buscando permiso.

> 🚨 **Un salto sin motivo escrito se lee como un veredicto sobre lo saltado.** No queda como
> «aquí no hacía falta»; queda como «no hace falta». La ausencia no se explica sola, y el
> lector futuro completa el hueco con la versión cómoda — que es siempre la que no le pide
> nada (`LM.26`).

Por eso el cierre no dice solo qué no se hizo. Dice, en mayúsculas y con nombre propio, **qué
sería obligatorio en una aplicación comercial**: construir una vara que discrimine *antes* de
cambiar el modelo —un eval saturado da 100 antes y 100 después, así que no es un freno, es un
adorno—, medir forma y veredicto por separado, distinguir *«el juez corrige de más»* de *«el
juez perdona»* en vez de promediarlos, medir el coste real de cada candidato, y tener una
regresión que corra sola en cada cambio.

📌 **La frase que hace el trabajo es la que separa las dos cosas:** *no se hace **porque** el
proyecto es educativo; en uno comercial sí se hace.* Sin ese «porque», las dos mitades se
funden en una sola conclusión falsa.

⚠️ **Y hay un daño de segundo orden, que apareció al auditar el cierre.** `[D-049]` —la
decisión de bajar de modelo— aparecía citada en diecinueve sitios del código, y casi en
ninguno era *la cosa afirmada*: era **la coartada de una protección que ya existía**. El
módulo que comprueba la forma, la decisión de no afinar un detector, un eje del nombre de los
corpus, el único test que clava el modelo — todos justificaban su existencia nombrando un
descenso que ahora no va a ocurrir.

> 🔑 **Cerrar una decisión no deja afirmaciones falsas sueltas: deja piezas buenas sin motivo
> escrito.** Y una pieza sin motivo no se corrige, se borra — porque quien la encuentra lee su
> justificación caducada y concluye que sobra. → Al renunciar a una decisión, **la renuncia
> tiene que adoptar explícitamente lo que la decisión engendró**, o la limpieza siguiente se
> lleva por delante justo los frenos que se querían conservar.

---

### LM.63 — Un fallo se resume por su consecuencia, y la consecuencia es la mitad que no sirve para arreglarlo

Un especialista se negó, y dijo por qué: *«me mandaron dólares donde iban euros»*. Su jefe
inmediato lo repitió **entero** y le añadió una coletilla: *«por lo tanto no tengo el dato»*.
El jefe del jefe se quedó con **la coletilla** y tiró el motivo.

🔑 **Ninguna capa mintió, y aun así arriba llegó una frase inútil.** *«No tiene el dato»* es
verdad y no le dice a nadie qué arreglar. La **causa** es accionable; la **consecuencia** es
lo que se parece a todas las demás consecuencias — y por eso es la que sobrevive a un
resumen: resumir es quedarse con lo último y lo general.

⭐ **Y la prueba de que eso hace daño llegó sola, en la misma corrida.** La otra rama falló
por una caída de red real, que nadie inyectó. Dos fallos **de naturaleza opuesta** —uno
culpa nuestra y arreglable, otro ajeno y transitorio— llegaron arriba con la misma frase:
*«no se pudo, por falta de datos de conversión»*. **Indistinguibles.**

🚨 **Y es peor que un booleano.** `correct: bool` mezcla causas contrarias en una casilla,
pero al menos **se ve** que no explica nada. La prosa mezcla igual y **suena informativa**:
tiene sujeto, verbo y motivo aparente. Un resumen educado es un booleano que aprendió a
disimular.

📌 **Lo que lo salva no es un prompt mejor pidiendo detalle, es la FORMA de lo que cruza.**
En la misma corrida, el salto que iba por **contrato** (campos de un diccionario) conservó
el motivo entero, y el que iba por **prosa** lo perdió — con el system prompt de esa capa
ordenándole explícitamente conservarlo. La instrucción estaba; no bastó.

**Dónde muerde fuera de aquí:** cualquier cadena donde un error suba por texto — capas de
servicios, informes de agentes, alertas que un humano lee al final. Si arriba no puedes
distinguir *«hay que arreglar algo»* de *«reintenta en un minuto»*, la cadena está
funcionando **exactamente como se diseñó**, y esa es la mala noticia.

### LM.64 — Cuadrar la suma no es haber atribuido nada

Un registro de dos capas guardaba, en cada renglón, quién lo había hecho. Se renombró el
dueño de **35 renglones** —el gasto de un worker pasó a figurar como de otro— **sin tocar un
solo número**: ni un costo, ni un token, ni una hora, ni el orden. El auditor siguió dando
**exactamente el mismo total** y **exactamente las mismas llamadas**. Ninguna de las catorce
pruebas del nivel se puso roja. **$0,036617 cambiaron de dueño y nadie se enteró.**

🔑 **El total es una pregunta más pequeña de la que parece.** *«La contabilidad cuadró al
centavo»* se había declarado **tres sesiones seguidas** como prueba de que las cuentas
estaban sanas. Lo que esa frase demuestra es que **la aritmética cierra**, y la aritmética
cierra igual de bien con las etiquetas cambiadas: sumar es conmutativo, y a quién se le
apunte cada sumando no altera el resultado.

🚨 **Y el daño no es teórico: el mismo síntoma tiene dos causas y el harness no las
distingue.** El mejor hallazgo de todo un bloque se destapó al ver una tabla de gasto con
*dos líneas de una moneda y ninguna de la otra*. Esa tabla se puede fabricar idéntica
**solo renombrando etiquetas**, sin que nada esté realmente mal. Aquella vez la causa era
real — y se comprobó **a mano, y solo porque alguien sospechó**.

📌 **El defecto no está en el que suma.** El auditor hace aritmética y la hace bien; tiene su
propia prueba contra un registro cuyo total se conoce. El defecto es que **la atribución no
tiene dueño**: el reparto por capa se calcula, se imprime, se usa para sacar conclusiones —
y no hay una sola prueba que lo compruebe. Es un instrumento **al que nadie le pregunta
nunca si acertó**, que es peor que uno que miente: el que miente acaba contradiciendo algo.

⭐ **Y la consecuencia práctica, antes de escribir la siguiente línea:** añadir un campo
`padre` al registro **no arregla esto por sí solo**. Un campo que nace sin nadie que lo
compruebe es un adjetivo más. **La pieza no es el campo: es la prueba que lo tuerce a
propósito y exige que algo se ponga rojo.**

**Dónde muerde fuera de aquí:** cualquier sitio donde un total se reparte entre dueños —
facturación por cliente, atribución de errores por servicio, uso de recursos por equipo,
métricas por región. El total se audita siempre, porque salta a la vista cuando falla. **El
reparto casi nunca**, porque cuando falla sigue sumando lo mismo.

### LM.65 — La traza es lo único del harness que no se puede añadir hacia atrás

Se instrumentó un multi-agente para que cada renglón del registro supiera de quién era hijo.
Funcionó. Y al ir a aplicarlo a las corridas ya guardadas —cinco sesiones de datos, pagados
con dinero de verdad— apareció que **no se puede**. No es caro: es imposible. Los campos no
están, y no hay de dónde deducirlos.

🔑 **Todo lo demás del harness se puede poner después. Esto no.** Un test se escribe cuando
aparece el bug. Un presupuesto se pone cuando asusta la factura. Un permiso se recorta el día
que alguien se asusta. Los tres arreglan **el futuro y el pasado a la vez**, porque el pasado
se puede volver a correr. **La traza no arregla nada hacia atrás: o la línea nació sabiendo
de quién era hija, o esa línea ya nunca lo va a saber.**

⚠️ **Y el sustituto barato falla exactamente donde más falta hace.** La tentación es unir las
piezas por el reloj: *«esta línea salió justo después de aquella, luego cuelga de aquella»*.
Medido sobre un caso real: acertaría **32 de 35** veces — y falla **en el paralelo**, que es
justo la parte que se construyó para presumir. 🔑 **El paralelo es el único sitio donde *lo
que pasó justo antes* deja de significar *quien me llamó*.** Un 91 % de acierto no es un
instrumento: es un instrumento que se equivoca solo en los casos difíciles.

🚨 **Y el mecanismo hereda la misma trampa, sin dar error.** El parentesco se lleva bien en
una variable de contexto —la luz de la habitación: quien entra la tiene, quien sale la
pierde— pero **un hilo nuevo arranca a oscuras**. Sin atar el contexto al cruzar al hilo, los
hijos salen huérfanos y **el árbol se dibuja plano y con pinta de correcto**. Otra vez el
paralelo, otra vez sin excepción y sin aviso.

📌 **Cómo se evita que el árbol mida a quien lo dibujó.** Si el parentesco se pasa a mano
—`padre=` como argumento en cada llamada— sale perfecto, y no prueba que el sistema sepa
quién llamó a quién: prueba que el que escribió las llamadas lo sabía. **Deducirlo del
contexto de ejecución quita esa firma:** nadie escribe el padre, se mira.

**Dónde muerde fuera de aquí:** cualquier decisión de instrumentar. Observabilidad, ids de
petición, versiones de esquema, marcas de origen de un dato. Todo eso parece aplazable
porque *«se puede añadir cuando haga falta»*, y casi todo se puede. **Lo que identifica de
dónde vino algo, no.** Ese es el único trabajo que hay que hacer antes de tener el problema,
porque el día que se tiene, ya es tarde para los datos que lo demuestran.


### LM.66 — Un dato se vuelve comprobable el día que hay otro que puede desmentirlo

Un registro tenía un campo que decía quién había hecho cada línea. Se le cambió el dueño a 35
renglones, a mano, sin tocar un solo número. **Nada se puso rojo.** Ni una prueba, ni una suma,
ni un informe. El campo llevaba cinco piezas de trabajo siendo leído para *imprimir* un reparto
y **nunca para comprobarlo**.

El arreglo obvio parecía ser *añadir una prueba que lo vigile*. Es el arreglo equivocado, y el
motivo es lo que hay que quedarse: **no había con qué compararlo.** Ese campo estaba solo en su
renglón. Cualquier valor que tuviera era consistente con todo lo demás, porque no había nada
más que hablara del mismo asunto. **Una prueba no puede comprobar un dato que nada contradice:
solo puede repetir lo que el dato dice.**

🔑 **Lo que lo arregló no fue una prueba: fue un segundo testigo.** Se grabaron, en el mismo
instante y por caminos distintos, dos cosas que hablan de lo mismo desde ángulos que no se
pueden coordinar: un apuntador (*«mi padre es el tramo t2»*) y un contador (*«yo estoy en el
escalón 2»*). Ahora se pueden contradecir. Si t2 está en el escalón 0, **uno de los dos miente,
y no hace falta saber cuál para saber que algo se rompió.**

📌 Medido, no supuesto. De cinco mentiras posibles sobre el parentesco, cuatro se cazan y **dos
de esas cuatro solo las caza el segundo testigo** — la del escalón que no cuadra y la del padre
de otra corrida. Escritas las dos en su versión más astuta: reparando a mano todo lo demás que
podría delatarlas, para que solo quedara en pie el testigo que se medía.

⭐ **Y una consecuencia que ordena una confusión vieja: un dato que nadie puede contradecir no
es que sea correcto, es que no es comprobable** — y las dos cosas se parecen muchísimo desde
fuera. Un campo que nunca ha fallado y un campo que no puede fallar dan exactamente el mismo
verde. Ante uno de esos, la pregunta útil no es *«¿está bien?»* sino **«¿qué otro dato tendría
que estar en desacuerdo con este si estuviera mal?»**. Si la respuesta es *ninguno*, no hay
nada que comprobar todavía.

⚠️ **Pero el segundo testigo sube el listón, no cierra la puerta.** La quinta mentira —mover
una rama entera a su hermana de al lado, cuadrando el escalón y la corrida— **pasa sin que
nadie grite, y hace bien**: produce algo que pudo haber ocurrido de verdad. 🔑 **La redundancia
caza las mentiras que rompen la forma; las que producen un mundo posible, no.** Para esas hace
falta salir del registro y traer lo que se pedía, que ya no es observabilidad: es evaluación.

📌 Hay un caso donde el segundo testigo no falla nunca, y merece nombre propio: cuando la
mentira es **aritméticamente imposible de cuadrar**. Un ciclo en un árbol no tiene escalones
que puedan encajar — alguien tendría que estar un peldaño por debajo de alguien que está por
debajo de él. Ahí el testigo redundante no caza por vigilancia, **caza por imposibilidad**, y
esa clase entera de mentira queda cerrada.

**Dónde muerde fuera de aquí:** cualquier campo que se escribe una vez y se lee para mostrar.
Etiquetas de origen, dueños, categorías, estados. Antes de escribir la prueba que lo vigile,
mira si hay algo con qué contrastarlo — y si no lo hay, **el trabajo no es la prueba, es grabar
el segundo dato.** Y el corolario incómodo para cualquier tablero: un número que cuadra
(la suma total, el balance, el conteo) puede estar **contestando una pregunta más pequeña de la
que parece**. Cuadrar la suma no es haber atribuido nada.


### LM.67 — Un «a propósito» en un comentario se lee como si alguien lo hubiera medido

Un identificador se generaba con un contador en vez de con azar, y al lado había un comentario
que decía *«se prefiere a un uuid **a propósito**: los ids salen cortos y en orden, y este
archivo no sale de una máquina»*. Unas horas después se midió que dos ejecuciones del mismo
programa producían **el mismo identificador**, porque el contador arranca de cero en cada
proceso. Dos corridas de $0,026390 se fundían en una que declaraba $0,052780, **sin un solo
error**.

🔑 **Lo interesante no es el fallo: es que el comentario nombró el riesgo que estaba asumiendo
y se equivocó en cuál era.** Dijo *«no sale de una máquina»* — o sea, pensó en el espacio. El
peligro estaba en el tiempo: **el mismo archivo, mañana.** Un razonamiento escrito no es más
correcto por estar escrito; lo que gana es **autoridad**, que es otra cosa.

⚠️ **Y ahí está el veneno.** Un «a propósito» le dice al siguiente lector —incluido tú dentro de
dos horas— *«esto ya se pensó, sigue adelante»*. Una decisión sin comentario invita a mirarla;
una decisión con un motivo escrito **la blinda**. El comentario no era mentira: era una
suposición con la ropa de una conclusión.

📌 **Cómo se distingue una de otra, y es barato:** un motivo medido puede decir **qué observación
lo respalda** y **qué observación lo tumbaría**. Si no puede, es una suposición y hay que
escribirla como tal — *«se supone que…»*, *«no se ha comprobado que…»*. Escribir «a propósito»
sin eso es cobrar por adelantado un trabajo que no se hizo.

⭐ **Y el corolario que ordena el resto de esta lista: una batería de comprobaciones que se
cumple entera no dice que no haya nada roto. Dice que no hay nada roto EN LA LISTA.** El día que
esto se midió, seis afirmaciones escritas de antemano salieron verdes a la primera. El fallo no
lo encontró ninguna: lo encontró mirar un nombre en la salida y pensar *«ese nombre es demasiado
corto para ser único»*. 🔑 **Una lista de comprobación protege contra los fallos que ya
imaginaste. No sustituye a mirar.**

**Dónde muerde fuera de aquí:** cualquier identificador que se genera en casa —claves de
idempotencia, nombres de archivo, ids de sesión, sufijos de reintento—. Y más allá de los ids,
cualquier comentario que empiece por *«a propósito»*, *«deliberadamente»* o *«se prefiere X
porque»*. Cuando encuentres uno, la pregunta no es si el motivo suena bien: es **qué medición lo
respalda, y si esa medición sigue siendo cierta hoy**.


### LM.68 — El segundo testigo suele estar ya grabado; lo que falta es alguien que le pregunte

Un experimento salió con un síntoma que tenía **dos causas posibles** y ninguna forma de
distinguirlas: una tabla mostraba dos trabajos hechos por el mismo especialista y ninguno por el
otro. Podía ser que el trabajo se hubiera enviado al sitio equivocado, o que solo mintiera la
etiqueta. Se resolvió **leyendo el encargo a mano**, y quedó anotado que *«el harness no sabe
distinguirlas»*.

Dos sesiones después, la conclusión razonable parecía ser *«hay que grabar un dato más»*. Al ir a
añadirlo apareció que **ya estaba grabado**, y desde antes del experimento. Cada línea llevaba el
nombre de quien trabajó —una etiqueta que alguien escribió— **y** el resultado estructurado de lo
que hizo, que venía de la herramienta. Dos campos, en la misma línea, hablando de lo mismo por
caminos que no se pueden coordinar. Al compararlos, la contradicción salió en un segundo, gratis,
sobre datos que llevaban un día en el repositorio.

🔑 **La instrumentación no faltaba. Faltaba la pregunta.** Y esa asimetría no es casual: **añadir
un campo se parece a progreso y cruzar dos que ya tienes no.** Lo primero se ve en el diff, tiene
nombre, se puede anunciar. Lo segundo es releer lo que ya escribiste, que se siente como no
avanzar. Por eso los registros crecen y las comprobaciones no.

📌 **La consecuencia práctica, y es una pregunta que se hace antes de tocar el código:** cuando
detectes que un dato no es comprobable (`LM.66`), **antes de añadir el testigo, busca si ya lo
estás escribiendo.** Un registro maduro casi siempre tiene, en algún campo puesto para otra cosa,
la sombra del dato que necesitas: un resultado estructurado al lado de un nombre libre, un código
de error al lado de un mensaje, un `id` al lado de una descripción. **La redundancia útil suele
llegar por accidente, y por eso nadie la mira.**

⚠️ **Y hay un coste que se paga en silencio mientras no se mira.** El dato estuvo ahí desde el
principio: eso significa que la investigación a mano que costó una sesión **era evitable el día
que se hizo**. No se pagó por falta de información — se pagó por no haberla consultado. Un
registro que nadie interroga no es observabilidad: **es almacenamiento.**

⭐ **Corolario sobre los rótulos, que es donde se coló la mentira:** si el mismo nombre que se
usa para etiquetar una línea se usa además para dibujar el informe —un árbol, un panel, un
gráfico—, **el informe hereda la mentira del rótulo**. La estructura puede ser honesta y la
lectura falsa al mismo tiempo, y lo que un humano mira primero son los rótulos. Un dibujo
bautizado con adjetivos no es más fiable que sus adjetivos.

**Dónde muerde fuera de aquí:** cualquier incidencia que acabe en *«nos falta telemetría»*. Antes
de aceptarlo, exporta lo que ya se guarda y crúzalo. Muy a menudo la respuesta lleva semanas
escrita en dos columnas que nunca se compararon — y añadir la tercera columna habría tapado, con
una tarea nueva y visible, un trabajo de diez minutos que nadie quería hacer.

---

### LM.69 — Un hueco y una contradicción no se cortan igual: el filtro de completitud deja pasar la respuesta a otra pregunta

Un agente especialista devolvía un paquete de datos estructurado en vez de prosa, y ese paquete
traía consigo la lista de **qué campos no había podido llenar**. La capa de arriba cortaba mirando
esa lista y un campo clave: si el campo esencial venía vacío, la consulta no había servido.
Funcionó durante varias piezas y parecía completo.

Entonces el especialista contestó **otra pregunta**. Se le pidió una moneda y consultó otra. El
paquete subió con los seis campos llenos, la lista de faltantes **vacía**, y el número esencial
presente — sólo que era el número de otra cosa. **Pasó entero por el filtro, porque el filtro
buscaba huecos y no había ninguno.**

🔑 La causa no era que faltara una comprobación más: era que el verificador **no recibía la
pregunta**. Llenaba el campo de identidad con lo que la herramienta hubiera devuelto, y no existía
ningún otro dato capaz de contradecirlo. Es `LM.66` en su forma más cara: *un dato que nadie puede
contradecir no es que sea correcto — es que no es comprobable*, y las dos cosas dan el mismo verde.
El segundo testigo que faltaba no estaba en la respuesta. **Estaba en la pregunta.**

⭐ **Y de ahí sale la distinción que hay que llevarse:** *falta un dato* y *sobra el que hay* son
dos estados distintos y **se cortan en sitios distintos**. Ante un hueco, el que llama a veces
puede seguir con lo que tiene. Ante una contradicción, lo que tiene es justamente lo que no puede
usar. Meterlas en la misma lista hace que la segunda herede el tratamiento de la primera, que es
el más blando de los dos.

📌 **Corolario de tres valores, no de dos:** un verificador que puede quedarse sin la pregunta
tiene que distinguir **no comprobado** de **comprobado y cuadra**. Si los dos casos devuelven lo
mismo, el instrumento ciego se lee como confirmación — que es `LM.15` otra vez, ahora con nombre
de campo. Y al decidir qué hacer con el dato equivocado, conservarlo bajo un nombre que nadie
confunda con un resultado bueno vale más que tirarlo: **tirar el dato es tirar la evidencia**, y
el hallazgo salió justamente de poder leer qué había subido.

**Dónde muerde fuera de aquí:** cualquier validación de esquema. Un JSON Schema, un `pydantic`,
un contrato de API comprueban **forma**, no **correspondencia**. Un payload perfectamente válido
que responde a otra petición pasa todas las validaciones que tengas. La pregunta que hay que
poder hacerle a una respuesta no es *«¿está completa?»* sino **«¿es la respuesta A ESTA?»**, y
para poder hacerla el validador tiene que ver la petición.

---

### LM.70 — Un detector que muerde y cuyo mordisco nadie va a mirar da el mismo silencio que uno que no muerde

`LM.13` dice que un freno que no has visto morder es una nota, no un freno. Este es su reverso, y
sale peor parado.

Un auditor escrito dos sesiones antes cruzaba dos campos que hablaban de lo mismo por caminos
independientes (`LM.68`). Estaba en el repositorio, tenía sus pruebas en verde, y **cazaba la
mentira desde el segundo exacto en que se grabó**. La mentira se grabó en una corrida pagada por
la tarde. Se descubrió a la mañana siguiente **leyendo la salida a ojo**, y una de las pruebas del
auditor llevaba toda la noche en rojo sin que nadie hubiera vuelto a correrla.

🔑 El detector funcionó. Lo que faltaba era el paso que nadie escribió: **volver a pasar los
auditores por encima de lo que acaba de ocurrir.** Una suite se corre antes de commitear código;
esta había que correrla después de **generar datos**, que es un momento distinto y no estaba en
ningún protocolo. Un mordisco que se queda en un archivo que nadie abre no produce una alarma:
produce silencio, y el silencio se lee como confirmación.

⚠️ **Y el segundo filo, que es sobre cómo se escriben las pruebas:** aquella prueba decía *«y no
caza nada más: exactamente una»*. Un número pelado **envejece**. Bastó que el mundo grabara una
segunda contradicción de verdad para que la prueba se pusiera roja sin que nada se hubiera roto —
y una prueba que se pone roja por motivos correctos se acaba desactivando por costumbre. Nombrar
los casos conocidos en vez de contarlos conserva la vigilancia y sobrevive al tiempo.

**Dónde muerde fuera de aquí:** todo lo que se llame *linter*, *sanity check* o *auditoría
nocturna*. La pregunta útil no es «¿existe?» ni «¿pasa?», sino **«¿quién lo corre, cuándo, y qué
pasa cuando sale rojo un martes?»**. Y si el disparador es *«después de que se generen datos
nuevos»*, tiene que estar escrito en el protocolo — porque no coincide con el momento en que
alguien corre las pruebas.

---

### LM.71 — Una consecuencia no puede ir delante de su causa: el detector nuevo enterró el motivo verdadero

Un especialista se quedó sin presupuesto **a mitad** de una tarea encadenada de tres pasos. Se
paró donde pudo, y su paquete de datos quedó incompleto y desalineado con lo que se le había
pedido — **porque se había parado**. La capa de arriba tenía dos comprobaciones: una nueva, que
miraba si la respuesta correspondía a la pregunta, y otra vieja, que miraba por qué había fallado.
La nueva iba primero, con un razonamiento que parecía sólido: *«si la respuesta no corresponde a
la pregunta, lo demás no vale»*.

El resultado fue que arriba subió *«no corresponde»* cuando la verdad era *«se quedó sin dinero»*,
y el modelo lo repitió palabra por palabra al usuario final. **La causa que llegó era falsa**, y
era exactamente el agujero que se había tapado la sesión anterior — reabierto por el arreglo de la
mañana siguiente.

🔑 El razonamiento era correcto **para un trabajo terminado**. En uno interrumpido, la
discrepancia no es la causa del fallo: **es el rastro de haberse interrumpido.** El orden de dos
comprobaciones no es un detalle de estilo — decide **qué explicación se lleva el que pregunta**, y
la primera que dispara se convierte en la versión oficial de lo ocurrido.

⭐ **La regla que queda:** antes de poner una comprobación por delante de otra, pregúntate si puede
dispararse *como efecto* de lo que la otra detecta. Si puede, va detrás. Un diagnóstico que se
adelanta a su propia causa produce informes que suenan precisos y son mentira.

📌 Y el corolario incómodo: **un arreglo puede reabrir el que tiene al lado.** El de ayer hacía que
la causa cruzara la frontera; el de hoy la interceptó antes de que cruzara. Ninguna prueba de las
existentes lo vio, porque cada una vigilaba su mitad. Sólo apareció al **pagar una corrida
completa** y leer lo que el modelo dijo al final.

**Dónde muerde fuera de aquí:** cualquier cadena de validadores, middlewares o *health checks*
donde el primero que falla escribe el mensaje de error. Los fallos derivados suelen ser más fáciles
de detectar que los originales —son más ruidosos— y por eso tienden a colocarse primero. Ordena por
**causalidad**, no por facilidad de detección.

---

### LM.72 — Un verificador que sólo ve el último paso no puede juzgar una tarea de varios

El paquete de datos de un especialista se llenaba recorriendo lo que había pasado por el harness, y
cada herramienta **sobrescribía** lo anterior. Con una tarea de un solo paso el resultado es
correcto y nadie lo nota. Con una tarea encadenada —*«convierte A a B, ese resultado a C, y ese a
D»*— el paquete acababa describiendo **el último tramo**: el final del camino en vez de la pregunta.

Lo caro es lo que vino después: el verificador que comprobaba *«¿responde a lo que se preguntó?»*
—escrito esa misma mañana, y correcto— **gritó sobre un trabajo impecable**. El especialista había
hecho exactamente lo que se le pidió. El falso positivo era del mismo tipo que el defecto que
aquel verificador venía a cazar: uno decía «completo» sin ser correcto, el otro dice «incorrecto»
sin que nadie haya mentido.

🔑 La corrección fue elegir **el primero** en vez del último: el primer paso es el que responde a lo
que se preguntó; los demás son trabajo derivado. Y «el primero» tiene que significar **el primer
acierto**, no la primera línea, para que un intento fallido seguido de uno bueno siga contando.

⚠️ **Y el precio se dice entero, no se esconde:** un paquete de un solo renglón describe bien la
primera conversión y **sigue sin contar la cadena**. Fingir que sí es lo que hacía la versión
anterior. Los pasos intermedios viven en el registro, y el día que haya que juzgarlos hará falta
otra forma — una lista, no un renglón.

**Dónde muerde fuera de aquí:** todo resumen de una traza multi-paso en un objeto plano —el «último
estado» de un pedido, de un despliegue, de un flujo de trabajo. La pregunta que hay que hacerle a
ese objeto es **«¿esto describe la petición o lo último que pasó?»**, y muy a menudo describe
lo segundo mientras todo el mundo lo lee como lo primero.

---

### LM.73 — El gasto no se pierde por gastarse mal: se pierde por no volver por donde se cuenta

Un especialista que revienta a media faena ya no tumbaba al programa que lo llamó: había un
`except` en la costura y hacía su trabajo. Lo que nadie miró es que la función que revienta **no
devuelve**, y que todo el apunte contable —lo gastado, las llamadas, los tokens, la ficha en el
detalle— estaba escrito **después** de esa devolución. Medido: **$0,004000 gastados de verdad,
$0,000000 en el libro.**

🔑 El dinero ya había salido. Las llamadas se hicieron y se cobraron. Lo que faltaba no era
controlar el gasto: era **volver a pasar por la caja**. Un fallo que sale por una puerta distinta a
la del éxito se lleva consigo todo lo que se apuntaba en la puerta del éxito, y no deja rastro de
haberlo hecho — porque el rastro también se apuntaba ahí.

⭐ La corrección es la misma que ya existía para un caso y no se había generalizado: **el fracaso
vuelve con la misma forma que el éxito**, un valor de retorno y no una excepción. Y el comentario
que había encima de la única excepción contemplada llevaba dos versiones diciendo *«esto devuelve
su fracaso como dato»* — era verdad **para ese caso y para ningún otro**, y el comentario no lo
distinguía.

**Dónde muerde fuera de aquí:** cualquier métrica, factura, contador o traza que se escriba después
de la llamada que puede fallar. La pregunta que lo destapa es **«si esto revienta a la mitad, ¿qué
línea de contabilidad no llega a correr?»** — y se responde leyendo, no midiendo.

---

### LM.74 — La ausencia no contradice a nadie

Un auditor de estructura caza mentiras **cruzando dos datos que no pueden ser ciertos a la vez**:
este apunta a un padre que no existe, este dice estar en el escalón 2 y su padre en el 7, esta rama
se muerde la cola. Cinco comprobaciones, todas de la misma familia, todas correctas.

Ninguna podía ver un tramo que **se abrió y no cerró**. El registro que deja un proceso que muere a
media faena es impecable para las cinco: el padre existe, el escalón cuadra, la corrida es la
misma, no hay ciclo. Medido antes de escribir la comprobación: **1 apertura, 0 cierres, 0 quejas.**

🔑 Es `LM.66` girado del revés, y es peor. Aquella decía que un dato que nadie puede desmentir no es
correcto, es **no comprobable**. Aquí no hay dato ninguno: **lo que falta no puede contradecir a
nada**, y un auditor construido entero sobre contradicciones es estructuralmente ciego a las
ausencias. No es un olvido del que lo escribió — es una consecuencia de cómo caza.

📌 Y la comprobación que lo tapa se escribe **en una sola dirección**: una apertura sin cierre es un
defecto; un cierre sin apertura, muy a menudo, es legítimo. Denunciar los dos lados por simetría es
inventarse un defecto, que es exactamente el falso positivo de `LM.72`.

**Dónde muerde fuera de aquí:** todo *health check*, validador o reconciliación que compare campos
entre sí. Pregúntale **«¿qué le pasa a esto cuando el dato simplemente no está?»**, y muy a menudo
la respuesta es: nada, y sale verde.

---

### LM.75 — Un plazo que nadie decidió no es un plazo: es un residuo

Un especialista que se demora tenía un tope. Era cierto y era comprobable: 5 vueltas × 3 intentos ×
30 s de timeout, más las esperas del reintento, daban **490 segundos — 8,2 minutos**. Nadie lo
había escrito nunca, porque no era una decisión: era la **consecuencia aritmética** de tres
constantes elegidas en tres momentos distintos por tres motivos que no tenían nada que ver con el
tiempo total.

🔑 Un límite que sale de multiplicar otras cosas **no se puede discutir, ni ajustar, ni defender**,
porque nadie sabe que existe. El día que hace falta cambiarlo, se cambia una de las tres constantes
por otro motivo y el tope se mueve solo, sin que nadie lo note.

⭐ Y al ponerle un plazo de verdad, el número salió **de un dato y no de una intuición**: 99
ejecuciones ya pagadas daban mediana 2,28 s, p90 5,73 s y peor caso 17,94 s. El plazo se puso en
**5× el peor caso jamás visto** — o sea, un freno que no puede morder a uno legítimo — y aun así
5,4 veces por debajo del residuo. ⚠️ **Aquí sí se elige por arriba a propósito**, y es la otra cara de lo que
costó la sesión anterior: allí un techo dimensionado con el p90 era el precio equivocado **para un
instrumento de medida**, porque le perdonaba la vida justo al que se quería ver ahogarse. Un freno
no es un instrumento: **equivocarse por arriba en un freno sólo cuesta espera.** El mismo número es
correcto en un papel y ciego en el otro, y lo que hay que saber es en cuál de los dos estás.

📌 Y su límite se dice entero: ese plazo corta **entre pasos**, no dentro de uno. Lo que mata es la
**suma** — que era justo lo que no tenía dueño.

**Dónde muerde fuera de aquí:** todo tiempo de espera que sea el producto de reintentos ×
*timeouts* × pasos. Escríbelo como número una vez y casi siempre asusta.

---

### LM.76 — Una advertencia con la lista incompleta no avisa a medias: tranquiliza

Se escribió una regla —*«un script que gasta no puede gastar por defecto»*— después de tirar
$0,087297 por correrlos en pelado. La regla venía con la lista de los archivos que la incumplían.
La lista nombraba **dos** de **cuatro**.

Al día siguiente, comprobando otra cosa, se corrió uno de los dos que faltaban y la factura volvió a
llegar. La regla estaba escrita, se había leído esa misma mañana, y **no protegió** — porque el que
la leyó buscó su archivo en la lista, no lo encontró, y concluyó lo razonable: que el suyo era de
los seguros.

🔑 Una lista de excepciones se lee **como si fuera exhaustiva**, siempre, aunque nadie lo prometa.
Media lista no protege la mitad de los casos: protege esos y **desprotege activamente el resto**,
porque convierte la duda en una falsa tranquilidad. **Es peor que no tener lista.**

📌 Y el mecanismo concreto que lo hizo invisible merece decirse: una bandera que el programa no
conoce **no da error**. `python X.py --pruebas` en un archivo sin lector de argumentos ignora la
bandera y hace lo suyo — y en pantalla se ve exactamente igual que una suite de pruebas.

**Dónde muerde fuera de aquí:** listas de excepciones, de comandos peligrosos, de rutas sensibles,
de entornos donde no se despliega. O la lista se genera desde la fuente de verdad, o llevará escrito
al lado **cómo comprobar si tu caso está en ella** — nunca sólo los ejemplos que alguien recordó.

---

### LM.77 — No hay bolsillo gratis: una reserva o se descuenta de alguien o hace crecer el total

Un arreglo dejó al harness dando dos órdenes contrarias en dos turnos seguidos: *«esta sí puede
salir bien al segundo intento»* y, cuando el modelo aceptaba, *«es uno de más. No lo reintentes.»*
La salida era obvia —reservar presupuesto para el reintento— y la pregunta real no era esa, sino
**de dónde sale ese dinero**.

Se propusieron dos bolsillos que parecían gratis, y los mató un dato:

- **La bolsa del que coordina**, que reservaba un 25 % y parecía holgada. Medida contra diez
  corridas pagadas, su sobrante real era **0,47 raciones**. No llegaba, y prestarla dejaba al que
  responde de la factura con $0,000001.
- **Media ración para el reintento.** De 57 ejecuciones pagadas, sólo 12 cabían en media ración:
  el reintento habría muerto por presupuesto el **79 %** de las veces. Y morir por presupuesto
  produce *«no lo reintentes»* — o sea, **fabricar una tercera orden contraria para tapar la
  segunda**. Un compromiso que dobla el problema no es un compromiso.

Una ración entera cubría el 93 %. Esa era la única que de verdad reintentaba, y ningún bolsillo
existente podía pagarla.

🔑 **Reservar cuesta, siempre.** «Reservar» suena a prudencia y se lee como si fuera gratis, pero
sólo hay tres sitios de donde puede salir: se lo quitas al que trabaja, se lo quitas al que
coordina, o **haces crecer el total y lo dices**. Los dos primeros son transferencias silenciosas
que el día de la factura nadie sabe explicar. El tercero es el único que deja rastro.

📌 Por eso la reserva acabó siendo una bolsa **aparte**, sumada al total y con nombre propio en el
informe (`reintentos_reservados` / `reintentos_usados`). Meterla como una ración más del mismo
reparto habría tenido un efecto que nadie pidió: la frase que rechaza al de más pasa a hablar de un
reparto para cuatro cuando sólo se pidieron tres. **Un número que se toca por un motivo aparece
diciendo otra cosa en la frase que lo cita.**

⚠️ Y hubo un atajo cómodo que se descartó a propósito: bastaba mandar el fallo pasajero a la frase
del fallo permanente para que dejara de invitar. Habría funcionado, y el modelo habría oído
*«defecto interno nuestro»* — falso. **El consejo puede cambiar con las circunstancias; el
diagnóstico, no.**

**Dónde muerde fuera de aquí:** cuotas, reintentos, *rate limits*, capacidad reservada, colchones de
tiempo, plazas de emergencia. Cada vez que alguien diga «reservamos un poco por si acaso», la
pregunta que falta es **a quién se lo quitamos**, y la respuesta tiene que caber en una línea de la
factura.

---

### LM.78 — Una clave contesta «a quién», y a veces la pregunta era «cuántas veces»

El libro del reparto guardaba `entregados[nombre] = trozo`. Correcto durante todo el curso, porque
cada nombre pedía exactamente una vez. El día que se permitió un reintento, el mismo nombre pidió
dos veces: salieron cuatro raciones de la caja y quedaron **tres** apuntadas. **$0,007422
desaparecidos, sin excepción, sin aviso y sin nadie protestando.**

Es `LM.73` en el mismo sitio —el dinero no se pierde por gastarse mal, se pierde por no volver por
donde se cuenta— pero con una vuelta más: aquí el registro **sí** se ejecutó. Lo que falló es que la
estructura elegida no tenía sitio para el segundo dato. Un diccionario por nombre es una afirmación
callada: *«esto ocurre una vez por nombre.»* Nadie la escribió y nadie la revisó el día que dejó de
ser cierta.

🔑 **Un cambio de política puede invalidar una estructura de datos sin tocar ni una línea de ella.**
El defecto no estaba en el código nuevo ni en el viejo: estaba en la costura, y por eso ninguna
prueba de ninguno de los dos lados lo veía.

📌 Lo que sí lo cazó fue el número que se comprueba por dos caminos: *repartido + guardado == total*.
No se descubrió leyendo la línea culpable —se leyó cincuenta veces sin ver nada— sino porque esa
igualdad dejó de cumplirse. **Un invariante sirve precisamente el día que el defecto es invisible a
la vista.**

⚠️ Y la razón de que llevara ahí sin morder: las pruebas pedían raciones con nombres siempre
distintos —`usd`, `eur`, `cad`, y veinticuatro `w0..w23` en la prueba de hilos—. Ninguna de las
cincuenta y tantos pedía **dos veces lo mismo**. El caso no estaba escondido: estaba **fuera del
campo de visión del instrumento**, que es distinto y bastante peor.

**Dónde muerde fuera de aquí:** cualquier acumulador indexado por identidad —gasto por usuario,
intentos por sesión, reservas por recurso— el día que llega el primer reintento, el primer duplicado
o el primer reenvío. Y en las suites: si todos los casos de prueba usan identificadores distintos,
la repetición no es un caso raro, **es un caso que nunca se probó**.

---

### LM.79 — Una red que lo atrapa todo convierte una catástrofe en un `ok=True`

C.4 puso una red de seguridad en la frontera: `except Exception`. Existe por una razón buena y
medida — sin ella, un worker que revienta se lleva por delante a los otros dos, y eso se vio morder.
Lo que C.5 midió es lo que esa misma red hace con un fallo que **no es local**.

Una pelota de agentes —un coordinador que delega en otro coordinador, y ése en otro— bajó 166 capas
y 330 llamadas al modelo. Python acabó quedándose sin pila y lanzó `RecursionError` a profundidad
327. **`RecursionError` es una `Exception`**, así que la red lo atrapó, lo convirtió en un
`tool_result` que decía *«el especialista falló por un defecto interno del programa»*, el modelo
obedeció y cerró su turno, y las 164 capas de encima cerraron **una a una y en verde**. La corrida
de arriba devolvió `ok=True`, `motivo=None` y un texto tranquilo.

🔑 **La red no distingue «se cayó uno de tres» de «el sistema entero se está comiendo a sí mismo».**
Las dos cosas entran por el mismo `except` y salen por el mismo tubo, con la misma forma de dato, y
lo que queda arriba es indistinguible de una corrida sana.

🚨 Y el rastro: **una línea de registro entre 823.** El desastre existió, quedó grabado, y estaba a
la vista de nadie — porque nadie audita un verde (`LM.15`).

📌 De ahí sale la forma del freno de C.5, y es una decisión de diseño, no una preferencia: **el freno
devuelve un diccionario, no lanza una excepción.** Una excepción lanzada dentro de la frontera se la
come la propia red que hace posible el problema. Se midió el contrafactual: el mismo corte, en el
mismo sitio, cambiando `BaseException` por `Exception` — con `BaseException` el aviso sale; con
`Exception` la corrida termina diciendo que todo fue bien.

**Dónde muerde fuera de aquí:** cualquier `catch (Exception e) { log; continue; }` en un bucle de
reintentos, en un consumidor de cola, en un `for` sobre registros. La pregunta que hay que hacerle a
cada uno es **de qué tamaño es el fallo que estoy tragando** — y si la respuesta es «no lo sé», la
red no es una red: es una venda.

---

### LM.80 — Un freno que muerde por la razón equivocada entrega el diagnóstico equivocado

La misma pelota, con el presupuesto repartido de C.2 encendido, murió en **2 capas** en vez de 166.
El freno funcionó: paró, paró pronto y paró barato. Y cerró con `motivo="presupuesto"`.

Eso es verdad y es una mentira a la vez. Es verdad que se acabó el dinero. Es mentira lo que ese
motivo da a entender: *el encargo era caro*. El encargo no era caro — **había un bucle**, y el dinero
sólo fue el primero que se rompió.

🔑 **De un freno sobrevive el diagnóstico, no la parada.** La parada dura un instante; el motivo se
escribe en el registro, sube al modelo, entra en el informe y es lo único sobre lo que alguien
decidirá mañana. Un freno correcto con un motivo impreciso deja al siguiente lector resolviendo el
problema que no era.

⚠️ **Y el adjetivo hay que medirlo, no suponerlo.** La apuesta sellada decía que el consejo deducido
—«dale más presupuesto»— era «el peor posible». Se midió obedeciéndolo: ×10 llevó de 2 capas a 4;
×100, a 5; **×1000, a 7**. El reparto parte el dinero en cada escalón, así que el dinero frena **como
un logaritmo**: nunca deja que una pelota se dispare. La apuesta acertó en lo falsable —para, y con
motivo falso— y **exageró en el adjetivo**. Se deja escrito con el número al lado.

📌 El corolario útil: **el presupuesto sólo frena si se REPARTE hacia abajo.** Con el tope por pieza
de A.2 —cada capa estrenando su propio tope— la misma pelota llegó a 40 capas sin una sola queja. Un
tope que cada capa vuelve a estrenar no es un tope del sistema: es un tope de cada uno.

**Dónde muerde fuera de aquí:** timeouts, cuotas, límites de memoria, `max_retries`. Cuando uno de
ésos corta, la pregunta no es «¿paró?» sino **«¿está contando lo que se rompió?»**. Si no, el
incidente se archivará bajo el nombre del testigo y no bajo el del culpable.

---

### LM.81 — Un ajuste que no viaja hacia abajo se queda en quien lo escribió

El laboratorio de C.5 tenía dos topes configurables —cuántas capas se permiten y dónde corta el
experimento— y los recibía como argumentos de la función frontera. Se veía bien y era ciego: **quien
llama a una herramienta no es quien la configuró, es el bucle del agente**, y ése le pasa exactamente
los argumentos que el modelo pidió. En cuanto la corrida bajaba una capa, los topes volvían a su
valor por defecto. Un tope configurado arriba que no cruza la frontera **no es un tope: es una
variable local con nombre de freno.**

🔑 Y cómo se cazó importa más que el fallo: **dos experimentos distintos dieron el mismo número.** El
segundo existía justamente para dar otro —40 capas, profundidad 78, el mismo corte, las mismas 40
llamadas—. Es `LM.15` con otra cara: el instrumento ciego no dio silencio, **dio la misma cifra dos
veces, que se lee como confirmación en vez de como avería.**

⚠️ La misma sesión produjo la versión pequeña del mismo bicho, en la báscula: se midió «cuántos
escalones cuesta una capa» dividiendo profundidad entre capas, y salió **1,5**. No es un número de
escalones: es la media entre un salto real de 2 y una cola suelta. **El cociente contestaba una
pregunta parecida a la que se hacía**, y por eso el resultado salió creíble. Lo cazó parecer raro, no
una prueba — que es `LM.17` otra vez.

📌 Y de ahí el dato que sí vale, medido restando posiciones: **una capa de agente cuesta DOS escalones
de `profundidad`** —la herramienta y la capa—. O sea que el campo `profundidad` de C.1, que existe
para LEER el árbol después, **no sirve para DECIDIR ahora** sin traducirlo. Cuarenta capas dan
profundidad 78. Un tope escrito contra `profundidad` permite capa y media.

**Dónde muerde fuera de aquí:** *feature flags*, niveles de log, `dry_run`, límites de gasto — todo lo
que se enciende en la capa de entrada y tiene que seguir encendido tres llamadas más abajo. Y en las
mediciones: **cuando dos experimentos que deberían diferir coinciden, el resultado no es una
confirmación — es la primera señal de que el instrumento no está conectado.**

---

### LM.82 — Una tabla de precios equivocada no descuadra nada: escala la factura entera

C.6 midió qué pasa cuando las dos capas dejan de compartir modelo, y la contabilidad del nivel 8
—cinco bloques midiendo dólares— siguió facturando al precio de una sola. El error se pudo poner en
un número: **5,0000000000×**, y la corrida pagada lo confirmó en factura real, $0,024075 donde el
harness de ayer habría dicho $0,004815.

🔑 **Y el hallazgo no es el factor: es que la mentira sale LIMPIA.** Los tres modelos del catálogo
tienen la salida a 5× la entrada, así que tarifar mal **multiplica todo por una constante**. Las
partes siguen sumando el total, el árbol suma hacia arriba lo mismo que el auditor suma en plano, y
todos los cuadres internos salen verdes. **Un error que respeta la aritmética no se puede cazar con
aritmética.**

⚠️ Es `LM.66` del revés y hay que decirlo con esas palabras. Allí un segundo testigo desmintió al
primero **porque los dos caminos eran independientes**. Aquí los dos caminos comparten la fuente del
error, así que **confirman la mentira en coro**. Antes de fiarse de un cuadre, la pregunta no es
«¿coinciden?» sino **«¿de dónde saca cada uno su dato?»** — dos cálculos que leen la misma tabla son
un testigo, no dos.

📌 El corolario del freno: `PRESUPUESTO_ORQ_USD` no hubo que tocarlo al cambiar de modelo, y el
motivo es **la unidad** — está escrito en dólares, así que el precio ya va dentro del número; un tope
en tokens habría que recalcularlo con cada modelo. **La unidad de un freno decide si viaja o no.**
Pero ese mismo techo se compara contra un gasto que salía de la tabla mala: habría visto un 9 % donde
había un 46 %. **Un freno correcto conectado a un instrumento ciego no es medio freno: es ninguno.**

**Dónde muerde fuera de aquí:** cualquier constante de configuración leída una vez al importar —
tarifas, husos horarios, tipos de cambio, tasas de impuesto, factores de conversión. Mientras haya un
solo valor en juego, la constante y el parámetro dan lo mismo y nadie nota la diferencia. **El día
que hay dos, uno de los dos empieza a mentir y no tiene forma de saberlo.**

---

### LM.83 — Un campo se graba si es una salida; lo que se PIDIÓ no queda escrito en ninguna parte

La apuesta de C.6 era que el registro no podría decir, después, qué modelo hizo cada llamada. Salió
exacta: **0 de 191 líneas**. Y al buscar el porqué apareció algo mejor que la apuesta.

En C.1 (`LM.68`) el tercer testigo **ya estaba grabado** y no hubo que añadir nada. Aquí no había
nada que leer. La diferencia no es suerte ni descuido: **el registro guardaba SALIDAS** —lo que trajo
una herramienta, lo que contestó el modelo, cuántos tokens costó— **y el modelo es una ENTRADA de la
petición.** De la petición no se guardaba nada.

🔑 Un registro construido mirando resultados documenta perfectamente **qué pasó** y no puede decir
**bajo qué condiciones pasó**. Y las dos preguntas se parecen lo suficiente como para que nadie note
que solo una tiene respuesta — hasta el día en que las condiciones cambian.

📌 La prueba práctica, y es de un minuto: coge una línea de tu registro y pregúntale *«¿con qué
ajustes se hizo esto?»*. Modelo, versión, límites, banderas, quién configuró. Si la línea no lo dice,
tu registro sirve para depurar y **no sirve para comparar dos corridas**, que es para lo que se
guardan los registros a largo plazo.

**Dónde muerde fuera de aquí:** versión del binario, commit desplegado, `feature flags` activos,
zona de la máquina, límites en vigor. Todo eso es entrada, todo eso cambia, y **casi ningún registro
lo escribe** porque en el momento de escribirlo parecía obvio.

---

### LM.84 — Un experimento cuyo resultado nulo no distingue dos causas todavía no ha medido nada

La segunda mitad de la apuesta 4 predecía que bajar el esfuerzo de `high` a `low` ahorraría poco.
Salió **0,0 %** — mismo coste, mismos tokens de salida hasta la unidad. La apuesta gana en el papel, y
aun así se dejó **sin resolver**, a propósito.

El motivo: un 0 % es compatible con dos mundos distintos. *«El parámetro llegó y no tenía nada que
recortar»* —el turno medido era un despacho puro, sin razonamiento— y *«el parámetro llegó y no hizo
nada»*. El experimento no tiene forma de separarlos, así que **el número confirma la predicción sin
enseñar por qué**.

🔑 **La pregunta que salva un resultado nulo no es «¿salió lo que esperaba?» sino «¿qué otra causa
produciría este mismo cero?»**. Si hay más de una y no puedes descartarlas, lo que tienes es una
coincidencia con forma de dato — y una coincidencia a favor es más peligrosa que una en contra,
porque nadie la va a auditar (`LM.15`).

📌 Lo que sí quedó probado, y por separado: el parámetro **existe y la API lo lee** — pedírselo a
`claude-haiku-4-5` devuelve un **400** con el motivo escrito, y ese rechazo **no se factura**.
Comprobar la mitad mala de una trampa puede salir gratis; lo que se paga es el **control**, o sea la
celda que demuestra que el instrumento funciona cuando debería. **Un experimento con una sola celda
no distingue la hipótesis del instrumento.**

**Dónde muerde fuera de aquí:** cachés que «no mejoran», índices que «no aceleran», reintentos que
«no ayudan». Antes de archivar un cero, hay que poder decir qué observación distinguiría *«no sirve»*
de *«no se activó»*. Si no la hay, el cero es una nota, no un dato — que es `LM.13` aplicado a una
medición en vez de a un freno.
