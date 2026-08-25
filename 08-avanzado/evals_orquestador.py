"""evals_orquestador.py — F.2 del nivel 8: los evals de los modos de falla que
SOLO existen porque hay dos capas.


    LA FRASE QUE HAY QUE VER, Y ES LA QUE JUSTIFICA QUE ESTE ARCHIVO EXISTA

Los **121** casos de `evals.py` del 5b siguen valiendo enteros. No se reescribe
ni uno. Los workers usan las mismas seis herramientas, y una herramienta no
cambia de conducta porque alguien la llame desde más arriba.

🔑 **Lo que cambia al subir una capa no es la herramienta: es quién decide
   llamarla, y qué pasa con lo que devuelve cuando cruza hacia arriba.**

Por eso este archivo tiene otro SUJETO, y ahí está toda la diferencia:

    evals.py (5b)     ->  ¿la herramienta calcula bien?   sujeto: la función
    check() (nivel 8) ->  ¿el freno corta?                sujeto: el harness
    ESTE ARCHIVO      ->  ¿QUÉ HACE EL DE ARRIBA CUANDO   sujeto: LA COSTURA
                          EL DE ABAJO DEVUELVE ESTO?              entre las dos

El punto exacto que se mide es `orquestador.herramienta_consultar_moneda`: el
único sitio del nivel donde un resultado del worker se convierte en algo que el
modelo de arriba va a leer. Todo lo que se pierda, se deforme o se invente ahí
**es un modo de falla del multi-agente y de nada más**.


    🚨 LO QUE ESTE ARCHIVO MIDE Y LO QUE NO — Y VA ANTES DE LA TABLA, A PROPÓSITO

**Estos evals miden el DETECTOR, no el DEFECTO.**

El modo de falla más caro del nivel está medido y tiene fecha: en la sesión 95
el orquestador mandó *«Convierte 400 EUR»* al worker del **dólar**. Un eval
determinista **no puede producir eso**, porque quien elige el destino es el
modelo — y un caso que clava la salida del modelo a mano ya no mide al modelo:
mide mi mano.

Lo que sí se puede medir, y es lo que hay abajo, es que **si** llega torcido, el
harness lo caza y no lo deja subir.

⚠️ Una tabla verde en este archivo NO significa *«el enrutado no se tuerce»*.
   Significa *«cuando se tuerce, no pasa de aquí»*. Son dos frases distintas y
   la segunda es mucho más pequeña que la primera.

📌 Quién mide la primera: **F.3**, pagando, con `atribuidor.py` al lado.


    💸 CUESTA $0,00, Y ESTÁ DEMOSTRADO EN VEZ DE PROMETIDO

Dos frenos, los dos con una prueba que los ve morder (`LM.13`):

  1. `_ClienteTrampa` — se le cambia a `agente` el cliente por uno que solo sabe
     reventar. Si un caso llega a la API, sale en rojo con nombre y apellido.
     Es la técnica de `evals.py` del 5b, heredada del nivel 3.
  2. El registro se desvía a un archivo temporal. Ninguno de estos casos toca
     el registro pagado — y eso también se comprueba, no se supone.
"""

import contextlib
import json
import sys
import tempfile
from pathlib import Path

import orquestador
import presupuesto
import worker

AQUI = Path(__file__).resolve().parent


# ---------------------------------------------------------------------------
#  LA TRAMPA DE RED
# ---------------------------------------------------------------------------
# 🔑 No basta con «no llamo a la API»: hay que hacer que llamar sea IMPOSIBLE y
#    RUIDOSO. Un archivo que promete ser gratis y no lo demuestra es una nota.


class LlegoALaRed(AssertionError):
    """Un caso pidió hablar con el modelo. Este archivo debe costar $0,00."""


class _ClienteTrampa:
    """Un cliente de la API que solo sabe reventar."""

    def __init__(self):
        self.messages = self

    def create(self, **kw):
        raise LlegoALaRed("un eval de F.2 llegó a la API: debe costar $0,00")


# ---------------------------------------------------------------------------
#  EL DOBLE DEL WORKER
# ---------------------------------------------------------------------------
# ⚠️ La trampa metodológica de este archivo, dicha en voz alta: el worker es de
#    mentira. Lo que se mide NO es el worker —para eso están los 121 casos del
#    5b y las 61 comprobaciones de `presupuesto.py`—: es lo que el ORQUESTADOR
#    hace con lo que le llega. Un worker de verdad aquí metería la variabilidad
#    del modelo dentro de un eval determinista, que es lo único que un eval no
#    puede tener.


