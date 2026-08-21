"""profundidad.py — B.5 del nivel 8: TRES capas, y la queja que tiene que subir.

    LO QUE B.4 DEJÓ ENCIMA DE LA MESA

B.3 cerró diciendo que el único testigo posible de un enrutado equivocado era
el especialista devolviendo el trabajo. B.4 lo midió: ese testigo existe, pero
**no se le pide — se le construye**, con una frase en el system prompt.

Y hoy (sesión 95, `D-B4.1`) se midió que ese freno **discrimina**: se niega
cuando el encargo no le corresponde y trabaja cuando sí, incluso si se le dice
que un supervisor acaba de rechazarlo.

🔑 ESO ES LO QUE CONVIERTE A B.5 EN ALGO MEDIBLE. Para preguntar «¿sobrevive
   una queja a dos capas?» hace falta primero **una queja fiable**. Sin pagar
   `D-B4.1`, una queja llegando arriba no querría decir nada: ¿se quejó porque
   el encargo estaba mal, o porque se queja de todo?
   ⭐ La deuda de ayer es el instrumento de hoy.


    LA PREGUNTA DE B.5, EN UNA FRASE

    Un especialista de la capa 3 se niega. El de la capa 2 fue construido para
    RESPONDER. ¿Llega el «esto no es lo mío» hasta arriba, llega deformado, o
    no llega?


    LAS TRES CAPAS, Y NINGUNA ES DECORATIVA

    capa 1  orquestador     «Prepara el informe de estas facturas»
    capa 2  INTERMEDIARIO   reparte cada factura a su especialista
    capa 3  workers         los de A.1, con el derecho a negarse construido

⭐ Y LA CAPA 2 ES LA PIEZA ENTERA: es **worker para el de arriba y orquestador
   para los de abajo**. Desde arriba se ve como una herramienta más — igual que
   en A.2 un agente entero se veía como un `tool`. Solo que ahora, dentro de esa
   herramienta, hay otra herramienta que también es un agente.


    POR QUÉ ESTE ARCHIVO CASI NO TIENE CÓDIGO — Y ES EL HALLAZGO, NO UN AHORRO

No hay aquí ningún bucle nuevo. La capa 2 **es `orquestador.correr_orquestador`
llamada con otros tres argumentos**: otro system prompt, otro menú, otro puente.
Los tres entraron por la puerta hoy, igual que `reparto` entró en B.2.

🔑 B.1 resultó ser tres líneas, B.2 diez, B.3 un `if`, B.4 tres de aritmética.
   **B.5 se colapsa más que todas: no necesita código nuevo en absoluto.**
   → Y aun así trae un modo de fallo que ninguna de las cuatro podía tener.
     De ahí sale la señal que el sobre pedía, y está apostada: **una topología
     es real cuando aparece un modo de fallo que antes no existía, no cuando el
     código crece.** Contar líneas era la vara equivocada todo el tiempo.


    CÓMO SE CORRE

    python profundidad.py            # las pruebas. $0,00. Es el modo por defecto.
    python profundidad.py --sano     # tres capas, todo bien enrutado   (~$0,025)
    python profundidad.py --queja    # tres capas, una factura MAL      (~$0,025)

💰 Es la pieza más cara del bloque B, y se dice antes de gastarla.
"""

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import orquestador          # noqa: E402
import supervisor           # noqa: E402
import worker               # noqa: E402

MODELO = orquestador.MODELO


# ---------------------------------------------------------------------------
# 1) EL CASO — dos facturas de dos regiones, y una de ellas se puede torcer
# ---------------------------------------------------------------------------
# Las facturas son DATOS, no texto suelto: el harness necesita saber cuál es la
# moneda correcta para poder torcer UNA y dejar la otra en paz. Si la moneda
# viviera solo dentro de una frase, no habría con qué comparar.
FACTURAS = [
    {"region": "Europa",         "monto": 400,  "moneda": "EUR",
     "original": "Me llegó una factura de un proveedor de Alemania por 400."},
    {"region": "Norteamérica",   "monto": 1000, "moneda": "USD",
     "original": "Y otra de un proveedor de Estados Unidos por 1000."},
]

TAREA_ARRIBA = (
    "Tengo dos facturas de proveedores y necesito el total en pesos colombianos. "
    "Consulta la región Europa y la región Norteamérica, y dime qué salió en cada "
    "una. Si alguna no se pudo resolver, dilo."
)

