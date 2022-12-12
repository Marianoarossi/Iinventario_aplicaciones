from vista import VistaInventario
from tkinter import Tk


class Controller:
    def __init__(self, root):
        self.root_controller = root
        self.vista_inventario = VistaInventario(self.root_controller)


if __name__=='__main__':
    root = Tk()
    Controller(root)
    root.mainloop()
