"""Interfaz de consola: solo solicita y presenta información."""
from getpass import getpass
from datetime import datetime


def pedir_orden():
    return {
        "codigo": input("Código (CIM-001): "),
        "maquina": input("Máquina (M-01): "),
        "procesadas": input("Unidades procesadas: "),
        "merma": input("Unidades de merma: "),
        "inicio": input("Inicio (DD-MM-AAAA HH:MM): "),
        "fin": input("Fin (DD-MM-AAAA HH:MM): "),
    }


def mostrar_orden(orden):
    print(f"\nOrden: {orden.codigo} | Máquina: {orden.maquina}")
    print(f"Procesadas: {orden.procesadas} | Buenas: {orden.buenas} | Merma: {orden.merma} ({orden.merma_pct:.2f}%)")
    print(f"Inicio: {orden.inicio:%d-%m-%Y %H:%M} | Fin: {orden.fin:%d-%m-%Y %H:%M} | Duración: {orden.minutos:.2f} min")


def mostrar_menu():
    print("\n========== CIMAGRAF | CONTROL DE PRODUCCIÓN ==========")
    for numero, opcion in enumerate(("Registrar orden", "Consultar orden", "Modificar orden",
                                     "Eliminar orden", "Listar por porcentaje de merma",
                                     "Resumen por máquina", "Exportar información",
                                     "Historial de auditoría", "Cerrar sesión"), 1):
        print(f"{numero}. {opcion}")
    return input("Seleccione una opción: ").strip()


def pedir_login():
    print("\n========== ACCESO AL SISTEMA ==========")
    return input("Usuario: ").strip(), getpass("Contraseña: ")


def pedir_codigo():
    return input("Código de orden: ").strip().upper()


def pedir_datos_actualizacion():
    print("Ingrese los datos actualizados de la orden:")
    return pedir_orden()
