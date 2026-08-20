"""verificador.py — el arreglo del hallazgo 1 de B.1, y no lleva ni un token.

    QUÉ PASÓ, Y POR QUÉ ESTE ARCHIVO EXISTE

En la primera corrida del pipeline (sesión 92) la etapa 3 recibió, además del
borrador, LOS DATOS VERIFICADOS del harness. Y contestó:

    "coinciden exactamente con los datos verificados"

🐛 NO COINCIDÍAN. El harness había devuelto

        "actualizado": "Thu, 20 Aug 2026 00:02:31 +0000"

    y el informe decía **"Fecha de consulta: 20 de agosto de 2026"**.
    `actualizado` es CUÁNDO LA FUENTE MOVIÓ LA TASA. "Fecha de consulta" es
    cuándo preguntamos nosotros. No son lo mismo: si la API llevara tres días
    sin actualizar, el informe diría "consultado hoy" sobre una tasa vieja, y
    la única palabra que delataba la vejez es justo la que se perdió.

    El dato estaba EN PANTALLA, al lado del borrador. Y firmó que cuadraba.

🔑 EL DIAGNÓSTICO, Y ES DE LA CASA: darle la verdad al modelo y PEDIRLE que
   compare es una PETICIÓN, no un arreglo. Es la frase de A.3 —"un arreglo que
   necesita que el modelo se porte bien no es un arreglo"— repetida un día
   después por quien la había escrito.

⭐ UNA COMPARACIÓN ES UN `if`, NO UNA INSTRUCCIÓN EN UN PROMPT.
   Este archivo es ese `if`. Cuesta $0,00, tarda milisegundos, y no se le puede
   convencer con buena redacción.

📌 Y de paso sale más barato: en la corrida medida, mandarle la verdad cruda al
   modelo costó +907 tokens de entrada (+$0,002122, un 34% más en esa etapa)
   PARA NO ENCONTRAR NADA. Aquí sube un resumen de lo que de verdad falla, que
   casi siempre es mucho más corto que los datos completos.


    EL PATRÓN YA ESTABA EN CASA, DOS VECES

  · `T-071` (sesión 49): el portero sobre `data/` entera, no sobre los archivos
    que alguien recuerde pasarle.
  · `sentences_are_invented()` (sesión 83): la cerradura que dejó de ser un
    comentario… y siguió dependiendo de que alguien se acordara de llamarla.

⚠️ La lección de la 83 se aplica AQUÍ MISMO: esta función no sirve de nada si
   hay que acordarse de invocarla. Por eso `pipeline.py` la llama SIEMPRE,
   entre la etapa 2 y la etapa 3, y no como un extra opcional.


    QUÉ COMPRUEBA, Y QUÉ NO — dicho antes de que alguien lo suponga

  1. CIFRAS INVENTADAS. Todo número del borrador tiene que poder rastrearse
     hasta un número que devolvió una herramienta. Este es el que importa.
     → bloqueante: un informe con un número que nadie midió no se archiva.

  2. CIFRAS PERDIDAS. Los pesos de cada moneda tienen que aparecer.
     → aviso.

  3. FUENTE PERDIDA. Las palabras que distinguen la fuente tienen que
     sobrevivir. En este proyecto "mercado" pesa: la sesión 90 midió que TRM
     oficial y mercado dan números distintos para "el dólar de hoy".
     → aviso.

  4. FECHA REETIQUETADA. El caso concreto que se midió arriba.
     → aviso.

🚨 LO QUE **NO** COMPRUEBA, Y HAY QUE DECIRLO O ESTO SE VUELVE LM.15:
   · El punto 4 es UNA BÚSQUEDA DE PALABRAS. Caza "fecha de consulta" porque es
     lo que apareció; NO caza una paráfrasis ("al día de hoy", "verificado el").
     Es un freno estrecho y honesto, no un detector de mentiras.
   · No juzga si el informe está bien escrito ni si es útil. Solo si sus
     números y sus etiquetas se sostienen contra lo que midió el harness.
   · Un número que coincide por casualidad con otro de la verdad pasa. Con
     tolerancia de redondeo, eso es inevitable y se acepta a sabiendas.


    CÓMO SE CORRE

    python verificador.py     # sus propias pruebas, SIN llamar al modelo, $0,00
"""

