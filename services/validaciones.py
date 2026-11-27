"""Validaciones centralizadas de órdenes y horarios de producción."""

import re
from datetime import datetime

from models.orden import Orden


FORMATO_FECHA = "%d/%m/%Y %H:%M"

HORARIOS = {
    0: ((8, 30, 13, 30), (15, 0, 20, 0)),
    1: ((8, 30, 13, 30), (15, 0, 20, 0)),
    2: ((8, 30, 13, 30), (15, 0, 20, 0)),
    3: ((8, 30, 13, 30), (15, 0, 20, 0)),
    4: ((8, 30, 13, 30), (15, 0, 20, 0)),
    5: ((8, 30, 12, 0),),
}


def validar_codigo(texto):
    valor = str(texto).strip().upper()

    if not re.fullmatch(r"CIM-\d{3,}", valor):
        raise ValueError(
            "Código inválido: use CIM-001 (se permiten más dígitos)."
        )

    return valor


def validar_maquina(texto):
    valor = str(texto).strip().upper()

    if not re.fullmatch(r"M-\d{2,}", valor):
        raise ValueError("Máquina inválida: use M-01.")

    return valor


def _minutos(hora):
    return hora.hour * 60 + hora.minute


def validar_horario(inicio, fin):
    if inicio.date() != fin.date():
        raise ValueError(
            "Una orden debe comenzar y finalizar el mismo día laboral."
        )

    jornadas = HORARIOS.get(inicio.weekday(), ())
    minuto_inicio = _minutos(inicio)
    minuto_fin = _minutos(fin)

    for apertura_h, apertura_m, cierre_h, cierre_m in jornadas:
        apertura = apertura_h * 60 + apertura_m
        cierre = cierre_h * 60 + cierre_m

        if apertura <= minuto_inicio < cierre and minuto_inicio < minuto_fin <= cierre:
            return

    raise ValueError(
        "Horario no permitido. De lunes a viernes: "
        "08:30 a 13:30 y 15:00 a 20:00. "
        "Sábados: 08:30 a 12:00. "
        "Domingos y horarios de refrigerio no permitidos."
    )


def validar_orden(datos):
    codigo = validar_codigo(datos.get("codigo", ""))
    maquina = validar_maquina(datos.get("maquina", ""))

    try:
        procesadas = int(datos.get("procesadas", ""))
    except (TypeError, ValueError):
        raise ValueError("Unidades procesadas: ingresa un n?mero entero v?lido.") from None

    if procesadas <= 0:
        raise ValueError("Unidades procesadas: debe ser un n?mero mayor que cero.")

    try:
        merma = int(datos.get("merma", ""))
    except (TypeError, ValueError):
        raise ValueError("Merma: ingresa un n?mero entero v?lido.") from None

    if merma < 0:
        raise ValueError("Merma: no puede ser un n?mero negativo.")

    if merma > procesadas:
        raise ValueError("Merma: no puede superar las unidades procesadas.")

    try:
        inicio = datetime.strptime(
            str(datos.get("inicio", "")).strip(), FORMATO_FECHA
        )
    except (TypeError, ValueError):
        raise ValueError(
            "Fecha de inicio: formato incorrecto. Usa DD/MM/AAAA HH:MM."
        ) from None

    try:
        fin = datetime.strptime(
            str(datos.get("fin", "")).strip(), FORMATO_FECHA
        )
    except (TypeError, ValueError):
        raise ValueError(
            "Fecha de fin: formato incorrecto. Usa DD/MM/AAAA HH:MM."
        ) from None

    if fin <= inicio:
        raise ValueError(
            "Fecha de fin: debe ser posterior a la fecha de inicio."
        )

    validar_horario(inicio, fin)

    return Orden(
        codigo,
        maquina,
        procesadas,
        merma,
        inicio,
        fin,
    )
