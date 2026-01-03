# model/complexity/complexity_result.py

class ComplexityResult:
    def __init__(self, O, Omega, Theta, detalles=""):
        self.O = O
        self.Omega = Omega
        self.Theta = Theta
        self.detalles = detalles

    def __repr__(self):
        return f"O({self.O}), Ω({self.Omega}), Θ({self.Theta})"