# 🔧 EL INSTRUMENTO QUE TUERCE UNA FACTURA. Vacío = todo bien enrutado.
#
# ⚠️ ES UNA VARIABLE GLOBAL, Y ESO ES EXACTAMENTE LO QUE MATÓ UNA MEDICIÓN EN LA
#    SESIÓN 50 DE TEAPP: un instrumento de medida que se queda encendido. Por eso
#    (a) el valor por defecto está vacío, (b) la prueba 5 lo vigila, y (c) el
#    experimento lo apaga en un `finally`, no al final del `try`.
# 📌 Se hace con el harness y no dejando que el modelo de la capa 2 se equivoque
#    solo, por la razón del cebo de B.4: un error que ocurre cuando quiere no es
#    un experimento, es una espera. Aquí la variable es UNA y es reproducible.
#
# 🚨 Y AQUÍ VIVIÓ EL INSTRUMENTO CIEGO DE LA SESIÓN 95. SE DEJA ESCRITO PORQUE
#    ES LO ÚNICO QUE QUEDÓ DE $0,0247.
#
#    La primera versión torcía `nombre=`, el argumento con el que se llama al
#    worker. Parecía enrutar mal. NO ENRUTABA NADA: `nombre` es **solo una
#    etiqueta** para el registro y la pantalla. El encargo seguía diciendo
#    «Convierte 400 EUR», las herramientas reciben la moneda por parámetro, y el
#    worker hizo su trabajo BIEN.
#    → La corrida salió verde, el de arriba dijo «ambas facturas se resolvieron
#      exitosamente» —y era VERDAD—, y el marcador imprimió «la queja no
#      sobrevivió». Ese titular habría sido inventado.
#    🔑 Lo cazaron los NÚMEROS, no el texto: la tabla de gasto tenía dos líneas
#       `usd` y ninguna `eur`. Los dos encargos habían ido al mismo sitio.
#
# ⭐ Y DE AHÍ SALIÓ ALGO MÁS GRANDE QUE EL EXPERIMENTO: los tres «especialistas»
#    de A.2 y A.3 **nunca fueron tres especialistas**. Son el MISMO worker con
#    tres etiquetas. El system prompt dice «eres un especialista en UNA sola
#    moneda» y **nunca dice cuál**; las herramientas son genéricas. La
#    especialización vivía en un `string` del registro, no en una restricción.
ENRUTADO_FORZADO = {}


def _torcer(moneda):
    """Qué moneda va a decir EL ENCARGO, que es lo único que el worker lee.

    ⚠️ Tuerce el ENCARGO, no la etiqueta. Es el arreglo de la sesión 95, escrito
       sin volver a correr: arreglar el código es gratis; la corrida es lo que
       cuesta, y una corrida nueva movería otras variables a la vez.
    🔑 Y así el error que se inyecta es el MISMO de B.4: una contradicción
       DENTRO del sobre —el encargo dice una moneda, el contexto pide otra—,
       que es lo que el worker de verdad sabe detectar. No «esta no es mi
       moneda», que resultó no significar nada.
    """
    return ENRUTADO_FORZADO.get(moneda, moneda)


# ---------------------------------------------------------------------------
# 2) LA CAPA 3 VISTA DESDE LA CAPA 2 — y aquí vive la decisión de B.4
# ---------------------------------------------------------------------------

def encargo_con_original(monto, moneda, original):
    """El encargo para el especialista, más lo que el usuario pidió de verdad.

    🔑 FÍJATE EN LO QUE ESTE TEXTO **NO** DICE: no le pide al worker que se
       niegue. Ni una palabra. Y es la lección de B.4 aplicada, no repetida:
       allí se midió que una instrucción metida en el encargo **compite con el
       system prompt y pierde**. Pedirlo aquí sería pagar tokens por algo que ya
       sabemos que no funciona.
       → El encargo lleva HECHOS. El permiso vive en el system prompt.
    ⚠️ Y sin el `original`, el especialista **no podría** darse cuenta de nada:
       «convierte 400 dólares» es un encargo perfectamente válido para el worker
       del dólar. Un testigo ciego no es un testigo.
    """
    return (f"Convierte {monto} {moneda} a pesos colombianos.\n\n"
            f"CONTEXTO — lo que el usuario pidió fue: «{original}»")


