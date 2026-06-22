from app import db


class Endereco(db.Model):
    __tablename__ = "enderecos"

    id = db.Column(db.Integer, primary_key=True)

    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    cliente = db.relationship("Cliente", backref="enderecos")

    cep = db.Column(db.String(20))
    logradouro = db.Column(db.String(180))
    numero = db.Column(db.String(30))
    complemento = db.Column(db.String(120))
    bairro = db.Column(db.String(120))
    cidade = db.Column(db.String(120))
    estado = db.Column(db.String(2))