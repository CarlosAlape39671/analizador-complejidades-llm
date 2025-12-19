# model/lexer/token_type.py

from enum import Enum, auto


class TokenType(Enum):
    """
    Enumeración de los tipos de tokens reconocidos por el analizador léxico.
    Estos tokens representan las unidades léxicas básicas del seudocódigo.
    """

    # Palabras clave
    KEYWORD_IF = auto()
    KEYWORD_THEN = auto()
    KEYWORD_ELSE = auto()
    KEYWORD_FOR = auto()
    KEYWORD_TO = auto()
    KEYWORD_WHILE = auto()
    KEYWORD_REPEAT = auto()
    KEYWORD_UNTIL = auto()
    KEYWORD_BEGIN = auto()
    KEYWORD_END = auto()

    # Identificadores y literales
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()

    # Operadores de asignación y aritméticos
    ASSIGN = auto()        # :=
    PLUS = auto()          # +
    MINUS = auto()         # -
    MULT = auto()          # *
    DIV = auto()           # /
    MOD = auto()           # %

    # Operadores relacionales
    LT = auto()            # <
    GT = auto()            # >
    LE = auto()            # <=
    GE = auto()            # >=
    EQ = auto()            # ==
    NEQ = auto()           # !=

    # Símbolos
    LPAREN = auto()        # (
    RPAREN = auto()        # )
    COMMA = auto()         # ,

    # Comentarios
    COMMENT = auto()
