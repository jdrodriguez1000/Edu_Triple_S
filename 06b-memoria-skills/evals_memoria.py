"""
evals.py — Las pruebas de memoria.py  (nivel 6b, paso 3)

Corre en un segundo, no usa internet y cuesta $0.00. Igual que el evals.py del
5b, y por la misma razón: lo que se puede probar gratis se prueba gratis, y a
la corrida pagada solo le queda lo que de verdad no se puede probar de otra
forma.

⚠️ PERO AQUÍ EL PELIGRO ES OTRO, Y ES NUEVO EN ESTE ARCHIVO.

   En el 5b la prohibición era "ningún caso puede tocar la RED". Aquí la red no
   existe: memoria.py no sabe qué es internet. El peligro es el DISCO.

   Si estas pruebas escriben en el memoria.json de verdad, cada corrida del eval
   le BORRA AL AGENTE LO QUE HABÍA APRENDIDO. Y lo peor es que no se notaría:
   el eval saldría en verde, feliz, mientras destruye el archivo que existe para
   sobrevivir.

   → Es la misma familia del registro del paso 9 que caía encima del anterior, y
     de la trampa del examen.py de la sesión 17. Tercera vez que aparece:
     UN PROGRAMA DE PRUEBA QUE ESCRIBE DONDE ESCRIBE EL DE VERDAD.

   Se resuelve con dos cosas, no con una:
     1. Se DESVÍA memoria.ARCHIVO a un archivo de mentiras.
     2. Se pone una TRAMPA que revienta si el archivo real cambió.
   La 1 sola sería una promesa. La 2 la convierte en un hecho comprobado.
"""

import json
import sys
from datetime import date
from pathlib import Path

import memoria

# ⚠️ Importar agente.py NO lo corre ni cuesta un centavo: lo protege su
#    `if __name__ == "__main__"`. Es lo mismo que descubrió examen.py en la
#    sesión 17, y por eso aquel `if` dejó de ser una formalidad.
import agente

sys.stdout.reconfigure(encoding="utf-8")

# ---------------------------------------------------------------------------
# La trampa: prueba que este eval NO toca la memoria de verdad
# ---------------------------------------------------------------------------
# Se guarda el archivo real y su contenido exacto ANTES de nada. Al final se
# compara. Si algún caso se le atravesó, salta en voz alta.
#
# Es el sabotaje del nivel 3 usado al revés otra vez: en vez de romper el código
# para ver si la prueba lo nota, se vigila el CAMINO PROHIBIDO para ver si
# alguien lo pisa.

ARCHIVO_REAL = memoria.ARCHIVO
ANTES_REAL = ARCHIVO_REAL.read_bytes() if ARCHIVO_REAL.exists() else None

# El desvío. A partir de aquí, todo lo que haga memoria.py cae en este archivo.
memoria.ARCHIVO = ARCHIVO_REAL.parent / "memoria_de_prueba.json"

HOY = date.today().isoformat()


# ---------------------------------------------------------------------------
# Ayudantes
# ---------------------------------------------------------------------------
def sembrar(textos):
    """Deja el archivo de pruebas con exactamente estos datos. ESTADO CONOCIDO.

    Es el limpiar_caja() del 5b: sin esto, lo que dejó el caso anterior hace
    que un caso pase por la razón equivocada.

    Escribe el JSON a mano, sin usar guardar_dato(), a propósito: si la semilla
    usara la función que se está probando, un defecto en guardar_dato() dañaría
    la semilla Y la comprobación, y las dos mentirían de acuerdo.
    """
    filas = [{"dato": t, "fecha": HOY} for t in textos]
    memoria.ARCHIVO.write_text(
        json.dumps({"datos": filas}, ensure_ascii=False), encoding="utf-8"
    )


def escribir_crudo(texto):
    """Deja en el archivo un contenido cualquiera, incluso uno inválido."""
    memoria.ARCHIVO.write_text(texto, encoding="utf-8")


def borrar_archivo():
    memoria.ARCHIVO.unlink(missing_ok=True)


def textos():
    """Los datos guardados, como lista de strings. Para comparar cómodo."""
    return [f["dato"] for f in memoria.cargar_memoria()]


fallos = 0
total = 0


def revisar(etiqueta, obtenido, esperado, ancho=34):
    """Compara, cuenta e imprime. Un solo sitio, para no repetirlo ocho veces.

    ⚠️ El `type(obtenido) is type(esperado)` viene del 5b y no es adorno: sin él,
       4.0 == 4 y True == 1 salen en verde. Una prueba en verde que esconde un
       defecto es lo peor que puede pasar aquí.
    """
    global fallos, total
    total += 1
    ok = obtenido == esperado and type(obtenido) is type(esperado)
    if not ok:
        fallos += 1
    marca = "ok   " if ok else "FALLA"
    print(f"{marca} {etiqueta:{ancho}} esperado={esperado!r:24} obtenido={obtenido!r}")


