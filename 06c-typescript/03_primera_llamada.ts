/**
 * 03_primera_llamada.ts — Nivel 6c, paso 3
 *
 * EL PRIMERO QUE CUESTA DINERO. Unos centavos.
 *
 * Es tu `01-primera-llamada/01_hola.py` del nivel 1, dicho en TypeScript.
 * La API es la misma, la key es la misma, el modelo es el mismo. Solo
 * cambia el idioma — que es exactamente el punto de todo este nivel.
 *
 * Corre así:
 *   npx tsc
 *   node dist/03_primera_llamada.js
 */

import Anthropic from "@anthropic-ai/sdk";
import { config } from "dotenv";
import path from "path";

// ══════════════════════════════════════════════════════════════════
//  1. 🚨 LA KEY, Y UNA TRAMPA QUE PYTHON NO TENÍA
// ══════════════════════════════════════════════════════════════════
// En Python tus scripts hacen esto:
//
//     load_dotenv(Path(__file__).resolve().parent.parent / ".env")
//                                        └── dos niveles: script → nivel → raíz
//
// Aquí hay que subir TRES. ¿Por qué?
//
// Porque este archivo NO es el que corre. Corre su traducción, que vive
// en `dist/`. Así que el programa arranca un nivel MÁS ABAJO:
//
//     .ts  →  06c-typescript/03_primera_llamada.ts   (lo que escribes)
//     .js  →  06c-typescript/dist/03_primera_llamada.js   (lo que corre)
//
// 🔑 En TypeScript, la ruta se calcula desde donde corre el .js,
//    no desde donde vive el .ts.

const RUTA_ENV = path.resolve(__dirname, "..", "..", ".env");
//                                        dist → 06c → raíz

config({ path: RUTA_ENV });

// ── Comprobar que la key llegó, SIN imprimirla ───────────────────
// Regla del curso desde el nivel 0: nunca imprimir la key completa.
const key = process.env.ANTHROPIC_API_KEY;

if (!key) {
  console.error(`❌ No encontré ANTHROPIC_API_KEY en:\n   ${RUTA_ENV}`);
  process.exit(1);
}

console.log(`✅ Key cargada desde la raíz (termina en …${key.slice(-4)})`);
console.log("=".repeat(60));

// ══════════════════════════════════════════════════════════════════
//  2. EL CLIENTE
// ══════════════════════════════════════════════════════════════════
// Python:      client = Anthropic()
// TypeScript:  const client = new Anthropic()
//
// El `new` es la única diferencia. Los dos leen ANTHROPIC_API_KEY del
// entorno solos — por eso nunca escribimos la key aquí adentro.

const client = new Anthropic();

async function main(): Promise<void> {
  // ════════════════════════════════════════════════════════════════
  //  3. LA LLAMADA — y fíjate en el `await`
  // ════════════════════════════════════════════════════════════════
  // Todo el paso 2 fue para esta línea. Sin el `await`, `respuesta`
  // sería un recibo y lo que sigue reventaría.

  const respuesta = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 2000,
    messages: [
      {
        role: "user",
        content:
          "En dos frases: ¿cuál es la diferencia entre TypeScript y JavaScript? " +
          "Habla en español y sin tecnicismos.",
      },
    ],
  });

  // ════════════════════════════════════════════════════════════════
  //  4. 🚨 AQUÍ SE PAGA LO QUE APRENDISTE EN EL PASO 1
  // ════════════════════════════════════════════════════════════════
  // En Python leías el texto así, directo:
  //
  //     print(respuesta.content[0].text)
  //
  // 🔴 ESA LÍNEA NO COMPILA EN TYPESCRIPT. Descomenta y pruébala:
  // console.log(respuesta.content[0].text);
  //
  // ¿Por qué? Porque `content` NO es una lista de textos. Es una lista
  // de bloques, y cada bloque puede ser de varios tipos: `text`,
  // `thinking`, `tool_use`… Es exactamente la UNIÓN del paso 1, pero
  // escrita por el SDK en vez de por ti:
  //
  //     type ContentBlock = TextBlock | ThinkingBlock | ToolUseBlock | ...
  //
  // TypeScript se niega a darte `.text` de algo que quizá no lo tenga.
  // Y tiene razón: en el nivel 1 te pasó DE VERDAD que el bloque de
  // texto no existía (todos los tokens se fueron en `thinking`) y la
  // pantalla salió vacía sin ningún error. → L1.1, L1.2
  //
  // La forma correcta es preguntar primero. A eso se le llama ESTRECHAR:

  for (const bloque of respuesta.content) {
    if (bloque.type === "text") {
      // Dentro de este `if`, y solo aquí, TypeScript sabe que
      // `bloque` es un TextBlock. Ahora `.text` sí existe.
      console.log(bloque.text);
    }
  }

  // 🔑 El aviso no es una molestia: es el bug del nivel 1, atrapado
  //    antes de correr y antes de pagar.

  // ════════════════════════════════════════════════════════════════
  //  5. usage y stop_reason — la costumbre de este curso
  // ════════════════════════════════════════════════════════════════

  console.log("=".repeat(60));
  console.log(`stop_reason : ${respuesta.stop_reason}`);
  console.log(`modelo      : ${respuesta.model}`);
  console.log(
    `tokens      : ${respuesta.usage.input_tokens} entrada / ${respuesta.usage.output_tokens} salida`,
  );

  // Precios de Opus 5, por millón de tokens. Se CALCULA, no se fija:
  // es la lección L1.13 (el "Haiku cuesta 5x menos" que era mentira).
  const costo =
    (respuesta.usage.input_tokens / 1_000_000) * 5 +
    (respuesta.usage.output_tokens / 1_000_000) * 25;

  console.log(`costo       : $${costo.toFixed(6)} USD`);
  console.log("=".repeat(60));
}

// El seguro del paso 2: sin esto, un fallo adentro desaparece callado.
main().catch((error) => {
  console.error("Murió el programa:", error);
  process.exit(1);
});
