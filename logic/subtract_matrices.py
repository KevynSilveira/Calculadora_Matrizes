# calculadora_matrizes/logic/subtract_matrices.py

# Importa a função de validação específica para operações de adição e subtração de matrizes.
# Esta função garante que ambas as matrizes são válidas e têm dimensões compatíveis.
from .validation_utils import validate_matrices_for_add_sub

def subtract_matrices(matrix_a, matrix_b):
    """
    Subtrai a matriz B da matriz A (A - B), elemento a elemento.

    Args:
        matrix_a (list[list[float]]): A primeira matriz (minuendo).
        matrix_b (list[list[float]]): A segunda matriz (subtraendo).

    Returns:
        list[list[float]]: A matriz resultante da subtração.

    Raises:
        ValueError: Se as matrizes não forem válidas ou não tiverem dimensões compatíveis
                    para a subtração (essa exceção é levantada por validate_matrices_for_add_sub).
    """
    # 1. Validação das Matrizes de Entrada:
    #    Assegura que A e B são matrizes válidas e possuem dimensões idênticas,
    #    uma condição necessária para a subtração elemento a elemento.
    #    Se a validação falhar, uma exceção ValueError é interrompe a função.
    validate_matrices_for_add_sub(matrix_a, matrix_b)

    # 2. Obtenção das Dimensões:
    #    As dimensões da matriz resultado serão as mesmas das matrizes de entrada (A e B),
    #    pois a validação já confirmou que são iguais.
    rows = len(matrix_a)      # Número de linhas.
    cols = len(matrix_a[0])   # Número de colunas.

    # 3. Criação da Matriz Resultado:
    #    Inicializa uma nova matriz (result) com zeros, do mesmo tamanho de A e B.
    #    Esta matriz armazenará a diferença.
    #    Ex: Para A e B 2x2, result = [[0, 0], [0, 0]].
    result = [[0 for _ in range(cols)] for _ in range(rows)]

    # 4. Processo de Subtração:
    #    Itera sobre cada posição (i, j) das matrizes.
    for i in range(rows):          # Para cada linha i...
        for j in range(cols):      # Para cada coluna j...
            # Subtrai o elemento B[i][j] do elemento A[i][j]
            # e armazena a diferença em result[i][j].
            # Ex: result[0][0] = matrix_a[0][0] - matrix_b[0][0]
            result[i][j] = matrix_a[i][j] - matrix_b[i][j]

    # 5. Retorno do Resultado:
    #    Devolve a matriz 'result' contendo a diferença A - B.
    return result