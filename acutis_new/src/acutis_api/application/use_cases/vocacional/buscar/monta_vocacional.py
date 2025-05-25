from acutis_api.communication.enums.vocacional import (
    PassosVocacionalEnum,
)
from acutis_api.communication.schemas.vocacional import (
    BuscaPreCadastroSchema,
    CadastroVocacionalSchema,
    FichaVocacionalResponseSchema,
)
from acutis_api.domain.repositories.vocacional import (
    InterfaceVocacionalRepository,
)
from acutis_api.domain.services.file_service import FileServiceInterface

DATE_FORMAT = '%d/%m/%Y'


class MontaVocacionalUseCase:
    def __init__(
        self,
        dados_da_consulta: tuple,
        vocacional_repository: InterfaceVocacionalRepository,
        s3_client: FileServiceInterface,
    ):
        self.__dados_da_consulta = dados_da_consulta
        self.__vocacional_repository = vocacional_repository
        self.__s3_client = s3_client

    def execute(self):
        vocacional = []

        for (
            usuario_vocacional,
            cadastro_vocacional,
            ficha_vocacional,
            etapa,
            endereco,
        ) in self.__dados_da_consulta.items:
            pre_cadastro = BuscaPreCadastroSchema(
                pais=usuario_vocacional.pais,
                id=usuario_vocacional.id,
                nome=usuario_vocacional.nome,
                genero=usuario_vocacional.genero,
                email=usuario_vocacional.email,
                telefone=usuario_vocacional.telefone,
                criado_em=usuario_vocacional.criado_em.strftime(DATE_FORMAT),
                status=self.__vocacional_repository.detalhes_da_etapa_vocacional(
                    PassosVocacionalEnum.pre_cadastro, usuario_vocacional.id
                ).status,
                responsavel_id=self.__vocacional_repository.detalhes_da_etapa_vocacional(
                    PassosVocacionalEnum.pre_cadastro, usuario_vocacional.id
                ).membro_id,
                responsavel=self.__vocacional_repository.detalhes_da_etapa_vocacional(
                    PassosVocacionalEnum.pre_cadastro, usuario_vocacional.id
                ).lead_nome,
                justificativa=self.__vocacional_repository.detalhes_da_etapa_vocacional(
                    PassosVocacionalEnum.pre_cadastro, usuario_vocacional.id
                ).justificativa,
            ).model_dump()

            if cadastro_vocacional is not None:
                cadastro = CadastroVocacionalSchema(
                    usuario_vocacional_id=usuario_vocacional.id,
                    id=cadastro_vocacional.id,
                    nome=usuario_vocacional.nome,
                    email=usuario_vocacional.email,
                    telefone=usuario_vocacional.telefone,
                    genero=usuario_vocacional.genero,
                    criado_em=(
                        cadastro_vocacional.criado_em.strftime(DATE_FORMAT)
                    ),
                    data_nascimento=(
                        cadastro_vocacional.data_nascimento.strftime(
                            DATE_FORMAT
                        )
                    ),
                    documento_identidade=(
                        cadastro_vocacional.documento_identidade
                    ),
                    logradouro=endereco.logradouro,
                    tipo_logradouro=endereco.tipo_logradouro,
                    cidade=endereco.cidade,
                    estado=endereco.estado,
                    bairro=endereco.bairro,
                    numero=endereco.numero,
                    codigo_postal=endereco.codigo_postal,
                    pais=usuario_vocacional.pais,
                    status=self.__vocacional_repository.detalhes_da_etapa_vocacional(
                        PassosVocacionalEnum.cadastro, usuario_vocacional.id
                    ).status,
                    responsavel_id=self.__vocacional_repository.detalhes_da_etapa_vocacional(
                        PassosVocacionalEnum.cadastro, usuario_vocacional.id
                    ).membro_id,
                    responsavel=self.__vocacional_repository.detalhes_da_etapa_vocacional(
                        PassosVocacionalEnum.cadastro, usuario_vocacional.id
                    ).lead_nome,
                    justificativa=self.__vocacional_repository.detalhes_da_etapa_vocacional(
                        PassosVocacionalEnum.cadastro, usuario_vocacional.id
                    ).justificativa,
                ).model_dump()
            else:
                cadastro = {}

            if ficha_vocacional is not None:
                sacramentos_list = []

                busca_sacramentos = (
                    self.__vocacional_repository.busca_sacramento_vocacional(
                        ficha_vocacional.id
                    )
                )

                for sacramento in busca_sacramentos:
                    sacramentos_list.append(sacramento.nome)

                ficha = FichaVocacionalResponseSchema(
                    motivacao_instituto=(ficha_vocacional.motivacao_instituto),
                    usuario_vocacional_id=(
                        ficha_vocacional.fk_usuario_vocacional_id
                    ),
                    motivacao_admissao_vocacional=(
                        ficha_vocacional.motivacao_admissao_vocacional
                    ),
                    referencia_conhecimento_instituto=(
                        ficha_vocacional.referencia_conhecimento_instituto
                    ),
                    identificacao_instituto=(
                        ficha_vocacional.identificacao_instituto
                    ),
                    seminario_realizado_em=(
                        ficha_vocacional.seminario_realizado_em.strftime(
                            DATE_FORMAT
                        )
                        if ficha_vocacional.seminario_realizado_em
                        else None
                    ),
                    testemunho_conversao=ficha_vocacional.testemunho_conversao,
                    escolaridade=ficha_vocacional.escolaridade,
                    profissao=ficha_vocacional.profissao,
                    cursos=ficha_vocacional.cursos,
                    rotina_diaria=ficha_vocacional.rotina_diaria,
                    aceitacao_familiar=ficha_vocacional.aceitacao_familiar,
                    estado_civil=ficha_vocacional.estado_civil,
                    motivo_divorcio=ficha_vocacional.motivo_divorcio,
                    deixou_religiao_anterior_em=(
                        ficha_vocacional.deixou_religiao_anterior_em.strftime(
                            DATE_FORMAT
                        )
                        if ficha_vocacional.deixou_religiao_anterior_em
                        else None
                    ),
                    remedio_controlado_inicio=(
                        ficha_vocacional.remedio_controlado_inicio.strftime(
                            DATE_FORMAT
                        )
                        if ficha_vocacional.remedio_controlado_inicio
                        else None
                    ),
                    remedio_controlado_termino=(
                        ficha_vocacional.remedio_controlado_termino.strftime(
                            DATE_FORMAT
                        )
                        if ficha_vocacional.remedio_controlado_termino
                        else None
                    ),
                    descricao_problema_saude=(
                        ficha_vocacional.descricao_problema_saude
                    ),
                    foto_vocacional=self.__s3_client.buscar_url_arquivo(
                        ficha_vocacional.foto_vocacional
                    ),
                    sacramentos=sacramentos_list,
                    status=(
                        self.__vocacional_repository.detalhes_da_etapa_vocacional(
                            PassosVocacionalEnum.ficha_vocacional,
                            usuario_vocacional.id,
                        ).status
                    ),
                    responsavel_id=self.__vocacional_repository.detalhes_da_etapa_vocacional(
                        PassosVocacionalEnum.ficha_vocacional,
                        usuario_vocacional.id,
                    ).membro_id,
                    responsavel=self.__vocacional_repository.detalhes_da_etapa_vocacional(
                        PassosVocacionalEnum.ficha_vocacional,
                        usuario_vocacional.id,
                    ).lead_nome,
                    justificativa=self.__vocacional_repository.detalhes_da_etapa_vocacional(
                        PassosVocacionalEnum.ficha_vocacional,
                        usuario_vocacional.id,
                    ).justificativa,
                ).model_dump()
            else:
                ficha = {}

            vocacional.append({
                'pre_cadastro': pre_cadastro,
                'cadastro_vocacional': cadastro,
                'ficha_do_vocacional': ficha,
            })

        return vocacional
