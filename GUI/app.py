from GUI.ventana import MainWindow
from GUI.botones import ButtonManager

class App:
    def __init__(self):
        self.window = MainWindow()
        self.botones = ButtonManager(self.window)

    @property
    def root(self):
        return self.window.root

    def run(self):
        self.window.root.mainloop()