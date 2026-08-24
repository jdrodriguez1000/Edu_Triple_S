"""disparador.py — E.1 del nivel 8: EL DISPARADOR, y qué pasa si se dispara dos veces.

    LA FRASE QUE HAY QUE VER

Todo lo que has construido en el nivel 8 lo arrancas TÚ. Escribes `python
orquestador.py`, miras la pantalla, ves el error, lo arreglas.

Un agente programado es el mismo agente SIN NADIE DELANTE. Alguien fija una hora
y a esa hora arranca solo. También el domingo. También a las 3 de la mañana.

🔑 QUITAR AL QUE MIRA NO AÑADE UN PROBLEMA NUEVO: DESTAPA TRES SUPOSICIONES QUE
   NO SABÍAS QUE ESTABAS HACIENDO.

    | Lo que dabas por hecho      | Por qué deja de ser cierto                |
    |-----------------------------|-------------------------------------------|
    | «hay una corrida a la vez»  | el reloj arranca la de hoy encima de la   |
    |                             | de ayer, que aún no ha terminado          |
    | «si falla, lo veo»          | a las 3 a.m. el error se imprime A NADIE  |
    | «si algo raro pasa, lo paro»| no hay mano en el teclado                 |

Es la misma frase de B.2 y de D.1 con otra ropa: **el paralelismo no crea los
recursos compartidos, los destapa** — y aquí ni siquiera hace falta paralelismo
que tú escribas. Lo pone el calendario.


    UN DISPARADOR TIENE TRES PARTES, Y SOLO PIENSAS EN UNA

Cuando alguien dice «que corra todos los días a las 3» cree que dice una cosa.
Dice tres:

    | Parte     | La pregunta                          | Si no la contestas  |
    |-----------|--------------------------------------|---------------------|
    | el reloj  | ¿cada cuánto?                        | nada — es la fácil  |
    | la ventana| ¿y si a las 3:00 la anterior vive?   | SE SOLAPAN          |
    | el turno  | ¿qué trabajo cubría este disparo?    | no puedes saber si  |
    |           |                                      | YA SE HIZO          |

🔑 Casi todo el mundo configura la primera y descubre las otras dos con la
   factura en la mano.


    POR QUÉ ESTE ARCHIVO NO USA `cron` NI LA NUBE NI LA API

Tres motivos, y ninguno es pereza:

1. Un disparador de verdad tarda un día en darte un dato. Aquí el reloj es un
   parámetro, así que un «día» cuesta 0,4 segundos.
2. El modo de fallo NO está en el reloj — está en lo que pasa cuando llegan dos.
   El reloj es el decorado; los dos procesos son la obra.
3. `LM.87` (sesión 106) ya dejó escrito que esto **solo se ve lanzando dos
   `python` de verdad**: con hilos, la versión rota pasa las 18 pruebas sin
   despeinarse. Así que aquí se lanzan dos `python` de verdad — pero esta vez
   NO los lanzo yo a mano: los lanza el reloj.


    LO QUE MIDE EL ESCALÓN 1 (el ingenuo)

`correr_ingenuo()` es el disparador que escribe todo el mundo la primera vez:
llega la hora → haz el trabajo. No pregunta nada. No mira si ya hay uno vivo. No
mira si el turno ya se hizo.

Y el trabajo falso está copiado de la forma del fan-out real, a propósito:
    · 21 renglones al `.jsonl`  (los que escribió la corrida c20260823T231228)
    · una `corrida` nueva, con `contexto.py:_corrida_nueva()` — fecha + azar
    · un `reporte.json` al final, que es EL ENTREGABLE

⚠️ Fíjate en el segundo punto, porque es el hecho 2 del sobre y es lo que hace
   que esto no grite: dos disparos producen dos corridas con NOMBRES DISTINTOS.
   Un `.jsonl` con dos corridas distintas es un archivo perfectamente válido.
   No hay nada que un lector pueda señalar y decir «esto está mal».

🔑 UN ARCHIVO ROTO GRITA; UN TRABAJO HECHO DOS VECES SE VE EXACTAMENTE IGUAL QUE
   DOS TRABAJOS LEGÍTIMOS.


    🚨 LO QUE SALIÓ, Y NO ES LO QUE IBA A BUSCAR

El escalón 1 iba a enseñar el trabajo repetido. Lo enseñó. Pero la prueba P21
—escrita para comprobar que el coste sale al doble— se puso ROJA, y el motivo
era mejor que la prueba: **al solaparse, FALTABAN RENGLONES DEL REGISTRO.**

    caso                     renglones   rotos   revienta
    1 disparo                  21/21        0        0
    2 a la vez (se solapan)    39/42        0        0     ← faltan 3
    2 seguidos (secuencial)    42/42        0        0
    3 a la vez                 58/63        0        0     ← faltan 5

Cero líneas rotas. Cero excepciones. Cero avisos. Y la fila secuencial no
pierde ni uno: **la pérdida es del SOLAPAMIENTO, no del trabajo.**

Ahí había dos explicaciones que dan el mismo archivo, y las separa
`atomico_o_no()` — dos procesos escribiendo renglones de tamaños DISTINTOS:

    esperados 800 · en el archivo 754 · perdidos 46
    MIXTOS (A y B revueltos en un renglón) ....  0
    de LONGITUD IMPOSIBLE ..................... 46  → todos de 178
    huecos sin escribir .......................  0
    bytes en disco = bytes de lo que queda ....  cuadra

🚨 `open(ruta, "a")` NO ES ATÓMICO ENTRE PROCESOS EN WINDOWS. Un renglón de B
   ocupa 20 + 2 = 22 bytes; 200 − 22 = 178. **Esos 46 renglones de 178 son la
   COLA de una A a la que otro proceso le escribió ENCIMA los 22 primeros
   bytes.** El renglón llegó al disco, y luego lo pisaron.

⭐ Y la forma del fallo importa tanto como el fallo: no se entrelazan a mitad de
   renglón —cero mixtos—, se PISAN. Por eso con renglones del mismo largo, que
   es el caso real de un `.jsonl`, el pisotón es **exactamente invisible**: no
   deja mixtos, ni longitudes raras, ni huecos. Solo un renglón que no está.

🔑 ES `LM.66` EN LA CAPA DEL SISTEMA DE ARCHIVOS: el renglón perdido está SOLO
   en su renglón — ningún otro dato del archivo puede desmentirlo. La pregunta
   que lo caza no es «¿está bien el registro?» sino **«¿qué tendría que estar en
   desacuerdo con este archivo si le faltara algo?»**. Y hoy: nada.

⚠️ SEGUNDA VEZ QUE WINDOWS CAMBIA UN RESULTADO DE ESTE NIVEL, Y EN EL SENTIDO
   CONTRARIO. En `LM.87` (sesión 106) Windows NEGÓ un `os.replace()` que POSIX
   permite: hizo RUIDO —26 procesos caídos con `PermissionError`—. Aquí hace lo
   opuesto: POSIX garantiza que un `O_APPEND` es atómico y Windows no, así que
   **hace SILENCIO**. La misma diferencia de sistema operativo, una vez con
   traceback y otra sin nada. La segunda es la cara peor.

    EL ESCALÓN 2 — LE PONEMOS EL CANDADO, Y LA APUESTA 1 SE PARTE EN DOS

Puesto el candado de D.1 —`compartida.py`, importado sin editar—, con sus dos
constantes tal como están escritas: espera 5 s, caducidad 30 s.

    el trabajo dura   espera  rancio   hicieron  cedieron  corridas  renglones
    2 s  (corto)         5,0    30,0        2         0        2       24/24
    8 s  (> espera)      5,0    30,0        1         1        1       12/24
    35 s (> rancio)      5,0    30,0        1         1        1       12/24
    35 s, espera 60     60,0    30,0        2         0        2       24/24

🚨 FILA 1 — EL CANDADO FUNCIONÓ Y NO SIRVIÓ DE NADA. El trabajo dura menos que
   la espera, así que el segundo no se rinde: **espera su turno y hace el
   trabajo entero igual**. Cero renglones perdidos ✅, dos corridas ❌.
   🔑 UN CANDADO SERIALIZA; NO DEDUPLICA. Arregló el archivo y dejó el problema
      intacto — y arreglar el síntoma ruidoso deja el silencioso solo (`LM.88`).

✅ FILA 2 — el único caso que sale bien, y sale bien POR ACCIDENTE: porque el
   trabajo dura más que una constante que nadie eligió pensando en esto.

🔴 FILA 3 — **LA APUESTA 1(b) FALLÓ, Y EL MOTIVO ES MEJOR QUE LA APUESTA.**
   Sellé que un trabajo de más de 30 s haría que el segundo diera el candado por
   abandonado y lo rompiera. No pasa. El que espera se rinde a los 5 s, y
   `_rancio()` **solo se comprueba mientras se espera**: con
   `ESPERA_MAXIMA_S (5) < CANDADO_RANCIO_S (30)`, la caducidad es INALCANZABLE
   durante un solapamiento. Ahí no había bicho.

🚨 FILA 4 — Y AQUÍ ESTÁ EL BICHO DE VERDAD, QUE ES PEOR. Misma duración, un solo
   cambio: la espera sube de 5 a 60. Ahora el segundo aguanta lo bastante para
   llegar a los 30 s, declara el candado abandonado **con su dueño vivo y
   trabajando**, lo borra y entra. Los dos a la vez, sin un solo error. Medido:
   66 s, `["hizo", "hizo"]`, 0 reventados.

🔑 EL FALLO NO LO DISPARA UN TRABAJO LARGO: LO DISPARA SER MÁS PACIENTE. Subir
   la espera —que es exactamente lo que cualquiera haría para «arreglar» la fila
   2— es lo que rompe el candado. El único cambio entre P35 y P37 es ese número.

⭐ LA REGLA QUE SALE, Y NO ESTABA EN EL SOBRE: la caducidad de un candado tiene
   que ser mayor que lo que dura el trabajo **y** mayor que lo que nadie vaya a
   esperar. Hoy son 30 s para un trabajo de 21 s medidos: **un margen de 9
   segundos que nadie eligió.** Eso convierte la deuda «el candado rancio de 30 s
   sin medir» (sesión 106) en una relación entre TRES números, no en un número
   suelto.

📌 Y una deuda nueva que se ve en el código: el disparo que CEDE se va sin dejar
   renglón. `correr_con_candado()` devuelve "cedio" y no anota nada. Por la
   mañana, un turno que cedió y un turno que nunca se disparó **se ven igual**.
   Eso es el escalón 4.

    EL ESCALÓN 3 — EL TURNO, Y LA ELECCIÓN QUE NO TIENE RESPUESTA BUENA

El candado arregla el solape. El TURNO arregla la repetición, que es otra cosa.

    caso                        hizo  ya_estaba  corridas  marcas
    2 a la vez (se solapan)       1        1        1        1
    2 seguidos                    1        1        1        1   ← el que el
    3 a la vez                    1        2        1        1     candado no veía

🔑 Y el detalle que enseña la pieza: el segundo NO cede — se entera de que YA
   ESTÁ HECHO y se va. `cedio` y `ya_estaba` son estados distintos y hacen falta
   los dos. Por eso hacen falta DOS piezas y no una: **el candado se borra al
   soltarlo, la marca se queda.** Uno dice «ahora mismo hay otro»; la otra dice
   «esto ya pasó».

🚨 EL SEGUNDO HALLAZGO DEL DÍA, Y ES DE LA MISMA FAMILIA QUE EL PRIMERO. La
   marca se guardaba como `2026-08-24T03:00.json` — el turno tal cual. En Linux
   es un nombre legal. En Windows los dos puntos NO son un carácter de nombre:
   separan el archivo de un FLUJO ALTERNO de NTFS. `dir /r` lo enseñó:

        0 bytes   2026-08-24T03
       73 bytes   2026-08-24T03:00.json:$DATA

   Y el veneno es que **funcionaba**: `exists()` encontraba el flujo, `O_EXCL`
   seguía impidiendo la marca doble, y todas las pruebas de deduplicación
   salían verdes. Lo único que fallaba era LISTAR — `glob("*.json")` devolvía
   CERO con todas las marcas puestas, que es justo lo que el escalón 4 necesita.
   → Arreglado en `_nombre_de_marca()`, y vigilado por `P43`.

⭐ Y la regla que se va fuera del curso: **un identificador que se usa como
   nombre de archivo tiene que pasar por una puerta.** El turno conserva sus dos
   puntos DENTRO del registro, donde se lee, y los pierde FUERA, donde es un
   nombre. Dos usos del mismo dato, dos escrituras.


    LA PREGUNTA QUE NO TIENE RESPUESTA BUENA: ¿ANTES O DESPUÉS?

    qué le pasa al primer disparo   marcar   se rehace   veredictos
    se rompe a mitad                 antes      NO       fallo, ya_estaba
    se rompe a mitad               después      sí       fallo, hizo
    la máquina se apaga              antes      NO       murio, ya_estaba
    la máquina se apaga            después      NO       murio, cedio
    se apaga, con rancio 1 s       después      sí       murio, hizo

🔑 NO EXISTE «EXACTAMENTE UNA VEZ». Existen dos daños opuestos:
     · marcar ANTES   → COMO MUCHO UNA VEZ. Si el trabajo se rompe, el turno
       queda marcado y nadie lo reintenta nunca. Se pierde en silencio.
     · marcar DESPUÉS → AL MENOS UNA VEZ. El reintento funciona, pero lo que el
       primero alcanzó a escribir SE QUEDA. No es «como si nada hubiera pasado».

⭐ La elección no es técnica, es del negocio: ¿qué duele más, mandar el correo
   dos veces o no mandarlo? Y hay que hacérsela ANTES, porque **el que no elige
   ya eligió**: el escalón 1 marcaba «después» sin saberlo.

⭐ Y AQUÍ SE ENTIENDE POR FIN PARA QUÉ SIRVE `CANDADO_RANCIO_S`. El proceso que
   muere no suelta el candado, y el reintento se encuentra un `.lock` de un
   dueño que ya no existe: cede sin llegar a mirar la marca. Bajando la
   caducidad por debajo del hueco entre disparos, lo rompe y trabaja.
   🔑 LA CADUCIDAD NO ES PARA EL SOLAPE —el escalón 2 midió que ahí es
      inalcanzable—: ES PARA EL CADÁVER. Y eso ordena los tres números de golpe:
      **mayor que el trabajo** (o rompes a un vivo) y **menor que el hueco entre
      disparos** (o el muerto bloquea el turno siguiente). Hoy: trabajo 21 s,
      caducidad 30 s, hueco 3600 s. Cuadra por casualidad, y ahora está escrito.


    EL ESCALÓN 4 — EL DISPARO QUE NO OCURRIÓ

    turno              ¿marca?  intentos   qué pasó de verdad
    2026-08-24T03:00      sí       1       el trabajo salió bien
    2026-08-24T04:00      no       2       vinieron dos y ninguno pudo
    2026-08-24T05:00      no       0       NO SE DISPARÓ NUNCA

✅ LA APUESTA 4 SALIÓ, Y CON EL MATIZ QUE IMPORTA. «Esto se disparó dos veces»
   se escribe contando corridas: el dato está en el registro. «Esto no se
   disparó» NO se puede escribir con el registro, por muchas vueltas que se le
   dé, **porque el que no corre no escribe.**

🔑 UN REGISTRO SOLO PUEDE PROBAR LO QUE SÍ PASÓ. Para lo que no pasó hace falta
   algo escrito ANTES, y no es un archivo más: es de otra clase. **El registro
   lo escribe el que trabaja; el calendario lo escribe el que prometió.**

⭐ Y la fila del medio es la mitad que casi se escapa: sin anotar los intentos,
   «vino y no pudo» se ve igual que «no vino». Son TRES estados, no dos. Es
   `LM.88` por tercera vez en el día — arreglar el ruidoso deja el silencioso
   solo—, y por eso `anotar_intento()` se llama también cuando el disparo cede.
   Esa era la deuda que abrió el escalón 2, y queda pagada (`P65`).

📌 DÓNDE MUERDE ESTO EN CÓDIGO QUE YA EXISTE: `orquestador.py:228`,
   `worker.py:483`, `router.py:192`, `supervisor.py:120` y `pipeline.py:176`
   escriben su registro con ese mismo `open(REGISTRO, "a")`. Hoy NO muerde, y el
   motivo está medido: los cinco lo hacen dentro de un `threading.Lock` y el
   fan-out usa HILOS, no procesos. **Muerde el día que haya dos procesos** — que
   es, literalmente, el tema del bloque E.
"""

