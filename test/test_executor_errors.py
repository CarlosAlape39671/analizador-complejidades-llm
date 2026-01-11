import pytest

from concurrent.futures import Executor
from email.parser import Parser
from model.lexer.lexer import Lexer


def test_error_variable_no_definida():
    codigo = "x := y + 1"

    lexer = Lexer()
    parser = Parser()
    executor = Executor()

    ast = parser.parse(lexer.tokenizar(codigo))

    with pytest.raises(RuntimeError) as err:
        executor.ejecutar(ast)

    assert "Variable 'y' no definida" in str(err.value)

def test_error_division_por_cero():
    codigo = "x := 5 / 0"

    lexer = Lexer()
    parser = Parser()
    executor = Executor()

    ast = parser.parse(lexer.tokenizar(codigo))

    with pytest.raises(RuntimeError) as err:
        executor.ejecutar(ast)

    assert "división por cero" in str(err.value).lower()

def test_error_en_paso_a_paso():
    codigo = """x := 1
y := z + 1"""

    lexer = Lexer()
    parser = Parser()
    executor = Executor()

    ast = parser.parse(lexer.tokenizar(codigo))

    trazas = executor.ejecutarPasoAPaso(ast)

    with pytest.raises(RuntimeError):
        while True:
            executor.siguientePaso()

def test_error_linea_correcta():
    codigo = """x := 1
y := z"""

    lexer = Lexer()
    parser = Parser()
    executor = Executor()

    ast = parser.parse(lexer.tokenizar(codigo))

    try:
        executor.ejecutar(ast)
    except RuntimeError as e:
        assert "línea 2" in str(e)


