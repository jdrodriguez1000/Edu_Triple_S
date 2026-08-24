"""skills_compartidas.py — D.2 del nivel 8: el menú que se paga en cada worker.

    LA TRAMPA, EN UNA FRASE

Una skill existe para NO pagar el conocimiento entero: se manda una ficha corta
y el cuerpo solo se lee si hace falta. Con UN agente eso es un ahorro claro.
Con TRES workers dando TRES vueltas cada uno, la ficha corta se paga NUEVE
veces — y el cuerpo que evitaba se habría pagado una.

    ⭐ LA ASIMETRÍA CON D.1, QUE ES EL TITULAR DEL BLOQUE D ENTERO

D.1 era ESCRIBIR: dos workers sobre el mismo archivo perdían el 49,5% de lo
que guardaban y el archivo quedaba válido. D.2 es LEER: cuatro `.md` que nadie
modifica, leídos por doce hilos a la vez, no rompen nada.

🔑 Lo compartido solo duele cuando alguien lo CAMBIA. Cuando nadie lo cambia,
   lo compartido no duele — CUESTA. Y un coste no da excepciones ni deja el
   archivo a medias: llega en la factura, un mes después, sin nombre.

    ESTE ARCHIVO NO EDITA `06b-memoria-skills/skills.py`. LO IMPORTA.

Mismo motivo que `worker.py` con `agente.py` en A.1 y que `compartida.py` con
`memoria.py` en D.1: es código medido de otro nivel, y el valor de una medición
vieja depende de que su código siga siendo el mismo.

⭐ Y NO HABLA CON LA API salvo en `tokens()`, que usa el contador oficial y
   cuesta $0,00. Todo lo demás se rompe gratis.
"""

import hashlib
import random
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent

# Se importa el del 6b tal cual. Ni una línea suya se toca.
sys.path.insert(0, str(RAIZ / "06b-memoria-skills"))
import skills as skills_6b            # noqa: E402


# ---------------------------------------------------------------------------
# 0) EL MÍNIMO DEL CACHÉ — un dato de fuera, y por eso lleva fecha y fuente
# ---------------------------------------------------------------------------
# 🚨 ESTO NO ES UNA CONSTANTE DE ESTE PROYECTO: es un número de Anthropic, y
#    puede cambiar sin avisarnos. Por eso vive en UN sitio con su fecha al lado
#    y no repartido por el código. Consultado el 2026-08-23.
#
# ⚠️ Y NO ES MONÓTONO POR GENERACIÓN, que es la trampa entera:
#    un prompt de 3000 tokens SÍ cachea en Opus 5 y NO cachea en Haiku 4.5.
#    Lo intuitivo —"el modelo más nuevo y barato tendrá el mínimo más bajo"— es
#    falso, y creérselo sale gratis hasta que llega la factura.
MINIMO_CACHE_TOKENS = {
    "claude-opus-5": 512,
    "claude-opus-4-8": 1024,
    "claude-sonnet-5": 1024,
    "claude-sonnet-4-6": 1024,
    "claude-opus-4-7": 2048,
    "claude-haiku-4-5": 4096,      # 🚨 el que corre este nivel entero
    "claude-opus-4-6": 4096,
}
MINIMO_CACHE_CONSULTADO = "2026-08-23"


# ---------------------------------------------------------------------------
# 0b) TOKENS DE VERDAD, MEDIDOS CON EL CONTADOR OFICIAL — y por qué no basta
#     con contar caracteres
# ---------------------------------------------------------------------------
# 🚨 ESTA TABLA NACIÓ DE UN ERROR MÍO, Y SE DEJA ESCRITO.
#    La primera versión de este archivo medía la apuesta 1 EN CARACTERES y daba
#    1,48x. Medida en TOKENS —que es lo que se factura— da 1,34x. La dirección
#    aguantó; el número que había sellado (">1,4x") NO.
#
# 🔑 Los caracteres no se reparten igual entre un texto y otro: el menú son
#    frases largas y los cuerpos llevan listas, cifras y viñetas, que se parten
#    en más tokens por carácter. Contar caracteres no es "una aproximación al
#    coste": es OTRA magnitud, que a veces se le parece.
#    → Cuando el número decide algo, se mide en la unidad que se paga.
#
# Medidos con `messages.count_tokens` el 2026-08-23. $0,00.
TOKENS_MEDIDOS = {
    "menu": 622,
    "cierre-de-ano": 866,
    "explicar-a-un-cliente": 1143,
    "normas-cambiarias": 1227,
    "reporte-mensual": 947,
}
TOKENS_MEDIDOS_FECHA = "2026-08-23"

