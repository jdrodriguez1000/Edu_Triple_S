# Nivel 6c — TypeScript

> **Este nivel no tiene ni un concepto nuevo de agentes.** Cero.
> El bucle, las herramientas, el harness, la memoria, las skills: ya los
> entiendes. Este nivel los dice en otro idioma.

## Por qué existe entonces

Por el nivel 7, donde hay navegador. Y el navegador entiende **un solo**
lenguaje: JavaScript. No entiende Python y no lo va a entender.

TypeScript es **JavaScript con avisos**: el mismo lenguaje, más una capa que
revisa tu código *antes* de correrlo.

📌 **Python no se va a ningún lado.** Tu agente, tus 228 evals y tu harness
siguen en Python. TypeScript entra solo en la capa que el navegador exige.

---

## El mapa del nivel

| Paso | Qué | Cuesta |
|---|---|---|
| **0** | El idioma no corre solo: hay que **compilarlo** | ✅ **$0,00** |
| **1** | Los tipos, con Python al lado | ✅ **$0,00** |
| **2** | `async`/`await` y las promesas | ✅ **$0,00** |
| **3** | El SDK de Anthropic en TS: primera llamada | 💰 centavos |
| **3b** | ¿A dónde se fue la factura? El thinking invisible | ✅ **$0,00** |
| **4** | La herramienta del clima y el bucle agéntico | ✅ **$0,0284** |
| **4b** | ¿De dónde salen los +5 tokens? Las tildes, medidas | ✅ **$0,00** |
| 5 | Los frenos, y medir | centavos |
| 6 | Las lecciones a `LESSONS.md` | $0,00 |

Los tres primeros pasos **no gastan un centavo**: no hay API, solo idioma.

---

# Paso 0 — TypeScript no corre

## La diferencia con Python, en una línea

En Python le entregas tu archivo a la máquina y ella lo ejecuta:

```
python script.py
```

En TypeScript hay **un paso antes**. Tu `.ts` nadie lo ejecuta. Primero se
**traduce** a JavaScript, y lo que corre es la traducción:

```
npx tsc              ← traduce  00_hola.ts  →  dist/00_hola.js
node dist/00_hola.js ← corre la traducción
```

Ese traductor se llama **compilador**, y es `tsc`.

> Es como escribir en español un texto que se va a leer en inglés. Tú escribes
> `.ts`. La máquina lee `.js`. Alguien traduce en el medio.

## Las piezas del proyecto

Un proyecto de TypeScript trae archivos que en Python no existían:

| Archivo | Qué es | Su equivalente en Python |
|---|---|---|
| `package.json` | Qué librerías necesita el proyecto | `requirements.txt` |
| `package-lock.json` | Las versiones **exactas** que se instalaron | *(no teníamos)* |
| `tsconfig.json` | Las reglas del **traductor** | *(no existe)* |
| `node_modules/` | Las librerías descargadas | `.venv/` |
| `dist/` | El JavaScript traducido | `__pycache__/` |

Dos cosas de esa tabla importan:

- **`node_modules/` es el `.venv` de JavaScript.** Se descarga, no se sube a
  Git. Este proyecto minúsculo ya tiene **672 archivos** adentro.
- **`dist/` es resultado, no fuente.** Se regenera entero con `npx tsc`. Los dos
  están en el `.gitignore` de la raíz.

⚠️ Y a diferencia de Python, aquí **el `.venv` es por proyecto**, no compartido.
Es la regla de `node`, no una decisión nuestra.

---

## 🚨 Lo que encontramos montando esto (y no lo esperábamos)

Al probar el ejercicio 1 —pasarle un número a una función que pide texto— salió
el aviso esperado:

```
error TS2345: Argument of type 'number' is not assignable to parameter of type 'string'.
```

Hasta ahí, todo normal. **Pero después corrimos el programa igual, y funcionó:**

```
Hola, Juan
El harness dará máximo 5 vueltas.
Hola, 42          ← el error del que acababa de quejarse
```

`tsc` protestó, **y aun así escribió el `.js`.** Node lo corrió tan tranquilo.

### Por qué

Abre `dist/00_hola.js` y compáralo con el `.ts`. Los tipos **no están**:

```javascript
const nombre = "Juan";              // era: const nombre: string = "Juan"
function saludar(quien) { ... }     // era: function saludar(quien: string): string
```

El traductor los leyó, te avisó con ellos, **y después los borró**. Para
JavaScript, `saludar(42)` es válido: no hay ninguna regla que romper.

> ### 🔑 Los tipos son para ti, no para la máquina.
> Viven **antes** de correr. Cuando el programa arranca, ya no existen.

### Y la lección que se repite en este curso

Ya la viste con los evals en verde que no probaban nada, y con el agente que
decía *"Anotado"* sin anotar:

> **Un aviso que no detiene nada es un aviso que se puede ignorar.**

Por eso `tsconfig.json` trae el **ejercicio 2**: la opción `noEmitOnError`, que
convierte el aviso en un freno de verdad. Con ella, un error deja al proyecto
**sin `.js`**, y entonces no hay nada que correr. Medido: `dist/` ni siquiera se
crea.

---

## Cómo correr esto

Párate en `06c-typescript/` y:

```powershell
npx tsc
node dist/00_hola.js
```

Salida esperada:

```
Hola, Juan
El harness dará máximo 5 vueltas.
```

Si `npx tsc` no imprime **nada**, salió bien. Un compilador contento es callado.

---

## Ejercicios

