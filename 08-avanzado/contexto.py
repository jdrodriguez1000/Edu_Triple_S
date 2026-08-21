"""C.1 · PASO 2 — DE QUIÉN ES HIJA ESTA LÍNEA. El parentesco, sin escribirlo a mano.

El paso 1 midió que `capa` era un adjetivo: se le podía cambiar el dueño a 35
renglones sin que nada se pusiera rojo. Este archivo es el intento de que el
parentesco **no** sea otro adjetivo.

⚠️ EL SOSPECHOSO DE ESTAR CIEGO, NOMBRADO EN EL SOBRE ANTES DE ESCRIBIR ESTO:

       «el que escribe `padre=` es el mismo que ya sabe quién es el padre»

   Un árbol dibujado por quien ya lo conocía mide al que lo dibujó, no al
   harness. **Por eso aquí NADIE escribe `padre=`.** No hay un solo sitio del
   código donde se pase el id del padre como argumento. El parentesco se
   DEDUCE de dónde está el programa cuando anota, y quien lo deduce es la
   librería estándar, no yo.

🔑 LA PIEZA QUE LO HACE POSIBLE: `contextvars`.
   Una variable de contexto es como una etiqueta colgada del hilo de ejecución:
   la cuelgas al entrar en un tramo y la descuelgas al salir. Todo lo que se
   ejecute dentro la ve, por hondo que esté, sin que nadie se la pase.
   → Analogía: no es una carta que va de mano en mano; es la luz de la
     habitación. Quien entra, la tiene. Quien sale, la pierde.

🚨 Y TRAE UNA TRAMPA QUE MUERDE EXACTAMENTE DONDE YA MORDIÓ LA TRAZA PLANA.
   **Un hilo nuevo NO hereda el contexto de quien lo lanzó.** `ThreadPoolExecutor`
   no lo copia. O sea: en serie el parentesco saldría perfecto, y en el fan-out
   PARALELO de B.2 los workers quedarían huérfanos — el mismo sitio donde unir
   por el reloj fallaba (1 segundo con 3 arranques, medido en la sesión 97).
   → Por eso existe `atado()`, abajo. Y por eso el paso 3 tiene que apuntar ahí.
"""

import contextvars
import functools
import inspect
import itertools
import threading

# El tramo actual: un diccionario con corrida / id / padre / profundidad, o
# `None` si todavía no se ha abierto ninguno.
_ACTUAL = contextvars.ContextVar("tramo_actual", default=None)

# Un contador con candado. Se prefiere a un `uuid` a propósito: los ids salen
# cortos y en orden, y en un registro que se lee a ojo eso vale más que la
# unicidad global — este archivo no sale de una máquina.
_CONTADOR = itertools.count(1)
_CANDADO = threading.Lock()


def _siguiente(prefijo):
    with _CANDADO:
        return f"{prefijo}{next(_CONTADOR)}"


class _Tramo:
    """Un `with` que abre un tramo hijo del que esté abierto ahora mismo.

    No recibe el padre: lo mira. Ahí está la diferencia entre un dato y un
    adjetivo.
    """

    __slots__ = ("nombre", "_ficha", "_testigo")

    def __init__(self, nombre):
        self.nombre = nombre
        self._ficha = None
        self._testigo = None

    def __enter__(self):
        padre = _ACTUAL.get()
        self._ficha = {
            # La corrida se hereda si ya había una; si no, este tramo la funda.
            # 🚨 ESTE CAMPO ES EL BICHO DE LA SESIÓN 97 CERRADO POR DISEÑO: sin
            #    él, una línea de prueba y una línea pagada viven en el mismo
            #    archivo sin nada que las separe.
            "corrida": padre["corrida"] if padre else _siguiente("c"),
            "id": _siguiente("t"),
            "padre": padre["id"] if padre else None,
            "profundidad": (padre["profundidad"] + 1) if padre else 0,
            "tramo": self.nombre,
        }
        self._testigo = _ACTUAL.set(self._ficha)
        return self._ficha

    def __exit__(self, *_):
        # 🔒 Se descuelga SIEMPRE, también si el tramo revienta. Un contexto que
        #    se queda encendido tras un fallo cuelga las líneas siguientes del
        #    padre equivocado — y eso no da error, da un árbol creíble y falso.
        _ACTUAL.reset(self._testigo)
        return False


