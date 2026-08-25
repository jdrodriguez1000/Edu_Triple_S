"""router.py — B.3 del nivel 8: la primera topología donde el camino DEPENDE.

    LA FRASE QUE ABRE EL BLOQUE

B.1 descubrió que un orden fijo son tres líneas seguidas. B.2, que un reparto
fijo son diez. Las dos topologías anteriores **no necesitaban un orquestador**:
el camino estaba escrito antes de que llegara nada.

⭐ Un router es la primera vez que el camino no se puede escribir por adelantado.
   Y por eso es la primera que **compra algo con el dinero que gasta arriba**:
   el modelo se paga por DECIDIR, y hasta ahora no había nada que decidir.

🔒 Las tres apuestas de este bloque están selladas en `README.md`
   (*«🎲 LA APUESTA»*) y COMMITEADAS antes de escribir este archivo. Ninguna se
   edita cuando lleguen los números: lo que salga se escribe debajo.


    LO QUE ESTE ARCHIVO **NO** HACE, Y ES LO QUE LO HACE BARATO

🚫 **No llama a ningún worker.** El router decide, se apunta la decisión, y se
   acabó. Llamar al especialista costaría $0,00724 por entrada (medido en B.2) y
   **no contesta ninguna de las tres preguntas del bloque**.

🔑 Esa resta es toda la economía del experimento: el banco entero con el router
   del modelo cuesta ~$0,003, y con el router de `if`, exactamente $0,00.

📌 Y no es un atajo: es la misma idea de las pruebas gratis de B.2. **Lo que se
   mide es la DECISIÓN, así que se paga la decisión y nada más.**


    EL EXPERIMENTO: UNA SOLA VARIABLE

Dos routers sobre el mismo banco de entradas, con el mismo juez:

    router_if       -> un `dict` de palabras clave          $0,00
    router_modelo   -> UNA llamada, salida de una palabra   ~$0,0004 (apostado)

Nada más cambia. Si al comparar se mueve el número de entradas o el texto del
banco, no cambió una variable: cambiaron dos. (Es la comprobación de las once
llamadas de B.2, en pequeño.)


    ⚠️ EL VIGILANTE ES EL PRIMER SOSPECHOSO DE ESTAR CIEGO

En B.1 el instrumento ciego fue el verificador escrito ese mismo día. En B.2, la
línea de tiempo escrita ese mismo día. Las dos veces **no dieron un dato falso:
dieron silencio**, y el silencio se lee como confirmación (`LM.15`).

🚨 Así que aquí se dice ANTES de escribirlo: **el juez de este archivo no puede
   devolver un booleano.** Cuando el router contesta *"no sé cuál"* ante *"pásalo
   a la moneda del cliente"*, eso NO es un fallo: es lo correcto. Un booleano lo
   mete en la misma casilla que elegir mal, y son **opuestos** — uno es seguro,
   el otro es daño silencioso.
   → Ver `juzgar()`, que tiene CUATRO veredictos y explica por qué no son tres.

🚨 Y el SEGUNDO sospechoso, que casi se cuela: **las etiquetas de oro del banco
   las escribí a mano.** Un juez que compara contra una etiqueta equivocada da un
   rojo perfecto por el motivo equivocado. Por eso el banco lleva un campo
   `discutible`, y las entradas marcadas ahí **no cuentan en el marcador**.


    CÓMO SE CORRE

    python router.py              -> LAS PRUEBAS. Gratis. $0,00
    python router.py --if         -> el banco entero con el router de `if`. $0,00
    python router.py --modelo     -> el banco entero con el router del modelo. ~$0,003
    python router.py --ambos      -> los dos y la comparación. ~$0,003

📌 Sin argumentos corre las PRUEBAS, no la demo. Lo que cuesta dinero se pide con
   todas las letras — igual que `fan_out.py`.
"""

import json
import sys
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "05b-proyecto"))

import agente          # noqa: E402
import compartida     # noqa: E402


