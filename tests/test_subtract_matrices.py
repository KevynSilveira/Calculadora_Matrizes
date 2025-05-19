# calculadora_matrizes/tests/test_subtract_matrices.py

# Importa utilitários de teste:
# - format_matrix_for_log: Para exibir matrizes de forma legível.
# - are_matrices_equal: Para comparar a matriz resultado com a esperada, com tolerância.
# - generate_matrix: Para criar matrizes de teste maiores.
# - print_test_header/footer: Para formatar o output do conjunto de testes.
from test_utils import format_matrix_for_log, are_matrices_equal, generate_matrix, print_test_header, print_test_footer
# Importa a função de subtração de matrizes que será testada.
from logic.subtract_matrices import subtract_matrices

# Contadores globais para rastrear estatísticas dos testes.
test_count = 0
passed_count = 0

def run_subtract_test_case(m_a, m_b, expected_result, description, 
                           expect_error=False, error_message_contains=None):
    """
    Executa um único caso de teste para a função subtract_matrices.

    Esta função irá:
    1. Chamar 'subtract_matrices(m_a, m_b)'.
    2. Se um erro é esperado (expect_error=True):
        a. Verificar se um ValueError foi levantado.
        b. Se sim, verificar se a mensagem de erro contém 'error_message_contains'.
    3. Se nenhum erro é esperado:
        a. Comparar o resultado obtido com 'expected_result' usando 'are_matrices_equal'.
    4. Imprimir o status ([OK] ou [FALHA]) e um log detalhado em caso de falha.

    Args:
        m_a (list[list[float]] or None): A primeira matriz (minuendo).
        m_b (list[list[float]] or None): A segunda matriz (subtraendo).
        expected_result (list[list[float]] or None): A matriz esperada como resultado da subtração.
                                                    None se um erro é esperado.
        description (str): Descrição do caso de teste.
        expect_error (bool): True se uma exceção ValueError é esperada.
        error_message_contains (str or None): Substring esperada na mensagem de erro.
    """
    global test_count, passed_count
    test_count += 1
    
    print(f"\n--- Teste: {description} ---")
    # Log inicial com as matrizes de entrada A (minuendo) e B (subtraendo).
    log_details = [
        format_matrix_for_log(m_a, "Matriz A (Minuendo) - Entrada"),
        format_matrix_for_log(m_b, "Matriz B (Subtraendo) - Entrada")
    ]

    try:
        # 1. Execução da Função: Realiza a subtração das matrizes (A - B).
        result = subtract_matrices(m_a, m_b)
        
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

    except ValueError as ve: # Captura ValueErrors (dimensões incompatíveis, matrizes inválidas, etc.)
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
    for detail in log_details:
        print(detail)

