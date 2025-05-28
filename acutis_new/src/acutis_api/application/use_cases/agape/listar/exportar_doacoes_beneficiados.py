import csv
import io
import uuid
from typing import List

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

        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)

        headers = [
            'ciclo_acao_id',
            'ciclo_acao_nome',
            'ciclo_acao_data_inicio',
            'ciclo_acao_data_termino',
            'familia_id',
            'familia_nome',
            'familia_observacao',
            'responsavel_familia_nome',
            'responsavel_familia_cpf',
            'responsavel_familia_telefone',
            'doacao_id',
            'doacao_data',
            'item_doado_nome',
            'item_doado_quantidade',
        ]
        writer.writerow(headers)

        for dado in dados_exportacao:
            writer.writerow([
                str(dado.ciclo_acao_id) if dado.ciclo_acao_id else '',
                dado.ciclo_acao_nome or '',
                (
                    dado.ciclo_acao_data_inicio.strftime('%Y-%m-%d %H:%M:%S')
                    if dado.ciclo_acao_data_inicio
                    else '',
                ),
                (
                    dado.ciclo_acao_data_termino.strftime('%Y-%m-%d %H:%M:%S')
                    if dado.ciclo_acao_data_termino
                    else '',
                ),
                str(dado.familia_id) if dado.familia_id else '',
                dado.familia_nome or '',
                dado.familia_observacao or '',
                dado.responsavel_familia_nome or '',
                dado.responsavel_familia_cpf or '',
                dado.responsavel_familia_telefone or '',
                str(dado.doacao_id) if dado.doacao_id else '',
                (
                    dado.doacao_data.strftime('%Y-%m-%d %H:%M:%S')
                    if dado.doacao_data
                    else '',
                ),
                dado.item_doado_nome or '',
                (
                    str(dado.item_doado_quantidade)
                    if dado.item_doado_quantidade is not None
                    else ''
                ),
            ])

        return output.getvalue()
