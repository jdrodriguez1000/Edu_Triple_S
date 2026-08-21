"""C.2 — EL PRESUPUESTO DEL ENCARGO, REPARTIDO A LA ENTRADA.

    Hasta hoy el nivel 8 tenía un tope POR PIEZA: $0,05 el orquestador y $0,05
    cada worker. Siete sesiones puesto, y el conteo de la 98 dice lo que valía:

        65 cierres pagados · `motivo="presupuesto"` en 0 de ellos

    No es que el freno estuviera mal. Es que el tope estaba 6,3 veces por encima
    del máximo que un worker ha gastado jamás, así que **no podía morder**. Un
    freno que nadie ha visto morder es una nota (`LM.13`).

⭐ Y EL DEFECTO DE FONDO NO ERA EL NÚMERO: ERA QUE NO HABÍA UN NÚMERO.
   Tres workers y un orquestador a $0,05 dan $0,20 de techo — y **nadie eligió
   $0,20**. Sale de multiplicar. El que paga la factura no podía nombrar su
   límite, porque el encargo no tenía límite: lo tenían sus pedazos.

🔑 LA IDEA DE C.2, EN UNA FRASE: **el dinero es del ENCARGO, no de las piezas.**
   Se decide un total, se parte a la entrada, y cada worker sale con su trozo
   en el bolsillo.


    POR QUÉ «A LA ENTRADA» Y NO UNA BOLSA COMÚN

Se eligió entre tres esquemas (sesión 98) y este es el segundo:

  1. TOPE FIJO POR PIEZA  -> aísla el daño; el total no se puede nombrar.
  2. REPARTO A LA ENTRADA -> el total se nombra; el reparto es CIEGO.
  3. BOLSA COMÚN EN VIVO  -> ni desperdicia ni descuadra; necesita un candado en
                             CADA llamada, hay que ESTIMAR lo que va a costar
                             una llamada antes de hacerla, y el primero que
                             llega se lo puede comer todo.

📌 El 3 no es peor por elegante: es que mueve el candado al camino caliente. Aquí
   el candado protege sólo el ACTO DE REPARTIR —que ocurre una vez por worker— y
   no el acto de gastar. Los trozos se calculan enteros en el constructor, antes
   de que arranque el primer hilo.

🚨 Y EL PRECIO DEL 2 SE MIDIÓ ANTES DE ELEGIRLO, con los registros ya pagados:
   los tres workers de moneda cuestan lo mismo hasta la tercera cifra
   (dispersión 1,00x-1,02x en cinco corridas). O sea: **en la tarea del duelo el
   reparto ciego es casi óptimo, y por eso mismo la tarea no puede distinguir el
   esquema 2 del 1.** No es una tarea fácil: es un instrumento ciego para esta
   pregunta. Queda apuntado en el sobre como obligación: sin un encargo DESIGUAL,
   C.2 mide el freno pero no el reparto.


    LO QUE EL REPARTO A LA ENTRADA EXIGE, Y NO ES GRATIS

Para partir en trozos hay que saber **en cuántos**. Y quien decide cuántos
workers se lanzan es EL MODELO de arriba, en tiempo de ejecución.

⭐ Por eso existe `SinTrozo`. Si el modelo pide un cuarto especialista, no hay
   cuarto trozo: se queda sin gasolina y se le dice por qué.
   🔑 Es un modo de fallo que el esquema 1 NO tiene —allí el cuarto worker
      traería su propio $0,05 tan campante—, y es exactamente lo que se compra
      al poder nombrar el total. **Un techo que no se puede pasar es un techo
      con el que se puede chocar.**
"""

import threading
from pathlib import Path

# La cadena es limpia y en un solo sentido: presupuesto -> worker -> agente.
# `orquestador` NO se importa aquí arriba (él nos importa a nosotros); se pide
# dentro de las funciones que lo necesitan.
import worker

AQUI = Path(__file__).resolve().parent


# ---------------------------------------------------------------------------
# 1) LA REGLA — la forma se selló ANTES de elegir el número, y ese orden importa
# ---------------------------------------------------------------------------
# 🚨 EL SOSPECHOSO DE ESTAR CIEGO, NOMBRADO EN EL SOBRE ANTES DE ESCRIBIR ESTO:
#
#        «el que elige el número del presupuesto es el mismo que ya sabe
#         lo que cuesta una corrida»
#
#    Yo conté que un worker gasta $0,0073. Si ahora pongo el tope en $0,005, el
#    freno muerde — y no habrá medido nada, porque lo afiné contra el dato que
#    tenía delante. Un freno ajustado al resultado es una DEMOSTRACIÓN.
#
# → La defensa son dos obligaciones selladas, y las dos están en este archivo:
#   1. el número sale de una REGLA con su motivo escrito, no de un dedo;
#   2. hay una prueba que exige que el freno SE CALLE con un presupuesto normal
#      (`P1`, abajo). Es la única que no se puede escribir a la medida del
#      instrumento, porque pide que el instrumento no haga nada.

# --- Lo MEDIDO. Ninguno de estos cuatro es una estimación: los cuatro salen de
#     registros pagados que están en el repositorio.
COSTE_MEDIDO_ENCARGO_USD = 0.026390   # corrida real completa, sesión 97 paso 4
COSTE_MEDIDO_WORKER_USD = 0.007960    # el PEOR worker de moneda visto, no la media
COSTE_MEDIDO_ORQ_USD = 0.005233       # el peor `acumulado_usd` del orquestador
# 🚨 ESTE NÚMERO ERA UNA MEDIA Y SE USABA COMO TOPE, y lo destapó `P12`.
#    Era $0,002404 —la media de las dos llamadas de la demo C.1— y al contar las
#    170 llamadas pagadas del nivel resultó que **96 de ellas (el 56 %) costaron
#    más**. La regla de abajo se construía sobre un precio que fallaba más de la
#    mitad de las veces.
# → Ahora sale del mismo sitio que la estimación del freno: el p90 medido. Un
#   solo número, un solo dueño (`worker.py`), y el archivo que decide el
#   presupuesto usa **exactamente** el que usa el que frena. Dos copias del
#   precio de una llamada era el bicho esperando.
COSTE_LLAMADA_WORKER_USD = worker.COSTE_ESTIMADO_LLAMADA_USD    # p90: $0,004546

# --- La HOLGURA. Es el único número de juicio, y va con su motivo.
# Un presupuesto se calcula con el precio malo, no con el medio (lección del
# nivel 7). El precio malo ya está arriba; la holgura cubre lo que ese precio no
# ve: un día en que el modelo dé una vuelta de más.
# ⚠️ Y es DELIBERADAMENTE generosa. Un presupuesto que muerde en operación normal
#    no es un freno: es una avería. Que sea generosa es lo que hace que `P1`
#    pueda existir.
HOLGURA = 1.5

# --- La RESERVA DE ARRIBA. Medida, no supuesta: el orquestador se llevó
#     $0,005233 de $0,026390, o sea el 19,8 %. Se declara 25 % —el cuarto
#     superior más cercano— para no dejarlo justo en su propio máximo.
RESERVA_ARRIBA = 0.25

# --- Cuántos workers se esperan. Sale de la tarea del duelo: tres monedas.
# 📌 Que esto sea una constante es la mitad interesante de C.2. El reparto ciego
#    necesita el reparto ANTES de saber qué va a pedir el modelo.
N_WORKERS_ESPERADOS = 3


def presupuesto_del_encargo(coste_medido=COSTE_MEDIDO_ENCARGO_USD,
                            holgura=HOLGURA):
    """El total del encargo. UNA constante, legible en voz alta.

    «Este encargo no puede costar más de X.» Antes de C.2 esa frase no se podía
    decir sobre el nivel 8, y no por descuido: no había X.
    """
    return round(coste_medido * holgura, 6)


PRESUPUESTO_ENCARGO_USD = presupuesto_del_encargo()   # $0,039585


