"""Exporta el mismo conjunto de órdenes a formatos solicitados."""
import csv
import json
import struct
from pathlib import Path

CABECERAS = ["codigo", "maquina", "procesadas", "merma", "buenas", "merma_pct", "inicio", "fin", "minutos"]


def exportar(ordenes, formato, carpeta="exportaciones"):
    destino = Path(carpeta)
    destino.mkdir(parents=True, exist_ok=True)
    registros = [orden.como_dict() for orden in ordenes]
    ruta = destino / f"ordenes.{formato}"
    if formato == "csv":
        with ruta.open("w", newline="", encoding="utf-8-sig") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=CABECERAS)
            escritor.writeheader()
            escritor.writerows(registros)
    elif formato == "json":
        ruta.write_text(json.dumps(registros, ensure_ascii=False, indent=2), encoding="utf-8")
    elif formato == "txt":
        ruta.write_text("\n".join(" | ".join(f"{k}: {v}" for k, v in fila.items()) for fila in registros), encoding="utf-8")
    elif formato == "bin":
        # BIN propio: firma CIM1 + longitud (4 bytes) + contenido JSON UTF-8.
        contenido = json.dumps(registros, ensure_ascii=False).encode("utf-8")
        ruta.write_bytes(b"CIM1" + struct.pack(">I", len(contenido)) + contenido)
    elif formato == "pdf":
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import landscape, A4
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        documento = SimpleDocTemplate(str(ruta), pagesize=landscape(A4))
        datos = [["Código", "Máquina", "Procesadas", "Merma", "Buenas", "% merma", "Minutos"]]
        datos += [[f["codigo"], f["maquina"], f["procesadas"], f["merma"], f["buenas"], f'{f["merma_pct"]:.2f}%', f["minutos"]] for f in registros]
        tabla = Table(datos, repeatRows=1)
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#263b5a")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.whitesmoke]),
            ("PADDING", (0, 0), (-1, -1), 6),
        ]))
        estilos = getSampleStyleSheet()
        documento.build([Paragraph("Cimagraf - Reporte de producción", estilos["Title"]), Spacer(1, 12), tabla])
    else:
        raise ValueError("Formato no admitido. Use csv, json, txt, bin o pdf.")
    return ruta
