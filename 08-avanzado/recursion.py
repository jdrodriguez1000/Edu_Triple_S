"""recursion.py — C.5 del nivel 8: LA PELOTA.

    LA PREGUNTA DE C.5, EN UNA FRASE

Un orquestador llama a un worker. ¿Y si el worker es otro orquestador? ¿Y si
ese llama a otro? **Dos agentes pueden pasarse la pelota para siempre**, y cada
pase es una llamada al modelo que se paga.

⚠️ LA TRAMPA DE HOY ES LA DE C.4, PERO PEOR, PORQUE AQUÍ HAY DOS FRENOS Y LOS
   DOS PARECEN VALER:

     `max_vueltas`   -> «el bucle no puede dar vueltas infinitas»
     el presupuesto  -> «cuando se acabe el dinero, para»

   Los dos existen, los dos están medidos, y los dos cierran corridas de verdad
   todos los días. **Este archivo va a preguntarles si paran ESTA.** Es `LM.13`:
   un freno que no has visto morder *en este caso* es una nota sobre este caso.

🚨 Y ES LA ANTESALA DE LA QUE HABLÓ LA SESIÓN 102 AL CERRAR C.4b: *un reintento
   que nadie acota es la pelota de C.5 un turno antes.* Allí se acotó con
   dinero. Hoy se le pregunta al dinero si era el freno correcto.


    ESTE PASO NO PAGA UN CENTAVO, Y ES LA MISMA MITAD DEL DISEÑO QUE EN C.4

El modelo es de mentira: `ClienteQueDelega` pide siempre delegar. Todo lo demás
es de verdad — el bucle de `correr_orquestador`, la frontera, la contabilidad,
el registro, el árbol y el reparto del dinero.

🔑 Lo falso es el que habla, no el harness. Y aquí importa más que en C.4: un
   modelo de verdad se cansaría de delegar, o no, y no sabríamos cuál de las dos
   cosas estamos midiendo. **Un modelo que SIEMPRE delega es el peor caso, y el
   peor caso es lo único contra lo que se puede dimensionar un freno.**


    ══════════════════════════════════════════════════════════════════════
    🔒 LAS CINCO APUESTAS, SELLADAS ANTES DE CORRER NADA
    ══════════════════════════════════════════════════════════════════════

    Escritas antes de la primera medición, como manda `LM.61`. Se abren abajo,
    en `_pruebas()`, **fila por fila**: la que falle se deja escrita fallada.

    1. La pelota sin freno NO la para ningún freno del harness. Lo que la para
       es Python quedándose sin pila, y eso llega **como una avería del
       programa**, no como una decisión del agente.

    2. `max_vueltas` no frena NADA aquí. Predicción falsable: en la corrida sin
       freno, **ninguna** capa cierra con `motivo="max_vueltas"`. El motivo es
       que cada capa nueva estrena su contador en cero: `max_vueltas` cuenta a lo
       ANCHO y la pelota crece a lo HONDO.

    3. El presupuesto SÍ para la pelota —el dinero se parte al bajar, así que se
       acaba—, y para **mucho antes** que Python. Pero cierra con
       `motivo="presupuesto"`, que es un diagnóstico FALSO: no es que el encargo
       fuera caro, es que hay un bucle. Y el consejo que se deduce de ese
       diagnóstico —«dale más presupuesto»— es exactamente el peor posible.

    4. Una capa de agente cuesta **dos** escalones de `profundidad`, no uno: la
       herramienta y la capa. O sea que el campo `profundidad` de C.1 **no cuenta
       capas**, y un tope escrito contra él mediría otra cosa.

    5. El tope por profundidad y el tope por repetición NO cazan lo mismo. Existe
       una topología legítima de tres capas —la de B.5, medida y pagada— a la que
       un tope de profundidad estrecho mata y a la que el de repetición deja
       pasar sin decir nada.

    ══════════════════════════════════════════════════════════════════════
"""

import contextlib
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "05b-proyecto"))

import agente          # noqa: E402
import contexto        # noqa: E402
import fallos          # noqa: E402
import orquestador     # noqa: E402
import presupuesto     # noqa: E402


# ---------------------------------------------------------------------------
# 1) LOS TOPES — y cuál de los dos es un freno y cuál un instrumento
# ---------------------------------------------------------------------------

# ⭐ EL FRENO DE VERDAD: cuántas CAPAS DE AGENTE pueden estar abiertas a la vez.
#    Tres, porque tres es lo que llegó a usar el nivel: B.5 tiene orquestador,
#    intermediario y worker. Un tope que mata la topología más grande que ya
#    corriste no es un freno: es una avería.
TOPE_CAPAS = 3

# 🔬 ESTO NO ES UN FRENO, ES UN INSTRUMENTO DE LABORATORIO, y se dice aquí para
#    que nadie lo confunda con el de arriba. Sirve para medir una pelota SIN
#    freno sin colgar la máquina. Un experimento que no termina no es un
#    experimento.
TOPE_LABORATORIO = 40


