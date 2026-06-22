from datetime import datetime
from app import db


class CarrinhoItem(db.Model):
    __tablename__ = "carrinho_itens"

    id = db.Column(db.Integer, primary_key=True)

    session_id = db.Column(db.String(120), nullable=False)

    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=False)
    produto = db.relationship("Produto")

    numeracao = db.Column(db.String(20), nullable=False)

    quantidade = db.Column(db.Integer, default=1)

    valor_unitario = db.Column(db.Numeric(10, 2), default=0)

    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def subtotal(self):
        return float(self.valor_unitario or 0) * int(self.quantidade or 0)