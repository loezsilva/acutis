from enum import Enum


class SexoEnum(str, Enum):
    masculino = 'masculino'
    feminino = 'feminino'


class TipoCadastroEnum(str, Enum):
    lead = 'lead'
    membro = 'membro'


class OrigemCadastroEnum(str, Enum):
    acutis = 'acutis'
    app = 'app'
    google = 'google'


class PerfilEnum(str, Enum):
    administrador: str = 'Administrador'
    benfeitor: str = 'Benfeitor'
    operacional: str = 'Operacional'
    campanhas_e_lp: str = 'Campanhas e LP'
    marketing: str = 'Marketing'
    dev: str = 'Dev'
    administrador_agape: str = 'Administrador Agape'
    voluntario_agape: str = 'Voluntario Agape'
    gestor_doacoes: str = 'Gestor Doacoes'
    vocacional_masculino: str = 'Vocacional Masculino'
    vocacional_feminino: str = 'Vocacional Feminino'
