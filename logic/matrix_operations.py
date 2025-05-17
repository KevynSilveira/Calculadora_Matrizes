def print_matrix(matrix, name="Matrix"): # Função auxiliar para testes
    print(f"{name}:")
    if not matrix or not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
        print("  [Matriz Inválida ou Vazia]")
        return
    if not matrix[0] and len(matrix) > 0 : # Se a primeira linha é vazia, mas a matriz não
        print("  [Matriz com Linha(s) Vazia(s)]")
        return
    for row in matrix:
        print(f"  {row}")
    print("-" * 20)

def validate_matrices_for_add_sub(matrix_a, matrix_b):
    if not matrix_a or not isinstance(matrix_a, list) or not all(isinstance(row, list) for row in matrix_a) or \
       not matrix_b or not isinstance(matrix_b, list) or not all(isinstance(row, list) for row in matrix_b):
        raise ValueError("Ambas as matrizes devem ser fornecidas e válidas.")
    if not matrix_a[0] or not matrix_b[0]:
        raise ValueError("Matrizes não podem ter linhas vazias.")
    if len(matrix_a) != len(matrix_b) or len(matrix_a[0]) != len(matrix_b[0]):
        raise ValueError("Matrizes devem ter as mesmas dimensões para adição/subtração.")
    return True

def validate_matrix_for_mult(matrix_a, matrix_b):
    if not matrix_a or not isinstance(matrix_a, list) or not all(isinstance(row, list) for row in matrix_a) or \
       not matrix_b or not isinstance(matrix_b, list) or not all(isinstance(row, list) for row in matrix_b):
        raise ValueError("Ambas as matrizes devem ser fornecidas e válidas.")
    if not matrix_a[0] or not matrix_b[0]:
        raise ValueError("Matrizes não podem ter linhas vazias.")
    if len(matrix_a[0]) != len(matrix_b):
        raise ValueError("Número de colunas da Matriz A deve ser igual ao número de linhas da Matriz B para multiplicação.")
    return True

def add_matrices(matrix_a, matrix_b):
    validate_matrices_for_add_sub(matrix_a, matrix_b)
    rows = len(matrix_a)
    cols = len(matrix_a[0])
    result = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            result[i][j] = matrix_a[i][j] + matrix_b[i][j]
    return result

def subtract_matrices(matrix_a, matrix_b):
    validate_matrices_for_add_sub(matrix_a, matrix_b)
    rows = len(matrix_a)
    cols = len(matrix_a[0])
    result = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            result[i][j] = matrix_a[i][j] - matrix_b[i][j]
    return result

def multiply_matrices(matrix_a, matrix_b):
    validate_matrix_for_mult(matrix_a, matrix_b)
    rows_a = len(matrix_a)
    cols_a = len(matrix_a[0])
    cols_b = len(matrix_b[0])
    result = [[0 for _ in range(cols_b)] for _ in range(rows_a)]
    for i in range(rows_a):
        for j in range(cols_b):
            sum_val = 0
            for k in range(cols_a):
                sum_val += matrix_a[i][k] * matrix_b[k][j]
            result[i][j] = sum_val
    return result

def scalar_multiply(matrix, scalar):
    if not matrix or not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
        raise ValueError("Matriz fornecida é inválida.")
    if not matrix[0]:
        raise ValueError("Matriz não pode ter linhas vazias.")
    rows = len(matrix)
    cols = len(matrix[0])
    result = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            result[i][j] = matrix[i][j] * scalar
    return result

def transpose_matrix(matrix):
    if not matrix or not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
        raise ValueError("Matriz fornecida é inválida.")
    if not matrix[0]:
        raise ValueError("Matriz não pode ter linhas vazias.")
    rows = len(matrix)
    cols = len(matrix[0])
    result = [[0 for _ in range(rows)] for _ in range(cols)]
    for i in range(rows):
        for j in range(cols):
            result[j][i] = matrix[i][j]
    return result

