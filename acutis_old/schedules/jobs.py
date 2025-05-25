import logging
import os
import random
from datetime import date, datetime, timedelta, timezone
from typing import List

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from sqlalchemy import Date, cast, func, or_

from builder import db, scheduler
from models import (
    Campanha,
    Clifor,
    Endereco,
    FormaPagamento,
    Pedido,
    ProcessamentoPedido,
    Usuario,
)
from models.agape.doacao_agape import DoacaoAgape
from models.agape.familia_agape import FamiliaAgape
from models.historico_campanha_doacoes import HistoricoCampanhaDonations
from models.list_exception_donations import ListExceptionDonations
from services import ItauAPI
from services.factories import file_service_factory
from services.mercado_pago_api import MercadoPago
from templates import recurrence_pix_invoice_payment_email_template
from templates.email_templates import (
    happy_birthday_email_template,
    reminder_active_account_email_template,
    reminder_recurrence_donation_email_template,
)
from utils.functions import get_current_time, send_thanks_for_donation
from utils.send_email import send_email
from utils.token_email import generate_token


@scheduler.task(
    "cron", id="job_obriga_atualizar_endereco", day="*", hour="23", minute="59"
)
def job_obriga_atualizar_endereco():
    with scheduler.app.app_context():
        enderecos: List[Endereco] = Endereco.query.all()

        for endereco in enderecos:
            if endereco.ultima_atualizacao_endereco:
                if (
                    date.today() - endereco.ultima_atualizacao_endereco
                ).days > 180 and not endereco.obriga_atualizar_endereco:
                    endereco.obriga_atualizar_endereco = True
                    try:
                        db.session.commit()
                    except Exception as err:
                        logging.error(f"{type(err)} - {err}")
                        db.session.rollback()


@scheduler.task(
    "cron", id="job_atualiza_status_campanha", day="*", hour="23", minute="59"
)
def job_atualiza_status_campanha():
    with scheduler.app.app_context():
        campanhas = Campanha.query.all()
        atualizados = []

        for campanha in campanhas:
            if campanha.status:
                date_to_update = (
                    campanha.data_prorrogacao
                    if campanha.data_prorrogacao
                    else campanha.data_fim
                )
                if date_to_update and date.today() > date_to_update:
                    campanha.status = False
                    try:
                        db.session.commit()
                        atualizados.append(campanha.id)
                    except Exception as err:
                        logging.error(f"{type(err)} - {err}")
                        db.session.rollback()