import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")


# ---------------------------------------------------------------------------
# 1) LEER NÚMEROS DE UN TEXTO ESCRITO POR UN HUMANO (o por un modelo)
# ---------------------------------------------------------------------------
# El informe escribe "3.099.309" y "3.610,38"; el harness devolvió 3099309 y
# 3610.3799525653394. Comparar los textos tal cual no serviría de nada: hay que
# convertir los dos lados a números y comparar números.

_TOKEN_NUMERICO = re.compile(r"\d[\d.,]*")


def a_numero(token):
    """Convierte un número escrito en formato colombiano a `float`.

    En es-CO el punto separa miles y la coma es el decimal — al revés que en
    inglés. Los casos que hay que resolver bien:

        "3.099.309"  -> 3099309.0      (puntos de miles)
        "3.610,38"   -> 3610.38        (punto de miles + coma decimal)
        "1.000"      -> 1000.0         (un solo punto, grupo de 3)
        "2026"       -> 2026.0
        "0,5"        -> 0.5

    Devuelve `None` si no se puede leer, y ese `None` NO se trata como un cero:
    un número ilegible se ignora, no se inventa.
    """
    token = token.strip(".,")
    if not token:
        return None

    hay_punto = "." in token
    hay_coma = "," in token

    if hay_punto and hay_coma:
        # El separador decimal es el que aparece de último.
        if token.rfind(",") > token.rfind("."):
            token = token.replace(".", "").replace(",", ".")
        else:
            token = token.replace(",", "")
    elif hay_coma:
        # Coma sola: en es-CO es decimal.
        token = token.replace(",", ".", 1).replace(",", "")
    elif hay_punto:
        # Punto solo: es de miles SI todos los grupos de después son de 3
        # dígitos. "3.099.309" sí; "3.14" no.
        partes = token.split(".")
        if len(partes) > 1 and all(len(p) == 3 for p in partes[1:]):
            token = "".join(partes)

    try:
        return float(token)
    except ValueError:
        return None


def numeros_de_texto(texto):
    """Todos los números que aparecen en un texto, como `float`."""
    encontrados = []
    for token in _TOKEN_NUMERICO.findall(texto or ""):
        valor = a_numero(token)
        if valor is not None:
            encontrados.append((token, valor))
    return encontrados


def numeros_de_verdad(verdad):
    """Todos los números que el HARNESS puede respaldar.

    ⭐ Recorre también los campos de TEXTO, y esa línea no es un detalle: la
       fecha `"Thu, 20 Aug 2026 00:02:31 +0000"` respalda el 20 y el 2026 que
       el informe escribe. Sin esto, el año saldría marcado como inventado en
       cada corrida y el freno se volvería ruido — que es la forma más rápida
       de que alguien lo apague.
    """
    respaldados = set()

    def recorrer(valor):
        if isinstance(valor, dict):
            for v in valor.values():
                recorrer(v)
        elif isinstance(valor, (list, tuple)):
            for v in valor:
                recorrer(v)
        elif isinstance(valor, bool):
            pass                      # un bool es un int en Python; aquí no cuenta
        elif isinstance(valor, (int, float)):
            respaldados.add(float(valor))
        elif isinstance(valor, str):
            for _, numero in numeros_de_texto(valor):
                respaldados.add(numero)

    recorrer(verdad)
    return respaldados


# El informe redondea a propósito: 3610.3799525653394 se escribe "3.610,38".
# Eso NO es inventar. Un número del borrador se da por respaldado si coincide
# con algún número de la verdad redondeado a cualquier cantidad de decimales
# entre 0 y 6.
#
# ⚠️ Y aquí está el precio de esta decisión, dicho entero: cuanto más ancha la
#    tolerancia, más fácil es que un número inventado se cuele por parecerse a
#    otro. Se para en 6 decimales y en redondeo EXACTO — no hay margen
#    porcentual. Un "casi igual" no se acepta.
_DECIMALES_TOLERADOS = range(0, 7)


