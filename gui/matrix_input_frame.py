# calculadora_matrizes/gui/matrix_input_frame.py
import customtkinter as ctk
from tkinter import messagebox

class MatrixInputFrame(ctk.CTkFrame):
    def __init__(self, master, title="Matriz", max_dim=10):
        super().__init__(master, fg_color="transparent")
        self.title_text_default = title
        self.max_dim = max_dim
        self.entries_vars = []
        self.entry_widgets = []
        self._is_enabled = True

        self.title_label = ctk.CTkLabel(self, text=self.title_text_default, font=("Segoe UI", 18, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=4, pady=(0, 12), sticky="w") # Aumentado columnspan

        # --- Linhas ---
        dim_frame_rows = ctk.CTkFrame(self, fg_color="transparent")
        dim_frame_rows.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 10))

        ctk.CTkLabel(dim_frame_rows, text="Linhas:", font=("Segoe UI", 13)).pack(side=ctk.LEFT, padx=(0,6))
        self.rows_var_str = ctk.StringVar(value="2")
        
        btn_dim_width = 28
        btn_dim_height = 28
        
        ctk.CTkButton(dim_frame_rows, text="-", width=btn_dim_width, height=btn_dim_height, command=lambda: self._adjust_dim(self.rows_var_str, -1, is_rows=True)).pack(side=ctk.LEFT)
        self.rows_entry = ctk.CTkEntry(dim_frame_rows, textvariable=self.rows_var_str, width=45, font=("Segoe UI", 13), justify="center")
        self.rows_entry.pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(dim_frame_rows, text="+", width=btn_dim_width, height=btn_dim_height, command=lambda: self._adjust_dim(self.rows_var_str, 1, is_rows=True)).pack(side=ctk.LEFT, padx=(0,15))
        
        self.rows_entry.bind("<Return>", self.create_matrix_entries_from_dim_input)
        self.rows_entry.bind("<FocusOut>", self.create_matrix_entries_from_dim_input)

        # --- Colunas ---
        dim_frame_cols = ctk.CTkFrame(self, fg_color="transparent")
        dim_frame_cols.grid(row=1, column=2, columnspan=2, sticky="w", pady=(0, 10), padx=(10,0))

        ctk.CTkLabel(dim_frame_cols, text="Colunas:", font=("Segoe UI", 13)).pack(side=ctk.LEFT, padx=(0,6))
        self.cols_var_str = ctk.StringVar(value="2")

        ctk.CTkButton(dim_frame_cols, text="-", width=btn_dim_width, height=btn_dim_height, command=lambda: self._adjust_dim(self.cols_var_str, -1, is_rows=False)).pack(side=ctk.LEFT)
        self.cols_entry = ctk.CTkEntry(dim_frame_cols, textvariable=self.cols_var_str, width=45, font=("Segoe UI", 13), justify="center")
        self.cols_entry.pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(dim_frame_cols, text="+", width=btn_dim_width, height=btn_dim_height, command=lambda: self._adjust_dim(self.cols_var_str, 1, is_rows=False)).pack(side=ctk.LEFT)

        self.cols_entry.bind("<Return>", self.create_matrix_entries_from_dim_input)
        self.cols_entry.bind("<FocusOut>", self.create_matrix_entries_from_dim_input)

        self.entries_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.entries_frame.grid(row=2, column=0, columnspan=4, sticky="nsew", pady=(10,0)) # pady superior
        
        self.create_matrix_entries()

    def _adjust_dim(self, var_str, delta, is_rows):
        try:
            current_val = int(var_str.get())
            new_val = current_val + delta
            if 1 <= new_val <= self.max_dim:
                var_str.set(str(new_val))
                self.create_matrix_entries_from_dim_input()
                # Se for ajuste de linhas da Matriz A, e a operação for Solve System, atualiza linhas de B
                if is_rows and self.master and hasattr(self.master, 'on_dimension_change_matrix_a'):
                     if self.title_label.cget("text").startswith("Matriz A"): # Identifica se é Matriz A
                        self.master.on_dimension_change_matrix_a()
            elif new_val < 1:
                var_str.set("1")
                self.create_matrix_entries_from_dim_input()
            elif new_val > self.max_dim:
                var_str.set(str(self.max_dim))
                self.create_matrix_entries_from_dim_input()

        except ValueError:
            var_str.set("2") # Reset para valor padrão
            self.create_matrix_entries_from_dim_input()


    def update_title_text(self, new_title_text=""):
        self.title_label.configure(text=new_title_text if new_title_text else self.title_text_default)

    def _get_validated_dim(self, var_str, default_val):
        try:
            val = int(var_str.get())
            if 1 <= val <= self.max_dim: return val
            elif val < 1: var_str.set("1"); return 1
            else: var_str.set(str(self.max_dim)); return self.max_dim
        except ValueError: var_str.set(str(default_val)); return default_val

    def create_matrix_entries_from_dim_input(self, event=None):
        self._get_validated_dim(self.rows_var_str, 2)
        self._get_validated_dim(self.cols_var_str, 2)
        self.create_matrix_entries()

    def create_matrix_entries(self):
        for widget in self.entries_frame.winfo_children(): widget.destroy()
        self.entries_vars, self.entry_widgets = [], []
        rows = self._get_validated_dim(self.rows_var_str, 2)
        cols = self._get_validated_dim(self.cols_var_str, 2)

        for i in range(rows):
            row_vars, row_widgets = [], []
            for j in range(cols):
                entry_var = ctk.StringVar(value="0")
                entry = ctk.CTkEntry(self.entries_frame, width=60, justify='center', textvariable=entry_var, font=("Consolas", 14))
                entry.grid(row=i, column=j, padx=4, pady=4, ipady=5)
                row_vars.append(entry_var); row_widgets.append(entry)
            self.entries_vars.append(row_vars); self.entry_widgets.append(row_widgets)
        self.set_enabled(self._is_enabled)

    def get_matrix(self):
        try:
            rows, cols = self._get_validated_dim(self.rows_var_str, 1), self._get_validated_dim(self.cols_var_str, 1)
            matrix = []
            for i in range(rows):
                row_data = []
                for j in range(cols):
                    val_str = self.entries_vars[i][j].get()
                    val = 0.0
                    if not val_str.strip(): self.entries_vars[i][j].set("0")
                    else:
                        try: val = int(val_str)
                        except ValueError: val = float(val_str)
                    row_data.append(val)
                matrix.append(row_data)
            return matrix
        except ValueError: messagebox.showerror("Erro de Entrada", f"Valor inválido em '{self.title_label.cget('text')}'.", parent=self); return None
        except IndexError: messagebox.showerror("Erro Interno", "Erro ao ler a matriz.", parent=self); return None

    def set_matrix(self, matrix_data):
        if not matrix_data or not isinstance(matrix_data, list) or not all(isinstance(row, list) for row in matrix_data) or (matrix_data and not matrix_data[0] and len(matrix_data)>0):
            self.rows_var_str.set("1"); self.cols_var_str.set("1")
            self.create_matrix_entries()
            if self.entries_vars and self.entries_vars[0]: self.entries_vars[0][0].set("0")
            return

        rows = len(matrix_data); cols = len(matrix_data[0]) if rows > 0 and matrix_data[0] else 0
        if rows == 0 or cols == 0:
            self.rows_var_str.set("1"); self.cols_var_str.set("1")
            self.create_matrix_entries()
            if self.entries_vars and self.entries_vars[0]: self.entries_vars[0][0].set("0")
            return
            
        self.rows_var_str.set(str(min(rows, self.max_dim)))
        self.cols_var_str.set(str(min(cols, self.max_dim)))
        self.create_matrix_entries() 
        actual_rows, actual_cols = self._get_validated_dim(self.rows_var_str, 1), self._get_validated_dim(self.cols_var_str, 1)

        for i in range(actual_rows):
            for j in range(actual_cols):
                if i < rows and j < cols: 
                    val = matrix_data[i][j]
                    val_str = str(int(val)) if isinstance(val, float) and val.is_integer() else f"{val:.4g}".rstrip('0').rstrip('.') if isinstance(val, float) else str(val)
                    self.entries_vars[i][j].set(val_str)
                else: self.entries_vars[i][j].set("0")

    def clear_entries(self):
        for row in self.entries_vars:
            for var in row: var.set("0")

    def set_enabled(self, enabled=True):
        self._is_enabled = enabled
        state = ctk.NORMAL if enabled else ctk.DISABLED
        
        # Botões de dimensão e entries de dimensão
        for child in self.winfo_children(): # Percorre os frames de dimensão
            if isinstance(child, ctk.CTkFrame):
                 for widget_in_dim_frame in child.winfo_children():
                    if isinstance(widget_in_dim_frame, (ctk.CTkButton, ctk.CTkEntry)):
                        widget_in_dim_frame.configure(state=state)
        
        # Entries da matriz
        for row_w in self.entry_widgets:
            for entry_widget in row_w: entry_widget.configure(state=state)
        
        # Caso especial: se desabilitado, a entrada de dimensão também deve ser desabilitada
        if not enabled:
            self.rows_entry.configure(state=ctk.DISABLED)
            self.cols_entry.configure(state=ctk.DISABLED)

    def is_enabled(self): return self._is_enabled