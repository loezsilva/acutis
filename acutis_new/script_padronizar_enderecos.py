from sqlalchemy.orm import Session

from acutis_api.api.app import app
from acutis_api.domain.entities.endereco import Endereco
from acutis_api.domain.entities.enderecos.log_logradouro import LogLogradouro
from acutis_api.infrastructure.extensions import database


def script_padronizar_enderecos():
    with app.app_context():
        enderecos = database.session.query(Endereco).all()
        engine = database.engines['enderecos']

        with Session(engine) as log_session:
            cep_cache = {}
            atualizados = 0

            for endereco in enderecos:
                cep = endereco.codigo_postal

                if cep in cep_cache:
                    logradouro = cep_cache[cep]
                else:
                    logradouro = log_session.scalar(
                        database.select(LogLogradouro).where(
                            LogLogradouro.cep == cep,
                        )
                    )
                    cep_cache[cep] = logradouro

                if logradouro:
                    endereco.estado = logradouro.ufe_sg
                    atualizados += 1
                    print(
                        f'Atualizado: CEP {cep} -> Estado {logradouro.ufe_sg}'
                    )
                    print(atualizados)
            try:
                database.session.commit()
                print(f'{atualizados} endereços atualizados com sucesso.')
            except Exception as e:
                database.session.rollback()
                print(f'Erro ao fazer commit das alterações: {e}')
                raise e


script_padronizar_enderecos()
