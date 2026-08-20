"""aislamiento.py — A.4 del nivel 8: por qué cada worker tiene su propia conversación.

    LA PREGUNTA

En A, las tres monedas viven en UNA conversación. En B, cada worker tiene la
suya y empieza en blanco. ¿Por qué? La respuesta habitual es «para ahorrar
tokens», y **es falsa** — los números de la sesión 91 dicen lo contrario:

    A (una conversación):   ~17.850 tokens de entrada, 4 vueltas
    B (tres aisladas):      ~20.540 tokens de entrada, 11 llamadas

🚨 **El aislamiento salió MÁS CARO.** Así que si la razón fuera el ahorro, la
   respuesta correcta a A.4 sería «no lo hagas». No es el ahorro.


    LO QUE SÍ ES, Y SE VE EN LA FORMA, NO EN EL TOTAL

Mira cómo crece la entrada, vuelta a vuelta, en las corridas de verdad:

    A       : 3.696 → 4.242 → 4.765 → 5.171     (+1.475 en cuatro vueltas)
    worker  : 1.828 → 1.994 → 2.171             (+343 en tres, y se acabó)

⭐ Cada vuelta de una conversación RELEE todo lo anterior. Así que el coste de
   una conversación no crece con lo que dices: crece con lo que YA se dijo.
   Es cuadrático, no lineal.

   - En A, «lo ya dicho» son LAS TRES MONEDAS. Cada vuelta repaga las tres.
   - En un worker, «lo ya dicho» es SOLO SU MONEDA. Y son siempre 3 vueltas,
     haya 3 monedas o haya 30.

🔑 **El aislamiento no baja el coste: le cambia la forma.** Paga un peaje fijo
   por worker (su menú y su system prompt, otra vez) a cambio de que ninguna
   conversación crezca con el trabajo de las demás.

    LA RESPUESTA, DESPUÉS DE MEDIRLA TRES VECES (y de fallar dos)

🐛 Este archivo probó tres hipótesis y **las dos primeras eran mías y salieron
   falsas**. Se dejan escritas, con sus números, porque el camino equivocado es
   la mitad de la lección:

     ① «gana con MÁS piezas»       → falso. Con 12 monedas B es 3× peor.
     ② «gana con piezas MÁS GORDAS» → falso. Con documentos de 2.000 tokens,
                                       B solo gana en el caso más chico.
     ③ «gana con MÁS VUELTAS POR PIEZA» → **sí.** Con 8 pasos por pieza,
                                       A = 140.796 y B = 69.544. La mitad.

⭐ EL MECANISMO, Y ES UNA MULTIPLICACIÓN:

       lo que cuesta una conversación ≈ (lo que hay dentro) × (cuántas vueltas)

   Las piezas y su tamaño mueven el PRIMER factor. Solo las vueltas mueven el
   SEGUNDO — y el segundo multiplica. Por eso ① y ② no despegaban.

🚨 Y AQUÍ APARECIÓ LO QUE DE VERDAD SALVA A LA CONVERSACIÓN ÚNICA: EL LOTE.
   En ① el modelo pide las tres `tasa` en UN turno, así que tres monedas caben
   en cuatro vueltas. En ③ los pasos van encadenados y no se pueden pedir
   juntos: tres piezas de 8 pasos son 25 vueltas, y cada una relee las otras
   dos piezas enteras.
   → **Lo que hace explotar una conversación compartida no es el trabajo: es la
     DEPENDENCIA entre pasos**, que es justo lo que impide agruparlos.
   📌 Y es el desmentido de la sesión 90 visto desde el otro lado: aquel día se
      descubrió que «A ya paraleliza». Esto explica por qué eso le bastaba.

📌 CONSECUENCIA PARA EL DUELO, dicha antes de abrir el sobre: la tarea de
   divisas es **el terreno más hostil posible para B**. Pasos independientes y
   agrupables, dos por moneda. No se cambia — cambiarla ahora sería amañarla.


    LO QUE HACE ESTE ARCHIVO

  PARTE 1 (GRATIS, y es la que contesta A.4)
      Simula la misma tarea con 3, 6 y 12 monedas, en los dos esquemas, y
      cuenta los tokens con `count_tokens`, QUE NO SE COBRA. No llama al
      modelo para generar: arma las conversaciones a mano, con salidas de
      herramienta reales, y las pesa.

  PARTE 2 (CUESTA ~$0,015 — hay que pedirla con `--contaminacion`)
      La otra mitad de A.4, que no es de dinero: qué pasa cuando un worker SÍ
      ve la conversación de otro. Se le mete al worker del EUR la conversación
      del USD ya hecha, y se mira qué hace.
      📌 Se mide en vez de nombrarse. Nombrar un mecanismo no es haberlo medido.

    CÓMO SE CORRE

    python aislamiento.py                  # solo la parte 1: gratis
    python aislamiento.py --contaminacion  # las dos: cuesta ~$0,015
"""