def resultado_worker(**cambios):
    """Un resultado de worker completo y sano. Cada caso le tuerce UNA cosa.

    Regla heredada del 5b: **un caso, una variable.** Un caso con dos defectos
    puede pasar por la razón equivocada.
    """
    datos_base = {"moneda": "CAD", "monto": 1000, "pesos": 2219774,
                  "tasa": 2219.774, "fuente": "mercado (open.er-api.com)",
                  "fecha": "Fri, 21 Aug 2026"}
    datos_base.update(cambios.pop("datos", None) or {})
    base = {
        "worker": "cad", "modelo": "falso", "esfuerzo": "-",
        "encargo": "Convierte 1000 CAD a pesos colombianos.",
        "origen": worker.ORIGEN_PLANTILLA,
        "texto": "1.000 CAD = 2.219.774 pesos.",
        "datos": datos_base,
        "faltan": [], "discrepa": [],
        "ok": True, "motivo": None, "vueltas": 3,
        "llamadas_api": 3, "herramientas": ["tasa", "convertir"],
        "entrada_tokens": 1200, "salida_tokens": 300,
        "coste_usd": 0.004321, "peor_llamada_usd": 0.002,
        "estimaciones_cortas": 0, "segundos": 4.2,
    }
    base.update(cambios)
    return base


class _RepartoSinSitio:
    """Un reparto que ya repartió todo: el siguiente que pida se queda fuera.

    Es `sin_trozo` de C.2, y **solo existe con dos capas**: el modelo de arriba
    pidió un especialista más de los que el reparto previó. No falló nadie —
    es que no hay sitio.
    """
    n_workers = 3

    def tomar(self, nombre):
        raise presupuesto.SinTrozo(
            f"'{nombre}' es el worker número 4 y el encargo se repartió para 3")

    def quedan_reintentos(self):
        return 0


# ---------------------------------------------------------------------------
#  EL DESVÍO — un solo sitio, y por eso existe
# ---------------------------------------------------------------------------
# 🐛 ESTE `with` NACIÓ DE UN BICHO DE HOY, y se deja escrito en vez de tapado.
#    La primera versión desviaba el registro DENTRO de `correr_evals` y luego
#    devolvía la ruta temporal. Una prueba de más abajo reutilizó esa ruta
#    creyendo que seguía enchufada — y no lo estaba: `correr_evals` restaura en
#    su `finally`. Resultado: tres `sin_trozo` escritos en el registro PAGADO,
#    por un archivo cuya cabecera promete no tocarlo.
#
# 🔑 Es `LM.20` por quinta vez en este nivel, y con el agravante de siempre:
#    `orquestador.registro_desviado()` existe desde la sesión 97 exactamente
#    para esto, y este archivo —escrito hoy— no lo alcanzó. **Una lección
#    aprendida en un archivo no viaja sola al siguiente.**
#
# ⭐ Y el arreglo no es acordarse: es que **no haya forma de escribir fuera**.
#    Quien quiera correr un caso tiene que estar dentro de un `with desviar()`,
#    porque la ruta solo existe ahí dentro.


@contextlib.contextmanager
def desviar():
    """Manda al temporal TODO lo que anoten las dos capas, y restaura al salir."""
    reg_w, reg_o = worker.REGISTRO, orquestador.REGISTRO
    tmp = Path(tempfile.mkdtemp(prefix="evals_orq_")) / "registro.jsonl"
    worker.REGISTRO = orquestador.REGISTRO = tmp
    try:
        yield tmp
    finally:
        worker.REGISTRO, orquestador.REGISTRO = reg_w, reg_o


# ---------------------------------------------------------------------------
#  LOS CASOS — DATOS, no código. Igual que en `evals.py` del 5b.
# ---------------------------------------------------------------------------
#  Cada caso es: (etiqueta, modo, montaje, esperado)
#
#    modo     -> el modo de falla del CATÁLOGO que ejercita
#    montaje  -> qué devuelve el worker, y con qué contabilidad se le llama
#    esperado -> qué tenía que hacer el ORQUESTADOR, y a veces qué tenía que
#                ANOTAR. Comprobar solo lo que sube deja fuera la mitad del
#                trabajo del harness: la mitad que se escribe.
#
#  📌 `esperado` describe CONDUCTA, no redacción. Si mañana se mejora una frase
#     de `_CAUSAS`, ningún caso debe romperse: es la decisión que el 5b pagó en
#     la sesión 12 y que aquí se hereda entera.


def _m(worker_dice=None, extra=None):
    return {"worker": worker_dice or {}, "extra": extra or {}}


