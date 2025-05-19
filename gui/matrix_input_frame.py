# calculadora_matrizes/gui/matrix_input_frame.py
import customtkinter as ctk
from tkinter import messagebox

class MatrixInputFrame(ctk.CTkFrame): # Widget reutilizável para entrada de dados de uma matriz
    def __init__(self, master, title="Matriz", max_dim=10):
        super().__init__(master, fg_color="transparent") # Herda a cor de fundo do widget pai
        self.title_text_default = title # Título padrão para este frame de matriz
        self.max_dim = max_dim # Dimensão máxima permitida para linhas/colunas
        self.entries_vars = [] # Lista para armazenar as CTkStringVars de cada célula da matriz
        self.entry_widgets = [] # Lista para armazenar os widgets CTkEntry de cada célula
        self._is_enabled = True # Estado de habilitação do frame (editável ou não)

        # Label para o título do frame (ex: "Matriz A")
        self.title_label = ctk.CTkLabel(self, text=self.title_text_default, font=("Segoe UI", 18, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=4, pady=(0, 12), sticky="w")

        # --- Seção para controle de Linhas ---
        dim_frame_rows = ctk.CTkFrame(self, fg_color="transparent")
        dim_frame_rows.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 10))

        ctk.CTkLabel(dim_frame_rows, text="Linhas:", font=("Segoe UI", 13)).pack(side=ctk.LEFT, padx=(0,6))
        self.rows_var_str = ctk.StringVar(value="2") # Variável Tkinter para o número de linhas
        
        btn_dim_width = 28 # Largura dos botões de ajuste de dimensão
        btn_dim_height = 28 # Altura dos botões de ajuste de dimensão
        
        # Botão para decrementar linhas
        ctk.CTkButton(dim_frame_rows, text="-", width=btn_dim_width, height=btn_dim_height, command=lambda: self._adjust_dim(self.rows_var_str, -1, is_rows=True)).pack(side=ctk.LEFT)
        # Campo de entrada para o número de linhas
        self.rows_entry = ctk.CTkEntry(dim_frame_rows, textvariable=self.rows_var_str, width=45, font=("Segoe UI", 13), justify="center")
        self.rows_entry.pack(side=ctk.LEFT, padx=5)
        # Botão para incrementar linhas
        ctk.CTkButton(dim_frame_rows, text="+", width=btn_dim_width, height=btn_dim_height, command=lambda: self._adjust_dim(self.rows_var_str, 1, is_rows=True)).pack(side=ctk.LEFT, padx=(0,15))
        
        # Binds para atualizar a matriz quando o valor da entrada de linhas muda (Enter ou perda de foco)
        self.rows_entry.bind("<Return>", self.create_matrix_entries_from_dim_input)
        self.rows_entry.bind("<FocusOut>", self.create_matrix_entries_from_dim_input)

        # --- Seção para controle de Colunas ---
        dim_frame_cols = ctk.CTkFrame(self, fg_color="transparent")
        dim_frame_cols.grid(row=1, column=2, columnspan=2, sticky="w", pady=(0, 10), padx=(10,0))

        ctk.CTkLabel(dim_frame_cols, text="Colunas:", font=("Segoe UI", 13)).pack(side=ctk.LEFT, padx=(0,6))
        self.cols_var_str = ctk.StringVar(value="2") # Variável Tkinter para o número de colunas

        # Botões e entrada para colunas, similar às linhas
        ctk.CTkButton(dim_frame_cols, text="-", width=btn_dim_width, height=btn_dim_height, command=lambda: self._adjust_dim(self.cols_var_str, -1, is_rows=False)).pack(side=ctk.LEFT)
        self.cols_entry = ctk.CTkEntry(dim_frame_cols, textvariable=self.cols_var_str, width=45, font=("Segoe UI", 13), justify="center")
        self.cols_entry.pack(side=ctk.LEFT, padx=5)
        ctk.CTkButton(dim_frame_cols, text="+", width=btn_dim_width, height=btn_dim_height, command=lambda: self._adjust_dim(self.cols_var_str, 1, is_rows=False)).pack(side=ctk.LEFT)

        self.cols_entry.bind("<Return>", self.create_matrix_entries_from_dim_input)
        self.cols_entry.bind("<FocusOut>", self.create_matrix_entries_from_dim_input)

        # Frame onde as células (CTkEntry) da matriz serão renderizadas
        self.entries_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.entries_frame.grid(row=2, column=0, columnspan=4, sticky="nsew", pady=(10,0))
        
        self.create_matrix_entries() # Cria as entradas iniciais da matriz (2x2 por padrão)

    def _adjust_dim(self, var_str, delta, is_rows):
        """(Método interno) Ajusta o valor da dimensão (linhas ou colunas) e recria as entradas da matriz."""
        try:
            current_val = int(var_str.get())
            new_val = current_val + delta
            # Garante que a nova dimensão está dentro dos limites (1 a max_dim)
            if 1 <= new_val <= self.max_dim:
                var_str.set(str(new_val))
            elif new_val < 1: # Mínimo de 1
                var_str.set("1")
            elif new_val > self.max_dim: # Máximo permitido
                var_str.set(str(self.max_dim))
            
            self.create_matrix_entries_from_dim_input() # Atualiza a grade de entradas
            # Notifica a janela principal se as linhas da Matriz A mudaram (para sincronização)
            if is_rows and hasattr(self, 'master_app') and self.master_app and hasattr(self.master_app, 'on_dimension_change_matrix_a'):
                 if self.title_label.cget("text").startswith("Matriz A"): # Verifica se é o frame da Matriz A
                    self.master_app.on_dimension_change_matrix_a()
        except ValueError: # Se o valor na entrada não for um inteiro
            var_str.set("2") # Reseta para um valor padrão
            self.create_matrix_entries_from_dim_input()

    def update_title_text(self, new_title_text=""):
        """Atualiza o texto do título do frame (ex: "Matriz A" para "Matriz A (Coeficientes)")."""
        self.title_label.configure(text=new_title_text if new_title_text else self.title_text_default)

    def _get_validated_dim(self, var_str, default_val):
        """(Método interno) Obtém e valida um valor de dimensão da StringVar, aplicando limites."""
        try:
            val = int(var_str.get())
            if 1 <= val <= self.max_dim: return val
            elif val < 1: var_str.set("1"); return 1
            else: var_str.set(str(self.max_dim)); return self.max_dim
        except ValueError: # Se a entrada não for um inteiro válido
            var_str.set(str(default_val)) # Reseta para o valor padrão
            return default_val

    def create_matrix_entries_from_dim_input(self, event=None): # event=None para permitir chamadas diretas
        """Valida as dimensões atuais das entradas de Linhas/Colunas e recria a grade de células da matriz."""
        self._get_validated_dim(self.rows_var_str, 2) # Valida e atualiza o valor de linhas
        self._get_validated_dim(self.cols_var_str, 2) # Valida e atualiza o valor de colunas
        self.create_matrix_entries() # Chama a função que de fato (re)cria as entradas

    def create_matrix_entries(self):
        """(Re)cria dinamicamente os campos de entrada (CTkEntry) para os elementos da matriz
        com base nas dimensões atuais definidas em rows_var_str e cols_var_str."""
        # Limpa entradas antigas
        for widget in self.entries_frame.winfo_children(): widget.destroy()
        self.entries_vars, self.entry_widgets = [], [] # Reseta as listas de variáveis e widgets

        rows = self._get_validated_dim(self.rows_var_str, 2) # Obtém o número de linhas validado
        cols = self._get_validated_dim(self.cols_var_str, 2) # Obtém o número de colunas validado

        # Cria a grade de CTkEntry widgets
        for i in range(rows):
            row_vars, row_widgets = [], []
            for j in range(cols):
                entry_var = ctk.StringVar(value="0") # Variável para cada célula, inicializada com "0"
                entry = ctk.CTkEntry(self.entries_frame, width=60, justify='center', textvariable=entry_var, font=("Consolas", 14))
                entry.grid(row=i, column=j, padx=4, pady=4, ipady=5) # Posiciona a célula no grid
                row_vars.append(entry_var)
                row_widgets.append(entry)
            self.entries_vars.append(row_vars)
            self.entry_widgets.append(row_widgets)
        self.set_enabled(self._is_enabled) # Re-aplica o estado de habilitação (editável/não editável)

    def get_matrix(self):
        """Lê os valores das células da matriz da GUI e os converte para uma lista de listas de números.
        Retorna a matriz ou None se ocorrer um erro de conversão."""
        try:
            rows = self._get_validated_dim(self.rows_var_str, 1)
            cols = self._get_validated_dim(self.cols_var_str, 1)
            matrix = []
            for i in range(rows):
                row_data = []
                for j in range(cols):
                    val_str = self.entries_vars[i][j].get() # Obtém o valor string da célula
                    val = 0.0 # Valor padrão se a célula estiver vazia
                    if not val_str.strip(): # Se a string estiver vazia ou só com espaços
                        self.entries_vars[i][j].set("0") # Atualiza a GUI para mostrar "0"
                    else:
                        try: val = int(val_str) # Tenta converter para inteiro
                        except ValueError: val = float(val_str) # Se falhar, tenta converter para float
                    row_data.append(val)
                matrix.append(row_data)
            return matrix
        except ValueError: # Erro na conversão de string para número
            messagebox.showerror("Erro de Entrada", f"Valor inválido em '{self.title_label.cget('text')}'. Insira apenas números.", parent=self)
            return None
        except IndexError: # Erro se as listas entries_vars não corresponderem às dimensões esperadas
            messagebox.showerror("Erro Interno", "Erro ao ler a matriz. Verifique as dimensões.", parent=self)
            return None

    def set_matrix(self, matrix_data):
        """Preenche as células da matriz na GUI com os valores de 'matrix_data'.
        Ajusta as dimensões do frame se necessário, dentro dos limites."""
        # Validação básica da matrix_data
        if not matrix_data or not isinstance(matrix_data, list) or \
           not all(isinstance(row, list) for row in matrix_data) or \
           (matrix_data and not matrix_data[0] and len(matrix_data)>0): # Caso como [[]]
            self.rows_var_str.set("1"); self.cols_var_str.set("1") # Reseta para 1x1
            self.create_matrix_entries()
            if self.entries_vars and self.entries_vars[0]: self.entries_vars[0][0].set("0") # Coloca "0" na célula 1x1
            return

        rows = len(matrix_data)
        cols = len(matrix_data[0]) if rows > 0 and matrix_data[0] else 0 # Evita erro se matrix_data[0] for vazia

        if rows == 0 or cols == 0: # Se a matriz de dados for efetivamente vazia
            self.rows_var_str.set("1"); self.cols_var_str.set("1")
            self.create_matrix_entries()
            if self.entries_vars and self.entries_vars[0]: self.entries_vars[0][0].set("0")
            return
            
        # Define as dimensões na GUI, respeitando max_dim
        self.rows_var_str.set(str(min(rows, self.max_dim)))
        self.cols_var_str.set(str(min(cols, self.max_dim)))
        self.create_matrix_entries() # Recria as células com as novas dimensões

        actual_rows = self._get_validated_dim(self.rows_var_str, 1) # Linhas realmente criadas na GUI
        actual_cols = self._get_validated_dim(self.cols_var_str, 1) # Colunas realmente criadas na GUI

        # Preenche as células com os dados
        for i in range(actual_rows):
            for j in range(actual_cols):
                if i < rows and j < cols: # Garante que não tentamos acessar fora dos limites de matrix_data
                    val = matrix_data[i][j]
                    # Formata o número para exibição (inteiro se for .0, senão com precisão)
                    val_str = str(int(val)) if isinstance(val, float) and val.is_integer() else \
                              f"{val:.4g}".rstrip('0').rstrip('.') if isinstance(val, float) else \
                              str(val)
                    self.entries_vars[i][j].set(val_str)
                else: # Se a matrix_data for menor que as dimensões da GUI (raro aqui)
                    self.entries_vars[i][j].set("0")

    def clear_entries(self):
        """Limpa todas as células da matriz, definindo seus valores para "0"."""
        for row_var_list in self.entries_vars:
            for entry_var in row_var_list:
                entry_var.set("0")

    def set_enabled(self, enabled=True):
        """Habilita ou desabilita todos os controles de entrada dentro deste frame (células, botões de dimensão, entradas de dimensão)."""
        self._is_enabled = enabled # Armazena o estado
        state = ctk.NORMAL if enabled else ctk.DISABLED # Estado Tkinter correspondente
        
        # Habilita/desabilita botões de ajuste de dimensão e entradas de dimensão
        # Isso percorre os frames de dim_frame_rows e dim_frame_cols
        for child_frame in self.winfo_children(): # Itera sobre os filhos diretos do MatrixInputFrame
            if isinstance(child_frame, ctk.CTkFrame): # Se for um dos dim_frames ou entries_frame
                 # Itera sobre os widgets dentro desses frames filhos
                 for widget_in_child_frame in child_frame.winfo_children():
                    # Se for um botão ou uma entrada nos dim_frames
                    if child_frame in (self.nametowidget(str(self.grid_slaves(row=1, column=0)[0])), 
                                       self.nametowidget(str(self.grid_slaves(row=1, column=2)[0]))): # Identifica dim_frame_rows e dim_frame_cols
                        if isinstance(widget_in_child_frame, (ctk.CTkButton, ctk.CTkEntry)):
                            widget_in_child_frame.configure(state=state)
        
        # Habilita/desabilita as células da matriz (widgets CTkEntry)
        for row_widget_list in self.entry_widgets:
            for entry_widget in row_widget_list:
                entry_widget.configure(state=state)
        
        # Garante que as entradas de dimensão (rows_entry, cols_entry) também sigam o estado
        # Essa redundância é para cobrir casos onde os widgets podem não estar nos frames filhos esperados
        # ou para simplificar se a estrutura interna mudar.
        # A lógica anterior com winfo_children já deveria cobrir isso se eles estiverem nesses frames.
        # Para ser mais explícito e seguro:
        if hasattr(self, 'rows_entry'): self.rows_entry.configure(state=state)
        if hasattr(self, 'cols_entry'): self.cols_entry.configure(state=state)


    def is_enabled(self):
        """Retorna o estado de habilitação atual do frame."""
        return self._is_enabled