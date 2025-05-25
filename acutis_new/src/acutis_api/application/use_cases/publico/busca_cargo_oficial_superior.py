from acutis_api.communication.responses.publico import SuperioresSchema
from acutis_api.domain.repositories.membros_oficiais import (
    MembrosOficiaisRepositoryInterface,
)
from acutis_api.exception.errors.not_found import HttpNotFoundError


class BuscaCargoSuperiorUseCase:
    def __init__(self, repository: MembrosOficiaisRepositoryInterface):
        self.repository = repository

    def execute(self, fk_cargo_oficial_id) -> dict:
        cargo_oficial = self.repository.busca_cargo_oficial_por_id(
            fk_cargo_oficial_id
        )

        if cargo_oficial is None:
            raise HttpNotFoundError('Cargo não encontrado.')

        if cargo_oficial.fk_cargo_superior_id is None:
            raise HttpNotFoundError('Cargo não possui superior.')

        membros_superiores = self.repository.busca_superiores_de_cargo_oficial(
            cargo_oficial.fk_cargo_superior_id
        )

        busca_cargo_superior = self.repository.busca_cargo_oficial_por_id(
            cargo_oficial.fk_cargo_superior_id
        )

        return {
            'superiores': [
                SuperioresSchema(nome_superior=superior.nome)
                for superior in membros_superiores
            ],
            'cargo_superior': busca_cargo_superior.nome_cargo,
            'fk_cargo_superior_id': busca_cargo_superior.id,
        }
