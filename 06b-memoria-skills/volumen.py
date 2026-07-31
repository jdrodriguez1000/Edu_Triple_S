"""
volumen.py — El paso 5 del nivel 6b: la memoria bajo VOLUMEN.

⚠️ ESTE ARCHIVO GASTA DINERO. Unos $0.10 en haiku, diez conversaciones.

QUÉ VIENE A CONTESTAR, Y POR QUÉ NINGÚN EVAL PUEDE

    prueba_memoria.py probó que la memoria FUNCIONA: guarda, sobrevive al
    cierre, y el agente la usa. Eso ya está.

    Lo que NO puede contestar una sola conversación es cómo se comporta el
    sistema cuando hay MUCHO de dónde escoger. Tres preguntas abiertas:

    1. ¿El modelo junta DOS HECHOS EN UNA FICHA?  Pasó una vez en la sesión 19
       ("es contador y factura a clientes en Estados Unidos"), y una vez no es
       un patrón: puede haber sido la variabilidad. Aquí se cuenta.

    2. ¿EL TOPE DESPLAZA DE VERDAD?  Los 73 evals lo prueban con datos
       SEMBRADOS POR NOSOTROS. Nunca se ha visto botar un dato que hubiera
       puesto el modelo. Por eso hay más de 8 hechos aquí abajo.

    3. ¿GUARDA BASURA?  Dos de las diez preguntas NO traen ningún hecho
       estable, y una trae una cifra tentadora. Si el agente guarda algo ahí,
       la descripción está de más.

⭐ Y LA REGLA QUE GOBIERNA LA LECTURA DE ESTOS NÚMEROS, aprendida ayer:

       UNA MUESTRA NO ES UNA MEDIDA.

    El mismo acto 2, corrido dos veces con la misma memoria, dio dos respuestas
    distintas. Así que aquí NO se busca "el resultado": se busca si algo pasa
    LAS DIEZ VECES, o si pasa una y son ganas de ver un patrón.
"""

import sys

import agente
import memoria

sys.stdout.reconfigure(encoding="utf-8")


# ---------------------------------------------------------------------------
# Las diez conversaciones
# ---------------------------------------------------------------------------
# Cada una: (etiqueta, pregunta, fichas_esperadas)
#
# `fichas_esperadas` es LA VARA, y se escribe ANTES de correr — igual que la
# rúbrica del paso 10 se escribió antes de ver una sola respuesta. Escribirla
# después sería acomodarla a lo que salió.
#
# ⚠️ Y como la rúbrica, esto es una HIPÓTESIS, no una verdad. Si una respuesta
#    buena "reprueba", el sospechoso es la vara. (Sesión 17, dos veces.)
CONVERSACIONES = [
    ("un hecho simple",
     "Soy contador. ¿A cómo está el dólar oficial hoy?", 1),

    ("un hecho de lugar",
     "Vivo en Medellín. ¿La TRM es la misma en todo el país?", 1),

    # 🎯 EL CASO DEL DEFECTO: dos hechos que se vencen por separado. Puede dejar
    #    de exportar y seguir viajando a Panamá.
    ("DOS hechos en una frase",
     "Tengo una empresa de exportación y viajo mucho a Panamá. "
     "¿Cuántos dólares son 2 millones de pesos?", 2),

    # 🎯 SIN HECHO: pregunta pelada. No hay nada que recordar.
    ("sin ningún hecho",
     "¿El dólar subió o bajó el último mes?", 0),

    ("una preferencia",
     "Prefiero que me des las cifras en tablas. ¿Cuál fue la TRM del 15 de julio?", 1),

    # 🎯 SIN HECHO, PERO CON CIFRA TENTADORA: la respuesta va a traer la TRM.
    #    Si la guarda, la descripción falló donde más importa.
    ("sin hecho + cifra a la vista",
     "¿A cómo está la tasa de mercado del dólar ahora mismo?", 0),

    ("un hecho de moneda",
     "Manejo el presupuesto de mi familia en euros. ¿Cómo va el euro frente al peso?", 1),

    ("un hecho de rutina",
     "Reviso las tasas todos los lunes en la mañana. ¿Hoy hay TRM nueva?", 1),

    ("un hecho de negocio",
     "Tengo una tienda de ropa importada. ¿Me conviene comprar dólares hoy?", 1),

    # A esta altura la memoria debería estar llena o cerca. Aquí se ve el tope.
    ("el que hace desbordar",
     "Estudio economía en la Universidad Nacional. "
     "¿Dónde puedo ver la serie histórica de la TRM?", 1),
]


def permiso_automatico(nombre, argumentos, autorizadas):
    """El mismo de prueba_memoria.py: los permisos no se prueban aquí.

    ⚠️ Y hay que decirlo cada vez: esto APAGA la prueba de permisos. Es
       aceptable porque se midieron en los pasos 8 y 10, no porque no importe.
    """
    grupo = agente.PERMISOS.get(nombre, "disco")
    if grupo == "libre":
        return True, "libre"
    if grupo == "red":
        return True, "volumen_autoriza_red"
    return False, "volumen_niega_disco"