class PelotaSinFin(BaseException):
    """El corte del laboratorio. Hereda de `BaseException` A PROPÓSITO.

    🚨 Y ESTA HERENCIA ES UN HALLAZGO DE C.5, NO UNA MANÍA DE PYTHON.
       `ejecutar_un_bloque` tiene un `except Exception` en la frontera — la red
       de seguridad de C.4, la que impide que un worker caído tumbe a los otros
       dos. Esa red **se traga cualquier cosa que suba desde abajo**, incluido un
       aviso de «esto no para nunca», y lo convierte en un `tool_result` que dice
       *«falló, no lo llames otra vez igual»*… tras lo cual el modelo llama otra
       vez, porque el que decide es él.
    🔑 Un instrumento que mide la pelota tiene que poder ESCAPAR de la red que la
       hace posible. Se mide abajo, en `red_se_traga_el_aviso()`.
    """


# ---------------------------------------------------------------------------
# 2) EL MODELO DE MENTIRA — el que siempre delega
# ---------------------------------------------------------------------------

class _Texto:
    """Un bloque de texto como el que devuelve la API."""

    def __init__(self, texto):
        self.type = "text"
        self.text = texto


class ClienteQueDelega:
    """Pide `delegar` una vez por capa y, con la respuesta en la mano, cierra.

    ⭐ UNA sola delegación por capa, y es una decisión de medida, no de comodidad.
       Si delegara varias veces por capa, la pelota crecería a lo ancho Y a lo
       hondo a la vez, y al ver el número final no sabríamos cuál de las dos
       cosas lo hizo crecer. **Se mide la profundidad sola.**

    📌 Cómo sabe que ya delegó: mira si el último mensaje trae `tool_result`. No
       lleva contador propio — y no puede llevarlo, porque este mismo objeto
       atiende a TODAS las capas. Un contador aquí contaría la corrida entera, no
       la capa.
    """

    def __init__(self, entrada=1200, salida=150):
        self.entrada = entrada
        self.salida = salida
        self.llamadas = 0
        self.messages = type("_M", (), {})()
        self.messages.create = self._create

    def _create(self, **kw):
        self.llamadas += 1
        mensajes = kw.get("messages", [])
        ultimo = mensajes[-1] if mensajes else None
        contenido = ultimo.get("content") if isinstance(ultimo, dict) else None
        ya_delego = isinstance(contenido, list) and any(
            isinstance(b, dict) and b.get("type") == "tool_result" for b in contenido)

        if ya_delego:
            return fallos._Respuesta("end_turn", [_Texto("listo, ya delegué")],
                                     self.entrada, self.salida)
        return fallos._Respuesta(
            "tool_use",
            [fallos._Bloque("delegar", {"encargo": "sigue tú"},
                            f"b{self.llamadas}")],
            self.entrada, self.salida)


# ---------------------------------------------------------------------------
# 3) LA TOPOLOGÍA ESPEJO — una capa cuya herramienta es una capa igual
# ---------------------------------------------------------------------------
#
# ⭐ AQUÍ NO HAY NADA NUEVO, Y ESO ES EXACTAMENTE EL PELIGRO.
#    No hace falta escribir código raro para fabricar una pelota: basta con
#    `correr_orquestador` llamándose a sí mismo por la puerta que B.5 le abrió
#    —`sistema`, `tools`, `funciones`—. La recursión no es una avería que se
#    cuela: **es lo que pasa por defecto cuando una capa puede abrir capas.**

NOMBRE_CAPA = "coordinador"

SISTEMA_ESPEJO = (
    "Eres un coordinador. Para cualquier encargo, llama a `delegar` una vez y "
    "usa lo que te devuelva. Responde en español."
)

TOOLS_ESPEJO = [
    {
        "name": "delegar",
        "description": "Pasa el encargo a otro coordinador y devuelve su respuesta.",
        "input_schema": {
            "type": "object",
            "properties": {"encargo": {"type": "string"}},
            "required": ["encargo"],
        },
    },
]


def capas_abiertas(cadena=None):
    """Cuántas CAPAS DE AGENTE hay abiertas ahora mismo.

    🚨 NO ES `profundidad`, Y ÉSA ES LA APUESTA 4. El campo `profundidad` de C.1
       cuenta escalones del árbol, y de una capa a la siguiente hay DOS: el tramo
       de la herramienta (`tool:delegar`) y el de la capa (`capa:coordinador`).
       Un tope escrito contra `profundidad` diría «3» y dejaría pasar capa y
       media.
    🔑 El árbol de C.1 se dibujó para LEERSE después; este número se pregunta
       para DECIDIR ahora. El mismo dato no sirve para las dos cosas sin
       traducirlo, y traducirlo es esta función.
    """
    cadena = contexto.cadena() if cadena is None else cadena
    return sum(1 for n in cadena if n.startswith("capa:"))


