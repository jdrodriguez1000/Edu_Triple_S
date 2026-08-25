"""duelo.py — F.3 del nivel 8: EL CONTENDIENTE B Y EL APLANADOR.

    LA FRASE QUE HAY QUE VER

El duelo lleva sellado desde el bloque 0. Lo que faltaba no era correrlo: era
**la pieza que le pone la venda al juez**, y no existía.

`linea_base.py` (contendiente A, una capa) escribe en su registro llamadas a
`tasa`, `convertir` y `guardar_reporte`. El orquestador (contendiente B, dos
capas) escribe en el suyo llamadas a `consultar_moneda` y `consultar_region`,
que **no son herramientas: son los workers disfrazados de herramienta**.

🚨 Si al juez se le entrega el registro de B tal cual, no tiene que deducir nada:
   **el vocabulario de la primera línea le dice que hay dos capas.** Y la Parte 0
   de `rubrica_duelo.md` lo prohíbe con su razón escrita — *«un modelo con
   opinión sobre multi-agente califica el esquema en vez de la respuesta»*.
   Sería el juez decidiendo el duelo que el duelo existe para decidir.

🔑 POR ESO EL TRABAJO DE F.3 NO ES CORRER EL DUELO: ES ESCRIBIR EL APLANADOR.
   Y no es «juntar los dos registros». Es **tirar** las llamadas de frontera y
   quedarse con las herramientas de verdad, que viven en el registro de los
   workers. La decisión estaba tomada desde el bloque 0, en la docstring de
   `juez_duelo.leer_corridas()`: *«APLANADA: se guarda QUÉ se llamó y QUÉ
   devolvió. NO se guarda quién la pidió.»* Faltaba quien la cumpliera.


    EL ORDEN DE LA LISTA, Y POR QUÉ NO ES LA HORA

`hora` se graba con `timespec="seconds"`. En una corrida entera caben decenas de
eventos en el mismo segundo, así que ordenar por hora **no ordena**: deja el
empate en manos del azar, y el criterio C1 de la rúbrica pregunta justamente si
`tasa` vino ANTES que `convertir` para cada moneda.

→ Se ordena por TRAMO: dentro del registro de los workers, las llamadas de un
  worker ya están en orden de archivo; y los workers se concatenan en el orden
  en que el orquestador los pidió (el orden de sus `consultar_*`).
  Así la secuencia por moneda —que es lo que se califica— se conserva exacta, y
  el orden entre monedas es el que hubo de verdad.

⚠️ Y con el reparto en paralelo las monedas se solapan en el tiempo real. La
   lista aplanada las presenta agrupadas, no entrelazadas. **Es una decisión, no
   un descuido**: A tampoco entrelaza —tiene un solo hilo—, y presentar a B
   entrelazado le enseñaría al juez que hubo concurrencia, que es otra manera de
   quitarle la venda.


    LO QUE ESTE ARCHIVO NO HACE

- No vuelve a correr al contendiente A. Ya está medido y ya costó.
- No juzga: eso es `juez_duelo.py`, y se le llama después, aparte.
- No abre el sobre.
"""
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(AQUI.parent / "05b-proyecto"))

import agente          # noqa: E402
import compartida      # noqa: E402
import contexto        # noqa: E402
import linea_base      # noqa: E402
import orquestador     # noqa: E402
import worker          # noqa: E402

# ⭐ APUESTA 3 — LA TAREA SE IMPORTA, NO SE COPIA.
#    `orquestador.TAREA_DEMO` NO es esta: le falta *«y guárdame el reporte»*, o
#    sea una herramienta menos. Correr B con la demo sería compararlo contra A en
#    una tarea más fácil — **regalarle el duelo**, y de una forma que no se ve
#    leyendo el resultado. Importarla es lo que hace imposible que se separen.
TAREA = linea_base.TAREA
CORRIDAS = linea_base.CORRIDAS

REGISTRO = AQUI / f"registro_duelo_{agente.MODELO}.jsonl"

# 🚧 LAS LLAMADAS DE FRONTERA: los workers vestidos de herramienta.
#    Esto NO es «lo que no nos interesa»: es la línea donde un agente se vuelve
#    una herramienta (el puente de A.3). Tirarlas es exactamente lo que pone la
#    venda; tirar una de más deja a B más limpio de lo que fue.
FRONTERA = {"consultar_moneda", "consultar_region"}


