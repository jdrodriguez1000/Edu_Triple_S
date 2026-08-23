"""modelos.py — C.6 del nivel 8: MODELO Y ESFUERZO POR CAPA.

    LA PREGUNTA DE C.6, EN UNA FRASE

¿Puede cada capa correr con su propio modelo y su propio esfuerzo? Y si puede,
**¿la contabilidad se entera?**

⭐ LA SEGUNDA MITAD DE LA PREGUNTA ES TODA LA PIEZA. Poner otro modelo arriba es
   cambiar una cadena de texto: eso lo hace cualquiera. Lo que hay que averiguar
   es si el harness que lleva CINCO bloques midiendo dólares sigue midiendo
   dólares cuando las dos capas dejan de costar lo mismo.


    POR QUÉ ESTA PIEZA ES LA MÁS CARA DEL NIVEL

Entre la configuración más barata y la más cara hay **5×**. No hay ninguna otra
palanca en el nivel 8 que mueva la factura tanto — ni el fan-out, ni el pipeline,
ni el aislamiento de A.4. Todos ellos mueven CUÁNTOS tokens se gastan; ésta
mueve **cuánto vale cada token**, y multiplica todo lo demás.


    ESTE PASO NO PAGA UN CENTAVO, Y ESTA VEZ NI SIQUIERA HAY MODELO DE MENTIRA

En C.4 y C.5 hubo que fabricar un cliente falso para que hablara. Aquí no hace
falta nadie que hable: **los tokens ya están pagados y grabados**. Los registros
del nivel llevan desde la sesión 91 el `entrada` y el `salida` de cada llamada.

🔑 Y eso es lo que hace esta medición mejor que una simulación: **volver a
   tarifar tokens REALES es aritmética sobre un hecho, no una estimación sobre
   un supuesto.** El único trozo falso de este archivo es `_Uso`, y solo existe
   para las pruebas.


    ══════════════════════════════════════════════════════════════════════
    🔒 LAS APUESTAS QUE ESTE PASO ABRE (selladas en la sesión 104, commit
       `c034939`, antes de la primera línea de este archivo)
    ══════════════════════════════════════════════════════════════════════

    1. El precio está pegado al MÓDULO, no a la llamada. Con dos modelos
       distintos la contabilidad entera sigue facturando al precio de UNO, sin
       una queja, y el error es exactamente `precio_real / precio_supuesto`.

    2. El registro NO puede decirlo después: ninguna línea anota qué modelo hizo
       esa llamada, así que ni pagando se puede auditar. Es el caso SIMÉTRICO de
       C.1, donde el tercer testigo ya estaba grabado (`LM.68`).

    3. El presupuesto en dólares es lo único de C.2 que sobrevive intacto al
       cambio de modelo —está escrito en la unidad correcta— **y aun así se cae
       con la 1**, porque vigilaría dólares falsos.

    Las apuestas 4, 5 y 6 (esfuerzo, isomorfía del árbol, coste) NO se abren
    aquí: necesitan pagar. Este archivo cuesta $0,000000.

📌 Cómo se corre:

    python modelos.py              <- las tres apuestas, sobre tokens ya pagados
    python modelos.py --pruebas    <- las pruebas. Sin modelo, sin red, $0,00
    python modelos.py --trampa     <- 🚨 LLAMA AL MODELO. Céntimos.
    python modelos.py --pagar      <- 🚨 LA CORRIDA REAL. ~$0,05.

⚠️ Y `--pruebas` es la bandera de este nivel a propósito: `fan_out.py` usa
   `--test` y `aislamiento.py` ignora la bandera. Las dos son deudas anotadas en
   `GUIDE.md` §6.e; no se arreglan aquí para no mezclar dos cosas.
"""

import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "05b-proyecto"))

import agente          # noqa: E402


# ---------------------------------------------------------------------------
# 1) LA PIEZA NUEVA — el precio, atado a la LLAMADA y no al módulo
# ---------------------------------------------------------------------------
#
# 🎁 ESTO NO SE INVENTA HOY: SE GENERALIZA. `juez_duelo.py:50-51` ya hace
#    exactamente esto desde la sesión 100, y no por elegancia: es el ÚNICO
#    archivo del nivel que usa un modelo distinto a `agente.MODELO`, y por eso
#    fue el único obligado a sacar sus precios del catálogo con su modelo como
#    llave. Nadie lo subió a función. Es `LM.20` esperando turno: **la
#    corrección ya estaba escrita en el repositorio y nadie la alcanzó.**

class ModeloDesconocido(ValueError):
    """El modelo pedido no está en el catálogo.

    ⚠️ Se muere aquí, antes de armar una petición, y por el mismo motivo que el
       freno 10 de `agente.py`: un nombre mal escrito que llega a la API te
       cuesta un 404 después de haber gastado el tiempo, y un nombre mal escrito
       que llega a la CONTABILIDAD te cuesta un número que parece bueno.
    """


def precio(modelo):
    """Los dos precios de UN modelo, en dólares por millón de tokens."""
    if modelo not in agente.CATALOGO:
        raise ModeloDesconocido(
            f"{modelo!r} no está en el catálogo. Los que hay: "
            f"{', '.join(agente.CATALOGO)}")
    fila = agente.CATALOGO[modelo]
    return fila["entrada"], fila["salida"]


def costo_de(uso, modelo):
    """Cuánto costó UNA llamada, con el precio DEL MODELO QUE LA HIZO.

    Compáralo con `agente.costo(usage)`, que es el mismo cálculo con una
    diferencia de una palabra: aquélla usa `PRECIO_ENTRADA` y `PRECIO_SALIDA`,
    constantes de módulo fijadas al importar. Ésta recibe el modelo.

    🔑 Y esa palabra es toda la apuesta 1. Mientras las dos capas comparten
       modelo, las dos funciones dan el mismo número y nadie nota nada. El día
       que dejan de compartirlo, una de las dos empieza a mentir — y no avisa,
       porque no tiene forma de saber que está mintiendo.
    """
    p_entrada, p_salida = precio(modelo)
    return (uso.input_tokens * p_entrada
            + uso.output_tokens * p_salida) / 1_000_000


# --- El esfuerzo, que NO es lo mismo que el modelo -------------------------
#
# ⭐ Y LA DIFERENCIA IMPORTA PARA ENTENDER POR QUÉ UNA PALANCA ES GRANDE Y LA
#    OTRA PEQUEÑA:
#
#      el MODELO   cambia cuánto vale cada token   -> multiplica TODA la factura
#      el ESFUERZO cambia cuántos tokens de SALIDA se producen
#
#    Por defecto el esfuerzo es `high`, que es lo mismo que no mandarlo.
#
#    En un agente con herramientas la entrada manda, porque el menú se repaga en
#    cada vuelta. Por eso la apuesta 4 predice que el esfuerzo es una palanca de
#    segundo orden. **Esa apuesta no se abre aquí: cuesta dinero.** Lo que sí se
#    puede hacer gratis es contar qué fracción del gasto es salida, que es el
#    techo de lo que el esfuerzo podría ahorrar.

