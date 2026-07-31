"""
Nivel 5 - Script 1: correr N veces y contar.

LA PREGUNTA QUE RESPONDE:
    El espanol rioplatense ("queres", "campera", "lleva paraguas") aparecio en
    1 de cada 3 respuestas, en 3 corridas, en 2 maquinas, y en respuesta
    distinta cada vez. Con n=1 no se puede saber nada. Aqui corremos el MISMO
    prompt N veces y contamos.

LO QUE NO HACE:
    No arregla el defecto. Solo lo mide. Arreglar sin medir antes es apostar.

COSTO: MEDIDO $0.0459 con N=10 y Opus 5 (1020 entrada / 1632 salida).
       Antes aqui decia "ESTIMADO ~$0.10": me pase al doble.
       Sale a ~$0.0046 por corrida, asi que N=30 son ~$0.14.
       (Regla del curso: un numero o viene de una corrida, o va marcado
       como estimacion. Ver el error del docstring de 04_streaming.py.)

USO:
    python 01_contar.py          # N = 10, el valor por defecto
    python 01_contar.py 30       # N = 30
"""

import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import anthropic
from dotenv import load_dotenv

# La consola de Windows es cp1252 y las respuestas traen tildes y emojis.
# Sin esto el print revienta con UnicodeEncodeError aunque la API haya
# funcionado perfecto. Leccion del nivel 3.
sys.stdout.reconfigure(encoding="utf-8")

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


# ---------------------------------------------------------------------------
# ZONA A - La configuracion del experimento
# ---------------------------------------------------------------------------
# Todo lo que define QUE se esta midiendo vive aqui arriba, junto y visible.
# Si manana quieres repetir el experimento cambiando una sola cosa, tienes
# que poder ver de un vistazo cual es esa sola cosa.

MODELO = "claude-opus-5"

# Copiado LITERAL de 04-harness-real/03_harness.py (linea 253).
# No es un system parecido: es EL system que produjo el defecto.
# Si lo cambias, ya no estas midiendo lo mismo.
SYSTEM = (
    "Eres un asistente breve. Responde en espanol de Colombia, "
    "en dos frases como maximo. Si una herramienta te dice que "
    "no pudo hacer algo, dilo con claridad en vez de inventar."
)

# La pregunta se eligio a proposito para provocar CONSEJO.
# El rioplatense aparecio siempre en modo imperativo ("lleva paraguas",
# "Si queres, autoriza"), y el voseo se nota justo ahi. Una pregunta
# de dato seco ("cuanto es 17 por 23") no daria terreno para el defecto.
PREGUNTA = "Que ropa me pongo hoy en Bogota si esta lloviendo?"

N = int(sys.argv[1]) if len(sys.argv) > 1 else 10


# ---------------------------------------------------------------------------
# ZONA B - El detector
# ---------------------------------------------------------------------------
# Esto es un eval de TIPO 1: se comprueba con un if.
# Y es tambien el limite del tipo 1, que veras en cuanto lo corras:
# la lista la escribi yo, y lo que no este en la lista no existe para el
# programa. Un detector no ve el dialecto: ve las palabras que le enseñaste.

# Van en DOS listas, y la razon es un defecto que casi se me cuela.
#
# "Lleva sombrilla"  <- Colombia, correcto
# "Llevá sombrilla"  <- rioplatense
#
# La UNICA diferencia es la tilde. Si normalizo tildes antes de comparar,
# borro justo la señal que vine a buscar, y el detector marcaria como
# rioplatense la forma colombiana correcta. Mismo patron del [:30] del
# nivel 1 y del [:80] del nivel 4: el preprocesamiento destruye el dato.

# Lista 1 - AQUI LA TILDE ES EL DATO. Se busca literal, sin normalizar.
IMPERATIVOS_VOSEANTES = [
    "llevá", "poné", "ponete", "mirá", "andá", "tomá", "esperá",
    "autorizá", "revisá", "usá", "probá", "dejá", "fijate", "salí",
    "vení", "hacé", "decí", "buscá", "abrigate", "cuidate",
]

