"""fan_out.py — B.2 del nivel 8: FAN-OUT / FAN-IN.

    B.1 (pipeline): la salida de uno entra al siguiente.  Tiempo = LA SUMA.
    B.2 (fan-out):  los pedazos no se necesitan entre sí.  Tiempo = EL MÁXIMO.


    LA FRASE QUE HAY QUE VER

En la corrida de A.2 el orquestador pidió las TRES monedas en UN SOLO TURNO.
Tres bloques `tool_use` en la vuelta 1. El modelo hizo el fan-out perfecto.

Y aun así tardó 20,02 s, porque abajo se ejecutaban en un `for`.

⭐ «PIDIÓ TRES A LA VEZ» Y «CORRIERON TRES A LA VEZ» SON COSAS DISTINTAS.
   Quien decide si algo corre en paralelo es EL HARNESS, nunca el modelo. El
   modelo solo puede pedirlo. Este archivo es el harness diciendo que sí.


    LO QUE EL FAN-OUT COMPRA, Y LO QUE NO

   ⏱️ COMPRA TIEMPO:  de la suma al máximo. Manda el más lento.
   💰 NO COMPRA NADA: son EXACTAMENTE las mismas llamadas, con los mismos
                      tokens y el mismo precio. Ni un centavo de diferencia.

⚠️ Confundir esas dos es el error clásico del tema. El paralelismo no es una
   optimización de costo: es una optimización de RELOJ. Si lo que duele es la
   factura, el fan-out no sirve para nada — eso es C.6 (modelo por capa), que
   es 5×.


    LA CONDICIÓN, Y ES LA ÚNICA

Los pedazos tienen que ser INDEPENDIENTES. El dólar no necesita saber nada del
euro. Si el segundo encargo necesitara el resultado del primero, no hay fan-out
posible: eso es un pipeline, y su tiempo es la suma por definición.

📌 Por eso la tarea del duelo SÍ sirve aquí y NO servía en B.1. La forma de la
   tarea decide la topología, no al revés.


    EL PARALELISMO NO SE AÑADE: SE DESBLOQUEA

Lo que había que arreglar no era la velocidad. Era LO COMPARTIDO. Tres hilos
tropiezan con tres cosas que en serie no eran de nadie:

   1. EL ARCHIVO DE REGISTRO  -> dos líneas se entrelazan, el .jsonl se rompe.
                                 Arreglo: `_CANDADO_REGISTRO`.
   2. LA CONTABILIDAD         -> `d[k] += x` son TRES operaciones; una suma se
                                 pierde SIN dar error. Arreglo: candado.
   3. LA PANTALLA             -> tres conversaciones encimadas, ilegibles.
                                 ⚠️ Esta NO se arregla con un candado: un
                                 candado sobre la pantalla vuelve a poner en
                                 fila justo lo que querías en paralelo.
                                 Arreglo: no imprimir en vivo, y dibujar la
                                 LÍNEA DE TIEMPO al final — que además es el
                                 único sitio donde el solapamiento SE VE.

🔑 Las tres son la misma idea: en serie, "compartido" y "mío" no se distinguen,
   porque solo hay uno. El paralelismo no crea los recursos compartidos — los
   DESTAPA.


    CÓMO SE CORRE

    python fan_out.py --test        <- 8 pruebas, sin modelo y sin red. $0,00
    python fan_out.py --paralelo    <- una corrida en paralelo
    python fan_out.py --ambos       <- serie Y paralelo, seguidas  (RECOMENDADO)

💰 `--ambos` cuesta el doble (~$0,05) y es el único que mide de verdad: la misma
   tarea, el mismo modelo, el mismo día, y UNA sola variable cambiada. Comparar
   contra los 20,02 s sellados de la sesión 91 es más barato y más flojo — hay
   ±12 % de ruido medido (sesión 90) y el modelo puede dar otro número de
   vueltas. 📌 La diferencia esperada es grande (suma contra máximo), así que
   probablemente saldría igual; "probablemente" es exactamente lo que `--ambos`
   quita de en medio.
"""

import argparse
import json
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "05b-proyecto"))

import orquestador     # noqa: E402
import worker          # noqa: E402


# ---------------------------------------------------------------------------
# 1) CONFIGURACIÓN
# ---------------------------------------------------------------------------

# ⚠️ UN TOPE DE HILOS, Y NO ES DECORATIVO.
#    "Paralelo" sin tope significa: si el modelo pide 40 monedas, salen 40
#    peticiones a la API a la vez. Eso es un 429 (demasiadas peticiones) y, peor,
#    es una forma NUEVA de quemar dinero que en serie no existía — en fila, el
#    presupuesto de arriba te frena antes de la número 20; a la vez, las 40 ya
#    salieron.
#    🔑 El paralelismo mueve el gasto de "poco a poco" a "todo de golpe", y un
#       tope que se mira ANTES no es lo mismo que uno que se mira DESPUÉS.
#    📌 Esto es media pieza C.2 asomando, igual que A.2 asomó C.3.
MAX_EN_VUELO = 4


# Lo que midió cada hilo: (id, etiqueta, t_inicio, t_fin), en segundos desde que
# arrancó el reparto. Se llena bajo candado y se dibuja al final.
_CANDADO_TIEMPOS = threading.Lock()
ULTIMA_LINEA_DE_TIEMPO = []
_CONTADOR_VUELTAS = {"n": 0}


def reiniciar_linea_de_tiempo():
    """Se llama al EMPEZAR una corrida, no al terminar un reparto.

    ⚠️ La diferencia importa: un orquestador puede repartir varias veces en una
       misma corrida, y las barras de todas esas vueltas cuentan la misma
       historia. Borrar entre vueltas sería el defecto `D-B2.1` con otro
       disfraz.
    """
    global ULTIMA_LINEA_DE_TIEMPO
    with _CANDADO_TIEMPOS:
        ULTIMA_LINEA_DE_TIEMPO = []
        _CONTADOR_VUELTAS["n"] = 0


# ---------------------------------------------------------------------------
# 2) EL REPARTO EN PARALELO — la pieza entera de B.2
# ---------------------------------------------------------------------------

