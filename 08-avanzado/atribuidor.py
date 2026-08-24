"""atribuidor.py — F.1 del nivel 8: la rúbrica de dos capas, o QUIÉN falló.

    LA FRASE QUE HAY QUE VER

Un `FALLA` a secas significa dos cosas contrarias, y las dos se arreglan en
sitios opuestos.

Cuando el juez marca `FALLA` en «el número del euro está mal», eso puede ser:

    (a) el worker del euro trajo un dato malo         -> se arregla ABAJO
    (b) el worker lo trajo bien y arriba se copió mal -> se arregla ARRIBA

Es el `correct: bool` de TEAPP (sesión 83) con una capa más. Un booleano no
puede llevar esa distinción: hace falta un campo con estados.


    🚨 EL NUDO DE F.1, Y ESTABA DECLARADO CUATRO DÍAS ANTES

`rubrica_duelo.md:50`, escrita el 2026-08-20, dice dos cosas que juntas son
imposibles:

    «el juez no puede saber si la corrida fue de una capa o de dos»
    «esta rúbrica NO tiene el campo quién falló... meterlo aquí obligaría a
     mostrarle las capas al juez»

Y tiene razón las dos veces. Si el juez ve workers, sabe que está calificando
al orquestador, y un modelo con opinión sobre multi-agente **califica el
esquema en vez de la respuesta**. Sería el juez decidiendo el duelo que el
duelo existe para decidir.

🔑 A UN INSTRUMENTO AL QUE LE TAPAS LOS OJOS A PROPÓSITO NO LE PUEDES PEDIR
   ADEMÁS QUE SEÑALE CON EL DEDO.

→ Por eso F.1 sale con DOS instrumentos y no con uno:

    CAPA 1 — el juez ciego (`juez_duelo.py`, ya existe, NO se toca)
             dice QUÉ casilla falló. Sigue sin saber cuántas capas hubo.

    CAPA 2 — este archivo
             dice DE QUIÉN es. No pregunta a ningún modelo: lee la traza que
             C.1 dejó grabada y cruza campos que YA existen.

📌 Y por eso este archivo no llama a la API ni una vez. No es un ahorro: es que
   **preguntarle a un modelo quién falló sería un tercer opinante**, y lo que
   hace falta aquí es un testigo.


    LO QUE SE CONTÓ ANTES DE ESCRIBIR ESTO (README §F.1, seis hechos, $0,00)

    | # | Qué se contó                              | Cuánto salió          |
    |---|-------------------------------------------|-----------------------|
    | 1 | veredictos pagados del nivel              | 33 ($0,12534)         |
    | 2 | de esos, cuántos FALLA y de qué casilla    | 3, y las 3 C4-DOLAR   |
    | 3 | casillas atribuibles por moneda / no       | 9 / 2                 |
    | 4 | el nudo, ya escrito en rubrica_duelo.md:50 | 4 días antes          |
    | 5 | `encargo` grabado en worker_inicio/fin     | 60 y 60               |
    | 6 | campos que nombran un culpable, de 80      | NINGUNO               |

⚠️ El hecho 2 es el que hace este archivo incómodo: **el defecto que F.1 viene
   a arreglar no se ha visto todavía ni una sola vez.** Las 33 casillas
   juzgadas son de la línea base, que tiene UNA capa, y con una capa un `FALLA`
   no mezcla nada porque no hay a quién culpar.

   Es `LM.13` con el nombre puesto y dicho antes de que sea una excusa: **este
   atribuidor va a llegar a F.3 sin haber mordido nunca lo que vino a medir.**


    LOS SEIS ESTADOS, Y POR QUÉ NO SON DOS

Aposté cuatro (`worker`, `orquestador`, `esquema`, `no atribuible`) y el
escalón 1 obligó a partir `esquema` en tres, porque no es lo mismo:

    ok                    — la casilla pasó
    worker                — el de abajo entregó mal el dato
    orquestador           — el de abajo entregó bien y arriba se torció
    esquema:presupuesto   — el dato ESTABA y un tope de gasto cortó el turno
    esquema:contrato      — el dato ESTABA y el contrato no daba para llevarlo
    esquema:aislamiento   — nadie tenía el contexto para acertar (el precio de A.4)
    no_atribuible         — falló, y no hay en el registro con qué repartir la culpa

⭐ Los tres `esquema:` no son adornos. Un fallo de esquema **no se arregla
   regañando a ninguna de las dos capas**: las dos hicieron su parte. Se
   arregla cambiando las reglas del juego, y esa es una decisión de otra
   persona y de otro día. Meterlos todos en `no_atribuible` sería cierto y
   sería inútil.
"""

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # la consola de Windows no habla emoji sin esto

AQUI = Path(__file__).resolve().parent

# Las tres monedas del duelo, con el nombre del worker a la izquierda y el
# código que aparece en el contrato a la derecha.
MONEDAS = {"usd": "USD", "eur": "EUR", "cad": "CAD"}