CASOS = [
    # --- El camino feliz. Sin él, un rojo no se distingue de un archivo roto.
    ("el contrato completo cruza entero",
     "contrato_ok",
     _m(),
     {"sube_contrato": True, "campos": worker.CAMPOS_DIVISA,
      "sin_faltan": True}),

    # --- 🔑 EL HUECO SUBE COMO HUECO. Es A.3 entero: un contrato no es «no
    #     perder nada», es ELEGIR qué perder — y `faltan` dice cuándo.
    ("un hueco del contrato sube DECLARADO, no relleno",
     "contrato_incompleto",
     _m({"datos": {"fecha": None}, "faltan": ["fecha"]}),
     {"sube_contrato": True, "faltan": ["fecha"]}),

    # --- 🚨 C.3 — el contrato contesta OTRA pregunta. Se pagó por verlo en la
    #     sesión 99: `pesos` está LLENO, con el número de otra moneda, así que
    #     el filtro de huecos lo deja pasar entero. Un hueco y una
    #     contradicción se ven distinto y se cortan distinto.
    ("un contrato de otra moneda NO sube: se descarta",
     "contrato_discrepa",
     _m({"datos": {"moneda": "USD"},
         "discrepa": ["moneda: se pidió CAD y el contrato trae USD"]}),
     {"error": True, "motivo": "discrepancia", "descartado": True,
      "anota": "contrato_discrepa"}),

    # --- 🐛 Y LA CAUSA QUE SUBE ES LA DE VERDAD, NO LA DE ENCIMA.
    #     La sesión 99 pagó por ver esto: un worker cortado por presupuesto a
    #     media cadena discrepaba **como consecuencia**, y arriba subía
    #     `motivo="discrepancia"`. Falso: se quedó sin dinero.
    #     Una consecuencia no puede ir delante de su causa.
    ("cortado por presupuesto: sube el motivo REAL, no `discrepancia`",
     "causa_correcta",
     _m({"ok": False, "motivo": "presupuesto",
         "datos": {"pesos": None}, "faltan": ["pesos"],
         "discrepa": ["moneda: se pidió CAD y el contrato trae USD"]}),
     {"error": True, "motivo": "presupuesto", "causa_menciona": "presupuesto"}),

    ("agotó las vueltas: sube `max_vueltas` y no otra cosa",
     "corte_vueltas",
     _m({"ok": False, "motivo": "max_vueltas",
         "datos": {"pesos": None}, "faltan": ["pesos"]}),
     {"error": True, "motivo": "max_vueltas", "causa_menciona": "vueltas"}),

    # --- ⚠️ EL CASO INCÓMODO. Está en verde porque es la CONDUCTA DE HOY, no
    #     porque sea la correcta: el worker se paró, pero su contrato salió
    #     COMPLETO — la respuesta que el usuario pidió estaba ahí, y se tira.
    #     C.4 lo dejó abierto a propósito y este caso lo mantiene a la vista.
    ("cortado PERO con la cifra buena: hoy se tira igual",
     "parcial_se_tira",
     _m({"ok": False, "motivo": "presupuesto"}),
     {"error": True, "motivo": "presupuesto"}),

    # --- 🚨 EL MODO QUE NO EXISTE CON UNA SOLA CAPA: el modelo pidió un
    #     especialista de más. No falló nada — es que no hay sitio.
    ("un worker de más se rechaza ANTES de gastar, y dice no reintentar",
     "sin_trozo",
     _m(extra={"reparto": _RepartoSinSitio()}),
     {"error": True, "sin_trozo": True, "sin_llamar_al_worker": True,
      "error_menciona": "no lo reintentes", "anota": "sin_trozo"}),

    # --- 🔑 LA FACTURA POR CAPA. Es el dato por el que existe el bloque F: si
    #     el coste del worker no cruza, F.3 no tiene qué comparar.
    ("la factura del worker sube a la contabilidad de arriba",
     "factura_por_capa",
     _m({"coste_usd": 0.004321, "llamadas_api": 3}),
     {"contabilidad": {"workers": 1, "coste_workers_usd": 0.004321,
                       "llamadas_api_workers": 3}}),

    # --- 🔑 Y EL MOTIVO CRUZA AL DETALLE. Faltaba, y se notó al escribir las
    #     comprobaciones de la corrida pagada: arriba llegaba `ok=False` a
    #     secas, que dice que salió mal y no dice de qué.
    ("el `motivo` del worker llega al detalle de la contabilidad",
     "motivo_en_el_detalle",
     _m({"ok": False, "motivo": "presupuesto",
         "datos": {"pesos": None}, "faltan": ["pesos"]}),
     {"detalle_motivo": "presupuesto"}),

    # --- 📎 F.1, cerrada esta misma sesión: quién escribió el encargo.
    ("el encargo baja marcado con su `origen` (F.1)",
     "origen_declarado",
     _m(),
     {"origen_bajo": worker.ORIGEN_PLANTILLA}),
]


# ---------------------------------------------------------------------------
#  EL BUCLE
# ---------------------------------------------------------------------------

def correr_caso(montaje, registro):
    """Monta la costura, la dispara UNA vez y devuelve todo lo observable.

    Devuelve `(subio, contabilidad, bajo, anotado)`:
      · `subio`        — lo que el orquestador entrega al modelo de arriba
      · `contabilidad` — lo que se apuntó en NUESTRO lado de la frontera
      · `bajo`         — con qué argumentos se llamó al worker, o `None`
      · `anotado`      — los eventos escritos en el registro durante el caso
    """
    bajo = {}
    llamado = {"si": False}

    def doble(encargo, **kw):
        llamado["si"] = True
        bajo.update(kw)
        bajo["encargo"] = encargo
        return resultado_worker(**montaje["worker"])

    contabilidad = {
        "workers": 0, "coste_workers_usd": 0.0, "llamadas_api_workers": 0,
        "entrada_workers": 0, "salida_workers": 0, "detalle": [],
        "capa": "orquestador", "encargos": None,
    }
    contabilidad.update(montaje["extra"])

    antes = _eventos(registro)
    real = worker.correr_worker
    worker.correr_worker = doble
    try:
        subio = orquestador.herramienta_consultar_moneda(
            1000, "CAD", contabilidad, verboso=False)
    finally:
        worker.correr_worker = real

    return subio, contabilidad, (bajo if llamado["si"] else None), _eventos(registro)[len(antes):]