def reparto_en_paralelo(bloques, contabilidad, verboso=True):
    """El mismo trabajo que `reparto_en_serie`, a la vez.

    Recibe lo mismo, devuelve lo mismo, en el mismo orden. Es intercambiable
    con el de serie sin que el bucle del orquestador se entere — que es justo
    lo que se buscaba al sacar el `for` a un parámetro.

    ⭐ SON DIEZ LÍNEAS. El bloque B no es difícil por el paralelismo: es difícil
       por saber CUÁNDO se puede usar (la independencia) y por lo compartido.
    """
    if not bloques:
        return []

    arranque = time.monotonic()
    tiempos = []

    def trabajo(bloque):
        t0 = time.monotonic() - arranque
        # ⚠️ `verboso=False` HACIA ABAJO, SIEMPRE. No es para ahorrar ruido: es
        #    que la pantalla es un recurso compartido y tres workers hablando a
        #    la vez producen un texto que no dice la verdad de nadie. Lo que se
        #    ve al final es la línea de tiempo, que sí.
        try:
            return orquestador.ejecutar_un_bloque(bloque, contabilidad,
                                                  verboso=False)
        finally:
            # `finally`: si el bloque revienta, su barra igual se dibuja. Un
            # hueco en la línea de tiempo es un dato, no un adorno que falta.
            t1 = time.monotonic() - arranque
            etiqueta = str(getattr(bloque, "input", {}))
            with _CANDADO_TIEMPOS:
                tiempos.append((getattr(bloque, "id", "?"), etiqueta, t0, t1))

    # ⭐ `pool.map` DEVUELVE EN EL ORDEN EN QUE SE ENTREGARON, no en el que
    #    terminaron. Es la línea que evita el defecto más traicionero de este
    #    archivo: si el CAD termina primero, su resultado NO debe adelantarse al
    #    del USD. Los `tool_use_id` protegerían la correspondencia, pero el
    #    registro y el informe quedarían barajados, y nadie lo notaría hasta
    #    leer una tabla con las filas cambiadas de sitio.
    #    🔑 En paralelo, el orden de LLEGADA deja de ser el orden de SALIDA. Si
    #       tu código daba por hechas las dos cosas, ahora son dos cosas.
    with ThreadPoolExecutor(max_workers=min(MAX_EN_VUELO, len(bloques))) as pool:
        resultados = list(pool.map(trabajo, bloques))

    # 🐛 D-B2.1 — ANTES ESTO ERA UNA ASIGNACIÓN, Y MENTÍA POR OMISIÓN.
    #    `ULTIMA_LINEA_DE_TIEMPO = ...` se quedaba solo con la ÚLTIMA vuelta de
    #    reparto. En la corrida de la sesión 93 hubo UNA sola vuelta, así que no
    #    se notó nada: el dibujo era correcto por casualidad. Con dos vueltas, la
    #    línea de tiempo habría enseñado la mitad del trabajo SIN avisar de que
    #    faltaba la otra — y un dibujo incompleto se lee como uno completo.
    #    🔑 `LM.15` otra vez: no habría dado un dato falso, habría dado SILENCIO
    #       sobre lo que faltaba. Se arregla acumulando, y cada tramo se etiqueta
    #       con su vuelta para que dos vueltas se distingan de una.
    #    ⚠️ ARREGLADO Y NO VISTO MORDER (`LM.13`): en esta tarea el orquestador
    #       da una sola vuelta de herramientas. Hasta que una corrida real dé
    #       dos, esto es una nota, no un freno.
    with _CANDADO_TIEMPOS:
        vuelta = _CONTADOR_VUELTAS["n"] = _CONTADOR_VUELTAS["n"] + 1
        ULTIMA_LINEA_DE_TIEMPO.extend(
            (i, f"v{vuelta} {etiqueta}", t0, t1) for i, etiqueta, t0, t1 in
            sorted(tiempos, key=lambda t: t[2]))

    if verboso:
        print(f"\n  [reparto] {len(bloques)} bloques a la vez "
              f"(tope: {MAX_EN_VUELO}) · {time.monotonic() - arranque:.2f}s")

    return resultados


# ---------------------------------------------------------------------------
# 3) LA LÍNEA DE TIEMPO — donde el solapamiento SE VE
# ---------------------------------------------------------------------------

def dibujar_linea_de_tiempo(eventos, ancho=52):
    """Dibuja las barras. Sin esto, "corrieron a la vez" es una afirmación.

    🔑 Es la diferencia entre decir que algo se solapó y ENSEÑARLO. Un total más
       bajo es compatible con dos mundos —se solaparon, o hoy la API estuvo
       rápida— y solo las barras los separan. Es `D-B1.1` de la sesión 92 otra
       vez: un número que cabe en dos explicaciones no es una medida.
    """
    if not eventos:
        return "  (sin eventos)"

    fin = max(t1 for _, _, _, t1 in eventos)
    if fin <= 0:
        return "  (todo ocurrió en menos de un milisegundo)"

    lineas = []
    for _id, etiqueta, t0, t1 in eventos:
        ini = int(round(t0 / fin * ancho))
        largo = max(1, int(round((t1 - t0) / fin * ancho)))
        barra = " " * ini + "#" * min(largo, ancho - ini)
        lineas.append(f"  {etiqueta[:28]:<28} |{barra:<{ancho}}| "
                      f"{t0:5.2f} -> {t1:5.2f}s  ({t1 - t0:5.2f}s)")

    suma = sum(t1 - t0 for _, _, t0, t1 in eventos)
    maximo = max(t1 - t0 for _, _, t0, t1 in eventos)
    lineas.append(f"  {'':<28} +{'-' * ancho}+")
    lineas.append(f"  suma de los trozos: {suma:5.2f}s   "
                  f"el más lento: {maximo:5.2f}s   "
                  f"reloj de pared: {fin:5.2f}s")
    return "\n".join(lineas)


