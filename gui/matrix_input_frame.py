# gui/matrix_input_frame.py
import tkinter as tk
from tkinter import ttk, messagebox

class MatrixInputFrame(ttk.Frame):
    # Adicionar style_prefix ao construtor
    def __init__(self, master, title="Matriz", max_dim=10, style_prefix=""):
        super().__init__(master, padding="0 0 0 0") # Padding removido, controlado externamente
        self.master = master
        self.title_text_base = title
        self.max_dim = max_dim
        self.entries = []
        self._is_enabled = True # Para checagem externa

        # Usar o estilo 'Title.TLabel' definido em app_window.py
        self.title_label = ttk.Label(self, text=self.title_text_base, style='Title.TLabel')
        self.title_label.grid(row=0, column=0, columnspan=4, pady=(0, 10), sticky="w")

        # Frame para os controles de dimensão
        dim_frame = ttk.Frame(self)
        dim_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(0,10))

        ttk.Label(dim_frame, text="Linhas:").pack(side=tk.LEFT, padx=(0,5))
        self.rows_var = tk.IntVar(value=2)
        self.rows_spinbox = ttk.Spinbox(dim_frame, from_=1, to=self.max_dim, textvariable=self.rows_var, width=4, command=self.create_matrix_entries_from_spinbox)
        self.rows_spinbox.pack(side=tk.LEFT, padx=(0,15))

        ttk.Label(dim_frame, text="Colunas:").pack(side=tk.LEFT, padx=(0,5))
        self.cols_var = tk.IntVar(value=2)
        self.cols_spinbox = ttk.Spinbox(dim_frame, from_=1, to=self.max_dim, textvariable=self.cols_var, width=4, command=self.create_matrix_entries_from_spinbox)
        self.cols_spinbox.pack(side=tk.LEFT)

        self.entries_frame = ttk.Frame(self, padding=(0, 0, 0, 0)) # Sem padding aqui
        self.entries_frame.grid(row=2, column=0, columnspan=4, sticky="nsew")
        
        # Estilo para as entries dentro desta frame (se precisar de algo específico)
        # s_entry = ttk.Style()
        # s_entry.configure(f"{style_prefix}.TEntry", padding=(5,6), relief='flat', borderwidth=1)

        self.create_matrix_entries()

    def update_title_text(self, new_title_suffix=""):
        self.title_label.config(text=new_title_suffix)

    def create_matrix_entries_from_spinbox(self):
        # ... (mesma lógica)
        try:
            r = int(self.rows_var.get())
            c = int(self.cols_var.get())
            if r < 1: self.rows_var.set(1)
            if c < 1: self.cols_var.set(1)
            if r > self.max_dim: self.rows_var.set(self.max_dim)
            if c > self.max_dim: self.cols_var.set(self.max_dim)
        except tk.TclError:
            self.rows_var.set(2)
            self.cols_var.set(2)
        self.create_matrix_entries()

    def create_matrix_entries(self):
        for widget in self.entries_frame.winfo_children():
            widget.destroy()
        self.entries = []

        rows = self.rows_var.get()
        cols = self.cols_var.get()

        for i in range(rows):
            row_entries = []
            for j in range(cols):
                entry_var = tk.StringVar(value="0")
                # Aplicar estilo específico se necessário, ou o global 'TEntry' será usado
                entry = ttk.Entry(self.entries_frame, width=5, justify='center', textvariable=entry_var)
                entry.grid(row=i, column=j, padx=1, pady=1, ipady=3, ipadx=3) # Padding menor entre entries
                row_entries.append(entry_var)
            self.entries.append(row_entries)
        self.set_enabled(self._is_enabled) # Reaplicar estado de habilitação

    def get_matrix(self):
        # ... (mesma lógica)
        try:
            rows = self.rows_var.get()
            cols = self.cols_var.get()
            matrix = []
            for i in range(rows):
                row_data = []
                for j in range(cols):
                    val_str = self.entries[i][j].get()
                    if not val_str.strip():
                        val = 0.0
                        self.entries[i][j].set("0")
                    else:
                        try: val = int(val_str)
                        except ValueError: val = float(val_str)
                    row_data.append(val)
                matrix.append(row_data)
            return matrix
        except ValueError:
            messagebox.showerror("Erro de Entrada", f"Valor inválido na {self.title_text_base}. Insira apenas números.")
            return None
        except IndexError:
            messagebox.showerror("Erro Interno", "Erro ao ler a matriz. Tente recriar as entradas.")
            return None

    def set_matrix(self, matrix_data):
        # ... (mesma lógica)
        if not matrix_data or not isinstance(matrix_data, list) or not all(isinstance(row, list) for row in matrix_data):
            self.rows_var.set(1); self.cols_var.set(1)
            self.create_matrix_entries(); return

        rows = len(matrix_data); cols = len(matrix_data[0]) if rows > 0 else 0
        if rows == 0 or cols == 0:
            self.rows_var.set(1); self.cols_var.set(1)
            self.create_matrix_entries(); return

        self.rows_var.set(min(rows, self.max_dim)); self.cols_var.set(min(cols, self.max_dim))
        self.create_matrix_entries()
        actual_rows = self.rows_var.get(); actual_cols = self.cols_var.get()
        for i in range(actual_rows):
            for j in range(actual_cols):
                val = matrix_data[i][j]
                val_str = str(int(val)) if isinstance(val, float) and val.is_integer() else str(val)
                self.entries[i][j].set(val_str)

    def clear_entries(self):
        for i in range(len(self.entries)):
            for j in range(len(self.entries[i])):
                self.entries[i][j].set("0")

    def set_enabled(self, enabled=True):
        self._is_enabled = enabled # Armazena o estado
        state = tk.NORMAL if enabled else tk.DISABLED
        self.rows_spinbox.config(state=state)
        self.cols_spinbox.config(state=state)
        
        for child_widget in self.entries_frame.winfo_children():
            if isinstance(child_widget, ttk.Entry):
                child_widget.config(state=state)
    
    def is_enabled(self): # Método para checar externamente
        return self._is_enabled