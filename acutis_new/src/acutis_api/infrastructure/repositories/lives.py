import uuid
from datetime import date

from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date, case, cast, extract, func, select

from acutis_api.communication.enums.lives import (
    DiaSemanaEnum,
    TipoProgramacaoLiveEnum,
)
from acutis_api.communication.requests.lives import (
    FiltrosLivesRecorrentes,
    ObterCanalRequest,
    ObterHistogramaLiveRequest,
    ObterLivesProgramadasRequest,
    ObterTodasLivesAvulsasRequest,
)
from acutis_api.communication.schemas.lives import CriarCanalSchema
from acutis_api.domain.entities.audiencia_live import AudienciaLive
from acutis_api.domain.entities.live import Live
from acutis_api.domain.entities.live_avulsa import LiveAvulsa
from acutis_api.domain.entities.live_recorrente import LiveRecorrente
from acutis_api.domain.repositories.lives import LivesRepositoryInterface
from acutis_api.domain.repositories.schemas.lives import (
    ObterAudienciaLivesSchema,
)


class LivesRepository(LivesRepositoryInterface):
    def __init__(self, database: SQLAlchemy):
        self.__database = database

    def salvar_dados(self):
        self.__database.session.commit()

    def criar_canal(self, request: CriarCanalSchema):
        novo_canal = Live(
            tag=request.tag,
            fk_campanha_id=request.campanha_id,
            rede_social=request.rede_social.lower(),
            criado_por=current_user.membro.id,
        )
        self.__database.session.add(novo_canal)
        return novo_canal

    def checar_existencia_canal(self, tag: str, rede_social: str) -> bool:
        return (
            self.__database.session.query(Live)
            .filter(Live.tag == tag, Live.rede_social == rede_social)
            .first()
        )

    def obter_canal(self, filtro: ObterCanalRequest):
        filtros = []

        if filtro.tag is not None:
            filtros.append(Live.tag == filtro.tag)
        if filtro.rede_social is not None:
            filtros.append(Live.rede_social == filtro.rede_social)

        consulta = (self.__database.session.query(Live).filter(*filtros)).all()
        return consulta

    def registrar_live_avulsa(self, dados_live_avulsa):
        db_lives_avulsas = [LiveAvulsa(**live) for live in dados_live_avulsa]
        self.__database.session.add_all(db_lives_avulsas)

    def registrar_live_recorrente(self, dados_live_recorrente):
        db_lives_recorrentes = [
            LiveRecorrente(**live) for live in dados_live_recorrente
        ]
        self.__database.session.add_all(db_lives_recorrentes)

    def obter_lives_programadas(self, filtros: ObterLivesProgramadasRequest):
        FORMATO_DATA = '%d/%m/%Y'
        FORMATO_HORA = '%H:%M'

        resultado = []

        tipo = filtros.tipo_programacao
        buscar_avulsas = tipo is None or tipo == TipoProgramacaoLiveEnum.AVULSA
        buscar_recorrentes = tipo is None or tipo == (
            TipoProgramacaoLiveEnum.RECORRENTE
        )

        if buscar_avulsas:
            query = select(LiveAvulsa, Live).join(
                Live, LiveAvulsa.fk_live_id == Live.id
            )

            if filtros.rede_social:
                query = query.filter(Live.rede_social == filtros.rede_social)

            for live_avulsa, live in self.__database.session.execute(
                query
            ).all():
                dados_especificos = {
                    'id': live_avulsa.id,
                    'data': live_avulsa.data_hora_inicio.strftime(
                        FORMATO_DATA
                    ),
                    'hora': live_avulsa.data_hora_inicio.strftime(
                        FORMATO_HORA
                    ),
                }
                resultado.append({
                    **dados_especificos,
                    'rede_social': live.rede_social,
                    'tag': live.tag,
                    'tipo_programacao': TipoProgramacaoLiveEnum.AVULSA.value,
                })

        if buscar_recorrentes:
            query = select(LiveRecorrente, Live).join(
                Live, LiveRecorrente.fk_live_id == Live.id
            )

            if filtros.rede_social:
                query = query.filter(Live.rede_social == filtros.rede_social)

            if filtros.filtro_dias_semana:
                dias_filtrados = [
                    dia.value for dia in filtros.filtro_dias_semana
                ]
                query = query.filter(
                    LiveRecorrente.dia_semana.in_(dias_filtrados)
                )

                ordenacao = case(
                    [
                        (LiveRecorrente.dia_semana == dia, pos)
                        for dia, pos in DiaSemanaEnum.ordem_dias().items()
                    ],
                    else_=8,
                )
                query = query.order_by(ordenacao)

            for live_recorrente, live in self.__database.session.execute(
                query
            ).all():
                dados_especificos = {
                    'id': live_recorrente.id,
                    'data': live_recorrente.dia_semana.title(),
                    'hora': live_recorrente.hora_inicio.strftime(FORMATO_HORA),
                }
                resultado.append({
                    **dados_especificos,
                    'rede_social': live.rede_social,
                    'tag': live.tag,
                    'tipo_programacao': (
                        TipoProgramacaoLiveEnum.RECORRENTE.value
                    ),
                })

        return resultado

    def editar_programacao_live(
        self, programacao_id, tipo_programacao, **kwargs
    ):
        if tipo_programacao == TipoProgramacaoLiveEnum.AVULSA:
            live = self.__database.session.get(LiveAvulsa, programacao_id)
            if not live:
                return None
            live.data_hora_inicio = kwargs['data_hora_inicio']
        elif tipo_programacao == TipoProgramacaoLiveEnum.RECORRENTE:
            live = self.__database.session.get(LiveRecorrente, programacao_id)
            if not live:
                return None
            live.dia_semana = kwargs['dia_semana'].lower()
            live.hora_inicio = kwargs['hora_inicio']
        else:
            return None

        self.__database.session.add(live)
        return live

    def buscar_programacao_por_id(
        self, programacao_id: uuid.UUID, model: LiveAvulsa | LiveRecorrente
    ):
        return self.__database.session.get(model, programacao_id)

    def deletar_programacao_live(self, programacao):
        self.__database.session.delete(programacao)

    def obter_live_por_id(self, live_id: uuid.UUID) -> Live | None:
        return (
            self.__database.session.query(Live)
            .filter_by(id=live_id)
            .one_or_none()
        )

    def obter_todas_lives_recorrentes(self, filtros: FiltrosLivesRecorrentes):
        query = (
            self.__database.session.query(LiveRecorrente)
            .join(Live, Live.id == LiveRecorrente.fk_live_id)
            .order_by(LiveRecorrente.hora_inicio)
        )

        if filtros.tag:
            query = query.filter(Live.tag.ilike(f'%{filtros.tag}%'))

        if filtros.rede_social:
            query = query.filter(
                Live.rede_social.ilike(f'%{filtros.rede_social}%')
            )

        if filtros.hora_inicio:
            query = query.filter(
                LiveRecorrente.hora_inicio >= filtros.hora_inicio
            )

        if filtros.dia_semana:
            query = query.filter(
                LiveRecorrente.dia_semana == filtros.dia_semana
            )

        return query.paginate(
            page=filtros.pagina,
            per_page=filtros.por_pagina,
            error_out=False,
        )

    def obter_todas_lives_avulsas(
        self, filtros: ObterTodasLivesAvulsasRequest
    ):
        query = self.__database.session.query(LiveAvulsa).join(
            Live, Live.id == LiveAvulsa.fk_live_id
        )

        if filtros.tag:
            query = query.filter(Live.tag.like(f'%{filtros.tag}%'))
        if filtros.rede_social:
            query = query.filter(
                Live.rede_social.like(f'%{filtros.rede_social}%')
            )
        if filtros.data_hora_inicio:
            query = query.filter(
                LiveAvulsa.data_hora_inicio >= filtros.data_hora_inicio
            )

        query = query.order_by(LiveAvulsa.data_hora_inicio)

        return query.paginate(
            page=filtros.pagina,
            per_page=filtros.por_pagina,
            error_out=False,
        )

    def obter_audiencia_lives(self, requisicao: ObterAudienciaLivesSchema):
        query = (
            self.__database.session.query(AudienciaLive)
            .filter(AudienciaLive.fk_live_id == requisicao.live_id)
            .order_by(AudienciaLive.data_hora_registro.asc())
        )

        if requisicao.data_inicial:
            query = query.filter(
                AudienciaLive.data_hora_registro >= requisicao.data_inicial
            )
        if requisicao.data_final:
            query = query.filter(
                AudienciaLive.data_hora_registro <= requisicao.data_final
            )

        return query.all()

    def obter_datas_lives_ocorridas(self) -> list[date]:
        query = (
            self.__database.session.query(
                cast(AudienciaLive.data_hora_registro, Date).label(
                    'data_hora_registro'
                )
            )
            .distinct()
            .all()
        )
        return [row.data_hora_registro for row in query]

    def obter_dados_histograma(
        self, request: ObterHistogramaLiveRequest
    ) -> dict:
        query = (
            self.__database.session.query(
                AudienciaLive.titulo,
                cast(AudienciaLive.data_hora_registro, Date).label('data'),
                extract('hour', AudienciaLive.data_hora_registro).label(
                    'hora'
                ),
                extract('minute', AudienciaLive.data_hora_registro).label(
                    'minuto'
                ),
                func.sum(AudienciaLive.audiencia).label('audiencia_total'),
            )
            .join(Live, Live.id == AudienciaLive.fk_live_id)
            .filter(AudienciaLive.titulo == request.filtro_titulo_live)
        )

        if request.filtro_rede_social:
            query = query.filter(
                Live.rede_social == request.filtro_rede_social
            )

        query = query.group_by(
            AudienciaLive.titulo,
            cast(AudienciaLive.data_hora_registro, Date),
            extract('hour', AudienciaLive.data_hora_registro),
            extract('minute', AudienciaLive.data_hora_registro),
        )

        dados_agrupados = query.all()

        redes_sociais = (
            self.__database.session.query(
                Live.rede_social,
                func.sum(AudienciaLive.audiencia).label('total_audiencia'),
            )
            .join(AudienciaLive, Live.id == AudienciaLive.fk_live_id)
            .filter(AudienciaLive.titulo == request.filtro_titulo_live)
        )

        if request.filtro_rede_social:
            redes_sociais = redes_sociais.filter(
                Live.rede_social == request.filtro_rede_social
            )

        redes_sociais = redes_sociais.group_by(Live.rede_social).all()

        return {
            'dados_agrupados': dados_agrupados,
            'redes_sociais': redes_sociais,
        }