# ---------------------------------------------------------------------------
# 1) EL APLANADOR
# ---------------------------------------------------------------------------
def _leer(ruta):
    """Las líneas de un `.jsonl`, saltándose las rotas sin morir.

    📌 Una línea partida no invalida las demás — y en este nivel hay una de
       verdad, la 626 de `registro_pruebas_gratis.jsonl`, que se dejó partida a
       propósito porque es la evidencia del bicho de E.1.
    """
    if not Path(ruta).exists():
        return []
    fuera = []
    for linea in Path(ruta).read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea:
            continue
        try:
            fuera.append(json.loads(linea))
        except json.JSONDecodeError:
            continue
    return fuera


def aplanar(corrida, eventos_orq, eventos_wrk):
    """La lista de llamadas de B con la MISMA pinta que la de A.

    Devuelve `(llamadas, tiradas)`:
      · `llamadas` — herramientas de verdad, en orden, sin dueño
      · `tiradas`  — lo que se dejó fuera, para poder EXIGIR que todo sea frontera

    🔑 Se devuelven las dos. Un aplanador que solo devuelve lo que conserva no se
       puede auditar: «se cayó una `tasa` por el camino» y «no hubo `tasa`» se
       leen igual. Es `LM.100` — la ausencia tiene que poder distinguirse.
    """
    # 🐛 ESTA FUNCIÓN SE REESCRIBIÓ ENTERA, Y LA CAZÓ LA PRUEBA 7.
    #    La primera versión iba en dos fases: primero apuntaba el orden de los
    #    workers, luego concatenaba sus llamadas. Y tenía una rama `else` con un
    #    `pass` y este comentario encima: *«si mañana la capa de arriba llama a
    #    `tasa` directamente, esta rama la deja pasar en vez de tirarla en
    #    silencio»*. **Hacía exactamente lo contrario: la tiraba en silencio.**
    # 🔑 Es el bicho de la sesión 111 otra vez —una docstring que blinda el
    #    hueco que describe— y esta vez con `pass` en vez de una lista corta.
    #    Un comentario no es una defensa: la prueba 7 sí.
    # ✅ La versión buena es además MÁS SIMPLE: se recorre el registro de arriba
    #    en orden y, cuando aparece una llamada de frontera, se INJERTAN ahí las
    #    llamadas del worker al que llamaba. Una sola pasada, y el orden sale
    #    solo: es el orden en que ocurrieron.
    llamadas, tiradas, injertados = [], [], set()

    # Las llamadas de cada worker, en orden de archivo.
    por_worker = {}
    for e in eventos_wrk:
        if e.get("corrida") != corrida or e.get("evento") != "herramienta":
            continue
        if e.get("nombre") in FRONTERA:
            tiradas.append(e)
            continue
        quien = str(e.get("worker") or e.get("tramo") or "?").lower()
        por_worker.setdefault(quien, []).append(e)

    for e in eventos_orq:
        if e.get("corrida") != corrida or e.get("evento") != "herramienta":
            continue
        if e.get("nombre") not in FRONTERA:
            # Una herramienta DE VERDAD llamada por la capa de arriba. Hoy no
            # pasa nunca (medido: 0 casos en 7 corridas), pero si pasa se
            # conserva en su sitio. Antes se perdía sin dejar rastro.
            llamadas.append(e)
            continue

        tiradas.append(e)
        entrada = e.get("entrada") or {}
        destino = str(entrada.get("moneda") or entrada.get("region") or "").lower()
        if destino in por_worker and destino not in injertados:
            llamadas.extend(por_worker[destino])
            injertados.add(destino)

    # Lo que no se supo emparejar va al final, NO se descarta. Perder una
    # llamada por no saber dónde ponerla sería el mismo bicho con mejor
    # educación — y es justo el que acaba de cazar la prueba 7.
    for quien, lista in por_worker.items():
        if quien not in injertados:
            llamadas.extend(lista)

    return llamadas, tiradas


def vocabulario(llamadas):
    """Los nombres de herramienta que aparecen. Es lo que delata la capa."""
    return {l.get("nombre") for l in llamadas}


# ---------------------------------------------------------------------------
# 2) UNA CORRIDA DEL CONTENDIENTE B
# ---------------------------------------------------------------------------
def _anotar_duelo(evento, **datos):
    """Escribe en el registro DEL DUELO, con el candado de la sesión 112."""
    compartida.anotar_linea(REGISTRO, {
        "hora": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "evento": evento, **datos})