def esta_respaldado(numero, respaldados):
    """¿Este número del borrador sale de algún dato del harness?"""
    if numero in respaldados:
        return True
    for verdadero in respaldados:
        for decimales in _DECIMALES_TOLERADOS:
            if round(verdadero, decimales) == numero:
                return True
    return False


# ---------------------------------------------------------------------------
# 2) LAS CUATRO COMPROBACIONES
# ---------------------------------------------------------------------------

# Etiquetas que afirman algo que el harness NUNCA dijo. El campo que devuelve
# `tasa` se llama `actualizado`: es cuándo la FUENTE movió el número, no cuándo
# lo miramos nosotros.
#
# 🚨 Esto es una búsqueda de palabras, con todo lo estrecho que suena. Está
#    escrito en la cabecera del archivo para que nadie lo lea como más de lo
#    que es. Caza el caso medido; no caza una paráfrasis.
_ETIQUETAS_DE_CONSULTA = [
    "fecha de consulta",
    "fecha de la consulta",
    "consultado el",
    "fecha de descarga",
]


def verificar(borrador, verdad):
    """Compara un borrador contra lo que devolvieron las herramientas.

    Devuelve una lista de hallazgos. Cada uno trae:

        tipo    — qué clase de problema es
        nivel   — "bloqueante" o "aviso"
        detalle — la frase que se le puede enseñar a un humano

    📌 El reparto bloqueante/aviso es el mismo criterio del CLAUDE.md: un
       informe con un número que nadie midió NO se archiva, punto. Lo demás se
       reporta y sigue, porque parar el trabajo por una etiqueta imprecisa
       cuesta más de lo que ahorra.

    Lista vacía = no encontró nada. ⚠️ Eso NO es "el informe está bien": es
    "estas cuatro comprobaciones pasaron". La diferencia entre las dos frases es
    `LM.15`, y es la que se cobra sola.
    """
    hallazgos = []
    borrador = borrador or ""
    minusculas = borrador.lower()
    respaldados = numeros_de_verdad(verdad)

    # --- 1. CIFRAS INVENTADAS ------------------------------------------------
    # El único bloqueante. Un número que no sale de ninguna herramienta se lo
    # inventó alguien por el camino, y un informe así no se archiva.
    sin_respaldo = []
    vistos = set()
    for token, numero in numeros_de_texto(borrador):
        if numero in vistos:
            continue
        if not esta_respaldado(numero, respaldados):
            vistos.add(numero)
            sin_respaldo.append(token)

    if sin_respaldo:
        hallazgos.append({
            "tipo": "cifra_inventada",
            "nivel": "bloqueante",
            "detalle": ("El borrador trae números que ninguna herramienta "
                        f"devolvió: {', '.join(sin_respaldo)}."),
        })

    # --- 2. CIFRAS PERDIDAS --------------------------------------------------
    for moneda, datos in sorted((verdad or {}).items()):
        pesos = datos.get("pesos")
        if pesos is None:
            continue
        if not any(numero == float(pesos)
                   for _, numero in numeros_de_texto(borrador)):
            hallazgos.append({
                "tipo": "cifra_perdida",
                "nivel": "aviso",
                # El separador de miles se escribe a la colombiana: el
                # `:,` de Python es inglés y aquí saldría "3,099,309".
                "detalle": (f"El resultado de {moneda} "
                            f"({format(pesos, ',').replace(',', '.')} COP) "
                            f"no aparece en el borrador."),
            })

    # --- 3. FUENTE PERDIDA ---------------------------------------------------
    # Se parte la fuente en palabras y se exige que sobrevivan las que
    # distinguen una fuente de otra. "mercado (open.er-api.com)" son dos.
    for moneda, datos in sorted((verdad or {}).items()):
        fuente = datos.get("fuente")
        if not isinstance(fuente, str):
            continue
        for palabra in {p for p in re.split(r"[\s()]+", fuente.lower())
                        if len(p) >= 4}:
            if palabra not in minusculas:
                hallazgos.append({
                    "tipo": "fuente_perdida",
                    "nivel": "aviso",
                    "detalle": (f"La fuente de {moneda} era «{fuente}» y la "
                                f"palabra «{palabra}» no sobrevivió al borrador."),
                })

    # --- 4. FECHA REETIQUETADA -----------------------------------------------
    for etiqueta in _ETIQUETAS_DE_CONSULTA:
        if etiqueta in minusculas:
            hallazgos.append({
                "tipo": "fecha_reetiquetada",
                "nivel": "aviso",
                "detalle": (f"El borrador dice «{etiqueta}», pero el harness "
                            f"nunca midió eso: el campo `actualizado` dice "
                            f"cuándo la FUENTE movió la tasa, no cuándo la "
                            f"consultamos nosotros."),
            })
            break        # una vez basta; no hace falta repetir el mismo aviso

    return hallazgos