# ---------------------------------------------------------------------------
# 4) LA DEMO — la misma tarea de A.2, con UNA sola variable cambiada
# ---------------------------------------------------------------------------

TAREA_DEMO = orquestador.TAREA_DEMO


def corrida(modo, verboso=True):
    """Corre la tarea con un reparto u otro. TODO lo demás es idéntico."""
    reparto = (reparto_en_paralelo if modo == "paralelo"
               else orquestador.reparto_en_serie)

    print("\n" + "=" * 70)
    print(f"REPARTO: {modo.upper()}")
    print("=" * 70)

    reiniciar_linea_de_tiempo()
    t0 = time.monotonic()
    r = orquestador.correr_orquestador(TAREA_DEMO, verboso=verboso,
                                       reparto=reparto)
    r["reloj_pared"] = round(time.monotonic() - t0, 2)
    r["modo"] = modo
    r["linea_de_tiempo"] = (list(ULTIMA_LINEA_DE_TIEMPO)
                            if modo == "paralelo" else [])
    return r


def informe(r):
    print("\n" + "-" * 70)
    print(f"RESPUESTA FINAL ({r['modo']})")
    print("-" * 70)
    print(r["texto"])

    if r["linea_de_tiempo"]:
        print("\n  LÍNEA DE TIEMPO DE LOS WORKERS")
        print(dibujar_linea_de_tiempo(r["linea_de_tiempo"]))

    print(f"\n  arriba (orquestador): ${r['coste_orquestador_usd']:.6f}  "
          f"({r['llamadas_api_orquestador']} llamadas API)")
    print(f"  abajo  ({r['workers_usados']} workers):  ${r['coste_workers_usd']:.6f}  "
          f"({r['llamadas_api_workers']} llamadas API)")
    print(f"  TOTAL:                ${r['coste_total_usd']:.6f}   "
          f"en {r['reloj_pared']} s")
    print("  detalle: " + " · ".join(
        f"{d['worker']}={d['segundos']}s" for d in r["detalle_workers"]))


def comparar(a, b):
    """El único sitio donde se dice quién ganó, y con LAS DOS columnas."""
    print("\n" + "=" * 70)
    print("EL RESULTADO DE B.2 — dos columnas, y dicen cosas distintas")
    print("=" * 70)
    print(f"  {'':<12} {'TIEMPO':>12} {'COSTE':>14} {'LLAMADAS API':>14}")
    for r in (a, b):
        print(f"  {r['modo']:<12} {r['reloj_pared']:>11.2f}s "
              f"${r['coste_total_usd']:>12.6f} "
              f"{r['llamadas_api_orquestador'] + r['llamadas_api_workers']:>14}")

    dif_t = a["reloj_pared"] - b["reloj_pared"]
    dif_c = a["coste_total_usd"] - b["coste_total_usd"]
    print(f"\n  ⏱️  diferencia de TIEMPO: {dif_t:+.2f}s  "
          f"({dif_t / a['reloj_pared'] * 100:+.0f} %)")
    print(f"  💰 diferencia de COSTE:  ${dif_c:+.6f}")
    print("\n  🔑 Lee las dos columnas juntas. Si la de tiempo bajó mucho y la")
    print("     de coste no se movió, eso NO es que algo salió mal: es la")
    print("     definición del fan-out. Compra reloj, no compra factura.")
    print("  ⚠️ Y si la de coste SÍ se movió mucho, el experimento está sucio:")
    print("     el modelo dio otro número de vueltas y entonces no cambió UNA")
    print("     variable, cambiaron dos. Míralo ANTES de creerte el tiempo.")


