from datetime import datetime
import json
from flask import request
from flask_jwt_extended import current_user
from models.conteudo_landpage import LandPageContent
from services.factories import file_service_factory
from utils.regex import format_string
from builder import db


class UpdateLandingPage:
    def __init__(self, landing_page) -> None:
        self.__landing_page = landing_page
        self.__s3_client = file_service_factory()

    def execute(self):
        return self.__update_landing_page()

    def __update_landing_page(self):
        payload = request.form.get("data")
        payload = json.loads(payload)

        titulo = payload["titulo"].strip()
        descricao = payload["descricao"].strip()
        tipo_cadastro = payload["tipo_cadastro"].strip()
        url = format_string(
            text=payload["url"].strip(), lower=True, is_url=True
        )
        conteudos = payload.get("conteudo", [])
        texto_pos_registro = payload["texto_pos_registro"]
        texto_email_pos_registro = payload["texto_email_pos_registro"]

        banner = request.files.get("banner")
        if banner:
            filename_banner = self.__s3_client.upload_image(
                banner, f"{titulo}_banner"
            )
            self.__landing_page.banner = filename_banner

        background = request.files.get("background")
        if background:
            filename_background = self.__s3_client.upload_image(
                background, f"{titulo}_background"
            )
            self.__landing_page.background = filename_background

        self.__landing_page.titulo = titulo
        self.__landing_page.descricao = descricao
        self.__landing_page.tipo_cadastro = tipo_cadastro
        self.__landing_page.url = url
        self.__landing_page.texto_pos_registro = texto_pos_registro
        self.__landing_page.texto_email_pos_registro = texto_email_pos_registro
        self.__landing_page.data_alteracao = datetime.now()
        self.__landing_page.usuario_alteracao = current_user["id"]

        conteudo_landpage = LandPageContent.query.filter_by(
            landpage_id=self.__landing_page.id
        ).all()

        conteudo_atualizar_ids = [
            conteudo.get("id") for conteudo in conteudos if conteudo.get("id")
        ]
        conteudo_atualizar = [
            conteudo
            for conteudo in conteudo_landpage
            if conteudo.id in conteudo_atualizar_ids
        ]
        conteudo_deletar = list(
            set(conteudo_landpage) - set(conteudo_atualizar)
        )

        for conteudo in conteudo_deletar:
            db.session.delete(conteudo)

        for index, conteudo in enumerate(conteudos):
            id = conteudo.get("id")
            content_image = request.files.get(f"conteudo_{index}_imagem")

            if id:
                content = db.session.get(LandPageContent, id)
                if content_image:
                    filename_content_image = self.__s3_client.upload_image(
                        content_image, f"{titulo}_content_{index}"
                    )
                    content.imagem = filename_content_image
                content.html = conteudo["html"]
                content.data_alteracao = datetime.now()
                content.usuario_alteracao = current_user["id"]
            else:
                filename_content_image = None
                if content_image:
                    filename_content_image = self.__s3_client.upload_image(
                        content_image, f"{titulo}_content_{index}"
                    )

                content = LandPageContent(
                    landpage_id=self.__landing_page.id,
                    imagem=filename_content_image
                    or conteudo.get("imagem", ""),
                    html=conteudo.get("html", ""),
                    usuario_criacao=current_user["id"],
                )
                db.session.add(content)

        db.session.commit()

        return self.__landing_page