def presupuesto_apretado(llamadas_permitidas=1.5,
                         n_workers=N_WORKERS_ESPERADOS,
                         reserva_arriba=RESERVA_ARRIBA):
    """El presupuesto con el que el freno SÍ tiene que morder, y sale de una regla.

    No se elige un número bonito: se elige cuántas llamadas al modelo caben en un
    trozo, y el dinero se deduce del coste medido de una llamada.

    🚨 Y LA PREDICCIÓN CAMBIÓ AL ARREGLAR EL TECHO — se deja escrito el cambio en
       vez de reescribir la vieja, porque lo que enseña es el ANTES y el DESPUÉS.

       Con el freno CIEGO (`gastado >= techo`), `llamadas_permitidas=1.5` daba:
         · llamada 1 -> gastado $0 < trozo            -> pasa
         · llamada 2 -> gastado ~$0,0023 < trozo      -> pasa (¡y no cabía!)
         · llamada 3 -> gastado ~$0,0049 > trozo      -> LA 3 SE BLOQUEA
       O sea: el trozo pagaba 1,5 llamadas y se hacían 2. Ese medio de más,
       multiplicado por los cuatro participantes, es el 27,5 % que se pasó.

       Con el freno que ESTIMA (`gastado + estimado > techo`), el 1,5 se cumple
       literalmente:
         · llamada 1 -> 0 + $0,004546 <= trozo $0,006819   -> pasa
         · llamada 2 -> ya no cabe                          -> LA 2 SE BLOQUEA

    ⭐ EL CORTE SE ADELANTA UNA LLAMADA ENTERA, Y ESE ES EL PRECIO DEL ARREGLO.
       Con el freno viejo el worker moría **con la respuesta en la mano** —tenía
       `tasa` y `convertir` hechas y sólo le faltaba redactar—. Con este muere
       antes de `convertir`. 🔑 Un freno ciego llega más lejos y se pasa del
       techo; uno que estima corta a tiempo y tira menos trabajo pagado.
       **No hay una tercera opción sin cambiar de esquema.**

    📌 Y el número del trozo se movió de $0,003606 a $0,006819 **sin tocar la
       regla**: `llamadas_permitidas` sigue siendo 1,5. Lo que cambió fue el
       precio de una llamada, que estaba mal medido. Cambiar el precio no es
       mover la portería; aflojar el 1,5 hasta que la prueba se pusiera verde
       sí lo habría sido (`LM.21`).
    """
    trozo = COSTE_LLAMADA_WORKER_USD * llamadas_permitidas
    return round(trozo * n_workers / (1.0 - reserva_arriba), 6)


PRESUPUESTO_APRETADO_USD = presupuesto_apretado()     # $0,014424


# ---------------------------------------------------------------------------
# 2) EL REPARTO
# ---------------------------------------------------------------------------

class SinTrozo(Exception):
    """Se pidió un trozo y ya no quedan. NO es lo mismo que quedarse sin dinero.

    ⭐ La diferencia importa y es la lección del esquema 2:
       · `PresupuestoAgotado` -> gastaste lo tuyo.
       · `SinTrozo`           -> eres el cuarto y sólo se repartió para tres.
    """


class RepartoDeEntrada:
    """Parte el presupuesto del encargo ANTES de lanzar a nadie.

    Los trozos se calculan enteros en el constructor. Lo único que ocurre
    durante la corrida es ENTREGARLOS, y eso sí lleva candado: en el fan-out de
    B.2 tres hilos piden su trozo a la vez, y `lista.pop()` desde tres hilos es
    la misma carrera que `d[k] += x`.

    📌 Fíjate en el tamaño del trozo protegido: una entrega por worker, tres en
       toda la corrida. En el esquema 3 el candado se tocaría en CADA llamada al
       modelo, que son ~9. La diferencia entre los dos esquemas no es de idea:
       es de cuántas veces se pone la cola.
    """

    def __init__(self, total_usd=PRESUPUESTO_ENCARGO_USD,
                 n_workers=N_WORKERS_ESPERADOS,
                 reserva_arriba=RESERVA_ARRIBA):
        if n_workers < 1:
            raise ValueError("un reparto para cero workers no es un reparto")

        self.total_usd = round(total_usd, 6)
        self.n_workers = n_workers

        # Lo que va abajo se parte en partes iguales. Es CIEGO a propósito: nadie
        # sabe todavía a qué moneda le tocará cada trozo, y en esta tarea da
        # igual (dispersión medida: 1,01x).
        para_abajo = self.total_usd * (1.0 - reserva_arriba)
        trozo = round(para_abajo / n_workers, 6)
        self._trozos = [trozo] * n_workers
        self._trozo = trozo

        # 🐛 Y AQUÍ SE CAZÓ UN FALLO DE VERDAD, EN LA PRIMERA CORRIDA DE `P4`.
        #    La versión anterior redondeaba los dos lados por separado:
        #        arriba = round(total * 0,25)   y   trozo = round(resto / 3)
        #    Con $0,039585 eso daba $0,009896 arriba y $0,009896 × 3 abajo, o sea
        #    **$0,039584 — una millonésima MENOS que el total**. Nadie protestaba:
        #    el dinero desaparecía en silencio.
        # 🔑 No es la millonésima lo que importa: es que un reparto que no cuadra
        #    con el total deja de ser un reparto. Si el error se escala con el
        #    número de trozos, un fan-out de 100 workers pierde 100 veces más.
        # → El resto se queda ARRIBA, y no es arbitrario: el que responde de la
        #   factura es el único que no se puede quedar corto por un redondeo.
        self.arriba_usd = round(self.total_usd - trozo * n_workers, 6)

        self.entregados = {}          # nombre -> cuánto se le dio
        self.rechazados = []          # los que llegaron tarde
        self._candado = threading.Lock()

    # --- lo que se entrega ------------------------------------------------
    def tomar(self, nombre):
        """Entrega un trozo a `nombre`. Si no quedan, `SinTrozo`."""
        with self._candado:
            if not self._trozos:
                self.rechazados.append(nombre)
                raise SinTrozo(
                    f"'{nombre}' es el worker número "
                    f"{self.n_workers + len(self.rechazados)} y el encargo se "
                    f"repartió para {self.n_workers}")
            trozo = self._trozos.pop()
            self.entregados[nombre] = trozo
            return trozo

    # --- lo que se puede preguntar ---------------------------------------
    def trozo_nominal(self):
        """Cuánto vale un trozo, sin entregar nada. Para las pruebas y el informe.

        📌 Se lee de `_trozos` y NO se recalcula. Recalcularlo era justo el fallo
           que cazó `P4`: dos caminos hasta el mismo número que no daban lo mismo.
        """
        return self._trozo

    def sin_repartir(self):
        """Dinero que quedó en la mesa porque nadie lo pidió."""
        return round(sum(self._trozos), 6)

    def cuadra(self):
        """Ni se crea ni se pierde dinero: arriba + entregado + sin repartir == total.

        🔑 Es `LM.66` aplicado aquí: un número que sólo puede comprobarse contra
           sí mismo no es comprobable. Este se comprueba por dos caminos —lo que
           se repartió y lo que se guardó— y tienen que dar el total.
        """
        suma = self.arriba_usd + sum(self.entregados.values()) + self.sin_repartir()
        return abs(round(suma, 6) - self.total_usd) < 1e-6

    def informe(self):
        return {
            "total_usd": self.total_usd,
            "arriba_usd": self.arriba_usd,
            "trozo_usd": self.trozo_nominal(),
            "entregados": dict(self.entregados),
            "rechazados": list(self.rechazados),
            "sin_repartir_usd": self.sin_repartir(),
            "cuadra": self.cuadra(),
        }




# ---------------------------------------------------------------------------
# 2.b) EL ENCARGO DESIGUAL — la obligación del sobre, y se diseña CON UN NÚMERO
# ---------------------------------------------------------------------------
# 🚨 EL MODO DE FALLO VA NOMBRADO ANTES DE CORRER, que es la mitad que se olvida:
#    **que el encargo «desigual» no lo sea de verdad.** Si el worker caro cuesta
#    un 20 % más, la corrida no distingue nada, y el resultado no será «apuesta
#    fallada»: será **instrumento ciego otra vez**, que es lo que pasó ayer.
#    Por eso la desigualdad no se pide con un adjetivo. Se construye.
#
#    ⭐ Y LA PALANCA NO ES «MÁS TRABAJO»: ES «TRABAJO QUE DEPENDE DEL ANTERIOR».
#       Pedirle cuatro conversiones a la vez NO encarece casi nada — el modelo
#       puede pedir las cuatro herramientas en la MISMA vuelta, y lo que se paga
#       son vueltas, no herramientas. Para forzar vueltas hace falta que el
#       segundo paso **necesite el resultado del primero**. Una cadena.
#    🔑 Es una lección de coste que sólo se ve al intentar encarecer algo a
#       propósito: en un agente, el precio lo pone la PROFUNDIDAD de la cadena
#       de dependencias, no la cantidad de trabajo.

# --- Los baratos: la frase de siempre. 3 vueltas -> tasa, convertir, redactar.
_ENCARGO_BARATO = "Convierte {monto} {moneda} a pesos colombianos."

# --- El caro: una CADENA de tres eslabones, cada uno atado al anterior.
#     Vuelta 1: tasa(CAD)      · vuelta 2: convertir a pesos
#     Vuelta 3: tasa(USD)      · vuelta 4: convertir esos pesos a dólares
#     Vuelta 5: tasa(EUR)      · vuelta 6: convertir esos dólares a euros
#     Vuelta 7: redactar
_ENCARGO_CARO = (
    "Convierte {monto} {moneda} a pesos colombianos. "
    "Después convierte ESE resultado en pesos a dólares estadounidenses. "
    "Y después convierte ESE resultado en dólares a euros. "
    "Hazlo paso a paso, en ese orden, usando el resultado de cada paso como "
    "entrada del siguiente. Dime las tres cifras."
)