@scheduler.task(
    "cron",
    id="job_atualiza_status_pagamento_boleto",
    day="*",
    hour="23",
    minute="59",
)
def job_atualiza_status_pagamento_boleto():
    with scheduler.app.app_context():
        data_atual = datetime.now()
        data_expiracao = data_atual - timedelta(days=31)

        pagamento_boletos_validos = (
            db.session.query(
                ProcessamentoPedido.id,
                ProcessamentoPedido.transaction_id,
                Pedido.periodicidade,
            )
            .join(Pedido, Pedido.id == ProcessamentoPedido.fk_pedido_id)
            .filter(
                ProcessamentoPedido.fk_forma_pagamento_id == 3,
                ProcessamentoPedido.status_processamento == 0,
                ProcessamentoPedido.data_processamento > data_expiracao,
                ProcessamentoPedido.transaction_id.isnot(None),
            )
            .all()
        )

        pagamento_boletos_expirados = ProcessamentoPedido.query.filter(
            ProcessamentoPedido.fk_forma_pagamento_id == 3,
            ProcessamentoPedido.status_processamento == 0,
            ProcessamentoPedido.data_processamento < data_expiracao,
        ).all()

        if not pagamento_boletos_validos and not pagamento_boletos_expirados:
            return

        with db.session.begin_nested():
            for pagamento in pagamento_boletos_validos:
                processamento_pedido = db.session.get(
                    ProcessamentoPedido, pagamento.id
                )
                pedido = db.session.get(
                    Pedido, processamento_pedido.fk_pedido_id
                )
                clifor = db.session.get(Clifor, pedido.fk_clifor_id)
                campanha = db.session.get(Campanha, pedido.fk_campanha_id)

                path = f"/cobv/{pagamento.transaction_id}"

                try:
                    itau_api = ItauAPI("pix")
                    response, status = itau_api.get(path=path)

                except Exception as err:
                    logging.error(
                        f"{datetime.now()} - job_atualiza_status_pagamento_boleto -> Erro ao atualizar ID {pagamento.id}: {type(err)} - {err}"
                    )
                    continue

                if status != 200:
                    logging.error(
                        f"{datetime.now()} - job_atualiza_status_pagamento_boleto -> Erro ao atualizar ID {pagamento.id}: ----> {response}"
                    )
                    continue

                if (
                    response["status"] == "CONCLUIDA"
                    or response["status"] == "REMOVIDA_PELO_USUARIO_RECEBEDOR"
                ):
                    processamento_pedido.status_processamento = 1
                    send_thanks_for_donation(
                        campanha, clifor.nome, clifor.email
                    )

                    if pagamento.periodicidade == 2:

                        clifor = db.session.get(
                            Clifor, processamento_pedido.fk_clifor_id
                        )

                        pedido = db.session.get(
                            Pedido, processamento_pedido.fk_pedido_id
                        )

                        campanha = db.session.get(
                            Campanha, pedido.fk_campanha_id
                        )

                        endereco = Endereco.query.filter_by(
                            fk_clifor_id=clifor.id
                        ).first()

                        reference_num = f"{clifor.fk_usuario_id}_BOLETO_{datetime.timestamp(datetime.now())}"

                        valor_boleto = str(
                            int(processamento_pedido.valor * 100)
                        ).zfill(17)

                        data_vencimento_obj = get_current_time().replace(
                            day=pedido.data_pedido.day
                        ) + relativedelta(months=1)
                        data_limite_vencimento_obj = data_vencimento_obj

                        data_vencimento_boleto = data_vencimento_obj.strftime(
                            "%Y-%m-%d"
                        )
                        data_limite_vencimento = (
                            data_limite_vencimento_obj.strftime("%Y-%m-%d")
                        )

                        numero_nosso_numero = random.randrange(10**7, 10**8)

                        path = "/boletos_pix"

                        TIPO_PESSOA_MAP = {
                            11: {
                                "codigo_tipo_pessoa": "F",
                                "numero_cadastro_pessoa_fisica": clifor.cpf_cnpj,
                            },
                            14: {
                                "codigo_tipo_pessoa": "J",
                                "numero_cadastro_nacional_pessoa_juridica": clifor.cpf_cnpj,
                            },
                        }

                        tipo_pessoa = TIPO_PESSOA_MAP[len(clifor.cpf_cnpj)]

                        body = {
                            "etapa_processo_boleto": "efetivacao",
                            "beneficiario": {
                                "id_beneficiario": "382700998646"
                            },
                            "dado_boleto": {
                                "tipo_boleto": "a vista",
                                "codigo_carteira": "109",
                                "valor_total_titulo": valor_boleto,
                                "codigo_especie": "99",
                                "data_emissao": get_current_time().strftime(
                                    "%Y-%m-%d"
                                ),
                                "pagador": {
                                    "pessoa": {
                                        "nome_pessoa": clifor.nome,
                                        "tipo_pessoa": tipo_pessoa,
                                    },
                                    "endereco": {
                                        "nome_logradouro": (
                                            endereco.rua
                                            if len(endereco.rua) <= 45
                                            else endereco.rua[:45]
                                        ),
                                        "nome_bairro": (
                                            endereco.bairro
                                            if len(endereco.bairro) <= 15
                                            else endereco.bairro[:15]
                                        ),
                                        "nome_cidade": (
                                            endereco.cidade
                                            if len(endereco.cidade) <= 20
                                            else endereco.cidade[:20]
                                        ),
                                        "sigla_UF": (
                                            endereco.estado
                                            if len(endereco.estado) <= 2
                                            else endereco.estado[:2]
                                        ),
                                        "numero_CEP": endereco.cep,
                                    },
                                },
                                "sacador_avalista": {
                                    "pessoa": {
                                        "nome_pessoa": "INSTITUTO HESED DOS IRMAOS E IRMAS",
                                        "tipo_pessoa": {
                                            "codigo_tipo_pessoa": "J",
                                            "numero_cadastro_nacional_pessoa_juridica": "02779337000174",
                                        },
                                    },
                                    "endereco": {
                                        "nome_logradouro": "AVENIDA DIONISIO LEONEL ALENCAR",
                                        "nome_bairro": "ANCURI",
                                        "nome_cidade": "FORTALEZA",
                                        "sigla_UF": "CE",
                                        "numero_CEP": "60873073",
                                    },
                                },
                                "dados_individuais_boleto": [
                                    {
                                        "numero_nosso_numero": numero_nosso_numero,
                                        "data_vencimento": data_vencimento_boleto,
                                        "valor_titulo": valor_boleto,
                                        "data_limite_pagamento": data_limite_vencimento,
                                    }
                                ],
                            },
                            "dados_qrcode": {"chave": campanha.chave_pix},
                        }

                        itau_api = ItauAPI("bolecode")

                        resp, status = itau_api.post(path=path, body=body)

                        if status != 200:
                            logging.error(
                                f"type_error: {str(status)} - msg_error: {str(resp)}"
                            )
                            return {
                                "error": "Ocorreu um erro ao criar o boleto de pagamento."
                            }, 500

                        data = resp["data"]

                        TxID = data["dados_qrcode"]["txid"]
                        nosso_numero = data["dado_boleto"][
                            "dados_individuais_boleto"
                        ][0]["numero_nosso_numero"]

                        novo_processamento_pedido = ProcessamentoPedido(
                            fk_empresa_id=processamento_pedido.fk_empresa_id,
                            fk_filial_id=processamento_pedido.fk_filial_id,
                            fk_pedido_id=processamento_pedido.fk_pedido_id,
                            fk_clifor_id=processamento_pedido.fk_clifor_id,
                            fk_forma_pagamento_id=processamento_pedido.fk_forma_pagamento_id,
                            fk_lancamento_id=processamento_pedido.fk_lancamento_id,
                            data_processamento=get_current_time(),
                            valor=processamento_pedido.valor,
                            status_processamento=0,
                            id_transacao_gateway=reference_num,
                            transaction_id=TxID,
                            nosso_numero=nosso_numero,
                            usuario_criacao=clifor.fk_usuario_id,
                        )
                        db.session.add(novo_processamento_pedido)

            for pagamento in pagamento_boletos_expirados:
                pagamento.status_processamento = 2

            try:
                db.session.commit()
            except Exception as err:
                db.session.rollback()
                logging.error(
                    f"{datetime.now()} - job_atualiza_status_pagamento_boleto -> Erro ao atualizar ID {pagamento.id}: {type(err)} - {err}"
                )