def _eventos(registro):
    """Los nombres de evento escritos en el registro, en orden."""
    p = Path(registro)
    if not p.exists():
        return []
    fuera = []
    for linea in p.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if linea:
            try:
                fuera.append(json.loads(linea).get("evento"))
            except json.JSONDecodeError:
                fuera.append("__LINEA_ROTA__")
    return fuera


def revisar(subio, contabilidad, bajo, anotado, esperado):
    """Compara lo observado con lo esperado y devuelve la lista de QUEJAS.

    🔑 Quejas y no un booleano, y es `LM` de F.1 aplicada aquí: un rojo sin
       motivo obliga a volver al código a mano, y entonces el eval no ahorra el
       trabajo — solo lo aplaza.
    """
    q = []
    hay_error = "error" in subio

    if esperado.get("error") and not hay_error:
        q.append(f"se esperaba un error y subió {sorted(subio)}")
    if esperado.get("sube_contrato"):
        if hay_error:
            q.append(f"se esperaba el contrato y subió error ({subio.get('motivo')})")
        else:
            faltantes = [c for c in esperado.get("campos", []) if c not in subio]
            if faltantes:
                q.append(f"no cruzaron los campos {faltantes}")
    if esperado.get("sin_faltan") and "faltan" in subio:
        q.append(f"subió `faltan` sin huecos: {subio['faltan']}")
    if "faltan" in esperado and subio.get("faltan") != esperado["faltan"]:
        q.append(f"faltan={subio.get('faltan')!r}, se esperaba {esperado['faltan']!r}")
    if "motivo" in esperado and subio.get("motivo") != esperado["motivo"]:
        q.append(f"motivo={subio.get('motivo')!r}, se esperaba {esperado['motivo']!r}")
    if esperado.get("descartado"):
        if "descartado" not in subio:
            q.append("el dato torcido no se conservó como `descartado`")
        if "datos" in subio:
            q.append("el dato torcido subió como `datos`: el de arriba se lo puede creer")
    if "causa_menciona" in esperado:
        aguja = esperado["causa_menciona"].lower()
        if aguja not in str(subio.get("causa", "")).lower():
            q.append(f"la causa no menciona {aguja!r}: {str(subio.get('causa'))[:55]!r}")
    if "error_menciona" in esperado:
        todo = " ".join(str(v) for v in subio.values()).lower()
        if esperado["error_menciona"].lower() not in todo:
            q.append(f"no se dice {esperado['error_menciona']!r} en ningún campo")
    if esperado.get("sin_trozo") and not subio.get("sin_trozo"):
        q.append("no se marcó `sin_trozo`")
    if esperado.get("sin_llamar_al_worker") and bajo is not None:
        q.append("se llamó al worker igual: el rechazo llegó tarde y ya se había pagado")
    for k, v in esperado.get("contabilidad", {}).items():
        if contabilidad.get(k) != v:
            q.append(f"contabilidad[{k!r}]={contabilidad.get(k)!r}, se esperaba {v!r}")
    if "detalle_motivo" in esperado:
        motivos = [d.get("motivo") for d in contabilidad["detalle"]]
        if esperado["detalle_motivo"] not in motivos:
            q.append(f"el detalle no lleva el motivo: {motivos!r}")
    if "origen_bajo" in esperado:
        if (bajo or {}).get("origen") != esperado["origen_bajo"]:
            q.append(f"origen bajó como {(bajo or {}).get('origen')!r}")
    if "anota" in esperado and esperado["anota"] not in anotado:
        q.append(f"no se anotó {esperado['anota']!r}: se anotó {sorted(set(anotado))}")
    return q


