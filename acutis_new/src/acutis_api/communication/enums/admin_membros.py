from enum import Enum


class ListarLeadsMembrosOrdenarPorEnum(str, Enum):
    lead_id = 'lead_id'
    nome = 'nome'
    email = 'email'
    telefone = 'telefone'
    pais = 'pais'
    data_cadastro_lead = 'data_cadastro_lead'
    lead_atualizado_em = 'lead_atualizado_em'
    membro_id = 'membro_id'
    benfeitor_id = 'benfeitor_id'
    endereco_id = 'endereco_id'
    nome_social = 'nome_social'
    data_nascimento = 'data_nascimento'
    numero_documento = 'numero_documento'
    sexo = 'sexo'
    foto = 'foto'
    ultimo_acesso = 'ultimo_acesso'
    status_conta_lead = 'status_conta_lead'
    data_cadastro_membro = 'data_cadastro_membro'
    membro_atualizado_em = 'membro_atualizado_em'
    cadastro_membro_atualizado_em = 'cadastro_membro_atualizado_em'