import json
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "05b-proyecto"))

import agente          # noqa: E402
import worker          # noqa: E402
import orquestador     # noqa: E402


# ---------------------------------------------------------------------------
# DATOS DE UTILERÍA — salidas de herramienta REALES, copiadas del registro
# ---------------------------------------------------------------------------
# ⚠️ Se usan salidas de verdad y no texto inventado: si fueran más cortas de lo
#    real, la simulación diría que las conversaciones pesan menos de lo que
#    pesan, y la curva saldría movida a favor de lo que queramos demostrar.
#    Una simulación con datos amables no mide: adorna.
MONEDAS = ["USD", "EUR", "CAD", "GBP", "JPY", "CHF",
           "AUD", "MXN", "BRL", "SEK", "NOK", "NZD"]


# `relleno` simula una herramienta que devuelve MUCHO: un documento, un
# expediente, una página web. No es un truco para inflar: es el caso normal en
# cuanto sales de una API de divisas, donde un `tool_result` son 150 tokens.
# La misma cantidad se le da a los dos esquemas, que es lo que hace justa la
# comparación.
PALABRA = "conforme al documento adjunto y a la resolución vigente, "


def salida_tasa(moneda, relleno=0):
    salida = {"de": moneda, "a": "COP", "tasa": 3099.309008,
              "usd_por_1_cop": 0.0003226526,
              "fuente": "mercado (open.er-api.com)",
              "actualizado": "Thu, 20 Aug 2026 00:02:31 +0000"}
    if relleno:
        salida["contexto"] = PALABRA * relleno
    return salida


def salida_convertir(moneda):
    return {"monto": 1000, "de": moneda, "a": "COP",
            "tasa": 3099.309008, "resultado": 3099309}


def bloque_uso(id_, nombre, entrada):
    return {"type": "tool_use", "id": id_, "name": nombre, "input": entrada}


def bloque_resultado(id_, salida):
    return {"type": "tool_result", "tool_use_id": id_,
            "content": json.dumps(salida, ensure_ascii=False)}


def pesar(sistema, tools, mensajes):
    """Cuánto pesa UNA llamada a la API. GRATIS: `count_tokens` no se cobra.

    ⭐ Y es el único contador que vale. La regla de "4 caracteres por token" ya
       se cayó en el 5b: estimó 1.557 donde había 3.049.

    ⚠️ GRATIS NO ES ILIMITADO. Este archivo hace cientos de conteos seguidos y
       la primera versión murió con un 429 a mitad de la segunda tabla — una
       tabla impresa a medias, que es peor que ninguna. El freno 2 del nivel 4
       aplica igual aunque no haya factura: **el límite de un servicio gratis
       es de ritmo, no de dinero.**
    """
    for intento in range(1, 6):
        try:
            return agente.cliente.messages.count_tokens(
                model=agente.MODELO, system=sistema, tools=tools, messages=mensajes
            ).input_tokens
        except agente.REINTENTABLES:
            if intento == 5:
                raise
            time.sleep(2.0 * intento)


# ---------------------------------------------------------------------------
# PARTE 1 — LA CURVA
# ---------------------------------------------------------------------------

