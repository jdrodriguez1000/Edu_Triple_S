"""
memoria.py — La memoria persistente del agente de divisas.  (nivel 6b, paso 2)

QUÉ ES ESTE ARCHIVO
    Tres funciones puras y un archivo JSON. NO hay nada de IA aquí: ni API, ni
    tokens, ni costo. Es Python plano — abrir un archivo, una lista, escribirlo.
    Por eso el paso 3 puede probarlo TODO gratis y sin red.

    ⭐ Esa separación es a propósito. Lo que se puede probar sin pagar, se separa
       de lo que hay que pagar para probar. Es tu propio método del paso 10, al
       derecho: los evals cubren lo que alcanzan, y la corrida pagada solo lo que
       no alcanzan.

LAS DECISIONES QUE LO GOBIERNAN  (sesión 18, tuyas)
    1. QUÉ se guarda ........ solo el PERFIL: hechos estables sobre el usuario.
    2. QUIÉN decide ......... el MODELO, con una herramienta `recordar`
                              (escuela B). Para LEER decide el código: siempre.
    3. CUÁNDO se lee ........ siempre, al arrancar, pegado al system prompt.
    4. FORMATO .............. un solo memoria.json que se REESCRIBE.
    5. QUÉ se olvida ........ cada dato con su fecha + un tope. Sale el más viejo.
    6. PERMISO .............. NO pide. Es "libre".
                              A cambio: huella en el registro + revisión aquí.

⭐ POR QUÉ .json Y NO .jsonl — EL FORMATO SALE DE LA POLÍTICA, NO DEL GUSTO

       registro.jsonl  ->  EVENTOS.  Lo que pasó. Solo crece. Se AÑADE al final.
       memoria.json    ->  ESTADO.   Lo que es verdad hoy. Se REESCRIBE entero.

    Tu agente ya escribía en disco desde la sesión 15 — pero escribía eventos.
    Este es el primer archivo suyo que guarda ESTADO, y por eso cambia de forma.

⚠️ ESTE ARCHIVO NO SE SUBE A GIT. Va en .gitignore, junto a .env. Contiene datos
   de una persona, y Git no olvida: borrarlo después NO lo borra del historial.
"""

import json
import sys
from datetime import date
from pathlib import Path

# La consola de Windows es cp1252 y no sabe imprimir emojis ni algunas tildes.
# El programa funciona; lo que revienta es el print. Está en GUIDE.md §64.
sys.stdout.reconfigure(encoding="utf-8")

# ---------------------------------------------------------------------------
# 1) DÓNDE VIVE Y CUÁNTO CABE
# ---------------------------------------------------------------------------
# La ruta se arma desde __file__, igual que la del .env en todos los niveles.
# Si se dejara "memoria.json" a secas, el archivo aparecería en la carpeta desde
# la que CORRES el programa, no donde vive el código. Correrlo desde otra
# carpeta crearía una segunda memoria vacía, sin error y sin aviso.
ARCHIVO = Path(__file__).resolve().parent / "memoria.json"

# El tope. Sin él vuelve el problema del nivel 2: algo que crece sin parar y que
# se paga en la ENTRADA de cada vuelta de cada conversación.
#   ⭐ "Un sistema de memoria sin política de olvido no está terminado."
# 8 es pequeño a propósito: queremos VER el desplazamiento funcionando, no
# esperar seis meses a que se llene.
TOPE = 8

# El largo máximo de un dato. El modelo es quien va a llamar a `recordar`, y
# nada le impide mandar tres párrafos.
#   ⚠️ Es la deuda 5 de la sesión 17 en miniatura: "el harness mete lo que sea
#      que devuelva una herramienta, sin mirarlo". Aquí sí se mira.
LARGO_MAXIMO = 200


