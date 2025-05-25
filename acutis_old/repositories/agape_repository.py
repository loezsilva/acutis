from typing import List, Optional, Tuple
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date, between, cast, func, case, literal_column, or_
from sqlalchemy.orm import Query

from exceptions.error_types.http_not_found import NotFoundError
from models.agape.acao_agape import AcaoAgape, PerfisAgape
from models.agape.aquisicao_agape import AquisicaoAgape
from models.agape.doacao_agape import DoacaoAgape
from models.agape.estoque_agape import EstoqueAgape
from models.agape.familia_agape import FamiliaAgape
from models.agape.foto_familia_agape import FotoFamiliaAgape
from models.agape.historico_movimentacao_agape import (
    HistoricoMovimentacaoAgape,
)
from models.agape.instancia_acao_agape import (
    InstanciaAcaoAgape,
    StatusAcaoAgapeEnum,
)
from models.agape.item_doacao_agape import ItemDoacaoAgape
from models.agape.item_instancia_agape import ItemInstanciaAgape
from models.agape.membro_agape import MembroAgape
from models.agape.recibo_agape import ReciboAgape
from models.endereco import Endereco
from models.menu_sistema import MenuSistema
from models.perfil import Perfil, ProfilesEnum
from models.permissao_menu import PermissaoMenu
from models.permissao_usuario import PermissaoUsuario
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
    ReceiptsEnum,
)
from models.schemas.agape.get.get_beneficiary_donated_items import (
    DonatedItemSchema,
)
from models.schemas.agape.get.get_instance_beneficiaries_addresses_geolocation import (
    BeneficiariesGeolocationsSchema,
)
from models.schemas.default import PaginationQuery
from models.usuario import Usuario
from repositories.interfaces.agape_repository_interface import (
    AgapeRepositoryInterface,
)
from repositories.schemas.agape_schemas import (
    GetAgapeFamiliesInfoSchema,
    GetLastAgapeActionSchema,
    GetLastStockSupplySchema,
    GetNumberRegisteredAgapeMembersSchema,
    GetNumberStockItemsSchema,
    GetSumAgapeFamiliesIncomeSchema,
    GetTotalDonationsReceiptsSchema,
)
from utils.regex import format_string


