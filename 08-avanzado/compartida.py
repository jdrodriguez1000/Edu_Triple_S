"""compartida.py — D.1 del nivel 8: MEMORIA COMPARTIDA entre workers.

    LA FRASE QUE HAY QUE VER

`06b-memoria-skills/memoria.py` está bien escrito. Tiene su política de olvido,
su fecha en cada dato, su par (resultado, motivo), y una promesa explícita:
*«el archivo dañado es la única evidencia de qué pasó, así que NO se borra»*.

Y no tiene un solo candado, porque en el 6b **no hacía falta**: había un agente,
un hilo, un escritor. En D.1 hay tres workers.

🔑 EL PARALELISMO NO CREA LOS RECURSOS COMPARTIDOS — LOS DESTAPA. Es la misma
   frase de B.2 (`fan_out.py`), y esta es la segunda vez que se cobra. Allá
   destapó el registro; aquí destapa el ESTADO, que se rompe distinto.


    POR QUÉ ESTE ARCHIVO NO EDITA `06b/memoria.py`

Mismo motivo por el que `worker.py` repitió el bucle en vez de tocar
`05b-proyecto/agente.py`: aquel código está MEDIDO, y el valor de una medición
vieja depende de que su código siga siendo el mismo. Además su `memoria.json`
tiene datos de una persona.

→ Aquí se trabaja sobre archivo propio (`memoria_equipo.json`, en `.gitignore`),
  y `guardar_ingenuo()` es una **copia deliberada** de la forma del 6b: existe
  para poder ROMPERLA a voluntad y medir cuánto se pierde.


    LOS TRES FALLOS QUE LA GENTE METE EN LA MISMA BOLSA

Se llaman todos «concurrencia» y necesitan TRES arreglos distintos. Confundirlos
es lo que hace que un arreglo parezca puesto y no lo esté.

    | El fallo                          | El arreglo                | ¿candado? |
    |-----------------------------------|---------------------------|-----------|
    | dos escrituras se entrelazan      | candado                   | sí        |
    | el archivo se ve / queda a medias | temporal + `os.replace()` | NO        |
    | una lectura vieja pisa lo nuevo   | releer DENTRO del candado | NO        |

⚠️ Y hay un cuarto que no cabe en la tabla porque no es del archivo, es del
   PROCESO: un `threading.Lock` vive en la memoria de UN proceso. Dos procesos
   tienen dos candados y ninguno ve al otro. Eso es `_candado_de_archivo()`.


    LO MEDIDO EN LA SESIÓN 106 — todo a $0,00, sin una llamada al modelo

Con la forma del 6b, N hilos guardando N datos distintos a la vez (200 vueltas
por fila, `TOPE = 8`):

    hilos   JSON roto      datos perdidos
      2     0/200  ( 0,0%)   198/400  (49,5%)
      3     0/200  ( 0,0%)   383/600  (63,8%)
      6     3/200  ( 1,5%)   872/1200 (72,7%)
     12    49/200  (24,5%)  1310/1600 (81,9%)

🚨 LEE LA PRIMERA FILA DESPACIO. **Dos workers — que es literal la trampa que el
   temario le puso a D.1 — pierden la MITAD de lo que escriben y dejan el archivo
   PERFECTAMENTE VÁLIDO.** Cero excepciones, cero avisos, cero líneas rotas.

🔑 UN `.jsonl` ROTO GRITA; UN ESTADO PISADO CALLA. Por eso el candado del
   registro (B.2) no se podía copiar y ya: allá el síntoma es un archivo
   ilegible, aquí es un archivo legible que MIENTE.

📌 Y la columna «JSON roto» y la columna «quedó vacío» salieron IDÉNTICAS en las
   cuatro filas (0, 0, 3, 49). No es casualidad: ver abajo.


    🚨 EL HALLAZGO DEL DÍA: LA PROMESA DE «NO SE BORRA» DURA TRES LÍNEAS

`memoria.py` promete no borrar un archivo dañado porque es la única evidencia.
`cargar_memoria()` cumple: avisa y devuelve `[]`. Y `guardar_dato()`, tres
líneas después, **llama a `cargar_memoria()`, recibe ese `[]`, le añade el dato
nuevo y reescribe el archivo entero**.

Medido, con tres datos sanos y el archivo cortado a la mitad:

    ANTES:  3 datos.  Se daña el archivo.
    LEER:   avisa, devuelve 0, y el archivo SIGUE dañado.   ✅ la promesa se cumple
    UNA ESCRITURA:  devuelve (True, "guardado").            🟢 luz verde
    DESPUÉS: el archivo es VÁLIDO y tiene UN dato.          💀 los 3 viejos, y la
                                                               evidencia, no existen

🔑 **La promesa era del lector, y quien la rompe es el escritor.** Nadie mintió:
   las dos funciones hacen exactamente lo que su comentario dice. Lo que no
   existía era el comentario que las mirara juntas.
🔑 Y ESO explica que «JSON roto» y «quedó vacío» dieran el mismo número: cada vez
   que la carrera rompe el archivo, la defensa escrita para ser prudente convierte
   *«esto está dañado»* en *«aquí no había nada»*. **Una defensa correcta contra
   un escritor es un borrador silencioso con dos.**

⚠️ Es `LM.15` en su cuarta cara: el instrumento ciego no da un dato falso, da
   SILENCIO — y aquí el silencio además limpia la escena.


    🚨 Y EL ARREGLO QUE PARECE BIEN HECHO NO ARREGLA NADA. Lo mismo, con PROCESOS:

    modo          perdidos          qué lleva puesto
    ingenuo       46/60 (76,7 %)    nada
    solo_hilos    48/60 (80,0 %)    candado de hilos + relectura dentro + atómico
    arreglado      0/60 ( 0,0 %)    lo anterior + candado DE ARCHIVO

🔑 Lee la fila de en medio. `solo_hilos` lleva **todo lo que una revisión de
   código llamaría correcto**, pasa las 18 pruebas de hilos sin despeinarse, y
   entre procesos **pierde MÁS que no hacer nada**. Un `threading.Lock` es un
   objeto en la memoria de UN proceso; dos procesos tienen dos y ninguno ve al
   otro.
⚠️ Y no es un caso de laboratorio: el **bloque E** son agentes programados, y su
   primera pregunta escrita es *«¿qué pasa si se dispara dos veces?»*.
🔑 **El modo de fallo peor de este archivo no se ve leyendo el código ni corriendo
   las pruebas que cualquiera escribiría. Solo se ve lanzando dos `python`.**


    📌 UN NÚMERO QUE CAMBIÓ DURANTE LA SESIÓN, Y SE DICE

La primera medición de `solo_hilos` traía **26 de 60 procesos caídos** con
`PermissionError [WinError 5]` en `os.replace()` — Windows niega el renombrado si
otro tiene el destino abierto (ver `_escribir_atomico`). Al ponerle reintentos,
esa columna bajó a **0** y la de pérdidas se quedó igual.

⚠️ O sea: **el arreglo se llevó el síntoma ruidoso y dejó el silencioso intacto.**
   Fue correcto ponerlo —el reintento cubre al lector que no pide candado— y hay
   que decir lo que hizo, porque un `0` en esa columna se lee como *«ya no pasa
   nada»* y lo que pasa es que ya no se oye.
"""

