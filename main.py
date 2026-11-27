import json
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

from controllers.autenticacion import iniciar_sesion
from controllers import ordenes, reportes


COLOR_FONDO = "#F3F6FA"
COLOR_PANEL = "#FFFFFF"
COLOR_LATERAL = "#17263C"
COLOR_AZUL = "#2878D0"
COLOR_TEXTO = "#26364A"
COLOR_SECUNDARIO = "#718096"

FORMATO_FECHA = "%d-%m-%Y %H:%M"


def configurar_estilo(raiz):
    estilo = ttk.Style(raiz)
    estilo.theme_use("clam")

    estilo.configure(
        "Treeview",
        background="white",
        foreground=COLOR_TEXTO,
        rowheight=34,
        fieldbackground="white",
        font=("Segoe UI", 9)
    )
    estilo.configure(
        "Treeview.Heading",
        background="#E8EEF6",
        foreground=COLOR_TEXTO,
        font=("Segoe UI", 9, "bold"),
        padding=9
    )
    estilo.map(
        "Treeview",
        background=[("selected", "#D8E9FC")],
        foreground=[("selected", COLOR_TEXTO)]
    )
    estilo.configure(
        "TButton",
        font=("Segoe UI", 9),
        padding=7
    )


def mostrar_login():
    ventana = tk.Tk()
    ventana.title("CIMAGRAF | Acceso")
    ventana.geometry("430x500")
    ventana.resizable(False, False)
    ventana.configure(bg=COLOR_LATERAL)

    x = (ventana.winfo_screenwidth() - 430) // 2
    y = (ventana.winfo_screenheight() - 500) // 2
    ventana.geometry(f"430x500+{x}+{y}")

    panel = tk.Frame(ventana, bg="#20334F", padx=35, pady=30)
    panel.pack(fill="both", expand=True, padx=25, pady=25)

    tk.Label(
        panel, text="CIMAGRAF",
        font=("Segoe UI", 27, "bold"),
        fg="white", bg="#20334F"
    ).pack(pady=(15, 4))

    tk.Label(
        panel, text="CONTROL DE PRODUCCIÓN",
        font=("Segoe UI", 9, "bold"),
        fg="#AFC2DD", bg="#20334F"
    ).pack(pady=(0, 30))

    tk.Label(
        panel, text="Usuario",
        font=("Segoe UI", 10, "bold"),
        fg="white", bg="#20334F"
    ).pack(anchor="w")

    usuario = tk.Entry(
        panel, font=("Segoe UI", 12),
        relief="flat", bg="white"
    )
    usuario.pack(fill="x", ipady=10, pady=(7, 18))

    tk.Label(
        panel, text="Contraseña",
        font=("Segoe UI", 10, "bold"),
        fg="white", bg="#20334F"
    ).pack(anchor="w")

    clave = tk.Entry(
        panel, font=("Segoe UI", 12),
        relief="flat", bg="white", show="*"
    )
    clave.pack(fill="x", ipady=10, pady=(7, 8))

    visible = tk.BooleanVar(value=False)

    def alternar():
        clave.configure(show="" if visible.get() else "*")

    tk.Checkbutton(
        panel, text="Mostrar contraseña",
        variable=visible, command=alternar,
        bg="#20334F", fg="white",
        activebackground="#20334F",
        selectcolor="#20334F"
    ).pack(anchor="w", pady=(0, 20))

    resultado = {"usuario": None}

    def acceder(event=None):
        nombre = usuario.get().strip()
        contrasena = clave.get()

        if not nombre or not contrasena:
            messagebox.showwarning(
                "Datos incompletos",
                "Ingresa tu usuario y contraseña.",
                parent=ventana
            )
            return

        try:
            cuenta = iniciar_sesion(nombre, contrasena)
        except Exception as error:
            messagebox.showerror(
                "Error de acceso", str(error), parent=ventana
            )
            return

        if cuenta is None:
            messagebox.showerror(
                "Acceso denegado",
                "Usuario o contraseña incorrectos.",
                parent=ventana
            )
            clave.delete(0, tk.END)
            clave.focus_set()
            return

        resultado["usuario"] = cuenta
        ventana.destroy()

    tk.Button(
        panel, text="INICIAR SESIÓN",
        command=acceder,
        font=("Segoe UI", 11, "bold"),
        bg=COLOR_AZUL, fg="white",
        activebackground="#1D65B5",
        relief="flat", cursor="hand2",
        pady=12
    ).pack(fill="x")

    tk.Label(
        panel, text="Acceso seguro al sistema de producción",
        font=("Segoe UI", 8),
        fg="#AFC2DD", bg="#20334F"
    ).pack(pady=(22, 0))

    ventana.bind("<Return>", acceder)
    ventana.protocol("WM_DELETE_WINDOW", ventana.destroy)
    usuario.focus_set()
    ventana.mainloop()

    return resultado["usuario"]


