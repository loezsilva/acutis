from datetime import datetime
import json
import logging
import uuid
from flask import request
from flask_jwt_extended import current_user
from python_http_client import BadRequestsError

from exceptions.errors_handler import errors_handler
from exceptions.exception_itau import ItauChavePixWebhookException
from exceptions.exception_upload_image import UploadImageException
from handlers.campaigns.landing_pages.create_landing_page import (
    CreateLandingPage,
)
from models.campanha import Campanha
from models.historico_campanha_doacoes import HistoricoCampanhaDonations
from models.setup_pagamento import SetupPagamento
from services.factories import file_service_factory
from services.itau_api import ItauAPI
from builder import db


class CreateCampaign:
    def __init__(self) -> None:
        pass

    def execute(self):
        return self.__create_campaign()

    def __create_campaign(self):
        try:
            data = request.form.get("data")
            payload = json.loads(data)

            # Validate and handle cover image
            imagem_capa = request.files.get("imagem_capa")
            if not imagem_capa:
                raise UploadImageException("Imagem de capa é obrigatória.")

            titulo = payload["titulo"]
            descricao = payload["descricao"]
            objetivo = payload["objetivo"]
            data_inicio = payload.get("data_inicio")
            data_fim = payload.get("data_fim")
            valor_meta = payload.get("valor_meta")
            prorrogado = payload.get("prorrogado")
            data_prorrogacao = payload.get("data_prorrogacao")
            valor_total_atingido = payload.get("valor_total_atingido")
            data_fechamento_campanha = payload.get("data_fechamento_campanha")
            status = payload.get("status")
            publica = payload.get("publica")
            duracao = payload.get("duracao")
            mes_ano = datetime.now().date()
            cadastros_meta = payload.get("cadastros_meta")
            preenchimento_foto = payload.get("preenchimento_foto", False)
            label_foto = payload["label_foto"] if preenchimento_foto else None
            cadastrar_landing_page = payload.get(
                "cadastrar_landing_page", False
            )
            chave_pix = (
                payload["chave_pix"]
                if objetivo == "doacao"
                else payload.get("chave_pix")
            )

            # Register Pix key webhook if provided
            if chave_pix:
                self.__registra_chave_pix_webhook_itau(chave_pix)

            # Validate campaign duration
            if duracao == "temporaria":
                if not data_inicio or not data_fim:
                    raise BadRequestsError(
                        "Para campanhas temporárias, é necessário fornecer data de início e de término."
                    )
                data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
                data_fim = datetime.strptime(data_fim, "%Y-%m-%d")
                if data_inicio >= data_fim:
                    raise BadRequestsError(
                        "A data de início deve ser anterior à data de término."
                    )
            else:
                data_inicio = None
                data_fim = None

            filename_imagem_capa = (
                f"campanha_{titulo}_{str(uuid.uuid4())}_capa.jpg"
            )

            s3_client = file_service_factory()
            s3_client.upload_image(imagem_capa, filename_imagem_capa)

            campanha = Campanha(
                fk_empresa_id=1,
                titulo=titulo,
                descricao=descricao,
                data_inicio=data_inicio,
                data_fim=data_fim,
                valor_meta=valor_meta,
                prorrogado=prorrogado,
                data_prorrogacao=data_prorrogacao,
                valor_total_atingido=valor_total_atingido,
                data_fechamento_campanha=data_fechamento_campanha,
                status=status,
                filename=filename_imagem_capa,
                chave_pix=chave_pix,
                publica=publica,
                duracao=duracao,
                usuario_criacao=current_user["id"],
                objetivo=objetivo,
                cadastros_meta=cadastros_meta,
                preenchimento_foto=preenchimento_foto,
                label_foto=label_foto,
            )
            db.session.add(campanha)
            db.session.flush()

            if objetivo == "cadastro" or cadastrar_landing_page:
                create_landing_page = CreateLandingPage(campanha.id)
                create_landing_page.execute()

            if objetivo == "doacao":
                credito_unico = payload["credito_unico"]
                credito_recorrente = payload["credito_recorrente"]
                pix_unico = payload["pix_unico"]
                pix_recorrente = payload["pix_recorrente"]
                boleto_unico = payload["boleto_unico"]
                boleto_recorrente = payload["boleto_recorrente"]

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

            las_campaign = (
                Campanha.query.order_by(Campanha.data_criacao.desc())
                .first()
                .to_dict()
            )
            if las_campaign["duracao"] == "permanente":
                history_campaign = HistoricoCampanhaDonations(
                    fk_campanha_id=las_campaign["id"],
                    mes_ano=mes_ano,
                    valor_meta=valor_meta,
                )
                db.session.add(history_campaign)

            db.session.commit()

            response = {"msg": "Campanha cadastrada com sucesso."}, 201
            return response

        except ItauChavePixWebhookException as err:
            return {"error": err.error_message}, err.status_code

        except UploadImageException as error:
            logging.error(error.error_message)
            return {"error": error.msg}, error.status_code

        except KeyError as key_error:
            return {"error": f"O campo {key_error} é obrigatório."}, 400

        except Exception as err:
            return errors_handler(err)

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
                razao = "A chave pix é inválida."
                raise ItauChavePixWebhookException(
                    razao,
                    response.get("status", 400),
                )
