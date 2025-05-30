from acutis_api.communication.requests.admin_membros_oficiais import (
    ListarMembrosOficiaisRequest,
)
from acutis_api.communication.responses.admin_membros_oficiais import (
    ListarMembrosOficiaisResponse,
    MembrosOficiaisResponse,
)
from acutis_api.domain.repositories.membros_oficiais import (
    MembrosOficiaisRepositoryInterface,
)
from acutis_api.domain.services.file_service import FileServiceInterface


class ListarMembrosOficiaisUseCase:
    def __init__(
        self,
        repository: MembrosOficiaisRepositoryInterface,
        file_service: FileServiceInterface,
    ):
        self.__repository = repository
        self._file_service = file_service

    def execute(
        self, filtros_da_requisicao: ListarMembrosOficiaisRequest
    ) -> ListarMembrosOficiaisResponse:
        membros_oficiais = self.__repository.admin_listar_membros_oficiais(
            filtros_da_requisicao
        )

        response = ListarMembrosOficiaisResponse(
            total=membros_oficiais.total,
            pagina=membros_oficiais.page,
            por_pagina=membros_oficiais.per_page,
            membros_oficiais=[
                MembrosOficiaisResponse(
                    id=str(oficial.id),
                    nome=lead.nome,
                    email=lead.email,
                    cargo_oficial=(
                        cargo_oficial
                        if oficial.fk_cargo_oficial_id is not None
                        else None
                    ),
                    criado_em=oficial.criado_em.strftime('%d/%m/%y %H:%M:%S'),
                    numero_documento=membro.numero_documento,
                    sexo=membro.sexo,
                    status=oficial.status,
                    superior=(
                        nome_superior
                        if oficial.fk_superior_id is not None
                        else None
                    ),
                    foto=(
                        self._file_service.buscar_url_arquivo(membro.foto)
                        if membro.foto is not None
                        else None
                    ),
                    logradouro=endereco.logradouro,
                    numero=endereco.numero,
                    bairro=endereco.bairro,
                    codigo_postal=endereco.codigo_postal,
                    cidade=endereco.cidade,
                    complemento=endereco.complemento,
                    pais=endereco.pais,
                )
                for (
                    lead,
                    membro,
                    endereco,
                    oficial,
                    cargo_oficial,
                    nome_superior,
                ) in membros_oficiais.items
            ],
        )

        return response
