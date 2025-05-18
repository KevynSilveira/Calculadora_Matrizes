# calculadora_matrizes/logic/multiply_matrices.py
from .validation_utils import validate_matrix_for_mult

def multiply_matrices(matrix_a, matrix_b):
    validate_matrix_for_mult(matrix_a, matrix_b)
    rows_a = len(matrix_a)
    cols_a = len(matrix_a[0])
    # rows_b = len(matrix_b) #  == cols_a
    cols_b = len(matrix_b[0])
    result = [[0 for _ in range(cols_b)] for _ in range(rows_a)]
    for i in range(rows_a):
        for j in range(cols_b):
            sum_val = 0
            for k in range(cols_a): # ou range(rows_b)
                sum_val += matrix_a[i][k] * matrix_b[k][j]
            result[i][j] = sum_val
    return result