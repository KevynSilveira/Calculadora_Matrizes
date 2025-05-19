# calculadora_matrizes/logic/helper_utils.py

# Importação de 'determinant' e 'transpose_matrix' é feita dentro das funções 
# que as utilizam (get_cofactor, adjoint_matrix) para evitar importações circulares
# caso este módulo helper_utils também fosse importado por eles no nível do módulo.

def print_matrix(matrix, name="Matrix"):
    """
    Função auxiliar para imprimir uma matriz formatada no console.
    Útil para depuração e testes manuais.
    """
    # Imprime o nome da matriz.
    print(f"{name}:")

    # 1. Validação Básica da Estrutura da Matriz:
    #    Verifica se 'matrix' é uma lista de listas não vazia.
    #    Se não for, imprime uma mensagem de erro e retorna.
    if not matrix or not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
        print("  [Matriz Inválida ou Vazia]")
        return
    
    # 2. Validação de Linhas Vazias Internas:
    #    Verifica se a matriz, embora não vazia, contém linhas internas que são listas vazias.
    #    Ex: matrix = [[]] ou matrix = [[1,2], []] (a segunda linha é vazia).
    #    A condição 'matrix and not matrix[0]' checa se a primeira linha é vazia (se a matriz existe).
    if matrix and not matrix[0] and len(matrix) > 0 : 
        print("  [Matriz com Linha(s) Vazia(s)]")
        return
    
    # 3. Impressão das Linhas da Matriz:
    #    Itera sobre cada 'row' (que é uma lista representando uma linha) na 'matrix'.
    for row in matrix:
        # Imprime a linha formatada com uma indentação.
        print(f"  {row}")
    
    # Imprime um separador para melhor visualização.
    print("-" * 20)


def get_minor(matrix, r, c):
    """
    Calcula e retorna a submatriz (menor) de 'matrix'.
    O menor é obtido removendo-se a linha 'r' e a coluna 'c' da matriz original.
    Essencial para o cálculo de cofatores e determinantes.

    Args:
        matrix (list[list[float]]): A matriz original.
        r (int): O índice da linha a ser removida (0-indexed).
        c (int): O índice da coluna a ser removida (0-indexed).

    Returns:
        list[list[float]]: A submatriz resultante (menor).
    """
    # 1. Seleção de Linhas:
    #    Cria uma nova lista de linhas excluindo a linha 'r'.
    #    'matrix[:r]' pega todas as linhas ANTES da linha 'r'.
    #    'matrix[r+1:]' pega todas as linhas DEPOIS da linha 'r'.
    #    A concatenação (matrix[:r] + matrix[r+1:]) resulta na matriz sem a linha 'r'.
    rows_without_r = matrix[:r] + matrix[r+1:]

    # 2. Seleção de Colunas para Cada Linha Restante:
    #    Para cada 'row' nas 'rows_without_r' (linhas que sobraram):
    #    - 'row[:c]' pega todos os elementos da linha ANTES da coluna 'c'.
    #    - 'row[c+1:]' pega todos os elementos da linha DEPOIS da coluna 'c'.
    #    - A concatenação (row[:c] + row[c+1:]) resulta na linha sem o elemento da coluna 'c'.
    #    Uma nova lista de listas (a submatriz menor) é construída com essas linhas modificadas.
    minor_submatrix = [row[:c] + row[c+1:] for row in rows_without_r]
    
    return minor_submatrix


def get_cofactor(matrix, r_idx, c_idx):
    """
    Calcula o cofator de um elemento específico matrix[r_idx][c_idx].
    O cofator é C_ij = (-1)^(i+j) * M_ij, onde M_ij é o determinante do menor.

    Args:
        matrix (list[list[float]]): A matriz original.
        r_idx (int): O índice da linha do elemento (0-indexed).
        c_idx (int): O índice da coluna do elemento (0-indexed).

    Returns:
        float: O valor do cofator.
    """
    # Importação local para evitar dependência circular no nível do módulo.
    from .determinant import determinant

    # 1. Obtenção do Menor:
    #    Calcula a submatriz (menor) removendo a linha 'r_idx' e a coluna 'c_idx'.
    minor_matrix = get_minor(matrix, r_idx, c_idx)

    # 2. Cálculo do Sinal:
    #    O sinal do cofator é determinado por (-1) elevado à soma dos índices da linha e coluna.
    sign = (-1)**(r_idx + c_idx)

    # 3. Cálculo do Valor do Cofator:
    #    Multiplica o sinal pelo determinante da submatriz (menor).
    #    A função 'determinant' é chamada recursivamente (ou diretamente se o menor for 2x2, 1x1, ou 0x0).
    cofactor_value = sign * determinant(minor_matrix)
    
    return cofactor_value


def matrix_of_cofactors(matrix):
    """
    Cria e retorna a matriz dos cofatores para uma dada 'matrix'.
    Cada elemento da matriz de cofatores é o cofator do elemento correspondente
    na matriz original.

    Pré-condição: A 'matrix' de entrada geralmente é quadrada para este contexto,
                 embora a função em si não valide isso (a validação ocorre antes,
                 nas funções que usam a matriz de cofatores, como inverse_matrix).

    Args:
        matrix (list[list[float]]): A matriz original.

    Returns:
        list[list[float]]: A matriz de cofatores.
    """
    # 1. Obtenção das Dimensões:
    #    Assume-se que 'matrix' é uma matriz válida (lista de listas não vazia).
    rows = len(matrix)
    cols = len(matrix[0]) 

    # 2. Inicialização da Matriz de Cofatores:
    #    Cria uma nova matriz (cofactor_matrix) preenchida com zeros,
    #    com as mesmas dimensões da matriz de entrada.
    cofactor_matrix = [[0 for _ in range(cols)] for _ in range(rows)]

    # 3. Cálculo de Cada Cofator:
    #    Itera sobre cada posição (r, c) da matriz original.
    for r in range(rows):      # Para cada linha r...
        for c in range(cols):  # Para cada coluna c...
            # Calcula o cofator do elemento matrix[r][c] usando a função get_cofactor
            # e armazena o resultado na posição (r,c) da cofactor_matrix.
            cofactor_matrix[r][c] = get_cofactor(matrix, r, c)
            
    # 4. Retorno da Matriz de Cofatores:
    return cofactor_matrix


def adjoint_matrix(matrix):
    """
    Calcula a matriz adjunta (ou adjugada) de uma 'matrix'.
    A matriz adjunta é a transposta da matriz dos cofatores.
    É um passo crucial para calcular a inversa de uma matriz.

    Args:
        matrix (list[list[float]]): A matriz original (geralmente quadrada).

    Returns:
        list[list[float]]: A matriz adjunta.
    """
    # Importação local para evitar dependência circular.
    from .transpose_matrix import transpose_matrix

    # 1. Cálculo da Matriz de Cofatores:
    #    Primeiro, calcula-se a matriz de cofatores da 'matrix' original.
    cofactor_m = matrix_of_cofactors(matrix)

    # 2. Transposição da Matriz de Cofatores:
    #    A matriz adjunta é obtida transpondo a matriz de cofatores.
    adj_matrix = transpose_matrix(cofactor_m)
    
    # 3. Retorno da Matriz Adjunta:
    return adj_matrix