def get_minor(matrix, r, c):
    """Retorna a submatriz removendo a linha r e coluna c."""
    return [row[:c] + row[c+1:] for row in (matrix[:r] + matrix[r+1:])]

def determinant(matrix):
    if not matrix or not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
        raise ValueError("Matriz fornecida é inválida.")
    if not matrix[0]: # Verifica se a primeira linha (e portanto todas, se for matriz válida) está vazia
        raise ValueError("Matriz não pode ter linhas vazias.")
    rows = len(matrix)
    if rows != len(matrix[0]):
        raise ValueError("Matriz deve ser quadrada para calcular o determinante.")

    if rows == 1:
        return matrix[0][0]
    if rows == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    det = 0
    for c_col in range(rows):
        minor_matrix = get_minor(matrix, 0, c_col)
        det += ((-1)**c_col) * matrix[0][c_col] * determinant(minor_matrix)
    return det

def get_cofactor(matrix, r_idx, c_idx):
    """Calcula o cofator de um elemento matrix[r_idx][c_idx]."""
    minor = get_minor(matrix, r_idx, c_idx)
    cofactor_value = ((-1)**(r_idx + c_idx)) * determinant(minor) # r_idx e c_idx são 0-indexed
    return cofactor_value

def matrix_of_cofactors(matrix):
    """Cria a matriz dos cofatores para a dada matriz."""
    if not matrix or not matrix[0] or len(matrix) != len(matrix[0]):
        raise ValueError("A matriz deve ser quadrada para calcular a matriz de cofatores.")
    
    rows = len(matrix)
    cols = len(matrix[0]) # == rows
    cofactor_matrix = [[0 for _ in range(cols)] for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):
            cofactor_matrix[r][c] = get_cofactor(matrix, r, c)
    return cofactor_matrix

def adjoint_matrix(matrix):
    """Calcula a matriz adjunta (transposta da matriz dos cofatores)."""
    cofactor_m = matrix_of_cofactors(matrix)
    adj_matrix = transpose_matrix(cofactor_m)
    return adj_matrix

def inverse_matrix(matrix):
    """Calcula a matriz inversa A^-1 = (1/det(A)) * adj(A)."""
    if not matrix or not matrix[0] or len(matrix) != len(matrix[0]):
        raise ValueError("A matriz deve ser quadrada para calcular a inversa.")

    det_a = determinant(matrix)
    if det_a == 0:
        raise ValueError("A matriz não é invertível (determinante é zero).")

    adj_a = adjoint_matrix(matrix)
    
    rows = len(adj_a)
    cols = len(adj_a[0])
    inv_matrix = [[0 for _ in range(cols)] for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):
            inv_matrix[r][c] = adj_a[r][c] / det_a
    return inv_matrix

def solve_linear_system_inverse(matrix_a, vector_b):
    """Resolve o sistema linear AX = B usando X = A_inversa * B.
       matrix_a: Matriz quadrada dos coeficientes.
       vector_b: Vetor coluna (matriz Nx1) dos termos independentes.
    """
    if not matrix_a or not matrix_a[0]:
        raise ValueError("Matriz A (coeficientes) não pode ser vazia.")
    if not vector_b or not vector_b[0]:
        raise ValueError("Vetor B (termos independentes) não pode ser vazio.")

    if len(matrix_a) != len(matrix_a[0]):
        raise ValueError("Matriz A (coeficientes) deve ser quadrada para este método.")
    if len(matrix_a) != len(vector_b):
        raise ValueError("Número de linhas da Matriz A deve ser igual ao número de linhas do Vetor B.")
    if len(vector_b[0]) != 1:
        raise ValueError("Vetor B (termos independentes) deve ser um vetor coluna (Nx1).")

    try:
        inv_a = inverse_matrix(matrix_a)
    except ValueError as e: 
        raise ValueError(f"Não é possível resolver o sistema: {e}")

    solution_x = multiply_matrices(inv_a, vector_b)
    return solution_x