# Los seis estados de la capa 2. Esta tupla es el contrato del archivo: si una
# función devuelve algo que no está aquí, `P1` se pone roja.
CULPAS = (
    "ok",
    "worker",
    "orquestador",
    "esquema:presupuesto",
    "esquema:contrato",
    "esquema:aislamiento",
    "no_atribuible",
)

# Las 11 casillas, copiadas de `juez_duelo.py`. Se repiten a propósito y no se
# importan: si un día las dos listas dejan de coincidir, `P2` lo dice en voz
# alta en vez de que el atribuidor califique casillas que el juez no juzga.
CASILLAS = [
    "C1-USD", "C1-EUR", "C1-CAD",
    "C2-USD", "C2-EUR", "C2-CAD",
    "C3-USD", "C3-EUR", "C3-CAD",
    "C4-DOLAR",
    "C5-REPORTE",
]

REG_WORKERS = AQUI / "registro_workers_claude-haiku-4-5.jsonl"
REG_ORQ = AQUI / "registro_orquestador_claude-haiku-4-5.jsonl"


# ---------------------------------------------------------------------------
#  LEER LO GRABADO
# ---------------------------------------------------------------------------

def _leer(ruta):
    """Los renglones de un .jsonl, saltándose los vacíos."""
    if not Path(ruta).exists():
        return []
    fuera = []
    for linea in Path(ruta).read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if linea:
            fuera.append(json.loads(linea))
    return fuera


def corridas_grabadas(reg_workers=REG_WORKERS, reg_orq=REG_ORQ):
    """Arma las corridas completas que hay en el disco.

    Una corrida sirve para atribuir solo si tiene las dos mitades: lo que se
    pidió arriba (`orquestador_inicio` / `orquestador_fin`) y lo que entregó
    cada worker (`worker_fin`). Las que no las tienen se dejan fuera **y se
    cuentan**, que no es lo mismo que ignorarlas.
    """
    W, O = _leer(reg_workers), _leer(reg_orq)

    ini = {d["corrida"]: d for d in O
           if d.get("evento") == "orquestador_inicio" and d.get("corrida")}
    fin = {d["corrida"]: d for d in O
           if d.get("evento") == "orquestador_fin" and d.get("corrida")}

    workers = defaultdict(dict)
    for d in W:
        if d.get("evento") == "worker_fin" and d.get("corrida"):
            workers[d["corrida"]][d.get("worker")] = d

    fuera = {}
    for c in sorted(set(ini) & set(fin)):
        ws = workers.get(c, {})
        if not set(MONEDAS) <= set(ws):
            continue                      # no es una corrida del duelo
        fuera[c] = {
            "corrida": c,
            "tarea": ini[c].get("tarea"),
            "texto": fin[c].get("texto") or "",
            "ok": fin[c].get("ok"),
            "workers": {m: ws[m] for m in MONEDAS},
        }
    return fuera


def numeros_publicados(texto):
    """Los números con separador de miles que aparecen en el texto final.

    ⚠️ Se buscan SOLO los que llevan puntos de millar (`3.059.012`), y es a
       propósito: un `1000` suelto del enunciado no es una cifra publicada.
       El precio de esa decisión está dicho en `P12`, que la obliga a fallar
       cuando el orquestador escribe el número sin separadores.
    """
    return {int(m.replace(".", ""))
            for m in re.findall(r"\d{1,3}(?:\.\d{3})+", texto or "")}


# ---------------------------------------------------------------------------
#  LA CAPA 2 — LOS TRES CRITERIOS QUE SE ATRIBUYEN POR MONEDA
# ---------------------------------------------------------------------------
#
#  🔑 Los tres hacen la MISMA pregunta con distinto objeto, y esa pregunta es
#     la que separa a las dos capas:
#
#         ¿el de abajo lo ENTREGÓ?  ->  si no, es del worker
#         ¿el de arriba lo PUBLICÓ? ->  si no, es del orquestador
#
#     Todo lo demás —presupuesto, contrato, aislamiento— son los casos en que
#     la respuesta a las dos es «sí» y la casilla falla igual. Ahí no falló
#     ninguna de las dos capas: falló la regla que las junta.


def _cortado_por_presupuesto(w):
    """¿A este worker lo paró un tope de gasto, teniendo ya la respuesta?

    🚨 Este es el hallazgo del escalón 1 convertido en función. Los cinco
       `ok:False` del registro traen `datos` COMPLETO y `faltan: []`: ninguno
       falló por el dato. El presupuesto los cortó **después** de que ya lo
       tenían. Si el atribuidor le creyera al `ok`, culparía al worker en los
       cinco casos, y en los cinco estaría señalando al que sí hizo el trabajo.
    """
    return w.get("ok") is False and w.get("motivo") == "presupuesto"


