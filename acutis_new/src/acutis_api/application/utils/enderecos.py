from acutis_api.communication.requests.agape import EnderecoAgapeFormData
from acutis_api.domain.entities.instancia_acao_agape import (
    AbrangenciaInstanciaAcaoAgapeEnum,
)


def generate_address_string(
    endereco: EnderecoAgapeFormData,
    abrangencia: AbrangenciaInstanciaAcaoAgapeEnum,
    pais: str = 'Brasil',
) -> str:
    mappings = {
        'sem_restricao': pais,
        'cidade': f'{endereco.cidade}, {endereco.estado}, {pais}',
        'bairro': f"""{endereco.bairro}, {endereco.cidade},
        {endereco.estado}, {pais}
        """,
        'estado': f'{endereco.estado}, {pais}',
        'cep': f'{endereco.cep}, {pais}',
        'rua': f"""{endereco.rua}, {endereco.bairro},
        {endereco.cidade}, {endereco.estado}, {endereco.cep}
        """,
    }

    return mappings[abrangencia]