# ---------------------------------------------------------------------------
# 5) LAS PRUEBAS — corren sin modelo, sin red y sin gastar un centavo
# ---------------------------------------------------------------------------
# El archivo que más enseñó de B.1 fue `verificador.py`, y costó $0,00. Estas
# pruebas son su equivalente aquí: miden con workers falsos que DUERMEN lo que
# de otro modo habría que pagar para ver.
#
# ⭐ Y la nº 3 es la joya: demuestra "en serie es la suma, en paralelo es el
#    máximo" con relojes de verdad y factura cero.

class _BloqueFalso:
    """Imita un bloque `tool_use` de la API: lo justo para pasar por el puente."""

    def __init__(self, nombre, entrada, ident):
        self.type = "tool_use"
        self.name = nombre
        self.input = entrada
        self.id = ident


def _es_json(linea):
    try:
        json.loads(linea)
        return True
    except Exception:
        return False


def _pruebas():
    import tempfile
    fallos = []

    def revisa(nombre, condicion, detalle=""):
        marca = "OK  " if condicion else "FALLA"
        print(f"  [{marca}] {nombre}"
              + (f"\n           -> {detalle}" if detalle and not condicion else ""))
        if not condicion:
            fallos.append(nombre)

    # ⚠️ EL REGISTRO SE DESVÍA A UN ARCHIVO TEMPORAL, Y ES DELIBERADO.
    #    Es la lección de la sesión 50 de TEAPP (`T-072`): el instrumento de
    #    medida escribía en los datos de verdad. Unas pruebas que ensucian el
    #    `.jsonl` real convierten el registro de las corridas PAGADAS en una
    #    mezcla de corridas pagadas e inventadas — y eso no se nota nunca.
    temporal = Path(tempfile.mkdtemp()) / "registro_de_pruebas.jsonl"
    registro_real = orquestador.REGISTRO
    funciones_reales = dict(orquestador.FUNCIONES_ORQ)
    orquestador.REGISTRO = temporal

    def contabilidad_limpia():
        return {"workers": 0, "coste_workers_usd": 0.0, "llamadas_api_workers": 0,
                "entrada_workers": 0, "salida_workers": 0, "detalle": []}

    try:
        # --- un "worker" falso: duerme lo que le digan y no gasta nada -------
        def worker_falso(monto, moneda, contabilidad, verboso=True):
            time.sleep(monto)          # `monto` = segundos, para la prueba
            with orquestador._CANDADO_CONTABILIDAD:
                contabilidad["workers"] += 1
                contabilidad["coste_workers_usd"] += 0.001
                contabilidad["llamadas_api_workers"] += 3
                contabilidad["detalle"].append({"worker": moneda, "ok": True,
                                                "vueltas": 1, "segundos": monto,
                                                "coste_usd": 0.001,
                                                "herramientas": []})
            return {"moneda": moneda, "pesos": 1}

        orquestador.FUNCIONES_ORQ["consultar_moneda"] = worker_falso

        # El primero es EL MÁS LENTO a propósito: si el orden se rompiera, se
        # rompería justo así.
        bloques = [
            _BloqueFalso("consultar_moneda", {"monto": 0.30, "moneda": "USD"}, "b1"),
            _BloqueFalso("consultar_moneda", {"monto": 0.10, "moneda": "EUR"}, "b2"),
            _BloqueFalso("consultar_moneda", {"monto": 0.05, "moneda": "CAD"}, "b3"),
        ]

        c = contabilidad_limpia()
        t0 = time.monotonic()
        res_par = reparto_en_paralelo(bloques, c, verboso=False)
        t_par = time.monotonic() - t0

        # 1 -----------------------------------------------------------------
        revisa("1. el orden se conserva aunque el PRIMERO sea el más lento",
               [r["tool_use_id"] for r in res_par] == ["b1", "b2", "b3"],
               str([r["tool_use_id"] for r in res_par]))

        # 2 -----------------------------------------------------------------
        revisa("2. sale un tool_result por cada tool_use, ni uno más",
               len(res_par) == 3 and all(r["type"] == "tool_result" for r in res_par))

        # 3 -----------------------------------------------------------------
        c2 = contabilidad_limpia()
        t0 = time.monotonic()
        orquestador.reparto_en_serie(bloques, c2, verboso=False)
        t_ser = time.monotonic() - t0

        suma, maximo = 0.45, 0.30
        revisa(f"3. EN SERIE ES LA SUMA ({t_ser:.2f}s ~ {suma}s) "
               f"Y EN PARALELO EL MÁXIMO ({t_par:.2f}s ~ {maximo}s)",
               t_ser >= suma * 0.95 and t_par < suma * 0.80,
               f"serie={t_ser:.2f} paralelo={t_par:.2f}")

        # 4 -----------------------------------------------------------------
        revisa("4. la contabilidad cuadra con hilos: 3 workers, $0,003, 9 llamadas",
               c["workers"] == 3 and abs(c["coste_workers_usd"] - 0.003) < 1e-9
               and c["llamadas_api_workers"] == 9,
               json.dumps({k: v for k, v in c.items() if k != "detalle"}))

        # 5 -----------------------------------------------------------------
        # ⚠️ ESTA PRUEBA DEMUESTRA EL MECANISMO; NO CAZA UNA CARRERA AL VUELO.
        #    Una carrera de verdad es intermitente, y una prueba intermitente es
        #    peor que ninguna (sesión 92, `D-B1.2`). Así que las tres operaciones
        #    que esconde `+=` —leer, sumar, escribir— se separan a mano. Lo que
        #    se prueba es que si NO son atómicas, una suma se pierde: por eso
        #    existe `_CANDADO_CONTABILIDAD`, y por eso su ausencia no da error.
        #    🔑 Y dice exactamente lo que es: mecanismo demostrado, no carrera
        #       observada. Nombrar un mecanismo no es haberlo medido.
        cuenta = {"n": 0}

        def sumar_sin_candado():
            visto = cuenta["n"]        # leer
            time.sleep(0.05)           # (lo que en la vida real dura un pelo)
            cuenta["n"] = visto + 1    # escribir sobre un valor ya viejo

        hilos = [threading.Thread(target=sumar_sin_candado) for _ in range(2)]
        for h in hilos:
            h.start()
        for h in hilos:
            h.join()
        revisa("5. sin candado, dos sumas se convierten en una "
               f"(2 pedidas -> {cuenta['n']} anotada)", cuenta["n"] == 1,
               "no se perdió: la demostración del mecanismo falló")

        # 6 -----------------------------------------------------------------
        def worker_que_revienta(monto, moneda, contabilidad, verboso=True):
            if moneda == "EUR":
                raise RuntimeError("me caí a propósito")
            return {"moneda": moneda, "pesos": 1}

        # ⚠️ AQUÍ ARRIBA VA A SALIR UN `traceback` EN ROJO, Y ESTÁ BIEN.
        #    Lo imprime `ejecutar_un_bloque` a propósito: un defecto NUESTRO se
        #    le enseña entero al programador aunque al modelo se le resuma. Que
        #    aparezca es la prueba de que el `except` hizo su trabajo, no de que
        #    algo se rompiera. 📌 Sale antes que las demás líneas porque el
        #    traceback va por `stderr`, que no espera turno.
        orquestador.FUNCIONES_ORQ["consultar_moneda"] = worker_que_revienta
        c3 = contabilidad_limpia()
        res3 = reparto_en_paralelo(bloques, c3, verboso=False)
        contenidos = [json.loads(r["content"]) for r in res3]
        revisa("6. un worker que revienta NO tumba a los otros dos, y su fallo "
               "llega como dato",
               len(res3) == 3 and "error" in contenidos[1]
               and "error" not in contenidos[0] and "error" not in contenidos[2],
               json.dumps(contenidos, ensure_ascii=False)[:140])

        # 8 (va antes de la 7 porque la 7 lee el archivo al final) -----------
        # 🐛 D-B2.1: dos vueltas de reparto tienen que SUMARSE, no pisarse.
        #    Antes esto era una asignación y la línea de tiempo enseñaba solo la
        #    última vuelta. En la corrida real hubo UNA vuelta, así que el dibujo
        #    salió bien por casualidad — y por eso el defecto necesitaba una
        #    prueba: lo que se arregla sin verlo morder es una nota (`LM.13`).
        orquestador.FUNCIONES_ORQ["consultar_moneda"] = worker_falso
        reiniciar_linea_de_tiempo()
        reparto_en_paralelo(bloques[:2], contabilidad_limpia(), verboso=False)
        reparto_en_paralelo(bloques[:2], contabilidad_limpia(), verboso=False)
        vueltas = {e[1].split()[0] for e in ULTIMA_LINEA_DE_TIEMPO}
        revisa("8. dos vueltas de reparto se ACUMULAN en la línea de tiempo, "
               f"no se pisan (4 barras, vueltas {sorted(vueltas)})",
               len(ULTIMA_LINEA_DE_TIEMPO) == 4 and vueltas == {"v1", "v2"},
               f"{len(ULTIMA_LINEA_DE_TIEMPO)} barras, vueltas {sorted(vueltas)}")

        # 7 -----------------------------------------------------------------
        # El registro se escribió desde tres hilos en las pruebas de arriba.
        # Sin el candado, aquí habría una línea partida.
        lineas = temporal.read_text(encoding="utf-8").splitlines()
        rotas = [n for n, l in enumerate(lineas, 1) if l.strip() and not _es_json(l)]
        revisa(f"7. el registro escrito desde hilos sigue siendo JSONL válido "
               f"({len(lineas)} líneas)", not rotas, f"líneas rotas: {rotas}")

    finally:
        orquestador.REGISTRO = registro_real
        orquestador.FUNCIONES_ORQ.clear()
        orquestador.FUNCIONES_ORQ.update(funciones_reales)

    print()
    if fallos:
        print(f"  {len(fallos)} de 8 fallaron: {', '.join(fallos)}")
        return 1
    print("  Las 8 en verde, sin modelo, sin red y sin gastar un centavo.")
    return 0


