# calculadora_matrizes/logic/validation_utils.py

# Este módulo contém funções de utilidade para validar a estrutura e as
# dimensões das matrizes antes de realizar operações matemáticas sobre elas.
# O objetivo é garantir a integridade dos dados e fornecer mensagens de erro claras.

def _is_valid_matrix_structure(matrix, matrix_name="Matriz"):
    """
    (Função auxiliar interna) Verifica a estrutura fundamental de uma matriz.
    Garante que a entrada é uma lista de listas e não é completamente vazia.
    Também verifica se a primeira linha (se a matriz tiver linhas) não é uma lista vazia.
    """
    # 1. Checagem de Tipo e Não Vazio:
    #    - 'not matrix': Verifica se a matriz é None ou uma lista vazia [].
    #    - 'not isinstance(matrix, list)': Verifica se a matriz é de fato uma lista.
    #    - 'not all(isinstance(row, list) for row in matrix)': Verifica se todos os elementos
    #      da lista principal (as linhas) são também listas.
    if not matrix or not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
        raise ValueError(f"{matrix_name} deve ser uma lista de listas e não pode ser vazia.")
    
    # 2. Checagem de Linha(s) Vazia(s) Interna(s):
    #    - 'not matrix[0]': Verifica se a primeira linha da matriz é uma lista vazia (ex: [[]]).
    #    - 'len(matrix) > 0': Garante que a matriz tem pelo menos uma linha antes de acessar matrix[0].
    #    Esta checagem é importante, pois uma matriz como [[]] é uma lista de listas,
    #    mas funcionalmente inválida para a maioria das operações matriciais.
    if not matrix[0] and len(matrix) > 0: # A segunda condição é redundante se a primeira checagem passou para 'not matrix'
                                         # Mas é uma boa prática para clareza ao acessar matrix[0].
         raise ValueError(f"{matrix_name} contém linha(s) vazia(s) ou não foi inicializada corretamente.")
    return True

def _has_consistent_column_count(matrix, matrix_name="Matriz"):
    """
    (Função auxiliar interna) Verifica se todas as linhas de uma matriz têm o mesmo número de colunas.
    Assume que a estrutura básica (lista de listas, primeira linha não vazia) já foi validada.
    """
    # 1. Condição de Saída Antecipada:
    #    Se a matriz é vazia (None, []) ou se a primeira linha é vazia ([[]]),
    #    essa checagem não é aplicável ou já foi tratada pela _is_valid_matrix_structure.
    #    Retorna True pois a consistência de colunas não pode ser violada nesses casos.
    if not matrix or not matrix[0]: 
        return True 
    
    # 2. Determinação do Número de Colunas da Primeira Linha:
    #    Assume-se que todas as outras linhas devem ter este mesmo número de colunas.
    first_row_len = len(matrix[0])
    
    # 3. Verificação da Consistência:
    #    Itera por todas as linhas da matriz e verifica se o comprimento (len)
    #    de cada linha é igual ao 'first_row_len'.
    #    'all(...)' retorna True apenas se a condição for verdadeira para todas as linhas.
    if not all(len(row) == first_row_len for row in matrix):
        raise ValueError(f"Todas as linhas da {matrix_name} devem ter o mesmo número de colunas.")
    return True

def validate_matrix_input(matrix, matrix_name="Matriz"):
    """
    Validação compreensiva para uma única matriz.
    Chama as funções auxiliares para verificar estrutura e consistência de colunas.
    """
    # 1. Valida a estrutura básica: se é uma lista de listas, não vazia, e a primeira linha não é vazia.
    _is_valid_matrix_structure(matrix, matrix_name)
    # 2. Valida se todas as linhas têm o mesmo número de colunas.
    _has_consistent_column_count(matrix, matrix_name)
    # Se ambas as validações passarem, a matriz é considerada estruturalmente válida.
    return True


def validate_matrices_for_add_sub(matrix_a, matrix_b):
    """
    Valida duas matrizes (A e B) para operações de adição ou subtração.
    Garante que ambas são válidas individualmente e que possuem as mesmas dimensões.
    """
    # 1. Validação Individual:
    #    Primeiro, cada matriz (A e B) é validada independentemente usando 'validate_matrix_input'.
    validate_matrix_input(matrix_a, "Matriz A")
    validate_matrix_input(matrix_b, "Matriz B")
    
    # 2. Verificação de Dimensões Iguais:
    #    - 'len(matrix_a) != len(matrix_b)': Compara o número de linhas.
    #    - 'len(matrix_a[0]) != len(matrix_b[0])': Compara o número de colunas (da primeira linha,
    #      assumindo que a consistência interna de cada matriz já foi validada).
    #    Se as dimensões não forem idênticas, uma exceção é levantada.
    if len(matrix_a) != len(matrix_b) or len(matrix_a[0]) != len(matrix_b[0]):
        raise ValueError("Matrizes devem ter as mesmas dimensões para adição/subtração.")
    return True

