# calculadora_matrizes/tests/test_utils.py
import math # Para funções matemáticas, especialmente math.isclose para comparação de floats.
import sys  # Para manipulação do sys.path, permitindo importações de módulos pais.
import os   # Para construir caminhos de arquivo de forma independente do sistema operacional.

# Configuração do Caminho de Importação:
# Esta seção modifica o sys.path para incluir o diretório pai ('calculadora_matrizes').
# Isso é crucial para que, quando os scripts de teste dentro da pasta 'tests'
# forem executados diretamente (ex: python tests/test_add_matrices.py), eles possam
# importar módulos do pacote 'logic' (ex: from logic.add_matrices import add_matrices)
# sem erros de 'ModuleNotFoundError'.
# os.path.dirname(__file__): Obtém o diretório do arquivo atual (test_utils.py).
# os.path.join(..., '..'): Navega um nível acima para o diretório pai.
# os.path.abspath(...): Obtém o caminho absoluto.
# sys.path.insert(0, ...): Adiciona este caminho no início da lista de caminhos de busca do Python.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Constante de Tolerância:
# Define uma pequena margem de erro para comparar números de ponto flutuante (floats).
# Devido à natureza da representação de floats, comparações diretas de igualdade (==)
# podem falhar mesmo para valores que são matematicamente idênticos.
# '1e-9' (ou 0.000000001) é uma tolerância comum.
TOLERANCE = 1e-9

def format_matrix_for_log(matrix, name="Matriz"):
    """
    Formata uma matriz (lista de listas), um vetor (lista de números) ou um escalar 
    para uma representação em string legível, adequada para exibição em logs de teste.
    Inclui tratamento para None, tipos inválidos e estruturas de matriz malformadas.

    Args:
        matrix (list[list[float]] or list[float] or float or int or None): A estrutura a ser formatada.
        name (str): Um nome descritivo para a matriz/vetor/escalar no log.

    Returns:
        str: A representação em string formatada.
    """
    header = f"    {name}:" # Cabeçalho padrão com indentação e nome.

    # Caso 1: Entrada é None.
    if matrix is None:
        return f"{header} None"
    
    # Caso 2: Entrada é um escalar (int ou float).
    # Usado para resultados como determinantes ou para exibir escalares de entrada.
    if isinstance(matrix, (int, float)):
        return f"{header} {matrix}"

    # Caso 3: Entrada não é uma lista (tipo inesperado para matriz/vetor).
    if not isinstance(matrix, list):
        return f"{header} [Tipo Inválido: {type(matrix)}]"
    
    # Caso 4: Entrada é uma lista vazia (representando matriz/vetor vazio).
    if not matrix: # True para []
        return f"{header} [Lista Vazia (representando matriz/vetor vazio)]"
    
    # Distingue entre uma lista de listas (matriz) e uma lista simples de números (vetor).
    is_matrix_of_lists = all(isinstance(row, list) for row in matrix)

    if not is_matrix_of_lists:
        # Se não for uma lista de listas, verifica se é uma lista de números (vetor).
        if all(isinstance(item, (int, float)) for item in matrix):
             return f"{header} {matrix}" # Formata como uma lista simples.
        # Se não for nem lista de listas nem lista de números, é uma estrutura inválida.
        return f"{header} [Estrutura Inválida detectada: não é lista de listas, nem lista de números, nem escalar]"

    # A partir daqui, 'matrix' é assumida como uma lista de listas.
    # Caso 5: Matriz contém linhas vazias (ex: [[]] ou [[1,2], []]).
    # A condição 'matrix[0]' acessa a primeira linha. 'not matrix[0]' verifica se ela é vazia.
    # 'len(matrix) > 0' garante que a matriz tem pelo menos uma linha.
    if not matrix[0] and len(matrix) > 0: # Ex: matrix = [[]]
        lines = [header, "      [Matriz com Linha(s) Vazia(s) ou Malformada (ex: [[]])]"]
        return "\n".join(lines)
    
    # Formatação detalhada para matrizes (lista de listas com conteúdo).
    try:
        # Determina o número de colunas baseado na primeira linha.
        # A consistência do número de colunas será verificada abaixo.
        num_cols = len(matrix[0]) if matrix and matrix[0] else 0
        col_widths = [0] * num_cols # Lista para armazenar a largura máxima de cada coluna para alinhamento.
        
        str_matrix = [] # Armazenará a matriz com elementos convertidos para string.
        for row_val in matrix:
            # Verificação de consistência: todas as linhas devem ter o mesmo número de colunas.
            if len(row_val) != num_cols:
                 lines = [header, "      [Inconsistência no número de colunas entre as linhas detectada durante formatação:]"]
                 for r_print_idx, r_print_val in enumerate(matrix): 
                     lines.append(f"        Linha {r_print_idx}: {r_print_val} (Comprimento: {len(r_print_val)})")
                 return "\n".join(lines)

            str_row = [] # Lista para os elementos string da linha atual.
            for c_idx, val in enumerate(row_val):
                # Formatação especial para floats para melhorar a legibilidade.
                if isinstance(val, float):
                    # Se o float é muito próximo de um inteiro, exibe como inteiro.
                    if math.isclose(val, round(val), abs_tol=TOLERANCE): 
                        s_val = str(round(val))
                    else:
                        # Formato geral com até 4 figuras significativas, remove zeros e ponto decimal desnecessários.
                        s_val = f"{val:.4g}".rstrip('0').rstrip('.') 
                    if s_val == "-0": s_val = "0" # Evita exibir "-0".
                else:
                    s_val = str(val) # Converte outros tipos (ex: int) para string.
                str_row.append(s_val)
                # Atualiza a largura máxima da coluna atual.
                if c_idx < num_cols: 
                    col_widths[c_idx] = max(col_widths[c_idx], len(s_val))
            str_matrix.append(str_row)

        # Constrói a string final da matriz formatada, linha por linha.
        lines = [header]
        for str_row_val in str_matrix:
            line_content = []
            for c_idx, s_val in enumerate(str_row_val):
                # Alinha cada elemento à direita dentro da largura calculada para sua coluna.
                line_content.append(f"{s_val:>{col_widths[c_idx]}}")
            lines.append(f"      [{', '.join(line_content)}]") # Adiciona colchetes e junta elementos com vírgula.
        return "\n".join(lines)

    except Exception as e: # Captura qualquer erro inesperado durante a formatação.
        return f"{header} [Erro ao formatar matriz: {type(e).__name__}: {e}]\n      Matriz Original Problemática: {matrix}"


