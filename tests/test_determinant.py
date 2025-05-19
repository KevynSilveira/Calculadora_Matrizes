# calculadora_matrizes/tests/test_determinant.py

# Importa utilitários de teste:
# - format_matrix_for_log: Para exibir matrizes de forma legível.
# - are_matrices_equal: Embora o determinante seja um escalar, esta função em test_utils
#                       foi adaptada para comparar escalares com tolerância também.
# - generate_matrix: Para criar matrizes de teste maiores (ex: identidade).
# - print_test_header/footer: Para formatar o output do conjunto de testes.
# - TOLERANCE: Constante para comparação de floats.
from test_utils import format_matrix_for_log, are_matrices_equal, generate_matrix, print_test_header, print_test_footer, TOLERANCE
# Importa a função de cálculo de determinante que será testada.
from logic.determinant import determinant
# Importa 'math' para usar 'math.isclose' na comparação direta de determinantes (floats).
import math

# Contadores globais para rastrear estatísticas dos testes.
test_count = 0
passed_count = 0

def run_determinant_test_case(matrix, expected_determinant, description, expect_error=False, error_message_contains=None):
    """
    Executa um único caso de teste para a função determinant.

    Esta função irá:
    1. Chamar 'determinant(matrix)'.
    2. Se um erro é esperado (expect_error=True):
        a. Verificar se um ValueError foi levantado.
        b. Se sim, verificar se a mensagem de erro contém 'error_message_contains'.
    3. Se nenhum erro é esperado:
        a. Verificar se o resultado do determinante é numericamente próximo ao 'expected_determinant'
           usando math.isclose com a TOLERANCE definida.
    4. Imprimir o status ([OK] ou [FALHA]) e um log detalhado em caso de falha.

    Args:
        matrix (list[list[float]] or None): A matriz para a qual calcular o determinante.
        expected_determinant (float or int or None): O valor esperado do determinante.
                                                     None se um erro é esperado.
        description (str): Descrição do caso de teste.
        expect_error (bool): True se uma exceção ValueError é esperada.
        error_message_contains (str or None): Substring esperada na mensagem de erro.
    """
    global test_count, passed_count
    test_count += 1
    
    print(f"\n--- Teste: {description} ---")
    # Log inicial com a matriz de entrada.
    log_details = [
        format_matrix_for_log(matrix, "Matriz de Entrada")
    ]

    try:
        # 1. Execução da Função: Calcula o determinante.
        result = determinant(matrix)
        
        # 2. Verificação Pós-Execução (se nenhum erro ocorreu durante a execução):
        if expect_error:
            # Se um erro ERA esperado, mas a função retornou um resultado, o teste FALHA.
            print(f"[FALHA] - {description}")
            log_details.append("  Status: Um erro era esperado, mas a operação foi concluída sem erros.")
            log_details.append(f"  Resultado Obtido (Inesperado): {result}")
            if error_message_contains:
                 log_details.append(f"  Detalhe do Erro Esperado: A mensagem deveria conter '{error_message_contains}'")
        # Compara o resultado com o esperado usando math.isclose para lidar com a precisão de floats.
        elif expected_determinant is not None and math.isclose(result, expected_determinant, rel_tol=TOLERANCE, abs_tol=TOLERANCE):
            # Se o resultado é próximo o suficiente do esperado, o teste PASSA.
            print(f"[OK] - {description}")
            passed_count += 1
            return # Saída antecipada para testes OK.
        elif expected_determinant is None and result is None:
            # Caso especial: se o esperado e o resultado são None (geralmente indica que um erro
            # deveria ter sido levantado mas o teste foi configurado com expected_determinant=None
            # e a função retornou None por algum motivo não previsto).
            # Considerado OK se for intencional, mas merece revisão da lógica do teste.
            print(f"[OK] - {description} (Resultado e esperado são None, verifique a intenção do teste)")
            passed_count += 1
            return
        else:
            # Se o resultado não é próximo o suficiente do esperado, o teste FALHA.
            print(f"[FALHA] - {description}")
            log_details.append(f"  Resultado Esperado: {expected_determinant}")
            log_details.append(f"  Resultado Obtido: {result}")

    except ValueError as ve: # Captura ValueErrors (erros de validação, matriz não quadrada, etc.)
        # 3. Tratamento de ValueErrors:
        if expect_error:
            # Se um ValueError era esperado:
            # Verifica se a mensagem de erro capturada contém a substring esperada.
            if error_message_contains is None or error_message_contains.lower() in str(ve).lower():
                # Se a mensagem corresponde, o teste PASSA.
                print(f"[OK] - {description} (Erro esperado ValueError corretamente capturado: {ve})")
                passed_count += 1
                return
            else:
                # Se a mensagem não corresponde, o teste FALHA.
                print(f"[FALHA] - {description}")
                log_details.append(f"  Status: Um erro ValueError era esperado, mas sua mensagem não correspondeu.")
                log_details.append(f"  Mensagem de Erro Obtida: ValueError: {ve}")
                log_details.append(f"  Esperado que a Mensagem Contivesse: '{error_message_contains}'")
        else:
            # Se um ValueError NÃO era esperado, mas ocorreu, o teste FALHA.
            print(f"[FALHA] - {description}")
            log_details.append(f"  Status: Erro ValueError inesperado durante a operação.")
            if not expect_error and expected_determinant is not None: # Mostra o esperado apenas se não era um teste de erro
                log_details.append(f"  Resultado Esperado: {expected_determinant}")
            log_details.append(f"  Detalhe do Erro: ValueError: {ve}")
            
    except Exception as e: # Captura qualquer outra exceção não prevista (ex: TypeError, IndexError).
        # 4. Tratamento de Outras Exceções Inesperadas:
        print(f"[FALHA] - {description}")
        log_details.append(f"  Status: Uma exceção totalmente inesperada do tipo {type(e).__name__} ocorreu.")
        if not expect_error and expected_determinant is not None:
            log_details.append(f"  Resultado Esperado: {expected_determinant}")
        log_details.append(f"  Detalhe do Erro: {e}")

    # 5. Impressão do Log Detalhado (Apenas em caso de FALHA):
    print("  Log Detalhado da Operação:")
    for detail in log_details:
        print(detail)

