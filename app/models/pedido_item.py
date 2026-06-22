from app import db


class PedidoItem(db.Model):
    __tablename__ = "pedido_itens"

    id = db.Column(db.Integer, primary_key=True)

    pedido_id = db.Column(
        db.Integer,
        db.ForeignKey("pedidos.id")
    )

    produto_id = db.Column(
        db.Integer,
        db.ForeignKey("produtos.id")
    )

    quantidade = db.Column(db.Integer)

    valor_unitario = db.Column(db.Numeric(10,2))

    subtotal = db.Column(db.Numeric(10,2))

    numeracao = db.Column(
        db.String(10)
    )

    produto = db.relationship("Produto")