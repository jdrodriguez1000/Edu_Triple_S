"""pipeline.py — B.1 del nivel 8: la primera topología, la cadena.

    QUÉ ES UN PIPELINE, EN UNA FRASE

Varios agentes en fila, donde la salida de uno es la entrada del siguiente.
El de en medio no puede empezar hasta que el de antes termine.


    LO PRIMERO, PORQUE ES LO QUE MÁS SE CONFUNDE

En el agente del 5b ya había pasos en orden: `tasa` tiene que correr antes que
`convertir`, y la prueba está en la firma de la función —

    def convertir(monto, de, a, tasa):     # herramientas.py:175

la tasa ENTRA como parámetro, no la busca. Eso es una dependencia de verdad.

⚠️ Y AUN ASÍ NO ES UN PIPELINE. Lo encadenado ahí son DOS HERRAMIENTAS dentro
   de una conversación. Un pipeline encadena DOS AGENTES, cada uno con su
   propia conversación.

🔑 LA PREGUNTA DE UNA TOPOLOGÍA NO ES "¿hay pasos en orden?" — eso lo tiene
   casi cualquier agente. ES "¿QUÉ ESTÁ ENCADENADO: HERRAMIENTAS O AGENTES?".

   herramienta → herramienta   el orden lo decide EL MODELO, y viaja un dato
                               exacto dentro de un tool_result
   agente      → agente        el orden lo decide TU CÓDIGO, y viaja lo que el
                               primero ENTENDIÓ, escrito con sus palabras

   La segunda flecha es mucho más cara y mucho más frágil. Eso es B.1.


    Y POR ESO LA TAREA DEL DUELO NO SIRVE AQUÍ

Las tres monedas son independientes: el euro no necesita saber nada del dólar.
Se ve en lo MEDIDO en la sesión 90 — el modelo pidió las TRES `tasa` en un
turno y las TRES `convertir` en el siguiente. Cuatro vueltas, siete llamadas.
Si aquello fuera una cadena de verdad, agruparlas sería imposible.

→ Divisas tiene forma de FAN-OUT (bloque B.2), no de cadena. Lo que hay son
  tres cadenitas de dos pasos corriendo en paralelo, tan cortas que no se notan.

📌 Es el mismo hallazgo de A.4 dicho desde el otro lado: "lo caro no es el
   trabajo, es la DEPENDENCIA entre pasos". Aquí la dependencia mide 2.

⭐ Así que para estudiar el pipeline hay que buscar un trabajo QUE SÍ TENGA
   FORMA DE CADENA. No se fuerza la tarea del duelo a ser lo que no es: se
   busca otro trabajo con las mismas seis herramientas. Es este:

       etapa 1 — RECOLECTOR   (tasa, convertir)     junta las tres cifras
             ↓  su texto
       etapa 2 — REDACTOR     (SIN herramientas)    escribe el informe
             ↓  el borrador  ⟶  🔍 el harness verifica, en Python y gratis
       etapa 3 — ARCHIVISTA   (guardar_reporte)     archiva lo verificado

   El redactor no puede arrancar hasta que el recolector termine, porque su
   materia prima ES el resultado del recolector. No hay forma de agruparlos.


    LO QUE NO TIENE ESTE ARCHIVO, Y ES SU DESCUBRIMIENTO

🚨 NO HAY ORQUESTADOR. Ni uno. Búscalo: no está.

   En A.2 había un agente arriba decidiendo a quién llamar. Aquí el orden es
   FIJO —1, luego 2, luego 3, siempre— y un orden fijo se escribe con tres
   líneas seguidas. Poner un modelo a decidir algo que ya sabes es pagar tokens
   y latencia para meterle dudas a algo que no las tenía.

🔑 UNA TOPOLOGÍA NO NECESITA UN AGENTE QUE LA DIRIJA. Lo necesita cuando el
   camino DEPENDE de lo que se vaya encontrando (eso es el router, B.3, y el
   supervisor, B.4). Si el camino es siempre el mismo, el camino es código.

📌 Dicho al revés, que es como se recuerda: EL MODELO SE PAGA POR DECIDIR. Si
   no hay nada que decidir, no hay nada que pagar.


    LA FRONTERA, QUE ES DONDE ESTÁ EL DAÑO — y aquí está MEDIDO

Entre dos etapas viaja el TEXTO que escribió la anterior, así que se pierde lo
que el anterior no escribió. En A.3 ya se midió una vez: el worker del CAD se
comió `open.er-api.com` al redactar.

⚠️ AQUÍ ESE DEFECTO SE MULTIPLICA, PORQUE HAY DOS FRONTERAS EN FILA. Lo que
   pierde la etapa 1 no lo puede recuperar la 2; lo que pierde la 2 no lo puede
   recuperar la 3. Las pérdidas se ACUMULAN, y ninguna avisa.

🐛 LO QUE PASÓ DE VERDAD EN LA PRIMERA CORRIDA (sesión 92). Sigue un campo:

       harness   "actualizado": "Thu, 20 Aug 2026 00:02:31 +0000"
       etapa 1   "— 20 de agosto de 2026"
       etapa 2   "**Fecha de consulta:** 20 de agosto de 2026"

   La etapa 2 LE PUSO UNA ETIQUETA QUE NADIE LE DIO. `actualizado` es cuándo la
   fuente movió la tasa; "fecha de consulta" es cuándo preguntamos nosotros. Si
   la API llevara tres días sin actualizar, el informe diría "consultado hoy"
   sobre una tasa vieja — y la palabra que delataba la vejez es la que se cayó.

🚨 Y LA PRIMERA VERSIÓN DE ESTE ARCHIVO INTENTÓ ARREGLARLO MAL. Le mandaba al
   archivista los datos verificados y le PEDÍA que comparara. Contestó:

       "coinciden exactamente con los datos verificados"

   ...teniendo `actualizado` en pantalla, al lado del borrador que decía
   "fecha de consulta". Costó +907 tokens (+34% en esa etapa) para no encontrar
   nada, y los dos informes guardados salieron IDÉNTICOS byte a byte.

   🔑 DARLE LA VERDAD AL MODELO Y PEDIRLE QUE COMPARE ES UNA PETICIÓN, NO UN
      ARREGLO. Es la frase de A.3 repetida un día después por quien la escribió.
      **Una comparación es un `if`, no una instrucción en un prompt.**

   → El `if` vive en `verificador.py`, corre SIEMPRE entre la etapa 2 y la 3,
     cuesta $0,00 y no se le puede convencer con buena redacción.


    CÓMO SE CORRE

    python pipeline.py            # la cadena entera + el freno mordiendo, gratis

💰 CUESTA DINERO. Centavos: tres llamadas a agente, una por etapa. La
   verificación no cuesta nada.
"""

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

