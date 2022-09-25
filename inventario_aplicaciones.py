import tkinter
from tkinter import *
from tkinter import messagebox
import sqlite3
from tkinter import ttk
import re

# ##############################################
# MODELO
# ##############################################
from tkinter.messagebox import OK


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


def valid_string(nombre_campo: str, cadena: str) -> str:
    patron_string = "^[A-Za-záéíóú]*$"
    if not re.match(patron_string, cadena):
        return f"El {nombre_campo} tiene caracteres inválidos. Solo se pueden ingresar letras de la a la z \n"
    else:
        return ''


def valid_int(nombre_campo: str, cadena: str) -> str:
    patron_num = '^([0-9])*$'
    if not re.match(patron_num, cadena):
        return f"El {nombre_campo} tiene caracteres inválidos. Solo se pueden números \n"
    else:
        return ''


def alta(id, nombre: str, tipo: str, nivel, ruta: str, descripcion: str, tree):
    errores: str = ''
    errores += valid_string('Nombre de la Aplicación', nombre)
    errores += valid_int('Nivel de Riesgo', nivel)
    if errores == '':
        #Hacer el Alta o la Modificación
        if boton_alta['text'] == "Actualizar":
            con = conexion()
            cursor = con.cursor()
            data = ( nombre, tipo, nivel, ruta, descripcion, id)
            sql = "UPDATE aplicaciones SET nombre = ?, tipo = ? , nivel = ?, ruta = ?, descripcion = ? WHERE id = ?"
            cursor.execute(sql, data)
            con.commit()
            messagebox.showinfo("Modificación", "Se actualizó exitosamente")
            actualizar_treeview(tree)
        else:
            con = conexion()
            cursor = con.cursor()
            data = (nombre, tipo, nivel, ruta, descripcion)
            sql = "INSERT INTO aplicaciones (nombre, tipo, nivel, ruta, descripcion) VALUES(?, ?, ?, ?, ?)"
            cursor.execute(sql, data)
            con.commit()
            messagebox.showinfo("Alta", "Se guardó exitosamente")
            actualizar_treeview(tree)
    else:
        messagebox.showinfo("Alta", errores)


def consultar(tree):
    actualizar_treeview(tree)


def modificar(tree):
    valor = tree.selection()
    item = tree.item(valor)
    my_id = item['text']
    app_sel = buscar_una_app(my_id)
    id_val.set(my_id)
    nombre_val.set(app_sel[1])
    tipo_val.set(app_sel[2])
    nivel_val.set(app_sel[3])
    ruta_val.set(app_sel[4])
    descripcion_val.set(app_sel[5])
    boton_alta['text'] = "Actualizar"


def borrar(tree):
    valor = tree.selection()
    item = tree.item(valor)
    mi_id = item['text']
    if messagebox.askokcancel("Atencion", f"Está seguro que desea eliminar la Aplicacion con ID: {mi_id}"):
        con = conexion()
        cursor = con.cursor()
        # mi_id = int(mi_id)
        data = (mi_id,)
        sql = "DELETE FROM aplicaciones WHERE id = ?;"
        cursor.execute(sql, data)
        con.commit()
        tree.delete(valor)
        messagebox.showinfo("Atención", f"La aplicación {mi_id} se eliminó correctamente")


def edit_form():
    pass


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
        mitreview.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[5]))


def buscar_una_app( id ):
    sql = f"SELECT * FROM aplicaciones WHERE id = {id}"
    con = conexion()
    cursor = con.cursor()
    datos = cursor.execute(sql)
    resultado = datos.fetchone()
    return resultado

# ##############################################
# VISTA
# ##############################################

#Defino ventana principal de la Aplicación
root = Tk()

#Título, tamaño y color de la ventana principal
root.title("Inventario de Aplicaciones")
root.geometry("560x485")
root.config(bg="#FFFDFD")

#Título del cuadro principal
titulo = Label(root, text="Ingrese los datos de la Aplicación", bg="#76B6E3", fg="White", height=1, width=80)
#Título del cuadro detalle
titulo_detalle = Label(root, text="Listado de Aplicaciones", bg="#76B6E3", fg="White", height=1, width=80)

# Defino variables para tomar valores de campos de entrada
id_val, nombre_val, tipo_val, nivel_val, ruta_val, descripcion_val = IntVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
w_ancho = 50

# Etiquetas / Labels:
id = Label(root, text="ID",bg="#FFFDFD")
nombre = Label(root, text="Nombre",bg="#FFFDFD")
tipo = Label(root, text="Tipo",bg="#FFFDFD")
nivel = Label(root, text="Nivel de Riesgo",bg="#FFFDFD")
ruta = Label(root, text="Ruta del Log",bg="#FFFDFD")
descripcion = Label(root, text="Descripción",bg="#FFFDFD")

# Campos de ingreso de información / Entries:
entrada_id = Entry(root, textvariable=id_val, state="readonly", width=10)
entrada_nombre = Entry(root, textvariable=nombre_val, width=w_ancho)
entrada_tipo = Entry(root, textvariable=tipo_val, width=w_ancho)
entrada_nivel = Entry(root, textvariable=nivel_val, width=w_ancho)
entrada_ruta = Entry(root, textvariable=ruta_val, width=w_ancho)
entrada_descripcion = Entry(root, textvariable=descripcion_val, width=w_ancho)

# Botones / Buttons:
boton_alta = Button(
    root,
    text="Agregar",
    command=lambda: alta(
        id_val.get(),
        nombre_val.get(),
        tipo_val.get(),
        nivel_val.get(),
        ruta_val.get(),
        descripcion_val.get(),
        tree)
    )
boton_consulta = Button(root, text="Consultar", command=lambda: consultar(tree))
boton_borrar = Button(root, text="Borrar", command=lambda: borrar(tree))
boton_modificar = Button(root, text="Modificar", command=lambda: modificar(tree))
boton_salir = Button(root, text="Salir", command=root.quit)

# --------------------------------------------------
# TREEVIEW
# --------------------------------------------------

tree = ttk.Treeview(root)

# Posición de etiquetas, campos de entrada y botones /Labels, Entries, Buttons
#Título
titulo.grid(row=0, column=0, columnspan=6, padx=1, pady=1, sticky=W + E)

#Labels
id.grid(row=1, column=1)
nombre.grid(row=2, column=1, sticky=E)
tipo.grid(row=3, column=1, sticky=E)
nivel.grid(row=4, column=1, sticky=E)
ruta.grid(row=5, column=1, sticky=E)
descripcion.grid(row=6, column=1, sticky=E)
#Entries
entrada_id.grid(row=1, column=2)
entrada_nombre.grid(row=2, column=2)
entrada_tipo.grid(row=3, column=2)
entrada_nivel.grid(row=4, column=2)
entrada_ruta.grid(row=5, column=2)
entrada_descripcion.grid(row=6, column=2)
#Buttons
boton_alta.grid(row=7, column=2, sticky=EW)

#Título Detalle
titulo_detalle.grid(row=8, column=0, columnspan=6, padx=1, pady=1, sticky=W + E)
boton_consulta.grid(row=9, columnspan=1, column=1, sticky=EW)

#Árbol de información
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

boton_borrar.grid(row=15, column=1, sticky=EW)
boton_modificar.grid(row=15, column=2, sticky=EW)
boton_salir.grid(row=15, column=4, sticky=EW)

root.mainloop()