# ---------------------------------------------------------------------------
# 2) LEER  —  cargar_memoria()
# ---------------------------------------------------------------------------
def cargar_memoria():
    """Devuelve la lista de datos recordados. NUNCA revienta.

    Esa promesa —"nunca revienta"— es la más importante del archivo, y no es
    pereza: esta función corre al ARRANCAR el agente, antes de la primera
    llamada. Si tira una excepción, el agente no existe.

    ⭐ Y hay una asimetría que vale la pena ver: que la memoria falle NO debe
       impedir contestar "¿a cómo está el dólar?". La memoria es un lujo; la
       respuesta es el producto. Un lujo que tumba el producto está mal cableado.

    Los cuatro casos que puede encontrarse:
      a) el archivo no existe .... es lo NORMAL la primera vez, no un error.
      b) el archivo está dañado .. alguien lo editó a mano y lo rompió.
      c) tiene otra forma ........ es un JSON válido pero no es lo que esperamos.
      d) todo bien ............... el caso aburrido.

    ⚠️ En (b) y (c) NO se borra el archivo. Es tentador ("está dañado, lo
       reinicio") y es un error: el archivo dañado es la única evidencia de qué
       pasó. Se avisa y se sigue con memoria vacía.
    """
    # (a) No existe. Silencio: no es un problema.
    if not ARCHIVO.exists():
        return []

    try:
        contenido = json.loads(ARCHIVO.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        # (b) Dañado.
        print(f"⚠️  memoria: {ARCHIVO.name} está dañado. Sigo sin memoria.")
        print("    El archivo NO se borró: ábrelo y míralo.")
        return []

    # (c) Es JSON válido, pero no tiene la forma que esperamos. Puede pasar si
    #     un día cambiamos el formato y queda un archivo viejo dando vueltas.
    if not isinstance(contenido, dict) or not isinstance(contenido.get("datos"), list):
        print(f"⚠️  memoria: {ARCHIVO.name} no tiene la forma esperada. Sigo sin memoria.")
        return []

    # (d) Bien. Se filtran las filas que no sirven en vez de confiar en todas:
    #     el archivo es editable a mano, así que su contenido es de FUERA.
    return [
        fila for fila in contenido["datos"]
        if isinstance(fila, dict) and isinstance(fila.get("dato"), str)
    ]


# ---------------------------------------------------------------------------
# 3) ESCRIBIR  —  guardar_dato()
# ---------------------------------------------------------------------------
def guardar_dato(texto):
    """Guarda un hecho. Devuelve (guardado, motivo).

    ⭐ EL PAR (resultado, motivo) ES TU PROPIA IDEA, y esta es la SEXTA vez que
       paga en otro archivo. Nació en el `motivo` de trm_en_fecha (cero filas
       tapaba tres casos distintos) y siguió en pedir_permiso, donde un `true`
       tapaba tres situaciones y hacía MENTIR al registro.

       Aquí pasaría lo mismo: un `False` pelado no distingue "el modelo mandó
       basura" de "eso ya lo sabíamos". Y como no hay permiso que interrumpa,
       el motivo es LO ÚNICO que va a quedar escrito en la huella.

    Los motivos posibles:
      guardado ....... entró un dato nuevo.
      desplazo ....... entró, y para que cupiera salió el más viejo.
      refrescado ..... ya lo sabíamos; se le actualizó la fecha.
      vacio .......... llegó "" o solo espacios.
      muy_largo ...... pasó de LARGO_MAXIMO.
      no_es_texto .... llegó algo que no es una cadena.
    """
    # --- Los frenos van ANTES de tocar el disco. Si algo se rechaza, el
    #     archivo ni se abre.
    if not isinstance(texto, str):
        return False, "no_es_texto"

    limpio = texto.strip()

    if not limpio:
        return False, "vacio"

    if len(limpio) > LARGO_MAXIMO:
        return False, "muy_largo"

    datos = cargar_memoria()

    # --- ¿Ya lo sabíamos? Se compara sin distinguir mayúsculas, porque el
    #     modelo no escribe igual dos veces.
    #     ⭐ Y no se descarta a secas: se le REFRESCA LA FECHA. Que el modelo
    #        vuelva a decir lo mismo es evidencia de que sigue siendo cierto, y
    #        la fecha es lo que va a decidir mañana a quién creerle.
    for fila in datos:
        if fila["dato"].lower() == limpio.lower():
            fila["fecha"] = date.today().isoformat()
            _escribir(datos)
            return True, "refrescado"

    # --- Entra el dato nuevo. La fecha NO es adorno:
    #     ⚠️ "Un dato guardado sin fecha es un dato que no sabes si creerle."
    #        Un dato no se daña: se VENCE. Y vencido parece bueno.
    datos.append({"dato": limpio, "fecha": date.today().isoformat()})

    # --- El tope. Sale el más viejo: es el primero de la lista, porque siempre
    #     se agrega al final.
    #     ⚠️ Y esto es una DECISIÓN, no una obviedad: se está diciendo que lo
    #        más viejo es lo menos valioso. No siempre es cierto — "es contador"
    #        vale más que algo dicho ayer. Queda anotado como deuda del nivel.
    motivo = "guardado"
    while len(datos) > TOPE:
        datos.pop(0)
        motivo = "desplazo"

    _escribir(datos)
    return True, motivo


def _escribir(datos):
    """Reescribe el archivo entero. El guion bajo dice: es de uso interno.

    Se reescribe COMPLETO, no se añade — porque esto es estado, no eventos.

    ⚠️ DEUDA CONOCIDA: si el programa muere justo aquí, el archivo queda a
       medias y la próxima carga lo verá dañado. La solución de verdad es
       escribir en un archivo temporal y renombrar al final. No se hace hoy
       para no meter dos temas nuevos a la vez, y queda anotado.
    """
    ARCHIVO.write_text(
        json.dumps({"datos": datos}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# 4) TRADUCIR  —  memoria_como_texto()
# ---------------------------------------------------------------------------
def memoria_como_texto(datos):
    """Convierte la lista en el párrafo que se le pega al system prompt.

    ⭐ ES LA FUNCIÓN QUE SE OLVIDA, Y ES LA QUE CUESTA DINERO. Entre "tener los
       datos" y "que el modelo los lea" hay un paso de traducción, y ese paso
       decide CUÁNTOS TOKENS pesa la memoria en la ENTRADA de cada vuelta.
       Con 27:1 de entrada contra salida, aquí es donde se paga.

    ⚠️ Recibe los datos como PARÁMETRO en vez de llamar a cargar_memoria().
       Así no toca el disco, y eso la vuelve trivial de probar: le metes una
       lista inventada y miras qué texto sale. Cero archivos, cero red.

    Y va la fecha, aunque cueste tokens: sin ella el modelo no puede decir
    "esto me lo dijiste hace seis meses, ¿sigue siendo así?".
    """
    if not datos:
        return ""

    lineas = [f"- {fila['dato']}  (recordado el {fila['fecha']})" for fila in datos]

    return (
        "Esto es lo que recuerdas de este usuario de conversaciones anteriores:\n"
        + "\n".join(lineas)
        + "\nÚsalo si viene al caso. Si algo se contradice con lo que dice hoy, "
        "manda lo de hoy."
    )


# ---------------------------------------------------------------------------
# 4-bis) LA HERRAMIENTA  —  recordar()   (paso 4)
# ---------------------------------------------------------------------------
def recordar(dato):
    """Lo que el MODELO llama. Envuelve a guardar_dato() y devuelve un dict.

    ⚠️ POR QUÉ NO SE LE ENTREGA guardar_dato() DIRECTAMENTE AL MODELO, que sería
       más corto: devuelve una TUPLA (True, "guardado"), y el content de un
       tool_result tiene que ser texto. Pero el problema de fondo no es el tipo:

       ⭐ una tupla le dice al harness qué pasó; no le dice al MODELO qué hacer.
          "muy_largo" es un diagnóstico. "resúmelo en menos de 200 caracteres y
          vuelve a intentarlo" es una instrucción. El modelo necesita la segunda.
       → Es lo mismo que hacen los errores del bucle desde el paso 8: el error
         VUELVE AL MODELO redactado para que pueda corregirse solo.

    ⚠️ Y lo que esta función NO devuelve, a propósito: la memoria entera. Sería
       cómodo ("mira cómo quedó") y se pagaría en la entrada de cada vuelta que
       falte. El tool_result también se reenvía. Es la deuda del tamaño del
       tool_result de la sesión 15, y aquí no se repite.
    """
    guardado, motivo = guardar_dato(dato)

    # Cada motivo con su instrucción. Los que el modelo puede corregir, se le
    # explican; los que no, se le dicen para que no insista.
    mensajes = {
        "guardado":    "Anotado. No se lo anuncies al usuario: sigue con su pregunta.",
        "desplazo":    "Anotado. Como la memoria estaba llena, salió el dato más viejo.",
        "refrescado":  "Ya lo sabías: se le actualizó la fecha. No lo vuelvas a guardar.",
        "vacio":       "No guardaste nada: el dato venía vacío.",
        "muy_largo":   f"Demasiado largo. Resúmelo en menos de {LARGO_MAXIMO} "
                       "caracteres y vuelve a intentarlo.",
        "no_es_texto": "El dato tiene que ser texto. Vuelve a intentarlo.",
    }

    return {
        "guardado": guardado,
        "motivo": motivo,
        "mensaje": mensajes[motivo],
    }


# ---------------------------------------------------------------------------
# 5) BORRAR  —  olvidar()
# ---------------------------------------------------------------------------
def olvidar(indice=None):
    """Borra un dato por su número, o todo si no se da número.

    Esta función es LA QUE REEMPLAZA AL PERMISO (decisión 6). El trato fue:
    el agente escribe sin preguntar, pero tú puedes ver y borrar cuando quieras.

    ⭐ Permiso = ANTES, para lo irreversible.  Revisión = DESPUÉS, para lo
       reversible. La memoria es un archivo de texto que abres y corriges, así
       que cae del lado de la revisión.
    """
    datos = cargar_memoria()

    if indice is None:
        _escribir([])
        return len(datos)

    if not (0 <= indice < len(datos)):
        return 0

    datos.pop(indice)
    _escribir(datos)
    return 1


# ---------------------------------------------------------------------------
# 6) EL COMANDO DE REVISIÓN
# ---------------------------------------------------------------------------
# ⚠️ El `if __name__` dejó de ser una formalidad en la sesión 17: sin él, un
#    `import memoria` desde el agente correría todo esto de una vez. Aquí no
#    costaría dinero, pero borraría archivos.
if __name__ == "__main__":
    import sys

    argumentos = sys.argv[1:]

    if argumentos and argumentos[0] == "borrar":
        if len(argumentos) > 1 and argumentos[1] == "todo":
            print(f"🗑️  Se olvidaron {olvidar()} datos.")
        elif len(argumentos) > 1 and argumentos[1].isdigit():
            n = int(argumentos[1])
            print(f"🗑️  Se olvidó el dato {n}." if olvidar(n) else f"No existe el dato {n}.")
        else:
            print("Uso: python memoria.py borrar <numero>   |   borrar todo")
        sys.exit()

    # Sin argumentos: mostrar. Es lo que reemplaza al permiso.
    filas = cargar_memoria()

    print(f"\n🧠 MEMORIA DEL AGENTE  ({ARCHIVO.name}, tope {TOPE})")
    print("─" * 64)

    if not filas:
        print("(vacía — el agente no recuerda nada todavía)")
    else:
        for i, fila in enumerate(filas):
            print(f"  [{i}]  {fila['dato']}")
            print(f"       recordado el {fila['fecha']}")

    print("─" * 64)
    print(f"{len(filas)} de {TOPE} datos.")
    print("Para borrar:  python memoria.py borrar 0   |   python memoria.py borrar todo\n")
