"""
herramientas.py — Las 5 herramientas del agente de divisas (nivel 5b).

Python puro. Este archivo NO sabe que Claude existe:
no importa `anthropic`, no lee la API key, no llama al modelo.

Por eso se puede probar entero sin gastar un centavo (ver evals.py).

Contrato de todas las herramientas de este archivo:
devuelven SIEMPRE un diccionario. Si algo sale mal, ese diccionario trae
la llave "error" con un texto que el MODELO va a leer para reintentar.
Ninguna lanza excepciones: el bucle del agente no se debe caer por un dato malo.
"""

import datetime
import json
import string
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

# La única lista de monedas del proyecto.
DECIMALES = {"COP": 0, "USD": 2, "EUR": 2, "CAD": 2}
# Las monedas aceptadas SON las llaves de DECIMALES. No se pueden desincronizar.
MONEDAS = tuple(DECIMALES)

# Las dos fuentes de datos. Gratis y sin llave. Verificadas el 2026-07-30.
# ⚠️ El espacio de "vigenciadesde DESC" va como %20: urllib NO acepta espacios
# crudos en una URL (revienta con InvalidURL). curl sí los aceptaba, y por eso
# el README traía la versión que no funciona en Python.
URL_MERCADO = "https://open.er-api.com/v6/latest/USD"
URL_TRM_BASE = "https://www.datos.gov.co/resource/32sa-8pi3.json"
URL_TRM = URL_TRM_BASE + "?$order=vigenciadesde%20DESC&$limit="

# Le pregunta a la fuente cuál es su PRIMER y su ÚLTIMO dato, en una sola
# llamada. Sirve para explicar por qué una fecha no tiene TRM sin mirar el
# reloj de la máquina: la fuente es su propio calendario.
# Verificado el 2026-07-30: primera 1991-12-02, ultima 2026-07-30.
URL_TRM_RANGO = (URL_TRM_BASE + "?$select=" + urllib.parse.quote(
    "min(vigenciadesde) AS primera, max(vigenciahasta) AS ultima"))

# El formato EXACTO que se acepta para una fecha. No es decoración: es la
# lista de permitidos que corta la inyección (ver trm_en_fecha).
FORMATO_FECHA = "%Y-%m-%d"      # o sea AAAA-MM-DD, como "2026-07-30"

# El tope de registros que historial() acepta pedir.
# 260 filas son ~un año (52 semanas x 5 publicaciones), así que 400 da año y
# medio largo: de sobra para cualquier pregunta de un agente de divisas.
# ⚠️ Este tope NO protege nuestros tokens: historial devuelve un RESUMEN, que
# pesa lo mismo con 30 filas que con 400. Protege al servidor del gobierno y al
# usuario, que si no se queda esperando. Un 100000 no es basura: es un número
# perfectamente válido con el que el modelo puede hacer un destrozo sin querer.
MAX_REGISTROS = 400

# La caja: la única carpeta donde guardar_reporte puede escribir.
CAJA = Path(__file__).resolve().parent / "caja"

# Los caracteres que puede llevar el nombre de un reporte:
# letras, números, guion, guion bajo y el punto del ".txt".
PERMITIDOS = string.ascii_letters + string.digits + "-_."


# ---------------------------------------------------------------------------
# Ayudantes internos (NO son herramientas: el modelo nunca las llama,
# no entran en la lista `tools` que se le manda)
# ---------------------------------------------------------------------------

def es_numero(x):
    """True si `x` es un número con el que se puede operar dinero.

    Los booleanos NO cuentan, aunque Python diga que sí: `True` es un `int`
    por historia del lenguaje (vale 1), así que isinstance(True, int) es True
    y `True * 3900` da 3900 sin protestar. Un booleano donde va un monto es
    siempre un error de quien llamó, no una cantidad.
    """
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def es_texto(x):
    """True si `x` es una cadena de texto.

    Hace falta porque el modelo manda JSON, y en JSON una lista se escribe igual
    de fácil que un texto. Y los métodos de texto no perdonan:
    `[].endswith(".txt")` no devuelve False, lanza AttributeError.
    """
    return isinstance(x, str)


def es_moneda(x):
    """True si `x` es una de las monedas que este proyecto maneja.

    Junta las DOS preguntas a propósito: ¿es texto? y ¿está en la lista?
    Antes solo se preguntaba lo segundo (`x in DECIMALES`), y eso funcionaba
    por casualidad: la prueba de pertenencia en un diccionario hace de paso un
    control de tipo... pero solo para valores HASHABLES. Con `de=123` decía
    "no la manejo" (bien) y con `de=[]` lanzaba
    `TypeError: unhashable type: 'list'` y tumbaba el bucle del agente.
    La casualidad servía y tenía un borde. Aquí la regla queda explícita.
    """
    return es_texto(x) and x in DECIMALES


