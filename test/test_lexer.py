from model.lexer.lexer import Lexer


def test_lexer_sin_errores():
    codigo = "x := 10 + 5"

    lexer = Lexer()
    lexer.tokenizar(codigo)

    assert lexer.obtenerErrores() == []
