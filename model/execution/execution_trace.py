# model/execution/execution_trace.py

class ExecutionTrace:
    """
    Representa un paso de ejecución.
    """

    def __init__(self, linea: int, accion: str, snapshot):
        self.linea = linea
        self.accion = accion
        self.snapshot = snapshot

    def __repr__(self):
        return f"Trace(linea={self.linea}, accion='{self.accion}')"