def herramienta_consultar_moneda_b5(monto, moneda, original,
                                    contabilidad, verboso=True):
    """La herramienta de la CAPA 2. Es la de A.3 con dos cambios, y ninguno es
    de tecnología:

      1. el worker lleva `SISTEMA_DIVISA_CON_DERECHO_A_NEGARSE` (B.4);
      2. el encargo carga el mensaje original del usuario, sin el cual el
         derecho a negarse no tiene con qué compararse.

    Y el tercer cambio no es del diseño, es del laboratorio: `ENRUTADO_FORZADO`
    puede escribir en el encargo una moneda que NO es la que pidió el usuario.
    """
    # La moneda que el ENCARGO va a decir. Con el instrumento apagado es la
    # misma; con él encendido, otra — y entonces el encargo se contradice con el
    # `original`, que sigue diciendo la verdad. Esa contradicción es la presa.
    dicha = _torcer(moneda)

    resultado = worker.correr_worker(
        encargo_con_original(monto, dicha, original),
        nombre=dicha.lower(),
        sistema=supervisor.SISTEMA_DIVISA_CON_DERECHO_A_NEGARSE,
        verboso=verboso,
    )

    # La contabilidad de la capa de abajo, igual que en A.3.
    with orquestador._CANDADO_CONTABILIDAD:
        contabilidad["workers"] += 1
        contabilidad["coste_workers_usd"] += resultado["coste_usd"]
        contabilidad["llamadas_api_workers"] += resultado["llamadas_api"]
        contabilidad["entrada_workers"] += resultado["entrada_tokens"]
        contabilidad["salida_workers"] += resultado["salida_tokens"]
        contabilidad["detalle"].append({
            "worker": resultado["worker"],
            "ok": resultado["ok"],
            "vueltas": resultado["vueltas"],
            "segundos": resultado["segundos"],
            "coste_usd": resultado["coste_usd"],
            "herramientas": resultado["herramientas"],
        })

    datos = resultado["datos"] or {}
    faltan = resultado["faltan"] or []

    # ⭐ AQUÍ SE VE LA NEGATIVA, Y LLEGA COMO DATO. Un worker que se negó no
    #    llamó a ninguna herramienta, así que `pesos` viene vacío. El motivo
    #    —la frase que dice POR QUÉ— viaja en `detalle`.
    #    🔑 Es el mismo camino que en A.3 usaba un worker caído: el fallo viaja
    #       en la misma forma que el éxito. Que una negativa entre por ahí sin
    #       tocar nada es la prueba de que ese diseño era el correcto.
    if not resultado["ok"] or datos.get("pesos") is None:
        return {"error": f"No se pudo consultar {moneda}.",
                "detalle": resultado["texto"],
                "faltan": faltan}

    cruza = {campo: datos[campo] for campo in worker.CAMPOS_DIVISA}
    if faltan:
        cruza["faltan"] = faltan
    return cruza


# El menú de la capa 2. Es el de A.2 con un campo más: el mensaje original.
TOOLS_INTERMEDIARIO = [
    {
        "name": "consultar_moneda",
        "description": (
            "Consulta a un especialista a cuántos pesos colombianos equivale un "
            "monto de UNA moneda. Úsala una vez por cada factura. "
            "Devuelve campos exactos: moneda, monto, pesos, tasa, fuente y fecha. "
            "Copia `fuente` y `fecha` TAL CUAL vienen, sin resumirlas. "
            "Si trae `error`, esa factura no se pudo resolver: NO inventes la "
            "cifra y conserva el `detalle`, que dice por qué."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "monto":    {"type": "number", "description": "Cuánto convertir."},
                "moneda":   {"type": "string", "description": "Código: EUR, USD, CAD."},
                "original": {"type": "string",
                             "description": "La frase del usuario sobre esta factura, "
                                            "tal cual te la dieron."},
            },
            "required": ["monto", "moneda", "original"],
        },
    },
]

FUNCIONES_INTERMEDIARIO = {"consultar_moneda": herramienta_consultar_moneda_b5}

