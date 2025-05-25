from flask_jwt_extended import current_user
from models.vocacional.usuario_vocacional import VocationalGendersEnum


def _verificar_permissao_genero(tipo_permissao: str) -> str:
    masculino = current_user["permissoes"]["vocacional_masculino"][tipo_permissao] == 1
    feminino = current_user["permissoes"]["vocacional_feminino"][tipo_permissao] == 1

    if feminino and masculino:
        return "todos"
    if feminino:
        return VocationalGendersEnum.FEMININO
    if masculino:
        return VocationalGendersEnum.MASCULINO
    return "nenhum"


def verificar_permissoes_vocacional() -> dict:

    permissoes = {
        "acessar": _verificar_permissao_genero("acessar"),
        "editar": _verificar_permissao_genero("editar"),
        "deletar": _verificar_permissao_genero("deletar"),
    }

    return permissoes
