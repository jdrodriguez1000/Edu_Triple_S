"""avisador.py — E.2 del nivel 8: FALLAR SIN PÚBLICO, y cómo se entera alguien.

    LA FRASE QUE HAY QUE VER

Un fallo mudo a las 3 a.m. no existe hasta la factura.

E.1 dejó el hilo colgando en su escalón 4: `auditar_turnos()` **calcula** el
veredicto `MUDO` —«nadie vino a las 5:00»— y luego lo **imprime**. A nadie. Ese
`print` es el final del camino: el dato existe, es correcto, está calculado, y
**no llega a ninguna persona**.

🔑 EL PROBLEMA DE E.2 NO ES DETECTAR. ES QUE ALGUIEN SE ENTERE.
   Son dos trabajos distintos y el segundo casi nunca se hace.


    LO QUE EL NIVEL YA TENÍA, CONTADO ANTES DE ESCRIBIR ESTO

Del sobre de E.2 (README §E.2), y los seis están contados, no recordados:

    | # | Qué se contó                          | Cuánto salió              |
    |---|---------------------------------------|---------------------------|
    | 1 | canales de aviso en los 20 `.py`      | CERO                      |
    | 2 | `print(` / `import logging`           | 1 108 / CERO              |
    | 3 | usos de `sys.stderr`                  | 4, y los 4 para CALLARLO  |
    | 4 | convenciones de «¿falló?» en 10 suites| TRES, dos invertidas      |
    | 5 | campos que dicen gravedad en 1 468    | NINGUNO                   |
    | 6 | renglones que ya gritan               | 163, y nadie los ha oído  |

⚠️ El hecho 6 es el que hace este archivo. **No falta el dato.** Los 163
   renglones llevan días en el disco, escritos, correctos, legibles. Lo que
   falta es alguien que los mire — y, en cuanto se pone a alguien a mirarlos,
   aparece el problema de verdad, que es el escalón 1.


    LO QUE MIDE EL ESCALÓN 1 (el ingenuo)

`avisar_ingenuo()` es el avisador que escribe todo el mundo la primera vez:
recorre el registro, y **cada renglón que pinta mal manda un aviso**. Una regla,
tres condiciones, ocho líneas. Funciona a la primera.

Y esa es exactamente la trampa: **funciona**. Manda sus avisos, no se cae, las
pruebas salen verdes. Para saber que no sirve hay que contarlos y luego
preguntarse, uno por uno, **cuál de ellos era una noticia**.

🔑 UN AVISADOR NO SE JUZGA POR LOS AVISOS QUE MANDA. SE JUZGA POR LOS QUE
   ALGUIEN HABRÍA QUERIDO RECIBIR.

📌 Y el canal aquí es un archivo, no un correo. Es la regla escrita en el sobre
   («no se manda un aviso de verdad a ningún sitio») y no es pereza: la apuesta
   6 dice que todo lo medible hoy va a ser sobre el **emisor** y nada sobre el
   **receptor**. Mandar un correo de verdad no mediría ni un dato más — solo
   haría que pareciera que sí.
"""

import json
import sys
import tempfile
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # la consola de Windows no habla emoji sin esto
# 📌 Va AQUÍ, al importar, y no dentro de `__main__`: esa es la deuda que E.1
#    dejó abierta en `skills_compartidas.py:586` — importar el módulo y llamar a
#    `_pruebas()` reventaba con el primer emoji.

RUTA_NIVEL = Path(__file__).resolve().parent


# ---------------------------------------------------------------------------
# 1) LEER LO QUE YA ESTÁ ESCRITO
# ---------------------------------------------------------------------------
#
# 🔒 Estos ocho archivos NO se tocan. Son la prueba de los hechos 5 y 6 del
#    sobre: si hoy les añado el campo `gravedad` que les falta, borro la
#    evidencia de que faltaba.

def registros_del_nivel():
    """Los ocho `registro_*.jsonl` que ya existen, en orden."""
    return sorted(RUTA_NIVEL.glob("registro_*.jsonl"))


def renglones(rutas=None):
    """Cada renglón legible, con su archivo y su número de línea al lado.

    📌 Los renglones ilegibles se saltan **en silencio**, y es el primer sitio
       donde este archivo comete el pecado que viene a estudiar. Está a
       propósito: el escalón 3 vuelve aquí.
    """
    for ruta in (rutas if rutas is not None else registros_del_nivel()):
        ruta = Path(ruta)
        if not ruta.exists():
            continue
        for n, linea in enumerate(ruta.read_text(encoding="utf-8").splitlines(), 1):
            if not linea.strip():
                continue
            try:
                yield ruta.name, n, json.loads(linea)
            except json.JSONDecodeError:
                continue


# ---------------------------------------------------------------------------
# 2) LA REGLA INGENUA — la que se le ocurre a cualquiera, y a mí el primero
# ---------------------------------------------------------------------------
#
# Tres condiciones. Ninguna es tonta:
#
#   · `ok is False`        → el propio worker declaró que terminó mal
#   · `contrato_discrepa`  → lo que volvió no era lo que se pidió (A.3)
#   · `sin_trozo`          → una respuesta llegó sin la parte que se esperaba
#
# 🔑 Fíjate en que NO estoy inventando la regla para que salga mal. Es la que
#    yo escribiría de verdad, y las tres condiciones son las únicas señales de
#    problema que el registro sabe dar: el hecho 5 dice que no hay ningún campo
#    de gravedad, así que hay que deducirla del evento.

EVENTOS_QUE_PINTAN_MAL = ("contrato_discrepa", "sin_trozo")


def pinta_mal(d):
    """La regla ingenua, entera. Ocho líneas y funciona a la primera."""
    if d.get("ok") is False:
        return "ok=False"
    if d.get("evento") in EVENTOS_QUE_PINTAN_MAL:
        return d["evento"]
    return None


# ---------------------------------------------------------------------------
# 3) EL CANAL — un archivo, y se dice por qué
# ---------------------------------------------------------------------------

class CanalDeArchivo:
    """El destinatario. Guarda cada aviso y sabe cuántos lleva.

    ⭐ Un canal de verdad —correo, Slack, un busca— cambia SOLO el método
       `mandar`. Todo lo demás de este archivo seguiría igual, y esa es la
       apuesta 1: el canal es la parte barata.
    """

    def __init__(self, carpeta):
        self.ruta = Path(carpeta) / "avisos.jsonl"
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        self.mandados = 0

    def mandar(self, asunto, cuerpo):
        self.mandados += 1
        linea = {
            "hora": datetime.now(timezone.utc).isoformat(),
            "asunto": asunto,
            "cuerpo": cuerpo,
        }
        with open(self.ruta, "a", encoding="utf-8") as f:
            f.write(json.dumps(linea, ensure_ascii=False) + "\n")

    def leidos(self):
        if not self.ruta.exists():
            return []
        return [json.loads(l) for l in self.ruta.read_text(encoding="utf-8").splitlines() if l.strip()]


def avisar_ingenuo(canal, rutas=None):
    """EL ESCALÓN 1 ENTERO. Un renglón malo, un aviso.

    Devuelve la cuenta por motivo, para poder enseñarla.
    """
    cuenta = Counter()
    for archivo, n, d in renglones(rutas):
        motivo = pinta_mal(d)
        if motivo is None:
            continue
        cuenta[motivo] += 1
        canal.mandar(
            asunto=f"[{motivo}] {d.get('evento')} en {archivo}:{n}",
            cuerpo=json.dumps(d, ensure_ascii=False)[:300],
        )
    return cuenta