def are_matrices_equal(m1, m2):
    """
    Compara duas estruturas (m1, m2), que podem ser matrizes (listas de listas),
    vetores (listas de números), ou escalares (int/float).
    Para números de ponto flutuante, a comparação é feita com uma tolerância (TOLERANCE).

    Args:
        m1, m2: As duas estruturas a serem comparadas.

    Returns:
        bool: True se as estruturas forem consideradas iguais (dentro da tolerância para floats),
              False caso contrário.
    """
    # 1. Comparação de Tipos Iniciais:
    #    Se os tipos base de m1 e m2 são diferentes, eles geralmente não são iguais.
    #    Exceção: permite que int e float sejam comparados numericamente.
    if type(m1) != type(m2):
        if isinstance(m1, (int, float)) and isinstance(m2, (int, float)):
            pass # Permite prosseguir para comparação numérica de int/float.
        else:
            return False # Tipos fundamentalmente diferentes (ex: lista e int).

    # 2. Comparação de Escalares:
    #    Se m1 (e, por implicação, m2) é um int ou float, usa math.isclose
    #    para comparar com tolerância.
    if isinstance(m1, (int, float)): 
        return math.isclose(m1, m2, rel_tol=TOLERANCE, abs_tol=TOLERANCE)
    
    # A partir daqui, m1 e m2 são assumidos como listas (sejam de números ou de listas).
    # 3. Validações de Lista:
    #    - Devem ser ambas listas.
    #    - Devem ter o mesmo comprimento (número de linhas para matrizes, ou número de elementos para vetores).
    if not isinstance(m1, list) or not isinstance(m2, list): return False # Não deveria acontecer se type(m1)==type(m2) e não são escalares
    if len(m1) != len(m2): return False
    
    #    - Se ambas são listas vazias (ex: [] ou [[]] dependendo da interpretação), são consideradas iguais.
    #      (Nota: a lógica aqui é para '[] == []'. Para '[[]] == [[]]', a recursão/loop abaixo trata).
    if not m1 and not m2: return True # Cobre '[] == []'.
    if not m1 or not m2: return False # Uma é vazia e a outra não (ex: '[]' vs '[1]').

    # 4. Distinção e Comparação de Vetores vs. Matrizes:
    #    Verifica se os elementos da lista são sub-listas (indicando uma matriz)
    #    ou diretamente números (indicando um vetor).
    m1_is_matrix_of_lists = all(isinstance(row, list) for row in m1)
    m2_is_matrix_of_lists = all(isinstance(row, list) for row in m2)

    # Se uma é matriz de listas e a outra não, são diferentes.
    if m1_is_matrix_of_lists != m2_is_matrix_of_lists: return False

    if not m1_is_matrix_of_lists: 
        # Caso: m1 e m2 são vetores (listas de números).
        # Compara cada elemento do vetor com tolerância.
        for i in range(len(m1)):
            # Verifica se os elementos são numéricos antes de usar math.isclose.
            if not isinstance(m1[i], (int, float)) or not isinstance(m2[i], (int, float)): return False 
            if not math.isclose(m1[i], m2[i], rel_tol=TOLERANCE, abs_tol=TOLERANCE): return False
        return True # Todos os elementos do vetor são próximos.

    # Caso: m1 e m2 são matrizes (listas de listas).
    # Compara cada elemento da matriz, linha por linha, coluna por coluna.
    for i in range(len(m1)): # Itera sobre as linhas.
        # Verifica se a linha atual em ambas as matrizes é uma lista e tem o mesmo comprimento.
        if not isinstance(m1[i], list) or not isinstance(m2[i], list): return False 
        if len(m1[i]) != len(m2[i]): return False
        
        for j in range(len(m1[i])): # Itera sobre os elementos (colunas) da linha atual.
            # Verifica se os elementos são numéricos.
            if not isinstance(m1[i][j], (int, float)) or not isinstance(m2[i][j], (int, float)): return False
            # Compara os elementos com tolerância.
            if not math.isclose(m1[i][j], m2[i][j], rel_tol=TOLERANCE, abs_tol=TOLERANCE):
                return False # Se qualquer elemento diferir, as matrizes não são iguais.
    return True # Todas as linhas e elementos correspondentes são próximos.