ENCARGOS_DESIGUALES = {
    "USD": _ENCARGO_BARATO,
    "EUR": _ENCARGO_BARATO,
    "CAD": _ENCARGO_CARO,      # el caro, y se elige el CAD a propósito: es la
                               # moneda cuya fuente ya dio guerra en A.2
}

# --- EL NÚMERO CON EL QUE SE DISEÑÓ, escrito antes de correr nada -----------
# Vueltas esperadas: 3 los baratos, ~7 el caro. Con el p90 de $0,004546 por
# llamada, eso es ~$0,0136 contra ~$0,0136/3... o sea una razón de **~2,3x**.
# 📌 Se declara un mínimo, no una predicción exacta: si al medir la razón sale
#    por debajo de 1,8x, EL INSTRUMENTO NO SIRVE y hay que alargar la cadena
#    antes de gastar en la corrida buena. Ese umbral está puesto ahora, no
#    después de ver el resultado.
RAZON_MINIMA_UTIL = 1.8
VUELTAS_ESPERADAS_BARATO = 3
VUELTAS_ESPERADAS_CARO = 7


def presupuesto_desigual(n_workers=N_WORKERS_ESPERADOS,
                         reserva_arriba=RESERVA_ARRIBA):
    """El techo para la corrida desigual: lo que costaría si TODOS fueran caros.

    ⭐ Y ESTA ES LA TRAMPA QUE SE EVITA A PROPÓSITO. Lo fácil sería poner un
       techo pequeño para que el caro corte seguro. Eso demostraría que el freno
       muerde —que ya se sabe desde ayer— y **no diría nada del reparto**.
       Lo que hay que mirar es otra cosa: con un techo que da de sobra para el
       encargo ENTERO, ¿basta que el reparto sea CIEGO para que el caro se
       ahogue mientras a los baratos les sobra?
    🔑 Si el caro corta con este techo, el culpable no es el número: **es el
       reparto a partes iguales.** Y ése es exactamente el defecto del
       candidato 2 que la tarea gemela no podía enseñar.

    ⚠️ ESTE TECHO VA SIN HOLGURA, Y ES LA ÚNICA VEZ EN TODO C.2 QUE ESO ESTÁ
       BIEN. Los presupuestos de operación llevan holgura porque un freno que
       muerde en un día normal es una avería. Éste **no es un presupuesto de
       operación: es un instrumento de medida**, y la holgura le quitaría filo —
       con un 50 % de más el trozo casi alcanza al caro y el resultado se
       volvería ambiguo (¿cortó por el reparto o porque el techo iba justo?).
       Aquí se pone **exactamente el dinero que el encargo necesita**, para que
       la frase que salga sea la más afilada posible:
       **«había justo lo necesario, y el que lo necesitaba no pudo tocarlo».**

    📌 Y el número que se aprende del otro lado: para que un reparto CIEGO a
       tercios no ahogue nunca al caro, el encargo tendría que llevar
       `3 × coste_del_caro` — o sea **pagar tres veces el peor worker**. Eso es
       lo que cuesta no saber, a la entrada, cuál de los tres va a ser el caro.
    """
    coste_esperado = (2 * VUELTAS_ESPERADAS_BARATO + VUELTAS_ESPERADAS_CARO)
    total_abajo = coste_esperado * worker.COSTE_ESTIMADO_LLAMADA_USD
    return round(total_abajo / (1.0 - reserva_arriba), 6)


PRESUPUESTO_DESIGUAL_USD = presupuesto_desigual()


# ---------------------------------------------------------------------------
# 3) LAS PRUEBAS — y las dos primeras son las OBLIGACIONES DEL SOBRE
# ---------------------------------------------------------------------------