def pedir_json(url, intentos=3, timeout=8):
    """Pide un JSON por internet. Devuelve (datos, error): uno es None, el otro no.

    Reintenta solo los fallos PASAJEROS (red caída, tiempo vencido). Esos no
    necesitan criterio: la única respuesta sensata es volver a intentar, y
    reintentar AQUÍ cuesta $0.00 porque el modelo nunca se enteró. Si en cambio
    devolviéramos el error para que el modelo reintente, cada reintento sería
    una vuelta más del bucle agéntico: se repaga el SYSTEM, el menú de las 5
    herramientas y el historial completo, para preguntar lo mismo otra vez.

    Los PERMANENTES (el servidor SÍ contestó, y contestó "no") salen de una:
    esperar no arregla una URL mal escrita.

    Regla del nivel: reintenta donde sea más barato; que el modelo decida solo
    lo que necesita criterio (p. ej. "es domingo y no hay TRM nueva, ¿qué hago?").

    OJO con lo que NO se atrapa aquí: no hay `except Exception`. Un defecto de
    nuestro propio código (un NameError, un typo) NO se disfraza de "problemas
    de conexión" — se cae fuerte y se ve. Un error del mundo es información;
    un error nuestro es un defecto, y taparlo lo deja vivo para siempre.
    → DEUDA DEL PASO 8: la red de seguridad va en el harness (agente.py), no
      aquí. Allá un `try` alrededor de CUALQUIER herramienta le dice al modelo
      "falló por un defecto interno" y a nosotros nos imprime el traceback:
      el bucle sobrevive Y el bug queda visible. Misma forma que el permiso del
      nivel 4, que se pedía en el harness y no dentro de borrar_archivo().
    """
    ultimo = "No se pudo consultar la fuente."   # existe antes del for: si
    espera = 1                                   # intentos=0, el return final
                                                 # la necesita igual.
    for intento in range(1, intentos + 1):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8")), None

        # PERMANENTE — el servidor contestó, y contestó "no" (404, 403, 500...).
        # Va PRIMERO porque HTTPError es HIJO de URLError: con el padre arriba,
        # esta línea sería inalcanzable y un 404 se reintentaría 3 veces.
        # Se comprobó corriéndolo: con el orden invertido, un 404 real se
        # reportaba como "problemas de conexión" con el internet perfecto.
        # El número (e.code) va en el mensaje a propósito: un 404 dice "la URL
        # está mal, no insistas" y un 503 dice "vuelve más tarde". No son lo
        # mismo, y el modelo solo puede distinguirlos si se lo decimos.
        except urllib.error.HTTPError as e:
            return None, f"La fuente respondió con error HTTP {e.code}."

        # PASAJEROS — no hubo respuesta: red caída, DNS, o se venció el tiempo.
        # NO hay `return` aquí a propósito: guarda el motivo y deja que el `for`
        # dé otra vuelta. Un `return` en esta rama borraría los reintentos.
        except (urllib.error.URLError, TimeoutError) as e:
            ultimo = f"No pude conectarme a la fuente ({type(e).__name__})."
            if intento < intentos:
                time.sleep(espera)
                espera = espera * 2   # 1s, luego 2s: espera exponencial (nivel 4).
                                      # Mil clientes reintentando cada segundo
                                      # saturan más al servidor que ya tosía.

    # Solo se llega aquí si se agotaron los intentos sin lograr conectar.
    # ⚠️ timeout e intentos se MULTIPLICAN: 3 x 8s = hasta 24s colgado, más las
    # esperas. El timeout es POR INTENTO (medido en el nivel 4).
    return None, ultimo


# ---------------------------------------------------------------------------
# Herramientas que no tocan internet
# ---------------------------------------------------------------------------

def convertir(monto, de, a, tasa):
    """Convierte `monto` de la moneda `de` a la moneda `a` usando `tasa`.

    La tasa entra como PARÁMETRO, no la busca esta función. Así convertir()
    es pura aritmética: mismos datos de entrada, mismo resultado, siempre.
    Quien consigue la tasa es otra herramienta (una que sí toca internet).
    """
    # --- Frenos de FORMA: ¿se puede operar con esto? ---
    # Van primero porque si el dato no es un número, la función no puede hacer
    # nada en absoluto. Sin estos dos, un monto de texto o una tasa vacía
    # lanzaban TypeError y tumbaban el bucle del agente entero.
    # Un {"error": ...} es una conversación; un TypeError es un funeral.
    if not es_numero(monto):
        return {"error": f"El monto debe ser un número, no {type(monto).__name__}. "
                         f"Ejemplo: 100 o 99.5 (sin comillas)."}
    if not es_numero(tasa):
        return {"error": f"La tasa debe ser un número, no {type(tasa).__name__}. "
                         f"Ejemplo: 3900 o 3900.75 (sin comillas)."}

    # --- Frenos de CONTENIDO: es un dato operable, ¿pero tiene sentido? ---
    # Un monto negativo siempre es un accidente: el modelo traduce lo que
    # escribió un humano, y nadie pide convertir menos cien dólares.
    # El monto CERO sí se acepta: es raro pero no es un error, y devuelve 0.
    if monto < 0:
        return {"error": "El monto no puede ser negativo."}

    # Una tasa de cambio menor o igual a cero no existe en el mundo real.
    # El 0 va en el mismo `if` a propósito: por separado, la tasa 0 devolvía 0
    # y un 0 se ve como una respuesta legítima. Es el error más silencioso
    # que tenía esta función.
    if tasa <= 0:
        return {"error": "La tasa debe ser mayor que cero."}

    # es_moneda revisa DOS cosas de una: que sea texto y que esté en la lista.
    # Con `de not in DECIMALES` a secas, un `de=[]` lanzaba TypeError.
    # El mensaje dice "entre comillas" — es el espejo del "sin comillas" de los
    # frenos numéricos de arriba: al modelo hay que decirle la FORMA del JSON.
    if not es_moneda(de):
        return {"error": f"No manejo la moneda {de!r}. "
                         f"Solo: {', '.join(MONEDAS)} (como texto, entre comillas)."}
    if not es_moneda(a):
        return {"error": f"No manejo la moneda {a!r}. "
                         f"Solo: {', '.join(MONEDAS)} (como texto, entre comillas)."}

    # Cada moneda se redondea distinto: los pesos no llevan centavos.
    # Los dos round() NO son el mismo: round(3.7, 0) devuelve 4.0 (decimal) y
    # round(3.7) devuelve 4 (entero). Para COP hace falta el segundo, o el
    # agente diría "son 39000.0 pesos".
    decimales = DECIMALES[a]
    if decimales == 0:
        resultado = round(monto * tasa)
    else:
        resultado = round(monto * tasa, decimales)

    return {
        "monto": monto,
        "de": de,
        "a": a,
        "tasa": tasa,
        "resultado": resultado,
    }