def test_determinantes():
    """
    Define e executa uma suíte de casos de teste para a função determinant.
    Inclui testes para matrizes de diferentes tamanhos, casos especiais (identidade, singular)
    e casos de erro (matriz não quadrada, inválida).
    """
    global test_count, passed_count
    test_count = 0
    passed_count = 0
    
    print_test_header("determinant.py")

    # --- Seção: Casos de Teste Válidos ---
    # Matriz 1x1: det([a]) = a
    run_determinant_test_case([[5]], 5, "Determinante de matriz 1x1")
    run_determinant_test_case([[-10]], -10, "Determinante de matriz 1x1 negativa")
    
    # Matriz 2x2: det([[a,b],[c,d]]) = ad - bc
    run_determinant_test_case([[1, 2], [3, 4]], -2, "Determinante de matriz 2x2 (1*4 - 2*3 = -2)")
    run_determinant_test_case([[0, 0], [3, 4]], 0, "Determinante de matriz 2x2 com uma linha de zeros (det=0)")
    run_determinant_test_case([[6, 1], [0, 4]], 24, "Determinante de matriz triangular inferior 2x2 (produto da diagonal)")

    # Matriz 3x3: Exemplo calculado manualmente
    m_3x3 = [[1, 2, 3], [0, 1, 4], [5, 6, 0]] 
    # Det = 1(0-24) - 2(0-20) + 3(0-5) = -24 + 40 - 15 = 1
    run_determinant_test_case(m_3x3, 1, "Determinante de matriz 3x3 (exemplo calculado)")

    # Matriz Diagonal 3x3: Determinante é o produto dos elementos da diagonal
    m_3x3_diag = [[2,0,0],[0,3,0],[0,0,4]]
    run_determinant_test_case(m_3x3_diag, 24, "Determinante de matriz diagonal 3x3 (2*3*4=24)")

    # Matriz Singular 3x3: Uma linha é múltipla de outra, det=0
    m_3x3_singular = [[1,2,3],[2,4,6],[7,8,9]] # Linha 2 = 2 * Linha 1
    run_determinant_test_case(m_3x3_singular, 0, "Determinante de matriz 3x3 singular (linhas dependentes, det=0)")

    # Matriz 4x4: Exemplo com resultado conhecido (pode ser verificado com ferramenta externa)
    m_4x4 = [[1,2,0,1], [0,3,1,2], [-1,0,2,-1], [2,1,-1,0]]
    run_determinant_test_case(m_4x4, 0, "Determinante de matriz 4x4 (exemplo conhecido com det=0)")
    
    # Matriz Identidade 10x10: Determinante de I é sempre 1
    ident_10x10 = generate_matrix(10, 10, lambda r,c: 1 if r==c else 0)
    run_determinant_test_case(ident_10x10, 1, "Determinante de matriz identidade 10x10 (det=1)")
    
    # --- Seção: Casos de Teste de Erro ---
    # Matriz não quadrada
    run_determinant_test_case(
        matrix=[[1,2],[3,4],[5,6]], # Matriz 3x2
        expected_determinant=None, 
        description="Determinante de matriz não quadrada (3x2)", 
        expect_error=True, 
        error_message_contains="deve ser quadrada" # Parte chave da mensagem de erro da validação
    )
    
    # Matriz é None
    run_determinant_test_case(
        matrix=None, 
        expected_determinant=None,
        description="Determinante de Matriz inválida (None)",
        expect_error=True, 
        error_message_contains="Matriz para determinante deve ser uma lista de listas"
    )
    
    # Matriz contém linha vazia (ex: [[]])
    run_determinant_test_case(
        matrix=[[]], 
        expected_determinant=None,
        description="Determinante de Matriz inválida (contém linha vazia [[]])",
        expect_error=True, 
        error_message_contains="Matriz para determinante contém linha(s) vazia(s)"
    )
    
    # Matriz com número inconsistente de colunas
    run_determinant_test_case(
        matrix=[[1,2],[3]], # Linha 0 tem 2 col, Linha 1 tem 1 col
        expected_determinant=None,
        description="Determinante de Matriz com contagem de colunas inconsistente",
        expect_error=True, 
        error_message_contains="Todas as linhas da Matriz para determinante devem ter o mesmo número de colunas"
    )

    print_test_footer("determinant.py", test_count, passed_count)

if __name__ == "__main__":
    test_determinantes()