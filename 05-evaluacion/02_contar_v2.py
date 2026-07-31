"""
Nivel 5 - Script 2: el experimento corregido, con N grande y dos detectores.

QUE CAMBIA RESPECTO A 01_contar.py, Y POR QUE
---------------------------------------------
1. LA PREGUNTA. En la v1 preguntabamos "que ropa me pongo hoy en Bogota si
   esta lloviendo?" y 6 de 10 respuestas se gastaron diciendo "no puedo
   consultar el clima". El modelo no tiene herramientas, asi que nunca
   llegaba a dar consejo -- que es justo donde el defecto aparecia.
   Ahora el clima viene DADO en la pregunta. No hay de que disculparse.

   (Es el error de 03_recortar.py del nivel 2 con otra ropa: alli se probo
   la memoria preguntando algo que el modelo ya sabia. La prueba corria,
   pero no probaba lo que decia probar.)

2. N = 30, no 10. Con 10 corridas y un defecto de 1-de-3 hay ~2% de
   probabilidad de no verlo ni una vez. Con 30 el numero empieza a
   significar algo.

   OJO a la distincion, que es la mitad de este nivel:
   - la PREGUNTA es una variable: cambiarla cambia lo que mides.
   - el N es precision: no mueve el resultado real, solo tu confianza.
   Por eso cambiar los dos a la vez NO es el error de las 3 variables
   del nivel 1. Solo hay una variable de verdad.

3. DOS DETECTORES. El del dialecto (heredado de 01_contar.py) y uno nuevo
   de TRATAMIENTO (tu vs usted), que salio de mirar las 10 respuestas de
   la v1: el modelo trataba de "tu" en 4 y de "usted" en 5, con el mismo
   prompt. Nadie fue a buscar eso. Aparecio por contar.

COSTO: ESTIMADO ~$0.14 con N=30 (a $0.0046 por corrida, medido en la v1).
       Marcado como estimacion a proposito: la respuesta ahora es de
       consejo puro y puede ser mas larga. Anotar el numero real al correr.

USO:
    python 00_probar_detector.py    # gratis, primero SIEMPRE
    python 02_contar_v2.py          # N = 30
    python 02_contar_v2.py 10       # N = 10, para una prueba barata
"""

import importlib.util
import json
import sys
import time
from datetime import datetime
from pathlib import Path

import anthropic
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# Reusamos el detector de dialecto de la v1 en vez de copiarlo.
# Copiar codigo entre scripts es como tener el mismo dato en dos sitios:
# tarde o temprano se corrigen uno y no el otro.
_ruta = Path(__file__).resolve().parent / "01_contar.py"
_spec = importlib.util.spec_from_file_location("contar", _ruta)
v1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v1)


# ---------------------------------------------------------------------------
# ZONA A - Configuracion
# ---------------------------------------------------------------------------

MODELO = "claude-opus-5"

# Identico a la v1, palabra por palabra. Es la unica forma de que la
# comparacion entre los dos experimentos signifique algo.
SYSTEM = v1.SYSTEM

# LA CORRECCION. El clima va dado, asi el modelo entra directo a aconsejar.
PREGUNTA = "Esta lloviendo en Bogota y hace 14 grados. Que ropa me pongo?"

N = int(sys.argv[1]) if len(sys.argv) > 1 else 30


# ---------------------------------------------------------------------------
# ZONA B - El detector nuevo: tratamiento (tu / usted)
# ---------------------------------------------------------------------------
# Se busca SIN normalizar tildes, por la misma razon que los imperativos
# voseantes: aqui la tilde tambien distingue.
#   "estás" (tuteo)  vs  "estas" (demostrativo: "estas cosas")
# Si normalizara, "estas cosas" contaria como tuteo. Falso positivo.

TUTEO = [
    # pronombres y cliticos: son los mas fiables
    "tú", "te", "ti", "contigo", "tuyo", "tuya",
    # verbos en 2a persona del singular
    "tienes", "puedes", "quieres", "estás", "necesitas", "vas", "sales",
    # imperativos con enclitico
    "ponte", "llévate", "cuídate", "abrígate",
]

