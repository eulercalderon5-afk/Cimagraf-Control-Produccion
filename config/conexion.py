"""Gestion centralizada de conexiones con PostgreSQL."""
import os

import psycopg
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()


def obtener_conexion():
    """Abre una conexion con PostgreSQL."""
    url = os.getenv("DATABASE_URL")

    if not url:
        raise RuntimeError(
            "No se encontro DATABASE_URL. Configura el archivo .env."
        )

    try:
        return psycopg.connect(url, connect_timeout=5)
    except psycopg.OperationalError as error:
        raise RuntimeError(
            "No se pudo conectar con PostgreSQL. "
            "Verifica que el servidor este activo y las credenciales sean correctas."
        ) from error