# ===========================================================================
# 1) cargar_memoria()  —  los cuatro caminos, y NUNCA revienta
# ===========================================================================
print("=== cargar_memoria() ===")

# (a) No existe. Es lo NORMAL la primera vez, no un error.
borrar_archivo()
revisar("archivo no existe", memoria.cargar_memoria(), [])

# (b) Dañado. Tiene que devolver [] Y — esto es lo importante — DEJAR EL
#     ARCHIVO QUIETO. Borrarlo es tentador y destruye la única evidencia.
escribir_crudo("{esto no es json, se rompió a mitad")
revisar("json dañado -> lista vacía", memoria.cargar_memoria(), [])
revisar("json dañado -> NO se borró", memoria.ARCHIVO.exists(), True)

# (c) JSON válido, pero con otra forma. Pasa el día que cambie el formato y
#     quede un archivo viejo dando vueltas.
escribir_crudo('["trabaja en pesos"]')          # una lista pelada
revisar("json con forma de lista", memoria.cargar_memoria(), [])

escribir_crudo('{"datos": "no soy una lista"}')  # la llave está, el valor no
revisar('la llave "datos" no es lista', memoria.cargar_memoria(), [])

escribir_crudo('{"otra_cosa": []}')              # falta la llave
revisar('falta la llave "datos"', memoria.cargar_memoria(), [])

escribir_crudo('42')                             # un número suelto
revisar("json que es un número", memoria.cargar_memoria(), [])

# (d) Camino feliz.
sembrar(["trabaja en pesos colombianos", "es contador"])
revisar("dos datos buenos", textos(), ["trabaja en pesos colombianos", "es contador"])

# (d-bis) Filas basura MEZCLADAS con buenas. El archivo es editable a mano, así
#         que su contenido viene de FUERA: no se confía en fila por fila.
#         ⚠️ Este caso es el que separa "el archivo es válido" de "cada fila lo
#            es". Sin él, una sola fila rota tumbaría el arranque del agente.
escribir_crudo(json.dumps({"datos": [
    {"dato": "es contador", "fecha": HOY},
    {"dato": 42, "fecha": HOY},        # el dato no es texto
    "soy un string suelto",            # ni siquiera es un dict
    {"fecha": HOY},                    # le falta el dato
    {"dato": "vive en Bogotá", "fecha": HOY},
]}))
revisar("filtra filas rotas", textos(), ["es contador", "vive en Bogotá"])


# ===========================================================================
# 2) guardar_dato()  —  el par (guardado, motivo)
# ===========================================================================
# Cada caso es un DATO: (etiqueta, semilla, texto, esperado).
# Regla del 5b, que sigue mandando: UN caso, UNA variable.
#
# ⭐ Se comprueba el MOTIVO, no solo el True/False. Un False pelado no distingue
#    "el modelo mandó basura" de "eso ya lo sabíamos" — y como este nivel quitó
#    el permiso, el motivo es lo ÚNICO que va a quedar escrito en la huella.

CASOS_GUARDAR = [
    # (etiqueta,                    semilla,              texto,        esperado)

    # --- camino feliz ---
    ("camino feliz",                [],                   "es contador",  (True, "guardado")),

    # --- lo vacío: el modelo puede llamar recordar("") ---
    ("cadena vacía",                [],                   "",             (False, "vacio")),
    ("solo espacios",               [],                   "   ",          (False, "vacio")),
    ("solo saltos de línea",        [],                   "\n\t ",        (False, "vacio")),

    # --- el largo. Los DOS bordes, porque un `>` mal puesto solo se ve aquí:
    #     con 200 tiene que pasar y con 201 tiene que fallar. Probar solo uno
    #     de los dos deja el error de "uno más" vivo. ---
    ("justo en el límite (200)",    [],                   "x" * 200,      (True, "guardado")),
    ("uno más del límite (201)",    [],                   "x" * 201,      (False, "muy_largo")),

    # --- lo que no es texto. Hoy el modelo manda strings, pero el harness no
    #     puede confiar en eso: es el freno 8 del paso 8, aquí adentro. ---
    ("le llega un número",          [],                   42,             (False, "no_es_texto")),
    ("le llega None",               [],                   None,           (False, "no_es_texto")),
    ("le llega una lista",          [],                   ["a"],          (False, "no_es_texto")),

    # --- lo repetido: NO se descarta, se le refresca la fecha. Que el modelo
    #     vuelva a decir lo mismo es evidencia de que sigue siendo cierto. ---
    ("repetido exacto",             ["es contador"],      "es contador",  (True, "refrescado")),
    ("repetido en MAYÚSCULAS",      ["es contador"],      "ES CONTADOR",  (True, "refrescado")),
    ("repetido con espacios",       ["es contador"],      "  es contador ", (True, "refrescado")),
]

print("\n=== guardar_dato() ===")

