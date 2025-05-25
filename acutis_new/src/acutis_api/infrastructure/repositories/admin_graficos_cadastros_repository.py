from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import case, func, literal_column, select, text

from acutis_api.application.utils.funcoes_auxiliares import (
    quantidade_meses_entre_datas,
)
from acutis_api.domain.entities.benfeitor import Benfeitor
from acutis_api.domain.entities.campanha import Campanha
from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.entities.lead_campanha import LeadCampanha
from acutis_api.domain.entities.membro import Membro
from acutis_api.domain.repositories.admin_graficos_cadastros import (
    GraficosCadastrosRepositoryInterface,
)
from acutis_api.domain.repositories.schemas.admin_graficos_cadastros import (
    ResumoQuantidadeRegistrosSchema,
)


class GraficosCadastrosRepository(GraficosCadastrosRepositoryInterface):
    def __init__(self, database: SQLAlchemy):
        self.__database = database

    def quantidade_leads_mes_atual(self) -> int:
        return (
            self.__database.session.query(
                func.count(Lead.id).label('quantidade_leads_mes_atual')
            )
            .filter(func.month(Lead.criado_em) == func.month(func.now()))
            .filter(func.year(Lead.criado_em) == func.year(func.now()))
            .scalar()
        )

    def media_mensal_leads(self) -> int:
        data_primeiro_lead = self.__database.session.query(
            func.min(Lead.criado_em)
        ).scalar()

        quantidade_lead_total = self.__database.session.query(
            func.count(Lead.id).label('quantidade_leads_mes_atual')
        ).scalar()

        quantidade_meses = quantidade_meses_entre_datas(
            data_primeiro_lead, datetime.now()
        )

        media_mensal = quantidade_lead_total / quantidade_meses

        return int(media_mensal)

    def quantidade_membros_mes_atual(self) -> int:
        return (
            self.__database.session.query(func.count(Membro.id))
            .filter(func.month(Membro.criado_em) == func.month(func.now()))
            .filter(func.year(Membro.criado_em) == func.year(func.now()))
            .scalar()
        )

    def quantidade_membros_dia_atual(self) -> int:
        return (
            self.__database.session.query(func.count(Membro.id))
            .filter(func.month(Membro.criado_em) == func.month(func.now()))
            .filter(func.year(Membro.criado_em) == func.year(func.now()))
            .filter(func.day(Membro.criado_em) == func.day(func.now()))
            .scalar()
        )

    def media_mensal_membros(self) -> int:
        data_primeiro_membro = self.__database.session.query(
            func.min(Membro.criado_em)
        ).scalar()

        quantidade_membro_total = self.__database.session.query(
            func.count(Membro.id)
        ).scalar()

        quantidade_meses = quantidade_meses_entre_datas(
            data_primeiro_membro, datetime.now()
        )

        media_mensal = quantidade_membro_total / quantidade_meses

        return int(media_mensal)

    def media_diaria_membros(self) -> tuple:
        data_primeiro_membro = self.__database.session.query(
            func.min(Membro.criado_em)
        ).scalar()

        quantidade_membro_total = self.__database.session.query(
            func.count(Membro.id)
        ).scalar()

        return data_primeiro_membro, quantidade_membro_total

    def resumo_quantidade_registros(
        self, filtros_requisicao: ResumoQuantidadeRegistrosSchema
    ) -> tuple:
        quantidade_leads = (
            self.__database.session.query(func.count(Lead.id))
            .filter(
                Lead.criado_em.between(
                    filtros_requisicao.data_inicio, filtros_requisicao.data_fim
                )
                if (
                    filtros_requisicao.data_inicio
                    and filtros_requisicao.data_fim
                )
                else True
            )
            .scalar()
        )

        quantidade_membros = (
            self.__database.session.query(func.count(Membro.id))
            .filter(
                Membro.criado_em.between(
                    filtros_requisicao.data_inicio, filtros_requisicao.data_fim
                )
                if (
                    filtros_requisicao.data_inicio
                    and filtros_requisicao.data_fim
                )
                else True
            )
            .scalar()
        )

        quantidade_benfeitores = (
            self.__database.session.query(func.count(Benfeitor.id))
            .filter(
                Benfeitor.criado_em.between(
                    filtros_requisicao.data_inicio, filtros_requisicao.data_fim
                )
                if (
                    filtros_requisicao.data_inicio
                    and filtros_requisicao.data_fim
                )
                else True
            )
            .scalar()
        )

        return quantidade_leads, quantidade_membros, quantidade_benfeitores

    def quantidade_membros_por_genero(self) -> list:
        return (
            self.__database.session.query(
                Membro.sexo.label('genero'),
                func.count(Membro.id).label('quantidade'),
            )
            .group_by(Membro.sexo)
            .all()
        )

    def quantidade_leads_por_hora(self) -> list:
        return (
            self.__database.session.query(
                func.extract('hour', Lead.criado_em).label('hora'),
                func.count(Lead.id).label('quantidade_leads_por_hora'),
            )
            .group_by(func.extract('hour', Lead.criado_em))
            .order_by(func.extract('hour', Lead.criado_em).asc())
            .all()
        )

    def quantidade_membros_por_hora_dia_atual(self) -> list:
        return (
            self.__database.session.query(
                func.extract('hour', Membro.criado_em).label('hora'),
                func.count(Membro.id).label('quantidade_membro'),
            )
            .filter(
                func.day(Membro.criado_em) == func.day(func.now()),
                func.month(Membro.criado_em) == func.month(func.now()),
                func.year(Membro.criado_em) == func.year(func.now()),
            )
            .group_by(func.extract('hour', Membro.criado_em))
            .order_by(func.extract('hour', Membro.criado_em).asc())
            .all()
        )

    def quantidade_membros_por_dia_mes_atual(self) -> list:
        query = text("""
            SELECT
                FORMAT(criado_em, 'dd-MM-yyyy') AS dia,
                COUNT(id) AS quantidade_membros
            FROM membros
            WHERE MONTH(criado_em) = MONTH(GETDATE())
            AND YEAR(criado_em) = YEAR(GETDATE())
            GROUP BY FORMAT(criado_em, 'dd-MM-yyyy')
            ORDER BY FORMAT(criado_em, 'dd-MM-yyyy') ASC
        """)

        return self.__database.session.execute(query).all()

    def leads_por_origem(self) -> Lead:
        return (
            self.__database.session.query(
                Lead.origem_cadastro,
                func.count(Lead.id).label('quantidade'),
            )
            .group_by(Lead.origem_cadastro)
            .order_by(func.count(Lead.id).desc())
            .all()
        )

    def leads_por_dia_semana(self) -> Lead:
        return (
            self.__database.session.query(
                func.extract('weekday', Lead.criado_em).label('dia_semana'),
                func.count(Lead.id).label('quantidade'),
            )
            .group_by(func.extract('weekday', Lead.criado_em))
            .order_by(func.extract('weekday', Lead.criado_em).asc())
            .all()
        )

    def leads_por_origem_mes_atual(self) -> list:
        subquery = (
            self.__database.session.query(
                Campanha.nome.label('campanha'),
                func.convert(text('varchar(10)'), Lead.criado_em, 105).label(
                    'dia'
                ),
                Lead.id.label('lead_id'),
            )
            .join(LeadCampanha, LeadCampanha.fk_lead_id == Lead.id)
            .join(Campanha, LeadCampanha.fk_campanha_id == Campanha.id)
            .filter(
                func.extract('month', Lead.criado_em)
                == func.extract('month', func.now()),
                func.extract('year', Lead.criado_em)
                == func.extract('year', func.now()),
            )
        ).subquery('formatted_data')

        return (
            self.__database.session.query(
                subquery.c.campanha,
                subquery.c.dia,
                func.count(subquery.c.lead_id).label('quantidade'),
            )
            .group_by(subquery.c.campanha, subquery.c.dia)
            .order_by(subquery.c.dia.asc())
            .all()
        )

    def quantidade_leads_por_mes(self) -> list:
        subquery = (
            self.__database.session.query(
                func.format(Lead.criado_em, 'MM-yyyy').label('mes'),
                Lead.id.label('lead_id'),
            ).filter(
                Lead.criado_em
                >= text("""
                    DATEADD(MONTH, -11, DATEADD(MONTH, DATEDIFF(
                        MONTH, 0, GETDATE()
                    ), 0))
                """),
                Lead.criado_em
                < text("""
                    DATEADD(MONTH, 1, DATEADD(MONTH, DATEDIFF(
                        MONTH, 0, GETDATE()
                    ), 0))
                """),
            )
        ).subquery('formatted_data')

        return (
            self.__database.session.query(
                subquery.c.mes,
                func.count(subquery.c.lead_id).label('quantidade'),
            )
            .group_by(subquery.c.mes)
            .order_by(text("CONVERT(datetime, '01-' + mes, 105) ASC"))
            .all()
        )

    def quantidade_leads_total(self) -> int:
        return self.__database.session.query(
            func.count(Lead.id).label('quantidade_leads_mes_atual')
        ).scalar()

    def quantidade_membros_por_idade(self) -> list:
        subquery = (
            select(
                case(
                    (
                        func.datediff(
                            text('year'),
                            Membro.data_nascimento,
                            func.getdate(),
                        )
                        < 15,  # NOSONAR #noqa
                        'Menos de 15',
                    ),
                    (
                        func.datediff(
                            text('year'),
                            Membro.data_nascimento,
                            func.getdate(),
                        ).between(15, 24),
                        '15-24',  # NOSONAR #noqa
                    ),
                    (
                        func.datediff(
                            text('year'),
                            Membro.data_nascimento,
                            func.getdate(),
                        ).between(25, 34),
                        '25-34',  # NOSONAR #noqa
                    ),
                    (
                        func.datediff(
                            text('year'),
                            Membro.data_nascimento,
                            func.getdate(),
                        ).between(35, 44),
                        '35-44',  # NOSONAR #noqa
                    ),
                    (
                        func.datediff(
                            text('year'),
                            Membro.data_nascimento,
                            func.getdate(),
                        ).between(45, 59),
                        '45-59',  # NOSONAR #noqa
                    ),
                    (
                        func.datediff(
                            text('year'),
                            Membro.data_nascimento,
                            func.getdate(),
                        ).between(60, 74),
                        '60-74',  # NOSONAR #noqa
                    ),
                    (
                        func.datediff(
                            text('year'),
                            Membro.data_nascimento,
                            func.getdate(),
                        )
                        >= 75,  # NOSONAR #noqa
                        '75+',
                    ),
                    else_='Desconhecido',
                ).label('faixa_etaria'),
                Membro.sexo,
                Membro.id.label('membro_id'),
            )
            .select_from(Membro)
            .alias('subq')
        )

        return (
            self.__database.session.query(
                subquery.c.faixa_etaria,
                func.sum(
                    case((subquery.c.sexo == 'masculino', 1), else_=0)
                ).label('masculino'),
                func.sum(
                    case((subquery.c.sexo == 'feminino', 1), else_=0)
                ).label('feminino'),
                func.sum(case((subquery.c.sexo.is_(None), 1), else_=0)).label(
                    'nao_informado'
                ),
            )
            .group_by(subquery.c.faixa_etaria)
            .order_by(subquery.c.faixa_etaria)
            .all()
        )

    def leads_por_evolucao_mensal(self):
        format_expr = literal_column("FORMAT(leads.criado_em, 'yyyy-MM')")

        leads_por_mes = (
            self.__database.session.query(
                format_expr.label('ano_mes'),
                func.count(Lead.id).label('quantidade_mes'),
            )
            .group_by(format_expr)
            .subquery()
        )

        return (
            self.__database.session.query(
                leads_por_mes.c.ano_mes,
                func.sum(leads_por_mes.c.quantidade_mes)
                .over(
                    order_by=leads_por_mes.c.ano_mes,
                    range_=None,
                    rows=(None, 0),
                )
                .label('montante_acumulado'),
            )
            .order_by(leads_por_mes.c.ano_mes)
            .all()
        )
