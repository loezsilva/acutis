from acutis_api.communication.requests.membros_oficiais import (
    RegistrarMembroOficialRequest,
)
from acutis_api.communication.responses.membros_oficiais import (
    RegistrarNovoMembroOficialResponse,
)
from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.repositories.membros_oficiais import (
    MembrosOficiaisRepositoryInterface,
)
from acutis_api.domain.services.enviar_notificacao import (
    AssuntosEmailEnum,
    EnviarNotificacaoInterface,
)
from acutis_api.domain.templates.email_templates import (
    send_email_cadastro_membro_oficial_recebido,
)
from acutis_api.exception.errors.bad_request import HttpBadRequestError
from acutis_api.exception.errors.conflict import HttpConflictError


class RegistrarNovoMembroOficialUseCase:
    def __init__(
        self,
        repository: MembrosOficiaisRepositoryInterface,
        notification: EnviarNotificacaoInterface,
    ):
        self.__notification = notification
        self.__repository = repository

    def execute(
        self, requisicao: RegistrarMembroOficialRequest
    ) -> RegistrarNovoMembroOficialResponse:
        membro_oficial_ja_cadastrado = (
            self.__repository.buscar_oficial_por_fk_membro_id(
                requisicao.fk_membro_id
            )
        )

        verificar_membro: Lead = self.__repository.busca_membro_por_id(
            requisicao.fk_membro_id
        )

        if verificar_membro is None:
            raise HttpBadRequestError('É necessário ter o cadastro de membro')

        if membro_oficial_ja_cadastrado is not None:
            raise HttpConflictError('Esse membro já é um membro oficial.')

        if requisicao.fk_membro_id == requisicao.fk_superior_id:
            raise HttpBadRequestError('Não é possível vincular-se a se mesmo.')

        # adicionar verificação se a campanha do oficial permite cadastro
        # para o fk_usuario_superior_id informado na requisicao

        novo_membro_oficial = self.__repository.registrar_novo_membro_oficial(
            requisicao
        )

        conteudo = send_email_cadastro_membro_oficial_recebido(
            verificar_membro.nome
        )

        self.__notification.enviar_email(
            verificar_membro.email, AssuntosEmailEnum.membro_oficial, conteudo
        )

        self.__repository.salvar_dados()

        return RegistrarNovoMembroOficialResponse(
            uuid=novo_membro_oficial.id,
            criado_em=novo_membro_oficial.criado_em.strftime(
                '%d/%m/%y %H:%M:%S'
            ),
        ).model_dump()
