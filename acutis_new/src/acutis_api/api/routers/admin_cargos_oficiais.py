from http import HTTPStatus

from flask import Blueprint
from flask import request as flask_request
from flask_jwt_extended import jwt_required
from spectree import Response

from acutis_api.application.use_cases.cargos_oficiais import (
    AtualizarCargoOficialUseCase,
    ExcluirCargoOficialUseCase,
    ListaDeCargosOficiaisUseCase,
    ListarTodosCargosOficiaisUseCase,
    ObterTotalCadastrosCargoOficialUseCase,
    RegistraNovoCargoOficialUseCase,
)
from acutis_api.communication.requests.cargos_oficiais import (
    ListarCargosOficiaisQuery,
    ListarCargosOficiaisResponse,
    RegistrarCargosOficiaisRequest,
)
from acutis_api.communication.responses.cargos_oficiais import (
    ListaDeCargosOficiaisResponse,
    ObterTotalCadastrosCargoOficialResponse,
    RegistrarNovoCargoficialResponse,
)
from acutis_api.communication.responses.padrao import (
    ErroPadraoResponse,
    ResponsePadraoSchema,
)
from acutis_api.exception.errors_handler import errors_handler
from acutis_api.infrastructure.extensions import database, swagger
from acutis_api.infrastructure.repositories.cargos_oficiais import (
    CargosOficiaisRepository,
)

admin_cargos_oficiais_bp = Blueprint(
    'admin_cargos_oficiais_bp', __name__, url_prefix='/admin/cargos-oficiais'
)


@admin_cargos_oficiais_bp.post('/registrar')
@swagger.validate(
    json=RegistrarCargosOficiaisRequest,
    resp=Response(
        HTTP_200=RegistrarNovoCargoficialResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Cargos Oficiais'],
)
@jwt_required()
def registrar_novo_cargo_oficial():
    """
    Cria novo cargo oficial
    """
    try:
        repository = CargosOficiaisRepository(database)
        request = RegistrarCargosOficiaisRequest.model_validate(
            flask_request.get_json()
        )
        usecase = RegistraNovoCargoOficialUseCase(repository)
        response = usecase.execute(request)
        return response, HTTPStatus.CREATED
    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@admin_cargos_oficiais_bp.get('/listar-todos-cargos')
@swagger.validate(
    query=ListarCargosOficiaisQuery,
    resp=Response(
        HTTP_200=ListarCargosOficiaisResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Cargos Oficiais'],
)
@jwt_required()
def listar_todos_cargos_oficiais():
    """
    Lista todos os cargos oficiais
    """
    try:
        repository = CargosOficiaisRepository(database)
        request = ListarCargosOficiaisQuery.model_validate(
            flask_request.args.to_dict()
        )
        usecase = ListarTodosCargosOficiaisUseCase(repository)
        response = usecase.execute(request)
        return response, HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)


@admin_cargos_oficiais_bp.put('/atualizar/<uuid:id>')
@swagger.validate(
    json=RegistrarCargosOficiaisRequest,
    resp=Response(
        HTTP_200=RegistrarNovoCargoficialResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Cargos Oficiais'],
)
@jwt_required()
def atualizar_cargo_oficial(id):
    """
    Atualiza um cargo oficial
    """
    try:
        repository = CargosOficiaisRepository(database)
        request = RegistrarCargosOficiaisRequest.model_validate(
            flask_request.get_json()
        )
        usecase = AtualizarCargoOficialUseCase(repository)
        response = usecase.execute(request, id)
        return response, HTTPStatus.OK
    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@admin_cargos_oficiais_bp.delete('/excluir/<uuid:fk_cargo_id>')
@swagger.validate(
    resp=Response(
        HTTP_200=ResponsePadraoSchema,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Cargos Oficiais'],
)
@jwt_required()
def excluir_cargo_oficial(fk_cargo_id):
    try:
        repository = CargosOficiaisRepository(database)
        usecase = ExcluirCargoOficialUseCase(repository)
        response = usecase.execute(fk_cargo_id)
        return response, HTTPStatus.OK
    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@admin_cargos_oficiais_bp.get('/lista-de-cargos-oficiais')
@swagger.validate(
    resp=Response(
        HTTP_200=ListaDeCargosOficiaisResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Cargos Oficiais'],
)
@jwt_required()
def lista_cargos_oficiais():
    try:
        repository = CargosOficiaisRepository(database)
        usecase = ListaDeCargosOficiaisUseCase(repository)
        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)


@admin_cargos_oficiais_bp.get('/cadastros-por-cargo')
@swagger.validate(
    resp=Response(
        HTTP_200=ObterTotalCadastrosCargoOficialResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Cargos Oficiais'],
)
@jwt_required()
def obter_total_cadastros_cargo_oficial():
    """
    Retorna a quantidade de cadastros de cada cargo oficial registrado
    """
    try:
        repository = CargosOficiaisRepository(database)
        usecase = ObterTotalCadastrosCargoOficialUseCase(repository)
        response = usecase.execute()
        return response, HTTPStatus.OK
    except Exception as exc:
        return errors_handler(exc)
