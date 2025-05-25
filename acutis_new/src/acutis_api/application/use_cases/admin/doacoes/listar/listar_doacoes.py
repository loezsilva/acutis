import math

from acutis_api.communication.requests.admin_doacoes import ListarDoacoesQuery
from acutis_api.communication.responses.admin_doacoes import (
    DadosBenfeitorSchema,
    DadosCampanhaSchema,
    DadosDoacaoSchema,
    ListarDoacoesResponse,
    ListarDoacoesSchema,
)
from acutis_api.domain.repositories.admin_doacoes import (
    AdminDoacoesRepositoryInterface,
)


class ListarDoacoesUseCase:
    def __init__(self, repository: AdminDoacoesRepositoryInterface):
        self._repository = repository

    def execute(self, filtros: ListarDoacoesQuery):
        doacoes, total = self._repository.listar_doacoes(filtros)

        response = ListarDoacoesResponse(
            pagina=filtros.pagina,
            paginas=math.ceil(total / filtros.por_pagina),
            total=total,
            doacoes=[
                ListarDoacoesSchema(
                    benfeitor=DadosBenfeitorSchema(
                        id=doacao.benfeitor_id,
                        nome=doacao.benfeitor_nome,
                        lead_id=doacao.lead_id,
                        membro_id=doacao.membro_id,
                    ),
                    campanha=DadosCampanhaSchema(
                        id=doacao.campanha_id,
                        nome=doacao.campanha_nome,
                    ),
                    doacao=DadosDoacaoSchema(
                        id=doacao.doacao_id,
                        criada_em=doacao.doacao_criada_em,
                        cancelada_em=doacao.doacao_cancelada_em,
                        pagamento_doacao_id=doacao.pagamento_doacao_id,
                        valor_doacao=doacao.valor_doacao,
                        recorrente=doacao.recorrente,
                        forma_pagamento=doacao.forma_pagamento,
                        codigo_ordem_pagamento=doacao.codigo_ordem_pagamento,
                        anonimo=doacao.anonimo,
                        gateway=doacao.gateway,
                        ativo=doacao.ativo,
                        processamento_doacao_id=doacao.processamento_doacao_id,
                        processado_em=doacao.processado_em,
                        codigo_referencia=doacao.codigo_referencia,
                        codigo_transacao=doacao.codigo_transacao,
                        codigo_comprovante=doacao.codigo_comprovante,
                        nosso_numero=doacao.nosso_numero,
                        status=doacao.status,
                    ),
                )
                for doacao in doacoes
            ],
        ).model_dump()

        return response