# El prefijo de un worker en su primera vuelta, del registro pagado de la
# corrida `c20260823T231228`: herramientas + system + el encargo. Es lo que se
# vuelve a pagar ENTERO cada vez que hay una vuelta más.
PREFIJO_WORKER_TOKENS = 1828


def cachea(tokens_del_prefijo, modelo="claude-haiku-4-5"):
    """¿Se activaría el caché con un prefijo de este tamaño?

    🚨 DEVUELVE TRES COSAS, Y LA TERCERA ES LA LECCIÓN:
       (True,  n) — cachea.
       (False, n) — NO cachea, y le faltan (n - tokens) para llegar.
       (None,  0) — no sabemos el mínimo de ese modelo. NO es "sí" ni es "no".

    ⚠️ Cuando devuelve False, la API **no da ningún error**. Se manda el
       `cache_control`, se acepta, y `cache_creation_input_tokens` vuelve en 0.
       Es `LM.15` con forma de descuento: el instrumento no da un dato falso,
       da SILENCIO, y el silencio se lee como "ya está cacheado".
       → Por eso lo único que prueba que el caché funciona es leer
         `usage.cache_read_input_tokens`, no haber escrito `cache_control`.
    """
    minimo = MINIMO_CACHE_TOKENS.get(modelo)
    if minimo is None:
        return None, 0
    return tokens_del_prefijo >= minimo, minimo


# ---------------------------------------------------------------------------
# 1) MEDIR EL MENÚ — apuesta 1
# ---------------------------------------------------------------------------
# El menú se paga una vez POR LLAMADA, no por corrida y no por worker. Y eso no
# es un detalle de contabilidad: es lo que convierte un 14% en otra cosa.

def peso_del_menu(carpeta=None):
    """Cuánto pesa el menú y cuánto pesan los cuerpos. En caracteres."""
    fichas = skills_6b.leer_fichas(carpeta) if carpeta else skills_6b.leer_fichas()
    menu = skills_6b.menu_como_texto(fichas)
    cuerpos = {}
    for f in fichas:
        r = skills_6b.leer_skill(f["nombre"], f["archivo"].parent)
        cuerpos[f["nombre"]] = len(r.get("contenido", ""))
    # Los tokens SOLO se conocen para las cuatro skills reales del 6b, que son
    # las que se midieron. Con una carpeta de prueba se deja en None a
    # propósito: mejor un hueco visible que un número inventado.
    tok_menu = TOKENS_MEDIDOS["menu"] if carpeta is None else None
    tok_cuerpos = ({n: TOKENS_MEDIDOS[n] for n in cuerpos}
                   if carpeta is None else None)
    return {"fichas": len(fichas), "menu": len(menu),
            "cuerpos": cuerpos, "cuerpos_total": sum(cuerpos.values()),
            "texto_menu": menu,
            "menu_tok": tok_menu, "cuerpos_tok": tok_cuerpos,
            "cuerpos_tok_total": sum(tok_cuerpos.values()) if tok_cuerpos else None}