# ⚠️ SON CINCO, NO CUATRO. Se escribieron cuatro de memoria y la documentación
#    puso el quinto: `xhigh`, que va ENTRE `high` y `max` y llegó con Opus 4.7.
#    Es el recomendado para trabajo agéntico en opus-5 y sonnet-5, o sea
#    justamente el caso de este nivel — el que faltaba era el útil.
# 🔑 Y el modo de fallo era silencioso en la dirección peligrosa: con la lista
#    corta, pedir `xhigh` moría en casa con «ese esfuerzo no existe» y el
#    mensaje habría sonado a verdad. Un validador con una lista incompleta no
#    deja pasar basura: **rechaza cosas buenas diciendo que son basura.**
ESFUERZOS = ("low", "medium", "high", "xhigh", "max")

# 🚨 LA TRAMPA VERIFICADA CONTRA LA DOCUMENTACIÓN EL 2026-08-20: `effort` NO
#    funciona en `claude-haiku-4-5`, que es de la generación anterior. Y como el
#    modelo por defecto de TODO el nivel es haiku, cualquiera que juegue con
#    esfuerzos sin leer esto se lleva un error de la API.
MODELOS_CON_ESFUERZO = ("claude-opus-5", "claude-sonnet-5")


class EsfuerzoNoSoportado(ValueError):
    """Se pidió `effort` a un modelo que no lo entiende."""


class Capa:
    """La configuración de UNA capa: con qué modelo habla y con cuánto esfuerzo.

    ⭐ ES UN OBJETO Y NO DOS PARÁMETROS SUELTOS, Y ESO ES B.5 OTRA VEZ: lo que
       entra por la puerta no crece el bucle. `correr_worker` y
       `correr_orquestador` van a recibir UNA cosa, no dos; el día que C.6 quiera
       añadir `thinking` o un `max_tokens` por capa, la firma no cambia.
    """

    def __init__(self, modelo=None, esfuerzo=None):
        self.modelo = modelo or agente.MODELO
        # Se valida en el constructor, no al llamar a la API. Un error de
        # configuración tiene que doler ANTES de que haya nada que perder.
        precio(self.modelo)
        if esfuerzo is not None:
            if esfuerzo not in ESFUERZOS:
                raise EsfuerzoNoSoportado(
                    f"esfuerzo {esfuerzo!r} no existe: {', '.join(ESFUERZOS)}")
            if self.modelo not in MODELOS_CON_ESFUERZO:
                raise EsfuerzoNoSoportado(
                    f"{self.modelo} no acepta `effort` (es de la generación "
                    f"anterior). Lo aceptan: {', '.join(MODELOS_CON_ESFUERZO)}")
        self.esfuerzo = esfuerzo

    def extras_de_peticion(self):
        """Lo que hay que añadirle a `messages.create` por esta configuración.

        Devuelve un diccionario para hacer `peticion.update(...)`. Vacío si no
        hay esfuerzo, y eso es a propósito: mandar `output_config` con el valor
        por defecto no es lo mismo que no mandarlo, y A.1 no debe cambiar de
        conducta porque C.6 exista.
        """
        if self.esfuerzo is None:
            return {}
        return {"output_config": {"effort": self.esfuerzo}}

    def __repr__(self):
        e = f", esfuerzo={self.esfuerzo}" if self.esfuerzo else ""
        return f"Capa({self.modelo}{e})"

    def __eq__(self, otra):
        return (isinstance(otra, Capa) and self.modelo == otra.modelo
                and self.esfuerzo == otra.esfuerzo)


# ---------------------------------------------------------------------------
# 2) LEER LO YA PAGADO — los tokens de verdad, sin gastar uno nuevo
# ---------------------------------------------------------------------------

REGISTRO_ARRIBA = AQUI / f"registro_orquestador_{agente.MODELO}.jsonl"
REGISTRO_ABAJO = AQUI / f"registro_workers_{agente.MODELO}.jsonl"


def antes_de_c6(linea):
    """¿Esta línea se grabó ANTES de que C.6 cableara el modelo?

    📌 No hace falta una fecha ni una versión: **la ausencia del campo ES la
       marca**. Toda línea sin `modelo` es anterior al cableado, y toda línea
       posterior lo lleva. Es el único caso en que un campo que falta sirve de
       reloj, y funciona porque el campo se añadió de una vez y para siempre.
    """
    return "modelo" not in linea


class Uso:
    """Los tokens de una capa entera, sumados. Sirve para `costo_de`."""

    def __init__(self, entrada=0, salida=0, llamadas=0):
        self.input_tokens = entrada
        self.output_tokens = salida
        self.llamadas = llamadas

    def __repr__(self):
        return (f"Uso(entrada={self.input_tokens}, salida={self.output_tokens},"
                f" llamadas={self.llamadas})")


def sumar_registro(ruta, filtro=None):
    """Suma los tokens de las líneas `llamada_api` de un registro.

    ⭐ `filtro` ENTRÓ EL MISMO DÍA QUE C.6 SE CABLEÓ, Y POR UN MOTIVO QUE VALE LA
       PENA CONTAR. Hasta esta sesión, sumar el registro entero y tarifarlo a
       precio de haiku daba exactamente lo grabado: **todas las líneas eran de
       un solo modelo.** En cuanto la primera corrida con opus tocó el archivo,
       esa suma dejó de significar nada — y **dos pruebas se pusieron rojas en el
       acto**, que es como se supo.
    🔑 Un registro que mezcla configuraciones no está roto: está diciendo la
       verdad sobre un mundo que se volvió más complicado. Lo que se rompe es
       **todo cálculo que daba por supuesto que el mundo era homogéneo** — y esos
       cálculos casi nunca escriben ese supuesto en ninguna parte.

    Devuelve `(Uso, costo_grabado_usd, campos_vistos)`.

    📌 `costo_grabado_usd` es lo que el harness ANOTÓ en su día, no lo que
       recalculamos. Guardarlo aparte es lo que permite la comprobación de la
       apuesta 1: si nuestro recálculo con el mismo modelo no reproduce el
       número grabado, el instrumento nuevo está roto y no hay nada que medir.
       Es `LM.66`: un segundo testigo que primero tiene que CONFIRMAR.
    """
    uso = Uso()
    grabado = 0.0
    campos = set()
    if not ruta.exists():
        return uso, grabado, campos
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            d = json.loads(linea)
            if d.get("evento") != "llamada_api":
                continue
            if filtro is not None and not filtro(d):
                continue
            campos.update(d)
            uso.input_tokens += d.get("entrada", 0)
            uso.output_tokens += d.get("salida", 0)
            uso.llamadas += 1
            grabado += d.get("costo_usd", 0.0)
    return uso, grabado, campos


def _fmt(usd):
    return f"${usd:,.6f}"