@scheduler.task(
    "cron",
    id="job_registra_usuarios_pagamento_pix_mercado_pago",
    day="*",
    hour="*",
    minute="*",
)
def job_registra_usuarios_pagamento_pix_mercado_pago():
    with scheduler.app.app_context():
        try:
            dt = datetime.now(tz=timezone.utc) - timedelta(hours=4, minutes=3)

            begin_date = dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[
                :-3
            ] + dt.strftime("%z")

            filters = {
                "criteria": "desc",
                "begin_date": begin_date,
                "end_date": "NOW",
                "limit": 1000,
            }

            mp = MercadoPago()

            response = mp.search_payments(filters)
            results = response.get("results")

            for result in results:
                try:
                    transaction_id = result.get("id")
                    bank = (
                        result.get("point_of_interaction", {})
                        .get("transaction_data", {})
                        .get("bank_info", {})
                        .get("payer", {})
                        .get("long_name")
                    )
                    if bank is None:
                        continue

                    if len(bank) > 90:
                        bank = bank[:90]

                    transaction_amount = result.get("transaction_amount")
                    status = result.get("status")
                    date_created_str = result.get("date_created")
                    date_approved_str = result.get("date_approved")
                    id_pagamento = result.get("transaction_details", {}).get(
                        "transaction_id"
                    )

                    date_created = parse(date_created_str) + timedelta(hours=1)
                    date_approved = parse(date_approved_str) + timedelta(
                        hours=1
                    )

                    pagamento_ja_registrado = (
                        ProcessamentoPedido.query.filter_by(
                            transaction_id=str(transaction_id)
                        ).first()
                    )
                    if (
                        pagamento_ja_registrado is not None
                        or status != "approved"
                    ):
                        continue

                    clifor = Clifor.query.filter(
                        Clifor.nome.ilike(f"%{bank}%")
                    ).first()

                    if clifor is None:
                        clifor = Clifor(
                            fk_empresa_id=1, tipo_clifor="j", nome=bank
                        )

                        db.session.add(clifor)
                        db.session.flush()

                    reference_num = (
                        f"{clifor.id}_PIX_{datetime.timestamp(datetime.now())}"
                    )

                    pedido = Pedido(
                        fk_empresa_id=1,
                        fk_clifor_id=clifor.id,
                        fk_forma_pagamento_id=2,
                        data_pedido=date_created,
                        periodicidade=1,
                        status_pedido=1,
                        valor_total_pedido=transaction_amount,
                        recorrencia_ativa=False,
                        fk_gateway_pagamento_id=2,
                        anonimo=True,
                        usuario_criacao=0,
                    )
                    db.session.add(pedido)
                    db.session.flush()

                    processamento_pedido = ProcessamentoPedido(
                        fk_empresa_id=1,
                        fk_clifor_id=clifor.id,
                        fk_pedido_id=pedido.id,
                        fk_forma_pagamento_id=2,
                        data_processamento=date_approved,
                        valor=transaction_amount,
                        status_processamento=1,
                        id_transacao_gateway=reference_num,
                        transaction_id=transaction_id,
                        id_pagamento=id_pagamento,
                        usuario_criacao=0,
                    )

                    db.session.add(processamento_pedido)

                    db.session.commit()
                except Exception as err:
                    db.session.rollback()
                    logging.error(
                        f"{type(err)} - {str(err)} - {transaction_id}"
                    )
                    continue

        except Exception as err:
            logging.error(
                f"{get_current_time()} - job_registra_usuarios_pagamento_pix_mercado_pago -> Ocorreu um erro ao executar a rotina.\nERROR: {type(err)} - {err}"
            )


