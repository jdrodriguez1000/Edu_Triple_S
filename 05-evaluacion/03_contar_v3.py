"""
Nivel 5 - Script 3: cerrar el ciclo. Medir, cambiar, volver a medir.

HASTA AQUI SOLO MEDISTE. Este script es el paso que hace que evaluar
sirva de verdad:

    medir  ->  cambiar UNA cosa  ->  medir otra vez  ->  comparar
     30%              ?                    ?              ¿bajo?

En el nivel 3 y en el 4 el dialecto se "arreglo" dos veces y ninguna de
las dos se pudo saber si habia funcionado, porque no habia numero contra
que comparar. Ahora si lo hay: 9 de 30 (30%) con el SYSTEM actual.

LAS TRES VERSIONES
------------------
A - CONTROL. El SYSTEM de hoy, sin tocar. No esta aqui de relleno: si A
    no vuelve a dar ~30%, ninguna comparacion vale, porque significaria
    que algo mas cambio entre ayer y hoy. El control es lo que te dice
    si tu regla de medir sigue siendo la misma regla.

B - PROHIBICION EXPLICITA. Igual que A pero nombrando el defecto:
    "nunca uses voseo". La apuesta: como las tres formas (ponte /
    ponete / pongase) son espanol correcto, el modelo no sabe cual es
    la tuya hasta que se lo dices con nombre propio.

C - LA MISMA INSTRUCCION, MOVIDA DE SITIO. "Responde en espanol de
    Colombia" sale del SYSTEM y entra en el turno del usuario. El texto
    es identico; lo unico que cambia es DONDE va.
    Esta es tu hipotesis pendiente del nivel 4: el marcador iba
    SYSTEM 3 de 9, turno del usuario 0 de 4. Con esos numeros no probaba
    nada. Con 30 y 30, empieza a probar algo.

POR QUE SE INTERCALAN A, B, C, A, B, C...
-----------------------------------------
En vez de correr las 30 de A, luego las 30 de B, luego las 30 de C.
Si algo cambia con el tiempo -- la carga de los servidores, tu red, lo
que sea -- correrlas en bloque se lo carga todo a la ultima version.
Intercalando, ese efecto se reparte por igual entre las tres.

Es tu propia tecnica del ejercicio 9 del nivel 4: alli descubriste que
ir primero costaba ~1 segundo, y lo cazaste corriendo las dos formas en
las dos posiciones. Misma idea, aplicada a tres.

COSTO: ESTIMADO ~$0.38 (90 llamadas, a ~$0.0042 cada una segun la v2).
       Tarda unos 7 minutos. Es la corrida mas cara del curso.

USO:
    python 00_probar_detector.py    # gratis, primero SIEMPRE
    python 03_contar_v3.py          # 30 por version = 90 llamadas
    python 03_contar_v3.py 10       # 10 por version = 30, para probar
"""

