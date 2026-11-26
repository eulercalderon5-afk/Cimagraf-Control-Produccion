"""Ordenamiento eficiente con Timsort incorporado en Python."""


def ordenar_por_merma(ordenes, descendente=True):
    return sorted(ordenes, key=lambda orden: ((-orden.merma_pct) if descendente else orden.merma_pct, orden.codigo))
