from datetime import datetime

from acutis_api.application.use_cases.doacoes.registrar import (
    BaseRegistrarDoacaoUseCase,
)
from acutis_api.application.utils.funcoes_auxiliares import (
    calcular_data_vencimento,
    definir_tipo_documento,
)
from acutis_api.communication.requests.doacoes import (
    RegistrarDoacaoBoletoRequest,
)
from acutis_api.communication.responses.doacoes import (
    RegistrarDoacaoBoletoResponse,
)
from acutis_api.domain.entities import Campanha, Lead
from acutis_api.domain.entities.pagamento_doacao import (
    FormaPagamentoEnum,
    GatewayPagamentoEnum,
)
from acutis_api.domain.entities.processamento_doacao import (
    StatusProcessamentoEnum,
)
from acutis_api.domain.repositories.doacoes import DoacoesRepositoryInterface
from acutis_api.domain.repositories.schemas.doacoes import (
    RegistrarDoacaoSchema,
)
from acutis_api.domain.services.file_service import FileServiceInterface
from acutis_api.domain.services.gateway_pagamento import (
    GatewayPagamentoInterface,
)
from acutis_api.domain.services.schemas.gateway_pagamento import (
    CriarPagamentoBolecodeRequest,
)
from acutis_api.exception.errors.unprocessable_entity import (
    HttpUnprocessableEntityError,
)


class RegistrarDoacaoBoletoUseCase(BaseRegistrarDoacaoUseCase):
    def __init__(
        self,
        repository: DoacoesRepositoryInterface,
        itau: GatewayPagamentoInterface,
        file_service: FileServiceInterface,
    ):
        super().__init__(repository)
        self._repository = repository
        self._itau = itau
        self._file_service = file_service

    def execute(self, request: RegistrarDoacaoBoletoRequest, lead: Lead):
        self._validar_lead(lead)
        campanha = self._buscar_campanha(request.campanha_id)
        self._vincular_ou_registrar_benfeitor(lead)

        response = self._realizar_doacao(request, campanha, lead)
        self._repository.salvar_alteracoes()

        return response

    def _realizar_doacao(
        self,
        request: RegistrarDoacaoBoletoRequest,
        campanha: Campanha,
        lead: Lead,
    ):
        data_atual = datetime.today().date()
        data_vencimento = calcular_data_vencimento(data_atual)

        tipo_documento = definir_tipo_documento(lead.membro.numero_documento)
        if tipo_documento == 'identidade_estrangeira':
            raise HttpUnprocessableEntityError(
                'Você precisa ter um CPF ou CNPJ cadastrado para doar por este meio de pagamento.'  # noqa
            )

        dados_pagamento = CriarPagamentoBolecodeRequest(
            valor_doacao=request.valor_doacao,
            nome=lead.nome,
            numero_documento=lead.membro.numero_documento,
            rua=lead.membro.endereco.logradouro,
            bairro=lead.membro.endereco.bairro,
            cidade=lead.membro.endereco.cidade,
            estado=lead.membro.endereco.estado,
            cep=lead.membro.endereco.codigo_postal,
            data_vencimento=data_vencimento,
            chave_pix=campanha.campanha_doacao.chave_pix,
        )

        response, transacao_id, nosso_numero = (
            self._itau.criar_pagamento_bolecode(dados_pagamento)
        )

        dados_doacao = RegistrarDoacaoSchema(
            benfeitor_id=lead.membro.benfeitor.id,
            campanha_doacao_id=campanha.campanha_doacao.id,
            valor_doacao=request.valor_doacao,
            recorrente=False,
            forma_pagamento=FormaPagamentoEnum.boleto,
            anonimo=False,
            gateway=GatewayPagamentoEnum.itau,
            codigo_transacao=transacao_id,
            status=StatusProcessamentoEnum.pendente,
            nosso_numero=nosso_numero,
        )
        self._repository.registrar_doacao(dados_doacao)

        dado_boleto = response['dado_boleto']
        dados_boleto_individual = dado_boleto['dados_individuais_boleto'][0]
        dados_qrcode = response['dados_qrcode']
        beneficiario = response['beneficiario']

        return RegistrarDoacaoBoletoResponse(
            numero_linha_digitavel=dados_boleto_individual[
                'numero_linha_digitavel'
            ],
            qrcode=dados_qrcode['base64'],
            nome_cobranca=beneficiario['nome_cobranca'],
            nosso_numero=dados_boleto_individual['numero_nosso_numero'],
            dac_titulo=dados_boleto_individual['dac_titulo'],
            numero_documento_empresa=beneficiario['tipo_pessoa'][
                'numero_cadastro_nacional_pessoa_juridica'
            ],
            data_vencimento=dados_boleto_individual['data_vencimento'],
            valor_doacao=dados_boleto_individual['valor_titulo'],
            nome_benfeitor=dado_boleto['pagador']['pessoa']['nome_pessoa'],
            data_emissao=dado_boleto['data_emissao'],
            codigo_carteira=dado_boleto['codigo_carteira'],
            codigo_especie=dado_boleto['codigo_especie'],
            codigo_barras=dados_boleto_individual['codigo_barras'],
            msg=response['msg'],
        ).model_dump()
