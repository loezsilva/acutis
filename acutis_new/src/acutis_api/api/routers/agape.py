import json
import logging
from datetime import date, datetime
from http import HTTPStatus

from flask import Blueprint
from flask import request as flask_request
from flask_jwt_extended import jwt_required
from spectree import Response

from acutis_api.application.use_cases.agape import (
    AbastecerItemEstoqueAgapeUseCase,
    BuscarCicloAcaoAgapeUseCase,
    BuscarItensCicloAcaoAgapeUseCase,
    DeletarCicloAcaoAgapeUseCase,
    EditarCicloAcaoAgapeUseCase,
    ExcluirItemEstoqueAgapeUseCase,
    FinalizarCicloAcaoAgapeUseCase,
    IniciarCicloAcaoAgapeUseCase,
    ListarCicloAcoesAgapeUseCase,
    ListarItensEstoqueAgapeUseCase,
    ListarNomesAcoesAgapeUseCase,
    RegistrarCicloAcaoAgapeUseCase,
    RegistrarEstoqueAgapeUseCase,
    RegistrarFamiliaAgapeUseCase,
    RegistrarNomeAcaoAgapeUseCase,
    RemoverItemEstoqueAgapeUseCase,
    ListarFamiliasUseCase,
    ListarMembrosFamiliaUseCase,
    AdicionarVoluntarioAgapeUseCase,
    BuscarEnderecoFamiliaAgapeUseCase,
    BuscarEnderecoCicloAcaoUseCase,
)
from acutis_api.application.utils.funcoes_auxiliares import (
    transforma_string_para_data,
)
from acutis_api.communication.requests.agape import (
    AbastecerItemEstoqueAgapeFormData,
    ListarCiclosAcoesAgapeQueryPaginada,
    ListarItensEstoqueAgapeQueryPaginada,
    ListarNomesAcoesAgapeQueryPaginada,
    RegistrarItemEstoqueAgapeFormData,
    RegistrarNomeAcaoAgapeFormData,
    RegistrarOuEditarCicloAcaoAgapeFormData,
    RegistrarOuEditarFamiliaAgapeFormData,
    RemoverItemEstoqueAgapeFormData,
    ListarFamiliasAgapeQueryPaginada,
    AdicionarVoluntarioAgapeFormData,
)
from acutis_api.communication.responses.agape import (
    BuscarCicloAcaoAgapeResponse,
    BuscarItensCicloAcaoAgapeResponse,
    ItemEstoqueAgapeResponse,
    ListarCiclosAcoesAgapeResponsePaginada,
    ListarItensEstoqueAgapeResponsePaginada,
    ListarNomesAcoesAgapeResponsePaginada,
    RegistrarAcaoAgapeResponse,
    RegistrarItemEstoqueAgapeResponse,
    ListarFamiliasAgapeResponsePaginada,
    EnderecoResponse,
    EnderecoCicloAcaoResponse,
)
from acutis_api.domain.repositories.schemas.agape import (
    ListarMembrosFamiliaAgapeFiltros
)

from acutis_api.communication.responses.padrao import (
    ErroPadraoResponse,
    ResponsePadraoSchema,
)
from acutis_api.domain.services.google_maps_service import GoogleMapsAPI
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
    pass

