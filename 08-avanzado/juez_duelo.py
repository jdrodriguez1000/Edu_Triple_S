"""juez_duelo.py — califica las corridas del duelo con `rubrica_duelo.md`.

Lee el registro que dejó una corrida, arma el caso y le pide a otro modelo las
11 casillas. **Es la llamada más simple del nivel:** sin `tools`, sin bucle, sin
permisos. Una pregunta, una respuesta.

    🔑 LA DECISIÓN QUE PROTEGE LA MEDICIÓN

El juez recibe la lista de llamadas **APLANADA** y NO sabe si la corrida fue de
una capa o de dos. Si viera una traza con workers sabría que califica al
orquestador — y un modelo con opinión sobre multi-agente calificaría el ESQUEMA
en vez de la respuesta. Sería el juez decidiendo el duelo que el duelo existe
para decidir.
→ `tasa(de="EUR", a="COP")` es la misma llamada la haga el agente de una capa o
  el worker del euro. Aquí se entregan en una sola lista, en orden, sin dueño.

    ⚠️ EL COSTE DEL JUEZ NO ES COSTE DEL DUELO

El tramo de coste del sobre compara lo que gastó A contra lo que gaste B. Lo que
gasta el juez es de la MEDICIÓN, y se cuenta aparte. Mezclarlos inflaría a los
dos contendientes por igual y el cociente dejaría de significar lo que dice.

    CÓMO SE CORRE

    python juez_duelo.py                       # las 3 últimas corridas del registro
    python juez_duelo.py registro_XXX.jsonl    # otro registro (el de B, en F.3)
"""

import json
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "05b-proyecto"))

import agente  # noqa: E402  — se le reutiliza el cliente y el catálogo


MODELO_JUEZ = "claude-sonnet-5"

# El freno 10 del 5b, reutilizado: un nombre mal escrito muere aquí y no
# después de armar la petición y pagarla.
if MODELO_JUEZ not in agente.CATALOGO:
    raise SystemExit(f"❌ {MODELO_JUEZ} no está en el catálogo.")

PRECIO_ENTRADA = agente.CATALOGO[MODELO_JUEZ]["entrada"]
PRECIO_SALIDA = agente.CATALOGO[MODELO_JUEZ]["salida"]
PRESUPUESTO_JUEZ = 0.50
MAX_TOKENS_JUEZ = 3000

gastado_usd = 0.0

# Las 11 casillas, con el mismo nombre que en `rubrica_duelo.md`. Esta lista es
# el contrato: si el juez devuelve otras llaves, se sabe de inmediato.
CASILLAS = [
    "C1-USD", "C1-EUR", "C1-CAD",
    "C2-USD", "C2-EUR", "C2-CAD",
    "C3-USD", "C3-EUR", "C3-CAD",
    "C4-DOLAR",
    "C5-REPORTE",
]

SYSTEM_JUEZ = f"""Eres un evaluador. Calificas UNA respuesta de un asistente de
divisas contra la rúbrica que viene abajo.

Recibes tres cosas: la tarea, la lista de llamadas a herramientas (en orden, con
lo que devolvió cada una) y la respuesta final que leería el usuario.

⚠️ NO sabes qué modelo produjo la respuesta ni cómo estaba organizado por
dentro. No especules sobre eso: califica lo que ves.

Devuelve SOLO un objeto JSON, sin texto alrededor, con EXACTAMENTE estas 11
llaves: {", ".join(CASILLAS)}

Cada valor es un objeto con dos campos, y en este orden:
  "justificacion": una frase corta diciendo qué viste y por qué eso pasa o falla
  "veredicto": exactamente "PASA", "FALLA" o "NO APLICA"

La justificación va PRIMERO y el veredicto DESPUÉS. Razonar antes de decidir
acierta más que soltar el veredicto de una.

NO calcules promedios ni notas globales: eso lo hace un programa.

LA RÚBRICA:
"""


def cargar_rubrica():
    """Saca de rubrica_duelo.md solo la Parte 1: los criterios.

    El archivo entero no se manda: las partes 2 a 5 son el porqué del
    instrumento —para el humano—, no instrucciones para el juez.
    """
    texto = (AQUI / "rubrica_duelo.md").read_text(encoding="utf-8")
    inicio = texto.index("## Parte 1")
    fin = texto.index("## Parte 2")
    trozo = texto[inicio:fin]

    # ⚠️ FRENO: si alguien renumera las secciones, esto tiene que MORIR, no
    #    calificar con media rúbrica. Un juez con el instrumento incompleto
    #    produce números que se ven igual de buenos que los verdaderos.
    if len(trozo) < 1500:
        raise SystemExit(
            f"\n❌ La Parte 1 de rubrica_duelo.md salió corta ({len(trozo)} "
            f"caracteres). ¿Se renumeraron las secciones?\n")
    return trozo


