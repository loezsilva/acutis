from typing import List

import pandas as pd

from acutis_api.application.utils.funcoes_auxiliares import exporta_csv
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.domain.repositories.schemas.agape import (
    DadosExportacaoFamiliaSchema,
)


class ExportarFamiliasAgapeUseCase:
    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self.agape_repository = agape_repository

    def execute(self) -> dict:
        dados_exportacao: List[DadosExportacaoFamiliaSchema] = (
            self.agape_repository.buscar_dados_completos_familias_agape()
        )

        if not dados_exportacao:
            return {'url': None}

        dados_formatados = []
        for dado in dados_exportacao:
            dados_formatados.append({
                'familia_id': str(dado.familia_id),
                'familia_nome': dado.familia_nome or '',
                'familia_data_cadastro': str(
                    dado.familia_data_cadastro.strftime('%d/%m/%Y %H:%M:%S')
                    if dado.familia_data_cadastro
                    else '',
                ),
                'familia_status': dado.familia_status or '',
                'familia_observacao': dado.familia_observacao or '',
                'endereco_logradouro': dado.endereco_logradouro or '',
                'endereco_numero': dado.endereco_numero or '',
                'endereco_complemento': dado.endereco_complemento or '',
                'endereco_bairro': dado.endereco_bairro or '',
                'endereco_cidade': dado.endereco_cidade or '',
                'endereco_estado': dado.endereco_estado or '',
                'endereco_cep': dado.endereco_cep or '',
                'responsavel_nome': dado.responsavel_nome or '',
                'responsavel_cpf': dado.responsavel_cpf or '',
                'responsavel_telefone': dado.responsavel_telefone or '',
                'responsavel_email': dado.responsavel_email or '',
                'responsavel_data_nascimento': str(
                    dado.responsavel_data_nascimento.strftime('%d/%m/%Y')
                    if dado.responsavel_data_nascimento
                    else '',
                ),
                'responsavel_funcao_familiar': (
                    dado.responsavel_funcao_familiar or ''
                ),
                'responsavel_escolaridade': (
                    dado.responsavel_escolaridade or ''
                ),
                'responsavel_ocupacao': dado.responsavel_ocupacao or '',
                'numero_total_membros': str(
                    str(dado.numero_total_membros)
                    if dado.numero_total_membros is not None
                    else '0',
                ),
                'renda_familiar_total_estimada': float(
                    float(dado.renda_familiar_total_estimada)
                    if dado.renda_familiar_total_estimada is not None
                    else '0.00',
                ),
                'comprovante_residencia_url': (
                    dado.comprovante_residencia_url or ''
                ),
                'cadastrada_por_usuario_id': (
                    str(dado.cadastrada_por_usuario_id)
                    if dado.cadastrada_por_usuario_id
                    else ''
                ),
            })

        df = pd.DataFrame(dados_formatados)

        return {'url': exporta_csv(df, 'familias_agape')['url']}
