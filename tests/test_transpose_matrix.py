# calculadora_matrizes/tests/test_transpose_matrix.py

# Importa utilitários de teste:
# - format_matrix_for_log: Para exibir matrizes de forma legível.
# - are_matrices_equal: Para comparar a matriz transposta calculada com a esperada.
# - generate_matrix: Para criar matrizes de teste maiores.
# - print_test_header/footer: Para formatar o output do conjunto de testes.
from test_utils import format_matrix_for_log, are_matrices_equal, generate_matrix, print_test_header, print_test_footer
# Importa a função de transposição de matrizes que será testada.
from logic.transpose_matrix import transpose_matrix

# Contadores globais para rastrear estatísticas dos testes.
test_count = 0
passed_count = 0

def run_transpose_test_case(matrix, expected_result, description, 
                            expect_error=False, error_message_contains=None):
    """
    Executa um único caso de teste para a função transpose_matrix.

    Esta função irá:
    1. Chamar 'transpose_matrix(matrix)'.
    2. Se um erro é esperado (expect_error=True):
        a. Verificar se um ValueError (da validação da matriz) foi levantado.
        b. Se sim, verificar se a mensagem de erro contém 'error_message_contains'.
    3. Se nenhum erro é esperado:
        a. Comparar o resultado obtido com 'expected_result' usando 'are_matrices_equal'.
    4. Imprimir o status ([OK] ou [FALHA]) e um log detalhado em caso de falha.

    Args:
        matrix (list[list[float]] or None): A matriz a ser transposta.
        expected_result (list[list[float]] or None): A matriz transposta esperada.
                                                    None se um erro é esperado.
        description (str): Descrição do caso de teste.
        expect_error (bool): True se uma exceção ValueError é esperada.
        error_message_contains (str or None): Substring esperada na mensagem de erro.
    """
    global test_count, passed_count
    test_count += 1
    print(f"\n--- Teste: {description} ---")
    # Log inicial com a matriz de entrada.
    log_details = [format_matrix_for_log(matrix, "Matriz Original de Entrada")]

    try:
        # 1. Execução da Função: Calcula a transposta da matriz.
        result = transpose_matrix(matrix)
        
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

    except ValueError as ve: # Captura ValueErrors da validação da matriz.
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

def test_transposicao_matriz():
    """
    Define e executa uma suíte de casos de teste para a função transpose_matrix.
    Cobre matrizes quadradas, retangulares (linha e coluna), e a propriedade T(T(A))=A.
    Também testa o tratamento de matrizes de entrada inválidas.
    """
    global test_count, passed_count
    test_count = 0
    passed_count = 0
    print_test_header("transpose_matrix.py")

    # --- Seção: Casos de Teste Válidos ---
    # Teste 1: Transposição de uma matriz 1x1 (a transposta é ela mesma).
    run_transpose_test_case(
        matrix=[[1]], 
        expected_result=[[1]], 
        description="Transposição de matriz 1x1"
    )
    
    # Teste 2: Transposição de uma matriz linha (1x3) para uma matriz coluna (3x1).
    run_transpose_test_case(
        matrix=[[1, 2, 3]], 
        expected_result=[[1], [2], [3]], 
        description="Transposição de matriz linha (1x3) para coluna (3x1)"
    )
    
    # Teste 3: Transposição de uma matriz coluna (3x1) para uma matriz linha (1x3).
    run_transpose_test_case(
        matrix=[[1], [2], [3]], 
        expected_result=[[1, 2, 3]], 
        description="Transposição de matriz coluna (3x1) para linha (1x3)"
    )
    
    # Teste 4: Transposição de uma matriz quadrada 2x2.
    m_2x2 = [[1, 2], [3, 4]]
    exp_2x2_t = [[1, 3], [2, 4]] # Linhas viram colunas
    run_transpose_test_case(m_2x2, exp_2x2_t, "Transposição de matriz 2x2")

    # Teste 5: Transposição de uma matriz retangular 2x3 para 3x2.
    m_2x3 = [[1, 2, 3], [4, 5, 6]]
    exp_3x2_t = [[1, 4], [2, 5], [3, 6]]
    run_transpose_test_case(m_2x3, exp_3x2_t, "Transposição de matriz 2x3 para 3x2")

    # Teste 6: Propriedade da transposição dupla: T(T(A)) = A.
    #   Primeiro, calcula a transposta de m_2x3 (que é exp_3x2_t).
    #   Depois, transpõe o resultado e compara com a m_2x3 original.
    transposed_once = transpose_matrix(m_2x3) # Resultado esperado é exp_3x2_t
    run_transpose_test_case(transposed_once, m_2x3, 
                            "Transposição dupla (T(T(A)) = A) para matriz 2x3")

    # Teste 7: Transposição de uma matriz 10x2 gerada (resulta em 2x10).
    #   Matriz Original: 10 linhas, 2 colunas. Elemento A[r][c] = r * 10 + c
    #   Matriz Transposta Esperada: 2 linhas, 10 colunas. Elemento A_T[r][c] = c * 10 + r
    #   (onde r, c são os índices da matriz transposta)
    m_10x2 = generate_matrix(10, 2, lambda r_orig, c_orig: r_orig * 10 + c_orig)
    # Para a transposta, as dimensões são trocadas, e a lógica do gerador também deve refletir a transposição.
    exp_2x10_t = generate_matrix(2, 10, lambda r_transp, c_transp: c_transp * 10 + r_transp)
    run_transpose_test_case(m_10x2, exp_2x10_t, "Transposição de matriz 10x2 (gerada)")
    
    # --- Seção: Casos de Teste de Erro ---
    # Teste 8: Matriz de entrada é None.
    run_transpose_test_case(
        matrix=None, 
        expected_result=None, 
        description="Transposição de Matriz inválida (None)",
        expect_error=True, 
        error_message_contains="Matriz para transposição deve ser uma lista de listas" # Mensagem da validação
    )
    
    # Teste 9: Matriz de entrada é [[]] (lista contendo uma lista vazia).
    run_transpose_test_case(
        matrix=[[]], 
        expected_result=None, 
        description="Transposição de Matriz inválida (contém linha vazia [[]])",
        expect_error=True, 
        error_message_contains="Matriz para transposição contém linha(s) vazia(s)" # Mensagem da validação
    )
    
    # Teste 10: Matriz com número inconsistente de colunas entre as linhas.
    run_transpose_test_case(
        matrix=[[1,2],[3]], # Linha 0 tem 2 col, Linha 1 tem 1 col
        expected_result=None, 
        description="Transposição de Matriz com contagem de colunas inconsistente",
        expect_error=True, 
        error_message_contains="mesmo número de colunas" # Mensagem da validação
    )

    print_test_footer("transpose_matrix.py", test_count, passed_count)

if __name__ == "__main__":
    test_transposicao_matriz()