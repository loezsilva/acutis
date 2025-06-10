import uuid

from acutis_api.application.utils.funcoes_auxiliares import (
    tratar_valor_campo_por_tipo_valor,
)
from acutis_api.communication.responses.admin_membros import (
    BuscarDetalhesDoLeadResponse,
    CampanhasRegistradasSchema,
    EnderecoSchema,
    LeadSchema,
    MembroSchema,
)
from acutis_api.domain.repositories.admin_membros import (
    AdminMembrosRepositoryInterface,
)
from acutis_api.domain.services.file_service import FileServiceInterface


class BuscarUsuarioPorIDUseCase:
    def __init__(
        self,
        repository: AdminMembrosRepositoryInterface,
        file_service: FileServiceInterface,
    ):
        self._repository = repository
        self._file_service = file_service

    def execute(self, uuid: uuid.UUID):
        dados_membro = None
        dados_endereco = None
        campanhas_registradas = []

        lead = self._repository.buscar_lead_por_id(uuid)

        dados_lead = LeadSchema(
            id=lead.id,
            nome=lead.nome,
            email=lead.email,
            telefone=lead.telefone,
            pais=lead.pais,
            status=lead.status,
            data_cadastro=lead.criado_em,
            ultimo_acesso=lead.ultimo_acesso,
        ).model_dump()

        if lead.membro:
            dados_membro = MembroSchema(
                id=lead.membro.id,
                foto=self._file_service.buscar_url_arquivo(lead.membro.foto)
                if lead.membro.foto
                else None,
                numero_documento=lead.membro.numero_documento,
                nome_social=lead.membro.nome_social,
            ).model_dump()

            dados_endereco = EnderecoSchema(
                id=lead.membro.endereco.id,
                cep=lead.membro.endereco.codigo_postal,
                tipo_logradouro=lead.membro.endereco.tipo_logradouro,
                logradouro=lead.membro.endereco.logradouro,
                numero=lead.membro.endereco.numero,
                complemento=lead.membro.endereco.complemento,
                bairro=lead.membro.endereco.bairro,
                cidade=lead.membro.endereco.cidade,
                estado=lead.membro.endereco.estado,
                pais=lead.membro.endereco.pais,
            ).model_dump()

        if lead.metadados:
            for metadado in lead.metadados:
                nome_campanha = metadado.campo_adicional.campanha.nome
                nome_campo = metadado.campo_adicional.nome_campo
                tipo_campo = metadado.campo_adicional.tipo_campo
                valor_campo = tratar_valor_campo_por_tipo_valor(
                    metadado.valor_campo, tipo_campo
                )

                campanha_existente = next(
                    (
                        campanha
                        for campanha in campanhas_registradas
                        if campanha['nome'] == nome_campanha
                    ),
                    None,
                )

                if campanha_existente:
                    campanha_existente['campos_adicionais'].append({
                        'nome_campo': nome_campo,
                        'valor_campo': valor_campo,
                    })
                else:
                    nova_campanha = {
                        'nome': nome_campanha,
                        'campos_adicionais': [
                            {
                                'nome_campo': nome_campo,
                                'valor_campo': valor_campo,
                            }
                        ],
                    }
                    campanhas_registradas.append(nova_campanha)

            campanhas_registradas = [
                CampanhasRegistradasSchema.model_validate(
                    campanha
                ).model_dump()
                for campanha in campanhas_registradas
            ]

        response = BuscarDetalhesDoLeadResponse(
            dados_lead=dados_lead,
            dados_membro=dados_membro,
            dados_endereco=dados_endereco,
            campanhas_registradas=campanhas_registradas,
        ).model_dump()

        return response
