from tkinter import *
from tkinter import messagebox
import sqlite3
from tkinter import ttk
import re


# ##############################################
# MODELO
# ##############################################


def conexion():
    con = sqlite3.connect("mibase.db")
    return con


def crear_tabla():
    con = conexion()
    cursor = con.cursor()
    sql = """CREATE TABLE aplicaciones
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             nombre varchar(100) NOT NULL,
             tipo varchar(20) NOT NULL,
             nivel int NOT NULL, 
             ruta varchar(200) NOT NULL,
             descripcion varchar(500) NOT NULL)
    """
    cursor.execute(sql)
    con.commit()


try:
    conexion()
    crear_tabla()
    messagebox.showinfo("CONEXION", "Base de Datos Creada exitosamente")

except:
    print("Hay un error")


def alta(nombre: str, tipo: str, nivel: int, ruta: str, descripcion: str, tree):
    patron_caracteres = "^[A-Za-záéíóú]*$"  # regex para el campo cadena
    patron_enteros = "[0-9]"  # regex para el campo entero
    # if re.match(patron_caracteres, nombre) & re.match(patron_enteros, nivel):
    if re.match(patron_caracteres, nombre):
        con = conexion()
        cursor = con.cursor()
        data = (nombre, tipo, nivel, ruta, descripcion)
        sql = "INSERT INTO aplicaciones (nombre, tipo, nivel, ruta, descripcion) VALUES(?, ?, ?, ?, ?)"
        cursor.execute(sql, data)
        con.commit()
        messagebox.showinfo("Alta", "Se guardo exitosamente")
        actualizar_treeview(tree)
    else:
        messagebox.showinfo("Alta", "Error al guardar, verifique los datos ingresados en el campo NOMBRE.")


def consultar(tree):
    actualizar_treeview(tree)


def modificar(tree):
    pass


def borrar(tree):
    valor = tree.selection()
    print(valor)  # ('I005',)
    item = tree.item(valor)
    print(item)  # {'text': 5, 'image': '', 'values': ['daSDasd', '13.0', '2.0'], 'open': 0, 'tags': ''}
    print(item['text'])
    mi_id = item['text']

    con = conexion()
    cursor = con.cursor()
    # mi_id = int(mi_id)
    data = (mi_id,)
    sql = "DELETE FROM aplicaciones WHERE id = ?;"
    cursor.execute(sql, data)
    con.commit()
    tree.delete(valor)


def actualizar_treeview(mitreview):
    records = mitreview.get_children()
    for element in records:
        mitreview.delete(element)

    sql = "SELECT * FROM aplicaciones ORDER BY id ASC"
    con = conexion()
    cursor = con.cursor()
    datos = cursor.execute(sql)

    resultado = datos.fetchall()
    for fila in resultado:
        print(fila)
        mitreview.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[5]))


# ##############################################
# VISTA
# ##############################################

root = Tk()
root.title("Tarea POO")

titulo = Label(root, text="Ingrese los datos de la aplicación", bg="#76B6E3", fg="White", height=1, width=60)
titulo.grid(row=0, column=0, columnspan=6, padx=1, pady=1, sticky=W + E)

nombre = Label(root, text="Nombre")
nombre.grid(row=1, column=0, sticky=W)
tipo = Label(root, text="Tipo")
tipo.grid(row=2, column=0, sticky=W)
nivel = Label(root, text="Nivel de Riesgo")
nivel.grid(row=3, column=0, sticky=W)
ruta = Label(root, text="Ruta del Log")
ruta.grid(row=4, column=0, sticky=W)
descripcion = Label(root, text="Descripción")
descripcion.grid(row=5, column=0, sticky=W)

# Defino variables para tomar valores de campos de entrada
nombre_val, tipo_val, nivel_val, ruta_val, descripcion_val = StringVar(), StringVar(), IntVar(), StringVar(), StringVar()
w_ancho = 20

entrada_nombre = Entry(root, textvariable=nombre_val, width=w_ancho)
entrada_nombre.grid(row=1, column=1)
entrada_tipo = Entry(root, textvariable=tipo_val, width=w_ancho)
entrada_tipo.grid(row=2, column=1)
entrada_nivel = Entry(root, textvariable=nivel_val, width=w_ancho)
entrada_nivel.grid(row=3, column=1)
entrada_ruta = Entry(root, textvariable=ruta_val, width=w_ancho)
entrada_ruta.grid(row=4, column=1)
entrada_descripcion = Entry(root, textvariable=descripcion_val, width=w_ancho)
entrada_descripcion.grid(row=5, column=1)

# --------------------------------------------------
# TREEVIEW
# --------------------------------------------------

tree = ttk.Treeview(root)
tree["columns"] = ("col1", "col2", "col3")
tree.column("#0", width=90, minwidth=50, anchor=W)
tree.column("col1", width=100, minwidth=80)
tree.column("col2", width=50, minwidth=80)
tree.column("col3", width=150, minwidth=80)
tree.heading("#0", text="ID")
tree.heading("col1", text="nombre")
tree.heading("col2", text="tipo")
tree.heading("col3", text="Descripción")

tree.grid(row=10, column=0, columnspan=4)

boton_alta = Button(root, text="Alta",
                    command=lambda: alta(nombre_val.get(), tipo_val.get(), nivel_val.get(), ruta_val.get(),
                                         descripcion_val.get(), tree))
boton_alta.grid(row=6, column=1)

boton_consulta = Button(root, text="Consultar", command=lambda: consultar(tree))
boton_consulta.grid(row=7, column=1)

boton_borrar = Button(root, text="Borrar", command=lambda: borrar(tree))
boton_borrar.grid(row=8, column=1)

boton_modificar = Button(root, text="Modificar", command=lambda: modificar(tree))
boton_modificar.grid(row=8, column=1)

root.mainloop()