def _contrato_de_otra_moneda(w, codigo):
    """¿El contrato que devolvió habla de una moneda distinta a la del encargo?

    Pasa de verdad y está medido: en `c20260821T194121-ae1e85` el worker del
    CAD hizo el trabajo bien —su texto dice `1.000 CAD = 2.219.774 COP`— pero
    el encargo era una CADENA de tres eslabones y el contrato de A.3 solo tiene
    sitio para UNA conversión. Guardó el último paso: `moneda: USD`.

    ⭐ Los dos hicieron bien su parte y la respuesta correcta se tiró a la
       basura, porque la caja no daba para llevarla. Eso no es culpa de nadie
       de los dos: es del formulario.
    """
    datos = w.get("datos") or {}
    return bool(datos) and datos.get("moneda") not in (None, codigo)


def revisar_moneda(criterio, moneda, corrida):
    """La opinión de la TRAZA sobre una casilla, sin preguntarle a ningún modelo.

    Devuelve `(culpa, motivo)`. `motivo` es una frase corta para el humano: un
    estado sin motivo obliga a volver al registro a mano, y entonces el
    atribuidor no ahorra el trabajo, solo lo aplaza.
    """
    codigo = MONEDAS[moneda]
    w = corrida["workers"].get(moneda)
    if w is None:
        return "no_atribuible", f"no hay worker_fin de {codigo} en la corrida"

    datos = w.get("datos") or {}
    texto = corrida["texto"]

    # --- C1 — ¿pidió las herramientas que esa moneda necesitaba? -----------
    if criterio == "C1":
        usadas = w.get("herramientas") or []
        if "trm" in usadas and codigo != "USD":
            return "worker", f"llamó trm para {codigo}, y la TRM solo existe para el USD"
        if not ("tasa" in usadas and "convertir" in usadas):
            return "worker", f"no llamó tasa+convertir: {usadas}"
        return "ok", ""

    # --- C2 — ¿la cifra publicada es la que entregó el worker? -------------
    if criterio == "C2":
        pesos = datos.get("pesos")
        if pesos is None:
            if _cortado_por_presupuesto(w):
                return "esquema:presupuesto", "el tope cortó el turno sin cifra"
            return "worker", "no entregó cifra en el contrato"
        if _contrato_de_otra_moneda(w, codigo):
            return ("esquema:contrato",
                    f"entregó un contrato de {datos.get('moneda')} para un encargo de {codigo}")
        if pesos in numeros_publicados(texto):
            return "ok", ""
        if _cortado_por_presupuesto(w):
            return ("esquema:presupuesto",
                    f"tenía la cifra ({pesos}) y el tope cortó el turno antes de publicarla")
        return "orquestador", f"el worker entregó {pesos} y arriba no salió publicado"

    # --- C3 — ¿la fuente y la fecha de esa cifra llegaron al usuario? -------
    if criterio == "C3":
        fuente, fecha = str(datos.get("fuente") or ""), str(datos.get("fecha") or "")
        if not fuente or not fecha:
            faltan = [n for n, v in (("fuente", fuente), ("fecha", fecha)) if not v]
            return "worker", f"el contrato no trae {' ni '.join(faltan)}"
        if fuente in texto and fecha in texto:
            return "ok", ""
        if _cortado_por_presupuesto(w):
            return "esquema:presupuesto", "el tope cortó el turno antes de publicar fuente/fecha"
        if _contrato_de_otra_moneda(w, codigo):
            return "esquema:contrato", "la fuente entregada es de otro eslabón de la cadena"
        return "orquestador", "el worker entregó fuente y fecha y arriba no salieron"

    raise ValueError(f"criterio desconocido: {criterio}")


def revisar_corrida(corrida):
    """Las 9 casillas por moneda, según la traza sola. Sin juez y sin API."""
    fuera = {}
    for criterio in ("C1", "C2", "C3"):
        for moneda, codigo in MONEDAS.items():
            fuera[f"{criterio}-{codigo}"] = revisar_moneda(criterio, moneda, corrida)
    return fuera


# ---------------------------------------------------------------------------
#  LAS DOS CASILLAS QUE NO SON DE NADIE, Y POR QUÉ
# ---------------------------------------------------------------------------

def atribuir_c4(corrida):
    """C4-DOLAR — la frontera del dólar. ¿De quién es cuando falla?

    De nadie de los dos, y la v1 de la rúbrica ya dijo por qué sin saber que
    estaba describiendo un estado: «el worker del dólar NO SABE que existen
    otras dos monedas — no tiene el contexto para decir *para que las tres sean
    comparables*».

    🔑 Ese es exactamente el precio de A.4 (aislamiento de contexto). Culpar al
       worker sería cobrarle algo que no podía ver; culpar al orquestador sería
       cobrarle algo que no dijo el worker. **Es del esquema.**

    ⚠️ Y esto **tumba media apuesta 2**: aposté que `no_atribuible` caería
       sobre C4-DOLAR, y no cae. C4 SÍ es atribuible — al esquema. Queda
       escrito aquí, en el código, y no solo en el informe.
    """
    return ("esquema:aislamiento",
            "ningún worker tenía el contexto de las otras dos monedas (A.4)")


