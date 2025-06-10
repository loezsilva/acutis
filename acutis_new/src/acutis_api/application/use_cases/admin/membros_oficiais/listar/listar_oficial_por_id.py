from acutis_api.application.utils.funcoes_auxiliares import (
    tratar_valor_campo_por_tipo_valor,
)
from acutis_api.communication.responses.admin_membros import (
    CampanhasRegistradasSchema,
)
from acutis_api.communication.responses.admin_membros_oficiais import (
    MembrosOficiaisResponse,
)
from acutis_api.domain.repositories.membros_oficiais import (
    MembrosOficiaisRepositoryInterface,
)
from acutis_api.domain.services.file_service import FileServiceInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class ListarMembroOficialPorIdUseCase:
    def __init__(
        self,
        repository: MembrosOficiaisRepositoryInterface,
        file_service: FileServiceInterface,
    ):
        self.__repository = repository
        self._file_service = file_service

    def execute(self, membro_oficial_id: str) -> MembrosOficiaisResponse:
        campanhas_registradas = []

        membro_oficial = self.__repository.admin_listar_membro_oficial_por_id(
            membro_oficial_id
        )
        if not membro_oficial:
            raise HttpNotFoundError('Membro oficial não encontrado.')
        (
            lead,
            membro,
            endereco,
            oficial,
            cargo_oficial,
            nome_superior,
        ) = membro_oficial

        if lead.metadados:
            for metadado in lead.metadados:
                nome_campanha = metadado.campo_adicional.campanha.nome
                nome_campo = metadado.campo_adicional.nome_campo
                tipo_campo = metadado.campo_adicional.tipo_campo
                valor_campo = tratar_valor_campo_por_tipo_valor(
                    self, metadado.valor_campo, tipo_campo
                )

                campanha_existente = next(
                    (
                        campanha
                        for campanha in campanhas_registradas
                        if campanha['nome'] == nome_campanha
                    ),
                    None,
                )

                if campanha_existente:
                    campanha_existente['campos_adicionais'].append({
                        'nome_campo': nome_campo,
                        'valor_campo': valor_campo,
                    })
                else:
                    nova_campanha = {
                        'nome': nome_campanha,
                        'campos_adicionais': [
                            {
                                'nome_campo': nome_campo,
                                'valor_campo': valor_campo,
                            }
                        ],
                    }
                    campanhas_registradas.append(nova_campanha)

        campanhas_registradas = [
            CampanhasRegistradasSchema.model_validate(campanha).model_dump()
            for campanha in campanhas_registradas
        ]

        response = MembrosOficiaisResponse(
            id=str(oficial.id),
            nome=lead.nome,
            email=lead.email,
            cargo_oficial=(
                cargo_oficial
                if (oficial.fk_cargo_oficial_id) is not None
                else None
            ),
            criado_em=oficial.criado_em.strftime('%d/%m/%y %H:%M:%S'),
            numero_documento=membro.numero_documento,
            sexo=membro.sexo,
            status=oficial.status,
            superior=(nome_superior if oficial.fk_superior_id else None),
            foto=(
                self._file_service.buscar_url_arquivo(membro.foto)
                if membro.foto
                else None
            ),
            logradouro=endereco.logradouro,
            numero=endereco.numero,
            bairro=endereco.bairro,
            codigo_postal=endereco.codigo_postal,
            cidade=endereco.cidade,
            complemento=endereco.complemento,
            pais=endereco.pais,
            campanhas_registradas=campanhas_registradas,
        )

        return response