AQUI = Path(__file__).resolve().parent

sys.path.insert(0, str(AQUI.parent / "05b-proyecto"))

import agente              # noqa: E402
import herramientas        # noqa: E402

import verificador         # noqa: E402
import worker              # noqa: E402


# ---------------------------------------------------------------------------
# 0) HIGIENE DEL INSTRUMENTO — va ANTES que nada, y es la sesión 50 de TEAPP
# ---------------------------------------------------------------------------
# 🚨 `herramientas.CAJA` apunta a `05b-proyecto/caja/`, que es la carpeta del
#    CONTENDIENTE A. Si el pipeline guardara ahí, los reportes del nivel 8 se
#    mezclarían con los de A sin un solo error y sin un solo aviso.
#    Allá el que estaba ensuciando los datos de verdad resultó ser EL
#    INSTRUMENTO DE MEDIDA. Aquí se desvía antes de la primera escritura,
#    igual que en `linea_base.py:70`.
herramientas.CAJA = AQUI / "caja"

MODELO = agente.MODELO

REGISTRO = AQUI / f"registro_pipeline_{MODELO}.jsonl"

# El presupuesto es POR ETAPA, no de la cadena entera. Misma razón que en A.1:
# un tope global se lo come el primero que se descarrile y deja a los de atrás
# sin gasolina por un problema que no era suyo.
PRESUPUESTO_ETAPA_USD = 0.05


def anotar(evento, **datos):
    """El registro de ESTE archivo: la vista por ETAPAS.

    📌 El detalle fino de cada agente (sus vueltas, sus herramientas, sus
       tokens) sigue cayendo en el registro de `worker.py`, porque las etapas
       SON workers. Aquí se anota lo que solo se ve desde arriba: el orden, qué
       cruzó cada frontera, qué encontró el verificador y cuánto tardó la fila.
    """
    linea = {
        "hora": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "evento": evento,
        **datos,
    }
    with open(REGISTRO, "a", encoding="utf-8") as f:
        f.write(json.dumps(linea, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# 1) EL CONTRATO DE LA ETAPA 1 — la verdad, sacada del harness
# ---------------------------------------------------------------------------
# Es `worker.contrato_divisa` estirado a VARIAS monedas. El de A.3 llenaba un
# solo diccionario porque su worker veía una sola moneda; el recolector ve
# tres, así que agrupa por moneda.
#
# ⭐ Y sigue valiendo la regla que lo hizo nacer: NADA DE ESTO SE LE PREGUNTA AL
#    MODELO. `fuente` y `fecha` vienen exactas dentro del `tool_result` de
#    `tasa`. Están en Python. Pedírselas al modelo sería pagar tokens para que
#    nos las repita de memoria y con sus palabras.

def contrato_recoleccion(llamadas):
    """Arma la tabla de la verdad leyendo lo que las herramientas devolvieron.

    Devuelve `(monedas, faltan)`:
      · `monedas` — un diccionario por moneda, con los seis campos de A.3
      · `faltan`  — qué campos quedaron sin llenar, con la moneda delante

    ⭐ Este es el patrón contra el que `verificador.py` compara el borrador. Es
       lo único de toda la corrida que no pasó por la redacción de nadie.
    """
    monedas = {}

    def fila(moneda):
        return monedas.setdefault(
            moneda, {campo: None for campo in worker.CAMPOS_DIVISA})

    for llamada in llamadas:
        salida = llamada["salida"]
        # Una llamada con error no llena nada, y solo se descarta ELLA: el
        # recolector puede fallar el euro y acertar el dólar en la misma
        # corrida, y lo bueno cuenta. (Igual que en A.3.)
        if not isinstance(salida, dict) or "error" in salida:
            continue

        moneda = salida.get("de")
        if not moneda:
            continue

        if llamada["nombre"] == "tasa":
            f = fila(moneda)
            f["moneda"] = moneda
            f["tasa"] = salida.get("tasa")
            f["fuente"] = salida.get("fuente")
            f["fecha"] = salida.get("actualizado")

        elif llamada["nombre"] == "convertir":
            f = fila(moneda)
            f["moneda"] = moneda
            f["monto"] = salida.get("monto")
            f["pesos"] = salida.get("resultado")

    faltan = [f"{m}.{campo}"
              for m, datos in sorted(monedas.items())
              for campo, valor in datos.items() if valor is None]

    return monedas, faltan


def contrato_archivo(llamadas):
    """El contrato de la etapa 3: ¿se guardó de verdad, y con qué nombre?

    ⭐ Fíjate en por qué esto existe en vez de leer la frase final del modelo.
       Un agente puede decir "listo, lo guardé" sin haber llamado a la
       herramienta. Aquí el dato sale del `tool_result` de `guardar_reporte`:
       si no está, es que NO se guardó, diga lo que diga la prosa.
       Es LM.15 otra vez — una afirmación no es una medición.
    """
    datos = {"archivo": None, "caracteres": None}

    for llamada in llamadas:
        if llamada["nombre"] != "guardar_reporte":
            continue
        salida = llamada["salida"]
        if not isinstance(salida, dict) or "error" in salida:
            continue
        datos["archivo"] = salida.get("guardado")
        datos["caracteres"] = salida.get("caracteres")

    faltan = [campo for campo, valor in datos.items() if valor is None]
    return datos, faltan


# ---------------------------------------------------------------------------
# 2) LOS TRES SYSTEM PROMPTS — uno por eslabón
# ---------------------------------------------------------------------------
# 📌 Compáralos entre sí y verás lo que de verdad define a una etapa: no es su
#    inteligencia, es SU SITIO EN LA FILA. Cada uno sabe de dónde le llega el
#    trabajo y a dónde va — y nada más.

SISTEMA_RECOLECTOR = (
    "Eres el PRIMER eslabón de una cadena. Tu trabajo es conseguir los datos, "
    "no presentarlos bonitos: alguien detrás de ti va a redactar el informe. "
    "Averigua a cuántos pesos colombianos equivale cada monto que te pidan. "
    "Nunca inventes ni estimes un número: si no lo tienes, pídelo con una "
    "herramienta. "
    "Para cada moneda di el monto, los pesos, la tasa usada, de qué fuente "
    "salió y de qué fecha es. "
    "No saludes, no ofrezcas ayuda extra y no hagas preguntas: nadie te va a "
    "contestar."
)

# ⚠️ ESTA ETAPA NO LLEVA NINGUNA HERRAMIENTA, Y ES A PROPÓSITO.
#    Si el redactor pudiera llamar a `tasa`, dejaría de ser un eslabón: iría a
#    buscar por su cuenta lo que le faltara, y la cadena se convertiría en tres
#    agentes haciendo cada uno la tarea entera. Es la misma decisión de A.2 —
#    "un orquestador que puede resolver la tarea él solo, la resuelve él solo".
#    🔑 LA CAJA VACÍA ES LO QUE LO OBLIGA A DEPENDER DEL ANTERIOR. Sin ella no
#       hay cadena, hay tres agentes sueltos que resultan correr en orden.
SISTEMA_REDACTOR = (
    "Eres el SEGUNDO eslabón de una cadena. NO tienes herramientas y no puedes "
    "consultar nada: trabajas ÚNICAMENTE con el texto que te entregó el "
    "eslabón anterior. "
    "Escribe un informe breve y claro para un cliente, con las cifras en pesos, "
    "la fuente y la fecha de cada una. "
    "Nunca añadas un número que no esté en el texto que recibiste, ni lo "
    "completes de memoria. Si un dato no está, escribe explícitamente que "
    "falta. "
    "Entrega solo el informe, sin comentarios sobre tu propio trabajo."
)

# 🚨 ESTE PROMPT CAMBIÓ, Y EL CAMBIO ES EL ARREGLO DEL HALLAZGO 1.
#    La versión anterior decía "contrasta el borrador contra la tabla de datos
#    verificados y señala cualquier diferencia". Eso es PEDIRLE AL MODELO QUE
#    VERIFIQUE, y en la corrida medida contestó "coinciden exactamente" cuando
#    no coincidían.
#    Ahora la comparación ya está hecha —en Python, antes de llegar aquí— y a
#    este eslabón se le entrega el VEREDICTO, no la materia prima.
#
# 📌 Y hay que decir lo que eso deja al descubierto: a esta etapa le queda muy
#    poco que decidir. Guardar un texto con un nombre dado es un `write_text`.
#    Es "el modelo se paga por decidir" apuntando a su propio pipeline — y es
#    justo la pregunta que abre el bloque C.
SISTEMA_ARCHIVISTA = (
    "Eres el TERCER y último eslabón de una cadena. Recibes un borrador de "
    "informe, el veredicto de un verificador automático que ya lo revisó, y un "
    "nombre de archivo. "
    "El verificador es la autoridad sobre los datos: no discutas su veredicto "
    "ni lo repitas como tuyo. "
    "Guarda el borrador tal cual con la herramienta `guardar_reporte`, usando "
    "exactamente el nombre que te indiquen. "
    "Después di en una o dos frases qué guardaste y, si el verificador reportó "
    "avisos, cuáles fueron. No saludes ni ofrezcas ayuda extra."
)


# ---------------------------------------------------------------------------
# 3) LAS TRES ETAPAS
# ---------------------------------------------------------------------------
# Cada una es `worker.correr_worker` con otra caja y otro system prompt. Otra
# vez el descubrimiento de A.1: no hay una clase nueva ni un framework.
# 🔑 UN ESLABÓN ES UN WORKER AL QUE LE LLEGA EL TRABAJO DE OTRO WORKER.

def etapa_recolectar(encargo, verboso=True):
    """Etapa 1. Es la única que toca internet."""
    return worker.correr_worker(
        encargo,
        nombre="1-recolector",
        sistema=SISTEMA_RECOLECTOR,
        permitidas=["tasa", "convertir"],
        max_vueltas=8,
        presupuesto_usd=PRESUPUESTO_ETAPA_USD,
        contrato=contrato_recoleccion,
        verboso=verboso,
    )


def etapa_redactar(texto_anterior, verboso=True):
    """Etapa 2. Sin herramientas: solo puede trabajar con lo que le llegó.

    ⭐ MIRA EL ARGUMENTO: `texto_anterior`. Eso ES la frontera, y es literal —
       lo único que cruza es la frase que escribió la etapa 1. Todo lo que la
       etapa 1 supo y no escribió, aquí ya no existe.
    """
    encargo = (
        "El eslabón anterior te entregó esto:\n\n"
        f"{texto_anterior}\n\n"
        "Redacta el informe para el cliente."
    )
    return worker.correr_worker(
        encargo,
        nombre="2-redactor",
        sistema=SISTEMA_REDACTOR,
        permitidas=[],            # <- la caja vacía. Ver el comentario de arriba.
        max_vueltas=2,
        presupuesto_usd=PRESUPUESTO_ETAPA_USD,
        contrato=None,            # sin herramientas no hay nada que contratar
        verboso=verboso,
    )


def etapa_archivar(borrador, nombre_archivo, hallazgos=None, verboso=True):
    """Etapa 3. Archiva un borrador QUE YA VIENE VERIFICADO.

    `hallazgos` es lo que devolvió `verificador.verificar()`. Fíjate en lo que
    NO es: no son los datos crudos del harness.

    🐛 La versión anterior recibía `verdad=<el contrato entero>` y le pedía al
       modelo que comparara. Medido: +907 tokens de entrada, +34% de coste en
       esta etapa, y un "coinciden exactamente" que era falso.

    ⭐ Ahora sube el VEREDICTO, no la materia prima. Casi siempre son cero
       líneas o dos, contra 907 tokens fijos hiciera falta o no. Salió más
       barato Y más correcto — que no es lo normal, y por eso conviene entender
       por qué: el trabajo se movió al sitio donde era determinista.
    """
    partes = [
        "Borrador a archivar:\n\n",
        borrador,
        "\n\n---\n",
        verificador.como_texto(hallazgos or []),
        f"\n\nGuárdalo con el nombre exacto: {nombre_archivo}",
    ]

    return worker.correr_worker(
        "".join(partes),
        nombre="3-archivista",
        sistema=SISTEMA_ARCHIVISTA,
        permitidas=["guardar_reporte"],
        max_vueltas=4,
        presupuesto_usd=PRESUPUESTO_ETAPA_USD,
        contrato=contrato_archivo,
        verboso=verboso,
    )


# ---------------------------------------------------------------------------
# 4) LA CADENA — y es tan corta que da vergüenza, que es exactamente el punto
# ---------------------------------------------------------------------------

def correr_pipeline(encargo, nombre_archivo="informe-pipeline.txt",
                    verboso=True):
    """Corre las tres etapas en fila y devuelve lo que pasó en cada una.

    🚨 ESTO ES EL PIPELINE ENTERO. Tres llamadas, una debajo de otra, con una
       comprobación de Python en medio. No hay framework, no hay grafo, no hay
       orquestador. LA TOPOLOGÍA ES EL ORDEN EN QUE ESTÁN ESCRITAS ESTAS LÍNEAS.

    ⏱️ Y fíjate en lo que NO se puede hacer aquí: no hay forma de adelantar la
       etapa 2 mientras corre la 1, porque la 2 recibe el resultado de la 1. El
       tiempo total es la SUMA, siempre. En un fan-out (B.2) sería el MÁXIMO.
       🔑 Esa es la diferencia entre las dos topologías, y no es de estilo: es
          aritmética.
    """
    arranque = time.monotonic()
    anotar("pipeline_inicio", encargo=encargo, archivo_pedido=nombre_archivo)

    # --- ESLABÓN 1 ---------------------------------------------------------
    if verboso:
        print("\n" + "─" * 70)
        print("ETAPA 1 · RECOLECTOR   (tasa, convertir)")
        print("─" * 70)

    r1 = etapa_recolectar(encargo, verboso=verboso)
    verdad = r1["datos"] or {}

    anotar("frontera", de="1-recolector", a="2-redactor", cruza="texto",
           caracteres=len(r1["texto"] or ""))

    # 🚨 UN ESLABÓN CAÍDO PARA LA CADENA, y esto es propio del pipeline. En un
    #    fan-out, si falla una moneda quedan dos; aquí, si falla el primero, el
    #    segundo no tiene con qué trabajar y el tercero archivaría humo.
    #    → Se corta, y el fracaso se devuelve COMO DATO, no como excepción.
    if not r1["ok"]:
        return _cerrar(arranque, encargo, nombre_archivo,
                       r1, None, None, [], corto_en="1-recolector")

    # --- ESLABÓN 2 ---------------------------------------------------------
    if verboso:
        print("\n" + "─" * 70)
        print("ETAPA 2 · REDACTOR     (sin herramientas)")
        print("─" * 70)

    r2 = etapa_redactar(r1["texto"], verboso=verboso)

    anotar("frontera", de="2-redactor", a="3-archivista", cruza="texto",
           caracteres=len(r2["texto"] or ""))

    if not r2["ok"]:
        return _cerrar(arranque, encargo, nombre_archivo,
                       r1, r2, None, [], corto_en="2-redactor")

    # --- LA VERIFICACIÓN ---------------------------------------------------
    # 🚨 VA AQUÍ, SIEMPRE, Y NO ES OPCIONAL. Es la lección de la sesión 83 de
    #    TEAPP: una cerradura que hay que acordarse de invocar sigue siendo una
    #    advertencia. No hay parámetro para saltársela.
    #
    # ⭐ Y cuesta $0,00. Es Python leyendo dos cosas que ya están en memoria.
    hallazgos = verificador.verificar(r2["texto"], verdad)
    anotar("verificacion", hallazgos=hallazgos,
           bloqueado=verificador.hay_bloqueante(hallazgos))

    if verboso:
        print("\n" + "─" * 70)
        print("🔍 EL HARNESS VERIFICA   (Python, sin modelo, $0,00)")
        print("─" * 70)
        print(verificador.como_texto(hallazgos))

    # 🚨 EL FRENO. Un informe con un número que ninguna herramienta devolvió NO
    #    SE ARCHIVA. Y para eso el archivista ni se enciende: gastar una llamada
    #    para guardar algo que sabemos que está mal es pagar por empeorar.
    if verificador.hay_bloqueante(hallazgos):
        if verboso:
            print("\n🛑 La cadena se corta aquí: hay cifras sin respaldo.")
            print("   No se llama a la etapa 3 — archivar esto sería el daño.")
        return _cerrar(arranque, encargo, nombre_archivo,
                       r1, r2, None, hallazgos, corto_en="verificacion")

    # --- ESLABÓN 3 ---------------------------------------------------------
    if verboso:
        print("\n" + "─" * 70)
        print("ETAPA 3 · ARCHIVISTA   (guardar_reporte)")
        print("─" * 70)

    r3 = etapa_archivar(r2["texto"], nombre_archivo, hallazgos=hallazgos,
                        verboso=verboso)

    return _cerrar(arranque, encargo, nombre_archivo,
                   r1, r2, r3, hallazgos, corto_en=None)


def _cerrar(arranque, encargo, nombre_archivo, r1, r2, r3, hallazgos, corto_en):
    """Un solo sitio donde se arma la salida — también cuando la cadena se cortó.

    La misma razón de siempre (A.1): un resultado de error con otra forma
    obliga al que llama a tratarlo aparte, y ahí es donde se olvida tratarlo.
    """
    etapas = [r for r in (r1, r2, r3) if r is not None]

    resultado = {
        "encargo": encargo,
        "archivo_pedido": nombre_archivo,
        "ok": corto_en is None and all(r["ok"] for r in etapas),
        "corto_en": corto_en,
        "hallazgos": hallazgos,
        "etapas": [
            {
                "worker": r["worker"],
                "ok": r["ok"],
                "vueltas": r["vueltas"],
                "segundos": r["segundos"],
                "coste_usd": r["coste_usd"],
                "entrada_tokens": r["entrada_tokens"],
                "salida_tokens": r["salida_tokens"],
                "herramientas": r["herramientas"],
                "caracteres_salida": len(r["texto"] or ""),
            }
            for r in etapas
        ],
        "borrador": (r2["texto"] if r2 else None),
        "texto_final": (r3 or r2 or r1)["texto"],
        "verdad": (r1["datos"] if r1 else None),
        "archivo": ((r3["datos"] or {}).get("archivo") if r3 else None),
        "coste_total_usd": round(sum(r["coste_usd"] for r in etapas), 6),
        "entrada_total": sum(r["entrada_tokens"] for r in etapas),
        "salida_total": sum(r["salida_tokens"] for r in etapas),
        "segundos": round(time.monotonic() - arranque, 2),
    }

    anotar("pipeline_fin", **{k: v for k, v in resultado.items()
                              if k not in ("texto_final", "borrador", "verdad")})
    return resultado


# ---------------------------------------------------------------------------
# 5) LA DEMO
# ---------------------------------------------------------------------------

ENCARGO = (
    "Tengo 1.000 dólares, 1.000 euros y 1.000 dólares canadienses. "
    "Averigua a cuántos pesos colombianos equivale cada uno."
)

if __name__ == "__main__":
    print("=" * 70)
    print("B.1 — PIPELINE. Tres agentes en fila: la salida de uno es la")
    print("      entrada del siguiente. Y NO HAY ORQUESTADOR.")
    print("=" * 70)
    print("⚠️  Es una DEMO del bloque B, no el duelo. El duelo se corre en F.3.")

    r = correr_pipeline(ENCARGO, nombre_archivo="informe-pipeline.txt")

    # --- LA FACTURA --------------------------------------------------------
    print("\n" + "=" * 70)
    print("LA FACTURA, ESLABÓN POR ESLABÓN")
    print("=" * 70)
    for e in r["etapas"]:
        print(f"  {e['worker']:>14}  {e['vueltas']} vueltas · "
              f"{e['segundos']:>6}s · ${e['coste_usd']:.6f} · "
              f"{e['entrada_tokens']:>6} ent / {e['salida_tokens']:>5} sal · "
              f"[{', '.join(e['herramientas']) or 'sin herramientas'}]")
    print(f"  {'verificador':>14}  —          0.00s · $0.000000 · "
          f"{'0':>6} ent / {'0':>5} sal · [Python]")
    print("  " + "─" * 66)
    print(f"  {'TOTAL':>14}  {r['segundos']:>16}s · ${r['coste_total_usd']:.6f} · "
          f"{r['entrada_total']:>6} ent / {r['salida_total']:>5} sal")

    print("\n⏱️  El tiempo total es la SUMA de las tres etapas, no el máximo.")
    print("    En un pipeline eso no es un defecto que se pueda optimizar: es")
    print("    la definición. Y el paralelismo que SÍ hay vive DENTRO de un")
    print("    eslabón —la etapa 1 pide sus tres `tasa` en un turno—, nunca")
    print("    ENTRE eslabones.")
    print("\n📌 NO se compara este total con el de A.3: aquel no redactaba")
    print("   informe ni guardaba archivo. Serían dos trabajos distintos, y")
    print("   además la sesión 90 midió ±12% de ruido en tiempo (LM.16).")

    # --- VER EL FRENO MORDER, Y NO CUESTA NADA ------------------------------
    # 🚨 LM.13: un freno que no has visto morder es una nota, no un freno.
    #    Se le cambia UN dígito al borrador real y se vuelve a verificar. Sin
    #    modelo, sin red, sin un centavo. Si esto no se pusiera rojo, todo lo
    #    de arriba sería decoración.
    print("\n" + "=" * 70)
    print("EL FRENO, MORDIENDO — se le cambia un dígito al borrador. $0,00.")
    print("=" * 70)

    verdad = r["verdad"] or {}
    primera = next(iter(verdad.values()), None)
    if r["borrador"] and primera and primera.get("pesos") is not None:
        real = f"{primera['pesos']:,}".replace(",", ".")
        falso = real[:-1] + ("0" if real[-1] != "0" else "1")
        adulterado = r["borrador"].replace(real, falso)

        if adulterado == r["borrador"]:
            print(f"  ⚠️ No se pudo adulterar: «{real}» no aparece literal en")
            print("     el borrador. El freno queda SIN demostrar en esta")
            print("     corrida — y eso se dice, no se calla.")
        else:
            print(f"  Se cambió «{real}» por «{falso}» y nada más.\n")
            print(verificador.como_texto(
                verificador.verificar(adulterado, verdad)))
            print("\n  🔑 Eso es lo que el modelo NO vio teniendo la verdad")
            print("     delante. Una comparación es un `if`.")

    print("\n" + "=" * 70)
    print("RESPUESTA FINAL (la del último eslabón)")
    print("=" * 70)
    print(r["texto_final"])

    print(f"\n📄 archivo: {r['archivo']}")
    print(f"📄 registros: {REGISTRO.name}  +  {worker.REGISTRO.name}")
