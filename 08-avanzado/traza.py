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
# 4) C.1 · PASO 3 — EL REGISTRO GRABADO, Y EL QUE TIENE QUE GRITAR
# ---------------------------------------------------------------------------

# La corrida de la demo, volcada a disco. NO es un registro pagado: no entra en
# `REGISTROS` y el portero no lo vigila. Cuesta $0,00 y se puede rehacer.
REGISTRO_DEMO = AQUI / "registro_demo_c1.jsonl"


def grabar_demo(ruta=None, verboso=True):
    """Corre la demo y **graba** su corrida en un archivo. Devuelve las líneas.

    🔑 POR QUÉ HACE FALTA ESTO, Y NO ES UN RODEO.
       El paso 3 tiene que torcer el `padre` de un registro **grabado** — así fue
       como el paso 1 mató a `capa`—. Pero no existe ninguno: los registros
       pagados de las sesiones 92 a 96 no tienen `id` ni `padre`, y no hay de
       dónde sacarlos (prueba 20). **Así que hay que fabricarlo.**

    📌 Y al fabricarlo se estrena la forma del PASO 4: «reconstruir una corrida
       ya grabada» solo puede significar **una corrida nueva**. Aquí está la
       primera.

    ⚠️ Este archivo NO es un registro pagado y no debe confundirse con uno. Por
       eso vive con otro nombre, fuera de `REGISTROS`, y el portero no lo mira:
       el portero vigila que nadie escriba en los de verdad, y este se escribe a
       propósito cada vez.
    """
    ruta = Path(ruta) if ruta else REGISTRO_DEMO
    _, lineas = demo(verboso=False)
    ruta.write_text(
        "\n".join(json.dumps(d, ensure_ascii=False) for d in lineas) + "\n",
        encoding="utf-8")
    if verboso:
        con_padre = sum(1 for d in lineas if d.get("id"))
        print(f"  grabado: {ruta.name} — {len(lineas)} líneas, "
              f"{con_padre} con parentesco")
    return lineas