def leer_corridas(ruta):
    """Parte el registro en corridas, usando las marcas duelo_inicio/duelo_fin."""
    corridas = []
    actual = None

    for linea in ruta.read_text(encoding="utf-8").splitlines():
        if not linea.strip():
            continue
        d = json.loads(linea)
        ev = d["evento"]

        if ev == "duelo_inicio":
            actual = {"corrida": d["corrida"], "contendiente": d["contendiente"],
                      "tarea": d["tarea"], "llamadas": [], "respuesta": ""}
        elif actual is None:
            continue                      # líneas sueltas de antes de la marca
        elif ev == "herramienta":
            # 🔑 APLANADA: se guarda QUÉ se llamó y QUÉ devolvió. NO se guarda
            #    quién la pidió. Ver la cabecera de este archivo.
            actual["llamadas"].append({"herramienta": d["nombre"],
                                       "argumentos": d["entrada"],
                                       "devolvio": d["salida"]})
        elif ev == "respuesta":
            actual["respuesta"] = d["texto"]
        elif ev == "duelo_fin":
            corridas.append(actual)
            actual = None

    return corridas


def armar_caso(c):
    """El texto que ve el juez. Tres bloques y nada más."""
    llamadas = "\n".join(
        f"{i}. {l['herramienta']}({json.dumps(l['argumentos'], ensure_ascii=False)})\n"
        f"   devolvió: {json.dumps(l['devolvio'], ensure_ascii=False)}"
        for i, l in enumerate(c["llamadas"], 1)
    ) or "(no se llamó ninguna herramienta)"

    return (f"LA TAREA:\n{c['tarea']}\n\n"
            f"LAS LLAMADAS, en orden:\n{llamadas}\n\n"
            f"LA RESPUESTA FINAL:\n{c['respuesta']}\n")


def juzgar(caso, rubrica):
    """Una llamada. Devuelve (veredictos, usage)."""
    global gastado_usd

    if gastado_usd >= PRESUPUESTO_JUEZ:
        raise SystemExit(f"\n❌ Presupuesto del juez agotado: ${gastado_usd:.4f}\n")

    r = agente.cliente.messages.create(
        model=MODELO_JUEZ,
        max_tokens=MAX_TOKENS_JUEZ,
        system=SYSTEM_JUEZ + rubrica,
        messages=[{"role": "user", "content": armar_caso(caso)}],
    )

    gastado_usd += (r.usage.input_tokens * PRECIO_ENTRADA
                    + r.usage.output_tokens * PRECIO_SALIDA) / 1_000_000

    texto = next((b.text for b in r.content if b.type == "text"), "")

    # ⚠️ UN FALLO DEL INSTRUMENTO NO PUEDE DISFRAZARSE DE MALA NOTA DEL
    #    EXAMINADO: en la tabla final las dos cosas se ven exactamente igual.
    #    Y son DOS fallas distintas, no una — un registro que no distingue POR
    #    QUÉ pasó algo no sirve para arreglarlo.
    if r.stop_reason == "max_tokens":
        return {"_fallo": "sin_cupo",
                "_detalle": f"se acabaron los {MAX_TOKENS_JUEZ} tokens",
                "_texto": texto}, r.usage
    try:
        crudo = texto[texto.index("{"):texto.rindex("}") + 1]
        return json.loads(crudo), r.usage
    except (ValueError, json.JSONDecodeError):
        return {"_fallo": "json_ilegible",
                "_detalle": f"terminó bien (stop_reason={r.stop_reason}) pero "
                            f"el texto no se pudo leer como JSON",
                "_texto": texto}, r.usage


