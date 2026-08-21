"""C.1 — LA TRAZA ANIDADA. Paso 1: ¿el dueño de una línea es un dato o un adjetivo?

    Apuesta 3, sellada en `README.md` antes de escribir esto:
    «La `capa` de hoy es una etiqueta decorativa: al torcerla no se rompe nada.»

Este archivo la pone a prueba y NO cuesta un centavo: trabaja sobre registros que
ya existen, escritos y pagados en las sesiones 92 a 96.

🔑 QUÉ SE TUERCE, Y POR QUÉ ASÍ.
   No se cambia ni un número. Se cambia SOLO el nombre del dueño: el gasto del
   worker `eur` pasa a figurar como del worker `usd`. El dinero total, las
   llamadas y los tokens quedan EXACTAMENTE iguales.
   → Es la mentira más pequeña que cabe en un registro: una que no toca la
     aritmética. Si el harness la detecta, `capa` es un dato. Si no, es un
     adjetivo.

📌 POR QUÉ ESTA MENTIRA Y NO OTRA. Es la que ya ocurrió sola. En la sesión 95 el
   instrumento torcía `nombre=`, que resultó ser solo una etiqueta del registro:
   el experimento salió VERDE y no midió nada. Aquí se repite a propósito, en el
   campo de al lado, para ver si el defecto sigue vivo.

⚠️ EL SOSPECHOSO DE ESTAR CIEGO, nombrado en el sobre antes de escribir esto: lo
   escrito hoy soy yo. Por eso este archivo NO inventa un auditor nuevo — usa
   `auditar()` de `profundidad.py`, que es de otra sesión y ya trae sus pruebas.
"""

import contextlib
import io
import json
import sys
from pathlib import Path

import profundidad

AQUI = Path(__file__).resolve().parent
MODELO = profundidad.MODELO

# Los registros reales, ya pagados. Este archivo NO escribe en ellos jamás:
# trabaja siempre sobre copias.
REGISTROS = [
    AQUI / f"registro_orquestador_{MODELO}.jsonl",
    AQUI / f"registro_workers_{MODELO}.jsonl",
]


# ---------------------------------------------------------------------------
# 1) LA MENTIRA MÍNIMA
# ---------------------------------------------------------------------------

def dueno(d):
    """Quién hizo esta línea, según el registro. Es la definición que usa el
    auditor de `profundidad.py`, copiada aquí para que se vea entera:

        capa (la de arriba)  o  worker (la de abajo)  o  "?"

    🔑 Fíjate en lo que NO hay: ningún campo dice de QUIÉN es hija. Con dos
       nombres sueltos se hace una lista; no se hace un árbol.
    """
    return d.get("capa") or d.get("worker") or "?"


def torcer_dueno(lineas, de, a):
    """Devuelve las líneas con el dueño `de` renombrado a `a`. Nada más.

    No cambia costos, ni tokens, ni horas, ni el orden. Solo el nombre.
    """
    salida, torcidas = [], 0
    for d in lineas:
        d = dict(d)                      # copia: el original no se muta
        if d.get("capa") == de:
            d["capa"], torcidas = a, torcidas + 1
        elif d.get("worker") == de:
            d["worker"], torcidas = a, torcidas + 1
        salida.append(d)
    return salida, torcidas


def leer(rutas):
    """Lee los registros a memoria. Los archivos no se tocan."""
    return {r: [json.loads(l) for l in open(r, encoding="utf-8") if l.strip()]
            for r in rutas}


def escribir_copia(contenido, sufijo):
    """Vuelca las líneas a copias temporales y devuelve las rutas nuevas."""
    rutas = []
    for original, lineas in contenido.items():
        copia = AQUI / f"_{sufijo}_{original.name}"
        copia.write_text(
            "\n".join(json.dumps(d, ensure_ascii=False) for d in lineas) + "\n",
            encoding="utf-8")
        rutas.append(copia)
    return rutas


def _auditar_copia(contenido, sufijo):
    """Audita un contenido volcado a disco, y borra las copias pase lo que pase."""
    rutas = escribir_copia(contenido, sufijo)
    try:
        return profundidad.auditar({r: 0 for r in rutas}, rutas=rutas)
    finally:
        for r in rutas:
            r.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# 2) EL EXPERIMENTO
# ---------------------------------------------------------------------------

def experimento(de="eur", a="usd", verboso=True):
    """Audita el registro real, y luego el mismo registro con el dueño torcido."""
    contenido = leer(REGISTROS)
    total_lineas = sum(len(v) for v in contenido.values())

    torcido, torcidas = {}, 0
    for ruta, lineas in contenido.items():
        torcido[ruta], n = torcer_dueno(lineas, de, a)
        torcidas += n

    limpio = _auditar_copia(contenido, "sano")
    sucio = _auditar_copia(torcido, "torcido")

    if verboso:
        _informe(de, a, total_lineas, torcidas, limpio, sucio)
    return limpio, sucio, torcidas


def _informe(de, a, total_lineas, torcidas, limpio, sucio):
    print("\n" + "=" * 72)
    print(f"  C.1 · PASO 1 — se renombró el dueño «{de}» a «{a}»")
    print("=" * 72)
    print(f"  Líneas del registro real ....... {total_lineas}")
    print(f"  Líneas cuyo dueño se torció .... {torcidas}")

    print("\n  LO QUE EL AUDITOR VE, ANTES Y DESPUÉS DE LA MENTIRA")
    print(f"  {'':22} {'sano':>14}  {'torcido':>14}   ¿lo notó?")
    for etiqueta, clave in (("total en dólares", "total_usd"),
                            ("llamadas a la API", "llamadas")):
        v1, v2 = limpio[clave], sucio[clave]
        print(f"  {etiqueta:22} {v1:>14}  {v2:>14}   "
              f"{'🚨 NO' if v1 == v2 else 'sí'}")

    print("\n  El reparto por dueño, que es lo único que sí cambia:")
    for k in sorted(set(limpio["por_capa"]) | set(sucio["por_capa"])):
        v1 = limpio["por_capa"].get(k, 0.0)
        v2 = sucio["por_capa"].get(k, 0.0)
        nota = ""
        if v2 > v1:
            nota = "  ←── se quedó con el gasto ajeno"
        elif v1 and not v2:
            nota = "  ←── desapareció del informe"
        print(f"    {k:26} {v1:>10.6f}  →  {v2:>10.6f}{nota}")
    print("=" * 72)


# ---------------------------------------------------------------------------
# 3) EL ÁRBOL — C.1 · PASO 2
# ---------------------------------------------------------------------------

def arbol(lineas, verboso=True):
    """Reconstruye el árbol de una corrida a partir de `id` y `padre`.

    ⚠️ Y AQUÍ HAY QUE DECIR ALGO INCÓMODO, PORQUE CAMBIA EL PLAN DEL PASO 4.
       Los registros de las sesiones 92 a 96 **no se pueden convertir en árbol**.
       No es que sea caro: es imposible. `id` y `padre` no están ahí y no hay de
       dónde sacarlos — unir por el reloj falla justo en el paralelo (medido en
       la 97: un segundo con tres arranques).

    🔑 **La traza es la única pieza del harness que no se puede añadir hacia
       atrás.** Un test se puede escribir después. Un presupuesto se puede poner
       después. Un árbol, no: o la línea nació sabiendo de quién era hija, o esa
       línea ya nunca lo va a saber. **Lo que no se instrumentó, no ocurrió.**
    """
    if not lineas:
        return {}

    gasto = {}
    hijos, raices, nombre = {}, [], {}
    for d in lineas:
        tid = d.get("id")
        if tid is None:
            continue
        nombre.setdefault(tid, d.get("tramo", "?"))
        gasto[tid] = round(gasto.get(tid, 0.0) + d.get("costo_usd", 0.0), 6)
        padre = d.get("padre")
        if padre is None:
            if tid not in raices:
                raices.append(tid)
        else:
            hijos.setdefault(padre, [])
            if tid not in hijos[padre]:
                hijos[padre].append(tid)

    def total(tid):
        """El gasto de un tramo Y de todo lo que cuelga de él."""
        return round(gasto.get(tid, 0.0) + sum(total(h) for h in hijos.get(tid, [])), 6)

    if verboso:
        print("\n" + "=" * 72)
        print("  EL ÁRBOL DE LA CORRIDA — reconstruido de `id` y `padre`")
        print("=" * 72)

        def dibujar(tid, sangria=""):
            propio = gasto.get(tid, 0.0)
            print(f"  {sangria}{nombre[tid]:28} {tid:5} "
                  f"total ${total(tid):.6f}   propio ${propio:.6f}")
            for h in hijos.get(tid, []):
                dibujar(h, sangria + "   ")

        for r in raices:
            dibujar(r)
        print("=" * 72)

    return {"raices": raices, "hijos": hijos, "total": {t: total(t) for t in raices}}


