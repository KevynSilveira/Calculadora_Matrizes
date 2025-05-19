# calculadora_matrizes/tests/test_multiply_matrices.py

# Importa utilitários de teste:
# - format_matrix_for_log: Para exibir matrizes de forma legível no log.
# - are_matrices_equal: Para comparar a matriz resultado com a esperada, com tolerância.
# - generate_matrix: Para criar matrizes de teste maiores.
# - print_test_header/footer: Para formatar o output do conjunto de testes.
from test_utils import format_matrix_for_log, are_matrices_equal, generate_matrix, print_test_header, print_test_footer
# Importa a função de multiplicação de matrizes que será testada.
from logic.multiply_matrices import multiply_matrices

# Contadores globais para rastrear estatísticas dos testes.
test_count = 0
passed_count = 0

def run_multiply_test_case(m_a, m_b, expected_result, description, expect_error=False, error_message_contains=None):
    """
    Executa um único caso de teste para a função multiply_matrices.

    Esta função irá:
    1. Chamar 'multiply_matrices(m_a, m_b)'.
    2. Se um erro é esperado (expect_error=True):
        a. Verificar se um ValueError foi levantado.
        b. Se sim, verificar se a mensagem de erro contém 'error_message_contains'.
    3. Se nenhum erro é esperado:
        a. Comparar o resultado obtido com 'expected_result' usando 'are_matrices_equal'.
    4. Imprimir o status ([OK] ou [FALHA]) e um log detalhado em caso de falha.

    Args:
        m_a (list[list[float]] or None): A primeira matriz (operando esquerdo).
        m_b (list[list[float]] or None): A segunda matriz (operando direito).
        expected_result (list[list[float]] or None): A matriz esperada como resultado.
                                                    None se um erro é esperado.
        description (str): Descrição do caso de teste.
        expect_error (bool): True se uma exceção ValueError é esperada.
        error_message_contains (str or None): Substring esperada na mensagem de erro.
    """
    global test_count, passed_count
    test_count += 1
    print(f"\n--- Teste: {description} ---")
    # Log inicial com as matrizes de entrada.
    log_details = [
        format_matrix_for_log(m_a, "Matriz A (Entrada)"), 
        format_matrix_for_log(m_b, "Matriz B (Entrada)")
    ]

    try:
        # 1. Execução da Função: Realiza a multiplicação das matrizes.
        result = multiply_matrices(m_a, m_b)
        
        # 2. Verificação Pós-Execução (se nenhum erro ocorreu durante a execução):
        if expect_error:
            # Se um erro ERA esperado, mas a função completou, o teste FALHA.
            print(f"[FALHA] - {description}")
            log_details.append("  Status: Um erro era esperado, mas a operação foi concluída sem erros.")
            log_details.append(format_matrix_for_log(result, "Resultado Obtido (Inesperado)"))
            if error_message_contains: 
                log_details.append(f"  Detalhe do Erro Esperado: A mensagem deveria conter '{error_message_contains}'")
        elif are_matrices_equal(result, expected_result):
            # Se nenhum erro era esperado e o resultado bate com o esperado, o teste PASSA.
            print(f"[OK] - {description}")
            passed_count += 1
            return # Saída antecipada para testes OK.
        else:
            # Se o resultado não bate com o esperado, o teste FALHA.
            print(f"[FALHA] - {description}")
            log_details.append(format_matrix_for_log(expected_result, "Resultado Esperado"))
            log_details.append(format_matrix_for_log(result, "Resultado Obtido"))

    except ValueError as ve: # Captura ValueErrors (dimensões incompatíveis, etc.)
        # 3. Tratamento de ValueErrors:
        if expect_error:
            # Se um ValueError era esperado:
            # Verifica se a mensagem de erro capturada contém a substring esperada.
            if error_message_contains is None or error_message_contains.lower() in str(ve).lower():
                # Se a mensagem corresponde, o teste PASSA.
                print(f"[OK] - {description} (Erro esperado ValueError corretamente capturado: {ve})")
                passed_count += 1
                return
            else:
                # Se a mensagem não corresponde, o teste FALHA.
                print(f"[FALHA] - {description}")
                log_details.append(f"  Status: Um erro ValueError era esperado, mas sua mensagem não correspondeu.")
                log_details.append(f"  Mensagem de Erro Obtida: ValueError: {ve}")
                log_details.append(f"  Esperado que a Mensagem Contivesse: '{error_message_contains}'")
        else:
            # Se um ValueError NÃO era esperado, mas ocorreu, o teste FALHA.
            print(f"[FALHA] - {description}")
            log_details.append(f"  Status: Erro ValueError inesperado durante a operação.")
            if not expect_error and expected_result is not None: 
                log_details.append(format_matrix_for_log(expected_result, "Resultado Esperado (se aplicável)"))
            log_details.append(f"  Detalhe do Erro: ValueError: {ve}")
            
    except Exception as e: # Captura qualquer outra exceção não prevista.
        # 4. Tratamento de Outras Exceções Inesperadas:
        print(f"[FALHA] - {description}")
        log_details.append(f"  Status: Uma exceção totalmente inesperada do tipo {type(e).__name__} ocorreu.")
        if not expect_error and expected_result is not None:
            log_details.append(format_matrix_for_log(expected_result, "Resultado Esperado (se aplicável)"))
        log_details.append(f"  Detalhe do Erro: {e}")
    
    # 5. Impressão do Log Detalhado (Apenas em caso de FALHA):
    print("  Log Detalhado da Operação:")
    for detail in log_details: print(detail)

