"""Registro centralizado de acciones para trazabilidad."""

import json


def registrar_auditoria(
    conexion, usuario_id, accion, entidad, entidad_id, detalle
):
    conexion.execute(
        """
        INSERT INTO auditoria(
            usuario_id, accion, entidad, entidad_id, detalle
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            usuario_id,
            accion,
            entidad,
            entidad_id,
            json.dumps(detalle, ensure_ascii=False),
        ),
    )
