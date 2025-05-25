from datetime import datetime

from builder import db


class Lancamento(db.Model):
    __tablename__ = "lancamento"

    id = db.Column(db.Integer, primary_key=True)
    fk_empresa_id = db.Column(
        db.Integer, db.ForeignKey("empresa.id"), nullable=False
    )
    fk_filial_id = db.Column(
        db.Integer, db.ForeignKey("filial.id"), nullable=False
    )
    fk_clifor_id = db.Column(
        db.Integer, db.ForeignKey("clifor.id"), nullable=False
    )
    fk_tipo_documento_id = db.Column(
        db.Integer, db.ForeignKey("tipo_documento.id"), nullable=False
    )
    fk_sistema_id = db.Column(
        db.Integer, db.ForeignKey("sistema.id"), nullable=False
    )
    fk_carteira_cod = db.Column(
        db.String(10), db.ForeignKey("carteira.cod_carteira"), nullable=False
    )
    fk_boleto_id = db.Column(db.Integer, db.ForeignKey("boleto.id"))
    natureza = db.Column(db.String(1), nullable=False)
    numero_documento = db.Column(db.String(40), nullable=False, unique=True)
    serie_documento = db.Column(db.String(8))
    status_lancamento = db.Column(db.SmallInteger, nullable=False)
    id_processo = db.Column(db.Integer)
    data_criacao = db.Column(db.DateTime, nullable=False)
    data_emissao = db.Column(db.DateTime, nullable=False)
    data_vencimento = db.Column(db.DateTime, nullable=False)
    data_previsao_baixa = db.Column(db.DateTime)
    data_baixa = db.Column(db.DateTime)
    data_cancelamento = db.Column(db.DateTime)
    historico = db.Column(db.String(255))
    mes_competencia = db.Column(db.DateTime)
    valor_original = db.Column(db.Numeric(15, 4), nullable=False)
    valor_baixado = db.Column(db.Numeric(15, 4), nullable=False)
    valor_juros = db.Column(db.Numeric(15, 4), nullable=False)
    valor_multa = db.Column(db.Numeric(15, 4), nullable=False)
    codigo_barra = db.Column(db.String(45))
    ipte = db.Column(db.String(48))
    nosso_numero_cnab = db.Column(db.String(20))
    numero_parcela = db.Column(db.Integer)
    id_classific_financ = db.Column(db.String(25))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_criacao = db.Column(db.Integer, nullable=False)
    data_alteracao = db.Column(db.DateTime)
    usuario_alteracao = db.Column(db.Integer)