for etiqueta, semilla, texto, esperado in CASOS_GUARDAR:
    sembrar(semilla)
    try:
        obtenido = memoria.guardar_dato(texto)
    except Exception as e:
        obtenido = f"REVENTO: {type(e).__name__}"
    revisar(etiqueta, obtenido, esperado)


# --- Y lo que el par (guardado, motivo) NO alcanza a decir --------------
# Un motivo correcto no garantiza que el archivo quedara bien. Estas cuatro
# comprobaciones miran el ESTADO, no el valor devuelto.
print("\n=== guardar_dato(): el estado del archivo ===")

sembrar([])
memoria.guardar_dato("  es contador  ")
revisar("guarda el texto SIN espacios", textos(), ["es contador"])

sembrar([])
memoria.guardar_dato("es contador")
revisar("le pone la fecha de hoy", memoria.cargar_memoria()[0]["fecha"], HOY)

sembrar(["es contador"])
memoria.guardar_dato("ES CONTADOR")
revisar("el repetido NO duplica", len(memoria.cargar_memoria()), 1)

sembrar(["es contador"])
memoria.guardar_dato("")
revisar("lo rechazado no toca el archivo", textos(), ["es contador"])


# ===========================================================================
# 3) El tope  —  la política de olvido
# ===========================================================================
# ⭐ "Un sistema de memoria sin política de olvido no está terminado."
#    Este es el bloque que lo comprueba.

print("\n=== el tope (política de olvido) ===")

llenos = [f"dato {i}" for i in range(memoria.TOPE)]

sembrar(llenos)
revisar(f"caben {memoria.TOPE} sin desplazar", len(memoria.cargar_memoria()), memoria.TOPE)

sembrar(llenos)
revisar("el que sobra dice 'desplazo'", memoria.guardar_dato("el nuevo"), (True, "desplazo"))

sembrar(llenos)
memoria.guardar_dato("el nuevo")
revisar("nunca pasa del tope", len(memoria.cargar_memoria()), memoria.TOPE)
sembrar(llenos)
memoria.guardar_dato("el nuevo")
revisar("salió el más viejo", "dato 0" in textos(), False)
sembrar(llenos)
memoria.guardar_dato("el nuevo")
revisar("entró el nuevo", "el nuevo" in textos(), True)
sembrar(llenos)
memoria.guardar_dato("el nuevo")
revisar("el segundo más viejo se queda", "dato 1" in textos(), True)

# ⚠️ Y el caso que se olvida: un REFRESCADO no debe desplazar a nadie. Si
#    refrescar contara como dato nuevo, repetir lo mismo ocho veces borraría
#    toda la memoria — con motivo 'refrescado', o sea sin que nada se viera mal.
sembrar(llenos)
revisar("refrescar estando lleno", memoria.guardar_dato("dato 0"), (True, "refrescado"))
sembrar(llenos)
memoria.guardar_dato("dato 0")
revisar("refrescar no bota a nadie", len(memoria.cargar_memoria()), memoria.TOPE)


# ===========================================================================
# 4) memoria_como_texto()  —  la que cuesta dinero
# ===========================================================================
# Es la única de las cuatro que NO toca el disco: recibe la lista por parámetro.
# Por eso aquí no hay que sembrar nada.
#
# ⭐ Y es la que se paga: lo que salga de aquí va en la ENTRADA de CADA vuelta
#    de CADA conversación. Con 27:1 de entrada contra salida, este texto es el
#    precio permanente de tener memoria.

print("\n=== memoria_como_texto() ===")

revisar("lista vacía -> cadena vacía", memoria.memoria_como_texto([]), "")

una = [{"dato": "es contador", "fecha": "2026-07-30"}]
salida = memoria.memoria_como_texto(una)
revisar("mete el dato", "es contador" in salida, True)
revisar("mete la fecha", "2026-07-30" in salida, True)

dos = una + [{"dato": "vive en Bogotá", "fecha": "2026-07-29"}]
salida_dos = memoria.memoria_como_texto(dos)
# Se cuentan las viñetas: dos datos, dos líneas que empiezan por "- ".
#
# ⚠️ ESTE CASO FALLÓ EN LA PRIMERA CORRIDA, Y EL DEFECTO ERA DE LA PRUEBA.
#    La versión original sumaba dos count() sin sentido y esperaba 0; el código
#    devolvió 2, que es LO CORRECTO. Se corrigió la vara, no lo medido.
#    → Es la sesión 17 otra vez: cuando una buena respuesta reprueba, el
#      sospechoso es el examen, no el examinado. Allá fueron dos filas de la
#      rúbrica; aquí fue esta línea.
revisar("una línea por dato", salida_dos.count("\n- "), 2)
revisar("los dos datos están", ("es contador" in salida_dos and "vive en Bogotá" in salida_dos), True)

# La prueba de que NO toca el disco: se apunta ARCHIVO a una ruta que no existe
# y a una carpeta que tampoco. Si la función leyera o escribiera, reventaría.
guardado = memoria.ARCHIVO
memoria.ARCHIVO = Path("/carpeta/que/no/existe/jamas.json")
try:
    r = memoria.memoria_como_texto(una)
    obtenido = "es contador" in r
