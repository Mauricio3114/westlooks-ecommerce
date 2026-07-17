from app import db


class ProdutoImagem(db.Model):
    __tablename__ = "produto_imagens"

    id = db.Column(db.Integer, primary_key=True)

    produto_id = db.Column(
        db.Integer,
        db.ForeignKey("produtos.id", ondelete="CASCADE"),
        nullable=False
    )

    produto = db.relationship(
        "Produto",
        backref=db.backref(
            "imagens",
            cascade="all, delete-orphan",
            passive_deletes=True
        )
    )

    imagem = db.Column(
        db.String(255),
        nullable=False
    )

    principal = db.Column(
        db.Boolean,
        default=False
    )