import json
import os
import sys
import tempfile
import threading
import time
from datetime import date, datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

AQUI = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# 1) DÓNDE VIVE Y CUÁNTO CABE
# ---------------------------------------------------------------------------
# ⚠️ Archivo PROPIO del nivel 8, y en `.gitignore`. No se toca el del 6b.
ARCHIVO = AQUI / "memoria_equipo.json"

# El tope, heredado del 6b: pequeño a propósito para VER el desplazamiento.
TOPE = 8
LARGO_MAXIMO = 200

# 🎲 APUESTA 5 — LA POLÍTICA DE OLVIDO ES UNA DECISIÓN DE PRODUCTO, Y CAMBIA.
#    En el 6b «sale el más viejo» era la política entera, y era correcta: un
#    escritor, una persona, un perfil. Con tres workers escribiendo, «el más
#    viejo» significa **que el worker más hablador desaloja al callado**, y eso
#    no lo decidió nadie: salió de que el código no sabe que hay tres.
#
#    → La reserva: al desalojar NO se puede dejar a un worker sin ningún dato
#      mientras otro tenga más de uno.
#
# 🔑 Es LA MISMA IDEA QUE `RepartoDeEntrada` DE C.2, aplicada al estado en vez
#    de al dinero: un recurso compartido y escaso se reparte con una reserva por
#    participante, o se lo lleva el primero que llegue. Que la misma forma sirva
#    para dólares y para renglones de memoria es la señal de que era estructura.
MINIMO_POR_WORKER = 1

# Cuánto se espera por el candado ENTRE PROCESOS antes de rendirse, y a partir de
# cuándo un candado se considera abandonado (su dueño murió sin soltarlo).
ESPERA_MAXIMA_S = 5.0
CANDADO_RANCIO_S = 30.0

# Cuánto se reintenta el `os.replace()` cuando Windows lo niega porque otro tiene
# el archivo abierto. Ver `_escribir_atomico()`: en POSIX este número no se usa
# nunca, y ese es justo el motivo por el que hace falta.
REINTENTO_REPLACE_S = 2.0


