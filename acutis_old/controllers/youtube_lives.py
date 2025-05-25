from handlers.lives.register.register_live import RegisterLive
from handlers.lives.update.update_live import UpdateLive
from models import (
    ViewLives,
    ViewAvulsas,
    ViewRecorrentes,
    ViewAudiencias,
)
from flask_jwt_extended import jwt_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from utils.functions import get_current_time
from utils.logs_access import log_access
from flask import Blueprint, jsonify, request
from spectree import Response
from datetime import datetime
from builder import api
from builder import db
import logging

youtube_lives_controller = Blueprint(
    "youtube_lives_controller", __name__, url_prefix="/youtube"
)


def validate_date_format(date_str):
    if not isinstance(date_str, str):
        return False
    try:
        datetime.fromisoformat(date_str)
        return True
    except ValueError:
        return False


@youtube_lives_controller.post("/create-channel")
@api.validate(
    resp=Response(HTTP_201=None, HTTP_409=None, HTTP_500=None), tags=["Lives"]
)
@jwt_required()
def create_channel():
    try:
        if current_user["fk_perfil_id"] != 1:
            return {
                "error": "Você não tem permissão para realizar esta ação."
            }, 403

        body = request.json

        tag = body["tag"].strip()
        rede_social = body["rede_social"].strip()
        fk_campanha_id = body.get("fk_campanha_id")

        channel_exists = (
            db.session.query(ViewLives)
            .filter(ViewLives.tag == tag, ViewLives.rede_social == rede_social)
            .first()
        )
        if channel_exists is not None:
            response = {"error": "Canal já cadastrado!"}
            log_access(
                str(response),
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
            )
            return response, 409

        new_channel = ViewLives(
            tag=tag,
            fk_campanha_id=fk_campanha_id,
            rede_social=rede_social.lower(),
        )
        db.session.add(new_channel)

        db.session.commit()

        response = {"msg": "Canal cadastrada com sucesso."}

        log_access(
            str(response),
            current_user["id"],
            current_user["nome"],
            current_user["fk_perfil_id"],
        )

        return response, 201

    except KeyError as err:
        return {"error": f"O campo {err} é obrigatório."}, 400

    except Exception as err:
        logging.error(f"{str(type(err))} - {str(err)}")
        db.session.rollback()
        response = {"error": "Ocorreu um error ao criar o canal."}
        log_access(
            str(response),
            current_user["id"],
            current_user["nome"],
            current_user["fk_perfil_id"],
        )
        return response, 500


@youtube_lives_controller.get("/get-channels")
@api.validate(
    resp=Response(HTTP_200=None, HTTP_204=None, HTTP_500=None), tags=["Lives"]
)
@jwt_required()
def get_channels():
    try:
        if current_user["fk_perfil_id"] != 1:
            return {
                "error": "Você não tem permissão para realizar esta ação."
            }, 403

        rede_social = request.args.get("rede_social")

        canais = ViewLives.query
        if rede_social:
            canais = canais.filter_by(rede_social=rede_social)

        canais = canais.all()
        if not canais:
            return jsonify([]), 204

        response = [
            {
                "id": canal.id,
                "tag": canal.tag,
                "rede_social": canal.rede_social,
            }
            for canal in canais
        ]

        return response, 200
    except Exception as err:
        logging.error(f"{str(type(err))} - {str(err)}")
        return {"error": "Ocorreu um erro ao listar as lives"}


@youtube_lives_controller.post("/register-live")
@api.validate(
    resp=Response(HTTP_201=None, HTTP_409=None, HTTP_500=None), tags=["Lives"]
)
@jwt_required()
def register_live():
    """Cria agendamento da live!"""
    if current_user["fk_perfil_id"] != 1:
        return {
            "error": "Você não tem permissão para realizar esta ação."
        }, 403

    register_live = RegisterLive()

    response = register_live.execute(request)

    return response