def guardar_reporte(nombre, contenido):
    """Escribe un reporte de texto, pero solo dentro de caja/.

    El `nombre` lo elige el MODELO, así que es un dato que llega de afuera y
    hay que revisarlo antes de tocar el disco. Los tres frenos van primero:
    si escribes y después validas, ya escribiste.
    """
    # Freno 0 — la FORMA, y va antes que todo lo demás: los frenos 1 y 2 usan
    # métodos de texto, y un método de texto sobre una lista no devuelve False,
    # lanza AttributeError. `[].endswith(".txt")` era un funeral, no un rechazo.
    # Mismo orden que en convertir(): primero la forma, después el contenido.
    if not es_texto(nombre):
        return {"error": f"El nombre debe ser texto, no {type(nombre).__name__}. "
                         f"Ejemplo: \"reporte.txt\" (entre comillas)."}
    if not es_texto(contenido):
        return {"error": f"El contenido debe ser texto, no {type(contenido).__name__}. "
                         f"Un contenido vacío sí se acepta: \"\"."}

    # Freno 1 — la extensión. Además de ordenar, corta rutas como "../../.env".
    if not nombre.endswith(".txt"):
        return {"error": "El nombre debe terminar en .txt"}

    # Freno 2 — lista de PERMITIDOS (allowlist), no lista de prohibidos:
    # lo que no se me ocurrió también queda afuera.
    if not all(c in PERMITIDOS for c in nombre):
        return {"error": "Solo se aceptan letras, números, guiones (- _) y el punto del .txt."}

    # Freno 3 — hoy es REDUNDANTE y se deja a propósito.
    # Se probaron por fuerza bruta los 278.916 nombres posibles: ninguno con ".."
    # logra salirse de caja/, porque escapar necesita "/" o "\" y el freno 2 ya
    # los prohíbe. Existe para el día que alguien afloje PERMITIDOS (p. ej. para
    # permitir subcarpetas): ese día pasa de inútil a ser el único que queda.
    if ".." in nombre:
        return {"error": "El nombre no puede llevar .."}

    # Pasó los tres frenos. Ahora sí se toca el disco.
    CAJA.mkdir(exist_ok=True)
    ruta = CAJA / nombre
    ruta.write_text(contenido, encoding="utf-8")

    return {"guardado": nombre, "caracteres": len(contenido)}


# ---------------------------------------------------------------------------
# Herramientas que SÍ tocan internet
# ---------------------------------------------------------------------------

def tasa(de, a):
    """Tasa de cambio de MERCADO entre dos monedas, vía open.er-api.com.

    La API entrega todo medido contra el dólar (base_code = "USD"), así que un
    par como EUR->COP no viene en el JSON: se calcula pasando por el dólar,
    rates[a] / rates[de]. Y como rates["USD"] vale 1, la misma fórmula sirve
    cuando una de las dos monedas ES el dólar: no hace falta un caso especial.

    Devuelve un dict PEQUEÑO. La fuente manda 166 monedas y 11 llaves (~2.967
    caracteres) y aquí se manejan 4: lo que devuelve una herramienta se reenvía
    en CADA vuelta que le quede a la conversación, así que un tool_result gordo
    es un impuesto permanente. Se conserva `actualizado` porque sí se gana sus
    tokens: mercado y TRM oficial dan números distintos para "el dólar de hoy"
    (el 2026-07-30, 3207,64 contra 3206,18), y una tasa sin fecha ni fuente es
    correcta e inútil a la vez.
    """
    # --- Frenos de moneda: los mismos de convertir(), y ANTES de gastar red ---
    # Si validas después de pedir el dato, ya gastaste la llamada. Es la misma
    # razón por la que los frenos de guardar_reporte van antes de tocar el disco.
    # No se hace .upper(): "usd" en minúscula se rechaza, decidido a conciencia.
    if not es_moneda(de):
        return {"error": f"No manejo la moneda {de!r}. "
                         f"Solo: {', '.join(MONEDAS)} (como texto, entre comillas)."}
    if not es_moneda(a):
        return {"error": f"No manejo la moneda {a!r}. "
                         f"Solo: {', '.join(MONEDAS)} (como texto, entre comillas)."}

    # --- El dato viene de afuera ---
    datos, error = pedir_json(URL_MERCADO)
    if error:
        # El error de red se reenvía tal cual: ya viene redactado para que el
        # modelo lo lea y decida. Envolverlo en otro texto solo gasta tokens.
        return {"error": error}

    # --- Frenos sobre la RESPUESTA del servidor ---
    # Hasta ahora desconfiábamos del modelo. Este dato lo manda un servidor que
    # no es nuestro: también hay que revisarlo. Puede cambiar de formato, quitar
    # una moneda o mandar null, y nadie nos va a avisar.
    # .get() devuelve None si la llave no está, y es_numero(None) es False:
    # un solo freno cubre tres desastres (llave ausente, null, y texto).
    rates = datos.get("rates", {})
    valor_de = rates.get(de)
    valor_a = rates.get(a)
    if not es_numero(valor_de) or not es_numero(valor_a):
        return {"error": f"La fuente no trajo un valor numérico para {de} o {a}."}

    # Sin este freno, un 0 en la fuente lanzaría ZeroDivisionError y tumbaría el
    # bucle del agente. Es el mismo razonamiento que `tasa <= 0` en convertir():
    # una tasa de cambio positiva no es una opción, es la definición.
    if valor_de <= 0:
        return {"error": f"La fuente reportó un valor imposible para {de}."}

    # ⚠️ ESTE FRENO LLEGÓ CON EL PUENTE DE ABAJO, y no es de adorno:
    #    la llave inversa divide entre valor_a. Sin esta línea, un 0 en la
    #    fuente para la moneda de destino sería ZeroDivisionError — el mismo
    #    funeral que evita el freno de arriba, pero por la otra división.
    #    → Cada número nuevo que devuelves puede traer su propia forma de
    #      reventar. El freno se escribe junto con el dato, no después.
    if valor_a <= 0:
        return {"error": f"La fuente reportó un valor imposible para {a}."}

    return {
        "de": de,
        "a": a,
        "tasa": valor_a / valor_de,

        # 🚨 EL PUENTE. Llegó en la sesión 17, y lo pidió un defecto REAL que
        #    encontró la rúbrica del paso 10.
        #
        #    Qué pasó: le preguntaron "¿cuál es la tasa de mercado del dólar?",
        #    el modelo llamó tasa(de="COP", a="USD") y recibió
        #    0.0003117558994603884. Para poder contestar en pesos tenía que
        #    invertirla — y NADIE le había dado ese número. Así que lo calculó
        #    en su cabeza y le salió 3.209,64 cuando el verdadero es 3.207,64.
        #
        #    ⭐ DOS PESOS DE ERROR, Y NINGÚN EVAL PODÍA VERLO: la cuenta ocurrió
        #       dentro del modelo y salió directo al texto, sin pasar por
        #       convertir() ni por ninguna herramienta. Es el "número creíble"
        #       en su forma más difícil de detectar: se ve exactamente como
        #       debería verse.
        #
        #    Es EXACTAMENTE el mismo hueco que trm() cerró en la sesión 15 con
        #    usd_por_1_cop, en la otra herramienta. Y la solución es la misma, y
        #    no es prohibir: PROHIBIR SIN OFRECER SALIDA ES UN CALLEJÓN. Si el
        #    modelo calcula a escondidas, casi siempre es porque le falta un
        #    puente — no porque le guste.
        #
        #    El nombre se arma solo, con las monedas adentro: para
        #    tasa("COP","USD") sale "cop_por_1_usd". Así el modelo no tiene que
        #    acordarse de qué lado es cuál: lo dice la llave.
        #
        #    Y se divide valor_de/valor_a en vez de 1/tasa a propósito: hacer la
        #    cuenta sobre los números originales evita redondear dos veces.
        f"{de.lower()}_por_1_{a.lower()}": round(valor_de / valor_a, 10),

        "fuente": "mercado (open.er-api.com)",
        "actualizado": datos.get("time_last_update_utc", "fecha no informada"),
    }


