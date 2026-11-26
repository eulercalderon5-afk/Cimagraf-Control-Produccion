from config.conexion import obtener_conexion
from services.autenticacion import verificar_clave


def iniciar_sesion(usuario, clave):
    with obtener_conexion() as conexion:
        fila = conexion.execute(
            "SELECT id, usuario, clave_hash FROM usuarios WHERE usuario=%s AND activo=TRUE",
            (usuario.strip(),),
        ).fetchone()
    if not fila or not verificar_clave(clave, fila[2]):
        return None
    return {"id": fila[0], "usuario": fila[1]}
