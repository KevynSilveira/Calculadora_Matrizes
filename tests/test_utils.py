# calculadora_matrizes/tests/test_utils.py
import math
import sys
import os

# Adiciona o diretório pai (calculadora_matrizes) ao sys.path
# para permitir imports de 'logic' quando os testes são executados diretamente.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

TOLERANCE = 1e-9  # Tolerância para comparação de floats

def format_matrix_for_log(matrix, name="Matriz"):
    """Formata uma matriz (ou escalar) para exibição no log de teste."""
    header = f"    {name}:"
    if matrix is None:
        return f"{header} None"
    
    # Se for um escalar (como resultado de determinante)
    if isinstance(matrix, (int, float)):
        return f"{header} {matrix}"

    if not isinstance(matrix, list):
        return f"{header} [Tipo Inválido: {type(matrix)}]"
    if not matrix:
        return f"{header} [Lista Vazia (representando matriz vazia)]"
    
    # Verifica se é uma lista de listas (matriz) ou uma lista simples (vetor)
    is_matrix_of_lists = all(isinstance(row, list) for row in matrix)

    if not is_matrix_of_lists: # Provavelmente um vetor resultado de AX=B ou uma matriz malformada
        # Tenta formatar como um vetor se for lista de números
        if all(isinstance(item, (int, float)) for item in matrix):
             return f"{header} {matrix}" # Simplesmente imprime a lista
        return f"{header} [Estrutura Inválida detectada: não é lista de listas ou escalar]"


    if not matrix[0] and len(matrix) > 0: # Ex: [[]]
        lines = [header, "      [Matriz com Linha(s) Vazia(s) ou Malformada]"]
        return "\n".join(lines)
    
    # Formatação para matrizes (lista de listas)
    try:
        num_cols = len(matrix[0]) if matrix and matrix[0] else 0
        col_widths = [0] * num_cols
        
        # Preparar strings e calcular larguras das colunas
        str_matrix = []
        for row_val in matrix:
            if len(row_val) != num_cols: # Checagem de consistência de colunas
                 lines = [header, "      [Inconsistência no número de colunas entre as linhas]"]
                 for r_print in matrix: lines.append(f"        {r_print}")
                 return "\n".join(lines)

            str_row = []
            for c_idx, val in enumerate(row_val):
                if isinstance(val, float):
                    # Formatação para floats para evitar excesso de casas decimais
                    if math.isclose(val, round(val), abs_tol=TOLERANCE): # Se próximo de um inteiro
                        s_val = str(round(val))
                    else:
                        s_val = f"{val:.4g}".rstrip('0').rstrip('.') # Formato geral, até 4 sig. figs
                    if s_val == "-0": s_val = "0"
                else:
                    s_val = str(val)
                str_row.append(s_val)
                if c_idx < num_cols: # Evita IndexError se num_cols foi 0
                    col_widths[c_idx] = max(col_widths[c_idx], len(s_val))
            str_matrix.append(str_row)

        # Construir a string da matriz formatada
        lines = [header]
        for str_row_val in str_matrix:
            line = "      ["
            for c_idx, s_val in enumerate(str_row_val):
                line += f"{s_val:>{col_widths[c_idx]}}"
                if c_idx < num_cols - 1:
                    line += ", "
            line += "]"
            lines.append(line)
        return "\n".join(lines)

    except Exception as e:
        return f"{header} [Erro ao formatar matriz: {e}]\n      Matriz Original: {matrix}"


def are_matrices_equal(m1, m2):
    """Compara duas matrizes (listas de listas de números) ou escalares com tolerância."""
    if type(m1) != type(m2):
        # Permite comparação entre int e float se numericamente próximos
        if isinstance(m1, (int, float)) and isinstance(m2, (int, float)):
            pass # Prossegue para a comparação com math.isclose
        else:
            return False

    if isinstance(m1, (int, float)): # Comparar escalares
        return math.isclose(m1, m2, rel_tol=TOLERANCE, abs_tol=TOLERANCE)
    
    if not isinstance(m1, list) or not isinstance(m2, list): return False
    if len(m1) != len(m2): return False
    if not m1 and not m2: return True # Ambas vazias [[ ]] ou []
    if not m1 or not m2: return False # Uma vazia e outra não

    # Checa se é lista de listas ou lista de números (vetor)
    m1_is_matrix = all(isinstance(row, list) for row in m1)
    m2_is_matrix = all(isinstance(row, list) for row in m2)

    if m1_is_matrix != m2_is_matrix: return False

    if not m1_is_matrix: # São vetores (lista de números)
        for i in range(len(m1)):
            if not isinstance(m1[i], (int, float)) or not isinstance(m2[i], (int, float)): return False # Elemento não numérico
            if not math.isclose(m1[i], m2[i], rel_tol=TOLERANCE, abs_tol=TOLERANCE): return False
        return True

    # São matrizes (lista de listas)
    for i in range(len(m1)):
        if not isinstance(m1[i], list) or not isinstance(m2[i], list): return False # Linha não é lista
        if len(m1[i]) != len(m2[i]): return False
        for j in range(len(m1[i])):
            if not isinstance(m1[i][j], (int, float)) or not isinstance(m2[i][j], (int, float)): return False # Elemento não numérico
            if not math.isclose(m1[i][j], m2[i][j], rel_tol=TOLERANCE, abs_tol=TOLERANCE):
                return False
    return True

def generate_matrix(rows, cols, value_generator=lambda r, c: r * cols + c + 1):
    """Gera uma matriz com base em uma função geradora de valor."""
    return [[value_generator(r, c) for c in range(cols)] for r in range(rows)]

def print_test_header(test_file_name):
    print("-" * 70)
    print(f"INICIANDO TESTES PARA: {test_file_name}")
    print("-" * 70)

def print_test_footer(test_file_name, total_tests, passed_tests):
    print("-" * 70)
    print(f"TESTES CONCLUÍDOS PARA: {test_file_name}")
    print(f"Total de Casos de Teste: {total_tests}")
    print(f"Passaram: {passed_tests}")
    print(f"Falharam: {total_tests - passed_tests}")
    print("-" * 70)
    print("\n")