def correr_evals(verboso=True):
    """Los 10 casos, sobre un registro desviado. Devuelve `(rojas, eventos)`.

    ⚠️ Devuelve los EVENTOS que se anotaron, no la ruta del temporal. Es el
       arreglo del bicho de hoy llevado hasta el final: si devolviera la ruta,
       quien la recibe tendría en la mano un camino que **ya no está enchufado
       a nada** — y ese fue exactamente el error. **Un recurso que solo vale
       dentro de un `with` no debe salir de él.**
    """
    rojas = []
    import agente
    cliente_real = agente.cliente
    agente.cliente = _ClienteTrampa()
    try:
        with desviar() as tmp:
            if verboso:
                print("=== F.2 · la costura entre las dos capas ===" + chr(10))
            for etiqueta, modo, montaje, esperado in CASOS:
                try:
                    subio, cont, bajo, anotado = correr_caso(montaje, tmp)
                except LlegoALaRed as fallo:
                    quejas = [f"REVENTÓ: {fallo}"]
                except Exception as fallo:
                    quejas = [f"REVENTÓ: {type(fallo).__name__}: {fallo}"]
                else:
                    quejas = revisar(subio, cont, bajo, anotado, esperado)
                if quejas:
                    rojas.append(etiqueta)
                if verboso:
                    marca = "ok   " if not quejas else "FALLA"
                    print(f"{marca} [{modo:22}] {etiqueta}")
                    for x in quejas:
                        print(f"        -> {x}")
            eventos = _eventos(tmp)
    finally:
        agente.cliente = cliente_real

    if verboso:
        print(chr(10) + f"{len(CASOS)} casos, {len(rojas)} fallaron")
    return rojas, eventos


# ---------------------------------------------------------------------------
#  EL CATÁLOGO — y es la mitad que vale de F.2
# ---------------------------------------------------------------------------
#
#  🕵️ LA DEFENSA CONTRA EL SOSPECHOSO DEL DÍA, Y ESTÁ AQUÍ.
#     El sospechoso: *el que escribe el eval es el que decide qué cuenta como
#     «modo de falla propio del multi-agente»* — y puede elegir la lista para
#     que salga cubierta. Dos defensas, y las dos son comprobables:
#
#       1. La lista NO sale de mi cabeza: sale de los modos ya medidos **con
#          fecha** en el README de este nivel, y se cruza contra los eventos
#          que el harness ya sabe emitir (`P4`).
#       2. **Los HUECOS se escriben.** Un modo sin eval aparece como `HUECO`
#          con su motivo, no se calla. `P5` exige que ninguno diga «pendiente»
#          sin decir POR QUÉ.
#
#  🔑 Y esto es lo que separa un catálogo de una lista de deseos: un catálogo
#     dice también lo que NO cubre. Una lista de lo cubierto siempre está
#     completa — se completa borrando lo que falta.

#  Cada fila: (modo, qué es, ¿solo con dos capas?, dónde se mide HOY)
CATALOGO = [
    # --- Los ocho que este archivo mide ---------------------------------
    ("contrato_ok", "el contrato completo cruza la frontera",
     True, "eval F.2"),
    ("contrato_incompleto", "un dato se pierde al cruzar y sube declarado (A.3)",
     True, "eval F.2"),
    ("contrato_discrepa", "el contrato contesta OTRA pregunta (C.3)",
     True, "eval F.2 + presupuesto.py"),
    ("causa_correcta", "arriba sube una causa que no es la real (sesión 99)",
     True, "eval F.2 + presupuesto.py"),
    ("corte_vueltas", "el worker agota vueltas y su motivo cruza",
     True, "eval F.2"),
    ("parcial_se_tira", "se descarta una respuesta correcta (C.4, ABIERTO)",
     True, "eval F.2 — y la conducta está en revisión, no bendecida"),
    ("sin_trozo", "el modelo pidió un especialista de más (C.2)",
     True, "eval F.2 + presupuesto.py"),
    ("factura_por_capa", "el coste de abajo no llega arriba (B.2)",
     True, "eval F.2"),
    ("motivo_en_el_detalle", "`ok=False` sin causa en el detalle (C.2)",
     True, "eval F.2"),
    ("origen_declarado", "quién escribió el encargo (F.1)",
     True, "eval F.2 + presupuesto.py"),

    # --- Los que se miden en otro sitio, y por eso NO se duplican aquí ----
    # 🔑 Esto es la apuesta 1 del día en forma de tabla: F.2 nació rodeada de
    #    433 `check()`, y su trabajo no era escribir el caso 434 sino decir
    #    quién tiene cada modo.
    ("recursion_sin_tope", "un agente que se llama a sí mismo sin fondo (C.5)",
     True, "recursion.py (28 comprobaciones)"),
    ("worker_revienta", "un worker se cae y no debe tumbar a los otros dos (D)",
     True, "fallos.py (27 comprobaciones)"),
    ("plazo_de_pared", "un worker colgado deja un residuo de minutos (C.4)",
     True, "fallos.py + worker.py"),
    ("traza_sin_padre", "una línea no sabe de quién es hija (C.1)",
     True, "traza.py (47 comprobaciones)"),
    ("atribucion", "un FALLA no dice de QUIÉN es (F.1)",
     True, "atribuidor.py (34 comprobaciones)"),

    # --- 🚨 LOS HUECOS. Van en la misma tabla, no en una nota al pie -------
    ("enrutado_torcido",
     "HUECO — el euro se manda al worker del dólar (medido en la sesión 95). "
     "NO PUEDE tener un eval determinista: quien elige el destino es el "
     "modelo, y clavarlo a mano sería medir mi mano. Lo mide F.3, pagando.",
     True, "HUECO"),
    ("orquestador_no_publica",
     "HUECO — el worker entregó bien y arriba no salió. `atribuidor.py` sabe "
     "marcarlo, pero sobre datos reales ha salido CERO veces: hacen falta dos "
     "capas corriendo el duelo. Lo mide F.3.",
     True, "HUECO"),
    ("aislamiento",
     "HUECO — ningún worker ve las otras dos monedas (A.4, casilla C4-DOLAR). "
     "No es un fallo del harness sino del esquema, así que no hay conducta que "
     "un eval determinista pueda exigir: lo califica el juez.",
     True, "HUECO"),
    ("registro_partido",
     "HUECO — dos `Lock()` distintos apuntando al mismo archivo parten una "
     "línea por dentro (declarado en la 106, MORDIÓ el 2026-08-24). Es deuda "
     "de E.1 y su arreglo es un candado por archivo, no un eval.",
     False, "HUECO"),
]

