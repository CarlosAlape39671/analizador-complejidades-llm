import unittest
from model.lexer.lexer import Lexer

class TestLexerErrors(unittest.TestCase):

    def test_simbolo_no_reconocido(self):
        codigo = "x := 5 @"

        lexer = Lexer()
        tokens = lexer.tokenizar(codigo)
        errores = lexer.obtenerErrores()

        self.assertEqual(len(errores), 1)

        error = errores[0]
        self.assertEqual(error.linea, 1)
        self.assertEqual(error.fragmento, "@")
        self.assertIn("Símbolo no reconocido", error.mensaje)

    def test_varios_errores_lexicos(self):
        codigo = "x := 5 @ #"

        lexer = Lexer()
        lexer.tokenizar(codigo)
        errores = lexer.obtenerErrores()

        self.assertEqual(len(errores), 2)
