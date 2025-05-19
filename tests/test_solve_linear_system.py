# calculadora_matrizes/tests/test_solve_linear_system.py

# Importa utilitários de teste:
# - format_matrix_for_log: Para exibir matrizes de forma legível.
# - are_matrices_equal: Para comparar a solução X calculada com a esperada.
# - generate_matrix: Para criar matrizes de teste maiores (ex: identidade para A).
# - print_test_header/footer: Para formatar o output do conjunto de testes.
from test_utils import format_matrix_for_log, are_matrices_equal, print_test_header, print_test_footer, generate_matrix 
# Importa a função de resolução de sistema linear que será testada.
from logic.solve_linear_system import solve_linear_system_inverse
# Importa a função de multiplicação para a verificação A * X_calculado = B.
from logic.multiply_matrices import multiply_matrices 
import math # Importa math (embora TOLERANCE já venha de test_utils, pode ser útil para outras comparações se necessário)

# Contadores globais para rastrear estatísticas dos testes.
test_count = 0
passed_count = 0

def run_solve_system_test_case(matrix_a, vector_b, expected_solution_x, description, 
                               expect_error=False, error_message_contains=None, 
                               check_ax_eq_b=True):
    """
    Executa um único caso de teste para a função solve_linear_system_inverse.

    Esta função irá:
    1. Chamar 'solve_linear_system_inverse(matrix_a, vector_b)'.
    2. Se um erro é esperado (expect_error=True):
        a. Verificar se um ValueError foi levantado.
        b. Se sim, verificar se a mensagem de erro contém 'error_message_contains'.
    3. Se nenhum erro é esperado:
        a. Comparar a solução X calculada com 'expected_solution_x'.
        b. Opcionalmente (se check_ax_eq_b=True), verificar se matrix_a * solution_x = vector_b.
    4. Imprimir o status ([OK] ou [FALHA]) e um log detalhado em caso de falha.

    Args:
        matrix_a (list[list[float]] or None): A matriz de coeficientes A.
        vector_b (list[list[float]] or None): O vetor de termos independentes B (como matriz coluna).
        expected_solution_x (list[list[float]] or None): O vetor solução X esperado (como matriz coluna).
                                                        None se um erro é esperado.
        description (str): Descrição do caso de teste.
        expect_error (bool): True se uma exceção ValueError é esperada.
        error_message_contains (str or None): Substring esperada na mensagem de erro.
        check_ax_eq_b (bool): Se True, realiza a verificação A * X = B.
    """
    global test_count, passed_count
    test_count += 1
    print(f"\n--- Teste: {description} ---")
    # Log inicial com as matrizes de entrada A e B.
    log_details = [
        format_matrix_for_log(matrix_a, "Matriz A (Coeficientes) - Entrada"),
        format_matrix_for_log(vector_b, "Vetor B (Termos Independentes) - Entrada")
    ]

    try:
        # 1. Execução da Função: Tenta resolver o sistema linear.
        solution_x = solve_linear_system_inverse(matrix_a, vector_b)
        
        # 2. Verificação Pós-Execução (se nenhum erro ocorreu durante a execução):
        if expect_error:
            # Se um erro ERA esperado, mas a função completou, o teste FALHA.
            print(f"[FALHA] - {description}")
            log_details.append(f"  Status: Um erro era esperado, mas a operação foi concluída sem erros.")
            log_details.append(format_matrix_for_log(solution_x, "Solução X Obtida (Inesperada)"))
            if error_message_contains: log_details.append(f"  Detalhe do Erro Esperado: A mensagem deveria conter '{error_message_contains}'")
        else:
            # Se nenhum erro era esperado, prossegue com as verificações da solução.
            passed_this_test = True # Flag para rastrear o sucesso das múltiplas verificações.

            # 2a. Comparação Direta da Solução X com a Esperada (se fornecida):
            if expected_solution_x is not None and not are_matrices_equal(solution_x, expected_solution_x):
                passed_this_test = False # Falha se X calculado não bate com X esperado.
                log_details.append(format_matrix_for_log(expected_solution_x, "Solução X Esperada"))
                log_details.append(format_matrix_for_log(solution_x, "Solução X Calculada pela Função"))
            elif expected_solution_x is None and solution_x is not None and not check_ax_eq_b :
                # Caso onde não há X esperado (talvez um erro era o "resultado" esperado),
                # a função retornou uma solução, e não vamos checar A*X=B.
                log_details.append("  AVISO: 'expected_solution_x' é None e 'check_ax_eq_b' é False, mas uma solução X foi calculada.")
                log_details.append(format_matrix_for_log(solution_x, "Solução X Calculada (Sem verificação A*X=B)"))
            
            # 2b. Verificação Fundamental: matrix_a * solution_x deve ser igual a vector_b.
            #     Esta verificação confirma se a solução X encontrada realmente satisfaz o sistema AX=B.
            #     Realizada se 'check_ax_eq_b' for True, nenhum erro era esperado, e uma solução X foi calculada.
            if check_ax_eq_b and passed_this_test and solution_x is not None and matrix_a is not None and vector_b is not None:
                try:
                    # Garante que 'matrix_a' é uma matriz válida para a multiplicação de verificação.
                    if not (isinstance(matrix_a, list) and matrix_a and isinstance(matrix_a[0], list)):
                        raise TypeError("Matriz A (coeficientes) inválida para a verificação A*X=B.")

                    # Calcula o produto: Matriz A * Solução X calculada.
                    product_ax = multiply_matrices(matrix_a, solution_x)
                    
                    if not are_matrices_equal(product_ax, vector_b):
                        passed_this_test = False # Falha se A*X não for igual a B (dentro da tolerância).
                        log_details.append(format_matrix_for_log(product_ax, "Produto A * X_calculado (Obtido)"))
                        log_details.append(format_matrix_for_log(vector_b, "Vetor B Original (Esperado)"))
                        log_details.append("  DETALHE: A verificação fundamental A * X = B falhou.")
                except Exception as mult_e: # Captura erros durante a multiplicação de verificação.
                    passed_this_test = False # Qualquer erro aqui significa que a verificação falhou.
                    log_details.append(f"  ERRO DURANTE VERIFICAÇÃO A*X=B: {type(mult_e).__name__}: {mult_e}")

            # Conclusão do teste baseado no flag 'passed_this_test'.
            if passed_this_test:
                print(f"[OK] - {description}")
                passed_count += 1
                return
            else:
                 print(f"[FALHA] - {description}")
                 # O log já contém os detalhes das falhas nas verificações acima.

    except ValueError as ve: # Captura ValueErrors (matriz A não quadrada, singular, dimensões A/B incompatíveis, etc.)
        # 3. Tratamento de ValueErrors:
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
            if not expect_error and expected_solution_x is not None: 
                log_details.append(format_matrix_for_log(expected_solution_x, "Solução X Esperada (se aplicável)"))
            log_details.append(f"  Detalhe do Erro: ValueError: {ve}")
            
    except Exception as e: # Captura qualquer outra exceção não prevista.
        # 4. Tratamento de Outras Exceções Inesperadas:
        print(f"[FALHA] - {description}")
        log_details.append(f"  Status: Uma exceção totalmente inesperada do tipo {type(e).__name__} ocorreu.")
        if not expect_error and expected_solution_x is not None: 
            log_details.append(format_matrix_for_log(expected_solution_x, "Solução X Esperada (se aplicável)"))
        log_details.append(f"  Detalhe do Erro: {e}")
    
    # 5. Impressão do Log Detalhado (Apenas em caso de FALHA):
    print("  Log Detalhado da Operação:")
    for detail in log_details: print(detail)


def test_resolucao_sistemas():
    """
    Define e executa uma suíte de casos de teste para a função solve_linear_system_inverse.
    Testa sistemas de diferentes tamanhos, incluindo casos com solução única,
    e cenários de erro como matriz A não quadrada, singular, ou dimensões incompatíveis.
    A verificação A*X = B é crucial para validar a corretude da solução.
    """
    global test_count, passed_count
    test_count = 0
    passed_count = 0
    print_test_header("solve_linear_system.py")

    # --- Seção: Casos de Teste Válidos ---
    # Teste 1: Sistema 1x1 simples (ex: 5x = 10 => x = 2)
    run_solve_system_test_case(
        matrix_a=[[5]], 
        vector_b=[[10]], 
        expected_solution_x=[[2.0]], # Solução como float para consistência
        description="Sistema linear 1x1 simples"
    )

    # Teste 2: Sistema 2x2 com solução única
    # 2x + 3y = 8
    #  x +  y = 3   => Solução: x=1, y=2
    m_a_2x2 = [[2,3],[1,1]]
    v_b_2x2 = [[8],[3]]
    exp_x_2x2 = [[1.0],[2.0]]
    run_solve_system_test_case(m_a_2x2, v_b_2x2, exp_x_2x2, "Sistema linear 2x2 com solução única")

    # Teste 3: Sistema 3x3 com solução conhecida
    # Usando A do teste de inversa (det=1), e X = [[1],[1],[1]]
    # B = A*X = [[1*1+2*1+3*1],[0*1+1*1+4*1],[5*1+6*1+0*1]] = [[6],[5],[11]]
    m_a_3x3 = [[1,2,3],[0,1,4],[5,6,0]]
    v_b_3x3 = [[6],[5],[11]]
    exp_x_3x3 = [[1.0],[1.0],[1.0]]
    run_solve_system_test_case(m_a_3x3, v_b_3x3, exp_x_3x3, "Sistema linear 3x3 com solução conhecida (X=[1,1,1])")

    # Teste 4: Sistema 10x10 com Matriz A sendo a Identidade (I*X = B => X = B)
    ident_10x10 = generate_matrix(10, 10, lambda r,c: 1 if r==c else 0)
    v_b_10x1 = generate_matrix(10, 1, lambda r,c: float(r+1)) # Vetor B: [[1.0], [2.0], ..., [10.0]]
    run_solve_system_test_case(ident_10x10, v_b_10x1, v_b_10x1, "Sistema 10x10 com A=Identidade (solução X=B)")

    # --- Seção: Casos de Teste de Erro ---
    # Teste 5: Matriz A (coeficientes) não é quadrada
    run_solve_system_test_case(
        matrix_a=[[1,2],[3,4],[5,6]], # Matriz 3x2
        vector_b=[[1],[1]],           # Vetor B compatível em linhas se A fosse 2xN
        expected_solution_x=None, 
        description="Sistema com Matriz A não quadrada",
        expect_error=True, 
        error_message_contains="Matriz A (coeficientes) deve ser quadrada"
    )
    
    # Teste 6: Matriz A é singular (determinante = 0), o que impede o método da inversa
    m_a_singular = [[1,2],[2,4]] # det = 0
    v_b_singular = [[3],[6]]     # Para este B, o sistema teria infinitas soluções, mas o método da inversa falha
    run_solve_system_test_case(
        matrix_a=m_a_singular, 
        vector_b=v_b_singular, 
        expected_solution_x=None,
        description="Sistema com Matriz A singular (det=0)",
        expect_error=True, 
        error_message_contains="determinante é zero" # Erro propagado da função inverse_matrix
    )
    
    # Teste 7: Número de linhas da Matriz A incompatível com o número de linhas do Vetor B
    run_solve_system_test_case(
        matrix_a=[[1,2],[3,4]],   # Matriz A 2x2
        vector_b=[[1],[2],[3]],   # Vetor B 3x1
        expected_solution_x=None,
        description="Sistema com nº de linhas de A diferente do nº de linhas de B",
        expect_error=True, 
        error_message_contains="Número de linhas da Matriz A (coeficientes) deve ser igual ao número de linhas do Vetor B"
    )
    
    # Teste 8: Vetor B não é um vetor coluna (tem mais de uma coluna)
    run_solve_system_test_case(
        matrix_a=[[1,2],[3,4]],   # Matriz A 2x2
        vector_b=[[1,0],[2,0]],   # Vetor B 2x2 (não é coluna)
        expected_solution_x=None,
        description="Sistema com Vetor B não sendo um vetor coluna",
        expect_error=True, 
        error_message_contains="Vetor B (termos independentes) deve ser um vetor coluna"
    )
    
    # Teste 9: Matriz A é None (inválida)
    run_solve_system_test_case(
        matrix_a=None, 
        vector_b=[[1]], 
        expected_solution_x=None,
        description="Sistema com Matriz A inválida (None)",
        expect_error=True, 
        error_message_contains="Matriz A (coeficientes) deve ser uma lista de listas" # Mensagem da validação
    )
    
    # Teste 10: Vetor B é None (inválido)
    #   É importante que matrix_a seja válida (quadrada) para que a validação de vector_b seja alcançada primeiro.
    valid_matrix_a_for_b_test = [[1]] # Matriz A 1x1 válida
    run_solve_system_test_case(
        matrix_a=valid_matrix_a_for_b_test, 
        vector_b=None, 
        expected_solution_x=None,
        description="Sistema com Vetor B inválido (None)",
        expect_error=True, 
        error_message_contains="Vetor B (termos independentes) deve ser uma lista de listas" # Mensagem da validação
    )

    print_test_footer("solve_linear_system.py", test_count, passed_count)

if __name__ == "__main__":
    test_resolucao_sistemas()