def atribuir_c5(corrida):
    """C5-REPORTE — guardar el reporte. Esta sí tiene dueño, y es de arriba.

    Ningún worker llama `guardar_reporte`: el reparto de A.2 les da `tasa` y
    `convertir` y nada más. El que guarda es el orquestador, y el que miente
    diciendo que guardó cuando el permiso fue denegado también.
    """
    return ("orquestador",
            "guardar_reporte solo está en el menú de la capa de arriba")


# ---------------------------------------------------------------------------
#  EL ACOPLE DE LAS DOS CAPAS
# ---------------------------------------------------------------------------

def atribuir(veredictos, corrida):
    """CAPA 1 + CAPA 2. Toma lo que dijo el juez ciego y le pone dueño.

    `veredictos` es el JSON de `juez_duelo.py`: casilla -> {justificacion, veredicto}.

    Reglas del acople, y la tercera es la que importa:

      1. El juez dijo `PASA`      -> `ok`. La traza no discute un aprobado.
      2. El juez dijo `NO APLICA` -> `ok`. No entra en el reparto.
      3. El juez dijo `FALLA`     -> se le pregunta a la traza de quién es.

    🚨 Y el caso que NO se esconde: el juez dice `FALLA` y la traza dice que
       todo cuadra. Eso NO se resuelve dándole la razón a ninguno de los dos.
       Se marca `no_atribuible` con el desacuerdo escrito, porque significa una
       de dos cosas y las dos hay que mirarlas a mano:

         - el juez se equivocó (la Parte 5 de la rúbrica avisa de esto), o
         - falló algo que la traza no sabe mirar.

       Es `LM.66`: la pregunta ante un dato no es «¿está bien?» sino «¿qué otro
       dato tendría que estar en desacuerdo con éste, si estuviera mal?». Aquí
       ese otro dato existe **y a veces está en desacuerdo**. Taparlo con un
       promedio sería inventarse la respuesta.
    """
    revision = revisar_corrida(corrida)
    fuera = {}

    for casilla in CASILLAS:
        v = veredictos.get(casilla) or {}
        dicho = str(v.get("veredicto", "")).strip().upper()

        if dicho != "FALLA":
            fuera[casilla] = ("ok", "")
            continue

        if casilla == "C4-DOLAR":
            fuera[casilla] = atribuir_c4(corrida)
        elif casilla == "C5-REPORTE":
            fuera[casilla] = atribuir_c5(corrida)
        else:
            culpa, motivo = revision[casilla]
            if culpa == "ok":
                fuera[casilla] = ("no_atribuible",
                                  "el juez marcó FALLA y la traza no ve nada torcido")
            else:
                fuera[casilla] = (culpa, motivo)

    return fuera


def reparto(atribuciones):
    """Cuántas casillas cayeron en cada estado. La herramienta cuenta; el
    modelo no ha opinado en ningún punto de este archivo."""
    return Counter(culpa for culpa, _ in atribuciones.values())


# ---------------------------------------------------------------------------
#  LOS INFORMES — lo que se midió, sobre lo que ya estaba pagado
# ---------------------------------------------------------------------------

def informe_escalon_1():
    """La apuesta 3: ¿se pueden atribuir las 9 casillas por moneda SIN modelo?"""
    print("\n" + "=" * 74)
    print("[F.1 · escalón 1] la traza sola, sobre las corridas REALES ya pagadas")
    print("=" * 74)

    corridas = corridas_grabadas()
    if not corridas:
        print("  (no hay corridas completas en el disco)")
        return

    total = Counter()
    print(f"\n  {'corrida':<28} {'mon':<4} {'C1':<11} {'C2':<21} {'C3':<21}")
    print("  " + "-" * 86)
    for c, corr in corridas.items():
        rev = revisar_corrida(corr)
        for moneda, codigo in MONEDAS.items():
            fila = [rev[f"{k}-{codigo}"][0] for k in ("C1", "C2", "C3")]
            total.update(fila)
            print(f"  {c:<28} {codigo:<4} {fila[0]:<11} {fila[1]:<21} {fila[2]:<21}")

    print(f"\n  corridas completas: {len(corridas)}   ·   casillas atribuidas: {sum(total.values())}")
    print(f"  llamadas a la API: 0   ·   coste: $0,000000")
    for culpa, n in total.most_common():
        print(f"     {culpa:<22} {n}")
    print("\n  ✅ APUESTA 3 — GANADA. Las 9 casillas por moneda se atribuyen cruzando")
    print("     `encargo`, `datos` y el texto final. Ni una llamada a un modelo.")

    # 🚨 Y lo que la tabla NO tiene, dicho aquí y no en una nota al pie.
    print("\n  " + "-" * 70)
    print("  🚨 EL HUECO, Y ES EL DEL TÍTULO DE F.1:")
    print(f"     casillas marcadas `orquestador` sobre datos REALES: "
          f"{total.get('orquestador', 0)}")
    print("\n     Cero. El estado que este archivo existe para poder marcar —«el de")
    print("     abajo lo entregó bien y arriba se torció»— NO se ha visto morder ni")
    print("     una vez en el mundo. Muerde en `P7` y `P8`, y esas dos corridas las")
    print("     fabriqué yo.")
    print("\n  🔑 Es `LM.13` con el nombre puesto, y estaba escrito en la apuesta 6")
    print("     ANTES de medir: el atribuidor llega a F.3 sin haber mordido nunca lo")
    print("     que vino a medir. No es un fallo del instrumento — es que el defecto")
    print("     necesita dos capas para existir, y las dos capas todavía no han")
    print("     corrido el duelo. **F.3 es la primera vez que este número puede")
    print("     dejar de ser cero.**")