USTEDEO = [
    "usted", "suyo", "suya",
    # imperativos de usted
    "póngase", "cuídese", "llévese", "abríguese", "cámbiese",
    "lleve", "tenga", "use", "salga", "póngale",
    # frases con "le": "le" solo es ambiguo (sirve tambien para 3a
    # persona), asi que se busca acompañado de su verbo.
    "le hablo", "le puedo", "le recomiendo", "le sugiero",
    "le cuento", "le digo", "le doy", "le conviene",
]

# NO van en ninguna lista, a proposito:
#   "le", "se", "su"  -> ambiguos con la 3a persona ("su chaqueta" puede
#                        ser de el, de ella o de usted).
# Perder señal es mejor que inventarla. Un detector que adivina produce
# un numero que parece exacto y no lo es.
DESCARTADOS_TRATAMIENTO = ["le", "se", "su"]


def tratamiento(texto):
    """Devuelve 'tu', 'usted', 'mixto' o 'indeterminado'.

    Cuatro salidas, no dos. Un detector honesto tiene que poder decir
    'no se': forzar un binario cuando no hay evidencia es inventarse el
    dato. El caso 'mixto' es ademas el mas interesante -- si una sola
    respuesta mezcla los dos, el defecto vive DENTRO del texto y no solo
    entre corridas."""
    tu = v1.buscar(texto, TUTEO, quitar_tildes=False)
    ud = v1.buscar(texto, USTEDEO, quitar_tildes=False)

    if tu and ud:
        etiqueta = "mixto"
    elif tu:
        etiqueta = "tu"
    elif ud:
        etiqueta = "usted"
    else:
        etiqueta = "indeterminado"
    return etiqueta, tu, ud


def dialecto(texto):
    """El detector de la v1, sin cambios."""
    return (v1.buscar(texto, v1.MARCADORES_RIOPLATENSES)
            + v1.buscar(texto, v1.IMPERATIVOS_VOSEANTES, quitar_tildes=False))


# ---------------------------------------------------------------------------
# ZONA C - Una corrida
# ---------------------------------------------------------------------------

cliente = anthropic.Anthropic(max_retries=2, timeout=60.0)

PRECIO_ENTRADA = 5.00 / 1_000_000
PRECIO_SALIDA = 25.00 / 1_000_000


def una_corrida(numero):
    inicio = time.time()
    respuesta = cliente.messages.create(
        model=MODELO,
        max_tokens=1024,
        system=SYSTEM,
        messages=[{"role": "user", "content": PREGUNTA}],
    )
    segundos = time.time() - inicio

    texto = "".join(b.text for b in respuesta.content if b.type == "text")
    rio = dialecto(texto)
    trato, marcas_tu, marcas_ud = tratamiento(texto)

    return {
        "n": numero,
        "texto": texto.strip(),
        "rioplatense": len(rio) > 0,
        "marcas_rio": rio,
        "tratamiento": trato,
        "marcas_tu": marcas_tu,
        "marcas_ud": marcas_ud,
        "entrada": respuesta.usage.input_tokens,
        "salida": respuesta.usage.output_tokens,
        "stop_reason": respuesta.stop_reason,
        "segundos": round(segundos, 2),
        "hora": datetime.now().isoformat(timespec="seconds"),
    }


# ---------------------------------------------------------------------------
# ZONA D - El bucle, el conteo y el guardado
# ---------------------------------------------------------------------------

SIGLA = {"tu": "TU   ", "usted": "USTED", "mixto": "MIXTO",
         "indeterminado": "  ?  "}