@youtube_lives_controller.get("/get-lives-schedules")
@api.validate(
    resp=Response(HTTP_200=None, HTTP_204=None, HTTP_400=None, HTTP_500=None),
    tags=["Lives"],
)
@jwt_required()
def get_lives_schedules():
    try:
        if current_user["fk_perfil_id"] != 1:
            return {
                "error": "Você não tem permissão para realizar esta ação."
            }, 403

        tipo_programacao = request.args.get("tipo_programacao")
        rede_social = request.args.get("rede_social")
        filtro_dias_semana = request.args.get("filtro_dias_semana", None)

        if filtro_dias_semana:
            filtro_dias_semana = filtro_dias_semana.split(",")

        if tipo_programacao and tipo_programacao not in [
            "avulsa",
            "periodica",
        ]:
            return {"error": "Tipo de programação inválida."}, 400

        query_avulsas = (
            db.session.query(
                ViewAvulsas.id,
                db.func.cast(ViewAvulsas.data_hora_inicio, db.Date).label(
                    "data"
                ),
                db.func.cast(ViewAvulsas.data_hora_inicio, db.Time).label(
                    "hora"
                ),
                ViewLives.rede_social,
                ViewLives.tag,
            )
            .join(ViewLives, ViewLives.id == ViewAvulsas.fk_view_live_id)
            .filter(ViewAvulsas.data_hora_inicio > get_current_time())
            .order_by(ViewAvulsas.data_hora_inicio.desc())
        )

        dia_semana_ordenacao = db.case(
            (ViewRecorrentes.dia_semana == "domingo", 1),
            (ViewRecorrentes.dia_semana == "segunda-feira", 2),
            (ViewRecorrentes.dia_semana == "terca-feira", 3),
            (ViewRecorrentes.dia_semana == "quarta-feira", 4),
            (ViewRecorrentes.dia_semana == "quinta-feira", 5),
            (ViewRecorrentes.dia_semana == "sexta-feira", 6),
            (ViewRecorrentes.dia_semana == "sabado", 7),
            else_=8,
        )

        query_recorrentes = (
            db.session.query(
                ViewRecorrentes.id,
                ViewRecorrentes.dia_semana.label("data"),
                ViewRecorrentes.data_hora_inicio.label("hora"),
                ViewLives.rede_social,
                ViewLives.tag,
            )
            .join(ViewLives, ViewLives.id == ViewRecorrentes.fk_view_live_id)
            .filter(
                (
                    ViewRecorrentes.dia_semana.in_(filtro_dias_semana)
                    if filtro_dias_semana
                    else True
                )
            )
            .order_by(dia_semana_ordenacao.asc())
        )

        if rede_social:
            query_avulsas = query_avulsas.filter(
                ViewLives.rede_social == rede_social
            )
            query_recorrentes = query_recorrentes.filter(
                ViewLives.rede_social == rede_social
            )

        resultado = []

        if (
            not tipo_programacao
            and not filtro_dias_semana
            or tipo_programacao == "avulsa"
        ):
            avulsas = query_avulsas.all()

            for live in avulsas:
                resultado.append(
                    {
                        "id": live.id,
                        "data": live.data.strftime("%d/%m/%Y"),
                        "hora": live.hora.strftime("%H:%M"),
                        "rede_social": live.rede_social,
                        "tag": live.tag,
                        "tipo_programacao": "avulsa",
                    }
                )

        if not tipo_programacao or tipo_programacao == "periodica":
            recorrentes = query_recorrentes.all()

            for live in recorrentes:
                resultado.append(
                    {
                        "id": live.id,
                        "data": live.data.title(),
                        "hora": live.hora.strftime("%H:%M"),
                        "rede_social": live.rede_social,
                        "tag": live.tag,
                        "tipo_programacao": "periodica",
                    }
                )

        return (
            jsonify(
                {
                    "data": resultado,
                }
            ),
            200,
        )

    except Exception as err:
        logging.error(f"{str(type(err))} - {str(err)}")
        return {
            "error": "Ocorreu um erro ao listar os horarios das lives."
        }, 500


