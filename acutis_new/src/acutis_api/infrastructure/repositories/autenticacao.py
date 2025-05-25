from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.repositories.autenticacao import (
    AutenticacaoRepositoryInterface,
)


class AutenticacaoRepository(AutenticacaoRepositoryInterface):
    def __init__(self, database: SQLAlchemy):
        self._database = database

    def salvar_alteracoes(self):
        try:
            self._database.session.commit()
        except Exception as exc:
            self._database.session.rollback()
            raise exc

    def buscar_lead_por_email(self, email: str) -> Lead | None:
        lead = self._database.session.scalar(
            select(Lead).where(Lead.email == email)
        )

        return lead

    def atualizar_data_ultimo_acesso(self, lead: Lead):
        lead.ultimo_acesso = datetime.now()
        self._database.session.add(lead)

    @staticmethod
    def alterar_senha(usuario: Lead, nova_senha: str):
        usuario.senha = nova_senha
