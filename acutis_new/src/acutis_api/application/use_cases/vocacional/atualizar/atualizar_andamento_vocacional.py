from acutis_api.application.utils.vocacional import (
    envia_email_vocacional,
)
from acutis_api.communication.enums.vocacional import (
    AprovacaoEnum,
    PassosVocacionalStatusEnum,
)
from acutis_api.communication.requests.vocacional import (
    AtualizarAndamentoVocacionalRequest,
)
from acutis_api.communication.responses.padrao import ResponsePadraoSchema
from acutis_api.domain.repositories.vocacional import (
    InterfaceVocacionalRepository,
)
from acutis_api.exception.errors_handler import (
    HttpConflictError,
    HttpNotFoundError,
)


class AtualizarAndamentoVocacionalUseCase:
    def __init__(self, vocacional_repository: InterfaceVocacionalRepository):
        self.__vocacional_repository = vocacional_repository

    def execute(self, request: AtualizarAndamentoVocacionalRequest):
        usuario_vocacional_id = request.usuario_vocacional_id
        acao = request.acao

        if not self.__vocacional_repository.verifica_usuario_vocacional(
            usuario_vocacional_id
        ):
            raise HttpNotFoundError('Usuário não encontrado')
        etapa_atual = self.__vocacional_repository.busca_etapa_atual(
            usuario_vocacional_id
        )
        if not etapa_atual:
            raise HttpNotFoundError('Nenhuma etapa encontrada')

        if acao == AprovacaoEnum.aprovar:
            if etapa_atual.status != PassosVocacionalStatusEnum.pendente:
                raise HttpConflictError(
                    'Usuário já aprovado, reprovado ou desistiu.'
                )
            self.__vocacional_repository.aprovar_para_proximo_passo(
                etapa_atual
            )
            self.__vocacional_repository.salvar_alteracoes()

            vocacional = self.__vocacional_repository.busca_vocacional(
                usuario_vocacional_id
            )
            envia_email_vocacional(vocacional)
            return ResponsePadraoSchema(msg='Vocacional aprovado com sucesso.')

        elif acao == AprovacaoEnum.reprovar:
            if etapa_atual.status != PassosVocacionalStatusEnum.pendente:
                raise HttpConflictError(
                    'Usuário já aprovado, reprovado ou desistiu.'
                )
            self.__vocacional_repository.reprovar_para_proximo_passo(
                etapa_atual,
                request.justificativa if request.justificativa else None,
            )
            self.__vocacional_repository.salvar_alteracoes()

            return ResponsePadraoSchema(
                msg='Vocacional reprovado com sucesso.'
            )
