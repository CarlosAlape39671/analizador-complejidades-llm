import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext


class GUIView:

    def __init__(self, controller):
        self.controller = controller

        self.root = tk.Tk()
        self.root.title("Analizador de Complejidades")

        self._crear_componentes()

    def _crear_componentes(self):
        # Área de código
        self.editor = scrolledtext.ScrolledText(self.root, width=80, height=20)
        self.editor.pack(padx=10, pady=10)

        # Botones
        frame_botones = tk.Frame(self.root)
        frame_botones.pack()

        tk.Button(frame_botones, text="Ejecutar",
                  command=self.ejecutar).pack(side=tk.LEFT, padx=5)

        tk.Button(frame_botones, text="Paso a paso",
                  command=self.ejecutarPasoAPaso).pack(side=tk.LEFT, padx=5)

        tk.Button(frame_botones, text="Siguiente",
                  command=self.siguientePaso).pack(side=tk.LEFT, padx=5)

        tk.Button(frame_botones, text="Anterior",
                  command=self.pasoAnterior).pack(side=tk.LEFT, padx=5)
        
        # Panel de ambientes
        frame_env = tk.Frame(self.root)
        frame_env.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        tk.Label(frame_env, text="Ambiente de ejecución").pack(anchor="w")

        self.env_text = scrolledtext.ScrolledText(
            frame_env, width=80, height=10, state=tk.DISABLED
        )
        self.env_text.pack(fill=tk.BOTH, expand=True)


    # ======================
    # Métodos usados por Controller
    # ======================

    def obtenerCodigo(self):
        return self.editor.get("1.0", tk.END)

    def mostrarError(self, msg):
        messagebox.showerror("Error", msg)

    def mostrarAmbientes(self, env):
        print(env)

    def mostrarTrazas(self, trazas):
        print(trazas)

    # ======================
    # Acciones de usuario
    # ======================

    def ejecutar(self):
        self.controller.ultimoCodigo = self.obtenerCodigo()
        self.controller.ejecutar()

    def ejecutarPasoAPaso(self):
        self.controller.ultimoCodigo = self.obtenerCodigo()
        self.controller.ejecutarPasoAPaso()

    def siguientePaso(self):
        self.controller.siguientePaso()

    def pasoAnterior(self):
        self.controller.pasoAnterior()

    def iniciar(self):
        self.root.mainloop()

    def mostrarAmbientes(self, env):
        self.env_text.config(state=tk.NORMAL)
        self.env_text.delete("1.0", tk.END)

        if env is None:
            self.env_text.insert(tk.END, "Sin ambiente de ejecución\n")
        else:
            self._mostrar_env_recursivo(env)

        self.env_text.config(state=tk.DISABLED)

    def _mostrar_env_recursivo(self, env, nivel=0):
        indent = "  " * nivel
        self.env_text.insert(
            tk.END,
            f"{indent}Ambiente nivel {nivel}:\n"
        )

        for var, val in env.tabla.items():
            self.env_text.insert(
                tk.END,
                f"{indent}  {var} = {val}\n"
            )

        if env.parent:
            self._mostrar_env_recursivo(env.parent, nivel + 1)
