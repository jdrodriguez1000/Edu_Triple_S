"""
evals.py — Las pruebas de las herramientas que NO tocan la red (nivel 5b).

Corre en un segundo, no usa internet y cuesta $0.00. Por eso se escribe ANTES
de arreglar nada: primero se ve fallar, después se arregla, y el cambio de
FALLA a ok es la prueba de que el arreglo sirvió.

Cada caso es un DATO de tres partes: (etiqueta, argumentos, esperado).
  - `esperado` es un número  -> se compara contra r["resultado"]
  - `esperado` es "error"    -> solo importa QUE haya rechazo, no su redacción.
    (Si comparas el texto exacto del error, el día que mejores el mensaje la
    prueba se rompe sin que nada esté mal. Se prueba el comportamiento.)
    ✅ Esa decisión YA SE PAGÓ: en la sesión 12 se reescribió la redacción de 4
    mensajes de error y no se rompió ni un caso. Una prueba bien diseñada te
    deja mejorar el código; una mal diseñada te lo congela.

⚠️ AQUÍ TAMBIÉN SE PRUEBA tasa(), que SÍ toca internet — pero solo sus casos de
RECHAZO. Se puede porque los frenos de moneda van ANTES de pedir el dato: esos
casos mueren sin salir de la máquina. El camino feliz de tasa() NO cabe en este
archivo (depende de un servidor ajeno) y se prueba en los pasos 9 y 10.
Y no lo suponemos: más abajo hay una TRAMPA que revienta si algún caso llega a
la red. El eval sigue siendo $0.00 y sin internet, y ahora está DEMOSTRADO.
"""

import herramientas
from herramientas import (CAJA, MAX_REGISTROS, convertir, guardar_reporte,
                          historial, tasa, trm, trm_en_fecha)

# ---------------------------------------------------------------------------
# La trampa: prueba que este eval NO toca la red
# ---------------------------------------------------------------------------
# Le cambiamos a herramientas el pedir_json de verdad por uno que solo sabe
# reventar. Si algún caso de aquí llega a la red, salta como REVENTO y el eval
# falla en voz alta. Es la técnica del sabotaje (nivel 3, y la del write_text
# comentado) usada al revés: en vez de romper el código para ver si la prueba
# lo nota, se rompe el CAMINO PROHIBIDO para ver si alguien lo pisa.


def trampa_de_red(*args, **kwargs):
    raise AssertionError("un caso llego a la red: este eval debe costar $0.00")


herramientas.pedir_json = trampa_de_red

# ---------------------------------------------------------------------------
# Casos de convertir()
# ---------------------------------------------------------------------------
# Regla: UN caso, UNA variable. Todo normal salvo lo que se está probando.
# Un caso con dos defectos puede pasar por la razón equivocada.

CASOS_CONVERTIR = [
    # (etiqueta,             argumentos,                      esperado)

    # --- camino feliz ---
    ("camino feliz",         (10, "USD", "COP", 3900),        39000),

    # --- el monto: se decidió que un monto negativo siempre es un accidente ---
    ("monto negativo",       (-100, "USD", "COP", 3900),      "error"),
    # El cero SÍ se acepta: raro, pero no es un error. Este caso existe para
    # que la decisión quede escrita y no se cambie por descuido.
    ("monto cero",           (0, "USD", "COP", 3900),         0),

    # --- la tasa: 0 y negativa no existen en el mundo real.
    #     La tasa 0 es la más traicionera: devuelve 0, y un 0 se ve legítimo.
    ("tasa cero",            (10, "USD", "COP", 0),           "error"),
    ("tasa negativa",        (10, "USD", "COP", -3900),       "error"),

    # --- datos que no son números: hoy REVIENTAN, y eso rompe el contrato
    #     del archivo ("ninguna lanza excepciones"). Un {"error"} es una
    #     conversación; un TypeError es un funeral: se cae el bucle del agente.
    ("tasa None",            (10, "USD", "COP", None),        "error"),
    ("monto vacio",          ("", "USD", "COP", 3900),        "error"),
    ("monto texto",          ("10", "USD", "COP", 3900),      "error"),   # ⚠️ ver abajo
    ("monto None",           (None, "USD", "COP", 3900),      "error"),

    # --- los booleanos: en Python True vale 1 y cuenta como entero, así que
    #     isinstance(True, int) es True y se colaban por el freno de tipos.
    #     "Raro" no es "imposible", y los bordes son donde nadie mira.
    ("monto booleano",       (True, "USD", "COP", 3900),      "error"),
    ("tasa booleana",        (10, "USD", "COP", True),        "error"),

    # --- las monedas: son texto, no cantidades. Estos tres los cubren los
    #     dos `if` que ya existen, así que hoy los tres pasan.
    ("moneda vacia",         (10, "", "COP", 3900),           "error"),
    ("moneda minuscula",     (10, "usd", "COP", 3900),        "error"),   # ⚠️ ver abajo
    ("moneda inexistente",   (10, "YEN", "COP", 3900),        "error"),

    # --- monedas que NO SON TEXTO. Estos cuatro los agregó la sesión 12, y los
    #     dos primeros REVENTABAN: `x in un_diccionario` funciona con cualquier
    #     valor hashable (números, None, booleanos), así que la prueba de
    #     pertenencia hacía de paso un control de tipo... pero una lista no es
    #     hashable, y ahí Python no dice "no está": dice TypeError.
    #     Funcionaba por casualidad y la casualidad tenía un borde.
    #     ⚠️ Los 26 casos anteriores estaban TODOS en verde con esto roto.
    ("moneda lista",         (10, [], "COP", 3900),           "error"),
    ("moneda dict",          (10, "USD", {}, 3900),           "error"),
    ("moneda numero",        (10, 123, "COP", 3900),          "error"),
    ("moneda None",          (10, None, "COP", 3900),         "error"),

    # --- el redondeo: COP no lleva centavos, USD sí.
    #     tasa=1 a propósito, para que la multiplicación no estorbe y el caso
    #     mida SOLO el redondeo. Hoy "a COP" da 4.0 en vez de 4.
    ("redondeo a COP",       (3.7, "USD", "COP", 1),          4),
    ("redondeo a USD",       (3.7777, "COP", "USD", 1),       3.78),
]

