from datetime import datetime
from app import db


class Estoque(db.Model):
    __tablename__ = "estoques"

    id = db.Column(db.Integer, primary_key=True)

    produto_id = db.Column(
        db.Integer,
        db.ForeignKey("produtos.id"),
        nullable=False
    )

    produto = db.relationship(
        "Produto",
        backref="estoques"
    )

    cor = db.Column(db.String(80))
    numeracao = db.Column(db.String(20), nullable=False)

    quantidade = db.Column(db.Integer, default=0)
    estoque_minimo = db.Column(db.Integer, default=0)

    data_atualizacao = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    @property
    def em_alerta(self):
        return self.quantidade <= self.estoque_minimo

    @property
    def descricao_variacao(self):
        return f"{self.cor or 'Sem cor'} - Nº {self.numeracao}"