1. **Rompe el tipo, y no te quedes en el aviso.** En `00_hola.ts`, descomenta
   `console.log(saludar(42))`. Corre `npx tsc` **y después `node`**. Vas a ver
   el error… y vas a ver que imprime `Hola, 42` de todos modos. Ese segundo
   comando es el ejercicio; el primero solo es la mitad.
2. **Convierte el aviso en un freno.** En `tsconfig.json`, descomenta
   `noEmitOnError`. Vuelve a compilar con el error puesto. Confirma que ahora
   **no hay `dist/`**. Decide si la dejas prendida.
3. **Lee la traducción.** Abre `dist/00_hola.js` y busca los `: string` y
   `: number`. Cuenta cuántos quedaron.
4. **Borra `dist/` entero** y vuelve a correr `npx tsc`. Comprueba que se
   reconstruye solo. Eso es lo que significa "resultado, no fuente".
5. Cambia `const nombre` por `let nombre` e intenta asignarle otro valor
   después. Luego hazlo con `const`. ¿Cuál se queja? *(En Python no había
   diferencia: todo era reasignable.)*

---

## Lo que ya sabes

- **TypeScript no se ejecuta: se compila.** `tsc` traduce `.ts` → `.js`, y Node
  corre el `.js`.
- **Los tipos se borran al compilar.** Existen antes de correr, no durante. Son
  para ti, no para la máquina.
- **Por defecto el compilador avisa pero no impide**: escribe el `.js` con
  errores y todo. `noEmitOnError` lo convierte en un freno real.
- `package.json` es el `requirements.txt`, `node_modules/` es el `.venv`, y
  `tsconfig.json` no tiene equivalente en Python: son las reglas del traductor.
- **`dist/` y `node_modules/` no suben a Git**: uno es resultado, el otro es
  descarga.

---

# Paso 1 — Los tipos

**Es lo único de verdad nuevo del idioma.** Funciones, listas, `if`, `for`: todo
eso ya lo sabes de Python con otra ropa. Los tipos no.

Y no los vamos a aprender con ejemplos de juguete. Los vamos a aprender
construyendo **las formas de tu agente**: el mensaje, el rol, el uso de tokens.
Las mismas que llevas 23 sesiones escribiendo en Python como diccionarios
sueltos.

## 1. Casi nunca se escriben

El paso 0 escribía `: string` y `: number` a propósito, para que los vieras. En
el día a día **no se escriben**: el compilador los deduce del valor.

```typescript
const modelo = "claude-opus-5";   // ya sabe que es string
let vueltas = 0;                  // ya sabe que es number
```

Y deducir **no es dejar pasar**. `vueltas = "tres"` sigue sin compilar, aunque
nadie escribió ningún tipo.

> 📌 **Los tipos se escriben en las fronteras** — lo que una función recibe y lo
> que devuelve. Adentro se dejan deducir.

## 2. Las listas son de un solo tipo

| Python | TypeScript |
|---|---|
| `nombres = ["a", "b"]` | `const nombres: string[] = ["a", "b"]` |
| Puede mezclar tipos | Todos del mismo tipo |

`lista.push(42)` en una lista de textos **no compila**. En Python era legal.

## 3. `interface` — ponerle nombre a una forma

Esto es lo que has escrito todo el curso, en Python:

```python
{"role": "user", "content": "¿Qué clima hace en Bogotá?"}
```

Un diccionario suelto. **Nada dice qué llaves debe tener ni de qué tipo.** Si
escribías `"rol"` en vez de `"role"`, te enterabas cuando la API devolvía un
400 — y para entonces ya habías pagado la llamada.

Una `interface` le pone nombre a esa forma, de una vez y para todas:

```typescript
interface Mensaje {
  role: "user" | "assistant";
  content: string;
}

const historial: Mensaje[] = [];
```

## 4. 🚨 La unión: el tipo que Python no tiene

Mira otra vez esa línea:

```typescript
role: "user" | "assistant"
```

Eso **no** dice *"role es un texto"*. Dice algo mucho más estrecho:

> **"role solo puede ser una de estas dos palabras exactas."**

La barra `|` se lee **"o"**. No hay tercera opción.

Y aquí está el punto. En Python, `"assistnat"` era un string perfectamente
válido: el error llegaba de la API, en forma de 400, **después de pagar**.
Aquí llega del traductor, gratis, antes de correr nada — y **medido**, esto es
lo que sale:

```
error TS2820: Type '"assistnat"' is not assignable to type '"assistant" | "user"'.
              Did you mean '"assistant"'?
```

Léelo dos veces: **el compilador te corrigió el typo.** Sabe cuáles son los
valores posibles, así que puede adivinar cuál querías. Ningún error de la API te
va a dar eso nunca.

> ### 🔑 Un tipo no es "de qué clase es el dato". Es **qué valores son legales**.
> Y cuanto más estrecho lo escribas, más errores atrapa gratis.

## 5. El `?` — lo que puede no venir

```typescript
interface Uso {
  inputTokens: number;
  outputTokens: number;
  costoUSD?: number;   // ← puede no estar
}
```

Lo bueno no es poder marcarlo opcional: es que después TypeScript **te obliga a
considerar que falta**. Escribir `uso.costoUSD.toFixed(2)` directo no compila.
El `??` da el valor de respaldo:

```typescript
const costo = uso.costoUSD ?? 0;
```

`undefined` en JavaScript es más o menos el `None` de Python — pero aquí no lo
puedes usar por accidente. **Ese es medio valor del idioma.**

## 6. `any` — la puerta de atrás

`any` significa *"no revises nada aquí"*. Apaga el idioma entero para esa
variable:

```typescript
const dato: any = { role: "cualquier_cosa", content: 42 };
```