# ---------------------------------------------------------------------------
# 4) LA PREGUNTA QUE NINGÚN AVISADOR SE HACE: ¿CUÁL DE ESTOS ERA NOTICIA?
# ---------------------------------------------------------------------------
#
# 🚨 Y aquí hay que ser honesto con el instrumento: esta clasificación **no la
#    saca de un campo**, porque el campo no existe (hecho 5). La saco YO,
#    leyendo el README del nivel y sabiendo de dónde vino cada renglón.
#
#    Eso NO es una trampa escondida: es justamente el hallazgo. **El único que
#    sabe si un renglón era noticia es alguien que ya sabía la respuesta**, y
#    ese alguien es el que no va a estar despierto a las 3 de la mañana.

ORIGEN = {
    "registro_pruebas_gratis.jsonl":
        ("PRUEBAS", "lo escribieron las suites del nivel; el nombre del archivo lo dice"),
    "registro_workers_claude-haiku-4-5.jsonl":
        ("EXPERIMENTO", "el freno de presupuesto del bloque C, provocado y documentado"),
    "registro_orquestador_claude-haiku-4-5.jsonl":
        ("EXPERIMENTO", "el contrato de A.3 y los trozos de C.4, provocados y documentados"),
}


def origen_de(archivo):
    """De dónde salió el renglón. 'NOTICIA' sería el que nadie esperaba."""
    return ORIGEN.get(archivo, ("NOTICIA", "nadie ha explicado este todavía"))


def clasificar_avisos(rutas=None):
    """Cada aviso del escalón 1, repartido por origen."""
    por_origen = Counter()
    detalle = Counter()
    for archivo, n, d in renglones(rutas):
        motivo = pinta_mal(d)
        if motivo is None:
            continue
        clase, _ = origen_de(archivo)
        por_origen[clase] += 1
        detalle[(archivo, motivo)] += 1
    return por_origen, detalle


# ---------------------------------------------------------------------------
# 5) EL INFORME DEL ESCALÓN 1
# ---------------------------------------------------------------------------

def informe_escalon_1():
    """La tabla que cobra la apuesta 2 con el número delante."""
    print("\n" + "=" * 78)
    print("E.2 · ESCALÓN 1 — EL AVISADOR INGENUO")
    print("=" * 78)

    archivos = registros_del_nivel()
    total = sum(1 for _ in renglones())
    print(f"\n  Se leen los {len(archivos)} registros del nivel: {total} renglones.")
    print("  Ninguno se modifica. La regla son ocho líneas y funciona a la primera.\n")

    canal = CanalDeArchivo(tempfile.mkdtemp())
    cuenta = avisar_ingenuo(canal)

    print(f"  {'motivo del aviso':<24} {'avisos':>8}")
    print("  " + "-" * 34)
    for motivo, n in cuenta.most_common():
        print(f"  {motivo:<24} {n:>8}")
    print("  " + "-" * 34)
    print(f"  {'TOTAL':<24} {canal.mandados:>8}")

    print(f"\n  🔔 {canal.mandados} avisos. Si el canal fuera un teléfono, son")
    print(f"     {canal.mandados} llamadas. El avisador funcionó: mandó todo lo que dijo")
    print("     que iba a mandar, no se cayó, y las pruebas salen verdes.")

    por_origen, detalle = clasificar_avisos()
    print("\n  Ahora la pregunta que ningún avisador se hace — ¿cuál era NOTICIA?\n")
    print(f"  {'origen':<14} {'avisos':>7}   por qué")
    print("  " + "-" * 76)
    porques = {
        "PRUEBAS": "lo escribieron las suites del nivel al correr",
        "EXPERIMENTO": "fallo provocado a propósito, con su resultado ya escrito",
        "NOTICIA": "nadie lo esperaba — ESTE sí habría que mandarlo",
    }
    for clase in ("PRUEBAS", "EXPERIMENTO", "NOTICIA"):
        print(f"  {clase:<14} {por_origen.get(clase, 0):>7}   {porques[clase]}")

    utiles = por_origen.get("NOTICIA", 0)
    ruido = canal.mandados - utiles
    pct = (100.0 * ruido / canal.mandados) if canal.mandados else 0.0
    print(f"\n  ⭐ FALSOS POSITIVOS: {ruido} de {canal.mandados} = {pct:.1f} %")

    print("\n  Y el reparto por archivo, que es donde está lo incómodo:\n")
    print(f"  {'archivo':<46} {'motivo':<20} {'n':>4}")
    print("  " + "-" * 76)
    for (archivo, motivo), n in sorted(detalle.items()):
        print(f"  {archivo:<46} {motivo:<20} {n:>4}")

    prue = sum(n for (a, _), n in detalle.items() if a == "registro_pruebas_gratis.jsonl")
    print(f"\n  🚨 {prue} de los {canal.mandados} ({100.0 * prue / canal.mandados:.0f} %) salen de UN archivo,")
    print("     y el archivo se llama `registro_pruebas_gratis.jsonl`.")
    print("     El filtro obvio —«ignora ese archivo»— es UNA línea y mata el 95 %.")
    print("     🔑 Y no sirve, por un motivo que el escalón 2 mide: ese filtro no")
    print("        lee un campo, lee un NOMBRE DE ARCHIVO. Ningún renglón dice de")
    print("        sí mismo «soy una prueba». La separación es un accidente de")
    print("        cómo se guardó, no una propiedad de lo que se guardó.")
    return canal.mandados, utiles


# ---------------------------------------------------------------------------
# 6) EL ESCALÓN 2 — ¿QUIÉN DECLARA LA GRAVEDAD?
# ---------------------------------------------------------------------------
#
# El escalón 1 acabó con un empate incómodo:
#
#   · el filtro por nombre de archivo mata el 95 % del ruido con UNA línea
#   · y no sirve, porque lee un accidente de cómo se guardó, no un dato
#
# La salida parece obvia: **que el renglón diga de sí mismo si es grave**. Y lo
# es. Pero antes hay una pregunta que decide el diseño entero:
#
#     ¿QUIÉN LO SABE? ¿EL QUE ESCRIBE O EL QUE LEE?
#
# 🔑 Y la respuesta no se puede negociar: **el que lee NUNCA puede saberlo.**
#    Un `ok:False` con motivo `presupuesto` es idéntico renglón por renglón
#    cuando lo provocó una prueba y cuando arruinó la corrida de un cliente.
#    No se distinguen porque **no son distintos**: lo distinto es el mundo
#    alrededor, y de ese mundo solo tiene noticia el que estaba dentro.
#
# ⭐ LA GRAVEDAD NO ES UNA PROPIEDAD DEL RENGLÓN. ES UNA PROPIEDAD DEL MOMENTO
#    EN QUE SE ESCRIBIÓ — y por eso solo se puede escribir ENTONCES, nunca
#    deducir DESPUÉS.
#
# ⚠️ Y de ahí sale la consecuencia cara, que es `LM.65` otra vez: **los 1 468
#    renglones que ya están pagados no van a tener este campo jamás.** No es que
#    sea trabajoso añadírselo: es que añadírselo sería inventármelo.

ENTORNOS = ("produccion", "experimento", "prueba")


def marca_de_entorno(entorno):
    """Lo que el que ESCRIBE añade a cada renglón suyo. Un campo, un valor.

    📌 Tan pequeño que da vergüenza, y es justo la pieza que faltaba en los ocho
       registros del nivel.
    """
    if entorno not in ENTORNOS:
        raise ValueError(f"entorno desconocido: {entorno!r} — los válidos son {ENTORNOS}")
    return {"entorno": entorno}


def merece_aviso(d):
    """La regla del escalón 2: pinta mal **Y** venía de producción.

    🔑 Fíjate en lo poco que cambia y en lo mucho que decide: es la MISMA regla
       del escalón 1 con una condición más. Lo caro no fue escribirla — fue que
       alguien, en otro archivo y en otro momento, hubiera escrito el campo.
    """
    motivo = pinta_mal(d)
    if motivo is None:
        return None
    if d.get("entorno") != "produccion":
        return None
    return motivo


