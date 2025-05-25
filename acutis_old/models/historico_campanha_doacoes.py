from builder import db
from datetime import datetime


class HistoricoCampanhaDonations(db.Model):
    __tablename__ = "historico_campanha_doacoes"

    id = db.Column(db.Integer, primary_key=True)
    fk_campanha_id = db.Column(
        db.Integer,
        db.ForeignKey("campanha.id", ondelete="CASCADE"),
        nullable=False,
    )
    mes_ano = db.Column(db.String, nullable=False)
    valor_meta = db.Column(db.Numeric(10, 2), nullable=True)
    valor_atingido = db.Column(db.Numeric(10, 2), nullable=True)
    data_alteracao = db.Column(db.Date)
    mes_ano = db.Column(db.Date, nullable=False)
    usuario_alteracao_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    deleted_at = db.Column(db.DateTime)

    campanha = db.relationship(
        "Campanha", backref="historico_campanha_donations"
    )
    usuario_alteracao = db.relationship("Usuario")

    def soft_delete(self):
        self.deleted_at = datetime.now()
        db.session.commit()

    def __init__(
        self,
        fk_campanha_id,
        mes_ano,
        valor_meta,
        valor_atingido=None,
        data_alteracao=None,
        usuario_alteracao_id=None,
    ):
        self.fk_campanha_id = fk_campanha_id
        self.mes_ano = mes_ano
        self.valor_meta = valor_meta
        self.valor_atingido = valor_atingido
        self.data_alteracao = data_alteracao
        self.usuario_alteracao_id = usuario_alteracao_id

    def to_dict(self):
        return {
            "id": self.id,
            "fk_campanha_id": self.fk_campanha_id,
            "mes_ano": self.mes_ano,
            "valor_meta": self.valor_meta,
            "valor_atingido": self.valor_atingido,
            "data_alteracao": (
                self.data_alteracao.strftime("%d-%m-%Y")
                if self.data_alteracao
                else None
            ),
            "usuario_alteracao_id": self.usuario_alteracao_id,
            "deleted_at": self.deleted_at,
        }

    def __repr__(self) -> str:
        return f"<HistoricoCampanhaDonations(id={self.id}, fk_campanha_id={self.fk_campanha_id}, mes_ano={self.mes_ano}, valor_meta={self.valor_meta}, valor_atingido={self.valor_atingido}, usuario_alteracao_id={self.usuario_alteracao_id})>"