@youtube_lives_controller.put("/edit-live-scheduled/<int:programacao_id>")
@jwt_required()
def edit_live_scheduled(programacao_id: int):
    if current_user["fk_perfil_id"] != 1:
        return {
            "error": "Você não tem permissão para realizar esta ação."
        }, 403

    update_live = UpdateLive()

    response = update_live.execute(request, programacao_id)

    return response


@youtube_lives_controller.delete("/delete-live-scheduled/<int:programacao_id>")
@jwt_required()
def delete_live_scheduled(programacao_id: int):
    try:
        if current_user["fk_perfil_id"] != 1:
            return {
                "error": "Você não tem permissão para realizar esta ação."
            }, 403

        tipo = request.args.get("tipo_programacao", type=str)
        if not tipo:
            return {
                "error": "A QueryParam 'tipo_programacao' é obrigatória."
            }, 400

        MAP_PROGRAMACAO = {"avulsa": ViewAvulsas, "periodica": ViewRecorrentes}

        programacao = db.session.get(
            MAP_PROGRAMACAO[tipo.lower()], programacao_id
        )
        if programacao is None:
            return {"error": "Programação da live não encontrada."}, 404

        db.session.delete(programacao)
        db.session.commit()

        return {"msg": "Programação da live deletada com sucesso."}, 200

    except KeyError as err:
        return {"error": f"O valor {err} é inválido."}, 400

    except Exception as err:
        logging.error(f"{str(type(err))} - {str(err)}")
        return {
            "error": "Ocorreu um erro ao deletar a programação da live."
        }, 500


@youtube_lives_controller.get("/get-all-lives-recurrence")
@api.validate(
    resp=Response(HTTP_201=None, HTTP_409=None, HTTP_500=None), tags=["Lives"]
)
@jwt_required()
def get_all_lives_recurrence():
    """Lista todas as lives recorrentes"""
    try:
        if current_user["fk_perfil_id"] != 1:
            return {
                "error": "Você não tem permissão para realizar esta ação."
            }, 403

        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)
        tag_filter = request.args.get("tag", type=str)
        rede_social_filter = request.args.get("rede_social", type=str)
        start_time = request.args.get("start_time", type=str)
        end_time = request.args.get("end_time", type=str)
        day = request.args.get("day", type=str)

        query_live_recurrence = (
            db.session.query(ViewRecorrentes)
            .join(ViewLives, ViewLives.id == ViewRecorrentes.fk_view_live_id)
            .order_by(ViewRecorrentes.id)
        )

        if tag_filter:
            query_live_recurrence = query_live_recurrence.filter(
                ViewLives.tag.like(f"%{tag_filter}%")
            )

        if rede_social_filter:
            query_live_recurrence = query_live_recurrence.filter(
                ViewLives.rede_social.like(f"%{rede_social_filter}%")
            )

        if start_time:
            query_live_recurrence = query_live_recurrence.filter(
                ViewRecorrentes.data_hora_inicio >= start_time
            )

        if end_time:
            query_live_recurrence = query_live_recurrence.filter(
                ViewRecorrentes.data_hora_fim <= end_time
            )

        if day:
            query_live_recurrence = query_live_recurrence.filter(
                ViewRecorrentes.dia_semana == day
            )

        paginated_result = query_live_recurrence.paginate(
            page=page, per_page=per_page, error_out=False
        )

        lives_recurrence_list = []
        for live_rec in paginated_result.items:
            live = (
                db.session.query(ViewLives)
                .filter(ViewLives.id == live_rec.fk_view_live_id)
                .one_or_none()
            )
            if live:
                obj = {
                    "agendamento_rec_id": live_rec.id,
                    "dia_semana": live_rec.dia_semana,
                    "fk_campanha_id": live.fk_campanha_id,
                    "rede_social": live.rede_social,
                    "tag": live.tag,
                    "fk_view_live_id": live_rec.fk_view_live_id,
                    "data_hora_inicio": live_rec.data_hora_inicio.strftime(
                        "%H:%M:%S"
                    ),
                    "data_hora_fim": live_rec.data_hora_fim.strftime(
                        "%H:%M:%S"
                    ),
                }
                lives_recurrence_list.append(obj)

        response = {
            "page": page,
            "per_page": per_page,
            "total": paginated_result.total,
            "total_pages": paginated_result.pages,
            "agendamentos_recorrentes": lives_recurrence_list,
        }

        return response

    except SQLAlchemyError as err:
        response = {
            "error": f"Ocorreu um erro ao listar lives recorrentes. - {str(err)}"
        }
        log_access(
            str(response),
            current_user.get("id"),
            current_user.get("nome"),
            current_user.get("fk_perfil_id"),
        )
        return response, 500

    except Exception as err:
        response = {"error": f"Ocorreu um erro inesperado. - {str(err)}"}
        log_access(
            str(response),
            current_user.get("id"),
            current_user.get("nome"),
            current_user.get("fk_perfil_id"),
        )
        return response, 500


@youtube_lives_controller.get("/get-all-lives-avulsas")
@api.validate(
    resp=Response(HTTP_201=None, HTTP_409=None, HTTP_500=None), tags=["Lives"]
)
@jwt_required()
def list_all_lives_avulsas():
    try:
        if current_user["fk_perfil_id"] != 1:
            return {
                "error": "Você não tem permissão para realizar esta ação."
            }, 403

        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)
        tag_filter = request.args.get("tag", type=str)
        rede_social_filter = request.args.get("rede_social", type=str)
        start_time = request.args.get("start_time", type=str)
        end_time = request.args.get("end_time", type=str)

        print(start_time)

        query_live_avulsas = (
            db.session.query(ViewAvulsas)
            .join(ViewLives, ViewLives.id == ViewAvulsas.fk_view_live_id)
            .order_by(ViewAvulsas.id)
        )

        if tag_filter:
            query_live_avulsas = query_live_avulsas.filter(
                ViewLives.tag.like(f"%{tag_filter}%")
            )

        if rede_social_filter:
            query_live_avulsas = query_live_avulsas.filter(
                ViewLives.rede_social.like(f"%{rede_social_filter}%")
            )

        if isinstance(start_time, str) and start_time:
            try:
                start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
                query_live_avulsas = query_live_avulsas.filter(
                    ViewAvulsas.data_hora_inicio >= start_time
                )
            except ValueError:
                return {
                    "error": "Formato de start_time inválido. Use 'YYYY-MM-DD HH:MM'."
                }, 400

        if isinstance(end_time, str) and end_time:
            try:
                end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M")
                query_live_avulsas = query_live_avulsas.filter(
                    ViewAvulsas.data_hora_fim <= end_time
                )
            except ValueError:
                return {
                    "error": "Formato de end_time inválido. Use 'YYYY-MM-DD HH:MM'."
                }, 400

        paginated_result = query_live_avulsas.paginate(
            page=page, per_page=per_page, error_out=False
        )

        lives_avulsas_list = []
        for live_rec in paginated_result.items:
            live = (
                db.session.query(ViewLives)
                .filter(ViewLives.id == live_rec.fk_view_live_id)
                .one_or_none()
            )
            if live:
                obj = {
                    "agendamento_rec_id": live_rec.id,
                    "fk_campanha_id": live.fk_campanha_id,
                    "rede_social": live.rede_social,
                    "tag": live.tag,
                    "fk_view_live_id": live_rec.fk_view_live_id,
                    "data_hora_inicio": live_rec.data_hora_inicio.strftime(
                        "%Y-%m-%d %H:%M"
                    ),
                    "data_hora_fim": live_rec.data_hora_fim.strftime(
                        "%Y-%m-%d %H:%M"
                    ),
                }
                lives_avulsas_list.append(obj)

        response = {
            "page": page,
            "per_page": per_page,
            "total": paginated_result.total,
            "total_pages": paginated_result.pages,
            "agendamentos_avulsos": lives_avulsas_list,
        }

        return response

    except SQLAlchemyError as err:
        response = {
            "error": f"Ocorreu um erro ao listar lives recorrentes. - {str(err)}"
        }
        log_access(
            str(response),
            current_user.get("id"),
            current_user.get("nome"),
            current_user.get("fk_perfil_id"),
        )
        return response, 500

    except Exception as err:
        response = {"error": f"Ocorreu um erro inesperado. - {str(err)}"}
        log_access(
            str(response),
            current_user.get("id"),
            current_user.get("nome"),
            current_user.get("fk_perfil_id"),
        )
        return response, 500


