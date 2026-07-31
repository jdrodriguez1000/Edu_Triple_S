"""agente.py — el bucle agéntico del nivel 5b.

Aquí es donde Claude por fin entra al proyecto. Las seis herramientas de
`herramientas.py` ya funcionaban (116 casos, 0 fallos), pero solo TÚ podías
llamarlas: para el modelo no existían.

Del PASO 7 salieron las tres partes que lo hacen funcionar:
  1. TOOLS      -> el menú: presentarle las seis herramientas al modelo.
  2. FUNCIONES  -> el puente: del nombre que dice el modelo a la función real.
  3. ejecutar_agente() -> el bucle. Es el MISMO del nivel 3, con seis
     herramientas en vez de una.

Del PASO 8 salieron los NUEVE FRENOS, y vienen de dos sitios distintos.

Seis son los del nivel 4, y te protegen DEL MUNDO y DE TU CUENTA DE COBRO:
  1. timeout + reintentos  -> que un problema ajeno no cuelgue tu programa
  2. errores tipados       -> reintentar lo temporal, cortar lo permanente
  3. presupuesto en USD    -> que un bucle no te vacíe la cuenta
  4. tope de vueltas       -> que un bucle no sea infinito
  5. permisos              -> que el modelo no decida solo lo irreversible
  6. registro JSONL        -> poder explicar después qué fue lo que pasó

Tres son nuevos de este nivel, y te protegen DEL MODELO:
  7. ¿existe la herramienta?   -> un nombre inventado ya no tumba el bucle
  8. ¿acepta esos argumentos?  -> trm(dias=1) ya no tumba el bucle
  9. la red final              -> un defecto nuestro se ve, pero no mata la corrida

⭐ Los tres últimos NO estaban en el nivel 4, y no fue un olvido: allá el
   agente tenía UNA herramienta. Que el modelo inventara un nombre era casi
   imposible. Con seis, apareció una superficie de error que antes no existía.
   → Más herramientas no es solo más capacidad: es más formas de equivocarse.

Correr con:  python agente.py
   ⚠️ Es INTERACTIVO: te va a pedir permiso antes de usar la red y antes de
      escribir en el disco. Responde s, t o n.

⚠️ Este es el primer archivo del nivel que CUESTA DINERO. `evals.py` corre
   116 casos por $0.00 porque nunca llama al modelo. Aquí cada vuelta se paga.
"""

import json
import random
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

import anthropic
from dotenv import load_dotenv

import herramientas

# La consola de Windows imprime en cp1252 y revienta con tildes. Sin esta
# línea el agente CORRE BIEN y falla al final, al imprimir: no falló el
# agente, falló la pantalla. (Lección del nivel 3.)
sys.stdout.reconfigure(encoding="utf-8")

AQUI = Path(__file__).resolve().parent
load_dotenv(AQUI.parent / ".env")

# ---------------------------------------------------------------------------
# LA CONFIGURACIÓN DEL HARNESS
# ---------------------------------------------------------------------------
# Todo número que gobierna el comportamiento vive aquí arriba, con nombre.
# Un límite escondido a la mitad del archivo es un límite que nadie ajusta.
# (Misma idea del nivel 4.)

# --- EL CATÁLOGO DE MODELOS ------------------------------------------------
# ⭐ POR QUÉ ESTO ES UNA TABLA Y NO TRES NÚMEROS SUELTOS:
#    Antes había MODELO por un lado y PRECIO_ENTRADA / PRECIO_SALIDA por otro.
#    Tres cosas que TENÍAN que estar de acuerdo entre sí, y nada las obligaba.
#    El día que cambiaras el modelo y olvidaras los precios, el programa NO
#    fallaba: imprimía un costo falso, calculado con precios de un modelo sobre
#    tokens de otro. Y te lo creías, porque el `usage` sí venía bueno.
#    → Es el número creíble otra vez, y aquí duele más que en ningún lado:
#      todo el paso 9 consiste en comparar costos. Si el costo miente, no hay
#      experimento.
#    Ahora el precio NO es algo que tú recuerdas: es algo que el programa
#    DEDUCE del modelo. Cambias una línea y lo demás se acomoda solo.
#    (Es la misma idea del `motivo` de trm_en_fecha: lo que tiene que ser
#     consistente no se deja en la memoria, se vuelve un dato.)
#
# Precios en dólares por MILLÓN de tokens. Verificados el 2026-07-30.
CATALOGO = {
    "claude-opus-5":    {"entrada": 5.00, "salida": 25.00, "contexto": 1_000_000},
    "claude-sonnet-5":  {"entrada": 3.00, "salida": 15.00, "contexto": 1_000_000},
    "claude-haiku-4-5": {"entrada": 1.00, "salida":  5.00, "contexto":   200_000},
}
# ⚠️ OJO CON SONNET, Y ANÓTALO: hasta el 2026-08-31 su precio real de
#    lanzamiento es 2.00 / 10.00, no 3.00 / 15.00. Aquí quedó el precio de
#    después, a propósito: prefieres que el programa reporte de MÁS y no de
#    menos. Un costo inflado te asusta y lo revisas; uno desinflado te
#    tranquiliza y no lo revisas nunca.
#    → Es un número que era verdad cuando lo escribiste y deja de serlo sin
#      avisarte. La diferencia es que este trae la fecha de vencimiento puesta.
#
# ⚠️ Y una diferencia que no es de precio: haiku tiene 200.000 tokens de
#    contexto, no un millón. A este agente le sobra (la corrida más cara fueron
#    26.000 de entrada), pero el día que un tool_result se dispare —como la
#    inyección de la sesión 13, con sus 31.000 tokens— haiku es el que se
#    queda sin aire primero.

# ⭐ ESTA ES LA ÚNICA LÍNEA QUE CAMBIAS PARA CORRER CON OTRO MODELO.
MODELO = "claude-haiku-4-5"

