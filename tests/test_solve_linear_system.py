# calculadora_matrizes/tests/test_solve_linear_system.py
from test_utils import format_matrix_for_log, are_matrices_equal, print_test_header, print_test_footer
from logic.solve_linear_system import solve_linear_system_inverse
from logic.multiply_matrices import multiply_matrices # Para verificar A * X = B

test_count = 0
passed_count = 0

def run_solve_system_test_case(matrix_a, vector_b, expected_solution_x, description, 
                               expect_error=False, error_message_contains=None, check_ax_eq_b=True):
    global test_count, passed_count
    test_count += 1
    print(f"\n--- Teste: {description} ---")
    log_details = [
        format_matrix_for_log(matrix_a, "Matriz A (Coeficientes)"),
        format_matrix_for_log(vector_b, "Vetor B (Termos Independentes)")
    ]

    try:
        solution_x = solve_linear_system_inverse(matrix_a, vector_b)
        
        if expect_error:
            print(f"[FALHA] - {description}")
            log_details.append(f"  Status: Erro era esperado, mas a operação foi concluída.")
            log_details.append(format_matrix_for_log(solution_x, "Solução X Obtida"))
            if error_message_contains: log_details.append(f"  Erro Esperado (contendo): '{error_message_contains}'")
        else:
            passed_this_test = True
            if not are_matrices_equal(solution_x, expected_solution_x):
                passed_this_test = False
                log_details.append(format_matrix_for_log(expected_solution_x, "Solução X Esperada"))
                log_details.append(format_matrix_for_log(solution_x, "Solução X Calculada"))
            
            if check_ax_eq_b and passed_this_test and solution_x is not None :
                # Verificar se A * X_calculado = B
                product_ax = multiply_matrices(matrix_a, solution_x)
                if not are_matrices_equal(product_ax, vector_b):
                    passed_this_test = False
                    log_details.append(format_matrix_for_log(product_ax, "Produto A * X_calculado (Obtido)"))
                    log_details.append(format_matrix_for_log(vector_b, "Vetor B Original (Esperado)"))
                    log_details.append("  Verificação A * X = B falhou.")
            
            if passed_this_test:
                print(f"[OK] - {description}")
                passed_count += 1
                return
            else:
                 print(f"[FALHA] - {description}")
                 # Logs já adicionados

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
            if not expect_error: log_details.append(format_matrix_for_log(expected_solution_x, "Solução X Esperada (se aplicável)"))
    except Exception as e:
        print(f"[FALHA] - {description}")
        log_details.append(f"  Status: Exceção inesperada {type(e).__name__}: {e}")
        if not expect_error: log_details.append(format_matrix_for_log(expected_solution_x, "Solução X Esperada (se aplicável)"))
    
    print("  Log da Conta:")
    for detail in log_details: print(detail)


def test_resolucao_sistemas():
    global test_count, passed_count
    test_count = 0
    passed_count = 0
    print_test_header("solve_linear_system.py")

    # --- Casos Válidos ---
    # Sistema 1x1: 5x = 10 => x = 2
    run_solve_system_test_case([[5]], [[10]], [[2]], "Sistema 1x1 simples")

    # Sistema 2x2:
    # 2x + 3y = 8
    #  x +  y = 3  => y = 3-x => 2x + 3(3-x) = 8 => 2x + 9 - 3x = 8 => -x = -1 => x = 1, y = 2
    # A = [[2,3],[1,1]], B = [[8],[3]], X_esperado = [[1],[2]]
    m_a_2x2 = [[2,3],[1,1]]
    v_b_2x2 = [[8],[3]]
    exp_x_2x2 = [[1],[2]]
    run_solve_system_test_case(m_a_2x2, v_b_2x2, exp_x_2x2, "Sistema 2x2 com solução única")

    # Sistema 3x3: (usando a inversa do teste anterior)
    # A = [[1,2,3],[0,1,4],[5,6,0]]
    # A_inv = [[-24, 18, 5], [20, -15, -4], [-5, 4, 1]]
    # Seja X = [[1],[1],[1]], então B = A*X = [[1+2+3],[0+1+4],[5+6+0]] = [[6],[5],[11]]
    m_a_3x3 = [[1,2,3],[0,1,4],[5,6,0]]
    v_b_3x3 = [[6],[5],[11]]
    exp_x_3x3 = [[1],[1],[1]]
    run_solve_system_test_case(m_a_3x3, v_b_3x3, exp_x_3x3, "Sistema 3x3 com solução conhecida (X=[1,1,1])")

    # Sistema com A = Identidade => X = B
    ident_10x10 = generate_matrix(10, 10, lambda r,c: 1 if r==c else 0)
    v_b_10x1 = generate_matrix(10, 1, lambda r,c: r+1) # [[1],[2],...,[10]]
    run_solve_system_test_case(ident_10x10, v_b_10x1, v_b_10x1, "Sistema 10x10 com A=Identidade (X=B)")

    # --- Casos de Erro Esperados ---
    # Matriz A não quadrada
    run_solve_system_test_case([[1,2],[3,4],[5,6]], [[1],[1]], None, "Sistema com Matriz A não quadrada",
                               expect_error=True, error_message_contains="Matriz A (coeficientes) deve ser quadrada")
    # Matriz A singular (det=0)
    m_a_singular = [[1,2],[2,4]] # det = 0
    v_b_singular = [[3],[6]] # Para este B, teria infinitas soluções, mas o método da inversa falha.
                             # Se B fosse [3],[7] não teria solução.
    run_solve_system_test_case(m_a_singular, v_b_singular, None, "Sistema com Matriz A singular (det=0)",
                               expect_error=True, error_message_contains="determinante é zero")
    # Dimensões de A e B incompatíveis (nº linhas)
    run_solve_system_test_case([[1,2],[3,4]], [[1],[2],[3]], None, "Sistema com nº linhas de A != nº linhas de B",
                               expect_error=True, error_message_contains="Número de linhas da Matriz A deve ser igual")
    # Vetor B não é vetor coluna
    run_solve_system_test_case([[1,2],[3,4]], [[1,0],[2,0]], None, "Sistema com Vetor B não sendo coluna (NxM onde M!=1)",
                               expect_error=True, error_message_contains="Vetor B (termos independentes) deve ser um vetor coluna")
    run_solve_system_test_case(None, [[1]], None, "Sistema com Matriz A como None",
                               expect_error=True, error_message_contains="Matriz A (coeficientes) deve ser uma lista de listas")

    print_test_footer("solve_linear_system.py", test_count, passed_count)

if __name__ == "__main__":
    test_resolucao_sistemas()