# ---------------------------------------------------------------------------
# 3) APUESTA 1 — el precio está pegado al módulo
# ---------------------------------------------------------------------------

def apuesta_1_el_precio_del_modulo():
    """¿Qué dice la contabilidad si las dos capas dejan de costar lo mismo?"""
    print("\n" + "=" * 72)
    print("  🎲 APUESTA 1 — el precio está pegado al MÓDULO, no a la llamada")
    print("=" * 72)

    arriba, grabado_arriba, _ = sumar_registro(REGISTRO_ARRIBA, antes_de_c6)
    abajo, grabado_abajo, _ = sumar_registro(REGISTRO_ABAJO, antes_de_c6)

    # 📌 Solo las líneas ANTERIORES a C.6: son las únicas de las que se sabe,
    #    sin preguntar, que se pagaron a precio de haiku. Mezclar las de hoy
    #    haría de esta tabla una media de dos tarifas disfrazada de una.
    print(f"\n  Tokens pagados con {agente.MODELO} "
          f"(solo líneas anteriores a C.6):")
    print(f"    arriba (orquestador): {arriba.llamadas:>4} llamadas · "
          f"{arriba.input_tokens:>7,} entrada · {arriba.output_tokens:>6,} salida")
    print(f"    abajo  (workers)    : {abajo.llamadas:>4} llamadas · "
          f"{abajo.input_tokens:>7,} entrada · {abajo.output_tokens:>6,} salida")

    # --- El testigo que primero CONFIRMA -----------------------------------
    recalculado_arriba = costo_de(arriba, agente.MODELO)
    recalculado_abajo = costo_de(abajo, agente.MODELO)
    print("\n  🔍 El instrumento nuevo contra lo grabado (mismo modelo):")
    print(f"    arriba: grabado {_fmt(grabado_arriba)} · "
          f"recalculado {_fmt(recalculado_arriba)}")
    print(f"    abajo : grabado {_fmt(grabado_abajo)} · "
          f"recalculado {_fmt(recalculado_abajo)}")
    print("    📌 Si estos no cuadraran, no habría nada que medir hoy.")

    # --- Y ahora la mentira -------------------------------------------------
    print("\n  Ahora se cambia el modelo de ARRIBA a `claude-opus-5`:")
    real = costo_de(arriba, "claude-opus-5")
    lo_que_dice = agente.costo(arriba)      # <- la función del harness de hoy
    print(f"    lo que REALMENTE costaría         : {_fmt(real)}")
    print(f"    lo que `agente.costo()` reportaría : {_fmt(lo_que_dice)}")
    print(f"    factor de la mentira              : {real / lo_que_dice:.4f}×")

    print("\n  🚨 Y la mentira no es ruidosa: es LIMPIA. El factor sale exacto")
    print("     porque los tres modelos del catálogo tienen la salida a 5× la")
    print("     entrada, así que tarifar mal escala TODA la factura por una")
    print("     constante.")
    print("  🔑 Consecuencia, y es lo peor del día: las sumas SIGUEN CUADRANDO.")
    print("     Las partes suman el total, el árbol de C.1 suma hacia arriba lo")
    print("     mismo que `auditar()` suma en plano, y todos los controles")
    print("     internos salen verdes — porque TODOS usan la misma tabla mala.")
    print("     No hay segundo testigo posible dentro de la contabilidad.")
    return {"arriba": arriba, "abajo": abajo,
            "grabado_arriba": grabado_arriba, "grabado_abajo": grabado_abajo,
            "real": real, "reportado": lo_que_dice}


# ---------------------------------------------------------------------------
# 4) APUESTA 2 — el registro no puede decirlo después
# ---------------------------------------------------------------------------

def apuesta_2_el_registro_no_lo_dice():
    """¿Se puede auditar, DESPUÉS, qué modelo hizo cada llamada?"""
    print("\n" + "=" * 72)
    print("  🎲 APUESTA 2 — el registro NO puede decirlo después")
    print("=" * 72)

    # 📌 EL ARCHIVO YA TIENE DOS ÉPOCAS, así que se cuentan por separado. La
    #    apuesta se hizo sobre lo que había ANTES del cableado; enseñarlo todo
    #    junto convertiría un agujero medido en un «pues ahí está el campo», y
    #    borraría de la vista justo lo que se aprendió.
    resultado = {}
    for etiqueta, ruta in (("arriba", REGISTRO_ARRIBA), ("abajo", REGISTRO_ABAJO)):
        viejas, _, campos_v = sumar_registro(ruta, antes_de_c6)
        nuevas, _, campos_n = sumar_registro(ruta, lambda d: not antes_de_c6(d))
        resultado[etiqueta] = {"viejas": viejas.llamadas,
                               "nuevas": nuevas.llamadas,
                               "tenia": "modelo" in campos_v,
                               "tiene": "modelo" in campos_n}
        print(f"\n  {ruta.name}")
        print(f"    ANTES de C.6 : {viejas.llamadas:>4} líneas · "
              f"¿anota `modelo`? "
              f"{'SÍ' if 'modelo' in campos_v else 'NO'}   <- la apuesta")
        print(f"    campos: {', '.join(sorted(campos_v))}")
        if nuevas.llamadas:
            print(f"    DESPUÉS de C.6: {nuevas.llamadas:>3} líneas · "
                  f"¿anota `modelo`? "
                  f"{'SÍ' if 'modelo' in campos_n else 'NO'}   <- el arreglo")

    print("\n  🚨 Es el caso SIMÉTRICO de C.1, y por eso valía medirlo.")
    print("     En la sesión 97 el tercer testigo YA ESTABA GRABADO: cada línea")
    print("     `worker_fin` llevaba el adjetivo y el hecho, y no hubo que")
    print("     añadir nada — solo un lector (`LM.68`).")
    print("     Aquí no hay lector posible: el dato no está.")
    print("  🔑 Y la diferencia entre los dos casos no es suerte. `datos.moneda`")
    print("     se grababa porque era la SALIDA de una herramienta, y el")
    print("     registro guarda salidas. El modelo es una ENTRADA de la")
    print("     petición, y de la petición el registro no guarda nada.")

    print("\n  📌 Y el nombre del archivo miente por lo mismo:")
    print("     `registro_orquestador_{MODELO}.jsonl` es UN rótulo. Con dos")
    print("     modelos en la corrida, el rótulo nombra a uno y las líneas del")
    print("     otro caen dentro sin distinguirse. Es `LM.17` con otra ropa: el")
    print("     rótulo del contenedor no describe el contenido.")
    return resultado


# ---------------------------------------------------------------------------
# 5) APUESTA 3 — el presupuesto en dólares, y por qué se cae con la 1
# ---------------------------------------------------------------------------

PRESUPUESTO_ORQ_USD = 0.05      # el de `orquestador.py:118`, tal cual


