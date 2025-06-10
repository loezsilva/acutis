import json
import logging
import uuid
from http import HTTPStatus

from flask import Blueprint
from flask import request as flask_request
from flask_jwt_extended import current_user, jwt_required
from spectree import Response

from acutis_api.application.use_cases.agape import (
    AbastecerItemEstoqueAgapeUseCase,
    AdicionarVoluntarioAgapeUseCase,
    AtualizarPermissoesVoluntariosUseCase,
    BuscarCicloAcaoAgapeUseCase,
    BuscarEnderecoCicloAcaoUseCase,
    BuscarEnderecoFamiliaAgapeUseCase,
    BuscarFamiliaAgapePorCpfUseCase,
    BuscarItensCicloAcaoAgapeUseCase,
    BuscarMembroAgapePorIdUseCase,
    BuscarUltimaAcaoAgapeUseCase,
    CardRendaFamiliarAgapeUseCase,
    CardsEstatisticasFamiliasAgapeUseCase,
    CardsEstatisticasItensEstoqueUseCase,
    CardTotalRecebimentosAgapeUseCase,
    DeletarCicloAcaoAgapeUseCase,
    DeletarFamiliaAgapeUseCase,
    DeletarMembroAgapeUseCase,
    DeletarVoluntarioAgapeUseCase,
    EditarCicloAcaoAgapeUseCase,
    EditarEnderecoFamiliaAgapeUseCase,
    EditarMembroAgapeUseCase,
    ExcluirItemEstoqueAgapeUseCase,
    ExportarDoacoesBeneficiadosUseCase,
    ExportarFamiliasAgapeUseCase,
    FinalizarCicloAcaoAgapeUseCase,
    IniciarCicloAcaoAgapeUseCase,
    ListarBeneficiariosAgapeUseCase,
    ListarCicloAcoesAgapeUseCase,
    ListarDoacoesRecebidasFamiliaUseCase,
    ListarEnderecosFamiliasAgapeUseCase,
    ListarFamiliasUseCase,
    ListarGeolocalizacoesBeneficiariosUseCase,
    ListarHistoricoMovimentacoesAgapeUseCase,
    ListarItensDoadosBeneficiarioUseCase,
    ListarItensEstoqueAgapeUseCase,
    ListarItensRecebidosUseCase,
    ListarMembrosFamiliaUseCase,
    ListarNomesAcoesAgapeUseCase,
    ListarStatusPermissaoVoluntariosUseCase,
    ListarVoluntariosAgapeUseCase,
    RegistrarCicloAcaoAgapeUseCase,
    RegistrarDoacaoAgapeUseCase,
    RegistrarEstoqueAgapeUseCase,
    RegistrarFamiliaAgapeUseCase,
    RegistrarMembrosFamiliaAgapeUseCase,
    RegistrarNomeAcaoAgapeUseCase,
    RegistrarRecibosDoacaoAgapeUseCase,
    RemoverItemEstoqueAgapeUseCase,
)
from acutis_api.communication.enums.membros import PerfilEnum
from acutis_api.communication.requests.agape import (
    AbastecerItemEstoqueAgapeRequest,
    EditarEnderecoFamiliaAgapeRequest,
    EditarMembroAgapeFormData,
    ListarCiclosAcoesAgapeQueryPaginada,
    ListarFamiliasAgapeQueryPaginada,
    ListarHistoricoMovimentacoesAgapeQueryPaginada,
    ListarItensEstoqueAgapeQueryPaginada,
    ListarNomesAcoesAgapeQueryPaginada,
    MembrosAgapeCadastroRequest,
    RegistrarDoacaoAgapeRequestSchema,
    RegistrarItemEstoqueAgapeRequest,
    RegistrarNomeAcaoAgapeRequest,
    RegistrarOuEditarCicloAcaoAgapeRequest,
    RegistrarOuEditarFamiliaAgapeFormData,
    RegistrarRecibosRequestScheme,
    RemoverItemEstoqueAgapeRequest,
)
from acutis_api.communication.responses.agape import (
    BuscarCicloAcaoAgapeResponse,
    BuscarItensCicloAcaoAgapeResponse,
    CardRendaFamiliarAgapeResponse,
    CardsEstatisticasFamiliasAgapeResponse,
    CardsEstatisticasItensEstoqueResponse,
    CardTotalRecebimentosAgapeResponse,
    EnderecoCicloAcaoResponse,
    EnderecoResponse,
    FamiliaAgapeDetalhesPorCpfResponse,
    ItemEstoqueAgapeResponse,
    ListarBeneficiariosAgapeResponse,
    ListarCiclosAcoesAgapeResponsePaginada,
    ListarDoacoesRecebidasFamiliaResponse,
    ListarEnderecosFamiliasAgapeResponse,
    ListarFamiliasAgapeResponsePaginada,
    ListarGeolocalizacoesBeneficiariosResponse,
    ListarHistoricoMovimentacoesAgapeResponsePaginada,
    ListarItensDoadosBeneficiarioResponse,
    ListarItensEstoqueAgapeResponsePaginada,
    ListarMembrosFamiliaAgapeResponsePaginada,
    ListarNomesAcoesAgapeResponsePaginada,
    ListarStatusPermissaoVoluntariosResponse,
    ListarVoluntariosAgapeResponse,
    MembroAgapeDetalhesResponse,
    RegistrarAcaoAgapeResponse,
    RegistrarDoacaoAgapeResponse,
    RegistrarItemEstoqueAgapeResponse,
    RegistrarRecibosResponse,
    UltimoCicloAcaoAgapeResponse,
    parse_datas_padrao_brasileiro,
)
from acutis_api.communication.responses.padrao import (
    ErroPadraoResponse,
    ResponsePadraoSchema,
)
from acutis_api.domain.repositories.schemas.agape import (
    ListarMembrosFamiliaAgapeFiltros,
    PaginacaoSchema,
)
from acutis_api.domain.services.google_maps_service import GoogleMapsAPI
from acutis_api.exception.errors.forbidden import HttpForbiddenError
from acutis_api.exception.errors_handler import errors_handler
from acutis_api.infrastructure.extensions import database, swagger
from acutis_api.infrastructure.repositories.agape import (
    AgapeRepository,
)
from acutis_api.infrastructure.services.factories import file_service_factory

