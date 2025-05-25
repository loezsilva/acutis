from acutis_api.communication.requests.admin_membros_oficiais import (
    AlterarVinculoOficialRequest,
)
from acutis_api.domain.repositories.membros_oficiais import (
    MembrosOficiaisRepositoryInterface,
)
from acutis_api.exception.errors.conflict import HttpConflictError
from acutis_api.exception.errors.not_found import HttpNotFoundError


class AlterarVinculoOficialUseCase:
    def __init__(self, repository: MembrosOficiaisRepositoryInterface):
        self.__repository = repository

    def execute(self, requisicao: AlterarVinculoOficialRequest) -> dict:
        membro_para_vincular = self.__repository.buscar_membro_oficial_por_id(
            requisicao.fk_membro_oficial_id
        )

        membro_oficial_superior = (
            self.__repository.buscar_membro_oficial_por_id(
                requisicao.fk_membro_superior_oficial_id
            )
        )

        if membro_para_vincular is None:
            raise HttpNotFoundError('Membro oficial não encontrado')

        if membro_oficial_superior is None:
            raise HttpNotFoundError('Oficial superior não encontrado')

        if requisicao.fk_membro_superior_oficial_id == (
            requisicao.fk_membro_oficial_id
        ):
            raise HttpConflictError(
                'Não é possível vincular oficial a ele mesmo'
            )

        if membro_oficial_superior.fk_cargo_oficial_id == (
            membro_para_vincular.fk_cargo_oficial_id
        ):
            raise HttpConflictError('Ambos oficiais possuem o mesmo cargo')

        self.__repository.admin_alterar_vinculo_oficial(
            membro_para_vincular, membro_oficial_superior
        )

        self.__repository.salvar_dados()
