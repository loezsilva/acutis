from flask import Blueprint
from flask_jwt_extended import current_user, jwt_required
from spectree import Response

from exceptions.error_types.http_forbidden import ForbiddenError
from exceptions.errors_handler import errors_handler
from builder import api, db as database
from handlers.agape.delete.delete_agape_action_instance import (
    DeleteAgapeActionInstance,
)
from handlers.agape.delete.remove_user_from_agape_voluntary import (
    RemoveUserFromAgapeVoluntary,
)
from handlers.agape.get.export_agape_donations import ExportAgapeDonations
from handlers.agape.get.export_agape_families import ExportAgapeFamilies
from handlers.agape.get.get_agape_action_by_id import GetAgapeActionById
from handlers.agape.get.get_agape_action_instance_by_id import (
    GetAgapeActionInstanceById,
)
from handlers.agape.get.get_agape_family_by_cpf import GetAgapeFamilyByCpf
from handlers.agape.get.get_agape_instance_address import (
    GetAgapeInstanceAddress,
)
from handlers.agape.get.get_agape_instance_items import GetAgapeInstanceItems
from handlers.agape.get.get_agape_items_balance_history import (
    GetAgapeItemsBalanceHistory,
)
from handlers.agape.get.get_agape_volunteers import GetAgapeVolunteers
from handlers.agape.put.update_user_to_agape_voluntary import (
    UpdateUserToAgapeVoluntary,
)
from models.schemas.agape.get.get_agape_volunteers import (
    GetAgapeVolunteersResponse,
)
from handlers.agape.get.get_agape_volunteers_permissions_status import (
    GetAgapeVolunteersPermissionsStatus,
)
from handlers.agape.get.get_all_agape_actions import (
    GetAllAgapeActions,
)
from handlers.agape.get.get_all_agape_actions_instances import (
    GetAllAgapeActionsInstances,
)
from handlers.agape.get.get_all_agape_actions_names import (
    GetAllAgapeActionsNames,
)
from handlers.agape.get.get_instance_beneficiaries_addresses_geolocation import (
    GetInstanceBeneficiariesAddressesGeolocation,
)
from handlers.agape.get.get_all_agape_families_address import (
    GetAllAgapeFamiliesAddress,
)
from handlers.agape.get.get_all_donations_receipts import (
    GetAllDonationsReceipts,
)
from handlers.agape.get.get_all_items_receipts import GetAllItemsReceipts
from handlers.agape.get.get_beneficiaries_by_agape_action_instance_id import (
    GetBeneficiariesByAgapeActionInstanceId,
)
from handlers.agape.get.get_all_stock_items import (
    GetAllStockItems,
)
from handlers.agape.get.get_beneficiary_donated_items import (
    GetBeneficiaryDonatedItems,
)
from handlers.agape.get.get_card_agape_family_income import (
    GetCardAgapeFamilyIncome,
)
from handlers.agape.get.get_card_total_donations_receipts import (
    GetCardTotalDonationsReceipts,
)
from handlers.agape.get.get_cards_agape_families_statistics import (
    GetCardsAgapeFamiliesStatistics,
)
from handlers.agape.get.get_cards_stock_items_statistics import (
    GetCardsStockItemsStatistics,
)
from handlers.agape.post.register_agape_action_name import (
    RegisterAgapeActionName,
)
from handlers.agape.post.register_agape_donation import (
    RegisterAgapeDonation,
)
from handlers.agape.post.register_agape_donation_receipts import (
    RegisterAgapeDonationReceipts,
)
from handlers.agape.post.register_agape_stock_item import (
    RegisterAgapeStockItem,
)
from handlers.agape.post.register_agape_action import (
    RegisterAgapeAction,
)
from handlers.agape.put.finish_agape_action_instance import (
    FinishAgapeActionInstance,
)
from handlers.agape.put.start_agape_action_instance import (
    StartAgapeActionInstance,
)
from handlers.agape.put.supply_agape_stock import (
    SupplyAgapeStock,
)
from handlers.agape.put.update_agape_action import UpdateAgapeAction
from handlers.agape.delete.delete_agape_family import (
    DeleteAgapeFamily,
)
from handlers.agape.delete.delete_agape_member import (
    DeleteAgapeMember,
)
from handlers.agape.get.get_all_agape_families import (
    GetAllAgapeFamilies,
)
from handlers.agape.get.get_all_members_by_family_id import (
    GetAllMembersByFamilyId,
)
from handlers.agape.get.get_agape_member import (
    GetAgapeMember,
)
from handlers.agape.get.get_family_address_by_id import (
    GetFamilyAddressById,
)
from handlers.agape.post.register_agape_family import (
    RegisterAgapeFamily,
)
from handlers.agape.post.register_agape_members import (
    RegisterAgapeMembers,
)
from handlers.agape.put.update_agape_family_address import (
    UpdateAgapeFamilyAddress,
)
from handlers.agape.put.update_agape_member import (
    UpdateAgapeMember,
)
from handlers.agape.put.update_agape_volunteers_permissions import (
    UpdateAgapeVolunteersPermissions,
)
from models.perfil import ProfilesEnum
from models.schemas.agape.get.get_agape_action_by_id import (
    GetAgapeActionByIdResponse,
)
from models.schemas.agape.get.get_agape_action_instance_by_id import (
    GetAgapeActionInstanceByIdResponse,
)
from models.schemas.agape.get.get_agape_family_by_cpf import (
    GetAgapeFamilyByCpfResponse,
)
from models.schemas.agape.get.get_agape_instance_address import (
    GetAgapeInstanceAddressResponse,
)
from models.schemas.agape.get.get_agape_volunteers_permissions_status import (
    GetAgapeVolunteersPermissionsStatusResponse,
)
from models.schemas.agape.get.get_instance_beneficiaries_addresses_geolocation import (
    GetInstanceBeneficiariesAddressesGeolocationResponse,
)
from models.schemas.agape.get.get_all_agape_families_address import (
    GetAllAgapeFamiliesAddressResponse,
)
from models.schemas.agape.get.get_all_donations_receipts import (
    GetAllDonationsReceiptsResponse,
)
from models.schemas.agape.get.get_all_items_receipts import (
    GetAllItemsReceiptsResponse,
)
from models.schemas.agape.get.get_card_agape_family_income import (
    GetCardAgapeFamilyIncomeResponse,
)
from models.schemas.agape.get.get_agape_instance_items import (
    GetAgapeInstanceItemsResponse,
)
from models.schemas.agape.get.get_agape_items_balance_history import (
    GetAgapeItemsBalanceHistoryQuery,
    GetAgapeItemsBalanceHistoryResponse,
)
from models.schemas.agape.get.get_agape_member import GetAgapeMemberResponse
from models.schemas.agape.get.get_all_agape_actions import (
    GetAllAgapeActionsQuery,
    GetAllAgapeActionsResponse,
)
from models.schemas.agape.get.get_all_agape_actions_instances import (
    GetAllAgapeActionsInstancesQuery,
    GetAllAgapeActionsInstancesResponse,
)
from models.schemas.agape.get.get_all_agape_actions_names import (
    GetAllAgapeActionsNamesResponse,
)
from models.schemas.agape.get.get_all_agape_families import (
    GetAllAgapeFamiliesResponse,
)
from models.schemas.agape.get.get_all_members_by_family_id import (
    GetAllMembersByFamilyIdResponse,
)
from models.schemas.agape.get.get_all_stock_items import (
    GetAllStockItemsResponse,
)
from models.schemas.agape.get.get_beneficiaries_by_agape_action_id import (
    GetBeneficiariesByAgapeActionIdQuery,
    GetBeneficiariesByAgapeActionIdResponse,
)
from models.schemas.agape.get.get_beneficiary_donated_items import (
    GetBeneficiaryDonatedItemsResponse,
)
from models.schemas.agape.get.get_card_total_donations_receipts import (
    GetCardTotalDonationsReceiptsResponse,
)
from models.schemas.agape.get.get_cards_agape_families_statistics import (
    GetCardsAgapeFamiliesStatisticsResponse,
)
from models.schemas.agape.get.get_cards_stock_items_statistics import (
    GetCardsStockItemsStatisticsResponse,
)
from models.schemas.agape.get.get_family_address_by_id import (
    GetFamilyAddressByIdResponse,
)
from models.schemas.agape.post.register_agape_donation import (
    RegisterAgapeDonationRequest,
    RegisterAgapeDonationResponse,
)
from models.schemas.agape.post.register_agape_family import (
    RegisterAgapeFamilyFormData,
)
from models.schemas.agape.post.register_agape_members import (
    RegisterAgapeMembersRequest,
)
from models.schemas.agape.post.register_agape_stock_item import (
    RegisterAgapeStockItemRequest,
)
from models.schemas.agape.post.register_agape_action import (
    RegisterAgapeActionRequest,
)
from models.schemas.agape.post.register_agape_action_name import (
    RegisterAgapeActionNameRequest,
)
from models.schemas.agape.post.register_agape_donation_receipts import (
    RegisterAgapeDonationReceiptsFormData,
)
from models.schemas.agape.put.supply_agape_stock import (
    SupplyAgapeStockRequest,
)
from models.schemas.agape.put.update_agape_action import (
    UpdateAgapeActionRequest,
)
from models.schemas.agape.put.update_agape_family_address import (
    UpdateAgapeFamilyAddressRequest,
)
from models.schemas.agape.put.update_agape_member import (
    UpdateAgapeMemberFormData,
)
from models.schemas.default import DefaultURLResponse, PaginationQuery
from repositories.agape_repository import AgapeRepository
from services.factories import file_service_factory
from services.google_maps_service import GoogleMapsAPI
from utils.response import (
    DefaultErrorResponseSchema,
    DefaultResponseSchema,
    response_handler,
)
from utils.verify_permission import permission_required