def demo(verboso=True):
    """Una corrida de dos capas SIN modelo y SIN red, para ver el árbol. $0,00.

    📌 Los workers son falsos a propósito: lo que se está probando es el
       parentesco, no el modelo. Y el camino que recorren es el DE VERDAD —
       `reparto_en_paralelo`, `ejecutar_un_bloque`, los dos `anotar`— porque un
       árbol dibujado por un camino de mentira mediría al camino de mentira.
    """
    import contexto
    import fan_out
    import orquestador
    import worker

    with orquestador.registro_desviado():
        def worker_falso(monto, moneda, contabilidad, verboso=True):
            with contexto.tramo(f"worker:{moneda.lower()}"):
                worker.anotar("llamada_api", worker=moneda.lower(), costo_usd=0.002183)
                worker.anotar("herramienta", worker=moneda.lower(), nombre="tasa")
                worker.anotar("llamada_api", worker=moneda.lower(), costo_usd=0.002624)
            return {"ok": True, "pesos": monto * 3099}

        class _Bloque:
            def __init__(self, m):
                self.name = "consultar_moneda"
                self.input = {"monto": 1000, "moneda": m}
                self.id = "b" + m

        conta = {"capa": "capa1"}
        with contexto.tramo("capa:orquestador"):
            orquestador.anotar("llamada_api", capa="orquestador", costo_usd=0.001989)
            fan_out.reparto_en_paralelo(
                [_Bloque("USD"), _Bloque("EUR"), _Bloque("CAD")], conta,
                verboso=False, funciones={"consultar_moneda": worker_falso})

        lineas = []
        for r in (orquestador.REGISTRO, worker.REGISTRO):
            if Path(r).exists():
                lineas += [json.loads(l) for l in open(r, encoding="utf-8") if l.strip()]

    return arbol(lineas, verboso=verboso), lineas


# ---------------------------------------------------------------------------
# 4) EL PORTERO — ninguna prueba gratis puede escribir en el registro pagado
# ---------------------------------------------------------------------------

def portero(verboso=True):
    """Corre las pruebas gratis de TODO el nivel y exige que los registros
    reales no crezcan ni una línea.

    🚨 POR QUÉ EXISTE. En la sesión 97 se descubrió que la prueba 2 de
       `profundidad.py` escribía en `registro_orquestador_*.jsonl`, el archivo
       de las corridas PAGADAS. Cuatro líneas inventadas ya estaban dentro, y
       **una de ellas commiteada**. Nadie lo notó en dos sesiones.

    🔑 Y ESTE ES EL ARREGLO DE VERDAD, NO EL `with` DE ALLÁ.
       Desviar el registro en `profundidad.py` arregla UN archivo. El portero
       arregla la CLASE: cualquier prueba de cualquier módulo —incluidos los que
       todavía no existen— que escriba en el registro real, pone esto rojo.
       Es la lección de la sesión 49 de TEAPP: el arreglo va en el origen, y
       encima se le pone un portero sobre los datos enteros.

    📌 Y se corre a ciegas a propósito: no le importa QUÉ prueba ensució, solo
       que alguien lo hizo. Un portero que necesita saber a quién vigilar solo
       caza a los que ya sospechabas.
    """
    import importlib

    # La convención del nivel: cada módulo con pruebas gratis expone `_pruebas`.
    nombres = ["fan_out", "profundidad", "router", "supervisor", "verificador"]
    antes = {r: r.stat().st_size for r in REGISTROS}
    lineas_antes = {r: sum(1 for _ in open(r, encoding="utf-8")) for r in REGISTROS}

    corridos, sin_pruebas = [], []
    for nombre in nombres:
        mod = importlib.import_module(nombre)
        fn = getattr(mod, "_pruebas", None)
        if fn is None:
            sin_pruebas.append(nombre)
            continue
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            fn()
        corridos.append(nombre)

    sucios = []
    for r in REGISTROS:
        ahora = sum(1 for _ in open(r, encoding="utf-8"))
        if ahora != lineas_antes[r]:
            sucios.append((r.name, lineas_antes[r], ahora))

    if verboso:
        print("\n" + "=" * 72)
        print("  EL PORTERO — ¿alguna prueba gratis escribió en el registro pagado?")
        print("=" * 72)
        print(f"  Módulos con pruebas corridos ... {', '.join(corridos)}")
        if sin_pruebas:
            print(f"  Sin `_pruebas` (no vigilados) .. {', '.join(sin_pruebas)}")
        for r in REGISTROS:
            print(f"  {r.name:44} {lineas_antes[r]} líneas")
        if sucios:
            for nombre, a, b in sucios:
                print(f"  🚨 {nombre}: {a} → {b} líneas. UNA PRUEBA ESCRIBIÓ AQUÍ.")
        else:
            print("  ✅ ninguno creció. El registro pagado sigue siendo solo pagado.")
        print("=" * 72)

    return sucios, corridos