def auditar_arbol(lineas):
    """El que tiene que gritar. Devuelve la lista de quejas; vacía = árbol sano.

    🚨 ESTE ES EL LECTOR QUE `capa` NUNCA TUVO, Y AHÍ ESTÁ TODO EL PASO 3.
       El paso 1 midió que `capa` era un adjetivo, y el motivo exacto era que su
       único lector —`auditar()`— la usaba para **imprimir** un reparto, no para
       **comprobarlo**. `arbol()` hace hoy lo mismo con `padre`: lo lee para
       dibujar. Un campo que solo se dibuja no puede estar mal nunca.

    🔑 LAS CUATRO QUEJAS, Y QUIÉN LAS CAZA. No es un detalle de implementación:
       es la mitad de lo que se apostó esta mañana.

         `padre_inexistente`  ← lo caza `padre` SOLO (apunta a algo que no está)
         `ciclo`              ← lo caza `padre` SOLO (se muerde la cola)
         `profundidad`        ← solo lo caza **`profundidad`**
         `corrida`            ← solo lo caza **`corrida`**

       Las dos primeras son integridad del propio campo. Las dos últimas **no se
       podrían escribir con `padre` a secas**: hacen falta DOS campos, escritos
       en el mismo instante, que puedan contradecirse. El apuntador dice «mi
       padre es t5»; el contador dice «yo estoy en el escalón 2». Si t5 está en
       el escalón 7, uno de los dos miente — y no hace falta saber cuál para
       saber que algo se rompió.

    ⭐ Y de ahí sale por qué `capa` no podía estar mal nunca: **estaba sola en su
       renglón.** Un dato que nadie puede contradecir no es que sea correcto: es
       que **no es comprobable**, que es otra cosa y peor, porque se le parece.

    ⚠️ LO QUE ESTE AUDITOR **NO** COMPRUEBA, DICHO AQUÍ Y NO ESCONDIDO:
       que dos líneas con el mismo `id` declaren el mismo padre. Es integridad
       de verdad y falta. Se deja fuera **a propósito**: ninguna de las cinco
       torceduras del sobre la ejercita, y un detector que nunca se ve morder es
       una nota, no un detector (`LM.13`). Queda apuntado para el paso 4.
    """
    # Un nodo por `id`. Las líneas viejas sin marca se ignoran: no son un error
    # del árbol, son de antes de que el árbol existiera (prueba 19).
    nodos = {}
    for d in lineas:
        tid = d.get("id")
        if tid is None:
            continue
        nodos.setdefault(tid, {
            "padre": d.get("padre"),
            "profundidad": d.get("profundidad"),
            "corrida": d.get("corrida"),
            "tramo": d.get("tramo", "?"),
        })

    quejas = []

    def quejarse(tipo, tid, detalle):
        quejas.append({"tipo": tipo, "id": tid, "detalle": detalle})

    for tid, n in nodos.items():
        padre = n["padre"]

        # 1) El padre tiene que existir. Una raíz (padre None) es legítima.
        if padre is not None and padre not in nodos:
            quejarse("padre_inexistente", tid,
                     f"apunta a «{padre}», que no está en el registro")
            continue

        # 2) Y la raíz tiene que estar en el escalón 0. Si no, es que alguien le
        #    quitó el padre a una línea que sí lo tenía.
        if padre is None:
            if n["profundidad"] not in (0, None):
                quejarse("profundidad", tid,
                         f"no tiene padre pero dice estar en el escalón "
                         f"{n['profundidad']}")
            continue

        p = nodos[padre]

        # 3) El contador contra el apuntador. Aquí es donde `profundidad` deja
        #    de ser decoración del dibujo y se vuelve testigo.
        if (None not in (n["profundidad"], p["profundidad"])
                and n["profundidad"] != p["profundidad"] + 1):
            quejarse("profundidad", tid,
                     f"dice escalón {n['profundidad']}, pero su padre «{padre}» "
                     f"está en el {p['profundidad']}")

        # 4) Padre e hijo tienen que ser de la misma corrida. Sin este campo, una
        #    línea de prueba podría colgar de una línea pagada y el árbol saldría
        #    creíble — que es el bicho de esta misma sesión, un escalón más
        #    arriba.
        if None not in (n["corrida"], p["corrida"]) and n["corrida"] != p["corrida"]:
            quejarse("corrida", tid,
                     f"es de la corrida «{n['corrida']}» y su padre «{padre}» "
                     f"de la «{p['corrida']}»")

    # 5) Ciclos. Se busca subiendo desde cada nodo: si se vuelve a pisar un id ya
    #    pisado en ESTE camino, la rama se muerde la cola. Sin esto, `arbol()`
    #    entraría en recursión infinita y el síntoma sería un `RecursionError`,
    #    que no dice nada de lo que pasó.
    for tid in nodos:
        visto, actual_id = [], tid
        while actual_id is not None and actual_id in nodos:
            if actual_id in visto:
                quejarse("ciclo", tid, " → ".join(visto + [actual_id]))
                break
            visto.append(actual_id)
            actual_id = nodos[actual_id]["padre"]

    return quejas


def informe_arbol(quejas, titulo="", verboso=True):
    """Imprime lo que el auditor encontró. Devuelve True si el árbol está sano."""
    if verboso:
        if titulo:
            print(f"\n  {titulo}")
        if not quejas:
            print("    ✅ árbol sano: ninguna queja")
        for q in quejas:
            print(f"    🚨 [{q['tipo']}] {q['id']}: {q['detalle']}")
    return not quejas


# ---------------------------------------------------------------------------
# 5) LAS CINCO MENTIRAS — C.1 · PASO 3
# ---------------------------------------------------------------------------
#
# 🚨 EL SOSPECHOSO DE ESTAR CIEGO, NOMBRADO EN EL SOBRE ANTES DE ESCRIBIR ESTO:
#
#        «el que elige las cinco torceduras es el mismo que sabe cuáles su
#         auditor puede cazar»
#
#    Cuatro de cinco cazadas sería un resultado sospechosamente cómodo si yo
#    elegí las cinco. Dos defensas, y las dos están en el código, no en la
#    intención:
#
#    1. `auditar_arbol` se escribió y se congeló ANTES que este apartado.
#    2. 🔑 **Cada mentira se escribe en su versión más astuta**: se le repara
#       todo lo demás que podría delatarla. Una mentira que se deja pillar por
#       un descuido no mide al detector, mide al descuido.
#
#    Y la mentira 5 entra en la lista **con su rojo esperado en blanco**: su
#    prueba exige que el auditor la DEJE PASAR. Una prueba que exige que el
#    instrumento falle es la única que no se puede escribir a su medida.

def _ids_por_tramo(lineas, nombre):
    """Los ids cuyo tramo empieza por `nombre`, en el orden en que aparecen."""
    vistos = []
    for d in lineas:
        if d.get("id") and str(d.get("tramo", "")).startswith(nombre):
            if d["id"] not in vistos:
                vistos.append(d["id"])
    return vistos


def _cambiar(lineas, tid, **campos):
    """Copia las líneas con los campos de `tid` cambiados. No muta el original."""
    salida, n = [], 0
    for d in lineas:
        d = dict(d)
        if d.get("id") == tid:
            d.update(campos)
            n += 1
        salida.append(d)
    return salida, n


def m1_padre_fantasma(lineas):
    """El `padre` apunta a un `id` que no existe en el registro.

    Es la mentira de un worker cuya línea de arriba se perdió: el gasto sigue
    ahí, con dueño, y el dueño no está en ninguna parte.
    """
    victima = _ids_por_tramo(lineas, "worker:eur")[0]
    fuera, n = _cambiar(lineas, victima, padre="t999")
    return fuera, f"{victima} pasa a colgar de «t999», que no existe ({n} líneas)"


def m2_ciclo(lineas):
    """La raíz acaba colgando de su propio nieto: la rama se muerde la cola.

    📌 Esta es la única de las cinco que NO se puede escribir en versión astuta,
       y el motivo es aritmético, no un descuido mío: **en un ciclo no hay
       escalones que cuadren.** Alguien tendría que estar un peldaño por debajo
       de alguien que está por debajo de él. Se anota porque es un hallazgo:
       **hay mentiras que un segundo testigo delata SIEMPRE.**
    """
    raiz = _ids_por_tramo(lineas, "capa:")[0]
    nieto = _ids_por_tramo(lineas, "worker:cad")[0]
    fuera, n = _cambiar(lineas, raiz, padre=nieto)
    return fuera, f"la raíz {raiz} pasa a colgar de su nieto {nieto} ({n} líneas)"


def m3_profundidad_vieja(lineas):
    """Se cambia el `padre` a uno que SÍ existe y se deja la `profundidad` vieja.

    Versión astuta: el padre nuevo es real, es de la misma corrida y no hace
    ciclo. Lo único que no cuadra es el escalón — o sea, **solo la caza el
    segundo testigo.** Con `padre` a secas esta mentira sería invisible.
    """
    victima = _ids_por_tramo(lineas, "worker:eur")[0]
    raiz = _ids_por_tramo(lineas, "capa:")[0]
    fuera, n = _cambiar(lineas, victima, padre=raiz)   # y NO se toca profundidad
    return fuera, (f"{victima} sube a colgar de la raíz {raiz} pero sigue "
                   f"diciendo que está en el escalón 2 ({n} líneas)")


def m4_otra_corrida(lineas_a, lineas_b):
    """Una línea de una corrida cuelga de una línea de OTRA corrida.

    Versión astuta: el padre existe, no hay ciclo, y **el escalón cuadra** — se
    engancha un nodo del escalón 1 a una raíz del escalón 0. Lo único que la
    delata es `corrida`.

    🚨 Y no es una mentira de laboratorio: **es el bicho de esta misma sesión,
       un escalón más arriba.** Una línea de prueba colgando de una línea
       pagada, en el mismo archivo, con pinta de árbol correcto.
    """
    juntas = list(lineas_a) + list(lineas_b)
    raiz_a = _ids_por_tramo(lineas_a, "capa:")[0]
    hijo_b = _ids_por_tramo(lineas_b, "tool:")[0]
    fuera, n = _cambiar(juntas, hijo_b, padre=raiz_a)
    return fuera, (f"{hijo_b} (corrida B) pasa a colgar de {raiz_a} (corrida A), "
                   f"y el escalón cuadra ({n} líneas)")


