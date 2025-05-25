import logging
from typing import Optional
from flask import Blueprint, jsonify
from pydantic import BaseModel
from spectree import Response
from sqlalchemy.orm import sessionmaker

from builder import api, db
from models.enderecos import LogBairro, LogLogradouro, LogLocalidade
from utils.response import DefaultErrorResponseSchema

services_controller = Blueprint(
    "services_controller", __name__, url_prefix="/services"
)


class CepResponseSchema(BaseModel):
    cep: str
    estado: str
    cidade: str
    bairro: Optional[str]
    rua: str


@services_controller.get("/search-cep/<cep>")
@api.validate(
    resp=Response(
        HTTP_200=CepResponseSchema,
        HTTP_400=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    security={},
    tags=["Serviços"],
)
def search_cep(cep):
    """
    Busca o endereço do usuário pelo CEP.
    """
    try:
        cep = cep.replace("-", "")

        engine = db.get_engine("enderecos")
        Session = sessionmaker(bind=engine)

        with Session() as session:
            logradouro = (
                session.query(LogLogradouro).filter_by(cep=cep).first()
            )

            if logradouro:
                localidade = (
                    session.query(LogLocalidade)
                    .filter_by(
                        ufe_sg=logradouro.ufe_sg, loc_nu=logradouro.loc_nu
                    )
                    .first()
                )
                bairro = (
                    None
                    if cep.endswith("000")
                    else session.query(LogBairro)
                    .filter_by(
                        bai_nu=logradouro.bai_nu_ini, loc_nu=localidade.loc_nu
                    )
                    .first()
                )
            else:
                localidade = (
                    session.query(LogLocalidade).filter_by(cep=cep).first()
                )
                if not localidade:
                    return (
                        jsonify(error="CEP não encontrado na base de dados."),
                        404,
                    )
                bairro = None

            return (
                jsonify(
                    {
                        "cep": cep,
                        "estado": (
                            logradouro.ufe_sg
                            if logradouro
                            else localidade.ufe_sg
                        ),
                        "cidade": localidade.loc_no,
                        "bairro": bairro.bai_no if bairro else "",
                        "rua": (
                            f"{logradouro.tlo_tx} {logradouro.log_no}"
                            if logradouro
                            else ""
                        ),
                    }
                ),
                200,
            )
    except Exception as e:
        logging.exception(e)
        return jsonify(error="Ocorreu um erro ao buscar o endereço."), 500
