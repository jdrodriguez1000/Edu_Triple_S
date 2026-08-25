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

    # 🚨 UN NODO ES (corrida, id), NO `id` — Y ESTO ES UN ARREGLO, NO UN DETALLE.
    #    El contador de tramos arranca de cero en cada proceso, así que dos
    #    corridas del mismo programa traen los mismos `t2`…`t8`. Cuando conviven
    #    en un archivo y el árbol las indexa solo por `id`, **se funden en una
    #    sola corrida que declara el doble de gasto y no da ni un error**
    #    (medido en el paso 4). La corrida ya es única; el par, también.
    def clave(d, tid):
        return (d.get("corrida"), tid)

    gasto = {}
    hijos, raices, nombre = {}, [], {}
    for d in lineas:
        tid = d.get("id")
        if tid is None:
            continue
        k = clave(d, tid)
        nombre.setdefault(k, d.get("tramo", "?"))
        gasto[k] = round(gasto.get(k, 0.0) + d.get("costo_usd", 0.0), 6)
        padre = d.get("padre")
        if padre is None:
            if k not in raices:
                raices.append(k)
        else:
            kp = clave(d, padre)
            hijos.setdefault(kp, [])
            if k not in hijos[kp]:
                hijos[kp].append(k)

    def total(tid):
        """El gasto de un tramo Y de todo lo que cuelga de él."""
        return round(gasto.get(tid, 0.0) + sum(total(h) for h in hijos.get(tid, [])), 6)

    if verboso:
        print("\n" + "=" * 72)
        print("  EL ÁRBOL DE LA CORRIDA — reconstruido de `id` y `padre`")
        print("=" * 72)

        def dibujar(k, sangria=""):
            propio = gasto.get(k, 0.0)
            print(f"  {sangria}{nombre[k]:28} {k[1]:5} "
                  f"total ${total(k):.6f}   propio ${propio:.6f}")
            for h in hijos.get(k, []):
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
#
# 📌 NO SUBE AL REPOSITORIO, y el motivo es la regla que ya está en `.gitignore`:
#    los `.jsonl` suben porque son EVIDENCIA de algo que se pagó. Este no lo es
#    —se regenera entero cada vez que corren las pruebas, con ids nuevos— así que
#    subirlo solo ensucia el `git status` de la siguiente sesión con un cambio
#    que no significa nada.
# ⚠️ Y se le quitó el `_c1` del nombre que tenía: venía de cuando las corridas se
#    llamaban `c1`, esquema que el paso 4 tuvo que matar. Un nombre de archivo
#    que cita un identificador difunto es una pista falsa esperando.
REGISTRO_DEMO = AQUI / "registro_demo_traza.jsonl"


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

    ✅ **LA QUINTA QUEJA, PAGADA EN LA SESIÓN 100** (`padre_doble`): que dos
       líneas con el mismo `id` declaren padres distintos. Llevaba dos sesiones
       apuntada como deuda y entra hoy con su torcedura al lado (`LM.13`).

    🚨 Y AL IR A ESCRIBIRLA APARECIÓ POR QUÉ NO SE PODÍA: **la estructura ya
       había tirado la prueba del delito.** Este cuerpo construía los nodos con
       `nodos.setdefault(...)`, que **se queda con la primera línea de cada `id`
       y descarta las demás en silencio**. Sobre los registros reales del curso
       eso son **134 líneas con `id` reducidas a 31**: 103 tiradas antes de
       auditar nada. Un desacuerdo entre la línea 1 y la línea 4 del mismo
       tramo era **invisible por construcción**, no por olvido.
       🔑 Antes de dar por difícil una comprobación que falta, mira si el dato
       que necesita sigue estando cuando llega el momento de comprobarlo. Aquí
       el auditor leía un resumen y creía leer el registro.
    """
    # Un nodo por `id`. Las líneas viejas sin marca se ignoran: no son un error
    # del árbol, son de antes de que el árbol existiera (prueba 19).
    # Mismo arreglo que en `arbol()`: la clave es (corrida, id). Sin esto, dos
    # corridas con los mismos `t2`…`t8` se auditan como una y salen limpias.
    #
    # ⭐ SE GUARDAN TODAS LAS DECLARACIONES, NO LA PRIMERA. Un tramo escribe
    #    varias líneas (inicio, llamadas, fin) y **todas dicen quién es su
    #    padre**. Que digan lo mismo no es un detalle: es la única forma de
    #    saber que nadie reescribió el parentesco a mitad de camino.
    declaraciones = {}
    nodos = {}
    for d in lineas:
        tid = d.get("id")
        if tid is None:
            continue
        clave = (d.get("corrida"), tid)
        declaraciones.setdefault(clave, []).append({
            "padre": d.get("padre"),
            "evento": d.get("evento", "?"),
            "hora": d.get("hora", "?"),
        })
        nodos.setdefault(clave, {
            "padre": d.get("padre"),
            "profundidad": d.get("profundidad"),
            "corrida": d.get("corrida"),
            "tramo": d.get("tramo", "?"),
        })

    quejas = []

    def quejarse(tipo, tid, detalle):
        quejas.append({"tipo": tipo, "id": tid, "detalle": detalle})

    # 0) 🚨 `padre_doble` — EL MISMO `id` DECLARANDO DOS PADRES DISTINTOS.
    #    Va la PRIMERA a propósito: si el parentesco de un tramo no está de
    #    acuerdo consigo mismo, las cuatro quejas de abajo están auditando **una
    #    de las dos versiones**, la que salió primero, y su veredicto no vale.
    #    ⚠️ Un `padre` ausente (`None`) en una línea y presente en otra también
    #    cuenta: «no tengo padre» y «mi padre es t3» son afirmaciones distintas,
    #    y tratar la ausencia como «no dijo nada» es justo cómo se cuela una
    #    raíz falsa en mitad de una rama.
    for (corr, tid), decls in declaraciones.items():
        distintos = {d["padre"] for d in decls}
        if len(distintos) > 1:
            quejarse("padre_doble", tid,
                     f"declara {len(distintos)} padres distintos en "
                     f"{len(decls)} líneas: "
                     + ", ".join(f"{d['evento']}→{d['padre']!r}" for d in decls))

    for (corr, tid), n in nodos.items():
        padre = n["padre"]
        kp = (corr, padre)

        # 1) El padre tiene que existir. Una raíz (padre None) es legítima.
        #    📌 Se busca DENTRO de la misma corrida: un padre que solo existe en
        #       otra corrida es un padre inexistente, no un padre de otra
        #       corrida. Esa distinción es la que hace falsable la mentira 4.
        if padre is not None and kp not in nodos:
            # 🔑 DOS DIAGNÓSTICOS DISTINTOS, Y LA DIFERENCIA IMPORTA. Si el
            #    padre no está en NINGUNA corrida, se perdió. Si está pero en
            #    OTRA, alguien cruzó dos corridas — que no es lo mismo y no se
            #    arregla igual.
            #    📌 Este `else` nació de una prueba en rojo: al hacer que la
            #       clave fuera (corrida, id), la queja `corrida` se quedó sin
            #       forma de dispararse y la prueba 25 lo cazó en el acto. Un
            #       arreglo correcto puede dejar muerto a un detector correcto.
            otras = sorted({c for (c, i) in nodos if i == padre and c != corr})
            if otras:
                quejarse("corrida", tid,
                         f"su padre «{padre}» no está en su corrida «{corr}», "
                         f"sino en {otras}")
            else:
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

        p = nodos[kp]

        # 3) El contador contra el apuntador. Aquí es donde `profundidad` deja
        #    de ser decoración del dibujo y se vuelve testigo.
        if (None not in (n["profundidad"], p["profundidad"])
                and n["profundidad"] != p["profundidad"] + 1):
            quejarse("profundidad", tid,
                     f"dice escalón {n['profundidad']}, pero su padre «{padre}» "
                     f"está en el {p['profundidad']}")

        # 4) ⚠️ AQUÍ HABÍA UNA COMPROBACIÓN Y SE RETIRÓ, CON SU MOTIVO:
        #    «padre e hijo tienen que ser de la misma corrida». Al pasar la clave
        #    de `id` a `(corrida, id)`, padre e hijo son de la misma corrida
        #    **por construcción** y la comprobación no podía fallar nunca. El
        #    caso que cazaba no desapareció: subió al `if` de arriba, donde
        #    ahora se distingue «tu padre se perdió» de «tu padre es de otra
        #    corrida». 🔑 Se anota porque es lo contrario de lo que uno espera:
        #    **arreglar la clave dejó muerto a un detector que funcionaba.**

    # 4.b) 🚨 C.4 — EL TRAMO QUE SE ABRIÓ Y NO CERRÓ.
    #
    #    Las cinco quejas de arriba se disparan porque **dos datos se
    #    contradicen**. Esta no: se dispara porque **falta uno**, y por eso hubo
    #    que escribirla aparte. Un worker que revienta anota su `worker_inicio`
    #    y muere antes del `worker_fin`. El árbol que sale es impecable: el
    #    `padre` existe, la `profundidad` cuadra, la `corrida` es la misma.
    # 🔑 `LM.66` al revés. Aquella decía que un dato que nadie puede desmentir
    #    no es correcto, es **no comprobable**. Esto es peor: no hay dato
    #    ninguno, y **la ausencia no contradice a nadie**. Medido en `fallos.py`
    #    antes de escribir esta comprobación: 1 `worker_inicio`, 0 `worker_fin`,
    #    **0 quejas del auditor**.
    #
    # 📌 SE MIRA POR EL SUFIJO DEL EVENTO, no por el nombre del tramo. Los 5
    #    pares del repo —`worker`, `orquestador`, `duelo`, `pipeline`,
    #    `corrida`— usan todos `_inicio`/`_fin`, y así la comprobación cubre
    #    también a los que se escriban mañana sin tener que acordarse de ella.
    # ⚠️ Y SOLO SE MIRA EN UNA DIRECCIÓN, a propósito: un `_fin` huérfano NO se
    #    denuncia. Existen de verdad y son legítimos (`exp1_fin`… de los
    #    experimentos de C.1, que nunca abrieron nada). Denunciarlos sería un
    #    falso positivo del mismo tipo que el de ayer.
    aperturas = {}
    cierres = {}
    for d in lineas:
        tid = d.get("id")
        evento = d.get("evento") or ""
        if tid is None:
            continue
        clave = (d.get("corrida"), tid)
        if evento.endswith("_inicio"):
            aperturas.setdefault(clave, evento)
        elif evento.endswith("_fin"):
            cierres.setdefault(clave, evento)

    for clave, evento in aperturas.items():
        if clave not in cierres:
            quejarse("nodo_abierto", clave[1],
                     f"anotó «{evento}» y nunca su cierre: el tramo "
                     f"«{nodos.get(clave, {}).get('tramo', '?')}» se abrió y "
                     f"no se sabe cómo terminó")

    # 5) Ciclos. Se busca subiendo desde cada nodo: si se vuelve a pisar un id ya
    #    pisado en ESTE camino, la rama se muerde la cola. Sin esto, `arbol()`
    #    entraría en recursión infinita y el síntoma sería un `RecursionError`,
    #    que no dice nada de lo que pasó.
    for k in nodos:
        visto, actual_k = [], k
        while actual_k is not None and actual_k in nodos:
            if actual_k in visto:
                quejarse("ciclo", k[1], " → ".join(v[1] for v in visto + [actual_k]))
                break
            visto.append(actual_k)
            siguiente = nodos[actual_k]["padre"]
            actual_k = None if siguiente is None else (actual_k[0], siguiente)

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
         {f"{nombre[x]} ({x})": propio[x] for x in tools}),

        (3, "3 tramos `worker:` y todos con propio > 0",
         len(workers) == 3 and all(propio[w] > 0 for w in workers),
         {f"{nombre[x]} ({x})": propio[x] for x in workers}),

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
# 7) C.1 · PASO 5 — EL ADJETIVO CONTRA EL HECHO
# ---------------------------------------------------------------------------
#
# 🔑 LA IDEA, Y ES LA DEL PASO 3 UN CAMPO MÁS ALLÁ.
#    Cada línea `worker_fin` del registro lleva DOS cosas que hablan de la misma
#    moneda por caminos que no se pueden coordinar:
#
#      · `worker` (y su `tramo`) → **el adjetivo**: cómo se llamó a quien trabajó.
#        Sale del argumento `nombre=`, y el paso 1 midió que es decorativo.
#      · `datos.moneda`          → **el hecho**: qué moneda salió del contrato de
#        A.3, producida por la herramienta que de verdad hizo la cuenta.
#
#    Si no coinciden, alguien miente. Es `LM.66` exactamente: **un dato se vuelve
#    comprobable el día que hay otro que puede desmentirlo.**
#
# 🚨 Y AQUÍ VIENE LO QUE HACE ESTO DISTINTO DE LOS PASOS 2, 3 Y 4: no hay que
#    grabar nada nuevo. **Los dos testigos llevan en el registro desde la sesión
#    93.** No faltaba un campo — faltaba alguien que le preguntara.

MONEDAS = ("usd", "eur", "cad")


def auditar_etiquetas(lineas):
    """Compara el NOMBRE de quien trabajó contra la moneda de su contrato.

    Devuelve `(contradicciones, comprobadas, no_comprobables)`.

    📌 LA REGLA, ESCRITA EN GENERAL Y NO A LA MEDIDA DE LO QUE ENCONTRÓ:
       si el nombre del worker menciona una moneda conocida y su contrato trae
       otra, es una contradicción. Si el nombre no menciona ninguna moneda
       (`1-recolector`, `divisa`, `2-redactor`), **no se puede comprobar y se
       dice** — un auditor que calla lo que no sabe mirar miente por omisión.

    ⚠️ EL SOSPECHOSO, NOMBRADO EN EL SOBRE: quien escribe esta regla ya vio el
       registro. Por eso la regla se aplica a TODAS las líneas y el informe
       publica también **cuántas pasó y cuántas no supo mirar**. Un detector que
       solo enseña lo que cazó no se distingue de uno escrito para cazar eso.
    """
    contradicciones, comprobadas, no_comprobables = [], 0, []
    for d in lineas:
        if d.get("evento") != "worker_fin":
            continue
        nombre = str(d.get("worker") or "")
        real = ((d.get("datos") or {}).get("moneda") or "").lower()
        dicha = next((m for m in MONEDAS if m in nombre.lower()), None)

        if not real or dicha is None:
            no_comprobables.append((nombre, d.get("hora"), "sin contrato"
                                    if not real else "el nombre no dice moneda"))
            continue
        comprobadas += 1
        if dicha != real:
            contradicciones.append({
                "hora": d.get("hora"),
                "se_llama": nombre,
                "hizo": real.upper(),
                "encargo": str(d.get("encargo", "")).splitlines()[0][:60],
                "tramo": d.get("tramo"),
                "id": d.get("id"),
            })
    return contradicciones, comprobadas, no_comprobables


def paso5(verboso=True):
    """C.1 · PASO 5 — le lleva el árbol (y el tercer testigo) al defecto de la
    sesión 95. **$0,00: solo lee lo que ya se pagó.**
    """
    lineas = [d for v in leer(REGISTROS).values() for d in v]
    contra, ok, mudas = auditar_etiquetas(lineas)

    if not verboso:
        return contra, ok, mudas

    print("\n" + "=" * 72)
    print("  C.1 · PASO 5 — EL ADJETIVO CONTRA EL HECHO, sobre el registro PAGADO")
    print("=" * 72)
    print(f"  Líneas `worker_fin` comprobadas ..... {ok}")
    print(f"  No comprobables (y se dice) ......... {len(mudas)}")
    print(f"  🚨 Contradicciones .................. {len(contra)}")
    for c in contra:
        print()
        print(f"    {c['hora']}")
        print(f"      se llama ....... worker «{c['se_llama']}»")
        print(f"      pero hizo ...... {c['hizo']}")
        print(f"      encargo ........ {c['encargo']}")
    print()
    print("  Por qué no se pudieron comprobar las otras:")
    razones = {}
    for _, _, r in mudas:
        razones[r] = razones.get(r, 0) + 1
    for r, n in sorted(razones.items()):
        print(f"    {n:3} × {r}")
    print("=" * 72)
    return contra, ok, mudas


# ---------------------------------------------------------------------------
# 8) EL PORTERO — ninguna prueba gratis puede escribir en el registro pagado
# ---------------------------------------------------------------------------

# 📎 SESIÓN 111 — LA LISTA SUBE A CONSTANTE, Y NO ES COSMÉTICA.
#    La prueba 8 llevaba clavado `len(corridos) == 5`. Al entrar un módulo
#    sexto se puso roja **sin que nada estuviera mal**, que es el mismo defecto
#    que tiene hoy `avisador.py`: una prueba que compara contra un número
#    escrito a mano caduca el día que el sistema crece.
# 🔑 Con la lista aquí arriba, el portero y su prueba miran EL MISMO dato, y el
#    invariante deja de ser un número para ser una frase: **se corrió todo lo
#    que se dijo que se iba a correr.**
VIGILADOS = ["fan_out", "profundidad", "router", "supervisor", "verificador",
             # entra el día que se le pilla ensuciando el registro pagado.
             "evals_orquestador"]

# Los que NO se vigilan, con su razón. No es una lista de excusas: es lo que
# permite distinguir «decidido que no» de «se nos olvidó».
NO_VIGILADOS = {
    "traza": "es este archivo: se estaría corriendo a sí mismo",
    "disparador": "lanza procesos y tarda minutos; su registro es propio",
    "compartida": "escribe en su propio archivo compartido, no en estos",
    "skills_compartidas": "no toca los registros del duelo",
    "avisador": "solo LEE registros; no anota",
    "atribuidor": "solo LEE registros; una prueba propia le impide anotar",
    "modelos": "sus pruebas no arrancan capas",
    "presupuesto": "desvía su propio registro y lo comprueba él mismo",
    "recursion": "desvía su propio registro",
    "fallos": "desvía su propio registro",
}


def portero(verboso=True):
    """Corre las pruebas gratis de TODO el nivel y exige que los registros
    reales no crezcan ni una línea.

    🚨 POR QUÉ EXISTE. En la sesión 97 se descubrió que la prueba 2 de
       `profundidad.py` escribía en `registro_orquestador_*.jsonl`, el archivo
       de las corridas PAGADAS. Cuatro líneas inventadas ya estaban dentro, y
       **una de ellas commiteada**. Nadie lo notó en dos sesiones.

    🔑 Y ESTE ES EL ARREGLO DE VERDAD, NO EL `with` DE ALLÁ.
       Desviar el registro en `profundidad.py` arregla UN archivo. El portero
       arregla la CLASE: cualquier prueba de los módulos que vigila que escriba
       en el registro real pone esto rojo. Es la lección de la sesión 49 de
       TEAPP: el arreglo va en el origen, y encima se le pone un portero sobre
       los datos enteros.

    🚨 CORRECCIÓN DE LA SESIÓN 111, Y ESTA DOCSTRING DECÍA UNA MENTIRA.
       Decía *«cualquier prueba de cualquier módulo —incluidos los que todavía
       no existen—»*. **Falso, y se demostró el día que se corrigió:**
       `evals_orquestador.py`, nacido esa mañana, escribió tres `sin_trozo` en
       el registro pagado y **este portero se quedó verde**, porque su lista
       decía cinco nombres y ese archivo no estaba en ella.

    🔑 **Un portero que vigila una LISTA no vigila una clase: vigila esa lista,
       y una lista se queda vieja el día siguiente.** Lo que sí escala es que
       el portero se queje cuando aparece un módulo con pruebas que nadie
       clasificó — y eso es `NO_VIGILADOS` y la comprobación de abajo.

    📌 Y se corre a ciegas a propósito: no le importa QUÉ prueba ensució, solo
       que alguien lo hizo. Un portero que necesita saber a quién vigilar solo
       caza a los que ya sospechabas.
    """
    import importlib

    # La convención del nivel: cada módulo con pruebas gratis expone `_pruebas`.
    nombres = VIGILADOS

    # 🚨 LOS QUE NO SE VIGILAN, CON SU RAZÓN ESCRITA. No es una lista de
    #    excusas: es lo que permite que la comprobación de más abajo distinga
    #    «decidido que no» de «se nos olvidó». Sin ella, un módulo nuevo se cuela
    #    en silencio, que es exactamente lo que pasó el 2026-08-25.
    no_vigilados = NO_VIGILADOS
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

    # 🚨 LA COMPROBACIÓN QUE FALTABA: ¿hay algún módulo con pruebas que nadie
    #    haya clasificado? Se lee el código fuente, no se importa nada — no
    #    hace falta correrlo para saber que existe.
    huerfanos = []
    for f in sorted(AQUI.glob("*.py")):
        mod = f.stem
        if "def _pruebas" not in f.read_text(encoding="utf-8"):
            continue
        if mod not in nombres and mod not in no_vigilados:
            huerfanos.append(mod)

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
        if huerfanos:
            print(f"  🚨 MÓDULOS CON PRUEBAS Y SIN CLASIFICAR: {', '.join(huerfanos)}")
            print("     No se sabe si ensucian: nadie los corre ni los descarta.")
        else:
            print("  ✅ todo módulo con `_pruebas` está vigilado o descartado con razón.")
        print("=" * 72)

    return sucios + [("SIN CLASIFICAR", 0, m) for m in huerfanos], corridos


# ---------------------------------------------------------------------------
# 9) LAS PRUEBAS — $0,00
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
          not sucios and set(corridos) == set(VIGILADOS),
          f"corridos={corridos}, sucios={sucios}, vigilados={VIGILADOS}")

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
        {"corrida": "cX", "id": "t1", "padre": None, "tramo": "raiz", "costo_usd": 1.0},
        {"corrida": "cX", "id": "t2", "padre": "t1", "tramo": "hijo-a", "costo_usd": 0.0},
        {"corrida": "cX", "id": "t3", "padre": "t2", "tramo": "nieto", "costo_usd": 2.0},
        {"corrida": "cX", "id": "t4", "padre": "t1", "tramo": "hijo-b", "costo_usd": 4.0},
        {"evento": "sin marca"},                       # línea vieja, sin traza
    ]
    a = arbol(falsas, verboso=False)
    check("18. el árbol suma hacia arriba: el padre incluye a sus nietos",
          a["raices"] == [("cX", "t1")] and a["total"][("cX", "t1")] == 7.0, a)
    check("19. y una línea SIN marca no inventa una raíz nueva",
          len(a["raices"]) == 1, a["raices"])

    # 20) ⚠️ LO QUE EL ÁRBOL NO PUEDE HACER, Y SE PRUEBA PARA QUE NO SE OLVIDE:
    #     los registros pagados de las sesiones 92-96 NO tienen `id` ni `padre`,
    #     y por eso NO se pueden convertir en árbol. No es caro: es imposible.
    #     🔑 La traza es la única pieza del harness que no se puede añadir hacia
    #        atrás. Lo que no se instrumentó, no ocurrió.
    #    📌 ESTA PRUEBA SE REESCRIBIÓ EN EL PASO 4, Y EL MOTIVO ES BUENO: se
    #       puso roja porque el paso 4 pagó una corrida NUEVA, que sí tiene
    #       parentesco. Decía «ninguna línea pagada tiene padre» y eso dejó de
    #       ser cierto ese mismo día. Lo que NO cambió es la lección: las líneas
    #       de las sesiones 92-96 siguen sin parentesco y **siguen sin poder
    #       tenerlo**. Se afirma eso, que es lo que `LM.65` dice de verdad.
    viejas = [d for v in leer(REGISTROS).values() for d in v]
    sin_traza = [d for d in viejas if "id" not in d]
    a_viejas = arbol(sin_traza, verboso=False)
    check("20. ⚠️ las líneas pagadas de las sesiones 92-96 no dan NINGÚN árbol",
          len(sin_traza) > 0 and not a_viejas.get("raices"),
          f"{len(sin_traza)} líneas sin traza → raíces={a_viejas.get('raices')}")

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

    # --- C.1 · PASO 4: la SEXTA mentira, la que no escribí yo ---------------
    #
    # 🚨 LAS CINCO DEL PASO 3 LAS INVENTÉ YO. ESTA LA ESCRIBE EL HARNESS SOLO,
    #    cada vez que se corre dos veces. Y hasta el paso 4 la dejaba pasar:
    #    dos corridas de $0,026390 se fundían en un árbol que declaraba
    #    $0,052780, sin una sola queja.
    #    🔑 Y no es como la quinta. La quinta pasa porque describe un mundo
    #       posible. Esta describía **un mundo que no ocurrió.**

    def _corrida(nombre_corrida):
        return [
            {"corrida": nombre_corrida, "id": "t2", "padre": None,
             "profundidad": 0, "tramo": "capa:orq", "evento": "llamada_api",
             "costo_usd": 1.0},
            {"corrida": nombre_corrida, "id": "t3", "padre": "t2",
             "profundidad": 1, "tramo": "worker:usd", "evento": "llamada_api",
             "costo_usd": 2.0},
        ]

    # 29) Dos corridas DISTINTAS con los MISMOS ids de tramo. Es exactamente lo
    #     que escribe el programa al correrlo dos veces, porque el contador de
    #     tramos arranca de cero en cada proceso.
    dos = _corrida("cA") + _corrida("cB")
    a_dos = arbol(dos, verboso=False)
    check("29. 🚨 dos corridas con los mismos ids NO se funden (la sexta mentira)",
          len(a_dos["raices"]) == 2
          and set(a_dos["total"].values()) == {3.0},
          f"raíces={a_dos['raices']}, totales={a_dos['total']}")

    # 30) Y el arreglo del ORIGEN: dos procesos distintos ya no dan la misma
    #     corrida. Se comprueba lanzando Python de verdad dos veces, porque el
    #     bicho vivía justo en el arranque del proceso y dentro de UNO solo no
    #     se puede ver. Es la lección de la sesión 50 de TEAPP: el experimento
    #     tiene que poder observar el sitio donde falla.
    import subprocess
    guion = ("import contexto\n"
             "with contexto.tramo('x') as a: print(a['corrida'])")
    salidas = [subprocess.run([sys.executable, "-c", guion], cwd=AQUI,
                              capture_output=True, text=True).stdout.strip()
               for _ in range(2)]
    check("30. 🚨 dos PROCESOS distintos ya no dan la misma corrida (visto morder)",
          len(set(salidas)) == 2 and all(s.startswith("c2") for s in salidas),
          salidas)

    # 31) Y los tramos siguen siendo cortos y en orden dentro de su corrida: el
    #     arreglo no se llevó por delante lo que el contador hacía bien.
    with contexto.tramo("a") as uno:
        with contexto.tramo("b") as dos_t:
            pass
    check("31. los ids de tramo siguen cortos y en orden (`t` + número)",
          uno["id"][0] == "t" and uno["id"][1:].isdigit()
          and int(dos_t["id"][1:]) > int(uno["id"][1:]),
          f"{uno['id']} → {dos_t['id']}")

    # --- C.1 · PASO 5: el adjetivo contra el hecho --------------------------

    contra, comprobadas, mudas = auditar_etiquetas(
        [d for v in leer(REGISTROS).values() for d in v])

    # 32) 🚨 LA LÍNEA DE LA SESIÓN 95, CAZADA SOBRE EL REGISTRO PAGADO DE VERDAD.
    #     No es una reproducción ni un cebo nuevo: es la línea que se escribió el
    #     2026-08-20 a las 20:32:23, que costó dinero y lleva en el repo desde
    #     entonces. El worker se llama `usd` y su contrato dice `EUR`.
    check("32. 🚨 la contradicción de la sesión 95, cazada en el registro PAGADO",
          any(c["se_llama"] == "usd" and c["hizo"] == "EUR"
              and c["hora"].startswith("2026-08-20T20:32") for c in contra),
          contra)

    # 32b) 🚨 LA SEGUNDA, Y ES EL HALLAZGO DE LA SESIÓN 100.
    #      La corrida pagada de la 99 grabó otra contradicción: el worker `cad`
    #      subió un contrato que decía `USD`. Es la mentira que C.3 arregla hoy.
    #      ⭐ Y LO QUE ENSEÑA NO ES QUE EL AUDITOR FUNCIONE — ES CUÁNDO SE VIO.
    #      `auditar_etiquetas` existe desde C.1 paso 5 y cazaba esta línea desde
    #      el segundo en que se escribió. Ayer el hallazgo lo hizo un humano
    #      leyendo la salida a ojo: **nadie corrió `traza.py` después de pagar.**
    #      🔑 Un detector que muerde y cuyo mordisco nadie va a mirar da el mismo
    #      silencio que uno que no muerde. Es `LM.13` girado del revés, y aquí la
    #      prueba 33 llevaba una noche en rojo sin que nadie la viera.
    check("32b. 🚨 y la de la sesión 99 también: `cad` subió un contrato de USD",
          any(c["se_llama"] == "cad" and c["hizo"] == "USD"
              and c["hora"].startswith("2026-08-21T19:41") for c in contra),
          contra)

    # 33) Y NO caza nada más. Es lo que separa un auditor de un detector escrito
    #     para encontrar la línea que ya habías visto: las sanas pasan.
    # ⚠️ Se comprueba por HORA y no por cuenta. Antes decía `len(contra) == 1`,
    #    y un número pelado envejece: bastó que el mundo grabara una segunda
    #    mentira de verdad para que la prueba se pusiera roja sin que nada se
    #    hubiera roto. Nombrándolas, una TERCERA contradicción sí la pondría
    #    roja — que es lo que se quería vigilar.
    # 🎁 LA TERCERA ES DE LA CORRIDA PAGADA DE C.3 ($0,028745), Y SALIÓ PORQUE
    #    ESTA VEZ SE CORRIÓ `traza.py` DESPUÉS DE PAGAR. Es `LM.70` cobrando a
    #    la sesión siguiente de haberse aprendido.
    # ⚠️ Y es una contradicción REAL de una conducta que ya está arreglada: el
    #    worker `cad` guardó `COP` porque el contrato de entonces se quedaba con
    #    el ÚLTIMO paso de la cadena. Con «el primero gana» esa línea saldría
    #    hoy como `CAD`. **Se deja en la lista porque el registro no se reescribe:
    #    es la huella del defecto, y borrarla sería borrar la evidencia.**
    CONOCIDAS = ("2026-08-20T20:32", "2026-08-21T19:41", "2026-08-21T20:25")
    check("33. y las demás comprobables pasan limpias (no es un detector de una)",
          all(c["hora"].startswith(CONOCIDAS) for c in contra)
          and comprobadas >= 20,
          f"{len(contra)} contradicción(es) de {comprobadas} comprobadas: "
          f"{[c['hora'] for c in contra]}")

    # 34) 🚨 VISTO MORDER, con las dos mitades en la misma corrida: la misma
    #     forma de línea, una torcida y otra sana.
    sana = [{"evento": "worker_fin", "worker": "cad",
             "datos": {"moneda": "CAD"}, "encargo": "x"}]
    torcida = [{"evento": "worker_fin", "worker": "cad",
                "datos": {"moneda": "USD"}, "encargo": "x"}]
    check("34. 🚨 el auditor de etiquetas MUERDE: sana en verde, torcida en rojo",
          not auditar_etiquetas(sana)[0] and len(auditar_etiquetas(torcida)[0]) == 1,
          (auditar_etiquetas(sana)[0], auditar_etiquetas(torcida)[0]))

    # 35) Y lo que NO puede este auditor, dicho con su número: 15 líneas del
    #     registro pagado no traen contrato y **no se pueden comprobar**. Un
    #     auditor que callara eso mentiría por omisión.
    check("35. las líneas sin contrato se declaran NO comprobables, no verdes",
          len(mudas) > 0 and all(r for _, _, r in mudas), len(mudas))

    # 36) 🚨 EL VEREDICTO DE LA APUESTA 1, EN CÓDIGO Y NO EN PROSA.
    #     El árbol bautiza sus nodos con `envuelto("nombre")`, que es el MISMO
    #     argumento que la inyección de la sesión 95 torcía. Así que un árbol
    #     dibujado sobre esa corrida habría enseñado dos ramas `worker:usd` y
    #     ninguna `eur` — el mismo síntoma ambiguo que costó la 95.
    #     🔑 Un árbol cuyos nodos se bautizan con un adjetivo HEREDA la mentira
    #        del adjetivo. La segunda mitad de la apuesta 1 queda FALLADA, y se
    #        queda aquí escrita para que no se pueda contar de otra manera.
    @contexto.envuelto("nombre", prefijo="worker:")
    def _worker_de_mentira(encargo, nombre="divisa"):
        return contexto.marca()["tramo"]

    honesto = _worker_de_mentira("Convierte 400 EUR a pesos", nombre="eur")
    mentiroso = _worker_de_mentira("Convierte 400 EUR a pesos", nombre="usd")
    check("36. 🚨 el árbol HEREDA la mentira de la etiqueta (apuesta 1, 2ª mitad: FALLADA)",
          honesto == "worker:eur" and mentiroso == "worker:usd",
          f"mismo encargo → «{honesto}» y «{mentiroso}»")

    # --- 37-41 · `padre_doble`: LA DEUDA DE C.1, PAGADA EN LA SESIÓN 100 ------
    # 🚨 Llevaba dos sesiones escrita como «lo que este auditor NO comprueba».
    #    Entra hoy, y entra con su torcedura al lado: `LM.13`.

    # La forma sana: un tramo escribe VARIAS líneas y todas dicen el mismo padre.
    SANO = [
        {"corrida": "cX", "id": "t1", "padre": None, "profundidad": 0, "evento": "inicio"},
        {"corrida": "cX", "id": "t2", "padre": "t1", "profundidad": 1, "evento": "inicio"},
        {"corrida": "cX", "id": "t2", "padre": "t1", "profundidad": 1, "evento": "llamada_api"},
        {"corrida": "cX", "id": "t2", "padre": "t1", "profundidad": 1, "evento": "fin"},
    ]
    check("37. el árbol sano NO dispara `padre_doble` (varias líneas, un padre)",
          not [q for q in auditar_arbol(SANO) if q["tipo"] == "padre_doble"],
          auditar_arbol(SANO))

    # 🚨 LA TORCEDURA: la misma corrida, el mismo `id`, y a mitad de camino el
    #    tramo cambia de padre. Es la mentira que `setdefault` hacía invisible.
    TORCIDO = [dict(d) for d in SANO]
    TORCIDO[3]["padre"] = "t9"
    quejas_t = auditar_arbol(TORCIDO)
    check("38. 🚨 MUERDE: el mismo `id` con dos padres distintos se caza",
          any(q["tipo"] == "padre_doble" and q["id"] == "t2" for q in quejas_t),
          quejas_t)

    # 39) La ausencia TAMBIÉN es una declaración. «no tengo padre» y «mi padre es
    #     t1» son afirmaciones distintas, y tratar el `None` como «no dijo nada»
    #     es justo cómo se cuela una raíz falsa en mitad de una rama.
    HUERFANO = [dict(d) for d in SANO]
    HUERFANO[2]["padre"] = None
    check("39. y un `padre` que DESAPARECE en una línea también cuenta",
          any(q["tipo"] == "padre_doble" for q in auditar_arbol(HUERFANO)),
          auditar_arbol(HUERFANO))

    # 40) ⭐ EL MOTIVO DE QUE VAYA LA PRIMERA, HECHO PRUEBA. Con el parentesco en
    #     desacuerdo consigo mismo, las otras cuatro quejas están auditando UNA
    #     de las dos versiones —la que salió primero— y su veredicto no vale.
    #     Que `padre_doble` aparezca es lo que avisa de que el resto es dudoso.
    check("40. `padre_doble` sale ANTES que las demás quejas del mismo árbol",
          quejas_t[0]["tipo"] == "padre_doble",
          [q["tipo"] for q in quejas_t])

    # 41) 🎲 LA APUESTA 5 DE LA SESIÓN 100, EVALUADA SOBRE LOS REGISTROS REALES.
    #     Sellada esta mañana: *«el detector nace SIN MORDER: no encuentra ni un
    #     caso en los `.jsonl` que ya hay»*. Se comprueba aquí, gratis, y queda
    #     como vigilancia: si algún día un registro real lo dispara, esta se pone
    #     roja y hay que ir a mirar.
    reales = [d for v in leer(REGISTROS).values() for d in v]
    dobles_reales = [q for q in auditar_arbol(reales) if q["tipo"] == "padre_doble"]
    check("41. 🎲 apuesta 5: sobre los registros REALES no muerde (GANADA)",
          dobles_reales == [],
          f"{len(dobles_reales)} caso(s): {dobles_reales}")

    # --- 42-45 · `nodo_abierto`: LA QUEJA DE C.4 ----------------------------
    # 🚨 Entra con su torcedura al lado, como manda `LM.13`. Y la torcedura de
    #    esta es rara: **no se tuerce nada, se BORRA**. Un worker que revienta
    #    no escribe un dato falso — deja de escribir.

    ABIERTO = [
        {"corrida": "cY", "id": "t1", "padre": None, "profundidad": 0,
         "evento": "orquestador_inicio", "tramo": "capa:orquestador"},
        {"corrida": "cY", "id": "t1", "padre": None, "profundidad": 0,
         "evento": "orquestador_fin", "tramo": "capa:orquestador"},
        {"corrida": "cY", "id": "t2", "padre": "t1", "profundidad": 1,
         "evento": "worker_inicio", "tramo": "worker:usd"},
        {"corrida": "cY", "id": "t2", "padre": "t1", "profundidad": 1,
         "evento": "llamada_api", "tramo": "worker:usd", "costo_usd": 0.002},
        # ⚠️ AQUÍ NO HAY `worker_fin`. Eso es todo el defecto.
    ]
    quejas_a = auditar_arbol(ABIERTO)
    check("42. 🚨 MUERDE: un `worker_inicio` sin su `worker_fin` se caza",
          any(q["tipo"] == "nodo_abierto" and q["id"] == "t2" for q in quejas_a),
          quejas_a)

    # 43) ⭐ Y ESTA ES LA QUE DE VERDAD SE APUESTA: el árbol de arriba es
    #     IMPECABLE para las otras cinco quejas. Padre real, escalón cuadrado,
    #     misma corrida, sin ciclo, un solo padre por tramo. **Antes de C.4 este
    #     registro salía verde entero.** Si mañana alguien encuentra otra queja
    #     que también lo cace, esta prueba lo dirá.
    check("43. ⭐ y es la ÚNICA que lo caza: las otras cinco lo dan por sano",
          [q["tipo"] for q in quejas_a] == ["nodo_abierto"],
          [q["tipo"] for q in quejas_a])

    # 44) El otro lado, que es lo que separa un detector de una alarma que
    #     siempre suena: cerrado el tramo, se calla.
    CERRADO = ABIERTO + [{"corrida": "cY", "id": "t2", "padre": "t1",
                          "profundidad": 1, "evento": "worker_fin",
                          "tramo": "worker:usd"}]
    check("44. y con el `worker_fin` puesto, se calla",
          not [q for q in auditar_arbol(CERRADO) if q["tipo"] == "nodo_abierto"],
          auditar_arbol(CERRADO))

    # 45) 🚨 EL FALSO POSITIVO QUE SE DECIDIÓ NO COMETER. Un `_fin` sin `_inicio`
    #     existe de verdad en el repo —`exp1_fin`… de los experimentos de C.1—
    #     y es legítimo. Denunciarlo sería inventarse un defecto, que es
    #     exactamente lo que hizo el detector nuevo de ayer (`LM.72`).
    SOLO_FIN = [{"corrida": "cZ", "id": "t1", "padre": None, "profundidad": 0,
                 "evento": "exp1_fin", "tramo": "exp"}]
    check("45. un `_fin` huérfano NO se denuncia (decisión, no descuido)",
          auditar_arbol(SOLO_FIN) == [], auditar_arbol(SOLO_FIN))

    # 46) 🎲 Vigilancia sobre los registros PAGADOS, igual que la 41. Hoy sale
    #     limpio —99 `worker_inicio` y 99 `worker_fin`, contados— y si un día
    #     una corrida real deja un tramo abierto, esta se pone roja.
    abiertos_reales = [q for q in auditar_arbol(reales)
                       if q["tipo"] == "nodo_abierto"]
    check("46. sobre los registros REALES tampoco muerde (99 pares completos)",
          abiertos_reales == [],
          f"{len(abiertos_reales)} caso(s): {abiertos_reales}")

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
    if "--paso5" in argv:
        paso5()
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
