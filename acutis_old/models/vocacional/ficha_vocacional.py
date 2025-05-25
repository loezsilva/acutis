from dataclasses import dataclass
from datetime import date, datetime
from builder import db
from utils.functions import get_current_time


@dataclass
class FichaVocacional(db.Model):
    __tablename__ = "fichas_vocacional"

    id: int = db.Column(db.Integer, primary_key=True)
    fk_usuario_vocacional_id: int = db.Column(
        db.Integer,
        db.ForeignKey("usuarios_vocacional.id"),
        nullable=False,
        index=True,
    )
    motivacao_instituto: str = db.Column(db.String(255), nullable=False)
    motivacao_admissao_vocacional: str = db.Column(
        db.String(255), nullable=False
    )
    referencia_conhecimento_instituto: str = db.Column(
        db.String(255), nullable=False
    )
    identificacao_instituto: str = db.Column(db.String(255), nullable=False)
    foto_vocacional: str = db.Column(db.String(100), nullable=False)
    seminario_realizado_em: date = db.Column(db.Date, nullable=False)
    testemunho_conversao: str = db.Column(db.String(255), nullable=False)
    escolaridade: str = db.Column(db.String(100), nullable=False)
    profissao: str = db.Column(db.String(100), nullable=False)
    cursos: str = db.Column(db.String(255))
    rotina_diaria: str = db.Column(db.String(255), nullable=False)
    aceitacao_familiar: str = db.Column(db.String(255), nullable=False)
    estado_civil: str = db.Column(db.String(20), nullable=False)
    motivo_divorcio: str = db.Column(db.String(255))
    deixou_religiao_anterior_em: date = db.Column(db.Date)
    remedio_controlado_inicio: date = db.Column(db.Date)
    remedio_controlado_termino: date = db.Column(db.Date)
    descricao_problema_saude: str = db.Column(db.String(255))
    created_at: datetime = db.Column(db.DateTime, default=get_current_time)
    updated_at: datetime = db.Column(db.DateTime)
    
    sacramentos = db.relationship('SacramentoVocacional', backref='ficha_vocacional', cascade='all, delete')