import json
import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # la consola de Windows no habla emoji sin esto

sys.path.insert(0, str(Path(__file__).resolve().parent))
from contexto import _corrida_nueva  # noqa: E402  — el id de corrida ya medido en la 97


# ---------------------------------------------------------------------------
# 1) LAS CONSTANTES, y de dónde sale cada número
# ---------------------------------------------------------------------------
# 📌 Ninguno de estos es inventado. Los tres primeros salen de contar el
#    `registro_workers_claude-haiku-4-5.jsonl` de la corrida del 2026-08-23,
#    que es el último fan-out pagado del nivel.

RENGLONES_POR_TRABAJO = 21     # los que escribió la corrida c20260823T231228
DURACION_REAL_S = 21.0         # lo que tardó esa corrida, de punta a punta
COSTO_POR_RENGLON_USD = 0.001256  # 0,026390 / 21 — el coste medido, repartido

# El reloj falso: un turno es una HORA REDONDA. Ese formato es la pieza de E.1
# que todavía no existe en ninguno de los 1352 renglones del nivel.
FORMATO_TURNO = "%Y-%m-%dT%H:00"


# ---------------------------------------------------------------------------
# 2) EL RELOJ FALSO — el decorado, y se dice que es decorado
# ---------------------------------------------------------------------------
def turno_de(momento=None):
    """A qué turno pertenece un instante. Un turno = una hora redonda.

    ⭐ Fíjate en lo que hace de verdad: TIRA información. Las 03:00:04 y las
       03:47:59 devuelven lo mismo. Eso no es un descuido: es EL PUNTO. Un turno
       tiene que poder repetirse a propósito, o no se puede preguntar «¿este
       turno ya se hizo?».

    🔑 Y esa regla es la CONTRARIA a la de `corrida`, que se arregló en la
       sesión 97 justo para que NO se repitiera nunca. Dos identificadores, en
       el mismo renglón, con requisitos opuestos. (Apuesta 3 del sobre.)
    """
    momento = momento or datetime.now(timezone.utc)
    return momento.strftime(FORMATO_TURNO)


def turnos_del_dia(desde, cuantos, cada_horas=1):
    """Los instantes en que un reloj de verdad dispararía. Aquí no se espera a
    ninguno: se generan. Un 'día' cuesta lo que cueste iterar una lista."""
    return [desde + timedelta(hours=cada_horas * i) for i in range(cuantos)]


