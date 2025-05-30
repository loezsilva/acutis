import uuid

from acutis_api.domain.repositories.admin_doacoes import (
    AdminDoacoesRepositoryInterface,
)
from acutis_api.exception.errors.not_found import HttpNotFoundError


class ContabilizarDoacoesUseCase:
    def __init__(self, repository: AdminDoacoesRepositoryInterface):
        self.__repository = repository

    def execute(self, fk_doacao_id: uuid.UUID):
        map_contabilizar = {True: 'contabilizada', False: 'descontabilizada'}
        consulta = self.__repository.busca_doacao_por_id(fk_doacao_id)

        if consulta is None:
            raise HttpNotFoundError('Doação não encontrada')

        atualizacao = self.__repository.alterar_considerar_doacao(consulta)

        self.__repository.salvar_alteracoes()

        return {
            'msg': f'Doação {
                map_contabilizar[atualizacao.contabilizar]
            } com sucesso.'
        }
