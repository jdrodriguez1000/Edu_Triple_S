"""
Nivel 4.2 — Reintentos y timeouts: lo que el SDK ya hace por ti.

Casi todo el mundo escribe su propia funcion de reintentos sin saber que el
SDK ya trae una. Antes de escribir la tuya, hay que saber que hace la de ellos,
porque si no terminas con reintentos DENTRO de reintentos: pides 3 y ejecutas 9.

Aqui medimos con cronometro cuatro comportamientos:
  A. Un error temporal SI se reintenta (y cuanto tarda cada intento).
  B. Un error permanente NO se reintenta (falla de una).
  C. Un timeout tambien cuenta como temporal -> se reintenta -> el tiempo total
     no es tu timeout, es tu timeout MULTIPLICADO.
  D. Como se escribe un reintento propio, y cuando vale la pena.

Correr con:  python 02_reintentos.py
Cuesta:      casi $0.00 (una sola llamada real al final, de unas decenas de tokens)
Tarda:       ~30 segundos. La mayor parte es el programa esperando a proposito.
"""

import random
import sys
import time
from pathlib import Path

import anthropic
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

MODELO = "claude-opus-5"
INEXISTENTE = "https://api.este-dominio-no-existe-jamas.invalid"


def cronometrar(etiqueta, funcion):
    """Corre algo, mide cuanto tardo y dice como termino."""
    inicio = time.monotonic()
    try:
        funcion()
        resultado = "termino bien"
    except Exception as e:
        resultado = type(e).__name__
    segundos = time.monotonic() - inicio
    print(f"  {etiqueta:<28} {segundos:6.2f}s   {resultado}")
    return segundos


print("\n=== A. Error temporal: el SDK reintenta solo")
print("Mismo error (no hay servidor), cambiando cuantos reintentos permitimos.\n")

for reintentos in (0, 1, 2, 3):
    cliente = anthropic.Anthropic(
        base_url=INEXISTENTE, max_retries=reintentos, timeout=5.0
    )
    cronometrar(
        f"max_retries={reintentos}",
        lambda c=cliente: c.messages.create(
            model=MODELO, max_tokens=5,
            messages=[{"role": "user", "content": "hola"}],
        ),
    )

print("""
  El error es el mismo en los cuatro. Lo que crece es el TIEMPO, porque entre
  intento e intento el SDK espera cada vez un poco mas (espera exponencial).
  Fijate que no imprimio nada mientras reintentaba: lo hace en silencio.
  Con max_retries=2 (el valor por defecto) tu programa hace 3 peticiones,
  no 1. Eso ya estaba pasando en TODOS los scripts de los niveles 1, 2 y 3.
""")


print("\n=== B. Error permanente: el SDK NO reintenta")
print("Misma configuracion generosa, pero la llave esta mala.\n")

cliente_llave_mala = anthropic.Anthropic(
    api_key="sk-ant-esta-llave-no-existe", max_retries=5, timeout=10.0
)
cronometrar(
    "max_retries=5, llave mala",
    lambda: cliente_llave_mala.messages.create(
        model=MODELO, max_tokens=5,
        messages=[{"role": "user", "content": "hola"}],
    ),
)

print("""
  Pedimos 5 reintentos y tardo lo que tarda UNA peticion. El SDK sabe que un
  401 no se arregla esperando. Reintenta 408, 409, 429, 5xx y errores de red.
  Todo lo demas lo lanza de una.
""")


print("\n=== C. El timeout se multiplica")
print("timeout=1s significa 1s POR INTENTO, no 1s en total.\n")

for reintentos in (0, 2):
    cliente = anthropic.Anthropic(
        base_url="https://10.255.255.1", max_retries=reintentos, timeout=1.0
    )
    cronometrar(
        f"timeout=1s, max_retries={reintentos}",
        lambda c=cliente: c.messages.create(
            model=MODELO, max_tokens=5,
            messages=[{"role": "user", "content": "hola"}],
        ),
    )

print("""
  (10.255.255.1 es una direccion que no responde: los paquetes se van y nadie
  contesta nunca. Por eso el timeout es el que corta, no el servidor.)

  Peor de los casos = timeout x (max_retries + 1) + las esperas entre intentos.
  Con los valores por DEFECTO del SDK eso es 10 minutos x 3 = media hora.
  Si tu agente tiene que responderle a un usuario, media hora no es un timeout:
  es un cuelgue. Poner un timeout corto es harness.
""")


# ---------------------------------------------------------------------------
# D. Tu propio reintento.
#
# El SDK reintenta la LLAMADA. Tu reintentas la OPERACION. No son lo mismo:
# el SDK no sabe que tu vuelta del bucle agentico incluye ejecutar una
# herramienta, escribir un log y descontar presupuesto.
#
# Reglas de esta funcion:
#   - solo reintenta lo que se puede reintentar
#   - espera cada vez mas (2s, 4s, 8s...) para no empeorar la saturacion
#   - le suma un numerito al azar ("jitter") para que mil programas que
#     fallaron al mismo tiempo no vuelvan todos juntos en el mismo segundo
#   - y avisa. El silencio del SDK esta bien para una libreria; en TU agente,
#     un reintento que nadie ve es un costo que nadie explica.
# ---------------------------------------------------------------------------
REINTENTABLES = (
    anthropic.RateLimitError,
    anthropic.InternalServerError,
    anthropic.APIConnectionError,   # incluye APITimeoutError
)


def con_reintentos(funcion, intentos=3, espera_base=2.0):
    for intento in range(1, intentos + 1):
        try:
            return funcion()
        except REINTENTABLES as e:
            if intento == intentos:
                print(f"     se acabaron los intentos ({type(e).__name__})")
                raise
            espera = espera_base * (2 ** (intento - 1)) + random.uniform(0, 1)
            print(f"     intento {intento} fallo ({type(e).__name__}), "
                  f"espero {espera:.1f}s")
            time.sleep(espera)


print("\n=== D. Reintento propio, sobre una llamada que SI funciona")

cliente = anthropic.Anthropic(max_retries=0, timeout=30.0)

respuesta = con_reintentos(
    lambda: cliente.messages.create(
        model=MODELO,
        max_tokens=300,   # con 100 la respuesta salia cortada: leccion L1.1
        system="Responde en una sola frase corta, en espanol de Colombia.",
        messages=[{"role": "user", "content": "Que es un timeout?"}],
    )
)

texto = next((b.text for b in respuesta.content if b.type == "text"), "(sin texto)")
print(f"  respuesta: {texto}")
print(f"  usage: {respuesta.usage.input_tokens} in / "
      f"{respuesta.usage.output_tokens} out   "
      f"stop_reason: {respuesta.stop_reason}")

print("""

Lectura del resultado
---------------------
1. El SDK ya reintentaba. Desde el nivel 1. max_retries=2 por defecto, o sea
   hasta 3 peticiones por cada create() que escribiste. Nunca lo viste porque
   nunca fallo nada.

2. Reintentar solo sirve para errores temporales, y el SDK ya distingue cuales
   son. No escribas tu propia lista de codigos HTTP: usa las clases de
   excepcion, que es lo que hicimos en REINTENTABLES.

3. El timeout es POR INTENTO. Tu presupuesto de paciencia real es
   timeout x (max_retries + 1). Los dos valores se eligen juntos, nunca solos.

4. Escribe tu propio reintento cuando lo que quieres repetir es mas que la
   llamada: una vuelta entera del bucle, con su herramienta y su log.
   Cuando pongas el tuyo, baja el del SDK (max_retries=0 o 1), o vas a
   multiplicar: 3 tuyos x 3 del SDK = 9 peticiones y el triple de factura.

5. La espera crece (2s, 4s, 8s) en vez de ser fija. Si el servidor esta
   saturado, volver cada segundo es empujar a alguien que ya se esta cayendo.
""")
