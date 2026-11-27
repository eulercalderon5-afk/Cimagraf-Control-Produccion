"""Autenticación de usuarios del sistema."""

from config.conexion import obtener_conexion
from services.autenticacion import verificar_clave


def iniciar_sesion(usuario, clave):
    with obtener_conexion() as conexion:
        fila = conexion.execute(
            """
            SELECT id, usuario, clave_hash
            FROM usuarios
            WHERE usuario = ? AND activo = 1
            """,
            (usuario.strip(),),
        ).fetchone()

    if not fila or not verificar_clave(clave, fila["clave_hash"]):
        return None

    return {
        "id": fila["id"],
        "usuario": fila["usuario"]
    }