def parse_datas_padrao_brasileiro(obj):
    if isinstance(obj, list):
        return [parse_datas_padrao_brasileiro(item) for item in obj]
    elif isinstance(obj, dict):
        new_obj = {}
        for key, value in obj.items():
            if isinstance(value, datetime):
                new_obj[key] = value.strftime('%d/%m/%Y %H:%M')
            elif isinstance(value, date):
                new_obj[key] = value.strftime('%d/%m/%Y')
            elif isinstance(value, str):
                parsed = transforma_string_para_data(value)
                if parsed:
                    new_obj[key] = parsed.strftime('%d/%m/%Y %H:%M')
                else:
                    new_obj[key] = value
            elif isinstance(value, (list, dict)):
                new_obj[key] = parse_datas_padrao_brasileiro(value)
            else:
                new_obj[key] = value
        return new_obj
    else:
        return obj


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
    form=RegistrarNomeAcaoAgapeFormData,
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
        form = flask_request.form
        request = RegistrarNomeAcaoAgapeFormData(
            nome=form['nome'],
        )

        repository = AgapeRepository(database)
        usecase = RegistrarNomeAcaoAgapeUseCase(repository)
        response = usecase.execute(request)
        return response, HTTPStatus.CREATED

    except Exception as exc:
        database.session.rollback()
        error_response = errors_handler(exc)
        return error_response


@agape_bp.get('/buscar-endereco-familia/<uuid:familia_id>')
@swagger.validate(
    resp=Response(
        HTTP_200=EnderecoResponse,
        HTTP_404=ErroPadraoResponse,
        HTTP_422=ErroPadraoResponse
    ),
    tags=['Ágape - Familias'],
)
def buscar_endereco_familia(familia_id: UUID):
    '''Busca o endereço de uma família ágape pelo ID da família.'''
    try:
        repository = AgapeRepository(database)
        use_case = BuscarEnderecoFamiliaAgapeUseCase(agape_repository=repository)
        endereco_response = use_case.execute(familia_id=familia_id)
        return endereco_response, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response


@agape_bp.get('/buscar-endereco-ciclo-acao/<uuid:ciclo_acao_id>')
@swagger.validate(
    resp=Response(
        HTTP_200=EnderecoCicloAcaoResponse, 
        HTTP_404=ErroPadraoResponse, 
        HTTP_422=ErroPadraoResponse 
    ),
    tags=['Ágape - Ações'], 
)
def buscar_endereco_ciclo_acao(ciclo_acao_id: UUID):
    '''Busca o endereço de um ciclo de ação ágape pelo ID do ciclo.'''
    try:
        repository = AgapeRepository(database) 
        use_case = BuscarEnderecoCicloAcaoUseCase(agape_repository=repository)
        response_data = use_case.execute(ciclo_acao_id=ciclo_acao_id)
        return response_data, HTTPStatus.OK
    except Exception as exc:
        error_response = errors_handler(exc)
        return error_response

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
        error_response = errors_handler(exc)
        return error_response


# FIM DAS ROTAS DE NOME DE AÇÕES


