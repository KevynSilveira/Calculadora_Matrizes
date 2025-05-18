# calculadora_matrizes/logic/scalar_multiply.py
from .validation_utils import validate_matrix_input

def scalar_multiply(matrix, scalar):
    validate_matrix_input(matrix, "Matriz para multiplicação por escalar")
    # A validação validate_matrix_input garante que matrix[0] existe se a matriz for válida
    rows = len(matrix)
    cols = len(matrix[0])
    result = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            result[i][j] = matrix[i][j] * scalar
    return result