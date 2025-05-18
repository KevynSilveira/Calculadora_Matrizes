# calculadora_matrizes/tests/test_scalar_multiply.py
from test_utils import format_matrix_for_log, are_matrices_equal, generate_matrix, print_test_header, print_test_footer
from logic.scalar_multiply import scalar_multiply

test_count = 0
passed_count = 0

def run_scalar_mult_test_case(matrix, scalar, expected_result, description, expect_error=False, error_message_contains=None):
    global test_count, passed_count
    test_count += 1
    print(f"\n--- Teste: {description} ---")
    log_details = [format_matrix_for_log(matrix, "Matriz"), f"    Escalar: {scalar}"]

    try:
        result = scalar_multiply(matrix, scalar)
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

def test_multiplicacao_escalar():
    global test_count, passed_count
    test_count = 0
    passed_count = 0
    print_test_header("scalar_multiply.py")

    # --- Casos Válidos ---
    run_scalar_mult_test_case([[2]], 3, [[6]], "Multiplicação escalar 1x1 por inteiro")
    run_scalar_mult_test_case([[1, 2], [3, 4]], 2, [[2, 4], [6, 8]], "Multiplicação escalar 2x2 por inteiro")
    run_scalar_mult_test_case([[1, 2], [3, 4]], 0, [[0, 0], [0, 0]], "Multiplicação escalar por zero")
    run_scalar_mult_test_case([[10, 20], [30, 0]], -1, [[-10, -20], [-30, 0]], "Multiplicação escalar por -1")
    run_scalar_mult_test_case([[2, 4], [6, 8]], 0.5, [[1, 2], [3, 4]], "Multiplicação escalar por float (0.5)")
    
    m_10x10 = generate_matrix(10, 10, lambda r, c: r + c + 1)
    exp_10x10_x3 = generate_matrix(10, 10, lambda r, c: (r + c + 1) * 3)
    run_scalar_mult_test_case(m_10x10, 3, exp_10x10_x3, "Multiplicação escalar matriz 10x10 por 3")

    # --- Casos de Erro Esperados ---
    # A função scalar_multiply espera um escalar numérico, a GUI deve tratar a entrada de escalar não numérico.
    # Aqui testamos a lógica da função em si, que não valida o tipo do escalar, Python faria isso.
    # O principal erro que a validação da função pega é a matriz inválida.
    run_scalar_mult_test_case(None, 2, None, "Multiplicação escalar com Matriz como None",
                              expect_error=True, error_message_contains="Matriz para multiplicação por escalar") # Mensagem de validation_utils
    run_scalar_mult_test_case([[]], 2, None, "Multiplicação escalar com Matriz como [[]]",
                              expect_error=True, error_message_contains="Matriz para multiplicação por escalar")
    run_scalar_mult_test_case("matriz", 2, None, "Multiplicação escalar com Matriz como string",
                              expect_error=True, error_message_contains="Matriz para multiplicação por escalar")

    print_test_footer("scalar_multiply.py", test_count, passed_count)

if __name__ == "__main__":
    test_multiplicacao_escalar()