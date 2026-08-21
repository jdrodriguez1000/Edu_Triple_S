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
COSTE_LLAMADA_WORKER_USD = 0.002404   # media de las dos llamadas de la demo C.1

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

    Con `llamadas_permitidas=1.5` la predicción es mecánica y falsable:
      · llamada 1 -> gastado ~ $0,0024, por debajo del trozo -> pasa
      · llamada 2 -> gastado ~ $0,0048, por encima del trozo -> LA 3 SE BLOQUEA

    🔑 Por eso el corte cae DESPUÉS de tener la tasa y ANTES de redactar: el
       worker vuelve a medias, que es justo lo que la apuesta 1 quiere mirar.
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
    check("P2b · pero SÍ llega a una: el corte cae en la 3a, no en la 1a",
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
    print(f"  presupuesto APRETADO (el que muerde): ${a.total_usd:.6f}")
    print(f"     cada worker: ${a.trozo_nominal():.6f}  ~ "
          f"{a.trozo_nominal()/COSTE_LLAMADA_WORKER_USD:.2f} llamadas al modelo")


def correr_pagado(apretado, verboso=True):
    """LANZA UNA CORRIDA DE VERDAD. Cuesta dinero. Se pide a mano.

    `apretado=True`  -> el presupuesto que tiene que morder  (~$0,014 de techo)
    `apretado=False` -> el presupuesto normal                (~$0,040 de techo)
    """
    import orquestador
    import fan_out

    total = PRESUPUESTO_APRETADO_USD if apretado else PRESUPUESTO_ENCARGO_USD
    rep = orquestador.presupuesto.RepartoDeEntrada(total_usd=total)

    etiqueta = "APRETADO" if apretado else "NORMAL"
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
                                       presupuesto_encargo=rep)

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

    (comprobar_apretada if apretado else comprobar_normal)(r)
    return r


if __name__ == "__main__":
    import sys

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
    print("\n💸 Las dos corridas pagadas NO corrieron. Para correrlas:")
    print("   python presupuesto.py --pagar")
    sys.exit(1 if _pruebas() else 0)
