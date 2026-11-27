"""Validaciones centralizadas: cada regla se define una sola vez."""
import re
from datetime import datetime
from models.orden import Orden

FORMATO_FECHA = "%d-%m-%Y %H:%M"


def validar_codigo(texto):
    valor = str(texto).strip().upper()
    if not re.fullmatch(r"CIM-\d{3,}", valor):
        raise ValueError("Código inválido: use CIM-001 (se permiten más dígitos).")
    return valor


def validar_maquina(texto):
    valor = str(texto).strip().upper()
    if not re.fullmatch(r"M-\d{2,}", valor):
        raise ValueError("Máquina inválida: use M-01.")
    return valor


def validar_orden(datos):
    try:
        procesadas = int(datos["procesadas"])
        merma = int(datos["merma"])
        inicio = datetime.strptime(str(datos["inicio"]).strip(), FORMATO_FECHA)
        fin = datetime.strptime(str(datos["fin"]).strip(), FORMATO_FECHA)
    except (KeyError, TypeError, ValueError):
        raise ValueError("Revise cantidades y fechas. Formato: DD-MM-AAAA HH:MM.") from None
    if procesadas <= 0 or not 0 <= merma <= procesadas:
        raise ValueError("Procesadas debe ser > 0 y merma debe estar entre 0 y procesadas.")
    if fin <= inicio:
        raise ValueError("La fecha/hora final debe ser posterior al inicio.")
    return Orden(validar_codigo(datos["codigo"]), validar_maquina(datos["maquina"]),
                 procesadas, merma, inicio, fin)
