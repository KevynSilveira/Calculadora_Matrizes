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
        self.geometry("950x920") 
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) 

        self.main_content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content_frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)
        self.main_content_frame.grid_columnconfigure(0, weight=1) 
        self.main_content_frame.grid_columnconfigure(1, weight=1) 

        left_column_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        left_column_frame.grid(row=0, column=0, sticky="new", padx=(0, 10))
        left_column_frame.grid_columnconfigure(0, weight=1)

        self.matrix_a_frame = MatrixInputFrame(left_column_frame, title="Matriz A", max_dim=10)
        self.matrix_a_frame.grid(row=0, column=0, sticky="ew")
        self.matrix_a_frame.master_app = self 

        self.scalar_input_outer_frame = ctk.CTkFrame(left_column_frame, fg_color="transparent")
        
        self.scalar_input_frame = ctk.CTkFrame(self.scalar_input_outer_frame, fg_color="transparent")
        self.scalar_input_frame.pack() 
        ctk.CTkLabel(self.scalar_input_frame, text="Escalar:", font=("Segoe UI", 14)).pack(side=ctk.LEFT, padx=(0,8))
        self.scalar_var = ctk.StringVar(value="1")
        self.scalar_entry = ctk.CTkEntry(self.scalar_input_frame, textvariable=self.scalar_var, width=120, font=("Segoe UI", 13))
        self.scalar_entry.pack(side=ctk.LEFT)

        self.right_column_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")

        self.matrix_b_frame = MatrixInputFrame(self.right_column_frame, title="Matriz B / Vetor B", max_dim=10)
        self.matrix_b_frame.pack(fill="x", expand=True, padx=0, pady=0) 
        
        operations_main_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        operations_main_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(25, 15))
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

        # Frame para os botões Limpar e Calcular
        action_buttons_frame = ctk.CTkFrame(operations_main_frame, fg_color="transparent")
        action_buttons_frame.grid(row=1, column=0, pady=(20, 20))
        # Centraliza o action_buttons_frame no operations_main_frame
        # operations_main_frame já tem columnconfigure(0, weight=1), então o grid(row=1, column=0) no action_buttons_frame o centralizará

        self.clear_button = ctk.CTkButton( # BOTÃO LIMPAR VEM PRIMEIRO
            action_buttons_frame, text="Limpar Tudo", command=self.clear_all_fields,
            font=("Segoe UI", 17, "bold"), height=50, width=200, corner_radius=8,
            fg_color="gray50", hover_color="gray35" 
        )
        self.clear_button.pack(side=ctk.LEFT, padx=(0, 10)) # Empacota à esquerda, com padding à direita

        self.calculate_button = ctk.CTkButton( # BOTÃO CALCULAR VEM DEPOIS
            action_buttons_frame, text="Calcular", command=self.execute_selected_operation,
            font=("Segoe UI", 17, "bold"), height=50, width=200, corner_radius=8
        )
        self.calculate_button.pack(side=ctk.LEFT, padx=(10, 0)) # Empacota à esquerda, com padding à esquerda


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

        status_bar_frame = ctk.CTkFrame(self, height=35, corner_radius=0, border_width=1, border_color=("gray60", "gray30"))
        status_bar_frame.grid(row=1, column=0, sticky="ew") 
        self.status_label = ctk.CTkLabel(status_bar_frame, text="Pronto.", anchor="w", font=("Segoe UI", 12))
        self.status_label.pack(side=ctk.LEFT, padx=15, pady=5)

        self.on_operation_change() 

    def clear_all_fields(self):
        self.matrix_a_frame.clear_entries()
        # Opcional: Resetar dimensões de A para 2x2 ou outro padrão
        # self.matrix_a_frame.rows_var_str.set("2")
        # self.matrix_a_frame.cols_var_str.set("2")
        # self.matrix_a_frame.create_matrix_entries_from_dim_input()


        # Limpa B apenas se estiver visível e habilitada
        if self.right_column_frame.winfo_ismapped() and self.matrix_b_frame.is_enabled():
            self.matrix_b_frame.clear_entries()
            # Opcional: Resetar dimensões de B se não for "Resolver Sistema"
            # current_op = self.selected_operation_var.get()
            # if "Resolver Sistema" not in current_op:
            #     self.matrix_b_frame.rows_var_str.set("2")
            #     self.matrix_b_frame.cols_var_str.set("2")
            #     self.matrix_b_frame.create_matrix_entries_from_dim_input()
        
        self.scalar_var.set("1") 

        self.result_textbox.configure(state=ctk.NORMAL)
        self.result_textbox.delete("1.0", ctk.END)
        self.result_textbox.configure(state=ctk.DISABLED)
        
        self.status_label.configure(text="Campos limpos.")
        self.on_operation_change() # Reconfigura a UI para o estado inicial da operação selecionada


    def on_dimension_change_matrix_a(self):
        selected_op_str = self.selected_operation_var.get()
        if "Resolver Sistema" in selected_op_str and self.right_column_frame.winfo_ismapped():
            rows_a_str = self.matrix_a_frame.rows_var_str.get()
            self.matrix_b_frame.rows_var_str.set(rows_a_str)
            self.matrix_b_frame.create_matrix_entries_from_dim_input() 
            self.matrix_b_frame.cols_entry.configure(state=ctk.DISABLED) 

    def on_operation_change(self, choice=None):
        selected_op_str = self.selected_operation_var.get()
        
        if "Multiplicação por Escalar" in selected_op_str:
            self.scalar_input_outer_frame.grid(row=1, column=0, pady=(15, 0), sticky="ew") 
            self.scalar_entry.configure(state=ctk.NORMAL)
        else:
            self.scalar_input_outer_frame.grid_remove() 
            self.scalar_entry.configure(state=ctk.DISABLED)

        if " (A)" in selected_op_str or "Multiplicação por Escalar" in selected_op_str: 
            self.right_column_frame.grid_remove() 
            self.matrix_b_frame.set_enabled(False)
            self.main_content_frame.grid_columnconfigure(1, weight=0) 
            self.main_content_frame.grid_columnconfigure(0, weight=1) 
        else: 
            self.right_column_frame.grid(row=0, column=1, sticky="new", padx=(10, 0)) 
            self.matrix_b_frame.set_enabled(True)
            self.main_content_frame.grid_columnconfigure(1, weight=1) 
            self.main_content_frame.grid_columnconfigure(0, weight=1)

            if "Resolver Sistema" in selected_op_str:
                self.matrix_a_frame.update_title_text("Matriz A (Coeficientes)")
                self.matrix_b_frame.update_title_text("Vetor B (Termos)")
                self.on_dimension_change_matrix_a() 
            else: 
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
        if not matrix or not isinstance(matrix, list) or (not matrix[0] and len(matrix) > 0):
            return "[ Matriz Vazia ou Inválida ]"
        if isinstance(matrix[0], list) and not matrix[0]:
            return "[ Matriz com Linha(s) Vazia(s) ]"

        str_matrix = []
        try:
            num_cols_check = len(matrix[0]) 
        except IndexError: 
             return "[ Matriz com Estrutura Inesperada ]"

        for r_idx, row_val in enumerate(matrix):
            if not isinstance(row_val, list) or len(row_val) != num_cols_check:
                return f"[ Erro na formatação: Linha {r_idx+1} tem estrutura/tamanho inesperado ]"
            str_row = []
            for val in row_val:
                s_val = f"{val:.4g}".rstrip('0').rstrip('.') if isinstance(val, float) else str(val)
                if s_val == "-0": s_val = "0" 
                str_row.append(s_val)
            str_matrix.append(str_row)

        if not str_matrix or not str_matrix[0]:
             return "[ Matriz Vazia Após Processamento ]"

        num_cols = len(str_matrix[0])
        col_widths = [0] * num_cols
        for str_row_val in str_matrix:
            for c_idx, s_val in enumerate(str_row_val):
                 if c_idx < num_cols: 
                    col_widths[c_idx] = max(col_widths[c_idx], len(s_val))
                 else: 
                    return "[ Erro na formatação: Inconsistência de colunas ]"
        
        display_str = ""
        for r_idx, str_row_val in enumerate(str_matrix):
            line = "  [" 
            for c_idx, s_val in enumerate(str_row_val):
                line += f"{s_val:>{col_widths[c_idx]}}" 
                if c_idx < num_cols - 1: 
                    line += "  " 
            line += "]"
            if r_idx < len(str_matrix) - 1:
                line += "\n"
            display_str += line
        
        return display_str

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