# ---------------------------------------------------------------------------
# 5) LAS PRUEBAS — $0,00
# ---------------------------------------------------------------------------

def _pruebas():
    fallos = []

    def check(nombre, cond, detalle=""):
        print(f"  {'✅' if cond else '❌'}  {nombre}")
        if not cond:
            if detalle:
                print(f"      → {detalle}")
            fallos.append(nombre.split(".")[0])

    print("\n  PRUEBAS — $0.00\n")

    # 1) 🚨 EL INSTRUMENTO TIENE QUE MORDER ANTES DE CREERLE NADA (`LM.13`). Si
    #    no torciera ninguna línea, el experimento saldría verde sin medir — que
    #    es exactamente lo que pasó en la sesión 95.
    lineas = [{"evento": "llamada_api", "worker": "eur", "costo_usd": 0.01},
              {"evento": "llamada_api", "worker": "usd", "costo_usd": 0.02}]
    fuera, n = torcer_dueno(lineas, "eur", "usd")
    check("1. el instrumento tuerce de verdad: la línea cambia de dueño",
          n == 1 and fuera[0]["worker"] == "usd", f"torcidas={n}, {fuera}")

    # 2) Y NO toca ningún número. Si tocara el costo, el auditor lo cazaría por
    #    la aritmética y no habríamos medido si `capa` es un dato.
    check("2. y no cambia ni un número: la mentira es SOLO el nombre",
          [d["costo_usd"] for d in fuera] == [0.01, 0.02], fuera)

    # 3) El original no se mutó. Sin esto, auditar el «sano» después del
    #    «torcido» daría el torcido y la comparación sería falsa.
    check("3. el original queda intacto (se copia, no se muta)",
          lineas[0]["worker"] == "eur", lineas)

    # 4) `dueno()` dice lo mismo que el auditor de `profundidad.py`. Si se
    #    separaran, este archivo mediría su propia definición y no la de allá.
    check("4. `dueno` coincide con la definición del auditor",
          dueno({"capa": "capa1"}) == "capa1"
          and dueno({"worker": "usd"}) == "usd"
          and dueno({}) == "?")

    # 5) Los registros reales existen. Sin ellos el experimento no mide nada, y
    #    saldría verde igual.
    check("5. los dos registros reales existen y tienen líneas",
          all(r.exists() and r.stat().st_size > 0 for r in REGISTROS),
          [str(r) for r in REGISTROS])

    # 6) No quedó ninguna copia temporal tirada. Es la sesión 50 de TEAPP: lo
    #    que mató una medición fue una báscula que se quedó encendida.
    check("6. el experimento no deja copias tiradas en la carpeta",
          not list(AQUI.glob("_sano_*")) and not list(AQUI.glob("_torcido_*")),
          [p.name for p in AQUI.glob("_*_registro_*")])

    # 7) 🚨 EL PORTERO SE VE MORDER. Sin esto es una nota, no un portero
    #    (`LM.13`) — y el nivel 8 ya lleva seis sesiones donde lo ciego era lo
    #    escrito ese mismo día.
    #    Se le quita el arreglo a `profundidad.py` (se anula el desviador) y se
    #    exige que el portero se ponga ROJO. Todo sobre COPIAS de los registros:
    #    el experimento que comprueba que nadie ensucia los datos de verdad
    #    sería un chiste si ensuciara los datos de verdad.
    import shutil
    import tempfile
    import orquestador
    import worker

    carpeta = Path(tempfile.mkdtemp())
    copias = []
    for r in REGISTROS:
        destino = carpeta / r.name
        shutil.copy(r, destino)
        copias.append(destino)

    @contextlib.contextmanager
    def _desviador_anulado(modulos=None):
        yield carpeta                    # no desvía nada: es el bicho de vuelta

    g = globals()
    guardado = (g["REGISTROS"], orquestador.REGISTRO, worker.REGISTRO,
                orquestador.registro_desviado)
    try:
        g["REGISTROS"] = copias
        orquestador.REGISTRO, worker.REGISTRO = copias[0], copias[1]
        orquestador.registro_desviado = _desviador_anulado
        sucios, corridos = portero(verboso=False)
        check("7. 🚨 el portero MUERDE: sin el desvío, se pone rojo",
              bool(sucios), f"corridos={corridos}, sucios={sucios}")
    finally:
        (g["REGISTROS"], orquestador.REGISTRO, worker.REGISTRO,
         orquestador.registro_desviado) = guardado
        shutil.rmtree(carpeta, ignore_errors=True)

    # 8) Y con el arreglo puesto, el mismo portero está verde sobre los reales.
    sucios, corridos = portero(verboso=False)
    check("8. y con el desvío puesto, el registro real no crece ni una línea",
          not sucios and len(corridos) == 5, f"corridos={corridos}, sucios={sucios}")

    # --- C.1 · PASO 2: el parentesco ---------------------------------------
    import contexto

    # 8b) Sin tramo abierto, `marca()` devuelve vacío. Es deliberado: una línea
    #     huérfana debe VERSE huérfana, no colgar de una raíz inventada que
    #     parecería correcta.
    check("9. sin tramo abierto, la marca va vacía (huérfana visible)",
          contexto.marca() == {}, contexto.marca())

    # 10) El parentesco se DEDUCE, no se pasa. En todo el nivel no hay una sola
    #     llamada que reciba un `padre=`: es el sospechoso que el sobre nombró.
    with contexto.tramo("a") as a:
        m1 = contexto.marca()
        with contexto.tramo("b"):
            m2 = contexto.marca()
    check("10. un tramo hijo hereda la corrida y apunta a su padre",
          m2["padre"] == m1["id"] and m2["corrida"] == m1["corrida"]
          and m2["profundidad"] == m1["profundidad"] + 1, f"{m1} / {m2}")
    check("11. y al salir, el contexto queda apagado",
          contexto.actual() is None, contexto.actual())

    # 12) 🚨 LA PRUEBA DEL PARALELO, Y ES LA QUE JUSTIFICA `atado()`.
    #     Un hilo nuevo NO hereda el contexto. Sin `atado` los tres workers
    #     anotarían con `padre: null` y el árbol saldría PLANO y con pinta de
    #     correcto — el mismo sitio donde unir por el reloj fallaba.
    from concurrent.futures import ThreadPoolExecutor

    def _marca_en_hilo():
        with contexto.tramo("hijo"):
            return contexto.marca()

    with contexto.tramo("padre") as p:
        with ThreadPoolExecutor(max_workers=3) as pool:
            sin_atar = list(pool.map(lambda _: _marca_en_hilo(), range(3)))
            atadas = [contexto.atado(_marca_en_hilo) for _ in range(3)]
        with ThreadPoolExecutor(max_workers=3) as pool:
            con_atar = list(pool.map(lambda f: f(), atadas))
        id_padre = p["id"]

    check("12. 🚨 SIN `atado`, el hilo pierde el padre (el bicho, visto morder)",
          all(m["padre"] is None and m["profundidad"] == 0 for m in sin_atar),
          sin_atar)
    check("13. CON `atado`, los tres hilos cuelgan del padre correcto",
          all(m["padre"] == id_padre and m["profundidad"] == 1 for m in con_atar),
          f"padre={id_padre} / {con_atar}")
    check("14. y los tres hermanos tienen ids DISTINTOS",
          len({m["id"] for m in con_atar}) == 3, con_atar)

    # 15) La corrida sobrevive al salto de hilo. Es el campo que cierra por
    #     diseño el bicho de la sesión 97: sin él, una línea de prueba y una
    #     pagada viven en el mismo archivo sin nada que las separe.
    check("15. la corrida es la MISMA en los tres hilos atados",
          len({m["corrida"] for m in con_atar}) == 1, con_atar)

    # 16) El decorador lee el nombre de la FIRMA, con sus valores por defecto.
    #     Si lo escribiera dos veces, sería el bicho de la sesión 33.
    @contexto.envuelto("nombre", prefijo="x:")
    def _fn(nombre="porDefecto"):
        return contexto.marca()["tramo"]
    check("16. el decorador saca el nombre del tramo de la firma real",
          _fn() == "x:porDefecto" and _fn(nombre="otro") == "x:otro", _fn())

    # 17) 🔒 Y `functools.wraps` no es cosmética: sin él, la prueba 1 de
    #     `profundidad.py` —la que vigila que A.2 siga siendo A.2— se pondría
    #     roja por un motivo que no tiene nada que ver con lo que vigila.
    import inspect
    import orquestador
    firma = inspect.signature(orquestador.correr_orquestador).parameters
    check("17. envolver NO alteró la firma que vigila la prueba 1 de A.2",
          all(firma[p].default is None for p in ("sistema", "tools", "funciones")),
          [firma[p].default for p in ("sistema", "tools", "funciones")])

    # 18) 🚨 EL ÁRBOL CONTRA UNO CUYO TOTAL SE SABE. Es la prueba 3 de
    #     `profundidad.py` aplicada al instrumento de hoy: `arbol()` es lo
    #     escrito esta sesión, o sea el sospechoso de estar ciego. Si sumara mal,
    #     inventaría un reparto que nadie contradice.
    falsas = [
        {"id": "t1", "padre": None, "tramo": "raiz", "costo_usd": 1.0},
        {"id": "t2", "padre": "t1", "tramo": "hijo-a", "costo_usd": 0.0},
        {"id": "t3", "padre": "t2", "tramo": "nieto", "costo_usd": 2.0},
        {"id": "t4", "padre": "t1", "tramo": "hijo-b", "costo_usd": 4.0},
        {"evento": "sin marca"},                       # línea vieja, sin traza
    ]
    a = arbol(falsas, verboso=False)
    check("18. el árbol suma hacia arriba: el padre incluye a sus nietos",
          a["raices"] == ["t1"] and a["total"]["t1"] == 7.0, a)
    check("19. y una línea SIN marca no inventa una raíz nueva",
          len(a["raices"]) == 1, a["raices"])

    # 20) ⚠️ LO QUE EL ÁRBOL NO PUEDE HACER, Y SE PRUEBA PARA QUE NO SE OLVIDE:
    #     los registros pagados de las sesiones 92-96 NO tienen `id` ni `padre`,
    #     y por eso NO se pueden convertir en árbol. No es caro: es imposible.
    #     🔑 La traza es la única pieza del harness que no se puede añadir hacia
    #        atrás. Lo que no se instrumentó, no ocurrió.
    viejas = [d for v in leer(REGISTROS).values() for d in v]
    check("20. ⚠️ las corridas ya pagadas NO tienen parentesco y nunca lo tendrán",
          not any("padre" in d for d in viejas),
          f"{sum('padre' in d for d in viejas)} líneas viejas con padre")

    print()
    if fallos:
        print(f"  ❌ {len(fallos)} prueba(s) en rojo: {', '.join(fallos)}")
        return 1
    print("  ✅ todas en verde, y no costaron nada.")
    return 0


def main(argv):
    if "--experimento" in argv:
        experimento()
        return 0
    if "--demo" in argv:
        demo()
        return 0
    if "--portero" in argv:
        sucios, _ = portero()
        return 1 if sucios else 0
    return _pruebas()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