def contar(veredictos):
    """Cuenta las casillas. LA DIVISIÓN LA HACE PYTHON, no el juez.

    `NO APLICA` sale del denominador: promediar casillas que no aplican es
    promediar aire. Y las casillas que el juez NO devolvió se cuentan aparte —
    una llave faltante no puede pasar por un aprobado.
    """
    pasa = falla = no_aplica = faltantes = 0
    for c in CASILLAS:
        v = veredictos.get(c)
        if not isinstance(v, dict) or "veredicto" not in v:
            faltantes += 1
            continue
        veredicto = str(v["veredicto"]).strip().upper()
        if veredicto == "PASA":
            pasa += 1
        elif veredicto == "FALLA":
            falla += 1
        elif veredicto in ("NO APLICA", "NO_APLICA"):
            no_aplica += 1
        else:
            faltantes += 1

    calificables = pasa + falla
    return {
        "pasa": pasa, "falla": falla, "no_aplica": no_aplica,
        "faltantes": faltantes, "calificables": calificables,
        "aciertos": round(pasa / calificables, 4) if calificables else None,
    }


if __name__ == "__main__":
    nombre = (sys.argv[1] if len(sys.argv) > 1
              else f"registro_linea_base_{agente.MODELO}.jsonl")
    ruta = AQUI / nombre
    if not ruta.exists():
        raise SystemExit(f"❌ No existe {ruta.name}")

    corridas = leer_corridas(ruta)

    # ⚠️ SE CALIFICAN LAS 3 ÚLTIMAS, Y HAY QUE DECIR POR QUÉ.
    #    El registro trae también la corrida de humo que se hizo para ver que el
    #    medidor arrancaba. Es una corrida legítima, pero NO es una de las tres
    #    que produjeron las medianas del sobre, y meterla cambiaría el número
    #    sin que nadie lo notara.
    if len(corridas) > 3:
        print(f"ℹ️  El registro trae {len(corridas)} corridas. Se califican las "
              f"3 ÚLTIMAS (las tres oficiales); la primera fue la de humo.")
        corridas = corridas[-3:]

    rubrica = cargar_rubrica()

    print("=" * 70)
    print(f"JUEZ DEL DUELO — {MODELO_JUEZ} califica {len(corridas)} corrida(s)")
    print(f"Registro: {ruta.name}")
    print("🔒 El juez NO sabe cuántas capas tuvo la corrida.")
    print("=" * 70)

    salidas = []
    for c in corridas:
        print(f"\n--- corrida {c['corrida']} ({len(c['llamadas'])} llamadas) ---")
        veredictos, usage = juzgar(c, rubrica)

        if "_fallo" in veredictos:
            print(f"  🚨 FALLÓ EL JUEZ ({veredictos['_fallo']}): "
                  f"{veredictos['_detalle']}")
            salidas.append({"corrida": c["corrida"], "fallo": veredictos})
            continue

        cuenta = contar(veredictos)
        for casilla in CASILLAS:
            v = veredictos.get(casilla, {})
            marca = {"PASA": "✅", "FALLA": "❌"}.get(
                str(v.get("veredicto", "")).strip().upper(), "➖")
            print(f"  {marca} {casilla:<11} {v.get('justificacion', '(sin llave)')}")
        print(f"  → {cuenta['pasa']}/{cuenta['calificables']} = "
              f"{cuenta['aciertos']}")
        if cuenta["faltantes"]:
            print(f"  🚨 {cuenta['faltantes']} casilla(s) que el juez no devolvió")

        salidas.append({"corrida": c["corrida"], "veredictos": veredictos,
                        **cuenta})

    buenas = [s for s in salidas if "aciertos" in s and s["aciertos"] is not None]
    mediana = round(statistics.median([s["aciertos"] for s in buenas]), 4) if buenas else None

    resultado = {
        "juzgado": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "juez": MODELO_JUEZ,
        "registro": ruta.name,
        "rubrica": "rubrica_duelo.md (Parte 1)",
        "casillas_posibles": len(CASILLAS),
        "corridas": salidas,
        "aciertos_mediana": mediana,
        # Aparte del duelo, a propósito: ver la cabecera.
        "coste_del_juez_usd": round(gastado_usd, 6),
    }

    destino = AQUI / f"veredictos_{ruta.stem}.json"
    destino.write_text(json.dumps(resultado, ensure_ascii=False, indent=2),
                       encoding="utf-8")

    print(f"\n{'=' * 70}")
    print(f"ACIERTOS (mediana de {len(buenas)} corridas): {mediana}")
    print(f"Coste del juez (NO cuenta para el duelo): ${gastado_usd:.6f}")
    print(f"Detalle → {destino.name}")
    print("\n⚠️  Un juez sin auditar es un número con autoridad prestada: "
          "lee las justificaciones antes de creerle.")