def apuesta_3_el_presupuesto_en_dolares():
    """¿Hay que retocar el techo de C.2 al cambiar de modelo?"""
    print("\n" + "=" * 72)
    print("  🎲 APUESTA 3 — el presupuesto en dólares sobrevive… y se cae con la 1")
    print("=" * 72)

    # Una corrida sola, no el histórico: el techo es POR CORRIDA.
    # Se usan los tokens de la corrida de A.3, que es la que el README tiene
    # medida en $0,004649 para la capa de arriba.
    una_corrida = Uso(entrada=4425, salida=45, llamadas=2)
    print(f"\n  Techo de la capa de arriba: {_fmt(PRESUPUESTO_ORQ_USD)} "
          f"(`orquestador.py:118`)")
    print(f"  Una corrida de arriba, en tokens: {una_corrida.input_tokens:,} "
          f"entrada · {una_corrida.output_tokens} salida")
    print()
    print(f"  {'modelo arriba':<20} {'coste':>12} {'% del techo':>12} {'margen':>10}")
    print("  " + "-" * 58)
    filas = {}
    for m in ("claude-haiku-4-5", "claude-sonnet-5", "claude-opus-5"):
        c = costo_de(una_corrida, m)
        pct = 100 * c / PRESUPUESTO_ORQ_USD
        filas[m] = (c, pct)
        print(f"  {m:<20} {_fmt(c):>12} {pct:>11.1f}% "
              f"{PRESUPUESTO_ORQ_USD / c:>9.1f}×")

    print("\n  ✅ El techo NO hay que tocarlo, y el motivo es la UNIDAD: está")
    print("     escrito en dólares, no en tokens ni en llamadas. Un tope en")
    print("     tokens habría que recalcularlo con cada modelo; uno en dólares")
    print("     se adapta solo, porque el precio ya está dentro del número.")
    print("  🔑 Es la misma lección que el `PRESUPUESTO_USD` del 5b, al revés:")
    print("     allá un límite HEREDADO sin recalcular era una trampa. Aquí un")
    print("     límite en la unidad correcta es lo único que no hay que heredar")
    print("     a mano. **La unidad de un freno decide si viaja o no.**")
    print("\n  🚨 Y AQUÍ SE CAE: ese techo se compara contra `gastado_usd`, que")
    print("     sale de `agente.costo()`. Si la apuesta 1 gana, el techo está")
    print("     vigilando dólares falsos — vería un 9 % donde hay un 46 %.")
    print("  🔑 Los dos frenos no son independientes: **el presupuesto solo vale")
    print("     lo que valga la tabla de precios.** Un freno correcto conectado a")
    print("     un instrumento ciego es `LM.15` con un techo encima.")
    return filas


# ---------------------------------------------------------------------------
# 6) LA TABLA DEL README, RECALCULADA SOBRE TOKENS REALES
# ---------------------------------------------------------------------------

def tabla_de_configuraciones():
    """Las cinco configuraciones, sobre TODO lo que el nivel lleva pagado."""
    print("\n" + "=" * 72)
    print("  📊 LAS CINCO CONFIGURACIONES, sobre tokens ya pagados")
    print("=" * 72)

    arriba, _, _ = sumar_registro(REGISTRO_ARRIBA, antes_de_c6)
    abajo, _, _ = sumar_registro(REGISTRO_ABAJO, antes_de_c6)
    tot_arriba = arriba.input_tokens + arriba.output_tokens
    tot_abajo = abajo.input_tokens + abajo.output_tokens
    total = tot_arriba + tot_abajo

    print("\n  El reparto de tokens, medido y no estimado:")
    print(f"    arriba {tot_arriba:>8,} tokens = {100*tot_arriba/total:>5.1f} %")
    print(f"    abajo  {tot_abajo:>8,} tokens = {100*tot_abajo/total:>5.1f} %")

    base = None
    print(f"\n  {'configuración':<34} {'arriba':>11} {'abajo':>11} "
          f"{'total':>12} {'vs.':>7}")
    print("  " + "-" * 80)
    combinaciones = [
        ("todo haiku (lo medido)", "claude-haiku-4-5", "claude-haiku-4-5"),
        ("sonnet arriba + haiku abajo", "claude-sonnet-5", "claude-haiku-4-5"),
        ("opus arriba + haiku abajo", "claude-opus-5", "claude-haiku-4-5"),
        ("haiku arriba + opus abajo", "claude-haiku-4-5", "claude-opus-5"),
        ("todo opus", "claude-opus-5", "claude-opus-5"),
    ]
    filas = {}
    for etiqueta, m_arriba, m_abajo in combinaciones:
        c_a = costo_de(arriba, m_arriba)
        c_b = costo_de(abajo, m_abajo)
        t = c_a + c_b
        base = base or t
        filas[etiqueta] = t
        print(f"  {etiqueta:<34} {_fmt(c_a):>11} {_fmt(c_b):>11} "
              f"{_fmt(t):>12} {t/base:>6.2f}×")

    subir_arriba = filas["opus arriba + haiku abajo"] - filas["todo haiku (lo medido)"]
    subir_abajo = filas["haiku arriba + opus abajo"] - filas["todo haiku (lo medido)"]
    print(f"\n  🔑 Subir el ORQUESTADOR a opus:  +{_fmt(subir_arriba)}")
    print(f"     Subir los WORKERS a opus:      +{_fmt(subir_abajo)}"
          f"   ({subir_abajo/subir_arriba:.1f}× más)")
    print("  🔑 Poner el modelo caro donde hay POCOS tokens es barato; ponerlo")
    print("     donde hay muchos arruina la factura. Y en un esquema de dos")
    print("     capas los tokens están abajo, siempre: cada worker relee su menú")
    print("     en cada vuelta, y hay tres workers por cada orquestador.")

    # El techo de lo que el esfuerzo podría ahorrar. Gratis, y acota la 4.
    salida_total = arriba.output_tokens + abajo.output_tokens
    p_salida_haiku = precio("claude-haiku-4-5")[1]
    coste_salida = salida_total * p_salida_haiku / 1_000_000
    print("\n  📏 EL TECHO DEL ESFUERZO, contado gratis y sin abrir la apuesta 4:")
    print(f"     la salida es {salida_total:,} de {total:,} tokens "
          f"({100*salida_total/total:.1f} %) y "
          f"{100*coste_salida/filas['todo haiku (lo medido)']:.1f} % del gasto.")
    print("     `effort` solo puede tocar ESA fracción. Aunque la redujera a")
    print("     CERO —que es imposible— el ahorro máximo sería ese porcentaje.")
    print("  🔑 Un techo que se calcula antes de medir no dice cuánto ahorrarás:")
    print("     dice cuánto NO puedes ahorrar. Y eso ya decide si vale la pena")
    print("     pagar la medición.")
    return filas


