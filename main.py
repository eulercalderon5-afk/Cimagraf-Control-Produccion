import json
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from PIL import Image, ImageTk

from controllers.autenticacion import iniciar_sesion
from controllers import ordenes, reportes


COLOR_FONDO = "#F3F6FA"
COLOR_PANEL = "#FFFFFF"
COLOR_LATERAL = "#17263C"
COLOR_AZUL = "#2878D0"
COLOR_TEXTO = "#26364A"
COLOR_SECUNDARIO = "#718096"

FORMATO_FECHA = "%d/%m/%Y %H:%M"


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
    ventana.title("CIMA GRAF S.A.C. | Acceso")
    ventana.geometry("430x500")
    ventana.resizable(False, False)
    ventana.configure(bg=COLOR_LATERAL)

    x = (ventana.winfo_screenwidth() - 430) // 2
    y = (ventana.winfo_screenheight() - 500) // 2
    ventana.geometry(f"430x500+{x}+{y}")

    panel = tk.Frame(ventana, bg="#20334F", padx=35, pady=30)
    panel.pack(fill="both", expand=True, padx=25, pady=25)

    tk.Label(
        panel, text="CIMA GRAF",
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
        self.raiz.title("CIMA GRAF S.A.C. | Control de producción")
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
            lateral, text="CIMA GRAF",
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
        from pathlib import Path

        self.limpiar()

        contenedor = tk.Frame(self.contenido, bg=COLOR_FONDO)
        contenedor.pack(fill="both", expand=True, padx=35, pady=25)

        portada = tk.Frame(
            contenedor, bg=COLOR_PANEL,
            highlightbackground="#E2E8F0", highlightthickness=1
        )
        portada.pack(fill="both", expand=True)

        centro = tk.Frame(portada, bg=COLOR_PANEL)
        centro.pack(expand=True, pady=15)

        ruta_logo = Path(__file__).resolve().parent / "assets" / "logo_cimagraf.jpeg"
        self.logo_imagen = None

        if ruta_logo.exists():
            try:
                imagen = Image.open(ruta_logo).convert("RGB")
                imagen.thumbnail((250, 155), Image.Resampling.LANCZOS)
                self.logo_imagen = ImageTk.PhotoImage(imagen)
                tk.Label(
                    centro, image=self.logo_imagen,
                    bg=COLOR_PANEL
                ).pack(pady=(5, 14))
            except Exception:
                tk.Label(
                    centro, text="CIMA GRAF",
                    font=("Segoe UI", 25, "bold"),
                    bg=COLOR_PANEL, fg=COLOR_LATERAL
                ).pack(pady=15)
        else:
            tk.Label(
                centro, text="CIMA GRAF",
                font=("Segoe UI", 25, "bold"),
                bg=COLOR_PANEL, fg=COLOR_LATERAL
            ).pack(pady=15)

        tk.Label(
            centro, text="CIMA GRAF S.A.C.",
            font=("Segoe UI", 24, "bold"),
            bg=COLOR_PANEL, fg=COLOR_LATERAL
        ).pack(pady=(0, 5))

        tk.Label(
            centro, text="SOLUCIONES GRÁFICAS",
            font=("Segoe UI", 11, "bold"),
            bg=COLOR_PANEL, fg=COLOR_AZUL
        ).pack(pady=3)

        tk.Label(
            centro,
            text="Sistema de gestión y control de producción",
            font=("Segoe UI", 10),
            bg=COLOR_PANEL, fg=COLOR_SECUNDARIO
        ).pack(pady=(4, 20))

        tk.Frame(
            centro, bg="#E2E8F0", height=1, width=430
        ).pack(pady=(0, 17))

        tk.Label(
            centro, text="HORARIO DE ATENCIÓN",
            font=("Segoe UI", 11, "bold"),
            bg=COLOR_PANEL, fg=COLOR_LATERAL
        ).pack(pady=(0, 12))

        horarios = tk.Frame(centro, bg=COLOR_PANEL)
        horarios.pack()

        for dia, horario in [
            ("LUNES A VIERNES", "08:30 a. m. – 01:30 p. m.  |  03:00 p. m. – 08:00 p. m."),
            ("SÁBADOS", "08:30 a. m. – 12:00 p. m."),
            ("DOMINGOS", "No hay atención"),
        ]:
            fila = tk.Frame(horarios, bg=COLOR_PANEL)
            fila.pack(fill="x", pady=5)

            tk.Label(
                fila, text=dia, width=19, anchor="w",
                font=("Segoe UI", 9, "bold"),
                bg=COLOR_PANEL, fg=COLOR_TEXTO
            ).pack(side="left")

            tk.Label(
                fila, text=horario, anchor="w",
                font=("Segoe UI", 9),
                bg=COLOR_PANEL, fg=COLOR_SECUNDARIO
            ).pack(side="left", padx=8)

        tk.Label(
            portada, text="CALIDAD • COMPROMISO • PRODUCCIÓN",
            font=("Segoe UI", 8, "bold"),
            bg=COLOR_PANEL, fg=COLOR_AZUL
        ).pack(side="bottom", pady=18)


    def mostrar_ordenes(self):
        self.limpiar()
        self.encabezado(
            "Órdenes de producción",
            "Busca, revisa y administra los registros de producción."
        )

        ordenes_actuales = ordenes.listar()

        barra = tk.Frame(self.contenido, bg=COLOR_FONDO)
        barra.pack(fill="x", padx=25, pady=8)

        busqueda = tk.Entry(barra, font=("Segoe UI", 10), relief="solid", bd=1)
        busqueda.pack(side="left", fill="x", expand=True, ipady=7)
        busqueda.insert(0, "Buscar por código o máquina...")

        maquinas = ["Todas"] + sorted(set(o.maquina for o in ordenes_actuales))
        filtro = ttk.Combobox(
            barra, values=maquinas, state="readonly", width=15
        )
        filtro.set("Todas")
        filtro.pack(side="left", padx=10)


        area = tk.Frame(self.contenido, bg=COLOR_FONDO)
        area.pack(fill="both", expand=True, padx=25, pady=5)

        lienzo = tk.Canvas(area, bg=COLOR_FONDO, highlightthickness=0)
        scroll = ttk.Scrollbar(area, orient="vertical", command=lienzo.yview)
        lista = tk.Frame(lienzo, bg=COLOR_FONDO)

        ventana_lista = lienzo.create_window((0, 0), window=lista, anchor="nw")
        lista.bind("<Configure>", lambda e: lienzo.configure(
            scrollregion=lienzo.bbox("all")
        ))
        lienzo.bind("<Configure>", lambda e: lienzo.itemconfigure(
            ventana_lista, width=e.width
        ))
        lienzo.configure(yscrollcommand=scroll.set)

        lienzo.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        def dibujar(event=None):
            for widget in lista.winfo_children():
                widget.destroy()

            termino = busqueda.get().strip().lower()
            maquina = filtro.get()

            encontrados = [
                o for o in ordenes_actuales
                if (termino in o.codigo.lower() or termino in o.maquina.lower()
                    or termino == "buscar por código o máquina...")
                and (maquina == "Todas" or o.maquina == maquina)
            ]

            if not encontrados:
                tk.Label(
                    lista, text="No se encontraron Órdenes.",
                    bg=COLOR_FONDO, fg=COLOR_SECUNDARIO,
                    font=("Segoe UI", 11)
                ).pack(pady=35)
                return

            for o in encontrados:
                tarjeta = tk.Frame(
                    lista, bg=COLOR_PANEL,
                    highlightbackground="#E2E8F0", highlightthickness=1
                )
                tarjeta.pack(fill="x", pady=5)

                superior = tk.Frame(tarjeta, bg=COLOR_PANEL)
                superior.pack(fill="x", padx=15, pady=(12, 5))

                tk.Label(
                    superior, text=o.codigo,
                    font=("Segoe UI", 12, "bold"),
                    bg=COLOR_PANEL, fg=COLOR_LATERAL
                ).pack(side="left")

                tk.Label(
                    superior, text=o.maquina,
                    font=("Segoe UI", 9, "bold"),
                    bg="#EAF2FC", fg=COLOR_AZUL, padx=9, pady=4
                ).pack(side="left", padx=12)

                tk.Label(
                    superior, text=f"Merma: {o.merma_pct:.2f}%",
                    font=("Segoe UI", 9, "bold"),
                    bg=COLOR_PANEL,
                    fg="#C45151" if o.merma_pct >= 10 else COLOR_SECUNDARIO
                ).pack(side="right")

                datos = tk.Frame(tarjeta, bg=COLOR_PANEL)
                datos.pack(fill="x", padx=15, pady=5)

                for titulo, valor in [
                    ("Procesadas", f"{o.procesadas:,}"),
                    ("Unidades buenas", f"{o.buenas:,}"),
                    ("Merma", f"{o.merma:,}"),
                    ("Duración", f"{o.minutos:.0f} min"),
                ]:
                    bloque = tk.Frame(datos, bg=COLOR_PANEL)
                    bloque.pack(side="left", expand=True, anchor="w")
                    tk.Label(
                        bloque, text=titulo, bg=COLOR_PANEL,
                        fg=COLOR_SECUNDARIO, font=("Segoe UI", 8)
                    ).pack(anchor="w")
                    tk.Label(
                        bloque, text=valor, bg=COLOR_PANEL,
                        fg=COLOR_TEXTO, font=("Segoe UI", 10, "bold")
                    ).pack(anchor="w", pady=3)

                acciones = tk.Frame(tarjeta, bg=COLOR_PANEL)
                acciones.pack(fill="x", padx=15, pady=(5, 12))

                tk.Button(
                    acciones, text="Ver detalle",
                    command=lambda c=o.codigo: self.ver_detalle(c),
                    relief="flat", fg=COLOR_AZUL, bg="#EAF2FC"
                ).pack(side="left", padx=(0, 6))

                tk.Button(
                    acciones, text="Modificar",
                    command=lambda c=o.codigo: self.abrir_registro(
                        ordenes.consultar(c)
                    ),
                    relief="flat", bg="#F1F4F8", fg=COLOR_TEXTO
                ).pack(side="left", padx=6)

                def eliminar(codigo=o.codigo):
                    if messagebox.askyesno(
                        "Confirmar eliminación",
                        f"¿Deseas eliminar la orden {codigo}?"
                    ):
                        try:
                            ordenes.eliminar(codigo, self.usuario)
                            messagebox.showinfo(
                                "Orden eliminada", "La orden se eliminó correctamente."
                            )
                            self.mostrar_ordenes()
                        except Exception as error:
                            messagebox.showerror("Error", str(error))

                tk.Button(
                    acciones, text="Eliminar",
                    command=eliminar, relief="flat",
                    bg="#FCEBEC", fg="#B83D45"
                ).pack(side="right")

        tk.Button(
            barra, text="Buscar", command=dibujar,
            bg=COLOR_AZUL, fg="white", relief="flat",
            font=("Segoe UI", 9, "bold"), padx=22, pady=8
        ).pack(side="right", padx=(8, 0))

        busqueda.bind("<KeyRelease>", dibujar)
        busqueda.bind("<Return>", dibujar)
        filtro.bind("<<ComboboxSelected>>", dibujar)
        dibujar()


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
            ("Inicio (DD/MM/AAAA HH:MM)", "inicio"),
            ("Fin (DD/MM/AAAA HH:MM)", "fin"),
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
            "Control de merma",
            "Identifica las Órdenes con mayor proporción de unidades desperdiciadas."
        )

        filas = reportes.ordenes_por_merma()

        resumen = tk.Frame(self.contenido, bg=COLOR_FONDO)
        resumen.pack(fill="x", padx=25, pady=10)

        total = len(filas)
        merma_total = sum(o.merma for o in filas)
        procesadas = sum(o.procesadas for o in filas)
        porcentaje = merma_total * 100 / procesadas if procesadas else 0

        for titulo, valor in [
            ("Órdenes revisadas", total),
            ("Unidades de merma", f"{merma_total:,}"),
            ("Merma acumulada", f"{porcentaje:.2f}%"),
        ]:
            tarjeta = tk.Frame(
                resumen, bg=COLOR_PANEL,
                highlightbackground="#E2E8F0", highlightthickness=1
            )
            tarjeta.pack(side="left", expand=True, fill="x", padx=5)
            tk.Label(
                tarjeta, text=titulo, bg=COLOR_PANEL,
                fg=COLOR_SECUNDARIO, font=("Segoe UI", 9)
            ).pack(anchor="w", padx=14, pady=(10, 3))
            tk.Label(
                tarjeta, text=str(valor), bg=COLOR_PANEL,
                fg=COLOR_AZUL, font=("Segoe UI", 18, "bold")
            ).pack(anchor="w", padx=14, pady=(0, 10))

        area = tk.Frame(self.contenido, bg=COLOR_FONDO)
        area.pack(fill="both", expand=True, padx=25, pady=8)

        lienzo = tk.Canvas(area, bg=COLOR_FONDO, highlightthickness=0)
        scroll = ttk.Scrollbar(area, orient="vertical", command=lienzo.yview)
        lista = tk.Frame(lienzo, bg=COLOR_FONDO)
        ventana = lienzo.create_window((0, 0), window=lista, anchor="nw")

        lista.bind("<Configure>", lambda e: lienzo.configure(
            scrollregion=lienzo.bbox("all")
        ))
        lienzo.bind("<Configure>", lambda e: lienzo.itemconfigure(
            ventana, width=e.width
        ))
        lienzo.configure(yscrollcommand=scroll.set)
        lienzo.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        if not filas:
            tk.Label(
                lista, text="No hay Órdenes registradas.",
                bg=COLOR_FONDO, fg=COLOR_SECUNDARIO
            ).pack(pady=30)
            return

        for o in filas:
            if o.merma_pct >= 10:
                nivel, color, fondo = "Mayor porcentaje", "#B83D45", "#FCEBEC"
            elif o.merma_pct >= 5:
                nivel, color, fondo = "Porcentaje intermedio", "#A66B17", "#FFF4DF"
            else:
                nivel, color, fondo = "Menor porcentaje", "#27845C", "#E8F5EE"

            tarjeta = tk.Frame(
                lista, bg=COLOR_PANEL,
                highlightbackground="#E2E8F0", highlightthickness=1
            )
            tarjeta.pack(fill="x", pady=5)

            encabezado = tk.Frame(tarjeta, bg=COLOR_PANEL)
            encabezado.pack(fill="x", padx=15, pady=10)

            tk.Label(
                encabezado, text=f"{o.codigo}  |  {o.maquina}",
                bg=COLOR_PANEL, fg=COLOR_TEXTO,
                font=("Segoe UI", 11, "bold")
            ).pack(side="left")

            tk.Label(
                encabezado, text=f"{o.merma_pct:.2f}%  |  {nivel}",
                bg=fondo, fg=color, padx=9, pady=5,
                font=("Segoe UI", 9, "bold")
            ).pack(side="right")

            tk.Label(
                tarjeta,
                text=f"Procesadas: {o.procesadas:,}     "
                     f"Buenas: {o.buenas:,}     Merma: {o.merma:,}",
                bg=COLOR_PANEL, fg=COLOR_SECUNDARIO,
                font=("Segoe UI", 9)
            ).pack(anchor="w", padx=15, pady=(0, 10))

            tk.Button(
                tarjeta, text="Consultar orden",
                command=lambda c=o.codigo: self.ver_detalle(c),
                bg="#EAF2FC", fg=COLOR_AZUL, relief="flat"
            ).pack(anchor="e", padx=15, pady=(0, 10))


    def mostrar_resumen(self):
        self.limpiar()
        self.encabezado(
            "Resumen por máquina",
            "Comparación de producción, unidades buenas y merma."
        )

        resumen = reportes.resumen_maquinas()
        if not resumen:
            tk.Label(
                self.contenido, text="Todavía no hay datos para mostrar.",
                bg=COLOR_FONDO, fg=COLOR_SECUNDARIO,
                font=("Segoe UI", 11)
            ).pack(pady=50)
            return

        total_procesadas = sum(d["procesadas"] for d in resumen.values())
        total_merma = sum(d["merma"] for d in resumen.values())
        total_buenas = total_procesadas - total_merma

        indicadores = tk.Frame(self.contenido, bg=COLOR_FONDO)
        indicadores.pack(fill="x", padx=25, pady=10)

        for titulo, valor, color in [
            ("Máquinas registradas", len(resumen), COLOR_AZUL),
            ("Unidades procesadas", f"{total_procesadas:,}", COLOR_LATERAL),
            ("Unidades buenas", f"{total_buenas:,}", "#27845C"),
            ("Unidades de merma", f"{total_merma:,}", "#C45151"),
        ]:
            tarjeta = tk.Frame(
                indicadores, bg=COLOR_PANEL,
                highlightbackground="#E2E8F0", highlightthickness=1
            )
            tarjeta.pack(side="left", fill="both", expand=True, padx=5)
            tk.Label(
                tarjeta, text=titulo, bg=COLOR_PANEL,
                fg=COLOR_SECUNDARIO, font=("Segoe UI", 8)
            ).pack(anchor="w", padx=12, pady=(12, 3))
            tk.Label(
                tarjeta, text=str(valor), bg=COLOR_PANEL,
                fg=color, font=("Segoe UI", 18, "bold")
            ).pack(anchor="w", padx=12, pady=(0, 12))

        zona = tk.Frame(self.contenido, bg=COLOR_PANEL)
        zona.pack(fill="both", expand=True, padx=30, pady=12)

        tk.Label(
            zona, text="COMPARACIÓN DE PRODUCCIÓN POR M?QUINA",
            bg=COLOR_PANEL, fg=COLOR_TEXTO,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", padx=18, pady=15)

        maximo = max(d["procesadas"] for d in resumen.values()) or 1

        for maquina, d in resumen.items():
            fila = tk.Frame(zona, bg=COLOR_PANEL)
            fila.pack(fill="x", padx=18, pady=9)

            tk.Label(
                fila, text=maquina, width=12, anchor="w",
                bg=COLOR_PANEL, fg=COLOR_TEXTO,
                font=("Segoe UI", 9, "bold")
            ).pack(side="left")

            barras = tk.Frame(fila, bg="#EDF1F6", height=18)
            barras.pack(side="left", fill="x", expand=True, padx=10)
            barras.pack_propagate(False)

            proporcion = d["procesadas"] / maximo
            ancho_total = max(1, int(400 * proporcion))
            buenas = d["procesadas"] - d["merma"]
            ancho_buenas = int(ancho_total * buenas / d["procesadas"]) if d["procesadas"] else 0

            tk.Frame(
                barras, bg="#2878D0", width=ancho_buenas
            ).pack(side="left", fill="y")
            tk.Frame(
                barras, bg="#D65B61",
                width=max(0, ancho_total - ancho_buenas)
            ).pack(side="left", fill="y")

            tk.Label(
                fila, text=f'{d["procesadas"]:,} unidades',
                width=15, anchor="e", bg=COLOR_PANEL,
                fg=COLOR_TEXTO, font=("Segoe UI", 8)
            ).pack(side="right")

            tk.Label(
                zona,
                text=f'{d["ordenes"]} Órdenes  |  {buenas:,} buenas  |  '
                     f'{d["merma"]:,} merma  |  {d["merma_pct"]:.2f}% de merma',
                bg=COLOR_PANEL, fg=COLOR_SECUNDARIO,
                font=("Segoe UI", 8)
            ).pack(anchor="w", padx=145)

        tk.Label(
            zona, text="Azul: unidades buenas     Rojo: unidades de merma",
            bg=COLOR_PANEL, fg=COLOR_SECUNDARIO,
            font=("Segoe UI", 8)
        ).pack(anchor="w", padx=18, pady=15)


    def mostrar_auditoria(self):
        self.limpiar()
        self.encabezado(
            "Historial de auditoría",
            "Consulta cronológicamente las operaciones realizadas en el sistema."
        )

        registros = ordenes.historial()

        area = tk.Frame(self.contenido, bg=COLOR_FONDO)
        area.pack(fill="both", expand=True, padx=25, pady=10)

        lienzo = tk.Canvas(area, bg=COLOR_FONDO, highlightthickness=0)
        scroll = ttk.Scrollbar(area, orient="vertical", command=lienzo.yview)
        lista = tk.Frame(lienzo, bg=COLOR_FONDO)
        ventana = lienzo.create_window((0, 0), window=lista, anchor="nw")

        lista.bind("<Configure>", lambda e: lienzo.configure(
            scrollregion=lienzo.bbox("all")
        ))
        lienzo.bind("<Configure>", lambda e: lienzo.itemconfigure(
            ventana, width=e.width
        ))
        lienzo.configure(yscrollcommand=scroll.set)
        lienzo.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        if not registros:
            tk.Label(
                lista, text="Todavía no existen actividades registradas.",
                bg=COLOR_FONDO, fg=COLOR_SECUNDARIO,
                font=("Segoe UI", 11)
            ).pack(pady=35)
            return

        nombres = {
            "codigo": "Código", "maquina": "Máquina",
            "procesadas": "Unidades procesadas",
            "buenas": "Unidades buenas", "merma": "Unidades de merma",
            "merma_pct": "Porcentaje de merma",
            "inicio": "Inicio", "fin": "Finalización",
            "minutos": "Duración (minutos)"
        }

        for numero, fila in enumerate(registros, 1):
            try:
                detalle = json.loads(fila["detalle"])
            except (TypeError, ValueError):
                detalle = {}

            tarjeta = tk.Frame(
                lista, bg=COLOR_PANEL,
                highlightbackground="#E2E8F0", highlightthickness=1
            )
            tarjeta.pack(fill="x", pady=5)

            superior = tk.Frame(tarjeta, bg=COLOR_PANEL)
            superior.pack(fill="x", padx=15, pady=(12, 5))

            tk.Label(
                superior, text=f"ACTIVIDAD {numero:03d}",
                bg=COLOR_PANEL, fg=COLOR_AZUL,
                font=("Segoe UI", 9, "bold")
            ).pack(side="left")

            tk.Label(
                superior, text=str(fila["accion"]),
                bg="#EAF2FC", fg=COLOR_AZUL,
                font=("Segoe UI", 9, "bold"), padx=9, pady=4
            ).pack(side="right")

            tk.Label(
                tarjeta, text=f"Fecha: {fila['fecha']}",
                bg=COLOR_PANEL, fg=COLOR_TEXTO,
                font=("Segoe UI", 9, "bold")
            ).pack(anchor="w", padx=15, pady=3)

            tk.Label(
                tarjeta,
                text=f"Usuario: {fila['usuario'] or 'Usuario eliminado'}",
                bg=COLOR_PANEL, fg=COLOR_SECUNDARIO,
                font=("Segoe UI", 9)
            ).pack(anchor="w", padx=15, pady=3)

            if "antes" in detalle and "despues" in detalle:
                tk.Label(
                    tarjeta, text="Cambios realizados:",
                    bg=COLOR_PANEL, fg=COLOR_TEXTO,
                    font=("Segoe UI", 9, "bold")
                ).pack(anchor="w", padx=15, pady=(8, 3))

                antes, despues = detalle["antes"], detalle["despues"]
                for campo, nombre in nombres.items():
                    if antes.get(campo) != despues.get(campo):
                        tk.Label(
                            tarjeta,
                            text=f"• {nombre}: {antes.get(campo)}  →  {despues.get(campo)}",
                            bg=COLOR_PANEL, fg=COLOR_SECUNDARIO,
                            font=("Segoe UI", 9)
                        ).pack(anchor="w", padx=25, pady=2)
            else:
                for campo, nombre in nombres.items():
                    if campo in detalle:
                        tk.Label(
                            tarjeta, text=f"{nombre}: {detalle[campo]}",
                            bg=COLOR_PANEL, fg=COLOR_SECUNDARIO,
                            font=("Segoe UI", 9)
                        ).pack(anchor="w", padx=15, pady=2)

            tk.Frame(tarjeta, bg=COLOR_PANEL, height=8).pack()


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