# ---------------------------------------------------------------------------
# 1) CONFIGURACIÓN
# ---------------------------------------------------------------------------

MODELO = agente.MODELO

REGISTRO = AQUI / f"registro_router_{MODELO}.jsonl"

# Los destinos posibles. Son los TRES WORKERS QUE YA EXISTEN desde A.1: el mismo
# código con otra moneda.
#
# ⭐ No se construye ningún especialista nuevo para B.3, y eso no es pereza: si
#    los destinos fueran nuevos, al comparar habría dos cosas cambiando (la
#    topología y los workers) y no se sabría a cuál atribuir el resultado.
DESTINOS = ["usd", "eur", "cad"]

# Lo que devuelve un router cuando NO puede decidir. No es un destino: es la
# ausencia de uno, y tiene que poder distinguirse de haber elegido mal.
NINGUNO = None

# Tope de gasto del banco entero. Con la apuesta de ~$0,0004 por decisión y 8
# entradas, esto es unas 15 veces el gasto esperado: no frena el experimento,
# frena un descarrilamiento.
PRESUPUESTO_BANCO_USD = 0.05


# ---------------------------------------------------------------------------
# 2) EL BANCO DE ENTRADAS — la frontera apostada, escrita como casos
# ---------------------------------------------------------------------------
#
# La apuesta 1 dice: «un `if` basta mientras la clave se pueda EXTRAER del texto;
# deja de bastar cuando hay que INFERIRLA.»
#
# Un banco que solo llevara casos fáciles la confirmaría siempre, y no habría
# medido nada. Por eso está ordenado en NIVELES que cruzan la frontera a
# propósito, y por eso el nivel 3 existe: es donde la apuesta dice que el `if`
# se cae.
#
# 📌 Cada entrada lleva `espera`, que es la ETIQUETA DE ORO: lo que un humano
#    dice que había que hacer. `None` significa «lo correcto es NO elegir».

BANCO = [
    # --- NIVEL 1: la palabra está ahí, literal -----------------------------
    {"id": "n1-a", "nivel": 1,
     "texto": "¿Cuánto son 250 dólares en pesos?",
     "espera": "usd"},
    {"id": "n1-b", "nivel": 1,
     "texto": "Necesito pasar 300 euros a pesos colombianos.",
     "espera": "eur"},

    # --- NIVEL 2: sinónimo o código. La LISTA se alarga, la idea no cambia --
    {"id": "n2-a", "nivel": 2,
     "texto": "Convierte 250 USD a pesos.",
     "espera": "usd"},
    {"id": "n2-b", "nivel": 2,
     "texto": "¿A cómo está el billete verde hoy?",
     "espera": "usd"},

    # --- NIVEL 3: hay que INFERIR. Aquí la apuesta dice que el `if` se cae ---
    {"id": "n3-a", "nivel": 3,
     "texto": "Me llegó una factura de un proveedor de Alemania por 400. ¿Cuánto es en pesos?",
     "espera": "eur"},
    {"id": "n3-b", "nivel": 3,
     "texto": "Un taller de Toronto me cobró 500 por la reparación. Pásalo a pesos.",
     "espera": "cad"},

    # --- NIVEL 4: no hay NADA que extraer. Lo correcto es no elegir ---------
    {"id": "n4-a", "nivel": 4,
     "texto": "Pásalo a la moneda del cliente, por favor.",
     "espera": NINGUNO},

    # --- NIVEL 5: la trampa. Menciona DOS destinos --------------------------
    # ⚠️ ETIQUETA DISCUTIBLE, y se marca en vez de fingir que está resuelta.
    #    Se puede defender `cad` (es lo que hay que convertir) y se puede
    #    defender abstenerse (hay dos monedas y ninguna es pesos, que es lo
    #    único que estos workers saben hacer).
    #    🔑 Un caso cuya respuesta correcta yo mismo no tengo clara NO PUEDE
    #       contar en el marcador: sería el juez midiendo mi duda, no al router.
    #       Se corre igual, porque lo interesante es VER qué contesta cada uno.
    {"id": "n5-a", "nivel": 5,
     "texto": "¿Cuánto es un dólar canadiense en dólares americanos?",
     "espera": NINGUNO, "discutible": True,
     "nota": "menciona dos destinos y ninguno es 'a pesos'"},
]