def grabar_demo_e2(carpeta):
    """Un registro FABRICADO con el campo que a los de verdad les falta.

    🚨 Y hay que decir en voz alta lo que esto es y lo que no es:

       · el escalón 1 se midió sobre **1 468 renglones REALES y pagados**
       · el escalón 2 se mide sobre **50 renglones que me acabo de inventar**

       No hay alternativa honesta —el campo no existe en ninguno de los
       pagados—, pero la diferencia de peso entre las dos mediciones es enorme y
       no se disimula. Los números de aquí abajo enseñan un MECANISMO; los de
       arriba eran un HECHO.
    """
    ruta = Path(carpeta) / "registro_demo_e2.jsonl"
    ruta.parent.mkdir(parents=True, exist_ok=True)
    lineas = []

    # 40 renglones de la suite de pruebas: 30 de ellos pintan mal, y está bien
    # que pinten mal — la suite existe justamente para provocarlos.
    for i in range(40):
        d = {"hora": f"2026-08-24T01:{i:02d}:00+00:00", "evento": "worker_fin",
             "worker": "prueba", "ok": i >= 30, "motivo": "presupuesto"}
        d.update(marca_de_entorno("prueba"))
        lineas.append(d)

    # 10 renglones de producción: dos salieron mal, y son LOS DOS que alguien
    # habría querido que le despertaran.
    for i in range(10):
        d = {"hora": f"2026-08-24T03:{i:02d}:00+00:00", "evento": "worker_fin",
             "worker": "eur", "ok": i not in (3, 7), "motivo": "presupuesto"}
        d.update(marca_de_entorno("produccion"))
        lineas.append(d)

    with open(ruta, "w", encoding="utf-8") as f:
        for d in lineas:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    return ruta


def informe_escalon_2():
    """La misma regla, con y sin el campo. Y el precio de haberlo escrito tarde."""
    print("\n" + "=" * 78)
    print("E.2 · ESCALÓN 2 — QUIÉN DECLARA LA GRAVEDAD")
    print("=" * 78)

    carpeta = Path(tempfile.mkdtemp())
    ruta = grabar_demo_e2(carpeta)
    todos = list(renglones([ruta]))

    ingenuos = [d for _, _, d in todos if pinta_mal(d)]
    filtrados = [d for _, _, d in todos if merece_aviso(d)]

    print(f"\n  Un registro fabricado: {len(todos)} renglones, y esta vez CADA UNO")
    print("  lleva un campo `entorno` que el que lo escribió puso al escribirlo.\n")
    print(f"  {'regla':<44} {'avisos':>7}   quién duerme")
    print("  " + "-" * 76)
    print(f"  {'escalón 1 — «pinta mal»':<44} {len(ingenuos):>7}   nadie")
    print(f"  {'escalón 2 — «pinta mal Y es producción»':<44} {len(filtrados):>7}   casi todos")

    print(f"\n  ⭐ {len(ingenuos)} → {len(filtrados)}. La regla creció UNA condición.")
    print("     Y los dos que quedan son exactamente los dos que alguien habría")
    print("     querido que le despertaran. Falsos positivos: 0.")

    print("\n  🚨 PERO EL TRABAJO NO ESTUVO EN LA REGLA, Y ESTE ES EL PUNTO:")
    print("     `merece_aviso()` son 6 líneas. El campo `entorno` lo tiene que")
    print("     escribir OTRO archivo, en OTRO momento, y en TODOS sus renglones.")
    print("     Uno solo que se olvide vuelve invisible lo que pasó ahí.")
    print("     🔑 El que lee no puede arreglar lo que el que escribe no dijo.")

    print("\n  ⚠️ Y el precio de haberlo entendido tarde, con el número al lado:")
    reales = sum(1 for _ in renglones())
    print(f"     los {reales} renglones ya pagados del nivel NO tienen `entorno`,")
    print("     y no se lo puedo poner hoy sin inventármelo. La gravedad se")
    print("     escribe en el momento o no se escribe nunca — es `LM.65`.")
    return len(ingenuos), len(filtrados)


# ---------------------------------------------------------------------------
# 7) EL ESCALÓN 3 — EL FALLO QUE NO ESCRIBE NINGÚN RENGLÓN
# ---------------------------------------------------------------------------
#
# El escalón 2 dejó la regla afinada: 32 → 2, cero falsos positivos. Parece
# terminado.
#
# 🚨 Y falta el fallo que importa. Los dos escalones anteriores leen renglones,
#    y por buenos que se pongan **solo pueden avisar de cosas que ESCRIBIERON un
#    renglón**. El turno que no se disparó no escribió ninguno.
#
# Es la apuesta 3 del sobre, y es la apuesta 4 de E.1 cobrada en la pieza
# siguiente: `disparador.py` ya calculaba el veredicto `MUDO` y ya sabía que
# necesitaba **el calendario**, que es un dato de otra naturaleza: lo escribe el
# que PROMETIÓ, no el que trabajó.

import disparador  # noqa: E402  — se importa aquí para que se lea al lado de lo que usa


def avisar_de_los_mudos(canal, carpeta, desde, hasta, cada_horas=1):
    """El aviso que NO se puede sacar del registro. Necesita dos entradas.

    · `carpeta` → lo que escribió el que trabajó (marcas e intentos)
    · `desde/hasta` → lo que prometió el calendario

    🔑 Y de aquí sale la consecuencia incómoda que se apostó: **este avisador no
       puede vivir dentro del proceso que vigila.** El que se murió a las 3:04
       no va a mandar el aviso de que se murió a las 3:04.
    """
    r = disparador.auditar_turnos(carpeta, desde, hasta, cada_horas)
    for turno, veredicto in r["por_turno"].items():
        if veredicto == "MUDO":
            canal.mandar(asunto=f"[MUDO] el turno {turno} no lo intentó NADIE",
                         cuerpo="ni marca ni intento: no hay renglón que consultar")
    return r


def informe_escalon_3():
    """Las dos entradas, y qué ve cada avisador con cada una."""
    print("\n" + "=" * 78)
    print("E.2 · ESCALÓN 3 — EL FALLO QUE NO ESCRIBE NINGÚN RENGLÓN")
    print("=" * 78)

    carpeta = Path(tempfile.mkdtemp())
    dia = datetime(2026, 8, 24, 3, 0, tzinfo=timezone.utc)
    t3, t4, t5 = (disparador.turno_de(dia + timedelta(hours=h)) for h in (0, 1, 2))

    # 03:00 salió bien · 04:00 vinieron dos y ninguno pudo · 05:00 NADIE VINO
    disparador.marcar_turno(carpeta, t3)
    disparador.anotar_intento(carpeta, t3, "d0", "hizo")
    disparador.anotar_intento(carpeta, t4, "d0", "fallo")
    disparador.anotar_intento(carpeta, t4, "d1", "cedio")

    print("\n  La misma noche del escalón 4 de E.1. Tres turnos.\n")

    canal_reg = CanalDeArchivo(Path(tempfile.mkdtemp()))
    intentos = disparador.intentos_de(carpeta)
    for d in intentos:
        if d["veredicto"] in ("fallo", "cedio"):
            canal_reg.mandar(f"[{d['veredicto']}] turno {d['turno']}", json.dumps(d))

    canal_cal = CanalDeArchivo(Path(tempfile.mkdtemp()))
    r = avisar_de_los_mudos(canal_cal, carpeta, dia, dia + timedelta(hours=2))

    print(f"  {'avisador':<40} {'entradas':>10} {'avisos':>8}")
    print("  " + "-" * 62)
    print(f"  {'lee el registro (escalones 1 y 2)':<40} {'1':>10} {canal_reg.mandados:>8}")
    print(f"  {'lee registro + CALENDARIO':<40} {'2':>10} {canal_cal.mandados:>8}")

    print("\n  Los dos aciertan en lo suyo. Mira QUÉ turno ve cada uno:\n")
    print(f"  {'turno':<20} {'veredicto':>12}   ¿lo avisó el que solo lee el registro?")
    print("  " + "-" * 76)
    for t, v in r["por_turno"].items():
        visto = "sí" if any(d["turno"] == t for d in intentos) else "NO — no hay renglón"
        print(f"  {t:<20} {v:>12}   {visto}")

    print("\n  🔑 EL MUDO NO ES INVISIBLE POR DESCUIDO DEL REGISTRO. LO ES POR")
    print("     CONSTRUCCIÓN: el que no corre no escribe, y un lector de renglones")
    print("     no puede leer el renglón que nadie escribió.")
    print("\n  ⭐ Por eso hacen falta dos entradas de naturaleza distinta:")
    print("     el registro lo escribe EL QUE TRABAJA — dice lo que SÍ pasó.")
    print("     el calendario lo escribe EL QUE PROMETIÓ — dice lo que DEBÍA pasar.")
    print("     Ningún volumen de la primera produce la segunda.")
    print("\n  🚨 Y la consecuencia que decide dónde vive el código:")
    print("     ESTE AVISADOR NO PUEDE CORRER DENTRO DEL PROCESO QUE VIGILA.")
    print("     El que se murió a las 3:04 no manda el aviso de que se murió.")
    return canal_reg.mandados, canal_cal.mandados


