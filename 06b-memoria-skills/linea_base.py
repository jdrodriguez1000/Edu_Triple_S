"""linea_base.py — el agente SIN skills, contra las 4 preguntas del paso 6.

    ¿PARA QUÉ SIRVE ESTE ARCHIVO?

Para responder una sola pregunta, y hay que responderla ANTES de conectar nada:

    ¿el modelo ya sabe lo que dicen las skills?

Si lo sabe, las skills no prueban nada. Es el error de la sesión 3, cuando se
probó el olvido preguntando "¿qué es una variable?": las tres estrategias
contestaron bien —el modelo ya lo sabía— y la prueba no demostraba nada,
pero el texto afirmaba que sí.

Aquí las skills están llenas de datos ARBITRARIOS a propósito: márgenes del
0,4 %, tramos de 5.000 y 20.000 dólares, un nombre de archivo `cierre-AAAA-MM`.
Nadie los puede adivinar. Esta corrida lo comprueba en vez de suponerlo.

    LOS DOS RESULTADOS POSIBLES, Y LOS DOS SIRVEN

  · Dice "no lo sé"  -> la skill tiene algo que aportar. Sigue el paso 6.
  · Se inventa la cifra -> peor y más interesante: es el modo de falla número 4
    (no carga nada y contesta igual de seguro). Y ahora está MEDIDO desde antes.

Lo que NO sirve es que acierte. Ahí la skill sobra.

    CÓMO SE CORRE

    python linea_base.py

No pregunta permisos: los concede solos, para poder correr las 4 seguidas.
Corre con la MEMORIA VACÍA (texto_memoria="") — no lee ni escribe memoria.json.
"""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

import agente


# ---------------------------------------------------------------------------
# LAS 4 PREGUNTAS, CON LA TRAMPA ESCRITA AL LADO
# ---------------------------------------------------------------------------
# ⭐ Cada pregunta viene con las "señales": pedacitos de texto que SOLO pueden
#    salir de la skill correspondiente. Si aparecen sin que exista la skill,
#    el modelo se los inventó.
#
# ⚠️ Y esto NO es un juez. Es coincidencia de texto, que es mucho más tonta:
#    puede acertar por casualidad y puede no ver una cifra escrita de otra
#    forma ("0.4%" vs "0,4 %"). Sirve para mirar rápido; la lectura la haces tú.
PREGUNTAS = [
    {
        "id": "1-sin-skill",
        "texto": "¿Cuánto son 200 dólares en pesos colombianos?",
        "skill_esperada": None,
        "senales": [],
        "que_mirar": "Aquí NO debería hacer falta ninguna skill. Es el caso "
                     "'17 por 23' del nivel 3: se paga el menú entero y no se "
                     "usa nada. Sirve de control.",
    },
    {
        "id": "2-explicar",
        "texto": "Un cliente me reclama porque el precio que le di no es el que "
                 "ve en Google. ¿Qué le digo?",
        "skill_esperada": "explicar-a-un-cliente",
        "senales": ["mayorista", "ventanilla", "entre bancos"],
        "que_mirar": "Sin la skill puede contestar razonablemente: esto es "
                     "conocimiento general. Lo que NO puede tener es la forma "
                     "acordada (máximo 6 líneas, primero el número, palabras "
                     "prohibidas).",
    },
    {
        "id": "3-umbral",
        "texto": "Necesito cambiar 50 millones de pesos a dólares. ¿Puedo "
                 "hacerlo de una o necesito alguna autorización?",
        "skill_esperada": "normas-cambiarias",
        "senales": ["0,4", "0.4", "5.000", "5000", "20.000", "20000",
                    "tesorería", "tesoreria", "dos firmas", "24 horas"],
        "que_mirar": "🚨 LA PRUEBA IMPORTANTE. Los tramos son inventados. Si "
                     "menciona un umbral cualquiera con seguridad, ese número "
                     "no salió de ningún lado.",
    },
    {
        "id": "4-diciembre",
        # 🐛 ESTA PREGUNTA DECÍA SOLO "el reporte de cierre de diciembre", Y
        #    ESTABA MAL HECHA. La primera corrida lo destapó: hoy es 31 de
        #    julio de 2026, así que le estaba pidiendo el cierre de un mes que
        #    NO HA PASADO. Contestó, con razón, "esa fecha está en el futuro",
        #    y nunca llegó al tema del formato — que era lo único que yo quería
        #    medir con ella.
        #    → Cuando una respuesta razonable "reprueba", el sospechoso es la
        #      prueba. La pregunta ahora pide un diciembre que ya ocurrió.
        "texto": "Ármame el reporte de cierre de diciembre de 2025.",
        "skill_esperada": "reporte-mensual + cierre-de-ano",
        "senales": ["cierre-2026-12", "cierre-anual", "nota al pie",
                    "último día hábil", "ultimo dia habil", "valoración anual",
                    "valoracion anual", "sección 6", "seccion 6"],
        "que_mirar": "El par confundible. Sin skills no puede saber ni las 5 "
                     "secciones, ni el nombre del archivo, ni que diciembre "
                     "lleva DOS cierres.",
    },
    {
        # 🐛 ESTA PREGUNTA NACIÓ DE UN EMPATE QUE NO SE PODÍA ROMPER.
        #    La 3 pregunta por el PERMISO ("¿puedo hacerlo de una?"), no pide una
        #    cotización. Cuando el agente dejó de aplicar el margen, no había
        #    forma de saber si:
        #      a) se abstuvo de una cuenta que sí tocaba hacer, o
        #      b) juzgó bien que ahí no tocaba cotizar.
        #    Las dos explicaciones encajaban con la misma respuesta.
        #
        # ⭐ Y ese es el defecto de fondo de la pregunta 3: mezcla dos cosas
        #    (autorizar y cotizar) y por eso no puede probar ninguna de las dos.
        #    Esta pide UNA sola, sin escapatoria.
        "id": "5-cotizar",
        "texto": "Cotízame el cambio de 50 millones de pesos colombianos a "
                 "dólares, con el margen aplicado.",
        "skill_esperada": "normas-cambiarias",
        # 15.898,25 es el resultado de aplicar el factor 0,996 con `convertir`.
        # Si aparece, la cuenta salió de la herramienta: es un número que el
        # modelo no puede producir de cabeza por casualidad.
        "senales": ["15.898", "15898", "0,996", "0.996"],
        "que_mirar": "🚨 Lo que se mide NO es la respuesta, son las LLAMADAS. "
                     "Tiene que haber DOS `convertir`: el bruto y el factor. "
                     "Con una sola, o el margen no se aplicó o se hizo de "
                     "cabeza — que es el defecto original.",
    },
]


