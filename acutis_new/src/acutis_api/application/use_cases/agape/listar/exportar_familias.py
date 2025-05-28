import csv
import io
from typing import List

from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.domain.repositories.schemas.agape import (
    DadosExportacaoFamiliaSchema,
)


class ExportarFamiliasAgapeUseCase:
    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self.agape_repository = agape_repository

    def execute(self) -> str:
        dados_exportacao: List[DadosExportacaoFamiliaSchema] = (
            self.agape_repository.buscar_dados_completos_familias_agape()
        )

        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)

        headers = [
            'familia_id',
            'familia_nome',
            'familia_data_cadastro',
            'familia_status',
            'familia_observacao',
            'endereco_logradouro',
            'endereco_numero',
            'endereco_complemento',
            'endereco_bairro',
            'endereco_cidade',
            'endereco_estado',
            'endereco_cep',
            'responsavel_nome',
            'responsavel_cpf',
            'responsavel_telefone',
            'responsavel_email',
            'responsavel_data_nascimento',
            'responsavel_funcao_familiar',
            'responsavel_escolaridade',
            'responsavel_ocupacao',
            'numero_total_membros',
            'renda_familiar_total_estimada',
            'comprovante_residencia_url',
            'cadastrada_por_usuario_id',
        ]
        writer.writerow(headers)

        if not dados_exportacao:
            return output.getvalue()

        for dado in dados_exportacao:
            writer.writerow([
                str(dado.familia_id),  # UUID
                dado.familia_nome or '',
                (
                    dado.familia_data_cadastro.strftime('%Y-%m-%d %H:%M:%S')
                    if dado.familia_data_cadastro
                    else '',
                ),
                dado.familia_status or '',
                dado.familia_observacao or '',
                dado.endereco_logradouro or '',
                dado.endereco_numero or '',
                dado.endereco_complemento or '',
                dado.endereco_bairro or '',
                dado.endereco_cidade or '',
                dado.endereco_estado or '',
                dado.endereco_cep or '',
                dado.responsavel_nome or '',
                dado.responsavel_cpf or '',
                dado.responsavel_telefone or '',
                dado.responsavel_email or '',
                (
                    dado.responsavel_data_nascimento.strftime('%Y-%m-%d')
                    if dado.responsavel_data_nascimento
                    else '',
                ),
                dado.responsavel_funcao_familiar or '',
                dado.responsavel_escolaridade or '',
                dado.responsavel_ocupacao or '',
                (
                    str(dado.numero_total_membros)
                    if dado.numero_total_membros is not None
                    else '0',
                ),
                (
                    str(dado.renda_familiar_total_estimada)
                    if dado.renda_familiar_total_estimada is not None
                    else '0.00',
                ),
                dado.comprovante_residencia_url or '',
                (
                    str(dado.cadastrada_por_usuario_id)
                    if dado.cadastrada_por_usuario_id
                    else ''
                ),
            ])

        return output.getvalue()