@scheduler.task(
    "cron",
    id="job_dispara_email_recorrencia_pagamento_pix_boleto",
    day="*",
    hour="11",
    minute="30",
)
def job_dispara_email_recorrencia_pagamento_pix_boleto():
    with scheduler.app.app_context():
        data_28_dias_atras = datetime.now() - timedelta(days=31)

        ultimo_processamento_subquery = (
            db.session.query(
                ProcessamentoPedido.fk_pedido_id,
                db.func.max(ProcessamentoPedido.id).label(
                    "ultimo_processamento_id"
                ),
            )
            .join(Pedido, ProcessamentoPedido.fk_pedido_id == Pedido.id)
            .filter(
                db.func.cast(ProcessamentoPedido.data_processamento, db.Date)
                == db.func.cast(data_28_dias_atras, db.Date)
            )
            .group_by(ProcessamentoPedido.fk_pedido_id)
            .subquery()
        )

        doacoes_recorrentes = (
            db.session.query(
                Usuario.id.label("fk_usuario_id"),
                Usuario.email.label("usuario_email"),
                Usuario.nome.label("usuario_nome"),
                ProcessamentoPedido.id.label("fk_processamento_pedido_id"),
                ProcessamentoPedido.fk_forma_pagamento_id,
                Pedido.id.label("fk_pedido_id"),
                Pedido.fk_gateway_pagamento_id,
                Pedido.fk_forma_pagamento_id.label("pedido_forma_pagamento"),
                Campanha.id.label("fk_campanha_id"),
                Campanha.titulo.label("nome_campanha"),
                Campanha.filename,
            )
            .join(Clifor, Clifor.fk_usuario_id == Usuario.id)
            .join(
                ProcessamentoPedido,
                Clifor.id == ProcessamentoPedido.fk_clifor_id,
            )
            .join(
                ultimo_processamento_subquery,
                ultimo_processamento_subquery.c.ultimo_processamento_id
                == ProcessamentoPedido.id,
            )
            .join(Pedido, Pedido.id == ProcessamentoPedido.fk_pedido_id)
            .join(Campanha, Campanha.id == Pedido.fk_campanha_id)
            .filter(
                Pedido.periodicidade == 2,
                Pedido.recorrencia_ativa == 1,
                Campanha.status == 1,
                db.or_(
                    ProcessamentoPedido.fk_forma_pagamento_id == 2,
                    ProcessamentoPedido.fk_forma_pagamento_id == 3,
                ),
            )
        )

        doacoes_recorrentes = doacoes_recorrentes.all()

        if not doacoes_recorrentes:
            return

        s3_client = file_service_factory()

        for doacao in doacoes_recorrentes:
            try:
                processamento_pedido = db.session.get(
                    ProcessamentoPedido, doacao.fk_processamento_pedido_id
                )

                PAYMENT_TYPE_MAP = {
                    2: {
                        "payment_type": "pix",
                        "payment_salt": "send_email_pix_recurrence_payment",
                    },
                    3: {
                        "payment_type": "invoice",
                        "payment_salt": "send_email_invoice_recurrence_payment",
                    },
                }

                payment_type = PAYMENT_TYPE_MAP[doacao.fk_forma_pagamento_id]

                id_usuario = doacao.fk_usuario_id
                forma_pagamento = (
                    "BOLETO" if doacao.fk_forma_pagamento_id == 3 else "PIX"
                )
                mpag = "MPAG_" if doacao.fk_gateway_pagamento_id == 2 else ""
                timestamp = datetime.timestamp(datetime.now())

                reference_num = (
                    f"{id_usuario}_{forma_pagamento}_{mpag}{timestamp}"
                )

                processamento_pedido = ProcessamentoPedido(
                    fk_empresa_id=processamento_pedido.fk_empresa_id,
                    fk_filial_id=processamento_pedido.fk_filial_id,
                    fk_pedido_id=processamento_pedido.fk_pedido_id,
                    fk_clifor_id=processamento_pedido.fk_clifor_id,
                    fk_forma_pagamento_id=doacao.pedido_forma_pagamento,
                    fk_lancamento_id=processamento_pedido.fk_lancamento_id,
                    valor=processamento_pedido.valor,
                    id_transacao_gateway=reference_num,
                    data_processamento=get_current_time(),
                    status_processamento=0,
                    usuario_criacao=doacao.fk_usuario_id,
                )

                db.session.add(processamento_pedido)

                db.session.flush()

                foto_campanha = s3_client.get_public_url(doacao.filename)

                obj_user = {
                    "id": doacao.fk_usuario_id,
                    "fk_processamento_pedido_id": processamento_pedido.id,
                    "fk_pedido_id": doacao.fk_pedido_id,
                    "fk_gateway_pagamento_id": doacao.fk_gateway_pagamento_id,
                }

                token = generate_token(
                    obj=obj_user, salt=payment_type.get("payment_salt")
                )

                html = recurrence_pix_invoice_payment_email_template(
                    name=doacao.usuario_nome,
                    token=token,
                    campanha_id=doacao.fk_campanha_id,
                    nome_campanha=doacao.nome_campanha,
                    tipo_pagamento=payment_type.get("payment_type"),
                    foto_campanha=foto_campanha,
                )

                send_email(
                    "HeSed - Doação mensal", doacao.usuario_email, html, 4
                )

                db.session.commit()

            except Exception as err:
                logging.error(
                    f"{datetime.now()} - job_dispara_email_recorrencia_pagamento_pix_boleto -> {type(err)} - {err}"
                )
                db.session.rollback()
                continue


@scheduler.task(
    "cron",
    id="job_atualiza_status_pagamento_48_horas",
    day="*",
    hour="23",
    minute="59",
)
def job_atualiza_status_pagamento_48_horas():
    with scheduler.app.app_context():
        try:
            db.session.query(ProcessamentoPedido).filter(
                ProcessamentoPedido.status_processamento == 0,
                db.cast(ProcessamentoPedido.data_processamento, db.Date)
                <= (get_current_time().date() - timedelta(days=2)),
            ).update(
                {ProcessamentoPedido.status_processamento: 2},
                synchronize_session=False,
            )

            db.session.commit()
        except Exception as err:
            db.session.rollback()
            logging.error(
                f"{datetime.now()} - job_atualiza_status_pagamento_48_horas -> {type(err)} - {err}"
            )