# INICIA AS ROTAS PARA ESTOQUE
@agape_bp.post('/registrar-item')
@swagger.validate(
    form=RegistrarItemEstoqueAgapeFormData,
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
        form = flask_request.form
        request = RegistrarItemEstoqueAgapeFormData(
            item=form['item'],
            quantidade=form['quantidade'],
        )

        repository = AgapeRepository(database)
        usecase = RegistrarEstoqueAgapeUseCase(repository)
        response = usecase.execute(request)
        return response, HTTPStatus.CREATED

    except Exception as exc:
        database.session.rollback()
        error_response = errors_handler(exc)
        return error_response


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
        error_response = errors_handler(exc)
        return error_response


@agape_bp.put('/abastecer-item/<uuid:item_id>')
@swagger.validate(
    form=AbastecerItemEstoqueAgapeFormData,
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
        form = flask_request.form
        quantidade = int(form['quantidade'])

        repository = AgapeRepository(database)
        usecase = AbastecerItemEstoqueAgapeUseCase(repository)
        response = usecase.execute(item_id, quantidade)
        return response, HTTPStatus.OK
    except Exception as exc:
        database.session.rollback()
        error_response = errors_handler(exc)
        return error_response


# Essa rota não está na lista de rotas da versão antiga.
@agape_bp.put('/remover-item/<uuid:item_id>')
@swagger.validate(
    form=RemoverItemEstoqueAgapeFormData,
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
        form = flask_request.form

        quantidade = int(form['quantidade'])

        repository = AgapeRepository(database)
        usecase = RemoverItemEstoqueAgapeUseCase(repository)
        response = usecase.execute(item_id, quantidade)
        return response, HTTPStatus.OK
    except Exception as exc:
        database.session.rollback()
        error_response = errors_handler(exc)
        return error_response


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
        response = usecase.execute(item_id)
        return response, HTTPStatus.NO_CONTENT
    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


# FIM DAS ROTAS DE ESTOQUE


# ROTAS PARA CICLO DE AÇÕES ÁGAPE
# Rota para registrar ciclo de ação Ágape completo
@agape_bp.post('/registrar-ciclo-acao')
@swagger.validate(
    json=RegistrarOuEditarCicloAcaoAgapeFormData,
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
        json_data = flask_request.get_json()
        form = RegistrarOuEditarCicloAcaoAgapeFormData.model_validate(
            json_data
        )

        repository = AgapeRepository(database)
        gmaps = GoogleMapsAPI()

        usecase = RegistrarCicloAcaoAgapeUseCase(repository, gmaps)

        body, status = usecase.execute(dados=form)
        return body, status
    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)


# Rota para editar ciclo de ação Ágape
@agape_bp.put('/editar-ciclo-acao/<uuid:acao_agape_id>')
@swagger.validate(
    json=RegistrarOuEditarCicloAcaoAgapeFormData,
    resp=Response(HTTP_200=ResponsePadraoSchema, HTTP_422=ErroPadraoResponse),
    tags=['Ágape - Ações'],
)
def editar_ciclo_acao_agape(acao_agape_id):
    """Edita um ciclo de ação Ágape não iniciado"""
    try:
        json_data = flask_request.get_json()
        form = RegistrarOuEditarCicloAcaoAgapeFormData.model_validate(
            json_data
        )

        repository = AgapeRepository(database)
        gmaps = GoogleMapsAPI()

        usecase = EditarCicloAcaoAgapeUseCase(repository, gmaps)

        body, status = usecase.execute(acao_agape_id, dados=form)

        return body, status

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

        response = usecase.execute(acao_agape_id)
        return response, HTTPStatus.OK
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

        response = usecase.execute(acao_agape_id)
        return response, HTTPStatus.OK
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

        response = usecase.execute(acao_agape_id)
        return response, HTTPStatus.NO_CONTENT
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
    query=ListarMembrosFamiliaAgapeFiltros,
    resp=Response(
        HTTP_200=ListarMembrosFamiliaAgapeFiltros,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Familias'],
)
def listar_membros_familia_agape():
    """Lista todas as famílias Ágape com contagem de membros
    
    (rota antiga /listar-membros/<fk_familia_agape_id>).
    """
    try:
        repository = AgapeRepository(database)
        usecase = ListarMembrosFamiliaUseCase(repository)
        filtros = ListarMembrosFamiliaAgapeFiltros.model_validate(
            flask_request.args.to_dict()
        )
        response = usecase.execute(filtros)
        return response, HTTPStatus.OK
    except Exception as exc:
        database.session.rollback()
        return errors_handler(exc)
    

@agape_bp.put('/adicionar-voluntario/<uuid:lead_id>')
@swagger.validate(
    form=AdicionarVoluntarioAgapeFormData,
    resp=Response(
        HTTP_204=None,
        HTTP_422=ErroPadraoResponse,
    ),
    tags=['Ágape - Familias'],
)
def adicionar_voluntario_agape(lead_id):
    """
    Adiciona um voluntário a uma família Ágape existente.
    """
    try:
        repository = AgapeRepository(database)
        usecase = AdicionarVoluntarioAgapeUseCase(repository)
        response = usecase.execute(lead_id)
        return response, HTTPStatus.OK
    except Exception as exc:
        database.session.rollback()
        error_response = errors_handler(exc)
        return error_response