
"""Inicializa la base de datos y registra el primer administrador."""

from getpass import getpass
from pathlib import Path

from config.conexion import obtener_conexion
from services.autenticacion import generar_hash


RUTA_ESQUEMA = Path(__file__).with_name("esquema.sql")


def inicializar_bd():
    if not RUTA_ESQUEMA.exists():
        raise FileNotFoundError("No se encontró esquema.sql")

    esquema = RUTA_ESQUEMA.read_text(encoding="utf-8")

    with obtener_conexion() as conexion:
        conexion.executescript(esquema)

        existe = conexion.execute(
            "SELECT 1 FROM usuarios LIMIT 1"
        ).fetchone()

        if not existe:
            print("\nCrea el primer usuario administrador.")

            usuario = input("Usuario administrador: ").strip()
            clave = getpass("Contraseña: ")
            confirmar = getpass("Repite la contraseña: ")

            if not usuario:
                raise ValueError("El usuario es obligatorio.")

            if len(clave) < 8:
                raise ValueError(
                    "La contraseña debe tener al menos 8 caracteres."
                )

            if clave != confirmar:
                raise ValueError("Las contraseñas no coinciden.")

            conexion.execute(
                """
                INSERT INTO usuarios (usuario, clave_hash)
                VALUES (?, ?)
                """,
                (usuario, generar_hash(clave))
            )

    print("Base de datos inicializada correctamente.")


if __name__ == "__main__":
    inicializar_bd()