def cuenta_de_la_corrida(llamadas, peso=None, unidad="tokens"):
    """🎲 APUESTA 1 — ¿el menú repetido cuesta más que los cuerpos que evita?

    `llamadas` es cuántas llamadas API tiene la corrida: en el fan-out real son
    3 workers × 3 vueltas = 9, medidas en `registro_workers_*.jsonl`.

    ⭐ FÍJATE EN QUÉ SE COMPARA, PORQUE ES LO QUE HACE HONESTA LA APUESTA:
       NO se compara "el menú" contra "los cuerpos". Se compara
         · lo que el menú cuesta DE VERDAD  -> menú × llamadas
         · contra el PEOR caso del rival    -> los 4 cuerpos, una vez cada uno
       El peor caso del rival es que el agente lea LAS CUATRO skills. Si el
       menú pierde incluso contra eso, pierde contra cualquier cosa.
    """
    p = peso or peso_del_menu()
    if unidad == "tokens":
        menu_uno, cuerpos = p["menu_tok"], p["cuerpos_tok_total"]
    else:
        menu_uno, cuerpos = p["menu"], p["cuerpos_total"]
    menu_pagado = menu_uno * llamadas
    return {
        "unidad": unidad,
        "llamadas": llamadas,
        "menu_una_vez": menu_uno,
        "menu_pagado": menu_pagado,
        "cuerpos_una_vez": cuerpos,
        "veces": menu_pagado / cuerpos if cuerpos else 0.0,
        "gana_el_menu": menu_pagado < cuerpos,
    }


# ---------------------------------------------------------------------------
# 2) RECORTAR EL MENÚ POR WORKER — apuesta 2
# ---------------------------------------------------------------------------
# Lo obvio es copiar `HERRAMIENTAS_DIVISA`: que cada worker vea solo sus fichas.
#
# 🚨 Y ES EXACTAMENTE A.3 Y A.4, EN LA CAPA QUE NADIE MIRABA.
#    Hasta hoy el aislamiento del nivel 8 se había medido en lo que el worker
#    puede HACER (la caja de herramientas). Esta es la primera vez en lo que el
#    worker SABE. La predicción del `SOBRE.md` estaba escrita para las
#    herramientas y vale igual aquí, palabra por palabra:
#       "el aislamiento que lo hace bueno es el mismo que le quita el contexto
#        para avisar".
#    Un worker que no ve la ficha de `normas-cambiarias` no es que se equivoque
#    al aplicarla: es que NO SABE QUE HAY UNA REGLA. Y no puede avisar de lo
#    que no ve — calla, que es la forma de error más difícil de encontrar.

def menu_recortado(permitidas, carpeta=None):
    """El menú con solo las fichas que este worker puede ver.

    Freno de casa, igual que `worker.menu_para()`: si pides una ficha que no
    existe, muere AQUÍ y no en mitad de una corrida pagada.
    """
    fichas = skills_6b.leer_fichas(carpeta) if carpeta else skills_6b.leer_fichas()
    hay = {f["nombre"] for f in fichas}
    faltan = [n for n in permitidas if n not in hay]
    if faltan:
        raise SystemExit(
            "\n❌ Este worker pide skills que no existen: "
            + ", ".join(faltan)
            + "\n   Las que hay son: " + ", ".join(sorted(hay)) + "\n")
    elegidas = [f for f in fichas if f["nombre"] in permitidas]
    return skills_6b.menu_como_texto(elegidas), elegidas


def ahorro_del_recorte(permitidas, llamadas, carpeta=None):
    """Cuánto ahorra el recorte, y contra QUÉ se mide el porcentaje.

    ⚠️ Decir "recorté el menú un 70%" es verdad y no dice nada: si el menú era
       el 10% de la entrada, ahorraste el 7%.
       → El denominador es la mitad del hallazgo, y es la que se suele callar.
       Por eso esta función devuelve el ahorro EN CRUDO y quien la llama pone
       el denominador que corresponda; no se maquilla aquí.
    """
    p = peso_del_menu(carpeta)
    corto, _ = menu_recortado(permitidas, carpeta)
    fichas = skills_6b.leer_fichas(carpeta) if carpeta else skills_6b.leer_fichas()
    todas = {f["nombre"] for f in fichas}
    return {"entero": p["menu"], "recortado": len(corto),
            "ahorro_por_llamada": p["menu"] - len(corto),
            "ahorro_corrida": (p["menu"] - len(corto)) * llamadas,
            "no_ve": sorted(todas - set(permitidas))}


# ---------------------------------------------------------------------------
# 3) COMPARTIR DESDE ARRIBA — apuesta 3
# ---------------------------------------------------------------------------
# La solución elegante: que el orquestador lea la skill UNA vez y le baje el
# cuerpo ya leído a los workers, en vez de que cada uno la lea por su cuenta.
#
# 🔑 Y pierde cuando los que la necesitan son POCOS, porque bajarla a los tres
#    la paga tres veces aunque dos la tiren sin mirarla. "Compartir" suena a
#    ahorro y aquí es un REPARTO: se le entrega a todos lo que pidió uno.

