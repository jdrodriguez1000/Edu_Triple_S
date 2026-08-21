"""fallos.py — C.4 del nivel 8: QUÉ PASA CUANDO UN WORKER SE CAE.

    LA PREGUNTA DE C.4, EN UNA FRASE

Un worker es un agente dentro de otro. Hasta aquí siempre terminó: bien, sin
presupuesto o sin vueltas, pero terminó. **C.4 es el día en que no termina.**

Tres formas de no terminar, y son distintas de verdad:

    SE CAE     -> revienta a mitad. Excepción, traceback, adiós.
    SE DEMORA  -> no revienta: se queda ahí. El que espera no sabe si sigue.
    NO CONTESTA-> da vueltas y nunca llega a una respuesta.

⚠️ LA TRAMPA ES QUE LAS TRES *PARECEN* RESUELTAS. El código ya tiene un
   `except Exception` en la frontera, ya tiene `motivo="max_vueltas"`, y el SDK
   ya trae un timeout. Este archivo NO da eso por bueno: lo hace morder y mira
   qué queda en pie. Es `LM.13` — un freno que no has visto morder es una nota.

🚨 Y LA PRIMERA VERSIÓN DE ESTE MISMO DOCSTRING CAYÓ EN LA TRAMPA, EL MISMO DÍA.
   Decía, de la tercera pata: *«esta ya está: `max_vueltas`»*. Dos horas después
   se contaron los cierres de worker de TODOS los registros del curso:
   **28 por presupuesto · 74 terminaron bien · `max_vueltas` CERO.**
   El freno existía, tenía su motivo, tenía su frase para el modelo y cruzaba la
   frontera — y no había cortado nunca nada. 🔑 **Se da por resuelto lo que está
   escrito, no lo que está probado**, y el archivo que venía a decir justo eso
   lo dio por resuelto en su tercer renglón. Se deja escrito en vez de borrarlo.


    ESTE PASO NO PAGA UN CENTAVO, Y ESA ES LA MITAD DEL DISEÑO

El modelo aquí es **de mentira**: `ClienteDeMentira` devuelve respuestas con
`usage` inventado y luego revienta cuando se le dice. Todo lo demás es de
verdad — el bucle del worker, la contabilidad, el registro, el árbol.

🔑 Y por eso lo que se mide vale: **lo falso es el que habla, no el harness.**
   Si el instrumento fuera falso, mediríamos al instrumento (sesión 97).

📌 El registro se desvía con `orquestador.registro_desviado()`. Ninguna línea
   de este archivo entra en los `.jsonl` pagados: aquella mezcla ya se pagó una
   vez en la sesión 97.
"""

import json
import sys
import threading
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "05b-proyecto"))

import agente          # noqa: E402
import contexto        # noqa: E402
import fan_out         # noqa: E402
import orquestador     # noqa: E402
import worker          # noqa: E402


# ---------------------------------------------------------------------------
# 1) EL MODELO DE MENTIRA — lo único falso de todo el archivo
# ---------------------------------------------------------------------------

class _Uso:
    """Lo mínimo que `agente.costo()` necesita mirar."""

    def __init__(self, entrada, salida):
        self.input_tokens = entrada
        self.output_tokens = salida


class _Bloque:
    """Un bloque `tool_use` como el que devuelve la API."""

    def __init__(self, nombre, entrada=None, ident="b1"):
        self.type = "tool_use"
        self.name = nombre
        self.input = entrada or {}
        self.id = ident


class _Respuesta:
    def __init__(self, stop_reason, content, entrada=1000, salida=200):
        self.stop_reason = stop_reason
        self.content = content
        self.usage = _Uso(entrada, salida)


class ClienteDeMentira:
    """Devuelve un guion de respuestas y, cuando se acaba, **revienta**.

    ⭐ La gracia está en el orden: primero contesta bien VARIAS veces —o sea,
       primero GASTA DINERO DE VERDAD en la contabilidad— y después se cae. Un
       worker que revienta en la primera llamada no habría gastado nada, y
       entonces el agujero que se busca no existiría. **El caso caro es el que
       se cae a media faena.**
    """

    def __init__(self, guion, fallo):
        self.guion = list(guion)
        self.fallo = fallo
        self.llamadas = 0
        self.messages = types.SimpleNamespace(create=self._create)

    def _create(self, **_kw):
        self.llamadas += 1
        if self.guion:
            return self.guion.pop(0)
        raise self.fallo


def _guion_que_revienta(vueltas_buenas, fallo):
    """`vueltas_buenas` respuestas que piden una herramienta, y luego el fallo.

    📌 Pide `tasa`, que SÍ está en el menú del worker — pero el puente se vacía
       abajo, así que ninguna herramienta llega a la red. La respuesta que
       recibe el modelo es el «no tienes esa herramienta» del freno 7, y con eso
       el bucle da la vuelta y vuelve a llamar. Es el camino de verdad, sin
       tocar internet ni pagar nada.
    """
    guion = [_Respuesta("tool_use", [_Bloque("tasa", {"moneda": "USD"}, f"b{i}")])
             for i in range(1, vueltas_buenas + 1)]
    return ClienteDeMentira(guion, fallo)


class _SinPuente:
    """Deja el puente del worker vacío mientras dure el `with`.

    ⚠️ Es un instrumento de medida y se apaga en el `finally`, como
       `registro_desviado`. Un instrumento que se queda encendido en producción
       es la sesión 50 de TEAPP otra vez.
    """

    def __enter__(self):
        self._real = worker.puente_para
        worker.puente_para = lambda nombres: {}

    def __exit__(self, *_):
        worker.puente_para = self._real
        return False


class _ClienteFalso:
    """Cambia el cliente de la API por el de mentira mientras dure el `with`."""

    def __init__(self, cliente):
        self.cliente = cliente

    def __enter__(self):
        self._real = agente.cliente
        agente.cliente = self.cliente
        return self.cliente

    def __exit__(self, *_):
        agente.cliente = self._real
        return False