def costo_una_capa(n, relleno=0):
    """El esquema de A: UNA conversación con las n monedas dentro.

    Se reproduce la forma real que midió la sesión 90: el modelo pide todas las
    `tasa` en un turno y todas las `convertir` en el siguiente. Cuatro vueltas,
    haya 3 monedas o haya 30 — lo que cambia no es cuántas vueltas, sino cuánto
    pesa cada una.
    """
    monedas = MONEDAS[:n]
    tarea = ("Tengo 1.000 de cada una de estas monedas: "
             + ", ".join(monedas)
             + ". Dime cuánto es cada una en pesos hoy, con la fuente y la "
               "fecha de cada cifra, y guárdame el reporte.")

    mensajes = [{"role": "user", "content": tarea}]
    total = 0
    por_vuelta = []

    # -- vuelta 1: pide las n tasas
    total += (t := pesar(agente.SISTEMA, agente.TOOLS, mensajes)); por_vuelta.append(t)
    mensajes.append({"role": "assistant", "content": [
        bloque_uso(f"t{i}", "tasa", {"de": m, "a": "COP"})
        for i, m in enumerate(monedas)]})
    mensajes.append({"role": "user", "content": [
        bloque_resultado(f"t{i}", salida_tasa(m, relleno))
        for i, m in enumerate(monedas)]})

    # -- vuelta 2: pide las n conversiones
    total += (t := pesar(agente.SISTEMA, agente.TOOLS, mensajes)); por_vuelta.append(t)
    mensajes.append({"role": "assistant", "content": [
        bloque_uso(f"c{i}", "convertir",
                   {"monto": 1000, "de": m, "a": "COP", "tasa": 3099.309008})
        for i, m in enumerate(monedas)]})
    mensajes.append({"role": "user", "content": [
        bloque_resultado(f"c{i}", salida_convertir(m))
        for i, m in enumerate(monedas)]})

    # -- vuelta 3: guarda el reporte
    total += (t := pesar(agente.SISTEMA, agente.TOOLS, mensajes)); por_vuelta.append(t)
    mensajes.append({"role": "assistant", "content": [
        bloque_uso("g0", "guardar_reporte",
                   {"nombre": "reporte.txt", "contenido": "…"})]})
    mensajes.append({"role": "user", "content": [
        bloque_resultado("g0", {"guardado": "reporte.txt", "bytes": 400})]})

    # -- vuelta 4: responde
    total += (t := pesar(agente.SISTEMA, agente.TOOLS, mensajes)); por_vuelta.append(t)
    return total, por_vuelta


def costo_dos_capas(n, relleno=0):
    """El esquema de B: un orquestador + n workers, cada uno en su conversación.

    Cada worker se pesa por separado y empieza EN BLANCO. Ahí está la pieza: su
    conversación no sabe nada de las otras monedas, así que no las repaga.
    """
    monedas = MONEDAS[:n]
    menu_w = worker.menu_para(worker.HERRAMIENTAS_DIVISA)
    total = 0

    # --- la capa de abajo: n conversaciones cortas e IDÉNTICAS entre sí
    for m in monedas:
        msgs = [{"role": "user",
                 "content": f"Convierte 1000 {m} a pesos colombianos."}]
        total += pesar(worker.SISTEMA_DIVISA, menu_w, msgs)
        msgs.append({"role": "assistant", "content": [
            bloque_uso("t0", "tasa", {"de": m, "a": "COP"})]})
        msgs.append({"role": "user", "content": [
            bloque_resultado("t0", salida_tasa(m, relleno))]})

        total += pesar(worker.SISTEMA_DIVISA, menu_w, msgs)
        msgs.append({"role": "assistant", "content": [
            bloque_uso("c0", "convertir",
                       {"monto": 1000, "de": m, "a": "COP", "tasa": 3099.309008})]})
        msgs.append({"role": "user", "content": [
            bloque_resultado("c0", salida_convertir(m))]})

        total += pesar(worker.SISTEMA_DIVISA, menu_w, msgs)

    # --- la capa de arriba: 2 vueltas, y su menú tiene UNA herramienta
    tarea = ("Tengo 1.000 de cada una de estas monedas: " + ", ".join(monedas)
             + ". Dime cuánto es cada una en pesos hoy, con la fuente y la fecha.")
    msgs = [{"role": "user", "content": tarea}]
    total += pesar(orquestador.SISTEMA_ORQ, orquestador.TOOLS_ORQ, msgs)
    msgs.append({"role": "assistant", "content": [
        bloque_uso(f"w{i}", "consultar_moneda", {"monto": 1000, "moneda": m})
        for i, m in enumerate(monedas)]})
    msgs.append({"role": "user", "content": [
        bloque_resultado(f"w{i}", {"moneda": m, "monto": 1000, "pesos": 3099309,
                                   "tasa": 3099.309008,
                                   "fuente": "mercado (open.er-api.com)",
                                   "fecha": "Thu, 20 Aug 2026 00:02:31 +0000"})
        for i, m in enumerate(monedas)]})
    total += pesar(orquestador.SISTEMA_ORQ, orquestador.TOOLS_ORQ, msgs)

    return total


