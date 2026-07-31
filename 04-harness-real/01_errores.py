"""
Nivel 4.1 — Los errores tienen nombre y apellido.

Hasta ahora, cuando algo fallaba, el programa reventaba con un traceback y ya.
Aqui provocamos errores A PROPOSITO, cuatro distintos, y miramos que tipo de
excepcion lanza el SDK en cada caso.

Por que importa: no todos los errores se arreglan igual.
  - Unos se arreglan REINTENTANDO (la red se cayo un segundo, el servidor esta
    saturado). Reintentar tiene sentido.
  - Otros NO se arreglan nunca reintentando (tu llave esta mala, el modelo no
    existe, tu peticion esta mal armada). Reintentar solo gasta tiempo.

Saber cual es cual es la mitad del nivel 4.

Correr con:  python 01_errores.py
Cuesta:      $0.00 — ninguna de estas 5 peticiones llega a generar tokens.
"""

import sys
from pathlib import Path

import anthropic
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

MODELO = "claude-opus-5"


def motivo(e) -> str:
    """
    Saca el mensaje LIMPIO de un error del servidor.

    e.message trae el JSON crudo entero:
        "Error code: 401 - {'type': 'error', 'error': {'type': ..., 'message': ...}}"
    Cortarlo con [:80] parte el JSON a la mitad y te deja justo sin el dato util.
    El SDK ya te dio el JSON parseado en e.body: solo hay que entrar a buscarlo.

    Ademas devolvemos el request_id: ese es el numero que le das a soporte de
    Anthropic si algun dia tienes que reportar un problema. Sin el no pueden
    buscar tu peticion.
    """
    cuerpo = getattr(e, "body", None)
    if isinstance(cuerpo, dict):
        texto = cuerpo.get("error", {}).get("message", "")
        pedido = cuerpo.get("request_id")
        if texto:
            return f"{texto}" + (f"  [request_id: {pedido}]" if pedido else "")
    # Si el cuerpo no vino como esperabamos, mejor el mensaje crudo que nada.
    return e.message


def intentar(titulo: str, funcion) -> None:
    """
    Ejecuta una funcion y clasifica lo que salga mal.

    OJO al orden de los except: van de lo MAS especifico a lo mas general.
    Python entra al primer except que coincida. Si pusieras APIStatusError
    arriba, se tragaria los 401, 404 y 400 y nunca sabrias cual fue.
    """
    print(f"\n=== {titulo}")
    try:
        respuesta = funcion()
        print(f"    No fallo. stop_reason={respuesta.stop_reason}")

    except ValueError as e:
        # Ni siquiera es un error de anthropic: es Python puro. El SDK reviso
        # tu peticion ANTES de mandarla y se nego. No hubo red, no hubo cuenta.
        print("    ValueError — el SDK se nego a mandar la peticion")
        print(f"    reintentar? NO, no salio de tu maquina. "
              f"{str(e).split('. See')[0]}")

    except anthropic.AuthenticationError as e:
        print("    AuthenticationError (HTTP 401) — la llave no sirve")
        print(f"    reintentar? NO. {motivo(e)}")

    except anthropic.NotFoundError as e:
        print("    NotFoundError (HTTP 404) — ese modelo o esa ruta no existe")
        print(f"    reintentar? NO. {motivo(e)}")

    except anthropic.BadRequestError as e:
        print("    BadRequestError (HTTP 400) — tu peticion esta mal armada")
        print(f"    reintentar? NO. {motivo(e)}")

    except anthropic.RateLimitError as e:
        print("    RateLimitError (HTTP 429) — vas muy rapido")
        print(f"    reintentar? SI, esperando. {motivo(e)}")

    except anthropic.APIStatusError as e:
        # Red de seguridad: cualquier otra respuesta HTTP que no sea 2xx.
        # Aqui caen los 500 y 529 del servidor de Anthropic, que SI se reintentan.
        print(f"    APIStatusError HTTP {e.status_code} — no lo previmos")
        print(f"    reintentar? Si es 5xx, si. {motivo(e)}")

    except anthropic.APIConnectionError as e:
        # Este NO es hermano de APIStatusError: aqui nunca hubo respuesta HTTP.
        # El paquete no llego a ningun lado. No hay codigo de estado que mirar.
        print("    APIConnectionError — no hubo respuesta, ni siquiera un error")
        print(f"    reintentar? SI. causa: {type(e.__cause__).__name__}")


# ---------------------------------------------------------------------------
# ERROR 1 — la llave esta mala.
# Fijate que el cliente se construye sin problema. Nadie valida la llave hasta
# que sale la primera peticion. Un cliente creado no es un cliente que funciona.
# ---------------------------------------------------------------------------
def llave_mala():
    cliente = anthropic.Anthropic(api_key="sk-ant-esta-llave-no-existe")
    return cliente.messages.create(
        model=MODELO,
        max_tokens=10,
        messages=[{"role": "user", "content": "hola"}],
    )


# ---------------------------------------------------------------------------
# ERROR 2 — el modelo no existe.
# Tipico al copiar un nombre de un blog viejo, o al escribirlo con puntos:
# "claude-opus-4.5" en vez de "claude-opus-4-5".
# ---------------------------------------------------------------------------
def modelo_inventado():
    cliente = anthropic.Anthropic()
    return cliente.messages.create(
        model="claude-opus-9-mil",
        max_tokens=10,
        messages=[{"role": "user", "content": "hola"}],
    )


# ---------------------------------------------------------------------------
# ERROR 3 — la peticion es tan grande que el SDK ni la manda.
# Pedimos 99 millones de tokens de salida. El SDK calcula cuanto tardaria eso,
# ve que pasa de 10 minutos, y se niega. No hay peticion, no hay servidor.
# ---------------------------------------------------------------------------
def peticion_absurda():
    cliente = anthropic.Anthropic()
    return cliente.messages.create(
        model=MODELO,
        max_tokens=99_999_999,
        messages=[{"role": "user", "content": "hola"}],
    )


# ---------------------------------------------------------------------------
# ERROR 4 — la peticion sale, pero el servidor la rechaza.
# 'temperature' existia en modelos viejos y en Opus 5 ya no. El SDK no sabe
# eso (es un dato del modelo, no del SDK), asi que la manda y el 400 vuelve
# desde el servidor. Compara con el caso 3: alli el filtro fue local.
# ---------------------------------------------------------------------------
def parametro_viejo():
    cliente = anthropic.Anthropic()
    return cliente.messages.create(
        model=MODELO,
        max_tokens=10,
        temperature=0.5,
        messages=[{"role": "user", "content": "hola"}],
    )


# ---------------------------------------------------------------------------
# ERROR 5 — no hay internet (lo simulamos apuntando a un servidor inexistente).
# Esto es lo que veria tu agente del nivel 3 si se cae el wifi.
#
# max_retries=0 a proposito: por defecto el SDK reintenta este tipo de error
# 2 veces mas, y el script se quedaria callado unos segundos antes de fallar.
# Lo apagamos para verlo fallar de una. En el script 2 lo prendemos de nuevo.
# ---------------------------------------------------------------------------
def sin_red():
    cliente = anthropic.Anthropic(
        base_url="https://api.este-dominio-no-existe-jamas.invalid",
        max_retries=0,
        timeout=5.0,
    )
    return cliente.messages.create(
        model=MODELO,
        max_tokens=10,
        messages=[{"role": "user", "content": "hola"}],
    )


intentar("1. Llave mala", llave_mala)
intentar("2. Modelo que no existe", modelo_inventado)
intentar("3. max_tokens absurdo", peticion_absurda)
intentar("4. Parametro que este modelo ya no acepta", parametro_viejo)
intentar("5. Sin red (dominio inexistente)", sin_red)

print("""

Lectura del resultado
---------------------
Cinco fallas, cinco maneras distintas de fallar. Esa es la idea.

  ValueError            --   -> ni salio de tu maquina. Arregla el codigo.
  AuthenticationError   401  -> arregla la llave. Reintentar no sirve.
  NotFoundError         404  -> arregla el nombre. Reintentar no sirve.
  BadRequestError       400  -> arregla la peticion. Reintentar no sirve.
  RateLimitError        429  -> ESPERA y reintenta.
  InternalServerError   5xx  -> espera y reintenta (culpa del servidor).
  APIConnectionError     --  -> espera y reintenta (culpa de la red).

Los cuatro primeros son culpa TUYA y son permanentes: el minuto que viene van
a fallar igual. Los tres ultimos son temporales y ajenos.

Tres detalles que valen mas que la tabla:

1. Hay tres fronteras, no una. El caso 3 murio en TU MAQUINA (el SDK reviso
   antes de mandar). El caso 5 murio EN LA RED (nunca hubo servidor). Los
   casos 1, 2 y 4 murieron EN EL SERVIDOR (hubo respuesta, con codigo HTTP).
   Casi el mismo sintoma, tres sitios distintos donde buscar.

2. APIConnectionError NO tiene status_code. Los demas heredan de
   APIStatusError, que existe porque hubo una respuesta HTTP. En el caso 5
   nunca hubo respuesta. Por eso va en su propio except, y por eso si escribes
   'except anthropic.APIStatusError' creyendo que atrapa todo, el dia que se
   caiga el wifi tu programa revienta igual.

3. El orden de los except es el programa. Van de especifico a general.
   Si mueves APIStatusError arriba de todo, los casos 1, 2 y 4 caen ahi y
   pierdes la informacion que necesitabas para arreglarlos.
""")
