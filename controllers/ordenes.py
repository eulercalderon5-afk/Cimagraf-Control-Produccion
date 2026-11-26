"""Casos de uso de órdenes; cada operación usa una transacción."""
from config.conexion import obtener_conexion
from models.orden import Orden
from services.validaciones import validar_orden
from services.auditoria import registrar_auditoria


def _modelo(fila):
    return Orden(fila[1], fila[2], fila[3], fila[4], fila[5], fila[6])


def registrar(datos, usuario):
    orden = validar_orden(datos)
    with obtener_conexion() as conexion:
        fila = conexion.execute(
            "INSERT INTO ordenes(codigo,maquina,procesadas,merma,inicio,fin,creado_por) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id",
            (orden.codigo, orden.maquina, orden.procesadas, orden.merma,
             orden.inicio, orden.fin, usuario["id"]),
        ).fetchone()
        registrar_auditoria(conexion, usuario["id"], "CREAR", "orden", fila[0], orden.como_dict())
    return orden


def consultar(codigo):
    with obtener_conexion() as conexion:
        fila = conexion.execute(
            "SELECT id,codigo,maquina,procesadas,merma,inicio,fin FROM ordenes WHERE codigo=%s",
            (codigo.strip().upper(),),
        ).fetchone()
    return _modelo(fila) if fila else None


def listar():
    with obtener_conexion() as conexion:
        filas = conexion.execute(
            "SELECT id,codigo,maquina,procesadas,merma,inicio,fin FROM ordenes"
        ).fetchall()
    return [_modelo(fila) for fila in filas]


def modificar(codigo, datos, usuario):
    nueva = validar_orden(datos)
    if nueva.codigo != codigo.strip().upper():
        raise ValueError("El código de la orden no se puede cambiar durante una modificación.")
    with obtener_conexion() as conexion:
        anterior = conexion.execute(
            "SELECT id,codigo,maquina,procesadas,merma,inicio,fin FROM ordenes WHERE codigo=%s FOR UPDATE",
            (codigo.strip().upper(),),
        ).fetchone()
        if not anterior:
            raise ValueError("No existe una orden con ese código.")
        conexion.execute(
            "UPDATE ordenes SET maquina=%s,procesadas=%s,merma=%s,inicio=%s,fin=%s,actualizado_en=CURRENT_TIMESTAMP WHERE id=%s",
            (nueva.maquina, nueva.procesadas, nueva.merma, nueva.inicio, nueva.fin, anterior[0]),
        )
        registrar_auditoria(conexion, usuario["id"], "MODIFICAR", "orden", anterior[0],
                            {"antes": _modelo(anterior).como_dict(), "despues": nueva.como_dict()})
    return nueva


def eliminar(codigo, usuario):
    with obtener_conexion() as conexion:
        fila = conexion.execute(
            "DELETE FROM ordenes WHERE codigo=%s RETURNING id,codigo,maquina,procesadas,merma,inicio,fin",
            (codigo.strip().upper(),),
        ).fetchone()
        if not fila:
            raise ValueError("No existe una orden con ese código.")
        registrar_auditoria(conexion, usuario["id"], "ELIMINAR", "orden", fila[0], _modelo(fila).como_dict())


def historial():
    with obtener_conexion() as conexion:
        return conexion.execute(
            "SELECT a.fecha,u.usuario,a.accion,a.entidad,a.entidad_id,a.detalle "
            "FROM auditoria a LEFT JOIN usuarios u ON u.id=a.usuario_id ORDER BY a.fecha DESC LIMIT 200"
        ).fetchall()
