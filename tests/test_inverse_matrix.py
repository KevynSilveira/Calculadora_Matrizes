# calculadora_matrizes/tests/test_inverse_matrix.py
from test_utils import format_matrix_for_log, are_matrices_equal, generate_matrix, print_test_header, print_test_footer, TOLERANCE
from logic.inverse_matrix import inverse_matrix
from logic.multiply_matrices import multiply_matrices # Para verificar A * A_inv = I
import math

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
            # Compara a inversa calculada com a esperada (se fornecida)
            if expected_inverse is not None and not are_matrices_equal(result_inv, expected_inverse):
                passed_this_test = False
                log_details.append(format_matrix_for_log(expected_inverse, "Inversa Esperada (Manual/Conhecida)"))
                log_details.append(format_matrix_for_log(result_inv, "Inversa Calculada"))
            elif expected_inverse is None and result_inv is not None: # Esperava None (erro), mas obteve resultado
                 passed_this_test = False
                 log_details.append("  Status: Esperava erro (expected_inverse é None), mas obteve resultado.")
                 log_details.append(format_matrix_for_log(result_inv, "Inversa Calculada Inesperadamente"))


            # Verifica A * A_inv = I, se a primeira verificação passou ou não era o foco
            if check_identity and not expect_error and result_inv is not None:
                try:
                    # Certifique-se que 'matrix' é uma matriz válida para multiplicação (não None)
                    if matrix and isinstance(matrix, list) and matrix[0] and isinstance(matrix[0], list):
                        ident_expected = generate_matrix(len(matrix), len(matrix[0]), lambda r,c: 1 if r==c else 0)
                        product = multiply_matrices(matrix, result_inv)
                        if not are_matrices_equal(product, ident_expected):
                            passed_this_test = False # Marca como falha se A*A_inv != I
                            log_details.append(format_matrix_for_log(product, "Produto A * A_inv (Obtido)"))
                            log_details.append(format_matrix_for_log(ident_expected, "Matriz Identidade (Esperada)"))
                            log_details.append("  Verificação A * A_inv = I falhou.")
                    else: # 'matrix' original não é válida para a verificação de identidade
                        if passed_this_test: # Se o teste da inversa passou, mas não podemos checar A*A_inv
                            log_details.append("  Aviso: Matriz original inválida para verificação A*A_inv=I, pulando esta checagem.")

                except Exception as mult_e: # Erro durante a multiplicação de verificação
                    passed_this_test = False
                    log_details.append(f"  Erro durante a verificação A * A_inv = I: {mult_e}")


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
            if not expect_error: log_details.append(format_matrix_for_log(expected_inverse, "Inversa Esperada (se aplicável)"))
            log_details.append(f"  Erro: ValueError: {ve}")
            
    except Exception as e:
        print(f"[FALHA] - {description}")
        log_details.append(f"  Status: Exceção inesperada do tipo {type(e).__name__}.")
        if not expect_error: log_details.append(format_matrix_for_log(expected_inverse, "Inversa Esperada (se aplicável)"))
        log_details.append(f"  Erro: {e}")
    
    print("  Log da Conta:")
    for detail in log_details: print(detail)


def test_inversao_matrizes():
    global test_count, passed_count
    test_count = 0
    passed_count = 0
    print_test_header("inverse_matrix.py")

    # --- Casos Válidos ---
    run_inverse_test_case([[5]], [[0.2]], "Inversa de matriz 1x1") # Era 1/5
    run_inverse_test_case([[-2]], [[-0.5]], "Inversa de matriz 1x1 negativa") # Era -1/2

    m_2x2 = [[4, 7], [2, 6]]
    exp_inv_2x2 = [[0.6, -0.7], [-0.2, 0.4]]
    run_inverse_test_case(m_2x2, exp_inv_2x2, "Inversa de matriz 2x2")

    ident_3x3 = [[1,0,0],[0,1,0],[0,0,1]]
    run_inverse_test_case(ident_3x3, ident_3x3, "Inversa da matriz identidade 3x3")

    m_3x3 = [[1,2,3],[0,1,4],[5,6,0]]
    exp_inv_3x3 = [[-24, 18, 5], [20, -15, -4], [-5, 4, 1]]
    run_inverse_test_case(m_3x3, exp_inv_3x3, "Inversa de matriz 3x3 (exemplo conhecido)")

    ident_10x10 = generate_matrix(10, 10, lambda r,c: 1 if r==c else 0)
    run_inverse_test_case(ident_10x10, ident_10x10, "Inversa da matriz identidade 10x10 (checa A*A_inv=I)", check_identity=True)

    # --- Casos de Erro Esperados ---
    run_inverse_test_case([[1,2],[3,4],[5,6]], None, "Inversa de matriz não quadrada",
                          expect_error=True, error_message_contains="deve ser quadrada") # CORRIGIDO AQUI
    
    run_inverse_test_case([[1,2],[2,4]], None, "Inversa de matriz singular (det=0) 2x2",
                          expect_error=True, error_message_contains="determinante é zero")
    
    run_inverse_test_case([[0]], None, "Inversa de matriz 1x1 singular (det=0)",
                          expect_error=True, error_message_contains="determinante é zero")
    
    run_inverse_test_case(None, None, "Inversa de Matriz None",
                          expect_error=True, error_message_contains="Matriz para inversão deve ser uma lista de listas")
    
    run_inverse_test_case([[]], None, "Inversa de Matriz [[]]",
                          expect_error=True, error_message_contains="Matriz para inversão contém linha(s) vazia(s)")


    print_test_footer("inverse_matrix.py", test_count, passed_count)

if __name__ == "__main__":
    test_inversao_matrizes()