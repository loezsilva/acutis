from dataclasses import dataclass
from datetime import date, datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, constr, validator
from werkzeug.security import check_password_hash, generate_password_hash

from builder import db
from models.endereco import Endereco
from models.perfil import Perfil
from models.permissao_usuario import PermissaoUsuario
from models.clifor import Clifor
from models.perfil import PermissionsMenuProfileSchema
from utils.functions import get_current_time


@dataclass
class Usuario(db.Model):
    __tablename__ = "usuario"

    id: int = db.Column(db.Integer, primary_key=True)
    nome: str = db.Column(db.String(100), nullable=False)
    nome_social: str = db.Column(db.String(45))
    status: bool = db.Column(db.Boolean, default=False)
    data_inicio: datetime = db.Column(db.DateTime)
    data_expiracao: datetime = db.Column(db.DateTime)
    password_hash: str = db.Column(db.String)
    obriga_atualizar_cadastro: bool = db.Column(db.Boolean, default=False)
    data_expiracao_senha: datetime = db.Column(db.DateTime)
    data_ultimo_acesso: datetime = db.Column(db.DateTime)
    email: str = db.Column(
        db.String(100), nullable=False, unique=True, index=True
    )
    bloqueado: bool = db.Column(db.Boolean, default=False)
    avatar: str = db.Column(db.String)
    campanha_origem: Optional[int] = db.Column(
        db.Integer, db.ForeignKey("campanha.id"), index=True
    )
    data_criacao: datetime = db.Column(db.DateTime, default=get_current_time)
    usuario_criacao: int = db.Column(db.Integer, nullable=False, default=0)
    data_alteracao: datetime = db.Column(db.DateTime)
    usuario_alteracao: int = db.Column(db.Integer)
    qr_code_hash: str = db.Column(db.UnicodeText(100))
    country: str = db.Column(db.UnicodeText(255), default="brasil")
    deleted_at: datetime = db.Column(db.DateTime, index=True)
    origem_cadastro: str = db.Column(db.String)

    permissao = db.relationship(
        "PermissaoUsuario",
        backref="user",
        lazy="dynamic",
        cascade="all, delete",
    )

    clifor = db.relationship(
        "Clifor", backref="user", lazy="dynamic", cascade="all, delete"
    )

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "nome_social": self.nome_social,
            "status": self.status,
            "data_inicio": self.data_inicio,
            "data_expiracao": self.data_expiracao,
            "password_hash": self.password_hash,
            "data_expiracao_senha": self.data_expiracao_senha,
            "data_ultimo_acesso": self.data_ultimo_acesso,
            "email": self.email,
            "bloqueado": self.bloqueado,
            "avatar": self.avatar,
            "data_criacao": self.data_criacao,
            "usuario_criacao": self.usuario_criacao,
            "data_alteracao": self.data_alteracao,
            "usuario_alteracao": self.usuario_alteracao,
            "deleted_at": self.deleted_at,
            "origem_cadastro": self.origem_cadastro,
        }

    def __repr__(self) -> str:
        return f"<Usuario {self.nome}>"

    def soft_delete(self):
        self.deleted_at = get_current_time()
        db.session.commit()

    @classmethod
    def get_informations_current_user(cls, fk_usuario_id: int):
        result_query = (
            db.session.query(
                cls.id,
                cls.nome,
                cls.nome_social,
                cls.avatar,
                cls.email,
                cls.country,
                cls.campanha_origem,
                cls.obriga_atualizar_cadastro,
                Clifor.cpf_cnpj,
                Clifor.data_nascimento,
                Clifor.telefone1,
                Clifor.sexo,
                Perfil.id.label("fk_perfil_id"),
                Clifor.id.label("fk_clifor_id"),
                Endereco.obriga_atualizar_endereco,
                Perfil.super_perfil,
                Perfil.nome.label("nome_perfil"),
            )
            .select_from(Usuario)
            .join(Clifor, Usuario.id == Clifor.fk_usuario_id)
            .join(Endereco, Clifor.id == Endereco.fk_clifor_id)
            .join(
                PermissaoUsuario, Usuario.id == PermissaoUsuario.fk_usuario_id
            )
            .join(Perfil, Perfil.id == PermissaoUsuario.fk_perfil_id)
            .filter(cls.id == fk_usuario_id)
        )

        result = result_query.first()

        return result


class UserUpdateSchema(BaseModel):
    nome: str
    #     nome_social: str
    avatar: str = None
    data_nascimento: date
    telefone: str
    sexo: str


class UserAdminUpdateSchema(BaseModel):
    name: str
    #     nome_social: str
    email: str
    cpf_cnpj: str
    phone: str = None
    profile_id: int = None
    company_id: int = None
    cargo_id: int = None
    usuario_superior_id: int = None


class UserGetOneResponseSchema(BaseModel):
    id: int
    nome: str
    nome_social: str = None
    status: bool
    data_inicio: date
    data_expiracao: date = None
    obriga_atualizar_cadastro: Optional[bool]
    data_expiracao_senha: date = None
    data_ultimo_acesso: date = None
    telefone: str = None
    email: str
    bloqueado: bool
    avatar: str = None
    fk_empresa_id: int
    cpf_cnpj: str = None
    fk_perfil_id: int = None
    nome_perfil: str = None
    country: Optional[str]
    fk_clifor_id: int
    deleted_at: Optional[str]
    origem_cadastro: Optional[str]

    class Config:
        orm_mode = True