def tramo(nombre):
    """Abre un tramo hijo del actual. Se usa como `with tramo("usd"): ...`."""
    return _Tramo(nombre)


def envuelto(param, prefijo="", atributo=None):
    """Decorador: abre un tramo alrededor de la función ENTERA.

    El nombre del tramo sale del parámetro `param` de la propia función, con
    sus valores por defecto aplicados. Si el parámetro es un objeto y lo que
    sirve de nombre es uno de sus campos, se dice con `atributo`.
    Se hace así y no a mano por dos razones:

    1. Envolver el cuerpo en un `with` obligaría a reindentar funciones de
       cien líneas, y una reindentación grande esconde cualquier otro cambio.
    2. 🔑 **Leer el nombre de la firma evita escribirlo dos veces.** Es el bicho
       de la sesión 33: la misma cosa escrita en dos sitios acaba diciendo cosas
       contrarias. Si mañana cambia el valor por defecto de `nombre`, el tramo
       cambia solo.

    📌 `functools.wraps` no es decoración: hace que `inspect.signature` siga
       viendo la firma de verdad. Sin él, la prueba 1 de `profundidad.py` —la
       que vigila que `sistema`, `tools` y `funciones` sigan arrancando en
       `None`— se pondría roja por un motivo que no tiene nada que ver con lo
       que vigila.
    """
    def decorar(fn):
        firma = inspect.signature(fn)

        @functools.wraps(fn)
        def dentro(*a, **kw):
            atados = firma.bind(*a, **kw)
            atados.apply_defaults()
            valor = atados.arguments.get(param)
            if atributo is not None:
                valor = getattr(valor, atributo, valor)
            with tramo(f"{prefijo}{valor}"):
                return fn(*a, **kw)
        return dentro
    return decorar


def marca():
    """Lo que hay que estampar en una línea del registro AHORA MISMO.

    Devuelve `{}` si no hay ningún tramo abierto — y eso es deliberado: una
    línea sin tramo se ve a simple vista como huérfana, en vez de colgar de una
    raíz inventada que parecería correcta.

    🔑 CUÁL DE ESTOS CINCO CAMPOS AGUANTA EL PESO, Y CUÁL ES DECORACIÓN.
       `corrida`, `id`, `padre` y `profundidad` son **estructura**: con ellos se
       reconstruye el árbol, y si uno miente el árbol sale distinto.
       `tramo` es **una etiqueta**, exactamente de la misma clase que `capa` —la
       que el paso 1 midió que se podía torcer sin que nada se rompiera—.
       → Se incluye igual, porque sin un nombre legible el árbol no se lee. Pero
         queda dicho aquí cuál es cuál. **El paso 1 no enseñó que las etiquetas
         sobren: enseñó que hay que saber cuáles lo son.**
    """
    actual = _ACTUAL.get()
    if actual is None:
        return {}
    return {k: actual[k] for k in ("corrida", "id", "padre", "profundidad", "tramo")}


def actual():
    """El tramo abierto, o `None`. Para las pruebas, no para el código normal."""
    return _ACTUAL.get()


def atado(fn):
    """Devuelve `fn` atada al contexto de traza de AHORA, para cruzar a un hilo.

    🚨 SIN ESTO, EL PARALELO PIERDE EL PARENTESCO, Y NO DA ERROR.
       `ThreadPoolExecutor` **no** copia el contexto: el hilo nuevo arranca con
       la habitación a oscuras. Los tres workers del fan-out de B.2 anotarían
       con `padre: null` y `profundidad: 0` — huérfanos, como si cada uno fuera
       una corrida entera. El árbol saldría plano y **con pinta de correcto**.

    🔑 Y fíjate DÓNDE falla: exactamente donde falla unir por el reloj. En la
       sesión 97 se contó que de 35 arranques hay UN segundo con tres a la vez,
       el del fan-out. **El paralelo es el sitio donde toda forma barata de
       saber quién es quién se rompe** — porque es el único sitio donde «lo que
       pasó justo antes» deja de significar «quien me llamó».

    📌 Se copia el contexto UNA VEZ POR TAREA, en el hilo de quien llama. Un
       mismo `Context` no se puede entrar dos veces a la vez: compartir una sola
       copia entre los tres hilos revienta con `cannot enter context`.
    """
    ctx = contextvars.copy_context()
    return lambda *a, **kw: ctx.run(fn, *a, **kw)
