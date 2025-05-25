from acutis_api.communication.enums.membros_oficiais import (
    AdminAcaoMembroOficialEnum,
    StatusOficialEnum,
)
from acutis_api.communication.requests.admin_membros_oficiais import (
    AlterarStatusMembroOficialRequest,
)
from acutis_api.communication.responses.padrao import ResponsePadraoSchema
from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.repositories.enums.membros_oficiais import (
    StatusMembroOficialEnum,
)
from acutis_api.domain.repositories.membros_oficiais import (
    MembrosOficiaisRepositoryInterface,
)
from acutis_api.domain.services.enviar_notificacao import (
    AssuntosEmailEnum,
    EnviarNotificacaoInterface,
)
from acutis_api.domain.templates.email_templates import (
    send_cadastro_membro_oficial_aprovado,
)
from acutis_api.exception.errors.conflict import HttpConflictError
from acutis_api.exception.errors.not_found import HttpNotFoundError


class AlterarStatusMembroOficialUseCase:
    def __init__(
        self,
        repository: MembrosOficiaisRepositoryInterface,
        notification: EnviarNotificacaoInterface,
    ):
        self.__repository = repository
        self.__notification = notification

    def execute(
        self, requisicao: AlterarStatusMembroOficialRequest
    ) -> dict[ResponsePadraoSchema]:
        busca_membro_oficial = self.__repository.buscar_membro_oficial_por_id(
            requisicao.fk_membro_oficial_id
        )

        if busca_membro_oficial is None:
            raise HttpNotFoundError('Membro oficial não encontrado')

        cadastro_de_membro: Lead = self.__repository.busca_membro_por_id(
            busca_membro_oficial.fk_membro_id
        )

        if requisicao.acao == AdminAcaoMembroOficialEnum.aprovar:
            if busca_membro_oficial.status == StatusOficialEnum.aprovado:
                raise HttpConflictError('Membro oficial já aprovado')
            else:
                oficial_atualizado = (
                    self.__repository.atualizar_status_membro_oficial(
                        busca_membro_oficial, StatusOficialEnum.aprovado
                    )
                )

                conteudo = send_cadastro_membro_oficial_aprovado(
                    cadastro_de_membro.nome
                )

                self.__notification.enviar_email(
                    cadastro_de_membro.email,
                    AssuntosEmailEnum.membro_oficial,
                    conteudo,
                )

        if requisicao.acao == AdminAcaoMembroOficialEnum.recusar:
            if busca_membro_oficial.status == StatusMembroOficialEnum.recusado:
                raise HttpConflictError('Membro oficial já recusado')
            else:
                oficial_atualizado = (
                    self.__repository.atualizar_status_membro_oficial(
                        busca_membro_oficial, StatusOficialEnum.recusado
                    )
                )

        self.__repository.salvar_dados()

        return oficial_atualizado.status.value
