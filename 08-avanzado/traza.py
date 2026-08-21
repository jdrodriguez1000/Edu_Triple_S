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
# 3) EL PORTERO — ninguna prueba gratis puede escribir en el registro pagado
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
# 4) LAS PRUEBAS — $0,00
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
    if "--portero" in argv:
        sucios, _ = portero()
        return 1 if sucios else 0
    return _pruebas()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