Eso compila sin una queja. Vuelve a ser JavaScript.

> 🔴 **Cada `any` es un pedazo de tu programa donde TypeScript dejó de
> trabajar** — y no te avisa que lo apagaste.

Lo vas a ver aparecer solo en el paso 3, cuando llegue JSON de afuera (la
respuesta de la API). Ahí se maneja distinto, y lo veremos entonces.

---

## Cómo correr esto

```powershell
npx tsc
node dist/01_tipos.js
```

Salida esperada (verificada):

```
============================================================
1. Modelo: claude-opus-5, vueltas: 0
2. Herramientas: 2
3. Historial: 1 mensaje(s)
4. Historial ahora: 2 mensajes
5. Tokens: 1200 in / 340 out, costo $0
6. any deja pasar: role="cualquier_cosa"
============================================================
```

## Ejercicios del paso 1

1. **El typo que Python no veía.** Descomenta la línea `const roto` del punto 4.
   Compila y lee el error completo, incluida la última frase. Ese error es el
   400 del nivel 3, pero gratis y antes de correr.
2. **Deducir no es dejar pasar.** Descomenta `vueltas = "tres"` del punto 1.
   Nadie escribió un tipo ahí y aun así se queja. ¿Por qué sabía?
3. **Agrega un tercer rol.** Cambia la unión a
   `"user" | "assistant" | "system"` y mira que ahora `"system"` sí compila.
   Los tipos no son fijos: los decides tú.
4. **Rompe una `interface` por lo que le falta**, no por lo que le sobra: crea
   un `Mensaje` sin `content`. Compara ese error con el del ejercicio 1.
5. **Prueba el veneno.** Cámbiale el tipo a `primerMensaje` de `Mensaje` a `any`
   y repite el ejercicio 1. Comprueba que el typo **ya no se detecta**.
6. Quítale el `?` a `costoUSD` y mira qué se rompe. ¿Se rompe donde esperabas?

---

## Lo que ya sabes del paso 1

- **Los tipos casi nunca se escriben**: se deducen. Se escriben en las fronteras
  (qué recibe y qué devuelve una función).
- **Una `interface` es tu diccionario de Python, pero con la forma declarada.**
  `Mensaje`, `Uso`: las formas que ya usabas, ahora con nombre.
- **Un tipo no dice "de qué clase es": dice qué valores son legales.** La unión
  `"user" | "assistant"` es más estrecha que `string`, y por eso atrapa el typo
  que la API te habría cobrado.
- **El `?` marca lo que puede faltar, y te obliga a manejarlo.** `??` da el
  respaldo.
- **`any` apaga TypeScript** para esa variable, en silencio.

---

# Paso 2 — `async` / `await`

**Aquí es donde Python y TypeScript de verdad se separan.** Los tipos eran
nuevos, pero cómodos. Esto es un cambio de cómo funciona el programa.

## La diferencia, en dos líneas

En Python, esta línea **detiene el programa** hasta que la API responda:

```python
respuesta = client.messages.create(...)   # el programa se queda aquí
```

En JavaScript **nada detiene el programa. Nunca.** Una función que se demora no
devuelve el dato: devuelve un **recibo**, en el acto. Y el programa sigue.

## Por qué es así de raro

Porque JavaScript **nació en el navegador**. Si una llamada de red congelara la
página, se congelaría de verdad: el usuario no podría ni hacer scroll.

Así que JavaScript decidió no congelarse jamás. En vez de esperar, dice:
*"sigue tú, yo te aviso cuando esté."*

Ese recibo se llama **promesa** (`Promise`). No es el dato. Es el compromiso de
que el dato va a llegar.

## 🚨 El error número uno de todo principiante

```typescript
const clima = consultarClima("Bogotá");   // ← falta el await
console.log(clima);
```

Lo que imprime, **medido**:

```
1. Sin await  →  [object Promise]
```

No imprimió el clima. Imprimió el recibo.

Y ahora la parte importante: **no hubo ningún error.** Ni una advertencia. El
programa siguió feliz.

> En un agente esto se ve como *"la respuesta llegó vacía"*, o como
> `[object Promise]` metido dentro de un prompt que sí se paga. **Nadie te avisa.**

Con `await`, la misma llamada:

```
2. Con await  →  Bogotá: 18 °C, nublado
```

Misma función. Misma línea. La única diferencia es esa palabra.

## `async` es contagioso

`await` **solo** se puede usar dentro de una función marcada `async`. Y una
función `async` **siempre** devuelve una promesa, la marques o no.

Es contagioso hacia arriba: si tu función espera algo, quien la llame también
tendrá que esperarla. Por eso el bucle agéntico entero, de arriba abajo, va a
estar en funciones `async`. **No es capricho, es contagio.**

Por eso también el archivo termina así:

```typescript
main().catch((error) => { ... });
```

`main()` devuelve una promesa. Si nadie la mira y algo falla adentro, el error
**desaparece en silencio**. Ese `.catch` es el seguro.

## ⭐ Y entonces lo molesto se vuelve la ventaja

Tres consultas, una detrás de otra — que es lo que hace tu código de Python:

```typescript
const a = await consultarClima("Bogotá");
const b = await consultarClima("Medellín");
const c = await consultarClima("Cali");
```

Las mismas tres, lanzadas a la vez. **Fíjate que no hay `await` arriba**: se
guardan los tres recibos, y el `await` es **uno solo, al final**:

```typescript
const recibo1 = consultarClima("Bogotá");
const recibo2 = consultarClima("Medellín");
const recibo3 = consultarClima("Cali");

const [x, y, z] = await Promise.all([recibo1, recibo2, recibo3]);
```