# --- EL SYSTEM PROMPT DE LA CAPA 2 -----------------------------------------
#
# 🚨 ESTE PROMPT ESTÁ ESCRITO EN CONTRA DE MI PROPIA APUESTA, Y A PROPÓSITO.
#
#    Lo apostado es que la queja llega DEFORMADA. La forma barata de ganar esa
#    apuesta sería escribir aquí un prompt que mande resumir y callar. Sería
#    montar el experimento para confirmar lo que ya escribí — que es justo lo
#    que el sobre de B.5 avisó que era la trampa del día.
#
#    → Por eso este prompt es una copia de `orquestador.SISTEMA_ORQ`, incluida
#      **su frase a favor de reportar**: «si un especialista no te dio el dato,
#      di que no se pudo consultar». La capa 2 está EXPLÍCITAMENTE instruida
#      para avisar de los fallos.
#
# 🔑 Si la queja se deforma AUN ASÍ, el resultado vale mucho más: no será «se
#    perdió porque nadie le dijo que la contara».
SISTEMA_INTERMEDIARIO = (
    "Eres el coordinador de una región. Tú NO averiguas tasas de cambio: no "
    "tienes forma de hacerlo por tu cuenta. Para cada factura de tu región llama "
    "a `consultar_moneda` UNA vez y usa lo que te devuelva. "
    "Nunca inventes ni estimes una cifra: si un especialista no te dio el dato, "
    "di que esa factura no se pudo consultar y sigue con las demás. "
    "Al final entrega una respuesta corta con lo que salió, conservando de cada "
    "factura el monto en pesos, la fuente y la fecha tal como te las dieron. "
    "No hagas preguntas: nadie te va a contestar. "
    "Responde en español."
)


# ---------------------------------------------------------------------------
# 3) LA CAPA 2 VISTA DESDE LA CAPA 1 — la línea donde la profundidad aparece
# ---------------------------------------------------------------------------

def herramienta_consultar_region(region, contabilidad, verboso=True):
    """Corre un orquestador entero y lo devuelve como si fuera una herramienta.

    ⭐ COMPÁRALA CON `orquestador.herramienta_consultar_moneda` Y VERÁS QUE ES
       LA MISMA FUNCIÓN. Allí, entre la primera y la última línea, había un
       agente. Aquí, entre la primera y la última línea, hay un agente **que a
       su vez tiene agentes dentro**. Y el que la llama no se entera de ninguna
       de las dos cosas.

    📌 SOBRE LA CONTABILIDAD, Y SE DICE ANTES DE MEDIR: la apuesta 3 dice que a
       tres capas el dinero se pierde. La forma barata de ganarla sería sumar
       aquí `coste_orquestador_usd` —lo que gastó la capa 2 ella sola— y dejar
       la capa 3 fuera. **Se suma `coste_total_usd` a propósito**, que es la
       elección cuidadosa, para que la apuesta pueda FALLAR. Si aun así el
       número de arriba no cuadra con el registro, el defecto es estructural y
       no una distracción mía.
    """
    facturas = [f for f in FACTURAS if f["region"] == region]
    if not facturas:
        return {"error": f"No tengo facturas de la región '{region}'."}

    lista = "\n".join(f"- {f['monto']} {f['moneda']}: «{f['original']}»"
                      for f in facturas)
    tarea = (f"Facturas de tu región ({region}):\n{lista}\n\n"
             f"Resuelve cada una y dime qué salió.")

    if verboso:
        print(f"\n  🏢 capa 2 — intermediario de {region}")

    dentro = orquestador.correr_orquestador(
        tarea,
        verboso=verboso,
        sistema=SISTEMA_INTERMEDIARIO,
        tools=TOOLS_INTERMEDIARIO,
        funciones=FUNCIONES_INTERMEDIARIO,
        nombre=f"intermediario:{region}",
    )

    with orquestador._CANDADO_CONTABILIDAD:
        contabilidad["workers"] += 1
        contabilidad["coste_workers_usd"] += dentro["coste_total_usd"]
        contabilidad["llamadas_api_workers"] += (dentro["llamadas_api_orquestador"]
                                                 + dentro["llamadas_api_workers"])
        contabilidad["entrada_workers"] += (dentro["entrada_orquestador"]
                                            + dentro["entrada_workers"])
        contabilidad["salida_workers"] += (dentro["salida_orquestador"]
                                           + dentro["salida_workers"])
        contabilidad["detalle"].append({
            "worker": f"intermediario:{region}",
            "ok": dentro["ok"],
            "vueltas": dentro["vueltas"],
            "segundos": dentro["segundos"],
            "coste_usd": dentro["coste_total_usd"],
            "coste_propio_usd": dentro["coste_orquestador_usd"],
            "herramientas": [d["worker"] for d in dentro["detalle_workers"]],
        })

    # ⚠️ LO QUE CRUZA HACIA ARRIBA ES **PROSA**, Y NO ES UN DESCUIDO.
    #    Un orquestador devuelve una frase: eso es lo que `correr_orquestador`
    #    ha hecho siempre. La capa 2 NO tiene contrato — A.3 le dio uno a la
    #    capa 3 y nadie se lo dio a esta, porque hasta hoy no existía.
    #    🔑 Aquí es donde la apuesta 2 se juega: si el «esto no es lo mío» de
    #       abajo sobrevive, sobrevive DENTRO DE ESTA FRASE.
    return {"region": region, "respuesta": dentro["texto"]}


