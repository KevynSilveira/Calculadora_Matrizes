# calculadora_matrizes/logic/determinant.py
from .validation_utils import validate_square_matrix
from .helper_utils import get_minor # get_minor é uma dependência limpa

def determinant(matrix):
    # Validação de estrutura e se é quadrada
    validate_square_matrix(matrix, "Matriz para determinante")
    
    rows = len(matrix)

    if rows == 0: # Ex: get_minor de matriz 1x1 resulta em []
        # Este caso não deveria ser alcançado em um fluxo normal de cálculo de determinante
        # de matrizes NxN (N>=1). Mas se get_minor pode retornar [], é bom ter um valor.
        # Para uma "matriz vazia", o determinante é por vezes definido como 1 (produto vazio).
        # No entanto, no contexto de cofatores, get_minor de 1x1 para det(M_1x1) = M[0][0] * det([])
        # Isso é para o cofator de uma matriz 1x1, que é 1.
        # Para M = [[a]], det(M)=a. Cofator de 'a' é (-1)^0 * det(submatriz vazia).
        # Se o cofator de 'a' deve ser 1, então det(submatriz vazia) = 1.
        # No entanto, get_minor não deve ser chamada para matrizes 1x1 pela lógica de expansão.
        return 1 # Definição para o determinante da "matriz 0x0"

    if rows == 1:
        return matrix[0][0]
    if rows == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    det = 0
    # Expansão de cofatores ao longo da primeira linha
    for c_col in range(rows):
        minor_matrix = get_minor(matrix, 0, c_col)
        # O sinal do cofator é (-1)**(linha + coluna), aqui linha é 0 (0-indexed)
        det += ((-1)**c_col) * matrix[0][c_col] * determinant(minor_matrix) # Chamada recursiva
    return det