**Medido en esta máquina:**

| | tiempo |
|---|---|
| En serie | **3.024 ms** |
| En paralelo | **1.007 ms** |
| | **3,0x más rápido, las mismas 3 llamadas** |

> 🔑 **"No bloquear" dejó de ser una molestia y se volvió la ventaja.**
> En Python esto necesita `asyncio` y decisiones; aquí es lo normal del idioma.

## `try` / `catch` — tu nivel 4, en TypeScript

Es el `try/except` que ya conoces, con dos diferencias que importan:

```typescript
try {
  await consultarQueFalla();
} catch (error) {
  const mensaje = error instanceof Error ? error.message : String(error);
  console.log(mensaje);
}
```

**Primera:** lo que atrapas es de tipo `unknown`, no `Error`. Porque en
JavaScript se puede lanzar **cualquier cosa** — un texto, un número, lo que sea.
Así que primero hay que comprobar qué llegó.

**Segunda, y es la peligrosa:** si a la línea del `try` le quitas el `await`,
**el error se escapa del `catch`**. Lo medimos, y el resultado fue peor de lo
esperado: no es que no lo atrape, es que **mata el proceso entero**:

```
Error: APIConnectionError: no se pudo conectar
Node.js v25.8.1
```

El `try/catch` estaba ahí, escrito, correcto. Y no sirvió de nada.

> ### 🔑 Un `try/catch` sin `await` adentro no protege nada.
> El `try` cierra antes de que el error ocurra. Es la versión JavaScript de un
> freno que se ve puesto y no frena — el mismo patrón del *"Anotado"* sin anotar.

## Un detalle que salió montando esto

El primer intento **no compiló**:

```
error TS2591: Cannot find name 'process'.
```

TypeScript **no sabe nada de Node por su cuenta** — el idioma nació en el
navegador, donde `process` no existe. Hubo que agregar `"types": ["node"]` al
`tsconfig.json` para que leyera las descripciones del paquete `@types/node`.

📌 `@types/node` no es código: **son solo las descripciones de tipos** de cosas
que ya existen. Es la biblioteca de instrucciones, no la herramienta.

---

## Cómo correr esto

```powershell
npx tsc
node dist/02_async.js
```

⏱️ **Tarda ~7 segundos a propósito**: está midiendo. Salida verificada:

```
============================================================
1. Sin await  →  [object Promise]
2. Con await  →  Bogotá: 18 °C, nublado
4. En serie   →  3024 ms   (Bogotá…, Medellín…, Cali…)
5. En paralelo → 1007 ms   (Bogotá…, Medellín…, Cali…)
   → 3.0x más rápido, mismas 3 llamadas
6. Atrapado   →  APIConnectionError: no se pudo conectar
============================================================
```

Tus milisegundos van a ser distintos. **La forma no**: serie ≈ 3x paralelo.

⚠️ Este paso **no llama a la API**. El clima es simulado. Cuesta **$0,00** — es
la misma regla del nivel 6b: *lo que puedas simular, no lo pagues*.

## Ejercicios del paso 2

1. **Pon el `await` que falta** en el punto 1 y comprueba que `[object Promise]`
   se vuelve el clima. Luego quítalo otra vez. Que se te grabe cómo se ve.
2. **Rompe el `try/catch`.** Quítale el `await` a `consultarQueFalla()` dentro
   del `try`. El programa **se muere**. Explícate en una frase por qué el
   `catch` no lo salvó.
3. **Cambia las 3 ciudades por 6** en los puntos 4 y 5. Predice los dos tiempos
   **antes** de correr, escríbelos, y después compara. *(Es el ejercicio del
   `count_tokens` del nivel 6b: predecir antes de medir.)*
4. **Haz que una de las tres falle** en `Promise.all` (lanza un error en la de
   Cali). ¿Qué pasa con las otras dos? ¿Se pierden los resultados que sí
   llegaron? Esta respuesta importa para el harness del paso 5.
5. Quítale el `.catch` final a `main()` y haz que algo falle adentro. Compara
   con lo que pasa cuando el `.catch` está.
6. Cambia `dormir(1000)` por tiempos distintos (300, 1500, 800). En paralelo,
   ¿cuánto tarda el conjunto? ¿Manda el más lento o la suma?

---

## Lo que ya sabes del paso 2

- **En JavaScript nada bloquea.** Una función lenta devuelve una **promesa** —un
  recibo— en el acto, no el dato.
- **`await` convierte el recibo en dato.** Olvidarlo no da error: da
  `[object Promise]` en silencio.
- **`async` es contagioso hacia arriba.** Por eso el agente entero vivirá en
  funciones `async`.
- **`Promise.all` lanza varias a la vez.** Medido: 3,0x más rápido con las
  mismas llamadas. Lo que era una molestia es la ventaja.
- **Un `try/catch` sin `await` adentro no protege nada** — y no falla callado:
  mata el proceso.
- **TypeScript no conoce Node por su cuenta.** `@types/node` + `"types": ["node"]`.

---

# Paso 3 — La primera llamada 💰

**El primero que cuesta.** Unos centavos.

Es tu `01-primera-llamada/01_hola.py` del nivel 1, dicho en TypeScript. La API es
la misma, la key es la misma, el modelo es el mismo. **Solo cambia el idioma** —
que es exactamente el punto de todo este nivel.

```powershell
npm install @anthropic-ai/sdk dotenv
```

## 1. La key, y una trampa que Python no tenía

En Python tus scripts suben **dos** niveles para encontrar el `.env`:

