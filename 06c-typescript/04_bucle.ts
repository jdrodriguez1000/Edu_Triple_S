/**
 * 04_bucle.ts — Nivel 6c, paso 4
 *
 * EL BUCLE AGÉNTICO, escrito a mano. Es tu
 * `03-primer-agente/02_bucle.py` del nivel 3, dicho en TypeScript.
 *
 * Misma herramienta (clima inventado), mismas 3 preguntas, misma lógica.
 * Ponlos lado a lado: son el mismo programa. Lo que cambia es que aquí el
 * compilador te obliga a hacer una cosa que Python te dejaba saltarte —
 * y esa cosa es la lección del paso.
 *
 * Corre así:
 *   npx tsc
 *   node dist/04_bucle.js
 *
 * 💰 CUESTA: 3 preguntas × 2 llamadas cada una, con Opus 5. Unos centavos.
 */

import Anthropic from "@anthropic-ai/sdk";
import { config } from "dotenv";
import path from "path";

// La ruta de siempre: TRES niveles, porque corre desde dist/ (paso 3).
config({ path: path.resolve(__dirname, "..", "..", ".env") });

const client = new Anthropic();
const MODELO = "claude-opus-5";

// ══════════════════════════════════════════════════════════════════
//  1. LA FUNCIÓN DE VERDAD
// ══════════════════════════════════════════════════════════════════
// Igual que en Python: el modelo NUNCA la ve ni la ejecuta. Es tu código.
// El clima es inventado a propósito: aquí el protagonista es el bucle.

const CLIMA_FALSO: Record<string, { temperatura_c: number; estado: string }> = {
  bogota: { temperatura_c: 14, estado: "lloviznando" },
  medellin: { temperatura_c: 24, estado: "despejado" },
  cartagena: { temperatura_c: 32, estado: "húmedo y soleado" },
};

function obtenerClima(ciudad: string): string {
  // Quitamos tildes y mayúsculas para que "Bogotá" encuentre a "bogota".
  const clave = ciudad
    .trim()
    .toLowerCase()
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "");

  const dato = CLIMA_FALSO[clave];

  if (dato === undefined) {
    // 🔑 Regla del nivel 3, intacta: NO lanzamos un error.
    // Devolvemos un texto que el modelo pueda LEER y con el que pueda
    // reaccionar. Un `throw` no lo lee nadie.
    return `No tengo datos de '${ciudad}'. Ciudades disponibles: Bogotá, Medellín, Cartagena.`;
  }

  return `${dato.temperatura_c} grados centígrados, ${dato.estado}.`;
}

// ══════════════════════════════════════════════════════════════════
//  2. EL MENÚ que ve el modelo
// ══════════════════════════════════════════════════════════════════
// Fíjate en el tipo `Anthropic.Tool`. En Python esto era un diccionario
// suelto: si escribías "input_shema" te enterabas con un 400 pagado.
// Aquí el typo no compila. Es el paso 1 otra vez, cobrando intereses.

const HERRAMIENTAS: Anthropic.Tool[] = [
  {
    name: "obtener_clima",
    description:
      "Devuelve el clima actual de una ciudad. Úsala siempre que te " +
      "pregunten por el clima, la temperatura o si llueve en algún lugar.",
    input_schema: {
      type: "object",
      properties: {
        ciudad: {
          type: "string",
          description: "Nombre de la ciudad, por ejemplo: Bogotá",
        },
      },
      required: ["ciudad"],
    },
  },
];

// ══════════════════════════════════════════════════════════════════
//  3. 🚨 EL PUNTO DEL PASO: `input` es de tipo `unknown`
// ══════════════════════════════════════════════════════════════════
// En Python escribías esto y ya:
//
//     funcion(**bloque.input)      # bloque.input era un diccionario
//
// En TypeScript el SDK declara el bloque así:
//
//     interface ToolUseBlock {
//       id: string;
//       name: string;
//       input: unknown;      ← 🚨 AQUÍ
//       type: "tool_use";
//     }
//
// `unknown` NO es `any`. `any` decía "no revises nada" (paso 1).
// `unknown` dice algo más honesto: **"aquí hay un dato y NO SÉ QUÉ ES."**
// Y no te deja tocarlo hasta que compruebes qué es.
//
// 🔴 Esta línea NO compila. Medido, esto es lo que sale:
//
//     error TS18046: 'bloque.input' is of type 'unknown'.
//
// Fíjate en la diferencia con el error del paso 3 (`TS2339: Property
// 'text' does not exist`). Allá el compilador SABÍA qué había y sabía
// que `.text` no estaba. Aquí ni siquiera sabe qué hay.
//
// ¿Por qué tiene razón el compilador? Porque `input` lo escribió **el
// modelo**, no tú. Tu `input_schema` es una PETICIÓN, no una garantía:
// puede llegar `{}`, puede llegar `{"ciudad": 42}`, puede llegar
// `{"ciuadd": "Bogotá"}` con el typo del modelo. Es un dato de afuera.
//
// 🔑 Los tipos protegen lo que TÚ escribes. Donde entra algo del mundo
//    (el modelo, un archivo, internet) los tipos se acaban, y empieza
//    la comprobación en tiempo de ejecución.
//
// Es exactamente el mismo trabajo que hacen tus 10 frenos del nivel 5b
// en `herramientas.py` — pero aquí el compilador NO TE DEJA olvidarlo.