except Exception as e:
    obtenido = f"REVENTO: {type(e).__name__}"
memoria.ARCHIVO = guardado
revisar("no toca el disco", obtenido, True)


# ===========================================================================
# 5) olvidar()  —  lo que reemplaza al permiso
# ===========================================================================
print("\n=== olvidar() ===")

tres = ["dato A", "dato B", "dato C"]

sembrar(tres)
revisar("olvidar(1) devuelve 1", memoria.olvidar(1), 1)
sembrar(tres)
memoria.olvidar(1)
revisar("borró el del medio", textos(), ["dato A", "dato C"])

sembrar(tres)
revisar("olvidar() sin índice: cuántos", memoria.olvidar(), 3)
sembrar(tres)
memoria.olvidar()
revisar("olvidar() deja vacío", textos(), [])

sembrar(tres)
revisar("índice que no existe", memoria.olvidar(99), 0)
sembrar(tres)
memoria.olvidar(99)
revisar("y no cambió nada", textos(), tres)

# ⚠️ EL CASO TRAICIONERO: en Python, lista[-1] es válido y significa "el último".
#    Sin el freno `0 <= indice`, escribir olvidar(-1) por error borraría el dato
#    MÁS NUEVO — en silencio y devolviendo 1, o sea informando éxito.
sembrar(tres)
revisar("índice negativo (-1)", memoria.olvidar(-1), 0)
sembrar(tres)
memoria.olvidar(-1)
revisar("el -1 no borró nada", textos(), tres)

# Sobre archivo inexistente: no debe reventar. Corre al arrancar el agente.
borrar_archivo()
revisar("olvidar sin archivo", memoria.olvidar(), 0)


# ===========================================================================
# 6) armar_sistema()  —  la unión de la memoria con el agente  (paso 4)
# ===========================================================================
# Es la primera pieza del nivel que vive en agente.py, y sigue costando $0.00:
# armar texto no llama a nadie. Lo que cuesta dinero es MANDARLO, y eso pasa
# una capa más abajo.
#
# ⭐ Y es la razón de que armar_sistema reciba el texto por parámetro en vez de
#    leer el disco: aquí se le meten cadenas inventadas y se mira qué sale.

print("\n=== armar_sistema() (agente.py) ===")

revisar("sin memoria: las reglas enteras", agente.SISTEMA in agente.armar_sistema(""), True)
revisar("None se trata como vacío",
        agente.armar_sistema(None), agente.armar_sistema(""))

con = agente.armar_sistema("Esto es lo que recuerdas: es contador.")
revisar("las reglas siguen enteras", agente.SISTEMA in con, True)
revisar("la memoria entró", "es contador" in con, True)

# --- LA FECHA  (sesión 19: el agente dijo "sábado 2 de agosto" un 31 de julio)
#
# ⭐ Y ESTA ES LA VENTAJA DE QUE `hoy` ENTRE POR PARÁMETRO: se puede probar el
#    lunes sin esperar al lunes. Si armar_sistema llamara a date.today() por
#    dentro, estos cuatro casos serían imposibles de escribir.
from datetime import date as _date

# 2026-07-31 es viernes. 2026-08-02, domingo. Los dos comprobados a mano.
viernes = agente.armar_sistema("", hoy=_date(2026, 7, 31))
revisar("dice el día de la semana", "viernes" in viernes, True)
revisar("dice la fecha en palabras", "31 de julio de 2026" in viernes, True)
revisar("y también en AAAA-MM-DD", "2026-07-31" in viernes, True)

domingo = agente.armar_sistema("", hoy=_date(2026, 8, 2))
revisar("otro día, otro nombre", "domingo" in domingo, True)

# --- EL PUENTE DE LAS FECHAS  (ayer, mañana, el próximo lunes)
#
# 🚨 POR QUÉ EXISTE: con la fecha de hoy puesta, el agente TODAVÍA dijo "el
#    viernes 2 de agosto" (es domingo). Contar días de calendario es aritmética,
#    y la línea vieja lo INVITABA a hacerla ("cuéntala desde esta").
# ⭐ Es el mismo puente de cop_por_1_usd, tercera vez: no le pidas que calcule,
#    dáselo hecho.

revisar("ayer, con su día", "jueves 30 de julio de 2026" in viernes, True)
revisar("mañana, con su día", "sábado 1 de agosto de 2026" in viernes, True)
revisar("el próximo lunes", "lunes 3 de agosto de 2026" in viernes, True)
revisar("prohíbe calcular los demás", "NO calcules el día de la semana" in viernes, True)

# ⚠️ EL BORDE QUE SE OLVIDA: si HOY es lunes, "el próximo lunes" NO es hoy.
#    Sin el `or 7`, el desplazamiento daría 0 y el agente le diría al usuario
#    que el próximo lunes es hoy — creíble, y falso.
un_lunes = agente.armar_sistema("", hoy=_date(2026, 8, 3))
revisar("si hoy es lunes, el próximo es en 7", "lunes 10 de agosto de 2026" in un_lunes, True)