# --- Freno 10: ¿ese modelo existe en el catálogo? --------------------------
# Un nombre mal escrito ("claude-haiku-45") reventaría más adelante con un
# KeyError feo, o peor: llegaría hasta la API para que te conteste un 404
# después de armar la petición. Que muera aquí, antes de gastar un centavo,
# y diciéndote cuáles sí valen.
# Misma familia que los frenos 7 y 8: no confíes en un nombre solo porque
# alguien lo escribió.
if MODELO not in CATALOGO:
    raise SystemExit(
        f"\n❌ MODELO = {MODELO!r} no está en el catálogo.\n"
        f"   Los que hay son: {', '.join(CATALOGO)}\n"
    )

# Cuántas vueltas puede dar el bucle antes de que lo cortemos.
# En el nivel 3 bastaban 5 porque una pregunta eran 2 vueltas. Aquí las
# preguntas se ENCADENAN: "¿cuántos dólares son 500 mil pesos?" necesita
# trm -> convertir -> responder. Son 3 vueltas para una sola pregunta, y 4
# si además pide guardar el reporte.
MAX_VUELTAS = 8

# --- Freno 1: timeout y reintentos -----------------------------------------
# ⚠️ Hasta el paso 8 esto no estaba: el cliente se creaba con
#    anthropic.Anthropic() a secas, o sea con los valores por defecto del SDK.
#    Y eso NO es lo mismo que no tener frenos — es tener frenos que no
#    escogiste. El SDK reintenta 2 veces y espera 10 minutos por defecto.
#    Diez minutos es una eternidad mirando una pantalla quieta.
TIMEOUT_SEGUNDOS = 30.0     # por INTENTO, no por llamada entera
REINTENTOS_SDK = 0          # apagados a propósito: el nuestro está más abajo
REINTENTOS_PROPIOS = 3      # el nuestro sí ANOTA cada intento en el registro

# --- Freno 3: el presupuesto -----------------------------------------------
# ⭐ EL NÚMERO NO SE COPIÓ DEL NIVEL 4, SE RECALCULÓ. Y menos mal:
#    allá era PRESUPUESTO_USD = 0.10, y la primera corrida de este agente
#    (7 vueltas, 23.710 de entrada, 887 de salida) costó $0.1407.
#    El presupuesto del nivel 4, copiado tal cual, habría cortado esta corrida
#    a mitad de la tercera pregunta — y habrías pasado media hora buscando el
#    "error" en el bucle.
#    → Un límite heredado sin recalcular no es un freno: es una trampa.
#
# ⚠️ Y ojo con POR QUÉ este agente cuesta tanto más que el del nivel 4:
#    allá el menú era de 3 herramientas; aquí son 6 y pesan 3.447 tokens que
#    se repagan EN CADA VUELTA. La entrada de ayer fue 27 veces la salida.
#    Un agente no paga por lo que dice: paga por lo que RELEE.
PRESUPUESTO_USD = 0.40      # para TODA la corrida, no por pregunta

# Los precios YA NO SE ESCRIBEN AQUÍ: se sacan del catálogo, con el nombre del
# modelo como llave. No hay nada que recordar y no hay nada que pueda quedar
# desacompasado.
PRECIO_ENTRADA = CATALOGO[MODELO]["entrada"]
PRECIO_SALIDA = CATALOGO[MODELO]["salida"]

# --- Freno 6: el registro ---------------------------------------------------
# ⭐ EL NOMBRE DEL ARCHIVO TAMBIÉN SALE DEL MODELO, y por la misma razón:
#    el archivo se abre en modo "añadir". Si las dos corridas escribieran en el
#    mismo `registro.jsonl`, las líneas de haiku caerían DEBAJO de las de opus
#    sin decir nada —sin error, sin aviso— y terminarías con un archivo
#    revuelto que parece una sola corrida. Renombrarlo a mano entre corridas
#    funciona... hasta el día que se te olvide.
#    Así, ninguna corrida puede pisar a otra ni aunque quieras.
#
# ⚠️ `registro.jsonl` (el viejo, sin nombre de modelo) NO SE TOCA: es la
#    corrida real de la sesión 15, y su línea 13 es la evidencia del defecto
#    de los permisos. Está citada en PROGRESO.md con ese nombre.
REGISTRO = AQUI / f"registro_{MODELO}.jsonl"

cliente = anthropic.Anthropic(
    timeout=TIMEOUT_SEGUNDOS,
    max_retries=REINTENTOS_SDK,
)

# Se va sumando en cada llamada. Es la única variable global del archivo, y es
# global porque el gasto es de la CORRIDA entera, no de una pregunta.
gastado_usd = 0.0


class PresupuestoAgotado(Exception):
    """No es un error de la API: es una decisión NUESTRA.

    Por eso es una clase propia y no un ValueError cualquiera. Cuando el bucle
    la atrape, sabe que no falló nada — que nosotros dijimos "hasta aquí".
    """

# ---------------------------------------------------------------------------
# EL SYSTEM PROMPT
# ---------------------------------------------------------------------------
# ⚠️ Esto también se manda en CADA vuelta, igual que el menú. Por eso es corto:
#    lo que se puede decir en la descripción de UNA herramienta va allá, no
#    aquí. Aquí solo van las reglas que valen para todas.
SISTEMA = (
    "Eres un asistente de tasas de cambio para Colombia. "
    "Nunca inventes un número: si no tienes el dato, pídelo con una herramienta. "
    "Di siempre de dónde salió cada cifra (TRM oficial o mercado) y de qué fecha es. "
    "Si una herramienta te devuelve un 'error', léelo, explícaselo al usuario en "
    "palabras normales y, si tiene arreglo, vuelve a intentarlo corregido. "
    "Responde en español y en pocas frases."
)

