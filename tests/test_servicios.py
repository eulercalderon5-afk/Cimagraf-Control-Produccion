import unittest
import tempfile
from pathlib import Path
from datetime import datetime
from models.orden import Orden
from services.calculos import calcular_merma_pct, calcular_minutos, resumen_por_maquina
from services.ordenamiento import ordenar_por_merma
from services.validaciones import validar_orden
from services.autenticacion import generar_hash, verificar_clave
from services.exportaciones import exportar


class PruebasCimagraf(unittest.TestCase):
    def setUp(self):
        self.ordenes = [
            Orden("CIM-001", "M-01", 1000, 60, datetime(2026, 10, 1, 8), datetime(2026, 10, 1, 9, 30)),
            Orden("CIM-002", "M-02", 800, 32, datetime(2026, 10, 1, 9), datetime(2026, 10, 1, 10)),
            Orden("CIM-003", "M-01", 1200, 48, datetime(2026, 10, 1, 10), datetime(2026, 10, 1, 11, 30)),
        ]

    def test_porcentaje_merma(self):
        self.assertEqual(calcular_merma_pct(1000, 60), 6.0)

    def test_rechaza_cero_procesadas(self):
        with self.assertRaises(ValueError):
            calcular_merma_pct(0, 0)

    def test_ordenamiento_descendente(self):
        resultado = ordenar_por_merma(self.ordenes)
        self.assertEqual([o.codigo for o in resultado], ["CIM-001", "CIM-002", "CIM-003"])

    def test_resumen_maquina(self):
        resumen = resumen_por_maquina(self.ordenes)
        self.assertEqual(resumen["M-01"]["ordenes"], 2)
        self.assertEqual(resumen["M-01"]["procesadas"], 2200)
        self.assertEqual(resumen["M-01"]["merma"], 108)

    def test_validacion_orden(self):
        datos = {"codigo": "cim-010", "maquina": "m-01", "procesadas": "100", "merma": "5",
                 "inicio": "01-10-2026 08:00", "fin": "01-10-2026 09:00"}
        self.assertEqual(validar_orden(datos).codigo, "CIM-010")

    def test_rechaza_periodo_incorrecto(self):
        datos = {"codigo": "CIM-010", "maquina": "M-01", "procesadas": "100", "merma": "5",
                 "inicio": "01-10-2026 09:00", "fin": "01-10-2026 08:00"}
        with self.assertRaises(ValueError):
            validar_orden(datos)

    def test_hash_no_es_clave_original(self):
        hash_clave = generar_hash("ClaveSegura123")
        self.assertNotIn("ClaveSegura123", hash_clave)
        self.assertTrue(verificar_clave("ClaveSegura123", hash_clave))
        self.assertFalse(verificar_clave("incorrecta", hash_clave))

    def test_duracion(self):
        self.assertEqual(calcular_minutos(self.ordenes[0].inicio, self.ordenes[0].fin), 90)


    def test_exportaciones_basicas(self):
        from openpyxl import load_workbook

        with tempfile.TemporaryDirectory() as carpeta:
            ruta = exportar(self.ordenes, carpeta, abrir=False)

            self.assertTrue(ruta.exists())
            self.assertGreater(ruta.stat().st_size, 0)
            self.assertEqual(ruta.suffix, ".xlsx")

            libro = load_workbook(ruta)
            hoja = libro.active

            self.assertEqual(hoja.title, "Registro de producción")
            self.assertEqual(hoja.max_row, 4)
            self.assertEqual(hoja.max_column, 9)
            self.assertEqual(hoja.freeze_panes, "A2")
            self.assertEqual(hoja["F2"].number_format, "0.00%")

            libro.close()

if __name__ == "__main__":
    unittest.main()