def freno_de_recursion(nombre=NOMBRE_CAPA, tope=TOPE_CAPAS):
    """¿Se puede abrir una capa más? `None` si sí; el error a devolver si no.

    ⭐ SON DOS TOPES Y NO UNO, Y NO MIDEN LO MISMO:

         REPETICIÓN  -> ¿ya hay una capa con este nombre abierta encima de mí?
                        Es un tope de IDENTIDAD. Caza la pelota A→B→A aunque sea
                        cortísima.
         PROFUNDIDAD -> ¿cuántas capas hay abiertas en total?
                        Es un tope de FORMA. Caza la escalera A→B→C→D→… aunque no
                        se repita ni un nombre.

    🔑 Y EL ORDEN IMPORTA: primero la repetición. Las dos pararían la corrida,
       pero **dan diagnósticos distintos**, y el de la repetición es más preciso:
       dice *estás dentro de ti mismo*, no *bajaste mucho*. Al revés, una pelota
       que llega al tope se reportaría como «demasiadas capas», que invita a
       subir el tope — y subir el tope de una pelota sólo la hace más cara. Es la
       lección de C.4b: **el consejo cambia con las circunstancias; el
       diagnóstico, no.**

    ⚠️ Y ESTO DEVUELVE UN DICCIONARIO, NO LANZA UNA EXCEPCIÓN. A propósito: una
       excepción lanzada aquí se la come el `except Exception` de la frontera
       (ver `PelotaSinFin`). El freno tiene que salir por el mismo camino por el
       que sale un resultado — que es lo que C.4 midió que funcionaba.
    """
    cadena = contexto.cadena()
    abiertas = capas_abiertas(cadena)
    if f"capa:{nombre}" in cadena:
        return {
            "error": f"Ya hay un '{nombre}' trabajando en este mismo encargo más "
                     f"arriba: delegar otra vez sería pedírtelo a ti mismo. "
                     f"Contesta con lo que tengas. NO reintentes.",
            "pelota": True,
            "causa": "repeticion",
            "capas": abiertas,
        }
    if abiertas >= tope:
        return {
            "error": f"Este encargo ya lleva {tope} capas de agentes encima. "
                     f"No delegues más: resuélvelo o di que no puedes. "
                     f"NO reintentes.",
            "pelota": True,
            "causa": "profundidad",
            "capas": abiertas,
        }
    return None


def _sumar_a_la_factura(contabilidad, hijo, nombre):
    """Sube a la capa de arriba lo que gastó la de abajo. Igual que en A.3."""
    with orquestador._CANDADO_CONTABILIDAD:
        contabilidad["workers"] += 1
        contabilidad["coste_workers_usd"] += hijo["coste_total_usd"]
        contabilidad["llamadas_api_workers"] += (hijo["llamadas_api_orquestador"]
                                                 + hijo["llamadas_api_workers"])
        contabilidad["detalle"].append({
            "worker": nombre,
            "ok": hijo["ok"],
            "motivo": hijo["motivo"],
            "vueltas": hijo["vueltas"],
            "coste_usd": hijo["coste_total_usd"],
            "capas": capas_abiertas(),
        })


# ⭐ LA CONFIGURACIÓN DEL LABORATORIO, EN UN SITIO Y NO EN LA FIRMA.
#
# 🐛 Y ESTO NACIÓ DE UN FALLO MÍO, CAZADO EN LA PRIMERA MEDICIÓN DE LA SESIÓN 103.
#    La versión anterior recibía `tope` y `laboratorio` como argumentos de esta
#    función. Se veía correcta y era ciega: **quien llama a la herramienta es
#    `ejecutar_un_bloque`, y le pasa exactamente los argumentos que el modelo
#    pidió — `encargo`, y nada más.** Los topes se quedaban en su valor por
#    defecto en cuanto bajaba una capa. Un tope que se configura arriba y no
#    viaja hacia abajo **no es un tope: es una variable local con nombre de
#    freno.**
# 🔑 Y cómo se cazó importa más que el fallo: los experimentos 1 y 2 dieron
#    números IDÉNTICOS —40 capas, 78 de profundidad, el mismo corte— cuando el 2
#    existía justamente para dar otro. Es `LM.15` con otra cara: el instrumento
#    ciego no dio silencio, dio **el mismo número dos veces**, que se lee como
#    confirmación en vez de como avería.
# 📌 La forma es la de `profundidad.ENRUTADO_FORZADO`: un ajuste del laboratorio
#    que se enciende y se apaga en un `finally`, no un parámetro del diseño.
_CONFIG = {
    "con_freno": True,
    "tope": TOPE_CAPAS,
    "laboratorio": TOPE_LABORATORIO,
}


@contextlib.contextmanager
def configurado(**kw):
    """Cambia el laboratorio mientras dure el `with`, y lo devuelve al salir."""
    antes = dict(_CONFIG)
    _CONFIG.update(kw)
    try:
        yield _CONFIG
    finally:
        _CONFIG.clear()
        _CONFIG.update(antes)


def herramienta_delegar(encargo, contabilidad, verboso=True):
    """La frontera de C.5: abre otra capa igual a la que la llamó.

    Compárala con `orquestador.herramienta_consultar_moneda`: es la misma función
    con `correr_orquestador` donde aquélla tiene `correr_worker`. **Esa única
    palabra es toda la diferencia entre un árbol y una pelota.**
    """
    con_freno = _CONFIG["con_freno"]
    tope = _CONFIG["tope"]
    laboratorio = _CONFIG["laboratorio"]

    if con_freno:
        parado = freno_de_recursion(NOMBRE_CAPA, tope)
        if parado is not None:
            orquestador.anotar("recursion_frenada",
                               capa=contabilidad.get("capa", "?"),
                               causa=parado["causa"], capas=parado["capas"])
            return parado

    # 🔬 El corte del laboratorio. No es el freno: es lo que permite medir qué
    #    pasa cuando NO hay freno sin quedarse sin máquina.
    if capas_abiertas() >= laboratorio:
        raise PelotaSinFin(f"el laboratorio cortó en {laboratorio} capas")

    # --- El dinero, si lo hay. Es la MISMA línea que la frontera de C.2: se pide
    #     un trozo justo antes de arrancar al de abajo.
    reparto = contabilidad.get("reparto")
    presupuesto_hijo = None
    if reparto is not None:
        try:
            presupuesto_hijo = reparto.tomar(NOMBRE_CAPA)
        except presupuesto.SinTrozo as fallo:
            return {"error": str(fallo), "sin_trozo": True}

    hijo = orquestador.correr_orquestador(
        encargo,
        sistema=SISTEMA_ESPEJO,
        tools=TOOLS_ESPEJO,
        funciones=FUNCIONES_ESPEJO,
        nombre=NOMBRE_CAPA,
        verboso=verboso,
        presupuesto_encargo=presupuesto_hijo,
    )
    _sumar_a_la_factura(contabilidad, hijo, NOMBRE_CAPA)
    return {"respuesta": hijo["texto"], "ok": hijo["ok"], "motivo": hijo["motivo"]}