# ---------------------------------------------------------------------------
# 3) REGISTRO — con candado, aunque hoy no haga falta
# ---------------------------------------------------------------------------
#
# 📌 B.2 dejó dicho que los candados EN SERIE NO CUESTAN NADA: nunca hay que
#    esperar a nadie. Por eso se ponen siempre, no «cuando haga falta». El día
#    que un router se llame desde un reparto en paralelo, esto ya está.

# 🚚 `_CANDADO_REGISTRO` se MUDÓ a `compartida.py` en la sesión 112 — no se
#    borró por gusto: mientras estuvo aquí era uno de CUATRO candados
#    distintos vigilando archivos que a veces son el mismo.


def anotar(evento, **datos):
    """Escribe UNA línea JSON en el registro. Una línea, un hecho."""
    linea = {"hora": datetime.now(timezone.utc).isoformat(timespec="seconds"),
             "evento": evento}
    linea.update(datos)
    # 🔒 SESIÓN 112 — EL CANDADO YA NO VIVE AQUÍ.
    #    Vive junto al ARCHIVO, en `compartida.anotar_linea`, y son DOS: uno de
    #    hilos por archivo y uno de disco para los otros procesos. Hasta hoy este
    #    módulo tenía el suyo propio, y un candado atado al módulo no protege un
    #    archivo que comparte con otros tres. Mordió: la línea 626 de
    #    `registro_pruebas_gratis.jsonl`. El porqué y los números, allá.
    compartida.anotar_linea(REGISTRO, linea)


# ---------------------------------------------------------------------------
# 4) ROUTER A — EL `if`. La apuesta del estudiante.
# ---------------------------------------------------------------------------

# Las palabras que delatan cada destino. Fíjate en que esto es literalmente
# «la lista se alarga, la idea no cambia»: añadir un sinónimo es añadir una
# cadena, no pensar distinto.
PALABRAS = {
    "usd": ["dolar", "dolares", "usd", "us$", "billete verde", "americano",
            "americanos", "estadounidense"],
    "eur": ["euro", "euros", "eur", "€"],
    "cad": ["dolar canadiense", "dolares canadienses", "cad", "canadiense",
            "canadienses"],
}


def sin_tildes(texto):
    """Quita tildes y baja a minúsculas.

    ⚠️ Sin esto, «dólares» no coincide con «dolares» y el router falla por
       ORTOGRAFÍA, no por no saber decidir — un rojo con la causa equivocada.
       Es el mismo bicho que `Juan`/`juan` de la sesión 33 de TEAPP: normalizar
       ANTES de comparar.
    """
    plano = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in plano if unicodedata.category(c) != "Mn")


def router_if(texto):
    """Elige destino por palabra clave. Devuelve un destino o `NINGUNO`.

    ⭐ CÓMO SE LEE ESTA FUNCIÓN: no «entiende» nada. Busca cadenas. Si la clave
       está ESCRITA en la entrada, gana; si hay que inferirla, no tiene con qué.

    ⚠️ Y aquí está el veneno de la apuesta 1, en una línea de código: cuando
       nada coincide, esta función NO da un error. Devuelve `NINGUNO` — y en un
       sistema real, un `NINGUNO` sin manejar cae a un destino por defecto y el
       especialista equivocado hace el trabajo IMPECABLEMENTE.
       🔑 Elegir el `if` no es elegir «más simple»: es elegir un modo de fallo
          silencioso en vez de uno caro.
    """
    plano = sin_tildes(texto)

    # ⚠️ EL ORDEN IMPORTA, y es un defecto real disfrazado de detalle: «dólar
    #    canadiense» contiene «dolar». Si se mirara `usd` primero, todo lo
    #    canadiense se enrutaría a Estados Unidos.
    #    🔑 Un `if` con reglas que se solapan tiene un ganador implícito, y el
    #       ganador es el ORDEN EN QUE ESTÁN ESCRITAS — que no se lee en ninguna
    #       parte. Se hace explícito aquí: primero el más específico.
    for destino in ["cad", "eur", "usd"]:
        for palabra in PALABRAS[destino]:
            if sin_tildes(palabra) in plano:
                return destino
    return NINGUNO