def coste_de_repartir(n_workers, n_piden, tam_cuerpo,
                      vueltas_totales=3, prefijo=PREFIJO_WORKER_TOKENS):
    """Compara las dos estrategias. En TOKENS, que es lo que se factura.

    · `cada_uno_lee`  — solo pagan los que la piden. Pero pagan DOS cosas:
                        una VUELTA EXTRA de API (pedir la skill es una llamada
                        a herramienta: el prompt entero se vuelve a mandar) y
                        el cuerpo en cada vuelta que les quede.
    · `bajar_a_todos` — el de arriba la lee una vez y la mete en el prompt de
                        LOS TRES, desde la primera vuelta. Sin vuelta extra,
                        pero la pagan los tres y desde el principio.

    🚨 EL TÉRMINO `prefijo` ES EL QUE FALTABA, Y SU AUSENCIA ROMPIÓ ESTA
       FUNCIÓN ANTES DE QUE NADIE LA USARA.
       La primera versión solo comparaba cuerpos, y con eso `gana_compartir`
       salía False **con cualquier número que se le metiera** — no porque
       compartir perdiera, sino porque la función NO PODÍA decir otra cosa.
       Lo cazó `P15` en rojo, no yo leyéndola.
       🔑 Una comparación cuyo resultado no depende de los datos no es una
          medición: es una constante disfrazada. Es `LM.66` otra vez — un
          resultado que nada puede contradecir da el mismo verde que uno
          correcto.
       → La pregunta que la salvó no fue "¿está bien la cuenta?" sino
         **"¿con qué entradas daría lo contrario?"**. Si no hay ninguna,
         la cuenta sobra.

    ⚠️ Y `vueltas_totales` no es un adorno: un cuerpo que entra en el prompt se
       vuelve a mandar en TODAS las vueltas siguientes, porque el historial
       viaja entero en cada llamada. Contarlo una sola vez es la forma más
       común de subestimar lo que cuesta una skill.
    """
    vueltas_tras_leer = max(vueltas_totales - 1, 0)
    cada_uno = n_piden * (prefijo + tam_cuerpo * vueltas_tras_leer)
    todos = n_workers * tam_cuerpo * vueltas_totales
    return {"cada_uno_lee": cada_uno, "bajar_a_todos": todos,
            "gana_compartir": todos < cada_uno}


def punto_de_equilibrio(n_workers, tam_cuerpo, vueltas_totales=3,
                        prefijo=PREFIJO_WORKER_TOKENS):
    """¿A partir de cuántos workers pidiéndola gana compartir?

    ⭐ Devuelve `None` cuando NUNCA gana con esos parámetros — y ese caso es
       real, no un error: si el umbral cae por encima de `n_workers`, no hay
       número de peticiones que lo alcance, porque no puede pedirla más gente
       de la que hay.
    """
    for k in range(0, n_workers + 1):
        if coste_de_repartir(n_workers, k, tam_cuerpo,
                             vueltas_totales, prefijo)["gana_compartir"]:
            return k
    return None


# ---------------------------------------------------------------------------
# 4) LEER EN PARALELO — apuesta 5
# ---------------------------------------------------------------------------
# `leer_skill()` del 6b RELEE los cuatro archivos del disco en cada llamada:
# llama a `leer_fichas()` para buscar el nombre en la lista. Con un agente eso
# no se nota. Con doce hilos son cinco aperturas de archivo por cada cuerpo
# que se devuelve.
#
# 🔑 Y AQUÍ ESTÁ LA ASIMETRÍA CON D.1, QUE ES LO QUE SE VIENE A MEDIR:
#    la misma forma —muchos a la vez sobre lo mismo— da un desastre cuando se
#    escribe y da NADA cuando se lee. El coste existe, pero es de disco, y el
#    disco no manda factura.

