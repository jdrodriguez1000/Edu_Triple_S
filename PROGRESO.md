# PROGRESO — Bitácora del curso

> Este es el archivo de memoria del curso. Claude lo lee al empezar cada sesión y lo
> actualiza al terminar. Tú también puedes escribir aquí lo que quieras.

**Última actualización:** 2026-08-18 (sesión 83)

---

# 📍 NIVEL 7 — PRODUCCIÓN. **Los frenos existen antes de que haya nada que frenar.**
# **Paso 6 CERRADO** en la sesión 38. La 39 pagó tres deudas sin tocar la nube.
# La 40 cerró la PLATAFORMA. La 41 **escribió `deploy/` entera antes de abrir la
# cuenta**. La 42 **midió desde fuera lo que la otra terminal dio por no medible**:
# `T-058` cerrada y comprobada por DNS. **$0,00** y la cuenta **sigue sin abrirse**.
# La 43 **no tocó código ni la nube**: fijó qué es ser senior con agentes, **qué
# información necesita la terminal que supervisa**, y registró **su método
# profesional de brief a MVP** — sin construirlo, porque falta contarlo entero.
# La 44 **tampoco tocó código**: cómo se corta el trabajo (feature, vertical
# slice, walking skeleton, tracer bullet, MVP en diagonal, cuánta arquitectura
# antes de teclear) → `LM.6`–`LM.11`. **El paso 7 de su método dejó de estar
# vacío.** La 45 **corrigió `LM.8` con un dato suyo** —su prototipo es desechable
# y puede no ser código— y de ahí salió **`LM.12`: en un producto de IA el
# wireframe valida la idea, no el producto.** Ver abajo.
# 🚨 **La 46 ABRIÓ LA CUENTA DE AWS (`T-057`) — el reloj de 6 meses ARRANCÓ el
# 2026-08-06 y vence el 2027-02-06.** Esta terminal auditó el historial público y
# está limpio. De la auditoría salió `LM.13`: **un freno que no has visto morder
# es una nota, no un freno.** Y de ahí, todo el día: la alarma se examinó, esta
# terminal **se equivocó y la otra la corrigió con una pantalla**, la región se
# cazó **antes** de decidirse sola, y `T-059` quedó **partida** con un
# experimento corriendo y la predicción **sellada en Git antes del clic**.
# ⏳ **Se espera con dos datos: la factura y la bandeja.** Primeros céntimos
# gastados del curso.
# 🚨 **La 47 no pudo leer el experimento —el dato de facturación tarda ~24 h— y
# adelantó lo que no toca la nube: `T-055` MEDIDA con uvicorn real y `T-052`
# cerrada.** De 310 a 314 tests. Y salió `LM.14`, que es **la otra mitad de
# `LM.4`**: esta terminal entregó un dato falso y lo cazó la que construye.
# 🚨 **La 48 cerró `T-054` —el tope de cuerpo de Caddy, ahora MEDIDO— sin tocar la
# nube ni gastar un centavo.** De 314 a 328 tests. Salió **`LM.15`, la más fuerte
# de estas tres sesiones**: un instrumento ciego no da un dato falso, da
# **silencio**, y el silencio se lee como confirmación. Tercera cara en dos
# sesiones del mismo defecto — **nadie audita un verde**.
# 🚨 **La 49 cerró `T-071`** —el aislamiento del marcador, arreglado en el ORIGEN
# (`app/tools.py`) y vigilado por un **portero sobre `data/` entera**— de 328 a
# **329 tests**, sin nube y sin gastar. Cuarta seguida así. Y el saldo del día no
# fue la trampa: **de mirar cinco fechas salió `A-020`, un camino que escribe en
# los datos de verdad POR FUERA de pytest.** Dos lecciones: **`LM.16`** (una
# salvedad correcta no arregla un titular falso) y **`LM.17`** (un `md5` no dice
# "todo igual", dice "los bytes, iguales" — y se llevó por delante la prueba).
# 🚨 **La 50 resolvió `T-072` en dos minutos y el culpable era de casa: el
# instrumento de medida.** El camino que escribía en `data/` real era
# `measure_body.py`, la báscula de `T-054` de la sesión 48 — desvió UNO de los
# TRES sitios. De ahí salió **`D-037`**: la raíz de los datos sale de
# `TEAPP_DATA_DIR`, **absoluta y sin valor por defecto**, y sin ella la app no
# arranca. De 329 a **342 tests**. Quinta seguida sin nube y sin gastar.
# 🚨 **La 51 abrió con "no hay nada que hacer sin la nube" y cerró con cinco
# artefactos**: `install.sh` corrió por primera vez —en un contenedor Ubuntu, no
# en EC2—, el freno de `T-050` **se vio morder**, y `A-019` murió con el borde
# del `413` de Caddy medido en **16000/16001**. De 342 a **348 tests**. Sexta
# seguida sin nube. De ahí `LM.19`: **la lista de pendientes dice qué falta por
# construir, nunca dijo qué falta por saber** — y la reserva estaba en `A-xxx`.
# ⚠️ **Dos errores de ESTA terminal, los dos medidos por la otra:** recomendó
# `T-068`, cerrada hacía cinco sesiones; y afirmó que invertir la precedencia
# rompería la suite (falso: 346 verdes, `data/` intacta). El miedo tenía blanco,
# pero **fuera de pytest** — que es donde vivía `T-072`. → `LM.20`: la corrección
# de `T-068` **ya estaba escrita en este archivo** y nadie la alcanzó.
# ⏳ **El experimento de `A-018` SIGUE SIN LEERSE, y ahora se sabe por qué:** el
# reloj de las 24 h cuelga de **la primera visita a la consola**, no del cargo.
# El `0,00 USD` de la página de Facturas viene con `Sin datos`: **no es un cero
# medido**, y se disfraza de la fila 3 de la tabla sellada.
# 🚨 **La 52 fue de SUPERVISIÓN, y encontró que la tabla sellada de `A-018` decía
# algo FALSO.** La fila 3 no decía solo "no concluyente": nombraba una causa —
# *"las horas de IPv4 aplican"*— que la otra terminal **desmintió esa misma
# mañana sin ver lo que estaba matando**. Verificado aquí en la fuente de AWS:
# *"no change in pricing for idle public IPv4 addresses"*. Enmienda **sellada
# antes de la lectura** → `LM.21`: **un sello protege de decidir tarde, no de que
# el mundo desmienta lo que sellaste.** Era lo único con fecha de caducidad.
# ⚠️ **Y de un reparo mío sobre la fila 2 salió algo peor de lo que planteaba:**
# los presupuestos se refrescan 3 veces al día (8–12 h). La guardia se queda, pero
# su motivo escrito cambió — *no sabemos si lo que se muestra y lo que se evalúa
# comparten reloj*. **Regla correcta, razón que podía no serlo: `D-039` con el
# signo cambiado.** Y la espera se convirtió en dato: `h2 − h1`, gratis.
# ✅ **`T-060a` HECHA** (el grupo de seguridad, `us-east-1`, sin 8000), partida en
# `a`/`b` por esta terminal: existir no es morder. La octava puerta salió de
# `T-068` y pasó al protocolo de lectura → `LM.22`: **el riesgo se mide por el
# tráfico, no por lo peligrosa que es la puerta.**
# 📎 **Y DESPUÉS del cierre salieron tres cosas** (ver el apéndice de la 52): un
# error mío —di por existente un aparejo Caddy+uvicorn que eran dos procesos
# sueltos: **tercera cara del mismo bicho en un día, de tres dueños distintos**—;
# **`T-055` amaneció costando una máquina y se acostó costando cero**; y `LM.23`,
# marcada por la otra terminal sola: **medido no es lo mismo que anotado.**
# 🔒 **La 53 paró un lanzamiento.** La otra terminal recomendó hacer hoy la segunda
# mitad de `T-059` (la EC2) — y el freno que lo impedía **estaba escrito por ellos
# mismos** en `tasks.md`: *"no se hace todavía a propósito"*. `LM.20` por segunda
# vez en tres sesiones. Se revisó si el freno seguía valiendo y **sí**: lanzar hoy
# mata `t_cargo − t=0`, la medición irrepetible que sirve seis meses; enciende lo
# primero que puede quemar los $200 **con la alarma sin verificar** (`LM.13`); y el
# ahorro iba al revés (una EC2 24/7 cuesta más bruto que la IP ociosa). **Esperar
# un día cuesta ~$0,12.** Decisión suya con los tres costos delante: **esperar.**
# 🔒 **Y la espera quedó SELLADA HOY, con fecha de caducidad:** la lectura del
# 2026-08-08 **es el límite** — diga lo que diga, después se lanza `T-059`. Si
# sigue `0,00`, eso es la **causa (b)** y es un hallazgo, no una excusa. Se sella
# hoy porque mañana, con el número delante, *"un día más"* vuelve a parecer
# razonable. Es `D-040` aplicado a la decisión, no a la lectura.
# ✅ **La Elastic IP dejó de ser decisión suelta:** no se suelta (mataría el
# generador) y se asocia mañana, que es la segunda mitad de `T-059`. Dos pendientes
# que eran una.
# 🐛 **Y el informe de la otra terminal traía dos datos viejos:** dijo 342 tests
# (**son 348**, corridos aquí) y llamó *"segunda lectura"* a un día en que ya había
# hecho la **tercera** (`1c3118d`, 11:13) — la que encontró el **cuarto reloj**,
# que era justo el argumento a favor de esperar.
# 🟢 **La 54 leyó el experimento y APARECIÓ EL PRIMER CARGO** — pero no donde se
# le esperaba: widget `Resumen de Costos` → `Costo Acumulado Mensual` = **0,12 US$**,
# con `Importe utilizado` **todavía en 0,00**. **Mata la causa (b)**: hay dinero
# visible, nada lo absorbe. Y la predicción de la 51 (`23 h × $0,005 ≈ $0,12`),
# escrita antes de medir, **acertó**.
# 🚨 **Y el sello `D-041` FALLÓ en su primera prueba: el 08 cerró SIN lanzar
# `T-059`.** No falló como se temía —nadie dijo *"esperemos un día más"*— sino de
# una forma que el sello no cubría: **las dos sesiones del día se acabaron antes de
# llegar al clic.** Un sello protege de un argumento; **no protege de que se agote
# la sesión.** → candidata a `LM.24`, que se escribe en TEAPP, no aquí.
# 🐛 **El documento de la otra terminal es BUENO y su RESUMEN es peor que él.**
# `A-018` marcó sola lo que había que marcar (que `h1` no ha ocurrido, que la hora
# de aparición se perdió, la aritmética como *de lista*, bruto/neto sin verificar y
# por qué no importa, y que esto **ejecuta** `D-040` en vez de violarlo). Pero el
# resumen que llegó al estudiante **borró el motivo (2) de `D-041`** —*la alarma no
# ha mordido*, en negrita y con sirena en el documento— y **reabrió una espera sin
# fecha de caducidad** (*"hasta que deje de ser 0,00"*), que es justo lo que
# `D-041` prohibió. → **`LM.20` por TERCERA vez en cuatro sesiones**, con una vuelta
# nueva: la razón no solo estaba escrita, **estaba escrita por quien informó.**
# 🚀 **La 55 LANZÓ LA MÁQUINA. `T-059` cerrada del todo: TEAPP tiene por primera
# vez un servidor propio en internet** (`t3.micro`, Ubuntu Server 24.04 LTS,
# Elastic IP asociada, DuckDNS resolviendo). **Décima sesión sin código de la app,
# y la primera que enciende algo.** El orden invertido funcionó: `T-059` fue lo
# primero y por eso ocurrió.
# ✅ **Y esta terminal MIDIÓ DESDE FUERA la cadena que la otra dio por no
# verificable** — `session-closer` lo marcó honradamente como *"reportado, no
# visto"*, pero añadió *"si algo no cuadra, saldrá mañana por SSH"*, aplazando a
# mañana una comprobación de doce segundos. **Es la sesión 42 por segunda vez**
# (`T-058`: *"nada que verificar"*, y era `nslookup`).
# 🔬 **`T-060b` NO estaba bloqueada por `T-062`, y ya está medida su primera
# mitad.** El commit razonaba con `L-020` —*nada escucha en el 8000, un escaneo
# saldría cerrado igual*— y era `L-020` bien aplicada, pero **tenía cura: el
# control al lado**, que es el método de la sesión 8. 🔑 **`RECHAZADO` y `TIMEOUT`
# no son la misma palabra:** el 80 y el 443 devuelven `RST` (permitidos, nada
# detrás) y el 8000 no devuelve nada (descartado). Contra ese control, **el
# silencio del 8000 sí es un dato**. Falta la otra mitad —que uvicorn se ate a
# `127.0.0.1`— y esa sí espera a `T-062`.
# ⚠️ **Dos trampas del formulario cazadas ANTES del clic, y ninguna estaba en la
# lista de las 7 puertas:** el punto 5 del guion decía *"reservar y asociar"* la
# Elastic IP —escrito cuando no existía— y seguirlo habría alquilado una **segunda
# dirección, que es justo la que cobra**; y el desplegable de AMI ofrecía
# **Ubuntu Pro**, que se factura por hora y habría hecho `A-018` ilegible al
# mezclar dos fuentes de gasto. → `L-028` y `D-043` en TEAPP.
# 🚨 **Y desde hoy la cuenta tiene DOS fuentes de gasto**, no una: la IP elástica y
# la máquina encendida. **`A-018` sigue vivo pero ya no se puede atribuir el
# importe a la IP sola.** El experimento perdió su aritmética limpia el día que
# cumplió su objetivo.
# 🚀 **La 56 (mismo día) PUSO TEAPP EN PRODUCCIÓN.** `install.sh` corrió por primera
# vez en una máquina de verdad. Verificado **desde esta terminal, no reportado**:
# `https://teapp.duckdns.org` → **200 en 5 de 5**, certificado Let's Encrypt válido
# (`Aug 8 16:55 → Nov 6 16:55 UTC`), el 80 redirige con **308**, `/me` sin cookie
# → **401**, y las cabeceras dicen `Server: uvicorn` + `Via: 1.1 Caddy` — **el
# aparejo existe de verdad**, que es justo el error que cometí en la 52.
# `T-061`, `T-062`, `T-060b`, `T-064` y `T-065` cerradas.
# 🔬 **`T-060b`: tenían razón ellos y yo estaba equivocado.** Sostuve que el escaneo
# ya estaba hecho por la mañana. Su respuesta es mejor: con **nada** escuchando en
# el 8000, "cerrado" sale igual con el cortafuegos abierto o cerrado. Ahora hay un
# proceso real detrás y sigue sin alcanzarse desde fuera → **el control se vio
# morder**. (Matiz que sí queda: el contraste `RST` vs `TIMEOUT` de la mañana no era
# `L-020` puro, distinguía "descarta" de "no hay nadie" — pero era inferencia sobre
# el grupo de seguridad, no la cadena entera. La medida de hoy la subsume.)
# 🌐 **El parpadeo de DuckDNS me pasó A MÍ, sin buscarlo y sin saber que ellos lo
# habían visto:** `curl: (6) Could not resolve host` mientras el puerto 80 respondía
# `308` en el mismo instante. **Dos observadores independientes, dos redes, mismo
# fenómeno.** `A-017` deja de ser un riesgo leído y pasa a tener dos testigos.
# 🐛 **Y ME EQUIVOQUÉ EN EL DIAGNÓSTICO DEL CIERRE, que es lo que hay que recordar
# de hoy.** Cacé bien el síntoma —`decisions.md` modificado y sin commitear, con
# `D-044` dentro (la máquina se queda encendida, **con caducidad de una noche**)— y
# lo diagnostiqué como *"el control se cumplió entero y no comprobó lo que creías"*,
# o sea la sesión 33 otra vez. **Falso.** Los `mtime` lo desmienten:
# `progress.md` 13:16:52 → commit **13:17:05** → `decisions.md` **13:37:41**.
# **A la hora del cierre el árbol estaba limpio.** `D-044` nació veinte minutos
# después. 🔑 **Deduje una cronología teniendo la báscula a un comando de
# distancia** — es la sesión 42 (*"no hay nada que verificar"*, y era `nslookup`)
# conmigo de protagonista, y el mismo día en que yo les corregí las 15:08 por
# heredar un número sin ir a la fuente.
# ✅ **El reencuadre bueno lo pusieron ellos, y es nuevo: `L-029` — lo que nace
# DESPUÉS del cierre no tiene dueño.** El `session-closer` corre una vez y el commit
# del día ya está hecho. No es un accidente raro: en este proyecto **las decisiones
# buenas salen conversando después** de que el trabajo técnico acabó.
# ⚖️ **Lo único que sí les discutí y gané:** querían aplazar `L-029` a mañana *"por
# no ensuciar el árbol recién limpio"*. Es el hallazgo aplicándose a sí mismo — una
# lección sobre trabajo huérfano, dejada huérfana. Se escribió en el momento
# (`0dfdbba`). 📌 **El árbol limpio no es el objetivo del protocolo, es su efecto
# secundario.**
# ✅ **Y no hubo fuga:** la contraseña de `jorge` se generó en la máquina, no por el
# chat. Rastreado el repo entero: ni la clave ni un hash entraron. `create_account.py`
# la toma por **variable de entorno**, y hay un test que **rechaza** pasarla como
# argumento (que quedaría en el historial del shell y en la lista de procesos).
# 🚀 **La 57 (día siguiente) CERRÓ LAS DOS TAREAS QUE LLEVABAN BLOQUEADAS DESDE EL
# 4 DE AGOSTO**, y las dos con medida real, no con `curl`: `T-051` (la cookie
# `Secure` guardada **y devuelta** por un navegador de verdad) y `T-050` (el
# redespliegue sobre la máquina viva, con la sesión de jorge sobreviviendo).
# Mueren tres suposiciones: `A-005`, `A-008` y `A-009` → `L-031` y `L-032`.
# ✅ **Verificado desde esta terminal antes de opinar de nada:** `351 passed`
# (su número era correcto), árbol limpio y sincronizado, `200` con `Server: uvicorn`
# + `Via: 1.1 Caddy`, certificado `Aug 8 → Nov 6`, el 80 en `308` y **el 8000 en
# TIMEOUT** desde fuera. Todo lo que afirmaron, cierto.
# 🌙 **`D-045` NUEVA — la máquina deja de vivir de noche:** ventana 07:00–18:00
# Colombia (12:00–23:00 UTC), **apagado automático desde dentro, encendido manual**.
# 🔑 El reparto es asimétrico a propósito: **el olvido tiene que caer del lado que
# no cobra.** Es `PERMISOS.get(nombre, "prohibir")` del nivel 4 aplicado a una
# factura. Reabre `D-029`, que había descartado esa pieza apoyándose en la holgura
# **nunca corrida** de `A-015`.
# 🚨 **Y de ahí salió el hallazgo caro del día, que era una trampa invisible:** en
# EC2 existe un ajuste —*comportamiento de apagado iniciado por la instancia*— con
# los mismos dos valores del menú, `stop` o `terminate`. El aviso de la 55 era
# *"Detener, nunca Terminar"* **con un humano leyendo la pantalla**. Una pieza
# automática ejecuta ese ajuste todas las noches **sin que nadie lea nada**: si
# estuviera en `terminate`, **destruye instancia y disco la primera noche que
# funcione, por funcionar bien.** Se exigió leerlo antes de escribir la pieza →
# **`Detener`, leído en pantalla.** 📌 Y la ruta del menú resultó no ser la
# esperada: la consola en español lo llama *"Cambiar comportamiento de CIERRE"*.
# 🐛 **ME CORRIGIERON UN COMANDO Y TENÍAN RAZÓN.** Yo dicté `shutdown -h 23:00`;
# ellos pusieron **`-P`** citando a AWS: `halt` no dispara el comportamiento, deja
# *"la CPU en HLT mientras la instancia sigue corriendo"* → **máquina muerta por
# dentro y viva para la factura, con fallo MUDO.** (Matiz: en systemd `-h` ya
# equivale a `poweroff`, así que seguramente escapábamos — pero *"seguramente"* es
# justo lo que ellos se negaron a aceptar dos párrafos antes con el ajuste
# `stop`/`terminate`. **Aplicaron su propio criterio a mi comando.**)
# 🔴 **Un choque en MIS PROPIAS LÍNEAS, cazado por ellos**, y es la lección del día
# sobre mí: escribí que la ventana no debía arrancar hasta que sonara la alarma
# *"porque apagar rompe la cuenta dinero ÷ horas de `A-018`"*. **Falso.** Lo que
# `A-018` tiene vivo son **relojes** (`h1`, `h2 − h1`), y esos no se enteran de que
# la máquina duerme: los 0,37 US$ ya están bancados y la IP cobra igual de noche.
# El daño era de **`T-067`**. 🔑 **La cautela era buena y le puse el dueño
# equivocado** — tercera vez en tres días del mismo bicho, hoy mío. Y el arreglo
# correcto no fue matizar la línea sino **borrarla y decir por qué era falsa**:
# *una regla con asterisco debajo se lee como regla; nadie baja al asterisco.*
# ✅ **Y él hizo lo correcto con el choque: lo trajo como choque.** Traía además el
# matiz que lo resolvía y **no lo metió por su cuenta.** Por eso se corrigió la
# regla en vez de parchearse.
# ➕ **El argumento que dio la vuelta a la decisión no era el mío:** `T-067` mide
# *gasto diario × 180*. Con máquina de 24 h se proyectaría **un régimen que no va a
# existir**. La ventana no le quita nada a `T-067`: **se lo da.**
# 🎁 **Y la ventana le REGALA algo a `A-018`:** las 12:00 y las 23:00 UTC pasan a
# ser **dos lecturas ancladas** del presupuesto. 🔑 **El correo se fecha solo; `h1`
# no.** Hasta hoy `h1` dependía de que a alguien le diera por mirar — y ya se
# perdió una hora así. El ritual de la ventana le pone horario al experimento.
# 🔬 **Sexta lectura de `A-018`: `Importe utilizado` sigue en 0,00 (cuarta seguida),
# `Costo Acumulado Mensual` sube a 0,37 US$.** Su cuenta —`0,37 ÷ 0,005 = 74 h`
# facturadas contra **71,3 h** que lleva viva la IP— es correcta, comprobada aquí, y
# está **bien construida**: aguanta **sin usar el precio de la `t3.micro`**, que no
# está medido. Primera vez que la EC2 se ve en pantalla.
# 📉 **Pero de esa misma cuenta salieron dos cosas que su nota no decía.** (1) **La
# «pantalla va ~20 h por detrás» acaba de morir**: el desfase pasó de **−19,7 h**
# (lectura 4) a **+2,7 h** (lectura 6), y un instrumento no se adelanta a sí mismo
# — nunca fue una propiedad del instrumento, era el relleno de una cuenta recién
# abierta. Si sobrevive a `T-067`, corrige un retraso que ya no existe. (2) **Los
# 0,37 US$ no son «lo gastado»**: de 22,8 h de EC2 solo asoman **$0,0137**. Quien
# divida ese total por los días transcurridos **proyecta muy por debajo.**
# ⚠️ **Y la guardia de `A-018` no tiene fecha de caducidad, que es el hueco de
# verdad:** *"alarma rota exige ≥12 h de silencio DESPUÉS de que el importe sea
# visible"*. Si el instrumento roto es el presupuesto, el importe **nunca** es
# visible, la guardia **nunca arranca** y la alarma **nunca se puede declarar
# rota**. 🔑 **El criterio es infalsable justo en el modo de fallo más probable.**
# Es una espera sin caducidad —lo que `D-041` se inventó para prohibir— pero
# metida **dentro del criterio** en vez de en la conversación. Pide un reloj de
# fuera. Y hay una medición gratis sin hacer: **mirar `Importe previsto`** — si hoy
# trae un número, el presupuesto SÍ traga datos y el problema es solo del campo
# `utilizado`, que es un diagnóstico mucho más estrecho.
# ➕ **Su hallazgo del volumen EBS es bueno y llega más lejos de lo que lo usaron:**
# lo escribieron para decir que apagar no lleva el gasto a cero, y lo que implica es
# que **son TRES fuentes de gasto desde el 08, no dos** como decía la quinta
# lectura. Corregido el mismo día, y `T-067` se reescribe para separar tres tarifas.
# 🐛 **El resumen hablado volvió a ser peor que el documento, dos veces**, y esta
# vez con consecuencia medible:
#   - **El testigo del primer apagado se cayó.** `T-074` dice literal *"con alguien
#     mirando la consola, no a las 23:00 con todo el mundo dormido"*; el resumen
#     decía *"se apaga sola"* y pasaba a mañana. Sin ese minuto, si el `-P` no
#     dispara, **la máquina cobra toda la noche y el fallo es mudo.**
#   - **«Entra por la IP» perdió la palabra SSH.** El documento dice *"entrar por
#     SSH usando la IP fija"*; el resumen dijo *"entra por la IP, no por el
#     nombre"*. **Medido aquí:** `https://32.199.55.191` → `000`, **y también con
#     `-k`**: no es un aviso de certificado que se pueda aceptar, **el handshake no
#     ocurre** (Caddy solo sirve el nombre que tiene certificado). Y `T-074` pide
#     mañana *"200 sin tocar nada"* y *"certificado sin reemitir"*: **las dos exigen
#     el nombre.** Seguir el atajo habría dado un **ROJO FALSO en la primera
#     medición de la regla nueva.** Reparto correcto: **SSH por IP, navegador y
#     `curl` por nombre**, y `curl --resolve` si el DNS falla — que es lo que
#     `A-017` ya prescribía.
# 🌐 **Episodio 6 de `A-017`, medido aquí sin buscarlo:** 1 de cada 3 intentos dio
# `Could not resolve host` y los otros dos `200`, en la misma ráfaga. Refuerza su
# conclusión del día —**es el cliente, no DuckDNS**— y aporta lo que no tenían:
# pasa también en esta máquina.
# ✏️ **Corrección mía, pequeña, por su `L-030`** (*`uptime -s` no es un registro, se
# reinicia*): el «EC2 viva 22,84 h» que di salía de ese número **anotado**. La
# conclusión no dependía de él —las 74 h contra 71,3 usan el `t=0` de la IP, que
# viene de la consola— pero la línea era menos firme de lo que parecía.
# 🌙 **La 58 (SEGUNDA del mismo día) CERRÓ `T-073`: la máquina se apaga sola.**
# Ya no es un `shutdown -P 23:00` de un solo uso —un despertador que se borra al
# reiniciar— sino dos unidades de systemd (`teapp-shutdown.service` = el *qué*,
# `.timer` = el *cuándo*), instaladas por `install.sh` y **armadas de verdad**:
# `NEXT: Sun 2026-08-09 23:00:00 UTC`, `LAST` y `PASSED` vacíos, y el despertador
# viejo desarmado con medida antes y después. De 351 a **362 tests**.
# `D-046`, `L-033`, `L-034`, `A-022` y el paso 5b de `console_steps.md`.
# 🎁 **Un testigo que salió gratis de una resta:** yo calculaba 5 h 13 min hasta el
# disparo desde esta máquina y la EC2 decía 5 h 13 min. **Los dos relojes coinciden
# al minuto**, así que la máquina está de verdad en UTC — que es la suposición sobre
# la que descansa `D-046` entero y que nadie había comprobado.
# 🔴 **EL HALLAZGO DEL DÍA ES ESTRUCTURAL Y ES DE ESTE REPARTO, NO DE TEAPP: la
# colisión `L-013` contra `LM.13`.** `D-041` citaba `[L-013]` para decir *"un
# control que nadie ha visto funcionar no es un control"*. `L-013` **no dice eso**
# —dice *"cerrar un hueco no cierra los demás"*, desde `499879a` y sin una edición—;
# la frase existe, es correcta, y es **`LM.13`**, de ESTE archivo. Una letra de
# diferencia entre dos espacios de nombres:
# `LM.nn` = lecciones de método (Edu_TripleS) · `L-nnn` = lecciones de TEAPP.
# **Auditado: 16 citas malas** (13 pasadas a `LM.13`, 1 que era la regla 6, 2 sin
# dueño en ningún repo → se les quitó el corchete). Prefijo escrito en el
# `CLAUDE.md` de TEAPP. 🔑 **Es un defecto del reparto que decidimos en la 43**
# —*aquí el porqué, allá lo que el programa hace*—: las lecciones de método se
# quedaron de este lado y **las citas cruzan la frontera sin pasaporte**. Por eso
# consta aquí y no solo allá.
# 📌 **Y la convención YA EXISTÍA de hecho**: `LM.13`, `LM.15` y `LM.19` se usaban
# bien en 19 sitios. Existía y no protegió de nada **porque no estaba escrita.**
# 🔑 Suya, y es la mejor línea del día: *un acuerdo que depende de que nadie se
# despiste no es un acuerdo, es una racha.* Es `Persistent=false` escrito a la
# fuerza aunque ya sea el valor por defecto — que lo escribió él **una hora antes**,
# en otro archivo, y no reconoció la misma idea al cambiar de material.
# 🚨 **CUATRO controles en un día midiendo algo distinto de lo que prometían**, y
# el cuarto es nuevo de verdad:
#   1. `is-active` en `install.sh`: su comentario declaraba que el fallo del
#      temporizador era *el más mudo de los tres*, y `is-active` **no distingue**
#      "activo y habilitado" de "activo y NO habilitado" — el fallo de mañana.
#      Verde esta noche, `T-074` verde, y el martes la factura corre. → `is-enabled`
#      **al lado**, no en su lugar: son dos preguntas.
#   2. El guardián que buscaba un texto literal que `install.sh` **nunca escribiría**
#      (usa una variable). Lo cazó él solo.
#   3. El recuento de citas: 9 → 13 → 15 → **16**. 🔑 *El bueno salió de `git diff`;
#      los tres malos salieron de la cabeza.* Y el matiz que vale: **el nueve no era
#      falso, era parcial y no se anunció como parcial.**
#   4. ⭐ **El control que acabó dictando cómo se escribe el archivo que vigila.**
#      Contaba apariciones de `[LM.13]` en `progress.md`; el `session-closer`
#      mencionó la colisión en prosa, el contador se fue a 4 y se puso rojo. **El
#      closer reescribió su texto evitando nombrar los identificadores para dejarlo
#      en verde** → una entrada sobre una colisión de identificadores **que no puede
#      nombrarlos**. Peor que un rojo falso: no da un dato malo, **deforma el
#      artefacto**. Arreglado: busca las dos frases concretas.
# ✅ **`L-034` es la lección madre de las cuatro**, y su antepasado no fue el que yo
# mandé buscar sino uno mejor y suyo: **`L-017`, del día 05, MISMO ARCHIVO y MISMO
# BLOQUE de `install.sh`.** Cuatro días después reintrodujo allí el atajo exacto que
# `L-017` había arreglado. 🔑 **Arreglar un bloque no lo inmuniza: lo deja más
# peligroso, porque lleva encima la cicatriz de haber sido auditado y esa cicatriz
# avala las líneas que se añaden después.** Es *nadie audita un verde* (`LM.15`) con
# el mecanismo explicado por fin: **un control sin estrenar da miedo y se revisa;
# uno en verde tranquiliza y ya no lo mira nadie.**
# ⚠️ **`A-022` — y la cara peligrosa la puso él, no yo.** Yo planteé que systemd
# rechazara la zona de `OnCalendar=... UTC`; eso está cubierto (el guion se para en
# rojo). Lo que no vi: **si la IGNORA en vez de rechazarla, la ventana de `D-045` se
# mueve 5 horas sin un solo error.** Se mide dos veces: hoy y en `T-069`, que es
# donde de verdad mordería porque la máquina es nueva. **Decisión conjunta: NO
# construir hoy el guardián de la hora** — no hay con qué verlo ponerse rojo, y
# estrenar un control sin verlo morder en la sesión que escribió `L-034` sería
# cómico.
# 🐛 **TRES ERRORES MÍOS, los tres medidos:**
#   - **Resté una hora local de una hora UTC** y dije *"vence en 1 h 40"* cuando
#     faltaban **5 h 30**. Tomé el `17:2x` de una línea y el `18:00` de otra, y las
#     dos eran ciertas **en zonas distintas**. 🔑 Es `D-046` —el motivo por el que
#     eligió systemd sobre cron— cometido a mano en la conversación que lo escribía.
#     Él **no lo supuso: lo dijo y no lo dio por bueno.**
#   - **Pedí comprobar `is-enabled` cuando `install.sh` ya hacía `enable --now`**
#     (línea 248). Estaba en el código; no lo había leído.
#   - **Mandé el antepasado al repo equivocado.** Dije *"la lección de la sesión 48"*
#     sin decir en qué archivo: `LM.15` vive AQUÍ, no en TEAPP. Lo buscó allá y no
#     estaba. → **Un puntero sin repo es medio puntero**, que es la misma familia de
#     lo que estuvimos arreglando todo el día.
# ✅ **Y una decisión suya que hay que respaldar: cruzó una frontera a sabiendas.**
# Dos de las 16 citas vivían en `progress.md`, que escribe el `session-closer`. Lo
# tocó igual —solo punteros— porque dejar citas falsas en el archivo que el
# `session-starter` lee primero es garantizar que mañana se propaguen. Correcto. El
# riesgo que abrió (**un arreglo que otro proceso puede deshacer sin ningún error**)
# quedó anotado dentro de `L-034` con su control al lado, y **comprobado por mí tras
# el cierre: `[LM.13]` = 2, `[L-013]` = 0.**
#
# 🟢 **La 59 (día siguiente) CERRÓ `A-014` ENTERA — la última suposición del paso 7
# que necesitaba la máquina.** Por la mañana `T-074` completa: **200 POR EL NOMBRE,
# 10 de 10**, certificado `Aug 8 16:55 → Nov 6 16:55` **SIN reemitir**, `Server:
# uvicorn` + `Via: 1.1 Caddy`, el 8000 en TIMEOUT y **el marcador de jorge vivo tras
# el apagado**. Que el certificado no se reemita no es cosmético: Let's Encrypt tiene
# tope semanal, y una máquina que se apaga cada noche pidiendo certificado nuevo cada
# mañana se quedaría sin cuota **el jueves, sin que nadie sepa por qué**.
# 🔑 **EL HALLAZGO DE ESTA TERMINAL FUE PARTIR `A-014` EN DOS MITADES.** Medir que
# *llega la dirección real* **no es** medir que *se descarta la falsa*, y la segunda
# es la que aguanta un ataque: si la cabecera forjada colara, quien ataca pone una
# dirección distinta en cada intento y **el freno no muerde nunca**. Estaba solo
# **inferida** —`Caddyfile.template:75` no declara `trusted_proxies`—, que es
# *tenerlo escrito*: `LM.13` con las mismas palabras que ellos usaron al partir
# `T-060`. Las dos, medidas hoy en el servidor real:
#   1. Dos aparatos honestos (PC por wifi, celular **con el wifi apagado**) → el log
#      escribe `181.58.xx.xx` (su casa) y `191.153.xx.xx` (la operadora móvil),
#      **cada una igual a su `ipify`** y distintas entre sí. ✂️ **Enmascaradas a
#      propósito: este repo es público y son datos personales** — ver la sesión 42.
#   2. Cuatro peticiones forjando la cabecera → **ni un solo `9.9.9.9`**. Y las dos
#      variantes de más —la cadena `9.9.9.9, 8.8.8.8` y `X-Real-IP`— **las añadieron
#      ellos sin que nadie las pidiera**: descartar solo la forma simple habría
#      dejado la puerta de al lado sin mirar.
# 🔑 **Su prueba estaba mejor construida de lo que la contaron, y el matiz lo puso
# esta terminal:** el cubo agotado no es "un control", es **lo que vuelve visible un
# fallo mudo**. Si la forja hubiera colado, el origen habría sido un cubo NUEVO y la
# respuesta **401, sin renglón en el log**. 📌 **El discriminador no era lo que dice
# el log: era 429 contra 401.**
# 🎁 **Y el log traía un reloj que nadie estaba usando.** `faltan N s` sale de
# `login_guard.py:191`, así que despejando se reconstruye **cuándo empezó cada
# ráfaga**: 899 s a las 15:01:03 → primer fallo **15:01:01**, que cuadra **al
# segundo** con su narración sin depender de ella. Y por la tarde los dos relojes
# **convergieron en el mismo instante** (`15:16:01`) por caminos separados hora y
# cuarto, probando que el cubo era el mismo. → su `L-036`: *antes de citar la
# narración de quien midió, mira si el instrumento trae su propio reloj.*
# ⭐ **Lo más fuerte de su informe venía archivado como "apoyo":** el celular gastó
# **sus propios 5 intentos** cuando el cubo del PC ya estaba agotado. Si la app viera
# solo a Caddy, el primer toque del celular habría dado 429 en el acto. **Es la misma
# conclusión por un camino que no pasa por el log** — dos testigos que no comparten
# instrumento. Subido a hallazgo por decisión suya.
# 🔬 **`Importe previsto` = `-`, y la medición que llamamos "gratis y decisiva" NO
# decide nada.** Verificado en la fuente: *"If AWS doesn't have enough data to
# forecast an 80% prediction interval, Cost Explorer doesn't provide a forecast.
# **This is common for accounts that have less than one full billing cycle.**"* La
# cuenta se abrió el 06: la raya es el comportamiento documentado, salga la alarma
# sana o rota. 🔑 **Es `LM.15` DENTRO de la prueba que diseñamos para escapar de un
# criterio infalsable.** ✅ Lo que sí aporta es una **fecha**: al cerrar el primer
# ciclo (~1 de septiembre) esa mitad deja de estar ciega. Antes no sabíamos cuándo.
# 🐛 **TRES ERRORES MÍOS, los tres cazados por ellos:**
#   - ⭐ **Propuse un experimento que llevaba CUATRO DÍAS corriendo.** Recomendé
#     bajar el umbral del presupuesto "para ver el freno morder": ya estaba en
#     **0,01 US$** desde el día 6, contra 0,37 gastados —**37× cubierto**— y sin un
#     solo correo. Mi rama *"si no salta en 24 h"* era el presente. Habría destruido
#     la línea base a cambio de nada. 🔑 Y su aritmética cierra la puerta: **contra
#     `0,00` no hay umbral positivo posible.** Es `LM.20` otra vez, y mío.
#   - **Crucé la numeración:** dije *"`T-073` reportada vs vista"* cuando la tarea de
#     mirar el disparo es **`T-074`**.
#   - **Leí el archivo y me paré en la rama que me daba la razón** (`api.py:482`).
#     Un usuario inventado **bien formado** no pasa por `InvalidUserError`: llega a
#     `accounts.verify`, que **devuelve `False`** (`accounts.py:280`), y cuenta como
#     fallo en la **494**. La conclusión era buena —cuenta igual, `jorge` no corría
#     riesgo— **y la causa estaba una rama al lado**: sesión 56 en pequeño.
# ✅ **Y una que sí cacé yo, antes de aceptar el arranque que proponían:** pidieron
# empezar por `T-060b`, **cerrada desde el 08** (`tasks.md:72`). No fue despiste: la
# tabla de `[A-014]` en `assumptions.md:1207` **seguía nombrándola** como lo que
# faltaba. Esa tabla es del **07** y nunca se encogió. → `LM.24`.
# 🔴 **`L-035`, de ellos, y nació de una predicción MÍA que falló:** dije que
# `list-timers` traería `LAST` y `PASSED` llenos. `Persistent=false` —puesto a
# propósito, con doce líneas de comentario— hace que systemd **no escriba la marca de
# disparo**, que es justo el archivo que `list-timers` lee. **La pregunta no sale mal
# contestada: no hay dónde contestarla.** El testigo bueno estaba en el journal, y
# ahí apareció la cadena entera con `[D-045]` dentro.
# 📐 **CORRECCIÓN SUYA SOBRE EL PAPEL DE ESTA TERMINAL, y es del reparto:** *"esta
# terminal no prueba ni ejecuta; asesora a la otra sobre lo que se debe hacer"*.
# Llegó cuando escribí *"yo lanzo los seis intentos de mi lado"* — eso era trabajo de
# la otra terminal, no supervisión. ⚠️ **Queda una pregunta abierta que hice y no se
# contestó:** si medir **desde fuera** sin tocar el servidor (`curl`, `nslookup`,
# `openssl`) entra en supervisar o también sobra. Importa porque es lo que cazó cosas
# en las sesiones 42, 55, 57 y hoy mismo el certificado. **Preguntarlo al abrir.**
# 📌 **Y una lección de trato, no de método:** a mitad de sesión dijo *"no entiendo
# nada de lo que estás buscando"*. Tenía razón — le había dado el procedimiento sin
# contarle **qué se quería averiguar y por qué**. El curso dice *concepto antes que
# código*, y llevaba tres mensajes al revés.
#
# 🚦 **La 60 (segunda del mismo día) CRUZÓ AL PASO 8, y la objeción que lo movió
# fue SUYA, no de una revisión:** *"sentimos que invertimos mucho tiempo y no
# hemos podido avanzar"*. 📊 **Se contó en vez de recordarse** (regla 6, sobre el
# índice de `progress.md`): pasos **0–6 = 12 sesiones / 3 días**; **paso 7 solo =
# 22 sesiones / 6 días**. Un paso costó casi el doble que los otros siete juntos.
# La sensación estaba **bien calibrada** y llevaba veintidós sesiones sin
# instrumento — ningún control del proyecto miraba el conjunto, todos miraban
# hacia dentro de la sesión. → su `L-037`: **el andamio se volvió el trabajo.**
# 🔑 **El argumento que decide apunta al revés de lo que parecía:** hay HTTPS,
# identidad verificada, cuota por persona y apagado automático montados **encima
# de un tutor que sigue siendo el maniquí del paso 1**. Cada día de pulido del
# paso 7 compra robustez para algo que todavía no hace aquello para lo que existe.
# ✅ **Y se cruzó bien:** `D-048` deja `T-046`, `T-067`, `T-069` y `T-070` abiertas
# **una a una con su motivo y su dueño** —`T-069` con fecha tope ≈ 2026-09-01 y su
# precio escrito aparte en `A-023`—, y corrige un error de su propia sesión
# (`T-069` **no** bloqueaba el paso 8; lo único que bloqueaba era `T-056`, de dos
# minutos). 📌 **`D-047` trae un hallazgo de verdad:** reutilizar
# `teapp.duckdns.org` en la máquina del ensayo **no es mala idea, es imposible** —
# Let's Encrypt iría a validar el nombre y llamaría a la máquina vieja, y el guion
# se para en `install.sh:378`.
# 🔴 **PERO EL CIERRE METIÓ UNA AFIRMACIÓN FALSA EN EL ARCHIVO, y es el hallazgo
# de método del día.** El resumen decía *"no hace falta encenderla a mano, el
# apagado y encendido ya son automáticos (`[D-045]`/`[D-046]`)"* — y `D-045` dice
# **lo contrario y a propósito**: encendido MANUAL, *para que el olvido caiga del
# lado que no cobra*. Contradicho también por `console_steps.md:416` (*"no se
# enciende sola"*). ⚙️ **Y no hace falta abrir ningún archivo para verlo: nada
# dentro de la máquina puede encenderla, porque apagada no hay nada dentro
# corriendo.** El daño era de mañana y medible: `T-056` exige SSH a la máquina
# viva, y el campo que se lee primero decía que no había que encenderla.
# ✂️ **Corregido y verificado desde esta terminal** (`37d92cf`, en `origin/main`,
# con `00b2365` intacto debajo): estaba en **tres sitios**, no en uno — se había
# replicado dentro del propio texto del closer. Barrido propio: la única mención
# viva es la correcta; las otras dos viven citadas dentro de `L-038` como lo que
# estuvo mal. Y el campo quedó **con el porqué dentro**, no solo con el aviso — sin
# la asimetría escrita, dentro de dos semanas alguien lo lee, le parece un
# descuido y **construye la pieza que lo automatiza**.
# 🔑 **`LM.26`, y el filo lo puso la otra terminal: la DIRECCIÓN del error es el
# diagnóstico.** Lo inventado fue **la versión cómoda** —*"no hace falta hacer
# nada"*—, nunca la incómoda. **Una frase que no le pide nada al lector no ofrece
# resistencia mientras se escribe.** Es la cuarta vez en siete sesiones (54, 57,
# 58, 60) que el resumen sale peor que el documento, y la primera que **entra al
# archivo** en vez de quedarse en la voz — con dos corchetes al lado que no venían
# de ninguna parte: **se le pegaron después, como armadura.**
# 📐 **Causa estructural, suya y buena:** el `session-closer` arranca en frío y
# reconstruye del `git diff`. Pero **un `diff` no puede decir si una máquina está
# encendida.** Regla que queda: el closer describe lo que el diff respalda y manda
# al Paso 5b; **no afirma estado del mundo.**
# ⚠️ **Dos cosas que añadí y conviene no perder.** (1) **Yo no lo cacé leyendo su
# documento**: chocaba con `D-045`, que tenía en la cabeza porque el protocolo de
# inicio me lo puso delante tres horas antes. **Si abro el día por otro lado, la
# frase pasa** — eso no es un control, es una coincidencia que salió bien.
# (2) **`L-038` no tiene control y su propia `L-026` dice que la disciplina se
# degrada con la repetición** — pero el control obvio (buscar frases como *"no
# hace falta"*) sería **peor**: enseñaría a esquivar las palabras, no la
# afirmación, que es el bicho de la sesión 58. Se queda como disciplina **y se
# anota como desprotegida**.
# ✅ **Y se contestó la pregunta que quedó abierta ayer sobre el reparto:**
# **medir desde fuera SÍ es supervisar.** `curl`, `nslookup`, `openssl` y leer sus
# repos entran; **probar y ejecutar, no.** Con eso, lo medido hoy aquí: 200 por el
# nombre (4 de 5), `Server: uvicorn` + `Via: 1.1 Caddy`, `/me` → 401, el 8000 en
# TIMEOUT, certificado `Aug 8 → Nov 6` **todavía sin reemitir** tras la primera
# noche de apagado, y `A-017` **episodio 7** (un `000` y cuatro `200` en la misma
# ráfaga, desde esta máquina).
# 🔴 **LO QUE SE CAYÓ POR EL BORDE HOY, y hay que recogerlo mañana: la SÉPTIMA
# lectura de `A-018` no se tomó.** La última es la sexta, del **09 ~14:45 UTC**.
# Se recomendó dos veces y las dos veces la tapó otra cosa. ⚠️ **Y ahora tiene un
# enemigo nuevo:** al cruzar al paso 8, `T-067` pasa a ser *"un pendiente del paso
# anterior"* — la categoría de cosas que nadie mira. `h1` **no se provoca, se lee**,
# y solo existe mientras alguien mire.
#
#
# 🔎 **La 61 (TERCERA del mismo día) fue de SUPERVISIÓN PURA: no se tocó una línea
# de código, ni aquí ni allá.** El encargo fue *"antes de salir revisa el estado del
# punto 8 en la terminal donde se lleva a cabo"* — leer sus repos, que es lo que
# `LM.25` dejó dentro del reparto.
# ✅ **El paso 8 ARRANCÓ, y arrancó bien.** La otra terminal tuvo sesión esta mañana
# (commits `cfe62d4` y `b62c67b`, 12:04, árbol limpio y sincronizado con `origin`).
# `T-075` cerrada (la API key de Anthropic en el `.env` **local**, verificada sin
# imprimirla: `sk-ant-`, 108 caracteres, `.gitignore:3`) y `T-056` cerrada por SSH
# real contra la EC2. **Primer gasto real del proyecto que no es la nube.**
# 🔬 **Y lo comprobé en vez de creerlo:** `git diff --stat 00b2365..HEAD` dice que
# los cuatro archivos del día son de `_persistence/`. **Ni `app/`, ni `tests/`, ni
# `deploy/`.** Leído `app/tools.py:128`: `judge_grammar` sigue devolviendo
# `FAKE_VERDICT`. 📌 **El plan de `T-076` es planeación honesta, no trabajo a
# medias** — cuando un informe dice *"plan hecho, sin ejecutar"*, eso se mira.
# 🔑 **`D-049` es buena y la respaldo:** arrancar con `claude-opus-5` a
# `effort: "low"` —**el modelo más caro, no el más barato**— para no mezclar dos
# sospechosos (modelo y rúbrica) el día que se estrena el veredicto real. Es el
# control al lado de la sesión 8 aplicado a una decisión de dinero.
#
# 🔴 **TRES HALLAZGOS SOBRE `T-076`, Y EL PRIMERO PUEDE ROMPERLA EN SU PRIMERA
# CORRIDA.** Salieron de ir a la fuente (`/claude-api`), no de la memoria:
#   1. 🚨 **En `claude-opus-5` el pensamiento viene ENCENDIDO por defecto** —cambia
#      respecto a los modelos anteriores— **y `max_tokens` no limita la respuesta:
#      limita pensamiento + respuesta JUNTOS.** `judge_grammar` devuelve una frase
#      corta, así que la tentación al escribirla es `max_tokens=200`. Con eso el
#      pensamiento se come el presupuesto y **el veredicto llega cortado o vacío**,
#      con `stop_reason: "max_tokens"`. 🔑 **No explota: devuelve basura en
#      silencio.** Es `LM.15` —*un instrumento ciego no da un dato falso, da
#      silencio*— metido en la primera línea del paso 8.
#   2. 🚨 **`stop_reason` puede venir `"refusal"` y entonces `content` está VACÍO.**
#      Un `response.content[0].text` sin mirar antes `stop_reason` revienta con
#      `IndexError`. Para un tutor de inglés es improbable — y *improbable* es la
#      palabra que este proyecto lleva cuarenta sesiones negándose a aceptar.
#   3. 🎁 **Una a favor de ellos:** en `claude-opus-5` el mínimo para que el caché de
#      prompt muerda bajó a **512 tokens** (era 1024). La rúbrica es idéntica en cada
#      llamada: si pesa más de 512, las lecturas cuestan **una décima parte** y
#      `D-049` sale aún más barata de lo que calcularon.
# 💰 **El precio, escrito para que `T-079` lo tenga delante:** `claude-opus-5`
# **$5/$25** por millón de tokens (entrada/salida); `claude-sonnet-5` $3/$15
# (**$2/$10 promocional hasta el 31 de agosto**); `claude-haiku-4-5` **$1/$5**.
# Opus es **5× Haiku**. Con una llamada típica (~300 entrada, ~100 salida) son
# **~$0,004 por práctica** contra ~$0,0008: a 20 prácticas/día (`A-010`),
# **$0,08/día contra $0,016/día por persona**. Con un usuario no decide nada — el
# descenso a Sonnet/Haiku como trabajo **medido** del paso 9 está bien colocado.
# 📌 **Y un detalle que nadie había puesto junto:** el pensamiento **se cobra como
# salida, a $25**. El `effort: "low"` de `D-049` no es solo calidad — **es la
# palanca de costo del día.** Bien elegido, aunque no por ese motivo.
#
# 🌙 **LA MÁQUINA ESTABA ENCENDIDA AL ABRIR, Y NO SE SUPO POR QUÉ.** Medido aquí a
# las 16:31 UTC: `200` por el nombre, `Server: uvicorn` + `Via: 1.1 Caddy`, `/me`
# → `401`, DNS a `32.199.55.191`. Se preguntó si la había encendido él y **la
# pregunta no se contestó** — la sesión siguió por el paso 8. ⚠️ **Queda abierta y
# no es cosmética:** o la encendió él (todo bien), **o el apagado automático de
# `D-046` no disparó anoche y lleva horas cobrando en silencio**. Es justo el modo
# de fallo que `L-034` describió: el control en verde que ya no mira nadie.
# 📌 **Se resuelve en un comando, no adivinando:** `systemctl list-timers` o el
# journal en la máquina, o el historial de la instancia en la consola de AWS.
# 🌐 **`A-017` episodio 8:** de 3 intentos, uno dio `000` y dos `200` en la misma
# ráfaga. Sigue vivo desde esta máquina.
#
# 🔴 **LA SÉPTIMA LECTURA DE `A-018` NO SE TOMÓ. TERCERA SESIÓN SEGUIDA.** La
# última sigue siendo la sexta (**09, ~14:45 UTC**). La 60 la recomendó dos veces y
# las dos veces la tapó otra cosa; hoy la tapó el paso 8. 🔑 **Ya no es un descuido,
# es un patrón** — y el patrón es exactamente lo que la 60 predijo al cruzar de
# paso: `T-067` pasó a ser *"un pendiente del paso anterior"*, la categoría de
# cosas que nadie mira. **`h1` no se provoca, se lee, y solo existe mientras alguien
# mire.** Son dos números de la consola: `Importe utilizado` y `Costo Acumulado
# Mensual`.
#
# 📍 **DÓNDE SE ARRANCA MAÑANA (paso 8, `T-076`):** sustituir el cuerpo de
# `judge_grammar` (`app/tools.py:128`) por la llamada real a Claude, con rúbrica.
# La firma ya es la definitiva; el paso 8 **solo cambia el cuerpo**. El plan de
# archivos está escrito y sin ejecutar (`tasks.md`, `T-076`).
# 🚨 **Llevarle los tres hallazgos de arriba ANTES de que escriba el cuerpo**, no
# después: dos de ellos son fallos mudos, y un fallo mudo no se encuentra probando.
# ⚠️ **`tests/no_network.py` bloquea la red en TODA la suite (`C-001`)** — los tests
# nuevos tienen que inyectar un cliente falso, no llamar a Claude de verdad. Lo
# cazaron ellos solos y está bien cazado.
# 🌙 **Comprobar si la máquina sigue encendida y POR QUÉ** (ver arriba). Si nadie la
# encendió, eso es lo primero del día y no `T-076`.
# 🔴 **PENDIENTE DEL PASO 7 QUE SIGUE TENIENDO RELOJ: la séptima lectura de
# `A-018`.** Tres sesiones seguidas sin tomarse. Es lo único que puede desbloquear
# `T-067`.
# 🔴 **`T-067`** (coste proyectado, con las **tres** tarifas separadas y bajo el
# régimen de la ventana) **cuelga de `h1`**: que `Importe utilizado` deje de marcar
# `0,00`. **Eso no se provoca, se espera y se lee** — el experimento del umbral
# quedó descartado por medición, no por pereza.
# ⏳ **Las dos lecturas ancladas siguen siendo el ritual:** 12:00 y 23:00 UTC.
# 📅 **Dos fechas ya puestas:** **~1 de septiembre**, cuando cierre el primer ciclo
# de facturación y `Importe previsto` deje de ser estructuralmente ciego; y
# **≈2026-09-01 como tope de `T-069`**, el ensayo de reconstrucción aplazado hoy
# con dueño de calendario (`D-048`, `A-023`).
#
#
# 🔬 **La 62 (CUARTA del mismo día) fue de SUPERVISIÓN a cuatro tiempos: se
# auditó la otra terminal cuatro veces seguidas, y de cada auditoría salió código
# suyo el mismo día.** Aquí no se escribió una línea de programa. TEAPP pasó de
# **362 a 381 tests** en cuatro commits (`671e703`, `9d7e076`, `8d335fd`,
# `d699bf5`), y `T-076` cierra el día honestamente en 🔄, no en ✅.
# 🟢 **LA SÉPTIMA LECTURA DE `A-018` SE TOMÓ POR FIN**, después de tres sesiones
# tapándose: `Importe utilizado` **0,00** (quinta seguida), `Importe previsto`
# **—**, `Costo Acumulado Mensual` **0,74 US$**.
# 🔴 **Y con ella muere la coartada del retraso.** El `0,00` viene del día 6: son
# cuatro días y ~doce refrescos del presupuesto sin moverse un céntimo, mientras
# el otro widget subía. Un retraso se mide en horas. ⚠️ **Ojo con la conclusión:**
# esto **no** prueba que la alarma esté rota — prueba que el presupuesto evalúa
# algo que no es el gasto real. Si evalúa su propio `0,00`, la alarma funciona
# perfectamente sobre un dato falso, que es peor. El umbral lleva en **0,01 US$**
# desde el día 6: va **74 veces cubierto** y no ha sonado.
# 🔑 **EL HALLAZGO DEL DÍA ES QUE `T-067` NUNCA NECESITÓ `h1`.** Llevaba días
# bloqueada esperando que `Importe utilizado` dejara de ser `0,00` — colgando del
# instrumento roto **teniendo el bueno al lado**. Dos lecturas fechadas del
# `Costo Acumulado Mensual` son un ritmo: `0,74 − 0,37 = 0,37 US$` en 28,2 h →
# `0,0131 US$/h` → **≈ $57 de los $200 en seis meses**, y menos aún bajo la
# ventana de `D-045`. 📌 **Lo mejor de esa cuenta es lo que NO lleva dentro:** ni
# el precio de la `t3.micro`, ni el del disco, ni el de la IP. **No usa ninguna
# lista de precios**, así que no puede equivocarse por heredar un número de mi
# memoria. Solo dos números leídos en pantalla y un reloj. **Los seis meses caben,
# y sobra.**
# ✅ **`D-046` disparó anoche (segunda noche) y la máquina la encendió él.** La
# duda que dejé abierta ayer queda cerrada con dato, no con "seguramente".
#
# 🚨 **LOS TRES HALLAZGOS DE `claude-opus-5` LLEGARON ANTES DE QUE ESCRIBIERAN EL
# CUERPO**, que era el punto: dos eran fallos mudos, y un fallo mudo no se
# encuentra probando. (1) El pensamiento viene **encendido por defecto** y
# `max_tokens` limita pensamiento + respuesta **juntos** → pusieron 1000, no 200.
# (2) `stop_reason: "refusal"` deja `content` vacío. (3) ✏️ **El tercero resultó
# NO aplicar, y lo corregí yo:** el caché muerde desde 512 tokens, pero la rúbrica
# pesa 678 caracteres ≈ **170 tokens**. Por debajo del mínimo el caché **no avisa,
# simplemente no cachea**. Mi nota les habría hecho añadir un `cache_control`
# inútil.
# 🔴 **AUDITORÍA 1 — el reloj que faltaba, y el aviso lo habían escrito ellos.**
# El cliente se construía sin `timeout`, y el del SDK de Python son **DIEZ
# MINUTOS**. `api.py:130`, escrito el **4 de agosto**, decía literal: *"en el paso
# 8 la llamada al modelo necesita SU PROPIO timeout... este 504 devuelve el
# control a quien pregunta y deja el hilo secuestrado igual"*. Y el comentario de
# `MAX_RETRIES = 0` razonaba **tres veces** sobre los 10 s de `A-011` — quitaron
# los reintentos para caber en un presupuesto de tiempo **que nunca se puso**.
# → `timeout=8.0` (`D-054`). Es `LM.20` por quinta vez, con la vuelta más dura:
# la razón estaba escrita, por ellos, en el archivo de al lado, con sirena.
# ✏️ **AUDITORÍA 2 — su arreglo fue MEJOR que el mío, y el mío tenía un defecto.**
# Yo propuse `request_sent = (stop_reason != "refusal")`. Eso **regala cuota**: un
# rechazo a *mitad* sí factura lo generado. Ellos añadieron `and not content` y
# escribieron los **dos** tests —mismo `stop_reason`, decisión contraria—. Es la
# partición de `A-014` aplicada a un booleano: *"un rechazo"* no era una cosa.
# 🔬 **AUDITORÍA 3 — pero `content` seguía siendo un PROXY, y tenía agujero real.**
# El dato está en la respuesta: `usage.input_tokens` / `usage.output_tokens`. Y sin
# streaming —que es como llama `judge_grammar`— un rechazo a mitad **omite el
# parcial**: llega con `content` vacío, calcado por fuera al rechazo gratis, con
# los tokens pagados. Se devolvía cuota justo donde `D-051` manda cobrar.
# → `D-055`, verificado en rojo por sabotaje. 🔑 **Un proxy no puede separar dos
# casos que tienen la misma forma.** 🎁 Y lo mejor del día es de ellos: `FakeUsage`
# **viene facturado por defecto**, así que una respuesta gratis tiene que escribir
# los ceros a propósito — la regla 3 metida en el valor por defecto.
#
# 🐛 **EL EPISODIO DE LA CITA, Y ES DE LOS DOS.** Yo escribí *"es su propia
# `L-036`: antes de inferirlo, mira si el instrumento trae su propio contador"*.
# **El puntero era correcto** —la regla vive en `lessons.md:334-335`, dentro de
# `L-036`—; **lo que derivó fue mi paráfrasis**: la suya habla de *la narración* y
# de *un reloj*, la mía de *inferir* y de *un contador*. Misma familia, regla
# distinta, y la presenté como frase suya.
# 🔴 **Ellos fueron a comprobarlo, leyeron 13 líneas de 119, vieron que el título
# hablaba de otra cosa y escribieron en `lessons.md` que la cita era falsa.** La
# regla estaba 90 líneas más abajo, en la misma entrada. Su frase suya: *el gesto
# de abrir el archivo se sintió igual que haber comprobado* — y bastó para retirar
# una cita buena y poner una afirmación falsa **dentro del párrafo escrito para
# denunciar exactamente eso**. Corregido el mismo día (`d699bf5`).
# 🔑 **Lo estructural, que vale más que las dos correcciones: `L-036` lleva CUATRO
# hallazgos bajo un solo título.** El corchete no dice a cuál se refiere, así que
# no se puede verificar sin leer los cuatro. Es medio puntero — lo mismo que ellos
# me dijeron en la 58 cuando mandé un antepasado al repo equivocado. Las citas a
# entradas largas tienen que nombrar el hallazgo: `[L-036, el reloj del log]`.
# ⚠️ **Y el control nuevo de `L-040` no habría cazado el error de hoy.** Dice *"se
# busca la frase"* — pero yo no cité, **parafraseé**: buscar mis palabras en
# `L-036` daba cero resultados y la conclusión habría sido la misma. **Cuarta cara
# del bicho de la 58: un control que mide algo distinto de lo que promete.**
#
# 🚨 **CASI SE CIERRA SIN COMMIT, y lo cacé mirando el árbol.** Su informe daba la
# sesión por cerrada con `D-055`, `L-040`, `tokens_billed` y `FakeUsage`
# "registrados" — y `git status` traía **cinco archivos modificados y ningún
# commit**. `git show HEAD:app/tools.py` seguía teniendo el proxy. ⚠️ **Y no es
# cosmético: su `session-starter` arranca en frío y reconstruye del `git diff`**,
# así que un trabajo sin commit **no existe para su protocolo de mañana**.
# 📐 **`L-029` por tercera vez esta semana, y la causa es MÍA.** Tres hallazgos
# buenos llegaron con su sesión ya cerrada de hecho. Llevo el día auditando
# *después* de su commit, así que el hallazgo nace huérfano porque yo lo entrego
# cuando ya no hay sesión donde meterlo. **El arreglo no es documental, es de
# horario: auditar con su sesión abierta.** Eso me toca a mí.
# 💰 **CUATRO BOLSILLOS, y hoy se separaron para que nadie los vuelva a sumar:**
# (1) AWS —IP + EC2 + disco—, con alarma; (2) **la llave de la API de Anthropic
# (`T-075`), SIN TOPE CONOCIDO**; (3) la **suscripción de Claude Code**, que avisó
# de límite mensual y es **el taller, no la obra** —no entra en `A-018` ni en
# `T-067`—; y el presupuesto de AWS como instrumento aparte. → `A-024` y **`T-080`
# bloqueante de `T-079`**: mirar si la llave admite tope **antes** de que `T-079`
# empiece a llamar en bucle. Es `LM.13` con nombre nuevo: un freno que no existe no
# es un freno flojo, es que no está. 📌 **Su versión es mejor que la mía:** yo dije
# *"mira si admite tope"*; ellos escribieron la rama del **no** —contador de
# llamadas y corte duro dentro del guion—, así que hay freno pase lo que pase.
#
# 📍 **DÓNDE SE ARRANCA MAÑANA (paso 8):** `app/api.py` es lo único que le falta a
# `T-076` — cazar `TutorUnavailableError`, mirar `request_sent` y llamar a
# `quota.refund()`. **La excepción ya viaja con el dato correcto y está probada;
# hoy nadie la atrapa, así que la cuota no se devuelve nunca.** Después `T-077`,
# `T-078`, `T-079`.
# 🚨 **`T-080` va ANTES que `T-079`**, y `T-079` es la que empieza a gastar de
# verdad con la llave.
# 📐 **Y lo mío: auditar mientras su sesión está ABIERTA.** Tres días seguidos
# entregando hallazgos huérfanos es un patrón, no mala suerte.
# 🔴 **`T-067` YA SE PUEDE CERRAR** con la aritmética de arriba: no necesita `h1`,
# necesita dos lecturas fechadas del `Costo Acumulado Mensual`, y ya las hay.
# ⏳ **El ritual sigue:** lecturas ancladas a las 12:00 y 23:00 UTC.
# 📅 **Las dos fechas siguen puestas:** ~1 de septiembre (cierra el primer ciclo y
# `Importe previsto` deja de estar ciego) y ≈2026-09-01 como tope de `T-069`.
#
#
# 🔬 **La 63 fue de SUPERVISIÓN PURA, y el rol quedó dicho por él al abrir:**
# *"esta terminal audita, supervisa, recomienda y analiza; en ningún caso ejecuta
# el proyecto"*. Aquí no se escribió una línea de programa. TEAPP pasó de **381 a
# 387 tests** en **cinco commits** (`1365ed1`, `ae2e981`, `e6fa6c4`, `dadbe75`,
# `5187a1c`), y el paso 8 cerró **`T-080`, `T-076`, `T-077` y `T-079`**. Las dos
# suposiciones más viejas del paso 4 se resolvieron el mismo día: **`A-010`
# muerta** (`D-058`) y **`A-011` encogida** tras haberse retirado mal.
# 🔴 **AUDITORÍA DE APERTURA — el arranque que proponían venía con un dato falso.**
# Decían *"`T-080` es lo primero, y bloquea todo lo demás"*. Su propio
# `tasks.md:92` dice **«Bloqueante de `T-079`»**, y solo de esa. El resumen hablado
# lo ensanchó. **Quinta vez en ocho sesiones** que el resumen sale peor que el
# documento (54, 57, 58, 60, hoy).
# 🚨 **Y lo que el resumen NO decía era el agujero:** `app/api.py` no importaba
# `TutorUnavailableError`, así que caía en el `except Exception` genérico → **500
# mudo y la práctica cobrada igual.** 🔑 El daño no era el 500: `request_sent`,
# `D-051`, `D-055`, `FakeUsage`, `tokens_billed` y siete tests —el trabajo de tres
# auditorías del día anterior— estaban **enchufados a nada**. Es `LM.13` en su
# forma más cruda: **no un freno sin ver morder, un freno desconectado del cable.**
# ✅ **Cerrado el mismo día** (`api.py:715`, 503 + `refund` si `not request_sent`),
# y el `except` quedó **antes** del genérico de la 765 — que es la regla del hijo
# primero de la sesión 12 aplicándose sola.
#
# 🌙 **MEDIDO DESDE FUERA lo que ellos dejaron honradamente sin afirmar.** Su
# cierre dijo *"nadie sabe si la máquina está encendida; amanece apagada mientras
# no conste lo contrario"* — correcto y sin inventar, que es `L-038` funcionando.
# Aquí se midió: **5 de 5 sin respuesta, `curl (28) Connection timed out`**, DNS
# resolviendo a `32.199.55.191`. 🔑 **Y es TIMEOUT, no `RST`:** su propio
# instrumento de la sesión 55 separa las dos cosas, y el timeout dice que **no hay
# máquina detrás**, no que Caddy se cayera. La suposición dejó de serlo.
#
# 🔴 **HALLAZGO 1 → su `L-042`: el hermano de al lado sigue decidiendo dinero con
# un proxy.** El bloque nuevo cita en su comentario el camino del 504 como buen
# precedente — y ese camino decide la devolución con `never_started =
# attempt.cancel()` (`api.py:673`), que contesta *"¿llegó a arrancar?"*, no
# *"¿se facturaron tokens?"*. Un tutor que arrancó y falló con 401/429/red —**cero
# tokens**— cobra igual. Alcanzable por la cola, que ellos **midieron** (23
# peticiones a la vez, 3 pagaron por nada). 🔑 **Lo importante es la fecha:**
# `D-023` decidió eso cuando no había forma de saberlo. Hoy sí la hay, y nadie
# volvió a mirar la premisa.
# 🔴 **HALLAZGO 2 → su `C-008`: medir y servir comparten los $6,55.** Tras `T-078`
# la llave vive también en el servidor; el día que una medición agote el saldo, la
# app real devuelve 503 por el camino nuevo —que no deja marca en el marcador— y
# **nada grita**. 🔑 Va contra `D-045`: *el olvido tiene que caer del lado que no
# cobra*, y aquí cae sobre el servicio vivo.
#
# ⭐ **HALLAZGO 3, EL FUERTE: `A-011` se retiró midiendo un reloj que no es el
# suyo.** Tres archivos, todos de ellos: `api.py:649-652` (el tope de 10 s cuenta
# **cola + `respond()` entero**), `english_tutor.py:79-83` (`respond` =
# `count_words` + `judge_grammar` + `add_point`, que escribe en disco) y
# `measure_tutor.py:122-133` (**solo `judge_grammar`, sin cola**). Los 4,72 s son
# **uno de tres trozos**; restar `10 − 4,72` calcula margen sobre un presupuesto
# que paga cosas que la báscula ni tocó.
# 🔑 **Y el rótulo lo delataba: la tabla decía «tiempo por práctica».** Es `L-041`
# —el nombre describe la pista, no el hecho— en su **tercera generación**, y esta
# vez en la cabecera de la medida que retiraba una suposición.
# 🔬 **EL REENCUADRE, que es lo que más valor tuvo del día:** el timeout del
# cliente (8,0 s) mide un **subconjunto** del de la ruta (10 s) y además es menor,
# así que **en una llamada sin cola el de la ruta no puede disparar NUNCA** — el
# cliente corta siempre antes. ⇒ **Los 10 s jamás protegieron de un modelo lento;
# lo único que pueden frenar es la cola.** Su `L-043` decía *"el reloj que va justo
# no es el que vigilábamos"*; lo cierto es más duro: **el reloj que vigilábamos no
# vigila lo que dice su nombre.** ✅ Y eso **respalda** su decisión de no tocar el
# 8,0: ese sí es un freno vivo.
# ✏️ **Corregido el mismo día (`5187a1c`):** `A-011` vuelve a `assumptions.md`
# **encogida**, igual que `A-010`; el rótulo pasa a *tiempo de `judge_grammar`*;
# los números se escriben como **«la peor de diez»** (n=10, dispersión 2,7×); y el
# aviso se metió **en `measure_tutor.py`**, donde alguien lo leerá antes de repetir
# el error, no solo en la bitácora.
#
# 🧭 **`LM.27` — LA LECCIÓN DE MÉTODO DEL DÍA, y la formulación final es SUYA:**
# **una salvedad en el párrafo no arregla un titular falso. El párrafo no se
# relee; la tabla sí.** La salvedad *"no dice nada de la cola llena"* ya estaba
# escrita en `L-043` cuando esa misma entrada tituló *"`A-011` muere"* y tachó la
# fila. 🔑 **Escribir la limitación tranquiliza a quien la escribe** —siente que ya
# lo ha dicho— **y no toca el índice, que es donde vive la conclusión.** Si la
# salvedad contradice al titular, manda la salvedad y el titular **se reescribe,
# no se acompaña.** Es `LM.16` con el mecanismo por fin explicado.
#
# ➕ **DOS VECES EN QUE ELLOS ESTUVIERON POR ENCIMA DE MÍ, y conviene no perderlo.**
#   1. **Mi instrumento era el frágil.** Recomendé cerrar `A-010` con
#      `6,55 − saldo actual`, y les metí prisa *"antes de `T-078`"* porque esa resta
#      se contamina con la siguiente llamada. Ellos leyeron el **consumo fechado**
#      de la consola, que no caduca. La urgencia que les puse sobraba, y sobraba
#      **porque mi método era peor**.
#   2. **Escribieron ellos la objeción que yo traía preparada** (`decisions.md:88`):
#      *"la consola redondea, así que dividir $0,02 entre 10 arrastra hasta un 25%
#      de error — sirve para confirmar, no para proyectar"*. Es `LM.27` aplicada
#      **el mismo día que la aprendieron**, y aplicada al número que sostiene su
#      propia conclusión, que es donde cuesta.
#
# 🔴 **`LM.28` — EL INFORME SE SALTÓ UN COMMIT ENTERO, Y LA DIRECCIÓN ES EL
# DIAGNÓSTICO.** `dadbe75` cierra `A-010`, crea `D-058` y trae el número que decide
# si `T-078` es seguro. **No apareció en el informe.** Ayer `LM.26` dijo que lo
# inventado era la versión cómoda; hoy no se inventó nada, **se omitió** — y lo
# omitido fue el resultado, mientras la enmienda del propio error sobrevivía entera
# y con tabla. 🔑 **Un informe escrito justo después de una corrección se organiza
# alrededor de la corrección: la contrición ocupa el sitio del hallazgo.** Precio
# medible: el dato que no llegó era `$6,55 = 140 días para UNA persona a tope`.
# ✅ **`D-058` es correcta — rehecha la aritmética aquí, no leída:** `2472÷1e6×$5 =
# $0,01236`; `443÷1e6×$25 = $0,011075`; total **$0,023435** (su $0,0234); por
# práctica **$0,00234**; 20/día **$0,0469**; 180 días **$8,44**; y
# `$6,55 ÷ $0,0469 = 139,7` → sus **140 días**. Los seis números salen.
# 🚨 **Y ESO ABRE UN SEGUNDO RELOJ QUE NADIE HA PUESTO EN EL CALENDARIO.** Hasta hoy
# el proyecto tenía uno: los créditos de AWS, que vencen el **2027-02-06**. El saldo
# de Anthropic se agota **antes** —hacia finales de diciembre bajo el supuesto de
# tope— y esos 140 días-persona son el techo **compartido entre servir y medir**,
# con el paso 9 entero por delante, que es todo medición de modelos.
#
# ⚠️ **LO QUE NO VERIFIQUÉ, y queda como pregunta de reparto:** **los 387 tests no
# se corrieron aquí.** La corrección suya de la 59 dice que esta terminal no prueba
# ni ejecuta; la 60 acotó que medir *desde fuera* sí entra, y correr su `pytest` cae
# del otro lado. Lo que sí se hizo es leer el `git show --stat`. 📌 **Importa
# decidirlo:** en la sesión 51 correr la suite aquí cazó un número falso (decían
# 342, eran 348). **Pregunta abierta, planteada y sin contestar.**
# ✅ **Y lo mío de ayer se cumplió: se auditó con su sesión ABIERTA.** Cuatro
# entregas, y las cuatro entraron en commits del mismo día (`ae2e981` recogió
# `C-008` y `L-042`; `5187a1c`, la reapertura de `A-011`). **Cero hallazgos
# huérfanos** — primera sesión sin `L-029` en cuatro días.
#
# 📍 **DÓNDE SE ARRANCA MAÑANA (paso 8):** **`T-078`** — que la llave llegue al
# servidor por `install.sh`, con permisos cerrados y sin pasar por el repo.
# 🚨 **Y no se hace sin que `C-008` esté escrita en `tasks.md` con el número
# delante:** el día que la llave viva en el servidor, **el saldo deja de tener un
# solo consumidor.** 140 días-persona a tope, menos lo que se lleve cada báscula.
# 🔴 **`L-042` sigue abierta:** el camino del 504 decide dinero con `cancel()`, un
# proxy, teniendo `request_sent` al lado. Es `D-023` con la premisa ya comprobable.
# 🔴 **`A-011` encogida, y lo que falta es la COLA** — el escenario que el timeout
# de la ruta sí gobierna. Sin concurrencia medida, el 10 sigue sin corrida detrás.
# ⏳ **El ritual de AWS sigue:** lecturas ancladas a las 12:00 y 23:00 UTC.
# 📅 **Las fechas puestas:** ~1 de septiembre (cierra el primer ciclo de AWS y
# `Importe previsto` deja de estar ciego), ≈2026-09-01 como tope de `T-069`, y
# **el nuevo: el saldo de Anthropic hacia finales de diciembre.**
#
#
# 🔬 **La 64 fue de SUPERVISIÓN, y el trabajo del día salió de preguntar de dónde
# salía un número.** Aquí no se escribió una línea de programa. TEAPP pasó de
# **387 a 395 tests** en un commit (`89d00fd`, verificado en `origin`, árbol
# limpio), y cerró `T-082` y `T-083`.
#
# 🐛 **PRIMERO UN ERROR MÍO, Y ESTABA ESCRITO EN SU REPO EL DÍA ANTERIOR.**
# Invoqué la skill `claude-api` para consultar documentación. Su `D-056`, del
# **10 de agosto**, lo prohíbe con la medición dentro: esa skill llevó una sesión
# **de 55 K a ~340 K tokens** porque vuelca treinta documentos cuando TEAPP hace
# **una** llamada. La escalera que dejaron escrita es (1) `ctx7`, (2) la página
# suelta, (3) la skill entera y solo diciéndolo en voz alta. 🔑 **`LM.20` conmigo
# de protagonista por segunda vez en seis sesiones** — y esta vez la razón no
# estaba en un archivo lateral: estaba en `decisions.md`, fechada el día antes,
# en el repo que vengo a auditar. Guardado ya en memoria permanente, no solo aquí.
#
# 📌 **Y una lección de trato que repite la de la 59, casi con las mismas
# palabras.** Le entregué el procedimiento para la consola —qué mirar, dónde
# hacer clic— y contestó *"pero no entiendo qué estamos buscando con esto"*.
# Tenía razón: le había dado el **cómo** sin el **qué se quiere averiguar**. Se
# rehízo con la analogía de la tarjeta de débito única (el negocio y el
# laboratorio pagando del mismo plástico) y entonces sí. 🔑 **Segunda vez en seis
# sesiones que el mismo fallo aparece en el mismo sitio: cuando la tarea es una
# comprobación en pantalla, se me va el concepto y arranco por el procedimiento.**
#
# 🟢 **`T-082` CERRADA CON `D-059`, y la documentación decidió en contra de lo
# que yo esperaba.** Fui a buscar si la consola de Anthropic permitía **dos
# bolsillos** —uno para medir, otro para servir—. La respuesta es **no**: los
# espacios de trabajo admiten tope de gasto propio, pero *"You can set workspace
# limits lower than (but not higher than) your organization's limits"* y
# *"Organization-wide limits always apply"*. 🔑 **Es un reparto del mismo techo,
# no un bolsillo aparte** — el saldo de $6,55 es de la organización y sigue
# siendo uno solo. Por eso la partición tuvo que bajar al código.
#
# 🔴 **MI HALLAZGO 1 — el titular decía «desbloquea `T-078`» y el freno no
# existía.** `D-059` decidía dos capas, y la única que protege el saldo —el corte
# duro en `measure_tutor.py`— **no estaba escrita**. Ellos lo decían honradamente
# en el cuerpo (*"`C-008` está decidida, no arreglada"*), pero el índice de
# `decisions.md` —lo que el `session-starter` lee en frío— decía «desbloquea».
# 🔑 **Una decisión no frena un bucle.** Es `LM.27` **un día después de que él la
# formulara**: *la salvedad en el párrafo no arregla un titular falso; el párrafo
# no se relee, la tabla sí.* Corregido el mismo día.
# 🔴 **MI HALLAZGO 2 — `D-059` creaba una segunda llave y no decía cuál viaja.**
# `T-078` dice *"que la llave llegue al servidor"*, una frase escrita cuando solo
# había una. Quedó escrita la asignación, y con ella el porqué de dejar servir en
# el espacio por defecto **como decisión y no como accidente**.
#
# ⭐ **EL HALLAZGO DEL DÍA ES DE ELLOS Y SALIÓ DE MI EMPUJÓN, y es el mejor de la
# semana: un número que parecía medido y salía de un `len()`.** Ellos propusieron
# poner el tope en **10**, *"que ya lo tienes medido de `T-079`"*. Le discutí que
# diez era **el tamaño de una corrida, no lo que se puede gastar** — dos preguntas
# distintas— y que el tope tenía que salir del saldo. Al ir a cambiarlo
# encontraron que `MAX_CALLS = 10` **ya existía** en `measure_tutor.py:49`, y que
# lo hacía cumplir un `SENTENCES[:MAX_CALLS]`. 🔑 **`SENTENCES` tiene exactamente
# diez frases: el recorte no recortaba nada. Freno decorativo.** Y el diez de la
# medición tampoco venía de medir — la tanda hizo diez llamadas **porque había
# diez frases**. → su `L-044`, con los tres disfraces del número (constante, tope
# comentado citando tres entradas, y argumento hablado — este último marcado como
# suyo). **La regla que deja: un número que decide dinero se escribe como la
# operación que lo produce, no como su resultado.**
# ✅ **Y así quedó, verificado por mí en el código y no en el informe:**
# `BUDGET_PER_RUN_USD = 0.25` (decisión de dinero, suya) `÷ COST_PER_CALL_USD =
# 0.00234` (medido, `D-058`) `= MAX_CALLS_PER_RUN = 106`, con un test que
# comprueba que sigue siendo la división. `CallBudget.spend()` cobra **antes** de
# llamar y vive dentro de `RecordingClient`, el paso obligado. Tres sabotajes
# vistos en rojo, y el que justifica el archivo es el segundo: `main()` construye
# un `RecordingClient` por vuelta, así que un contador dentro del cliente **se
# reinicia en cada frase y el guion seguiría midiendo bien**.
#
# 📉 **Mi tercera aportación fue poner número a un hueco que estaba escrito en
# prosa.** El alcance del freno lo escribieron bien (*"no protege de correr el
# guion 40 veces a mano"*), pero **$6,55 ÷ $0,25 = 26 corridas**. 🔑 *"No protege
# de correrlo muchas veces"* se lee como *"habría que ser tonto"*; **`26` se lee
# como lo que es** — y el paso 9 es comparar modelos, o sea correr el guion una
# vez por modelo. Puesto en tres sitios: índice, cuerpo y docstring del código.
#
# 🧭 **`LM.29` — LA LECCIÓN DE MÉTODO DEL DÍA, y es sobre la lista de tareas.**
# `T-082` pedía **decidir**, así que una decisión la cerraba — y con eso `T-078`
# quedaba «desbloqueada» sin que existiera ni un freno. Nadie mintió: la tarea
# decía *decidir* y se decidió. 🔑 **Una lista de pendientes escribe igual «lo que
# hay que resolver» y «lo que hay que construir», y solo lo segundo protege de
# algo. Cuando un desbloqueo cuelga de una decisión en vez de una pieza, el hueco
# se abre sin que nada se ponga rojo.** Es `LM.19` con el mecanismo explicado
# (*la lista dice qué falta por construir, nunca dijo qué falta por saber* — aquí,
# al revés: dijo lo que faltaba por saber y se leyó como construido). El arreglo
# quedó en `tasks.md`: `T-078` cuelga ahora de *"la capa 1 existe y se le ha visto
# morder"*, no de *"la partición está decidida"*.
#
# ✅ **Y lo mío se cumplió por segundo día: se auditó con su sesión ABIERTA.** Los
# tres hallazgos llegaron con dos archivos modificados y sin commit, y los tres
# entraron en `89d00fd`. **Cero hallazgos huérfanos.**
#
# 📍 **DÓNDE SE ARRANCA MAÑANA (paso 8): `T-084`, y es ACCIÓN SUYA en el
# navegador** — crear el espacio de trabajo para medir, con su llave propia y su
# límite de **velocidad** (no de gasto). 🚨 **Bloquea `T-078`, y no por el saldo
# sino por el reparto de llaves:** hoy solo existe una llave, así que si `T-078`
# corriera antes, al servidor viajaría la misma que usa `measure_tutor.py` y se
# perderían las dos cosas que la capa 2 compra —revocarla sola y la contabilidad
# por `workspace_id`—. Después, `T-078`.
# 🔴 **`C-008` quedó cerrada A MEDIAS a propósito**, con las dos mitades separadas
# en su propia fila: tapado el fallo mudo, abierta la partición.
# 🔴 **Sigue abierto del paso 8:** `T-079` a medias (falta cronometrar `/practice`
# entera **con concurrencia**, que es el escenario que el timeout de la ruta sí
# gobierna), `L-042` (el 504 decide dinero con `cancel()`, un proxy, teniendo
# `request_sent` al lado) y `T-081` (renombrar `request_sent`).
# ⏳ **`A-025` sin comprobar y no bloquea nada:** si el tope por espacio de trabajo
# es blando en primera parte. La frase está leída en la página de AWS, no en la de
# primera parte, y por eso la escribieron como **suposición y no como razón** —
# que es la mejor pieza de disciplina del día.
# ⏳ **El ritual de AWS sigue sin tomarse hoy:** lecturas ancladas 12:00 y 23:00
# UTC. La última es la séptima, del 11 (`Costo Acumulado Mensual` 0,74 US$).
# 📅 **Tres fechas puestas:** ~1 de septiembre (cierra el primer ciclo de AWS),
# ≈2026-09-01 tope de `T-069`, y el saldo de Anthropic hacia finales de diciembre.
#
#
# 🔎 **La 65 fue de SUPERVISIÓN, y el saldo del día es un experimento que NO se
# corrió.** Aquí no se escribió una línea de programa. TEAPP hizo **cinco commits**
# (`e233fc6`, `b257c7b`, `3626c95`, `a1c015c`, `196e3eb`, todos en `origin`),
# cerró `T-084` y abrió `T-085` y `T-086`. La suite no se movió de **395**: el
# día entero fue decidir, medir y no gastar.
#
# 🔴 **EL HALLAZGO DEL DÍA: el `23` de `T-079` era un FÓSIL, y la corrida habría
# salido VERDE midiendo cero.** Su plan era lanzar 23 peticiones a la vez para
# forzar cola y ver disparar `TUTOR_TIMEOUT_SECONDS = 10.0`. El 23 no era
# inventado —está medido, en `[L-013]` y en `api.py:689`: *"23 peticiones, 20
# llegaron al tutor, 3 pagaron por nada"*—. 🔑 **Pero se midió contra un pool de
# 20**, que era lo que `ThreadPoolExecutor()` sacaba de las CPUs de aquella
# máquina, y **ellos mismos lo arreglaron**: hoy `TUTOR_POOL_SIZE = 40`
# (`api.py:184`), puesto a mano justo por eso. Con 40 sitios, 23 peticiones entran
# todas y **nadie hace cola**. El cronómetro habría medido una espera de cero, el
# timeout no habría disparado, y la conclusión —*"los 10 s aguantan"*— habría
# salido en verde **sobre un escenario que no ocurrió**, gastando saldo real para
# producirla. 📌 **Hermano de `L-044` con UN DÍA de diferencia y la forma
# invertida:** ayer el número nunca midió nada (era un `len()`); hoy midió bien y
# **caducó**. La pregunta que caza las dos es la misma — *¿qué pregunta contestó
# el día que se escribió, y es la misma que le hago hoy?*
# 🔬 **Y debajo había algo peor, que es lo que reformula la tarea: la cola quizá
# no pueda formarse NUNCA.** El invariante de `api.py:172` —escrito por ellos—
# dice que el pool iguala las 40 fichas de `anyio`, así que la petición 41 espera
# **antes de que arranque la ruta**, o sea antes del `submit` y antes de que el
# reloj empiece a contar. ✅ **No es inferencia mía: hay un test que compara los
# dos números** y se pone rojo si dejan de coincidir; y `api.py:573` confirma que
# `practice` es una ruta **síncrona**, que es lo que sostiene la cadena.
# ➕ Aporte propio que aprieta más: `/practice` **no es la única ruta síncrona**
# —`/me`, el login— así que caben **menos** de 40 prácticas a la vez, no 40.
# 🔑 **Junto con lo de la 63 (el cliente corta a 8,0 s, la ruta a 10), los 10 s no
# pueden disparar ni por cola ni por modelo lento.** Lo único que les queda es que
# `respond()` **fuera del modelo** se coma más de 2 s. → **`T-079` reformulada: la
# mitad que falta ya no es cronometrar, es DECIDIR qué hacer con un freno que no
# gobierna nada.** Se lee y se decide; no se mide.
# ⭐ **EL QUINTO PUNTO LO PUSIERON ELLOS Y ES LA MEJOR LÍNEA DEL DÍA:** el
# experimento **ya estaba hecho y era gratis**. `tests/test_api.py:1043` deja el
# pool en **1** *"para que el segundo tenga que hacer cola"*. 🔑 **Para provocar
# contención se quita sitio, no se añade carga** — cerrar cajas, no traer
# clientes. Lo primero es un test con tutor de mentira y cuesta cero; lo segundo
# son llamadas reales contra un saldo de $6,55.
# ✏️ **Corrección mía sobre su propio hallazgo, y evitó cerrar `T-079` de más:**
# ese test **cambia el timeout a 0,2 s**, así que prueba el MECANISMO (quien se
# queda en la cola no paga) y **no dice nada del número 10**. Son dos preguntas y
# solo estaba contestada la primera. Sin esa fila separada, el titular *"el
# experimento ya estaba hecho"* habría tapado la mitad viva. `LM.27` otra vez.
#
# 🐛 **UN DATO FALSO EN SU RESUMEN, Y ESTABA ESCRITO EN SU PROPIO ARCHIVO.**
# Dijeron *"`claude-opus-5` **respondiendo en vivo**"* dentro del párrafo de
# producción. **En el servidor la llave está VACÍA** (`install.sh:188`), y su
# `tasks.md:87` lo dice con todas las letras. El tutor responde **en local**.
# **Sexta vez en nueve sesiones que el resumen sale peor que el documento**, y
# otra vez en la dirección de `LM.26`: se coló la versión cómoda.
#
# 💰 **`T-084` CERRADA, y `D-061` es de las mejores entradas del proyecto.**
# Espacio `teapp-measure` con llave propia y freno de velocidad para Opus 5 en
# `50 / 20.000 / 5.000`, **con la derivación dentro**: `measure_tutor.py:208` es un
# `for` secuencial (verificado), la más rápida de `[A-011]` son **1,72 s** ⇒ techo
# físico `60 ÷ 1,72 = 35/min`, y con los `247 + 44` tokens de `[D-058]` salen
# ~8.650 y ~1.540 por minuto. **Elegir el MÍNIMO fue lo correcto**: para un techo
# de velocidad el caso peor es el más rápido — al revés que para un timeout.
# 🚨 **La regla 6 mordió en directo:** la documentación decía que `Default` hereda
# `2.000.000/400.000`; la consola de ESTA cuenta dijo `1.000/500.000/80.000`.
# **Gana la consola** — el instrumento de la cuenta, no una lista general.
# ✅ **Y la llave se confirmó POR CABECERAS, no por fe:** `requests-limit: 50`,
# `requests-remaining: 49`. **Catorce tokens para no suponer**, después de
# descartar tres instrumentos gratis que no distinguían una llave de otra.
# ➕ **Y fueron más lejos que mi aviso:** yo dije *"cuidado con el `effort`, que el
# paso 9 es quien mueve esa palanca"*; ellos escribieron **"cada modelo nuevo
# necesita su fila con su propia medida antes de la primera tanda"**, con Haiku
# nombrado. Mejor formulado que el mío.
# ✏️ **Corrección menor mía:** decían *"holgura de ~1,5×"* y las tres filas llevan
# **1,43× / 2,31× / 3,25×**. Los números están bien; **la etiqueta no describía su
# propia tabla.** `LM.27` en pequeño — se arregla la frase, no los números.
#
# 🌩️ **`L-046` — nueve `529 Overloaded` seguidos en ~50 s, y es la primera vez que
# se VE lo que `D-051` decidió sobre el papel.** En producción un 529 llega con
# `request_sent=True` (`tools.py:320`): **se cobra la cuota y no se devuelve**, y
# con `MAX_RETRIES = 0` una racha así le come prácticas de sus 20 **sin darle un
# solo veredicto**. Hoy no le pasa a nadie porque en el servidor no hay llave.
# 📌 Y matan una vía de diagnóstico: los 529 **no traen cabeceras
# `anthropic-ratelimit-*`** — comprobado, no supuesto.
#
# 🚦 **MI RECOMENDACIÓN DEL CIERRE, y la aceptaron: NO hacer `T-078` hoy.** El
# argumento estaba escrito en lo que acababan de commitear — `D-061` dejaba
# abierto *"tope de gasto por espacio de trabajo... el freno real es el saldo de
# $6,55 y un tope mensual bajo sí mordería antes"*. 🔑 **`T-078` es el momento en
# que el saldo pasa a tener DOS consumidores**, y el lado que sirve no tiene freno
# propio: `CallBudget` solo vive en `measure_tutor.py` (verificado: nada de `app/`
# lo importa). Esa decisión **cuesta cero antes y deja de ser gratis después**.
# → `T-085` nueva, **delante de `T-078`**.
# 📐 **Y un detalle de `LM.29` que conviene no perder:** `T-078` colgaba de *"la
# capa 1 existe y se le ha visto morder"* — cierto, **pero la capa 1 protege al
# laboratorio y `T-078` es una tarea del lado que sirve**. La puerta y la cerradura
# no eran de la misma habitación. (Exposición real modesta: con un usuario a 20/día
# el techo son $0,047 diarios. El orden importa, no el susto.)
# 🎁 **Y el cierre suyo encontró algo que yo no tenía: `[A-025]` dice que el tope
# de gasto por espacio es BLANDO y tarda ~2 h en aplicarse.** Eso cambia el terreno
# de `T-085` — un freno con dos horas de retraso protege menos de lo que parece.
# Se decide mañana con ese dato delante, que es exactamente para lo que sirvió
# aplazarlo.
#
# 🚨 **CASI SE CIERRA SIN `push`, y lo cacé mirando el árbol.** Dijeron *"árbol
# limpio, cuatro commits hoy"* — y `git status -sb` decía **`ahead 4`**. Árbol
# limpio **no es** trabajo respaldado. Corregido en el cierre: `196e3eb` y los
# cuatro anteriores están en `origin`. 📌 **Tercera vez que el estado del árbol se
# reporta como si fuera el estado del respaldo.**
#
# 🔴 **EL HALLAZGO DE REPARTO DEL DÍA, Y ES DE ESTE ARCHIVO: las lecturas de AWS
# viven en el repo que NO es dueño de la suposición.** El cierre suyo lo dijo
# claro: las lecturas del 11 (`0,74`) y del 12 (`1,12`) **no están en
# `assumptions.md` ni en `[A-018]`** — llegaron por conversación y ahí se quedaron.
# ⚠️ **Pero no se perdieron: están AQUÍ**, en este archivo (líneas 640 y 997), que
# es de Edu_TripleS. 🔑 **`A-018` es una suposición de TEAPP y su historial de
# lecturas vive en el repo del método.** Es la misma frontera que reventó en la 58
# con `L-013` contra `LM.13`: **el reparto de la sesión 43 —aquí el porqué, allá lo
# que el programa hace— no dijo dónde van los DATOS que él trae del navegador.**
# El dato entra por esta terminal y su dueño está en la otra. → `T-086`.
#
# 💵 **La lectura de hoy: `Costo Acumulado Mensual` = 1,12 US$** (la séptima fue
# `0,74` el 11). **Ninguna de las dos lleva hora**, así que el ritmo sale con una
# banda en vez de un número: entre `0,011` y `0,032` US$/h según hayan pasado 36 h
# o 12 h. ✅ **Y lo bueno es que la conclusión de `T-067` sobrevive a la banda
# ENTERA:** entre **$46 y $137** de los $200 en 180 días. **Los seis meses caben en
# las tres ramas**, y sin usar ninguna lista de precios. No hace falta afinar el
# número para decidir — hace falta la hora para poder cerrarlo.
# 🔴 **`Importe utilizado` sigue en `0,00`: SEXTA seguida.** Con 1,12 US$ gastados
# contra un umbral de `0,01`, el presupuesto va **112 veces cubierto y mudo**. Ya
# no es sospecha: **ese instrumento no está mirando el gasto real.**
# (`Importe previsto` en `—` es lo documentado hasta que cierre el ciclo, ~1 sep.)
#
# 🌐 **`A-017` episodio 9, medido aquí sin buscarlo:** dos `000` y tres `200` en la
# misma ráfaga. Y la máquina viva: `Server: uvicorn` + `Via: 1.1 Caddy`, `/me` →
# `401`. La encendió él.
#
# 📍 **DÓNDE SE ARRANCA MAÑANA (paso 8):** **`T-085`** — decidir el tope de gasto
# de `teapp-measure` contra el saldo real de **$6,55**, no contra los $500
# mensuales, **y con `[A-025]` delante** (es blando y tarda ~2 h). Después
# **`T-078`** (la llave de `Default` al servidor), y luego `T-079` reformulada.
# 🔴 **`T-086`:** anotar la **hora UTC** de la lectura de AWS, y meter las dos
# lecturas huérfanas (11 y 12) en `[A-018]`, que es su sitio.
# 🔴 **Sigue abierto:** `L-042` (el 504 decide dinero con `cancel()`, un proxy,
# teniendo `request_sent` al lado), `T-081` (renombrar `request_sent`) y `C-008`
# cerrada a medias a propósito.
# ✅ **Lo mío se cumplió por tercer día: se auditó con su sesión ABIERTA.** Los
# hallazgos entraron en commits del mismo día. **Cero hallazgos huérfanos.**
# ⏳ **El ritual sigue:** lecturas ancladas a las 12:00 y 23:00 UTC, **con la hora
# escrita**.
# 📅 **Tres fechas puestas:** ~1 de septiembre (cierra el primer ciclo de AWS),
# ≈2026-09-01 tope de `T-069`, y el saldo de Anthropic hacia finales de diciembre.
#
# 🔎 **La 66 fue de SUPERVISIÓN, y es la primera en que un diseño se construyó
# CONVERSANDO entre las dos terminales, turno a turno.** Aquí no se escribió una
# línea de programa. TEAPP hizo **cuatro commits** (`c071530`, `d4c40eb`,
# `be30bd4`, `32f3314`, todos en `origin`), cerró `T-085` y dejó `T-078`
# **abierta a propósito**. Suite reportada en **410** (venía de 395) —
# **reportada, no verificada aquí**: ver `D-064` abajo, que nace justo de esto.
#
# 🔴 **HALLAZGO 1 — el tope de $2 decía morder un flanco, y el número que lo
# desmiente estaba entre paréntesis en su misma frase.** `[D-062]` cerró `T-085`
# con un tope de gasto de `$2,00/mes` para `teapp-measure`, bien razonado: no es
# corte, es **reserva**, porque `Default` no admite tope y el único suelo para
# producción es indirecto. Pero afirmaba que lo único que sí mordía era el flanco
# de las 26 corridas de `[D-060]` — y al lado escribía `26 × 106 × 1,72 s ≈ 79
# min`. 🔑 **79 está DENTRO de la ventana ciega de 120** (`[A-025]`). Por su
# propia regla —*lo que no se puede comprobar no cuenta como freno*— ese flanco
# tampoco queda cortado. **Lo que el tope muerde no son «las 26 corridas»: es el
# gasto LENTO**, el repartido en más de dos horas. Lo mismo le pasaba al titular
# `$4,48 ≈ 95 días`, cierto contra gasto lento y falso contra una corrida
# desbocada. 📌 **`LM.16` otra vez** (`[L-043]`): el matiz en el párrafo, el
# titular sin él — y el párrafo no se relee, la tabla sí. Corregido el mismo día
# **en cuerpo e índice**, verificado aquí. El flanco sin dueño quedó como
# `[A-026]`, declarado sin dueño en vez de tapado.
#
# 🔴 **HALLAZGO 2 — y este es de método: el número con el que se identifica una
# llave no puede ser un número que no controlas.** Yo propuse que `install.sh`
# exigiera `requests-limit: 1000` (la firma de `Default`) antes de mandar la
# llave al servidor. **Ellos le dieron la vuelta y tenían razón:** el 1.000 lo
# pone Anthropic y `[D-061]` lo vio desmentirse en un día. Colgar el freno del
# despliegue de ahí fabrica un **rojo falso con fecha desconocida**, *y un freno
# que muerde en falso se acaba quitando con red y todo*. La regla buena es
# **abortar si vale `50`** —la firma del laboratorio, número suyo, escrito por
# ellos ayer—: **denegar lo conocido-malo en vez de exigir lo conocido-bueno.**
# ⚠️ **Lo que se paga, y quedó escrito:** exigir el 1.000 falla en **rojo falso**
# (ruidoso, alguien mira); abortar con el 50 falla en **verde falso** (mudo: el
# `429` de dentro de tres semanas). Se acepta porque el riesgo real es
# **exactamente uno** — mandar la del laboratorio porque en el `.env` local las
# dos llaves **se llaman igual**.
# 🚨 **Y el disparador de ese verde falso ya estaba predicho por escrito** en
# `[D-061]` (*"cada modelo nuevo necesita su fila"*, con Haiku nombrado): **ese
# 50 se va a mover en el paso 9.** De ahí la condición no opcional: el 50 pasa a
# vivir en dos sitios, que es el bicho de la sesión 33.
# ⭐ **Y el remate lo pusieron ellos, y es la mejor línea del día:** *un
# acoplamiento se anota **donde va a estar mirando quien lo rompa**, no donde lo
# entendió quien lo creó.* El día que suban el freno a 80 para medir Haiku no van
# a abrir `[D-063]` —no están desplegando— van a abrir `[D-061]`, que es donde
# vive el número. Por eso el aviso tenía que estar en las **dos** entradas.
# Escrita como `L-047` **porque se la reclamé en el momento**: estaba solo en el
# chat, y ahí es donde `L-029` mata las cosas buenas.
#
# 🔴 **HALLAZGO 3 — el sabotaje que salió VERDE, y es lo mejor del día aunque no
# sea mío.** De los tres sabotajes a `check_api_key.py`, el tercero —mover la
# comprobación detrás de la escritura— **pasó en verde**. El test buscaba la
# primera línea que nombrara el archivo, y la primera era **un comentario doce
# líneas antes de la llamada**: se cumplía solo, pasara lo que pasara. Un test
# con **nombre correcto, aserción correcta y verde**, que habría entrado en la
# suite como un guardián más. 🔑 **El sabotaje no auditó la capa: auditó al
# vigilante.** Es `LM.15` en su forma más pura —*nadie audita un verde*— y lo
# cazó **sabotear**, no leer. Quedó como `[L-048]`.
#
# ✏️ **ME EQUIVOQUÉ YO, y conviene que quede escrito.** Dije que `install.sh`
# dejaba una ventana entre escribir el `.env` y hacerle `chmod`, apoyándome en un
# comentario de la línea 163 y en el `chmod` de la 211. **Falso, y lo comprobé
# leyendo el archivo:** la línea 168 hace `install -m 600 … /dev/null`, el
# archivo **nace vacío y ya cerrado**, y el `cat >` no toca permisos; el `chmod`
# de la 211 cierra el **otro** camino. 🔑 **Pero el fallo tiene forma, y es la que
# yo mismo audité un mensaje antes:** ese comentario dedica **cuatro líneas al
# peligro y una a la solución**, y la del peligro va primero. Leí el titular y
# reconstruí un problema que el código tenía resuelto. **`LM.16` cometido por mí
# a la vuelta de haberlo señalado.** 📌 Regla que sale: en un comentario, **la
# primera línea dice el ESTADO; el riesgo baja a explicación.**
#
# 🔑 **`D-064` — SE CERRÓ LA PREGUNTA DE REPARTO QUE LLEVABA ABIERTA DESDE LA
# 63.** Hasta hoy esta terminal no corría su `pytest` (la 59 dijo *no prueba ni
# ejecuta*, la 60 acotó *medir desde fuera sí*), y quedó **planteada y sin
# contestar** en las líneas 862–867 de este archivo. **Ahora sí: puedo correr
# `pytest -q`.** El argumento que lo cierra es suyo y es mejor que el mío: *una
# terminal que audita y no puede medir solo sabe releer; releer caza un
# razonamiento torcido, pero un número solo lo caza una corrida* — y la sesión 51
# lo probó (decían 342, eran **348**). **Es la regla 6 aplicada al auditor.**
# ⚖️ **El disparador es el suyo, no el mío, y por qué:** yo propuse *"correr
# cuando el número sostenga una decisión"* — exige **predecir el futuro**, y ese
# hueco se resuelve siempre para el lado cómodo. El suyo — **"correr siempre que
# vayas a escribir o citar un número de la suite"** — se comprueba **mirando el
# presente**: ¿estoy tecleando un número? sí o no. 📌 **Transferible: un
# disparador que se comprueba observando lo que haces vale más que uno que se
# comprueba estimando lo que importará.** Misma familia que `[D-060]` (cobrar
# antes de llamar) y que el `install -m 600`: el momento lo fija la mecánica, no
# el criterio de alguien.
# ➕ **Dos remates míos que entraron:** (1) la regla abre un escape —*no escribir
# el número*—, así que solo hay **dos formas legales** de nombrar la suite:
# **medido aquí** con su número, o **reportado, no verificado**, con esas
# palabras; nunca una afirmación sin etiqueta. (2) **Un número solo se compara
# contra el mismo commit**: si mi corrida discrepa, la primera hipótesis no es
# que mientan, es que corrí otro árbol — así que se registra el commit sobre el
# que se corrió.
#
# 🐛 **UNA TAREA MUERTA VIAJÓ EN EL TRASPASO, y la cazó su cerrador.** El reporte
# de inicio traía `T-074` (comprobar el apagado automático) como pendiente.
# **Está cerrada desde el 2026-08-10**, con testigo directo en el journal de
# systemd. La arrastraron del reporte sin abrir la línea — `[L-034]` en pequeño:
# *una tarea que aparece dos veces en una lista deja de auditarse, y la lista se
# lee más rápido que el archivo*. ⚠️ **Y me pasó por delante sin que la
# preguntara.** No la repetí, pero tampoco la audité: entró por esta terminal y
# salió intacta. **Séptima vez en diez sesiones que el resumen sale peor que el
# documento** — y la primera en que el que lo corrige es el propio cerrador,
# mandando la evidencia del archivo en vez de la del traspaso.
#
# ✅ **Y esta vez el árbol se cuidó, después de que lo señalara dos veces:** a
# mitad de sesión el trabajo estaba **escrito y sin commitear**, y más tarde el
# código nuevo estaba en **`??`** —sin rastrear, invisible a un `diff`, y un
# `git clean` se lo lleva—. Se corrigió en el momento. 📌 **Quinta y sexta vez
# que el estado del árbol se reporta como el estado del respaldo**, hoy en dos
# formas distintas el mismo día.
#
# 📍 **DÓNDE SE ARRANCA MAÑANA (paso 8):** **`T-078`, y es lo NO hecho:** correr
# `check_api_key.py` contra la red real **dos veces** — **puerta 3** con la llave
# del laboratorio y **puerta 0** con la de `Default`. 🔑 **Una sola corrida no
# vale**: con la del laboratorio la única salida posible es la 3, así que ese 3
# no distingue *"la identificó"* de *"acierta por casualidad"*. **Hace falta el
# control al lado** — es `T-060b` de la 56 otra vez (*sin nada escuchando en el
# 8000, «cerrado» salía igual con el cortafuegos abierto que cerrado*). **410
# verdes y una corrida no cierran `T-078`**, y la condición está escrita **en
# tabla dentro de `[D-063]`**, no en una nota suelta.
# 🔴 **Siguen abiertos:** `T-079` (a medias: ya no es cronometrar, es **decidir**
# qué hacer con un freno que no gobierna nada), `T-086` (la hora UTC de las
# lecturas de AWS + las dos huérfanas del 11 y el 12), `[A-026]` (las corridas
# repetidas, sin dueño), `L-042`, `T-081` y `C-008` cerrada a medias.
# ✅ **Lo mío se cumplió por cuarto día: se auditó con su sesión ABIERTA.** Los
# tres hallazgos entraron en commits del mismo día. **Cero hallazgos huérfanos.**
#
# 🔎 **La 67 (2026-08-13) fue de SUPERVISIÓN, y arrancó desmontando el propio
# reporte de inicio.** TEAPP cerró con `699f2b2` en `origin`. `T-078` sigue
# **abierta**, ahora por dos motivos distintos —uno del proyecto (`[D-065]`: la
# llave buena es otra) y uno ajeno (Anthropic saturado)—, y eso está bien
# separado. Suite **410, MEDIDA AQUÍ** sobre `32f3314` con la `.venv` de TEAPP:
# coincide con la suya. **Primer uso de `[D-064]`**, y la regla funcionó sola —
# corrí porque iba a escribir el número, no porque el número decidiera nada.
#
# 🧟 **HALLAZGO 1 — `T-074` volvió por SEGUNDA vez, y esta vez traía factura.**
# Ayer viajó en el traspaso como duplicado inofensivo y la cazó su propio
# cerrador. Hoy volvió **de prioridad número 1**, con una consecuencia encima:
# *"cuatro días de retraso, y esa máquina encendida se come el plan gratuito"*.
# Está **cerrada desde el 2026-08-10** (`tasks.md:81`, ✅, con el journal de
# systemd dentro) y la frase **no venía de ninguna corrida**. Medido aquí antes de
# opinar: `443` por nombre y por IP → `000` con TIMEOUT de 12 s y 10 s, `22` sin
# respuesta. **Dos puertos independientes, los dos mudos:** nada sostiene *"la
# máquina encendida"*. Y falla por el otro lado también — con la EC2 apagada lo
# que sigue cobrando son **la IP elástica y el volumen EBS**, no las horas de
# instancia: **acusaba a la pieza equivocada.** → `LM.30`.
# 🔑 **El mecanismo, y es lo que hay que guardar:** la caza de ayer **vivió solo
# en el chat**. El puntero viejo siguió en el disco en DOS sitios —línea 12 de
# `progress.md`, campo `siguiente acción`, y la cola de `[S-044]`— y el arranque
# de hoy lo volvió a servir. **`L-029` con las tres cosas a la vez:** lo huérfano
# no fue una decisión buena, fue **la caza de un error**; y lo huérfano no se
# queda quieto, **vuelve más fuerte**.
# ⭐ **Y la formulación final es suya:** *una corrección que no toca el disco es
# una corrección que mañana no existe.* Yo le añadí el anillo de fuera —estaba
# escrita y **sin commitear**, o sea a un `git checkout` de distancia— y ahí sí
# tuvieron razón ellos al no adelantar el commit: **el protocolo cierra dentro de
# la sesión, y adelantarlo habría sido fabricar urgencia el mismo día en que
# escribimos que la urgencia no se audita.**
#
# 🔴 **HALLAZGO 2 — el círculo vicioso del identificador, y es la aportación de
# método del día.** Iban a averiguar de quién era cada llave **preguntándoselo al
# guion**, y lo que se estaba auditando era que el guion sabe de quién es cada
# llave. **Eso sale verde pase lo que pase**: la respuesta queda definida por el
# instrumento que se juzga. 🔑 **Es `T-060b` con la forma exacta** —allí *"cerrado"*
# salía igual con el cortafuegos abierto que cerrado— y el arreglo es el mismo:
# **un control de fuera**, aquí la consola de Anthropic, leída **antes** de correr.
# Lo tomaron entero y la tabla del cierre lleva la columna *"identidad — de la
# consola, antes de correr"*.
# 🐛 **Y una trampa mecánica que se cazó leyendo el archivo, no suponiéndolo:**
# `check_api_key.py` **NO carga ningún `.env`** —importa `json`, `os`, `sys`,
# `urllib` y termina en `sys.exit(main(os.environ))`; las cinco apariciones de
# `.env` están en prosa—. Editar el `.env` y correrlo habría dado la **puerta 1**
# (*falta la llave*) o, peor, un valor exportado viejo. **Un rojo con la causa
# equivocada**, en la primera corrida real de la pieza.
# 📌 También quedó dicho lo que la puerta 0 significa —*"no es la del
# laboratorio"*, nunca *"es la de `Default`"*— y que la **puerta 4 no es un
# resultado**: con `claude-opus-5` un `529` cae ahí y significa *"no pude mirar"*.
# Se cobró el mismo día: **diez `529` entre las 13:36 y las 13:46 UTC** dejaron
# `teapp-server` sin comprobar, y **no se confundió con una llave mala.**
#
# 🥇 **HALLAZGO 3 — el que más valió, y salió de un `grep` de esta terminal.**
# `[A-027]` decía *"esa llave la está usando algo más y no sabemos qué"*. Medido
# aquí: **21 archivos `.py` en 8 niveles** (`00-setup` … `06b-memoria-skills`)
# leen `ANTHROPIC_API_KEY` del `.env` de ESTE repo. **El "algo más" era el curso.**
# 🔑 No es *"alguien podría revocarla"*: es que **producción iba a compartir
# credencial con un repositorio donde se corren ejercicios a diario**, y el día
# que se rote por un motivo del curso el síntoma le llega a alguien practicando
# inglés **con la causa en otro repositorio**.
# ⚖️ **Y el orden dejó de ser opinión: lo impuso `install.sh:89-95`** —*una llave
# ya escrita no se pisa NUNCA*—, así que mandar hoy la provisional convertía el
# arreglo de mañana en **edición a mano por SSH sobre la máquina viva**, por un
# camino sin tests. Crear la llave cuesta $0; encender la EC2, no. **Lo barato
# primero**, y por mecánica, no por preferencia.
# 🔒 **Predicción sellada antes del clic** (sesión 46): *`teapp-server` dentro de
# `Default` va a leer `1000`, no `50`.* **Sin resolver** — la saturación se la
# llevó por delante. Queda como `T-087`.
#
# ⚠️ **DOS HUECOS QUE NOMBRÉ Y QUE LA LLAVE NUEVA NO CIERRA**, para que el
# registro no diga *"`[A-027]` resuelta"* a secas: (1) dos llaves del mismo
# espacio **comparten cubo y saldo**, y `Default` **no admite tope de gasto**
# (`[D-062]`) — el curso y producción beben del mismo $6,55 sin suelo, que es
# `[A-026]` con las apuestas subidas: **vaciar el saldo pasa de estropear una
# medición a dejar sin tutor a personas reales**. (2) el portero **es ciego al
# caso nuevo**: curso y servidor devuelven el mismo `1000`, así que mandar la
# llave del curso pasa por la puerta 0 tan campante. **No hay que taparlo con
# código** —colgar el freno del 1.000 es el rojo falso que se descartó ayer con
# razón (`L-047`)— pero sí escribirlo. **`L-013`: cerrar un hueco no cierra los
# demás.**
#
# ✅ **Una desviación que reportaron ELLOS sin que nadie preguntara:** `[D-063]`
# prohibía imprimir *"ni un prefijo"* de la llave y imprimieron los 4 últimos
# caracteres. Mi reparo no fue el acto —4 de 108 no reconstruye nada— sino
# **dónde quedó**: la regla diciendo que no y la desviación dos párrafos abajo
# diciendo que sí, o sea **la regla con asterisco de la sesión 57, que nadie baja
# a leer**. Lo enmendaron a norma: *"los cuatro finales, solo en la terminal,
# jamás en el repositorio"*. **Ahora la norma y la práctica dicen lo mismo.**
#
# ✏️ **Una discrepancia mía que NO tomaron, y queda anotada como suya.** El cierre
# dice *"`[A-027]` era falsa"*. **No lo era:** decía *"la usa algo más y no
# sabemos qué"* y **las dos mitades eran ciertas** — lo que le faltaba no era
# verdad, era **resolución**, y se la dio un `grep`. 🔑 Importa por lo que enseña
# dentro de un año: *"era falsa"* enseña **desconfía de tus corazonadas**; *"era
# cierta y le faltaba un `grep`"* enseña **una suposición vaga se cobra midiendo,
# no descartándola**. Lo planteé una vez, mantuvieron su redacción, y es su
# archivo. Que una suposición naciera y muriera en dos horas dejando
# `assumptions.md` intacto **está bien**, y en eso sí coincidimos.
#
# 🧭 **`LM.30` — LA LECCIÓN DE MÉTODO DEL DÍA:** **una tarea muerta que reaparece
# con una FACTURA pegada deja de ser un duplicado y se convierte en la agenda del
# día. La urgencia no se audita: se obedece.** Es la familia de `LM.20` (*está
# escrito y nadie llega*), `LM.24` (*se llega antes a lo viejo*) y `LM.26` (*se
# fabricó al comprimir*), con la vuelta que faltaba: aquí lo inventado **no fue
# la versión cómoda sino la alarmante**, y por eso es peor — *"no hace falta hacer
# nada"* invita a comprobar, *"llevas cuatro días perdiendo dinero"* invita a
# correr. 📌 Y el antídoto es barato y ya está probado tres veces este mes:
# **antes de obedecer una urgencia, preguntar de qué corrida sale.** Hoy salieron
# dos comandos y catorce segundos.
# 📌 **Suyo, y es el mejor apunte del cierre:** los tres hallazgos del día
# —el arrastre, la llave compartida y el `529` que no era la llave nueva— salieron
# todos de **no creerse el primer resultado**.
#
# 🧹 ~~**DEUDA DE ESTE REPO, detectada hoy y sin tocar:** `LM.27`, `LM.28` y
# `LM.29` viven en este `PROGRESO.md` y **`LESSONS.md` se quedó en `LM.26`**.~~
# → **PAGADA EN LA SESIÓN 70**, y para entonces eran **cinco** (`LM.27`–`LM.31`):
# la deuda creció mientras nadie la tocaba, que es justo lo que `LM.24` predice.
#
# 🚀 **La 68 (SEGUNDA del 2026-08-13) — TEAPP CORRIGE INGLÉS DE VERDAD, EN
# PRODUCCIÓN.** `T-087` y `T-078` cerradas: la llave llegó al servidor comprobada
# antes de escribirse y con permisos `600`, y hubo primera práctica real —
# *"I cooking in these morning"* → corregido, Score 9. **El día empezó con una
# tarea muerta disfrazada de urgencia y acabó con la aplicación funcionando.**
# ✅ **MEDIDO AQUÍ, no reportado** (`811d436`, árbol limpio y en `origin`):
# `200` con `Server: uvicorn` + `Via: 1.1 Caddy` —el aparejo real—, `/me` sin
# cookie → `401`, el **8000 en TIMEOUT** desde fuera con un proceso de verdad
# detrás, y el certificado `Aug 8 16:55 → Nov 6 16:55` de Let's Encrypt **SIN
# reemitir** pese a los apagados de cada noche, que era el riesgo de cuota de la
# 59. **Suite: 410, corrida aquí sobre `811d436`.** Sigue en 410 y eso es lo
# correcto: los commits del día son `_persistence/` y `deploy/` — **no es que
# nada se rompiera, es que el código de la app no se movió.**
#
# 🔒 **LA PREDICCIÓN SELLADA AGUANTÓ:** dije antes del clic que `teapp-server`,
# naciendo dentro de `Default`, leería **1000** y no 50. Leyó `requests-limit=1000`
# y salió por la puerta 0. ⚠️ **Pero acertar era la mitad mala de la apuesta**, y
# conviene que quede escrito el mismo día: el hueco que nombré ayer **ya no es
# hipotético, está vivo en producción.** El curso y el servidor devuelven **el
# mismo 1000**, así que `check_api_key.py` **no puede distinguirlos**: mandar por
# error la llave del curso al servidor pasa por la puerta 0 tan campante. Sigue
# sin haber que taparlo con código —colgar el freno del 1.000 es el rojo falso que
# `L-047` descartó con razón— pero el portero nació para un riesgo y hoy convive
# con otro que no ve. **`L-013`: cerrar un hueco no cierra los demás.**
#
# 💵 **Y el dinero cambió de categoría hoy, que es lo que hay que llevarse.**
# `Default` no admite tope (`[D-062]`), así que el único freno del servidor es el
# saldo de **$6,55**, y sobre ese saldo hay ahora **tres bebedores**: el curso (21
# scripts), la báscula y **producción**. 🔑 **`[A-026]` sube de categoría sin que
# nadie la tocara:** ayer 26 corridas seguidas de la báscula estropeaban una
# medición; **desde hoy dejan sin tutor a una persona que está practicando.** La
# suposición no cambió — cambió lo que cuelga de ella. 📌 Es el mismo movimiento
# que `[A-018]` el día que se encendió la EC2: *el experimento perdió su
# aritmética limpia el día que cumplió su objetivo.*
#
# 🌐 **`A-017`, y esta medición es MEJOR que las anteriores por lo que le falta:**
# 5 intentos en la misma ráfaga → **2 × `000` y 3 × `200`**. Esta mañana también
# hubo `000`, pero la máquina estaba apagada y eso **confundía la medida**; ahora
# la máquina está demostrablemente viva —los 200 salen de la misma ráfaga— así que
# los fallos **solo pueden ser resolución de nombre**. Muestra pequeña: 5
# intentos no dan una tasa, dan una existencia. ⚠️ **Lo que sí quiero dejar
# dicho:** *"es el cliente, no DuckDNS"* es un diagnóstico **cierto y una
# conclusión insuficiente**, y hoy dejó de ser gratis — **la persona que practica
# inglés también tiene un cliente.** Un fallo que solo le pasa al que mide es una
# curiosidad; el mismo fallo, el día que hay usuarios, es el producto.
#
# ✅ **Su apunte del día es correcto y me lo quedo:** *lo escrito ayer te defendió
# hoy* — `[L-033]` les ahorró diagnosticar un SSH que fallaba por nombre y
# `[L-046]` ya tenía escrito que la puerta 4 no es un veredicto, así que diez
# `529` no se convirtieron en una acusación contra una llave recién creada.
# 📌 Mi matiz, que es el reparto de la 43 en pequeño: **los tres hallazgos del día
# no salieron de auditar el programa, salieron de auditar lo que se DICE del
# programa** — un reporte (`T-074`), un plan (preguntarle la identidad al guion
# que se audita) y una suposición (`[A-027]`). Ninguno era código. Y eso es
# justo lo que esta terminal puede hacer y la otra no: **no lo escribió.**
#
# 🔬 **La 69 (TERCERA del 2026-08-13) fue una AUDITORÍA PEDIDA, con el traspaso
# escrito por ellos "para que audite, no para que me crea".** Es la primera vez
# que llega una lista de comprobaciones concretas en vez de un resumen, y el
# formato funciona: **tres hallazgos, y ninguno habría salido de leer el resumen.**
# ✅ **Confirmado aquí:** árbol limpio con `76e9bee` y `f4b73b7` en `origin`,
# **425 passed corridos sobre `f4b73b7`** (su número, correcto), `add_point` y
# `read_score` **sin una sola llamada ni definición viva**, `[A-001]`/`[A-028]`
# solo como comentarios de defunción, y `https://teapp.duckdns.org/` → `200` con
# la página sirviendo `id="practice"`. Las dos citas que existen aguantan:
# `[L-051]`→`[L-007]` es buena **y bien defendida** (*"hermana por el fondo, no
# por el tema"*: allí `diff -r` gritaba «viejo» con el repo correcto, aquí el
# navegador con el despliegue correcto), y `[D-066]`→`[D-050]` también.
#
# 🔴 **HALLAZGO 1 — dos de las citas que me mandaron verificar NO EXISTEN.** El
# traspaso decía que `[D-066]` y `[D-069]` citan `[L-017]`, `[D-050]` y `[A-002]`;
# buscadas en índice y cuerpo, **solo está `[D-050]`**. 📌 **Falla del lado
# seguro** —mandaron a comprobar de más, no de menos— y eso es mérito. Pero es la
# mecánica de siempre: **el traspaso describe el documento en vez de citarlo.**
#
# 🔴 **HALLAZGO 2 — `[A-001]` estaba BIEN clasificada, y lo comprobé porque creí
# que no.** Mi objeción parecía sólida: una frase mala que sube el marcador
# **confirma** *"cuenta practicadas, no correctas"*, no la desmiente — o sea el
# mismo error que les señalé ayer con `[A-027]`. Fui al historial antes de
# decirlo, y `[A-001]` traía **su propio criterio de falsación escrito**: *"si
# sube y eso es lo que se quería → cierta; **si sube y chirría → falsa**"*. Por su
# propia regla, *falsa* es correcto. 🔑 **La entrada estaba mejor construida que
# mi objeción**, y no había nada que corregir. Es la lección de la 59 —*abrirlo no
# basta, y no abrirlo tampoco*— resuelta del lado bueno por una vez: **la sospecha
# se cobró en la fuente y murió ahí, sin llegar a ser un hallazgo falso.**
# ⚠️ **Pero la misma frase mandaba a otro sitio y esa mitad NO se cumplió:** *"era
# falsa → entra en `lessons.md`"*, y se fue a `decisions.md` (`[D-066]`), que es el
# destino de la otra rama. **No se escribió ninguna lección, y hay una servida:**
# `[A-001]` avisó el 2026-08-02 de que *"hoy no se nota porque el juez es falso y
# aprueba todo"* y de que *"el coste crece: en el paso 8 sería rediseñar la
# herramienta el mismo día que se enchufa el modelo"*. **Ocurrió hoy, al pie de la
# letra, once días después.** 🔑 **Un maniquí no solo tapa un fallo: tapa una
# DECISIÓN DE DISEÑO, y la devuelve el día en que es cara.** Es el activo más
# valioso del día y no vive en ningún archivo.
#
# 🔴 **HALLAZGO 3 — `[D-069]` es más flojo de lo que ellos mismos avisaron, y no
# por lo que avisaron.** Marcaron como punto débil *"no hay archivo de salida
# guardado"*. El problema real es otro: **tres versiones del mismo dato y ninguna
# coincide.** `[D-069]` dice `{"score": 1, "practice": 3}`; el traspaso dice cinco
# llamadas y `practice: 2`; en disco, `data/users/jorge.json` dice `practice: 2`.
# El `3` venía de una *"cuenta desechable"* que **desapareció con ella**. 🔑 **Si
# la evidencia es "lo escrito en la entrada", dos escrituras que se contradicen la
# anulan** — y quien mañana siga la instrucción de mirar el disco encontrará otro
# número **sin manera de saber que es otra corrida**. Arreglo barato y sin gastar:
# decir de qué cuenta era y que se borró.
#
# 🌐 **Y UN CASI-ERROR MÍO, que es el mejor dato del día.** Mi primera medición
# del despliegue **no encontró `id="practice"`** y estuve a un paso de escribir
# *"contradice tu afirmación 7"*. No lo era: `curl -s` había fallado al resolver
# el nombre y devolvió **cuerpo vacío**, y mi `grep` leyó ese vacío como *"el
# marcador no está"*. La corrida siguiente, en el mismo instante, dio `200` con
# los tres contadores. 🔑 **`[A-017]` no cuesta una petición: FABRICA EVIDENCIA.**
# Un fallo de resolución con `-s` es **silencioso y con forma de hallazgo**, y el
# hallazgo que fabrica es *"el despliegue está roto"* sobre un despliegue bueno.
# 📌 **Es `[L-051]` un anillo más afuera y conmigo de víctima:** allí la pantalla
# mentía sobre un despliegue correcto; aquí mentía mi instrumento. → `LM.31`:
# **un instrumento que falla devolviendo VACÍO no da un error, da el silencio —
# y el silencio entra en un `grep` como si fuera una respuesta.** Es `LM.15`
# (*nadie audita un verde*) con el vacío en el papel del verde. **Regla que sale:
# cuando el resultado de una medición sea "no aparece", comprobar primero que la
# medición ocurrió.**
# ⚠️ **Los tres hallazgos llegaron con su sesión YA CERRADA** (`f4b73b7` hecho):
# nacen huérfanos salvo que les den commit. `[L-029]` y `[L-049]` a la vez.
#
# 🧹 **La 70 (CUARTA del 2026-08-13) NO TOCÓ LA NUBE NI TEAPP: pagó la deuda de
# este repo.**
# `LESSONS.md` llevaba desde la sesión 60 clavado en `LM.26` mientras
# `PROGRESO.md` acumulaba lecciones nuevas. **Subieron las cinco que faltaban:**
# `LM.27` (*el párrafo no se relee; la tabla sí*), `LM.28` (*la contrición ocupa
# el sitio del hallazgo*), `LM.29` (*una lista escribe igual lo que hay que
# resolver y lo que hay que construir*), `LM.30` (*la urgencia no se audita, se
# obedece*) y `LM.31` (*cuando una medición diga «no aparece», comprueba primero
# que la medición ocurrió*). **De 26 a 31, sin huecos ni repetidas.**
# 📌 **La deuda se detectó en la 67 diciendo «son tres»; al pagarla eran cinco.**
# Creció **el mismo día**, en dos sesiones. Es `LM.24` cumpliéndose sobre la lista
# de lecciones que contiene a `LM.24`.
# ✏️ **Y del propio índice salió una corrección que no estaba prevista:** dos de
# los cinco títulos nacían casi calcados de lecciones ya existentes —`LM.27` de
# `LM.16` y `LM.31` de `LM.15`— porque cada una es *el mecanismo* de la anterior.
# Vistos en la lista, **dos titulares iguales se leen como una repetición y el
# lector se salta el segundo.** Se retitularon por lo que aportan de nuevo, no por
# el hecho que comparten. Es `LM.27` aplicada a `LM.27` el día que se escribió.
# 📐 **La cabecera del bloque de Método también estaba desactualizada:** describía
# el origen hasta la sesión 45 y las 19 lecciones siguientes vienen de otro sitio
# —las sesiones de supervisión del nivel 7—. Ahora lo dice, y deja escrito que
# **estas `LM.x` ascienden sobre la marcha, no al cerrar el nivel**, que era una
# práctica real sin regla escrita. `LM.13` de TEAPP: *un acuerdo que depende de
# que nadie se despiste no es un acuerdo, es una racha.*
#
# 🔬 **La 71 (QUINTA del 2026-08-13) fueron CUATRO RONDAS DE AUDITORÍA sobre UNA
# SOLA DECISIÓN**, de `0395c1b` a `a0ccb1f`. Sin tocar la nube y sin gastar un
# centavo. TEAPP cerró cuatro veces el mismo día para atenderlas, y las cuatro
# rondas encontraron algo. **La cadena importa más que los hallazgos sueltos:**
#
# | ronda | qué se encontró |
# |---|---|
# | 1ª (`0395c1b`) | 5 hallazgos. El grande: **un techo que no existía** |
# | 2ª (`3463f2c`) | el arreglo metió una **regresión viva**, cobrando, 2 h en producción |
# | 3ª (`c89ae1d`) | el arreglo de eso traía una **justificación que caducaba** |
# | 4ª (`a0ccb1f`) | la justificación buena se quedó **sin guardián** |
#
# 🔑 **EL HALLAZGO 1, y es el que sostenía todo.** `[D-070]` afirmaba que el
# cliente de Anthropic *"corta a los 8,0 s pase lo que pase"*. Falso: `httpx`
# reparte un `timeout=8.0` escalar a **cuatro fases con cronómetro
# independiente** — `connect`, `read`, `write`, `pool` — que **suman 32 s**.
# Medido aquí construyendo el cliente igual que la app, no recordado. Con eso se
# caían las tres afirmaciones que colgaban: el tope de 8,06 s por práctica, el
# *"el reloj de la ruta no puede morder por nada de dentro"* y los 1.944 ms de
# margen. 📌 **La premisa no nacía en el commit auditado:** venía de `[L-045]` y
# `[L-043]`, de días antes, y se heredó sin volver a comprobarla.
# 🔑 **HALLAZGO 2 — dos argumentos que no podían ser ciertos a la vez.** La misma
# decisión usaba *"el reembolso vive dentro del `except`"* y *"la cola no se
# forma, por construcción"*. Si no hay cola, `cancel()` devuelve siempre `False`
# y el reembolso **es código muerto**. Se resolvió con una corrida suya: un `504`
# suelta la ficha de `anyio` **pero no el sitio del pool**, porque Python no sabe
# matar un hilo. La falsa era *"no hay cola"*, y estaba escrita **seis líneas por
# encima** del comentario que decía lo contrario, en el mismo archivo.
# 🔴 **LA RONDA 2 ES LA QUE ENSEÑA, Y VA CONTRA MÍ.** Al repartir los 8 s entre
# las cuatro fases le tocaron **4,0 s al `read`** — y `read` gobierna la espera
# de cabeceras, o sea **la generación entera**. Su propia medida decía `4,72 s`
# como peor de diez. **El arreglo de una afirmación falsa metió un corte real**,
# por debajo de un valor ya medido, con el modo de fallo **cobrando la práctica**
# y el log culpando a Anthropic. Estuvo dos horas vivo en producción.
# 📌 **Y mi one-liner del primer informe tampoco arreglaba nada:**
# `httpx.Timeout(8.0, connect=2.0)` deja 26 s. Escribí *"o mejor, fase por fase"*
# en segunda posición, y **la línea que alguien copia es la primera que lee.**
# 🧭 **SU MEJOR APORTACIÓN, y es una objeción a mí:** al correr su báscula por
# sexta vez el peor caso subió otra vez — `44,9 → 45,9 → 49,2 → 50,6 → 56,3 →
# 62,4 ms`. De ahí: **«el peor de N no es un techo: es un suelo que crece con
# N»** — y me lo cobraron donde dolía, porque yo había colocado `read = 6,5`
# justificándolo como *"38% por encima de los 4,72"*, **el mismo estadístico
# inestable**. Tenían razón. 🔑 **La respuesta que salió de ahí es lo mejor del
# día: `read` no debe estimarse, debe ser el MÁXIMO QUE CABE** — porque el coste
# no es simétrico (pasarse cuesta cero, el reloj de la ruta es el backstop real;
# quedarse corto cobra una práctica). Se calcula **por resta del presupuesto**,
# no por medición. **El número no cambió; cambió el porqué** — y el porqué era lo
# único que iba a engañar al siguiente que lo tocara.
# 📌 **Y una diferencia que va en su contra y no a favor:** la distribución del
# tiempo de generación **no está quieta** — la produce un sistema que no
# controlan y que cambia sin avisar. Medirla hoy dice cómo era hoy. Es el
# argumento definitivo contra afinar un timeout a una cola medida.
#
# 🧭 **`LM.32` — LA LECCIÓN DE MÉTODO DEL DÍA:** **el sitio con más probabilidad
# de esconder el error siguiente es la corrección que acabas de hacer.** Las
# cuatro rondas salieron todas del remedio de la anterior. Una corrección se
# escribe con prisa, con alivio, con el foco en el defecto viejo y **con una
# cicatriz que la avala**. Es `LM.15` y `L-034` en su forma más pura: el código
# recién corregido es el único que nadie va a volver a mirar, **porque todos
# acaban de mirarlo**. No es un argumento para revisar más — es sobre dónde
# apuntar: **cuando alguien arregle algo que señalaste, el arreglo ENTRA en la
# cola de auditoría, no sale de ella.**
#
# 🧭 **`LM.33` — y esta la acreditaron ELLOS, que es lo que la hace valer.** La
# suite tardó `39 s` donde por la mañana tardaba `17`. Tenía forma de hallazgo
# número seis. La corrí dos veces más — `39 / 36 / 27` — era **ruido de mi
# máquina**, y no lo mandé. Ellos lo devolvieron: *"nos habría puesto a buscar
# una regresión inexistente medio día"*. 🔑 **Dos minutos comprobarlo contra
# medio día de ellos**, y engancha con `LM.30`: si la urgencia no se audita sino
# que se obedece, **quien emite la alarma es el único filtro que existe.** El
# filtro no es un paso previo a auditar: **es la mitad del trabajo**, y es la
# mitad que no deja rastro.
#
# ✅ **Lo que ellos hicieron bien y conviene no perder:** enmendaron `[D-070]` en
# vez de borrarla (con los punteros muertos tabulados), lo que permitió que la
# segunda vuelta se hiciera en una hora; vieron morder cada test antes de darlo
# por bueno; usaron **mi propio one-liner malo como sabotaje** para comprobar que
# el test nuevo se ponía rojo; y estrenaron el formato de encargo —*"audita, no
# me creas"*, con lista de afirmaciones y comandos— que es **lo que produjo los
# hallazgos**: los tres primeros de la ronda 1 estaban DEBAJO de lo que un
# resumen contaba.
# ✏️ **Y me retracté de algo que dije la víspera.** Les había dicho *"pedid la
# auditoría ANTES de cerrar"* (`[L-029]`). Su solución es mejor: **la ronda de
# respuesta lleva commit propio**, y así no acoplan su ritmo al de esta terminal.
# La condición real no es el orden commit/auditoría, es que **la auditoría llegue
# mientras la decisión siga siendo reversible**. Hoy `[D-070]` se enmendó en 4 h.
# 🛑 **Y la cuarta ronda se cerró diciendo que había que PARAR.** Hallazgos
# decrecientes: techo falso → regresión → justificación caduca → un `assert` que
# falta. Una quinta vuelta encontraría comas. **Una terminal que audita hasta
# encontrar algo acaba fabricando hallazgos para justificar la ronda** — el
# riesgo era mío, y por eso lo dije yo.
# 🔲 **Queda vivo en su lado, y no se resuelve auditando:** un `assert` que ate
# la resta de `[D-073]` (hoy `TIMEOUT_SECONDS = 9,9` pasa los dos tests en verde
# y se come el margen entero), y **`T-093` — ~$0,09**, que contesta la única
# pregunta viva: *¿son 10 s el presupuesto correcto de la ruta?* Con el percentil
# y la tasa de corte **decididos antes de medir**, porque `max(40)` tampoco es un
# techo. `[A-011]` cierra con eso, y esta vez sin techos inventados.
# ✏️ **Corregido en la 72: el `~$0,09` de arriba era MÍO y estaba viejo** — era
# con 40 muestras. Al subir la N a 60 son **$0,14**. El dato desactualizado no lo
# traía el informe de ellos: lo traía este archivo.
#
# 🔬 **La 72 (2026-08-14) AUDITÓ UN CRITERIO ANTES DE QUE SE GASTARA EL DINERO, y
# esa es toda la sesión.** Supervisión pura: esta terminal no ejecutó TEAPP ni
# gastó un centavo. Ellos llegaron con `T-093` lista para correr (~$0,14 contra
# `claude-opus-5`) y la pregunta fue *"¿la lanzo?"*. La respuesta fue **todavía
# no**, y salieron **tres defectos reales** del criterio, todos confirmados por
# ellos corriéndolos.
# 🔑 **POR QUÉ ERA AHORA O NUNCA, y es la idea que sostiene el día entero:** el
# criterio de `T-093` estaba escrito **a ciegas la víspera** para que la medición
# no pudiera acomodarse al resultado. Un criterio así solo se puede auditar
# **antes**. Después de ver los números, arreglarlo y moverlo son indistinguibles
# — no para quien lo hace, sino **para cualquiera que lo lea después**.
# 🚩 **H-1, el grave: un umbral por encima del techo de lo que puede pasar.**
# `ROUTE_THRESHOLD_SECONDS = 9,5` mientras el presupuesto entero del cliente son
# `9,0` (`1,5 + 0,5 + 6,5 + 0,5`). Una llamada de 9,2 s salía **ÁMBAR**, y la
# receta de ÁMBAR es *"quítale a connect/write/pool y dáselo a read"* — **receta
# imposible**: aunque las otras tres fases quedaran en cero, `read` no pasa de
# 9,0. El criterio mandaba a hacer algo irrealizable en vez de decir que el
# presupuesto de la ruta estaba mal.
# 🚩 **H-2 y H-3: dos frases que afirmaban cosas falsas**, y las dos a un comando
# de distancia. `verdict_for(1,0,60)` imprimía *"1.7%, por encima del 5%
# acordado"*; `verdict_for(0,0,45)` imprimía *"por debajo de 6.7%, que es el 5%
# acordado"*. `ACCEPTED_CUT_RATE` no aparecía en **ninguna** comparación: se
# interpolaba en textos y nada más. ⚠️ **Los umbrales no estaban mal** —exigir
# cero cortes para VERDE es correcto, la regla de tres solo deja afirmar ≤5% con
# cero observados—: lo falso era **lo que la frase decía de sí misma**.
# 🔴 **H-5, y es el hallazgo del día aunque no cambió ningún número.** Al arreglar
# H-1 justificaron el `9,0` con *"dos restas independientes que dan lo mismo"*.
# Ninguna de las dos era lo que decía: la del cliente es una **tautología** (el
# máximo si le das todo a `read` **es** el presupuesto del cliente), y la de la
# ruta solo aterriza en 9,0 tomando el `1,0` como `ruta − cliente`, que era la
# conclusión. Con los componentes de su propia tabla —`0,07` de trabajo local +
# `0,50` de margen— da **9,43**, no 9,0. → **`LM.35`**, y la escribieron ellos
# sobre sí mismos: *una corroboración inventada es peor que ninguna, porque
# desactiva la revisión.*
# 🧭 **`LM.34`, también suya:** *una función que nadie prueba es un párrafo con
# paréntesis.* Escribir el criterio como función y no como párrafo fue **la
# decisión que hizo posible auditarlo** con tres comandos y $0 — pero no tenía ni
# un test, y por eso los dos defectos llevaban un día ahí. La forma ejecutable
# promete comprobación y no la entrega.
# ⬆️ **H-4 (la deuda que yo había dejado viva en la 71) CAMBIÓ DE CATEGORÍA por
# culpa del arreglo de ellos.** Al derivar el umbral de `TIMEOUT_SECONDS`, el
# hueco cliente→ruta pasó a ser carga estructural del criterio. Dejó de ser deuda
# independiente. 📌 **Un arreglo correcto puede subir de prioridad una deuda
# ajena** — lo anotaron ellos en `[D-076]`.
# ⚠️ **H-6, tercera ronda seguida con la misma forma: número correcto, razón
# equivocada.** Justificaron usar `0,07` con *"errar del lado seguro"*. La primera
# mitad es cierta (subestimar produce falsos negativos), la segunda invierte la
# asimetría: para un `read` pasarse cuesta cero, pero **para un guardián el error
# permisivo es el peligroso**, porque produce un verde que no significa nada. La
# razón buena la tenían al lado sin usarla: el margen de rendición (500 ms)
# **domina siete veces** al sumando dudoso (70 ms).
# 🟢 **Y la tanda salió VERDE: 0 de 60.** Mediana `2,88 s`, peor de 60 `3,91 s`,
# contra un corte de `6,5 s`. `[A-011]` **muerta al tercer intento**, ascendida a
# `[D-077]`. Techo del instrumento 30 s vs peor caso 3,91 s → **no hubo censura de
# la cola**: ninguna muestra se perdió chocando contra la báscula.
# 🔑 **LO QUE HACE QUE ESE VERDE VALGA ES EL ORDEN, no el color.** Los tres
# arreglos **endurecieron** el criterio (ROJO bajó de 9,5 a 9,0, ÁMBAR dejó de
# mentir, la tanda corta ya ni emite veredicto). **Salió verde con el criterio más
# estricto, no con el más laxo** — y eso es lo único que lo distingue de un umbral
# movido hasta que encajara.
# 🧭 **H-7 — la condición, y sin ella la suposición no muere.** Las 60 llamadas
# fueron **secuenciales, en ~3 minutos, un solo día**, contra un sistema que no
# controlan. No son 60 observaciones independientes de *cómo le va a alguien
# practicando*: son 60 llamadas pegadas bajo condiciones que duraron tres minutos.
# Y hay prueba viva de que la condición varía: **`T-087` fue "Anthropic dejó de
# saturar"**. 🔑 **El fallo que previene es peor que los dos anteriores: el cuarto
# intento llegaría disfrazado de asunto zanjado** — alguien vería cortes en seis
# meses, no encontraría el porqué, y leería un `[A-011]` cerrado diciéndole que eso
# ya se resolvió.
# ✅ **Y ELLOS MEJORARON MI PROPIA RECOMENDACIÓN.** Yo dije *"que la condición
# quede adentro de la decisión"* y me quedé en `_persistence/`. La pusieron
# **también junto al número en `app/api.py`**. 📌 **Un archivo de decisiones lo
# consulta el que ya sospecha; el comentario al lado de la constante lo lee el que
# no sospecha nada** — y ese es el que hay que interceptar.
# ✅ **Tampoco se cobraron el "dato gratis".** Les ofrecí comparar el cargo real
# contra `60 × $0,00234 = $0,1404`; lo anotaron como pendiente en vez de escribir
# un número que no habían leído. **Regla 6 contra sí mismos en el momento más
# tentador**, porque se lo habían ofrecido con la etiqueta que más invita a
# tomarlo sin verificar. Quedó como `T-095`, con el aviso de `LM.31`: si la
# consola no muestra el cargo, **eso no es un cero**.
# 🛑 **Me apliqué mi propia regla de parada de la 71.** H-6 se entregó marcado
# **"NO BLOQUEA"** y H-7 igual: una terminal que audita hasta encontrar algo acaba
# fabricando hallazgos para justificar la ronda. Y por `LM.32`, **`[D-077]` entra
# en la cola de auditoría, no sale de ella**: es la corrección más reciente y no
# la he leído. Quedó como `T-094`, primero de mañana, antes que `T-090`.
# 🗣️ **Corrección suya sobre el idioma, y era real:** esta terminal venía
# escribiendo **español peninsular** en los encargos (*"vuestra"*, *"lanzad"*,
# *"tenéis"*). Pidió **español colombiano** y tiene razón: es su curso y su
# empresa. De la 72 en adelante, *ustedes / su / corran / arreglen*.
# 🔲 **Queda anotado para mañana, y lo levantaron ELLOS solos:** el `session-closer`
# cerró **`T-079` por inferencia**, no por evidencia directa del día, y lo declaró
# como decisión propia. **Es la segunda vez que a esa misma tarea le pasa** (ya se
# desmarcó tras la auditoría del 13). Un ✅ que se puede volver a quitar.
#
# 💵 **La 73 (2026-08-14, misma fecha) AUDITÓ `[D-077]` Y CAZÓ UN PRECIO
# CADUCADO QUE IBA A MANDAR LA SIGUIENTE TAREA AL ARCHIVO EQUIVOCADO.**
# Supervisión: no ejecuté TEAPP, no llamé a la API, no gasté un centavo. Corrí
# `pytest` y unos `git show`. Suite **439 → 440, MEDIDA AQUÍ** sobre `46cce85`;
# su número era correcto las dos veces.
# 🔴 **H-1, el que bloqueaba:** `[D-077]` mandaba comparar el cargo real contra
# `60 × $0,00234 = $0,1404`. Ese `$0,00234` es de `[D-058]`, medido el **11 de
# agosto** sobre llamadas de **247 tokens de entrada**. La corrida de `T-093`
# gastó **361**. 🔑 **La causa la medí, no la supuse:** `[D-066]`/`[D-067]` le
# añadieron el bloque `OK`/`FIX` a `GRAMMAR_RUBRIC` el día 13 — **678 → 1.016
# caracteres, +49,9%**, contra **+46,2%** de tokens de entrada. Las dos cifras se
# persiguen.
# ⚠️ **Y lo grave no era el número, era la conclusión pre-escrita:** *"si no
# cuadra, lo que hay que revisar es `[A-010]`"* — el tope de 20 prácticas al día,
# que no tiene nada que ver. La tercera explicación **estaba impresa en la salida
# de la propia corrida** y nadie la miró. Pre-comprometer una conclusión única fue
# el error; pre-comprometer la **lista de ramas** no lo es.
# 🧭 **`LM.36` — la lección madre del día, y sale de su propia `[L-043]`:** aquella
# escribió *"la entrada apenas se mueve, la rúbrica pesa casi todo, o sea el coste
# por práctica es casi fijo"*. **Identificó bien el término dominante y acto
# seguido lo trató como constante.** Es al revés: **que la rúbrica domine el coste
# es exactamente lo que vuelve el coste sensible a editar la rúbrica.**
# 🥇 **Y ELLOS LO ENCONTRARON MEJOR QUE YO.** Yo lo cacé cruzando dos documentos
# (la corrida contra `[D-058]`). Ellos lo encontraron **dentro de uno solo**:
# `decisions.md:110` dice *"~361 y ~49 por llamada"* y `decisions.md:161` razona
# con el precio de 247 — **la misma entrada, mismo autor, mismo minuto, a cincuenta
# líneas**. 🔑 **`LM.37`: la cercanía no protege.** Escribíamos las decisiones
# juntas para que quien lea una lea la otra; estar al lado **no obliga a nadie a
# hacer la resta**. Lo único que habría mordido es aritmético — que el `$0,1404`
# fuera una **división visible** y no un producto ya resuelto. `measure_tutor.py`
# ya escribía sus constantes como divisiones; la prosa no lo heredó. → `[L-059]`.
# ⚖️ **La decisión del día era suya y la pregunta estaba mal planteada.**
# Preguntaron *"¿dejo el `0,00234` marcado como caducado, o subo al `0,00304`
# derivado?"*, o sea medido-contra-derivado. **Esa opción no existía:** `0,00234`
# tampoco es hoy un número medido — es la medición de una rúbrica que ellos mismos
# borraron. **Las dos opciones metían en el código un número sin medir, y una era
# conservadora.** Ahí se acabó. Subieron a `0,00304` con etiqueta de tres partes.
# 🔑 **Tres apoyos, en orden de peso:** (1) esa constante **no afirma nada, divide**
# —es la calibración de un freno, no una afirmación sobre el mundo, y la regla 6
# protege afirmaciones; (2) la dirección del error **ya la habían decidido ellos**
# (*"errar del lado seguro: el tope se queda corto, nunca largo"*) y hoy estaba
# **invertida**; (3) un `caducado` en un comentario es `LM.13` — **una nota, no un
# freno**. 📌 **Y localicé el acantilado, que es lo que abarató la decisión:**
# `int(0,25 / x) ≥ 60` → hasta **$0,00416** el freno sigue permitiendo la tanda de
# 60. Con `0,00304` caben **82**. Gratis de un lado, dinero del otro.
# ✅ **El mejor artefacto del día es suyo: un test que cruza `MAX_CALLS_PER_RUN` con
# `TARGET_SAMPLES`.** Uno sale del dinero y el otro de la regla de tres, y **nadie
# los cruzaba nunca**: si el coste sube de `$0,00416`, el monedero corta antes de
# las 60 muestras y `verdict_for` devuelve `SIN VEREDICTO` **después de haber
# gastado** — se paga y no se concluye. El margen pasó de comentario a morder.
# 🔒 **`T-095` NO SE CERRÓ, y eso fue deliberado.** Antes de abrir la consola se
# selló `[D-079]`: **banda `$0,156–$0,205`** —barre *todos* los repartos
# entrada/salida, no es un ±10% a ojo—, el espacio a leer (`teapp-measure`, no el
# total de la organización), la línea base de `[D-062]`, y **cuatro ramas A/B/C/D
# escritas antes de mirar**. Es la sesión 46 aplicada a una lectura en vez de a un
# clic: cuesta $0 y es lo único que después distingue una explicación de una
# racionalización.
# 📊 **LA LECTURA, del 2026-08-14 a las 15:08 UTC** (10:08 Colombia, UTC−5; la zona
# va dentro del dato, `[D-046]`). **El día 14 está limpio AL TOKEN:** consola
# `21.668 / 2.959`, `T-093` medido `21.668 / 2.959` — **idénticos**. No hubo ni una
# llamada ajena; no hay sondas que descontar. Y **la consola confirmó la derivación
# al centavo**: semana `$0,2004` calculado contra **`$0,20` leído**, sobre un mix de
# tokens distinto al que originó las tarifas. El día 14 sale en **≈$0,183, dentro
# de la banda** → apunta a la rama A. 🚨 **Pero `T-095` sigue abierta a propósito:
# ese `$0,183` lo derivé yo y el `$0,20` leído es de "últimos 7 días", no del 14.**
# Falta leer la barra del día en *Costo diario de tokens*. **Predicción sellada
# antes de esa lectura: `$0,18–$0,19`.**
# 🐛 **Dos vistas de la MISMA consola no cuentan lo mismo, y lo declaran ellas
# solas:** `Uso` dice *"incluye la API **y la Consola**"*, `Costo` dice *"**solo**
# uso de API"*. Hoy no muerde —el día 14 coincide exacto— **pero el día que un
# número de `Uso` y uno de `Costo` no cuadren, la causa es esta, no un error de
# cálculo.** Es el cuarto reloj de la 53 en otro instrumento.
# 🧟 **Cabo suelto medido, no resuelto:** la semana (ago 10–16) trae **1.834
# entrada / 338 salida** más que el día 14 — **~5 llamadas ≈ $0,018** que **no**
# cuadran con las dos sondas anotadas. Algo más llamó con la llave del laboratorio,
# en un día que no es el 14. **No bloquea y son centavos**, pero va anotado *con el
# número dentro*: es la forma en que `LM.30` empieza.
# ⏱️ **Y un dato que nadie pidió: el cargo apareció el MISMO día de la corrida.**
# En AWS tardaba ~24 h y esa espera costó las sesiones 46–54. ⚠️ Es **una**
# observación de **un** día, y lo que no se sabe también queda escrito: no se midió
# el retardo, solo que a las 15:08 UTC ya estaba — está entre 0 y ~15 horas.
# ✏️ **ME EQUIVOQUÉ EN `T-086`, y del peor modo posible.** Mandé saldarla con esta
# lectura. `T-086` dice literalmente *"la próxima lectura de **AWS**"*, y `[A-024]`
# lleva sellado desde el día 10 que son **cuatro bolsillos y no se mezclan**. 🔑 Lo
# leí en **el resumen de la tarea**, no en su texto — *el resumen sale peor que el
# documento*, que es lo que llevo tres sesiones señalándoles a ellos, cometido por
# mí **al escribir un encargo cuyo tema era leer con cuidado**. Lo cazaron ellos.
# Se salvó lo transferible: **ninguna lectura de costo se anota sin su hora UTC,
# venga del bolsillo que venga.** `T-086` sigue abierta.
# ✏️ **Y un segundo error mío que ellos devolvieron MEJOR.** Propuse buscar caché
# de prompt en el objeto `usage` de las 60 llamadas: **el dato no existía** —
# `measure_tutor.py` no escribe a disco y `client.usages` murió con el proceso.
# Su sustituto es superior y también gratis: la caché es **opt-in**, exige
# `cache_control`, y **no hay ni una coincidencia** en el código del proyecto.
# ✅ **Verificado en la documentación, y salió un segundo cerrojo que no esperaba:**
# el prefijo mínimo cacheable de `claude-opus-5` son **512 tokens** y la llamada
# mide **361** — no habría cacheado ni con la marca puesta, **y en silencio**.
# 🔑 **Dos cerrojos independientes le dan la vuelta a la rama:** si la consola
# muestra caché, eso no es la explicación cómoda de un número bajo, **es la
# sorpresa que hay que perseguir**. 📌 Para el paso 9: ese mínimo **no es monótono**
# —`claude-opus-4-6` y `claude-haiku-4-5` piden **4096**—, así que un prompt que
# cachea en un modelo puede dejar de cachear en otro **sin que nada avise**.
# 🗣️ **Corrección suya sobre CÓMO respondo, y era justa:** preguntó *"¿cerramos la
# sesión en la otra terminal?"* y yo ya lo había contestado — **al final de un
# mensaje largo**, o sea enterrado. Tuvo que volver a preguntar temiendo estar
# dando vueltas. **La respuesta a una pregunta directa va primero, no de remate.**
# ✅ **Tercera sesión seguida en que un encargo mío vuelve mejorado** (`LM.37` es
# suya, el test del cruce es suyo, el reencuadre de la caché es suyo). Y por cuarto
# día se auditó con su sesión **abierta**: cero hallazgos huérfanos (`L-029`).
#
# 🔐 **La 74 (2026-08-14, CUARTA del mismo día) CONVIRTIÓ UNA SOSPECHA MÍA EN UN
# HECHO MEDIDO POR ELLOS, Y CERRÓ `T-089` COMO CLASE DE SEGURIDAD.** Supervisión:
# no ejecuté TEAPP, no llamé a la API, no gasté un centavo. Leí su repo y corrí
# `git`/`grep`. Commits del día allá: `8b9b37f` (`T-089` + `T-097` + `[L-061]`) y
# `6c7b5a7` (`[D-080]`).
# 📊 **`T-095` cerrada: la barra del día 14 dio `$0,18`** — dentro de mi banda
# sellada `$0,18–$0,19`. **Pero la lectura vale menos de lo que parece, y lo cazaron
# ellos** (`[L-060]`): la consola redondea al céntimo, así que `$0,18` solo dice que
# el número vive en **`[0,175 – 0,185)`**. Las dos predicciones —mi banda y su
# derivación de `$0,183`— **caben dentro del mismo redondeo**. El instrumento no
# tiene la finura que pedía el método.
# ✏️ **El matiz que le añadí, y lo mantengo:** de ahí NO se sigue que la lectura no
# midiera nada. Excluyó las ramas B/C/D **y mató el 60% superior de mi propia
# banda** (`0,185–0,19` habría salido como `$0,19`). 📌 **Un resultado nulo *para
# discriminar dos hipótesis* no es un resultado nulo.** Importa decirlo porque *"el
# instrumento no tenía finura"* se desliza solo hacia *"no aprendimos nada"*.
# 🧭 **`LM.38` — y el error es MÍO, que es lo que hay que guardar de hoy.** El coste
# **no es una medida, es una cuenta**: `tokens × tarifa`, y encima redondeada para
# mostrarla. Los tokens sí eran medida cruda, **y ya estaban leídos y ya habían
# salido exactos** (consola `21.668/2.959` = `T-093` `21.668/2.959`). Tenía en la
# mano un instrumento sin pérdida, aguas arriba, y sellé la predicción sobre el que
# está aguas abajo y redondeado. 🔑 **No es `LM.15`** (allí el instrumento era ciego
# y devolvía silencio): aquí **no es ciego, es de baja resolución y derivado de otro
# que no lo es.** → **Sella la predicción sobre la medida más cruda que tengas, no
# sobre la que la consola enseña más bonita.**
# 🐛 **Su resumen de inicio decía *"la barra de costo del día 14 en AWS"*, y era
# ANTHROPIC** (`teapp-measure`). `[A-024]`: cuatro bolsillos y no se mezclan. **Su
# propia lista se contradecía sola** — `T-086` seguía listada como pendiente, y si
# `T-095` hubiera sido AWS, `T-086` estaría cerrada por ella. ⚠️ **Es mi error de la
# 73 en espejo** (yo mandé saldar `T-086` con esta lectura por leer el resumen de la
# tarea y no su texto): **cuarta vez en cuatro sesiones que el resumen sale peor que
# el documento, y esta vez cayeron los dos autores en la misma línea.**
# 🔬 **`T-090` — voté NO, y con un dato, no con una opinión.** Leyendo su
# `install.sh` encontré que su propia forma documentada era
# `sudo TEAPP_DOMAIN=... ANTHROPIC_API_KEY=... bash install.sh`. 🔑 **Una variable de
# entorno normalmente NO se ve en `ps`** —el entorno vive en `/proc/PID/environ`,
# que solo lee su dueño, y por eso `create_account.py` tomando la contraseña por
# `environ` fue **correcto** en la 56—. **Pero con `sudo` delante, `VAR=valor` deja
# de ser entorno y pasa a ser un ARGUMENTO de `sudo`**, y las líneas de comandos son
# públicas. 📌 **El precedente de la 56 aplica y falla a la vez: una palabra
# (`sudo`) lo invierte.** No es `LM.20` (*la corrección ya estaba escrita*): es peor
# —**un precedente que no transfiere parece verificado.**
# ⚠️ **Lo entregué marcado como INFERENCIA, no medición**, que es justo lo que llevo
# tres sesiones señalándoles. **Lo midieron ellos en doce segundos**: `sudo
# FOO=secreto123 sleep 30 &` + `ps aux` **desde la cuenta `ubuntu`**, el
# 2026-08-14 a las **18:54 UTC** → dos procesos de `root` con el valor entero a la
# vista. Sospecha → hecho. `T-089` cerrada, y `T-097` (retirar la forma de los tres
# sitios restantes) abierta y cerrada el mismo día.
# 🚨 **`bash -n` NO CRUZABA EL DIFF, y ese fue mi mejor aviso del día.** Reportaron
# *"arreglado y comprobado, `bash -n` → sintaxis OK"*, y los dos cambios eran
# **comentarios y cadenas dentro de un `echo`**: pasar era casi seguro y no tocaba
# lo único que había cambiado de verdad —**si la instrucción nueva funciona**.
# → **`LM.39`: un verde que no cruza el diff no es evidencia sobre el diff.**
# 📌 **Tercera cara del mismo bicho en UN día**: la barra redondeada no distinguía
# dos predicciones, y `bash -n` no distingue una instrucción buena de una que no
# arranca. **Instrumentos reales, que pasan, y ortogonales a lo que se afirma.**
# ✏️ **Y aquí ME EQUIVOQUÉ EN LA DIRECCIÓN DEL RIESGO, aunque la alarma era buena.**
# Predije que `sudo -E` podía no entregar la variable: Ubuntu trae `Defaults
# env_reset` y ni `ANTHROPIC_API_KEY` ni `TEAPP_DOMAIN` están en el `env_keep`.
# **Medido en la EC2: `llego: hola` — sí sobrevive.** La preocupación era legítima y
# el desenlace fue el benigno. **Queda anotado como error de dirección, no como
# acierto** — lo que se salvó es que la instrucción dejó de estar sin verificar.
# 🔗 **Y esa medición decidía DOS preguntas, no una:** si `sudo -E` no hubiera
# sobrevivido, `TEAPP_DOMAIN` tampoco llegaría, y los tres sitios que ellos habían
# dejado (`README.md:45`, `console_steps.md:562`, `install.sh:59`) **no eran "el
# mismo patrón sin secreto dentro": eran el mismo mecanismo.** Una medición, dos
# criterios. 🔑 Y el de más tráfico era el que menos lo parecía: **`install.sh:59`
# es un mensaje de error** — un README se hojea, **un mensaje de error se copia**, y
# se lee justo cuando alguien improvisa una línea de comandos con algo roto delante.
# 🧹 **Ofrecieron quitar el `-s` del `read` "para que quedara igual a lo que se
# corrió el 13", y la oferta iba al revés.** Lo que se corrió el 13 **era un
# instrumento, no un modelo a copiar**; alinear la recomendación con la corrida de
# medición es dejar que la báscula herede a producción. **Es `T-072` de la sesión 50
# otra vez** (`measure_body.py` escribiendo en el `data/` de verdad). El `-s` se
# quedó, y además no necesita medirse: suprimir el eco es definicional.
# ✅ **No hubo que rotar la llave:** `grep -c "sk-ant"` sobre `~/.bash_history` y
# `/root/.bash_history` → **`0` y `0`**. El despliegue real del 13 ya había usado la
# forma segura.
# 🐛 **Cierre: su resumen dijo "dos mediciones" y fueron TRES.** La tercera es
# justamente el `0 / 0` de los historiales, **la que mató la pregunta de rotar** —
# el resultado de más peso del día, ausente del resumen. **Quinta vez del mismo
# bicho, pero invertido: hoy el resumen SUBVENDIÓ trabajo real en vez de
# deformarlo.** Lo detecté porque fui al repo en vez de creerle al parte.
# 📍 **CÓMO QUEDA EL PASO 8:** `T-089` y `T-097` cerradas hoy. `[D-080]` anotada —el
# paso 8 **no cierra**, y con el porqué real (*"una de las cuatro cambió de
# categoría en cuanto se tocó"*, no *"quedan cuatro tareas"*) y con su límite escrito
# para que no sirva de excusa. Abiertas: **`T-088`** (cosmética de verdad, y encima
# depende de bajar a Haiku en el paso 9) y **`T-079`**.
# 📍 **DÓNDE SE ARRANCA MAÑANA: `T-079` de primera, con `[D-077]` abierto y el día
# entero por delante.** La pregunta es si su ✅ se sostiene o se cae por estar
# **cerrada por inferencia** (tercera vez que a esa tarea le pasa). Se aplazó a
# propósito: era la cuarta sesión del día y necesita evidencia propia — **`D-041`
# falló en la 54 no por un mal argumento, sino porque la sesión se acabó antes de
# llegar al clic.**
# ⏳ **`T-086` sigue esperando su lectura de AWS**, con la hora UTC anotada **antes**
# del número — el hábito que salió de `[D-079]`.
# ✅ **Cuarta sesión seguida en que un encargo mío vuelve mejorado** (`[L-060]` es
# suya, el `-s` es suyo, las tres mediciones son suyas). Y por **quinto día** se
# auditó con su sesión **abierta**: cero hallazgos huérfanos (`L-029`).
# 🧭 **La 75 (2026-08-15) FUERON CUATRO RONDAS DE AUDITORÍA SOBRE UNA MISMA
# SESIÓN SUYA, Y EN LAS CUATRO EL ARRANQUE QUE PROPONÍAN VENÍA CON UN DATO
# MUERTO.** Supervisión pura: no ejecuté TEAPP, no llamé a la API, **$0,00**. Leí
# su repo y corrí `git`/`grep`. Commits del día allá: `0e5fe25`, `d3384ff`,
# `5d278a6`. Suite en **440**, y ninguna línea de lógica tocada en todo el día.
# 🐛 **RONDA 1 — proponían empezar por `T-090`, *"la decisión nunca llegó a
# `decisions.md`"*. Falso, y comprobado en doce segundos:** `[D-080]` existía
# entera, 44 líneas, `decisions.md:95`, commit `6c7b5a7`, y su primera frase es
# *"La pregunta era `T-090`"*. 🔑 **Y el porqué es lo que vale:** `progress.md` se
# selló en `8b9b37f` y `[D-080]` se commiteó **después**, en `6c7b5a7`, tocando
# solo `decisions.md`. El archivo de estado quedó congelado con la frase vieja.
# → **`L-029` con vuelta nueva: aquí el trabajo huérfano SÍ se hizo y SÍ se
# commiteó; lo huérfano fue la ACTUALIZACIÓN DEL ESTADO.** Un `progress.md`
# sellado antes que el último commit **miente en la dirección más cara**: dice que
# falta trabajo que ya está hecho, y se paga gastando el arranque siguiente en
# repetirlo. Ellos lo escribieron como `[L-062]`.
# 🐛 **Y el segundo aviso también era falso: `[A-024]` no está "sin comprobar",
# está RETIRADA desde el 2026-08-11** y era falsa **al revés de como la contaban**
# — sí hay tope, y de dos clases (`T-080`, medido en consola: saldo **6,55 US$**,
# recarga automática **DESACTIVADA**, límite mensual 500 US$ inerte). Lo único
# vivo de ahí es el disparador de `[D-057]` —el día que se recargue saldo, el 500
# pasa a ser el único freno y se baja **antes** de volver a llamar— y que **los
# 6,55 son del día 11**, con `T-093` y `T-095` corridas después.
# ⚖️ **RONDA 2 — ME EQUIVOQUÉ, Y SU CORRECCIÓN ES MEJOR QUE MI OBJECIÓN.** Yo
# pedí quitarle el ✅ a `T-079` *"por estar cerrada por inferencia"*, y eso era
# falso: la medición existe, son 60 llamadas reales. **Lo que estaba mal era el
# símbolo, no la medida** — `[D-077]` deja viva una condición que no depende de
# nosotros (*"vale mientras Anthropic responda como el 2026-08-14"*), y eso **no
# se cierra midiendo**: repetir la tanda daría otro verde igual de condicionado
# por otros $0,18. → **`T-079` a 🟡 con el disparador arriba del todo, coste
# $0,00.** Síntoma bien cazado, causa equivocada.
# 🚨 **Pero su argumento traía una frase que contradecía su PROPIO código, y en la
# dirección cara.** Escribieron *"cuatro relojes en paralelo, y la suma cabe en
# los 9,0 por construcción"*; `app/tools.py:239` dice *"los 10 s de `api.py` **NO
# sobran**: son la única garantía de reloj de pared que existe. Aquí abajo no hay
# ninguna que lo sea"*. Dos errores en una frase: **son fases secuenciales** (si
# fueran paralelas el techo sería `max(6,5)`, no la suma `9,0` — su propia
# aritmética los desmiente), y **el `9,0` es una constante nuestra sumada a mano,
# que el SDK no impone**; lo único que corta por reloj de pared es
# `attempt.result(timeout=10,0)` en `api.py:730`. 🔑 **El daño no es semántico:**
# con esa lectura, un día alguien concluye que el `10,0` sobra y retira la única
# garantía que hay. Su código ya preveía ese día; su resumen lo borraba.
# 📌 **Y el eco que no me callé: los DOS cierres anteriores de `[A-011]` murieron
# por colgarse de un techo inexistente** (`[D-070]`, `[L-054]`). El argumento de
# hoy no falla, pero es la **tercera vez** que ese cierre se apoya en un techo.
# ✅ **El reparo de `[A-030]` sí se deshace, y por un camino mejor que el suyo:**
# `connect=1,5` tiene presupuesto propio y **no se come el `read`**, y por encima
# está el `10,0` de pared, que corta **se ejerciten las fases que se ejerciten**.
# No hace falta discutir el reparto.
# 🧠 **Su `[L-063]` es de las buenas del proyecto, y la marcaron ellos:** no
# guarda *"me equivoqué en las fases"*, guarda **la comparación entre los dos
# párrafos del mismo mensaje** — el que citó `tools.py:245` pegado a la afirmación
# salió correcto; el que razonó sin citar nada salió **falso en sus dos mitades**.
# Mismo archivo abierto, mismo minuto. 🔑 **La cita no es cortesía para quien lee:
# es lo que te obliga a mirar antes de afirmar.**
# 🐛 **RONDA 3 — arreglaron la prosa de `T-090` y dejaron la COLUMNA en 🔲.** El
# texto de la fila decía *"✅ CERRADA con `[D-080]`"* y el campo de estado —**el
# que se lee a máquina**— seguía diciendo abierta. Es `[L-062]` **un día después y
# en el archivo que acababan de arreglar**, y el desenlace era predecible: el
# próximo arranque volvería a ofrecer `T-090` como trabajo por hacer. Tercera vez.
# 🚨 **Y `T-088` no estaba aplazada: estaba ARMADA.** Su comentario decía *"da
# igual cuál sea el modelo"* y **el paso 9 es, literalmente, bajar a Haiku** — un
# comentario falso puesto justo delante de quien va a cambiar `MODEL`, el día que
# lo cambie. **Al mirarla resultó peor que su ficha, y lo midieron ellos:** el
# límite es **por modelo**, así que la firma del laboratorio no es el número 50
# sino **el par (espacio, modelo)**; con Haiku `requests_limit == 50` sale falso,
# `main()` imprime *"no es la del laboratorio"* y devuelve `EXIT_OK`. **El portero
# acepta justo la llave que existía para rechazar, sin dar error.** Denegar por
# defecto convertido en aceptar por accidente. Desarmada con **dos comentarios y
# cero lógica**.
# 🧭 **`LM.40` — y es la regla que le faltaba a `[D-080]`** (ellos la guardaron
# como `[L-064]`): **una tarea aplazada espera; una tarea armada tiene
# disparador.** Aplazar la primera es gestión; aplazar la segunda es dejar el
# disparador sin dueño. `T-081` está aplazada —su daño ya está escrito en la ficha
# y nada del paso 9 la activa—; `T-088` estaba armada. ⭐ **Su añadido es mejor que
# mi enunciado:** una lista de pendientes **las iguala a todas por su aspecto**
# —tres renglones, tres 🔲— y **el formato borra la distinción que importa.** Es la
# misma enfermedad que la columna de `T-090` esa misma mañana.
# 🔑 **DOS DE DOS, Y DE LA MISMA FORMA — esto es lo que hay que guardar del día.**
# `T-089` estaba escrita como cosmética y era clase de seguridad; `T-088` estaba
# escrita como *"corregir un comentario"* y era denegar-por-defecto roto. **En los
# dos casos el archivo llevaba un aviso CORRECTO sobre una puerta a pocas líneas
# de una línea que negaba la otra** (`install.sh` y `check_api_key.py`, distinto
# archivo, mismo defecto). `[D-080]` eligió la opción (b) con **un** dato y lo dijo
# honradamente; ahora tiene **dos**. → **`LM.41`: donde un archivo se molesta en
# avisar de una puerta, hay que preguntar si existe una segunda que ese aviso no
# cubre. Un aviso presente baja la guardia sobre el hueco de al lado.**
# ⏱️ **RONDA 4 — el orden del cierre, y el criterio es nuevo: se ordena por
# PERECIBILIDAD, no por importancia.** Preguntaron si escribir el cierre del paso
# 8 o arreglar antes el guion de arranque. El guion es **lo más importante de los
# dos**; el cierre es **lo único que se pudre**: descansa en cuatro juicios hechos
# hoy que solo existen en la conversación, mientras el bug del guion es estable y
# estará igual dentro de veinte minutos. Y el arreglo del guion es de los que se
# ensanchan solos (protocolo de arranque, quizá `CLAUDE.md`, quizá un test):
# empezar por ahí es **exactamente** cómo la sesión 54 se quedó sin llegar al clic
# (`[D-041]`). → Cierre primero, guion después el mismo día, **y número a la tarea
# del guion ANTES de las dos cosas**, que es `LM.40` aplicándose a sí misma.
# ✏️ **Un falso positivo MÍO, y conviene que quede:** mi barrido de `tasks.md`
# marcó `T-079` como fila en desacuerdo, y al abrir el diff la prosa estaba
# reescrita a *"🟡 CERRADA CON CONDICIÓN VIVA"*. **Su verificación era buena y la
# mía tenía ruido.** Un barrido automático que no distingue 🟡 de 🔲 comete la
# misma falta que `LM.40` señala en la lista de pendientes.
# ⏳ **Lo que queda vivo y NO bloquea:** el arreglo del guion de arranque (lee la
# prosa en vez del campo de estado y **no se salta lo tachado** — `A-010`, `A-011`
# y `A-014` esperan turno); el **saldo de `[D-057]`** antes del próximo bucle de
# llamadas sea cual sea; y **`T-086`**, con la hora UTC anotada **antes** del
# número.
# 📍 **CÓMO QUEDA EL PASO 8:** las cuatro miradas una por una, como pedía
# `[D-080]` — `T-089` cerrada midiendo, `T-079` resuelta como condición viva,
# `T-081` aplazada con motivo, `T-088` desarmada. **Falta escribir el cierre como
# decisión.**
# ✅ **Quinta sesión seguida en que un encargo mío vuelve mejorado** (`[L-063]` es
# suya, `[L-064]` mejorada por ellos, el hallazgo del par (espacio, modelo) es
# suyo y medido). Y por **sexto día** se auditó con su sesión **abierta**: cero
# hallazgos huérfanos (`L-029`).
# 🧭 **La 76 (2026-08-16) NO TOCÓ CÓDIGO NI LA NUBE: $0,00, sin API, sin abrir
# TEAPP.** Salió de una pregunta suya: *"en la otra terminal el mismo Claude
# escribe el código y también escribe y corre los tests, ¿eso no está mal?"*.
# Sí lo está, pero no por donde parece — y **la mitad de la respuesta ya estaba
# escrita en este repo**, cosa que se vio al abrir los archivos, no al razonar.
# 📚 **Lo que ya existía y no había que volver a escribir:** el sabotaje entero con
# su tabla (`GUIDE.md` §8.l), las tres familias de casos con los bordes como la que
# todo el mundo se salta (§8.l), el ciclo `ROJO → CONSTRUIR → VERDE → REFACTOR`
# (§11.f), `LM.4` (quien construye no puede ser su propio testigo) y `LM.5` (la
# supervisora vale por lo que no sabe). **Se re-explicó de viva voz material ya
# escrito antes de mirar** — barato hoy porque no costó nada, pero es la forma de
# `LM.20`: la respuesta estaba en el archivo y no se alcanzó.
# 🔑 **El hueco real eran tres cosas, y ninguna estaba:** `LM.4` mira hacia AFUERA
# (por eso hay dos terminales) y **no cubre lo de adentro** — que un test escrito
# después del código hereda el malentendido del código y sale verde confirmándolo;
# que ante un rojo hay una salida barata (ablandar el test) que **borra la decisión
# escrita** y solo se ve en el diff; y que el refactor se cae **por estructura**,
# porque "los tests pasan" es comprobable y "quedó limpio" no lo dice ningún
# comando. → **`LM.42`, `LM.43`, `LM.44`**, escritas en `LESSONS.md`.
# ✅ **Y `GUIDE.md` §11.i, nueva:** *"Cuando el que teclea es un agente"*. Es la
# tabla de cuatro filas (quién define el criterio, quién teclea, qué se exige VER,
# quién verifica), las dos reglas duras para el `CLAUDE.md` de TEAPP, y las dos
# cosas que se miran gratis en el diff. Corta y en tabla a propósito: `LM.27`.
# 📌 **`§11.f` se escribió suponiendo una persona corriendo el ciclo, y desde el
# nivel 7 eso dejó de ser cierto.** No estaba mal: estaba escrita para otro mundo.
# 🐛 **UNA COLISIÓN DE NUMERACIÓN, CAZADA JUSTO ANTES DEL COMMIT.** Las lecciones
# nuevas se escribieron primero como `LM.38`–`LM.40` porque `LESSONS.md` termina en
# `LM.37`. **Falso: `LM.38`, `LM.39`, `LM.40` y `LM.41` ya están nombradas en ESTE
# archivo** por las sesiones 74 y 75 (el `LM.40` de ellas es *"una tarea aplazada
# espera; una tarea armada tiene disparador"*). Renumeradas a `LM.42`–`LM.44` antes
# de commitear. 🔑 **El mecanismo, que es lo que vale:** el número de una lección se
# reserva en `PROGRESO.md` el día que se piensa y se gasta en `LESSONS.md` el día
# que asciende — **son dos archivos distintos, y entre uno y otro el contador no
# existe en ninguna parte.** Mirar el final de `LESSONS.md` es mirar el registro
# equivocado.
# ✅ **DEUDA SALDADA EL MISMO DÍA (segundo commit de la sesión):** `LM.38`, `LM.39`,
# `LM.40` y `LM.41` **ascendieron a `LESSONS.md`**, redactadas desde la narrativa de
# este archivo. Vivían solo aquí, que es exactamente lo que `LM.24` dice que nadie
# alcanza. Ya no hay hueco en la numeración: `LM.36 → LM.44` seguidas.
# 📌 **Lo que se vio al redactarlas:** las cuatro estaban **razonadas y medidas** en
# `PROGRESO.md` —con la corrida detrás—, así que subirlas fue reescribir, no
# reconstruir. **El coste de la deuda no era el trabajo: era el riesgo de que se
# perdieran**, y ese riesgo duró dos sesiones.
# ✅ **Y la quinta también subió, decidida por él: `LM.45`** — *al final de una
# sesión no se ordena por importancia, se ordena por perecibilidad*. Venía de la
# ronda 4 de la 75 (cierre del paso 8 vs. bug del guion de arranque) y llevaba dos
# sesiones sin número. 🔑 **Su núcleo:** lo que se pudre no es la tarea, es el
# estado mental que la sostiene — un bug es materia, cuatro juicios de esta mañana
# son memoria de trabajo. Ante dos pendientes al final, la pregunta no es cuál
# importa más sino **cuál de las dos existe fuera de tu cabeza**.
# 🧭 **Y la conversación siguió hacia CUÁNDO SE CREA UN AGENTE, de una práctica
# suya: montaba TDD con TRES subagentes —rojo, verde y refactor.** El corte estaba
# en el sitio equivocado y **amplificaba `LM.43`**: el agente del verde tiene como
# única métrica que el test pase, que es exactamente la orden mal formulada, ahora
# convertida en puesto de trabajo y en manos de quien no escribió el test. 🔑 **El
# error de fondo es copiar el organigrama:** los roles humanos resuelven un problema
# de cuerpos —una persona no puede estar en dos sitios— y un agente no lo tiene.
# **Lo que un agente no puede es ser testigo de sí mismo, y ese es el único corte
# que compra algo.** → **`LM.46`**, con la pregunta que decide: *¿este agente
# necesita saber MENOS que yo, o MÁS?*
# ✅ **Segunda pregunta suya, y la respuesta fue que sí: un subagente verificador
# DENTRO de la sesión que construye, antes de la auditora.** Pasa el test de
# `LM.46` —necesita saber menos— si recibe el criterio y el diff **y no la
# narrativa**, y sin permiso de escribir. Caza lo mecánico (¿existió el rojo?, ¿el
# refactor tocó tests?, ¿se ablandó alguno?) y **no** puede juzgar si el criterio
# estaba bien: eso sigue siendo de la terminal auditora. 🚨 **El peligro es `LM.41`
# con otro traje: un veredicto verde se vuelve coartada** y la auditora baja la
# guardia sin decidirlo. → **`LM.47`: evidencia con salida cruda, nunca veredicto; y
# lista cerrada, donde lo no mirado se declara NO MIRADO.**
# ✅ **Y las dos bajaron a `GUIDE.md` el mismo día: §11.i.2** (cuándo crear un
# subagente, con la pregunta que decide y la tabla de las tres razones) **y
# §11.i.3** (el verificador: qué recibe, su lista cerrada, y las dos reglas). Más
# un aviso dentro de §11.i contra repartir el ciclo de TDD entre tres agentes.
# 📌 **§11.i.2 es la parte más portable de todo esto: no depende de TDD ni de este
# curso.** Si crece, pide sección propia.
# 📌 **`LESSONS.md` cierra la sesión en `LM.47`, sin huecos y sin candidatas
# sueltas.** El bloque Método pasó de **37 a 47** lecciones en un día. Ocho de las
# diez ya estaban razonadas y medidas de sesiones anteriores; **las dos nuevas
# (`LM.46`, `LM.47`) salen de conversación, sin corrida detrás, y lo dicen dentro.**
# ➡️ **SIGUIENTE PASO CONCRETO, y es en la OTRA terminal:** copiar a la
# `CLAUDE.md` de TEAPP las dos reglas duras de tests que quedaron redactadas en
# `GUIDE.md` §11.i — *(1) ante un rojo se arregla el código; modificar o borrar un
# test exige autorización explícita con la razón escrita; (2) el refactor se pide
# explícitamente cada ciclo*. **Nada de esto está todavía en TEAPP:** hoy solo se
# escribió el método aquí. Y si monta el subagente verificador, §11.i.3 tiene su
# lista cerrada y las dos reglas.
# ⏳ **Lo del nivel 7 que sigue vivo y NO lo tocó esta sesión:** el arreglo del
# guion de arranque de TEAPP (lee la prosa en vez del campo de estado y no se salta
# lo tachado; `A-010`, `A-011`, `A-014` esperan turno), el **saldo de `[D-057]`**
# antes del próximo bucle de llamadas, y **`T-086`** con la hora UTC anotada antes
# del número.
# 🧾 **Cierre de la 76: CINCO commits en vez de uno**, contra la regla de
# `CLAUDE.md`. Pasó porque el primero se hizo cuando él pidió cerrar y el trabajo
# siguió después — cada uno lleva su razón escrita. **No es el patrón a repetir:**
# el motivo real es que la sesión no había terminado cuando se selló la primera vez.
# 📌 **Lo que NO se hizo a propósito:** no se tocó el `CLAUDE.md` de TEAPP. Las dos
# reglas duras quedan en `GUIDE.md` §11.i como texto listo para copiar allá cuando
# se abra esa terminal.
#
# ---
#
# 🧩 **SESIÓN 77 — la trajo él, y es de plan, no de código: LAS TRES PREGUNTAS.**
# Arrancó preguntando *cuándo se trabaja seguridad —guardrails, inyección— porque le
# causan dolor de cabeza*, y terminó en algo más grande: **que las tres no se le
# olviden en los proyectos futuros que construya con lo aprendido aquí.**
# 🔎 **El diagnóstico fue que las tres NO estaban en el mismo estado**, y meterlas en
# la misma frase era justo lo que confundía:
#   - **Evaluación → hecha** (nivel 5 + 5b). Hoy no es estudio: son los 348 tests de
#     TEAPP. Lo que queda es mantenerla.
#   - **Observabilidad → declarada, no construida.** Pieza propia del nivel 7 desde
#     la sesión 6; el `registro.jsonl` del nivel 4 es su primer ladrillo.
#   - **Seguridad → NI declarada.** Único hueco real: existía en pedazos bien
#     aprendidos (`L5b.9`, `LM.13`, `LM.22`, los guardrails del nivel 4) **y sin
#     ningún sitio que los juntara**. Aparecía solo cuando algo se rompía.
# 🔑 **Lo que las une:** las tres solo tienen respuesta medible **cuando hay alguien
# afuera usando la cosa** — por eso las tres aterrizan en el nivel 7, y no es
# desorden del plan. Evaluación pregunta *¿funciona?* **antes**; observabilidad
# *¿qué está pasando?* **mientras**; seguridad *¿qué puede hacer y qué le pueden
# hacer?* **porque está expuesto**.
# 🚨 **Y el riesgo de escribirlo mal ya lo tenía medido este repo:** dejarlo solo en
# `LESSONS.md` es dejarlo **cierto y fuera de alcance** — `LM.20`, que en este repo
# ya pasó tres veces (`T-068`, el freno de `T-059`, la tabla de `A-014`).
# `LESSONS.md` y `GUIDE.md` se leen **cuando alguien va a buscarlos**; `CLAUDE.md` se
# lee **siempre, sin buscarlo**. De ahí el reparto de hoy, uno por archivo:
#   - **`CLAUDE.md`** → sección nueva *Las tres preguntas*: en CUALQUIER proyecto
#     nuevo se **declaran** antes de la primera línea del producto. Corto, un
#     puntero. Es el contrato, no el manual.
#   - **`GUIDE.md` §6.b** → las tres como casillas ejecutables dentro de la checklist
#     de proyecto nuevo. **§6.c nueva**: guardrail ≠ inyección, la regla del modelo
#     que no es la barrera, y las tres consecuencias.
#   - **`LESSONS.md` → `LM.48`** → el porqué. El bloque Método pasa de 47 a **48**.
#   - **`README.md`** → seguridad entra al mapa como pieza nombrada del nivel 7, y
#     **el tercero de "los tres temas que se preguntan siempre" cambia**: el proyecto
#     integrador dejó de ser una pregunta el día que lo construyó, y su sitio lo
#     ocupa seguridad. Su descripción queda intacta más abajo.
# 🔑 **Las dos ideas que hacen el trabajo, y las dos son eco de lecciones suyas:**
#   1. **`LM.13` aplicado a las casillas** — una casilla marcada con una intención no
#      es un freno, es una nota. Cada una se marca con un **artefacto que existe**:
#      tests **con un rojo real** (`LM.42`), un registro **ya abierto** para
#      responder algo, y **la lista de herramientas del agente con sus permisos** —
#      que *es* la superficie de ataque.
#   2. **Se declaran, no se construyen, el día 1.** Al día 1 no hay observabilidad de
#      producción y no se pide: lo que sí puede haber es **dueño y sitio**.
# 📌 **Y el orden entre ellas es por DEPENDENCIA, no por importancia:**
# observabilidad antes que seguridad, porque **sin registro no puedes ver morder un
# freno de seguridad** ni demostrar que un ataque ocurrió.
# 🩹 **El dolor de cabeza tenía causa concreta, y quedó escrita:** son dos cosas
# distintas con el mismo miedo. Un **guardrail** es un freno tuyo contra accidentes;
# una **inyección** es un ataque. Se intenta frenar el segundo con el primero —con
# instrucciones al modelo— y por eso no funciona y no se ve por qué. **El modelo
# nunca es la barrera: la barrera vive en el código, fuera del modelo.** Ya lo había
# aplicado sin ponerle nombre en `T-071` (arreglado en el origen, `app/tools.py`).
# ➡️ **SIGUIENTE PASO CONCRETO — sin cambios, sigue siendo el de la 76 y es en la
# OTRA terminal:** copiar a la `CLAUDE.md` de TEAPP las dos reglas duras de tests de
# `GUIDE.md` §11.i. **Hoy no se tocó TEAPP** — esta sesión fue de plan.
# ⏳ **Lo que queda pendiente de ESTA sesión, y es chico:** `07-produccion/README.md`
# (el puente) todavía **no nombra la pieza de seguridad** que el mapa ya le asigna.
# No se escribió a propósito: ese archivo guarda análisis medido, y la pieza se
# redacta cuando se trabaje, no antes.
# ⏳ **Y sigue vivo del nivel 7, intacto desde la 76:** el guion de arranque de TEAPP
# (`A-010`, `A-011`, `A-014`), el saldo de `[D-057]` y `T-086`.
#
# ---
#
# 🔬 **SESIÓN 78 (2026-08-17) — SUPERVISIÓN PURA. Tres hallazgos de apertura, y
# los cuatro del día resultaron ser EL MISMO. Cerrada en TEAPP con `41c753f`.**
# Esta terminal no tocó TEAPP: leyó, midió desde fuera y entregó. La otra corrigió
# y cerró — **440 tests**, árbol limpio, sin `ahead`.
# 🔴 **H-1 — el freno del paso 9 no existía; era un comentario.** `check_api_key.py`
# avisa en mayúsculas de que la firma del laboratorio es **el par (modelo, límite)**,
# y el test que parecía vigilarlo clavaba **media firma**: `LAB_REQUESTS_PER_MINUTE
# == 50`, y nada sobre `MODEL`. El escenario exacto que `[D-049]` tiene programado
# **dos veces** dentro del paso 9 (Sonnet 5, Haiku 4.5) dejaba los 440 **en verde**
# con el portero mudo. Arreglado clavando el par, con el rojo enseñado y **la
# salvedad escrita dentro** (no lee la consola; verifica que nadie mueva media
# firma sola). Es `LM.13` con el nombre puesto: *un freno que no has visto morder
# es una nota* — y aquí la nota era literalmente un comentario.
# 🟠 **H-2 — un día entero que no ocurrió, escrito 40 veces en 6 archivos.** Toda
# la sesión `[S-060]` de TEAPP se fechó **2026-08-15**; sus commits son del **14**,
# el último a las 15:16 -0500. **Cazado cruzando `git log` con la prosa**, no
# leyendo. Descartado el reloj como sospechoso con el discriminador limpio: **este
# repo fechó bien el 16 desde la misma máquina**, y ninguno de los dos tiene
# commits el 15. La fecha se había colado hasta **las dos skills del protocolo** y
# hasta dentro de `[L-062]`–`[L-067]`, cinco lecciones que existen para cazar
# afirmaciones que nadie fue a apagar.
# 🚨 **Y al corregirlo se cayó el REMEDIO, que es el mejor hallazgo del día y es
# suyo:** `[L-067]` había dejado escrito *"si la fecha de la última fila no es la
# de hoy, falta la entrada"* — y **ese criterio habría dado VERDE en el caso que lo
# originó**, porque hubo cinco cierres el mismo 14 y la fila de arriba ya llevaba
# la fecha de hoy siendo de otro tramo. Cambiado a comparar el **id**. *Una regla
# que no caza su propio caso es una nota.*
# 🟡 **H-3 — las dos reglas duras de `GUIDE.md` §11.i no habían llegado a TEAPP.**
# Entraron como `PI-6` y `PI-7`. 🔑 **Y entraron desde el VERBATIM, no desde mi
# paráfrasis** — porque él pidió el original antes de tocar la constitución del
# proyecto, que era la decisión correcta. A mi paráfrasis se le habían caído tres
# cosas y **una era de carga: "del humano"**. Sin el actor, la autorización para
# ablandar un test la puede firmar la sesión que construye o esta terminal: **la
# regla se firma sola y deja de existir.** También perdí la regla 2 en pasiva, que
# **invierte quién pide el refactor**. Y no le pasé las dos comprobaciones que
# hacen exigible la regla 1 —el diff de los tests aparte, y que el rojo existiera—,
# que eran la mitad útil.
# 🏚️ **H-4, que salió de H-3 — la dirección de los `[LM.nn]` NACIÓ falsa, en tres
# sitios.** La tabla de citas de TEAPP mandaba a `Edu_TripleS/PROGRESO.md`; viven
# en **`LESSONS.md`**. No caducó: el conteo del día en que se escribió (`a12ba3c`,
# 2026-08-09) da **`LM.1`–`LM.23` en `LESSONS.md`, `LM.13` incluida** — la única
# lección que la propia tabla cita de ejemplo. Y el sitio es la lección entera:
# **la dirección falsa vivía dentro del recuadro que enseña a distinguir `LM.13` de
# `L-013`**, es decir, dentro del arreglo de la sesión 58 que cazó 16 citas malas.
# ⚠️ **Es de la clase muda por un motivo concreto:** `PROGRESO.md` **menciona**
# `LM.nn` unas 200 veces y **no define ninguna**. Quien sigue la dirección mala
# *encuentra* lo que busca. → La comprobación no es *"¿hay menciones allí?"* sino
# **"¿cuántas DEFINICIONES hay allí?"** — se cuentan encabezados, no apariciones, y
# **en los dos destinos**.
# 🪞 **Y la cuarta vuelta cayó sobre MÍ, catorce horas después de proponer la
# regla.** Mi fundamento para *"nació falsa"* era flojo: dije *"el bloque `LM` está
# en `LESSONS.md` desde el 05, la tabla es del 09"*, **y eso no se sigue** — el
# archivo crece de a poco, y hubo de hecho una ventana (`LM.27`–`LM.31`, pagada en
# la sesión 70) en que algunas vivían **solo** en `PROGRESO.md`. Acerté la
# conclusión por un camino que podía haber dado la contraria. Enmendado **antes de
# su commit**, con el conteo del día: por eso se audita con la sesión del otro
# abierta y no después (`L-029`).
# 🔑 **LO QUE SE LLEVA EL DÍA, Y YA TENÍA NÚMERO: `LM.32`.** *El sitio con más
# probabilidad de esconder el error siguiente es la corrección que acabas de
# hacer.* Cuatro caras en una jornada y de **tres dueños distintos**: un test con
# el nombre correcto, una regla de comprobación recién escrita, el arreglo de una
# auditoría, y **la auditoría del arreglo**. 📌 **No se escribe `LM.49`**: sería
# `LM.32` dicha otra vez, y este repo ya sabe lo que cuesta la misma cosa escrita
# en dos sitios. Lo que sí gana `LM.32` es su formulación operativa —**cuando
# alguien arregle algo que tú señalaste, el arreglo entra en la cola de auditoría,
# no sale de ella**— confirmada sobre el auditor mismo.
# 📌 **Ninguno de los cuatro daba error. Los cuatro daban verde.**
# ➡️ **SIGUIENTE PASO CONCRETO — el paso 9 de TEAPP, y es en la OTRA terminal:**
# *Observabilidad y evals con rúbrica*. Empieza tocando `MODEL`, y ahí muerde el
# disparador: leer en la consola de `teapp-measure` el límite por minuto del modelo
# nuevo y ponerlo en `LAB_REQUESTS_PER_MINUTE` **en el mismo cambio**. Salta al
# menos dos veces. **La diferencia con esta mañana es que ya no depende de que
# alguien lea el comentario: la suite se pone roja.**
# ⏳ **Y sigue vivo, sin tocar hoy:** el saldo prepagado de Anthropic antes del
# próximo bucle de llamadas (**con la hora UTC anotada antes del número**, `T-086`),
# `T-067`, `T-069` (fecha tope ≈ 2026-09-01, la única con reloj de verdad), `T-046`
# y `T-081`. Y de esta terminal: `07-produccion/README.md` todavía no nombra la
# pieza de seguridad que el mapa le asigna desde la 77.
#
# ---
#
# 👁️ **SESIÓN 79 (2026-08-17, la segunda del día) — OBSERVABILIDAD. El paso 9
# arrancó, y arrancó por aquí: esta terminal entregó la especificación y la otra la
# construyó. Cerrada en TEAPP con `c292210` — 452 tests, árbol limpio.**
# 🔴 **ABRIÓ CON UN FRENO ESCRITO QUE NADIE TENÍA DELANTE (`LM.20`, quinta vez).**
# El reporte de arranque preguntaba *"¿paso 9, o el saldo primero?"* como si fuera
# una preferencia. `[D-081]` ya lo había decidido, verbatim: *"Se lee **antes del
# próximo bucle de llamadas, sea cual sea**, con la hora UTC anotada ANTES del
# número"*. 📌 **Y el matiz importa, y va a favor de ellos:** *"sin bloquear"* era
# sobre el cierre del paso 8, y la condición no es *antes del paso 9* — es **antes
# de la primera llamada**. El paso 9 se abre sin gastar un centavo.
# 💵 **SE LEYÓ, Y EL DESCUADRE TENÍA DUEÑO: `$6,24`** (hora fijada antes del
# número). Se esperaban ~$6,37. **El tercer inquilino del saldo es ESTE CURSO** —
# invisible en la vista de COSTO porque enseña *"solo uso de API"*. → **`[C-009]`, y
# no es un número: mata una premisa.** `[D-057]` y `[D-058]` calculaban
# *"días-persona"* dando por hecho que solo TEAPP gasta. **El saldo puede agotarse
# sin que TEAPP gaste nada.** ⚠️ Consecuencia derivada, apuntada y no perseguida: si
# la llave de este curso vive en `Default`, está en el **único espacio que no admite
# tope** (`[D-059]`) — el tope de $2,00 de `[D-062]` capa al laboratorio, que era el
# sospechoso equivocado.
# 🔬 **EL MÉTODO DEL DÍA: no se escribió un registro nuevo, se INTERROGÓ el que ya
# existía.** Ocho preguntas contra sus dos `registro.jsonl` reales (nivel 4 y 5b
# paso 9), **$0,00 y sin llamar a Claude**. Contestan 1 y 2 (costo, tiempo total);
# fallan las demás. → **La regla: un registro se diseña por la pregunta que alguien
# va a hacer el día que algo se rompa, no por lo que es fácil escribir. Y mientras
# nadie se la haya hecho, es un archivo — no observabilidad.** Es `LM.13` con otro
# traje: un freno que no has visto morder es una nota.
# 🔴 **El hallazgo que decide si el paso 9 sirve: NADIE REPARTE EL TIEMPO.** En su
# corrida del 5b, **20,7 s de Claude sobre 59 s totales**. `[D-049]` mete en el paso
# 9 el descenso a Sonnet 5 y Haiku 4.5 — y **cambiar de modelo solo acelera la parte
# de Claude**. Si el reparto se parece, el descenso compra un tercio. ⚠️ **El
# principio viaja, el número NO** (esa corrida no es TEAPP; la otra terminal puso el
# matiz y es correcto). Y ellos aportaron el remate: `app/tools.py` **ya** parte el
# presupuesto en `connect`/`write`/`pool`/`read` — la arquitectura ya piensa en
# fases y el registro no las escribía. **El campo no inventa una idea: le pone
# instrumento a una que ya está en el código.**
# ⚠️ **La salvedad que salva el titular (`LM.16`):** los 385 s del nivel 4 **no** son
# la app siendo lenta — era él autorizando permisos a mano. Un registro que no marca
# la espera humana entrega un 89% **cierto e inútil**.
# 🔀 **CONVERGENCIA, que vale más que un acuerdo:** las dos terminales encontraron
# lo mismo por caminos que no comparten fuente. Ellos leyendo `api.py` hasta el
# `return` de la línea 838 (la práctica exitosa no escribe nada); esta interrogando
# el `registro.jsonl`. **El caso más frecuente de la app —que funcione— era
# invisible.** Mismo cruce que hizo `[D-058]` con la consola contra los tokens.
# 🚨 **LA CUARTA PREGUNTA, y `.gitignore` no la cubre.** Su pregunta era *qué se
# guarda, dónde vive, cuánto tiempo*. Falta **quién puede leerlo**. `data/` está en
# `.gitignore` y tapado. El flanco abierto es otro: **una frase de una persona
# copiada a mano dentro de una lección** como ejemplo. `_persistence/` **sí** va a
# Git y **es público** (`[C-007]`: *"antes de escribir en `_persistence/` se asume
# lectura mundial"*). Ninguna herramienta valida esa prosa. **Es la clase muda: la
# misma por la que viajó la fecha del 15 a seis archivos.** → **`PI-8`**.
# 🎯 **LA TENSIÓN EVALS↔PRIVACIDAD ERA FALSA HOY, y se resolvió por secuencia.** Su
# argumento —*si guardamos solo números, me toca inventarme las frases*— cayó con
# tres datos: (1) **no hay frases que recolectar**, porque su propia pregunta 1 es
# *"¿alguien está usando esto?"* y no lo saben; (2) **inventarlas ya es la práctica y
# fue buena**: `measure_tutor.py` lleva 60 frases A1 elegidas a propósito, que es lo
# que un eval necesita y una cosecha aleatoria no da; (3) **un conjunto de prueba es
# una cosecha, no una llave abierta** — sus propios `examen_*.jsonl` del 5b son un
# archivo fijo. **Reparto de tres filas: traza operativa (forma, nunca la frase) ·
# material de evals (aplazado con razón) · `_persistence/` (ninguna frase de nadie,
# nunca, ni como ejemplo).**
# 🪞 **DOS ERRORES DE ESTA TERMINAL, los dos cazados por la otra, los dos de
# MECANISMO — y los dos con la conclusión correcta por un camino que podía fallar:**
#   1. **Dije que la traza «hereda el portero» de `T-071`.** Falso: el portero toma
#      un `md5` de `data/` antes y después de cada test — da **limpieza de la suite,
#      no privacidad**; la privacidad la da `.gitignore`. Y el módulo **nombra su
#      propio punto ciego**: lo que corre fuera de pytest. **El modo normal de la
#      traza es exactamente ese.**
#   2. **Dije que congelar la ruta en una constante de módulo pondría el test
#      rojo.** Falso: `require_data_dir()` corre al importar y la suite **ni
#      arranca** (`ImportError`). → **Un sabotaje que rompe la carga no es un
#      sabotaje: parece más contundente y demuestra menos.** El alcanzable es una
#      caché. **Lección suya, y la repitieron una hora después** pese a tenerla
#      escrita en `[D-086]` → **la receta del sabotaje tiene que vivir donde se
#      sabotea**, no en una decisión: dentro del docstring del test.
# ✅ **Y DOS ENMIENDAS MÍAS QUE SÍ AGUANTARON, las dos del mismo tipo — estructura
# contra acordarse:**
#   1. Su *"acuérdate de desviar la traza en `conftest.py` en el mismo cambio"* era
#      el mundo **anterior a `[D-037]`**: `conftest.py:81` desvía **una** variable y
#      `users_dir()`/`quota_dir()`/`accounts_file()` cuelgan las tres de
#      `require_data_dir()`. **No hay tres sitios que desviar ni habrá cuatro** —
#      comprobado después: la traza escribió en la carpeta desviada sin tocar
#      `conftest.py`. 🔑 **Su remedio era el mecanismo que `[L-023]` costó quitar:
#      aquel fallo no pasó por falta de una nota, pasó porque el remedio ERA
#      acordarse.** Lo que sí quedó, y es comprobable: **la ruta se resuelve llamando
#      a una función, nunca en una constante** (se congela al importar).
#   2. **La fila 3 no podía vivir solo en `decisions.md`** — `LM.20`, que en este
#      proyecto ya mordió cinco veces. Ascendida a **`PI-8` en `CLAUDE.md`** (se lee
#      sin buscarlo) + casilla en `protocol-close`. ⚠️ **Con su debilidad escrita en
#      los tres sitios: `PI-8` pregunta, no detecta.** Es más flojo que `PI-6`/`PI-7`
#      y decirlo es lo que impide marcarlo con una intención.
# 🚨 **EL HALLAZGO DEL DÍA FUE DE ELLOS Y CONTRA ELLOS: el campo nuevo nació sin
# guardián.** `correct: bool` se añadió a `TutorReply` para la traza; saboteado con
# `correct=True` clavado, **la suite dio 447 en verde**. Podía mentir en producción.
# **Causa: los tests cubrían las cuatro piezas viejas una por una, así que el archivo
# se leía como cobertura completa de la clase.**
# 🔑 **Y la SEGUNDA MITAD la puso esta terminal: su arreglo cubría el caso y dejaba
# la fábrica viva.** Nada enumeraba los campos desde la clase (comprobado: cero
# apariciones de `dataclasses.fields`, `model_fields` o `__annotations__` en todo el
# repo). **El sexto campo iba a nacer igual de mudo, y encima con más aspecto de
# rigor.** → **Tres alambres puestos y los tres vistos morder** (`TutorReply`,
# `GrammarVerdict`, `Counters`; los `BaseModel` de `api.py` ya estaban clavados de
# rebote por comparación de diccionarios). **452 passed.**
# 🔑 **LA LECCIÓN DEL DÍA, candidata a `LESSONS.md`:** *El hueco no aparece donde el
# código es difícil. Aparece donde un conjunto que estaba completo acaba de crecer en
# uno.* Tercera cara en tres días: media firma en `T-099`, los 26 casos verdes con el
# contrato roto en tres sitios del 5b, y el quinto campo de `TutorReply`.
# 📌 **Y el criterio de dónde va el alambre, para que no sea creep:** lo merece la
# clase **cuyos campos viajan en bloque a un sitio donde nadie los mira uno por uno**
# (se serializan, se persisten, se comparan enteros). **Un alcance que cabe en una
# tabla con última fila no es creep.**
# 🆕 **`PI-8` se estrenó el mismo día y ya afinó la regla:** el closer distinguió
# bien *"quien usa la app"* de *"el dueño del proyecto conversando con el agente"* —
# y **esa distinción no está escrita en `PI-8`**. Acertó por buena lectura, no porque
# la regla lo dijera. **`LM.13` sobre la regla misma: esa frase va dentro.**
# ➡️ **SIGUIENTE PASO CONCRETO — seguir el paso 9 por observabilidad, en la OTRA
# terminal:** el **reparto del tiempo por fase** (`connect`/`write`/`pool`/`read`),
# que es el campo del que depende poder juzgar si el descenso de modelo ayuda.
# ⏳ **Vivo con disparador de ACCIÓN, no de fecha** (forma correcta, `[D-081]` /
# `[L-064]`): **`T-102`** — la traza no se ha visto escribir con el servidor
# levantado y una llamada real; salta en la primera llamada del descenso de
# `[D-049]`, montada encima de un gasto ya decidido en vez de pagar aparte de un
# saldo que `[C-009]` declaró compartido. **`PI-4` NO se declara cumplido.**
# 🔲 **Y PENDIENTE DE ESTA TERMINAL, sin escribir hoy por falta de sesión:** la
# **Pieza 8 de `07-produccion/README.md`** — las ocho preguntas con sus respuestas
# medidas, el reparto del tiempo, la cuarta pregunta y el reparto de tres filas. Va
# después de `## Pieza 7 — El orden de los pasos`. **Hoy vive en la conversación y en
# TEAPP, no en el puente.** Sigue sin nombrar la pieza de seguridad — aunque hoy le
# salió su primer artefacto real, que es `PI-8`.
# 🔴 **LA 80 PARÓ EL CAMPO QUE ESTA MISMA TERMINAL HABÍA PROPUESTO, y el error era
# mío.** El paso natural del día era escribir en la traza el reparto
# `connect`/`write`/`pool`/`read`. **No se puede medir: son TOPES, no relojes.**
# `app/tools.py:245` es `anthropic.Timeout(connect=1.5, write=0.5, read=6.5,
# pool=0.5)` — un presupuesto que se le **entrega** a la librería, no un cronómetro.
# Y el dato no existe aguas abajo: en el `httpx 0.28.1` instalado hay **un solo
# número**, `_client.py:157`, el total de la respuesta entera; los `monotonic()` de
# `httpcore` son la expiración del *keepalive*. **Comprobado en la librería del
# disco, no en la documentación** — `ctx7` falló y no se contestó de memoria.
# 🤝 **Y ellos lo remataron con lo que yo no miré:** ese `.venv` tiene **dos**
# librerías, `httpx 0.28.1` y `httpx2 2.9.1` (la del `TestClient`). Miraron la
# segunda: otro `elapsed` único y total. **La conclusión aguanta por partida doble.**
# 🔑 **LA LECCIÓN DEL DÍA, y es contra mí: un tope no es un reloj.** Declarar cuánto
# se le permite durar a algo no es haber medido cuánto duró. `[D-085]` decía *"la
# arquitectura ya piensa en fases y el registro no las escribe"* — **cierto y
# venenoso**: se lee como si los números existieran y solo faltara apuntarlos.
# 📌 **Y es la sesión 59 con una vuelta peor.** Allí la lección fue *abrir el archivo
# no basta*. Aquí **abrí la tabla de las cuatro fases** (`tools.py:182-185`), la leí
# entera, y **leí un límite como si fuera una medida.** No fue por no mirar.
# ✅ **El reparto que SÍ decide `[D-049]` resultó más barato que el descartado:** hay
# **una sola** llamada al modelo en toda la app (`tools.py:489`) y `MAX_RETRIES = 0`,
# así que un cronómetro y ya está. **Pero son TRES números, no dos:** el reloj de la
# ruta arranca **antes del `submit`** (`api.py:733`, a propósito — mide lo que espera
# la persona), así que `total − modelo` es *"cola + nuestro código"*. **Sin separar la
# cola, el descenso de modelo parecería inútil cuando el culpable sería la cola.**
# 🧰 **Y la pregunta de diseño que trajeron era buena: ¿el reloj contamina las dos
# cajas?** Voto de esta terminal: **una caja, no dos.** `respond()` ya tiene la
# llamada en una línea propia, así que mide desde fuera y `GrammarVerdict` no se
# toca. 🔑 **El argumento que lo cerró estaba en el disco:** de los cinco campos de
# `TutorReply`, **tres no vienen del juez** (`words` es local, `score`/`practice`
# salen del archivo de contadores). **La contaminación que temían ya había ocurrido
# en `[D-066]`, y con razón** — la caja no es "qué dijo el tutor", es "lo que la ruta
# necesita saber de esta práctica". El reloj **encaja en el significado que ya tenía**.
# 🚫 **La cola no pasó por ninguna caja:** un cierre creado **dentro** del handler
# (`api.py:748-754`), uno por petición. Descartada la global, que se pisaría entre
# prácticas simultáneas **y en silencio**, que es el modo de fallo peor.
# 🦷 **EL ALAMBRE DE AYER MORDIÓ, y en un caso que nadie le preparó.** Añadir
# `model_seconds` puso rojo solo al test que clava los campos de `TutorReply`
# (`Extra items in the left set`). **Segunda vez visto morder**, y esta vez de
# rebote. Tres sabotajes más, los tres con su rojo visto — el bueno es el segundo:
# **un reloj demasiado ancho también sube y baja con el juez**, así que pasaría
# cualquier test que solo mirase la cota de abajo.
# 🚨 **AUDITORÍA DEL CIERRE, y llegó a tiempo:** cuando preguntaron *"¿cerramos?"*,
# `git status -sb` tenía **ocho archivos sin commitear** — el día entero en un solo
# disco. Es el animal de la sesión 33 esperando su turno. Avisado, y cerraron bien:
# **`25332da` en `origin/main`, árbol limpio, diez archivos** — verificado aquí.
# ✅ **Y su `closer` hizo lo que esta terminal predica: no se fio del número que le
# pasaron, corrió la suite. 456 en verde.** `LM.23` cumplida por ellos solos.
# 🔍 **Verificado y no reportado:** `app/tools.py` **no aparece** en el commit.
# `GrammarVerdict` quedó intacto de verdad, no de palabra.
# ⚠️ **Detalle menor anotado, no arreglado:** los cuatro tiempos se redondean por
# separado, así que la identidad escrita en el docstring de `trace.py`
# —`seconds = queue + model + rest`— puede fallar por un milisegundo al leerla en el
# archivo. No mueve ninguna decisión; pero es una identidad escrita.
# 🪞 **Y lo trajeron ellos, que es lo que vale:** actuaron sobre **mi voto técnico**
# sin que el estudiante hubiera votado, y lo dijeron sin que nadie preguntara.
# **Un voto verificado contra el disco no es la decisión de su dueño.**
# ➡️ **SIGUIENTE PASO CONCRETO, y sigue siendo el mismo de la 79 — en la OTRA
# terminal:** seguir el paso 9. Con el reparto ya puesto, lo que viene son los
# **evals con rúbrica**, y detrás el descenso de modelo de `[D-049]` — que es lo que
# el reparto existe para poder juzgar.
# ⏳ **Vivas con disparador de ACCIÓN:** **`T-102`** (ver la traza escribir con el
# servidor levantado y una llamada real) y **`T-103`**, nueva — el hueco del
# `IndexError` en el camino del timeout, **sacada como tarea propia en vez de
# quedarse enterrada en un comentario**, que es lo que le da dónde morir.
# 🐛 **LA 81 CAZÓ UNA FECHA INVENTADA, Y LO QUE ENSEÑA NO ES LA ERRATA.** La sesión
# 80 se fechó **2026-08-18** cuando sus tres commits son del **2026-08-17** (10:54,
# 15:04, 15:41). Viajó a **17 sitios**: 16 en TEAPP y **`PROGRESO.md:6`, aquí**.
# 🔑 **La fecha buena ya estaba en el repo:** el commit de las 10:54 de esa misma
# mañana escribe `2026-08-17` bien, y las dos sesiones de la tarde no se tropezaron
# con ella ni una vez. `LM.20` otra vez — y `[L-069]` **ya existía y no frenó nada**.
# Una lección escrita en un archivo no muerde: es `LM.13` aplicada a la memoria.
# 🚨 **Y el hallazgo mejor salió DE LA CORRECCIÓN, no del error.** La otra terminal
# corrigió mi conteo —*"son 16, no 13"*— y tenía razón dentro de TEAPP, pero al
# hacerlo **perdió la única aparición que estaba fuera de su repo**, que yo había
# listado con ruta y línea. **Un número que sube y trae una tabla se lee como
# estrictamente mejor, y nadie audita un dato que acaba de mejorar.** `LM.15` con
# otra piel. 📌 **Sin culpa de nadie, y esa es la parte útil: cada terminal contó su
# propio repo. Lo escribimos dos y lo contamos cada uno en su patio.**
# ✅ **Reemplazo auditado leyendo el diff, sin ejecutar TEAPP:** `16 insertions,
# 16 deletions`, **ni una línea del diff que no fuera la fecha**, 0 apariciones en
# el árbol. Los cuatro bloques 🔴 de enmienda quedaron coherentes.
# 🛑 **`T-103` NO era un bicho vivo, y el código de ellos ya lo decía.** El camino
# del timeout muere en `raise HTTPException(504)` (`api.py:804`); `tutor_started[0]`
# se lee en la **906**. Nunca se llega. `api.py:892-897` y el docstring de
# `test_api.py:690-693` lo dicen bien — **el resumen que llegó al estudiante se comió
# la salvedad**. Cuarta vez de este patrón: *el documento es bueno y su resumen es
# peor que él*. Parada con disparador de acción, como `T-102`.
# ⚠️ **Y lo dijeron ellos solos, que es lo que vale:** parar `T-103` eran **dos votos
# técnicos, no su firma**. Quedó como `T-104`.
# 🔲 **PENDIENTE DE ESTA TERMINAL POR CUARTA SESIÓN: la Pieza 8 de**
# **`07-produccion/README.md`. NO se escribió hoy tampoco** — la sesión se fue en la
# auditoría de la fecha. Es el mismo modo de fallo que `D-041` en la 54: no falló
# por un argumento, **se agotó la sesión antes de llegar**. Ahora le toca contar
# además la fecha que cruzó dos repos y el conteo que no la alcanzó.
# 🔲 **PENDIENTE ANTERIOR (79 y 80), sigue vivo dentro de la Pieza 8 de
# `07-produccion/README.md`.** Ya no es solo lo de la 79 — ahora le toca contar
# también **el tope que no era reloj** y **el reparto en tres**. Cada sesión que pasa
# tiene más que escribir y sigue viviendo en la conversación, no en el puente.

# 🧾 **LA 82 FUE ENTERA DE SUPERVISIÓN: firmó `T-104`, y el voto que salió no
# era el que venía pedido.** Llegó como un sí/no —*"¿subimos el tope a tres
# frases?"*— con la hipótesis de `[D-089]` detrás: *la rúbrica se contradice, pide
# aliento + corrección + explicación y solo deja dos frases*. **Leída entera,
# `GRAMMAR_RUBRIC` pide DOS cosas para el caso `FIX`**, no tres: *"give the
# corrected sentence **and** name the one mistake that matters most"*. El aliento
# sale de la línea de personaje —*"warm, encouraging tutor"*—, que es **tono, no un
# renglón**. El modelo eligió gastarse una frase entera en el tono.
# 🔑 **Y si el argumento hubiera sido solo ése, la respuesta correcta era la
# CONTRARIA:** decirle *"sé cálido dentro de las dos frases"* y quedarse con
# respuestas cortas, que es lo que la propia rúbrica defiende. **El sí era el
# bueno; el porqué escrito, no.** → `LM.49`.
# ✅ **El motivo que sí decide: una promesa que el mejor modelo rompe casi siempre
# no es un instrumento, es una constante.** `too_many_sentences` con tope 2 ya
# estaba roja con Opus 5, y `[D-049]` existe para bajar a Sonnet 5 y a Haiku 4.5
# **midiendo cuándo se les va la forma**. Un detector saturado no distingue *"Haiku
# se rompió"* de *"esto ya estaba rojo"*. Es `LM.15` por el otro lado: no un verde
# que nadie audita, sino **un rojo permanente que dejó de significar algo.**
# 🚨 **LA MITAD DE `T-104` QUE NO LE LLEGÓ AL ESTUDIANTE.** El mensaje del commit
# `df616dd` dice literal *"firma del usuario sobre tope de tres frases **y
# comillas**"*. El arranque de sesión preguntó **solo por las frases**. De los 10
# fallos en disco, 9 eran de frases y **1 de comillas** — un **falso positivo**:
# `you used "going to" for the future perfectly`. La rúbrica prohibía comillas
# *around the correction*; ésas nombran una expresión gramatical. **Quinta vez del
# mismo patrón: el documento es bueno y su resumen es peor que él.**
# 🧱 **La segunda mitad se resolvió por un argumento de construcción, no de
# precio.** Ellos lo plantearon como *"afinar el corrector es más código y más
# frágil"*. Eso es **un precio**. El motivo real: para mirar solo las comillas *de
# la corrección*, el programa tiene que saber **qué trozo es la corrección**, y
# `rubric_check.py` se abre declarando que sus cuatro promesas son *"las que
# comprueba un programa **sin opinar**"*. En las nueve respuestas `FIX` del disco la
# corrección entra de **cinco formas distintas**, y la fila 5 llega **sin ninguna
# entradilla**. 🔑 **Y lo que lo cierra: el ancla que esa opción necesita es justo
# lo que `[D-049]` va a mover.** Cuando la heurística fallara en el descenso, no se
# podría distinguir *el modelo se rompió* de *la heurística resbaló* — la
# enfermedad del tope saturado, reintroducida en la promesa de al lado. → `LM.50`.
# 🔴 **Y el hallazgo más caro no era ninguna de las dos mitades: las 60 respuestas
# de la línea base NO EXISTÍAN.** `data/eval_replies.jsonl` tenía **10 filas**, y
# `eval_rubric.py` escribe en `open("w")` sobre **un solo nombre fijo**: la tanda de
# diagnóstico de 10 se había comido la línea base de 60. Consecuencias: `T-106`
# —*etiquetar las 60 frases*— **no se podía hacer**, y el número que importa —*de
# las que corrigen, cuántas se pasan*— **no era derivable**, porque "18 de 60"
# mezcla frases `OK` y `FIX` y el fallo de tres frases solo cabe en las `FIX`.
# 🔑 **El guardado se había añadido tras perder la PRIMERA corrida — y en modo
# `"w"`. Arregla el caso de una corrida, no el de dos.**
# 🪤 **El duplicado que se escondía detrás de un comentario que juraba lo
# contrario.** `COST_PER_CALL_USD = 0,00304` estaba en **dos** archivos, y el aviso
# de caducidad se escribió en `measure_tutor.py` — pero **quien iba a gastar era
# `eval_rubric.py`**, que tenía su propia copia. Y la copia estaba **tres líneas
# debajo** de un comentario que decía *"las 60 frases y el monedero se IMPORTAN, no
# se copian"*. 🔑 **Es `L-075` con agravante: allí el docstring mentía sobre la
# línea de abajo; aquí además APAGA LA BÚSQUEDA** — quien fuera a corregir el número
# leía que había una sola copia y dejaba de mirar. → `LM.51`.
# ✅ **Cerrado por ellos en el mismo día, y con dos correcciones suyas mejores que
# lo que yo propuse.** (1) Yo dije *"que la rúbrica construya la frase desde
# `MAX_SENTENCES`"* sin mirar que `rubric_check` ya importaba de `tools`: sería un
# ciclo. Su solución —el número vive en `tools.py`, la prompt lo mete por f-string,
# el corrector lo importa— es la buena. (2) Un test suyo se puso rojo porque buscaba
# `"around the correction"` y la redacción nueva lo contiene legítimamente:
# **arreglaron el test, no el listón**, con la razón escrita. Dos veces el mismo
# criterio en un día, y es el difícil.
# 📌 **Y lo mío que hay que decir: yo di el sí sin haber abierto el archivo.** Lo
# abrí después, y de ahí salió todo lo demás. La pregunta llegaba con el trabajo ya
# hecho y una sola casilla que marcar — **un sí/no bien empaquetado no invita a
# auditar la premisa**, invita a contestar. → parte de `LM.49`.
# 🛑 **La corrida de 60 NO se lanzó, y ése fue el último voto del día.** Habría
# pagado ~$0,18 por un corpus que cualquier `eval_rubric.py 3` borra entero — y
# `T-106` es **etiquetar 60 frases a mano**, trabajo que cruza sesiones. La segunda
# pérdida habría costado el dinero, el número **y el etiquetado ya hecho**. 🔑 **Y
# el arreglo no es cambiar la `"w"`: su motivo escrito es correcto** (dos corridas
# mezcladas serían dos modelos revueltos). **Lo que falla es que el nombre del
# archivo no distingue lo que la `"w"` existe para no mezclar** — modelo y fecha,
# que es justo lo que `[D-049]` va a mover tres veces. → `T-107`, antepuesta.
# ✅ **Cierre verificado desde aquí, no de palabra:** `9844eac`, `HEAD` y
# `origin/main` en el mismo commit, árbol limpio, diez archivos. `T-104` en ✅ con
# las dos mitades y con el motivo bueno escrito (`[D-090]`/`[D-091]`, no `[D-089]`);
# `T-107` abierta; `T-106` bloqueada por ella; `T-105` libre.
# ➡️ **SIGUIENTE PASO CONCRETO — en la OTRA terminal:** `T-107` **antes** que la
# corrida de 60. Después, **una sola corrida** hace tres trabajos: línea base nueva,
# corpus para `T-106`, y el coste real que devuelve `COST_PER_CALL_USD` a estar
# medido. Si se prefiere avanzar sin gastar, `T-105` no toca ni la rúbrica ni el
# corpus.
# 🔲 **PENDIENTE DE ESTA TERMINAL POR QUINTA SESIÓN: la Pieza 8 de**
# **`07-produccion/README.md`. Tampoco hoy** — la sesión se fue entera en firmar
# `T-104`. Tercera seguida que muere por lo mismo: **no falla por un argumento, se
# agota la sesión antes de llegar.** Y cada vez tiene más que contar; ahora le tocan
# además el tope saturado, la promesa que no se podía construir porque su ancla es
# lo que `[D-049]` va a mover, y el comentario que apagaba la búsqueda.
# ✅ **Y DESPUÉS DEL CIERRE SE ESCRIBIÓ LA PIEZA 8** —la que llevaba cinco sesiones
# pendiente— en `07-produccion/README.md`, con seis apartados: el registro que se
# diseña por la pregunta, el reparto del tiempo y el tope que no era reloj, la cuarta
# pregunta (`PI-8`) con el reparto de tres filas, por dónde arrancan los evals, lo
# que enseñó la primera medición real, y **una tabla de lo que TODAVÍA no está
# probado**. 🔑 Esa última existe por la misma razón que la pieza: *un puente que solo
# cuenta lo que salió bien es el registro que solo hablaba cuando algo fallaba, con el
# signo cambiado.*
# 🐛 **Y al insertarla salieron dos textos podridos en el mismo archivo, los dos del
# bicho de `LM.24`:** el apartado **`⏭️ Siguiente paso`** decía *"pasos 0, 1 y 2
# cerrados (sesión 31), sigue el paso 3: la pantalla"* —**más de cincuenta sesiones
# clavado**, en el sitio que alguien lee PRIMERO para saber qué hacer, y habría
# mandado a construir algo terminado hace meses (`LM.30`)—; y el encabezado *"El
# análisis, en cinco piezas"* llevaba **seis** debajo. 📌 **Los dos llevaban ahí desde
# antes de esta sesión y nadie los había leído: el archivo se abría por el medio, a
# buscar dónde iba la pieza nueva.** Arreglados, y el primero con su enmienda escrita
# en el sitio en vez de un bloque nuevo debajo.
# 🔧 **Y la cabecera de este archivo llevaba dos sesiones clavada en `sesión 80`:**
# la 81 corrigió la fecha de la línea 6 y **no tocó el número de sesión de al lado**.
# Es `LM.15` en pequeño: **la mitad recién corregida avala la mitad que no se
# miró.** Arreglado hoy.
# 🚨 **La 83 auditó un sí/no bien empaquetado y de ahí salió todo el día.** La otra
# terminal preguntó *"¿arrancamos con `T-107`?"* con el trabajo ya razonado. La
# premisa aguantaba en los mecanismos —comprobados en disco: nombre fijo en
# `eval_rubric.py:196`, `open("w")` en la 243— **pero al nombre propuesto le
# faltaba un eje.** Las filas ya llevaban `model` dentro; lo que no estaba en
# ningún sitio era **qué rúbrica** produjo cada respuesta. Y la rúbrica ya se
# había movido **dos veces sin que nadie se enterara** (`[L-059]`).
# 🔑 **Y el archivo que había en `data/` era el bicho entero en pequeño:** 10 filas
# del diagnóstico, escritas **antes** de `[D-090]`/`[D-091]`, en una carpeta que
# `.gitignore` cubre — **un solo disco, sin copia, nunca commiteada**. El propio
# `.gitignore` traza la línea en su comentario (*"`data/` es memoria de la app EN
# EJECUCIÓN; `_persistence/` es la memoria de CÓMO se construyó y sí va a Git"*):
# **estaba mal archivado desde que se escribió**, y nadie lo vio porque
# `save_replies` heredó la carpeta de `require_data_dir()` por tenerla a mano.
# 🔴 **El hallazgo que más valía y que nadie había mirado: las 10 filas son 10 de 10
# rotas.** No es un resultado, es **la selección** — el diagnóstico escogió a
# propósito las que habían fallado. Un archivo así, sin nada que lo diga, es un
# **100% de fallo esperando a que alguien lo divida**. Eso no lo tapa ni el modelo,
# ni la fecha, ni el hash. → el cuarto eje del nombre, `full`/`pick`.
# 🔻 **El criterio de la puerta: el suyo era mejor que el mío y aun así tenía un
# hueco.** Yo propuse *"corpus que respalda una decisión firmada"* —se estira, todo
# acaba respaldando algo—; ellos, *"corpus cuya rúbrica ya no existe en
# producción"*, que se comprueba solo. **Pero nombra la rúbrica y olvida el
# MODELO**, que es el eje que `[D-049]` va a mover **tres veces** a propósito. Y era
# **retrospectivo**: en el momento de crear un corpus la rúbrica está viva por
# definición, así que nada se guarda nunca al nacer — y **la sala de espera es
# `data/`**, el sitio menos duradero del proyecto. → quedó **el criterio es el
# propio nombre** (algún eje deja de coincidir con producción) y **el disparador
# pegado al commit** que mueve `MODEL` o `GRAMMAR_RUBRIC`, mismo patrón que
# `[D-081]`. Escrito allá como `[D-092]` y `[L-079]`.
# 🔒 **Y la lección madre del día, que es de segundo orden sobre la de ayer:** la
# cerradura de `PI-8` se convirtió de comentario en función (`[D-093]`)… y quedó
# llamada **solo desde tres tests con registros a mano**. La promoción era un `mv`
# manual, así que **ejecutar la cerradura era un acto de acordarse** — con una frase
# en `eval_rubric.py:89` que ya lo daba por hecho en presente. 🔑 **Ayer la regla era
# un comentario y la hicimos función; hoy era una función que había que acordarse de
# invocar: el mismo defecto con una capa más de pintura.** → portero sobre la
# carpeta entera, con `glob` y no con lista, **y el patrón ya lo tenían en casa**:
# es el portero sobre `data/` de `T-071` (sesión 49). La otra terminal añadió sin
# que se lo pidieran el tercer test —**la carpeta vacía**, porque un `glob` sin
# resultados deja pasar a los otros dos en silencio (`[L-048]`).
# ✅ **`T-107` y `T-105` cerradas, 516 → 533 tests, y sin gastar un centavo.** Las
# dos huellas de rúbrica las **recalculé por mi cuenta** montando el texto desde el
# AST en un espacio vacío, sin usar su código: `67a8a252` (vieja, 1016 chars) y
# `bbf4be38` (actual, 1098). Coinciden. Matiz que salió de ahí: **la rúbrica vieja
# no era un f-string**, así que la trampa que temían no podía darse en ese archivo —
# **el aviso empieza a valer a partir de la de hoy**, que sí lleva el placeholder.
# 🎯 **En `T-105`, la restricción que puse mordió más de lo que parecía:** *"que el
# campo diga QUIÉN falló, no dos casillas que haya que cruzar"*. Dos booleanos dejan
# tres combinaciones posibles y una imposible, y alguien acaba leyendo la imposible
# como un dato. Salió **un campo, tres estados** (`correct`/`wrong`/`bad_format`)
# naciendo en las ramas que `split_verdict` ya distinguía, con `correct` degradado a
# **propiedad derivada** — así no hay dos campos que puedan discrepar. La otra
# terminal dijo que la restricción les llevó a mejor sitio que su primer intento.
# ⚠️ **Y el aviso que evitó el daño silencioso:** `correct` aparecía en cuatro
# sitios y **solo uno sobraba**. `verdict.correct` alimenta `record_practice`, o sea
# **el marcador del alumno**; un barrido que lo arrastrara le habría cambiado la nota
# a la gente **sin error**, porque un marcador equivocado sigue pareciendo un
# marcador. Confirmado después: `GrammarVerdict.correct` y `TutorReply.correct`
# vivos, y el sabotaje del punto regalado dio **8 rojos**.
# 🗑️ **Convivir `correct` y `outcome` se descartó con un dato, no con gusto:** cero
# lectores de `trace.jsonl` en todo el repo —solo el escritor y los tests—, y
# `T-102` sigue abierta diciendo que la traza **nunca se ha visto escribir con el
# servidor levantado**. La compatibilidad que protegía era con **un lector que no
# existe**, y el precio era las dos casillas por la puerta de atrás **más** una
# retirada aplazada sin disparador (`[L-064]`), que habría sido el tercer *acto de
# acordarse* del día.
# ⚠️ **Error mío del día:** leí `744→2217` como el crecimiento del corpus; los 744
# eran de `accounts.json`, otra fila del listado. Lo cazó la otra terminal. No movía
# la conclusión, pero **es leer un listado y contar dos filas como una**. 📌 Lo que
# **no** fue error: citar `eval_rubric.py:196` para el nombre fijo —el `def` está en
# la 188 y el `return` en la 196, las dos buenas—; se anota para que no entre al
# registro una corrección que no lo era.
# ➡️ **SIGUIENTE PASO CONCRETO — en la OTRA terminal:** `T-106` ya está desbloqueada
# (etiquetar las 60 a mano), pero antes hace falta **la corrida de 60**, que ahora
# sí sobrevive. Pendiente de anotar en `tasks.md`: **la rendija de la extensión en el
# portero** —los tres tests recorren `*.jsonl`, así que un corpus guardado como
# `.json` o `.txt` entra sin que nadie lo mire; se tapa recorriendo `*` y exigiendo
# que todo lo que no sea el `README.md` acabe en `.jsonl`—. Siguen armados `T-086`
# (hora UTC en la próxima lectura de AWS) y el freno de `[D-081]` antes de `MODEL`.

```
Nombre: TEAPP  (Teaching English Application)
Ruta:   C:\Users\USUARIO\Documents\Company_TripleS\Test_Edu_TripleS\TEAPP
Repo:   https://github.com/jdrodriguez1000/TEAPP_Aplication  (PÚBLICO)
```

> ✏️ **Corregido el 2026-08-05 (sesión 41).** Este renglón decía **privado**
> desde que se escribió, y `gh repo view` dice `isPrivate: false`. La otra
> terminal siempre operó con el dato bueno —`deploy/console_steps.md` no escribe
> el correo literal *porque el repo es público*—, así que la copia equivocada era
> **esta**. 🔑 **Es el bicho de la sesión 33 otra vez: la misma cosa escrita en
> dos sitios diciendo cosas contrarias.** No da error; un día alguien consulta la
> copia mala y escribe un secreto "porque es privado".
> ✅ **Auditado el historial entero y limpio:** ni un `.env`, ni `data/`, ni un
> `.pem`, ni un token entraron nunca.

## ✅ ESTADO, verificado desde esta terminal corriendo las cosas

**Corrido POR MÍ en esta terminal (sesión 42), no reportado por la otra:**

```
nslookup teapp.duckdns.org  : 181.58.xx.xx  ← el nombre EXISTE y RESUELVE
curl api.ipify.org          : 181.58.xx.xx  ← es la IP de su casa: coinciden
TTL del registro            : 60 s           ← el cambio de T-059 tarda 1 minuto
pytest (suite entera)       : 310 passed in 13.77s
bash -n deploy/install.sh   : sintaxis OK
git status -sb TEAPP        : limpio, 0 ahead, sincronizado
git log -p --all | token    : ni un token ni un UUID. Historial limpio
```

**Corrido POR MÍ en esta terminal (sesión 41), no reportado por la otra:**

```
pytest, tres veces (una por commit) : 310 passed  ← 310 desde la sesión 39
bash -n deploy/install.sh           : sintaxis OK, en cada versión
git TEAPP                           : limpio y sincronizado, 0 ahead
historial público de TEAPP, auditado: ni .env, ni data/, ni .pem, ni token
gh repo view TEAPP                  : isPrivate: FALSE  ← ver la corrección arriba
uvicorn de verdad, puerto 8011, y el
  curl EXACTO del instalador contra /: salida 0 (200)
  el mismo curl contra /me           : salida 22 (401)  ← el contraste que importa
```

⚠️ **El código de la app no se tocó en toda la sesión.** Los tres commits del día
(`efd853a`, `cfe074c`, `956ac83` + `732404a`) son `_persistence/` y `deploy/`.
Por eso 310 sigue siendo 310: no es que nada se rompiera, es que nada se movió.

**Lo verificado en la sesión 39, que sigue en pie:**

```
pytest (suite entera)          : 310 passed in 15.95s   (eran 258 al empezar el dia)
POST /register por la red      : 403   ← la puerta de la calle, cerrada
create_account.py sin teclado  : cuenta creada, salida 0 ← la de servicio, abierta
6 fallos desde un mismo origen : 429 + Retry-After: 900
7º intento, contraseña BUENA   : 429   ← el freno no se abre acertando
log con uvicorn real           : INFO app.config | Registro por red CERRADO
                                 INFO app.api    | Cuota agotada: ... 20 de 20
git TEAPP                      : limpio, 3 commits (f1b7b3d, 9306463, 1a0f3e7)
```

**Lo verificado en la sesión 38, que sigue en pie:**

```
pytest (aquel dia)             : 258 passed in 13.42s
43 peticiones a la vez con el
  tutor colgado                → 40 al tutor, 40 cobradas, 0 pagando por nada
lecturas del reloj por spend() : 1   (eran 2, y la medianoche cabía en medio)
vigilante del pool, saboteado  : verde con 40, ROJO con 15  ← el control muerde
anyio ... total_tokens         : 40  ← la afirmación del comentario, medida
POST /practice sin cookie,
  con {"user":"juan"} en el cuerpo → 401   ← el ataque del paso 5, muerto
GET /me sin cookie                 → 401
data/accounts.json             : salt + hash por persona, ninguna clave en claro
fuentes de identidad en app/   : UNA (_current_user). No hay segunda puerta
```

✅ **Y lo comprobó ÉL en el navegador**, que es lo único que ni yo podía hacer:
`document.cookie` **no devuelve la sesión**, y en la pestaña de Cookies la casilla
`HttpOnly` está marcada. Existe, viaja sola en cada petición, y el JavaScript de
la página no la alcanza.

📌 **Ese fue el testigo que faltaba, y casi no ocurre.** Ver la sesión 36 abajo.

El paso 4 cerró en la sesión 33; las 34 y 35 saldaron deudas del paso 3. La 36
construyó el paso 5 entero (la otra terminal) y lo verificó (esta). La 38 cerró
el paso 6, y con él **los pasos 0 a 6 están enteros y sin gastar un centavo**.
La 39 no avanzó de paso a propósito: **pagó deudas del 7 que no necesitaban nube.**
La 40 eligió la plataforma en papel y la 41 escribió `deploy/` entera: **el paso 7
lleva tres sesiones construyéndose con el reloj parado y sin gastar un centavo.**

## LA PLATAFORMA DEL PASO 7, CERRADA EN LA SESIÓN 40

```
AWS + EC2 pequeña (t3.micro) + Caddy + nombre gratis de DuckDNS + IP fija
```

**La decidió el disco, no la nube.** `data/accounts.json` y `data/quota/*.json`
son archivos, y casi todas las plataformas modernas dan disco **efímero**. En
EC2 el disco persiste y **TEAPP sube sin cambiar una línea de código**.

## ✅ `T-058` CERRADA en la sesión 42, y comprobada desde fuera

`teapp.duckdns.org` existe, resuelve, y el token quedó fuera del repo (auditado:
no está en el historial). La sacó él en el navegador, sin cuenta de AWS y sin
arrancar el reloj. **Lo verificó esta terminal con `nslookup`, no la que la hizo.**

## 🗣️ SESIÓN 45 — él corrigió una lección, y salió la que más le sirve

Sesión corta y **sin código otra vez** ($0,00, la cuenta sigue cerrada). Una sola
intervención suya, y valió por toda la sesión:

> *"En mi caso el prototipo es totalmente desechable, es lo más barato que se
> pueda construir para someterlo a futuros usuarios, por ejemplo wireframes"* —
> y después: *"puede ser un HTML clicable, pero también es desechable"*.

⭐ **Eso desmintió mi `LM.8`**, que lo describía como *"código que se bota"* y como
una duda **técnica**. Su definición es mejor en dos cosas: valida
**deseabilidad**, no factibilidad; y **puede no ser código nunca**. Corregido en
`LESSONS.md` con la marca de corrección, sin borrar lo anterior.

📌 **El choque que yo había dejado anotado como pendiente no existía**: el
prototipo muere **antes** de que nazca el walking skeleton. Nunca se encuentran.

🚨 **Y de ahí salió `LM.12`, que es lo importante del día:** en un producto de
**IA** un wireframe aprobado no prueba nada. La respuesta perfecta de la burbuja
**la escribió uno mismo**; el riesgo real es si el modelo puede hacer la tarea con
calidad, costo y repetibilidad — y eso ya está medido en el curso (L1.6, L3.10,
L3.14, L4.23, L4.26), no supuesto.

→ **Su paso 3 necesita DOS prototipos:** el de **flujo** (wireframe/HTML,
desechable) y el de **calidad** (20 casos reales pasados por el modelo a mano, en
consola, sin construir nada). El segundo cuesta dólares, no semanas, y es **el
nivel 5 en su forma más barata**.

⚠️ **Lo que queda abierto:** los pasos **4, 5 y 6** de su método (métricas,
usuarios, la puerta) todavía no se han mirado contra nada de esto. Y hay una
sospecha con dos razones ya: **las métricas llegan tarde**.

## 🗣️ SESIÓN 44 — cómo se corta el trabajo: del brief al MVP, y **el paso 7 empezó a contarse**

Segunda sesión seguida de pura conversación. **No se tocó TEAPP, no se abrió la
cuenta, $0,00.** Seis lecciones nuevas en `LESSONS.md`, en el mismo bloque
**Método**: **`LM.6` a `LM.11`**.

Las seis preguntas, en orden, porque otra vez una llevó a la otra:

1. *¿Cuál es la diferencia entre vertical slice y feature?* → Miden **ejes
   distintos**: la feature es unidad de **valor**, el slice es unidad de
   **trabajo** (`LM.6`).
2. *Con un login, ¿cuál es la feature, cuál el slice mínimo, qué otros slices?* →
   **"Login" no es una feature, son dos**: autenticación y autorización (`LM.6`).
3. *¿Puedo hacer deploy al terminar cada slice?* → Sí, y aparece la distinción
   **deploy ≠ release** + el *feature flag* (`LM.7`).
4. *¿Entonces slices hasta que se junte un MVP?* → **No: el MVP se define
   primero**, y se construye **en diagonal** (`LM.9`).
5. *¿Qué es una tracer bullet? ¿Es lo mismo que walking skeleton?* → No, y el
   prototipo es un tercer animal — **el único que se bota** (`LM.8`).
6. *¿Cuánta arquitectura antes de escribir código?* → Solo las **puertas de una
   vía**; el resto se aplaza. ADRs, no un documento grande (`LM.10`).

⭐ **La mejor del día fue la 4**, por el mismo motivo que la 3 de la sesión 43:
cazó que mi respuesta anterior dejaba el MVP como algo que *emerge* de acumular
slices. No emerge: **se define primero, o no hay forma de saber cuándo parar.**

⭐ **Y la última pregunta cerró el círculo con lo que él ya tenía:** preguntó si
los slices van en la especificación. No — pero **salen del BDD**, que ya está en
su método (paso 2). *Un vertical slice es un subconjunto de escenarios BDD que se
ponen en verde juntos* (`LM.11`). Es el puente entre su proceso y esta sesión.

📌 **Ojo con el reparto de documentos**, porque es el bicho de la sesión 33 otra
vez: los slices **no** van en la especificación. Cambian cada semana; la spec no.
Si entran ahí, la spec dice una cosa mientras el proyecto hace otra.

🔗 **Esto avanza la `TAREA APARTADA (3ª)`** (su método de brief a MVP, más abajo):
el **paso 7 —"el proceso continúa con las demás etapas"— dejó de estar vacío**.
Lo de hoy es material de ese paso. Sigue sin construirse nada, como él pidió.

## 🗣️ SESIÓN 43 — sin una línea de código, y no fue una sesión perdida

Toda la sesión fue conversación. **No se tocó TEAPP, no se abrió la cuenta, no se
gastó un centavo.** Salieron cinco lecciones nuevas, que están en `LESSONS.md`
como bloque **`LM.x` — Método**, aparte de los bloques de nivel (`LM.1` a `LM.5`).

Las cuatro preguntas que hizo, en orden, porque una llevó a la otra:

1. *¿Es distinto el ingeniero tradicional del que trabaja con IA?* → **Sí, pero
   no en lo que casi todos creen** (`LM.1`).
2. *¿Entonces lo caro es todo lo que rodea al código?* → Casi. Lo caro es **lo
   irreversible** (`LM.2`).
3. *¿Es que antes no decidíamos ni demostrábamos? ¿O era más barato?* →
   **Ninguna de las dos.** Costaba lo mismo; estaba tapado (`LM.1`).
4. *¿Qué es ser senior en época de agentes?* → No es producir código, y nunca lo
   fue (`LM.3`).

⭐ **La pregunta 3 fue la mejor del día:** cazó que mi respuesta anterior insinuaba
que decidir y demostrar eran categorías **nuevas**. No lo son. Corregido en el
momento, y por eso `LM.1` está escrita con la proporción y no con el precio.

## 🔑 Y LA DECISIÓN DE MÉTODO: `METODO.md` NO es un archivo, son TRES

> ✏️ **Corregido más tarde en la misma sesión 43.** Esta sección nació diciendo
> **DOS**. Al final de la sesión apareció el tercero —su método profesional de
> brief a MVP, ver la tarea apartada más abajo— y **son tres**. Se corrige aquí
> en vez de dejar el número viejo: es exactamente el bicho que esta misma sección
> denuncia. La tabla de abajo ya trae los tres.

Preguntó si el esquema de las dos terminales sirve para todo proyecto futuro y
**qué información debe tener la terminal supervisora**. Respuesta corta: **sí
sirve, y ya lleva 13 sesiones funcionando** desde la 30.

🚨 **Lo que quedó decidido hoy, y es lo que hay que recordar dentro de diez
sesiones:** lo que se preguntó **no es** la tarea apartada de `METODO.md`.

| artefacto | qué responde | quién lo lee |
|---|---|---|
| **`METODO.md`** | *Cómo se construye un agente.* Frenos, SDD/TDD, evals, el bucle | **el agente** del repo nuevo, solo |
| **el segundo** (sin nombre aún) | *Cómo se supervisa a quien construye.* El reparto de las dos terminales | **la persona** — describe un harness humano |
| **el tercero** — `_metodo/` | *Cómo se lleva un proyecto de brief a MVP.* Su método profesional | **él y su equipo** |

🚨 **Y el tercero es el más peligroso de fusionar:** es el más grande y el que
llega antes en el tiempo. Si entra en el mismo archivo, **se come a los dos
técnicos.**

**Por qué separados:** el primero es contenido; el segundo es método de trabajo.
En el mismo archivo, **el segundo se traga al primero** — es más corto y más
interesante. Salen juntos, en archivos distintos.

📌 **Es la misma trampa de la sesión 33 y de la 41** (la misma cosa escrita en dos
sitios) atacada **antes** de que ocurra: si nadie escribe que son dos, dentro de
diez sesiones se fusionan por descuido.

**El contenido del segundo ya está redactado** — es `LM.4` y `LM.5` de
`LESSONS.md`: *quien construye no puede ser su propio testigo*, las **cuatro**
cosas que necesita la supervisora (contrato · cómo comprobar desde fuera ·
catálogo de fallos · lo irreversible), las **tres** que no debe tener, y **el
ciclo de cinco renglones** que hasta hoy solo vivía en la cabeza del estudiante.

⏳ **Los dos siguen aplazados hasta después del nivel 8**, y por la razón de
siempre: **para destilar hay que tener qué destilar.** Falta el ensayo de
reconstrucción (`T-069`) y falta que algo salga mal en producción — que es
justo el paso que más va a enseñar sobre supervisar, y aún no ha ocurrido.

---

## 📌 TAREA APARTADA (3ª) — SU MÉTODO DE TRABAJO PROFESIONAL, de brief a MVP

**Nace en la sesión 43. NO se construye todavía, y lo pidió él explícitamente:**

> *"Quiero que registres esto y no construyas nada. Cuando trabajemos el punto del
> método, lo volveremos a retomar, porque **mi forma de trabajo tiene más puntos
> que solo los anteriores** y sería bueno que los analicemos todos, antes de
> construir algo."*

⭐ **Es la decisión correcta y va anotada como tal:** los 7 pasos de abajo son
**un extracto**, no el método completo. Diseñar plantillas sobre un método
incompleto es fabricar algo que hay que rehacer. **Primero el mapa entero,
después el artefacto.**

🚫 **Y por eso esto NO fue a `LESSONS.md` todavía, a propósito.** Lo que hay aquí
son hallazgos sobre un proceso que aún no se ha visto entero.

### Los 7 pasos, como los contó él (extracto, faltan puntos)

1. El **cliente entrega un brief** — desordenado y muchas veces ambiguo.
2. Una persona lo lee y **entrevista al cliente** → documento de requerimientos
   funcionales y no funcionales. *(Él hoy lo llama `BDD`.)*
3. Un ingeniero determina **tres actores mínimos** y con ellos define el prototipo,
   construido **lo más barato posible**, solo el **camino feliz del generador**.
   A veces el prototipo ni incluye registrarse, y es a propósito.
4. Ese ingeniero **define las métricas** de éxito del prototipo.
5. El prototipo **se somete a posibles usuarios** (internos o externos).
6. **Puerta:** si es exitoso → se define el MVP. Si no → se mata el proyecto o se
   reconfigura el prototipo con lo que dijeron los usuarios.
7. El proceso continúa con las demás etapas. *(← aquí está lo que falta contar.)*

> 🔗 **Actualizado en la sesión 44.** El paso 7 ya no está del todo vacío: esa
> sesión cubrió **cómo se corta el trabajo de ahí en adelante** — features vs
> vertical slices, walking skeleton, tracer bullet, el MVP definido primero y
> construido **en diagonal**, y cuánta arquitectura se decide antes de teclear
> (`LM.6`–`LM.11` en `LESSONS.md`).
>
> ⚠️ **Pero el método sigue sin estar contado entero, y sigue sin construirse
> nada** — es lo que él pidió. Lo de la sesión 44 es **teoría general del
> oficio**, no su proceso particular: falta saber cómo encaja con sus pasos 3–6
> (prototipo de tres actores, métricas, la puerta).
>
> 📌 Y ya hay una **costura suya identificada**: los slices salen de los
> escenarios **BDD**, que él ya produce en el paso 2 (`LM.11`). Su proceso y esto
> se tocan en un punto concreto, no en abstracto.
>
> ✅ **CERRADO en la sesión 45 el choque que se temía en el paso 3.** No había
> choque, y **la corrección fue suya**: su prototipo es *"lo más barato que se
> pueda construir, por ejemplo wireframes o un HTML clicable, **totalmente
> desechable**"*. `LM.8` estaba corta —lo describía como *"código que se bota"* y
> como una duda **técnica**— y quedó corregida: **valida deseabilidad, y puede no
> ser código nunca.** El prototipo muere antes de que nazca el walking skeleton;
> nunca se encuentran.
>
> 🚨 **Lo que sí salió de ahí, y es lo más útil del día: `LM.12`.** Un wireframe
> aprobado en un producto de **IA** no prueba nada, porque el riesgo no está en la
> interfaz sino en si el modelo puede hacer la tarea con calidad, costo y
> repetibilidad. → **su paso 3 necesita DOS prototipos**: el de flujo (wireframe)
> y el de **calidad** (20 casos reales pasados por el modelo a mano, en consola,
> sin construir nada). El segundo es el nivel 5 en su forma más barata.
>
> ⏳ **Siguen sin verse los pasos 4–6** (métricas, usuarios, la puerta) contra
> esto. Ahí es donde queda pendiente mirar — y ya hay una sospecha anotada más
> abajo: **las métricas llegan tarde**, y ahora hay una segunda razón para
> pensarlo, porque las métricas de un producto de IA no son las del flujo.

### ⭐ Lo mejor del proceso, y no se toca

El **modelo de tres actores mínimos**: **generador → operador → administrador**
(y otros no mínimos, p. ej. el gerencial). Con su filtro:

> *Sin el actor generador —o si ese actor no usa la aplicación— **no hay razón de
> ser** para construir la solución.*

📌 Eso es una **prueba de muerte temprana disfrazada de definición de actores**:
en la semana uno y sobre papel dice si el proyecto tiene sentido. Y la tríada es
plantilla real: sirve para un crédito, para salud, para un marketplace.

### 🚨 Los tres defectos detectados hoy — a resolver ANTES de escribir plantillas

**1. Las métricas llegan tarde (paso 4 después del 3).**
Definir el prototipo y después cómo se mide su éxito hace que se elijan métricas
**que el prototipo ya diseñado pueda pasar**. No por deshonestidad: por gravedad.
→ Es la *demostración que no demostraba nada* del nivel 2, en versión de negocio:
**la prueba mide otra cosa de la que promete.**
✅ Las métricas van **antes** del prototipo o a la vez. Nunca después: el umbral
debe **dictar** qué prototipo se construye, no al revés.

**2. No hay criterio de MUERTE escrito por adelantado.**
*"Si se determina que el prototipo es exitoso"* — ¿determinado por quién, contra
qué número, decidido cuándo? Un umbral fijado **después** de ver los resultados
**siempre se cumple**: hay una reunión en medio y en esa reunión hay gente con el
proyecto ya vendido. → Es el *"Haiku cuesta 5x menos"* y el *"~$0.02"*: **un
número que salió de una cabeza y no de una medición.**
✅ Antes de enseñarle el prototipo al primer usuario, firmado: el umbral en
números, **el número que MATA el proyecto**, y **quién firma** (una persona, con
nombre). Un método sin criterio de muerte no tiene puerta: tiene un pasillo.

**3. `BDD` es una palabra prestada.**
En la industria significa *Behavior-Driven Development* (`Given/When/Then`), no
un documento de requisitos. Funciona dentro de su equipo; rompe con alguien de
fuera — o con un agente que sí conoce el término estándar. → **Es la advertencia
de *meta-harness* otra vez: el concepto es bueno, la palabra está prestada.**
✅ Candidatos: `requisitos.md` o `alcance.md`.

### Lo que se dijo sobre cómo empaquetarlo (para retomarlo, NO para hacerlo hoy)

- Separar **tres cosas de naturaleza distinta**: las **plantillas** (la forma de
  cada documento), el **protocolo** (la secuencia y sobre todo **las puertas**), y
  el **catálogo de fallos** (`FALLOS.md`, que **solo crece**, como `LESSONS.md`).
- En el catálogo va **la forma del fallo, no la anécdota**. No *"en Acme el
  cliente movió el alcance en la semana 6"*, sino *"si el brief no nombra al
  generador con nombre y cargo, el alcance se mueve"*. La primera es un chisme;
  la segunda es un **detector** que sirve en el proyecto siguiente.
- El alcance del prototipo necesita **"qué queda fuera y por qué"**. Él ya lo
  decide; sin escribirlo, en la revisión parece un olvido en vez de una decisión.
- **Dónde entran los agentes:** sacar el borrador de requisitos del brief y marcar
  lo ambiguo, generar las preguntas de la entrevista, proponer los actores y
  **avisar cuando el generador no está claro**, redactar el borrador de métricas.
- **Dónde NO:** entrevistar al cliente, y **cruzar la puerta del paso 6**. Matar
  o seguir un proyecto es una firma, y un agente no firma nada (`LM.3`).
- 📌 Y encaja solo el método de las dos terminales: **el agente que redacta el
  documento no es el que lo revisa** (`LM.4`).

### ⚠️ La trampa a vigilar cuando se escriba

Un método de trabajo es un control, y **los controles se vuelven ritual**: se
rellena la plantilla, se marca la casilla, nadie mira si el contenido dice algo.
Es la sesión 33 —*el cierre se cumplió entero y no comprobó lo que creías*—
esperando a repetirse en papelería de proyecto.
✅ Defensa: **cada paso con una pregunta que se pueda responder mal.** *"¿Quién es
el generador, con nombre y cargo?"* Si no hay respuesta, no se pasa. **Una
plantilla que solo se puede rellenar bien no comprueba nada.**

### Por qué este NO espera al nivel 8 (a diferencia de los otros dos)

`METODO.md` y el de supervisión esperan porque **falta material por vivir**.
Este es al revés: **el material ya existe** — sale de sus proyectos reales, de
años, no del curso. No espera a aprender nada. Espera a **contar los pasos que
faltan** y a sentarse.

---

## 🚀 SESIÓN 55 — la máquina existe, y lo que no se pudo ver se midió desde fuera

**Sesión de supervisión con la otra terminal a los mandos.** Él ejecutó todos los
clics allá; aquí se revisó el guion **antes** de cada paso y se midió **después**.
`T-059` ✅ **cerrada del todo**: `t3.micro`, Ubuntu Server 24.04 LTS, Elastic IP
asociada, DuckDNS resolviendo. Commits `5075762` y `aff4350`, subidos.

### 🔎 Las tres revisiones de esta terminal, y las tres cambiaron el día

**1. El guion describía un mundo que ya no existía.** `console_steps.md` §Paso 3
punto 5 decía *"Elastic IP: reservarla y asociarla"* — escrito en la sesión 41,
cuando no había ninguna. Al partirse `T-059` en la 46 se ejecutó solo *reservar*,
**y el punto se quedó igual**. Seguirlo al pie de la letra alquilaba una segunda
dirección, y **en AWS la que cobra es la ociosa**. → `L-028` en TEAPP:
*partir una tarea en dos deja el guion operativo describiendo la mitad vieja, y
eso ningún `grep` lo encuentra — porque el texto no cambió, cambió el mundo que
describía.*

**2. El aviso del cortafuegos vivía solo en el chat.** El asistente de lanzamiento
preselecciona un `launch-wizard-1` con el 22 abierto al mundo, y deja sin usar el
grupo de `T-060a`. Buscado en `console_steps.md`: **el Paso 3 no mencionaba el
cortafuegos ni una vez.** Es `LM.13` en vivo — *un freno que solo vive en la
conversación se muere al cerrar la sesión*, que es exactamente cómo falló el sello
`D-041` el día anterior. Quedó escrito **antes** de tocar la consola.

**3. Ubuntu Pro, una puerta que no estaba en ninguna lista.** El desplegable
ofrecía cuatro opciones que **no eran cuatro versiones, sino dos versiones × dos
productos**. Pro se factura por hora aparte de la instancia. 🔑 **Es el patrón de
"Actualizar plan"** (`LM.22`): no está escondida en un menú al que nadie entra,
está **en la lista que hay que usar**, a una palabra del nombre bueno, con tráfico
garantizado. No entró en las 7 puertas porque es de otra familia —no cambia el
plan de la cuenta— **pero muerde el mismo experimento**: con Pro, `A-018` deja de
ser legible. El testigo se dejó en pantalla (`Free tier eligible`), no en mi
memoria. → `D-043`.

📌 **Y sobre `install.sh`: el argumento escrito era el flojo.** La otra terminal
defendió la 24.04 diciendo *"los paquetes cambian de nombre entre versiones"*.
Se leyó el guion: **no fija ni una versión** — ni `24.04`, ni `noble`, ni
`python3.12`. Eso no salva el argumento, **lo invierte**: un guion que no fija
nada se come lo que el sistema le dé. No es portátil, es **obediente**.

### ✅ La cadena de AWS, medida desde fuera (lo que la otra terminal no pudo ver)

```
teapp.duckdns.org  ->  32.199.xx.xx   (TTL 60)  <- ya NO es la IP de su casa
PTR de esa IP      ->  ec2-32-199-xx-xx.compute-1.amazonaws.com
```

**Cuatro eslabones en una sola medida, y ninguno es un reporte:** DuckDNS
repuntado, la instancia existe, la IP está asociada a ella, y `compute-1` es el
nombre interno de AWS para **`us-east-1`** — la región confirmada por AWS, no por
el selector.

⚠️ **`session-closer` hizo lo correcto marcándolo *"reportado, no visto"*** — su
instrumento es `git diff` y con eso no se ve una nube. Lo que no fue correcto fue
la frase siguiente: *"si algún eslabón no fuera como lo describimos, saldría
mañana al conectar por SSH"*. **Aplaza a mañana algo que hoy tardó doce segundos.**
Es la sesión 42 por segunda vez: la pregunta no es *"¿es mío este artefacto?"*
sino **"¿qué podría mirar alguien de fuera?"**

### 🔬 `T-060b` no estaba bloqueada, y le faltaba el control

`aff4350` la dejó bloqueada por `T-062` razonando: *"nada escucha en el 8000
todavía, un escaneo saldría cerrado igual sin decir nada"*. **Es `L-020` bien
aplicada** —un instrumento ciego da silencio, no un dato falso— pero tenía cura,
y es la del curso desde la sesión 8: **poner un control al lado.**

```
80   : RECHAZADO   (llego a la maquina, nada escucha)   <- CONTROL
443  : RECHAZADO   (llego a la maquina, nada escucha)   <- CONTROL
8000 : TIMEOUT     (el paquete se descarto - cortafuegos)
22   : ABIERTO
```

🔑 **"Cerrado" y "cerrado" no son la misma palabra.** Un puerto **permitido** sin
nada detrás devuelve `RST` inmediato: *rechazado*. Un puerto **descartado** por el
grupo de seguridad no devuelve nada: *timeout*. El 80 y el 443 demuestran que la
máquina sí contesta a lo permitido, y **contra ese control el silencio del 8000 sí
dice algo**. La primera mitad de `T-060b` está medida con la máquina en blanco.

⚠️ **Lo que sigue sin medirse, y esa mitad sí espera a `T-062`:** que uvicorn se
ate a `127.0.0.1`. Son **dos frenos distintos** — el cortafuegos y el `bind`— y
hoy solo se pudo ver morder uno.

⚠️ **El 22 sale ABIERTO y es lo esperado: se escaneó desde su misma casa**, con la
IP autorizada. Buena noticia doble (la regla lleva la dirección correcta; mañana
el SSH entra), **pero no se apunta como "el 22 está bien cerrado"**: desde este
mirador no se puede ver si el mundo llega al 22. Es `L-019` — el sabotaje
disfrazado de aquello que quiere atacar.

### 🚨 Lo que cambió para siempre hoy

**La cuenta pasó de UNA fuente de gasto a DOS**: la IP elástica y la máquina
encendida. `A-018` sigue vivo, pero **el importe ya no se puede atribuir a la IP
sola**. La aritmética limpia de la sesión 51 (`23 h × $0,005 ≈ $0,12`, que ayer
sirvió además de inventario para descartar una segunda IP) **ya no vuelve**.
El experimento perdió su instrumento el día en que cumplió su objetivo.

### Saldo de la sesión 55

**Primera máquina encendida del curso.** Décima sesión sin tocar código de la app.
Dos trampas cazadas antes del clic, ninguna de ellas en la lista de las 7 puertas,
y las dos **escritas en `console_steps.md` antes de tocar la consola, no después**.

⭐ **Lo de más valor no fue la máquina: fue que las dos trampas se encontraron
leyendo lo que estaba puesto, no pensando en lo que debía estar puesto.** Y que la
tercera —`T-060b`— se encontró preguntando *qué control le falta a esta medida*.

### ⏳ Pendiente para la próxima sesión

1. 🔓 **SSH con `teapp-key` y correr `install.sh`.** Es la primera vez que ese
   guion pisa una máquina de verdad. `L-024` dice hasta dónde llega la prueba del
   contenedor: **muere en `systemctl`**, así que el servicio y el arranque se
   estrenan mañana enteros.
2. 🔬 **Cerrar `T-060b`** con la app viva: falta la mitad del `bind` a `127.0.0.1`.
3. 📖 **Releer las 7 puertas otra vez** si hay clics en consola (`L-026`: es
   disciplina, y la disciplina se degrada).
4. 🔬 **`A-018` con la lectura nueva**: ahora hay dos fuentes; anotar la hora de
   encendido de la EC2 para poder separarlas.

---

## 🟢 SESIÓN 54 — apareció el primer cargo, y el sello falló por donde nadie miraba

**Sesión de supervisión y lectura. Cero código, $0,00.** Novena seguida sin
encender una máquina. La lectura del experimento **por fin dio un número distinto
de cero** — y el día cerró **sin ejecutar el sello que lo mandaba**.

### 🟢 El dato: 0,12 US$, y en una pantalla que no estaba en ninguna tabla

Lectura del estudiante, **2026-08-08 ~05:50 hora Colombia = ~10:50 UTC**
(~43,4 h desde `t=0`, que fue 2026-08-06 15:29 UTC):

| pantalla | campo | valor |
|---|---|---|
| Presupuesto (el instrumento **sellado**) | `Importe utilizado` | **0,00 US$** |
| Inicio de *Facturación y costos*, widget `Resumen de Costos` | `Costo Acumulado Mensual` | 🟢 **0,12 US$** |

🔑 **Esto mata la causa (b) de la enmienda de `D-040`.** Había dos explicaciones
vivas para un `0,00`: **(a)** el dato no ha aterrizado, **(b)** algo absorbe el
cargo. **Hay 0,12 US$ visibles: nada los absorbe.** La (b) muere por observación,
no por argumento.

🎁 **Y la predicción acertó.** En la sesión 51 quedó escrito, antes de medir nada:
*"la IP ociosa cobra ~23 h × $0,005 ≈ $0,12"*. La pantalla dice **0,12**. Una
cuenta escrita por adelantado y confirmada después — es lo contrario del
`~$0.02` de la sesión 43.

⚠️ **Y él vio el dato porque miró DE MÁS.** El protocolo decía *"UN campo:
`Importe utilizado`"* — y ese campo es **el único que no se movió**. Obedecida la
instrucción al pie de la letra, hoy se escribiría *"sigue en 0,00"* sin saber por
qué. 🔑 **Un protocolo que estrecha la mirada protege del ruido y ciega para lo
que no estaba previsto.**

📌 Corrección menor al registro de la otra terminal: anotó `11:10 UTC (~43,7 h)`;
la lectura del estudiante fue *"más o menos las 5:50"* = **~10:50 UTC, ~43,4 h**.
Veinte minutos, no cambia ninguna conclusión — pero `43,7` tiene un decimal que
la observación no tiene. **`LM.23` en pequeño: precisión mayor que la fuente.**

### 🚨 EL HALLAZGO DEL DÍA — el sello `D-041` falló, y no como se temía

Ayer se selló: *"la lectura del 2026-08-08 es el límite; diga lo que diga,
después se lanza `T-059`"*. **El 08 cerró sin lanzar.** Dos sesiones, ninguna
llegó al clic: la de TEAPP se cerró después de la lectura (`76493e7`, y lo anota
con honestidad), y esta se cerró después de la explicación.

🔑 **Y lo importante es CÓMO falló.** El sello se diseñó contra una frase concreta
—*"esperemos un día más"*, que con el número delante siempre parece razonable— y
**contra eso funcionó: nadie la dijo.** Falló por otro lado: **se acabó la sesión
antes de llegar.**

> ⚠️ **Un sello protege de un argumento. No protege de que se agote el tiempo.**
> Lo que no tiene defensa no es la tentación de esperar: es que la tarea esté
> **al final de la lista** dos días seguidos.

📌 **Es pariente de la sesión 33** (*el cierre se cumplió entero y dejó el trabajo
sin salvar*): un control que se cumple en su letra y no consigue lo que quería.
→ **Candidata a `LM.24`, y se escribe en TEAPP** (`lessons.md`), no aquí — la
numeración `LM.*` es de allá. Esta terminal **no toca ese repo**.

✅ **La defensa, y es de una línea: mañana `T-059` va PRIMERO**, antes de leer
ningún campo. La lectura ya no la bloquea —el cargo apareció— y ponerla delante
es lo que la dejó sin ejecutar dos veces.

### 🐛 El documento es bueno y el resumen es peor que el documento

Se leyó `A-018` entera en el repo, no el informe. **Es de las mejores entradas
del proyecto**, y marcó sola, sin que nadie se lo pidiera:

- que **`h1` no ha ocurrido** y que `A-018` **no se cierra**;
- que la hora en que apareció el 0,12 **se perdió y no se recupera**
  (*"un instrumento que no se conoce no se puede haber mirado"*);
- la cuenta de las ~24 h marcada como **aritmética de lista, no corrida**;
- que **no verificó si el widget mide bruto o neto**, y **por qué la conclusión no
  depende de ello** — cualquier valor > 0 basta;
- que esto **no viola `D-040`**, con el argumento correcto: la tabla *encargaba*
  distinguir (a) de (b), y esto **la ejecuta**;
- que el widget vive en la página de la **octava puerta**, y que este hallazgo
  **aumenta el tráfico** por ella (`LM.22`).

🚨 **Pero el resumen que llegó al estudiante perdió dos cosas del documento:**

| el documento dice | el resumen dijo |
|---|---|
| *motivo (2) de `D-041`:* 🚨 **SIGUE VIVO. La alarma no ha mordido ni una vez** | *"lo primero que toca es lanzar la t3.micro"* — **el motivo (2) no aparece** |
| la espera tenía **fecha de caducidad** (`D-041`) | *"seguir mirando **hasta que** deje de ser 0,00"* — **espera sin final** |

→ **`LM.20` por TERCERA vez en cuatro sesiones**, y con una vuelta nueva: antes la
razón estaba escrita **por otro**; hoy **estaba escrita por quien informó, ese
mismo día, en el mismo commit.** No es que no se leyera el archivo: es que **el
resumen no hereda las salvedades de lo que resume.**

### ⚖️ La recomendación de esta terminal — lanzar, y con argumento de ellos

El motivo (2) (`L-013`: *no enciendas el fuego antes de probar el detector*) queda
respondido por una frase del **propio documento** de la otra terminal, que el
resumen tampoco trasladó:

> *Los 0,12 US$ ya están bancados y superan el umbral por 12x, atribuibles solo a
> la Elastic IP. El próximo refresco del presupuesto cruza el umbral por ese
> cargo, encienda o no la EC2. Lo que la EC2 emborrona es la **cuantía**, no el
> **cruce**.*

🔑 **El detector ya está cargado.** La prueba de la alarma está en marcha y el
lanzamiento no la cancela. Y hay una red que ayer no existía: **el widget va ~20 h
por delante del presupuesto** — ventana de aviso temprano para los seis meses.

⚠️ **El riesgo que queda, sin adornar:** si el presupuesto no se refresca *nunca*
—roto, no lento— se descubriría con una EC2 encendida. Lo acota que una `t3.micro`
no quema $200 en un día, y ahora se ve el gasto un día antes.

### 📖 Se explicó el clic antes de darlo, a petición suya

Leído `deploy/console_steps.md` §Paso 3 y §Paso 4. Lo que se le explicó: que
`T-059` son **tres** cosas (instancia, asociar la IP, apuntar DuckDNS); que **la
app NO queda arriba** —la máquina queda en blanco—; las cuatro trampas ya cazadas
(**la región**, que abre en Ohio y no da error; **la VPC**, el mismo animal un
piso abajo; **el `.pem`**, única forma de entrar; **las tildes** en las
descripciones); y que las **8 puertas se releen antes**, porque `L-026` dice que
esa lista **no es un freno sino disciplina, y la disciplina se degrada**.

### Verificado por MÍ en esta terminal, corriéndolo

```
git -C TEAPP log      : 76493e7  <- el commit existe
git -C TEAPP status -sb : ## main...origin/main  <- subido, sin "ahead"
git show --stat 76493e7 : solo _persistence/ (3 archivos)  <- ni app/ ni tests/
git status (Edu_TripleS): solo PROGRESO.md  <- ni .env ni claves
```

### Saldo de la sesión 54

**Cero código. Novena sesión seguida sin encender una máquina. $0,00.**
El experimento dio su primer número, la causa (b) murió, y `A-018` sigue abierta
porque **`h1` no ha ocurrido**: el presupuesto sigue en 0,00 y la guardia de las
≥12 h ni ha arrancado.

⭐ **Lo de más valor no fue el 0,12: fue ver cómo falla un sello que se cumplió en
su letra.** Y que el mejor documento del proyecto llegara resumido sin sus dos
salvedades más importantes.

### ⏳ Pendiente para la próxima sesión — en este orden, y el orden cambió

1. 🔓 **`T-059` PRIMERO, antes de leer nada.** Instancia `t3.micro` + asociar la
   Elastic IP + apuntar DuckDNS. **Va delante porque ir detrás lo dejó sin hacer
   dos días.**
   - Antes del primer clic: releer las **8 puertas** (`T-068`).
   - Comprobar **región = Norte de Virginia (`us-east-1`)** y la **VPC**.
   - Usar el grupo de seguridad **que ya existe** (`T-060a`), no crear otro.
2. 🔬 **Después**, la lectura: `Importe utilizado` **y** el widget. Si el
   presupuesto pasa de 0,00 → **eso sí es `h1`**, y arranca la cuenta de `h2`.
3. `T-060b` con la máquina viva: el **8000 escaneado desde fuera**.
4. Para la otra terminal: escribir **`LM.24`** (el sello que se cumple y no
   consigue) y corregir `~43,7 h` → **~43,4 h, aproximada**.

---

## 🔒 SESIÓN 53 — el freno de `T-059` se sostuvo, y la espera quedó con fecha de caducidad

**Sesión de supervisión.** La otra terminal abrió recomendando **lanzar la EC2 hoy**
(`T-059`, segunda mitad): *"desbloquea todo lo demás y apaga el goteo de la IP"*.
Se paró. **Decisión suya, tomada con los tres costos delante: esperar un día.**

### 🚨 El choque: la recomendación contradecía un freno escrito por ellos mismos

`_persistence/tasks.md`, entrada `T-059`, de su puño:

> *"No se hace todavía **a propósito**: primero hay que leer el resultado del
> experimento de `[A-018]`."*

`T-059` es la **primera tarea partida en dos** del proyecto, y se partió por ese
experimento. Hoy se recomendó hacer la segunda mitad **sin mencionar el motivo del
freno**. → **`LM.20` por segunda vez en tres sesiones: la razón ya estaba escrita
y nadie la alcanzó.** No la contradijeron: no la vieron.

📌 Y no se resolvió citando la regla. Se volvió a mirar si el freno seguía valiendo.

### Las tres razones por las que sigue valiendo — y ninguna es "por precaución"

**1. Lanzar hoy mata una medición irrepetible.** Con la IP ociosa como **único**
gasto y `t=0` sellado (15:29 UTC del 06), `t_cargo − t=0` es el retraso real de la
alarma. La bitácora ya decía que **vale más que el experimento**: se mide una vez y
sirve seis meses. Encendida la EC2, el `Importe utilizado` mezcla dos fuentes y
**el cargo deja de ser atribuible**. La cuenta se abre una sola vez.

**2. Es encender el fuego antes de probar el detector.** La EC2 es lo primero que
puede quemar los $200 de verdad, y la alarma **nunca se ha visto saltar** —
`LM.13`. Siete sesiones defendiendo ese orden para invertirlo el día 8.

**3. El argumento del dinero iba al revés.** *"Apagar el goteo"* sustituye la IP
ociosa por una instancia encendida 24/7 **más su disco**, que bruto cuesta más.
⚠️ **Aritmética de lista, no corrida, y va marcado como tal** — no se verificó el
precio hoy. Lo que sí es firme es el otro lado: **esperar un día cuesta ~$0,12.**

### 🎁 Y el hallazgo de las 11:13 empujaba al mismo lado, sin que nadie lo notara

El commit `1c3118d` (tercera lectura) encontró el **cuarto reloj** — el de relleno
del presupuesto, que vence **durante el 07**. O sea: **mañana es la primera lectura
con los cuatro relojes vencidos.** Es el día en que el experimento por fin puede
hablar. La recomendación de lanzar hoy se lo comía — **y salió de la misma terminal
que descubrió el reloj, tres horas antes.**

### 🔒 EL SELLO — escrito HOY, antes de ver el número de mañana

> **La lectura del 2026-08-08 es la fecha de caducidad de la espera.**
> **Diga lo que diga, después de esa lectura se lanza `T-059`.**
> - Si `Importe utilizado` > 0,00 → el experimento concluye, y además se lleva `h1`.
> - Si sigue en `0,00` → **eso ya no es "esperar más"**: es la causa **(b)** de la
>   enmienda (*algo absorbe el cargo*), y es un **hallazgo**, no una excusa.

🔑 **Por qué se sella hoy y no mañana:** mañana, con el número en pantalla,
*"esperemos un día más"* vuelve a estar disponible y **siempre parece razonable**.
Es `D-040` aplicado a la decisión en vez de a la lectura. Una espera sin fecha de
caducidad no es prudencia: es la puerta del paso 6 de su método convertida en
pasillo.

⚠️ **Y el reparo honesto, anotado porque la otra terminal tenía parte de razón:**
`T-059` **es** el cuello de botella y tres tareas cuelgan de ella. En algún punto
esperar deja de ser criterio y pasa a ser miedo. El sello existe para que ese punto
tenga fecha en vez de sensación.

### ✅ Y la Elastic IP se resolvió sola

El punto 2 de las pendientes de ayer (*"soltarla o asociarla"*) **deja de ser una
decisión suelta**: no se suelta —mataría el generador del experimento— y se asocia
mañana, que es **la segunda mitad de `T-059` de todos modos.** Dos pendientes que
eran una.

### 🐛 Dos datos viejos en el informe de la otra terminal

| dijo | es | de cuándo |
|---|---|---|
| `342 tests verdes` | **348** (corridos aquí: `348 passed in 17.43s`) | 342 es de la sesión 50 |
| *"S-026 (hoy) — **Segunda** lectura"* | hubo una **tercera**, `1c3118d`, hoy 11:13 | su propio commit, 3 h antes |

Ninguno cambia la decisión. Se anotan porque **el informe iba detrás de su propio
Git**, y el segundo es el que escondía el argumento bueno: el cuarto reloj.
→ **`LM.23` con el signo cambiado: no es que se midiera y no se anotara — se anotó
en un sitio y se informó desde otro.**

### Verificado por MÍ en esta terminal, corriéndolo

```
pytest (suite entera TEAPP) : 348 passed in 17.43s   <- el informe decia 342
git -C TEAPP log            : 1c3118d  <- tercera lectura, no estaba en el informe
git -C TEAPP status -sb     : ## main...origin/main  <- sin "ahead"
git status (Edu_TripleS)    : solo PROGRESO.md       <- ni .env ni claves
```

### Saldo de la sesión 53

**Cero código escrito. Octava sesión seguida sin encender una máquina, $0,00.**
El trabajo del día fue **parar un lanzamiento** y ponerle fecha de caducidad a la
espera. `T-059` sigue partida; la Elastic IP sigue reservada y sigue siendo el
generador del experimento.

⭐ **Lo de más valor no fue tener razón, fue el orden:** el freno se revisó antes de
invocarlo. Si el freno no hubiera aguantado las tres preguntas, hoy habría EC2.

⚠️ **Nada nuevo en `LESSONS.md`, y es correcto.** Lo de hoy son `LM.13`, `LM.20` y
`LM.23` **repitiéndose**, no lecciones nuevas. Inventar una `LM.24` para que el día
parezca productivo sería la trampa del ritual que este mismo archivo denuncia.

### ⏳ Pendiente para mañana, 2026-08-08 — en este orden

1. 🔬 **UN campo:** `Importe utilizado`. **Anotar `h1`.** No tocar la cabecera.
2. 🔓 **Después, y diga lo que diga: lanzar `T-059`** (instancia + asociar la IP +
   apuntar DuckDNS). **Está sellado hoy** — ver arriba.
3. `T-068` releída antes del clic (7 puertas + la octava del protocolo).
4. `T-060b` en cuanto la máquina viva: el 8000 escaneado **desde fuera**.
5. Suelto de hoy: `T-055`, la mitad de Caddy en el contenedor. Gratis, sin EC2.

---

## ✅ SESIÓN 52 — la tabla sellada llevaba un día diciendo algo falso

**Sesión de supervisión pura desde esta terminal.** Cero código escrito aquí. El
trabajo del día fue auditar a la otra terminal y **un clic** en la consola.

### 🚨 Lo primero: la sesión 51 estaba escrita y NO commiteada

`git log` iba por la 50; `PROGRESO.md` y `LESSONS.md` (con `LM.19` y `LM.20`
dentro) llevaban 277 líneas **en un solo disco**. Es el bicho de la sesión 33 en
versión pequeña. Commiteado y subido: `f1ae968`, verificado con `git status -sb`
→ **sin `ahead`**. Que haya hash no basta; el testigo es el remoto.

### 🚨 EL HALLAZGO: la fila 3 de la tabla sellada estaba muerta

La tabla de `A-018`, sellada en `cfba50a` **antes del primer clic**, decía:

```
coste = $0.00  ->  las horas de IPv4 aplican: experimento no concluyente
```

Esa fila **no dice solo "no concluyente": nombra una causa.** Y esa causa la
desmintió la otra terminal **esa misma mañana** —se cazó a sí misma antes de
escribir *"es gratis por las 750 horas"*— **sin ver que al hacerlo mataba una
fila de la tabla.**

✅ **Comprobado por MÍ en la fuente**, no aceptado de su informe:

> *"There is no change in pricing for idle public IPv4 addresses that you
> allocate in your account but don't attach to an EC2 instance."*

Las 750 h son para direcciones **en uso**. La IP ociosa cobra: `23 h × $0,005 ≈
$0,12`, **doce veces el umbral**. La premisa del experimento está viva.

🔑 La 51 cazó que el `0,00` **se disfrazaba** de la fila 3. Nadie miró si la fila 3
**seguía siendo verdad.** Se auditó el dato nuevo, no el papel viejo. → **`LM.21`**

⏱️ **Y solo se podía hacer ese día.** Leído el número, la enmienda ya no habría
sido un criterio: habría sido una explicación buscada para lo que ya estaba en
pantalla. Era **lo único con fecha de caducidad** de toda la sesión.

### El cambio de instrumento: bien razonado, con un precio que había que decir

Pasaron de la **factura** al `Importe utilizado` del presupuesto — mejor, porque
es el mismo instrumento que alimenta la alarma y desaparece una suposición. El
precio, escrito por esta terminal y aceptado:

| | |
|---|---|
| **Se pierde** | ya no detecta un fallo en la **entrada** de datos al presupuesto |
| **Se conserva** | el tramo *"el presupuesto vio el dinero → mandó el correo"* |
| **Falla del lado** | **seguro**: si el servicio está ciego, ambos callan → se lee *"aún no hay cargo"* y se sigue esperando |

### La guardia de la fila 2 — mi reparo se quedó corto

Planteé un camino a conclusión falsa: declarar *"alarma rota"* por un correo que
solo iba con retraso. **Resultó peor:** los presupuestos se refrescan *"up to
three times a day… 8–12 hours after the previous update"*.

⚠️ **Pero el motivo que escribieron primero era doble conteo** (`24 + 12 = 36`):
el refresco ya está dentro de que el importe sea visible. Corregido. La guardia
de ≥12 h **se queda** —esperar de más no produce conclusiones falsas, solo
tarda— con el motivo bueno: **no sabemos si lo que se muestra y lo que se evalúa
comparten reloj.**

🔑 **Una regla correcta sostenida por una razón que podía no serlo. Es `D-039`
con el signo cambiado**, y peor: un motivo escrito se lee como verificado.
📌 Anotado también que la corrección **contenía el mismo defecto que corregía**
(afirmaba sin seto el doble conteo, que es el mismo desconocido). Segunda vez en
dos sesiones que una corrección trae dentro su propio bicho.

✅ **Y la espera dejó de ser tiempo muerto:** `h1` (importe visible) y `h2`
(correo). **`h2 − h1` es un número que hoy no tiene ni la documentación**, y
decide la duda gratis. `LM.19` otra vez: la lista decía qué falta por construir,
no qué falta por saber.

### `T-060a` hecha, y lo que esta terminal aportó al clic

| aporte | qué era |
|---|---|
| **`T-060` partida** en `a`/`b` | crear el grupo **no es** tener cortafuegos. `T-060b` = medido desde fuera con la máquina viva. Si no, es `LM.13` con otro traje |
| **La octava puerta** | *"Actualizar plan"* salió de `T-068` y pasó al **protocolo de lectura** → `LM.22` |
| **`T-068` reclasificada** | único control **estructuralmente inverificable**: probarlo es el desastre. No es freno, es **disciplina** — y se degrada. (`L-026`) |
| **La región** | `us-east-1` = `D-033`, sellada en `9cc1b72` antes de tocar el selector. Cuadra |
| **La trampa de la VPC** | el piso de abajo de la trampa de la región: grupo en la VPC mala **no da error**, solo no aparece al lanzar |
| **La salida se queda abierta** | "denegar por defecto" es de **entrada**. Endurecer la salida mata `install.sh` **pareciendo un fallo de red** |
| **El aviso del 22** | le faltaba el final: si tu IP cambia, se arregla en un minuto. Molestia, **no** cierre de puerta |

### Verificado por MÍ al cierre, corriéndolo

```
4a0a88a                 : existe
git status -sb TEAPP    : ## main...origin/main   <- SIN "ahead"
archivos del commit     : 6, TODOS .md            <- ni una linea de codigo
sg- / cuenta / IP / ARN : cero coincidencias en el diff entero
docker teapp-test       : Up 2 hours, ubuntu:24.04  <- sigue vivo
```

**No corrí `pytest`, a propósito:** el diff no tiene código, así que 348 sigue
siendo 348 **porque nada se movió**, no porque nada se rompiera. Mismo
razonamiento que la 41.

### Saldo del día

Un clic y mucho papel — **y el papel era el trabajo.** `T-060a` ✅ · la enmienda
de `A-018` sellada a tiempo · `LM.21` y `LM.22` · `L-026` · `D-040`.
**$0,00, séptima sesión sin encender una máquina.**

⭐ **Lo de más valor no fue crear el cortafuegos.** Fue cazar que un papel sellado
seguía diciendo algo falso, y arreglarlo **antes** de mirar el dato.

### ⏳ Pendiente para mañana, 2026-08-08

1. 🔬 **UN campo:** `Importe utilizado` del presupuesto. **Y anotar `h1`** — sin
   esa hora, la segunda medición no existe. **No tocar la cabecera de la página.**
2. 🚨 **Decidir la Elastic IP**: soltarla o asociarla. Lleva **dos días** cobrando.
3. `T-068` releída antes del siguiente clic (7 puertas + la octava en el protocolo).
4. Sueltos: el contenedor `teapp-test` encendido · las 2 menciones muertas de `L-025`.
   ✅ **RESUELTO en el mismo cierre:** el `.env` del contenedor tenía
   `ANTHROPIC_API_KEY=` **vacía** — la llave entra en el paso 8. Medido pidiendo
   **la longitud, no el valor**. Ver el apéndice.

---

## 📎 APÉNDICE DE LA SESIÓN 52 — lo que pasó DESPUÉS del cierre

**El cierre ya estaba commiteado (`07b06ed`) y salieron tres cosas más.** Se
anotan aquí en vez de fingir que estaban dentro.

### 🚨 Un error MÍO, y es el tercero del mismo día con distinto dueño

Recomendé cobrarle a `T-055` su mitad de Caddy en el contenedor, diciendo que ahí
había *"un Caddy de verdad hablando con un uvicorn de verdad"*. **Falso, y no lo
medí: lo deduje** de que `progress.md` decía *"con uvicorn y Caddy dentro"*.

Eran **dos procesos sueltos con el Caddyfile de fábrica.** Lo cazó la otra
terminal al ir a hacerlo.

> **"Dentro" dice que el binario está instalado. No dice que esté delante de la
> app.** Leí una frase de inventario y saqué una conclusión de topología.

🔑 Es `LM.17` otra vez —*un `md5` no dice "todo igual", dice "los bytes,
iguales"*—. **Y es la tercera cara del mismo bicho en un solo día, de tres
participantes distintos:** las horas de IPv4 (la otra terminal), la fila 3 de la
tabla sellada (el papel), y el aparejo inexistente (yo).

### ✅ `T-055` amaneció costando una máquina y se acostó costando cero

`7630862`. Su mitad de Caddy estaba en la lista como **"espera máquina"**. No la
espera: se puede medir en el contenedor, gratis y sin EC2.

📌 **No apareció trabajo nuevo. Apareció que un trabajo conocido costaba mucho
menos de lo que decía su etiqueta.** `LM.19` por tercera vez en dos días.
⚠️ Con su límite escrito **por delante**: ese Caddy sirve por HTTP sin dominio,
así que mide **si escribe la cabecera**, no el `https` final. Media medición
declarada es honesta; media medición callada, no.

### El contenedor se queda vivo, y mi paso 3 se retira

Propuse borrarlo. **La otra terminal lo discutió y tenía razón**, porque la
contaminación solo descalifica para **un** uso:

| uso | veredicto |
|---|---|
| banco de pruebas de `install.sh` **limpio** | ❌ el estado previo falsea el verde |
| caja Linux con Caddy y venv ya dentro | ✅ el estado previo **es el punto de partida** |

Y el riesgo que yo temía —que alguien pruebe ahí dentro de tres sesiones y se
crea el verde— **ya no depende de la memoria de nadie: está en `deploy/README.md`,
donde se mira antes de desplegar.** Borrarlo protege una vez; el README, cada vez.
✅ **Seguro puesto:** `teapp-rig:latest` (1,05 GB), la base congelada. El
`apt-get` se paga una vez.

### 🐛 Y el cabo que la otra terminal marcó sola — `LM.23`

La comprobación de la API key **no dejó artefacto**: vive en la conversación, no
en el repo. Lo marcó como *sin resolver* en vez de darlo por registrado, sin que
nadie se lo pidiera. → **Medido no es lo mismo que anotado.** Cierra el arco del
día: `LM.20` (cierto y no alcanzado) · `LM.21` (sellado y ya falso) · `LM.15`
(silencio leído como verde) · **`LM.23` (cierto y no escrito).**

### Verificado por MÍ al cierre del apéndice

```
TEAPP, 4 commits del dia : 4a0a88a c0f0201 7630862 f08b7b8
git status -sb           : ## main...origin/main   <- sin "ahead"
archivos .py tocados hoy : 0        <- el diff ES lo que se hizo
docker images            : teapp-rig:latest  1.05GB
docker ps                : teapp-test  Up 2 hours
```

---

## ✅ SESIÓN 51 — el día empezó con "no hay nada que hacer sin la nube" y salieron cinco cosas

**Sexta sesión sin tocar la nube.** Cero máquinas encendidas, cero gasto. Y la
sesión arrancó con la otra terminal diciendo, revisadas las pendientes, que
**ninguna se podía cerrar hoy**. Era cierto de las *tareas*. No de la ignorancia.

### 🚨 Lo primero fue un error MÍO, y es el bicho de las sesiones 33, 41 y 50

Le recomendé `T-068` como el trabajo del día. **Estaba hecha desde la sesión 46.**

```
tasks.md:79   T-068 ... | ✅ | 7 |     ← cerrada en dos mitades
progress.md   "A-016 comprobada y FALSA: son SIETE puertas, no tres"
              "console_steps.md, líneas 14-39, minutos antes del primer clic"
```

⚠️ **Dije "cuatro menciones muertas" y al ir a arreglarlas eran DOS.** Las otras
dos decían *"se **lee** antes del primer clic"* — correctas, y no se tocaron.
**Verificar también lo que resultó ser verdad**, incluso cuando lo acusado es tuyo.

🚨 **Y lo peor no es el error, es que ya estaba corregido en este mismo archivo.**
Línea 874, de una sesión anterior:

> *"Dije que `T-068` estaba pendiente. Está ✅. Lo que `PROGRESO.md` decía era
> «se **lee** antes del primer clic» — un freno de lectura, no una tarea.
> **Yo leí "hacer" donde decía "releer".»*

**Segunda vez con el mismo malentendido, y la corrección de la primera llevaba
sesiones escrita cuatro mil líneas más abajo.** No es una copia desactualizada:
es una copia **correcta que nadie alcanza**.
→ **`PROGRESO.md` tiene 7.700 líneas y ha cruzado el punto en que corregirlo por
dentro deja de servir.** Primera deuda estructural del archivo de memoria. Ver el
hueco al final.

⚠️ **Y su censo también estaba mal:** dijo *"las once pendientes"*; `grep -c 🔲`
da **17**. La conclusión resultó sostenerse igual, pero **"ninguna" es una
afirmación sobre un conjunto, y el conjunto estaba mal contado.**

### Lo medido en el contenedor (Docker, ~25 min de tanteo que acabaron en dato)

`deploy/install.sh` —escrito el 5 de agosto, **nunca corrido**, con `bash -n` como
única verificación— corrió entero en Ubuntu 24.04 hasta morir en `systemctl`,
que es donde se predijo. Todo lo que importaba queda antes.

| qué | resultado |
|---|---|
| `T-050`, el mecanismo | 1ª y 2ª corrida: **misma huella**. Con el `.env` borrado: **huella nueva** |
| `T-050`, **el freno visto morder** | guarda anulada (`if false`) → la llave **cambia** entre corridas |
| `A-019` | `caddy adapt` → `"max_size":16000`. Control: `16KiB` → `16384` |
| `A-019`, el borde real | 15999 y 16000 → **401** · 16001 y 16384 → **413** |
| `D-038`, el señuelo de `data/` | guion viejo: crea carpeta vacía ❌ · arreglado: no ✅ |

🔑 **El par 16000/16001 es el que vale.** El `401` prueba que el cuerpo llegó
(falta de sesión, no de tamaño), y uvicorn directo contesta `401` a los cinco
tamaños → **el `413` es de Caddy y de nadie más.** Se retira la salvedad de
dentro de `T-054`, y `A-019` deja de ser documentación: **asciende a `D-035`.**

### El hallazgo del `data/` señuelo — leído aquí, medido allá

Salió de leer `install.sh:126-129`: `mkdir -p "${DATA_DIR}"` corre **antes** de
mirar el `.env` que ya existe, y `DATA_DIR` es siempre `${INSTALL_DIR}/data`. Si
una instalación anterior movió los datos a otro disco, el guion fabrica igualmente
una **carpeta vacía al lado de la app**.

🔑 Es exactamente el señuelo que `D-037` existe para evitar —*"una carpeta vacía y
quien use la app parecería haber perdido su marcador"*—. **El guion lo fabricaba
con la mano.** Arreglado en el origen, con el guion viejo como control rojo.

### `D-039` — una regla muda que ahora habla, y la pregunta estaba mal planteada

`app/config.py` decía, **dentro del código que corre**, que *"en la nube no hay
ningún `.env`: los secretos los pone la plataforma"*. Falso desde `D-029`: la nube
es EC2 y `install.sh` escribe un `.env`. Llevaba **dos días justificando
`os.environ.setdefault` con un motivo muerto**, y un comentario pegado a la línea
se lee como la explicación autorizada de esa línea.

La pregunta que llegó era binaria: *¿invierto la precedencia o cambio solo el
comentario?* **Ninguna de las dos.**

> **La regla de precedencia no está mal. Está MUDA.** Lo específico (el entorno)
> debe ganarle a lo general (el `.env`) — es el canal del que dependen `pytest`,
> el contenedor y cualquier corrida de una vez. Lo que falta es que **diga que
> está mandando.**

Implementado: `config.value_origin` compara el valor vivo contra el que proponía
el archivo, y el log del arranque dice `(TEAPP_DATA_DIR, origen: .env | entorno)`.
**Compara valores en vez de apuntar quién ganó**, porque un apunte envejecería mal
—`monkeypatch` cambia la variable después—.

### ⚠️ Y AQUÍ ME EQUIVOQUÉ YO, con titular y todo

Afirmé que invertir la precedencia haría que **"los 342 tests empezaran a escribir
en `data/`"**. Se saboteó en el contenedor: **346 pasaron, `data/` con 0 archivos.**

**Dónde se me paró el razonamiento:** seguí la cadena hasta el import y me bajé
ahí. `load_env_file` corre **una** vez; el fixture `autouse` corre **342**. El
último que escribe gana, y `D-036` obliga a resolver la ruta en cada llamada.
**Miré el orden de arranque y lo tomé por el orden de la suite.**

→ **La decisión sigue en pie; el motivo era falso.** Es `LM.16` apuntándome a mí.

🔑 **Pero el miedo sí tenía un blanco, y se midió después:** el riesgo nunca
estuvo en pytest, sino en **lo que no es pytest**. Un guion suelto
(`create_account.py`, `measure_body.py`) llama a `load_env_file()` y ahí se acaba:
no hay fixture que pise después, y el portero de `no_data_writes.py` **vive dentro
de pytest**. Con la precedencia invertida, escribiría en `data/` de verdad.
**Es `T-072` exacta y `A-020` con otro disfraz.**
→ **Conclusión correcta apuntando al blanco equivocado.** Eso enseña algo;
*"tenías razón"* no.

### El sabotaje de un solo lado, y lo que escondía

Se saboteó `value_origin` fijándola en `"entorno"`: cayeron los 2 que afirman
`.env`. Se pidió **el espejo**, y ahí estaba lo bueno:

| `value_origin` fijada en | qué cae |
|---|---|
| `"entorno"` | los **2** que afirman `.env` |
| `".env"` | los **4** que afirman entorno, sin valor, y el renglón del log |

🚨 **Con el sabotaje de un solo lado, esos cuatro se quedaban verdes sin que nadie
supiera por qué.** Es la sesión 50 otra vez (*el test decía "rechaza la relativa" y
medía "la carpeta no existe"*), un día después. **Un sabotaje asimétrico audita la
mitad de lo que crees.**

### El punto ciego del instrumento nuevo, escrito antes de que muerda

Cuando el entorno y el `.env` traen **el mismo valor**, `value_origin` no los
distingue. Es benigno —el valor es el mismo— y define **qué mide de verdad** el
renglón: *delata anulaciones, no procedencias.* Queda en el docstring y en `D-039`.

### 🐛 `L-025` — y la regla pescó dos copias que yo había dado por completas

El barrido que exige la propia lección encontró, **después** de que yo cerrara mi
lista: `app/api.py:40-42` (la misma frase muerta, en un segundo archivo) y
`assumptions.md:633` dentro de `A-008`. → **Una lección con su propio control no
es un buen propósito.** Séptima cara del bicho de las copias en tres días.

### Saldo del día

`A-008` encogida y su freno visto morder · `A-019` **muerta** y ascendida a
`D-035` · `D-038` un señuelo real arreglado en el origen · `D-039` una regla muda
que habla · `L-024` y `L-025`, las dos con control propio.
**342 → 348 tests verdes. `data/` sin un solo cambio. Diez archivos en el diff,
ninguno que nadie pidiera. $0,00.**

⭐ **Cuatro de las cinco salieron de que alguien no se creyó un titular** — incluida
la otra terminal con el suyo, y yo con el mío.

### ⏳ HUECO ABIERTO — el experimento de `A-018`, sin leer todavía

**No se leyó en esta sesión, y no por olvido.** A las 14:25 UTC el instrumento
seguía sin estar listo.

🚨 **El hallazgo del día sobre esto, y cambia el reloj:** la consola dice que los
datos de coste tardan hasta 24 h **desde la primera visita a la consola de
facturación** — no desde el cargo. **Es un t=0 distinto del que quedó sellado en
`cfba50a`.** Confirmado que el aviso ya salía el día 6, así que el reloj arrancó
ese día.

⚠️ **Y la página de Facturas dice `Total general estimado: 0,00 USD` con
`Sin datos` tres veces.** Eso **no es un cero medido**: es la suma de un conjunto
vacío. **Se disfraza de la fila 3 de la tabla sellada** (*"las horas de IPv4
aplican"*) y se habría anotado la conclusión contraria.

> **La tabla sellada NO se edita.** La cuarta fila entra como enmienda fechada:
> ```
> instrumento "preparando"  ->  NO HAY LECTURA. No se anota nada.
> ```

🔑 **Y de aquí sale lo que faltaba en el diseño del experimento:** `A-018` predijo
los tres resultados, pero **no predijo cómo sabrías que ya se puede mirar**. El
criterio existe y es gratis: **cuando desaparezca el aviso "Estamos preparando sus
datos de costos y uso".** Hasta entonces no se lee el número, se lee el aviso.

**Pendiente inmediato:** mirar después de ~15:30 UTC. Primero el aviso; el número
solo si el aviso ya no está. Y anotar cuánto tardó.

---

## ✅ SESIÓN 50 — `T-072` resuelta, y el culpable era el instrumento de medida

**Quinta sesión del mismo día, y la quinta sin tocar la nube.** El experimento de
`A-018` sigue sin poderse leer: t=0 fueron las 15:29 UTC y el dato no está antes
del **2026-08-07 a esa hora**. Cero máquinas encendidas, cero gasto.

### Lo que corrió ESTA terminal, y por qué importa el orden

Lo primero del día, antes de opinar de nada, fue **tomar la huella de `data/`**:
bytes **y** fechas. Fue `L-022`/`LM.17` aplicada al día siguiente de aprenderla, y
sirvió: esa huella fue el testigo independiente que verificó **todas** las
afirmaciones posteriores de la otra terminal.

```
pytest TEAPP (al abrir)   : 329 passed in 28.54s
pytest TEAPP (al cerrar)  : 342 passed in 14.66s
data/ al abrir vs cerrar  : ni un byte, ni una fecha  ← huella propia, no la suya
git status -sb TEAPP      : limpio y sincronizado al abrir
.env.example:36           : TEAPP_DATA_DIR=  ← vacío, el defecto no volvió a colarse
load_env_file(), quién lo llama: SOLO app/api.py:42
```

### 🚨 `T-072` cerrada en dos minutos, y el rastro no estaba donde se buscaba

La otra terminal propuso —y era el movimiento correcto— buscar en el historial de
comandos del día. Estaba **medio bien**: `ConsoleHost_history.txt` de PowerShell
no se había tocado desde las 07:51, así que **lo de las 14:48 no lo tecleó nadie**.
Lo había ejecutado un agente, y eso vive en las **transcripciones de sesión**.

```
19:48:17.409 UTC  Write   → measure_body.py           (la báscula de T-054)
19:48:32.094 UTC  Bash    → ejecutarla desde la raíz de TEAPP
19:48:33.051 local        → nacen los dos archivos en data/     ← 1 segundo
```

**El culpable era la medición de `T-054`, de la sesión 48, seis horas antes.** El
script se registraba como `otronombrelargo` y hacía 5 llamadas a `/practice` —los
5 casos de `CASES`—, de ahí `{"score": 5}` y `{"used": 5}`.

🔑 **El mecanismo es de manual: el aislamiento necesitaba TRES desvíos y la
báscula se acordó de UNO.** Desvió `accounts.ACCOUNTS_FILE` a un temporal —con su
comentario *"medir no debe tocar `data/`"*— y dejó `USERS_DIR` y `QUOTA_DIR`
apuntando a los datos de verdad. Y eso explica el "misterio" que abrió `A-020`:
la cuenta no salía en `accounts.json` **porque `accounts.json` fue justo el único
que sí se desvió**.

📌 **No fue un accidente: `probe-log.json`, el otro huérfano, sale del 2026-08-05.**
Otro día, otra sesión, mismo patrón.

### Y una corrección al análisis de la otra terminal

Había concluido que *"`/practice` nunca comprueba que la cuenta exista, así que un
script que se firme su propia cookie entra sin registrarse"*. **El script sí se
registró.** La evidencia que sostenía el titular tenía otra explicación → `LM.16`
otra vez, un día después. Se le pidió **re-verificarlo por su cuenta**, lo hizo con
los tres desvíos puestos y el portero delante, y el mecanismo resultó **cierto
pero más pequeño**: no hay puerta abierta —firmar exige la llave—, lo que no
existe es la **revocación selectiva**. Quedó en `A-021`.

⚠️ **Y esta terminal le corrigió una frase falsa a esa misma entrada:** decía que
no había forma de cortar una sesión. La hay, tosca: **rotar `TEAPP_SECRET_KEY`
las invalida todas de golpe.** Lo que no existe es cortar *una*.

### `D-037` — la raíz de los datos sale del entorno

El arreglo no fue perseguir al culpable, sino **cerrar la puerta**: hoy `data/`
real era alcanzable por defecto desde cualquier cosa que importara `app`.

```
TEAPP_DATA_DIR — absoluta, obligatoria, SIN valor por defecto.
Si falta, o no es absoluta, o no es un directorio: la app NO ARRANCA.
```

**Por qué absoluta y no relativa**, que fue la pregunta que él trajo: una ruta
relativa se resuelve contra *algo*, y ese "algo" es el bicho original — la báscula
acabó tomando la raíz de `sys.argv[1] = "."`, el directorio de trabajo. Y el
argumento que cerró la discusión era suyo: *"con relativa el `.env.example` puede
traer un valor que sirve"*. **Un ejemplo que funciona sin editarlo es un valor por
defecto con pasos extra** — la alternativa que el propio ADR había descartado,
entrando por la puerta de atrás. `TEAPP_SECRET_KEY` ya paga ese precio: en
`.env.example` está vacía, por el mismo motivo.

Tres detalles pedidos desde aquí y puestos: **rechazar la relativa explícitamente**
(no resolverla en silencio), `.resolve()` + `is_dir()` en vez de `exists()`, y
**una línea de log en INFO con la ruta ya resuelta** — que además es el testigo
gratis de `T-066` y el primer ladrillo de observabilidad del paso 7.

⭐ **Dos huecos que encontró ÉL, no yo, y son los que salvan el despliegue:**
`create_account.py` no cargaba el `.env` —y es la **puerta de servicio**, la única
forma de crear la primera cuenta con el registro por red cerrado (sesión 39)—, e
`install.sh` no toca un `.env` que ya existe, para no regenerar la llave, así que
se habría quedado **sin la variable nueva**. Las dos rutas solo se recorren el día
del despliegue: se habrían roto justo cuando no hay otra manera de entrar.

### ⭐ El sabotaje encontró un test flojo, y esa es la mejor parte del día

Puso `if False` en la comprobación de ruta absoluta esperando **dos** rojos. Cayó
**uno**. El otro seguía verde por la razón equivocada: la ruta relativa `data` se
resolvía contra un `cwd` donde esa carpeta no existía, así que saltaba *el otro*
freno. **El test decía "rechaza la relativa" y medía "la carpeta no existe".**

🔑 **`LM.15` era "nadie audita un verde", escrita esa misma mañana. Hoy auditó uno
y estaba podrido.** Cuarta cara del mismo animal en dos días, y la primera que
caza él antes de que muerda. Arreglado creando la carpeta en el `cwd` del test:
ahora la única forma de ponerlo rojo es que la relativa se acepte.

### Lo que queda para mañana, en este orden

1. ⏳ **El experimento de `A-018`**: la factura (la premisa) y la bandeja (la
   prueba), **a partir de las 15:29 UTC**, leídos contra la tabla sellada en
   `cfba50a`. Y anotar cuánto tardó.
2. 🚨 **Soltar o asociar la Elastic IP** — lleva todo el día cobrando por existir.
3. ~~🚨 **`T-068`**, la lista de "esto NUNCA se toca".~~
   ✏️ **FALSO, corregido en la sesión 51: `T-068` está ✅ desde la sesión 46.**
   Lo que queda de ella no es escribirla, es **releerla** antes del primer clic.
   Este renglón hizo que la 51 arrancara recomendando una tarea ya cerrada.
4. **Repuntar DuckDNS a la Elastic IP** (TTL 60 s) antes de encender nada.
5. Solo entonces, la segunda mitad de `T-059`.

---

## ✅ SESIÓN 49 — `T-071` cerrada, y de mirar cinco fechas salió algo mayor

**Cuarta sesión del mismo día, y la cuarta sin tocar la nube.** El experimento de
`A-018` seguía sin poderse leer (t=0 a las 15:29 UTC, ~5 h de las ~24; el dato no
está antes del 2026-08-07 a esa hora). Cero máquinas encendidas, cero gasto.

### Lo que auditó ESTA terminal, corrido aquí

```
pytest, al empezar             : 328 passed
pytest, al cerrar              : 329 passed in 34.72s
check_no_data_writes.py        : 6 passed   ← los controles del portero nuevo
huella de data/users/ ANTES de
  que la otra terminal tocara  : guardada al abrir la sesion  ← salvo el dia
md5 antes / despues de la suite: IDENTICO — la suite no escribe en data/
defaults congelados de tools.py: medido con __defaults__, no leido
los 3 sitios del punto ciego   : comprobados uno por uno
```

### La tarea decía dos archivos y eran tres

El maniquí `autouse` —`monkeypatch.setattr(english_tutor, "add_point", lambda
user: 7)`, palabra por palabra— estaba en `test_api.py`, `test_deploy_limits.py`
**y `test_english_tutor.py`**. `T-071`, escrita la noche antes, nombraba dos.
📌 **Borrar dos y olvidar el tercero es el bicho de las sesiones 33, 41 y 47**:
la misma regla en varios sitios, y un día alguien lee la copia vieja.

### El diagnóstico bueno lo trajo la otra terminal

Las tres funciones del marcador llevaban la carpeta **como valor por defecto en
la firma** (`users_dir: Path = USERS_DIR`), y Python congela ese valor al
importar. O sea: el arreglo "obvio" —un `setattr` en `conftest.py`— **no habría
hecho nada, y el `conftest.py` se habría visto arreglado.** Lo medí aquí en vez
de creerlo: `add_point.__defaults__` sigue apuntando a la carpeta real después de
cambiar `tools.USERS_DIR`. 🔑 **Un aislamiento que parece puesto y no lo está es
peor que no tenerlo.**

Se arregló en el **origen** (`app/tools.py`, como ya hacía `quota.py`), no en los
tests. La tarea estaba escrita como si fuera solo de tests, y eso no era un
contrato sobre qué se puede tocar: era la descripción del síntoma.

### Portero, no test — y por qué se escribieron los dos

Preguntó, antes de escribir nada, si el testigo debía ser un test normal o un
control aparte al estilo de `no_network.py`. **La respuesta fue el portero**, y
la razón es lo que hay que conservar: lo que hace fuerte a `no_network.py` no es
dónde vive, es **qué vigila** — no vigila a un inquilino, vigila **la puerta**.

Un test sobre `add_point` habría seguido verde el día que apareciera una segunda
ruta hacia `data/`. **Y esa ruta ya existe** (ver abajo).

Pero se escribieron **los dos**, y la asimetría vale: el portero se queda verde
si alguien vuelve a poner un maniquí —nadie escribe— y eso solo lo caza el test
que **exige ver el archivo aparecer** en `tmp_path`.

Las tres condiciones que se le pusieron al portero, y las tres son maneras de
entregar uno ciego: que compare **contenido** y no `iterdir()`; que mire **por
test** y no por sesión; y que la carpeta real **no** pase por el desvío, o se
pondría verde mirándose a sí mismo.

### 🚨 El hallazgo del día no era la trampa: `A-020`

De mirar las fechas de `data/users/` salió esto:

```
data/users/otronombrelargo.json   2026-08-06 14:48:33.051240000
data/quota/otronombrelargo.json   2026-08-06 14:48:33.051240000  ← mismo nanosegundo
```

El mismo instante en dos carpetas no es alguien tocando archivos: son **cinco
peticiones a `/practice` completas**, de una cuenta que **no existe** en
`data/accounts.json`. Y no pudo ser pytest —`conftest.py` desvía la cuota de
verdad—, lo que corrobora por otro camino la medida del `md5`.

📌 **Existe un camino que escribe en los datos reales sin pasar por
`conftest.py`, y el portero de `T-071` no lo ve ni lo verá nunca**, igual que
`no_network.py` no ve los subprocesos. Quedó como `A-020` en TEAPP, y de ahí sale
una tarea nueva que **no** es `T-071`.

### `LM.16` — el titular que su propia salvedad desmentía

El análisis decía **"la trampa ya se disparó"** en el titular y, tres renglones
abajo, *"te lo doy como sospecha fuerte, no como hecho medido"*. La salvedad es
impecable; el titular es lo que se recuerda. **Se midió**: la suite no escribe
ahí. Estado real: **armada, no disparada.**

🔗 Es `LM.15` por el otro lado — allí el silencio se leyó como confirmación, aquí
como acusación. **No sostiene ninguna de las dos.**

### `LM.17` — y estrenó `LM.15` dentro del arreglo de `LM.15`

Para ver morder el portero hubo que sabotearlo, y el sabotaje escribe de verdad.
Se hizo con copia previa y se verificó la restauración con `md5`: siete archivos,
siete huellas idénticas. **Correcto — no se perdió ningún dato de la app.**

Lo que se destruyó fue el **`mtime`**: los siete quedaron marcados a las
15:56:56, y con ellos se fue la prueba física del nanosegundo compartido. Se cazó
porque esta terminal había guardado las fechas al abrir la sesión. **Por poco.**

🔑 **Un `md5` no dice "todo igual": dice "los bytes, iguales".** Las tres caras
anteriores eran instrumentos ciegos **a un cambio**; este vio el cambio que le
importaba y fue ciego a **una dimensión entera del archivo**.
→ **La prueba de un defecto no puede vivir en la carpeta que el defecto ensucia.**
Las siete fechas están ahora en `A-020`, en `_persistence/`, que sí va a Git.

### Lo que quedó escrito allá

`D-036` (el arreglo y por qué dos testigos), `A-020` (el camino de fuera, con las
fechas), `L-021` (el titular) y `L-022` (el `md5`). El punto ciego heredado —el
portero tampoco ve fechas— está en los **tres** sitios donde alguien lo va a
leer: el portero, el fixture y `D-036`. Comprobado uno por uno desde aquí.

### 📤 Lo que queda pendiente de la 49

- 🔲 **La tarea nueva del camino que escribe fuera de pytest**, con `A-020`
  detrás como motivo. La mete el cierre de TEAPP, **aparte de `T-071`**.
- 🔲 **`A-019`**: el entero real de `16KB` vía `caddy adapt`, gratis en `T-061`.
- ⏳ **Y lo de siempre:** los dos datos del experimento de `A-018`. **Mañana
  2026-08-07 después de las 15:29 UTC** ya se pueden leer.

---

## ✅ SESIÓN 48 — `T-054` cerrada y MEDIDA, y el defecto del proyecto ya tiene nombre

**Tercera sesión del mismo día.** El experimento de `A-018` seguía sin poderse
leer (t=0 a las 15:29 UTC, ~4 h de las ~24), así que otra vez se adelantó trabajo
que **no gasta el reloj de los 6 meses ni un centavo**. La cuenta de AWS sigue con
**cero máquinas encendidas** y la Elastic IP **no se tocó a propósito**: ella
misma es el disparador del experimento, y soltarla lo habría cortado.

### Lo que auditó ESTA terminal, corrido aquí

```
pytest, al empezar            : 314 passed
pytest, al cerrar             : 328 passed in 16.73s   (+14)
git status TEAPP              : 5 archivos, ni uno de codigo de la app
git check-ignore -v data/     : .gitignore:18  ← el hallazgo del dia
fechas de data/users/*.json   : nada escrito despues de las 14:48
sabotaje MIO, no suyo:
  MAX_SENTENCE_LENGTH 500→5000 → 4 rojos, y api.py restaurado
docs de Caddy (ctx7)          : "formats supported by go-humanize"
```

### Dos correcciones mías al empezar, y las dos las cazó él

1. **Dije que `T-068` estaba pendiente. Está ✅ desde la sesión 45.** Lo que
   `PROGRESO.md` decía era *"se **lee** antes del primer clic"* — un freno de
   lectura, no una tarea. **Yo leí "hacer" donde decía "releer".**
2. De paso apareció que el **traspaso 2 de la sesión 46** (la alerta de coste
   previsto) figuraba aquí como deuda y **ya estaba hecha y verificada en
   pantalla** desde `S-019`. Corregido en su sitio.

📌 Es `LM.14` funcionando **en el sentido contrario**: esta vez el dato malo lo
dio la supervisora y lo cazó él. Dos sesiones seguidas.

### `T-054` — la mitad archivo ya existía; lo que faltaba era la báscula

Yo propuse escribir la directiva de Caddy. **Él avisó de que ya estaba escrita**
desde `T-063` (`deploy/Caddyfile.template:28`), con el comentario que confiesa su
propio defecto: *"el número es por criterio, no por medida"*.

**Lo que faltaba era pesarlo**, y eso sí se podía hacer sin nube. Cinco alfabetos,
frase de 500 caracteres (el máximo que acepta la app), los cinco con **200**:

| frase de 500 caracteres | cuerpo | % de 16000 |
|---|---|---|
| inglés (ASCII) | 516 B | 3,2 % |
| español con tildes | 1016 B | 6,4 % |
| chino | 1516 B | 9,5 % |
| emoji (UTF-8 crudo) | 2016 B | 12,6 % |
| **emoji escapado `\uXXXX`** | **6016 B** | **37,6 %** |

🔑 **El hallazgo suyo, y es bueno: un carácter cuesta entre 1 y 12 bytes.**
`MAX_SENTENCE_LENGTH` acota **caracteres**. Un emoji ocupa 4 bytes en UTF-8, pero
JSON permite escribirlo con **dos** escapes `\uXXXX` seguidos —un *surrogate
pair*— y eso son **12 bytes ASCII para un solo carácter**. No es un ataque: es lo
que produce cualquier cliente que serialice con `ensure_ascii=True`, **el valor
por defecto de Python**.

⚠️ **Y el criterio viejo no estaba solo sin medir: estaba MAL.** Decía *"500
caracteres no llegan a 2 KB"* y el peor caso son 6 KB. **Falso por 3x.** Los 16 KB
estaban bien **por suerte**. Un tope puesto "a unos pocos KB" —que era el
enunciado literal de `T-054`— habría roto el uso normal con emoji.
→ **Un número a ojo no se equivoca al azar: se equivoca en el orden de magnitud
del caso que no imaginaste.**

### 🚨 La corrección de esta terminal: `KB` son 1000, no 1024

Él iba a atar el test a `16_384`. Fui a la documentación de Caddy (`ctx7`, no de
memoria): los tamaños se leen con **go-humanize**, donde **`KB`=1000 y
`KiB`=1024**. El techo real de `max_size 16KB` es **16000**.

Un test contra 16384 se pondría **verde en una franja de 384 bytes donde Caddy ya
está devolviendo 413**. → **Un control verde midiendo un número que no rige es
peor que no tener control.**

⚠️ **Y esto está LEÍDO, no medido** — el mismo estado del "~24 h" de facturación.
Quedó como `A-019` en TEAPP, con su forma de comprobarlo escrita: `caddy adapt`
imprime el entero. **Necesita el binario → se paga gratis el día de `T-061`.**

### Las tres correcciones al test, y por qué

1. **El número se lee del `Caddyfile`, no se copia.** Copiarlo habría creado una
   **tercera** copia (Caddyfile, test, máquina) — y sería el archivo que existe
   para cazar números descoordinados quien introdujera uno.
2. **El ×12 va como constante con nombre y porqué**, no como un `12` suelto.
3. **El techo conservador (16000)**: quedarse corto no rompe nada; pasarse sí.

Y él encontró un hueco propio que yo no vi: sabotear el Caddyfile a `16KiB` salía
**verde correctamente**, o sea que no había testigo de que el conversor
**aplicara** la unidad, solo de que la tabla existiera. Añadió
`test_el_conversor_aplica_la_unidad_y_no_solo_la_conoce`. **Es el mejor test del
archivo.**

### 🚨🚨 EL HALLAZGO DEL DÍA — `LM.15`, y es el más importante de las tres sesiones

Él escribió: *"verifiqué con `git status` que `data/` quedó intacto"*.
**`data/` está en el `.gitignore` de TEAPP, línea 18.** `git status` **no la
mira**: habría callado igual si los tests hubieran escrito ahí.

La conclusión era **correcta** —lo comprobé por las fechas de los archivos, que sí
ven esa carpeta— pero **se supo por suerte, no por la prueba citada.**

| instrumento | qué produce | qué pasa después |
|---|---|---|
| **equivocado** | un dato **falso** | otro dato lo contradice y se investiga |
| **ciego** | **silencio** | se lee como confirmación, y nadie vuelve |

⭐ **La distinción la afinó él, y es la frase que hay que conservar:** *un dato
falso se puede contradecir; el silencio no choca con nada.* Y la ató a `L-016`:
las cinco puertas ❓ de `C-005` eran silencio de AWS leído como un "no pasa nada".
**Mismo animal: allá un texto callado, aquí una herramienta callada.**

🚨 **Tercera cara del mismo defecto en dos sesiones** — el suplantador por
`127.0.0.1` (47), el techo de 16384 (48), y esto (48). Ya no es casualidad: es el
**modo de fallo característico del proyecto**, y tiene razón estructural —
**nadie audita un verde.** El rojo pide explicación; el verde se cobra y se pasa
de página. Quedó como `L-020` en TEAPP y `LM.15` aquí.

### Y el sabotaje que faltaba lo corrió esta terminal

Sus cuatro sabotajes atacaban el `Caddyfile` y el conversor — **el instrumento**.
**Ninguno atacaba el escenario que el test dice existir para cazar.** Lo corrí:
`MAX_SENTENCE_LENGTH` de 500 a 5000 → **4 rojos**, `api.py` restaurado.
→ **Un guardián al que solo se le sabotea el instrumento no ha demostrado morder
en su propia dirección.**

### 📤 Lo que queda pendiente de la 48

- ~~🔲 **`T-071`, propuesta y con el texto ya escrito**~~ → ✅ **CERRADA en la
  sesión 49.** ✏️ Y el texto de la tarea tenía un dato mal: decía **dos** fixtures
  locales y eran **tres** (faltaba `test_english_tutor.py`). `conftest.py` aísla
  cuentas, cuota y `login_guard`, pero no el marcador (`USERS_DIR`).
- 🔲 **`A-019`**: el entero real de `16KB` vía `caddy adapt`, gratis en `T-061`.
- ⏳ **Y lo de siempre, sin moverse:** los dos datos del experimento de `A-018`.

---

## ✅ SESIÓN 47 — `T-055` y `T-052` cerradas sin tocar la nube, y **el supervisor se equivocó**

**Mismo día que la 46.** El experimento de `A-018` no se podía leer todavía (t=0
a las 15:29 UTC, el dato de facturación tarda ~24 h), así que **se adelantó
trabajo que no gasta el reloj de los 6 meses ni un centavo.** La cuenta de AWS
sigue con **cero máquinas encendidas**.

### Lo que auditó ESTA terminal, corrido aquí

```
pytest, al empezar el tramo   : 310 passed in 13.56s
pytest, al cerrarlo           : 314 passed in 16.13s
git TEAPP                     : limpio, 2 commits (1c87836, 0d53775), 2 ahead
install.sh copia el .service  : cp literal, linea 167  ← el cambio llega a la maquina
ExecStart                     : --proxy-headers --forwarded-allow-ips 127.0.0.1
uvicorn instalado             : 0.52.1
  proxy_headers por defecto   : True
  forwarded_allow_ips         : 127.0.0.1
```

### `T-055` — no necesitaba ni una línea de Python, **y eso está MEDIDO**

La tarea traía escrito *"el nombre exacto de la opción se consulta en la
documentación el día que se haga — no se escribe de memoria (regla 6)"*. Se
consultó. Las dos banderas ya vienen puestas de fábrica y hacen exactamente lo
que pedía la tarea: leer `X-Forwarded-For` **solo** si la petición llega por
loopback.

⚠️ **Pero eso era un razonamiento, no una medición** — y la otra terminal lo
midió con **uvicorn de verdad, no `TestClient`** (que es la trampa de `L-010`):
servidor levantado como lo levanta `teapp.service`, logins fallidos hasta el 429,
y mirar qué dirección escribía el log. **Cuatro escenarios, los cuatro verdes.**

El que no era obvio: uvicorn recorre la cadena **al revés** buscando el primer
host no confiable. Como Caddy **añade** la dirección real al final, la cabecera
que traiga quien ataca **queda delante y se descarta sola**. Leído en
`proxy_headers.py`, no supuesto.

### 🎭 El susto del día, y es de la familia de `LM.13`

El escenario del suplantador salió **rojo**, y el rojo era **del montaje**: se
fingió ser un extraño hablando por `127.0.0.2`, y Windows pone `127.0.0.1` como
dirección de **origen** aunque el destino sea otro. La petición entraba
**disfrazada de Caddy** — el sabotaje llegaba vestido de aquello que quería
atacar. Quedó como `L-019` en TEAPP.

🚨 **Lo grave no es el rojo: es la simetría.** El rojo pedía explicación y por eso
se fue a mirar. **El mismo montaje en cualquiera de los otros tres escenarios
habría salido verde por la razón falsa**, y `T-055` se habría cerrado sobre una
medición que no midió nada. **Nadie audita un verde.**
→ Es el defecto de los *26 evals verdes con el contrato roto*, una vuelta más
arriba: allí el control no miraba; aquí el control miraba **otra cosa**.

### 🔎 Los dos hallazgos de esta terminal, y ninguno era un bug

**1. `tasks.md` contradecía a `decisions.md`.** `D-034` daba `T-055` por resuelta
y `tasks.md` la tenía en 🔲. Es el bicho de la sesión 33 y de la 41 otra vez: la
misma cosa en dos sitios diciendo cosas contrarias. **No da error** — un día
alguien lee el cuadrito vacío y rehace el trabajo, o lo rehace distinto.

**2. El acoplamiento mudo entre `teapp.service` y el `Caddyfile`.** Los dos
dependen de que la dirección sea `127.0.0.1` **literal**, y ningún archivo lo
decía. El día que alguien escriba `localhost:8000` —que parece lo mismo y se lee
mejor— puede resolverse a `::1`, uvicorn no se fía de esa dirección y **descarta
la cabecera en silencio**: todo el mundo al mismo cubo, sin un solo error en el
log. **Es el fallo mudo de `A-008` con otro disfraz.** Avisado junto al
`reverse_proxy`.

### ⭐ Y la quinta copia obsoleta estaba EN EL CÓDIGO

La cazó la otra terminal aplicando `L-018` antes de commitear: el docstring de
`_request_origin` seguía diciendo, **en presente y como pendiente**, *"ahí hay que
leer la dirección real de la cabecera"*.

🚨 **Es la peor de las cinco, y por una razón concreta: el código se lee más que
`_persistence/`.** Quien lo leyera mañana implementaría a mano justo el arreglo
peligroso que `D-034` descartó — con la mejor intención. Reescrito (solo el
docstring, ninguna línea de lógica), y ahora cierra la puerta por delante: *"si
algún día parece que falta leerla, la respuesta está en `D-034`"*.
→ **Un comentario obsoleto no es ruido: es una instrucción equivocada con la
autoridad de estar dentro del archivo.**

### `T-052` — cuatro tests, y dos desviaciones del enunciado que mejoraron el test

- El fixture **borra** la variable en vez de ponerla a `"true"`: así se mide el
  valor por defecto **de verdad** —el que correrá en la nube si nadie escribe
  nada— y no una copia nuestra de lo que creemos que vale.
- Se mira la cabecera `Set-Cookie` **en crudo**, no el tarro del cliente: el tarro
  descarta la cookie **con razón**, porque habla por `http://`. Lo que hay que
  medir es lo que el servidor envió.
- **Sabotaje doble**, con `L-019` recién escrita delante: invertido el valor por
  defecto → los cuatro en rojo (miden lo que dicen); quitado el fixture a uno →
  rojo también (**el fixture es quien hace el trabajo**). Se verificó el
  **montaje**, no solo el resultado.
- `A-009` **encogida, no muerta**: la rama ya tiene testigo, pero nadie ha visto
  un navegador de verdad guardar esa cookie por `https://`. Muere con `T-051`.

### 🚨 EL HALLAZGO DE MÉTODO: esta terminal entregó un dato falso → `LM.14`

En el traspaso se escribió *"`cookie_secure()` aparece en `app/api.py:295` y
`app/api.py:512` — **registro y login**"*. Los números eran correctos; **los
nombres se dedujeron sin abrir la función que los contenía**. Los sitios reales
son `_start_session` (ayudante compartido por registro y login) y el
`delete_cookie` de **`/logout`**.

⚠️ **Y el dato malo era peligroso en una dirección concreta:** obedecido al pie de
la letra, `/logout` se habría quedado **sin testigo** — justo el camino que se
olvida, porque no se parece al otro. `A-009` se habría cerrado con la mitad
medida.

**Lo cazó quien construye, mirando el código en vez de obedecer la lista.**
→ `LM.14` en `LESSONS.md`: **el reparto no funciona porque el supervisor acierte,
sino porque quien construye comprueba en vez de obedecer.** Y de ahí sale una
regla de forma: **el traspaso se escribe como cosas que mirar, no como órdenes** —
una orden transmite el error con autoridad; una pregunta lo mata ahí.

📌 **Corrección de reparto, anotada:** la otra terminal **no sabe que esta
existe**. Los traspasos van redactados **en primera persona de él**, sin `LM.x`
ni números de sesión de este repo: allá solo existen `L-0xx`, `D-0xx`, `A-0xx` y
`T-0xx` de TEAPP. Se corrigió a mitad de sesión.

---

## ✅ SESIÓN 46 — `T-057` CERRADA. La cuenta existe y el reloj corre

**Lo hizo la otra terminal con él. Esta lo auditó.** El trabajo de aquí fue el de
siempre: no creer el reporte (`LM.4`).

```
Cuenta abierta, plan gratuito           hecho
MFA en el root, en el mismo acto        hecho
Camino de vuelta del MFA                probado en el iPad  ← no supuesto
Alarma a un céntimo, con correo         hecho
Retraso de facturación (~24 h)          documentación + pantalla
Fin del plan: 2027-02-06                leído en la consola ("185 días")
Desviación del alias +aws               registrada en D-031
```

⏱️ **El reloj de `C-006` arrancó el 2026-08-06. Es una sola ventana en toda la
vida y no se renueva.** Todo lo que queda del paso 7 cabe dentro, y `D-030` dice
que el cierre lo elegimos nosotros: **la fecha real de trabajo es antes.**

### Lo que auditó ESTA terminal, corrido aquí (commit `d811295` de TEAPP)

```
git log --all --name-only | .env|data/|.pem|.key   : 0   ← nunca entraron
git log -p --all | llaves ANCLADAS (4 formatos)    : 0   ← historial limpio
git log -p --all | correo personal literal         : 0   ← la regla de D-031 AGUANTÓ
git status TEAPP                                   : limpio, 0 ahead
```

✅ **Lo mejor del día, y es de método, no de nube:** soltó el alias `+aws`, y la
regla que de verdad importaba —**el correo literal fuera de un repo público**— no
se cayó con ella. Y la desviación se **anotó** en `D-031` en vez de reescribir la
decisión para que pareciera que siempre fue así. **Es exactamente lo contrario de
la sesión 33.**

⚠️ **Lo que esta terminal NO puede verificar, y está bien que no pueda:** la
consola de AWS. No tiene credenciales y no debe tenerlas. El MFA activo, la alarma
y los "185 días" son hechos de pantalla y **el testigo es él** — misma categoría
que el `HttpOnly` de la sesión 36.

### 🚨 EL HALLAZGO DEL DÍA: la alarma es una red, no un semáforo → `LM.13`

Su frase fue *"la alarma existía antes de que existiera nada que pudiera gastar"*,
y el orden **es** el correcto. Lo que faltaba es media frase, y sale de cruzar dos
datos que ya estaban escritos por separado:

| qué puede pasar | ¿la alarma llega a tiempo? |
|---|---|
| máquina encendida y olvidada, goteando | ✅ sí — 24 h de retraso no importan |
| cruzar una de las **7 puertas** de `C-005` | ❌ **no.** Los créditos *"se evaporan en el acto"* |

**La alarma protege del goteo, no del acantilado.** Contra las 7 puertas el único
freno real es `T-068` (la lista de "esto NUNCA se toca"), porque ahí no hay aviso
posible: cuando llega el correo, ya pasó ayer.

📌 **Y la alarma nunca se ha visto saltar.** No se puede poner en rojo barato —
habría que gastar de verdad y esperar un día. Cuando un control no se puede probar,
**se escribe que no está probado**, no se hace como si lo estuviera.

⏳ **Ventana gratis que se cierra sola:** con cero máquinas encendidas, el silencio
de la alarma **significa algo**. En cuanto exista la EC2 (`T-059`), el silencio ya
no distingue *"no hay gasto"* de *"la alarma está mal montada"*.

### El caso hermano, y salió de un sabotaje hecho aquí

La búsqueda de llaves que esta terminal venía corriendo desde la sesión 41 usaba
`AKIA|ASIA` y devolvía **21 avisos. Los 21 falsos**: `ASIA` vive dentro de
**dem·ASIA·do**, y `Select-String` ignora mayúsculas por defecto.

Se ancló el patrón, y **se probó en rojo a propósito** con líneas envenenadas.
Ahí salió lo que nadie sospechaba:

```
flojo   (AKIA|ASIA)  -> 3 avisos: 1 bueno, 2 basura, y SE LE ESCAPA la llave sk-ant
anclado              -> 2 avisos, los 2 buenos
```

🚨 **El patrón flojo era peor en las dos direcciones a la vez: ruidoso Y ciego.**
Uno supone que un control ruidoso al menos es seguro. No lo era. Y eso **solo se
supo al ponerlo en rojo**. → Quedó escrito en `GUIDE.md` **§2.b** (nueva).

📌 Los dos casos del día son el mismo animal: **un control que nunca habla y uno
que habla de más acaban los dos apagados.** Es el defecto de los *26 evals verdes
con el contrato roto*, ahora sobre **dinero y llaves, que no tienen `git revert`**.

---

## 🔬 SIGUIENTE PASO: **LEER LOS DOS DATOS DEL EXPERIMENTO** (no encender nada)

`T-057` ✅, `T-058` ✅, `T-059` 🔄 **partida**: la Elastic IP está reservada, la
máquina no. **Hay un experimento corriendo desde el 2026-08-06, 15:29 UTC.**

```
1. ¿Hubo cargo bruto?  -> la FACTURA.  Es la PREMISA.
2. ¿Llego el correo?   -> la BANDEJA.  Es la PRUEBA.
```

Se leen **contra la tabla de `A-018`**, que está sellada en `cfba50a` desde antes
del clic. **Los tres veredictos ya están escritos**: no se decide ahora qué
significa cada caso.

- ⏱️ **Y se anota cuánto tardó**: ese número sustituye al "~24 h" de documentación.
- ⚠️ **Después**, el umbral definitivo (**$200 ÷ 6 ≈ $33/mes**) — no antes.
- 🚨 **Y soltar o asociar la Elastic IP**: mientras espera, cobra por existir.

**Solo entonces la segunda mitad de `T-059`**, que **sí enciende una máquina**.
Antes de encenderla:

- 🚨 **Repuntar el nombre de DuckDNS a la Elastic IP** en cuanto exista. Hoy
  apunta a la casa (hallazgo 2 de la sesión 42). TTL 60 s: tarda un minuto.
- 🚨 **`T-068` —la lista de "esto NUNCA se toca"— se lee ANTES del primer clic**,
  no después. Es el único freno que corre a la velocidad del acantilado (`LM.13`).
- ⏳ **Deuda para la otra terminal:** anotar el riesgo de que la alarma es un
  control no observado (ver el traspaso al final de esta entrada). ✅ Hecho en
  `S-019`: `A-018` existe.
- ✅ **Mirado en pantalla: la alarma mide coste BRUTO** ("costes sin combinar").
  La premisa contraria de esta terminal era falsa — ver la CORRECCIÓN abajo.
- 🚨 **`T-059` se parte en dos: primero SOLO la Elastic IP, y se espera el correo.**
  La IP ociosa cobra igual y hace falta de todos modos. La instancia va después.
  ⚠️ Y se miran **dos** cosas, no una: el **coste bruto en la factura** (la
  premisa) y **el correo** (la prueba). Con una sola, el silencio es ambiguo.

**Las 14 tareas nuevas del paso 7** (`T-057` a `T-070`, en `tasks.md` de TEAPP).
Las cinco deudas fantasma **por fin tienen dueño**:

| | qué falta |
|---|---|
| ~~`T-057`~~ | ✅ **HECHA** (sesión 46). Cuenta + MFA + alarma. ⏱️ El reloj corre |
| ~~`T-058`~~ | ✅ **HECHA** (sesión 42). `teapp.duckdns.org` existe y resuelve |
| `T-059` · `T-060` | la instancia con IP fija · cortafuegos solo en 80 y 443 |
| `T-061` · `T-062` | Caddy (HTTPS solo) · uvicorn en arranque automático, atado a `127.0.0.1` |
| `T-063` | 📦 la carpeta `deploy/` — **sin Terraform** (PI-2) |
| `T-064` · `T-065` · `T-066` · `T-067` | subir y crear la 1ª cuenta · comprobar el disco · el origen real · el presupuesto real |
| ~~`T-068`~~ | ✅ **HECHA** (sesión 46). Son **siete** puertas, no tres (`A-016` resultó FALSA). En `deploy/console_steps.md:14-39`. Lo que queda es **releerla** antes del primer clic, no escribirla |
| `T-069` | 🚨 **el ensayo de reconstrucción, y va PRONTO** |
| `T-070` | el **cierre planeado** del paso 7 |
| ~~`T-055`~~ | ✅ **la mitad de Python** (sesión 47), medida con uvicorn real. Faltan las dos mitades que **no son código**: que Caddy escriba la cabecera, y `T-060` |
| ~~`T-052`~~ | ✅ **HECHA** (sesión 47). 4 tests, de 310 a 314. `A-009` encogida |
| ~~`T-054`~~ | ✅ **HECHA y MEDIDA** (sesión 48). El tope de Caddy, 5 alfabetos, 14 tests. Queda `A-019`: el entero real de `16KB` vía `caddy adapt`, gratis en `T-061` |
| `T-050` `T-051` `T-056` | las que quedan de las cinco de siempre, ya **escribibles** |
| ~~`T-071`~~ | ✅ **HECHA** (sesión 49). Arreglada en el **origen** (`app/tools.py`), no en los tests, y vigilada por un portero sobre `data/` entera + 6 controles. Eran **tres** maniquíes, no dos. De 328 a 329 tests |
| 🔲 **sin número todavía** | **nueva, salida de la 49**: el camino que escribe en `data/` real **por fuera de pytest** (`A-020`). El portero no lo ve. La mete el cierre de TEAPP |
| 🚨 `T-060` | **subió de categoría en la 47**: no es "un clic de la consola", es **la mitad que sostiene a `T-055`**. Sin ella, `--forwarded-allow-ips` no protege de nada |
| `T-046` | `A-006` — la única que no es de la nube |

---

## 📤 TRASPASO A LA OTRA TERMINAL — sesión 46

> Esto lo produce la terminal que supervisa y lo ejecuta la que construye
> (`LM.4`, `LM.5`). **Son tres cosas, y ninguna es código.**

**1. Un riesgo nuevo en `_persistence/assumptions.md`** — la alarma de facturación
es un **control no observado**:

- Nunca se la ha visto saltar, y **no se puede probar barato**: haría falta gastar
  de verdad y esperar ~24 h. Está montada, probablemente. Nadie lo sabe.
- Con ~24 h de retraso **no puede frenar las 7 puertas de `C-005`**, que evaporan
  los créditos *"en el acto"*. Protege del **goteo**, no del **acantilado**.
- Contra el acantilado el único freno es **`T-068`**, y por eso `T-068` deja de ser
  papeleo: **es el freno**. Debe estar leída antes del primer clic de `T-059`.
- ⏳ **Y hay una calibración gratis que caduca:** con cero máquinas encendidas, si
  la alarma suena hoy es que algo pasa. En cuanto exista la EC2 ese silencio deja
  de significar nada. **Es ahora o no es.**

**2. Una alarma de coste PREVISTO, además de la de coste real que ya existe.**
> ✅ **HECHA y verificada en pantalla (sesión 46, `S-019`).** Comprobado el
> 2026-08-06 en el `progress.md` de TEAPP, no reportado: son **dos alertas en UN
> solo presupuesto** (no dos presupuestos), `ACTUAL` y `FORECASTED`, ambas a
> 0,01 US$ absoluto y al mismo correo. Se dejó anotado aquí como deuda y ya
> estaba pagada: **el bicho de siempre, la misma cosa en dos sitios.**

La que hay es un presupuesto de 1 USD con umbral al 1% — o sea, salta con **1
céntimo** de cargo real, que es lo más cerca de "cualquier cargo distinto de cero"
que AWS deja poner. Está bien. Pero es de **coste real**, y el coste real llega con
~24 h de retraso.
→ Una segunda alerta sobre **coste previsto** avisa *antes* de que el cargo exista,
porque AWS lo proyecta. **No arregla el acantilado** —las 7 puertas siguen sin
aviso posible— pero recorta el retraso en el caso del **goteo**, que es justamente
el único del que esta alarma protege (`LM.13`). Cuesta cero y es un clic.

> ✅ **Comprobado, no supuesto:** `progress.md` y `tasks.md` **ya** dan `T-057` por
> cerrada y ya dicen que lo siguiente es `T-059`. Aquí yo había anotado que
> faltaba; fui a mirarlo y estaba hecho. Las dos menciones que quedan a *"siguiente:
> `T-057`"* viven **dentro de entradas viejas del diario** (`S-016`, `S-017`), que
> es donde deben estar: un diario registra lo que era cierto ese día.

**3. El dato del retraso de facturación está tomado de la documentación, no de la
pantalla** — y el propio `console_steps.md` lo marca honradamente. El paso original
pedía medirlo en la consola (*"no se escribe de memoria — regla 6"*). **No urge, y
se paga gratis:** el día que aparezca el primer cargo real, mirar cuánto tardó en
verse. Ahí el ~24 h deja de ser documentación y pasa a ser medición.

**Lo que NO hay que pasarle, y conviene decirlo:** nada de la auditoría de llaves.
`GUIDE.md` §2.b vive **aquí a propósito** — es la herramienta de la terminal que
vigila, y si la que construye también la corre, vuelve a ser su propio testigo.

---

## 🚨 ADENDA de la sesión 46 (tras `S-019`) — LA ALARMA MIDE LO QUE NO CREÍAMOS

> ⛔ **LA PREMISA DE ESTA SECCIÓN ES FALSA. No la leas suelta.** La métrica NO era
> neta: se miró en pantalla y dice **"costes sin combinar"** (bruta). El error fue
> de esta terminal y está desmontado en la **CORRECCIÓN**, dos secciones más
> abajo. Se conserva entera porque **el razonamiento sí era correcto sobre la
> premisa equivocada**, y porque borrarla escondería cómo se llegó al hallazgo.
> 📌 Este aviso existe por `L-018`: una copia que ya no es cierta y que nadie
> marca es exactamente el bicho de las cinco copias.

**Salió de una frase suya al cerrar**, y por eso está escrita aquí y no perdida:

> *"En los días siguientes, si no llega correo, la alarma está bien montada."*

**Está al revés, y es `LM.13` con otra ropa.** El silencio nunca demuestra que un
control funcione. Pero al ir a comprobarlo apareció algo peor que el razonamiento:
**el mecanismo.** Documentación de AWS, consultada el 2026-08-06:

```
Métrica por defecto de un presupuesto de coste : NET_UNBLENDED_COST
"NET" = DESPUES de aplicar creditos y reembolsos
"AWS Free Tier credits are automatically applied to cover eligible costs
 BEFORE standard AWS billing rates are charged"
```

Con **$200 en créditos**, la cuenta sale sola:

| | mañana, al encender la EC2 |
|---|---|
| la máquina genera coste | ✅ sí, unos dólares al mes |
| los créditos lo cubren | ✅ sí — para eso están |
| coste **neto** resultante | **$0,00** |
| ¿salta el umbral de $0,01? | ❌ **no, y hace bien** |

🚨 **No va a llegar correo — y no llegaría aunque la alarma estuviera rota, aunque
el correo estuviera mal escrito, aunque se hubiera borrado sin querer.** El
silencio está garantizado **por diseño, no por corrección**.

📌 **Es el defecto de los 26 evals verdes con el contrato roto, exacto:** verde
porque no existía nada capaz de ponerlo rojo. → `T-059` **NO comprueba `A-018`**,
al contrario de lo que dice el cierre de `S-019`.

### La consecuencia grande: la alarma no vigila el goteo

Si la métrica es neta, una máquina encendida y olvidada **quema créditos en
silencio durante meses**, y el primer correo llega el día en que los $200 se
acabaron. Cuando avise, ya no queda nada que salvar.

Y ahí `A-015` empieza a doler: dice que el paso 7 gasta *"del orden de $50"* de
los $200 — **por aritmética de lista de precios, no por una corrida**. Ese número
es hoy la única defensa contra el goteo, **y no lo vigila nadie**.

⚠️ **Dos alarmas muy distintas con el mismo nombre**, y hay que mirar en pantalla
cuál es (esta terminal no ve la consola): según esté la casilla de **créditos**,
la alarma dice *"algo empezó a gastar"* o dice *"los $200 se terminaron"*.

✅ **El arreglo, si se confirma:** un segundo presupuesto sobre coste **bruto**
(créditos excluidos), umbral bajo. Ese salta con el primer dólar real, **lo paguen
los créditos o él**. Es el detector del goteo, que hoy no existe.

### Y cómo se comprueba `A-018` de verdad, gratis

No hay que gastar. Un presupuesto **de prueba con el umbral por debajo de lo ya
gastado** dispara la notificación en el siguiente ciclo y **el correo llega de
verdad**: prueba que la dirección es buena, que no cae en spam, y que el mecanismo
anda. Luego se borra.

🔑 **Es el sabotaje de siempre, aplicado a una alarma en vez de a una función: no
se sube el riesgo, se BAJA EL LISTÓN hasta que el control tenga que morder.**
Mismo gesto que poner el vigilante del pool en 15 (sesión 38) y verlo rojo.

### ✅ Lo que se resolvió bien en `S-019`, y no hay que tocar

Decidió **no** abrir entrada en `decisions.md` para lo de meter la alerta prevista
en el mismo presupuesto: el porqué ya está en `console_steps.md`, donde se va a
leer. **Correcto, y por el motivo correcto** — duplicarlo crea dos sitios donde
mañana uno miente. Es el bicho de la sesión 33 y de la 41, cazado ahora en su
propia documentación y no en el código, que es la parte difícil.
📌 Y que el agente **señalara el hueco sin escribirlo** es `LM.3` funcionando: el
archivo tiene dueño, y un agente no firma.

⏳ **El orden de mañana importa, y por eso esto se escribió hoy:** si la EC2 se
enciende antes de arreglar la alarma, **la ventana de calibración se cierra y no
vuelve** (ver `LM.13`).

---

## ✏️ CORRECCIÓN — la métrica es BRUTA, y el error fue de ESTA terminal

**Se miró en pantalla y la pantalla ganó:**

```
Campo "qué mide" del presupuesto : "costes sin combinar"  ← BRUTO
"costes netos sin combinar"      : existe como opción, SIN marcar
Importe utilizado                : 0,00 sobre presupuesto de 1,00
```

🚨 **Mi premisa era falsa.** Escribí *"la métrica por defecto es
`NET_UNBLENDED_COST`"*. Lo que había visto era **un ejemplo** de la documentación
de la API que llevaba ese valor dentro. **Un ejemplo no es un valor por defecto**,
y lo presenté como hecho verificado, con bloque de código y todo.

📌 **Es el `~$0.02` de la sesión 43 y el "Haiku cuesta 5x menos": un número que
salió de una cabeza y no de una medición.** Y lo cometió la terminal cuyo único
trabajo es cazar exactamente eso. → La defensa no falló: **funcionó la de al
lado.** La otra terminal no me creyó, fue a mirar, y trajo la pantalla.

### Lo que la corrección cambia, en las dos direcciones

| | con métrica bruta |
|---|---|
| ¿la alarma vigila el goteo? | ✅ **sí.** El segundo presupuesto que propuse **NO hace falta** |
| ¿`T-059` garantiza silencio? | ❌ no. Al revés: **tiene que sonar** |
| ¿mi paso 3 era ejecutable? | ❌ **no.** Bajar el umbral por debajo de lo gastado **no existe cuando lo gastado es $0,00** |

### ⭐ Y de ahí salió algo mejor que mi propuesta, y lo trajo la otra terminal

**La Elastic IP cobra estando ociosa**, sin instancia — verificado en la
documentación de EC2. Y la Elastic IP **hace falta para `T-059` de todos modos**.

> Se reserva **solo la IP** —lo más pequeño, reversible y ya necesario— y se
> espera el correo. Sin máquina, sin sistema operativo, sin nada que administrar.

🔑 **Es mi paso 3 con la forma correcta: no bajar el listón, sino subir el suelo
lo mínimo imprescindible hasta que el control tenga que morder.** Y convierte
`T-059` de *destructor del experimento* en **el experimento**.

### ⚠️ PERO el experimento aún NO es falsable — el cabo suelto pesa

La otra terminal lo anotó honradamente y luego siguió como si no pesara. Pesa: en
la misma consulta apareció *"750 hours of public IPv4 address usage at no cost"*,
lenguaje del plan viejo (anterior al 2025-07-15). Si esas horas aplicaran, **la IP
ociosa no generaría cargo y el silencio volvería a tener dos significados.**

✅ **El arreglo es la lección del 5b (sesión 12) literal: separar "¿mi control está
bien?" de "¿el mundo está como creo?".** Son dos observaciones, no una:

1. **¿Hubo coste bruto?** → se lee en la **factura**, no en la bandeja. Es la premisa.
2. **¿Llegó el correo?** → es la prueba.

```
coste > $0.01  +  correo    -> A-018 CERRADA, y se mide cuanto tardo
coste > $0.01  +  silencio  -> LA ALARMA ESTA ROTA. Hallazgo grande, y a tiempo
coste = $0.00               -> las horas de IPv4 aplican: experimento no concluyente,
                               pero se aprende algo que hoy nadie sabe, y C-003 queda tocada
```

🚨 **Sin la observación 1, el tercer caso se disfraza del segundo** y se saca la
conclusión contraria. Es el mismo animal que el silencio de ayer, más fino.

### ⚠️ "Va a sonar todos los días" TAMPOCO está medido — y no hace falta

Es la afirmación que sostiene *"hay que subir el umbral"*. **Se fue a comprobar y
no se pudo:** la documentación confirma el retraso de notificación, pero no dice
si una alerta se repite mientras el umbral siga superado o si suena una vez por
período. **No se afirma lo que no se sabe** — es el error que esta terminal acaba
de cometer, no se repite doce horas después.

📌 **Y el experimento que ya se va a correr lo mide gratis:** llegará **un** correo
o llegará **uno cada día**. Observación en vez de razonamiento.

→ **Por eso el umbral NO se toca todavía.** Cambiarlo ahora arreglaría un problema
**predicho**, y de paso destruiría el único experimento capaz de confirmar que
existe. Es el error de forma de ayer con el signo cambiado.

### Lo que sí queda decidido para después del correo

`$0.01` no puede ser el umbral con el que se convive 6 meses, suene una vez o
cien. Y el número que lo sustituya **sale de una división, no de un gusto**:
**$200 ÷ 6 meses ≈ $33 al mes.** Un presupuesto mensual por ahí convierte la
alarma en lo único que hoy no existe: **un vigilante del ritmo de quema de
créditos** — el riesgo real de `A-015`, que nadie mira.

### La frase falsa estaba en CINCO sitios, y la peor era nueva

Al corregir `S-019` aparecieron **cinco copias**: la entrada, la fila del índice,
"Estado actual", `A-018` en dos puntos, y `console_steps.md` paso 1.

🚨 **La peor era de ese mismo día y propia, no heredada:** *"los $200 descuentan,
así que el coste debería quedarse en cero"*, escrito en tono tranquilizador sobre
un presupuesto que, si eso fuera cierto, **no podría saltar nunca**. Y se dijo en
voz alta en vez de arreglarse callando. **Para eso existe el reparto de dos
terminales.**

📌 **Tercera vez con el mismo bicho** (sesiones 33, 41, y ahora): ya no es
casualidad. **En este proyecto los datos se replican solos, y al corregir uno hay
que ir a buscar las copias.** Tocar `progress.md` fuera de turno estuvo bien: una
frase falsa sobre un control de dinero no espera al próximo cierre.

✅ **Y la otra terminal escribió `L-018` sobre esto, aplicándola sobre sí misma:**
la tabla del experimento vive en **un** sitio y `console_steps.md` la **referencia
en vez de copiarla**. Documentar el problema de las copias haciendo una copia
habría sido la sexta. Después corrió el `grep` que la propia lección exige y
**encontró dos copias más ya obsoletas**. Sin el grep se le escapan: **la lección
trae su propio control, que es lo que la separa de un buen propósito.**

---

## 🚦 LAS DOS COSAS DE ANTES DEL CLIC (auditado el 2026-08-06, tercer tramo)

### 1. 🚨 Las 207 líneas estaban SIN COMMITEAR — y eso rompía el experimento

```
git log TEAPP -1 : 23a1ecb (S-019)   ← el trabajo del tramo NO estaba dentro
git status       : 4 archivos modificados, en el arbol de trabajo
```

En un día normal esto es *"commitea al cerrar"*. Hoy no:

> **`A-018` contiene una predicción escrita antes de mirar. Una predicción sin
> commitear no es una predicción: es un borrador que se puede editar después de
> ver el resultado.**

No por mala fe — porque **nadie podrá demostrar que no se editó**, empezando por
él mismo dentro de tres meses. Lo que da valor a esa tabla es el sello de tiempo,
y **el sello lo pone Git, no la buena intención**.

📌 Es lo de los sabotajes de la sesión 12: *"se predijo por escrito ANTES de
correr"*, y por eso el *"salió exacto"* significa algo. **Commit antes del clic.**

### 2. 🚨 LA REGIÓN NO ESTABA DECIDIDA, y la Elastic IP se reserva dentro de una

Buscado en todo TEAPP: `us-east-1` aparece **una sola vez en el repo entero**, y
**no como decisión**:

```
assumptions.md:240
| t3.micro, Linux, us-east-1, $0.0104/hora | ~$7.59/mes |
```

Está **dentro de una tabla de precios de `A-015`**, como insumo de una cuenta.
**No hay ningún `D-xxx` que elija región.** `D-029` eligió AWS, EC2, Caddy,
DuckDNS e IP fija — la región no.

Una Elastic IP se reserva en **la región seleccionada en la consola**. Si no es la
misma en la que se lanzará la EC2, la IP no sirve: hay que soltarla y pedir otra,
**y la nueva no es la misma dirección**, así que `teapp.duckdns.org` habría que
repuntarlo dos veces.

🔑 **Es el bicho de las cinco copias en su forma PREVENTIVA, y por eso vale más
que las otras cinco:** la región está escrita en un sitio (una estimación) y a
punto de decidirse en otro (un desplegable). **La segunda copia nace en el clic.**
Si no coinciden, mañana `A-015` calcula precios de una región donde no hay nada.

→ **Decidirla a propósito y escribirla ANTES de reservar.** Si sale `us-east-1`,
`A-015` ya cuadra. Si sale otra, hay que corregir esa tabla en el mismo acto.

📌 **La lección general, que es nueva:** hasta ahora las copias se cazaban
**después** de divergir. Esta se cazó **antes de que la segunda existiera**. Ese
es el uso barato del catálogo de fallos del que se habló en la sesión 43: no un
chisme, **un detector que sirve en el siguiente proyecto**.

### ✅ Y algo que refuerza la predicción, escrito hace dos días por otro motivo

`A-015` ya decía el 2026-08-05:

> *"le falta un renglón que se sabe que existe: AWS cobra por cada dirección IPv4
> pública, esté o no en uso, del orden de $3-4/mes"*

**La predicción de que la IP ociosa cobra no es de hoy: estaba anotada desde
antes**, por otra razón y sin saber que serviría para esto. Sube la confianza en
el caso `coste > $0.01`. → `D-029` otra vez: **una nota tomada por un motivo que
acaba pagando por otro.**

### El orden acordado antes de tocar la consola

```
1. Commit de los 4 archivos.        <- sella la prediccion
2. Decidir y ESCRIBIR la region.    <- antes del desplegable, no despues
3. Leer la lista de T-068.
4. Reservar SOLO la Elastic IP.
5. Esperar. Mirar FACTURA y BANDEJA, las dos, contra la tabla de A-018.
```

---

## ✅ CIERRE DE LA SESIÓN 46 — el orden se cumplió, y esta vez es DEMOSTRABLE

**Ejecutado por la otra terminal (`S-020`), verificado aquí commit por commit:**

```
10:17  cfba50a  sella la prediccion de A-018   <- ANTES de reservar
10:23  9cc1b72  D-033 elige us-east-1          <- ANTES de tocar el selector
10:29           t=0: se reserva la Elastic IP  (15:29 UTC)
10:30  3ff793e  experimento lanzado, t=0 sellado
10:33  cd20c4d  cierre S-020
```

⭐ **LA COMPROBACIÓN QUE IMPORTABA, y es la novedad del día:**

```
git diff cfba50a 3ff793e -- assumptions.md
-> SOLO lineas anadidas. Ni una linea de la tabla de prediccion, tocada.
```

🔑 **El sello aguanta.** Ayer yo solo podía *pedir* que la predicción se escribiera
antes; hoy **la secuencia la cuenta Git, no el reporte**. Eso convierte la
honestidad del experimento en algo verificable por cualquiera **en vez de en una
cuestión de confianza** — que es exactamente lo que `LM.4` persigue.

### Lo que hizo bien y no se lo pidió nadie

- **La región:** eligió `us-east-1` **contra** el Ohio que traía la consola, y
  `D-033` da el motivo bueno — `A-015` ya calculaba con Virginia, así que Ohio
  obligaba a corregir esa tabla. 📌 **Alineó la decisión con la copia que ya
  existía en vez de crear una segunda.** Y dejó dicho lo que **no** comprobó:
  *"los precios entre regiones NO se compararon"* (regla 6).
- **`console_steps.md` remite a `D-033` en vez de repetir el porqué.** `L-018`
  aplicándose el mismo día que se escribió.
- **Anticipó el hallazgo que esta terminal traía:** que la Elastic IP reservada y
  sin usar **es literalmente el goteo del que avisa `A-018`**. Ya estaba escrito:
  *"si esto se queda aquí olvidado, la entrada que avisaba del goteo lo habrá
  causado"*. Y **no se quedó en prosa**: `T-059` está en 🔄 con *"soltarla o
  asociarla al terminar el experimento"* dentro de la tarea.
  → **Es la diferencia entre una nota y un freno (`LM.13`), aplicada a su propio
  residuo.**
- **No escribió la dirección IP** en un repo público.

### 🚦 T-059 partida en dos — primera vez en el proyecto

La Elastic IP ✅, la máquina ❌. **Se partió porque hay un experimento en medio**,
no por cansancio. La segunda mitad (instancia + asociar la IP + repuntar DuckDNS)
espera a los dos datos.

### Lo que queda vivo y no depende de nadie

```
¿hubo cargo bruto?  -> la FACTURA.  Es la PREMISA.
¿llego el correo?   -> la BANDEJA.  Es la PRUEBA.
```

⏱️ **Con `t=0` sellado a las 15:29 UTC, la diferencia hasta que aparezca el cargo
es el número que sustituye al "~24 h" de documentación.** Esa medición vale más
que el resultado del experimento: **se hace una vez y sirve los seis meses.**

⚠️ Y sigue pendiente el umbral definitivo (**$200 ÷ 6 ≈ $33/mes**), que **no se
toca hasta ver si llega un correo o uno cada día**.

---

## 🏁 BALANCE DE LA SESIÓN 46

**Sin una línea de código, y con la cuenta abierta el mismo día.**

| | |
|---|---|
| lo irreversible | cuenta AWS abierta, MFA probado en 2 dispositivos, **reloj corriendo** |
| lo construido | 2 alertas, región decidida, Elastic IP reservada |
| gastado | **unos céntimos** — los primeros del curso |
| quedan | **185 días y $200** |

### ⭐ Lo que hace este día distinto, y no es el clic

**La terminal que audita se equivocó y la que construye la corrigió con una
pantalla.** Yo afirmé que `NET_UNBLENDED_COST` era el valor por defecto; era un
**ejemplo** de la documentación de la API, y lo presenté como hecho verificado.

📌 **El reparto de dos terminales dejó de ser una jerarquía hoy.** No es "una
manda y otra obedece": es que **ninguna de las dos es fiable sola**, y el mismo
día quedó demostrado en las dos direcciones — yo cacé su frase falsa, ella cazó mi
premisa falsa, y **ninguna de las dos llegó a la consola**.

### Y `L-018` cobró su primera factura antes de que hubiera daño

La región estaba escrita en un sitio (`A-015`) y a punto de decidirse en otro (un
desplegable). **Se cazó antes de que la segunda copia existiera** — no después de
divergir, como las sesiones 33, 41 y las cinco de esta mañana.

🔑 **Esa es la única forma en que un catálogo de fallos vale lo que cuesta:** no
explicando lo que salió mal, sino **impidiendo la siguiente**.

---

📌 **Las cinco fantasma eran la MISMA decisión disfrazada de cinco:** todas eran
*"configurar lo que hay delante"*, y ninguna se podía escribir antes de elegir la
plataforma. Elegirla las desbloqueó todas a la vez. **Por eso el orden fue
decidir en papel primero y abrir la cuenta después** — y hay una razón dura
debajo: **el reloj de 6 meses arranca el día del clic, no el día del despliegue.**
Cada hora dentro de la consola decidiendo es regalo quemándose.

---

# 🧪 LA SESIÓN 42: `T-058` cerrada, y **lo que se dio por no medible se midió en dos segundos**

Sesión corta y de una sola pieza: revisar lo que la otra terminal hizo en **dos
tramos** que esta bitácora no tenía (`S-016` y `S-017`). Ningún código escrito
aquí, ningún gasto de API, y la cuenta de AWS **sigue sin abrirse**.

## Lo que había pasado en la otra terminal

- **`S-016`** — `A-017` nueva: DuckDNS **comprobado** en vez de heredado (existe,
  es gratis, se sostiene con donaciones, y tiene caídas registradas). Y dos
  revisiones seguidas de `install.sh`, que quedaron como una sola lección `L-017`.
- **`S-017`** — `T-058`: `teapp.duckdns.org` creado, token guardado fuera del repo.

## ⭐ HALLAZGO 1 — *"no había nada que correr"* era falso, y el testigo era gratis

La entrada `S-017` cierra la tarea diciendo textualmente:

> *"Verificado: nada que correr — es una cuenta externa, no un artefacto en este
> repo."*

**Sí había qué correr: `nslookup`.** Y tardó dos segundos.

```
nslookup teapp.duckdns.org  → 181.58.xx.xx
```

🔑 **La distinción que se saltó:** ver el nombre en el panel de DuckDNS demuestra
que *el panel te lo enseña*. **No demuestra que el mundo lo resuelva** — que es lo
único que le va a importar a Let's Encrypt cuando vaya a emitir el certificado.
Son dos afirmaciones distintas, y la primera no implica la segunda.

📌 **Es el animal de la sesión 36 otra vez** (*el paso se declaró terminado sin el
único testigo que cuenta*) y el de la 33 (*un control puede cumplirse entero y no
comprobar lo que creías*). Pero con una vuelta nueva y peor: **aquí ni siquiera se
buscó el testigo.** Se decidió de antemano que no existía.

> **La lección, y es la que se lleva el día: "externo" no significa "no medible".**
> Antes de escribir *"no hay nada que verificar"*, la pregunta correcta no es
> *"¿es mío este artefacto?"* sino **"¿qué podría mirar alguien de fuera?"**

## 🚨 HALLAZGO 2 — el nombre publica la IP de su casa

`teapp.duckdns.org` es un nombre **público**. DuckDNS lo rellenó solo con la
dirección desde la que se entró. Se comprobó que son la misma:

```
nslookup teapp.duckdns.org  → 181.58.xx.xx
curl api.ipify.org          → 181.58.xx.xx   ← la IP de su casa
```

**No es una alarma hoy:** el router no reenvía ningún puerto y no hay nada
escuchando detrás. Pero mientras dure hay dos reglas, y la segunda es una tarea:

1. ⚠️ **No abrir puertos en el router de casa.** Hoy el nombre no lleva a ninguna
   parte. Abrir un puerto lo convertiría en **una puerta con la dirección
   publicada**, que es peor que una puerta anónima.
2. 🚨 **Repuntar el nombre en cuanto exista la Elastic IP** (`T-059`).

### ⚠️ Y el hallazgo 2 casi se comete a sí mismo, al escribir esto

Al redactar esta entrada escribí **la IP completa** en este archivo. **Y este
repo también es público.** Se cazó al mirar `git status` antes del commit, y se
enmascaró a `181.58.xx.xx` — el dato que enseña la lección es el prefijo, no los
cuatro octetos.

🔑 **La diferencia entre publicarla en DNS y publicarla aquí:** en DNS es
**efímera** — cambia cuando el proveedor la rote, y desaparece cuando `T-059`
repunte el nombre. **En Git es para siempre**, y queda pegada a su nombre y a su
cara. **Git no olvida:** borrar el renglón mañana no la borra.

📌 Es la regla de `CLAUDE.md` (*"mira qué entra antes de commitear"*) mordiendo
por primera vez en algo que **no era una llave ni un `.env`**. Un dato personal
no necesita parecer un secreto para no querer que sea permanente.

✅ **Y el TTL quitó un riesgo que sí preocupaba: 60 segundos.** Cuando se cambie
la IP en `T-059`, el mundo se entera en un minuto. Un TTL largo habría dejado a
Let's Encrypt mirando la IP vieja durante horas **con el reloj de AWS corriendo** —
justo el recurso que las sesiones 40 y 41 se esforzaron en no quemar.

## ✏️ Corrección pendiente PARA LA OTRA TERMINAL

`S-017` dice que el nombre coincidía con el que esperaban `install.sh`,
`Caddyfile.template` y `console_steps.md`. **`Caddyfile.template` no contiene
ningún nombre**: tiene `DOMAIN_PLACEHOLDER`, y es `install.sh` quien lo sustituye
(línea 177). Los otros dos sí lo nombran.

El efecto es el mismo, pero la frase **manda a buscar el nombre donde no está**.
Es la semilla del bicho de la sesión 33, en pequeño. Dos cosas para el próximo
tramo de TEAPP, y **no las hace esta terminal** (método de las dos terminales):

- Corregir ese renglón de `S-017`.
- Anotar que `T-058` **quedó comprobada por DNS**, no solo declarada.

## Lo que sigue sin estar probado

⚠️ Lo mismo que ayer, sin cambios: **nada de `deploy/` se ha corrido nunca.** El
nombre resuelve, pero no hay máquina, ni certificado, ni Caddy. `T-069` (borrar la
máquina y levantarla solo desde `deploy/`) sigue siendo la prueba que lo dirá.

---

# 🧪 LA SESIÓN 41: `deploy/` escrita antes de abrir la cuenta, y **tres formas del mismo defecto** dentro de quince líneas

**Novena sesión seguida sin escribir producto desde esta terminal**, y la segunda
sin correr un test propio de la app: el día fue **verificar lo ajeno**. Tres
commits en TEAPP (`efd853a`, `cfe074c`, `956ac83`, más `732404a`).
Costo: **$0,00**. La cuenta de AWS **sigue sin abrirse**.

## Lo que pasó, en orden

1. La otra terminal cerró `T-068`: **`A-016` comprobada y FALSA.** Las puertas al
   plan de pago no eran tres, eran **siete**.
2. Esta terminal fue a las tres fuentes y **encontró que una parte del hallazgo no
   estaba en la documentación** (ver abajo). `C-005` se corrigió a media sesión.
3. Se decidió el orden: **`T-063` antes que `T-057`** — escribir `deploy/` antes
   de abrir la cuenta.
4. La otra terminal escribió `deploy/` entera. Esta la revisó y sacó **tres
   defectos**; se arreglaron en `cfe074c`.
5. La revisión del arreglo sacó **un cuarto**, que era el mismo de antes con el
   signo cambiado. `956ac83`.

## ⭐ HALLAZGO 1 — el silencio de un documento no es una respuesta

`C-005` quedó diciendo que solo las dos primeras puertas evaporan los créditos y
que **las otras cinco los conservan**. Fui a comprobarlo y **la documentación no
dice eso**. La frase literal nombra dos:

> *"if you upgrade to paid plan **by joining an AWS Organization or setting up an
> AWS Control Tower landing zone**, your Free Tier credits expire immediately"*

De las otras cinco **no dice ni que se salvan ni que se pierden**. La frase de
"los créditos se aplican a facturas futuras" existe, pero es del **upgrade
manual** — el que haces tú a propósito. Se le había pegado al caso equivocado.

> 🔑 **Y es el MISMO defecto que acababa de matar a `A-016`, un piso más abajo.**
> `A-016` cayó porque **una lista que tiene sentido parece completa**. Esto casi
> cae porque **un documento que no dice "no" parece que dice "sí"**. Las dos
> veces el hecho no salió del texto: salió de la **forma** del texto.

**Cómo quedó:** las cinco desconocidas se tratan **como si evaporaran**. No es
pesimismo, es **denegar por defecto** — la misma regla que está en el código
desde el nivel 4 con `PERMISOS.get(nombre, "prohibir")`.

**Y una corrección de método que salió de paso:** se había escrito que "las tres
fuentes repiten literalmente la misma frase". Cierto para la lista de siete;
falso para el matiz de los créditos — los **Términos**, que son la fuente que
manda porque es la que se firma, solo hablan de Organizations, ni mencionan
Control Tower, y lo dicen peor (*"no longer be able to **use or earn** credits"*).

> 📌 **Tres fuentes que coinciden en un párrafo no coinciden automáticamente en
> el siguiente.** La coincidencia se verifica **por afirmación, no por documento.**

## ⭐ HALLAZGO 2 — el decisivo: **tres formas del mismo descuido en quince líneas**

`deploy/install.sh` terminaba citando el principio del proyecto —*terminado =
visto funcionando*— y **dos líneas después no lo cumplía**: lo único que
comprobaba era `systemctl is-active`, que demuestra que systemd **lanzó** el
proceso, no que la app conteste.

El hueco era **alcanzable y mudo**: uvicorn arranca, revienta medio segundo
después por un `.env` que no puede leer, `Restart=always` lo relanza, y el
`is-active` de la línea siguiente lo ve `active`. El guion imprimía
**"Listo. TEAPP corriendo en…"** sobre una app muerta.

Se arregló. Y **al revisar el arreglo apareció el mismo defecto invertido**:

| | qué miraba | qué le pasaba |
|---|---|---|
| **1. falso verde** | `is-active` | decía verde **sin haber mirado** |
| **2. falso rojo** | `curl` al HTTPS **sin reintentos** | diría rojo **por mirar demasiado pronto** |
| **3. la ruta** | `curl` a `/` | `/me` suena más representativa, y **pararía cada instalación en rojo estando todo bien** |

El 2 es fino: le habían dado **10 reintentos** al `curl` que espera a uvicorn
(segundos) y **ninguno** al que espera a que Let's Encrypt emita un certificado
(decenas de segundos, más si el DNS acaba de crearse).

> 🔑 **La lección, y es de la otra terminal, no mía.** Yo llevé el hallazgo como
> *"falta un bucle"*. Lo que vale es cómo lo escribieron:
>
> **Un falso verde y un falso rojo no son errores opuestos: son el MISMO error
> —no haber pensado *cuándo* es válido preguntar— y por eso el segundo se coló
> mientras se arreglaba el primero.**

**Y lo más incómodo de los tres: el comentario correcto no evitó el fallo, lo
escondió.** Es `L-017` en TEAPP: *un bloque que se declara auditado es un bloque
que nadie vuelve a auditar — y eso incluye a quien lo escribió media hora antes.*
Misma familia que la sesión 33, donde el cierre se recitó entero y el trabajo se
quedó sin subir: **el procedimiento completo, el resultado sin mirar.**

📌 **La regla práctica que quedó escrita:** cuando un comentario prometa que algo
está comprobado, leer lo de debajo con **más** desconfianza, no con menos. Es
donde menos ojos van a mirar.

## Lo que se verificó corriendo, y por qué importó

El `curl` del instalador no me lo creí: **levanté TEAPP en el puerto 8011** y le
pegué el comando exacto.

```
curl -fsS -o /dev/null http://127.0.0.1:8011/     → salida 0   (200)
curl -fsS -o /dev/null http://127.0.0.1:8011/me   → salida 22  (401)
```

El contraste es el hallazgo 3 medido: `-f` convierte un 401 en fallo. La ruta
sostenía el control entero **y no estaba dicho por qué**. Ahora sí.

## El orden del día, que fue una decisión y no una casualidad

Se eligió **escribir `deploy/` antes de abrir la cuenta**, por la lección de la
sesión 40: **el reloj arranca el día del clic**. Escribir el documento de clics
con la cuenta abierta es escribirlo con los 6 meses corriendo, y no necesita nube
para nada. Segundo motivo, más fuerte: **el documento de clics es el guión de
`T-057`** — escrito antes, se entra a la consola a *ejecutar*; escrito después,
se entra a *decidir*, que es justo lo que la 40 sacó fuera de la consola.

**Salió bien:** los cuatro defectos se encontraron y se arreglaron **con el reloj
parado**. En la nube, cada uno habría costado tiempo de una ventana irrepetible.

## Lo que sigue sin estar probado, y hay que decirlo

⚠️ **Nada de `deploy/` se ha corrido nunca — no hay máquina.** "Está todo
escrito" **no es** "está medido". Por eso `T-069` (borrar la máquina y levantarla
otra vez solo desde `deploy/`) va **pronto y no al final**: cuesta céntimos y deja
meses de margen para arreglar lo que falte.

---

# 🧪 LA SESIÓN 40: la plataforma del paso 7, **decidida en papel y sin abrir la cuenta**

**Octava sesión seguida sin escribir producto desde esta terminal.** Y la primera
en que **no se corrió ni un test**: todo el día fue **decidir y verificar**. Esta
terminal aportó **cuatro hechos comprobados contra la documentación** que
cambiaron el plan; la otra los convirtió en `D-029`, `D-030`, `D-031`, `C-003` a
`C-006`, `A-015`, `A-016` y **14 tareas nuevas**. Commit en TEAPP: `790b111`.
Costo: **$0,00**. La cuenta de AWS **sigue sin abrirse**.

## El punto de partida: cero experiencia, y había que decirlo

Él nunca ha trabajado con AWS ni con ninguna nube. No tiene cuenta. **La otra
terminal no lo sabía**, y eso cambiaba cómo explicar el paso entero. Fue lo
primero del mensaje de traspaso.

## ⭐ HALLAZGO 1 — el plan gratuito de AWS **ya no es el que dicen los tutoriales**

🚨 **El 15 de julio de 2025 AWS cambió el modelo.** El famoso "12 meses gratis"
**no existe** para cuentas nuevas. Lo que hay hoy:

| | |
|---|---|
| créditos | $100 al abrir + hasta $100 más = **$200** |
| duración | **6 meses**, o hasta gastar los créditos |
| al terminar | **AWS cierra la cuenta**. 90 días de gracia, luego borrado |
| la tarjeta | 🔑 **no puede cobrar**: *"AWS will not charge your payment method until you upgrade to paid plan"* |

📌 **Eso RECOLOCA la alarma de facturación, no la cancela.** El roadmap la pedía
para proteger la tarjeta. Ahora protege **otra cosa**: los 6 meses y los $200.

## ⭐ HALLAZGO 2 — el disco, que fue lo que decidió la plataforma entera

**`data/` son archivos.** En una máquina local eso no significa nada; en la nube
es el nudo del paso 7, porque casi todo lo moderno da **disco efímero**.

| con disco efímero | cómo se vería |
|---|---|
| reinicio → `accounts.json` desaparece | **se nota en 5 minutos**: nadie entra |
| dos copias → dos `accounts.json` | me registro en una, entro por la otra |
| 🚨 reinicio → **cuota nueva** | **no se nota NUNCA**: la factura del paso 8 habla |

> 🔑 **La tercera es la grave, y por ser la muda.** El freno del paso 6 se
> rompería **sin que nadie le tocara una línea**. Tercera aparición del patrón de
> la sesión 39: *un freno se rompe cambiando lo que lo rodea*.

→ Lambda y Fargate quedaron descartados **por una sola columna**. EC2 ✅.

## ⭐ HALLAZGO 3 — el que **casi mata el despliegue entero**

La otra terminal preguntó si "no tengo dominio" complicaba el certificado, y dijo
tener *"la fuerte impresión, pero es impresión, no dato"* de que Let's Encrypt
rechaza los nombres de AWS. **Se verificó, y era dato:**

```
"The ACME server refuses to issue a certificate for this domain name,
 because it is forbidden by policy."
```

Es política deliberada, con hilos en su foro **desde 2016**. No hay forma de
convencerlo.

> 🚨 **Sin certificado, `T-051` no se cumple y NADIE ENTRA A TEAPP.** La cookie
> `Secure` no viaja por HTTP, y el fallo es **mudo**. Un despliegue entero muerto
> por la política de una autoridad certificadora — **y se descubrió preguntando,
> no desplegando.**

→ Se resuelve con un nombre **gratuito** de DuckDNS. 📌 Su límite era **el dinero,
no el nombre**, y esa distinción valió el despliegue.

## ⭐ HALLAZGO 4 — el freno que se pierde **sin querer**, con clics inocentes

AWS pasa la cuenta al plan de pago **sola** —Organization, Control Tower, Partner
Network— y entonces: **los créditos se evaporan, la tarjeta queda viva, y no hay
vuelta atrás.**

> 🔑 **"AWS no puede cobrarme" no es propiedad de la cuenta: es propiedad del
> PLAN.** Un clic la desactiva entera y desde dentro todo se ve igual. **Cuarta
> aparición del mismo patrón en dos días.**

📌 **Y de ahí salió lo más útil del día, que no es la lista de nombres:** cambió
**el umbral de la alarma**. No es *"avísame si gasto mucho"* — es **avísame ante
CUALQUIER cargo distinto de cero**, porque el primer cargo no nulo significa que
ya se cruzó. 🔑 **Nació de una pregunta que parecía administrativa** (*"¿esto es
realmente gratis?"*) y acabó cambiando la configuración de la primera cosa del paso 7.

## ⚠️ Y un hallazgo que salió AL REVÉS de lo que se temía

La otra terminal avisó, con razón, de que EC2 **consume créditos** (ya no hay
franja de 750 horas) y dedujo: *"el reloj lo marca la resta, no el calendario"*,
y habría que escribir una pieza que apagara la máquina sola.

**Al ponerle números, no aguanta:** ~$7,59/mes × 6 meses + disco ≈ **$50 de $200**.

> 🔑 **Gana el calendario, y sobra un factor de cuatro.** La pieza se descartó
> **por medición, no por pereza.** Tenía razón en el HECHO y se equivocó en la
> CONSECUENCIA — y eso solo se ve poniendo números. Es la lección de la sesión 12
> otra vez: *separar "¿esto es cierto?" de "¿qué se sigue de esto?"*.

⚠️ Quedó como `A-015`, **marcada como suposición**: son precios de lista, no una
factura, y le falta el renglón de la IPv4 pública.

## ⚠️ Tres cosas que la otra terminal devolvió MEJOR de como se las mandaron

| se mandó | volvió |
|---|---|
| *"sé quién escribe `X-Forwarded-For` porque el proxy es mío"* | **falso**. La garantía viene de que **nadie más pueda hablar con FastAPI**: uvicorn en `127.0.0.1` **y** cortafuegos solo en 80/443. **Sin las dos no hay certeza, hay costumbre** |
| *"verificar `deploy/` al apagar"* (`T-070`) | 🚨 **`T-069`: el ensayo va PRONTO, no al final.** Borrar la máquina y levantarla solo desde `deploy/`, **con cinco meses de margen para arreglar lo que falte** |
| *"la lista de puertas al plan de pago"* | **partida en dos**: el **mecanismo** está verificado → `C-005`. El **inventario** no → `A-016`. 🔑 Y de ahí sale cuál capa protege de verdad: como la lista puede estar incompleta, **la alarma pasa a ser la capa principal** — detecta el resultado sin saber la puerta |

## Lo que se verificó desde esta terminal (todo documentación, ninguna corrida)

```
plan gratuito nuevo, 6 meses, $200  : aws.amazon.com/free + FAQ
"no cobra hasta que subas a pago"   : FAQ, literal
upgrades automaticos al plan pago   : FAQ  -> C-005 + A-016
free tier = UNO POR PERSONA         : aws.amazon.com/free/terms -> C-006
Let's Encrypt rechaza AWS EC2       : foro Let's Encrypt, hilos desde 2016
EC2 ya NO tiene franja de 750h      : para cuentas post 15-jul-2025
precio t3.micro ~$7,59/mes          : ⚠️ calculadora de TERCEROS, no AWS -> A-015
forma de TEAPP (data/ en disco)     : leido en la otra carpeta
commit 790b111 de TEAPP             : revisado entero; repo limpio
```

⚠️ **Una fuente devolvió números inventados** ($300, 12 meses) confesando que no
había leído la página. Se descartó. 🔑 **La regla 6 aplica también a lo que dice
esta terminal**, no solo a lo que dice el usuario.

## Las decisiones personales que se tomaron hoy

1. **AWS queda cerrado sin comparar con otras nubes**, y se escribió *por qué*
   para que nadie lo reabra creyendo que se olvidó: es elección **del curso**, no
   del proyecto. Una plataforma que esconda el proxy **contradice el método**.
2. **Un nombre gratis SÍ entra**: su límite es el dinero, no el nombre.
3. **Final planeado** (`T-070`): bajar TEAPP con fecha en el calendario. Cuesta
   lo mismo que no hacer nada — 🔑 **un cierre planeado se aprende y uno
   automático solo se sufre.** 📌 **La cuenta es desechable; `deploy/` no.**
4. **Correo con alias `+aws` y MFA en el `root` el mismo día.** El `root` es la
   llave maestra y **no se puede limitar**; el correo de compras está pensado
   para circular. Son dos trabajos opuestos para un mismo buzón.

## La lección que se lleva el día

> 🔑 **Decidir en papel no gasta reloj.** El regalo empieza a contar el día que
> abres la cuenta, no el día que despliegas. Y encima es **uno por persona en
> toda la vida**: una sola ventana de 6 meses para todo lo que quiera aprender
> de AWS.

Es la hermana de la lección de la 39 (*las deudas se apuntan juntas y no todas
esperan lo mismo*): allí había que **dudar del rótulo**; aquí había que **dudar
de que empezar ya fuera empezar antes**.

📌 **Y una segunda, sobre el método de las dos terminales:** hoy no hubo código
que revisar, así que lo único que esta terminal aportó fue **ir a comprobar**.
Los cuatro hallazgos salieron de negarse a contestar de memoria. 🔑 **Cuando no
hay nada que correr, verificar ES el trabajo.**

---

# 🧪 LA SESIÓN 39: tres deudas del paso 7 pagadas **sin abrir la cuenta de AWS**

**Séptima sesión seguida sin escribir producto desde esta terminal, y la séptima
que vale.** La otra terminal hizo `T-053`, cerró `/register` y remató `T-033`.
Esta aportó **un hallazgo que cambió el alcance del día**, la forma de retirar una
suposición, y las comprobaciones. Commits en TEAPP: `f1b7b3d`, `9306463`,
`1a0f3e7`. La suite pasó de **258 a 310**. Costo: **$0,00**.

## ⭐ EL HALLAZGO DEL DÍA (de esta terminal): el registro abierto **anulaba la cuota**

Vino de una pregunta que parecía de producto —*¿quién puede registrarse?*— y
resultó ser sobre el freno del paso 6:

> 🔑 **Un límite por persona presupone que las personas son caras de conseguir.**
> `quota.py` topa el gasto **por persona y por día**. Si cualquiera puede fabricar
> personas, el tope sigue funcionando perfectamente y **no protege nada**: 200
> cuentas son 200 cuotas. Deja de ser un techo y pasa a ser **una tarifa**.

Y detrás de cada cuota hay llamadas al modelo, en una cuenta de AWS con su
tarjeta. **El curso lleva 39 sesiones a $0,00.** Un registro abierto y la alarma
de facturación del paso 7 no caben en la misma app.

📌 **Lo que hay que llevarse:** el fallo no estaba en `quota.py`, que está bien
escrito. Estaba en **una suposición que nadie escribió** — *"las cuentas las crea
alguien de confianza"*. 🔑 **Un freno se puede romper sin tocarlo, cambiando lo
que hay a su alrededor.**

## La decisión, y por qué NO fue la que yo recomendé primero

Yo dije *"cerrado, con invitaciones"*. Al pasarlo por la regla que el propio
`scope.md` de TEAPP fija para los casos dudosos —*"¿es necesario para que la
tubería funcione en producción? Si no, es v2"*— **las invitaciones no pasan la
regla**: son producto, y este proyecto trata de lo que rodea al agente.

Quedó en **cerrado a secas**: `TEAPP_REGISTRATION_OPEN`, que **por defecto vale
`false`**. La palanca no se estrechó, **desapareció** — desde una petición anónima
ya no se llega ni al `scrypt` ni al archivo.

⚠️ **Y la otra terminal afinó la regla mejor que yo:** el defecto seguro aquí es
`false` y en `cookie_secure()` es `true`. No es incoherencia. **La regla no es
"el defecto es `true`": es DENEGAR POR DEFECTO**, y eso cae de un lado distinto en
cada ajuste. Por eso además abrir exige la palabra exacta `true`: un `yes` mal
escrito **no abre nada**, porque aquí equivocarse abriría la puerta.

## ⭐ La medición que convirtió un requisito en un hallazgo

Yo pedí, como punto de una lista, *"hace falta crear cuentas sin la ruta"*. La
otra terminal **fue a comprobar si `main.py` ya lo hacía** en vez de escribir algo
nuevo — y se colgó. `getpass` en Windows **lee del teclado, no de la entrada
estándar**: sirve a quien está sentado delante, no a un servidor.

> 🔑 **Un freno nuevo cambia qué OTRAS cosas son críticas.** Con `/register`
> abierto, `main.py` colgado era una molestia. Con `/register` cerrado era la
> única puerta, **y estaba tapiada**: en el paso 7 nadie habría podido crear la
> primera cuenta. Eso no se descubre leyendo — se descubre corriéndolo.

→ Nació `create_account.py`: nombre por argumento, contraseña por variable de
entorno, nunca impresa. Verificado de punta a punta con uvicorn: cuenta creada
sin teclado, `POST /register` → **403**, `POST /login` con esa cuenta → **200**.
**La puerta de la calle cerrada, la de servicio abierta.**

## `A-012` no se retiró: **se partió en dos**

Preguntaron si `A-012` (*"nadie prueba contraseñas a la fuerza"*) salía de
`assumptions.md` ahora que existía el tope, y si `D-026` la sustituía.

**Sí a lo primero, no a lo segundo.** Una decisión dice *qué elegimos y por qué*;
una suposición dice *qué damos por cierto, qué se rompe si es falso y cuándo
caduca*. `D-026` no contesta ninguna de las tres.

> 🔑 **Al cerrar una suposición la pregunta no es "¿quién hereda el archivo?" sino
> "¿qué seguimos dando por cierto?".** Lo que no vale es mudar el riesgo a un
> registro que no sabe cargarlo.

Quedó así, y las dos mitades **caducan el mismo día**:
`A-013` = los números 5 y 15 son **predicción, no medida**.
`A-014` = que `request.client.host` sea el origen real **depende de que no haya
nada delante**.

✅ **Y ellos vieron la segunda mitad, que era mejor que la pregunta:** al ir a
retirarla descubrieron que `A-012` **eran dos suposiciones pegadas y solo una se
había resuelto**. Eso es `L-014`.

## ⚠️ Tres verdes que mentían, y las tres cayeron igual

| tarea | el verde | lo que pasaba de verdad |
|---|---|---|
| `T-053` | `Retry-After` parecía faltar | la sonda la buscaba en mayúsculas; el servidor la manda en minúsculas |
| `/register` | test en verde con `logger.info` | con uvicorn la línea **no salía** — el handler de último recurso empieza en `WARNING` |
| `T-033` | el test del log en verde | un fixture no limpiaba: `caplog` repone los handlers, y `basicConfig` no hace nada si la raíz ya los tiene. **El test medía el estado que ponía pytest** |

> 🔑 **Tres veces en un día, y las tres se cayeron al medir en las condiciones de
> verdad.** Ya no es una anécdota: es el método del proyecto. Un test que corre en
> un sitio que no es el sitio real puede estar midiéndose a sí mismo.

Y el tercero trae su propia lección (`L-015`), con dos partes que valen aparte:
1. **Lo delató el par, no el test.** El del estado bueno solo habría seguido verde
   para siempre; fue tenerlo **al lado del estado malo** lo que hizo visible que
   los dos medían lo mismo. → *Un test del estado bueno no demuestra nada si no hay
   uno del estado malo que se comporte distinto.*
2. **La solución fue cambiar de condiciones, no de aserción:** medirlo en otro
   proceso, porque **un intérprete recién arrancado es la única condición honesta —
   es la de uvicorn.**

## Lo que arregló `T-033`, que no es el formato bonito

Hasta la 39 mandaba el handler de último recurso de Python, que **empieza en
`WARNING`**: cualquier `info` no se perdía por poco — **no existía**. La única
forma de que un renglón saliera era subirlo de nivel, **y eso obliga a mentir
sobre su importancia**.

> 🔑 **Un log donde todo es aviso no tiene avisos.** Con el log configurado,
> bajaron a `info` la cuota agotada (*el freno funcionando*) y el registro cerrado
> (*el estado normal de la v1*), y se quedó en `warning` "demasiados intentos",
> que **no describe el sistema funcionando: describe a alguien intentando entrar
> en una cuenta ajena** — y en memoria es el único rastro que sobrevive a un reinicio.

## Los carteles que apuntaban a un mundo que ya había cambiado

Dos hallazgos de esta terminal, pequeños de escribir y del mismo tipo:

1. **El log decía "las cuentas se crean con `main.py`"** — la herramienta que
   acababan de medir que **se cuelga en un servidor**. Y ese renglón existe para
   una sola persona: quien administra y ve un 403 sin explicación. **El único
   mensaje pensado para desatascar a alguien lo mandaba al sitio donde se atasca.**
2. **`L-012`** decía *"`warning` y no `info`, porque se midió"*. Cierto **mientras
   `T-033` no existiera** — y ese mismo renglón acaba de bajar a `info`.

> 🔑 **Al arreglar algo, busca los carteles que lo señalaban.** El registro sigue
> siendo verdad sobre el pasado y mentira sobre el presente, y nadie lo nota hasta
> que alguien lo obedece.

## ✅ LO QUE CORRÍ YO

```
pytest, tres veces en el dia   : 278 -> 301 -> 310 passed
app/login_guard.py             : leido entero; frenos, barrido y candado
/register en app/api.py        : SIN freno (hallazgo) -> luego cerrado y reverificado
T-055 citada en api.py y en
  decisions.md                 : NO EXISTIA en tasks.md (hallazgo) -> creada
T-053 en tasks.md              : seguia en 🔲 (hallazgo) -> a ✅
log_cookie_mode()              : `info` invisible en su rama segura — confirmado
T-033 citada en app/           : 4 sitios doblados esperandola — el argumento para hacerla
git TEAPP al cerrar            : limpio, 3 commits
```

## La lección que se lleva el día

> 🔑 **Las deudas se apuntan juntas y no todas esperan lo mismo.** Siete tareas
> vivían en la lista del paso 7. Tres se podían pagar hoy, en la máquina de casa,
> por $0,00 — estaban ahí **por contagio**, no por calendario. Releer la lista
> valió más que empezar la tarea que tocaba.

Es la hermana de la lección de la 38 (*un freno solo se conoce cuando falla*):
allí había que provocar el escenario malo; aquí había que **dudar del rótulo**.

---

# 🧪 LA SESIÓN 38: el paso 6, y dos fallos que solo aparecen cuando algo va mal

**Sexta sesión seguida sin escribir producto desde esta terminal, y la sexta que
vale.** La otra terminal construyó el paso 6 entero. Esta encontró **cinco
huecos**, y **dos de ellos los midió con sabotajes propios** en vez de razonarlos.
Commits en TEAPP: `499879a` y `9f33182`. Costo: **$0,00**.

## Qué se construyó (la otra terminal)

Los cuatro frenos del paso 6, todos con librería estándar:

| pieza | qué hace |
|---|---|
| `app/quota.py` | cuota por persona y por día, en `data/quota/<nombre>.json` |
| `MAX_SENTENCE_LENGTH` | tope al tamaño de la frase — 422 antes de llegar al tutor |
| `TUTOR_TIMEOUT_SECONDS` | el tutor corre en otro hilo; a los 10 s, 504 |
| el motivo | cada 429 y cada 504 dicen **por qué**, en la respuesta y en el log |

## ⭐ EL MÉTODO DEL DÍA: no discutir el diseño, sabotearlo

Las dos cosas que de verdad valieron no salieron de leer el código con cuidado.
Salieron de **escribir un programa que lo rompiera**.

**Sabotaje 1 — saturar la cola del tutor:**

```
23 peticiones a la vez, tutor colgado, pool de 20 hilos
respuestas                  : {504: 23}
veces que se llamo al tutor : 20
cuota gastada               : 23
=> 3 personas pagaron por un trabajo que NADIE empezo nunca
```

La causa: **`future.result(timeout=)` cuenta desde que se llama, no desde que la
tarea arranca.** El tiempo de espera en la cola se le cargaba a quien esperaba.

**Sabotaje 2 — la medianoche dentro de una sola llamada:**

`spend()` leía el reloj **dos veces** (una en `spend`, otra dentro de
`read_usage`). Con la medianoche en medio: comprobaba el tope contra el día nuevo
y escribía bajo el día viejo. **Cuota gratis, una vez al día, justo a quien esté
practicando a esa hora.**

> 🔑 **Los dos fallos son invisibles cuando todo va bien.** El primero solo existe
> con el servidor lleno; el segundo, un instante cada noche. Ninguna lectura del
> código los habría dado por seguros — y por eso hubo que provocarlos.

## Los otros tres huecos, y uno era de registro

3. **Nada estaba commiteado ni registrado.** Las decisiones y lecciones sí; la
   tarea y el paso, no. Es la trampa de la sesión 37 otra vez.
4. **El marcador subía después del 504:** el hilo del tutor sigue vivo y llama a
   `add_point`. Se **decidió y se escribió**, no se "arregló": el marcador cuenta
   frases practicadas (`A-001`) y esa se practicó.
5. **`/login` sin tope de intentos.** Fuera del alcance del paso — anotado como
   `T-053`, con dueño en el paso 7.

## ⭐ Lo que la otra terminal hizo mejor de lo que se le pidió

1. **El arreglo del cobro es más fino que el diagnóstico.** Yo pedí *"decidan qué
   pasa con la cuota en la cola"*. Ellos vieron que **`future.cancel()` ya sabe la
   respuesta**: devuelve `True` solo si la tarea nunca arrancó. Eso convirtió una
   decisión de política en un dato que el sistema ya tenía.
   → 🔑 **Antes de decidir a mano, mira si el sistema ya sabe la respuesta.**
2. **Encontraron el límite de mi propio freno.** `MAX_SENTENCE_LENGTH` frena el
   gasto, **no la subida**: un cuerpo de 5 MB se sube entero antes del 422. Es
   `T-054`, y salió de ellos.
3. **`warning` y no `info`, porque se midió.** Con uvicorn de verdad: 20 frenazos,
   cero líneas en el log. Y el test pide `WARNING` en vez de bajar el listón con
   `at_level(INFO)` — que habría salido verde con el renglón invisible.

## La razón prestada, y el vigilante que la cuida

El pool se fijó en **40 a mano**, para que no lo decidiera el número de CPUs de la
máquina. Correcto. Pero el 40 seguía apoyado en algo heredado: **es el defecto del
limitador de `anyio`**, la librería que FastAPI usa para las rutas `def`. Lo
verifiqué: hoy vale 40. Y `anyio` **ni siquiera está en `requirements.txt`** —
entra de rebote con `fastapi`.

> 🔑 **Cambiaron un número heredado por uno escrito, pero la RAZÓN del número
> seguía heredada.** Un invariante que se apoya en el defecto de otro necesita
> quien lo vigile, o se rompe en silencio el día que ese otro cambie de versión.

Ahora hay un test que compara los dos números. **Y lo comprobé como se comprueba
un control: rompiéndolo.**

```
con el 40 de verdad      : VERDE
el pool bajado a 15      : ROJO   ← el vigilante muerde
```

## ✅ LO QUE CORRÍ YO

```
suite de TEAPP                      : 258 passed in 13.42s
sabotaje del pool, DESPUES           : 43 peticiones, 40 al tutor,
                                       40 cobradas, 0 pagando por nada
sabotaje de medianoche, DESPUES      : 1 lectura del reloj por spend()  (antes 2)
control del vigilante de anyio       : verde con 40, rojo con 15
anyio.to_thread ... total_tokens     : 40  ← la afirmación del comentario, medida
git status TEAPP                     : limpio
```

## La lección que se lleva el día

> 🔑 **Un freno solo se conoce cuando falla.** Los cuatro frenos del paso 6
> funcionaban en la corrida feliz desde el primer día. Los dos fallos de verdad
> vivían en la cola llena y en el cambio de día — dos sitios donde nadie mira
> hasta que duele. **Leer el código no bastó; hubo que escribir el que lo rompía.**

Es la hermana mayor de la lección de la sesión 37 (*un portero sin sus controles
es la trampa de la que venía a salvarte*): ahí faltaba el control, aquí faltaba
**el escenario malo** en el que el control significa algo.

---

# 🧪 LA SESIÓN 37: `T-047`, y la diferencia entre medir algo y dejarlo medido

**Quinta sesión seguida sin escribir producto desde esta terminal, y la quinta que
vale.** Hoy el trabajo lo hizo la otra terminal entero y bien. Lo que esta aportó
fueron **cuatro correcciones antes del cierre** y **un sabotaje que nadie más podía
hacer**. Commit en TEAPP: `00e9925`. Costo: **$0,00**.

## Qué era `T-047`

`C-001` decía *"la suite no toca la red, y nada de lo que corre en el cierre
tampoco"*. Estaba **escrita y razonada, pero nunca medida**. La forma anotada de
comprobarla era *"desconecta el WiFi y corre `pytest`"*.

La otra terminal la sustituyó por algo mejor: **un portero dentro de Python** que
para todo lo que intente salir de la máquina y deja pasar `127.0.0.1`. Equivale a
apagar el WiFi, pero lo puede correr ella sola y se repite cada día.

## Las cuatro correcciones de esta terminal, y de dónde salieron

Otra vez el mismo método: **abrir el archivo del que hablaba la frase.**

1. **La medición no había quedado escrita.** `git status` en TEAPP: limpio. `T-047`
   en 🔲, `constraints.md` sin tocar, y el portero viviendo en `AppData\Local\Temp\`,
   que Windows borra sola. El trabajo estaba bien hecho **y ya empezaba a evaporarse**.
2. ⭐ **Proponían meter el portero al repo, pero no los controles.** Ellos mismos
   habían escrito que la fila de los controles es lo único que convierte "pasaron"
   en prueba — y esos controles estaban en la carpeta temporal.
3. **El portero mordía menos de lo que decía, y lo comprobé:**
   `socket().connect_ex(('example.com', 80))` devolvió **0** con el portero puesto.
   Salió a internet por la puerta de atrás.
4. **Había una prueba más fuerte y más barata que no usaron:** busqué `requests`,
   `httpx`, `urllib`, `socket`, `aiohttp`, `subprocess` en **todo** el Python de
   TEAPP → **cero coincidencias**. Los 192 no pasaron porque el portero los dejara:
   pasaron **porque nunca hubo nada que interceptar**.

> 🔑 **Un portero en el repo sin sus controles en el repo es exactamente la trampa
> de la que el portero venía a salvarte.** Dentro de tres meses se rompe en
> silencio, la suite sigue verde, y ya no queda nadie que pueda demostrar que muerde.

Es la lección de la sesión 36 un piso más abajo: *si todas las casillas las marca
quien hizo el trabajo, la que faltaba sigue faltando.*

## Las tres cosas que la otra terminal hizo mejor de lo que se le pidió

1. ⭐ **No se fio del primer rojo.** El control de `connect_ex` usaba el nombre
   `example.com`, que pasa por `getaddrinfo` — **ya parcheado de antes**. O sea que
   el rojo podía venir del parche viejo. Lo separó con **IP literal** (`1.1.1.1`),
   y dejó escrito en el docstring **por qué es IP y no nombre**.
   → 🔑 **Un control que se pone rojo por el motivo equivocado es un control verde
   disfrazado.** Y sin la nota, alguien lo "arregla" a nombre en seis meses y rompe
   el control sin verlo.
2. **Añadió un quinto control que no estaba en la orden:** que el portero **deje
   pasar `127.0.0.1`**. Se le pidió que mordiera; nadie pidió que **no se pasara de
   listo**. Un portero que bloquea lo local rompe `TestClient` — y eso se habría
   descubierto por un incendio, no por un control.
3. **Invirtió los controles con `pytest.raises`: verde = muerde.** Mejor que la
   orden de trabajo, que dejaba el veredicto en *"interpreta este rojo"*.
   → 🔑 **Un veredicto que hay que interpretar se interpreta mal el día que hay prisa.**

## Cómo quedó en el repo de TEAPP (commit `00e9925`)

| pieza | qué es |
|---|---|
| `tests/no_network.py` | el portero: `connect`, `connect_ex` y `getaddrinfo` |
| `tests/check_no_network.py` | sus **5 controles**. No se llama `test_*.py`, así que la suite normal no lo recoge — **salen a internet de verdad si el portero falla** |
| `tests/conftest.py` | el enganche: fixture `autouse`, vigila en cada corrida sin que nadie lo pida |

**El diseño del enganche es correcto y vale anotarlo:** fixture `autouse` con
`monkeypatch`, **no** `pytest_configure`. Se deshace solo al acabar cada test y no
depende de desde dónde se lance `pytest`.

## ✅ LO QUE CORRÍ YO, y el sabotaje que faltaba

```
sabotaje dentro de la suite normal : 1 failed, 192 passed   ← el portero SÍ vigila
controles (check_no_network.py)    : 5 passed in 0.11s
suite limpia                       : 192 passed in 5.46s
git status TEAPP                   : limpio
```

**El sabotaje es la comprobación que ninguno de los cinco controles hace.** Quedaba
una afirmación sin testigo: *"vigila en cada corrida, sin que nadie lo pida"*. Metí
un `test_*.py` que sale a internet, corrí `pytest` a secas, y se puso rojo con
`NetworkTouched`. Después lo borré y el repo quedó limpio.
**Ahora sí: 192 verdes significa algo.**

## `C-001` reescrita, y la mitad que no se puede automatizar nunca

La redacción vieja **era falsa desde `D-016`**, cuando el `git push` entró al
protocolo de cierre. La nueva, que es de ellos y es mejor: *"nada sale a internet a
buscar algo que le falta"* — **`npx` es el peligro; `git push` es el trabajo.**

Y quedó **partida en dos mitades de comprobación**, que era el punto más fácil de
dejar borroso:

| mitad | cómo se mide |
|---|---|
| la suite | **automática**, el portero, cada corrida |
| el cierre (`node`, `git`) | **a mano, y para siempre** |

📌 El portero **solo parchea el `socket` de su proceso**. Un subproceso sale por
delante de sus narices y el portero ni se entera. **No es un descuido arreglable:
es cómo está construido**, y está escrito en su docstring.
→ 🔑 *Saber dónde acaba una prueba es parte de tenerla* — la misma idea que el
límite del eval del nivel 5b, tres niveles después.

## ⚠️ El `@` en los títulos de commit: ya cobró una vez

El commit de hoy salió con un `@` colgando en el título por meter **sintaxis de
PowerShell en una shell bash**. Lo enmendaron a tiempo. Pero `git log --all` en
TEAPP da **una coincidencia**: `d6924f8`, de una sesión anterior, que sí quedó.

Cosmético, y no vale reescribir historia por él. **El patrón sí importa**, y lo vio
la otra terminal sola: *no es un tropiezo de hoy, ya pasó antes*.

> 🔑 **Dos veces el mismo error con dos meses de distancia no son dos descuidos: es
> una trampa del entorno que sigue armada.**

→ **Pendiente:** un renglón en `lessons.md` de TEAPP o en el protocolo de cierre —
*el mensaje de commit va por heredoc, y se relee el título antes de confirmar.*

## El dato que se retiró, y por qué está bien retirarlo

Habían presentado *"5,8s con portero contra 7,0s con red"* como si comparara algo.
No compara nada: **no había red que ahorrar**. Lo vieron y lo sacaron antes de que
quedara escrito.
→ 🔑 **Un número que no compara nada es peor que ningún número, porque el lector
supone que sí compara.** Misma familia que el `@`.

---

# 🧪 LA SESIÓN 36: el paso 5, y la casilla que nadie había marcado

**El paso más grande del nivel 7 hasta ahora, y esta terminal no escribió una
línea de producto.** El reparto de las dos terminales funcionó entero: la otra
construyó, esta revisó, y el valor salió tres veces de **ir a abrir el archivo
del que hablaba la frase**.

## Lo que se construyó (la otra terminal)

El nombre **sale del cuerpo de `/practice`**. Ese hueco es el paso entero: quien
practica sale de una cookie firmada y de ningún otro sitio. Tres piezas nuevas,
todas con librería estándar — **cero paquetes añadidos**, así que `C-001` sigue en
pie sin nada que pensar:

| archivo | qué hace |
|---|---|
| `app/accounts.py` | quién existe. `scrypt` con sal por persona, `compare_digest` al comparar |
| `app/sessions.py` | la tarjeta: `hmac` para firmar, caducidad a una semana |
| `app/config.py` | de dónde salen los secretos. Lector de `.env` de doce líneas |

Cookie `HttpOnly` + `SameSite=Lax` + `Secure` configurable. Y se cerró la puerta
de atrás: `main.py` creaba marcadores sin credencial, así que **la terminal pide
contraseña desde hoy**. Un solo almacén de credenciales, no uno por puerta.

## ⭐ LO MÁS IMPORTANTE: el paso se declaró terminado sin el único testigo que cuenta

La otra terminal preguntó: *"¿Lo pruebas en el navegador y me cuentas qué ves?"*.
En el mensaje siguiente, **sin haber recibido respuesta**, escribió: *"El paso 5
está terminado: código, tests, corrida real, prueba negativa y registro"*.

Y la regla del roadmap dice justo lo contrario:

> *"Un paso no está terminado porque el código exista: está terminado **cuando lo
> viste funcionar**."*

Mira la lista de las cinco pruebas. **Las cinco las hizo ella.** El único testigo
que el roadmap pide era el que faltaba.

> 🔑 **Una lista de comprobaciones completa no es lo mismo que una comprobación
> completa. Si todas las casillas las marca quien hizo el trabajo, la que faltaba
> sigue faltando.**

Es la distinción que este archivo ya se reprochaba en la sesión 35 —*"lo comprobé"*
vs *"me lo reportaron"*— y esta vez el atajo iba a cerrar un paso entero. **Se
paró el cierre y se mandó al navegador.** Ahí sí: `document.cookie` no devuelve la
sesión, y `HttpOnly` está marcado.

## El hueco que encontré en los tests, y por qué es de la familia de `L-010`

`tests/conftest.py:38` pone `COOKIE_SECURE=false` con `autouse=True`. En los 192.
Busqué en toda la suite: **la rama `secure=True` no se ejecuta nunca.**

- `cookie_secure()` devuelve `true` cuando la variable no está puesta. **Ese es el
  valor por defecto, el seguro, y no corre en ningún test.**
- En el paso 7 se pone en `true` **en producción**: esa rama estrenará en la nube.

> 🔑 **El camino por defecto es el que menos se prueba, precisamente porque las
> pruebas lo apagan para poder trabajar.**

Ella lo anotó como `A-009` y añadió el parentesco con `L-010` mejor de lo que yo lo
dije: *"las dos veces el hueco no está en lo que el test afirma, sino en lo que ni
se plantea"*.

## Las dos correcciones que evitaron trabajo perdido

1. **Su argumento contra "entrar con Google" era falso.** Dijo que necesita una
   dirección pública de vuelta que no existe hasta desplegar; **Google admite
   `http://localhost`**. El costo real es otro: cuenta de Google Cloud, pantalla de
   consentimiento, secreto de cliente. Se dejó **anotado como argumento falso, no
   borrado** — 🔑 *una decisión correcta sostenida por un motivo malo se cae en
   cuanto alguien comprueba el motivo.*
2. **Su resumen decía "la cookie va `HttpOnly`, `SameSite=Lax` y `Secure`"**, que
   leído solo significa que el navegador la descarta en localhost. El código era
   mejor que la frase: `TEAPP_COOKIE_SECURE=false` en el `.env` local y un aviso en
   el log al arrancar. → 🔑 **un resumen que describe el caso de producción sin
   decir que lo es hace que el lector diagnostique un fallo que no existe.**

## Lo que faltaba en su análisis, y lo encontró el disco

Su análisis describía **cómo se entra**, no **cómo se registra**. Y en
`data/users/` había cuatro marcadores sin dueño: `ana`, `juan`, `maria`, `pedro`,
12 bytes cada uno, escritos entre las **10:44:02 y las 10:44:42** del 3 de agosto.
Cuarenta segundos: no son cuatro personas, es una corrida de `curl`.

Con registro abierto, cualquiera se registra como `juan` y hereda sus puntos —
**el agujero de `D-013` con un formulario delante.** Su respuesta (`D-020`) fue
mejor que mi pregunta:

> 🔑 **Sembrar esas cuentas no obliga a inventarles un dueño: obliga a inventarles
> una contraseña.** Fabricar credenciales válidas sin nadie detrás es lo contrario
> de lo que este paso viene a construir.

Y de ahí salió la regla que cierra el agujero por estructura: **todo marcador nace
junto a su credencial.** Con dos avisos míos que sí hacían falta:

1. **El borrado se deshacía solo.** `add_point` crea el archivo la primera vez, así
   que el primer `curl` de prueba resucitaba `juan.json`. → No era una tarea que se
   completa, era **una condición que solo se estabiliza cuando el registro existe**.
2. **La regla necesitaba decir según qué archivo.** *"El registro rechaza un nombre
   que ya existe"* — ¿existe según `data/users/`, una carpeta que cualquiera llena
   practicando? → 🔑 **la lista de quién existe y la lista de quién tiene puntos no
   son la misma lista, aunque hoy se parezcan.**

## El fallo que los tests no vieron (suyo, y bien contado)

`/logout` devolvía `HTTP 000` contra el servidor real, con los 191 en verde. El
test miraba **el efecto** —la sesión quedó cerrada— y no la respuesta. → `L-010`:
*un test que solo mira consecuencias da por bueno cualquier camino que llegue ahí.*

## El método

Cuarta sesión seguida en que esta terminal no escribe producto y la cuarta que
vale. Hoy el patrón se vio en su forma más limpia: **los tres hallazgos salieron de
abrir un archivo que la otra terminal mencionaba pero no había mirado** —
`conftest.py`, `add_point`, `data/users/` con sus marcas de tiempo.

---

# 🧪 LA SESIÓN 35: `T-049`, y una promesa que casi se escribe en papel

**Otra sesión sin una línea de producto, y la tercera seguida que lo justifica.**
Hoy esta terminal no escribió: **revisó**. Todo el trabajo lo hizo la otra, y el
valor del día salió de una comprobación de treinta segundos.

## El problema, y por qué tenía dos mitades distintas

`T-049`: `protocol-close` escribía `tasks.md` en el Paso 4, pero **dos pasos
posteriores producen tareas** — el control del `.js` y el push. Su resultado
llegaba tarde y no había dónde anotarlo.

La otra terminal lo partió bien, y esa partición es lo que hay que conservar:

| mitad | qué tenía | arreglo |
|---|---|---|
| el `.js` | un **problema de orden** | mover el control: Paso 5b → **Paso 2b** |
| el push | una **imposibilidad lógica** | no se arregla: se **escribe** |

🔑 **La segunda es la que enseña.** Para saber si el push funcionó, el commit ya
tiene que existir — y `tasks.md` va dentro de ese commit. Un segundo commit hereda
el mismo problema con su propio push, y así al infinito.

> 🔑 **Distinguir "está en el orden equivocado" de "no puede estar en ningún
> orden" es la mitad del trabajo.** Lo primero se reordena. Lo segundo, si lo
> tratas como pendiente, se queda de pendiente para siempre y parece un olvido.

## ⭐ LO MÁS IMPORTANTE: la promesa que se apoyaba en un comando que nadie miró

Su arreglo de la segunda mitad decía: *"la sesión siguiente lo recoge leyendo
`git status -sb` al arrancar"*. La frase **sonaba completa**.

Fui a mirar si era verdad. **`protocol-start` no leía `-sb`: leía
`git status --short`.** Y lo medí en un repo de mentira, con un commit sin subir
a propósito:

```
=== git status --short  (lo que leía protocol-start) ===
[vacío — no vio nada]

=== git status -sb ===
## master...origin/main [ahead 1]
```

`--short` **no imprime la línea de la rama**. Los dos listan los archivos sueltos,
y por eso se parecen; pero un commit sin subir le resulta **invisible** al primero.

> 🔑 **Una promesa cruzada entre dos archivos solo vale si vas a leer el otro.**
> Si se hubiera escrito tal cual, el cierre habría quedado entero, en verde, y el
> trabajo sin salvar. Es `L-006` por tercera vez, con disfraz nuevo.

Y es, literal, el corolario que salió ayer: **cuando corrijas una regla, pregunta
quién más la dice.** La regla vivía en dos archivos y se iba a tocar uno.

## Lo que la otra terminal hizo mejor de lo que se le pidió

1. **No dio por buena la medición: la volvió a correr.** Y la dejó escrita en
   `[L-009]` **con la corrida detrás**, no con la conclusión sola.
2. **Escribió la dependencia donde vive**, avisando al que la vaya a romper:
   *"si algún día alguien cambia ese comando, esta promesa se convierte en papel"*.
   → 🔑 **Una nota que solo explica el presente se borra en la siguiente limpieza;
   una que le habla al que va a romperla, no.**
3. **Anotó la suposición que nace al mover el control** (`A-007`): entre la
   comprobación y el `git add` no se toca ningún `.ts`. Hoy es cierto, pero ahora
   está escrito — la familia de `C-001`.
4. **Dejó el nombre viejo documentado.** El control se llamó "Paso 5b" dos días y
   ese nombre está en `decisions.md`, `tasks.md` y aquí. En vez de renombrarlo todo,
   una nota: *"se llamaba Paso 5b hasta el 2026-08-04; es el mismo control"*.
   → 🔑 **Renombrar hacia atrás rompe el registro; una nota de equivalencia no.**

## El incidente del `probe/`, que salió bien por el motivo correcto

Su repo de prueba se creó **dentro del proyecto**: el `cd` al scratchpad falló y el
comando siguió corriendo, en silencio. **El cierre lo cazó y lo reportó en "Sin
resolver" en vez de commitearlo.**

Se verificó desde aquí que **nunca entró al historial** (`git log -- probe`, vacío).
Eso no era paranoia: **Git no olvida**, y borrar la carpeta después no lo habría
borrado del historial. La regla de siempre, estrenada en un caso real.

> 🔑 **Un `cd` que falla no detiene el comando que va detrás.** Es la misma familia
> del `for` que devolvía 0 de ayer: **en la shell, el fallo no se propaga solo.**

## Lo que se revisó y estaba bien — y lo que está bien por suerte

Se comprobó que **ningún archivo quedó diciendo `--short` como instrucción**, y que
**los dos agentes no contradicen a las skills** (el fallo de la sesión 33).

⚠️ Pero un matiz que no hay que perder: `session-starter.md` menciona `git status`
**a secas**. Se comprobó qué imprime — y sí muestra `Your branch is ahead...`, o
sea no contradice. **Está bien por suerte, no por diseño**: nadie eligió ese
comando pensando en esto. Cabo anotado, no hace daño hoy.

## El método, otra vez

Tres sesiones seguidas sin producto y las tres han valido. El patrón se repite:
**la otra terminal construye, esta comprueba lo que la otra da por supuesto.** Hoy
el hallazgo entero cabía en dos comandos — y no salió de saber más, sino de **ir a
abrir el archivo del que hablaba la frase.**

---

# 🧪 LA SESIÓN 34: `T-037`, y seis rondas de revisión sobre un control de 8 líneas

**No se escribió una línea de producto.** Se cerró la última deuda del paso 3, y
el camino hasta ahí produjo más lecciones que cualquier sesión de código.

## Lo que se decidió, y por qué no fue un test

`T-037`: el test `test_the_compiled_script_is_served` se llamaba *compiled* y
solo medía *"existe un archivo"*. Un `.js` de hace tres días daba **200
perfecto**.

La pregunta de fondo la contestó la otra terminal, y su argumento es el que
cierra el asunto:

> 🔑 **Si el arreglo no toca el código, la comprobación no estaba mirando el
> código.** Cuando falla un test de los 121, abres el `.py`. Cuando falla este,
> el código está perfecto: corres `npm run build` y commiteas. Es una pregunta
> sobre **el repositorio**, no sobre el programa — la misma familia que
> *"¿hiciste push?"*.

Segunda señal, y apunta igual: **en el servidor desplegado no hay `.ts`.** Una
comprobación que se evapora en producción no hablaba del producto: hablaba de tu
mesa de trabajo.

→ Vive en `protocol-close`, **Paso 5b, antes del `git add`** (`D-017`).

## ⭐ `L-007` — el animal por su **séptima** aparición, y por la cara nueva

Las seis anteriores **medían de menos**: la prueba pasaba con el código roto.
La primera versión de este control **medía de más**:

```
$ diff -r app/static "$OUT"        # con el repo CORRECTO
Only in app/static: index.html
diff exit=1                        ← 🚨 declara "viejo" un .js impecable
```

`diff -r` compara **en las dos direcciones**, y `app/static/` es una carpeta
**mixta**: ahí vive `index.html`, escrito a mano, que ningún compilador genera.

> 🔑 **Una alarma que siempre suena y una que nunca suena fallan igual.** La
> segunda no te avisa; la primera **te enseña a no escuchar**, y se lleva por
> delante tu atención para todo lo demás.

**El arreglo bueno, y el porqué que hay que conservar:** la lista de archivos a
comparar sale de `$OUT`, **la carpeta del compilador**.

> 🔑 **No es una lista negra de excepciones: es que el compilador declara qué le
> toca vigilar.** Un `-x index.html` funcionaba hoy y mentía el día que hubiera
> un segundo archivo. **Una lista negra hay que mantenerla; esta se mantiene sola.**

## 🐛 Dos fallos que detectan, informan, y devuelven éxito

Sobre la versión corregida, medido aquí con dos archivos de mentira:

```
a.js distinto · b.js igual
1c1
< nuevo
--- > viejo              ← la diferencia SÍ se imprime
>>> exit del bucle = 0    ← 🚨 y el bucle dice "todo bien"
```

Un `for` termina con el código del **último** comando, no de *"alguno falló"*.
Y el fragmento acababa en `rm -rf "$OUT"`, que casi siempre funciona: **exit 0
pasara lo que pasara.** El segundo fallo era gemelo — el "freno explícito" del
caso *cero archivos* era un `echo`, que imprime y sigue.

> 🔑 **Un control que reporta el problema sin señalarlo como fallo depende de que
> alguien lea la salida entera** — justo de lo que huíamos. Se arregla con una
> bandera: `|| FALLO=1`.

⚠️ **Y aquí está lo que vale la sesión.** Ese bug **solo aparece con dos o más
archivos generados**. La medición se había hecho con uno.

> 🔑 **El bug vivía en el caso exacto que el diseño presumía manejar, y la prueba
> se hizo en el único caso donde no se manifiesta.**

## ⭐⭐ La lección madre: `L-008` y la mitad que nadie mide

Las **tres** correcciones del día fueron la misma:

| ronda | qué faltaba |
|---|---|
| 1 | la lista de archivos: faltaba `tasks.md`, el archivo donde vive la propia tarea |
| 2 | se comparó la opción rival **en su versión floja** y se le ganó a esa |
| 3 | el control se midió **solo contra el caso bueno** |

> 🔑 **Un control se mide dos veces o no se midió:** que **atrape lo malo** y que
> **deje pasar lo bueno**. Nadie salta la primera mitad. La segunda se salta
> siempre.

Y el remate: **esa lección ya estaba escrita en TEAPP, por la misma terminal, un
paso antes** — `test_normalize_user_accepts_ordinary_names`, con el comentario
*"un validador que rechaza todo también pasaría los tests de arriba"*.

> 🔑 **Saber un principio y aplicárselo a lo que estás escribiendo ahora son dos
> habilidades distintas.** Por eso el arreglo nunca es "acordarse": es meterlo en
> el protocolo.

`L-008` es la de la ronda 2: **argumentar contra la peor versión de la otra
opción no es comparar — es elegir y buscarle razones después.** Y se ve igual
que un análisis.

## Dos decisiones de operación que valen para todo el curso

1. **`D-018` — un control no puede causar un daño mayor que el que previene.**
   Si el `.js` está viejo, el cierre **commitea y sube igual**, con la alarma
   encendida. Un cierre que se planta reproduce `L-006`: el día entero sin
   guardar. *Un `.js` viejo señalado en rojo es una tarea; trabajo sin subir es
   el desastre.*
2. **⛔ No recompilar automáticamente**, ni cuando es obvio. Regenerar el `.js`
   deja el repo correcto y **borra la señal de que se olvidó**.
   → 🔑 **El olvido es la información.**

## La regla que hoy había que obedecer, y ayer había que corregir

El commit `d6924f8` de TEAPP salió con un `@` suelto de primera línea (sintaxis
de PowerShell dentro de Bash — ver `GUIDE.md §3.a`). No se arregló, **y la
decisión fue correcta**: pedía `--amend` + `push --force` sobre algo ya
publicado.

| | letra | espíritu |
|---|---|---|
| sesión 33 — prohibición de `git push` | ❌ lo vetaba | ✅ lo cumplía |
| sesión 34 — prohibición de `--amend` | ✅ lo veta | ✅ **y hace bien** |

> 🔑 **La habilidad no es "seguir reglas" ni "cuestionarlas": es distinguir cuál
> toca.** La señal que lo decide: `push` **solo añade**; `--amend --force`
> **reescribe lo publicado**.

## Errores míos de esta sesión, corregidos

1. **El contador estaba mal en este archivo.** La prosa de la sesión 32 llamaba a
   `T-037` *"un sexto caso"* contradiciendo su propia tabla (donde es el 5). La
   otra terminal lo leyó y creyó que había que renumerar `L-006`.
   → 🔑 **Un contador mal llevado no se equivoca solo: manda a otro a arreglar
   algo que no está roto.** Corregido arriba, con la nota.
2. **Dije que *"la suite corre sin red" estaba anotado***. Estaba anotado **aquí**,
   no en TEAPP. La otra terminal lo comprobó y me corrigió, con razón. De ahí
   salió `C-001`, la primera entrada de `constraints.md`.
   → 🔑 **Una propiedad de la que el proyecto depende y que no está escrita en el
   proyecto no se puede romper a sabiendas, porque nadie sabe que existe.**

## El método, que hoy dio su mejor día

**Seis rondas de revisión cruzada sobre un control de 8 líneas**, y cada una
encontró algo que la anterior no veía. Ninguna salió de saber más: **salieron de
correr las cosas en vez de leerlas.**

Y una técnica nueva que trajo la otra terminal, sin que se le pidiera: **extraer
el bloque de comandos desde el propio `SKILL.md` y compararlo con el archivo que
se corrió.**

> 🔑 **La evidencia tiene que poder decir de qué texto es evidencia.** Una
> medición que no puede señalar el código exacto que midió es una anécdota.

⚠️ **Lo único que quedó a medias:** las corridas del control **fallando**
(B/C/D) no llegaron a `progress.md`. Solo está anotada la verde.
→ 🔑 **Una medición que no llega al registro no existe mañana.**

---

# 🧪 LA SESIÓN 33: el paso 4, y un cierre que se cumplió entero y falló igual

**El día no produjo código en esta terminal: produjo dos revisiones cruzadas.**
Una antes de construir (el análisis del paso 4) y otra después (la verificación).
Las dos encontraron cosas, y la de después encontró la más grave.

## ⭐ LO MÁS IMPORTANTE: `L-006` — la regla se cumplió y el cierre falló

La otra terminal cerró el paso 4 con su commit y su hash: `f015a01`. La regla de
cierre nacida en la sesión 31 decía **"si no hay hash, no hubo cierre"**, y se
cumplió al pie de la letra.

`git fetch` desde aquí: **`origin/main` seguía en `460b04f`.** El paso 4 entero
existía **solo en ese disco**. Un disco roto esa noche se lo llevaba con el
cierre marcado como correcto.

> 🔑 **Un control puede cumplirse entero y no comprobar lo que creías.**
> "Existe un hash" no es lo mismo que "el trabajo está a salvo fuera de esta
> máquina". La regla corregida: **si el hash no está en `origin`, no hubo
> cierre**, y se comprueba con `git status -sb` — si dice `ahead`, no terminaste.

Y fíjate qué animal es: **la comprobación mide algo distinto de lo que su nombre
promete.** Es el mismo defecto de los cinco tests de TEAPP — pero esta vez en el
**protocolo**, no en el código. Sexta aparición, sitio nuevo.

**El arreglo no fue acordarse mejor: fue automatizarlo.** El `session-closer`
hace `push` y comprueba `git status -sb`; si queda `ahead`, lo reporta como
*"sin resolver"* en vez de taparlo.

## 🚨 La regla que fallaba por el otro extremo, y por poco no se ve

Al arreglarlo apareció algo que **casi se escapa**: el agente repetía la lista de
prohibidos **por su cuenta**, en sus propios límites. Arreglar solo la skill
habría dejado **dos fuentes diciendo cosas contrarias de la misma regla** — una
ordenando `push`, otra prohibiéndolo.

Y el fallo de eso no es un error: es obedecer a una de las dos **sin manera de
saber a cuál**, distinto cada vez.

> 🔑 **Una regla escrita puede fallar por los dos extremos.**
>
> | | la letra | el espíritu |
> |---|---|---|
> | `L-006` — *"si no hay hash"* | ✅ cumplida | ❌ el trabajo sin salvar |
> | la prohibición de `git push` | ❌ lo vetaba | ✅ lo cumplía |
>
> `git push` **solo añade** historia. La prohibición decía *"nunca reescribir ni
> borrar"*. Cumplía el propósito entero y la letra lo vetaba igual.

Y el corolario de operación: **cuando corrijas una regla, pregunta quién más la
dice.** Eso no se ve leyendo el archivo que estás editando.

## La revisión de ANTES de construir: cuatro huecos, y uno era serio

Se analizó el paso 4 sin tocar código. El análisis de la otra terminal era bueno
—identificó la lista blanca como el corazón del paso, y bien— pero le faltaban
cuatro cosas:

| # | hueco | por qué importaba |
|---|---|---|
| 🔴 1 | `Juan` y `juan` | Windows **no** distingue mayúsculas y Linux **sí** |
| 2 | `con`, `prn`, `nul`… | son letras: pasan enteros la lista blanca |
| 3 | el hueco de la sesión 11 | el test no puede probar que no se escribió **fuera** |
| 4 | `A-002` cambia de alcance | y nadie lo iba a anotar |

**El 1 es el que valía el día.** Sin normalizar, `Juan` y `juan` son **una**
persona en su máquina y **dos** en la nube del paso 7. Sin ningún error, con
todos los tests en verde, y descubriéndose cuando ya hay archivos escritos —
o sea, migrando datos en vez de cambiando una línea.

> 🔑 **Los bugs que no puedes ver en tu máquina son los caros.** El sistema
> operativo miente distinto en cada sitio, y ninguna prueba local lo destapa.

## Lo que se construyó, y lo que se hizo mejor de lo pedido

Los cuatro huecos entraron enteros, y dos volvieron **mejor planteados**:

- **"Validar los caracteres no es validar el nombre"** pasó de frase suelta mía a
  principio con nombre, escrito en `tools.py` encima de la lista de reservados.
- **`A-002` se marcó 🔻 ENCOGIDA con fecha**, dejando el texto viejo al lado, en
  vez de reescribirse. Una suposición que cambia de alcance en silencio es peor
  que una equivocada: la equivocada al menos avisa cuando falla.
- **El arreglo del test superó lo que pedí.** Yo propuse una línea —comprobar que
  `escapado.json` no existe—. Pusieron tres, y la tercera es la general:
  `assert list(tmp_path.iterdir()) == [users_dir]`, o sea *no apareció **nada***.
  > 🔑 **Comprobar que no pasó *lo que imaginaste* es más débil que comprobar que
  > no pasó *nada*.** Y la versión débil se disfraza de la fuerte.

**Tres decisiones suyas que valen más que el código:**

1. **`respond(sentence, user)` sin valor por defecto.** Un `user="anonimo"` de
   repuesto haría que olvidarse de pasarlo **no diera error**: los puntos se
   irían a un marcador compartido. Es el bug que el paso mata, entrando por la
   puerta de atrás. **Diseñar para que el olvido falle hacia el lado seguro.**
2. **El navegador NO repite las reglas de validación**, y el comentario dice por
   qué: *"lo que corre en el navegador se puede saltar, así que repetirlas aquí
   daría una sensación de freno que no es real"*.
3. **El control que faltaba desde hace cinco defectos:**
   `test_normalize_user_accepts_ordinary_names`, con el comentario *"un validador
   que rechaza todo también pasaría los tests de arriba"*. Un freno que rechaza
   absolutamente todo pasa cada prueba de seguridad y rompe la app. Salió sin que
   nadie lo pidiera.

## De 57 a 121 tests, $0,00, y la cadena de cierre

| | construir | registrar | guardar |
|---|---|---|---|
| paso 1 | ✅ | 🟡 | ✅ |
| paso 2 | ✅ | ✅ | ❌ commit |
| paso 3 | ✅ | ✅ | ✅ |
| paso 4 | ✅ | ✅ | ❌ push → ✅ tras revisión |

**El fallo se sigue corriendo un eslabón cada vez.** Se acabaron los eslabones
del disco local; el siguiente que quede sin comprobar ya es del remoto.

**La revisión cruzada sigue siendo lo más rentable del método**, y hoy dio su
mejor caso: sin ella el paso 4 estaba en un solo disco y nadie lo sabía.

---

# 🧪 LA SESIÓN 32: el paso 3, y la primera vez que se auditó una decisión

**El día no empezó donde terminó.** Arrancó preguntando *"¿cómo configuro CORS?"*
y terminó con CORS **descartado**, la arquitectura auditada, y un agujero del
paso 7 escrito con nombre y fecha. Ninguna de las tres cosas estaba en el plan.

## ⭐ LO MÁS IMPORTANTE DEL DÍA: una tarea que predecía un problema inexistente

La otra terminal leyó `_context/architecture.md`, vio que **contradecía a
`T-029`**, y en vez de obedecer la tarea o ignorarla, **paró y preguntó**.

`T-029` decía: *"Configurar CORS: la pantalla se abrirá desde otro origen"*. Pero
la arquitectura dice que en la nube hay **un solo servidor** y que la pantalla son
*"archivos quietos"*. Un solo servidor sirviendo el HTML y `/practice` = **mismo
origen** = el navegador no tiene nada que bloquear.

**De dónde salió la tarea mala:** la escribió una revisión externa mirando el
código del paso 2, **antes de que existiera pantalla alguna**. Adivinó cómo se
iba a servir el HTML, y adivinó mal.

> 🔑 **Una tarea no describe un problema: puede describir una predicción.** Y una
> predicción hereda las suposiciones de quien la escribió, sin que se vean.

> 🔑 **La mejor configuración de CORS es no necesitar CORS.**

Y el corolario, que es el mismo animal de `L-004` visto por el otro lado:
**antes de arreglar algo, comprueba que está roto.** Configurar un freno para un
problema que no existe es fabricarse el problema.

## 🚨 EL SEGUNDO HALLAZGO, y lo destapó una pregunta suya

Preguntó, sin que nadie lo pidiera: ***"¿debió ser la arquitectura diferente?"***
Esa pregunta —*"¿esto está bien decidido?"* en vez de *"¿cómo lo hago?"*— es el
cambio de nivel que este proyecto venía a enseñar.

La respuesta, leyendo `architecture.md` entero: **la forma es correcta, pero
tiene dos silencios, y uno es caro.**

| silencio | qué falta | costo |
|---|---|---|
| **barato** | no dice **quién sirve** el `index.html` | es el hueco que produjo `T-029`; se cierra escribiendo |
| **caro** 🔴 | no dice **dónde vive `data/`** en producción | toca `app/tools.py` entero en el paso 7 |

El documento dice de `data/` **dónde no va** (a Git, no). No dice **dónde vive**.
En toda la arquitectura no aparece la palabra "base de datos", ni para elegirla
ni para descartarla. Hoy son archivos en el disco porque es lo que salió del paso
1, **no porque se haya decidido**.

Y `assumptions.md` sabía algo que `architecture.md` no: `A-002` ya apuntaba al
paso 7. **El registro de suposiciones iba por delante del documento de diseño.**

> 🔑 **Lo que es barato de deshacer, se decide tarde. Lo que es caro de deshacer,
> se decide temprano.** `architecture.md` aplica esta regla explícitamente con
> React —dice que es *"la única decisión reversible"* y deja escrita **la señal**
> que la revertiría— y no la aplicó con el almacenamiento, que es cara. Se aplazó
> **en silencio**, que es la única forma mala de aplazar.

## 🔴 `A-005` se cayó dos veces, y ese es el patrón que enseña

Se escribieron dos suposiciones. Sobrevivió una:

| | qué pasó | por qué |
|---|---|---|
| `A-004` (mismo origen) | ✅ **nunca llegó a ser suposición** | se decidió el mismo día → nació como `D-011` |
| `A-005` (dónde vive `data/`) | ❌ se perdió **dos veces** | no era del paso 3 |

La segunda vez se perdió **después de señalarla**, con el texto escrito y listo
para pegar. No por descuido: porque el cierre del paso 3 cierra lo del paso 3.

> 🔑 **Lo urgente del paso de hoy siempre expulsa lo importante del paso 7.** Por
> eso las decisiones caras hay que escribirlas el día que se **piensan**, no el
> día que se necesitan. `A-005` es la primera suposición del proyecto que se
> escribe **sin tener trabajo asociado hoy** — las otras cuatro nacieron pegadas
> a algo que se estaba construyendo.

## Lo que se construyó (el paso 3)

- **`index.html` + `frontend/app.ts` compilado con `tsc`** a `app/static/app.js`.
  El fuente en una carpeta, la salida en otra, para que sea imposible confundir
  cuál se edita. `strict: true`.
- **El mismo FastAPI sirve la pantalla** (`StaticFiles` + `GET /`). Mismo origen
  desde el primer día de desarrollo, igual que en la nube.
- **El `.js` compilado se versiona**, contra la costumbre: en la nube corre **un
  solo servicio, en Python**. Si el `.js` no está en Git, el paso 7 sube una
  pantalla que no existe.
- **De 53 a 57 tests**, sin red, **$0,00**.

**Tres detalles que valen más que el código:**

1. **Un comentario que documenta una AUSENCIA.** `api.py` explica por qué **no**
   hay CORS. Casi nadie documenta lo que no está — y es lo que evita que dentro
   de seis meses alguien "arregle" el hueco.
2. **Se consultó la documentación en vez de la memoria, y valió:** `"module":
   "none"` **lo rechazó el compilador** (TypeScript 7 ya no lo acepta).
   → 🔑 *el compilador es la única fuente que no se queda desactualizada.*
3. **`STATIC_DIR = Path(__file__).parent / "static"`** — calculado desde el
   archivo, no desde dónde se lanzó el servidor. Es el mismo patrón que el
   `load_dotenv(Path(__file__)...)` de todo Edu_TripleS, **aplicado solo, sin que
   nadie lo recordara.** Conocimiento que ya es suyo.

## 🐛 `L-005`, y el animal va por su cuarta aparición

El primer test de la pantalla decía `assert "localhost" not in script`.
**Falló con el código correcto:** la palabra estaba en el archivo, dentro del
comentario que explica **por qué no se usa**. El compilador conserva comentarios.

> 🔑 **Cuando un test busca texto dentro de un archivo, el patrón tiene que
> incluir la parte que lo hace código.** `"localhost"` cabe en un comentario;
> `fetch("http` no.

Y esta terminal encontró **un quinto caso** el mismo día:
`test_the_compiled_script_is_served` afirma cubrir el riesgo de `D-012`
(*editar el `.ts` y olvidar compilar*) y solo detecta *"nunca se compiló"*. Un
`.js` de hace tres días pasa con un 200 perfecto. → `T-037`.

> ✏️ **Corregido en la sesión 34.** Esta prosa decía *"un sexto caso"* y
> *"quinta aparición"* arriba, **contradiciendo a la tabla de abajo**, donde
> `L-005` es el 4 y `T-037` el 5. La numeración buena es la de la tabla. El
> error se propagó: la otra terminal lo leyó y creyó que cerrar `T-037` obligaba
> a renumerar `L-006`. **Un contador mal llevado no se equivoca solo: manda a
> otro a arreglar algo que no está roto.**

| # | dónde | qué medía de más |
|---|---|---|
| 1 | paso 0 | el `session-starter` inventó las 3 herramientas |
| 2 | paso 2 | 45 tests que nunca mandaban 2 peticiones juntas |
| 3 | paso 2 | una prueba de carga contra el servidor equivocado (**la cazó él**) |
| 4 | paso 3 | un test que buscaba una palabra y encontraba un comentario |
| 5 | paso 3 | un test que dice cubrir `D-012` y no lo cubre |

> 🔑 El síntoma es siempre el mismo: **la prueba mide algo distinto de lo que su
> nombre promete.** Y solo se descubre preguntándose *qué tendría que pasar para
> que fallara*.

## La cadena de cierre, que por fin llegó al final

| | construir | registrar | guardar |
|---|---|---|---|
| paso 1 | ✅ | 🟡 | ✅ |
| paso 2 | ✅ | ✅ | ❌ no se commiteó |
| paso 3 | ✅ | ✅ | ✅ |

**El fallo se fue corriendo un eslabón cada vez** —registro, commit, push— hasta
que se acabaron los eslabones. Y la regla que lo cerró nació del fallo del
`session-closer` de la sesión 31:

> 🔑 **Si no hay hash, no hubo cierre.** Un protocolo que se lanza no es un
> protocolo que se cumple.

Hoy hubo que revisar **tres veces** desde esta terminal para llegar ahí (después
del paso 3, después del cierre, después del push). Las tres veces faltaba algo
distinto. **La revisión cruzada sigue siendo lo más rentable del método.**

---

# 🧪 LA SESIÓN 31: el paso 2, y la revisión cruzada funcionando

**El método de las dos terminales dio su mejor resultado hasta ahora.** Él
construyó en TEAPP; esta terminal solo leyó, midió y devolvió listas. Salieron
**dos defectos graves que 45 tests en verde no veían**, y los dos se arreglaron
y se volvieron a medir el mismo día.

## Lo que se construyó (el paso 2)

- **`app/api.py`** — FastAPI con una sola ruta, `POST /practice`. Ahí murió
  `input()`: existe únicamente en `main.py`, que ya no es la única puerta.
- **`D-008`: `respond` devuelve tres piezas sueltas** (`TutorReply`) en vez de un
  texto ya armado. 🔑 *El agente manda los ingredientes, no el plato servido.*
  Decisión suya, tomada **antes** de escribir la pantalla — hacerlo en el paso 3
  habría costado el doble.
- **Pydantic como filtro:** un número, un `null` o una lista se paran con 422
  antes de que el agente vea nada. Es *denegar por defecto* aplicado a los datos.
- **De 30 tests a 53**, 0,96 s, sin red, **$0,00**.

## 🚨 EL HALLAZGO: los 45 tests en verde no vieron que 7 de cada 10 peticiones caían

Esta terminal levantó el servidor de verdad y le mandó **50 peticiones a la vez**.
Tres corridas, antes del arreglo:

| | corrida 1 | corrida 2 | corrida 3 |
|---|---|---|---|
| respuestas 200 | 11 | 14 | 19 |
| **fallos 500** | **39** | **36** | **31** |
| marcador (esperado 50) | **8** | **10** | **12** |
| mismo número a 2+ personas | 3 | 4 | 7 |

**Y eran DOS defectos distintos con el mismo síntoma**, que es lo que hace la
lección:

1. **Se peleaban por el archivo temporal.** Todas escribían el mismo
   `score.json.tmp`; Windows cortaba con `PermissionError`. → temporal con
   nombre propio por escritura (`tempfile.mkstemp`).
2. **El hueco entre leer y escribir.** `add_point` lee el total y luego lo
   escribe; entre esas dos líneas otra petición ya leyó el mismo número. → un
   candado que abarca **la lectura y la escritura juntas**.

> 🔑 **La escritura atómica y el candado resuelven cosas distintas.** La atómica
> protege de UNA escritura cortada por la mitad (un corte de luz). El candado
> protege de DOS escrituras pisándose. Tener la primera no te da la segunda —
> y él tenía la primera desde el mismo día, escrita y con test.

**Después del arreglo, 300 peticiones simultáneas, tres corridas:**
`300/300 OK · 0 fallos · marcador exacto · la secuencia 1…300 completa, sin un
hueco ni un repetido · 0 basura .tmp`.

> 🔑 **Un test en verde no dice "el código está bien". Dice "el código está bien
> para lo que este test hace".** `TestClient` manda las peticiones **de una en
> una**: ni un solo test, ni una sola prueba a mano, creó nunca el estado que
> rompía. Con un escritor el código era correcto.

**Y la firma del nivel, quinta vez:** producción no rompió el código. Rompió la
suposición de **"un solo usuario"** — que el roadmap tenía apuntada para el paso
4. Apareció en el paso 2.

## 🚨 EL SEGUNDO DEFECTO: el 500 regalaba la ruta del servidor

Estaba **anotado desde la sesión 30** como el único pendiente explícito del paso
2, y se hizo el paso 2 sin hacerlo. Comprobado con el servidor encendido:

```json
{ "detail": "El marcador C:\\Users\\USUARIO\\...\\TEAPP\\data\\score.json no es un JSON valido (...)" }
```

Y tenía los **dos extremos mal a la vez**: ese 500 contaba de más, y el 500 de la
concurrencia era **mudo** — sin mensaje y sin quedar apuntado en ninguna parte.

**`D-010`, una sola regla para los dos:**

> 🔑 **El detalle completo va al log. Al navegador, un mensaje corto y sin rutas.**

Comprobado después: `{"detail":"El marcador del servidor no se pudo leer..."}`,
sin ruta, sin `score.json`, con el archivo roto intacto — y el mensaje completo
sí en el log del servidor.

## ⭐ LA MEJOR LECCIÓN DEL DÍA ES SUYA, Y NO LA PIDIÓ NADIE: `L-004`

Montó la prueba de carga para validar su propio arreglo. Dio **50 de 50:
perfecto**. Y en vez de darse por satisfecho descubrió que **contestaba el
servidor viejo**, por el puerto ocupado — y que el viejo **también** daba 50 de
50, porque las peticiones de PowerShell no salían lo bastante juntas para
pisarse.

> 🔑 **Antes de fiarte de una prueba, comprueba que falla con el código roto.**
> Una prueba que pasa en los dos casos no está midiendo el arreglo: está dando
> una confianza que no existe.

Es la **tercera vez** en TEAPP que aparece el mismo animal —algo que mide otra
cosa y suena convincente— y la primera que lo caza él solo:

| | qué medía de más | quién lo cazó |
|---|---|---|
| paso 0 | el `session-starter` inventó las 3 herramientas | esta terminal, leyendo el transcript |
| paso 2 | 45 tests que nunca mandaban 2 peticiones juntas | esta terminal, con carga real |
| paso 2 | una prueba de carga que medía el servidor equivocado | **él** |

## 🚨 Y EL TERCER FALLO DEL HARNESS: el `session-closer` no cerró nada

Dijo "cerremos la sesión" a las 18:38:00. El `session-closer` **se lanzó** a las
18:38:09 —está en el transcript `.jsonl`— y el resultado **nunca volvió**: el
archivo termina ahí. No hubo commit, y `progress.md` sigue en "paso 1 de 9".

**Es el segundo defecto del proyecto que sale del harness y no del código**, y
los dos se encontraron igual: leyendo desde aquí el registro de la otra terminal.

> 🔑 **Un protocolo que se lanza no es un protocolo que se cumple.** El
> `starter` inventó porque nadie comprobó lo que leyó; el `closer` no guardó
> porque nadie comprobó lo que escribió. **Lanzar no es terminar** — es la misma
> `PI-4` de su `CLAUDE.md` (*terminado = visto funcionando*) aplicada al harness
> en vez de al código.

⏳ **Sin resolver:** si el `closer` falló, se quedó a medias o lo interrumpió el
cambio de terminal. **El trabajo interno del subagente no queda en el
transcript** — es el mismo hueco anotado en la sesión 30, y ya ha estorbado dos
veces. Vale la pena que el protocolo de cierre **termine imprimiendo el hash del
commit**: si no hay hash, no hubo cierre.

## `assumptions.md` pasó de 0 a 3 — el hábito cuajó

Era *"el archivo que más va a valer"* y cerró vacío los pasos 0 y 1. Hoy tiene
las tres, y las tres son de verdad:

| | qué se da por cierto | cuándo muerde |
|---|---|---|
| `A-001` | el marcador cuenta frases **practicadas**, no correctas | paso 8 |
| `A-002` | el marcador lo escribe **un solo proceso a la vez** | paso 7 |
| `A-003` | lo que se manda al **log** se ve y se puede reconstruir | paso 7 |

📌 **`A-002` hubo que corregirla el mismo día, y ese es el detalle que enseña.**
Nació diciendo *"sin `--workers`"* — cierto, pero es la forma que **se ve venir**.
La que va a pasar de verdad es tener `main.py` abierto en una terminal **y el
servidor en otra**: dos procesos, dos candados. Medido: de 400 puntos llegaron
**169**, con 169 llamadas fallidas.

> 🔑 **Registrar algo no sirve si señala al sitio equivocado.** Es lo mismo que
> el puntero del paso 0, en otra forma: allí el archivo no se abría, aquí el
> aviso apuntaba al peligro improbable. Y el propio `README.md` invitaba a
> romperla, presentando las dos puertas una debajo de otra sin decir que no se
> usan a la vez.

## Lo que quedó anotado y NO se hizo, a propósito

- **`T-033`, el log (paso 7).** Hoy la línea se ve por el *handler de último
  recurso* de Python: sin hora, sin nivel, y solo WARNING o peor. Funciona por
  defecto, **no porque nadie lo haya decidido**. Hoy no aporta arreglarlo; en la
  nube, un log sin hora no sirve para lo que se escribió.
- **`T-029`, CORS (paso 3).** Es lo primero que va a fallar con la pantalla.

---

## 🔑 LA DECISIÓN DE MÉTODO DE LA SESIÓN 30: **dos terminales**

Salió de él, y cambia cómo se trabaja de aquí en adelante:

| terminal | papel |
|---|---|
| **Edu_TripleS** (esta) | **orienta.** Decide, explica, revisa y guarda el porqué |
| **TEAPP** (la otra) | **construye.** Ahí vive el código y se hacen sus commits |

*"Me dices qué hacer y yo te digo cómo va todo."* Esta terminal **no toca TEAPP**
para construir — pero **sí lo lee para revisar**, y eso resultó ser lo más valioso
del día (ver abajo).

📌 Y una consecuencia práctica: **TEAPP se explica solo.** No lleva ni una
referencia al curso, ni vocabulario de niveles. Se le quitó a propósito.

## Lo que se construyó en TEAPP (paso 0 y paso 1)

**Paso 0 — el esqueleto y el protocolo:**
- `CLAUDE.md` **agnóstico** (convención suya): residente solo lo que evita un
  daño; el detalle en `_context/` con una tabla de *"ábrelo cuando…"*.
- `_context/` — `scope.md`, `architecture.md`, `roadmap.md`.
- `_persistence/` — sus 6 archivos, con **formato índice + anclas** (idea suya:
  *"búscala con grep, no leas el archivo entero"*).
- **Dos agentes de Claude Code**, que estaban solo diseñados desde la sesión 28:
  `session-starter` (Haiku, solo lectura) y `session-closer` (Sonnet, escribe
  desde el `git diff`), cada uno con su skill.

**Paso 1 — el agente FALSO en terminal, $0,00:**
- `respond(sentence) -> str` como **enchufe**: `input()` existe en **un solo
  archivo**, `main.py`, que muere entero en el paso 2.
- 3 herramientas: `count_words` (Python puro), `judge_grammar` (falsa),
  `read_score`/`add_point` (marcador en disco).
- **30 tests, 0,07 s, sin red.** El marcador sobrevivió a cerrar la app.
- Convención adoptada: **nombres en inglés, contenido en español**.

## 🚨 EL HALLAZGO DE LA SESIÓN 30: el primer defecto salió del harness, no del código

`session-starter` corrió en frío (`/clear`) y reportó que las tres herramientas
eran *"abrir un archivo, listar archivos y sacar una captura del navegador"*.

**Se las inventó.** Las de verdad son contar palabras, juzgar gramática y el
marcador — y están escritas en `_context/scope.md`.

**La causa era de diseño, no del modelo:** `protocol-start` mandaba leer
`progress.md` y `tasks.md`, y **`_context/` no aparecía en ninguna parte**, ni
obligatorio ni a demanda. Además el freno decía *"no inventes avances, fechas ni
tareas"* — **no decía "no inventes el proyecto"**. El agujero estaba justo donde
rompió.

> 🔑 **Un puntero que nadie sigue es peor que no tener puntero.** Si el agente no
> abre el archivo, no se queda sin la información: **se la inventa**, y suena
> convincente. Es el precio del `CLAUDE.md` agnóstico, y se paga con lecturas
> obligatorias.

**Arreglado:** `_context/scope.md` y `roadmap.md` pasaron a lectura obligatoria,
más la regla *"todo lo que digas sobre QUÉ ES el proyecto tiene que salir de un
archivo que abriste en esta corrida; si no lo abriste, di **no está
registrado**"*.

📌 **Y cómo se encontró:** leyendo el transcript `.jsonl` de la otra terminal
desde aquí. Es el hallazgo de la sesión 28 puesto a trabajar — **el registro que
Claude Code ya escribía sirvió para auditar a un agente**. Con un hueco anotado:
**el trabajo interno del subagente no queda en ese archivo**, así que no se pudo
saber si la invención fue del `session-starter` en Haiku o de la sesión principal
al reescribir el reporte.

## Los tres defectos que encontró la revisión del paso 1

Los tres los encontró **esta** terminal leyendo el código de la otra. Ninguno lo
habría visto quien lo escribió.

1. **`read_score` reventaba con el archivo roto** (`JSONDecodeError` / `KeyError`).
   Se había señalado antes de escribir código —*"ausente no es lo mismo que
   corrupto"*— y quedó a medias. → Arreglado con `ScoreFileError`, y con la regla
   🔑 **nunca sobrescribas un dato que no lograste entender**: `add_point` lee
   antes de escribir, así que con el archivo roto la escritura ni se intenta.
   **Comprobado a mano:** se rompió el archivo, se corrió la app, salió mensaje
   claro sin traceback, y el archivo quedó intacto.
2. **`count_words(None)` → `AttributeError`.** Hoy no molesta; en el paso 2 sí,
   porque FastAPI recibe JSON de internet. → Arreglado con `TypeError` explícito.
3. **El juez falso tapaba una pregunta de diseño:** `respond` suma un punto
   **siempre**, sin mirar el veredicto. ¿El marcador cuenta *frases practicadas*
   o *frases correctas*? Hoy no se nota porque el falso aprueba todo. **En el
   paso 8 se vuelve un bug.** ⚠️ **Quedó SIN registrar en TEAPP.**

> 🔑 **Los dos primeros son el mismo defecto: qué hace el código cuando le llega
> algo que no esperaba.** Y los dos arreglos no hacen que el programa haga algo
> *más* — hacen que **falle mejor**. Eso es casi todo lo que separa un script de
> un producto.

📌 **Y una trampa que él cazó solo, sin que nadie se la señalara:**
`isinstance(True, int)` vale `True` en Python porque `bool` hereda de `int`. Sin
descartarlo, un `{"score": true}` habría pasado por un `1` válido. Es la misma
trampa del nivel 5b, reencontrada por su cuenta.

## ~~⏳ Para el paso 2 — anotado, no arreglado~~ → **RESUELTO en la sesión 31**

🚨 **El mensaje de error trae la ruta absoluta del servidor.** En la terminal es
ayuda: te dice qué archivo abrir. **En el navegador es información regalada**
sobre cómo está organizado el servidor por dentro.

> **El mismo mensaje sirve para dentro y estorba para fuera.** En el paso 2:
> el detalle al log, una versión corta y sin rutas al navegador.

📌 **Cómo terminó:** se hizo el paso 2 **sin hacerlo** —quedó igual— y lo
encontró la revisión de la sesión 31 comprobándolo contra el servidor. Se cerró
con `D-010`. ⚠️ **Anotarlo no bastó**: la nota existía desde la sesión 30 y aun
así se pasó por alto. Lo que lo cazó fue **volver a medirlo**, no releer la nota.

## ~~⚠️ El hábito que no cuajó: `assumptions.md` sigue en cero~~ → **CUAJÓ en la 31** (0 → 3)

```
decisions.md    6 entradas
lessons.md      2 entradas
assumptions.md  0 entradas   ← cerró el paso 0 vacío, y el paso 1 vacío
```

Y es el archivo del que se dijo, al diseñarlo, que sería **el más valioso del
proyecto**. La razón de que se quede vacío es humana: una decisión se siente
terminada y da gusto escribirla; una suposición se siente incómoda.

> 🔑 **`decisions.md` guarda lo que ya resolviste. `assumptions.md` guarda lo que
> te va a morder.** El vacío no es el archivo: es el hábito.

**Suposiciones vivas que deberían estar ahí:** cuántas vueltas del bucle cuesta
una frase · cuántas llamadas cuesta un tema · si el `system` y las skills se
pagan en cada vuelta · los límites reales de la capa gratis de AWS · **y si el
par `starter`/`closer` ahorra algo de verdad, que nadie ha medido.**

## Dos lecciones que TEAPP anotó solo (candidatas a `L7.x`)

- **`L-001`: la consola de Windows no pinta nada fuera de ASCII.** Los 14 tests
  en verde y la pantalla mostrando `TEAPP ? write a sentence`. Su conclusión:
  *un test comprueba lo que la función devuelve, no lo que la persona ve*. Es la
  **tercera vez** que ese error aparece en el curso, y la primera que queda
  escrito como regla.
- **`L-002`: `pip install pytest` no pide "pytest", pide "el más nuevo de hoy".**
  El global tenía 8.1.1 y el entorno nuevo instaló 9.1.1, el mismo día. →
  `requirements.txt` con `==` siempre.

## Lo que decidió la sesión 29 — tres decisiones

**1. Nombre y ruta del proyecto** (arriba). Fuera de este repo, que era el punto.

**2. La pantalla es TypeScript puro** — sin React, sin Next.js, sin Tailwind.
Preguntó él si los tres entraban aquí. Las razones, en orden de peso:
- **Next.js trae su propio servidor de Node** → serían **dos** servidores
  encendidos en AWS en vez de uno, y *la nube cobra por estar encendida*.
- **Una cosa nueva a la vez.** El nivel 7 ya trae cinco (FastAPI, identidad,
  HTTP, AWS, despliegue). React sería la sexta y es un tema entero.
- 🔑 **React sin haber sufrido el problema que resuelve no se entiende.**

📌 Y se le dijo lo que la hace barata: **es la única decisión reversible** de la
lista. Los tres viven **dentro** de la caja "pantalla"; no mueven la llave, no
tocan FastAPI, no tocan el agente. **La señal para que React entre** (v2 o nivel
8): cuando `app.ts` se llene de *"borra esto, pinta aquello, esconde lo otro"*.

**3. Plan Free de AWS** (ver el hallazgo abajo).

## 🚨 EL HALLAZGO DE LA SESIÓN: "12 meses gratis" en AWS **ya no existe**

Cambió a mediados de 2025. **Verificado en la documentación oficial el
2026-08-02** — y es el mejor ejemplo del curso de por qué se verifica: de memoria
yo habría dicho "12 meses gratis" con toda la confianza, y llevaría un año
equivocado. La tabla completa y las fuentes están en el puente.

Hoy una cuenta nueva elige entre **plan Free** (hasta $200 en créditos, **6
meses**, no te pueden cobrar nunca, y al terminar 🚨 **la cuenta se cierra sola**
y pierdes los datos — 90 días para pasarte a Paid) y **plan Paid** (no expira,
pero sí cobra).

> 🔑 **Hasta hoy el tiempo era gratis en este curso.** Un script que no corres no
> gasta. En AWS no: el reloj de 6 meses arranca el día que abres la cuenta.
> **La nube no solo cobra por estar encendida — en el plan Free cobra en tiempo.**

De ahí salen las dos cosas que hay que recordar:
- **Regla: no abrir la cuenta de AWS hasta tener algo que subir.**
- **Se eligió el plan Free**, porque hace la factura **imposible**, no
  improbable: es el `PRESUPUESTO_USD` del nivel 4 impuesto por AWS.

⚠️ **Los créditos de AWS NO pagan a Anthropic.** La API de Claude se sigue
pagando aparte. Se le aclaró para que no se lleve la sorpresa en el paso 8.

⏳ **Sin verificar a propósito:** los límites exactos de los servicios *Always
Free*. AWS los publica en una tabla hecha con JavaScript, ilegible desde aquí, y
**no se escriben de memoria**. Se comprueban en **Billing → Free Tier** de la
consola el día que se abra la cuenta — que además muestra el consumo real.

## El orden de construcción (pieza 7), en una línea

> 🔑 **La tubería completa se construye y se prueba con un agente FALSO. El
> modelo se enchufa al final** (paso 8 de 9).

Y la razón de peso **no es el dinero**: el modelo es la única pieza que no
responde igual dos veces. Sacarlo del camino **es el control del nivel 5**.
Los 10 pasos, con qué suposición mata cada uno, están en el puente.

## ⭐ TODO EL ANÁLISIS ESTÁ EN `07-produccion/README.md`

**No se repite aquí.** Ese archivo es el **puente** al repositorio del proyecto y
guarda las 5 piezas, las 7 decisiones, las 4 suposiciones que producción rompe,
las restricciones, el reparto de archivos entre los dos repos y los dos agentes
de sesión. Léelo al abrir la próxima sesión.

Lo mínimo para orientarse sin abrirlo:

- **El proyecto va en OTRO repositorio**, privado, fuera de este. Aquí queda el
  puente. Razón dura: al desplegar en AWS **se sube lo que hay en el repo**, y a
  ese servidor no tienen por qué viajar 321 KB de bitácora ni las skills de su
  empresa.
- **El proyecto es un agente para practicar inglés escrito** (A1, 3 temas, sin
  voz, 3 herramientas). Salió de una idea propia suya. Se descartó la de
  extractos bancarios: **la primera vez que despliegas, el dato de adentro debe
  ser el más aburrido que tengas.**
- **Arquitectura B decidida** (estaba aplazada desde la sesión 18): FastAPI en el
  servidor, TypeScript en la pantalla.
- **Se adopta su convención `_persistence/`** (6 archivos + protocolos de inicio
  y cierre en el `CLAUDE.md` del proyecto). Es mejor que lo que yo propuse: es el
  mismo principio de los 4 archivos de esta raíz, con más grano fino.

## La firma del nivel, que se repitió cuatro veces

> 🚨 **Producción no rompe el agente. Rompe las suposiciones que el agente tenía
> derecho a hacer.**

Un solo usuario · el historial en una variable · alguien tecleando (`input()`) ·
que existe "la corrida" con su presupuesto. **Las cuatro salieron de leer el
código del 6b, no de teoría.** Por eso `assumptions.md` va a ser el archivo que
más valga en este proyecto.

📌 **Quinta vez, en la sesión 31** (ver arriba): la suposición de *"un solo
usuario"* estaba apuntada para el paso 4 y reventó en el **paso 2**, en cuanto
hubo servidor. **Las suposiciones no esperan al paso donde las anotaste.**

## Hallazgo suelto de la sesión 28, que vale para siempre

**Claude Code ya escribía tu `registro.jsonl`.** Está en
`~/.claude/projects/<ruta-del-proyecto>/*.jsonl`: un `usage` por cada respuesta,
con el modelo al lado. Llevaba 28 sesiones escribiéndose solo.

Y trajo un dato nuevo, medido en una respuesta real de esta sesión:
`input_tokens: 2` contra `cache_read_input_tokens: 336.229`. **Casi todo es
caché** — por eso una sesión larga no cuesta lo que costaría multiplicar 336 mil
por el precio de entrada. ⏳ El factor exacto de ahorro del *prompt caching*
queda **sin verificar**.

📌 Con suscripción los tokens **sí se cuentan** (`/usage`, el transcript, o
telemetría con `CLAUDE_CODE_ENABLE_TELEMETRY=1`). Lo que cambia es el dólar: ahí
es una **estimación** de lo que habría costado por API, no una factura.

📌 Y sigue apartada, para **después del nivel 8**, la tarea de `METODO.md` — que
esta sesión perfiló: será la unión de **su protocolo `_persistence`** con **el
criterio del curso**.

---

# 🎓 NIVEL 6c — TYPESCRIPT. **CERRADO.** Los 7 pasos corridos y medidos.
# Costo del nivel: **$0,1084**.

Sesiones 24, 25, 26, 27 y 28. Carpeta: `06c-typescript/`.
La 25 no gastó nada; la 26 gastó **$0,0284**; la 27 gastó **$0,0739**;
la **28 gastó $0,00** (el paso 6 es solo escritura).

## Lo que se hizo en la sesión 28 — el paso 6, y con él el cierre

- **`LESSONS.md`: bloque `L6c.1` a `L6c.29`**, destilado de los pasos 0 a 5 de
  esta cabecera. Sin huecos, con el *porqué* y sin comandos.
- **`GUIDE.md`: sección nueva §13 — TypeScript.** No tenía **nada** del idioma,
  como se sospechaba. Ahora trae los comandos (`npm install` + `npx tsc` +
  `node dist/...`), la tabla comparada con Python, el `tsconfig.json` real, la
  ruta de **tres** niveles al `.env`, una **tabla propia de errores `TS####`**
  (§13.e), el patrón de estrechar bloques, `leerCiudad` con la unión
  discriminada, `as`, y los tres errores de `async`.
  - Y se le puso el aviso a la tabla de errores del §3: **esa es de Python**;
    los `TS####` están en §13.e.
  - §1 (arrancar sesión) ahora dice que en el 6c **no se activa el `.venv`**.
- ⚠️ **Se verificó el código antes de escribir la guía, no de memoria.** Dos
  cosas no cuadraban con el borrador: `leerCiudad` **no usa** `as Record<...>`
  (el `in` ya basta) y `noEmitOnError` está **comentado a propósito** en el
  `tsconfig.json`, como ejercicio 2. Las dos se corrigieron antes de publicar.
  Es L6c.29 aplicada al material mismo.
- `README.md` de la raíz y del nivel actualizados: el 6c aparece **cerrado**, y
  la fila del mapa decía `06-typescript/` cuando la carpeta es `06c-`.

## Por qué se llama 6c y no 6

El plan decía `06-typescript/`. Se cambió a **`06c`** a petición del estudiante:
después de `05b` y `06b`, una carpeta `06` a secas se lee como si fuera
*anterior*, y el orden de las carpetas debe contar el orden real en que se hizo.

## Antes de tocar código: las 4 capas de la web, explicadas

La sesión empezó con dos dudas conceptuales, y valen la pena anotadas porque la
segunda es **la confusión más común al llegar a la web**:

1. **¿Backend en Python con FastAPI?** Sí. Y no es opcional: la API key **jamás**
   puede estar en el frontend, porque todo lo que llega al navegador el usuario
   lo puede leer. El agente vive en el servidor. FastAPI solo le pone una puerta
   de entrada por internet a funciones de Python que ya existen.

2. **TypeScript / React / Next.js / Tailwind.** No son cuatro opciones de una
   lista: son **cuatro capas** que se usan a la vez.
   - **TypeScript** = el idioma (el único de los cuatro que lo es).
   - **React** = armar la pantalla por piezas reutilizables.
   - **Next.js** = React **más** todo lo que le falta (rutas, servidor, build).
     No es "React o Next": si usas Next, estás usando React.
   - **Tailwind** = solo aspecto. Es la más opcional de las cuatro.

   Y la duda que se resolvió de una vez: **Next.js sí puede hacer backend**,
   pero para él la respuesta es quedarse con FastAPI, porque su agente está en
   Python con 228 evals y un harness de 10 frenos. **Traducir código que ya
   funciona y ya está medido es la peor apuesta que hay.**

## Paso 0 — `00_hola.ts`: TypeScript no corre, se compila

✅ **Corrido por el estudiante**, salida idéntica a la esperada
(`Hola, Juan` + la línea del harness).

### 🚨 El hallazgo del paso 0, que no estaba previsto

Probando el ejercicio 1 —pasarle un número a una función que pide texto— salió
el aviso esperado (`TS2345`). **Pero el programa corrió igual y imprimió
`Hola, 42`.**

`tsc` protestó **y aun así escribió el `.js`**. Node lo corrió sin chistar.

La causa está a la vista en `dist/00_hola.js`: los tipos **no están**.
`const nombre: string = "Juan"` quedó como `const nombre = "Juan"`. El traductor
los leyó, avisó con ellos, y los borró.

- 🔑 **Los tipos son para ti, no para la máquina.** Viven *antes* de correr.
- 🔑 Y la lección que ya se repitió con los evals en verde y con el *"Anotado"*
  sin anotar: **un aviso que no detiene nada es un aviso que se puede ignorar.**

→ Arreglo medido: `noEmitOnError` en `tsconfig.json` deja el proyecto **sin
`dist/`** cuando hay error. Quedó **comentada, como ejercicio 2**, para que él
vea primero el problema.

## Paso 1 — `01_tipos.ts`: los tipos, sobre las formas del agente

✅ **Corrido por el estudiante**, salida idéntica a la esperada (6 líneas).

Se enseñan sobre las formas que él ya escribía en Python como diccionarios
sueltos (`Mensaje`, `Uso`), no con ejemplos de juguete.

### El punto que carga el paso: la unión `"user" | "assistant"`

No dice *"role es un texto"*: dice **qué valores son legales**, y no hay tercero.
En Python `"assistnat"` era un string válido y el error llegaba como **400 de la
API, después de pagar**. Aquí sale del traductor, gratis, y **medido** trae un
regalo:

```
error TS2820: Type '"assistnat"' is not assignable to type '"assistant" | "user"'.
              Did you mean '"assistant"'?
```

**El compilador corrige el typo.** Sabe cuáles son los valores posibles, así que
puede adivinar cuál querías. Ningún error de la API da eso.

- 🔑 **Un tipo no dice "de qué clase es el dato": dice qué valores son legales.**
  Cuanto más estrecho, más errores atrapa gratis.

### Los 3 errores verificados a mano antes de escribirlos en el README

| Ejercicio | Error medido |
|---|---|
| 1 — typo en la unión | `TS2820` + *"Did you mean 'assistant'?"* |
| 2 — `vueltas = "tres"` sin tipo escrito | `TS2322` (la deducción **sí** revisa) |
| 4 — `Mensaje` sin `content` | `TS2741: Property 'content' is missing` |
| 5 — lo mismo pero con `any` | **ningún error.** El typo pasa en silencio |

## Paso 2 — `02_async.ts`: donde Python y TS de verdad se separan

✅ **Corrido por el estudiante** (confirmado en la sesión 25). Sus tiempos:
3033 ms en serie / 1006 ms en paralelo → los mismos **3,0x**. Las 6 líneas
idénticas a las esperadas, incluida la del `catch` que sí atrapa.
⏱️ Tarda ~7 s a propósito: está midiendo. **No llama a la API** — el clima es
simulado, es la regla del 6b (*lo que puedas simular, no lo pagues*).

**La idea:** en Python `client.messages.create(...)` **detiene** el programa. En
JavaScript **nada bloquea nunca**: una función lenta devuelve un **recibo**
(una promesa) en el acto. Es así porque JS nació en el navegador, donde
congelarse habría congelado la página de verdad.

### Los 3 hallazgos medidos

**1. Olvidar `await` no da error.** Da esto, en silencio:

```
1. Sin await  →  [object Promise]
```

En un agente se ve como *"la respuesta llegó vacía"* o como `[object Promise]`
metido en un prompt que sí se paga. Nadie avisa.

**2. `Promise.all` — lo molesto se vuelve la ventaja.** Las mismas 3 llamadas:

| | tiempo |
|---|---|
| En serie (lo que hace Python) | 3.024 ms |
| En paralelo | 1.007 ms |
| | **3,0x** |

**3. 🚨 Un `try/catch` sin `await` adentro no protege nada** — y es peor que no
atrapar: **mata el proceso entero**. El `try` cierra antes de que el error
ocurra. Es la versión JavaScript del *"Anotado"* sin anotar: un freno que se ve
puesto y no frena.

### El error de montaje, que vale como lección

El primer intento no compiló: `error TS2591: Cannot find name 'process'`.
**TypeScript no sabe nada de Node por su cuenta** (el idioma nació en el
navegador). Se agregó `"types": ["node"]` al `tsconfig.json`.
📌 `@types/node` no es código: son **solo las descripciones de tipos** de cosas
que ya existen.

## Paso 3 — `03_primera_llamada.ts`: el primero que cuesta 💰

✅ **Corrido por el estudiante.** Escrito y verificado **sin** llamar a la API;
la única llamada del nivel fue la suya.

| | |
|---|---|
| `stop_reason` | `end_turn` |
| tokens | 53 entrada / **235 salida** |
| costo | **$0,006140 USD** |

El `for` con el estrechamiento funcionó a la primera: imprimió el texto limpio.

Instalado: `@anthropic-ai/sdk` **0.115.0** y `dotenv`. Modelo `claude-opus-5`,
`max_tokens: 2000`. Se consultó la referencia del SDK antes de escribir una
línea, en vez de tirar de memoria.

### La trampa de la ruta, que Python no tenía

En Python el `.env` está **dos** niveles arriba (`parent.parent`). Aquí son
**tres**, y la razón es la del paso 0: **este archivo no es el que corre.**

```
.ts  →  06c-typescript/03_primera_llamada.ts        ← lo que se escribe
.js  →  06c-typescript/dist/03_primera_llamada.js   ← lo que CORRE
```

- 🔑 **En TypeScript la ruta se calcula desde donde corre el `.js`, no desde
  donde vive el `.ts`.** Primera consecuencia práctica de que el idioma se
  compile.

### 🚨 El punto del paso: `content[0].text` NO COMPILA

En Python se leía directo. Aquí, **medido**:

```
error TS2339: Property 'text' does not exist on type 'ContentBlock'.
```

Porque `content` **no es una lista de textos**: es una lista de **bloques**, y
el SDK los declara como una unión —`TextBlock | ThinkingBlock | ToolUseBlock`—
**la misma unión del paso 1, escrita por el SDK en vez de por él**. Hay que
**estrechar** con `if (bloque.type === "text")`.

Y TypeScript tiene razón, porque **ese bug le pasó de verdad**: nivel 1, sesión
1, `max_tokens=30` con Opus, los 30 tokens se fueron en `thinking`, no hubo
bloque `text`, y la pantalla salió vacía sin ningún error (L1.1, L1.2).

- 🔑 **El aviso no es una molestia: es el bug del nivel 1, atrapado antes de
  correr y antes de pagar.**

El ejercicio 2 del paso lo revive a propósito (bajar `max_tokens` a 30).

## Paso 3b — ✅ **SOSPECHA CERRADA Y MEDIDA:** los 235 tokens de salida

Sesión 25. Script: `03b_thinking.ts`. **Costo de la medición: $0,00.**

La sesión 24 dejó abierta una sospecha: que Opus 5 pensara por defecto y que
ese pensamiento se cobrara dentro de `output_tokens`. Se cerró en dos pasos —
primero la referencia oficial del SDK, después la medición.

### El mecanismo — confirmado en la documentación

- **Opus 5 piensa por defecto.** Omitir el parámetro `thinking` **no lo apaga**:
  equivale a `thinking: {type: "adaptive"}`. Es un **cambio respecto a Opus 4.8
  y 4.7**, donde omitirlo sí significaba no pensar.
- Existe un campo `display`, que por defecto vale **`"omitted"`**: el bloque
  `thinking` llega igual, pero **con el texto vacío**. Por eso el `for` del
  paso 3 no vio nada — el bloque estaba ahí, callado y cobrado.
- 🚨 **`max_tokens` es el techo de PENSAMIENTO + RESPUESTA juntos.** Si se ajusta
  al tamaño de la respuesta esperada, el texto se corta a mitad de frase.
  **Es el bug del nivel 1 (`max_tokens=30`, L1.1/L1.2) con otra cara** — y ahora
  se sabe *por qué* pasó.

### El número — medido con `count_tokens`, $0,00

| | tokens |
|---|---|
| texto que se vio | ~176 |
| cobrado por la API | **235** |
| **pensamiento invisible** | **~59 (25% de la factura)** |

Costo de lo invisible: **$0,001475** de los $0,006140 del paso 3.

⚠️ **Advertencia del instrumento, pegada al dato:** `count_tokens` pide un
mensaje completo, no un texto suelto, así que esos 176 incluyen unos pocos
tokens de envoltorio. Es una **cota alta**: el texto pesa eso o un poco menos,
y el thinking es de 59 **o un poco más**.

### ⭐ LA LECCIÓN DE MÉTODO: la hipótesis acertó, MI NÚMERO NO

Escribí *"se pagaron ~100 tokens"*. Fueron **59** — casi el doble de lo real.

Es la **quinta vez** que un número salido de mi cabeza se cae al medirlo:
el *"Haiku cuesta 5x menos"* (nivel 1), la fila inventada (nivel 2), el `~$0.02`
del streaming (nivel 4), el costo del examen (6b), y este.

🔑 **Y por eso funcionó el formato.** Estaba escrito como **sospecha**, no como
dato, así que nadie construyó nada encima. La regla se confirma: *un número
escrito en el material tiene que venir de una corrida, o venir marcado como
estimación.* Marcarlo salva; afirmarlo cuesta.

📌 Corolario nuevo: **la documentación da el mecanismo, no la magnitud.** La
referencia del SDK dijo correctamente *qué* pasaba; el *cuánto* solo salió al
medir. Consultar docs no reemplaza correr el experimento.

## Paso 4 — `04_bucle.ts`: el bucle agéntico 💰 **$0,028375**

✅ **Corrido por el estudiante.** **Eligió el camino (A): escribirlo a mano**,
como se le recomendó. El `toolRunner` del SDK queda pendiente como comparación
(⚠️ está en beta) — es una deuda voluntaria, no bloquea nada.

Las 3 preguntas del nivel 3, traducidas. Patrón confirmado en las tres:
`tool_use` → `end_turn`, **6 vueltas en total**. 3.050 entrada / 525 salida.

### 🚨 El punto del paso: `input` es de tipo `unknown`

En Python `funcion(**bloque.input)` funcionaba porque `input` era un diccionario.
El SDK de TS lo declara `input: unknown`, y leerlo directo **no compila**:

```
error TS18046: 'bloque.input' is of type 'unknown'.
```

Comparado con el error del paso 3 (`TS2339: Property 'text' does not exist`), la
diferencia es de grado de ignorancia: allá el compilador **sabía qué había** y
sabía que `.text` faltaba; aquí **no sabe ni qué hay**.

- 🔑 **`unknown` no es `any`.** `any` decía *"no revises nada"* y dejaba pasar en
  silencio; `unknown` dice *"hay algo y no sé qué es"* y **frena**.
- 🔑 **Los tipos protegen lo que TÚ escribes. Donde entra algo de afuera —el
  modelo, un archivo, internet— los tipos se acaban y empieza la comprobación en
  tiempo de ejecución.** Que es exactamente lo que hacen sus 10 frenos de
  `herramientas.py` (5b) — la novedad no es la idea, es que **el compilador no le
  deja olvidarla**.

Se escribió `leerCiudad(input: unknown)` con 3 comprobaciones (¿objeto y no
`null`? ¿tiene la llave? ¿el valor es string?). ⚠️ El `input === null` no sobra:
en JavaScript `typeof null === "object"`.

### Lo que confirmó la corrida

- **Tokio se recuperó.** La función devolvió **texto**, no una excepción; el
  modelo lo leyó y ofreció las tres ciudades disponibles. Y fue la respuesta
  **más larga de las seis (149 tok de salida)** — *el error lo hizo hablar más,
  no menos.* Regla del nivel 3, revalidada.
- ⚠️ **El freno nunca disparó.** El modelo mandó `{"ciudad": "..."}` correcto las
  3 veces. Es **el freno 3 del 5b otra vez**: un candado que hoy no atrapó a
  nadie y que sigue estando para el día que sí.

## Paso 4b — `04b_tildes.ts`: ✅ **SOSPECHA CERRADA**, y costó $0,00

### El idioma no cambia la factura

Mismo agente, mismas 3 preguntas, contra `03-primer-agente/02_bucle.py`:

| | Python | TypeScript |
|---|---|---|
| entrada | 3.062 | 3.050 |
| salida | 590 | 525 |
| costo | ~$0,030 | **$0,028** |

🔑 **Los tokens los cuenta la API, no `tsc` ni Python.**

### El +5 que no cuadraba

Las vueltas 1 dieron **+5 exacto en las tres** (452→457, 458→463, 452→457).
Sospecha: las **tildes** (el archivo de Python está escrito sin ellas). Pero eso
no explicaba que el número fuera *idéntico* en las tres, si cada pregunta cambió
de forma distinta. Se midió con `count_tokens`, separando los dos sospechosos:

```
menú sin tildes (Python) : 441      Medellín  py=18 ts=21 → +3
menú con tildes (TS)     : 443      Bogotá    py=24 ts=27 → +3
→ diferencia             : +2       Tokio     py=18 ts=21 → +3
```

**Cuadra exacto: +2 (menú) + 3 (pregunta) = +5.** El menú aporta un peaje fijo
en las tres; cada pregunta resultó costar +3 por su cuenta.

### 🔑 El hallazgo que no se esperaba: una tilde NO cuesta un token

| texto | sitios cambiados | tokens de más |
|---|---|---|
| el menú (`Úsala`, `algún`, `Bogotá`) | **3** | **+2** |
| `¿Me llevo... a Bogotá?` (`¿`, `á`) | **2** | **+3** |

No hay regla de *"una tilde = un token"*: depende de cómo el tokenizador parta
esa palabra. **El conteo se mide, no se deduce** (L1 con otra ropa).

### ⚠️ Y lo que NO hay que concluir — anotado a propósito

Son **+5 sobre 457: un 1,1%**; en la corrida entera, **$0,00008**. Y el nivel 5
midió lo contrario en la dirección que importa: el prompt en mal español daba
**respuestas peores** (rioplatense, tú/usted mezclado). Escribir mal para ahorrar
el 1% y pagarlo en calidad es mal negocio.

> 🔑 Lo que vale del hallazgo no es el número: es que **el texto del menú de
> herramientas se paga en CADA vuelta**. Con 3 ciudades da igual; con 20
> herramientas de tres párrafos en un agente de 8 vueltas, la descripción es una
> factura recurrente. *Eso* sí es decisión de ingeniería. Las tildes no.

📌 **Un hallazgo del 1% se cierra, no se actúa.** Saber de dónde salen los +5
vale mucho; cambiar el código por $0,00008 no vale nada.

## Paso 4c — `04c_puerta_trasera.ts`: ✅ el ejercicio 3, hecho. **$0,00**

Era la deuda que dejó la sesión 26: ver qué hace `as` de verdad. Se escribió un
banco de pruebas **sin API** con los 4 `input` que el modelo puede mandar, y las
dos lecturas lado a lado: `leerCiudad()` (comprueba) contra
`(input as { ciudad: string }).ciudad` (jura y no mira).

**Resultado: 4 de 4 contra 1 de 4.** Ninguna de las dos dio un aviso al compilar.

Y los tres fallos **no fallan igual** — eso es lo que enseñó el ejercicio:

```
{}                    → typeof undefined → revienta LEJOS, en obtenerClima()
{"ciudad": 42}        → typeof number    → la firma prometía string. Mintió.
{"ciuadd": "Bogotá"}  → typeof undefined → el más traicionero: el modelo casi acierta
```

- 🔑 **`as` no comprueba, no convierte, no existe.** Se verificó en el `.js`
  compilado: `leerCiudadConAs` quedó en `return input.ciudad;` — las tres
  comprobaciones y el `as` **no están**. Lo único que hace es callar al compilador.
  Detalle bonito: la única vez que aparece `ciudad: string` en el `.js` es dentro
  de un **comentario**. Los comentarios sobreviven a la traducción; los tipos no.
- 🔑 **El daño de `as` no es que falle: es DÓNDE falla.** Miente en un sitio y
  revienta en otro. Es el paso 0 (`Hola, 42`) pero caro.
- 🔑 **Cuándo sí:** cuando el dato es TUYO y sabes algo que el compilador no puede
  saber. Nunca sobre lo que escribió el modelo, un archivo, o internet.

## Paso 5 — `05_frenos.ts`: ✅ **CERRADO Y MEDIDO.** 💰 $0,0739 (dos corridas)

### El cambio de fondo: `string | null` → una unión discriminada

```ts
type Lectura =
  | { ok: true;  ciudad: string }
  | { ok: false; error: string };
```

El paso 4 aplastaba **tres motivos distintos** en un `null`, y el bucle tenía que
inventarse un mensaje genérico. La función *sabía* cuál `if` falló y tiraba ese
dato a la basura.

- 🔑 **Un buen mensaje de error nombra el error Y nombra el arreglo.** La frase
  la produjo él sin que se le pidiera: *"le diría que la llave se llama ciudad,
  no ciuadd"*. Son dos datos, no uno. Cada vuelta que el modelo gasta adivinando
  la paga el dueño del agente.
- 🔑 **No se puede olvidar el caso malo.** `leerCiudad(x).ciudad` directo **no
  compila**. El freno lo pone el idioma, no la disciplina.
- 🔑 **Un mensaje de error solo puede ser tan bueno como lo que tu código se
  molestó en mirar.** Su mejor respuesta (nombrar el typo) no cabía en la función
  vieja: había que leer `Object.keys(input)`, que estaba ahí gratis y nadie miraba.
- ⚠️ **El `if` 1 se quedó sin mensaje en su primera respuesta.** Es el caso raro
  —que no llegue ni un objeto— y es justo el que menos se mira. *Denegar por
  defecto* del 5b: el caso que crees que nunca pasa también necesita su mensaje.
- **Se quitó el `as Record<string, unknown>` del paso 4:** el `in` del freno 2 ya
  le enseña a TS que la llave existe. Sobraba, y se supo por el 4c.

### 🐛 El defecto que salió de PROBAR los frenos, no de leerlos

Con los 7 casos corridos sin API, dos mensajes salieron mintiendo: `null` producía
*"esperaba un objeto y llegó un object"*, porque **`typeof null === "object"`**.
El comentario del freno anunciaba la trampa y el mensaje la olvidaba. Se arregló
con un ayudante `describir()`.

- 🔑 **El mensaje de error es código también, y puede tener el mismo bug del que
  protege.**

### 🚨 EL SABOTAJE: el freno disparó, y el modelo se recuperó 3 de 3

`const SABOTEAR = true` le renombra la llave a `ciuadd` en la vuelta 1. Patrón en
las tres preguntas: `tool_use` → **error** → `tool_use` correcto → `end_turn`.
Nunca se cayó, nunca inventó un dato, nunca se rindió.

| | limpio | saboteado | dif |
|---|---|---|---|
| vueltas | 6 | **9** | +3 |
| entrada | 3.030 | **5.165** | +70% |
| salida | 507 | **809** | +60% |
| costo | $0,027825 | **$0,046050** | **+65%** |

- 🔑 **UN ERROR NO SE PAGA UNA VEZ: SE PAGA EN CADA VUELTA POSTERIOR.** La vuelta 3
  de Medellín pagó **689 tokens de entrada** — más que cualquier vuelta de la
  corrida limpia — porque el historial **todavía lleva adentro el intento fallido**
  (el `ciuadd`, el mensaje de error, la disculpa). Todo eso vuelve a entrar y se
  vuelve a pagar. Es el peso del menú del 5b visto desde otro lado.
- 🔑 **Un candado solo se sabe que sirve rompiéndolo a propósito.** En dos días de
  corridas normales el freno nunca disparó.
- **El caso Tokio encadenó DOS errores distintos** (el del freno + "no tengo datos")
  y el agente manejó los dos. La regla del nivel 3 aguantando bajo presión.
- **Contar es determinista, generar no.** Las vueltas 1 dieron **exactamente** los
  mismos tokens de entrada que el paso 4 (457 / 463 / 457) porque la entrada es
  idéntica; las vueltas 2 cambiaron, porque ahí entra lo que el modelo dijo antes.

### 🐛 DEFECTO MÍO, el 5º de este tipo: precios escritos de memoria

`05_frenos.ts` salió con `$15/$75` por millón. Opus 5 cuesta **$5 / $25**. La
primera corrida imprimió **$0,083475** cuando el costo real era **$0,027825**.

**Se cazó porque no cuadraba con un número que SÍ estaba medido:** el paso 4 dio
$0,028375 con 3.050/525, y esa cuenta solo cierra con 5 y 25. Se verificó contra
la documentación oficial antes de corregir, no de memoria otra vez.

- 🔑 Quinta vez del mismo patrón (*"Haiku cuesta 5x menos"*, la fila inventada del
  nivel 2, el `~$0.02` del streaming, el docstring de `04_streaming.py`).
  **Tener mediciones viejas escritas es lo que hace que las mentiras nuevas se noten.**

## Paso 6 — ✅ **HECHO en la sesión 28.** El detalle está arriba, en la cabecera.

`L6c.1`–`L6c.29` en `LESSONS.md` y la sección **§13 (TypeScript)** nueva en
`GUIDE.md`. Costó **$0,00**.

### Deudas voluntarias que quedan (ninguna bloquea el cierre)

- **El `toolRunner` del SDK nunca se probó** (camino B del paso 4, ⚠️ está en beta).
  Comparar el bucle a mano con el de la librería sigue siendo el mejor ejercicio
  de cierre.
- **El mensaje bueno nunca se comparó contra el genérico.** Se midió que el mensaje
  bueno recupera 3 de 3 en 1 vuelta — **pero no se midió si el genérico del paso 4
  ("falta el parámetro o no es un texto") habría costado más vueltas.** Es el
  experimento que falta para *demostrar* que el mensaje bueno se paga solo; hoy
  solo está razonado. Cuesta una corrida (~$0,046).

### Lo que ya estaba listo desde el paso 3

- `@anthropic-ai/sdk` 0.115.0 instalado, `tsconfig.json` con `strict: true` y
  `"types": ["node"]`, `dist/` en `.gitignore`.
- La ruta al `.env` es `path.resolve(__dirname, "..", "..", ".env")` — **tres**
  niveles, porque corre desde `dist/`.
- El patrón de estrechar bloques ya está escrito y probado en
  `03_primera_llamada.ts`; el bucle usa el mismo con `type === "tool_use"`.

El mapa del nivel está en `06c-typescript/README.md`.

### Decisiones técnicas del nivel

- `node_modules/` es el `.venv` de JavaScript, y aquí **sí es por proyecto**, no
  compartido como el de Python. Es regla de `node`, no decisión nuestra.
- `dist/` se agregó al `.gitignore`: **es resultado, no fuente.** Subirlo
  permitiría que el `.js` y el `.ts` se contradigan.
- Node v25.8.1, npm 11.11.0, TypeScript 7.0.2, `strict: true`.

---

# 🎓 NIVEL 6b — **CERRADO.** Memoria persistente y Skills, terminados y medidos.

Sesión 22 (Skills, $0,1796) + sesión 23 (las lecciones, **$0,00**).

## Lo que se hizo en la sesión 23: se saldó la única deuda del nivel

`LESSONS.md` tenía el bloque del 6b **a medias**: las 17 de Skills escritas
(L6b.30–L6b.46) y las de memoria pendientes. Ya no.

**Escritas L6b.1 a L6b.29**, destiladas de las sesiones 18 a 21 de este archivo.
Cero llamadas a la API. **El bloque del nivel 6b tiene ahora 46 lecciones
seguidas, sin huecos.**

### La decisión de encaje, que vale anotarla

Las candidatas apuntadas sumaban **más de 29** (8 de la sesión 18, 21 de la 19,
y las de la 20 y la 21, que ninguna sesión había numerado). Y el hueco reservado
era exactamente 29, porque **Skills ya estaba escrito desde L6b.30 y renumerarlo
habría roto las referencias**.

→ Se **fundieron las que eran la misma idea con otra ropa**, en vez de dejar
fuera las de las sesiones 20 y 21. Las fusiones:

| quedó | venía de |
|---|---|
| **L6b.4** | política de olvido **+** el tope botando `es contador` |
| **L6b.9** | un eval verde es ambiguo **+** el eval destructivo se ve verde |
| **L6b.10** | el `motivo` que miente **+** *"Anotado"* sin anotar (las dos capas del mismo engaño) |
| **L6b.13** | el peaje fijo del encabezado **+** enseñar cuesta más que dar **+** la predicción gratis |
| **L6b.20** | dónde va la regla **+** prohibir mucho y ordenar poco |
| **L6b.22** | lo que no puede saber se pone **+** el puente de fechas |
| **L6b.27** | un criterio sin evidencia mide mal **+** un criterio nuevo no crea evidencia |
| **L6b.28** | escribir ≠ medir **+** los dos errores de costo del examen |

> **Una lección que se dice dos veces con otras palabras no son dos lecciones.**
> Fundirlas fue más barato que renumerar 17 lecciones ya escritas.

## 🚨 SIGUIENTE PASO: **EL NIVEL 7**

El 6b está cerrado. El orden acordado en la sesión 18 era **6b → 6 → 7**, así que
antes del 7 va el **nivel 6 (TypeScript)**: no trae conceptos nuevos de agentes,
traduce lo que ya funciona, y el navegador del nivel 7 solo habla JavaScript.

📌 Y sigue apartada, para **después del nivel 8**, la tarea de `METODO.md`
(abajo, en su sección).

### Deudas que el nivel 6b deja abiertas (ninguna bloquea)

- Los **dos defectos del prompt** confirmados por el examen: dos hechos en una
  ficha, y narrar el proceso. Se arreglan **el día que se vuelva a correr el
  examen**, no antes (sesión 21).
- **C9 está escrito y nunca corrido.**
- Las **skills nunca se han saboteado**.
- Escritura no atómica en `_escribir()`; el tope bota el más viejo; hay dos
  `agente.py` en el curso.

---

## Lo que se hizo en la sesión 22: SKILLS, de cero a medido

### Las 4 skills (`06b-memoria-skills/skills/`)

| Skill | Qué contiene |
|---|---|
| `reporte-mensual.md` | 5 secciones en orden, redondeos, `cierre-AAAA-MM.md`, nota al pie textual |
| `normas-cambiarias.md` | tramos de 5.000 y 20.000 USD, márgenes 0,4 % / 0,7 %, monedas permitidas |
| `explicar-a-un-cliente.md` | palabras prohibidas y 3 respuestas modelo (la única sin cifras) |
| `cierre-de-ano.md` | una sola tasa para todos los saldos, sección 6, archivo aparte |

Todas rotuladas **⚠️ reglas de una empresa ficticia**. Ninguna se presenta como
normativa colombiana. Y todas llenas de **datos arbitrarios a propósito**: si el
modelo pudiera adivinarlos, no se podría medir nada.

### El código

| Archivo | Qué |
|---|---|
| `skills.py` | **nuevo.** Funciones puras: partir ficha/cuerpo, armar el menú, `leer_skill`. No conoce la API |
| `linea_base.py` | **nuevo.** Las 5 preguntas, en dos modos (`--con` / sin) |
| `agente.py` | menú al SYSTEM, `leer_skill` en TOOLS/FUNCIONES/PERMISOS, freno de doble carga, `menu_skills` como parámetro |
| `skills/*.md` | las 4 |

**228 evals (121 + 107) siguen en verde**, y `memoria.json` quedó byte por byte
igual.

### 🚨 LA LÍNEA BASE, que fue lo primero y hay que insistir en ella

Antes de conectar nada se corrieron las 4 preguntas **sin** skills ($0,0405).
Resultado: **el agente no inventó ni un umbral** — se declaró fuera de alcance
(*"no soy de regulaciones bancarias, pregunte en su banco"*) o pidió más datos.

Eso probó lo único que había que probar antes de gastar: **las skills tienen
algo que aportar.** Es el error del *"¿qué es una variable?"* de la sesión 3,
evitado esta vez **comprobando** en vez de suponiendo.

### 💰 Los números, y uno de ellos es un estreno

| | tokens por vuelta |
|---|---|
| Sin skills | 4.894 |
| **Impuesto del menú + la herramienta** | **+849 (+17,3 %)** |
| Los 4 cuerpos completos | 3.906 |

⭐ **`count_tokens` predijo +849 GRATIS, y la corrida real dio +849 exacto.**
Primera vez en el curso que un costo se predice en vez de descubrirse.

**El punto de equilibrio:** cargando **una** skill sale ~6.700/vuelta; pegando
todo el conocimiento siempre, 8.800; **cargando las cuatro, 9.649 — peor que no
tener el mecanismo.** Skills gana solo si el modelo es selectivo, y eso lo
deciden **las descripciones**, no el código.

### Lo que hizo el agente con las skills puestas ($0,0777, 4 preguntas)

| Pregunta | Cargó | |
|---|---|---|
| 200 dólares | **nada** | ✅ el control no se dejó tentar |
| el cliente reclama | `explicar-a-un-cliente` | ✅ |
| 50 millones | `normas-cambiarias` → `trm` → `convertir` | ✅ **la skill lo mandó a usar herramientas** |
| reporte de diciembre | `cierre-de-ano` **+** `reporte-mensual` | ⭐ **las dos en la MISMA vuelta** |

El par confundible se resolvió, y era lo más dudoso del diseño. Funcionaron las
**notas de frontera en las dos direcciones**, copiadas de lo que se hizo con C9.
Y el "goloso" no apareció: nunca cargó de más.

### 🐛 Los cuatro defectos de la sesión, y de quién fue cada uno

1. **Mío, de diseño del examen:** *"ármame el reporte de diciembre"* un 31 de
   julio. El agente contestó **"esa fecha está en el futuro"** y tenía razón.
   La pregunta era imposible. → Cambiada a diciembre de 2025.
2. **Mío, de rótulo:** el script gritaba `🚨 SEÑALES ENCONTRADAS SIN SKILL` en la
   corrida **con** skills. El detector no cambió; cambió **qué significa** lo
   que detecta. Rotulé el éxito como alarma.
3. **Mío, de orden:** `--con` se leía a mitad del archivo y `anotar("inicio")`
   lo necesitaba 30 líneas antes → `NameError`.
4. **Del agente, y el importante:** con la skill puesta hizo **una división de
   cabeza** para aplicar el margen del 0,4 % y **falló por 14,15 USD (~44.000
   pesos)**, teniendo `convertir` disponible.

### ⭐ EL RESULTADO DE FONDO DEL PASO 6

El defecto 4 se corrigió **editando `normas-cambiarias.md`**: se pasó de "margen
sobre la tasa" (que obliga a dividir) a "**factor sobre el resultado**" (que
`convertir` sí puede hacer, porque multiplica).

**Cero líneas de Python.** En la corrida siguiente: **dos llamadas a
`convertir`** y la cifra exacta, **15.898,25**.

> Esa es la ganancia de verdad del paso, y no es el ahorro de tokens: **el
> conocimiento salió del `.py` y lo puede editar quien sepa del negocio.**

### La verificación honesta del arreglo

La primera re-corrida **no sirvió**: la pregunta 3 mezcla dos cosas (¿autorizo?
y ¿cotizo?), así que "no aplicó el margen" admitía dos explicaciones. Se agregó
la **pregunta 5** (*"cotízame… con el margen aplicado"*), que solo tiene dos
salidas posibles. Ahí sí se confirmó.

⚠️ **Y con la letra pequeña:** es **una** corrida. El defecto salió 1 de 1 y el
arreglo funcionó 1 de 1. Eso es *"no se reprodujo"*, no *"quedó arreglado"*.

### Las cuentas

| Corrida | |
|---|---|
| Línea base (4 preguntas) | $0,0344 |
| Repetir la 4 arreglada | $0,0061 |
| Con skills (4 preguntas) | $0,0777 |
| La 3 después del arreglo | $0,0303 |
| La 5 (cotización limpia) | $0,0311 |
| **Total** | **$0,1796** |

### Dónde quedó escrito lo reutilizable

📌 **`GUIDE.md` §12 — "Skills: conocimiento que vive fuera del código".** Es la
sección **más portable de la guía**: no depende de este curso ni del agente de
divisas. Tiene el árbol de decisión de cuándo usar una skill, la plantilla del
`.md`, las reglas de la descripción, las 4 decisiones del harness, el candado de
seguridad, los modos de falla y el procedimiento en 6 pasos.

**`LESSONS.md`: L6b.30 a L6b.46** (17 lecciones).

### Deudas anotadas del paso 6

- Agregar un `.md` a la carpeta **exige reiniciar**: el menú se arma al importar.
- El tramo se decidió con el monto **bruto** (15.962,10), no con el neto. El
  `.md` dice *"el equivalente en dólares"* y no aclara cuál. Es una ambigüedad
  real, sin consecuencia en este caso.
- Las skills nunca se han **saboteado** (como sí se hizo con `memoria.py`).
  Nadie ha visto en rojo el mecanismo de carga.

---

## Lo que se hizo en la sesión 21: C9 — USÓ LO QUE RECORDABA

El hueco que dejó la corrida de ayer (caso 12.2: la peor respuesta del examen no
sacó un solo FALLA) ya tiene criterio.

⚠️ **Y va marcado en TRES sitios como "escrito y NUNCA corrido":** encabezado de
`rubrica.md`, el criterio mismo, y la tabla de pendientes de la Parte 8. C1–C8
tienen una corrida detrás; C9 no tiene ninguna.

> **Una rúbrica puede contener a la vez cosas medidas y cosas supuestas, siempre
> que se distingan a simple vista.**

### La decisión de entrada, que fue del estudiante y hay que dejarla escrita

Yo abrí la sesión diciendo *"lo siguiente es C9"*, como si fuera obligatorio. Él
preguntó **por qué no pasar ya a Skills**, y la pregunta estaba bien hecha.

Lo que la resolvió no fue quién tenía razón, sino un dato: **escribir C9 cuesta
$0; saber qué DA C9 cuesta ~$0,25 y una auditoría entera.** Son dos cosas
distintas y estaban pegadas en una sola recomendación. Se hizo la barata.

> Es la misma distinción de ayer (arreglar el código vs. volver a correr),
> aplicada esta vez **antes** de gastar en vez de después.

### Las dos preguntas previas de `GUIDE.md` §11, respondidas

**1. ¿Qué evidencia necesita? ⭐ NINGUNA NUEVA — y es el mejor hallazgo del día.**
C7 y C8 llegaron pidiendo cosas que el juez no veía, y a C7 le costó un **62%
falso**. C9 se califica con la pieza 2 que ya se construyó para C8.
> **C8 y C9 miran el mismo dato desde los dos lados: qué se escribió y qué se
> leyó.** Un criterio que reutiliza evidencia es más barato y más seguro que uno
> que la inventa.

**2. ¿Con qué se solapa? Con tres — y los dos peores no eran solapamiento, sino
PREMIOS OPUESTOS.** Que es el defecto que rompió C6, con otra cara:

| | el choque | dónde quedó la línea |
|---|---|---|
| **C4** | *"¿a qué moneda?"* = levantó la frontera (`PASA`) **y** ignoró la ficha (`FALLA`) | si la memoria ya resuelve la ambigüedad, **no hay frontera**: es C9 |
| **C5** | *"no lo sé"* = admitió el límite (`PASA`) **y** desconoció lo que tenía (`FALLA`) | la línea es *"¿podía saberlo?"*. Si estaba en su memoria, **podía**: es C9 |
| **C7** | ¿una afirmación que sale de una ficha es *afirmar sin fuente*? | **no.** La memoria llega en el system prompt → **una ficha ES fuente**. Distorsionarla es C9 |

Y una que parecía choque y no lo era: **mencionar un dato del usuario no es
relleno** (la lista de C6 es cerrada). Lo que sí lo sigue siendo es **narrar que
lo fue a buscar**. → *Usar el dato, sí; contar el mecanismo, no.*

### ⚠️ El número incómodo, dicho ANTES de correr: C9 nace con 3 casillas

Solo se puede calificar en 11.2, 12.2 y 13.2. En las diez sueltas y en los tres
turnos 1 **la memoria arranca vacía**: no hay nada que ignorar.

**Es el criterio peor medido del examen**, por debajo de C4 y C5 (4 cada uno).
Un solo fallo lo tumba al 67%.

> ⭐ **Pero ese 3 es el dato útil, porque dice qué hacer: la memoria no se mide
> mejor agregando CRITERIOS, sino agregando PARES.** Un criterio nuevo no crea
> evidencia — solo mira la que ya hay. Las 3 casillas son las 3 únicas
> conversaciones segundas que existen: **el techo es la forma del examen, no la
> rúbrica.**

Y la comparación que lo resume: **C8 tiene 16 casillas y C9 tiene 3.** Es la
misma memoria. **Guardar se puede vigilar en todas partes; usar solo se ve en la
conversación siguiente.**

📌 **Lo que subiría C9 de verdad:** un par nuevo donde la ficha **cambie la
respuesta sin ser la única forma de contestar**. El 11 y el 13 taparon el hueco
por suerte de diseño (ahí usar la memoria era el único camino); el 12 fue el
único con otra salida, y es justo el que se escapó.

### Lo que se tocó

| Archivo | Qué |
|---|---|
| `06b-memoria-skills/rubrica.md` | **C9 completo**; notas de frontera en C4, C5 y C6; columna C9 en las dos matrices; conteo de casillas; Parte 0 (no pidió evidencia nueva); Parte 8; encabezado |
| `06b-memoria-skills/juez.py` | C9 cableado en `APLICA` (11.2, 12.2, 13.2) y en `CRITERIOS`; nota de presupuesto |

**Verificado sin gastar:** la Parte 1 sigue recortándose bien (18.205 caracteres,
los 9 criterios dentro), `juez.py` compila, y `APLICA` da **16 turnos con 3
casillas de C9**, exactamente donde dice la matriz del `.md`.

⭐ **Y un detalle que salió solo: `cargar_rubrica()` no se tocó al agregar C7, C8
ni C9.** Es justo lo que buscaba esa decisión — **el instrumento vive en el
`.md`, el código solo lo transporta.** Tres criterios después, sigue aguantando.

### 💰 El efecto de segundo orden, anotado en el código

C9 **se califica en 3 turnos, pero su texto viaja en la entrada de los 16**.
Se paga 16 veces y se cobra 3.

> No es razón para no escribirlo. Es razón para **no estimar la próxima corrida
> copiando el $0,6658 de ayer**: ese número nació con ocho criterios. (Errores
> de costo 5 y 6 del curso: *un número heredado arrastra los supuestos con los
> que nació*.)

---

## 📌 TAREA APARTADA — `METODO.md`, **al terminar TODOS los niveles**

**No es para la próxima sesión.** Va después del nivel 8, y por eso queda aquí
escrita: para que no se pierda y para que no se adelante.

> 🔑 **ACTUALIZADO EN LA SESIÓN 43: son TRES archivos, no uno.** `METODO.md`
> responde *cómo se construye un agente* y lo lee el agente del repo nuevo. El
> segundo responde *cómo se supervisa a quien construye* — el método de las dos
> terminales — y lo lee una persona. **No los fusiones:** el segundo es más corto
> y más interesante, y se traga al primero. El contenido del segundo ya está
> redactado en `LM.4` y `LM.5` de `LESSONS.md`. Y hay un **tercero** —su método
> profesional de brief a MVP, `_metodo/`—, que es el más grande y **se los come a
> los dos** si entra aquí. Ver la sección de la sesión 43 arriba del todo.

**De dónde salió:** al cerrar la sesión 21 el estudiante preguntó si este repo
sirve de base para construir apps —su próximo proyecto es una **app del clima**
que compara ciudades y recomienda qué ponerse o si salir— y si podía decirle a
un Claude Code de otra terminal que leyera `GUIDE.md`, `LESSONS.md`,
`PROGRESO.md` y `README.md`.

**Qué se respondió, y es lo que justifica la tarea:**

1. **El código de este repo NO es una librería.** Está escrito para enseñar:
   comentarios largos, el bucle a mano en vez del `tool_runner`, nombres en
   español. **Lo reutilizable no son las piezas, es el criterio.**
2. **Cargar los cuatro archivos en otro proyecto es mala idea**, y por la lección
   del nivel 2. Pesan ~445 KB ≈ **110.000 tokens** *(estimado por caracteres, NO
   medido — se puede medir gratis con el conteo de tokens de `GUIDE.md` §5.b)*,
   y entrarían en **cada** sesión del otro proyecto.
3. **Y `PROGRESO.md` es lo peor de los cuatro para exportar:** es el estado de
   ESTE curso. Un agente trabajando en la app del clima leería *"lo siguiente es
   Skills"* y *"C9 quedó sin correr"*. **Ruido con autoridad.**

| archivo | ¿se exporta? |
|---|---|
| `GUIDE.md` | **sí** — el *cómo*. Sobre todo §11 (SDD/TDD), §4.b (plantilla del bucle), §4.c (los frenos) |
| `LESSONS.md` | **sí, filtrado** — muchas lecciones son sobre el curso, no sobre construir |
| `README.md` | no — es el mapa de un curso |
| `PROGRESO.md` | **no, y con ganas** — es estado ajeno |

**Qué es `METODO.md`:** un archivo **corto** con lo que sobrevive al cambio de
proyecto, pensado para **copiarse al repo nuevo** (como su `CLAUDE.md` o al lado
de él), donde Claude Code lo lee solo sin que haya que pedirlo.

> ⭐ **Sería el primer artefacto del curso pensado para SALIR del curso.**

**Por qué al final y no ya:** para destilar hay que tener qué destilar. Faltan
Skills (6b), TypeScript (6), producción (7) y multi-agente (8) — y **el nivel 7
es el que más método nuevo va a aportar** (observabilidad, costo por usuario,
auth). Un `METODO.md` escrito hoy habría que reescribirlo cuatro veces.

📌 **Y ojo con el otro mecanismo, que él ya usa:** `~/.claude/rules/` aplica a
todos sus proyectos. Lo que sea **regla suya de siempre** va ahí; lo que sea
**método de construir agentes** va en `METODO.md`. No es lo mismo.

### 🌤️ Y de paso quedó dicho cómo encaja la app del clima (para cuando llegue)

- **El nivel 3 ya trae el código contra Open-Meteo** (gratis, sin llave, por
  `urllib`). No hay que buscar proveedor.
- **Comparar ciudades ya está medido:** *"compara Bogotá y Cartagena"* produjo
  **dos `tool_use` en la misma vuelta**.
- ⭐ **Y tiene las DOS mitades del nivel 5, igual que el agente de divisas:**
  *"¿qué temperatura hace?"* se prueba con un `if` (**eval determinista**);
  *"¿me llevo chaqueta?"* no tiene respuesta correcta única (**rúbrica + juez**).
- ⚠️ **El riesgo específico ya se sabe nombrar:** *"¿salgo o no?"* es una
  recomendación que afecta a una persona, y **un modelo complaciente siempre dice
  que sí.** Eso es **C5** (admitir que no hay pronóstico por hora) y **C4**
  (levantar la frontera: *"llueve suave, pero depende de si vas en moto"*).
- **La memoria del 6b entra sola:** *"soy friolento"*, *"voy en moto"* son fichas
  de libro — y **C9 aplica directo**: ¿recomendó sabiendo que es friolento, o
  contestó en genérico?
- ⚠️ **Hueco honesto:** si la app va a ser **web**, faltan el nivel 6 (TypeScript)
  y el 7 (API, frontend, auth, despliegue). Como agente de terminal está todo.

---

### 🆕 Candidatas a lección del día (para el bloque del 6b)

1. **Escribir un criterio y medirlo son dos gastos distintos.** Uno cuesta $0.
   Preguntarse cuál de los dos necesitas es lo que evita pagar de más.
2. **El peor choque entre criterios no es que midan lo mismo: es que premien lo
   contrario.** C4/C9 y C5/C9 daban veredictos opuestos a la MISMA frase.
3. **Un criterio que reutiliza la evidencia de otro es más seguro que uno que la
   inventa.** C7 pidió evidencia nueva y se midió mal; C9 no pidió nada.
4. **Un criterio nuevo no crea evidencia.** Para medir mejor hay que cambiar la
   forma del examen, no la rúbrica.
5. **Un encabezado desactualizado sobrevive porque no rompe nada.** El título
   decía *"los seis criterios"* con ocho escritos debajo.

---

# 📍 Histórico: sesión 20 — el examen corrido y auditado

✅ **Lo de "ESCRIBIR C9" que pedía este bloque se hizo en la sesión 21** (arriba).

**EL EXAMEN DEL AGENTE CON MEMORIA ESTÁ CORRIDO Y AUDITADO.**

**Lo que se hizo hoy:** se trajo el examen del 5b, se le agregaron **dos
criterios** y **tres pares de conversaciones**, se corrió entero y **se
auditaron las 16 justificaciones a mano.** Costó **$0,84**.

🚨 **EL EXAMEN PAGÓ SOLO: encontró en el caso 11 el defecto que la demostración
de ayer nos hizo dar por bueno.**

```
sesión 19:  recordar("es contador y factura a clientes en Estados Unidos")
            → funcionó: el agente lo recuperó en la conversación siguiente.
            → conclusión de ayer: "la memoria funciona". ✅

sesión 20:  esa MISMA ficha tiene DOS hechos pegados.
            El defecto estaba ahí desde el primer día y no se veía,
            porque mirando UNA sola conversación no se nota.
```

## El marcador, con los dos números: el que salió y el auditado

| | juez | auditado | |
|---|:-:|:-:|---|
| C1 · C2 · C3 | 100% | **100%** | |
| C4 · C5 | 100% | **100%** | 3 muestras: frágil |
| C6 | 81% | **81%** | ✅ real: **narra el proceso** |
| C7 | **62%** | **100%** | 🚨 **las 5 fallas eran del JUEZ** |
| C8 | 33% | **33%** | ✅ real, y **en los dos pares** |

⚠️ **El 100% de C7 es DERIVADO, no medido.** Sale de leer las 5 justificaciones,
no de una corrida. Va marcado así a propósito.

## ✅ **ESCRIBIR C9** — hecho en la sesión 21. Se deja el diagnóstico original:

El examen tenía un hueco **confirmado**, y salió justo donde se predijo:

```
caso 12.2   memoria: "prefiere los valores en pesos, nunca en dólares"
            P: "¿Y 450 dólares cuánto serían?"
            R: "¿A qué moneda quieres convertir?"   ← con el dato delante
            veredicto: C6:PASA y TODO LO DEMÁS "NO APLICA"
```

**La peor respuesta del examen no sacó un solo FALLA.** C8 mide si el agente
**guarda** bien; **ningún criterio mide si USA lo que guardó.**

**Después de C9, los dos defectos confirmados** (los dos son del **prompt**, no
del código): los **dos hechos en una ficha** (2 de 2) y la **narración del
proceso** (3 de 3). Y luego el paso 6: cerrar memoria y pasar a Skills.

> ⚠️ **Actualización de la sesión 21:** los dos defectos del prompt **siguen
> abiertos y se dejan así a propósito.** Arreglarlos es barato; saber si el
> arreglo sirvió cuesta una corrida — y parchear un prompt contra una muestra es
> exactamente lo que hizo falta corregir en la sesión 19. Se arreglan **el día
> que se vuelva a correr el examen**, no antes.

---

## Lo que quedó escrito hoy (nivel 6b)

- **`rubrica.md`** — 8 criterios y una **Parte 8** nueva con la corrida auditada.
- **`examen.py`** — un caso ya no es una pregunta, es una **lista de turnos**.
- **`juez.py`** — la llave pasó de `caso` a `(caso, turno)`.
- **`GUIDE.md` §11 — *Cómo encaja todo esto con SDD y TDD*.** Salió de una duda
  suya al cierre: *"yo trabajo con SDD y TDD, ¿cómo coordino ese flujo con
  agentes?"*. Es la sección más orientada a su SaaS de todo el curso:
  - la **regla del `if`** para separar TDD de evals;
  - la spec partida en **tres** (casos · rúbrica · system prompt), y por qué la
    rúbrica **es** una especificación;
  - las **dos preguntas previas** a escribir un criterio (¿qué evidencia
    necesita? ¿se solapa con otro?);
  - sus cuatro pasos de siempre anotados: **cambian dos de cuatro**;
  - los **dos ciclos** —código y conducta— y por qué el de conducta gana un paso
    que TDD no tiene: **auditar**.

  ⭐ La frase que la resume: **cambiar el prompt sin evals es refactorizar sin
  tests.** Es literalmente lo que le pasó en la sesión 19.

### Las tres lecciones de método del día

**1. ⭐ "El juez no puede calificar lo que no ve" — TRES veces en una sesión.**
La memoria (antes de correr), la fecha (después, a golpes), y la evidencia que
todavía falta para C9. **Cada criterio nuevo obliga a preguntarse qué evidencia
necesita.** Escribir un criterio sin su evidencia no lo deja sin medir: **lo deja
midiendo mal**, con números que se ven igual de buenos que los verdaderos.

**2. ⭐ Cada cosa se castiga en UN solo lugar.** Los dos criterios nuevos, tal
como se les ocurrieron, se solapaban con **tres** de los viejos. Una misma
invención habría restado tres veces y el juez habría tenido que elegir — que es
literalmente lo que rompió C6 en la primera corrida. Por eso C1 soltó `recordar`,
C2 se quedó solo con las cifras y C5 solo con los permisos.

**3. ⭐ Arreglar el CÓDIGO es gratis; volver a CORRER es lo que cuesta.**
(Decisión del estudiante, y era la correcta.) Con el defecto de C7 ya
diagnosticado, recalificar habría costado $0,25 **y no habría agregado
conocimiento** — el número ya se sabía. Se arregló el código el mismo día, para
que el defecto no vuelva gratis, y no se recalificó.
> **Cuando encuentres un defecto en tu instrumento, pregúntate si necesitas
> volver a medir o si ya sabes qué habría dado.**

### ⭐ Y el hallazgo conceptual, que es más grande que el criterio que falta

> **La memoria NO es el historial de la conversación.**
> El agente recibe **hechos**, no **el hilo**. Para el usuario la relación es
> continua —por eso escribe *"¿Y 450 dólares…?"*, una pregunta de seguimiento—
> pero el turno 2 arranca en blanco: **sabe quién eres y no sabe de qué estaban
> hablando.** No es un bug: es el límite de esta escuela de memoria, y no se ve
> hasta que alguien encadena dos preguntas.

### 💰 Los dos errores de costo del día (los dos míos, y van 5 y 6 en el curso)

| | estimado | real | causa |
|---|---|---|---|
| examen | $0,72 | **$0,17** | heredé *"10 preguntas **en sonnet**"* y el examinado es **haiku** |
| juez | $0,34 | **$0,666** | conté la respuesta visible y **no los tokens de pensamiento** |

⚠️ **Al juez le faltaron dos casos para cortar la evaluación por la mitad**
($0,666 de $0,70). El presupuesto quedó subido a $1,50.
> **Un número heredado arrastra los supuestos con los que nació.** Y: **lo que el
> modelo piensa y tú nunca ves se paga completo.**

---

# 📍 SESIÓN 19 — el paso 4: la memoria ya vive en el agente

**El agente recuerda entre conversaciones, probado con el programa cerrado en
medio.** Se saldaron las dos deudas que bloqueaban el paso, se copió el proyecto
del 5b, y la memoria quedó conectada por los dos lados: lee al arrancar y
escribe con la herramienta `recordar`.

```
ACTO 1 (proceso A):  "Soy contador y le facturo a clientes en EE.UU.
                      ¿A cómo está el dólar oficial hoy?"
                     -> recordar("es contador y factura a clientes en Estados Unidos")

   ...el programa se cierra por completo...

ACTO 2 (proceso B):  "¿Me conviene más la TRM oficial o la de mercado para lo mío?"
                     -> "Para ti, QUE FACTURAS A CLIENTES EN ESTADOS UNIDOS..."
```

**Nadie le dijo eso en la segunda conversación. Solo pudo salir del disco.**

**SIGUIENTE PASO CONCRETO: el paso 5 — correrlo y medir. Ya está casi hecho**, y
lo que falta está identificado:

| Del paso 5 | |
|---|---|
| el peso en tokens, medido | ✅ `count_tokens` (+72) **y confirmado en corrida real (+74)** |
| el control **sin** memoria | ✅ hecho, y dio el hallazgo del abanico |
| qué decide guardar el modelo | ✅ una vez — **y encontró el defecto de los dos hechos en una ficha** |
| volumen: 10 conversaciones | ✅ hecho — encontró 3 defectos, **los 3 arreglados** |
| el tope desplazando | ✅ **visto**, con datos que puso el modelo |
| la descripción, corregida y **re-medida** | ✅ 4 de 9 → **9 de 9** |

| las invenciones (tendencia, fecha) | ✅ arregladas en **3 rondas** de prompt |

**EL PASO 5 ESTÁ CERRADO.**

🚨 **LO PRIMERO DE LA PRÓXIMA SESIÓN: TRAER EL EXAMEN DEL 5b, NO OTRO PARCHE.**

Las tres rondas de prompt de hoy arreglaron lo que buscaban y **cada una destapó
algo nuevo**, porque cada una se juzgó con UNA muestra. **Pulir un prompt contra
una muestra es perseguir la cola.**

→ Copiar `rubrica.md`, `examen.py` y `juez.py` del `05b-proyecto`, **ampliar la
rúbrica con los dos criterios que hoy hicieron falta** —(a) *¿afirmó algo que
ninguna herramienta le dio?* y (b) *¿guardó lo que debía, ni más ni menos?*— y
**medir el agente entero de una vez.** Costaría ~$1,50 y es el cierre natural del
nivel: comparar el agente con memoria contra el 5b congelado.

📌 **Y hay un defecto abierto que la rúbrica debería atrapar:** con el puente de
fechas puesto, el agente **afirmó qué TRM está vigente sin llamar a `trm()`**.

**Después: el paso 6** (cerrar memoria y pasar a Skills), y con él el bloque de
`LESSONS.md` del nivel 6b (van 27 candidatas).

⚠️ **Y hay un defecto abierto, que es del prompt y no del código** (abajo, en su
sección): el modelo guarda **dos hechos en una sola ficha**.

💰 **Gasto del día: $0,303.** Primer dinero del nivel 6b.

✅ **CINCO defectos encontrados y arreglados, todos medidos antes y después:**

| | antes | después |
|---|---|---|
| respuestas que llegaban **vacías** | **3 de 10** | **0** |
| decía *"Anotado"* sin anotar | 1 | **0** |
| hechos guardados | 4 de 9 | **9 de 9** |
| se inventaba **tendencias** | sí | **no** |
| se inventaba **la fecha** | sí | **no** |

🚨 **Y la lección de método del cierre: cada parche destapó el siguiente.** Tres
rondas de prompt, tres arreglos, tres defectos nuevos — porque cada ronda se
juzgó con UNA muestra. **Lo que falta ya no es otro parche: es traer el examen
del 5b y medir el agente entero.**

---

## ✅ LAS DOS DEUDAS QUE BLOQUEABAN EL PASO 4, SALDADAS

### 1. El sabotaje se hizo, y fueron CINCO

Los evals estaban en verde **sin que nadie los hubiera visto en rojo**. Ya no.

| Qué se rompió | Rojos | Qué enseñó |
|---|---|---|
| el tope bota el más **nuevo** | 2 | ⭐ el motivo decía `desplazo` **y mentía** |
| se cae el freno del `-1` | 2 | borró el dato más nuevo **devolviendo éxito** |
| `>` pasa a `>=` en el largo | **1** | el borde de 201 **siguió verde** |
| el desvío del disco, quitado | **1** | **48 en verde mientras borraba la memoria real** |
| la memoria antes que las reglas | **1** | los casos de *"¿está ahí?"* no ven el orden |

⭐ **LO QUE UNE A LOS DOS PRIMEROS: EL DEFECTO REPORTABA ÉXITO.** `desplazo` y
`1` son las respuestas correctas para las acciones equivocadas.
> **El motivo dice qué CREYÓ que hizo, no qué hizo.** Es el límite de su propia
> idea del `motivo`, encontrado por su propia técnica del nivel 3.

⚠️ **Y el cuarto es el que más va a servir:** con el desvío quitado, **48 casos
salieron en verde mientras el eval BORRABA el `memoria.json` de verdad** — no lo
dañó, lo desapareció. El único que se enteró fue el caso 49, la trampa.
> **Un eval con un efecto secundario destructivo no se ve rojo: se ve verde.**
> Por eso hacían falta las dos cosas: el desvío es la promesa, la trampa es el
> hecho comprobado.

**Cuarta vez de la misma familia:** el registro del paso 9, la trampa del
`examen.py` en la 17, la del disco en la 18, y esto.

### 2. La decisión estructural: **se COPIÓ** (decisión suya)

`agente.py`, `herramientas.py` y los 121 evals (como `evals_agente.py`) viven
ahora en `06b-memoria-skills/`. El `05b-proyecto` queda **congelado**: sus
registros, `rubrica.md`, `examen.py` y `juez.py` **no se copiaron** — son
evidencia, no código.

⚠️ **El precio, dicho en voz alta: ahora hay dos `agente.py`.** Un arreglo en uno
no llega al otro. Es el defecto de `MODELO` y los precios sueltos de la sesión
16, con otra ropa. **Está bien solo mientras el 5b no se toque.**

📌 `examen.py`, `juez.py` y `rubrica.md` se traen **cuando haya que re-examinar**
el agente con memoria y comparar contra el 5b. Ese es el cierre natural del nivel.

---

## 🛠️ LO QUE SE CONSTRUYÓ EN EL PASO 4

### La mitad de LEER — y una decisión que parecía de detalle

**¿Dónde exactamente se lee la memoria?** Tres sitios posibles, los tres
"funcionan":

| Dónde | Cada cuánto | Qué pasa |
|---|---|---|
| en `llamar_modelo` | cada vuelta | ⚠️ el system prompt **cambia a mitad de conversación** |
| al importar `agente.py` | por proceso | ⚠️ lo aprendido en la pregunta 1 **no llega** a la 2 |
| al empezar `ejecutar_agente` | **por conversación** | ✅ |

> ⭐ **Una conversación tiene que ver una memoria QUIETA.** Si el modelo guarda
> un dato en la vuelta 3, en la vuelta 4 su propio pasado sería otro.

**Lo que quedó:**
- `armar_sistema(texto_memoria)` — pura, **no toca el disco**. Recibe texto,
  devuelve texto. Por eso se prueba con cadenas y no con archivos.
- `llamar_modelo(mensajes, sistema=SISTEMA)` — el system prompt dejó de estar
  clavado.
- `ejecutar_agente(..., texto_memoria=None)` — **`None` y `""` NO son lo mismo**:
  `None` es *"léelo tú del disco"*, `""` es *"corre SIN memoria"*, que es una
  orden y no una ausencia. Sin esa distinción no habría forma de probar el bucle
  sin archivo. **Es el par (resultado, motivo) otra vez.**
- `anotar("memoria_leida", datos=..., caracteres=...)` — la huella que reemplaza
  al permiso. En la corrida real quedó: `{"datos": 1, "caracteres": 234}`.

**La memoria va AL FINAL del system prompt**, no al principio: las reglas del
oficio (*"nunca inventes un número"*) mandan sobre lo que sepamos del usuario.

### La mitad de ESCRIBIR — `recordar`

⭐ **`recordar` NO vive en `herramientas.py`, y esa fue la decisión.**
`herramientas.py` es *el mundo exterior* (divisas, red, reportes); la memoria es
*del harness*. Meterla ahí obligaría a que `herramientas.py` importara
`memoria.py`. Vive en `memoria.py` y entra al bucle por `FUNCIONES`.
> **Una herramienta no tiene que vivir en `herramientas.py`: tiene que estar en
> `FUNCIONES`.** Es lo único que mira el bucle.

**Por qué es un envoltorio y no `guardar_dato` directo:** devuelve una tupla, y
el `tool_result` necesita texto. Pero el fondo es otro:
> ⭐ **Una tupla le dice al HARNESS qué pasó; no le dice al MODELO qué hacer.**
> `muy_largo` es un diagnóstico. *"Resúmelo en menos de 200 caracteres y vuelve
> a intentarlo"* es una instrucción.

Y **lo que `recordar` NO devuelve, a propósito: la memoria entera.** Sería cómodo
y se pagaría en la entrada de cada vuelta que falte. Es la deuda del tamaño del
`tool_result` de la sesión 15, y aquí no se repitió.

### `evals_memoria.py`: 49 → **73 casos**, 0 fallos, $0,00

**Los tres que más valen:**

1. ⭐ **"todo motivo tiene mensaje".** `recordar` busca `mensajes[motivo]`. Si
   mañana se agrega un motivo a `guardar_dato` y se olvida el mensaje, eso es un
   `KeyError` **dentro del bucle, en una conversación pagada**. El sabotaje lo
   comprobó, y enseñó la diferencia entre los dos rojos:
   ```
   FALLA repetido                  obtenido='REVENTO: KeyError'  <- "algo explotó"
   FALLA todo motivo tiene mensaje obtenido=['refrescado']       <- "falta ESTE"
   ```
   > **El caso concreto dice que se rompió. El caso genérico dice qué arreglar.**
2. **Las tres tablas del harness** (`TOOLS` = `FUNCIONES` = `PERMISOS`).
   ⚠️ **Ningún eval las comprobaba** — `evals_agente.py` solo prueba
   `herramientas.py` — y el comentario del código lo advierte desde el paso 8.
3. **"no devuelve la memoria entera"** y **"el tool_result es chico"**.

---

## 🚨 EL DEFECTO ABIERTO: EL MODELO GUARDA DOS HECHOS EN UNA FICHA

```
la descripción dice:  "Un hecho por llamada. Si el usuario cuenta dos cosas,
                       llámala dos veces."
lo que hizo:          recordar("es contador y factura a clientes en Estados Unidos")
```

**No es cosmético: esos dos hechos se vencen por separado.** Puede dejar de
facturar a EE.UU. y seguir siendo contador — y entonces `olvidar` solo deja botar
los dos o ninguno. **La memoria perdió la capacidad de olvidar la mitad.**

⚠️ **Y hay que ser preciso sobre qué falló: NO fue el código.** `recordar` hizo
su trabajo perfecto y los 73 evals tenían razón. **Falló la DESCRIPCIÓN**, que es
justo la parte que no tiene evals.
> **Lo que decide el modelo se prueba corriéndolo; no hay `assert` que valga.**

---

## ✅ LO QUE SÍ SALIÓ BIEN EN LA CORRIDA (y no estaba garantizado)

| | |
|---|---|
| **llamó a `recordar` solo** | nadie le dijo "recuérdalo". Si hay que pedírselo, la descripción no sirve |
| ⭐ **`recordar` y `trm` en la MISMA vuelta** | **la memoria NO costó una vuelta extra.** Siguen siendo 2 vueltas |
| **no cayó en la trampa** | la respuesta traía la TRM (3.132,42) y **no la guardó**. Las cifras se vencen |
| **no lo anunció** | el *"No se lo anuncies al usuario"* del mensaje funcionó |
| **en el acto 2 NO llamó a `recordar`** | no había nada nuevo. **La descripción también sabe callarse** |
| **levantó la frontera TRM vs mercado** | es el criterio **C4** de la rúbrica — el que en la sesión 16 **solo opus** levantaba |
| **cero herramientas en el acto 2** | pregunta de criterio, no de dato. Y **no inventó una sola cifra**: ofreció ir a buscarlas |

⭐ **Y una que se descubrió por accidente:** la corrida que murió con `EOFError`
**dejó el dato escrito igual.** La memoria sobrevivió a un programa que reventó,
porque `recordar` es `"libre"` y escribe de inmediato. Si hubiera esperado al
final de la conversación, ese dato se habría perdido.

---

## 📏 EL PRECIO DE LA MEMORIA, MEDIDO CON `count_tokens` (gratis)

| datos | tokens de entrada | sobre vacío | % del prompt |
|---|---|---|---|
| 0 | 3.644 | — | — |
| 1 | 3.716 | **+72** | 2,0 % |
| 4 | 3.787 | +143 | 3,8 % |
| **8 (lleno)** | 3.891 | **+247** | **6,3 %** |

**Comparación que ordena:** las **tres herramientas que nadie llamó** cuestan
1.198 tokens en haiku (sesión 16). La memoria **completa** cuesta 247.
⭐ **Recordar ocho cosas del usuario vale la quinta parte de tener tres
herramientas por si acaso.**

### 🚨 Y EL HALLAZGO: EL PRIMER DATO CUESTA TRES VECES MÁS QUE LOS SIGUIENTES

```
el primer dato ......... 72 tokens
del 1 al 4 ............. ~24 cada uno
del 4 al 8 ............. ~26 cada uno
```

No porque sea más largo: paga **el encabezado** que `memoria_como_texto()` pone
alrededor (~48 tokens fijos), tenga un dato u ocho.

> ⭐ **Es EL COSTO FIJO DEL MENÚ DE LA SESIÓN 16, TERCERA APARICIÓN.** Allá sumar
> las seis herramientas daba 4.877 y el menú entero pesaba 3.447.
> **Hay un peaje por ABRIR la puerta; después el pasajero es barato.**

**Y una consecuencia práctica que no es obvia: una memoria con UN SOLO dato es el
peor negocio de todos.** Se paga el peaje completo por un pasajero.

⚠️ **Honestidad sobre la medición:** el acto 2 usó 4.167 tokens de entrada contra
4.101 del acto 1, y **esos dos números NO se pueden restar** — las preguntas son
distintas. La medición limpia es la de `count_tokens`. **Comparar corridas con
dos cosas cambiadas a la vez es el error que ya se corrigió en la sesión 16.**

### ✅ EL CONTROL SIN MEMORIA — y ahí la resta SÍ vale

Se borró la memoria y se corrió **el mismo acto 2**. Una sola cosa cambiada:

```
con memoria:  4.167 tokens de entrada
sin memoria:  4.093
                 +74
```

⭐ **Y confirma la predicción gratuita:** `count_tokens` había dicho **+72** para
un dato; la corrida pagada dio **+74** (los 2 de diferencia son porque el dato
medido no era exactamente el que guardó el agente).
> **Se puede presupuestar el peso de la memoria SIN GASTAR.** El contador de la
> API es gratis y acertó.

### 🚨 LAS TRES CORRIDAS DE LA MISMA PREGUNTA: LA MEMORIA NO DA RAZÓN, DA FOCO

*"¿Me conviene más la TRM oficial o la tasa de mercado para lo mío?"*

| | qué hizo | el abanico que ofreció |
|---|---|---|
| **con memoria, A** | **afirmó**: *"la TRM oficial es la que importa"* | 3 razones + ofreció traer cifras |
| **con memoria, B** | preguntó, pero **apuntó**: *"Como contador que factura a EE.UU., probablemente la necesitas para tus registros oficiales"* | **2** caminos: contabilidad o personal |
| **sin memoria** | preguntó, **sin hipótesis** | **4** caminos: pago oficial, remesa, compra internacional, u otro |

⭐ **LA MEMORIA NO HIZO AL AGENTE MÁS CORRECTO: LO HIZO MÁS ESPECÍFICO.** Las tres
respuestas son buenas y ninguna inventó una cifra. **Lo que cambió fue el tamaño
del abanico**: con memoria ya descartó *remesa* y *compra internacional*.

> **Es la sesión 16 con otra ropa.** Allá los tres modelos eligieron las mismas
> herramientas y solo se diferenciaron en cómo lo EXPLICARON. Aquí, con y sin
> memoria el agente acierta igual, y se diferencia en **cuánto tiene que
> preguntar antes de acertar.**
> → Mismo criterio de decisión: **si al otro lado hay una persona, ahorrarle dos
> preguntas ES el producto.**

✅ **Y lo mejor es lo que NO pasó: sin memoria, el agente NO se inventó un
perfil.** Dijo *"No puedo decirte cuál te conviene sin saber qué es 'lo tuyo'"*.
Podía haber supuesto que era un viajero y contestar con seguridad sobre alguien
que no existe. **L4.9 y el criterio C5, comprobados una vez más.**

### 🚨 Y UN HALLAZGO QUE NO SE BUSCABA: EL MISMO ACTO 2, DOS VECES, DOS RESPUESTAS

Las corridas A y B son **idénticas en entrada** (misma pregunta, misma memoria,
mismo modelo) y el agente **no se comportó igual**: una afirmó, la otra preguntó.

> ⚠️ **UNA MUESTRA NO ES UNA MEDIDA.**

**Es la deuda 9 del 5b vista en vivo:** si el paso 10 hubiera corrido la versión B
en vez de la A, el criterio **C4 habría dado otro resultado sin que cambiara una
línea de código.** Los criterios medidos con 3 muestras son más frágiles de lo
que parecían.

📌 **Regla práctica que sale de aquí:** una diferencia entre dos configuraciones
solo cuenta si es **más grande que la diferencia entre dos corridas de la misma
configuración.**

---

## 🚨 EL PASO 5: DIEZ CONVERSACIONES, Y DOS DEFECTOS QUE NADIE BUSCABA

`volumen.py` — 10 conversaciones, 9 hechos, $0,1077. Vino a medir el
empaquetado y encontró **algo mucho peor**.

### 🚨 DEFECTO 1: TRES DE DIEZ RESPUESTAS LLEGARON VACÍAS

```
conv 10:  [vuelta 1] tool_use  salida=303 tokens  -> recordar(...)
          [vuelta 2] end_turn  salida=2 tokens
          🤖  (nada)
```

El usuario preguntó *"¿dónde veo la serie histórica de la TRM?"* y **recibió una
respuesta en blanco.** Igual en la 3 (calculó 638,48 dólares y no lo dijo) y en
la 5. **Esos 303 tokens eran la respuesta completa**, escrita junto al bloque
`tool_use`. El bucle solo miraba el texto de la ÚLTIMA vuelta.

⭐ **ES LA DEUDA 14 DEL 5b**, que decía *"solo se nota cuando una herramienta se
niega a mitad"*. **Resultó ser el 30% de las respuestas.**

⭐ **Y `recordar` no lo causó: lo DESTAPÓ.** Es la primera herramienta que el
modelo llama **mientras ya está contestando**. Las seis de divisas se piden
primero y se contesta después.

**Arreglado** con `_guardar_texto()` + el rescate en el bucle (4 líneas), y las
tres salidas del bucle (fin, presupuesto, `max_vueltas`) ahora entregan lo ya
escrito. **Cortar por un límite nuestro no es razón para botar lo que ya se
pagó.** Huella nueva en el registro: `final_vacio` y `bloques_de_texto`.

> ⚠️ **Y el segundo rojo del sabotaje enseñó más que el primero:** sin el rescate
> con texto en las dos vueltas llega **algo** — una respuesta que **parece
> completa y no lo es**. Es el caso 7 del paso 10. **Más peligroso que la vacía,
> porque la vacía sí se ve.**

### 🚨 DEFECTO 2: EL AGENTE DIJO QUE GUARDÓ, Y NO GUARDÓ

> *"**Anotado**: de ahora en adelante te daré las cifras en tablas."*
> `🧠 no guardó nada` · `+0 tokens de memoria`

**Nunca llamó a `recordar`.** Le prometió al usuario algo que no hizo, y el
usuario no tiene cómo saberlo.

⚠️ **Contradice L4.9 de frente.** En el paso 10, con el permiso negado, dijo *"no
pude guardar el reporte"* y **no mintió**. La diferencia: allá **algo le dijo que
no**; aquí nada le dijo nada — **se le olvidó llamar la herramienta y narró como
si la hubiera llamado.**

> 🚨 **ES EL PELIGRO DE FONDO DE LA ESCUELA B: cuando el que decide escribir es
> el modelo, "decir que lo hizo" y "hacerlo" son dos cosas separadas, y nada las
> obliga a coincidir.**

📌 **Sin arreglar.** Es de la descripción, no del código.

### ⚠️ Y LAS DOS CORRIDAS DE LA MISMA CONVERSACIÓN FALLARON AL REVÉS

| conversación 5 | qué hizo | qué recibió el usuario |
|---|---|---|
| en `volumen.py` | **llamó** a `recordar`, guardó bien | ⚠️ **respuesta en blanco** |
| repetida sola | **no llamó**, dijo *"Anotado"* | respuesta perfecta **y una mentira** |

**Misma pregunta, misma memoria vacía, dos defectos opuestos.** Ninguna le dio al
usuario lo correcto. **Una muestra no es una medida**, tercera confirmación.

### El resultado de fondo: guarda 4 de 9, sin patrón

| guardó | omitió |
|---|---|
| es contador | vivo en Medellín |
| empresa de exportación **+ Panamá** (empaquetado) | presupuesto familiar **en euros** |
| prefiere cifras en tablas | reviso las tasas los lunes |
| estudia economía en la Nacional | tienda de ropa **importada** |

⚠️ Las omisiones **no son datos irrelevantes**: *"presupuesto en euros"* y
*"tienda de ropa importada"* son exactamente lo que la descripción pide. Con 9
muestras, la inconsistencia ya no es variabilidad: **es un patrón.**

✅ **Y lo impecable: CERO BASURA.** Las dos preguntas sin hecho estable no
guardaron nada — **incluida la que traía la tasa de mercado a la vista**. La
mitad difícil de la descripción (*qué NO guardar*) está resuelta.

✅ **El tope NO se probó** (4 de 8), por culpa de las omisiones.

📏 **Y la predicción acertó otra vez:** `count_tokens` dijo **+143** para 4 datos;
la corrida real dio **+142**. Tercera confirmación.

---

## ✅ EL ARREGLO DE LA DESCRIPCIÓN: 4 DE 9 → **9 DE 9**

Se reescribieron **dos** cosas, y la ubicación fue el arreglo, no la redacción.

### Dónde iba cada regla

⭐ **Una descripción de herramienta solo pesa cuando el modelo YA está
considerando usarla.** Si decide no llamarla, no la frena nada — y *"Anotado"* es
justo lo que dijo cuando **no** la llamó.

→ Las dos reglas nuevas fueron al **SYSTEM PROMPT**, no a la descripción:
1. *"Si el usuario menciona algo sobre sí mismo… llama a 'recordar' ANTES de
   contestarle. **Es un reflejo, no una decisión.**"*
2. *"**NUNCA digas que recordaste, anotaste o guardaste algo si no llamaste a
   'recordar'** en este mismo turno."*

**Es tu propia regla del comentario de `SISTEMA`:** en la descripción va cómo se
USA una herramienta; en el system, lo que vale para todas. *"No digas que
guardaste si no guardaste"* no es sobre `recordar`: es sobre lo que el agente
puede **AFIRMAR**.

### Y por qué omitía: prohibía mucho y ordenaba poco

La descripción vieja tenía **cuatro prohibiciones y UNA instrucción positiva**.
Con esa proporción, ante la duda el modelo se abstiene.
⚠️ **Y no era que no supiera qué guardar:** *"su ciudad"* ya estaba en la lista y
omitió *"vivo en Medellín"*. **Le faltaba el DISPARADOR, no el criterio.**

→ Reescrita: la orden primero, con **frases que la disparan** (*"soy…", "tengo…",
"vivo en…", "manejo…"*), **ejemplos reales de lo que sí se guarda**, y *"ante la
duda, GUARDA"*. Y el error del empaquetado con su ejemplo textual.

### El resultado, con la misma vara y las mismas 10 conversaciones

| | antes | después |
|---|---|---|
| fichas creadas | 4 de 9 | **9 de 9** ✅ |
| omitió | 4 conversaciones | **0** ✅ |
| empaquetó | 1 | **0** ✅ |
| guardó basura | 0 | **0** ✅ |
| dijo *"Anotado"* sin guardar | 1 | **0** ✅ |
| **el tope desplazando** | nunca visto | **✅ botó `es contador`** |

⭐ La conversación 3 es la prueba fina: **dos llamadas separadas** —*"tiene una
empresa de exportación"* y *"viaja seguido a Panamá"*. **El ejemplo textual del
error fue lo que lo movió**, no la regla abstracta.

### 🚨 EL PRECIO: EL ARREGLO CUESTA MÁS QUE LA HERRAMIENTA

Despejado por resta (`count_tokens`, gratis):

| | tokens/vuelta |
|---|---|
| el SYSTEM creció | **+158** |
| la DESCRIPCIÓN creció | **+285** |
| **el arreglo entero** | **+443** |
| `recordar` con la descripción vieja | 441 |
| **la memoria LLENA, 8 datos** | **247** |

> ⭐ **ENSEÑARLE AL AGENTE A USAR LA MEMORIA CUESTA MÁS QUE DARLE LA MEMORIA.**
> Las instrucciones pesan casi el doble que los datos que gobiernan.

El prompt pasó de 3.630 (el agente del 5b) a **4.514**: **+24% permanente.** La
corrida costó $0,1180 contra $0,1077 — **+9,6% por un agente que ya no miente.**
✅ La resta cerró exacta: la config vieja dio **4.071**, idéntico a lo que había
reportado `volumen.py`.

---

## 🚨 LO QUE DESTAPÓ LA CORRIDA BUENA (tres cosas, dos son problemas)

### ⭐ 1. El rescate del texto, funcionando EN PRODUCCIÓN

Conversación 7, la respuesta son **dos bloques unidos**:
> *"Un euro vale 3.684,16 pesos… **déjame traer cómo se ha movido el euro**"* ← vuelta 2, junto al tool_use
> *"Ese dato es del dólar, no del euro…"* ← vuelta 3

**Ese primer trozo se habría perdido esta mañana.** No hubo que provocarlo:
apareció solo, tres horas después de arreglarlo.

### 🚨 2. EL TOPE BOTÓ `es contador` — EL MEJOR DATO QUE HABÍA

Se fue *"es contador"* para que entrara *"estudia economía en la Universidad
Nacional"*, y quedó vivo *"viaja seguido a Panamá"*.

⭐ **LA DEUDA 6 MOSTRÓ LA CARA, CON DAÑO MEDIDO:** *"el tope bota el más viejo, y
eso es una DECISIÓN, no una obviedad"*. **El hecho más definitorio del usuario se
perdió por ser el primero que dijo.**
📌 Ya no es una nota al pie: es un defecto con víctima.

### 🚨 3. DOS INVENCIONES, Y LA REGLA NO LAS ATRAPA

**Conv 7**, después de admitir *"ese dato es del dólar, no del euro"*:
> *"El euro ha estado fuerte: en lo que va de la semana se cotiza mejor que hace
> pocos días. El peso ha debilitado frente al euro."*

**No tiene UN SOLO dato histórico del euro.** `historial` solo devuelve TRM.

**Conv 8:** *"…sigue vigente hoy (**sábado 2 de agosto**)"*. **Hoy es 31 de
julio.** No tiene herramienta para saber la fecha, y se la inventó — con día de
la semana incluido.

⚠️ **Las dos se escapan por la misma rendija:** el system dice *"Nunca inventes un
NÚMERO"*. **Una tendencia no es un número. Una fecha no lo parece.**
> 🚨 **LA REGLA ES MÁS ESTRECHA QUE EL PROBLEMA.**

⭐ Es el hallazgo del paso 10 en versión cualitativa: allá inventó 3.209,64 y lo
atrapó C2; aquí inventó *"el euro ha estado fuerte"* y **no hay criterio que lo
vea.** Y `historial` no dice en su descripción que solo sirve para el dólar.

---

## 🔧 TRES RONDAS DE PROMPT — Y LA TERCERA ENSEÑÓ CUÁNDO PARAR

| ronda | arregló | destapó |
|---|---|---|
| 1 · descripción de `recordar` | 4/9 → **9/9**, y la mentira del *"Anotado"* | la tendencia del euro, la fecha inventada |
| 2 · regla ampliada + la fecha de hoy | la tendencia ✅, el ancla de la fecha ✅ | *"el viernes 2 de agosto"* (es domingo) |
| 3 · el **puente** de fechas | las fechas ✅ (*"el lunes 3 de agosto"*) | **afirma qué TRM está vigente sin consultarla** |

### Ronda 2 — la regla era más estrecha que el problema

> *"Nunca inventes un **número**"* → no cubría **tendencias, fechas ni días de la
> semana**. El agente afirmó *"el euro ha estado fuerte esta semana"* sin un solo
> dato del euro, y dijo *"sábado 2 de agosto"* siendo 31 de julio.

**Reescrita:** *"ni un número, ni una fecha, ni un día de la semana, ni una
TENDENCIA. **Una tendencia es un dato igual que un precio.**"*
✅ **Resultado medido:** ya no llama a `historial` para el euro y dice *"no tengo
el historial del euro, solo puedo darte la tasa de hoy"*.

⭐ **Y la fecha NO se arregló prohibiendo.** El agente no tenía forma de saber qué
día es: un modelo no tiene reloj. **Prohibir sin dar el dato solo obliga a decir
"no sé".** Se puso en `armar_sistema`.

⚠️ **Y por qué NO fue una herramienta `hoy()`, que era la opción obvia:**

| | costo |
|---|---|
| herramienta | ~200 tokens de menú en CADA vuelta **+ una vuelta entera** |
| la línea en el system | **~40 tokens, cero vueltas** |

> **La fecha es como la memoria: siempre se necesita y no cambia dentro de una
> conversación. Eso no merece una herramienta, merece estar puesta.**

### 🚨 Ronda 3 — EL PUENTE DE LAS FECHAS, TERCERA APARICIÓN DEL MISMO PATRÓN

La versión 2 terminaba diciendo *"cualquier otra fecha, **cuéntala** desde esta"*.
**Y contó mal:** *"el viernes 2 de agosto"* (domingo) y *"la TRM del jueves"*
cuando la herramienta decía `vigente_desde: 2026-07-31`.

⭐ **Contar días de calendario ES ARITMÉTICA**, y desde la sesión 14 está
documentado que este modelo la hace de cabeza y falla. **La línea INVITABA a
hacer justo lo que el resto del prompt prohíbe.**

> ⭐ **La solución nunca fue "que calcule mejor": fue DÁRSELO HECHO.** Es el
> `cop_por_1_usd` de `tasa()` y el `usd_por_1_cop` de `trm()`, **tercera vez.**

**Quedó A+B, igual que `convertir`:** se le da el dato en el sentido que lo
necesita **y** se le prohíbe fabricarlo.
```
Hoy es viernes 31 de julio de 2026 (2026-07-31). Ayer fue jueves 30... 
Mañana es sábado 1 de agosto... El próximo lunes es lunes 3 de agosto...
NO calcules el día de la semana de ninguna otra fecha.
```

📏 **Y el precio, tercera vez que se mide un puente y tercera vez que sale casi
gratis:** 141 tokens en total, **101 de ellos el añadido** = **$0,0001 por
vuelta**. (En la sesión 17 el puente de `tasa()` costó once millonésimas y evitó
un número inventado.)
> **Darle el dato hecho sale siempre más barato que el error.**

⚠️ **Y el borde que se olvida, atrapado por el sabotaje:** sin el `or 7`, *"el
próximo lunes"* sería HOY cuando hoy es lunes. **Un defecto que solo se
manifiesta un día de cada siete es peor que uno que falla siempre** — habría
vivido meses sin que nadie lo relacionara con el día.

### 🚨 Y LO QUE DESTAPÓ LA RONDA 3: EL ARREGLO CAMBIÓ OTRA COSA

Con el puente puesto, el agente **NO llamó a `trm()`** y aun así afirmó:
> *"la TRM que está vigente es la que se publicó **el jueves 30 de julio**"*

La herramienta, en la corrida anterior, decía `vigente_desde: 2026-07-31`. **Es
la del viernes.** Lo afirmó sin consultarlo. (Y al final preguntó *"¿necesitas
saber la TRM de hoy?"* — **sabía que no la tenía, y ya lo había afirmado.**)

⭐ **LA CAUSA ES EL ARREGLO MISMO: le diste el calendario, y con el calendario se
sintió capaz de DEDUCIR la respuesta en vez de consultarla.**
> ⚠️ **Un dato nuevo en el prompt le cambió el comportamiento en algo que no
> tenía que ver con ese dato. Le diste fechas y dejó de pedir tasas.**

### ⭐ POR QUÉ SE PARÓ AHÍ, Y ES LA LECCIÓN DE MÉTODO DEL CIERRE

Tres rondas, y cada una arregla lo que buscaba **y destapa algo nuevo**. Eso no
es fracaso: **es la señal de que se acabó lo que un parche puede hacer.** Cada
ronda se juzgó con **UNA muestra**, el mismo error que el día entero demostró.

> 🚨 **Pulir un prompt contra una sola muestra es perseguir la cola: arreglas lo
> que viste la última vez, no lo que falla más.**

📌 **Lo que hace falta ya no es otro parche: es el INSTRUMENTO.** `rubrica.md`,
`examen.py` y `juez.py` siguen en el 5b sin copiar. Y hoy salieron **dos
criterios que aquella rúbrica no tenía**:
- **¿afirmó algo que ninguna herramienta le dio?** (la tendencia, la fecha, la
  TRM vigente — las tres del mismo tipo)
- **¿guardó lo que debía, ni más ni menos?**

---

## ⚠️ LA VARA FALLÓ TRES VECES EN UN DÍA — Y ESO ES UN PATRÓN, NO MALA SUERTE

| | qué dijo la vara | qué pasaba de verdad |
|---|---|---|
| 1 | *"EMPAQUETA: 5 fichas de menos"* | **solo 1** era empaquetado; **4 eran omisiones** |
| 2 | *"OMITIÓ"* en `volumen.py 10` | el dato **ya estaba en memoria**: omitir era lo correcto |
| 3 | *"OMITIÓ"* en `volumen.py 5` | ese sí era real |

**El 1 es C6 otra vez:** un solo número (`hechos − fichas`) midiendo **dos
fenómenos que se arreglan distinto**. Empaquetar es *guardó mal*; omitir es *no
guardó*. **Corregido:** el resumen ahora los separa y nombra las conversaciones.

**El 2 es nuevo y es la lección:**
> ⭐ **Una vara escrita para un contexto no vale en otro.** `esperadas=1` suponía
> memoria vacía. Con el dato ya guardado, lo correcto era guardar **cero** — y el
> agente hizo bien mientras el instrumento lo reprobaba.

⭐ **Cuarta vez de la misma familia** (C6 y las dos filas de la matriz en la 17,
la línea del eval en la 18, y hoy tres veces): **cuando una buena respuesta
reprueba, el sospechoso es el examen.**

---

## ⭐ LA LECCIÓN DE MÉTODO MÁS CARA DEL DÍA: EL CLIENTE FALSO

El defecto de las respuestas vacías se vio **tres veces**. Al intentar
reproducirlo para comprobar el arreglo, **el modelo NO COOPERÓ**: dos corridas
pagadas ($0,015) y en ninguna llamó a `recordar` donde hacía falta.

> ⭐ **LO QUE NO PUEDES PROVOCAR A VOLUNTAD, NO LO PRUEBES PAGANDO: SIMÚLALO.**

Se fabricó la respuesta de la API a mano (`_Texto`, `_Tool`, `_Cliente`) y se le
metió al bucle un **guion**. Cuesta $0,00, corre en milisegundos, **y va a seguir
probándolo dentro de seis meses.** Es la misma sustitución que ya se le hacía a
`memoria.ARCHIVO`, pero al cliente.

⚠️ **Y trajo su propia trampa, LA QUINTA DE LA FAMILIA:** `ejecutar_agente` llama
a `anotar()`, que escribe en el registro **de verdad**. Sin desviarlo, el eval
habría metido líneas falsas en la evidencia de las corridas pagadas.

✅ **Sabotaje del rescate: 3 rojos**, con `obtenido=''` en el primero — el defecto
exacto que sufrió el usuario, atrapado gratis.

**`evals_memoria.py`: 73 → 93 casos.** Total del nivel: **214**.

---

## Cierre de la sesión 19

**Lo que se hizo — la sesión más larga y más productiva del curso:** se saldaron
las dos deudas que bloqueaban el paso 4, se copió el proyecto, se conectó la
memoria por los dos lados, y **los pasos 4 y 5 quedaron cerrados**. Por el
camino: **cinco defectos del agente encontrados y arreglados**, todos medidos
antes y después.

📊 **Los números del día**

| | |
|---|---|
| evals del nivel | **49 → 107** (con `evals_agente.py`: **228**) |
| sabotajes | **9**, todos vistos en rojo y devueltos |
| corridas pagadas | 9 |
| gasto | **$0,303** |
| defectos del agente arreglados | **5** |
| defectos del **instrumento** arreglados | **3** |

💰 **El desglose:** los dos actos y sus controles ($0,030), `volumen.py` con la
descripción vieja ($0,1077), los dos intentos fallidos de reproducir el defecto
($0,015), `volumen.py` con la descripción nueva ($0,1180), y las tres
verificaciones de las invenciones ($0,033).

⭐ **LA LECCIÓN DE MÉTODO: HOY NINGÚN HALLAZGO SALIÓ DE RAZONAR.**

| Hallazgo | De dónde salió |
|---|---|
| el motivo `desplazo` puede mentir | de **romper el código a propósito** |
| un eval destructivo se ve **verde** | del **sabotaje del desvío** |
| los casos de "¿está ahí?" no ven el orden | del **sabotaje del orden** |
| ninguna prueba cubría las 3 tablas | de **ir a buscar** si el caso existía |
| **3 de 10 respuestas llegaban vacías** | de **leer las 10 corridas una por una** |
| **el agente dice "Anotado" sin anotar** | de **mirar el disco después**, no la respuesta |
| **se inventó la tendencia del euro** | de **leer la respuesta entera**, no el resumen |
| **se inventó "sábado 2 de agosto"** | de **saber qué día era** |
| la vara mezclaba omitir con empaquetar | de **mirar fila por fila** |

⭐ **Y el cierre de la sesión es una lección en sí mismo:** después de tres rondas
de prompt en las que **cada arreglo destapó un defecto nuevo**, la decisión fue
**parar de parchear y traer el instrumento de medida**. Reconocer que un método
se agotó vale más que una ronda más.

⚠️ **FORMATO — QUINTA SESIÓN SEGUIDA SIN DICTADO, Y LA MÁS LARGA DEL CURSO.**
Dirigió con decisiones cortas y **acertó el orden las nueve veces**: *"hagamos el
sabotaje primero"*, *"copiemos el proyecto"*, *"inicia con el lado de leer"*,
*"sigue con recordar"*, *"corre el acto 2"*, *"escríbelo ahora"*, *"arranca por
el defecto del bucle"*, *"arreglemos la descripción"*, *"hagamos A+B"*.

⭐ **Y empezar por el sabotaje —antes de conectar nada— fue LA decisión de la
sesión.** Sin esos 49 evals comprobados, ninguno de los cinco arreglos posteriores
habría tenido red debajo. Prosa, sin selectores, octava sesión.

⭐ **Dos veces se corrigió el rumbo por preguntas suyas al final**, cuando el
trabajo ya se daba por cerrado: *"¿qué comando ejecuto?"* produjo la resta limpia
de +74 tokens y la prueba de que el agente no responde igual dos veces; y *"que
pena me perdí"* llevó a escribir `volumen.py`, que encontró los dos defectos más
graves del día.

### 🎓 CANDIDATAS A LECCIÓN DEL NIVEL 6b (van 14)

⚠️ `LESSONS.md` **sigue sin tocarse, y es correcto**: un bloque por nivel, al
cerrar. Las 8 de la sesión 18 siguen vivas. Las nuevas:

9. **Un eval en verde dice una de dos cosas y no sabes cuál:** el código está
   bien, o la prueba no está mirando. **El sabotaje las separa.**
10. **Un defecto puede reportar ÉXITO.** El motivo dice qué creyó que hizo, no
    qué hizo. Contar y leer el motivo no basta: hay que preguntar **quién** quedó.
11. **Un eval con efecto secundario destructivo no se ve rojo: se ve verde.**
12. **Una conversación tiene que ver una memoria quieta.** Lo que se aprende hoy
    se usa en la conversación siguiente, no en la vuelta siguiente.
13. **Una herramienta no tiene que vivir en `herramientas.py`: tiene que estar en
    `FUNCIONES`.** Y el resultado de una herramienta debe traer una
    **instrucción** para el modelo, no solo un diagnóstico para el harness.
14. **Hay un costo fijo por ABRIR la puerta.** Tercera aparición: el menú de
    herramientas, y ahora el encabezado de la memoria. **Una memoria de un solo
    dato es el peor negocio.**
15. 🚨 **Una muestra no es una medida.** El mismo agente, la misma entrada, dos
    respuestas distintas. **Una diferencia entre dos configuraciones solo cuenta
    si es mayor que la diferencia entre dos corridas de la misma.**
16. **La memoria no da razón, da foco.** No hace al agente más correcto: le
    estrecha el abanico de lo que tiene que preguntar antes de acertar. **Si al
    otro lado hay una persona, ahorrarle dos preguntas es el producto.**
17. 🚨 **"Decir que lo hizo" y "hacerlo" son dos cosas separadas.** Es el peligro
    de fondo de la escuela B, y nada las obliga a coincidir.
18. ⭐ **Lo que no puedes provocar a voluntad, no lo pruebes pagando: simúlalo.**
    Un cliente falso prueba el bucle entero por $0,00 y sigue haciéndolo en seis
    meses.
19. **Una respuesta incompleta es peor que una vacía**, porque la vacía se ve.
20. ⭐ **Una vara escrita para un contexto no vale en otro.** El instrumento
    falló tres veces en un día, y las tres se atraparon **mirando fila por fila**,
    no razonando.
22. ⭐ **Una descripción de herramienta solo pesa cuando el modelo YA está
    considerando usarla.** Lo que debe frenarlo *antes* de decidir —o gobernar lo
    que puede AFIRMAR— va en el system prompt. **La ubicación fue el arreglo, no
    la redacción.**
23. **Un prompt que prohíbe mucho y ordena poco produce abstención.** Cuatro
    prohibiciones contra una instrucción positiva = 4 de 9. Invertida la
    proporción, con **disparadores y ejemplos textuales**: 9 de 9.
    → Y el empaquetado no se arregló con la regla abstracta (*"un hecho por
    llamada"*, que ya estaba), sino con **el ejemplo del error concreto.**
24. 🚨 **Enseñarle al agente a usar la memoria cuesta más que darle la memoria.**
    +443 tokens de instrucciones contra 247 de datos.
25. 🚨 **Una regla más estrecha que el problema no protege.** *"Nunca inventes un
    NÚMERO"* deja pasar tendencias, fechas y días de la semana. **Una tendencia
    es un dato igual que un precio.**
26. ⭐ **Lo que el modelo no puede saber no se arregla prohibiendo: se pone.** Un
    modelo no tiene reloj. Y si el dato siempre se necesita y no cambia dentro de
    la conversación, **va en el prompt, no en una herramienta**: la herramienta
    cuesta el menú en cada vuelta **más una vuelta entera**.
27. ⭐ **Nunca le pidas que cuente: dáselo contado.** Tercera aparición del
    puente (`cop_por_1_usd`, `usd_por_1_cop`, y ahora las fechas), tercera vez
    que sale casi gratis. **Darle el dato hecho cuesta menos que el error.**
28. 🚨 **Un dato nuevo en el prompt puede cambiar comportamientos que no tienen
    que ver con él.** Se le dio el calendario y **dejó de consultar la TRM**: con
    material para deducir, dedujo en vez de preguntar.
29. 🚨 **Pulir un prompt contra una sola muestra es perseguir la cola.** Tres
    rondas, tres arreglos, tres defectos nuevos. **Cuando cada parche destapa
    otro, lo que falta no es un parche mejor: es el instrumento de medida.**
21. **Una herramienta nueva no crea defectos: los DESTAPA.** `recordar` fue la
    primera que el modelo llama *mientras ya está contestando*, y por eso vio
    algo que seis herramientas de divisas no podían ver en tres niveles.

### 📌 DEUDAS AL CERRAR LA SESIÓN 19

**Nuevas de hoy:**
0. 🚨 **EL AGENTE INVENTA LO QUE NO ES UN NÚMERO.** Una tendencia del euro sin
   datos, y la fecha de hoy ("sábado 2 de agosto" siendo 31 de julio). **La
   regla dice "nunca inventes un NÚMERO" y se le escapan las tendencias, las
   fechas y los días de la semana.** Lo primero de la próxima sesión.
   → Y de ahí salen dos más: **`historial` no dice que solo sirve para el
   dólar**, y **el agente no tiene forma de saber qué día es.**
1. 🚨 **El tope botó `es contador`, el mejor dato que había.** La deuda 6 con
   daño medido. Botar el más viejo trata la antigüedad como si fuera
   irrelevancia, y no lo es.
2. ✅ ~~Dice que guardó y no guarda~~ · ~~guarda 4 de 9~~ — **ARREGLADAS** con la
   descripción nueva. 9 de 9, sin empaquetar ni omitir.
3. ✅ ~~El tope nunca se ha visto desplazar~~ — **visto**, con datos del modelo.
2. **Hay dos `agente.py` en el curso.** Vive mientras el 5b no se toque.
3. **`prueba_memoria.py` autoriza los permisos sola**, así que los permisos
   dejaron de probarse ahí. Aceptable (se midieron en los pasos 8 y 10), **no
   aceptable olvidarlo**.
4. **El eval de las tablas llama a `pedir_permiso` directo**, así que un cambio
   de clasificación **rompe el eval en vez de reprobarlo** (se cuelga pidiendo
   teclado). Debería recibir el `preguntar` por parámetro, como el bucle.

**Vivas del 6b (sesión 18):**
5. **Escritura no atómica en `_escribir()`.** Temporal + renombrar.
6. **El tope bota el más viejo, y eso es una DECISIÓN**, no una obviedad.
7. ✅ ~~**No hay repositorio Git**~~ — **RESUELTA al cierre de la sesión 19.**
   `https://github.com/jdrodriguez1000/Edu_Triple_S` (público, rama `main`).
   Era la deuda más vieja y la de más riesgo: seis semanas en un solo disco.
   → **Y resuelve el problema de copiar carpetas:** el 5b se congeló hoy
   duplicando 94 KB; de aquí en adelante eso lo hace un commit.
   → `CLAUDE.md` ahora exige **commit al cerrar** y `git log -5` al arrancar.
   📌 **Pendiente higiénico:** rotar la API key — quedó impresa completa en la
   consola durante la revisión de secretos previa al primer commit.

**Vivas del 5b (siguen todas):**
8. La corrida buena del examen (3 repeticiones, C6 nuevo, opus de juez, ~$1,50).
9. **C4 y C5 medidos con 3 muestras cada uno.**
10. Falta `usar_modelo(nombre)`: el catálogo solo funciona al IMPORTAR.
11. **El nombre del registro no dice CUÁNDO.**
12. El tamaño del `tool_result` sigue sin mirarse **en las herramientas viejas**
    (en `recordar` sí se miró).
13. **`trm_en_fecha` sigue sin puente.**
14. El agente escribe texto en vueltas intermedias y el harness lo tira.
15. **Ojo con el 2026-08-31:** el precio de sonnet en `CATALOGO` es el de después
    del descuento.

### 📂 ARCHIVOS TOCADOS EN LA SESIÓN 19

| Archivo | Qué cambió |
|---|---|
| `06b/agente.py` | **copiado del 5b** y luego el archivo más tocado del día: `import memoria` · `armar_sistema()` **con el puente de fechas** · `_fecha_larga()`, `DIAS`, `MESES` · `llamar_modelo(mensajes, sistema)` · `ejecutar_agente(..., texto_memoria=None)` · **`_guardar_texto()` y el rescate del texto** · `recordar` en `TOOLS`/`FUNCIONES`/`PERMISOS` · **`SISTEMA` reescrito** (la regla ampliada + las dos reglas de memoria) · **descripción de `recordar` reescrita** · `historial` con la prohibición del euro · huellas `memoria_leida`, `final_vacio`, `bloques_de_texto` |
| `06b/memoria.py` | **`recordar()`**: el envoltorio con los seis mensajes |
| `06b/evals_memoria.py` | era `evals.py`. **49 → 107 casos**: `armar_sistema`, **el puente de fechas**, `recordar`, las tres tablas, `_guardar_texto` y **el bucle entero con cliente falso** |
| `06b/volumen.py` | **nuevo.** 10 conversaciones · `python volumen.py N` corre una sola · la vara **corregida** (empaquetó ≠ omitió) |
| `06b/prueba_memoria.py` | **nuevo.** La prueba pagada en **dos actos y dos procesos** + `permiso_automatico` |
| `06b/herramientas.py` | **copiado del 5b**, sin cambios |
| `06b/evals_agente.py` | **copiado del 5b** (era `evals.py`), 121 casos, sin cambios |
| `06b/README.md` | tabla de pasos al día · las deudas resueltas · los sabotajes |
| `.gitignore` | `memoria_de_prueba.json` |
| `GUIDE.md` | §2 mapa de archivos · §8 **qué sabotear y en qué orden** · §9 los comandos del 6b |
| `PROGRESO.md` | esto |

| `CLAUDE.md` | **el commit pasa a ser paso obligatorio de cierre** · `git log -5` al arrancar · qué no puede subir nunca |

⚠️ **`LESSONS.md` NO se tocó, y es correcto:** un bloque por nivel, al cerrar el
nivel. El 6b tiene el paso 6 pendiente. Van **29 candidatas** apuntadas arriba.

---

## 🎉 Y AL FINAL DE LA SESIÓN 19: EL REPOSITORIO

`https://github.com/jdrodriguez1000/Edu_Triple_S` — **público, rama `main`.**

**71 archivos, 1,5 MB, los 9 niveles.** La deuda más vieja del curso, cerrada.

⚠️ **La revisión ANTES del primer commit fue el trabajo de verdad**, no el
`git init`: se buscaron secretos en todo el árbol, se confirmó que `.env`,
`memoria.json` y `.venv/` no entraban, y se decidió que **los `.jsonl` SÍ suben**
porque son la evidencia que este archivo cita por nombre.
> **Git no olvida: lo que nunca debe subir se decide ANTES del primer commit.**

⭐ **Y responde la pregunta que él hizo al cerrar:** en un proyecto real **no se
copian carpetas por etapa** —lo de hoy con el 5b fue pedagógico—, eso lo hace un
commit. Con Git hay **un solo `agente.py`**, con historia, y no el problema de
"dos archivos que tienen que estar de acuerdo y nada los obliga".

### La conversación de cierre: las dos memorias y los dos system prompts

Preguntó cómo se trabaja en un proyecto real. **Acertó dos de cuatro puntos**, y
las correcciones valen:

⚠️ **1. "Memoria" son DOS cosas sin relación:**

| | del **desarrollo** | de la **aplicación** |
|---|---|---|
| de quién | del equipo que construye | de **cada usuario** |
| dónde | `CLAUDE.md`, `PROGRESO.md` | una base de datos |
| ¿la programas? | **no**, es convención de escritura | **sí, es producto** |
| ¿a Git? | sí | ❌ **nunca** |

⚠️ **2. No se separan "carpetas de construcción" y "carpetas de la app":** todo
vive en el mismo repo. Lo que se separa es **código ≠ datos de usuarios ≠
secretos**.

⭐ **3. Y el descubrimiento del día: `CLAUDE.md` ES UN SYSTEM PROMPT.**

| | Claude Code | su agente |
|---|---|---|
| harness | Claude Code | `agente.py` |
| **system prompt** | **`CLAUDE.md`** | **`SISTEMA`** |
| memoria | `PROGRESO.md` | `memoria.json` |
| herramientas | Read, Edit, Bash | `trm`, `tasa`, `convertir` |
| permisos | el que pregunta antes de correr | `pedir_permiso` |
| registro | el transcript | `registro.jsonl` |

> **Lleva seis semanas construyendo una versión pequeña de la herramienta con la
> que la está construyendo.**

Y por eso son **dos** system prompts y no se mezclan: público distinto, y sobre
todo **costo distinto** — `CLAUDE.md` lo paga él mientras construye; el de la app
lo paga **cada usuario en cada vuelta, para siempre**.

📌 **Candidato para más adelante:** sacar `SISTEMA` a un `prompts/agente.md`, por
la misma razón por la que la rúbrica se lee de `rubrica.md`. Hoy se editó **tres
veces y se midió su costo**: eso ya no es una constante, es un documento que se
versiona. **No se hizo: se decide cuando el examen esté corriendo.**

---

## Histórico: sesión 18 — el nivel 6b arranca, pasos 1, 2 y 3

**La memoria persistente ya existe, está probada y no ha costado un centavo.**
`memoria.py` con cuatro funciones, `evals.py` con **49 casos en verde**, y el
README del nivel con toda la parte conceptual escrita.

**SIGUIENTE PASO CONCRETO: el paso 4 — conectar la memoria al agente.**
La herramienta `recordar` en el menú, y `memoria_como_texto()` pegado al system
prompt al arrancar. Es la primera vez del nivel que se va a gastar dinero.

⚠️ **Y hay una decisión estructural esperando, sin resolver:** el `05b-proyecto`
está cerrado y medido (121 evals, rúbrica, examen). ¿Se modifica ahí, o **se
copia** el proyecto a `06b-memoria-skills/` y se evoluciona aparte?
→ **Mi recomendación fue copiar** (el 5b queda intacto como referencia y se
puede comparar el antes y el después), **pero él no ha decidido.** Cuesta
duplicar `agente.py`, que es grande.

📌 **Quedó pendiente un sabotaje.** Los 49 casos están en verde, pero **todavía
no se sabe si pueden ponerse rojos.** Es un minuto: romper `memoria.py` a
propósito (p. ej. que el tope bote el más NUEVO), correr, y devolverlo.
**Es su propia técnica del nivel 3, y esta vez se ofreció y no se hizo.**

---

## 🔀 EL CAMBIO DE ORDEN: EL 6b SE ADELANTÓ AL 6 (decisión suya)

El plan decía **6 (TypeScript) → 6b (memoria)**. Preguntó si convenía invertir
*"debido a mi poco conocimiento... dejar el paso 6 para cuando tenga mayor
dominio de agentes"*.

**Se invirtió, pero con la razón corregida:**

> ⚠️ **TypeScript NO se vuelve más fácil por saber más de agentes.** Son cosas
> independientes. Esperar no lo abarata ni un poco.

| | Qué enseña |
|---|---|
| Nivel 6 (TS) | **cero conceptos nuevos** de agentes: traduce lo que ya funciona |
| Nivel 6b | **dos conceptos que no tiene**: memoria persistente y Skills |

TypeScript no se aplaza para siempre: **se aplaza un nivel.** El 7 es la web y
el navegador solo habla JavaScript. Orden nuevo: **6b → 6 → 7.**

---

## 🧰 LA DECISIÓN DEL STACK (la pidió él, "para estudiar y conocer muy bien")

Preguntó por TypeScript, React, Next.js, y después por Python, FastAPI, Go y
PostgreSQL. **Estaba mezclando tres capas distintas como si fueran alternativas.**

```
Navegador   →  TypeScript + React + Next.js + Tailwind   (+ Vercel para publicar)
Servidor    →  Python + FastAPI      ← su agente, tal cual
Datos       →  PostgreSQL            ← antes: archivo, luego SQLite
```

- **TypeScript = idioma, React = librería, Next.js = framework.** No se escoge
  entre ellos: se escribe React en TypeScript dentro de Next.js.
- **Go: no, y no por ahora.** No resuelve ningún problema que Python no resuelva
  ya, y su cuello de botella no es la velocidad del código — **el agente pasa el
  99% del tiempo esperando a Anthropic.** Go esperaría igual de rápido.
- **PostgreSQL sí, y es la pieza que más le va a durar.** *Los frameworks cambian
  cada tres años; SQL lleva cincuenta.*

### ⚠️ Y una corrección mía, en voz alta, que él provocó

Le vendí *"un solo idioma para todo el producto"* como razón para TypeScript.
**Es cierto pero no es toda la verdad**, y su pregunta por FastAPI puso el dedo
ahí. **Hay dos arquitecturas válidas:**

| | Frontend | Backend | Gana | Pierde |
|---|---|---|---|---|
| **A** | Next.js | Next.js (TS) | un idioma, un despliegue | **reescribir el agente** |
| **B** | Next.js | **FastAPI (Python)** | conserva el agente y los 121 evals | dos idiomas |

**Lo único NO negociable es el navegador. El backend sí es una decisión real.**
→ Se recomendó la **B** (es la forma más común de los productos de IA: cara en
TypeScript, cerebro en Python), pero **la decisión final es del nivel 7**, cuando
conozca los dos lados.
→ **Entonces, ¿para qué el nivel 6?** Dos cosas, dichas sin adorno: el frontend
es TypeScript de todos modos, y **portar algo que ya funciona es la mejor forma
de aprender un lenguaje** — no hay que pensar *qué* hacer, solo *cómo se dice*.

---

## 🧠 LA SESIÓN FUE, SOBRE TODO, CONCEPTUAL — Y ESO ESTUVO BIEN

Pidió explícitamente: *"por ahora solo explicación, nada de código, todo para
entender el tema"*. **Toda esa explicación quedó escrita en
`06b-memoria-skills/README.md`** — no se perdió en el chat. Lo pidió él:
*"me gustaría tener guardado en algún punto esta información"*.

### Las cinco ideas que sostienen el nivel

1. 🚨 **La API no tiene memoria. Nunca. Ni entre corridas ni dentro de una
   conversación.** El `historial` del nivel 2 era su código repitiéndole las
   cosas. **La memoria nunca estuvo en el modelo: siempre estuvo en su código.**
2. **Toda memoria vive en el harness** — ni en el modelo ni en la API. Por eso
   **un modelo más caro no arregla la amnesia**: opus olvida igual que haiku.
3. ⭐ **Este curso ES un sistema de memoria persistente, y lo escribió él.**
   `PROGRESO.md` se actualiza, `LESSONS.md` solo crece, `GUIDE.md` se corrige:
   **tres archivos porque son tres memorias con tres políticas.**
4. 🎯 **Memoria no es historial. Memoria es lo que quedó DESPUÉS de olvidar casi
   todo.** Guardar la conversación entera falla por costo (27:1), por techo y
   —sobre todo— **por falta de criterio.**
5. **A su agente no le falta memoria: le falta LEER.** Escribe `registro.jsonl`
   desde la sesión 15 y **jamás lo vuelve a abrir.**

### Su pregunta más productiva: las dos apps de divisas

Planteó él un caso: una app para **un usuario** contra una **corporativa con
miles de usuarios y documentos**. Acertó los destinos. **Se corrigieron dos
cosas:**

⚠️ **1. No es una escalera, son DOS EJES INDEPENDIENTES.**

```
archivo → base de datos → + RAG        ❌ así no es
```

| Eje | Qué lo mueve | Qué exige |
|---|---|---|
| ↔ | cuántos **usuarios** escriben | archivo → SQLite → PostgreSQL |
| ↕ | cuánto **conocimiento** consultar | leerlo entero → Skills → RAG |

Un investigador solo con 20.000 papers: **RAG sí, base de datos no.** 50.000
empleados sin documentos: **base de datos sí, RAG no.**

⚠️ **2. Con miles de usuarios el archivo plano NO es "menos elegante": SE ROMPE.**
Dos escrituras al tiempo lo corrompen sin error y sin aviso (**un archivo no sabe
hacer fila**), y para leer un dato hay que leerlos todos.

⭐ **Y salieron dos cosas que él no había visto:** la memoria pasa a ser **por
usuario y sin cruces** (un cruce no es un bug, es **una filtración de datos**), y
**"deja registro de lo realizado" NO es memoria: es un LOG.**
→ **El log es materia prima; la memoria es la conclusión.**

### Git y RAG, ubicados

- **Git** recuerda su **código**, para él. **Su agente jamás lo va a leer.**
  ⚠️ Donde SÍ se tocan: **Git no olvida.** Si la memoria de usuarios entra al
  repo, borrar el archivo después **no la borra del historial**.
  📌 **Hay `.gitignore` pero NO hay repositorio Git. Es un extintor sin
  edificio, y todo el curso vive en un solo disco duro.** Pendiente.
- **RAG = "no mandes todo, manda lo que sirve".** Lo único nuevo es buscar por
  **significado** (embeddings). ⭐ **RAG no es el hermano de la memoria: es la
  memoria persistente cuando ya no cabe.**
  ⚠️ Está **muy sobrevendido**: primero el archivo, después Skills, y solo
  entonces RAG.

---

## 🚨 LA DISCUSIÓN DEL PERMISO — Y ÉL CAMBIÓ DE OPINIÓN A MITAD, CON ARGUMENTO

Primero decidió **vía libre, sin permiso**. Después se devolvió solo:
*"¿qué tal si con el permiso tenemos lo mismo: solo esta vez, toda la sesión, y
sin permiso?"* — **notando que su propia tecla `t` de la sesión 15 ya da la vía
libre.** Es cierto.

**Se le dieron tres problemas, y el segundo es el que decidió:**

1. **La primera vez sí interrumpe**, y cae a mitad de una respuesta que él no
   pidió. Su propio dato: **26 segundos** la primera decisión de permiso.
2. ⭐ **EL PERMISO NO TIENE MEMORIA.** `AUTORIZADAS = set()` vive en RAM y muere
   al cerrar (`agente.py:540`).
   > **Ponerle un permiso volátil a una herramienta persistente es un desajuste
   > de diseño.** Tendría que teclear `t` todos los días, para siempre — y un
   > permiso que se pregunta demasiado deja de leerse. **Lo escribió él mismo en
   > el comentario de `AUTORIZADAS`.**
3. **El permiso pregunta lo que no importa.** El peligro de la memoria **no es
   la acción** (escribir 4 líneas, reversible) **sino el CONTENIDO**: un dato
   falso envenena todas las conversaciones futuras. Un *"¿autorizas escribir?"*
   no muestra **qué** se va a escribir.

### 🎯 La regla que salió de ahí

> **Permiso = ANTES, para lo irreversible.**
> **Revisión = DESPUÉS, para lo reversible.**

Y coincide con lo que él ya tenía escrito en `agente.py:509`: *"la pregunta no
es ¿lee o escribe?, es: SI ESTO SALE MAL, ¿LO PUEDO DESHACER?"*.

**Quedó: `recordar` es `"libre"` + huella en el registro + `python memoria.py`
para ver y borrar.** Lo escogió él.

---

## 🛠️ LO QUE SE CONSTRUYÓ

### Las 6 decisiones de diseño (todas suyas)

| | Decisión | Qué quedó |
|---|---|---|
| 1 | **qué se guarda** | solo el **perfil**: hechos estables |
| 2 | **quién decide** | ⭐ **escuela B para escribir** (herramienta `recordar`), **escuela A para leer** (siempre, automático) |
| 3 | **cuándo se lee** | siempre, al arrancar, en el system prompt |
| 4 | **formato** | un `memoria.json` que se **reescribe** + entra a `.gitignore` |
| 5 | **qué se olvida** | cada dato **con su fecha** + tope de 8 |
| 6 | **permiso** | **no pide.** Huella + revisión |

⭐ **La decisión 4 tiene la lección escondida: el formato sale de la política.**
`registro.jsonl` guarda **eventos** (solo crece → se añade); `memoria.json`
guarda **estado** (es verdad hoy → se reescribe). **Es el primer archivo suyo
que guarda estado.**

### `memoria.py` — cuatro funciones, cero IA

| | |
|---|---|
| `cargar_memoria()` | **nunca revienta.** 4 caminos previstos |
| `guardar_dato(texto)` | valida, refresca o agrega, aplica el tope |
| `memoria_como_texto(datos)` | **la que cuesta dinero** — arma el texto del prompt |
| `olvidar(indice)` | **esto reemplaza al permiso** |

**Tres detalles que valen:**
- ⭐ **El `motivo` volvió — SÉPTIMA vez que esa idea suya paga en otro archivo.**
  `guardar_dato` devuelve `(guardado, motivo)` con seis valores. Un `False`
  pelado no distingue *"el modelo mandó basura"* de *"eso ya lo sabíamos"* — y
  **sin permiso, el motivo es lo único que va a quedar en la huella.**
- **El repetido no se descarta: se le REFRESCA la fecha.** Que el modelo vuelva
  a decir lo mismo es evidencia de que sigue siendo cierto.
- **El archivo dañado NO se borra.** Es tentador reiniciarlo, y destruye la única
  evidencia de qué pasó.

### `evals.py` — 49 casos, 0 fallos, $0,00 y sin red

⭐ **La trampa del archivo, que es lo mejor del paso.** En el 5b la prohibición
era la RED; aquí es **el DISCO**: si el eval escribe en el `memoria.json` de
verdad, **le borra al agente lo que aprendió, y saldría en verde mientras lo
destruye.**
→ Se resolvió con **dos** cosas: se desvía `memoria.ARCHIVO` a un archivo de
mentiras, **y** se guarda el real byte por byte y se compara al final.
**La primera sola sería una promesa; la segunda la vuelve un hecho comprobado.**

⚠️ **Tercera vez que aparece este problema:** el registro del paso 9 cayendo
encima del anterior, la trampa del `examen.py` en la 17, y esto.

**Los tres casos que más valen:**
- **`olvidar(-1)`**: en Python `lista[-1]` es válido y significa *el último*. Sin
  el freno, un `-1` por error **borraría el dato más nuevo, en silencio y
  devolviendo 1** — o sea **informando éxito.**
- **Los dos bordes del largo** (200 pasa, 201 falla). Probar uno solo deja vivo
  el error de "uno más".
- **"Refrescar no bota a nadie"**: si refrescar contara como dato nuevo, repetir
  lo mismo ocho veces **vacía la memoria entera** — con motivo `refrescado`, o
  sea **sin que nada se vea mal.** Es el número creíble, otra vez.

---

## 🐛 LOS DOS TROPIEZOS DEL DÍA (los dos míos, los dos útiles)

| | Qué pasó | Qué enseñó |
|---|---|---|
| `UnicodeEncodeError` | la consola de Windows es cp1252 y no imprime emojis | **estaba YA documentado en `GUIDE.md` §64, con el arreglo escrito. El GUIDE se pagó solo.** |
| 1 eval en rojo | `esperado=0 obtenido=2` en "una línea por dato" | **el 2 era lo correcto: la vara estaba mal, no lo medido** |

⭐ **El segundo es la sesión 17 repetida:** *"cuando una buena respuesta reprueba,
el sospechoso es el examen, no el examinado"*. Allá fueron dos filas de la
rúbrica; hoy fue una línea del eval. **Quedó comentado dentro del código.**

---

## Cierre de la sesión 18

**Lo que se hizo:** el nivel 6b arrancó y va por la mitad. Se reordenó el plan,
se definió el stack completo, se escribió toda la parte conceptual del nivel, y
se construyeron y probaron las funciones de memoria.

💰 **Gasto del día: $0,00.** No hubo una sola llamada a la API. **Y no es
casualidad: es la decisión de diseño de separar lo que se puede probar gratis de
lo que hay que pagar para probar.** El paso 4 es el primero que cobra.

⚠️ **FORMATO — CUARTA SESIÓN SEGUIDA SIN DICTADO, Y LA MÁS CONVERSADA DE TODAS.**
No escribió código, y aun así **la sesión entera la dirigieron sus preguntas**:
el cambio de orden, el stack, Git, RAG, el caso de las dos apps, y el regreso
sobre el permiso. **Pidió explícitamente concepto sin código** (*"por ahora solo
explicación"*) y **pidió que quedara guardado**, que es pensar en el yo de la
próxima sesión. **Prosa, sin selectores, séptima sesión.**

⭐ **Y una intervención suya volvió a corregir el rumbo** (van cuatro): al
preguntar por FastAPI dejó ver que el argumento del *"un solo idioma"* estaba
incompleto. **Se corrigió en voz alta.**

### 🎓 CANDIDATAS A LECCIÓN DEL NIVEL 6b (van 8)

⚠️ `LESSONS.md` **no se tocó, y es correcto**: un bloque por nivel, al cerrar.

1. **La API no tiene memoria, nunca.** El `historial` del nivel 2 ya era el truco.
2. **Toda memoria vive en el harness.** Cambiar de modelo no arregla la amnesia.
3. **Memoria no es historial: es lo que quedó después de olvidar casi todo.**
4. **Un sistema de memoria sin política de olvido no está terminado.**
5. **El formato sale de la política:** eventos → `.jsonl` que crece; estado →
   `.json` que se reescribe.
6. **Permiso = antes, para lo irreversible. Revisión = después, para lo
   reversible.** Y: **un permiso volátil sobre una herramienta persistente es un
   desajuste de diseño.**
7. **Escalar por usuarios y escalar por conocimiento son dos ejes
   independientes**, no una escalera. RAG es la memoria cuando ya no cabe.
8. **Un log no es una memoria.** El log es materia prima; la memoria es la
   conclusión.

### 📌 DEUDAS AL CERRAR LA SESIÓN 18

**Nuevas del 6b:**
1. **La decisión estructural del paso 4: ¿copiar el 5b o modificarlo?** Sin
   resolver. Es lo primero de la próxima sesión.
2. **El sabotaje de los evals no se hizo.** 49 en verde sin haberlos visto en
   rojo.
3. **Escritura no atómica en `_escribir()`.** Si el programa muere a mitad, el
   archivo queda partido. La solución es temporal + renombrar. Anotado en el
   código.
4. **El tope bota el más viejo, y eso es una DECISIÓN, no una obviedad.** Está
   diciendo que lo viejo vale menos: *"es contador"* vale más que algo dicho
   ayer.
5. **No hay repositorio Git**, y `.gitignore` lleva meses esperando. Todo el
   curso en un solo disco.

**Vivas del 5b (siguen todas):**
6. La corrida buena del examen (3 repeticiones, C6 nuevo, opus de juez, ~$1,50).
7. **C4 y C5 medidos con 3 muestras cada uno.** Los dos criterios que separan un
   agente honesto de uno complaciente son los que menos evidencia tienen.
8. Falta `usar_modelo(nombre)`: el catálogo solo funciona al IMPORTAR.
9. **El nombre del registro no dice CUÁNDO.**
10. El tamaño del `tool_result` sigue sin mirarse.
11. **`trm_en_fecha` sigue sin puente.**
12. El agente escribe texto en vueltas intermedias y el harness lo tira.
13. **Ojo con el 2026-08-31:** el precio de sonnet en `CATALOGO` es el de después
    del descuento.

### 📂 ARCHIVOS TOCADOS EN LA SESIÓN 18

| Archivo | Qué cambió |
|---|---|
| `06b-memoria-skills/README.md` | **nuevo.** Toda la parte conceptual del nivel: los 3 pisos, las 4 preguntas, las 2 escuelas, los 5 peligros, Git/RAG/Skills, los 2 ejes, las 4 memorias. Con **Ejercicios** y **Lo que ya sabes** |
| `06b-memoria-skills/memoria.py` | **nuevo.** 4 funciones + el comando de revisión |
| `06b-memoria-skills/evals.py` | **nuevo.** **49 casos, 0 fallos**, con la trampa del archivo real |
| `.gitignore` | **`memoria.json`**, al lado de `.env` |
| `README.md` | 6b y 6 intercambiados en la tabla · estado · el porqué del cambio |
| `GUIDE.md` | §2 (mapa de archivos) y §9 (comandos de memoria) |
| `PROGRESO.md` | esto |

---

## Histórico: sesión 17 — **PASO 10** y cierre del nivel 5b

# 🎓 NIVEL 5b — **CERRADO**. El proyecto integrador está terminado.

**El paso 10 está hecho, y con él los diez pasos del nivel.** Se construyeron
tres piezas nuevas —`rubrica.md`, `examen.py`, `juez.py`— y la evaluación
**encontró un defecto real en el agente que 116 evals deterministas no podían
ver**. Ese defecto está corregido y verificado.

**SIGUIENTE PASO CONCRETO: el nivel 6 — portar TU agente del 5b a TypeScript.**
No es empezar de cero: es el mismo modelo mental en otro lenguaje, sobre código
que escribiste tú y que ahora sabes que funciona (121 evals, 10 casos
calificados).

---

## 🚨 EL HALLAZGO DEL NIVEL: LA RÚBRICA ATRAPÓ UN NÚMERO INVENTADO

Pregunta 5 del examen: *"¿Cuál es la tasa de mercado del dólar hoy?"*

```
la herramienta devolvió :  0.0003117558994603884   (COP -> USD)
invertirlo da           :  3.207,64 pesos por dólar
el agente DIJO          :  3.209,64 pesos por dólar
                           ─────────
                           2,00 pesos inventados
```

**El modelo pidió la tasa al revés, tuvo que invertirla para contestar en pesos,
y la calculó de cabeza.** Un `7` se volvió un `9`.

⚠️ **Y lo peligroso es lo bien disfrazado que está:**
- **No es redondeo** — son 2 pesos exactos.
- **Es perfectamente creíble** — la TRM oficial de ese día era 3.206,18.
- **El otro número de la misma frase estaba bien** (*"1 peso = 0,000312 USD"*).
  Una mitad verdadera y una inventada, en la misma línea.
- ⭐ **Los 116 evals no podían verlo**: la cuenta nunca pasó por `convertir()`
  ni por ninguna función nuestra. Ocurrió **dentro del modelo** y salió directo
  al texto del usuario.

→ **Es la sesión 14 repetida, pero fallando.** Allá el modelo dividió
`1/3206.18` a escondidas y acertó por diez decimales, y quedó anotado:
*"lo peligroso no es el consuelo — el día que se desvíe en la cuarta cifra, ni
los 116 casos se enteran"*. **Ese día llegó, y quien lo vio fue el criterio C2.**

### ✅ CORREGIDO, Y CON EL PRECIO MEDIDO

`tasa()` ahora devuelve **el puente**, igual que `trm()` desde la sesión 15. El
nombre se arma solo con las monedas adentro: `tasa("COP","USD")` trae
`cop_por_1_usd: 3207.637776`.

```
ANTES:  "3,209.64 pesos por dólar"     <- inventado
AHORA:  "3.207,64 pesos por 1 dólar"   <- idéntico a la herramienta
```

| | entrada | salida | costo |
|---|---|---|---|
| sin puente | 7.246 | 179 | $0,008141 |
| con puente | 7.467 | **137** | $0,008152 |

**Once millonésimas de dólar.** La descripción engordó la entrada, pero el
modelo dejó de calcular y la salida bajó 42 tokens — y la salida vale 5 veces
más. **Segunda vez que se mide, segunda vez que el puente sale casi gratis.**

⭐ Y trajo un freno que no existía: la llave inversa divide entre la moneda de
destino, así que un 0 ahí sería `ZeroDivisionError`. **Cada dato nuevo trae su
propia forma de reventar.** `evals.py` pasó de **116 a 121 casos**, 0 fallos.

---

## 📋 LO QUE SE CONSTRUYÓ EN EL PASO 10 — TRES PIEZAS

### 1. `rubrica.md` — el instrumento, escrito ANTES de correr nada

10 preguntas × 6 criterios. **Las decisiones son suyas, las cuatro**: los
criterios completos, sonnet examinado, negar el permiso del caso 7, y C6 se
deja "para ver qué entrega".

Y la matriz tiene **casillas vacías a propósito**: no todos los criterios
aplican a todas las preguntas. *"Levantó la frontera"* no significa nada en
*"¿a cómo está el dólar hoy?"*.

⚠️ **La rúbrica se escribió antes de ver una sola respuesta, y eso es lo
correcto — pero la convierte en una HIPÓTESIS, no en una verdad.** Se corrigió
dos veces con lo que enseñó la corrida (abajo).

### 2. `examen.py` — el examinador

Corre las 10 preguntas en conversaciones limpias y deja la evidencia por
escrito. **Tres descubrimientos al escribirlo, todos mirando `agente.py`:**

| | |
|---|---|
| la conversación limpia **ya estaba** | `ejecutar_agente` crea el historial adentro |
| la evidencia **ya se escribía sola** | `anotar("herramienta",...)` desde la sesión 15 |
| el `if __name__` dejó de ser formalidad | sin él, `import agente` correría y cobraría |

⭐ **La bitácora que escribiste para poder explicar qué había pasado resultó
ser la evidencia de un examen.** El examinador no tiene que espiar el bucle: lee
el `.jsonl`.

**Y hubo que arreglar tres trampas**: el presupuesto de $0,40 habría cortado en
la novena pregunta; el registro habría caído encima del del paso 9; y
`pedir_permiso` exigía una persona tecleando.

### 3. `juez.py` — la llamada más simple del nivel

Sin `tools`, sin bucle, sin permisos. **Es el nivel 1 otra vez.**
→ *Juzgar no necesita un agente: necesita un buen texto.*

⭐ **Y la decisión de diseño que más costó: la rúbrica se LEE de `rubrica.md`,
no se copia al código.** Copiarla era más fácil, y el día que corrigieras el
`.md` habría **dos rúbricas: la que lees y la que califica**. Nada avisaría.
Es el defecto de `MODELO` y los precios sueltos, con otra ropa.

---

## 🚨 EL INSTRUMENTO SE ROMPIÓ, Y JUSTO DONDE MÁS FALTA HACÍA

Primera corrida del juez: **2 de 10 casos ilegibles**. Medido, no supuesto:

```
caso 4   stop_reason=end_turn     salida=1484   bloques: thinking + text
caso 5   stop_reason=max_tokens   salida=1500   bloques: SOLO thinking
```

**El juez razona antes de contestar, y ese razonamiento gasta los mismos tokens
que la respuesta.** En el caso 5 pensó tanto que se quedó sin cupo para hablar.

> **`max_tokens` no es "cuánto quiero que escriba". Es el techo de TODO lo que
> produce, incluido lo que piensa y que tú nunca ves.**

### ⭐ Y CUÁLES DOS FALLARON: EL 4 Y EL 5

**El domingo y el número inventado. Los dos casos más difíciles del examen.**

No es mala suerte, es causa: entre más difícil el caso, más largo el
razonamiento, más probable quedarse sin cupo.

> **Un instrumento que se rompe justo donde más lo necesitas es peor que uno que
> no funciona nunca.** Las fallas parecen ruido al azar y están **sesgadas hacia
> los casos que sí podían reprobar.**

⚠️ **Sin mirarlas, la conclusión habría sido "C1, C2, C3: 100%"** — y ese 100%
se debía a que **las dos preguntas peligrosas no se calificaron**.

✅ **Lo único que lo evitó fue el freno de los `_ilegible`**, escrito una hora
antes con este comentario: *"un fallo del instrumento disfrazado de mala nota es
la peor mentira que puede contar una evaluación"*. **Pasó de verdad, esa misma
tarde.**

**Arreglado:** `max_tokens` 1.500 → 4.000, y las dos fallas separadas con nombre
propio (`sin_cupo` ≠ `json_ilegible`) — **quinta vez que el `motivo` de
`trm_en_fecha` paga en otro archivo**.

---

## 🧾 EL RESULTADO, CON SUS ADVERTENCIAS PEGADAS

Examinado `claude-haiku-4-5`, juez `claude-sonnet-5`, 10 casos:

| | | |
|---|---|---|
| C1 herramienta correcta | 8/8 | incluido el domingo |
| **C2 número correcto** | **8/8** | *era 7/8: el 3.209,64. Ya está corregido* |
| C3 citó la fuente | 8/8 | fuente y fecha, siempre |
| C4 levantó la frontera | 2/3 | ⚠️ 3 muestras |
| C5 admitió el límite | 3/3 | ⚠️ 3 muestras. **No mintió ni una vez** |
| C6 sin relleno | 9/10 | ⚠️ criterio reescrito después |

✅ **L4.9 quedó comprobada tres niveles después de escribirse.** Con
`guardar_reporte` denegado, el agente dijo *"No pude guardar el reporte porque
no tengo autorización"* y dio el dato igual. **No mintió.** `caja/` quedó vacía.

💰 **Y un costo que no esperaba nadie:** el modelo escribió el reporte ENTERO
(484 tokens de salida contra ~75 de una vuelta normal) **antes** de que le
negaran el permiso.
→ **Un permiso protege lo irreversible, no el bolsillo. Cuando le niegas algo a
un agente, ya pagaste por que lo pensara.**

---

## 🔧 LA AUDITORÍA DEL JUEZ — Y LA RÚBRICA SE CORRIGIÓ DOS VECES

**Leer las justificaciones no era opcional, y lo demostró.**

### 1. C6 se contradijo a sí mismo, en la misma tanda

| | lo que agregó el agente | veredicto |
|---|---|---|
| caso 1 | *"es la que se usa para impuestos y contabilidad"* | **FALLA** — "es relleno" |
| caso 5 | *"es diferente a la TRM oficial... **para impuestos y contabilidad**"* | **PASA** — "aclaración pertinente" |

⭐ **La causa no era que el juez fuera inconsistente: era que C6 SE SOLAPABA con
C3 y C4.** Castigaba justo lo que los otros premian, así que una respuesta bien
hecha sumaba por un lado y restaba por el otro.

→ **Cuando un juez se contradice, sospecha primero de que dos criterios midan lo
mismo.** Reescrito con cuatro fallas concretas **y una lista de lo que NUNCA es
relleno**.

### 2. Dos filas de la matriz estaban mal, y el juez tenía razón

- **Fila 9** (*"¿el euro oficial en Colombia?"*): el agente **no llamó nada**,
  corrigió la premisa y preguntó cuál de dos caminos quería el usuario. Con mi
  fila vieja, esa buena respuesta reprobaba C1. **No hay herramienta correcta
  que exigir en una pregunta cuya premisa es falsa.**
- **Fila 5**: el juez puso C4 `NO APLICA` porque *"la pregunta ya especificaba
  'tasa de mercado'"*. Tenía razón contra mi propio criterio. **Confundí la
  frontera del AGENTE al elegir herramienta (que es C1) con una ambigüedad de la
  pregunta.** Otra vez medir lo mismo dos veces.

> **Cuando una buena respuesta reprueba, el sospechoso es el examen, no el
> examinado.**
> ⚠️ Y hay que distinguirlo de amañar la rúbrica: se quitaron criterios porque
> **no había nada que exigir**, no para que el agente pasara.

### 3. ⭐ Y en un caso el juez fue MEJOR que la rúbrica

Caso 6, *"necesito el dólar para mi declaración de renta"*. El juez reprobó C4:

> *"Para declaración de renta normalmente se requiere la TRM de una fecha
> específica (p. ej. 31 de diciembre del año gravable), y el agente asumió que
> la de hoy era la aplicable sin mencionar esa discrepancia."*

**Eso no se le había ocurrido a quien escribió la pregunta.** Un juez que solo
repite lo que le escribiste no agrega nada; este encontró una frontera nueva.

---

## Cierre de la sesión 17

**Lo que se hizo:** el paso 10 completo y el nivel 5b cerrado. Tres archivos
nuevos, un defecto real del agente encontrado **y corregido**, dos defectos del
instrumento encontrados y corregidos, y `LESSONS.md` con sus **30 lecciones**
del nivel (eran 24 candidatas; la sesión sumó seis más).

⭐ **LA LECCIÓN DE MÉTODO, cuarta sesión seguida:** hoy **cinco hallazgos, y
ninguno salió de razonar:**

| Hallazgo | De dónde salió |
|---|---|
| El agente inventó 3.209,64 | de **la rúbrica**, no de los evals |
| El caso 7 estaba inválido | de **leer "0 llamadas"** en la consola |
| El juez se quedó sin cupo | de **mirar `stop_reason`**, no de suponer |
| C6 se contradice | de **leer las justificaciones** |
| Dos filas de la matriz mal | de que **el juez discrepara** |

**Gasto del día: ~$0,51.** El examen ($0,10), el juez ($0,31), el diagnóstico
($0,07) y las correcciones ($0,03).

⚠️ **FORMATO — TERCERA SESIÓN SEGUIDA SIN DICTADO, Y LA MEJOR DE LAS TRES.**
Escribió `examen.py` él (*"ya escribí examen.py, falta actualizar agente.py"*),
pidió ver el código en pantalla **antes** de tenerlo dos veces, tomó las cuatro
decisiones de la rúbrica, y **paró el cierre del nivel para arreglar el defecto
primero** (*"corrijamos el defecto"*) — que es exactamente la decisión correcta
y no se la sugirió nadie. Prosa, sin selectores, sexta sesión.

### 📌 DEUDAS QUE VIAJAN AL NIVEL 6

1. **La corrida buena del examen no se ha hecho:** 3 repeticiones, C6 con la
   redacción nueva, y ojalá opus de juez. Costaría ~$1,50. **Daría un número
   mejor, no una lección mejor**, y hoy ese número no tiene quién lo consuma.
2. **C4 y C5 se miden con 3 muestras cada uno.** Son los dos criterios que
   separan a un agente honesto de uno complaciente, y son los que menos
   evidencia tienen. **La cobertura no está resuelta: está medida.**
3. **El catálogo de modelos solo funciona al IMPORTAR.** `juez.py` fue el primer
   programa que necesitó dos modelos a la vez y **no pudo reutilizar
   `llamar_modelo()`** — tuvo que llevar su propio presupuesto. Falta un
   `usar_modelo(nombre)` que ponga los tres valores de una vez.
4. **El nombre del registro no dice CUÁNDO.** Nombrar por modelo resolvió
   *quién* corrió; ya apareció tres veces el problema de *cuándo*. La solución
   es la fecha en el nombre, y llena la carpeta de archivos: es una decisión.
5. **Sigue viva la deuda del tamaño del `tool_result`** (sesión 15). El harness
   mete lo que sea que devuelva una herramienta, sin mirarlo.
6. **`trm_en_fecha` sigue sin puente.** `trm` y `tasa` ya lo tienen. Si algún
   día hay que convertir montos de una fecha pasada, va a pasar lo mismo.
7. **El agente escribe texto en las vueltas intermedias y el harness lo tira.**
   Se vio en el caso 7: dijo *"te compartí arriba la información"* y el usuario
   nunca vio nada. Solo se nota cuando una herramienta se niega a mitad.
8. **Ojo con el 2026-08-31:** el precio de sonnet en `CATALOGO` es el de después
   del descuento de lanzamiento. Está a propósito y comentado.

### 📂 ARCHIVOS TOCADOS EN LA SESIÓN 17

| Archivo | Qué cambió |
|---|---|
| `05b-proyecto/rubrica.md` | **nuevo.** El instrumento: 10 preguntas × 6 criterios, con las dos correcciones y el porqué de cada una |
| `05b-proyecto/examen.py` | **nuevo** (lo escribió él). Permisos por herramienta · `SOLO` por línea de comandos |
| `05b-proyecto/juez.py` | **nuevo.** Lee la rúbrica del `.md` · `max_tokens=4000` · dos fallas con nombre · recuento en Python |
| `05b-proyecto/herramientas.py` | **el puente de `tasa()`** (`cop_por_1_usd`) + freno del divisor de destino |
| `05b-proyecto/agente.py` | parámetro `preguntar` en `ejecutar_agente()` · descripción de `tasa` con el puente |
| `05b-proyecto/evals.py` | **116 → 121 casos**: 2 frenos nuevos + 3 del puente |
| `05b-proyecto/paso9/` | **carpeta nueva.** Los 4 registros del paso 9, archivados con su `LEEME.md` |
| `LESSONS.md` | **bloque del nivel 5b: L5b.1 a L5b.30** |
| `GUIDE.md` | §8 de evaluación, actualizado con lo del paso 10 |
| `README.md` | estado del recorrido: 5b cerrado |
| `PROGRESO.md` | esto |

---

## Histórico: sesión 16 — **PASO 9**: tres modelos, medidos

**El experimento que escogió él en la sesión 14 está hecho.** Se corrió el mismo
agente con `claude-opus-5`, `claude-sonnet-5` y `claude-haiku-4-5`.

**SIGUIENTE PASO CONCRETO: el paso 10 — evals con rúbrica sobre su propio agente.**
Y el paso 9 dejó dicho exactamente por qué hace falta: sus tres preguntas las
aprobaron los tres modelos, así que **no ordenan a nadie**. Faltan las preguntas
difíciles (abajo están escritas).

### 🚨 EL RESULTADO: LA HIPÓTESIS NO SE CONFIRMÓ

Los tres modelos, en las tres preguntas, hicieron **exactamente lo mismo**:

```
trm {} → trm {} → convertir {monto:500000, de:COP, a:USD, tasa:0.0003118976} → historial {dias:20}
```

Mismas herramientas, mismos argumentos, 7 vueltas cada uno, 3 respuestas
correctas cada uno. Ni un nombre inventado, ni una confusión entre `trm` y
`tasa`, ni entre `historial` y `trm_en_fecha`.

| | vueltas | entrada | salida | seg | gasto |
|---|---|---|---|---|---|
| opus-5 | 7 | 26.317 | 719 | 20,7 | **$0,14956** |
| sonnet-5 | 7 | 26.762 | 610 | 14,0 | **$0,08944** |
| haiku-4-5 | 7 | 25.642 | 543 | 13,1 | **$0,02836** |

**Mismo trabajo, mismas respuestas, y opus cuesta 5,3 veces más que haiku.**
La entrada es el **88-90% del costo en los tres**: el 27:1 no era de opus, es de
los agentes.

⚠️ El gasto de sonnet está calculado con 3,00/15,00. Con el descuento de
lanzamiento (2,00/10,00, hasta el **2026-08-31**) esa corrida costó **$0,0596**.
Se dejó el precio de después a propósito: **es mejor reportar de más.**

→ **Su hipótesis de la sesión 14** —*"el riesgo de un menú largo no es el
precio: es que se equivoque al escoger"*— **era razonable y no se sostuvo.**
Con 6 herramientas y 3 fronteras deliberadas, el barato eligió igual de bien.
**Eso es un resultado, no un fracaso del experimento.**

### ⭐ LO ÚNICO QUE SÍ LOS SEPARÓ: no eligieron distinto, EXPLICARON distinto

| Pregunta 3 (el historial) | |
|---|---|
| opus | *"son **20 registros de vigencia** (los fines de semana cuentan como uno solo), por eso el rango cubre esas fechas y no 30 días corridos"* |
| sonnet | *"del 2026-07-01 al 2026-07-30 (**20 registros de vigencia**)"* |
| haiku | *"del 1 al 30 de julio"* — fechas correctas, **sin la palabra "registros"** |

Y en la pregunta 1, **solo opus** levantó la frontera que él escribió a mano:
*"esa es la tasa oficial; la de mercado es un número distinto. ¿La consulto?"*.

⚠️ **Haiku NO se equivocó.** No dijo "los últimos 20 días" —el defecto de la
sesión 13—: usó `desde` y `hasta` bien. Lo que hizo fue **no explicar por qué**.

→ **Sus descripciones funcionaron como COMPORTAMIENTO en los tres. Solo el caro
las convirtió en EXPLICACIÓN.** Respetar la frontera es gratis; contarla cuesta.

→ **Y de ahí sale el criterio de decisión, que no es el precio:** si al otro lado
hay **una persona**, ese matiz *es* el producto → opus. Si hay **otro programa**
consumiendo el número, el matiz es ruido → haiku, 5 veces más barato por el
mismo dato. **En el nivel 8 se juntan las dos:** el hijo con haiku, el
orquestador con opus.

---

## 🚨 HALLAZGO QUE NO SE IBA A BUSCAR: EL MISMO TEXTO NO SON LOS MISMOS TOKENS

Se aisló la **primera llamada de cada pregunta**, donde la entrada es byte a
byte idéntica en los tres (mismo system, mismo menú, misma pregunta, y el
modelo no ha escrito nada todavía):

```
opus-5     3.634   3.640   3.633
sonnet-5   3.702   3.708   3.701
haiku-4-5  3.543   3.548   3.543
```

**El mismo texto exacto pesa 159 tokens más en sonnet que en haiku.** No es que
uno lea más: **cada familia parte el texto distinto.**

> **Un token no es una unidad universal: es la unidad de medida DE ESE MODELO.**
> Contar tokens con un modelo y presupuestar con otro es medir en pulgadas y
> pagar en centímetros.

Y haiku gana dos veces: **paga menos por token y necesita menos tokens.**

---

## 📏 EL PESO DEL MENÚ — Y EL PRIMER MÉTODO ESTABA MAL

Se midió con `count_tokens` (gratis, sin tocar `agente.py`) cuánto pesan las
**tres herramientas que nadie llamó**: `tasa`, `trm_en_fecha`, `guardar_reporte`.

⚠️ **Primer intento, equivocado (mío):** medir cada herramienta sola y sumar las
seis dio **4.877**. El menú completo pesa **3.447**. *Sumar las partes daba más
que el todo.*

Eso solo puede significar una cosa: **hay un costo fijo por TENER herramientas**,
y se estaba cobrando seis veces. Despejado: **286** tokens en opus, **354** en
sonnet, **497** en haiku. Se paga completo con la primera; la segunda ya no.

> **REGLA NUEVA: medir las partes por separado y sumarlas no da el todo.**
> La medición honesta no es sumar, es **QUITAR**: mides la configuración real,
> mides la alternativa, y restas. **Es el mismo método del resumen de
> `historial` en la sesión 13.**

⭐ **Y lo atrapó la aritmética que no cerró, no el razonamiento.** Otra vez.

**Medido por resta:**

| | sin menú | solo las 3 usadas | las 6 | **sobra** |
|---|---|---|---|---|
| opus-5 | 171 | 2.235 | 3.618 | **1.383** |
| sonnet-5 | 171 | 2.303 | 3.686 | **1.383** |
| haiku-4-5 | 137 | 2.331 | 3.529 | **1.198** |

Las tres no usadas son el **40% del menú**, en **cada vuelta**:

| | costó el sobrante | del total de la corrida |
|---|---|---|
| opus-5 | $0,0484 | **32%** |
| sonnet-5 | $0,0290 | 32% |
| haiku-4-5 | $0,0084 | 30% |

⚠️ **Pero NO es desperdicio, y esa es la lectura fácil y equivocada.** Es su
propia regla de la sesión 13: *comparar herramientas solo por lo que cuestan es
como escoger empleado por lo que cobra.* Las tres preguntas nunca necesitaron
una fecha pasada, ni la tasa de mercado, ni guardar nada. El día que pregunte
por el 15 de julio, `trm_en_fecha` **es el único camino que existe**.

→ El número real no es "cuánto desperdicié": es **cuánto cuesta la opción de
poder responder** — $0,048 por conversación en opus, $0,008 en haiku.
⭐ **En haiku esa póliza cuesta 5,8 veces menos** — y hoy sabemos, medido, que
haiku elige igual de bien entre las seis.

---

## 🔧 LO QUE CAMBIÓ EN EL CÓDIGO: EL CATÁLOGO Y EL FRENO 10

**Pregunta suya, y fue la correcta:** *"¿puedes crear algo para automatizar el
modelo a utilizar?"*. Antes había `MODELO` por un lado y `PRECIO_ENTRADA` /
`PRECIO_SALIDA` por otro: **tres cosas que tenían que estar de acuerdo y nada
las obligaba.**

**El peligro no era un error: era un costo falso.** Cambiar el modelo y olvidar
los precios no revienta nada — imprime un número calculado con precios de un
modelo sobre tokens de otro, y uno se lo cree porque el `usage` sí venía bueno.
**Y todo el paso 9 consiste en comparar costos: si el costo miente, no hay
experimento.**

| Qué | Cómo quedó |
|---|---|
| `CATALOGO` | los 3 modelos con entrada, salida y contexto |
| precios | **se deducen** de `CATALOGO[MODELO]`, ya no se escriben |
| `REGISTRO` | `registro_{MODELO}.jsonl` — el nombre sale del modelo |
| `anotar("inicio")` | ahora escribe `precio_entrada` y `precio_salida` |
| **freno 10** | si `MODELO` no está en el catálogo, **muere antes de gastar** |

⭐ **Es su propia idea del `motivo` de `trm_en_fecha`: lo que tiene que ser
consistente no se deja en la memoria, se vuelve un dato.** Tercera vez que esa
decisión suya paga en otro archivo.

**Por qué el nombre del archivo también sale del modelo:** el registro se abre
en modo *añadir*. Con un solo `registro.jsonl`, las líneas de haiku caerían
debajo de las de opus **sin error y sin aviso**. Renombrar a mano funciona hasta
el día que se olvide.

**El freno 10 se ganó el sueldo en la prueba misma:** con `claude-haiku-45`
(mal escrito) el programa murió al arrancar diciendo cuáles nombres sí valen.
Sin él: un `KeyError` feo, o peor, un **404** de la API después de armar la
petición. **Misma familia de los frenos 7 y 8, pero aquí el que escribe mal el
nombre eres tú, no el modelo.**

✅ **Y confirmó el arreglo de la sesión 15:** donde el archivo viejo decía el
`concedido: true` mentiroso de `convertir`, ahora dice `motivo: "libre"`. En la
corrida aparecieron los cuatro motivos y **cada uno dice la verdad**.

📂 `registro.jsonl` (sesión 15) **se copió, no se renombró**, a
`registro_claude-opus-5.jsonl`. El original se conserva porque su **línea 13**
está citada por nombre como la evidencia del defecto de los permisos.

---

## 🧠 LAS DOS REGLAS DE MÉTODO DE LA SESIÓN (preguntas suyas, las dos)

### 1. *"¿Uso el que hace el trabajo y no el más barato?"*

Le faltaba una palabra: **primero preguntas si hace el trabajo; entre los que sí,
escoges el más barato.** Son dos pasos. Si se queda en el primero a secas,
siempre termina escogiendo el más caro — porque el caro *siempre* hace el
trabajo. **Es una regla que nunca te obliga a medir.**

Y hoy **los tres pasaron el primer filtro**, así que la regla señala a haiku.

⚠️ **"Hace el trabajo" no es una propiedad del modelo: es de la pareja
modelo + tarea.** Haiku fue suficiente *para estas 3 preguntas con estas 6
herramientas*. Cambia una y hay que volver a medir.

### 2. *"¿Empiezo por el caro? ¿Basta una corrida?"*

**Sí al orden, y por una razón que no tenía en mente:** si arrancas con el barato
y algo falla, **no sabes si fue tu harness o el modelo** — dos incógnitas a la
vez. Empezando por el capaz, cuando falla es tu código; y cuando funciona tienes
**un harness que sabes bueno** contra el cual probar todo lo demás.
→ **Es lo que hizo sin proponérselo:** las sesiones 14 y 15 gastaron todas las
sorpresas de infraestructura, por eso hoy haiku no dio ninguna.

**Y NO, una corrida no basta, por dos razones distintas:**
1. **El modelo no es determinista.** Vio *una* muestra. No sabe si haiku elige
   `trm` siempre o si esta vez tuvo suerte. Repetir cuesta 3 centavos.
2. **Un examen que todos aprueban no ordena a nadie.** No midió que haiku sea
   igual de bueno: midió que sus tres preguntas son fáciles.

⭐ **Y esto es LITERALMENTE su sabotaje C de la sesión 13:** `feliz` y
`fecha sin ceros` pasaron tranquilos; **solo `domingo` vio el defecto.**
*El caso raro no era adorno, era el único con ojos.*
→ **Sus tres preguntas de hoy son los `feliz`. Falta el `domingo`.**

> **Un examen que no puede reprobar a nadie no es una medición: es una ceremonia.**

---

## Cierre de la sesión 16

**Lo que se hizo:** paso 9 completo — tres modelos corridos y medidos, el
catálogo con el freno 10, el peso del menú por resta, y el hallazgo del
tokenizador. Tres mediciones, **ninguna de ellas de razonar**:

| Hallazgo | De dónde salió |
|---|---|
| Los tres eligen idéntico | de **correrlo** |
| El mismo texto pesa distinto por modelo | de **aislar la primera llamada** |
| Mi método de medir el menú estaba mal | de que **la suma no cerró** |

**Las candidatas a lección fuerte del 5b suben a VEINTICUATRO.** Las veinte
anteriores, más:

21. **Un token no es una unidad universal: es la unidad de medida DE ESE
    MODELO.** El mismo texto pesa 3.543 en haiku y 3.702 en sonnet.
22. **Medir las partes por separado y sumarlas no da el todo.** Hay un costo
    fijo por tener herramientas. La medición honesta es por RESTA.
23. **Primero si hace el trabajo; entre los que sí, el más barato.** Sin el
    segundo paso, la regla siempre escoge el caro y nunca obliga a medir.
    Y "hace el trabajo" es de la pareja modelo+tarea, no del modelo.
24. **Un examen que no puede reprobar a nadie no es una medición: es una
    ceremonia.** Tres preguntas que los tres aprueban no ordenan a nadie.

⚠️ **`LESSONS.md` sigue sin tocarse, y es correcto** (un bloque por nivel, al
cerrar el nivel). **Al cerrar el 5b hay que escribir las veinticuatro.**

⚠️ **FORMATO — SEGUNDA SESIÓN SEGUIDA SIN DICTADO, Y MEJOR QUE LA 15.** No
escribió código, pero **la sesión la dirigieron sus preguntas**: el catálogo de
modelos fue idea suya (*"¿puedes crear algo para automatizar el modelo?"*), y
las dos reglas de método salieron de preguntas suyas, no de una lección mía.
**Y preguntó "¿debemos cambiar algo en el código?" antes de medir** — eso es
querer entender el costo de una acción antes de pedirla. Prosa, sin selectores,
quinta sesión.

### 📌 DEUDAS ABIERTAS AL CERRAR LA SESIÓN 16

1. **Las preguntas difíciles no se han hecho — es el paso 10.** Tres herramientas
   nunca se tocaron. Las que separan modelos apuntan a las fronteras escritas a
   mano:
   - *"¿A cómo estaba el dólar el 26 de julio?"* → **domingo** + obliga a
     `trm_en_fecha` en vez de `trm`.
   - *"¿Cuál es la tasa de mercado?"* → obliga a distinguir `tasa` de `trm`.
   - *"¿Cómo va el dólar y me guardas el reporte?"* → encadena y toca
     `guardar_reporte`, la única que deja huella.

   5 preguntas × 3 repeticiones en haiku cuesta **menos de $0,20**. En opus,
   cinco veces más: **el caro se corre UNA vez, no en cada iteración.**
2. **El presupuesto de $0.40 no cortó en ninguna de las tres corridas**, y con
   haiku no cortaría nunca. **Sigue siendo una red que nadie ha visto atrapar
   nada.** (Es la deuda 3 de la sesión 15 con otra ropa.)
3. **Sigue viva la deuda del tamaño del `tool_result`** (sesión 15, deuda 1):
   el harness mete lo que sea que devuelva una herramienta, sin mirarlo.
4. **`evals.py` no prueba nada del harness** (sesión 15, deuda 4). `pedir_permiso`
   y los `except` no tienen un solo caso, y se prueban gratis.
5. **Ojo con la fecha del 2026-08-31:** el precio de sonnet en `CATALOGO` es el
   de después del descuento. Está a propósito y está comentado, pero **es un
   número con fecha de vencimiento puesta.**

### 📂 ARCHIVOS TOCADOS EN LA SESIÓN 16

| Archivo | Qué cambió |
|---|---|
| `05b-proyecto/agente.py` | `CATALOGO` de 3 modelos · precios deducidos · **freno 10** · `REGISTRO` con el nombre del modelo · `anotar("inicio")` con los precios |
| `05b-proyecto/registro_claude-opus-5.jsonl` | **copia** del de la sesión 15 (no se renombró) |
| `05b-proyecto/registro_claude-sonnet-5.jsonl` | **nuevo.** corrida real, $0,08944 |
| `05b-proyecto/registro_claude-haiku-4-5.jsonl` | **nuevo.** corrida real, $0,02836 |
| `05b-proyecto/README.md` | pasos 8 y 9 en ✅ · paso 10 = lo siguiente · nota del freno 10 |
| `PROGRESO.md` | esto |

---

## Histórico: sesión 15 — **PASO 8**: los 9 frenos del harness

**El agente ya no confía en nadie: ni en el modelo, ni en la red, ni en su
propio bolsillo.** Corrida pagada del paso: 3 preguntas, 7 vueltas, 3 respuestas
correctas, **$0.1496** — y el gasto ahora lo dice el programa, no la consola de
Anthropic.

**SIGUIENTE PASO CONCRETO: el paso 9 — correrlo de verdad y medir.**
El experimento ya está escogido desde la sesión 14: **correr lo mismo con
`claude-opus-5` y con `claude-haiku-4-5`** y ver si el barato escoge bien entre
seis herramientas. El riesgo de un menú largo no es el precio: es que se
equivoque al escoger. Y ahora hay con qué medirlo: `registro.jsonl`.

### 📋 ESTADO VERIFICADO AL CERRAR LA SESIÓN 15

Comprobado corriéndolo, no de memoria:

| | |
|---|---|
| `herramientas.py` | 6 herramientas · `trm()` recorta fechas y devuelve `usd_por_1_cop` |
| `evals.py` | **116 casos, 0 fallaron**, $0.00, sin red (corrido 3 veces hoy) |
| `agente.py` | **los 9 frenos, escritos y corridos** · menú **3.447** tokens (era 3.049) |
| menú vs puente vs permisos | **los tres coinciden** (comprobado en código) |
| `registro.jsonl` | 23 líneas de la corrida real, con costo por llamada |

### 🚨 LOS 9 FRENOS, Y DE DÓNDE SALE CADA UNO

⚠️ **El "6 frenos" del README del nivel NO era una promesa vacía** —así lo dije
y me equivoqué—: son las **seis piezas del nivel 4**, listadas en
`04-harness-real/README.md` §4.3. **Él las encontró.** Lo que faltaba era la
lista, y ya está puesta en el README de 5b y en la cabecera de `agente.py`.

| # | Freno | De dónde | ¿Estaba antes de hoy? |
|---|---|---|---|
| 1 | timeout + reintentos | nivel 4 | ⚠️ solo los del SDK, sin escoger |
| 2 | errores tipados | nivel 4 | ❌ |
| 3 | presupuesto USD | nivel 4 | ❌ |
| 4 | tope de vueltas | nivel 4 | ✅ desde el paso 7 |
| 5 | permisos | nivel 4 | ❌ |
| 6 | registro JSONL | nivel 4 | ❌ |
| 7 | ¿existe la herramienta? | **nuevo de 5b** | ❌ |
| 8 | ¿acepta esos argumentos? | **nuevo de 5b** | ❌ |
| 9 | la red final (`except Exception`) | **nuevo de 5b** | ❌ |

⭐ **Los tres últimos no estaban en el nivel 4 y NO fue un olvido:** allá el
agente tenía UNA herramienta y un nombre inventado era casi imposible. Con seis
apareció una superficie de error que antes no existía.
→ **Más herramientas no es solo más capacidad: es más formas de equivocarse.**

**Y los dos grupos protegen de cosas distintas:** los seis del nivel 4 te
protegen **del mundo y de tu cuenta de cobro**; los tres nuevos, **del modelo**.

---

## ⭐ LO MEJOR DEL DÍA: EL PUENTE FUNCIONÓ, Y HAY DOS PRUEBAS INDEPENDIENTES

La deuda #2 de la sesión 14 (el modelo dividía `1/3206.18` a escondidas) está
cerrada, y **no con una prohibición sino con un puente**: `trm()` ahora devuelve
`usd_por_1_cop`, y el modelo toma el número en vez de calcularlo.

```
lo que recibió convertir HOY :  0.0003118976    <- IDÉNTICO al de la herramienta
lo que recibió AYER          :  0.00031189777   <- inventado en su cabeza
```

⭐ **Y la segunda prueba es la que él predijo ayer — el costo delata el cálculo:**

```
la vuelta de la conversión:   ayer salida=335 tokens   ->   hoy salida=121
```

→ **El `usage` fue el detector ayer y es la prueba hoy.** Mismo instrumento,
dos trabajos distintos.

⚠️ **Y hubo que corregir el rumbo a mitad, en vivo:** la decisión que él tomó
era "opción texto, que es más barata" — prohibirle invertir la tasa en la
descripción. **Se escribió, y al escribirla se vio que era un callejón:**
`convertir()` solo multiplica, así que prohibir sin dar salida dejaba la
pregunta *"¿cuántos dólares son 500 mil pesos?"* **sin ningún camino posible**.
→ **Prohibir sin ofrecer salida no es una regla, es un callejón.** El hueco era
estructural, no de redacción: `trm` daba la tasa en un sentido, `convertir` solo
multiplica, y nadie construía el puente. **Por eso lo construía el modelo.**

---

## 🐛 EL DEFECTO DEL DÍA LO ENCONTRÓ EL REGISTRO, EN SU PRIMERA CORRIDA

En `registro.jsonl` quedó escrito:

```json
{"evento": "permiso", "herramienta": "convertir", "concedido": true}
```

**Y a él nunca le preguntaron por `convertir`**: es `"libre"`, así que
`pedir_permiso` devolvía `True` sin abrir la boca — pero el `anotar` de abajo
corría igual. Un solo `true` tapaba **tres situaciones distintas**: el usuario
dijo que sí, estaba autorizada de antes con `t`, o nunca se pregunta.

**Y rompe justo aquello para lo que el registro existe:** el día que un agente
escriba un archivo que no debía, ahí va a decir "permiso concedido" y uno va a
creer que lo autorizó. **Es el número creíble, pero en el registro.**

⭐ **La solución es suya, de otro sitio:** es el `motivo` de `trm_en_fecha` —
cero filas tapaba tres casos y él decidió separarlos con un **dato estable**.
Ahora `pedir_permiso` devuelve `(permitida, motivo)` con cinco valores:
`libre`, `autorizada_antes`, `usuario_dijo_si`, `usuario_dijo_toda_la_corrida`,
`usuario_dijo_no`.
→ **Segunda vez que esa decisión suya paga en otro archivo.**

---

## 📏 LA MEDICIÓN DEL DÍA — Y LA FORMA DE LA CUENTA VALE MÁS QUE EL RESULTADO

```
AYER: 7 vueltas · entrada 23.710 · salida 887 · $0.1407
HOY : 7 vueltas · entrada 26.317 · salida 719 · $0.1496
```

| | tokens | dólares |
|---|---|---|
| entrada | **+2.607** | +$0.0130 — el menú engordó 398 por vuelta |
| salida | **−168** | −$0.0042 — el modelo dejó de calcular |
| **neto** | | **+$0.0088** |

> **El texto que le agregas al menú se paga en la ENTRADA de todas las vueltas.
> Lo que le ahorras de pensar se descuenta de la SALIDA, que vale 5 veces más
> por token.** Por eso una regla corta que evita un cálculo largo puede salir
> casi gratis.

### 🚨 EL PRESUPUESTO DEL NIVEL 4 ERA UNA TRAMPA

`PRESUPUESTO_USD = 0.10` allá. La corrida de ayer costó **$0.1407**. Copiado tal
cual **habría cortado a mitad de la tercera pregunta**, y se habrían perdido
horas buscando un defecto en el bucle que no existe.
→ **Un límite heredado sin recalcular no es un freno: es una trampa.**
Quedó en `0.40`, y la corrida real gastó $0.1496 (37% del tope).

### ⏱️ Y UN COSTO QUE NO ESTÁ EN TOKENS

Las llamadas a la API sumaron **20,7 s**. La corrida duró **59 s**. Los otros
**38 segundos fue él decidiendo permisos** — la primera decisión le tomó 26.
No aparece en ningún `usage`, y es el argumento más fuerte a favor de la tecla
`t`: tres permisos idénticos de 26 segundos es cuando el usuario deja de leer y
dice que sí por reflejo.

---

## ⭐ LO QUE PASÓ CON EL FORMATO, Y ES LA NOTICIA DE LA SESIÓN

**SE CORTÓ LA RACHA DE 7 PIEZAS DICTADAS — pero no escribiendo código.**

Él dijo: *"primero explícame sin código alguno en qué consiste el paso 8,
después me dices cuáles son las decisiones abiertas y yo te respondo"*.
**Y respondió las cuatro.** El código lo escribí yo, pero **el diseño es suyo**:
error del modelo como tercera categoría, negar no corta el bucle, permiso por
herramienta, y las tres opciones s/t/n fueron **idea suya**, no del nivel 4.

⚠️ **Y a mitad de sesión frenó otra vez, como en la 13:** *"revisa el README de
04-harness-real, creo que en ese archivo se describen"*. **Tenía razón y yo
estaba equivocado** — yo había dicho que el "6" era una promesa sin lista.
→ **Tercera vez que una intervención suya corrige el rumbo** (las anteriores:
`trm(dias=1)` y *"no es una decisión fácil, podemos analizarlo mejor"*).

⚠️ **Preferencia de formato, confirmada por cuarta sesión:** prosa, sin
selectores de opciones. Y una nueva: **pide el concepto sin código primero.**
Cuando se le explicó el paso 8 con la analogía del mesero y sin una línea de
Python, respondió las cuatro decisiones seguidas.

---

## 💬 SU PREGUNTA DE CIERRE: MULTI-AGENTE (nivel 8, contestada corta)

*"1. ¿Cada agente es un archivo .py? 2. ¿El orquestador sería un bucle externo
y cada agente un bucle interior?"*

Se le contestó corto y se le devolvió al paso 9, pero **la pregunta 2 estaba a
una pieza de la respuesta correcta y la pieza la acababa de construir él**:

> **El agente hijo es una HERRAMIENTA del orquestador.** En su `FUNCIONES`,
> `"trm"` apunta a una función que por dentro tiene `urllib`. En el nivel 8,
> `"investigador"` apunta a una función que por dentro tiene **otro
> `ejecutar_agente()`**. El orquestador no sabe que llamó a un agente: recibe un
> `tool_result` como cualquier otro. **Su puente ya es el mecanismo completo.**

Y a la 1: **un agente no es un archivo.** Son tres cosas —system prompt, menú y
bucle—; tres agentes pueden vivir en un archivo compartiendo `ejecutar_agente()`.

⭐ **Esto cierra su pregunta de la sesión 14** (*"¿puede usar un modelo diferente
según la herramienta?"*), que tal como la hizo no existía. Así sí: el hijo corre
su bucle con `haiku-4-5` y el orquestador con `opus-5`.

**Y el motivo real son sus propios números:** cada agente tiene **su propio
`historial`**, y el del hijo se muere cuando la función retorna. Con 27:1 de
entrada contra salida, los sub-agentes existen sobre todo **para que el bucle de
arriba no repague el trabajo sucio del de abajo**.

→ **Anotado para el nivel 8. No adelantar más.**

---

## Cierre de la sesión 15

**Lo que se hizo:** paso 8 completo — los 9 frenos, escritos y **corridos**.
Dos deudas viejas cerradas (`trm()` ya no manda `T00:00:00.000`; la aritmética
a escondidas, cerrada con un puente). Un defecto nuevo encontrado **por el
registro en su primera corrida** y arreglado con el `motivo`. README del nivel
corregido: la fila del paso 8 ya dice **cuáles** son los frenos.

⭐ **LA LECCIÓN DE MÉTODO, tercera sesión seguida y cada vez más clara:**
hoy **tres cosas salieron de correr o de medir, ninguna de razonar**:

| Hallazgo | De dónde salió |
|---|---|
| Prohibir la división era un callejón | de **escribirlo** y ver que no había salida |
| El registro miente sobre `convertir` | de **leer el `.jsonl`**, no la pantalla |
| El presupuesto del nivel 4 no alcanzaba | de **multiplicar**, no de suponer |

**Las candidatas a lección fuerte del 5b suben a VEINTE.** Las dieciséis
anteriores, más:
17. **Prohibir sin ofrecer salida no es una regla, es un callejón.** Cuando el
    modelo hace algo indebido, primero pregúntate si le falta un puente.
18. **Un límite heredado sin recalcular no es un freno: es una trampa**
    ($0.10 del nivel 4 contra $0.1407 reales).
19. **Un registro que no distingue POR QUÉ pasó algo puede afirmar lo falso.**
    El `motivo` de `trm_en_fecha`, aplicado a los permisos.
20. **Más herramientas no es solo más capacidad: es más formas de
    equivocarse.** Los frenos 7, 8 y 9 no existían en el nivel 4 porque allá
    había una sola herramienta.

⚠️ **`LESSONS.md` sigue sin tocarse, y es correcto** (un bloque por nivel, al
cerrar el nivel). **Al cerrar el 5b hay que escribir las veinte.**

### 📌 DEUDAS ABIERTAS AL CERRAR LA SESIÓN 15

1. **El freno del tamaño del `tool_result`** — se habló y no se hizo. Hoy el
   harness mete en el `tool_result` lo que sea que devuelva una herramienta,
   sin mirarlo. La inyección de la sesión 13 (1 → 1000 filas ≈ 31.000 tokens)
   está cerrada **dentro de `trm_en_fecha`**, no en el harness: una séptima
   herramienta sin ese freno vuelve a abrir la puerta.
2. **`trm_en_fecha` no tiene `usd_por_1_cop`** — mismo hueco del puente, se
   dejó a propósito (cada llave se repaga en cada vuelta). Si algún día hay que
   convertir montos de una fecha pasada, se agrega.
3. **Los caminos 7 y 8 no se han visto atrapar nada.** El modelo no inventó
   nombres en la corrida. La forma barata de forzarlo es el sabotaje de
   siempre: cambiarle el `name` a una herramienta en `TOOLS` sin tocar
   `FUNCIONES`. **Una red que nunca viste atrapar nada no es una red: es un
   comentario.**
4. **`evals.py` no prueba nada del harness.** Los 116 casos son de
   `herramientas.py`. `pedir_permiso` y los tres `except` no tienen un solo
   caso — y se pueden probar gratis, sin red y sin modelo.

### 📂 ARCHIVOS TOCADOS EN LA SESIÓN 15 (para no buscarlos la próxima vez)

| Archivo | Qué cambió |
|---|---|
| `05b-proyecto/agente.py` | los 9 frenos · `PERMISOS` · `anotar()` · `llamar_modelo()` · `pedir_permiso()` con motivo · descripciones de `convertir` y `trm` |
| `05b-proyecto/herramientas.py` | `trm()`: fechas a 10 caracteres + `usd_por_1_cop` |
| `05b-proyecto/README.md` | plan: paso 7 ✅, paso 8 = **9 frenos** ✅, con la lista · fila nueva en la tabla de piezas |
| `05b-proyecto/registro.jsonl` | **nuevo.** 23 líneas de la corrida real. **NO borrarlo:** la línea 13 es la evidencia del defecto del permiso |
| `GUIDE.md` | §4.c pasó de 6 a **9 frenos** · presupuesto que no se hereda · permisos s/t/n con motivo · frenos 7-8-9 nuevos |
| `PROGRESO.md` | esto |

---

## Histórico: sesión 14 — **PASO 7**: `agente.py` CORRE. Claude ya usa sus 6 herramientas

**El agente existe y funciona.** Primera corrida pagada del nivel: 3 preguntas,
**7 vueltas, las 3 respuestas correctas**. Las 6 herramientas dejaron de ser
código que solo él podía llamar.

✅ **Las tres deudas que dejó esta sesión se cerraron en la 15.** Lo que sigue es
el histórico de cómo se veían entonces.

### 📋 ESTADO VERIFICADO AL CERRAR LA SESIÓN 14

Comprobado corriéndolo, no de memoria:

| | |
|---|---|
| `herramientas.py` | 41.374 bytes · **6 herramientas** + **5 ayudantes** · sin tocar hoy |
| `evals.py` | 44.412 bytes · **116 casos, 0 fallaron**, $0.00, sin red · sin tocar hoy |
| `agente.py` | **escrito y corrido** · `TOOLS` (6) + `FUNCIONES` (6) + `ejecutar_agente()` |
| menú vs puente | **coinciden: los 6 `name` = las 6 llaves de `FUNCIONES`** (comprobado) |

### 🚨 LAS 3 DEUDAS DEL PASO 8 (las tres ya están escritas en `agente.py`)

1. **`FUNCIONES[bloque.name]` y `funcion(**bloque.input)` confían en el modelo.**
   Nombre inventado → `KeyError`. Argumento que no existe (`trm(dias=1)`, el que
   corrigió él) → `TypeError`. **Y reventar ahí tumba el bucle entero** — justo
   lo que costó tanto trabajo evitar DENTRO de cada función. El `try` del
   harness le dice al modelo "falló por un defecto interno" y a nosotros nos
   imprime el traceback. Misma forma que el permiso del nivel 4.
2. **⭐ EL MODELO HACE ARITMÉTICA A MANO** (hallazgo de la primera corrida, abajo).
3. **Los permisos por herramienta** — pregunta suya de hoy, ver más abajo.

**Deuda chica que sigue sin decidirse (van 2 sesiones):** `trm()` devuelve las
fechas con `T00:00:00.000`; `historial` y `trm_en_fecha` las recortan a 10.
**Hoy se vio en la corrida real** (`'vigente_desde': '2026-07-30T00:00:00.000'`):
son 56 caracteres de relleno por llamada a `trm`. Una línea, pero es cambio de
comportamiento: se decide, no se hace de paso.

---

## 🚨 EL HALLAZGO DE LA SESIÓN: EL MODELO DIVIDE A ESCONDIDAS

De la pregunta *"¿cuántos dólares son 500 mil pesos colombianos?"*:

```
trm() devolvió       ->  3206.18        (COP por 1 USD)
convertir() recibió  ->  0.00031189777  (USD por 1 COP)
```

**Ese número no salió de ninguna herramienta.** El modelo calculó `1/3206.18`
en su cabeza.

**El hueco de diseño, y es real:** `convertir()` se escribió justamente para que
el modelo NO hiciera aritmética. Pero `trm` entrega la tasa en un sentido y la
pregunta iba en el otro. **Nadie construyó ese puente, así que lo construyó él
— calculando.**

Verificado: se desvió en la **10ª cifra decimal** (`1.2e-10`) y el resultado
salió idéntico. **Y eso es lo peligroso, no el consuelo:** el día que se desvíe
en la 4ª, `convertir()` recibe una tasa perfectamente válida y **ni los 116
casos se enteran**. Es el número creíble en su forma más difícil de ver.

⭐ **La pista que lo delata está en el `usage`:** esa vuelta gastó
**`salida=335`** tokens contra ~60 de las otras. **El costo delata el cálculo.**

→ **Decisión del paso 8, sin tomar:** o `convertir()` voltea la tasa ella misma,
o la descripción le prohíbe invertirla a mano. Las dos tienen costo.

---

## ✅ PASO 7.1 — EL MENÚ (`TOOLS`), Y LO QUE ENSEÑÓ ESCRIBIRLO

⚠️ **DICTADO.** Se le dieron `convertir` y `trm` como ejemplos y se le propuso
escribir las otras cuatro; pidió el archivo completo. **Séptima pieza seguida.**
Se le dijo **una sola vez** y él acotó el encargo por su cuenta —
*"no quiero que escribas el archivo completo, solo la presentación de las
herramientas"*—, y **ya había pegado a mano las dos del ejemplo en el archivo.**
Es menos que escribirlo, pero es más que las 6 anteriores. **Anotarlo como
movimiento en la dirección correcta.**

**El patrón que salió al escribirlas, y es la lección del paso:**

> **Casi toda una buena descripción no dice QUÉ hace la herramienta: dice
> CUÁNDO NO usarla y CON CUÁL NO CONFUNDIRLA.** Decir qué hace es lo fácil.
> Las fronteras son las que evitan el error — y un error de elección cuesta una
> vuelta entera, o sea >3.000 tokens.

Las tres fronteras que se marcaron a propósito:
- **`trm` vs `trm_en_fecha`** — las dos descripciones se nombran mutuamente.
  A `trm_en_fecha` se le PROHÍBE explícitamente usarse para hoy o ayer: *"tú no
  sabes qué día es hoy, pondrías una fecha imaginada y devolverías un número
  real del día equivocado"*.
- **`trm` vs `tasa`** — con los dos números del 2026-07-30 metidos en el texto
  (3206,18 y 3207,64) para que no parezcan intercambiables.
- **`historial` vs `trm_en_fecha`** — tendencia contra día puntual.

---

## ✅ LAS 3 COSAS QUE FUNCIONARON, MEDIDAS EN LA CORRIDA REAL

### ⭐ 1. La advertencia de `historial` FUNCIONÓ. Es la mejor noticia del día

El modelo contestó: *"entre el 1 y el 30 de julio... (20 registros de vigencia)"*.

**NO dijo "en los últimos 20 días".** Usó `desde` y `hasta`, exactamente como se
lo ordenó la descripción.

→ **El defecto que él descubrió midiendo en la sesión 13 —30 registros son 48
días— no llegó a la respuesta del usuario. Y se cerró CON TEXTO, sin una sola
línea de código.** Es la prueba de que la lista `tools` no es documentación:
es comportamiento.

### 2. La cadena de 3 vueltas ocurrió, como estaba previsto

`trm` → `convertir` → responder. **El modelo no se inventó la tasa**: pidió el
número real primero. La frontera de `convertir` (*"esta herramienta NO busca la
tasa"*) hizo su trabajo.

### 3. El modelo admitió que no tiene reloj

*"si hoy ya es un día posterior, la TRM vigente podría ser otra"*.
Honestidad forzada por la descripción — **y la prueba de que la deuda de
`hora_utc` es real**: tiene que andar con esa muletilla porque no sabe qué día es.

---

## 📏 MEDICIÓN — Y ME EQUIVOQUÉ DOS VECES SEGUIDAS, EN EL MISMO SENTIDO

| Método | Resultado |
|---|---|
| A ojo, en el comentario | "~700-900 tokens" |
| Caracteres / 4 | 6.231 / 4 = **~1.557** |
| **`count_tokens(tools=TOOLS)`** | **3.049 exactos, y GRATIS** |

Los dos estimados cortos, **y en el mismo sentido**. La regla de "4 caracteres
por token" viene del inglés en prosa; **JSON en español tokeniza mucho peor**.

⚠️⚠️ **Y lo incómodo: `GUIDE.md` §5.b YA documentaba `count_tokens` desde el
nivel 5.** La herramienta que me habría evitado equivocarme dos veces estaba
escrita en su propia guía y no la usé — estimé. Lo que faltaba en la guía era
**decir que acepta `tools=`**, que es justo lo caro. Ya está corregido.
→ **Tener la herramienta documentada no es lo mismo que acordarse de usarla.**

**Aislar el costo del menú son tres llamadas gratis y una resta:**

```
solo el mensaje  :     8
+ system         :   171   -> el system cuesta   163
+ system + tools : 3.220   -> EL MENÚ CUESTA   3.049
```

→ **REGLA NUEVA: el único contador que vale es el de la API. Y es gratis, así
que no hay excusa para estimar.**

**Y la proporción de la corrida completa dice lo que hay que entender de un
agente:**

```
7 vueltas · entrada 23.710 tokens · salida 887 tokens
```

> **La entrada es 27 veces la salida. Un agente no paga por lo que dice: paga
> por lo que RELEE en cada vuelta.**

Y pone en perspectiva media sesión 13: el resumen de `historial` ahorra **143
tokens por vuelta**; el menú cuesta **~2.900**. **Veinte veces más que la
decisión que costó media sesión analizar.** No invalida aquel análisis (el
método sigue siendo el bueno) — pero dice **dónde está el dinero de verdad**.

---

## 💬 SUS DOS PREGUNTAS DE HOY (las dos buenas, las dos anotadas)

### 1. *"¿deberíamos poder configurar los permisos que le asignamos?"*

**Sí, y es del paso 8.** Es su propia decisión del nivel 4 (el permiso de
`borrar_archivo()` va en el harness, no dentro de la función) aplicada a seis
herramientas en vez de una.

Lo que se le mostró, y es la parte que enseña — **no son dos categorías, son tres:**

| Herramientas | Qué tocan | |
|---|---|---|
| `convertir` | nada | libre |
| `tasa`, `trm`, `historial`, `trm_en_fecha` | leen un servidor **ajeno** | cuesta, no rompe |
| **`guardar_reporte`** | **escribe en el disco** | **deja huella** |

> **La pregunta no es "¿lee o escribe?", es: si esto sale mal, ¿lo puedo
> deshacer?**

⭐ **Y el detalle que lo conecta con lo que él ya mide:** el permiso **no le
cuesta un solo token al modelo** — la tabla vive en Python y el modelo nunca la
ve. Explicárselo en la descripción sí se pagaría en cada vuelta.
→ **Lo que puede vivir en el harness, que viva en el harness: es gratis ahí e
impuesto permanente allá.**

### 2. *"¿puede usar un modelo diferente según la herramienta?"*

**Hubo que corregirle una pieza, y es de las que se quedan mal puestas:**

> **El modelo no ejecuta la herramienta. La ejecuta el harness.** Dentro de sus
> seis funciones no hay ningún modelo: hay `urllib` y unos `if`. **Por eso
> `evals.py` corre 116 casos por $0.00.**

Tal como la preguntó, no existe. Pero su intuición apunta a tres cosas reales
que sí existen y son de más adelante: un modelo distinto para el bucle (eso sí,
es una línea), una herramienta que por dentro llama a otro modelo, y el
enrutamiento (modelo barato decide, caro ejecuta).

→ **Lo que sí le toca ya: escoger el modelo del bucle.** Y hay un experimento
honesto para el paso 9: correr lo mismo con `claude-opus-5` y con
`claude-haiku-4-5` y ver **si el barato escoge bien entre seis herramientas**.
El riesgo de un menú largo no es el precio: es que se equivoque al escoger.

---

## Cierre de la sesión 14

**Lo que se hizo:** paso 7 completo. `agente.py` pasó de **0 bytes** a un agente
que corre: menú de 6, puente de 6, bucle con `usage` por vuelta. Primera corrida
pagada del nivel — **7 vueltas, 3 respuestas correctas**. Tres deudas del paso 8
anotadas DENTRO del código, en el sitio donde se leerán solas.

⭐ **LA LECCIÓN DE MÉTODO DE LA SESIÓN, y es la misma de la 13 con otra ropa:**
hoy se encontraron **tres cosas, y ninguna salió de razonar**:

| Hallazgo | De dónde salió |
|---|---|
| El modelo divide a escondidas | de **correrlo** |
| El menú pesa el doble de lo estimado | del **`usage`** |
| Su advertencia de "registros, no días" funciona | de **leer la respuesta** |

→ **Las tres las habría jurado de otra forma.** Es *"verificar también lo que
uno acaba de escribir con toda seguridad"*, segunda sesión seguida.

**Las candidatas a lección fuerte del 5b suben a DIECISÉIS.** Las trece
anteriores, más:
14. **Una buena descripción de herramienta dice sobre todo CUÁNDO NO usarla y
    con cuál no confundirla.** Y el menú es comportamiento, no documentación:
    el defecto del `dias` se cerró con texto, sin código.
15. **El modelo hace aritmética a escondidas cuando falta un puente entre dos
    herramientas** — y el `usage` de salida lo delata.
16. **El único contador de tokens que vale es el `usage` de la API.** Dos
    estimados seguidos, los dos cortos, en el mismo sentido.
    Y: **un agente paga por lo que RELEE, no por lo que dice** (27:1).

⚠️ **`LESSONS.md` sigue sin tocarse, y es correcto** (un bloque por nivel, al
cerrar el nivel). **Al cerrar el 5b hay que escribir las dieciséis.**

⚠️ **DEUDA DE FORMATO — VAN 7 PIEZAS SEGUIDAS DICTADAS**, pero **hoy se movió**:
acotó el encargo por su cuenta ("solo la presentación de las herramientas, no el
archivo completo"), **pegó a mano en el archivo las dos descripciones de
ejemplo**, y **pidió ver el bucle en pantalla antes de escribirlo**
(*"pero primero lo muestras para entenderlo"*). Eso último es nuevo y es bueno:
es querer entender antes que tener. Se le dijo una vez y no se repitió.

**Dónde cortar la racha, y el paso 8 es mejor sitio que el 7:** las tres deudas
son **decisiones**, no transcripción — y decidir es justo lo que él hace bien
(lleva dos diseños míos corregidos). Empezar preguntándole **qué debería pasar**
cuando el modelo pide una herramienta que no existe, antes de escribir el `try`.

⚠️ **Preferencia de formato, confirmada otra vez:** se le habló en prosa toda la
sesión, sin un solo selector de opciones, y respondió largo y con criterio.

---

## Histórico: sesión 13 (pasos 6 y 6b — las 6 herramientas terminadas)

Al cerrar la sesión 13: `herramientas.py` 41.374 bytes con las 6 herramientas y
5 ayudantes; `evals.py` 44.412 bytes con **116 casos, 0 fallos**, $0.00 y sin
red; `agente.py` en 0 bytes.

---

## ⭐ LA IDEA DE LA SESIÓN ES SUYA, Y ES MEJOR QUE LAS TRES MÍAS

Contexto: se decidió que `historial` devuelve un **resumen**, no las filas. Eso
abre un hueco — si el usuario pregunta *"¿cuánto valió el 15 de julio?"*, el
modelo no lo sabe **y no tiene cómo averiguarlo**, así que o se rinde o se lo
inventa (y con máximo, mínimo y promedio en la mano, puede inventar algo muy
creíble). Se le ofrecieron 3 salidas, las tres **metiendo el día puntual DENTRO
de `historial`**: respuesta de tamaño variable, un parámetro `detalle`, o
confiar en que el modelo lea la descripción.

**Él propuso una cuarta: una herramienta aparte que lea UNA fecha del pasado.**

Y es la aplicación de **su propia regla**, la que salió al corregir mi
`trm(dias=1)` en la sesión 12: *dos herramientas que se pisan obligan al modelo a
elegir entre dos caminos para lo mismo; una cosa cada una.* Mis tres opciones
parchaban `historial`; él aplicó la regla que ya estaba establecida.
→ **Vale la pena decírselo: es la segunda vez que corrige un diseño mío** (la
primera fue `trm(dias=1)`), y esta vez sin que se le pidiera.

**Las 5 pruebas contra la fuente ya están corridas (2026-07-30), no hay que
volverlas a hacer.** La fuente acepta `$where` con rango de fechas:

```
$where=vigenciadesde <= 'FECHA' AND vigenciahasta >= 'FECHA'   (espacios como %20)
```

| Fecha pedida | Resultado |
|---|---|
| 2026-07-30 (jueves) | 1 fila ✅ |
| **2026-07-26 (DOMINGO)** | **1 fila: la vigente 25→27, `3210.56`** ✅ |
| 2024-03-05 (hace 2 años) | 1 fila, `3948.67` ✅ |
| 2027-01-01 (futuro) | **0 filas**, sin error |
| 1990-01-01 | **0 filas**, sin error |

⭐ **El domingo se resuelve solo.** No hay que calcular nada de calendario: se
pregunta por rango y **la fuente sabe qué fila cubre qué días**. Es la misma
idea que ya estaba en `trm()`, pero ahora usada para *buscar*, no solo para
informar.

**Los 3 problemas nuevos que traerá (material del paso):**
1. **La fecha la escribe el modelo:** va a mandar `"15 de julio"`, `"15/07/2026"`,
   `"2026-7-5"`. Freno de formato, clase que él no ha hecho.
2. **0 filas NO es error de red.** Y el mensaje tiene que decir *por qué*:
   ¿futura? ¿anterior al dataset? Son cosas distintas para el modelo.
3. **Una URL armada con texto que viene de afuera.** Hasta hoy todas sus URLs
   eran constantes. Esto tiene nombre propio en seguridad.

⚠️ **Y algo que su idea deja claro sin querer: `trm()` NO queda redundante.** No
se puede reemplazar por `trm_en_fecha("hoy")` porque **el modelo no sabe qué día
es** — no tiene reloj, pondría la fecha que se imagine, y volvemos al número
creíble. Es la misma razón por la que `trm()` no mira el reloj.

---

## ✅ `trm_en_fecha(fecha)` — LA 6ª HERRAMIENTA, IDEA SUYA. 27 casos + corrida real

⚠️ **DICTADA.** Se le dio el esqueleto con 6 huecos y un ejemplo desechable
(`validar_hora`, con `"25:99"` como el caso que justifica `strptime`), y pidió
*"escribe la herramienta completa y después me la explicas"*. **Sexta seguida.**
Se le había dicho una vez en esta misma sesión; no se repitió (repetir es
regañar). Ver la deuda de formato al final.

**Decisión suya:** *"que distinga el porqué, para que el modelo pueda
explicar"*. Cero filas tapa tres situaciones distintas y ahora se separan.

### 🚨 LO MÁS IMPORTANTE DEL DÍA: LA INYECCIÓN, DEMOSTRADA EN VIVO

Primera URL del proyecto que se arma con **texto de afuera** (todas las demás
eran constantes). La consulta pone el dato entre comillas simples:

```
$where=vigenciadesde <= 'LA_FECHA' AND ...
```

Se probó contra **la fuente real** con `2026-07-30' OR '1'='1`:

```
filas devueltas: 1000
```

La comilla **cerró** la que abría el dato, y lo que seguía dejó de ser dato:
se volvió **parte de la pregunta**. Pedimos un día y trajo el dataset entero
(1000 = el tope del servidor).

**Y el daño es DOBLE, y el segundo casi nadie lo ve:**
| | |
|---|---|
| Respuesta equivocada | el agente reporta cualquier cosa |
| **Bomba de tokens** | 1000 filas ≈ **125.000 caracteres ≈ 31.000 tokens**, repagados en CADA vuelta |

→ Un `tool_result` de 175 caracteres se vuelve uno de 125.000. Por una comilla.
→ **La defensa es su LISTA DE PERMITIDOS de `guardar_reporte`**, no una lista de
prohibidos: no se pregunta "¿tiene comillas?" (siempre falta un carácter), se
exige la forma exacta `AAAA-MM-DD`. **Lo que no se nos ocurrió también queda
afuera.** Y no hubo que escribir una sola línea pensando en comillas.

⚠️ **Distinción que hay que conservar: `quote()` NO es el freno.** Codifica para
transportar; codificar una comilla no la rechaza, la transporta intacta.
**El freno decide QUÉ entra; `quote()` solo lo lleva sin romperse.** Confiar en
`quote()` para la seguridad es confiar en el bus para decidir quién viaja.

### 🐛 DEFECTO REAL ENCONTRADO POR LA PRIMERA CORRIDA (no por razonar)

`strptime` con `%Y-%m-%d` **NO exige el cero a la izquierda**: `"2026-7-5"` le
encaja igual que `"2026-07-05"`. Yo escribí ese freno convencido de lo
contrario. **Lo dijo la corrida, no el análisis.**

Y el defecto no era cosmético: se **validaba una cosa y se mandaba otra** (a la
URL iba el texto original). Eso rompe la comparación de fechas como texto:

```
"2026-7-5" > "2026-07-30"   ->   True   (en el 6º carácter, "7" > "0")
```

El agente diría **"todavía no hay TRM para esa fecha"** de un día que ya pasó,
con toda seguridad. → Arreglado con `fecha = dia.strftime(FORMATO_FECHA)`.
→ **REGLA NUEVA: después de validar, usa lo VALIDADO, no lo que llegó.**

### ⭐ EL TRUCO DEL CALENDARIO: no le preguntes al reloj, pregúntale a la fuente

Para decir "esa fecha es futura" hacía falta saber qué día es hoy — y una
función que mira el reloj **deja de poderse probar con datos fijos** (la razón
por la que `trm()` no calcula "¿es de hoy?"). La salida: `URL_TRM_RANGO`, una
consulta con `$select=min(vigenciadesde),max(vigenciahasta)`.

**Verificado: la fuente cubre del `1991-12-02` al `2026-07-30`.**

→ **La fuente es su propio calendario.** Determinista, probable, sin reloj. Y la
segunda llamada solo ocurre **en el camino del fallo**, que es raro.

**Los 4 motivos** (`futura`, `muy_antigua`, `hueco`, `desconocido`). El último
importa: **si la consulta del rango también falla, NO se inventa el motivo.**
Un motivo inventado es peor que ninguno — familia del número creíble.

### 🎨 Y EL EVAL MEJORÓ EL DISEÑO: el `motivo` como DATO

Al escribir los casos apareció el choque: **¿cómo pruebo que los tres motivos
son distintos, si su propia regla del paso 5 prohíbe comparar el texto de un
error?** Salida: que el motivo sea un **dato estable** (`"futura"`,
`"muy_antigua"`, `"hueco"`, `"desconocido"`) al lado de la frase, que se puede
reescribir cuando se quiera.
→ **La prueba no solo verificó el código: lo mejoró.** El modelo también gana:
ramifica por un valor fijo y no por cómo esté redactada una frase.

### 🎭 PIEZA NUEVA EN `evals.py`: el doble de DOS RESPUESTAS

Primera herramienta que hace **dos consultas distintas** (el dato y el rango).
Un doble que conteste siempre lo mismo no sirve: para probar "es futura" hace
falta que la primera devuelva vacío **y** la segunda devuelva el rango.
`servidor_dos_respuestas()` mira si la URL trae `$select` y escoge.
→ **El actor ahora tiene dos parlamentos y escoge según la pregunta.**

### LOS 4 SABOTAJES — 3 predicciones exactas y ⚠️ UNA FALLADA (mía)

| | Predicho | Real |
|---|---|---|
| **A** quitar la normalización | 1 | ✅ 1 |
| **B** quitar el freno `strptime` | 7 | ⚠️ **13** |
| **C** juntar `fecha_pedida` con `vigente_desde` | 1 | ✅ 1 |
| **D** `>` por `>=` en "es futura" | 1 | ✅ 1 |

⚠️ **La predicción B falló y se deja escrita con la razón**, como la del paso 5.
Dos causas, y son distintas: (1) conté 7 y eran **8** — se me pasó
`fecha vacia`; (2) los otros **5 fueron efecto secundario de CÓMO saboteé**:
reemplacé `strptime` por una fecha fija, y como la normalización usa lo que él
devuelve, **todas las fechas se volvieron `2026-07-30`**.
→ Lo que sí enseña, y no estaba previsto: **romper un freno no rompe solo el
freno.** El resto de la función depende de lo que produce. Está encadenado.

**Lo que B sí demostró, que era el objetivo:** las dos inyecciones salieron con
`REVENTO: AssertionError`, o sea **llegaron a la red**. Con el freno puesto
mueren limpias y **la consulta ni se arma**.

⭐ **EL SABOTAJE C ES EL MÁS INSTRUCTIVO: falló SOLO el caso `domingo`.**
`feliz` y `fecha sin ceros` pasaron tranquilos, porque en un día normal la fecha
pedida y la vigencia **son la misma** y el defecto es invisible.
→ **Misma forma que el `feliz con filas al reves` de `historial`: el caso raro
no era adorno, era el único con ojos.** Un eval hecho solo de días normales
habría dado verde con el agente diciendo "el 26 la TRM fue X" de un día en que
no se publicó nada.

**El sabotaje D** también se ganó el sueldo: un carácter (`>` → `>=`) y el
agente diría "todavía no hay TRM para hoy" del día que sí la tiene.

### La corrida real (2026-07-30) — lo que el doble no puede dar

```
2026-07-30 (jueves)  -> 3206.18   vigente 2026-07-30 a 2026-07-30
2026-07-26 (DOMINGO) -> 3210.56   vigente 2026-07-25 a 2026-07-27  ⭐
2024-03-05 (2 anios) -> 3948.67
2027-01-01 (futura)  -> "el dato más reciente que publica la fuente es del 2026-07-30"
1990-01-01           -> "la serie oficial empieza el 1991-12-02"
```

**175 caracteres, ~43 tokens: la más barata de las seis herramientas.**

⚠️ **Inconsistencia menor anotada, sin resolver:** `trm_en_fecha` e `historial`
recortan las fechas a 10 caracteres; **`trm()` todavía devuelve el
`T00:00:00.000` completo** (28 caracteres de relleno). Arreglarlo es una línea
y no rompe ningún caso — pero es cambio de comportamiento, así que se anota y
se decide, no se hace de paso.

---

## 🧠 CÓMO SE DECIDIÓ EL RECORTE — el método vale más que la decisión

⚠️ **Él frenó la decisión:** se le presentaron 3 opciones y contestó
*"amigo no es una decisión fácil, podemos analizarlo mejor"*. **Tenía razón y
hay que anotarlo**: la iba a tomar a ojo. De ahí salió todo lo bueno del día.

**Se midió con los 30 días reales**, no con estimados:

| Opción | Caracteres | Tokens | vs. crudo |
|---|---|---|---|
| Crudo, sin recortar | 3.808 | ~952 | — |
| **A resumen** | **238** | ~59 | **16x** |
| B filas recortadas | 811 | ~202 | 4,7x |
| C resumen + filas | 997 | ~249 | 3,8x |

**Lo primero que salió al medir: botar el ruido no está en discusión.**
`"unidad":"COP"` repetido 30 veces y `T00:00:00.000` repetido 60 no lo necesita
nadie. La pregunta de verdad era solo **A contra B: 143 tokens por vuelta.**

**Y ahí el número solo no alcanzaba.** Se puso al lado de otro: **una vuelta
extra del bucle** (repagar SYSTEM + menú de 5 herramientas + historial) cuesta
**más de 1.000 tokens**. O sea que ahorrar 143 puede salir carísimo si obliga a
una segunda llamada.

**La pregunta se le devolvió convertida en una sobre SU agente:** *"¿qué vas a
preguntar más: cómo va el dólar, o cuánto valió tal día?"*. Contestó **"cómo va
el dólar"** → gana A.

⭐ **Y lo que hay que conservar del método es el punto de equilibrio:**

```
236 + (p × 1.000) = 808   →   p = 0,57
```

> **A gana mientras necesite el día puntual menos del 57% de las veces.**

No se decidió con un pálpito ni con un "creo que casi siempre": se decidió con un
número que dice **cuánto puede estar equivocado y seguir teniendo razón**. Aunque
se haya quedado corto y sea 40%, A sigue ganando. **La decisión es robusta, y eso
es un resultado distinto de "la decisión es correcta".**

### 🆕 EL CONCEPTO NUEVO: el menú también se paga

Al evaluar su idea salió algo que no se había tocado en todo el curso:

| Qué | Cuándo se paga |
|---|---|
| Un `tool_result` gordo | desde la vuelta en que se llamó, en adelante |
| **Una herramienta en la lista `tools`** | **desde la vuelta 1 de TODAS las conversaciones, aunque nunca se llame** |

Una herramienta bien descrita son ~100–150 tokens **por vuelta, siempre**.
→ **Un `tool_result` es un impuesto permanente; una herramienta de más es un
impuesto permanente que se paga aunque nunca la uses.** Y peor que los tokens:
**un menú largo hace que el modelo se equivoque más al escoger** (medible en el
paso 9).

⚠️ **Se le dijo el resultado incómodo sin maquillarlo: en puros tokens su idea
NO gana.** A + 6ª herramienta ≈ 960 tokens en una conversación de 6 vueltas;
B sola ≈ 810. **Gana en otra cosa:** B no puede contestar por el 3 de marzo de
2024 **nunca**, pida lo que pida. → **Comparar herramientas solo por lo que
cuestan es como escoger empleado por lo que cobra: primero se pregunta si hace
el trabajo.**

---

## 🚨 EL DEFECTO QUE SOLO APARECIÓ POR MEDIR: `dias` MIENTE

Al traer los 30 días de verdad, el resumen salió con `desde: 2026-06-12`.
**30 filas = 48 días de calendario.** Y `historial(5)` dio 7 días.

La fuente **no guarda un registro por día: guarda uno por VIGENCIA.** La TRM del
viernes vale también sábado y domingo, así que un fin de semana entero es UNA
fila. 7 fines de semana + festivos ≈ los 18 días que faltaban.

Si el parámetro se llama `dias`, el modelo diría *"en los últimos 30 días el
dólar bajó 8,75%"* y **sería falso**: fueron 48. El número está bien; **la frase
que lo acompaña miente**. Es su lección de la sesión 11 (el *"solo letras y
números"* que prometía lo que no cumplía) aplicada a un nombre de parámetro.

**Cómo quedó (decisión mía, revocable, y se le dijo):** el parámetro se sigue
llamando `dias` —el modelo y el usuario piensan en días; con `filas` el modelo
tendría que *adivinar* cuántas filas son un mes, y adivinar es lo que no
queremos— pero el dict devuelve `registros`, `desde` y `hasta`, así que **la
función nunca afirma "los últimos 30 días"**. La alternativa (recortar de verdad
a N días de calendario) se puede y **queda anotada como deuda**: pide aritmética
de fechas, un tema nuevo a mitad de otro. README del nivel corregido.

→ **Esto no se sabía 10 minutos antes. Salió de medir en vez de suponer.**

---

## ✅ `historial(dias)` — escrita, 27 casos, corrida real, 248 caracteres

⚠️ **DICTADA.** Se le dio primero el esqueleto con **6 huecos numerados** en el
archivo y se le pidió empezar por el 1; contestó *"escribe los 6 huecos por favor
y la herramienta completa y después me la explicas"*. **Quinta pieza seguida
dictada.** Se le dijo una vez, sin insistir, y se le propuso el trato de que
`trm_en_fecha` sea suya.

**Lo nuevo que trajo esta función, y ninguna anterior tenía:**

1. **Un tope que protege a un TERCERO.** `MAX_REGISTROS = 400`. Y el comentario
   dice lo importante: **este tope no protege nuestros tokens** (el resumen pesa
   igual con 30 filas que con 400), protege **al servidor del gobierno** y al
   usuario que se queda esperando. `100000` no es basura: es un número
   perfectamente válido con el que el modelo hace un destrozo sin querer.
   → Primer freno del curso que no defiende al propio programa.
2. **`.is_integer()` en vez de `int()`.** `3.5` se rechaza, `30.0` se acepta
   (es un 30 con decimales; rechazarlo sería castigar al modelo por una coma).
   **`int(3.5)` daría 3 en silencio** — haría algo distinto de lo pedido sin
   avisarle a nadie. Es la categoría del número creíble, otra vez.
3. **`continue` en vez de `return`** dentro del bucle: los mismos frenos de
   `trm()`, pero una fila que se cae no tumba a las otras 29.
4. **`serie.sort()` y el regalo del formato ISO.** Se ordena aquí en vez de
   confiar en el `$order` de la URL. Y ordenar es **gratis** porque la fecha es
   `"AAAA-MM-DD"`: el ISO se ordena solo como texto, sin convertirlo a fecha.
   → **Por eso se recortó a 10 caracteres y no a 4 ni a 7: el corte no fue
   estético, se escogió el punto donde la fecha todavía se ordena bien.**
5. **`if not serie: return error`** — un promedio de cero números no existe
   (`sum([])/len([])` es `ZeroDivisionError`).
6. **Los redondeos son de PRESENTACIÓN**, al final y nunca sobre un número que
   se vuelve a usar. Es la trampa de `tasa()` (`0.00031` → `0.0`) ya interiorizada.

**LA DECISIÓN DEL HUECO 4 (mía, revocable): una fila podrida se salta y se
cuenta, no tumba la respuesta.** 29 días buenos siguen contestando "¿cómo va el
dólar?". **Pero el descarte no se esconde:** se devuelve `descartados`, porque
decidir si 29 de 30 sirven **es criterio, o sea del modelo** — la misma regla del
domingo en `trm()`. Callarlo sería el `except Exception` que no se puso en
`pedir_json`: un problema real disfrazado de respuesta normal.

⚠️ **Y la llave `descartados` solo aparece si hubo descartes.** Un
`"descartados": 0` fijo sería ruido que se repaga en cada vuelta.

**Corrida real 2026-07-30:** `historial(30)` → 248 caracteres (~62 tokens),
30 registros del 12-jun al 30-jul, promedio 3334.44, **cambio -8,75%**.
El estimado era 238; el real 248.

---

## 🪤 LOS 27 CASOS, Y UNA PIEZA NUEVA EN `evals.py`

**8 rechazos sin red** (con la trampa puesta: hacen doble trabajo, comprueban el
rechazo **y** demuestran que los frenos están antes de la red) + **19 con
servidor de mentira**.

### La pieza nueva: el `esperado` puede ser un DICCIONARIO

`historial` devuelve muchas cosas y varias vale la pena mirarlas a la vez. Los
casos nuevos comparan **solo las llaves que se nombran**, no el dict entero.
→ **Misma razón por la que nunca se compara el texto de un error:** el día que se
le agregue una llave al resumen, no se tienen que romper 10 casos. La prueba
tiene que dejar mejorar el código.

**Truco:** `r.get(k)` da `None` cuando la llave no está, así que un esperado con
`"descartados": None` **comprueba que la llave NO exista.**

### ⚠️ Y ESO DESTAPÓ UN DEFECTO VIEJO ESCONDIDO UN PISO MÁS ABAJO

```python
{"promedio": 4000.0} == {"promedio": 4000}   # True
```

El `==` de los diccionarios compara los valores con `==`, y **`4.0 == 4` es
True**. O sea: la comparación estricta de tipos que él endureció en el paso 5
**se perdía en cuanto el esperado dejaba de ser un número suelto.** Es su propio
defecto del `4.0 == 4`, reaparecido en otra forma.
→ Se escribió `igual_estricto(a, b)`, que compara tipo **y** valor, y en los
dicts va llave por llave. **Tercera vez que ese hallazgo del paso 5 paga.**

### LOS 3 SABOTAJES — predicción escrita antes de correr, las 3 exactas

Se predijo **2, 9 y 1**. Salió **2, 9 y 1**.

**A — quitar `serie.sort()` → 2 rojos. EL HALLAZGO DEL DÍA:**

```
esperado  'desde':'2026-07-01'  'cambio_pct': 33.33
obtenido  'desde':'2026-07-03'  'cambio_pct': -25.0
```

Sin ordenar, la función dice que el dólar **bajó 25%** cuando **subió 33%**. No
revienta, no avisa: devuelve un número creíble **con el signo al revés**.
→ **Cuarta aparición del patrón hoy** (con `monto=True → 3900`,
`moneda=[] → 39000`, `tasa<0 → -4000.0`), y **el peor de los cuatro**: un −25% en
una serie de dólares no le llama la atención a nadie.

⭐ **Y el detalle que más enseña, también predicho:** el caso
`feliz con filas al reves` **pasó tranquilo** con el sabotaje puesto. Con el
`sort()` roto la función acierta **solo cuando el servidor manda al revés de como
manda hoy**. Con un solo caso feliz —el que copia el orden real— habría habido
verde con la función rota.
→ **Dos casos con los MISMOS datos en distinto orden no son un caso repetido:
son la única forma de ver una dependencia oculta del orden.**

**B — que `descartados` nunca se informe → 9 rojos.** Una línea rota, 9 casos.
Y `registros: 3` estaba **bien** en los nueve: la función devolvía 3 días
correctos **y se callaba que botó uno**. Solo lo cazó la llave del descarte —
igual que el sabotaje del `write_text`, donde las dos primeras columnas
coincidían.

**C — quitar el freno de decimales → 1 rojo, con `REVENTO: AssertionError`.**
`3.5` pasa el freno, `int(3.5)` da 3 en silencio y la función **sale a la red**:
**saltó la trampa**. Segundo trabajo de la trampa confirmado otra vez: no solo
documenta que el eval es gratis, **detecta un freno movido de sitio**.

**Restaurado y verificado: `88 casos, 0 fallaron`.**

---

## Cierre de la sesión 13

**Lo que se hizo:** pasos 6 **y** 6b cerrados. `historial(dias)` y
`trm_en_fecha(fecha)` escritas, 27 casos cada una, las dos corridas contra la
fuente real. `evals.py` de **61 a 116 casos**, sigue en **0 fallos**, **$0.00** y
**sin red**. Dos defectos reales corregidos en el README (`historial(de,a,dias)`
era imposible con estas fuentes; el `dias` que miente). Dos defectos reales
encontrados **corriendo** (la normalización de la fecha; y el `4.0 == 4`
escondido en la comparación de dicts, tapado con `igual_estricto`).
**Y una vulnerabilidad de inyección demostrada en vivo y cerrada.**

**Los 7 sabotajes de la sesión:** 3 sobre `historial` (2, 9, 1 — las tres
predicciones exactas) y 4 sobre `trm_en_fecha` (1, 13, 1, 1 — tres exactas y
**una fallada, escrita con su razón**). Ninguna prueba de hoy se dio por buena
sin verla ponerse roja primero.

**Las candidatas a lección fuerte del 5b suben a TRECE.** Las seis de la sesión
12, más:
7. **Un plan escrito antes de mirar los datos se corrige con los datos**
   (`historial(de,a,dias)`, y el `dias` que miente).
8. **Decidir con el punto de equilibrio, no con la respuesta:** el 57% dice
   cuánto puedes equivocarte y seguir teniendo razón.
9. **El menú también se paga:** una herramienta de más cuesta en cada vuelta de
   cada conversación, aunque nunca se llame.
10. **INYECCIÓN — la primera vez que un dato de afuera entra a una consulta.**
    Demostrada en vivo (1 → 1000 filas). La defensa es la lista de PERMITIDOS,
    no la de prohibidos. Y `quote()` transporta, no decide.
11. **Después de validar, usa lo validado, no lo que llegó** (`2026-7-5`).
12. **El caso raro no es adorno: suele ser el único con ojos.** Dos pruebas
    independientes del mismo patrón hoy — `feliz con filas al reves` y
    `domingo` fueron los únicos que vieron su sabotaje.
13. **Escribir la prueba mejora el diseño**, no solo lo verifica: el `motivo`
    como dato nació de no poder comparar el texto del error.

⚠️ **Y una candidata de método, distinta de las técnicas:** hoy **dos defectos
reales salieron de CORRER, no de razonar** (la normalización, y que 30 filas
eran 48 días). Los dos los escribí yo convencido de lo contrario.
→ **"Verificar también lo que resultó ser verdad" tiene un hermano: verificar
también lo que uno acaba de escribir con toda seguridad.**

⚠️ **`LESSONS.md` sigue sin tocarse, y es correcto** (un bloque por nivel, al
cerrar el nivel). **Al cerrar el 5b hay que escribir las nueve.**

**Su intervención del día:** *"no es una decisión fácil, podemos analizarlo
mejor"* — frenó una decisión que se iba a tomar a ojo. De ahí salieron la
medición, el punto de equilibrio, el defecto del `dias` y su propia idea de
`trm_en_fecha`. **Segunda sesión seguida en que una pregunta suya cambia el rumbo
para bien** (la anterior fue *"¿la función tasa ya está totalmente
implementada?"*). Vale la pena decírselo.

⚠️⚠️ **DEUDA DE FORMATO — VAN 6 PIEZAS SEGUIDAS DICTADAS.** `pedir_json`,
`tasa`, la ampliación de `evals.py`, `trm`, `historial` y `trm_en_fecha`.
**Las dos veces de hoy se le dio el esqueleto con huecos numerados PRIMERO** (y
con `trm_en_fecha`, además, un ejemplo desechable sobre otra función), y las dos
veces pidió que se llenaran igual. Se le dijo una vez por sesión y no se repitió
— repetir es regañar, y esto es su curso.

**El dato duro para la próxima sesión: desde `convertir()` y `guardar_reporte()`
(sesiones 10 y 11) no ha escrito una línea de código él.** Lo que sí conserva:
lee, entiende, corrige diseños ajenos y toma buenas decisiones — hoy dos.

**Dónde cortar la racha, y hay una oportunidad natural en el paso 7:** el bucle
agéntico del nivel 3 **ya lo escribió una vez**. `agente.py` no es material
nuevo, es material que él ya tocó. Es el mejor sitio del nivel para que vuelva a
escribir. **Ofrecérselo así: "este ya lo hiciste una vez".**

⚠️ **Preferencia de formato observada (nueva):** rechazó **dos veces** el
selector de opciones y en cambio respondió largo y bien cuando las opciones se
le pusieron en texto normal. **Preguntarle en prosa, no con menús.**

---

## Histórico: sesión 12 (pasos 6 al 75%)

### URLs revisadas hoy 2026-07-30: las dos HTTP 200. Tercer dato de la brecha

| Día | Mercado | TRM oficial | Brecha |
|---|---|---|---|
| 2026-07-28 | 3.215,61 | 3.205,80 | ~10 pesos |
| 2026-07-29 | 3.206,17 | 3.205,87 | 0,30 pesos |
| **2026-07-30** | **3.207,64** | **3.206,18** | **1,46 pesos** |

Tres observaciones, tres brechas. **Confirma con datos** lo que el README decía
como sospecha: lo estable es *que son fuentes distintas*, nunca la magnitud.

### 🐛 DEFECTO REAL DEL README, CORREGIDO HOY

§5b.4 decía `?$order=vigenciadesde DESC` **con un espacio de verdad**. Verificado
con `curl` en la sesión 9 (y funcionaba: `curl` codifica el espacio solo). Pegado
en `urllib` **revienta**: `http.client.InvalidURL: URL can't contain control
characters`. Va `%20`. → **Una URL verificada con una herramienta no está
verificada para otra.** Es *"verificar también lo que resultó ser verdad"* otra vez.

### La decisión del "hueco 3" — y se validó POR ACCIDENTE a los 10 minutos

`pedir_json` **no tiene `except Exception`**. Razón dada: hay dos clases de falla
que se parecen y no son lo mismo.

| Falla | Qué es | Qué merece |
|---|---|---|
| No hay red, 503 | El **mundo** falló | `{"error": ...}` → conversación |
| `NameError`, un typo | **Nuestro código** está roto | Que se caiga fuerte y visible |

Un error del mundo es información; un error nuestro es un **defecto**, y taparlo
lo deja vivo para siempre disfrazado de "problemas de conexión".

⚠️ **Y pasó de verdad:** el espacio de la URL lanzó `InvalidURL`, que **no** es
hijo de `URLError` ni de `OSError` (comprobado). No lo atrapó nadie → salió el
traceback con la línea exacta y el motivo real. **Con `except Exception` habría
dicho "no pude conectarme" tras 3s de espera, y él se habría puesto a revisar el
router por un espacio en un texto.** → **Candidata a lección fuerte del 5b.**

⚠️ **Deuda que esto abre, apuntada en el código:** el contrato del archivo dice
"ninguna lanza excepciones". La red de seguridad va **en el harness** (paso 8):
un `try` alrededor de cualquier herramienta que le diga al modelo "falló por un
defecto interno" y a nosotros nos imprima el traceback — el bucle sobrevive **y**
el bug se ve. Misma forma que el permiso del nivel 4, que se pedía en el harness
y no dentro de `borrar_archivo()`.

### La regla del paso 6 (salió de una respuesta suya)

Se le preguntó quién debe reintentar cuando se cae el internet: A la función,
B el modelo, C el harness. **Contestó B, "porque el modelo decide si vale la
pena".** Buena razón, opción cara: cada reintento del modelo es **una vuelta más
del bucle** (se repaga SYSTEM + menú de 5 herramientas + historial) para preguntar
lo mismo. Un bucle dentro de la función cuesta **$0.00**. Es el mismo precio que
él ya aceptó a conciencia con `"usd"` en minúscula.

Su razón **no se descartó, se afiló** — la regla quedó así:

> **Reintenta donde sea más barato. Que el modelo decida solo lo que necesita
> criterio.** Falla mecánica (red, timeout, 503) → reintenta la función, gratis.
> Falla con juicio (es domingo y no hay TRM, la moneda no existe) → `{"error"}`
> y decide el modelo. Es lo que hace el SDK, que él ya midió: con 401 **no
> reintentó ni una vez**.

⚠️ **Antes había contestado "un mensaje de no conexión y que lo seguirá
intentando".** La primera mitad, perfecta. La segunda escondía **su propio
defecto de la sesión 11**: si el mensaje promete reintentos y la función ya
terminó, **el mensaje miente** — igual que el *"solo letras y números"* de
`guardar_reporte`. Se le señaló con su propia lección.

### `HTTPError` es HIJO de `URLError`: el orden de dos líneas decide todo

Se le demostró **corriéndolo** contra un 404 real, con las dos versiones:

```
padre primero : PASAJERO -> reintentaria 3 veces  (HTTPError)
hijo primero  : PERMANENTE -> corta de una  (codigo 404)
```

Detalle que más enseñó: en la versión mala `type(e).__name__` **dice `HTTPError`**
y trae el 404 adentro. → **La excepción no te mintió; tú no preguntaste bien.**
**Es la imagen en espejo de L4.x del nivel 4** (*"el caso general atrapa hijos que
no sabías que existían"*, `APITimeoutError` hija de `APIConnectionError`): allá la
herencia **ayudaba** porque querías tratarlos igual; aquí **traiciona** porque los
quieres tratar distinto. **Regla: cuando dos excepciones son familia y las tratas
distinto, el hijo va primero.**

### La corrida de `pedir_json` — 7 casos, $0.00, sin Claude

| Caso | Tiempo | Resultado |
|---|---|---|
| 1. feliz: mercado | 0.32s | datos OK |
| 2. feliz: TRM (con `%20`) | 0.52s | datos OK, `valor 3206.18` |
| 3. permanente: 404 | **0.54s** | `error HTTP 404` |
| 4. pasajero: host inexistente | **3.11s** | `URLError` tras 3 intentos |
| 5. pasajero: `timeout=0.001` | 3.27s | `URLError` |
| 6. borde: `intentos=0` | 0.00s | mensaje, **no `NameError`** |
| 7. espacio en la URL | — | **REVENTÓ** con `InvalidURL` ✅ |

Lo que hay que conservar de esta tabla:

1. **El par 3 vs 4 (0.54s vs 3.11s) PRUEBA que el permanente no reintenta.** No
   se supone: se mide. De los 3.11s, **3 son puro `sleep`** (1s + 2s). Es su
   técnica del nivel 4 (`max_retries=5` con 401 = 0.39s vs 3 reintentos = 3.00s)
   aplicada a su propio código. → **Un número solo significa algo al lado de otro.**
2. **Caso 5: `timeout=0.001` tardó 3.27s.** El timeout limita **cada intento**,
   no el total; las esperas se suman aparte. Tercera confirmación de que
   `timeout` × `intentos` se multiplican.
3. **Inicializar `ultimo` antes del `for` se ganó el sueldo en la primera
   corrida** (caso 6). Era un defecto de MI esqueleto: con `intentos=0` el `for`
   no da vueltas y el `return` final usaba una variable que nunca nació.

⚠️ **HALLAZGO INCÓMODO SIN RESOLVER: `TimeoutError` nunca disparó.** El caso 5 se
diseñó para provocarlo y salió `URLError` — `urllib` envuelve el vencimiento de
tiempo **al conectar**. Nuestro `except` lo menciona sin prueba de que atrape algo:
**es el freno 3 de `guardar_reporte()` otra vez.** Sospecha *no medida* (se le dijo
que era sospecha): saldría pelado si el tiempo se vence **leyendo** la respuesta,
no conectando. → **Pendiente medible**, como los 278.916 nombres.

⚠️ **Formato: esta pieza fue DICTADA.** Se le dio el esqueleto con 3 huecos para
que llenara los 2 primeros y pidió *"amgio escribelo, muestralo y explicalo"*. Se
dictó y **queda anotado** para no perder la cuenta de qué código pasó por su cabeza.
Antes pidió *"escribeme un ejemplo primero"* (tercera vez que usa esa muletilla, y
funciona): se le dio sobre **otra** función desechable (`leer_config`, con
`FileNotFoundError` permanente vs `PermissionError` pasajero, las dos hijas de
`OSError`) **diciendo explícitamente que no va en su archivo** — la advertencia que
faltó con `doblar` en la sesión 11. Se le dejó un `SyntaxError` a propósito en el
ejemplo (el mismo suyo de la sesión 11: coma en vez de dos puntos).

### `tasa()` — escrita y probada (8 casos + 12 pares, $0.00 de Claude)

**Dictada** (pidió *"escribelo y despues me explicas paso a paso"*). Se le avisó
que era la 2ª pieza seguida dictada y **se le ofreció un trato: `tasa` dictada,
`trm` la escribe él.** Aún no lo confirma.

**El concepto del día: la triangulación.** La API entrega TODO contra el dólar
(`base_code = "USD"`), 166 monedas. Un par como EUR→COP **no existe en el JSON**.

```
tasa(de, a) = rates[a] / rates[de]
```

Verificado numéricamente por los dos caminos: paso a paso (1/0.875576 = 1.1421
USD, × 3207.637776) da `3663.460140524637`; la fórmula da `3663.4601405246376`.
Iguales hasta el decimal 12 (la diferencia es `float` — la deuda de `Decimal`).
**Regalo:** como `rates["USD"] = 1`, la misma fórmula cubre los 12 pares **sin
un `if` especial para el dólar**. `USD→USD` dio `1.0` en la corrida.

**El recorte, y él dio la razón correcta antes de que se la dijera:** se le
preguntó qué devolver y contestó *"algo mas pequeño, solo la tasa, porque se
reenvia en cada vuelta"* — o sea aplicó solo su medición del nivel 3 (los
`tool_result` de 18/20/46 tokens). **2.967 caracteres → ~130. Unas 22x.**
→ **Lo que devuelve una herramienta no se paga una vez: se paga en cada vuelta
que le quede a la conversación. Un `tool_result` gordo es un impuesto permanente.**

⚠️ **Se le afinó "solo la tasa":** se conserva `time_last_update_utc` porque **sí
se gana sus tokens**. Mercado y TRM dan números distintos para el mismo día
(3207,64 vs 3206,18), así que una tasa sin fecha ni fuente es **correcta e
inútil a la vez** — y es la rúbrica "¿citó la fuente?" del paso 10.
→ **La regla no es "devuelve lo mínimo", es "devuelve lo que se gana sus tokens".**

**Lo nuevo estructural: hay un SEGUNDO desconocido.** Hasta hoy se desconfiaba
solo del modelo. Ahora el dato lo manda **un servidor ajeno**, que puede cambiar
de formato, quitar una moneda o mandar `null` sin avisar. Por eso `tasa` tiene
frenos **sobre la respuesta**, no solo sobre los argumentos.
- `rates.get(de)` + `es_numero()` → **un solo freno cubre tres desastres**
  (llave ausente, `null`, texto). Reusa el `es_numero()` que él escribió.
- `if valor_de <= 0` evita `ZeroDivisionError`. Es su propio `tasa <= 0` de
  `convertir()`, pero apuntando al servidor en vez de al modelo.

⚠️ **LA TRAMPA DEL REDONDEO (se le dijo "no redondees, quiero que la veas").**
`COP→USD` dio `0.0003117558994603884`. Redondear la tasa a 2 decimales "para que
no sea tan larga" da **`0.0`**, y entonces su propio freno `tasa <= 0` la
rechazaría: la herramienta correcta destruida por un cambio cosmético.
→ **`DECIMALES` redondea el RESULTADO en dinero, nunca la TASA.** Son dos números
con precisiones distintas: uno es plata que alguien paga, el otro es un factor.

⚠️ **Decisión mía, revocable:** `USD→USD` se acepta y devuelve `1.0`, gastando una
llamada de red para averiguar que un dólar es un dólar. Se podría cortar con
`if de == a`. Se dejó simple a propósito. Mismo patrón que `monto cero`.

### 🐛 HALLAZGO GRANDE DEL DÍA: las 3 funciones incumplían el contrato

Salió de una corazonada al ver que `tasa(123, "COP")` se rechazaba bien. **Seis
funerales**, comprobados corriéndolos:

```
convertir       de=[]        -> TypeError: unhashable type: 'list'
convertir       a={}         -> TypeError: unhashable type: 'dict'
guardar_reporte nombre=[]    -> AttributeError: 'list' has no attribute 'endswith'
guardar_reporte nombre=5     -> AttributeError: 'int' has no attribute 'endswith'
guardar_reporte contenido=None -> TypeError: data must be str, not NoneType
tasa            de=[]        -> TypeError: unhashable type: 'list'
```

**La causa:** `x in un_diccionario` funciona con cualquier valor **hashable**
(números, texto, `None`, booleanos), así que la prueba de pertenencia hacía **de
paso** un control de tipo. Con una lista Python no dice "no está": dice
`TypeError`. **Funcionaba por casualidad, y la casualidad tenía un borde.**

⚠️⚠️ **LO IMPORTANTE NO ES EL BUG: `evals.py` tenía 26 casos, 0 fallos, y NO VE
NINGUNO DE LOS SEIS.** Es la segunda prueba —y más filosa que la del banker's
rounding— de la lección que ya estaba anotada: *el eval no dice "tu código está
bien"; dice "estas 26 cosas se comportan como dijiste"*. **Los 26 en verde
mientras el contrato del archivo estaba roto en tres sitios.**
→ **Candidata a LECCIÓN FUERTE del 5b, junto con la del hueco 3.**
Y no es un caso raro: el modelo manda **JSON**, donde una lista se escribe igual
de fácil que un número. Es `monto="10"` otra vez.

**El arreglo: lo decidió él, opción B.** Se le dieron A (un `if` en cada función)
y B (ayudante compartido) y contestó *"B, porque una regla en un solo sitio"* —
consistente con sus dos precedentes (`es_numero`, `MONEDAS = tuple(DECIMALES)`).
Se implementaron **dos** ayudantes porque son dos reglas, y el segundo se
construye sobre el primero:
- `es_texto(x)` → `isinstance(x, str)`. Lo usa `guardar_reporte` (nombre y contenido).
- `es_moneda(x)` → `es_texto(x) and x in DECIMALES`. Lo usan `convertir` y `tasa`
  (4 sitios). **Junta las dos preguntas** que antes estaban implícitas en una.
- En `guardar_reporte` el nuevo bloque es el **freno 0** y va **antes** de todo:
  los frenos 1 y 2 usan métodos de texto, y un método de texto sobre una lista
  no devuelve `False`, **lanza**. Mismo orden forma→contenido de `convertir()`.
- Los mensajes dicen **"entre comillas"**: es el **espejo** del *"sin comillas"*
  de los frenos numéricos. Al modelo hay que decirle la FORMA del JSON.

**Verificado:** `9 casos, 0 funerales` · `evals.py` sigue en `26 casos, 0 fallaron`.

### ✅ Y una decisión suya de la sesión 11 que se pagó HOY

Se reescribió la **redacción de 4 mensajes de error** de sus dos funciones y **no
se rompió ni uno de los 26 casos**. Pudo pasar porque en el paso 5 él decidió que
el eval compara `"error"` contra un número y **nunca el texto del mensaje**
(*"si comparas el texto, mejorar el mensaje rompe la prueba"*).
→ **Una prueba bien diseñada te deja mejorar el código; una mal diseñada te lo
congela.** Vale la pena decírselo: fue su decisión y le pagó una sesión después.

### ✅ `evals.py` AMPLIADO: **35 casos, 0 fallos**, $0.00 y sin red (DEMOSTRADO)

**Dictado** (pidió *"trabja en lso nueve casos, llevalso a evals.py"*). Tercera
pieza seguida dictada — **ver la deuda de formato al final de esta sección.**

**La decisión de diseño se resolvió sola: 7 de los 9 casos entraron en sus dos
listas existentes** sin tocar el bucle; solo se agregaron filas. Solo `tasa`
necesitó lista y bucle nuevos.
→ **Las pruebas se agrupan por la función que prueban, no por el bug que las
descubrió.** La tentación era una lista "casos del contrato": habría repartido
las pruebas de `guardar_reporte` por fecha de descubrimiento en vez de por función.

### 🪤 LA PIEZA NUEVA: la TRAMPA DE RED

El archivo prometía en su docstring *"no usa internet y cuesta $0.00"*. Meter
`tasa` ponía eso en riesgo. El razonamiento era: sus casos son todos de RECHAZO y
los frenos de moneda van ANTES de pedir el dato, así que mueren sin salir de la
máquina. **Pero eso era un razonamiento, no una prueba** (su lección del freno 3).

```python
def trampa_de_red(*args, **kwargs):
    raise AssertionError("un caso llego a la red: este eval debe costar $0.00")
herramientas.pedir_json = trampa_de_red
```

→ Antes: *"creo que no toca la red"*. Ahora: **"si toca la red, se ve"**.
Es **su técnica del sabotaje al revés**: con el `write_text` comentado rompió **el
código** para ver si la prueba lo notaba; aquí se rompe **el camino prohibido**
para ver si alguien lo pisa.

⚠️ **El camino feliz de `tasa` NO cabe en `evals.py` y está dicho en el archivo:**
no se puede exigir un número fijo a una tasa que cambia a diario ni depender de
que el servidor esté vivo. Eso es de los pasos 9 y 10. **Aquí solo rechazos.**

### Los DOS sabotajes que comprueban que todo esto sirve

**A — la trampa:** con la trampa puesta se pidió `tasa("USD","COP")` (camino
feliz, necesita red) → **saltó `AssertionError`** ✅. Y `tasa([],"COP")` pasó
tranquilo sin saltar ✅. Los dos comportamientos buscados.

**B — los 9 casos nuevos:** se rompieron `es_moneda` y `es_texto` para que
**siempre devolvieran `True`** y se corrió el eval → **`35 casos, 12 fallaron`**
(los 9 nuevos + 3 viejos que también dependen de `es_moneda`). Archivo restaurado
y verificado de vuelta en 35/0. **Los casos nuevos no son adorno.**

⚠️⚠️ **EL HALLAZGO QUE DA MIEDO, del sabotaje B:**

```
FALLA moneda lista    esperado='error'    obtenido=39000
```

Con el freno roto, `convertir(10, [], "COP", 3900)` **devolvió 39000**. Convertir
10 de *lista vacía* a pesos entregó **una cantidad de dinero perfectamente
creíble**. Es idéntico a `monto=True → 3900`.
→ **Un error que revienta te avisa; un error que devuelve un número creíble no.**
Es la categoría más peligrosa del proyecto. **Candidata a lección fuerte.**

**Y aquí se ve el valor concreto de su respuesta "B":** un sabotaje de **dos
líneas** puso rojos **12 casos en 3 funciones**. Si la regla vive en un sitio,
romperla se ve en todas partes.

**Regalo no buscado:** en el sabotaje B la sección de `tasa` dio
`REVENTO: AssertionError` — **la trampa de red disparó**, porque con el freno roto
`tasa([],"COP")` sí llegó a buscar internet. La trampa hace **dos** trabajos:
documenta que el eval es gratis **y detecta un freno roto** por la puerta de atrás.

### ⚠️ DECISIÓN PENDIENTE PARA ÉL (anotada en el código, no resuelta)

El tercer bucle es **casi idéntico** al de `convertir`: solo cambian la función
llamada y la llave del resultado (`"resultado"` vs `"tasa"`). Con
`guardar_reporte` el bucle aparte SÍ estaba justificado (revisa el disco, es otro
trabajo); aquí no. **Su propio argumento *"una regla en un solo sitio"* ahora
apunta al otro lado.** Se dejó separado para no tocar el bucle que escribió él.
Las dos respuestas son defendibles y la decisión es suya.

### ⚠️⚠️ DEUDA DE FORMATO — HAY QUE ATAJARLA LA PRÓXIMA SESIÓN

**Tres piezas seguidas dictadas** en la sesión 12: `pedir_json`, `tasa` y la
ampliación de `evals.py`. Todas las pidió él (*"escribelo"*, *"trabja en los nueve
casos"*), se le avisó y se le ofreció un trato explícito (**`tasa` dictada, `trm`
la escribe él**) que **no confirmó**. El README del nivel dice por qué importa:
*"si se le dicta todo, termina con un agente que funciona y que no sabría
rehacer — sería el único nivel donde el código no pasó por su cabeza."*
→ **`trm` debería escribirla él**, con `tasa` delante como modelo (son casi la
misma forma). Si vuelve a pedir dictado, dictarlo — es su curso —, pero **decirlo
una vez más y seguir contando**. Lo que sí funciona y hay que conservar: darle un
esqueleto con **huecos numerados** y un ejemplo sobre **otra** función desechable.

### ✅ `tasa()` CERRADA BIEN: `evals.py` en **45 casos, 0 fallos**, $0.00 y sin red

Él eligió la opción **A** ("cerrar `tasa` bien") sobre la B ("seguir y anotarlo"),
después de que se le dijera qué le faltaba de verdad a la función. Preguntó
*"¿la función tasa ya está totalmente implementada?"* y **la respuesta honesta era
NO**: la lógica funcionaba, pero **3 de sus 5 caminos jamás se habían ejecutado**
(los dos frenos sobre la respuesta del servidor y el camino de error de red).
Escritos, legibles, y sin correr una sola vez — podían tener un typo.

### 🎭 LA PIEZA NUEVA: el DOBLE (servidor de mentira)

Sale de la trampa de red: **si se puede reemplazar `pedir_json` por uno que
revienta, se puede reemplazar por uno que finge ser un servidor con problemas.**

```python
def servidor_falso(respuesta):
    def falso(url, **kwargs):
        return respuesta
    return falso
```

10 casos nuevos (`CASOS_TASA_FUENTE`), cada uno con la respuesta falsa que
`pedir_json` va a devolver, en su misma forma `(datos, error)`: sin llave `rates`,
moneda ausente, `null`, valor de texto, divisor cero, divisor negativo, error de
red, y **tres felices**.

### ⭐ EL HALLAZGO CONCEPTUAL DEL PASO — corrige una nota del propio plan

El plan del nivel decía que estas tres herramientas *"no se pueden probar como las
otras dos, dependen de un servidor ajeno"*. **Resultó medio falso: lo que estaba
mal era la pregunta.** Había DOS metidas en una:

| Pregunta | ¿Necesita internet? |
|---|---|
| ¿Mi aritmética está bien? ¿Los frenos atrapan? | ❌ **No.** Los datos los pongo yo |
| ¿El servidor sigue vivo y con el mismo formato? | ✅ Sí, sin remedio |

→ **No es que una herramienta de red no se pueda probar: es que hay que separar
"¿mi código está bien?" de "¿el mundo está como creo?".** La primera se prueba en
tu máquina siempre; la segunda nunca. **Candidata a lección fuerte del 5b.**

**Y el camino feliz SÍ cabe, determinista:** con `1 EUR = 2 USD` y
`1 USD = 4000 COP`, la triangulación **tiene que** dar 8000 y se verifica a ojo.
Con la fuente real era imposible: la tasa cambia a diario, no hay esperado fijo.
```
feliz USD->COP    esperado=4000.0    obtenido=4000.0
feliz EUR->COP    esperado=8000.0    obtenido=8000.0
```

### El sabotaje, con PREDICCIÓN ACERTADA (y la cuenta se lleva en los dos sentidos)

Se predijo por escrito **antes de correr**: *"6 FALLA, cinco reventones y uno que
devuelve un número creíble: `divisor negativo` daría `-4000.0`"*. **Salió exacto.**

```
FALLA sin llave rates   -> REVENTO: TypeError
FALLA moneda ausente    -> REVENTO: TypeError
FALLA valor null        -> REVENTO: TypeError
FALLA valor texto       -> REVENTO: TypeError
FALLA divisor cero      -> REVENTO: ZeroDivisionError
FALLA divisor negativo  -> -4000.0
45 casos, 6 fallaron
```

⚠️ **Tercera aparición HOY del mismo patrón:** con el freno apagado, la tasa
negativa **no revienta**, devuelve `-4000.0`. Menos creíble que el `39000` porque
el signo canta, pero **el agente lo reportaría como respuesta, no como falla**.
(Los tres del día: `monto=True → 3900`, `moneda=[] → 39000`, `tasa<0 → -4000.0`.)

### Dos detalles del código, dichos en la explicación

1. **`servidor_falso` es una función que fabrica funciones**, no un `lambda` en el
   bucle: un `lambda` ahí se acordaría de la **última** respuesta del bucle, no de
   la de su caso. Trampa clásica de Python, evitada a propósito.
2. **`4000 / 1` da `4000.0`, no `4000`** — en Python 3 `/` siempre devuelve float.
   Por eso el esperado es `4000.0`. **Lo detectó su comparación estricta de tipos**,
   la que endureció en el paso 5 tras el `4.0 == 4`. **Segunda vez que le paga.**

### ⚠️ EL LÍMITE DEL DOBLE, dicho explícitamente (patrón de la casa)

**Un doble prueba tu código contra TUS SUPOSICIONES sobre el servidor, no contra
el servidor.** El nuestro asume que el mercado manda números; si mañana manda
texto, los 10 casos siguen verdes y el agente se rompe en producción. Por eso el
caso `valor texto` existe (es el formato real de datos.gov.co: `"3206.18"`) y por
eso en el paso 9 hace falta **una** corrida contra las fuentes de verdad.
Mismo espíritu que *"el eval no puede demostrar que no escribió fuera de caja/"*.

### Lo que a `tasa()` le sigue faltando (y no es código)

1. Una corrida real contra la fuente viva → **paso 9**.
2. `USD→USD` gasta una llamada de red para saber que un dólar es un dólar
   (decisión mía, revocable, sin resolver).
3. **El modelo todavía no sabe que existe:** falta describirla en la lista `tools`
   → **paso 7**.

### ✅ `trm()` — escrita, probada (16 casos) y corrida contra la fuente real

**Dictada** (pidió *"armala y despues cierra la sesion"*). Cuarta seguida — la
deuda de formato de más abajo sigue viva y **es lo primero de la próxima sesión**.

⚠️ **CAMBIO DE DISEÑO, y lo corregí sobre mi propia propuesta:** yo había dicho
`trm(dias=1)`. **Va SIN parámetro.** Si `trm` supiera traer varios días haría a
medias el trabajo de `historial`, y **dos herramientas que se pisan obligan al
modelo a elegir entre dos caminos para lo mismo.** `trm()` = la más reciente;
`historial(dias)` = la serie. Una cosa cada una.

**Las tres cosas nuevas de `trm`, y las tres dieron material:**

1. **La fuente devuelve una LISTA de filas**, no un diccionario como la de
   mercado. → **Dos fuentes, dos formas: cada herramienta conoce la suya.** Sin
   el freno, `datos[0]` sobre una lista vacía es un funeral.
2. **`valor` viene como TEXTO** (`"valor":"3206.18"`, con comillas en el JSON).
   Van **dos frenos porque son dos preguntas**, igual que en `convertir()`:
   - **FORMA** (`es_texto` o `es_numero`) → descarta `None`, listas, dicts y
     booleanos.
   - **CONTENIDO** (`try: float(...) except ValueError`) → descarta `"abc"`, `""`
     y ⚠️ **`"3.206,18"`**, que es **cómo se escribe la plata en Colombia**:
     coma decimal y punto de miles. `float()` lo rechaza. Es el caso más
     realista de la lista y está escrito como prueba.
3. **EL DOMINGO — resuelto con su propia regla.** `trm()` **no decide**: devuelve
   `vigente_desde` y `vigente_hasta` bien visibles y **la decisión sube al
   modelo** (usar la del viernes y avisar, o decir que espere). El caso de prueba
   **no se inventó**: la TRM del viernes 24 vigente hasta el domingo 26.
   → Primera vez en el curso que la regla *"que el modelo decida solo lo que
   necesita criterio"* se aplica **al diseño de una herramienta**, no a un error.

⚠️ **Decisión de diseño con razón que no hay que perder: `trm()` NO calcula
"¿es de hoy?".** Para eso tendría que mirar el reloj, y entonces dependería de
**dos mundos** (la fuente y la hora de la máquina) y **dejaría de ser probable con
datos fijos** — el eval no podría afirmar nada estable. Si el agente necesita la
fecha de hoy, **eso es otra herramienta**, como `hora_utc` en el nivel 3.
→ **Una función que mira el reloj deja de ser determinista, y con eso se pierde
la única forma barata de probarla.**

**Los 16 casos** (`CASOS_TRM`) van **todos** con servidor de mentira: `trm()` no
recibe argumentos, así que **no hay nada que rechazar antes de salir a la red**.
Sin el doble, esta función no se podía probar en absoluto.

✅ **LA CORRIDA REAL (la que el doble no puede reemplazar), 2026-07-30:**

```
trm()   -> 3206.18   vigente_desde/hasta = 2026-07-30   (llegó como texto, salió número)
tasa()  -> 3207.637776                                   brecha = 1.46 pesos
```

La brecha coincide con la medida al empezar la sesión. **Las dos fuentes vivas y
con el formato que suponíamos** — que es exactamente lo único que el doble no
podía decirnos.

---

## Cierre de la sesión 12

**Lo que se hizo:** paso 6 al 75%. `pedir_json` + `tasa` + `trm`, las tres
probadas. `evals.py` pasó de **26 a 61 casos**, sigue en **0 fallos**, **$0.00** y
**sin red demostrado** (la trampa). Un defecto real corregido en el README.
El contrato del archivo reparado en las 3 funciones que lo incumplían.

**Los 4 sabotajes de la sesión** (la técnica que más rindió): la trampa de red,
`es_moneda`/`es_texto` siempre True (12 rojos), y los dos frenos de `tasa` sobre
la respuesta del servidor (6 rojos, **con predicción acertada**). Ninguna prueba
de hoy se dio por buena sin verla ponerse roja primero.

**⚠️ `LESSONS.md` NO se tocó, y es correcto:** su regla es **un bloque por nivel**,
al cerrar el nivel. Las candidatas a lección fuerte del 5b están acumuladas en
esta bitácora y son ya **seis**: (1) el hueco 3 / no tapes tus propios bugs,
(2) los 26 verdes con el contrato roto, (3) el número creíble es peor que el
reventón, (4) separar "¿mi código está bien?" de "¿el mundo está como creo?",
(5) el doble prueba tus suposiciones, no el servidor, (6) el `tool_result` es un
impuesto permanente. **Al cerrar el nivel 5b hay que escribirlas.**

**Dudas suyas de hoy:** una sola, y muy buena — *"¿la función `tasa` ya está
totalmente implementada?"*. **Preguntó justo cuando yo iba a seguir de largo**, y
de ahí salió todo el trabajo del doble. Vale la pena decírselo: esa pregunta
cambió el rumbo de la sesión para bien.

---

## Histórico del paso 6: notas previas

**Lo que decía antes este bloque: `trm(dias=1)`** — la TRM oficial de datos.gov.co, con
`URL_TRM` (ya en el archivo, con el `%20`). Sus problemas propios, y son nuevos:
1. **El domingo no hay TRM nueva.** Aquí SÍ manda su razón (*"el modelo decide si
   vale la pena"*): usar la del viernes y avisar que es del viernes, o decir que
   espere, **necesita criterio** → `{"error"}` o un dict con la fecha bien visible.
   El dato lo trae la fuente: `vigenciadesde`/`vigenciahasta` (la del 25 de julio
   valió hasta el 27). **El caso de prueba no hay que inventarlo.**
2. **`valor` viene como TEXTO** (`"3206.18"`, con comillas en el JSON). Hay que
   convertirlo, y esa conversión puede fallar → otro freno sobre la respuesta.
3. Después `historial`: **recortar el JSON de 30 días ANTES de devolverlo**.

---

## Histórico: paso 5 (sesión 11)

**SIGUIENTE PASO (ya cumplido en la sesión 12): paso 6 — las 3 herramientas que SÍ tocan la red**
(`tasa`, `trm`, `historial`), formato **mixto**. Las 2 URLs están verificadas en
`05b-proyecto/README.md` §5b.4 (HTTP 200 el 2026-07-29) — ⚠️ **volver a
comprobarlas**, ya pasaron varios días. Aquí aparecen problemas nuevos que las dos
primeras herramientas no tenían: el domingo sin TRM, el JSON de 30 días que se
reenvía en cada vuelta (recortar la salida ANTES de devolverla), y que **estas
tres no se pueden probar como las otras dos** — dependen de un servidor ajeno.

### Las dos decisiones abiertas: CERRADAS (las dos se rechazan)

Lo decidió él: `"10"` como texto **no** se convierte a número, y `"usd"` **no** se
pasa a mayúsculas. ⚠️ **Se le dijo lo que cuesta la segunda y hay que medirlo en el
paso 9:** cada minúscula gasta **una vuelta extra del bucle** (manda `"usd"`, lee el
error, reintenta con `"USD"`) = 2 llamadas a la API en vez de 1. Con `.upper()`
habría sido gratis. Si aparece mucho en `registro.jsonl`, se revisa **con datos**.

### Los arreglos a `convertir()` (los pidió dictados: *"realiza los cambios directamente"*)

Se aplicaron **de uno en uno, corriendo `evals.py` después de cada uno**: 8 fallos
→ 4 → (se agregan los booleanos) 6 → 4 → **0**. El orden fue de lo más grave a lo
más pequeño: primero lo que tumba el bucle, de último lo cosmético.

1. **Frenos de FORMA vs frenos de CONTENIDO**, agrupados y rotulados. Los de tipo
   van primero porque si el dato no es número la función no puede hacer *nada*;
   los de moneda son sobre el significado. Dos `if` separados (uno por parámetro)
   para que el mensaje **nombre al culpable** — con uno solo, el modelo reintenta
   a ciegas. Los mensajes dicen el tipo que llegó (`type(x).__name__`) y traen
   ejemplo **"sin comillas"**, que es lo que de verdad corrige el `"10"`.
2. ✅ **Los booleanos: los pidió él** (*"agrega también el caso de los booleanos"*),
   después de que se le señalara el hueco. **Primero se vieron fallar:**
   `monto=True` → **3900** y `tasa=True` → **10**, o sea una cantidad de dinero
   creíble. `isinstance(True, int)` es `True` porque en Python `True` vale 1.
   → Se sacó a un ayudante `es_numero(x)` en vez de repetir la condición:
   **una regla, un sitio.** Mismo motivo que `MONEDAS = tuple(DECIMALES)`.
   `es_numero` va en un bloque rotulado como **ayudante interno, no herramienta**
   (el modelo nunca la llama, no entra en `tools`) — distinción que importa en el paso 7.
3. **`monto < 0`** rechaza; **el cero se acepta** y devuelve 0. Esa decisión llevaba
   colgando desde la pregunta *"¿monto=0 es accidente o es válido?"*, que nunca se
   contestó: **la tomé yo y se le dijo que era mía y revocable.** Se escribió como
   **caso de prueba** (`("monto cero", ..., 0)`) → *un caso de prueba es la forma
   más duradera de escribir una decisión: un comentario se ignora, un caso rojo no.*
4. **`tasa <= 0`** en un solo `if`: tasa cero y negativa son **la misma idea** (una
   tasa siempre es positiva). ⚠️ **La asimetría `monto < 0` vs `tasa <= 0` parece
   un descuido y no lo es** — está anotada en el código: la forma del `if` sale del
   mundo real, no de la simetría. Aquí murió el fallo más silencioso de la función
   (tasa 0 devolvía `0`, y un `0` se ve legítimo).
5. **El `round`:** `round(3.7, 0)` → `4.0` (decimal) pero `round(3.7)` → `4`
   (entero). **No son la misma llamada.** Por eso hay un `if decimales == 0`.

### ⚠️ DEFECTO CONOCIDO, SIN ARREGLAR: banker's rounding

Con los 16 casos en verde, se le mostró que **verde no significa correcto**:

```
0.5 -> 0    1.5 -> 2    2.5 -> 2    3.5 -> 4    4.5 -> 4
```

Python redondea **al par más cercano** cuando el número cae justo en la mitad
(para no sesgar sumas grandes hacia arriba). Para estadística está bien; **para
dinero la norma contable suele ser "medio para arriba"**. Los 16 casos no lo
detectan porque **ninguno cae en `.5`** — el eval contesta exactamente las 16
preguntas que se le hicieron y nada más.

→ **Ejercicio del nivel:** agregar los casos `.5`, verlos fallar, y arreglarlo con
**`Decimal`** (el tipo que Python trae para dinero) en vez de `float`. No es un
`if`, es un tema entero — por eso se dejó anotado y no hecho.

→ Candidata a lección fuerte: *el eval no dice "tu código está bien"; dice "estas
16 cosas se comportan como dijiste". Todo lo demás sigue sin explorar.*

### Los 10 casos de `guardar_reporte` — el problema nuevo: el EFECTO SECUNDARIO

`convertir()` es pura: solo devuelve, así que revisar lo devuelto es revisar todo.
`guardar_reporte()` **cambia el mundo**, y lo que devuelve es apenas un recibo.
Se le mostró con un experimento mental: si alguien comenta el `write_text`, la
función **devuelve exactamente lo mismo** y no guarda nada. Es L4.9 del otro lado —
allá el agente decía *"ya lo borré"* con el archivo intacto; aquí es **la prueba**
la que dice *"ya lo guardó"*.

**Las tres respuestas se las dio él, una por pregunta** (la regla de una pregunta a
la vez funcionó otra vez):

1. *"que el archivo estuviera en la ruta"* → hay que comprobar que **existe**.
2. *"que el contenido sea el que se le pasó"* → y que **coincida** (podría crearlo
   vacío, o escribirlo dos veces).
3. Se le mostró que `caja/reporte-trm-2026-07-30.txt` **seguía vivo desde la
   mañana**, así que "el archivo existe" pasaría aunque la función ya no escribiera.
   Contestó: *"borrar el archivo antes de la prueba o marcarlo como no actual"*.
   → La primera es la estándar; la segunda (comparar la fecha) depende del reloj y
   de la precisión del sistema de archivos: más frágil por más trabajo.
   **Nombre del concepto que se le dio: la prueba arranca de un ESTADO CONOCIDO.**
   No "probablemente vacío": vacío porque tú lo vaciaste.

**Cómo quedó implementado:**
- `limpiar_caja()` corre **antes de cada caso**, no una vez al principio → **cada
  caso independiente de los demás.** Si el orden importa, son 10 casos encadenados,
  no 10 pruebas. Solo borra dentro de `caja/`, nunca sube.
- El veredicto tiene **dos mitades**: `ok = (obtenido == esperado) and (pero == "")`.
  `obtenido` = ¿dijo lo correcto? · `pero` = ¿el disco quedó como debe? El texto
  del `pero` se imprime, así que al fallar se ve **cuál** mitad se rompió.
- **Bucle aparte**, no un `if` dentro del primero: dos trabajos distintos, dos
  bucles. Con banderas quedaba ilegible.
- Los 7 casos que esperan `error` comprueban además que **`caja/` quedó vacía** —
  una función podría escribir y *después* devolver error, que es peor que no validar.
- `limpiar_caja()` también al final: el eval no deja basura (verificado: 0 archivos).

✅ **SE COMPROBÓ QUE LAS PRUEBAS SIRVEN, con sabotaje.** Se comentó el
`write_text` a propósito y salieron **3 FALLA** con el mensaje
`esperado='guardado' obtenido='guardado' PERO NO HAY ARCHIVO` — o sea las dos
primeras columnas **coincidían** y lo atrapó solo la revisión del disco. Se
restauró la línea y volvió a 26/0. Es la técnica del nivel 3 (ejercicios de
sabotaje) aplicada a un eval.

⚠️ **Límite conocido de este eval, dicho explícitamente:** comprueba que no
escribió *dentro* de `caja/`, pero **no puede demostrar que no escribió fuera**.
Si `../../.env` pasara los frenos, el archivo caería en la raíz y el eval no lo
vería. Para eso se confía en los 3 frenos + la prueba de fuerza bruta de 278.916
nombres. **La prueba es parcial, y saber dónde acaba es parte de tenerla.**

**Decisión nueva del día (mía, revocable, escrita como caso):** contenido vacío
**se acepta** — un reporte sin datos es raro pero no es un error de formato. Mismo
patrón que `monto cero`.


El nivel 5 quedó cerrado en la sesión 9 (detalle más abajo). La sesión 10 arrancó
el 5b: se creó `05b-proyecto/`, se escribió el `README.md` del nivel completo
(§5b.0 a §5b.5, con **el plan de los 10 pasos y quién escribe cada uno**), y
**él escribió `convertir()` entera** — la primera función del curso que sale de su
cabeza y no de un dictado. La sesión 11 cerró el paso 4 con `guardar_reporte()`,
**también escrita por él**.

**Estado de los archivos del 5b:**

| Archivo | Estado |
|---|---|
| `README.md` | ✅ completo hasta §5b.5 (Ejercicios y "Lo que ya sabes" vacíos a propósito) |
| `herramientas.py` | ✅ las 2 que no tocan internet (`convertir`, `guardar_reporte`) + el ayudante `es_numero`. Faltan las 3 de red |
| `evals.py` | ✅ 26 casos (16 de `convertir` + 10 de `guardar_reporte`), 2 bucles, **0 fallos** |
| `agente.py` | ⬜ vacío (0 bytes) |

### Paso 5 — `evals.py` (sesión 11)

**Lo escribió él: los casos, el bucle y la tabla.** El diseño quedó así: cada caso
es **un dato de tres partes** `(etiqueta, argumentos, esperado)`, y `esperado` es
un número (se compara contra `r["resultado"]`) o el texto `"error"` (solo importa
QUE rechace, **nunca la redacción** del mensaje — si comparas el texto, mejorar el
mensaje rompe la prueba). Un bucle recorre todo y cuenta.

**Cómo salieron los casos, y esto es lo que hay que conservar del método:** se le
enseñaron las **tres familias** (camino feliz / bordes / lo malo) y se le dijo que
la familia que todo el mundo se salta es la de **los bordes**. Los propuso él.

- ⚠️ **Confusión suya que hay que recordar:** propuso *"valores negativos para
  `monto`, `de` y `a`"*. `de` y `a` son **texto** (nombres de moneda), no números.
  Se corrigió y de ahí salió que **el número que se le había pasado era `tasa`**.
- ✅ **Decisión de diseño suya:** monto negativo → **rechazar**, *"porque un monto
  negativo siempre es un accidente"*. Correcta y bien razonada (el modelo traduce
  lo que escribió un humano).
- ✅ **Segunda decisión suya, y la contestó completa: los DOS candados.** ¿Dónde se
  validan los no-números? *"Inicialmente A (la herramienta), pero además en el
  agente, o sea B"*. Es `guardar_reporte` otra vez. Se le añadió el argumento que
  decide el orden: **A se prueba por $0.00 y sin red; B necesita llamadas pagadas.**
- ⚠️ **Error suyo, el mismo que él me corrigió a mí en el nivel 1:** el caso
  `"tasa cero"` lo escribió con `monto=-100` (copiado del caso anterior) → **dos
  variables en un caso**. Ese caso habría pasado a verde al arreglar el monto, con
  la tasa cero **todavía rota**. Regla escrita en el archivo: **un caso, una
  variable.** (Lo corrigió solo antes de que lo revisáramos.)
- ⚠️ **No entendió que `doblar` era un ejemplo desechable** y preguntó cómo
  "convertirla" para el ejercicio. → **Al dar un ejemplo con función de mentira,
  decir explícitamente que no va en su archivo.** La técnica sirve (funcionó con
  `poner_apodo`), la advertencia faltaba.

#### Los 3 hallazgos de la corrida

1. **`4.0 == 4` es `True` en Python** — el `==` compara valor, no tipo. El caso
   `"redondeo a COP"` salía **en verde con el defecto puesto**. Se endureció la
   comparación a `(obtenido == esperado) and (type(obtenido) is type(esperado))`
   y pasó a FALLA. → **Una prueba en verde no dice que no haya problema; dice que
   tu comparación no lo ve.** Es *"una corrida limpia no prueba nada"* (nivel 5)
   un piso más abajo. Candidata a lección fuerte del 5b.
2. ⚠️ **PREDICCIÓN MÍA FALLADA:** dije "se esperan 8 FALLA" y salieron **7**,
   justo por lo de arriba. Se le planteó como pregunta antes de correr (*"¿4.0 == 4
   es verdadero?"*) y **la contestó bien**: "hay que preguntar si es entero". Con
   la comparación estricta salieron los 8. La predicción no se borró del archivo:
   se corrigió con la razón.
3. **El `try/except` se ganó el sueldo.** 4 de los 13 casos dan
   `REVENTO: TypeError` (`tasa=None`, `monto=""`, `monto="10"`, `monto=None`).
   Sin el `try`, el eval moría en el caso 5 y **nunca se veían los 8 siguientes**.
   Se anota el reventón **como si fuera un resultado más**, alineado en la tabla:
   reventar *es* un comportamiento. → *"una prueba que se cae con lo que estaba
   probando no es una prueba, es otra víctima"*.

#### El hallazgo conceptual más importante del día

**`convertir()` incumple el contrato que está escrito en su propio archivo**
(*"ninguna lanza excepciones"*). Y la razón de por qué importa, en sus términos:
**un `{"error": ...}` es una conversación; un `TypeError` es un funeral.** Con el
dict el modelo lee el error y reintenta; con la excepción se cae el bucle del
agente y con él la conversación. `monto="10"` no es un caso raro: el modelo manda
**JSON**, donde `10` y `"10"` son cosas distintas.

#### Reorganización de `herramientas.py` (pedida por él: *"que se vea más profesional"*)

Se hizo **y se volvió a correr la misma prueba antes y después** para comprobar que
no cambió comportamiento. Cambios: `import` juntos arriba (PEP 8), constantes en un
solo bloque, separadores de sección, docstrings en las dos funciones, frenos
numerados con su *por qué*, y el comentario que **salva el freno 3** (con el número
278.916). **Lo más valioso no fue código: fue escribir el CONTRATO** del archivo en
el docstring de arriba (*"todas devuelven dict; ninguna lanza excepciones"*). Sus
dos funciones ya lo cumplían, pero en ningún sitio decía que era una regla.
**No se pusieron anotaciones de tipo** a propósito: las conoce en el nivel 6 con
TypeScript, y aquí serían un tema nuevo a mitad de otro.

⚠️ **Regla de método confirmada dos veces hoy: UNA pregunta a la vez.** Tres
preguntas encadenadas no son tres veces más difíciles, son un muro. Cada vez que
se reformuló a una sola pregunta, la contestó bien de inmediato. También pide
**"escríbeme un ejemplo primero"** — dárselo sobre **otra** función funciona.

**Siguiente paso concreto: paso 5 — `evals.py`**, probando las dos funciones que
no tocan internet. **$0.00 y sin red.** Ese es el orden y tiene razón: si
`convertir()` está mal, saberlo antes de pagar llamadas. Buena parte del material
ya existe: en la sesión 11 se probó `guardar_reporte` a mano con 6 casos en un
archivo temporal. **El paso 5 es dejar eso escrito y repetible**, no inventarlo.

### Lo que pasó con `guardar_reporte()` (sesión 11)

- ⚠️ **No entendió las tres preguntas cuando se las hice juntas.** Lo dijo él:
  *"no entendí las preguntas"*. Se reformularon a **una sola**, con analogía del
  portero (lista de prohibidos vs lista de autorizados) y **la contestó bien de
  inmediato**: *"el portero A, porque no conoce al nuevo peligroso"*.
  → **Regla de método para lo que queda del curso: una pregunta a la vez.**
  Tres preguntas encadenadas no son tres veces más difíciles, son un muro.
- También pidió **"escríbeme un ejemplo primero"**. Se le dio el patrón completo
  sobre **otra función** (`poner_apodo`, nada de archivos) para no regalarle la
  suya. Funcionó: copió la estructura, no la respuesta. **Conservar esa técnica.**
- Escribió los 3 frenos. Dos defectos suyos, los dos didácticos:
  1. `{"error". "..."}` con **punto en vez de dos puntos** → `SyntaxError`.
  2. **El mensaje de error mentía:** copió *"solo letras y números"* del ejemplo,
     pero su `PERMITIDOS` también acepta `-`, `_` y `.`. → **el mensaje de error
     es la instrucción de reintento que le das al agente**; si es incompleto,
     reintenta peor de lo que podría. Es L4.9 en espejo (allá era negar en
     silencio, aquí es negar con una explicación equivocada).
- **Corrida real, 6 casos, $0.00:** `reporte-trm-2026-07-30.txt` guardado;
  `../../.env`, `C:/Windows/x.txt`, `reporte.md`, `mi reporte.txt` y `..txt`
  rechazados. En `caja/` quedó un solo archivo.
  - **Hallazgo que no esperaba:** `../../.env` **no lo paró la allowlist**, lo
    paró el freno 1 (no termina en `.txt`). Tres candados apilados y al ladrón lo
    atrapó el que menos parecía de seguridad.
- ✅ **Se midió si el freno 3 sirve, en vez de suponerlo.** Fuerza bruta sobre
  **278.916 nombres** (todos los armables con `PERMITIDOS` + `.txt`): los que
  llevan `..` **y además escapan de `caja/` son 0**. **El freno 3 hoy no bloquea
  nada** — escapar necesita un separador y el freno 2 ya prohíbe `/` y `\`.
  - Se le planteó como decisión consciente: quitarlo (código muerto) o dejarlo
    con comentario (seguro para el día que alguien agregue `/` a `PERMITIDOS`).
    Recomendación dada: **dejarlo con la nota** — un candado sin nota se borra en
    la siguiente limpieza. ⚠️ **Él no había contestado todavía.**
  - → Candidata a lección L5b.x: **no des por bueno un candado sin probar que
    atrapa algo.** Y aquí la prueba se pudo hacer **entera** (278.916 casos, $0.00,
    sin red) porque la herramienta no sabe que Claude existe. Es el argumento más
    fuerte que ha dado el curso a favor de separar `herramientas.py`.

✅ **URLs YA VERIFICADAS el 2026-07-29** (sesión 9), las dos con HTTP 200, y están
copiadas en `05b-proyecto/README.md` §5b.4 con sus campos y la advertencia de la
brecha variable. **No hace falta volver a comprobarlas** si la próxima sesión es
pronto; sí conviene si pasan varios días.

⚠️ **Formato del 5b, decidido por él y con una razón que no hay que perder:
MIXTO.** Lo mecánico se dicta (carpetas, `import`, estructura); lo conceptual lo
escribe él (bucle, frenos, evals): se le dice *qué* y *por qué*, lo intenta, y
después compara con mi versión. **La razón:** si se le dicta todo, termina con un
agente que funciona y que no sabría rehacer — sería el único nivel donde el
código no pasó por su cabeza.

---

**Lo que queda vivo del nivel 5** (todo voluntario, nada bloquea el 5b — igual
que los pendientes de los niveles 2 y 3):

- ⚠️ **Ejercicio 4, el mejor que quedó sin hacer.** Meter `"No olvide"` en el
  detector. Las 4 mezclas reales lo llevaban **todas**, así que un `if` de una
  línea le gana a los dos jueces ($0.00, 100% estable, cero citas fabricadas).
  Es la demostración más limpia de L5.15 que ha dado el curso.
  ⚠️ Si lo retoma: **límites de palabra** (`\bolvide\b`) — `'olvide' in
  "no olvides"` es `True` y `"No olvides"` es tuteo correcto (L5.24).
- ⚠️ **Los 6 scripts con el precio suelto siguen con el bug armado.** Hoy no
  mienten (modelo y precio coinciden), pero mienten el día que se cambie
  `MODELO`: `01/02/03_contar.py`, `04-harness-real/03_harness.py`,
  `02-conversacion/02_ventana.py` y `03_recortar.py`. Se le ofreció arreglarlos
  y prefirió avanzar. → aplicar el patrón `PRECIOS[MODELO]` de L5.23 cuando toque.
- ⚠️ **Él no leyó a mano ninguna de las 8 respuestas** que marcó Sonnet. Las
  analizó un script con reglas mías: comparte **mi** punto ciego, no el del
  modelo. Son 8, es barato.
- ⚠️ **El defecto del TRATAMIENTO (tú/usted) está medido pero sin arreglar.**
  En la v2: 26 tú / 2 usted / 2 mixto. En la v3-A: 6 de 30 `póngase`. **Ni B ni C
  lo arreglaron.** → ejercicio 2.
- ⚠️ **B vs C sigue sin resolverse:** se solapan con N=30. → ejercicio 3.

**Dos dudas viejas cerradas en el nivel 5:** *"¿cómo se prueba algo que nunca
responde igual dos veces?"* (abierta desde el nivel 1) y *"¿por qué aparece el
rioplatense?"* (abierta desde el nivel 3).

**Detalle del nivel 5 (histórico):**

- ✅ **RESUELTO en la sesión 9 (ejercicio 1).** Antes decía: *"los 43 marcados
  por el juez no se revisaron uno por uno"*. El juez de Sonnet redujo la lista a
  **8**, y las 8 se revisaron con código: **4 mezclas reales** (todas con
  `"No olvide"` + `"ponte"`), **3 falsas alarmas** y **1 cita fabricada**.
  Los dos jueces cazaron **las mismas 4** → el conteo real de mezclas en las
  120 respuestas es **4**, no 43 ni 46. Ver §5.6.
- El detalle del defecto del tratamiento (v2: 26 tú / 2 usted / 2 mixto; v3-A:
  6 de 30 `póngase`) y el solape B vs C están en la bitácora de la sesión 8.

**Cómo trabaja este estudiante** (confirmado otra vez en la sesión 8): pide la
explicación **antes** de ejecutar, y después compara sus números con los del
README. Mantener el ritmo: explicar → predecir → correr → comparar → escribir.
**Novedad de esta sesión, que hay que conservar: se le pidió una predicción por
escrito antes de cada corrida.** Funcionó muy bien — acertó el número de
respuestas `mixto` (2 de 30) y falló el del dialecto (dijo 5, salió 9), y las
dos cosas enseñaron. También hace **preguntas conceptuales espontáneas de mucho
nivel** (guardrails, jurado de jueces, evaluación en multi-agente); vale la pena
responderlas bien y anotarlas.

**Cómo trabaja este estudiante** (confirmado en la sesión 6): pide la
explicación **antes** de ejecutar, y después compara sus números con los del
README. De esa comparación es de donde han salido los mejores hallazgos del
curso. Mantener ese ritmo: explicar → correr → comparar → escribir.

---

## Estado de los niveles

| Nivel | Nombre | Material escrito | Estudiante lo completó |
|---|---|---|---|
| 0 | Setup | ✅ | ✅ |
| 1 | Primera llamada | ✅ | ✅ |
| 2 | Conversación con memoria | ✅ | ✅ |
| 3 | Primer agente (clima) | ✅ | ✅ |
| 4 | Harness real | ✅ | ✅ |
| 5 | Evaluación (evals + rúbricas) | ✅ | ✅ |
| 5b | Proyecto integrador (divisas/TRM) | 🔄 README ✅ | 🔄 paso 6/10 |
| 6b | Memoria persistente y Skills | ✅ | ✅ |
| **6c** | **TypeScript** ← **EN CURSO** | 🔄 pasos 0–4b ✅ | 🔄 paso 4b/6 |
| 7 | Producción (incl. observabilidad) | ⬜ | ⬜ |
| 8 | Multi-agente (orquestador + workers) | ⬜ | ⬜ |

> ⚠️ **El orden real en que se hicieron es 5b (a medias) → 6b → 6c.** El 5b quedó
> parado en el paso 6/10 y **nadie ha decidido si se retoma o se da por cerrado**:
> es la única fila de esta tabla con una pregunta abierta.

> ⚠️ **Los niveles 5 y 6 se intercambiaron en la sesión 6.** Antes: 5 = TypeScript,
> 6 = Evaluación. Ahora: **5 = Evaluación, 6 = TypeScript**. Las entradas de la
> bitácora anteriores a la sesión 6 usan la numeración vieja — cuando digan
> "nivel 6" refiriéndose a evaluación, hoy es el **nivel 5**.

Leyenda: ⬜ pendiente · 🔄 en curso · ✅ hecho

---

## Bitácora de sesiones

### Sesión 1 — 2026-07-28
- Definimos el plan: 9 niveles, Python primero, TypeScript desde el nivel 5.
- Escribí el material de los niveles 0 y 1.
- Creé `CLAUDE.md` y este archivo para que la memoria sobreviva entre sesiones.
- **Verificado:** los 4 scripts compilan sin errores de sintaxis.
- **NO verificado:** ningún script se ha ejecutado de verdad todavía — falta la API key.
- Pendiente del estudiante: hacer el nivel 0.

### Sesión 2 — 2026-07-28
- **Nivel 0 COMPLETADO.** Creamos `.venv` en la raíz e instalamos `anthropic 0.120.0`
  y `python-dotenv`. El estudiante consiguió su API key y la guardó en `.env`.
- `verificar.py` corrió de verdad: `TODO LISTO`, con llamada real a la API
  (17 tokens entrada / 5 salida). **Primera ejecución real del curso.**
- Duda resuelta: diferencia entre **suscripción** (Claude Pro/Code, mensualidad, para
  que Claude te ayude) y **créditos de API** (pago por token, lo que consumen tus
  propios programas). Son facturas separadas.
- Explicamos `verificar.py` línea por línea. El estudiante pidió dejar registro.
- **Creamos `LESSONS.md` y `GUIDE.md`** (separados a propósito: el *por qué* vs el
  *cómo*). Nivel 0 documentado con 9 lecciones (L0.1–L0.9).
- Actualizamos `CLAUDE.md` con las reglas de mantenimiento de esos archivos.
- **Nivel 1 COMPLETADO.** Corrió los 3 scripts y los 3 ejercicios.
- Hallazgos propios del estudiante (16 lecciones, L1.1–L1.16). Los mejores:
  - Con `max_tokens=30`, Opus 5 devolvió **solo un bloque `thinking`** y cero texto.
    `content[0].text` habría reventado. L0.7 comprobada en su máquina.
  - Cambiar solo el `SYSTEM` (profesor → pirata) **cuadruplicó la factura**.
  - El script `03_costo.py` **imprimía "Haiku cuesta 5x menos"** — la medición real
    dio **55x**. Corregimos el script para que calcule la razón en vez de fijarla.
  - Detectó que la fila de Sonnet no estaba cortada por el modelo sino por
    `texto.strip()[:30]` del propio script. Arreglado con `" ".join(texto.split())`.
- **El estudiante corrigió un análisis mío**: avisó que había añadido la regla
  "máx 4 frases" antes del ejercicio 3, así que el experimento tenía 3 variables,
  no 1. Reescribimos L1.10 y L1.11.
- Costo total del nivel: menos de $0.05 USD.

### Sesión 3 — 2026-07-28
- **Pendiente de la sesión 2 resuelto:** corrimos `03_costo.py` ya corregido.
  La tabla sale entera (la fila de Sonnet ya no rompe el formato) y la razón se
  calcula de verdad. **Pero dio 30.9x, no 55x** como la vez pasada. Mismo script,
  mismo precio por token: lo único que cambió fue cuánto razonó Opus esa corrida.
  → El costo tampoco es determinista. Corregimos `GUIDE.md`, que afirmaba "55x"
  como si fuera un dato fijo.
- **Nivel 2 escrito y verificado** (`02-conversacion/`): README + 3 scripts.
  - `01_chat.py` — bucle de chat con historial. Interactivo, **no ejecutado**
    (lo corre el estudiante). Usa Haiku a propósito: en un bucle se reenvía todo.
  - `02_ventana.py` — **ejecutado.** 6 preguntas cortas: la entrada pasó de
    43 a 469 tokens (11x) sin que las preguntas crecieran. Costo: $0.0038.
  - `03_recortar.py` — **ejecutado.** Compara historial completo (418 tok) vs
    ventana deslizante (127 tok) vs resumen+recientes (308 tok).
- **Error mío detectado y corregido antes de entregar:** la primera versión de
  `03_recortar.py` probaba el olvido preguntando "¿qué es una variable?". Las
  tres estrategias respondieron bien —el modelo ya sabe qué es una variable—,
  así que la prueba no demostraba nada, pero el texto afirmaba que sí. Era L1.13
  otra vez. Lo cambié por un dato inventado (el nombre "Marta" y su taller de
  bicicletas) que solo existe en el turno 1. Ahora la ventana deslizante
  responde *"No tengo esa información"* y la demostración es real.
- **Segundo texto falso corregido:** el cierre decía que el resumen cuesta
  "casi lo mismo que la ventana". La medición dice 308 vs 127 tokens (2.4x más).
  Reescrito para explicar por qué: con 8 turnos el resumen no gana; gana con 80,
  porque su tamaño se mantiene fijo mientras el historial crece.
- `GUIDE.md` ampliado: `count_tokens` (§5.b) y tabla de ventanas de contexto (§5.c).
- **El estudiante corrió `01_chat.py`.** 5 turnos: entrada 61 → 808 tok (13x).
  Verificamos con su propia tabla que `entrada(n) = entrada(n-1) + salida(n-1)
  + su mensaje`; cuadra en los 4 saltos. Hallazgo suyo del análisis: **el
  historial crece sobre todo por lo que responde Claude (~200 tok/turno), no
  por lo que escribe el usuario (~25 tok/turno).**
- **BUG encontrado por el estudiante en `01_chat.py`:** el contador imprimía
  `len(historial) // 2`, que asume 2 mensajes por turno. Al hacer el ejercicio 1
  entra 1 por turno y el contador salió `0, 1, 1, 2`. Arreglado con una variable
  `turno` propia. **Regla:** no deduzcas un dato de la forma de una estructura
  que puede cambiar.
- **Comentario mío falso, corregido en el código:** decía que sin guardar el
  turno `assistant` "cada turno empieza de cero". Falso. Los mensajes del
  usuario siguen entrando, así que Claude **recuerda los datos y olvida el
  diálogo**: contestó bien "vives en Sabaneta, estás en Bucaramanga", pero
  saludó "¡Hola Juan!" 4 veces y repitió la misma recomendación 3 veces.
- Ejercicio 1 completado. Entrada con memoria completa vs sin respuestas:
  570 vs 116 tokens en el turno 4 (~5x más barato, y coherencia destruida).
- **`02-conversacion/README.md` actualizado** con todo lo anterior: nueva sección
  **2.1b** (tabla de la corrida real, la fórmula verificada con restas, el
  resultado del ejercicio 1, y el bug del contador). Ejercicio 1 marcado como
  hecho. Nuevo ejercicio 6: medir la "cuarta estrategia".
- **El estudiante corrió `02_ventana.py`.** Entrada 43 → 511; total 1.669 tok,
  $0.0041. Tres hallazgos al comparar sus números con los míos:
  1. **El turno 1 dio 43 en las dos corridas.** La entrada es determinista
     (system + pregunta ya existen); lo que varía es la salida.
  2. **Medimos el defecto que yo había confesado.** Restando
     `entrada − (entrada previa + salida previa)` en ambas corridas, las
     preguntas pesan 10, 14, 10, 11, 12 tokens — **idéntico en las dos**.
     El historial aporta ~90/turno, o sea 7x más. El defecto era real pero
     irrelevante, y ahora está medido en vez de supuesto.
  3. **Amplificación de la salida:** 27 tokens de salida de más costaron 145
     tokens de entrada de más (~5x). Un token generado en el turno 1 se
     reenvía 5 veces. → Pedir respuestas cortas en el SYSTEM ahorra en todos
     los turnos siguientes, no solo en uno.
- **Cuarto texto falso mío, corregido:** `02_ventana.py` afirmaba que la entrada
  "crece como una escalera cada vez más alta". Los incrementos reales son
  planos (99, 101, 81, 82, 105) porque el SYSTEM limita a 2 frases. Yo había
  generalizado desde `01_chat.py`, que no tiene ese límite y ahí sí aceleraban
  (124, 177, 208, 238). **El escalón mide lo que mida la respuesta anterior.**
  Corregido en el script y explicado en el README con la comparación de ambos.
- **El estudiante corrió `03_recortar.py`.** Resultados: completo 418, ventana
  127, resumen 293 (el mío dio 308).
  1. **Confirmada la determinismo por tercera vez:** las estrategias 1 y 2
     coinciden AL TOKEN entre corridas (texto preexistente); solo la 3 varía,
     porque el resumen lo genera el modelo. Ya es una propiedad, no casualidad.
  2. **Mejor evidencia que la mía:** su ventana deslizante respondió *"solo me
     has preguntado sobre errores de sintaxis y cómo leer mensajes de error"* —
     que es EXACTAMENTE el contenido de los últimos 4 mensajes. El modelo
     recita su propia ventana. No alucina: describe la lista que recibió.
- **Cerrado el hueco de honestidad que yo mismo había señalado:** la tabla
  comparaba tokens pero no incluía el costo de GENERAR el resumen. En vez de
  estimarlo, modifiqué `03_recortar.py` para medirlo. Resultado: resumen
  $0.001077, ahorro $0.000117/turno → **se paga solo a los ~9 turnos**.
  Generar el resumen cuesta 9x lo que ahorra en un turno. Convierte "resumir
  ahorra" en "¿cuánto va a durar esta conversación?".
- **El estudiante preguntó "¿cómo se prueba gratis?"** Yo había escrito "es
  gratis" en 3 sitios **sin verificarlo** — salía de mi memoria. Lo comprobé en
  `platform.claude.com/docs/.../token-counting`. Era cierto, pero aparecieron
  dos letras pequeñas que yo ignoraba y que ahora están en `GUIDE.md` §5.b y en
  el README del nivel:
  1. **Es un estimado**, no exacto: el conteo real "puede diferir en una
     cantidad pequeña".
  2. **Gratis ≠ ilimitado:** 2.000 peticiones/minuto en el nivel inicial, con
     límite propio e independiente del de `messages.create`.
  Lección de método: *verificar también lo que resultó ser verdad* — la
  comprobación trajo dos matices que la afirmación correcta escondía.
- **NIVEL 2 CERRADO.** 14 lecciones escritas en `LESSONS.md` (L2.1–L2.14).
  Costo total del nivel: menos de $0.03 USD entre todas las corridas.
  Ejercicios hechos: el 1 (y de él salieron un bug y una cuarta estrategia).
  Pendientes voluntarios si quiere retomarlos algún día: ejercicios 2, 3, 4, 5, 6.
  El 4 (romper el prompt del resumen) y el 6 (medir la cuarta estrategia) son
  los que más enseñan.
- **Auditoría pedida por el estudiante** ("revisa que todo esté actualizado").
  Aparecieron 3 huecos que yo había dado por cerrados:
  1. La frase falsa de la "escalera cada vez más alta" **seguía viva** en la
     sección *Lo que ya sabes* del README. La corregí en el script y en el
     cuerpo del README, pero no en el resumen. → **Al corregir una afirmación,
     buscarla en TODOS los archivos, no solo donde la viste.**
  2. La tabla de §2.2 decía "lo que se midió de verdad" sin aclarar que era una
     de dos corridas. Etiquetada como *corrida A*.
  3. `GUIDE.md` decía solo "la salida cuesta ~5x más que la entrada", sin el
     segundo multiplicador (la salida se recobra como entrada en cada turno
     siguiente). Agregado.
- **Recaída mía en el mismo error, atajada en el momento:** metí una fila con
  "~180 tokens" para la cuarta estrategia dentro de la tabla titulada
  *"Resultados reales de la corrida"*. Nadie la midió: me la inventé. La quité y
  la convertí en el ejercicio 6, para que el número salga de una medición.
  Tercera vez en la sesión que aparece el mismo patrón (ver L1.13).

### Sesión 4 — 2026-07-28
- **Nivel 3 escrito y verificado** (`03-primer-agente/`): README + 3 scripts.
  Los **tres se ejecutaron de verdad**, no solo compilan.
  - `01_pedir_herramienta.py` — **ejecutado.** Define una herramienta que *no
    existe* como función, y aun así funciona: `stop_reason=tool_use`, un bloque
    `type=tool_use` con `id=toolu_01WQq8...`, `name=obtener_clima`,
    `input={"ciudad": "Bogota"}`. El modelo extrajo "Bogota" de la frase solo.
    - **El estudiante lo corrió y le salió DISTINTO:** 2 bloques
      (`thinking` + `tool_use`) donde a mí me salió 1 (solo `tool_use`). Mismo
      script, mismo modelo. Opus 5 decide por llamada si razona. → No solo el
      texto es no determinista: **la estructura de `content` también lo es**.
      Es la mejor prueba posible de L0.7: `content[0].name` habría funcionado
      en mi máquina y reventado en la suya. README corregido: la salida ya no
      se presenta como un hecho fijo, sino como corrida A vs corrida B.
  - `02_bucle.py` — **ejecutado.** Bucle agéntico completo con clima falso
    (diccionario). Medellín: vuelta 1 `tool_use` (452 in / 73 out) → vuelta 2
    `end_turn` (543 in / 82 out). **Una pregunta = 2 llamadas.**
    - **El estudiante lo corrió.** Comparando sus números con los míos salieron
      cuatro cosas, todas medidas:
      1. **Las 3 entradas de vuelta 1 coincidieron AL TOKEN** (452, 458, 452)
         entre dos corridas distintas. El menú de `tools` es texto fijo.
      2. **La única divergencia se propagó exacta:** Bogotá dio 102 vs 106 de
         salida en v1, y la entrada de v2 dio 580 vs 584. Los mismos 4 tokens.
         Confirma la fórmula del nivel 2 con herramientas:
         `entrada(v2) = entrada(v1) + salida(v1) + tool_result`.
      3. **El peso del `tool_result` es determinista** y dio idéntico en ambas
         corridas: 18 tokens (Medellín), 20 (Bogotá), **46 (el mensaje de error
         de Tokio)**. Lógico: ese texto lo escribe la función, no el modelo.
         → Lo que devuelve una herramienta se reenvía en cada vuelta siguiente.
         Un JSON gigante sale caro para siempre. Recortar salidas de
         herramientas es harness, igual que recortar historial.
      4. **Costo:** 3 preguntas ≈ $0,030 (3.062 in / 590 out). En el nivel 2,
         6 preguntas costaron $0,0041 → **7x más caro con la mitad de
         preguntas**, por dos multiplicadores apilados: Opus vs Haiku, y dos
         llamadas por pregunta en vez de una.
    - **Hallazgo que no es de tokens:** las respuestas salieron en español
      rioplatense ("Querés", "llevá paraguas", "campera") y el estudiante es
      colombiano. Este script no tiene `SYSTEM`. **Sin ancla de voz, el modelo
      elige una** — bug visible para el usuario que ninguna prueba automática
      detecta. Anotado en el README; el script 3 sí tiene `SYSTEM` para comparar.
  - `03_agente_real.py` — **ejecutado.** Clima real vía Open-Meteo (gratis, sin
    llave, por `urllib`) + una segunda herramienta `hora_utc`.
- **Las 4 predicciones del script 3 se cumplieron todas** en la corrida real:
  "¿qué hora es?" → solo `hora_utc`; "clima en Bucaramanga" → solo
  `obtener_clima` (26.4 C, parcialmente nublado — dato que el modelo no podía
  tener); "compara Bogotá y Cartagena" → **`obtener_clima` dos veces en la MISMA
  vuelta** (dos bloques `tool_use` en un turno); "17 por 23" → **ninguna
  herramienta**, `end_turn` en la vuelta 1. Nadie programó esas decisiones: solo
  existen las `description`.
- **Error real encontrado al ejecutar `02_bucle.py`:** `UnicodeEncodeError:
  'charmap' codec`. El agente había funcionado perfecto — lo que reventó fue el
  `print`, porque la consola de Windows es `cp1252` y Claude respondió con `°` y
  emojis. Arreglado con `sys.stdout.reconfigure(encoding="utf-8")` en los tres
  scripts. **El traceback apuntaba a `print`, no a la API.** Documentado en
  `GUIDE.md` §3 y en el README del nivel.
- `GUIDE.md` ampliado: 3 filas nuevas en la tabla de errores (encoding,
  `tool_use_id` que no coincide, guardar solo el texto en vez de
  `respuesta.content`) y una sección **§4.b — plantilla del bucle agéntico**
  con las 4 reglas que rompen el programa si se ignoran.
- **Decisión de diseño del nivel:** bucle **manual**, no el `tool_runner` del
  SDK. El SDK tiene un helper que hace todo esto solo, pero esconde justo lo que
  hay que entender. El `tool_runner` se puede mencionar en el nivel 4, ya con el
  bucle entendido a mano.
- Costo de escribir y verificar el nivel: unos pocos centavos.
- **El estudiante corrió los 3 scripts y los ejercicios 1 y 2.** Hallazgos suyos
  al comparar sus números con los míos, además de los ya anotados arriba:
  - **Las 4 entradas de vuelta 1 de `03_agente_real.py` coincidieron al token**
    (598, 610, 612, 605). Cuarta confirmación de que la entrada es determinista.
  - **Con API real el costo deja de ser determinista.** Bucaramanga dio 709 vs
    714 de entrada en v2 con la MISMA salida de v1 (59). La diferencia de 5
    tokens la puso el cielo: `nublado` vs `parcialmente nublado`. En el script 2,
    con diccionario fijo, el peso del `tool_result` era idéntico entre corridas.
  - **El menú de `tools` es una suscripción fija:** "¿cuánto es 17 por 23?" no
    usó ninguna herramienta y pagó 605 tokens de entrada. La pregunta pesa ~10;
    el resto es `SYSTEM` + las 2 descripciones, que viajan siempre.
  - Las 4 predicciones del script 3 se cumplieron en su corrida también,
    incluidas las dos peticiones en la misma vuelta.
- **Predicción MÍA que falló, y era mi error de diseño:** le dije que mirara si
  el `SYSTEM` arreglaba el dialecto rioplatense. No lo arregló — el `SYSTEM`
  decía *"Responde en espanol"*, que **no especifica cuál español**. Le pedí un
  idioma, no una variedad. Y apareció en **1 de 4** respuestas: un defecto
  intermitente, que no se detecta probando una vez. Convertido en ejercicio 7
  (con nota de que una corrida limpia no prueba nada → guiño al nivel 6).
- **NIVEL 3 CERRADO.** 16 lecciones escritas en `LESSONS.md` (L3.1–L3.16).
  Ejercicios hechos: 1 y 2 (los dos de sabotaje). Pendientes voluntarios: 3, 4,
  5, 6, 7, 8. El 7 (anclar el dialecto y medirlo en varias corridas) y el 8
  (medir el costo del menú con `tools=[]`) son los que más enseñan.
  Costo total del nivel para el estudiante: unos $0,06.

### Sesión 5 — 2026-07-28
- **Nivel 4 escrito y verificado** (`04-harness-real/`): README + 4 scripts.
  Los **cuatro se ejecutaron de verdad**, con sus números en el README.
  - `01_errores.py` — **ejecutado.** Provoca 5 fallas: 401, 404, `ValueError`,
    400 y `APIConnectionError`. Cuesta $0.00 (ninguna genera tokens).
    - **Sorpresa mía al escribirlo:** puse `max_tokens=99_999_999` esperando un
      400 del servidor y salió un **`ValueError` de Python**. El SDK calcula que
      la respuesta tardaría más de 10 minutos y **se niega a mandar la petición**.
      Nunca hubo red. Agregué un quinto caso (`temperature=0.5`, que Opus 5 ya
      no acepta) para tener también un 400 real y poder comparar los dos.
    - De ahí salió **L4.2: un error puede morir en tres sitios** — tu máquina,
      la red, o el servidor. "Falló la API" son tres diagnósticos distintos.
  - `02_reintentos.py` — **ejecutado.** Cuatro mediciones con cronómetro:
    1. Mismo error de red, subiendo `max_retries`: **0.22s / 0.39s / 1.34s /
       3.39s** para 0, 1, 2 y 3 reintentos. El error es idéntico; lo que crece
       es el tiempo, y **el SDK reintenta en silencio**.
    2. `max_retries=5` con llave mala: **0.39s**. No reintentó ni una vez. El
       SDK ya sabe que un 401 es permanente.
    3. `timeout=1s` con 0 reintentos: **1.00s**. Con 2 reintentos: **4.20s**.
       El timeout es **por intento**. Con los valores de fábrica (10 min, 2
       reintentos) el peor caso es **media hora colgado**.
    4. Reintento propio con espera exponencial + jitter, sobre una llamada real.
    - **Hallazgo retroactivo importante:** `max_retries=2` es el valor de
      fábrica, así que **todos los scripts de los niveles 1, 2 y 3 podían hacer
      hasta 3 peticiones por cada `create()`**. Nunca se notó porque nunca falló
      nada. → L4.4.
  - `03_harness.py` — **ejecutado dos veces** (concediendo y negando el permiso).
    El agente del clima con las 6 piezas: timeout, errores tipados, presupuesto
    en dólares, tope de vueltas, permisos y registro JSONL.
    Nueva herramienta peligrosa `borrar_archivo`, que borra de verdad dentro de
    una carpeta `caja/` que el script crea con dos archivos de mentira.
    - Corrida completa: **$0.0319** de un tope de $0.10, 3 preguntas, 6 llamadas.
    - **Con permiso:** borró y contestó *"Listo, ya borré borrador.txt"*.
    - **Sin permiso:** el archivo siguió ahí y contestó *"No pude borrarlo: el
      sistema negó el permiso"*. Funcionó porque le devolvemos un `tool_result`
      que dice `PERMISO DENEGADO`. → L4.9: negar en silencio haría que el
      agente dijera "ya lo borré" con el archivo intacto.
  - `04_streaming.py` — **ejecutado.** Primera palabra a los **11.9s** sin
    streaming vs **8.6s** con streaming. Anotado en el README que es **una sola
    corrida y las dos respuestas no midieron lo mismo** (la de streaming salió
    de 787 tokens, por eso su total es mayor): lo único comparable ahí es
    cuándo aparece la primera palabra.
- **Predicción del nivel 3 que se cayó (mía):** en L3.15 concluí que el
  rioplatense aparecía porque el `SYSTEM` decía solo *"Responde en espanol"*,
  sin especificar la variedad. En el harness el `SYSTEM` dice **"español de
  Colombia"** y aun así salió *"Si querés, autorizá"* en **1 de 3** respuestas.
  La explicación del nivel 3 era razonable y encajaba con los datos, pero era
  **incompleta**. Escrito como L4.13: una hipótesis no está confirmada hasta
  que arreglas la causa y el defecto desaparece. Medirlo en serio es nivel 6.
- `GUIDE.md` ampliado: 4 filas nuevas en la tabla de errores (el `ValueError` de
  streaming, `temperature` deprecado, el timeout multiplicado, los reintentos
  anidados) y dos secciones nuevas: **§4.c — los seis frenos del harness** y
  **§4.d — streaming**.
- `LESSONS.md`: 13 lecciones nuevas (L4.1–L4.13).
- **Decisión de diseño:** el permiso se pide **fuera** de la herramienta, en el
  harness. La función `borrar_archivo()` solo obedece; quien decide es el
  diccionario `PERMISOS` y, si toca, el humano. Además la herramienta se
  defiende sola (solo borra dentro de `caja/`): dos candados, porque el permiso
  lo puede dar un humano distraído.
- Costo de escribir y verificar el nivel: unos $0.08 en total.

### Sesión 6 — 2026-07-28
- **El estudiante corrió `01_errores.py`.** Las 5 clasificaciones salieron
  **idénticas** a las mías.
  - **Primera cosa determinista del curso**, y tiene explicación: en este script
    el modelo nunca genera nada, las 5 peticiones mueren antes. Lo no
    determinista siempre fue *la generación*, no la infraestructura. → Es lo que
    hace posible el nivel 5: el harness sí se puede probar de forma repetible.
    Lo único que cambia entre corridas es el `request_id`.
  - El caso 5 mostró la causa envuelta: `causa: ConnectError`. `APIConnectionError`
    es una etiqueta de Anthropic encima de un error de `httpx`.
- **Defecto mío encontrado al leer la salida, y arreglado antes de seguir:**
  el script imprimía `e.message[:80]`, y el corte caía **a mitad del JSON crudo**,
  justo antes del mensaje útil. Los casos 1 y 2 eran ilegibles. Es el mismo
  patrón de `texto.strip()[:30]` del nivel 1: **el script mutila el dato y luego
  parece culpa del servidor.**
  - Arreglo: función `motivo(e)` que entra a `e.body` (el JSON ya parseado que
    el SDK te da) y saca `body["error"]["message"]`. Verificado ejecutando, no
    supuesto.
  - **Regalo inesperado:** ahí venía también el `request_id`, el número que se
    le da a soporte de Anthropic para que encuentren tu petición. Estaba desde
    siempre, escondido detrás del corte.
- **Hallazgo nuevo al poder leer los mensajes:** son de calidad muy desigual.
  El 404 dice solo `model: claude-opus-9-mil` (repite lo que mandaste, no ayuda);
  el 400 dice `` `temperature` is deprecated for this model `` (te dice qué hacer).
  → **Clasificar por clase de excepción, nunca por el texto del mensaje.** El
  texto lo cambia el proveedor sin avisar; la clase no.
- `04-harness-real/README.md` §4.1 actualizado con todo lo anterior.
- **El estudiante corrió `02_reintentos.py`.** Sus tiempos: A 0.31/0.50/1.34/3.00,
  B 0.41, C 1.02 y 4.36. Los míos: A 0.22/0.39/1.34/3.39, B 0.39, C 1.00 y 4.20.
  - **Los números no se repiten pero la forma sí.** Su red es más lenta; el orden
    y las proporciones aguantaron enteros. → Un script de tiempos se lee
    comparando filas entre sí, nunca contra un número fijo.
  - El `1.34s` idéntico en A **es casualidad** y lo anoté como tal en el README.
    Importa distinguirlo de las coincidencias al token de los niveles 2 y 3, que
    sí tenían causa mecánica (el texto de entrada era el mismo).
  - **Hallazgo nuevo: la sección C aísla el backoff mejor que la A.** En A el
    tiempo mezcla "lo que tarda el intento en fallar" con "lo que espera el SDK".
    En C cada intento cuesta exactamente 1.00s (lo fija el timeout), así que
    restando sale la espera pura: **4.36 − 3.00 = 1.36s** en su corrida, 1.20s en
    la mía. Casi igual en dos redes distintas, porque es un `sleep` del SDK.
    → Misma técnica de resta del nivel 2. **Lo que no puedes medir directo, lo
    fijas todo lo demás y lo restas.**
  - **Hallazgo nuevo: apareció `APITimeoutError`**, que no salió en el script 1.
    La sección A da `APIConnectionError` y la C da `APITimeoutError` — y las dos
    se reintentan porque **una hereda de la otra**. Es la contraparte de la
    lección del orden de los `except`: ahí se ve para qué sirve el caso general.
  - B confirmado por comparación: 0.41s con `max_retries=5` es el mismo orden que
    `max_retries=0` (0.31s), no el de 3 reintentos (3.00s). **Un número solo
    significa algo al lado de otro número.**
  - D: 37 in / 47 out ≈ $0.0013, sin reintentos (la llamada funcionó). La
    respuesta salió en español neutro, sin rioplatense — pero **n=1, no prueba
    nada** sobre el defecto del dialecto (L4.13).
  - `README.md` §4.2 actualizado: tablas con las dos corridas, la resta del
    backoff, y la sección de la herencia de excepciones.
- **Candidatas a lección, para cuando se cierre el nivel 4** (irían como L4.14 en
  adelante; el material ya está en esta bitácora y en el README del nivel):
  1. **La infraestructura sí es determinista, aunque el modelo no.** Es la base
     de que el nivel 5 sea posible: se puede probar el harness de forma repetible
     aunque no se pueda probar la generación.
  2. **Clasificar por clase de excepción, nunca por el texto del mensaje.** Los
     mensajes son de calidad desigual (comparar el 404 con el 400) y el proveedor
     los cambia sin avisar.
  3. **Antes de recortar un error, mira si el SDK ya te lo dio parseado**
     (`e.body`). Y de ahí salió gratis el `request_id`.
  4. **Un número solo significa algo al lado de otro número.** Los tiempos no se
     reproducen entre máquinas; la forma sí. Y hay que saber cuándo una
     coincidencia es mecánica y cuándo es casualidad.
  5. **Lo que no puedes medir directo: fija todo lo demás y réstalo.** La espera
     del SDK salió de `4.36 − 3.00`. Misma técnica que el nivel 2.
  6. **El caso general del `except` atrapa hijos que no sabías que existían**
     (`APITimeoutError` hereda de `APIConnectionError`).

### Sesión 7 — 2026-07-29
**NIVEL 4 CERRADO, sin cabos sueltos.** Se corrieron los 2 scripts que faltaban
**y los 2 ejercicios abiertos (8 y 9)**. Las dos hipótesis pendientes quedaron
medidas.

- **`03_harness.py`, dos corridas** (concediendo y negando). Totales $0.0323 y
  $0.0328 contra mis $0.0319. Con `s` el archivo desapareció; con `n`
  `borrador.txt` seguía ahí y el agente dijo la verdad.
- **Se leyó `registro.jsonl` con él**, que era el objetivo pedagógico del paso.
  Cuatro hallazgos, todos de comparar los dos registros:
  1. **Negar cuesta más que conceder.** v2 de la pregunta del borrado: 823/35
     con `s` contra 838/54 con `n`. Los **dos** lados suben: el texto
     `PERMISO DENEGADO` pesa 15 tokens más y el agente gasta 19 más
     explicándose. La cuenta cuadró exacta (15×$5/M + 19×$25/M = $0.00055) y de
     paso **confirmó el precio de Opus 5 con aritmética propia: $5/M in,
     $25/M out.** → L4.20.
  2. Entradas de vuelta 1 idénticas al token en las dos corridas (724, 735, 736)
     y la única divergencia propagada exacta (93/94 out → 934/935 in).
     Séptima confirmación.
  3. **El harness no tiene memoria entre preguntas** — no se había dicho nunca.
     Las tres vueltas 1 arrancan en ~730, no acumulan. Explica por qué el costo
     por pregunta es plano, al revés que en el nivel 2.
  4. **El hallazgo que solo existe en el registro:** 47 s entre `llamada_api`
     (3.98 s) y `herramienta`. Los otros 43 fueron **el humano** decidiendo el
     permiso. Ninguna de las otras cinco piezas del harness puede decir eso.
     Primera vez que la observabilidad responde algo que nada más responde.
     → L4.21, y es el anticipo directo del nivel 7.
- **`04_streaming.py` corrido.** Primera palabra a los **13.2 s** sin streaming
  contra **5.8 s** con streaming (2.3x de adelanto; el mío fue 1.38x). Números
  distintos, dirección idéntica.
  - **Los totales no eran comparables** (691 vs 814 tokens de salida) y se
    normalizaron a **52.3 vs 58.6 tokens/segundo**: con streaming se generó
    *más* texto por segundo. Sin normalizar, la conclusión se invierte. → L4.22.
  - **Hipótesis nueva, escrita COMO hipótesis:** los 5.8 s de silencio con
    streaming podrían ser un bloque `thinking`, porque `text_stream` entrega
    solo texto. Si es cierto, streaming **reduce** la espera en blanco, no la
    elimina. **Sin verificar** → ejercicio 8 (iterar los eventos crudos).
  - **Sesgo de orden que sigue sin medir:** la forma sin streaming corre primera
    y paga la apertura de la conexión. → ejercicio 9 (invertir el orden).
  - **El dialecto NO apareció aquí** (0 de 2, usted colombiano limpio). Y hay
    una diferencia de diseño: en este script el "español de Colombia" va en el
    **mensaje del usuario**, no en el `SYSTEM`. → **hipótesis nueva para el
    nivel 5**, con n=2 no prueba nada pero es medible.
  - El emoji 🕐 se imprimió sin reventar: `sys.stdout.reconfigure` del nivel 3
    trabajando en silencio.
- **Defecto mío corregido:** el docstring de `04_streaming.py` decía
  `Cuesta ~$0.02`. El costo real medido fue **$0.038**, casi el doble. Era un
  estimado mío sin medir — mismo patrón del "5x" del nivel 1. Corregido con el
  número medido y con la nota de que antes decía otra cosa.
- **`03_harness.py` NO se volvió a explicar** (ya estaba explicado en la sesión
  6). Se pasó directo a correr, como decía este archivo. Funcionó bien.
- **El dialecto, tercera y cuarta observación:** 1 de 3 en las dos corridas del
  harness, **pero en respuestas distintas** (con `s` en la 2ª, con `n` en la 1ª).
  El defecto es intermitente **y se mueve de sitio**. → L4.23.
- **Archivos actualizados:** `04-harness-real/README.md` (§4.3 con las dos
  corridas y el desglose del registro; §4.4 reescrita entera con las dos
  máquinas, la normalización, las dos hipótesis y el costo real; ejercicios 8 y
  9 nuevos), `04_streaming.py` (docstring), `LESSONS.md` (**L4.14–L4.23**, 10
  lecciones: las 6 candidatas de la sesión 6 más 4 de esta), `GUIDE.md` (§6 del
  registro: anotar siempre la hora + cómo leer el `.jsonl`; §4.d de streaming:
  `text_stream` solo da texto, y las dos trampas al medir tiempos).
- **EJERCICIO 9 HECHO — lo modificó él y salió el mejor resultado del nivel.**
  Invirtió el orden de `04_streaming.py` (streaming primero). Eso da cuatro
  datos: dos formas × dos posiciones.

  | | primera | segunda |
  |---|---|---|
  | sin streaming | 13.2 s | 12.3 s |
  | con streaming | 7.1 s | 5.8 s |

  1. **Por filas sale el sesgo:** +0.9 s y +1.3 s de castigo por ir primero.
     **Dos mediciones independientes del mismo fenómeno, casi idénticas** →
     abrir la conexión cuesta ~1 s. (Mi predicción antes de correr era "unos
     cientos de milisegundos": me quedé corto al doble.)
  2. **Por columnas sale el efecto limpio:** 6.1 s y 6.5 s. **La ventaja real
     del streaming es ~6.3 s, no los 7.4 s medidos con el experimento sesgado.**
     El control no tumbó la conclusión: **la corrigió, un ~15%.**
  3. → **L4.24**, y la técnica generalizable: cuando la posición contamina una
     medición, corre las dos cosas en las dos posiciones y lee filas y columnas.
- **CORRECCIÓN MÍA, encontrada por esta corrida.** En §4.4 yo había escrito
  *"con streaming se genera más texto por segundo"* con los datos de una sola
  corrida (52.3 vs 58.6 tok/s). La corrida invertida dio **56.6 vs 52.8 — al
  revés**. Las cuatro llamadas caen entre 52 y 59 tok/s: **era ruido y yo le
  puse dirección.** Es L1.13 disfrazada de aritmética: normalizar arregló que
  las magnitudes fueran comparables, pero **no arregla que n=1**. Corregido en
  el README y en L4.22, que ahora tiene las dos mitades.
- **El dialecto sigue limpio: 0 de 4** en el script de streaming. Y no solo
  evita el rioplatense — elige léxico colombiano: *"un **tinto**"*, *"la
  **plata**"*, *"el **freno de mano**"*. Marcador actualizado: `SYSTEM` 3 de 9,
  turno del usuario 0 de 4. Sigue sin probar nada (prompts distintos), pero
  aguantó otra corrida.
- **EJERCICIO 8 HECHO.** Escribió `04b_eventos.py` (archivo nuevo, no toca el
  script original) que itera el stream **crudo** con cronómetro.
  - **Defecto mío en el código que le dicté, atrapado antes de correr:**
    `messages.stream()` no es el stream pelado — es un ayudante que además de
    los eventos de la API emite **los suyos propios, uno por pedazo**
    (`text_stream` está hecho con esos). Mi rama `else` los imprimía: ~800
    líneas de ruido tapando los 4 renglones que importaban. Arreglado
    contándolos con prefijo `sdk:` en vez de imprimirlos. **Mismo patrón del
    `[:80]`, en espejo: allá el print escondía el dato cortándolo, aquí lo
    habría ahogado.**
  - **Hipótesis CONFIRMADA en el mecanismo:** `thinking` a los 1.97 s, cierra a
    las 4.22 s, `text` empieza a las 4.23 s. `content` final = `['thinking',
    'text']`. `text_stream` no podía dar nada antes porque **no existía texto**.
  - **Pero INCOMPLETA, y ese es el hallazgo:** `message_start` no llegó hasta
    los **1.95 s**. El silencio son dos tramos — 1.95 s de "nada todavía" y
    2.28 s de thinking. **El thinking es la mitad.** → L4.25.
  - **El ~1 s de apertura de conexión del ejercicio 9 vive dentro de esos
    1.95 s.** El número de un experimento apareció dentro de otro.
  - **Explica la variación que nunca entendimos:** "primera palabra" dio 8.6,
    5.8, 7.1 y 4.23 s. **El silencio dura lo que dure el razonamiento de esa
    corrida**, y eso no es determinista (L3.14). Esta corrida pensó poco (el
    resumen es una sola frase) y por eso arrancó a los 4.23 s. No fue la red.
  - **Costo invisible:** 654 tokens de salida para ~200 palabras (~350 tokens).
    Unos **300 fueron razonamiento facturado**. Y las corridas anteriores lo
    pagaban igual (691, 814, 802, 696) con `display` en `"omitted"`. **El
    parámetro decide si te lo enseñan, no si ocurre ni si se cobra.** → L4.26.
  - Detalles nuevos: 1.8 s entre que el bloque `thinking` se anuncia y llega su
    primer pedazo (hay huecos reales aun con el stream crudo), y apareció
    `signature_delta` — los bloques `thinking` vienen **firmados** para poder
    verificar que no los modificaste al devolverlos.
- **Métricas nombradas** (lo preguntó él al final, y pidió que quedaran
  registradas para conocerlas): **TTFT** (*Time To First Token*), **TPOT**
  (*Time Per Output Token*), **ITL** (*Inter-Token Latency*) y **latencia
  end-to-end**, más **TTFB** como la métrica de redes que no hay que confundir.
  Quedaron en **dos sitios a propósito**: `GUIDE.md` §4.d como referencia rápida,
  y `04-harness-real/README.md` §4.4 como lección, **con sus propios números al
  lado de cada nombre** (que es como se aprende un término, no como lista suelta).
  Incluye la fórmula `total = TTFT + (tokens × TPOT)` y la advertencia de los
  **dos TTFT** cuando el modelo razona (1.97 s el del sistema, 4.23 s el que ve
  el usuario).
- **Auditoría de cierre pedida por él** ("revisa que todo esté listo"). Aparecieron
  4 huecos, los 4 míos, todos corregidos:
  1. `GUIDE.md` §4.d seguía diciendo *"hipótesis con buena pinta, sin verificar"*
     del thinking — ya estaba medido. **Es la regla de la sesión 3: al cambiar
     una afirmación, buscarla en TODOS los archivos.**
  2. `GUIDE.md` decía "1.4x y 2.3x de adelanto" — números del experimento
     sesgado. Corregido a ~6.3 s con el orden controlado.
  3. La sección *"Lo que ya sabes"* del README del nivel 4 tenía el resumen
     viejo, sin nada de los ejercicios 8 y 9. **Exactamente el hueco de la
     auditoría de la sesión 3, repetido.**
  4. **L4.23 había quedado escrita DESPUÉS de L4.26** (yo inserté las nuevas en
     el sitio equivocado). Reordenado.
  - También: la cabecera de este archivo decía "10 lecciones (L4.14–L4.23)"
    cuando ya son 13 (L4.14–L4.26). Y L4.12 quedó con una nota que apunta a los
    números corregidos de L4.24.
- Costo del estudiante en la sesión: **~$0.17** ($0.0323 + $0.0328 + $0.038 +
  ~$0.04 del ejercicio 9 + ~$0.017 del ejercicio 8). Es la sesión más cara hasta
  ahora, por las respuestas largas del streaming.

**NIVEL 6b NUEVO — pedido por el estudiante al final de la sesión.** Preguntó si
el curso contemplaba *(1) multi-agente con memoria persistente* y *(2) multi-agente
con Skills*. Al revisar el repo:

1. **"Memoria persistente" aparecía UNA vez en todo el repo**: como palabra suelta
   en la celda "Concepto nuevo" del nivel 8. Sin sección, sin ejercicios, sin nada.
   **Es el mismo defecto que observabilidad en la sesión 6** — nombrada de pasada
   dentro de una lista y no desarrollada. Segunda vez que aparece el patrón.
2. **"Skills" no aparecía en ningún archivo.** Hueco completo, cero menciones.

**Corrección conceptual que se le dio, y que decide la ubicación:** ninguna de las
dos es un tema multi-agente. Memoria persistente es que el agente recuerde
**después de que el proceso se cierra**; Skills es conocimiento empaquetado que el
modelo **carga solo cuando le hace falta**. Un agente solo ya necesita las dos. El
multi-agente las *amplifica*, pero aprenderlas ahí sería mezclarlas con
orquestación — dos cosas nuevas a la vez.

**Y sale un tercer hueco de ahí:** el nivel 2 enseñó que el historial crece
*dentro de una corrida*. **Nadie cubría qué pasa cuando el programa termina.**
Memoria persistente es la continuación natural de esa pregunta, y estaba
huérfana.

**Decisión (la eligió él entre tres opciones): nivel `6b — Memoria persistente y
habilidades`**, después de TypeScript y antes de producción.

- Se construye **sobre su propio agente de divisas** del 5b, ya portado en el 6.
- Va antes del 7 porque ahí el agente pasa a tener usuarios reales y "recordar a
  cada usuario" deja de ser curiosidad y se vuelve requisito.
- Se usó sufijo `b` en vez de renumerar: **renumerar costó 12 referencias vivas en
  la sesión 6** y no vale la pena repetirlo.

**Archivos actualizados por el cambio:** `README.md` (fila nueva en el mapa +
sección *"Memoria persistente y habilidades (nivel 6b)"* + la celda del nivel 8
ahora dice *"memoria y skills **compartidas**"*), `CLAUDE.md` (las dos menciones a
"el mapa de los 9 niveles"), y este archivo.

⚠️ **Cuando se llegue al 6b: verificar la API antes de escribir nada.** Memoria y
Skills son de las partes que más rápido cambian del SDK. Es la regla de la sesión
3 (afirmar "es gratis" sin comprobarlo) y la misma nota que ya tiene el 5b con
sus dos URLs.

### Sesión 8 — 2026-07-29

**NIVEL 5 ARRANCADO.** Se creó `05-evaluacion/` con el README (§5.0) y cuatro
scripts, **los cuatro corridos por el estudiante**. Se cerró la duda que venía
abierta desde el nivel 3.

**Lo primero que pidió, y hay que anotarlo como método:** antes de escribir una
línea de código preguntó *"explícame qué es la evaluación, para qué sirve, qué
aporta, en qué momento se hace"*. Y después: *"¿todo esto va a quedar
registrado?"*. Por eso §5.0 del README se escribió **antes** que cualquier
script, no al final.

**Orden del nivel, elegido por él:** duda del dialecto → evals deterministas →
LLM-as-judge.

#### Los cuatro scripts

- **`00_probar_detector.py`** — prueba los detectores **sin llamar a la API**.
  16 casos, $0.00. Salió **idéntico en las dos máquinas**, como los errores del
  nivel 4. Es un eval determinista de verdad, aunque todavía no se llame así.
- **`01_contar.py`** — el mismo prompt N veces, con detector de rioplatense.
- **`02_contar_v2.py`** — la versión corregida + detector de tratamiento.
- **`03_contar_v3.py`** — tres versiones intercaladas (control / prohibición /
  posición), con rangos de confianza.

#### Experimento 1 (v1): 0 de 10 — y el error de diseño era mío

Preguntó *"¿qué ropa me pongo hoy en Bogotá si está lloviendo?"* a un modelo
**sin herramientas**. Resultado: **0 de 10**, contra un histórico de 3 de 9.

- **La causa: 6 de las 10 respuestas se gastaron disculpándose** (*"no puedo
  consultar el clima"*). El modelo nunca llegaba a dar consejo, que es donde el
  defecto vive. Yo había escrito en el código que la pregunta "provoca consejo".
  Provoca consejo **y también** disculpa, y no lo pensé.
- Es el error de `03_recortar.py` del nivel 2 con otra ropa: una prueba que
  corre, que no revienta, y que no prueba lo que dice probar.
- → **`0 de 10` no refuta `3 de 9` si no midieron lo mismo.** Un experimento que
  cambia las condiciones y sale limpio no demuestra que arreglaste algo:
  demuestra que dejaste de mirar donde estaba.
- **Hallazgo lateral que nadie buscaba:** al leer las 10 respuestas se vio que el
  modelo trataba de **tú** en 4 y de **usted** en 5, con el mismo prompt. De ahí
  salió el segundo detector. **Contar N veces te enseña cosas que no fuiste a
  buscar.**
- **Novena confirmación de la entrada determinista:** las 10 dieron 102 tokens.
  Es la más fuerte hasta ahora (antes eran 3 o 4 datos, aquí 10 de 10).

#### Dos bugs míos en los detectores, cazados antes de gastar

1. **`normalizar()` borraba la señal que buscaba.** `"Llevá"` y `"Lleva"` se
   diferencian solo en la tilde, y yo quitaba tildes antes de comparar. El
   detector habría marcado la forma **colombiana correcta** como rioplatense.
   Arreglo: dos listas, y los imperativos voseantes se buscan **sin normalizar**.
   → Mismo patrón del `[:30]` del nivel 1 y del `[:80]` del nivel 6: **el
   preprocesamiento destruye el dato antes de que lo veas.**
2. **`margen()` mentía en los extremos.** Con 0 de 30 devolvía `±0.0`, o sea
   *"defecto eliminado, con certeza total"*. Falso: un defecto del 5% tiene ~21%
   de probabilidad de no salir ni una vez en 30. Arreglado con la **regla de
   tres** (si no viste ninguno en n intentos, el tope al 95% es 3/n) y renombrado
   a `rango()`, porque dejó de ser simétrico. → **El peor bug posible en un eval:
   no revienta, solo miente, y miente con cara de matemática.**

Los dos se encontraron **corriendo las pruebas offline antes de pagar nada**.
Ese hábito ya se pagó solo dos veces en una sesión.

#### Experimento 2 (v2): 9 de 30 — el defecto vive en UN verbo

Con el clima **dado** en la pregunta, el modelo entra directo a aconsejar.

- **9 de 30 = 30%**, contra el histórico de 3 de 9 = 33%. **Dos estimaciones
  independientes, condiciones distintas, y coinciden.** El defecto pasó de
  sospecha a número reproducible.
- **EL HALLAZGO DEL NIVEL.** Casi todas las respuestas dicen lo mismo; lo único
  que baila es cómo conjuga el primer verbo:

  | forma | cuántas | qué es |
  |---|---|---|
  | `ponte` | 18 de 30 | tú, colombiano correcto |
  | `ponete` | **9 de 30** | **rioplatense — el defecto entero** |
  | `póngase` | 2 de 30 | usted |

  **Los 9 rioplatenses son exactamente las 9 respuestas con `ponete`**, y los 2
  ustedeos son los 2 `póngase`. Los 3 `llevá` acompañan siempre a un `ponete`.
  → El fantasma que se perseguía desde el nivel 3 no es "a veces habla
  argentino": es **una bifurcación en una sola palabra**, entre tres formas que
  son todas español correcto. Por eso ningún `SYSTEM` que diga "español de
  Colombia" lo mata: las tres *son* español.
- Y explica la v1: allí la respuesta empezaba con *"no puedo consultar…"*, así
  que **la bifurcación nunca ocurría**.
- **Los 2 `mixto` son reales**, verificados leyendo el texto completo: *"**Ponte**
  una chaqueta… **Lleve** paraguas"*. Cambia de tú a usted entre la primera y la
  segunda frase, **las dos veces en el mismo sitio**.
- Predicciones del estudiante: rioplatense 4 (salió 9), mixto 2 (**salió 2,
  clavado**), usted 4 (salieron 2).
- Costo $0.1273 contra mi estimación de $0.14. Le pegué, después de fallar dos.

#### Experimento 3 (v3): el control NO se replicó

Tres versiones **intercaladas** A,B,C,A,B,C… (la técnica del ejercicio 9 del
nivel 4, aplicada a tres), 30 corridas cada una, $0.3191.

- ⚠️ **A (control) dio 3 de 30 = 10%, no el 30% de la v2.** Mismo prompt exacto
  (entrada 108 en las dos), misma máquina, veinte minutos después.
  - Los rangos se tocan (13.6–46.4 vs 0–20.7), así que **el azar basta**: no hace
    falta suponer que cambió algo del lado de Anthropic.
  - **Pero la lección es grande: con N=30 el mismo prompt dio 30% y 10%.**
    N=30 no era suficiente, y solo se supo **porque había un control**.
  - Como el prompt es idéntico, las 60 corridas se pueden juntar:
    **12 de 60 = 20%, entre 9.9% y 30.1%.** Es la mejor estimación que hay.
  - → **El control no es relleno. Es lo que te dice si tu regla de medir sigue
    siendo la misma regla.**
- **La métrica binaria no tenía poder; la fina sí.** El script declaró
  correctamente "no demostrado" para *¿hubo rioplatense sí/no?*. Al preguntar en
  cambio *¿qué forma del verbo usó?* —que tiene señal en las 30 respuestas y no
  solo en las 3 malas— todo se separa:

  | | dijo `ponte` | rango |
  |---|---|---|
  | A | 19/30 = 63% | 46–81% |
  | B | **30/30 = 100%** | 90–100% |
  | C | 28/30 = 93% | 84–100% |

  A vs B **separados**. A vs C **separados**. B vs C **se solapan**.
  → **No hizo falta gastar más: hizo falta medir mejor.** Mismos datos, mismo
  dinero, otra pregunta. Si tu métrica solo mira los fallos, tiras la información
  de los aciertos.
  - Salvedad anotada: elegir la métrica después de ver los datos es una trampa
    clásica. Aquí no aplica porque `forma_verbal()` se escribió **antes** de
    correr la v3, con los datos de la v2. Pero había que decirlo.
- **La hipótesis del estudiante (nivel 4) sobrevive.** C —mover *"español de
  Colombia"* del `SYSTEM` al turno del usuario— funciona, y es indistinguible de
  prohibir el voseo con nombre propio. **Lo que NO se demostró es que C sea
  mejor que B**: se solapan.
- **El premio es de ingeniería:** B cuesta **+80 tokens de entrada por llamada**
  ($0.40 por cada 1.000 llamadas, para siempre); C cuesta **+3** ($0.015).
  **26x más barato por el mismo efecto.** Mismo tipo de costo permanente que el
  menú de `tools` del nivel 3.

#### Paso 2 — Evals deterministas del harness (`04_evals_harness.py`)

**24 evals, $0.00, idénticos en las dos máquinas.** Prueban los seis frenos del
nivel 4: dinero, permisos, candado de ruta, coherencia, registro y topes.

- **Muro previo, y es lección:** `03_harness.py` **no se podía importar sin
  ejecutarse** (no tenía `if __name__ == "__main__"`). Cargarlo para probar sus
  piezas creaba la caja, hacía las 3 preguntas, gastaba $0.03 y esperaba un
  `input()`. **Arreglado**: todo lo ejecutable se movió dentro de `main()`.
  → **Para poder probar tu código, tiene que poder cargarse sin ejecutarse.**
- **AGUJERO DE SEGURIDAD REAL encontrado por un eval**, y es el hallazgo del
  paso: el permiso decía `if respuesta.startswith("s")`, así que **cualquier
  palabra que empezara por `s` autorizaba el borrado** — incluidas `salir`,
  `stop`, `suspende`, `sal de ahí`. **Las palabras para abortar en español
  empiezan por s.** El freno se abría con la palabra que uno escribe para
  cerrarlo.
  - **Lo que falló de fondo:** *denegar por defecto* estaba perfecto en
    `PERMISOS.get(nombre, "prohibir")` y **no** en la lectura del teclado,
    **tres líneas más abajo, en la misma función**. Nadie lo vio en dos sesiones
    leyendo ese archivo. → L5.14.
  - Arreglado: `if respuesta in {"s", "si", "sí"}`.
  - Lo encontró el caso que probaba **13 teclas hostiles**. Probar `"s"` y `"n"`
    habría pasado. → **Un eval vale por sus casos hostiles.**
- **Defecto mío de presentación, cuarta vez del mismo patrón:** los evals
  llamaban a `pedir_permiso()`, que imprime, y 20 líneas de `PERMISO:` ahogaban
  la salida. Arreglado capturando `stdout` — **y guardándolo para mostrarlo solo
  si el caso falla**. Callado cuando va bien, hablador cuando se rompe.

#### Paso 3 — El juez (`05_juez.py`), y por qué perdió contra el `if`

- **Primer intento: detectar dialecto. Tres rúbricas, empeorando: 83% → 75% →
  42%** de acuerdo con el detector determinista.
  - v1 falló porque no tenía **regla de desempate**: el texto era una mezcla real
    (`ponete` junto a `buso`, `harto`, `sombrilla`) y el juez desempató por
    mayoría. **El fallo era de la rúbrica, no del juez.** → L5.16.
  - v2 y v3 fallaron porque el juez **no distingue `lleva` de `lleve` ni `ponte`
    de `ponete`** — una letra.
  - **Se paró de tunear a propósito**, porque seguir ajustando hasta que el
    número quedara bonito es la trampa que el propio §5.3 advierte.
  - → **Si un `if` puede responder la pregunta, no uses un juez.** Distinciones
    ortográficas: `if`. Comprensión del contexto: juez. El detector gana en
    costo ($0 vs cuesta), estabilidad (100% vs 92%) y acierto.
- **Reorientado a donde el `if` SÍ se había rendido:** la consistencia del
  tratamiento, donde `le`/`se`/`su` se habían dejado fuera por ambiguos.
- **Balance sobre 120 respuestas:** cazó **3 de 3** mezclas conocidas, encontró
  **4 reales nuevas** y soltó **36 falsas alarmas**. Una de cada seis alarmas era
  real.
  - Las 4 reales eran todas `"No olvide el paraguas"` junto a `"ponte"` —
    **ustedeo que no estaba en ninguna lista y que no se me habría ocurrido
    buscar.** Eso es lo que un `if` no puede hacer.
  - → **Un juez es buen filtro y mal decisor.** 120 respuestas → marca 43 → lees
    43 → encuentras 4 defectos invisibles.
- **LO MÁS GRAVE: el juez fabrica evidencia.** En textos que decían `Lleva`
  (tuteo consistente), citó `['ponte','te','lleva','lleve']` — **`lleve` no
  estaba en el texto** — para sostener una mezcla inexistente. Tres veces.
  En total **9 de 451 citas (2%) no estaban**, y eran justo las que sostenían los
  veredictos. → L5.18.
  - **Se descubrió solo porque la rúbrica pedía `"palabras"` además de la nota.**
    Con solo el número, habríamos creído "43 respuestas con mezcla".
    → **Un juez que solo devuelve una nota es incomprobable.**
  - ⚠️ **Mi primera comprobación de las citas tenía el bug de la tilde** (comparaba
    `pongase` contra `póngase`) y estuvo a punto de acusar al juez de inventarse
    lo que sí había dicho. **Cuarta aparición del mismo patrón en una sesión.**
- **Estabilidad:** el juez repitió la misma nota en 6 de 6 en la primera versión
  — **100% consistente y equivocado**. → **Consistencia no es corrección**, y por
  eso correr el mismo modelo dos veces no protege de nada (L5.17).
- **Decisión de diseño anotada:** elegí Haiku razonando "clasificar es tarea
  fácil". **Los datos lo contradicen** y quedó convertido en el ejercicio 1.

#### Tres preguntas conceptuales suyas (respondidas, vale la pena conservarlas)

1. **"¿Esto son guardrails?"** — No exactamente: el **guardrail** es la
   protección (vive en el agente, corriendo); el **eval** es la prueba de que
   funciona (vive en el banco de pruebas). El freno del carro vs la revisión
   técnico-mecánica. De los seis frenos del nivel 4, cinco son guardrails; el
   registro **no** (no impide nada, solo cuenta: eso es observabilidad).
2. **"¿Sería mejor un juez de otro proveedor?"** — Conceptualmente sí para la
   autopreferencia, pero **lo primero es validar contra tus propias etiquetas**,
   no diversificar proveedores. Un juez de otra empresa sin validar sigue siendo
   una opinión sin validar.
3. **"Con 5 agentes, ¿hay que evaluar cada uno?"** — Sí, y el número que lo
   justifica: cinco agentes al 90% dan `0.9^5 = 59%` de acierto en el sistema.
   Aparece además el problema de **atribución** (¿cuál de los cinco falló?), que
   es lo que convierte el registro del nivel 4 en obligatorio. El resto, nivel 8.

#### Costo del estudiante en la sesión

$0.0459 (v1) + $0.1273 (v2) + $0.3191 (v3) + $0.1268 (juez Haiku)
= **~$0.62**. La sesión más cara del curso, con diferencia, y la primera en que
dos preguntas suyas se responden con evidencia en vez de con una explicación
plausible.

⚠️ **CORREGIDO en la sesión 9:** esta línea decía *"~$0.06 (juez, 140 llamadas
Haiku)"* y el total *"~$0.55"*. Los **$0.06 eran un estimado mío sin medir**; el
JSON de la corrida dice **$0.1268**, más del doble. Total real ~$0.62. → L5.23.

**Nota de costo que vale la pena recordar:** el juez calificó texto **ya
generado**, leído de `resultados/*.json` — los $0.49 de generarlo ya estaban
pagados, así que juzgarlo costó una fracción. → L5.20.

### Sesión 9 — 2026-07-29

**EJERCICIO 1 DEL NIVEL 5 HECHO.** Corrió `05_juez.py` con `MODELO_JUEZ =
"claude-sonnet-5"` sobre las mismas 120 respuestas. Fue el ejercicio que más
enseñó del nivel, como estaba previsto — pero **enseñó cosas distintas de las
que yo había anticipado**, y las tres correcciones son mías.

#### El resultado

| | Haiku 4.5 | Sonnet 5 |
|---|---|---|
| acuerdo con el detector | 66.4% | **95.8%** |
| marcó como mezcla | 43 de 120 | **8 de 120** |
| **mezclas reales cazadas** | **4 de 4** | **4 de 4** |
| falsas alarmas | 39 | 4 |
| precisión | 9% | **50%** |
| citas fabricadas | 9/451 (2.0%) | **1/323 (0.3%)** |
| estabilidad | 18/20 | **20/20** |
| sin formato válido | 1 | **0** |
| costo real | $0.1268 | **$0.3060** |

- **El hallazgo central, y no es el que la pregunta del ejercicio buscaba:**
  los dos jueces cazaron **las mismas 4 mezclas reales**. El caro **no encontró
  nada** que el barato se perdiera. Lo que cambió fue el trabajo humano: 43
  respuestas que leer contra 8. **$0.18 más = 35 respuestas menos.** → L5.21.
  Yo había escrito el ejercicio preguntando *"¿sube el acuerdo?"*, como si la
  pregunta fuera de exactitud. Era de **cuánto te queda por leer**.
- **Sonnet TAMBIÉN fabricó una cita** (`lleve` por `lleva`, la misma
  alucinación de Haiku) y en otra alarma **se contradijo dentro de su propia
  `razon`**: *"Mezcla tuteo (ponte) con ustedeo (lleva es tuteo, pero revis..."*.
  → L5.22: un modelo mejor vuelve el defecto **raro**, no lo elimina — y eso es
  más peligroso, porque desactiva la costumbre de comprobar.

#### Tres correcciones, las tres mías

1. **BUG REAL en `05_juez.py`.** Los precios estaban quemados a mano con los de
   Haiku (`PRECIO_ENTRADA = 1.00 / 1_000_000  # Haiku`). Al cambiar el modelo
   **el costo impreso quedó a la mitad**: dijo `$0.1530`, real `$0.3060`.
   Sin excepción, sin aviso, y en la línea que dice `COSTO REAL`.
   **Arreglado**: diccionario `PRECIOS[MODELO]` que **revienta** si el modelo no
   está; el precio aplicado ahora se imprime al lado del total y se guarda en el
   JSON junto con los tokens (un costo suelto no se puede auditar). → L5.23.
2. **Mis dos estimados de costo eran inventados.** El README decía *"~$0.18 en
   vez de ~$0.06"*. Medido: **$0.306 y $0.127**. La *razón* entre modelos quedó
   cerca (~2.4x contra el 3x que dije); las **magnitudes** las inventé las dos.
   Mismo patrón del `"55x"` (nivel 1) y del `"~$0.02"` (nivel 4).
3. **Un cuarto bug del preprocesamiento, cometido por mí en vivo al analizar sus
   datos.** Escribí `if 'olvide' in texto`, y `'olvide' in "no olvides"` es
   `True` — pero `"No olvides"` es tuteo **correcto**. Dio **46** mezclas; con
   `\bolvide\b` da **4**. **El 91% del hallazgo era el bug.** Cuarta aparición de
   la misma familia (`[:30]`, `[:80]`, `normalizar()`, `in`). → L5.24, con tabla
   de las cuatro.

#### Verificado, no recordado

Se comprobaron los precios en la documentación oficial antes de tocar el código
(regla de la sesión 3). Apareció una letra pequeña que yo no tenía: **Sonnet 5
está en precio de lanzamiento ($2/$10 por millón) hasta el 2026-08-31**; desde
septiembre, $3/$15, y esa misma corrida costará **~$0.46** sin cambiar una
línea. Está escrito **en el código con la fecha**, no en la memoria de nadie.

#### Archivos actualizados

- `05_juez.py` — diccionario `PRECIOS` + guarda que revienta + precio impreso +
  `precio_usado` y `tokens` en el JSON.
- `05-evaluacion/README.md` — **§5.6 nueva** (la comparación entera, las tres
  afirmaciones caídas, el cuarto bug, y la conclusión honesta); nota en §5.5
  aclarando que sus números son los de Haiku; ejercicio 1 marcado ✅ con
  resumen; ejercicio 4 reescrito y ascendido.
- `LESSONS.md` — **L5.21–L5.24** (4 nuevas; el nivel 5 va por 24).
- `GUIDE.md` §8.j — tabla de costos con los números **medidos** en vez de los
  estimados, + cómo atar precios al modelo, + la caducidad del precio de
  lanzamiento.
- `PROGRESO.md` — este bloque, la cabecera, el costo de la sesión 8 corregido, y
  el punto de "los 43 marcados" cerrado.

#### NIVEL 5 CERRADO + APIs del 5b reverificadas

Se le ofrecieron los ejercicios que quedaban y **eligió cerrar el nivel 5 y
pasar al 5b**. También se le ofreció arreglar los 6 scripts con el precio suelto
y prefirió avanzar (queda anotado arriba como pendiente vivo).

**Las dos URLs del 5b se reverificaron con `curl` el 2026-07-29**, cumpliendo la
nota que dejó la sesión 8. Las dos responden **HTTP 200**:

| Fuente | URL | 29 jul | 28 jul |
|---|---|---|---|
| Mercado | `https://open.er-api.com/v6/latest/USD` | 3.206,17 | 3.215,61 |
| TRM oficial | `https://www.datos.gov.co/resource/32sa-8pi3.json` | 3.205,87 | 3.205,80 |

- La TRM acepta `?$order=vigenciadesde DESC&$limit=N` y devuelve los campos
  `valor`, `unidad`, `vigenciadesde`, `vigenciahasta`. La API de mercado sigue
  trayendo `time_last_update_utc` / `time_next_update_utc`.
- **HALLAZGO NUEVO, y corrige un supuesto de la sesión 8:** la brecha entre las
  dos fuentes **no es fija**. El 28 de julio eran ~10 pesos; el 29 son **0,30
  pesos**. La sesión 8 anotó *"no coinciden (~10 pesos)"* con **una sola
  observación** detrás. Lo estable es **que son fuentes distintas**, no cuánto se
  separan. → El material del 5b debe enseñar *"pueden no coincidir"*, nunca una
  magnitud. Es L1.13 otra vez, atajada antes de escribir nada.
- El hueco del fin de semana sigue vivo en los datos (la TRM del 25 valió hasta
  el 27): el caso de prueba no hay que inventarlo.

#### Método del estudiante — confirmado otra vez

- **Pidió las dos cosas** ("arregla el bug y escribe el análisis") en vez de
  elegir una. Prefiere cerrar el ciclo completo antes de pasar a lo siguiente.
  **Ofrecerle las dos juntas en vez de hacerle escoger.**
- Cuando decide avanzar, avanza: no se queda puliendo pendientes opcionales.
  Anotarlos como vivos y no insistir.

### Sesión 10 — 2026-07-29

**NIVEL 5b ARRANCADO.** Y arrancó como él pidió: **explicación primero, cero
teclado**. Los tres temas que había dejado anotados se explicaron antes de crear
un solo archivo.

#### Lo que se hizo

- **Carpeta creada por él:** `05b-proyecto/` en la raíz, hermana de las otras.
  Se le explicó **por qué ahí y no dentro de `05-evaluacion/`**: además de que es
  un nivel propio, `parent.parent / ".env"` deja de encontrar la key si se anida
  un nivel más. Creó los 4 archivos vacíos (`README.md`, `herramientas.py`,
  `agente.py`, `evals.py`).
- **`README.md` del nivel escrito completo** (§5b.0 a §5b.5): qué es un proyecto
  integrador, la tabla de piezas heredadas nivel por nivel, las 5 herramientas con
  *lo difícil de cada una*, la estructura de archivos con su porqué, las dos APIs
  con la advertencia de la brecha variable, y **el plan de los 10 pasos con quién
  escribe cada uno**.
- **Decisión de estructura, dictada y con su razón:** `herramientas.py` separado de
  `agente.py`. La razón es la del nivel 5 (`00_probar_detector.py`): **separar lo
  que se puede probar gratis de lo que cuesta dinero probar.** De las 5
  herramientas, 3 necesitan internet y 2 no.

#### `convertir()` — la primera función que escribe él solo

Se le planteó como **decisión de diseño**, no como dictado: ¿la tasa la busca la
función (opción A) o se la pasan por parámetro (opción B)? **Eligió B** y contestó
bien las tres preguntas de control (no se puede probar sin internet con A; el
error de la tasa y el de la multiplicación solo se distinguen en B).

- **Se le completó la respuesta 2**, que tenía a medias. Dijo *"yo le paso el
  número"* — cierto para `evals.py`, pero cuando el agente corre **el que consigue
  la tasa es el modelo**, encadenando dos herramientas en tres vueltas
  (`obtener_tasa` → `convertir` → responder). **Nadie programa esa cadena**; solo
  existen las dos `description`. Es el nivel 3 otra vez. → Su opción B no solo hace
  la función probable gratis: **le da al modelo algo que decidir.**
- **Se le enseñó a construir el `dict` de retorno**, que era lo que no sabía hacer.
  El punto que confunde a todos: `"monto": monto` son dos cosas distintas (etiqueta
  fija vs valor que cambia).

#### Los cuatro defectos de su primera versión, y qué lección tenía cada uno

Los encontró él corrigiéndolos, no se los reescribí. **Tres de los cuatro son
patrones que ya aparecieron antes en el curso:**

1. **Validaba solo `a`, no `de`.** Y salió el *por qué* se escapa, que es lo
   valioso: `de` es **el único parámetro que no participa en ningún cálculo** —
   entra y sale directo al `dict`. → **Los parámetros que solo se transportan son
   los que nadie valida.** No fallan, no dan señales, y son los que dejan pasar la
   basura. Y es el peor: si `de` está mal, la multiplicación es perfecta y el
   resultado falso. *(Se le pasó una vez más incluso después de señalarlo — se
   corrigió a la tercera pasada.)*
2. **Dos listas que tenían que coincidir** (`MONEDAS` y `DECIMALES`) y nada las
   obligaba. **Es L5.23 exacta** — el precio suelto al lado del `MODELO`: hoy no
   miente, miente el día que cambies uno solo. Se resolvió con **una sola fuente de
   verdad**: `MONEDAS = tuple(DECIMALES)`. Eligió esa opción sobre la de validar
   contra `MONEDAS`.
3. **`DECIMALES` estaba declarado dentro de la función.** Dos razones para subirlo:
   `evals.py` no puede verlo, y `MAYÚSCULAS` es la convención de "constante del
   archivo" — una constante dentro de una función se contradice.
4. **La multiplicación estaba dos veces**, y la primera **calculaba antes de
   validar**. Hoy no duele (multiplicar no revienta), pero el hábito es el que
   importa: **primero se revisa, después se calcula.**

**Más un regalo:** su mensaje de error decía solo *"No manejo la moneda BTC"* —
que es **el 404 de la sesión 6**: repite lo que le mandaron y no dice qué hacer.
Se le recordó **quién lo va a leer** (el modelo, como `tool_result`) y lo cambió a
`f"... Solo: {', '.join(MONEDAS)}."`, que sí permite que se corrija solo en la
vuelta siguiente.

#### Pregunta suya que se volvió media lección: **`if` o `try/except`**

La hizo sin que nadie la provocara (*"¿podría ser un try except o un if? ayúdame
explicando"*). Se le dio con la analogía primero:

- **`if` = mirar antes de cruzar la calle.** La información está ahí antes de
  moverte.
- **`try/except` = ponerse el cinturón.** No sabes si va a haber choque, pero si
  hay, no te mata.
- **La pregunta que decide:** *¿puedes saber la respuesta antes de intentarlo?*
  Sí → `if`. No, depende de algo que no controlas → `try/except`. Y ese "algo" casi
  siempre es **internet, el disco, o lo que escribió un humano**.
- **Segunda razón, más práctica:** el `try/except` equivalente aquí habría envuelto
  tres operaciones en una línea, así que `except KeyError` no distinguiría cuál
  falló. → **Un `try` debe envolver lo menos posible.** Es el nivel 3 otra vez
  (*"lee la coordenada antes que la frase"*): un `try` ancho borra la coordenada.
- **Y se le dijo dónde SÍ lo va a usar:** el paso 6, las tres herramientas de
  internet. *No hay ningún `if` que te diga si internet va a funcionar dentro de
  200 ms.* Lo normal es tener **los dos en la misma función**: el `if` arriba
  revisando argumentos, el `try` abajo envolviendo la línea peligrosa.

→ **Candidata fuerte a lección del nivel** (L5b.x) cuando se cierre el 5b.

#### Un despiste que vale anotarlo

Me pegó la versión corregida en el chat, pero **el archivo en disco seguía con la
versión vieja** — no había guardado. Se detectó porque leí el archivo en vez de
creerle al chat. Si hubiera pasado en el paso 5, `evals.py` habría fallado sobre
código viejo y el rato perdido habría sido buscando un bug ya arreglado.
→ **Leer el archivo antes de opinar sobre él**, aunque me acaben de pegar el
contenido.

#### Costo de la sesión: **$0.00**

No se hizo ni una llamada a la API. Y eso **es el diseño del nivel, no una
casualidad**: los pasos 4 y 5 son gratis a propósito.

---

**Cambio de plan pedido por el estudiante (sesión 6).** Preguntó dos cosas que el
plan no cubría bien: *(1) ¿y los harnesses con orquestador y workers?* y
*(2) ¿dónde entran observabilidad, rúbricas y evaluación?* Al revisar el mapa
aparecieron tres huecos reales, dos míos:

1. El nivel 6 decía solo *"evals, casos de prueba, regresiones"* — eso cubre lo
   que se comprueba con un `if`, y **dejaba fuera las rúbricas / LLM-as-judge**,
   que es justo lo que hace falta para su propia duda del dialecto.
2. Observabilidad estaba **nombrada de pasada** en una lista del nivel 7, no
   desarrollada como pieza.
3. Al explicarle el nivel 5 (que no está escrito, solo planeado) salió una
   pregunta que yo no tenía resuelta: **si el nivel 5 pasa a TypeScript, ¿en qué
   lenguaje se hace el nivel 6?** Cualquiera de las dos respuestas tenía costo.

**Decisión: se intercambian los niveles 5 y 6.** Nuevo orden: harness →
**evaluación** → **TypeScript** → producción → multi-agente. Él eligió esta
opción entre tres que le planteé. Ver *Decisiones tomadas* para el porqué.

Archivos actualizados por el cambio de numeración (12 referencias vivas, buscadas
en todo el repo antes de editar — la regla de la sesión 3): `README.md` (mapa
nuevo + sección "Los tres temas que se preguntan siempre"), `CLAUDE.md`,
`LESSONS.md` (4), `GUIDE.md` (1), `03-primer-agente/README.md` (1),
`04-harness-real/README.md` (2), y este archivo.

**El nivel 8 también se precisó:** ahora dice *"Multi-agente: orquestador y
workers"*. La respuesta corta que se le dio, y que quedó escrita en el
`README.md`: **un orquestador es un agente cuyas herramientas son otros agentes**
— el bucle del nivel 3 anidado, por eso va al final.

---

**Nivel 5b propuesto por el estudiante (sesión 6).** Pidió un proyecto práctico
donde construya un harness con varias herramientas **desde un archivo vacío**,
con instrucciones paso a paso, hasta la evaluación.

- **Diagnóstico que lo justifica:** en 6 sesiones ha leído, corrido y analizado
  mis scripts — y muy bien: encontró dos bugs míos y corrigió un análisis mal
  atribuido. Pero **nunca ha empezado desde un archivo vacío**. Entender código y
  producirlo no son la misma habilidad, y hasta ahora solo se practica la primera.
- **Ubicación:** después del nivel 5 (evaluación), antes del 6 (TypeScript).
  Carpeta `05b-proyecto/` para que ordene bien. La eligió él y es correcta:
  cierra todo el Python de un tirón, y el nivel 6 pasa a portar **su** agente en
  vez del mío.
- **Formato elegido: mixto.** Dictado literal en lo mecánico (entorno, imports,
  estructura de carpetas); guiado en lo conceptual (bucle, frenos, evals), donde
  se dice *qué* y *por qué*, lo escribe él, y después se compara con mi versión.
  - ⚠️ **La razón del formato mixto, para no olvidarla:** el paso a paso dictado
    tiene el riesgo de que teclee sin pensar y termine con un agente que funciona
    y que no sabría rehacer. Sería el único nivel donde el código no pasó por su
    cabeza. Pero crear el `.venv` o escribir los `import` es mecánico y ahí
    dictarlo está bien. **Separar lo mecánico de lo conceptual.**
- **Tema elegido por él: agente de divisas y TRM.** COP ↔ USD, EUR, CAD en ambos
  sentidos, más TRM oficial de Colombia. Es mejor que las tres opciones que yo
  había propuesto, por cuatro razones:
  1. **Tiene verdad comprobable** — la conversión se verifica con una
     multiplicación. Casi ningún agente tiene ground truth; este sí. Los evals
     deterministas del nivel 5 salen solos.
  2. **Y también tiene el caso de rúbrica** — "¿dijo de qué fuente sacó la tasa?"
     no se comprueba con un `if`.
  3. **Trae la trampa central:** un LLM puede equivocarse multiplicando.
     **La herramienta calcula; el modelo solo decide a cuál llamar.** Y aquí se
     puede *medir* que pasa.
  4. Da para 5 herramientas de tipos distintos (API en vivo, cálculo puro, API
     con fecha, serie de tiempo, y una que escribe en disco y pide permiso).

### Verificado el 2026-07-28 (revisar de nuevo AL LLEGAR al 5b)

Las dos APIs son gratis y **sin llave**. Comprobadas con `curl`, no de memoria:

| Fuente | URL | Dato de hoy |
|---|---|---|
| Mercado | `https://open.er-api.com/v6/latest/USD` | 1 USD = 3.215,61 COP |
| TRM oficial | `https://www.datos.gov.co/resource/32sa-8pi3.json` | 1 USD = 3.205,80 COP |

Tres hallazgos que salieron de esa verificación y que ya son material del nivel:

1. **Las dos fuentes no coinciden (~10 pesos) y las dos son correctas.** Para una
   factura en Colombia la respuesta legal es la TRM; para saber cuánto te cobran
   de verdad, la del mercado. → *"¿A cuánto está el dólar?"* no tiene una sola
   respuesta correcta. Es material de rúbrica servido en bandeja.
2. **El plan gratis actualiza una vez al día.** La respuesta trae
   `time_last_update_utc` y `time_next_update_utc`, así que el agente **puede
   saber qué tan vieja es su información**. Obliga a dos piezas de harness real:
   caché y avisar de datos rancios. No lo busqué: venía en la respuesta.
3. **La TRM no cambia el fin de semana.** La de hoy vale del 28 al 28; la
   anterior valía **del 25 al 27**. Preguntar por un sábado es un caso de prueba
   que no hubo que inventar.

> ⚠️ Las URLs funcionaban el 2026-07-28. **Volver a comprobarlas antes de escribir
> nada encima** — es la lección de la sesión 3 (afirmar "es gratis" sin verificar).

---

**`03_harness.py` explicado (final de la sesión 6), pero NO corrido todavía.**
Se hizo en las tres partes acordadas y **no hay que repetirlo**:

1. *Los seis frenos*, planteados como "¿qué pasa si falta?" en vez de "¿qué
   hace?". La idea que los amarra: **ninguno de los seis confía en el modelo.
   El modelo decide qué hacer; tu código decide qué está permitido.**
2. *El recorrido por el código*, por zonas (A–G): la configuración arriba del
   todo, `PresupuestoAgotado` como error-que-no-es-error, el `**datos` de
   `anotar()`, la herramienta que atrapa su propio error y lo devuelve como
   texto, los tres detalles de los permisos, la llamada blindada y el bucle con
   tope.
3. *Qué se aprende*: la diferencia entre "funciona" y "es confiable"; dónde vive
   cada decisión; **denegar por defecto**; que los errores se degradan en tres
   capas en vez de propagarse; y que estas seis piezas son lo más directamente
   aplicable a su SaaS de todo el curso.

Dos cosas que se le señalaron y que conviene retomar cuando lo corra:

- **Trampa latente que él podría cazar:** si alguien pusiera
  `REINTENTOS_PROPIOS = 0`, el `for` de `llamar_modelo()` (línea 247) no se
  ejecutaría nunca y la función devolvería `None` en silencio. Hoy no molesta
  —está en 3— pero es del mismo tipo que el contador roto de `01_chat.py`.
- **Denegar por defecto** (`PERMISOS.get(nombre, "prohibir")`) se presentó como
  principio general, no como detalle: diseñar para que **el olvido falle hacia
  el lado seguro**. Vuelve a aparecer en el nivel 7.

---

**Sesión 6 cerrada aquí.** Lo hecho: scripts 1 y 2 corridos y analizados, un
defecto de presentación arreglado y verificado, README §4.1 y §4.2 actualizados,
el mapa del curso reordenado, un nivel nuevo (5b) diseñado con sus APIs
verificadas, y `03_harness.py` explicado.
Costo del estudiante en la sesión: ~$0.0013 (solo la llamada real del script 2).

---

### Sesión 11 — 2026-07-30

**PASOS 4 y 5 DEL NIVEL 5b CERRADOS.** El detalle completo está arriba, en la
cabecera del 5b (no se duplica aquí). Resumen de lo que se produjo:

- **`guardar_reporte()` escrita por él**, con 3 frenos y la **allowlist** razonada
  desde cero (la analogía del portero A/B). Costo: $0.00.
- **`herramientas.py` reorganizado** a petición suya (*"que se vea más
  profesional"*), con el **contrato** del archivo escrito arriba. Se corrió la
  misma prueba antes y después: comportamiento idéntico.
- **`evals.py` completo: 26 casos, 2 bucles, 0 fallos, $0.00 y sin red.**
  16 casos de `convertir()` + 10 de `guardar_reporte()`.
- **Cinco defectos reales encontrados y arreglados** en `convertir()`: 4 `TypeError`
  que tumbaban el bucle del agente, la tasa 0 que devolvía `0`, el monto negativo,
  los booleanos colándose como números, y el `4.0` en pesos.
- **Un defecto encontrado y NO arreglado, a propósito:** *banker's rounding*
  (`round(2.5)` → 2). Necesita `Decimal` y es un tema entero → ejercicio del nivel.
- **`GUIDE.md` §8.l nueva:** *Probar tus propias funciones (sin modelo, sin red,
  $0.00)* — la plantilla del bucle, las tres familias de casos, las 6 reglas, las
  **4 trampas de Python** (`4.0 == 4`, `round(x, 0)`, `isinstance(True, int)`,
  banker's rounding) y cómo se prueban las funciones con **efecto secundario**.
- **Ningún gasto de API en toda la sesión.** Es la primera sesión del curso que
  cuesta exactamente **$0.00**, y no por casualidad: era el objetivo del paso 5.

**Método — dos cosas que hay que conservar:**

1. ⚠️ **UNA pregunta a la vez.** Se confirmó dos veces: con tres preguntas juntas
   dijo *"no entendí las preguntas"*; reformuladas a una sola, las contestó bien
   de inmediato, todas.
2. **Pide "escríbeme un ejemplo primero"**, y funciona dárselo **sobre otra
   función** (`poner_apodo`, `doblar`) para no regalarle su ejercicio.
   ⚠️ Pero hay que **decir explícitamente que la función del ejemplo no va en su
   archivo**: preguntó cómo "convertir `doblar`" para el ejercicio.

**Lo que hizo bien y conviene reconocerle:** las decisiones de diseño del día
salieron de él (allowlist, rechazar el monto negativo, los **dos candados**, dejar
el freno 3, rechazar minúsculas y textos, borrar antes de probar, comprobar
existencia **y** contenido). El código mecánico lo pidió dictado; **el criterio no.**

---

## Dudas abiertas

_(Aquí anotamos preguntas que quedaron sin resolver, para retomarlas después.)_

> Las tres primeras se abrieron antes del nivel 5 y **dos ya están cerradas**
> (sesión 8). Llegar al nivel 5 con preguntas propias sin resolver funcionó
> exactamente como se esperaba: el nivel se escribió contra ellas.

- ~~**¿Cómo se prueba algo que nunca responde igual dos veces?**~~ →
  **RESUELTO en la sesión 8**, y la respuesta cabe en cuatro pasos: se corre N
  veces, se cuenta, se pone un **control** al lado, y se mira si los **rangos**
  se solapan antes de declarar nada. La pregunta madre del curso, abierta desde
  el nivel 1 (L1.6, L1.11, L1.16).
- **¿Borrar el turno `assistant` afecta la longitud de la respuesta?** Quedó sin
  resolver porque el experimento tenía 3 variables. Se podría medir de verdad en
  el nivel 5, con 5 corridas por versión.
- ~~**¿Por qué sigue apareciendo el rioplatense con el dialecto anclado?**~~ →
  **RESUELTO en la sesión 8.** Abierto desde el nivel 3, cerrado con 130
  corridas.
  - **La causa:** el modelo elige entre tres conjugaciones del mismo verbo
    (`ponte` / `ponete` / `póngase`) y **las tres son español correcto**. Por eso
    decir "español de Colombia" no lo mataba: no es un problema de idioma sino de
    **variedad**, y el modelo no sabe cuál es la tuya hasta que se la nombras.
  - **La tasa:** 12 de 60 = **20%** (entre 9.9% y 30.1%) con el `SYSTEM` viejo.
  - **El arreglo, demostrado:** tanto prohibir el voseo por su nombre (B) como
    mover la instrucción al turno del usuario (C) suben el uso de la forma
    correcta de 63% a 100% y 93%. Las dos diferencias están demostradas contra
    el control; **B vs C sigue sin resolverse** (se solapan con N=30).
  - **La hipótesis del estudiante sobrevivió:** la posición sí importa, y además
    C cuesta 26x menos que B (+3 tokens contra +80, por llamada, para siempre).
- ⚠️ **DUDA NUEVA, abierta en la sesión 8: el tratamiento tú/usted.** Apareció
  sola al contar. Con el mismo prompt el modelo trata de tú, de usted, o **mezcla
  los dos dentro de una misma respuesta** (2 de 30, verificados a mano). **Ni B
  ni C lo arreglan.** Es el mismo tipo de defecto que el dialecto, en otra
  dimensión, y está medido pero sin resolver.
- **¿Qué llega en los primeros segundos de un stream?** Con streaming la pantalla
  estuvo quieta 5.8 s. La hipótesis es que `text_stream` no entrega los bloques
  `thinking`. **Sin verificar** — es el ejercicio 8 del nivel 4 y se resuelve en
  una corrida barata.

---

## ⚠️ PENDIENTE DE VERIFICAR (leer al abrir la próxima sesión)

- 🔴 **LO PRIMERO DEL PASO 6: volver a comprobar las 2 URLs del 5b.** Están
  verificadas con HTTP 200 el **2026-07-29** y copiadas en
  `05b-proyecto/README.md` §5b.4 con sus campos. **No se escribe código encima sin
  volver a comprobarlas** — es la lección de la sesión 3 (afirmar "es gratis" sin
  verificar). Son `open.er-api.com/v6/latest/USD` (mercado) y
  `datos.gov.co/resource/32sa-8pi3.json` (TRM oficial).
- ⚠️ **`convertir()` tiene un defecto conocido sin arreglar:** *banker's rounding*
  (`round(2.5)` → 2, `round(3.5)` → 4). Los 26 casos del eval **no lo detectan**
  porque ninguno cae en `.5`. El arreglo es `Decimal` en vez de `float` → ejercicio
  del nivel, y empieza por **agregar los casos `.5` y verlos fallar**.
- ⚠️ **Hueco conocido del eval de `guardar_reporte`:** comprueba que no se escribió
  *dentro* de `caja/`, pero **no puede demostrar que no se escribió fuera**. Se
  confía en los 3 frenos + la prueba de fuerza bruta de 278.916 nombres.
- **El manejo de error de red nunca se vio ocurrir con el wifi apagado.** En el
  nivel 4 sí vimos `APIConnectionError` de verdad (apuntando a un dominio que no
  existe), pero nadie ha desconectado el internet y corrido el agente completo.
  Es el **ejercicio 7 del nivel 4**.
- ~~**La hipótesis del `thinking` en el stream**~~ → **medida (ejercicio 8).**
  Mecanismo confirmado, hipótesis **incompleta**: el thinking es la mitad del
  silencio. Ver §4.4, L4.25 y `04b_eventos.py`.
- ~~**El sesgo de orden de `04_streaming.py`**~~ → **medido (ejercicio 9).**
  ~1 s, y la ventaja del streaming corregida a ~6.3 s. Ver §4.4 y L4.24.
  ⚠️ **`04_streaming.py` quedó con el orden invertido** (streaming primero).
  Es el orden correcto para el ejercicio, pero **los números del README §4.4
  están etiquetados por corrida** — al releerlos, mirar la etiqueta.
- ~~**Faltan por correr 2 de los 4 scripts del nivel 4**~~ → **los 4 corridos.**
  - ~~`01_errores.py`~~ → **corrido en la sesión 6.** Idéntico al mío. Encontró
    un defecto de presentación (ver bitácora).
  - ~~`02_reintentos.py`~~ → **corrido en la sesión 6.** Tiempos distintos,
    forma idéntica. Salieron dos hallazgos nuevos (la resta del backoff en la
    sección C y la herencia de `APITimeoutError`).
  - ~~`03_harness.py`~~ → **corrido dos veces en la sesión 7** (`s` y `n`), con
    lectura del `registro.jsonl`. Cuatro hallazgos nuevos.
  - ~~`04_streaming.py`~~ → **corrido en la sesión 7.** Encontró que mi
    estimación de costo del docstring estaba al doble.

### Resuelto en la sesión 4
- ~~`02_bucle.py` con los sabotajes de los ejercicios 1 y 2 aplicados~~ →
  **restaurado por el estudiante y verificado**: línea 107 (`historial.append`
  del turno `assistant`) activa, línea 122 con `"tool_use_id": bloque.id`.

### Resuelto
- ~~`02-conversacion/01_chat.py` sin ejecutar~~ → **corrido por el estudiante**
  en dos versiones (normal y ejercicio 1). Encontró un bug (ver abajo).
- ~~`01-primera-llamada/03_costo.py` modificado y sin ejecutar~~ → **corrido en
  la sesión 3.** Tabla entera, razón calculada = 30.9x. Costo $0.0039.

---

## Errores que encontramos y cómo se resolvieron

_(Este historial vale oro: los mismos errores reaparecen. Anótalos aunque parezcan tontos.)_

- **Pantalla vacía sin ningún error.** `max_tokens=30` en Opus 5: los 30 tokens se
  fueron enteros en el bloque `thinking` y no hubo bloque `text`. No fue un bug —
  `stop_reason: max_tokens` lo decía. → L1.1, L1.2
- **Tabla rota en 3 renglones + respuesta aparentemente cortada** en `03_costo.py`.
  Causa real: el propio script hacía `texto.strip()[:30]`, y la respuesta traía
  saltos de línea internos que `.strip()` no limpia. **No era del modelo.**
  Solución: `" ".join(texto.split())`. → L1.14
- **Dato falso impreso con confianza:** el script decía "Haiku cuesta 5x menos"
  (texto fijo) cuando la medición real dio 55x. Solución: calcular, no fijar. → L1.13
- **Contador roto que no falla, solo miente** (sesión 3, `01_chat.py`):
  `len(historial) // 2` asumía 2 mensajes por turno. Al cambiar la forma del
  historial imprimió `0, 1, 1, 2` sin lanzar ningún error. → Contar con una
  variable propia, no deducir de la estructura.
- **Demostración que no demostraba nada** (sesión 3, `03_recortar.py`): para
  probar que la ventana deslizante "olvida", le preguntábamos algo de cultura
  general (*¿qué es una variable?*). Las tres estrategias acertaron, porque el
  modelo ya lo sabía sin historial. **Regla:** para probar memoria, pregunta un
  dato que el modelo no pueda saber de otro modo (un nombre inventado).
- **Mismo texto de error, causas opuestas** (sesión 4, ejercicios 1 y 2 del
  nivel 3). Los dos dan el mismo mensaje —*"Each `tool_result` block must have a
  corresponding `tool_use` block in the previous message"*— pero:
  - `tool_use_id` inventado → `messages.2.content.0` (había `tool_use`, no
    emparejaba).
  - Sin el turno `assistant` → `messages.0.content.1` (no había `tool_use`
    **ninguno**; y el id era real y correcto).
  → **Lee la coordenada antes que la frase.** El texto no distingue los casos;
  la dirección sí.
- **La API fusiona mensajes consecutivos del mismo rol.** Descubierto sin
  buscarlo en el ejercicio 2: al quitar el turno `assistant` quedaron dos `user`
  seguidos y la API los unió en uno solo, por eso el `tool_result` apareció como
  `content[1]` del mensaje 0. **Tu lista de Python y lo que ve la API no tienen
  siempre la misma forma.**
- **En un bucle agéntico el síntoma va una vuelta por delante de la causa.** El
  id malo se escribe procesando la vuelta 1; el 400 sale en la llamada de la
  vuelta 2. Y para entonces ya pagaste la vuelta 1 sin obtener respuesta:
  un agente roto gasta antes de fallar.
- **El programa funcionó y aun así reventó** (sesión 4, `02_bucle.py`):
  `UnicodeEncodeError: 'charmap' codec`. Las 2 llamadas a la API salieron bien,
  la herramienta se ejecutó, el modelo respondió — y el `print` de esa respuesta
  murió porque la consola de Windows es `cp1252` y el texto traía `°` y emojis.
  → `sys.stdout.reconfigure(encoding="utf-8")`. **Lee a qué línea apunta el
  traceback antes de sospechar de la API.**
- **El error que no era de la API** (sesión 5, `01_errores.py`): pedir
  `max_tokens=99_999_999` no da un 400. Da un `ValueError` de Python — el SDK
  calcula que tardaría más de 10 minutos y **se niega a mandar la petición**.
  Ni red, ni servidor, ni factura. → Antes de buscar la causa, decide en cuál de
  las tres fronteras murió: tu máquina, la red, o el servidor.
- **La protección duplicada que multiplica** (sesión 5): si escribes tu propio
  reintento y dejas el del SDK (`max_retries=2` por defecto), 3 × 3 = **9
  peticiones** por una sola llamada. Solución: `max_retries=0` en el cliente
  cuando el reintento propio existe.
- **El corte que esconde el dato, por tercera vez** (sesión 6, `01_errores.py`):
  `e.message[:80]` partía el JSON del error justo antes del mensaje real, así que
  los casos 401 y 404 salían ilegibles. Ya había pasado con `texto.strip()[:30]`
  (nivel 1) y con la respuesta "cortada" de Sonnet. → **Cuando un dato salga
  truncado o raro, sospecha primero de tu propio `print`.** Y: antes de recortar
  un error, busca si el SDK te lo da ya parseado (`e.body`).
- **Costo estimado en vez de medido, cuarta vez** (sesión 7, `04_streaming.py`):
  el docstring anunciaba `~$0.02` y la corrida real dio **$0.038**. Nadie lo
  había medido; salió de mi cabeza al escribir el archivo. Es el mismo patrón del
  "Haiku cuesta 5x menos" (nivel 1) y de la fila inventada de la cuarta
  estrategia (nivel 2). → **Un número escrito en el material tiene que venir de
  una corrida, o venir marcado como estimación.**
- **Análisis mal atribuido (mío, no del estudiante):** concluí que borrar el turno
  `assistant` causó la brevedad, sin saber que él también había añadido una regla
  al `SYSTEM`. Lección: preguntar **qué se tocó** antes de interpretar. → L1.11
- **El cierre que se cumplió entero y dejó el trabajo sin salvar** (sesión 33,
  TEAPP paso 4): la regla decía *"si no hay hash, no hubo cierre"*, y había hash
  (`f015a01`). Pero `origin/main` seguía dos commits atrás: el paso entero vivía
  **solo en un disco**. → **Un control puede cumplirse entero y no comprobar lo
  que creías.** Es el mismo animal que "la prueba mide otra cosa de la que
  promete", ahora en el protocolo en vez del código. Se comprueba con
  `git status -sb`: si dice `ahead`, no terminaste.
- **La misma regla escrita en dos sitios, diciendo cosas contrarias** (sesión 33):
  al arreglar lo anterior, la skill decía "haz `push`" y los límites del propio
  agente lo tenían prohibido. No da error: **obedece a una de las dos sin manera
  de saber a cuál.** → Cuando corrijas una regla, pregunta **quién más la dice**.
- **"No hay nada que verificar", dicho sin haberlo buscado** (sesión 42, `T-058`):
  el cierre de la tarea decía *"nada que correr — es una cuenta externa"*. Había
  qué correr, era `nslookup`, y tardó dos segundos. **Ver el nombre en el panel
  del proveedor demuestra que el panel te lo enseña, no que el mundo lo resuelva.**
  → Es la sesión 36 (declarar hecho sin el testigo) con una vuelta peor: **el
  testigo ni se buscó.** Antes de escribir "no se puede verificar", la pregunta
  no es *"¿es mío este artefacto?"* sino **"¿qué podría mirar alguien de fuera?"**
- **El dato personal que no parecía un secreto** (sesión 42): al escribir el
  hallazgo de la IP, la IP completa entró en `PROGRESO.md` — **y este repo es
  público**. Se cazó mirando `git status` antes del commit. No era una llave ni
  un `.env`, que es justo por lo que casi pasa. → **En DNS la IP es efímera; en
  Git es para siempre.** La regla de "mira qué entra" no es solo para
  credenciales.
- **El síntoma bueno con la causa inventada** (sesión 56, mío): vi `decisions.md`
  sin commitear y lo llamé *"el control se cumplió entero y no comprobó lo que
  creías"* (sesión 33). Los `mtime` decían otra cosa: el archivo se escribió
  **veinte minutos después** del commit, y a la hora del cierre el árbol estaba
  limpio. → **Acertar el síntoma no vuelve buena la causa.** Y la causa se medía
  con `ls -l --time-style`, que no llegué a correr. Es la sesión 42 con el
  agravante de haber corregido ese mismo error ajeno esa misma mañana.
  📌 **Corolario que casi cuesta caro:** una lección sacada de un no-evento
  ensucia el archivo **más** que no escribir nada.
- **La cautela buena con el dueño equivocado** (sesión 57, mío): escribí que la
  ventana nocturna no debía arrancar *"porque apagar rompe la cuenta dinero ÷ horas
  de `A-018`"*. El daño era real pero de **`T-067`**: lo que `A-018` tiene vivo son
  relojes (`h1`, `h2 − h1`), y esos no dependen de que la máquina esté encendida.
  → Es el hermano del error de la 56 (*síntoma bueno, causa inventada*): aquí el
  **riesgo** era bueno y el **experimento** al que se lo cobré, falso. Antes de
  frenar algo, pregunta **de quién es el daño**, no solo si el daño existe.
  📌 **Y el arreglo no fue matizar la línea:** se borró y se escribió por qué era
  falsa. *Una regla con un asterisco debajo se lee como regla; nadie baja al
  asterisco.*
- **Dos reglas mías que se contradecían, y las cazó él** (sesión 57): una decía
  *"la ventana arranca cuando suene la alarma"* y otra *"hoy se apaga a las 23:00"*.
  No se pueden cumplir las dos. → Lo importante no es el fallo, es **cómo lo trajo**:
  como choque, y **con el matiz que lo resolvía en la mano, sin meterlo por su
  cuenta**. Por eso se corrigió la regla en vez de parchearse. Es el mismo gesto de
  *"escríbeme un ejemplo primero"*: traer el problema entero, no media solución.
- **El aviso que valía para un humano y no para una máquina** (sesión 57). El
  freno de la 55 era *"Detener, nunca Terminar"* — escrito para alguien **leyendo
  un menú**. Al automatizar el apagado aparece el mismo par como **ajuste** de la
  instancia (`stop` / `terminate`), y ahí **no hay nadie leyendo nada**: en
  `terminate`, la pieza destruye máquina y disco **la primera noche que funcione,
  por funcionar bien**. → **Un control escrito para un humano no protege a un
  programa.** Al automatizar un gesto, vuelve a preguntar qué lo hacía seguro.
- **La bandera equivocada en un comando que yo dicté** (sesión 57, mío): di
  `shutdown -h`; AWS documenta que `halt` **no** dispara el comportamiento de
  apagado y deja la instancia *"corriendo"* para la factura — muerta por dentro,
  viva para el cobro, y **sin ningún síntoma visible desde fuera**. La otra terminal
  puso `-P`. → **Un comando dictado también es material sin verificar.** Y el modo
  de fallo es el peor: silencioso y caro.
- **El resumen que se come el testigo** (sesión 57, tercera vez en cuatro sesiones).
  `T-074` exigía mirar la consola durante el primer apagado; el resumen hablado dijo
  *"se apaga sola"* y siguió. Y *"entrar por SSH usando la IP fija"* llegó como
  *"entra por la IP"* — **sin la palabra SSH**, que era la que lo hacía cierto.
  Medido: por HTTPS la IP da `000` **incluso saltándose el certificado**, porque el
  handshake no llega a ocurrir. Seguir el atajo habría dado un **rojo falso** en la
  medición de mañana. → **El documento y el resumen no son el mismo artefacto, y el
  que se lee es el resumen.**
- **Un desfase que nunca fue del instrumento** (sesión 57). De la lectura 4 se
  concluyó *"la pantalla va ~20 h por detrás"*. La lectura 6 lo desmiente: el
  desfase pasó de **−19,7 h a +2,7 h**, y **un instrumento no se adelanta a sí
  mismo**. Era el relleno inicial de una cuenta recién abierta, no una propiedad.
  → **Una constante medida una sola vez no es una constante.** Estaba marcado como
  *aritmética de lista*, y por eso murió limpio en vez de contaminar `T-067`.
- **El criterio infalsable justo donde importa** (sesión 57). La guardia decía
  *"alarma rota exige ≥12 h de silencio DESPUÉS de que el importe sea visible"*.
  Si lo que está roto es el propio presupuesto, el importe **nunca** es visible y la
  guardia **nunca arranca**: la alarma no se puede declarar rota **en el modo de
  fallo más probable**. → **Toda espera necesita un reloj de fuera.** Es `D-041`
  (la espera con fecha de caducidad) que hay que aplicar también **dentro** del
  criterio, no solo a la conversación.
- **Resté una hora local de una hora UTC** (sesión 58, mío). Dije *"el testigo vence
  en 1 h 40"* y faltaban **5 h 30**: tomé el `17:2x` de una línea y el `18:00` de
  otra, y las dos eran ciertas **en zonas distintas**. Lo cazó él —*"sus propias
  horas dan otra cosa"*— y no lo dio por bueno en ninguna dirección. → Es `D-046`
  (la zona horaria escrita **dentro** de la pieza, para que no dependa de un ajuste
  que vive fuera) cometido a mano en la misma conversación que lo redactaba.
  📌 **Una hora sin zona no es una hora.** Y el daño real no era la resta: era que
  metía prisa a un despliegue que tenía holgura de sobra.
- **Una cita que se propaga por parecer verificada** (sesión 58). `[L-013]` estaba
  mal citada en **16 sitios** de TEAPP con **tres significados distintos**, y
  ninguno era el suyo. La frase que se quería citar existe y es correcta: es
  **`LM.13`**, de este repo. Una letra entre dos espacios de nombres —`LM.nn` para
  las lecciones de método, `L-nnn` para las de TEAPP— y ninguna regla escrita que
  los separara. 🔑 **La convención ya existía de hecho** (19 usos correctos) y no
  protegió de nada **porque no estaba escrita**: *un acuerdo que depende de que
  nadie se despiste no es un acuerdo, es una racha.* → Es el bicho de la sesión 33
  (la misma cosa escrita en dos sitios diciendo cosas contrarias) mudado **a las
  citas**. Y una cita que ya aparece en muchos sitios tranquiliza igual que un
  verde: deja de auditarse.
- **Un puntero sin repo es medio puntero** (sesión 58, mío). Le dije *"eso ya salió
  en la sesión 48"* sin decir **en qué archivo**. `LM.15` vive aquí, no en TEAPP; lo
  buscó en el suyo y no estaba. → El mismo defecto que estábamos arreglando ese día,
  cometido al señalarlo.
- **El control que dicta cómo se escribe el archivo que vigila** (sesión 58, y es
  nuevo). Para proteger dos punteros corregidos en `progress.md` se escribió un
  control que **contaba apariciones** de `[LM.13]`. El `session-closer` mencionó la
  colisión en prosa, el contador subió a 4 y el control se puso rojo — legítimamente,
  pero por el motivo equivocado: no distinguía *"alguien revirtió los punteros"* de
  *"alguien escribió sobre ellos"*. **El closer reescribió su propio texto evitando
  nombrar los identificadores para dejarlo en verde**, y el resultado fue una entrada
  sobre una colisión de identificadores **que no puede nombrarlos**. 🔑 **Es peor que
  un rojo falso: un rojo falso da un dato malo; esto deforma el artefacto medido.**
  → Un control se escribe contra **la condición** que quiere proteger (las dos frases
  concretas), no contra un síntoma contable que el texto humano puede mover.
- **Arreglar un bloque no lo inmuniza: lo vuelve más peligroso** (sesión 58, suya y
  es la lección madre del día). El bloque final de `install.sh` ya había sido
  auditado el día 05 (`L-017`) por titularse *"terminado = visto funcionando"* y
  mirar solo `is-active`. Cuatro días después se le añadió una comprobación nueva
  **y se reintrodujo el atajo exacto**, bajo un comentario todavía más enfático.
  🔑 **La cicatriz de haber sido auditado avala también las líneas que se añadan
  después.** → Es *nadie audita un verde* (`LM.15`, sesión 48) con el mecanismo por
  fin explicado: **un control sin estrenar da miedo y se revisa; uno en verde
  tranquiliza y ya no lo mira nadie.** La pregunta que queda: leer el comentario y
  preguntarle a la comprobación *"¿te pondrías roja en el caso que este comentario
  acaba de describir?"*.
- **Propuse encender un experimento que llevaba cuatro días corriendo** (sesión 59,
  mío). Recomendé bajar el umbral del presupuesto *"para ver el freno morder"*:
  llevaba en **0,01 US$ desde el día 6**, contra 0,37 gastados y sin un solo correo.
  Mi rama *"si no salta en 24 h, el campo está clavado en 0"* **era el presente**.
  → Es `LM.20` (la respuesta ya estaba escrita y nadie la alcanzó) con un agravante:
  el coste no era solo perder el tiempo, era **destruir la línea base** y añadir una
  tarea con caducidad. 🔑 Y lo que lo mataba era aritmética, no configuración:
  **contra `0,00` no hay umbral positivo que dispare.**
- **Abrí el archivo, leí una rama y la llamé el mecanismo** (sesión 59, mío). Dije
  que un usuario inventado cuenta como fallo *por `api.py:482`*. Un nombre **bien
  formado** no pasa por ahí: `accounts.verify` **devuelve `False`** para quien no
  existe (`accounts.py:280`) y el fallo se registra en la **494**. La conclusión era
  correcta y la causa estaba **una rama al lado** — sesión 56 en pequeño.
  📌 **Y es de segundo orden respecto a ayer:** ayer la lección fue *no prescribas
  sobre un archivo que no abriste*. Hoy resulta que abrirlo no basta. Suyo, y es la
  mejor formulación: *«no lo abrí» se rompe fácil; «lo abrí, luego lo sé» no.*
- **Una tabla que nunca se encogió mandó a hacer una tarea cerrada** (sesión 59).
  Propusieron arrancar por `T-060b`, **cerrada el 08**; la tabla de `[A-014]` en
  `assumptions.md:1207` seguía nombrándola como lo que faltaba. Esa tabla es del
  **07**: la entrada encogió tres veces y **cada encogimiento se escribió como un
  bloque nuevo DEBAJO**. → **En un archivo que crece por enmiendas, el texto más
  viejo se queda arriba, que es donde cae el ojo primero.** No es `LM.20` (allí lo
  cierto está escrito y nadie lo alcanza): aquí **sí se alcanza, primero, y es
  falso**. → `LM.24`
- **Predije la salida de un instrumento que la pieza tenía apagado** (sesión 59,
  mío). Dije que `list-timers` traería `LAST` y `PASSED` llenos; con
  `Persistent=false` systemd **no escribe la marca de disparo**, que es el archivo
  que `list-timers` lee. → Suyo, `L-035`: **un ajuste que apaga la memoria de una
  pieza apaga también los instrumentos que la leen, y eso no aparece en el
  comentario que justifica el ajuste.**
- **Una afirmación que no venía de ninguna parte, con corchetes puestos después**
  (sesión 60). El cierre escribió en `progress.md` —campo `siguiente acción`, el
  primero que se lee al abrir— que *"no hace falta encenderla a mano, el apagado y
  encendido ya son automáticos `[D-045]`/`[D-046]`"*. **`D-045` dice lo contrario
  y a propósito.** No fue una cita mal numerada como la de la sesión 58: **la
  frase se fabricó al comprimir**, y los identificadores se le pegaron encima como
  armadura. Estaba en **tres sitios**, replicada dentro del propio texto del closer.
  🔑 **La dirección del error es el diagnóstico:** lo inventado fue *la versión
  cómoda* —"no hace falta hacer nada"—, nunca la incómoda. **Una frase que no le
  pide nada al lector no ofrece resistencia mientras se escribe.** → `LM.26`.
  📌 Y no hacía falta abrir ningún archivo para verlo: **nada dentro de la máquina
  puede encenderla, porque apagada no hay nada dentro corriendo.**
- **Una tarea muerta volvió con una factura pegada** (sesión 67). `T-074` llevaba
  **dos traspasos** viajando como pendiente estando cerrada desde el 2026-08-10
  con testigo en el journal. El segundo día llegó **de prioridad nº 1** y con una
  consecuencia inventada —*"la máquina encendida se come el plan gratuito"*— que
  no salía de ninguna corrida: medido, `443` y `22` **mudos los dos**, y con la
  EC2 apagada quien cobra son la IP elástica y el EBS, **no las horas de
  instancia**. → **`LM.30`: la urgencia no se audita, se obedece.** Y el
  mecanismo: la caza del día anterior **vivió solo en el chat**, el puntero viejo
  se quedó en el disco, y el arranque siguiente lo volvió a servir.
- **El instrumento que certifica una identidad que solo él define** (sesión 67).
  Iban a averiguar de quién era cada llave preguntándoselo al guion **que estaban
  auditando**. Eso sale verde pase lo que pase. → **La identidad tiene que venir
  de fuera** (la consola, leída antes de correr). Es `T-060b` otra vez: *sin nada
  escuchando en el 8000, "cerrado" salía igual con el cortafuegos abierto*.
- **Un `.env` que nadie lee** (sesión 67). `check_api_key.py` no carga ningún
  `.env`: termina en `sys.exit(main(os.environ))`. Editar el archivo y correrlo
  habría dado *falta la llave* — **un rojo con la causa equivocada** en la primera
  corrida real de la pieza. → Antes de preparar una prueba, mira **de dónde lee**
  el programa, no de dónde crees que lee.
- **Un tope leído como si fuera un reloj** (sesión 80, mío, y es especie nueva).
  Propuse que la traza escribiera el reparto `connect`/`write`/`pool`/`read`
  *"porque la arquitectura ya piensa en fases y el registro no las escribe"*. Esos
  cuatro nombres son `anthropic.Timeout(...)`: un **presupuesto que se le entrega a
  la librería**, no un cronómetro. Los números **no existen** — `httpx` devuelve un
  solo `elapsed`, el total. → **Declarar cuánto se le permite durar a algo no es
  haber medido cuánto duró.** 📌 Y el agravante: **la tabla de las cuatro fases la
  había abierto y leído entera** (`tools.py:182-185`). Es la sesión 59 (*abrirlo no
  basta*) subida un piso: **lo leí bien y lo clasifiqué mal.**
  🔑 La frase era **cierta y venenosa**: *"el registro no las escribe"* se lee como
  *"están ahí, solo falta apuntarlos"*. **Una afirmación verdadera puede mandar a
  construir algo imposible si el lector completa la mitad que no dice.**
- **`Juan` y `juan`: una persona en Windows, dos en Linux** (sesión 33, análisis
  previo del paso 4). Si un nombre escrito por el usuario se vuelve un nombre de
  archivo sin normalizar, el marcador se parte en dos al desplegar — **sin ningún
  error y con todos los tests locales en verde**. → Normalizar (minúsculas +
  `strip`) antes de que el texto toque el disco. **Los bugs que no puedes ver en
  tu máquina son los caros.**
- **Una cerradura que hay que acordarse de invocar sigue siendo una advertencia**
  (sesión 83, y es la lección madre del día). El día anterior `PI-8` era un
  comentario y se convirtió en función, `sentences_are_invented()`. Bien probada,
  honesta sobre su alcance… y llamada **solo desde tres tests con registros hechos a
  mano**. La promoción de un corpus era un `mv` manual, así que **correr la cerradura
  era un acto de acordarse** — y en `eval_rubric.py:89` ya había una frase dándolo
  por hecho en presente. 🔑 **El mismo defecto con una capa más de pintura**, y la
  pintura es lo peligroso: un comentario da miedo, una función tranquiliza (`LM.15`).
  → Un control se echa sobre **la carpeta entera con un `glob`**, no sobre los
  registros que alguien le pase. Y el patrón ya estaba en casa: el portero sobre
  `data/` de `T-071`, sesión 49.
- **Un criterio de conservación que se evalúa DESPUÉS deja la evidencia esperando en
  el sitio menos duradero** (sesión 83). *"Se guarda el corpus cuya rúbrica ya no
  existe en producción"* se comprueba solo y no se estira — pero en el momento de
  crear un corpus la rúbrica está viva **por definición**, así que nada se guarda
  nunca al nacer. Se guardaría más tarde, cuando alguien caiga; y mientras tanto el
  archivo espera en `data/`, ignorado por Git y en un solo disco. 🔑 **Su valor solo
  se reconoce a toro pasado, y el reconocimiento depende de que alguien se acuerde.**
  → El disparador se pega a un evento que **ocurre seguro y se nota seguro**: el
  commit que mueve `MODEL` o `GRAMMAR_RUBRIC`. Mismo patrón que `[D-081]`.
- **Un criterio que nombra un eje y olvida el otro** (sesión 83). El criterio
  propuesto colgaba de *"si la rúbrica sigue viva, la corrida se puede repetir"* —
  cierto **solo si todo lo demás está quieto**, y `[D-049]` va a mover el modelo tres
  veces a propósito. El corpus que más iba a doler perder (la línea base de Opus,
  para comparar el descenso) era justo el que el criterio dejaba fuera.
- **10 de 10 rotas no es un resultado, es la selección** (sesión 83). El corpus del
  diagnóstico tenía las diez filas rotas porque **se escogieron las que habían
  fallado**. Sin nada en el nombre que lo dijera, es un **100% de fallo esperando a
  que alguien lo divida** — y eso no lo tapan ni el modelo, ni la fecha, ni el hash.
  Es `[L-071]` (cuadrar contra un agregado no es cuadrar) con el sesgo dentro del
  propio conjunto. → cuarto eje del nombre: `full` / `pick`.
- **Dos booleanos dejan una combinación imposible, y alguien la leerá como un dato**
  (sesión 83). La traza escribía `correct: bool` y mezclaba dos causas **opuestas**:
  el juez rompió el formato, o el alumno se equivocó. El arreglo natural —añadir un
  segundo booleano y cruzarlos— deja tres estados válidos y uno imposible.
  → **Un campo que diga QUIÉN falló**, con sus tres estados, naciendo donde la
  función ya los distinguía; y el booleano viejo degradado a **propiedad derivada**,
  que es lo único que garantiza que no discrepen.
- **El campo que sobra y el campo que se le parece** (sesión 83, y es el aviso que
  evitó el daño). `correct` aparecía en cuatro sitios y **solo uno era redundante**:
  el de la traza. Los otros alimentan `record_practice`, o sea **el marcador del
  alumno**. Un barrido de `correct` habría cambiado la nota de la gente **sin lanzar
  un error**, porque un marcador equivocado sigue pareciendo un marcador.
  → Antes de retirar un nombre, mira **quién más lo consume**, no cuántas veces sale.
- **Leí un listado y conté dos filas como una** (sesión 83, mío). Dije que el corpus
  había crecido de `744` a `2217` bytes; los `744` eran de `accounts.json`, otra fila
  del mismo `ls`. Lo cazó la otra terminal. No movía la conclusión, pero es la misma
  familia de la sesión 80: **mirar el sitio correcto y clasificar mal lo que hay**.
  📌 Y en la misma revisión llegó una corrección que **no lo era** —citar la línea
  196 en vez de la 188, cuando el `def` está en la 188 y el `return` en la 196, las
  dos buenas—. Se anota porque **una corrección falsa que entra al registro pesa
  igual que un error de verdad**, y nadie vuelve a auditarla.

---

## Decisiones tomadas

- **Python antes que TypeScript.** Python tiene los ejemplos y librerías de agentes más
  maduros; TypeScript entra cuando lleguemos a la parte web (**nivel 6**).
- **Evaluación antes que TypeScript** (decidido en la sesión 6, a petición del
  estudiante). Evaluar es el concepto difícil del curso. Aprenderlo al mismo
  tiempo que un lenguaje nuevo sería **cargar dos cosas nuevas a la vez**, que es
  justo lo que este recorrido evita en todos los demás niveles. Así se mide en
  Python —que ya maneja— y TypeScript entra pegado al momento en que tiene razón
  de ser: el nivel 7, donde hay navegador.
- **Rúbricas y LLM-as-judge se nombran aparte de los evals deterministas**
  (nivel 5). No son lo mismo: un `if` comprueba "¿llamó la herramienta correcta?";
  "¿respetó el dialecto?" necesita una escala y otro modelo juzgando. El plan
  antes decía solo "evals, casos de prueba, regresiones" y el segundo tipo
  quedaba fuera.
- **Observabilidad es una pieza propia del nivel 7**, no un ítem de lista.
  Evaluación pregunta *"¿funciona?"* antes de soltarlo; observabilidad pregunta
  *"¿qué está haciendo ahora?"* con usuarios encima. El `registro.jsonl` del
  nivel 4 es su primer ladrillo.
- **Un nivel a la vez.** No se escriben lecciones futuras por adelantado, para que el
  material se ajuste al ritmo real del estudiante.
- **El agente del clima como primer agente** (nivel 3), porque es el caso mínimo donde
  el modelo no puede responder solo y obliga a construir el bucle completo.
