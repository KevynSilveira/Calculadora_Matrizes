# calculadora_matrizes/tests/test_add_matrices.py

# Importa utilitários de teste:
# - format_matrix_for_log: Para exibir matrizes de forma legível no log de falhas.
# - are_matrices_equal: Para comparar a matriz resultado com a esperada, com tolerância para floats.
# - generate_matrix: Para criar matrizes de teste maiores com padrões definidos.
# - print_test_header/footer: Para formatar o output do conjunto de testes.
from test_utils import format_matrix_for_log, are_matrices_equal, generate_matrix, print_test_header, print_test_footer
# Importa a função específica que este arquivo de teste se destina a verificar.
from logic.add_matrices import add_matrices 

# Contadores globais para rastrear o número total de casos de teste executados
# e o número de casos que passaram.
test_count = 0
passed_count = 0

def run_add_test_case(m_a, m_b, expected_result, description, expect_error=False, error_message_contains=None):
    """
    Executa um único caso de teste para a função add_matrices.

    Esta função encapsula a lógica para:
    1. Chamar a função add_matrices com as matrizes de entrada (m_a, m_b).
    2. Comparar o resultado obtido com o resultado esperado (expected_result).
    3. Lidar com casos onde uma exceção (erro) é esperada (expect_error=True).
    4. Imprimir o status do teste ([OK] ou [FALHA]) e um log detalhado em caso de falha.

    Args:
        m_a (list[list[float]] or None): A primeira matriz para a soma.
        m_b (list[list[float]] or None): A segunda matriz para a soma.
        expected_result (list[list[float]] or None): A matriz que se espera como resultado da soma.
                                                    None se um erro é esperado.
        description (str): Uma breve descrição do caso de teste.
        expect_error (bool): True se este caso de teste espera que uma exceção ValueError seja levantada.
        error_message_contains (str or None): Se expect_error é True, esta string (ou parte dela,
                                              ignorando maiúsculas/minúsculas) deve estar contida na
                                              mensagem da exceção ValueError para o teste passar.
    """
    global test_count, passed_count # Permite modificar os contadores globais
    test_count += 1 # Incrementa o contador total de testes
    
    print(f"\n--- Teste: {description} ---") # Imprime um cabeçalho para o caso de teste
    
    # Prepara uma lista para armazenar detalhes do log em caso de falha
    log_details = [
        format_matrix_for_log(m_a, "Matriz A (Entrada)"),
        format_matrix_for_log(m_b, "Matriz B (Entrada)")
    ]

    try:
        # 1. Execução da Função Testada:
        #    Chama a função add_matrices com as matrizes fornecidas.
        result = add_matrices(m_a, m_b)
        
        # 2. Verificação Pós-Execução:
        if expect_error:
            # Se um erro era esperado, mas a função completou sem levantar uma exceção, o teste falha.
            print(f"[FALHA] - {description}")
            log_details.append("  Status: Um erro era esperado, mas a operação foi concluída sem erros.")
            log_details.append(format_matrix_for_log(result, "Resultado Obtido (Inesperado)"))
            if error_message_contains:
                 log_details.append(f"  Detalhe do Erro Esperado: A mensagem deveria conter '{error_message_contains}'")
        elif are_matrices_equal(result, expected_result):
            # Se nenhum erro era esperado e o resultado obtido é igual ao esperado (com tolerância), o teste passa.
            print(f"[OK] - {description}")
            passed_count += 1 # Incrementa o contador de testes que passaram
            return # Retorna cedo, pois não há necessidade de imprimir log detalhado para testes OK
        else:
            # Se nenhum erro era esperado, mas o resultado obtido é diferente do esperado, o teste falha.
            print(f"[FALHA] - {description}")
            log_details.append(format_matrix_for_log(expected_result, "Resultado Esperado"))
            log_details.append(format_matrix_for_log(result, "Resultado Obtido"))

    except ValueError as ve: # Captura especificamente ValueErrors, que são esperados para entradas inválidas.
        # 3. Tratamento de Exceções Esperadas:
        if expect_error:
            # Se um ValueError era esperado:
            # Verifica se a mensagem da exceção capturada (ve) contém a string esperada (error_message_contains).
            # A comparação é feita ignorando maiúsculas/minúsculas.
            if error_message_contains is None or error_message_contains.lower() in str(ve).lower():
                # Se a mensagem corresponde (ou nenhuma mensagem específica era esperada), o teste passa.
                print(f"[OK] - {description} (Erro esperado corretamente capturado: {ve})")
                passed_count += 1
                return
            else:
                # Se a mensagem da exceção não corresponde à esperada, o teste falha.
                print(f"[FALHA] - {description}")
                log_details.append(f"  Status: Um erro ValueError era esperado, mas sua mensagem não correspondeu ao esperado.")
                log_details.append(f"  Mensagem de Erro Obtida: ValueError: {ve}")
                log_details.append(f"  Esperado que a Mensagem Contivesse: '{error_message_contains}'")
        else:
            # Se um ValueError NÃO era esperado, mas ocorreu, o teste falha.
            print(f"[FALHA] - {description}")
            log_details.append(f"  Status: Erro ValueError inesperado durante a operação.")
            if expected_result is not None: # Só mostra o esperado se não era um teste de erro
                log_details.append(format_matrix_for_log(expected_result, "Resultado Esperado (se aplicável)"))
            log_details.append(f"  Detalhe do Erro: ValueError: {ve}")
            
    except Exception as e: # Captura qualquer outra exceção inesperada.
        # 4. Tratamento de Exceções Totalmente Inesperadas:
        #    Se ocorrer uma exceção diferente de ValueError, o teste falha.
        print(f"[FALHA] - {description}")
        log_details.append(f"  Status: Uma exceção totalmente inesperada do tipo {type(e).__name__} ocorreu.")
        if expected_result is not None and not expect_error:
            log_details.append(format_matrix_for_log(expected_result, "Resultado Esperado (se aplicável)"))
        log_details.append(f"  Detalhe do Erro: {e}")

    # 5. Impressão do Log Detalhado (Apenas em caso de FALHA):
    #    Se o teste chegou até aqui, significa que ele falhou por algum motivo.
    #    Imprime os detalhes coletados para ajudar na depuração.
    print("  Log Detalhado da Operação:")
    for detail in log_details:
        print(detail)