# ---------------------------------------------------------------------------
# 6) LA PUERTA
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="B.2 — fan-out / fan-in")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--test", action="store_true",
                   help="las 8 pruebas. Sin modelo, sin red, $0,00")
    g.add_argument("--serie", action="store_true", help="una corrida en serie")
    g.add_argument("--paralelo", action="store_true", help="una corrida en paralelo")
    g.add_argument("--ambos", action="store_true",
                   help="serie Y paralelo seguidas: la única medida limpia")
    args = p.parse_args()

    print("=" * 70)
    print("B.2 — FAN-OUT / FAN-IN")
    print("=" * 70)

    # ⭐ SIN ARGUMENTOS CORRE LAS PRUEBAS, NO LA DEMO. Es a propósito: lo que
    #    cuesta dinero se pide con todas las letras.
    if args.test or not any((args.serie, args.paralelo, args.ambos)):
        print("Pruebas del reparto — sin modelo, sin red, sin gastar.\n")
        sys.exit(_pruebas())

    if args.ambos:
        print("Dos corridas completas. Una sola variable cambia: el reparto.")
        a = corrida("serie")
        informe(a)
        b = corrida("paralelo")
        informe(b)
        comparar(a, b)
    else:
        informe(corrida("paralelo" if args.paralelo else "serie"))

    print(f"\nregistros: {orquestador.REGISTRO.name}  +  {worker.REGISTRO.name}")
