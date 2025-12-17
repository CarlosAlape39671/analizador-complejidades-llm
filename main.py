from controller.controller import Controller
from view.gui_view import GUIView

def main():
    vista = GUIView()
    controller = Controller(vista)
    vista.set_controller(controller)
    vista.iniciar()

if __name__ == "__main__":
    main()
