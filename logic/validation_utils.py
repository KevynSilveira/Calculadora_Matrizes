# calculadora_matrizes/logic/validation_utils.py

def _is_valid_matrix_structure(matrix, matrix_name="Matriz"):
    if not matrix or not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
        raise ValueError(f"{matrix_name} deve ser uma lista de listas e não pode ser vazia.")
    if not matrix[0] and len(matrix) > 0: # Primeira linha vazia, mas matriz não é vazia (lista de listas vazias)
         raise ValueError(f"{matrix_name} contém linha(s) vazia(s) ou não foi inicializada corretamente.")
    return True

def _has_consistent_column_count(matrix, matrix_name="Matriz"):
    if not matrix or not matrix[0]: # Já coberto por _is_valid_matrix_structure se matrix[0] for o problema
        return True # Ou levanta erro se for [[], []] -> _is_valid_matrix_structure pega isso
    
    first_row_len = len(matrix[0])
    if not all(len(row) == first_row_len for row in matrix):
        raise ValueError(f"Todas as linhas da {matrix_name} devem ter o mesmo número de colunas.")
    return True

def validate_matrix_input(matrix, matrix_name="Matriz"):
    _is_valid_matrix_structure(matrix, matrix_name)
    _has_consistent_column_count(matrix, matrix_name)
    # Checagem adicional para garantir que nenhuma linha seja None ou algo diferente de lista
    # if not all(isinstance(row, list) for row in matrix): # Já coberto em _is_valid_matrix_structure
    #     raise ValueError(f"{matrix_name} contém elementos que não são linhas (listas).")
    return True


def validate_matrices_for_add_sub(matrix_a, matrix_b):
    validate_matrix_input(matrix_a, "Matriz A")
    validate_matrix_input(matrix_b, "Matriz B")
    if len(matrix_a) != len(matrix_b) or len(matrix_a[0]) != len(matrix_b[0]):
        raise ValueError("Matrizes devem ter as mesmas dimensões para adição/subtração.")
    return True

def validate_matrix_for_mult(matrix_a, matrix_b):
    validate_matrix_input(matrix_a, "Matriz A")
    validate_matrix_input(matrix_b, "Matriz B")
    if len(matrix_a[0]) != len(matrix_b):
        raise ValueError("Número de colunas da Matriz A deve ser igual ao número de linhas da Matriz B para multiplicação.")
    return True

def validate_square_matrix(matrix, matrix_name="Matriz"):
    validate_matrix_input(matrix, matrix_name)
    if not matrix[0]: # Se for uma matriz como [[]], len(matrix) é 1 mas len(matrix[0]) é 0
        raise ValueError(f"{matrix_name} é inválida (linha vazia) e não pode ser verificada como quadrada.")
    if len(matrix) != len(matrix[0]):
        raise ValueError(f"{matrix_name} deve ser quadrada.")
    return True

def validate_linear_system_inputs(matrix_a, vector_b):
    validate_square_matrix(matrix_a, "Matriz A (coeficientes)")
    validate_matrix_input(vector_b, "Vetor B (termos independentes)")

    if len(matrix_a) != len(vector_b):
        raise ValueError("Número de linhas da Matriz A (coeficientes) deve ser igual ao número de linhas do Vetor B.")
    if len(vector_b[0]) != 1:
        raise ValueError("Vetor B (termos independentes) deve ser um vetor coluna (ter uma única coluna).")
    return True