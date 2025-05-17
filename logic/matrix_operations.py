# logic/matrix_operations.py

def print_matrix(matrix, name="Matrix"): # Função auxiliar para testes
    print(f"{name}:")
    if not matrix or not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
        print("  [Matriz Inválida ou Vazia]")
        return
    for row in matrix:
        print(f"  {row}")
    print("-" * 20)

def validate_matrices_for_add_sub(matrix_a, matrix_b):
    if not matrix_a or not isinstance(matrix_a, list) or not all(isinstance(row, list) for row in matrix_a) or \
       not matrix_b or not isinstance(matrix_b, list) or not all(isinstance(row, list) for row in matrix_b):
        raise ValueError("Ambas as matrizes devem ser fornecidas e válidas.")
    if not matrix_a[0] or not matrix_b[0]: # Checa se as linhas internas não estão vazias
        raise ValueError("Matrizes não podem ter linhas vazias.")
    if len(matrix_a) != len(matrix_b) or len(matrix_a[0]) != len(matrix_b[0]):
        raise ValueError("Matrizes devem ter as mesmas dimensões para adição/subtração.")
    return True

def validate_matrix_for_mult(matrix_a, matrix_b):
    if not matrix_a or not isinstance(matrix_a, list) or not all(isinstance(row, list) for row in matrix_a) or \
       not matrix_b or not isinstance(matrix_b, list) or not all(isinstance(row, list) for row in matrix_b):
        raise ValueError("Ambas as matrizes devem ser fornecidas e válidas.")
    if not matrix_a[0] or not matrix_b[0]: # Checa se as linhas internas não estão vazias
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
    cols_a = len(matrix_a[0]) # = rows_b
    cols_b = len(matrix_b[0])
    result = [[0 for _ in range(cols_b)] for _ in range(rows_a)]
    for i in range(rows_a):
        for j in range(cols_b):
            sum_val = 0
            for k in range(cols_a): # ou len(matrix_b)
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
    result = [[0 for _ in range(rows)] for _ in range(cols)] # Dimensões invertidas
    for i in range(rows):
        for j in range(cols):
            result[j][i] = matrix[i][j]
    return result

def get_minor(matrix, r, c):
    return [row[:c] + row[c+1:] for row in (matrix[:r] + matrix[r+1:])]

def determinant(matrix):
    if not matrix or not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
        raise ValueError("Matriz fornecida é inválida.")
    if not matrix[0]:
        raise ValueError("Matriz não pode ter linhas vazias.")

    rows = len(matrix)
    if rows != len(matrix[0]):
        raise ValueError("Matriz deve ser quadrada para calcular o determinante.")

    if rows == 1:
        return matrix[0][0]
    if rows == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    det = 0
    for c_col in range(rows): # Expansão pela primeira linha (índice 0)
        minor = get_minor(matrix, 0, c_col)
        # O cofator é (-1)**(linha + coluna) * M_ij. Como estamos na linha 0, fica (-1)**(0 + c_col)
        det += ((-1)**c_col) * matrix[0][c_col] * determinant(minor)
    return det

# # Testes (pode remover ou comentar depois)
# if __name__ == '__main__':
#     mat_a = [[1, 2, 3], [4, 5, 6]]
#     mat_b = [[7, 8], [9, 10], [11, 12]]
#     mat_c = [[1, 2], [3, 4]]
#     mat_d = [[5, 6], [7, 8]]
#     scalar_val = 2

#     print_matrix(mat_a, "Matriz A")
#     print_matrix(mat_b, "Matriz B")
#     print_matrix(mat_c, "Matriz C")
#     print_matrix(mat_d, "Matriz D")

#     try:
#         print_matrix(add_matrices(mat_c, mat_d), "C + D")
#         print_matrix(subtract_matrices(mat_d, mat_c), "D - C")
#         print_matrix(multiply_matrices(mat_a, mat_b), "A * B")
#         print_matrix(scalar_multiply(mat_c, scalar_val), "C * Escalar")
#         print_matrix(transpose_matrix(mat_a), "Transposta de A")
#         print_matrix(transpose_matrix(mat_b), "Transposta de B")

#         mat_sq = [[1, 2, 3], [0, 1, 4], [5, 6, 0]]
#         print_matrix(mat_sq, "Matriz Quadrada")
#         print(f"Determinante de Matriz Quadrada: {determinant(mat_sq)}")

#         mat_sq_2 = [[4, 2], [3, 5]]
#         print_matrix(mat_sq_2, "Matriz Quadrada 2x2")
#         print(f"Determinante de Matriz Quadrada 2x2: {determinant(mat_sq_2)}")
#     except ValueError as e:
#         print(f"Erro: {e}")