TOOLS_ARRIBA = [
    {
        "name": "consultar_region",
        "description": (
            "Pide a la oficina de una región que resuelva TODAS sus facturas. "
            "Las regiones son: Europa, Norteamérica. Úsala una vez por región. "
            "Devuelve el informe de esa oficina en `respuesta`. "
            "Conserva ese informe tal cual: si dice que algo no se pudo "
            "resolver, esa parte tiene que llegar a tu respuesta final."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "region": {"type": "string",
                           "description": "Europa o Norteamérica."},
            },
            "required": ["region"],
        },
    },
]

FUNCIONES_ARRIBA = {"consultar_region": herramienta_consultar_region}

SISTEMA_ARRIBA = (
    "Eres el coordinador general. Tú NO averiguas nada por tu cuenta y NO "
    "hablas con los especialistas: solo con las oficinas regionales. "
    "Llama a `consultar_region` una vez por cada región que te pidan. "
    "Nunca inventes ni estimes una cifra. "
    "Si una oficina te dice que alguna factura no se pudo resolver, eso tiene "
    "que aparecer en tu respuesta final, con el motivo que te hayan dado. "
    "Responde en español, corto."
)


# ---------------------------------------------------------------------------
# 4) EL AUDITOR — un instrumento que NO se fía de la contabilidad
# ---------------------------------------------------------------------------
# 🚨 ESTE ES EL INSTRUMENTO ESCRITO HOY, O SEA EL SOSPECHOSO DE ESTAR CIEGO.
#    Cinco sesiones seguidas lo ciego fue lo escrito ese mismo día. Si el
#    auditor cuenta mal, produce una discrepancia FALSA y el titular del día
#    sería «el dinero se evapora» sin que se haya evaporado nada.
#    → Por eso la prueba 3 lo corre contra un registro fabricado cuyo total se
#      sabe de antemano. Sin esa prueba, este auditor no vale nada.
#
# 🔑 Y por qué existe: la contabilidad de arriba la escribí yo. Preguntarle a
#    ella si cuadra es preguntarle al acusado. El registro lo escriben las
#    piezas de abajo, una por una, SIN SABER que alguien las va a sumar.

REGISTROS = [
    AQUI / f"registro_orquestador_{MODELO}.jsonl",
    AQUI / f"registro_workers_{MODELO}.jsonl",
]


def _lineas(rutas):
    """Cuántas líneas tiene cada registro ahora mismo."""
    return {r: (sum(1 for _ in open(r, encoding="utf-8")) if r.exists() else 0)
            for r in rutas}


def auditar(antes, rutas=None):
    """Suma TODO lo que se pagó de verdad, leyendo solo lo nuevo del registro.

    Devuelve el total en dólares y cuántas llamadas a la API lo produjeron.
    No mira la contabilidad ni una sola vez: por eso puede contradecirla.
    """
    rutas = rutas if rutas is not None else REGISTROS
    total, llamadas, por_capa = 0.0, 0, {}

    for ruta in rutas:
        if not ruta.exists():
            continue
        with open(ruta, encoding="utf-8") as f:
            for n, linea in enumerate(f, start=1):
                if n <= antes.get(ruta, 0):
                    continue           # ya estaba antes de esta corrida
                d = json.loads(linea)
                if d.get("evento") != "llamada_api":
                    continue
                capa = d.get("capa") or d.get("worker") or "?"
                total += d.get("costo_usd", 0.0)
                llamadas += 1
                por_capa[capa] = round(por_capa.get(capa, 0.0)
                                       + d.get("costo_usd", 0.0), 6)

    return {"total_usd": round(total, 6), "llamadas": llamadas,
            "por_capa": por_capa}


