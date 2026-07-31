/**
 * 03b_thinking.ts — Nivel 6c, paso 3b
 *
 * LA MEDICIÓN QUE CUESTA $0,00.
 *
 * En el paso 3 pagaste 235 tokens de salida por dos frases. Pareció mucho.
 * Aquí se comprueba por qué, SIN gastar un centavo.
 *
 * `count_tokens` es un endpoint de la API que cuenta tokens y NO cobra.
 * No llama al modelo: solo pasa el texto por el mismo tokenizador.
 *
 * Corre así:
 *   npx tsc
 *   node dist/03b_thinking.js
 */

import Anthropic from "@anthropic-ai/sdk";
import { config } from "dotenv";
import path from "path";

const RUTA_ENV = path.resolve(__dirname, "..", "..", ".env");
config({ path: RUTA_ENV });

const client = new Anthropic();

// ══════════════════════════════════════════════════════════════════
//  1. EL TEXTO QUE SÍ LLEGÓ — copiado de tu corrida del paso 3
// ══════════════════════════════════════════════════════════════════
// Esto es exactamente lo que imprimió tu pantalla. Ni una coma más.

const RESPUESTA_QUE_LLEGO =
  "JavaScript es el lenguaje que entienden los navegadores para dar vida " +
  "a las páginas web, y funciona de forma muy libre: acepta lo que le " +
  "escribas y solo se queja cuando algo falla mientras el programa está " +
  "en marcha. TypeScript es ese mismo lenguaje pero con una capa extra " +
  "que te obliga a decir de antemano qué tipo de datos manejas (números, " +
  "textos, etc.), así te avisa de los errores mientras escribes, antes de " +
  "que el programa llegue a los usuarios.";

// Los números que la API te cobró de verdad, en la corrida del paso 3.
const COBRADO_SALIDA = 235;

async function main(): Promise<void> {
  // ════════════════════════════════════════════════════════════════
  //  2. CONTAR — gratis
  // ════════════════════════════════════════════════════════════════
  // `countTokens` pide un mensaje completo, no un texto suelto. Por eso
  // el texto va envuelto como si fuera un turno del usuario.
  //
  // ⚠️ Eso mete un puñado de tokens de "envoltorio" que no son del texto.
  //    Así que el número que sale es una COTA ALTA: el texto real pesa
  //    eso o un poco menos. Lo decimos porque medir mal y no avisar es
  //    peor que no medir.

  const cuenta = await client.messages.countTokens({
    model: "claude-opus-5",
    messages: [{ role: "user", content: RESPUESTA_QUE_LLEGO }],
  });

  const visibles = cuenta.input_tokens;
  const invisibles = COBRADO_SALIDA - visibles;
  const porcentaje = (invisibles / COBRADO_SALIDA) * 100;

  // ════════════════════════════════════════════════════════════════
  //  3. LA CUENTA
  // ════════════════════════════════════════════════════════════════

  console.log("=".repeat(60));
  console.log("  ¿A DÓNDE SE FUERON LOS 235 TOKENS DE SALIDA?");
  console.log("=".repeat(60));
  console.log(`texto que VISTE      : ~${visibles} tokens  (envoltorio incluido)`);
  console.log(`la API te COBRÓ      :  ${COBRADO_SALIDA} tokens`);
  console.log("-".repeat(60));
  console.log(
    `pensamiento INVISIBLE: ~${invisibles} tokens  (${porcentaje.toFixed(0)}% de la factura)`,
  );
  console.log("=".repeat(60));

  // Opus 5: $25 por millón de tokens de salida.
  const costoInvisible = (invisibles / 1_000_000) * 25;
  console.log(`Lo invisible te costó: $${costoInvisible.toFixed(6)} USD`);
  console.log("");
  console.log("🔑 En Opus 5 el modelo PIENSA por defecto: no escribir el");
  console.log("   parámetro `thinking` NO lo apaga, lo deja en automático.");
  console.log("   Y ese pensamiento se factura dentro de output_tokens.");
  console.log("");
  console.log("🚨 Y la consecuencia que muerde: `max_tokens` es el techo de");
  console.log("   PENSAMIENTO + RESPUESTA juntos. Si lo ajustas al tamaño de");
  console.log("   la respuesta que esperas, el texto se corta a mitad.");
  console.log("   Es el bug del nivel 1 (max_tokens=30) con otra cara.");
  console.log("=".repeat(60));
  console.log("Esta corrida costó: $0,000000 — count_tokens no cobra.");
}

main().catch((error) => {
  console.error("Murió el programa:", error);
  process.exit(1);
});
