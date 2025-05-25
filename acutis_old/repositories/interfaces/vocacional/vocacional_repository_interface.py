from abc import ABC, abstractmethod
from ast import Dict, List
from http import HTTPStatus
from models.schemas.vocacional.get.listar_fichas_vocacionais_schema import (
    ListarFichasVocacionaisQuery,
)
from models.schemas.vocacional.get.listar_desistencias_vocacionais_schema import (
    DesistenciaVocacionaisQuery,
)
from models.schemas.vocacional.post.registrar_cadastro_vocacional_request import (
    RegistrarCadastroVocacionalRequest,
)
from models.schemas.vocacional.post.registrar_ficha_vocacional_request import (
    FormFichaVocacionalSchema,
)
from models.schemas.vocacional.post.registrar_pre_cadastro_vocacional_request import (
    RegistrarPreCadastroRequest,
)


class InterfaceVocacionalRepository(ABC):

    @abstractmethod
    def pre_register_vocacional(
        self, data_request: RegistrarPreCadastroRequest
    ) -> tuple[Dict, HTTPStatus]:
        pass

    @abstractmethod
    def get_pre_cadastro_vocacional(
        self, data: RegistrarPreCadastroRequest
    ) -> tuple[Dict, HTTPStatus]:
        pass

    @abstractmethod
    def register_cadastro_vocacional(
        self, data: RegistrarCadastroVocacionalRequest
    ) -> tuple[Dict, HTTPStatus]:
        pass

    @abstractmethod
    def get_all_cadastro_vocacional(self, filters: list) -> tuple[Dict, HTTPStatus]:
        pass

    @abstractmethod
    def register_ficha_vocacional(
        self, data: FormFichaVocacionalSchema
    ) -> tuple[Dict, HTTPStatus]:
        pass

    @abstractmethod
    def get__all_fichas_vocacionais(
        self, filters: ListarFichasVocacionaisQuery
    ) -> tuple[Dict, HTTPStatus]:
        pass

    @abstractmethod
    def get_desistencias_vocacionais(
        self, filters: DesistenciaVocacionaisQuery, page: int, per_page: int
    ) -> tuple[Dict, HTTPStatus]:
        pass

    @abstractmethod
    def get_vocacionais_recusados(
        self, filters: DesistenciaVocacionaisQuery, page: int, per_page: int
    ) -> tuple[Dict, HTTPStatus]:
        pass

    @abstractmethod
    def register_desistencia(
        self, fk_usuario_vocacional_id: int
    ) -> tuple[Dict, HTTPStatus]:
        pass

    @abstractmethod
    def delete_vocacional(
        self, fk_usuario_vocacional_id: int
    ) -> tuple[Dict, HTTPStatus]:
        pass

    @abstractmethod
    def get_usuario_vocacional(self, usuario_vocacional_id): ...