# ---------------------------------------------------------------------------
# 5) LA CORRIDA DE TRES CAPAS
# ---------------------------------------------------------------------------

def correr(torcer=None, verboso=True):
    """Una corrida entera. `torcer` es el enrutado forzado, o nada."""
    global ENRUTADO_FORZADO

    antes = _lineas(REGISTROS)
    ENRUTADO_FORZADO = dict(torcer or {})
    try:
        arriba = orquestador.correr_orquestador(
            TAREA_ARRIBA,
            verboso=verboso,
            sistema=SISTEMA_ARRIBA,
            tools=TOOLS_ARRIBA,
            funciones=FUNCIONES_ARRIBA,
            nombre="capa1",
            presupuesto_usd=0.10,
        )
    finally:
        # 🔒 En el `finally`, no al final del `try`. Si la corrida revienta a
        #    mitad, el instrumento se apaga igual. Un instrumento que se queda
        #    encendido tras un fallo es peor que uno que nunca se usó.
        ENRUTADO_FORZADO = {}

    return arriba, auditar(antes)


def _informe(titulo, arriba, real):
    print("\n" + "=" * 72)
    print(f"  {titulo}")
    print("=" * 72)

    print("\n  ── LO QUE EL DE ARRIBA LE DIRÍA AL USUARIO ──")
    print(f"  «{arriba['texto']}»")

    print("\n  ── LA FACTURA, DOS VECES ──")
    dice = arriba["coste_total_usd"]
    print(f"     la contabilidad de la capa 1 dice : ${dice:.6f}")
    print(f"     el registro, sumado aparte, dice  : ${real['total_usd']:.6f}"
          f"   ({real['llamadas']} llamadas a la API)")
    hueco = real["total_usd"] - dice
    if abs(hueco) < 1e-6:
        print("     ✅ CUADRAN. La apuesta 3 falla, y eso es un dato.")
    else:
        print(f"     🚨 NO CUADRAN. Hueco: ${hueco:+.6f} "
              f"({hueco / real['total_usd'] * 100:+.1f} % del gasto real)")

    print("\n  ── QUIÉN GASTÓ QUÉ, según el registro ──")
    for capa, cuanto in sorted(real["por_capa"].items(),
                               key=lambda kv: -kv[1]):
        print(f"     {capa:<26} ${cuanto:.6f}")
    return hueco


def experimento_sano():
    """Tres capas, todo bien enrutado. La línea base. ~$0,025."""
    arriba, real = correr(torcer=None)
    _informe("B.5 SANO — tres capas, ninguna factura torcida", arriba, real)
    print("\n  🔑 QUÉ MIRAR: el peaje. La capa 2 no averigua NI UN DATO — solo")
    print("     re-dice lo que la capa 3 ya dijo. Lo que le cueste es el precio")
    print("     de la profundidad, y es el «casi nunca» del plan con un número.")
    orquestador.anotar("b5_sano", texto=arriba["texto"],
                       dice_usd=arriba["coste_total_usd"],
                       real_usd=real["total_usd"], por_capa=real["por_capa"])
    return 0