agape_controller = Blueprint("agape_controller", __name__, url_prefix="/agape")


@agape_controller.post("/cadastrar-familia")
@api.validate(
    form=RegisterAgapeFamilyFormData,
    resp=Response(
        HTTP_201=DefaultResponseSchema, HTTP_500=DefaultErrorResponseSchema
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("familia_agape", "criar")
def register_agape_family():
    """Cadastra uma familia ágape"""
    try:
        gmaps = GoogleMapsAPI()
        file_service = file_service_factory()
        register_family = RegisterAgapeFamily(database, gmaps, file_service)
        response = response_handler(register_family.execute(), save_logs=True)
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.post("/cadastrar-membros/<int:fk_familia_agape_id>")
@api.validate(
    json=RegisterAgapeMembersRequest,
    resp=Response(
        HTTP_201=DefaultResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("familia_agape", "criar")
def register_agape_members(fk_familia_agape_id: int):
    """Cadastra membros em uma família ágape pelo ID"""
    try:
        file_service = file_service_factory()
        register_member = RegisterAgapeMembers(database, file_service)
        response = response_handler(
            register_member.execute(fk_familia_agape_id),
            save_logs=True,
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.put("/editar-endereco-familia/<int:fk_familia_agape_id>")
@api.validate(
    json=UpdateAgapeFamilyAddressRequest,
    resp=Response(
        HTTP_200=DefaultResponseSchema, HTTP_500=DefaultErrorResponseSchema
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("familia_agape", "editar")
def update_agape_family_address(fk_familia_agape_id: int):
    """Edita o endereço de uma familia ágape pelo ID"""
    try:
        gmaps = GoogleMapsAPI()
        update_address = UpdateAgapeFamilyAddress(database, gmaps)
        response = response_handler(
            update_address.execute(fk_familia_agape_id), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.get("/buscar-endereco-familia/<int:fk_familia_agape_id>")
@api.validate(
    resp=Response(
        HTTP_200=GetFamilyAddressByIdResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("familia_agape", "acessar")
def get_family_address_by_id(fk_familia_agape_id: int):
    """Busca o endereço da familia agape pelo ID"""
    try:
        repository = AgapeRepository(database)
        get_family_address = GetFamilyAddressById(repository)
        response = response_handler(
            get_family_address.execute(fk_familia_agape_id), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.put("/editar-membro/<int:fk_membro_agape_id>")
@api.validate(
    form=UpdateAgapeMemberFormData,
    resp=Response(
        HTTP_200=DefaultResponseSchema, HTTP_500=DefaultErrorResponseSchema
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("familia_agape", "editar")
def update_agape_member(fk_membro_agape_id: int):
    """Edita um membro ágape pelo ID"""
    try:
        file_service = file_service_factory()
        update_member = UpdateAgapeMember(database, file_service)
        response = response_handler(
            update_member.execute(fk_membro_agape_id), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.delete("/deletar-membro/<int:fk_membro_agape_id>")
@api.validate(
    resp=Response(HTTP_204=None, HTTP_500=DefaultErrorResponseSchema),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("familia_agape", "deletar")
def delete_agape_member(fk_membro_agape_id: int):
    """Deleta um membro ágape pelo ID"""
    try:
        delete_member = DeleteAgapeMember(database)
        response = response_handler(
            delete_member.execute(fk_membro_agape_id), save_logs=True
        )
        return response
    except Exception as exception:
        database.session.rollback()
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.delete("/deletar-familia/<int:fk_familia_agape_id>")
@api.validate(
    resp=Response(HTTP_204=None, HTTP_500=DefaultErrorResponseSchema),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("familia_agape", "deletar")
def delete_agape_family(fk_familia_agape_id: int):
    """Deleta uma família ágape pelo ID"""
    try:
        delete_family = DeleteAgapeFamily(database)
        response = response_handler(
            delete_family.execute(fk_familia_agape_id), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.post("/cadastrar-item-estoque")
@api.validate(
    json=RegisterAgapeStockItemRequest,
    resp=Response(
        HTTP_201=DefaultResponseSchema, HTTP_500=DefaultErrorResponseSchema
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("estoque_agape", "criar")
def register_agape_stock_item():
    """Registra um item no estoque do Ágape"""
    try:
        register_item = RegisterAgapeStockItem(database)
        response = response_handler(register_item.execute(), save_logs=True)
        return response
    except Exception as exception:
        database.session.rollback()
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.put("/abastecer-estoque/<int:fk_estoque_agape_id>")
@api.validate(
    json=SupplyAgapeStockRequest,
    resp=Response(
        HTTP_200=DefaultResponseSchema, HTTP_500=DefaultErrorResponseSchema
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("estoque_agape", "editar")
def supply_agape_stock(fk_estoque_agape_id: int):
    """Adiciona quantidade de um determinado item no estoque pelo ID"""
    try:
        supply_stock = SupplyAgapeStock(database)
        response = response_handler(
            supply_stock.execute(fk_estoque_agape_id), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.post("/cadastrar-nome-acao-agape")
@api.validate(
    json=RegisterAgapeActionNameRequest,
    resp=Response(
        HTTP_201=DefaultResponseSchema, HTTP_500=DefaultErrorResponseSchema
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("acao_doacao_agape", "criar")
def register_agape_action_name():
    """Cadastra o nome de uma ação ágape"""
    try:
        register_action = RegisterAgapeActionName(database)
        response = response_handler(register_action.execute(), save_logs=True)
        return response
    except Exception as exception:
        database.session.rollback()
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.get("/listar-nomes-acoes-agape")
@api.validate(
    resp=Response(
        HTTP_200=GetAllAgapeActionsNamesResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("acao_doacao_agape", "acessar")
def get_all_agape_actions_names():
    """Retorna o nome de todas as ações ágape"""
    try:
        get_agape_actions = GetAllAgapeActionsNames()
        response = response_handler(
            get_agape_actions.execute(), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.post("/cadastrar-acao-agape")
@api.validate(
    json=RegisterAgapeActionRequest,
    resp=Response(
        HTTP_201=DefaultResponseSchema,
        HTTP_422=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("acao_doacao_agape", "criar")
def register_agape_action():
    """Cadastra uma nova ação ágape"""
    try:
        gmaps = GoogleMapsAPI()
        register_action = RegisterAgapeAction(database, gmaps)
        response = response_handler(register_action.execute(), save_logs=True)
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.get("/buscar-acao-agape/<int:fk_acao_agape_id>")
@api.validate(
    resp=Response(
        HTTP_200=GetAgapeActionByIdResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("acao_doacao_agape", "acessar")
def get_agape_action(fk_acao_agape_id: int):
    """Busca o último ciclo de uma ação ágape pelo ID"""
    try:
        repository = AgapeRepository(database)
        get_action = GetAgapeActionById(repository)
        response = response_handler(
            get_action.execute(fk_acao_agape_id), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.post("/registrar-doacao")
@api.validate(
    json=RegisterAgapeDonationRequest,
    resp=Response(
        HTTP_201=RegisterAgapeDonationResponse,
        HTTP_422=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("doacao_agape", "criar")
def register_agape_donation():
    """Registra uma doação de um ciclo de ação ágape"""
    try:
        register_donate = RegisterAgapeDonation(database)
        response = response_handler(register_donate.execute(), save_logs=True)
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.get("/listar-familias")
@api.validate(
    query=PaginationQuery,
    resp=Response(
        HTTP_200=GetAllAgapeFamiliesResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("familia_agape", "acessar")
def get_agape_families():
    """Lista todas as familias ágapes e suas informações"""
    try:
        repository = AgapeRepository(database)
        file_service = file_service_factory()
        get_families = GetAllAgapeFamilies(repository, file_service)
        response = response_handler(get_families.execute(), save_logs=True)
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.get("/listar-membros/<int:fk_familia_agape_id>")
@api.validate(
    query=PaginationQuery,
    resp=Response(
        HTTP_200=GetAllMembersByFamilyIdResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("familia_agape", "acessar")
def get_members_by_family_id(fk_familia_agape_id: int):
    """Lista os membros de uma família ágape pelo ID"""
    try:
        repository = AgapeRepository(database)
        get_members = GetAllMembersByFamilyId(repository)
        response = response_handler(
            get_members.execute(fk_familia_agape_id), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.get("/buscar-membro/<int:fk_membro_agape_id>")
@api.validate(
    resp=Response(
        HTTP_200=GetAgapeMemberResponse, HTTP_500=DefaultErrorResponseSchema
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("familia_agape", "acessar")
def get_agape_member(fk_membro_agape_id: int):
    """Busca um membro ágape pelo ID"""
    try:
        file_service = file_service_factory()
        repository = AgapeRepository(database)
        get_member = GetAgapeMember(repository, file_service)
        response = response_handler(
            get_member.execute(fk_membro_agape_id), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.get("/listar-itens-estoque")
@api.validate(
    resp=Response(
        HTTP_200=GetAllStockItemsResponse, HTTP_500=DefaultErrorResponseSchema
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("estoque_agape", "acessar")
def get_all_stock_items():
    """Lista os itens cadastrados no estoque"""
    try:
        get_items = GetAllStockItems()
        response = response_handler(get_items.execute(), save_logs=True)
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.get("/listar-acoes-agape")
@api.validate(
    query=GetAllAgapeActionsQuery,
    resp=Response(
        HTTP_200=GetAllAgapeActionsResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("acao_doacao_agape", "acessar")
def get_all_agape_actions():
    """Lista todas as ações ágape"""
    try:
        repository = AgapeRepository(database)
        get_actions = GetAllAgapeActions(repository)
        response = response_handler(get_actions.execute(), save_logs=True)
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.get("/listar-beneficiarios/<int:fk_instancia_acao_agape_id>")
@api.validate(
    query=GetBeneficiariesByAgapeActionIdQuery,
    resp=Response(
        HTTP_200=GetBeneficiariesByAgapeActionIdResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("doacao_agape", "acessar")
def get_beneficiaries(fk_instancia_acao_agape_id: int):
    """Retorna os beneficiarios de um ciclo de doação ágape pelo ID"""
    try:
        file_service = file_service_factory()
        repository = AgapeRepository(database)
        get_beneficiaries = GetBeneficiariesByAgapeActionInstanceId(
            repository, file_service
        )
        response = response_handler(
            get_beneficiaries.execute(fk_instancia_acao_agape_id),
            save_logs=True,
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.get("/listar-ciclos-acoes-agape")
@api.validate(
    query=GetAllAgapeActionsInstancesQuery,
    resp=Response(
        HTTP_200=GetAllAgapeActionsInstancesResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("acao_doacao_agape", "acessar")
def get_all_agape_actions_instances():
    """Retorna todos os ciclos de todas as ações ágape"""
    try:
        repository = AgapeRepository(database)
        get_instances = GetAllAgapeActionsInstances(repository)
        response = response_handler(get_instances.execute(), save_logs=True)
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.get(
    "/buscar-familia-agape-por-cpf/<string:cpf>/<int:fk_instancia_acao_agape_id>"
)
@api.validate(
    resp=Response(
        HTTP_200=GetAgapeFamilyByCpfResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("familia_agape", "acessar")
def get_agape_family_by_cpf(cpf: str, fk_instancia_acao_agape_id: int):
    """Busca os dados de uma família ágape pelo CPF de um responsável"""
    try:
        repository = AgapeRepository(database)
        file_service = file_service_factory()
        get_family = GetAgapeFamilyByCpf(repository, file_service)
        response = response_handler(
            get_family.execute(cpf, fk_instancia_acao_agape_id), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.get(
    "/buscar-itens-ciclo-acao-agape/<int:fk_instancia_acao_agape_id>"
)
@api.validate(
    resp=Response(
        HTTP_200=GetAgapeInstanceItemsResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("acao_doacao_agape", "acessar")
def get_agape_instance_items(fk_instancia_acao_agape_id: int):
    """Retorna os itens cadastrados no ciclo da ação ágape"""
    try:
        repository = AgapeRepository(database)
        get_items = GetAgapeInstanceItems(repository)
        response = response_handler(
            get_items.execute(fk_instancia_acao_agape_id), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.post(
    "/registrar-recibos-doacao-agape/<int:fk_doacao_agape_id>"
)
@api.validate(
    form=RegisterAgapeDonationReceiptsFormData,
    resp=Response(
        HTTP_201=DefaultResponseSchema, HTTP_500=DefaultErrorResponseSchema
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("doacao_agape", "criar")
def register_agape_donation_receipts(fk_doacao_agape_id: int):
    """Registra os recibos emitidos na doação"""
    try:
        file_service = file_service_factory()
        register_receipts = RegisterAgapeDonationReceipts(
            database, file_service
        )
        response = response_handler(
            register_receipts.execute(fk_doacao_agape_id)
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.put(
    "/iniciar-ciclo-acao-agape/<int:fk_instancia_acao_agape_id>"
)
@api.validate(
    resp=Response(
        HTTP_200=DefaultResponseSchema,
        HTTP_422=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("acao_doacao_agape", "editar")
def start_agape_action_instance(fk_instancia_acao_agape_id: int):
    """Inicia um ciclo de ação Ágape pelo ID"""
    try:
        start_instance = StartAgapeActionInstance(database)
        response = response_handler(
            start_instance.execute(fk_instancia_acao_agape_id), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.put(
    "/finalizar-ciclo-acao-agape/<int:fk_instancia_acao_agape_id>"
)
@api.validate(
    resp=Response(
        HTTP_200=DefaultResponseSchema,
        HTTP_422=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("acao_doacao_agape", "editar")
def finish_agape_action_instance(fk_instancia_acao_agape_id: int):
    """Finaliza um ciclo de ação Ágape pelo ID"""
    try:
        finish_instance = FinishAgapeActionInstance(database)
        response = response_handler(
            finish_instance.execute(fk_instancia_acao_agape_id), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.get(
    "/listar-itens-doados-beneficiario/<int:fk_doacao_agape_id>"
)
@api.validate(
    resp=Response(
        HTTP_200=GetBeneficiaryDonatedItemsResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("doacao_agape", "acessar")
def get_beneficiary_donated_items(fk_doacao_agape_id: int):
    """Retorna os itens doados para um beneficiário pelo ID da doação"""
    try:
        repository = AgapeRepository(database)
        get_items = GetBeneficiaryDonatedItems(repository)
        response = response_handler(
            get_items.execute(fk_doacao_agape_id), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.get("/listar-historico-movimentacoes-agape")
@api.validate(
    query=GetAgapeItemsBalanceHistoryQuery,
    resp=Response(
        HTTP_200=GetAgapeItemsBalanceHistoryResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("estoque_agape", "acessar")
def get_agape_items_balance_history():
    """Retorna o histórico de movimentações do estoque da ação ágape"""
    try:
        repository = AgapeRepository(database)
        get_history = GetAgapeItemsBalanceHistory(repository)
        response = response_handler(get_history.execute(), save_logs=True)
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.get(
    "/buscar-ciclo-acao-agape/<int:fk_instancia_acao_agape_id>"
)
@api.validate(
    resp=Response(
        HTTP_200=GetAgapeActionInstanceByIdResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("acao_doacao_agape", "acessar")
def get_agape_action_instance_by_id(fk_instancia_acao_agape_id: int):
    """Busca um ciclo de ação ágape pelo ID"""
    try:
        repository = AgapeRepository(database)
        get_action_instance = GetAgapeActionInstanceById(repository)
        response = response_handler(
            get_action_instance.execute(fk_instancia_acao_agape_id),
            save_logs=True,
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.put(
    "/editar-ciclo-acao-agape/<int:fk_instancia_acao_agape_id>"
)
@api.validate(
    json=UpdateAgapeActionRequest,
    resp=Response(
        HTTP_200=DefaultResponseSchema,
        HTTP_422=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("acao_doacao_agape", "editar")
def update_agape_action(fk_instancia_acao_agape_id: int):
    """Edita um ciclo de ação ágape pelo ID"""
    try:
        gmaps = GoogleMapsAPI()
        update_action = UpdateAgapeAction(database, gmaps)
        response = response_handler(
            update_action.execute(fk_instancia_acao_agape_id), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.get("/cards-estatisticas-familias-agape")
@api.validate(
    resp=Response(
        HTTP_200=GetCardsAgapeFamiliesStatisticsResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("familia_agape", "acessar")
def get_cards_agape_families_statistics():
    """Retorna as estatisticas dos cards de famílias ágape"""
    try:
        repository = AgapeRepository(database)
        get_card = GetCardsAgapeFamiliesStatistics(repository)
        response = response_handler(get_card.execute())
        return response
    except Exception as exception:
        error_response = errors_handler(exception)
        return error_response


@agape_controller.get("/cards-estatisticas-itens-estoque")
@api.validate(
    resp=Response(
        HTTP_200=GetCardsStockItemsStatisticsResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("estoque_agape", "acessar")
def get_cards_stock_items_statistics():
    """Retorna as estatisticas dos cards de itens do estoque"""
    try:
        repository = AgapeRepository(database)
        get_card = GetCardsStockItemsStatistics(repository)
        response = response_handler(get_card.execute())
        return response
    except Exception as exception:
        error_response = errors_handler(exception)
        return error_response


@agape_controller.get("/card-renda-familiar-agape/<int:fk_familia_agape_id>")
@api.validate(
    resp=Response(
        HTTP_200=GetCardAgapeFamilyIncomeResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("familia_agape", "acessar")
def get_card_agape_family_income(fk_familia_agape_id: int):
    """Retorna o card de renda familiar da família ágape pelo ID"""
    try:
        repository = AgapeRepository(database)
        get_card = GetCardAgapeFamilyIncome(repository)
        response = response_handler(get_card.execute(fk_familia_agape_id))
        return response
    except Exception as exception:
        error_response = errors_handler(exception)
        return error_response


@agape_controller.get("/card-total-recebimentos/<int:fk_familia_agape_id>")
@api.validate(
    resp=Response(
        HTTP_200=GetCardTotalDonationsReceiptsResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("familia_agape", "acessar")
def get_card_total_donations_receipts(fk_familia_agape_id: int):
    """Retorna o card de itens recebidos pela família ágape pelo ID"""
    try:
        repository = AgapeRepository(database)
        get_card = GetCardTotalDonationsReceipts(repository)
        response = response_handler(get_card.execute(fk_familia_agape_id))
        return response
    except Exception as exception:
        error_response = errors_handler(exception)
        return error_response


@agape_controller.get("/listar-doacoes-recebidas/<int:fk_familia_agape_id>")
@api.validate(
    query=PaginationQuery,
    resp=Response(
        HTTP_200=GetAllDonationsReceiptsResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("familia_agape", "acessar")
def get_all_donations_receipts(fk_familia_agape_id: int):
    """Retorna todas as doações recebidas pela família ágape pelo ID"""
    try:
        file_service = file_service_factory()
        repository = AgapeRepository(database)
        get_card = GetAllDonationsReceipts(repository, file_service)
        response = response_handler(
            get_card.execute(fk_familia_agape_id), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.get(
    "/listar-itens-recebidos/<int:fk_instancia_acao_agape_id>/<int:doacao_agape_id>"
)
@api.validate(
    resp=Response(
        HTTP_200=GetAllItemsReceiptsResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("familia_agape", "acessar")
def get_all_items_receipts(
    fk_instancia_acao_agape_id: int, doacao_agape_id: int
):
    """Retorna todos os itens recebidos pela família ágape pelo ID"""
    try:
        repository = AgapeRepository(database)
        get_card = GetAllItemsReceipts(repository)
        response = response_handler(
            get_card.execute(fk_instancia_acao_agape_id, doacao_agape_id),
            save_logs=True,
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.get(
    "/buscar-endereco-instancia-acao-agape/<int:fk_instancia_acao_agape_id>"
)
@api.validate(
    resp=Response(
        HTTP_200=GetAgapeInstanceAddressResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("acao_doacao_agape", "acessar")
def get_agape_instance_address(fk_instancia_acao_agape_id: int):
    """Retorna o endereço do ciclo da ação ágape pelo ID"""
    try:
        repository = AgapeRepository(database)
        get_card = GetAgapeInstanceAddress(repository)
        response = response_handler(
            get_card.execute(fk_instancia_acao_agape_id), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.get("/listar-enderecos-familias-agape")
@api.validate(
    resp=Response(
        HTTP_200=GetAllAgapeFamiliesAddressResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("familia_agape", "acessar")
def get_all_agape_families_address():
    """Retorna todos os endereços das família ágape"""
    try:
        repository = AgapeRepository(database)
        get_card = GetAllAgapeFamiliesAddress(repository)
        response = response_handler(get_card.execute(), save_logs=True)
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.get(
    "/listar-geolocalizacoes-beneficiarios-ciclo-acao-agape/<int:fk_instancia_acao_agape_id>"
)
@api.validate(
    resp=Response(
        HTTP_200=GetInstanceBeneficiariesAddressesGeolocationResponse,
        HTTP_422=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("doacao_agape", "acessar")
def get_agape_beneficiaries_addresses_geolocation(
    fk_instancia_acao_agape_id: int,
):
    """Retorna a geolocalização dos beneficiários de um ciclo de doação ágape pelo ID"""
    try:
        repository = AgapeRepository(database)
        get_geo_locations = GetInstanceBeneficiariesAddressesGeolocation(
            repository
        )
        response = response_handler(
            get_geo_locations.execute(fk_instancia_acao_agape_id),
            save_logs=True,
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.delete(
    "/deletar-ciclo-acao-agape/<int:fk_instancia_acao_agape_id>"
)
@api.validate(
    resp=Response(
        HTTP_200=None,
        HTTP_422=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
@permission_required("acao_doacao_agape", "deletar")
def delete_agape_action_instance(fk_instancia_acao_agape_id: int):
    """Deleta um ciclo de doação ágape pelo ID"""
    try:
        delete_agape_instance = DeleteAgapeActionInstance(database)
        response = response_handler(
            delete_agape_instance.execute(fk_instancia_acao_agape_id),
            save_logs=True,
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.put("/atualizar-permissoes-voluntarios")
@api.validate(
    resp=Response(
        HTTP_204=None,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
def update_agape_volunteers_permissions():
    """Atualiza as permissoes dos voluntários para o fluxo de família ágape"""
    try:
        allowed_profiles = [
            ProfilesEnum.ADMINISTRADOR,
            ProfilesEnum.ADMINISTRADOR_AGAPE,
        ]
        if current_user["nome_perfil"] not in allowed_profiles:
            raise ForbiddenError(
                "Você não tem permissão para realizar esta ação."
            )

        repository = AgapeRepository(database)
        update_permissions = UpdateAgapeVolunteersPermissions(repository)
        response = response_handler(
            update_permissions.execute(), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.get("/status-permissao-voluntarios")
@api.validate(
    resp=Response(
        HTTP_200=GetAgapeVolunteersPermissionsStatusResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
def get_agape_volunteers_permissions_status():
    """
    Retorna o status das permissoes dos voluntários para o fluxo de família ágape
    """
    try:
        allowed_profiles = [
            ProfilesEnum.ADMINISTRADOR,
            ProfilesEnum.ADMINISTRADOR_AGAPE,
        ]
        if current_user["nome_perfil"] not in allowed_profiles:
            raise ForbiddenError(
                "Você não tem permissão para realizar esta ação."
            )

        repository = AgapeRepository(database)
        get_permissions = GetAgapeVolunteersPermissionsStatus(repository)
        response = response_handler(get_permissions.execute(), save_logs=True)
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.get("/listar-voluntarios-agape")
@api.validate(
    resp=Response(
        HTTP_200=GetAgapeVolunteersResponse,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
def get_agape_volunteers():
    """Retorna todos os voluntários ágape"""
    try:
        allowed_profiles = [
            ProfilesEnum.ADMINISTRADOR,
            ProfilesEnum.ADMINISTRADOR_AGAPE,
        ]
        if current_user["nome_perfil"] not in allowed_profiles:
            raise ForbiddenError(
                "Você não tem permissão para realizar esta ação."
            )

        repository = AgapeRepository(database)
        get_volunteers = GetAgapeVolunteers(repository)
        response = response_handler(get_volunteers.execute(), save_logs=True)
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.put("/adicionar-voluntario-agape/<int:fk_usuario_id>")
@api.validate(
    resp=Response(
        HTTP_204=None,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
def add_agape_volunteer(fk_usuario_id: int):
    """Adiciona um voluntário ágape"""
    try:
        allowed_profiles = [
            ProfilesEnum.ADMINISTRADOR,
            ProfilesEnum.ADMINISTRADOR_AGAPE,
        ]
        if current_user["nome_perfil"] not in allowed_profiles:
            raise ForbiddenError(
                "Você não tem permissão para realizar esta ação."
            )

        repository = AgapeRepository(database)
        add_volunteer = UpdateUserToAgapeVoluntary(repository)
        response = response_handler(
            add_volunteer.execute(fk_usuario_id), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.delete("/remover-voluntario-agape/<int:fk_usuario_id>")
@api.validate(
    resp=Response(
        HTTP_204=None,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Ágape"],
)
@jwt_required()
def remove_agape_volunteer(fk_usuario_id: int):
    """Remove um voluntário ágape"""
    try:
        allowed_profiles = [
            ProfilesEnum.ADMINISTRADOR,
            ProfilesEnum.ADMINISTRADOR_AGAPE,
        ]
        if current_user["nome_perfil"] not in allowed_profiles:
            raise ForbiddenError(
                "Você não tem permissão para realizar esta ação."
            )

        repository = AgapeRepository(database)
        remove_volunteer = RemoveUserFromAgapeVoluntary(repository)
        response = response_handler(
            remove_volunteer.execute(fk_usuario_id), save_logs=True
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.get("/exportar-familias")
@api.validate(
    resp=Response(
        HTTP_200=DefaultURLResponse, HTTP_500=DefaultErrorResponseSchema
    ),
    tags=["Ágape"],
)
@jwt_required()
def export_agape_families():
    """Exporta os dados de família ágape"""
    try:
        allowed_profiles = [
            ProfilesEnum.ADMINISTRADOR,
            ProfilesEnum.ADMINISTRADOR_AGAPE,
        ]
        if current_user["nome_perfil"] not in allowed_profiles:
            raise ForbiddenError(
                "Você não tem permissão para realizar esta ação."
            )

        repository = AgapeRepository(database)
        export_families = ExportAgapeFamilies(repository)
        response = response_handler(export_families.execute(), save_logs=True)
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response


@agape_controller.get(
    "/exportar-doacoes-beneficiados/<int:fk_instancia_acao_agape_id>"
)
@api.validate(
    resp=Response(
        HTTP_200=DefaultURLResponse, HTTP_500=DefaultErrorResponseSchema
    ),
    tags=["Ágape"],
)
@jwt_required()
def export_agape_donations(fk_instancia_acao_agape_id: int):
    """Exporta os dados de doações a beneficiados"""
    try:
        allowed_profiles = [
            ProfilesEnum.ADMINISTRADOR,
            ProfilesEnum.ADMINISTRADOR_AGAPE,
        ]
        if current_user["nome_perfil"] not in allowed_profiles:
            raise ForbiddenError(
                "Você não tem permissão para realizar esta ação."
            )

        repository = AgapeRepository(database)
        export_donations = ExportAgapeDonations(repository)
        response = response_handler(
            export_donations.execute(fk_instancia_acao_agape_id),
            save_logs=True,
        )
        return response
    except Exception as exception:
        error_response = errors_handler(exception, save_logs=True)
        return error_response
