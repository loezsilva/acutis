from http import HTTPStatus

from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy
from flask import request as flask_request

from exceptions.error_types.http_bad_request import BadRequestError
from exceptions.error_types.http_conflict import ConflictError
from models.agape.familia_agape import FamiliaAgape
from models.agape.foto_familia_agape import FotoFamiliaAgape
from models.agape.membro_agape import MembroAgape
from models.endereco import Endereco
from models.schemas.agape.post.register_agape_family import (
    RegisterAgapeFamilyFormData,
)
from services.file_service import FileService
from services.google_maps_service import GoogleMapsAPI
from utils.functions import decodificar_base64_para_arquivo, is_valid_email, is_valid_name
from utils.regex import format_string
from utils.validator import cpf_cnpj_validator


class RegisterAgapeFamily:
    def __init__(
        self,
        database: SQLAlchemy,
        gmaps: GoogleMapsAPI,
        file_service: FileService,
    ) -> None:
        self.__database = database
        self.__gmaps = gmaps
        self.__file_service = file_service

    def execute(self):
        request = RegisterAgapeFamilyFormData(
            endereco=flask_request.form["endereco"],
            membros=flask_request.form["membros"],
            observacao=flask_request.form.get("observacao"),
            comprovante_residencia=flask_request.files.get("comprovante_residencia"),
            fotos_familia=flask_request.files.getlist('fotos_familia'),
        )
        request.endereco.cep = format_string(
            request.endereco.cep, only_digits=True
        )
        try:
            endereco = self.__register_address(request.endereco)
            familia = self.__register_family(request, endereco)
            self.__register_members(
                request.membros, familia
            )
        except Exception as exception:
            self.__database.session.rollback()
            raise exception

        return {"msg": "Família cadastrada com sucesso."}, HTTPStatus.CREATED

    def __register_address(self, endereco: Endereco) -> Endereco:
        str_endereco = f"{endereco.rua}, {endereco.numero}, {endereco.bairro}, {endereco.cidade}, {endereco.estado}, {endereco.cep}"
        geolocalidade = self.__gmaps.get_geolocation(str_endereco)

        db_endereco = Endereco(
            cep=endereco.cep,
            rua=endereco.rua,
            numero=endereco.numero,
            complemento=endereco.complemento,
            ponto_referencia=endereco.ponto_referencia,
            bairro=endereco.bairro,
            cidade=endereco.cidade,
            estado=endereco.estado,
            latitude=geolocalidade.latitude,
            longitude=geolocalidade.longitude,
            latitude_nordeste=geolocalidade.latitude_nordeste,
            longitude_nordeste=geolocalidade.longitude_nordeste,
            latitude_sudoeste=geolocalidade.latitude_sudoeste,
            longitude_sudoeste=geolocalidade.longitude_sudoeste,
        )

        self.__database.session.add(db_endereco)
        self.__database.session.flush()

        return db_endereco

    def __generate_family_name(self, membros: list[MembroAgape]) -> str:
        responsaveis = [
            is_valid_name(membro.nome)
            for membro in membros
            if membro.responsavel
        ]

        if len(responsaveis) == 1:
            primeiro_nome: str = responsaveis[0].split()[0]
            sobrenome: str = responsaveis[0].split()[-1]
            return f"{primeiro_nome} {sobrenome.upper()}"
        elif len(responsaveis) >= 2:
            primeiro_nome: str = responsaveis[0].split()[0]
            segundo_nome: str = responsaveis[1].split()[0]
            sobrenome: str = responsaveis[0].split()[-1]
            return f"{primeiro_nome} e {segundo_nome} {sobrenome.upper()}"
        else:
            return "Família Sem Responsável"

    def __register_family(
        self,
        request: RegisterAgapeFamilyFormData,
        endereco: Endereco,
    ) -> FamiliaAgape:
        nome_familia = self.__generate_family_name(request.membros)
        comprovante_residencia = request.comprovante_residencia

        familia = FamiliaAgape(
            fk_endereco_id=endereco.id,
            status=True,
            nome_familia=nome_familia,
            observacao=request.observacao,
            comprovante_residencia=(
                self.__file_service.upload_image(comprovante_residencia) 
                if comprovante_residencia else None
            ),
            cadastrada_por=current_user["id"],
        )
        self.__database.session.add(familia)
        self.__database.session.flush()

        for foto in request.fotos_familia:
            foto_familia = FotoFamiliaAgape(
                fk_familia_agape_id=familia.id,
                foto=self.__file_service.upload_image(foto)
            )
            self.__database.session.add(foto_familia)

        return familia

    def __register_members(
        self, 
        membros: list[MembroAgape], 
        familia: FamiliaAgape,
    ) -> None:
        for membro in membros:
            if membro.responsavel and membro.cpf is None:
                raise BadRequestError(
                    f"O CPF do responsável {membro.nome} é obrigatório."
                )

            if membro.cpf:
                membro.cpf = cpf_cnpj_validator(
                    membro.cpf, document_type="cpf"
                )
                db_membro: MembroAgape = MembroAgape.query.filter_by(
                    cpf=membro.cpf
                ).first()
                if db_membro:
                    raise ConflictError(
                        f"Já existe um membro com o CPF {membro.cpf} cadastrado."
                    )

            if membro.email:
                membro.email = is_valid_email(
                    membro.email,
                    check_deliverability=True,
                    check_valid_domain=False,
                )
                db_membro = MembroAgape.query.filter_by(
                    email=membro.email
                ).first()
                if db_membro:
                    raise ConflictError(
                        f"Já existe um membro com o email {membro.email} cadastrado."
                    )

            membro.nome = is_valid_name(membro.nome)
            membro.telefone = format_string(membro.telefone, only_digits=True)

            membro_agape = MembroAgape(
                fk_familia_agape_id=familia.id,
                responsavel=membro.responsavel,
                nome=membro.nome,
                email=membro.email,
                telefone=membro.telefone,
                cpf=membro.cpf,
                data_nascimento=membro.data_nascimento,
                funcao_familiar=membro.funcao_familiar,
                escolaridade=membro.escolaridade,
                ocupacao=membro.ocupacao,
                renda=membro.renda,
                beneficiario_assistencial=membro.beneficiario_assistencial,
                foto_documento=(
                    self.__file_service.upload_image(
                        decodificar_base64_para_arquivo(
                            membro.foto_documento
                        )
                    ) if membro.foto_documento else None
                )
            )
            self.__database.session.add(membro_agape)

        self.__database.session.commit()