# ---------------------------------------------------------------------------
# 1) EL MENÚ: las 6 herramientas, descritas para el modelo
# ---------------------------------------------------------------------------
# ⚠️ Esta lista se manda ENTERA en cada vuelta de cada conversación, se llame
#    o no una herramienta. Es un impuesto permanente.
#
#    MEDIDO EXACTO con count_tokens(tools=TOOLS), que es GRATIS: 3.049 tokens.
#
#    Y los dos estimados previos se quedaron cortos, en el mismo sentido:
#      "700-900 tokens"       -> a ojo, mal.
#      6.231 caracteres / 4   -> ~1.557, la mitad de lo real.
#    La regla de "4 caracteres por token" viene del inglés en prosa; JSON en
#    español tokeniza mucho peor (llaves, comillas, tildes).
#    → REGLA: el único contador que vale es el de la API. Y es gratis, así que
#      no hay excusa para estimar.
#
#    Para comparar: el resumen de historial() ahorra 143 tokens por vuelta.
#    El menú cuesta VEINTE veces más que aquella decisión, que costó media
#    sesión analizar. El método de aquel análisis sigue siendo el bueno; lo que
#    dice este número es DÓNDE está el dinero de verdad.
#
# Cada entrada tiene tres partes y nada más:
#   name         -> idéntico al nombre de la función en herramientas.py
#   description  -> PARA QUÉ sirve y CUÁNDO usarla. Es lo único que el modelo
#                   lee para decidir. Es la parte que importa.
#   input_schema -> la forma exacta de los argumentos. Los nombres tienen que
#                   coincidir con los del `def`.
#
# ⚠️ NO van aquí: es_numero, es_texto, es_moneda, pedir_json y explicar_sin_trm.
#    Son ayudantes internos nuestros; el modelo nunca los llama. Y cada línea
#    de más en esta lista se paga en cada vuelta.

