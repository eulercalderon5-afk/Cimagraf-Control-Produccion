from controllers.ordenes import listar
from services.calculos import resumen_por_maquina
from services.ordenamiento import ordenar_por_merma
from services.exportaciones import exportar


def ordenes_por_merma():
    return ordenar_por_merma(listar())


def resumen_maquinas():
    return resumen_por_maquina(listar())


def generar_exportacion(formato):
    return exportar(listar(), formato)
