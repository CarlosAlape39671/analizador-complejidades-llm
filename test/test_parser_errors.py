import unittest
from model.lexer.lexer import Lexer
from model.parser.parser import Parser

class TestParserErrors(unittest.TestCase):

    def test_asignacion_incompleta(self):
        codigo = "x :="

        lexer = Lexer()
        tokens = lexer.tokenizar(codigo)

        parser = Parser()
        ast = parser.parse(tokens)
        errores = parser.obtenerErrores()

        self.assertIsNone(ast)
        self.assertEqual(len(errores), 1)

        error = errores[0]
        self.assertEqual(error.linea, 1)
        self.assertIn("Expresión", error.mensaje)

    def test_if_sin_end(self):
        codigo = """
        if x > 0 then
            y := 3
        """

        lexer = Lexer()
        tokens = lexer.tokenizar(codigo)

        parser = Parser()
        ast = parser.parse(tokens)
        errores = parser.obtenerErrores()

        self.assertIsNone(ast)
        self.assertGreater(len(errores), 0)

    def test_while_sin_begin(self):
        codigo = "while x > 0 y := 1 end"

        lexer = Lexer()
        tokens = lexer.tokenizar(codigo)

        parser = Parser()
        ast = parser.parse(tokens)
        errores = parser.obtenerErrores()

        self.assertIsNone(ast)
        self.assertGreater(len(errores), 0)

    def test_error_linea_correcta(self):
        codigo = """
        x := 5
        if x > then
            y := 3
        end
        """

        lexer = Lexer()
        tokens = lexer.tokenizar(codigo)

        parser = Parser()
        parser.parse(tokens)
        errores = parser.obtenerErrores()

        self.assertEqual(errores[0].linea, 3)
