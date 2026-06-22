from datetime import datetime
from app import db


class Categoria(db.Model):
    __tablename__ = "categorias"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(
        db.String(120),
        nullable=False
    )

    slug = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    descricao = db.Column(
        db.Text
    )

    imagem = db.Column(
        db.String(255)
    )

    destaque = db.Column(
        db.Boolean,
        default=False
    )

    ordem = db.Column(
        db.Integer,
        default=0
    )

    ativo = db.Column(
        db.Boolean,
        default=True
    )

    data_cadastro = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )