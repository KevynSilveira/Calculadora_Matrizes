# calculadora_matrizes/logic/add_matrices.py
from .validation_utils import validate_matrices_for_add_sub

def add_matrices(matrix_a, matrix_b):
    """
    Soma duas matrizes, A e B.
    Pré-condição: Matrizes A e B devem ser válidas e ter as mesmas dimensões.
    Retorna: Uma nova matriz contendo a soma de A e B.
    """
    # 1. Validação das entradas:
    #    Garante que A e B são matrizes válidas e possuem dimensões idênticas.
    #    Se não, uma exceção (ValueError) é lançada pela função de validação.
    validate_matrices_for_add_sub(matrix_a, matrix_b)

    # 2. Obtenção das dimensões:
    #    As dimensões da matriz resultado serão as mesmas das matrizes de entrada.
    rows = len(matrix_a)      # Número de linhas.
    cols = len(matrix_a[0])   # Número de colunas.

    # 3. Criação da matriz resultado:
    #    Inicializa uma nova matriz (result) com zeros, do mesmo tamanho de A e B.
    #    Ex: Para A e B 2x3, result = [[0, 0, 0], [0, 0, 0]].
    result = [[0 for _ in range(cols)] for _ in range(rows)]

    # 4. Processo de soma:
    #    Itera sobre cada posição (i, j) das matrizes.
    for i in range(rows):          # Para cada linha i...
        for j in range(cols):      # Para cada coluna j...
            # Soma os elementos A[i][j] e B[i][j] e armazena em result[i][j].
            result[i][j] = matrix_a[i][j] + matrix_b[i][j]

    # 5. Retorno do resultado:
    #    Devolve a matriz 'result' contendo a soma.
    return result