def main():
    print("=" * 74)
    print(f"  EXPERIMENTO v2: el mismo prompt, {N} veces")
    print("=" * 74)
    print(f"  modelo   : {MODELO}")
    print(f"  pregunta : {PREGUNTA}")
    print(f"  cambio   : el clima va DADO (en la v1 se disculpaba 6 de 10)")
    print("=" * 74)
    print()
    print("   #   dialecto      trato    tiempo    tokens")
    print("  " + "-" * 46)

    resultados = []
    for i in range(1, N + 1):
        r = una_corrida(i)
        resultados.append(r)
        dial = "RIOPLAT." if r["rioplatense"] else "limpia  "
        print(f"  {i:>2}   {dial}      {SIGLA[r['tratamiento']]}"
              f"   {r['segundos']:>5.2f}s   {r['salida']:>4}")

    # ---- el detalle, solo de lo que llama la atencion ------------------
    print()
    print("-" * 74)
    print("  RESPUESTAS CON ALGO QUE MIRAR")
    print("-" * 74)
    for r in resultados:
        if not r["rioplatense"] and r["tratamiento"] not in ("mixto", "indeterminado"):
            continue
        print(f"  {r['n']:>2}. {' '.join(r['texto'].split())[:62]}...")
        if r["marcas_rio"]:
            print(f"      rioplatense: {', '.join(r['marcas_rio'])}")
        if r["tratamiento"] == "mixto":
            print(f"      MIXTO -> tu: {', '.join(r['marcas_tu'])}"
                  f"  |  usted: {', '.join(r['marcas_ud'])}")
        if r["tratamiento"] == "indeterminado":
            print("      indeterminado: ningun marcador. Leela con tus ojos.")

    # ---- los dos numeros -----------------------------------------------
    sucias = sum(1 for r in resultados if r["rioplatense"])
    conteo = {}
    for r in resultados:
        conteo[r["tratamiento"]] = conteo.get(r["tratamiento"], 0) + 1

    entrada = sum(r["entrada"] for r in resultados)
    salida = sum(r["salida"] for r in resultados)
    costo = entrada * PRECIO_ENTRADA + salida * PRECIO_SALIDA

    print()
    print("=" * 74)
    print(f"  DEFECTO 1 - dialecto rioplatense: {sucias} de {N}"
          f"   ({sucias / N:.0%})")
    print(f"  DEFECTO 2 - tratamiento:")
    for etiqueta in ("tu", "usted", "mixto", "indeterminado"):
        cuantas = conteo.get(etiqueta, 0)
        barra = "#" * cuantas
        print(f"       {etiqueta:<14} {cuantas:>3} de {N}  {barra}")
    print("=" * 74)

    entradas = sorted({r["entrada"] for r in resultados})
    print(f"  entradas identicas al token? "
          f"{'SI' if len(entradas) == 1 else 'NO'}  -> {entradas}")
    print(f"  salida  : de {min(r['salida'] for r in resultados)} a "
          f"{max(r['salida'] for r in resultados)} tokens")
    print(f"  tiempo  : de {min(r['segundos'] for r in resultados)}s a "
          f"{max(r['segundos'] for r in resultados)}s")
    print(f"  tokens  : {entrada} entrada / {salida} salida")
    print(f"  COSTO REAL: ${costo:.4f}")
    print("=" * 74)

    carpeta = Path(__file__).resolve().parent / "resultados"
    carpeta.mkdir(exist_ok=True)
    sello = datetime.now().strftime("%Y%m%d-%H%M%S")
    archivo = carpeta / f"v2-clima-dado-{sello}.json"
    archivo.write_text(json.dumps({
        "experimento": "v2 - clima dado, dialecto + tratamiento",
        "modelo": MODELO,
        "system": SYSTEM,
        "pregunta": PREGUNTA,
        "n": N,
        "rioplatense": sucias,
        "tratamiento": conteo,
        "costo": round(costo, 4),
        "corridas": resultados,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  guardado en: resultados/{archivo.name}")

    print()
    print("  COMO LEER ESTO:")
    print(f"  - Si el dialecto sale 0 de {N} otra vez, ya no se puede echar")
    print("    la culpa al diseño del experimento: el terreno ahora SI es")
    print("    el de dar consejo. Seria evidencia de verdad.")
    print("  - Si el tratamiento sale repartido, tienes un defecto nuevo")
    print("    medido, que nadie fue a buscar. Y se arregla en el SYSTEM.")
    print("  - Si sale algun MIXTO, es el caso mas grave: el modelo se")
    print("    contradice DENTRO de una sola respuesta.")


if __name__ == "__main__":
    main()