```python
load_dotenv(Path(__file__).resolve().parent.parent / ".env")
#                                    └── script → nivel → raíz
```

Aquí hay que subir **tres**. Y la razón es la del paso 0:

> **Este archivo no es el que corre.** Corre su traducción, que vive en `dist/`.

```
.ts  →  06c-typescript/03_primera_llamada.ts        ← lo que escribes
.js  →  06c-typescript/dist/03_primera_llamada.js   ← lo que CORRE
```

El programa arranca un nivel más abajo, así que la ruta también:

```typescript
const RUTA_ENV = path.resolve(__dirname, "..", "..", ".env");
//                                        dist → 06c → raíz
```

> 🔑 **En TypeScript la ruta se calcula desde donde corre el `.js`, no desde
> donde vive el `.ts`.** Es la primera consecuencia práctica de que el idioma se
> compile.

Lo demás es igual que siempre: la key **nunca** se escribe en el código, y nunca
se imprime completa — el script solo muestra los últimos 4 caracteres.

## 2. El cliente

| Python | TypeScript |
|---|---|
| `client = Anthropic()` | `const client = new Anthropic()` |

El `new` es la única diferencia. Los dos leen `ANTHROPIC_API_KEY` del entorno
por su cuenta.

## 3. La llamada — y el `await` del paso 2

```typescript
const respuesta = await client.messages.create({
  model: "claude-opus-5",
  max_tokens: 2000,
  messages: [{ role: "user", content: "..." }],
});
```

Todo el paso 2 fue para esa palabra. Sin el `await`, `respuesta` sería un recibo
y todo lo que sigue reventaría — **sin dar error**.

## 4. 🚨 Aquí se paga lo que aprendiste en el paso 1

En Python leías el texto directo:

```python
print(respuesta.content[0].text)
```

**Esa línea no compila en TypeScript.** Medido:

```
error TS2339: Property 'text' does not exist on type 'ContentBlock'.
```

¿Por qué? Porque `content` **no es una lista de textos**. Es una lista de
**bloques**, y cada bloque puede ser de varios tipos:

```typescript
type ContentBlock = TextBlock | ThinkingBlock | ToolUseBlock | ...
```

Esa barra `|` es **la unión del paso 1**, esta vez escrita por el SDK en vez de
por ti. TypeScript se niega a darte `.text` de algo que quizá no lo tenga.

**Y tiene razón, porque a ti eso te pasó de verdad.** Nivel 1, sesión 1: pediste
`max_tokens=30` con Opus, los 30 tokens se fueron enteros en el bloque
`thinking`, no hubo bloque `text`, y **la pantalla salió vacía sin ningún
error**. → L1.1, L1.2

La forma correcta es preguntar primero. A eso se le llama **estrechar**:

```typescript
for (const bloque of respuesta.content) {
  if (bloque.type === "text") {
    console.log(bloque.text);   // aquí, y solo aquí, .text existe
  }
}
```

> ### 🔑 El aviso no es una molestia: es el bug del nivel 1, atrapado antes de
> ### correr y antes de pagar.

## 5. `usage` y `stop_reason`

La costumbre de este curso desde el nivel 1. Y el costo se **calcula**, nunca se
escribe fijo — es la lección L1.13, la del *"Haiku cuesta 5x menos"* que era
mentira:

```typescript
const costo =
  (respuesta.usage.input_tokens  / 1_000_000) * 5 +
  (respuesta.usage.output_tokens / 1_000_000) * 25;
```

---

## Cómo correr esto

```powershell
npx tsc
node dist/03_primera_llamada.js
```

⚠️ **Este sí gasta.** Debe imprimir la confirmación de la key (últimos 4
caracteres), la respuesta del modelo, y después `stop_reason`, tokens y costo.

## Ejercicios del paso 3

1. **Rompe la unión.** Descomenta `console.log(respuesta.content[0].text)` en el
   punto 4 y compila. Lee el error. Es el mismo `TS2820` del paso 1 con otra
   ropa — y esta vez la unión no la escribiste tú, la escribió el SDK.
2. **Revive el bug del nivel 1, gratis.** Baja `max_tokens` a `30` y corre.
   Predice antes: ¿qué va a imprimir el `for`? ¿Qué va a decir `stop_reason`?
   *(Sí, esto cuesta unos centavos — pero es el mismo experimento que te costó
   una sesión entera de confusión en el nivel 1.)*
3. **Quítale el `await`** a `client.messages.create`. ¿Compila? ¿Qué error da, y
   en qué línea? Compáralo con el `[object Promise]` silencioso del paso 2 —
   ¿por qué aquí sí te avisa y allá no?
4. **Cambia el modelo** a `claude-haiku-4-5` y ajusta los dos precios del cálculo
   ($1 entrada / $5 salida por millón). Corre las dos versiones y compara costo
   real. Es tu `03_costo.py` del nivel 1, en TypeScript.
5. **Borra el `.env` de la raíz un momento** (o renómbralo) y corre. Comprueba
   que el mensaje de error dice **la ruta exacta** donde lo buscó. Vuelve a
   ponerlo. *(Un error que no dice dónde buscó no sirve para nada.)*

---

## Lo que ya sabes del paso 3

- **La ruta al `.env` se cuenta desde `dist/`**, no desde el `.ts`. Compilar
  mueve el punto de partida del programa.
- `new Anthropic()` = `Anthropic()`. La key se lee del entorno, nunca del código.
- **`content` es una lista de bloques, no de textos.** `content[0].text` no
  compila: hay que **estrechar** con `if (bloque.type === "text")`.