def test_multiplicacao_matrizes():
    """
    Define e executa uma suíte de casos de teste para a função multiply_matrices.
    Cobre diferentes dimensões de matrizes, casos especiais (identidade, zeros)
    e cenários de erro (dimensões incompatíveis, matrizes inválidas).
    """
    global test_count, passed_count
    test_count = 0
    passed_count = 0
    print_test_header("multiply_matrices.py")

    # --- Seção: Casos de Teste Válidos ---
    # Teste 1: Multiplicação de escalares (representados como matrizes 1x1)
    run_multiply_test_case([[2]], [[3]], [[6]], "Multiplicação 1x1 (escalares)")
    
    # Teste 2: Produto de um vetor linha por um vetor coluna -> escalar (matriz 1x1)
    # (1x2) * (2x1) = (1x1)
    # [1, 2] * [[3], [4]] = [[1*3 + 2*4]] = [[3 + 8]] = [[11]]
    run_multiply_test_case([[1, 2]], [[3], [4]], [[11]], "Multiplicação (Vetor Linha * Vetor Coluna) -> Escalar 1x1")
    
    # Teste 3: Produto de um vetor coluna por um vetor linha -> matriz
    # (2x1) * (1x2) = (2x2)
    # [[1], [2]] * [[3, 4]] = [[1*3, 1*4], [2*3, 2*4]] = [[3, 4], [6, 8]]
    run_multiply_test_case([[1], [2]], [[3, 4]], [[3, 4], [6, 8]], "Multiplicação (Vetor Coluna * Vetor Linha) -> Matriz 2x2")
    
    # Teste 4: Multiplicação de matrizes 2x2 padrão
    m_a_2x2 = [[1, 2], [3, 4]]
    m_b_2x2 = [[2, 0], [1, 2]]
    # Calculado como:
    # C11 = 1*2 + 2*1 = 4
    # C12 = 1*0 + 2*2 = 4
    # C21 = 3*2 + 4*1 = 10
    # C22 = 3*0 + 4*2 = 8
    exp_2x2 = [[4, 4], [10, 8]] 
    run_multiply_test_case(m_a_2x2, m_b_2x2, exp_2x2, "Multiplicação de matrizes 2x2")

    # Teste 5: Multiplicação de matrizes retangulares (2x3) * (3x2) -> (2x2)
    m_a_2x3 = [[1, 0, 2], [0, 3, -1]]
    m_b_3x2 = [[1, 1], [0, 2], [2, 0]]
    # C11 = 1*1 + 0*0 + 2*2 = 5
    # C12 = 1*1 + 0*2 + 2*0 = 1
    # C21 = 0*1 + 3*0 + (-1)*2 = -2
    # C22 = 0*1 + 3*2 + (-1)*0 = 6
    exp_2x2_from_2x3_3x2 = [[5, 1], [-2, 6]] 
    run_multiply_test_case(m_a_2x3, m_b_3x2, exp_2x2_from_2x3_3x2, "Multiplicação (2x3) * (3x2) resultando em 2x2")

    # Teste 6 e 7: Multiplicação por matriz identidade (A*I = A e I*A = A)
    ident_3x3 = [[1,0,0],[0,1,0],[0,0,1]]
    m_a_3x3 = [[1,2,3],[4,5,6],[7,8,9]]
    run_multiply_test_case(m_a_3x3, ident_3x3, m_a_3x3, "Multiplicação por Matriz Identidade à direita (A*I = A)")
    run_multiply_test_case(ident_3x3, m_a_3x3, m_a_3x3, "Multiplicação por Matriz Identidade à esquerda (I*A = A)")
    
    # Teste 8: Multiplicação por matriz de zeros (A*0 = 0)
    zeros_2x2 = [[0,0],[0,0]] # Matriz de resultado também será 2x2 de zeros
    run_multiply_test_case(m_a_2x2, zeros_2x2, zeros_2x2, "Multiplicação por Matriz de Zeros (A*0 = 0)")

    # Teste 9: Multiplicação de matriz identidade maior por outra matriz
    # (5x5 Identidade) * (5x2 Matriz Genérica) -> (5x2 Matriz Genérica)
    m_a_5x5_ident = generate_matrix(5,5, lambda r,c: 1 if r==c else 0) # Identidade 5x5
    m_b_5x2_gen = generate_matrix(5,2, lambda r,c: r*2 + c + 1) # Matriz 5x2 com valores (r*2+c+1)
    run_multiply_test_case(m_a_5x5_ident, m_b_5x2_gen, m_b_5x2_gen, "Multiplicação (Identidade 5x5 * Matriz 5x2)")

    # Teste 10: Multiplicação de matrizes maiores (7x10) * (10x3) -> (7x3)
    # Matriz A: 7x10, todos os elementos são 1
    # Matriz B: 10x3, todos os elementos são 2
    # Resultado Esperado: Matriz 7x3, todos os elementos são 20 (soma de 10 produtos de 1*2)
    m_a_7x10_ones = generate_matrix(7,10, lambda r,c: 1)
    m_b_10x3_twos = generate_matrix(10,3, lambda r,c: 2)
    exp_7x3_twenties = [[20 for _ in range(3)] for _ in range(7)] 
    run_multiply_test_case(m_a_7x10_ones, m_b_10x3_twos, exp_7x3_twenties, "Multiplicação Matriz 7x10 (de 1s) * Matriz 10x3 (de 2s)")

    # --- Seção: Casos de Teste de Erro ---
    # Teste 11: Dimensões incompatíveis (número de colunas de A != número de linhas de B)
    run_multiply_test_case(
        m_a=[[1,2]],           # Matriz 1x2
        m_b=[[1,2]],           # Matriz 1x2 (precisaria ser 2xN)
        expected_result=None,
        description="Multiplicação com dimensões incompatíveis (Colunas A != Linhas B)",
        expect_error=True, 
        error_message_contains="colunas da Matriz A deve ser igual ao número de linhas da Matriz B"
    )
    # Teste 12: Outro caso de dimensões incompatíveis
    run_multiply_test_case(
        m_a=[[1],[2]],         # Matriz 2x1
        m_b=[[1,2],[3,4],[5,6]], # Matriz 3x2 (A precisaria ter 3 colunas)
        expected_result=None,
        description="Multiplicação com dimensões incompatíveis (Colunas A != Linhas B, B maior)",
        expect_error=True, 
        error_message_contains="colunas da Matriz A deve ser igual ao número de linhas da Matriz B"
    )
    # Teste 13: Matriz A é None (inválida)
    run_multiply_test_case(
        m_a=None, 
        m_b=[[1]], 
        expected_result=None,
        description="Multiplicação com Matriz A inválida (None)",
        expect_error=True, 
        error_message_contains="deve ser uma lista de listas" # Mensagem da validação
    )
    # Teste 14: Matriz A contém uma linha vazia (ex: [[]])
    run_multiply_test_case(
        m_a=[[]], 
        m_b=[[1]], 
        expected_result=None,
        description="Multiplicação com Matriz A inválida (contém linha vazia [[]])",
        expect_error=True, 
        error_message_contains="linha(s) vazia(s)" # Mensagem da validação
    )

    print_test_footer("multiply_matrices.py", test_count, passed_count)

if __name__ == "__main__":
    test_multiplicacao_matrizes()