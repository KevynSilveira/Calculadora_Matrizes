# calculadora_matrizes/tests/test_determinant.py
from test_utils import format_matrix_for_log, are_matrices_equal, generate_matrix, print_test_header, print_test_footer, TOLERANCE
from logic.determinant import determinant
import math # Para isclose em verificações específicas

test_count = 0
passed_count = 0

def run_determinant_test_case(matrix, expected_determinant, description, expect_error=False, error_message_contains=None):
    global test_count, passed_count
    test_count += 1
    print(f"\n--- Teste: {description} ---")
    log_details = [format_matrix_for_log(matrix, "Matriz")]

    try:
        result = determinant(matrix)
        if expect_error:
            print(f"[FALHA] - {description}")
            log_details.append(f"  Status: Erro era esperado, mas a operação foi concluída. Obtido: {result}")
            if error_message_contains: log_details.append(f"  Erro Esperado (contendo): '{error_message_contains}'")
        elif math.isclose(result, expected_determinant, rel_tol=TOLERANCE, abs_tol=TOLERANCE):
            print(f"[OK] - {description}")
            passed_count += 1
            return
        else:
            print(f"[FALHA] - {description}")
            log_details.append(f"  Resultado Esperado: {expected_determinant}")
            log_details.append(f"  Resultado Obtido: {result}")
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
            if not expect_error : log_details.append(f"  Resultado Esperado: {expected_determinant}")
    except Exception as e:
        print(f"[FALHA] - {description}")
        log_details.append(f"  Status: Exceção inesperada {type(e).__name__}: {e}")
        if not expect_error : log_details.append(f"  Resultado Esperado: {expected_determinant}")
    
    print("  Log da Conta:")
    for detail in log_details: print(detail)

def test_determinantes():
    global test_count, passed_count
    test_count = 0
    passed_count = 0
    print_test_header("determinant.py")

    # --- Casos Válidos ---
    run_determinant_test_case([[5]], 5, "Determinante de matriz 1x1")
    run_determinant_test_case([[-10]], -10, "Determinante de matriz 1x1 negativa")
    
    run_determinant_test_case([[1, 2], [3, 4]], -2, "Determinante de matriz 2x2 (1*4 - 2*3 = -2)")
    run_determinant_test_case([[0, 0], [3, 4]], 0, "Determinante de matriz 2x2 com linha de zeros")
    run_determinant_test_case([[6, 1], [0, 4]], 24, "Determinante de matriz triangular inferior 2x2")

    m_3x3 = [[1, 2, 3], [0, 1, 4], [5, 6, 0]]
    # Det = 1*(1*0 - 4*6) - 2*(0*0 - 4*5) + 3*(0*6 - 1*5)
    #     = 1*(-24) - 2*(-20) + 3*(-5)
    #     = -24 + 40 - 15 = 1
    run_determinant_test_case(m_3x3, 1, "Determinante de matriz 3x3")

    m_3x3_diag = [[2,0,0],[0,3,0],[0,0,4]]
    run_determinant_test_case(m_3x3_diag, 24, "Determinante de matriz diagonal 3x3 (produto da diagonal)")

    m_3x3_singular = [[1,2,3],[2,4,6],[7,8,9]] # Linha 2 = 2 * Linha 1
    run_determinant_test_case(m_3x3_singular, 0, "Determinante de matriz 3x3 singular (det=0)")

    # Matriz 4x4 (exemplo da Wikipedia para Sarrus 3x3 não aplicável, cofator)
    # | 1  2  0  1 |
    # | 0  3  1  2 |
    # | -1 0  2  -1 |
    # | 2  1  -1 0 |
    # Expansão pela primeira linha:
    # 1 * det([[3,1,2],[0,2,-1],[1,-1,0]])  = 1 * (3(0-1) - 1(0-(-1)) + 2(0-2)) = 1 * (3(-1) -1(1) + 2(-2)) = 1 * (-3 -1 -4) = -8
    # -2 * det([[0,1,2],[-1,2,-1],[2,-1,0]]) = -2 * (0 - 1(0-(-2)) + 2(1-4)) = -2 * (-1(2) + 2(-3)) = -2 * (-2 -6) = -2 * (-8) = 16
    # +0 * det(...) = 0
    # -1 * det([[0,3,1],[-1,0,2],[2,1,-1]]) = -1 * (0 - 3(1-4) + 1(-1-0)) = -1 * (-3(-3) + 1(-1)) = -1 * (9 - 1) = -1 * (8) = -8
    # Total: -8 + 16 + 0 - 8 = 0
    m_4x4 = [[1,2,0,1], [0,3,1,2], [-1,0,2,-1], [2,1,-1,0]]
    run_determinant_test_case(m_4x4, 0, "Determinante de matriz 4x4 (exemplo conhecido)")
    
    # Para matrizes 10x10, o cálculo manual é impraticável.
    # Testar propriedades: det(I) = 1
    ident_10x10 = generate_matrix(10, 10, lambda r,c: 1 if r==c else 0)
    run_determinant_test_case(ident_10x10, 1, "Determinante de matriz identidade 10x10")
    
    # --- Casos de Erro Esperados ---
    run_determinant_test_case([[1,2],[3,4],[5,6]], None, "Determinante de matriz não quadrada (3x2)", 
                              expect_error=True, error_message_contains="matriz deve ser quadrada")
    run_determinant_test_case(None, None, "Determinante de Matriz None",
                              expect_error=True, error_message_contains="Matriz para determinante")
    run_determinant_test_case([[]], None, "Determinante de Matriz [[]]",
                              expect_error=True, error_message_contains="Matriz para determinante")

    print_test_footer("determinant.py", test_count, passed_count)

if __name__ == "__main__":
    test_determinantes()