# ✅ LAS DOS DECISIONES, YA TOMADAS: las dos se RECHAZAN.
#
#   - "monto texto": "10" no se convierte a número. Si el modelo manda texto
#     donde va un número, es un error suyo y tiene que corregirlo.
#   - "moneda minuscula": "usd" no se pasa a mayúsculas. Se exige el formato.
#
# Lo que cuesta la segunda, y hay que medirlo en el paso 9: cada minúscula gasta
# una vuelta extra del bucle (manda "usd", lee el error, reintenta con "USD"),
# o sea dos llamadas a la API en vez de una. Con .upper() habría sido gratis.
# Si en registro.jsonl aparece mucho, la decisión se revisa CON DATOS.
# Por eso el mensaje de error debe listar las monedas en mayúscula: es lo único
# que le dice al modelo que el problema era el formato y no la moneda.


# ---------------------------------------------------------------------------
# Casos de guardar_reporte()
# ---------------------------------------------------------------------------
# Esta función es distinta: convertir() solo DEVUELVE algo, y guardar_reporte()
# CAMBIA EL MUNDO (escribe un archivo). Lo que devuelve es apenas un recibo;
# la verdad está en el disco. Si alguien comenta la línea del write_text, la
# función devuelve exactamente lo mismo de siempre y no guarda nada.
#
# Por eso aquí `esperado` es "guardado" o "error", y el bucle además revisa:
#   - si esperaba guardar: que el archivo EXISTA y que su contenido COINCIDA
#   - si esperaba error:   que caja/ haya quedado INTACTA

CASOS_GUARDAR = [
    # (etiqueta,             argumentos,                        esperado)

    # --- camino feliz ---
    ("camino feliz",         ("reporte.txt", "TRM: 3900"),      "guardado"),
    ("nombre con guiones",   ("trm-2026-07-30.txt", "3900"),    "guardado"),

    # --- borde: contenido vacío. Se ACEPTA (decisión, igual que monto cero):
    #     un reporte sin datos es raro, pero no es un error de formato.
    ("contenido vacio",      ("vacio.txt", ""),                 "guardado"),

    # --- freno 1: la extensión ---
    ("sin .txt",             ("reporte.md", "x"),               "error"),
    ("sin extension",        ("reporte", "x"),                  "error"),

    # --- freno 2: la allowlist de caracteres ---
    ("con espacio",          ("mi reporte.txt", "x"),           "error"),
    ("ruta absoluta",        ("C:/Windows/x.txt", "x"),         "error"),
    ("sube de carpeta",      ("../../.env", "x"),               "error"),
    ("subcarpeta",           ("sub/reporte.txt", "x"),          "error"),

    # --- freno 3: el punto punto (hoy redundante, ver herramientas.py) ---
    ("punto punto",          ("..txt", "x"),                    "error"),

    # --- freno 0: la FORMA. Los tres los agregó la sesión 12 y los tres
    #     REVENTABAN. Los frenos 1 y 2 usan métodos de texto, y un método de
    #     texto sobre algo que no es texto no devuelve False: LANZA.
    #     [].endswith(".txt") -> AttributeError. write_text(None) -> TypeError.
    #     Por eso el freno 0 va antes de todos: primero la forma, después el
    #     contenido. Mismo orden que ya tenía convertir().
    ("nombre lista",         ([], "x"),                         "error"),
    ("nombre numero",        (5, "x"),                          "error"),
    ("contenido None",       ("reporte.txt", None),             "error"),
]


# ---------------------------------------------------------------------------
# Casos de tasa()
# ---------------------------------------------------------------------------
# Esta es la tercera función, y la primera que depende de un servidor ajeno.
# Solo caben aquí sus casos de RECHAZO: los frenos de moneda van antes de pedir
# el dato, así que estos mueren sin salir de la máquina ($0.00, sin internet).
# El camino feliz NO cabe: no se puede exigir un número fijo a una tasa que
# cambia todos los días, ni depender de que el servidor esté vivo hoy.
# Aquí se pueden agregar más rechazos; ninguno feliz.

CASOS_TASA = [
    # (etiqueta,             argumentos,      esperado)
    ("moneda lista",         ([], "COP"),     "error"),
    ("moneda None",          (None, "COP"),   "error"),
]


# ---------------------------------------------------------------------------
# Casos de tasa() CON UN SERVIDOR DE MENTIRA
# ---------------------------------------------------------------------------
# Aquí se le cambia a tasa() su pedir_json por uno que devuelve lo que nosotros
# digamos. Es la misma maña de la trampa de red, usada para construir en vez de
# para prohibir: si podemos reemplazar pedir_json por uno que revienta, podemos
# reemplazarlo por uno que finge ser un servidor con problemas.
# Eso se llama un DOBLE: un actor que hace de servidor.
#
# Resuelve el problema que tenía anotado el paso 6 ("estas tres no se pueden
# probar como las otras dos, dependen de un servidor ajeno"). Sí se pueden:
# si les cambias el servidor. Y sirve para las DOS mitades:
#
#   1. Los caminos MALOS. Los tres frenos de tasa() sobre la respuesta del
#      servidor nunca se habían ejecutado, porque para eso la fuente tendría
#      que mandar null o caerse, y hoy vino perfecta las 8 veces. Escritos y
#      sin correr: podrían tener un typo y no lo sabríamos.
#   2. El camino FELIZ, y esto es lo que no habíamos visto: con datos de
#      mentira SÍ se puede probar la aritmética, porque los números los
#      ponemos nosotros. Son DOS preguntas distintas que veníamos mezclando:
#        - "¿mi cuenta está bien?"        -> datos de mentira, $0.00, determinista
#        - "¿el servidor sigue vivo?"     -> eso sí necesita red (pasos 9 y 10)
#      Lo que no cabe aquí es la segunda. La primera cabe perfecto.
#
# Cada caso trae la RESPUESTA FALSA que va a devolver pedir_json, en la misma
# forma que devuelve el de verdad: la tupla (datos, error).

CASOS_TASA_FUENTE = [
    # (etiqueta,            (datos_falsos, error_falso),                                  argumentos,      esperado)

    # --- la fuente contestó, pero contestó cualquier cosa ---
    ("sin llave rates",     ({}, None),                                                   ("USD", "COP"),  "error"),
    ("moneda ausente",      ({"rates": {"USD": 1}}, None),                                ("USD", "COP"),  "error"),
    ("valor null",          ({"rates": {"USD": 1, "COP": None}}, None),                   ("USD", "COP"),  "error"),
    # ⚠️ Este es el formato REAL de la otra fuente: datos.gov.co manda el valor
    #    como texto ("3206.18", con comillas). Si un día el mercado hace lo
    #    mismo, este freno es el que avisa.
    ("valor texto",         ({"rates": {"USD": 1, "COP": "3206.18"}}, None),              ("USD", "COP"),  "error"),

    # --- el divisor: sin este freno sería ZeroDivisionError, o sea un funeral ---
    ("divisor cero",        ({"rates": {"USD": 0, "COP": 4000}}, None),                   ("USD", "COP"),  "error"),
    ("divisor negativo",    ({"rates": {"USD": -1, "COP": 4000}}, None),                  ("USD", "COP"),  "error"),
    # ⚠️ Estos dos son NUEVOS de la sesión 17, y existen por el puente:
    #    la llave inversa divide entre la moneda de DESTINO. Antes del puente
    #    un 0 ahí solo daba una tasa de 0; ahora reventaría.
    #    → Un dato nuevo trae su propia forma de fallar, y su propio caso.
    ("destino cero",        ({"rates": {"USD": 1, "COP": 0}}, None),                      ("USD", "COP"),  "error"),
    ("destino negativo",    ({"rates": {"USD": 1, "COP": -4000}}, None),                  ("USD", "COP"),  "error"),

    # --- la red falló: el error de pedir_json se reenvía tal cual ---
    ("error de red",        (None, "No pude conectarme a la fuente (URLError)."),          ("USD", "COP"),  "error"),

    # --- camino feliz DETERMINISTA: las tasas las ponemos nosotros ---
    #     Ojo: el esperado es 4000.0 y no 4000. En Python 3 la división `/`
    #     siempre devuelve float, incluso 4000/1. Y el eval compara el TIPO.
    ("feliz USD->COP",      ({"rates": {"USD": 1, "COP": 4000},
                              "time_last_update_utc": "hoy"}, None),                      ("USD", "COP"),  4000.0),
    # La triangulación con números escogidos para que la cuenta se vea a ojo:
    # 1 EUR son 2 USD, y 1 USD son 4000 COP -> 1 EUR son 8000 COP.
    ("feliz EUR->COP",      ({"rates": {"USD": 1, "EUR": 0.5, "COP": 4000},
                              "time_last_update_utc": "hoy"}, None),                      ("EUR", "COP"),  8000.0),
    # Sin la llave de la fecha: comprueba que el .get() con respaldo no revienta.
    ("sin fecha",           ({"rates": {"USD": 1, "COP": 4000}}, None),                   ("USD", "COP"),  4000.0),
]


# ---------------------------------------------------------------------------
# Casos de trm() — todos con servidor de mentira
# ---------------------------------------------------------------------------
# trm() no tiene NINGÚN caso sin doble: no recibe argumentos, así que no hay
# nada que rechazar antes de salir a la red. Todo lo que se le puede probar
# aquí pasa por controlar lo que "contesta" la fuente.
#
# Y la fuente oficial devuelve una LISTA de filas, no un diccionario como la de
# mercado. Dos fuentes, dos formas: cada herramienta tiene que conocer la suya.

TRM_OK = [{"valor": "3206.18", "unidad": "COP",
           "vigenciadesde": "2026-07-30T00:00:00.000",
           "vigenciahasta": "2026-07-30T00:00:00.000"}]

CASOS_TRM = [
    # (etiqueta,            (datos_falsos, error_falso),                      esperado)

    # --- camino feliz: el valor llega como TEXTO y debe salir como número ---
    ("feliz",               (TRM_OK, None),                                   3206.18),

    # --- ⚠️ EL DOMINGO. No hay que inventarlo: está en los datos. La TRM del
    #     viernes 24 siguió vigente hasta el domingo 26. La herramienta lo
    #     ACEPTA y devuelve las fechas; decidir qué hacer es del MODELO.
    ("domingo (viernes vigente hasta domingo)",
                            ([{"valor": "3200.00", "unidad": "COP",
                               "vigenciadesde": "2026-07-24T00:00:00.000",
                               "vigenciahasta": "2026-07-26T00:00:00.000"}], None),
                                                                              3200.00),

    # --- la lista: distinto de tasa(), aquí lo que llega es una lista ---
    ("lista vacia",         ([], None),                                       "error"),
    ("no es lista",         ({"valor": "3206.18"}, None),                     "error"),
    ("fila que no es dict", (["3206.18"], None),                              "error"),

    # --- el valor: freno de FORMA ---
    ("valor ausente",       ([{"unidad": "COP"}], None),                      "error"),
    ("valor null",          ([{"valor": None}], None),                        "error"),
    ("valor lista",         ([{"valor": []}], None),                          "error"),
    ("valor booleano",      ([{"valor": True}], None),                        "error"),

    # --- el valor: freno de CONTENIDO. Es texto, pero ¿es un número escrito? ---
    ("valor texto no numerico", ([{"valor": "no hay dato"}], None),           "error"),
    ("valor vacio",         ([{"valor": ""}], None),                          "error"),
    # ⚠️ Formato colombiano: coma decimal y punto de miles. float() lo rechaza.
    #    Es el caso más realista de esta lista: así se escribe la plata acá.
    ("valor con coma decimal", ([{"valor": "3.206,18"}], None),               "error"),

    # --- valores imposibles ---
    ("valor cero",          ([{"valor": "0"}], None),                         "error"),
    ("valor negativo",      ([{"valor": "-3206.18"}], None),                  "error"),

    # --- la red falló ---
    ("error de red",        (None, "No pude conectarme a la fuente (URLError)."), "error"),

    # --- sin fechas: no revienta, el .get() tiene respaldo ---
    ("sin fechas",          ([{"valor": "3206.18"}], None),                   3206.18),
]


# ---------------------------------------------------------------------------
# Casos de historial() — RECHAZOS, sin salir a la red
# ---------------------------------------------------------------------------
# Estos son como los de tasa(): los frenos sobre `dias` van ANTES de pedir el
# dato, así que mueren en la máquina. Corren con LA TRAMPA puesta, así que
# hacen dos trabajos: comprueban el rechazo Y demuestran que el freno de
# verdad está antes de la red. Si alguien moviera un freno para después del
# pedir_json, aquí saltaría un AssertionError.

