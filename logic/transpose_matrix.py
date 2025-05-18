# calculadora_matrizes/logic/transpose_matrix.py
from .validation_utils import validate_matrix_input

def transpose_matrix(matrix):
    validate_matrix_input(matrix, "Matriz para transposição")
    rows = len(matrix)
    cols = len(matrix[0])
    result = [[0 for _ in range(rows)] for _ in range(cols)] # Dimensões invertidas
    for i in range(rows):
        for j in range(cols):
            result[j][i] = matrix[i][j]
    return result