# ---------------------------------------------------------------------------
# LA TERCERA CURVA — y llegó porque las dos primeras midieron mal
# ---------------------------------------------------------------------------
# 🐛 LO QUE PASÓ, Y SE DEJA ESCRITO ENTERO:
#    La tabla ① midió "más piezas" y B empeoró. Supuse entonces que la palanca
#    era el TAMAÑO de cada pieza y monté la tabla ②... donde B tampoco despegó.
#    Dos hipótesis mías, dos desmentidos, y ninguno de los dos era el mecanismo.
#
# ⭐ EL MECANISMO ES ESTE, Y SE VE EN LA MULTIPLICACIÓN:
#       lo que cuesta una conversación ≈ (lo que hay dentro) × (cuántas vueltas)
#    Las vueltas son el factor que MULTIPLICA. Añadir piezas o engordarlas mueve
#    el primer factor; solo repartir el trabajo en más vueltas mueve el segundo.
#    → La palanca del aislamiento no es cuántas piezas hay ni cuánto pesan: es
#      CUÁNTAS VUELTAS NECESITA CADA PIEZA.
#
#    En divisas cada moneda son 2 llamadas. Por eso B no gana: no hay nada que
#    aislar. Una pieza que necesita ocho vueltas dentro de una conversación
#    compartida obliga a releer las otras siete piezas OCHO VECES.

def costo_una_capa_k(n, k):
    """n piezas, cada una necesita k llamadas EN CADENA, todo en una conversación."""
    tarea = f"Resuelve estas {n} cosas, cada una necesita varios pasos."
    mensajes = [{"role": "user", "content": tarea}]
    total = 0
    for pieza in range(n):
        for paso in range(k):
            total += pesar(agente.SISTEMA, agente.TOOLS, mensajes)
            id_ = f"p{pieza}s{paso}"
            mensajes.append({"role": "assistant", "content": [
                bloque_uso(id_, "tasa", {"de": MONEDAS[pieza], "a": "COP"})]})
            mensajes.append({"role": "user", "content": [
                bloque_resultado(id_, salida_tasa(MONEDAS[pieza]))]})
    total += pesar(agente.SISTEMA, agente.TOOLS, mensajes)   # la respuesta final
    return total


def costo_dos_capas_k(n, k):
    """Lo mismo, pero cada pieza en su propia conversación."""
    menu_w = worker.menu_para(worker.HERRAMIENTAS_DIVISA)
    total = 0
    for pieza in range(n):
        msgs = [{"role": "user", "content": f"Resuelve la pieza {MONEDAS[pieza]}."}]
        for paso in range(k):
            total += pesar(worker.SISTEMA_DIVISA, menu_w, msgs)
            id_ = f"s{paso}"
            msgs.append({"role": "assistant", "content": [
                bloque_uso(id_, "tasa", {"de": MONEDAS[pieza], "a": "COP"})]})
            msgs.append({"role": "user", "content": [
                bloque_resultado(id_, salida_tasa(MONEDAS[pieza]))]})
        total += pesar(worker.SISTEMA_DIVISA, menu_w, msgs)

    msgs = [{"role": "user", "content": f"Resuelve estas {n} cosas."}]
    total += pesar(orquestador.SISTEMA_ORQ, orquestador.TOOLS_ORQ, msgs)
    msgs.append({"role": "assistant", "content": [
        bloque_uso(f"w{i}", "consultar_moneda", {"monto": 1000, "moneda": MONEDAS[i]})
        for i in range(n)]})
    msgs.append({"role": "user", "content": [
        bloque_resultado(f"w{i}", {"moneda": MONEDAS[i], "monto": 1000,
                                   "pesos": 3099309, "tasa": 3099.309008,
                                   "fuente": "mercado (open.er-api.com)",
                                   "fecha": "Thu, 20 Aug 2026 00:02:31 +0000"})
        for i in range(n)]})
    total += pesar(orquestador.SISTEMA_ORQ, orquestador.TOOLS_ORQ, msgs)
    return total


