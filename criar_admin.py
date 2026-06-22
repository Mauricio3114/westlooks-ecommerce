from app import create_app, db
from app.models.usuario import Usuario

app = create_app()

with app.app_context():

    usuario = Usuario.query.filter_by(
        email="admin@westlooks.com"
    ).first()

    if not usuario:

        usuario = Usuario(
            nome="Administrador",
            email="admin@westlooks.com",
            perfil="admin",
            ativo=True
        )

        usuario.set_senha("123456")

        db.session.add(usuario)
        db.session.commit()

        print("ADMIN CRIADO COM SUCESSO")

    else:
        print("ADMIN JÁ EXISTE")