- **Esa unión es la del paso 1, escrita por el SDK** — y atrapa exactamente el
  bug de pantalla vacía que te costó una sesión en el nivel 1.
- El costo se calcula desde `usage`. Nunca se escribe fijo.

---

# Paso 3b — ¿A dónde se fue la factura? ✅ $0,00

Archivo: `03b_thinking.ts`

El paso 3 dejó una pregunta incómoda: **dos frases costaron 235 tokens de
salida.** Parecía mucho. Este paso la responde **sin gastar un centavo**.

## La herramienta: `count_tokens`

Es un endpoint de la API que **cuenta tokens y no cobra**. No llama al modelo:
solo pasa el texto por el mismo tokenizador que usaría la llamada real.

```typescript
const cuenta = await client.messages.countTokens({
  model: "claude-opus-5",
  messages: [{ role: "user", content: RESPUESTA_QUE_LLEGO }],
});
console.log(cuenta.input_tokens);
```

Es la misma jugada que ganó en el nivel 6b, cuando `count_tokens` predijo los
+849 tokens del menú de skills **antes** de gastarlos.

## El resultado, medido

| | tokens |
|---|---|
| texto que se vio | ~176 |
| cobrado por la API | **235** |
| **pensamiento invisible** | **~59 (25% de la factura)** |

## 🚨 Lo que explica ese 25%

**Opus 5 piensa por defecto.** No escribir el parámetro `thinking` **no lo
apaga**: lo deja en automático (`adaptive`). Esto es un cambio: en Opus 4.8 y
4.7, omitirlo sí significaba no pensar.

Y hay un campo `display` que por defecto vale `"omitted"`: el bloque `thinking`
**llega igual, pero con el texto vacío**. Por eso tu `for` del paso 3 no vio
nada — el bloque estaba ahí, callado. Y cobrado.

Para verlo, se pide explícitamente:

```typescript
thinking: { type: "adaptive", display: "summarized" }
```

- 🔑 **Lo que no se ve también se paga.** El pensamiento se factura dentro de
  `output_tokens`.
- 🚨 **Y muerde donde ya te dolió:** `max_tokens` es el techo de
  **pensamiento + respuesta juntos**. Si lo ajustas al tamaño de la respuesta
  que esperas, el texto se corta a mitad de frase. **Es el bug del nivel 1
  (`max_tokens=30`) con otra cara** — y ahora sabes *por qué* pasó.

## ⚠️ La advertencia del instrumento, pegada al dato

`countTokens` pide un **mensaje completo**, no un texto suelto. Por eso el texto
va envuelto como un turno de usuario — y ese envoltorio mete unos pocos tokens
que no son del texto.

Así que 176 es una **cota alta**: el texto pesa eso o un poco menos, y el
pensamiento invisible es de 59 **o un poco más**.

📌 Un instrumento sin su margen escrito al lado es un número que engaña.

## Cómo correr esto

```powershell
npx tsc
node dist/03b_thinking.js
```

✅ **No gasta nada.** `count_tokens` no cobra.

## Ejercicios del paso 3b

1. **Hazlo visible.** Agrega `thinking: { type: "adaptive", display: "summarized" }`
   a `03_primera_llamada.ts` y añade una rama `if (bloque.type === "thinking")`
   al `for`. Corre. ¿Ahora sí ves el razonamiento? ¿Cambió `output_tokens`?
   *(Cuesta unos centavos.)*
2. **Mide el envoltorio.** Corre `countTokens` con `content: ""` (texto vacío).
   Lo que salga son los tokens de envoltorio. Réstalos de 176: ese es el texto
   de verdad. Gratis.
3. **Predice antes de pagar.** Escribe un prompt nuevo, cuenta sus tokens de
   entrada con `countTokens`, y **anota tu predicción**. Después córrelo de
   verdad y compara con `usage.input_tokens`. ¿Acertaste?

---

## Lo que ya sabes del paso 3b

- **`count_tokens` cuenta gratis.** Es la forma de medir *antes* de pagar.
- **Opus 5 piensa por defecto**, y `display: "omitted"` hace que ese
  pensamiento llegue invisible — pero cobrado dentro de `output_tokens`.
- **`max_tokens` cubre pensamiento + respuesta.** Ajustarlo a la respuesta
  esperada corta el texto.
- **La documentación da el mecanismo; solo medir da la magnitud.** La referencia
  del SDK acertó en *qué* pasaba. El *cuánto* (59, no ~100) solo salió al medir.

---

# Paso 4 — El bucle agéntico 💰

Archivo: `04_bucle.ts`

Es tu `03-primer-agente/02_bucle.py` del nivel 3, dicho en TypeScript. **Misma
herramienta, mismas 3 preguntas, misma lógica.** Ponlos lado a lado: son el
mismo programa.

> ⚠️ **Se escribió a mano a propósito.** El SDK trae un `toolRunner` que hace el
> bucle solo — pero está en beta, y sobre todo: si nunca escribiste el bucle, no
> tienes con qué diagnosticar el día que se porte raro. Es la misma razón por la
> que aquí escribiste los evals a mano antes de tocar una librería.

## El bucle, en 3 movimientos (idénticos a los de Python)

```
vuelta 1 → stop_reason = "tool_use"    el modelo PIDE
           ...corre TU código...
vuelta 2 → stop_reason = "end_turn"    el modelo RESPONDE con el dato
```

Y las tres reglas del nivel 3 siguen intactas:

1. **Guarda `respuesta.content` ENTERO** en el historial. Si le quitas los
   bloques `tool_use`, la API rechaza el mensaje siguiente. Y desde el paso 3b
   sabes que ahí viaja también un bloque `thinking` invisible — que también hay
   que devolver.
