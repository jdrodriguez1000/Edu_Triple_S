"""skills.py — leer la carpeta de skills y armar el menú.

    QUÉ ES UNA SKILL, EN UNA LÍNEA

Un archivo `.md` con dos partes: una FICHA arriba (entre los `---`) y un CUERPO
abajo. La ficha viaja SIEMPRE en el system prompt; el cuerpo solo cuando el
modelo lo pide.

    herramienta -> extiende lo que el agente puede HACER
    skill       -> extiende lo que el agente SABE

⭐ ESTE ARCHIVO NO HABLA CON LA API Y NO SABE QUE EXISTE UN MODELO.
   Es la misma decisión de memoria.py: funciones puras, probables sin red y sin
   plata. Todo lo que aquí se rompa, se rompe gratis.

⚠️ Y NO CONFUNDIR LAS DOS COSAS QUE HACE:
     leer_fichas()  -> abre los 4 archivos y se queda SOLO con lo de arriba.
                       Corre UNA vez, al arrancar.
     leer_skill()   -> abre UN archivo y devuelve lo de abajo.
                       Corre cuando el modelo lo pide, y cuesta una vuelta.
   Si leer_fichas() devolviera también el cuerpo, el menú pesaría lo mismo que
   el conocimiento entero y no habríamos ganado nada.
"""

from pathlib import Path

AQUI = Path(__file__).resolve().parent
CARPETA = AQUI / "skills"


def _partir(texto):
    """Separa un .md en (ficha, cuerpo).

    El formato es el mismo de las skills de Claude Code, y se copió a propósito:
    tres guiones, los campos, tres guiones, y debajo el contenido.

        ---
        nombre: normas-cambiarias
        descripcion: ...
        ---

        # el cuerpo

    Devuelve ("", texto) si el archivo no tiene ficha. No revienta: un archivo
    mal formado es un problema que hay que VER, no una excepción que tumbe el
    agente antes de arrancar.
    """
    lineas = texto.splitlines()
    if not lineas or lineas[0].strip() != "---":
        return "", texto

    for i in range(1, len(lineas)):
        if lineas[i].strip() == "---":
            return "\n".join(lineas[1:i]), "\n".join(lineas[i + 1:]).strip()

    # Abrió la ficha y nunca la cerró.
    return "", texto


def _campos(ficha):
    """Saca `nombre` y `descripcion` de la ficha.

    ⚠️ Esto NO es YAML de verdad, y decirlo importa. Entiende `clave: valor` y
       las líneas seguidas indentadas (para descripciones de varias líneas), que
       es todo lo que usamos. Si algún día una skill necesita listas o comillas,
       hay que traer una librería — no parchar esto.
       → Un parser casero que crece de a poquitos es cómo nacen los defectos
         raros de leer.
    """
    datos = {}
    clave = None
    for linea in ficha.splitlines():
        if not linea.strip():
            continue
        # Línea indentada = sigue la clave anterior.
        if linea[0] in " \t" and clave:
            datos[clave] += " " + linea.strip()
            continue
        if ":" in linea:
            clave, _, valor = linea.partition(":")
            clave = clave.strip()
            datos[clave] = valor.strip()
    return datos


def leer_fichas(carpeta=CARPETA):
    """Abre todos los .md de la carpeta y devuelve SOLO las fichas.

    Cada ficha es {"nombre", "descripcion", "archivo"}.
    Se ordenan por nombre para que el menú salga igual en cada corrida: un menú
    que cambia de orden entre corridas hace que dos mediciones no se puedan
    comparar, y ese es el tipo de ruido que después nadie encuentra.

    ⚠️ El `nombre` que manda es el DEL ARCHIVO, no el de la ficha. Si no
       coinciden se avisa, pero el que se usa es el del archivo — porque es el
       que existe de verdad en el disco. Un nombre que el modelo pide y que no
       corresponde a ningún archivo no se puede abrir por más bien escrito que
       esté.
    """
    fichas = []
    if not carpeta.is_dir():
        return fichas

    for archivo in sorted(carpeta.glob("*.md")):
        ficha, _ = _partir(archivo.read_text(encoding="utf-8"))
        campos = _campos(ficha)

        nombre = archivo.stem
        if campos.get("nombre") and campos["nombre"] != nombre:
            print(f"  ⚠️ {archivo.name}: la ficha dice nombre='{campos['nombre']}' "
                  f"pero el archivo se llama '{nombre}'. Mando el del archivo.")

        descripcion = campos.get("descripcion", "").strip()
        if not descripcion:
            # Sin descripción el modelo no tiene con qué escoger. Es un defecto
            # del .md, y se dice fuerte: la skill existe pero es invisible.
            print(f"  ⚠️ {archivo.name} no tiene 'descripcion': el modelo no va "
                  f"a saber para qué sirve.")
            descripcion = "(sin descripción)"

        fichas.append({"nombre": nombre, "descripcion": descripcion,
                       "archivo": archivo})
    return fichas