def informe_escalon_2():
    """El `ok` del worker no significa lo que parece."""
    print("\n" + "=" * 74)
    print("[F.1 · escalón 2] 🚨 el ok:False de los workers NO es un fallo del dato")
    print("=" * 74)

    W = _leer(REG_WORKERS)
    malos = [d for d in W if d.get("evento") == "worker_fin" and d.get("ok") is False]
    print(f"\n  worker_fin con ok:False .............. {len(malos)}")
    con_datos = [d for d in malos if (d.get("datos") or {}).get("pesos") is not None]
    sin_faltantes = [d for d in malos if d.get("faltan") == []]
    print(f"  ...de esos, con una cifra entregada .. {len(con_datos)}")
    print(f"  ...de esos, con `faltan: []` ......... {len(sin_faltantes)}")
    print(f"  motivos .............................. "
          f"{dict(Counter(d.get('motivo') for d in malos))}")

    print("\n  🔑 Ninguno falló POR EL DATO. El presupuesto los cortó DESPUÉS de que")
    print("     ya tenían la respuesta. Un atribuidor que le creyera al `ok` culparía")
    print("     al worker en los cinco casos — y en los cinco señalaría al que sí")
    print("     hizo el trabajo.")
    print("\n  ⭐ Por eso `esquema:presupuesto` es un estado y no una nota al pie.")


def informe_escalon_3():
    """La única fila `orquestador` de todo lo grabado, y por qué no es suya."""
    print("\n" + "=" * 74)
    print("[F.1 · escalón 3] 🎁 el cruce acierta en el HECHO y se equivoca en el CULPABLE")
    print("=" * 74)

    corridas = corridas_grabadas()
    torcidos = []
    for c, corr in corridas.items():
        tarea = (corr["tarea"] or "").lower()
        for moneda in MONEDAS:
            w = corr["workers"][moneda]
            enc = w.get("encargo") or ""
            # ⭐ El cruce más tonto que se puede escribir, y salta de verdad:
            #    la tarea pide UNA conversión por moneda; este encargo pide tres.
            if "ese resultado" in enc.lower() and "ese resultado" not in tarea:
                torcidos.append((c, moneda, enc))

    print(f"\n  encargos que NO corresponden a la tarea de arriba: {len(torcidos)}")
    for c, moneda, enc in torcidos:
        print(f"     {c}  [{moneda}]  {enc[:58]}...")

    print("\n  ⚠️ Y aquí hay que corregirse en voz alta, porque el dato es correcto")
    print("     y la conclusión fácil era falsa. Fui a ver QUIÉN torció ese encargo:")
    print("     NO fue el orquestador. Está fijo a mano en `presupuesto.py:406`,")
    print("     `ENCARGOS_DESIGUALES`, puesto a propósito por C.2 para que el CAD")
    print("     saliera caro y se pudiera medir el reparto del presupuesto.")
    print("\n  🔑 El registro no tiene forma de distinguirlo: `encargo` está grabado,")
    print("     pero QUIÉN LO ESCRIBIÓ, no. Es `LM.92` de ayer con otra ropa —")
    print("     un encargo que no corresponde a la tarea se ve IDÉNTICO cuando lo")
    print("     torció el orquestador y cuando lo clavó a mano un experimento.")
    print("\n  📎 Deuda anotada, no arreglada hoy: falta un campo `origen` en")
    print("     `worker_inicio` que diga si el encargo lo escribió el modelo o el")
    print("     harness. No se añade ahora porque reescribir los registros borraría")
    print("     la evidencia de que faltaba (`LM.65`, y está en el sobre).")