2. **Cada resultado lleva su `tool_use_id`.** Es el ticket.
3. **Todos los resultados van en UN solo mensaje**, con `role: "user"` — aunque
   no los escribiste tú. Para la API, todo lo que *entra* al modelo es `user`.

## 🚨 Lo nuevo: `input` es de tipo `unknown`

En Python leías el parámetro directo:

```python
funcion(**bloque.input)      # bloque.input era un diccionario, y ya
```

En TypeScript, el SDK declara el bloque así:

```typescript
interface ToolUseBlock {
  id: string;
  name: string;
  input: unknown;      // 🚨 aquí
  type: "tool_use";
}
```

Y esa línea **no compila**. Medido:

```
error TS18046: 'bloque.input' is of type 'unknown'.
```

### `unknown` no es `any`

Ya conociste `any` en el paso 1: decía *"no revises nada aquí"*. Apagaba el
idioma. `unknown` dice algo distinto y más honesto:

> **"aquí hay un dato y NO SÉ QUÉ ES."**

Y no te deja tocarlo hasta que compruebes qué es. `any` te deja pasar en
silencio; `unknown` te frena.

Compara los dos errores que llevas medidos:

| Paso | Error | Lo que sabía el compilador |
|---|---|---|
| 3 | `TS2339: Property 'text' does not exist` | Sabía qué había, y que `.text` no estaba |
| 4 | `TS18046: is of type 'unknown'` | **No sabe ni qué hay** |

### ¿Por qué tiene razón?

Porque `input` **lo escribió el modelo, no tú**. Tu `input_schema` es una
*petición*, no una garantía. Puede llegar `{}`. Puede llegar `{"ciudad": 42}`.
Puede llegar `{"ciuadd": "Bogotá"}` con el typo del modelo.

> ### 🔑 Los tipos protegen lo que TÚ escribes.
> Donde entra algo del mundo —el modelo, un archivo, internet— los tipos se
> acaban, y empieza la comprobación **en tiempo de ejecución**.

Y eso ya lo sabías hacer: son tus **10 frenos** de `herramientas.py` en el nivel
5b. La novedad no es la idea. Es que aquí **el compilador no te deja olvidarla**.

### Comprobar de verdad: 3 preguntas

```typescript
function leerCiudad(input: unknown): string | null {
  if (typeof input !== "object" || input === null) return null;  // 1. ¿objeto?
  if (!("ciudad" in input)) return null;                          // 2. ¿la llave?
  const valor = (input as Record<string, unknown>).ciudad;
  if (typeof valor !== "string") return null;                     // 3. ¿texto?
  return valor;
}
```

⚠️ El `input === null` no sobra: en JavaScript `typeof null` es `"object"`.
Es un defecto famoso del idioma, de 1995, que nadie se atrevió a arreglar.

Y si devuelve `null`, el agente **no se cae**: le manda al modelo un mensaje de
error que puede leer. Es la lección del nivel 5b otra vez — *el mensaje de error
es la instrucción de reintento que le das al agente*.

## Cómo correr esto

```powershell
npx tsc
node dist/04_bucle.js
```

💰 **Este gasta**: 3 preguntas × 2 llamadas, con Opus 5. Unos centavos.

Debes ver, por cada pregunta, dos líneas `[vuelta N]` y en medio el `→ ejecuté`.
La tercera pregunta (Tokio) no está en el diccionario: mira **qué hace el agente
con el error** en vez de morirse.

## Ejercicios del paso 4

1. **Rompe el `unknown`.** Descomenta la línea del punto 3 y compila. Lee el
   `TS18046`. Compáralo con el `TS2339` del paso 3: ¿qué sabe el compilador en
   cada caso, y qué no?
2. **Fuerza la basura.** Cambia `leerCiudad` para que devuelva siempre `null`.
   Corre. ¿Se cae el agente? ¿Qué hace el modelo cuando lee ese error? ¿Vuelve a
   intentar, se rinde, o inventa? *(Cuesta unos centavos y enseña mucho.)*
3. **Quita el freno.** Cambia `leerCiudad(bloque.input)` por
   `(bloque.input as { ciudad: string }).ciudad`. **Compila** — el `as` es la
   otra puerta de atrás del idioma. Pregúntate: ¿qué pasa el día que el modelo
   mande `{}`? *(Este es el ejercicio importante del paso.)*
4. **Cuenta las llamadas.** Suma los tokens de las 6 vueltas y compáralo con lo
   que te costó el paso 3 (una sola llamada, 53 in / 235 out). ¿Cuántas veces
   más caro es un agente que un chat?
5. **Añade una ciudad** al diccionario y pregunta por ella. Fíjate en que **no
   tocaste el bucle**: el bucle no cambia, cambian las herramientas.
6. **Baja `maxVueltas` a 1** y corre. ¿Qué devuelve? ¿Por qué ese límite no es
   un adorno?

---

## Lo que ya sabes del paso 4

- **El bucle agéntico es el mismo en los dos idiomas**: pedir → ejecutar →
  devolver con `tool_use_id` → repetir, guardando `content` entero.
- **`input` llega como `unknown`**, porque lo escribe el modelo, no tú.
- **`unknown` ≠ `any`.** `any` apaga el idioma en silencio; `unknown` te obliga
  a comprobar antes de tocar.
- **Los tipos se acaban en las fronteras.** Lo que entra de afuera se valida en
  tiempo de ejecución — que es justo lo que hacen tus frenos del 5b.