# ---------------------------------------------------------------------------
# 8) EL ESCALÓN 4 — EL AVISADOR TIENE EL MISMO BICHO QUE VIGILA
# ---------------------------------------------------------------------------
#
# Los tres escalones anteriores dan por hecho algo que nadie comprueba: **que el
# aviso llega**. Un canal de verdad es una red, y una red se cae.
#
# Y entonces pasa lo que pasa siempre, porque el código que lo provoca lo
# escribe todo el mundo y parece prudente:
#
#       try:
#           canal.mandar(...)
#       except Exception:
#           pass          # ← «que un fallo del aviso no tumbe el trabajo»
#
# 🚨 La intención es correcta. El resultado es que **el que vigila el silencio
#    se queda en silencio**, y no deja ni un rastro de haberse quedado.
#
# 📌 Y no es un hombre de paja: `anotar_intento()` en `disparador.py:1035` tiene
#    ese `except: pass` desde ayer, escrito por mí, con su comentario explicando
#    por qué. Allí está bien puesto — aquí es el bicho entero.

class CanalCaido(CanalDeArchivo):
    """El mismo canal, con la red caída. Lo único que cambia es `mandar`."""

    def mandar(self, asunto, cuerpo):
        raise ConnectionError("no hay red")


def avisar_como_todo_el_mundo(canal, rutas):
    """La versión prudente. Devuelve cuántos avisos MANDÓ.

    ⚠️ Fíjate en lo que devuelve y en lo que NO: devuelve los que mandó. Nadie
       le pregunta por los que no pudo mandar, porque no los cuenta.
    """
    mandados = 0
    for _, _, d in renglones(rutas):
        if merece_aviso(d):
            try:
                canal.mandar("aviso", json.dumps(d, ensure_ascii=False))
                mandados += 1
            except Exception:
                pass
    return mandados


# ---------------------------------------------------------------------------
# EL LATIDO — y por qué NO es «otro try»
# ---------------------------------------------------------------------------
#
# La reacción natural al descubrir lo de arriba es envolverlo en otro `try` que
# avise de que el aviso falló. Y no puede funcionar, por un motivo de forma y no
# de esfuerzo: **ese segundo aviso viaja por el mismo canal caído**.
#
# ⭐ LA ALARMA LA MANDA EL QUE FALLA. EL LATIDO LO ECHA DE MENOS EL QUE ESCUCHA.
#
#    | pieza    | quién actúa      | qué pasa si el que falla está muerto |
#    |----------|------------------|--------------------------------------|
#    | alarma   | el que falla     | no la manda — silencio               |
#    | latido   | el que ESCUCHA   | lo echa de menos — ruido             |
#
# 🔑 Es exactamente el mecanismo del escalón 3 aplicado al propio avisador: se
#    comprueba una AUSENCIA contra algo prometido de antemano. El calendario
#    prometía un turno; el latido promete un ritmo.

ARCHIVO_LATIDO = "latido.json"


def latir(carpeta, revisados, mandados, fallos_envio, ahora=None):
    """El avisador deja constancia de su propia ronda. Y CUENTA LO QUE NO PUDO.

    🚨 El campo `fallos_envio` es la mitad que casi nadie escribe, y sin ella el
       latido MIENTE: un latido que dice «vivo» pase lo que pase es un
       `except: pass` con mejor prensa.
    """
    ruta = Path(carpeta) / ARCHIVO_LATIDO
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps({
        "hora": (ahora or datetime.now(timezone.utc)).isoformat(),
        "revisados": revisados,
        "mandados": mandados,
        "fallos_envio": fallos_envio,
    }, ensure_ascii=False), encoding="utf-8")
    return ruta


def avisar_con_latido(canal, rutas, carpeta_latido, ahora=None):
    """Igual que el de arriba, pero contando lo que NO pudo mandar."""
    revisados = mandados = fallos_envio = 0
    for _, _, d in renglones(rutas):
        revisados += 1
        if merece_aviso(d):
            try:
                canal.mandar("aviso", json.dumps(d, ensure_ascii=False))
                mandados += 1
            except Exception:
                fallos_envio += 1
    latir(carpeta_latido, revisados, mandados, fallos_envio, ahora)
    return mandados, fallos_envio


def echa_de_menos(carpeta_latido, ahora, tolerancia_s):
    """EL QUE ESCUCHA. Devuelve la queja, o `None` si todo va bien.

    Dos quejas distintas, y confundirlas es perder la mitad:

        · «no late»   → hace más de `tolerancia_s` que no escribe. Está muerto,
                        colgado, o nadie lo arrancó. **No hay dato: hay ausencia.**
        · «late mal»  → sí escribe, pero confiesa envíos fallidos. Está vivo y
                        no está sirviendo para nada.

    🔑 La primera es la que ningún avisador se hace a sí mismo, porque para
       hacérsela hay que estar FUERA.
    """
    ruta = Path(carpeta_latido) / ARCHIVO_LATIDO
    if not ruta.exists():
        return "no late: nunca ha latido — ¿alguien lo arrancó?"
    d = json.loads(ruta.read_text(encoding="utf-8"))
    edad = (ahora - datetime.fromisoformat(d["hora"])).total_seconds()
    if edad > tolerancia_s:
        return f"no late: el último latido tiene {edad:.0f} s (tolerancia {tolerancia_s:.0f} s)"
    if d.get("fallos_envio", 0) > 0:
        return f"late mal: vivo, pero {d['fallos_envio']} avisos no salieron"
    return None