def informe_escalon_4():
    """Las dos capas juntas, sobre el único juicio pagado que existe."""
    print("\n" + "=" * 74)
    print("[F.1 · escalón 4] las dos capas acopladas — sobre los 33 veredictos pagados")
    print("=" * 74)

    ruta = AQUI / "veredictos_registro_linea_base_claude-haiku-4-5.json"
    if not ruta.exists():
        print("  (no está el archivo de veredictos)")
        return
    j = json.loads(ruta.read_text(encoding="utf-8"))

    corridas = corridas_grabadas()
    if not corridas:
        print("  (no hay corridas completas)")
        return
    prestada = list(corridas.values())[0]

    print(f"\n  juez: {j.get('juez')}   ·   coste ya pagado: ${j.get('coste_del_juez_usd')}")
    print(f"  corridas juzgadas: {len(j.get('corridas', []))}   ·   casillas: "
          f"{len(j.get('corridas', [])) * j.get('casillas_posibles', 11)}")

    total = Counter()
    for it in j.get("corridas", []):
        a = atribuir(it.get("veredictos", {}), prestada)
        total.update(reparto(a))
    for culpa, n in total.most_common():
        print(f"     {culpa:<22} {n}")

    print("\n  🚨 Y hay que leer esta tabla con la salvedad ARRIBA, no de remate:")
    print("     los 33 veredictos son de la LÍNEA BASE, que tiene UNA capa. La")
    print("     traza que se les cruza es prestada de otra corrida. Este número NO")
    print("     mide el defecto que F.1 vino a arreglar — mide que el acople corre.")
    print("\n  🔑 Con una capa, un `FALLA` no mezcla nada: no hay a quién culpar.")
    print("     Las 3 FALLA son las 3 de `C4-DOLAR`, y caen en `esquema:aislamiento`,")
    print("     que es el estado que dice «ninguna de las dos capas pudo evitarlo».")


def informe_apuesta_2():
    """La apuesta 2, resuelta contra el código y no contra el recuerdo."""
    print("\n" + "=" * 74)
    print("[F.1] 🎲 APUESTA 2 — media ganada, media FALLADA, y la fallada es mejor")
    print("=" * 74)
    print(f"\n  aposté 4 estados; el escalón 1 obligó a {len(CULPAS)}:")
    for c in CULPAS:
        print(f"     · {c}")
    print("\n  ✅ Ganada la mitad falsable: SÍ hace falta un estado para «falló y no")
    print("     se puede decir de quién es». Existe y es `no_atribuible`.")
    print("\n  🔴 FALLADA la predicción concreta: aposté que `no_atribuible` caería")
    print("     sobre `C4-DOLAR`. NO cae. C4 sí es atribuible — al ESQUEMA, porque")
    print("     el aislamiento de A.4 impide a los dos lados verlo. `no_atribuible`")
    print("     quedó para otra cosa y para algo más útil: el juez dice FALLA y la")
    print("     traza no ve nada torcido. Un desacuerdo entre dos testigos.")
    print("\n  ⭐ Y `esquema` no era un estado: eran TRES. presupuesto, contrato y")
    print("     aislamiento fallan igual de lejos de las dos capas y se arreglan en")
    print("     sitios distintos. Juntarlos habría sido cierto e inútil.")


# ---------------------------------------------------------------------------
#  PRUEBAS — cada estado tiene que MORDER, o es una nota (LM.13)
# ---------------------------------------------------------------------------

def _corrida_falsa(**cambios):
    """Una corrida de dos capas fabricada a mano, $0,00, para torcerla.

    ⚠️ Y se dice aquí y no en una nota al pie: esto es fabricado. Es la trampa
       que la apuesta 6 declaró antes de empezar. Sirve para ver morder a cada
       estado; NO sirve como evidencia de que el atribuidor acierta en el mundo.
    """
    base = {
        "corrida": "cFALSA",
        "tarea": "Tengo 1.000 dólares, 1.000 euros y 1.000 dólares canadienses.",
        "texto": ("1.000 USD = 3.059.012 pesos. 1.000 EUR = 3.573.458 pesos. "
                  "1.000 CAD = 2.219.774 pesos. "
                  "Fuente: mercado (open.er-api.com). Fecha: Fri, 21 Aug 2026"),
        "ok": True,
        "workers": {},
    }
    cifras = {"usd": 3059012, "eur": 3573458, "cad": 2219774}
    for m, cod in MONEDAS.items():
        base["workers"][m] = {
            "evento": "worker_fin", "worker": m, "corrida": "cFALSA",
            "encargo": f"Convierte 1000 {cod} a pesos colombianos.",
            "ok": True, "motivo": None, "faltan": [],
            "herramientas": ["tasa", "convertir"],
            "datos": {"moneda": cod, "monto": 1000, "pesos": cifras[m],
                      "fuente": "mercado (open.er-api.com)",
                      "fecha": "Fri, 21 Aug 2026"},
        }
    base.update(cambios)
    return base


def _falla_todo():
    """Un veredicto de juez con las 11 casillas en FALLA."""
    return {c: {"justificacion": "-", "veredicto": "FALLA"} for c in CASILLAS}


