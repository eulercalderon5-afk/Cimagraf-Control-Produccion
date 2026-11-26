"""Punto de entrada. Coordina vistas y controladores, sin lógica de negocio."""
from dotenv import load_dotenv
load_dotenv()

from controllers.autenticacion import iniciar_sesion
from controllers import ordenes, reportes
from views import pantallas
from services.exportaciones import exportar
from services.calculos import resumen_por_maquina
from services.ordenamiento import ordenar_por_merma


def mostrar_resumen():
    resumen = reportes.resumen_maquinas()
    print("\nMÁQUINA | ÓRDENES | PROCESADAS | MERMA | % MERMA | MINUTOS")
    for maquina, datos in resumen.items():
        print(f"{maquina:7} | {datos['ordenes']:7} | {datos['procesadas']:10} | "
              f"{datos['merma']:5} | {datos['merma_pct']:7.2f}% | {datos['minutos']:7.2f}")


def ejecutar():
    usuario = None
    while usuario is None:
        nombre, clave = pantallas.pedir_login()
        usuario = iniciar_sesion(nombre, clave)
        if usuario is None:
            print("Usuario o contraseña incorrectos.")
    print(f"Bienvenido, {usuario['usuario']}.")

    while True:
        opcion = pantallas.mostrar_menu()
        try:
            if opcion == "1":
                orden = ordenes.registrar(pantallas.pedir_orden(), usuario)
                print("Orden registrada correctamente.")
                pantallas.mostrar_orden(orden)
            elif opcion == "2":
                orden = ordenes.consultar(pantallas.pedir_codigo())
                print("Orden encontrada." if orden else "No se encontró la orden.")
                if orden:
                    pantallas.mostrar_orden(orden)
            elif opcion == "3":
                codigo = pantallas.pedir_codigo()
                orden = ordenes.consultar(codigo)
                if not orden:
                    print("No se encontró la orden.")
                else:
                    orden = ordenes.modificar(codigo, pantallas.pedir_datos_actualizacion(), usuario)
                    print("Orden modificada correctamente.")
            elif opcion == "4":
                ordenes.eliminar(pantallas.pedir_codigo(), usuario)
                print("Orden eliminada y acción auditada.")
            elif opcion == "5":
                filas = reportes.ordenes_por_merma()
                for orden in filas:
                    pantallas.mostrar_orden(orden)
            elif opcion == "6":
                mostrar_resumen()
            elif opcion == "7":
                formato = input("Formato (csv/json/txt/bin/pdf): ").strip().lower()
                ruta = reportes.generar_exportacion(formato)
                print(f"Archivo generado: {ruta}")
            elif opcion == "8":
                for fila in ordenes.historial():
                    print(fila)
            elif opcion == "9":
                print("Sesión finalizada.")
                break
            else:
                print("Opción no válida.")
        except (ValueError, OSError) as error:
            print(f"No se pudo completar la operación: {error}")
        except Exception as error:
            # Mensaje controlado para errores de conexión/BD; detalle técnico en terminal.
            print(f"Error del sistema: {error}")


if __name__ == "__main__":
    ejecutar()