@scheduler.task(
    "cron", id="job_fechamento_campanha_mensal", day=1, hour=0, minute=0
)
def job_fechar_mes():
    with scheduler.app.app_context():
        print("Job iniciado:", datetime.now())

        agora = datetime.now()
        primeiro_dia_mes_atual = datetime(agora.year, agora.month, 1)
        ultimo_dia_mes_anterior = primeiro_dia_mes_atual - timedelta(days=1)
        mes_anterior = ultimo_dia_mes_anterior.month
        ano_anterior = ultimo_dia_mes_anterior.year

        print(f"Mês anterior: {mes_anterior}, Ano anterior: {ano_anterior}")

        campanhas_permanentes = (
            Campanha.query.filter_by(
                duracao="permanente", objetivo="doacao", deleted_at=None
            )
            .options(db.joinedload(Campanha.historico_doacoes))
            .all()
        )
        print(
            f"Campanhas de doação permanentes encontradas: {campanhas_permanentes}"
        )

        for campanha in campanhas_permanentes:
            print(f"Processando campanha: {campanha.id}")
            historico_existente = next(
                (
                    h
                    for h in campanha.historico_doacoes
                    if h.mes_ano.month == mes_anterior
                    and h.mes_ano.year == ano_anterior
                ),
                None,
            )

            if historico_existente:
                print(
                    f"Histórico encontrado para o mês anterior: {historico_existente}"
                )
                valor_total_doacoes = (
                    db.session.query(
                        db.func.coalesce(
                            db.func.sum(Pedido.valor_total_pedido), 0
                        )
                    )
                    .join(
                        ProcessamentoPedido,
                        ProcessamentoPedido.fk_pedido_id == Pedido.id,
                    )
                    .filter(
                        Pedido.fk_campanha_id == campanha.id,
                        ProcessamentoPedido.status_processamento == 1,
                        db.func.month(Pedido.data_pedido) == mes_anterior,
                    )
                    .scalar()
                )

                print(
                    f"Valor total de doações calculado: {valor_total_doacoes}"
                )
                historico_existente.valor_atingido = valor_total_doacoes
                db.session.commit()
                print(
                    f"Histórico atualizado com valor atingido: {historico_existente.valor_atingido}"
                )

            if mes_anterior == 12:
                novo_ano = ano_anterior + 1
                novo_mes = 1
            else:
                novo_ano = ano_anterior
                novo_mes = mes_anterior + 1

            novo_mes_ano = datetime(novo_ano, novo_mes, 1)

            historico_futuro_existente = next(
                (
                    h
                    for h in campanha.historico_doacoes
                    if h.mes_ano.month == novo_mes
                    and h.mes_ano.year == novo_ano
                ),
                None,
            )

            if not historico_futuro_existente:
                novo_historico = HistoricoCampanhaDonations(
                    fk_campanha_id=campanha.id,
                    mes_ano=novo_mes_ano,
                    valor_meta=campanha.valor_meta,
                )
                db.session.add(novo_historico)
                db.session.commit()
                print(f"Novo histórico de doações criado: {novo_historico}")

        print("Job concluído:", datetime.now())


@scheduler.task(
    "cron", id="job_include_pedido_exception", day="*", hour="*", minute="*"
)
def job_include_pedido_exception():
    """Garante que todo pedido realizado pelos clifors que estão listados na lista de doações em exceção sejam desconsiderados da contagem"""

    try:
        with scheduler.app.app_context():
            print("job_include_pedido_exception iniciado!")
            ids_clifor = db.session.query(
                ListExceptionDonations.fk_clifor_id
            ).all()

            for id in ids_clifor:
                id_clifor = id[0]

                pedidos = (
                    db.session.query(Pedido)
                    .filter(
                        Pedido.fk_clifor_id == id_clifor,
                        Pedido.contabilizar_doacao == True,
                    )
                    .all()
                )

                for pedido in pedidos:
                    pedido.contabilizar_doacao = False
                    db.session.add(pedido)

            db.session.commit()

    except Exception as err:
        db.session.rollback()
        logging.error(f"{type(err)} - {err}")
        print(
            f"Ocorreu um erro ao executar job ***job_include_pedido_exception*** -> {err}"
        )


@scheduler.task("cron", id="job_register_file_logs", minute="*/59")
def job_register_logs():
    with scheduler.app.app_context():
        print("Executando registro de logs")

        s3_client = file_service_factory()
        name_file_to_bucket = "access.txt"

        size_path_local = os.path.getsize("access_log.txt")

        log_bucket = s3_client.get_object_by_filename(name_file_to_bucket)

        if log_bucket is not None:
            size_log_bucket = len(log_bucket.read())
            if size_path_local < size_log_bucket:
                name_file_to_bucket = (
                    f"{datetime.now().strftime('%Y%m%d%H%M%S')}_access.txt"
                )

            with open("access_log.txt", "rb") as file_obj:
                s3_client.upload_image(file_obj, name_file_to_bucket)


@scheduler.task(
    "cron",
    id="job_enviar_email_ativar_cadastro",
    day="*",
    hour="14",
    minute="15",
)
def job_enviar_email_ativar_cadastro():
    with scheduler.app.app_context():
        try:
            tres_dias_atras = get_current_time().date() - timedelta(days=3)

            usuarios = Usuario.query.filter(
                Usuario.status == False,
                db.func.cast(Usuario.data_inicio, db.Date) == tres_dias_atras,
            ).all()

            for usuario in usuarios:
                try:
                    payload = {"email": usuario.email}
                    token = generate_token(
                        obj=payload, salt="active_account_confirmation"
                    )
                    html = reminder_active_account_email_template(
                        usuario.nome, token
                    )
                    send_email(
                        "HeSed - Verificação de Email", usuario.email, html, 1
                    )
                except Exception as err:
                    logging.error(
                        f"{get_current_time()} - job_enviar_email_ativar_cadastro: OCORREU UM ERRO AO ENVIAR O LEMBRETE DE ATIVAÇÃO DE CONTA -> {type(err)} - {err}"
                    )
                    continue

        except Exception as err:
            logging.error(
                f"{get_current_time()} - job_enviar_email_ativar_cadastro: OCORREU UM ERRO AO EXECUTAR O JOB -> {type(err)} - {err}"
            )


