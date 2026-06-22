from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app():

    app = Flask(__name__)

    app.config.from_object("config.Config")

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Faça login para continuar."

    # IMPORTAÇÃO DOS MODELOS
    from app.models.usuario import Usuario
    from app.models.categoria import Categoria
    from app.models.produto import Produto
    from app.models.produto_imagem import ProdutoImagem
    from app.models.estoque import Estoque
    from app.models.cliente import Cliente
    from app.models.endereco import Endereco
    from app.models.pedido import Pedido
    from app.models.pedido_item import PedidoItem
    from app.models.carrinho import CarrinhoItem
    from app.models.configuracao import Configuracao

    # IMPORTAÇÃO DAS ROTAS
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.categorias import categorias_bp
    from app.routes.produtos import produtos_bp
    from app.routes.estoque import estoque_bp
    from app.routes.clientes import clientes_bp
    from app.routes.pedidos import pedidos_bp
    from app.routes.loja import loja_bp
    from app.routes.configuracoes import configuracoes_bp
    from app.routes.carrinho import carrinho_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(produtos_bp)
    app.register_blueprint(estoque_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(pedidos_bp)
    app.register_blueprint(loja_bp)
    app.register_blueprint(configuracoes_bp)
    app.register_blueprint(carrinho_bp)

    return app