# Cruces de mes y de año: los dos sitios donde una resta de días se rompe.
fin_de_mes = agente.armar_sistema("", hoy=_date(2026, 8, 1))
revisar("ayer cruza el mes", "viernes 31 de julio de 2026" in fin_de_mes, True)

fin_de_ano = agente.armar_sistema("", hoy=_date(2026, 12, 31))
revisar("mañana cruza el año", "1 de enero de 2027" in fin_de_ano, True)

# Y el AAAA-MM-DD va al lado del día, porque es el que necesita trm_en_fecha.
revisar("las fechas traen su AAAA-MM-DD", "(2026-07-30)" in viernes, True)

# El orden: reglas, fecha, memoria. La memoria va de última.
completo = agente.armar_sistema("es contador", hoy=_date(2026, 7, 31))
revisar("orden: reglas < fecha < memoria",
        completo.index("Eres un asistente") < completo.index("Hoy es")
        < completo.index("es contador"), True)

# Los 12 meses y los 7 días existen: un IndexError o un KeyError aquí sería un
# agente que no arranca, y solo el día que caiga en ese mes.
faltan = []
for m in range(1, 13):
    try:
        agente.armar_sistema("", hoy=_date(2026, m, 1))
    except Exception as e:
        faltan.append((m, type(e).__name__))
revisar("los 12 meses tienen nombre", faltan, [])

# ⚠️ EL ORDEN NO ES GUSTO: las reglas del oficio van ANTES que lo que sepamos
#    del usuario. Un dato recordado no puede pisar "nunca inventes un número".
revisar("las reglas van primero", con.index("Eres un asistente") < con.index("es contador"), True)

# El texto de verdad, tal como saldría de memoria_como_texto(). Es el caso que
# más se parece a lo que va a pasar mañana en la corrida pagada.
real = memoria.memoria_como_texto([{"dato": "es contador", "fecha": HOY}])
completo = agente.armar_sistema(real)
revisar("con el texto real: cabe todo", (agente.SISTEMA in completo and HOY in completo), True)

# ⭐ EL PRECIO, MEDIDO EN CARACTERES. La memoria se manda en la ENTRADA de CADA
#    vuelta: no se paga una vez, se paga por vuelta y por conversación, para
#    siempre. Que crezca es normal; que crezca SIN QUE NADIE MIRE, no.
print(f"      el system prompt pasó de {len(agente.SISTEMA)} a {len(completo)} "
      f"caracteres con 1 dato (+{len(completo) - len(agente.SISTEMA)})")

# Y que la función NO toque el disco, con el mismo truco de más arriba: se
# apunta ARCHIVO a una ruta imposible. Si leyera algo, reventaría.
guardado = memoria.ARCHIVO
memoria.ARCHIVO = Path("/carpeta/que/no/existe/jamas.json")
try:
    obtenido = agente.SISTEMA in agente.armar_sistema("hola")
except Exception as e:
    obtenido = f"REVENTO: {type(e).__name__}"
memoria.ARCHIVO = guardado
revisar("armar_sistema no toca el disco", obtenido, True)


# ===========================================================================
# 7) recordar()  —  la herramienta que llama el modelo  (paso 4)
# ===========================================================================
print("\n=== recordar() ===")

CASOS_RECORDAR = [
    # (etiqueta,              semilla,           dato,          guardado, motivo)
    ("dato nuevo",            [],                "es contador", True,  "guardado"),
    ("repetido",              ["es contador"],   "ES CONTADOR", True,  "refrescado"),
    ("vacío",                 [],                "",            False, "vacio"),
    ("no es texto",           [],                42,            False, "no_es_texto"),
    ("muy largo",             [],                "x" * 201,     False, "muy_largo"),
    ("lleno -> desplaza",     [f"dato {i}" for i in range(memoria.TOPE)],
                                                 "el nuevo",    True,  "desplazo"),
]

for etiqueta, semilla, dato, guardado, motivo in CASOS_RECORDAR:
    sembrar(semilla)
    try:
        r = memoria.recordar(dato)
        obtenido = (r["guardado"], r["motivo"])
    except Exception as e:
        obtenido = f"REVENTO: {type(e).__name__}"
    revisar(etiqueta, obtenido, (guardado, motivo))