def parte_1():
    print("=" * 74)
    print("A.4 · PARTE 1 — LA CURVA.  GRATIS: count_tokens no se cobra.")
    print("=" * 74)

    # La forma, con 3 monedas: dónde crece cada esquema.
    _, por_vuelta = costo_una_capa(3)
    print("\nCómo crece UNA conversación (esquema A, 3 monedas), vuelta a vuelta:")
    print("   " + " → ".join(str(t) for t in por_vuelta))
    print("   ⭐ Cada vuelta repaga TODAS las monedas. Por eso sube.")

    def tabla(titulo, relleno, ns):
        print("\n" + "-" * 74)
        print(titulo)
        print("-" * 74)
        print(f"{'piezas':>7} │ {'A: una capa':>12} │ {'B: dos capas':>13} │ "
              f"{'B − A':>10} │ veredicto")
        print("-" * 74)
        for n in ns:
            a, _ = costo_una_capa(n, relleno)
            b = costo_dos_capas(n, relleno)
            signo = "+" if b >= a else "−"
            veredicto = "A más barato" if b > a else "B MÁS BARATO"
            print(f"{n:>7} │ {a:>12,} │ {b:>13,} │ {signo}{abs(b - a):>9,} │ {veredicto}")
        print("-" * 74)

    tabla("① MÁS PIEZAS — cada herramienta devuelve ~150 tokens "
          "(el caso de divisas)", 0, (3, 6, 12))
    tabla("② PIEZAS MÁS GORDAS — cada herramienta devuelve ~2.000 tokens "
          "(un documento)", 130, (3, 6))

    # --- ③ la que sí encontró la palanca
    print("\n" + "-" * 74)
    print("③ MÁS VUELTAS POR PIEZA — 3 piezas fijas, cambiando cuántos pasos")
    print("   necesita cada una. AQUÍ está la palanca.")
    print("-" * 74)
    print(f"{'vueltas/pieza':>13} │ {'A: una capa':>12} │ {'B: dos capas':>13} │ "
          f"{'B − A':>10} │ veredicto")
    print("-" * 74)
    for k in (2, 4, 8):
        a = costo_una_capa_k(3, k)
        b = costo_dos_capas_k(3, k)
        signo = "+" if b >= a else "−"
        veredicto = "A más barato" if b > a else "B MÁS BARATO"
        print(f"{k:>13} │ {a:>12,} │ {b:>13,} │ {signo}{abs(b - a):>9,} │ {veredicto}")
    print("-" * 74)
    print("""
🔑 LA RESPUESTA A A.4, Y NO ES «PARA AHORRAR TOKENS»:

   lo que cuesta una conversación ≈ (lo que hay dentro) × (cuántas vueltas)

   Las tablas ① y ② mueven el primer factor y B no despega. La ③ mueve el
   segundo, que es el que MULTIPLICA, y B pasa a costar la mitad.

   → El aislamiento no se pone porque haya muchas piezas ni porque sean
     grandes. Se pone cuando CADA PIEZA NECESITA MUCHAS VUELTAS SUYAS, porque
     en una conversación compartida cada una de esas vueltas relee el trabajo
     de todas las demás.

🚨 Y lo que salva a la conversación única es EL LOTE: en ① el modelo pide las
   tres `tasa` en un solo turno. Cuando los pasos DEPENDEN unos de otros no se
   pueden agrupar, y ahí es donde explota.
   → Lo caro no es el trabajo: es la dependencia entre pasos.

⚠️  CONSECUENCIA PARA EL DUELO, dicha antes de abrir el sobre: divisas es el
    terreno MÁS HOSTIL POSIBLE para B — pasos independientes y agrupables, dos
    por moneda. No se cambia la tarea: cambiarla ahora sería amañarla.
""")