TOOLS = [

    # -----------------------------------------------------------------------
    # 1. convertir — la única que no toca nada del mundo
    # -----------------------------------------------------------------------
    {
        "name": "convertir",
        "description": (
            "Convierte un monto de una moneda a otra usando una tasa que TÚ le das. "
            "Esta herramienta NO busca la tasa: hace solo la multiplicación. "
            "Si todavía no tienes la tasa, consíguela primero con 'tasa' (mercado) "
            "o con 'trm' (oficial de Colombia), y después llama a esta. "
            "PROHIBIDO calcular la tasa tú mismo. Esta herramienta multiplica el monto por "
            "la tasa, así que la tasa tiene que ir en el sentido de la conversión: cuántas "
            "unidades de 'a' vale UNA unidad de 'de'. "
            "Si la que tienes va al revés, NO la inviertas dividiendo 1 entre ella: pide el "
            "número en el sentido que necesitas. Para pesos a dólares con la tasa oficial, "
            "'trm' ya te lo da hecho en la llave 'usd_por_1_cop'; para el mercado, llama a "
            "'tasa' con 'de' y 'a' en el orden que necesitas. "
            "Una tasa calculada por ti no salió de ninguna fuente, y si te equivocas nadie se "
            "entera: llegaría aquí como una tasa perfectamente válida y el resultado se vería "
            "igual de creíble. "
            "Redondea el resultado según la moneda: los pesos colombianos no llevan "
            "centavos, el dólar y el euro sí."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "monto": {
                    "type": "number",
                    "description": "Cuánto convertir. No puede ser negativo. El cero sí se acepta.",
                },
                "de": {
                    "type": "string",
                    "enum": ["COP", "USD", "EUR", "CAD"],
                    "description": "Moneda de origen.",
                },
                "a": {
                    "type": "string",
                    "enum": ["COP", "USD", "EUR", "CAD"],
                    "description": "Moneda de destino.",
                },
                "tasa": {
                    "type": "number",
                    "description": (
                        "Cuántas unidades de la moneda 'a' vale UNA unidad de la moneda 'de'. "
                        "Tiene que ser mayor que cero. No lo inventes: sácalo de 'tasa' o de 'trm'."
                    ),
                },
            },
            "required": ["monto", "de", "a", "tasa"],
        },
    },

    # -----------------------------------------------------------------------
    # 2. trm — el dólar oficial de HOY
    # -----------------------------------------------------------------------
    # La frontera con trm_en_fecha es la más delicada de las seis, y por eso
    # las dos descripciones se nombran mutuamente.
    {
        "name": "trm",
        "description": (
            "La TRM oficial de Colombia (fuente: datos.gov.co) del día más reciente publicado. "
            "Úsala cuando el usuario pregunte por el dólar HOY, o por la tasa oficial, "
            "o para convertir pesos colombianos ahora mismo. "
            "No necesitas saber qué día es: esta herramienta siempre trae el dato más nuevo. "
            "Para un día del PASADO usa 'trm_en_fecha', no esta. "
            "Devuelve el valor y las fechas 'vigente_desde' y 'vigente_hasta'. "
            "Devuelve la tasa en LOS DOS SENTIDOS: 'trm' son los pesos que vale un dólar, y "
            "'usd_por_1_cop' son los dólares que vale un peso. Para pasar pesos a dólares usa "
            "ese segundo número tal cual: no lo calcules tú dividiendo. "
            "IMPORTANTE: los fines de semana y festivos no se publica TRM nueva, así que "
            "la del viernes sigue vigente sábado y domingo. Si las fechas que te devuelve "
            "no corresponden a hoy, díselo al usuario en tu respuesta. "
            "La TRM es la tasa OFICIAL (para impuestos y contabilidad) y NO es igual a la "
            "tasa de mercado que devuelve la herramienta 'tasa': son números distintos."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },

    # -----------------------------------------------------------------------
    # 3. tasa — el mercado, y cualquier par de monedas
    # -----------------------------------------------------------------------
    {
        "name": "tasa",
        "description": (
            "Tasa de cambio de MERCADO entre dos monedas cualesquiera (fuente: open.er-api.com). "
            "Úsala para pares que no involucran a Colombia (por ejemplo EUR a USD), o cuando "
            "pregunten a cuánto se está negociando el dólar, no cuánto marca la tasa oficial. "
            "Devuelve la tasa junto con la fecha en que la fuente la actualizó. "
            "Devuelve TAMBIÉN la tasa en el sentido contrario, en una llave que se llama "
            "sola: para tasa(de='COP', a='USD') viene 'cop_por_1_usd'. NUNCA inviertas una "
            "tasa dividiendo tú: el número contrario ya viene, tómalo de ahí. "
            "IMPORTANTE: para pesos colombianos existen DOS números distintos y no son "
            "intercambiables. El de mercado lo da esta herramienta; el oficial lo da 'trm'. "
            "El 30 de julio de 2026 fueron 3207,64 y 3206,18. Di siempre cuál de los dos usaste."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "de": {
                    "type": "string",
                    "enum": ["COP", "USD", "EUR", "CAD"],
                    "description": "Moneda de origen.",
                },
                "a": {
                    "type": "string",
                    "enum": ["COP", "USD", "EUR", "CAD"],
                    "description": "Moneda de destino.",
                },
            },
            "required": ["de", "a"],
        },
    },

    # -----------------------------------------------------------------------
    # 4. historial — la tendencia, NO el día puntual
    # -----------------------------------------------------------------------
    # ⚠️ La advertencia de "registros, no días" es obligatoria: sin ella el
    #    modelo dice "en los últimos 30 días" y miente con total confianza.
    #    Medido el 2026-07-30: 30 registros = 48 días de calendario.
    {
        "name": "historial",
        "description": (
            "Cómo se ha movido la TRM oficial en los últimos registros: devuelve un RESUMEN "
            "(máximo, mínimo, promedio, primero, último y el cambio porcentual), no la lista "
            "día por día. Úsala para preguntas de TENDENCIA: si el dólar subió o bajó, cómo "
            "viene la semana, cuánto se movió el mes. "
            "NO sirve para un día puntual del pasado: para eso está 'trm_en_fecha'. "
            "IMPORTANTE Y FÁCIL DE EQUIVOCAR: el parámetro 'dias' cuenta REGISTROS, no días de "
            "calendario. La fuente publica un registro por VIGENCIA, y la TRM del viernes cubre "
            "también sábado y domingo, así que un fin de semana entero es UN solo registro. "
            "Pedir 30 registros trae aproximadamente 48 días de calendario. "
            "Por eso NUNCA digas 'en los últimos 30 días': usa las fechas 'desde' y 'hasta' que "
            "te devuelve la herramienta, que sí son exactas. "
            "Si la respuesta trae la llave 'descartados', significa que ese número de registros "
            "venía ilegible y no entró en las cuentas; vale la pena mencionarlo."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "dias": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 400,
                    "description": (
                        "Cuántos REGISTROS traer (no días de calendario). Entre 1 y 400. "
                        "Para 'la última semana' pide unos 5; para 'el último mes', unos 20."
                    ),
                },
            },
            "required": ["dias"],
        },
    },

    # -----------------------------------------------------------------------
    # 5. trm_en_fecha — un día concreto del pasado
    # -----------------------------------------------------------------------
    # El modelo NO tiene reloj. Si usa esta para "hoy" o "ayer" va a partir de
    # una fecha imaginada y va a entregar un número real de un día equivocado.
    # Por eso la descripción se lo prohíbe con todas las letras.
    {
        "name": "trm_en_fecha",
        "description": (
            "La TRM oficial de Colombia de UN día concreto del pasado (fuente: datos.gov.co). "
            "Úsala cuando el usuario nombre una fecha: 'cuánto valió el dólar el 15 de julio'. "
            "NO la uses para hoy ni para ayer: tú no sabes qué día es hoy, pondrías una fecha "
            "imaginada y devolverías un número real del día equivocado. Para hoy usa 'trm'. "
            "Funciona también con domingos y festivos: devuelve la vigencia que cubre ese día, "
            "y las fechas 'vigente_desde' y 'vigente_hasta' te dicen de qué día salió el dato. "
            "Si no hay TRM para esa fecha, la respuesta trae un 'motivo' que explica por qué: "
            "'futura' (esa fecha todavía no llega), 'muy_antigua' (anterior al 2 de diciembre "
            "de 1991, cuando empieza la serie oficial), 'hueco' (la fuente no la cubre) o "
            "'desconocido'. Usa ese motivo para explicarle al usuario qué pasó, en vez de "
            "decirle solo que no encontraste el dato."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "fecha": {
                    "type": "string",
                    "description": (
                        "El día que se quiere consultar, en formato AAAA-MM-DD y con los ceros "
                        "a la izquierda. Ejemplo: \"2026-07-15\". "
                        "No se aceptan otros formatos como \"15 de julio\" ni \"15/07/2026\"."
                    ),
                },
            },
            "required": ["fecha"],
        },
    },

    # -----------------------------------------------------------------------
    # 6. guardar_reporte — LA ÚNICA QUE DEJA HUELLA
    # -----------------------------------------------------------------------
    # Las otras cinco leen. Ésta escribe un archivo en el disco, y después de
    # correr el mundo quedó distinto. Es la candidata natural a pedir permiso
    # en el harness (paso 8).
    {
        "name": "guardar_reporte",
        "description": (
            "Guarda un texto en un archivo dentro de la carpeta caja/. "
            "Es la ÚNICA herramienta que deja algo escrito en el disco: las otras cinco solo "
            "leen. Úsala solo cuando el usuario pida explícitamente guardar, exportar o dejar "
            "un reporte. No la uses por iniciativa propia para archivar lo que acabas de "
            "calcular: si el usuario no lo pidió, no lo guardes. "
            "Si ya existe un archivo con ese nombre, se sobrescribe sin avisar, así que conviene "
            "usar nombres descriptivos con la fecha adentro. "
            "Devuelve el nombre guardado y cuántos caracteres se escribieron."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "nombre": {
                    "type": "string",
                    "description": (
                        "Nombre del archivo. Tiene que terminar en .txt y solo puede llevar "
                        "letras, números, guiones (- _) y el punto de la extensión. "
                        "Sin espacios, sin tildes, sin barras ni carpetas. "
                        "Ejemplo: \"trm-2026-07-30.txt\"."
                    ),
                },
                "contenido": {
                    "type": "string",
                    "description": (
                        "El texto completo del reporte, ya redactado. Un texto vacío se acepta."
                    ),
                },
            },
            "required": ["nombre", "contenido"],
        },
    },

]