def informe_escalon_4():
    """El canal caído, con las dos versiones al lado."""
    print("\n" + "=" * 78)
    print("E.2 · ESCALÓN 4 — EL AVISADOR QUE FALLA MUDO")
    print("=" * 78)

    carpeta = Path(tempfile.mkdtemp())
    ruta = grabar_demo_e2(carpeta)
    ahora = datetime(2026, 8, 24, 3, 0, tzinfo=timezone.utc)

    print("\n  Los mismos 50 renglones del escalón 2. Dos de ellos merecen aviso.")
    print("  Y esta vez la red está caída.\n")

    caido = CanalCaido(tempfile.mkdtemp())
    mandados = avisar_como_todo_el_mundo(caido, [ruta])

    print(f"  {'versión':<34} {'avisos':>7} {'errores':>8} {'rastro':>9}")
    print("  " + "-" * 62)
    print(f"  {'con `except: pass`':<34} {mandados:>7} {0:>8} {'NINGUNO':>9}")

    caido2 = CanalCaido(tempfile.mkdtemp())
    lat = Path(tempfile.mkdtemp())
    m2, f2 = avisar_con_latido(caido2, [ruta], lat, ahora)
    print(f"  {'con latido':<34} {m2:>7} {0:>8} {'latido.json':>9}")

    print("\n  🚨 Las DOS mandan cero avisos y las DOS terminan sin un error.")
    print("     El proceso sale con código 0. La pantalla no dice nada. Y los")
    print("     dos fallos de producción de las 3:00 siguen ahí sin que nadie")
    print("     los sepa. El avisador no se rompió: se CALLÓ.")

    print("\n  La diferencia está en lo que quedó escrito. Lo que ve el que escucha:\n")
    queja = echa_de_menos(lat, ahora, tolerancia_s=3600)
    vacio = echa_de_menos(Path(tempfile.mkdtemp()), ahora, tolerancia_s=3600)
    tarde = echa_de_menos(lat, ahora + timedelta(hours=3), tolerancia_s=3600)
    print(f"  {'situación':<34} qué dice el que escucha")
    print("  " + "-" * 76)
    print(f"  {'el que usa `except: pass`':<34} {vacio}")
    print(f"  {'el del latido, red caída':<34} {queja}")
    print(f"  {'el del latido, 3 h sin correr':<34} {tarde}")

    print("\n  ⭐ Y fíjate en la tercera fila, que es la que cierra E.1:")
    print("     el avisador que NO CORRIÓ produce una queja sin haber escrito")
    print("     nada. Es el `MUDO` del escalón 3 aplicado al vigilante — se")
    print("     comprueba una AUSENCIA contra un ritmo prometido de antemano.")

    print("\n  🔑 LA ALARMA LA MANDA EL QUE FALLA; EL LATIDO LO ECHA DE MENOS EL")
    print("     QUE ESCUCHA. Por eso el segundo `try` no arregla nada: viajaría")
    print("     por el mismo canal caído.")

    print("\n  ⚠️ Y lo que ESTO no arregla, dicho aquí y no escondido: alguien")
    print("     tiene que escuchar el latido, y ese alguien puede callarse")
    print("     también. La cadena no se cierra con más código — termina fuera,")
    print("     en algo que no controlas: una persona, o un servicio que pagas")
    print("     precisamente para que grite. Cada capa mueve el silencio un")
    print("     escalón hacia arriba; ninguna lo borra.")
    return mandados, f2


# ---------------------------------------------------------------------------
# 9) EL ESCALÓN 5 — EL AVISO QUE YA EXISTÍA Y SE TIRABA A LA BASURA
# ---------------------------------------------------------------------------
# EL DETECTOR QUE SOBREVIVE AL ARREGLO
# ---------------------------------------------------------------------------
#
# 🚨 En cuanto se arregla `disparador.py`, la prueba que midió el agujero se
#    pone roja: medía que salía 0, y ya no sale 0. **Una prueba que describe el
#    estado roto muere el día que lo arreglas**, y lo que queda es una anécdota
#    en un README.
#
# ⭐ Lo que sí sobrevive es un detector de la FORMA del bicho, no de su caso:
#    *«¿hay algún módulo cuyo `__main__` llame a sus pruebas y tire el
#    resultado?»*. Ese se puede correr mañana, sobre archivos que todavía no
#    existen, y encuentra al siguiente.
#
# 🔑 ES LA DIFERENCIA ENTRE ARREGLAR UN FALLO Y CERRAR UNA CLASE DE FALLOS.

import ast


def tira_el_resultado_de_sus_pruebas(ruta):
    """¿El `__main__` de este archivo llama a `_pruebas()` y descarta el valor?

    Se lee con `ast`, no con `grep`: lo que importa no es que el nombre
    aparezca, sino **en qué posición** aparece. `_pruebas()` a solas es una
    sentencia y su valor se pierde; dentro de un `sys.exit(...)` no.
    """
    arbol = ast.parse(Path(ruta).read_text(encoding="utf-8"))
    for nodo in arbol.body:
        if not (isinstance(nodo, ast.If) and "__main__" in ast.unparse(nodo.test)):
            continue
        for hijo in ast.walk(nodo):
            # una llamada cuyo valor NO se usa es una sentencia `Expr`
            if (isinstance(hijo, ast.Expr) and isinstance(hijo.value, ast.Call)
                    and isinstance(hijo.value.func, ast.Name)
                    and hijo.value.func.id in ("_pruebas", "pruebas")):
                return True
    return False


def auditar_codigos_de_salida():
    """Los módulos del nivel que tienen suite, y qué hacen con su resultado."""
    salida = {}
    for ruta in sorted(RUTA_NIVEL.glob("*.py")):
        texto = ruta.read_text(encoding="utf-8")
        if "def _pruebas(" not in texto or '__main__' not in texto:
            continue
        salida[ruta.name] = tira_el_resultado_de_sus_pruebas(ruta)
    return salida


# ---------------------------------------------------------------------------
#
# Todo lo anterior construye avisos nuevos. Este escalón no construye nada:
# mira uno que **ya estaba** y que se pierde en la última línea del archivo.
#
# Un proceso automático tiene un canal de aviso que no cuesta nada, que entiende
# cualquier programador de sistemas y que funciona sin red: **el código de
# salida**. 0 es «bien», cualquier otro es «mal». Es lo que mira el que arrancó
# el proceso — el reloj, el `cron`, la nube, el `Makefile`.
#
# 🚨 Y el hecho 3 del sobre dice que `disparador.py` —el módulo del bloque donde
#    NO HAY NADIE MIRANDO— lo tira: `_pruebas()` devuelve la lista de fallos y
#    `__main__` la llama pelada, descartando el valor.
#
# 📌 Cómo se mide, dicho antes de enseñar el número: se copian los módulos a una
#    carpeta temporal, se les fuerza una comprobación en rojo y se lee el código
#    de salida. Se **neutralizan los informes**, que tardan dos minutos y no
#    tienen nada que ver con lo que se mide. Lo único que se está midiendo es la
#    tubería entre `_pruebas()` y el proceso: una línea en cada archivo.
#
# 🔒 Y se mide sobre COPIAS. El original no se toca hasta después del número —
#    es la regla que quedó escrita en el sobre: primero se mide, después se
#    arregla, o el dato se pierde y queda la anécdota.

import re
import shutil
import subprocess


# 🔑 Este diccionario ES el hecho 4 del sobre hecho código: tres convenciones
#    distintas para decir «falló», dos de ellas con la polaridad invertida.
#    Un medidor que no las supiera leería «no falló» donde dice «falló».
DEVUELVEN_LISTA = ("disparador.py", "skills_compartidas.py", "compartida.py",
                   "verificador.py", "avisador.py")


