# calculadora_matrizes/logic/determinant.py
from .validation_utils import validate_square_matrix
from .helper_utils import get_minor 

def determinant(matrix):
    """
    Calcula o determinante de uma matriz quadrada usando expansão de cofatores.
    """
    # CASO ESPECIAL: Matriz 0x0 (resultante do menor de uma matriz 1x1)
    # O determinante da matriz 0x0 é 1 por convenção.
    # Esta verificação deve ser específica para a lista vazia.
    if matrix == []: # Especificamente para lista vazia
        return 1

    # Validação de estrutura e se é quadrada para matrizes não-vazias (ou não-[]).
    # A validação pegará None, string, etc., e levantará ValueError.
    validate_square_matrix(matrix, "Matriz para determinante") 
    
    # Se passou na validação, 'matrix' é uma lista de listas e matrix[0] existe (a menos que rows seja 0,
    # mas validate_square_matrix -> validate_matrix_input -> _is_valid_matrix_structure impede matrix vazia)
    rows = len(matrix) 

    # Caso base para a recursão ou matrizes muito pequenas
    if rows == 1: # matrix é [[a]]
        return matrix[0][0]
    
    if rows == 2: # matrix é [[a,b],[c,d]]
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    det = 0
    # Expansão de cofatores ao longo da primeira linha (linha 0)
    for c_col in range(rows): 
        minor_matrix = get_minor(matrix, 0, c_col) # get_minor pode retornar []
        sign = (-1)**c_col 
        det += sign * matrix[0][c_col] * determinant(minor_matrix) # Chamada recursiva
        
    return det