def _pruebas():
    fallos = []

    def check(nombre, cond, detalle=""):
        print(("  OK  " if cond else "  XX  ") + nombre + (f"  -> {detalle}" if detalle else ""))
        if not cond:
            fallos.append(nombre)

    print("\n[C.2] presupuesto del encargo, repartido a la entrada\n")

    # --- P1: LA OBLIGACIÓN DEL SOBRE. El freno tiene que CALLARSE. -------
    # 🔑 Es la única prueba que no se puede escribir a la medida del instrumento,
    #    porque pide que el instrumento no haga nada. Si mañana alguien aprieta el
    #    presupuesto "para que se vea el freno", esta se pone roja y hay que venir
    #    a tacharla a mano. Un freno que muerde siempre es tan inútil como uno que
    #    no muerde nunca, y hasta hoy sólo se vigilaba la segunda mitad.
    r = RepartoDeEntrada()
    check("P1 · con presupuesto NORMAL el trozo cubre al PEOR worker medido",
          r.trozo_nominal() > COSTE_MEDIDO_WORKER_USD,
          f"trozo ${r.trozo_nominal():.6f} > peor worker ${COSTE_MEDIDO_WORKER_USD:.6f}")
    check("P1b · y la reserva de arriba cubre al PEOR orquestador medido",
          r.arriba_usd > COSTE_MEDIDO_ORQ_USD,
          f"arriba ${r.arriba_usd:.6f} > peor orq ${COSTE_MEDIDO_ORQ_USD:.6f}")

    # --- P2: y con el apretado tiene que MORDER, por una regla, no por un dedo
    a = RepartoDeEntrada(total_usd=PRESUPUESTO_APRETADO_USD)
    check("P2 · con presupuesto APRETADO el trozo NO llega a dos llamadas",
          a.trozo_nominal() < 2 * COSTE_LLAMADA_WORKER_USD,
          f"trozo ${a.trozo_nominal():.6f} < 2 llamadas "
          f"${2 * COSTE_LLAMADA_WORKER_USD:.6f}")
    check("P2b · pero SÍ llega a una: el corte cae en la 2a, no en la puerta",
          a.trozo_nominal() > COSTE_LLAMADA_WORKER_USD,
          f"trozo ${a.trozo_nominal():.6f} > 1 llamada "
          f"${COSTE_LLAMADA_WORKER_USD:.6f}")

    # --- P3: el modo de fallo que el esquema 1 NO tiene ------------------
    r3 = RepartoDeEntrada()
    for n in ("usd", "eur", "cad"):
        r3.tomar(n)
    try:
        r3.tomar("jpy")
        check("P3 · el CUARTO worker se queda sin trozo", False, "no levantó SinTrozo")
    except SinTrozo as fallo:
        check("P3 · el CUARTO worker se queda sin trozo", True, str(fallo))

    # --- P4: ni se crea ni se pierde dinero ------------------------------
    check("P4 · el reparto cuadra por dos caminos (repartido + guardado == total)",
          r3.cuadra(), f"total ${r3.total_usd:.6f}")

    r4 = RepartoDeEntrada()
    r4.tomar("usd")
    check("P4b · y cuadra también a medio repartir",
          r4.cuadra(), f"sin repartir ${r4.sin_repartir():.6f}")

    # --- P5: el total es UNA constante y se puede decir en voz alta ------
    check("P5 · el total sale de la regla, no de un dedo",
          PRESUPUESTO_ENCARGO_USD == round(COSTE_MEDIDO_ENCARGO_USD * HOLGURA, 6),
          f"${COSTE_MEDIDO_ENCARGO_USD:.6f} x {HOLGURA} = ${PRESUPUESTO_ENCARGO_USD:.6f}")
    check("P5b · y es MENOR que el techo de ayer ($0,20 sin que nadie lo eligiera)",
          PRESUPUESTO_ENCARGO_USD < 0.20,
          f"${PRESUPUESTO_ENCARGO_USD:.6f} < $0,200000")

    # --- P6: varios hilos pidiendo a la vez no se llevan el mismo trozo --
    # ⚠️ Es el sitio donde el fan-out de B.2 destapó los otros dos compartidos.
    #    Aquí se ejercita a propósito: sin candado, `pop()` desde varios hilos
    #    puede entregar de menos y NO da error.
    r6 = RepartoDeEntrada(n_workers=24)
    salidas = []
    cerrojo_lista = threading.Lock()

    def pedir(i):
        try:
            t = r6.tomar(f"w{i}")
            with cerrojo_lista:
                salidas.append(t)
        except SinTrozo:
            pass

    hilos = [threading.Thread(target=pedir, args=(i,)) for i in range(24)]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    check("P6 · 24 hilos pidiendo a la vez reciben 24 trozos, sin perder ninguno",
          len(salidas) == 24 and len(r6.entregados) == 24 and r6.sin_repartir() == 0.0,
          f"entregados={len(r6.entregados)} sobrante=${r6.sin_repartir():.6f}")
    check("P6b · y sigue cuadrando después de la tanda paralela", r6.cuadra())

    # --- P7: un reparto para cero workers no existe ----------------------
    try:
        RepartoDeEntrada(n_workers=0)
        check("P7 · un reparto para 0 workers se rechaza", False, "no levantó ValueError")
    except ValueError:
        check("P7 · un reparto para 0 workers se rechaza", True)

    # --- P8/P9/P10: EL CABLE. Que la clase funcione no dice que esté enchufada.
    # 🔑 Es la lección del nivel entero: un freno en un módulo aparte, correcto y
    #    con todas sus pruebas en verde, **no frena nada** si nadie lo llama. Aquí
    #    se comprueba el camino de verdad —`herramienta_consultar_moneda`— con el
    #    worker sustituido por uno falso, así que sigue costando $0,00.
    import orquestador          # dentro, para no morder la importación circular

    # 🐛 EL INSTRUMENTO DE MEDIDA ESCRIBÍA EN LOS DATOS DE VERDAD, Y SE CAZÓ
    #    CONTANDO — no revisando código.
    #    Al medir el coste real de una llamada sobre los registros pagados, la
    #    secuencia que salió era 0,002300 -> 0,002650 -> 0,003000: **los números
    #    inventados de `_GUION`, aquí abajo.** Las pruebas gratis de este archivo
    #    llevaban once líneas de mentira metidas en
    #    `registro_workers_claude-haiku-4-5.jsonl`, que es la EVIDENCIA PAGADA
    #    del nivel — la que sube a Git justamente porque volver a producirla
    #    cuesta dinero.
    # 🚨 Es la sesión 50 de TEAPP, palabra por palabra: *el que estaba ensuciando
    #    los datos de verdad era la báscula.* Y aquí llevaba puesto desde ayer:
    #    la prueba `P9` ya venía dejando su línea `sin_trozo`.
    # 🔑 Lo que lo hace peor que un dato falso es que **no da error**: un registro
    #    contaminado se lee igual de bien, y el conteo de mañana saldrá torcido
    #    sin que nadie lo note. Lo cazó que los números falsos eran RECONOCIBLES.
    #    Si `_GUION` hubiera usado cifras verosímiles, seguirían ahí.
    # → Las pruebas escriben en su propio archivo, y ese NO sube (`.gitignore`).
    import worker as w
    _reg_w, _reg_o = w.REGISTRO, orquestador.REGISTRO
    w.REGISTRO = AQUI / "registro_pruebas_gratis.jsonl"
    orquestador.REGISTRO = w.REGISTRO

    vistos = []

    def worker_falso(encargo, nombre="x", presupuesto_usd=None, verboso=True, **kw):
        vistos.append((nombre, presupuesto_usd))
        return {"ok": True, "texto": "(falso)", "coste_usd": 0.0, "vueltas": 1,
                "llamadas_api": 0, "entrada_tokens": 0, "salida_tokens": 0,
                "segundos": 0.0, "herramientas": [], "motivo": None,
                "worker": nombre,
                "datos": {"moneda": nombre.upper(), "pesos": 1.0,
                          "tasa": 1.0, "fuente": "falsa", "fecha": "hoy",
                          "monto": 1000},
                "faltan": []}

    real = orquestador.worker.correr_worker
    orquestador.worker.correr_worker = worker_falso
    try:
        # 🐛 Y AQUÍ MORDIÓ UN BICHO QUE MERECE QUEDARSE ESCRITO.
        #    Al correr ESTE archivo directamente, Python lo carga como `__main__`
        #    y, cuando `orquestador` hace `import presupuesto`, lo carga OTRA VEZ
        #    con otro nombre. Son dos copias, y por tanto **dos clases `SinTrozo`
        #    distintas**: el `except presupuesto.SinTrozo` del orquestador no
        #    atrapaba la excepción de la copia de aquí, y la prueba reventaba con
        #    el mensaje correcto por el camino equivocado.
        # 🔑 No es una rareza de las pruebas: es que la identidad de una clase en
        #    Python es (módulo, nombre), no el nombre. Un `except` puede fallar
        #    ante una excepción que se llama igual y parece la misma.
        # → Por eso el reparto se construye con LA COPIA QUE USA EL ORQUESTADOR.
        rep = orquestador.presupuesto.RepartoDeEntrada()
        conta = {"capa": "orquestador", "workers": 0, "coste_workers_usd": 0.0,
                 "llamadas_api_workers": 0, "entrada_workers": 0,
                 "salida_workers": 0, "detalle": [], "reparto": rep}

        for m in ("USD", "EUR", "CAD"):
            orquestador.herramienta_consultar_moneda(1000, m, conta, verboso=False)

        check("P8 · el trozo LLEGA al worker (no se queda en el módulo)",
              len(vistos) == 3 and all(p == rep.trozo_nominal() for _, p in vistos),
              f"{vistos}")

        cuarto = orquestador.herramienta_consultar_moneda(1000, "JPY", conta,
                                                          verboso=False)
        check("P9 · el CUARTO no arranca: se le dice al modelo, no se revienta",
              cuarto.get("sin_trozo") is True and len(vistos) == 3,
              f"workers arrancados={len(vistos)}")

        # --- P10: y sin reparto, NADA cambia. Es la otra mitad de P1.
        vistos.clear()
        conta_vieja = dict(conta, reparto=None, detalle=[])
        orquestador.herramienta_consultar_moneda(1000, "USD", conta_vieja,
                                                 verboso=False)
        check("P10 · sin reparto se usa el tope de siempre: A.2 y el bloque B "
              "no cambian de conducta",
              vistos == [("usd", orquestador.worker.PRESUPUESTO_WORKER_USD)],
              f"{vistos}")
    finally:
        orquestador.worker.correr_worker = real

    # --- P11/P12/P13/P14: EL TECHO ARREGLADO, MEDIDO SIN PAGAR UN CENTAVO -
    # 🚨 ES LA OBLIGACIÓN DE `LM.13` PARA EL ARREGLO DE HOY: un freno que nadie
    #    ha visto morder es una nota. Ayer el freno viejo se pasó un 27,5 % del
    #    techo; hoy se cambió `gastado >= techo` por `gastado + estimado > techo`
    #    y **eso hay que verlo, no prometerlo**.
    #
    # ⭐ Y SE MIDE SOBRE EL BUCLE DE VERDAD, no sobre una copia de la aritmética.
    #    Lo único falso es la API: un cliente de mentira que devuelve respuestas
    #    con `usage` inventado pero REALISTA, y un puente de herramientas de
    #    mentira para no tocar la red. Todo lo demás —el `if` del freno, la
    #    estimación, `cerrar()`, el `except`— es el código que correrá pagando.
    # 🔑 Comprobar una copia de la fórmula habría dado verde con el bug de ayer
    #    dentro: la copia habría tenido el bug copiado.

    class _Uso:
        def __init__(self, e, s):
            self.input_tokens, self.output_tokens = e, s

    class _Bloque:
        def __init__(self, tipo, **kw):
            self.type = tipo
            self.__dict__.update(kw)

    class _Respuesta:
        def __init__(self, bloques, stop, uso):
            self.content, self.stop_reason, self.usage = bloques, stop, uso

    # Tres llamadas con el historial CRECIENDO, que es lo que pasa de verdad:
    # cada vuelta reenvía todo lo anterior, así que la entrada sube y la llamada
    # se encarece. Los tokens salen de quedar cerca de los $0,0024 medidos.
    _GUION = [
        (1400, 180, "tasa"),
        (1900, 150, "convertir"),
        (2400, 120, None),          # None = redacta y termina
    ]

    class _ClienteFalso:
        def __init__(self):
            self.messages = self
            self.n = 0

        def create(self, **kw):
            e, s, herr = _GUION[min(self.n, len(_GUION) - 1)]
            self.n += 1
            if herr is None:
                return _Respuesta([_Bloque("text", text="Son 4.000.000 de pesos.")],
                                  "end_turn", _Uso(e, s))
            return _Respuesta(
                [_Bloque("tool_use", name=herr, id="t%d" % self.n, input={})],
                "tool_use", _Uso(e, s))

    def _correr_worker_falso(presupuesto_usd):
        """Corre el worker REAL con la API y las herramientas de mentira."""
        cliente_real = w.agente.cliente
        puente_real = w.puente_para
        w.agente.cliente = _ClienteFalso()
        w.puente_para = lambda nombres: {
            "tasa": lambda **kw: {"tasa": 4000.0, "fuente": "falsa", "fecha": "hoy"},
            "convertir": lambda **kw: {"pesos": 4000000.0},
        }
        try:
            return w.correr_worker("falso", nombre="prueba",
                                   presupuesto_usd=presupuesto_usd, verboso=False)
        finally:
            w.agente.cliente = cliente_real
            w.puente_para = puente_real

    # P11 · con el trozo APRETADO el freno muerde ANTES de pasarse del techo.
    #       Es la prueba que el freno viejo habría FALLADO: con `>=` la llamada 2
    #       se autorizaba (gastado $0,00230 < trozo $0,003606) y el gasto acababa
    #       en $0,00495 — un 37 % por encima del trozo.
    trozo_ap = RepartoDeEntrada(total_usd=PRESUPUESTO_APRETADO_USD).trozo_nominal()
    rp = _correr_worker_falso(trozo_ap)
    check("P11 · el trozo APRETADO se respeta: el gasto NO se pasa del techo",
          rp["coste_usd"] <= trozo_ap and rp["motivo"] == "presupuesto",
          "gasto $%.6f de $%.6f - motivo=%s"
          % (rp["coste_usd"], trozo_ap, rp["motivo"]))

    # P11b · Y EL PRECIO DEL ARREGLO, COMO NÚMERO Y NO COMO ADJETIVO.
    #        El freno viejo dejaba llegar a la llamada 3; este corta en la 2.
    #        Una llamada menos de trabajo hecho, a cambio de no pasarse del techo.
    check("P11b · y el corte se ADELANTA: una sola llamada, no dos",
          rp["llamadas_api"] == 1,
          "%d llamadas - herramientas: %s"
          % (rp["llamadas_api"], rp["herramientas"] or "ninguna"))

    # P12 · LA BÁSCULA DE LA PROPIA ESTIMACIÓN. Estimar puede quedarse corto, y
    #       cuando se queda corto el techo se pasa igual. Que este contador
    #       exista es lo que separa el arreglo de una promesa.
    trozo_no = RepartoDeEntrada().trozo_nominal()
    rn = _correr_worker_falso(trozo_no)
    check("P12 · la estimación no se quedó corta en ninguna llamada",
          rn["estimaciones_cortas"] == 0,
          "%d de %d - peor llamada $%.6f vs estimada $%.6f"
          % (rn["estimaciones_cortas"], rn["llamadas_api"],
             rn["peor_llamada_usd"], w.COSTE_ESTIMADO_LLAMADA_USD))

    # P13 · Y LA OTRA MITAD, QUE ES `P1` EN EL CAMINO REAL: con el presupuesto
    #       NORMAL el freno arreglado tiene que seguir CALLADO. Un freno más
    #       estricto que muerde en operación normal no es más seguro: es una
    #       avería, y sería la forma fácil de "ganar" esta sesión.
    check("P13 · con presupuesto NORMAL el freno arreglado SIGUE callado",
          rn["motivo"] is None and rn["ok"] and rn["llamadas_api"] == 3,
          "motivo=%s - %d llamadas - $%.6f de $%.6f"
          % (rn["motivo"], rn["llamadas_api"], rn["coste_usd"], trozo_no))

    # P13b · EL MARGEN QUE QUEDA EN OPERACIÓN NORMAL, Y ES EL HALLAZGO DE HOY.
    # 🚨 Importancia: ALTA · Urgencia: NO bloqueante (nada se rompe hoy).
    #    El arreglo del techo tiene un modo de fallo NUEVO, que es el espejo del
    #    de ayer: si la estimación se pasa POR ARRIBA, el freno corta a un worker
    #    que **sí cabía**. Ayer el freno dejaba pasar de más; hoy puede cortar de
    #    más. Un `>=` ciego tenía falsos negativos; un `+ estimado` tiene falsos
    #    positivos. **Ningún freno que decida antes de conocer el precio se libra
    #    de los dos.**
    #
    #    El número, sobre el peor worker que se ha visto pagar en todo el nivel:
    #      trozo normal            $0,009896
    #      peor worker medido      $0,007960
    #      margen                  $0,001936  <- MENOS DE MEDIA LLAMADA ESTIMADA
    #
    # 🔑 Con el freno viejo ese margen era irrelevante: no miraba el precio, así
    #    que un worker caro llegaba hasta el final igual (pasándose). Con este,
    #    **una vuelta de más del modelo en operación normal ya corta.** El techo
    #    dejó de ser holgado sin que nadie moviera el techo.
    # 📌 No se toca `HOLGURA` para arreglarlo. Subirla ahora, con este número
    #    delante, sería moverla contra un resultado ya visto (`LM.21`). Queda
    #    dicho, medido, y lo decide la corrida pagada.
    margen = trozo_no - COSTE_MEDIDO_WORKER_USD
    check("P13b · queda margen sobre el PEOR worker medido... pero es fino",
          margen > 0,
          "margen $%.6f = %.2f llamadas estimadas (una vuelta de mas ya corta)"
          % (margen, margen / w.COSTE_ESTIMADO_LLAMADA_USD))

    # P14 · LA CAUSA CRUZA LA FRONTERA HACIA ARRIBA (2º pendiente de C.2).
    #       Ayer subía `{"error": "No se pudo consultar USD."}` sin causa, y el
    #       modelo se inventó una: «limitaciones en el servicio».
    def _worker_cortado(encargo, nombre="x", presupuesto_usd=None, verboso=True, **kw):
        return {"ok": False, "texto": "(me detuve: se acabo el presupuesto)",
                "coste_usd": 0.0, "vueltas": 1, "llamadas_api": 1,
                "entrada_tokens": 0, "salida_tokens": 0, "segundos": 0.0,
                "herramientas": ["tasa"], "motivo": "presupuesto",
                "worker": nombre, "datos": None, "faltan": ["pesos"]}

    real2 = orquestador.worker.correr_worker
    orquestador.worker.correr_worker = _worker_cortado
    try:
        conta2 = {"capa": "orquestador", "workers": 0, "coste_workers_usd": 0.0,
                  "llamadas_api_workers": 0, "entrada_workers": 0,
                  "salida_workers": 0, "detalle": [], "reparto": None}
        subio = orquestador.herramienta_consultar_moneda(1000, "USD", conta2,
                                                         verboso=False)
        check("P14 · el fallo sube con MOTIVO, no mudo",
              subio.get("motivo") == "presupuesto",
              "motivo=%s" % subio.get("motivo"))
        # ⚠️ Y la segunda mitad, que es la que de verdad importa: el modelo no
        #    lee `motivo`, lee prosa. Si la causa no viaja en español, se la
        #    inventa igual aunque el campo exista.
        causa = (subio.get("causa") or "").lower()
        check("P14b · y con la causa EN ESPAÑOL, que es lo que el modelo repite",
              "presupuesto" in causa and "no es un fallo del servicio" in causa,
              "<<%s>>" % subio.get("causa"))
    finally:
        orquestador.worker.correr_worker = real2


    # --- P15/P16/P17: EL ENCARGO DESIGUAL, COMPROBADO ANTES DE PAGARLO ----
    # 🚨 Estas tres no comprueban el freno: comprueban **que el instrumento sirve
    #    para la pregunta**. Ayer se pagó una corrida que no podía distinguir los
    #    dos esquemas, y eso se supo DESPUÉS. Hoy se sabe antes, y es gratis.
    coste_barato = VUELTAS_ESPERADAS_BARATO * w.COSTE_ESTIMADO_LLAMADA_USD
    coste_caro = VUELTAS_ESPERADAS_CARO * w.COSTE_ESTIMADO_LLAMADA_USD
    rd = RepartoDeEntrada(total_usd=PRESUPUESTO_DESIGUAL_USD)

    # P15 · el techo NO está apretado. Si lo estuviera, el corte no probaría nada
    #       del reparto: probaría que un techo pequeño corta, que ya se sabe.
    abajo = PRESUPUESTO_DESIGUAL_USD * (1.0 - RESERVA_ARRIBA)
    # ⚠️ Y la tolerancia es de UNA MILLONÉSIMA, no de cero, porque el techo se
    #    redondea a seis decimales al declararse: comparar dos caminos hasta el
    #    mismo número con `>=` exacto es el bicho de `P4` de ayer, en pequeño.
    check("P15 · el techo DESIGUAL cubre el encargo entero (no se apretó a mano)",
          abajo >= 2 * coste_barato + coste_caro - 1e-6,
          "abajo $%.6f >= necesario $%.6f (cubre JUSTO, y a proposito)"
          % (abajo, 2 * coste_barato + coste_caro))

    # P16 · Y AUN ASÍ EL CARO NO CABE EN SU TROZO. Aquí está el defecto entero
    #       del candidato 2, en dos números: hay dinero de sobra en el encargo y
    #       el que lo necesita no puede tocarlo, porque se repartió a ciegas.
    check("P16 · pero el trozo NO cubre al caro: el culpable es el REPARTO",
          rd.trozo_nominal() < coste_caro,
          "trozo $%.6f < caro $%.6f" % (rd.trozo_nominal(), coste_caro))

    # P17 · EL NÚMERO QUE C.2 LLEVA DOS SESIONES SIN PODER ENSEÑAR: el dinero
    #       que se queda quieto en el bolsillo del que no lo necesita.
    sobrante = 2 * (rd.trozo_nominal() - coste_barato)
    check("P17 · y el desperdicio es CONTABLE: sobra en los baratos lo que le "
          "falta al caro",
          sobrante > 0 and sobrante > (coste_caro - rd.trozo_nominal()) * 0.5,
          "sobra $%.6f en los dos baratos - al caro le faltan $%.6f"
          % (sobrante, coste_caro - rd.trozo_nominal()))

    # P17b · LA RAZÓN DE DESIGUALDAD, CONTRA EL UMBRAL PUESTO DE ANTEMANO.
    #        Si el caro no es al menos 1,8x el barato, el instrumento es ciego
    #        otra vez y no hay que gastar en la corrida.
    razon = VUELTAS_ESPERADAS_CARO / VUELTAS_ESPERADAS_BARATO
    check("P17b · la desigualdad DISEÑADA pasa el umbral puesto de antemano",
          razon >= RAZON_MINIMA_UTIL,
          "%.2fx esperada >= %.2fx minima util" % (razon, RAZON_MINIMA_UTIL))

    # P18 · EL CABLE: que el encargo desigual LLEGUE al worker. Es P8 otra vez,
    #       y por el mismo motivo: una tabla correcta que nadie enchufa no hace
    #       nada, y esta vez el fallo sería invisible (los tres correrían con la
    #       frase de siempre y la corrida saldría gemela sin avisar).
    encargos_vistos = []

    def _worker_espia(encargo, nombre="x", presupuesto_usd=None, verboso=True, **kw):
        encargos_vistos.append((nombre, encargo))
        return _worker_cortado(encargo, nombre=nombre)

    real3 = orquestador.worker.correr_worker
    orquestador.worker.correr_worker = _worker_espia
    try:
        conta3 = {"capa": "orquestador", "workers": 0, "coste_workers_usd": 0.0,
                  "llamadas_api_workers": 0, "entrada_workers": 0,
                  "salida_workers": 0, "detalle": [], "reparto": None,
                  "encargos": ENCARGOS_DESIGUALES}
        for m in ("USD", "EUR", "CAD"):
            orquestador.herramienta_consultar_moneda(1000, m, conta3, verboso=False)
        largos = {n: len(e) for n, e in encargos_vistos}
        check("P18 · el encargo DESIGUAL llega al worker (usd/eur cortos, cad largo)",
              largos.get("cad", 0) > 2 * largos.get("usd", 1)
              and largos.get("usd") == largos.get("eur"),
              "largos=%s" % largos)
    finally:
        orquestador.worker.correr_worker = real3

    # =====================================================================
    # P19-P25 · C.3 — EL CONTRATO TIENE QUE RESPONDER A LO QUE SE PREGUNTÓ
    # =====================================================================
    # 🚨 LA TORCEDURA ES LA MENTIRA DE LA CORRIDA PAGADA DE LA 99, COPIADA
    #    PALABRA POR PALABRA: se pidió CAD y las herramientas trajeron USD.
    #    No es un caso inventado para lucir el detector — es el caso que ya
    #    ocurrió con dinero de verdad y que nadie cazó. `LM.13`: el detector
    #    entra con su torcedura al lado, y esta torcedura tiene factura.
    LLAMADAS_TORCIDAS = [
        {"nombre": "tasa", "entrada": {"de": "USD"},
         "salida": {"de": "USD", "tasa": 4102.5, "fuente": "mercado (open.er-api.com)",
                    "actualizado": "2026-08-20"}},
        {"nombre": "convertir", "entrada": {"de": "USD", "monto": 250},
         "salida": {"de": "USD", "monto": 250, "resultado": 1025625.0}},
    ]

    d_t, f_t, disc_t = w.contrato_divisa(LLAMADAS_TORCIDAS,
                                         pedido={"moneda": "CAD", "monto": 250})

    # P19 · LA MITAD QUE DUELE: el contrato está COMPLETO. Sin esta prueba,
    #       P20 podría estar cazando un hueco y no una contradicción.
    check("P19 · la respuesta torcida NO tiene ningun hueco (`faltan` vacio)",
          f_t == [] and d_t.get("pesos") is not None,
          "faltan=%s · pesos=%s" % (f_t, d_t.get("pesos")))

    # P20 · y AUN ASÍ se caza. Este es el detector nuevo mordiendo.
    check("P20 · pero SI discrepa: se pidio CAD y trae USD",
          bool(disc_t) and any("CAD" in x and "USD" in x for x in disc_t),
          "discrepa=%s" % disc_t)

    # P21 · NO COMPROBADO ≠ COMPROBADO Y BIEN. `None` y `[]` se ven casi igual
    #       en pantalla y significan lo contrario: es `LM.15` con dos valores.
    _, _, disc_ciego = w.contrato_divisa(LLAMADAS_TORCIDAS)
    check("P21 · sin `pedido` el contrato dice NO COMPROBADO (None), no [] ",
          disc_ciego is None,
          "discrepa=%r" % (disc_ciego,))

    # P22 · Y EL DETECTOR TIENE QUE CALLARSE CUANDO TODO CUADRA. Un detector
    #       que siempre grita no distingue nada. Es la hermana de `P1`.
    _, _, disc_ok = w.contrato_divisa(LLAMADAS_TORCIDAS,
                                      pedido={"moneda": "USD", "monto": 250})
    check("P22 · con la moneda correcta el detector se CALLA (lista vacia)",
          disc_ok == [],
          "discrepa=%r" % (disc_ok,))

    # P23 · el monto también, y por el mismo motivo: un worker puede convertir
    #       100 cuando le pidieron 250 y devolver un contrato impecable.
    _, _, disc_monto = w.contrato_divisa(LLAMADAS_TORCIDAS,
                                         pedido={"moneda": "USD", "monto": 100})
    check("P23 · y el MONTO tambien se comprueba contra lo pedido",
          bool(disc_monto) and any("monto" in x for x in disc_monto),
          "discrepa=%s" % disc_monto)

    # --- P24/P25: EL CORTE DE ARRIBA. Que el contrato lo detecte no sirve de
    #     nada si el orquestador lo deja pasar igual.
    def _worker_torcido(encargo, nombre="x", presupuesto_usd=None, verboso=True,
                        pedido=None, **kw):
        datos, faltan, disc = w.contrato_divisa(LLAMADAS_TORCIDAS, pedido)
        return {"ok": True, "texto": "250 CAD son 1.025.625 pesos.",
                "coste_usd": 0.0, "vueltas": 2, "llamadas_api": 2,
                "entrada_tokens": 0, "salida_tokens": 0, "segundos": 0.0,
                "herramientas": ["tasa", "convertir"], "motivo": None,
                "worker": nombre, "datos": datos, "faltan": faltan,
                "discrepa": disc}

    real4 = orquestador.worker.correr_worker
    orquestador.worker.correr_worker = _worker_torcido
    try:
        conta4 = {"capa": "orquestador", "workers": 0, "coste_workers_usd": 0.0,
                  "llamadas_api_workers": 0, "entrada_workers": 0,
                  "salida_workers": 0, "detalle": [], "reparto": None}
        subio4 = orquestador.herramienta_consultar_moneda(250, "CAD", conta4,
                                                          verboso=False)

        # 🚨 P24 · LA APUESTA 2 DE HOY, HECHA PRUEBA. El corte viejo del
        #    orquestador es `datos.get("pesos") is None`, y aquí `pesos` ESTÁ
        #    LLENO: 1.025.625. Por ese filtro la respuesta torcida pasa entera.
        #    Hacía falta un corte propio, y esta prueba se pone roja si alguien
        #    intenta resolverlo metiendo la discrepancia dentro de `faltan`.
        check("P24 · la respuesta torcida NO SUBE: el orquestador la descarta",
              subio4.get("motivo") == "discrepancia" and "pesos" not in subio4,
              "subio=%s" % sorted(subio4.keys()))

        # P25 · y sube con causa EN ESPAÑOL, porque el modelo no lee `motivo`.
        #       Con una frase que además le prohíbe lo que hizo la 99: usar
        #       el dato de otra moneda como si fuera este.
        causa4 = (subio4.get("causa") or "").lower()
        check("P25 · con causa en espanol que dice NO uses el dato de otra moneda",
              "no corresponde" in causa4 and "otra moneda" in causa4,
              "<<%s>>" % subio4.get("causa"))

        # P26 · LA EVIDENCIA SE CONSERVA, y bajo un nombre que nadie confunde
        #       con un resultado bueno. El hallazgo de la 99 salió de poder
        #       leer QUÉ había subido: tirarlo es tirar la prueba del delito.
        check("P26 · el dato descartado se conserva como `descartado`, no `datos`",
              subio4.get("descartado", {}).get("moneda") == "USD",
              "descartado=%s" % subio4.get("descartado"))
    finally:
        orquestador.worker.correr_worker = real4

    w.REGISTRO, orquestador.REGISTRO = _reg_w, _reg_o

    print()
    if fallos:
        print(f"XX  {len(fallos)} en rojo: {', '.join(fallos)}")
    else:
        print("OK  todas en verde")
    return fallos


