from builder import db


class ListExceptionDonations(db.Model):
    __tablename__ = "list_exception_donations"

    id = db.Column(db.Integer, primary_key=True)
    fk_clifor_id = db.Column(
        db.Integer, db.ForeignKey("clifor.id"), nullable=False
    )
    fk_usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    nome = db.Column(db.String(130), nullable=False)
    cpf_cnpj = db.Column(db.String(20))
    data_inclusao = db.Column(db.DateTime)
    incluido_por = db.Column(db.Integer)

    clifor = db.relationship(
        "Clifor", backref="exceptions_donations", lazy=True
    )
    usuario = db.relationship(
        "Usuario", backref="exceptions_donations", lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "fk_clifor_id": self.fk_clifor_id,
            "fk_usuario_id": self.fk_usuario_id,
            "cpf_cnpj": self.cpf_cnpj,
            "data_inclusao": self.data_inclusao,
            "incluido_por": self.incluido_por,
        }

    def __repr__(self) -> str:
        return f"<ListExceptionDonations {self.nome}, {self.cpf_cnpj}, {self.fk_clifor_id}>"
