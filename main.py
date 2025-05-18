# calculadora_matrizes/main.py
import customtkinter as ctk
from gui.app_window import AppWindow

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Define o tema escuro globalmente
    ctk.set_default_color_theme("blue") # Ou "green", "dark-blue"

    app = AppWindow()
    app.mainloop()