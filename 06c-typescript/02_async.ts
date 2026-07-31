/**
 * 02_async.ts — Nivel 6c, paso 2
 *
 * AQUÍ ES DONDE PYTHON Y TYPESCRIPT DE VERDAD SE SEPARAN.
 *
 * En Python, esta línea DETIENE el programa hasta que la API responda:
 *
 *     respuesta = client.messages.create(...)
 *
 * En JavaScript, NADA detiene el programa. Nunca. Una función que se
 * demora NO devuelve el dato: devuelve un RECIBO, ahí mismo, en el acto.
 * Y el programa sigue corriendo.
 *
 * ¿Por qué tan raro? Porque JavaScript nació en el navegador. Si una
 * llamada de red congelara la página, la página se congelaría de verdad:
 * el usuario no podría ni hacer scroll. Así que JavaScript decidió no
 * congelarse jamás. En vez de esperar, dice "yo te aviso cuando esté".
 *
 * Corre así:
 *   npx tsc
 *   node dist/02_async.js
 *
 * ⏱️ Tarda ~7 segundos a propósito. Está midiendo.
 */

// ══════════════════════════════════════════════════════════════════
//  EL SIMULADOR — no hay API en este paso, y es a propósito
// ══════════════════════════════════════════════════════════════════
// Nada de esto llama a Anthropic. Cuesta $0,00. Es la misma idea del
// nivel 6b: lo que puedes simular, no lo pagues.

/** Espera `ms` milisegundos. Es el `time.sleep()` de JavaScript. */
function dormir(ms: number): Promise<void> {
  return new Promise((listo) => setTimeout(listo, ms));
}

/** Finge ser la API del clima. Se demora 1 segundo, como una de verdad. */
async function consultarClima(ciudad: string): Promise<string> {
  await dormir(1000);
  return `${ciudad}: 18 °C, nublado`;
}

// ══════════════════════════════════════════════════════════════════
//  Todo tiene que ir dentro de una función `async`.
//  (Por qué, en el punto 3.)
// ══════════════════════════════════════════════════════════════════
async function main(): Promise<void> {
  console.log("=".repeat(60));

  // ────────────────────────────────────────────────────────────────
  //  1. 🚨 EL ERROR NÚMERO UNO DE TODO PRINCIPIANTE: olvidar `await`
  // ────────────────────────────────────────────────────────────────
  // Aquí NO hay `await`. Mira bien qué imprime.

  const sinAwait = consultarClima("Bogotá");
  console.log(`1. Sin await  →  ${sinAwait}`);

  // No imprimió el clima. Imprimió un OBJETO PROMESA: el recibo.
  //
  // 📌 Y fíjate en lo peor: NO HUBO NINGÚN ERROR. El programa siguió
  //    feliz. En un agente esto se ve como "la respuesta llegó vacía"
  //    o "[object Promise]" metido en un prompt. Nadie te avisa.

  // ────────────────────────────────────────────────────────────────
  //  2. `await` — "espérame aquí a que el recibo se vuelva dato"
  // ────────────────────────────────────────────────────────────────

  const conAwait = await consultarClima("Bogotá");
  console.log(`2. Con await  →  ${conAwait}`);

  // Misma función, misma llamada. La única diferencia es esa palabra.

  // ────────────────────────────────────────────────────────────────
  //  3. Por qué todo esto vive dentro de `async function main()`
  // ────────────────────────────────────────────────────────────────
  // `await` solo se puede usar dentro de una función marcada `async`.
  // Y una función `async` SIEMPRE devuelve una promesa, la marques o no.
  //
  // Es contagioso: si tu función espera algo, quien la llame también
  // tendrá que esperarla. Por eso el bucle agéntico entero, de arriba
  // abajo, va a estar en funciones `async`. No es capricho.

  // ────────────────────────────────────────────────────────────────
  //  4. TRES CIUDADES, UNA DETRÁS DE OTRA (lo que hace Python)
  // ────────────────────────────────────────────────────────────────

  const inicioSerie = Date.now();

  const a = await consultarClima("Bogotá");
  const b = await consultarClima("Medellín");
  const c = await consultarClima("Cali");

  const serie = Date.now() - inicioSerie;
  console.log(`4. En serie   →  ${serie} ms   (${a.slice(0, 6)}…, ${b.slice(0, 8)}…, ${c.slice(0, 4)}…)`);

  // Cada `await` espera a que termine el anterior. 1s + 1s + 1s.

  // ────────────────────────────────────────────────────────────────
  //  5. ⭐ LAS TRES A LA VEZ — esto Python no lo hace de gratis
  // ────────────────────────────────────────────────────────────────
  // Fíjate: NO hay `await` en las tres primeras líneas. Se lanzan las
  // tres y se guardan los tres recibos. El `await` es UNO SOLO, al
  // final, sobre los tres juntos.

  const inicioParalelo = Date.now();

  const recibo1 = consultarClima("Bogotá");
  const recibo2 = consultarClima("Medellín");
  const recibo3 = consultarClima("Cali");

  const [x, y, z] = await Promise.all([recibo1, recibo2, recibo3]);

  const paralelo = Date.now() - inicioParalelo;
  console.log(`5. En paralelo → ${paralelo} ms   (${x.slice(0, 6)}…, ${y.slice(0, 8)}…, ${z.slice(0, 4)}…)`);
  console.log(`   → ${(serie / paralelo).toFixed(1)}x más rápido, mismas 3 llamadas`);

  // 🔑 Aquí "no bloquear" dejó de ser una molestia y se volvió la
  //    ventaja. En Python esto necesita asyncio; aquí es lo normal.

  // ────────────────────────────────────────────────────────────────
  //  6. try / catch — el `try/except` del nivel 4, en TypeScript
  // ────────────────────────────────────────────────────────────────

  async function consultarQueFalla(): Promise<string> {
    await dormir(200);
    throw new Error("APIConnectionError: no se pudo conectar");
  }

  try {
    await consultarQueFalla();
    console.log("6. Esto NO se imprime");
  } catch (error) {
    // ⚠️ En TypeScript, lo que atrapas es de tipo `unknown`, no `Error`.
    //    Porque en JavaScript se puede lanzar CUALQUIER COSA, no solo
    //    errores. Así que primero hay que comprobar qué llegó.
    const mensaje = error instanceof Error ? error.message : String(error);
    console.log(`6. Atrapado   →  ${mensaje}`);
  }

  // 📌 Sin el `await` de la línea del try, el error se escaparía del
  //    catch: el `throw` pasa DESPUÉS, y para entonces el try ya cerró.
  //    Es el ejercicio 4.

  console.log("=".repeat(60));
}

// ══════════════════════════════════════════════════════════════════
//  Y esta última línea es obligatoria: hay que ARRANCAR la promesa.
// ══════════════════════════════════════════════════════════════════
// `main()` devuelve una promesa. Si nadie la mira y algo falla adentro,
// el error desaparece en silencio. El `.catch` es el seguro.

main().catch((error) => {
  console.error("Murió el programa:", error);
  process.exit(1);
});
