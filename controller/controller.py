from model.execution.executor import Executor
from model.parser.parser import Parser
from model.lexer.lexer import Lexer
from model.complexity.complexity_analyzer import ComplexityAnalyzer
from services.file_manager import FileManager
from services.llm_service import LLMService


class Controller:

    def __init__(self, vista):
        self.vista = vista
        self.lexer = Lexer()
        self.parser = Parser()
        self.executor = Executor()
        self.analyzer = ComplexityAnalyzer()
        self.fileManager = FileManager()
        self.llmService = LLMService()

        self.ultimoCodigo = ""
        self.ultimoAST = None
        self.erroresParseo = []

    def parsear(self, codigo):
        tokens = self.lexer.tokenizar(codigo)

        if self.lexer.obtenerErrores():
            self.erroresParseo = self.lexer.obtenerErrores()
            self.vista.mostrarError()
            return None

        ast = self.parser.parse(tokens)

        if ast is None:
            self.erroresParseo = self.parser.obtenerErrores()
            self.vista.mostrarError()
            return None

        self.ultimoAST = ast
        return ast

    def ejecutar(self):
        if not self.ultimoAST:
            ast = self.parsear(self.ultimoCodigo)
            if not ast:
                return

        self.executor.reiniciarEjecucion()
        ambiente = self.executor.ejecutar(self.ultimoAST)
        self.vista.mostrarAmbientes(ambiente)

    def ejecutarPasoAPaso(self):
        if not self.ultimoAST:
            ast = self.parsear(self.ultimoCodigo)
            if not ast:
                return

        trazas = self.executor.ejecutarPasoAPaso(self.ultimoAST)
        self.vista.mostrarTrazas(trazas)

        if trazas:
            self.vista.resaltarTraza(0)
            self.vista.resaltarLinea(trazas[0].linea)
            self.vista.mostrarAmbientes(trazas[0].snapshot)

    def siguientePaso(self):
        traza = self.executor.siguientePaso()
        if traza:
            self.vista.resaltarLinea(traza.linea)
            self.vista.mostrarAmbientes(traza.snapshot)
            self.vista.resaltarTraza(self.executor.indiceActual - 1)

    def pasoAnterior(self):
        traza = self.executor.pasoAnterior()
        if traza:
            self.vista.resaltarLinea(traza.linea)
            self.vista.mostrarAmbientes(traza.snapshot)
            self.vista.resaltarTraza(self.executor.indiceActual)

    def reiniciarPasoAPaso(self):
        self.executor.reiniciarPasoAPaso()
        self.vista.limpiarResaltadoLinea()
        self.vista.mostrarAmbientes(None)

    def reiniciarEjecucion(self):
        self.executor.reiniciarEjecucion()
        self.ultimoAST = None
        self.vista.mostrarAmbientes(None)

    def mostrarDetalleError(self):
        for err in self.erroresParseo:
            mensaje = (
                        f"Error en línea {err.linea}\n\n"
                        f"{err.mensaje}\n"
                        f"Fragmento: '{err.fragmento}'"
                    )
            self.vista.mostrarError(mensaje)
            self.vista.resaltarLinea(err.linea)
            self.vista.resaltarFragmento(err.linea, err.fragmento)


    def procesarTexto(self, codigo):
        self.ultimoCodigo = codigo
        self.ultimoAST = None
    
    def procesarArchivo(self, ruta):
        codigo = self.fileManager.leerArchivo(ruta)
        self.ultimoCodigo = codigo
        self.ultimoAST = None
        self.vista.mostrarCodigo(codigo)