def una_corrida(numero, tarea=TAREA):
    """Corre B una vez y deja en el registro del duelo lo que el juez verá.

    ⚠️ El aplanado se hace DESPUÉS de la corrida, leyendo los dos registros de
       verdad. No se toca el orquestador ni el worker: sus registros siguen
       siendo lo que eran, con dueño y con capas. **La venda es una vista, no
       una mutilación de los datos.** Si mañana hace falta saber quién pidió
       qué, sigue estando.
    """
    orquestador.gastado_usd = 0.0

    with contexto.tramo(f"duelo-b-{numero}") as marca:
        corrida = marca["corrida"]
        arranque = time.perf_counter()
        r = orquestador.correr_orquestador(tarea, verboso=True)
        segundos = time.perf_counter() - arranque

    eventos_orq = _leer(orquestador.REGISTRO)
    eventos_wrk = _leer(worker.REGISTRO)
    llamadas, tiradas = aplanar(corrida, eventos_orq, eventos_wrk)

    # 🚨 EL FRENO QUE PROTEGE LA VENDA, Y VA AQUÍ Y NO EN UNA PRUEBA.
    #    Una prueba se corre cuando alguien se acuerda. Esto se corre SIEMPRE, y
    #    revienta ANTES de escribir: más vale una corrida pagada que se cae que
    #    un duelo entero medido con el juez viendo las capas.
    intrusos = vocabulario(llamadas) & FRONTERA
    if intrusos:
        raise RuntimeError(
            f"la venda está rota: la lista de B contiene {sorted(intrusos)}")

    _anotar_duelo("duelo_inicio", contendiente="B_dos_capas", corrida=numero,
                  modelo=agente.MODELO,
                  max_vueltas_orquestador=orquestador.MAX_VUELTAS_ORQ,
                  max_vueltas_worker=worker.MAX_VUELTAS_WORKER,
                  tarea=tarea, corrida_interna=corrida)

    for l in llamadas:
        _anotar_duelo("herramienta", corrida=numero, nombre=l.get("nombre"),
                      entrada=l.get("entrada"), salida=l.get("salida"))

    _anotar_duelo("respuesta", corrida=numero, texto=r["texto"])
    _anotar_duelo("duelo_fin", contendiente="B_dos_capas", corrida=numero,
                  segundos=round(segundos, 2),
                  gastado_usd=r["coste_total_usd"],
                  coste_orquestador_usd=r["coste_orquestador_usd"],
                  coste_workers_usd=r["coste_workers_usd"],
                  llamadas_api=r["llamadas_api_orquestador"]
                  + r["llamadas_api_workers"],
                  llamadas_vistas_por_el_juez=len(llamadas),
                  llamadas_de_frontera_tiradas=len(tiradas))

    return {"corrida": numero, "segundos": round(segundos, 2),
            "usd": r["coste_total_usd"], "respuesta": r["texto"],
            "vistas": len(llamadas), "tiradas": len(tiradas)}