def hay_bloqueante(hallazgos):
    """¿Alguno de estos hallazgos impide archivar?"""
    return any(h["nivel"] == "bloqueante" for h in hallazgos)


def como_texto(hallazgos):
    """Los hallazgos en prosa corta, para dárselos a un modelo o a un humano.

    ⭐ ESTO es lo que sube ahora a la etapa 3, en vez de la verdad cruda. Casi
       siempre son cero líneas o dos; la verdad cruda eran 907 tokens fijos,
       hiciera falta o no.
    """
    if not hallazgos:
        return ("El harness verificó el borrador contra los datos de las "
                "herramientas y no encontró diferencias.")
    lineas = ["El harness verificó el borrador y encontró esto:"]
    for h in hallazgos:
        marca = "🚨 BLOQUEANTE" if h["nivel"] == "bloqueante" else "⚠️ aviso"
        lineas.append(f"  {marca} · {h['detalle']}")
    return "\n".join(lineas)


# ---------------------------------------------------------------------------
# 3) LAS PRUEBAS — corren sin modelo, sin red y sin gastar un centavo
# ---------------------------------------------------------------------------
# 🚨 Y ESTO NO ES UN EXTRA. Un freno que nadie ha visto morder es una nota, no
#    un freno (LM.13). Aquí se le enseña a morder en los cuatro casos, y
#    también se comprueba que NO muerde cuando el borrador está bien — que es
#    la mitad que se olvida y la que convierte un freno en ruido.

VERDAD_DE_PRUEBA = {
    "USD": {"moneda": "USD", "monto": 1000, "pesos": 3099309,
            "tasa": 3099.309008, "fuente": "mercado (open.er-api.com)",
            "fecha": "Thu, 20 Aug 2026 00:02:31 +0000"},
    "EUR": {"moneda": "EUR", "monto": 1000, "pesos": 3610380,
            "tasa": 3610.3799525653394, "fuente": "mercado (open.er-api.com)",
            "fecha": "Thu, 20 Aug 2026 00:02:31 +0000"},
}

BORRADOR_LIMPIO = """# INFORME

Fuente: mercado (open.er-api.com). Tasas actualizadas el 20 de agosto de 2026.

| Divisa | Monto | En COP | Tasa |
|---|---|---|---|
| USD | 1.000 | $3.099.309 | 3.099,31 |
| EUR | 1.000 | $3.610.380 | 3.610,38 |
"""