def validate_matrix_for_mult(matrix_a, matrix_b):
    """
    Valida duas matrizes (A e B) para a operação de multiplicação (A * B).
    Garante que ambas são válidas individualmente e que o número de colunas de A
    é igual ao número de linhas de B.
    """
    # 1. Validação Individual:
    #    Valida cada matriz separadamente.
    validate_matrix_input(matrix_a, "Matriz A")
    validate_matrix_input(matrix_b, "Matriz B")
    
    # 2. Verificação da Condição de Multiplicação:
    #    Para multiplicar A (m x n) por B (p x q), é necessário que n == p.
    #    - 'len(matrix_a[0])': Número de colunas da matriz A.
    #    - 'len(matrix_b)': Número de linhas da matriz B.
    #    Se esta condição não for satisfeita, a multiplicação não é definida.
    if len(matrix_a[0]) != len(matrix_b):
        raise ValueError("Número de colunas da Matriz A deve ser igual ao número de linhas da Matriz B para multiplicação.")
    return True

def validate_square_matrix(matrix, matrix_name="Matriz"):
    """
    Valida se uma matriz é quadrada (número de linhas igual ao número de colunas).
    Também realiza as validações básicas de 'validate_matrix_input'.
    """
    # 1. Validação Básica da Matriz:
    #    Chama 'validate_matrix_input' para garantir que é uma matriz bem formada.
    validate_matrix_input(matrix, matrix_name)
    
    # 2. Checagem Adicional para Linha Vazia (Defensiva):
    #    Embora 'validate_matrix_input' já verifique isso através de '_is_valid_matrix_structure',
    #    esta checagem é uma redundância defensiva antes de comparar len(matrix) com len(matrix[0]).
    #    Se matrix[0] for vazia, len(matrix[0]) seria 0, o que poderia levar a uma
    #    conclusão incorreta sobre ser quadrada se, por exemplo, matrix fosse [[]] (1 linha, 0 colunas).
    #    NOTA: A lógica em _is_valid_matrix_structure já impede [[]] de passar, tornando esta linha
    #    potencialmente redundante se a ordem de chamadas for garantida. No entanto, não causa dano.
    if not matrix[0]: # Esta condição já é coberta por _is_valid_matrix_structure
        # Se chegou aqui e matrix[0] é falso (vazio), _is_valid_matrix_structure deveria ter pego.
        # Mantido por segurança ou se a lógica de chamada mudar.
        raise ValueError(f"{matrix_name} é inválida (linha vazia detectada em validate_square_matrix) e não pode ser verificada como quadrada.")

    # 3. Verificação de "Quadratura":
    #    Compara o número de linhas ('len(matrix)') com o número de colunas ('len(matrix[0])').
    #    Se não forem iguais, a matriz não é quadrada.
    if len(matrix) != len(matrix[0]):
        raise ValueError(f"{matrix_name} deve ser quadrada.")
    return True

def validate_linear_system_inputs(matrix_a, vector_b):
    """
    Valida as entradas para resolver um sistema linear AX = B.
    Verifica se A é quadrada, B é um vetor coluna, e suas dimensões são compatíveis.
    """
    # 1. Validação da Matriz de Coeficientes (A):
    #    'matrix_a' deve ser uma matriz quadrada válida.
    validate_square_matrix(matrix_a, "Matriz A (coeficientes)")
    
    # 2. Validação do Vetor de Termos Independentes (B):
    #    'vector_b' deve ser uma matriz válida (que representará um vetor coluna).
    validate_matrix_input(vector_b, "Vetor B (termos independentes)")

    # 3. Verificação de Compatibilidade de Linhas:
    #    O número de equações (linhas de A) deve ser igual ao número de elementos
    #    no vetor B (linhas de B, já que B é um vetor coluna).
    if len(matrix_a) != len(vector_b):
        raise ValueError("Número de linhas da Matriz A (coeficientes) deve ser igual ao número de linhas do Vetor B.")
    
    # 4. Verificação de Vetor Coluna para B:
    #    'vector_b' deve ter exatamente uma coluna para ser um vetor coluna.
    if len(vector_b[0]) != 1:
        raise ValueError("Vetor B (termos independentes) deve ser um vetor coluna (ter uma única coluna).")
    return True