# ---------------------------------------------------------------------------
# 4) LA FORMA ESPERADA DE LA CORRIDA PAGADA — escrita y commiteada ANTES de pagar
# ---------------------------------------------------------------------------
# 🚨 EL ORDEN ES LA DEFENSA, NO LA BUENA INTENCIÓN. Contra un sesgo de
#    confirmación no vale prometer que se mirará con cuidado: vale que la
#    comprobación sea ANTERIOR al dato y que se pueda ver en el orden de los
#    commits. Es lo que hizo el paso 4 de C.1 y volvió a cobrar.
#
# ⚠️ Y estas funciones NO lanzan nada. Lo que cuesta dinero se pide con todas las
#    letras y se hace una vez; leer el resultado es gratis y se repite.

def comprobar_apretada(r, verboso=True):
    """Las afirmaciones de la corrida CON el presupuesto que tiene que morder.

    Traduce a máquina la apuesta 1 del sobre: *«cuando el freno muerda, el
    encargo no fallará: volverá a medias»*.
    """
    dichos = []

    def afirmar(n, texto, cond, detalle=""):
        dichos.append((n, texto, bool(cond), detalle))

    cortados = [d for d in r.get("detalle_workers", [])
                if d.get("motivo") == "presupuesto"]
    detalle = r.get("detalle_workers", [])

    afirmar(1, "AL MENOS UN WORKER CORTA POR PRESUPUESTO (el freno muerde)",
            len(cortados) >= 1,
            f"{len(cortados)} de {len(detalle)} cortados")

    afirmar(2, "el orquestador NO revienta: entrega un texto",
            bool((r.get("texto") or "").strip()),
            f"{len((r.get('texto') or '').strip())} caracteres")

    afirmar(3, "el total se queda DENTRO del techo del encargo",
            r.get("dentro_del_presupuesto") is True,
            f"${r.get('coste_total_usd', 0):.6f} de "
            f"${r.get('presupuesto', {}).get('total_usd', 0):.6f}")

    # El corte estaba predicho en la llamada 3, porque el trozo da para 1,5.
    afirmar(4, "el corte cae DESPUÉS de la 1ª llamada, no en la puerta",
            all(d.get("llamadas_api", 0) >= 1 for d in cortados),
            f"llamadas de los cortados: {[d.get('llamadas_api') for d in cortados]}")

    afirmar(5, "el reparto sigue cuadrando al final de la corrida",
            r.get("presupuesto", {}).get("cuadra") is True)

    # ⚠️ LA 6 ES LA QUE DE VERDAD SE QUIERE MIRAR, Y ES LA MÁS DÉBIL DE LAS SEIS.
    #    «¿avisa de que está incompleta?» no es un campo: es prosa. Se comprueba
    #    por palabras, y eso puede dar un falso verde (dice "no se pudo" por otra
    #    cosa) o un falso rojo (avisa con otras palabras). **Queda declarado como
    #    indicio, no como veredicto**, y el veredicto lo pone la lectura a ojo.
    texto = (r.get("texto") or "").lower()
    avisos = ("no se pudo", "no pude", "no fue posible", "incompleto",
              "incompleta", "falta", "no se obtuvo", "sin dato", "no disponible")
    afirmar(6, "INDICIO (no veredicto): la respuesta AVISA de que va incompleta",
            any(a in texto for a in avisos),
            f"encontrado: {[a for a in avisos if a in texto] or 'ninguno'}")

    if verboso:
        _imprimir_afirmaciones("CORRIDA APRETADA — el freno tiene que MORDER", dichos)
    return dichos


