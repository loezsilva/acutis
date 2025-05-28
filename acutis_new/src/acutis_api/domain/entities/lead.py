import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from pwdlib import PasswordHash
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from acutis_api.domain.database import table_registry

if TYPE_CHECKING:
    from acutis_api.domain.entities import (  # pragma: no cover
        LeadCampanha,
        Membro,
        MetadadoLead,
        PermissaoLead,
    )

pwd_context = PasswordHash.recommended()


class OrigemCadastroEnum(str, Enum):
    acutis = 'acutis'
    app = 'app'
    google = 'google'


@table_registry.mapped_as_dataclass
class Lead:
    __tablename__ = 'leads'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False, primary_key=True, default_factory=uuid.uuid4
    )
    nome: Mapped[str] = mapped_column(String(100), index=True)
    email: Mapped[str] = mapped_column(String(100), index=True, unique=True)
    telefone: Mapped[str]
    pais: Mapped[str] = mapped_column(String(100), index=True)
    password_hashed: Mapped[str] = mapped_column(
        String(500), init=False, index=True, repr=False
    )
    origem_cadastro: Mapped[OrigemCadastroEnum] = mapped_column(
        String(50), index=True
    )
    status: Mapped[bool | None] = mapped_column(default=False, index=True)
    ultimo_acesso: Mapped[datetime | None] = mapped_column(default=None)
    criado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    membro: Mapped['Membro'] = relationship(
        init=False,
        back_populates='lead',
        cascade='all, delete-orphan',  # NOSONAR
        single_parent=True,
    )

    metadados: Mapped[list['MetadadoLead']] = relationship(
        init=False, backref='lead', cascade='all, delete-orphan'
    )

    leads_campanhas: Mapped[list['LeadCampanha']] = relationship(
        init=False, backref='lead', cascade='all, delete-orphan'
    )
    
    permissoes_lead: Mapped[list['PermissaoLead']] = relationship(
        init=False,
        back_populates='lead', 
        cascade='all, delete-orphan'
    )

    @property
    def senha(self):
        raise AttributeError(
            'Senha não é um atributo acessível.'
        )  # pragma: no cover

    @senha.setter
    def senha(self, senha: str):
        self.password_hashed = pwd_context.hash(senha)

    def verificar_senha(self, senha: str) -> bool:
        return pwd_context.verify(senha, self.password_hashed)

    @property
    def nomes_dos_perfis(self):
        print("@@@@@@", self.permissoes_lead)
        return [
            permissao.perfil.nome 
            for permissao in self.permissoes_lead if permissao.perfil
        ]