# ⭐ EL CASO QUE PROTEGE EL FUTURO, Y ES EL MÁS VALIOSO DE ESTE BLOQUE.
#    recordar() busca el mensaje con mensajes[motivo]. Si mañana se le agrega un
#    motivo nuevo a guardar_dato() y se olvida el mensaje, eso es un KeyError
#    DENTRO DEL BUCLE, en mitad de una conversación pagada — y lo atraparía el
#    `except Exception` del paso 8, que lo reporta como "defecto interno".
#    → Aquí ese olvido cuesta un eval en rojo, gratis, en un segundo.
MOTIVOS = ["guardado", "desplazo", "refrescado", "vacio", "muy_largo", "no_es_texto"]
sembrar([])
# Se fuerza cada motivo a mano y se mira si recordar() sabe qué decir.
sin_mensaje = []
for m in MOTIVOS:
    original = memoria.guardar_dato
    memoria.guardar_dato = lambda _t, _m=m: (True, _m)
    try:
        memoria.recordar("lo que sea")
    except KeyError:
        sin_mensaje.append(m)
    finally:
        memoria.guardar_dato = original
revisar("todo motivo tiene mensaje", sin_mensaje, [])

# El resultado viaja como tool_result, y el content de un tool_result es TEXTO.
# Si algo aquí no fuera serializable, reventaría en el bucle, no aquí.
sembrar([])
r = memoria.recordar("es contador")
try:
    crudo = json.dumps(r, ensure_ascii=False)
    obtenido = isinstance(crudo, str)
except Exception as e:
    obtenido = f"REVENTO: {type(e).__name__}"
revisar("el resultado es JSON válido", obtenido, True)

# ⚠️ Y lo que NO debe devolver: la memoria entera. Sería cómodo y se pagaría en
#    la entrada de cada vuelta que falte. Es la deuda del tamaño del tool_result.
sembrar([f"dato numero {i} con texto de relleno" for i in range(memoria.TOPE)])
r = memoria.recordar("es contador")
revisar("no devuelve la memoria entera", "dato numero 3" in json.dumps(r), False)
revisar("el tool_result es chico", len(json.dumps(r)) < 250, True)


# ===========================================================================
# 8) LAS TRES TABLAS DEL HARNESS  —  que no se desincronicen
# ===========================================================================
# ⚠️ TOOLS, FUNCIONES y PERMISOS se editan A MANO y por separado, y tienen que
#    decir lo mismo. El comentario de FUNCIONES lo advierte desde el paso 8
#    ("si se desincronizan, el modelo pide algo que no existe") y NINGÚN eval lo
#    comprobaba: evals_agente.py solo prueba herramientas.py.
#
# ⭐ Es el defecto de MODELO y los precios sueltos de la sesión 16, otra vez:
#    tres cosas que tienen que estar de acuerdo y nada las obliga. Allá se
#    resolvió haciéndolo un dato; aquí, al menos, se comprueba.

print("\n=== las tres tablas del harness ===")

nombres_menu = sorted(t["name"] for t in agente.TOOLS)
revisar("TOOLS == FUNCIONES", nombres_menu, sorted(agente.FUNCIONES))
revisar("TOOLS == PERMISOS", nombres_menu, sorted(agente.PERMISOS))

# Cada permiso tiene que ser un grupo conocido: un typo ("libres") no reventaría,
# caería al camino de preguntar y pediría permiso para algo declarado libre.
grupos = {"libre", "red", "disco"}
revisar("no hay grupos inventados", sorted(set(agente.PERMISOS.values()) - grupos), [])

# Y los grupos que SÍ preguntan necesitan su aviso: sin él, el usuario vería un
# permiso sin saber qué consecuencia está autorizando.
que_preguntan = {g for g in agente.PERMISOS.values() if g != "libre"}
revisar("todo grupo que pregunta tiene aviso", sorted(que_preguntan - set(agente.AVISOS)), [])

# recordar quedó libre a propósito, y es la única que escribe en disco sin
# preguntar. Se fija por escrito para que un cambio accidental salte.
revisar("recordar está en el menú", "recordar" in nombres_menu, True)
revisar("recordar es 'libre'", agente.PERMISOS["recordar"], "libre")
revisar("recordar no pide permiso", agente.pedir_permiso("recordar", {}, set()), (True, "libre"))


# ===========================================================================
# 9) _guardar_texto()  —  el arreglo de las respuestas vacías  (sesión 19)
# ===========================================================================
# 🚨 EL DEFECTO QUE ESTO ARREGLA, MEDIDO: en volumen.py, 3 de 10 respuestas
#    llegaron VACÍAS. El modelo escribía la respuesta completa junto al tool_use
#    de `recordar` y el bucle solo miraba el texto de la ÚLTIMA vuelta.
#
# ⭐ Es la deuda 14 del nivel 5b, que decía "solo se nota cuando una herramienta
#    se niega a mitad". Resultó ser el 30% de las respuestas.

print("\n=== _guardar_texto() (agente.py) ===")

