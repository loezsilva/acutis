from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from sqlalchemy.orm import Query

from models.agape.estoque_agape import EstoqueAgape
from models.agape.familia_agape import FamiliaAgape
from models.agape.foto_familia_agape import FotoFamiliaAgape
from models.agape.instancia_acao_agape import InstanciaAcaoAgape
from models.agape.membro_agape import MembroAgape
from models.endereco import Endereco
from models.schemas.agape.get.get_agape_action_by_id import DonationSchema
from models.schemas.agape.get.get_agape_family_by_cpf import (
    GetAgapeFamilyByCpfResponse,
)
from models.schemas.agape.get.get_agape_items_balance_history import (
    GetAgapeItemsBalanceHistoryQuery,
)
from models.schemas.agape.get.get_all_agape_actions import (
    GetAllAgapeActionsQuery,
)
from models.schemas.agape.get.get_all_agape_actions_instances import (
    GetAllAgapeActionsInstancesQuery,
)
from models.schemas.agape.get.get_all_agape_families_address import (
    AgapeFamilyAddress,
)
from models.schemas.agape.get.get_all_items_receipts import ItemReceiptSchema
from models.schemas.agape.get.get_beneficiaries_by_agape_action_id import (
    GetBeneficiariesByAgapeActionIdQuery,
)
from models.schemas.agape.get.get_beneficiary_donated_items import (
    DonatedItemSchema,
)
from models.schemas.agape.get.get_instance_beneficiaries_addresses_geolocation import (
    BeneficiariesGeolocationsSchema,
)
from repositories.schemas.agape_schemas import (
    GetAgapeFamiliesInfoSchema,
    GetSumAgapeFamiliesIncomeSchema,
    GetLastAgapeActionSchema,
    GetLastStockSupplySchema,
    GetNumberRegisteredAgapeMembersSchema,
    GetNumberStockItemsSchema,
    GetTotalDonationsReceiptsSchema,
)


class AgapeRepositoryInterface(ABC):
    @abstractmethod
    def paginate_query(
        self, query: Query, page: int, per_page: int
    ) -> Tuple[List, int]:
        pass

    @abstractmethod
    def get_all_members(self, fk_familia_agape_id: int) -> Query:
        pass

    @abstractmethod
    def get_all_families(self) -> Query:
        pass

    @abstractmethod
    def buscar_fotos_por_familia_agape_id(
        self, familia_agape_id: int
    ) -> list[FotoFamiliaAgape]: ...

    @abstractmethod
    def get_member_by_id(
        self, fk_membro_agape_id: int
    ) -> Optional[MembroAgape]:
        pass

    @abstractmethod
    def get_last_agape_action_instance(
        self, fk_acao_agape_id: int
    ) -> Optional[InstanciaAcaoAgape]:
        pass

    @abstractmethod
    def get_agape_action_instance_address(
        self, fk_instancia_acao_agape_id: int
    ) -> Endereco:
        pass

    @abstractmethod
    def get_agape_action_instance_donations(
        self, fk_instancia_acao_agape_id: int
    ) -> List[DonationSchema]:
        pass

    @abstractmethod
    def get_all_agape_action_instances(
        self, filtros: GetAllAgapeActionsInstancesQuery, perfil: str
    ) -> Query:
        pass

    @abstractmethod
    def get_all_agape_actions(self, filtros: GetAllAgapeActionsQuery) -> Query:
        pass

    @abstractmethod
    def get_agape_family_by_cpf(
        self, cpf: str, fk_instancia_acao_agape_id: int
    ) -> Optional[GetAgapeFamilyByCpfResponse]:
        pass

    @abstractmethod
    def get_agape_instance_items(
        self, fk_instancia_acao_agape_id
    ) -> List[EstoqueAgape]:
        pass

    @abstractmethod
    def get_agape_family_address_by_id(self, fk_endereco_id: int) -> Endereco:
        pass

    @abstractmethod
    def get_agape_family_by_id(
        self, fk_familia_agape_id: int
    ) -> Optional[FamiliaAgape]:
        pass

    @abstractmethod
    def get_beneficiaries_by_agape_action_instance_id(
        self,
        fk_instancia_acao_agape_id: int,
        filtros: GetBeneficiariesByAgapeActionIdQuery,
    ) -> Query:
        pass

    @abstractmethod
    def get_beneficiary_donated_items(
        self, fk_doacao_agape_id: int
    ) -> List[DonatedItemSchema]:
        pass

    @abstractmethod
    def get_agape_items_balance_history(
        self, filtros: GetAgapeItemsBalanceHistoryQuery
    ) -> Query:
        pass

    @abstractmethod
    def get_agape_action_instance_by_id(
        self, fk_instancia_acao_agape_id: int
    ) -> Optional[InstanciaAcaoAgape]:
        pass

    @abstractmethod
    def get_agape_families_info(self) -> GetAgapeFamiliesInfoSchema:
        pass

    @abstractmethod
    def get_number_registered_agape_families_members(
        self, fk_familia_agape_id: Optional[int] = None
    ) -> GetNumberRegisteredAgapeMembersSchema:
        pass

    @abstractmethod
    def get_sum_agape_families_income(
        self, fk_familia_agape_id: Optional[int] = None
    ) -> GetSumAgapeFamiliesIncomeSchema:
        pass

    @abstractmethod
    def get_number_stock_items(self) -> GetNumberStockItemsSchema:
        pass

    @abstractmethod
    def get_last_agape_action(self) -> GetLastAgapeActionSchema:
        pass

    @abstractmethod
    def get_last_stock_supply(self) -> GetLastStockSupplySchema:
        pass

    @abstractmethod
    def get_total_donations_receipts(
        self, fk_familia_agape_id: int
    ) -> GetTotalDonationsReceiptsSchema:
        pass

    @abstractmethod
    def get_all_donations_receipts(self, fk_familia_agape_id: int) -> Query:
        pass

    @abstractmethod
    def get_all_items_receipts(
        self, fk_instancia_acao_agape_id: int, fk_familia_agape_id: int
    ) -> List[ItemReceiptSchema]:
        pass

    @abstractmethod
    def get_all_agape_families_address(self) -> List[AgapeFamilyAddress]:
        pass

    @abstractmethod
    def get_instance_beneficiaries_geolocations(
        self, fk_instancia_acao_agape_id: int
    ) -> List[BeneficiariesGeolocationsSchema]:
        pass
