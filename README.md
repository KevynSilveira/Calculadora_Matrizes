# Documentação da Calculadora de Matrizes

## 1. Introdução ao Projeto

Esta Calculadora de Matrizes é uma aplicação desenvolvida em **Python** com interface gráfica baseada na biblioteca `Tkinter`, voltada para o estudo e exploração de conceitos fundamentais da álgebra linear. 

O sistema é capaz de realizar operações clássicas sobre matrizes como:

- Soma e subtração
- Multiplicação entre matrizes
- Multiplicação por escalar
- Transposição
- Cálculo de determinante
- Cálculo de inversa
- Resolução de sistemas lineares via inversa (AX = B)

A aplicação é modular: separa a lógica matemática (em `matrix_operations.py`) da interface gráfica (em `app_window.py`, `matrix_input_frame.py`, etc). Isso facilita a manutenção, testes e futuras expansões.

---

## 2. O que são Matrizes

Matrizes são estruturas matemáticas organizadas em linhas e colunas. Cada elemento é acessado por um índice de linha e coluna.

Exemplo de uma matriz 2x3:

```
[1 2 3]
[4 5 6]
```

Matrizes podem representar dados, sistemas de equações, transformações lineares, gráficos e muito mais. Em Python, comumente usamos listas de listas para representar uma matriz.

---

## 3. Resolução de Sistemas AX = B (pela Inversa)

### Conceito

Resolver `AX = B` significa encontrar o vetor X. Isso pode ser feito via inversa:

```
X = A^-1 * B
```

### Código
```python
def solve_linear_system_inverse(matrix_a, vector_b):
    if not matrix_a or not matrix_a[0]:
        raise ValueError("Matriz A (coeficientes) não pode ser vazia.")
    if not vector_b or not vector_b[0]:
        raise ValueError("Vetor B (termos independentes) não pode ser vazio.")

    if len(matrix_a) != len(matrix_a[0]):
        raise ValueError("Matriz A deve ser quadrada.")
    if len(matrix_a) != len(vector_b):
        raise ValueError("Linhas de A devem ser iguais às de B.")
    if len(vector_b[0]) != 1:
        raise ValueError("Vetor B deve ser coluna (Nx1).")

    inv_a = inverse_matrix(matrix_a)
    return multiply_matrices(inv_a, vector_b)
```

---

## 4. Determinante de A

### Conceito

O determinante é um valor escalar associado a uma matriz quadrada. Ele indica se a matriz é invertível (det ≠ 0) e está presente em muitas fórmulas matemáticas.

### Código
```python
def determinant(matrix):
    if len(matrix) != len(matrix[0]):
        raise ValueError("Matriz deve ser quadrada.")
    if len(matrix) == 1:
        return matrix[0][0]
    if len(matrix) == 2:
        return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
    
    det = 0
    for c_col in range(len(matrix)):
        minor = get_minor(matrix, 0, c_col)
        det += ((-1)**c_col) * matrix[0][c_col] * determinant(minor)
    return det
```

---

## 5. Inversa de A

### Conceito

A matriz inversa A⁻¹ satisfaz a relação:

```
A * A⁻¹ = I
```

Onde I é a matriz identidade.

### Código
```python
def inverse_matrix(matrix):
    det_a = determinant(matrix)
    if det_a == 0:
        raise ValueError("A matriz não é invertível.")
    adj_a = adjoint_matrix(matrix)
    return [[adj_a[i][j] / det_a for j in range(len(matrix))] for i in range(len(matrix))]
```

---

## 6. Transposta de A

### Conceito

Troca linhas por colunas. Elemento `[i][j]` se torna `[j][i]`.

### Código
```python
def transpose_matrix(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
```

---

## 7. Soma de Matrizes (A + B)

### Conceito

A + B = matriz somada elemento a elemento. As dimensões devem ser iguais.

### Código
```python
def add_matrices(matrix_a, matrix_b):
    return [[matrix_a[i][j] + matrix_b[i][j] for j in range(len(matrix_a[0]))] for i in range(len(matrix_a))]
```

---

## 8. Subtração de Matrizes (A - B)

### Conceito

Semelhante à soma, mas subtrai os elementos de B dos de A.

### Código
```python
def subtract_matrices(matrix_a, matrix_b):
    return [[matrix_a[i][j] - matrix_b[i][j] for j in range(len(matrix_a[0]))] for i in range(len(matrix_a))]
```

---

## 9. Multiplicação de Matrizes (A * B)

### Conceito

É feita multiplicando as linhas de A pelas colunas de B. A operação só é possível se o número de colunas de A for igual ao número de linhas de B.

### Código
```python
def multiply_matrices(matrix_a, matrix_b):
    return [
        [sum(matrix_a[i][k] * matrix_b[k][j] for k in range(len(matrix_b)))
         for j in range(len(matrix_b[0]))]
        for i in range(len(matrix_a))
    ]
```

---

## 10. Multiplicação por Escalar (A * k)

### Conceito

Multiplica todos os elementos da matriz A por um escalar k.

### Código
```python
def scalar_multiply(matrix, scalar):
    return [[scalar * elem for elem in row] for row in matrix]
```

---

## 11. Considerações Finais

Este projeto oferece uma ferramenta visual e educacional para explorar operações com matrizes. Ele pode ser expandido para suportar outras funcionalidades como:

- Cálculo de autovalores e autovetores
- Decomposição LU ou QR
- Operações com matrizes esparsas
- Exportação/importação de matrizes

Sua modularização facilita a adição de testes automatizados e integração com outras bibliotecas como NumPy.

---