# Lista 2 - aqui la tilde no distingue nada, porque estas formas
# simplemente NO existen en el espanol colombiano. "querés" y "queres"
# son las dos rioplatenses; ninguna choca con "quieres". Se normaliza.
MARCADORES_RIOPLATENSES = [
    # voseo verbal
    "sos", "queres", "tenes", "podes",
    "vos", "decis", "venis", "vivis",
    # lexico
    "campera", "pileta", "colectivo", "laburo", "boludo", "che",
    "remera", "pollera", "birome", "frazada", "pucha",
]

# OJO: estas NO van en la lista aunque suenen rioplatenses.
# "aca" y "plata" se usan igual en Colombia. Meterlas daria falsos
# positivos y el numero final seria mentira. Un detector mal calibrado
# es peor que no tener detector: da una cifra con aire de exactitud.
DESCARTADAS_A_PROPOSITO = ["aca", "plata", "ahorita"]

# Control positivo: si aparecen estas, el modelo SI esta hablando colombiano.
# Sirve para saber que el detector mira donde debe.
MARCADORES_COLOMBIANOS = [
    "tinto", "parcero", "chevere", "sumerce", "vaina", "bacano",
    "usted", "sombrilla", "saco", "buseta", "chaqueta",
]


def normalizar(texto):
    """Quita tildes y baja a minusculas, para que 'llevá' y 'lleva' se
    comparen igual. Sin esto el detector se le escapa la mitad."""
    texto = texto.lower()
    for con, sin in [("á", "a"), ("é", "e"), ("í", "i"),
                     ("ó", "o"), ("ú", "u"), ("ñ", "n")]:
        texto = texto.replace(con, sin)
    return texto


def buscar(texto, lista, quitar_tildes=True):
    """Devuelve los marcadores de la lista que aparecen en el texto.

    quitar_tildes=False es para los imperativos voseantes, donde la tilde
    ES la señal ('llevá' vs 'lleva') y normalizar la destruiria.

    Usa \\b (limite de palabra) para no cazar 'vos' dentro de 'nosotros'.
    Ese es el falso positivo mas facil de cometer aqui."""
    plano = normalizar(texto) if quitar_tildes else texto.lower()
    hallados = []
    for marca in lista:
        objetivo = marca.strip().lower()
        if quitar_tildes:
            objetivo = normalizar(objetivo)
        patron = r"\b" + re.escape(objetivo) + r"\b"
        if re.search(patron, plano):
            hallados.append(marca.strip())
    return hallados


# ---------------------------------------------------------------------------
# ZONA C - Una corrida
# ---------------------------------------------------------------------------

# max_retries explicito, aunque 2 es el valor de fabrica.
# Leccion L4.4: durante tres niveles enteros cada create() podia hacer hasta
# 3 peticiones y nunca se noto porque nunca fallo nada. En un experimento
# donde CUENTAS llamadas, eso no puede quedar invisible.
cliente = anthropic.Anthropic(max_retries=2, timeout=60.0)

PRECIO_ENTRADA = 5.00 / 1_000_000   # Opus 5, confirmado con aritmetica en L4.20
PRECIO_SALIDA = 25.00 / 1_000_000


def una_corrida(numero):
    """Hace UNA llamada y devuelve el diccionario con todo lo que paso."""
    inicio = time.time()
    respuesta = cliente.messages.create(
        model=MODELO,
        max_tokens=1024,          # holgado: con poco, el thinking se lo come (L1.1)
        system=SYSTEM,
        messages=[{"role": "user", "content": PREGUNTA}],
    )
    segundos = time.time() - inicio

    # respuesta.content puede traer bloques 'thinking' ademas de 'text'.
    # Nunca content[0].text: en la maquina del estudiante salio distinto
    # que en la mia (L3.1). Se recorre y se filtra.
    texto = "".join(b.text for b in respuesta.content if b.type == "text")

    # Dos busquedas distintas porque son dos criterios distintos.
    # Los imperativos NO se normalizan: ahi la tilde es el dato.
    rio = (buscar(texto, MARCADORES_RIOPLATENSES)
           + buscar(texto, IMPERATIVOS_VOSEANTES, quitar_tildes=False))
    col = buscar(texto, MARCADORES_COLOMBIANOS)

    return {
        "n": numero,
        "texto": texto.strip(),
        "rioplatense": len(rio) > 0,
        "marcas_rio": rio,
        "marcas_col": col,
        "entrada": respuesta.usage.input_tokens,
        "salida": respuesta.usage.output_tokens,
        "stop_reason": respuesta.stop_reason,
        "segundos": round(segundos, 2),
        "hora": datetime.now().isoformat(timespec="seconds"),
    }