def _contabilidad_nueva():
    """La misma forma que arma `correr_orquestador`, sin el orquestador."""
    return {
        "capa": "orquestador",
        "workers": 0,
        "coste_workers_usd": 0.0,
        "llamadas_api_workers": 0,
        "entrada_workers": 0,
        "salida_workers": 0,
        "detalle": [],
        "reparto": None,
        "encargos": None,
    }


def _leer(carpeta):
    """Todas las líneas anotadas dentro de la carpeta desviada."""
    lineas = []
    for ruta in sorted(Path(carpeta).glob("*.jsonl")):
        with open(ruta, encoding="utf-8") as f:
            for renglon in f:
                renglon = renglon.strip()
                if renglon:
                    lineas.append(json.loads(renglon))
    return lineas


def _gasto_real(lineas):
    """La factura según el REGISTRO: cada `llamada_api` con su costo."""
    return round(sum(d.get("costo_usd", 0.0) for d in lineas
                     if d.get("evento") == "llamada_api"), 6)


# ---------------------------------------------------------------------------
# 2) EL EXPERIMENTO — un worker que revienta a media faena
# ---------------------------------------------------------------------------

def correr_crash(fallo, vueltas_buenas=2, verboso=False):
    """Corre UN worker por la frontera de verdad y lo hace reventar.

    Devuelve `(contabilidad, lineas_del_registro, salida_al_modelo)`.

    🔑 Se llama a `ejecutar_un_bloque` y no a `correr_worker` a pelo **a
       propósito**: el agujero que se busca no está dentro del worker, está en
       la costura. Medir el worker solo sería medir el sitio equivocado.
    """
    contabilidad = _contabilidad_nueva()
    bloque = _Bloque("consultar_moneda", {"monto": 1000, "moneda": "USD"}, "b0")

    with orquestador.registro_desviado() as carpeta:
        with _ClienteFalso(_guion_que_revienta(vueltas_buenas, fallo)):
            with _SinPuente():
                # Un tramo raíz, para que las líneas salgan con parentesco como
                # en una corrida de verdad.
                #
                # 🐛 Y LA RAÍZ TIENE QUE ANOTAR. La primera versión de esto abría
                #    el tramo y no escribía nada, y el auditor del árbol se
                #    quejaba de `padre_inexistente` — con razón, pero de un
                #    defecto MÍO, no del harness: en una corrida de verdad
                #    `correr_orquestador` anota `orquestador_inicio` nada más
                #    entrar. 🔑 Se dejó escrito porque estuvo a punto de contarse
                #    como hallazgo: **un instrumento mal montado no da silencio,
                #    da una queja creíble sobre otra cosa.**
                with contexto.tramo("capa:orquestador"):
                    orquestador.anotar("orquestador_inicio", capa="orquestador",
                                       tarea="(experimento de C.4)")
                    salida = orquestador.ejecutar_un_bloque(
                        bloque, contabilidad, verboso=verboso)
                    # 🎁 Y ESTA LÍNEA LA PIDIÓ EL DETECTOR NUEVO, EN VOZ ALTA.
                    #    Sin ella la raíz anotaba `orquestador_inicio` y nunca
                    #    su cierre, y `nodo_abierto` se quejó — con razón. **Es
                    #    la segunda vez en este mismo archivo que una queja del
                    #    árbol apunta a un defecto del INSTRUMENTO y no del
                    #    harness** (la primera fue el `padre_inexistente` de
                    #    arriba). ⭐ Y eso no resta: un detector que caza dos
                    #    montajes descuidados el día que nace es lo contrario de
                    #    los que nunca se ven morder (`LM.13`).
                    orquestador.anotar("orquestador_fin", capa="orquestador")
        lineas = _leer(carpeta)

    return contabilidad, lineas, salida


# ---------------------------------------------------------------------------
# 3) LAS CUATRO PREGUNTAS DE LA APUESTA, UNA POR FUNCIÓN
# ---------------------------------------------------------------------------

def agujero_1_factura(verboso=True):
    """¿El dinero que gastó el worker que reventó entra en la factura?

    📏 LO QUE SE MIDIÓ ANTES DE ARREGLARLO (C.4 · paso 1):
           gastado de verdad $0,004000 · anotado en el libro $0,000000
    """
    contabilidad, lineas, _ = correr_crash(RuntimeError("la API se cayó"))

    registro = _gasto_real(lineas)
    libro = round(contabilidad["coste_workers_usd"], 6)
    perdido = round(registro - libro, 6)
    detalle = contabilidad["detalle"]

    if verboso:
        print("\n" + "=" * 72)
        print("  AGUJERO 1 — EL DINERO DEL WORKER QUE REVENTÓ  ✅ ARREGLADO")
        print("=" * 72)
        print(f"  Gastado de verdad (registro) ..... ${registro:.6f}")
        print(f"  Anotado en la factura (libro) .... ${libro:.6f}")
        print(f"  Descuadre ........................ ${perdido:.6f}")
        print(f"  Workers contados en el libro ..... {contabilidad['workers']}")
        print("-" * 72)
        print("  ANTES: $0,004000 gastados y $0,000000 en el libro. El")
        print("  `except Exception` de la frontera atrapaba el crash —eso")
        print("  funciona desde B.2— pero `correr_worker` que LANZA nunca")
        print("  devuelve, así que las seis sumas de `contabilidad[...] +=`")
        print("  no llegaban a correr.")
        print("  🔑 El gasto no se perdía por gastarse mal: se perdía por no")
        print("  volver por donde se cuenta. AHORA el worker atrapa cualquier")
        print("  excepción y CIERRA — devuelve su fracaso como dato, igual que")
        print("  hacía con el presupuesto. El dinero cuadra al céntimo.")

    return {"registro": registro, "libro": libro, "perdido": perdido,
            "workers": contabilidad["workers"],
            "motivo": detalle[0]["motivo"] if detalle else None}


