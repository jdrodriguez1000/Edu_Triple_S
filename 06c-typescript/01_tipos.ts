/**
 * 01_tipos.ts — Nivel 6c, paso 1
 *
 * Los tipos son LO ÚNICO de verdad nuevo del idioma. Todo lo demás
 * (funciones, listas, if, for) ya lo sabes de Python con otra ropa.
 *
 * Y no los vamos a aprender con ejemplos de juguete: los vamos a
 * aprender construyendo LAS FORMAS DE TU AGENTE. El mensaje, el rol,
 * la herramienta. Las mismas que llevas 23 sesiones escribiendo en
 * Python como diccionarios sueltos.
 *
 * Corre así:
 *   npx tsc
 *   node dist/01_tipos.js
 */

console.log("=".repeat(60));

// ══════════════════════════════════════════════════════════════════
//  1. NO HAY QUE ESCRIBIR TODOS LOS TIPOS. TypeScript los deduce.
// ══════════════════════════════════════════════════════════════════
// El paso 0 los escribía a propósito, para que los vieras. En el día
// a día casi nunca se escriben: el compilador los adivina del valor.

const modelo = "claude-opus-5"; // TypeScript ya sabe: es string
let vueltas = 0; // ya sabe: es number

// Y adivinar NO es "dejar pasar". Descomenta esto y verás que se queja
// igual, aunque nadie escribió ningún tipo:
// vueltas = "tres";

console.log(`1. Modelo: ${modelo}, vueltas: ${vueltas}`);

// 📌 La regla práctica: los tipos se escriben en las FRONTERAS
//    (lo que una función recibe y devuelve). Adentro se dejan deducir.

// ══════════════════════════════════════════════════════════════════
//  2. LISTAS
// ══════════════════════════════════════════════════════════════════
// Python:      nombres = ["a", "b"]          ← puede mezclar tipos
// TypeScript:  const nombres: string[] = []  ← todos del mismo tipo

const herramientasDisponibles: string[] = ["consultar_clima"];
herramientasDisponibles.push("convertir_moneda");

// herramientasDisponibles.push(42);  ← esto no compila. En Python sí.

console.log(`2. Herramientas: ${herramientasDisponibles.length}`);

// ══════════════════════════════════════════════════════════════════
//  3. interface — LE PONES NOMBRE A UNA FORMA
// ══════════════════════════════════════════════════════════════════
// Esto es lo que llevas escribiendo todo el curso en Python:
//
//     {"role": "user", "content": "¿Qué clima hace en Bogotá?"}
//
// Un diccionario suelto. Nada dice qué llaves debe tener ni de qué
// tipo. Si escribías "rol" en vez de "role", te enterabas cuando la
// API devolvía un 400 — y ya habías pagado la llamada.
//
// Una `interface` le pone NOMBRE a esa forma, de una vez y para todas:

interface Mensaje {
  role: "user" | "assistant"; // ← ojo a esta línea, es la del punto 4
  content: string;
}

const primerMensaje: Mensaje = {
  role: "user",
  content: "¿Qué clima hace en Bogotá?",
};

const historial: Mensaje[] = [primerMensaje];

console.log(`3. Historial: ${historial.length} mensaje(s)`);

// ══════════════════════════════════════════════════════════════════
//  4. 🚨 UNIÓN — EL TIPO QUE PYTHON NO TIENE, Y QUE TE HABRÍA
//     AHORRADO UN ERROR REAL DEL NIVEL 3
// ══════════════════════════════════════════════════════════════════
// Mira otra vez:
//
//     role: "user" | "assistant"
//
// Eso NO dice "role es un texto". Dice algo mucho más estrecho:
//
//     "role solo puede ser una de ESTAS DOS PALABRAS EXACTAS"
//
// La barra `|` se lee "o". Y no hay tercera opción.
//
// En Python, "assistnat" era un string perfectamente válido. El error
// llegaba de la API, en forma de 400, después de pagar. Aquí llega
// del traductor, gratis, antes de correr nada.
//
// Descomenta y compila:
// const roto: Mensaje = { role: "assistnat", content: "hola" };

const respuesta: Mensaje = { role: "assistant", content: "Hace 18 °C." };
historial.push(respuesta);

console.log(`4. Historial ahora: ${historial.length} mensajes`);

// ══════════════════════════════════════════════════════════════════
//  5. CAMPOS OPCIONALES — el `?`
// ══════════════════════════════════════════════════════════════════
// No todo mensaje trae lo mismo. El `?` dice "puede no venir".

interface Uso {
  inputTokens: number;
  outputTokens: number;
  costoUSD?: number; // ← opcional: puede no estar
}

const uso: Uso = { inputTokens: 1200, outputTokens: 340 };

// Y aquí está la parte buena: TypeScript te OBLIGA a considerar que
// puede faltar. Si escribieras `uso.costoUSD.toFixed(2)` directo, se
// queja: "puede ser undefined". El `??` da el valor de respaldo.
const costo = uso.costoUSD ?? 0;

console.log(`5. Tokens: ${uso.inputTokens} in / ${uso.outputTokens} out, costo $${costo}`);

// 📌 `undefined` de JavaScript ≈ `None` de Python, pero TypeScript no
//    te deja usarlo por accidente. Ese es medio valor del idioma.

// ══════════════════════════════════════════════════════════════════
//  6. `any` — LA PUERTA DE ATRÁS, Y POR QUÉ NO LA USES
// ══════════════════════════════════════════════════════════════════
// `any` significa "no revises nada aquí". Apaga el idioma entero
// para esa variable.

const datoSinRevisar: any = { role: "cualquier_cosa", content: 42 };

// Esto compila sin una sola queja. Es JavaScript otra vez:
console.log(`6. any deja pasar: role="${datoSinRevisar.role}"`);

// 🔴 Cada `any` que escribes es un pedazo de tu programa donde
//    TypeScript dejó de trabajar — y no te avisa que lo apagaste.
//    Lo vas a ver aparecer solo cuando llegue JSON de afuera
//    (paso 3, la respuesta de la API). Ahí se maneja distinto.

console.log("=".repeat(60));

// ─────────────────────────────────────────────────────────────────
//  Los ejercicios están en el README del nivel, sección "Paso 1".
// ─────────────────────────────────────────────────────────────────
