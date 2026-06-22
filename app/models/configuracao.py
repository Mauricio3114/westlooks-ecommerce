from app import db


class Configuracao(db.Model):
    __tablename__ = "configuracoes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome_loja = db.Column(
        db.String(200)
    )

    whatsapp = db.Column(
        db.String(30)
    )

    instagram = db.Column(
        db.String(100)
    )

    email = db.Column(
        db.String(150)
    )

    tipo_pix = db.Column(
        db.String(50)
    )

    chave_pix = db.Column(
        db.String(255)
    )

    nome_recebedor = db.Column(
        db.String(200)
    )

    mercado_pago_public_key = db.Column(db.String(255))
    mercado_pago_access_token = db.Column(db.Text)