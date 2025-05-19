# calculadora_matrizes/tests/test_scalar_multiply.py

# Importa utilitários de teste:
# - format_matrix_for_log: Para exibir matrizes e escalares de forma legível.
# - are_matrices_equal: Para comparar a matriz resultado com a esperada.
# - generate_matrix: Para criar matrizes de teste maiores.
# - print_test_header/footer: Para formatar o output do conjunto de testes.
from test_utils import format_matrix_for_log, are_matrices_equal, generate_matrix, print_test_header, print_test_footer
# Importa a função de multiplicação por escalar que será testada.
from logic.scalar_multiply import scalar_multiply

# Contadores globais para rastrear estatísticas dos testes.
test_count = 0
passed_count = 0

def run_scalar_mult_test_case(matrix, scalar, expected_result, description, 
                              expect_error=False, error_message_contains=None):
    """
    Executa um único caso de teste para a função scalar_multiply.

    Esta função irá:
    1. Chamar 'scalar_multiply(matrix, scalar)'.
    2. Se um erro é esperado (expect_error=True):
        a. Verificar se um ValueError (da validação da matriz) foi levantado.
        b. Se sim, verificar se a mensagem de erro contém 'error_message_contains'.
    3. Se nenhum erro é esperado:
        a. Comparar o resultado obtido com 'expected_result' usando 'are_matrices_equal'.
    4. Imprimir o status ([OK] ou [FALHA]) e um log detalhado em caso de falha.

    Args:
        matrix (list[list[float]] or None): A matriz a ser multiplicada.
        scalar (float or int): O valor escalar pelo qual multiplicar.
        expected_result (list[list[float]] or None): A matriz esperada como resultado.
                                                    None se um erro é esperado.
        description (str): Descrição do caso de teste.
        expect_error (bool): True se uma exceção ValueError é esperada (da validação da matriz).
        error_message_contains (str or None): Substring esperada na mensagem de erro para ValueErrors.
    """
    global test_count, passed_count
    test_count += 1
    print(f"\n--- Teste: {description} ---")
    log_details = [
        format_matrix_for_log(matrix, "Matriz de Entrada"), 
        f"    Escalar de Entrada: {scalar}" 
    ]

    try:
        result = scalar_multiply(matrix, scalar)
        
        if expect_error:
            print(f"[FALHA] - {description}")
            log_details.append("  Status: Um erro era esperado, mas a operação foi concluída sem erros.")
            log_details.append(format_matrix_for_log(result, "Resultado Obtido (Inesperado)"))
            if error_message_contains: 
                log_details.append(f"  Detalhe do Erro Esperado: A mensagem deveria conter '{error_message_contains}'")
        elif are_matrices_equal(result, expected_result):
            print(f"[OK] - {description}")
            passed_count += 1
            return 
        else:
            print(f"[FALHA] - {description}")
            log_details.append(format_matrix_for_log(expected_result, "Resultado Esperado"))
            log_details.append(format_matrix_for_log(result, "Resultado Obtido"))

    except ValueError as ve: 
        if expect_error:
            if error_message_contains is None or error_message_contains.lower() in str(ve).lower():
                print(f"[OK] - {description} (Erro esperado ValueError corretamente capturado: {ve})")
                passed_count += 1
                return
            else:
                print(f"[FALHA] - {description}")
                log_details.append(f"  Status: Um erro ValueError era esperado, mas sua mensagem não correspondeu.")
                log_details.append(f"  Mensagem de Erro Obtida: ValueError: {ve}")
                log_details.append(f"  Esperado que a Mensagem Contivesse: '{error_message_contains}'")
        else:
            print(f"[FALHA] - {description}")
            log_details.append(f"  Status: Erro ValueError inesperado durante a operação.")
            if not expect_error and expected_result is not None: 
                log_details.append(format_matrix_for_log(expected_result, "Resultado Esperado (se aplicável)"))
            log_details.append(f"  Detalhe do Erro: ValueError: {ve}")
            
    except Exception as e: 
        print(f"[FALHA] - {description}")
        log_details.append(f"  Status: Uma exceção totalmente inesperada do tipo {type(e).__name__} ocorreu.")
        if not expect_error and expected_result is not None:
            log_details.append(format_matrix_for_log(expected_result, "Resultado Esperado (se aplicável)"))
        log_details.append(f"  Detalhe do Erro: {e}")
    
    print("  Log Detalhado da Operação:")
    for detail in log_details: print(detail)

def test_multiplicacao_escalar():
    """
    Define e executa uma suíte de casos de teste para a função scalar_multiply.
    """
    global test_count, passed_count
    test_count = 0
    passed_count = 0
    print_test_header("scalar_multiply.py")

    # --- Seção: Casos de Teste Válidos ---
    run_scalar_mult_test_case(matrix=[[2]], scalar=3, expected_result=[[6]], 
                              description="Multiplicação escalar: Matriz 1x1 por inteiro")
    
    run_scalar_mult_test_case(matrix=[[1, 2], [3, 4]], scalar=2, expected_result=[[2, 4], [6, 8]], 
                              description="Multiplicação escalar: Matriz 2x2 por inteiro")
    
    run_scalar_mult_test_case(matrix=[[1, 2], [3, 4]], scalar=0, expected_result=[[0, 0], [0, 0]], 
                              description="Multiplicação escalar: Por escalar zero")
    
    run_scalar_mult_test_case(matrix=[[10, 20], [30, 0]], scalar=-1, expected_result=[[-10, -20], [-30, 0]], 
                              description="Multiplicação escalar: Por escalar -1")
    
    run_scalar_mult_test_case(matrix=[[2, 4], [6, 8]], scalar=0.5, expected_result=[[1.0, 2.0], [3.0, 4.0]], 
                              description="Multiplicação escalar: Por escalar float (0.5)")
    
    m_10x10 = generate_matrix(10, 10, lambda r, c: r + c + 1) 
    exp_10x10_x3 = generate_matrix(10, 10, lambda r, c: (r + c + 1) * 3) 
    run_scalar_mult_test_case(m_10x10, 3, exp_10x10_x3, 
                              description="Multiplicação escalar: Matriz 10x10 gerada por escalar 3")

    # --- Seção: Casos de Teste de Erro (para validação da matriz de entrada) ---
    run_scalar_mult_test_case(matrix=None, scalar=2, expected_result=None, 
                              description="Multiplicação escalar: Matriz de entrada é None",
                              expect_error=True, 
                              error_message_contains="Matriz para multiplicação por escalar deve ser uma lista de listas") 
    
    run_scalar_mult_test_case(matrix=[[]], scalar=2, expected_result=None, 
                              description="Multiplicação escalar: Matriz de entrada é [[]]",
                              expect_error=True, 
                              error_message_contains="Matriz para multiplicação por escalar contém linha(s) vazia(s)")
    
    run_scalar_mult_test_case(matrix="matriz", scalar=2, expected_result=None, 
                              description="Multiplicação escalar: Matriz de entrada é uma string",
                              expect_error=True, 
                              error_message_contains="Matriz para multiplicação por escalar deve ser uma lista de listas")

    print_test_footer("scalar_multiply.py", test_count, passed_count)

if __name__ == "__main__":
    test_multiplicacao_escalar()