CASOS_HISTORIAL = [
    # (etiqueta,             argumentos,          esperado)

    # --- FORMA: el modelo manda JSON, donde "30" y 30 son cosas distintas ---
    ("dias texto",           ("30",),             "error"),
    ("dias None",            (None,),             "error"),
    ("dias lista",           ([],),               "error"),
    # True vale 1 en Python: sin es_numero() esto pediría 1 registro tan campante.
    ("dias booleano",        (True,),             "error"),

    # --- ¿ENTERO? 3.5 registros no existen. Ojo que 30.0 SÍ se acepta y ese
    #     caso está abajo, con el doble: es un 30 escrito con decimales.
    ("dias con decimales",   (3.5,),              "error"),

    # --- RANGO ---
    ("dias cero",            (0,),                "error"),
    ("dias negativo",        (-5,),               "error"),
    # ⚠️ 100000 no es basura: es un número perfectamente válido con el que el
    #    modelo le pediría 100.000 filas a un servidor del gobierno. El tope no
    #    protege nuestros tokens (el resumen pesa igual): protege a un tercero.
    ("dias sobre el tope",   (100000,),           "error"),
]


# ---------------------------------------------------------------------------
# Casos de historial() CON SERVIDOR DE MENTIRA
# ---------------------------------------------------------------------------
# Aquí sí cabe el camino feliz, y con la aritmética verificable a ojo: las
# fechas y los valores los ponemos nosotros. Es la misma separación de tasa():
#   "¿mi cuenta está bien?"    -> datos de mentira, $0.00, determinista
#   "¿el servidor sigue vivo?" -> eso necesita red (paso 9)
#
# ⚠️ NOVEDAD DE ESTA LISTA: `esperado` puede ser un DICCIONARIO con las llaves
# que importan, no un solo número. historial() devuelve muchas cosas y hay
# varias que vale la pena mirar a la vez (cuántos registros quedaron, si el
# promedio está bien, si se descartó alguna fila).
# Se comparan SOLO las llaves que se nombran, no el dict entero. Es la misma
# razón por la que no se compara el texto de los errores: el día que le
# agreguemos una llave nueva al resumen, no se tienen que romper 10 casos.


def fila_trm(fecha, valor):
    """Una fila de mentira con la forma REAL de datos.gov.co.

    La fecha llega con hora pegada ("2026-07-30T00:00:00.000") y el valor llega
    como TEXTO. Escribirlo así, y no bonito, es a propósito: si el doble se
    parece a lo que uno quisiera en vez de a lo que manda el servidor, las
    pruebas pasan y el agente se rompe en producción.
    """
    return {"valor": valor, "unidad": "COP",
            "vigenciadesde": f"{fecha}T00:00:00.000",
            "vigenciahasta": f"{fecha}T00:00:00.000"}


# Tres días con números escogidos para que la cuenta se vea a ojo:
# 3000, 3500 y 4000 -> promedio 3500, y de 3000 a 4000 son +33,33%.
# Van de más NUEVO a más VIEJO, como los manda la fuente de verdad ($order DESC).
FILAS_OK = [fila_trm("2026-07-03", "4000"),
            fila_trm("2026-07-02", "3500"),
            fila_trm("2026-07-01", "3000")]

RESUMEN_OK = {
    "registros": 3,
    "desde": "2026-07-01",      # el T00:00:00.000 tiene que haberse ido
    "hasta": "2026-07-03",
    "primero": 3000.0,          # float: llegó como texto y salió número
    "ultimo": 4000.0,
    "maximo": 4000.0,
    "minimo": 3000.0,
    "promedio": 3500.0,
    "cambio_pct": 33.33,        # (4000-3000)/3000*100 = 33.333... -> 33.33
    "descartados": None,        # ⚠️ None = la llave NO debe existir.
}                               #    Sin filas malas, "descartados": 0 sería
                                #    ruido que se repaga en cada vuelta.

CASOS_HISTORIAL_FUENTE = [
    # (etiqueta,                 (datos_falsos, error_falso),      argumentos,  esperado)

    # --- camino feliz, aritmética verificable a ojo ---
    ("feliz 3 dias",             (FILAS_OK, None),                 (3,),        RESUMEN_OK),

    # ⭐ EL MISMO caso con las filas AL REVÉS, y el esperado es idéntico.
    #    Prueba el serie.sort(): el resumen no depende de en qué orden las
    #    mande el servidor. Sin el sort, "desde" y "hasta" saldrían cambiados
    #    y el cambio_pct saldría -25.0 en vez de +33.33 (el signo al revés).
    ("feliz con filas al reves", (list(reversed(FILAS_OK)), None), (3,),        RESUMEN_OK),

    # --- borde: un solo día. primero == ultimo, así que el cambio es 0%.
    #     Comprueba de paso que no hay ZeroDivisionError con un solo punto.
    ("un solo dia",              ([fila_trm("2026-07-03", "4000")], None), (1,),
                                 {"registros": 1, "cambio_pct": 0.0, "promedio": 4000.0}),

    # --- borde: 30.0 (float entero) SE ACEPTA. Rechazarlo sería castigar al
    #     modelo por escribir una coma. Lo que se rechaza es 3.5.
    ("dias 30.0 se acepta",      (FILAS_OK, None),                 (30.0,),     {"registros": 3}),

    # --- borde: el tope EXACTO se acepta. El 401 se rechaza arriba.
    ("dias en el tope exacto",   (FILAS_OK, None),         (MAX_REGISTROS,),    {"registros": 3}),

    # --- el valor como NÚMERO y no como texto: si la fuente cambia y manda
    #     3900 sin comillas, la función tiene que seguir funcionando.
    ("valor numerico, no texto", ([{"valor": 4000, "unidad": "COP",
                                    "vigenciadesde": "2026-07-03T00:00:00.000"}], None), (1,),
                                 {"registros": 1, "promedio": 4000.0}),

    # --- UNA FILA PODRIDA ENTRE BUENAS: se salta, se cuenta, y NO tumba el
    #     resto. Es la decisión del hueco 4. Fíjate que "desde" sigue siendo
    #     el 01: la fila mala del 30 de junio no entró en el resumen.
    ("una fila podrida",         (FILAS_OK + [fila_trm("2026-06-30", "no hay dato")], None), (4,),
                                 {"registros": 3, "descartados": 1, "desde": "2026-07-01"}),

    # --- cada clase de fila podrida, una por una ---
    ("fila que no es dict",      (FILAS_OK + ["3206.18"], None),   (4,),
                                 {"registros": 3, "descartados": 1}),
    ("valor null",               (FILAS_OK + [fila_trm("2026-06-30", None)], None), (4,),
                                 {"registros": 3, "descartados": 1}),
    ("valor cero",               (FILAS_OK + [fila_trm("2026-06-30", "0")], None), (4,),
                                 {"registros": 3, "descartados": 1}),
    ("valor negativo",           (FILAS_OK + [fila_trm("2026-06-30", "-3206.18")], None), (4,),
                                 {"registros": 3, "descartados": 1}),
    # ⚠️ El formato colombiano de verdad: punto de miles y coma decimal.
    #    float("3.206,18") revienta. Es el caso más realista de la lista.
    ("valor con coma decimal",   (FILAS_OK + [fila_trm("2026-06-30", "3.206,18")], None), (4,),
                                 {"registros": 3, "descartados": 1}),
    ("fecha ausente",            (FILAS_OK + [{"valor": "3206.18"}], None), (4,),
                                 {"registros": 3, "descartados": 1}),
    # Una fecha demasiado corta no se puede recortar a 10 ni ordenar bien.
    ("fecha incompleta",         (FILAS_OK + [{"valor": "3206.18",
                                               "vigenciadesde": "2026"}], None), (4,),
                                 {"registros": 3, "descartados": 1}),

    # --- DOS podridas: el contador tiene que decir 2, no "hubo problemas" ---
    ("dos filas podridas",       (FILAS_OK + [fila_trm("2026-06-30", "abc"),
                                              fila_trm("2026-06-29", "")], None), (5,),
                                 {"registros": 3, "descartados": 2}),

    # --- aquí SÍ es error: no queda ni una fila, y un promedio de cero
    #     números no existe (sum([])/len([]) sería ZeroDivisionError) ---
    ("todas podridas",           ([fila_trm("2026-07-03", "abc"),
                                   fila_trm("2026-07-02", "")], None), (2,),   "error"),

    # --- la forma de la respuesta ---
    ("lista vacia",              ([], None),                       (3,),        "error"),
    ("no es lista",              ({"valor": "3206.18"}, None),     (3,),        "error"),

    # --- la red falló: el error de pedir_json se reenvía tal cual ---
    ("error de red",             (None, "No pude conectarme a la fuente (URLError)."), (3,), "error"),
]


