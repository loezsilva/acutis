import uuid
from abc import ABC

from acutis_api.domain.entities import Campanha, Lead
from acutis_api.domain.repositories.doacoes import DoacoesRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError
from acutis_api.exception.errors.unprocessable_entity import (
    HttpUnprocessableEntityError,
)


class BaseRegistrarDoacaoUseCase(ABC):
    def __init__(self, repository: DoacoesRepositoryInterface):
        self._repository = repository

    def _validar_lead(self, lead: Lead):
        if not lead.membro or not lead.membro.numero_documento:
            raise HttpUnprocessableEntityError(
                'Complete seu cadastro para realizar uma doação.'
            )

    def _buscar_campanha(self, campanha_id: uuid.UUID) -> Campanha:
        campanha = self._repository.buscar_campanha_por_id(campanha_id)
        if not campanha:
            raise HttpNotFoundError('Campanha não encontrada.')

        if not campanha.ativa or not campanha.campanha_doacao:
            raise HttpUnprocessableEntityError(
                'Doações para essa campanha estão indisponíveis no momento.'
            )

        return campanha

    def _vincular_ou_registrar_benfeitor(self, lead: Lead):
        if not lead.membro.benfeitor:
            benfeitor = self._repository.buscar_benfeitor_por_numero_documento(
                lead.membro.numero_documento
            )
            if not benfeitor:
                self._repository.registrar_membro_benfeitor(
                    lead.membro, lead.membro.numero_documento, lead.nome
                )
            else:
                self._repository.vincular_membro_benfeitor(
                    lead.membro, benfeitor
                )
