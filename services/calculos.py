"""Indicadores y agrupaciones de producción."""
from collections import defaultdict


def calcular_merma_pct(procesadas, merma):
    if procesadas <= 0 or not 0 <= merma <= procesadas:
        raise ValueError("Cantidades fuera de rango.")
    return round(merma * 100 / procesadas, 2)


def calcular_minutos(inicio, fin):
    if fin <= inicio:
        raise ValueError("El fin debe ser posterior al inicio.")
    return round((fin - inicio).total_seconds() / 60, 2)


def resumen_por_maquina(ordenes):
    acumulado = defaultdict(lambda: {"ordenes": 0, "procesadas": 0, "merma": 0, "minutos": 0.0})
    for orden in ordenes:
        fila = acumulado[orden.maquina]
        fila["ordenes"] += 1
        fila["procesadas"] += orden.procesadas
        fila["merma"] += orden.merma
        fila["minutos"] += orden.minutos
    return {maquina: {**fila, "merma_pct": calcular_merma_pct(fila["procesadas"], fila["merma"])}
            for maquina, fila in sorted(acumulado.items())}