# ---------------------------------------------------------------------------
# Casos de trm_en_fecha() — RECHAZOS, sin salir a la red
# ---------------------------------------------------------------------------
# El freno de formato va antes de armar la URL, así que estos mueren en la
# máquina. Corren con LA TRAMPA puesta, y aquí eso importa más que nunca:
# demuestra que la inyección no llega ni a construir la consulta.

CASOS_EN_FECHA = [
    # (etiqueta,             argumentos,                  esperado)

    # --- FORMA ---
    ("fecha None",           (None,),                     "error"),
    ("fecha lista",          ([],),                       "error"),
    ("fecha numero",         (20260730,),                 "error"),

    # --- CONTENIDO: la forma está mal ---
    ("fecha vacia",          ("",),                       "error"),
    ("formato con barras",   ("15/07/2026",),             "error"),
    ("fecha en palabras",    ("15 de julio",),            "error"),
    ("fecha al reves",       ("30-07-2026",),             "error"),

    # --- CONTENIDO: la forma está PERFECTA y el día NO EXISTE. Este es el
    #     caso que justifica strptime: un freno hecho con len() e isdigit()
    #     los dejaría pasar a los dos.
    ("30 de febrero",        ("2026-02-30",),             "error"),
    ("mes 99",               ("9999-99-99",),             "error"),

    # --- 🚨 LA INYECCIÓN. Probada contra la fuente real el 2026-07-30: sin
    #     este freno, la primera devolvía 1000 filas en vez de 1 (~125.000
    #     caracteres, ~31.000 tokens repagados en cada vuelta).
    #     Que estos casos pasen CON LA TRAMPA PUESTA es la prueba de que no
    #     llegan a la red: no es que la consulta salga mal armada, es que
    #     nunca se arma.
    ("inyeccion OR 1=1",     ("2026-07-30' OR '1'='1",),  "error"),
    ("inyeccion comentario", ("2026-07-30'; --",),        "error"),
]


# ---------------------------------------------------------------------------
# Casos de trm_en_fecha() CON SERVIDOR DE MENTIRA
# ---------------------------------------------------------------------------
# ⚠️ PIEZA NUEVA: esta es la primera herramienta que hace DOS consultas
# distintas — la del dato ($where) y, solo si no hubo dato, la del rango que
# cubre la fuente ($select con min/max). Un doble que conteste siempre lo mismo
# no sirve: para probar "esa fecha es futura" hace falta que la primera
# devuelva vacío Y la segunda devuelva el rango.
# → El doble ahora tiene que saber QUÉ le están preguntando.


def servidor_dos_respuestas(respuesta_where, respuesta_rango):
    """Doble que contesta distinto según a qué URL le pregunten.

    Mira si la URL trae "$select" (la del rango) o no (la del dato). Es la
    misma idea del servidor_falso, un escalón más arriba: el actor ahora tiene
    dos parlamentos y escoge según la pregunta.
    """
    def falso(url, **kwargs):
        return respuesta_rango if "$select" in url else respuesta_where
    return falso


# El rango que informa la fuente de verdad (verificado el 2026-07-30).
RANGO_OK = ([{"primera": "1991-12-02T00:00:00.000",
              "ultima": "2026-07-30T00:00:00.000"}], None)


def fila_vigencia(desde, hasta, valor):
    """Una fila con vigencia de VARIOS días: así es un fin de semana."""
    return {"valor": valor, "unidad": "COP",
            "vigenciadesde": f"{desde}T00:00:00.000",
            "vigenciahasta": f"{hasta}T00:00:00.000"}


CASOS_EN_FECHA_FUENTE = [
    # (etiqueta,   respuesta_$where,   respuesta_$select,   argumentos,   esperado)

    # --- camino feliz ---
    ("feliz",
     ([fila_trm("2026-07-15", "4000")], None), RANGO_OK, ("2026-07-15",),
     {"trm": 4000.0, "fecha_pedida": "2026-07-15", "vigente_desde": "2026-07-15"}),

    # ⭐ EL DOMINGO: se pregunta por el 26 y la fila vigente es la del 24 al 26.
    #    El esperado comprueba que `fecha_pedida` y `vigente_desde` son
    #    DISTINTOS. Si se hubieran juntado en un solo campo, el agente diría
    #    "el 26 la TRM fue X" como si ese día se hubiera publicado.
    ("domingo",
     ([fila_vigencia("2026-07-24", "2026-07-26", "4000")], None), RANGO_OK, ("2026-07-26",),
     {"trm": 4000.0, "fecha_pedida": "2026-07-26",
      "vigente_desde": "2026-07-24", "vigente_hasta": "2026-07-26"}),

    # ⭐ LA NORMALIZACIÓN: "2026-7-5" sin ceros SÍ se acepta (strptime no los
    #    exige) y tiene que salir normalizada. Este caso nació de un defecto
    #    real de la primera corrida: sin normalizar, se validaba una cosa y se
    #    mandaba otra, y la comparación de fechas como texto se rompía
    #    ("2026-7-5" > "2026-07-30" es True).
    ("fecha sin ceros se normaliza",
     ([fila_trm("2026-07-05", "4000")], None), RANGO_OK, ("2026-7-5",),
     {"fecha_pedida": "2026-07-05", "trm": 4000.0}),

    # --- CERO FILAS: los cuatro motivos, que es lo que él pidió distinguir ---
    ("sin dato: futura",
     ([], None), RANGO_OK, ("2027-01-01",),            {"motivo": "futura"}),
    ("sin dato: muy antigua",
     ([], None), RANGO_OK, ("1990-01-01",),            {"motivo": "muy_antigua"}),
    # Dentro del rango publicado y aun así sin fila: no es culpa de quien preguntó.
    ("sin dato: hueco en la fuente",
     ([], None), RANGO_OK, ("2026-05-05",),            {"motivo": "hueco"}),
    # BORDE: exactamente la fecha del último dato. NO es futura (no es `>`).
    ("sin dato: borde, el ultimo dia",
     ([], None), RANGO_OK, ("2026-07-30",),            {"motivo": "hueco"}),

    # --- y si la segunda consulta tampoco sirve, NO se inventa el motivo ---
    ("sin dato: el rango no responde",
     ([], None), (None, "No pude conectarme a la fuente (URLError)."), ("2026-05-05",),
     {"motivo": "desconocido"}),
    ("sin dato: rango con basura",
     ([], None), ({"otra cosa": 1}, None), ("2026-05-05",),
     {"motivo": "desconocido"}),
    ("sin dato: rango sin las llaves",
     ([], None), ([{"primera": None, "ultima": None}], None), ("2026-05-05",),
     {"motivo": "desconocido"}),

    # --- fallas de la fuente: son "error" y NO llevan motivo (la llave no
    #     existe, y por eso el esperado dice None) ---
    ("no es lista",
     ({"valor": "4000"}, None), RANGO_OK, ("2026-07-15",),  {"motivo": None}),
    ("fila que no es dict",
     (["4000"], None), RANGO_OK, ("2026-07-15",),           {"motivo": None}),
    ("valor null",
     ([fila_trm("2026-07-15", None)], None), RANGO_OK, ("2026-07-15",), {"motivo": None}),
    ("valor con coma decimal",
     ([fila_trm("2026-07-15", "3.206,18")], None), RANGO_OK, ("2026-07-15",), {"motivo": None}),
    ("valor cero",
     ([fila_trm("2026-07-15", "0")], None), RANGO_OK, ("2026-07-15",), {"motivo": None}),
    ("valor numerico, no texto",
     ([fila_trm("2026-07-15", 4000)], None), RANGO_OK, ("2026-07-15",), {"trm": 4000.0}),

    # --- la red falló en la consulta principal ---
    ("error de red",
     (None, "No pude conectarme a la fuente (URLError)."), RANGO_OK, ("2026-07-15",),
     {"motivo": None}),
]


def igual_estricto(a, b):
    """`==` pero exigiendo además el mismo TIPO, y en los dict llave por llave.

    Hace falta porque `{"promedio": 4000.0} == {"promedio": 4000}` es True:
    el `==` de los diccionarios compara los valores con `==`, y 4.0 == 4.
    O sea que la comparación de tipos que endureciste en el paso 5 se perdía
    en cuanto el esperado dejó de ser un número suelto. Es el mismo defecto de
    entonces, escondido un piso más abajo.
    """
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(igual_estricto(a[k], b[k]) for k in a)
    return a == b


def servidor_falso(respuesta):
    """Devuelve un pedir_json de mentira que siempre contesta `respuesta`.

    Es una función que fabrica funciones. Se hace así, y no con un lambda
    dentro del bucle, porque un lambda se acordaría de la ÚLTIMA respuesta del
    bucle y no de la de su caso. Aquí cada caso se queda con la suya.
    """
    def falso(url, **kwargs):
        return respuesta
    return falso


def limpiar_caja():
    """Deja caja/ vacía, para que cada caso arranque de un ESTADO CONOCIDO.

    Sin esto, el archivo que dejó la corrida de ayer hace que la comprobación
    "el archivo existe" pase incluso si la función ya no escribe nada.
    Solo borra archivos DENTRO de caja/: nunca sube de carpeta.
    """
    CAJA.mkdir(exist_ok=True)
    for p in CAJA.iterdir():
        if p.is_file():
            p.unlink()


# ---------------------------------------------------------------------------
# El bucle  <-- ESTO LO ESCRIBES TÚ
# ---------------------------------------------------------------------------
fallos = 0

print("=== convertir() ===")

for etiqueta, args, esperado in CASOS_CONVERTIR:
    try:
        r = convertir(*args)
    except Exception as e:
        obtenido = f"REVENTO: {type(e).__name__}"
    else:
        obtenido = "error" if "error" in r else r["resultado"]

    # El valor tiene que coincidir Y ser del mismo tipo.
    # Sin la segunda mitad, 4.0 == 4 es verdadero y el caso "redondeo a COP"
    # salía en verde con el defecto puesto. Una prueba en verde que esconde un
    # defecto es lo peor que puede pasar aquí.
    ok = (obtenido == esperado) and (type(obtenido) is type(esperado))
    if not ok:
        fallos += 1

    marca = "ok   " if ok else "FALLA"
    print(f"{marca} {etiqueta:22} esperado={esperado!r:10} obtenido={obtenido!r}")