def m5_a_la_hermana(lineas):
    """Una rama se mueve a su hermana de al lado. Todo lo demás, cuadrado.

    🚨 ESTA ES LA MENTIRA DEL PASO 1, PALABRA POR PALABRA. El gasto del `eur`
       pasa a figurar bajo la rama del `usd`, y el total no se mueve ni una
       millonésima. Lo único que cambia es de quién es hijo — que es justo el
       campo que se escribió hoy para arreglar aquello.

    🔑 Y el árbol que sale es **perfectamente válido**: el padre existe, el
       escalón cuadra, la corrida cuadra, no hay ciclo. No hay nada en el
       registro que lo desmienta, porque **esa corrida pudo haber ocurrido de
       verdad.** El auditor tiene que dejarla pasar, y su prueba lo exige.
    """
    victima = _ids_por_tramo(lineas, "worker:eur")[0]
    padre_viejo = next(d["padre"] for d in lineas if d.get("id") == victima)
    hermana = next(t for t in _ids_por_tramo(lineas, "tool:") if t != padre_viejo)
    fuera, n = _cambiar(lineas, victima, padre=hermana)
    return fuera, (f"{victima} se muda de {padre_viejo} a su hermana {hermana}; "
                   f"mismo escalón, misma corrida ({n} líneas)")


def experimento_padre(verboso=True):
    """Las cinco mentiras contra el auditor, sobre un registro GRABADO. $0,00.

    Devuelve `{nombre: (cazada, quejas, descripción)}`.
    """
    lineas_a = grabar_demo(verboso=False)
    ruta_b = AQUI / "_demo_b.jsonl"
    lineas_b = grabar_demo(ruta=ruta_b, verboso=False)
    ruta_b.unlink(missing_ok=True)

    casos = [
        ("1. padre fantasma", lambda: m1_padre_fantasma(lineas_a),
         {"padre_inexistente"}),
        ("2. ciclo", lambda: m2_ciclo(lineas_a), {"ciclo"}),
        ("3. profundidad vieja", lambda: m3_profundidad_vieja(lineas_a),
         {"profundidad"}),
        ("4. otra corrida", lambda: m4_otra_corrida(lineas_a, lineas_b),
         {"corrida"}),
        ("5. a la hermana", lambda: m5_a_la_hermana(lineas_a), set()),
    ]

    sano = auditar_arbol(lineas_a)
    resultados = {"0. sin torcer": (bool(sano), sano, "el registro tal cual se grabó")}

    if verboso:
        print("\n" + "=" * 72)
        print("  C.1 · PASO 3 — LAS CINCO MENTIRAS CONTRA EL AUDITOR")
        print("=" * 72)
        print(f"  Registro grabado ... {REGISTRO_DEMO.name}, {len(lineas_a)} líneas")
        informe_arbol(sano, "Sin torcer (si esto grita, no se puede medir nada):")

    for nombre, hacer, esperado in casos:
        torcidas, desc = hacer()
        quejas = auditar_arbol(torcidas)
        tipos = {q["tipo"] for q in quejas}
        resultados[nombre] = (bool(quejas), quejas, desc)
        if verboso:
            print(f"\n  {nombre.upper()}")
            print(f"    qué se torció: {desc}")
            informe_arbol(quejas, "")
            if esperado and not esperado <= tipos:
                print(f"    ⚠️ se esperaba {esperado} y salió {tipos or 'nada'}")

    if verboso:
        print("\n" + "-" * 72)
        print("  MARCADOR")
        for nombre, (cazada, quejas, _) in resultados.items():
            if nombre.startswith("0."):
                continue
            tipos = sorted({q["tipo"] for q in quejas})
            print(f"    {nombre:24} "
                  f"{'🚨 CAZADA' if cazada else '😶 pasa sin más'}"
                  f"   {', '.join(tipos)}")
        print("=" * 72)

    return resultados


