from http import HTTPStatus

from flask import Blueprint
from flask import request as flask_request
from flask_jwt_extended import jwt_required
from spectree import Response

from acutis_api.application.use_cases.admin.graficos_cadastros import (
    CadastrosPorIdadeUseCase,
    CadastrosPorMesUseCase,
    LeadsMediaMensalUseCase,
    LeadsPorCampanhaMesAtualUseCase,
    LeadsPorDiaSemanaUseCase,
    LeadsPorEvolucaoMensalUseCase,
    LeadsPorOrigemUseCase,
    MembrosMediaDiariaUseCase,
    MembrosMediaMensalUseCase,
    MembrosPorDiaMesAtualUseCase,
    MembrosPorEstadoUseCase,
    MembrosPorHoraDiaAtualUseCase,
    MembrosPorPaisUseCase,
    QuantidadeCadastrosDiaAtualUseCase,
    QuantidadeCadastrosUseCase,
    QuantidadeLeadsPorHoraUseCase,
    QuantidadeLeadsUseCase,
    QuantidadeMembrosPorGeneroUseCase,
    ResumoQuantidadeRegistrosUseCase,
)
from acutis_api.communication.requests.admin_graficos_cadastros import (
    ResumoQuantidadeRegistrosRequest,
)
from acutis_api.communication.responses.admin_graficos_cadastros import (
    CadastrosPorIdadeResponse,
    CadastrosPorMesResponse,
    LeadsMediaMensalResponse,
    LeadsPorCampanhaMesAtualResponse,
    LeadsPorDiaSemanaResponse,
    LeadsPorEvolucaoMensalResponse,
    MembrosMediaDiariaResponse,
    MembrosMediaMensalResponse,
    MembrosPorGeneroResponse,
    MembrosPorHoraDiaAtualResponse,
    MembrosPorLocalidadeResponse,
    QuantidadeCadastrosDiaAtualResponse,
    QuantidadeCadastrosMesAtualResponse,
    QuantidadeLeadsMesAtualResponse,
    QuantidadeLeadsPorHoraResponse,
    QuantidadeLeadsPorOrigemResponse,
    QuantidadeMembrosPorDiaMesAtualResponse,
    ResumoQuantidadeRegistrosResponse,
)
from acutis_api.communication.responses.padrao import ErroPadraoResponse
from acutis_api.exception.errors_handler import errors_handler
from acutis_api.infrastructure.extensions import database, swagger
from acutis_api.infrastructure.repositories import GraficosCadastrosRepository

admin_graficos_cadastros_bp = Blueprint(
    'admin_graficos_cadastros',
    __name__,
    url_prefix='/admin/graficos-cadastros',
)


@admin_graficos_cadastros_bp.get('/quantidade-leads-mes-atual')
@swagger.validate(
    resp=Response(
        HTTP_200=QuantidadeLeadsMesAtualResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Dashboard Cadastros'],
)
@jwt_required()
def quantidade_leads_mes_atual():
    """Retorna o número total de cadastros realizados no mês atual"""
    try:
        repository = GraficosCadastrosRepository(database)
        usecase = QuantidadeLeadsUseCase(repository)
        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)


@admin_graficos_cadastros_bp.get('/leads-media-mensal')
@swagger.validate(
    resp=Response(
        HTTP_200=LeadsMediaMensalResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Dashboard Cadastros'],
)
@jwt_required()
def leads_media_mensal():
    """Retorna a média mensal de leads"""
    try:
        repository = GraficosCadastrosRepository(database)
        usecase = LeadsMediaMensalUseCase(repository)
        response = usecase.execute()
        return {'leads_media_mensal': response}, HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)


@admin_graficos_cadastros_bp.get('/quantidade-cadastros-mes-atual')
@swagger.validate(
    resp=Response(
        HTTP_200=QuantidadeCadastrosMesAtualResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Dashboard Cadastros'],
)
@jwt_required()
def quantidade_membros_mes_atual():
    """Retorna o número total de membros cadastrados no mês atual"""
    try:
        repository = GraficosCadastrosRepository(database)
        usecase = QuantidadeCadastrosUseCase(repository)
        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)


@admin_graficos_cadastros_bp.get('/membros-media-mensal')
@swagger.validate(
    resp=Response(
        HTTP_200=MembrosMediaMensalResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Dashboard Cadastros'],
)
@jwt_required()
def membros_media_mensal():
    """Retorna a média mensal de membros cadastrados"""
    try:
        repository = GraficosCadastrosRepository(database)
        usecase = MembrosMediaMensalUseCase(repository)
        response = usecase.execute()
        return {'membros_media_mensal': response}, HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)


@admin_graficos_cadastros_bp.get('/quantidade-cadastros-dia-atual')
@swagger.validate(
    resp=Response(
        HTTP_200=QuantidadeCadastrosDiaAtualResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Dashboard Cadastros'],
)
@jwt_required()
def quantidade_membros_dia_atual():
    """Retorna o número total de membros no dia atual"""
    try:
        repository = GraficosCadastrosRepository(database)
        usecase = QuantidadeCadastrosDiaAtualUseCase(repository)
        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)


@admin_graficos_cadastros_bp.get('/membros-media-diaria')
@swagger.validate(
    resp=Response(
        HTTP_200=MembrosMediaDiariaResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Dashboard Cadastros'],
)
@jwt_required()
def membros_media_diaria():
    """Retorna a média diária de membros cadastrados"""
    try:
        repository = GraficosCadastrosRepository(database)
        usecase = MembrosMediaDiariaUseCase(repository)
        response = usecase.execute()
        return {'membros_media_diaria': response}, HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)


@admin_graficos_cadastros_bp.get('/resumo-quantidade-registros')
@swagger.validate(
    query=ResumoQuantidadeRegistrosRequest,
    resp=Response(
        HTTP_200=ResumoQuantidadeRegistrosResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Dashboard Cadastros'],
)
@jwt_required()
def resumo_quantidade_registros():
    """Retorna o resumo da quantidade de registros"""
    try:
        request = ResumoQuantidadeRegistrosRequest.model_validate(
            flask_request.args.to_dict()
        )
        repository = GraficosCadastrosRepository(database)
        usecase = ResumoQuantidadeRegistrosUseCase(repository)
        response = usecase.execute(request)
        return response, HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)


@admin_graficos_cadastros_bp.get('/membros-por-genero')
@swagger.validate(
    resp=Response(
        HTTP_200=MembrosPorGeneroResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Dashboard Cadastros'],
)
@jwt_required()
def membros_por_genero():
    """Retorna quantidade de registros por gênero"""
    try:
        repository = GraficosCadastrosRepository(database)
        usecase = QuantidadeMembrosPorGeneroUseCase(repository)
        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)


@admin_graficos_cadastros_bp.get('/quantidade-leads-por-hora')
@swagger.validate(
    resp=Response(
        HTTP_200=QuantidadeLeadsPorHoraResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Dashboard Cadastros'],
)
@jwt_required()
def quantidade_leads_por_hora():
    """Retorna o número total de leads por hora"""
    try:
        repository = GraficosCadastrosRepository(database)
        usecase = QuantidadeLeadsPorHoraUseCase(repository)
        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)


@admin_graficos_cadastros_bp.get('/membros-por-hora-dia-atual')
@swagger.validate(
    resp=Response(
        HTTP_200=MembrosPorHoraDiaAtualResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Dashboard Cadastros'],
)
@jwt_required()
def membros_por_hora_dia_atual():
    """Retorna quantidade de membros por hora do dia atual"""
    try:
        repository = GraficosCadastrosRepository(database)
        usecase = MembrosPorHoraDiaAtualUseCase(repository)
        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)


