"""
Nivel 5 - Script 4: evals deterministas del HARNESS.

LA IDEA CENTRAL DE ESTE PASO
----------------------------
Tu agente son dos cosas pegadas, y se prueban de formas opuestas:

    EL MODELO            decide que herramienta pedir, escribe el texto
                         -> caro, lento, nunca igual dos veces
                         -> se prueba corriendo N veces y contando (scripts 1-3)

    EL HARNESS           presupuesto, permisos, timeouts, tope de vueltas,
                         registro, validacion
                         -> es codigo normal y corriente
                         -> se prueba con casos, GRATIS, con respuesta conocida

Los seis frenos del nivel 4 no tienen nada de probabilistico.
PRESUPUESTO_USD = 0.10 o corta o no corta. PERMISOS o deniega o no deniega.

    -> LA MITAD DE TU AGENTE SE PUEDE PROBAR SIN LLAMAR A LA API NI UNA VEZ.

Y se apoya en L4.14, que mediste tu mismo en el nivel 4: la infraestructura
SI es determinista aunque el modelo no lo sea.

QUE HUBO QUE ARREGLAR PARA PODER ESCRIBIR ESTO
----------------------------------------------
03_harness.py no tenia 'if __name__ == "__main__"'. Importarlo para probar
sus piezas lo arrancaba entero: creaba la caja, hacia las 3 preguntas,
gastaba los $0.03 y se quedaba esperando que alguien tecleara s/n.

    -> Para poder probar tu codigo, tiene que poder cargarse sin ejecutarse.

Es un defecto que solo aparece cuando intentas probar. Arreglado en la
sesion 8 (ver el docstring de main() alli).

COSTO: $0.00. Ni una llamada a la API.

USO:
    python 04_evals_harness.py
"""

import contextlib
import importlib.util
import io
import json
import sys
import tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# Cargamos el harness del nivel 4 como piezas, sin ejecutarlo.
_ruta = Path(__file__).resolve().parent.parent / "04-harness-real" / "03_harness.py"
_spec = importlib.util.spec_from_file_location("harness", _ruta)
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)


# ---------------------------------------------------------------------------
# El armazon: registrar casos y contarlos
# ---------------------------------------------------------------------------
# Cada caso es una funcion que devuelve (paso, detalle).
# No hace falta una libreria de testing para entender la idea: un eval es
# una funcion que compara lo que salio con lo que deberia salir.

CASOS = []


def caso(grupo, descripcion):
    """Decorador. Apunta la funcion en la lista con su etiqueta."""
    def envolver(fn):
        CASOS.append((grupo, descripcion, fn))
        return fn
    return envolver


class Falso:
    """Un 'usage' de mentira, para probar costo() sin llamar a la API.

    Esto se llama un DOBLE: un objeto que finge ser otro lo justo para
    que el codigo que estas probando no note la diferencia. Es lo que
    te deja probar la aritmetica del dinero sin gastar dinero."""
    def __init__(self, entrada, salida):
        self.input_tokens = entrada
        self.output_tokens = salida


# ---------------------------------------------------------------------------
# GRUPO 1 - El dinero
# ---------------------------------------------------------------------------

@caso("dinero", "costo() calcula bien con los precios de Opus 5")
def _():
    # 1000 entrada a $5/M = $0.005 ; 1000 salida a $25/M = $0.025
    obtenido = h.costo(Falso(1000, 1000))
    esperado = 0.030
    return abs(obtenido - esperado) < 1e-9, f"esperado {esperado}, obtenido {obtenido}"


@caso("dinero", "costo() de una llamada vacia es 0")
def _():
    return h.costo(Falso(0, 0)) == 0.0, "una llamada sin tokens no puede costar"


@caso("dinero", "la salida cuesta 5x lo que la entrada")
def _():
    # Comprobar la RELACION, no el numero fijo. Si manana Anthropic
    # cambia los precios, este caso sigue diciendo algo cierto o falla
    # por una razon de verdad. Leccion L1.13: calcular, no fijar.
    razon = h.costo(Falso(0, 1000)) / h.costo(Falso(1000, 0))
    return abs(razon - 5.0) < 1e-9, f"razon salida/entrada = {razon}"


@caso("dinero", "el presupuesto esta puesto en un valor sensato")
def _():
    return 0 < h.PRESUPUESTO_USD <= 1.0, f"PRESUPUESTO_USD = {h.PRESUPUESTO_USD}"


# ---------------------------------------------------------------------------
# GRUPO 2 - Los permisos
# ---------------------------------------------------------------------------