@scheduler.task(
    "cron",
    id="job_enviar_email_feliz_aniversario",
    day="*",
    hour="11",
    minute="15",
)
def job_enviar_email_feliz_aniversario():
    with scheduler.app.app_context():
        try:
            data_atual = get_current_time()

            dia_atual = data_atual.day
            mes_atual = data_atual.month

            usuarios = Clifor.query.filter(
                db.func.day(Clifor.data_nascimento) == dia_atual,
                db.func.month(Clifor.data_nascimento) == mes_atual,
            ).all()

            for usuario in usuarios:
                html = happy_birthday_email_template(usuario.nome)
                try:
                    send_email(
                        "Instituto Hesed - Feliz Aniversário",
                        usuario.email,
                        html,
                        8,
                    )
                except Exception as err:
                    logging.error(
                        f"{get_current_time()} - job_enviar_email_feliz_aniversario: OCORREU UM ERRO AO ENVIAR O EMAIL -> {type(err)} - {err}"
                    )
                    continue

        except Exception as err:
            logging.error(
                f"{get_current_time()} - job_enviar_email_feliz_aniversario: OCORREU UM ERRO AO EXECUTAR O JOB -> {type(err)} - {err}"
            )


@scheduler.task(
    "cron",
    id="job_enviar_email_lembrete_doacao_recorrente",
    day="*",
    hour="16",
    minute="30",
)
def job_enviar_email_lembrete_doacao_recorrente():
    with scheduler.app.app_context():
        try:
            s3_client = file_service_factory()

            data_atual = get_current_time().date()
            data_cinco_dias_depois = data_atual + timedelta(days=5)

            dia_atual = data_atual.day
            cinco_dias_depois = data_cinco_dias_depois.day

            pedidos = (
                Pedido.query.join(
                    Campanha, Campanha.id == Pedido.fk_campanha_id
                )
                .filter(
                    db.or_(
                        Pedido.fk_forma_pagamento_id == 2,
                        Pedido.fk_forma_pagamento_id == 3,
                    ),
                    Pedido.status_pedido == 1,
                    Pedido.recorrencia_ativa == True,
                    Pedido.periodicidade == 2,
                    Pedido.contabilizar_doacao == True,
                    Campanha.status == True,
                    db.or_(
                        db.func.day(Pedido.data_pedido) == dia_atual,
                        db.func.day(Pedido.data_pedido) == cinco_dias_depois,
                    ),
                )
                .all()
            )

            for pedido in pedidos:
                processamento_pedido = (
                    ProcessamentoPedido.query.filter_by(fk_pedido_id=pedido.id)
                    .order_by(ProcessamentoPedido.data_criacao.desc())
                    .first()
                )
                clifor = db.session.get(Clifor, pedido.fk_clifor_id)
                campanha = db.session.get(Campanha, pedido.fk_campanha_id)
                forma_pagamento = db.session.get(
                    FormaPagamento, pedido.fk_forma_pagamento_id
                )

                foto_campanha = s3_client.get_public_url(campanha.filename)

                PAYMENT_TYPE_MAP = {
                    2: {
                        "payment_type": "pix",
                        "payment_salt": "send_email_pix_recurrence_payment",
                    },
                    3: {
                        "payment_type": "invoice",
                        "payment_salt": "send_email_invoice_recurrence_payment",
                    },
                }

                payment_type = PAYMENT_TYPE_MAP[pedido.fk_forma_pagamento_id]

                obj_user = {
                    "id": clifor.fk_usuario_id,
                    "fk_processamento_pedido_id": processamento_pedido.id,
                    "fk_pedido_id": pedido.id,
                    "fk_gateway_pagamento_id": pedido.fk_gateway_pagamento_id,
                }

                data_vencimento = (
                    processamento_pedido.data_criacao + relativedelta(days=31)
                ).strftime("%d/%m/%Y")

                token = generate_token(
                    obj=obj_user, salt=payment_type.get("payment_salt")
                )

                html = reminder_recurrence_donation_email_template(
                    nome_benfeitor=clifor.nome,
                    campanha_id=campanha.id,
                    nome_campanha=campanha.titulo,
                    foto_campanha=foto_campanha,
                    tipo_pagamento=payment_type.get("payment_type"),
                    metodo_pagamento=forma_pagamento.descricao,
                    data_vencimento=data_vencimento,
                    token=token,
                )

                try:
                    send_email(
                        "Instituto Hesed - Lembrete de Doação",
                        clifor.email,
                        html,
                        7,
                    )
                except Exception as err:
                    logging.error(
                        f"{get_current_time()} - job_enviar_email_lembrete_doacao_recorrente: OCORREU UM ERRO AO ENVIAR O EMAIL -> {type(err)} - {err}"
                    )
                    continue

        except Exception as err:
            logging.error(
                f"{get_current_time()} - job_enviar_email_lembrete_doacao_recorrente: OCORREU UM ERRO AO EXECUTAR O JOB -> {type(err)} - {err}"
            )


