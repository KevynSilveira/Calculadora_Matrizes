# calculadora_matrizes/tests/test_inverse_matrix.py

# Importa utilitários de teste:
# - format_matrix_for_log: Para exibir matrizes de forma legível no log.
# - are_matrices_equal: Para comparar a matriz inversa calculada com a esperada,
#                       com tolerância para números de ponto flutuante.
# - generate_matrix: Para criar matrizes de teste (ex: identidade).
# - print_test_header/footer: Para formatar o output do conjunto de testes.
# - TOLERANCE: Constante para comparação de floats (usada implicitamente por are_matrices_equal).
from test_utils import format_matrix_for_log, are_matrices_equal, generate_matrix, print_test_header, print_test_footer, TOLERANCE
# Importa a função de cálculo da inversa que este arquivo se destina a testar.
from logic.inverse_matrix import inverse_matrix
# Importa a função de multiplicação de matrizes, usada para a verificação crucial A * A_inv = I.
from logic.multiply_matrices import multiply_matrices
import math # Importa math (embora TOLERANCE já venha de test_utils, pode ser útil para outras comparações se necessário)

# Contadores globais para rastrear o número total de casos de teste executados
# e o número de casos que passaram dentro desta suíte de teste.
test_count = 0
passed_count = 0

def run_inverse_test_case(matrix, expected_inverse, description, 
                          expect_error=False, error_message_contains=None, 
                          check_identity=True):
    """
    Executa um único caso de teste para a função inverse_matrix.

    Esta função encapsula a lógica para:
    1. Chamar a função 'inverse_matrix' com a matriz de entrada.
    2. Comparar o resultado obtido com o 'expected_inverse'.
    3. Opcionalmente (e crucialmente), verificar se 'matrix * resultado_inversa' é igual à matriz identidade (A * A⁻¹ = I).
    4. Lidar com casos onde uma exceção (erro) é esperada (expect_error=True).
    5. Imprimir o status do teste ([OK] ou [FALHA]) e um log detalhado em caso de falha.

    Args:
        matrix (list[list[float]] or None): A matriz para a qual calcular a inversa.
        expected_inverse (list[list[float]] or None): A matriz inversa esperada.
                                                      Pode ser None se um erro é esperado ou se a verificação principal
                                                      é a propriedade A * A_inv = I.
        description (str): Uma breve descrição do caso de teste.
        expect_error (bool): True se este caso de teste espera que uma exceção ValueError seja levantada.
        error_message_contains (str or None): Se expect_error é True, esta string (ou parte dela,
                                              ignorando maiúsculas/minúsculas) deve estar contida na
                                              mensagem da exceção ValueError para o teste passar.
        check_identity (bool): Se True (padrão), realiza a verificação A * A_inv = I.
    """
    global test_count, passed_count 
    test_count += 1 
    
    print(f"\n--- Teste: {description} ---") 
    
    log_details = [format_matrix_for_log(matrix, "Matriz Original de Entrada")]

    try:
        result_inv = inverse_matrix(matrix)
        
        if expect_error:
            print(f"[FALHA] - {description}")
            log_details.append(f"  Status: Um erro era esperado, mas a operação foi concluída sem erros.")
            log_details.append(format_matrix_for_log(result_inv, "Inversa Obtida (Inesperada)"))
            if error_message_contains: log_details.append(f"  Detalhe do Erro Esperado: A mensagem deveria conter '{error_message_contains}'")
        else:
            passed_this_test = True 

            if expected_inverse is not None and not are_matrices_equal(result_inv, expected_inverse):
                passed_this_test = False 
                log_details.append(format_matrix_for_log(expected_inverse, "Inversa Esperada (Definida no Teste)"))
                log_details.append(format_matrix_for_log(result_inv, "Inversa Calculada pela Função"))
            elif expected_inverse is None and result_inv is not None and check_identity is False:
                log_details.append("  AVISO: 'expected_inverse' é None e 'check_identity' é False, mas uma inversa foi calculada.")
                log_details.append(format_matrix_for_log(result_inv, "Inversa Calculada (Sem verificação adicional)"))

            if check_identity and not expect_error and result_inv is not None:
                try:
                    if matrix and isinstance(matrix, list) and matrix[0] and isinstance(matrix[0], list) and len(matrix) == len(matrix[0]):
                        ident_expected = generate_matrix(len(matrix), len(matrix[0]), lambda r,c: 1 if r==c else 0)
                        product = multiply_matrices(matrix, result_inv)
                        
                        if not are_matrices_equal(product, ident_expected):
                            passed_this_test = False 
                            log_details.append(format_matrix_for_log(product, "Produto (Matriz Original * Inversa Calculada)"))
                            log_details.append(format_matrix_for_log(ident_expected, "Matriz Identidade (Esperada)"))
                            log_details.append("  DETALHE: A verificação fundamental A * A_inversa = I falhou.")
                    else: 
                        if passed_this_test: 
                            log_details.append("  AVISO: Matriz original inválida ou não quadrada para a verificação A*A_inv=I. Pulando esta checagem crucial.")
                except Exception as mult_e: 
                    passed_this_test = False
                    log_details.append(f"  ERRO DURANTE VERIFICAÇÃO A*A_inv=I: {type(mult_e).__name__}: {mult_e}")

            if passed_this_test:
                print(f"[OK] - {description}")
                passed_count += 1
                return
            else:
                print(f"[FALHA] - {description}")

    except ValueError as ve: 
        if expect_error:
            if error_message_contains is None or error_message_contains.lower() in str(ve).lower():
                print(f"[OK] - {description} (Erro esperado ValueError corretamente capturado: {ve})")
                passed_count += 1
                return
            else:
                print(f"[FALHA] - {description}")
                log_details.append(f"  Status: Um erro ValueError era esperado, mas sua mensagem não correspondeu.")
                log_details.append(f"  Mensagem de Erro Obtida: ValueError: {ve}")
                log_details.append(f"  Esperado que a Mensagem Contivesse: '{error_message_contains}'")
        else:
            print(f"[FALHA] - {description}")
            log_details.append(f"  Status: Erro ValueError inesperado durante a operação.")
            if not expect_error and expected_inverse is not None: 
                log_details.append(format_matrix_for_log(expected_inverse, "Inversa Esperada (se aplicável)"))
            log_details.append(f"  Detalhe do Erro: ValueError: {ve}")
            
    except Exception as e: 
        print(f"[FALHA] - {description}")
        log_details.append(f"  Status: Uma exceção totalmente inesperada do tipo {type(e).__name__} ocorreu.")
        if not expect_error and expected_inverse is not None:
            log_details.append(format_matrix_for_log(expected_inverse, "Inversa Esperada (se aplicável)"))
        log_details.append(f"  Detalhe do Erro: {e}")
    
    print("  Log Detalhado da Operação:")
    for detail in log_details: print(detail)


