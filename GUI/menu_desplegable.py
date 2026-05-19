import tkinter as tk

MODOS_RLC = {
    "Subamortiguado": (10, 0.1, 100e-6),
    "Criticamente amortiguado": (200, 0.1, 10e-6),
    "Sobreamortiguado": (1000, 0.1, 10e-6),
}

class Menu:
    def __init__(self, parent, text, width, row, command=None):
        self.text = text
        self.command = command
        self.default_bg = "#200a8c"
        self.hover_bg = "#1e78c7"

        self.label = tk.Label(
            parent,
            text=self.text,
            bg=self.default_bg,
            fg="white",
            padx=width,
            pady=8,
            cursor="hand2",
            width=width
        )
        self.label.grid(row=row, column=0, sticky="ew")

        # Hover
        self.label.bind("<Enter>", lambda e: self.label.config(bg=self.hover_bg))
        self.label.bind("<Leave>", lambda e: self.label.config(bg=self.default_bg))

        # Click
        if self.command:
            self.label.bind("<Button-1>", lambda e: self.command(self.text))

class Menu_desplegable:
    def __init__(self, root, entry_r, entry_l, entry_c):
        self.root = root
        self.entry_r = entry_r
        self.entry_l = entry_l
        self.entry_c = entry_c

        self.width = 20
        self.visible = False
        self.brbg = "#2936ab"

        self._setup_ui()

    def _setup_ui(self):

        self.barra = tk.Frame(self.root, bg=self.brbg, width=260)
        self.barra.grid(
            row=0,
            column=1,
            rowspan=10,
            sticky="nsew"
        )

        self.btn_menu = tk.Label(
            self.barra,
            text="Modo de respuesta",
            bg=self.brbg,
            fg="white",
            relief="raised",
            padx=10,
            pady=5,
            cursor="hand2"
        )
        self.btn_menu.grid(row=0, column=0, sticky="ew")
        self.btn_menu.bind("<Button-1>", self.toggle_menu)

        self.menu_frame = tk.Frame(
            self.barra,
            bg=self.brbg,
            bd=1,
            relief="solid"
        )

        self._create_menu_items()

    def _create_menu_items(self):
        opciones = [
            "Subamortiguado",
            "Criticamente amortiguado",
            "Sobreamortiguado"
        ]

        for i, opcion in enumerate(opciones):
            Menu(
                self.menu_frame,
                opcion,
                self.width,
                row=i,
                command=self.accion_menu
            )

    def accion_menu(self, nombre_opcion):
        if nombre_opcion in MODOS_RLC:
            R, L, C = MODOS_RLC[nombre_opcion]

            self.entry_r.delete(0, tk.END)
            self.entry_r.insert(0, str(R))

            self.entry_l.delete(0, tk.END)
            self.entry_l.insert(0, str(L))

            self.entry_c.delete(0, tk.END)
            self.entry_c.insert(0, str(C))

        self.toggle_menu(None)

    def toggle_menu(self, event):
        if self.visible:
            self.menu_frame.grid_forget()
        else:
            self.menu_frame.grid(row=1, column=0, sticky="w")
        self.visible = not self.visible
