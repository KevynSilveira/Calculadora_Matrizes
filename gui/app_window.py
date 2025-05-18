# calculadora_matrizes/gui/app_window.py
import customtkinter as ctk
from tkinter import messagebox
from .matrix_input_frame import MatrixInputFrame
from logic import (
    add_matrices, subtract_matrices, multiply_matrices, scalar_multiply,
    transpose_matrix, determinant, inverse_matrix, solve_linear_system_inverse
)

class AppWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de Matrizes Elegante")
        self.geometry("950x880") 
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # Linha principal do conteúdo

        self.main_content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content_frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)
        self.main_content_frame.grid_columnconfigure(0, weight=1) 
        self.main_content_frame.grid_columnconfigure(1, weight=1) # Permitir que ambas as colunas tenham peso igual inicialmente

        # --- Matriz A e Escalar (Coluna Esquerda) ---
        left_column_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        left_column_frame.grid(row=0, column=0, sticky="new", padx=(0, 10))
        left_column_frame.grid_columnconfigure(0, weight=1)

        self.matrix_a_frame = MatrixInputFrame(left_column_frame, title="Matriz A", max_dim=10)
        self.matrix_a_frame.grid(row=0, column=0, sticky="ew")
        self.matrix_a_frame.master_app = self 

        self.scalar_input_outer_frame = ctk.CTkFrame(left_column_frame, fg_color="transparent")
        # grid será chamado em on_operation_change
        
        self.scalar_input_frame = ctk.CTkFrame(self.scalar_input_outer_frame, fg_color="transparent")
        self.scalar_input_frame.pack() 
        ctk.CTkLabel(self.scalar_input_frame, text="Escalar:", font=("Segoe UI", 14)).pack(side=ctk.LEFT, padx=(0,8))
        self.scalar_var = ctk.StringVar(value="1")
        self.scalar_entry = ctk.CTkEntry(self.scalar_input_frame, textvariable=self.scalar_var, width=120, font=("Segoe UI", 13))
        self.scalar_entry.pack(side=ctk.LEFT)

        # --- Matriz B (Coluna Direita) ---
        self.right_column_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        # grid será chamado em on_operation_change

        self.matrix_b_frame = MatrixInputFrame(self.right_column_frame, title="Matriz B / Vetor B", max_dim=10)
        self.matrix_b_frame.pack(fill="x", expand=True, padx=0, pady=0) 
        
        # --- Operations ---
        operations_main_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        operations_main_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(25, 20))
        operations_main_frame.grid_columnconfigure(0, weight=1)

        self.operation_options = [
            "Adição (A + B)", "Subtração (A - B)", "Multiplicação (A * B)",
            "Multiplicação por Escalar (k * A)", "Transposição (A)",
            "Determinante (A)", "Inversa (A)", "Resolver Sistema (AX = B)"
        ]
        self.selected_operation_var = ctk.StringVar(value=self.operation_options[0])
        
        self.operation_combobox = ctk.CTkComboBox(
            operations_main_frame, values=self.operation_options, variable=self.selected_operation_var,
            font=("Segoe UI", 15), dropdown_font=("Segoe UI", 14), command=self.on_operation_change,
            height=38, border_width=1
        )
        self.operation_combobox.grid(row=0, column=0, sticky="ew", padx=70, ipady=4)

        self.calculate_button = ctk.CTkButton(
            operations_main_frame, text="Calcular", command=self.execute_selected_operation,
            font=("Segoe UI", 17, "bold"), height=50, width=280, corner_radius=8
        )
        self.calculate_button.grid(row=1, column=0, pady=(20, 25))

        # --- Result Section ---
        result_section_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        result_section_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(10,15))
        result_section_frame.grid_columnconfigure(0, weight=1)
        result_section_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(result_section_frame, text="Resultado:", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, sticky="w", pady=(0,8))
        self.result_textbox = ctk.CTkTextbox(
            result_section_frame, height=220, font=("Consolas", 15), wrap="none", activate_scrollbars=True, border_width=1
        )
        self.result_textbox.grid(row=1, column=0, sticky="nsew")
        self.result_textbox.configure(state=ctk.DISABLED)
        self.main_content_frame.grid_rowconfigure(2, weight=1) 

        # --- Status Bar ---
        status_bar_frame = ctk.CTkFrame(self, height=35, corner_radius=0, border_width=1, border_color=("gray60", "gray30"))
        status_bar_frame.grid(row=1, column=0, sticky="ew") 
        self.status_label = ctk.CTkLabel(status_bar_frame, text="Pronto.", anchor="w", font=("Segoe UI", 12))
        self.status_label.pack(side=ctk.LEFT, padx=15, pady=5)

        self.on_operation_change() 

    def on_dimension_change_matrix_a(self):
        selected_op_str = self.selected_operation_var.get()
        if "Resolver Sistema" in selected_op_str and self.right_column_frame.winfo_ismapped():
            rows_a_str = self.matrix_a_frame.rows_var_str.get()
            self.matrix_b_frame.rows_var_str.set(rows_a_str)
            self.matrix_b_frame.create_matrix_entries_from_dim_input() 
            self.matrix_b_frame.cols_entry.configure(state=ctk.DISABLED) 

    def on_operation_change(self, choice=None):
        selected_op_str = self.selected_operation_var.get()
        
        # Visibilidade do campo Escalar
        if "Multiplicação por Escalar" in selected_op_str:
            self.scalar_input_outer_frame.grid(row=1, column=0, pady=(15, 0), sticky="ew") 
            self.scalar_entry.configure(state=ctk.NORMAL)
        else:
            self.scalar_input_outer_frame.grid_remove() 
            self.scalar_entry.configure(state=ctk.DISABLED)

        # Gerenciamento da Matriz B e layout das colunas principais
        # Operações que NÃO usam Matriz B
        if " (A)" in selected_op_str or "Multiplicação por Escalar" in selected_op_str: # CONDIÇÃO ATUALIZADA AQUI
            self.right_column_frame.grid_remove() 
            self.matrix_b_frame.set_enabled(False)
            self.main_content_frame.grid_columnconfigure(1, weight=0) 
            self.main_content_frame.grid_columnconfigure(0, weight=1) 
        else: # Operações que usam Matriz B (Adição, Subtração, Multiplicação A*B, Resolver Sistema)
            self.right_column_frame.grid(row=0, column=1, sticky="new", padx=(10, 0)) 
            self.matrix_b_frame.set_enabled(True)
            self.main_content_frame.grid_columnconfigure(1, weight=1) 
            self.main_content_frame.grid_columnconfigure(0, weight=1)

            # Configurações específicas para as operações que usam B
            if "Resolver Sistema" in selected_op_str:
                self.matrix_a_frame.update_title_text("Matriz A (Coeficientes)")
                self.matrix_b_frame.update_title_text("Vetor B (Termos)")
                self.on_dimension_change_matrix_a() 
            else: # A+B, A-B, A*B
                self.matrix_a_frame.update_title_text("Matriz A")
                self.matrix_b_frame.update_title_text("Matriz B")
                self.matrix_b_frame.cols_entry.configure(state=ctk.NORMAL)
                self.matrix_b_frame.rows_entry.configure(state=ctk.NORMAL)

        self.status_label.configure(text=f"Operação: {selected_op_str}")

    def _get_scalar(self):
        try:
            s_str = self.scalar_var.get()
            if not s_str.strip(): self.scalar_var.set("1"); return 1.0 
            return float(s_str) if '.' in s_str or 'e' in s_str.lower() else int(s_str)
        except ValueError: self.show_error("Valor escalar inválido."); return None

    def format_matrix_for_display(self, matrix):
        if isinstance(matrix, (int, float)): return str(matrix)
        if not matrix or not matrix[0]: return "[ Matriz Vazia ]"
        
        col_widths = [0] * len(matrix[0])
        str_matrix = []
        for r_idx, row_val in enumerate(matrix):
            str_row = []
            for c_idx, val in enumerate(row_val):
                s_val = f"{val:.4g}".rstrip('0').rstrip('.') if isinstance(val, float) else str(val)
                if s_val == "-0": s_val = "0" 
                str_row.append(s_val)
                col_widths[c_idx] = max(col_widths[c_idx], len(s_val))
            str_matrix.append(str_row)

        display_str = ""
        for str_row_val in str_matrix:
            line = "  ["
            for c_idx, s_val in enumerate(str_row_val):
                line += f"{s_val:>{col_widths[c_idx]}}" 
                if c_idx < len(str_row_val) - 1: line += "  " 
            line += "]\n"
            display_str += line
        return display_str.strip()

    def display_result(self, result_data, operation_name=""):
        self.result_textbox.configure(state=ctk.NORMAL)
        self.result_textbox.delete("1.0", ctk.END)
        formatted_output = self.format_matrix_for_display(result_data)
        self.result_textbox.insert("1.0", formatted_output)
        self.result_textbox.configure(state=ctk.DISABLED)
        self.show_success(f"'{operation_name}' calculado.")

    def show_error(self, message):
        messagebox.showerror("Erro", message, parent=self)
        self.status_label.configure(text=f"Erro: {message}")

    def show_success(self, message="Operação concluída."):
        self.status_label.configure(text=message)

    def execute_selected_operation(self):
        selected_op_str = self.selected_operation_var.get()
        self.on_operation_change() 

        matrix_a = self.matrix_a_frame.get_matrix()
        if matrix_a is None: return

        result, op_func, needs_b, needs_scalar, is_solve = None, None, False, False, False
        
        op_map = {
            "Adição (A + B)": (add_matrices, True, False, False),
            "Subtração (A - B)": (subtract_matrices, True, False, False),
            "Multiplicação (A * B)": (multiply_matrices, True, False, False),
            "Multiplicação por Escalar (k * A)": (scalar_multiply, False, True, False),
            "Transposição (A)": (transpose_matrix, False, False, False),
            "Determinante (A)": (determinant, False, False, False),
            "Inversa (A)": (inverse_matrix, False, False, False),
            "Resolver Sistema (AX = B)": (solve_linear_system_inverse, True, False, True)
        }

        if selected_op_str in op_map:
            op_func, needs_b, needs_scalar, is_solve = op_map[selected_op_str]
        else: self.show_error("Operação não mapeada."); return

        try:
            args = [matrix_a]
            if needs_b: 
                if not self.right_column_frame.winfo_ismapped(): 
                    self.show_error(f"Matriz B é necessária para '{selected_op_str}' mas não está visível.")
                    return
                matrix_b = self.matrix_b_frame.get_matrix()
                if matrix_b is None: return
                args.append(matrix_b)
            
            if needs_scalar:
                if not self.scalar_input_outer_frame.winfo_ismapped():
                     self.show_error(f"Escalar é necessário para '{selected_op_str}' mas não está visível.")
                     return
                scalar_val = self._get_scalar()
                if scalar_val is None: return
                args.append(scalar_val)

            result = op_func(*args)
            self.display_result(result, selected_op_str)

        except ValueError as e: self.show_error(str(e))
        except Exception as e: self.show_error(f"Erro inesperado ({type(e).__name__}): {str(e)}")