def agujero_2_arbol(verboso=True):
    """¿El árbol se entera de que un tramo se abrió y no cerró?

    📏 ANTES: 1 `worker_inicio`, 0 `worker_fin`, **0 quejas del auditor**.
    """
    _, lineas, _ = correr_crash(RuntimeError("la API se cayó"))

    from traza import auditar_arbol

    quejas = auditar_arbol(lineas)
    inicios = sum(1 for d in lineas if d.get("evento") == "worker_inicio")
    fines = sum(1 for d in lineas if d.get("evento") == "worker_fin")
    abiertos = [q for q in quejas if q["tipo"] == "nodo_abierto"]

    if verboso:
        print("\n" + "=" * 72)
        print("  AGUJERO 2 — EL CRASH VISTO DESDE EL ÁRBOL  ✅ ARREGLADO")
        print("=" * 72)
        print(f"  Líneas `worker_inicio` ........... {inicios}")
        print(f"  Líneas `worker_fin` .............. {fines}")
        print(f"  Quejas `nodo_abierto` ............ {len(abiertos)}")
        print("-" * 72)
        print("  ⭐ FÍJATE EN QUÉ CAMBIÓ Y QUÉ NO. El arreglo del agujero 1 hace")
        print("  que el worker CIERRE aunque se caiga, así que hoy sale 1 y 1:")
        print("  este tramo ya no queda abierto. Pero eso arregla el síntoma de")
        print("  este caso, no la ceguera del auditor.")
        print("  🔑 Por eso el detector `nodo_abierto` entra igual (prueba 42 de")
        print("  `traza.py`, con su torcedura al lado): un `Ctrl-C`, un corte de")
        print("  luz o un `os._exit` siguen dejando el tramo abierto, y ANTES")
        print("  de C.4 ese registro salía **verde entero**. `LM.66` al revés:")
        print("  no es que el dato fuera incontestable, es que NO HABÍA dato, y")
        print("  la ausencia no contradice a nadie.")

    return {"inicios": inicios, "fines": fines, "quejas": quejas,
            "abiertos": abiertos}


def agujero_3_mensaje(verboso=True):
    """¿Lo que sube al modelo distingue un fallo que se arregla reintentando?

    📏 ANTES: las dos frases eran IDÉNTICAS, carácter por carácter, y las dos
       decían «No lo llames otra vez igual».
    """
    import httpx

    temporal = agente.anthropic.APIConnectionError(
        request=httpx.Request("POST", "https://api.anthropic.com/v1/messages"))
    permanente = RuntimeError("nuestro programa tiene un defecto")

    _, _, salida_temporal = correr_crash(temporal)
    _, _, salida_permanente = correr_crash(permanente)

    texto_t = json.loads(salida_temporal["content"])
    texto_p = json.loads(salida_permanente["content"])
    iguales = texto_t == texto_p

    if verboso:
        print("\n" + "=" * 72)
        print("  AGUJERO 3 — LO QUE EL MODELO LEE CUANDO SU ESPECIALISTA MUERE")
        print("                                                ✅ ARREGLADO")
        print("=" * 72)
        print("  Se cayó la red (SÍ se arregla reintentando):")
        print(f"    motivo: {texto_t.get('motivo')}")
        print(f"    → {texto_t.get('causa')}")
        print("  Defecto nuestro (NO se arregla reintentando):")
        print(f"    motivo: {texto_p.get('motivo')}")
        print(f"    → {texto_p.get('causa')}")
        print("-" * 72)
        print(f"  ¿Dicen lo mismo? .... {'SÍ 🚨' if iguales else 'no ✅'}")
        print("  ANTES las dos eran la misma frase: «falló por un defecto")
        print("  interno del programa. No lo llames otra vez igual.»")
        print("  🔑 Para el reintentable esa frase no era imprecisa: era")
        print("  DAÑINA. Le prohibía justo lo único que lo arreglaba. Es")
        print("  `LM.71` con otra ropa — el mensaje que llega primero entierra")
        print("  la causa real.")

    return {"temporal": texto_t, "permanente": texto_p, "iguales": iguales}


def agujero_4_reloj(verboso=True):
    """¿Cuánto puede tardar un worker antes de que alguien lo pare?

    El techo residual no se mide esperando —eso costaría ocho minutos de
    reloj—: se calcula con las constantes que ya están escritas.
    """
    vueltas = worker.MAX_VUELTAS_WORKER
    intentos = agente.REINTENTOS_PROPIOS
    timeout = agente.TIMEOUT_SEGUNDOS

    # Las esperas del reintento: 2·2⁰ y 2·2¹ entre los tres intentos, más el
    # azar de hasta 1 s de cada una. Se toma el peor caso, que es de lo que
    # habla un techo.
    espera_por_vuelta = (2.0 + 1) + (4.0 + 1)
    techo = vueltas * (intentos * timeout + espera_por_vuelta)
    plazo = worker.LIMITE_WORKER_SEGUNDOS

    if verboso:
        print("\n" + "=" * 72)
        print("  AGUJERO 4 — EL WORKER QUE SE DEMORA  ✅ ARREGLADO")
        print("=" * 72)
        print(f"  Vueltas máximas ................ {vueltas}")
        print(f"  Intentos por llamada ........... {intentos}")
        print(f"  Timeout por intento ............ {timeout} s")
        print(f"  Espera entre intentos (peor) ... {espera_por_vuelta} s por vuelta")
        print("-" * 72)
        print(f"  Techo que SALÍA de multiplicar eso .. {techo:.0f} s "
              f"= {techo/60:.1f} min")
        print(f"  ✅ Plazo que ahora se DECIDE ........ {plazo:.0f} s "
              f"= {plazo/60:.1f} min")
        print("-" * 72)
        print("  Nadie había escrito nunca el primer número. No es que el tope")
        print("  no existiera: es que era la CONSECUENCIA de tres constantes")
        print("  elegidas por otros motivos.")
        print("  🔑 Un plazo que nadie decidió no es un plazo: es un residuo.")
        print("  📌 Y los 90 s salen de un dato, no de una intuición: los 99")
        print("  workers pagados del curso dan mediana 2,28 s, p90 5,73 s y")
        print("  peor caso 17,94 s. 90 s son CINCO VECES el peor visto — un")
        print("  freno que no puede morder a uno legítimo.")
        print("  ⚠️ Y su límite, dicho entero: corta ENTRE vueltas, no dentro")
        print("  de una. Una llamada colgada sigue acotada por el timeout del")
        print("  SDK. Lo que este plazo mata es la SUMA, que era lo que no")
        print("  tenía dueño.")

    return {"vueltas": vueltas, "intentos": intentos, "timeout": timeout,
            "techo_segundos": round(techo, 1), "plazo": plazo}


