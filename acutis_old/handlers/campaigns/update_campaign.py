from datetime import datetime
import json
from flask import request
from flask_jwt_extended import current_user
import logging

from exceptions.error_types.http_not_found import NotFoundError
from exceptions.error_types.http_unprocessable_entity import (
    HttpUnprocessableEntity,
)
from exceptions.exception_itau import ItauChavePixWebhookException
from handlers.campaigns.landing_pages.create_landing_page import (
    CreateLandingPage,
)
from handlers.campaigns.landing_pages.update_landing_page import (
    UpdateLandingPage,
)
from models.campanha import Campanha
from builder import db
from models.landpage import LandPage
from models.setup_pagamento import SetupPagamento
from services.factories import file_service_factory
from services.itau_api import ItauAPI


class UpdateCampaign:
    def __init__(self, fk_campanha_id: int) -> None:
        self.__fk_campanha_id = fk_campanha_id

    def execute(self) -> None:
        return self.__update_campaign()

    def __update_campaign(self):
        try:

            campanha = self.__verify_campaing()

            data = request.form.get("data")
            payload = json.loads(data)

            imagem_capa = request.files.get("imagem_capa")

            titulo = payload["titulo"]
            descricao = payload.get("descricao")
            data_inicio = payload.get("data_inicio")
            data_fim = payload.get("data_fim")
            valor_meta = payload.get("valor_meta")
            prorrogado = payload.get("prorrogado")
            data_prorrogacao = payload.get("data_prorrogacao")
            valor_total_atingido = payload.get("valor_total_atingido")
            data_fechamento_campanha = payload.get("data_fechamento_campanha")
            status = payload["status"]
            chave_pix = (
                payload["chave_pix"].strip()
                if campanha.objetivo == "doacao"
                else payload.get("chave_pix")
            )
            publica = payload["publica"]
            duracao = payload.get("duracao")
            cadastros_meta = payload.get("cadastros_meta")
            preenchimento_foto = payload.get("preenchimento_foto", False)
            label_foto = payload["label_foto"] if preenchimento_foto else None
            cadastrar_landing_page = payload.get(
                "cadastrar_landing_page", False
            )

            if chave_pix:
                self.__registra_chave_pix_webhook_itau(chave_pix)

            if campanha.duracao == "permanente":
                data_fim = None
                data_inicio = None

            campanha.titulo = titulo
            campanha.descricao = descricao
            campanha.data_inicio = data_inicio
            campanha.data_fim = data_fim
            campanha.valor_meta = valor_meta
            campanha.prorrogado = prorrogado
            campanha.data_prorrogacao = data_prorrogacao
            campanha.valor_total_atingido = valor_total_atingido
            campanha.data_fechamento_campanha = data_fechamento_campanha
            campanha.status = status
            campanha.chave_pix = chave_pix
            campanha.data_alteracao = datetime.now()
            campanha.usuario_alteracao = current_user["id"]
            campanha.publica = publica
            campanha.duracao = duracao
            campanha.cadastros_meta = cadastros_meta
            campanha.preenchimento_foto = preenchimento_foto
            campanha.label_foto = label_foto

            s3_client = file_service_factory()
            if imagem_capa:
                s3_client.upload_image(imagem_capa, campanha.filename)

            if campanha.objetivo == "doacao":
                credito_unico = payload["credito_unico"]
                credito_recorrente = payload["credito_recorrente"]
                pix_unico = payload["pix_unico"]
                pix_recorrente = payload["pix_recorrente"]
                boleto_unico = payload["boleto_unico"]
                boleto_recorrente = payload["boleto_recorrente"]

                setup_pagamento = SetupPagamento.query.filter_by(
                    fk_campanha_id=campanha.id
                ).first()

                if setup_pagamento is not None:
                    setup_pagamento.credito_unico = credito_unico
                    setup_pagamento.credito_recorrente = credito_recorrente
                    setup_pagamento.pix_unico = pix_unico
                    setup_pagamento.pix_recorrente = pix_recorrente
                    setup_pagamento.boleto_unico = boleto_unico
                    setup_pagamento.boleto_recorrente = boleto_recorrente
                    setup_pagamento.data_alteracao = datetime.now()
                    setup_pagamento.usuario_alteracao = current_user["id"]
                else:
                    data_setup_pagamento = {
                        "fk_campanha_id": campanha.id,
                        "credito_unico": credito_unico,
                        "credito_recorrente": credito_recorrente,
                        "pix_unico": pix_unico,
                        "pix_recorrente": pix_recorrente,
                        "boleto_unico": boleto_unico,
                        "boleto_recorrente": boleto_recorrente,
                        "usuario_criacao": current_user["id"],
                    }

                    setup = SetupPagamento(**data_setup_pagamento)
                    db.session.add(setup)

            landing_page = LandPage.query.filter_by(
                campanha_id=campanha.id
            ).first()
            if landing_page is not None:
                update_landing_page = UpdateLandingPage(landing_page)
                update_landing_page.execute()

            elif cadastrar_landing_page:
                create_landing_page = CreateLandingPage(campanha.id)
                create_landing_page.execute()

            db.session.commit()

            response = {"msg": "Campanha atualizada com sucesso."}, 200

            return response

        except KeyError as err:
            response = {"error": f"O campo {str(err)} é obrigatório."}, 400

            return response

        except Exception as err:
            logging.error(f"{type(err)} - {err}")
            db.session.rollback()
            raise HttpUnprocessableEntity(
                "Ocorreu um erro ao atualizar o cadastro da campanha."
            )

    def __verify_campaing(self):
        campanha = db.session.get(Campanha, self.__fk_campanha_id)
        if not campanha:
            raise NotFoundError("Campaha não encontrada")
        return campanha

    def __registra_chave_pix_webhook_itau(self, chave_pix: str) -> None:
        itau_api = ItauAPI("pix")
        path = f"/webhook/{chave_pix}"

        _, status_code = itau_api.get(path)
        if status_code != 200:
            body = {
                "webhookUrl": "https://api-acutis.institutohesed.org.br/webhook/itau"
            }
            response, status = itau_api.put(path, body)
            if status not in [200, 201, 204]:
                logging.error(
                    f"OCORREU UM ERRO AO CADASTRAR A CHAVE PIX NO WEBHOOK: {response}"
                )
                raise ItauChavePixWebhookException(
                    response.get("violacoes", {}).get(
                        "razao", "A chave pix é inválida."
                    ),
                    response.get("status", 400),
                )