class AgapeRepository(AgapeRepositoryInterface):
    def __init__(self, database: SQLAlchemy):
        self.__database = database

    def paginate_query(
        self, query: Query, page: int, per_page: int
    ) -> Tuple[List, int]:
        query_pagination = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        items, total = query_pagination.items, query_pagination.total
        return items, total

    def get_all_members(self, fk_familia_agape_id: int) -> Query:
        membros_query = (
            self.__database.session.query(MembroAgape)
            .filter(MembroAgape.fk_familia_agape_id == fk_familia_agape_id)
            .order_by(MembroAgape.responsavel.desc(), MembroAgape.nome)
        )

        return membros_query

    def get_all_families(self) -> Query:
        sub_membros = (
            self.__database.session.query(
                MembroAgape.fk_familia_agape_id,
                func.count(MembroAgape.id).label("membros"),
                func.sum(MembroAgape.renda).label("renda"),
            )
            .group_by(MembroAgape.fk_familia_agape_id)
            .subquery()
        )

        sub_recebimentos = (
            self.__database.session.query(
                DoacaoAgape.fk_familia_agape_id,
                func.count(DoacaoAgape.id).label("recebimentos"),
                func.format(
                    func.max(DoacaoAgape.created_at), "dd/MM/yyyy"
                ).label("ultimo_recebimento"),
            )
            .group_by(DoacaoAgape.fk_familia_agape_id)
            .subquery()
        )

        familias_query = (
            self.__database.session.query(
                FamiliaAgape.id,
                FamiliaAgape.nome_familia.label("familia"),
                FamiliaAgape.comprovante_residencia,
                FamiliaAgape.observacao,
                func.format(FamiliaAgape.created_at, "dd/MM/yyyy").label(
                    "cadastrado_em"
                ),
                sub_membros.c.membros.label("membros"),
                sub_membros.c.renda.label("renda"),
                func.coalesce(sub_recebimentos.c.recebimentos, 0).label(
                    "recebimentos"
                ),
                sub_recebimentos.c.ultimo_recebimento.label(
                    "ultimo_recebimento"
                ),
                Endereco.id.label("fk_endereco_id"),
                Usuario.nome.label("cadastrada_por"),
            )
            .join(Endereco, Endereco.id == FamiliaAgape.fk_endereco_id)
            .join(Usuario, FamiliaAgape.cadastrada_por == Usuario.id)
            .join(
                sub_membros,
                FamiliaAgape.id == sub_membros.c.fk_familia_agape_id,
            )
            .outerjoin(
                sub_recebimentos,
                FamiliaAgape.id == sub_recebimentos.c.fk_familia_agape_id,
            )
            .filter(
                FamiliaAgape.deleted_at.is_(None), FamiliaAgape.status == True
            )
            .order_by(FamiliaAgape.id)
        )

        return familias_query

    def buscar_fotos_por_familia_agape_id(
        self, familia_agape_id: int
    ) -> list[FotoFamiliaAgape]:
        fotos_familia_agape = FotoFamiliaAgape.query.filter_by(
            fk_familia_agape_id=familia_agape_id
        ).all()

        return fotos_familia_agape

    def get_member_by_id(
        self, fk_membro_agape_id: int
    ) -> Optional[MembroAgape]:
        membro = self.__database.session.query(
            MembroAgape.id,
            MembroAgape.responsavel,
            MembroAgape.nome,
            MembroAgape.email,
            MembroAgape.telefone,
            MembroAgape.cpf,
            func.format(MembroAgape.data_nascimento, "dd/MM/yyyy").label(
                "data_nascimento"
            ),
            MembroAgape.funcao_familiar,
            MembroAgape.escolaridade,
            MembroAgape.ocupacao,
            MembroAgape.renda,
            MembroAgape.foto_documento,
            MembroAgape.beneficiario_assistencial,
        ).filter_by(id=fk_membro_agape_id)

        membro = membro.first()
        return membro

    def get_last_agape_action_instance(
        self, fk_acao_agape_id: int
    ) -> Optional[InstanciaAcaoAgape]:
        ultima_instancia = InstanciaAcaoAgape.query.filter_by(
            fk_acao_agape_id=fk_acao_agape_id
        ).order_by(InstanciaAcaoAgape.created_at.desc())

        ultima_instancia = ultima_instancia.first()

        return ultima_instancia

    def get_agape_action_instance_address(
        self, fk_instancia_acao_agape_id: int
    ) -> Endereco:
        endereco = Endereco.query.join(
            InstanciaAcaoAgape,
            Endereco.id == InstanciaAcaoAgape.fk_endereco_id,
        ).filter(InstanciaAcaoAgape.id == fk_instancia_acao_agape_id)

        endereco = endereco.first()

        return endereco

    def get_agape_action_instance_donations(
        self, fk_instancia_acao_agape_id: int
    ) -> List[DonationSchema]:
        doacoes = (
            self.__database.session.query(
                EstoqueAgape.id.label("fk_estoque_agape_id"),
                EstoqueAgape.item,
                ItemInstanciaAgape.quantidade,
                ItemInstanciaAgape.id.label("fk_item_instancia_agape_id"),
            )
            .select_from(InstanciaAcaoAgape)
            .join(
                ItemInstanciaAgape,
                InstanciaAcaoAgape.id
                == ItemInstanciaAgape.fk_instancia_acao_agape_id,
            )
            .join(
                EstoqueAgape,
                EstoqueAgape.id == ItemInstanciaAgape.fk_estoque_agape_id,
            )
            .filter(
                ItemInstanciaAgape.fk_instancia_acao_agape_id
                == fk_instancia_acao_agape_id
            )
        )

        doacoes = doacoes.all()

        return doacoes

    def get_all_agape_action_instances(
        self, filtros: GetAllAgapeActionsInstancesQuery, perfil: str
    ) -> Query:
        prioridade_ordenacao = case(
            (InstanciaAcaoAgape.status == StatusAcaoAgapeEnum.em_andamento, 1),
            (InstanciaAcaoAgape.status == StatusAcaoAgapeEnum.nao_iniciado, 2),
            (InstanciaAcaoAgape.status == StatusAcaoAgapeEnum.finalizado, 3),
            else_=4,
        )

        instancias_query = (
            self.__database.session.query(
                InstanciaAcaoAgape.id,
                InstanciaAcaoAgape.status,
                AcaoAgape.nome.label("nome_acao_agape"),
            )
            .join(
                AcaoAgape, AcaoAgape.id == InstanciaAcaoAgape.fk_acao_agape_id
            )
            .order_by(prioridade_ordenacao, AcaoAgape.nome)
        )
        if perfil == PerfisAgape.Voluntario:
            instancias_query = instancias_query.filter(
                InstanciaAcaoAgape.status == StatusAcaoAgapeEnum.em_andamento
            )
        elif filtros.status:
            instancias_query = instancias_query.filter(
                InstanciaAcaoAgape.status == filtros.status
            )

        if filtros.fk_acao_agape_id:
            instancias_query = instancias_query.filter(
                InstanciaAcaoAgape.fk_acao_agape_id == filtros.fk_acao_agape_id
            )

        return instancias_query

    def get_all_agape_actions(self, filtros: GetAllAgapeActionsQuery) -> Query:
        acoes_agape_query = (
            self.__database.session.query(
                AcaoAgape.id,
                AcaoAgape.nome,
                func.format(AcaoAgape.created_at, "dd/MM/yyyy").label(
                    "data_cadastro"
                ),
                func.count(
                    case(
                        (
                            InstanciaAcaoAgape.status
                            == StatusAcaoAgapeEnum.finalizado,
                            InstanciaAcaoAgape.id,
                        ),
                        else_=None,
                    )
                ).label("ciclos_finalizados"),
            )
            .outerjoin(
                InstanciaAcaoAgape,
                AcaoAgape.id == InstanciaAcaoAgape.fk_acao_agape_id,
            )
            .group_by(AcaoAgape.id, AcaoAgape.nome, AcaoAgape.created_at)
            .order_by(AcaoAgape.created_at.desc(), AcaoAgape.nome)
        )

        if filtros.fk_acao_agape_id:
            acoes_agape_query = acoes_agape_query.filter(
                AcaoAgape.id == filtros.fk_acao_agape_id
            )
        if filtros.data_cadastro_inicial:
            acoes_agape_query = acoes_agape_query.filter(
                between(
                    cast(AcaoAgape.created_at, Date),
                    filtros.data_cadastro_inicial,
                    filtros.data_cadastro_final,
                )
            )

        return acoes_agape_query

    def get_agape_family_by_cpf(
        self, cpf: str, fk_instancia_acao_agape_id: int
    ) -> Optional[GetAgapeFamilyByCpfResponse]:
        familia_query = (
            self.__database.session.query(
                FamiliaAgape.id,
                FamiliaAgape.nome_familia,
                FamiliaAgape.observacao,
                FamiliaAgape.comprovante_residencia,
                func.format(FamiliaAgape.created_at, "dd/MM/yyyy").label(
                    "cadastrado_em"
                ),
                FamiliaAgape.status,
                func.format(
                    func.max(
                        case(
                            (
                                InstanciaAcaoAgape.id
                                == fk_instancia_acao_agape_id,
                                DoacaoAgape.created_at,
                            ),
                            else_=None,
                        )
                    ),
                    "dd/MM/yyyy",
                ).label("ultimo_recebimento"),
                FamiliaAgape.fk_endereco_id,
            )
            .select_from(MembroAgape)
            .join(
                FamiliaAgape,
                FamiliaAgape.id == MembroAgape.fk_familia_agape_id,
            )
            .outerjoin(
                DoacaoAgape, FamiliaAgape.id == DoacaoAgape.fk_familia_agape_id
            )
            .outerjoin(
                ItemDoacaoAgape,
                DoacaoAgape.id == ItemDoacaoAgape.fk_doacao_agape_id,
            )
            .outerjoin(
                ItemInstanciaAgape,
                ItemInstanciaAgape.id
                == ItemDoacaoAgape.fk_item_instancia_agape_id,
            )
            .outerjoin(
                InstanciaAcaoAgape,
                InstanciaAcaoAgape.id
                == ItemInstanciaAgape.fk_instancia_acao_agape_id,
            )
            .group_by(
                FamiliaAgape.id,
                FamiliaAgape.nome_familia,
                FamiliaAgape.observacao,
                FamiliaAgape.comprovante_residencia,
                FamiliaAgape.created_at,
                FamiliaAgape.status,
                FamiliaAgape.fk_endereco_id,
            )
            .filter(
                FamiliaAgape.deleted_at.is_(None),
                MembroAgape.cpf == cpf,
            )
        )

        familia = familia_query.first()
        return familia

    def get_agape_instance_items(
        self, fk_instancia_acao_agape_id
    ) -> List[EstoqueAgape]:
        itens_query = (
            self.__database.session.query(
                ItemInstanciaAgape.id.label("fk_item_instancia_agape_id"),
                ItemInstanciaAgape.quantidade,
                EstoqueAgape.item,
            )
            .select_from(InstanciaAcaoAgape)
            .join(
                ItemInstanciaAgape,
                InstanciaAcaoAgape.id
                == ItemInstanciaAgape.fk_instancia_acao_agape_id,
            )
            .join(
                EstoqueAgape,
                EstoqueAgape.id == ItemInstanciaAgape.fk_estoque_agape_id,
            )
            .filter(
                InstanciaAcaoAgape.id == fk_instancia_acao_agape_id,
                ItemInstanciaAgape.quantidade > 0,
            )
            .order_by(EstoqueAgape.item, EstoqueAgape.id)
        )

        itens = itens_query.all()
        return itens

    def get_agape_family_address_by_id(self, fk_endereco_id: int) -> Endereco:
        endereco = self.__database.session.get(Endereco, fk_endereco_id)
        return endereco

    def get_agape_family_by_id(
        self, fk_familia_agape_id: int
    ) -> Optional[FamiliaAgape]:
        familia = self.__database.session.get(
            FamiliaAgape, fk_familia_agape_id
        )
        return familia

    def get_beneficiaries_by_agape_action_instance_id(
        self,
        fk_instancia_acao_agape_id: int,
        filtros: GetBeneficiariesByAgapeActionIdQuery,
    ) -> Query:
        subquery_recibos = (
            self.__database.session.query(
                ReciboAgape.fk_doacao_agape_id.label("fk_doacao_agape_id"),
                func.string_agg(
                    ReciboAgape.recibo, literal_column("','")
                ).label("recibos"),
            ).group_by(ReciboAgape.fk_doacao_agape_id)
        ).subquery("subquery_recibos")

        beneficiarios_query = (
            self.__database.session.query(
                DoacaoAgape.id.label("fk_doacao_agape_id"),
                FamiliaAgape.nome_familia.label("nome_familia"),
                func.format(
                    DoacaoAgape.created_at.label("data_hora_doacao"),
                    "dd/MM/yyyy HH:mm",
                ).label("data_hora_doacao"),
                func.coalesce(subquery_recibos.c.recibos, "").label("recibos"),
            )
            .join(
                MembroAgape, FamiliaAgape.id == MembroAgape.fk_familia_agape_id
            )
            .join(
                DoacaoAgape, FamiliaAgape.id == DoacaoAgape.fk_familia_agape_id
            )
            .outerjoin(
                subquery_recibos,
                DoacaoAgape.id == subquery_recibos.c.fk_doacao_agape_id,
            )
            .join(
                ItemDoacaoAgape,
                DoacaoAgape.id == ItemDoacaoAgape.fk_doacao_agape_id,
            )
            .join(
                ItemInstanciaAgape,
                ItemDoacaoAgape.fk_item_instancia_agape_id
                == ItemInstanciaAgape.id,
            )
            .join(
                EstoqueAgape,
                ItemInstanciaAgape.fk_estoque_agape_id == EstoqueAgape.id,
            )
            .join(
                InstanciaAcaoAgape,
                InstanciaAcaoAgape.id
                == ItemInstanciaAgape.fk_instancia_acao_agape_id,
            )
            .filter(
                or_(
                    InstanciaAcaoAgape.status
                    == StatusAcaoAgapeEnum.em_andamento,
                    InstanciaAcaoAgape.status
                    == StatusAcaoAgapeEnum.finalizado,
                ),
                InstanciaAcaoAgape.id == fk_instancia_acao_agape_id,
            )
            .group_by(
                DoacaoAgape.id,
                FamiliaAgape.nome_familia,
                DoacaoAgape.created_at,
                subquery_recibos.c.recibos,
            )
            .order_by(DoacaoAgape.created_at.desc())
        )

        if filtros.cpf:
            beneficiarios_query = beneficiarios_query.filter(
                MembroAgape.cpf.ilike(
                    f"%{format_string(filtros.cpf, only_digits=True)}%"
                )
            )

        if filtros.data_inicial:
            beneficiarios_query = beneficiarios_query.filter(
                between(
                    cast(DoacaoAgape.created_at, Date),
                    filtros.data_inicial,
                    filtros.data_final,
                )
            )

        if filtros.recibos == ReceiptsEnum.com_recibo:
            beneficiarios_query = beneficiarios_query.filter(
                subquery_recibos.c.recibos != ""
            )
        elif filtros.recibos == ReceiptsEnum.sem_recibo:
            beneficiarios_query = beneficiarios_query.filter(
                func.coalesce(subquery_recibos.c.recibos, "") == ""
            )

        return beneficiarios_query

    def get_beneficiary_donated_items(
        self, fk_doacao_agape_id: int
    ) -> List[DonatedItemSchema]:
        itens_query = (
            self.__database.session.query(
                EstoqueAgape.item,
                ItemDoacaoAgape.quantidade,
            )
            .join(
                ItemInstanciaAgape,
                ItemInstanciaAgape.id
                == ItemDoacaoAgape.fk_item_instancia_agape_id,
            )
            .join(
                EstoqueAgape,
                EstoqueAgape.id == ItemInstanciaAgape.fk_estoque_agape_id,
            )
            .filter(ItemDoacaoAgape.fk_doacao_agape_id == fk_doacao_agape_id)
        ).order_by(EstoqueAgape.item)

        itens = itens_query.all()

        return itens

    def get_agape_items_balance_history(
        self, filtros: GetAgapeItemsBalanceHistoryQuery
    ) -> Query:
        movimentacoes_query = (
            self.__database.session.query(
                HistoricoMovimentacaoAgape.id,
                EstoqueAgape.item,
                HistoricoMovimentacaoAgape.quantidade,
                HistoricoMovimentacaoAgape.tipo_movimentacao,
                func.format(
                    HistoricoMovimentacaoAgape.created_at, "dd/MM/yyyy HH:mm"
                ).label("data_movimentacao"),
            )
            .join(
                EstoqueAgape,
                EstoqueAgape.id
                == HistoricoMovimentacaoAgape.fk_estoque_agape_id,
            )
            .order_by(
                HistoricoMovimentacaoAgape.created_at.desc(), EstoqueAgape.item
            )
        )

        if filtros.fk_estoque_agape_id:
            movimentacoes_query = movimentacoes_query.filter(
                EstoqueAgape.id == filtros.fk_estoque_agape_id
            )
        if filtros.tipo_movimentacao:
            movimentacoes_query = movimentacoes_query.filter(
                HistoricoMovimentacaoAgape.tipo_movimentacao
                == filtros.tipo_movimentacao
            )
        if filtros.data_movimentacao_inicial:
            movimentacoes_query = movimentacoes_query.filter(
                between(
                    cast(HistoricoMovimentacaoAgape.created_at, Date),
                    filtros.data_movimentacao_inicial,
                    filtros.data_movimentacao_final,
                )
            )

        return movimentacoes_query

    def get_agape_action_instance_by_id(
        self, fk_instancia_acao_agape_id: int
    ) -> Optional[InstanciaAcaoAgape]:
        instancia_acao_agape = self.__database.session.get(
            InstanciaAcaoAgape, fk_instancia_acao_agape_id
        )

        return instancia_acao_agape

    def get_agape_families_info(self) -> GetAgapeFamiliesInfoSchema:
        familias_query = self.__database.session.query(
            func.coalesce(func.count(FamiliaAgape.id), 0).label("cadastradas"),
            func.coalesce(
                func.sum(case((FamiliaAgape.status == True, 1), else_=0)),
                0,
            ).label("ativas"),
            func.coalesce(
                func.sum(case((FamiliaAgape.status == False, 1), else_=0)),
                0,
            ).label("inativas"),
        ).filter(FamiliaAgape.deleted_at.is_(None))

        familias = familias_query.first()

        return familias

    def get_number_registered_agape_families_members(
        self, fk_familia_agape_id: Optional[int] = None
    ) -> GetNumberRegisteredAgapeMembersSchema:
        membros_cadastrados_query = (
            self.__database.session.query(
                func.coalesce(func.count(MembroAgape.id), 0).label(
                    "quantidade"
                )
            )
            .join(
                FamiliaAgape,
                FamiliaAgape.id == MembroAgape.fk_familia_agape_id,
            )
            .filter(FamiliaAgape.deleted_at.is_(None))
        )

        if fk_familia_agape_id:
            membros_cadastrados_query = membros_cadastrados_query.filter(
                FamiliaAgape.id == fk_familia_agape_id
            )

        membros_cadastrados = membros_cadastrados_query.first()

        return membros_cadastrados

    def get_sum_agape_families_income(
        self, fk_familia_agape_id: Optional[int] = None
    ) -> GetSumAgapeFamiliesIncomeSchema:
        renda_query = (
            self.__database.session.query(
                func.coalesce(func.sum(MembroAgape.renda), 0).label("total"),
            )
            .join(
                FamiliaAgape,
                FamiliaAgape.id == MembroAgape.fk_familia_agape_id,
            )
            .filter(
                FamiliaAgape.deleted_at.is_(None), 
                MembroAgape.renda.isnot(None)
            )
        )

        if fk_familia_agape_id:
            renda_query = renda_query.filter(
                FamiliaAgape.id == fk_familia_agape_id
            )

        renda = renda_query.first()

        return renda

    def get_number_stock_items(self) -> GetNumberStockItemsSchema:
        itens_query = self.__database.session.query(
            func.coalesce(func.sum(EstoqueAgape.quantidade), 0).label(
                "em_estoque"
            )
        )

        itens = itens_query.first()

        return itens

    def get_last_agape_action(self) -> GetLastAgapeActionSchema:
        ultima_acao_query = (
            self.__database.session.query(
                InstanciaAcaoAgape.data_termino.label("data"),
                func.sum(ItemDoacaoAgape.quantidade).label(
                    "quantidade_itens_doados"
                ),
            )
            .join(
                ItemInstanciaAgape,
                InstanciaAcaoAgape.id
                == ItemInstanciaAgape.fk_instancia_acao_agape_id,
            )
            .join(
                ItemDoacaoAgape,
                ItemInstanciaAgape.id
                == ItemDoacaoAgape.fk_item_instancia_agape_id,
            )
            .filter(
                InstanciaAcaoAgape.status == StatusAcaoAgapeEnum.finalizado
            )
            .group_by(InstanciaAcaoAgape.data_termino)
            .order_by(InstanciaAcaoAgape.data_termino.desc())
        )

        ultima_acao = ultima_acao_query.first()

        return ultima_acao

    def get_last_stock_supply(self) -> GetLastStockSupplySchema:
        ultima_entrada_query = self.__database.session.query(
            AquisicaoAgape.created_at.label("data"),
            func.coalesce(AquisicaoAgape.quantidade, 0).label("quantidade"),
        ).order_by(AquisicaoAgape.created_at.desc())

        ultima_entrada = ultima_entrada_query.first()

        return ultima_entrada

    def get_total_donations_receipts(
        self, fk_familia_agape_id: int
    ) -> GetTotalDonationsReceiptsSchema:
        doacoes_query = (
            self.__database.session.query(
                func.coalesce(func.sum(ItemDoacaoAgape.quantidade), 0).label(
                    "total_recebidas"
                ),
            )
            .join(
                DoacaoAgape,
                DoacaoAgape.id == ItemDoacaoAgape.fk_doacao_agape_id,
            )
            .join(
                FamiliaAgape,
                FamiliaAgape.id == DoacaoAgape.fk_familia_agape_id,
            )
            .filter(FamiliaAgape.id == fk_familia_agape_id)
        )

        doacoes = doacoes_query.first()

        return doacoes

    def get_all_donations_receipts(self, fk_familia_agape_id: int) -> Query:
        subquery_recibos = (
            self.__database.session.query(
                ReciboAgape.fk_doacao_agape_id.label("fk_doacao_agape_id"),
                func.string_agg(
                    ReciboAgape.recibo, literal_column("','")
                ).label("recibos"),
            ).group_by(ReciboAgape.fk_doacao_agape_id)
        ).subquery("subquery_recibos")

        doacoes_query = (
            self.__database.session.query(
                AcaoAgape.nome.label("nome_acao"),
                InstanciaAcaoAgape.id.label("fk_instancia_acao_agape_id"),
                DoacaoAgape.id.label("fk_doacao_agape_id"),
                func.format(
                    DoacaoAgape.created_at, "dd/MM/yyyy - HH:mm"
                ).label("dia_horario"),
                func.coalesce(subquery_recibos.c.recibos, "").label("recibos"),
            )
            .select_from(FamiliaAgape)
            .join(
                DoacaoAgape, FamiliaAgape.id == DoacaoAgape.fk_familia_agape_id
            )
            .join(
                subquery_recibos,
                DoacaoAgape.id == subquery_recibos.c.fk_doacao_agape_id,
                isouter=True,
            )
            .join(
                ItemDoacaoAgape,
                DoacaoAgape.id == ItemDoacaoAgape.fk_doacao_agape_id,
            )
            .join(
                ItemInstanciaAgape,
                ItemDoacaoAgape.fk_item_instancia_agape_id
                == ItemInstanciaAgape.id,
            )
            .join(
                InstanciaAcaoAgape,
                ItemInstanciaAgape.fk_instancia_acao_agape_id
                == InstanciaAcaoAgape.id,
            )
            .join(
                AcaoAgape, AcaoAgape.id == InstanciaAcaoAgape.fk_acao_agape_id
            )
            .group_by(
                AcaoAgape.nome,
                DoacaoAgape.id,
                InstanciaAcaoAgape.id,
                DoacaoAgape.created_at,
                subquery_recibos.c.recibos,
            )
            .order_by(DoacaoAgape.created_at.desc(), AcaoAgape.nome)
            .filter(FamiliaAgape.id == fk_familia_agape_id)
        )

        return doacoes_query

    def get_all_items_receipts(
        self, fk_instancia_acao_agape_id: int, fk_doacao_agape_id: int
    ) -> List[ItemReceiptSchema]:
        itens_query = (
            self.__database.session.query(
                EstoqueAgape.item,
                func.sum(ItemDoacaoAgape.quantidade).label("quantidade"),
            )
            .select_from(DoacaoAgape)
            .join(
                ItemDoacaoAgape,
                DoacaoAgape.id == ItemDoacaoAgape.fk_doacao_agape_id,
            )
            .join(
                ItemInstanciaAgape,
                ItemDoacaoAgape.fk_item_instancia_agape_id
                == ItemInstanciaAgape.id,
            )
            .join(
                EstoqueAgape,
                EstoqueAgape.id == ItemInstanciaAgape.fk_estoque_agape_id,
            )
            .group_by(EstoqueAgape.item)
            .filter(
                ItemInstanciaAgape.fk_instancia_acao_agape_id
                == fk_instancia_acao_agape_id,
                DoacaoAgape.id == fk_doacao_agape_id,
            )
        )

        itens = itens_query.all()

        return itens

    def get_all_agape_families_address(self) -> List[AgapeFamilyAddress]:
        enderecos_query = Endereco.query.join(
            FamiliaAgape, Endereco.id == FamiliaAgape.fk_endereco_id
        ).filter(FamiliaAgape.deleted_at.is_(None))

        enderecos = enderecos_query.all()

        return enderecos

    def get_instance_beneficiaries_geolocations(
        self, fk_instancia_acao_agape_id: int
    ) -> List[BeneficiariesGeolocationsSchema]:
        enderecos_beneficiarios_query = (
            self.__database.session.query(
                FamiliaAgape.nome_familia,
                Endereco.latitude,
                Endereco.longitude,
            )
            .join(FamiliaAgape, Endereco.id == FamiliaAgape.fk_endereco_id)
            .join(
                DoacaoAgape, DoacaoAgape.fk_familia_agape_id == FamiliaAgape.id
            )
            .join(
                ItemDoacaoAgape,
                ItemDoacaoAgape.fk_doacao_agape_id == DoacaoAgape.id,
            )
            .join(
                ItemInstanciaAgape,
                ItemInstanciaAgape.id
                == ItemDoacaoAgape.fk_item_instancia_agape_id,
            )
            .join(
                InstanciaAcaoAgape,
                InstanciaAcaoAgape.id
                == ItemInstanciaAgape.fk_instancia_acao_agape_id,
            )
            .filter(InstanciaAcaoAgape.id == fk_instancia_acao_agape_id)
        )

        enderecos_beneficiarios = enderecos_beneficiarios_query.all()

        return enderecos_beneficiarios

    def get_volunteer_profile(self) -> Perfil:
        perfil_voluntario = (
            self.__database.session.query(Perfil)
            .filter_by(nome=ProfilesEnum.VOLUNTARIO_AGAPE)
            .first()
        )

        return perfil_voluntario

    def get_volunteer_permission(
        self, voluntario_agape: Perfil
    ) -> PermissaoMenu:
        permissao_query = (
            PermissaoMenu.query.join(
                Perfil, PermissaoMenu.fk_perfil_id == Perfil.id
            )
            .join(MenuSistema, PermissaoMenu.fk_menu_id == MenuSistema.id)
            .filter(
                Perfil.id == voluntario_agape.id,
                MenuSistema.slug == "familia_agape",
            )
        )
        permissao = permissao_query.first()

        return permissao

    def update_volunteer_permission(self, permissao: PermissaoMenu) -> None:
        permissao.acessar = not permissao.acessar
        permissao.criar = not permissao.criar
        permissao.editar = not permissao.editar

        try:
            self.__database.session.commit()
        except Exception as exception:
            self.__database.session.rollback()
            raise exception

    def get_all_agape_volunteers(
        self, filtros: PaginationQuery
    ) -> tuple[list[Usuario], int]:
        voluntarios_query = (
            self.__database.session.query(Usuario)
            .join(
                PermissaoUsuario,
                PermissaoUsuario.fk_usuario_id == Usuario.id,
            )
            .join(Perfil, Perfil.id == PermissaoUsuario.fk_perfil_id)
            .filter(Perfil.nome == ProfilesEnum.VOLUNTARIO_AGAPE)
            .order_by(Usuario.nome)
        )

        voluntarios_paginate = voluntarios_query.paginate(
            page=filtros.page, per_page=filtros.per_page, error_out=False
        )
        voluntarios, total = (
            voluntarios_paginate.items,
            voluntarios_paginate.total,
        )

        return voluntarios, total

    def update_user_profile_to_agape_voluntary(
        self, fk_usuario_id: Usuario
    ) -> None:
        db_usuario: Usuario = self.__database.session.get(
            Usuario, fk_usuario_id
        )
        if not db_usuario or db_usuario.deleted_at is not None:
            raise NotFoundError("Usuário não encontrado.")

        perfil = Perfil.query.filter_by(
            nome=ProfilesEnum.VOLUNTARIO_AGAPE
        ).first()
        if not perfil:
            raise NotFoundError("Perfil de voluntário não encontrado.")

        permissao_usuario = PermissaoUsuario.query.filter_by(
            fk_usuario_id=db_usuario.id
        ).first()

        permissao_usuario.fk_perfil_id = perfil.id

        try:
            self.__database.session.commit()
        except Exception as exception:
            self.__database.session.rollback()
            raise exception

    def remove_user_from_agape_voluntary_profile(
        self, fk_usuario_id: Usuario
    ) -> None:
        db_usuario: Usuario = self.__database.session.get(
            Usuario, fk_usuario_id
        )
        if not db_usuario or db_usuario.deleted_at is not None:
            raise NotFoundError("Usuário não encontrado.")

        permissao_usuario = PermissaoUsuario.query.filter_by(
            fk_usuario_id=db_usuario.id
        ).first()

        perfil_atual = self.__database.session.get(
            Perfil, permissao_usuario.fk_perfil_id
        )
        if perfil_atual.nome != ProfilesEnum.VOLUNTARIO_AGAPE:
            raise NotFoundError(
                "Não é possível remover um usuário que não é um voluntário."
            )

        perfil_benfeitor = Perfil.query.filter_by(
            nome=ProfilesEnum.BENFEITOR
        ).first()
        if not perfil_benfeitor:
            raise NotFoundError("Perfil de benfeitor não encontrado.")

        permissao_usuario.fk_perfil_id = perfil_benfeitor.id

        try:
            self.__database.session.commit()
        except Exception as exception:
            self.__database.session.rollback()
            raise exception

    def export_agape_families(self) -> list:
        familias_query = (
            self.__database.session.query(
                FamiliaAgape.nome_familia,
                FamiliaAgape.created_at.label("data_cadastro_familia"),
                MembroAgape.nome,
                case(
                    (MembroAgape.responsavel == True, "Sim"), else_="Não"
                ).label("responsavel"),
                MembroAgape.telefone,
                MembroAgape.email,
                MembroAgape.cpf,
                MembroAgape.data_nascimento,
                MembroAgape.ocupacao,
                MembroAgape.renda,
                MembroAgape.created_at.label("data_cadastro_membro"),
                Endereco.rua,
                Endereco.numero,
                Endereco.complemento,
                Endereco.bairro,
                Endereco.ponto_referencia,
                Endereco.cidade,
                Endereco.estado,
                Endereco.cep,
            )
            .join(
                MembroAgape,
                MembroAgape.fk_familia_agape_id == FamiliaAgape.id,
            )
            .join(Endereco, Endereco.id == FamiliaAgape.fk_endereco_id)
            .order_by(FamiliaAgape.nome_familia, MembroAgape.nome)
        )

        familias = familias_query.all()

        return familias

    def export_agape_donations(self, fk_instancia_acao_agape_id: int) -> list:
        doacoes_query = (
            self.__database.session.query(
                AcaoAgape.nome,
                FamiliaAgape.nome_familia,
                EstoqueAgape.item,
                ItemDoacaoAgape.quantidade,
                ItemDoacaoAgape.created_at,
            )
            .select_from(DoacaoAgape)
            .join(
                FamiliaAgape,
                DoacaoAgape.fk_familia_agape_id == FamiliaAgape.id,
            )
            .join(
                ItemDoacaoAgape,
                DoacaoAgape.id == ItemDoacaoAgape.fk_doacao_agape_id,
            )
            .join(
                ItemInstanciaAgape,
                ItemInstanciaAgape.id
                == ItemDoacaoAgape.fk_item_instancia_agape_id,
            )
            .join(
                InstanciaAcaoAgape,
                InstanciaAcaoAgape.id
                == ItemInstanciaAgape.fk_instancia_acao_agape_id,
            )
            .join(
                AcaoAgape, InstanciaAcaoAgape.fk_acao_agape_id == AcaoAgape.id
            )
            .join(
                EstoqueAgape,
                ItemInstanciaAgape.fk_estoque_agape_id == EstoqueAgape.id,
            )
            .filter(InstanciaAcaoAgape.id == fk_instancia_acao_agape_id)
            .order_by(
                FamiliaAgape.nome_familia, ItemDoacaoAgape.created_at.desc()
            )
        )

        doacoes = doacoes_query.all()

        return doacoes