# --- Segundo bucle: guardar_reporte() -------------------------------------
# Es un bucle APARTE y no uno solo con un `if` dentro. Las dos funciones se
# revisan de formas distintas (una devuelve un valor, la otra escribe un
# archivo). Forzar un bucle a hacer los dos trabajos lo vuelve ilegible.

print("\n=== guardar_reporte() ===")

for etiqueta, args, esperado in CASOS_GUARDAR:
    nombre, contenido = args
    limpiar_caja()          # <-- estado conocido antes de CADA caso

    try:
        r = guardar_reporte(*args)
    except Exception as e:
        obtenido, pero = f"REVENTO: {type(e).__name__}", ""
    else:
        if "error" in r:
            obtenido = "error"
            # Rechazar no basta: el disco tiene que haber quedado intacto.
            pero = "" if not any(CAJA.iterdir()) else " PERO ESCRIBIO ALGO"
        else:
            obtenido = "guardado"
            ruta = CAJA / nombre
            if not ruta.exists():
                pero = " PERO NO HAY ARCHIVO"
            elif ruta.read_text(encoding="utf-8") != contenido:
                pero = " PERO EL CONTENIDO NO COINCIDE"
            else:
                pero = ""

    # Dos condiciones: el veredicto correcto Y el disco como debe estar.
    ok = (obtenido == esperado) and (pero == "")
    if not ok:
        fallos += 1

    marca = "ok   " if ok else "FALLA"
    print(f"{marca} {etiqueta:22} esperado={esperado!r:10} obtenido={obtenido!r}{pero}")

limpiar_caja()              # no dejar basura al terminar


# --- Tercer bucle: tasa() --------------------------------------------------
# ⚠️ DECISIÓN PENDIENTE PARA TI: este bucle es casi idéntico al de convertir().
# Solo cambian dos cosas: qué función se llama, y en qué llave viene el
# resultado ("resultado" vs "tasa"). Con guardar_reporte el bucle aparte estaba
# justificado (revisa el DISCO, es otro trabajo). Aquí no: las dos funciones se
# revisan igual, mirando lo que devuelven.
# O sea que tu propio argumento de "una regla en un solo sitio" ahora apunta al
# otro lado: estos dos bucles se podrían juntar en un ayudante que reciba la
# función y el nombre de la llave. Se dejó separado para no tocar el bucle que
# escribiste tú, pero la duplicación es real y la decisión es tuya.

print("\n=== tasa() ===")

for etiqueta, args, esperado in CASOS_TASA:
    try:
        r = tasa(*args)
    except Exception as e:
        # Si aquí sale AssertionError, es LA TRAMPA: un caso llegó a la red.
        obtenido = f"REVENTO: {type(e).__name__}"
    else:
        obtenido = "error" if "error" in r else r["tasa"]

    ok = (obtenido == esperado) and (type(obtenido) is type(esperado))
    if not ok:
        fallos += 1

    marca = "ok   " if ok else "FALLA"
    print(f"{marca} {etiqueta:22} esperado={esperado!r:10} obtenido={obtenido!r}")


# --- Cuarto bucle: historial(), rechazos ----------------------------------
# Va AQUÍ, antes de los dobles, porque necesita LA TRAMPA todavía puesta: si
# algún freno de `dias` se moviera para después del pedir_json, estos casos
# saltarían con AssertionError en vez de pasar tranquilos.

print("\n=== historial() rechazos (sin red) ===")

for etiqueta, args, esperado in CASOS_HISTORIAL:
    try:
        r = historial(*args)
    except Exception as e:
        obtenido = f"REVENTO: {type(e).__name__}"
    else:
        obtenido = "error" if "error" in r else r

    ok = igual_estricto(obtenido, esperado)
    if not ok:
        fallos += 1

    marca = "ok   " if ok else "FALLA"
    print(f"{marca} {etiqueta:22} esperado={esperado!r:10} obtenido={obtenido!r}")


# --- Quinto bucle: trm_en_fecha(), rechazos -------------------------------
# Con LA TRAMPA todavía puesta. Los dos casos de inyección son los que más
# valen aquí: si pasaran, saltaría AssertionError — o sea que la consulta se
# habría llegado a armar. Que salgan como "error" limpio significa que el
# freno los mató ANTES de tocar la URL.

print("\n=== trm_en_fecha() rechazos (sin red) ===")

for etiqueta, args, esperado in CASOS_EN_FECHA:
    try:
        r = trm_en_fecha(*args)
    except Exception as e:
        obtenido = f"REVENTO: {type(e).__name__}"
    else:
        obtenido = "error" if "error" in r else r

    ok = igual_estricto(obtenido, esperado)
    if not ok:
        fallos += 1

    marca = "ok   " if ok else "FALLA"
    print(f"{marca} {etiqueta:22} esperado={esperado!r:10} obtenido={obtenido!r}")


# --- Sexto bucle: tasa() con el servidor de mentira -----------------------
# La diferencia con el bucle de arriba: aquí ANTES de cada caso se le instala a
# herramientas un pedir_json falso. Después del bucle se vuelve a poner la
# trampa, para que nadie de aquí en adelante toque la red por descuido.

print("\n=== tasa() con servidor de mentira ===")

for etiqueta, respuesta, args, esperado in CASOS_TASA_FUENTE:
    herramientas.pedir_json = servidor_falso(respuesta)   # <-- el doble entra

    try:
        r = tasa(*args)
    except Exception as e:
        obtenido = f"REVENTO: {type(e).__name__}"
    else:
        obtenido = "error" if "error" in r else r["tasa"]

    ok = (obtenido == esperado) and (type(obtenido) is type(esperado))
    if not ok:
        fallos += 1

    marca = "ok   " if ok else "FALLA"
    print(f"{marca} {etiqueta:22} esperado={esperado!r:10} obtenido={obtenido!r}")


