# model/parser/parse_error.py

class ParseError:
    """
    Representa un error léxico o sintáctico detectado durante
    el análisis del pseudocódigo.
    """

    def __init__(self, linea: int, mensaje: str, fragmento: str = ""):
        self.linea = linea
        self.mensaje = mensaje
        self.fragmento = fragmento

    def __str__(self) -> str:
        if self.fragmento:
            return f"Línea {self.linea}: {self.mensaje} -> '{self.fragmento}'"
        return f"Línea {self.linea}: {self.mensaje}"

    def __repr__(self) -> str:
        return self.__str__()
