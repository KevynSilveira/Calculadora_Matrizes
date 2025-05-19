# calculadora_matrizes/logic/multiply_matrices.py

# Importa a função de validação específica para a multiplicação de matrizes.
# Esta função verifica se as matrizes são válidas e se o número de colunas de A
# é igual ao número de linhas de B, uma condição necessária para a multiplicação.
from .validation_utils import validate_matrix_for_mult

def multiply_matrices(matrix_a, matrix_b):
    """
    Multiplica duas matrizes, matrix_a (A) e matrix_b (B), resultando em C = A * B.
    O elemento C[i][j] é o produto escalar da i-ésima linha de A com a j-ésima coluna de B.

    Args:
        matrix_a (list[list[float]]): A primeira matriz (operando esquerdo).
        matrix_b (list[list[float]]): A segunda matriz (operando direito).

    Returns:
        list[list[float]]: A matriz resultante da multiplicação.

    Raises:
        ValueError: Se as matrizes não forem válidas ou se o número de colunas
                    de matrix_a não for igual ao número de linhas de matrix_b.
    """
    # 1. Validação das Matrizes de Entrada:
    #    Garante que A e B são matrizes válidas e que o número de colunas de A
    #    é igual ao número de linhas de B. Se não, uma exceção (ValueError) é lançada.
    validate_matrix_for_mult(matrix_a, matrix_b)

    # 2. Obtenção das Dimensões Relevantes:
    #    - rows_a: Número de linhas da matriz A.
    #    - cols_a: Número de colunas da matriz A (que deve ser igual ao número de linhas da matriz B).
    #    - cols_b: Número de colunas da matriz B.
    #    A matriz resultante C terá dimensões rows_a x cols_b.
    rows_a = len(matrix_a)
    cols_a = len(matrix_a[0])  # Também é igual a len(matrix_b) (número de linhas de B)
    cols_b = len(matrix_b[0])

    # 3. Inicialização da Matriz de Resultado:
    #    Cria uma nova matriz 'result' (representando C) preenchida com zeros.
    #    As dimensões da matriz 'result' serão (rows_a x cols_b).
    #    Ex: Se A é 2x3 e B é 3x4, result será 2x4: [[0,0,0,0], [0,0,0,0]].
    result = [[0 for _ in range(cols_b)] for _ in range(rows_a)]

    # 4. Processo de Multiplicação (Cálculo de cada elemento C[i][j]):
    #    Itera sobre cada linha 'i' da matriz A (que será a linha 'i' da matriz resultado).
    for i in range(rows_a):
        #    Itera sobre cada coluna 'j' da matriz B (que será a coluna 'j' da matriz resultado).
        for j in range(cols_b):
            #       Para calcular o elemento result[i][j], é realizado o produto escalar
            #       da linha 'i' de matrix_a com a coluna 'j' de matrix_b.
            #       'sum_val' acumulará este produto escalar.
            sum_val = 0
            #       O índice 'k' itera sobre as colunas de A e, correspondentemente, sobre as linhas de B.
            #       Este loop interno realiza a soma dos produtos:
            #       sum_val = A[i][0]*B[0][j] + A[i][1]*B[1][j] + ... + A[i][cols_a-1]*B[cols_a-1][j]
            for k in range(cols_a): # Ou range(len(matrix_b)) que é o número de linhas de B
                sum_val += matrix_a[i][k] * matrix_b[k][j]
            
            #       Após o loop interno, 'sum_val' contém o valor do elemento C[i][j].
            result[i][j] = sum_val

    # 5. Retorno da Matriz Resultante:
    #    A matriz 'result', agora contendo o produto de matrix_a e matrix_b, é retornada.
    return result