@youtube_lives_controller.put("/edite-agendamento-live/<int:agendamento_id>")
@api.validate(
    resp=Response(HTTP_201=None, HTTP_409=None, HTTP_500=None), tags=["Lives"]
)
@jwt_required()
def edit_agendamento_live(agendamento_id):
    """Realiza edição de agendamento da live"""
    try:
        if current_user["fk_perfil_id"] != 1:
            return {
                "error": "Você não tem permissão para realizar esta ação."
            }, 403

        tipo = request.json.get("tipo", None)
        fk_live_id = request.json.get("fk_live_id", None)
        data_horario_fim = request.json.get("data_horario_fim", None)
        data_horario_inicio = request.json.get("data_horario_inicio", None)
        dia_semana = request.json.get("dia_semana", None)

        dias_da_semana = [
            "segunda-feira",
            "terca-feira",
            "quarta-feira",
            "quinta-feira",
            "sexta-feira",
            "sabado",
            "domingo",
        ]
        options_type = ["recorrente", "avulsa"]

        if tipo is None:
            return {"error": "O campo tipo deve ser informado!"}, 400
        if tipo not in options_type:
            return {"error": "Tipo inválido"}

        if not data_horario_inicio or not data_horario_fim:
            return {
                "error": "Os campos 'data_horario_inicio' e 'data_horario_fim' são obrigatórios."
            }, 400

        if not validate_date_format(data_horario_inicio):
            return {
                "error": "Formato de data inválido. Use o formato 'YYYY-MM-DDTHH:MM:SS'."
            }, 400

        if not validate_date_format(data_horario_fim):
            return {
                "error": "Formato de data inválido. Use o formato 'YYYY-MM-DDTHH:MM:SS'."
            }, 400

        if data_horario_fim <= data_horario_inicio:
            return {"error": "Data fim deve ser maior que data início!"}, 400

        live_exists = (
            db.session.query(ViewLives)
            .filter(ViewLives.id == fk_live_id)
            .first()
        )

        if live_exists is None:
            return {"error": "Live não encontrada!"}, 404

        if tipo == "avulsa":
            agendamento_avulso = (
                db.session.query(ViewAvulsas)
                .filter(ViewAvulsas.id == agendamento_id)
                .first()
            )

            if agendamento_avulso is None:
                response = {"error": "Agendamento não econtrado"}
                log_access(
                    str(response),
                    current_user["id"],
                    current_user["nome"],
                    current_user["fk_perfil_id"],
                )
                return response, 404

            agendamento_avulso.tipo = tipo
            agendamento_avulso.fk_live_id = fk_live_id
            agendamento_avulso.data_hora_fim = data_horario_fim
            agendamento_avulso.data_hora_inicio = data_horario_inicio

            db.session.commit()

        if tipo == "recorrente":

            if dia_semana is None:
                return {
                    "error": "O campo 'dia_semana' deve ser informado para agendamentos recorrentes!"
                }, 400
            if dia_semana not in dias_da_semana:
                return {"error": "Dia da semana inválido!"}, 400

            agendamento_recorrentes = (
                db.session.query(ViewRecorrentes)
                .filter(ViewRecorrentes.id == agendamento_id)
                .first()
            )
            if agendamento_recorrentes is None:
                response = {"error": "Agendamento não econtrado"}
                log_access(
                    str(response),
                    current_user["id"],
                    current_user["nome"],
                    current_user["fk_perfil_id"],
                )
                return response, 404

            agendamento_recorrentes.dia_semana = dia_semana
            agendamento_recorrentes.fk_view_live_id = fk_live_id
            agendamento_recorrentes.data_hora_inicio = data_horario_inicio
            agendamento_recorrentes.data_hora_fim = data_horario_fim

            db.session.commit()

        response = {"msg": "Agendamento live editado com sucesso!"}
        log_access(
            str(response),
            current_user["id"],
            current_user["nome"],
            current_user["fk_perfil_id"],
        )
        return response, 200

    except Exception as err:
        db.session.rollback()
        response = {"error": f"Ocorreu um error ao editar live!"}
        logging.error(f"Erro ao editar agendamento: {err}")
        log_access(
            str(response),
            current_user["id"],
            current_user["nome"],
            current_user["fk_perfil_id"],
        )
        return response, 400


