"""supervisor.py — B.4 del nivel 8: el que juzga y reenvía.

    LO QUE B.3 DEJÓ SOBRE LA MESA

B.3 midió que un juez **solo funciona con la respuesta correcta escrita de
antemano**, y en vivo no la hay. Su última frase apuntaba a un sitio: *si no hay
etiqueta de oro, el único testigo posible es el propio especialista diciendo
«esto no es lo mío»*.

⭐ Así que B.4 no pregunta cómo se construye un supervisor. Pregunta si un
   supervisor puede saber algo que el juez de B.3 no podía.

🔒 Las tres apuestas están selladas y COMMITEADAS en `README.md`
   (*«🎲 B.4 — EL SUPERVISOR»*) antes de escribir este archivo.


    LOS DOS EXPERIMENTOS, CADA UNO DE UNA SOLA VARIABLE

  1) SUPERVISOR CIEGO  contra  SUPERVISOR QUE VE EL ORIGINAL
     La misma respuesta mal enrutada, dos jueces. Cambia UNA cosa: si el juez
     ve o no el mensaje que escribió el usuario.

  2) REINTENTO CIEGO  contra  REINTENTO INFORMADO
     El mismo worker, dos veces. Cambia UNA cosa: si el segundo encargo lleva
     escrito QUÉ estuvo mal.

🚨 **LA PRESA SE INYECTA A PROPÓSITO, y eso es lo que le faltó a B.3.** Allí
   ninguno de los dos routers falló en nada puntuable, así que el cazador quedó
   sin estrenar. Aquí el error de enrutado se mete a mano: se coge el caso
   `n3-a` del banco de B.3 —*«una factura de un proveedor de Alemania»*, cuyo
   destino correcto es `eur`— y se manda al worker del **dólar**.


    ⚠️ EL PRIMER SOSPECHOSO DE ESTAR CIEGO, NOMBRADO ANTES DE ESCRIBIRLO

Cuatro sesiones seguidas lo ciego ha sido lo escrito ese mismo día: el
verificador (B.1), la línea de tiempo (B.2), la etiqueta de oro (B.3).

🚨 **En B.4 el sospechoso es EL ERROR INYECTADO.** Si el cebo es más burdo que
   un fallo real, el supervisor lo caza por lo obvio y el resultado no dice nada.
   → Por eso la respuesta que juzgan los dos supervisores **la escribe un worker
     de verdad, corriendo de verdad, y se GRABA**. No la escribo yo. Un cebo
     redactado por quien monta el experimento mide al cebo.
   → Y por eso los dos supervisores ven **exactamente el mismo texto grabado**:
     si cada uno viera su propia corrida, no habría una variable, habría dos.


    CÓMO SE CORRE

    python supervisor.py            -> LAS PRUEBAS. Gratis. $0,00
    python supervisor.py --cebo     -> corre el worker mal enrutado y lo GRABA. ~$0,007
    python supervisor.py --exp1     -> los dos supervisores sobre el cebo. ~$0,001
    python supervisor.py --exp2     -> reintento ciego contra informado. ~$0,015

📌 Sin argumentos corre las PRUEBAS. Lo que cuesta dinero se pide con todas las
   letras — igual que `fan_out.py` y `router.py`.
"""

import json
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "05b-proyecto"))

import agente          # noqa: E402
import worker          # noqa: E402


# ---------------------------------------------------------------------------
# 1) CONFIGURACIÓN
# ---------------------------------------------------------------------------

MODELO = agente.MODELO

REGISTRO = AQUI / f"registro_supervisor_{MODELO}.jsonl"

# El cebo grabado. Se corre UNA vez y se guarda, por dos razones distintas:
#   1) barato: no se vuelve a pagar el worker en cada prueba de supervisor;
#   2) 🔑 y la que de verdad importa: los dos supervisores tienen que ver EL
#      MISMO TEXTO. Si cada uno viera su propia corrida del worker, el
#      experimento tendría dos variables y no diría nada.
CEBO = AQUI / f"cebo_mal_enrutado_{MODELO}.json"

# --- LA PRESA, tomada tal cual del banco de B.3 ----------------------------
# `n3-a`, cuyo destino correcto es `eur` y donde el router de `if` se abstuvo.
MENSAJE_ORIGINAL = ("Me llegó una factura de un proveedor de Alemania por 400. "
                    "¿Cuánto es en pesos?")