def experimento_queja():
    """La factura de Europa se manda al especialista del dólar. ~$0,025.

    El worker de abajo tiene el derecho a negarse (B.4) y ve el mensaje original
    del usuario, así que **puede** darse cuenta. Lo que se mide es qué queda de
    esa negativa dos capas más arriba.
    """
    arriba, real = correr(torcer={"EUR": "USD"})
    _informe("B.5 CON QUEJA — la factura de Europa va al especialista del dólar",
             arriba, real)

    texto = (arriba["texto"] or "").lower()
    print("\n  ── ¿SOBREVIVIÓ LA QUEJA? ──")
    print("     🔑 Esto lo juzgan TUS OJOS sobre el texto de arriba. Lo de abajo")
    print("        son pistas del harness, no el veredicto — es la lección de")
    print("        B.4: la parte del juicio que se puede verificar es la que no")
    print("        necesita un modelo, y ésta no se puede.")
    for pista, señal in [
        ("dice que algo no se pudo resolver",
         any(p in texto for p in ("no se pudo", "no pudo", "no se resolvió",
                                  "no corresponde", "no fue posible"))),
        ("menciona EUROS o EUROPA",
         any(p in texto for p in ("euro", "europa"))),
        ("nombra el MOTIVO (dólares donde iban euros)",
         "dólar" in texto or "dolar" in texto),
    ]:
        print(f"        {'sí' if señal else 'no ':>3} · {pista}")

    orquestador.anotar("b5_queja", texto=arriba["texto"],
                       dice_usd=arriba["coste_total_usd"],
                       real_usd=real["total_usd"], por_capa=real["por_capa"])
    return 0


# ---------------------------------------------------------------------------
# 6) LAS PRUEBAS — gratis
# ---------------------------------------------------------------------------