@youtube_lives_controller.delete(
    "/delete-agendamento-live/<tipo>/<int:agendamento_id>"
)
@api.validate(
    resp=Response(HTTP_201=None, HTTP_409=None, HTTP_500=None), tags=["Lives"]
)
@jwt_required()
def delete_agendamento(tipo, agendamento_id):
    try:
        if current_user["fk_perfil_id"] != 1:
            return {
                "error": "Você não tem permissão para realizar esta ação."
            }, 403

        optional_types = ["recorrente", "avulsa"]

        if tipo not in optional_types:
            response = {"error": "Tipo de agendamento inválido!"}
            log_access(
                str(response),
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
            )
            return response, 409

        if tipo == "recorrente":
            agendamento_rec = (
                db.session.query(ViewRecorrentes)
                .filter(ViewRecorrentes.id == agendamento_id)
                .first()
            )
            if agendamento_id is None:
                return {"error": "Agendamento não encontrado!"}, 404

            db.session.delete(agendamento_rec)

        if tipo == "avulsa":
            agendamento_rec = (
                db.session.query(ViewAvulsas)
                .filter(ViewAvulsas.id == agendamento_id)
                .first()
            )
            if agendamento_id is None:
                return {"error": "Agendamento não encontrado!"}, 404

            db.session.delete(agendamento_rec)

        db.session.commit()

        response = {"msg": "Agendamento cancelado com sucesso!"}
        log_access(
            str(response),
            current_user["id"],
            current_user["nome"],
            current_user["fk_perfil_id"],
        )

        return response, 200

    except Exception as err:
        db.session.rollback()
        response = {"error": f"Ocorreu um error ao deletar agendamento!"}
        logging.error(f"Erro ao deletar agendamento: {err}")
        log_access(
            str(response),
            current_user["id"],
            current_user["nome"],
            current_user["fk_perfil_id"],
        )
        return response, 400


