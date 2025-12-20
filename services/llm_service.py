def llmGenerarPseudocodigo(self, descripcion):
    codigo = self.llmService.generarPseudocodigo(descripcion)
    self.ultimoCodigo = codigo
    self.ultimoAST = None
    self.vista.mostrarCodigo(codigo)
