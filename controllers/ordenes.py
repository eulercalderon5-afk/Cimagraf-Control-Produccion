"""Operaciones de órdenes de producción con SQLite."""

from config.conexion import obtener_conexion
from models.orden import Orden
from services.validaciones import validar_orden
from services.auditoria import registrar_auditoria



from datetime import datetime


def _modelo(fila):
    inicio = fila["inicio"]
    fin = fila["fin"]

    if isinstance(inicio, str):
        inicio = datetime.fromisoformat(inicio)

    if isinstance(fin, str):
        fin = datetime.fromisoformat(fin)

    return Orden(
        fila["codigo"],
        fila["maquina"],
        fila["procesadas"],
        fila["merma"],
        inicio,
        fin,
    )



def registrar(datos, usuario):
    orden = validar_orden(datos)

    with obtener_conexion() as conexion:
        conexion.execute("BEGIN IMMEDIATE")

        existente = conexion.execute(
            "SELECT 1 FROM ordenes WHERE codigo = ?",
            (orden.codigo,),
        ).fetchone()

        if existente:
            raise ValueError(
                f"Ya existe una orden con el c?digo {orden.codigo}. "
                "Ingresa un c?digo diferente."
            )

        cursor = conexion.execute(
            """
            INSERT INTO ordenes(
                codigo, maquina, procesadas, merma,
                inicio, fin, creado_por
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                orden.codigo,
                orden.maquina,
                orden.procesadas,
                orden.merma,
                orden.inicio,
                orden.fin,
                usuario["id"],
            ),
        )

        registrar_auditoria(
            conexion, usuario["id"], "CREAR",
            "orden", cursor.lastrowid, orden.como_dict()
        )

    return orden


def consultar(codigo):
    with obtener_conexion() as conexion:
        fila = conexion.execute(
            """
            SELECT id, codigo, maquina, procesadas,
                   merma, inicio, fin
            FROM ordenes
            WHERE codigo = ?
            """,
            (codigo.strip().upper(),),
        ).fetchone()

    return _modelo(fila) if fila else None


def listar():
    with obtener_conexion() as conexion:
        filas = conexion.execute(
            """
            SELECT id, codigo, maquina, procesadas,
                   merma, inicio, fin
            FROM ordenes
            ORDER BY id DESC
            """
        ).fetchall()

    return [_modelo(fila) for fila in filas]


def modificar(codigo, datos, usuario):
    codigo = codigo.strip().upper()
    nueva = validar_orden(datos)

    if nueva.codigo != codigo:
        raise ValueError(
            "El código de la orden no se puede cambiar durante una modificación."
        )

    with obtener_conexion() as conexion:
        conexion.execute("BEGIN IMMEDIATE")

        anterior = conexion.execute(
            """
            SELECT id, codigo, maquina, procesadas,
                   merma, inicio, fin
            FROM ordenes
            WHERE codigo = ?
            """,
            (codigo,),
        ).fetchone()

        if not anterior:
            raise ValueError("No existe una orden con ese código.")

        conexion.execute(
            """
            UPDATE ordenes
            SET maquina = ?, procesadas = ?, merma = ?,
                inicio = ?, fin = ?,
                actualizado_en = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                nueva.maquina,
                nueva.procesadas,
                nueva.merma,
                nueva.inicio,
                nueva.fin,
                anterior["id"],
            ),
        )

        registrar_auditoria(
            conexion,
            usuario["id"],
            "MODIFICAR",
            "orden",
            anterior["id"],
            {
                "antes": _modelo(anterior).como_dict(),
                "despues": nueva.como_dict(),
            },
        )

    return nueva


def eliminar(codigo, usuario):
    codigo = codigo.strip().upper()

    with obtener_conexion() as conexion:
        conexion.execute("BEGIN IMMEDIATE")

        fila = conexion.execute(
            """
            SELECT id, codigo, maquina, procesadas,
                   merma, inicio, fin
            FROM ordenes
            WHERE codigo = ?
            """,
            (codigo,),
        ).fetchone()

        if not fila:
            raise ValueError("No existe una orden con ese código.")

        conexion.execute(
            "DELETE FROM ordenes WHERE id = ?",
            (fila["id"],),
        )

        registrar_auditoria(
            conexion,
            usuario["id"],
            "ELIMINAR",
            "orden",
            fila["id"],
            _modelo(fila).como_dict(),
        )


def historial():
    with obtener_conexion() as conexion:
        return conexion.execute(
            """
            SELECT a.fecha, u.usuario, a.accion,
                   a.entidad, a.entidad_id, a.detalle
            FROM auditoria a
            LEFT JOIN usuarios u ON u.id = a.usuario_id
            ORDER BY a.fecha DESC
            LIMIT 200
            """
        ).fetchall()
