import uuid
from typing import List

import pandas as pd

from acutis_api.application.utils.funcoes_auxiliares import exporta_csv
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.domain.repositories.schemas.agape import (
    DadosCompletosDoacaoSchema,
)
from acutis_api.exception.errors.not_found import HttpNotFoundError


class ExportarDoacoesBeneficiadosUseCase:
    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self.agape_repository = agape_repository

    def execute(self, ciclo_acao_id: uuid.UUID) -> str:
        ciclo_acao = self.agape_repository.buscar_ciclo_acao_agape_por_id(
            ciclo_acao_id
        )

        if not ciclo_acao:
            raise HttpNotFoundError(
                f'Ciclo de Ação com ID {ciclo_acao_id} não encontrado.'
            )

        dados_exportacao: List[DadosCompletosDoacaoSchema] = (
            self.agape_repository.buscar_dados_exportacao_doacoes_ciclo(
                ciclo_acao_id
            )
        )

        if not dados_exportacao:
            return {'url': None}

        dados_formatados = []
        for dado in dados_exportacao:
            dados_formatados.append({
                'ciclo_acao_id': str(
                    str(dado.ciclo_acao_id) if dado.ciclo_acao_id else ''
                ),
                'ciclo_acao_nome': dado.ciclo_acao_nome or '',
                'ciclo_acao_data_inicio': str(
                    dado.ciclo_acao_data_inicio.strftime('%d/%m/%Y %H:%M:%S')
                    if dado.ciclo_acao_data_inicio
                    else '',
                ),
                'ciclo_acao_data_termino': str(
                    dado.ciclo_acao_data_termino.strftime('%d/%m/%Y %H:%M:%S')
                    if dado.ciclo_acao_data_termino
                    else '',
                ),
                'familia_id': str(dado.familia_id) if dado.familia_id else '',
                'familia_nome': dado.familia_nome or '',
                'familia_observacao': dado.familia_observacao or '',
                'responsavel_familia_nome': str(
                    dado.responsavel_familia_nome or ''
                ),
                'responsavel_familia_cpf': dado.responsavel_familia_cpf or '',
                'responsavel_familia_telefone': (
                    dado.responsavel_familia_telefone or ''
                ),
                'doacao_id': str(dado.doacao_id) if dado.doacao_id else '',
                'doacao_data': str(
                    dado.doacao_data.strftime('%d/%m/%Y %H:%M:%S')
                    if dado.doacao_data
                    else '',
                ),
                'item_doado_nome': dado.item_doado_nome or '',
                'item_doado_quantidade': str(
                    str(dado.item_doado_quantidade)
                    if dado.item_doado_quantidade is not None
                    else ''
                ),
            })

        df = pd.DataFrame(dados_formatados)

        return {'url': exporta_csv(df, 'familias_agape')['url']}