def test_subtracao_matrizes():
    """
    Define e executa uma suíte de casos de teste para a função subtract_matrices.
    Cobre cenários válidos com diferentes tamanhos e tipos de dados (inteiros, floats),
    casos especiais (subtração por zero, subtração de zero), e
    cenários de erro (dimensões incompatíveis, matrizes inválidas).
    """
    global test_count, passed_count
    test_count = 0
    passed_count = 0
    
    print_test_header("subtract_matrices.py") # Imprime um cabeçalho para esta suíte de teste

    # --- Seção: Casos de Teste Válidos ---

    # Teste 1: Subtração de matrizes 1x1 simples
    run_subtract_test_case(
        m_a=[[5]], 
        m_b=[[2]], 
        expected_result=[[3]], 
        description="Subtração de matrizes 1x1 (5 - 2 = 3)"
    )

    # Teste 2: Subtração resultando em valor negativo
    run_subtract_test_case(
        m_a=[[1]], 
        m_b=[[5]], 
        expected_result=[[-4]], 
        description="Subtração de matrizes 1x1 resultando em negativo (1 - 5 = -4)"
    )

    # Teste 3: Subtração de matrizes 2x2
    m_a_2x2 = [[10, 20], [30, 40]]
    m_b_2x2 = [[1, 2], [3, 4]]
    exp_2x2 = [[9, 18], [27, 36]] # (10-1, 20-2), (30-3, 40-4)
    run_subtract_test_case(m_a_2x2, m_b_2x2, exp_2x2, "Subtração de matrizes 2x2 padrão")

    # Teste 4: Subtração de matrizes 2x3 (retangulares)
    m_a_2x3 = [[1, 0, -1], [2, -2, 5]]
    m_b_2x3 = [[3, 2, 1],  [0,  4, 2]]
    exp_2x3 = [[-2, -2, -2], [2, -6, 3]] # (1-3, 0-2, -1-1), (2-0, -2-4, 5-2)
    run_subtract_test_case(m_a_2x3, m_b_2x3, exp_2x3, "Subtração de matrizes 2x3")
    
    # Teste 5: Subtração envolvendo matriz de zeros (0 - B = -B)
    m_zeros_2x2 = [[0,0],[0,0]]
    m_b_any_2x2 = [[1,2],[3,4]]
    exp_neg_b_2x2 = [[-1,-2],[-3,-4]]
    run_subtract_test_case(m_zeros_2x2, m_b_any_2x2, exp_neg_b_2x2, "Subtração de matriz de zeros por outra (0 - B = -B)")
    
    # Teste 6: Subtração por matriz de zeros (B - 0 = B)
    run_subtract_test_case(m_b_any_2x2, m_zeros_2x2, m_b_any_2x2, "Subtração por matriz de zeros (B - 0 = B)")

    # Teste 7: Subtração de matrizes contendo números de ponto flutuante (floats)
    m_a_float = [[0.5, 1.5], [2.0, -0.5]]
    m_b_float = [[0.2, 0.5], [-1.0, 0.8]]
    exp_float = [[0.3, 1.0], [3.0, -1.3]] # (0.5-0.2, 1.5-0.5), (2.0-(-1.0), -0.5-0.8)
    run_subtract_test_case(m_a_float, m_b_float, exp_float, "Subtração de matrizes com números de ponto flutuante")

    # Teste 8: Subtração de matrizes 10x10 geradas automaticamente
    #   Matriz A: elemento A[r][c] = r + c + 5
    #   Matriz B: todos os elementos são 1
    #   Resultado Esperado: elemento Exp[r][c] = r + c + 4
    m_a_10x10 = generate_matrix(10, 10, lambda r, c: r + c + 5)
    m_b_10x10 = generate_matrix(10, 10, lambda r, c: 1)
    exp_10x10 = generate_matrix(10, 10, lambda r, c: r + c + 4)
    run_subtract_test_case(m_a_10x10, m_b_10x10, exp_10x10, "Subtração de matrizes 10x10 (geradas)")

    # --- Seção: Casos de Teste de Erro ---
    # Teste 9: Tentativa de subtrair matrizes com dimensões incompatíveis
    run_subtract_test_case(
        m_a=[[1,2]],           # Matriz 1x2
        m_b=[[1],[2]],         # Matriz 2x1
        expected_result=None,
        description="Subtração com dimensões incompatíveis (erro: linhas/colunas diferentes)", 
        expect_error=True, 
        error_message_contains="mesmas dimensões" # Parte da mensagem de erro esperada
    )
    
    # Teste 10: Matriz A é None (inválida)
    run_subtract_test_case(
        m_a=None, 
        m_b=[[1]], 
        expected_result=None,
        description="Subtração com Matriz A inválida (None)",
        expect_error=True, 
        error_message_contains="deve ser uma lista de listas" # Mensagem da validação
    )

    # Teste 11: Matriz B com estrutura inválida (linha interna não é lista)
    run_subtract_test_case(
        m_a=[[1,2],[3,4]],
        m_b=[[5,6], 7], # Segunda linha de B não é uma lista
        expected_result=None,
        description="Subtração com Matriz B com estrutura inválida (elemento não é lista)",
        expect_error=True,
        error_message_contains="deve ser uma lista de listas" # Erro pego por _is_valid_matrix_structure em B
    )


    print_test_footer("subtract_matrices.py", test_count, passed_count)

if __name__ == "__main__":
    test_subtracao_matrizes()