/**
 * 04c_puerta_trasera.ts — Nivel 6c, paso 4, ejercicio 3
 *
 * LA PUERTA DE ATRÁS DEL IDIOMA: `as`.
 *
 * En el paso 4 escribiste `leerCiudad()` con tres comprobaciones porque el
 * compilador NO te dejó tocar `bloque.input` directo (era `unknown`).
 *
 * Pero TypeScript tiene una salida para saltarse ese trabajo:
 *
 *     (bloque.input as { ciudad: string }).ciudad
 *
 * Compila sin una sola queja. Y no protege absolutamente nada.
 * Este archivo lo demuestra con los cuatro `input` que el modelo PUEDE
 * mandarte de verdad.
 *
 * Corre así:
 *   npx tsc
 *   node dist/04c_puerta_trasera.js
 *
 * 💰 CUESTA $0,00 — no hay ni una llamada a la API. Todo pasa en tu máquina.
 */

// ══════════════════════════════════════════════════════════════════
//  1. LAS DOS VERSIONES DE LA MISMA LECTURA
// ══════════════════════════════════════════════════════════════════

// ── VERSIÓN HONESTA: la tuya del paso 4. Pregunta antes de tocar.
function leerCiudad(input: unknown): string | null {
  if (typeof input !== "object" || input === null) return null;
  if (!("ciudad" in input)) return null;

  const valor = (input as Record<string, unknown>).ciudad;
  if (typeof valor !== "string") return null;

  return valor;
}

// ── VERSIÓN CON LA PUERTA DE ATRÁS: una línea, cero comprobaciones.
//
// 🔴 Fíjate en la firma: dice `: string`. Está MINTIENDO, y el compilador
//    se lo cree porque tú se lo juraste con el `as`.
function leerCiudadConAs(input: unknown): string {
  return (input as { ciudad: string }).ciudad;
}

// ══════════════════════════════════════════════════════════════════
//  2. LO QUE EL MODELO PUEDE MANDARTE DE VERDAD
// ══════════════════════════════════════════════════════════════════
// Tu `input_schema` es una PETICIÓN, no una garantía. Estos cuatro casos
// no son inventados de la nada: son los cuatro que ya viste discutidos en
// los comentarios de `04_bucle.ts`.

const CASOS: { nombre: string; input: unknown }[] = [
  { nombre: "lo normal", input: { ciudad: "Bogotá" } },
  { nombre: "vino vacío", input: {} },
  { nombre: "el modelo escribió un número", input: { ciudad: 42 } },
  { nombre: "el modelo hizo un typo", input: { ciuadd: "Bogotá" } },
];

// ══════════════════════════════════════════════════════════════════
//  3. LA FUNCIÓN DE VERDAD (recortada del paso 4)
// ══════════════════════════════════════════════════════════════════
// Le pide un `string` a quien la llame. Y usa `.trim()`, que solo existe
// en los textos. Guarda ese detalle: es donde va a reventar todo.

function obtenerClima(ciudad: string): string {
  const clave = ciudad.trim().toLowerCase();
  return clave === "bogotá" || clave === "bogota"
    ? "14 grados centígrados, lloviznando."
    : `No tengo datos de '${ciudad}'.`;
}

// ══════════════════════════════════════════════════════════════════
//  4. LAS DOS CORRIDAS, LADO A LADO
// ══════════════════════════════════════════════════════════════════

console.log("=".repeat(64));
console.log("A) CON leerCiudad()  — la versión que comprueba");
console.log("=".repeat(64));

for (const caso of CASOS) {
  const ciudad = leerCiudad(caso.input);

  // El bucle del paso 4 hace exactamente esto: si es null, devuelve texto.
  const salida =
    ciudad === null
      ? "⚠️  Falta el parámetro 'ciudad', o no es un texto."
      : obtenerClima(ciudad);

  console.log(`\n${caso.nombre}  →  ${JSON.stringify(caso.input)}`);
  console.log(`   ${salida}`);
}

console.log("\n");
console.log("=".repeat(64));
console.log("B) CON `as`  — la versión que jura y no mira");
console.log("=".repeat(64));

for (const caso of CASOS) {
  console.log(`\n${caso.nombre}  →  ${JSON.stringify(caso.input)}`);

  // El try/catch NO está en el paso 4. Está aquí solo para que el programa
  // no se muera en el primer caso malo y podamos ver los cuatro.
  // En `04_bucle.ts` no hay try: ahí se caería el agente entero. 🚨
  try {
    const ciudad = leerCiudadConAs(caso.input);

    // 👀 MIRA ESTO antes de seguir. Para TypeScript, `ciudad` es un string
    //    —lo dice la firma—. Preguntémosle a JavaScript qué es DE VERDAD:
    console.log(`   typeof ciudad = ${typeof ciudad}   valor = ${ciudad}`);

    console.log(`   ${obtenerClima(ciudad)}`);
  } catch (error) {
    console.log(`   [X] SE CAYO: ${(error as Error).message}`);
  }
}

// ══════════════════════════════════════════════════════════════════
//  5. LO QUE ACABAS DE VER
// ══════════════════════════════════════════════════════════════════

console.log(`
${"=".repeat(64)}
Lectura del resultado
${"=".repeat(64)}

Los dos bloques corrieron el MISMO programa con los MISMOS datos.
Ninguna de las dos versiones dio un solo aviso al compilar.

  leerCiudad()      → 4 de 4 casos manejados. El agente sigue vivo.
  leerCiudadConAs() → el bueno pasa; los tres malos NO.

Y fíjate en CÓMO fallan los tres, porque no fallan igual:

  vino vacío   → 'undefined'. No revienta aquí: revienta más adelante,
                 lejos, cuando ya no se ve de dónde vino.
  el número    → typeof dice "number" donde la firma prometía "string".
                 Reventó dentro de obtenerClima(), en .trim().
  el typo      → 'undefined' otra vez, y el más traicionero: el modelo
                 casi acierta, y tú te enteras en otra parte del código.

🔑 El daño de \`as\` no es que falle. Es DÓNDE falla: lejos del error.

🔑 \`as\` no comprueba, no convierte, no existe. En dist/04c_puerta_trasera.js
   el \`as\` no aparece por ningún lado — se borra igual que se borraron los
   tipos en el paso 0. Lo único que hace es callar al compilador.

🔑 Es el paso 0 otra vez, más caro: allá 'Hola, 42' salió MAL pero salió.
   Aquí el agente se cae en producción, con la vuelta 1 ya pagada.

¿Cuándo SÍ se usa \`as\`? Cuando sabes algo que el compilador no puede
saber, y el dato es TUYO. Nunca sobre lo que escribió el modelo, ni sobre
lo que llegó de un archivo o de internet. Ahí tú tampoco lo sabes.
`);