# ---------------------------------------------------------------------------
# 2) EL PUENTE: del nombre que dice el modelo, a la función real de Python
# ---------------------------------------------------------------------------
# El modelo solo devuelve un TEXTO: "trm". Este diccionario es lo que convierte
# ese texto en la función que hay que correr. Sin él, "trm" es una palabra sin
# dueño.
#
# En el nivel 3 tenía UNA entrada. Es la única pieza del archivo que crece con
# el número de herramientas.
#
# ⚠️ Las llaves de aquí tienen que ser IDÉNTICAS a los "name" del menú de
#    arriba. Si se desincronizan, el modelo pide algo que no existe.
FUNCIONES = {
    "convertir":       herramientas.convertir,
    "trm":             herramientas.trm,
    "tasa":            herramientas.tasa,
    "historial":       herramientas.historial,
    "trm_en_fecha":    herramientas.trm_en_fecha,
    "guardar_reporte": herramientas.guardar_reporte,
}


# ---------------------------------------------------------------------------
# 3) LOS PERMISOS  (paso 8)
# ---------------------------------------------------------------------------
# Tus seis herramientas NO son iguales, y hasta ahora el harness las trataba
# igual. Caen en tres grupos, no en dos:
#
#   convertir                          -> no toca nada del mundo. Es aritmética.
#   tasa, trm, historial, trm_en_fecha -> leen un servidor AJENO. Cuesta tiempo
#                                         y molesta a un tercero, pero no rompe.
#   guardar_reporte                    -> ESCRIBE EN EL DISCO. Después de
#                                         correr, el mundo quedó distinto.
#
# ⭐ La pregunta no es "¿lee o escribe?". Es: SI ESTO SALE MAL, ¿LO PUEDO
#    DESHACER? Una consulta de más se olvida; un archivo sobrescrito, no.
#
# ⚠️ Y el detalle que conecta esto con todo lo que has medido en el nivel:
#    ESTA TABLA NO LE CUESTA UN SOLO TOKEN AL MODELO. Vive en Python y él nunca
#    la ve. Si en vez de esto le explicáramos los permisos en las descripciones,
#    se pagaría en CADA vuelta de CADA conversación.
#    → Lo que puede vivir en el harness, que viva en el harness: ahí es gratis
#      y allá es impuesto permanente.
PERMISOS = {
    "convertir":       "libre",
    "tasa":            "red",
    "trm":             "red",
    "historial":       "red",
    "trm_en_fecha":    "red",
    "guardar_reporte": "disco",
}

# Qué se le dice al usuario según el grupo. Se explica LA CONSECUENCIA, no la
# categoría: "red" no le dice nada a nadie.
AVISOS = {
    "red":   "va a consultar un servidor de internet (cuesta tiempo, no rompe nada)",
    "disco": "VA A ESCRIBIR UN ARCHIVO EN TU DISCO. Si ya existe, lo sobrescribe.",
}


# La memoria de los "sí, toda la corrida". Vive FUERA de ejecutar_agente() a
# propósito: "toda la corrida" son las tres preguntas, no cada pregunta. Si
# viviera adentro, se te preguntaría otra vez en cada pregunta nueva — y un
# permiso que se pregunta demasiado deja de leerse: el usuario dice "sí" sin
# mirar, que es peor que no preguntar.
AUTORIZADAS = set()


def pedir_permiso(nombre, argumentos, autorizadas):
    """Le pregunta al usuario si deja correr esta herramienta.

    Devuelve DOS cosas: si se puede o no, y el MOTIVO.

    ⚠️ Al principio devolvía solo True o False, y la primera corrida (sesión 15)
       destapó por qué no alcanza. En el registro quedó escrito
       `"herramienta": "convertir", "concedido": true` — y a ti NUNCA te
       preguntaron por convertir: es "libre", así que la función devolvía True
       sin abrir la boca. El registro afirmaba un permiso que no existió.

       Un solo True estaba tapando TRES situaciones distintas:
         - el usuario miró la pantalla y dijo que sí
         - estaba autorizada de antes con la tecla 't'
         - nunca se pregunta, es libre

       Y eso rompe justo aquello para lo que existe el registro: el día que un
       agente escriba un archivo que no debía, vas a leer "permiso concedido" y
       vas a creer que lo autorizaste tú.

    ⭐ La solución no es nueva: es TU decisión de trm_en_fecha. Allá cero filas
       tapaba tres situaciones y las separaste con un `motivo` que es un DATO
       estable ("futura", "muy_antigua", "hueco"), no una frase. Aquí igual.
       → El motivo se puede filtrar, contar y comparar; una frase, no.
    """
    # Lo que no está en la tabla se trata como lo más peligroso. Es a propósito:
    # el día que agregues una herramienta y se te olvide clasificarla, el
    # programa pregunta de más. Olvidarse tiene que salir seguro, no barato.
    grupo = PERMISOS.get(nombre, "disco")

    if grupo == "libre":
        return True, "libre"

    # Ya dijiste "para toda la corrida" a ESTA herramienta.
    if nombre in autorizadas:
        return True, "autorizada_antes"

    print(f"\n  🔐 El modelo quiere usar: {nombre}({json.dumps(argumentos, ensure_ascii=False)})")
    print(f"     {AVISOS[grupo]}")

    # ⚠️ El bucle es obligatorio. Sin él, una tecla mal puesta decide por ti, y
    #    la que decidiría es la respuesta por defecto. Un permiso que se puede
    #    conceder por accidente no es un permiso.
    while True:
        respuesta = input("     [s] sí, esta vez  ·  [t] sí, toda la corrida  ·  [n] no > ")
        opcion = respuesta.strip().lower()

        if opcion == "s":
            return True, "usuario_dijo_si"
        if opcion == "t":
            # Por HERRAMIENTA, no para todas. Autorizar 'trm' no autoriza
            # 'guardar_reporte': son riesgos distintos y se dicen por separado.
            autorizadas.add(nombre)
            return True, "usuario_dijo_toda_la_corrida"
        if opcion == "n":
            return False, "usuario_dijo_no"
        print("     No entendí. Escribe s, t o n.")


