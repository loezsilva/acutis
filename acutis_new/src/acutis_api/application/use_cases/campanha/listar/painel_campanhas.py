from datetime import datetime, timedelta

from acutis_api.application.utils.funcoes_auxiliares import buscar_data_valida
from acutis_api.communication.enums.campanhas import (
    ObjetivosCampanhaEnum,
    PeriodicidadePainelCampanhasEnum,
)
from acutis_api.communication.requests.campanha import PainelCampanhasRequest
from acutis_api.communication.responses.campanha import (
    PainelCampanhasResponse,
    PainelCampanhasSchema,
)
from acutis_api.domain.repositories.campanha import CampanhaRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class PainelCampanhasUseCase:
    def __init__(self, repository: CampanhaRepositoryInterface):
        self.__repository = repository

    def execute(self, request: PainelCampanhasRequest):
        campanhas = []
        periodo_map = define_periodo_map()
        hoje = datetime.now()

        for campanha in request.lista_painel:
            campanha_e_landing = self.__repository.buscar_campanha_por_id(
                campanha.campanha_id
            )

            if not campanha_e_landing:
                raise HttpNotFoundError(
                    f'Campanha com ID {campanha.campanha_id} não encontrada.'
                )

            dados_campanha = campanha_e_landing[0]

            (inicio_atual, fim_atual), (inicio_anterior, fim_anterior) = (
                periodo_map[campanha.periodicidade](hoje)
            )

            if dados_campanha.objetivo == ObjetivosCampanhaEnum.doacao:
                valor = self.__repository.buscar_valor_arrecadado_periodo(
                    campanha.campanha_id, inicio_atual, fim_atual
                )
                valor_anterior = (
                    self.__repository.buscar_valor_arrecadado_periodo(
                        campanha.campanha_id, inicio_anterior, fim_anterior
                    )
                )
            elif dados_campanha.objetivo in {
                ObjetivosCampanhaEnum.pre_cadastro,
                ObjetivosCampanhaEnum.cadastro,
                ObjetivosCampanhaEnum.oficiais,
            }:
                valor = self.__repository.buscar_cadastros_campanha_periodo(
                    campanha.campanha_id, inicio_atual, fim_atual
                )
                valor_anterior = (
                    self.__repository.buscar_cadastros_campanha_periodo(
                        campanha.campanha_id, inicio_anterior, fim_anterior
                    )
                )
            porcentagem_crescimento = (
                round(((valor - valor_anterior) / valor_anterior) * 100, 2)
                if valor_anterior != 0
                else 0
            )

            valor = round(valor, 2)

            response_campanha = PainelCampanhasSchema(
                nome_campanha=dados_campanha.nome,
                objetivo=dados_campanha.objetivo,
                total=valor,
                periodicidade=campanha.periodicidade,
                porcentagem_crescimento=porcentagem_crescimento,
            ).model_dump()

            campanhas.append(response_campanha)

        return PainelCampanhasResponse(campanhas=campanhas).model_dump()


def define_periodo_map():
    def periodo_diario(ref: datetime):
        hoje = ref
        ontem = ref - timedelta(days=1)
        inicio_hoje = datetime.combine(hoje.date(), datetime.min.time())
        inicio_ontem = datetime.combine(ontem.date(), datetime.min.time())

        return (inicio_hoje, hoje), (inicio_ontem, ontem)

    def periodo_semanal(ref: datetime):
        hoje = ref
        inicio_semana_atual = datetime.combine(
            (ref - timedelta(days=ref.weekday())).date(), datetime.min.time()
        )

        inicio_semana_anterior = datetime.combine(
            (inicio_semana_atual - timedelta(days=7)).date(),
            datetime.min.time(),
        )

        fim_semana_anterior = inicio_semana_atual - timedelta(days=1)

        return (inicio_semana_atual, hoje), (
            inicio_semana_anterior,
            fim_semana_anterior,
        )

    def periodo_mensal(ref: datetime):
        hoje = ref

        inicio_mes_atual = datetime.combine(
            ref.replace(day=1).date(), datetime.min.time()
        )

        ultimo_dia_mes_anterior = ref.replace(day=1) - timedelta(days=1)
        mes_anterior = ultimo_dia_mes_anterior.month
        ano_anterior = ultimo_dia_mes_anterior.year

        inicio_mes_anterior = datetime.combine(
            ultimo_dia_mes_anterior.replace(day=1).date(), datetime.min.time()
        )

        fim_mes_anterior = datetime.combine(
            buscar_data_valida(ref.day, mes_anterior, ano_anterior),
            datetime.max.time(),
        )

        return (inicio_mes_atual, hoje), (
            inicio_mes_anterior,
            fim_mes_anterior,
        )

    return {
        PeriodicidadePainelCampanhasEnum.diario: periodo_diario,
        PeriodicidadePainelCampanhasEnum.semanal: periodo_semanal,
        PeriodicidadePainelCampanhasEnum.mensal: periodo_mensal,
    }
