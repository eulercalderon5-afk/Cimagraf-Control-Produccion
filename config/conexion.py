"""Único punto de conexión con PostgreSQL."""
import os
import psycopg


def obtener_conexion():
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("Configura DATABASE_URL en las variables de entorno.")
    return psycopg.connect(url)