def test_inversao_matrizes():
    """
    Define e executa uma suíte de casos de teste para a função inverse_matrix.
    """
    global test_count, passed_count
    test_count = 0
    passed_count = 0
    print_test_header("inverse_matrix.py")

    # --- Seção: Casos de Teste Válidos ---
    run_inverse_test_case([[5]], [[0.2]], "Inversa de matriz 1x1 ([5] -> [0.2])")
    run_inverse_test_case([[-2]], [[-0.5]], "Inversa de matriz 1x1 negativa ([-2] -> [-0.5])")

    m_2x2 = [[4, 7], [2, 6]] 
    exp_inv_2x2 = [[0.6, -0.7], [-0.2, 0.4]] 
    run_inverse_test_case(m_2x2, exp_inv_2x2, "Inversa de matriz 2x2 padrão")

    ident_3x3 = [[1,0,0],[0,1,0],[0,0,1]]
    run_inverse_test_case(ident_3x3, ident_3x3, "Inversa da matriz identidade 3x3 (Inv(I)=I)")

    m_3x3 = [[1,2,3],[0,1,4],[5,6,0]] 
    exp_inv_3x3 = [[-24, 18, 5], [20, -15, -4], [-5, 4, 1]] 
    run_inverse_test_case(m_3x3, exp_inv_3x3, "Inversa de matriz 3x3 (exemplo conhecido, det=1)")

    ident_10x10 = generate_matrix(10, 10, lambda r,c: 1 if r==c else 0)
    run_inverse_test_case(ident_10x10, ident_10x10, 
                          "Inversa da matriz identidade 10x10 (principalmente checa A*A_inv=I)", 
                          check_identity=True)

    # O CASO DE TESTE DA MATRIZ 4X4 COMPLEXA FOI REMOVIDO DESTA VERSÃO.

    # --- Seção: Casos de Teste de Erro ---
    run_inverse_test_case(
        matrix=[[1,2],[3,4],[5,6]], 
        expected_inverse=None, 
        description="Inversa de matriz não quadrada (3x2)",
        expect_error=True, 
        error_message_contains="deve ser quadrada" 
    )
    
    run_inverse_test_case(
        matrix=[[1,2],[2,4]], 
        expected_inverse=None, 
        description="Inversa de matriz singular 2x2 (det=0)",
        expect_error=True, 
        error_message_contains="determinante é zero" 
    )
    
    run_inverse_test_case(
        matrix=[[0]], 
        expected_inverse=None,
        description="Inversa de matriz 1x1 singular (det=0)",
        expect_error=True, 
        error_message_contains="determinante é zero"
    )
    
    run_inverse_test_case(
        matrix=None, 
        expected_inverse=None,
        description="Inversa de Matriz inválida (None)",
        expect_error=True, 
        error_message_contains="Matriz para inversão deve ser uma lista de listas"
    )
    
    run_inverse_test_case(
        matrix=[[]], 
        expected_inverse=None,
        description="Inversa de Matriz inválida (contém linha vazia [[]])",
        expect_error=True, 
        error_message_contains="Matriz para inversão contém linha(s) vazia(s)"
    )

    print_test_footer("inverse_matrix.py", test_count, passed_count)

if __name__ == "__main__":
    test_inversao_matrizes()