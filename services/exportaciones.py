"""Genera el registro de producción en formato Excel."""

import os
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side


NOMBRE_ARCHIVO = "Registro_Produccion_Cimagraf.xlsx"

COLUMNAS = [
    ("codigo", "Código"),
    ("maquina", "Máquina"),
    ("procesadas", "Unidades procesadas"),
    ("buenas", "Unidades buenas"),
    ("merma", "Unidades de merma"),
    ("merma_pct", "Porcentaje de merma"),
    ("inicio", "Fecha de inicio"),
    ("fin", "Fecha de fin"),
    ("minutos", "Duración (minutos)")
]


def exportar(ordenes, carpeta="exportaciones", abrir=True):
    """Genera y abre automáticamente el registro de producción."""

    destino = Path(carpeta)
    destino.mkdir(parents=True, exist_ok=True)

    ruta = destino / NOMBRE_ARCHIVO

    libro = Workbook()
    hoja = libro.active
    hoja.title = "Registro de producción"

    # Encabezados
    hoja.append([titulo for _, titulo in COLUMNAS])

    # Información de las órdenes
    for orden in ordenes:
        registro = orden.como_dict()
        fila = []

        for clave, _ in COLUMNAS:
            valor = registro[clave]

            if clave == "merma_pct":
                valor = valor / 100

            fila.append(valor)

        hoja.append(fila)

    # Diseño de encabezados
    for celda in hoja[1]:
        celda.font = Font(
            bold=True,
            color="FFFFFF",
            size=11
        )
        celda.fill = PatternFill(
            "solid",
            fgColor="1F4E78"
        )
        celda.alignment = Alignment(
            horizontal="center",
            vertical="center"
        )

    # Ancho de columnas
    anchos = [18, 14, 20, 17, 18, 20, 22, 22, 20]

    for numero, ancho in enumerate(anchos, 1):
        letra = hoja.cell(row=1, column=numero).column_letter
        hoja.column_dimensions[letra].width = ancho

    # Formatos numéricos
    for fila in range(2, hoja.max_row + 1):
        hoja.cell(fila, 6).number_format = "0.00%"
        hoja.cell(fila, 9).number_format = "0.00"

    # Organización de la hoja
    hoja.freeze_panes = "A2"
    hoja.auto_filter.ref = hoja.dimensions
    hoja.sheet_view.showGridLines = False
    hoja.row_dimensions[1].height = 30

    # Bordes y alineación
    borde = Border(
        bottom=Side(style="thin", color="D9E2F3")
    )

    for fila in hoja.iter_rows():
        for celda in fila:
            celda.border = borde
            celda.alignment = Alignment(
                horizontal="center",
                vertical="center"
            )

    # Guardar archivo
    libro.save(ruta)

    # Abrir automáticamente en Windows
    if abrir:
        try:
            os.startfile(str(ruta.resolve()))
        except OSError:
            pass

    return ruta