@scheduler.task(
    "cron",
    id="job_atualiza_status_familia_agape",
    day="*",
    hour="23",
    minute="59",
)
def job_atualiza_status_familia_agape():
    with scheduler.app.app_context():
        try:
            data_corte = get_current_time().date()
            data_corte -= relativedelta(months=3)

            subquery = (
                db.session.query(
                    DoacaoAgape.fk_familia_agape_id.label("familia_id"),
                    func.max(cast(DoacaoAgape.created_at, Date)).label(
                        "ultima_doacao"
                    ),
                )
                .group_by(DoacaoAgape.fk_familia_agape_id)
                .subquery()
            )

            familias_query = FamiliaAgape.query.outerjoin(
                subquery, subquery.c.familia_id == FamiliaAgape.id
            ).filter(
                or_(
                    subquery.c.ultima_doacao < data_corte,
                    subquery.c.ultima_doacao.is_(None),
                ),
                FamiliaAgape.status == True,
            )
            familias = familias_query.all()

            for familia in familias:
                familia.status = False

            try:
                db.session.commit()
            except Exception as exception:
                db.session.rollback()
                raise exception

        except Exception as err:
            logging.error(
                f"{get_current_time()} - job_atualiza_status_familia_agape: OCORREU UM ERRO AO EXECUTAR O JOB -> {type(err)} - {err}"
            )


# @scheduler.task("cron", id="job_atualiza_status_pagamento_pix_1_minuto", day="*", hour="*", minute="*")
# def job_atualiza_status_pagamento_pix_1_minuto():
#     logging.error('Inicializando verificação de pagamento pix de 1 minuto')
#     with scheduler.app.app_context():
#         data_atual = datetime.now()
#         data_limite = data_atual - timedelta(minutes=10)

#         pagamentos_pix = ProcessamentoPedido.query.filter(
#             ProcessamentoPedido.fk_forma_pagamento_id == 2,
#             ProcessamentoPedido.status_processamento == 0,
#             ProcessamentoPedido.data_processamento >= data_limite,
#             ProcessamentoPedido.transaction_id.isnot(None))

#         pagamentos_pix = pagamentos_pix.all()

#         if not pagamentos_pix:
#             logging.error(
#                 'Nenhum pagamento tipo pix encontrado.. Fim de processo!')
#             return

#         with db.session.begin_nested():
#             for pagamento in pagamentos_pix:
#                 path = f"/cobv/{pagamento.transaction_id}"

#                 try:
#                     itau_api = ItauAPI("pix")
#                     response, status = itau_api.get(path=path)

#                 except Exception as err:
#                     logging.error(
#                         f"{datetime.now()} - job_atualiza_status_pagamento_pix_1_minuto -> Erro ao atualizar ID {pagamento.id}: {type(err)} - {err}")
#                     continue

#                 if status != 200:
#                     logging.error(
#                         f"{datetime.now()} - job_atualiza_status_pagamento_pix_1_minuto -> Erro ao atualizar ID {pagamento.id}: ----> {response}")
#                     continue

#                 if response["status"] == "CONCLUIDA":
#                     pagamento.status_processamento = 1

#             try:
#                 db.session.commit()
#             except Exception as err:
#                 db.session.rollback()
#                 logging.error(
#                     f"{datetime.now()} - job_atualiza_status_pagamento_pix_1_minuto -> Erro ao atualizar ID {pagamento.id}: {type(err)} - {err}")


# @scheduler.task("cron", id="job_atualiza_status_pagamento_pix_10_minutos", day="*", hour="*", minute="*/10")
# def job_atualiza_status_pagamento_pix_10_minutos():
#     with scheduler.app.app_context():
#         data_atual = datetime.now()
#         data_limite = data_atual - timedelta(minutes=10)
#         data_expiracao = data_atual - timedelta(days=31)

#         pagamentos_pix_validos = ProcessamentoPedido.query.filter(
#             ProcessamentoPedido.fk_forma_pagamento_id == 2,
#             ProcessamentoPedido.status_processamento == 0,
#             ProcessamentoPedido.data_processamento < data_limite,
#             ProcessamentoPedido.data_processamento > data_expiracao,
#             ProcessamentoPedido.transaction_id.isnot(None)).all()

#         pagamentos_pix_expirados = ProcessamentoPedido.query.filter(
#             ProcessamentoPedido.fk_forma_pagamento_id == 2,
#             ProcessamentoPedido.status_processamento == 0,
#             ProcessamentoPedido.data_processamento < data_expiracao).all()

#         if not pagamentos_pix_validos and not pagamentos_pix_expirados:
#             return

#         with db.session.begin_nested():
#             for pagamento in pagamentos_pix_validos:
#                 path = f"/cobv/{pagamento.transaction_id}"

#                 try:
#                     itau_api = ItauAPI("pix")
#                     response, status = itau_api.get(path=path)

#                 except Exception as err:
#                     logging.error(
#                         f"{datetime.now()} - job_atualiza_status_pagamento_pix_10_minutos -> Erro ao atualizar ID {pagamento.id}: {type(err)} - {err}")
#                     continue

#                 if status != 200:
#                     logging.error(
#                         f"{datetime.now()} - job_atualiza_status_pagamento_pix_10_minutos -> Erro ao atualizar ID {pagamento.id}: ----> {response}")
#                     continue

#                 if response["status"] == "CONCLUIDA":
#                     pagamento.status_processamento = 1

#             for pagamento in pagamentos_pix_expirados:
#                 pagamento.status_processamento = 3

#             try:
#                 db.session.commit()
#             except Exception as err:
#                 db.session.rollback()
#                 logging.error(
#                     f"{datetime.now()} - job_atualiza_status_pagamento_pix_10_minutos -> Erro ao atualizar ID {pagamento.id}: {type(err)} - {err}")

# @scheduler.task("cron", id="job_registra_usuarios_pagamento_pix_itau", day="*", hour="*", minute="*")
# def job_registra_usuarios_pagamento_pix_itau():
#     with scheduler.app.app_context():
#         try:
#             campanhas = Campanha.query.filter(Campanha.status == True).all()
#             if not campanhas:
#                 return

