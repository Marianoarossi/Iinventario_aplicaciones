import re

class Utils:
    #Se agrega como metodo estatico ya que no será necesario crear un objeto, sino que usamos directamente el metodo.
    @staticmethod
    def valid_string(nombre_campo: str, cadena: str) -> str:
        patron_string = "^[A-Za-záéíóú]*$"
        if not re.match(patron_string, cadena):
            return f"El {nombre_campo} tiene caracteres inválidos. Solo se pueden ingresar letras de la a la z \n"
        else:
            return ''

    @staticmethod
    def valid_int(nombre_campo: str, cadena: str) -> str:
        patron_num = '^([0-9])*$'
        if not re.match(patron_num, cadena):
            return f"El {nombre_campo} tiene caracteres inválidos. Solo se pueden números \n"
        else:
            return ''

    @staticmethod
    def validate_entry(text, new_text):
        # Primero chequear que el contenido total no exceda los dos caracteres.
        if len(new_text) > 2:
            return False
        # Luego, si la validación anterior no falló, chequear que el texto solo contenga nros
        return text.isdecimal()

