from datetime import datetime
from app import db


class Produto(db.Model):
    __tablename__ = "produtos"

    id = db.Column(db.Integer, primary_key=True)

    categoria_id = db.Column(
        db.Integer,
        db.ForeignKey("categorias.id")
    )

    categoria = db.relationship(
        "Categoria",
        backref="produtos"
    )

    nome = db.Column(
        db.String(180),
        nullable=False
    )

    slug = db.Column(
        db.String(220),
        unique=True,
        nullable=False
    )

    descricao = db.Column(
        db.Text
    )

    marca = db.Column(
        db.String(120)
    )

    referencia = db.Column(
        db.String(80)
    )

    preco = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        default=0
    )

    preco_promocional = db.Column(
        db.Numeric(10, 2)
    )

    custo = db.Column(
        db.Numeric(10, 2)
    )

    ativo = db.Column(
        db.Boolean,
        default=True
    )

    destaque = db.Column(
        db.Boolean,
        default=False
    )

    lancamento = db.Column(
        db.Boolean,
        default=False
    )

    mais_vendido = db.Column(
        db.Boolean,
        default=False
    )

    frete_gratis = db.Column(
        db.Boolean,
        default=False
    )

    peso = db.Column(
        db.Float,
        default=0
    )

    altura = db.Column(
        db.Float,
        default=0
    )

    largura = db.Column(
        db.Float,
        default=0
    )

    comprimento = db.Column(
        db.Float,
        default=0
    )

    visualizacoes = db.Column(
        db.Integer,
        default=0
    )

    data_cadastro = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )