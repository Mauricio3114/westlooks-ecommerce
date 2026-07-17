from app import db


class ProdutoImagem(db.Model):
    __tablename__ = "produto_imagens"

    id = db.Column(db.Integer, primary_key=True)

    produto_id = db.Column(
        db.Integer,
        db.ForeignKey("produtos.id"),
        nullable=False
    )

    produto = db.relationship(
        "Produto",
        backref="imagens"
    )

    imagem = db.Column(
        db.String(255),
        nullable=False
    )

    principal = db.Column(
        db.Boolean,
        default=False
    )