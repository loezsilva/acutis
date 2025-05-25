import re
import uuid
from abc import ABC, abstractmethod
from datetime import date, datetime
from enum import Enum

from flask import jsonify

from acutis_api.application.utils.funcoes_auxiliares import exporta_csv
from acutis_api.domain.repositories.admin_exportar_dados import (
    ExportarDadosRepositoryInterface,
)


class BaseExportarUseCase(ABC):
    def __init__(self, repository: ExportarDadosRepositoryInterface):
        self._repository = repository

    @property
    @abstractmethod
    def colunas_map(self) -> dict: ...

    @abstractmethod
    def _executar_consulta(self, colunas_para_consulta, request) -> list: ...

    @abstractmethod
    def _nome_arquivo_exportacao(self) -> str: ...

    def _formatar_coluna(self, valor, *, coluna=None):  # NOSONAR
        if valor is None:
            resultado = None
        elif isinstance(valor, uuid.UUID):
            resultado = str(valor)
        elif isinstance(valor, datetime):
            resultado = valor.strftime('%d/%m/%Y %H:%M:%S')
        elif isinstance(valor, date):
            resultado = valor.strftime('%d/%m/%Y')
        elif isinstance(valor, str):
            resultado = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', valor)
        elif isinstance(valor, Enum):
            resultado = valor.value
        else:
            resultado = valor

        return resultado

    def execute(self, request):
        colunas_para_consulta = [
            self.colunas_map[coluna] for coluna in request.colunas
        ]
        resultados = self._executar_consulta(colunas_para_consulta, request)

        dados_json = []
        for resultado in resultados:
            item = {}
            for coluna, valor in zip(request.colunas, resultado):
                if isinstance(coluna, Enum):
                    coluna = coluna.value.title().replace('_', ' ')  # noqa

                item[coluna] = self._formatar_coluna(valor)
            dados_json.append(item)

        url = (
            exporta_csv(dados_json, self._nome_arquivo_exportacao())['url']
            if dados_json
            else None
        )

        return jsonify({
            'url': url,
            'msg': f'Exportados {len(dados_json)} registros',
        })