def generate_matrix(rows, cols, value_generator=lambda r, c: r * cols + c + 1):
    """
    Gera uma matriz (lista de listas) com dimensões 'rows' x 'cols'.
    Os valores de cada elemento são determinados pela função 'value_generator'.

    Args:
        rows (int): O número de linhas da matriz a ser gerada.
        cols (int): O número de colunas da matriz a ser gerada.
        value_generator (function, optional): Uma função lambda ou nomeada que aceita
            dois argumentos (índice da linha 'r', índice da coluna 'c') e retorna
            o valor para o elemento matrix[r][c].
            O padrão é um gerador que preenche a matriz com números sequenciais
            (1, 2, 3, ...).

    Returns:
        list[list[float]]: A matriz gerada.
    """
    # Usa list comprehension aninhada para construir a matriz.
    # O loop externo itera sobre as linhas (r).
    # O loop interno itera sobre as colunas (c) para cada linha.
    # 'value_generator(r, c)' é chamado para cada célula.
    return [[value_generator(r, c) for c in range(cols)] for r in range(rows)]

def print_test_header(test_file_name):
    """Imprime um cabeçalho padronizado para o início de uma suíte de testes."""
    print("-" * 70)
    print(f"INICIANDO TESTES PARA: {test_file_name}")
    print("-" * 70)

def print_test_footer(test_file_name, total_tests, passed_tests):
    """Imprime um rodapé padronizado com o resumo dos resultados da suíte de testes."""
    print("-" * 70)
    print(f"TESTES CONCLUÍDOS PARA: {test_file_name}")
    print(f"Total de Casos de Teste: {total_tests}")
    print(f"Passaram: {passed_tests}")
    print(f"Falharam: {total_tests - passed_tests}")
    print("-" * 70)
    print("\n") # Adiciona uma linha em branco para separar outputs de diferentes suítes.