# ---------------------------------------------------------------------------
# EL PUENTE DE tasa(): la llave inversa
# ---------------------------------------------------------------------------
# 🚨 ESTOS CASOS EXISTEN POR UN DEFECTO REAL, encontrado por la rúbrica del
#    paso 10 y no por estos evals. Vale la pena tenerlo presente:
#
#    El agente recibió tasa(de="COP", a="USD") = 0.0003117558994603884, tuvo que
#    invertirla para contestar en pesos, la calculó de cabeza y dijo 3.209,64
#    cuando lo correcto es 3.207,64. Dos pesos de más, perfectamente creíbles.
#
#    ⚠️ Y ESTOS 116 CASOS NO PODÍAN VERLO, por una razón que enseña: la cuenta
#       no pasó por ninguna función nuestra. Ocurrió DENTRO del modelo y salió
#       directo al texto del usuario.
#       → Un eval determinista prueba tu CÓDIGO. No puede ver lo que el modelo
#         hace en su cabeza. Para eso hacía falta la rúbrica.
#
#    Lo que sí podemos probar aquí, gratis y siempre igual, es que el puente
#    exista, se llame como debe y dé el número correcto. Ahora que ese número
#    está en la mesa, el modelo no tiene que inventarlo.

CASOS_TASA_PUENTE = [
    # (etiqueta,           (datos_falsos, error_falso),                    args,           llave esperada,   valor esperado)
    ("USD->COP",           ({"rates": {"USD": 1, "COP": 4000}}, None),     ("USD", "COP"), "usd_por_1_cop",  0.00025),
    ("COP->USD",           ({"rates": {"USD": 1, "COP": 4000}}, None),     ("COP", "USD"), "cop_por_1_usd",  4000.0),
    # La triangulación otra vez: 1 EUR = 2 USD, 1 USD = 4000 COP -> 1 EUR = 8000 COP,
    # así que el puente de EUR->COP tiene que decir 1/8000 = 0.000125.
    ("EUR->COP",           ({"rates": {"USD": 1, "EUR": 0.5, "COP": 4000}}, None),
                                                                           ("EUR", "COP"), "eur_por_1_cop",  0.000125),
]

print()
print("--- tasa(): el puente (la llave inversa) ---")

for etiqueta, respuesta, args, llave, esperado in CASOS_TASA_PUENTE:
    herramientas.pedir_json = servidor_falso(respuesta)

    try:
        r = tasa(*args)
    except Exception as e:
        obtenido = f"REVENTO: {type(e).__name__}"
    else:
        # ⭐ Se comprueban DOS cosas, no una: que la llave se llame exactamente
        #    así (el modelo la lee por el nombre) y que el número sea el bueno.
        #    Un puente con el nombre cambiado es un puente que nadie cruza.
        obtenido = r.get(llave, f"NO EXISTE LA LLAVE {llave!r}")

    ok = (obtenido == esperado) and (type(obtenido) is type(esperado))
    if not ok:
        fallos += 1

    marca = "ok   " if ok else "FALLA"
    print(f"{marca} {etiqueta:22} {llave:16} esperado={esperado!r:10} obtenido={obtenido!r}")

# --- Sexto bucle: trm() con el servidor de mentira ------------------------

print("\n=== trm() con servidor de mentira ===")

for etiqueta, respuesta, esperado in CASOS_TRM:
    herramientas.pedir_json = servidor_falso(respuesta)

    try:
        r = trm()
    except Exception as e:
        obtenido = f"REVENTO: {type(e).__name__}"
    else:
        obtenido = "error" if "error" in r else r["trm"]

    ok = (obtenido == esperado) and (type(obtenido) is type(esperado))
    if not ok:
        fallos += 1

    marca = "ok   " if ok else "FALLA"
    print(f"{marca} {etiqueta:42} esperado={esperado!r:10} obtenido={obtenido!r}")

# --- Séptimo bucle: historial() con el servidor de mentira ----------------
# La diferencia con los otros bucles del doble: aquí `esperado` casi siempre es
# un DICCIONARIO con las llaves que importan, no un número suelto. Se comparan
# solo esas llaves — el resto del resumen puede crecer sin romper las pruebas.
# `r.get(k)` devuelve None cuando la llave no está, y por eso un esperado con
# "descartados": None comprueba que la llave NO exista.

print("\n=== historial() con servidor de mentira ===")

for etiqueta, respuesta, args, esperado in CASOS_HISTORIAL_FUENTE:
    herramientas.pedir_json = servidor_falso(respuesta)

    try:
        r = historial(*args)
    except Exception as e:
        obtenido = f"REVENTO: {type(e).__name__}"
    else:
        if "error" in r:
            obtenido = "error"
        else:
            obtenido = {k: r.get(k) for k in esperado}

    ok = igual_estricto(obtenido, esperado)
    if not ok:
        fallos += 1

    # Un esperado con 10 llaves no cabe en una línea. En verde se imprime
    # cuántas llaves se verificaron; solo al fallar se muestra todo, que es
    # cuando de verdad hace falta leerlo.
    if ok:
        cuantas = len(esperado) if isinstance(esperado, dict) else 1
        print(f"ok    {etiqueta:26} {cuantas} llave(s) verificada(s)")
    else:
        print(f"FALLA {etiqueta:26} esperado={esperado!r}")
        print(f"      {'':26} obtenido={obtenido!r}")

# --- Octavo bucle: trm_en_fecha() con el doble de DOS respuestas ----------

print("\n=== trm_en_fecha() con servidor de mentira ===")

for etiqueta, resp_where, resp_rango, args, esperado in CASOS_EN_FECHA_FUENTE:
    herramientas.pedir_json = servidor_dos_respuestas(resp_where, resp_rango)

    try:
        r = trm_en_fecha(*args)
    except Exception as e:
        obtenido = f"REVENTO: {type(e).__name__}"
    else:
        obtenido = {k: r.get(k) for k in esperado}

    ok = igual_estricto(obtenido, esperado)
    if not ok:
        fallos += 1

    if ok:
        print(f"ok    {etiqueta:32} {len(esperado)} llave(s) verificada(s)")
    else:
        print(f"FALLA {etiqueta:32} esperado={esperado!r}")
        print(f"      {'':32} obtenido={obtenido!r}")

herramientas.pedir_json = trampa_de_red      # se restaura la prohibición

total = (len(CASOS_CONVERTIR) + len(CASOS_GUARDAR)
         + len(CASOS_TASA) + len(CASOS_TASA_FUENTE) + len(CASOS_TASA_PUENTE)
         + len(CASOS_TRM)
         + len(CASOS_HISTORIAL) + len(CASOS_HISTORIAL_FUENTE)
         + len(CASOS_EN_FECHA) + len(CASOS_EN_FECHA_FUENTE))
print(f"\n{total} casos, {fallos} fallaron")
print("TODO BIEN" if fallos == 0 else "HAY FALLOS")