agape_bp = Blueprint('agape_bp', __name__, url_prefix='/agape')
logger = logging.getLogger()


@agape_bp.before_request
@jwt_required()
def requer_jwt_token():
    """Esssa função adiciona autenticação as rotas ágape"""
    pass


@agape_bp.after_request
def parser_date_and_datetime(response):
    if response.content_type == 'application/json':
        try:
            data = json.loads(response.get_data())
            parsed_data = parse_datas_padrao_brasileiro(data)
            response.set_data(json.dumps(parsed_data))
        except Exception as e:
            logger.exception(f'Erro ao parsear datas: {e}')

    return response


# ROTAS PARA NOME DAS AÇÕES
@agape_bp.post('/registrar-nome-acao')
@swagger.validate(
    json=RegistrarNomeAcaoAgapeRequest,
    resp=Response(
        HTTP_201=RegistrarAcaoAgapeResponse,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Ações'],
)
def registrar_nome_acao_agape():
    """
    Registrar o nome de uma ação
    """
    try:
        request = RegistrarNomeAcaoAgapeRequest.model_validate(
            flask_request.json
        )

        repository = AgapeRepository(database)
        usecase = RegistrarNomeAcaoAgapeUseCase(repository)
        response = usecase.execute(request)
        return response, HTTPStatus.CREATED

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.get('/buscar-endereco-familia/<uuid:familia_id>')
@swagger.validate(
    resp=Response(
        HTTP_200=EnderecoResponse,
        HTTP_404=ErroPadraoResponse,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Familias'],
)
def buscar_endereco_familia(familia_id):
    """Busca o endereço de uma família ágape pelo ID da família."""
    try:
        repository = AgapeRepository(database)
        use_case = BuscarEnderecoFamiliaAgapeUseCase(
            agape_repository=repository
        )
        endereco_response = use_case.execute(familia_id=familia_id)
        return endereco_response, HTTPStatus.OK

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.get('/listar-nomes-acoes')
@swagger.validate(
    query=ListarNomesAcoesAgapeQueryPaginada,
    resp=Response(
        HTTP_200=ListarNomesAcoesAgapeResponsePaginada,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Ações'],
)
def listar_nomes_acoes():
    """
    Listar nomes das ações
    """
    try:
        params = flask_request.args.to_dict()
        repository = AgapeRepository(database)
        usecase = ListarNomesAcoesAgapeUseCase(repository)
        filtros = ListarNomesAcoesAgapeQueryPaginada.model_validate(params)
        response = usecase.execute(filtros)
        return response, HTTPStatus.OK

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


# INICIA AS ROTAS PARA ESTOQUE
@agape_bp.post('/registrar-item')
@swagger.validate(
    json=RegistrarItemEstoqueAgapeRequest,
    resp=Response(
        HTTP_201=RegistrarItemEstoqueAgapeResponse,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Estoque'],
)
def registrar_item_estoque_agape():
    """
    Registrar um item no estoque
    """
    try:
        request = RegistrarItemEstoqueAgapeRequest.model_validate(
            flask_request.json
        )

        repository = AgapeRepository(database)
        usecase = RegistrarEstoqueAgapeUseCase(repository)
        response = usecase.execute(request)
        return response, HTTPStatus.CREATED

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.get('/listar-itens')
@swagger.validate(
    query=ListarItensEstoqueAgapeQueryPaginada,
    resp=Response(
        HTTP_200=ListarItensEstoqueAgapeResponsePaginada,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Estoque'],
)
def listar_itens_estoque_agape():
    """
    Listar nomes das ações
    """
    try:
        repository = AgapeRepository(database)
        usecase = ListarItensEstoqueAgapeUseCase(repository)
        filtros = ListarItensEstoqueAgapeQueryPaginada.model_validate(
            flask_request.args.to_dict()
        )
        response = usecase.execute(filtros)
        return response, HTTPStatus.OK
    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.put('/abastecer-item/<uuid:item_id>')
@swagger.validate(
    json=AbastecerItemEstoqueAgapeRequest,
    resp=Response(
        HTTP_200=ItemEstoqueAgapeResponse,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Estoque'],
)
def abastecer_item_estoque_agape(item_id):
    """
    Abastecer um item do estoque, adicionando a quantidade fornecida à
    quantidade existente
    """
    try:
        request = AbastecerItemEstoqueAgapeRequest.model_validate(
            flask_request.json
        )
        repository = AgapeRepository(database)
        usecase = AbastecerItemEstoqueAgapeUseCase(repository)
        response = usecase.execute(item_id, request)
        return response, HTTPStatus.OK
    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


# Essa rota não está na lista de rotas da versão antiga.
@agape_bp.put('/remover-item/<uuid:item_id>')
@swagger.validate(
    json=RemoverItemEstoqueAgapeRequest,
    resp=Response(
        HTTP_200=ItemEstoqueAgapeResponse,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Estoque'],
)
def remover_item_estoque_agape(item_id):
    """
    Remover uma quantidade de um item do estoque, subtraindo a quantidade
    fornecida
    """
    try:
        request = RemoverItemEstoqueAgapeRequest.model_validate(
            flask_request.json
        )

        repository = AgapeRepository(database)
        usecase = RemoverItemEstoqueAgapeUseCase(repository)
        response = usecase.execute(item_id, request)
        return response, HTTPStatus.OK
    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.delete('/deletar-item/<uuid:item_id>')
@swagger.validate(
    resp=Response(
        HTTP_200=ResponsePadraoSchema,
        HTTP_500=ErroPadraoResponse,
    ),
    tags=['Ágape - Estoque'],
)
def deletar_item_estoque_agape(item_id):
    """
    Excluir um item de estoque completamente do banco de dados
    """
    try:
        repository = AgapeRepository(database)
        usecase = ExcluirItemEstoqueAgapeUseCase(repository)
        usecase.execute(item_id)

        return {
            'msg': 'Item de estoque excluído com sucesso.'
        }, HTTPStatus.NO_CONTENT

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


# FIM DAS ROTAS DE ESTOQUE


# ROTAS PARA CICLO DE AÇÕES ÁGAPE
# Rota para registrar ciclo de ação Ágape completo
@agape_bp.post('/registrar-ciclo-acao')
@swagger.validate(
    json=RegistrarOuEditarCicloAcaoAgapeRequest,
    resp=Response(
        HTTP_201=ResponsePadraoSchema,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Ações'],
)
def registrar_ciclo_acao_agape():
    """
    Registra um ciclo de ação Ágape

    Abrangencias válidas:
        cep \n
        rua \n
        bairro \n
        cidade \n
        estado \n
        sem_restricao \n
    """

    try:
        request = RegistrarOuEditarCicloAcaoAgapeRequest.model_validate(
            flask_request.json
        )

        repository = AgapeRepository(database)
        gmaps = GoogleMapsAPI()

        usecase = RegistrarCicloAcaoAgapeUseCase(repository, gmaps)

        usecase.execute(dados=request)
        return {
            'msg': 'Ciclo da ação Ágape cadastrado com sucesso.'
        }, HTTPStatus.CREATED

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


# Rota para editar ciclo de ação Ágape
@agape_bp.put('/editar-ciclo-acao/<uuid:acao_agape_id>')
@swagger.validate(
    json=RegistrarOuEditarCicloAcaoAgapeRequest,
    resp=Response(HTTP_200=ResponsePadraoSchema, HTTP_422=ErroPadraoResponse),
    tags=['Ágape - Ações'],
)
def editar_ciclo_acao_agape(acao_agape_id):
    """Edita um ciclo de ação Ágape não iniciado"""
    try:
        json_data = flask_request.get_json()
        form = RegistrarOuEditarCicloAcaoAgapeRequest.model_validate(json_data)

        repository = AgapeRepository(database)
        gmaps = GoogleMapsAPI()

        usecase = EditarCicloAcaoAgapeUseCase(repository, gmaps)

        usecase.execute(acao_agape_id, dados=form)

        return {'msg': 'Ciclo da ação atualizado com sucesso.'}, HTTPStatus.OK

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.put('/iniciar-ciclo-acao-agape/<uuid:acao_agape_id>')
@swagger.validate(
    resp=Response(HTTP_200=ResponsePadraoSchema, HTTP_422=ErroPadraoResponse),
    tags=['Ágape - Ações'],
)
def iniciar_ciclo_acao_agape(acao_agape_id):
    """Inicia um ciclo de uma ação Ágape"""
    try:
        repository = AgapeRepository(database)

        usecase = IniciarCicloAcaoAgapeUseCase(repository)

        usecase.execute(acao_agape_id)

        return {'msg': 'Ciclo da ação iniciado com sucesso.'}, HTTPStatus.OK

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


# Finalizar ciclo
@agape_bp.put('/finalizar-ciclo-acao-agape/<uuid:acao_agape_id>')
@swagger.validate(
    resp=Response(HTTP_200=ResponsePadraoSchema, HTTP_422=ErroPadraoResponse),
    tags=['Ágape - Ações'],
)
def finalizar_ciclo_acao_agape(acao_agape_id):
    """Finaliza um ciclo de uma ação Ágape"""
    try:
        repository = AgapeRepository(database)

        usecase = FinalizarCicloAcaoAgapeUseCase(repository)

        usecase.execute(acao_agape_id)

        return {'msg': 'Ciclo da ação finalizado com sucesso.'}, HTTPStatus.OK

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


# Deletar ciclo
@agape_bp.delete('/deletar-ciclo-acao-agape/<uuid:acao_agape_id>')
@swagger.validate(
    resp=Response(HTTP_204=None, HTTP_422=ErroPadraoResponse),
    tags=['Ágape - Ações'],
)
def deletar_ciclo_acao_agape(acao_agape_id):
    """Deleta um ciclo de uma ação Ágape"""
    try:
        repository = AgapeRepository(database)

        usecase = DeletarCicloAcaoAgapeUseCase(repository)

        usecase.execute(acao_agape_id)

        return {}, HTTPStatus.NO_CONTENT

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


# Buscar itens de ciclo
@agape_bp.get('/buscar-itens-ciclo-acao-agape/<uuid:acao_agape_id>')
@swagger.validate(
    resp=Response(
        HTTP_200=BuscarItensCicloAcaoAgapeResponse, HTTP_422=ErroPadraoResponse
    ),
    tags=['Ágape - Ações'],
)
def buscar_itens_ciclo_acao_agape(acao_agape_id):
    """Busca itens de um ciclo de ação Ágape pelo ID do ciclo de ação."""

    try:
        repository = AgapeRepository(database)
        usecase = BuscarItensCicloAcaoAgapeUseCase(repository)
        response = usecase.execute(acao_agape_id)
        return response, HTTPStatus.OK

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


# Buscar ciclo
@agape_bp.get('/buscar-ciclo-acao-agape/<uuid:acao_agape_id>')
@swagger.validate(
    resp=Response(
        HTTP_200=BuscarCicloAcaoAgapeResponse, HTTP_422=ErroPadraoResponse
    ),
    tags=['Ágape - Ações'],
)
def buscar_ciclo_acao_agape(acao_agape_id):
    """Busca detalhes de um ciclo de ação Ágape pelo ID do ciclo de ação."""
    try:
        repository = AgapeRepository(database)

        usecase = BuscarCicloAcaoAgapeUseCase(repository)

        response = usecase.execute(acao_agape_id)

        return response, HTTPStatus.OK

    except Exception as exc:
        database.session.rollback()

        return errors_handler(exc)


@agape_bp.get('/listar-ciclo-acoes-agape')
@swagger.validate(
    query=ListarCiclosAcoesAgapeQueryPaginada,
    resp=Response(
        HTTP_200=ListarCiclosAcoesAgapeResponsePaginada,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Ações'],
)
def listar_ciclo_acoes_agape():
    """Lista todas as ações Ágape com contagem de ciclos
    (rota antiga /listar-acoes-agape).
    """
    try:
        repository = AgapeRepository(database)
        usecase = ListarCicloAcoesAgapeUseCase(repository)
        filtros = ListarCiclosAcoesAgapeQueryPaginada.model_validate(
            flask_request.args.to_dict()
        )
        response = usecase.execute(filtros)
        return response, HTTPStatus.OK
    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


# ROTA PARA FAMILIAS
@agape_bp.post('/registrar-familia')
@swagger.validate(
    form=RegistrarOuEditarFamiliaAgapeFormData,
    resp=Response(
        HTTP_201=ResponsePadraoSchema,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Familias'],
)
def registrar_familia():
    """
    Cadastra uma nova família Ágape

    Observações:
    \n
    - `comprovante_residencia` é opcional, deve ser um arquivo do tipo file
    \n
    - `fotos_familia` é opcional, deve ser uma lista de arquivos do tipo file
    \n
    - O campo `foto_documento` em membros deve ser um arquivo em `base64`
    """

    try:
        form_data = flask_request.form

        repository = AgapeRepository(database)
        gmaps = GoogleMapsAPI()
        file_service = file_service_factory()

        usecase = RegistrarFamiliaAgapeUseCase(
            repository,
            gmaps,
            file_service,
        )

        response = usecase.execute(form_data)
        return response, HTTPStatus.CREATED

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.get('/listar-familias')
@swagger.validate(
    query=ListarFamiliasAgapeQueryPaginada,
    resp=Response(
        HTTP_200=ListarFamiliasAgapeResponsePaginada,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Familias'],
)
def listar_familias_agape():
    """Lista todas as famílias Ágape com contagem de membros
    (rota antiga /listar-familias-agape).
    """
    try:
        repository = AgapeRepository(database)
        usecase = ListarFamiliasUseCase(repository)
        filtros = ListarFamiliasAgapeQueryPaginada.model_validate(
            flask_request.args.to_dict()
        )
        response = usecase.execute(filtros)
        return response, HTTPStatus.OK
    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.get('/listar-membros-familia/<uuid:familia_id>')
@swagger.validate(
    query=PaginacaoSchema,
    resp=Response(
        HTTP_200=ListarMembrosFamiliaAgapeResponsePaginada,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Familias'],
)
def listar_membros_familia_agape(familia_id):
    """Lista todas as famílias Ágape com contagem de membros
    (rota antiga /listar-membros/<fk_familia_agape_id>).
    """
    try:
        repository = AgapeRepository(database)
        usecase = ListarMembrosFamiliaUseCase(repository)
        filtros = ListarMembrosFamiliaAgapeFiltros.model_validate(
            flask_request.args.to_dict()
        )
        response = usecase.execute(
            filtros=filtros,
            familia_id=familia_id,
        )
        return response, HTTPStatus.OK
    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.get('/buscar-endereco-ciclo-acao/<uuid:ciclo_acao_id>')
@swagger.validate(
    resp=Response(
        HTTP_200=EnderecoCicloAcaoResponse,
        HTTP_404=ErroPadraoResponse,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Ações'],
)
def buscar_endereco_ciclo_acao(ciclo_acao_id):
    """Busca o endereço de um ciclo de ação ágape pelo ID do ciclo."""
    try:
        repository = AgapeRepository(database)
        use_case = BuscarEnderecoCicloAcaoUseCase(agape_repository=repository)
        response_data = use_case.execute(ciclo_acao_id=ciclo_acao_id)
        return response_data, HTTPStatus.OK
    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.get('/buscar-ultimo-ciclo-acao-agape/<uuid:nome_acao_id>')
@swagger.validate(
    resp=Response(
        HTTP_200=UltimoCicloAcaoAgapeResponse,
        HTTP_404=ErroPadraoResponse,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Ações'],
)
def buscar_ultima_acao_agape(nome_acao_id):
    """Busca o último ciclo de uma ação ágape
    (nome da ação) pelo ID do nome da ação.
    """
    try:
        repository = AgapeRepository(database)
        use_case = BuscarUltimaAcaoAgapeUseCase(agape_repository=repository)
        response_data = use_case.execute(nome_acao_id=nome_acao_id)
        return response_data, HTTPStatus.OK
    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.get(
    '/buscar-familia-agape-por-cpf/<string:cpf>/<uuid:ciclo_acao_id>'
)
@swagger.validate(
    resp=Response(
        HTTP_200=FamiliaAgapeDetalhesPorCpfResponse,
        HTTP_404=ErroPadraoResponse,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Familias'],
)
def buscar_familia_agape_por_cpf(cpf: str, ciclo_acao_id):
    """Busca os detalhes de uma família ágape pelo
    CPF do responsável e ID do ciclo de ação.
    """
    try:
        repository = AgapeRepository(database)
        file_service = file_service_factory()

        use_case = BuscarFamiliaAgapePorCpfUseCase(
            agape_repository=repository, file_service=file_service
        )
        response_data = use_case.execute(cpf=cpf, ciclo_acao_id=ciclo_acao_id)
        return response_data, HTTPStatus.OK
    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.get('/buscar-membro/<uuid:membro_agape_id>')
@swagger.validate(
    resp=Response(
        HTTP_200=MembroAgapeDetalhesResponse,
        HTTP_404=ErroPadraoResponse,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Familias'],
)
def buscar_membro_agape_por_id(membro_agape_id):
    """Busca os detalhes de um membro ágape pelo seu ID."""
    try:
        repository = AgapeRepository(database)
        file_service = file_service_factory()

        use_case = BuscarMembroAgapePorIdUseCase(
            agape_repository=repository, file_service=file_service
        )
        response_data = use_case.execute(membro_agape_id=membro_agape_id)
        return response_data, HTTPStatus.OK
    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.post('/registrar-membros/<uuid:familia_agape_id>')
@swagger.validate(
    json=MembrosAgapeCadastroRequest,  # Valida o corpo da requisição
    resp=Response(
        HTTP_201=ResponsePadraoSchema,
        HTTP_400=ErroPadraoResponse,
        HTTP_404=ErroPadraoResponse,
        HTTP_409=ErroPadraoResponse,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Familias'],
)
def registrar_membros_familia(familia_agape_id):
    """Cadastra um ou mais membros em uma família ágape existente."""
    try:
        dados_requisicao = MembrosAgapeCadastroRequest.model_validate(
            flask_request.get_json()
        )

        repository = AgapeRepository(database)
        file_service = file_service_factory()

        use_case = RegistrarMembrosFamiliaAgapeUseCase(
            agape_repository=repository, file_service=file_service
        )

        response_data = use_case.execute(
            familia_agape_id=familia_agape_id,
            dados_requisicao=dados_requisicao,
        )

        return response_data, HTTPStatus.CREATED

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.get('/card-renda-familiar-agape/<uuid:familia_id>')
@swagger.validate(
    resp=Response(
        HTTP_200=CardRendaFamiliarAgapeResponse,
        HTTP_404=ErroPadraoResponse,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Familias'],
)
def card_renda_familiar_agape(familia_id: uuid.UUID):
    """
    Retorna o card de renda familiar da família ágape pelo ID.
    """
    try:
        repository = AgapeRepository(database)
        usecase = CardRendaFamiliarAgapeUseCase(repository)

        response_data = usecase.execute(familia_id=familia_id)

        return response_data, HTTPStatus.OK

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.get('/card-total-recebimentos/<uuid:familia_id>')
@swagger.validate(
    resp=Response(
        HTTP_200=CardTotalRecebimentosAgapeResponse,
        HTTP_404=ErroPadraoResponse,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Familias'],
)
def card_total_itens_recebimentos(familia_id: uuid.UUID):
    """
    Retorna o card de itens recebidos pela família ágape pelo ID.
    """
    try:
        repository = AgapeRepository(database)
        usecase = CardTotalRecebimentosAgapeUseCase(repository)

        response_data = usecase.execute(familia_id=familia_id)

        return response_data, HTTPStatus.OK

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.get('/cards-estatisticas-familias-agape')
@swagger.validate(
    resp=Response(
        HTTP_200=CardsEstatisticasFamiliasAgapeResponse,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Familias'],
)
def cards_estatisticas_familias():
    """
    Retorna as estatisticas dos cards de famílias ágape.
    """
    try:
        repository = AgapeRepository(database)
        usecase = CardsEstatisticasFamiliasAgapeUseCase(repository)

        response_data = usecase.execute()

        return response_data, HTTPStatus.OK

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.get('/cards-estatisticas-itens-estoque')
@swagger.validate(
    resp=Response(
        HTTP_200=CardsEstatisticasItensEstoqueResponse,
        HTTP_422=ErroPadraoResponse,  # General error for unexpected issues
    ),
    tags=['Ágape - Estoque'],
)
def cards_estatisticas_itens_estoque():
    """
    Retorna as estatisticas dos cards de itens do estoque.
    """

    try:
        repository = AgapeRepository(database)
        usecase = CardsEstatisticasItensEstoqueUseCase(repository)

        response_data = usecase.execute()

        return response_data, HTTPStatus.OK

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.delete('/deletar-familia/<uuid:familia_id>')
@swagger.validate(
    resp=Response(
        HTTP_204=None,  # Sucesso, sem conteúdo
        HTTP_404=ErroPadraoResponse,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Familias'],
)
def deletar_familia(familia_id: uuid.UUID):
    """
    Deleta (soft delete) uma família ágape e seus membros (hard delete).
    """
    try:
        repository = AgapeRepository(database)
        usecase = DeletarFamiliaAgapeUseCase(repository)

        usecase.execute(familia_id=familia_id)

        return {}, HTTPStatus.NO_CONTENT

    except Exception as exc:
        database.session.rollback()  # Rollback em caso de exceção
        error_response = errors_handler(exc)
        return error_response


@agape_bp.delete('/deletar-membro/<uuid:membro_agape_id>')
@swagger.validate(
    resp=Response(
        HTTP_204=None,  # Sucesso, sem conteúdo
        HTTP_404=ErroPadraoResponse,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Familias'],
)
def deletar_membro_agape(membro_agape_id: uuid.UUID):
    """
    Deleta (hard delete) um membro ágape pelo ID.
    """
    try:
        repository = AgapeRepository(database)
        usecase = DeletarMembroAgapeUseCase(repository)

        usecase.execute(membro_agape_id=membro_agape_id)

        return {}, HTTPStatus.NO_CONTENT

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.put('/editar-endereco-familia/<uuid:familia_id>')
@swagger.validate(
    json=EditarEnderecoFamiliaAgapeRequest,  # Validação do corpo da requisição
    resp=Response(
        HTTP_200=ResponsePadraoSchema,
        HTTP_404=ErroPadraoResponse,
        HTTP_422=ErroPadraoResponse,  # For Pydantic validation errors
        HTTP_400=ErroPadraoResponse,  # For EnderecoInvalidoError
    ),
    tags=['Ágape - Familias'],
)
def editar_endereco_familia(familia_id: uuid.UUID):
    """
    Edita o endereço de uma família ágape pelo ID.
    """
    try:
        dados_request = EditarEnderecoFamiliaAgapeRequest.model_validate(
            flask_request.get_json()
        )

        repository = AgapeRepository(database)
        gmaps_service = GoogleMapsAPI()
        usecase = EditarEnderecoFamiliaAgapeUseCase(repository, gmaps_service)

        usecase.execute(familia_id=familia_id, dados_endereco=dados_request)

        return {'msg': 'Endereço atualizado com sucesso.'}, HTTPStatus.OK

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.put('/editar-membro/<uuid:membro_agape_id>')
@swagger.validate(
    form=EditarMembroAgapeFormData,
    resp=Response(
        HTTP_200=ResponsePadraoSchema,
        HTTP_404=ErroPadraoResponse,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Familias'],
)
def editar_membro_agape(membro_agape_id: uuid.UUID):
    """
    Edita um membro ágape pelo ID.
    """
    try:
        request = EditarMembroAgapeFormData.model_validate(
            flask_request.form.to_dict()
        )

        file_service = file_service_factory()

        repository = AgapeRepository(database)
        use_case = EditarMembroAgapeUseCase(repository, file_service)

        use_case.execute(membro_agape_id=membro_agape_id, dados_edicao=request)

        return {'msg': 'Membro Ágape atualizado com sucesso.'}, HTTPStatus.OK

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.get('/listar-beneficiarios/<uuid:ciclo_acao_id>')
@swagger.validate(
    resp=Response(
        HTTP_200=ListarBeneficiariosAgapeResponse,
        HTTP_404=ErroPadraoResponse,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Ações'],
)
def listar_beneficiarios_ciclo_acao(ciclo_acao_id: uuid.UUID):
    """
    Lista os beneficiários de um ciclo de ação ágape pelo ID do ciclo.
    """
    try:
        repository = AgapeRepository(database)
        use_case = ListarBeneficiariosAgapeUseCase(agape_repository=repository)

        response_data = use_case.execute(ciclo_acao_id=ciclo_acao_id)

        return response_data, HTTPStatus.OK

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.get('/listar-enderecos-familias-agape')
@swagger.validate(
    resp=Response(
        HTTP_200=ListarEnderecosFamiliasAgapeResponse,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Familias'],
)
def listar_enderecos_familias_agape():
    """
    Lista todos os endereços das famílias ágape.
    """
    try:
        repository = AgapeRepository(database)
        use_case = ListarEnderecosFamiliasAgapeUseCase(
            agape_repository=repository
        )

        response_data = use_case.execute()

        return response_data, HTTPStatus.OK

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.get(
    '/listar-geolocalizacoes-beneficiarios-ciclo-acao/<uuid:ciclo_acao_id>'
)
@swagger.validate(
    resp=Response(
        HTTP_200=ListarGeolocalizacoesBeneficiariosResponse,
        HTTP_404=ErroPadraoResponse,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Familias'],
)
def listar_geolocalizacoes_beneficiarios_ciclo_acao(ciclo_acao_id: uuid.UUID):
    try:
        repository = AgapeRepository(database)
        use_case = ListarGeolocalizacoesBeneficiariosUseCase(
            agape_repository=repository
        )

        response_data = use_case.execute(ciclo_acao_id=ciclo_acao_id)

        return response_data, HTTPStatus.OK

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.get('/listar-historico-movimentacoes')
@swagger.validate(
    query=ListarHistoricoMovimentacoesAgapeQueryPaginada,
    resp=Response(
        HTTP_200=ListarHistoricoMovimentacoesAgapeResponsePaginada,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Estoque'],
)
def listar_historico_movimentacoes_agape():
    """
    Lista o histórico de movimentações do estoque da ação ágape com paginação.
    """
    query_params = (
        ListarHistoricoMovimentacoesAgapeQueryPaginada.model_validate(
            flask_request.args.to_dict()
        )
    )

    repository = AgapeRepository(database)

    use_case = ListarHistoricoMovimentacoesAgapeUseCase(
        agape_repository=repository
    )

    response_data = use_case.execute(filtros=query_params)

    return response_data, HTTPStatus.OK


@agape_bp.get('/listar-itens-doados-beneficiario/<uuid:doacao_id>')
@swagger.validate(
    resp=Response(
        HTTP_200=ListarItensDoadosBeneficiarioResponse,
        HTTP_404=ErroPadraoResponse,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Doações'],
)
def listar_itens_doados_beneficiario(doacao_id: uuid.UUID):
    """
    Lista os itens doados para um beneficiário pelo ID da doação (DoacaoAgape).
    """
    try:
        repository = AgapeRepository(database)
        use_case = ListarItensDoadosBeneficiarioUseCase(
            agape_repository=repository
        )

        response_data = use_case.execute(doacao_id=doacao_id)

        return response_data, HTTPStatus.OK

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.get('/listar-itens-recebidos/<uuid:ciclo_acao_id>/<uuid:doacao_id>')
@swagger.validate(
    resp=Response(
        HTTP_200=ListarItensDoadosBeneficiarioResponse,
        HTTP_404=ErroPadraoResponse,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Doações'],
)
def listar_itens_recebidos(ciclo_acao_id: uuid.UUID, doacao_id: uuid.UUID):
    """
    Lista os itens recebidos por um beneficiário em um ciclo de ação específico
    """
    try:
        repository = AgapeRepository(database)
        use_case = ListarItensRecebidosUseCase(agape_repository=repository)

        response_data = use_case.execute(
            ciclo_acao_id=ciclo_acao_id, doacao_id=doacao_id
        )

        return response_data, HTTPStatus.OK

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.put('/adicionar-voluntario/<uuid:lead_id>')
@swagger.validate(
    resp=Response(
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Voluntários'],
)
def adicionar_voluntario_agape(lead_id):
    """Adiciona um voluntário ágape"""
    try:
        if (
            PerfilEnum.administrador_agape.value
            not in current_user.nomes_dos_perfis
            and PerfilEnum.voluntario_agape.value
            not in current_user.nomes_dos_perfis
        ):
            raise HttpForbiddenError(
                'Você não tem permissão para realizar esta ação.'
            )

        repository = AgapeRepository(database)

        usecase = AdicionarVoluntarioAgapeUseCase(repository)

        usecase.execute(lead_id)

        return {
            'msg': 'Voluntário adicionado com sucesso.',
        }, HTTPStatus.OK

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.get('/listar-voluntarios-agape')
@swagger.validate(
    query=PaginacaoSchema,
    resp=Response(
        HTTP_200=ListarVoluntariosAgapeResponse, HTTP_422=ErroPadraoResponse
    ),
    tags=['Ágape - Voluntários'],
)
def listar_voluntarios_agape():
    """
    Lista todos os voluntários ágape de forma paginada.
    """
    try:
        filtros = PaginacaoSchema.model_validate(flask_request.args.to_dict())

        repository = AgapeRepository(database)
        usecase = ListarVoluntariosAgapeUseCase(repository)

        response = usecase.execute(filtros)

        return response, HTTPStatus.OK

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.post('/registrar-doacao')
@swagger.validate(
    json=RegistrarDoacaoAgapeRequestSchema,
    resp=Response(
        HTTP_201=RegistrarDoacaoAgapeResponse,
        HTTP_404=ErroPadraoResponse,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Doações'],
)
def registrar_doacao_agape():
    """
    Registra uma nova doação para uma
    família em um ciclo de ação ágape específico.
    """
    try:
        request_payload = RegistrarDoacaoAgapeRequestSchema.model_validate(
            flask_request.get_json()
        )

        repository = AgapeRepository(database)
        usecase = RegistrarDoacaoAgapeUseCase(repository)

        response = usecase.execute(request_payload)

        return response, HTTPStatus.CREATED

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.delete('/remover-voluntario-agape/<uuid:lead_id>')
@swagger.validate(
    resp=Response(
        HTTP_204=None, HTTP_404=ErroPadraoResponse, HTTP_422=ErroPadraoResponse
    ),
    tags=['Ágape - Voluntários'],
)
def remover_voluntario_agape(lead_id: uuid.UUID):
    """
    Remove o perfil de voluntário ágape de um lead específico.
    """
    try:
        repository = AgapeRepository(database)
        usecase = DeletarVoluntarioAgapeUseCase(repository)

        usecase.execute(lead_id=lead_id)

        return {}, HTTPStatus.NO_CONTENT

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.put('/atualizar-permissoes-voluntarios')
@swagger.validate(
    resp=Response(
        HTTP_200=ResponsePadraoSchema,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Voluntários'],
)
def atualizar_permissoes_voluntarios():
    """
    Atualiza as permissões de múltiplos voluntários
    (leads) para o fluxo de família ágape.
    Remove permissões ágape gerenciáveis existentes
    e adiciona as novas solicitadas.
    """
    try:
        if (
            PerfilEnum.administrador_agape.value
            not in current_user.nomes_dos_perfis
            and PerfilEnum.voluntario_agape.value
            not in current_user.nomes_dos_perfis
        ):
            raise HttpForbiddenError(
                'Você não tem permissão para realizar esta ação.'
            )

        repository = AgapeRepository(database)
        AtualizarPermissoesVoluntariosUseCase(repository).execute()

        return {}, HTTPStatus.NO_CONTENT

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.get('/exportar-doacoes-beneficiados/<uuid:ciclo_acao_id>')
@swagger.validate(
    resp=Response(HTTP_200=None, HTTP_404=ErroPadraoResponse),
    tags=['Ágape - Doações'],
)
def exportar_doacoes_beneficiados(ciclo_acao_id: uuid.UUID):
    """
    Exporta os dados de doações de um
    ciclo de ação específico para um arquivo CSV.
    """
    try:
        repository = AgapeRepository(database)
        usecase = ExportarDoacoesBeneficiadosUseCase(repository)

        dados = usecase.execute(ciclo_acao_id=ciclo_acao_id)

        return dados

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.get('/exportar-familias')
@swagger.validate(
    resp=Response(HTTP_404=ErroPadraoResponse),
    tags=['Ágape - Familias'],
)
def exportar_familias_agape_route():
    """
    Exporta os dados de todas as famílias ágape ativas para um arquivo CSV.
    """

    try:
        repository = AgapeRepository(database)
        usecase = ExportarFamiliasAgapeUseCase(repository)

        dados = usecase.execute()

        return dados

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.post('/registrar-recibos-doacao-agape/<uuid:doacao_id>')
@swagger.validate(
    json=RegistrarRecibosRequestScheme,
    resp=Response(
        HTTP_201=RegistrarRecibosResponse,
        HTTP_404=ErroPadraoResponse,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Doações'],
)
def registrar_recibos_doacao_route(doacao_id: uuid.UUID):
    """
    Registra um ou mais recibos para uma doação ágape específica.
    """
    try:
        request_payload = RegistrarRecibosRequestScheme.model_validate(
            flask_request.get_json()
        )

        repository = AgapeRepository(database)
        usecase = RegistrarRecibosDoacaoAgapeUseCase(repository)

        response = usecase.execute(
            doacao_id=doacao_id, request_data=request_payload
        )

        return response, HTTPStatus.CREATED

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.get('/status-permissao-voluntarios')
@swagger.validate(
    resp=Response(
        HTTP_200=ListarStatusPermissaoVoluntariosResponse,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Voluntários'],
)
def listar_status_permissao_voluntarios_route():
    """
    Lista o status das permissões ágape para
    todos os voluntários relevantes, com paginação.
    """

    try:
        repository = AgapeRepository(database)
        usecase = ListarStatusPermissaoVoluntariosUseCase(repository)

        response = usecase.execute()

        return response, HTTPStatus.OK

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


@agape_bp.get('/listar-doacoes-recebidas/<uuid:familia_id>')
@swagger.validate(
    resp=Response(
        HTTP_200=ListarDoacoesRecebidasFamiliaResponse,
        HTTP_404=ErroPadraoResponse,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Doações'],
)
def listar_doacoes_recebidas_familia_agape(familia_id: uuid.UUID):
    """
    Retorna todas as doações recebidas pela família ágape especificada pelo ID.
    """
    try:
        repository = AgapeRepository(database)
        use_case = ListarDoacoesRecebidasFamiliaUseCase(
            agape_repository=repository
        )

        response_data = use_case.execute(familia_id=familia_id)

        return response_data, HTTPStatus.OK

    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)
