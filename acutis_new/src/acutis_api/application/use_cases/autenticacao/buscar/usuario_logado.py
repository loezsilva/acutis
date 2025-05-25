from flask_jwt_extended import current_user

from acutis_api.communication.responses.autenticacao import (
    UsuarioLogadoResponse,
)

PADRAO_DATETIME = '%d/%m/%Y %H:%M:%S'


class UsuarioLogadoUseCase:
    @staticmethod
    def execute() -> UsuarioLogadoResponse:
        lead = current_user

        dados_usuario = UsuarioLogadoResponse(
            lead_id=lead.id,
            membro_id=lead.membro.id if lead.membro else None,
            nome=lead.nome,
            nome_social=lead.membro.nome_social if lead.membro else None,
            email=lead.email,
            telefone=lead.telefone,
            pais=lead.pais,
            numero_documento=(
                lead.membro.numero_documento if lead.membro else None
            ),
            data_nascimento=(
                lead.membro.data_nascimento.strftime('%d/%m/%Y')
                if lead.membro
                else None
            ),
            sexo=lead.membro.sexo if lead.membro else None,
            foto=lead.membro.foto if lead.membro else None,
            criado_em=(
                lead.membro.criado_em.strftime(PADRAO_DATETIME)
                if lead.membro
                else None
            ),
            atualizado_em=(
                lead.membro.atualizado_em.strftime(PADRAO_DATETIME)
                if lead.membro and lead.membro.atualizado_em
                else None
            ),
            cadastro_atualizado_em=(
                lead.membro.cadastro_atualizado_em.strftime(PADRAO_DATETIME)
                if lead.membro and lead.membro.cadastro_atualizado_em
                else None
            ),
            ultimo_acesso=(
                lead.ultimo_acesso.strftime(PADRAO_DATETIME)
                if lead.ultimo_acesso
                else None
            ),
            origem_cadastro=lead.origem_cadastro,
        ).model_dump()

        return UsuarioLogadoResponse.model_validate(dados_usuario)
