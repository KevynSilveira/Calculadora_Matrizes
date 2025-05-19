# calculadora_matrizes/gui/app_window.py
import customtkinter as ctk
from tkinter import messagebox
from .matrix_input_frame import MatrixInputFrame # Widget reutilizável para entrada de matrizes
from logic import ( # Funções de cálculo de matriz importadas do pacote de lógica
    add_matrices, subtract_matrices, multiply_matrices, scalar_multiply,
    transpose_matrix, determinant, inverse_matrix, solve_linear_system_inverse
)

class AppWindow(ctk.CTk): # Janela principal da aplicação, herda de ctk.CTk
    def __init__(self):
        super().__init__()
        self.title("Calculadora de Matrizes")
        self.geometry("950x920") # Define o tamanho inicial da janela
        
        # Configura o sistema de grid da janela raiz para que o frame principal (main_content_frame)
        # possa expandir e ocupar todo o espaço disponível. weight=1 permite expansão.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) 

        # Frame principal que atua como container para todos os elementos da UI,
        # permitindo padding e gerenciamento de layout centralizado.
        self.main_content_frame = ctk.CTkFrame(self, fg_color="transparent") # fg_color transparente para herdar do tema
        self.main_content_frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25) # "nsew" faz o frame expandir com a janela
        # Configura o grid interno do main_content_frame para duas colunas principais (Matriz A e Matriz B)
        self.main_content_frame.grid_columnconfigure(0, weight=1) 
        self.main_content_frame.grid_columnconfigure(1, weight=1) 

        # --- Coluna Esquerda: Contém Matriz A e o campo de entrada para o Escalar ---
        left_column_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        left_column_frame.grid(row=0, column=0, sticky="new", padx=(0, 10)) # 'n' para alinhar ao topo, 'e' para expandir leste, 'w' para expandir oeste
        left_column_frame.grid_columnconfigure(0, weight=1) # Permite que o conteúdo da coluna expanda horizontalmente

        # Instância do widget reutilizável MatrixInputFrame para a Matriz A
        self.matrix_a_frame = MatrixInputFrame(left_column_frame, title="Matriz A", max_dim=10)
        self.matrix_a_frame.grid(row=0, column=0, sticky="ew") # Ocupa a largura da coluna
        # Passa uma referência da AppWindow para o MatrixInputFrame.
        # Isso permite que MatrixInputFrame chame métodos da AppWindow (ex: on_dimension_change_matrix_a).
        self.matrix_a_frame.master_app = self 

        # Frame container para a entrada de escalar. Sua visibilidade é controlada dinamicamente.
        self.scalar_input_outer_frame = ctk.CTkFrame(left_column_frame, fg_color="transparent")
        # O posicionamento (grid) do scalar_input_outer_frame é gerenciado por on_operation_change().
        
        self.scalar_input_frame = ctk.CTkFrame(self.scalar_input_outer_frame, fg_color="transparent")
        self.scalar_input_frame.pack() # Usa pack para centralizar Label e Entry dentro do outer_frame.
        ctk.CTkLabel(self.scalar_input_frame, text="Escalar:", font=("Segoe UI", 14)).pack(side=ctk.LEFT, padx=(0,8))
        self.scalar_var = ctk.StringVar(value="1") # Variável Tkinter para o valor do escalar
        self.scalar_entry = ctk.CTkEntry(self.scalar_input_frame, textvariable=self.scalar_var, width=120, font=("Segoe UI", 13))
        self.scalar_entry.pack(side=ctk.LEFT)

        # --- Coluna Direita: Contém Matriz B ---
        self.right_column_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        # O posicionamento (grid) do right_column_frame é gerenciado por on_operation_change().

        # Instância do widget reutilizável MatrixInputFrame para a Matriz B ou Vetor B
        self.matrix_b_frame = MatrixInputFrame(self.right_column_frame, title="Matriz B / Vetor B", max_dim=10)
        self.matrix_b_frame.pack(fill="x", expand=True, padx=0, pady=0) # Preenche a largura do right_column_frame
        
        # --- Seção de Operações: Contém a ComboBox para seleção de operação ---
        operations_main_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        operations_main_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(25, 15)) # Ocupa as duas colunas
        operations_main_frame.grid_columnconfigure(0, weight=1) # Para centralizar ComboBox e botões de ação

        self.operation_options = [ # Lista de operações disponíveis
            "Adição (A + B)", "Subtração (A - B)", "Multiplicação (A * B)",
            "Multiplicação por Escalar (k * A)", "Transposição (A)",
            "Determinante (A)", "Inversa (A)", "Resolver Sistema (AX = B)"
        ]
        self.selected_operation_var = ctk.StringVar(value=self.operation_options[0]) # Operação selecionada por padrão
        
        self.operation_combobox = ctk.CTkComboBox(
            operations_main_frame, values=self.operation_options, variable=self.selected_operation_var,
            font=("Segoe UI", 15), dropdown_font=("Segoe UI", 14), command=self.on_operation_change, # Chama on_operation_change ao selecionar
            height=38, border_width=1
        )
        self.operation_combobox.grid(row=0, column=0, sticky="ew", padx=70, ipady=4) # padx para não esticar totalmente

        # --- Frame para Botões de Ação: Limpar e Calcular ---
        # Agrupa os botões para facilitar o posicionamento lado a lado e centralizado.
        action_buttons_frame = ctk.CTkFrame(operations_main_frame, fg_color="transparent")
        action_buttons_frame.grid(row=1, column=0, pady=(20, 20)) # Centralizado abaixo da ComboBox

        self.clear_button = ctk.CTkButton( 
            action_buttons_frame, text="Limpar Tudo", command=self.clear_all_fields, # Ação de limpar
            font=("Segoe UI", 17, "bold"), height=50, width=200, corner_radius=8,
            fg_color="gray50", hover_color="gray35" # Estilo distinto para o botão Limpar
        )
        self.clear_button.pack(side=ctk.LEFT, padx=(0, 10)) # Posiciona à esquerda dentro do action_buttons_frame

        self.calculate_button = ctk.CTkButton(
            action_buttons_frame, text="Calcular", command=self.execute_selected_operation, # Ação de calcular
            font=("Segoe UI", 17, "bold"), height=50, width=200, corner_radius=8
        )
        self.calculate_button.pack(side=ctk.LEFT, padx=(10, 0)) # Posiciona à direita do botão Limpar

        # --- Seção de Resultado: Contém o Textbox para exibir o resultado ---
        result_section_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        result_section_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(10,15))
        result_section_frame.grid_columnconfigure(0, weight=1) # Label do resultado
        result_section_frame.grid_rowconfigure(1, weight=1) # Textbox do resultado (para expandir verticalmente)

        ctk.CTkLabel(result_section_frame, text="Resultado:", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, sticky="w", pady=(0,8))
        self.result_textbox = ctk.CTkTextbox(
            result_section_frame, height=220, font=("Consolas", 15), # Fonte monoespaçada para matrizes
            wrap="none", activate_scrollbars=True, border_width=1 # 'wrap="none"' para barras de rolagem horizontais
        )
        self.result_textbox.grid(row=1, column=0, sticky="nsew") # Ocupa todo o espaço disponível na sua célula
        self.result_textbox.configure(state=ctk.DISABLED) # O resultado é apenas para visualização, não editável
        self.main_content_frame.grid_rowconfigure(2, weight=1) # Permite que a seção de resultado expanda verticalmente

        # --- Barra de Status: Exibe mensagens informativas ou de erro ---
        # Posicionada na parte inferior da janela principal, fora do main_content_frame.
        status_bar_frame = ctk.CTkFrame(self, height=35, corner_radius=0, border_width=1, border_color=("gray60", "gray30"))
        status_bar_frame.grid(row=1, column=0, sticky="ew") # Ocupa toda a largura da janela
        self.status_label = ctk.CTkLabel(status_bar_frame, text="Pronto.", anchor="w", font=("Segoe UI", 12))
        self.status_label.pack(side=ctk.LEFT, padx=15, pady=5) # Alinhado à esquerda dentro da barra

        self.on_operation_change() # Chamada inicial para configurar a UI baseada na operação padrão da ComboBox

    def clear_all_fields(self):
        """Limpa os campos de entrada das matrizes (A e B, se visível), o campo de escalar,
        e o Textbox de resultado. Atualiza a barra de status."""
        self.matrix_a_frame.clear_entries()

        # Limpa Matriz B apenas se seu frame pai (right_column_frame) estiver visível
        # e o próprio frame da Matriz B estiver habilitado.
        if self.right_column_frame.winfo_ismapped() and self.matrix_b_frame.is_enabled():
            self.matrix_b_frame.clear_entries()
        
        self.scalar_var.set("1") # Reseta o valor do escalar para o padrão

        # Habilita temporariamente o Textbox para limpar, depois desabilita novamente.
        self.result_textbox.configure(state=ctk.NORMAL)
        self.result_textbox.delete("1.0", ctk.END) # Deleta todo o texto
        self.result_textbox.configure(state=ctk.DISABLED)
        
        self.status_label.configure(text="Campos limpos.")
        # Reconfigura a UI (visibilidade de B, escalar) para o estado da operação atualmente selecionada.
        self.on_operation_change()

    def on_dimension_change_matrix_a(self):
        """
        Callback acionado quando as dimensões da Matriz A são alteradas.
        Se a operação selecionada for "Resolver Sistema" e a Matriz B estiver visível,
        esta função ajusta o número de linhas da Matriz B para corresponder ao da Matriz A
        e garante que Matriz B tenha apenas uma coluna (configurando-a como um vetor).
        """
        selected_op_str = self.selected_operation_var.get()
        # A verificação winfo_ismapped() garante que não tentamos modificar B se ela não estiver na tela.
        if "Resolver Sistema" in selected_op_str and self.right_column_frame.winfo_ismapped():
            rows_a_str = self.matrix_a_frame.rows_var_str.get() # Pega o número de linhas de A
            self.matrix_b_frame.rows_var_str.set(rows_a_str)   # Define o mesmo número de linhas para B
            self.matrix_b_frame.cols_var_str.set("1")          # Força B a ter 1 coluna
            self.matrix_b_frame.create_matrix_entries_from_dim_input() # Recria as entradas de B
            self.matrix_b_frame.cols_entry.configure(state=ctk.DISABLED) # Trava a edição das colunas de B

    def on_operation_change(self, choice=None): # O argumento 'choice' é o valor selecionado na ComboBox
        """
        Atualiza a interface gráfica do usuário (UI) com base na operação de matriz selecionada.
        Isso inclui mostrar/esconder o campo de escalar e a Matriz B, e ajustar os pesos
        das colunas do layout para otimizar o espaço.
        """
        selected_op_str = self.selected_operation_var.get() # Obtém a operação atualmente selecionada
        
        # Gerencia a visibilidade do campo de entrada para o escalar
        if "Multiplicação por Escalar" in selected_op_str:
            # Posiciona o frame do escalar na UI se a operação o requer
            self.scalar_input_outer_frame.grid(row=1, column=0, pady=(15, 0), sticky="ew") 
            self.scalar_entry.configure(state=ctk.NORMAL) # Habilita a entrada do escalar
        else:
            self.scalar_input_outer_frame.grid_remove() # Remove o frame do escalar da UI
            self.scalar_entry.configure(state=ctk.DISABLED) # Desabilita a entrada do escalar

        # Gerencia a visibilidade e configuração da Matriz B (localizada na coluna da direita)
        # Condição: operações unárias (que afetam apenas A) ou multiplicação por escalar (não usa B)
        if " (A)" in selected_op_str or "Multiplicação por Escalar" in selected_op_str: 
            self.right_column_frame.grid_remove() # Remove a coluna da Matriz B da UI
            self.matrix_b_frame.set_enabled(False) # Desabilita logicamente o frame da Matriz B
            # Ajusta os pesos das colunas no main_content_frame para que a Matriz A ocupe todo o espaço
            self.main_content_frame.grid_columnconfigure(1, weight=0) # Coluna da direita (B) não expande
            self.main_content_frame.grid_columnconfigure(0, weight=1) # Coluna da esquerda (A) expande
        else: 
            # Operações que requerem Matriz B (Adição, Subtração, Multiplicação A*B, Resolver Sistema)
            self.right_column_frame.grid(row=0, column=1, sticky="new", padx=(10, 0)) # Mostra a coluna da Matriz B
            self.matrix_b_frame.set_enabled(True) # Habilita o frame da Matriz B
            # Ambas as colunas dividem o espaço disponível igualmente
            self.main_content_frame.grid_columnconfigure(1, weight=1) 
            self.main_content_frame.grid_columnconfigure(0, weight=1)

            # Configurações adicionais específicas para certas operações que usam Matriz B
            if "Resolver Sistema" in selected_op_str:
                self.matrix_a_frame.update_title_text("Matriz A (Coeficientes)") # Atualiza título de A
                self.matrix_b_frame.update_title_text("Vetor B (Termos)")      # Atualiza título de B
                self.on_dimension_change_matrix_a() # Sincroniza dimensões de B com A e a configura como vetor
            else: # Adição, Subtração, Multiplicação A*B
                self.matrix_a_frame.update_title_text("Matriz A") # Título padrão para A
                self.matrix_b_frame.update_title_text("Matriz B") # Título padrão para B
                self.matrix_b_frame.cols_entry.configure(state=ctk.NORMAL) # Permite editar colunas de B
                self.matrix_b_frame.rows_entry.configure(state=ctk.NORMAL) # Permite editar linhas de B

        self.status_label.configure(text=f"Operação: {selected_op_str}") # Atualiza a barra de status

    def _get_scalar(self):
        """Obtém o valor numérico do campo de escalar, validando-o.
        Retorna o escalar como float ou int, ou None se a entrada for inválida."""
        try:
            s_str = self.scalar_var.get()
            if not s_str.strip(): # Se vazio, assume 1 como padrão
                self.scalar_var.set("1")
                return 1.0 
            # Tenta converter para float se contiver '.', ou 'e'/'E' para notação científica, senão para int.
            return float(s_str) if '.' in s_str or 'e' in s_str.lower() else int(s_str)
        except ValueError: # Se a conversão falhar
            self.show_error("Valor escalar inválido.")
            return None

    def format_matrix_for_display(self, matrix_data):
        """Formata uma matriz (lista de listas) ou um escalar para uma representação textual
        bem alinhada, adequada para exibição no CTkTextbox."""
        if isinstance(matrix_data, (int, float)): return str(matrix_data) # Retorna como string se for escalar
        
        # Validações robustas da estrutura da matriz de entrada
        if not matrix_data or not isinstance(matrix_data, list): return "[ Entrada Inválida ]"
        if not matrix_data[0] and len(matrix_data) > 0 : return "[ Matriz com Linha(s) Vazia(s) ]" # Ex: [[]]
        if not isinstance(matrix_data[0], list): return "[ Formato de Matriz Inesperado (não é lista de listas) ]"
        if isinstance(matrix_data[0], list) and not matrix_data[0] and len(matrix_data[0])==0 and len(matrix_data)>0 : # Ex: [[],[]]
             return "[ Matriz com Linhas Vazias Internas ]"


        str_matrix = [] # Armazenará a matriz como lista de listas de strings
        try:
            # Assume que todas as linhas devem ter o mesmo número de colunas que a primeira linha
            num_cols_expected = len(matrix_data[0]) 
        except IndexError: # Se matrix_data[0] for inacessível (ex: matrix_data é [[]] que escapou das checagens)
             return "[ Estrutura de Matriz Inconsistente ]"

        # Converte cada elemento para string e verifica a consistência do número de colunas
        for r_idx, row_list in enumerate(matrix_data):
            if not isinstance(row_list, list) or len(row_list) != num_cols_expected:
                return f"[ Erro de Formato: Linha {r_idx+1} com {len(row_list)} colunas, esperado {num_cols_expected} ]"
            
            str_row_elements = []
            for val in row_list:
                # Formata floats para melhor legibilidade, caso contrário converte para string
                s_val = f"{val:.4g}".rstrip('0').rstrip('.') if isinstance(val, float) else str(val)
                if s_val == "-0": s_val = "0" # Correção estética para evitar "-0"
                str_row_elements.append(s_val)
            str_matrix.append(str_row_elements)

        if not str_matrix or not str_matrix[0]: # Se, após o processamento, str_matrix estiver vazia
             return "[ Matriz Resultou Vazia Após Formatação ]"

        actual_num_cols = len(str_matrix[0])
        col_widths = [0] * actual_num_cols # Largura máxima de cada coluna

        # Determina a largura necessária para cada coluna para alinhamento
        for s_row in str_matrix:
            for c_idx, s_val_element in enumerate(s_row):
                 if c_idx < actual_num_cols: 
                    col_widths[c_idx] = max(col_widths[c_idx], len(s_val_element))
                 # else: caso de inconsistência já tratado acima.
        
        # Constrói a string final, formatando cada linha
        output_lines = []
        for s_row in str_matrix:
            formatted_elements = [f"{s_val_element:>{col_widths[c_idx]}}" for c_idx, s_val_element in enumerate(s_row)]
            output_lines.append("  [ " + "  ".join(formatted_elements) + " ]") # Adiciona indentação e formatação
        
        return "\n".join(output_lines)


    def display_result(self, result_data, operation_name=""):
        """Exibe o resultado formatado da operação no CTkTextbox e atualiza a barra de status."""
        self.result_textbox.configure(state=ctk.NORMAL) # Habilita o Textbox para modificação
        self.result_textbox.delete("1.0", ctk.END)   # Limpa qualquer conteúdo anterior
        formatted_output = self.format_matrix_for_display(result_data) # Formata o resultado
        self.result_textbox.insert("1.0", formatted_output) # Insere o resultado formatado
        self.result_textbox.configure(state=ctk.DISABLED) # Desabilita o Textbox novamente (read-only)
        self.show_success(f"'{operation_name}' calculado.") # Mensagem de sucesso na barra de status

    def show_error(self, message):
        """Exibe uma caixa de diálogo de erro e atualiza a barra de status com a mensagem de erro."""
        messagebox.showerror("Erro de Operação", message, parent=self) # 'parent=self' para modal relativo à janela
        self.status_label.configure(text=f"Erro: {message}")

    def show_success(self, message="Operação concluída com sucesso."):
        """Atualiza a barra de status com uma mensagem de sucesso."""
        self.status_label.configure(text=message)

    def execute_selected_operation(self):
        """
        Ponto central para executar a operação de matriz selecionada.
        Coleta os inputs, chama a função lógica apropriada e lida com a exibição
        do resultado ou de mensagens de erro.
        """
        selected_op_str = self.selected_operation_var.get()
        # Garante que a UI (visibilidade dos campos B e escalar) esteja correta para a operação atual
        # antes de tentar obter os valores das matrizes.
        self.on_operation_change() 

        matrix_a = self.matrix_a_frame.get_matrix()
        if matrix_a is None: return # Se get_matrix retornou None, um erro já foi mostrado

        # Inicializa variáveis para a função lógica e seus requisitos
        op_func, needs_b, needs_scalar = None, False, False
        
        # Mapeia as strings das opções da ComboBox para as funções lógicas correspondentes
        # e flags indicando se a Matriz B ou um escalar são necessários.
        op_map = {
            "Adição (A + B)": (add_matrices, True, False),
            "Subtração (A - B)": (subtract_matrices, True, False),
            "Multiplicação (A * B)": (multiply_matrices, True, False),
            "Multiplicação por Escalar (k * A)": (scalar_multiply, False, True),
            "Transposição (A)": (transpose_matrix, False, False),
            "Determinante (A)": (determinant, False, False),
            "Inversa (A)": (inverse_matrix, False, False),
            "Resolver Sistema (AX = B)": (solve_linear_system_inverse, True, False) # needs_b é True para o vetor B
        }

        if selected_op_str in op_map:
            op_func, needs_b, needs_scalar = op_map[selected_op_str]
        else: 
            self.show_error("Operação selecionada não está mapeada para uma função.")
            return

        try:
            args_for_op_func = [matrix_a] # Matriz A é sempre um argumento
            
            # Coleta Matriz B se a operação a requer e se o frame de B está visível
            if needs_b: 
                if not self.right_column_frame.winfo_ismapped(): # Segurança: verifica se B deveria estar visível
                    self.show_error(f"Matriz B é necessária para '{selected_op_str}' mas não está disponível na UI.")
                    return
                matrix_b = self.matrix_b_frame.get_matrix()
                if matrix_b is None: return # Erro ao obter Matriz B já foi mostrado
                args_for_op_func.append(matrix_b)
            
            # Coleta o escalar se a operação o requer e se o campo de escalar está visível
            if needs_scalar:
                if not self.scalar_input_outer_frame.winfo_ismapped(): # Segurança
                     self.show_error(f"Escalar é necessário para '{selected_op_str}' mas não está disponível na UI.")
                     return
                scalar_val = self._get_scalar()
                if scalar_val is None: return # Erro ao obter o escalar já foi mostrado
                args_for_op_func.append(scalar_val)

            # Executa a função lógica com os argumentos coletados
            result_data = op_func(*args_for_op_func)
            self.display_result(result_data, selected_op_str) # Exibe o resultado

        except ValueError as ve: # Captura ValueErrors levantados pelas funções lógicas (ex: dimensões inválidas)
            self.show_error(str(ve))
        except Exception as e: # Captura quaisquer outras exceções inesperadas durante o cálculo
            self.show_error(f"Erro inesperado durante o cálculo ({type(e).__name__}): {str(e)}")