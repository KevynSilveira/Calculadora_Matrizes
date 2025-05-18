# calculadora_matrizes/tests/test_transpose_matrix.py
from test_utils import format_matrix_for_log, are_matrices_equal, generate_matrix, print_test_header, print_test_footer
from logic.transpose_matrix import transpose_matrix

test_count = 0
passed_count = 0

def run_transpose_test_case(matrix, expected_result, description, expect_error=False, error_message_contains=None):
    global test_count, passed_count
    test_count += 1
    print(f"\n--- Teste: {description} ---")
    log_details = [format_matrix_for_log(matrix, "Matriz Original")]

    try:
        result = transpose_matrix(matrix)
        if expect_error:
            print(f"[FALHA] - {description}")
            log_details.append("  Status: Erro era esperado, mas a operação foi concluída.")
            log_details.append(format_matrix_for_log(result, "Resultado Obtido"))
            if error_message_contains: log_details.append(f"  Erro Esperado (contendo): '{error_message_contains}'")
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
                log_details.append(f"  Status: Erro esperado ({error_message_contains}), mas msg difere: ValueError: {ve}")
        else:
            print(f"[FALHA] - {description}")
            log_details.append(f"  Status: Erro inesperado: ValueError: {ve}")
            log_details.append(format_matrix_for_log(expected_result, "Resultado Esperado (se aplicável)"))
    except Exception as e:
        print(f"[FALHA] - {description}")
        log_details.append(f"  Status: Exceção inesperada {type(e).__name__}: {e}")
        log_details.append(format_matrix_for_log(expected_result, "Resultado Esperado (se aplicável)"))
    
    print("  Log da Conta:")
    for detail in log_details: print(detail)

def test_transposicao_matriz():
    global test_count, passed_count
    test_count = 0
    passed_count = 0
    print_test_header("transpose_matrix.py")

    # --- Casos Válidos ---
    run_transpose_test_case([[1]], [[1]], "Transposição de matriz 1x1")
    run_transpose_test_case([[1, 2, 3]], [[1], [2], [3]], "Transposição de matriz linha (1x3) para coluna (3x1)")
    run_transpose_test_case([[1], [2], [3]], [[1, 2, 3]], "Transposição de matriz coluna (3x1) para linha (1x3)")
    
    m_2x2 = [[1, 2], [3, 4]]
    exp_2x2_t = [[1, 3], [2, 4]]
    run_transpose_test_case(m_2x2, exp_2x2_t, "Transposição de matriz 2x2")

    m_2x3 = [[1, 2, 3], [4, 5, 6]]
    exp_3x2_t = [[1, 4], [2, 5], [3, 6]]
    run_transpose_test_case(m_2x3, exp_3x2_t, "Transposição de matriz 2x3 para 3x2")

    # Transpor duas vezes retorna a original
    run_transpose_test_case(transpose_matrix(m_2x3), m_2x3, "Transposição dupla (T(T(A)) = A) para 2x3")

    m_10x2 = generate_matrix(10, 2, lambda r, c: r * 10 + c)
    # Esperado: Troca r e c na função geradora para a transposta
    exp_2x10_t = generate_matrix(2, 10, lambda r, c: c * 10 + r)
    run_transpose_test_case(m_10x2, exp_2x10_t, "Transposição de matriz 10x2 (gerada)")
    
    # --- Casos de Erro Esperados ---
    run_transpose_test_case(None, None, "Transposição de Matriz None",
                              expect_error=True, error_message_contains="Matriz para transposição")
    run_transpose_test_case([[]], None, "Transposição de Matriz [[]]",
                              expect_error=True, error_message_contains="Matriz para transposição")
    run_transpose_test_case([[1,2],[3]], None, "Transposição de Matriz com linhas de tamanhos diferentes",
                              expect_error=True, error_message_contains="mesmo número de colunas")

    print_test_footer("transpose_matrix.py", test_count, passed_count)

if __name__ == "__main__":
    test_transposicao_matriz()