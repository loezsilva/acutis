from datetime import datetime
from typing import Optional
from uuid import UUID

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, distinct, func, select
from sqlalchemy.orm import aliased, selectinload

from acutis_api.communication.enums.membros import PerfilEnum
from acutis_api.communication.requests.agape import (
    CoordenadaFormData,
    EditarEnderecoFamiliaAgapeRequest,
    EnderecoAgapeFormData,
    RegistrarItemCicloAcaoAgapeFormData,
)
from acutis_api.domain.entities.acao_agape import AcaoAgape
from acutis_api.domain.entities.aquisicao_agape import AquisicaoAgape
from acutis_api.domain.entities.coordenada import Coordenada
from acutis_api.domain.entities.doacao_agape import DoacaoAgape
from acutis_api.domain.entities.endereco import Endereco
from acutis_api.domain.entities.estoque_agape import EstoqueAgape
from acutis_api.domain.entities.familia_agape import FamiliaAgape
from acutis_api.domain.entities.foto_familia_agape import FotoFamiliaAgape
from acutis_api.domain.entities.historico_movimentacao_agape import (
    HistoricoDestinoEnum,
    HistoricoMovimentacaoAgape,
    HistoricoOrigemEnum,
    TipoMovimentacaoEnum,
)
from acutis_api.domain.entities.instancia_acao_agape import (
    InstanciaAcaoAgape,
    StatusAcaoAgapeEnum,
)
from acutis_api.domain.entities.item_doacao_agape import ItemDoacaoAgape
from acutis_api.domain.entities.item_instancia_agape import ItemInstanciaAgape
from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.entities.membro_agape import MembroAgape
from acutis_api.domain.entities.perfil import Perfil
from acutis_api.domain.entities.permissao_lead import PermissaoLead
from acutis_api.domain.entities.recibo_agape import ReciboAgape
from acutis_api.domain.repositories.agape import (
    AgapeRepositoryInterface,
)
from acutis_api.domain.repositories.schemas.agape import (
    ContagemItensEstoqueSchema,
    CoordenadasSchema,
    DadosCompletosDoacaoSchema,
    DadosExportacaoFamiliaSchema,
    DoacaoAgapeSchema,
    EstoqueAgapeSchema,
    FotoFamiliaAgapeSchema,
    InformacoesAgregadasFamiliasSchema,
    ListarCicloAcoesAgapeFiltros,
    ListarItensEstoqueAgapeFiltros,
    ListarMembrosFamiliaAgapeFiltros,
    ListarNomesAcoesAgapeFiltros,
    MembroFamiliaSchema,
    NomeAcaoAgapeSchema,
    NumeroMembrosFamiliaAgapeSchema,
    NumeroTotalMembrosSchema,
    RegistrarCicloAcaoAgapeScheme,
    RegistrarFamiliaAgapeSchema,
    RegistrarItemEstoqueAgapeSchema,
    RegistrarNomeAcaoAgapeSchema,
    SomaRendaFamiliarAgapeSchema,
    SomaTotalRendaSchema,
    TotalItensRecebidosSchema,
    UltimaAcaoAgapeSchema,
    UltimaEntradaEstoqueSchema,
)
from acutis_api.domain.repositories.schemas.paginacao import PaginacaoQuery
from acutis_api.exception.errors.not_found import HttpNotFoundError