def comprobar_normal(r, verboso=True):
    """Las afirmaciones de la corrida con presupuesto NORMAL.

    Es `P1` en el mundo real, y es la obligación sellada esta mañana: **el freno
    tiene que callarse**. Sin esta corrida, "no muerde en operación normal" es
    una prueba de aritmética, no un hecho.
    """
    dichos = []

    def afirmar(n, texto, cond, detalle=""):
        dichos.append((n, texto, bool(cond), detalle))

    detalle = r.get("detalle_workers", [])
    cortados = [d for d in detalle if d.get("motivo") == "presupuesto"]

    afirmar(1, "NINGÚN worker corta por presupuesto (el freno SE CALLA)",
            len(cortados) == 0,
            f"{len(cortados)} cortados de {len(detalle)}")

    afirmar(2, "el orquestador tampoco corta",
            r.get("motivo") != "presupuesto",
            f"motivo={r.get('motivo')}")

    afirmar(3, "el total se queda DENTRO del techo del encargo",
            r.get("dentro_del_presupuesto") is True,
            f"${r.get('coste_total_usd', 0):.6f} de "
            f"${r.get('presupuesto', {}).get('total_usd', 0):.6f}")

    afirmar(4, "los TRES workers arrancaron y ninguno se quedó sin trozo",
            len(detalle) == N_WORKERS_ESPERADOS
            and not r.get("presupuesto", {}).get("rechazados"),
            f"{len(detalle)} workers · rechazados="
            f"{r.get('presupuesto', {}).get('rechazados')}")

    afirmar(5, "y sobra dinero: el techo NO estaba pegado al gasto",
            r.get("coste_total_usd", 1e9)
            < r.get("presupuesto", {}).get("total_usd", 0),
            f"margen ${r.get('presupuesto', {}).get('total_usd', 0) - r.get('coste_total_usd', 0):.6f}")

    if verboso:
        _imprimir_afirmaciones("CORRIDA NORMAL — el freno tiene que CALLARSE", dichos)
    return dichos


def comprobar_desigual(r, verboso=True):
    """Las afirmaciones de la corrida DESIGUAL — la obligación del sobre.

    🎯 Lo que se mira aquí NO es si el freno muerde. Eso ya se midió ayer y da
       igual. Lo que se mira es **si el reparto ciego desperdicia**, y ésa es la
       pregunta que la tarea gemela no podía responder.

    ⚠️ Y la afirmación que decide es la 3, no la 1. Que el caro corte es la
       mitad barata; lo que acusa al esquema es que corte **mientras hay dinero
       parado en el bolsillo de los otros dos**.
    """
    dichos = []

    def afirmar(n, texto, cond, detalle=""):
        dichos.append((n, texto, bool(cond), detalle))

    detalle = r.get("detalle_workers", [])
    porw = {d.get("worker"): d for d in detalle}
    caro = porw.get("cad", {})
    baratos = [porw[k] for k in ("usd", "eur") if k in porw]
    pres = r.get("presupuesto", {})
    trozo = pres.get("trozo_usd", 0.0)

    afirmar(1, "EL CARO (cad) corta por presupuesto",
            caro.get("motivo") == "presupuesto",
            "motivo=%s - %s llamadas" % (caro.get("motivo"), caro.get("llamadas_api")))

    afirmar(2, "los DOS baratos (usd, eur) terminan bien",
            len(baratos) == 2 and all(b.get("motivo") is None for b in baratos),
            "motivos=%s" % [b.get("motivo") for b in baratos])

    # 🚨 LA QUE IMPORTA. El desperdicio, en dólares y contable.
    sobrante = sum(max(0.0, trozo - b.get("coste_usd", 0.0)) for b in baratos)
    afirmar(3, "🚨 HAY DINERO PARADO EN LOS BARATOS MIENTRAS EL CARO SE AHOGA",
            sobrante > 0,
            "sin usar en usd+eur: $%.6f (el caro se paro en $%.6f de $%.6f)"
            % (sobrante, caro.get("coste_usd", 0.0), trozo))

    # Y la comparación que separa los dos esquemas de una vez:
    # con TOPE POR PIEZA ($0,05 cada uno) el caro NO habría cortado.
    afirmar(4, "y con el TOPE POR PIEZA de ayer el caro NO habría cortado",
            caro.get("coste_usd", 0.0) < 0.05,
            "el caro gasto $%.6f, muy por debajo del viejo tope $0,050000"
            % caro.get("coste_usd", 0.0))

    afirmar(5, "el total sigue DENTRO del techo del encargo",
            r.get("dentro_del_presupuesto") is True,
            "$%.6f de $%.6f" % (r.get("coste_total_usd", 0),
                                pres.get("total_usd", 0)))

    afirmar(6, "el reparto sigue cuadrando al final",
            pres.get("cuadra") is True)

    # ⚠️ INDICIO, no veredicto — declarado débil ANTES de correr, como ayer.
    #    Es la apuesta 2: darle la causa al modelo debería quitarle la causa
    #    inventada. Se comprueba por palabras, y buscar palabras ya dio un falso
    #    rojo una vez.
    texto = (r.get("texto") or "").lower()
    culpas_ajenas = ("servicio", "proveedor", "api", "no disponible",
                     "limitacion", "limitación")
    palabras_dinero = ("presupuesto", "límite", "limite", "coste", "costo")
    afirmar(7, "INDICIO: la respuesta NO culpa a un tercero del fallo",
            not any(c in texto for c in culpas_ajenas),
            "encontrado: %s" % ([c for c in culpas_ajenas if c in texto] or "nada"))
    afirmar(8, "INDICIO: y SÍ nombra el dinero como causa",
            any(pl in texto for pl in palabras_dinero),
            "encontrado: %s" % ([pl for pl in palabras_dinero if pl in texto] or "nada"))

    # La báscula del techo arreglado, en la corrida de verdad.
    cortas = r.get("estimaciones_cortas", 0) + sum(
        d.get("estimaciones_cortas", 0) for d in detalle)
    afirmar(9, "el techo arreglado NO se pasó: ninguna estimación se quedó corta",
            cortas == 0, "estimaciones cortas: %s" % cortas)

    if verboso:
        _imprimir_afirmaciones(
            "CORRIDA DESIGUAL — el REPARTO tiene que enseñar su defecto", dichos)
    return dichos