# ---------------------------------------------------------------------------
# PARTE 2 — LA CONTAMINACIÓN  (esta sí cuesta)
# ---------------------------------------------------------------------------
# ⭐ Y ES LA MITAD QUE NO ES DE DINERO. Aunque el aislamiento saliera más caro
#    SIEMPRE, seguiría habiendo una razón para tenerlo: una conversación
#    compartida hace que lo que un worker vio pueda usarlo otro.
#    Con divisas suena inocente. Con un worker que leyó el expediente de OTRO
#    cliente, no.

def parte_2():
    print("\n" + "=" * 74)
    print("A.4 · PARTE 2 — CONTAMINACIÓN.  Esto SÍ cuesta (~$0,015).")
    print("=" * 74)

    # La conversación del USD, ya hecha, tal como la vivió el worker del dólar.
    previo = [
        {"role": "user", "content": "Convierte 1000 USD a pesos colombianos."},
        {"role": "assistant", "content": [
            bloque_uso("t0", "tasa", {"de": "USD", "a": "COP"})]},
        {"role": "user", "content": [bloque_resultado("t0", salida_tasa("USD"))]},
        {"role": "assistant", "content": [
            bloque_uso("c0", "convertir", {"monto": 1000, "de": "USD",
                                           "a": "COP", "tasa": 3099.309008})]},
        {"role": "user", "content": [bloque_resultado("c0", salida_convertir("USD"))]},
        {"role": "assistant", "content":
            "1000 USD equivale a 3.099.309 pesos colombianos según la tasa de "
            "mercado (open.er-api.com) del 20 de agosto de 2026."},
    ]

    print("\n① LIMPIO — el worker del EUR empieza en blanco (lo que hace B hoy):")
    limpio = worker.correr_worker("Convierte 1000 EUR a pesos colombianos.",
                                  nombre="eur_limpio")

    print("\n② CONTAMINADO — el MISMO encargo, pero con la conversación del USD"
          "\n   ya dentro (lo que pasaría con una conversación compartida):")
    sucio = worker.correr_worker("Convierte 1000 EUR a pesos colombianos.",
                                 nombre="eur_contaminado",
                                 historial_previo=previo)

    print("\n" + "-" * 74)
    print("QUÉ CAMBIÓ")
    print("-" * 74)
    for etiqueta, r in (("limpio     ", limpio), ("contaminado", sucio)):
        d = r["datos"] or {}
        print(f"  {etiqueta}: {r['llamadas_api']} llamadas · "
              f"{r['entrada_tokens']:>5} entrada · ${r['coste_usd']:.6f} · "
              f"herramientas: {', '.join(r['herramientas']) or 'NINGUNA'}")
        print(f"               tasa usada: {d.get('tasa')}  →  pesos: {d.get('pesos')}")

    print(f"""
📌 QUÉ MIRAR, y es una sola cosa: LA TASA.
   La del USD era 3099.309008. Si el worker contaminado la reutilizó para el
   euro —o si ni siquiera llamó a `tasa`— la conversación compartida le pasó
   un dato ajeno y él lo tomó por suyo.
   Si llamó a `tasa` igual, entonces aquí no se contaminó: eso también es un
   dato, y se anota tal cual. Una alarma que no suena es un resultado.
""")


if __name__ == "__main__":
    parte_1()
    if "--contaminacion" in sys.argv:
        parte_2()
    else:
        print("💡 La parte 2 (contaminación) cuesta ~$0,015 y no corrió.")
        print("   Para correrla:  python aislamiento.py --contaminacion")
