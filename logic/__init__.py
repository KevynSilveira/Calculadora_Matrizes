# calculadora_matrizes/logic/__init__.py

# Importações relativas (.) para trazer as funções principais de cada módulo
# de operação de matriz para o namespace do pacote 'logic'.
# Isso permite que outros partes do código (como a GUI) importem essas funções
# diretamente de 'logic' (ex: from logic import add_matrices) em vez de ter que
# especificar o módulo completo (ex: from logic.add_matrices import add_matrices).

from .add_matrices import add_matrices
from .subtract_matrices import subtract_matrices
from .multiply_matrices import multiply_matrices
from .scalar_multiply import scalar_multiply
from .transpose_matrix import transpose_matrix
from .determinant import determinant
from .inverse_matrix import inverse_matrix
from .solve_linear_system import solve_linear_system_inverse 
                                                           
# A variável especial __all__ define a interface pública do pacote 'logic'.
# Quando um usuário faz 'from logic import *', apenas os nomes listados em __all__
# serão importados. Isso ajuda a evitar a poluição do namespace do importador
# com módulos ou variáveis internas do pacote que não são destinadas ao uso externo direto.
# Neste caso, estamos exportando todas as funções de operação de matriz que foram importadas acima.
__all__ = [
    "add_matrices",
    "subtract_matrices",
    "multiply_matrices",
    "scalar_multiply",
    "transpose_matrix",
    "determinant",
    "inverse_matrix",
    "solve_linear_system_inverse", 
    # Funções de validation_utils.py e helper_utils.py não estão listadas aqui
    # pois são consideradas utilitários internos para o pacote 'logic' e não
    # parte de sua API pública primária para o resto da aplicação.
]