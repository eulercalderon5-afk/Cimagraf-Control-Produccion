
"""Gestion centralizada de conexiones con SQLite."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path


RUTA_BD = Path(__file__).resolve().parent.parent / "database" / "cimagraf.db"


@contextmanager
def obtener_conexion():
    """Abre, confirma o revierte y cierra la conexion."""

    conexion = sqlite3.connect(RUTA_BD, timeout=10)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")

    try:
        yield conexion
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()
