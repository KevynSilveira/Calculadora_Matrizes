# calculadora_matrizes/logic/add_matrices.py
from .validation_utils import validate_matrices_for_add_sub

def add_matrices(matrix_a, matrix_b):
    validate_matrices_for_add_sub(matrix_a, matrix_b)
    rows = len(matrix_a)
    cols = len(matrix_a[0])
    result = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            result[i][j] = matrix_a[i][j] + matrix_b[i][j]
    return result