# ---------------------------------------------------------------------------
# ZONA D - El bucle y el conteo
# ---------------------------------------------------------------------------

def main():
    print("=" * 72)
    print(f"  EXPERIMENTO: el mismo prompt, {N} veces")
    print("=" * 72)
    print(f"  modelo   : {MODELO}")
    print(f"  pregunta : {PREGUNTA}")
    print(f"  system   : espanol de Colombia (copiado de 03_harness.py)")
    print("=" * 72)
    print()

    resultados = []
    for i in range(1, N + 1):
        print(f"  corrida {i:>2}/{N} ... ", end="", flush=True)
        r = una_corrida(i)
        resultados.append(r)
        marca = "RIOPLATENSE" if r["rioplatense"] else "limpia     "
        print(f"{marca}  ({r['segundos']:>5.2f}s, {r['salida']} tok)")

    print()
    print("-" * 72)
    print("  DETALLE")
    print("-" * 72)
    for r in resultados:
        senal = "!!" if r["rioplatense"] else "  "
        primera = " ".join(r["texto"].split())[:58]
        print(f"{senal} {r['n']:>2}. {primera}...")
        if r["marcas_rio"]:
            print(f"      -> rioplatense: {', '.join(r['marcas_rio'])}")
        if r["marcas_col"]:
            print(f"      -> colombiano : {', '.join(r['marcas_col'])}")

    # ---- el numero que veniamos a buscar -------------------------------
    sucias = sum(1 for r in resultados if r["rioplatense"])
    entrada = sum(r["entrada"] for r in resultados)
    salida = sum(r["salida"] for r in resultados)
    costo = entrada * PRECIO_ENTRADA + salida * PRECIO_SALIDA

    print()
    print("=" * 72)
    print(f"  RESULTADO: {sucias} de {N} respuestas con marcador rioplatense")
    print(f"             ({sucias / N:.0%})")
    print("=" * 72)
    print(f"  entradas identicas al token? "
          f"{'SI' if len({r['entrada'] for r in resultados}) == 1 else 'NO'}"
          f"  -> {sorted({r['entrada'] for r in resultados})}")
    print(f"  salida  : de {min(r['salida'] for r in resultados)} a "
          f"{max(r['salida'] for r in resultados)} tokens")
    print(f"  tiempo  : de {min(r['segundos'] for r in resultados)}s a "
          f"{max(r['segundos'] for r in resultados)}s")
    print(f"  tokens  : {entrada} entrada / {salida} salida")
    print(f"  COSTO REAL: ${costo:.4f}")
    print("=" * 72)

    # ---- guardar, para poder comparar despues ---------------------------
    # Un numero suelto no sirve: el valor de este archivo aparece cuando
    # cambies algo y corras otra vez. Sin guardar, no hay con que comparar.
    carpeta = Path(__file__).resolve().parent / "resultados"
    carpeta.mkdir(exist_ok=True)
    sello = datetime.now().strftime("%Y%m%d-%H%M%S")
    archivo = carpeta / f"dialecto-system-{sello}.json"
    archivo.write_text(json.dumps({
        "experimento": "dialecto anclado en el SYSTEM",
        "modelo": MODELO,
        "system": SYSTEM,
        "pregunta": PREGUNTA,
        "n": N,
        "sucias": sucias,
        "costo": round(costo, 4),
        "corridas": resultados,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  guardado en: resultados/{archivo.name}")

    # ---- la advertencia que evita sacar conclusiones de mas -------------
    print()
    print("  OJO antes de concluir:")
    print(f"  - {sucias}/{N} NO es lo mismo que decir '{sucias / N:.0%} exacto'.")
    print("    Con N pequeño el numero baila. Por eso el siguiente paso es")
    print("    subir N, no interpretar este.")
    print("  - Un marcador que no este en mi lista no existe para el programa.")
    print("    Lee las respuestas 'limpias' con tus ojos y busca si se me")
    print("    escapo alguna. Eso es justo lo que el juez del tipo 2 arregla.")


if __name__ == "__main__":
    main()
