import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk


class GUIView:

    def __init__(self, controller):
        self.controller = controller

        self.root = tk.Tk()
        self.root.title("Analizador de Complejidades")

        self._crear_componentes()
        self.varNodes = {}

        self.lineaActual = None

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

        # Configuración de tags para resaltar líneas
        self.editor.tag_configure(
            "linea_actual",
            background="#ffeaa7"   # amarillo suave
        )

        # Panel de trazas
        self.panelTrazas = tk.Listbox(
            self.frameDerecho,
            height=15
        )

        self.panelTrazas.pack(
            fill=tk.BOTH,
            expand=True,
            padx=5,
            pady=5
        )

        self.panelTrazas.bind("<<ListboxSelect>>", self._onTrazaSeleccionada)

        # Panel de ambientes (árbol)
        self.panelAmbientes = ttk.Treeview(
            self.frameInferior,
            columns=("valor",),
            show="tree headings"
        )

        self.panelAmbientes.heading("#0", text="Variable")
        self.panelAmbientes.heading("valor", text="Valor")

        self.panelAmbientes.pack(
            fill=tk.BOTH,
            expand=True,
            padx=5,
            pady=5
        )

        # Configuración de tags para cambios en variables: definir colores
        self.panelAmbientes.tag_configure(
            "cambio",
            background="#fff3cd"   # amarillo suave
        )

        self.panelAmbientes.tag_configure(
            "nuevo",
            background="#d4edda"   # verde suave
        )

        # Configuración de tag para resaltar fragmentos con error
        self.editor.tag_configure(
            "error_fragmento",
            background="#fab1a0"
        )


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

    def _onTrazaSeleccionada(self, event):
        seleccion = self.panelTrazas.curselection()
        if not seleccion:
            return

        index = seleccion[0]
        traza = self.trazas[index]

        self.resaltarLinea(traza.linea)
        self.mostrarAmbientes(traza.snapshot)
    
    def resaltarTraza(self, index):
        self.panelTrazas.selection_clear(0, tk.END)
        self.panelTrazas.selection_set(index)
        self.panelTrazas.see(index)

    def _limpiarAmbientes(self):
        for item in self.panelAmbientes.get_children():
            self.panelAmbientes.delete(item)
    
    def limpiarResaltadoLinea(self):
        self.editor.tag_remove("linea_actual", "1.0", tk.END)
        self.lineaActual = None

    def resaltarFragmento(self, linea, fragmento):
        if not fragmento:
            return

        texto_linea = self.editor.get(f"{linea}.0", f"{linea}.end")
        idx = texto_linea.find(fragmento)

        if idx == -1:
            return

        inicio = f"{linea}.{idx}"
        fin = f"{linea}.{idx + len(fragmento)}"

        self.editor.tag_add("error_fragmento", inicio, fin)


    # ======================
    # Métodos usados por Controller
    # ======================

    def obtenerCodigo(self):
        return self.editor.get("1.0", tk.END)

    def mostrarError(self, mensaje):
        messagebox.showerror("Error", mensaje)

        import re
        match = re.search(r"línea (\d+)", mensaje)
        if match:
            linea = int(match.group(1))
            self.resaltarLinea(linea)


    def mostrarAmbientes(self, env):
        self._limpiarAmbientes()

        if env is None:
            return

        self._mostrarAmbienteRec(env, "Scope actual")
        self.ultimoEnv = env

        # if self.ultimoEnv and nombre in self.ultimoEnv.tabla:
        #     if self.ultimoEnv.tabla[nombre] != valor:
        #         # colorear


    def _mostrarAmbienteRec(self, env, titulo):
        nodo_scope = self.panelAmbientes.insert(
            "",
            "end",
            text=titulo,
            open=True
        )

        for nombre, valor in sorted(env.tabla.items()):
            item_id = self.panelAmbientes.insert(
                nodo_scope,
                "end",
                text=nombre,
                values=(valor,)
            )

            # Guardar referencia
            self.varNodes[(env, nombre)] = item_id

            # ¿Cambió el valor?
            if self.ultimoEnv:
                try:
                    valor_anterior = self._buscarValorAnterior(
                        self.ultimoEnv, nombre
                    )
                    if valor_anterior != valor:
                        self.panelAmbientes.item(
                            item_id,
                            tags=("cambio",)
                        )
                except:
                    # Variable nueva
                    self.panelAmbientes.item(
                        item_id,
                        tags=("nuevo",)
                    )

        if env.parent:
            self._mostrarAmbienteRec(env.parent, "Scope padre")

    def mostrarTrazas(self, trazas):
        print(trazas)

    def _buscarValorAnterior(self, env, nombre):
        if nombre in env.tabla:
            return env.tabla[nombre]
        if env.parent:
            return self._buscarValorAnterior(env.parent, nombre)
        raise KeyError()


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

    def resaltarLinea(self, linea):
        if linea < 1:
            return

        # Quitar resaltado anterior
        if self.lineaActual:
            self.editor.tag_remove(
                "linea_actual",
                f"{self.lineaActual}.0",
                f"{self.lineaActual}.end"
            )

        inicio = f"{linea}.0"
        fin = f"{linea}.end"

        self.editor.tag_add("linea_actual", inicio, fin)
        self.editor.see(inicio)

        self.lineaActual = linea


    def mostrarTrazas(self, trazas):
        self.panelTrazas.delete(0, tk.END)
        self.trazas = trazas  # guardamos referencia

        for i, traza in enumerate(trazas):
            texto = f"{i+1}. {traza.accion} (línea {traza.linea})"
            self.panelTrazas.insert(tk.END, texto)

