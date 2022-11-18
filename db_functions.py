from tkinter import messagebox
import sqlite3


class DataBase:
    def __init__(self):
        self.connection = None

        try:
            self.connect()
            self.make_table()
            messagebox.showinfo("CONEXION", "Base de Datos Creada exitosamente")
        except:
            print("Error al crear la base de datos")

    def connect(self):
        self.connection = sqlite3.connect("mibase.db")

    def make_table(self):
        self.connect()
        cursor = self.connection.cursor()
        sql = """CREATE TABLE aplicaciones
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 nombre varchar(100) NOT NULL,
                 tipo varchar(20) NOT NULL,
                 nivel int NOT NULL, 
                 ruta varchar(200) NOT NULL,
                 descripcion varchar(500) NOT NULL)
        """
        cursor.execute(sql)
        self.connection.commit()
