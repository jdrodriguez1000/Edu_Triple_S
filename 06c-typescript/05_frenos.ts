/**
 * 05_frenos.ts — Nivel 6c, paso 5
 *
 * LOS FRENOS, Y MEDIR.
 *
 * Es `04_bucle.ts` con UN solo cambio de fondo: `leerCiudad()` deja de
 * devolver `string | null` y pasa a devolver un SOBRE que lleva adentro
 * el motivo del fallo.
 *
 * Por qué. En el paso 4 los tres motivos distintos salían aplastados en
 * un `null`, y el bucle tenía que inventarse un mensaje genérico:
 *
 *     "Falta el parámetro 'ciudad', o no es un texto."
 *
 * La función SABÍA cuál de los tres `if` falló, y tiraba ese dato a la
 * basura. Aquí no.
 *
 * 🔑 Un buen mensaje de error nombra el error Y nombra el arreglo.
 *    Cada vuelta que el modelo gasta adivinando la pagas tú.
 *
 * Corre así:
 *   npx tsc
 *   node dist/05_frenos.js
 *
 * 💰 CUESTA unos centavos (3 preguntas). Con SABOTEAR = true cuesta un
 *    poco más, porque el modelo tiene que reintentar.
 */

import Anthropic from "@anthropic-ai/sdk";
import { config } from "dotenv";
import path from "path";

config({ path: path.resolve(__dirname, "..", "..", ".env") });

const client = new Anthropic();
const MODELO = "claude-opus-5";

// 🔴 EL INTERRUPTOR DE LA MEDICIÓN. Ponlo en `true` y el programa le
//    ROMPE a propósito el `input` al modelo en su primera petición, para
//    ver qué hace al leer tu mensaje de error: ¿reintenta bien? ¿se
//    rinde? ¿inventa? Eso es lo que nunca se había visto.
// Las dos corridas ya están hechas y anotadas en PROGRESO.md (sesión 27):
//   false → 6 vueltas, $0,027825      true → 9 vueltas, $0,046050  (+65%)
// Se deja en `false` para que correrlo por curiosidad salga barato.
const SABOTEAR = false;

// ══════════════════════════════════════════════════════════════════
//  1. LA FUNCIÓN DE VERDAD — igual que en el paso 4, sin tocar
// ══════════════════════════════════════════════════════════════════

const CLIMA_FALSO: Record<string, { temperatura_c: number; estado: string }> = {
  bogota: { temperatura_c: 14, estado: "lloviznando" },
  medellin: { temperatura_c: 24, estado: "despejado" },
  cartagena: { temperatura_c: 32, estado: "húmedo y soleado" },
};

function obtenerClima(ciudad: string): string {
  const clave = ciudad
    .trim()
    .toLowerCase()
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "");

  const dato = CLIMA_FALSO[clave];

  if (dato === undefined) {
    // Regla del nivel 3: NO lanzamos un error. Devolvemos texto legible.
    return `No tengo datos de '${ciudad}'. Ciudades disponibles: Bogotá, Medellín, Cartagena.`;
  }

  return `${dato.temperatura_c} grados centígrados, ${dato.estado}.`;
}

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
//  2. 🚨 EL CAMBIO DEL PASO: UNA UNIÓN DISCRIMINADA
// ══════════════════════════════════════════════════════════════════
//
// Se lee: "un Lectura es O BIEN esto, O BIEN lo otro". La barra | es "o".
// `ok` es la ETIQUETA que dice cuál de los dos te tocó — el discriminante.

type Lectura =
  | { ok: true; ciudad: string }
  | { ok: false; error: string };

// Lo que compra este tipo, y no es la sintaxis:
//
//   1. El sobre LLEVA el motivo. `null` no podía llevar nada.
//   2. El compilador sabe en qué rama estás: dentro del `if (r.ok)` te
//      deja leer `r.ciudad` y te PROHÍBE `r.error`. En el `else`, al revés.
//   3. 🔑 NO PUEDES OLVIDAR EL CASO MALO. Escribir `leerCiudad(x).ciudad`
//      directo no compila, porque puede que no haya `ciudad`. El freno lo
//      pone el idioma, no tu disciplina.

// Un ayudante de 3 líneas, y no sobra: `typeof null` dice "object", así
// que sin esto los mensajes de error salen mintiendo ("esperaba un objeto
// y llegó un object"). Se descubrió probando los frenos, no leyéndolos.
// 🔑 El mensaje de error es código, y puede tener el mismo bug del que protege.
function describir(valor: unknown): string {
  return valor === null ? "null" : typeof valor;
}