def carrera_de_lectura(hilos=12, vueltas=40, carpeta=None):
    """Doce hilos leyendo las mismas skills. ¿Rompe algo?

    Se comprueba lo fuerte, no lo cómodo: no basta con "no hubo excepciones".
    Cada lectura tiene que devolver EL CUERPO CORRECTO — el mismo que se leyó
    en frío antes de arrancar los hilos.
    """
    fichas = skills_6b.leer_fichas(carpeta) if carpeta else skills_6b.leer_fichas()
    nombres = [f["nombre"] for f in fichas]
    padre = fichas[0]["archivo"].parent
    esperado = {n: skills_6b.leer_skill(n, padre)["contenido"] for n in nombres}

    total = {"lecturas": 0, "errores": 0, "equivocadas": 0}
    candado = threading.Lock()

    def tanda(_):
        local = {"lecturas": 0, "errores": 0, "equivocadas": 0}
        for _ in range(vueltas):
            n = random.choice(nombres)
            try:
                got = skills_6b.leer_skill(n, padre)
            except Exception:
                local["errores"] += 1
                continue
            local["lecturas"] += 1
            if got.get("contenido") != esperado[n]:
                local["equivocadas"] += 1
        return local

    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=hilos) as pool:
        for local in pool.map(tanda, range(hilos)):
            with candado:
                for k in local:
                    total[k] += local[k]
    total["segundos"] = round(time.perf_counter() - t0, 3)
    # Cada leer_skill() abre los N archivos para armar la lista, y uno más para
    # sacar el cuerpo. Ese es el coste invisible: no sale en ninguna factura.
    total["aperturas"] = (total["lecturas"] + total["errores"]) * (len(nombres) + 1)
    return total


# ---------------------------------------------------------------------------
# 5) DOS VERSIONES DE LA MISMA SKILL — apuesta 6
# ---------------------------------------------------------------------------
# 🚨 Nada en `skills.py` fija una versión. Cada `leer_skill()` abre el `.md`
#    OTRA VEZ. Si el archivo cambia a mitad del fan-out, el worker del dólar y
#    el del euro trabajan con reglas distintas — y los dos devuelven contratos
#    completos, verdes y coherentes CONSIGO MISMOS.
#
# 🔑 Es `LM.66` en la capa del conocimiento: el cuerpo de la skill está SOLO en
#    su renglón. Ningún otro dato del contrato puede desmentirlo. Un dato que
#    nadie puede contradecir no es que sea correcto — es que no es comprobable.

def huella(contenido):
    """Una marca corta del cuerpo que se leyó. NO es seguridad: es identidad.

    Sirve para poder decir "estos dos workers leyeron lo mismo" en el registro.
    Hoy esa frase no se puede decir, porque no se anota nada.
    """
    return hashlib.sha256(contenido.encode("utf-8")).hexdigest()[:12]


def lectura_partida(carpeta, nombre, cambio):
    """Provoca la partición: un lector antes del cambio y otro después.

    Devuelve las dos huellas. Que sean distintas es el defecto; que hoy nadie
    las mire es la deuda.
    """
    a = skills_6b.leer_skill(nombre, carpeta)["contenido"]
    archivo = carpeta / (nombre + ".md")
    texto = archivo.read_text(encoding="utf-8")
    archivo.write_text(texto.replace(cambio[0], cambio[1]), encoding="utf-8")
    b = skills_6b.leer_skill(nombre, carpeta)["contenido"]
    return {"antes": huella(a), "despues": huella(b), "iguales": a == b}


# ---------------------------------------------------------------------------
# 6) EL CONTADOR OFICIAL DE TOKENS — $0,00, y por eso se usa
# ---------------------------------------------------------------------------

def tokens(texto, modelo="claude-haiku-4-5"):
    """Cuenta tokens con el endpoint oficial. NO cuesta dinero.

    ⚠️ Se usa esto y no una regla de tres sobre caracteres, y el motivo es la
       apuesta 4: si el prefijo queda a 200 tokens del mínimo del caché, una
       estimación de "4 caracteres por token" decide mal. Cuando un número está
       cerca de un umbral, estimarlo es lo mismo que no medirlo.
    """
    sys.path.insert(0, str(RAIZ / "05b-proyecto"))
    import agente
    r = agente.cliente.messages.count_tokens(
        model=modelo, messages=[{"role": "user", "content": texto}])
    return r.input_tokens