def _pruebas():
    global ENRUTADO_FORZADO
    fallos = []

    def check(nombre, condicion, detalle=""):
        print(f"  {'✅' if condicion else '❌'} {nombre}"
              f"{f'  → {detalle}' if detalle and not condicion else ''}")
        if not condicion:
            fallos.append(nombre)

    print("\n  PRUEBAS — $0.00\n")

    # 1) 🚨 LA QUE PROTEGE A.2. `correr_orquestador` ahora acepta tres cosas por
    #    la puerta; si algún día un valor por defecto cambia, A.2 dejaría de ser
    #    A.2 y sus números pagados dejarían de valer, SIN dar un error.
    import inspect
    firma = inspect.signature(orquestador.correr_orquestador).parameters
    check("1. los tres parámetros nuevos existen y arrancan en None",
          all(firma[p].default is None
              for p in ("sistema", "tools", "funciones")),
          f"defaults: {[firma[p].default for p in ('sistema','tools','funciones')]}")

    # 2) El puente entra por la puerta y MANDA sobre el global. Si no mandara,
    #    la capa 2 correría con el menú de A.2 y nadie lo notaría.
    class _Bloque:
        name, input, id = "solo_mia", {}, "b1"
    llamada = {}

    def _falsa(contabilidad, verboso=True):
        llamada["si"] = True
        return {"ok": 1}

    conta = {"capa": "prueba"}
    # 🚨 EL DESVÍO NO ES UN ADORNO — SIN ÉL ESTA PRUEBA ENSUCIABA EL REGISTRO
    #    REAL, Y LO HIZO CUATRO VECES ANTES DE QUE ALGUIEN LO MIRARA (sesión 97).
    #    `ejecutar_un_bloque` llama a `anotar`, y `anotar` escribe donde diga
    #    `orquestador.REGISTRO`. Que aquí sea el archivo de las corridas PAGADAS
    #    es lo que convierte una prueba gratis en un dato inventado.
    with orquestador.registro_desviado():
        r = orquestador.ejecutar_un_bloque(_Bloque(), conta, verboso=False,
                                           funciones={"solo_mia": _falsa})
    check("2. el puente que entra por la puerta manda sobre el global",
          llamada.get("si") and '"ok": 1' in r["content"], r["content"])

    # 3) 🚨 EL AUDITOR CONTRA UN REGISTRO CUYO TOTAL SE SABE. Sin esta prueba el
    #    auditor no vale nada: es lo escrito hoy, o sea el sospechoso de estar
    #    ciego, y si contara mal inventaría un agujero que no existe.
    falso = AQUI / "_prueba_registro.jsonl"
    falso.write_text(
        "\n".join(json.dumps(d, ensure_ascii=False) for d in [
            {"evento": "llamada_api", "capa": "vieja", "costo_usd": 99.0},
            {"evento": "llamada_api", "capa": "capa1", "costo_usd": 0.001},
            {"evento": "herramienta", "capa": "capa1"},
            {"evento": "llamada_api", "capa": "intermediario:X", "costo_usd": 0.002},
            {"evento": "llamada_api", "worker": "usd", "costo_usd": 0.003},
        ]) + "\n", encoding="utf-8")
    try:
        a = auditar({falso: 1}, rutas=[falso])
        check("3. el auditor suma solo lo NUEVO y solo las llamadas pagadas",
              abs(a["total_usd"] - 0.006) < 1e-9 and a["llamadas"] == 3,
              f"dio {a}")
        check("4. el auditor separa el gasto por capa",
              a["por_capa"] == {"capa1": 0.001, "intermediario:X": 0.002,
                                "usd": 0.003},
              f"dio {a['por_capa']}")
    finally:
        falso.unlink(missing_ok=True)

    # 5) EL INSTRUMENTO ESTÁ APAGADO. Es la sesión 50 de TEAPP: lo que mató una
    #    medición fue una báscula que se quedó encendida.
    check("5. el enrutado forzado arranca vacío", ENRUTADO_FORZADO == {})
    check("6. sin torcer, cada moneda va a su especialista",
          _torcer("EUR") == "EUR" and _torcer("USD") == "USD")

    # 7) 🔑 LA QUE DEFIENDE LA LECCIÓN DE B.4. El encargo lleva HECHOS; el
    #    permiso de negarse vive en el system prompt. Si alguien "mejora" el
    #    encargo metiéndole la instrucción, el experimento mediría otra cosa —
    #    y B.4 ya midió que metida ahí no funciona.
    e = encargo_con_original(400, "EUR", "una factura de Alemania por 400")
    check("7. el encargo NO le pide al worker que se niegue",
          not any(p in e.lower() for p in ("no lo respondas", "dilo en vez",
                                           "niégate", "no corresponde")),
          e)
    check("8. pero SÍ le da el mensaje original (sin él no hay testigo)",
          "Alemania" in e)

    # 9) El permiso está donde B.4 dijo que tenía que estar.
    check("9. el worker de la capa 3 lleva el derecho a negarse en el SYSTEM",
          "no lo respondas" in
          supervisor.SISTEMA_DIVISA_CON_DERECHO_A_NEGARSE.lower())

    # 10) 🚨 LA PRUEBA QUE DEFIENDE LA APUESTA 3 DE MÍ MISMO. La forma barata de
    #     ganarla era sumar solo lo que la capa 2 gastó ella sola. Esta prueba
    #     afirma que se suma el TOTAL, para que la apuesta pueda fallar.
    fuente = inspect.getsource(herramienta_consultar_region)
    check("10. la contabilidad suma el coste TOTAL de la capa 2, no el propio",
          'coste_workers_usd"] += dentro["coste_total_usd"]' in fuente)

    # 11) Las dos regiones existen y cada factura tiene su original. Sin el
    #     original, el testigo de la capa 3 es ciego y el experimento no mide.
    check("11. cada factura trae su mensaje original",
          all(f.get("original") for f in FACTURAS) and len(FACTURAS) == 2)

    # 12-13) 🚨 LA PRUEBA QUE FALTABA, Y SU AUSENCIA COSTÓ $0,0247. El
    #        instrumento de la primera versión NO torcía nada: cambiaba una
    #        etiqueta y el encargo seguía siendo correcto. La corrida salió
    #        verde y no midió nada.
    #        🔑 Un instrumento que no se ha visto morder es una nota, no un
    #           instrumento (`LM.13`) — y aquí se ve morder GRATIS, sin API:
    #           basta leer el texto que se le iba a mandar al worker.
    guardado = ENRUTADO_FORZADO
    try:
        ENRUTADO_FORZADO = {"EUR": "USD"}
        torcido = encargo_con_original(400, _torcer("EUR"),
                                       "una factura de un proveedor de Alemania")
        check("12. torcido, el ENCARGO pide una moneda distinta de la real",
              "400 USD" in torcido, torcido)
        check("13. y el CONTEXTO sigue diciendo la verdad (esa es la presa)",
              "Alemania" in torcido)
    finally:
        ENRUTADO_FORZADO = guardado

    check("14. y al salir, el instrumento quedó apagado", ENRUTADO_FORZADO == {})

    print()
    if fallos:
        print(f"  ❌ {len(fallos)} prueba(s) en rojo: {', '.join(fallos)}")
        return 1
    print("  ✅ todas en verde, y no costaron nada.")
    return 0


def main(argv):
    if "--sano" in argv:
        return experimento_sano()
    if "--queja" in argv:
        return experimento_queja()
    return _pruebas()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