# ---------------------------------------------------------------------------
# 5) ROUTER B — EL MODELO. Una llamada, una palabra.
# ---------------------------------------------------------------------------

# ⭐ Compara este system prompt con los tres que ya existen y verás la cuarta voz:
#      A (5b)       -> "eres un asistente de tasas"       (hace)
#      worker       -> "eres un especialista en UNA"      (hace, estrecho)
#      orquestador  -> "tú no averiguas: repartes"        (NO hace)
#      router       -> "tú no repartes: SEÑALAS"          (ni siquiera reparte)
#
# ⚠️ La frase de la abstención no es cortesía: sin ella, un modelo con presión
#    por responder ELIGE IGUAL. Darle una salida honesta es lo que hace que la
#    abstención sea medible en vez de imposible — y es la misma idea que «nunca
#    inventes una cifra» del orquestador.
SISTEMA_ROUTER = (
    "Eres un clasificador. Tu único trabajo es decir a qué especialista de "
    "divisas hay que mandar un mensaje. Los especialistas son exactamente "
    "tres: 'usd' (dólar estadounidense), 'eur' (euro) y 'cad' (dólar "
    "canadiense). "
    "Responde SOLO con una de estas cuatro palabras, en minúscula y sin nada "
    "más: usd, eur, cad, ninguno. "
    "Responde 'ninguno' si el mensaje no permite saber de qué moneda se trata, "
    "o si no se trata de ninguna de esas tres. "
    "No expliques, no saludes, no añadas puntuación."
)


def router_modelo(texto, verboso=True):
    """Una llamada a la API. Devuelve (destino, gasto_usd, tok_entrada, tok_salida).

    📌 `max_tokens=8` no es un ahorro decorativo: la salida esperada es UNA
       palabra. Un tope apretado convierte «se puso a explicar» en un corte
       visible en vez de en una factura silenciosa.

    ⚠️ Devuelve también el gasto porque la apuesta 2 se mide AQUÍ. Un router que
       no informa de lo que costó obliga a estimarlo, y estimar es justo lo que
       este bloque no quiere hacer.
    """
    for intento in range(1, agente.REINTENTOS_PROPIOS + 1):
        try:
            respuesta = agente.cliente.messages.create(
                model=MODELO,
                max_tokens=8,
                system=SISTEMA_ROUTER,
                messages=[{"role": "user", "content": texto}],
            )
            gasto = agente.costo(respuesta.usage)
            crudo = "".join(b.text for b in respuesta.content
                            if b.type == "text").strip().lower()

            # ⚠️ NORMALIZAR LO QUE DEVUELVE EL MODELO, no confiar en que obedeció.
            #    Un modelo que contesta «USD.» habría dado un fallo que no es de
            #    enrutado sino de FORMATO — y se leería como error del router.
            #    Es `LM.15` otra vez: el instrumento midiendo su propio ruido.
            limpio = sin_tildes(crudo).strip(" .`\n\"'")
            destino = limpio if limpio in DESTINOS else NINGUNO

            anotar("decision_router", router="modelo", texto=texto,
                   crudo=crudo, destino=destino,
                   entrada=respuesta.usage.input_tokens,
                   salida=respuesta.usage.output_tokens,
                   costo_usd=round(gasto, 6),
                   stop_reason=respuesta.stop_reason)

            # 🚨 Un `stop_reason` de corte significa que el modelo iba a seguir
            #    hablando. La decisión puede ser buena igual, pero ese dato NO
            #    se puede perder en la pantalla (sesión 84: el aviso vive donde
            #    se borra, la mentira donde sobrevive). Por eso va al registro.
            if respuesta.stop_reason == "max_tokens" and verboso:
                print(f"      ⚠️ el modelo se cortó en el tope: «{crudo}»")

            return (destino, gasto,
                    respuesta.usage.input_tokens, respuesta.usage.output_tokens)

        except agente.REINTENTABLES as fallo:
            if intento == agente.REINTENTOS_PROPIOS:
                anotar("router_fallo", texto=texto, error=str(fallo))
                raise
            time.sleep(2 ** intento)


