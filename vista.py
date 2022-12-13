from tkinter import ttk
from tkinter import Label
from tkinter import IntVar
from tkinter import StringVar
from tkinter import Entry
from tkinter import Button
from tkinter import W
from tkinter import E
from tkinter import EW
from utils import Utils
from modelo import Abmc


class VistaInventario:
    def __init__(self, window):
        self.root = window
        # Creo el objeto ABMC
        self.abmc = Abmc()
        # ##############################################
        # VISTA
        # ##############################################
        #Creamos el objeto utilidades
        utilidades = Utils()       

        # Título, tamaño y color de la ventana principal
        self.root.title("Inventario de Aplicaciones")
        self.root.geometry("560x485")
        self.root.config(bg="#FFFDFD")

        # Título del cuadro principal
        titulo = Label(self.root, text="Ingrese los datos de la Aplicación", bg="#76B6E3", fg="White", height=1,
                    width=80)
        # Título del cuadro detalle
        titulo_detalle = Label(self.root, text="Listado de Aplicaciones", bg="#76B6E3", fg="White", height=1, width=80)

        # Defino variables para tomar valores de campos de entrada
        id_val, nombre_val, tipo_val = IntVar(), StringVar(), StringVar()
        nivel_val, ruta_val, descripcion_val = IntVar(), StringVar(), StringVar()

        w_ancho = 50

        # Etiquetas / Labels:
        id = Label(self.root, text="ID", bg="#FFFDFD")
        nombre = Label(self.root, text="Nombre", bg="#FFFDFD")
        tipo = Label(self.root, text="Tipo", bg="#FFFDFD")
        nivel = Label(self.root, text="Nivel de Riesgo", bg="#FFFDFD")
        ruta = Label(self.root, text="Ruta del Log", bg="#FFFDFD")
        descripcion = Label(self.root, text="Descripción", bg="#FFFDFD")

        # Campos de ingreso de información / Entries:
        entrada_id = Entry(self.root, textvariable=id_val, state="readonly", width=10)
        entrada_nombre = Entry(self.root, textvariable=nombre_val, width=w_ancho)
        entrada_tipo = Entry(self.root, textvariable=tipo_val, width=w_ancho)
        #utlizamos el metodo validate_entry para realizar las validaciones de regex
        entrada_nivel = Entry(self.root, textvariable=nivel_val, width=w_ancho, validate="key",
                            validatecommand=(self.root.register(utilidades.validate_entry), "%S", "%P")
                            )

        entrada_ruta = Entry(self.root, textvariable=ruta_val, width=w_ancho)
        entrada_descripcion = Entry(self.root, textvariable=descripcion_val, width=w_ancho)

        # Botones / Buttons:
        boton_alta = Button(
            self.root,
            text="Agregar",
            command=lambda: self.abmc.alta(
                id_val.get(),
                nombre_val.get(),
                tipo_val.get(),
                nivel_val.get(),
                ruta_val.get(),
                descripcion_val.get(),
                tree, boton_alta)
        )
        boton_consulta = Button(self.root, text="Consultar", command=lambda: self.abmc.consultar(tree))
        boton_borrar = Button(self.root, text="Borrar", command=lambda: self.abmc.borrar(tree))
        boton_modificar = Button(self.root, text="Modificar",
                                 command=lambda: self.abmc.modificar(tree, boton_alta, id_val, nombre_val, tipo_val,
                                                                     nivel_val, ruta_val, descripcion_val))
        boton_limpiar = Button(self.root, text="Limpiar campos",
                               command=lambda: self.abmc.limpiar(tree, boton_alta, id_val, nombre_val, tipo_val,
                                                                 nivel_val, ruta_val, descripcion_val))
        boton_salir = Button(self.root, text="Salir", command=self.root.quit)

        # --------------------------------------------------
        # TREEVIEW
        # --------------------------------------------------

        tree = ttk.Treeview(self.root)

        # Posición de etiquetas, campos de entrada y botones /Labels, Entries, Buttons
        # Título
        titulo.grid(row=0, column=0, columnspan=6, padx=1, pady=1, sticky=W + E)

        # Labels
        id.grid(row=1, column=1)
        nombre.grid(row=2, column=1, sticky=E)
        tipo.grid(row=3, column=1, sticky=E)
        nivel.grid(row=4, column=1, sticky=E)
        ruta.grid(row=5, column=1, sticky=E)
        descripcion.grid(row=6, column=1, sticky=E)
        # Entries
        entrada_id.grid(row=1, column=2)
        entrada_nombre.grid(row=2, column=2)
        entrada_tipo.grid(row=3, column=2)
        entrada_nivel.grid(row=4, column=2)
        entrada_ruta.grid(row=5, column=2)
        entrada_descripcion.grid(row=6, column=2)

        # Buttons
        boton_alta.grid(row=7, column=2, sticky=EW)
        boton_limpiar.grid(row=3, column=3, sticky=EW)
        boton_borrar.grid(row=15, column=1, sticky=EW)
        boton_modificar.grid(row=15, column=2, sticky=EW)
        boton_salir.grid(row=15, column=4, sticky=EW)

        # Título Detalle
        titulo_detalle.grid(row=8, column=0, columnspan=6, padx=1, pady=1, sticky=W + E)
        boton_consulta.grid(row=9, columnspan=1, column=1, sticky=EW)

        # Árbol de información
        tree.grid(row=10, column=1, columnspan=4)
        tree["columns"] = ("col1", "col2", "col3")
        tree.column("#0", width=90, minwidth=50, anchor=W)
        tree.column("col1", width=100, minwidth=80)
        tree.column("col2", width=50, minwidth=80)
        tree.column("col3", width=250, minwidth=80)
        tree.heading("#0", text="ID")
        tree.heading("col1", text="Nombre")
        tree.heading("col2", text="Tipo")
        tree.heading("col3", text="Descripción")