@caso("permisos", "una herramienta 'permitir' pasa sin preguntar")
def _():
    ok, motivo = h.pedir_permiso("obtener_clima", {"ciudad": "Bogota"})
    return ok is True, f"ok={ok}, motivo={motivo!r}"


@caso("permisos", "DENEGAR POR DEFECTO: una herramienta desconocida se prohibe")
def _():
    # El caso mas importante del archivo. Nadie escribio una regla para
    # 'formatear_disco': justamente por eso tiene que fallar hacia el
    # lado seguro. PERMISOS.get(nombre, "prohibir").
    ok, motivo = h.pedir_permiso("formatear_disco", {})
    return ok is False, f"ok={ok}, motivo={motivo!r}"


@caso("permisos", "'preguntar' respeta el SI del humano")
def _():
    import builtins
    guardado = builtins.input
    builtins.input = lambda _="": "s"          # simulamos que teclea s
    try:
        ok, motivo = h.pedir_permiso("borrar_archivo", {"nombre": "x.txt"})
    finally:
        builtins.input = guardado              # siempre devolverlo
    return ok is True, f"ok={ok}, motivo={motivo!r}"


@caso("permisos", "'preguntar' respeta el NO del humano")
def _():
    import builtins
    guardado = builtins.input
    builtins.input = lambda _="": "n"
    try:
        ok, motivo = h.pedir_permiso("borrar_archivo", {"nombre": "x.txt"})
    finally:
        builtins.input = guardado
    return ok is False, f"ok={ok}, motivo={motivo!r}"


@caso("permisos", "solo un SI explicito autoriza; todo lo demas es NO")
def _():
    # ESTE CASO ENCONTRO UN AGUJERO DE SEGURIDAD REAL en el harness del
    # nivel 4. El codigo decia 'respuesta.startswith("s")', asi que
    # CUALQUIER palabra que empezara por s autorizaba el borrado --
    # incluidas las que teclea alguien que quiere abortar.
    #
    # Fijate en la lista: "salir", "stop", "suspende". Las palabras que
    # la gente usa para cancelar en espanol empiezan por s. El freno se
    # abria con la palabra que uno escribe para cerrarlo.
    #
    # Es tambien la leccion de por que un eval se escribe con casos
    # HOSTILES y no con el caso feliz. Probar "s" y "n" habria pasado.
    import builtins
    guardado = builtins.input
    fallos = []
    peligrosas = [
        "", "  ", "no", "nunca", "quiza", "y", "yes",
        "salir", "stop", "suspende", "sal de ahi", "sacame", "S I",
    ]
    try:
        for tecla in peligrosas:
            builtins.input = lambda _="", t=tecla: t
            ok, _m = h.pedir_permiso("borrar_archivo", {"nombre": "x.txt"})
            if ok:
                fallos.append(repr(tecla))
    finally:
        builtins.input = guardado
    return not fallos, (f"AUTORIZARON EL BORRADO: {fallos}" if fallos
                        else f"las {len(peligrosas)} negadas correctamente")


@caso("permisos", "el SI sigue funcionando en sus formas normales")
def _():
    # El complemento del anterior: al blindar algo es facil pasarse y
    # dejarlo tan cerrado que ya nadie pueda decir que si.
    import builtins
    guardado = builtins.input
    fallos = []
    try:
        for tecla in ["s", "S", "si", "Si", "SI", "sí", " s "]:
            builtins.input = lambda _="", t=tecla: t
            ok, _m = h.pedir_permiso("borrar_archivo", {"nombre": "x.txt"})
            if not ok:
                fallos.append(repr(tecla))
    finally:
        builtins.input = guardado
    return not fallos, (f"estas deberian autorizar y no lo hicieron: {fallos}"
                        if fallos else "todas autorizan")


# ---------------------------------------------------------------------------
# GRUPO 3 - El segundo candado de la herramienta peligrosa
# ---------------------------------------------------------------------------
# borrar_archivo se defiende SOLA, ademas del permiso. Son dos candados
# para la misma puerta, porque el permiso lo puede dar un humano distraido.

@caso("candado", "no deja salir de caja/ con ../")
def _():
    salida = h.borrar_archivo("../03_harness.py")
    sigue = (_ruta).exists()
    return ("solo" in salida.lower() or "no" in salida.lower()) and sigue, \
        f"devolvio {salida!r}; el harness sigue existiendo: {sigue}"


@caso("candado", "no deja usar una ruta absoluta")
def _():
    objetivo = str(Path(tempfile.gettempdir()) / "no-deberia-borrarse.txt")
    Path(objetivo).write_text("intacto", encoding="utf-8")
    h.borrar_archivo(objetivo)
    sobrevivio = Path(objetivo).exists()
    if sobrevivio:
        Path(objetivo).unlink()
    return sobrevivio, "el archivo de fuera de caja/ sobrevivio" if sobrevivio \
        else "SE BORRO UN ARCHIVO FUERA DE caja/"