CASOS_TEXTO = [
    # (etiqueta,                    lista de entrada,        nuevo,        resultado)
    ("el primero entra",            [],                      "hola",       ["hola"]),
    ("dos distintos se acumulan",   ["hola"],                 "adiós",     ["hola", "adiós"]),

    # Los tres frenos, y los tres salieron de mirar una corrida de verdad.
    ("lo vacío no entra",           ["hola"],                 "",          ["hola"]),
    ("solo espacios no entra",      ["hola"],                 "   \n ",    ["hola"]),
    ("None no revienta",            ["hola"],                 None,        ["hola"]),

    # ⚠️ El repetido: el modelo suele reescribir lo mismo en la vuelta siguiente.
    #    Verlo dos veces es peor que no verlo.
    ("repetido exacto",             ["hola"],                 "hola",      ["hola"]),
    ("ya está contenido",           ["hola cómo estás"],      "hola",      ["hola cómo estás"]),

    # Y al revés: si lo nuevo CONTIENE lo viejo, gana lo largo. Es el caso de
    # verdad — el modelo empieza "la TRM es" y luego escribe el párrafo entero.
    ("lo largo reemplaza a lo corto", ["hola"],               "hola cómo estás", ["hola cómo estás"]),

    # Los espacios de los bordes se van: entran al join y se ven como líneas sueltas.
    ("recorta los bordes",          [],                       "  hola  ",  ["hola"]),
]

for etiqueta, entrada, nuevo, esperado in CASOS_TEXTO:
    lista = list(entrada)          # copia: un caso no puede ensuciar al siguiente
    try:
        agente._guardar_texto(lista, nuevo)
        obtenido = lista
    except Exception as e:
        obtenido = f"REVENTO: {type(e).__name__}"
    revisar(etiqueta, obtenido, esperado)

# ⭐ EL CASO QUE REPRODUCE EL DEFECTO ENTERO, sin API y sin red:
#    vuelta 1 -> el modelo escribe la respuesta Y pide una herramienta
#    vuelta 2 -> el modelo no dice nada (los 2 tokens de la corrida real)
#    Antes, el usuario recibía "". Ahora recibe la respuesta.
guion = []
agente._guardar_texto(guion, "La serie histórica de la TRM está en datos.gov.co")
agente._guardar_texto(guion, "")          # la vuelta que llegó vacía
revisar("la respuesta NO se pierde", "\n\n".join(guion),
        "La serie histórica de la TRM está en datos.gov.co")


# ===========================================================================
# 10) EL BUCLE ENTERO, CON UN CLIENTE FALSO  —  el rescate del texto
# ===========================================================================
# 🚨 POR QUÉ ESTE BLOQUE EXISTE, Y ES UNA LECCIÓN DE MÉTODO
#
#    El defecto de las respuestas vacías se vio TRES veces en volumen.py. Pero
#    al intentar reproducirlo para comprobar el arreglo, el modelo NO COOPERÓ:
#    dos corridas pagadas ($0,015) y en ninguna llamó a `recordar` en el sitio
#    que hacía falta. El caso no se deja pedir.
#
#    ⭐ LO QUE NO PUEDES PROVOCAR A VOLUNTAD, NO LO PRUEBES PAGANDO: SIMÚLALO.
#
#    Aquí se fabrica a mano la respuesta de la API — la misma sustitución que ya
#    se le hace a `memoria.ARCHIVO` arriba, pero al cliente. Cuesta $0.00, corre
#    en milisegundos, y va a seguir probándolo dentro de seis meses.
#
# ⚠️ Y TRAE SU PROPIA TRAMPA, LA QUINTA DE LA MISMA FAMILIA: ejecutar_agente
#    llama a anotar(), que escribe en el registro DE VERDAD. Sin desviarlo, este
#    eval metería líneas falsas en la evidencia de las corridas pagadas.

print("\n=== el bucle con un cliente falso (agente.py) ===")


class _Texto:
    """Un bloque de texto, como los que manda la API."""
    type = "text"

    def __init__(self, text):
        self.text = text


class _Tool:
    """Un bloque tool_use, como los que manda la API."""
    type = "tool_use"

    def __init__(self, name, entrada, id="falso_1"):
        self.name = name
        self.input = entrada
        self.id = id


class _Usage:
    def __init__(self, entrada=100, salida=50):
        self.input_tokens = entrada
        self.output_tokens = salida


class _Respuesta:
    def __init__(self, content, stop_reason, salida=50):
        self.content = content
        self.stop_reason = stop_reason
        self.usage = _Usage(salida=salida)


class _Cliente:
    """El doble del cliente de Anthropic. Devuelve un GUION, en orden.

    No hay red, no hay llave, no hay dinero. Lo único que le importa a
    ejecutar_agente de un cliente es que .messages.create() devuelva algo con
    .content, .stop_reason y .usage — así que eso es todo lo que tiene.
    """

    def __init__(self, guion):
        self.messages = self
        self.guion = list(guion)
        self.llamadas = 0

    def create(self, **kwargs):
        self.llamadas += 1
        if not self.guion:
            raise AssertionError("el bucle pidió más vueltas de las que tiene el guion")
        return self.guion.pop(0)