# ---------------------------------------------------------------------------
# 2) LA FORMA INGENUA — la del 6b, copiada para poder romperla
# ---------------------------------------------------------------------------
def cargar(archivo=None):
    """Devuelve (datos, estado). NUNCA revienta — esa promesa se mantiene.

    ⭐ PERO DEVUELVE EL PAR, y ahí está el arreglo del hallazgo del día. En el 6b
       `cargar_memoria()` devolvía `[]` a secas, y `[]` significaba DOS cosas
       distintas: «no hay nada» y «no pude leer». Quien recibe `[]` no puede
       distinguirlas, y por eso el escritor borró la evidencia sin enterarse.

       Es el par (resultado, motivo) del 6b —el que ya pagó seis veces— aplicado
       a la función que NO lo llevaba. `LM.20` otra vez: la corrección ya estaba
       escrita en el mismo archivo, en la función de al lado.

    Estados: `vacio` · `ok` · `danado` · `otra_forma`
    """
    archivo = archivo or ARCHIVO

    if not Path(archivo).exists():
        return [], "vacio"

    try:
        contenido = json.loads(Path(archivo).read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return [], "danado"

    if not isinstance(contenido, dict) or not isinstance(contenido.get("datos"), list):
        return [], "otra_forma"

    return [
        fila for fila in contenido["datos"]
        if isinstance(fila, dict) and isinstance(fila.get("dato"), str)
    ], "ok"


def _escribir_ingenuo(datos, archivo=None):
    """La forma del 6b: `write_text`, que TRUNCA y luego escribe.

    ⚠️ El hueco entre truncar y escribir es donde entra el otro hilo. Y no hay
       que imaginarlo: es lo que produjo el 24,5 % de archivos rotos con 12 hilos.
    """
    Path(archivo or ARCHIVO).write_text(
        json.dumps({"datos": datos}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def guardar_ingenuo(texto, quien="?", archivo=None):
    """Leer → modificar → escribir, SIN candado. Es el defecto, no el arreglo.

    🚨 Esta función existe para MEDIRSE, no para usarse. Es la única forma de que
       el arreglo de abajo tenga un antes contra el que compararse: sin un
       control, «no se rompió» no dice si el candado sirvió o si el experimento
       no apretó. Es lo que faltó en la primera medición de la sesión y lo que la
       convirtió en una anécdota hasta que se puso el control al lado.
    """
    ok, motivo, limpio = _revisar(texto)
    if not ok:
        return False, motivo

    datos, _estado = cargar(archivo)          # 👈 se ignora el estado: el bug del 6b
    datos = _mezclar(datos, limpio, quien)
    _escribir_ingenuo(datos, archivo)
    return True, "guardado"


# ---------------------------------------------------------------------------
# 3) LOS FRENOS DE ENTRADA — no cambian con el paralelismo
# ---------------------------------------------------------------------------
def _revisar(texto):
    """Los frenos van ANTES de tocar el disco. Idénticos a los del 6b."""
    if not isinstance(texto, str):
        return False, "no_es_texto", None
    limpio = texto.strip()
    if not limpio:
        return False, "vacio", None
    if len(limpio) > LARGO_MAXIMO:
        return False, "muy_largo", None
    return True, "ok", limpio


def _mezclar(datos, limpio, quien):
    """Mete el dato en la lista y aplica el tope. Función PURA: no toca disco.

    ⚠️ Que sea pura es lo que la vuelve probable sin hilos, sin archivos y sin
       esperar: se le mete una lista inventada y se mira qué sale. Misma razón
       por la que `memoria_como_texto()` del 6b recibía los datos por parámetro.
    """
    hoy = date.today().isoformat()

    for fila in datos:
        if fila["dato"].lower() == limpio.lower():
            fila["fecha"] = hoy
            fila["quien"] = quien       # el último que lo confirmó
            return datos

    datos = datos + [{"dato": limpio, "fecha": hoy, "quien": quien}]

    while len(datos) > TOPE:
        datos.pop(_a_quien_desalojar(datos))

    return datos


def _a_quien_desalojar(datos):
    """Devuelve el índice del que sale. Con la reserva por worker de la apuesta 5.

    Regla: sale el más viejo **de entre los que se pueden sacar**. No se puede
    sacar el último dato de un worker si otro worker tiene más de uno.

    🔑 Y si TODOS tienen exactamente uno, la reserva no se puede cumplir y sale
       el más viejo a secas. Eso no es un fallo: es que la reserva prometía un
       reparto, no un milagro. `RepartoDeEntrada` hace lo mismo cuando el
       presupuesto no alcanza — dice que no alcanza, no inventa dinero.
    """
    cuantos = {}
    for fila in datos:
        cuantos[fila.get("quien", "?")] = cuantos.get(fila.get("quien", "?"), 0) + 1

    for i, fila in enumerate(datos):
        if cuantos[fila.get("quien", "?")] > MINIMO_POR_WORKER:
            return i

    return 0


# ---------------------------------------------------------------------------
# 4) ARREGLO 2 — ESCRIBIR ENTERO O NO ESCRIBIR: `os.replace()`
# ---------------------------------------------------------------------------
def _escribir_atomico(datos, archivo=None):
    """Escribe en un temporal AL LADO y renombra encima. El renombrado es atómico.

    ⭐ Esta es la deuda que `06b/memoria.py` dejó anotada con sus palabras:
       *«la solución de verdad es escribir en un archivo temporal y renombrar al
       final»*. Se paga aquí.

    🪤 PERO SU MOTIVO ESCRITO ERA EL RIESGO EQUIVOCADO, y es `LM.67` por segunda
       vez. La deuda dice: *«si el programa MUERE justo aquí»*. Pensó en el
       proceso propio muriéndose; el peligro de D.1 es **el proceso de al lado
       leyendo**. `os.replace()` cubre los dos — pero por suerte, no por diseño,
       y un arreglo que acierta por suerte no se puede repetir a propósito.

    ⚠️ El temporal va en la MISMA carpeta a propósito: `os.replace()` solo es
       atómico dentro del mismo sistema de archivos. En `/tmp` sería una copia.

    ⚠️ Y `os.replace()` NO resuelve la actualización perdida. Dos escrituras
       atómicas siguen pisándose: la segunda gana entera. Atómico quiere decir
       «no queda a medias», no «no se pierde».

    🚨 SESIÓN 106, MEDIDO — «ATÓMICO» NO QUIERE DECIR «SIEMPRE SE PUEDE».
       En POSIX, renombrar encima de un archivo que otro tiene abierto funciona.
       En **Windows no**: si cualquiera lo tiene abierto —aunque sea LEYÉNDOLO—,
       `os.replace()` da `PermissionError [WinError 5]`. Con 5 procesos y sin
       candado, **26 de 60 se cayeron con un traceback, y los 16 clasificados
       eran este error, sin una sola excepción de otra clase.**
    🔑 Así que la escritura atómica, ella sola, no vuelve seguro escribir: cambia
       **corrupción silenciosa** por **proceso muerto**. Es mejor —un fallo que
       grita se arregla y uno que calla no— pero **no es el arreglo**. El arreglo
       es el candado; esto es lo que hace que el candado no tenga que ser perfecto.
    → Por eso hay reintentos: cubren al LECTOR que no pidió el candado, que es el
      hueco que queda incluso con todo bien puesto.
    """
    archivo = Path(archivo or ARCHIVO)
    texto = json.dumps({"datos": datos}, ensure_ascii=False, indent=2)

    fd, tmp = tempfile.mkstemp(dir=str(archivo.parent), prefix=".tmp_", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(texto)
            f.flush()
            os.fsync(f.fileno())     # que llegue al disco, no solo al buffer

        limite = time.monotonic() + REINTENTO_REPLACE_S
        while True:
            try:
                os.replace(tmp, archivo)     # 👈 el renombrado atómico
                return
            except PermissionError:
                if time.monotonic() > limite:
                    raise
                time.sleep(0.002)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


# ---------------------------------------------------------------------------
# 5) ARREGLO 1 y 4 — LOS DOS CANDADOS, Y POR QUÉ SON DOS
# ---------------------------------------------------------------------------
# 🔒 El de hilos. Igual que `orquestador._CANDADO_REGISTRO`.
#    ⚠️ Y con la lección de la apuesta 1 encima: en `orquestador.py` y en
#       `worker.py` hay DOS objetos `Lock()` distintos, uno por módulo. Hoy no se
#       pisan porque escriben en dos archivos distintos — pero
#       `presupuesto.py:823` apunta los dos al mismo archivo, y ahí son dos
#       cerraduras en dos puertas de la misma habitación. Medido en la 106.
#    → Por eso aquí hay UN candado y vive junto al archivo que protege, no junto
#      al módulo que escribe. **Un candado protege un ARCHIVO, y tiene que estar
#      donde está el archivo.**
_CANDADO_HILOS = threading.Lock()


class CandadoOcupado(Exception):
    """No se pudo entrar a tiempo. No es un fallo del disco: es una decisión."""


class _CandadoDeArchivo:
    """Un candado que SÍ cruza procesos, porque vive en el disco.

    Cómo funciona, en una frase: **el que consigue CREAR el archivo `.lock`
    manda**, y crear-si-no-existe es una sola operación del sistema operativo,
    así que no hay hueco donde entren dos.

    ⭐ `os.O_CREAT | os.O_EXCL` es la pieza entera. Sin `O_EXCL` habría que
       preguntar «¿existe?» y luego crearlo — dos operaciones, y entre las dos
       cabe el otro proceso. Es exactamente la carrera de `guardar_ingenuo()`,
       en miniatura: **preguntar y actuar por separado ES la carrera.**

    ⚠️ Y tiene un defecto real que se nombra en vez de esconderse: si el dueño
       MUERE sin soltarlo, el `.lock` se queda ahí y nadie vuelve a entrar. Por
       eso se mira su edad: pasados `CANDADO_RANCIO_S` se considera abandonado y
       se rompe. Es un arreglo con un supuesto dentro —que nadie tarda 30 s en
       guardar un renglón— y el supuesto queda escrito, que es la diferencia
       entre una decisión y un descuido (`LM.67`).
    """

    def __init__(self, archivo, espera_maxima_s=ESPERA_MAXIMA_S):
        self.ruta = Path(str(archivo) + ".lock")
        self.espera_maxima_s = espera_maxima_s

    def __enter__(self):
        limite = time.monotonic() + self.espera_maxima_s
        ultimo = None
        while True:
            try:
                fd = os.open(str(self.ruta), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, f"{os.getpid()} {datetime.now(timezone.utc).isoformat()}".encode())
                os.close(fd)
                return self

            # 🚨 SESIÓN 106 — LOS DOS ERRORES, Y EL SEGUNDO SOLO EXISTE EN WINDOWS.
            #    La primera versión solo atrapaba `FileExistsError`, que es lo que
            #    dice el manual y lo que pasa en Linux. En Windows, cuando el dueño
            #    BORRA su `.lock` mientras otro está intentando crearlo, el nombre
            #    entra en «borrado pendiente»: sigue existiendo, y cualquier
            #    apertura da `PermissionError [Errno 13]` — NO `FileExistsError`.
            #    Se midió: 2 de 60 procesos reventaron con un traceback, y su dato
            #    se perdió.
            # 🔑 EL CANDADO ERA CORRECTO; EL `except` ESTABA MAL. La lógica no
            #    tenía un solo fallo — lo que fallaba era la CLASIFICACIÓN del
            #    error, y esa clase de fallo no se ve leyendo el algoritmo.
            # ⚠️ Y en Linux esta prueba habría estado verde para siempre. Un
            #    detector que no puede morder en tu máquina no es un detector.
            except (FileExistsError, PermissionError) as fallo:
                ultimo = fallo
                if self._rancio():
                    self.ruta.unlink(missing_ok=True)
                    continue
                if time.monotonic() > limite:
                    # 📌 El motivo va DENTRO del mensaje: pasado el plazo ya no se
                    #    puede distinguir «ocupado» de «no tengo permiso», y un
                    #    motivo que tapa dos casos es el bicho del 6b. Se guarda
                    #    el error real en vez de resumirlo a una palabra.
                    raise CandadoOcupado(
                        f"{self.ruta.name} lleva ocupado más de "
                        f"{self.espera_maxima_s}s (último: {ultimo!r})"
                    )
                time.sleep(0.002)

    def __exit__(self, *_):
        self.ruta.unlink(missing_ok=True)
        return False

    def _rancio(self):
        try:
            return (time.time() - self.ruta.stat().st_mtime) > CANDADO_RANCIO_S
        except FileNotFoundError:
            return False


# ---------------------------------------------------------------------------
# 6) ARREGLO 3 — RELEER DENTRO DEL CANDADO, y el bueno completo
# ---------------------------------------------------------------------------
def guardar_dato(texto, quien="?", archivo=None):
    """El bueno. Devuelve (guardado, motivo).

    LOS CUATRO ARREGLOS, EN ORDEN, Y CADA UNO CONTRA SU FALLO:

      1. `_CANDADO_HILOS` ......... dos hilos del mismo proceso
      2. `_CandadoDeArchivo` ...... dos procesos distintos
      3. `cargar()` AQUÍ DENTRO ... la lectura vieja que pisa lo nuevo
      4. `_escribir_atomico()` .... el archivo que queda a medias

    🔑 EL 3 ES EL QUE SE OLVIDA, y es invisible: si `cargar()` se llamara ANTES
       del `with`, el candado estaría puesto, verde, y no serviría de nada —
       porque lo que se protege no es la escritura: es **la distancia entre leer
       y escribir**. Un candado mal colocado no da error; da confianza.

    🚨 Y EL MOTIVO `danado` ES EL HALLAZGO DEL DÍA CONVERTIDO EN FRENO. Si el
       archivo está dañado, esta función **NO escribe y devuelve `(False,
       "danado")`**. En el 6b escribía, borraba los datos viejos y devolvía
       `(True, "guardado")`. La promesa de *«no se borra el archivo dañado»*
       ahora la cumplen el lector Y el escritor.
    """
    ok, motivo, limpio = _revisar(texto)
    if not ok:
        return False, motivo

    archivo = Path(archivo or ARCHIVO)

    try:
        with _CANDADO_HILOS:
            with _CandadoDeArchivo(archivo):
                datos, estado = cargar(archivo)      # 👈 DENTRO. Ahí está el arreglo 3.

                if estado in ("danado", "otra_forma"):
                    return False, estado             # 👈 no se escribe encima

                antes = len(datos)
                datos = _mezclar(datos, limpio, quien)
                _escribir_atomico(datos, archivo)

                if len(datos) == antes and antes > 0:
                    return True, "refrescado"
                return True, "desplazo" if antes >= TOPE else "guardado"
    except CandadoOcupado:
        return False, "ocupado"


def guardar_solo_hilos(texto, quien="?", archivo=None):
    """Igual que el bueno PERO sin el candado de archivo. Existe para medir.

    🎲 APUESTA 3 en forma de función. Lleva el `threading.Lock`, la relectura
       dentro y la escritura atómica: **todo lo que un repaso de código llamaría
       "bien hecho"**. Entre hilos es perfecta. Entre procesos no protege nada,
       porque un `Lock` es un objeto en la memoria de UN proceso y dos procesos
       tienen dos.

    ⚠️ Y ese es el modo de fallo peor de este archivo: no se ve leyendo el
       código, no se ve en las pruebas de hilos, y las pruebas de hilos son las
       que cualquiera escribiría. Solo se ve lanzando dos `python`.
    """
    ok, motivo, limpio = _revisar(texto)
    if not ok:
        return False, motivo

    archivo = Path(archivo or ARCHIVO)
    with _CANDADO_HILOS:
        datos, estado = cargar(archivo)
        if estado in ("danado", "otra_forma"):
            return False, estado
        _escribir_atomico(_mezclar(datos, limpio, quien), archivo)
        return True, "guardado"


def recordar(dato, quien="?"):
    """Lo que llamaría el MODELO. Traduce el motivo a una instrucción.

    Igual que en el 6b: una tupla le dice al harness qué pasó; no le dice al
    modelo qué hacer. Con dos motivos nuevos que en el 6b no podían existir.
    """
    guardado, motivo = guardar_dato(dato, quien=quien)

    mensajes = {
        "guardado":    "Anotado. No se lo anuncies al usuario: sigue con su pregunta.",
        "desplazo":    "Anotado. Como la memoria estaba llena, salió un dato viejo.",
        "refrescado":  "Ya lo sabías: se le actualizó la fecha. No lo vuelvas a guardar.",
        "vacio":       "No guardaste nada: el dato venía vacío.",
        "muy_largo":   f"Demasiado largo. Resúmelo en menos de {LARGO_MAXIMO} "
                       "caracteres y vuelve a intentarlo.",
        "no_es_texto": "El dato tiene que ser texto. Vuelve a intentarlo.",
        # --- los dos que solo existen porque hay más de un escritor ---
        "ocupado":     "La memoria estaba ocupada. No insistas: sigue con la "
                       "pregunta del usuario, el dato no era imprescindible.",
        "danado":      "La memoria está dañada y NO se tocó. Sigue sin ella y "
                       "avisa al usuario de que hoy no recuerdas nada.",
        "otra_forma":  "La memoria tiene un formato que no entiendo y NO se tocó. "
                       "Sigue sin ella.",
    }

    return {"guardado": guardado, "motivo": motivo, "mensaje": mensajes[motivo]}


# ---------------------------------------------------------------------------
# 7) EL MEDIDOR — el experimento que produjo la tabla de la cabecera
# ---------------------------------------------------------------------------
MODOS = {
    "ingenuo":     guardar_ingenuo,       # ningún arreglo
    "solo_hilos":  guardar_solo_hilos,    # todo menos el candado entre procesos
    "arreglado":   guardar_dato,          # los cuatro arreglos
}


def carrera(n_hilos, vueltas=200, modo="ingenuo", carpeta=None):
    """Lanza N hilos que guardan N datos distintos A LA VEZ y cuenta el destrozo.

    ⭐ `threading.Barrier` es la pieza que hace honesto el experimento: sin ella
       los hilos arrancan escalonados y la carrera casi no ocurre. La barrera los
       retiene a todos hasta que el último llega, y entonces los suelta juntos.
       **Un experimento de concurrencia sin barrera mide el arranque, no la
       carrera** — y habría dado verde por el motivo equivocado.
    """
    guardar = MODOS[modo]
    carpeta = Path(carpeta or tempfile.mkdtemp())
    esperados = min(n_hilos, TOPE)

    invalidos = vacios = perdidos = 0

    for v in range(vueltas):
        arch = carpeta / f"c_{modo}_{n_hilos}_{v}.json"
        barrera = threading.Barrier(n_hilos)

        def escribe(i):
            barrera.wait()
            guardar(f"dato-{i}", quien=f"w{i}", archivo=arch)

        hilos = [threading.Thread(target=escribe, args=(i,)) for i in range(n_hilos)]
        for h in hilos:
            h.start()
        for h in hilos:
            h.join()

        datos, estado = cargar(arch)
        if estado in ("danado", "otra_forma"):
            invalidos += 1
        if not datos:
            vacios += 1
        perdidos += esperados - len(datos)

        arch.unlink(missing_ok=True)
        Path(str(arch) + ".lock").unlink(missing_ok=True)

    return {
        "modo": modo, "hilos": n_hilos, "vueltas": vueltas, "esperados": esperados,
        "invalidos": invalidos, "vacios": vacios,
        "perdidos": perdidos, "total": esperados * vueltas,
    }


def carrera_entre_procesos(n=5, vueltas=12, modo="solo_hilos", carpeta=None):
    """Lo mismo, pero lanzando `python` de verdad. Es la prueba de la apuesta 3.

    🔑 Aquí no hay barrera posible —los procesos no comparten objetos, que es
       justo el problema que se está midiendo—, así que el arranque se sincroniza
       por RELOJ: a todos se les da el mismo instante futuro y esperan a que
       llegue. Es más burdo que una barrera y es lo único que hay.
       ⭐ Y es la lección en miniatura: **lo que se comparte entre procesos hay
          que escribirlo en algún sitio que los dos puedan ver.** Un candado
          también.
    """
    import subprocess

    carpeta = Path(carpeta or tempfile.mkdtemp())
    perdidos = rotos = reventados = 0

    for v in range(vueltas):
        arch = carpeta / f"p_{modo}_{v}.json"
        arranque = time.time() + 1.0
        procs = [
            subprocess.Popen(
                [sys.executable, str(Path(__file__).resolve()), "--procesos",
                 f"w{i}", str(arch), modo, str(arranque)],
                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            for i in range(n)
        ]
        for p in procs:
            _, err = p.communicate()
            if p.returncode != 0:
                reventados += 1

        datos, estado = cargar(arch)
        if estado in ("danado", "otra_forma"):
            rotos += 1
        perdidos += n - len(datos)

    return {"modo": modo, "procesos": n, "vueltas": vueltas,
            "perdidos": perdidos, "total": n * vueltas,
            "rotos": rotos, "reventados": reventados}


def informe_de_hoy():
    """Reproduce la tabla de la cabecera. $0,00 y sin red."""
    print("\n" + "=" * 74)
    print("D.1 · LA CARRERA — N workers guardando a la vez sobre el mismo archivo")
    print("=" * 74)
    print(f"\n{'modo':>10} {'hilos':>6} {'esperaba':>9} {'JSON roto':>16} "
          f"{'quedó vacío':>12} {'DATOS PERDIDOS':>18}")

    for modo in ("ingenuo", "arreglado"):
        for n in (2, 3, 6, 12):
            r = carrera(n, vueltas=60, modo=modo)
            print(f"{r['modo']:>10} {r['hilos']:>6} {r['esperados']:>9} "
                  f"{r['invalidos']:>4}/{r['vueltas']} ({100*r['invalidos']/r['vueltas']:5.1f}%) "
                  f"{r['vacios']:>5}/{r['vueltas']} "
                  f"{r['perdidos']:>7}/{r['total']} ({100*r['perdidos']/r['total']:5.1f}%)")
        print()

    print("🔑 La fila de 2 hilos del modo ingenuo es la trampa del temario, medida:")
    print("   dos workers pierden la mitad y el archivo queda VÁLIDO. Nadie grita.\n")


# ---------------------------------------------------------------------------
# 8) LAS PRUEBAS — todas gratis, sin red, sin modelo
# ---------------------------------------------------------------------------
def _pruebas():
    fallos = []

    def check(nombre, cond, detalle=""):
        print(("  OK  " if cond else "  XX  ") + nombre + (f"  -> {detalle}" if detalle else ""))
        if not cond:
            fallos.append(nombre)

    print("\n[D.1] memoria compartida entre workers\n")
    carpeta = Path(tempfile.mkdtemp())

    # --- P1-P4: los frenos de entrada siguen siendo los del 6b -------------
    a = carpeta / "p1.json"
    check("P1 · el dato vacío no entra", guardar_dato("   ", archivo=a) == (False, "vacio"))
    check("P2 · el dato larguísimo no entra",
          guardar_dato("z" * (LARGO_MAXIMO + 1), archivo=a) == (False, "muy_largo"))
    check("P3 · lo que no es texto no entra", guardar_dato(42, archivo=a) == (False, "no_es_texto"))
    check("P4 · y ninguno de los tres llegó a crear el archivo", not a.exists())

    # --- P5-P7: lo aburrido, que también tiene que estar -------------------
    b = carpeta / "p5.json"
    check("P5 · el primer dato entra", guardar_dato("es contador", quien="w1", archivo=b) == (True, "guardado"))
    check("P6 · repetirlo lo REFRESCA, no lo duplica",
          guardar_dato("ES CONTADOR", quien="w2", archivo=b) == (True, "refrescado"))
    datos, estado = cargar(b)
    check("P7 · y queda UN solo dato", len(datos) == 1 and estado == "ok", f"{len(datos)} datos")

    # --- P8: el estado que el 6b no devolvía -------------------------------
    c = carpeta / "p8.json"
    c.write_text('{"datos": [{"dato": "x"', encoding="utf-8")
    check("P8 · un archivo dañado se lee como (vacío, 'danado'), no como vacío a secas",
          cargar(c) == ([], "danado"))

    # --- P9: 🚨 EL HALLAZGO DEL DÍA, convertido en prueba ------------------
    # Es la prueba que la sesión existe para escribir. Si mañana alguien
    # "simplifica" guardar_dato() quitando el corte por `danado`, esta se pone
    # roja — y sin ella el bug es invisible, porque el bug DEVUELVE VERDE.
    antes = c.read_text(encoding="utf-8")
    check("P9 · escribir sobre un archivo DAÑADO se rechaza",
          guardar_dato("dato nuevo", archivo=c) == (False, "danado"))
    check("P9b · y el archivo dañado sigue INTACTO: la evidencia no se borró",
          c.read_text(encoding="utf-8") == antes)

    # --- P10: y el contraste, que es lo que lo vuelve un hallazgo ----------
    # ⚠️ Sin esta prueba, P9 solo dice "mi código hace lo que escribí". Con ella
    #    dice "y el de al lado hace lo contrario". Un detector que no se ve morder
    #    es una nota (LM.13); aquí se le ve morder sobre la versión ingenua.
    d = carpeta / "p10.json"
    guardar_ingenuo("uno", quien="w1", archivo=d)
    guardar_ingenuo("dos", quien="w1", archivo=d)
    texto = d.read_text(encoding="utf-8")
    d.write_text(texto[: len(texto) // 2], encoding="utf-8")
    guardar_ingenuo("tres", quien="w1", archivo=d)
    quedan, _ = cargar(d)
    check("P10 · la forma INGENUA sí borra la evidencia y devuelve verde",
          len(quedan) == 1 and quedan[0]["dato"] == "tres",
          f"quedaron {[f['dato'] for f in quedan]}")

    # --- P11-P13: `_mezclar` es pura, así que se prueba sin hilos ----------
    lista = [{"dato": f"d{i}", "fecha": "2020-01-01", "quien": "w1"} for i in range(TOPE)]
    salida = _mezclar(lista, "nuevo", "w1")
    check("P11 · el tope se respeta", len(salida) == TOPE, f"{len(salida)} de {TOPE}")
    check("P11b · y con un solo worker sale el más viejo",
          salida[0]["dato"] == "d1", salida[0]["dato"])

    # 🎲 APUESTA 5, hecha prueba: la política del 6b desaloja al worker callado.
    lista = [{"dato": f"d{i}", "fecha": "2020-01-01", "quien": "w1"} for i in range(TOPE - 1)]
    lista.insert(0, {"dato": "el unico de w2", "fecha": "2019-01-01", "quien": "w2"})
    salida = _mezclar(lista, "nuevo de w1", "w1")
    check("P12 · la RESERVA protege el único dato del worker callado",
          any(f["dato"] == "el unico de w2" for f in salida),
          f"desalojó a {[f['dato'] for f in lista if f not in salida]}")
    check("P12b · y el que salió fue el más viejo DE LOS DESALOJABLES",
          not any(f["dato"] == "d0" for f in salida))

    # ⚠️ Y el límite de la reserva, dicho en vez de escondido.
    lista = [{"dato": f"d{i}", "fecha": "2020-01-01", "quien": f"w{i}"} for i in range(TOPE)]
    salida = _mezclar(lista, "nuevo", "wX")
    check("P13 · si TODOS tienen uno solo, la reserva no puede cumplirse y sale el más viejo",
          len(salida) == TOPE and salida[0]["dato"] == "d1")

    # --- P14: el candado de archivo, y que de verdad excluye ---------------
    e = carpeta / "p14.json"
    with _CandadoDeArchivo(e):
        try:
            with _CandadoDeArchivo(e, espera_maxima_s=0.05):
                check("P14 · el candado de archivo excluye al segundo", False, "entró")
        except CandadoOcupado:
            check("P14 · el candado de archivo excluye al segundo", True)
    check("P14b · y al salir se suelta", not Path(str(e) + ".lock").exists())
    check("P14c · y con el candado suelto, guardar funciona",
          guardar_dato("ya se puede", archivo=e) == (True, "guardado"))

    # --- P15: escritura atómica --------------------------------------------
    f = carpeta / "p15.json"
    _escribir_atomico([{"dato": "x", "fecha": "2026-01-01", "quien": "w1"}], f)
    check("P15 · la escritura atómica deja un JSON válido", cargar(f)[1] == "ok")
    check("P15b · y no deja temporales tirados",
          not list(carpeta.glob(".tmp_*")), [p.name for p in carpeta.glob(".tmp_*")])

    # --- P16-P17: LA CARRERA. El control y el arreglo, juntos --------------
    # 🚨 Las dos van juntas o no vale ninguna. P17 sola diría "no se rompió", y
    #    eso puede ser el candado o puede ser que el experimento no apretara.
    ing = carrera(6, vueltas=40, modo="ingenuo", carpeta=carpeta)
    check("P16 · CONTROL: sin candado se pierden datos de verdad",
          ing["perdidos"] > 0,
          f"{ing['perdidos']}/{ing['total']} perdidos ({100*ing['perdidos']/ing['total']:.0f}%)")

    arr = carrera(6, vueltas=40, modo="arreglado", carpeta=carpeta)
    check("P17 · ARREGLADO: no se pierde ni uno",
          arr["perdidos"] == 0, f"{arr['perdidos']}/{arr['total']} perdidos")
    check("P17b · y ni un solo archivo roto", arr["invalidos"] == 0)

    # --- P18: dos hilos, que es LITERAL la trampa del temario ---------------
    dos = carrera(2, vueltas=60, modo="ingenuo", carpeta=carpeta)
    check("P18 · con DOS workers el ingenuo pierde ~la mitad y NO rompe el archivo",
          dos["perdidos"] > dos["total"] * 0.25 and dos["invalidos"] == 0,
          f"{100*dos['perdidos']/dos['total']:.0f}% perdidos, "
          f"{dos['invalidos']} archivos rotos")

    # --- P19-P21: 🚨 LA APUESTA 3. Lanza `python` de verdad, y tarda ~15 s.
    # Es la prueba cara de la suite y se queda igual, porque es la ÚNICA que
    # puede ver el fallo más caro del archivo: `solo_hilos` pasa TODAS las
    # pruebas de hilos y no protege nada entre procesos. Sin P19 el bug es
    # invisible, y es invisible del peor modo — leyendo el código parece bien.
    print("\n  (P19-P21 lanzan procesos de verdad: tardan ~15 s)")
    sh = carrera_entre_procesos(n=4, vueltas=4, modo="solo_hilos", carpeta=carpeta)
    check("P19 · CONTROL: candado de HILOS + atómico + relectura, y entre "
          "PROCESOS pierde igual",
          sh["perdidos"] > sh["total"] * 0.3,
          f"{sh['perdidos']}/{sh['total']} perdidos, {sh['reventados']} procesos caídos")

    ar = carrera_entre_procesos(n=4, vueltas=4, modo="arreglado", carpeta=carpeta)
    check("P20 · con el candado de ARCHIVO no se pierde ni uno entre procesos",
          ar["perdidos"] == 0, f"{ar['perdidos']}/{ar['total']} perdidos")
    check("P21 · y no se cae ni un proceso",
          ar["reventados"] == 0, f"{ar['reventados']} caídos")

    print()
    if fallos:
        print(f"XX  {len(fallos)} en rojo: {', '.join(fallos)}")
    else:
        print("OK  todas en verde")
    return fallos


if __name__ == "__main__":
    if "--carrera" in sys.argv:
        informe_de_hoy()
        sys.exit(0)

    if "--procesos" in sys.argv:
        # Lo llama `procesos.py`. Un solo dato, y sale.
        etiqueta = sys.argv[sys.argv.index("--procesos") + 1]
        ARCHIVO = Path(sys.argv[sys.argv.index("--procesos") + 2])
        modo = sys.argv[sys.argv.index("--procesos") + 3]
        arranque = float(sys.argv[sys.argv.index("--procesos") + 4])
        while time.time() < arranque:      # todos salen al mismo segundo
            time.sleep(0.001)
        print(MODOS[modo](f"dato-{etiqueta}", quien=etiqueta, archivo=ARCHIVO))
        sys.exit(0)

    if "--entre-procesos" in sys.argv:
        print("\n" + "=" * 74)
        print("D.1 · LA MISMA CARRERA, PERO CON PROCESOS DE VERDAD (5 × 12 vueltas)")
        print("=" * 74)
        print(f"\n{'modo':>12} {'perdidos':>18} {'archivos rotos':>16} {'procesos caídos':>17}")
        for m in ("ingenuo", "solo_hilos", "arreglado"):
            r = carrera_entre_procesos(modo=m)
            print(f"{r['modo']:>12} {r['perdidos']:>8}/{r['total']:<4} "
                  f"({100*r['perdidos']/r['total']:5.1f}%) {r['rotos']:>10} "
                  f"{r['reventados']:>16}")
        print("\n🔑 `solo_hilos` lleva candado, relectura dentro y escritura atómica.")
        print("   Entre hilos es perfecto. Mira su fila.\n")
        sys.exit(0)

    fallado = _pruebas()
    print("\n📊 Para ver la tabla de la carrera:  python compartida.py --carrera")
    sys.exit(1 if fallado else 0)