class UserResponseSchema(BaseModel):
    id: int
    nome: str
    nome_social: str = None
    status: bool
    data_inicio: datetime
    data_expiracao: datetime = None
    obriga_atualizar_endereco: Optional[bool]
    data_expiracao_senha: datetime = None
    data_ultimo_acesso: datetime = None
    email: str
    bloqueado: bool
    avatar: str = None
    data_criacao: datetime
    usuario_criacao: int = None
    data_alteracao: datetime = None
    usuario_alteracao: int = None
    country: Optional[str]

    class Config:
        orm_mode = True


class UserResponseListSchema(BaseModel):
    __root__: List[UserResponseSchema]


class UserResetPasswordSchema(BaseModel):
    new_password: constr(min_length=8, max_length=16)  # type: ignore


class UserChangePasswordSchema(UserResetPasswordSchema):
    old_password: str


class UserReceiveTokenSchema(BaseModel):
    token: str


class UserReceiveEmailSchema(BaseModel):
    email: str


class LoggedUserResponseSchema(BaseModel):
    id: int
    nome: str
    nome_social: str = None
    email: str
    cpf_cnpj: str = None
    data_nascimento: str = None
    telefone: str = None
    sexo: str = None
    avatar: str = None
    fk_sistema_id: int
    fk_perfil_id: int
    fk_clifor_id: int = None
    atualizar_endereco: bool
    obriga_atualizar_cadastro: bool
    cargo_id: int = None
    campanha_origem: Optional[int]
    permissoes: Dict[str, PermissionsMenuProfileSchema]


class DashBoardCountUsers(BaseModel):
    count_users: int


class DashBoardActiveUsers(BaseModel):
    percent_active_users: float
    percent_female_users: float
    percent_male_users: float
    percent_null_sex_users: float
    user_inactive: float
    users_active: float


class UsuarioPorFaixaEtaria(BaseModel):
    age_range: str
    female_count: int
    male_count: int
    total_count: int


class DashBoardUsersByAge(BaseModel):
    user_by_age: List[UsuarioPorFaixaEtaria]


class DayOfWeekProgress(BaseModel):
    day: str = Field(...)
    count: int = Field(...)


class DashBoardProgressByHours(BaseModel):
    users_per_hour: Dict[str, int]


class UserByRegion(BaseModel):
    count: int
    percentage: float


class UsersByRegionResponse(BaseModel):
    user_per_region: Dict[str, UserByRegion]


class CampaignDetails(BaseModel):
    campanha: str
    total_cadastros: int


class UserByRegion(BaseModel):
    Campanha_destaque: Optional[CampaignDetails]
    count: int
    percentage: float


class UsersAndCampaignsByRegionResponseSchema(BaseModel):
    users_and_campaigns_by_region: Dict[str, UserByRegion]


class UsuarioPorCampanha(BaseModel):
    campanha: Optional[str]
    quantidade_usuarios: int
    percentual: float


class DashBoardUsersByCampaign(BaseModel):
    usuarios_por_campanha: List[UsuarioPorCampanha]


class DashBoardAmountDonations(BaseModel):
    amount_donations: float


class FaixaEtaria(BaseModel):
    age_range: str
    female_count: int
    male_count: int
    total_count: int
    desconhecido: int


class DashBoardUsersByAge(BaseModel):
    user_by_age: List[FaixaEtaria]


class CadastroPorMes(BaseModel):
    month: int
    total_users: int
    year: int


class DashBordProgressUsersByMonth(BaseModel):
    cadastros_por_mes: List[CadastroPorMes]


class DashBoardCampaigns(BaseModel):
    campaigns: List[str]


class DashBoardProgressByDayOfWeek(BaseModel):
    day_of_weeks: List[Dict[str, int]]


class CadastrosPorMesSchema(BaseModel):
    cadastros_by_months: List[Dict[str, int]]

    @validator("cadastros_by_months")
    def validate_cadastros_by_months(cls, value):
        for item in value:
            if len(item) != 1:
                raise ValueError(
                    "Cada item na lista deve conter apenas uma chave representando o mês."
                )

        for item in value:
            month_year = list(item.keys())[0]
            try:
                datetime.strptime(month_year, "%m/%Y")
            except ValueError:
                raise ValueError(
                    f"Formato inválido para o mês: {month_year}. Use o formato 'MM/AAAA'."
                )

        return value


class DashBoardUsersNotCampaign(BaseModel):
    total_usuarios_nulos = int


class DashBoardUsersByState(BaseModel):
    users_by_state: Dict[str, int]

    @validator("users_by_state")
    def validate_users_by_state(cls, value):
        for count in value.values():
            if not isinstance(count, int) or count < 0:
                raise ValueError(
                    "As contagens de usuários devem ser inteiros positivos."
                )

        return value


class Keys(BaseModel):
    campanha1: str
    campanha2: str
    periodo: str
    resultados_por_mes: Dict[str, Dict[str, int]]


class DashBoardUsersByCampaignComparation(BaseModel):
    comparativo_campanha: Keys


class ResponseUserAddresAdmin(BaseModel):
    bairro: Optional[str]
    cep: Optional[str]
    cidade: Optional[str]
    complemento: Optional[str]
    numero: Optional[str]
    pais_origem: Optional[str]
    rua: Optional[str]
    detalhes_estrangeiro: Optional[str]
    estado: Optional[str]


class ResponseSchemaCadasDiario(BaseModel):
    cadastros_hoje: int
    media_diaria: int


class ResponseSchemaCadasMensal(BaseModel):
    cadastros_mes: int
    media_mensal: int
