# calculadora_matrizes/tests/test_add_matrices.py
from test_utils import format_matrix_for_log, are_matrices_equal, generate_matrix, print_test_header, print_test_footer
from logic.add_matrices import add_matrices # Importa a função a ser testada

# Contador global para os testes
test_count = 0
passed_count = 0

def run_add_test_case(m_a, m_b, expected_result, description, expect_error=False, error_message_contains=None):
    """Executa um caso de teste para add_matrices e registra o resultado."""
    global test_count, passed_count
    test_count += 1
    
    print(f"\n--- Teste: {description} ---")
    log_details = [
        format_matrix_for_log(m_a, "Matriz A"),
        format_matrix_for_log(m_b, "Matriz B")
    ]

    try:
        result = add_matrices(m_a, m_b)
        
        if expect_error:
            print(f"[FALHA] - {description}")
            log_details.append("  Status: Erro era esperado, mas a operação foi concluída.")
            log_details.append(format_matrix_for_log(result, "Resultado Obtido"))
            if error_message_contains:
                 log_details.append(f"  Erro Esperado (contendo): '{error_message_contains}'")
        elif are_matrices_equal(result, expected_result):
            print(f"[OK] - {description}")
            passed_count += 1
            return # Teste passou, não precisa de log detalhado
        else:
            print(f"[FALHA] - {description}")
            log_details.append(format_matrix_for_log(expected_result, "Resultado Esperado"))
            log_details.append(format_matrix_for_log(result, "Resultado Obtido"))

    except ValueError as ve:
        if expect_error:
            if error_message_contains is None or error_message_contains.lower() in str(ve).lower():
                print(f"[OK] - {description} (Erro esperado capturado: {ve})")
                passed_count += 1
                return
            else:
                print(f"[FALHA] - {description}")
                log_details.append(f"  Status: Erro esperado, mas a mensagem não correspondeu.")
                log_details.append(f"  Erro Obtido: ValueError: {ve}")
                log_details.append(f"  Esperado que a mensagem de erro contivesse: '{error_message_contains}'")
        else:
            print(f"[FALHA] - {description}")
            log_details.append(f"  Status: Erro inesperado durante a operação.")
            log_details.append(format_matrix_for_log(expected_result, "Resultado Esperado (se aplicável)"))
            log_details.append(f"  Erro: ValueError: {ve}")
            
    except Exception as e:
        print(f"[FALHA] - {description}")
        log_details.append(f"  Status: Exceção inesperada do tipo {type(e).__name__}.")
        log_details.append(format_matrix_for_log(expected_result, "Resultado Esperado (se aplicável)"))
        log_details.append(f"  Erro: {e}")

    # Imprime o log detalhado em caso de falha ou se um erro era esperado mas não ocorreu
    print("  Log da Conta:")
    for detail in log_details:
        print(detail)

def test_soma_matrizes():
    """Define e executa todos os casos de teste para a soma de matrizes."""
    global test_count, passed_count
    test_count = 0
    passed_count = 0
    
    print_test_header("add_matrices.py")

    # --- Casos Válidos ---
    # 1x1
    run_add_test_case([[1]], [[2]], [[3]], "Soma de matrizes 1x1")
    run_add_test_case([[-5]], [[5]], [[0]], "Soma de matrizes 1x1 com negativos")

    # 2x2
    m_a_2x2 = [[1, 2], [3, 4]]
    m_b_2x2 = [[5, 6], [7, 8]]
    exp_2x2 = [[6, 8], [10, 12]]
    run_add_test_case(m_a_2x2, m_b_2x2, exp_2x2, "Soma de matrizes 2x2")

    # 2x3
    m_a_2x3 = [[1, 0, -1], [2, -2, 5]]
    m_b_2x3 = [[3, 2, 1],  [0,  4, 2]]
    exp_2x3 = [[4, 2, 0],  [2,  2, 7]]
    run_add_test_case(m_a_2x3, m_b_2x3, exp_2x3, "Soma de matrizes 2x3")

    # 3x1 (vetores coluna)
    m_a_3x1 = [[10], [20], [30]]
    m_b_3x1 = [[-5], [-10], [-15]]
    exp_3x1 = [[5], [10], [15]]
    run_add_test_case(m_a_3x1, m_b_3x1, exp_3x1, "Soma de matrizes 3x1 (vetores coluna)")
    
    # Matrizes com Zeros
    m_a_zeros = [[0,0],[0,0]]
    m_b_id = [[1,2],[3,4]]
    run_add_test_case(m_a_zeros, m_b_id, m_b_id, "Soma com matriz de zeros")

    # Matrizes com Floats
    m_a_float = [[0.5, 1.5], [2.0, -0.5]]
    m_b_float = [[0.5, 0.5], [-1.0, 0.5]]
    exp_float = [[1.0, 2.0], [1.0, 0.0]]
    run_add_test_case(m_a_float, m_b_float, exp_float, "Soma de matrizes com floats")

    # Matriz 5x5 (gerada)
    m_a_5x5 = generate_matrix(5, 5, lambda r, c: 1) # Todos 1s
    m_b_5x5 = generate_matrix(5, 5, lambda r, c: 2) # Todos 2s
    exp_5x5 = generate_matrix(5, 5, lambda r, c: 3) # Todos 3s
    run_add_test_case(m_a_5x5, m_b_5x5, exp_5x5, "Soma de matrizes 5x5 (todos 1s + todos 2s)")
    
    # Matriz 10x10 (gerada)
    m_a_10x10 = generate_matrix(10, 10, lambda r, c: r + c)
    m_b_10x10 = generate_matrix(10, 10, lambda r, c: 1)
    exp_10x10 = generate_matrix(10, 10, lambda r, c: r + c + 1)
    run_add_test_case(m_a_10x10, m_b_10x10, exp_10x10, "Soma de matrizes 10x10 (geradas)")

    # --- Casos de Erro Esperados ---
    # Dimensões diferentes
    run_add_test_case([[1,2]], [[1],[2]], None, "Soma com dimensões incompatíveis (linhas)", 
                      expect_error=True, error_message_contains="mesmas dimensões")
    run_add_test_case([[1,2],[3,4]], [[1,2]], None, "Soma com dimensões incompatíveis (colunas)", 
                      expect_error=True, error_message_contains="mesmas dimensões")

    # Matrizes inválidas (None, string, etc.) - a validação deve pegar isso
    run_add_test_case(None, [[1]], None, "Soma com Matriz A como None",
                      expect_error=True, error_message_contains="deve ser uma lista de listas")
    run_add_test_case([[1]], "[[1]]", None, "Soma com Matriz B como string",
                      expect_error=True, error_message_contains="deve ser uma lista de listas")
    run_add_test_case([[]], [[1]], None, "Soma com Matriz A como [[]]",
                      expect_error=True, error_message_contains="linha(s) vazia(s)")
    run_add_test_case([[1,2],[3]], [[1,1],[1,1]], None, "Soma com Matriz A com linhas de tamanhos diferentes",
                      expect_error=True, error_message_contains="mesmo número de colunas")


    print_test_footer("add_matrices.py", test_count, passed_count)


if __name__ == "__main__":
    test_soma_matrizes()