FUNCIONES_ESPEJO = {"delegar": herramienta_delegar}


@contextlib.contextmanager
def _delegando_con(fn):
    """Cambia la herramienta `delegar` mientras dure el `with`.

    📌 Hay UN solo puente y por eso basta con parchear uno. Cuando había dos
       —uno con freno y otro sin—, el espía se quedaba fuera en cuanto una capa
       bajaba por el otro diccionario. Ése fue el mismo fallo que `_CONFIG`:
       **una decisión del laboratorio que no viaja hacia abajo.**
    """
    real = FUNCIONES_ESPEJO["delegar"]
    FUNCIONES_ESPEJO["delegar"] = fn
    try:
        yield
    finally:
        # 🔒 En el `finally`, como `registro_desviado`. Un instrumento encendido
        #    de más contamina la prueba siguiente, no ésta.
        FUNCIONES_ESPEJO["delegar"] = real


# ---------------------------------------------------------------------------
# 4) EL LABORATORIO — correr la pelota y contar qué quedó
# ---------------------------------------------------------------------------

ENCARGO = "Prepara el informe de estas facturas."


def _resumen(lineas):
    """Lee el registro desviado y contesta las preguntas de C.5.

    🔑 Se lee EL REGISTRO y no la contabilidad devuelta, por un motivo que la
       propia pelota impone: cuando la corrida muere a media escalera **no
       devuelve nada**. La contabilidad se pierde con la pila; el registro ya
       está en el disco. Es C.1 cobrando en el peor caso, que es el único en el
       que un registro hace falta de verdad.
    """
    inicios = [d for d in lineas if d.get("evento") == "orquestador_inicio"]
    cierres = [d for d in lineas if d.get("evento") == "orquestador_fin"]
    llamadas = [d for d in lineas if d.get("evento") == "llamada_api"]
    frenadas = [d for d in lineas if d.get("evento") == "recursion_frenada"]

    motivos = {}
    for d in cierres:
        motivos[d.get("motivo")] = motivos.get(d.get("motivo"), 0) + 1

    return {
        "capas_abiertas": len(inicios),
        "capas_cerradas": len(cierres),
        "sin_cerrar": len(inicios) - len(cierres),
        "profundidad_max": max([d.get("profundidad", 0) for d in inicios] or [0]),
        "motivos": motivos,
        "llamadas_api": len(llamadas),
        "coste_usd": round(sum(d.get("costo_usd", 0.0) for d in llamadas), 6),
        "frenadas": [d.get("causa") for d in frenadas],
    }


def correr_pelota(con_freno, presupuesto_encargo=None, tope=TOPE_CAPAS,
                  laboratorio=TOPE_LABORATORIO, max_vueltas=8, callar=True):
    """Arranca la capa de arriba y devuelve el resumen de lo que quedó grabado.

    📌 El registro se desvía SIEMPRE. Ninguna línea de este archivo entra en los
       `.jsonl` pagados: aquella mezcla ya se pagó una vez en la sesión 97.
    """
    cliente = ClienteQueDelega()
    reventon = None
    arriba = None

    with orquestador.registro_desviado() as carpeta, \
            configurado(con_freno=con_freno, tope=tope, laboratorio=laboratorio):
        with fallos._ClienteFalso(cliente):
            # 🔇 El `except Exception` de la frontera imprime el traceback, y en
            #    una pelota de cuarenta capas eso son miles de líneas que tapan
            #    el resultado. Se calla el ruido, no el dato.
            real_err = sys.stderr
            if callar:
                sys.stderr = open(os.devnull, "w", encoding="utf-8")
            try:
                arriba = orquestador.correr_orquestador(
                    ENCARGO,
                    sistema=SISTEMA_ESPEJO,
                    tools=TOOLS_ESPEJO,
                    funciones=FUNCIONES_ESPEJO,
                    nombre=NOMBRE_CAPA + "-raiz",
                    verboso=False,
                    max_vueltas=max_vueltas,
                    presupuesto_encargo=presupuesto_encargo,
                )
            except PelotaSinFin as corte:
                reventon = f"PelotaSinFin: {corte}"
            except RecursionError as corte:
                reventon = f"RecursionError: {corte}"
            finally:
                if callar:
                    sys.stderr.close()
                    sys.stderr = real_err

        lineas = fallos._leer(carpeta)
        resumen = _resumen(lineas)

    resumen["reventon"] = reventon
    resumen["llamadas_al_modelo"] = cliente.llamadas
    resumen["lineas"] = lineas
    resumen["texto_de_arriba"] = (arriba or {}).get("texto")
    resumen["ok_de_arriba"] = (arriba or {}).get("ok")
    return resumen