MODOS = {fila[0] for fila in CATALOGO}
HUECOS = {fila[0] for fila in CATALOGO if fila[3] == "HUECO"}

# Eventos que el harness sabe emitir y que este catálogo NO reclama, con la
# razón. Se escriben para que `P4` pueda exigir que la suma cuadre: sin esta
# lista, «los que faltan» sería un número sin dueño.
FUERA_DE_ALCANCE = {
    "llamada_api": "contabilidad, no fallo",
    "herramienta": "contabilidad, no fallo",
    "worker_inicio": "contabilidad, no fallo",
    "worker_fin": "contabilidad, no fallo",
    "orquestador_inicio": "contabilidad, no fallo",
    "orquestador_fin": "contabilidad, no fallo",
    "corrida_inicio": "contabilidad del router (B.3)",
    "corrida_fin": "contabilidad del router (B.3)",
    "pipeline_inicio": "contabilidad del pipeline (B.1)",
    "pipeline_fin": "contabilidad del pipeline (B.1)",
    "duelo_inicio": "contabilidad de la línea base",
    "duelo_fin": "contabilidad de la línea base",
    "exp1_fin": "instrumento de un experimento, no del esquema",
    "exp2_fin": "instrumento de un experimento, no del esquema",
    "exp3_fin": "instrumento de un experimento, no del esquema",
    "exp4_fin": "instrumento de un experimento, no del esquema",
    "cebo_creado": "instrumento de un experimento, no del esquema",
    "b5_sano": "instrumento de B.5",
    "b5_queja": "instrumento de B.5",
    "frontera": "instrumento de B.1",
    "verificacion": "instrumento de B.1",
    "supervision": "instrumento de D",
    "decision_router": "contabilidad del router (B.3)",
    "corte_presupuesto": "es `sin_trozo` visto desde el router",
    "error_temporal": "fallo de red, no del esquema de dos capas",
    "error_permanente": "fallo de red, no del esquema de dos capas",
    "router_fallo": "es `worker_revienta` visto desde el router",
    "supervision_fallo": "es `worker_revienta` visto desde el supervisor",
    "recursion_frenada": "el freno de `recursion_sin_tope`, ya reclamado",
}
# 🔑 `contrato_discrepa` y `sin_trozo` NO están aquí a propósito: los reclama un
#    modo del catálogo con el mismo nombre. Un nombre en las dos listas dejaría
#    a `P4` pasando por el sitio equivocado — verde por estar clasificado dos
#    veces en vez de por estarlo una.
assert not (set(FUERA_DE_ALCANCE) & MODOS), "un evento no puede estar en las dos listas"


def eventos_que_sabe_emitir():
    """Los `anotar("…")` de todo el nivel, leídos del código fuente.

    ⚠️ Es un instrumento GRUESO y se dice aquí: lee texto, no código. Si
       alguien anota con una variable en vez de un literal, esto no lo ve.
       Se usa para que nadie AÑADA un evento sin pasar por el catálogo — no
       como censo definitivo. (`LM.99`: un detector de texto lee texto.)
    """
    import re
    fuera = set()
    for f in sorted(AQUI.glob("*.py")):
        if f.name == Path(__file__).name:
            continue          # este archivo nombra eventos para hablar de ellos
        fuera |= set(re.findall(r'anotar\("([a-z_0-9]+)"', f.read_text(encoding="utf-8")))
    return fuera


# ---------------------------------------------------------------------------
#  LAS PRUEBAS — y la que importa es la de MUTACIÓN
# ---------------------------------------------------------------------------