def permiso_automatico(nombre, argumentos, autorizadas):
    """Concede todo, sin preguntar.

    Es el mismo parámetro `preguntar` que se inventó para el examen: el bucle
    no sabe CÓMO se pide un permiso, solo A QUIÉN preguntarle.

    ⚠️ Se concede todo a propósito, para que la línea base mida lo que el
       modelo SABE y no lo que el harness le dejó hacer. Un permiso negado a
       mitad cambiaría la respuesta y ensuciaría la comparación.
    """
    return True, "automatico_linea_base"


def senales_encontradas(texto, senales):
    bajo = texto.lower()
    return [s for s in senales if s.lower() in bajo]


if __name__ == "__main__":
    # 🐛 LOS ARGUMENTOS SE LEEN DE PRIMERAS, Y ANTES NO ERA ASÍ.
    #    Estaban 30 líneas más abajo, y `anotar("inicio")` los usaba antes de
    #    que existieran: NameError apenas arrancaba.
    #    → Lo que decide CÓMO va a correr el programa se lee antes de que el
    #      programa empiece a hacer nada. Si se lee a mitad, siempre hay algo
    #      más arriba que ya lo necesitaba.
    #
    # ⭐ Se puede correr UNA sola pregunta:  python linea_base.py 4-diciembre
    #    Existe porque arreglar una pregunta mal hecha no debería obligar a
    #    pagar las otras tres otra vez. Volver a medir es lo que cuesta;
    #    arreglar el archivo es gratis.
    #
    # 🚨 Y `--con` ES EL ARREGLO DE UN DEFECTO QUE CASI PASA.
    #    Este archivo se escribió ANTES de conectar las skills, así que
    #    llamaba a ejecutar_agente() a secas. En el momento en que el menú entró
    #    al system prompt por defecto, este script habría seguido corriendo con
    #    el mismo nombre y midiendo OTRA COSA.
    #    → Una medición "antes" deja de ser el antes en el instante en que
    #      cambias lo que mide, y no avisa. Ahora el modo es explícito y se
    #      imprime en pantalla.
    argumentos = [a for a in sys.argv[1:] if a != "--con"]
    con_skills = "--con" in sys.argv
    filtro = argumentos[0] if argumentos else None
    pendientes = [p for p in PREGUNTAS if filtro is None or p["id"] == filtro]
    if not pendientes:
        sys.exit(f"❌ No hay ninguna pregunta con id {filtro!r}. "
                 f"Hay: {[p['id'] for p in PREGUNTAS]}")

    # El MODO queda escrito en el registro. Sin eso, dentro de un mes hay dos
    # corridas en el mismo .jsonl y ninguna dice cuál era cuál.
    agente.anotar("inicio", modelo=agente.MODELO,
                  corrida="con_skills" if con_skills else "linea_base",
                  skills=[f["nombre"] for f in agente.FICHAS] if con_skills else [],
                  presupuesto_usd=agente.PRESUPUESTO_USD,
                  precio_entrada=agente.PRECIO_ENTRADA,
                  precio_salida=agente.PRECIO_SALIDA)

    print("=" * 70)
    print("CON SKILLS 🧠" if con_skills else "LÍNEA BASE — el agente SIN skills")
    print(f"Modelo: {agente.MODELO}   ·   memoria: VACÍA a propósito")
    print(f"menú de skills: {'PUESTO (' + str(len(agente.FICHAS)) + ' fichas)' if con_skills else 'QUITADO'}")
    print("=" * 70)

    resultados = []

    for p in pendientes:
        print(f"\n\n{'=' * 70}")
        print(f"[{p['id']}]  {p['texto']}")
        print(f"  skill que le haría falta: {p['skill_esperada'] or 'ninguna'}")
        print("-" * 70)

        # texto_memoria="" es una ORDEN ("corre sin memoria"), no una ausencia.
        # Con None iría a leer memoria.json del disco, y la línea base dejaría
        # de ser limpia.
        respuesta = agente.ejecutar_agente(
            p["texto"],
            preguntar=permiso_automatico,
            texto_memoria="",
            # None = con el menú de skills.  "" = sin él, la línea base.
            menu_skills=None if con_skills else "",
        )

        print(f"\nRESPUESTA:\n{respuesta}")

        encontradas = senales_encontradas(respuesta, p["senales"])
        resultados.append((p, respuesta, encontradas))

        # 🚨 LA MISMA SEÑAL SIGNIFICA LO CONTRARIO EN CADA MODO, Y ESTO ESTABA MAL.
        #    La primera versión decía siempre "🚨 SEÑALES ENCONTRADAS SIN SKILL:
        #    ese dato no está en ninguna parte de este programa" — escrito
        #    cuando el programa NO tenía skills. Con --con, encontrar señales es
        #    exactamente lo que se busca, y el script lo gritaba como alarma.
        #
        # ⭐ El detector no cambió ni una línea: lo que cambió fue QUÉ SIGNIFICA
        #    lo que detecta. Una medición no vale por sí sola; vale contra la
        #    configuración con la que se tomó. Y esa configuración hay que
        #    escribirla al lado del número, o el número miente solo.
        if p["senales"]:
            if con_skills:
                if encontradas:
                    print(f"\n✅ USÓ LA SKILL: {encontradas}")
                    print("   Esos datos SOLO existen dentro del .md.")
                else:
                    print("\n🚨 NO SE VE LA SKILL en la respuesta. O no la cargó, "
                          "o la cargó y la ignoró.")
            else:
                if encontradas:
                    print(f"\n🚨 SEÑALES SIN TENER LA SKILL: {encontradas}")
                    print("   No hay de dónde sacarlos: se los inventó.")
                else:
                    print("\n✅ Ninguna señal. El modelo NO tiene este dato.")
        print(f"\n👀 Qué mirar: {p['que_mirar']}")

    agente.anotar("fin", corrida="linea_base",
                  gastado_usd=round(agente.gastado_usd, 6))

    print(f"\n\n{'=' * 70}")
    print("RESUMEN")
    print("=" * 70)
    for p, respuesta, encontradas in resultados:
        if not p["senales"]:
            marca = "— control, sin señales que buscar"
        elif con_skills:
            marca = "✅ usó la skill" if encontradas else "🚨 la skill no se ve"
        else:
            marca = "🚨 inventó algo" if encontradas else "— limpio"
        print(f"  [{p['id']:<14}] {len(respuesta):>5} caracteres   {marca}")
    print(f"\nGasto de la corrida ({'con skills' if con_skills else 'línea base'}): "
          f"${agente.gastado_usd:.4f} "
          f"de ${agente.PRESUPUESTO_USD:.2f}")
    print(f"Todo quedó anotado en: {agente.REGISTRO.name}")