function leerCiudad(input: unknown): string | null {
  // Paso 1: ¿es un objeto y no es null?  (typeof null === "object", ojo)
  if (typeof input !== "object" || input === null) return null;

  // Paso 2: ¿tiene la llave que pedimos?
  if (!("ciudad" in input)) return null;

  // Paso 3: ¿el valor es un texto?
  const valor = (input as Record<string, unknown>).ciudad;
  if (typeof valor !== "string") return null;

  // Solo ahora TypeScript sabe que es un string, y nosotros también.
  return valor;
}

// El puente nombre → función, igual que el dict FUNCIONES de Python.
const FUNCIONES: Record<string, (ciudad: string) => string> = {
  obtener_clima: obtenerClima,
};

// ══════════════════════════════════════════════════════════════════
//  4. EL BUCLE — el corazón de todo agente
// ══════════════════════════════════════════════════════════════════

async function ejecutarAgente(pregunta: string, maxVueltas = 5): Promise<string> {
  // `MessageParam` es la `interface Mensaje` del paso 1, escrita por el SDK.
  const historial: Anthropic.MessageParam[] = [
    { role: "user", content: pregunta },
  ];

  for (let vuelta = 1; vuelta <= maxVueltas; vuelta++) {
    const respuesta = await client.messages.create({
      model: MODELO,
      max_tokens: 2048,
      tools: HERRAMIENTAS,
      messages: historial,
    });

    const { input_tokens, output_tokens } = respuesta.usage;
    console.log(
      `  [vuelta ${vuelta}] stop_reason=${respuesta.stop_reason} ` +
        `entrada=${input_tokens} salida=${output_tokens}`,
    );

    // ── CASO A: el modelo terminó. Salimos.
    if (respuesta.stop_reason !== "tool_use") {
      // Estrechar otra vez, igual que en el paso 3.
      for (const bloque of respuesta.content) {
        if (bloque.type === "text") return bloque.text;
      }
      return "(terminó sin texto)";
    }

    // ── CASO B: el modelo pidió herramientas.

    // B.1 Guardar su petición TAL CUAL vino: `respuesta.content` ENTERO.
    //     Si le quitas los bloques tool_use, la API rechaza el siguiente
    //     mensaje. Y desde el paso 3b sabes que ahí viaja también un
    //     bloque `thinking` invisible — que también hay que devolver.
    historial.push({ role: "assistant", content: respuesta.content });

    // B.2 Ejecutar cada herramienta pedida. Pueden ser varias en un turno.
    const resultados: Anthropic.ToolResultBlockParam[] = [];

    for (const bloque of respuesta.content) {
      if (bloque.type !== "tool_use") continue;

      const ciudad = leerCiudad(bloque.input);
      const funcion = FUNCIONES[bloque.name];

      let salida: string;

      if (funcion === undefined) {
        // El modelo pidió una herramienta que no existe. No revientes:
        // díselo, que es lo que puede leer.
        salida = `No existe la herramienta '${bloque.name}'.`;
      } else if (ciudad === null) {
        // 🚨 Aquí aterriza el `unknown`. Si el modelo mandó basura, el
        //    agente NO se cae: le devuelve un mensaje de error útil.
        //    Es L5b: el mensaje de error es la instrucción de reintento.
        salida = "Falta el parámetro 'ciudad', o no es un texto.";
      } else {
        salida = funcion(ciudad); // aquí corre TU código
      }

      console.log(`     → ejecuté ${bloque.name}(${JSON.stringify(bloque.input)})`);
      console.log(`       devolvió: ${salida}`);

      resultados.push({
        type: "tool_result",
        tool_use_id: bloque.id, // el ticket: sin él, la API no sabe a qué responde
        content: salida,
      });
    }

    // B.3 Devolver TODOS los resultados en UN solo mensaje, con role "user".
    //     Aunque no los escribiste tú: para la API, todo lo que ENTRA al
    //     modelo es "user".
    historial.push({ role: "user", content: resultados });
  }

  return "(el agente se quedó dando vueltas y se cortó el límite)";
}

// ══════════════════════════════════════════════════════════════════
//  5. LAS MISMAS 3 PREGUNTAS DEL NIVEL 3
// ══════════════════════════════════════════════════════════════════
// La tercera (Tokio) no está en el diccionario. A propósito.

const PREGUNTAS = [
  "¿Qué clima hace en Medellín?",
  "¿Me llevo paraguas si voy a Bogotá?",
  "¿Qué clima hace en Tokio?",
];

async function main(): Promise<void> {
  for (const pregunta of PREGUNTAS) {
    console.log(`\n=== ${pregunta}`);
    console.log(`RESPUESTA: ${await ejecutarAgente(pregunta)}`);
  }

  console.log(`
${"=".repeat(60)}
Lectura del resultado
${"=".repeat(60)}

El patrón es el mismo que viste en Python:

  vuelta 1 → stop_reason=tool_use   (el modelo pide)
  ...corre TU código...
  vuelta 2 → stop_reason=end_turn   (el modelo responde con el dato)

Una pregunta = DOS llamadas. Un agente cuesta mínimo el doble que un chat.

Y lo nuevo de este paso, en una línea:

  Python:      funcion(**bloque.input)          ← confiaba
  TypeScript:  leerCiudad(bloque.input)         ← comprueba, obligado

El bucle no cambió de idioma. Cambió de quién se fía.
`);
}

main().catch((error) => {
  console.error("Murió el programa:", error);
  process.exit(1);
});