def test_soma_matrizes():
    """
    Define e executa uma suíte de casos de teste para a função add_matrices.
    Cobre cenários válidos (com diferentes tamanhos e tipos de dados) e inválidos (erros esperados).
    """
    global test_count, passed_count # Reseta os contadores para esta suíte de teste
    test_count = 0
    passed_count = 0
    
    print_test_header("add_matrices.py") # Imprime um cabeçalho para esta suíte de teste

    # --- Seção: Casos de Teste Válidos (onde a soma deve funcionar) ---

    # Teste 1: Soma de matrizes 1x1 simples
    run_add_test_case(
        m_a=[[1]], 
        m_b=[[2]], 
        expected_result=[[3]], 
        description="Soma de matrizes 1x1"
    )

    # Teste 2: Soma de matrizes 1x1 com números negativos
    run_add_test_case(
        m_a=[[-5]], 
        m_b=[[5]], 
        expected_result=[[0]], 
        description="Soma de matrizes 1x1 com negativos resultando em zero"
    )

    # Teste 3: Soma de matrizes 2x2
    m_a_2x2 = [[1, 2], [3, 4]]
    m_b_2x2 = [[5, 6], [7, 8]]
    exp_2x2 = [[6, 8], [10, 12]]
    run_add_test_case(m_a_2x2, m_b_2x2, exp_2x2, "Soma de matrizes 2x2 padrão")

    # Teste 4: Soma de matrizes 2x3 (retangulares)
    m_a_2x3 = [[1, 0, -1], [2, -2, 5]]
    m_b_2x3 = [[3, 2, 1],  [0,  4, 2]]
    exp_2x3 = [[4, 2, 0],  [2,  2, 7]]
    run_add_test_case(m_a_2x3, m_b_2x3, exp_2x3, "Soma de matrizes 2x3")

    # Teste 5: Soma de vetores coluna (matrizes 3x1)
    m_a_3x1 = [[10], [20], [30]]
    m_b_3x1 = [[-5], [-10], [-15]]
    exp_3x1 = [[5], [10], [15]]
    run_add_test_case(m_a_3x1, m_b_3x1, exp_3x1, "Soma de matrizes 3x1 (vetores coluna)")
    
    # Teste 6: Soma com uma matriz de zeros (elemento neutro da adição)
    m_a_zeros = [[0,0],[0,0]]
    m_b_ident_like = [[1,2],[3,4]] # Usando uma matriz qualquer
    run_add_test_case(m_a_zeros, m_b_ident_like, m_b_ident_like, "Soma com matriz de zeros (0 + B = B)")

    # Teste 7: Soma de matrizes contendo números de ponto flutuante (floats)
    m_a_float = [[0.5, 1.5], [2.0, -0.5]]
    m_b_float = [[0.5, 0.5], [-1.0, 0.5]]
    exp_float = [[1.0, 2.0], [1.0, 0.0]]
    run_add_test_case(m_a_float, m_b_float, exp_float, "Soma de matrizes com números de ponto flutuante")

    # Teste 8: Soma de matrizes 5x5 geradas automaticamente
    #   Matriz A: todos os elementos são 1
    #   Matriz B: todos os elementos são 2
    #   Resultado Esperado: todos os elementos são 3
    m_a_5x5 = generate_matrix(5, 5, lambda r, c: 1) 
    m_b_5x5 = generate_matrix(5, 5, lambda r, c: 2) 
    exp_5x5 = generate_matrix(5, 5, lambda r, c: 3) 
    run_add_test_case(m_a_5x5, m_b_5x5, exp_5x5, "Soma de matrizes 5x5 (geradas: 1s + 2s = 3s)")
    
    # Teste 9: Soma de matrizes 10x10 geradas automaticamente com valores mais complexos
    #   Matriz A: elemento A[r][c] = r + c
    #   Matriz B: todos os elementos são 1
    #   Resultado Esperado: elemento Exp[r][c] = r + c + 1
    m_a_10x10 = generate_matrix(10, 10, lambda r, c: r + c)
    m_b_10x10 = generate_matrix(10, 10, lambda r, c: 1)
    exp_10x10 = generate_matrix(10, 10, lambda r, c: r + c + 1)
    run_add_test_case(m_a_10x10, m_b_10x10, exp_10x10, "Soma de matrizes 10x10 (geradas com padrão r+c)")

    # --- Seção: Casos de Teste de Erro (onde a função deve levantar um ValueError) ---

    # Teste 10: Tentativa de somar matrizes com número de linhas incompatível
    run_add_test_case(
        m_a=[[1,2]],             # Matriz 1x2
        m_b=[[1],[2]],           # Matriz 2x1
        expected_result=None,    # Nenhum resultado esperado, pois um erro é esperado
        description="Soma com dimensões incompatíveis (erro: linhas diferentes)", 
        expect_error=True,       # Indica que um erro é esperado
        error_message_contains="mesmas dimensões" # Parte da mensagem de erro esperada
    )

    # Teste 11: Tentativa de somar matrizes com número de colunas incompatível
    run_add_test_case(
        m_a=[[1,2],[3,4]],       # Matriz 2x2
        m_b=[[1,2]],             # Matriz 1x2
        expected_result=None,
        description="Soma com dimensões incompatíveis (erro: colunas diferentes)", 
        expect_error=True,
        error_message_contains="mesmas dimensões"
    )

    # Teste 12: Matriz A é None (inválida)
    run_add_test_case(
        m_a=None, 
        m_b=[[1]], 
        expected_result=None,
        description="Soma com Matriz A inválida (None)",
        expect_error=True, 
        error_message_contains="deve ser uma lista de listas e não pode ser vazia" # Mensagem da validação
    )

    # Teste 13: Matriz B é uma string (inválida)
    run_add_test_case(
        m_a=[[1]], 
        m_b="[[1]]", # Matriz B como string
        expected_result=None,
        description="Soma com Matriz B inválida (string)",
        expect_error=True, 
        error_message_contains="deve ser uma lista de listas e não pode ser vazia"
    )
    
    # Teste 14: Matriz A contém uma linha vazia (ex: [[]])
    run_add_test_case(
        m_a=[[]], 
        m_b=[[1]], 
        expected_result=None,
        description="Soma com Matriz A contendo linha vazia [[]]",
        expect_error=True, 
        error_message_contains="linha(s) vazia(s) ou não foi inicializada corretamente"
    )
    
    # Teste 15: Matriz A com número inconsistente de colunas entre as linhas
    run_add_test_case(
        m_a=[[1,2],[3]],       # Linha 0 tem 2 colunas, Linha 1 tem 1 coluna
        m_b=[[1,1],[1,1]],     # Matriz B válida para referência
        expected_result=None,
        description="Soma com Matriz A com contagem de colunas inconsistente",
        expect_error=True, 
        error_message_contains="mesmo número de colunas"
    )

    print_test_footer("add_matrices.py", test_count, passed_count) # Imprime o resumo dos testes

if __name__ == "__main__":
    # Este bloco permite que o arquivo de teste seja executado diretamente.
    test_soma_matrizes()