# ---------------------------------------------------------------------------
# 6.b) LA TRAMPA, VISTA MORDER — 🚨 ESTO SÍ LLAMA AL MODELO
# ---------------------------------------------------------------------------
#
# ⚠️ VA DETRÁS DE `--trampa` Y NUNCA EN PELADO. Es la deuda de `GUIDE.md` §6.e:
#    un archivo del nivel 8 que llama al modelo al ejecutarse sin bandera es una
#    factura que aparece cuando alguien solo quería comprobar que no rompió nada.
#
# 🎁 Y HAY UNA SORPRESA EN EL PRECIO: comprobar la mitad mala de la trampa es
#    GRATIS. Una petición rechazada con 400 no se factura — no hubo tokens que
#    cobrar. Lo único que se paga aquí es el CONTROL, o sea la prueba de que el
#    parámetro llega bien cuando el modelo sí lo entiende.
# 🔑 Sin ese control no habría medición: un error podría venir de que `effort` no
#    exista en haiku **o** de que lo estemos mandando mal. **Un experimento con
#    una sola celda no distingue la hipótesis del instrumento.**

def trampa_del_esfuerzo(verboso=True):
    """Le pide `effort` a haiku (debe fallar) y a sonnet (debe funcionar)."""
    print("=" * 72)
    print("  🎲 APUESTA 4 · primera mitad — LA TRAMPA DEL `effort`, PAGANDO")
    print("=" * 72)

    import anthropic          # noqa: E402

    # 🚨 EL FRENO DE CASA SE APAGA A PROPÓSITO PARA ESTA MEDICIÓN. `Capa` mata
    #    esto antes de salir de la máquina; aquí se rodea para preguntarle a la
    #    API de verdad si el freno tenía razón. Es `LM.13`: un freno que no has
    #    visto morder es una nota, y uno cuyo motivo no has comprobado es peor —
    #    es una nota que se cita como si fuera un dato.
    resultados = {}
    casos = [
        ("claude-haiku-4-5", "low", "debe FALLAR (generación anterior)"),
        ("claude-sonnet-5", "low", "debe FUNCIONAR (el control)"),
    ]
    gastado = 0.0
    for modelo, esfuerzo, espera in casos:
        print(f"\n  → {modelo} con effort={esfuerzo!r} — {espera}")
        try:
            r = agente.cliente.messages.create(
                model=modelo,
                max_tokens=16,
                output_config={"effort": esfuerzo},
                messages=[{"role": "user", "content": "Di OK y nada más."}],
            )
            costo = costo_de(r.usage, modelo)
            gastado += costo
            resultados[modelo] = {"ok": True, "costo": costo,
                                  "entrada": r.usage.input_tokens,
                                  "salida": r.usage.output_tokens}
            print(f"     ✅ pasó · {r.usage.input_tokens} entrada · "
                  f"{r.usage.output_tokens} salida · {_fmt(costo)}")
        except anthropic.APIStatusError as fallo:
            resultados[modelo] = {"ok": False, "codigo": fallo.status_code,
                                  "mensaje": str(fallo)[:300], "costo": 0.0}
            print(f"     🚨 {type(fallo).__name__} · HTTP {fallo.status_code}")
            print(f"     {str(fallo)[:300]}")
            print(f"     💸 $0,000000 — un 400 no se factura: no hubo tokens.")

    print("\n" + "-" * 72)
    print(f"  💸 Coste de la medición: {_fmt(gastado)}")
    return resultados, gastado



# ---------------------------------------------------------------------------
# 6.c) EL PASO QUE CUESTA — la corrida con OPUS ARRIBA y haiku abajo
# ---------------------------------------------------------------------------
#
# 🚨 DETRÁS DE `--pagar`, Y ARRANCA TRES WORKERS. Igual que `orquestador.py`.
#
# 🔑 Y SOLO SE PAGA UNA CORRIDA, NO DOS. La de haiku ya está pagada y grabada:
#    su árbol, su factura y su forma están en el registro desde la sesión 97.
#    **Comparar contra lo ya pagado es la mitad del ahorro de hoy**, y es C.1
#    quien lo hace posible: sin `corrida`, `id` y `padre` no habría con qué
#    comparar. La traza es la única pieza que no se puede añadir hacia atrás, y
#    hoy se cobra el interés de haberla puesto entonces.

def corrida_con_opus_arriba(verboso=True):
    """Corre A.3 con `opus-5` arriba y `haiku` abajo. Resuelve 5 y 6."""
    import orquestador as _orq          # noqa: E402

    print("=" * 72)
    print("  PASO 3 — LA CORRIDA QUE CUESTA: opus arriba, haiku abajo")
    print("=" * 72)

    arriba_antes, _, _ = sumar_registro(REGISTRO_ARRIBA)
    print("\n  Antes de correr, el registro tiene "
          f"{arriba_antes.llamadas} llamadas de la capa de arriba.")
    print("  Horquilla sellada para el día: $0,045-$0,060")

    r = _orq.correr_orquestador(
        _orq.TAREA_DEMO,
        capa=Capa("claude-opus-5"),
        capa_workers=Capa("claude-haiku-4-5"),
        verboso=verboso)

    print("\n" + "=" * 72)
    print("  LA FACTURA, CON CADA CAPA A SU PRECIO")
    print("=" * 72)
    print(f"  arriba (opus-5) : {_fmt(r['coste_orquestador_usd'])}  "
          f"({r['llamadas_api_orquestador']} llamadas · "
          f"{r['entrada_orquestador']} entrada / {r['salida_orquestador']} salida)")
    print(f"  abajo  (haiku)  : {_fmt(r['coste_workers_usd'])}  "
          f"({r['llamadas_api_workers']} llamadas · "
          f"{r['entrada_workers']} entrada / {r['salida_workers']} salida)")
    print(f"  TOTAL           : {_fmt(r['coste_total_usd'])}   en {r['segundos']} s")

    # 🔍 EL CONTRAFACTUAL QUE ANTES ERA IMPOSIBLE: qué habría dicho la
    #    contabilidad de ayer. Es gratis —los tokens ya se pagaron— y es la
    #    apuesta 1 vista en una factura de verdad, no en un recálculo.
    uso_arriba = Uso(entrada=r["entrada_orquestador"],
                     salida=r["salida_orquestador"])
    mentira = agente.costo(uso_arriba)
    print("\n  🚨 Lo que el harness de AYER habría reportado arriba: "
          f"{_fmt(mentira)}")
    print("     Lo que costó de verdad:                            "
          f"{_fmt(r['coste_orquestador_usd'])}")
    print(f"     Diferencia no vista: {_fmt(r['coste_orquestador_usd'] - mentira)}")
    return r