def _pruebas():
    fallos = []

    def revisar(nombre, condicion, pista=""):
        estado = "✅" if condicion else "❌"
        print(f"  {estado} {nombre}")
        if not condicion:
            fallos.append(f"{nombre} {pista}")

    print("\n1) LEER NÚMEROS EN FORMATO COLOMBIANO")
    for texto, esperado in [("3.099.309", 3099309.0), ("3.610,38", 3610.38),
                            ("1.000", 1000.0), ("2026", 2026.0),
                            ("0,5", 0.5), ("3.14", 3.14)]:
        revisar(f"«{texto}» → {esperado}", a_numero(texto) == esperado,
                f"(dio {a_numero(texto)})")

    print("\n2) EL BORRADOR LIMPIO NO DEBE DISPARAR NADA")
    # Esta es la prueba que evita que el freno se vuelva ruido. Si falla, el
    # verificador es inútil aunque cace todo lo demás: nadie deja encendida una
    # alarma que suena siempre.
    limpio = verificar(BORRADOR_LIMPIO, VERDAD_DE_PRUEBA)
    revisar("cero hallazgos", limpio == [], f"(dio {limpio})")

    print("\n3) CIFRA INVENTADA → bloqueante")
    sucio = BORRADOR_LIMPIO.replace("$3.099.309", "$3.150.000")
    h = verificar(sucio, VERDAD_DE_PRUEBA)
    revisar("marca cifra_inventada",
            any(x["tipo"] == "cifra_inventada" for x in h), f"(dio {h})")
    revisar("y bloquea el archivo", hay_bloqueante(h))

    print("\n4) CIFRA PERDIDA → aviso")
    # Se borra la fila del EUR entera. El 3.610.380 desaparece.
    sin_eur = "\n".join(l for l in BORRADOR_LIMPIO.splitlines()
                        if "EUR" not in l)
    h = verificar(sin_eur, VERDAD_DE_PRUEBA)
    revisar("marca cifra_perdida",
            any(x["tipo"] == "cifra_perdida" for x in h), f"(dio {h})")
    revisar("y NO bloquea", not hay_bloqueante(h))

    print("\n5) FUENTE PERDIDA → aviso")
    sin_mercado = BORRADOR_LIMPIO.replace("mercado (open.er-api.com)",
                                          "open.er-api.com")
    h = verificar(sin_mercado, VERDAD_DE_PRUEBA)
    revisar("marca fuente_perdida",
            any(x["tipo"] == "fuente_perdida" for x in h), f"(dio {h})")

    print("\n6) FECHA REETIQUETADA → aviso  (el caso REAL de la sesión 92)")
    reetiquetado = BORRADOR_LIMPIO.replace(
        "Tasas actualizadas el", "Fecha de consulta:")
    h = verificar(reetiquetado, VERDAD_DE_PRUEBA)
    revisar("marca fecha_reetiquetada",
            any(x["tipo"] == "fecha_reetiquetada" for x in h), f"(dio {h})")
    revisar("una sola vez, no repetido",
            sum(1 for x in h if x["tipo"] == "fecha_reetiquetada") == 1)

    print("\n7) EL LÍMITE DECLARADO: una paráfrasis NO se caza")
    # 🚨 Esta prueba comprueba que el verificador FALLA, y está aquí a
    #    propósito. La cabecera promete un freno estrecho; si algún día alguien
    #    lo ensancha, esta prueba se pone roja y le obliga a corregir la
    #    promesa en vez de dejarla desactualizada en silencio.
    parafrasis = BORRADOR_LIMPIO.replace("Tasas actualizadas el",
                                         "Datos tomados al")
    h = verificar(parafrasis, VERDAD_DE_PRUEBA)
    revisar("no marca fecha_reetiquetada (límite conocido)",
            not any(x["tipo"] == "fecha_reetiquetada" for x in h))

    return fallos


if __name__ == "__main__":
    print("=" * 70)
    print("VERIFICADOR — pruebas propias. Sin modelo, sin red, $0,00.")
    print("=" * 70)

    fallos = _pruebas()

    print("\n" + "=" * 70)
    if fallos:
        print(f"❌ {len(fallos)} prueba(s) en rojo:")
        for f in fallos:
            print(f"   · {f}")
        sys.exit(1)
    print("✅ Todas en verde.")
    print("=" * 70)

    print("\nY así se ve sobre el borrador REAL de la corrida de la sesión 92:")
    real = """# INFORME DE CONVERSIÓN DE DIVISAS A PESOS COLOMBIANOS

**Fecha de consulta:** 20 de agosto de 2026
**Fuente:** open.er-api.com

| Divisa | Monto Original | Equivalente en COP | Tasa de Cambio |
|--------|----------------|--------------------|----------------|
| USD | 1.000 | $3.099.309 | 3.099,31 COP/USD |
| EUR | 1.000 | $3.610.380 | 3.610,38 COP/EUR |

**Nota:** Las tasas corresponden al mercado abierto en la fecha indicada."""
    print("-" * 70)
    print(como_texto(verificar(real, VERDAD_DE_PRUEBA)))
    print("-" * 70)
    print("\n📌 Compáralo con lo que dijo el modelo teniendo esos mismos datos")
    print("   delante: «coinciden exactamente con los datos verificados».")
