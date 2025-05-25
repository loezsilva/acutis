from datetime import datetime

from builder import db


class ItemPedido(db.Model):
    __tablename__ = "item_pedido"

    id = db.Column(db.Integer, primary_key=True)
    fk_empresa_id = db.Column(
        db.Integer, db.ForeignKey("empresa.id"), nullable=False
    )
    fk_produto_id = db.Column(
        db.Integer, db.ForeignKey("produto.id"), nullable=False
    )
    fk_pedido_id = db.Column(
        db.Integer, db.ForeignKey("pedido.id"), nullable=False
    )
    data_pedido = db.Column(db.DateTime)
    quantidade = db.Column(db.Numeric(15, 2), nullable=False)
    valor = db.Column(db.Numeric(15, 4), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_criacao = db.Column(db.Integer, nullable=False)
    data_alteracao = db.Column(db.DateTime)
    usuario_alteracao = db.Column(db.Integer)