# ---------------------------------------------------------------------------
# 3) LAS PRUEBAS — gratis, y sobre las 7 corridas PAGADAS que ya hay en disco
# ---------------------------------------------------------------------------
# ⭐ Este archivo tiene una suerte que casi ningún otro tuvo: el aplanador se
#    puede probar entero **sobre datos reales y ya pagados**, sin llamar a nadie.
#    Los registros del orquestador y de los workers llevan 7 corridas de las dos
#    capas desde el bloque C. Probarlo con datos inventados habría sido
#    exactamente `LM.104`: un experimento más limpio que la realidad.
def _pruebas():
    fallos = []

    def check(nombre, cond, detalle=""):
        print(("  ✅  " if cond else "  ❌  ") + nombre
              + (f"  -> {detalle}" if detalle else ""))
        if not cond:
            fallos.append(nombre)

    print("\n[F.3] el aplanador — sobre las corridas reales del bloque C\n")

    eo = _leer(orquestador.REGISTRO)
    ew = _leer(worker.REGISTRO)
    reales = [c for c in {e.get("corrida") for e in eo if e.get("corrida")}
              if any(e.get("corrida") == c and e.get("evento") == "herramienta"
                     for e in eo)]
    reales.sort()

    check("1. hay corridas reales de DOS capas con las que probar",
          len(reales) >= 3, f"{len(reales)} corridas")

    todas, todas_tiradas = [], []
    for c in reales:
        ll, ti = aplanar(c, eo, ew)
        todas.append((c, ll))
        todas_tiradas.extend(ti)

    # 🚨 2 — LA PRUEBA DEL DÍA. Es la apuesta 1, y es lo único que separa un
    #    duelo medido de uno decidido por el vocabulario.
    sucias = [c for c, ll in todas if vocabulario(ll) & FRONTERA]
    check("2. 🚨 NINGUNA lista lleva una llamada de frontera (la venda, puesta)",
          sucias == [], sucias)

    # 3 — El otro lado: que todo lo tirado sea frontera. Sin esto, la 2 se
    #     cumple tirándolo todo.
    no_frontera = [t.get("nombre") for t in todas_tiradas
                   if t.get("nombre") not in FRONTERA]
    check("3. ⭐ y TODO lo que se tiró era frontera: no se cayó ni una "
          "herramienta de verdad",
          no_frontera == [], no_frontera)

    # 4 — El vocabulario de B tiene que salir del mismo saco que el de A.
    ea = _leer(linea_base.REGISTRO)
    voc_a = {e.get("nombre") for e in ea if e.get("evento") == "herramienta"}
    voc_b = set().union(*[vocabulario(ll) for _, ll in todas]) if todas else set()
    check("4. 🚨 el vocabulario de B ⊆ el de A: el juez no puede distinguirlos",
          voc_b <= voc_a, f"B={sorted(voc_b)}  A={sorted(voc_a)}")

    # 5 — Y no se vació: una lista vacía cumpliría 2, 3 y 4 a la vez.
    vacias = [c for c, ll in todas if not ll]
    check("5. ⭐ y ninguna lista quedó vacía (una vacía cumpliría 2, 3 y 4)",
          vacias == [], vacias)

    # 6 — El orden por moneda, que es lo que califica el criterio C1.
    desordenadas = []
    for c, ll in todas:
        vistos = {}
        for i, l in enumerate(ll):
            ent = l.get("entrada") or {}
            moneda = ent.get("de") or ent.get("moneda")
            if l.get("nombre") == "tasa" and moneda:
                vistos.setdefault(moneda, i)
            if l.get("nombre") == "convertir" and moneda:
                if moneda in vistos and vistos[moneda] > i:
                    desordenadas.append((c, moneda))
    check("6. `tasa` viene antes que `convertir` para cada moneda (criterio C1)",
          desordenadas == [], desordenadas)

    # 7 — MUERDE: si se le quita la frontera al conjunto, la 2 tiene que caerse.
    #     Un aplanador que no se puede romper no ha demostrado que aplane.
    global FRONTERA
    guardado = FRONTERA
    try:
        FRONTERA = set()
        rotas = [c for c in reales
                 if vocabulario(aplanar(c, eo, ew)[0]) & guardado]
        check("7. 🚨 MUERDE: sin la lista de frontera, las llamadas de los "
              "workers se cuelan y la venda se cae",
              len(rotas) >= 1, f"{len(rotas)} corridas se ensucian")
    finally:
        FRONTERA = guardado

    # 8 — Y la tarea, que es la apuesta 3 y no se comprueba corriendo nada.
    check("8. ⭐ B corre la MISMA tarea que A, importada y no copiada",
          TAREA is linea_base.TAREA and TAREA != orquestador.TAREA_DEMO,
          f"demo≠tarea: {TAREA != orquestador.TAREA_DEMO}")

    print()
    if fallos:
        print(f"  ❌ {len(fallos)} en rojo: {', '.join(fallos)}")
        return 1
    print("  ✅ todas en verde, y no costaron nada.")
    return 0


if __name__ == "__main__":
    print("=" * 70)
    print("F.3 — EL DUELO. Contendiente B: el orquestador de DOS capas.")
    print("=" * 70)

    if "--pruebas" in sys.argv:
        raise SystemExit(_pruebas())

    cuantas = next((int(a) for a in sys.argv[1:] if a.isdigit()), CORRIDAS)

    print(f"Modelo: {agente.MODELO}   ·   corridas: {cuantas}")
    print(f"Tarea:  {TAREA}")
    print("=" * 70)

    # 🔒 El freno de la sesión 112, que nació de correr un archivo como este
    #    "para ver si seguía sano".
    compartida.exigir_pagar(
        "python duelo.py",
        f"Corre {cuantas} veces el orquestador de DOS capas contra la API.",
        archivo_precio=orquestador.REGISTRO, campo="coste_total_usd",
        tambien_pisa=[f"{REGISTRO.name} — el registro del duelo"])

    resultados = [una_corrida(n) for n in range(1, cuantas + 1)]

    print("\n" + "=" * 70)
    print("CONTENDIENTE B — LO QUE COSTÓ")
    print("=" * 70)
    for r in resultados:
        print(f"  corrida {r['corrida']}: {r['segundos']:>6.2f}s · "
              f"${r['usd']:.6f} · {r['vistas']} llamadas vistas por el juez "
              f"({r['tiradas']} de frontera, tiradas)")
    total = sum(r["usd"] for r in resultados)
    print(f"  {'TOTAL':>11}: ${total:.6f}")
    print(f"\n📄 registro del duelo: {REGISTRO.name}")
    print(f"\n▶ Ahora el juez:  python juez_duelo.py {REGISTRO.name} --pagar")