def trm():
    """La TRM oficial de Colombia (datos.gov.co): la del día más reciente.

    No lleva parámetro `dias` a propósito. Si `trm` supiera traer varios días
    haría a medias el trabajo de `historial`, y dos herramientas que se pisan
    obligan al modelo a elegir entre dos caminos para lo mismo. Una cosa cada una.

    ⚠️ La TRM y la tasa de mercado NO son el mismo número. El 2026-07-30 fueron
    3206,18 y 3207,64. La TRM es la oficial (la que sirve para impuestos y
    contabilidad); el mercado es a cuánto se está negociando. Por eso las dos
    herramientas existen, y por eso las dos dicen de dónde salió su dato.

    ⚠️ EL DOMINGO NO HAY TRM NUEVA: la del viernes sigue vigente el sábado y el
    domingo (la del 25 de julio valió hasta el 27). Esta función NO decide qué
    hacer con eso: devuelve `vigente_desde` y `vigente_hasta` bien visibles y
    la decisión sube al MODELO — usar la del viernes y avisar que es del
    viernes, o decirle al usuario que espere, ES CRITERIO, y el criterio no lo
    toma un `if`. Es la regla del paso 6: reintenta/resuelve donde sea más
    barato, y que el modelo decida solo lo que necesita juicio.

    ⚠️ Y por eso tampoco calcula "¿es de hoy?": para eso tendría que mirar el
    reloj, y entonces la función dependería de DOS mundos (la fuente y la hora
    de la máquina) y dejaría de ser probable con datos fijos. Si el agente
    necesita saber la fecha de hoy, eso es OTRA herramienta — como `hora_utc`
    en el nivel 3.
    """
    # La URL ya termina en "&$limit=", así que se le pega el número.
    datos, error = pedir_json(URL_TRM + "1")
    if error:
        return {"error": error}

    # --- Frenos sobre la respuesta: aquí la fuente devuelve una LISTA ---
    # Es distinto de la API de mercado, que devuelve un diccionario. Si llega
    # otra cosa, o llega vacía, no hay nada que leer y datos[0] sería un funeral.
    if not isinstance(datos, list) or not datos:
        return {"error": "La fuente oficial no devolvió ninguna fila de TRM."}

    fila = datos[0]
    if not isinstance(fila, dict):
        return {"error": "La fila de TRM no tiene el formato esperado."}

    # ⚠️ AQUÍ ESTÁ LA DIFERENCIA GRANDE CON tasa(): el valor viene como TEXTO.
    # El JSON real dice  "valor":"3206.18"  — con comillas. Hay que convertirlo,
    # y convertir puede fallar. Van dos frenos porque son dos preguntas
    # distintas, igual que en convertir(): primero la FORMA, después el CONTENIDO.
    valor_crudo = fila.get("valor")

    # Freno de FORMA: descarta None, listas, diccionarios y booleanos.
    # (es_numero rechaza los booleanos: True no es una cantidad de dinero.)
    if not es_texto(valor_crudo) and not es_numero(valor_crudo):
        return {"error": f"La fuente mandó un valor de TRM que no se puede leer "
                         f"({type(valor_crudo).__name__})."}

    # Freno de CONTENIDO: es texto, pero ¿es un número escrito?
    # float("abc") y float("") lanzan ValueError. Y ojo con float("3.206,18"):
    # también revienta, porque Python quiere punto decimal y no coma.
    try:
        valor = float(valor_crudo)
    except ValueError:
        return {"error": f"La fuente mandó un valor de TRM que no es un número: "
                         f"{valor_crudo!r}."}

    # Una TRM de cero o negativa no existe. Mismo razonamiento que `tasa <= 0`.
    if valor <= 0:
        return {"error": f"La fuente reportó una TRM imposible: {valor}."}

    # Dict pequeño, y las dos fechas van adentro porque son LA información que
    # el modelo necesita para el caso del domingo.
    #
    # ⚠️ Las fechas van recortadas a 10 caracteres, igual que en historial() y
    #    en trm_en_fecha(). La fuente manda "2026-07-30T00:00:00.000": los 14
    #    caracteres del final son relleno, siempre iguales y nunca útiles —
    #    esta fuente no publica horas. Son 28 caracteres por llamada que el
    #    modelo RELEE en cada vuelta.
    #    Esto quedó dos sesiones sin arreglar a propósito: es una línea, pero
    #    es cambio de comportamiento, y eso se decide, no se hace de paso.
    #    Ninguno de los casos de evals.py mira estas fechas (todos comparan el
    #    valor), así que el cambio no rompe nada. Comprobado corriéndolo.
    desde = fila.get("vigenciadesde", "")
    hasta = fila.get("vigenciahasta", "")
    return {
        "trm": valor,
        "unidad": "COP por 1 USD",
        # ⭐ EL PUENTE QUE FALTABA (paso 8). La primera corrida del agente
        #    mostró que el modelo, para pasar pesos a dólares, calculaba
        #    1/3206.18 EN SU CABEZA y le pasaba el resultado a convertir().
        #    Acertó por diez cifras decimales. El día que se desvíe en la
        #    cuarta, convertir() recibe una tasa perfectamente válida y ni los
        #    116 casos se enteran: es el número creíble otra vez.
        #    El modelo no dividía por vicio: dividía porque trm() daba la tasa
        #    en un sentido, convertir() solo multiplica, y NADIE había
        #    construido el puente entre las dos. Así que lo construía él.
        #    Aquí está el puente, y es una división que sí se puede probar.
        #    Prohibirle calcular sin darle este número habría sido un callejón.
        "usd_por_1_cop": round(1 / valor, 10),
        # ⚠️ DEUDA ANOTADA: trm_en_fecha() tiene el mismo hueco y NO lleva esta
        #    llave. Se dejó a propósito: trm() es la que se usa para convertir
        #    ahora mismo, y cada llave se repaga en cada vuelta. Si algún día
        #    hay que convertir montos de una fecha pasada, se agrega allá.
        "vigente_desde": desde[:10] if es_texto(desde) else "no informado",
        "vigente_hasta": hasta[:10] if es_texto(hasta) else "no informado",
        "fuente": "TRM oficial (datos.gov.co)",
    }


def historial(dias):
    """Cómo se ha movido la TRM oficial: un RESUMEN de los últimos registros.

    Devuelve un resumen (máximo, mínimo, promedio, primero, último), NO la
    lista día por día. Se decidió midiendo, con los 30 días reales del
    2026-07-30: el crudo pesa 3.808 caracteres, las filas recortadas 811 y el
    resumen 238. Y lo que devuelve una herramienta se reenvía en CADA vuelta
    que le quede a la conversación, así que 238 contra 811 no se paga una vez.
    La cuenta que decidió: el resumen gana mientras el agente necesite un día
    puntual menos del 57% de las veces.
    → Para un día puntual está (estará) `trm_en_fecha(fecha)`. Una cosa cada
      una: misma regla por la que `trm()` no recibe `dias`.

    ⚠️⚠️ EL NOMBRE `dias` NO ES EXACTO, Y HAY QUE SABERLO.
    La fuente no guarda un registro por día: guarda uno por VIGENCIA. La TRM
    del viernes vale también sábado y domingo, así que un fin de semana entero
    es UNA sola fila. Medido: pedir 30 filas el 2026-07-30 devolvió desde el
    2026-06-12, o sea 48 días de calendario, no 30.
    Por eso este dict devuelve `desde`, `hasta` y `registros`: la función NUNCA
    afirma "los últimos 30 días". Si el modelo dijera eso, estaría mintiendo con
    total confianza — el mismo defecto del "solo letras y números" que prometía
    lo que no cumplía.
    → Deuda anotada: recortar de verdad a N días de calendario se puede, pero
      pide aritmética de fechas. Se dejó para después, a conciencia.
    """
    # -----------------------------------------------------------------------
    # 1. Frenos sobre `dias` — lo escoge el MODELO, así que es dato de afuera
    # -----------------------------------------------------------------------
    # Van ANTES de pedir el dato, por la misma razón que en tasa(): si validas
    # después, ya gastaste la llamada de red. Son TRES preguntas distintas y por
    # eso son tres `if`: cada mensaje tiene que nombrar al culpable, o el modelo
    # reintenta a ciegas.
    if not es_numero(dias):
        return {"error": f"`dias` debe ser un número entero, no "
                         f"{type(dias).__name__}. Ejemplo: 30 (sin comillas)."}

    # ¿Es ENTERO? No se pueden pedir 3.5 registros. Un 30.0 SÍ se acepta: es un
    # 30 escrito con decimales, y rechazarlo sería castigar al modelo por una
    # coma. `.is_integer()` responde eso; `int(3.5)` daría 3 en silencio, que es
    # peor: haría algo distinto de lo que pidieron sin decírselo a nadie.
    if isinstance(dias, float) and not dias.is_integer():
        return {"error": f"`dias` no puede llevar decimales. Llegó {dias}. "
                         f"Ejemplo: 30."}
    dias = int(dias)   # a partir de aquí `dias` es un int seguro

    if dias < 1:
        return {"error": f"`dias` debe ser 1 o más. Llegó {dias}."}

    if dias > MAX_REGISTROS:
        return {"error": f"`dias` no puede pasar de {MAX_REGISTROS} "
                         f"(son más de año y medio). Llegó {dias}."}

    # -----------------------------------------------------------------------
    # 2. Pedir el dato
    # -----------------------------------------------------------------------
    # La URL termina en "$limit=" y una URL es TEXTO: str(dias), no dias.
    # Sin el str() esto sería  TypeError: can only concatenate str to str.
    datos, error = pedir_json(URL_TRM + str(dias))
    if error:
        # Igual que en trm(): el error de red ya viene redactado para el modelo.
        return {"error": error}

    # -----------------------------------------------------------------------
    # 3. Frenos sobre la respuesta — esta fuente devuelve una LISTA
    # -----------------------------------------------------------------------
    if not isinstance(datos, list) or not datos:
        return {"error": "La fuente oficial no devolvió ninguna fila de TRM."}

    # -----------------------------------------------------------------------
    # 4. Recorrer las filas — lo NUEVO de esta función: son muchas, no una
    # -----------------------------------------------------------------------
    # ⚠️ DECISIÓN (mía, revocable): una fila podrida NO tumba la respuesta.
    # Se salta y se cuenta. Razón: 29 días buenos siguen contestando "¿cómo va
    # el dólar?", y tirar los 29 por 1 es peor negocio. Pero el descarte NO se
    # esconde: se devuelve `descartados`, y decidir si 29 de 30 le sirven ES
    # CRITERIO — o sea del modelo, igual que el domingo en trm().
    # Callarlo sería lo mismo que el `except Exception` que no pusimos en
    # pedir_json: un problema real disfrazado de respuesta normal.
    serie = []          # pares (fecha, valor) que sí se pudieron leer
    descartados = 0

    for fila in datos:
        # Los frenos de trm(), uno por uno, pero aquí en vez de `return` va
        # `continue`: esta fila se cae, las demás siguen.
        if not isinstance(fila, dict):
            descartados += 1
            continue

        # La fecha: "2026-07-30T00:00:00.000" son 24 caracteres y los 14 del
        # final son siempre lo mismo. Los primeros 10 son la fecha entera.
        fecha = fila.get("vigenciadesde")
        if not es_texto(fecha) or len(fecha) < 10:
            descartados += 1
            continue

        # El valor: los mismos DOS frenos de trm(), porque son dos preguntas.
        # FORMA (¿es la clase de cosa correcta?) y CONTENIDO (¿es un número
        # escrito?). Ojo que float("3.206,18") revienta: así se escribe la
        # plata en Colombia y esta fuente podría cambiar a ese formato.
        crudo = fila.get("valor")
        if not es_texto(crudo) and not es_numero(crudo):
            descartados += 1
            continue
        try:
            valor = float(crudo)
        except ValueError:
            descartados += 1
            continue
        if valor <= 0:
            descartados += 1
            continue

        serie.append((fecha[:10], valor))

    # Si no sobrevivió ninguna, no hay resumen que sacar. Aquí sí es error:
    # un promedio de cero números no existe (sum([])/len([]) es ZeroDivisionError).
    if not serie:
        return {"error": f"Ninguna de las {len(datos)} filas de TRM se pudo "
                         f"leer: la fuente cambió de formato."}

    # -----------------------------------------------------------------------
    # 5. El resumen
    # -----------------------------------------------------------------------
    # Se ordena AQUÍ en vez de confiar en el $order de la URL: así el resumen
    # sale bien aunque el servidor un día devuelva las filas al revés.
    # Y ordenar es gratis porque la fecha es "AAAA-MM-DD": el formato ISO se
    # ordena solo como texto, sin convertirla a fecha de verdad. Por eso se
    # recortó a 10 caracteres arriba y no a 4 ni a 7.
    serie.sort()
    fecha_vieja, valor_viejo = serie[0]     # el más antiguo
    fecha_nueva, valor_nuevo = serie[-1]    # el más reciente

    valores = [v for _, v in serie]

    # -----------------------------------------------------------------------
    # 6. El dict pequeño
    # -----------------------------------------------------------------------
    # Los redondeos son de PRESENTACIÓN: promedio y porcentaje se calculan
    # completos y se recortan al final. Nunca se redondea un número que después
    # se vuelve a usar en una cuenta (la trampa que casi mata a tasa()).
    resumen = {
        "registros": len(serie),
        "desde": fecha_vieja,
        "hasta": fecha_nueva,
        "primero": valor_viejo,
        "ultimo": valor_nuevo,
        "maximo": max(valores),
        "minimo": min(valores),
        "promedio": round(sum(valores) / len(valores), 2),
        "cambio_pct": round((valor_nuevo - valor_viejo) / valor_viejo * 100, 2),
        "unidad": "COP por 1 USD",
        "fuente": "TRM oficial (datos.gov.co)",
    }

    # La llave solo aparece si hubo algo que contar. Un "descartados": 0 fijo
    # sería ruido que se repaga en cada vuelta y que no informa nada.
    if descartados:
        resumen["descartados"] = descartados

    return resumen


def explicar_sin_trm(fecha):
    """AYUDANTE INTERNO (no es herramienta: el modelo nunca la llama).

    Dice POR QUÉ una fecha bien escrita no trajo ninguna TRM. Devuelve DOS
    cosas: (motivo, texto). Quien las envuelve en un dict es trm_en_fecha().

    ⚠️ El `motivo` ("futura", "muy_antigua", "hueco", "desconocido") lo pidió
    el EVAL, y por una regla que él mismo puso en el paso 5: las pruebas no
    comparan el texto de un error, porque el día que mejores la redacción se
    romperían sin que nada esté mal. Pero los tres motivos SÍ hay que
    distinguirlos. La salida es que el motivo sea un DATO estable al lado de la
    frase, que puede cambiar cuando se quiera.
    → Escribir la prueba mejoró el diseño: el modelo también gana, porque ahora
      puede ramificar por un valor fijo y no por cómo esté redactada una frase.

    Existe porque "no hay dato" tapa tres situaciones distintas y el modelo
    necesita distinguirlas para explicarle algo al usuario. Es la misma idea de
    pedir_json, que pone el número del HTTP en el mensaje: un 404 y un 503 no
    piden lo mismo.

    ⚠️ Y aquí está el truco que evita el reloj: para saber si una fecha es
    "futura" NO se mira la hora de la máquina — eso volvería la función
    imposible de probar con datos fijos. Se le pregunta A LA FUENTE cuál es su
    rango. La fuente es su propio calendario.
    """
    datos, error = pedir_json(URL_TRM_RANGO)

    # Si la segunda consulta también falla, NO se inventa el motivo. Se dice
    # que no se pudo averiguar. Un motivo inventado es peor que ninguno.
    if error or not isinstance(datos, list) or not datos or not isinstance(datos[0], dict):
        return ("desconocido",
                f"No hay TRM para {fecha}, y no pude averiguar por qué: la "
                f"fuente no respondió qué rango de fechas cubre.")

    primera = datos[0].get("primera")
    ultima = datos[0].get("ultima")
    if not es_texto(primera) or not es_texto(ultima) or len(primera) < 10 or len(ultima) < 10:
        return ("desconocido",
                f"No hay TRM para {fecha}, y la fuente no informó bien el "
                f"rango de fechas que cubre.")
    primera, ultima = primera[:10], ultima[:10]

    # Comparar fechas como TEXTO funciona porque son "AAAA-MM-DD": el formato
    # ISO se ordena solo. Es el mismo regalo que usa el serie.sort() de
    # historial(), y la razón por la que se recorta a 10 y no a 7.
    if fecha > ultima:
        return ("futura",
                f"Todavía no hay TRM para {fecha}: el dato más reciente que "
                f"publica la fuente es del {ultima}.")
    if fecha < primera:
        return ("muy_antigua",
                f"No hay TRM para {fecha}: la serie oficial empieza el {primera}.")

    # Está dentro del rango y aun así no hay fila. No es culpa de quien preguntó.
    return ("hueco",
            f"No encontré TRM para {fecha}, aunque está dentro del rango que "
            f"publica la fuente ({primera} a {ultima}). Puede ser un hueco en "
            f"los datos oficiales.")


def trm_en_fecha(fecha):
    """La TRM oficial que estaba VIGENTE en una fecha del pasado.

    Existe porque historial() devuelve un resumen: sin esta herramienta, si el
    usuario pregunta "¿cuánto valió el 15 de julio?" el modelo tiene el máximo,
    el mínimo y el promedio en la mano y NINGUNA forma de conseguir el dato
    real — o se rinde, o se inventa un número creíble. Esto le da a dónde ir.

    ⚠️ NO SIRVE PARA "HOY". El modelo no tiene reloj: si le pides que calcule
    "hoy" o "ayer", va a partir de una fecha que se imaginó y va a entregar un
    número real de un día equivocado. Para hoy está trm(), que no necesita
    saber la fecha porque la fuente le da la más reciente. Frontera que hay que
    dejar clarísima en la descripción del paso 7.

    ⚠️⚠️ ESTA ES LA PRIMERA URL DEL PROYECTO QUE SE ARMA CON TEXTO DE AFUERA.
    Todas las demás son constantes. Aquí el dato del modelo entra a la consulta,
    y la consulta lo pone entre comillas simples:

        $where=vigenciadesde <= 'LA_FECHA' AND ...

    Si LA_FECHA trae una comilla simple, cierra la comilla que abría el dato y
    lo que siga deja de ser un dato: se vuelve parte de la PREGUNTA. Eso se
    llama INYECCIÓN. Probado contra la fuente real el 2026-07-30 con
    `2026-07-30' OR '1'='1` -> devolvió 1000 filas en vez de 1.
    Y el daño es doble: respuesta equivocada Y un tool_result de ~125.000
    caracteres (~31.000 tokens) que se repagaría en cada vuelta siguiente.
    → La defensa es la LISTA DE PERMITIDOS de guardar_reporte, no una lista de
      prohibidos: no se pregunta "¿tiene comillas?" (siempre falta algo), se
      exige la forma exacta AAAA-MM-DD y lo demás no entra.
    """
    # -----------------------------------------------------------------------
    # 1. El freno sobre `fecha` — EL MÁS IMPORTANTE DE LA FUNCIÓN
    # -----------------------------------------------------------------------
    # Dos preguntas, dos frenos, porque son distintas.
    # FORMA: sin esto, strptime() sobre una lista no devuelve False, LANZA.
    if not es_texto(fecha):
        return {"error": f"La fecha debe ser texto con la forma AAAA-MM-DD, no "
                         f"{type(fecha).__name__}. Ejemplo: \"2026-07-15\" "
                         f"(entre comillas)."}

    # CONTENIDO: strptime intenta CONSTRUIR la fecha con ese molde. Si no
    # encaja, lanza ValueError. Contesta dos cosas de un golpe:
    #   - la forma:      "15/07/2026" y "15 de julio" no encajan
    #   - la existencia: "2026-02-30" tiene forma perfecta y NO EXISTE.
    # Un freno hecho a mano con len() e isdigit() dejaría pasar el 30 de
    # febrero: mediría la forma sin preguntar si el día existe.
    # ⚠️ Y ESTE ES EL FRENO QUE CORTA LA INYECCIÓN: `2026-07-30' OR '1'='1`
    #    no tiene la forma AAAA-MM-DD, así que muere aquí y NUNCA llega a la
    #    URL. Es una lista de permitidos (se exige la forma exacta), no una de
    #    prohibidos (buscar comillas): lo que no se me ocurrió también queda
    #    afuera. Mismo criterio que PERMITIDOS en guardar_reporte.
    try:
        dia = datetime.datetime.strptime(fecha, FORMATO_FECHA)
    except ValueError:
        return {"error": f"No entiendo la fecha {fecha!r}. Debe ir como "
                         f"AAAA-MM-DD y ser un día que exista. "
                         f"Ejemplo: \"2026-07-15\"."}

    # ⚠️ NORMALIZAR, y esto salió de la PRIMERA CORRIDA como un defecto real:
    # strptime NO exige el cero a la izquierda. "2026-7-5" le encaja igual que
    # "2026-07-05". Sin esta línea se validaba una cosa y se mandaba otra:
    # a la URL iba el texto original, sin rellenar.
    # Y eso rompe la comparación de explicar_sin_trm, que compara fechas como
    # TEXTO: "2026-7-5" > "2026-07-30" es True, porque en el 6º carácter "7"
    # es mayor que "0". El agente diría "todavía no hay TRM para esa fecha"
    # de un día que ya pasó — seguro de sí mismo y equivocado.
    # → REGLA: después de validar, usa lo VALIDADO, no lo que llegó.
    #   strftime vuelve a escribir la fecha en su forma canónica.
    fecha = dia.strftime(FORMATO_FECHA)

    # -----------------------------------------------------------------------
    # 2. Armar la consulta y pedirla
    # -----------------------------------------------------------------------
    # Se pregunta por RANGO y no por igualdad, y esa es la clave del domingo:
    # el domingo no tiene fila propia, lo cubre la del viernes. Preguntando
    # "¿qué fila contiene este día?" la fuente lo resuelve sola y nosotros no
    # hacemos ni una cuenta de calendario.
    momento = f"{fecha}T00:00:00.000"
    condicion = (f"vigenciadesde <= '{momento}'"
                 f" AND vigenciahasta >= '{momento}'")

    # quote() codifica espacios, comillas y símbolos que no pueden ir crudos en
    # una URL (es el problema del %20 otra vez, ahora resuelto bien).
    # ⚠️ El quote() NO reemplaza al freno de arriba: son dos trabajos distintos.
    #    El freno decide QUÉ entra; quote() solo lo transporta sin romperse.
    #    Confiar solo en quote() sería confiar en el transporte para decidir
    #    quién puede viajar.
    url = URL_TRM_BASE + "?$where=" + urllib.parse.quote(condicion)

    datos, error = pedir_json(url)
    if error:
        return {"error": error}

    # -----------------------------------------------------------------------
    # 3. Freno sobre la forma de la respuesta
    # -----------------------------------------------------------------------
    # Ojo: aquí NO se junta "no es lista" con "está vacía" como en trm(). Una
    # lista vacía es una respuesta legítima —esa fecha no tiene TRM— y merece
    # una explicación, no un "la fuente falló".
    if not isinstance(datos, list):
        return {"error": "La fuente oficial no devolvió una lista de filas."}

    # -----------------------------------------------------------------------
    # 4. Cero filas: se explica el PORQUÉ (decisión suya, sesión 13)
    # -----------------------------------------------------------------------
    if not datos:
        motivo, texto = explicar_sin_trm(fecha)
        # `motivo` es un dato estable ("futura", "muy_antigua", "hueco",
        # "desconocido"); `error` es la frase, que se puede reescribir cuando
        # se quiera sin romper una sola prueba.
        return {"error": texto, "motivo": motivo}

    # -----------------------------------------------------------------------
    # 5. Leer la fila — los mismos frenos de trm(), sin novedad
    # -----------------------------------------------------------------------
    fila = datos[0]
    if not isinstance(fila, dict):
        return {"error": "La fila de TRM no tiene el formato esperado."}

    valor_crudo = fila.get("valor")
    if not es_texto(valor_crudo) and not es_numero(valor_crudo):
        return {"error": f"La fuente mandó un valor de TRM que no se puede "
                         f"leer ({type(valor_crudo).__name__})."}
    try:
        valor = float(valor_crudo)
    except ValueError:
        return {"error": f"La fuente mandó un valor de TRM que no es un "
                         f"número: {valor_crudo!r}."}
    if valor <= 0:
        return {"error": f"La fuente reportó una TRM imposible: {valor}."}

    # -----------------------------------------------------------------------
    # 6. El dict pequeño
    # -----------------------------------------------------------------------
    # `fecha_pedida` va aparte de `vigente_desde` A PROPÓSITO: si preguntaron
    # por el domingo 26 y la respuesta es la del viernes 24, el modelo tiene
    # que PODER decirlo. Con un solo campo, esa diferencia se pierde y el
    # agente diría "el 26 la TRM fue X" como si ese día se hubiera publicado.
    # Las fechas van recortadas a 10: el T00:00:00.000 son 14 caracteres de
    # relleno por fecha, y esto se repaga en cada vuelta.
    desde = fila.get("vigenciadesde", "")
    hasta = fila.get("vigenciahasta", "")
    return {
        "fecha_pedida": fecha,
        "trm": valor,
        "unidad": "COP por 1 USD",
        "vigente_desde": desde[:10] if es_texto(desde) else "no informado",
        "vigente_hasta": hasta[:10] if es_texto(hasta) else "no informado",
        "fuente": "TRM oficial (datos.gov.co)",
    }
