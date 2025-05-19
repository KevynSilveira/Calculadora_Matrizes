# calculadora_matrizes/logic/solve_linear_system.py

# Importa as funções necessárias:
# - validate_linear_system_inputs: Para validar as dimensões e propriedades de A e B.
# - inverse_matrix: Para calcular a inversa da matriz A.
# - multiply_matrices: Para multiplicar A_inversa por B.
from .validation_utils import validate_linear_system_inputs
from .inverse_matrix import inverse_matrix
from .multiply_matrices import multiply_matrices

def solve_linear_system_inverse(matrix_a, vector_b):
    """
    Resolve um sistema de equações lineares da forma AX = B,
    utilizando o método da matriz inversa: X = A⁻¹ * B.

    Args:
        matrix_a (list[list[float]]): A matriz quadrada dos coeficientes (A).
        vector_b (list[list[float]]): O vetor coluna (matriz Nx1) dos termos 
                                      independentes (B).

    Returns:
        list[list[float]]: O vetor coluna (matriz Nx1) da solução (X).

    Raises:
        ValueError: Se as entradas não forem válidas (ex: A não quadrada, dimensões
                    incompatíveis, A singular), ou se ocorrer um erro durante o
                    cálculo da inversa.
    """
    # 1. Validação das Entradas do Sistema:
    #    Verifica se 'matrix_a' é quadrada, se 'vector_b' é um vetor coluna,
    #    e se as dimensões são compatíveis para um sistema AX=B.
    #    Levanta ValueError se a validação falhar.
    validate_linear_system_inputs(matrix_a, vector_b)

    # 2. Cálculo da Matriz Inversa de A (A⁻¹):
    #    Tenta calcular a inversa de 'matrix_a'.
    try:
        inv_a = inverse_matrix(matrix_a)
    except ValueError as e: 
        # Se 'inverse_matrix' levantar um ValueError (ex: matriz singular, det(A)=0),
        # a exceção é capturada e relançada com uma mensagem mais contextualizada
        # para a resolução do sistema.
        raise ValueError(f"Não é possível resolver o sistema: {e}")

    # 3. Cálculo da Solução (X = A⁻¹ * B):
    #    Multiplica a matriz inversa de A (inv_a) pelo vetor B (vector_b).
    #    O resultado desta multiplicação é o vetor solução X.
    #    A função 'multiply_matrices' lida com a multiplicação de uma matriz NxN (inv_a)
    #    por uma matriz Nx1 (vector_b), resultando em uma matriz Nx1 (solution_x).
    solution_x = multiply_matrices(inv_a, vector_b)

    # 4. Retorno da Solução:
    #    Devolve o vetor coluna 'solution_x'.
    return solution_x