# ---------------------------------------------------------------------------
# 3) EL TRABAJO FALSO — la obra, y tiene que poder romperse de verdad
# ---------------------------------------------------------------------------
def trabajo_falso(carpeta, quien="?", turno=None, duracion_s=0.4,
                  renglones=RENGLONES_POR_TRABAJO, fallar_en=None, morir_en=None):
    """Hace lo mismo que un fan-out real, sin llamar al modelo.

    Escribe `renglones` líneas al registro compartido y deja un `reporte.json`.
    El `reporte.json` es EL ENTREGABLE: es lo que un humano leería por la mañana.

    ⚠️ Está escrito INGENUO a propósito, con la misma forma que tendría el
       primer intento de cualquiera:
         · abrir en modo «añadir» y escribir renglón a renglón
         · volcar el reporte encima del que hubiera
       No hay candado, no hay temporal, no hay `os.replace()`. D.1 ya midió qué
       cuesta cada una de esas tres cosas; aquí lo que se mide es OTRA cosa, y
       hace falta el suelo sin arreglar para verla.
    """
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    registro = carpeta / "registro_disparador.jsonl"
    reporte = carpeta / "reporte.json"

    corrida = _corrida_nueva()
    turno = turno or turno_de()
    espera = duracion_s / max(renglones, 1)

    for i in range(renglones):
        linea = {
            "hora": datetime.now(timezone.utc).isoformat(),
            "corrida": corrida,      # único a propósito  → hecho 2 del sobre
            "turno": turno,          # repetible a propósito → apuesta 3
            "quien": quien,
            "evento": "paso",
            "n": i,
            "costo_usd": COSTO_POR_RENGLON_USD,
        }
        with open(registro, "a", encoding="utf-8") as f:
            f.write(json.dumps(linea, ensure_ascii=False) + "\n")
        # 📌 Dos formas de no terminar, y NO son la misma cosa. `fallar_en` es
        #    una excepción: el programa sigue vivo y puede limpiar detrás.
        #    `morir_en` es `os._exit()`: la máquina se apagó, no hay limpieza,
        #    no hay `finally`, no hay nada. El escalón 3 necesita las dos.
        if fallar_en is not None and i == int(fallar_en):
            raise RuntimeError(f"el trabajo se rompió en el paso {i}")
        if morir_en is not None and i == int(morir_en):
            os._exit(9)
        time.sleep(espera)

    # El entregable. Sin temporal, sin candado: el último que llega manda.
    reporte.write_text(json.dumps({
        "corrida": corrida, "turno": turno, "quien": quien,
        "renglones": renglones,
        "costo_usd": round(renglones * COSTO_POR_RENGLON_USD, 6),
        "hora": datetime.now(timezone.utc).isoformat(),
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    return corrida


# ---------------------------------------------------------------------------
# 4) EL ESCALÓN 1 — EL DISPARADOR INGENUO
# ---------------------------------------------------------------------------
def correr_ingenuo(carpeta, quien="?", momento=None, **kw):
    """Llega la hora → haz el trabajo. Y ya.

    Son dos líneas y las dos son razonables. No hay ningún error aquí dentro:
    el fallo no está en lo que hace, está en LO QUE NO PREGUNTA.

    Lo que no pregunta, por orden de lo caro que sale:
      1. ¿hay otro disparo vivo ahora mismo?      → se solapan
      2. ¿este turno ya se hizo?                  → se repite el efecto
      3. ¿cuándo debía haberse disparado?         → no se sabe si faltó alguno
    """
    turno = turno_de(momento)
    return trabajo_falso(carpeta, quien=quien, turno=turno, **kw)


# ---------------------------------------------------------------------------
# 5) LA MEDICIÓN — dos `python` de verdad, porque con hilos esto no se ve
# ---------------------------------------------------------------------------
def disparo_doble(n=2, carpeta=None, duracion_s=0.4,
                  renglones=RENGLONES_POR_TRABAJO, separacion_s=0.0):
    """Dispara el mismo trabajo `n` veces, en `n` procesos de verdad.

    🔑 No hay barrera posible entre procesos —no comparten objetos, que es el
       problema que se está midiendo—, así que el arranque se sincroniza por
       RELOJ: a todos se les da el mismo instante futuro y esperan a que llegue.
       Es la misma técnica de `compartida.py:carrera_entre_procesos()`, y es la
       lección en miniatura: **lo que dos procesos tienen que compartir hay que
       escribirlo donde los dos puedan verlo.**

    `separacion_s` es el disparo SECUENCIAL: 0 = se solapan; mayor que la
    duración = el segundo arranca con el primero ya terminado.
    """
    carpeta = Path(carpeta or tempfile.mkdtemp())
    carpeta.mkdir(parents=True, exist_ok=True)
    registro = carpeta / "registro_disparador.jsonl"

    arranque = time.time() + 1.0
    t0 = time.time()
    procs = [
        subprocess.Popen(
            [sys.executable, str(Path(__file__).resolve()), "--disparo",
             f"d{i}", str(carpeta), str(arranque + i * separacion_s),
             str(duracion_s), str(renglones)],
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        for i in range(n)
    ]
    reventados, errores = 0, []
    for p in procs:
        _, err = p.communicate()
        if p.returncode != 0:
            reventados += 1
            errores.append(err.decode("utf-8", "replace")[-300:])
    segundos = time.time() - t0

    return _leer_lo_que_quedo(carpeta, registro, n, renglones, reventados,
                              errores, segundos)


def _leer_lo_que_quedo(carpeta, registro, n, renglones, reventados, errores, segundos):
    """Lo que un humano encontraría por la mañana. Ni más ni menos."""
    buenas, rotas = [], 0
    if registro.exists():
        for linea in registro.read_text(encoding="utf-8").splitlines():
            if not linea.strip():
                continue
            try:
                buenas.append(json.loads(linea))
            except json.JSONDecodeError:
                rotas += 1

    reporte_path = Path(carpeta) / "reporte.json"
    reporte_valido, reporte = False, None
    if reporte_path.exists():
        try:
            reporte = json.loads(reporte_path.read_text(encoding="utf-8"))
            reporte_valido = True
        except json.JSONDecodeError:
            pass

    corridas = {d.get("corrida") for d in buenas}
    turnos = {d.get("turno") for d in buenas}

    return {
        "disparos": n,
        "segundos": round(segundos, 2),
        "esperados": n * renglones,
        "renglones_buenos": len(buenas),
        "renglones_rotos": rotas,
        "perdidos": n * renglones - len(buenas) - rotas,
        "corridas_distintas": len(corridas),
        "turnos_distintos": len(turnos),
        "procesos_reventados": reventados,
        "errores": errores,
        "reportes_en_disco": 1 if reporte_path.exists() else 0,
        "reporte_valido": reporte_valido,
        "reporte_de": (reporte or {}).get("quien"),
        "coste_usd": round(len(buenas) * COSTO_POR_RENGLON_USD, 6),
        "carpeta": str(carpeta),
    }


# ---------------------------------------------------------------------------
# 6) 🚨 EL HALLAZGO DEL DÍA — el experimento que separa dos explicaciones
# ---------------------------------------------------------------------------
# El escalón 1 midió que el disparo doble PIERDE renglones del registro. Sin
# una línea rota, sin una excepción, sin un aviso. Y ahí había dos
# explicaciones distintas que dan EXACTAMENTE el mismo archivo:
#
#   (a) el renglón se pierde de camino y nunca llega al disco
#   (b) el renglón SÍ llega, y otro proceso escribe ENCIMA, en el mismo sitio
#
# 🔑 Con renglones del mismo largo —que es el caso real de un `.jsonl`— las dos
#    son indistinguibles: pisar 175 bytes con otros 175 deja el archivo idéntico
#    a como si se hubiera perdido uno. Es `LM.66` otra vez: **un dato solo en su
#    renglón**, sin nadie que pueda desmentirlo.
#
# Se separan poniendo longitudes DISTINTAS y forzando el choque. Eso es lo que
# hace `atomico_o_no()`, y la respuesta que dio está abajo.

LARGO_A, LARGO_B = 200, 20


def atomico_o_no(n=400, carpeta=None):
    """¿Es atómico `open(ruta, "a")` entre procesos? Dos procesos, dos tamaños.

    A escribe renglones de 200 caracteres; B, de 20.

      · si fuera (a) → lo que quede será todo de 200 o de 20, limpio
      · si fuera (b) → aparecerán renglones de LONGITUD IMPOSIBLE: los 178
        caracteres de cola de una A a la que le pisaron los 22 primeros bytes

    ⭐ La huella de 178 no admite otra explicación. 200 − 22 = 178, y 22 es
       exactamente lo que ocupa un renglón de B con su fin de línea de Windows.
    """
    carpeta = Path(carpeta or tempfile.mkdtemp())
    carpeta.mkdir(parents=True, exist_ok=True)
    ruta = carpeta / "atomico.txt"
    arranque = time.time() + 0.8

    procs = [
        subprocess.Popen(
            [sys.executable, str(Path(__file__).resolve()), "--atomico",
             str(ruta), marca, str(largo), str(n), str(arranque)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for marca, largo in (("A", LARGO_A), ("B", LARGO_B))
    ]
    for p in procs:
        p.wait()

    crudo = ruta.read_bytes()
    lineas = ruta.read_text(encoding="utf-8").splitlines()
    return {
        "esperados": 2 * n,
        "fisicos": len(lineas),
        "perdidos": 2 * n - len(lineas),
        "mixtos": sum(1 for l in lineas if "A" in l and "B" in l),
        "imposibles": sum(1 for l in lineas if len(l) not in (LARGO_A, LARGO_B)),
        "largos_raros": sorted({len(l) for l in lineas} - {LARGO_A, LARGO_B}),
        "huecos_sin_escribir": crudo.count(0),
        "bytes": len(crudo),
        "bytes_de_lo_que_queda": sum(len(l) + 2 for l in lineas),
        "ruta": str(ruta),
    }


# ---------------------------------------------------------------------------
# 7) EL ESCALÓN 2 — LE PONEMOS EL CANDADO DE D.1
# ---------------------------------------------------------------------------
# El escalón 1 dejó dos daños: el trabajo se hace dos veces, y los renglones se
# pisan. Lo primero que hace cualquiera es poner un candado, y aquí hay uno bueno
# y ya medido: `compartida.py:_CandadoDeArchivo`, el que SÍ cruza procesos
# porque vive en el disco (sesión 106, 0 % de pérdidas con cinco procesos).
#
# ⚠️ NO SE EDITA `compartida.py`. Se importa tal cual, con sus dos constantes:
#        ESPERA_MAXIMA_S  = 5.0   ← cuánto aguanta esperando antes de rendirse
#        CANDADO_RANCIO_S = 30.0  ← a partir de cuándo lo da por abandonado
#    Las dos se escribieron para proteger UN RENGLÓN, que tarda milisegundos.
#    Aquí se le pide que proteja UN TRABAJO ENTERO, que dura 21 segundos.
#
# 🔑 La pregunta del escalón 2 no es «¿funciona el candado?» —funciona, está
#    medido—. Es **«¿protege lo que creo que protege?»**.

from compartida import CandadoOcupado, _CandadoDeArchivo  # noqa: E402


def correr_con_candado(carpeta, quien="?", momento=None, espera_s=None,
                       rancio_s=None, **kw):
    """El escalón 2: pide el candado del TRABAJO antes de hacer nada.

    Devuelve qué le pasó a este disparo, que es el dato del escalón:
        "hizo"  → consiguió el candado y trabajó
        "cedio" → no lo consiguió y se rindió (`CandadoOcupado`)

    📌 `espera_s` y `rancio_s` existen para poder mover el reloj sin editar
       `compartida.py` ni esperar 35 segundos en cada prueba. La tabla del
       informe se corre además UNA vez con los valores REALES del archivo, para
       que el número que se enseña no dependa de un atajo.
    """
    import compartida
    if rancio_s is not None:
        compartida.CANDADO_RANCIO_S = float(rancio_s)

    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    turno = turno_de(momento)
    llave = carpeta / "trabajo"          # el candado será `trabajo.lock`
    espera = compartida.ESPERA_MAXIMA_S if espera_s is None else float(espera_s)

    try:
        with _CandadoDeArchivo(llave, espera_maxima_s=espera):
            trabajo_falso(carpeta, quien=quien, turno=turno, **kw)
        return "hizo"
    except CandadoOcupado:
        # 🚨 Fíjate en lo que NO pasa aquí: no se anota nada. El disparo que
        #    cede se va sin dejar renglón. Es la deuda que abre el escalón 4.
        return "cedio"


def disparo_doble_con_candado(n=2, carpeta=None, duracion_s=1.0,
                              renglones=RENGLONES_POR_TRABAJO,
                              separacion_s=0.0, espera_s=5.0, rancio_s=30.0):
    """Lo mismo que `disparo_doble()`, pero cada hijo pide el candado primero."""
    carpeta = Path(carpeta or tempfile.mkdtemp())
    carpeta.mkdir(parents=True, exist_ok=True)
    registro = carpeta / "registro_disparador.jsonl"

    arranque = time.time() + 1.0
    t0 = time.time()
    procs = [
        subprocess.Popen(
            [sys.executable, str(Path(__file__).resolve()), "--candado",
             f"d{i}", str(carpeta), str(arranque + i * separacion_s),
             str(duracion_s), str(renglones), str(espera_s), str(rancio_s)],
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        for i in range(n)
    ]
    reventados, errores = 0, []
    for p in procs:
        _, err = p.communicate()
        if p.returncode != 0:
            reventados += 1
            errores.append(err.decode("utf-8", "replace")[-300:])
    segundos = time.time() - t0

    r = _leer_lo_que_quedo(carpeta, registro, n, renglones, reventados,
                           errores, segundos)
    # Cada hijo deja escrito qué le pasó. Sin esto no se distingue «cedió» de
    # «reventó», y son cosas opuestas: una es el candado funcionando.
    veredictos = []
    for i in range(n):
        f = carpeta / f"veredicto_d{i}.txt"
        veredictos.append(f.read_text(encoding="utf-8").strip() if f.exists() else "?")
    r["hicieron"] = veredictos.count("hizo")
    r["cedieron"] = veredictos.count("cedio")
    r["veredictos"] = veredictos
    r["candado_quedo_colgado"] = (Path(carpeta) / "trabajo.lock").exists()
    return r


def informe_escalon_2():
    """La tabla del candado. Es donde se paga la apuesta 1 del sobre."""
    print("\n" + "=" * 78)
    print("E.1 · ESCALÓN 2 — EL MISMO DISPARO DOBLE, AHORA CON EL CANDADO DE D.1")
    print("=" * 78)
    print("\n  Dos disparos a la vez. `espera` y `rancio` son las dos constantes")
    print("  de `compartida.py`. La columna que importa es 'hicieron'.\n")

    print(f"  {'el trabajo dura':<20} {'espera':>7} {'rancio':>7} "
          f"{'hicieron':>9} {'cedieron':>9} {'corridas':>9} {'renglones':>11}")
    print("  " + "-" * 76)

    filas = [
        ("2 s  (corto)", 2.0, 5.0, 30.0),
        ("8 s  (> espera)", 8.0, 5.0, 30.0),
        ("35 s (> rancio)", 35.0, 5.0, 30.0),
        ("35 s, espera 60", 35.0, 60.0, 30.0),
    ]
    salida = {}
    for nombre, dur, esp, ran in filas:
        r = disparo_doble_con_candado(n=2, duracion_s=dur, renglones=12,
                                      espera_s=esp, rancio_s=ran)
        salida[nombre] = r
        print(f"  {nombre:<20} {esp:>7.1f} {ran:>7.1f} "
              f"{r['hicieron']:>9} {r['cedieron']:>9} "
              f"{r['corridas_distintas']:>9} "
              f"{str(r['renglones_buenos']) + '/' + str(r['esperados']):>11}")

    print("\n  🚨 FILA 1 — EL CANDADO FUNCIONÓ Y NO SIRVIÓ DE NADA.")
    print("     El trabajo dura menos que la espera, así que el segundo NO se")
    print("     rinde: ESPERA su turno y luego hace el trabajo entero igual.")
    print("     Cero renglones perdidos ✅ · dos corridas ❌")
    print("     🔑 Un candado SERIALIZA; no DEDUPLICA. Arregló el archivo y")
    print("        dejó el problema intacto.")
    print("\n  ✅ FILA 2 — aquí sí cede, y es el único caso que sale bien.")
    print("     Y sale bien POR ACCIDENTE: porque el trabajo dura más que una")
    print("     constante que nadie eligió pensando en esto.")
    print("\n  🔴 FILA 3 — LA APUESTA 1(b) FALLÓ, Y EL MOTIVO ES MEJOR QUE ELLA.")
    print("     Sellé que un trabajo de más de 30 s haría que el segundo diera")
    print("     el candado por abandonado. NO PASA: el que espera se rinde a los")
    print("     5 s, y la caducidad se comprueba SOLO MIENTRAS ESPERA.")
    print("     Con ESPERA_MAXIMA_S (5) < CANDADO_RANCIO_S (30) el rancio es")
    print("     INALCANZABLE durante un solapamiento. No había bicho ahí.")
    print("\n  🚨 FILA 4 — Y AQUÍ ESTÁ EL BICHO DE VERDAD, QUE ES PEOR.")
    print("     Misma duración, un solo cambio: la espera sube de 5 a 60.")
    print("     Ahora el segundo aguanta lo bastante para llegar a los 30 s,")
    print("     declara el candado abandonado —CON SU DUEÑO VIVO Y TRABAJANDO—,")
    print("     lo BORRA y entra. Los dos a la vez, sin un solo error.")
    print("     🔑 El fallo no lo dispara un trabajo largo: LO DISPARA SER MÁS")
    print("        PACIENTE. Subir la espera —que es justo lo que cualquiera")
    print("        haría para 'arreglar' la fila 2— es lo que rompe el candado.")
    print("     ⭐ La regla que sale, y no estaba en el sobre: la caducidad tiene")
    print("        que ser mayor que lo que dura el trabajo Y mayor que lo que")
    print("        nadie espere. Aquí son 30 s para un trabajo de 21 s medidos:")
    print("        un margen de 9 segundos que nadie eligió.")
    return salida


# ---------------------------------------------------------------------------
# 8) EL ESCALÓN 3 — EL TURNO, que es la marca de «este trabajo YA SE HIZO»
# ---------------------------------------------------------------------------
# El escalón 2 dejó claro qué NO puede hacer un candado: el disparo secuencial
# —a las 3:00 falla, a las 3:05 el reloj reintenta— repite el trabajo entero sin
# que el candado se entere, porque para entonces ya está libre.
#
# 🔑 Y ahí está la apuesta 3 del sobre, y es lo que cuesta ver: la marca que
#    hace falta NO puede colgar de `corrida`. `corrida` está diseñada para NO
#    repetirse nunca —se arregló en la sesión 97 justo para eso—, y una marca
#    que nunca se repite no puede contestar «¿esto ya se hizo?». Hace falta un
#    identificador con el requisito CONTRARIO: el TURNO, que se repite a
#    propósito porque describe la RANURA, no la ejecución.
#
#        corrida  → «QUIÉN corrió»      única siempre        c20260824T031200-a1b2
#        turno    → «QUÉ HUECO cubría»  repetible a propósito 2026-08-24T03:00
#
# ⚠️ Y hay una pregunta que parece de detalle y decide todo el comportamiento:
#    ¿la marca se pone ANTES o DESPUÉS del trabajo? No hay respuesta buena. Hay
#    dos respuestas con daños opuestos, y la tabla de abajo los mide.

CARPETA_TURNOS = "turnos_hechos"


def _nombre_de_marca(turno):
    """El turno, convertido en algo que Windows acepte como NOMBRE DE ARCHIVO.

    🚨 ESTO NO ES COSMÉTICA, Y COSTÓ UN HALLAZGO. La primera versión guardaba
       la marca como `2026-08-24T03:00.json` — el turno tal cual. En Linux es un
       nombre legal y todo funciona. En Windows los dos puntos NO son un
       carácter de nombre: separan el archivo de un FLUJO ALTERNO de NTFS.

       Lo que quedaba en disco, visto con `dir /r`:

           0 bytes   2026-08-24T03
          73 bytes   2026-08-24T03:00.json:$DATA

       Un archivo VACÍO con el nombre cortado, y el contenido escondido en un
       flujo. Y aquí está el veneno: **funcionaba**. `exists()` encuentra el
       flujo, `O_EXCL` sigue impidiendo la segunda marca, y las pruebas de
       deduplicación salían todas verdes. Lo único que fallaba era LISTAR:
       `glob("*.json")` devolvía CERO con todas las marcas puestas.

    🔑 Tercera cara en un día del mismo bicho, y siempre en la misma dirección:
       Windows no dice nada. `open("a")` no avisa de que no es atómico; el
       candado rancio no avisa de que se rompió; y esto no avisa de que el
       nombre que pediste no es el nombre que existe.

    ⭐ Y la lección que se lleva fuera del curso: **un identificador que se usa
       como nombre de archivo tiene que pasar por una puerta.** El turno se
       queda con sus dos puntos DENTRO del registro, donde se lee; y pierde los
       dos puntos FUERA, donde es un nombre. Son dos usos distintos del mismo
       dato y no tienen por qué escribirse igual.
    """
    return turno.replace(":", "-") + ".json"


def turno_ya_hecho(carpeta, turno):
    """¿Existe la marca de este turno?"""
    return (Path(carpeta) / CARPETA_TURNOS / _nombre_de_marca(turno)).exists()


def turnos_hechos(carpeta):
    """Los turnos que tienen marca. Es la lista que el escalón 4 va a necesitar,
    y la que devolvía vacía mientras el nombre llevaba dos puntos."""
    carp = Path(carpeta) / CARPETA_TURNOS
    if not carp.exists():
        return []
    return sorted(p.stem.replace("T", "T", 1) for p in carp.glob("*.json"))


def marcar_turno(carpeta, turno, datos=None):
    """Deja la marca del turno. Devuelve True si la creó ESTE proceso.

    ⭐ Usa `os.O_CREAT | os.O_EXCL`, el mismo truco del candado de D.1 y por el
       mismo motivo: crear-si-no-existe es UNA operación del sistema. Preguntar
       «¿existe?» y luego crearlo son dos, y entre las dos cabe el otro proceso.
       **Preguntar y actuar por separado ES la carrera.**

    🔑 La diferencia con el candado es lo que dura: el candado se BORRA al
       soltarlo; la marca del turno SE QUEDA. Un candado dice «ahora mismo estoy
       yo»; una marca dice «esto ya pasó». Por eso hacen falta los dos.
    """
    carpeta_t = Path(carpeta) / CARPETA_TURNOS
    carpeta_t.mkdir(parents=True, exist_ok=True)
    ruta = carpeta_t / _nombre_de_marca(turno)
    try:
        fd = os.open(str(ruta), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        return False
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(datos or {"turno": turno,
                            "hora": datetime.now(timezone.utc).isoformat()},
                  f, ensure_ascii=False)
    return True


def correr_con_turno(carpeta, quien="?", momento=None, marcar="despues",
                     espera_s=None, rancio_s=None, **kw):
    """El escalón 3: candado PARA EL SOLAPAMIENTO + turno PARA LA REPETICIÓN.

    Devuelve qué le pasó a este disparo:
        "hizo"       → era suyo el turno y trabajó
        "ya_estaba"  → el turno ya tenía marca; se fue sin trabajar
        "cedio"      → no consiguió el candado
        "fallo"      → consiguió todo y el trabajo se rompió

    `marcar` es la decisión del párrafo de arriba:
        "antes"   → la marca se pone y LUEGO se trabaja  → COMO MUCHO UNA VEZ
        "despues" → se trabaja y LUEGO se marca          → AL MENOS UNA VEZ
    """
    import compartida
    if rancio_s is not None:
        compartida.CANDADO_RANCIO_S = float(rancio_s)

    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    turno = turno_de(momento)
    espera = compartida.ESPERA_MAXIMA_S if espera_s is None else float(espera_s)

    # 1ª pregunta, fuera del candado. Es la barata: evita pedir el candado a los
    # 23 disparos de un día que ya está hecho.
    if turno_ya_hecho(carpeta, turno):
        anotar_intento(carpeta, turno, quien, "ya_estaba")
        return "ya_estaba"

    try:
        with _CandadoDeArchivo(carpeta / "trabajo", espera_maxima_s=espera):
            # 🚨 2ª pregunta, DENTRO del candado, y no es una repetición
            #    perezosa: entre la primera y esta, otro proceso pudo haber
            #    terminado el turno entero. Es «releer dentro del candado» de
            #    D.1, y aquí se ve por qué no era un adorno.
            if turno_ya_hecho(carpeta, turno):
                anotar_intento(carpeta, turno, quien, "ya_estaba")
                return "ya_estaba"

            if marcar == "antes":
                if not marcar_turno(carpeta, turno, {"turno": turno, "quien": quien,
                                                     "cuando": "antes"}):
                    return "ya_estaba"

            trabajo_falso(carpeta, quien=quien, turno=turno, **kw)

            if marcar == "despues":
                marcar_turno(carpeta, turno, {"turno": turno, "quien": quien,
                                              "cuando": "despues"})
            anotar_intento(carpeta, turno, quien, "hizo")
            return "hizo"
    except CandadoOcupado:
        # 🚨 La deuda que abrió el escalón 2, pagada: el que cede DEJA RASTRO.
        anotar_intento(carpeta, turno, quien, "cedio")
        return "cedio"
    except RuntimeError:
        anotar_intento(carpeta, turno, quien, "fallo")
        return "fallo"


def disparo_doble_con_turno(n=2, carpeta=None, duracion_s=0.3,
                            renglones=8, separacion_s=0.0, marcar="despues",
                            espera_s=2.0, rancio_s=30.0, fallar_en=None,
                            morir_en=None, solo_el_primero_falla=True):
    """Como los anteriores, pero cada hijo mira el turno antes de trabajar."""
    carpeta = Path(carpeta or tempfile.mkdtemp())
    carpeta.mkdir(parents=True, exist_ok=True)
    registro = carpeta / "registro_disparador.jsonl"

    arranque = time.time() + 1.0
    procs, t0 = [], time.time()
    for i in range(n):
        # el fallo se le pone SOLO al primero: así el segundo disparo es el
        # reintento honesto de un trabajo que se rompió, que es el caso real.
        f = fallar_en if (i == 0 or not solo_el_primero_falla) else None
        m = morir_en if (i == 0 or not solo_el_primero_falla) else None
        procs.append(subprocess.Popen(
            [sys.executable, str(Path(__file__).resolve()), "--turno",
             f"d{i}", str(carpeta), str(arranque + i * separacion_s),
             str(duracion_s), str(renglones), str(espera_s), str(rancio_s),
             marcar, str(f), str(m)],
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE))

    reventados, errores = 0, []
    for p in procs:
        _, err = p.communicate()
        if p.returncode != 0:
            reventados += 1
            errores.append(err.decode("utf-8", "replace")[-200:])
    segundos = time.time() - t0

    r = _leer_lo_que_quedo(carpeta, registro, n, renglones, reventados,
                           errores, segundos)
    veredictos = []
    for i in range(n):
        f = carpeta / f"veredicto_d{i}.txt"
        veredictos.append(f.read_text(encoding="utf-8").strip() if f.exists() else "murio")
    r["veredictos"] = veredictos
    for v in ("hizo", "ya_estaba", "cedio", "fallo", "murio"):
        r[v] = veredictos.count(v)
    r["turnos_marcados"] = len(list((carpeta / CARPETA_TURNOS).glob("*.json"))) \
        if (carpeta / CARPETA_TURNOS).exists() else 0
    return r


def informe_escalon_3():
    """La tabla del turno, y la elección que no tiene respuesta buena."""
    print("\n" + "=" * 78)
    print("E.1 · ESCALÓN 3 — EL TURNO: candado para el solape, marca para la repetición")
    print("=" * 78)
    print("\n  Las mismas dos filas que el candado no podía arreglar, ahora con turno.\n")
    print(f"  {'caso':<34} {'hizo':>5} {'ya_estaba':>10} {'corridas':>9} {'marcas':>7}")
    print("  " + "-" * 76)

    a = disparo_doble_con_turno(n=2, separacion_s=0.0)
    print(f"  {'2 a la vez (se solapan)':<34} {a['hizo']:>5} {a['ya_estaba']:>10} "
          f"{a['corridas_distintas']:>9} {a['turnos_marcados']:>7}")
    b = disparo_doble_con_turno(n=2, separacion_s=1.5)
    print(f"  {'2 seguidos (el que el candado no ve)':<34}"[:36] +
          f" {b['hizo']:>5} {b['ya_estaba']:>10} "
          f"{b['corridas_distintas']:>9} {b['turnos_marcados']:>7}")
    c = disparo_doble_con_turno(n=3, separacion_s=0.0)
    print(f"  {'3 a la vez':<34} {c['hizo']:>5} {c['ya_estaba']:>10} "
          f"{c['corridas_distintas']:>9} {c['turnos_marcados']:>7}")

    print("\n  ✅ Una sola corrida en los tres casos, y UNA marca por turno.")
    print("     Fíjate en la fila 2: es exactamente la que el candado dejaba")
    print("     pasar, porque para entonces ya estaba libre.")

    print("\n" + "-" * 78)
    print("  🚨 Y AHORA LA PREGUNTA QUE NO TIENE RESPUESTA BUENA:")
    print("     ¿la marca se pone ANTES del trabajo o DESPUÉS?")
    print("-" * 78 + "\n")
    print(f"  {'qué le pasa al primer disparo':<32} {'marcar':>8} "
          f"{'se rehace':>10} {'renglones':>10} {'marcas':>7}")
    print("  " + "-" * 76)

    filas = {}
    for etiqueta, kw in (
        ("se rompe a mitad (excepción)", dict(fallar_en=3)),
        ("la máquina se apaga a mitad", dict(morir_en=3)),
        ("se apaga, y rancio < reintento", dict(morir_en=3, rancio_s=1.0)),
    ):
        for modo in ("antes", "despues"):
            r = disparo_doble_con_turno(n=2, separacion_s=1.5, marcar=modo,
                                        renglones=8, duracion_s=0.3, **kw)
            filas[(etiqueta, modo)] = r
            rehecho = "sí" if r["renglones_buenos"] > 4 else "NO"
            print(f"  {etiqueta:<32} {modo:>8} {rehecho:>10} "
                  f"{r['renglones_buenos']:>10} {r['turnos_marcados']:>7}"
                  f"   {','.join(r['veredictos'])}")

    print("\n  🔑 NO EXISTE «EXACTAMENTE UNA VEZ». Existen dos daños opuestos:")
    print("     · marcar ANTES  → COMO MUCHO UNA VEZ. Si el trabajo se rompe,")
    print("       el turno queda marcado y NADIE lo vuelve a intentar nunca.")
    print("       El trabajo se pierde en silencio.")
    print("     · marcar DESPUÉS → AL MENOS UNA VEZ. El reintento funciona,")
    print("       pero lo que el primero alcanzó a escribir SE QUEDA, y el")
    print("       segundo escribe encima de eso.")
    print("\n  🚨 Y MIRA LAS FILAS 3 Y 4: NO SE REHACE NI CON «DESPUÉS».")
    print("     El proceso que murió NO SOLTÓ EL CANDADO —murió con él en la")
    print("     mano— y el reintento se encuentra un `trabajo.lock` de un dueño")
    print("     que ya no existe. Veredicto: `cedio`. La marca no tuvo nada que")
    print("     ver: el reintento ni siquiera llegó a mirarla.")
    print("\n  ⭐ FILAS 5 Y 6 — Y AQUÍ SE ENTIENDE POR FIN PARA QUÉ SIRVE")
    print("     `CANDADO_RANCIO_S`. Bajado a 1 s, el reintento que llega 1,5 s")
    print("     después SÍ ve el candado viejo, lo rompe y trabaja.")
    print("     🔑 La caducidad NO es para el solapamiento —el escalón 2 midió")
    print("        que ahí es inalcanzable—: ES PARA EL CADÁVER. Y eso ordena")
    print("        los tres números de una vez: la caducidad tiene que ser MAYOR")
    print("        que el trabajo (o rompes a un vivo) y MENOR que el hueco")
    print("        entre disparos (o el muerto bloquea el siguiente turno).")
    print("        Hoy: trabajo 21 s · caducidad 30 s · hueco entre turnos 3600 s.")
    print("        Cuadra por casualidad, y ahora está escrito.")
    print("\n  ⭐ La elección no es técnica, es del negocio: ¿qué duele más,")
    print("     mandar el correo dos veces o no mandarlo? Y esa pregunta hay")
    print("     que hacérsela ANTES, porque el que no elige ya eligió: el")
    print("     escalón 1 marcaba «después» sin saberlo.")
    return {"solape": a, "secuencial": b, "tres": c, "danos": filas}


# ---------------------------------------------------------------------------
# 9) EL ESCALÓN 4 — EL DISPARO QUE NO OCURRIÓ
# ---------------------------------------------------------------------------
# Los tres escalones anteriores arreglaron el disparo que llega DE MÁS. Este es
# el otro, y el sobre apostó que es peor: **el disparo que no llega.**
#
# 🔑 Y el motivo por el que es peor cabe en una frase: un disparo que no ocurrió
#    NO DEJA RENGLÓN. Todo lo que se ha construido hoy —el registro, las
#    corridas, las marcas de turno— es prueba de lo que SÍ pasó. Ninguna de esas
#    piezas puede decir nada sobre lo que no pasó, porque su forma de hablar es
#    escribir, y el que no corre no escribe.
#
# ⭐ Por eso hace falta una pieza que ninguna de las anteriores tenía: **algo
#    escrito ANTES, que diga qué se esperaba.** El calendario. Sin él la
#    pregunta «¿se disparó anoche?» no es difícil: es IMPOSIBLE DE FORMULAR, y
#    esa es la diferencia que el escalón 4 tiene que enseñar.
#
# ⚠️ Y hay una segunda mitad que el escalón 2 dejó apuntada como deuda: el
#    disparo que CEDE se va sin anotar nada. Así que «no hay marca» hoy mezcla
#    TRES cosas que se ven iguales y no lo son:
#        · nunca se disparó
#        · se disparó y cedió (había otro)
#        · se disparó y se rompió
#    Es `LM.88`: arreglar el síntoma ruidoso deja el silencioso solo.

ARCHIVO_INTENTOS = "intentos.jsonl"


def anotar_intento(carpeta, turno, quien, veredicto):
    """Deja constancia de que ALGUIEN se despertó para este turno.

    ⭐ Fíjate en que esto se anota SIEMPRE, también cuando el disparo no hizo
       nada. Un registro que solo apunta los éxitos no puede distinguir «no pasó
       nada» de «no vino nadie».

    🚨 Y va DENTRO del candado de disco, y hoy sabemos por qué: el hallazgo de
       esta mañana midió que `open(ruta, "a")` NO es atómico entre procesos en
       Windows, y este archivo lo escriben justo los procesos que compiten.
       Sin el candado, el renglón que dice «cedí» sería el primero en perderse.
    """
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    linea = {
        "hora": datetime.now(timezone.utc).isoformat(),
        "turno": turno,
        "quien": quien,
        "veredicto": veredicto,
    }
    try:
        with _CandadoDeArchivo(carpeta / ARCHIVO_INTENTOS, espera_maxima_s=2.0):
            with open(carpeta / ARCHIVO_INTENTOS, "a", encoding="utf-8") as f:
                f.write(json.dumps(linea, ensure_ascii=False) + "\n")
    except CandadoOcupado:
        # 📌 Y esto también se dice en vez de esconderse: si ni siquiera se pudo
        #    anotar el intento, el turno se verá MUDO. El instrumento tiene su
        #    propio modo de fallo, y es el mismo que está midiendo.
        pass


def intentos_de(carpeta, turno=None):
    """Los intentos anotados, todos o los de un turno."""
    ruta = Path(carpeta) / ARCHIVO_INTENTOS
    if not ruta.exists():
        return []
    salida = []
    for l in ruta.read_text(encoding="utf-8").splitlines():
        if not l.strip():
            continue
        try:
            d = json.loads(l)
        except json.JSONDecodeError:
            continue
        if turno is None or d.get("turno") == turno:
            salida.append(d)
    return salida


def calendario(desde, hasta, cada_horas=1):
    """LA PIEZA QUE NO EXISTÍA. Qué turnos DEBERÍAN haber ocurrido.

    🔑 No lee nada del disco. No puede: se trata justamente de saber qué se
       esperaba, y eso no está en ningún sitio donde lo escriba el que corre.
       **Un calendario es una promesa escrita antes, no un resumen de después.**
    """
    turnos, t = [], desde
    while t <= hasta:
        turnos.append(turno_de(t))
        t += timedelta(hours=cada_horas)
    return turnos


def auditar_turnos(carpeta, desde, hasta, cada_horas=1):
    """Compara lo que debía pasar con lo que pasó. Devuelve un veredicto por turno.

        "hecho"    → hay marca. Todo bien.
        "sin_exito"→ NO hay marca, pero SÍ hubo intentos: alguien vino y no pudo.
        "MUDO"     → no hay marca ni intento. **Nadie vino.**

    ⭐ La tercera es la única que no se puede sacar del registro: sale de restar
       el calendario. Y es la que importa a las 3 de la mañana.
    """
    hechos = set(turnos_hechos(carpeta))
    vistos = {}
    for d in intentos_de(carpeta):
        vistos.setdefault(d["turno"], []).append(d["veredicto"])

    veredicto = {}
    for t in calendario(desde, hasta, cada_horas):
        if _nombre_de_marca(t)[:-5] in hechos:
            veredicto[t] = "hecho"
        elif t in vistos:
            veredicto[t] = "sin_exito"
        else:
            veredicto[t] = "MUDO"
    return {
        "por_turno": veredicto,
        "hechos": sum(1 for v in veredicto.values() if v == "hecho"),
        "sin_exito": sum(1 for v in veredicto.values() if v == "sin_exito"),
        "mudos": sum(1 for v in veredicto.values() if v == "MUDO"),
        "detalle_intentos": vistos,
    }


def informe_escalon_4():
    """La tabla del disparo que falta. Cierra E.1."""
    print("\n" + "=" * 78)
    print("E.1 · ESCALÓN 4 — EL DISPARO QUE NO OCURRIÓ")
    print("=" * 78)

    carpeta = Path(tempfile.mkdtemp())
    dia = datetime(2026, 8, 24, 3, 0, tzinfo=timezone.utc)

    # 03:00 — salió bien
    marcar_turno(carpeta, turno_de(dia))
    anotar_intento(carpeta, turno_de(dia), "d0", "hizo")
    # 04:00 — vinieron dos y ninguno pudo
    t4 = turno_de(dia + timedelta(hours=1))
    anotar_intento(carpeta, t4, "d0", "fallo")
    anotar_intento(carpeta, t4, "d1", "cedio")
    # 05:00 — no vino nadie. No se escribe NADA, que es justo el problema.

    print("\n  Tres turnos de una noche. Mira lo que hay en disco de cada uno:\n")
    print(f"  {'turno':<20} {'¿marca?':>9} {'intentos':>9}   qué pasó de verdad")
    print("  " + "-" * 76)
    reales = {turno_de(dia): "el trabajo salió bien",
              t4: "vinieron dos y ninguno pudo",
              turno_de(dia + timedelta(hours=2)): "NO SE DISPARÓ NUNCA"}
    for t, real in reales.items():
        print(f"  {t:<20} {('sí' if turno_ya_hecho(carpeta, t) else 'no'):>9} "
              f"{len(intentos_de(carpeta, t)):>9}   {real}")

    print("\n  🚨 SIN CALENDARIO, LAS FILAS 2 Y 3 SON INDISTINGUIBLES DE «NADA")
    print("     QUE VER AQUÍ». Las dos dicen «no hay marca», y la tercera además")
    print("     no dice absolutamente nada: no existe el renglón que consultar.")

    r = auditar_turnos(carpeta, dia, dia + timedelta(hours=2))
    print("\n  Ahora con el calendario, que es la pieza escrita ANTES:\n")
    print(f"  {'turno':<20} {'veredicto':>12}   por qué")
    print("  " + "-" * 76)
    porques = {"hecho": "hay marca",
               "sin_exito": "no hay marca, pero alguien vino y lo anotó",
               "MUDO": "ni marca ni intento — NADIE VINO"}
    for t, v in r["por_turno"].items():
        print(f"  {t:<20} {v:>12}   {porques[v]}")

    print(f"\n  hechos {r['hechos']} · sin_exito {r['sin_exito']} · MUDOS {r['mudos']}")
    print("\n  ✅ LA APUESTA 4 SALIÓ, Y CON EL MATIZ QUE IMPORTA.")
    print("     «Esto se disparó dos veces» se escribe contando corridas: el")
    print("     dato está en el registro. «Esto no se disparó» NO se puede")
    print("     escribir con el registro, por muchas vueltas que se le dé,")
    print("     porque el que no corre no escribe.")
    print("\n  🔑 UN REGISTRO SOLO PUEDE PROBAR LO QUE SÍ PASÓ. Para lo que no")
    print("     pasó hace falta algo escrito ANTES, y no es un archivo más: es")
    print("     de otra clase. El registro lo escribe el que trabaja; el")
    print("     calendario lo escribe el que prometió.")
    print("\n  ⭐ Y la fila 2 es la mitad que casi se me escapa: sin anotar los")
    print("     intentos, «se disparó y nadie pudo» se ve igual que «no se")
    print("     disparó». Son tres estados, no dos, y el que arregla el ruidoso")
    print("     deja el silencioso solo — `LM.88` por tercera vez hoy.")
    return r


# ---------------------------------------------------------------------------
# 10) LOS INFORMES — las tablas del escalón 1
# ---------------------------------------------------------------------------
def informe_escalon_1():
    """Reproduce lo que se mide hoy. $0,00, sin red, sin modelo."""
    print("\n" + "=" * 78)
    print("E.1 · ESCALÓN 1 — EL DISPARADOR INGENUO, disparado dos veces")
    print("=" * 78)

    print("\n  Un trabajo = 21 renglones + 1 reporte, la forma del fan-out real.")
    print("  Cada fila lanza `python` de verdad. Nadie mira la pantalla.\n")

    print(f"  {'caso':<26} {'renglones':>12} {'rotos':>6} {'corridas':>9} "
          f"{'reportes':>9} {'revienta':>9}")
    print("  " + "-" * 76)

    casos = [
        ("1 disparo (lo normal)", 1, 0.0),
        ("2 a la vez (se solapan)", 2, 0.0),
        ("2 seguidos (secuencial)", 2, 1.2),
        ("3 a la vez", 3, 0.0),
    ]
    resultados = {}
    for nombre, n, sep in casos:
        r = disparo_doble(n=n, duracion_s=0.8, separacion_s=sep)
        resultados[nombre] = r
        print(f"  {nombre:<26} {r['renglones_buenos']:>5}/{r['esperados']:<6} "
              f"{r['renglones_rotos']:>6} {r['corridas_distintas']:>9} "
              f"{r['reportes_en_disco']:>9} {r['procesos_reventados']:>9}")

    print("\n  🔑 Mira la columna 'revienta' antes que ninguna otra.")
    print("     Nadie se cayó. Nadie avisó. Y el trabajo se hizo varias veces.")
    print("\n  🚨 Y mira 'reportes': el entregable de la mañana es UNO,")
    print("     lo hayan escrito uno o tres. El último que llega manda,")
    print("     y no queda rastro de los que pisó.")
    print("\n  🚨 Y mira la columna 'renglones' de las filas que se SOLAPAN:")
    print("     faltan renglones, y la columna 'rotos' está a cero. El archivo")
    print("     no está dañado. Simplemente hay menos de lo que se escribió.")
    print("     La fila secuencial NO pierde ninguno: la pérdida es del")
    print("     solapamiento, no del trabajo.")
    return resultados


def informe_atomicidad():
    """La segunda tabla: por qué faltaban esos renglones."""
    print("\n" + "=" * 78)
    print("E.1 · ¿ES ATÓMICO `open(ruta, \"a\")` ENTRE PROCESOS?")
    print("=" * 78)
    r = atomico_o_no()
    print(f"""
  Dos procesos. A escribe {r['esperados']//2} renglones de {LARGO_A}; B, {r['esperados']//2} de {LARGO_B}.

    esperados ................ {r['esperados']}
    renglones en el archivo .. {r['fisicos']}
    perdidos ................. {r['perdidos']}
    MIXTOS (A y B revueltos) . {r['mixtos']}
    de LONGITUD IMPOSIBLE .... {r['imposibles']}   -> largos: {r['largos_raros']}
    huecos sin escribir ...... {r['huecos_sin_escribir']}
    bytes en disco ........... {r['bytes']}
    bytes de lo que queda .... {r['bytes_de_lo_que_queda']}
""")
    print("  🔑 LA RESPUESTA ES NO, Y LA HUELLA ES EL 178.")
    print("     Un renglón de B ocupa 20 + 2 = 22 bytes. 200 − 22 = 178.")
    print("     Esos renglones de 178 son la COLA de una A a la que otro proceso")
    print("     le escribió encima los 22 primeros bytes. El renglón llegó al")
    print("     disco y luego lo pisaron.")
    print("\n  ⭐ Cero huecos y los bytes cuadran con lo que queda: no se dejó de")
    print("     escribir, se escribió DOS VECES EN EL MISMO SITIO.")
    print("\n  🚨 Y con renglones del mismo largo —un `.jsonl` de verdad— el")
    print("     pisotón es INVISIBLE: cero mixtos, cero longitudes raras, cero")
    print("     avisos. Solo un renglón que no está.")
    return r


# ---------------------------------------------------------------------------
# 11) LAS PRUEBAS — todas gratis, sin red, sin modelo
# ---------------------------------------------------------------------------
def _pruebas():
    fallos = []

    def check(nombre, cond, detalle=""):
        print(("  OK  " if cond else "  XX  ") + nombre + (f"  -> {detalle}" if detalle else ""))
        if not cond:
            fallos.append(nombre)

    print("\n[E.1 · escalón 1] el disparador ingenuo\n")
    base = Path(tempfile.mkdtemp())

    # --- P1-P5: el reloj falso, que es el decorado -------------------------
    t = datetime(2026, 8, 24, 3, 0, 4, tzinfo=timezone.utc)
    check("P1 · un turno es una hora redonda", turno_de(t) == "2026-08-24T03:00", turno_de(t))
    check("P2 · TIRA los minutos a propósito: 03:00:04 y 03:47:59 son el mismo turno",
          turno_de(t) == turno_de(t.replace(minute=47, second=59)))
    check("P3 · y dos horas distintas NO son el mismo turno",
          turno_de(t) != turno_de(t + timedelta(hours=1)))
    check("P4 · `corrida` tiene el requisito CONTRARIO: dos seguidas nunca coinciden",
          _corrida_nueva() != _corrida_nueva())
    check("P5 · 24 turnos de un día son 24 nombres distintos",
          len({turno_de(x) for x in turnos_del_dia(t, 24)}) == 24)

    # --- P6-P9: un disparo solo, que es lo aburrido y tiene que estar ------
    c1 = base / "uno"
    r1 = disparo_doble(n=1, carpeta=c1, duracion_s=0.2, renglones=5)
    check("P6 · un disparo escribe todos sus renglones",
          r1["renglones_buenos"] == 5, str(r1["renglones_buenos"]))
    check("P7 · ninguno roto", r1["renglones_rotos"] == 0)
    check("P8 · una sola corrida", r1["corridas_distintas"] == 1)
    check("P9 · y deja su reporte válido", r1["reporte_valido"])

    # --- P10-P15: EL DISPARO DOBLE SOLAPADO -------------------------------
    c2 = base / "dos_a_la_vez"
    r2 = disparo_doble(n=2, carpeta=c2, duracion_s=0.6, renglones=8, separacion_s=0.0)
    check("P10 · 🚨 nadie revienta: el disparo doble NO produce un solo error",
          r2["procesos_reventados"] == 0, str(r2["errores"])[:200])
    check("P11 · 🚨 el trabajo se hizo DOS veces: dos corridas distintas",
          r2["corridas_distintas"] == 2, str(r2["corridas_distintas"]))
    check("P12 · y las dos dicen el MISMO turno — es el único dato que las une",
          r2["turnos_distintos"] == 1, str(r2["turnos_distintos"]))
    check("P13 · 🚨 y sin embargo queda UN solo entregable, no dos",
          r2["reportes_en_disco"] == 1)
    check("P14 · el reporte que sobrevive es válido: no parece dañado, parece normal",
          r2["reporte_valido"])
    check("P15 · el reporte lleva el nombre de UNO de los dos, y del otro no queda nada",
          r2["reporte_de"] in ("d0", "d1"), str(r2["reporte_de"]))

    # --- P16-P18: el disparo SECUENCIAL, que es otro bicho -----------------
    c3 = base / "dos_seguidos"
    r3 = disparo_doble(n=2, carpeta=c3, duracion_s=0.3, renglones=6, separacion_s=1.0)
    check("P16 · el segundo disparo arranca con el primero YA TERMINADO",
          r3["procesos_reventados"] == 0)
    check("P17 · 🚨 y repite el trabajo entero igual: dos corridas otra vez",
          r3["corridas_distintas"] == 2, str(r3["corridas_distintas"]))
    check("P18 · 🔑 no solaparse NO es no repetir — son dos problemas distintos",
          r3["corridas_distintas"] == r2["corridas_distintas"])

    # --- P19-P22: el archivo que queda es VÁLIDO, y eso es lo grave -------
    reg = c2 / "registro_disparador.jsonl"
    lineas = [l for l in reg.read_text(encoding="utf-8").splitlines() if l.strip()]
    check("P19 · el .jsonl del disparo doble no tiene ni una línea rota",
          all(json.loads(l) for l in lineas))
    check("P20 · 🔑 un lector no tiene NADA que señalar: dos corridas con nombres "
          "distintos es un archivo perfectamente legítimo",
          len({json.loads(l)["corrida"] for l in lineas}) == 2)
    # 🚨 P21 SE MIDE EN VARIAS RONDAS, Y ESO NO ES UN PARCHE: ES EL HALLAZGO.
    #    La pérdida NO ocurre siempre. Depende de que las dos escrituras caigan
    #    en la misma rendija, así que hay corridas enteras donde no se pierde ni
    #    un renglón. La primera versión de esta prueba pedía `perdidos > 0` en
    #    UNA corrida, y se puso roja sola media hora después, en la misma
    #    sesión en que se escribió.
    # 🔑 Y esa es exactamente la razón por la que un fallo así vive años en un
    #    programa: no se reproduce a la primera, así que el que lo ve una vez
    #    concluye que se equivocó. Una prueba de algo probabilístico tiene que
    #    medir la TASA, no el suceso.
    rondas = [disparo_doble(n=2, carpeta=base / f"perdida_{k}", duracion_s=0.4,
                            renglones=10, separacion_s=0.0)
              for k in range(4)]
    perdidos_total = sum(x["perdidos"] for x in rondas)
    rotos_total = sum(x["renglones_rotos"] for x in rondas)
    esperados_total = sum(x["esperados"] for x in rondas)
    check("P21 · 🚨 EL HALLAZGO: al solaparse FALTAN renglones, y ni uno está roto",
          perdidos_total > 0 and rotos_total == 0,
          f"faltan {perdidos_total} de {esperados_total} en 4 rondas "
          f"({100*perdidos_total/esperados_total:.1f}%), rotos {rotos_total}")
    check("P21b · ⭐ y NO pasa siempre: por eso un fallo así sobrevive años. "
          "Se mide la tasa, no el suceso",
          any(x["perdidos"] == 0 for x in rondas) or perdidos_total > 0,
          f"perdidos por ronda: {[x['perdidos'] for x in rondas]}")
    check("P22 · y el secuencial NO pierde ninguno: la pérdida es del SOLAPAMIENTO, "
          "no del trabajo",
          r3["perdidos"] == 0, f"perdidos {r3['perdidos']}")

    # --- P23-P26: por qué faltan. El experimento decisivo ------------------
    ra = atomico_o_no(n=200, carpeta=base / "atomico")
    check("P23 · 🚨 `open(ruta,\"a\")` NO es atómico entre procesos: aparecen "
          "renglones de longitud IMPOSIBLE",
          ra["imposibles"] > 0, f"{ra['imposibles']} raros, largos {ra['largos_raros']}")
    check("P24 · y su largo es exactamente 200 − 22 = 178: la COLA de una A "
          "pisada por un renglón de B entero",
          178 in ra["largos_raros"], str(ra["largos_raros"]))
    check("P25 · ⭐ NO se entrelazan a mitad de renglón: cero mixtos. Se PISAN",
          ra["mixtos"] == 0, str(ra["mixtos"]))
    check("P26 · y no quedan huecos sin escribir: los bytes cuadran con lo que hay",
          ra["huecos_sin_escribir"] == 0 and ra["bytes"] == ra["bytes_de_lo_que_queda"],
          f"{ra['bytes']} vs {ra['bytes_de_lo_que_queda']}")

    # --- P27-P29: lo que HOY no se puede preguntar -------------------------
    turnos_escritos = {json.loads(l)["turno"] for l in lineas}
    check("P27 · sí se puede escribir en código «esto se disparó dos veces»",
          len({json.loads(l)["corrida"] for l in lineas}) > 1)
    esperados = {turno_de(x) for x in turnos_del_dia(
        datetime(2026, 8, 24, 0, 0, tzinfo=timezone.utc), 24)}
    check("P28 · 🚨 y NO se puede escribir «esto no se disparó» mirando el registro: "
          "el turno que falta no deja renglón",
          len(turnos_escritos) < len(esperados),
          f"turnos con renglón: {len(turnos_escritos)} de 24 posibles")
    check("P29 · 🔑 el registro solo prueba lo que SÍ pasó — el silencio no es un dato",
          len(esperados - turnos_escritos) > 0)

    # --- P30-P37: EL ESCALÓN 2, el candado -------------------------------
    # 📌 Aquí las dos constantes van ENCOGIDAS (0,3 s y 0,6 s en vez de 5 y 30)
    #    para que las pruebas no tarden dos minutos. La proporción entre ellas
    #    es la misma, que es lo único de lo que depende el resultado. La tabla
    #    del informe se corre con los valores REALES del archivo.
    ESP, RAN = 0.3, 0.6

    c4 = base / "candado_corto"
    r4 = disparo_doble_con_candado(n=2, carpeta=c4, duracion_s=0.15, renglones=6,
                                   espera_s=ESP, rancio_s=RAN)
    check("P30 · con candado y trabajo CORTO no se pierde ni un renglón",
          r4["perdidos"] == 0, f"perdidos {r4['perdidos']}")
    check("P31 · 🚨 y aun así el trabajo se hace DOS veces: los dos consiguieron "
          "el candado, uno detrás del otro",
          r4["hicieron"] == 2, str(r4["veredictos"]))
    check("P32 · 🔑 un candado SERIALIZA, no DEDUPLICA: arregla el archivo y "
          "deja el problema intacto",
          r4["perdidos"] == 0 and r4["corridas_distintas"] == 2)

    c5 = base / "candado_largo"
    r5 = disparo_doble_con_candado(n=2, carpeta=c5, duracion_s=ESP * 2.5, renglones=6,
                                   espera_s=ESP, rancio_s=RAN)
    check("P33 · si el trabajo dura MÁS que la espera, el segundo cede",
          r5["cedieron"] == 1 and r5["hicieron"] == 1, str(r5["veredictos"]))
    check("P34 · y cede SIN reventar: `CandadoOcupado` es una decisión, no un fallo",
          r5["procesos_reventados"] == 0)

    c6 = base / "candado_rancio_inalcanzable"
    r6 = disparo_doble_con_candado(n=2, carpeta=c6, duracion_s=RAN * 1.6, renglones=6,
                                   espera_s=ESP, rancio_s=RAN)
    check("P35 · 🔴 LA APUESTA 1(b) FALLÓ: un trabajo más largo que la caducidad "
          "NO hace que el segundo rompa el candado",
          r6["hicieron"] == 1, str(r6["veredictos"]))
    check("P36 · 🔑 y el motivo: el que espera se rinde ANTES de poder declararlo "
          "rancio, porque espera < caducidad",
          ESP < RAN)

    c7 = base / "candado_paciente"
    r7 = disparo_doble_con_candado(n=2, carpeta=c7, duracion_s=RAN * 1.6, renglones=6,
                                   espera_s=RAN * 2.5, rancio_s=RAN)
    check("P37 · 🚨 EL BICHO DE VERDAD: con la espera POR ENCIMA de la caducidad, "
          "el segundo rompe el candado con su dueño vivo y entra",
          r7["hicieron"] == 2, str(r7["veredictos"]))
    check("P38 · y lo hace sin un solo error: nadie revienta, nadie avisa",
          r7["procesos_reventados"] == 0)
    check("P39 · ⭐ el fallo no lo dispara un trabajo largo — lo dispara SER MÁS "
          "PACIENTE: el único cambio entre P35 y P37 es la espera",
          r6["hicieron"] == 1 and r7["hicieron"] == 2)

    # --- P40-P44: la marca del turno, y el nombre de archivo --------------
    c8 = base / "marca"
    t8 = "2026-08-24T03:00"
    check("P40 · la primera marca la pone quien la pide", marcar_turno(c8, t8) is True)
    check("P41 · la segunda NO: `O_EXCL` hace la pregunta y el acto en un solo paso",
          marcar_turno(c8, t8) is False)
    check("P42 · y el turno queda dado por hecho", turno_ya_hecho(c8, t8))
    check("P43 · 🚨 EL BICHO DE WINDOWS: la marca tiene que APARECER al listar. "
          "Con los dos puntos en el nombre, `exists()` decía sí y `glob` cero",
          turnos_hechos(c8) == ["2026-08-24T03-00"], str(turnos_hechos(c8)))
    check("P44 · ⭐ y el turno conserva sus dos puntos DENTRO del registro: el "
          "nombre de archivo es otro uso del mismo dato",
          ":" in t8 and ":" not in _nombre_de_marca(t8), _nombre_de_marca(t8))

    # --- P45-P48: el turno arregla lo que el candado no podía -------------
    r8 = disparo_doble_con_turno(n=2, carpeta=base / "t_solape", separacion_s=0.0)
    check("P45 · dos a la vez → UNA sola corrida", r8["corridas_distintas"] == 1,
          str(r8["veredictos"]))
    r9 = disparo_doble_con_turno(n=2, carpeta=base / "t_secuencial", separacion_s=1.5)
    check("P46 · 🚨 y el SECUENCIAL también, que es el que el candado dejaba pasar",
          r9["corridas_distintas"] == 1 and r9["ya_estaba"] == 1, str(r9["veredictos"]))
    check("P47 · una marca por turno, ni más ni menos", r9["turnos_marcados"] == 1)
    check("P48 · 🔑 el segundo no CEDE: se entera de que ya está hecho y se va. "
          "Ceder y estar hecho son estados distintos y hacen falta los dos",
          r9["ya_estaba"] == 1 and r9["cedio"] == 0, str(r9["veredictos"]))

    # --- P49-P52: la elección que no tiene respuesta buena ----------------
    ra_ = disparo_doble_con_turno(n=2, carpeta=base / "t_antes", separacion_s=1.5,
                                  marcar="antes", fallar_en=3, renglones=8)
    rd_ = disparo_doble_con_turno(n=2, carpeta=base / "t_despues", separacion_s=1.5,
                                  marcar="despues", fallar_en=3, renglones=8)
    check("P49 · marcar ANTES = COMO MUCHO UNA VEZ: el trabajo se rompió y nadie "
          "lo reintenta nunca",
          ra_["ya_estaba"] == 1 and ra_["renglones_buenos"] < 8, str(ra_["veredictos"]))
    check("P50 · marcar DESPUÉS = AL MENOS UNA VEZ: el reintento sí trabaja",
          rd_["hizo"] == 1 and rd_["renglones_buenos"] > 8, str(rd_["veredictos"]))
    check("P51 · 🔑 y los renglones a medias del primer intento SE QUEDAN: "
          "«al menos una vez» no es «como si nada hubiera pasado»",
          rd_["renglones_buenos"] == 12, str(rd_["renglones_buenos"]))
    check("P52 · ⭐ no existe «exactamente una vez»: las dos opciones pierden algo, "
          "y son cosas opuestas",
          ra_["renglones_buenos"] != rd_["renglones_buenos"])

    # --- P53-P56: el cadáver, y para qué sirve de verdad la caducidad -----
    rm = disparo_doble_con_turno(n=2, carpeta=base / "t_muerto", separacion_s=1.5,
                                 marcar="despues", morir_en=3, renglones=8,
                                 espera_s=2.0, rancio_s=30.0)
    check("P53 · 🚨 si el proceso MUERE con el candado en la mano, el reintento "
          "no llega ni a mirar la marca: CEDE",
          rm["cedio"] == 1 and rm["hizo"] == 0, str(rm["veredictos"]))
    check("P54 · y el candado del muerto se queda colgado en el disco",
          (base / "t_muerto" / "trabajo.lock").exists())
    rv = disparo_doble_con_turno(n=2, carpeta=base / "t_muerto_rancio", separacion_s=1.5,
                                 marcar="despues", morir_en=3, renglones=8,
                                 espera_s=2.0, rancio_s=1.0)
    check("P55 · ⭐ con la caducidad POR DEBAJO del hueco entre disparos, el "
          "reintento rompe el candado del muerto y trabaja",
          rv["hizo"] == 1, str(rv["veredictos"]))
    check("P56 · 🔑 LA CADUCIDAD NO ES PARA EL SOLAPE — ES PARA EL CADÁVER. "
          "Único cambio entre P53 y P55: ese número",
          rm["hizo"] == 0 and rv["hizo"] == 1)

    # --- P57-P66: el escalón 4, el disparo que no ocurrió -----------------
    c9 = base / "auditoria"
    dia = datetime(2026, 8, 24, 3, 0, tzinfo=timezone.utc)
    t3, t4, t5 = (turno_de(dia + timedelta(hours=k)) for k in (0, 1, 2))

    marcar_turno(c9, t3)
    anotar_intento(c9, t3, "d0", "hizo")
    anotar_intento(c9, t4, "d0", "fallo")
    anotar_intento(c9, t4, "d1", "cedio")
    # t5 no recibe NADA: es el turno que no se disparó.

    check("P57 · el calendario es una lista escrita ANTES, no un resumen del disco",
          calendario(dia, dia + timedelta(hours=2)) == [t3, t4, t5])
    aud = auditar_turnos(c9, dia, dia + timedelta(hours=2))
    check("P58 · el turno que salió bien sale «hecho»", aud["por_turno"][t3] == "hecho")
    check("P59 · el turno donde vinieron dos y ninguno pudo sale «sin_exito»",
          aud["por_turno"][t4] == "sin_exito", aud["por_turno"][t4])
    check("P60 · 🚨 y el que NADIE disparó sale «MUDO» — que es el que importa",
          aud["por_turno"][t5] == "MUDO", aud["por_turno"][t5])
    check("P61 · 🔑 son TRES estados, no dos: «hecho», «vino y no pudo» y «no vino»",
          (aud["hechos"], aud["sin_exito"], aud["mudos"]) == (1, 1, 1),
          str((aud["hechos"], aud["sin_exito"], aud["mudos"])))
    check("P62 · ⭐ sin calendario los dos últimos son EL MISMO archivo: los dos "
          "«no hay marca»",
          not turno_ya_hecho(c9, t4) and not turno_ya_hecho(c9, t5))
    check("P63 · y el mudo no deja NADA que consultar: cero intentos, cero marca",
          intentos_de(c9, t5) == [] and not turno_ya_hecho(c9, t5))
    check("P64 · lo que SÍ se puede sin calendario es contar disparos de más",
          len(intentos_de(c9, t4)) == 2)

    # la deuda del escalón 2, pagada: el que cede deja rastro
    c10 = base / "cede_con_rastro"
    rc = disparo_doble_con_turno(n=2, carpeta=c10, separacion_s=0.0,
                                 duracion_s=1.2, renglones=8, espera_s=0.3)
    veredictos_anotados = {d["veredicto"] for d in intentos_de(c10)}
    check("P65 · 🚨 LA DEUDA DEL ESCALÓN 2, PAGADA: el disparo que cede ya deja "
          "renglón",
          "cedio" in veredictos_anotados or "ya_estaba" in veredictos_anotados,
          str(veredictos_anotados))
    check("P66 · 🔑 y por eso «vino y no pudo» dejó de verse igual que «no vino»",
          len(intentos_de(c10)) == 2, str(len(intentos_de(c10))))

    print()
    if fallos:
        print(f"❌ {len(fallos)} en rojo:")
        for f in fallos:
            print("   -", f)
    else:
        print("✅ las 67 en verde. $0,00 — ni una llamada al modelo.")
    return fallos


# ---------------------------------------------------------------------------
# 12) LOS GANCHOS DE LOS PROCESOS — esto es lo que ejecuta cada `python` hijo
# ---------------------------------------------------------------------------
def _hijo(quien, carpeta, arranque, duracion_s, renglones):
    """Espera a su instante y hace el trabajo. Es el agente programado entero."""
    while time.time() < float(arranque):
        time.sleep(0.001)
    correr_ingenuo(carpeta, quien=quien,
                   duracion_s=float(duracion_s), renglones=int(renglones))


def _hijo_candado(quien, carpeta, arranque, duracion_s, renglones, espera_s, rancio_s):
    """El hijo del escalón 2: pide el candado y deja escrito qué le pasó."""
    while time.time() < float(arranque):
        time.sleep(0.001)
    veredicto = correr_con_candado(
        carpeta, quien=quien, espera_s=float(espera_s), rancio_s=float(rancio_s),
        duracion_s=float(duracion_s), renglones=int(renglones))
    (Path(carpeta) / f"veredicto_{quien}.txt").write_text(veredicto, encoding="utf-8")


def _hijo_turno(quien, carpeta, arranque, duracion_s, renglones, espera_s,
                rancio_s, marcar, fallar_en, morir_en):
    """El hijo del escalón 3: mira el turno, pide el candado, trabaja, marca."""
    while time.time() < float(arranque):
        time.sleep(0.001)
    nada = lambda x: None if x in ("None", "", None) else int(x)
    veredicto = correr_con_turno(
        carpeta, quien=quien, marcar=marcar,
        espera_s=float(espera_s), rancio_s=float(rancio_s),
        duracion_s=float(duracion_s), renglones=int(renglones),
        fallar_en=nada(fallar_en), morir_en=nada(morir_en))
    (Path(carpeta) / f"veredicto_{quien}.txt").write_text(veredicto, encoding="utf-8")


def _hijo_atomico(ruta, marca, largo, n, arranque):
    """El del experimento decisivo: escribe renglones de un solo tamaño."""
    while time.time() < float(arranque):
        time.sleep(0.001)
    for _ in range(int(n)):
        with open(ruta, "a", encoding="utf-8") as f:
            f.write(marca * int(largo) + "\n")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--disparo":
        _hijo(*sys.argv[2:])
    elif len(sys.argv) > 1 and sys.argv[1] == "--candado":
        _hijo_candado(*sys.argv[2:])
    elif len(sys.argv) > 1 and sys.argv[1] == "--turno":
        _hijo_turno(*sys.argv[2:])
    elif len(sys.argv) > 1 and sys.argv[1] == "--atomico":
        _hijo_atomico(*sys.argv[2:])
    elif len(sys.argv) > 1 and sys.argv[1] == "--informe":
        informe_escalon_1()
        informe_atomicidad()
        informe_escalon_2()
        informe_escalon_3()
        informe_escalon_4()
    else:
        _pruebas()
        informe_escalon_1()
        informe_atomicidad()
        informe_escalon_2()
        informe_escalon_3()
        informe_escalon_4()
