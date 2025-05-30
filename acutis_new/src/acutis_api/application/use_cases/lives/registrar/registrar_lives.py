from flask_jwt_extended import current_user

from acutis_api.communication.enums.lives import TipoProgramacaoLiveEnum
from acutis_api.communication.requests.lives import RegistrarLiveRequest
from acutis_api.communication.responses.padrao import (
    ResponsePadraoSchema,
)
from acutis_api.domain.repositories.lives import LivesRepositoryInterface


class RegistrarLiveUseCase:
    def __init__(self, lives_repository: LivesRepositoryInterface):
        self.repository = lives_repository

    def execute(self, request: RegistrarLiveRequest) -> ResponsePadraoSchema:
        tipo = request.tipo

        if tipo == TipoProgramacaoLiveEnum.AVULSA:
            return self.__registrar_live_avulsa(request)
        elif tipo == TipoProgramacaoLiveEnum.RECORRENTE:
            return self.__registrar_live_recorrente(request)

    def __registrar_live_avulsa(
        self, request: RegistrarLiveRequest
    ) -> ResponsePadraoSchema:
        lives_avulsas = [
            {
                'data_hora_inicio': request.data_hora_inicio,
                'fk_live_id': canal_id,
                'criado_por': current_user.membro.id,
            }
            for canal_id in request.canais_ids
        ]

        self.repository.registrar_live_avulsa(lives_avulsas)
        self.repository.salvar_dados()
        return ResponsePadraoSchema(msg='Live registrada com sucesso.')

    def __registrar_live_recorrente(
        self, request: RegistrarLiveRequest
    ) -> ResponsePadraoSchema:
        lives_recorrentes = []

        for programacao in request.programacoes:
            for canal_id in request.canais_ids:
                lives_recorrentes.append({
                    'dia_semana': programacao.dia_semana,
                    'hora_inicio': programacao.hora_inicio,
                    'fk_live_id': canal_id,
                    'criado_por': current_user.membro.id,
                })

        self.repository.registrar_live_recorrente(lives_recorrentes)
        self.repository.salvar_dados()
        return ResponsePadraoSchema(msg='Live registrada com sucesso.')
