from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy.orm import Session

from acutis_api.domain.entities.enderecos.log_bairro import LogBairro
from acutis_api.domain.entities.enderecos.log_localidade import LogLocalidade
from acutis_api.domain.entities.enderecos.log_logradouro import LogLogradouro
from acutis_api.domain.repositories.enderecos import (
    EnderecosRepositoryInterface,
)


class EnderecosRepository(EnderecosRepositoryInterface):
    def __init__(self, database: SQLAlchemy):
        self._database = database

    def buscar_cep(self, cep: str) -> dict | None:
        engine = self._database.engines['enderecos']

        with Session(engine) as session:
            logradouro = session.scalar(
                select(LogLogradouro).where(LogLogradouro.cep == cep)
            )

            if logradouro:
                localidade = session.scalar(
                    select(LogLocalidade).where(
                        LogLocalidade.ufe_sg == logradouro.ufe_sg,
                        LogLocalidade.loc_nu == logradouro.loc_nu,
                    )
                )
                bairro = (
                    None
                    if cep.endswith('000')
                    else session.scalar(
                        select(LogBairro).where(
                            LogBairro.bai_nu == logradouro.bai_nu_ini,
                            LogBairro.loc_nu == localidade.loc_nu,
                        )
                    )
                )
            else:
                localidade = session.scalar(
                    select(LogLocalidade).where(LogLocalidade.cep == cep)
                )
                if not localidade:
                    return None
                bairro = None

            endereco = {
                'cep': cep,
                'estado': (
                    logradouro.ufe_sg if logradouro else localidade.ufe_sg
                ),
                'cidade': localidade.loc_no,
                'bairro': bairro.bai_no if bairro else '',
                'rua': (
                    f'{logradouro.tlo_tx} {logradouro.log_no}'
                    if logradouro
                    else ''
                ),
                'tipo_logradouro': logradouro.tlo_tx,
            }

            return endereco