@admin_graficos_cadastros_bp.get('/membros-por-dia-mes-atual')
@swagger.validate(
    resp=Response(
        HTTP_200=QuantidadeMembrosPorDiaMesAtualResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Dashboard Cadastros'],
)
@jwt_required()
def quantidade_membros_por_dia_mes_atual():
    """Retorna o número total de leads por hora"""
    try:
        repository = GraficosCadastrosRepository(database)
        usecase = MembrosPorDiaMesAtualUseCase(repository)
        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)


@admin_graficos_cadastros_bp.get('/leads-por-origem')
@swagger.validate(
    resp=Response(
        HTTP_200=QuantidadeLeadsPorOrigemResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Dashboard Cadastros'],
)
@jwt_required()
def leads_por_origem():
    """Retorna o número total de leads por origem do cadastro"""
    try:
        repository = GraficosCadastrosRepository(database)
        usecase = LeadsPorOrigemUseCase(repository)
        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)


@admin_graficos_cadastros_bp.get('/leads-por-dia-da-semana')
@swagger.validate(
    resp=Response(
        HTTP_200=LeadsPorDiaSemanaResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Dashboard Cadastros'],
)
@jwt_required()
def leads_por_dia_semana():
    """Retorna o número total de leads por dia da semana"""
    try:
        repository = GraficosCadastrosRepository(database)
        usecase = LeadsPorDiaSemanaUseCase(repository)
        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)


@admin_graficos_cadastros_bp.get('/leads-por-campanha-mes-atual')
@swagger.validate(
    resp=Response(
        HTTP_200=LeadsPorCampanhaMesAtualResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Dashboard Cadastros'],
)
@jwt_required()
def leads_por_origem_mes_atual():
    """Retorna o número total de leads por campanha mês atual"""
    try:
        repository = GraficosCadastrosRepository(database)
        usecase = LeadsPorCampanhaMesAtualUseCase(repository)
        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)


@admin_graficos_cadastros_bp.get('/cadastros-por-mes')
@swagger.validate(
    resp=Response(
        HTTP_200=CadastrosPorMesResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Dashboard Cadastros'],
)
@jwt_required()
def cadastros_por_mes():
    """Retorna o número total de cadastros a cada mês"""
    try:
        repository = GraficosCadastrosRepository(database)
        usecase = CadastrosPorMesUseCase(repository)
        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)


@admin_graficos_cadastros_bp.get('/cadastros-por-idade')
@swagger.validate(
    resp=Response(
        HTTP_200=CadastrosPorIdadeResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Dashboard Cadastros'],
)
@jwt_required()
def cadastros_por_idade():
    """Retorna quantidade de cadastro por idade e gênero"""
    try:
        repository = GraficosCadastrosRepository(database)
        usecase = CadastrosPorIdadeUseCase(repository)
        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)


@admin_graficos_cadastros_bp.get('/leads-por-evolucao-mensal')
@swagger.validate(
    resp=Response(
        HTTP_200=LeadsPorEvolucaoMensalResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Dashboard Cadastros'],
)
@jwt_required()
def leads_por_evolucao_mensal():
    """Retorna quantidade de leads por evolução mensal"""
    try:
        repository = GraficosCadastrosRepository(database)
        usecase = LeadsPorEvolucaoMensalUseCase(repository)
        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)


@admin_graficos_cadastros_bp.get('/membros-por-estado')
@swagger.validate(
    resp=Response(
        HTTP_200=MembrosPorLocalidadeResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Dashboard Cadastros'],
)
@jwt_required()
def membros_por_estado():
    """Retorna quantidade de leads por estado"""
    try:
        repository = GraficosCadastrosRepository(database)
        usecase = MembrosPorEstadoUseCase(repository)
        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)


@admin_graficos_cadastros_bp.get('/membros-por-pais')
@swagger.validate(
    resp=Response(
        HTTP_200=MembrosPorLocalidadeResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Dashboard Cadastros'],
)
@jwt_required()
def membros_por_pais():
    """Retorna quantidade de leads por estado"""
    try:
        repository = GraficosCadastrosRepository(database)
        usecase = MembrosPorPaisUseCase(repository)
        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)
