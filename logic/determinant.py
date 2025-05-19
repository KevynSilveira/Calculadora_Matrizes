# calculadora_matrizes/logic/determinant.py
from .validation_utils import validate_square_matrix
from .helper_utils import get_minor 

def determinant(matrix):
    """
    Calcula o determinante de uma matriz quadrada.
    Utiliza o método de expansão de cofatores recursivamente.
    Pré-condição: A matriz de entrada deve ser quadrada (validada internamente).
    Retorna: O valor do determinante (um número).
    """
    # 1. Caso Base da Recursão (para menores de matrizes 1x1):
    #    O determinante da "matriz 0x0" (representada por uma lista vazia [])
    #    é definido como 1. Isso é crucial para o cálculo correto dos cofatores.
    if matrix == []: 
        return 1

    # 2. Validação da Matriz de Entrada:
    #    Verifica se a 'matrix' é realmente quadrada e uma estrutura válida.
    #    A função 'validate_square_matrix' lança um ValueError se não for.
    #    O nome "Matriz para determinante" é passado para mensagens de erro mais claras.
    validate_square_matrix(matrix, "Matriz para determinante") 
    
    # 3. Obtenção do Tamanho da Matriz:
    #    'rows' armazena o número de linhas (que é igual ao número de colunas).
    rows = len(matrix) 

    # 4. Casos Base para Matrizes Pequenas (Otimização e Fim da Recursão):
    #    a) Matriz 1x1: O determinante é o próprio elemento.
    #       Ex: det([[a]]) = a
    if rows == 1:
        return matrix[0][0]
    
    #    b) Matriz 2x2: O determinante é calculado pela fórmula ad - bc.
    #       Ex: det([[a,b],[c,d]]) = a*d - b*c
    if rows == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    # 5. Cálculo do Determinante por Expansão de Cofatores (para matrizes > 2x2):
    #    Inicializa o valor do determinante.
    det = 0

    #    Itera sobre os elementos da primeira linha da matriz (poderia ser qualquer linha ou coluna).
    #    'c_col' é o índice da coluna do elemento atual na primeira linha.
    for c_col in range(rows): 
        #    a) Obtenção do Menor:
        #       'minor_matrix' é a submatriz obtida removendo a primeira linha (linha 0)
        #       e a coluna 'c_col' da matriz original.
        minor_matrix = get_minor(matrix, 0, c_col)
        
        #    b) Cálculo do Sinal do Cofator:
        #       O sinal alterna: + - + - ... e é dado por (-1)^(linha_idx + coluna_idx).
        #       Como estamos na linha 0 (índice 0), o sinal é (-1)^(0 + c_col) = (-1)^c_col.
        sign = (-1)**c_col 
        
        #    c) Acumulação do Termo da Expansão:
        #       O determinante é a soma dos produtos:
        #       sinal * elemento_da_primeira_linha * determinante_do_menor_correspondente.
        #       A chamada 'determinant(minor_matrix)' é a chamada recursiva.
        det += sign * matrix[0][c_col] * determinant(minor_matrix)
        
    # 6. Retorno do Determinante Calculado:
    return det