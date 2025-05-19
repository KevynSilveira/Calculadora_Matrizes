# calculadora_matrizes/logic/transpose_matrix.py

# Importa a função de validação genérica para uma única matriz.
# Garante que a 'matrix' de entrada é uma estrutura de lista de listas válida.
from .validation_utils import validate_matrix_input

def transpose_matrix(matrix):
    """
    Calcula a transposta de uma dada 'matrix'.
    A transposta de uma matriz A, denotada por Aᵀ, é obtida trocando-se
    as linhas pelas colunas. Ou seja, o elemento Aᵀ[j][i] é igual a A[i][j].

    Args:
        matrix (list[list[float]]): A matriz a ser transposta.

    Returns:
        list[list[float]]: A matriz transposta.

    Raises:
        ValueError: Se a 'matrix' de entrada não for uma estrutura válida
                    (essa exceção é levantada por validate_matrix_input).
    """
    # 1. Validação da Matriz de Entrada:
    #    Verifica se 'matrix' é uma lista de listas bem formada e não vazia.
    #    Se a validação falhar, 'validate_matrix_input' levantará um ValueError.
    #    O nome "Matriz para transposição" é para mensagens de erro claras.
    validate_matrix_input(matrix, "Matriz para transposição")

    # 2. Obtenção das Dimensões Originais:
    #    - 'rows': Número de linhas da matriz original.
    #    - 'cols': Número de colunas da matriz original.
    #    A validação anterior garante que matrix[0] existe se a matriz for válida.
    rows = len(matrix)
    cols = len(matrix[0])

    # 3. Inicialização da Matriz Transposta (Resultado):
    #    Cria uma nova matriz 'result' preenchida com zeros.
    #    Importante: As dimensões da matriz transposta são invertidas em relação à original.
    #    Se a matriz original é M x N, a transposta será N x M.
    #    Portanto, a matriz resultado terá 'cols' linhas e 'rows' colunas.
    #    Ex: Se original é 2x3, transposta é 3x2: result = [[0,0],[0,0],[0,0]].
    result = [[0 for _ in range(rows)] for _ in range(cols)] # Note a inversão: range(rows) para colunas, range(cols) para linhas

    # 4. Processo de Transposição:
    #    Itera sobre cada elemento (i, j) da matriz ORIGINAL.
    for i in range(rows):          # Para cada linha 'i' da matriz original...
        for j in range(cols):      # Para cada coluna 'j' da matriz original...
            # O elemento matrix[i][j] da matriz original se torna
            # o elemento result[j][i] da matriz transposta.
            # As linhas da original tornam-se as colunas da transposta, e vice-versa.
            result[j][i] = matrix[i][j]

    # 5. Retorno da Matriz Transposta:
    #    A matriz 'result', agora contendo a transposta da 'matrix' original, é retornada.
    return result