class _RelojFalso:
    """Adelanta el reloj del worker un salto por consulta, sin esperar de verdad.

    🔑 ES LA ÚNICA FORMA HONESTA DE VER MORDER UN PLAZO DE 90 SEGUNDOS EN UNA
       PRUEBA QUE TIENE QUE DURAR MENOS DE UN SEGUNDO. La alternativa —un
       `sleep` de verdad— haría la suite tan lenta que dejaría de correrse, y
       una prueba que no se corre es peor que no tenerla.
    📌 Lo que se falsea es el RELOJ, no el freno: el `if` que corta es el mismo
       que va a correr en producción.
    """

    def __init__(self, salto):
        self.salto = salto
        self.ahora = 0.0

    def __enter__(self):
        self._real = worker.time.monotonic

        def monotonic():
            self.ahora += self.salto
            return self.ahora

        worker.time.monotonic = monotonic
        return self

    def __exit__(self, *_):
        worker.time.monotonic = self._real
        return False


def plazo_muerde(limite=90.0, salto=40.0, verboso=True):
    """Corre un worker con el reloj adelantado y mira si el plazo corta.

    El modelo de mentira aquí NO revienta: contesta bien siempre y pide
    herramientas sin parar. Si el worker se para, se paró por el plazo.
    """
    guion = [_Respuesta("tool_use", [_Bloque("tasa", {"moneda": "USD"}, f"b{i}")])
             for i in range(1, 20)]
    cliente = ClienteDeMentira(guion, RuntimeError("no debería llegar aquí"))

    with orquestador.registro_desviado():
        with _ClienteFalso(cliente):
            with _SinPuente():
                with _RelojFalso(salto):
                    resultado = worker.correr_worker(
                        "Convierte 1000 USD a pesos colombianos.",
                        nombre="usd", limite_segundos=limite, verboso=False)

    if verboso:
        print("\n" + "=" * 72)
        print("  EL PLAZO, VISTO MORDER")
        print("=" * 72)
        print(f"  Plazo dado ....... {limite:.0f} s")
        print(f"  Motivo del corte . {resultado['motivo']}")
        print(f"  Vueltas dadas .... {resultado['vueltas']}")
        print(f"  Texto ............ {resultado['texto']}")

    return resultado


# ---------------------------------------------------------------------------
# 3.b) LAS OTRAS DOS PATAS DE C.4 — «no contesta» y el CRASH EN PARALELO
# ---------------------------------------------------------------------------
#
# ⭐ Y HACE FALTA UN INSTRUMENTO MÁS QUE ARRIBA NO HACÍA FALTA.
#    Hasta aquí bastaba con vaciar el puente: daba igual lo que la herramienta
#    contestara, porque el worker iba a reventar de todos modos. Para el
#    paralelo NO: ahí hay dos workers que tienen que TERMINAR BIEN mientras el
#    tercero se cae. Un worker que termina bien necesita un contrato lleno, y un
#    contrato lleno necesita herramientas que devuelvan datos.
# 📌 Por eso el puente de mentira devuelve exactamente la forma que devuelven
#    `tasa` y `convertir` de verdad — `de`/`tasa`/`fuente`/`actualizado` y
#    `monto`/`resultado`/`de`—, que es la que lee `contrato_divisa`. Si la forma
#    no fuera la misma, los workers "buenos" saldrían fallidos y el experimento
#    mediría otra cosa sin decirlo.

TASAS_DE_MENTIRA = {"USD": 4000.0, "EUR": 4400.0, "CAD": 2900.0}


def _puente_de_mentira(nombres):
    """Las dos herramientas del worker, sin red y con datos inventados."""

    def tasa(moneda, **_):
        m = (moneda or "").upper()
        if m not in TASAS_DE_MENTIRA:
            return {"error": f"no tengo la moneda {m}"}
        return {"de": m, "a": "COP", "tasa": TASAS_DE_MENTIRA[m],
                "fuente": "inventado.local", "actualizado": "2026-08-21"}

    def convertir(monto, moneda, tasa=None, **_):
        m = (moneda or "").upper()
        t = tasa if tasa is not None else TASAS_DE_MENTIRA.get(m)
        if t is None:
            return {"error": f"no tengo la moneda {m}"}
        return {"de": m, "monto": monto, "tasa": t,
                "resultado": round(float(monto) * float(t), 2)}

    todas = {"tasa": tasa, "convertir": convertir}
    return {n: todas[n] for n in nombres if n in todas}


class _PuenteDeMentira:
    """Cambia el puente del worker por el de datos inventados, sin red."""

    def __enter__(self):
        self._real = worker.puente_para
        worker.puente_para = _puente_de_mentira

    def __exit__(self, *_):
        worker.puente_para = self._real
        return False