# ---------------------------------------------------------------------------
# 6) EL JUEZ — cuatro veredictos, y por qué no son tres ni uno
# ---------------------------------------------------------------------------

def juzgar(decidio, espera):
    """Compara la decisión con la etiqueta de oro. Devuelve un VEREDICTO, no un bool.

    🚨 ESTA ES LA FUNCIÓN QUE SE PODÍA ESCRIBIR CIEGA, y por eso se explica
       entera. Lo natural era `return decidio == espera`. Mira lo que eso
       aplasta:

         esperaba 'usd', dijo 'eur'    -> eligió el destino equivocado
         esperaba 'usd', dijo ninguno  -> no eligió, y sí había respuesta
         esperaba ninguno, dijo 'usd'  -> eligió cuando no había nada que elegir

       Un booleano mete las tres en la misma casilla: «False». Y son cosas
       DISTINTAS, con consecuencias opuestas:

         ❌ elegir mal   -> el trabajo sale impecable y equivocado. SILENCIOSO.
         ⚪ abstenerse   -> no se resolvió, pero NADIE recibió basura. SEGURO.
         🔥 inventar     -> lo peor: había una razón para no elegir y eligió.

    ⭐ Por eso son cuatro veredictos y no tres: `abstencion` e `invencion` son
       los dos lados de la misma línea y confundirlos sería exactamente el
       defecto que este comentario evita.

    📌 Es la lección de la sesión 83 de TEAPP (`correct: bool` mezclando dos
       causas contrarias) aplicada ANTES de que muerda, no después.
    """
    if decidio == espera:
        return "acierto"                 # incluye abstenerse cuando tocaba
    if espera is NINGUNO:
        return "invencion"               # no había nada que elegir, y eligió
    if decidio is NINGUNO:
        return "abstencion"              # había respuesta, y no la dio
    return "error_de_destino"            # eligió, y eligió mal


# Los dos veredictos que hacen daño en silencio. Se nombran aparte porque el
# marcador tiene que poder decir «5 aciertos» y, sobre todo, «cuántos de los
# fallos son de los malos».
VEREDICTOS_QUE_HACEN_DANO = ("error_de_destino", "invencion")

SIMBOLO = {"acierto": "✅", "error_de_destino": "❌",
           "abstencion": "⚪", "invencion": "🔥"}


# ---------------------------------------------------------------------------
# 7) LA CORRIDA — el banco entero contra UN router
# ---------------------------------------------------------------------------

