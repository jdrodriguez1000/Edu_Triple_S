"""
Nivel 0 — Verificación del entorno.

Revisa, en orden, las 4 cosas que tienen que estar bien antes de empezar:
  1. Version de Python
  2. Librerias instaladas
  3. La API key existe y se puede leer
  4. La API key funciona de verdad (hace una llamada minima)

Correr con:  python verificar.py
"""

import sys
from pathlib import Path

OK = "[OK]  "
ERR = "[FALTA]"


def fallar(mensaje: str, solucion: str) -> None:
    """Imprime el problema y cómo arreglarlo, y detiene el programa."""
    print(f"{ERR} {mensaje}")
    print(f"        -> {solucion}\n")
    sys.exit(1)


# --- 1. Python -------------------------------------------------------------
if sys.version_info < (3, 10):
    fallar(
        f"Python {sys.version_info.major}.{sys.version_info.minor} es muy viejo.",
        "Instala Python 3.10 o superior desde python.org",
    )
print(f"{OK} Python {sys.version_info.major}.{sys.version_info.minor}")


# --- 2. Librerías ----------------------------------------------------------
try:
    import anthropic
except ImportError:
    fallar(
        "La libreria 'anthropic' no esta instalada.",
        "Activa el entorno virtual y corre: pip install -r requirements.txt",
    )

try:
    from dotenv import load_dotenv
except ImportError:
    fallar(
        "La libreria 'python-dotenv' no esta instalada.",
        "Corre: pip install -r requirements.txt",
    )

print(f"{OK} Librerias instaladas (anthropic {anthropic.__version__})")


# --- 3. La API key ---------------------------------------------------------
import os  # noqa: E402  (lo importamos aquí a propósito, después de validar dotenv)

# El .env vive en la carpeta de arriba (la raíz del proyecto), no en 00-setup.
raiz = Path(__file__).resolve().parent.parent
ruta_env = raiz / ".env"

if not ruta_env.exists():
    fallar(
        f"No existe el archivo {ruta_env}",
        "Desde la raiz corre: Copy-Item .env.example .env  y pega tu llave adentro",
    )

load_dotenv(ruta_env)
api_key = os.environ.get("ANTHROPIC_API_KEY", "")

if not api_key or "pega-aqui" in api_key:
    fallar(
        "ANTHROPIC_API_KEY esta vacia o todavia tiene el texto de ejemplo.",
        f"Abre {ruta_env} y pega tu llave real de console.anthropic.com",
    )

# Nunca imprimimos la llave completa: solo lo suficiente para reconocerla.
print(f"{OK} API key encontrada ({api_key[:14]}...{api_key[-4:]})")


# --- 4. La llamada real ----------------------------------------------------
print("       Probando la conexion con la API...")

# Anthropic() lee ANTHROPIC_API_KEY del entorno automáticamente.
cliente = anthropic.Anthropic()

try:
    respuesta = cliente.messages.create(
        model="claude-haiku-4-5",  # el más barato: esto es solo un ping
        max_tokens=16,
        messages=[{"role": "user", "content": "Responde solo con la palabra: listo"}],
    )
except anthropic.AuthenticationError:
    fallar(
        "La API key fue rechazada por el servidor.",
        "Verifica que la copiaste completa, sin espacios, desde console.anthropic.com",
    )
except anthropic.PermissionDeniedError:
    fallar(
        "La llave es valida pero no tiene permisos / saldo.",
        "Revisa en console.anthropic.com que tu cuenta tenga credito cargado",
    )
except anthropic.APIConnectionError:
    fallar(
        "No se pudo conectar con api.anthropic.com",
        "Revisa tu conexion a internet, VPN o firewall corporativo",
    )

texto = next(b.text for b in respuesta.content if b.type == "text")
print(f"{OK} La API respondio: {texto.strip()!r}")
print(f"       Tokens usados: {respuesta.usage.input_tokens} entrada / "
      f"{respuesta.usage.output_tokens} salida")

print("\n=== TODO LISTO. Pasa a la carpeta 01-primera-llamada ===")