# ---------------------------------------------------------------------------
# 4) EL REGISTRO  (freno 6)
# ---------------------------------------------------------------------------
# Una línea de JSON por evento. El formato .jsonl se lee con los ojos, se
# puede abrir a mitad de escritura, y se procesa línea por línea sin cargar el
# archivo entero.
#
# ⭐ POR QUÉ ESTE FRENO ES DISTINTO DE LOS OTROS OCHO: los demás EVITAN que
#    algo malo pase. Éste no evita nada — sirve DESPUÉS, cuando ya pasó.
#
#    Y tú ya tienes la prueba de que hace falta. Los dos hallazgos de ayer —el
#    modelo dividiendo a escondidas, y los 335 tokens de salida que lo
#    delataron— los viste porque estabas mirando la pantalla en ese instante.
#    Si hubieras cerrado la terminal, se perdían. El registro los guarda solo.
#    → Sin esto, cuando el agente haga algo raro solo tienes tu memoria.
def anotar(evento, **datos):
    linea = {
        "hora": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "evento": evento,
        **datos,
    }
    with open(REGISTRO, "a", encoding="utf-8") as f:
        f.write(json.dumps(linea, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# 5) LA LLAMADA AL MODELO  (frenos 1, 2 y 3 en un solo sitio)
# ---------------------------------------------------------------------------
# Todo lo que tiene que ver con hablarle a la API vive aquí: revisar el
# presupuesto, medir el gasto, reintentar lo que se puede reintentar y cortar
# lo que no. El bucle de abajo queda limpio: pide y recibe.

# ⚠️ ESTA TUPLA ES EL FRENO 2, Y ES UNA DECISIÓN, NO UNA LISTA.
#    La tabla del nivel 4 (§4.1) dice cuál va aquí y cuál no:
#      RateLimitError (429)     -> vas muy rápido. Esperar SÍ arregla.
#      InternalServerError (5xx)-> el servidor tropezó. Esperar SÍ arregla.
#      APIConnectionError       -> no hubo red. Esperar SÍ arregla.
#    Lo que NO está aquí (400, 401, 403, 404) no se reintenta jamás: una clave
#    mala sigue mala dentro de diez segundos. Reintentar un error permanente es
#    esperar tres veces para recibir el mismo "no" — y pagarlo.
REINTENTABLES = (
    anthropic.RateLimitError,
    anthropic.InternalServerError,
    anthropic.APIConnectionError,
)


def costo(usage):
    """Cuánto costó UNA llamada, en dólares."""
    return (usage.input_tokens * PRECIO_ENTRADA
            + usage.output_tokens * PRECIO_SALIDA) / 1_000_000


def llamar_modelo(mensajes):
    """Le habla a la API con los tres frenos puestos."""
    global gastado_usd

    # ⭐ EL PRESUPUESTO SE REVISA ANTES DE GASTAR. Revisarlo después es contar
    #    el dinero que ya no tienes.
    if gastado_usd >= PRESUPUESTO_USD:
        raise PresupuestoAgotado(f"llevas ${gastado_usd:.4f} de ${PRESUPUESTO_USD:.2f}")

    for intento in range(1, REINTENTOS_PROPIOS + 1):
        try:
            inicio = time.monotonic()
            respuesta = cliente.messages.create(
                model=MODELO,
                max_tokens=2048,
                system=SISTEMA,
                tools=TOOLS,
                messages=mensajes,
            )
            demora = time.monotonic() - inicio

            este_costo = costo(respuesta.usage)
            gastado_usd += este_costo
            anotar(
                "llamada_api",
                intento=intento,
                segundos=round(demora, 2),
                entrada=respuesta.usage.input_tokens,
                salida=respuesta.usage.output_tokens,
                costo_usd=round(este_costo, 6),
                acumulado_usd=round(gastado_usd, 6),
                stop_reason=respuesta.stop_reason,
            )
            return respuesta

        except REINTENTABLES as fallo:
            anotar("error_temporal", intento=intento, tipo=type(fallo).__name__)
            if intento == REINTENTOS_PROPIOS:
                raise      # se acabaron los intentos: que se vea
            # Espera que se DUPLICA (2s, 4s, 8s) más un pellizco al azar.
            # Se duplica porque si el servidor está ahogado, insistir cada
            # segundo lo ahoga más. El pellizco al azar existe para que mil
            # programas que fallaron al tiempo no vuelvan todos juntos.
            espera = 2.0 * (2 ** (intento - 1)) + random.uniform(0, 1)
            print(f"     la red o el servidor falló ({type(fallo).__name__}), "
                  f"reintento en {espera:.1f}s")
            time.sleep(espera)

        except anthropic.APIStatusError as fallo:
            # 400, 401, 403, 404... esperar no arregla nada. Se corta ya.
            anotar("error_permanente", tipo=type(fallo).__name__,
                   codigo=fallo.status_code)
            raise


# ---------------------------------------------------------------------------
# 6) EL BUCLE AGÉNTICO
# ---------------------------------------------------------------------------

def ejecutar_agente(pregunta, max_vueltas=MAX_VUELTAS, autorizadas=AUTORIZADAS,
                    preguntar=pedir_permiso):
    """El bucle. Es el mismo del nivel 3, con seis herramientas en vez de una.

    Mandar mensaje -> mirar stop_reason -> si dice "tool_use", ejecutar la
    herramienta y devolver el tool_result -> repetir.

    ⭐ EL PARÁMETRO `preguntar` LLEGÓ EN EL PASO 10, Y ES UNA LÍNEA QUE ENSEÑA.

       Hasta ayer este bucle tenía clavado CÓMO se pide un permiso: llamaba a
       pedir_permiso(), que imprime en pantalla y espera un input(). Eso está
       bien cuando hay una persona sentada — y deja de estarlo en el momento en
       que quieres correr 10 preguntas seguidas para medir algo.

       Ahora el bucle ya no sabe cómo se pregunta: recibe A QUIÉN preguntarle.
       Por defecto sigue siendo pedir_permiso, así que nada cambia para quien
       corre el agente a mano. El examinador le pasa otro que responde solo,
       según lo que diga la pregunta del examen.

    ⚠️ Y esto paga una deuda vieja de gratis: `evals.py` no tenía un solo caso
       para los permisos porque exigían un humano tecleando. Ahora se pueden
       probar sin red, sin modelo y sin persona, como los otros 116.
       → Lo que recibes desde afuera se puede probar; lo que está clavado
         adentro, no.
    """
    anotar("pregunta", texto=pregunta)
    historial = [{"role": "user", "content": pregunta}]

    for vuelta in range(1, max_vueltas + 1):
        # El presupuesto puede acabarse a mitad de una pregunta. Cuando eso
        # pasa NO se revienta: se devuelve una respuesta honesta y el programa
        # sigue vivo. Que se acabe la plata es una decisión nuestra, no un
        # defecto — por eso tiene clase propia y se atrapa aquí.
        try:
            respuesta = llamar_modelo(historial)
        except PresupuestoAgotado as fallo:
            anotar("detenido", motivo="presupuesto", detalle=str(fallo))
            return f"(me detuve: se acabó el presupuesto — {fallo})"

        # Se imprime el usage en cada vuelta a propósito: aquí se ve crecer la
        # entrada vuelta tras vuelta. Es la lección del nivel 2 (todo lo que
        # pasa se reenvía) ahora con el menú y los tool_result adentro.
        # Y desde el paso 8 se imprime también el gasto ACUMULADO: el número
        # que hasta ayer este agente no mostraba por ningún lado.
        print(f"  [vuelta {vuelta}] stop_reason={respuesta.stop_reason} "
              f"entrada={respuesta.usage.input_tokens} "
              f"salida={respuesta.usage.output_tokens} "
              f"gastado=${gastado_usd:.4f}")

        # -- CASO A: el modelo terminó. Salimos del bucle.
        if respuesta.stop_reason != "tool_use":
            final = next((b.text for b in respuesta.content if b.type == "text"), "")
            anotar("respuesta", vueltas=vuelta, texto=final)
            return final

        # -- CASO B: el modelo pidió una o más herramientas.

        # B.1 Guardar la petición del modelo TAL CUAL vino. Se guarda
        #     respuesta.content entero, no solo el texto: si le quitas los
        #     bloques tool_use, la API rechaza el siguiente mensaje.
        historial.append({"role": "assistant", "content": respuesta.content})

        # B.2 Ejecutar cada herramienta pedida. Pueden ser varias en un turno.
        resultados = []
        for bloque in respuesta.content:
            if bloque.type != "tool_use":
                continue

            # ===============================================================
            # LA RED DE SEGURIDAD DEL HARNESS (paso 8)
            # ===============================================================
            # Dentro de cada herramienta ya hay frenos: convertir rechaza
            # montos negativos, historial rechaza el 3.5, trm_en_fecha exige
            # AAAA-MM-DD. Ninguna de las seis lanza excepciones.
            #
            # ⭐ Pero todo ese cuidado protege el INTERIOR de las funciones.
            #    Aquí se protege el CAMINO hacia ellas. Una función a prueba de
            #    balas no sirve de nada si el modelo no logra entrar por la
            #    puerta — y hasta ayer estas dos líneas eran la puerta abierta.

            # --- 1) EL PERMISO. Va ANTES de todo lo demás, y es a propósito:
            #        preguntar después de haber escrito el archivo no es
            #        preguntar, es avisar.
            #        Se llama a `preguntar`, no a pedir_permiso: es el que
            #        llegó por parámetro. Por defecto son el mismo.
            permitida, motivo = preguntar(bloque.name, bloque.input, autorizadas)
            if not permitida:
                # ⚠️ NEGAR NO ES FALLAR. El usuario no se equivocó: decidió.
                #    Por eso esto NO corta el bucle — si cortara, se perderían
                #    las vueltas que ya pagaste por un "no" a la última. El
                #    modelo recibe la negativa como información y puede
                #    terminar bien: darte la respuesta y decirte que no la
                #    guardó.
                resultados.append({
                    "type": "tool_result",
                    "tool_use_id": bloque.id,
                    "content": json.dumps({
                        "error": "El usuario NO autorizó esta herramienta. No la vuelvas "
                                 "a pedir. Responde con lo que ya tengas y dile qué no "
                                 "pudiste hacer."
                    }, ensure_ascii=False),
                })
                print("        🚫 permiso NEGADO por el usuario")
                anotar("permiso", herramienta=bloque.name, concedido=False,
                       motivo=motivo, entrada=bloque.input)
                continue

            # ⚠️ `motivo` va SIEMPRE, también cuando se concede. Sin él, el
            #    registro dice "concedido" de una herramienta que nunca se
            #    preguntó — que es exactamente el defecto que destapó la
            #    primera corrida del paso 8.
            anotar("permiso", herramienta=bloque.name, concedido=True,
                   motivo=motivo, entrada=bloque.input)

            # --- 2) ¿EXISTE LA HERRAMIENTA?
            #        Antes esto era FUNCIONES[bloque.name], y un nombre
            #        inventado reventaba con KeyError y tumbaba el bucle entero.
            #
            # ⭐ AQUÍ APARECIÓ UNA CATEGORÍA NUEVA DE ERROR. En la sesión 12
            #    había dos, y por eso pedir_json no tiene `except Exception`:
            #      - falla el MUNDO (no hay red, 503) -> información, se cuenta
            #      - falla NUESTRO CÓDIGO (un typo)   -> defecto, tiene que doler
            #    Un nombre inventado no es ninguna de las dos: falla EL MODELO.
            #    Y es la única de las tres que se arregla sola, porque el modelo
            #    lee el error y reintenta. El mundo no se arregla porque le
            #    insistas; nuestro código, tampoco.
            #    → Por eso este error VUELVE AL MODELO en vez de reventar.
            #
            # .get() en vez de [ ] no es un detalle de estilo: es lo que separa
            # "no existe esa llave" de un KeyError que venga de ADENTRO de una
            # función. Si envolviéramos las dos cosas en el mismo try, un
            # defecto nuestro se disfrazaría de error del modelo.
            funcion = FUNCIONES.get(bloque.name)
            if funcion is None:
                salida = {
                    "error": f"No existe ninguna herramienta llamada '{bloque.name}'. "
                             f"Las que tienes son: {', '.join(FUNCIONES)}. "
                             f"Vuelve a intentarlo con una de esas."
                }
                print(f"     -> ❌ herramienta inexistente: {bloque.name}")

            else:
                # --- 3) LA LLAMADA. Aquí corre TU código.
                try:
                    salida = funcion(**bloque.input)

                except TypeError as fallo:
                    # Argumentos que la función no acepta: trm(dias=1), el
                    # error que corregiste tú en la sesión 12. Python rechaza
                    # la llamada ANTES de entrar, así que los frenos de la
                    # función ni se enteran. También es error del modelo.
                    #
                    # ⚠️ HONESTIDAD SOBRE ESTE `except`: un TypeError también
                    #    puede nacer DENTRO de la función, y entonces sería un
                    #    defecto nuestro disfrazado de error del modelo. Por eso
                    #    igual se imprime el traceback: si aparece uno y los
                    #    argumentos se ven bien, el culpable somos nosotros.
                    #    Distinguirlos de verdad exige mirar la firma de la
                    #    función, y eso es de más adelante.
                    traceback.print_exc()
                    salida = {
                        "error": f"Llamaste a '{bloque.name}' con argumentos que no acepta "
                                 f"({fallo}). Revisa los nombres exactos de los parámetros "
                                 f"en la lista de herramientas y vuelve a intentarlo."
                    }

                except Exception:
                    # Cualquier otra cosa es un DEFECTO NUESTRO. Y aquí se hacen
                    # las dos cosas a la vez, que es el punto del paso:
                    #   - a nosotros: el traceback completo, con la línea exacta.
                    #     Un defecto tapado vive para siempre disfrazado de
                    #     "problemas de conexión" (lección de la sesión 12).
                    #   - al modelo: un aviso honesto de que no es culpa suya,
                    #     para que no se ponga a reintentar lo mismo diez veces.
                    # Y el bucle NO se cae: las otras herramientas siguen vivas.
                    traceback.print_exc()
                    salida = {
                        "error": "Esa herramienta falló por un defecto interno del programa. "
                                 "No es culpa de tu petición: llamarla otra vez igual no va a "
                                 "servir. Sigue con lo que puedas o dile al usuario que esto "
                                 "no está disponible."
                    }

                print(f"     -> {bloque.name}({json.dumps(bloque.input, ensure_ascii=False)})")

            print(f"        devolvió: {salida}")
            anotar("herramienta", nombre=bloque.name, entrada=bloque.input,
                   salida=salida)

            resultados.append({
                "type": "tool_result",
                "tool_use_id": bloque.id,     # el ticket: hay que citarlo exacto
                # ⚠️ LO ÚNICO DE VERDAD NUEVO FRENTE AL NIVEL 3:
                # allá obtener_clima devolvía TEXTO. Estas seis devuelven
                # DICCIONARIOS, y el content de un tool_result tiene que ser
                # texto. json.dumps hace la traducción.
                # ensure_ascii=False no es cosmético: sin él "día" viaja como
                # "día" — más caracteres, más tokens, y para nada.
                "content": json.dumps(salida, ensure_ascii=False),
            })

        # B.3 Devolver los resultados. Van con role "user" aunque no los
        #     escribieras tú: para la API, todo lo que ENTRA al modelo es
        #     "user". Y todos los resultados van en UN solo mensaje.
        historial.append({"role": "user", "content": resultados})

    anotar("detenido", motivo="max_vueltas", vueltas=max_vueltas)
    return "(se acabaron las vueltas: el agente no llegó a una respuesta final)"


# ---------------------------------------------------------------------------
# La corrida
# ---------------------------------------------------------------------------
# Tres preguntas escogidas para que se vean tres formas distintas del bucle:
#   1. una sola herramienta       -> 2 vueltas
#   2. dos herramientas en cadena -> 3 vueltas
#   3. una pregunta de tendencia  -> 2 vueltas, pero con el resumen adentro
PREGUNTAS = [
    "¿A cómo está el dólar oficial hoy?",
    "¿Cuántos dólares son 500 mil pesos colombianos?",
    "¿El dólar subió o bajó el último mes?",
]

if __name__ == "__main__":
    # ⭐ Los precios quedan ESCRITOS en el registro, no solo usados.
    #    El día que compares dos archivos, la primera línea de cada uno te dice
    #    con qué números se calculó ese costo. Un registro que guarda el
    #    resultado pero no de dónde salió te obliga a confiar en tu memoria —
    #    y esa es justo la parte que falla.
    anotar("inicio", modelo=MODELO, presupuesto_usd=PRESUPUESTO_USD,
           precio_entrada=PRECIO_ENTRADA, precio_salida=PRECIO_SALIDA,
           max_vueltas=MAX_VUELTAS, timeout=TIMEOUT_SEGUNDOS,
           herramientas=list(FUNCIONES))

    for pregunta in PREGUNTAS:
        print(f"\n=== {pregunta}")
        print(f"RESPUESTA: {ejecutar_agente(pregunta)}")

    anotar("fin", gastado_usd=round(gastado_usd, 6))

    # ⚠️ Hasta el paso 8 este agente no decía en ningún lado lo que costaba.
    #    Corrías, veías las respuestas, y el precio lo sabías después mirando
    #    la consola de Anthropic. Un agente que no te dice lo que gasta te
    #    obliga a confiar — y confiar es justo lo que el nivel entero enseña
    #    a no hacer.
    print(f"\n{'=' * 60}")
    print(f"Gasto total de la corrida: ${gastado_usd:.4f} de ${PRESUPUESTO_USD:.2f}")
    print(f"Todo quedó anotado en: {REGISTRO.name}")
    print("Ábrelo: cada llamada con su costo, cada permiso, cada herramienta.")