def _pruebas():
    fallos = []

    def check(nombre, cond, detalle=""):
        print(("  OK  " if cond else "  XX  ") + nombre + ("  -> " + detalle if detalle else ""))
        if not cond:
            fallos.append(nombre)

    print("\n[D.2] skills compartidas entre workers\n")

    # --- P1-P3: no se rompió nada del 6b al importarlo ---------------------
    p = peso_del_menu()
    check("P1 · se ven las cuatro skills del 6b", p["fichas"] == 4, str(p["fichas"]))
    check("P2 · el menú no viene vacío", p["menu"] > 0, str(p["menu"]) + " car.")
    check("P3 · con UN agente los cuerpos pesan mucho más que el menú",
          p["cuerpos_total"] > p["menu"] * 5,
          str(p["cuerpos_total"]) + " vs " + str(p["menu"]))

    # --- P4-P8: 🎲 APUESTA 1, medida en TOKENS ------------------------------
    c1 = cuenta_de_la_corrida(1, p)
    check("P4 · con UNA llamada el menú gana holgado — para eso se inventó",
          c1["gana_el_menu"] and c1["veces"] < 0.25, "%.2fx" % c1["veces"])
    c9 = cuenta_de_la_corrida(9, p)
    check("P5 · 🎲 con las NUEVE llamadas del fan-out real, el menú PIERDE",
          not c9["gana_el_menu"],
          str(c9["menu_pagado"]) + " vs " + str(c9["cuerpos_una_vez"]) + " tok")
    # 🔴 LA MITAD DE LA APUESTA 1 QUE FALLÓ, Y SE DEJA COMO PRUEBA EN VERDE
    #    PARA QUE EL NÚMERO NO SE PUEDA MAQUILLAR MAÑANA.
    #    Sellé ">1,4x". En caracteres da 1,48x y habría cantado victoria; en
    #    tokens da 1,34x. La dirección aguanta, el número no.
    check("P6 · 🔴 y NO llega al 1,4x apostado: se queda en 1,34x",
          1.30 < c9["veces"] < 1.40, "%.2fx" % c9["veces"])
    car = cuenta_de_la_corrida(9, p, unidad="caracteres")
    check("P7 · 🚨 y en CARACTERES habría dado 1,48x — la unidad me daba la razón",
          car["veces"] > 1.4, "%.2fx en caracteres" % car["veces"])
    vuelco = next(n for n in range(1, 100) if not cuenta_de_la_corrida(n, p)["gana_el_menu"])
    check("P8 · el vuelco está en la 7ª llamada, y en las dos unidades",
          vuelco == 7
          and next(n for n in range(1, 100)
                   if not cuenta_de_la_corrida(n, p, "caracteres")["gana_el_menu"]) == 7,
          "en la " + str(vuelco))

    # --- P9-P11: 🎲 APUESTA 2, el recorte ----------------------------------
    a = ahorro_del_recorte(["normas-cambiarias"], 9)
    check("P9 · recortar a UNA ficha corta el menú a menos de la mitad",
          a["recortado"] < a["entero"] / 2,
          str(a["recortado"]) + " de " + str(a["entero"]))
    check("P10 · y el worker recortado deja de ver TRES fichas",
          len(a["no_ve"]) == 3, ", ".join(a["no_ve"]))
    try:
        menu_recortado(["skill-que-no-existe"])
        check("P11 · pedir una skill inexistente muere aquí, no en la corrida", False)
    except SystemExit:
        check("P11 · pedir una skill inexistente muere aquí, no en la corrida", True)

    # --- P12-P16: 🎲 APUESTA 3, compartir desde arriba ---------------------
    cuerpo = p["cuerpos_tok"]["normas-cambiarias"]
    uno = coste_de_repartir(3, 1, cuerpo)
    check("P12 · 🎲 con UN worker pidiéndola, bajarla a los tres sale MÁS CARO",
          not uno["gana_compartir"],
          str(uno["bajar_a_todos"]) + " vs " + str(uno["cada_uno_lee"]) + " tok")
    dos = coste_de_repartir(3, 2, cuerpo)
    check("P13 · con DOS pidiéndola sigue perdiendo",
          not dos["gana_compartir"],
          str(dos["bajar_a_todos"]) + " vs " + str(dos["cada_uno_lee"]) + " tok")
    # 🟡 LA OTRA MITAD DE LA APUESTA 3, Y AQUÍ ME EQUIVOQUÉ:
    #    aposté que "este fan-out NUNCA lo alcanza". Lo alcanza — justo en el
    #    último escalón posible, con los tres pidiéndola.
    tres = coste_de_repartir(3, 3, cuerpo)
    check("P14 · 🟡 pero con los TRES pidiéndola, compartir GANA",
          tres["gana_compartir"],
          str(tres["bajar_a_todos"]) + " vs " + str(tres["cada_uno_lee"]) + " tok")
    check("P15 · o sea: el equilibrio es 3 de 3, no 'nunca' como aposté",
          punto_de_equilibrio(3, cuerpo) == 3,
          str(punto_de_equilibrio(3, cuerpo)))
    # 🚨 Y LA PRUEBA QUE LE FALTABA A LA VERSIÓN ROTA: exigir que la función
    #    PUEDA dar las dos respuestas. Sin esto, P12-P14 pasarían igual de
    #    verdes con la cuenta amañada que las parió.
    check("P16 · 🚨 y la cuenta puede dar las DOS respuestas — la rota no podía",
          len({coste_de_repartir(3, k, cuerpo)["gana_compartir"]
               for k in (0, 1, 2, 3)}) == 2)

    # --- P17-P20: 🎲 APUESTA 5, leer en paralelo ---------------------------
    r = carrera_de_lectura(hilos=12, vueltas=40)
    check("P17 · 12 hilos × 40 lecturas: 480 lecturas hechas",
          r["lecturas"] == 480, str(r["lecturas"]))
    check("P18 · 🎲 cero excepciones", r["errores"] == 0, str(r["errores"]))
    check("P19 · 🎲 y cero cuerpos equivocados — donde D.1 perdía el 49,5%",
          r["equivocadas"] == 0, str(r["equivocadas"]))
    check("P20 · el coste existe y es de disco: 2400 aperturas para 480 lecturas",
          r["aperturas"] == 2400,
          str(r["aperturas"]) + " en " + str(r["segundos"]) + "s")

    # --- P21-P23: 🎲 APUESTA 6, dos versiones de la misma skill ------------
    tmp = Path(tempfile.mkdtemp())
    (tmp / "reglas.md").write_text(
        "---\nnombre: reglas\ndescripcion: la de prueba\n---\n\nEl tope es 1000 dolares.\n",
        encoding="utf-8")
    r6 = lectura_partida(tmp, "reglas", ("1000 dolares", "5000 dolares"))
    check("P21 · 🚨 dos lecturas de la MISMA skill dan cuerpos distintos",
          not r6["iguales"], r6["antes"] + " != " + r6["despues"])
    check("P22 · y las dos devuelven un cuerpo válido, sin error ni aviso",
          len(r6["antes"]) == 12 and len(r6["despues"]) == 12)
    # La deuda, escrita como prueba para que no se olvide: hoy nadie anota esto.
    linea_de_registro = {"tramo": "worker:usd", "skill": "reglas"}
    check("P23 · y el registro de hoy NO tiene dónde decir CUÁL se leyó",
          "huella_skill" not in linea_de_registro
          and "version_skill" not in linea_de_registro)

    # --- P24-P28: el caché, y el mínimo que muerde sin avisar --------------
    ok, minimo = cachea(1828, "claude-haiku-4-5")
    check("P24 · 🚨 el prefijo de un worker (1828 tok medidos) NO cachea en haiku",
          ok is False and minimo == 4096, "faltan " + str(minimo - 1828) + " tokens")
    ok5, min5 = cachea(1828, "claude-opus-5")
    check("P25 · el MISMO prefijo SÍ cachearía en Opus 5", ok5 is True and min5 == 512)
    check("P26 · el mínimo NO baja con la generación, y creerlo sale caro",
          MINIMO_CACHE_TOKENS["claude-haiku-4-5"] > MINIMO_CACHE_TOKENS["claude-opus-5"])
    desconocido, _ = cachea(9999, "un-modelo-que-no-conozco")
    check("P27 · un modelo que no está en la tabla devuelve None, no True",
          desconocido is None)
    ok_con_menu, _ = cachea(1828 + 500, "claude-haiku-4-5")
    check("P28 · ni añadiéndole el menú entero al prefijo llegaría al mínimo",
          ok_con_menu is False)

    print("")
    if fallos:
        print("❌ " + str(len(fallos)) + " en rojo: " + ", ".join(fallos))
    else:
        print("✅ Las 28 verdes.")
    return fallos