def comparar_arboles(verboso=True):
    """🎲 APUESTA 5 — el árbol de opus contra los árboles ya pagados de haiku."""
    import traza as _traza              # noqa: E402

    print("\n" + "=" * 72)
    print("  🎲 APUESTA 5 — ¿cambia el ÁRBOL al cambiar el modelo de arriba?")
    print("=" * 72)

    lineas = []
    for ruta in (REGISTRO_ARRIBA, REGISTRO_ABAJO):
        if ruta.exists():
            with open(ruta, encoding="utf-8") as f:
                lineas += [json.loads(l) for l in f if l.strip()]

    # 🐛 ARREGLADO EN CALIENTE, Y SE DEJA ESCRITO PORQUE ENSEÑA. La primera
    #    versión tomaba `orden[-1]` como «la corrida de hoy» — o sea la última
    #    en ORDEN DE ARCHIVO. Y aquí se concatenan DOS registros, arriba y luego
    #    abajo, así que la última del montón acabó siendo una corrida vieja de
    #    solo workers: el comparador señaló un árbol de UN nodo y lo llamó «hoy».
    # 🔑 El orden de un archivo no es el orden del tiempo, y solo coinciden
    #    mientras haya UN archivo. Ahora se ordena por la hora de la primera
    #    línea de cada corrida, que es un dato y no una casualidad de lectura.
    # ⚠️ Y el modo de fallo era el de siempre: NO dio error. Dibujó una tabla
    #    correcta con la fila equivocada resaltada, y el número de abajo salió
    #    verde. `LM.15` una vez más — nadie audita un verde.
    modelo_de = {}
    primera_hora = {}
    for l in lineas:
        c = l.get("corrida")
        if not c:
            continue
        h = l.get("hora", "")
        if c not in primera_hora or h < primera_hora[c]:
            primera_hora[c] = h
        if l.get("evento") == "llamada_api" and l.get("capa"):
            modelo_de.setdefault(c, l.get("modelo", "(sin anotar)"))
    orden = sorted(primera_hora, key=lambda c: primera_hora[c])

    def forma(corrida):
        """La FORMA del árbol: cuántos nodos hay a cada profundidad.

        📌 Se compara la forma y no los nombres a propósito: los `id` de tramo
           son un contador por proceso, así que dos corridas idénticas traen
           nombres distintos. Lo que la apuesta 5 afirma es que la ESTRUCTURA
           no cambia, no que los rótulos coincidan.
        """
        prof = {}
        vistos = set()
        for l in lineas:
            if l.get("corrida") != corrida:
                continue
            clave = (l.get("corrida"), l.get("id"))
            if clave in vistos:
                continue
            vistos.add(clave)
            prof[l.get("profundidad")] = prof.get(l.get("profundidad"), 0) + 1
        return tuple(sorted(prof.items()))

    hoy = orden[-1]
    print(f"\n  Corridas con parentesco en el registro: {len(orden)}")
    print(f"  {'corrida':<26} {'modelo arriba':<20} forma del árbol")
    print("  " + "-" * 74)
    # 📌 Solo se muestran y se comparan las corridas de DOS CAPAS. Las de un
    #    nodo son pruebas sueltas de un worker: comparar un fan-out contra ellas
    #    no dice nada, e inflaría el denominador con casos que nunca fueron el
    #    mismo experimento. Excluir lo que no es comparable es parte de medir.
    formas = {c: forma(c) for c in orden}
    de_dos_capas = [c for c in orden if len(formas[c]) > 1]
    for c in de_dos_capas:
        marca = "  <- hoy" if c == hoy else ""
        print(f"  {c:<26} {modelo_de.get(c, '(sin anotar)'):<20} "
              f"{formas[c]}{marca}")

    previas = [formas[c] for c in de_dos_capas if c != hoy]
    iguales = [f for f in previas if f == formas[hoy]]
    print(f"\n  Forma de hoy (opus arriba): {formas[hoy]}")
    print(f"  Corridas de dos capas previas: {len(previas)}")
    print(f"  …de ellas, con la MISMA forma: {len(iguales)}")

    quejas = _traza.auditar_arbol([l for l in lineas if l.get("corrida") == hoy])
    print(f"  Quejas del auditor sobre el árbol de hoy: {quejas or 'ninguna'}")
    return {"hoy": formas[hoy], "previas": previas, "iguales": len(iguales),
            "quejas": quejas}


def esfuerzo_medido(verboso=True):
    """🎲 APUESTA 4, segunda mitad — cuánto ahorra `effort` de verdad."""
    import orquestador as _orq          # noqa: E402

    print("\n" + "=" * 72)
    print("  🎲 APUESTA 4 · segunda mitad — ¿cuánto ahorra `effort` de verdad?")
    print("=" * 72)
    print("\n  ⚠️ SE MIDE UN TURNO, NO UNA CORRIDA, y se dice ANTES de dar el")
    print("     número: el primer turno del orquestador, con su system prompt y")
    print("     su menú de verdad, en sonnet-5, a `high` y a `low`. La entrada")
    print("     es idéntica en los dos, así que la única variable es la salida")
    print("     — que es justo lo que `effort` toca.")

    filas = {}
    gastado = 0.0
    for esf in ("high", "low"):
        r = agente.cliente.messages.create(
            model="claude-sonnet-5",
            max_tokens=1024,
            system=_orq.SISTEMA_ORQ,
            tools=_orq.TOOLS_ORQ,
            output_config={"effort": esf},
            messages=[{"role": "user", "content": _orq.TAREA_DEMO}],
        )
        c = costo_de(r.usage, "claude-sonnet-5")
        gastado += c
        filas[esf] = {"entrada": r.usage.input_tokens,
                      "salida": r.usage.output_tokens,
                      "costo": c, "stop": r.stop_reason}
        print(f"\n  effort={esf:<5} · {r.usage.input_tokens} entrada · "
              f"{r.usage.output_tokens} salida · {_fmt(c)} · {r.stop_reason}")

    ahorro = 1 - filas["low"]["costo"] / filas["high"]["costo"]
    ahorro_salida = 1 - filas["low"]["salida"] / max(filas["high"]["salida"], 1)
    print(f"\n  Ahorro en el COSTE del turno: {100*ahorro:.1f} %")
    print(f"  Ahorro en TOKENS DE SALIDA  : {100*ahorro_salida:.1f} %")
    print(f"  💸 Coste de esta medición: {_fmt(gastado)}")
    return filas, gastado


# ---------------------------------------------------------------------------
# 7) LAS PRUEBAS — sin modelo, sin red, $0,00
# ---------------------------------------------------------------------------

class _Uso:
    """Lo mínimo que `costo_de` necesita mirar. Lo único falso del archivo."""

    def __init__(self, entrada, salida):
        self.input_tokens = entrada
        self.output_tokens = salida