def _imprimir(titulo, r, notas=()):
    print(f"\n{'-' * 72}\n  {titulo}\n{'-' * 72}")
    print(f"  capas abiertas ......... {r['capas_abiertas']}")
    print(f"  capas SIN cerrar ....... {r['sin_cerrar']}")
    print(f"  profundidad max (C.1) .. {r['profundidad_max']}")
    print(f"  llamadas al modelo ..... {r['llamadas_al_modelo']}")
    print(f"  motivos de cierre ...... {r['motivos'] or '—'}")
    print(f"  frenos que mordieron ... {r['frenadas'] or '—'}")
    print(f"  reventón ............... {r['reventon'] or '—'}")
    for n in notas:
        print(f"  {n}")


# --- Experimento 1: la pelota desnuda --------------------------------------

def pelota_sin_freno(verboso=True):
    """Sin freno de C.5, con los dos frenos VIEJOS puestos y funcionando."""
    r = correr_pelota(con_freno=False)
    if verboso:
        _imprimir("1 · LA PELOTA SIN FRENO — con `max_vueltas` puesto", r, [
            "📌 `max_vueltas=8` estaba activo en TODAS las capas.",
        ])
    return r


# --- Experimento 2: ¿y si quitamos hasta el corte del laboratorio? ----------

def pelota_hasta_el_final(verboso=True):
    """El laboratorio se sube tanto que quien corte tenga que ser Python.

    🚨 ESTE ES EL EXPERIMENTO QUE CONTESTA LA APUESTA 1, Y HAY QUE MIRAR DÓNDE
       SALE EL CORTE, no sólo si sale. `RecursionError` **es una `Exception`**,
       así que el `except Exception` de la frontera —la red de C.4— la puede
       atrapar igual que atrapa a un worker caído.
    """
    r = correr_pelota(con_freno=False, laboratorio=10 ** 9)
    if verboso:
        _imprimir("2 · SIN NI SIQUIERA EL CORTE DEL LABORATORIO", r, [
            f"texto final de arriba: {str(r['texto_de_arriba'])[:70]!r}",
            f"la corrida de arriba dice ok={r['ok_de_arriba']}",
        ])
    return r


# --- Experimento 3: el dinero ----------------------------------------------

def pelota_con_dinero(total_usd=presupuesto.PRESUPUESTO_ENCARGO_USD, verboso=True):
    """La misma pelota, con el presupuesto de encargo de C.2 repartiéndose."""
    r = correr_pelota(con_freno=False, presupuesto_encargo=total_usd)
    if verboso:
        _imprimir(f"3 · LA MISMA PELOTA CON ${total_usd:.6f} DE PRESUPUESTO", r, [
            f"gasto grabado ......... ${r['coste_usd']:.6f}",
            "🔑 Mira el MOTIVO de cierre, no si paró.",
        ])
    return r


# --- Experimento 3b: qué pasa si le haces caso al diagnóstico --------------

def mas_dinero_mas_pelota(verboso=True):
    """Se obedece al `motivo="presupuesto"`: se le da más dinero. Cuatro veces.

    🚨 ESTE ES EL EXPERIMENTO QUE CONVIERTE LA APUESTA 3 EN UNA LECCIÓN Y NO EN
       UNA QUEJA. Que el diagnóstico sea impreciso no bastaría para descartarlo:
       hay diagnósticos imprecisos y útiles. Éste hay que medirlo por lo que
       pasa **cuando alguien le hace caso**, que es lo único que un diagnóstico
       llega a provocar.
    """
    filas = []
    base = presupuesto.PRESUPUESTO_ENCARGO_USD
    for veces in (1, 10, 100, 1000):
        r = correr_pelota(con_freno=False, presupuesto_encargo=base * veces)
        filas.append((veces, base * veces, r))
    if verboso:
        print(f"\n{'-' * 72}\n  3b · SE OBEDECE EL DIAGNÓSTICO: MÁS PRESUPUESTO"
              f"\n{'-' * 72}")
        print(f"  {'x':>6}  {'presupuesto':>12}  {'capas':>6}  {'gasto':>10}  motivos")
        for veces, total, r in filas:
            print(f"  {veces:>6}  ${total:>11.6f}  {r['capas_abiertas']:>6}  "
                  f"${r['coste_usd']:>9.6f}  {r['motivos']}")
    return filas


# --- Experimento 4: cuántos escalones cuesta una capa ----------------------

