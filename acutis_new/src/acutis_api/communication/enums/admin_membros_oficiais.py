from enum import Enum


class ListarMembrosOficiaisOrdenarPorEnum(str, Enum):
    lead_nome = 'lead_nome'
    lead_email = 'lead_email'
    membro_documento = 'membro_numero_documento'
    membro_sexo = 'membro_sexo'
    oficial_status = 'oficial_status'
    cargo_oficial = 'nome_cargo_oficial'
    superior_nome = 'superior_nome'
    criado_em = 'oficial_criado_em'
