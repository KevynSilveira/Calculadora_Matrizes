# calculadora_matrizes/tests/test_solve_linear_system.py
from test_utils import format_matrix_for_log, are_matrices_equal, print_test_header, print_test_footer, generate_matrix 
from logic.solve_linear_system import solve_linear_system_inverse
from logic.multiply_matrices import multiply_matrices 
import math 

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
            if expected_solution_x is not None and not are_matrices_equal(solution_x, expected_solution_x):
                passed_this_test = False
                log_details.append(format_matrix_for_log(expected_solution_x, "Solução X Esperada"))
                log_details.append(format_matrix_for_log(solution_x, "Solução X Calculada"))
            elif expected_solution_x is None and solution_x is not None: 
                passed_this_test = False
                log_details.append("  Status: Esperava erro (expected_solution é None), mas obteve resultado.")
                log_details.append(format_matrix_for_log(solution_x, "Solução X Calculada Inesperadamente"))
            
            if check_ax_eq_b and passed_this_test and solution_x is not None and matrix_a is not None and vector_b is not None:
                try:
                    # Verifica se matrix_a é realmente uma matriz válida para multiplicação
                    if not (isinstance(matrix_a, list) and matrix_a and isinstance(matrix_a[0], list)):
                        raise TypeError("Matriz A inválida para verificação A*X=B")

                    product_ax = multiply_matrices(matrix_a, solution_x)
                    if not are_matrices_equal(product_ax, vector_b):
                        passed_this_test = False 
                        log_details.append(format_matrix_for_log(product_ax, "Produto A * X_calculado (Obtido)"))
                        log_details.append(format_matrix_for_log(vector_b, "Vetor B Original (Esperado)"))
                        log_details.append("  Verificação A * X = B falhou.")
                except Exception as mult_e:
                    passed_this_test = False
                    log_details.append(f"  Erro durante a verificação A*X=B: {mult_e}")

            if passed_this_test:
                print(f"[OK] - {description}")
                passed_count += 1
                return
            else:
                 print(f"[FALHA] - {description}")

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
            if not expect_error: log_details.append(format_matrix_for_log(expected_solution_x, "Solução X Esperada (se aplicável)"))
            log_details.append(f"  Erro: ValueError: {ve}")
            
    except Exception as e:
        print(f"[FALHA] - {description}")
        log_details.append(f"  Status: Exceção inesperada do tipo {type(e).__name__}.")
        if not expect_error: log_details.append(format_matrix_for_log(expected_solution_x, "Solução X Esperada (se aplicável)"))
        log_details.append(f"  Erro: {e}")
    
    print("  Log da Conta:")
    for detail in log_details: print(detail)


def test_resolucao_sistemas():
    global test_count, passed_count
    test_count = 0
    passed_count = 0
    print_test_header("solve_linear_system.py")

    # --- Casos Válidos ---
    run_solve_system_test_case([[5]], [[10]], [[2.0]], "Sistema 1x1 simples")

    m_a_2x2 = [[2,3],[1,1]]
    v_b_2x2 = [[8],[3]]
    exp_x_2x2 = [[1.0],[2.0]]
    run_solve_system_test_case(m_a_2x2, v_b_2x2, exp_x_2x2, "Sistema 2x2 com solução única")

    m_a_3x3 = [[1,2,3],[0,1,4],[5,6,0]]
    v_b_3x3 = [[6],[5],[11]]
    exp_x_3x3 = [[1.0],[1.0],[1.0]]
    run_solve_system_test_case(m_a_3x3, v_b_3x3, exp_x_3x3, "Sistema 3x3 com solução conhecida (X=[1,1,1])")

    ident_10x10 = generate_matrix(10, 10, lambda r,c: 1 if r==c else 0)
    v_b_10x1 = generate_matrix(10, 1, lambda r,c: float(r+1)) 
    run_solve_system_test_case(ident_10x10, v_b_10x1, v_b_10x1, "Sistema 10x10 com A=Identidade (X=B)")

    # --- Casos de Erro Esperados ---
    run_solve_system_test_case([[1,2],[3,4],[5,6]], [[1],[1]], None, "Sistema com Matriz A não quadrada",
                               expect_error=True, error_message_contains="Matriz A (coeficientes) deve ser quadrada")
    
    m_a_singular = [[1,2],[2,4]] 
    v_b_singular = [[3],[6]] 
    run_solve_system_test_case(m_a_singular, v_b_singular, None, "Sistema com Matriz A singular (det=0)",
                               expect_error=True, error_message_contains="determinante é zero") # A mensagem de erro da inversa é propagada
    
    run_solve_system_test_case([[1,2],[3,4]], [[1],[2],[3]], None, "Sistema com nº linhas de A != nº linhas de B",
                               expect_error=True, error_message_contains="Número de linhas da Matriz A (coeficientes) deve ser igual ao número de linhas do Vetor B") # CORRIGIDO AQUI
    
    run_solve_system_test_case([[1,2],[3,4]], [[1,0],[2,0]], None, "Sistema com Vetor B não sendo coluna (NxM onde M!=1)",
                               expect_error=True, error_message_contains="Vetor B (termos independentes) deve ser um vetor coluna")
    
    run_solve_system_test_case(None, [[1]], None, "Sistema com Matriz A como None",
                               expect_error=True, error_message_contains="Matriz A (coeficientes) deve ser uma lista de listas")
    
    # CORRIGIDO: Fornecer uma Matriz A válida para que o erro de Vetor B seja testado
    valid_matrix_a_for_b_test = [[1]] 
    run_solve_system_test_case(valid_matrix_a_for_b_test, None, None, "Sistema com Vetor B como None",
                                expect_error=True, error_message_contains="Vetor B (termos independentes) deve ser uma lista de listas")


    print_test_footer("solve_linear_system.py", test_count, passed_count)

if __name__ == "__main__":
    test_resolucao_sistemas()