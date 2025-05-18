# calculadora_matrizes/tests/test_subtract_matrices.py
from test_utils import format_matrix_for_log, are_matrices_equal, generate_matrix, print_test_header, print_test_footer
from logic.subtract_matrices import subtract_matrices

test_count = 0
passed_count = 0

def run_subtract_test_case(m_a, m_b, expected_result, description, expect_error=False, error_message_contains=None):
    global test_count, passed_count
    test_count += 1
    
    print(f"\n--- Teste: {description} ---")
    log_details = [
        format_matrix_for_log(m_a, "Matriz A"),
        format_matrix_for_log(m_b, "Matriz B")
    ]

    try:
        result = subtract_matrices(m_a, m_b)
        
        if expect_error:
            print(f"[FALHA] - {description}")
            log_details.append("  Status: Erro era esperado, mas a operação foi concluída.")
            log_details.append(format_matrix_for_log(result, "Resultado Obtido"))
            if error_message_contains:
                 log_details.append(f"  Erro Esperado (contendo): '{error_message_contains}'")
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

    print("  Log da Conta:")
    for detail in log_details:
        print(detail)

def test_subtracao_matrizes():
    global test_count, passed_count
    test_count = 0
    passed_count = 0
    
    print_test_header("subtract_matrices.py")

    # --- Casos Válidos ---
    run_subtract_test_case([[5]], [[2]], [[3]], "Subtração de matrizes 1x1")
    run_subtract_test_case([[1]], [[5]], [[-4]], "Subtração de matrizes 1x1 resultando em negativo")

    m_a_2x2 = [[10, 20], [30, 40]]
    m_b_2x2 = [[1, 2], [3, 4]]
    exp_2x2 = [[9, 18], [27, 36]]
    run_subtract_test_case(m_a_2x2, m_b_2x2, exp_2x2, "Subtração de matrizes 2x2")

    m_a_2x3 = [[1, 0, -1], [2, -2, 5]]
    m_b_2x3 = [[3, 2, 1],  [0,  4, 2]]
    exp_2x3 = [[-2, -2, -2], [2, -6, 3]]
    run_subtract_test_case(m_a_2x3, m_b_2x3, exp_2x3, "Subtração de matrizes 2x3")
    
    m_a_zeros = [[0,0],[0,0]]
    m_b_id = [[1,2],[3,4]]
    exp_zero_sub = [[-1,-2],[-3,-4]]
    run_subtract_test_case(m_a_zeros, m_b_id, exp_zero_sub, "Subtração de matriz de zeros por outra (0 - B = -B)")
    run_subtract_test_case(m_b_id, m_a_zeros, m_b_id, "Subtração por matriz de zeros (B - 0 = B)")

    m_a_float = [[0.5, 1.5], [2.0, -0.5]]
    m_b_float = [[0.2, 0.5], [-1.0, 0.8]]
    exp_float = [[0.3, 1.0], [3.0, -1.3]]
    run_subtract_test_case(m_a_float, m_b_float, exp_float, "Subtração de matrizes com floats")

    m_a_10x10 = generate_matrix(10, 10, lambda r, c: r + c + 5)
    m_b_10x10 = generate_matrix(10, 10, lambda r, c: 1)
    exp_10x10 = generate_matrix(10, 10, lambda r, c: r + c + 4)
    run_subtract_test_case(m_a_10x10, m_b_10x10, exp_10x10, "Subtração de matrizes 10x10 (geradas)")

    # --- Casos de Erro Esperados ---
    run_subtract_test_case([[1,2]], [[1],[2]], None, "Subtração com dimensões incompatíveis", 
                      expect_error=True, error_message_contains="mesmas dimensões")
    run_subtract_test_case(None, [[1]], None, "Subtração com Matriz A como None",
                      expect_error=True, error_message_contains="deve ser uma lista de listas")

    print_test_footer("subtract_matrices.py", test_count, passed_count)

if __name__ == "__main__":
    test_subtracao_matrizes()