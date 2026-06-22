from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from app import db
from app.models.produto import Produto
from app.models.estoque import Estoque


estoque_bp = Blueprint(
    "estoque",
    __name__,
    url_prefix="/admin/estoque"
)


@estoque_bp.route("/")
@login_required
def listar():

    produtos = Produto.query.order_by(
        Produto.nome.asc()
    ).all()

    resumo_estoque = {}

    for produto in produtos:

        estoques = Estoque.query.filter_by(
            produto_id=produto.id
        ).all()

        resumo = {}

        for est in estoques:
            num = est.numeracao

            if num not in resumo:
                resumo[num] = {
                    "numeracao": num,
                    "quantidade": 0,
                    "estoque_minimo": est.estoque_minimo or 0
                }

            resumo[num]["quantidade"] += est.quantidade or 0

        resumo_estoque[produto.id] = sorted(
            resumo.values(),
            key=lambda x: int(x["numeracao"]) if str(x["numeracao"]).isdigit() else 0
        )

    return render_template(
        "admin/estoque/listar.html",
        produtos=produtos,
        resumo_estoque=resumo_estoque
    )


@estoque_bp.route("/produto/<int:produto_id>", methods=["GET", "POST"])
@login_required
def produto(produto_id):

    produto = Produto.query.get_or_404(produto_id)

    if request.method == "POST":
        cor = request.form.get("cor")

        numeracoes = request.form.getlist("numeracao[]")
        quantidades = request.form.getlist("quantidade[]")
        minimos = request.form.getlist("estoque_minimo[]")

        for i in range(len(numeracoes)):
            numeracao = numeracoes[i]
            quantidade = int(quantidades[i] or 0)
            estoque_minimo = int(minimos[i] or 0)

            if numeracao:
                estoque = Estoque.query.filter_by(
                    produto_id=produto.id,
                    cor=cor,
                    numeracao=numeracao
                ).first()

                if not estoque:
                    estoque = Estoque(
                        produto_id=produto.id,
                        cor=cor,
                        numeracao=numeracao
                    )
                    db.session.add(estoque)

                estoque.quantidade = quantidade
                estoque.estoque_minimo = estoque_minimo

        db.session.commit()

        flash("Estoque atualizado com sucesso.", "success")
        return redirect(url_for("estoque.produto", produto_id=produto.id))

    return render_template("admin/estoque/produto.html", produto=produto)