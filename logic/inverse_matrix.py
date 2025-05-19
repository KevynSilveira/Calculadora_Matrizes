# calculadora_matrizes/logic/inverse_matrix.py

# Importa as funções necessárias de outros módulos dentro do pacote 'logic'.
# - validate_square_matrix: Garante que a matriz de entrada é quadrada.
# - determinant: Calcula o determinante da matriz.
# - adjoint_matrix: Calcula a matriz adjunta (transposta da matriz de cofatores).
from .validation_utils import validate_square_matrix
from .determinant import determinant
from .helper_utils import adjoint_matrix 

def inverse_matrix(matrix):
    """
    Calcula a matriz inversa de uma dada 'matrix' quadrada.
    A fórmula utilizada é: A⁻¹ = (1 / det(A)) * adj(A)
    onde det(A) é o determinante de A e adj(A) é a matriz adjunta de A.

    Args:
        matrix (list[list[float]]): A matriz quadrada para a qual a inversa será calculada.

    Returns:
        list[list[float]]: A matriz inversa.

    Raises:
        ValueError: Se a matriz não for quadrada ou se for singular (determinante igual a zero),
                    o que significa que a inversa não existe.
    """
    # 1. Validação da Matriz de Entrada:
    #    Verifica se a 'matrix' fornecida é quadrada. Se não for,
    #    'validate_square_matrix' levantará um ValueError.
    #    O nome "Matriz para inversão" é usado para clareza nas mensagens de erro.
    validate_square_matrix(matrix, "Matriz para inversão")

    # 2. Cálculo do Determinante:
    #    Calcula o determinante (det_a) da matriz. O determinante é essencial
    #    para encontrar a inversa e para verificar se a matriz é invertível.
    det_a = determinant(matrix)

    # 3. Verificação de Singularidade:
    #    Se o determinante for zero, a matriz é singular e não possui inversa.
    #    Nesse caso, uma exceção ValueError é levantada.
    #    A comparação com zero deve ser exata para matemática com inteiros/racionais.
    #    Para floats, uma pequena tolerância poderia ser considerada, mas aqui seguimos a exatidão.
    if det_a == 0:
        raise ValueError("A matriz não é invertível (determinante é zero).")

    # 4. Cálculo da Matriz Adjunta:
    #    Calcula a matriz adjunta (adj_a) da 'matrix'. A matriz adjunta é a
    #    transposta da matriz dos cofatores da 'matrix'.
    adj_a = adjoint_matrix(matrix)
    
    # 5. Obtenção das Dimensões da Matriz Adjunta:
    #    A matriz adjunta terá as mesmas dimensões da matriz original (já que é quadrada).
    #    Estas dimensões são usadas para criar a matriz inversa.
    rows = len(adj_a)
    cols = len(adj_a[0]) # Para uma matriz quadrada, rows == cols.

    # 6. Inicialização da Matriz Inversa:
    #    Cria uma nova matriz (inv_matrix) preenchida com zeros,
    #    com as mesmas dimensões da matriz adjunta (e da original).
    inv_matrix = [[0 for _ in range(cols)] for _ in range(rows)]

    # 7. Cálculo dos Elementos da Matriz Inversa:
    #    Itera sobre cada elemento (r, c) da matriz adjunta.
    for r in range(rows):      # Para cada linha r...
        for c in range(cols):  # Para cada coluna c...
            # Cada elemento da matriz inversa é o elemento correspondente
            # da matriz adjunta dividido pelo determinante da matriz original.
            # A⁻¹[r][c] = adj(A)[r][c] / det(A)
            # A divisão aqui resultará em floats se det_a ou adj_a[r][c] forem floats,
            # ou se a divisão não for exata.
            inv_matrix[r][c] = adj_a[r][c] / det_a 
            
    # 8. Retorno da Matriz Inversa:
    #    A matriz 'inv_matrix', agora contendo a inversa da matriz original, é retornada.
    return inv_matrix