function leerCiudad(input: unknown): Lectura {
  // ── FRENO 1: ¿es un objeto y no es null?  (ojo: typeof null === "object")
  //    El caso que crees que nunca pasa también necesita su mensaje:
  //    el día que pase, el silencio es lo único que vas a tener.
  //    Es "denegar por defecto" del 5b, otra vez.
  if (typeof input !== "object" || input === null) {
    return {
      ok: false,
      error:
        `Esperaba un objeto con la llave 'ciudad', y llegó ` +
        `${describir(input)}. Manda: {"ciudad": "Bogotá"}`,
    };
  }

  // ── FRENO 2: ¿está la llave?
  //    Aquí caen DOS casos distintos que el paso 4 no distinguía:
  //    el objeto vacío {} y el typo {"ciuadd": "..."}.
  //    Los separamos mirando algo que antes nadie miraba: QUÉ llaves
  //    sí llegaron. El dato estaba ahí, gratis, en el input.
  if (!("ciudad" in input)) {
    const llaves = Object.keys(input);

    if (llaves.length === 0) {
      return { ok: false, error: "Falta la llave 'ciudad'. Llegó un objeto vacío." };
    }

    // 🔑 Este es EL mensaje bueno: dice lo que está mal Y lo que está bien.
    return {
      ok: false,
      error:
        `Falta la llave 'ciudad'. Llegó: ${llaves.map((k) => `'${k}'`).join(", ")}. ` +
        `La llave se llama 'ciudad'.`,
    };
  }

  // ── FRENO 3: ¿el valor es un texto?
  //    Fíjate: NO hay `as` aquí. El `in` de arriba ya le enseñó a
  //    TypeScript que la llave existe, y `input.ciudad` vale `unknown`.
  //    (En el paso 4 usábamos `as Record<string, unknown>`. Sobraba.)
  const valor: unknown = input.ciudad;

  if (typeof valor !== "string") {
    return {
      ok: false,
      error: `'ciudad' debe ser texto, no ${describir(valor)}. Llegó: ${JSON.stringify(valor)}`,
    };
  }

  // ── Solo aquí TypeScript sabe que es un string, y nosotros también.
  return { ok: true, ciudad: valor };
}

const FUNCIONES: Record<string, (ciudad: string) => string> = {
  obtener_clima: obtenerClima,
};

// ══════════════════════════════════════════════════════════════════
//  3. EL SABOTEADOR — solo para MEDIR
// ══════════════════════════════════════════════════════════════════
// Le daña al modelo su primera petición para forzar que el freno dispare.
// Nunca se hace esto en un programa de verdad: es un banco de pruebas.

function sabotear(input: unknown): unknown {
  // Le cambiamos el nombre a la llave: {"ciudad": X} → {"ciuadd": X}
  if (typeof input === "object" && input !== null && "ciudad" in input) {
    return { ciuadd: input.ciudad };
  }
  return input;
}

// ══════════════════════════════════════════════════════════════════
//  4. EL BUCLE — igual que el paso 4, salvo el `if (r.ok)`
// ══════════════════════════════════════════════════════════════════

type Resultado = { texto: string; vueltas: number; entrada: number; salida: number };

