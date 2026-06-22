import uuid

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_required

from app import db
from app.models.produto import Produto
from app.models.carrinho import CarrinhoItem
from app.models.estoque import Estoque


carrinho_bp = Blueprint("carrinho", __name__, url_prefix="/carrinho")


def get_session_id():
    if "carrinho_id" not in session:
        session["carrinho_id"] = str(uuid.uuid4())

    return session["carrinho_id"]


@carrinho_bp.route("/")
def ver():
    session_id = get_session_id()

    itens = CarrinhoItem.query.filter_by(
        session_id=session_id
    ).all()

    total = sum(item.subtotal for item in itens)

    return render_template(
        "loja/carrinho.html",
        itens=itens,
        total=total
    )


@carrinho_bp.route("/adicionar", methods=["POST"])
def adicionar():
    session_id = get_session_id()

    produto_id = request.form.get("produto_id")
    numeracao = request.form.get("numeracao")

    produto = Produto.query.get_or_404(produto_id)

    if not numeracao:
        flash("Escolha uma numeração antes de adicionar ao carrinho.", "warning")
        return redirect(url_for("loja.detalhe_produto", slug=produto.slug))

    valor = produto.preco_promocional if produto.preco_promocional else produto.preco

    item = CarrinhoItem.query.filter_by(
        session_id=session_id,
        produto_id=produto.id,
        numeracao=numeracao
    ).first()

    if item:
        item.quantidade += 1
    else:
        item = CarrinhoItem(
            session_id=session_id,
            produto_id=produto.id,
            numeracao=numeracao,
            quantidade=1,
            valor_unitario=valor
        )
        db.session.add(item)

    db.session.commit()

    flash("Produto adicionado ao carrinho.", "success")
    return redirect(url_for("carrinho.ver"))


@carrinho_bp.route("/remover/<int:id>")
def remover(id):
    item = CarrinhoItem.query.get_or_404(id)

    db.session.delete(item)
    db.session.commit()

    flash("Item removido do carrinho.", "success")
    return redirect(url_for("carrinho.ver"))


@carrinho_bp.route("/checkout", methods=["GET", "POST"])
def checkout():
    session_id = get_session_id()

    itens = CarrinhoItem.query.filter_by(session_id=session_id).all()
    total = sum(item.subtotal for item in itens)

    if not itens:
        flash("Seu carrinho está vazio.", "warning")
        return redirect(url_for("carrinho.ver"))

    if request.method == "POST":
        from app.models.cliente import Cliente
        from app.models.endereco import Endereco
        from app.models.pedido import Pedido
        from app.models.pedido_item import PedidoItem

        for item in itens:
            estoque = Estoque.query.filter_by(
                produto_id=item.produto_id,
                numeracao=item.numeracao
            ).first()

            if not estoque or estoque.quantidade < item.quantidade:
                flash(
                    f"Estoque insuficiente para {item.produto.nome} tamanho {item.numeracao}.",
                    "danger"
                )
                return redirect(url_for("carrinho.ver"))

        cliente = Cliente(
            nome=request.form.get("nome"),
            telefone=request.form.get("telefone"),
            email=request.form.get("email"),
            cpf=request.form.get("cpf")
        )

        db.session.add(cliente)
        db.session.flush()

        endereco = Endereco(
            cliente_id=cliente.id,
            cep=request.form.get("cep"),
            logradouro=request.form.get("logradouro"),
            numero=request.form.get("numero"),
            bairro=request.form.get("bairro"),
            cidade=request.form.get("cidade"),
            estado=request.form.get("estado")
        )

        db.session.add(endereco)

        pedido = Pedido(
            cliente_id=cliente.id,
            valor_total=total,
            status="aguardando_pagamento",
            forma_pagamento="pix",
            observacao=request.form.get("observacao"),
            tipo_entrega=request.form.get("tipo_entrega"),
            valor_entrega=request.form.get("valor_entrega") or 0,
        )

        db.session.add(pedido)
        db.session.flush()

        for item in itens:

            estoque = Estoque.query.filter_by(
                produto_id=item.produto_id,
                numeracao=item.numeracao
            ).first()

            pedido_item = PedidoItem(
                pedido_id=pedido.id,
                produto_id=item.produto_id,
                numeracao=item.numeracao,
                quantidade=item.quantidade,
                valor_unitario=item.valor_unitario,
                subtotal=item.subtotal
            )

            db.session.add(pedido_item)

            estoque.quantidade -= item.quantidade

            db.session.delete(item)

        from app.models.configuracao import Configuracao
        from app.services.mercado_pago_service import gerar_pix_pedido

        config = Configuracao.query.first()

        gerar_pix_pedido(
            pedido,
            config
        )

        db.session.commit()

        flash("Pedido criado com sucesso.", "success")
        return redirect(url_for("carrinho.pedido_sucesso", pedido_id=pedido.id))

    return render_template(
        "loja/checkout.html",
        itens=itens,
        total=total
    )


@carrinho_bp.route("/aumentar/<int:id>")
def aumentar(id):

    item = CarrinhoItem.query.get_or_404(id)

    estoque = Estoque.query.filter_by(
        produto_id=item.produto_id,
        numeracao=item.numeracao
    ).first()

    if not estoque or item.quantidade >= estoque.quantidade:
        flash("Quantidade máxima disponível em estoque.", "warning")
        return redirect(url_for("carrinho.ver"))

    item.quantidade += 1

    db.session.commit()

    return redirect(url_for("carrinho.ver"))


@carrinho_bp.route("/diminuir/<int:id>")
def diminuir(id):

    item = CarrinhoItem.query.get_or_404(id)

    if item.quantidade > 1:
        item.quantidade -= 1
    else:
        db.session.delete(item)

    db.session.commit()

    return redirect(url_for("carrinho.ver"))


@carrinho_bp.route("/pedido/sucesso/<int:pedido_id>")
def pedido_sucesso(pedido_id):
    from app.models.pedido import Pedido
    from app.models.configuracao import Configuracao

    pedido = Pedido.query.get_or_404(pedido_id)
    config = Configuracao.query.first()

    return render_template(
        "loja/pedido_sucesso.html",
        pedido=pedido,
        config=config
    )