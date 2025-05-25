from datetime import datetime

from builder import db


class Boleto(db.Model):
    __tablename__ = "boleto"

    id = db.Column(db.Integer, primary_key=True)
    fk_empresa_id = db.Column(
        db.Integer, db.ForeignKey("empresa.id"), nullable=False
    )
    fk_carteira_cod = db.Column(
        db.String(10), db.ForeignKey("carteira.cod_carteira"), nullable=False
    )
    fk_convenio_id = db.Column(
        db.Integer, db.ForeignKey("convenio.id"), nullable=False
    )
    fk_filial_id = db.Column(
        db.Integer, db.ForeignKey("filial.id"), nullable=False
    )
    fk_clifor_id = db.Column(
        db.Integer, db.ForeignKey("clifor.id"), nullable=False
    )
    status_boleto = db.Column(db.SmallInteger, nullable=False)
    status_cnab = db.Column(db.SmallInteger)
    comando_cnab = db.Column(db.SmallInteger)
    data_emissao = db.Column(db.DateTime, nullable=False)
    data_vencimento = db.Column(db.DateTime, nullable=False)
    data_cancelamento = db.Column(db.DateTime)
    valor_boleto = db.Column(db.Numeric(15, 4), nullable=False)
    valor_baixado = db.Column(db.Numeric(15, 4))
    valor_desconto = db.Column(db.Numeric(15, 4))
    juros_ao_dia = db.Column(db.Numeric(15, 4))
    valor_juros = db.Column(db.Numeric(15, 4), nullable=False)
    valor_multa = db.Column(db.Numeric(15, 4), nullable=False)
    codigo_barra = db.Column(db.String(45))
    ipte = db.Column(db.String(48))
    nosso_numero = db.Column(db.String(20))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_criacao = db.Column(db.Integer, nullable=False)
    data_alteracao = db.Column(db.DateTime)
    usuario_alteracao = db.Column(db.Integer)