async function ejecutarAgente(pregunta: string, maxVueltas = 5): Promise<Resultado> {
  const historial: Anthropic.MessageParam[] = [{ role: "user", content: pregunta }];

  let totalEntrada = 0;
  let totalSalida = 0;

  for (let vuelta = 1; vuelta <= maxVueltas; vuelta++) {
    const respuesta = await client.messages.create({
      model: MODELO,
      max_tokens: 2048,
      tools: HERRAMIENTAS,
      messages: historial,
    });

    const { input_tokens, output_tokens } = respuesta.usage;
    totalEntrada += input_tokens;
    totalSalida += output_tokens;

    console.log(
      `  [vuelta ${vuelta}] stop_reason=${respuesta.stop_reason} ` +
        `entrada=${input_tokens} salida=${output_tokens}`,
    );

    // ── CASO A: terminó.
    if (respuesta.stop_reason !== "tool_use") {
      for (const bloque of respuesta.content) {
        if (bloque.type === "text") {
          return { texto: bloque.text, vueltas: vuelta, entrada: totalEntrada, salida: totalSalida };
        }
      }
      return { texto: "(terminó sin texto)", vueltas: vuelta, entrada: totalEntrada, salida: totalSalida };
    }

    // ── CASO B: pidió herramientas.
    historial.push({ role: "assistant", content: respuesta.content });

    const resultados: Anthropic.ToolResultBlockParam[] = [];

    for (const bloque of respuesta.content) {
      if (bloque.type !== "tool_use") continue;

      // El sabotaje entra SOLO en la vuelta 1, para verlo recuperarse.
      const crudo = SABOTEAR && vuelta === 1 ? sabotear(bloque.input) : bloque.input;

      const funcion = FUNCIONES[bloque.name];
      const r = leerCiudad(crudo);

      let salida: string;

      if (funcion === undefined) {
        salida = `No existe la herramienta '${bloque.name}'.`;
      } else if (r.ok) {
        // 👀 Dentro de esta rama existe r.ciudad, y r.error NO existe.
        salida = funcion(r.ciudad);
      } else {
        // 👀 Y aquí al revés. El motivo llegó vivo hasta el modelo.
        salida = r.error;
      }

      console.log(`     -> ${bloque.name}(${JSON.stringify(crudo)})`);
      console.log(`        devolvio: ${salida}`);

      resultados.push({
        type: "tool_result",
        tool_use_id: bloque.id,
        content: salida,
      });
    }

    historial.push({ role: "user", content: resultados });
  }

  return {
    texto: "(el agente se quedó dando vueltas y se cortó el límite)",
    vueltas: maxVueltas,
    entrada: totalEntrada,
    salida: totalSalida,
  };
}

// ══════════════════════════════════════════════════════════════════
//  5. LAS MISMAS 3 PREGUNTAS, Y LA CUENTA AL FINAL
// ══════════════════════════════════════════════════════════════════

const PREGUNTAS = [
  "¿Qué clima hace en Medellín?",
  "¿Me llevo paraguas si voy a Bogotá?",
  "¿Qué clima hace en Tokio?",
];

// Precios de Opus 5 por millón de tokens.
// ⚠️ VERIFICADOS el 2026-08-01 contra la documentación oficial, NO de memoria:
//    $5 de entrada, $25 de salida.
// La primera versión de este archivo decía 15 y 75 (el triple) y el error se
// cazó porque el costo no cuadraba con el del paso 4, que SÍ estaba medido.
// 🔑 Un número escrito en el material tiene que venir de una corrida o de una
//    fuente comprobada. Es el mismo defecto de "Haiku cuesta 5x menos" (nivel 1).
const PRECIO_ENTRADA = 5 / 1_000_000;
const PRECIO_SALIDA = 25 / 1_000_000;

async function main(): Promise<void> {
  console.log(SABOTEAR ? ">>> MODO SABOTAJE: el freno 2 va a disparar <<<\n" : "");

  let entrada = 0;
  let salida = 0;
  let vueltas = 0;

  for (const pregunta of PREGUNTAS) {
    console.log(`\n=== ${pregunta}`);
    const r = await ejecutarAgente(pregunta);
    console.log(`RESPUESTA: ${r.texto}`);

    entrada += r.entrada;
    salida += r.salida;
    vueltas += r.vueltas;
  }

  const costo = entrada * PRECIO_ENTRADA + salida * PRECIO_SALIDA;

  console.log(`
${"=".repeat(64)}
La cuenta de esta corrida
${"=".repeat(64)}

  saboteado : ${SABOTEAR ? "SI" : "no"}
  vueltas   : ${vueltas}   (sin sabotaje son 6: dos por pregunta)
  entrada   : ${entrada} tokens
  salida    : ${salida} tokens
  costo     : $${costo.toFixed(6)}

Corre las dos veces (SABOTEAR = false y true) y compara. La diferencia
de vueltas es lo que cuesta un error, y lo que vale un mensaje bueno.

Lo que cambio en este paso, en una linea:

  paso 4:  string | null   -> el motivo se pierde, el bucle adivina
  paso 5:  Lectura         -> el motivo viaja hasta el modelo

Y el compilador dejo de confiar en tu memoria: con la union discriminada
NO SE PUEDE leer la ciudad sin haber mirado antes si hubo error.
`);
}

main().catch((error) => {
  console.error("Murió el programa:", error);
  process.exit(1);
});