def _imprimir_afirmaciones(titulo, dichos):
    print("\n" + "-" * 70)
    print(titulo)
    print("-" * 70)
    for n, texto, ok, detalle in dichos:
        print(("  OK  " if ok else "  XX  ") + f"{n}. {texto}"
              + (f"  -> {detalle}" if detalle else ""))
    rojas = [n for n, _, ok, _ in dichos if not ok]
    print(f"\n  {len(dichos) - len(rojas)} de {len(dichos)} cumplidas"
          + (f" · en rojo: {rojas}" if rojas else ""))


def informe_de_hoy():
    """Lo que C.2 puede decir en voz alta, y ayer no."""
    r = RepartoDeEntrada()
    a = RepartoDeEntrada(total_usd=PRESUPUESTO_APRETADO_USD)
    print("\n[C.2] EL PRESUPUESTO DEL ENCARGO\n")
    print(f"  «este encargo no puede costar más de ${r.total_usd:.6f}»")
    print(f"     = ${COSTE_MEDIDO_ENCARGO_USD:.6f} medido x {HOLGURA} de holgura")
    print(f"  arriba (orquestador):  ${r.arriba_usd:.6f}   ({int(RESERVA_ARRIBA*100)} %)")
    print(f"  cada worker:           ${r.trozo_nominal():.6f}   x {r.n_workers}")
    print(f"\n  ayer el techo era $0,200000 - y nadie lo había elegido.\n")
    d = RepartoDeEntrada(total_usd=PRESUPUESTO_DESIGUAL_USD)
    print(f"  presupuesto APRETADO (el que muerde): ${a.total_usd:.6f}")
    print(f"     cada worker: ${a.trozo_nominal():.6f}  ~ "
          f"{a.trozo_nominal()/COSTE_LLAMADA_WORKER_USD:.2f} llamadas al modelo")

    # --- Y la tercera, que es la que mide el REPARTO y no el freno.
    caro = VUELTAS_ESPERADAS_CARO * worker.COSTE_ESTIMADO_LLAMADA_USD
    barato = VUELTAS_ESPERADAS_BARATO * worker.COSTE_ESTIMADO_LLAMADA_USD
    print()
    print(f"  presupuesto DESIGUAL (el que mide el REPARTO): ${d.total_usd:.6f}")
    print(f"     cada trozo: ${d.trozo_nominal():.6f}   (ciego, a partes iguales)")
    print(f"     el caro (cad) necesita ${caro:.6f}  -> NO le cabe, corta")
    print(f"     cada barato necesita   ${barato:.6f}  -> le sobran "
          f"${d.trozo_nominal() - barato:.6f}")
    print()
    print(f"  🚨 hay ${2 * (d.trozo_nominal() - barato):.6f} parados en los "
          f"baratos, y al caro le faltan ${caro - d.trozo_nominal():.6f}.")
    print(f"     El encargo TIENE el dinero. El que lo necesita no puede tocarlo.")
    print(f"     Eso es el reparto ciego, y con tres encargos gemelos era invisible.")


def correr_pagado(apretado, verboso=True, desigual=False):
    """LANZA UNA CORRIDA DE VERDAD. Cuesta dinero. Se pide a mano.

    `apretado=True`   -> el presupuesto que tiene que morder (~$0,014 de techo)
    `apretado=False`  -> el presupuesto normal               (~$0,040 de techo)
    `desigual=True`   -> la obligación del sobre: encargos DISTINTOS entre
                         workers y un techo que cubre el encargo ENTERO
                         (~$0,079). Aquí no se mide el freno: se mide el REPARTO.
    """
    import orquestador
    import fan_out

    if desigual:
        total = PRESUPUESTO_DESIGUAL_USD
    else:
        total = PRESUPUESTO_APRETADO_USD if apretado else PRESUPUESTO_ENCARGO_USD
    rep = orquestador.presupuesto.RepartoDeEntrada(total_usd=total)

    etiqueta = "DESIGUAL" if desigual else ("APRETADO" if apretado else "NORMAL")
    print("\n" + "=" * 70)
    print(f"CORRIDA PAGADA · presupuesto {etiqueta} · techo ${rep.total_usd:.6f}")
    print(f"  arriba ${rep.arriba_usd:.6f} · cada worker ${rep.trozo_nominal():.6f}")
    print("=" * 70)

    # Se corre en PARALELO a propósito: es la topología donde el reparto tiene
    # que entregar tres trozos a tres hilos a la vez, y donde el candado del
    # reparto se gana el sueldo o no se lo gana.
    fan_out.reiniciar_linea_de_tiempo()
    r = orquestador.correr_orquestador(orquestador.TAREA_DEMO,
                                       verboso=verboso,
                                       reparto=fan_out.reparto_en_paralelo,
                                       presupuesto_encargo=rep,
                                       encargos=(ENCARGOS_DESIGUALES
                                                 if desigual else None))

    print("\n" + "-" * 70)
    print(f"RESPUESTA FINAL ({etiqueta})")
    print("-" * 70)
    print(r["texto"])
    print(f"\n  arriba: ${r['coste_orquestador_usd']:.6f} · "
          f"abajo: ${r['coste_workers_usd']:.6f} · "
          f"TOTAL: ${r['coste_total_usd']:.6f}  (techo ${rep.total_usd:.6f})")
    print("  workers: " + " · ".join(
        f"{d['worker']}={d['motivo'] or 'terminó'}({d['llamadas_api']} llamadas)"
        for d in r["detalle_workers"]))

    if desigual:
        comprobar_desigual(r)
    else:
        (comprobar_apretada if apretado else comprobar_normal)(r)
    return r


if __name__ == "__main__":
    import sys

    if "--pagar-desigual" in sys.argv:
        # 💸 LA OBLIGACIÓN DEL SOBRE. UNA sola corrida, y mide el REPARTO — no
        #    el freno. Va aparte de `--pagar` a propósito: son dos preguntas
        #    distintas y se pagan por separado, para poder decidir una sin la
        #    otra.
        d = correr_pagado(apretado=False, desigual=True)
        print()
        print("=" * 70)
        print(f"GASTO DE LA CORRIDA DESIGUAL: ${d['coste_total_usd']:.6f}")
        print("=" * 70)
        sys.exit(0)

    if "--pagar" in sys.argv:
        # 💸 Las DOS corridas, en el orden que importa: primero la apretada
        #    —la barata y la que puede fallar— y después la normal.
        a = correr_pagado(apretado=True)
        n = correr_pagado(apretado=False)
        print("\n" + "=" * 70)
        print(f"GASTO DE LAS DOS CORRIDAS: "
              f"${a['coste_total_usd'] + n['coste_total_usd']:.6f}")
        print("=" * 70)
        sys.exit(0)

    informe_de_hoy()
    print("\n💸 Las TRES corridas pagadas NO corrieron. Para correrlas:")
    print("   python presupuesto.py --pagar             (apretada + normal)")
    print("   python presupuesto.py --pagar-desigual    (la del REPARTO)")
    sys.exit(1 if _pruebas() else 0)
