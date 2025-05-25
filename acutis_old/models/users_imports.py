from builder import db
from email_validator import validate_email, EmailNotValidError


class UsersImports(db.Model):
    __tablename__ = "users_imports"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(1010), nullable=False)
    email = db.Column(db.String(1010), nullable=False, index=True)
    data_criacao = db.Column(db.DateTime, nullable=True)
    phone = db.Column(db.String(1010), nullable=True)
    origem_cadastro = db.Column(
        db.Integer, db.ForeignKey("actions_leads.id"), nullable=False
    )
    intencao = db.Column(db.String(250))
    updated_at = db.Column(db.DateTime, nullable=True)

    action_lead = db.relationship(
        "ActionsLeads", backref="users_imports", lazy=True
    )

    def validar_email(self, email):
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "data_criacao": self.data_criacao,
            "phone": self.phone,
            "intencao": self.intencao,
        }

    def __repr__(self) -> str:
        return f"<UsuarioImports {self.nome}>"
