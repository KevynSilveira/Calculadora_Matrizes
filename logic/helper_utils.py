# calculadora_matrizes/logic/helper_utils.py

def print_matrix(matrix, name="Matrix"): # Função auxiliar para testes
    print(f"{name}:")
    if not matrix or not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
        print("  [Matriz Inválida ou Vazia]")
        return
    if matrix and not matrix[0] and len(matrix) > 0 : # Se a primeira linha é vazia, mas a matriz não
        print("  [Matriz com Linha(s) Vazia(s)]")
        return
    for row in matrix:
        print(f"  {row}")
    print("-" * 20)

def get_minor(matrix, r, c):
    """Retorna a submatriz removendo a linha r e coluna c."""
    return [row[:c] + row[c+1:] for row in (matrix[:r] + matrix[r+1:])]

# Funções que dependem de outras operações serão importadas localmente dentro das funções
# para evitar problemas de importação circular no nível do módulo.

def get_cofactor(matrix, r_idx, c_idx):
    """Calcula o cofator de um elemento matrix[r_idx][c_idx]."""
    from .determinant import determinant # Importação local
    minor_matrix = get_minor(matrix, r_idx, c_idx)
    # O determinante de uma matriz vazia (resultado de get_minor em matriz 1x1) pode ser problemático.
    # A função determinant deve lidar com matriz 0x0 (get_minor de 1x1) ou 1x1.
    # Se minor_matrix for [], determinant([[]]) ou determinant([]) precisa ser tratado.
    # determinant([]) não faz sentido. determinant([[]]) também não.
    # determinant([[x]]) é x.
    # Se a matriz original for 1x1, get_minor(matrix,0,0) será [].
    # O cálculo do cofator/determinante não deve chegar a chamar determinant([])
    # pois a recursão para em matriz 2x2 ou 1x1.
    cofactor_value = ((-1)**(r_idx + c_idx)) * determinant(minor_matrix)
    return cofactor_value

def matrix_of_cofactors(matrix):
    """Cria a matriz dos cofatores para a dada matriz."""
    # A validação de ser quadrada é feita pela função que chama esta (ex: inverse_matrix)
    rows = len(matrix)
    cols = len(matrix[0]) # Assume que é quadrada (cols == rows)
    cofactor_matrix = [[0 for _ in range(cols)] for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):
            cofactor_matrix[r][c] = get_cofactor(matrix, r, c)
    return cofactor_matrix

def adjoint_matrix(matrix):
    """Calcula a matriz adjunta (transposta da matriz dos cofatores)."""
    from .transpose_matrix import transpose_matrix # Importação local
    cofactor_m = matrix_of_cofactors(matrix)
    adj_matrix = transpose_matrix(cofactor_m)
    return adj_matrix