def escalones_por_capa(verboso=True):
    """Mide la distancia real entre `profundidad` (C.1) y «capas» (C.5).

    Corre una pelota corta y apunta, en cada frontera, la cadena de tramos
    abiertos. La respuesta no se deduce: se mira.
    """
    visto = []
    real = FUNCIONES_ESPEJO["delegar"]

    def espia(encargo, contabilidad, verboso=True, **kw):
        visto.append(contexto.cadena())
        return real(encargo, contabilidad, verboso, **kw)

    with _delegando_con(espia):
        correr_pelota(con_freno=True, tope=TOPE_CAPAS)

    cadena = max(visto, key=len) if visto else ()
    donde = [i for i, n in enumerate(cadena) if n.startswith("capa:")]
    capas = len(donde)
    profundidad = len(cadena) - 1

    # 🐛 LA PRIMERA VERSIÓN DIVIDÍA `profundidad / capas` Y DABA **1,5**, que no
    #    es un número de escalones: es la media entre un salto de 2 y una cola
    #    suelta —el `tool:delegar` desde el que se está midiendo, que todavía no
    #    tiene su capa debajo—. El dato que hace falta es **la distancia entre
    #    una capa y la siguiente**, y esa se mide restando posiciones, no
    #    dividiendo totales.
    # 🔑 Es el mismo bicho que `LM.17` (un `md5` no dice «todo igual», dice «los
    #    bytes, iguales»): **el cociente contestaba una pregunta parecida a la
    #    que se hacía, y por eso el número salió creíble.** Lo cazó parecer raro,
    #    no una prueba.
    saltos = [b - a for a, b in zip(donde, donde[1:])]
    escalon = saltos[0] if saltos else 0

    if verboso:
        print(f"\n{'-' * 72}\n  4 · UNA CAPA, ¿CUÁNTOS ESCALONES?\n{'-' * 72}")
        print("  la cadena más larga que se vio abierta:")
        for i, n in enumerate(cadena):
            marca = "  <- capa" if n.startswith("capa:") else ""
            print(f"     profundidad {i}  ->  {n}{marca}")
        print(f"  capas de agente ........ {capas}")
        print(f"  profundidad (C.1) ...... {profundidad}")
        print(f"  saltos entre capas ..... {saltos}")
        print(f"  UN escalón de capa vale  {escalon} de `profundidad`")
    return {"cadena": cadena, "capas": capas, "profundidad": profundidad,
            "saltos": saltos, "escalon": escalon}


# --- Experimento 5: el freno de C.5 ----------------------------------------

def pelota_con_freno(verboso=True):
    r = correr_pelota(con_freno=True)
    if verboso:
        _imprimir("5 · LA MISMA PELOTA CON EL FRENO DE C.5", r, [
            f"texto final de arriba: {str(r['texto_de_arriba'])[:70]!r}",
        ])
    return r


# --- Experimento 6: la red de C.4 se traga el aviso ------------------------

def red_se_traga_el_aviso(verboso=True):
    """El contrafactual de `PelotaSinFin`: ¿y si el corte fuera un `Exception`?

    🔑 Es el mismo corte, en el mismo sitio, cambiando UNA palabra en la
       herencia. Si la red de C.4 se lo traga, la corrida sigue y termina
       diciendo que todo fue bien — que es la peor de las salidas posibles.
    """
    class _CorteNormal(Exception):
        pass

    def con_corte_normal(encargo, contabilidad, verboso=True, **kw):
        if capas_abiertas() >= 5:
            raise _CorteNormal("esto no para")
        return herramienta_delegar(encargo, contabilidad, verboso)

    with _delegando_con(con_corte_normal):
        r = correr_pelota(con_freno=False)

    if verboso:
        _imprimir("6 · EL MISMO CORTE, PERO COMO `Exception` CORRIENTE", r, [
            f"la corrida de arriba dice ok={r['ok_de_arriba']}",
            f"texto final: {str(r['texto_de_arriba'])[:70]!r}",
        ])
    return r


# --- Experimento 7: la topología legítima de B.5 ---------------------------

def b5_no_es_una_pelota(verboso=True):
    """Tres capas con nombres distintos: ¿las mata el freno? ¿Cuál de los dos?

    📌 Se simula la CADENA de B.5, no se corre B.5. Correrlo costaría dinero y el
       dato que hace falta es de forma, no de conducta: qué contesta el freno
       ante `orquestador → region → worker`. Las cadenas se abren de verdad con
       `contexto.tramo`, así que lo que se pregunta es el freno real.
    """
    respuestas = {}
    with contexto.tramo("capa:orquestador"):
        with contexto.tramo("tool:consultar_region"):
            with contexto.tramo("capa:region-norte"):
                with contexto.tramo("tool:consultar_moneda"):
                    respuestas["b5_tope3"] = freno_de_recursion("worker-usd", tope=3)
                    respuestas["b5_tope2"] = freno_de_recursion("worker-usd", tope=2)
                    # Y la pelota corta, en la MISMA cadena: un `orquestador`
                    # queriendo abrir otro `orquestador`.
                    respuestas["pelota_corta"] = freno_de_recursion("orquestador",
                                                                   tope=9)
    if verboso:
        print(f"\n{'-' * 72}\n  7 · B.5 (3 CAPAS LEGÍTIMAS) CONTRA LOS DOS TOPES\n"
              f"{'-' * 72}")
        for k, v in respuestas.items():
            print(f"  {k:14} -> {v['causa'] if v else 'PASA, sin una queja'}")
    return respuestas


# ---------------------------------------------------------------------------
# 5) LAS PRUEBAS — y aquí se abre el sobre, fila por fila
# ---------------------------------------------------------------------------