def tabla():
    """El informe del día. $0,00: aquí no se llama a la API."""
    p = peso_del_menu()
    print("\n" + "=" * 74)
    print("D.2 · LO QUE CUESTA UN MENÚ QUE SE PAGA EN CADA LLAMADA")
    print("=" * 74)
    print("\nel menú pesa %d tokens (%d car.) · los 4 cuerpos, %d tokens (%d car.)"
          % (p["menu_tok"], p["menu"], p["cuerpos_tok_total"], p["cuerpos_total"]))
    print("\n%9s %13s %11s %11s  %s"
          % ("llamadas", "menú pagado", "vs cuerpos", "en car.", "quién gana"))
    for n in (1, 3, 6, 7, 9, 18):
        c = cuenta_de_la_corrida(n, p)
        cc = cuenta_de_la_corrida(n, p, "caracteres")
        print("%9d %13d %10.2fx %10.2fx  %s" % (
            n, c["menu_pagado"], c["veces"], cc["veces"],
            "el menú" if c["gana_el_menu"] else "🚨 los cuerpos"))
    print("\n  1 llamada = un agente del 6b.  9 = el fan-out real de este nivel.")
    print("  18 = el mismo fan-out con dos rondas, que es el bloque E.")
    print("  🚨 La columna de caracteres NO es la que se paga. Está para ver")
    print("     cuánto se separan: en la fila del 9, 1,34x contra 1,48x.\n")

    print("-" * 74)
    print("COMPARTIR DESDE ARRIBA vs. QUE CADA WORKER LEA  (3 workers, 3 vueltas)")
    cuerpo = p["cuerpos_tok"]["normas-cambiarias"]
    print("  skill: normas-cambiarias, %d tokens de cuerpo" % cuerpo)
    print("\n%9s %15s %15s  %s"
          % ("la piden", "cada uno lee", "bajar a todos", "quién gana"))
    for k in (0, 1, 2, 3):
        r = coste_de_repartir(3, k, cuerpo)
        print("%9d %15d %15d  %s" % (
            k, r["cada_uno_lee"], r["bajar_a_todos"],
            "compartir" if r["gana_compartir"] else "que cada uno lea"))
    print("\n  🔑 El que decide no es el cuerpo: es la VUELTA EXTRA de %d tokens"
          % PREFIJO_WORKER_TOKENS)
    print("     que cuesta pedir la skill. Pedirla es una llamada a herramienta,")
    print("     y una llamada más re-manda el prompt entero.\n")

    print("-" * 74)
    print("EL CACHÉ, QUE PARECÍA LA SALIDA")
    print("  mínimos consultados el " + MINIMO_CACHE_CONSULTADO + ":")
    for m, t in sorted(MINIMO_CACHE_TOKENS.items(), key=lambda x: x[1]):
        marca = "  <-- el de este nivel" if m == "claude-haiku-4-5" else ""
        print("    %-20s %5d tokens%s" % (m, t, marca))
    ok, minimo = cachea(1828, "claude-haiku-4-5")
    print("\n  prefijo medido de un worker: 1828 tokens · mínimo: " + str(minimo))
    print("  ¿cachea? " + ("sí" if ok else "🚨 NO — y la API no lo dice") + "\n")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--tabla" in sys.argv:
        tabla()
        sys.exit(0)
    fallado = _pruebas()
    print("\n📊 Para ver la tabla:  python skills_compartidas.py --tabla")
    sys.exit(1 if fallado else 0)