#             itau_api = ItauAPI("pix_recebimentos")
#             path = "/lancamentos_pix"
#             hora_atual = (datetime.now(timezone.utc) - timedelta(hours=3)
#                           ).strftime("%Y-%m-%dT%H:%M")
#             hora_anterior = (datetime.now(timezone.utc) - timedelta(hours=4)
#                              ).strftime("%Y-%m-%dT%H:%M")
#             MAP_CPF_CNPJ = {
#                 11: "f",
#                 14: "j"
#             }

#             for campanha in campanhas:
#                 query_params = {
#                     "data_lancamento": f"{hora_anterior},{hora_atual}",
#                     "chaves": campanha.chave_pix,
#                     "visao": "emissor",
#                     "page_size": 1000
#                 }

#                 response, status = itau_api.get(path=path, params=query_params)

#                 if status != 200:
#                     logging.error(
#                         f"{get_current_time()} - job_registra_usuarios_pagamento_pix_itau -> Erro ao consultar chave pix {campanha.chave_pix} da campanha {campanha.titulo}: ----> {response}")
#                     continue

#                 for data in response["data"]:
#                     payload_usuario = data["detalhe_pagamento"]["debitado"]
#                     payload_pagamento = data["detalhe_pagamento"]
#                     payload_valor = data["detalhe_pagamento"]["detalhe_valor"]
#                     cpf_cnpj = payload_usuario["numero_documento"]
#                     nome = payload_usuario["nome"]
#                     data_pagamento = payload_pagamento["data"]
#                     valor_pagamento = payload_valor["valor"]
#                     txid = data["detalhe_pagamento"]["txid"]

#                     txid_pedido = ProcessamentoPedido.query.filter_by(
#                         transaction_id=txid).first()

#                     if txid_pedido:
#                         continue

#                     clifor = Clifor.query.filter_by(cpf_cnpj=cpf_cnpj).first()

#                     if clifor and clifor.fk_usuario_id is not None:
#                         reference_num = f"{clifor.fk_usuario_id}_PIX_{datetime.timestamp(datetime.now())}"
#                     else:
#                         reference_num = f"0_PIX_{datetime.timestamp(datetime.now())}"

#                     with db.session.begin_nested():
#                         if not clifor:
#                             clifor = Clifor(
#                                 fk_empresa_id=campanha.fk_empresa_id,
#                                 tipo_clifor=MAP_CPF_CNPJ[len(cpf_cnpj)],
#                                 nome=nome,
#                                 cpf_cnpj=cpf_cnpj
#                             )

#                             db.session.add(clifor)
#                             db.session.flush()

#                         pedido = Pedido(
#                             fk_empresa_id=campanha.fk_empresa_id,
#                             fk_clifor_id=clifor.id,
#                             fk_campanha_id=campanha.id,
#                             fk_forma_pagamento_id=2,
#                             data_pedido=data_pagamento,
#                             periodicidade=1,
#                             status_pedido=1,
#                             valor_total_pedido=valor_pagamento,
#                             anonimo=True,
#                             recorrencia_ativa=False,
#                             usuario_criacao=0,
#                             fk_gateway_pagamento_id=1
#                         )

#                         db.session.add(pedido)
#                         db.session.flush()

#                         processamento_pedido = ProcessamentoPedido(
#                             fk_empresa_id=campanha.fk_empresa_id,
#                             fk_pedido_id=pedido.id,
#                             fk_clifor_id=clifor.id,
#                             fk_forma_pagamento_id=2,
#                             data_processamento=data_pagamento,
#                             valor=valor_pagamento,
#                             status_processamento=1,
#                             id_transacao_gateway=reference_num,
#                             transaction_id=txid,
#                             usuario_criacao=0
#                         )

#                         db.session.add(processamento_pedido)

#                     db.session.commit()

#         except Exception as err:
#             db.session.rollback()
#             logging.error(
#                 f"{get_current_time()} - job_registra_usuarios_pagamento_pix_itau -> Ocorreu um erro ao executar a rotina.\nERROR: {type(err)} - {err}")


# @scheduler.task("cron", id="job_send_activation_emails", hour="11", minute="30")
# def job_send_activation_emails():
#     with scheduler.app.app_context():
#         print("Job iniciado:", datetime.now())

#         yesterday = datetime.now() - timedelta(days=1)
#         today = datetime.now()

#         emails_sent_yesterday = db.session.query(SendEmailsInactives.email_send).filter(SendEmailsInactives.send_date == yesterday).all()
#         emails_sent_yesterday = [email[0] for email in emails_sent_yesterday]

#         emails_to_send = db.session.query(Usuario.email, Usuario.nome)\
#                         .filter(Usuario.status != 1, Usuario.email.notin_(emails_sent_yesterday))\
#                         .order_by(Usuario.data_criacao)\
#                         .limit(100).all()

#         for email, nome in emails_to_send:
#             try:
#                 token = generate_token(
#                     obj=email, salt="active_account_confirmation")
#                 html = active_account_email_template_for_emails_inactives(nome, token)
#                 send_email("HeSed - Verificação de Email", [email], html)
#                 email_log = SendEmailsInactives(email_send=email, send_date=today)
#                 db.session.add(email_log)
#             except Exception as e:
#                 logging.exception(f"Erro ao enviar e-mail para {email}: {e}")
#                 continue
#         db.session.commit()
#         print(f"{len(emails_to_send)} emails enviados.")