def _pruebas():
    rojas = []

    def check(nombre, cond, detalle=""):
        print(f"  {'✅' if cond else '❌'} {nombre}")
        if detalle:
            print(f"       {detalle}")
        if not cond:
            rojas.append(nombre.split(".")[0])

    print("=" * 72)
    print("  PRUEBAS DE C.6 — sin modelo, sin red, sin gastar")
    print("=" * 72)

    # --- 1 a 4 · el instrumento antes que la medida ------------------------
    u = _Uso(1_000_000, 0)
    check("1. `costo_de` con un millón de entrada da el precio de tabla",
          costo_de(u, "claude-haiku-4-5") == 1.00,
          costo_de(u, "claude-haiku-4-5"))
    u2 = _Uso(0, 1_000_000)
    check("2. …y con un millón de salida, el otro precio de tabla",
          costo_de(u2, "claude-opus-5") == 25.00, costo_de(u2, "claude-opus-5"))

    malo = None
    try:
        precio("claude-haiku-45")
    except ModeloDesconocido as e:
        malo = str(e)
    check("3. un modelo que no existe muere ANTES de calcular nada",
          malo is not None and "catálogo" in malo, malo)

    # 🔑 La prueba que convierte el instrumento en creíble: con el MISMO
    #    modelo, la función nueva y la del harness tienen que dar lo mismo.
    #    Si no, todo lo que mida hoy es basura.
    u3 = _Uso(44813, 6107)
    check("4. con el mismo modelo, `costo_de` == `agente.costo` (LM.66)",
          abs(costo_de(u3, agente.MODELO) - agente.costo(u3)) < 1e-12,
          f"{costo_de(u3, agente.MODELO)} vs {agente.costo(u3)}")

    # --- 5 a 9 · la configuración de capa ----------------------------------
    check("5. una `Capa` sin argumentos hereda el modelo del nivel",
          Capa().modelo == agente.MODELO, Capa())
    check("6. una `Capa` sin esfuerzo NO añade nada a la petición",
          Capa().extras_de_peticion() == {}, Capa().extras_de_peticion())
    check("7. con esfuerzo, añade `output_config`",
          Capa("claude-opus-5", "low").extras_de_peticion()
          == {"output_config": {"effort": "low"}},
          Capa("claude-opus-5", "low").extras_de_peticion())

    # 🚨 LA TRAMPA, CONVERTIDA EN FRENO. Está verificada contra la
    #    documentación, no contra la memoria, y aquí se le exige morder.
    mordio = None
    try:
        Capa("claude-haiku-4-5", "low")
    except EsfuerzoNoSoportado as e:
        mordio = str(e)
    check("8. pedirle `effort` a haiku muere en casa, no en la API",
          mordio is not None and "generación anterior" in mordio, mordio)

    esf_malo = None
    try:
        Capa("claude-opus-5", "altísimo")
    except EsfuerzoNoSoportado as e:
        esf_malo = str(e)
    check("9. un esfuerzo que no existe también muere en casa",
          esf_malo is not None, esf_malo)

    # --- 10 a 14 · LAS APUESTAS, exigidas como pruebas ---------------------
    #
    # ⭐ Se escriben como pruebas y no como prosa a propósito: una apuesta
    #    contada en el README envejece sin avisar. Una apuesta que es una
    #    prueba se pone ROJA el día que alguien arregla lo que describe — y
    #    entonces hay que venir a tacharla a mano, que es justo lo que se
    #    quiere. Es `LM.13` aplicado a las propias apuestas.

    # 🚨 SE MIRAN SOLO LAS LÍNEAS ANTERIORES A C.6, Y ESO ES UN ARREGLO DE HOY,
    #    NO UNA COMODIDAD. Estas pruebas describen el registro que existía antes
    #    del cableado; al correr la primera corrida con opus, sumar el archivo
    #    entero y tarifarlo a precio de haiku dejó de tener sentido y **las
    #    pruebas 11 y 13 se pusieron rojas en el acto**.
    # 🔑 Y así se supo que la corrección anterior también era imprecisa: se dijo
    #    que estas pruebas «describen el mundo de ayer y el mundo de ayer nunca
    #    se pone rojo». Falso — describían un ARCHIVO QUE CRECE. El pasado no
    #    cambia; el archivo donde está guardado, sí. **Un dato histórico solo es
    #    inmutable si tiene cómo separarse de lo que se le añade encima**, y aquí
    #    la marca es la ausencia del campo `modelo`.
    arriba, grabado_arriba, campos_arriba = sumar_registro(REGISTRO_ARRIBA,
                                                          antes_de_c6)
    abajo, grabado_abajo, campos_abajo = sumar_registro(REGISTRO_ABAJO,
                                                       antes_de_c6)
    nuevas_ar, _, campos_nuevos = sumar_registro(
        REGISTRO_ARRIBA, lambda d: not antes_de_c6(d))

    check("10. hay tokens ya pagados que leer (si no, no hay medición)",
          arriba.llamadas > 0 and abajo.llamadas > 0,
          f"arriba {arriba.llamadas} · abajo {abajo.llamadas} llamadas")

    check("11. el recálculo reproduce lo grabado ANTES de C.6, al sexto decimal",
          abs(costo_de(arriba, agente.MODELO) - grabado_arriba) < 5e-4
          and abs(costo_de(abajo, agente.MODELO) - grabado_abajo) < 5e-4,
          f"arriba {costo_de(arriba, agente.MODELO):.6f} vs {grabado_arriba:.6f}")

    # 🎲 APUESTA 1
    real = costo_de(arriba, "claude-opus-5")
    reportado = agente.costo(arriba)
    check("12. 🎲 APUESTA 1 — `agente.costo` sigue tarifando con la tabla del "
          "módulo, y el factor es exacto",
          abs(real / reportado - 5.0) < 1e-9,
          f"real {real:.6f} · reportado {reportado:.6f} · "
          f"factor {real/reportado:.10f}×")

    # 🎲 APUESTA 2
    check("13. 🎲 APUESTA 2 — ninguna línea anterior a C.6 anota el modelo",
          "modelo" not in campos_arriba and "modelo" not in campos_abajo,
          f"{arriba.llamadas + abajo.llamadas} líneas · "
          f"campos arriba: {sorted(campos_arriba)}")

    # 🎁 Y LA OTRA MITAD, QUE ES LA QUE VALE: el registro de HOY sí lo dice. La
    #    apuesta 2 se ganó describiendo un agujero; esta línea comprueba que el
    #    agujero está tapado, y se puso verde con la primera corrida pagada.
    check("13b. …y toda línea posterior a C.6 SÍ lo anota",
          nuevas_ar.llamadas > 0 and "modelo" in campos_nuevos,
          f"{nuevas_ar.llamadas} líneas nuevas · "
          f"{'modelo' in campos_nuevos}")

    # 🎲 APUESTA 3
    una = Uso(entrada=4425, salida=45)
    cabe_haiku = costo_de(una, "claude-haiku-4-5") < PRESUPUESTO_ORQ_USD
    cabe_opus = costo_de(una, "claude-opus-5") < PRESUPUESTO_ORQ_USD
    check("14. 🎲 APUESTA 3 — el techo en dólares NO corta con ninguno de los dos",
          cabe_haiku and cabe_opus,
          f"haiku {costo_de(una,'claude-haiku-4-5'):.6f} · "
          f"opus {costo_de(una,'claude-opus-5'):.6f} · "
          f"techo {PRESUPUESTO_ORQ_USD}")

    # --- 15 y 16 · lo que la apuesta 1 hace INVISIBLE -----------------------
    #
    # 🚨 ESTA ES LA PAREJA QUE MÁS ENSEÑA, y no prueba que algo funcione:
    #    prueba que un control NO PUEDE VER el fallo. Las partes siguen sumando
    #    el total aunque la tabla de precios sea la equivocada, así que ningún
    #    cuadre interno se entera.
    mitad_a, mitad_b = _Uso(20000, 3000), _Uso(24813, 3107)
    entero = _Uso(44813, 6107)
    suma_mala = agente.costo(mitad_a) + agente.costo(mitad_b)
    check("15. con la tabla MALA, las partes siguen sumando el total",
          abs(suma_mala - agente.costo(entero)) < 1e-12,
          f"{suma_mala:.9f} == {agente.costo(entero):.9f}")
    suma_buena = (costo_de(mitad_a, "claude-opus-5")
                  + costo_de(mitad_b, "claude-opus-5"))
    check("16. …y con la BUENA también. El cuadre es ciego a la tarifa",
          abs(suma_buena - costo_de(entero, "claude-opus-5")) < 1e-12,
          f"{suma_buena:.9f} == {costo_de(entero, 'claude-opus-5'):.9f}")

    # --- 17 a 22 · EL ARREGLO, VISTO MORDER --------------------------------
    #
    # 🚨 ESTAS SEIS EXISTEN POR UN DEFECTO DE LAS OTRAS, Y SE DEJA ESCRITO.
    #    Al cablear C.6 se esperaba que las pruebas 12 y 13 se pusieran rojas, y
    #    NO se pusieron — porque no podían. La 12 interroga a `agente.costo`,
    #    que nadie tocó (el arreglo fue dejar de LLAMARLA en los dos bucles), y
    #    la 13 interroga a 191 líneas ya grabadas, que son historia y no cambian.
    # 🔑 Las dos son ciertas y las dos son inútiles como vigilancia: **describen
    #    el mundo de ayer, y el mundo de ayer nunca se pone rojo.** Es la prueba
    #    que no podía fallar de la sesión 103, otra vez, y esta vez la escribí yo
    #    dentro del archivo donde se cuenta esa lección.
    # ✅ Lo que sigue SÍ se pone rojo si alguien deshace el cableado.

    import types                              # noqa: E402
    import orquestador as _orq                # noqa: E402
    import worker as _w                       # noqa: E402

    class _ClienteEspia:
        """Contesta una vez y APUNTA con qué se le pidió. Nada de red."""

        def __init__(self):
            self.peticiones = []
            self.messages = types.SimpleNamespace(create=self._create)

        def _create(self, **kw):
            self.peticiones.append(kw)
            return types.SimpleNamespace(
                stop_reason="end_turn",
                content=[types.SimpleNamespace(type="text", text="listo")],
                usage=_Uso(1000, 200))

    def _correr(capa_pedida):
        espia = _ClienteEspia()
        real = agente.cliente
        carpeta = None
        try:
            agente.cliente = espia
            with _orq.registro_desviado() as carpeta:
                res = _w.correr_worker("da igual", nombre="usd",
                                       capa=capa_pedida, verboso=False)
                lineas = [json.loads(l) for l in
                          open(_w.REGISTRO, encoding="utf-8")]
        finally:
            agente.cliente = real
        return espia, res, lineas

    espia_o, res_o, lineas_o = _correr(Capa("claude-opus-5"))
    espia_h, res_h, _ = _correr(None)

    check("17. el modelo de la CAPA llega a la petición",
          espia_o.peticiones[0]["model"] == "claude-opus-5",
          espia_o.peticiones[0]["model"])
    check("18. sin capa, sigue siendo el de siempre (nada de lo medido cambia)",
          espia_h.peticiones[0]["model"] == agente.MODELO,
          espia_h.peticiones[0]["model"])
    check("19. …y sin esfuerzo NO se manda `output_config`",
          "output_config" not in espia_h.peticiones[0],
          sorted(espia_h.peticiones[0]))

    # 🔑 LA QUE MÁS VALE: el mismo gasto de tokens, tarifado a 5×. Antes del
    #    cableado estas dos cifras eran IGUALES, y ese era todo el agujero.
    check("20. el coste sale del precio de la capa: opus cuesta 5× lo mismo",
          abs(res_o["coste_usd"] / res_h["coste_usd"] - 5.0) < 1e-6,
          f"opus {res_o['coste_usd']:.6f} · haiku {res_h['coste_usd']:.6f}")

    con_modelo = [l for l in lineas_o
                  if l.get("evento") == "llamada_api" and "modelo" in l]
    check("21. la línea nueva del registro SÍ dice qué modelo la hizo",
          len(con_modelo) > 0 and con_modelo[0]["modelo"] == "claude-opus-5",
          con_modelo[0] if con_modelo else "ninguna")

    espia_e, _, _ = _correr(Capa("claude-sonnet-5", "low"))
    check("22. el esfuerzo también viaja hasta la petición",
          espia_e.peticiones[0].get("output_config") == {"effort": "low"},
          espia_e.peticiones[0].get("output_config"))

    print("-" * 72)
    if rojas:
        print(f"  ❌ {len(rojas)} prueba(s) en rojo: {rojas}")
    else:
        print("  ✅ las 23 pruebas, verdes, y no costaron nada.")
        print("     🎲 Las 12, 13 y 14 describen LO DE AYER: `agente.costo` sin")
        print("        tocar y 191 líneas ya grabadas. Son ciertas y no vigilan")
        print("        nada — se dejan porque son el registro de las apuestas.")
        print("     ✅ Las 17 a 22 son las que vigilan: se ponen rojas si")
        print("        alguien deshace el cableado de C.6. Y la 20 es la que")
        print("        mata el agujero: antes, opus y haiku costaban IGUAL.")
    print("=" * 72)
    return not rojas


def main(argv):
    if "--pruebas" in argv:
        return 0 if _pruebas() else 1

    if "--trampa" in argv:
        trampa_del_esfuerzo()
        return 0

    if "--pagar" in argv:
        r = corrida_con_opus_arriba()
        comparar_arboles()
        _, gasto_esf = esfuerzo_medido()
        total = r["coste_total_usd"] + gasto_esf
        print("\n" + "=" * 72)
        print(f"  TOTAL DEL PASO 3: {_fmt(total)}")
        print("  Horquilla sellada (apuesta 6): $0,045-$0,060")
        print("=" * 72)
        return 0

    print("=" * 72)
    print("  C.6 — MODELO Y ESFUERZO POR CAPA · PASO 1, SIN PAGAR")
    print("=" * 72)
    apuesta_1_el_precio_del_modulo()
    apuesta_2_el_registro_no_lo_dice()
    apuesta_3_el_presupuesto_en_dolares()
    tabla_de_configuraciones()
    print("\n📌 Coste de todo esto: $0,000000. Los tokens ya estaban pagados;")
    print("   volver a tarifarlos es aritmética.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
