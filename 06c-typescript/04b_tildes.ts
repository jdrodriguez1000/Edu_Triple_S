/**
 * 04b_tildes.ts — Nivel 6c, paso 4b
 *
 * ¿DE DÓNDE SALEN LOS +5 TOKENS?
 *
 * El paso 4 dejó una sospecha. Las mismas 3 preguntas, el mismo agente:
 *
 *   pregunta   Python   TypeScript   dif
 *   Medellín     452       457       +5
 *   Bogotá       458       463       +5
 *   Tokio        452       457       +5
 *
 * Exactamente +5 en las tres. Eso no es casualidad.
 *
 * La sospecha: las TILDES. El archivo de Python está escrito sin ellas
 * ("Usala", "algun", "Bogota"); el de TypeScript sí las tiene.
 *
 * Este script no la supone: la mide, y por separado — el menú de
 * herramientas por un lado, cada pregunta por el otro.
 *
 * Corre así:
 *   npx tsc
 *   node dist/04b_tildes.js
 *
 * ✅ CUESTA $0,00. `count_tokens` cuenta y no cobra. Es el mismo
 *    instrumento del paso 3b.
 */

import Anthropic from "@anthropic-ai/sdk";
import { config } from "dotenv";
import path from "path";

config({ path: path.resolve(__dirname, "..", "..", ".env") });

const client = new Anthropic();
const MODELO = "claude-opus-5";

// ══════════════════════════════════════════════════════════════════
//  LOS DOS MENÚS — copiados TAL CUAL de cada archivo
// ══════════════════════════════════════════════════════════════════

// El de 03-primer-agente/02_bucle.py — SIN tildes
const MENU_PYTHON: Anthropic.Tool[] = [
  {
    name: "obtener_clima",
    description:
      "Devuelve el clima actual de una ciudad. Usala siempre que te " +
      "pregunten por el clima, la temperatura o si llueve en algun lugar.",
    input_schema: {
      type: "object",
      properties: {
        ciudad: {
          type: "string",
          description: "Nombre de la ciudad, por ejemplo: Bogota",
        },
      },
      required: ["ciudad"],
    },
  },
];

// El de 04_bucle.ts — CON tildes
const MENU_TYPESCRIPT: Anthropic.Tool[] = [
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

// Las 3 preguntas, en sus dos versiones
const PREGUNTAS: { nombre: string; py: string; ts: string }[] = [
  {
    nombre: "Medellín",
    py: "Que clima hace en Medellin?",
    ts: "¿Qué clima hace en Medellín?",
  },
  {
    nombre: "Bogotá",
    py: "Me llevo paraguas si voy a Bogota?",
    ts: "¿Me llevo paraguas si voy a Bogotá?",
  },
  {
    nombre: "Tokio",
    py: "Que clima hace en Tokio?",
    ts: "¿Qué clima hace en Tokio?",
  },
];

// ══════════════════════════════════════════════════════════════════
//  EL INSTRUMENTO
// ══════════════════════════════════════════════════════════════════
// ⚠️ `countTokens` pide un mensaje COMPLETO, no un texto suelto (es la
//    advertencia del paso 3b). Por eso todo va envuelto en un turno.
//    Como aquí sólo nos importan las DIFERENCIAS, el envoltorio se
//    cancela solo: pesa lo mismo en los dos lados de la resta.

async function contar(
  texto: string,
  herramientas?: Anthropic.Tool[],
): Promise<number> {
  const cuenta = await client.messages.countTokens({
    model: MODELO,
    messages: [{ role: "user", content: texto }],
    ...(herramientas ? { tools: herramientas } : {}),
  });
  return cuenta.input_tokens;
}

async function main(): Promise<void> {
  const linea = "=".repeat(64);

  // ── SOSPECHOSO 1: el menú de herramientas ───────────────────────
  // Mismo mensaje de relleno en los dos, para que sólo varíe el menú.
  const RELLENO = "x";

  const menuPy = await contar(RELLENO, MENU_PYTHON);
  const menuTs = await contar(RELLENO, MENU_TYPESCRIPT);

  console.log(linea);
  console.log("SOSPECHOSO 1 — el menú de herramientas");
  console.log(linea);
  console.log(`  menú sin tildes (Python)     : ${menuPy}`);
  console.log(`  menú con tildes (TypeScript) : ${menuTs}`);
  console.log(`  → diferencia                 : ${menuTs - menuPy} tokens`);

  // ── SOSPECHOSO 2: cada pregunta ─────────────────────────────────
  console.log(`\n${linea}`);
  console.log("SOSPECHOSO 2 — las preguntas, una por una");
  console.log(linea);

  let sumaPreguntas = 0;

  for (const p of PREGUNTAS) {
    const py = await contar(p.py);
    const ts = await contar(p.ts);
    const dif = ts - py;
    sumaPreguntas += dif;
    console.log(
      `  ${p.nombre.padEnd(10)} py=${py}  ts=${ts}  → ${dif >= 0 ? "+" : ""}${dif}`,
    );
  }

  // ── EL VEREDICTO ────────────────────────────────────────────────
  const difMenu = menuTs - menuPy;

  console.log(`\n${linea}`);
  console.log("VEREDICTO");
  console.log(linea);
  console.log(`  del menú     : ${difMenu >= 0 ? "+" : ""}${difMenu} (igual en las 3 preguntas)`);
  console.log(`  de preguntas : ${sumaPreguntas >= 0 ? "+" : ""}${sumaPreguntas} repartidos entre las 3`);
  console.log("");
  console.log("  Lo observado en la corrida real fue +5, +5, +5.");
  console.log("  Si el menú explica los 3 iguales y cada pregunta suma su");
  console.log("  parte, los números de arriba tienen que cuadrar. Compara.");
  console.log(linea);
}

main().catch((error) => {
  console.error("Murió el programa:", error);
  process.exit(1);
});
