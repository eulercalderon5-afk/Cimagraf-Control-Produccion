"""Crea las tablas y permite registrar el primer usuario administrador."""
from getpass import getpass
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path
from config.conexion import obtener_conexion
from services.autenticacion import generar_hash


def inicializar():
    esquema = Path(__file__).with_name("esquema.sql").read_text(encoding="utf-8")
    with obtener_conexion() as conexion:
        for sentencia in esquema.split(";"):
            if sentencia.strip():
                conexion.execute(sentencia)
        existe = conexion.execute("SELECT EXISTS(SELECT 1 FROM usuarios)").fetchone()[0]
        if not existe:
            print("Crea el primer usuario del sistema.")
            usuario = input("Usuario administrador: ").strip()
            clave = getpass("Contraseña: ")
            confirmar = getpass("Repite la contraseña: ")
            if not usuario or len(clave) < 8 or clave != confirmar:
                raise ValueError("Usuario requerido; contraseña mínima de 8 caracteres y confirmación correcta.")
            conexion.execute("INSERT INTO usuarios(usuario, clave_hash) VALUES (%s, %s)",
                              (usuario, generar_hash(clave)))
    print("Base de datos inicializada correctamente.")


if __name__ == "__main__":
    inicializar()
