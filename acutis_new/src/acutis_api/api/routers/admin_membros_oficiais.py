from http import HTTPStatus

from flask import Blueprint
from flask import request as flask_request
from flask_jwt_extended import jwt_required
from spectree import Response

from acutis_api.application.use_cases.admin.membros_oficiais import (
    AlterarCargoMembroOficialUseCase,
    AlterarStatusMembroOficialUseCase,
    AlterarVinculoOficialUseCase,
    ExcluirMembroOficialUseCase,
    ListarMembrosOficiaisUseCase,
)
from acutis_api.communication.requests.admin_membros_oficiais import (
    AlterarCargoOficialRequest,
    AlterarStatusMembroOficialRequest,
    AlterarVinculoOficialRequest,
    ListarMembrosOficiaisRequest,
)
from acutis_api.communication.responses.admin_membros_oficiais import (
    ListarMembrosOficiaisResponse,
)
from acutis_api.communication.responses.padrao import (
    ErroPadraoResponse,
    ResponsePadraoSchema,
)
from acutis_api.exception.errors_handler import errors_handler
from acutis_api.infrastructure.extensions import database, swagger
from acutis_api.infrastructure.repositories.membros_oficiais import (
    MembrosOficiaisRepository,
)
from acutis_api.infrastructure.services.factories import file_service_factory
from acutis_api.infrastructure.services.sendgrid import SendGridService

admin_membros_oficiais = Blueprint(
    'admin_membros_oficiais', __name__, url_prefix='/admin/membros-oficiais'
)


@admin_membros_oficiais.get('/listar')
@swagger.validate(
    query=ListarMembrosOficiaisRequest,
    resp=Response(
        HTTP_200=ListarMembrosOficiaisResponse,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Membros Oficiais'],
)
@jwt_required()
def admin_listar_membros_oficiais():
    try:
        file_service = file_service_factory()
        repository = MembrosOficiaisRepository(database)
        request = ListarMembrosOficiaisRequest.model_validate(
            flask_request.args.to_dict()
        )
        usecase = ListarMembrosOficiaisUseCase(repository, file_service)
        response = usecase.execute(request)
        return response, HTTPStatus.OK
    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@admin_membros_oficiais.put('/alterar-status')
@swagger.validate(
    json=AlterarStatusMembroOficialRequest,
    resp=Response(
        HTTP_200=ResponsePadraoSchema,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Membros Oficiais'],
)
@jwt_required()
def admin_alterar_status_membro_oficial():
    try:
        repository = MembrosOficiaisRepository(database)
        request = AlterarStatusMembroOficialRequest.model_validate(
            flask_request.get_json()
        )
        notification = SendGridService()
        usecase = AlterarStatusMembroOficialUseCase(repository, notification)
        response = usecase.execute(request)
        return {'msg': f'Oficial {response} com sucesso'}, HTTPStatus.OK
    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@admin_membros_oficiais.put('/alterar-cargo')
@swagger.validate(
    json=AlterarCargoOficialRequest,
    resp=Response(
        HTTP_200=ResponsePadraoSchema,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Membros Oficiais'],
)
@jwt_required()
def admin_alterar_cargo_membro_oficial():
    try:
        repository = MembrosOficiaisRepository(database)
        request = AlterarCargoOficialRequest.model_validate(
            flask_request.get_json()
        )
        usecase = AlterarCargoMembroOficialUseCase(repository)
        usecase.execute(request)
        return {'msg': 'Cargo do oficial alterado com sucesso.'}, HTTPStatus.OK
    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@admin_membros_oficiais.put('/alterar-vinculo')
@swagger.validate(
    json=AlterarVinculoOficialRequest,
    resp=Response(
        HTTP_200=ResponsePadraoSchema,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Membros Oficiais'],
)
@jwt_required()
def admin_alterar_vinculo_membro_oficial():
    try:
        repository = MembrosOficiaisRepository(database)
        request = AlterarVinculoOficialRequest.model_validate(
            flask_request.get_json()
        )
        usecase = AlterarVinculoOficialUseCase(repository)
        usecase.execute(request)
        return {'msg': 'Vinculo alterado com sucesso.'}, HTTPStatus.OK
    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@admin_membros_oficiais.delete('/excluir/<uuid:fk_membro_oficial_id>')
@swagger.validate(
    resp=Response(
        HTTP_200=ResponsePadraoSchema,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Admin - Membros Oficiais'],
)
@jwt_required()
def admin_excluir_oficial(fk_membro_oficial_id):
    try:
        repository = MembrosOficiaisRepository(database)
        usecase = ExcluirMembroOficialUseCase(repository)
        usecase.execute(fk_membro_oficial_id)
        return {'msg': 'Membro Oficial deletado com sucesso'}, HTTPStatus.OK
    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)
