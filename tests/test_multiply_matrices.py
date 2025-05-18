# calculadora_matrizes/tests/test_multiply_matrices.py
from test_utils import format_matrix_for_log, are_matrices_equal, generate_matrix, print_test_header, print_test_footer
from logic.multiply_matrices import multiply_matrices

test_count = 0
passed_count = 0

def run_multiply_test_case(m_a, m_b, expected_result, description, expect_error=False, error_message_contains=None):
    global test_count, passed_count
    test_count += 1
    print(f"\n--- Teste: {description} ---")
    log_details = [format_matrix_for_log(m_a, "Matriz A"), format_matrix_for_log(m_b, "Matriz B")]

    try:
        result = multiply_matrices(m_a, m_b)
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

def test_multiplicacao_matrizes():
    global test_count, passed_count
    test_count = 0
    passed_count = 0
    print_test_header("multiply_matrices.py")

    # --- Casos Válidos ---
    run_multiply_test_case([[2]], [[3]], [[6]], "Multiplicação 1x1")
    run_multiply_test_case([[1, 2]], [[3], [4]], [[11]], "Multiplicação (1x2) * (2x1) -> (1x1)") # 1*3 + 2*4 = 3+8=11
    run_multiply_test_case([[1], [2]], [[3, 4]], [[3, 4], [6, 8]], "Multiplicação (2x1) * (1x2) -> (2x2)")
    
    m_a_2x2 = [[1, 2], [3, 4]]
    m_b_2x2 = [[2, 0], [1, 2]]
    exp_2x2 = [[4, 4], [10, 8]] # (1*2+2*1), (1*0+2*2) | (3*2+4*1), (3*0+4*2)
    run_multiply_test_case(m_a_2x2, m_b_2x2, exp_2x2, "Multiplicação de matrizes 2x2")

    m_a_2x3 = [[1, 0, 2], [0, 3, -1]]
    m_b_3x2 = [[1, 1], [0, 2], [2, 0]]
    exp_2x2_from_2x3_3x2 = [[5, 1], [-2, 6]] # (1*1+0*0+2*2), (1*1+0*2+2*0) | (0*1+3*0-1*2), (0*1+3*2-1*0)
    run_multiply_test_case(m_a_2x3, m_b_3x2, exp_2x2_from_2x3_3x2, "Multiplicação (2x3) * (3x2) -> (2x2)")

    # Multiplicação por matriz identidade
    ident_3x3 = [[1,0,0],[0,1,0],[0,0,1]]
    m_a_3x3 = [[1,2,3],[4,5,6],[7,8,9]]
    run_multiply_test_case(m_a_3x3, ident_3x3, m_a_3x3, "Multiplicação por matriz identidade I (A*I=A)")
    run_multiply_test_case(ident_3x3, m_a_3x3, m_a_3x3, "Multiplicação por matriz identidade I (I*A=A)")
    
    # Multiplicação por matriz de zeros
    zeros_2x2 = [[0,0],[0,0]]
    run_multiply_test_case(m_a_2x2, zeros_2x2, zeros_2x2, "Multiplicação por matriz de zeros (A*0=0)")

    # Matriz 5x5 (A) * 5x2 (B) -> 5x2 (Resultado)
    m_a_5x5 = generate_matrix(5,5, lambda r,c: 1 if r==c else 0) # Identidade
    m_b_5x2 = generate_matrix(5,2, lambda r,c: r+c+1)
    run_multiply_test_case(m_a_5x5, m_b_5x2, m_b_5x2, "Multiplicação Matriz Identidade 5x5 * 5x2")

    # Matriz 7x10 (A) * 10x3 (B) -> 7x3 (Resultado)
    # Para matrizes grandes, verificar as dimensões do resultado pode ser um teste inicial
    # Calcular o resultado exato para log pode ser verboso, então podemos omitir 'expected_result'
    # ou calcular um resultado conhecido (e.g. A * I)
    m_a_7x10 = generate_matrix(7,10, lambda r,c: 1)
    m_b_10x3 = generate_matrix(10,3, lambda r,c: 2)
    exp_7x3_val10x2 = [[20 for _ in range(3)] for _ in range(7)] # 10 colunas de A, cada elemento 1. 10 linhas de B, cada elemento 2. Somatório de 1*2, 10 vezes.
    run_multiply_test_case(m_a_7x10, m_b_10x3, exp_7x3_val10x2, "Multiplicação Matriz 7x10 (1s) * 10x3 (2s)")


    # --- Casos de Erro Esperados ---
    run_multiply_test_case([[1,2]], [[1,2]], None, "Multiplicação com dimensões incompatíveis (col A != lin B)",
                           expect_error=True, error_message_contains="colunas da Matriz A deve ser igual")
    run_multiply_test_case([[1],[2]], [[1,2],[3,4],[5,6]], None, "Multiplicação com dimensões incompatíveis (col A != lin B, mais linhas em B)",
                           expect_error=True, error_message_contains="colunas da Matriz A deve ser igual")
    run_multiply_test_case(None, [[1]], None, "Multiplicação com Matriz A como None",
                           expect_error=True, error_message_contains="deve ser uma lista de listas")
    run_multiply_test_case([[]], [[1]], None, "Multiplicação com Matriz A como [[]]",
                           expect_error=True, error_message_contains="linha(s) vazia(s)")


    print_test_footer("multiply_matrices.py", test_count, passed_count)

if __name__ == "__main__":
    test_multiplicacao_matrizes()