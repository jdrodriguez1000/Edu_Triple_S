/**
 * 00_hola.ts — Nivel 6c, paso 0
 *
 * Lo único que este archivo tiene que enseñarte:
 *
 *   TypeScript NO CORRE. Se traduce a JavaScript, y eso es lo que corre.
 *
 * Python lo ejecutas directo:      python script.py
 * TypeScript tiene un paso previo: npx tsc  →  node dist/00_hola.js
 *
 * Corre así (los dos comandos, en orden):
 *   npx tsc
 *   node dist/00_hola.js
 */

// ── 1. Una variable con su tipo escrito ──────────────────────────
// En Python:      nombre = "Juan"
// En TypeScript:  const nombre: string = "Juan"
//
// Ese ": string" es la parte nueva. Se lee "nombre, que es un texto".
const nombre: string = "Juan";

// ── 2. Una función que declara qué recibe y qué devuelve ─────────
// En Python:
//     def saludar(quien):
//         return f"Hola, {quien}"
//
// En TypeScript, lo mismo pero diciendo los tipos:
//     (quien: string)  → lo que RECIBE
//     : string         → lo que DEVUELVE
function saludar(quien: string): string {
  // Las comillas ` (backtick) son el f-string de JavaScript.
  // Python: f"Hola, {quien}"     JS: `Hola, ${quien}`
  return `Hola, ${quien}`;
}

// ── 3. Un número, para ver que los tipos no son solo texto ───────
const vueltasMaximas: number = 5;

console.log(saludar(nombre));
console.log(`El harness dará máximo ${vueltasMaximas} vueltas.`);

// ─────────────────────────────────────────────────────────────────
//  EJERCICIO 1 — rompe esto a propósito, y NO te quedes en el aviso.
//
//  Descomenta la última línea de este archivo y corre los dos comandos:
//
//      npx tsc
//      node dist/00_hola.js
//
//  Le estás pasando un número a una función que pidió texto. Vas a ver
//  el aviso que esperabas:
//
//      error TS2345: Argument of type 'number' is not assignable
//                    to parameter of type 'string'.
//
//  🚨 Y AHORA MIRA LO QUE IMPRIME NODE. Va a decir "Hola, 42".
//
//  Sí: tsc se quejó, y AUN ASÍ escribió el .js, y Node lo corrió sin
//  ningún problema. El aviso no detuvo nada.
//
//  La razón es la del EJERCICIO 3: en el .js traducido los tipos NO
//  EXISTEN. Para JavaScript, saludar(42) es perfectamente válido.
//
//  → Sigue con el EJERCICIO 2, en tsconfig.json.
// ─────────────────────────────────────────────────────────────────

// console.log(saludar(42));

// ─────────────────────────────────────────────────────────────────
//  EJERCICIO 3 — abre dist/00_hola.js y compáralo con este archivo.
//
//  Busca los ": string" y los ": number". No están. Ni uno.
//  El traductor los LEYÓ, te avisó con ellos, y después los BORRÓ.
//
//  Los tipos son para ti, no para la máquina.
// ─────────────────────────────────────────────────────────────────