def _copia_con_prueba_rota(modulo):
    """Copia el módulo CON UNA PRUEBA ROTA, sin tocar el original.

    🚨 La copia vive **en la carpeta del nivel**, no en una temporal, y eso lo
       decidió un fallo del medidor y no una preferencia: `router.py` hace
       `sys.path.insert(0, AQUI.parent / "05b-proyecto")`. Desde una carpeta
       temporal ese vecino no existe y la copia muere con `ModuleNotFoundError`
       — código de salida 1 **por el motivo equivocado**, que es exactamente el
       dato falso que este escalón viene a cazar.

    ⚠️ Se borra siempre, en el `finally` de quien la llama.
    """
    ruta = RUTA_NIVEL / f"_medicion_{modulo}"
    s = (RUTA_NIVEL / modulo).read_text(encoding="utf-8")

    # 1) el cuerpo de `_pruebas` se sustituye por uno mínimo que falla siempre,
    #    devolviendo lo que ESE módulo devuelve para decir «falló».
    inicio = s.index("def _pruebas(")
    fin = s.index("\ndef ", inicio + 10)
    devuelve = "['fallo forzado']" if modulo in DEVUELVEN_LISTA else "1"
    cuerpo = (
        "def _pruebas():\n"
        '    print("  XX  FALLO FORZADO para medir el codigo de salida")\n'
        "    return " + devuelve + "\n"
    )
    s = s[:inicio] + cuerpo + s[fin:]

    # 2) los informes tardan minutos y no tienen nada que ver con lo que se
    #    mide. Se sustituyen por `pass` — y NO por un nombre inventado: la
    #    primera versión de esto puso `_nada_` y las copias reventaban con
    #    `NameError`, dando código 1 por el motivo equivocado. **El medidor
    #    tuvo el mismo bicho que venía a medir, y lo cazó pedir el `stderr`.**
    s = re.sub(r"^(\s*)informe_[a-z_0-9]+\(\)", r"\1pass", s, flags=re.M)

    ruta.write_text(s, encoding="utf-8")
    return ruta


def codigo_de_salida_con_prueba_rota(modulo):
    """Corre la copia rota y devuelve (código, última línea del stderr).

    🔑 Devuelve TAMBIÉN el `stderr`, y no es adorno: sin él, un `1` de
       `ModuleNotFoundError` se lee igual que un `1` de «la prueba falló», y las
       dos veces que este medidor se equivocó hoy se leían así.
    """
    ruta = _copia_con_prueba_rota(modulo)
    try:
        r = subprocess.run([sys.executable, str(ruta)],
                           capture_output=True, text=True, timeout=180)
    finally:
        ruta.unlink(missing_ok=True)
    err = r.stderr.strip().splitlines()
    return r.returncode, (err[-1] if err else "")


def informe_escalon_5():
    """Dos módulos del mismo nivel ante el mismo fallo."""
    print("\n" + "=" * 78)
    print("E.2 · ESCALÓN 5 — EL AVISO QUE YA EXISTÍA Y SE TIRABA A LA BASURA")
    print("=" * 78)

    print("\n  A cada módulo se le fuerza UNA comprobación en rojo, sobre una")
    print("  copia, y se lee lo que el proceso le cuenta a quien lo arrancó.\n")

    print(f"  {'módulo':<18} {'última línea de su __main__':<32} {'código':>6}  {'¿reventó?':>10}")
    print("  " + "-" * 74)
    filas = [("disparador.py", "_pruebas()"),
             ("router.py", "sys.exit(main(sys.argv[1:]))")]
    salidas = {}
    for modulo, forma in filas:
        codigo, err = codigo_de_salida_con_prueba_rota(modulo)
        salidas[modulo] = (codigo, err)
        print(f"  {modulo:<18} {forma:<32} {codigo:>6}  {('no' if not err else err[:40]):>10}")

    print("\n  📌 La última columna no es adorno. Las dos primeras versiones de")
    print("     este medidor dieron 1 en los dos módulos, y las dos veces era un")
    print("     reventón —`NameError` y `ModuleNotFoundError`—, no una prueba en")
    print("     rojo. 🔑 UN CÓDIGO 1 NO DICE «FALLÓ LA PRUEBA»: DICE «ALGO PASÓ».")
    print("     El medidor tuvo el mismo bicho que venía a medir, y lo cazó")
    print("     pedirle el `stderr` en vez de creerle el número.")

    print("\n  ⚠️ Y esta tabla YA NO ENSEÑA EL AGUJERO, porque el agujero se")
    print("     arregló hace un rato, en esta misma sesión y después de medirlo.")
    print("     Lo medido, con su fecha, para que no se pierda al arreglarlo:\n")
    print("       2026-08-24, sesión 109, ANTES del arreglo:")
    print("         disparador.py  →  código 0   (`_pruebas()` llamada pelada)")
    print("         router.py      →  código 1   (`sys.exit(main(...))`)")
    print("\n     Mismo nivel, misma mano, la misma semana, el mismo fallo: uno")
    print("     gritaba y el otro decía que todo había ido bien.")
    print("\n  🔑 Y no era un descuido de estilo: `disparador.py` es precisamente")
    print("     el módulo pensado para correr SIN NADIE DELANTE. Sus 67")
    print("     comprobaciones en rojo se imprimían en una pantalla que nadie")
    print("     mira, y lo único que sí llegaba al que lo arrancó —el código de")
    print("     salida— decía 0.")
    print("\n  ⭐ EL AVISO MÁS BARATO DEL MUNDO YA ESTABA AHÍ, y se tiraba en la")
    print("     última línea del archivo. No hacía falta escribir un canal:")
    print("     hacía falta no tirar el que había.")
    print("\n  📌 Que la tabla de arriba diga hoy 1 y 1 es la prueba de que el")
    print("     arreglo entró. Y es también el motivo del apartado siguiente.")

    print("\n  Y como el arreglo mata a la prueba que lo midió, queda el detector")
    print("  de la FORMA del bicho, que sí sobrevive y encuentra al siguiente:\n")
    aud = auditar_codigos_de_salida()
    print(f"  {'módulo con suite':<26} {'¿tira el resultado de sus pruebas?':>36}")
    print("  " + "-" * 64)
    for modulo, tira in sorted(aud.items()):
        print(f"  {modulo:<26} {('SÍ — nadie se entera' if tira else 'no'):>36}")
    rotos = [m for m, t in aud.items() if t]
    print(f"\n  {len(aud)} módulos con suite · {len(rotos)} tiran el resultado: "
          f"{', '.join(rotos) if rotos else 'ninguno'}")
    print("\n  🔑 ES LA DIFERENCIA ENTRE ARREGLAR UN FALLO Y CERRAR UNA CLASE DE")
    print("     FALLOS. El de hoy ya está arreglado; este detector es para el")
    print("     archivo que alguien escriba en la sesión 130.")
    return salidas


# ---------------------------------------------------------------------------
# 10) EL CIERRE — LA APUESTA 1, CONTADA EN VEZ DE OPINADA
# ---------------------------------------------------------------------------
#
# El sobre apostó: *«menos del 10 % del trabajo de E.2 es mandar el aviso»*, y
# lo dejó falsificable con una cuenta — **líneas que EMITEN contra líneas que
# DECIDEN**. Aquí está la cuenta, hecha con `ast` para que no dependa de dónde
# ponga yo los saltos de línea: se cuentan **sentencias ejecutables**, no
# renglones ni comentarios.

EMITEN = [("CanalDeArchivo", "mandar"), ("CanalCaido", "mandar")]

DECIDEN = ["pinta_mal", "merece_aviso", "marca_de_entorno", "origen_de",
           "clasificar_avisos", "avisar_de_los_mudos", "latir",
           "avisar_con_latido", "echa_de_menos",
           "tira_el_resultado_de_sus_pruebas", "auditar_codigos_de_salida"]


def _sentencias(nodo):
    """Cuántas sentencias ejecutables tiene, sin contar su docstring."""
    n = 0
    for hijo in ast.walk(nodo):
        if isinstance(hijo, ast.stmt) and hijo is not nodo:
            if isinstance(hijo, ast.Expr) and isinstance(hijo.value, ast.Constant) \
                    and isinstance(hijo.value.value, str):
                continue  # el docstring
            n += 1
    return n


