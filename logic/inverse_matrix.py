# calculadora_matrizes/logic/inverse_matrix.py
from .validation_utils import validate_square_matrix
from .determinant import determinant
from .helper_utils import adjoint_matrix # adjoint_matrix lida com cofatores e transposição

def inverse_matrix(matrix):
    validate_square_matrix(matrix, "Matriz para inversão")

    det_a = determinant(matrix)
    if det_a == 0: # Usar uma pequena tolerância para comparação com zero se usar floats? Não, para exatidão.
        raise ValueError("A matriz não é invertível (determinante é zero).")

    adj_a = adjoint_matrix(matrix) # Esta função já usa transpose_matrix e matrix_of_cofactors
    
    rows = len(adj_a)
    cols = len(adj_a[0]) # Deve ser igual a rows
    inv_matrix = [[0 for _ in range(cols)] for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):
            # Garante divisão de ponto flutuante
            inv_matrix[r][c] = adj_a[r][c] / det_a 
    return inv_matrix