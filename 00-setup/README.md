# Nivel 0 — Setup

Objetivo: dejar el entorno listo y verificado. Cuando `verificar.py` te diga
"TODO LISTO", pasas al nivel 1.

Ya tienes instalado Python 3.12, Node 25 y Git. No hay que instalar nada de eso.

---

## Paso 1 — Conseguir la API key

1. Entra a **https://console.anthropic.com**
2. Crea cuenta y carga crédito (con **$5 USD** te sobra para todo el curso).
3. Ve a **Settings → API Keys → Create Key**.
4. Cópiala. **Solo se muestra una vez.**

> Una API key es una contraseña: quien la tenga puede gastar tu saldo.
> Nunca la escribes dentro del código. Nunca la pegas en un chat. Va en `.env`.

## Paso 2 — Crear el entorno virtual

Un *entorno virtual* es una carpeta aislada con las librerías de este proyecto.
Sin él, todo se instala globalmente en tu máquina y a la larga se rompe.

Desde la **raíz** del proyecto (`Edu_TripleS`), en PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Sabrás que funcionó porque tu prompt cambia a `(.venv) PS C:\...`.

> Si PowerShell bloquea el script con un error de "execution policy", corre esto
> una sola vez y vuelve a intentar:
> `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`

**Cada vez que abras una terminal nueva tienes que volver a activarlo**
(`.\.venv\Scripts\Activate.ps1`). Es lo más común de olvidar.

## Paso 3 — Instalar las librerías

```powershell
pip install -r requirements.txt
```

- `anthropic` — el SDK oficial para hablar con Claude.
- `python-dotenv` — lee el archivo `.env` y carga la key como variable de entorno.

## Paso 4 — Guardar la key

```powershell
Copy-Item .env.example .env
notepad .env
```

Reemplaza el texto de ejemplo por tu llave real, guarda y cierra.

## Paso 5 — Verificar

```powershell
cd 00-setup
python verificar.py
```

Ese script revisa las 4 cosas y hace una llamada real mínima a la API.

---

## Glosario del nivel

- **SDK**: librería oficial que te evita escribir peticiones HTTP a mano.
- **Variable de entorno**: valor de configuración que vive fuera del código, en el
  sistema. Es el lugar estándar para secretos.
- **`.env`**: archivo local con tus variables de entorno. Está en `.gitignore`
  precisamente para que nunca salga de tu máquina.
- **`requirements.txt`**: la lista de dependencias del proyecto. Permite que
  cualquiera reproduzca tu entorno exacto.
