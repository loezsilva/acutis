from datetime import datetime
from typing import Any

from acutis_api.application.utils.funcoes_auxiliares import validar_base64
from acutis_api.communication.enums.campanhas import TiposCampoEnum
from acutis_api.communication.requests.membros import CampoAdicionalSchema
from acutis_api.domain.entities.campanha import Campanha
from acutis_api.domain.entities.campo_adicional import CampoAdicional
from acutis_api.exception.errors.not_found import HttpNotFoundError
from acutis_api.exception.errors.unprocessable_entity import (
    HttpUnprocessableEntityError,
)


class CamposAdicionaisValidators:
    @staticmethod
    def verificar_campanha_valida(campanha: Campanha):
        if not campanha:
            raise HttpNotFoundError('Ops, Campanha não encontrada.')
        if not campanha.ativa:
            raise HttpUnprocessableEntityError(
                'Ops, a campanha está inativa e não pode receber cadastros.'
            )

    def validar_campos_adicionais(
        self,
        campos_recebidos: list[CampoAdicionalSchema],
        campos_campanha: list[CampoAdicional],
    ):
        ids_requeridos = {
            campo.id for campo in campos_campanha if campo.obrigatorio
        }
        ids_recebidos = {
            campo.campo_adicional_id for campo in campos_recebidos
        }
        campos_faltantes = ids_requeridos - ids_recebidos
        if campos_faltantes:
            raise HttpUnprocessableEntityError(
                'Campos obrigatórios faltantes na campanha.'
            )

        ids_validos = {campo.id for campo in campos_campanha}
        for campo in campos_recebidos:
            if campo.campo_adicional_id not in ids_validos:
                raise HttpUnprocessableEntityError('Campo adicional inválido.')

        for ca in campos_recebidos:
            campo = next(
                c for c in campos_campanha if c.id == ca.campo_adicional_id
            )
            self._validar_tipo_campo(campo, ca.valor_campo)

    def _validar_tipo_campo(self, campo: CampoAdicional, valor_campo: Any):
        tipo = campo.tipo_campo
        nome = campo.nome_campo

        match tipo:
            case TiposCampoEnum.string:
                if not isinstance(valor_campo, str):
                    raise HttpUnprocessableEntityError(
                        f'O campo "{nome}" deve ser uma string.'
                    )
            case TiposCampoEnum.integer:
                if not isinstance(valor_campo, int) and not (
                    isinstance(valor_campo, str) and valor_campo.isdigit()
                ):
                    raise HttpUnprocessableEntityError(
                        f'O campo "{nome}" deve ser um número inteiro.'
                    )
            case TiposCampoEnum.float:
                if not (
                    isinstance(valor_campo, (int, float))
                    or (
                        isinstance(valor_campo, str)
                        and self._float_valido(valor_campo)
                    )
                ):
                    raise HttpUnprocessableEntityError(
                        f'O campo "{nome}" deve ser um número decimal.'
                    )
            case TiposCampoEnum.date:
                try:
                    datetime.strptime(valor_campo, '%Y-%m-%d')
                except (ValueError, TypeError):
                    raise HttpUnprocessableEntityError(
                        f'O campo "{nome}" deve estar no formato YYYY-MM-DD.'
                    )
            case TiposCampoEnum.datetime:
                try:
                    datetime.fromisoformat(valor_campo)
                except (ValueError, TypeError):
                    raise HttpUnprocessableEntityError(
                        f'O campo "{nome}" deve estar no formato ISO 8601.'
                    )
            case TiposCampoEnum.arquivo:
                validar_base64(valor_campo)

    @staticmethod
    def _float_valido(value):
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False
