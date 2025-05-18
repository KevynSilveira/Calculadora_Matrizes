# calculadora_matrizes/logic/solve_linear_system.py
from .validation_utils import validate_linear_system_inputs
from .inverse_matrix import inverse_matrix
from .multiply_matrices import multiply_matrices

def solve_linear_system_inverse(matrix_a, vector_b):
    """Resolve o sistema linear AX = B usando X = A_inversa * B.
       matrix_a: Matriz quadrada dos coeficientes.
       vector_b: Vetor coluna (matriz Nx1) dos termos independentes.
    """
    validate_linear_system_inputs(matrix_a, vector_b)
    # Validações específicas das dimensões já estão em validate_linear_system_inputs

    try:
        inv_a = inverse_matrix(matrix_a)
    except ValueError as e: 
        # Re-lança o erro, o contexto já é bom de inverse_matrix e determinant
        raise ValueError(f"Não é possível resolver o sistema: {e}")

    # vector_b é uma matriz Nx1, multiply_matrices deve lidar com isso.
    solution_x = multiply_matrices(inv_a, vector_b)
    return solution_x