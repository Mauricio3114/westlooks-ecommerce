from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.produto import Produto
from app.models.categoria import Categoria
from app.models.estoque import Estoque


loja_bp = Blueprint("loja", __name__)


@loja_bp.route("/")
@loja_bp.route("/loja")
def home():
    produtos = Produto.query.filter_by(
        ativo=True
    ).order_by(
        Produto.data_cadastro.desc()
    ).limit(12).all()

    destaques = Produto.query.filter_by(
        ativo=True,
        destaque=True
    ).order_by(
        Produto.data_cadastro.desc()
    ).limit(8).all()

    lancamentos = Produto.query.filter_by(
        ativo=True,
        lancamento=True
    ).order_by(
        Produto.data_cadastro.desc()
    ).limit(8).all()

    categorias = Categoria.query.filter_by(
        ativo=True
    ).order_by(
        Categoria.ordem.asc()
    ).all()

    return render_template(
        "loja/home.html",
        produtos=produtos,
        destaques=destaques,
        lancamentos=lancamentos,
        categorias=categorias
    )


@loja_bp.route("/produto/<slug>")
def detalhe_produto(slug):
    produto = Produto.query.filter_by(slug=slug, ativo=True).first_or_404()

    from app.models.estoque import Estoque

    estoques = Estoque.query.filter(
        Estoque.produto_id == produto.id,
        Estoque.quantidade > 0
    ).order_by(
        Estoque.numeracao.asc()
    ).all()

    categorias = Categoria.query.filter_by(ativo=True).order_by(Categoria.ordem.asc()).all()

    estoques = Estoque.query.filter(
        Estoque.produto_id == produto.id,
        Estoque.quantidade > 0
    ).order_by(Estoque.numeracao.asc()).all()

    return render_template(
        "loja/produto.html",
        produto=produto,
        estoques=estoques
    )


@loja_bp.route("/acompanhar/<int:pedido_id>")
def acompanhar_pedido(pedido_id):

    from app.models.pedido import Pedido

    pedido = Pedido.query.get_or_404(
        pedido_id
    )

    return render_template(
        "loja/acompanhar_pedido.html",
        pedido=pedido
    )


@loja_bp.route("/consultar-pedido", methods=["GET", "POST"])
def consultar_pedido():

    from app.models.pedido import Pedido

    pedido = None

    if request.method == "POST":

        numero = request.form.get("pedido")
        cpf = request.form.get("cpf")

        pedido = Pedido.query.filter(
            Pedido.id == numero
        ).first()

        if not pedido:
            flash("Pedido não encontrado.", "danger")
            return redirect(url_for("loja.consultar_pedido"))

        if pedido.cliente.cpf.replace(".", "").replace("-", "") != cpf.replace(".", "").replace("-", ""):
            flash("CPF não confere com o pedido.", "danger")
            return redirect(url_for("loja.consultar_pedido"))

        return redirect(
            url_for(
                "loja.acompanhar_pedido",
                pedido_id=pedido.id
            )
        )

    return render_template(
        "loja/consultar_pedido.html"
    )


@loja_bp.route("/sobre-nos")
def sobre():
    return render_template("loja/sobre.html")


@loja_bp.route("/trocas-e-devolucoes")
def trocas():
    return render_template("loja/trocas.html")


@loja_bp.route("/politica-de-privacidade")
def privacidade():
    return render_template("loja/privacidade.html")