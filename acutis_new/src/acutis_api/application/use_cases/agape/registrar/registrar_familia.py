from flask import request as flask_request
from flask_jwt_extended import current_user

from acutis_api.application.utils.funcoes_auxiliares import (
    decodificar_base64_para_arquivo,
    valida_nome,
)
from acutis_api.communication.requests.agape import (
    RegistrarOuEditarFamiliaAgapeFormData,
)
from acutis_api.domain.repositories.agape import (
    AgapeRepositoryInterface,
)
from acutis_api.domain.repositories.schemas.agape import (
    EnderecoScheme,
    FotoFamiliaAgapeSchema,
    MembroFamiliaSchema,
    RegistrarFamiliaAgapeSchema,
)
from acutis_api.domain.services.file_service import FileServiceInterface
from acutis_api.domain.services.google_maps_service import GoogleMapsAPI
from acutis_api.exception.errors.conflict import HttpConflictError


class RegistrarFamiliaAgapeUseCase:
    def __init__(
        self,
        agape_repository: AgapeRepositoryInterface,
        gmaps: GoogleMapsAPI,
        file_service: FileServiceInterface,
    ):
        self.__repository = agape_repository
        self.__gmaps: GoogleMapsAPI = gmaps
        self.__file_service = file_service

    def execute(self, dados: RegistrarOuEditarFamiliaAgapeFormData) -> dict:
        formulario = RegistrarOuEditarFamiliaAgapeFormData(
            endereco=dados['endereco'],
            membros=dados['membros'],
            observacao=(
                dados['observacao'] if hasattr(dados, 'observacao') else None
            ),
            fotos_familia=[],
        )
        comprovante_residencia = flask_request.files.get(
            'comprovante_residencia'
        )
        dados_endereco: EnderecoScheme = formulario.endereco

        str_endereco = f"""
        {dados_endereco.rua}, {dados_endereco.numero},
        {dados_endereco.bairro}, {dados_endereco.cidade},
        {dados_endereco.estado}, {dados_endereco.cep}
        """
        endereco = self.__repository.registrar_endereco(dados_endereco)
        self.__repository.registrar_coordenada(
            endereco.id, self.__gmaps.get_geolocation(str_endereco)
        )

        responsaveis_da_familia = list(
            filter(lambda x: x.responsavel, formulario.membros)
        )

        nome_da_familia = self.gerar_nome_da_familia(
            list(map(lambda x: x.nome, responsaveis_da_familia))
        )

        familia = self.__repository.registrar_familia(
            RegistrarFamiliaAgapeSchema(
                nome_familia=nome_da_familia,
                endereco_id=endereco.id,
                observacao=formulario.observacao,
                comprovante_residencia=self.__file_service.salvar_arquivo(
                    comprovante_residencia
                )
                if comprovante_residencia
                else None,
                cadastrada_por=current_user.membro.id,
            )
        )

        fotos_familia = flask_request.files.getlist('fotos_familia')

        for foto in fotos_familia:
            self.__repository.registrar_foto_familia(
                FotoFamiliaAgapeSchema(
                    familia_id=familia.id,
                    foto=self.__file_service.salvar_arquivo(foto),
                )
            )

        for membro in formulario.membros:
            membro_cpf = membro.cpf

            if self.__repository.verficar_membro_familia_por_cpf(membro_cpf):
                raise HttpConflictError(
                    f'Membro com o cpf {membro_cpf} já cadastrado.'
                )

            elif self.__repository.verificar_membro_familia_por_email(
                membro.email
            ):
                raise HttpConflictError(
                    f'Membro com o email {membro.email} já cadastrado.'
                )

            else:
                self.__repository.registrar_membro_familia(
                    MembroFamiliaSchema(
                        familia_id=familia.id,
                        nome=membro.nome,
                        email=membro.email,
                        telefone=membro.telefone,
                        cpf=membro_cpf,
                        data_nascimento=membro.data_nascimento,
                        responsavel=membro.responsavel,
                        funcao_familiar=membro.funcao_familiar,
                        escolaridade=membro.escolaridade,
                        ocupacao=membro.ocupacao,
                        renda=membro.renda,
                        foto_documento=self.__file_service.salvar_arquivo(
                            decodificar_base64_para_arquivo(
                                membro.foto_documento
                            )
                        )
                        if membro.foto_documento
                        else None,
                        beneficiario_assistencial=membro.beneficiario_assistencial,
                    )
                )

        self.__repository.salvar_alteracoes()

        return {'msg': 'Família cadastrada com sucesso.'}

    @staticmethod
    def gerar_nome_da_familia(nomes: list[str]) -> str:
        nomes_validos = [nome for nome in nomes if valida_nome(nome)[0]]

        if not nomes_validos:
            return 'Família Sem Responsável'

        # Extração de nomes já com split seguro
        nomes_split = [nome.split() for nome in nomes_validos if nome.strip()]
        if not nomes_split:
            return 'Família Sem Responsável'

        # Nome base (primeiro nome + sobrenome em maiúsculas)
        primeiro = nomes_split[0][0]
        sobrenome = nomes_split[0][-1].upper()

        if len(nomes_split) == 1:
            return f'{primeiro} {sobrenome}'
        else:
            segundo = nomes_split[1][0]
            return f'{primeiro} e {segundo} {sobrenome}'
