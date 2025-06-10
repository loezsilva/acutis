from enum import Enum


class ListarCampanhasOrdenarPorEnum(str, Enum):
    campanha_id = 'campanha_id'
    campanha_nome = 'campanha_nome'
    campanha_objetivo = 'campanha_objetivo'
    campanha_publica = 'campanha_publica'
    campanha_ativa = 'campanha_ativa'
    criado_em = 'criado_em'
