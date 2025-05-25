from builder import db
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PedidosDeOracao(db.Model):
    __tablename__ = "pedidos_de_oracao"

    id = db.Column(db.Integer, primary_key=True)
    fk_usuario_criacao = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id"),
        nullable=False,
    )
    autor = db.Column(db.Text, nullable=False)
    destinado = db.Column(db.Text, nullable=False)
    dados_publicos = db.Column(db.Boolean, nullable=False)
    descricao_pedido = db.Column(db.Text, nullable=False)
    leitura_publica = db.Column(db.Boolean, nullable=False)
    status = db.Column(db.String, nullable=False, default="aberto")
    local_realizacao = db.Column(db.Text, nullable=True)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    data_realizacao = db.Column(db.DateTime, nullable=True)

    usuario_criacao = db.relationship("Usuario", backref="pedidos_de_oracao")

    def to_dict(self):
        return {
            "id": self.id,
            "fk_usuario_criacao": self.fk_usuario_criacao,
            "autor": self.autor,
            "destinado": self.destinado,
            "dados_publicos": bool(self.dados_publicos),
            "descricao_pedido": self.descricao_pedido,
            "leitura_publica": self.leitura_publica,
            "status": self.status,
            "local_realizacao": self.local_realizacao,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "data_realizacao": (
                self.data_realizacao.strftime("%Y-%m-%d %H:%M:%S")
                if self.data_realizacao
                else None
            ),
        }

    def __repr__(self):
        return f"Pedido(id={self.id}, autor='{self.autor}', destinado='{self.destinado}', status='{self.status}')"


class SchemaPedidoDeOracao(BaseModel):
    fk_usuario_criacao: int
    autor: str
    destinado: str
    dados_publicos: bool
    descricao_pedido: str
    leitura_publica: bool
    local_realizacao: Optional[str]