@youtube_lives_controller.get("/views-live/<int:live_id>")
@api.validate(
    resp=Response(HTTP_201=None, HTTP_409=None, HTTP_500=None), tags=["Lives"]
)
@jwt_required()
def list_audiencia(live_id):
    try:
        if current_user["fk_perfil_id"] != 1:
            return {
                "error": "Você não tem permissão para realizar esta ação."
            }, 403

        filter_initial_date = request.args.get("initial_date", None)
        filter_end_date = request.args.get("end_date", None)

        query = (
            db.session.query(ViewAudiencias)
            .filter(ViewAudiencias.fk_view_live_id == live_id)
            .order_by(db.asc(ViewAudiencias.data_hora_registro))
        )

        if filter_initial_date:
            if not validate_date_format(filter_initial_date):
                return {
                    "error": "Formato de data inválido. Use o formato 'YYYY-MM-DDTHH:MM:SS'."
                }, 400

            query = query.filter(
                ViewAudiencias.data_hora_registro >= filter_initial_date
            )

        if filter_end_date:
            if not validate_date_format(filter_end_date):
                return {
                    "error": "Formato de data inválido. Use o formato 'YYYY-MM-DDTHH:MM:SS'."
                }, 400

            query = query.filter(
                ViewAudiencias.data_hora_registro <= filter_end_date
            )

        audiencia = query.all()

        res = [
            {
                "titulo": view.titulo,
                "data_hora": view.data_hora_registro.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "audiencia": view.audiencia,
            }
            for view in audiencia
        ]

        log_access(
            str(res),
            current_user["id"],
            current_user["nome"],
            current_user["fk_perfil_id"],
        )
        return res, 200

    except Exception as err:
        response = {
            "error": f"Ocorreu um error ao listar audiencia da live! - {err}"
        }
        log_access(
            str(response),
            current_user["id"],
            current_user["nome"],
            current_user["fk_perfil_id"],
        )
        return response, 400


@youtube_lives_controller.get("/lives/datas")
@api.validate(
    resp=Response(HTTP_200=None, HTTP_204=None, HTTP_500=None), tags=["Lives"]
)
@jwt_required()
def get_datas_lives_ocorridas():
    try:
        if current_user["fk_perfil_id"] != 1:
            return {
                "error": "Você não tem permissão para realizar esta ação."
            }, 403

        dates = (
            db.session.query(
                db.cast(ViewAudiencias.data_hora_registro, db.Date).label(
                    "data_hora_registro"
                )
            )
            .distinct()
            .all()
        )
        if not dates:
            return {}, 204

        formatted_dates = [
            date.data_hora_registro.strftime("%Y-%m-%d") for date in dates
        ]

        return jsonify({"datas": formatted_dates}), 200
    except Exception as err:
        logging.error(f"{str(type(err))} - {str(err)}")
        return {"error": "Ocorreu um erro ao listar as datas das lives"}


@youtube_lives_controller.get("/lives/titulos")
@api.validate(
    resp=Response(HTTP_200=None, HTTP_204=None, HTTP_500=None), tags=["Lives"]
)
@jwt_required()
def get_lives_titles_by_date():
    try:
        if current_user["fk_perfil_id"] != 1:
            return {
                "error": "Você não tem permissão para realizar esta ação."
            }, 403

        data = request.args.get("data")

        if not data:
            return {"error": "A data é obrigatória."}, 400

        try:
            data_formatada = datetime.strptime(data, "%Y-%m-%d")
        except ValueError:
            return {
                "error": "Formato de data inválido. Use o formato YYYY-MM-DD."
            }, 400

        lives_data = (
            db.session.query(
                ViewAudiencias.titulo,
                db.func.min(ViewAudiencias.data_hora_registro).label("inicio"),
                db.func.max(ViewAudiencias.data_hora_registro).label("fim"),
            )
            .filter(
                db.cast(ViewAudiencias.data_hora_registro, db.Date)
                == data_formatada.date()
            )
            .group_by(ViewAudiencias.titulo)
            .distinct()
            .all()
        )

        response_data = [
            {
                "titulo": live.titulo,
                "inicio": live.inicio.strftime("%H:%M:%S"),
                "fim": live.fim.strftime("%H:%M:%S"),
            }
            for live in lives_data
        ]

        return jsonify({"titulos": response_data}), 200

    except Exception as err:
        logging.error(f"{str(type(err))} - {str(err)}")
        return {
            "error": "Ocorreu um erro ao retornar os títulos das lives."
        }, 500