class AgapeRepository(AgapeRepositoryInterface):
    def __init__(self, database: SQLAlchemy):
        self._database = database

    def salvar_alteracoes(self):
        self._database.session.commit()

    def registrar_nome_acao_agape(
        self, dados: RegistrarNomeAcaoAgapeSchema
    ) -> AcaoAgape:
        instancia = AcaoAgape(
            nome=dados.nome,
        )
        self._database.session.add(instancia)

        return instancia

    def buscar_acao_por_nome(self, nome_acao: str) -> AcaoAgape | None:
        instancia = self._database.session.scalar(
            select(AcaoAgape).where(AcaoAgape.nome == nome_acao)
        )

        if instancia is None:
            raise HttpNotFoundError(f'Ação {nome_acao} não encontrada.')

        return instancia

    def buscar_nome_acao_por_id(self, nome_acao_id: UUID) -> AcaoAgape | None:
        instancia = self._database.session.scalar(
            select(AcaoAgape).where(AcaoAgape.id == nome_acao_id)
        )
        if instancia is None:
            raise HttpNotFoundError(
                f'Nome da ação {nome_acao_id} não encontrada.'
            )

        return instancia

    def verificar_nome_da_acao(self, nome_acao: str) -> tuple:
        return (
            self._database.session.query(AcaoAgape)
            .filter(AcaoAgape.nome == nome_acao.strip())
            .first()
        )

    def listar_nomes_acoes_agape(
        self, filtros: ListarNomesAcoesAgapeFiltros
    ) -> tuple[list[NomeAcaoAgapeSchema], int]:
        query = self._database.session.query(AcaoAgape).order_by(
            desc(AcaoAgape.nome)
        )

        if filtros.nome:
            query = query.filter(AcaoAgape.nome.like(f'%{filtros.nome}%'))

        paginacao = query.paginate(
            page=filtros.pagina,
            per_page=filtros.por_pagina,
            error_out=False,
        )

        return paginacao.items, paginacao.total

    def listar_membros_por_familia_id(
        self, familia_id: UUID
    ) -> list[MembroAgape]:
        return (
            self._database.session.query(MembroAgape)
            .filter(MembroAgape.fk_familia_agape_id == familia_id)
            .all()
        )

    def listar_membros_familia(
        self, filtros: ListarMembrosFamiliaAgapeFiltros
    ) -> tuple[list[MembroFamiliaSchema], int]:
        query = self._database.session.query(MembroAgape).order_by(
            desc(MembroAgape.nome)
        )

        if filtros.familia_id:
            query = query.filter(AcaoAgape.id == filtros.familia_id)

        paginacao = query.paginate(
            page=filtros.pagina,
            per_page=filtros.por_pagina,
            error_out=False,
        )

        return paginacao.items, paginacao.total

    def buscar_item_estoque_por_id(self, item_id) -> EstoqueAgape | None:
        """
        Retorna um item de estoque pelo seu ID.
        """
        instancia = self._database.session.get(EstoqueAgape, item_id)

        if instancia is None:
            raise HttpNotFoundError(f'Item {item_id} não encontrado.')

        return instancia

    def verificar_item_estoque(self, item: str) -> tuple:
        return (
            self._database.session.query(EstoqueAgape)
            .filter(EstoqueAgape.item == item.strip())
            .first()
        )

    def registrar_item_estoque(
        self, dados: RegistrarItemEstoqueAgapeSchema
    ) -> EstoqueAgape:
        instancia = EstoqueAgape(
            item=dados.item,
            quantidade=dados.quantidade,
        )
        self._database.session.add(instancia)

        return instancia

    def remover_item_estoque(self, item: EstoqueAgape) -> None:
        """
        Remove um item de estoque do banco de dados.
        """
        self._database.session.delete(item)

    def listar_itens_estoque_agape(
        self, filtros: ListarItensEstoqueAgapeFiltros
    ) -> tuple[list[EstoqueAgapeSchema], int]:
        query = self._database.session.query(EstoqueAgape).order_by(
            desc(EstoqueAgape.item)
        )

        if filtros.item:
            query = query.filter(EstoqueAgape.item.like(f'%{filtros.item}%'))

        paginacao = query.paginate(
            page=filtros.pagina,
            per_page=filtros.por_pagina,
            error_out=False,
        )

        return paginacao.items, paginacao.total

    # Ciclo de ação Ágape
    def buscar_ciclo_acao_agape_por_id(self, acao_agape_id):
        """Retorna a instância de ciclo de ação Ágape pelo ID da instância."""

        instancia = self._database.session.get(
            InstanciaAcaoAgape, acao_agape_id
        )

        return instancia

    def buscar_endereco_ciclo_acao_agape(self, acao_agape_id):
        """Retorna o endereço de uma instância de ciclo de ação Ágape."""
        return (
            self._database.session.query(Endereco)
            .join(
                InstanciaAcaoAgape,
                Endereco.id == InstanciaAcaoAgape.fk_endereco_id,
            )
            .filter(InstanciaAcaoAgape.id == acao_agape_id)
            .first()
        )

    def buscar_doacoes_ciclo_acao_agape(
        self, acao_agape_id
    ) -> list[DoacaoAgapeSchema]:
        """Retorna lista de doações de uma instância de ciclo de ação Ágape."""

        instancias = (
            self._database.session.query(
                ItemInstanciaAgape.id,
                EstoqueAgape.item,
                EstoqueAgape.id.label('item_id'),
                ItemInstanciaAgape.quantidade,
            )
            .select_from(InstanciaAcaoAgape)
            .join(
                ItemInstanciaAgape,
                (
                    InstanciaAcaoAgape.id
                    == ItemInstanciaAgape.fk_instancia_acao_agape_id
                ),
            )
            .join(
                EstoqueAgape,
                EstoqueAgape.id == ItemInstanciaAgape.fk_estoque_agape_id,
            )
            .filter(
                ItemInstanciaAgape.fk_instancia_acao_agape_id == acao_agape_id
            )
            .all()
        )

        return instancias

    def listar_itens_ciclo_acao_agape(
        self, acao_agape_id
    ) -> list[ItemInstanciaAgape]:
        """Retorna lista de itens de um ciclo de ação Ágape."""

        session = self._database.session

        instancias = (
            session.query(ItemInstanciaAgape)
            .filter_by(fk_instancia_acao_agape_id=acao_agape_id)
            .all()
        )

        return instancias

    def buscar_itens_ciclo_acao_agape(
        self, acao_agape_id
    ) -> list[DoacaoAgapeSchema]:
        """
        Retorna itens de estoque usados em um ciclo de ação Ágape.
        """
        return self.buscar_doacoes_ciclo_acao_agape(acao_agape_id)

    def registrar_endereco(self, dados: EnderecoAgapeFormData) -> Endereco:
        """Registra um novo endereço."""

        session = self._database.session

        # Salva endereço
        instancia = Endereco(
            codigo_postal=dados.cep,
            tipo_logradouro=None,
            logradouro=dados.rua,
            numero=dados.numero,
            complemento=dados.complemento,
            bairro=dados.bairro,
            cidade=dados.cidade,
            estado=dados.estado,
            pais=None,
            obriga_atualizar_endereco=True,
        )

        session.add(instancia)

        return instancia

    def registrar_coordenada(
        self, endereco_id, dados: CoordenadaFormData
    ) -> Coordenada:
        """Registra uma nova coordenada."""

        session = self._database.session

        instancia = Coordenada(
            fk_endereco_id=endereco_id,
            latitude=dados.latitude,
            longitude=dados.longitude,
            latitude_ne=dados.latitude_ne,
            longitude_ne=dados.longitude_ne,
            latitude_so=dados.latitude_so,
            longitude_so=dados.longitude_so,
        )

        session.add(instancia)

        return instancia

    def registrar_ciclo_acao_agape(
        self, dados: RegistrarCicloAcaoAgapeScheme
    ) -> InstanciaAcaoAgape:
        """
        Registra um novo ciclo de ação Ágape.
        """
        session = self._database.session

        # Cria instância do ciclo
        instancia = InstanciaAcaoAgape(
            fk_endereco_id=dados.endereco_id,
            fk_acao_agape_id=dados.nome_acao_id,
            abrangencia=dados.abrangencia,
            data_inicio=None,
            data_termino=None,
        )
        session.add(instancia)
        session.flush()

        return instancia

    # Ciclo de ação Ágape
    def buscar_item_ciclo_acao_agape_por_id(
        self, item_ciclo_id: UUID
    ) -> ItemInstanciaAgape:
        """Retorna a instância de ciclo de ação Ágape pelo ID da instância."""
        instancia = self._database.session.get(
            ItemInstanciaAgape, item_ciclo_id
        )

        if instancia is None:
            raise HttpNotFoundError(
                f'Item ciclo da ação {item_ciclo_id} não encontrado.'
            )

        return instancia

    def deletar_item_ciclo_acao_agape(self, item_ciclo_id: UUID) -> None:
        """
        Deleta um item de ciclo de ação Ágape.
        """
        session = self._database.session

        instancia = self.buscar_item_ciclo_acao_agape_por_id(item_ciclo_id)

        session.delete(instancia)

    def retorna_item_estoque_ciclo_acao_agape(
        self, item_ciclo_id: UUID
    ) -> None:
        session = self._database.session

        item_ciclo = self.buscar_item_ciclo_acao_agape_por_id(item_ciclo_id)
        item_estoque = self.buscar_item_estoque_por_id(
            item_ciclo.fk_estoque_agape_id
        )

        item_estoque.quantidade += item_ciclo.quantidade

        # Registra movimentação de saída
        historico = HistoricoMovimentacaoAgape(
            fk_estoque_agape_id=item_estoque.id,
            fk_instancia_acao_agape_id=None,
            quantidade=item_ciclo.quantidade,
            origem=HistoricoOrigemEnum.acao,
            destino=HistoricoDestinoEnum.estoque,
            tipo_movimentacoes=TipoMovimentacaoEnum.entrada,
        )
        session.add(historico)

    def registrar_item_ciclo_acao_agape(
        self, ciclo_acao_id, dados: RegistrarItemCicloAcaoAgapeFormData
    ) -> None:
        session = self._database.session

        item = self.buscar_item_estoque_por_id(dados.item_id)

        if int(dados.quantidade) > int(item.quantidade):
            from acutis_api.exception.errors.unprocessable_entity import (
                HttpUnprocessableEntityError,
            )

            raise HttpUnprocessableEntityError(
                f"Quantidade insuficiente em estoque para '{item.item}'."
            )

        # Ajusta estoque
        item.quantidade -= dados.quantidade

        # Registra item de instância
        instancia = ItemInstanciaAgape(
            fk_estoque_agape_id=item.id,
            fk_instancia_acao_agape_id=ciclo_acao_id,
            quantidade=dados.quantidade,
        )

        session.add(instancia)

        # Registra movimentação de saída
        historico = HistoricoMovimentacaoAgape(
            fk_estoque_agape_id=item.id,
            fk_instancia_acao_agape_id=None,
            quantidade=dados.quantidade,
            origem=HistoricoOrigemEnum.estoque,
            destino=HistoricoDestinoEnum.acao,
            tipo_movimentacoes=TipoMovimentacaoEnum.saida,
        )
        session.add(historico)

        return instancia

    def listar_ciclos_acao(
        self, filtros: ListarCicloAcoesAgapeFiltros
    ) -> tuple[list[InstanciaAcaoAgape], int]:
        """
        Retorna lista paginada de instâncias de ciclo de ação Ágape,
        permitindo filtrar por ID da ação e por status do ciclo.
        """
        session = self._database.session
        query = session.query(InstanciaAcaoAgape)

        # Filtros opcionais
        if hasattr(filtros, 'fk_acao_id') and filtros.fk_acao_id:
            query = query.filter(
                InstanciaAcaoAgape.fk_acao_agape_id == filtros.fk_acao_id
            )

        # Filtro por status
        if hasattr(filtros, 'status') and filtros.status:
            query = query.filter(InstanciaAcaoAgape.status == filtros.status)

        # Ordenação: mais recentes primeiro
        query = query.order_by(InstanciaAcaoAgape.criado_em.desc())

        # Paginação
        paginacao = query.paginate(
            page=filtros.pagina,
            per_page=filtros.por_pagina,
            error_out=False,
        )

        return paginacao.items, paginacao.total

    def listar_familias(self, filtros) -> tuple[list[FamiliaAgape], int]:
        session = self._database.session
        query = session.query(FamiliaAgape)

        # Ordenação: mais recentes primeiro
        query = query.order_by(FamiliaAgape.criado_em.desc())

        # Paginação
        paginacao = query.paginate(
            page=filtros.pagina,
            per_page=filtros.por_pagina,
            error_out=False,
        )

        return paginacao.items, paginacao.total

    def iniciar_ciclo_acao_agape(
        self, ciclo_acao: InstanciaAcaoAgape
    ) -> InstanciaAcaoAgape:
        """
        Inicia um ciclo de uma ação Ágape, marcando status e data de início.
        """

        session = self._database.session

        # Inicia ciclo
        ciclo_acao.status = StatusAcaoAgapeEnum.em_andamento
        ciclo_acao.data_inicio = datetime.utcnow()

        session.add(ciclo_acao)

        return ciclo_acao

    def finalizar_ciclo_acao_agape(
        self, ciclo_acao: InstanciaAcaoAgape
    ) -> InstanciaAcaoAgape:
        """
        Finaliza o ciclo de uma ação Ágape
        """

        session = self._database.session

        # Finaliza ciclo
        ciclo_acao.status = StatusAcaoAgapeEnum.finalizado
        ciclo_acao.data_termino = datetime.utcnow()

        session.add(ciclo_acao)

        return ciclo_acao

    def deletar_ciclo_acao_agape(self, acao_agape_id) -> InstanciaAcaoAgape:
        """
        Deleta um ciclo de ação Ágape não iniciado
        """

        session = self._database.session

        instancia = self.buscar_ciclo_acao_agape_por_id(acao_agape_id)

        # Remove ciclo
        session.delete(instancia)

        return {}

    def buscar_membro_familia_por_id(self, membro_id: UUID) -> FamiliaAgape:
        """
        Retorna a instância de um membro da família pelo ID da instância.
        """
        instancia = self._database.session.get(MembroAgape, membro_id)

        return instancia

    def verificar_membro_familia_por_email(self, email: str) -> MembroAgape:
        """
        Verifica se o email já está cadastrado na família.
        """
        return (
            self._database.session.query(MembroAgape)
            .filter(MembroAgape.email == email.strip())
            .first()
        )

    def verificar_ciclo_acao_iniciado(
        self, ciclo_acao: InstanciaAcaoAgape
    ) -> InstanciaAcaoAgape:
        """
        Verifica se o ciclo de uma ação Ágape já foi iniciado.
        """
        session = self._database.session

        # Verifica se já existe ciclo em andamento para essa ação
        ciclo_em_andamento = (
            session.query(InstanciaAcaoAgape)
            .filter(
                (InstanciaAcaoAgape.fk_acao_agape_id == ciclo_acao.id),
                (
                    InstanciaAcaoAgape.status
                    == StatusAcaoAgapeEnum.em_andamento
                ),
            )
            .first()
        )
        return ciclo_em_andamento

    def verificar_ciclo_acao_finalizado(
        self, ciclo_acao: InstanciaAcaoAgape
    ) -> InstanciaAcaoAgape:
        """
        Verifica se o ciclo de uma ação Ágape já foi finalizado.
        """
        session = self._database.session

        # Verifica se já existe ciclo em andamento para essa ação
        ciclo_em_andamento = (
            session.query(InstanciaAcaoAgape)
            .filter(
                (InstanciaAcaoAgape.fk_acao_agape_id == ciclo_acao.id),
                (InstanciaAcaoAgape.status == StatusAcaoAgapeEnum.finalizado),
            )
            .first()
        )
        return ciclo_em_andamento

    def verficar_membro_familia_por_cpf(self, cpf: str) -> MembroAgape:
        """
        Verifica se o cpf já está cadastrado na família.
        """
        return (
            self._database.session.query(MembroAgape)
            .filter(MembroAgape.cpf == cpf.strip())
            .first()
        )

    def registrar_familia(
        self, dados: RegistrarFamiliaAgapeSchema
    ) -> FamiliaAgape:
        session = self._database.session

        # Cria instância do ciclo
        instancia = FamiliaAgape(
            nome_familia=dados.nome_familia,
            status=False,
            fk_endereco_id=dados.endereco_id,
            observacao=dados.observacao,
            comprovante_residencia=dados.comprovante_residencia,
            cadastrada_por=dados.cadastrada_por,
            deletado_em=None,
        )

        session.add(instancia)

        return instancia

    def registrar_membro_familia(
        self, dados: MembroFamiliaSchema
    ) -> MembroAgape:
        session = self._database.session

        # Cria instância do membro
        instancia = MembroAgape(
            fk_familia_agape_id=dados.familia_id,
            nome=dados.nome,
            email=dados.email,
            telefone=dados.telefone,
            cpf=dados.cpf,
            responsavel=dados.responsavel,
            data_nascimento=dados.data_nascimento,
            funcao_familiar=dados.funcao_familiar,
            escolaridade=dados.escolaridade,
            ocupacao=dados.ocupacao,
            renda=dados.renda,
            foto_documento=dados.foto_documento,
            beneficiario_assistencial=dados.beneficiario_assistencial,
        )

        session.add(instancia)

        return instancia

    def registrar_foto_familia(
        self, dados: FotoFamiliaAgapeSchema
    ) -> FotoFamiliaAgape:
        session = self._database.session

        # Cria instância do membro
        instancia = FotoFamiliaAgape(
            fk_familia_agape_id=dados.familia_id,
            foto=dados.foto,
        )

        session.add(instancia)

        return instancia

    def movimentar_historico_ciclo_acao_agape(
        self,
        item_id,
        ciclo_acao_id,
        quantidade,
    ) -> HistoricoMovimentacaoAgape:
        session = self._database.session

        historico = HistoricoMovimentacaoAgape(
            fk_estoque_agape_id=item_id,
            fk_instancia_acao_agape_id=ciclo_acao_id,
            quantidade=quantidade,
            origem=HistoricoOrigemEnum.acao,
            destino=HistoricoDestinoEnum.estoque,
            tipo_movimentacoes=TipoMovimentacaoEnum.entrada,
        )

        session.add(historico)

    def buscar_lead_por_id(self, id: UUID) -> Lead | None:
        session = self._database.session
        lead = session.get(Lead, id)
        return lead

    def buscar_familia_por_id(
        self, familia_id: UUID
    ) -> Optional[FamiliaAgape]:
        instancia = self._database.session.scalar(
            select(FamiliaAgape).where(
                FamiliaAgape.id == familia_id,
                FamiliaAgape.deletado_em.is_(None),
            )
        )
        return instancia

    def numero_membros_familia_agape(
        self, familia_id: UUID
    ) -> NumeroMembrosFamiliaAgapeSchema:
        """
        Conta o número de membros ativos de uma família.
        """
        familia = self.buscar_familia_por_id(familia_id)
        if not familia:
            raise HttpNotFoundError(
                f'Família com ID {familia_id} não encontrada ou foi deletada.'
            )

        count = (
            self._database.session.scalar(
                select(func.count(MembroAgape.id)).where(
                    MembroAgape.fk_familia_agape_id == familia_id
                )
            )
            or 0
        )
        return NumeroMembrosFamiliaAgapeSchema(quantidade=count)

    def soma_renda_familiar_agape(
        self, familia: FamiliaAgape
    ) -> SomaRendaFamiliarAgapeSchema:
        """
        Soma a renda dos membros ativos de uma família.
        """
        total_sum = (
            self._database.session.scalar(
                select(func.sum(MembroAgape.renda)).where(
                    MembroAgape.fk_familia_agape_id == familia.id
                )
            )
            or 0.0
        )

        return SomaRendaFamiliarAgapeSchema(total=float(total_sum))

    def buscar_endereco_por_id(self, endereco_id: UUID) -> Endereco | None:
        instancia = self._database.session.get(Endereco, endereco_id)
        return instancia

    def buscar_ultimo_ciclo_acao_por_nome_acao_id(
        self, nome_acao_id: UUID
    ) -> InstanciaAcaoAgape | None:
        instancia = (
            self._database.session.query(InstanciaAcaoAgape)
            .filter(InstanciaAcaoAgape.fk_acao_agape_id == nome_acao_id)
            .order_by(desc(InstanciaAcaoAgape.criado_em))
            .first()
        )

        return instancia

    def buscar_membro_por_cpf(self, cpf: str) -> MembroAgape | None:
        membro = (
            self._database.session.query(MembroAgape)
            .filter(MembroAgape.cpf == cpf)
            .first()
        )
        return membro

    def buscar_membro_por_email(self, email: str) -> MembroAgape | None:
        membro = (
            self._database.session.query(MembroAgape)
            .filter(MembroAgape.email == email)
            .first()
        )
        return membro

    def listar_fotos_por_familia_id(
        self, familia_id: UUID
    ) -> list[FotoFamiliaAgape]:
        """Lista todas as fotos de uma família ágape."""
        fotos = (
            self._database.session.query(FotoFamiliaAgape)
            .filter(FotoFamiliaAgape.fk_familia_agape_id == familia_id)
            .all()
        )
        return fotos

    def buscar_ultimo_recebimento_familia_no_ciclo(
        self, familia_id: UUID, ciclo_acao_id: UUID
    ) -> datetime | None:
        data_maxima = (
            self._database.session.query(func.max(DoacaoAgape.criado_em))
            .join(
                ItemDoacaoAgape,
                ItemDoacaoAgape.fk_doacao_agape_id == DoacaoAgape.id,
            )
            .join(
                ItemInstanciaAgape,
                ItemInstanciaAgape.id
                == ItemDoacaoAgape.fk_item_instancia_agape_id,
            )
            .filter(
                DoacaoAgape.fk_familia_agape_id == familia_id,
                ItemInstanciaAgape.fk_instancia_acao_agape_id == ciclo_acao_id,
            )
            .scalar()
        )
        return data_maxima

    def buscar_membro_agape_por_id(
        self, membro_agape_id: UUID
    ) -> MembroAgape | None:
        membro = self._database.session.get(MembroAgape, membro_agape_id)
        return membro

    def registrar_membro_agape(self, membro: MembroAgape) -> MembroAgape:
        """Registra um novo membro ágape na sessão do banco de dados."""
        self._database.session.add(membro)
        return membro

    def total_itens_recebidos_por_familia(
        self, familia: FamiliaAgape
    ) -> TotalItensRecebidosSchema:
        total_sum = (
            self._database.session.query(func.sum(ItemDoacaoAgape.quantidade))
            .join(
                DoacaoAgape,
                ItemDoacaoAgape.fk_doacao_agape_id == DoacaoAgape.id,
            )
            .filter(DoacaoAgape.fk_familia_agape_id == familia.id)
            .scalar()
            or 0
        )

        return TotalItensRecebidosSchema(total_recebidas=int(total_sum))

    def informacoes_agregadas_familias(
        self,
    ) -> InformacoesAgregadasFamiliasSchema:
        session = self._database.session

        total_cadastradas = (
            session.query(func.count(FamiliaAgape.id)).scalar() or 0
        )
        total_ativas = (
            session.query(func.count(FamiliaAgape.id))
            .filter(FamiliaAgape.deletado_em.is_(None))
            .scalar()
            or 0
        )
        total_inativas = (
            session.query(func.count(FamiliaAgape.id))
            .filter(FamiliaAgape.deletado_em.isnot(None))
            .scalar()
            or 0
        )

        return InformacoesAgregadasFamiliasSchema(
            total_cadastradas=total_cadastradas,
            total_ativas=total_ativas,
            total_inativas=total_inativas,
        )

    def numero_total_membros_agape(self) -> NumeroTotalMembrosSchema:
        """Calcula o número total de membros de famílias Ágape ativas."""
        session = self._database.session

        quantidade_total_membros = (
            session.query(func.count(MembroAgape.id))
            .join(
                FamiliaAgape,
                MembroAgape.fk_familia_agape_id == FamiliaAgape.id,
            )
            .filter(FamiliaAgape.deletado_em.is_(None))
            .scalar()
            or 0
        )

        return NumeroTotalMembrosSchema(
            quantidade_total_membros=quantidade_total_membros
        )

    def soma_total_renda_familiar_agape(self) -> SomaTotalRendaSchema:
        session = self._database.session

        soma_total_renda = (
            session.query(func.sum(MembroAgape.renda))
            .join(
                FamiliaAgape,
                MembroAgape.fk_familia_agape_id == FamiliaAgape.id,
            )
            .filter(FamiliaAgape.deletado_em.is_(None))
            .scalar()
            or 0.0
        )

        return SomaTotalRendaSchema(soma_total_renda=float(soma_total_renda))

    def contagem_itens_estoque(self) -> ContagemItensEstoqueSchema:
        session = self._database.session
        total_em_estoque = (
            session.query(func.sum(EstoqueAgape.quantidade)).scalar() or 0
        )
        return ContagemItensEstoqueSchema(em_estoque=int(total_em_estoque))

    def ultima_acao_agape_com_itens(self) -> Optional[UltimaAcaoAgapeSchema]:
        session = self._database.session

        subquery = (
            session.query(
                ItemInstanciaAgape.fk_instancia_acao_agape_id,
                func.sum(ItemInstanciaAgape.quantidade).label(
                    'total_itens_doados'
                ),
            )
            .group_by(ItemInstanciaAgape.fk_instancia_acao_agape_id)
            .subquery()
        )

        ultima_acao = (
            session.query(
                InstanciaAcaoAgape.data_termino, subquery.c.total_itens_doados
            )
            .join(
                subquery,
                InstanciaAcaoAgape.id == subquery.c.fk_instancia_acao_agape_id,
            )
            .filter(
                InstanciaAcaoAgape.status == StatusAcaoAgapeEnum.finalizado,
                InstanciaAcaoAgape.data_termino.isnot(None),
            )
            .order_by(desc(InstanciaAcaoAgape.data_termino))
            .first()
        )

        if ultima_acao and ultima_acao.data_termino:
            return UltimaAcaoAgapeSchema(
                data=ultima_acao.data_termino.date(),
                quantidade_itens_doados=int(ultima_acao.total_itens_doados),
            )
        return None

    def ultima_entrada_estoque(self) -> Optional[UltimaEntradaEstoqueSchema]:
        session = self._database.session

        ultima_entrada = (
            session.query(AquisicaoAgape.criado_em, AquisicaoAgape.quantidade)
            .order_by(desc(AquisicaoAgape.criado_em))
            .first()
        )

        if ultima_entrada and ultima_entrada.criado_em:
            return UltimaEntradaEstoqueSchema(
                data=ultima_entrada.criado_em.date(),
                quantidade=int(ultima_entrada.quantidade),
            )
        return None

    def deletar_familia_e_membros(self, familia: FamiliaAgape) -> None:
        session = self._database.session

        # Hard delete dos membros da família
        session.query(MembroAgape).filter(
            MembroAgape.fk_familia_agape_id == familia.id
        ).delete(synchronize_session='fetch')

        familia.deletado_em = datetime.utcnow()
        session.add(familia)

    def deletar_membro(self, membro_id: UUID) -> None:
        self._database.session.query(MembroAgape).filter(
            MembroAgape.id == membro_id
        ).delete(synchronize_session='fetch')

    def atualizar_endereco_familia(
        self,
        familia: FamiliaAgape,
        dados_endereco: EditarEnderecoFamiliaAgapeRequest,
        coordenadas: Optional[CoordenadasSchema],
    ) -> FamiliaAgape:
        session = self._database.session

        endereco_obj = None
        if familia.fk_endereco_id:
            endereco_obj = session.query(Endereco).get(familia.fk_endereco_id)

        if not endereco_obj:
            endereco_obj = Endereco()
            session.add(endereco_obj)
            session.flush()
            familia.fk_endereco_id = endereco_obj.id
            session.add(familia)

        endereco_obj.codigo_postal = dados_endereco.cep
        endereco_obj.logradouro = dados_endereco.rua
        endereco_obj.numero = dados_endereco.numero
        endereco_obj.complemento = dados_endereco.complemento
        endereco_obj.bairro = dados_endereco.bairro
        endereco_obj.cidade = dados_endereco.cidade
        endereco_obj.estado = dados_endereco.estado
        endereco_obj.obriga_atualizar_endereco = False

        session.add(endereco_obj)

        if coordenadas:
            coordenada_obj = endereco_obj.coordenada
            coordenada_obj = Coordenada(
                fk_endereco_id=endereco_obj.id,
                latitude=coordenadas.latitude,
                longitude=coordenadas.longitude,
                latitude_ne=coordenadas.latitude_ne,
                longitude_ne=coordenadas.longitude_ne,
                latitude_so=coordenadas.latitude_so,
                longitude_so=coordenadas.longitude_so,
            )
            session.add(coordenada_obj)

        return familia

    def atualizar_membro_agape(self, membro_agape: MembroAgape) -> MembroAgape:
        try:
            self._database.session.add(membro_agape)
            self._database.session.commit()
            self._database.session.refresh(membro_agape)
        except Exception as e:
            self._database.session.rollback()
            raise e
        return membro_agape

    def listar_familias_beneficiadas_por_ciclo_id(
        self, ciclo_acao_id: UUID
    ) -> list[FamiliaAgape]:
        instancias = (
            self._database.session.query(FamiliaAgape)
            .distinct()
            .join(
                DoacaoAgape, FamiliaAgape.id == DoacaoAgape.fk_familia_agape_id
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
            .filter(
                ItemInstanciaAgape.fk_instancia_acao_agape_id == ciclo_acao_id
            )
            .options(
                selectinload(FamiliaAgape.membros),
            )
        )

        return instancias.all()

    def listar_familias_com_enderecos(self) -> list[FamiliaAgape]:
        instancias = (
            self._database.session.query(FamiliaAgape)
            .filter(FamiliaAgape.deletado_em.is_(None))
            .filter(FamiliaAgape.fk_endereco_id.isnot(None))
            .order_by(FamiliaAgape.nome_familia)
        )
        return instancias.all()

    def listar_historico_movimentacoes_paginado(
        self, pagina: int, por_pagina: int
    ) -> tuple[list[tuple[HistoricoMovimentacaoAgape, str]], int]:
        offset = (pagina - 1) * por_pagina

        query_dados = (
            self._database.session.query(
                HistoricoMovimentacaoAgape,
                EstoqueAgape.item.label('nome_item'),
            )
            .join(
                EstoqueAgape,
                HistoricoMovimentacaoAgape.fk_estoque_agape_id
                == EstoqueAgape.id,
            )
            .order_by(HistoricoMovimentacaoAgape.criado_em.desc())
            .limit(por_pagina)
            .offset(offset)
        )
        resultados = query_dados.all()

        query_total = self._database.session.query(
            func.count(HistoricoMovimentacaoAgape.id)
        )

        total_itens = query_total.scalar() or 0

        return resultados, total_itens

    def listar_itens_por_doacao_agape_id(self, doacao_id: UUID) -> list:
        instancias = (
            self._database.session.query(
                EstoqueAgape.id.label('item_id'),
                EstoqueAgape.item.label('nome_item'),
                ItemDoacaoAgape.quantidade.label('quantidade_doada'),
                ItemDoacaoAgape.id.label('item_doacao_agape_id'),
                ItemDoacaoAgape.fk_item_instancia_agape_id.label(
                    'item_instancia_agape_id'
                ),
            )
            .select_from(ItemDoacaoAgape)
            .join(
                ItemInstanciaAgape,
                ItemDoacaoAgape.fk_item_instancia_agape_id
                == ItemInstanciaAgape.id,
            )
            .join(
                EstoqueAgape,
                ItemInstanciaAgape.fk_estoque_agape_id == EstoqueAgape.id,
            )
            .filter(ItemDoacaoAgape.fk_doacao_agape_id == doacao_id)
            .order_by(EstoqueAgape.item)
        )

        return instancias.all()

    def listar_itens_recebidos_por_ciclo_e_doacao_id(
        self, ciclo_acao_id: UUID, doacao_id: UUID
    ) -> list:
        instancias = (
            self._database.session.query(
                EstoqueAgape.id.label('item_id'),
                EstoqueAgape.item.label('nome_item'),
                ItemDoacaoAgape.quantidade.label('quantidade_doada'),
                ItemDoacaoAgape.id.label('item_doacao_agape_id'),
                ItemDoacaoAgape.fk_item_instancia_agape_id.label(
                    'item_instancia_agape_id'
                ),
            )
            .select_from(ItemDoacaoAgape)
            .join(
                ItemInstanciaAgape,
                ItemDoacaoAgape.fk_item_instancia_agape_id
                == ItemInstanciaAgape.id,
            )
            .join(
                EstoqueAgape,
                ItemInstanciaAgape.fk_estoque_agape_id == EstoqueAgape.id,
            )
            .filter(ItemDoacaoAgape.fk_doacao_agape_id == doacao_id)
            .filter(
                ItemInstanciaAgape.fk_instancia_acao_agape_id == ciclo_acao_id
            )
            .order_by(EstoqueAgape.item)
        )

        return instancias.all()

    def listar_voluntarios_agape(
        self, filtros: PaginacaoQuery
    ) -> tuple[list[Lead], int]:
        query = (
            self._database.session.query(Lead)
            .join(
                PermissaoLead,
                PermissaoLead.lead_id == Lead.id,
            )
            .join(Perfil, Perfil.id == PermissaoLead.lead_id)
            .filter(Perfil.nome == PerfilEnum.voluntario_agape.value)
            .order_by(Lead.nome)
        )

        paginacao = query.paginate(
            page=filtros.pagina,
            per_page=filtros.por_pagina,
            error_out=False,
        )

        return paginacao.items, paginacao.total

    def registrar_doacao_agape(self, doacao: DoacaoAgape) -> DoacaoAgape:
        self._database.session.add(doacao)
        return doacao

    def registrar_item_doacao_agape(
        self, item_doacao: ItemDoacaoAgape
    ) -> ItemDoacaoAgape:
        self._database.session.add(item_doacao)
        return item_doacao

    def buscar_item_instancia_agape_por_id(
        self, item_instancia_id: UUID
    ) -> ItemInstanciaAgape | None:
        """Busca um item de instância de ação ágape pelo seu ID."""
        return self._database.session.get(
            ItemInstanciaAgape, item_instancia_id
        )

    def atualizar_item_instancia_agape(
        self, item_instancia: ItemInstanciaAgape
    ) -> ItemInstanciaAgape:
        self._database.session.add(item_instancia)
        return item_instancia

    def buscar_lead_com_permissoes_por_id(self, lead_id: UUID) -> Lead | None:
        return (
            self._database.session.query(Lead)
            .options(
                selectinload(Lead.permissoes_lead).selectinload(
                    PermissaoLead.perfil
                )
            )
            .filter(Lead.id == lead_id)
            .one_or_none()
        )

    def buscar_perfil_por_nome(self, nome_perfil: str) -> Perfil | None:
        return (
            self._database.session.query(Perfil)
            .filter(Perfil.nome == nome_perfil)
            .one_or_none()
        )

    def remover_permissao_lead(self, permissao_lead: PermissaoLead) -> None:
        self._database.session.delete(permissao_lead)

    def adicionar_permissao_lead(
        self, lead: Lead, perfil: Perfil, lead_id: UUID, perfil_id: UUID
    ) -> PermissaoLead:
        nova_permissao = PermissaoLead(
            lead=lead, perfil=perfil, lead_id=lead_id, perfil_id=perfil_id
        )
        self._database.session.add(nova_permissao)
        return nova_permissao

    def buscar_dados_exportacao_doacoes_ciclo(
        self, ciclo_acao_id: UUID
    ) -> list[DadosCompletosDoacaoSchema]:
        MembroResponsavel = aliased(MembroAgape)

        query_results = (
            self._database.session.query(
                InstanciaAcaoAgape.id.label('ciclo_acao_id'),
                AcaoAgape.nome.label('ciclo_acao_nome'),
                InstanciaAcaoAgape.data_inicio.label('ciclo_acao_data_inicio'),
                InstanciaAcaoAgape.data_termino.label(
                    'ciclo_acao_data_termino'
                ),
                FamiliaAgape.id.label('familia_id'),
                FamiliaAgape.nome_familia.label('familia_nome'),
                FamiliaAgape.observacao.label('familia_observacao'),
                MembroResponsavel.nome.label('responsavel_familia_nome'),
                MembroResponsavel.cpf.label('responsavel_familia_cpf'),
                MembroResponsavel.telefone.label(
                    'responsavel_familia_telefone'
                ),
                DoacaoAgape.id.label('doacao_id'),
                DoacaoAgape.criado_em.label('doacao_data'),
                EstoqueAgape.item.label('item_doado_nome'),
                ItemDoacaoAgape.quantidade.label('item_doado_quantidade'),
            )
            .select_from(ItemDoacaoAgape)
            .join(
                DoacaoAgape,
                DoacaoAgape.id == ItemDoacaoAgape.fk_doacao_agape_id,
            )
            .join(
                FamiliaAgape,
                FamiliaAgape.id == DoacaoAgape.fk_familia_agape_id,
            )
            .outerjoin(
                MembroResponsavel,
                (MembroResponsavel.fk_familia_agape_id == FamiliaAgape.id)
                & (MembroResponsavel.responsavel == True),
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
                AcaoAgape, AcaoAgape.id == InstanciaAcaoAgape.fk_acao_agape_id
            )
            .join(
                EstoqueAgape,
                EstoqueAgape.id == ItemInstanciaAgape.fk_estoque_agape_id,
            )
            .filter(InstanciaAcaoAgape.id == ciclo_acao_id)
            .order_by(
                FamiliaAgape.nome_familia,
                DoacaoAgape.criado_em,
                EstoqueAgape.item,
            )
            .all()
        )

        resultados_schema = [
            DadosCompletosDoacaoSchema(**row._asdict())
            for row in query_results
        ]
        return resultados_schema

    def buscar_dados_completos_familias_agape(
        self,
    ) -> list[DadosExportacaoFamiliaSchema]:
        MembroResponsavel = aliased(MembroAgape)

        query_explicit = (
            self._database.session.query(
                FamiliaAgape, Endereco, MembroResponsavel
            )
            .outerjoin(Endereco, FamiliaAgape.fk_endereco_id == Endereco.id)
            .outerjoin(
                MembroResponsavel,
                (MembroResponsavel.fk_familia_agape_id == FamiliaAgape.id)
                & (MembroResponsavel.responsavel == True),
            )
            .options(selectinload(FamiliaAgape.membros))
            .filter(FamiliaAgape.deletado_em.is_(None))
            .order_by(FamiliaAgape.nome_familia)
        )

        resultados_tuplas = query_explicit.all()

        resultados_schema = []
        for familia_ent, endereco_ent, responsavel_ent in resultados_tuplas:
            num_membros = (
                len(familia_ent.membros) if familia_ent.membros else 0
            )
            renda_total = (
                sum(m.renda for m in familia_ent.membros if m.renda)
                if familia_ent.membros
                else 0.0
            )

            schema_data = DadosExportacaoFamiliaSchema(
                familia_id=familia_ent.id,
                familia_nome=familia_ent.nome_familia,
                familia_data_cadastro=familia_ent.criado_em,
                familia_status='Ativa',
                familia_observacao=familia_ent.observacao,
                endereco_logradouro=(
                    endereco_ent.logradouro if endereco_ent else None
                ),
                endereco_numero=endereco_ent.numero if endereco_ent else None,
                endereco_complemento=(
                    endereco_ent.complemento if endereco_ent else None
                ),
                endereco_bairro=endereco_ent.bairro if endereco_ent else None,
                endereco_cidade=endereco_ent.cidade if endereco_ent else None,
                endereco_estado=endereco_ent.estado if endereco_ent else None,
                endereco_cep=(
                    endereco_ent.codigo_postal if endereco_ent else None
                ),
                responsavel_nome=(
                    responsavel_ent.nome if responsavel_ent else None
                ),
                responsavel_cpf=(
                    responsavel_ent.cpf if responsavel_ent else None
                ),
                responsavel_telefone=(
                    responsavel_ent.telefone if responsavel_ent else None
                ),
                responsavel_email=(
                    responsavel_ent.email if responsavel_ent else None
                ),
                responsavel_data_nascimento=(
                    responsavel_ent.data_nascimento
                    if responsavel_ent
                    else None
                ),
                responsavel_funcao_familiar=(
                    responsavel_ent.funcao_familiar
                    if responsavel_ent
                    else None
                ),
                responsavel_escolaridade=(
                    responsavel_ent.escolaridade if responsavel_ent else None
                ),
                responsavel_ocupacao=(
                    responsavel_ent.ocupacao if responsavel_ent else None
                ),
                numero_total_membros=num_membros,
                renda_familiar_total_estimada=renda_total,
                comprovante_residencia_url=familia_ent.comprovante_residencia,
                cadastrada_por_usuario_id=familia_ent.cadastrada_por,
            )
            resultados_schema.append(schema_data)

        return resultados_schema

    def registrar_recibo_agape(self, recibo_agape: ReciboAgape) -> ReciboAgape:
        self._database.session.add(recibo_agape)
        return recibo_agape

    def buscar_doacao_agape_por_id(self, doacao_id) -> DoacaoAgape | None:
        """
        Retorna uma doação ágape
        """
        instancia = self._database.session.get(DoacaoAgape, doacao_id)

        return instancia

    def listar_leads_por_nomes_de_perfis(
        self, nomes_perfis: list[str], filtros_paginacao: PaginacaoQuery
    ) -> tuple[list[Lead], int]:
        query = (
            self._database.session.query(Lead)
            .join(Lead.permissoes_lead)
            .join(PermissaoLead.perfil)
            .filter(Perfil.nome.in_(nomes_perfis))
            .options(
                selectinload(Lead.permissoes_lead).selectinload(
                    PermissaoLead.perfil
                )
            )
            .order_by(Lead.nome)
        )

        count_query = (
            self._database.session.query(func.count(distinct(Lead.id)))
            .join(Lead.permissoes_lead)
            .join(PermissaoLead.perfil)
            .filter(Perfil.nome.in_(nomes_perfis))
        )
        total = count_query.scalar() or 0

        paginated_query = query.limit(filtros_paginacao.por_pagina).offset(
            (filtros_paginacao.pagina - 1) * filtros_paginacao.por_pagina
        )

        leads = paginated_query.all()

        return leads, total

    def buscar_permissoes_por_lead_id(
        self, lead_id: UUID
    ) -> PermissaoLead | None:
        return self._database.session.query(PermissaoLead).filter(
            PermissaoLead.lead_id == lead_id
        )