class ClientePorMoneda:
    """Un modelo de mentira que atiende a TRES workers a la vez.

    🚨 Y ESTA CLASE ES LA MITAD DEL EXPERIMENTO DEL PARALELO, ASÍ QUE VALE LA
       PENA VER POR QUÉ NO SIRVE EL DE ARRIBA. `ClienteDeMentira` reparte un
       guion en fila: la 1ª llamada se lleva la 1ª respuesta. Con tres workers
       en tres hilos **el orden de llegada ya no es el de nadie** — el guion se
       barajaría entre los tres y cada uno recibiría trozos del de otro.
    🔑 Por eso este mira QUIÉN pregunta, no CUÁNDO. Lee la moneda del encargo y
       lleva la cuenta de cada uno por separado, con candado. Es exactamente la
       lección de B.2 aplicada al instrumento: **en paralelo, «lo que pasó justo
       antes» deja de significar «lo mío».**
    """

    def __init__(self, revienta_en=None, vueltas_antes=2, sin_fin=()):
        # `revienta_en`: la moneda cuyo worker se cae. `sin_fin`: las monedas
        # cuyo worker no termina nunca (piden herramienta una y otra vez).
        self.revienta_en = (revienta_en or "").upper()
        self.vueltas_antes = vueltas_antes
        self.sin_fin = {m.upper() for m in sin_fin}
        self.cuenta = {}
        self.candado = threading.Lock()
        self.messages = types.SimpleNamespace(create=self._create)

    def _moneda(self, mensajes):
        texto = ""
        for m in mensajes:
            if m.get("role") == "user" and isinstance(m.get("content"), str):
                texto = m["content"]
                break
        for m in ("USD", "EUR", "CAD"):
            if m in texto.upper():
                return m
        return "USD"

    def _create(self, **kw):
        moneda = self._moneda(kw.get("messages", []))
        with self.candado:
            self.cuenta[moneda] = self.cuenta.get(moneda, 0) + 1
            n = self.cuenta[moneda]

        if moneda == self.revienta_en and n > self.vueltas_antes:
            raise RuntimeError(f"el worker de {moneda} se cayó en la vuelta {n}")

        if moneda in self.sin_fin:
            # Nunca dice que terminó: pide herramienta hasta que un freno lo
            # pare. Es «no contesta» en su forma pura.
            return _Respuesta("tool_use",
                              [_Bloque("tasa", {"moneda": moneda}, f"b{n}")])

        if n == 1:
            return _Respuesta("tool_use",
                              [_Bloque("tasa", {"moneda": moneda}, f"b{n}")])
        if n == 2:
            return _Respuesta("tool_use",
                              [_Bloque("convertir",
                                       {"monto": 1000, "moneda": moneda},
                                       f"b{n}")])
        return _Respuesta("end_turn", [_Texto(f"1000 {moneda} son pesos.")])


class _Texto:
    """Un bloque de texto como el que devuelve la API al terminar."""

    def __init__(self, texto):
        self.type = "text"
        self.text = texto


def sin_respuesta(verboso=True):
    """PATA 3 DE C.4 — «no contesta». El worker que nunca dice que terminó.

    🚨 SE ESCRIBE PORQUE ESTE FRENO NUNCA SE HABÍA VISTO MORDER, Y EL DOCSTRING
       DE ARRIBA LLEGÓ A DECIR QUE ESTA PATA «YA ESTABA».
       Contados los cierres de worker de todos los registros del curso:
       **28 por presupuesto, 74 terminaron bien, `max_vueltas` CERO.** Existe
       desde A.1, está en la lista de motivos, cruza la frontera con su frase…
       y no hay una sola línea en la que haya cortado nada. Es `LM.13` exacto:
       **un freno que no has visto morder es una nota, no un freno.**
    """
    contabilidad = _contabilidad_nueva()
    bloque = _Bloque("consultar_moneda", {"monto": 1000, "moneda": "USD"}, "b0")

    with orquestador.registro_desviado() as carpeta:
        with _ClienteFalso(ClientePorMoneda(sin_fin=["USD"])):
            with _PuenteDeMentira():
                with contexto.tramo("capa:orquestador"):
                    orquestador.anotar("orquestador_inicio", capa="orquestador",
                                       tarea="(experimento de C.4)")
                    salida = orquestador.ejecutar_un_bloque(
                        bloque, contabilidad, verboso=False)
                    orquestador.anotar("orquestador_fin", capa="orquestador")
        lineas = _leer(carpeta)

    al_modelo = json.loads(salida["content"])
    detalle = contabilidad["detalle"][0] if contabilidad["detalle"] else {}

    if verboso:
        print("\n" + "=" * 72)
        print("  PATA 3 — EL WORKER QUE NO CONTESTA  (visto morder por 1ª vez)")
        print("=" * 72)
        print(f"  Vueltas dadas .................... {detalle.get('vueltas')} "
              f"(el tope es {worker.MAX_VUELTAS_WORKER})")
        print(f"  Motivo del cierre ................ {detalle.get('motivo')}")
        print(f"  Gastado antes de cortar .......... ${detalle.get('coste_usd', 0):.6f}")
        print(f"  En la factura .................... "
              f"${contabilidad['coste_workers_usd']:.6f}")
        print("-" * 72)
        print(f"  Lo que sube al modelo:")
        print(f"    motivo: {al_modelo.get('motivo')}")
        print(f"    → {al_modelo.get('causa')}")
        print("-" * 72)
        print("  📊 En los 102 cierres de worker registrados del curso:")
        print("     28 por presupuesto · 74 terminaron bien · max_vueltas CERO.")
        print("  🔑 Existía, cruzaba la frontera y tenía su frase escrita. Lo")
        print("  que no tenía era una sola línea de haber cortado algo. Hoy la")
        print("  tiene, y por eso deja de ser una nota.")

    return {"lineas": lineas, "al_modelo": al_modelo, "detalle": detalle,
            "libro": round(contabilidad["coste_workers_usd"], 6),
            "registro": _gasto_real(lineas)}