# ---------------------------------------------------------------------------
# 6) C.1 · PASO 4 — LA FORMA ESPERADA, ESCRITA ANTES DE PAGAR
# ---------------------------------------------------------------------------
#
# 🚨 EL SOSPECHOSO DE ESTAR CIEGO, NOMBRADO EN EL SOBRE ANTES DE CORRER NADA, Y
#    ES EL PRIMERO QUE NO ES UN INSTRUMENTO SINO YO MIRANDO:
#
#        «la demo y la corrida real comparten casi todo el camino, así que voy a
#         mirar el árbol de verdad buscando confirmar la forma que ya vi»
#
#    Un árbol de once llamadas es lo bastante bonito como para asentir con la
#    cabeza, y «se ve bien» no es una medición.
#
#    → LA DEFENSA, Y ESTÁ EN EL ORDEN DE LOS COMMITS, NO EN LA INTENCIÓN: este
#      apartado se escribió y se commiteó **antes** de gastar el primer centavo.
#      La forma esperada son SEIS afirmaciones falsables por separado, y las
#      comprueba la máquina. Lo que yo opine del dibujo no entra.

def corrida_mas_reciente(lineas):
    """Se queda con las líneas de la ÚLTIMA corrida que aparece en el registro.

    🔑 Y fíjate en que esto **antes de hoy no se podía hacer**. Es el campo
       `corrida` ganándose el sueldo: en el mismo archivo conviven las líneas
       pagadas de cinco sesiones y las de la corrida de ahora, y hasta el paso 2
       no había **nada** que las separara. Es el bicho de esta sesión, resuelto
       por el campo que se añadió para otra cosa.
    """
    con_marca = [d for d in lineas if d.get("corrida")]
    if not con_marca:
        return []
    ultima = con_marca[-1]["corrida"]
    return [d for d in con_marca if d["corrida"] == ultima]


def comprobar_forma(lineas, verboso=True):
    """Las SEIS afirmaciones del sobre, comprobadas a máquina. Devuelve la lista
    de `(nº, texto, cumple, lo_que_salió)`.
    """
    a = arbol(lineas, verboso=False)
    quejas = auditar_arbol(lineas)

    # Gasto propio y profundidad por tramo, para no rehacerlos tres veces.
    propio, prof, nombre, apis = {}, {}, {}, {}
    for d in lineas:
        tid = d.get("id")
        if tid is None:
            continue
        nombre.setdefault(tid, d.get("tramo", "?"))
        prof.setdefault(tid, d.get("profundidad"))
        propio[tid] = round(propio.get(tid, 0.0) + d.get("costo_usd", 0.0), 6)
        if d.get("evento") == "llamada_api":
            apis[tid] = apis.get(tid, 0) + 1

    tools = [t for t in nombre if nombre[t].startswith("tool:")]
    workers = [t for t in nombre if nombre[t].startswith("worker:")]

    # 5) EL CRUCE, y es el que de verdad se apuesta: el árbol suma HACIA ARRIBA
    #    desde `padre`; `auditar()` suma en plano y no mira el parentesco. Dos
    #    caminos independientes hasta el mismo número. Es `LM.66` aplicado al
    #    propio instrumento.
    total_arbol = round(sum(a.get("total", {}).values()), 6)
    total_plano = round(sum(d.get("costo_usd", 0.0) for d in lineas
                            if d.get("evento") == "llamada_api"), 6)

    afirmaciones = [
        (1, "exactamente 1 raíz y profundidad máxima 2",
         len(a.get("raices", [])) == 1 and max(
             [v for v in prof.values() if v is not None] or [-1]) == 2,
         f"raíces={a.get('raices')}, profundidad máx="
         f"{max([v for v in prof.values() if v is not None] or [-1])}"),

        (2, "3 tramos `tool:` y todos con propio $0,000000",
         len(tools) == 3 and all(propio[t] == 0.0 for t in tools),
         {nombre[t]: propio[t] for t in tools}),

        (3, "3 tramos `worker:` y todos con propio > 0",
         len(workers) == 3 and all(propio[w] > 0 for w in workers),
         {nombre[w]: propio[w] for w in workers}),

        (4, "el auditor no tiene ni una queja sobre el registro sin torcer",
         not quejas, quejas),

        (5, "🔑 la suma del ÁRBOL cuadra con la factura PLANA",
         total_arbol == total_plano,
         f"árbol ${total_arbol:.6f} · plano ${total_plano:.6f}"),

        (6, "al menos un tramo con VARIAS `llamada_api` dentro (el bucle)",
         any(n > 1 for n in apis.values()),
         {nombre[k]: v for k, v in apis.items()}),
    ]

    if verboso:
        print("\n" + "=" * 72)
        print("  C.1 · PASO 4 — LA FORMA ESPERADA CONTRA LA QUE SALIÓ")
        print("=" * 72)
        for n, texto, cumple, salio in afirmaciones:
            print(f"  {'✅' if cumple else '❌'} {n}. {texto}")
            print(f"       → {salio}")
        rojas = [n for n, _, c, _ in afirmaciones if not c]
        print("-" * 72)
        if rojas:
            print(f"  ❌ {len(rojas)} afirmación(es) del sobre NO se cumplieron: {rojas}")
            print("     📌 No es un fracaso del paso 4: es la primera vez que este")
            print("        parentesco se mira fuera del laboratorio, y avisó.")
        else:
            print("  ✅ las 6 afirmaciones del sobre, cumplidas.")
        print("=" * 72)

    return afirmaciones


