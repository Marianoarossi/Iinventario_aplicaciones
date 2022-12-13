from utils import Utils
from db_functions import DataBase
from tkinter import messagebox


class Abmc:
    def __init__(self):
        self.db = DataBase()
        self.utilidades = Utils()

    def alta(self, id, nombre: str, tipo: str, nivel, ruta: str, descripcion: str, tree, boton_alta):
        errores: str = ''
        errores += self.utilidades.valid_string('Nombre de la Aplicación', nombre)
        errores += self.utilidades.valid_int('Nivel de Riesgo', str(nivel))
        if errores == '':
            #Hacer el Alta o la Modificación
            if boton_alta['text'] == "Actualizar":
                cursor = self.db.connection.cursor()
                data = ( nombre, tipo, nivel, ruta, descripcion, id)
                sql = "UPDATE aplicaciones SET nombre = ?, tipo = ? , nivel = ?, ruta = ?, descripcion = ? WHERE id = ?"
                cursor.execute(sql, data)
                self.db.connection.commit()
                messagebox.showinfo("Modificación", "Se actualizó exitosamente")
                self.actualizar_treeview(tree)
            else:
                cursor = self.db.connection.cursor()
                data = (nombre, tipo, nivel, ruta, descripcion)
                sql = "INSERT INTO aplicaciones (nombre, tipo, nivel, ruta, descripcion) VALUES(?, ?, ?, ?, ?)"
                cursor.execute(sql, data)
                self.db.connection.commit()
                messagebox.showinfo("Alta", "Se guardó exitosamente")
                self.actualizar_treeview(tree)
        else:
            messagebox.showinfo("Alta", errores)

    def consultar(self, tree):
        self.actualizar_treeview(tree)

    def limpiar(self, tree, boton_alta, id_val, nombre_val, tipo_val, nivel_val, ruta_val, descripcion_val):
        id_val.set(0)
        nombre_val.set('')
        tipo_val.set('')
        nivel_val.set('')
        ruta_val.set('')
        descripcion_val.set('')
        boton_alta['text'] = "Agregar"

    def modificar(self, tree, boton_alta, id_val, nombre_val, tipo_val, nivel_val, ruta_val, descripcion_val):
        valor = tree.selection()
        item = tree.item(valor)
        my_id = item['text']
        app_sel = self.buscar_una_app(my_id)
        id_val.set(my_id)
        nombre_val.set(app_sel[1])
        tipo_val.set(app_sel[2])
        nivel_val.set(app_sel[3])
        ruta_val.set(app_sel[4])
        descripcion_val.set(app_sel[5])
        boton_alta['text'] = "Actualizar"

    def borrar(self, tree):
        valor = tree.selection()
        item = tree.item(valor)
        mi_id = item['text']
        if messagebox.askokcancel("Atencion", f"Está seguro que desea eliminar la Aplicacion con ID: {mi_id}"):
            cursor = self.db.connection.cursor()
            # mi_id = int(mi_id)
            data = (mi_id,)
            sql = "DELETE FROM aplicaciones WHERE id = ?;"
            cursor.execute(sql, data)
            self.db.connection.commit()
            tree.delete(valor)
            messagebox.showinfo("Atención", f"La aplicación {mi_id} se eliminó correctamente")


    def actualizar_treeview(self, mitreview):
        records = mitreview.get_children()
        for element in records:
            mitreview.delete(element)
        sql = "SELECT * FROM aplicaciones ORDER BY id ASC"
        cursor = self.db.connection.cursor()
        datos = cursor.execute(sql)

        resultado = datos.fetchall()
        for fila in resultado:
            mitreview.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[5]))

    def buscar_una_app( self, id ):
        sql = f"SELECT * FROM aplicaciones WHERE id = {id}"
        cursor = self.db.connection.cursor()
        datos = cursor.execute(sql)
        resultado = datos.fetchone()
        return resultado