def menu_como_texto(fichas):
    """El menú que se pega al system prompt. Devuelve "" si no hay skills.

    ⭐ POR QUÉ ESTE TEXTO VIVE EN EL SYSTEM Y NO EN LA DESCRIPCIÓN DE
       `leer_skill`, que era la opción obvia:

       Es la misma decisión que ya se tomó con la memoria, y allá la UBICACIÓN
       fue el arreglo, no la redacción. Una descripción de herramienta solo pesa
       cuando el modelo YA está considerando llamarla. Los dos defectos medidos
       en volumen.py fueron justo eso: nunca llegó a considerarla.

       Si el menú viviera dentro de la descripción, el modelo tendría que querer
       cargar una skill para enterarse de que existen. Aquí lo ve siempre.
       → Y por eso las fichas son cortas: esto se paga en CADA vuelta.
    """
    if not fichas:
        return ""

    lineas = [
        "TIENES ESTOS DOCUMENTOS DE CONSULTA (skills). No los tienes delante: "
        "son fichas. Para leer uno, llama a 'leer_skill' con su nombre.",
    ]
    for f in fichas:
        lineas.append(f"- {f['nombre']}: {f['descripcion']}")
    lineas.append(
        "Si la pregunta cae en el tema de una de estas fichas, LEE la skill ANTES "
        "de contestar. No contestes de memoria lo que un documento define: los "
        "montos, los formatos y las reglas internas SOLO están ahí, y no hay forma "
        "de deducirlos. Si crees saber la respuesta pero hay una ficha sobre el "
        "tema, léela igual."
    )
    return "\n".join(lineas)


def leer_skill(nombre, carpeta=CARPETA):
    """Devuelve el CUERPO de una skill. Es lo que corre la herramienta.

    🚨 EL NOMBRE SE BUSCA EN LA LISTA, NO SE PEGA A UNA RUTA.

       La versión obvia sería `carpeta / (nombre + ".md")`. Y con eso,
       leer_skill("../../.env") devuelve la llave de la API. El modelo escribe
       ese argumento: es texto que viene DE AFUERA, y el texto de afuera nunca
       se convierte en una ruta directamente.

       Aquí el nombre solo sirve para BUSCAR entre los archivos que leer_fichas
       ya encontró. Lo que no está en esa lista, no existe.
       → Es el segundo candado de borrar_archivo (nivel 4), otra vez: la
         herramienta se defiende sola, sin depender de quién la llame.

    Y cuando no existe, el error DICE cuáles sí — la lección del PERMISO
    DENEGADO: un error que el modelo puede leer se arregla solo; uno mudo lo
    hace inventar.
    """
    fichas = leer_fichas(carpeta)
    disponibles = [f["nombre"] for f in fichas]

    for f in fichas:
        if f["nombre"] == nombre:
            _, cuerpo = _partir(f["archivo"].read_text(encoding="utf-8"))
            return {"skill": nombre, "contenido": cuerpo}

    return {
        "error": f"No existe ninguna skill llamada '{nombre}'.",
        "disponibles": disponibles,
    }


if __name__ == "__main__":
    # Correrlo a mano muestra el menú tal como lo va a ver el modelo, y cuánto
    # pesa. Cuesta $0.00: aquí no hay API.
    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    fichas = leer_fichas()
    menu = menu_como_texto(fichas)

    print(menu)
    print()
    print("=" * 70)
    print(f"skills encontradas: {len(fichas)}")
    print(f"el menú pesa: {len(menu)} caracteres (viaja en CADA vuelta)")
    total = 0
    for f in fichas:
        cuerpo = leer_skill(f["nombre"])["contenido"]
        total += len(cuerpo)
        print(f"  {f['nombre']:<24} cuerpo: {len(cuerpo):>6} caracteres")
    print(f"el conocimiento entero pesa: {total} caracteres")
    print(f"el menú es el {100 * len(menu) / (len(menu) + total):.0f}% del total")