import importlib.util
import json
import math
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import anthropic
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def cargar(nombre, alias):
    ruta = Path(__file__).resolve().parent / nombre
    spec = importlib.util.spec_from_file_location(alias, ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


v1 = cargar("01_contar.py", "contar")
v2 = cargar("02_contar_v2.py", "contar_v2")


# ---------------------------------------------------------------------------
# ZONA A - Las tres versiones
# ---------------------------------------------------------------------------

MODELO = "claude-opus-5"
N = int(sys.argv[1]) if len(sys.argv) > 1 else 30

CLIMA = "Esta lloviendo en Bogota y hace 14 grados. Que ropa me pongo?"

# El SYSTEM de siempre, sin la parte del dialecto. Se usa para armar
# las tres versiones sin repetir texto.
BASE_SIN_DIALECTO = (
    "Eres un asistente breve. Responde en dos frases como maximo. "
    "Si una herramienta te dice que no pudo hacer algo, dilo con "
    "claridad en vez de inventar."
)

VERSIONES = {
    # A: exactamente el de la v2. Se toma de v1.SYSTEM, no se copia,
    #    para que sea imposible que se desincronicen.
    "A": {
        "nombre": "control (el SYSTEM de siempre)",
        "system": v1.SYSTEM,
        "usuario": CLIMA,
    },
    # B: lo mismo + prohibicion con nombre propio.
    "B": {
        "nombre": "prohibicion explicita del voseo",
        "system": v1.SYSTEM + (
            " Nunca uses voseo ni formas rioplatenses como 'ponete', "
            "'llevá', 'querés' o 'tenés'. Usa siempre el tuteo colombiano: "
            "'ponte', 'lleva', 'quieres'."
        ),
        "usuario": CLIMA,
    },
    # C: MISMA instruccion que A, movida al turno del usuario.
    #    Fijate en que el SYSTEM aqui NO menciona Colombia: si lo dijera
    #    en los dos sitios, no estarias midiendo la posicion, estarias
    #    midiendo "decirlo dos veces".
    "C": {
        "nombre": "dialecto en el turno del usuario",
        "system": BASE_SIN_DIALECTO,
        "usuario": "Responde en espanol de Colombia. " + CLIMA,
    },
}


# ---------------------------------------------------------------------------
# ZONA B - Detectores (heredados) + el de la forma verbal
# ---------------------------------------------------------------------------

def forma_verbal(texto):
    """Cual de las tres conjugaciones de 'poner' uso.

    Este detector nacio del hallazgo de la v2: los 9 rioplatenses eran
    EXACTAMENTE las 9 respuestas con 'ponete', y los 2 ustedeos eran los
    2 'pongase'. El defecto no es un estilo difuso: es una bifurcacion
    en una sola palabra. Medir esa palabra directamente es mas preciso
    que medir el estilo."""
    plano = texto.lower()
    for forma, etiqueta in [("ponete", "ponete (rioplatense)"),
                            ("póngase", "pongase (usted)"),
                            ("pongase", "pongase (usted)"),
                            ("ponte", "ponte (tu, correcto)")]:
        if re.search(r"\b" + forma + r"\b", plano):
            return etiqueta
    return "otro verbo"


def dialecto(texto):
    return (v1.buscar(texto, v1.MARCADORES_RIOPLATENSES)
            + v1.buscar(texto, v1.IMPERATIVOS_VOSEANTES, quitar_tildes=False))


# ---------------------------------------------------------------------------
# ZONA C - Una corrida
# ---------------------------------------------------------------------------

cliente = anthropic.Anthropic(max_retries=2, timeout=60.0)
PRECIO_ENTRADA = 5.00 / 1_000_000
PRECIO_SALIDA = 25.00 / 1_000_000


def una_corrida(clave, numero):
    ver = VERSIONES[clave]
    inicio = time.time()
    respuesta = cliente.messages.create(
        model=MODELO,
        max_tokens=1024,
        system=ver["system"],
        messages=[{"role": "user", "content": ver["usuario"]}],
    )
    segundos = time.time() - inicio

    texto = "".join(b.text for b in respuesta.content if b.type == "text")
    rio = dialecto(texto)
    trato, m_tu, m_ud = v2.tratamiento(texto)

    return {
        "version": clave,
        "n": numero,
        "texto": texto.strip(),
        "rioplatense": len(rio) > 0,
        "marcas_rio": rio,
        "tratamiento": trato,
        "forma_verbal": forma_verbal(texto),
        "entrada": respuesta.usage.input_tokens,
        "salida": respuesta.usage.output_tokens,
        "segundos": round(segundos, 2),
        "hora": datetime.now().isoformat(timespec="seconds"),
    }


# ---------------------------------------------------------------------------
# ZONA D - Cuanto se puede confiar en la diferencia
# ---------------------------------------------------------------------------

def rango(exitos, total):
    """Devuelve (minimo, maximo) creibles al 95%, en porcentaje.

    Se llamaba 'margen' y devolvia un solo numero, pero al arreglar el
    bug de los extremos dejo de ser simetrico: 0 de 30 va de 0% a 10%,
    no "0% mas menos algo". El nombre tenia que cambiar con el dato.

    POR QUE HACE FALTA:
    Si A da 9/30 y B da 7/30, la tentacion es decir "B mejoro".
    Pero con 30 corridas, dos respuestas de diferencia caben de sobra
    dentro del ruido: si repitieras A tal cual, podria darte 7 sin que
    nada haya cambiado.

    Esta funcion pone numero a esa duda. Si los rangos de dos versiones
    se solapan, la diferencia NO esta demostrada -- lo cual no significa
    que no exista, solo que 30 corridas no alcanzan para verla.

    Es la version con formula de la leccion que ya vivio en el nivel 4
    (L4.22): normalizar los tok/s no arreglaba que n=1.

    OJO CON LOS EXTREMOS -- bug encontrado probando esta funcion antes
    de usarla, y es el peor tipo de bug para un eval: no revienta, solo
    miente, y miente con cara de matematica.
    La formula normal da +/- 0.0 cuando exitos=0, o sea "0 de 30
    significa CERO defecto, con certeza total". Es falso: un defecto
    del 5% tiene ~21% de probabilidad de no salir ni una vez en 30.
    Para ese caso se usa la REGLA DE TRES: si no viste ninguno en n
    intentos, el tope al 95% es 3/n. Con n=30 eso es 10%, no 0%."""
    if total == 0:
        return 0.0, 0.0
    p = exitos / total * 100

    if exitos == 0:
        return 0.0, 3 / total * 100          # regla de tres
    if exitos == total:
        return 100 - 3 / total * 100, 100.0  # la misma, por el otro lado

    m = 1.96 * math.sqrt((p / 100) * (1 - p / 100) / total) * 100
    return max(0.0, p - m), min(100.0, p + m)


# ---------------------------------------------------------------------------
# ZONA E - El bucle intercalado
# ---------------------------------------------------------------------------

def main():
    claves = list(VERSIONES)
    print("=" * 78)
    print(f"  EXPERIMENTO v3: tres versiones x {N} corridas = {N * len(claves)} llamadas")
    print("=" * 78)
    for c in claves:
        print(f"  {c} - {VERSIONES[c]['nombre']}")
    print("-" * 78)
    print("  Se corren INTERCALADAS (A,B,C,A,B,C...) para que cualquier")
    print("  cambio con el tiempo se reparta por igual entre las tres.")
    print("=" * 78)
    print()
    print("  vuelta    A            B            C")
    print("  " + "-" * 46)

    resultados = []
    for vuelta in range(1, N + 1):
        fila = f"  {vuelta:>4}   "
        for clave in claves:
            r = una_corrida(clave, vuelta)
            resultados.append(r)
            fila += ("RIOPLAT.  " if r["rioplatense"] else "limpia    ") + "   "
        print(fila, flush=True)

    # ---- el resumen que responde la pregunta ----------------------------
    print()
    print("=" * 78)
    print("  RESULTADO")
    print("=" * 78)
    print(f"  {'ver':<4} {'rioplatense':<16} {'margen 95%':<18} {'que era'}")
    print("  " + "-" * 74)

    resumen = {}
    for clave in claves:
        suyas = [r for r in resultados if r["version"] == clave]
        sucias = sum(1 for r in suyas if r["rioplatense"])
        pct = sucias / len(suyas) * 100
        bajo, alto = rango(sucias, len(suyas))
        resumen[clave] = {"sucias": sucias, "n": len(suyas),
                          "pct": round(pct, 1), "bajo": round(bajo, 1),
                          "alto": round(alto, 1)}
        print(f"  {clave:<4} {sucias:>2} de {len(suyas):<3} ({pct:>4.1f}%)  "
              f"  entre {bajo:>4.1f}% y {alto:>4.1f}%   {VERSIONES[clave]['nombre']}")

    # ---- la comparacion honesta -----------------------------------------
    print()
    print("-" * 78)
    print("  ¿LAS DIFERENCIAS SON DE VERDAD?")
    print("-" * 78)
    for i, a in enumerate(claves):
        for b in claves[i + 1:]:
            ra, rb = resumen[a], resumen[b]
            solapan = not (ra["alto"] < rb["bajo"] or rb["alto"] < ra["bajo"])
            if solapan:
                print(f"  {a} vs {b}: los rangos se SOLAPAN -> la diferencia "
                      f"no esta demostrada con N={N}.")
            else:
                mejor = a if ra["pct"] < rb["pct"] else b
                print(f"  {a} vs {b}: separados -> {mejor} es mejor de verdad.")

    # ---- la forma verbal, que es donde vive el defecto -------------------
    print()
    print("-" * 78)
    print("  EN QUE FORMA DEL VERBO 'PONER' CAYO CADA VERSION")
    print("-" * 78)
    for clave in claves:
        suyas = [r for r in resultados if r["version"] == clave]
        cuenta = {}
        for r in suyas:
            cuenta[r["forma_verbal"]] = cuenta.get(r["forma_verbal"], 0) + 1
        print(f"  {clave}:")
        for forma, c in sorted(cuenta.items(), key=lambda x: -x[1]):
            print(f"       {forma:<24} {c:>3} de {len(suyas)}  {'#' * c}")

    # ---- entradas y costo ------------------------------------------------
    print()
    print("-" * 78)
    for clave in claves:
        suyas = [r for r in resultados if r["version"] == clave]
        ent = sorted({r["entrada"] for r in suyas})
        print(f"  {clave}: entradas {'identicas' if len(ent) == 1 else 'VARIAS'} "
              f"-> {ent}")
    print("  (entre versiones deben ser distintas: el texto no es el mismo.")
    print("   dentro de cada version deben ser identicas, como siempre.)")

    entrada = sum(r["entrada"] for r in resultados)
    salida = sum(r["salida"] for r in resultados)
    costo = entrada * PRECIO_ENTRADA + salida * PRECIO_SALIDA
    print()
    print("=" * 78)
    print(f"  tokens: {entrada} entrada / {salida} salida")
    print(f"  COSTO REAL: ${costo:.4f}")
    print("=" * 78)

    carpeta = Path(__file__).resolve().parent / "resultados"
    carpeta.mkdir(exist_ok=True)
    sello = datetime.now().strftime("%Y%m%d-%H%M%S")
    archivo = carpeta / f"v3-tres-versiones-{sello}.json"
    archivo.write_text(json.dumps({
        "experimento": "v3 - A control / B prohibicion / C posicion",
        "modelo": MODELO,
        "n_por_version": N,
        "versiones": {k: {"system": v["system"], "usuario": v["usuario"]}
                      for k, v in VERSIONES.items()},
        "resumen": resumen,
        "costo": round(costo, 4),
        "corridas": resultados,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  guardado en: resultados/{archivo.name}")

    print()
    print("  LO PRIMERO QUE HAY QUE MIRAR es la version A.")
    print("  Si A no vuelve a dar cerca del 30% que dio la v2, para y")
    print("  piensa antes de creerle nada a B y C: significaria que algo")
    print("  cambio fuera del experimento.")


if __name__ == "__main__":
    main()
