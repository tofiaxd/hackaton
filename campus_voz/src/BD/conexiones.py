
import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client, Client


# Obtener la ubicación de este archivo
CARPETA_BD = Path(__file__).resolve().parent

# Cargar configuracion.env
ARCHIVO_ENV = CARPETA_BD / "configuracion.env"
load_dotenv(ARCHIVO_ENV)

# Obtener las credenciales
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

from urllib.parse import urlparse

url_info = urlparse(SUPABASE_URL)

print("\n--- DIAGNÓSTICO SUPABASE ---")
print("URL:", repr(SUPABASE_URL))
print("Protocolo:", url_info.scheme)
print("Dominio:", url_info.netloc)
print("Ruta adicional:", repr(url_info.path))
print("Clave cargada:", bool(SUPABASE_KEY))
print("----------------------------\n")

# Verificar que existan
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "No se encontraron las credenciales de Supabase. "
        "Revisa configuracion.env"
    )

# Crear cliente de Supabase
supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

print("Conexión con Supabase inicializada correctamente")

