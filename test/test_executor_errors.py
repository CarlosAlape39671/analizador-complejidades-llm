import pytest
from model.lexer.lexer import Lexer
from model.parser.parser import Parser
from model.execution.executor import Executor



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

    with pytest.raises(ZeroDivisionError):
        executor.ejecutar(ast)

def test_error_en_paso_a_paso():
    codigo = """x := 1
y := z + 1"""

    lexer = Lexer()
    parser = Parser()
    executor = Executor()

    ast = parser.parse(lexer.tokenizar(codigo))

    with pytest.raises(ZeroDivisionError):
        executor.ejecutar(ast)


# def test_error_linea_correcta():
#     codigo = """x := 1
# y := z"""

#     lexer = Lexer()
#     parser = Parser()
#     executor = Executor()

#     ast = parser.parse(lexer.tokenizar(codigo))

#     try:
#         executor.ejecutar(ast)
#     except RuntimeError as e:
#         assert "línea 2" in str(e)