def _correr(guion, sembrado=None, max_vueltas=agente.MAX_VUELTAS):
    """Corre ejecutar_agente contra un guion. Devuelve (respuesta, llamadas).

    Guarda y restaura TODO lo que toca: el cliente, el registro y el contador
    de gasto. Un eval que deja el módulo distinto de como lo encontró hace que
    el siguiente pase o falle por la razón equivocada.
    """
    sembrar(sembrado or [])

    cliente_real = agente.cliente
    registro_real = agente.REGISTRO
    gastado_real = agente.gastado_usd

    falso = _Cliente(guion)
    agente.cliente = falso
    agente.REGISTRO = memoria.ARCHIVO.parent / "registro_de_prueba.jsonl"
    agente.gastado_usd = 0.0
    try:
        r = agente.ejecutar_agente("¿pregunta de mentiras?", max_vueltas=max_vueltas)
    finally:
        agente.cliente = cliente_real
        agente.REGISTRO.unlink(missing_ok=True)
        agente.REGISTRO = registro_real
        agente.gastado_usd = gastado_real

    return r, falso.llamadas


# ⭐ EL CASO DEL DEFECTO, RECONSTRUIDO EXACTO. Es lo que pasó tres veces en
#    volumen.py: el modelo contesta Y pide `recordar` en el mismo turno, y la
#    vuelta siguiente viene vacía (los 2 tokens de salida de la corrida real).
RESPUESTA = "La serie histórica de la TRM está en datos.gov.co"

guion_defecto = [
    _Respuesta([_Texto(RESPUESTA),
                _Tool("recordar", {"dato": "estudia economía"})], "tool_use", salida=303),
    _Respuesta([], "end_turn", salida=2),      # la vuelta que llegó vacía
]
r, llamadas = _correr(guion_defecto)
revisar("la respuesta NO llega vacía", r, RESPUESTA)
revisar("fueron 2 vueltas", llamadas, 2)

# Y la herramienta se ejecutó de verdad: el dato quedó guardado. Esto prueba que
# el rescate no rompió el camino normal del bucle.
revisar("y la herramienta sí corrió", textos(), ["estudia economía"])

# --- El caso normal, que NO debe cambiar. Un arreglo que arregla lo roto y
#     rompe lo sano no es un arreglo.
guion_normal = [
    _Respuesta([_Texto("Hoy la TRM es 3.132,42")], "end_turn"),
]
r, llamadas = _correr(guion_normal)
revisar("una vuelta, sin herramientas", r, "Hoy la TRM es 3.132,42")
revisar("no pidió vueltas de más", llamadas, 1)

# --- Texto en las DOS vueltas: se ven los dos, en orden.
guion_dos = [
    _Respuesta([_Texto("Déjame consultar la TRM."),
                _Tool("recordar", {"dato": "es contador"})], "tool_use"),
    _Respuesta([_Texto("Listo: 3.132,42 pesos.")], "end_turn"),
]
r, _ = _correr(guion_dos)
revisar("los dos textos, en orden", r, "Déjame consultar la TRM.\n\nListo: 3.132,42 pesos.")

# --- Y el repetido entre vueltas NO se ve dos veces. El modelo reescribe.
guion_repe = [
    _Respuesta([_Texto("La TRM es 3.132,42"),
                _Tool("recordar", {"dato": "es contador"})], "tool_use"),
    _Respuesta([_Texto("La TRM es 3.132,42")], "end_turn"),
]
r, _ = _correr(guion_repe)
revisar("lo repetido no se duplica", r, "La TRM es 3.132,42")

# --- max_vueltas: lo ya escrito se entrega igual, con el aviso pegado.
#     ⚠️ Cortar por un límite nuestro no es razón para botar lo que el usuario
#        ya pagó. Antes del arreglo, aquí se perdía todo.
guion_infinito = [
    _Respuesta([_Texto("Voy a mirar eso."),
                _Tool("recordar", {"dato": "es contador"})], "tool_use")
    for _ in range(3)
]
r, llamadas = _correr(guion_infinito, max_vueltas=3)
revisar("se acabaron las vueltas: avisa", "se acabaron las vueltas" in r, True)
revisar("...y NO bota lo escrito", "Voy a mirar eso." in r, True)
revisar("respetó max_vueltas", llamadas, 3)


# ===========================================================================
# EL CIERRE: se dispara la trampa y se recoge la basura
# ===========================================================================
memoria.ARCHIVO.unlink(missing_ok=True)      # el archivo de mentiras se va
memoria.ARCHIVO = ARCHIVO_REAL               # se restaura el de verdad

DESPUES_REAL = ARCHIVO_REAL.read_bytes() if ARCHIVO_REAL.exists() else None

print("\n=== la trampa: ¿se tocó la memoria de verdad? ===")
total += 1
if DESPUES_REAL != ANTES_REAL:
    fallos += 1
    print(f"FALLA algún caso escribió en {ARCHIVO_REAL.name} — la memoria real cambió")
else:
    print(f"ok    {ARCHIVO_REAL.name} quedó byte por byte igual")

print(f"\n{total} casos, {fallos} fallaron")
print("TODO BIEN" if fallos == 0 else "HAY FALLOS")
