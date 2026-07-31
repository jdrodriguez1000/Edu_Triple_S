"""
prueba_memoria.py — La prueba pagada del paso 4.  (nivel 6b)

⚠️ ESTE ARCHIVO SÍ GASTA DINERO. Es el primero del nivel que llama a la API.
   Todo lo demás —las 4 funciones, recordar(), armar_sistema(), las 3 tablas—
   quedó probado en evals_memoria.py por $0.00. Aquí solo queda lo que NINGÚN
   eval puede contestar, que es una sola pregunta:

       ¿el MODELO decide bien CUÁNDO llamar a recordar?

   Eso no depende de nuestro código: depende de la descripción del menú. Y una
   descripción no se prueba con assert, se prueba corriéndola.

⭐ POR QUÉ SON DOS ACTOS Y NO UNO, Y ES EL PUNTO ENTERO DEL ARCHIVO

       python prueba_memoria.py 1     <- cuenta algo suyo. El agente lo guarda.
       python memoria.py              <- lo miras con tus ojos, en el disco.
       python prueba_memoria.py 2     <- OTRO PROCESO. ¿Se acuerda?

   Si los dos actos corrieran en la misma corrida, el acto 2 podría estar
   leyendo lo que quedó en la RAM y saldría igual de bien. No probaría NADA.
   La única prueba honesta de que algo es persistente es CERRAR EL PROGRAMA.

   → Es la trampa del archivo de evals_memoria.py, al derecho: allá el peligro
     era escribir donde no se debe; aquí es leer de donde no se debe.
"""

import sys

import agente
import memoria

sys.stdout.reconfigure(encoding="utf-8")

# ---------------------------------------------------------------------------
# Las dos conversaciones
# ---------------------------------------------------------------------------
# El acto 1 mete UN hecho estable ("soy contador", "facturo a EE.UU.") dentro de
# una pregunta normal de divisas. No dice "recuérdalo": si hay que pedírselo,
# la descripción no sirve.
#
# ⚠️ Y trae a propósito un hecho que NO se debe guardar: la respuesta va a traer
#    la TRM de hoy. Si el agente guarda la tasa, la descripción falló — un dato
#    que se vence guardado sin vencimiento es peor que ninguno.
ACTO_1 = (
    "Soy contador y le facturo a clientes en Estados Unidos. "
    "¿A cómo está el dólar oficial hoy?"
)

# El acto 2 NO menciona nada de lo anterior. Si el agente sabe que es contador,
# solo puede haberlo sacado del disco.
ACTO_2 = "¿Me conviene más la TRM oficial o la tasa de mercado para lo mío?"


# ---------------------------------------------------------------------------
# El permiso automático
# ---------------------------------------------------------------------------
def permiso_automatico(nombre, argumentos, autorizadas):
    """Responde los permisos sin una persona tecleando.

    ⚠️ HIZO FALTA EN LA PRIMERA CORRIDA, Y NO ERA SORPRESA: es la misma trampa
       que encontró examen.py en la sesión 17. pedir_permiso() llama a input(),
       y una prueba que se corre sola no tiene a quién preguntarle. Sin esto,
       la corrida muere con EOFError a mitad — y ya pagada.

    ⭐ Y por eso ejecutar_agente() recibe `preguntar` como parámetro desde el
       paso 10: lo que entra por parámetro se puede automatizar; lo que está
       clavado adentro, no.

    ⚠️ LO QUE ESTO CUESTA, DICHO EN VOZ ALTA: aquí los permisos dejan de
       probarse. Es aceptable porque lo que se mide hoy es la MEMORIA, y los
       permisos ya se midieron en los pasos 8 y 10. No es aceptable olvidarlo.

    guardar_reporte se NIEGA a propósito: nada en estas dos preguntas justifica
    escribir un archivo, y si el modelo lo intenta, quiero verlo en el registro.
    """
    grupo = agente.PERMISOS.get(nombre, "disco")

    if grupo == "libre":
        return True, "libre"
    if grupo == "red":
        return True, "prueba_autoriza_red"
    return False, "prueba_niega_disco"


if __name__ == "__main__":
    acto = sys.argv[1] if len(sys.argv) > 1 else ""

    if acto not in ("1", "2"):
        print(__doc__)
        print("Uso:  python prueba_memoria.py 1   |   python prueba_memoria.py 2")
        sys.exit()

    pregunta = ACTO_1 if acto == "1" else ACTO_2

    # Lo que el agente recuerda ANTES de esta conversación. Se imprime para que
    # el acto 2 no tenga que creerle a nadie: se ve de dónde salió.
    datos_previos = memoria.cargar_memoria()

    agente.anotar("inicio", modelo=agente.MODELO, prueba=f"memoria_acto_{acto}",
                  presupuesto_usd=agente.PRESUPUESTO_USD,
                  precio_entrada=agente.PRECIO_ENTRADA,
                  precio_salida=agente.PRECIO_SALIDA,
                  memoria_previa=len(datos_previos),
                  herramientas=list(agente.FUNCIONES))

    print(f"\n{'=' * 66}")
    print(f"ACTO {acto}   modelo={agente.MODELO}")
    print(f"{'=' * 66}")
    print(f"\n🧠 lo que recordaba al empezar: {len(datos_previos)} dato(s)")
    for fila in datos_previos:
        print(f"     · {fila['dato']}  ({fila['fecha']})")

    print(f"\n👤 {pregunta}\n")

    respuesta = agente.ejecutar_agente(pregunta, preguntar=permiso_automatico)

    print(f"\n🤖 {respuesta}")

    # Y lo que quedó DESPUÉS. La diferencia es lo que el modelo decidió guardar.
    datos_finales = memoria.cargar_memoria()
    print(f"\n🧠 memoria al terminar: {len(datos_finales)} dato(s)")
    for i, fila in enumerate(datos_finales):
        marca = "NUEVO" if fila["dato"] not in [d["dato"] for d in datos_previos] else "     "
        print(f"  [{i}] {marca} {fila['dato']}")

    agente.anotar("fin", gastado_usd=round(agente.gastado_usd, 6),
                  memoria_final=len(datos_finales))

    print(f"\n💰 esta corrida costó ${agente.gastado_usd:.6f}")
    print(f"📓 todo quedó anotado en {agente.REGISTRO.name}")

    if acto == "1":
        print("\n→ Ahora mira el disco:   python memoria.py")
        print("→ Y después el acto 2:   python prueba_memoria.py 2")
        print("   (proceso NUEVO: si se acuerda, salió del archivo)")