- **Un error de herramienta se devuelve como texto, no como excepción.** Un
  agente que lanza excepciones se muere; uno que devuelve texto se recupera.

---

# Paso 4b — ¿De dónde salen los +5 tokens? ✅ $0,00

Archivo: `04b_tildes.ts`

## La corrida real del paso 4

| | |
|---|---|
| entrada | **3.050** tokens |
| salida | **525** tokens |
| **costo** | **$0,028375 USD** |

Las tres preguntas hicieron `tool_use` → `end_turn`, sin excepción. Y **Tokio se
recuperó**: la función devolvió texto en vez de reventar, el modelo lo leyó, y
contestó ofreciendo las tres ciudades disponibles. Fue la respuesta **más larga
de las seis** (149 tokens de salida) — el error lo hizo hablar *más*, no menos.

## Lo primero: el idioma no cambia la factura

El mismo agente, las mismas 3 preguntas, en `03-primer-agente/02_bucle.py`:

| | Python | TypeScript |
|---|---|---|
| entrada | 3.062 | 3.050 |
| salida | 590 | 525 |
| costo | ~$0,030 | $0,028 |

> 🔑 **Los tokens los cuenta la API, no `tsc` ni Python.** Es el mismo agente
> hablando con el mismo modelo, y el recibo lo demuestra.

## 🚨 Pero apareció un +5 que no cuadraba

Comparando las vueltas 1, una a una:

| pregunta | Python | TypeScript | dif |
|---|---|---|---|
| Medellín | 452 | 457 | **+5** |
| Bogotá | 458 | 463 | **+5** |
| Tokio | 452 | 457 | **+5** |

**Exactamente +5 en las tres.** La sospecha: las **tildes**. El archivo de Python
está escrito sin ellas (`Usala`, `algun`, `Bogota`); el de TypeScript sí las
tiene. Pero eso no explicaba por qué el número era *idéntico* en las tres, si las
preguntas cambiaron cada una de forma distinta.

Se midió con `count_tokens`, **gratis**, separando los dos sospechosos:

```
SOSPECHOSO 1 — el menú de herramientas
  menú sin tildes (Python)     : 441
  menú con tildes (TypeScript) : 443
  → diferencia                 : +2

SOSPECHOSO 2 — las preguntas
  Medellín   py=18  ts=21  → +3
  Bogotá     py=24  ts=27  → +3
  Tokio      py=18  ts=21  → +3
```

**Cuadra exacto:** `+2 (menú) + 3 (pregunta) = +5`. El menú aporta un peaje fijo
en las tres, y cada pregunta resultó costar +3 por su cuenta. Sospecha cerrada.

## 🔑 Una tilde no cuesta un token

Y aquí está lo que no se esperaba:

| texto | sitios cambiados | tokens de más |
|---|---|---|
| el menú (`Úsala`, `algún`, `Bogotá`) | **3** | **+2** |
| `¿Me llevo... a Bogotá?` (`¿`, `á`) | **2** | **+3** |

No hay regla de *"una tilde = un token"*. Depende de cómo el tokenizador parta
esa palabra concreta. Es la lección del nivel 1 con otra ropa: **el conteo se
mide, no se deduce.**

## ⚠️ Lo que NO hay que concluir

La tentación es *"escribo sin tildes y ahorro"*. **No.**

Son **+5 sobre 457: un 1,1%.** En la corrida entera, las tildes costaron unos
**$0,00008**. Y el nivel 5 midió lo contrario en la dirección que sí importa: el
prompt en mal español producía **respuestas peores** (el rioplatense, el tú/usted
mezclado). Escribir mal para ahorrar el 1% y pagarlo en calidad es mal negocio.

> ### 🔑 El costo del acento es real, medible y despreciable.
> Lo que vale del hallazgo no es el número: es que ahora sabes que **el texto de
> tu menú de herramientas se paga en CADA vuelta.** Con 3 ciudades da igual. Con
> 20 herramientas descritas en tres párrafos, en un agente de 8 vueltas, la
> descripción es una factura recurrente. *Eso* sí es una decisión de ingeniería.

## Cómo correr esto

```powershell
npx tsc
node dist/04b_tildes.js
```

✅ **No gasta nada.** `count_tokens` no cobra.

## Ejercicios del paso 4b

1. **Mide el envoltorio.** Cuenta un mensaje con `content: "x"` y sin `tools`.
   Ese es el piso. Réstaselo a los 441/443 y tienes el peso real del menú.
2. **Engorda la descripción.** Duplica el texto de `description` en el menú y
   vuelve a contar. Multiplica la diferencia por 6 (las vueltas de la corrida):
   eso es lo que te habría costado ese párrafo de más.
3. **Predice antes de medir.** Escribe una cuarta pregunta con muchas tildes,
   **anota tu predicción** de cuántos tokens pesa, y después cuéntala. *(Es el
   ejercicio del 3b: predecir antes de pagar — aquí ni siquiera se paga.)*
4. **¿Y el nombre de la herramienta?** Cambia `obtener_clima` por un nombre
   larguísimo y cuenta. ¿Pesa el nombre igual que la descripción?

---

## Lo que ya sabes del paso 4b

- **El idioma no cambia la factura**: 3.050 vs 3.062 tokens para el mismo agente.
- **El menú de herramientas se reenvía en cada vuelta.** Su texto es un peaje
  recurrente, no un costo único.
- **Una tilde no cuesta exactamente un token.** No hay regla; hay medición.
- **Un hallazgo del 1% se cierra, no se actúa.** Saber de dónde salen los +5 vale
  mucho; cambiar el código por $0,00008 no vale nada.
