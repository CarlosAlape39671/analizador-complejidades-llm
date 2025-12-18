# model/lexer/token.py

from model.lexer.token_type import TokenType


class Token:
    """
    Representa un token generado por el analizador léxico.
    Un token encapsula un tipo, un lexema y su posición en el código fuente.
    """

    def __init__(self, token_type: TokenType, lexema: str, linea: int, columna: int):
        self.type = token_type
        self.lexema = lexema
        self.linea = linea
        self.columna = columna

    def __str__(self) -> str:
        return f"Token({self.type.name}, '{self.lexema}', línea={self.linea}, columna={self.columna})"

    def __repr__(self) -> str:
        return self.__str__()