@youtube_lives_controller.get("/live/histograma")
@api.validate(
    resp=Response(HTTP_200=None, HTTP_204=None, HTTP_500=None), tags=["Lives"]
)
@jwt_required()
def get_histogram_data():
    try:
        if current_user["fk_perfil_id"] != 1:
            return {
                "error": "Você não tem permissão para realizar esta ação."
            }, 403

        filtro_rede_social = request.args.get(
            "filtro_rede_social", None, type=str
        )
        filtro_titulo_live = request.args.get(
            "filtro_titulo_live", None, type=str
        )
        if not filtro_titulo_live:
            return {"error": "O titulo da live é obrigatório."}, 400

        grouped_data = (
            db.session.query(
                ViewAudiencias.titulo,
                db.cast(ViewAudiencias.data_hora_registro, db.Date).label(
                    "data"
                ),
                db.extract("hour", ViewAudiencias.data_hora_registro).label(
                    "hora"
                ),
                db.extract("minute", ViewAudiencias.data_hora_registro).label(
                    "minuto"
                ),
                db.func.sum(ViewAudiencias.audiencia).label("audiencia_total"),
            )
            .join(ViewLives, ViewLives.id == ViewAudiencias.fk_view_live_id)
            .filter(
                ViewAudiencias.titulo == filtro_titulo_live,
                (
                    ViewLives.rede_social == filtro_rede_social
                    if filtro_rede_social
                    else True
                ),
            )
            .group_by(
                ViewAudiencias.titulo,
                db.cast(ViewAudiencias.data_hora_registro, db.Date),
                db.extract("hour", ViewAudiencias.data_hora_registro),
                db.extract("minute", ViewAudiencias.data_hora_registro),
            )
        )
        grouped_data = grouped_data.all()
        if not grouped_data:
            return {}, 204

        data = {}
        for row in grouped_data:
            titulo = row.titulo
            audiencia_total = row.audiencia_total
            data_hora_registro = f"{row.data} {row.hora:02}:{row.minuto:02}"

            if titulo not in data:
                data[titulo] = []
            data[titulo].append(
                {"audiencia": audiencia_total, "horario": data_hora_registro}
            )

        audiencias = [row.audiencia_total for row in grouped_data]
        audiencia_maxima = max(audiencias)
        audiencia_minima = min(audiencias)
        audiencia_media = round(sum(audiencias) / len(audiencias))

        redes_sociais = (
            db.session.query(
                ViewLives.rede_social,
                db.func.sum(ViewAudiencias.audiencia).label("total_audiencia"),
            )
            .join(
                ViewAudiencias, ViewLives.id == ViewAudiencias.fk_view_live_id
            )
            .filter(
                ViewAudiencias.titulo == filtro_titulo_live,
                (
                    ViewLives.rede_social == filtro_rede_social
                    if filtro_rede_social
                    else True
                ),
            )
            .group_by(ViewLives.rede_social)
        )
        redes_sociais.all()

        print("chegou aqui")

        total_geral = sum([rs.total_audiencia for rs in redes_sociais])
        canal_principal = max(redes_sociais, key=lambda rs: rs.total_audiencia)
        canal_principal_nome = canal_principal.rede_social
        canal_principal_porcentagem = (
            canal_principal.total_audiencia / total_geral
        ) * 100

        response = {
            "audiencia_maxima": audiencia_maxima,
            "audiencia_minima": audiencia_minima,
            "audiencia_media": audiencia_media,
            "canal_principal": f"{canal_principal_nome} - {canal_principal_porcentagem:.2f}%",
            "live_data": [
                {"titulo": titulo, "dados": dados}
                for titulo, dados in data.items()
            ],
        }

        return jsonify(response), 200
    except Exception as err:
        logging.error(f"{str(type(err))} - {str(err)}")
        return {"error": "Ocorreu um erro ao retornar o histograma."}, 500
