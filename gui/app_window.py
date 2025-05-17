import tkinter as tk
from tkinter import ttk, messagebox
from gui.matrix_input_frame import MatrixInputFrame
from logic import matrix_operations as ops

class AppWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de Matrizes")
        self.geometry("900x680")
        self.minsize(750, 550)

        self.BG_COLOR = "#f0f0f0"
        self.INPUT_BG_COLOR = "#ffffff"
        self.TEXT_COLOR = "#333333"
        self.ACCENT_COLOR = "#007AFF"
        self.BORDER_COLOR = "#d0d0d0"
        self.ACCENT_TEXT_COLOR = "#ffffff"

        self.configure(background=self.BG_COLOR)

        s = ttk.Style()
        try:
            available_themes = s.theme_names()
            if 'clam' in available_themes: s.theme_use('clam')
            elif 'alt' in available_themes: s.theme_use('alt')
        except tk.TclError:
            print("Tema ttk padrão será usado.")

        s.configure('.', background=self.BG_COLOR, foreground=self.TEXT_COLOR, font=('Segoe UI', 10))
        s.configure('TFrame', background=self.BG_COLOR)
        s.configure('TLabel', background=self.BG_COLOR, foreground=self.TEXT_COLOR)
        s.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'), background=self.BG_COLOR)
        s.configure('TButton', padding=(10, 6), relief="flat", font=('Segoe UI', 10, 'normal'), borderwidth=1, background=self.INPUT_BG_COLOR, foreground=self.TEXT_COLOR)
        s.map('TButton', background=[('active', '#e0e0e0'), ('pressed', '#cccccc')], relief=[('pressed', 'sunken'), ('!pressed', 'flat')])
        s.configure('Accent.TButton', font=('Segoe UI', 11, 'bold'), background=self.ACCENT_COLOR, foreground=self.ACCENT_TEXT_COLOR)
        s.map('Accent.TButton', background=[('active', '#0056b3'), ('pressed', '#004085')], relief=[('pressed', 'sunken'), ('!pressed', 'flat')])
        s.configure('TSpinbox', padding=5, relief='flat', arrowsize=12, borderwidth=1, background=self.INPUT_BG_COLOR, foreground=self.TEXT_COLOR, bordercolor=self.BORDER_COLOR, fieldbackground=self.INPUT_BG_COLOR)
        s.map('TSpinbox', bordercolor=[('focus', self.ACCENT_COLOR)])
        s.configure('TEntry', padding=(5,6), relief='flat', borderwidth=1, background=self.INPUT_BG_COLOR, foreground=self.TEXT_COLOR, bordercolor=self.BORDER_COLOR, fieldbackground=self.INPUT_BG_COLOR)
        s.map('TEntry', bordercolor=[('focus', self.ACCENT_COLOR)])
        s.configure('TCombobox', padding=(5,6), relief='flat', arrowsize=12)
        s.map('TCombobox', fieldbackground=[('readonly', self.INPUT_BG_COLOR)], foreground=[('readonly', self.TEXT_COLOR)], selectbackground=[('readonly', self.INPUT_BG_COLOR)], selectforeground=[('readonly', self.TEXT_COLOR)], bordercolor=[('focus', self.ACCENT_COLOR), ('!focus', self.BORDER_COLOR)], relief=[('focus', 'flat'), ('!focus', 'flat')])
        self.option_add('*TCombobox*Listbox.font', ('Segoe UI', 10))
        self.option_add('*TCombobox*Listbox.background', self.INPUT_BG_COLOR)
        self.option_add('*TCombobox*Listbox.foreground', self.TEXT_COLOR)
        self.option_add('*TCombobox*Listbox.selectBackground', self.ACCENT_COLOR)
        self.option_add('*TCombobox*Listbox.selectForeground', self.ACCENT_TEXT_COLOR)
        self.option_add('*TCombobox*Listbox.relief', 'flat'); self.option_add('*TCombobox*Listbox.bd', 0)

        main_frame = ttk.Frame(self, padding="20 20 20 20")
        main_frame.pack(expand=True, fill=tk.BOTH)
        main_frame.columnconfigure(0, weight=1); main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        self.matrix_a_frame = MatrixInputFrame(main_frame, title="Matriz A")
        self.matrix_a_frame.grid(row=0, column=0, padx=(0,15), pady=(0,20), sticky="nsew")
        self.matrix_b_frame = MatrixInputFrame(main_frame, title="Matriz B")
        self.matrix_b_frame.grid(row=0, column=1, padx=(15,0), pady=(0,20), sticky="nsew")

        operations_container = ttk.Frame(main_frame)
        operations_container.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky="ew")
        ttk.Label(operations_container, text="Operação:", font=('Segoe UI', 11, 'bold')).pack(side=tk.LEFT, padx=(0,10), anchor='w')

        self.operations_map = {
        # --- Solução de Sistemas ---
        "Resolver AX = B (pela Inversa)": "solve_axb",
        # --- Análise de Matriz A ---
        "Determinante de A": "det_a",
        "Inversa de A": "inverse_a",
        "Transposta de A": "transpose_a",
        # --- Operações entre Matrizes ---
        "A + B (Soma)": "+",
        "A - B (Subtração)": "-",
        "A * B (Multiplicação Matricial)": "*",
        # --- Operações com Escalar ---
        "A * k (Multiplicação por Escalar)": "scalar_a",
        }
        self.operation_var = tk.StringVar()
        self.operation_combobox = ttk.Combobox(operations_container, textvariable=self.operation_var,
                                               values=list(self.operations_map.keys()), state="readonly", width=30)
        self.operation_combobox.pack(side=tk.LEFT, padx=(0,20), fill=tk.X, expand=True)
        self.operation_combobox.set(list(self.operations_map.keys())[0])
        self.operation_combobox.bind("<<ComboboxSelected>>", self.on_operation_change)

        self.scalar_label = ttk.Label(operations_container, text="Escalar:")
        self.scalar_var = tk.StringVar(value="1")
        self.scalar_entry = ttk.Entry(operations_container, textvariable=self.scalar_var, width=8)

        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=(20, 0), sticky="e")
        self.clear_button = ttk.Button(buttons_frame, text="Limpar Tudo", command=self.clear_all)
        self.clear_button.pack(side=tk.LEFT, padx=(0,10))
        self.calculate_button = ttk.Button(buttons_frame, text="Calcular", command=self.perform_calculation, style='Accent.TButton')
        self.calculate_button.pack(side=tk.LEFT)

        result_container = ttk.Frame(main_frame)
        result_container.grid(row=2, column=0, columnspan=2, pady=0, sticky="nsew")
        result_container.rowconfigure(1, weight=1); result_container.columnconfigure(0, weight=1)
        ttk.Label(result_container, text="Resultado", style='Title.TLabel').grid(row=0, column=0, sticky="w", pady=(0,8))
        text_frame = ttk.Frame(result_container, style="Result.TFrame")
        s.configure("Result.TFrame", background=self.INPUT_BG_COLOR, relief="solid", borderwidth=1, bordercolor=self.BORDER_COLOR)
        text_frame.grid(row=1, column=0, sticky="nsew"); text_frame.rowconfigure(0, weight=1); text_frame.columnconfigure(0, weight=1)
        self.result_text = tk.Text(text_frame, height=10, width=50, wrap=tk.NONE, state=tk.DISABLED, font=("Consolas", 11), relief=tk.FLAT, borderwidth=0, padx=10, pady=10, background=self.INPUT_BG_COLOR, foreground=self.TEXT_COLOR, highlightthickness=0)
        ys = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        xs = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL, command=self.result_text.xview)
        self.result_text.configure(yscrollcommand=ys.set, xscrollcommand=xs.set)
        self.result_text.grid(row=0, column=0, sticky="nsew"); ys.grid(row=0, column=1, sticky="ns"); xs.grid(row=1, column=0, sticky="ew")
        
        self.on_operation_change()

    def on_operation_change(self, event=None):
        selected_operation_text = self.operation_var.get()
        op_value = self.operations_map.get(selected_operation_text)
        self.scalar_label.pack_forget(); self.scalar_entry.pack_forget()
        self.scalar_entry.config(state=tk.DISABLED)

        if op_value == "scalar_a":
            self.scalar_label.pack(side=tk.LEFT, padx=(0,5), after=self.operation_combobox)
            self.scalar_entry.pack(side=tk.LEFT, after=self.scalar_label)
            self.scalar_entry.config(state=tk.NORMAL)
            self.matrix_b_frame.set_enabled(False)
            self.matrix_a_frame.update_title_text("Matriz (para Escalar)")
            self.matrix_b_frame.update_title_text("Matriz B (Desabilitada)")
        elif op_value in ["+", "-", "*"]:
            self.matrix_b_frame.set_enabled(True)
            self.matrix_a_frame.update_title_text("Matriz A")
            self.matrix_b_frame.update_title_text("Matriz B")
        elif op_value == "solve_axb":
            self.matrix_b_frame.set_enabled(True)
            self.matrix_a_frame.update_title_text("Matriz A (Coeficientes)")
            self.matrix_b_frame.update_title_text("Vetor B (Termos Independentes)")
        elif op_value in ["transpose_a", "det_a"]:
            self.matrix_b_frame.set_enabled(False)
            title = "Matriz (para Transpor)" if op_value == "transpose_a" else "Matriz (para Determinante)"
            self.matrix_a_frame.update_title_text(title)
            self.matrix_b_frame.update_title_text("Matriz B (Desabilitada)")
        else:
            self.matrix_b_frame.set_enabled(False)
            self.matrix_a_frame.update_title_text("Matriz A")
            self.matrix_b_frame.update_title_text("Matriz B (Desabilitada)")

    def perform_calculation(self):
        selected_operation_text = self.operation_var.get()
        op = self.operations_map.get(selected_operation_text)
        if not op: messagebox.showerror("Erro", "Selecione uma operação."); return

        matrix_a = self.matrix_a_frame.get_matrix()
        if matrix_a is None: self.display_result(""); return
        result = None
        try:
            if op in ["+", "-", "*"]:
                if not self.matrix_b_frame.is_enabled(): messagebox.showerror("Erro", "Matriz B desabilitada."); return
                matrix_b = self.matrix_b_frame.get_matrix()
                if matrix_b is None: self.display_result(""); return
                if op == "+": result = ops.add_matrices(matrix_a, matrix_b)
                elif op == "-": result = ops.subtract_matrices(matrix_a, matrix_b)
                elif op == "*": result = ops.multiply_matrices(matrix_a, matrix_b)
            elif op == "solve_axb":
                if not self.matrix_b_frame.is_enabled(): messagebox.showerror("Erro", "Vetor B desabilitado."); return
                vector_b_input = self.matrix_b_frame.get_matrix()
                if vector_b_input is None: self.display_result(""); return
                if not vector_b_input or not vector_b_input[0] or len(vector_b_input[0]) != 1:
                    messagebox.showerror("Erro", "Vetor B deve ser Nx1."); self.display_result("Erro: Vetor B deve ser Nx1."); return
                if len(matrix_a) != len(vector_b_input):
                     messagebox.showerror("Erro", "Linhas de A != Linhas de B."); self.display_result("Erro: Linhas de A != Linhas de B."); return
                
                solution_matrix = ops.solve_linear_system_inverse(matrix_a, vector_b_input)
                if solution_matrix:
                    solution_text_parts = ["Solução X:"]
                    var_names = [f"x{i+1}" for i in range(len(solution_matrix))]
                    for i, row in enumerate(solution_matrix):
                        val = row[0]
                        val_str = str(int(val)) if isinstance(val, float) and val.is_integer() else f"{val:.4g}"
                        solution_text_parts.append(f"  {var_names[i]} = {val_str}")
                    self.display_result("\n".join(solution_text_parts))
                    return # Importante: evita a formatação de matriz padrão abaixo
            elif op == "scalar_a":
                try: scalar_str = self.scalar_var.get(); scalar = float(scalar_str) if '.' in scalar_str or 'e' in scalar_str.lower() else int(scalar_str)
                except ValueError: messagebox.showerror("Erro", "Escalar inválido."); self.display_result(""); return
                result = ops.scalar_multiply(matrix_a, scalar)
            elif op == "transpose_a": result = ops.transpose_matrix(matrix_a)
            elif op == "det_a": result = ops.determinant(matrix_a)

            if result is not None: self.display_result(result)
            # Não precisa de 'else' aqui se solve_axb já fez display e retornou
        except ValueError as e: messagebox.showerror("Erro de Cálculo", str(e)); self.display_result(f"Erro: {e}")
        except Exception as e: messagebox.showerror("Erro Inesperado", f"{type(e).__name__}: {e}"); self.display_result(f"Erro: {type(e).__name__} - {e}")

    def display_result(self, result_data):
        self.result_text.config(state=tk.NORMAL, background=self.INPUT_BG_COLOR, foreground=self.TEXT_COLOR)
        self.result_text.delete("1.0", tk.END)
        if isinstance(result_data, str): self.result_text.insert(tk.END, result_data)
        elif isinstance(result_data, list) and result_data:
            if not isinstance(result_data[0], list): self.result_text.insert(tk.END, str(result_data))
            else:
                max_len = 0; str_mat = []
                for r in result_data:
                    s_r = []
                    for v in r:
                        s_v = str(int(v)) if isinstance(v,float) and v.is_integer() else (f"{v:.2f}" if isinstance(v,float) and abs(v)<1e5 and abs(v)>1e-3 and '.' in f"{v:.4g}" and len(f"{v:.4g}".split('.')[1])>2 else f"{v:.4g}")
                        if len(s_v)>max_len: max_len=len(s_v)
                        s_r.append(s_v)
                    str_mat.append(s_r)
                for r_s in str_mat: self.result_text.insert(tk.END, f"  | {'  '.join(v.rjust(max_len) for v in r_s)} |  \n")
        elif isinstance(result_data, (int, float)):
            val_s = str(int(result_data)) if isinstance(result_data,float) and result_data.is_integer() else (f"{result_data:.2f}" if isinstance(result_data,float) and abs(result_data)<1e5 and abs(result_data)>1e-3 and '.' in f"{result_data:.4g}" and len(f"{result_data:.4g}".split('.')[1])>2 else f"{result_data:.4g}")
            self.result_text.insert(tk.END, f"Valor: {val_s}")
        else: self.result_text.insert(tk.END, str(result_data))
        self.result_text.config(state=tk.DISABLED)

    def clear_all(self):
        self.matrix_a_frame.clear_entries(); self.matrix_b_frame.clear_entries()
        self.scalar_var.set("1")
        self.result_text.config(state=tk.NORMAL); self.result_text.delete("1.0", tk.END); self.result_text.config(state=tk.DISABLED)
        self.operation_combobox.set(list(self.operations_map.keys())[0])
        self.on_operation_change()