class Aplicacion:

    def __init__(self, usuario):
        self.usuario = usuario
        self.raiz = tk.Tk()
        self.raiz.title("CIMAGRAF | Control de producción")
        self.raiz.geometry("1200x730")
        self.raiz.minsize(1000, 620)
        self.raiz.configure(bg=COLOR_FONDO)

        configurar_estilo(self.raiz)
        self.construir_estructura()
        self.mostrar_inicio()

    def construir_estructura(self):
        lateral = tk.Frame(
            self.raiz, bg=COLOR_LATERAL, width=225
        )
        lateral.pack(side="left", fill="y")
        lateral.pack_propagate(False)

        tk.Label(
            lateral, text="CIMAGRAF",
            font=("Segoe UI", 22, "bold"),
            fg="white", bg=COLOR_LATERAL
        ).pack(pady=(30, 2))

        tk.Label(
            lateral, text="CONTROL DE PRODUCCIÓN",
            font=("Segoe UI", 8, "bold"),
            fg="#AFC2DD", bg=COLOR_LATERAL
        ).pack(pady=(0, 30))

        opciones = [
            ("Inicio", self.mostrar_inicio),
            ("Registrar orden", self.abrir_registro),
            ("Consultar órdenes", self.mostrar_ordenes),
            ("Resumen por máquina", self.mostrar_resumen),
            ("Órdenes por merma", self.mostrar_merma),
            ("Historial de auditoría", self.mostrar_auditoria),
            ("Exportar a Excel", self.exportar),
        ]

        for texto, funcion in opciones:
            tk.Button(
                lateral, text=texto,
                command=funcion,
                anchor="w", padx=22,
                font=("Segoe UI", 10),
                bg=COLOR_LATERAL, fg="white",
                activebackground="#29415F",
                activeforeground="white",
                relief="flat", cursor="hand2",
                pady=12
            ).pack(fill="x", padx=8, pady=2)

        tk.Frame(
            lateral, bg="#354963", height=1
        ).pack(fill="x", padx=15, pady=20)

        tk.Label(
            lateral,
            text=f"Usuario: {self.usuario['usuario']}",
            font=("Segoe UI", 9),
            fg="#D5E0EE", bg=COLOR_LATERAL
        ).pack(side="bottom", pady=(0, 8))

        tk.Button(
            lateral, text="Cerrar sesión",
            command=self.cerrar_sesion,
            bg="#A83C45", fg="white",
            activebackground="#8D3039",
            relief="flat", cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            pady=10
        ).pack(side="bottom", fill="x", padx=12, pady=(0, 20))

        self.contenido = tk.Frame(
            self.raiz, bg=COLOR_FONDO
        )
        self.contenido.pack(
            side="right", fill="both", expand=True
        )

    def limpiar(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def encabezado(self, titulo, descripcion):
        cabecera = tk.Frame(self.contenido, bg=COLOR_FONDO)
        cabecera.pack(fill="x", padx=30, pady=(25, 20))

        tk.Label(
            cabecera, text=titulo,
            font=("Segoe UI", 21, "bold"),
            fg=COLOR_TEXTO, bg=COLOR_FONDO
        ).pack(anchor="w")

        tk.Label(
            cabecera, text=descripcion,
            font=("Segoe UI", 10),
            fg=COLOR_SECUNDARIO, bg=COLOR_FONDO
        ).pack(anchor="w", pady=(5, 0))

    def tarjeta(self, padre, titulo, valor, detalle):
        tarjeta = tk.Frame(
            padre, bg=COLOR_PANEL,
            padx=20, pady=17,
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )
        tarjeta.pack(
            side="left", fill="both",
            expand=True, padx=6
        )

        tk.Label(
            tarjeta, text=titulo,
            font=("Segoe UI", 9),
            fg=COLOR_SECUNDARIO, bg=COLOR_PANEL
        ).pack(anchor="w")

        tk.Label(
            tarjeta, text=str(valor),
            font=("Segoe UI", 23, "bold"),
            fg=COLOR_AZUL, bg=COLOR_PANEL
        ).pack(anchor="w", pady=7)

        tk.Label(
            tarjeta, text=detalle,
            font=("Segoe UI", 8),
            fg=COLOR_SECUNDARIO, bg=COLOR_PANEL
        ).pack(anchor="w")

    def crear_tabla(self, padre, columnas, altura=12):
        marco = tk.Frame(padre, bg=COLOR_PANEL)
        marco.pack(fill="both", expand=True, padx=30, pady=10)

        tabla = ttk.Treeview(
            marco, columns=tuple(columna[0] for columna in columnas),
            show="headings", height=altura
        )

        for clave, titulo, ancho in columnas:
            tabla.heading(clave, text=titulo)
            tabla.column(
                clave, width=ancho,
                minwidth=70, anchor="center"
            )

        barra = ttk.Scrollbar(
            marco, orient="vertical",
            command=tabla.yview
        )
        tabla.configure(yscrollcommand=barra.set)

        tabla.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        return tabla

    def cargar_ordenes(self, tabla, filas):
        tabla.delete(*tabla.get_children())

        for orden in filas:
            tabla.insert("", "end", values=(
                orden.codigo,
                orden.maquina,
                orden.procesadas,
                orden.buenas,
                orden.merma,
                f"{orden.merma_pct:.2f}%",
                orden.inicio.strftime(FORMATO_FECHA),
                orden.fin.strftime(FORMATO_FECHA),
                f"{orden.minutos:.2f}"
            ))

    def mostrar_inicio(self):
        self.limpiar()
        self.encabezado(
            "Panel principal",
            "Resumen general del control de producción."
        )

        try:
            filas = ordenes.listar()
            total = len(filas)
            procesadas = sum(o.procesadas for o in filas)
            merma = sum(o.merma for o in filas)
            porcentaje = (merma * 100 / procesadas) if procesadas else 0
        except Exception as error:
            messagebox.showerror("Error", str(error))
            return

        tarjetas = tk.Frame(self.contenido, bg=COLOR_FONDO)
        tarjetas.pack(fill="x", padx=24, pady=8)

        self.tarjeta(tarjetas, "Órdenes registradas", total, "Registros actuales")
        self.tarjeta(tarjetas, "Unidades procesadas", procesadas, "Producción acumulada")
        self.tarjeta(tarjetas, "Unidades de merma", merma, "Pérdidas acumuladas")
        self.tarjeta(tarjetas, "Porcentaje de merma", f"{porcentaje:.2f}%", "Sobre unidades procesadas")

        tk.Label(
            self.contenido, text="Órdenes recientes",
            font=("Segoe UI", 13, "bold"),
            fg=COLOR_TEXTO, bg=COLOR_FONDO
        ).pack(anchor="w", padx=30, pady=(22, 5))

        columnas = [
            ("codigo", "Código", 110),
            ("maquina", "Máquina", 90),
            ("procesadas", "Procesadas", 110),
            ("buenas", "Buenas", 100),
            ("merma", "Merma", 90),
            ("porcentaje", "% Merma", 100),
            ("inicio", "Inicio", 145),
            ("fin", "Fin", 145),
            ("minutos", "Minutos", 90),
        ]

        tabla = self.crear_tabla(self.contenido, columnas, 8)
        self.cargar_ordenes(tabla, filas[:10])

    def mostrar_ordenes(self):
        self.limpiar()
        self.encabezado(
            "Consultar órdenes",
            "Consulta y administra las órdenes de producción."
        )

        barra = tk.Frame(self.contenido, bg=COLOR_FONDO)
        barra.pack(fill="x", padx=30, pady=5)

        tk.Button(
            barra, text="Nueva orden",
            command=self.abrir_registro,
            bg=COLOR_AZUL, fg="white",
            relief="flat", padx=15, pady=8
        ).pack(side="left")

        tk.Button(
            barra, text="Modificar seleccionada",
            command=lambda: self.modificar_seleccion(tabla),
            padx=12
        ).pack(side="left", padx=8)

        tk.Button(
            barra, text="Eliminar seleccionada",
            command=lambda: self.eliminar_seleccion(tabla),
            padx=12
        ).pack(side="left")

        columnas = [
            ("codigo", "Código", 100),
            ("maquina", "Máquina", 85),
            ("procesadas", "Procesadas", 100),
            ("buenas", "Buenas", 90),
            ("merma", "Merma", 80),
            ("porcentaje", "% Merma", 90),
            ("inicio", "Inicio", 140),
            ("fin", "Fin", 140),
            ("minutos", "Minutos", 85),
        ]

        tabla = self.crear_tabla(self.contenido, columnas, 15)
        self.cargar_ordenes(tabla, ordenes.listar())

        def seleccionar(event=None):
            elegido = tabla.selection()
            if elegido:
                valores = tabla.item(elegido[0], "values")
                self.ver_detalle(valores[0])

        tabla.bind("<Double-1>", seleccionar)

    def ver_detalle(self, codigo):
        orden = ordenes.consultar(codigo)
        if not orden:
            messagebox.showwarning("Aviso", "No se encontró la orden.")
            return

        datos = (
            f"Código: {orden.codigo}\n"
            f"Máquina: {orden.maquina}\n"
            f"Unidades procesadas: {orden.procesadas}\n"
            f"Unidades buenas: {orden.buenas}\n"
            f"Unidades de merma: {orden.merma}\n"
            f"Porcentaje de merma: {orden.merma_pct:.2f}%\n"
            f"Inicio: {orden.inicio.strftime(FORMATO_FECHA)}\n"
            f"Fin: {orden.fin.strftime(FORMATO_FECHA)}\n"
            f"Duración: {orden.minutos:.2f} minutos"
        )
        messagebox.showinfo("Detalle de la orden", datos)

    def abrir_registro(self, orden=None):
        modificar = orden is not None
        ventana = tk.Toplevel(self.raiz)
        ventana.title("Modificar orden" if modificar else "Registrar orden")
        ventana.geometry("480x570")
        ventana.resizable(False, False)
        ventana.configure(bg=COLOR_PANEL)
        ventana.transient(self.raiz)
        ventana.grab_set()

        tk.Label(
            ventana,
            text="Modificar orden" if modificar else "Nueva orden de producción",
            font=("Segoe UI", 17, "bold"),
            bg=COLOR_PANEL, fg=COLOR_TEXTO
        ).pack(anchor="w", padx=28, pady=(22, 4))

        tk.Label(
            ventana,
            text="Completa los datos solicitados.",
            font=("Segoe UI", 9),
            bg=COLOR_PANEL, fg=COLOR_SECUNDARIO
        ).pack(anchor="w", padx=28, pady=(0, 15))

        campos = [
            ("Código (CIM-001)", "codigo"),
            ("Máquina (M-01)", "maquina"),
            ("Unidades procesadas", "procesadas"),
            ("Unidades de merma", "merma"),
            ("Inicio (DD-MM-AAAA HH:MM)", "inicio"),
            ("Fin (DD-MM-AAAA HH:MM)", "fin"),
        ]

        entradas = {}

        for etiqueta, clave in campos:
            tk.Label(
                ventana, text=etiqueta,
                font=("Segoe UI", 9, "bold"),
                bg=COLOR_PANEL, fg=COLOR_TEXTO
            ).pack(anchor="w", padx=30)

            entrada = tk.Entry(
                ventana, font=("Segoe UI", 10),
                relief="solid", bd=1
            )
            entrada.pack(fill="x", padx=30, pady=(4, 10), ipady=5)
            entradas[clave] = entrada

            if orden:
                valor = getattr(orden, clave)
                if clave in ("inicio", "fin"):
                    valor = valor.strftime(FORMATO_FECHA)
                entrada.insert(0, str(valor))

            if modificar and clave == "codigo":
                entrada.configure(state="readonly")

        def guardar():
            datos = {
                clave: entrada.get().strip()
                for clave, entrada in entradas.items()
            }

            try:
                if modificar:
                    ordenes.modificar(orden.codigo, datos, self.usuario)
                    mensaje = "La orden se modificó correctamente."
                else:
                    ordenes.registrar(datos, self.usuario)
                    mensaje = "La orden se registró correctamente."

                messagebox.showinfo("Operación completada", mensaje, parent=ventana)
                ventana.destroy()
                self.mostrar_inicio()

            except (ValueError, OSError) as error:
                messagebox.showerror("No se pudo guardar", str(error), parent=ventana)
            except Exception as error:
                messagebox.showerror("Error del sistema", str(error), parent=ventana)

        tk.Button(
            ventana, text="GUARDAR",
            command=guardar,
            bg=COLOR_AZUL, fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat", pady=10,
            cursor="hand2"
        ).pack(fill="x", padx=30, pady=15)

    def obtener_seleccion(self, tabla):
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning(
                "Selecciona una orden",
                "Primero selecciona una orden de la tabla."
            )
            return None

        return tabla.item(seleccion[0], "values")[0]

    def modificar_seleccion(self, tabla):
        codigo = self.obtener_seleccion(tabla)
        if codigo:
            orden = ordenes.consultar(codigo)
            if orden:
                self.abrir_registro(orden)

    def eliminar_seleccion(self, tabla):
        codigo = self.obtener_seleccion(tabla)
        if not codigo:
            return

        if not messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Deseas eliminar la orden {codigo}?"
        ):
            return

        try:
            ordenes.eliminar(codigo, self.usuario)
            messagebox.showinfo(
                "Orden eliminada",
                "La orden fue eliminada correctamente."
            )
            self.mostrar_ordenes()
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def mostrar_merma(self):
        self.limpiar()
        self.encabezado(
            "Órdenes por porcentaje de merma",
            "Órdenes ordenadas de mayor a menor porcentaje de merma."
        )

        columnas = [
            ("codigo", "Código", 110),
            ("maquina", "Máquina", 100),
            ("procesadas", "Procesadas", 120),
            ("buenas", "Buenas", 110),
            ("merma", "Merma", 100),
            ("porcentaje", "% Merma", 120),
            ("inicio", "Inicio", 150),
            ("fin", "Fin", 150),
            ("minutos", "Minutos", 100),
        ]

        tabla = self.crear_tabla(self.contenido, columnas, 18)
        self.cargar_ordenes(tabla, reportes.ordenes_por_merma())

    def mostrar_resumen(self):
        self.limpiar()
        self.encabezado(
            "Resumen por máquina",
            "Indicadores acumulados de producción para cada máquina."
        )

        columnas = [
            ("maquina", "Máquina", 120),
            ("ordenes", "Órdenes", 110),
            ("procesadas", "Procesadas", 150),
            ("merma", "Merma", 130),
            ("porcentaje", "% Merma", 130),
            ("minutos", "Minutos", 130),
        ]

        tabla = self.crear_tabla(self.contenido, columnas, 15)

        for maquina, datos in reportes.resumen_maquinas().items():
            tabla.insert("", "end", values=(
                maquina,
                datos["ordenes"],
                datos["procesadas"],
                datos["merma"],
                f"{datos['merma_pct']:.2f}%",
                f"{datos['minutos']:.2f}"
            ))

    def mostrar_auditoria(self):
        self.limpiar()
        self.encabezado(
            "Historial de auditoría",
            "Registro de las operaciones realizadas en el sistema."
        )

        marco = tk.Frame(self.contenido, bg=COLOR_PANEL)
        marco.pack(fill="both", expand=True, padx=30, pady=10)

        texto = tk.Text(
            marco, font=("Consolas", 9),
            bg="white", fg=COLOR_TEXTO,
            relief="flat", padx=15, pady=12,
            wrap="word"
        )
        barra = ttk.Scrollbar(marco, command=texto.yview)
        texto.configure(yscrollcommand=barra.set)

        texto.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        nombres = {
            "codigo": "Código",
            "maquina": "Máquina",
            "procesadas": "Unidades procesadas",
            "buenas": "Unidades buenas",
            "merma": "Unidades de merma",
            "merma_pct": "Porcentaje de merma",
            "inicio": "Fecha de inicio",
            "fin": "Fecha de finalización",
            "minutos": "Duración (minutos)"
        }

        registros = ordenes.historial()

        if not registros:
            texto.insert("end", "No existen registros de actividad.")
        else:
            for numero, fila in enumerate(registros, 1):
                try:
                    detalle = json.loads(fila["detalle"])
                except (TypeError, ValueError):
                    detalle = {}

                texto.insert("end", f"REGISTRO N. {numero}\n")
                texto.insert("end", "=" * 65 + "\n")
                texto.insert("end", f"Fecha: {fila['fecha']}\n")
                texto.insert("end", f"Usuario: {fila['usuario'] or 'Usuario eliminado'}\n")
                texto.insert("end", f"Acción: {fila['accion']}\n")

                if fila["accion"] == "MODIFICAR" and "antes" in detalle:
                    texto.insert("end", "\nCAMBIOS REALIZADOS:\n")
                    antes = detalle["antes"]
                    despues = detalle["despues"]

                    for campo, nombre in nombres.items():
                        anterior = antes.get(campo)
                        nuevo = despues.get(campo)

                        if anterior != nuevo:
                            if campo == "merma_pct":
                                anterior = f"{anterior:.2f}%"
                                nuevo = f"{nuevo:.2f}%"
                            texto.insert("end", f"  {nombre}: {anterior} -> {nuevo}\n")
                else:
                    texto.insert("end", "\nDATOS DE LA ORDEN:\n")
                    for campo, nombre in nombres.items():
                        if campo in detalle:
                            valor = detalle[campo]
                            if campo == "merma_pct":
                                valor = f"{valor:.2f}%"
                            texto.insert("end", f"  {nombre}: {valor}\n")

                texto.insert("end", "\n" + "-" * 65 + "\n\n")

        texto.configure(state="disabled")

    def exportar(self):
        try:
            ruta = reportes.generar_exportacion()
            messagebox.showinfo(
                "Exportación completada",
                f"El archivo Excel se generó correctamente:\n{ruta}"
            )
        except Exception as error:
            messagebox.showerror("Error de exportación", str(error))

    def cerrar_sesion(self):
        if messagebox.askyesno(
            "Cerrar sesión",
            "¿Deseas salir de Cimagraf?"
        ):
            self.raiz.destroy()

    def ejecutar(self):
        self.raiz.mainloop()


def ejecutar():
    usuario = mostrar_login()

    if usuario is not None:
        aplicacion = Aplicacion(usuario)
        aplicacion.ejecutar()


if __name__ == "__main__":
    ejecutar()

