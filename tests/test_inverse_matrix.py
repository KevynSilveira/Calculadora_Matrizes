# calculadora_matrizes/tests/test_inverse_matrix.py
from test_utils import format_matrix_for_log, are_matrices_equal, generate_matrix, print_test_header, print_test_footer
from logic.inverse_matrix import inverse_matrix
from logic.multiply_matrices import multiply_matrices # Para verificar A * A_inv = I

test_count = 0
passed_count = 0

def run_inverse_test_case(matrix, expected_inverse, description, expect_error=False, error_message_contains=None, check_identity=True):
    global test_count, passed_count
    test_count += 1
    print(f"\n--- Teste: {description} ---")
    log_details = [format_matrix_for_log(matrix, "Matriz Original")]

    try:
        result_inv = inverse_matrix(matrix)
        
        if expect_error:
            print(f"[FALHA] - {description}")
            log_details.append(f"  Status: Erro era esperado, mas a operação foi concluída.")
            log_details.append(format_matrix_for_log(result_inv, "Inversa Obtida"))
            if error_message_contains: log_details.append(f"  Erro Esperado (contendo): '{error_message_contains}'")
        else:
            passed_this_test = True
            if not are_matrices_equal(result_inv, expected_inverse):
                passed_this_test = False
                log_details.append(format_matrix_for_log(expected_inverse, "Inversa Esperada (Manual/Conhecida)"))
                log_details.append(format_matrix_for_log(result_inv, "Inversa Calculada"))
            
            if check_identity and passed_this_test: # Só checa identidade se a comparação direta passar ou não for o foco
                ident_expected = generate_matrix(len(matrix), len(matrix[0]), lambda r,c: 1 if r==c else 0)
                product = multiply_matrices(matrix, result_inv)
                if not are_matrices_equal(product, ident_expected):
                    passed_this_test = False
                    log_details.append(format_matrix_for_log(product, "Produto A * A_inv (Obtido)"))
                    log_details.append(format_matrix_for_log(ident_expected, "Matriz Identidade (Esperada)"))
                    log_details.append("  Verificação A * A_inv = I falhou.")

            if passed_this_test:
                print(f"[OK] - {description}")
                passed_count += 1
                return
            else:
                print(f"[FALHA] - {description}")
                # Os logs já foram adicionados acima no caso de falha

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
            if not expect_error: log_details.append(format_matrix_for_log(expected_inverse, "Inversa Esperada (se aplicável)"))
    except Exception as e:
        print(f"[FALHA] - {description}")
        log_details.append(f"  Status: Exceção inesperada {type(e).__name__}: {e}")
        if not expect_error: log_details.append(format_matrix_for_log(expected_inverse, "Inversa Esperada (se aplicável)"))
    
    print("  Log da Conta:")
    for detail in log_details: print(detail)


def test_inversao_matrizes():
    global test_count, passed_count
    test_count = 0
    passed_count = 0
    print_test_header("inverse_matrix.py")

    # --- Casos Válidos ---
    # 1x1
    run_inverse_test_case([[5]], [[1/5]], "Inversa de matriz 1x1")
    run_inverse_test_case([[-2]], [[-1/2]], "Inversa de matriz 1x1 negativa")

    # 2x2
    # A = [[a,b],[c,d]], A_inv = 1/det(A) * [[d, -b],[-c, a]]
    # Matriz: [[4, 7], [2, 6]], det = 24 - 14 = 10
    # Inversa: (1/10) * [[6, -7], [-2, 4]] = [[0.6, -0.7], [-0.2, 0.4]]
    m_2x2 = [[4, 7], [2, 6]]
    exp_inv_2x2 = [[0.6, -0.7], [-0.2, 0.4]]
    run_inverse_test_case(m_2x2, exp_inv_2x2, "Inversa de matriz 2x2")

    # Matriz identidade
    ident_3x3 = [[1,0,0],[0,1,0],[0,0,1]]
    run_inverse_test_case(ident_3x3, ident_3x3, "Inversa da matriz identidade 3x3")

    # Exemplo 3x3 com inversa conhecida
    # A = [[1,2,3],[0,1,4],[5,6,0]], det(A) = 1 (do teste de determinante)
    # Adj(A) = [[-24, 18, 5], [20, -15, -4], [-5, 4, 1]] (Transposta dos cofatores)
    # Cofatores:
    # C11 = -24, C12 = -(-20)=20, C13 = -5
    # C21 = -(0-18)=18, C22 = 0-15=-15, C23 = -(6-10)=4
    # C31 = 8-3=5, C32 = -(4-0)=-4, C33 = 1-0=1
    # Matriz Cofatores = [[-24,20,-5],[18,-15,4],[5,-4,1]]
    # Adjunta = Transposta = [[-24,18,5],[20,-15,-4],[-5,4,1]]
    # Inversa = (1/1) * Adjunta
    m_3x3 = [[1,2,3],[0,1,4],[5,6,0]]
    exp_inv_3x3 = [[-24, 18, 5], [20, -15, -4], [-5, 4, 1]]
    run_inverse_test_case(m_3x3, exp_inv_3x3, "Inversa de matriz 3x3 (exemplo conhecido)")

    # Para matrizes 10x10, o cálculo manual é impraticável.
    # Testar apenas a propriedade A * A_inv = I para uma matriz invertível conhecida (Identidade).
    ident_10x10 = generate_matrix(10, 10, lambda r,c: 1 if r==c else 0)
    run_inverse_test_case(ident_10x10, ident_10x10, "Inversa da matriz identidade 10x10 (checa A*A_inv=I)", check_identity=True)


    # --- Casos de Erro Esperados ---
    run_inverse_test_case([[1,2],[3,4],[5,6]], None, "Inversa de matriz não quadrada",
                          expect_error=True, error_message_contains="matriz deve ser quadrada")
    run_inverse_test_case([[1,2],[2,4]], None, "Inversa de matriz singular (det=0) 2x2",
                          expect_error=True, error_message_contains="determinante é zero")
    run_inverse_test_case([[0]], None, "Inversa de matriz 1x1 singular (det=0)",
                          expect_error=True, error_message_contains="determinante é zero")
    run_inverse_test_case(None, None, "Inversa de Matriz None",
                          expect_error=True, error_message_contains="Matriz para inversão")

    print_test_footer("inverse_matrix.py", test_count, passed_count)

if __name__ == "__main__":
    test_inversao_matrizes()