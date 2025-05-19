import customtkinter as ctk
from gui.app_window import AppWindow

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    # Cria uma instância da janela principal da aplicação.
    app = AppWindow()
    # Inicia o loop principal de eventos do Tkinter (e CustomTkinter).
    app.mainloop()