def _pruebas():
    import traza

    print("=" * 72)
    print("  C.5 — PRUEBAS. Coste: $0,000000")
    print("=" * 72)
    rojas = []

    def check(nombre, cond, detalle=""):
        print(f"  {'✅' if cond else '❌'} {nombre}")
        if detalle:
            print(f"       {detalle}")
        if not cond:
            rojas.append(nombre.split(".")[0])

    # --- 1 a 4 · EL INSTRUMENTO NUEVO: la cadena -----------------------------
    check("1. sin ningún tramo abierto, `cadena()` está vacía",
          contexto.cadena() == (), contexto.cadena())

    with contexto.tramo("capa:a"):
        with contexto.tramo("tool:t"):
            dentro = contexto.cadena()
    check("2. la cadena crece hacia dentro y se descuelga al salir",
          dentro == ("capa:a", "tool:t") and contexto.cadena() == (), dentro)

    # 🔒 Esta prueba NO es sobre C.5: vigila que C.1 no se movió al añadirle un
    #    campo. `marca()` es lo que baja al registro, y los registros pagados
    #    tienen que seguir teniendo exactamente los mismos cinco campos.
    with contexto.tramo("capa:a"):
        campos = sorted(contexto.marca())
    check("3. 🔒 `marca()` sigue bajando CINCO campos: `cadena` no entra al registro",
          campos == ["corrida", "id", "padre", "profundidad", "tramo"], campos)

    check("4. `capas_abiertas` cuenta capas, no tramos",
          capas_abiertas(("capa:a", "tool:t", "capa:b", "tool:t")) == 2)

    # --- 5 a 8 · EL FRENO, con sus dos topes ---------------------------------
    check("5. con la cadena vacía, el freno DEJA PASAR",
          freno_de_recursion("coordinador", tope=3) is None)

    with contexto.tramo("capa:coordinador"):
        con_repeticion = freno_de_recursion("coordinador", tope=99)
    check("6. 🚨 el tope de REPETICIÓN muerde aunque el de profundidad sobre",
          con_repeticion is not None and con_repeticion["causa"] == "repeticion",
          con_repeticion)

    with contexto.tramo("capa:a"):
        with contexto.tramo("capa:b"):
            with contexto.tramo("capa:c"):
                con_profundidad = freno_de_recursion("d", tope=3)
    check("7. 🚨 el tope de PROFUNDIDAD muerde sin que se repita un solo nombre",
          con_profundidad is not None
          and con_profundidad["causa"] == "profundidad", con_profundidad)

    with contexto.tramo("capa:x"):
        with contexto.tramo("capa:y"):
            with contexto.tramo("capa:x"):
                los_dos = freno_de_recursion("x", tope=3)
    check("8. ⭐ cuando aplican LOS DOS, gana el diagnóstico más preciso",
          los_dos["causa"] == "repeticion", los_dos["causa"])

    # =======================================================================
    #  EL SOBRE. Cinco apuestas, una fila cada una.
    # =======================================================================
    print("\n  " + "=" * 68)
    print("  🔒 EL SOBRE DE C.5 — sellado antes de la primera medición")
    print("  " + "=" * 68)

    sin_freno = correr_pelota(con_freno=False)
    hasta_el_final = correr_pelota(con_freno=False, laboratorio=10 ** 9)
    con_dinero = correr_pelota(con_freno=False,
                               presupuesto_encargo=presupuesto.PRESUPUESTO_ENCARGO_USD)
    con_freno = correr_pelota(con_freno=True)

    # --- APUESTA 2 (se abre antes que la 1: la 1 depende de mirar la 2) ------
    check("9. 🎲 APUESTA 2 — `max_vueltas` no frena NADA: cero cierres por vueltas",
          "max_vueltas" not in sin_freno["motivos"]
          and sin_freno["capas_abiertas"] == TOPE_LABORATORIO,
          f"{sin_freno['capas_abiertas']} capas abiertas · "
          f"motivos: {sin_freno['motivos'] or 'ninguno, no cerró ni una'}")

    check("10. ⭐ y el motivo se ve: la pelota no cerró NI UNA capa",
          sin_freno["sin_cerrar"] == sin_freno["capas_abiertas"],
          f"{sin_freno['sin_cerrar']} de {sin_freno['capas_abiertas']} sin cerrar")

    # --- APUESTA 1 · LA QUE FALLA -------------------------------------------
    con_error = [d for d in hasta_el_final["lineas"]
                 if d.get("evento") == "herramienta"
                 and isinstance(d.get("salida"), dict) and "error" in d["salida"]]
    check("11. 🔴 APUESTA 1 — FALLADA. Python SÍ corta… y la corrida dice `ok=True`",
          hasta_el_final["ok_de_arriba"] is True
          and hasta_el_final["reventon"] is None,
          f"{hasta_el_final['capas_abiertas']} capas · "
          f"{hasta_el_final['llamadas_al_modelo']} llamadas · "
          f"${hasta_el_final['coste_usd']:.6f} · ok={hasta_el_final['ok_de_arriba']}")

    check("12. 🚨 y del desastre entero queda UNA línea de registro",
          len(con_error) == 1
          and "defecto interno" in con_error[0]["salida"]["error"],
          f"1 de {len(hasta_el_final['lineas'])} líneas · "
          f"profundidad {con_error[0].get('profundidad') if con_error else '?'}")

    # --- APUESTA 3 -----------------------------------------------------------
    check("13. 🎲 APUESTA 3 — el dinero SÍ para la pelota, y muy pronto",
          con_dinero["capas_abiertas"] < sin_freno["capas_abiertas"]
          and con_dinero["sin_cerrar"] == 0,
          f"{con_dinero['capas_abiertas']} capas contra "
          f"{sin_freno['capas_abiertas']} sin presupuesto")

    check("14. 🚨 …y cierra con un diagnóstico FALSO: `presupuesto`, no `pelota`",
          "presupuesto" in con_dinero["motivos"] and con_dinero["frenadas"] == [],
          con_dinero["motivos"])

    # ⚠️ LA MITAD DEL ADJETIVO DE LA APUESTA 3, Y SE MIDE EN VEZ DE AFIRMARSE.
    #    La primera versión de esta prueba era `check(..., True, "medido en el
    #    experimento 3b")`: una prueba que no puede ponerse roja, o sea una nota
    #    con forma de prueba. Es `LM.13` cometido dentro del archivo que va sobre
    #    `LM.13`. Ahora corre el experimento y compara.
    escalera = mas_dinero_mas_pelota(verboso=False)
    capas_x1 = escalera[0][2]["capas_abiertas"]
    capas_x1000 = escalera[-1][2]["capas_abiertas"]
    check("15. ⚠️ APUESTA 3, LA MITAD DEL ADJETIVO: obedecer el diagnóstico NO "
          "dispara la pelota",
          capas_x1000 < 10 and capas_x1000 > capas_x1,
          f"x1 -> {capas_x1} capas · x1000 -> {capas_x1000} capas. Crece, pero "
          f"como el logaritmo: el reparto parte el dinero en cada escalón")

    # --- APUESTA 4 -----------------------------------------------------------
    esc = escalones_por_capa(verboso=False)
    check("16. 🎲 APUESTA 4 — una capa de agente vale DOS escalones de `profundidad`",
          esc["escalon"] == 2, f"saltos entre capas: {esc['saltos']}")

    check("17. ⭐ y por eso `profundidad` no sirve de tope: 40 capas -> 78",
          sin_freno["profundidad_max"] == 2 * (sin_freno["capas_abiertas"] - 1),
          f"{sin_freno['capas_abiertas']} capas -> profundidad "
          f"{sin_freno['profundidad_max']}")

    # --- APUESTA 5 -----------------------------------------------------------
    b5 = b5_no_es_una_pelota(verboso=False)
    check("18. 🎲 APUESTA 5 — las 3 capas legítimas de B.5 PASAN con el tope en 3",
          b5["b5_tope3"] is None)
    check("19. …y el mismo tope en 2 las MATA por profundidad",
          b5["b5_tope2"]["causa"] == "profundidad")
    check("20. ⭐ mientras la pelota corta cae por REPETICIÓN con el tope en 9",
          b5["pelota_corta"]["causa"] == "repeticion")

    # --- 21 a 24 · EL FRENO DE C.5, VISTO MORDER ----------------------------
    check("21. 🚨 CON el freno, la pelota para en el tope y la causa es la buena",
          con_freno["frenadas"] == ["repeticion"]
          and con_freno["capas_abiertas"] <= TOPE_CAPAS,
          f"{con_freno['capas_abiertas']} capas · {con_freno['frenadas']}")

    check("22. ⭐ y TODAS las capas cierran — el contrafactual de la prueba 10",
          con_freno["sin_cerrar"] == 0,
          f"{con_freno['sin_cerrar']} sin cerrar, contra "
          f"{sin_freno['sin_cerrar']} sin freno")

    tragado = red_se_traga_el_aviso(verboso=False)
    check("23. 🚨 el MISMO corte, como `Exception`, se lo traga la red de C.4",
          tragado["ok_de_arriba"] is True and tragado["reventon"] is None,
          f"{tragado['capas_abiertas']} capas y la corrida dice ok=True")

    check("24. ⭐ …y con `BaseException` el aviso SÍ sale — es la única diferencia",
          sin_freno["reventon"] is not None
          and "PelotaSinFin" in sin_freno["reventon"], sin_freno["reventon"])

    # --- 25 y 26 · LO QUE EL AUDITOR DE C.1 Y C.4 VE DE TODO ESTO ------------
    quejas = traza.auditar_arbol(sin_freno["lineas"])
    abiertos = [q for q in quejas if q["tipo"] == "nodo_abierto"]
    check("25. 🎁 el auditor de C.4 ve la pelota sin saber que existe: 40 abiertos",
          len(abiertos) == sin_freno["capas_abiertas"],
          f"{len(abiertos)} quejas `nodo_abierto` de "
          f"{sin_freno['capas_abiertas']} capas")

    quejas_ok = traza.auditar_arbol(con_freno["lineas"])
    check("26. …y con el freno puesto no tiene NINGUNA queja",
          quejas_ok == [], quejas_ok)

    print("-" * 72)
    if rojas:
        print(f"  ❌ {len(rojas)} prueba(s) en rojo: {rojas}")
    else:
        print("  ✅ las 26 pruebas, verdes, y no costaron nada.")
        print("     🔴 Y la 11 está verde COMPROBANDO QUE LA APUESTA 1 FALLÓ.")
        print("        Se deja así a propósito: una apuesta fallada se prueba,")
        print("        no se borra.")
    print("=" * 72)
    return not rojas


def main(argv):
    if "--pruebas" in argv:
        return 0 if _pruebas() else 1

    print("=" * 72)
    print("  C.5 — LA PELOTA, MEDIDA SIN PAGAR")
    print("=" * 72)
    pelota_sin_freno()
    pelota_hasta_el_final()
    pelota_con_dinero()
    mas_dinero_mas_pelota()
    escalones_por_capa()
    pelota_con_freno()
    red_se_traga_el_aviso()
    b5_no_es_una_pelota()
    print("\n📌 Coste de todo esto: $0,000000. El modelo era de mentira; el")
    print("   harness, no.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