def _pruebas():
    fallos = []

    def check(nombre, cond, detalle=""):
        print(("  OK  " if cond else "  XX  ") + nombre + (f"  -> {detalle}" if detalle else ""))
        if not cond:
            fallos.append(nombre)

    print("\n[F.2] pruebas de los evals\n")

    # --- P1-P3: el contrato del archivo ------------------------------------
    check("P1 · todo caso declara un modo que existe en el catálogo",
          all(modo in MODOS for _, modo, _, _ in CASOS),
          str({m for _, m, _, _ in CASOS} - MODOS))

    check("P2 · ningún caso mide un modo declarado HUECO",
          not ({m for _, m, _, _ in CASOS} & HUECOS),
          "un hueco con eval no es un hueco: o se borra la fila o se borra el caso")

    check("P3 · las etiquetas no se repiten",
          len({e for e, _, _, _ in CASOS}) == len(CASOS))

    # --- P4: 🚨 el catálogo no se queda atrás cuando nace un evento --------
    #     Si mañana alguien escribe `anotar("cosa_nueva")` y no la clasifica,
    #     esta se pone roja. Es la defensa 1 del sospechoso, en código.
    sabe = eventos_que_sabe_emitir()
    sin_clasificar = sorted(sabe - set(FUERA_DE_ALCANCE) - MODOS)
    check("P4 · todo evento que el harness sabe emitir está clasificado",
          not sin_clasificar,
          f"sin clasificar: {sin_clasificar}" if sin_clasificar
          else f"{len(sabe)} eventos, todos con dueño o con razón")

    # --- P5: 🚨 los huecos se explican, no se aplazan ----------------------
    #     «Pendiente» sin motivo es una promesa; con motivo es una decisión.
    sin_motivo = [m for m, que, _, d in CATALOGO
                  if d == "HUECO" and len(que) < 60]
    check("P5 · cada HUECO dice POR QUÉ lo es, no solo que lo es",
          not sin_motivo, str(sin_motivo))

    check("P6 · hay huecos declarados (un catálogo sin huecos miente)",
          len(HUECOS) >= 3, f"{len(HUECOS)} huecos")

    # --- P7: la trampa de red MUERDE ---------------------------------------
    #     LM.13: un freno que no has visto morder es una nota.
    revento = False
    try:
        _ClienteTrampa().messages.create(model="x")
    except LlegoALaRed:
        revento = True
    check("P7 · MUERDE: la trampa de red revienta si alguien llama al modelo",
          revento, "sin esto, el $0,00 sería una promesa")

    # --- P8: los evals corren en verde -------------------------------------
    rojas, _ = correr_evals(verboso=False)
    check("P8 · los 10 casos pasan", not rojas, str(rojas))

    # --- P9: 🚨 LA PRUEBA QUE VALE — CADA CASO SE VE MORDER ----------------
    #
    #  Un eval que nace todo verde no ha demostrado NADA: puede estar mirando
    #  hacia otro lado. Aquí se rompe la conducta que cada caso mide y se exige
    #  que ESE caso se ponga rojo.
    #
    #  🔑 Y la mutación se hace sobre lo que el WORKER devuelve, no sobre el
    #     código del orquestador: así se prueba que el eval mira la costura, que
    #     es justo lo que dice medir.
    mutaciones = {
        # modo                 -> qué se le rompe al resultado del worker
        "contrato_ok":          {"datos": {"tasa": None}, "faltan": ["tasa"]},
        "contrato_incompleto":  {"faltan": []},
        "contrato_discrepa":    {"discrepa": []},
        "causa_correcta":       {"motivo": "discrepancia"},
        "corte_vueltas":        {"motivo": "presupuesto"},
        "parcial_se_tira":      {"ok": True, "motivo": None},
        "factura_por_capa":     {"coste_usd": 0.0},
        "motivo_en_el_detalle": {"motivo": None},
        # ⚠️ `origen_declarado` NO se muta tocando el resultado del worker: se
        #    muta cambiando LA ENTRADA del orquestador. Con `encargos` puesto,
        #    el encargo pasa a ser el de C.2 y `origen` baja como `experimento`
        #    en vez de `plantilla` — así que el caso tiene que ponerse rojo.
        # 🚨 Y esto se escribe porque la primera versión hacía TRAMPA: rompía el
        #    diccionario observado justo antes de compararlo. Eso no prueba que
        #    el eval mire el sistema — prueba que `revisar()` sabe restar.
        #    **Una mutación que toca la observación en vez del sistema siempre
        #    muerde, y no dice nada.**
        "origen_declarado":     "ENTRADA",
    }
    mordieron, mudos = [], []
    with desviar() as tmp2:
        for etiqueta, modo, montaje, esperado in CASOS:
            if modo not in mutaciones:
                continue
            roto = {"worker": dict(montaje["worker"]), "extra": dict(montaje["extra"])}
            if modo == "origen_declarado":
                roto["extra"]["encargos"] = presupuesto.ENCARGOS_DESIGUALES
            else:
                roto["worker"].update(mutaciones[modo])
            subio, cont, bajo, anotado = correr_caso(roto, tmp2)
            quejas = revisar(subio, cont, bajo, anotado, esperado)
            (mordieron if quejas else mudos).append(modo)

    check("P9 · MUERDEN: al romper la conducta, cada caso se pone rojo",
          not mudos, f"se quedaron mudos: {mudos}" if mudos
          else f"{len(mordieron)} de {len(mordieron)} mordieron")

    # --- P10: el `sin_trozo` no llega tarde --------------------------------
    #     Es el único caso donde la conducta correcta es NO llamar al worker.
    #     Si el rechazo llegara después, ya se habría pagado la corrida.
    #
    # 🐛 Y AQUÍ MORDIÓ `LM.20` OTRA VEZ, EN EL ARCHIVO QUE LO SABÍA.
    #    La primera versión pasaba el `tmp` que devuelve `correr_evals`… que ya
    #    no está enchufado a nada: esa función RESTAURA las rutas en su
    #    `finally`. Así que esta línea escribía tres `sin_trozo` en el
    #    **registro pagado**, y lo hacía un archivo cuya cabecera promete que
    #    no toca el registro pagado.
    # 🔑 Un `tmp` que sigue existiendo como variable después de que su montaje
    #    se deshizo **parece** válido: no da error, no avisa, y apunta a un
    #    archivo real que ya nadie mira. → `desviar()` es el arreglo en el
    #    ORIGEN: aquí ya no se puede escribir fuera del temporal.
    with desviar() as tmp_p10:
        _, _, bajo, _ = correr_caso(
            {"worker": {}, "extra": {"reparto": _RepartoSinSitio()}}, tmp_p10)
    check("P10 · con el reparto lleno, al worker NO se le llega a llamar",
          bajo is None, "si se llamara, el rechazo costaría dinero")

    # --- P11: 🔒 el registro pagado no se toca -----------------------------
    pagados = [AQUI / f"registro_{n}_claude-haiku-4-5.jsonl"
               for n in ("workers", "orquestador")]
    tam = {p.name: p.stat().st_size for p in pagados if p.exists()}
    correr_evals(verboso=False)
    igual = all(p.stat().st_size == tam[p.name] for p in pagados if p.exists())
    check("P11 · correr los evals NO escribe ni un byte en el registro pagado",
          igual and len(tam) == 2, str(tam))

    # --- P12: el registro desviado sí recibió, o el P11 no prueba nada -----
    #     🔑 Sin esto, `P11` estaría verde también si los evals no anotaran
    #        nada en absoluto. Un «no ensució» solo vale si algo se escribió.
    _, eventos = correr_evals(verboso=False)
    check("P12 · ...y el registro desviado SÍ recibió líneas",
          len(eventos) > 0,
          f"{len(eventos)} eventos en el temporal: {sorted(set(eventos))}")

    print(f"\n  → {len(fallos)} en rojo." if fallos else "\n  → todas verdes.")
    return fallos