def contar_emitir_contra_decidir(ruta=None):
    """Devuelve (sentencias que emiten, sentencias que deciden)."""
    arbol = ast.parse(Path(ruta or (RUTA_NIVEL / "avisador.py")).read_text(encoding="utf-8"))
    emiten = decide = 0
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.ClassDef):
            for m in nodo.body:
                if isinstance(m, ast.FunctionDef) and (nodo.name, m.name) in EMITEN:
                    emiten += _sentencias(m)
        elif isinstance(nodo, ast.FunctionDef) and nodo.name in DECIDEN:
            decide += _sentencias(nodo)
    return emiten, decide


def informe_apuesta_1():
    """La apuesta 1, resuelta con una cuenta reproducible."""
    print("\n" + "=" * 78)
    print("E.2 · EL CIERRE — ¿CUÁNTO DEL TRABAJO ERA «MANDAR EL AVISO»?")
    print("=" * 78)

    emiten, decide = contar_emitir_contra_decidir()
    total = emiten + decide
    pct = 100.0 * emiten / total

    print(f"\n  {'parte':<44} {'sentencias':>11} {'%':>7}")
    print("  " + "-" * 64)
    print(f"  {'EMITIR — poner el aviso en el canal':<44} {emiten:>11} {pct:>6.1f}%")
    print(f"  {'DECIDIR — qué, a quién, con qué gravedad, y':<44} {decide:>11} {100 - pct:>6.1f}%")
    print(f"  {'  comprobar que el aviso siquiera salió':<44}")
    print("  " + "-" * 64)
    print(f"  {'TOTAL':<44} {total:>11}")

    print(f"\n  🎲 Se apostó «menos del 10 %», con pronóstico «1 a 10 o peor».")
    print(f"     Sale {pct:.1f} % — {'✅ dentro' if pct < 10 else '🔴 fuera'} de lo apostado.")
    print("\n  ⚠️ Y hay que decir lo que esta cuenta NO es: yo elegí qué funciones")
    print("     van en cada columna, y esa elección la hice después de escribirlas.")
    print("     El reparto está en las listas `EMITEN` y `DECIDEN`, arriba, para")
    print("     que se pueda discutir renglón por renglón en vez de creérselo.")
    print("     🔑 Una cuenta cuyo criterio se puede leer se discute; una")
    print("        impresión, no — y por eso vale más aunque sea discutible.")

    print("\n  ⭐ EL TITULAR: «no tenemos alertas» casi nunca significa que falte")
    print("     el emisor. `mandar()` son nueve renglones y no fue el problema")
    print("     ni una sola vez en los cinco escalones de hoy.")
    return emiten, decide


# ---------------------------------------------------------------------------
# 11) LAS PRUEBAS — todas gratis, sin red, sin modelo
# ---------------------------------------------------------------------------