# Lo que un router que decidió MAL le habría escrito al worker. Fíjate en que
# el encargo es impecable: bien redactado, sin ambigüedad, y equivocado.
ENCARGO_MAL = "Convierte 400 dólares estadounidenses a pesos colombianos."

DESTINO_CORRECTO = "eur"
DESTINO_USADO = "usd"

# Tolerancia de la comprobación aritmética, en pesos. No es cero porque las
# herramientas redondean; no es enorme porque entonces no comprobaría nada.
TOLERANCIA_PESOS = 1.0


# ---------------------------------------------------------------------------
# 2) REGISTRO
# ---------------------------------------------------------------------------

_CANDADO_REGISTRO = threading.Lock()


def anotar(evento, **datos):
    """Una línea JSON, un hecho."""
    linea = {"hora": datetime.now(timezone.utc).isoformat(timespec="seconds"),
             "evento": evento}
    linea.update(datos)
    with _CANDADO_REGISTRO:
        with open(REGISTRO, "a", encoding="utf-8") as f:
            f.write(json.dumps(linea, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# 3) EL REVISOR DETERMINISTA — y aquí la apuesta 1 se rompió sola
# ---------------------------------------------------------------------------
#
# 🚨 LO QUE PASÓ AL ABRIR `worker.py` PARA ESCRIBIR ESTO, y se anota porque
#    cambia la apuesta ANTES de correr nada:
#
#    La apuesta 1 dice que un supervisor sin herramientas «no puede verificar la
#    verdad pero sí la coherencia, y la aritmética se comprueba multiplicando».
#    Cierto. Pero el contrato de A.3 (`contrato_divisa`) ya trae `monto`, `tasa`
#    y `pesos` en CAMPOS SEPARADOS.
#
# ⭐ Entonces la comprobación aritmética no necesita un modelo: son tres líneas
#    de Python y cuesta $0,00.
#
# 🔑 Y eso reordena la pregunta entera del bloque: **la parte del juicio que se
#    puede VERIFICAR es exactamente la parte que NO necesita un modelo. La parte
#    que necesita un modelo es exactamente la que no se puede verificar.**
#    Es la misma forma que B.1 («el pipeline eran tres líneas») y B.2 («el
#    reparto eran diez»), una capa más arriba.
#
# 📌 Se escribe aquí y no en la apuesta: la apuesta no se toca.

def revisar_contrato(res):
    """Todo lo que se puede objetar SIN un modelo y SIN tocar la red.

    Devuelve la lista de quejas. Lista vacía = nada que objetar por esta vía.

    ⚠️ Y lo que NO puede hacer, dicho aquí para que nadie lo lea como más de lo
       que es: no sabe si la tasa es la de verdad. Solo sabe si la cuenta cierra
       con la tasa que el propio worker declaró. **Un número inventado pero
       coherente consigo mismo pasa por aquí sin despeinarse.**
    """
    quejas = []
    datos = res.get("datos") or {}

    # a) Campos que el contrato no pudo llenar. El worker YA los calcula.
    if res.get("faltan"):
        quejas.append(f"faltan campos del contrato: {', '.join(res['faltan'])}")

    # b) 🔑 LA ARITMÉTICA. Tres líneas, cero modelos, cero dólares.
    monto, tasa, pesos = datos.get("monto"), datos.get("tasa"), datos.get("pesos")
    if None not in (monto, tasa, pesos):
        esperado = monto * tasa
        if abs(esperado - pesos) > TOLERANCIA_PESOS:
            quejas.append(f"la cuenta no cierra: {monto} × {tasa} = {esperado:,.2f}"
                          f", pero dice {pesos:,.2f}")

    # c) El worker mismo avisó de que terminó mal. Es un dato que ya existía y
    #    que un supervisor descuidado ignoraría por mirar solo el texto.
    if not res.get("ok"):
        quejas.append(f"el worker no terminó bien: {res.get('motivo')}")

    return quejas


# ---------------------------------------------------------------------------
# 4) EL SUPERVISOR CON MODELO — la variable del experimento 1
# ---------------------------------------------------------------------------

SISTEMA_SUPERVISOR = (
    "Eres un supervisor de calidad. Te doy el trabajo que hizo un especialista "
    "y tienes que decir si SIRVE o NO SIRVE. "
    "Tú no tienes forma de consultar tasas de cambio: no puedes comprobar si "
    "una cifra es la real, y no debes intentarlo. "
    "Responde en DOS líneas exactamente, sin nada más:\n"
    "VEREDICTO: sirve   (o)   VEREDICTO: no sirve\n"
    "MOTIVO: una frase corta"
)


def _sobre_ciego(encargo, respuesta):
    """Lo que ve el supervisor CIEGO: el encargo y la respuesta. Nada más.

    ⭐ Esto NO es un supervisor mal hecho: es el supervisor natural. Cuando
       escribes «el orquestador revisa lo que devolvió el worker», esto es lo
       que sale. El mensaje original ni siquiera se te ocurre pasarlo, porque
       el worker nunca lo vio.
    """
    return (f"ENCARGO QUE SE LE DIO AL ESPECIALISTA:\n{encargo}\n\n"
            f"RESPUESTA DEL ESPECIALISTA:\n{respuesta}\n\n"
            f"¿Sirve este trabajo?")


def _sobre_con_original(encargo, respuesta, original):
    """Lo mismo, MÁS el mensaje que escribió el usuario.

    🔑 La diferencia con el de arriba es UNA sección de texto. Toda la apuesta 3
       cuelga de si esa sección cambia el veredicto.
    """
    return (f"LO QUE PIDIÓ EL USUARIO:\n{original}\n\n"
            f"ENCARGO QUE SE LE DIO AL ESPECIALISTA:\n{encargo}\n\n"
            f"RESPUESTA DEL ESPECIALISTA:\n{respuesta}\n\n"
            f"¿Sirve este trabajo para lo que pidió el usuario?")


# Pistas de que un motivo habla DEL ENRUTADO y no de otra cosa.
#
# 📌 Es un `if` sobre palabras clave, con el límite exacto que B.3 midió: caza
#    lo que está ESCRITO, no lo que hay que inferir. Se acepta a sabiendas
#    porque aquí es una PISTA para leer más rápido, no el veredicto — y esa
#    diferencia es justo la que este archivo casi pierde.
PISTAS_DE_ENRUTADO = ("euro", "alemania", "moneda equivocada", "otra moneda",
                      "no corresponde", "no era", "distinta moneda")


def habla_del_enrutado(motivo):
    """¿El motivo del rechazo menciona el error de enrutado, o rechazó por otra cosa?

    🔑 Existe porque un booleano `sirve/no sirve` mete en la misma casilla dos
       rechazos por razones opuestas. Un supervisor que rechaza lo correcto por
       un motivo inventado NO está cazando nada: está acertando la casilla.
    """
    m = (motivo or "").lower()
    return any(p in m for p in PISTAS_DE_ENRUTADO)


def supervisar(encargo, respuesta, original=None, etiqueta="?", verboso=True):
    """Una llamada. Devuelve (sirve, motivo, gasto_usd).

    Si `original` es None, el supervisor es CIEGO. Si trae texto, ve el mensaje
    del usuario. Es la única diferencia entre los dos brazos del experimento 1.
    """
    sobre = (_sobre_ciego(encargo, respuesta) if original is None
             else _sobre_con_original(encargo, respuesta, original))

    for intento in range(1, agente.REINTENTOS_PROPIOS + 1):
        try:
            r = agente.cliente.messages.create(
                model=MODELO,
                max_tokens=120,
                system=SISTEMA_SUPERVISOR,
                messages=[{"role": "user", "content": sobre}],
            )
            gasto = agente.costo(r.usage)
            texto = "".join(b.text for b in r.content if b.type == "text").strip()

            # ⚠️ Leer el veredicto del texto, no confiar en que obedeció el
            #    formato. Un fallo de FORMATO leído como «no sirve» sería el
            #    instrumento midiendo su propio ruido (`LM.15`).
            sirve = None
            motivo = ""
            for linea in texto.splitlines():
                bajo = linea.strip().lower()
                if bajo.startswith("veredicto:"):
                    resto = bajo.split(":", 1)[1].strip()
                    if resto.startswith("no"):
                        sirve = False
                    elif resto.startswith("sirve"):
                        sirve = True
                elif bajo.startswith("motivo:"):
                    motivo = linea.split(":", 1)[1].strip()

            anotar("supervision", etiqueta=etiqueta, ve_original=original is not None,
                   crudo=texto, sirve=sirve, motivo=motivo,
                   entrada=r.usage.input_tokens, salida=r.usage.output_tokens,
                   costo_usd=round(gasto, 6), stop_reason=r.stop_reason)

            if sirve is None and verboso:
                print(f"      ⚠️ no se pudo leer el veredicto: «{texto[:60]}»")

            return sirve, motivo, gasto

        except agente.REINTENTABLES as fallo:
            if intento == agente.REINTENTOS_PROPIOS:
                anotar("supervision_fallo", etiqueta=etiqueta, error=str(fallo))
                raise
            time.sleep(2 ** intento)


# ---------------------------------------------------------------------------
# 5) EL CEBO — un worker de verdad, mal enrutado, GRABADO
# ---------------------------------------------------------------------------

def crear_cebo(verboso=True):
    """Corre el worker del dólar con el encargo equivocado y guarda el resultado.

    💰 Cuesta ~$0,00724 (medido en B.2). Se corre UNA vez.

    🚨 POR QUÉ NO ESCRIBO YO LA RESPUESTA: porque entonces el experimento mide
       mi redacción. El aviso está en la cabecera de este archivo — un cebo más
       burdo que un fallo real hace que el supervisor lo cace por lo obvio.
       El worker de verdad produce una respuesta de verdad: impecable, con
       fuente y fecha, y en la moneda equivocada.
    """
    print(f"\n  Corriendo el worker «{DESTINO_USADO}» con el encargo EQUIVOCADO…")
    print(f"  original: «{MENSAJE_ORIGINAL}»")
    print(f"  encargo : «{ENCARGO_MAL}»")
    print(f"  correcto era: {DESTINO_CORRECTO}\n")

    res = worker.correr_worker(ENCARGO_MAL, nombre=DESTINO_USADO, verboso=verboso)

    guardado = {"mensaje_original": MENSAJE_ORIGINAL, "encargo": ENCARGO_MAL,
                "destino_correcto": DESTINO_CORRECTO, "destino_usado": DESTINO_USADO,
                "resultado": res}
    CEBO.write_text(json.dumps(guardado, ensure_ascii=False, indent=2),
                    encoding="utf-8")
    anotar("cebo_creado", coste_usd=res["coste_usd"], texto=res["texto"])
    print(f"\n  ✅ cebo grabado en {CEBO.name}  (${res['coste_usd']:.6f})")
    return guardado


def cargar_cebo():
    """Lee el cebo grabado, o explica cómo crearlo. No lo crea solo.

    📌 No lo crea solo A PROPÓSITO: crear el cebo cuesta dinero, y una función
       que gasta sin que se lo pidan es exactamente lo que `fan_out.py` y
       `router.py` evitan con su modo por defecto.
    """
    if not CEBO.exists():
        print(f"\n  ⚠️ no hay cebo grabado ({CEBO.name}).")
        print("     Córrelo primero:  python supervisor.py --cebo   (~$0,007)")
        return None
    return json.loads(CEBO.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# 6) EXPERIMENTO 1 — ciego contra el que ve el original
# ---------------------------------------------------------------------------

def experimento_1():
    """La misma respuesta, dos jueces. Cambia UNA cosa: ver el original."""
    cebo = cargar_cebo()
    if cebo is None:
        return 1

    res = cebo["resultado"]
    respuesta = res["texto"]

    print("\n" + "=" * 72)
    print("  EXPERIMENTO 1 — ¿caza el supervisor un enrutado equivocado?")
    print("=" * 72)
    print(f"\n  usuario  : «{cebo['mensaje_original']}»")
    print(f"  encargo  : «{cebo['encargo']}»   ← MAL: era {cebo['destino_correcto']}")
    print(f"  respuesta: «{respuesta}»\n")

    # --- Primero, GRATIS: el revisor determinista --------------------------
    quejas = revisar_contrato(res)
    print("  ── revisor determinista (sin modelo, $0,00) ──")
    if quejas:
        for q in quejas:
            print(f"     ❌ {q}")
    else:
        print("     ✅ sin objeciones: campos completos y la cuenta cierra")
    print("     🔑 y no podía ser de otra forma: el worker del dólar hizo un")
    print("        trabajo impecable. El error no está en la respuesta.")

    # --- Ahora los dos supervisores ----------------------------------------
    print("\n  ── los dos supervisores ──")
    gasto = 0.0

    sirve_c, motivo_c, g = supervisar(cebo["encargo"], respuesta,
                                      original=None, etiqueta="ciego")
    gasto += g
    print(f"\n     CIEGO           (ve encargo + respuesta)")
    print(f"     veredicto: {'sirve' if sirve_c else 'NO sirve'}   ${g:.6f}")
    print(f"     motivo   : {motivo_c}")

    sirve_o, motivo_o, g = supervisar(cebo["encargo"], respuesta,
                                      original=cebo["mensaje_original"],
                                      etiqueta="con_original")
    gasto += g
    print(f"\n     CON EL ORIGINAL (ve además lo que pidió el usuario)")
    print(f"     veredicto: {'sirve' if sirve_o else 'NO sirve'}   ${g:.6f}")
    print(f"     motivo   : {motivo_o}")

    # --- El veredicto del experimento --------------------------------------
    #
    # 🚨 ESTE BLOQUE NACIÓ CIEGO Y SE ARREGLÓ EL MISMO DÍA. Se deja escrito
    #    porque es el hallazgo de B.4, no una anécdota.
    #
    #    La primera versión comparaba `sirve_c` y `sirve_o`, dos booleanos. En
    #    la corrida real los dos supervisores rechazaron, así que imprimió
    #    «los DOS rechazan: la apuesta falla». Y era MENTIRA:
    #
    #      ciego         -> rechazó por «la fecha es futura»  ← NADA que ver
    #      con original  -> rechazó por «pidió euros, convirtió dólares» ← EXACTO
    #
    # 🔑 **Un rechazo no es un dato: el dato es POR QUÉ.** Dos rechazos por
    #    motivos opuestos entran en la misma casilla booleana, igual que el
    #    `correct: bool` de la sesión 83 y que el juez de cuatro veredictos que
    #    `router.py` construyó AYER a propósito para evitarlo.
    #
    # ⚠️ Y la parte incómoda: el booleano se coló justo en la función que
    #    evalúa mi propia apuesta. Quinta sesión seguida en que lo ciego es lo
    #    escrito ese mismo día.
    print("\n  ── QUÉ DICE ESTO DE LA APUESTA 3 ──")
    print("     apostado: el ciego no caza EL ENRUTADO; el que ve el original, sí")
    print(f"     veredictos: ciego {'aprueba' if sirve_c else 'rechaza'} · "
          f"con original {'aprueba' if sirve_o else 'rechaza'}")
    print("     ⚠️ y los veredictos NO bastan. Lo que decide es el MOTIVO:")

    print(f"\n     ciego         → {'HABLA' if habla_del_enrutado(motivo_c) else 'NO habla'}"
          f" del enrutado: «{motivo_c}»")
    print(f"     con original  → {'HABLA' if habla_del_enrutado(motivo_o) else 'NO habla'}"
          f" del enrutado: «{motivo_o}»")

    if not habla_del_enrutado(motivo_c) and habla_del_enrutado(motivo_o):
        print("\n     ✅ la apuesta se cumple: SOLO el que ve el original nombra")
        print("        el enrutado. Que el ciego rechazara por otra cosa no es")
        print("        cazarlo — es acertar la casilla por el motivo equivocado.")
    elif habla_del_enrutado(motivo_c):
        print("\n     ❌ el ciego SÍ nombra el enrutado: la apuesta falla")
    else:
        print("\n     ⁉️ ninguno lo nombra: leer los dos motivos enteros")

    print("\n     📌 Esta pista es un `if` sobre palabras clave, con el límite")
    print("        que B.3 midió: caza lo que está ESCRITO, no lo que se infiere.")
    print("        El motivo entero está arriba y en el registro. Léelo.")

    print(f"\n  gasto del experimento 1: ${gasto:.6f}")
    anotar("exp1_fin", ciego_sirve=sirve_c, original_sirve=sirve_o,
           quejas_deterministas=quejas, gasto_usd=round(gasto, 6))
    return 0


# ---------------------------------------------------------------------------
# 7) EXPERIMENTO 2 — reintento ciego contra reintento informado
# ---------------------------------------------------------------------------

def experimento_2():
    """El mismo worker, dos veces. Cambia UNA cosa: si el encargo dice qué falló.

    💰 Dos corridas de worker: ~$0,0145.
    """
    cebo = cargar_cebo()
    if cebo is None:
        return 1

    print("\n" + "=" * 72)
    print("  EXPERIMENTO 2 — ¿vale algo un reintento que no dice qué falló?")
    print("=" * 72)

    # --- Brazo A: reintento CIEGO. El mismo encargo, otra vez. -------------
    print("\n  ── A) REINTENTO CIEGO: el mismo encargo, sin más ──")
    print(f"     «{cebo['encargo']}»\n")
    a = worker.correr_worker(cebo["encargo"], nombre=DESTINO_USADO)

    # --- Brazo B: reintento INFORMADO. El encargo + el motivo. -------------
    #
    # ⚠️ El texto del rechazo se escribe aquí y es parte del experimento, no
    #    decoración: dice QUÉ estuvo mal sin decir qué hacer. Si le dijera «usa
    #    euros», el reintento no mediría nada — le habría dado la respuesta.
    encargo_informado = (
        f"{cebo['encargo']}\n\n"
        f"AVISO: un supervisor rechazó tu respuesta anterior. Lo que el usuario "
        f"pidió en realidad fue: «{cebo['mensaje_original']}». "
        f"Si este encargo no corresponde a lo que pidió el usuario, dilo "
        f"claramente en vez de responderlo."
    )
    print("\n  ── B) REINTENTO INFORMADO: el encargo + qué estuvo mal ──")
    print(f"     (se le dice QUÉ falló, NO qué hacer)\n")
    b = worker.correr_worker(encargo_informado, nombre=DESTINO_USADO)

    # --- Comparación --------------------------------------------------------
    print("\n  ── COMPARACIÓN ──")
    print(f"     A ciego     : ${a['coste_usd']:.6f}  → {a['texto'][:90]}")
    print(f"     B informado : ${b['coste_usd']:.6f}  → {b['texto'][:90]}")
    print("\n  🔑 Lo que hay que mirar NO es cuál respuesta es más bonita:")
    print("     es si B se DIO CUENTA de que el encargo no era suyo.")
    print("     Un worker que devuelve el trabajo es el testigo que B.3 buscaba.")

    total = a["coste_usd"] + b["coste_usd"]
    print(f"\n  gasto del experimento 2: ${total:.6f}")
    anotar("exp2_fin", ciego_texto=a["texto"], informado_texto=b["texto"],
           gasto_usd=round(total, 6))
    return 0


# ---------------------------------------------------------------------------
# 8) LAS PRUEBAS — gratis
# ---------------------------------------------------------------------------

def _pruebas():
    fallos = []

    def check(nombre, condicion, detalle=""):
        estado = "✅" if condicion else "❌"
        extra = f"  → {detalle}" if detalle and not condicion else ""
        print(f"  {estado} {nombre}{extra}")
        if not condicion:
            fallos.append(nombre)

    print("\n  PRUEBAS — $0.00\n")

    bueno = {"datos": {"monto": 400, "tasa": 4200.0, "pesos": 1680000.0,
                       "moneda": "USD", "fuente": "x", "fecha": "y"},
             "faltan": [], "ok": True, "motivo": None}

    # 1) Un contrato sano no genera quejas.
    check("1. un contrato completo y cuadrado no tiene quejas",
          revisar_contrato(bueno) == [])

    # 2) 🔑 LA ARITMÉTICA MUERDE. Es la parte de la apuesta 1 que resultó no
    #    necesitar modelo, así que más vale que esté probada.
    malo = json.loads(json.dumps(bueno))
    malo["datos"]["pesos"] = 1234567.0
    quejas = revisar_contrato(malo)
    check("2. la cuenta que no cierra se caza sin modelo",
          any("no cierra" in q for q in quejas), f"quejas: {quejas}")

    # 3) Los campos que faltan se reportan.
    falta = json.loads(json.dumps(bueno))
    falta["faltan"] = ["fuente"]
    check("3. un campo sin llenar se reporta",
          any("faltan campos" in q for q in revisar_contrato(falta)))

    # 4) Un worker que terminó mal se reporta aunque el texto se vea bien.
    roto = json.loads(json.dumps(bueno))
    roto["ok"], roto["motivo"] = False, "presupuesto"
    check("4. un worker que no terminó bien se reporta",
          any("no terminó bien" in q for q in revisar_contrato(roto)))

    # 5) 🚨 LA PRUEBA QUE DEFIENDE EL PUNTO DEL BLOQUE: un número INVENTADO pero
    #    coherente consigo mismo PASA. Esta prueba afirma un LÍMITE, igual que
    #    la nº 4 de `router.py`. Si algún día se pone roja sola, alguien le dio
    #    herramientas al revisor y hay que volver a apostar.
    inventado = json.loads(json.dumps(bueno))
    inventado["datos"]["tasa"] = 99999.0
    inventado["datos"]["pesos"] = 400 * 99999.0
    check("5. una tasa INVENTADA pero coherente pasa el revisor (límite)",
          revisar_contrato(inventado) == [],
          f"quejas: {revisar_contrato(inventado)}")

    # 6) Tolerancia: un redondeo pequeño no debe disparar la alarma.
    redondeo = json.loads(json.dumps(bueno))
    redondeo["datos"]["pesos"] = 1680000.4
    check("6. un redondeo dentro de la tolerancia no da falso positivo",
          revisar_contrato(redondeo) == [])

    # 7) Los dos sobres son DISTINTOS, y solo en una cosa: el original.
    c = _sobre_ciego("ENC", "RESP")
    o = _sobre_con_original("ENC", "RESP", "ORIG")
    check("7. el sobre ciego NO contiene el mensaje original",
          "ORIG" not in c and "ENC" in c and "RESP" in c)
    check("8. el sobre con original SÍ lo contiene, y lo demás igual",
          "ORIG" in o and "ENC" in o and "RESP" in o)

    # 9) Un contrato sin datos no revienta (el worker pudo fallar del todo).
    vacio = {"datos": None, "faltan": ["monto"], "ok": False, "motivo": "max_vueltas"}
    try:
        q = revisar_contrato(vacio)
        check("9. un resultado sin contrato no revienta el revisor", len(q) == 2)
    except Exception as e:
        check("9. un resultado sin contrato no revienta el revisor", False, str(e))

    # 10) El cebo apunta a un destino equivocado A PROPÓSITO. Si alguien lo
    #     "arregla", el experimento deja de tener presa y nadie lo notaría.
    check("10. el cebo está mal enrutado a propósito",
          DESTINO_USADO != DESTINO_CORRECTO)

    # 11-13) 🚨 EL ARREGLO DEL DÍA, CON PRUEBA. La primera versión del veredicto
    #        comparaba dos booleanos y dio un resultado FALSO sobre mi propia
    #        apuesta. Estas tres usan los MOTIVOS REALES de la corrida pagada,
    #        copiados del registro — no inventados.
    motivo_ciego_real = ("la fecha indicada (20 de agosto de 2026) es futura y no "
                         "puede ser una tasa real de mercado.")
    motivo_original_real = ("El usuario preguntó por una factura en euros (proveedor "
                            "de Alemania), pero el especialista convirtió dólares "
                            "estadounidenses.")
    check("11. el motivo del supervisor CIEGO no habla del enrutado",
          not habla_del_enrutado(motivo_ciego_real))
    check("12. el motivo del que VE EL ORIGINAL sí habla del enrutado",
          habla_del_enrutado(motivo_original_real))
    check("13. un motivo vacío no revienta la pista",
          habla_del_enrutado(None) is False and habla_del_enrutado("") is False)

    print()
    if fallos:
        print(f"  ❌ {len(fallos)} prueba(s) en rojo: {', '.join(fallos)}")
        return 1
    print("  ✅ todas en verde, y no costaron nada.")
    return 0


# ---------------------------------------------------------------------------
# 9) MAIN
# ---------------------------------------------------------------------------

def releer():
    """Vuelve a leer la corrida GRABADA y aplica la lógica de veredicto de hoy.

    🔑 EXISTE POR UNA RAZÓN CONCRETA: la primera versión del veredicto del
       experimento 1 estaba ciega, y arreglarla no puede costar $0,001 otra vez.
       **Arreglar el código es gratis; volver a correr es lo que cuesta.**
       Los motivos ya están en el registro: la conclusión se recalcula sobre
       ellos, no sobre una corrida nueva.

    ⚠️ Y no es solo ahorro: una corrida nueva daría motivos DISTINTOS, y
       entonces no se sabría si cambió la conclusión por el arreglo o por el
       modelo. Releer mantiene la variable quieta.
    """
    if not REGISTRO.exists():
        print(f"\n  ⚠️ no hay registro ({REGISTRO.name}). Corre --exp1 primero.")
        return 1

    sup = [json.loads(l) for l in REGISTRO.read_text(encoding="utf-8").splitlines()
           if json.loads(l).get("evento") == "supervision"]
    if not sup:
        print("\n  ⚠️ el registro no tiene supervisiones.")
        return 1

    # La última de cada brazo: si se corrió más de una vez, manda la reciente.
    ultimo = {}
    for d in sup:
        ultimo[d["etiqueta"]] = d

    print("\n" + "=" * 72)
    print("  RELECTURA del registro — $0,00, sobre la corrida ya pagada")
    print("=" * 72)
    for etiqueta in ("ciego", "con_original"):
        d = ultimo.get(etiqueta)
        if not d:
            continue
        habla = habla_del_enrutado(d.get("motivo"))
        print(f"\n  {etiqueta:<14} veredicto: {'sirve' if d['sirve'] else 'NO sirve'}"
              f"   ({'HABLA' if habla else 'NO habla'} del enrutado)")
        print(f"                 motivo: «{d.get('motivo')}»")

    c, o = ultimo.get("ciego"), ultimo.get("con_original")
    if c and o:
        hc, ho = habla_del_enrutado(c.get("motivo")), habla_del_enrutado(o.get("motivo"))
        print("\n  ── APUESTA 3 ──")
        if not hc and ho:
            print("     ✅ SE CUMPLE. Los dos rechazaron, pero solo el que ve el")
            print("        original nombra el enrutado. El ciego rechazó por otra")
            print("        cosa: acertó la casilla, no cazó el error.")
        elif hc:
            print("     ❌ FALLA: el ciego también nombra el enrutado.")
        else:
            print("     ⁉️ ninguno lo nombra.")
    return 0


# ---------------------------------------------------------------------------
# 7b) EXPERIMENTO 3 — ¿dónde tiene que vivir el permiso de negarse?
# ---------------------------------------------------------------------------
#
# 🚨 ESTE EXPERIMENTO NO ESTABA PLANEADO. Lo pidió el resultado del 2:
#
#    Al worker se le dio el mensaje original Y se le dijo explícitamente «si
#    este encargo no corresponde a lo que pidió el usuario, dilo en vez de
#    responderlo». Respondió igual, en dólares, idéntico.
#
# ⚠️ La explicación cómoda sería «le faltaba contexto» — y es FALSA: el
#    contexto se lo dimos entero. Escribirlo así sería la sesión 80 otra vez.
#
# 🔑 La explicación que queda, y que este experimento pone a prueba: **el
#    system prompt del worker le manda responder siempre** («no hagas
#    preguntas: nadie te va a contestar. Responde en UNA sola frase con el
#    monto en pesos»). Una instrucción metida en el encargo compite con eso y
#    pierde.
#
# → Hipótesis: **el permiso de negarse tiene que vivir en CÓMO SE CONSTRUYÓ el
#   worker, no en lo que se le dice.** Una sola variable: el system prompt.

# El de `worker.SISTEMA_DIVISA`, con UNA frase añadida. Nada más cambia.
SISTEMA_DIVISA_CON_DERECHO_A_NEGARSE = (
    worker.SISTEMA_DIVISA +
    " Si el encargo que recibes no corresponde a TU moneda, o no corresponde a "
    "lo que el usuario pidió en realidad, NO lo respondas: di claramente que "
    "ese encargo no es para ti y explica en una frase por qué."
)


def experimento_3():
    """El mismo encargo informado, el mismo worker, OTRO system prompt.

    💰 Una corrida de worker: ~$0,0073.
    """
    cebo = cargar_cebo()
    if cebo is None:
        return 1

    encargo_informado = (
        f"{cebo['encargo']}\n\n"
        f"AVISO: un supervisor rechazó tu respuesta anterior. Lo que el usuario "
        f"pidió en realidad fue: «{cebo['mensaje_original']}». "
        f"Si este encargo no corresponde a lo que pidió el usuario, dilo "
        f"claramente en vez de responderlo."
    )

    print("\n" + "=" * 72)
    print("  EXPERIMENTO 3 — ¿dónde tiene que vivir el permiso de negarse?")
    print("=" * 72)
    print("\n  MISMO encargo informado que el brazo B del experimento 2.")
    print("  MISMO worker. La única variable: UNA frase en el system prompt.\n")

    c = worker.correr_worker(encargo_informado, nombre=DESTINO_USADO,
                             sistema=SISTEMA_DIVISA_CON_DERECHO_A_NEGARSE)

    print("\n  ── QUÉ MIRAR ──")
    print("     ¿Devolvió el trabajo, o volvió a convertir dólares?")
    print(f"     herramientas usadas: {', '.join(c['herramientas']) or 'NINGUNA'}")
    print("     🔑 si no usó ninguna herramienta, se negó ANTES de trabajar —")
    print("        y entonces negarse además es GRATIS, no solo correcto.")
    print(f"\n  gasto del experimento 3: ${c['coste_usd']:.6f}")
    anotar("exp3_fin", texto=c["texto"], herramientas=c["herramientas"],
           gasto_usd=c["coste_usd"])
    return 0


def main(argv):
    if "--releer" in argv:
        return releer()
    if "--exp3" in argv:
        return experimento_3()
    if "--cebo" in argv:
        crear_cebo()
        return 0
    if "--exp1" in argv:
        return experimento_1()
    if "--exp2" in argv:
        return experimento_2()
    return _pruebas()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