def corrida(nombre_router, verboso=True):
    """Pasa el banco entero por un router y devuelve lo que pasó.

    `nombre_router` es "if" o "modelo". Se pasa por NOMBRE y no la función
    suelta para que el registro y el informe no puedan discrepar sobre cuál
    corrió: el nombre que se anota es el mismo que decidió.
    """
    if nombre_router not in ("if", "modelo"):
        raise ValueError(f"router desconocido: {nombre_router}")

    anotar("corrida_inicio", router=nombre_router, entradas=len(BANCO))
    if verboso:
        print(f"\n  ROUTER «{nombre_router}» — {len(BANCO)} entradas\n")

    filas = []
    gasto_total = 0.0
    llamadas = 0
    t0 = time.time()

    for caso in BANCO:
        # ⭐ El presupuesto se mira ANTES de gastar. Mirarlo después es contar
        #    el dinero que ya no tienes (`agente.py`, nivel 5b).
        if gasto_total >= PRESUPUESTO_BANCO_USD:
            print(f"  🛑 presupuesto agotado (${gasto_total:.6f}). Corte.")
            anotar("corte_presupuesto", router=nombre_router,
                   gastado_usd=round(gasto_total, 6), hechas=len(filas))
            break

        if nombre_router == "if":
            destino, gasto, t_in, t_out = router_if(caso["texto"]), 0.0, 0, 0
            anotar("decision_router", router="if", texto=caso["texto"],
                   destino=destino, costo_usd=0.0)
        else:
            destino, gasto, t_in, t_out = router_modelo(caso["texto"], verboso)
            llamadas += 1

        gasto_total += gasto
        veredicto = juzgar(destino, caso["espera"])
        discutible = caso.get("discutible", False)

        filas.append({"id": caso["id"], "nivel": caso["nivel"],
                      "texto": caso["texto"], "espera": caso["espera"],
                      "decidio": destino, "veredicto": veredicto,
                      "discutible": discutible, "costo_usd": gasto,
                      "entrada": t_in, "salida": t_out})

        if verboso:
            marca = SIMBOLO[veredicto] + (" 🤔" if discutible else "")
            esperado = caso["espera"] or "ninguno"
            dicho = destino or "ninguno"
            print(f"  {marca} [n{caso['nivel']}·{caso['id']}] "
                  f"esperaba {esperado:<7} dijo {dicho:<7} ${gasto:.6f}")
            print(f"        «{caso['texto'][:66]}»")

    segundos = time.time() - t0

    # ⚠️ Los casos DISCUTIBLES salen del marcador. Se corrieron y se ven, pero
    #    no cuentan: un juez que puntúa contra una etiqueta que su propio autor
    #    no tiene clara mide la duda del autor, no al router.
    puntuables = [f for f in filas if not f["discutible"]]

    resultado = {
        "router": nombre_router,
        "filas": filas,
        "puntuables": len(puntuables),
        "aciertos": sum(1 for f in puntuables if f["veredicto"] == "acierto"),
        "dano": sum(1 for f in puntuables
                    if f["veredicto"] in VEREDICTOS_QUE_HACEN_DANO),
        "abstenciones": sum(1 for f in puntuables
                            if f["veredicto"] == "abstencion"),
        "gasto_usd": gasto_total,
        "llamadas_api": llamadas,
        "segundos": segundos,
    }
    anotar("corrida_fin", **{k: v for k, v in resultado.items() if k != "filas"})
    return resultado


def informe(r):
    """Lo que se lee al final de una corrida."""
    print(f"\n  ── ROUTER «{r['router']}» ─────────────────────────────")
    print(f"     aciertos      : {r['aciertos']}/{r['puntuables']}"
          f"   (de {len(r['filas'])} corridas; los 🤔 no puntúan)")
    print(f"     hacen daño    : {r['dano']}   (❌ destino equivocado + 🔥 invención)")
    print(f"     abstenciones  : {r['abstenciones']}   (⚪ seguro, pero sin resolver)")
    print(f"     llamadas API  : {r['llamadas_api']}")
    print(f"     gasto         : ${r['gasto_usd']:.6f}")
    if r["llamadas_api"]:
        print(f"     por decisión  : ${r['gasto_usd'] / r['llamadas_api']:.6f}")
    print(f"     tiempo        : {r['segundos']:.2f} s")


# ---------------------------------------------------------------------------
# 8) LA COMPARACIÓN — donde se lee la apuesta 1
# ---------------------------------------------------------------------------