def informe_catalogo():
    """La tabla, para leerla. Es la salida que un humano se lleva de F.2."""
    print("\n" + "=" * 78)
    print("[F.2] CATÁLOGO DE MODOS DE FALLA DEL MULTI-AGENTE")
    print("=" * 78)
    con_eval = [f for f in CATALOGO if f[3].startswith("eval F.2")]
    otros = [f for f in CATALOGO if not f[3].startswith("eval F.2") and f[3] != "HUECO"]
    huecos = [f for f in CATALOGO if f[3] == "HUECO"]

    print(f"\n  MEDIDOS AQUÍ ({len(con_eval)}):")
    for m, que, _, d in con_eval:
        print(f"     {m:22} {que}")
    print(f"\n  MEDIDOS EN OTRO SITIO ({len(otros)}) — no se duplican:")
    for m, que, _, d in otros:
        print(f"     {m:22} {d}")
        print(f"     {'':22} {que}")
    print(f"\n  🚨 HUECOS DECLARADOS ({len(huecos)}):")
    for m, que, _, _ in huecos:
        print(f"     {m}")
        for linea in _envolver(que.replace("HUECO — ", ""), 68):
            print(f"        {linea}")

    sabe = eventos_que_sabe_emitir()
    print(f"\n  eventos que el harness sabe emitir: {len(sabe)}")
    print(f"  reclamados por un modo del catálogo: {len(sabe & MODOS)}")
    print(f"  fuera de alcance, con razón escrita:  {len(sabe & set(FUERA_DE_ALCANCE))}")
    print("\n  ⚠️ Recuerda lo de la cabecera: esto mide el DETECTOR, no el")
    print("     DEFECTO. Verde aquí = «cuando se tuerce, no pasa de la costura».")
    print("     NO significa que no se tuerza. Eso lo mide F.3, pagando.")


def _envolver(texto, ancho):
    palabras, linea, fuera = texto.split(), "", []
    for p in palabras:
        if len(linea) + len(p) + 1 > ancho:
            fuera.append(linea)
            linea = p
        else:
            linea = (linea + " " + p).strip()
    if linea:
        fuera.append(linea)
    return fuera


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--catalogo":
        informe_catalogo()
    else:
        rojas, _ = correr_evals()
        fallidas = _pruebas()
        informe_catalogo()
        # LM.94: el resultado de las pruebas llega a quien arrancó el proceso.
        sys.exit(1 if (rojas or fallidas) else 0)
