import tkinter as tk

class No_molestar:
    def __init__(self, root):
        self.root = root
        self.root.state('zoomed')
        # Variable de control para evitar el bucle infinito
        self.saliendo_de_fullscreen = False
        

        self.root.bind("<Configure>", self.detectar_maximizado)
        self.root.bind("<Escape>", self.salir_fullscreen)

    def detectar_maximizado(self, event):
        # Solo activamos fullscreen si no estamos en proceso de salida
        if self.root.state() == 'zoomed' and not self.saliendo_de_fullscreen:
            self.root.attributes("-fullscreen", True)
            self.root.attributes("-alpha",1)
        # Resetear la bandera cuando la ventana vuelve a estar estable
        if self.root.state() == 'normal':
            self.saliendo_de_fullscreen = False
            self.root.attributes("-alpha",0.9)
        #print(self.root.state())        # Devuelve 'normal', 'zoomed', etc.
        #print(self.root.attributes("-alpha")) # Devuelve el nivel de transparencia actual.

    def salir_fullscreen(self, event=None):
        # 1. Activamos la bandera para que <Configure> no nos regrese a fullscreen
        self.saliendo_de_fullscreen = True
        
        # 2. Quitamos el modo fullscreen
        self.root.attributes("-fullscreen", False)
        
        # 3. Forzamos el estado a 'normal' para que no se quede en 'zoomed'
        self.root.state('normal')

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pantalla Completa")
    root.geometry("800x600")
        
    app = No_molestar(root)
    
    root.mainloop()