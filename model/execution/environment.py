# model/execution/environment.py

class Environment:
    """
    Representa un ambiente de ejecución (scope).
    Permite variables locales y encadenamiento con ambientes padre.
    """

    def __init__(self, parent=None):
        self.tabla = {}
        self.parent = parent

    def crearHijo(self):
        """
        Crea un nuevo ambiente hijo.
        """
        return Environment(parent=self)

    def definir(self, nombre, valor):
        """
        Define o actualiza una variable en el ambiente actual.
        """
        self.tabla[nombre] = valor

    def obtener(self, nombre):
        """
        Obtiene el valor de una variable, buscando recursivamente.
        """
        if nombre in self.tabla:
            return self.tabla[nombre]

        if self.parent:
            return self.parent.obtener(nombre)

        raise RuntimeError(f"Variable '{nombre}' no definida")

    def __repr__(self):
        return f"Environment({self.tabla}, parent={self.parent is not None})"