@caso("candado", "un archivo que no existe da mensaje, no excepcion")
def _():
    try:
        salida = h.borrar_archivo("no-existe-jamas.txt")
        return isinstance(salida, str) and len(salida) > 0, f"devolvio {salida!r}"
    except Exception as e:
        return False, f"lanzo {type(e).__name__} en vez de devolver texto"


@caso("candado", "SI borra lo que esta dentro de caja/")
def _():
    # El complemento imprescindible: un candado que no deja pasar nada
    # tampoco sirve. Hay que probar que la funcion HACE su trabajo.
    h.CAJA.mkdir(exist_ok=True)
    victima = h.CAJA / "archivo-de-prueba-del-eval.txt"
    victima.write_text("borrame", encoding="utf-8")
    h.borrar_archivo(victima.name)
    return not victima.exists(), "el archivo de dentro de caja/ se borro"


# ---------------------------------------------------------------------------
# GRUPO 4 - Coherencia de la tabla de herramientas
# ---------------------------------------------------------------------------
# Estos no prueban comportamiento: prueban que no se te olvido nada.
# Son los que cazan el error de agregar una herramienta nueva y olvidar
# darle permiso o funcion.

@caso("coherencia", "toda herramienta anunciada tiene funcion que la ejecuta")
def _():
    anunciadas = {t["name"] for t in h.HERRAMIENTAS}
    faltan = anunciadas - set(h.FUNCIONES)
    return not faltan, f"anunciadas al modelo pero sin funcion: {faltan or 'ninguna'}"


@caso("coherencia", "no hay funciones que el modelo no pueda pedir")
def _():
    anunciadas = {t["name"] for t in h.HERRAMIENTAS}
    sobran = set(h.FUNCIONES) - anunciadas
    return not sobran, f"con funcion pero no anunciadas: {sobran or 'ninguna'}"


@caso("coherencia", "toda herramienta tiene una politica de permiso explicita")
def _():
    anunciadas = {t["name"] for t in h.HERRAMIENTAS}
    sin_regla = anunciadas - set(h.PERMISOS)
    # No es fatal (el .get las prohibe), pero si es un olvido: significa
    # que una herramienta anunciada nunca podria ejecutarse.
    return not sin_regla, f"sin entrada en PERMISOS: {sin_regla or 'ninguna'}"


@caso("coherencia", "toda herramienta describe para que sirve")
def _():
    mudas = [t["name"] for t in h.HERRAMIENTAS
             if len(t.get("description", "").strip()) < 20]
    # Es lo UNICO que el modelo lee para decidir. Una descripcion vacia
    # es una herramienta que nunca se va a usar bien (nivel 3).
    return not mudas, f"con descripcion pobre: {mudas or 'ninguna'}"


@caso("coherencia", "las politicas de permiso son valores conocidos")
def _():
    validas = {"permitir", "prohibir", "preguntar"}
    raras = {k: v for k, v in h.PERMISOS.items() if v not in validas}
    # Una errata como "permtir" no revienta: cae en el else y prohibe.
    # Falla del lado seguro, pero rompe la herramienta en silencio.
    return not raras, f"politicas no reconocidas: {raras or 'ninguna'}"


# ---------------------------------------------------------------------------
# GRUPO 5 - El registro
# ---------------------------------------------------------------------------

@caso("registro", "anotar() escribe una linea de JSON valido")
def _():
    guardado = h.REGISTRO
    with tempfile.TemporaryDirectory() as tmp:
        h.REGISTRO = Path(tmp) / "prueba.jsonl"
        try:
            h.anotar("prueba", uno=1, dos="dos")
            lineas = h.REGISTRO.read_text(encoding="utf-8").strip().splitlines()
            dato = json.loads(lineas[-1])
        finally:
            h.REGISTRO = guardado          # no ensuciar el registro real
    tiene = "evento" in dato and dato["uno"] == 1
    return tiene, f"quedo: {dato}"


@caso("registro", "anotar() incluye la hora")
def _():
    guardado = h.REGISTRO
    with tempfile.TemporaryDirectory() as tmp:
        h.REGISTRO = Path(tmp) / "prueba.jsonl"
        try:
            h.anotar("prueba")
            dato = json.loads(h.REGISTRO.read_text(encoding="utf-8").strip())
        finally:
            h.REGISTRO = guardado
    # Sin hora, el registro no puede responder "cuanto tardo cada cosa",
    # que fue el mejor hallazgo del nivel 4 (los 43 s del humano).
    clave = [k for k in dato if "hora" in k or "time" in k or "ts" in k]
    return bool(clave), f"claves del evento: {list(dato)}"