def crash_en_paralelo(verboso=True):
    """PATA 2 DE C.4, Y LA QUE DE VERDAD FALTABA — el crash con TRES hilos.

    🚨 TODO LO MEDIDO ANTES DE ESTA FUNCIÓN FUE UN WORKER, EN SERIE, Y ESA ES
       LA TOPOLOGÍA FÁCIL. `orquestador.py` lleva escrito desde B.2 que atrapar
       la excepción **en el sitio que no sabe de hilos** hace que dé igual — y
       nadie lo había visto. Si una excepción escapara del hilo, el `Future` se
       la guardaría y saltaría **al recogerla**, matando la tanda entera: los
       otros dos workers no hicieron nada malo y morirían con el tercero.

    ⭐ Y hay una segunda cosa que solo se puede mirar aquí: **el árbol**. Los
       tres workers anotan desde tres hilos distintos, y el que se cae lo hace a
       media faena. Que el parentesco salga bien con un crash de por medio es lo
       que `atado()` promete y esto es lo que lo comprueba.
    """
    from traza import auditar_arbol

    contabilidad = _contabilidad_nueva()
    bloques = [_Bloque("consultar_moneda", {"monto": 1000, "moneda": m}, f"b{i}")
               for i, m in enumerate(("USD", "EUR", "CAD"), start=1)]

    with orquestador.registro_desviado() as carpeta:
        with _ClienteFalso(ClientePorMoneda(revienta_en="CAD")):
            with _PuenteDeMentira():
                with contexto.tramo("capa:orquestador"):
                    orquestador.anotar("orquestador_inicio", capa="orquestador",
                                       tarea="(experimento de C.4 en paralelo)")
                    fan_out.reiniciar_linea_de_tiempo()
                    resultados = fan_out.reparto_en_paralelo(
                        bloques, contabilidad, verboso=False)
                    orquestador.anotar("orquestador_fin", capa="orquestador")
        lineas = _leer(carpeta)

    subidos = [json.loads(r["content"]) for r in resultados]
    por_moneda = dict(zip(("USD", "EUR", "CAD"), subidos))
    quejas = auditar_arbol(lineas)
    padres = {d["id"]: d.get("padre") for d in lineas if d.get("id")}
    tramos = {d["id"]: d.get("tramo") for d in lineas if d.get("id")}
    workers = [i for i, t in tramos.items() if (t or "").startswith("worker:")]
    huerfanos = [i for i in workers if padres.get(i) is None]

    if verboso:
        print("\n" + "=" * 72)
        print("  PATA 2 — UN WORKER SE CAE Y LOS OTROS DOS SIGUEN VIVOS")
        print("=" * 72)
        for m in ("USD", "EUR", "CAD"):
            d = por_moneda[m]
            if "error" in d:
                print(f"  {m}: ❌ {d.get('motivo')} — {d.get('causa')[:52]}…")
            else:
                print(f"  {m}: ✅ pesos = {d.get('pesos')}  "
                      f"(fuente {d.get('fuente')})")
        print("-" * 72)
        print(f"  Workers en la factura ............ {contabilidad['workers']} de 3")
        print(f"  Gastado (registro) ............... ${_gasto_real(lineas):.6f}")
        print(f"  Anotado (libro) .................. "
              f"${contabilidad['coste_workers_usd']:.6f}")
        print(f"  Tramos `worker:` en el árbol ..... {len(workers)}")
        print(f"  De ellos, huérfanos .............. {len(huerfanos)}")
        print(f"  Quejas del auditor ............... {len(quejas)}  {quejas}")
        print("-" * 72)
        print("  🔑 La tanda NO murió. El `except` de la frontera está en el")
        print("  sitio que no sabe de hilos, así que la excepción nunca llega")
        print("  al `Future` — y si llegara, saltaría al recogerla y se")
        print("  llevaría por delante a dos workers que hicieron su trabajo.")
        print("  ⭐ Y el árbol aguanta el crash: los tres siguen colgando de su")
        print("  padre. Eso es `atado()` cumpliendo con un hilo muerto dentro.")

    return {"subidos": por_moneda, "quejas": quejas, "workers": workers,
            "huerfanos": huerfanos, "contabilidad": contabilidad,
            "registro": _gasto_real(lineas), "lineas": lineas}


def red_de_seguridad(verboso=True):
    """LOS DOS LADOS DE LA MISMA AFIRMACIÓN, Y EL SEGUNDO NO ES PROSA.

    `crash_en_paralelo` enseña que la tanda sobrevive. Eso, solo, **no prueba
    que la red de seguridad sirva de algo**: podría ser que en paralelo un
    crash nunca fuera peligroso. Aquí se hace lo mismo DOS VECES sobre los
    mismos tres bloques, con una sola diferencia:

        CON red  → por `ejecutar_un_bloque`, que tiene el `except Exception`
        SIN red  → la misma función levantando la excepción, a `pool.map` pelado

    🔑 Y lo que se mira no es solo si revienta: es **qué pasa con los otros
       dos**. La excepción no se queda en su hilo — el `Future` se la guarda y
       la relanza AL RECOGERLA, así que `pool.map` muere y **los dos resultados
       buenos, ya calculados y ya pagados, se pierden**. Ese es el precio real,
       y no se ve en el traceback.
    """
    from concurrent.futures import ThreadPoolExecutor

    bloques = [_Bloque("consultar_moneda", {"monto": 1000, "moneda": m}, f"b{i}")
               for i, m in enumerate(("USD", "EUR", "CAD"), start=1)]

    # La herramienta de mentira: los dos primeros contestan, el tercero LANZA.
    # Es lo mismo que haría un defecto nuestro en la capa de abajo.
    def herramienta(monto, moneda, contabilidad, verboso=False):
        if moneda.upper() == "CAD":
            raise RuntimeError("defecto interno en la capa de abajo")
        return {"moneda": moneda.upper(), "pesos": monto * 4000}

    # --- CON RED: por la frontera de verdad ---------------------------------
    contabilidad = _contabilidad_nueva()
    with orquestador.registro_desviado():
        with contexto.tramo("capa:orquestador"):
            orquestador.anotar("orquestador_inicio", capa="orquestador",
                               tarea="(red de seguridad)")
            con_red = fan_out.reparto_en_paralelo(
                bloques, contabilidad, verboso=False,
                funciones={"consultar_moneda": herramienta})
            orquestador.anotar("orquestador_fin", capa="orquestador")
    vivos_con_red = len(con_red)

    # --- SIN RED: la misma excepción, directa al `pool.map` ------------------
    # ⚠️ Esto NO es nuestro harness con un agujero: es el harness con la costura
    #    quitada a mano, para ver qué costura era. La diferencia importa — el
    #    código de verdad no pasa por aquí.
    def trabajo_sin_red(bloque):
        return herramienta(contabilidad=None, verboso=False, **bloque.input)

    sin_red_error = None
    vivos_sin_red = 0
    try:
        with ThreadPoolExecutor(max_workers=3) as pool:
            vivos_sin_red = len(list(pool.map(trabajo_sin_red, bloques)))
    except Exception as fallo:
        sin_red_error = f"{type(fallo).__name__}: {fallo}"

    if verboso:
        print("\n" + "=" * 72)
        print("  LA RED DE SEGURIDAD, CON Y SIN — el mismo fallo, dos finales")
        print("=" * 72)
        print(f"  CON red (por `ejecutar_un_bloque`)")
        print(f"    resultados que llegan ....... {vivos_con_red} de 3")
        print(f"    la tanda ..................... sobrevive ✅")
        print(f"  SIN red (a `pool.map` pelado)")
        print(f"    resultados que llegan ....... {vivos_sin_red} de 3")
        print(f"    la tanda ..................... {sin_red_error} ❌")
        print("-" * 72)
        print("  ⭐ FÍJATE EN LOS DOS QUE NO FALLARON. Sin red no llega NINGUNO:")
        print("  el USD y el EUR terminaron su trabajo, gastaron su dinero, y")
        print("  su resultado se pierde al recoger la tanda. **La excepción no")
        print("  mata al que falló: mata a los que iban bien.**")
        print("  🔑 Y por eso el `except` está donde está —en el sitio que no")
        print("  sabe de hilos—: así el paralelo no tiene que acordarse de nada.")

    return {"con_red": vivos_con_red, "sin_red": vivos_sin_red,
            "error_sin_red": sin_red_error}


