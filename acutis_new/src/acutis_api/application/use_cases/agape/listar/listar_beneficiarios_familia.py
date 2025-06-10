import uuid
from datetime import date

from acutis_api.communication.responses.agape import (
    BeneficiarioFamiliaResponse,
    EnderecoResponse,
    ListarBeneficiariosAgapeResponse,
    MembroFamiliaAgapeResponse,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class ListarBeneficiariosAgapeUseCase:
    """
    Caso de uso para listar os beneficiários de um ciclo de ação ágape.
    """

    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self.agape_repository = agape_repository

    def _calcular_idade(self, data_nascimento: date | None) -> int | None:
        if not data_nascimento:
            return None
        hoje = date.today()
        idade = (
            hoje.year
            - data_nascimento.year
            - (
                (hoje.month, hoje.day)
                < (data_nascimento.month, data_nascimento.day)
            )
        )
        return idade

    def execute(
        self, ciclo_acao_id: uuid.UUID
    ) -> ListarBeneficiariosAgapeResponse:
        ciclo_acao = self.agape_repository.buscar_ciclo_acao_agape_por_id(
            ciclo_acao_id
        )

        if ciclo_acao is None:
            raise HttpNotFoundError('Ciclo de ação não encontrado.')

        familias_beneficiadas = (
            self.agape_repository.listar_familias_beneficiadas_por_ciclo_id(
                ciclo_acao_id=ciclo_acao_id
            )
        )

        beneficiarios_response_list = []
        if familias_beneficiadas:
            for familia_entity in familias_beneficiadas:
                membros_response = []
                if (
                    hasattr(familia_entity, 'membros')
                    and familia_entity.membros
                ):
                    for membro_entity in familia_entity.membros:
                        membros_response.append(
                            MembroFamiliaAgapeResponse(
                                id=membro_entity.id,
                                cpf=membro_entity.cpf,
                                nome=membro_entity.nome,
                                email=membro_entity.email,
                                telefone=membro_entity.telefone,
                                ocupacao=membro_entity.ocupacao,
                                renda=membro_entity.renda,
                                responsavel=membro_entity.responsavel,
                                idade=self._calcular_idade(
                                    getattr(
                                        membro_entity, 'data_nascimento', None
                                    )
                                ),
                            )
                        )

                endereco_response = None
                if familia_entity.fk_endereco_id:
                    endereco_entity = (
                        self.agape_repository.buscar_endereco_por_id(
                            familia_entity.fk_endereco_id
                        )
                    )
                    endereco_response = EnderecoResponse(
                        id=endereco_entity.id,
                        codigo_postal=endereco_entity.codigo_postal,
                        logradouro=endereco_entity.logradouro,
                        bairro=endereco_entity.bairro,
                        cidade=endereco_entity.cidade,
                        estado=endereco_entity.estado,
                        numero=endereco_entity.numero,
                        complemento=endereco_entity.complemento,
                    )

                beneficiarios_response_list.append(
                    BeneficiarioFamiliaResponse(
                        id=familia_entity.id,
                        nome_familia=familia_entity.nome_familia,
                        observacao=getattr(familia_entity, 'observacao', None),
                        membros=membros_response,
                        endereco=endereco_response,
                    )
                )

        return ListarBeneficiariosAgapeResponse(
            root=beneficiarios_response_list
        ).model_dump()