# ---------------------------------------------------------------------------
# GRUPO 6 - Los topes
# ---------------------------------------------------------------------------

@caso("topes", "MAX_VUELTAS es mayor que 1")
def _():
    # Con 1 el agente no podria ni responder tras usar una herramienta:
    # hacen falta 2 vueltas como minimo (pedir, y contestar con el dato).
    return h.MAX_VUELTAS > 1, f"MAX_VUELTAS = {h.MAX_VUELTAS}"


@caso("topes", "REINTENTOS_PROPIOS >= 1 (si no, llamar_modelo devuelve None)")
def _():
    # La trampa latente que se señalo en la sesion 6: con 0, el 'for' de
    # llamar_modelo() no se ejecuta nunca y la funcion devuelve None sin
    # avisar. Mismo tipo que el contador roto de 01_chat.py.
    return h.REINTENTOS_PROPIOS >= 1, f"REINTENTOS_PROPIOS = {h.REINTENTOS_PROPIOS}"


@caso("topes", "el SDK no reintenta ademas del reintento propio")
def _():
    # Si los dos estan activos se multiplican: 3 x 3 = 9 peticiones por
    # una sola llamada (leccion del nivel 4).
    return h.REINTENTOS_SDK == 0, f"REINTENTOS_SDK = {h.REINTENTOS_SDK}"


# ---------------------------------------------------------------------------
# El corredor
# ---------------------------------------------------------------------------

def main():
    print("=" * 76)
    print("  EVALS DETERMINISTAS DEL HARNESS  (costo: $0.00)")
    print("=" * 76)
    print("  Se prueba el codigo que TU escribiste, no lo que dice el modelo.")
    print("  Por eso puede dar identico siempre y correrse mil veces.")
    print("=" * 76)

    pasaron, fallaron = 0, []
    grupo_actual = None

    for grupo, descripcion, fn in CASOS:
        if grupo != grupo_actual:
            grupo_actual = grupo
            print(f"\n  [{grupo.upper()}]")

        # Se le tapa la boca al codigo probado mientras corre el caso.
        #
        # POR QUE: pedir_permiso() imprime "PERMISO: el agente quiere...".
        # Los casos que barren 13 y 7 teclas lo llamaban 20 veces, y la
        # salida quedaba enterrada bajo 20 lineas de ruido.
        # Es el mismo patron del [:30], del [:80] y del 'else' de
        # 04b_eventos.py -- alli el print CORTABA el dato, aqui lo AHOGA.
        #
        # Pero no se tira: se guarda. Si el caso falla, se enseña, porque
        # entonces esas lineas son justo lo que hace falta para entender.
        capturado = io.StringIO()
        try:
            with contextlib.redirect_stdout(capturado):
                ok, detalle = fn()
        except Exception as e:
            ok, detalle = False, f"REVENTO: {type(e).__name__}: {e}"

        if ok:
            pasaron += 1
            print(f"    OK    {descripcion}")
        else:
            fallaron.append((grupo, descripcion, detalle))
            print(f"   FALLA  {descripcion}")
            print(f"          -> {detalle}")
            ruido = capturado.getvalue().strip()
            if ruido:
                print("          lo que imprimio mientras fallaba:")
                for linea in ruido.splitlines()[:8]:
                    print(f"            | {linea.strip()}")

    print()
    print("=" * 76)
    print(f"  {pasaron} de {len(CASOS)} evals pasaron")
    print("=" * 76)

    if fallaron:
        print("\n  LO QUE HAY QUE ARREGLAR:")
        for grupo, desc, detalle in fallaron:
            print(f"    [{grupo}] {desc}")
            print(f"             {detalle}")
        sys.exit(1)

    print("""
  QUE ACABA DE PASAR
  ------------------
  Se probaron los seis frenos del harness sin gastar un centavo y sin
  que el modelo interviniera. Todos estos casos dan lo mismo siempre:
  son codigo normal.

  Lo que estos evals NO pueden decirte:
    - si el modelo eligio la herramienta correcta
    - si la respuesta esta bien escrita
    - si respeto el dialecto
  Eso necesita llamadas de verdad (scripts 1-3) o un juez (lo que viene).

  La division vale para todo lo que construyas despues:
    lo que decide TU codigo  -> se prueba asi, gratis y con certeza
    lo que decide EL MODELO  -> se prueba contando, y cuesta
""")


if __name__ == "__main__":
    main()
