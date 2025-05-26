from datetime import datetime
from uuid import UUID

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, select, func # Added func

from acutis_api.communication.requests.agape import (
    CoordenadaFormData,
    EnderecoAgapeFormData,
    RegistrarItemCicloAcaoAgapeFormData,
)
from acutis_api.domain.entities.acao_agape import AcaoAgape
from acutis_api.domain.entities.coordenada import Coordenada
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
# ItemInstanciaAgape is already imported below
from acutis_api.domain.entities.item_instancia_agape import ItemInstanciaAgape
# MembroAgape is already imported below
from acutis_api.domain.entities.membro_agape import MembroAgape
# FamiliaAgape and FotoFamiliaAgape are already imported
# HttpNotFoundError is already imported

# Assuming these paths based on instructions, will verify if entities exist
from acutis_api.domain.entities.doacao_agape import DoacaoAgape 
from acutis_api.domain.entities.item_doacao_agape import ItemDoacaoAgape
from acutis_api.domain.repositories.agape import (
    AgapeRepositoryInterface,
)
from acutis_api.domain.repositories.schemas.agape import (
    DoacaoAgapeSchema,
    EstoqueAgapeSchema,
    FotoFamiliaAgapeSchema,
    ListarCicloAcoesAgapeFiltros,
    ListarItensEstoqueAgapeFiltros,
    ListarNomesAcoesAgapeFiltros,
    MembroFamiliaSchema,
    NomeAcaoAgapeSchema,
    RegistrarCicloAcaoAgapeScheme,
    RegistrarFamiliaAgapeSchema,
    RegistrarItemEstoqueAgapeSchema,
    RegistrarNomeAcaoAgapeSchema,
    ListarMembrosFamiliaAgapeFiltros,
)
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
    
    def listar_familias(
        self, filtros
    ) -> tuple[list[FamiliaAgape], int]:
        
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

    def buscar_familia_por_id(self, familia_id: UUID) -> FamiliaAgape:
        """
        Retorna a instância da família pelo ID da instância.
        """
        instancia = self._database.session.get(FamiliaAgape, familia_id)

        if instancia is None:
            raise HttpNotFoundError(f'Família {familia_id} não encontrada.')

        return instancia

    def buscar_membro_familia_por_id(self, membro_id: UUID) -> FamiliaAgape:
        """
        Retorna a instância de um membro da família pelo ID da instância.
        """
        instancia = self._database.session.get(MembroAgape, membro_id)

        if instancia is None:
            raise HttpNotFoundError('Membro da família não encontrado.')

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

    def adicionar_voluntario_agape(self, lead_id: UUID) -> None:
        """
        Adiciona um voluntário ao ciclo de ação Ágape.
        """
        session = self._database.session

        # Verifica se o voluntário já está cadastrado
        if not session.query(MembroAgape).filter_by(id=lead_id).first():
            raise HttpNotFoundError(f'Voluntário {lead_id} não encontrado.')

    def buscar_familia_agape_por_id(self, familia_id: UUID) -> FamiliaAgape | None:
        instancia = self._database.session.get(FamiliaAgape, familia_id)
        if instancia is None:
            raise HttpNotFoundError(f'Família ágape {familia_id} não encontrada.')
        if hasattr(instancia, 'deletado_em') and instancia.deletado_em is not None:
            raise HttpNotFoundError(f'Família ágape {familia_id} não encontrada (deletada).')
        return instancia

    def buscar_endereco_por_id(self, endereco_id: UUID) -> Endereco | None:
        instancia = self._database.session.get(Endereco, endereco_id)
        if instancia is None:
            raise HttpNotFoundError(f'Endereço {endereco_id} não encontrado.')
        return instancia

    def buscar_instancia_acao_agape_por_id(self, ciclo_acao_id: UUID) -> InstanciaAcaoAgape | None:
        '''Busca uma instância de ciclo de ação ágape pelo seu ID.'''
        instancia = self._database.session.get(InstanciaAcaoAgape, ciclo_acao_id)
        
        # A entidade InstanciaAcaoAgape em acutis_new não possui campo 'deletado_em' explícito.
        # Portanto, se 'instancia' for None, ela não foi encontrada.
        if instancia is None:
            raise HttpNotFoundError(f'Ciclo de ação ágape com ID {ciclo_acao_id} não encontrado.')
            
        return instancia

    def buscar_ultima_instancia_por_nome_acao_id(self, nome_acao_id: UUID) -> InstanciaAcaoAgape | None:
        '''Busca a última instância de ciclo de ação ágape (mais recente) associada a um nome de ação específico.'''
        instancia = (
            self._database.session.query(InstanciaAcaoAgape)
            .filter(InstanciaAcaoAgape.fk_acao_agape_id == nome_acao_id)
            .order_by(desc(InstanciaAcaoAgape.criado_em)) # Ordena pela data de criação para pegar a mais recente
            .first()
        )
        
        # Não levanta erro se não encontrar, apenas retorna None. O caso de uso tratará isso.
        return instancia

    def buscar_membro_por_cpf(self, cpf: str) -> MembroAgape | None:
        '''Busca um membro ágape pelo seu CPF.'''
        # A entidade MembroAgapeEntity armazena CPF como string, a comparação direta é usada.
        # O tratamento de CPF (limpeza de caracteres) deve ocorrer antes de chamar este método, se necessário.
        membro = self._database.session.query(MembroAgape).filter(MembroAgape.cpf == cpf).first()
        return membro

    def listar_fotos_por_familia_id(self, familia_id: UUID) -> list[FotoFamiliaAgape]:
        '''Lista todas as fotos de uma família ágape.'''
        fotos = (
            self._database.session.query(FotoFamiliaAgape)
            .filter(FotoFamiliaAgape.fk_familia_agape_id == familia_id)
            .all()
        )
        return fotos

    def buscar_data_ultimo_recebimento_familia_no_ciclo(self, familia_id: UUID, ciclo_acao_id: UUID) -> datetime | None:
        '''Busca a data da última doação recebida por uma família em um ciclo de ação específico.'''
        # Esta query é baseada na lógica do acutis_old, adaptada para SQLAlchemy com entidades do acutis_new
        # DoacaoAgape.criado_em é o que queremos maximizar.
        # Junção: DoacaoAgape -> ItemDoacaoAgape -> ItemInstanciaAgape
        
        data_maxima = (
            self._database.session.query(func.max(DoacaoAgape.criado_em))
            .join(ItemDoacaoAgape, ItemDoacaoAgape.fk_doacao_agape_id == DoacaoAgape.id)
            .join(ItemInstanciaAgape, ItemInstanciaAgape.id == ItemDoacaoAgape.fk_item_instancia_agape_id)
            .filter(
                DoacaoAgape.fk_familia_agape_id == familia_id,
                ItemInstanciaAgape.fk_instancia_acao_agape_id == ciclo_acao_id
            )
            .scalar_one_or_none() # Retorna o valor máximo ou None se não houver doações
        )
        return data_maxima

    def buscar_membro_agape_por_id(self, membro_agape_id: UUID) -> MembroAgape | None:
        '''Busca um membro ágape pelo seu ID, considerando soft delete se aplicável.'''
        # A entidade MembroAgape em acutis_new herda de ModeloBase, que NÃO tem 'deletado_em'.
        # Portanto, a busca é direta. Se não encontrado, levanta HttpNotFoundError.
        membro = self._database.session.get(MembroAgape, membro_agape_id)
        if not membro:
            # Para consistência com outros métodos de busca por ID que levantam erro no repo.
            raise HttpNotFoundError(f"Membro Ágape com ID {membro_agape_id} não encontrado.")
        return membro

    def buscar_membro_por_email(self, email: str) -> MembroAgape | None:
        '''Busca um membro ágape pelo seu email.'''
        # MembroAgape não tem 'deletado_em', então a busca é direta.
        # Retorna None se não encontrado; o UseCase tratará o HttpNotFoundError ou ConflictError.
        membro = self._database.session.query(MembroAgape).filter(MembroAgape.email == email).first()
        return membro

    def registrar_membro_agape(self, membro: MembroAgape) -> MembroAgape:
        '''Registra um novo membro ágape na sessão do banco de dados.
           Não faz commit, apenas adiciona à sessão e retorna a entidade.
        '''
        self._database.session.add(membro)
        # self._database.session.flush() # Opcional
        return membro