def _pruebas():
    fallos = []

    def check(nombre, cond, detalle=""):
        print(("  OK  " if cond else "  XX  ") + nombre + (f"  -> {detalle}" if detalle else ""))
        if not cond:
            fallos.append(nombre)

    print("\n[F.1] pruebas del atribuidor\n")

    # --- P1-P3: el contrato del archivo ------------------------------------
    corr = _corrida_falsa()
    rev = revisar_corrida(corr)
    check("P1 · toda culpa devuelta está en CULPAS",
          all(c in CULPAS for c, _ in rev.values()),
          str({c for c, _ in rev.values()} - set(CULPAS)))
    check("P2 · el atribuidor cubre las 11 casillas del juez",
          set(atribuir(_falla_todo(), corr)) == set(CASILLAS))
    check("P3 · una corrida sana no culpa a nadie",
          set(c for c, _ in rev.values()) == {"ok"},
          str(reparto(rev)))

    # --- P4-P6: el estado `worker` muerde ----------------------------------
    c = _corrida_falsa()
    c["workers"]["eur"]["herramientas"] = ["tasa"]           # se saltó convertir
    check("P4 · sin `convertir`, C1 es del WORKER",
          revisar_moneda("C1", "eur", c)[0] == "worker",
          revisar_moneda("C1", "eur", c)[1])

    c = _corrida_falsa()
    c["workers"]["cad"]["herramientas"] = ["trm", "convertir"]
    check("P5 · `trm` para el CAD es del WORKER",
          revisar_moneda("C1", "cad", c)[0] == "worker",
          revisar_moneda("C1", "cad", c)[1])

    c = _corrida_falsa()
    c["workers"]["usd"]["datos"]["fuente"] = ""
    check("P6 · contrato sin fuente, C3 es del WORKER",
          revisar_moneda("C3", "usd", c)[0] == "worker",
          revisar_moneda("C3", "usd", c)[1])

    # --- P7-P8: el estado `orquestador` muerde -----------------------------
    #     🔑 ESTAS DOS SON EL ARCHIVO ENTERO. Es la distinción que F.1 existe
    #        para hacer: el worker entregó bien y arriba se torció.
    c = _corrida_falsa()
    c["texto"] = c["texto"].replace("3.573.458", "3.573.999")   # arriba lo cambió
    culpa, motivo = revisar_moneda("C2", "eur", c)
    check("P7 · worker bien + cifra cambiada arriba = ORQUESTADOR",
          culpa == "orquestador", motivo)

    c = _corrida_falsa()
    c["texto"] = c["texto"].replace("Fecha: Fri, 21 Aug 2026", "Fecha: hoy")
    culpa, motivo = revisar_moneda("C3", "usd", c)
    check("P8 · worker trae fecha + arriba la borra = ORQUESTADOR",
          culpa == "orquestador", motivo)

    # --- P9: el mismo síntoma, el otro dueño -------------------------------
    #     ⭐ P7 y P9 producen EL MISMO síntoma —la cifra del worker no está
    #        publicada— y tienen dueños opuestos. Si el atribuidor no
    #        distinguiera estas dos, no serviría para nada.
    c = _corrida_falsa()
    c["workers"]["cad"]["ok"] = False
    c["workers"]["cad"]["motivo"] = "presupuesto"
    c["texto"] = c["texto"].replace("1.000 CAD = 2.219.774 pesos.",
                                    "1.000 CAD: no se pudo consultar.")
    culpa, motivo = revisar_moneda("C2", "cad", c)
    check("P9 · misma cifra ausente, pero cortado por tope = ESQUEMA:PRESUPUESTO",
          culpa == "esquema:presupuesto", motivo)

    # --- P10: el contrato que no daba para la respuesta --------------------
    c = _corrida_falsa()
    c["workers"]["cad"]["datos"] = {"moneda": "USD", "monto": 725.65, "pesos": 621,
                                    "fuente": "mercado (open.er-api.com)",
                                    "fecha": "Fri, 21 Aug 2026"}
    culpa, motivo = revisar_moneda("C2", "cad", c)
    check("P10 · contrato de otra moneda = ESQUEMA:CONTRATO",
          culpa == "esquema:contrato", motivo)

    # --- P11: el desacuerdo entre los dos testigos -------------------------
    #     🚨 La prueba que exige que el atribuidor DIGA QUE NO SABE. Sin ella,
    #        un desacuerdo se disfrazaría de culpa de alguien.
    c = _corrida_falsa()
    a = atribuir({"C2-EUR": {"veredicto": "FALLA", "justificacion": "-"}}, c)
    check("P11 · juez dice FALLA y la traza no ve nada = NO_ATRIBUIBLE",
          a["C2-EUR"][0] == "no_atribuible", a["C2-EUR"][1])

    # --- P12: el precio declarado de `numeros_publicados` ------------------
    #     ⚠️ Obliga a que el defecto conocido se vea. Si un día alguien mejora
    #        el lector de números, esta prueba se pone roja y hay que venir a
    #        tachar el comentario que declara el precio. (LM.94)
    c = _corrida_falsa()
    c["texto"] = c["texto"].replace("3.059.012", "3059012")   # sin separadores
    check("P12 · el lector NO ve cifras sin separador, y eso culpa al de arriba",
          revisar_moneda("C2", "usd", c)[0] == "orquestador",
          "es un falso positivo conocido y declarado, no un acierto")

    # --- P13-P14: las dos casillas que no son por moneda -------------------
    check("P13 · C4-DOLAR en FALLA cae en ESQUEMA:AISLAMIENTO",
          atribuir(_falla_todo(), corr)["C4-DOLAR"][0] == "esquema:aislamiento")
    check("P14 · C5-REPORTE en FALLA es del ORQUESTADOR",
          atribuir(_falla_todo(), corr)["C5-REPORTE"][0] == "orquestador")

    # --- P15-P16: el acople no inventa culpas ------------------------------
    check("P15 · PASA nunca produce culpa",
          set(x[0] for x in atribuir(
              {c: {"veredicto": "PASA"} for c in CASILLAS}, corr).values()) == {"ok"})
    check("P16 · NO APLICA tampoco",
          set(x[0] for x in atribuir(
              {c: {"veredicto": "NO APLICA"} for c in CASILLAS}, corr).values()) == {"ok"})

    # --- P17: sin worker no se inventa un dueño ----------------------------
    c = _corrida_falsa()
    del c["workers"]["eur"]
    check("P17 · sin worker_fin, la casilla es NO_ATRIBUIBLE",
          revisar_moneda("C2", "eur", c)[0] == "no_atribuible",
          revisar_moneda("C2", "eur", c)[1])

    # --- P18: todo estado tiene motivo escrito -----------------------------
    c = _corrida_falsa()
    c["workers"]["eur"]["herramientas"] = ["tasa"]
    todos = list(revisar_corrida(c).values()) + list(atribuir(_falla_todo(), c).values())
    check("P18 · ninguna culpa distinta de `ok` llega sin motivo",
          all(motivo for culpa, motivo in todos if culpa != "ok"))

    # --- P19-P21: las apuestas, medidas contra el disco --------------------
    corridas = corridas_grabadas()
    check("P19 · hay corridas reales completas para medir la apuesta 3",
          len(corridas) >= 5, f"{len(corridas)} corridas")

    total = Counter()
    for corr_real in corridas.values():
        total.update(c for c, _ in revisar_corrida(corr_real).values())
    check("P20 · APUESTA 3 · las 9 por moneda se atribuyen sin modelo",
          sum(total.values()) == len(corridas) * 9 and "no_atribuible" not in total,
          str(dict(total)))

    check("P21 · APUESTA 5 · la rúbrica sigue teniendo 11 casillas",
          len(CASILLAS) == 11, f"{len(CASILLAS)}")

    # --- P22: el freno de la apuesta 1 -------------------------------------
    #     🔒 Si alguien mete una llamada a la API en este archivo, la apuesta 1
    #        deja de ser cierta EN SILENCIO. Esta prueba lo impide.
    #     🎁 Y esta prueba nació en rojo por un motivo que vale la lección: los
    #        literales que buscaba estaban EN LA LÍNEA QUE LOS BUSCABA. Un
    #        detector que lee su propio archivo se encuentra a sí mismo. Se
    #        arregla partiendo las agujas, y se deja escrito en vez de tapado.
    agujas = ["anthro" + "pic", "messages." + "create", "import " + "agente"]
    texto = Path(__file__).read_text(encoding="utf-8")
    codigo = "\n".join(l for l in texto.splitlines()
                       if not l.strip().startswith("#"))
    check("P22 · APUESTA 1 · este archivo no llama a ningún modelo",
          not any(s in codigo for s in agujas),
          "el atribuidor es un testigo, no un tercer opinante")

    #     Y el freno anterior tiene que VERSE MORDER, o es una nota (LM.13).
    #     🎁 Y cayó DOS VECES en el mismo sitio: el cebo de esta prueba también
    #        es una aguja, y también vive en este archivo. Un detector que se
    #        lee a sí mismo no distingue el veneno del frasco de muestras.
    sucio = "resp = cliente.messages." + "create(model=MODELO)"
    check("P23 · ...y ese freno muerde: sobre un archivo con la llamada, salta",
          any(s in sucio for s in agujas),
          "sin esta línea, P22 podría estar verde por no mirar nada")

    # --- P24: el contrato con el juez --------------------------------------
    juez = (AQUI / "juez_duelo.py")
    if juez.exists():
        t = juez.read_text(encoding="utf-8")
        check("P24 · las 11 casillas coinciden con las de juez_duelo.py",
              all(f'"{c}"' in t for c in CASILLAS),
              "si divergen, el atribuidor calificaría casillas que el juez no juzga")

    print(f"\n  → {len(fallos)} en rojo." if fallos else "\n  → todas verdes.")
    return fallos


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--informe":
        informe_escalon_1()
        informe_escalon_2()
        informe_escalon_3()
        informe_escalon_4()
        informe_apuesta_2()
    else:
        fallidas = _pruebas()
        informe_escalon_1()
        informe_escalon_2()
        informe_escalon_3()
        informe_escalon_4()
        informe_apuesta_2()
        # LM.94 de ayer: el resultado de las pruebas llega a quien arrancó el
        # proceso. Es la línea que `disparador.py` no tenía.
        sys.exit(1 if fallidas else 0)