def comparar(a, b):
    """Pone los dos routers uno al lado del otro, POR NIVEL.

    ⭐ Por nivel y no en total, y esa es la decisión de diseño del informe: un
       marcador global («5 de 7 contra 6 de 7») no dice DÓNDE se cayó cada uno,
       que es literalmente la apuesta. La frontera es un sitio, no un promedio.

    📌 Es la lección de B.2 con otro traje: allí el coste global subió 2,3 % y no
       significaba nada hasta repartirlo por capas.
    """
    print("\n" + "=" * 72)
    print("  COMPARACIÓN — la misma entrada, dos formas de decidir")
    print("=" * 72)

    por_id_a = {f["id"]: f for f in a["filas"]}
    por_id_b = {f["id"]: f for f in b["filas"]}

    nivel_actual = None
    for caso in BANCO:
        fa, fb = por_id_a.get(caso["id"]), por_id_b.get(caso["id"])
        if fa is None or fb is None:
            continue
        if caso["nivel"] != nivel_actual:
            nivel_actual = caso["nivel"]
            print(f"\n  ── NIVEL {nivel_actual} " + "─" * 40)
        marca_a = SIMBOLO[fa["veredicto"]]
        marca_b = SIMBOLO[fb["veredicto"]]
        duda = " 🤔" if caso.get("discutible") else ""
        print(f"    if {marca_a} {str(fa['decidio'] or 'ninguno'):<8}│ "
              f"modelo {marca_b} {str(fb['decidio'] or 'ninguno'):<8}{duda}")
        print(f"       «{caso['texto'][:60]}»")

    print("\n  ── MARCADOR ─────────────────────────────────────────")
    print(f"    {'':<14}{'if':>12}{'modelo':>12}")
    print(f"    {'aciertos':<14}{a['aciertos']:>12}{b['aciertos']:>12}"
          f"   de {a['puntuables']}")
    print(f"    {'hacen daño':<14}{a['dano']:>12}{b['dano']:>12}")
    print(f"    {'abstenciones':<14}{a['abstenciones']:>12}{b['abstenciones']:>12}")
    print(f"    {'gasto':<14}{'$' + format(a['gasto_usd'], '.6f'):>12}"
          f"{'$' + format(b['gasto_usd'], '.6f'):>12}")

    # --- LA APUESTA 2, CONTRASTADA CON EL NÚMERO MEDIDO EN B.2 -------------
    if b["llamadas_api"] and b["gasto_usd"] > 0:
        r = b["gasto_usd"] / b["llamadas_api"]
        worker_usd = 0.00724          # MEDIDO en B.2, corrida paralela 19:21
        umbral = 2 * worker_usd
        print("\n  ── APUESTA 2: ¿sale a cuenta pagar por elegir? ──────")
        print(f"    decisión medida       : ${r:.6f}")
        print(f"    apostado antes de ver : $0.000430")
        print(f"    umbral (2 workers)    : ${umbral:.6f}")
        print(f"    enrutar   = R + 1 worker = ${r + worker_usd:.6f}")
        print(f"    los tres  = 3 workers    = ${3 * worker_usd:.6f}")
        gana = r < umbral
        print(f"    → {'SÍ' if gana else 'NO'} sale a cuenta"
              f"   ({umbral / r:.0f}× de margen)")


# ---------------------------------------------------------------------------
# 9) LAS PRUEBAS — gratis, como en B.2
# ---------------------------------------------------------------------------