def paso4(verboso=True):
    """Lee los registros PAGADOS, se queda con la última corrida, dibuja su árbol
    y comprueba las seis afirmaciones. **No corre nada ni paga nada**: la corrida
    se lanza aparte con `python fan_out.py --paralelo`.

    📌 Se separa a propósito. Lo que cuesta dinero se pide con todas las letras y
       se hace una sola vez; leer el resultado es gratis y se puede repetir.
    """
    lineas = [d for v in leer(REGISTROS).values() for d in v]
    corrida = corrida_mas_reciente(lineas)
    if not corrida:
        print("  ⚠️ no hay ninguna corrida con parentesco en los registros pagados.")
        print("     Lánzala con:  python fan_out.py --paralelo")
        return None
    if verboso:
        print(f"\n  Corrida leída: «{corrida[0]['corrida']}» — {len(corrida)} líneas")
        arbol(corrida, verboso=True)
    return comprobar_forma(corrida, verboso=verboso)


# ---------------------------------------------------------------------------
# 7) EL PORTERO — ninguna prueba gratis puede escribir en el registro pagado
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
# 8) LAS PRUEBAS — $0,00
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

    # --- C.1 · PASO 3: torcer el parentesco y exigir rojo ------------------
    #
    # 🚨 ESTAS SIETE SON LA OBLIGACIÓN SELLADA EN EL SOBRE. Si `padre` no puede
    #    ponerse rojo al torcerlo, es el tercer adjetivo del registro —después
    #    de `capa` y `worker`— y C.1 cambió una etiqueta por otra más larga.

    a_lineas = grabar_demo(verboso=False)
    ruta_b = AQUI / "_prueba_b.jsonl"
    b_lineas = grabar_demo(ruta=ruta_b, verboso=False)
    ruta_b.unlink(missing_ok=True)

    def tipos_de(quejas):
        return {q["tipo"] for q in quejas}

    # 21) El registro grabado nace SANO. Sin esto no se puede medir nada: un
    #     auditor que ya grita antes de la mentira grita por otra cosa.
    check("21. el registro recién grabado no tiene ni una queja",
          not auditar_arbol(a_lineas), auditar_arbol(a_lineas))

    # 22) Mentira 1 — el padre no existe. La caza `padre` SOLO.
    q1 = auditar_arbol(m1_padre_fantasma(a_lineas)[0])
    check("22. 🚨 padre fantasma: ROJO, y lo caza `padre` solo",
          tipos_de(q1) == {"padre_inexistente"}, q1)

    # 23) Mentira 2 — ciclo. Y se comprueba TAMBIÉN que salte `profundidad`,
    #     porque un ciclo es la única mentira que no se puede cuadrar: en un
    #     ciclo no hay escalones posibles. **Hay mentiras que el segundo testigo
    #     delata siempre.**
    q2 = auditar_arbol(m2_ciclo(a_lineas)[0])
    check("23. 🚨 ciclo: ROJO por `ciclo` Y por `profundidad` (no se puede cuadrar)",
          {"ciclo", "profundidad"} <= tipos_de(q2), q2)

    # 24) Mentira 3 — padre real, escalón viejo. 🔑 ES LA PRUEBA DE QUE
    #     `profundidad` NO ES DECORACIÓN: con `padre` a secas esto sería
    #     invisible, porque el padre nuevo existe y es de la misma corrida.
    q3 = auditar_arbol(m3_profundidad_vieja(a_lineas)[0])
    check("24. 🚨 escalón viejo: ROJO, y SOLO lo caza el segundo testigo",
          tipos_de(q3) == {"profundidad"}, q3)

    # 25) Mentira 4 — colgar de otra corrida, con el escalón cuadrado a mano.
    #     Solo la caza `corrida`. Es el bicho de esta sesión un escalón arriba.
    q4 = auditar_arbol(m4_otra_corrida(a_lineas, b_lineas)[0])
    check("25. 🚨 padre de otra corrida: ROJO, y SOLO lo caza `corrida`",
          tipos_de(q4) == {"corrida"}, q4)

    # 26) 🚨 LA PRUEBA QUE EXIGE QUE EL INSTRUMENTO **FALLE**, y es la defensa
    #     contra el sospechoso de hoy: «el que elige las torceduras es el mismo
    #     que sabe cuáles su auditor puede cazar».
    #     Mover una rama a su hermana produce un árbol PERFECTAMENTE VÁLIDO: el
    #     padre existe, el escalón cuadra, la corrida cuadra, no hay ciclo. Y es
    #     la mentira del paso 1 palabra por palabra: el gasto del `eur` bajo la
    #     rama del `usd`, con el total sin moverse.
    #     🔑 Si mañana alguien enseña al auditor a cazarla, ESTA PRUEBA SE PONE
    #        ROJA y hay que venir aquí a tacharla. Es exactamente lo que tiene
    #        que pasar: el límite queda escrito, no supuesto.
    q5 = auditar_arbol(m5_a_la_hermana(a_lineas)[0])
    check("26. 🚨 a la hermana: el auditor la DEJA PASAR (límite medido, no supuesto)",
          not q5, q5)

    # 27) Ninguna torcedura mutó el original. Sin esto, la mentira 2 heredaría la
    #     1 y el marcador mediría mentiras acumuladas, no cada una.
    check("27. las cinco mentiras trabajan sobre copias: el original queda sano",
          not auditar_arbol(a_lineas), auditar_arbol(a_lineas))

    # 28) Y grabar la demo no toca los registros PAGADOS. El registro nuevo vive
    #     fuera de `REGISTROS` a propósito: el portero vigila los de verdad, y
    #     este se escribe adrede cada vez.
    antes = {r: sum(1 for _ in open(r, encoding="utf-8")) for r in REGISTROS}
    grabar_demo(verboso=False)
    despues = {r: sum(1 for _ in open(r, encoding="utf-8")) for r in REGISTROS}
    check("28. grabar la demo NO escribe ni una línea en el registro pagado",
          antes == despues, f"{antes} → {despues}")

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
    if "--paso4" in argv:
        r = paso4()
        return 0 if r and all(c for _, _, c, _ in r) else 1
    if "--padre" in argv:
        experimento_padre()
        return 0
    if "--portero" in argv:
        sucios, _ = portero()
        return 1 if sucios else 0
    return _pruebas()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
