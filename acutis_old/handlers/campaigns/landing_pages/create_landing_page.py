import json
import uuid
from flask import request
from flask_jwt_extended import current_user
from models.conteudo_landpage import LandPageContent
from models.landpage import LandPage
from services.factories import file_service_factory
from utils.regex import format_string
from builder import db
from typing import Optional, BinaryIO


class CreateLandingPage:
    def __init__(self, fk_campanha_id: int) -> None:
        self.__fk_campanha_id = fk_campanha_id
        self.__s3_client = file_service_factory()

    def execute(self):
        return self.__create_landing_page()

    def __upload_image(
        self, image_file: Optional[BinaryIO], prefix: str, titulo: str
    ) -> Optional[str]:
        if not image_file:
            return None

        if not hasattr(image_file, "read"):
            raise ValueError(f"Invalid file object: {image_file}")

        filename = f"{prefix}_{titulo}_{str(uuid.uuid4())}.jpg"

        try:
            self.__s3_client.upload_image(image_file, filename)
            return filename
        except Exception as e:
            raise ValueError(f"Erro ao fazer upload da imagem: {str(e)}")

    def __create_landing_page(self):
        data = request.form.get("data")
        payload = json.loads(data)

        titulo = payload["titulo"].strip()
        descricao = payload["descricao"].strip()
        objetivo = payload["objetivo"].strip()
        tipo_cadastro = payload["tipo_cadastro"].strip()
        url = format_string(
            text=payload["url"].strip(), lower=True, is_url=True
        )
        conteudo = payload.get("conteudo", [])
        texto_pos_registro = payload["texto_pos_registro"]
        texto_email_pos_registro = payload["texto_email_pos_registro"]
        filename_background = None

        banner = request.files.get("banner")
        if not banner:
            raise ValueError("Banner deve ser enviado!")
        filename_banner = self.__upload_image(
            banner, "landing_page", titulo + "_banner"
        )

        background = request.files.get("background")
        if background:
            filename_background = self.__upload_image(
                background, "landing_page", titulo + "_background"
            )

        type_landpage = 1 if objetivo == "cadastro" else 2

        landpage = LandPage(
            campanha_id=self.__fk_campanha_id,
            background=filename_background,
            banner=filename_banner,
            titulo=titulo,
            descricao=descricao,
            tipo_cadastro=tipo_cadastro,
            url=url,
            type=type_landpage,
            texto_pos_registro=texto_pos_registro,
            texto_email_pos_registro=texto_email_pos_registro,
            usuario_criacao=current_user["id"],
        )

        db.session.add(landpage)
        db.session.flush()

        if len(conteudo) > 0:
            conteudos = []
            for index, item in enumerate(conteudo):
                content_image = request.files.get(f"conteudo_{index}_imagem")
                filename_content_image = self.__upload_image(
                    content_image,
                    "landing_page_content",
                    f"{titulo}_content_{index}",
                )

                content_data = {
                    "landpage_id": landpage.id,
                    "imagem": filename_content_image or item.get("imagem", ""),
                    "html": item.get("html", ""),
                    "usuario_criacao": current_user["id"],
                }

                conteudos.append(content_data)

            conteudo_landpage = [
                LandPageContent(**conteudo) for conteudo in conteudos
            ]
            db.session.add_all(conteudo_landpage)

        db.session.commit()

        return landpage