def _pruebas():
    """Todo lo que se puede comprobar sin gastar un centavo.

    ⭐ Igual que en B.1 y B.2: lo que se puede probar con piezas falsas se
       prueba con piezas falsas. Aquí sale casi todo, porque `router_if` y
       `juzgar` NO tocan la red.
    """
    fallos = []

    def check(nombre, condicion, detalle=""):
        estado = "✅" if condicion else "❌"
        extra = f"  → {detalle}" if detalle and not condicion else ""
        print(f"  {estado} {nombre}{extra}")
        if not condicion:
            fallos.append(nombre)

    print("\n  PRUEBAS — $0.00\n")

    # 1) La normalización, que es de donde salen los rojos con causa equivocada.
    check("1. sin_tildes iguala «dólares» y «dolares»",
          sin_tildes("Dólares") == sin_tildes("dolares") == "dolares")

    # 2) El `if` en el caso literal. Si esto falla, no hay experimento.
    check("2. el `if` acierta el caso literal",
          router_if("¿Cuánto son 250 dólares en pesos?") == "usd")

    # 3) 🚨 LA JOYA: el solapamiento de «dólar canadiense» con «dólar».
    #    Es el defecto que el ORDEN de la lista evita, y sin esta prueba el
    #    orden es un comentario que nadie vuelve a mirar.
    check("3. «dólar canadiense» NO se enruta a usd",
          router_if("¿Cuánto es un dólar canadiense?") == "cad",
          f"dio {router_if('¿Cuánto es un dólar canadiense?')}")

    # 4) El `if` se cae donde la apuesta dice que se cae. Esta prueba AFIRMA UN
    #    LÍMITE, no una capacidad — y por eso vale: si algún día pasa a verde
    #    por sí sola, alguien amplió el router y hay que volver a apostar.
    check("4. el `if` NO infiere Alemania → eur (límite apostado)",
          router_if("Una factura de Alemania por 400") is NINGUNO,
          f"dio {router_if('Una factura de Alemania por 400')}")

    # 5-9) El juez. Los cuatro veredictos, uno por uno, porque es la pieza que
    #      se podía escribir ciega.
    check("5. juzgar: acertar es acierto", juzgar("usd", "usd") == "acierto")
    check("6. juzgar: abstenerse cuando tocaba TAMBIÉN es acierto",
          juzgar(NINGUNO, NINGUNO) == "acierto")
    check("7. juzgar: elegir mal es error_de_destino (el silencioso)",
          juzgar("eur", "usd") == "error_de_destino")
    check("8. juzgar: no elegir habiendo respuesta es abstencion",
          juzgar(NINGUNO, "usd") == "abstencion")
    check("9. juzgar: elegir sin nada que elegir es invencion (el peor)",
          juzgar("usd", NINGUNO) == "invencion")

    # 10) 🚨 LA PRUEBA QUE DEFIENDE EL PUNTO ENTERO DEL ARCHIVO: los cuatro
    #     veredictos tienen que ser CUATRO COSAS DISTINTAS. Si alguien
    #     «simplifica» `juzgar` a un booleano, esto se pone rojo.
    distintos = {juzgar("usd", "usd"), juzgar("eur", "usd"),
                 juzgar(NINGUNO, "usd"), juzgar("usd", NINGUNO)}
    check("10. los cuatro veredictos son cuatro valores distintos",
          len(distintos) == 4, f"salieron {len(distintos)}: {distintos}")

    # 11) El banco no puede tener ids repetidos: el informe cruza por id, y dos
    #     iguales harían que una fila tapara a la otra SIN AVISAR.
    ids = [c["id"] for c in BANCO]
    check("11. no hay ids repetidos en el banco", len(ids) == len(set(ids)))

    # 12) Toda etiqueta de oro es un destino válido o NINGUNO. Una etiqueta mal
    #     escrita («eu» en vez de «eur») haría fallar al router POR MI ERROR.
    check("12. las etiquetas de oro son válidas",
          all(c["espera"] in DESTINOS or c["espera"] is NINGUNO for c in BANCO))

    # 13) El banco tiene que cruzar la frontera. Un banco solo de casos fáciles
    #     confirmaría la apuesta siempre — y no habría medido nada.
    niveles = {c["nivel"] for c in BANCO}
    check("13. el banco cubre los 5 niveles de dificultad",
          niveles == {1, 2, 3, 4, 5}, f"cubre {sorted(niveles)}")

    print()
    if fallos:
        print(f"  ❌ {len(fallos)} prueba(s) en rojo: {', '.join(fallos)}")
        return 1
    print("  ✅ todas en verde, y no costaron nada.")
    return 0


# ---------------------------------------------------------------------------
# 10) MAIN
# ---------------------------------------------------------------------------

def main(argv):
    if "--ambos" in argv:
        a = corrida("if")
        informe(a)
        b = corrida("modelo")
        informe(b)
        comparar(a, b)
        return 0
    if "--modelo" in argv:
        informe(corrida("modelo"))
        return 0
    if "--if" in argv:
        informe(corrida("if"))
        return 0
    return _pruebas()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
