# calculadora_matrizes/logic/scalar_multiply.py

# Importa a função de validação genérica para uma única matriz.
# Esta função garante que a 'matrix' de entrada é uma estrutura de lista de listas válida.
from .validation_utils import validate_matrix_input

def scalar_multiply(matrix, scalar):
    """
    Multiplica cada elemento de uma 'matrix' por um valor 'scalar'.

    Args:
        matrix (list[list[float]]): A matriz cujos elementos serão multiplicados.
        scalar (float or int): O valor escalar pelo qual multiplicar cada elemento.

    Returns:
        list[list[float]]: Uma nova matriz resultante da multiplicação escalar.

    Raises:
        ValueError: Se a 'matrix' de entrada não for uma estrutura válida
                    (essa exceção é levantada por validate_matrix_input).
        TypeError: Se 'scalar' não for um tipo numérico compatível com multiplicação
                   (esta exceção seria levantada nativamente pelo Python durante a operação).
    """
    # 1. Validação da Matriz de Entrada:
    #    Verifica se 'matrix' é uma lista de listas bem formada e não vazia.
    #    Se a validação falhar, 'validate_matrix_input' levantará um ValueError.
    #    O nome "Matriz para multiplicação por escalar" é para mensagens de erro claras.
    validate_matrix_input(matrix, "Matriz para multiplicação por escalar")

    # 2. Obtenção das Dimensões da Matriz:
    #    A matriz resultante terá as mesmas dimensões da matriz original.
    rows = len(matrix)      # Número de linhas.
    cols = len(matrix[0])   # Número de colunas (a validação garante que matrix[0] existe).

    # 3. Inicialização da Matriz de Resultado:
    #    Cria uma nova matriz 'result' preenchida com zeros,
    #    com as mesmas dimensões da matriz de entrada.
    result = [[0 for _ in range(cols)] for _ in range(rows)]

    # 4. Processo de Multiplicação Escalar:
    #    Itera sobre cada elemento (i, j) da matriz de entrada.
    for i in range(rows):          # Para cada linha i...
        for j in range(cols):      # Para cada coluna j...
            # Multiplica o elemento matrix[i][j] pelo 'scalar'
            # e armazena o resultado na posição correspondente da matriz 'result'.
            # Ex: result[0][0] = matrix[0][0] * scalar
            result[i][j] = matrix[i][j] * scalar

    # 5. Retorno da Matriz Resultante:
    #    A matriz 'result', agora contendo cada elemento da 'matrix' original
    #    multiplicado pelo 'scalar', é retornada.
    return result