def _pruebas():
    fallos = []

    def check(nombre, cond, detalle=""):
        print(("  OK  " if cond else "  XX  ") + nombre + (f"  -> {detalle}" if detalle else ""))
        if not cond:
            fallos.append(nombre)

    print("\n[E.2 · escalón 1] el avisador ingenuo\n")

    # --- P1-P4: la regla, sola ---------------------------------------------
    check("P1 · un renglón con ok=False pinta mal", pinta_mal({"ok": False}) == "ok=False")
    check("P2 · uno con ok=True NO pinta mal", pinta_mal({"ok": True, "evento": "worker_fin"}) is None)
    check("P3 · `contrato_discrepa` pinta mal aunque no lleve `ok`",
          pinta_mal({"evento": "contrato_discrepa"}) == "contrato_discrepa")
    check("P4 · 🚨 y un renglón NORMAL tampoco pinta mal — que es la mitad que se olvida",
          pinta_mal({"evento": "llamada_api", "costo_usd": 0.001}) is None)

    # --- P5-P7: el canal ----------------------------------------------------
    c = CanalDeArchivo(tempfile.mkdtemp())
    c.mandar("asunto", "cuerpo")
    c.mandar("otro", "cuerpo")
    check("P5 · el canal cuenta lo que manda", c.mandados == 2, c.mandados)
    check("P6 · y lo deja escrito, no solo contado", len(c.leidos()) == 2, len(c.leidos()))
    check("P7 · con su hora, que es lo primero que se pregunta al recibirlo",
          "hora" in c.leidos()[0])

    # --- P8-P11: sobre los registros de verdad -----------------------------
    total = sum(1 for _ in renglones())
    check("P8 · los ocho registros del nivel se leen enteros", total == 1468, total)

    c2 = CanalDeArchivo(tempfile.mkdtemp())
    cuenta = avisar_ingenuo(c2)
    check("P9 · 🎲 LA APUESTA 2, primera mitad: la regla ingenua manda 163 avisos",
          c2.mandados == 163, c2.mandados)
    check("P10 · y salen de las tres condiciones, no de una sola",
          set(cuenta) == {"ok=False", "contrato_discrepa", "sin_trozo"}, dict(cuenta))

    por_origen, _ = clasificar_avisos()
    check("P11 · 🎲 LA APUESTA 2, la mitad que importa: NI UNO era noticia",
          por_origen.get("NOTICIA", 0) == 0, dict(por_origen))
    check("P12 · y el 95 % sale de un solo archivo, el de las pruebas",
          por_origen.get("PRUEBAS", 0) == 155, por_origen.get("PRUEBAS", 0))

    # --- P13: el control, que es lo que separa medir de confirmar ----------
    #     Si la regla marcara TODO, los números de arriba saldrían igual de
    #     redondos y no dirían nada. Esta prueba exige que la regla DEJE PASAR
    #     la inmensa mayoría de los renglones.
    check("P13 · 🔑 el control: la regla deja pasar el 89 % de los renglones",
          0.10 < (163 / total) < 0.12, f"{163 / total:.3f}")

    # --- P14-P18: el escalón 2, la gravedad declarada ----------------------
    print("\n[E.2 · escalón 2] quién declara la gravedad\n")

    ruta = grabar_demo_e2(tempfile.mkdtemp())
    demo = [d for _, _, d in renglones([ruta])]
    check("P14 · la demo lleva el campo que a los 1 468 reales les falta",
          all("entorno" in d for d in demo))
    check("P15 · la regla del escalón 1 sigue avisando de 32 sobre la demo",
          sum(1 for d in demo if pinta_mal(d)) == 32,
          sum(1 for d in demo if pinta_mal(d)))
    check("P16 · 🎲 y con UNA condición más quedan 2 — los dos de producción",
          sum(1 for d in demo if merece_aviso(d)) == 2,
          sum(1 for d in demo if merece_aviso(d)))
    check("P17 · 🔑 el control: los 2 que quedan son de producción, no dos cualesquiera",
          all(d.get("entorno") == "produccion" for d in demo if merece_aviso(d)))
    check("P18 · 🚨 y un entorno inventado NO pasa en silencio: el que escribe se entera",
          _revienta(lambda: marca_de_entorno("casi_produccion"), ValueError))

    # --- P19-P23: el escalón 3, el que no escribe renglón -------------------
    print("\n[E.2 · escalón 3] el fallo que no escribe ningún renglón\n")

    carpeta = Path(tempfile.mkdtemp())
    dia = datetime(2026, 8, 24, 3, 0, tzinfo=timezone.utc)
    t3 = disparador.turno_de(dia)
    t4 = disparador.turno_de(dia + timedelta(hours=1))
    t5 = disparador.turno_de(dia + timedelta(hours=2))
    disparador.marcar_turno(carpeta, t3)
    disparador.anotar_intento(carpeta, t3, "d0", "hizo")
    disparador.anotar_intento(carpeta, t4, "d0", "fallo")

    canal3 = CanalDeArchivo(tempfile.mkdtemp())
    avisar_de_los_mudos(canal3, carpeta, dia, dia + timedelta(hours=2))
    check("P19 · 🎲 LA APUESTA 3: el turno que nadie intentó SÍ se avisa, con calendario",
          canal3.mandados == 1, canal3.mandados)
    check("P20 · y el aviso nombra al turno mudo, no a otro",
          t5 in canal3.leidos()[0]["asunto"], canal3.leidos()[0]["asunto"])
    check("P21 · 🔑 el control: el turno que salió BIEN no genera aviso",
          all(t3 not in a["asunto"] for a in canal3.leidos()))
    check("P22 · 🚨 y sin calendario el mudo no deja NADA que leer: cero renglones suyos",
          len(disparador.intentos_de(carpeta, t5)) == 0)
    check("P23 · ⭐ la prueba de que hacen falta DOS entradas: alargar el calendario",
          _mudos_con(carpeta, dia, dia + timedelta(hours=4)) == 3,
          _mudos_con(carpeta, dia, dia + timedelta(hours=4)))

    # --- P24-P30: el escalón 4, el avisador que falla mudo ------------------
    print("\n[E.2 · escalón 4] el avisador que falla mudo\n")

    carpeta = Path(tempfile.mkdtemp())
    ruta_demo = grabar_demo_e2(carpeta)
    ahora = datetime(2026, 8, 24, 3, 0, tzinfo=timezone.utc)

    sano = CanalDeArchivo(tempfile.mkdtemp())
    check("P24 · el control: con la red SANA salen los 2 avisos de producción",
          avisar_como_todo_el_mundo(sano, [ruta_demo]) == 2, sano.mandados)

    caido = CanalCaido(tempfile.mkdtemp())
    check("P25 · 🎲 LA APUESTA 4: con la red caída manda 0 y NO revienta",
          avisar_como_todo_el_mundo(caido, [ruta_demo]) == 0)

    lat = Path(tempfile.mkdtemp())
    m, f = avisar_con_latido(CanalCaido(tempfile.mkdtemp()), [ruta_demo], lat, ahora)
    check("P26 · el del latido tampoco manda nada — el canal está caído igual",
          (m, f) == (0, 2), (m, f))
    check("P27 · 🔑 pero DEJA ESCRITO lo que no pudo, y por eso el que escucha se entera",
          echa_de_menos(lat, ahora, 3600) == "late mal: vivo, pero 2 avisos no salieron",
          echa_de_menos(lat, ahora, 3600))
    check("P28 · 🚨 y el que usa `except: pass` no deja NADA que consultar",
          echa_de_menos(Path(tempfile.mkdtemp()), ahora, 3600).startswith("no late"))
    check("P29 · ⭐ el avisador que no corrió produce queja SIN haber escrito nada",
          echa_de_menos(lat, ahora + timedelta(hours=3), 3600).startswith("no late"),
          echa_de_menos(lat, ahora + timedelta(hours=3), 3600))

    lat_ok = Path(tempfile.mkdtemp())
    avisar_con_latido(CanalDeArchivo(tempfile.mkdtemp()), [ruta_demo], lat_ok, ahora)
    check("P30 · 🔑 el control que hace falsificable a las dos: con todo bien, CALLA",
          echa_de_menos(lat_ok, ahora, 3600) is None,
          str(echa_de_menos(lat_ok, ahora, 3600)))

    # --- P31-P33: el escalón 5, el código de salida -------------------------
    print("\n[E.2 · escalón 5] el aviso que ya existía y se tiraba\n")

    # 📌 P31 se escribió midiendo el agujero —`disparador.py` salía con 0— y
    #    hubo que darle la vuelta al arreglarlo, en la misma sesión. El 0 medido
    #    queda en el README §E.2 con su fecha; aquí vive lo que debe seguir
    #    siendo cierto mañana. ⭐ Una prueba que describe el estado roto muere
    #    con el arreglo: por eso además está el detector de P35.
    c_disp, e_disp = codigo_de_salida_con_prueba_rota("disparador.py")
    check("P31 · 🎲 LA APUESTA 5, medida en 0 y ARREGLADA: ahora sale con 1",
          c_disp == 1, f"{c_disp} · stderr: {e_disp or 'vacío'}")
    c_rout, e_rout = codigo_de_salida_con_prueba_rota("router.py")
    check("P32 · y `router.py`, del mismo nivel y la misma semana, sale con 1",
          c_rout == 1, f"{c_rout} · stderr: {e_rout or 'vacío'}")
    check("P33 · ⭐ y ahora los dos módulos responden IGUAL al mismo fallo",
          c_disp == c_rout == 1, f"{c_disp} vs {c_rout}")
    check("P34 · 🚨 el control que salvó la medición: ninguno de los dos REVENTÓ",
          not e_disp and not e_rout, f"{e_disp!r} / {e_rout!r}")

    aud = auditar_codigos_de_salida()
    check("P35 · ⭐ el detector que sobrevive al arreglo: NINGÚN módulo tira el "
          "resultado de sus pruebas",
          not any(aud.values()), str([m for m, t in aud.items() if t]))
    check("P36 · 🔑 el control: el detector SÍ sabe morder — lo demuestra con un archivo torcido",
          _detector_muerde(), "no mordió")

    print("\n[E.2 · el cierre] la apuesta 1, contada\n")
    emiten, decide = contar_emitir_contra_decidir()
    check("P37 · 🎲 LA APUESTA 1: emitir es menos del 10 % del trabajo",
          emiten / (emiten + decide) < 0.10, f"{100 * emiten / (emiten + decide):.1f} %")
    check("P38 · 🔑 el control: la cuenta mira las DOS columnas, no una",
          emiten > 0 and decide > 0, f"{emiten} / {decide}")

    print(f"\n  {len(fallos)} fallos de 38")
    return fallos


def _detector_muerde():
    """Un detector que nunca se ve morder es una nota, no un detector (`LM.13`).

    Se fabrica un archivo con la forma exacta del bicho y se comprueba que el
    detector lo caza. Sin esto, P35 podría estar verde por no funcionar.
    """
    ruta = Path(tempfile.mkdtemp()) / "torcido.py"
    ruta.write_text(
        "def _pruebas():\n    return ['algo']\n\n\n"
        'if __name__ == "__main__":\n    _pruebas()\n',
        encoding="utf-8")
    sano = Path(tempfile.mkdtemp()) / "sano.py"
    sano.write_text(
        "def _pruebas():\n    return ['algo']\n\n\nimport sys\n"
        'if __name__ == "__main__":\n    sys.exit(1 if _pruebas() else 0)\n',
        encoding="utf-8")
    return tira_el_resultado_de_sus_pruebas(ruta) and not tira_el_resultado_de_sus_pruebas(sano)


def _revienta(f, tipo):
    """¿Levanta la excepción que se espera? Usado por P18."""
    try:
        f()
    except tipo:
        return True
    except Exception:
        return False
    return False


def _mudos_con(carpeta, desde, hasta):
    """Cuántos mudos ve el auditor si el calendario prometía MÁS turnos.

    ⭐ Es el control de la apuesta 3 y es el que la hace falsificable: si el
       mudo saliera del registro, alargar el calendario no cambiaría nada.
       Cambia — porque el dato lo pone el calendario, no el registro.
    """
    c = CanalDeArchivo(tempfile.mkdtemp())
    avisar_de_los_mudos(c, carpeta, desde, hasta)
    return c.mandados


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--informe":
        informe_escalon_1()
        informe_escalon_2()
        informe_escalon_3()
        informe_escalon_4()
        informe_escalon_5()
        informe_apuesta_1()
    else:
        fallidas = _pruebas()
        informe_escalon_1()
        informe_escalon_2()
        informe_escalon_3()
        informe_escalon_4()
        informe_escalon_5()
        informe_apuesta_1()
        # El escalon 5 de este mismo archivo mide lo que pasa cuando esta
        # linea no esta. Aqui esta: el resultado de las pruebas llega a quien
        # arranco el proceso, que es el unico que puede hacer algo con el.
        sys.exit(1 if fallidas else 0)