# ---------------------------------------------------------------------------
# 4) LAS PRUEBAS
# ---------------------------------------------------------------------------

def _pruebas():
    fallos = []

    def check(titulo, condicion, detalle=""):
        marca = "✅" if condicion else "❌"
        print(f"  {marca} {titulo}")
        if detalle:
            print(f"       {detalle}")
        if not condicion:
            fallos.append(titulo)

    print("\n" + "=" * 72)
    print("  PRUEBAS DE C.4 · PASO 1 — los agujeros, medidos y no supuestos")
    print("=" * 72)

    # -- 1 a 3: el instrumento antes que la medida. Si el modelo de mentira no
    #    se comporta como se cree, las cuatro medidas de abajo son ficción.
    cliente = _guion_que_revienta(2, RuntimeError("boom"))
    check("1. el cliente de mentira sirve el guion y luego revienta",
          cliente._create().stop_reason == "tool_use"
          and cliente._create().stop_reason == "tool_use",
          "dos respuestas buenas antes del fallo")
    try:
        cliente._create()
        revienta = False
    except RuntimeError:
        revienta = True
    check("2. y en la tercera llamada lanza el fallo pedido", revienta)

    real = agente.cliente
    with _ClienteFalso("de mentira"):
        cambiado = agente.cliente == "de mentira"
    check("3. el cliente falso se apaga al salir del `with`",
          cambiado and agente.cliente is real)

    # -- 4: el registro no se ensucia. Va antes que nada porque si esto falla,
    #    el daño ya no se puede deshacer (`git` salvó la línea base ayer).
    reales = (worker.REGISTRO, orquestador.REGISTRO)
    contabilidad, lineas, salida = correr_crash(RuntimeError("boom"))
    check("4. los registros pagados quedan intactos",
          (worker.REGISTRO, orquestador.REGISTRO) == reales
          and len(lineas) > 0,
          f"{len(lineas)} líneas escritas, todas en la carpeta temporal")

    # -- 5: el crash NO tumba al orquestador. Esto ya funcionaba: se comprueba
    #    para que el día que alguien lo rompa, se ponga rojo aquí.
    check("5. el crash del worker no tumba al orquestador",
          salida["type"] == "tool_result",
          f"el modelo recibe un resultado, no un traceback")

    # ═══════════════════════════════════════════════════════════════════════
    # LO QUE SIGUE VIGILA LOS CUATRO ARREGLOS, Y LAS SEIS PRUEBAS QUE HABÍA
    # ANTES DESCRIBÍAN EL DAÑO.
    #
    # ⭐ Se dice porque es la parte que no se ve en el archivo terminado: las
    #    pruebas 7 a 13 existieron en verde diciendo *«el dinero NO llega a la
    #    factura»*, *«el auditor no se queja»*, *«las dos frases son la misma»*.
    #    Al meter los arreglos se pusieron ROJAS LAS SEIS, y ese rojo es la
    #    única prueba de que los arreglos tocan lo que se midió y no otra cosa.
    # 🔑 Un arreglo que no pone roja ninguna prueba vieja no está arreglando
    #    nada medido: está arreglando algo que nadie había visto romperse.
    # ═══════════════════════════════════════════════════════════════════════

    # -- 6 y 7: ARREGLO 1 — el dinero del worker que revienta.
    a1 = agujero_1_factura(verboso=False)
    check("6. el worker gastó dinero de verdad antes de reventar",
          a1["registro"] > 0, f"${a1['registro']:.6f} en el registro")
    check("7. ✅ ARREGLO 1 — y ese dinero SÍ llega a la factura (era $0,000000)",
          a1["libro"] == a1["registro"] and a1["perdido"] == 0.0
          and a1["workers"] == 1,
          f"libro ${a1['libro']:.6f} · descuadre ${a1['perdido']:.6f}")
    check("8. y el crash llega con su motivo propio, no como un `ok=False` mudo",
          a1["motivo"] == "crash", f"motivo={a1['motivo']!r}")

    # -- 9 y 10: ARREGLO 2 — el árbol.
    a2 = agujero_2_arbol(verboso=False)
    check("9. ✅ ARREGLO 1 de rebote — el tramo ya cierra aunque el worker se caiga",
          a2["inicios"] == 1 and a2["fines"] == 1,
          f"inicios={a2['inicios']} · fines={a2['fines']}")
    check("10. y el árbol de este crash sale sano (no quedan nodos abiertos)",
          a2["abiertos"] == [] and a2["quejas"] == [], f"quejas={a2['quejas']}")
    # ⚠️ La otra mitad del arreglo 2 —que el detector MUERDA cuando el tramo sí
    #    queda abierto— vive en `traza.py`, pruebas 42 a 46. Aquí no se repite:
    #    se dice dónde está, para que nadie crea que este verde la incluye.

    # -- 11 y 12: ARREGLO 3 — el mensaje que sube al modelo.
    a3 = agujero_3_mensaje(verboso=False)
    check("11. ✅ ARREGLO 3 — el reintentable y el permanente ya NO dicen lo mismo",
          not a3["iguales"],
          f"{a3['temporal'].get('motivo')} vs {a3['permanente'].get('motivo')}")
    check("12. y al pasajero se le deja reintentar; al nuestro, no",
          "no lo reintentes" not in a3["temporal"].get("causa", "").lower()
          and "no lo reintentes" in a3["permanente"].get("causa", "").lower(),
          a3["temporal"].get("causa"))

    # -- 13 a 15: ARREGLO 4 — el plazo, y hay que VERLO MORDER (`LM.13`).
    a4 = agujero_4_reloj(verboso=False)
    check("13. el techo residual que había pasaba de 7 minutos",
          a4["techo_segundos"] > 420,
          f"{a4['techo_segundos']} s = {a4['techo_segundos']/60:.1f} min")
    check("14. ✅ ARREGLO 4 — ahora hay un plazo DECIDIDO, y es mucho menor",
          a4["plazo"] < a4["techo_segundos"] / 4,
          f"{a4['plazo']:.0f} s decididos contra {a4['techo_segundos']:.0f} s de residuo")

    r = plazo_muerde(verboso=False)
    check("15. 🚨 Y MUERDE: con el reloj adelantado, el worker corta por plazo",
          r["motivo"] == "plazo" and not r["ok"],
          f"motivo={r['motivo']!r} · vueltas={r['vueltas']}")
    # 16) El otro lado, sin el cual la 15 no prueba nada: con tiempo de sobra el
    #     plazo se calla y el que corta es el freno de siempre.
    sin_prisa = plazo_muerde(limite=90.0, salto=0.001, verboso=False)
    check("16. y con tiempo de sobra el plazo NO corta (corta `max_vueltas`)",
          sin_prisa["motivo"] == "max_vueltas",
          f"motivo={sin_prisa['motivo']!r}")
    # 17) El reloj falso se apaga. Un instrumento encendido de más aquí sería
    #     peor que en ningún otro sitio: falsearía el tiempo de todo lo demás.
    check("17. el reloj falso se apagó al salir del `with`",
          worker.time.monotonic is __import__("time").monotonic)

    # -- 18 a 20: PATA 3 — «no contesta», vista morder por primera vez.
    nc = sin_respuesta(verboso=False)
    check("18. 🚨 `max_vueltas` MUERDE (0 veces en 102 cierres registrados)",
          nc["detalle"].get("motivo") == "max_vueltas"
          and nc["detalle"].get("vueltas") == worker.MAX_VUELTAS_WORKER,
          f"motivo={nc['detalle'].get('motivo')!r} · "
          f"vueltas={nc['detalle'].get('vueltas')}")
    check("19. y su causa llega arriba en prosa, no como un `ok=False` mudo",
          nc["al_modelo"].get("motivo") == "max_vueltas"
          and "vueltas" in nc["al_modelo"].get("causa", ""),
          nc["al_modelo"].get("causa"))
    check("20. el gasto del que no contestó también cuadra",
          nc["libro"] == nc["registro"] and nc["libro"] > 0,
          f"libro ${nc['libro']:.6f} · registro ${nc['registro']:.6f}")

    # -- 21 a 24: PATA 2 — el crash con TRES hilos. La topología de verdad.
    par = crash_en_paralelo(verboso=False)
    check("21. 🚨 un worker se cae y los otros DOS entregan su dato",
          par["subidos"]["USD"].get("pesos") is not None
          and par["subidos"]["EUR"].get("pesos") is not None
          and par["subidos"]["CAD"].get("motivo") == "crash",
          {m: (d.get("motivo") or "ok") for m, d in par["subidos"].items()})
    check("22. los TRES entran en la factura, también el que reventó",
          par["contabilidad"]["workers"] == 3
          and round(par["contabilidad"]["coste_workers_usd"], 6) == par["registro"],
          f"{par['contabilidad']['workers']} workers · "
          f"${par['contabilidad']['coste_workers_usd']:.6f} de ${par['registro']:.6f}")
    check("23. ⭐ y el ÁRBOL aguanta el crash: 3 tramos, ninguno huérfano",
          len(par["workers"]) == 3 and par["huerfanos"] == [],
          f"{len(par['workers'])} tramos worker · "
          f"{len(par['huerfanos'])} huérfanos")
    check("24. el auditor no tiene ni una queja sobre ese árbol",
          par["quejas"] == [], par["quejas"])

    # -- 25 y 26: la red de seguridad, con y sin. La 25 sola no probaría nada:
    #    hace falta el contrafactual para saber que la costura sirve.
    red = red_de_seguridad(verboso=False)
    check("25. CON la red, los 3 resultados llegan",
          red["con_red"] == 3, f"{red['con_red']} de 3")
    check("26. 🚨 SIN la red, no llega NINGUNO — ni los dos que iban bien",
          red["sin_red"] == 0 and red["error_sin_red"] is not None,
          f"{red['sin_red']} de 3 · {red['error_sin_red']}")

    print("-" * 72)
    if fallos:
        print(f"  ❌ {len(fallos)} prueba(s) en rojo: {fallos}")
    else:
        print("  ✅ las 26 pruebas, verdes, y no costaron nada.")
        print("     📌 Las 7 a 13 existieron en verde DESCRIBIENDO EL DAÑO. Los")
        print("     arreglos las pusieron rojas, y por eso se sabe que arreglan")
        print("     lo que se midió.")
    print("=" * 72)
    return not fallos


def main(argv):
    if "--pruebas" in argv:
        return 0 if _pruebas() else 1

    print("=" * 72)
    print("  C.4 — LOS TRES FALLOS DEL WORKER, MEDIDOS SIN PAGAR")
    print("=" * 72)
    agujero_1_factura()
    agujero_2_arbol()
    agujero_3_mensaje()
    agujero_4_reloj()
    sin_respuesta()
    crash_en_paralelo()
    red_de_seguridad()
    print("\n📌 Coste de todo esto: $0,000000. El modelo era de mentira; el")
    print("   harness, no.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