def peso_entrada(datos):
    """Cuánto pesa el prompt HOY, con esta memoria. Gratis: count_tokens."""
    texto = memoria.memoria_como_texto(datos)
    r = agente.cliente.messages.count_tokens(
        model=agente.MODELO,
        system=agente.armar_sistema(texto),
        tools=agente.TOOLS,
        messages=[{"role": "user", "content": "x"}],
    )
    return r.input_tokens


if __name__ == "__main__":
    # `python volumen.py 10` corre SOLO la conversación 10. Nació de necesitar
    # comprobar un arreglo sin pagar las diez otra vez.
    solo = None
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        solo = int(sys.argv[1])
        if not (1 <= solo <= len(CONVERSACIONES)):
            print(f"No existe la conversación {solo}. Hay {len(CONVERSACIONES)}.")
            sys.exit()
        CONVERSACIONES = [CONVERSACIONES[solo - 1]]
        print(f"\n▶️  Solo la conversación {solo}. Las otras no se corren.")

    previos = memoria.cargar_memoria()
    if previos:
        print(f"\n⚠️  La memoria tiene {len(previos)} dato(s) de antes. Esta prueba mide")
        print("    QUÉ GUARDA DESDE CERO, así que conviene arrancar limpia:")
        print("        python memoria.py borrar todo\n")
        print("    (o sigue, y lee los números sabiendo que venían datos de antes)")
        if input("    ¿Sigo de todos modos? [s/n] > ").strip().lower() != "s":
            sys.exit()

    agente.anotar("inicio", modelo=agente.MODELO, prueba="volumen",
                  presupuesto_usd=agente.PRESUPUESTO_USD,
                  precio_entrada=agente.PRECIO_ENTRADA,
                  precio_salida=agente.PRECIO_SALIDA,
                  conversaciones=len(CONVERSACIONES),
                  herramientas=list(agente.FUNCIONES))

    vacio = peso_entrada([])
    filas = []          # lo que se va midiendo, para la tabla del final
    desplazados = []    # los datos que el tope botó

    for i, (etiqueta, pregunta, esperadas) in enumerate(CONVERSACIONES, 1):
        antes = memoria.cargar_memoria()
        gasto_antes = agente.gastado_usd

        print(f"\n{'=' * 70}")
        print(f"[{i}/{len(CONVERSACIONES)}]  {etiqueta}   (memoria: {len(antes)} datos)")
        print(f"{'=' * 70}")
        print(f"👤 {pregunta}\n")

        try:
            respuesta = agente.ejecutar_agente(pregunta, preguntar=permiso_automatico)
        except Exception as fallo:
            # Una conversación que revienta NO puede tumbar las otras nueve: ya
            # están pagadas las anteriores y se perdería la medición entera.
            print(f"  💥 esta conversación falló: {type(fallo).__name__}: {fallo}")
            respuesta = f"(falló: {type(fallo).__name__})"

        print(f"\n🤖 {respuesta[:400]}{'...' if len(respuesta) > 400 else ''}")

        despues = memoria.cargar_memoria()
        textos_antes = [d["dato"] for d in antes]
        textos_despues = [d["dato"] for d in despues]

        nuevas = [t for t in textos_despues if t not in textos_antes]
        salieron = [t for t in textos_antes if t not in textos_despues]
        desplazados.extend(salieron)

        for t in nuevas:
            print(f"     🧠 guardó: {t}")
        for t in salieron:
            print(f"     🗑️  el tope botó: {t}")
        if not nuevas and not salieron:
            print("     🧠 no guardó nada")

        filas.append({
            "n": i,
            "etiqueta": etiqueta,
            "esperadas": esperadas,
            "nuevas": len(nuevas),
            "textos": nuevas,
            "total": len(despues),
            "tokens": peso_entrada(despues),
            "costo": agente.gastado_usd - gasto_antes,
        })

    # =======================================================================
    # LOS TRES ANÁLISIS
    # =======================================================================
    print(f"\n\n{'=' * 70}")
    print("RESUMEN")
    print(f"{'=' * 70}\n")

    print(f"{'#':>2}  {'qué traía':<28} {'esperadas':>9} {'guardó':>7} "
          f"{'total':>6} {'tokens':>7} {'$':>9}")
    print("-" * 74)
    for f in filas:
        marca = " " if f["nuevas"] == f["esperadas"] else "⚠"
        print(f"{f['n']:>2}{marca} {f['etiqueta']:<28} {f['esperadas']:>9} "
              f"{f['nuevas']:>7} {f['total']:>6} {f['tokens']:>7} {f['costo']:>9.5f}")

    # --- 1) ¿junta dos hechos en una ficha? -------------------------------
    print(f"\n{'─' * 70}")
    print("1) ¿EL MODELO JUNTA VARIOS HECHOS EN UNA FICHA?")
    print(f"{'─' * 70}")
    # ⚠️ ESTA VARA ESTABA MAL EN LA PRIMERA CORRIDA, Y ES LA SESIÓN 17 OTRA VEZ.
    #    Restaba `hechos - fichas` y llamaba "empaquetado" a todo el faltante.
    #    Mirando fila por fila había DOS fenómenos distintos:
    #      - EMPAQUETÓ: 1 ficha donde había 2 hechos   -> guardó MAL
    #      - OMITIÓ:    0 fichas donde había un hecho  -> NO guardó
    #    De los 5 "faltantes" de la primera corrida, solo 1 era empaquetado.
    #    Y se arreglan distinto. Un diagnóstico que no distingue no es un
    #    diagnóstico: es el defecto de C6 solapándose con C3 y C4, otra vez.
    #    → Cuando el diagnóstico no distingue, el sospechoso es el instrumento.
    hechos = sum(f["esperadas"] for f in filas)
    fichas = sum(f["nuevas"] for f in filas)

    empaquetadas = [f for f in filas if 0 < f["nuevas"] < f["esperadas"]]
    omitidas = [f for f in filas if f["esperadas"] > 0 and f["nuevas"] == 0]
    de_mas = [f for f in filas if f["nuevas"] > f["esperadas"]]

    print(f"   hechos que traían las preguntas : {hechos}")
    print(f"   fichas que creó el agente       : {fichas}\n")

    print(f"   EMPAQUETÓ (guardó mal) : {len(empaquetadas)} conversación(es)")
    for f in empaquetadas:
        print(f"      [{f['n']}] {f['esperadas']} hechos -> {f['nuevas']}: {f['textos']}")
    print(f"   OMITIÓ (no guardó)     : {len(omitidas)} conversación(es)")
    for f in omitidas:
        print(f"      [{f['n']}] {f['etiqueta']}")
    if de_mas:
        print(f"   PARTIÓ DE MÁS          : {len(de_mas)} conversación(es)")

    if empaquetadas:
        print("\n   → Empaquetar duele: dos hechos en una ficha SE VENCEN POR")
        print("     SEPARADO, y `olvidar` solo deja botar los dos o ninguno.")
    if omitidas:
        print("\n   → Omitir es OTRO problema, y es de la DESCRIPCIÓN: el hecho")
        print("     estaba ahí y el modelo no lo consideró digno de guardar.")
    if not (empaquetadas or omitidas or de_mas):
        print("\n   ✅ CUADRA. Una ficha por hecho, como pide la descripción.")

    # --- 2) ¿guardó basura? ------------------------------------------------
    print(f"\n{'─' * 70}")
    print("2) ¿GUARDÓ LO QUE NO DEBÍA?")
    print(f"{'─' * 70}")
    basura = [f for f in filas if f["esperadas"] == 0 and f["nuevas"] > 0]
    if basura:
        for f in basura:
            print(f"   ⚠️  [{f['n']}] {f['etiqueta']}: guardó {f['textos']}")
        print("   → La descripción no está frenando lo que debería.")
    else:
        print("   ✅ Ninguna de las preguntas sin hecho estable guardó nada.")
        print("      Incluida la que traía una cifra a la vista.")

    # --- 3) el tope -------------------------------------------------------
    print(f"\n{'─' * 70}")
    print("3) ¿EL TOPE DESPLAZÓ DE VERDAD?")
    print(f"{'─' * 70}")
    if desplazados:
        print(f"   ✅ Botó {len(desplazados)} dato(s), con datos que puso EL MODELO:")
        for t in desplazados:
            print(f"      · {t}")
        print("   → Los 73 evals lo probaban con datos sembrados por nosotros.")
        print("     Esta es la primera vez que se ve con datos de verdad.")
    else:
        final = memoria.cargar_memoria()
        print(f"   ⏳ No se llenó: quedaron {len(final)} de {memoria.TOPE}.")
        print("      Hacen falta más hechos para cruzar el tope.")

    # --- el precio --------------------------------------------------------
    lleno = peso_entrada(memoria.cargar_memoria())
    print(f"\n{'─' * 70}")
    print("EL PRECIO")
    print(f"{'─' * 70}")
    print(f"   prompt sin memoria : {vacio} tokens")
    print(f"   prompt al terminar : {lleno} tokens  ({lleno - vacio:+} por la memoria)")
    print(f"   gasto de la corrida: ${agente.gastado_usd:.4f} de "
          f"${agente.PRESUPUESTO_USD:.2f}")

    agente.anotar("fin", gastado_usd=round(agente.gastado_usd, 6),
                  hechos=hechos, fichas=fichas,
                  desplazados=len(desplazados),
                  memoria_final=len(memoria.cargar_memoria()))

    print(f"\n📓 todo quedó anotado en {agente.REGISTRO.name}")
    print("🧠 mira la memoria final con:  python memoria.py\n")
