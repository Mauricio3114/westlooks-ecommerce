from datetime import datetime
from app import db


class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)

    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=True)
    cliente = db.relationship("Cliente", backref="pedidos")

    valor_total = db.Column(db.Numeric(10, 2), default=0)

    status = db.Column(db.String(50), default="aguardando_pagamento")
    forma_pagamento = db.Column(db.String(50), nullable=True)

    mercado_pago_payment_id = db.Column(db.String(120), nullable=True)
    pix_copia_cola = db.Column(db.Text, nullable=True)
    pix_qr_code_base64 = db.Column(db.Text, nullable=True)
    pix_ticket_url = db.Column(db.Text, nullable=True)

    observacao = db.Column(db.Text, nullable=True)

    data_pedido = db.Column(db.DateTime, default=datetime.utcnow)

    tipo_entrega = db.Column(db.String(50), default="fortaleza")
    valor_entrega = db.Column(db.Numeric(10, 2), default=0)

    codigo_rastreamento = db.Column(db.String(120))
    transportadora = db.Column(db.String(120))
    data_envio = db.Column(db.DateTime)
    data_entrega = db.Column(db.DateTime)
    data_pagamento = db.Column(db.DateTime)
    data_preparacao = db.Column(db.DateTime)

    itens = db.relationship(
        "PedidoItem",
        backref="pedido",
        lazy=True,
        cascade="all, delete-orphan"
    )