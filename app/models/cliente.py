from datetime import datetime
from app import db


class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=True)
    telefone = db.Column(db.String(30), nullable=True)
    cpf = db.Column(db.String(20), nullable=True)

    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)