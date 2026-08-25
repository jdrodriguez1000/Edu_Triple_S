"""linea_base.py — la línea base del duelo: el CONTENDIENTE A, tres veces.

    QUÉ MIDE, Y POR QUÉ SE MIDE HOY

Mide al agente de UNA capa (el del 5b) contra la tarea del duelo, y guarda tres
números: TIEMPO, COSTE y las LLAMADAS que hizo (para que después las califique
el juez con `rubrica_duelo.md`).

🚨 Se mide AHORA, antes de que exista una sola línea del orquestador. Tomada al
   final ya no sería línea base, sería un recuerdo — y perder una línea base ya
   pagada es `L7.8`, que en TEAPP costó dinero de verdad.

    POR QUÉ EL AGENTE DEL 5b Y NO EL DEL 6b

El del 6b lleva MEMORIA y SKILLS. Ninguna de las dos entra en la tarea del duelo,
y las dos cuestan tokens en cada vuelta. Meterlas aquí sería cargarle al agente
de una capa un peso que su rival no lleva.
→ Contendiente A = `05b-proyecto/agente.py`, seis herramientas, sin más.

    TRES CORRIDAS, Y SE TOMA LA MEDIANA

Con una sola no se puede evaluar el tramo de tiempo: no se sabría cuánto varía A
consigo mismo, así que no se podría distinguir una victoria de una casualidad.
Tres corridas de haiku sobre siete llamadas cuestan centavos.

    CÓMO SE CORRE

    python linea_base.py            # las tres corridas
    python linea_base.py 1          # una sola (para probar que arranca)
"""

import json
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

AQUI = Path(__file__).resolve().parent

# El contendiente A vive en otra carpeta del curso. Se importa, no se copia:
# una copia se desincroniza el día que alguien toque el original, y entonces la
# línea base mediría un agente que ya no existe.
sys.path.insert(0, str(AQUI.parent / "05b-proyecto"))

import agente          # noqa: E402
import compartida
import herramientas    # noqa: E402


# ---------------------------------------------------------------------------
# 1) DESVIAR LO QUE ESCRIBE EN DISCO  — y esto NO es un detalle de limpieza
# ---------------------------------------------------------------------------
# 🚨 ES LA LECCIÓN DE LA SESIÓN 50 DE TEAPP, APLICADA ANTES DE QUE MUERDA.
#    Allá, el camino que estaba escribiendo en los datos de verdad resultó ser
#    `measure_body.py`: LA PROPIA BÁSCULA. El instrumento de medida ensuciando
#    lo que medía.
#
#    Aquí pasaría lo mismo por dos puertas distintas:
#      · `agente.REGISTRO` apunta a `05b-proyecto/registro_<modelo>.jsonl`, que
#        es la EVIDENCIA del nivel 5b. Estas corridas se le mezclarían dentro.
#      · `herramientas.CAJA` apunta a `05b-proyecto/caja/`, donde el agente
#        guarda los reportes.
#
#    Se reasignan las dos, y se reasignan AQUÍ ARRIBA: si se hiciera a mitad del
#    archivo, la primera corrida ya habría escrito en el sitio equivocado.
REGISTRO = AQUI / f"registro_linea_base_{agente.MODELO}.jsonl"
agente.REGISTRO = REGISTRO
herramientas.CAJA = AQUI / "caja"

# ---------------------------------------------------------------------------
# 2) LA TAREA — copiada TEXTUAL del sobre
# ---------------------------------------------------------------------------
# ⚠️ Si esta cadena y la de `SOBRE.md` dejan de ser la misma, el sello queda
#    anulado y nadie se entera: es la misma cosa escrita en dos sitios (el bicho
#    de la sesión 33). Al abrir el sobre, esto se compara a mano.
TAREA = ("Tengo 1.000 dólares, 1.000 euros y 1.000 dólares canadienses. "
         "Dime cuánto es cada uno en pesos hoy, con la fuente y la fecha de "
         "cada cifra, y guárdame el reporte.")

CORRIDAS = 3

# ⭐ MÁS VUELTAS QUE LAS 8 DE FÁBRICA, Y HAY QUE DECIR POR QUÉ.
#    La tarea necesita ~7 llamadas (tasa+convertir por moneda, y guardar). Con
#    el tope en 8, una corrida que pida las herramientas de una en una se queda
#    SIN vuelta para redactar la respuesta final — y estaríamos midiendo el
#    tope, no al agente.
#    → Se sube a 12 y se ESCRIBE AL LADO DEL NÚMERO. Una medición no vale sola:
#      vale contra la configuración con la que se tomó.
#    🚨 El contendiente B tendrá que correr con el mismo tope.
MAX_VUELTAS = 12


def permiso_automatico(nombre, argumentos, autorizadas):
    """Concede todo, sin preguntar.

    La tarea pide guardar un reporte, y `guardar_reporte` pide permiso. Un
    humano tecleando "sí" metería SU tiempo de reacción dentro del cronómetro,
    que es justo el número que estamos midiendo.

    ⚠️ Se concede a propósito, y B correrá igual. La rama del permiso NEGADO
       (el "ya lo guardé" que es mentira, `L4.9`) no es lo que este duelo mide.
    """
    return True, "automatico_duelo"


def una_corrida(numero):
    """Corre la tarea UNA vez y devuelve sus tres números."""
    # El gasto es un global del módulo y se acumula entre corridas. Sin este
    # reinicio, la corrida 3 arrancaría con el presupuesto casi agotado y se
    # cortaría sola — un fallo que además parecería del agente.
    agente.gastado_usd = 0.0

    # La marca de inicio va al registro ANTES de la primera llamada: es lo que
    # después permite recortar del .jsonl las líneas de ESTA corrida y no de la
    # de al lado.
    agente.anotar("duelo_inicio", contendiente="A_una_capa", corrida=numero,
                  modelo=agente.MODELO, max_vueltas=MAX_VUELTAS,
                  herramientas=len(agente.HERRAMIENTAS)
                  if hasattr(agente, "HERRAMIENTAS") else None,
                  tarea=TAREA)

    print(f"\n{'=' * 70}")
    print(f"CORRIDA {numero} de {CORRIDAS}  ·  contendiente A (una capa)")
    print(f"{'=' * 70}")

    # perf_counter y no datetime: mide tiempo transcurrido de verdad, y no se
    # descuadra si el reloj del sistema se ajusta a mitad de la corrida.
    arranque = time.perf_counter()
    respuesta = agente.ejecutar_agente(
        TAREA,
        max_vueltas=MAX_VUELTAS,
        preguntar=permiso_automatico,
    )
    segundos = time.perf_counter() - arranque
    usd = round(agente.gastado_usd, 6)

    agente.anotar("duelo_fin", contendiente="A_una_capa", corrida=numero,
                  segundos=round(segundos, 2), gastado_usd=usd)

    print(f"\nRESPUESTA FINAL:\n{respuesta}")
    print(f"\n⏱️  {segundos:.2f} s     💰 ${usd:.6f}")

    return {"corrida": numero, "segundos": round(segundos, 2),
            "usd": usd, "respuesta": respuesta}


if __name__ == "__main__":
    # Los argumentos se leen de primeras: lo que decide CÓMO va a correr el
    # programa se lee antes de que el programa haga nada.
    cuantas = int(sys.argv[1]) if len(sys.argv) > 1 else CORRIDAS

    print("=" * 70)
    print("LÍNEA BASE DEL DUELO — contendiente A: el agente de UNA capa")
    print(f"Modelo: {agente.MODELO}   ·   corridas: {cuantas}   ·   "
          f"max_vueltas: {MAX_VUELTAS}")
    print(f"Tarea: {TAREA}")
    print("=" * 70)

    # 🔒 SESIÓN 112 — el freno que faltaba, y aquí es el que más falta hacía:
    #    esto no solo paga, REHACE la contrincante sellada del duelo de F.3.
    compartida.exigir_pagar(
        "python linea_base.py",
        f"Corre {cuantas} veces el agente de UNA capa contra la API de verdad.",
        archivo_precio=REGISTRO,
        tambien_pisa=[
            f"linea_base_{agente.MODELO}.json — la línea base medida el "
            "2026-08-20, contrincante del duelo de F.3",
        ])

    resultados = [una_corrida(n) for n in range(1, cuantas + 1)]

    tiempos = [r["segundos"] for r in resultados]
    costes = [r["usd"] for r in resultados]

    # La MEDIANA y no el promedio: con tres corridas, una sola con un hipo de
    # red se lleva el promedio y no toca la mediana. Se quiere el caso típico,
    # no el caso arrastrado.
    resumen = {
        "medido": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "contendiente": "A_una_capa",
        # ⭐ La configuración viaja PEGADA al número. Un tiempo sin saber con qué
        #    modelo, con cuántas herramientas y con qué tope se tomó, es un
        #    número que miente solo.
        "configuracion": {
            "agente": "05b-proyecto/agente.py",
            "modelo": agente.MODELO,
            "herramientas": 6,
            "max_vueltas": MAX_VUELTAS,
            "memoria": "no aplica (el 5b no la tiene)",
            "skills": "no aplica (el 5b no las tiene)",
            "permisos": "concedidos automáticamente",
            "tarea": TAREA,
        },
        "corridas": resultados,
        "segundos_mediana": round(statistics.median(tiempos), 2),
        "usd_mediana": round(statistics.median(costes), 6),
        "usd_total_gastado": round(sum(costes), 6),
    }

    salida = AQUI / f"linea_base_{agente.MODELO}.json"
    salida.write_text(json.dumps(resumen, ensure_ascii=False, indent=2),
                      encoding="utf-8")

    print(f"\n\n{'=' * 70}")
    print("RESUMEN — LÍNEA BASE (contendiente A)")
    print("=" * 70)
    for r in resultados:
        print(f"  corrida {r['corrida']}:  {r['segundos']:>6.2f} s   "
              f"${r['usd']:.6f}")
    print(f"\n  MEDIANA tiempo : {resumen['segundos_mediana']} s")
    print(f"  MEDIANA coste  : ${resumen['usd_mediana']:.6f}")
    print(f"  Gasto total    : ${resumen['usd_total_gastado']:.6f}")
    print(f"\n  Números  → {salida.name}")
    print(f"  Llamadas → {REGISTRO.name}   (las califica el juez en 0.4/F)")
    print("\n⚠️  Los ACIERTOS todavía no están medidos: falta pasarle estas "
          "corridas al juez.")
