import os
import re

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename

from app import db
from app.models.produto import Produto
from app.models.produto_imagem import ProdutoImagem
from app.models.categoria import Categoria


produtos_bp = Blueprint(
    "produtos",
    __name__,
    url_prefix="/admin/produtos"
)


def gerar_slug(texto):
    texto = texto.lower().strip()
    texto = re.sub(r"[áàãâä]", "a", texto)
    texto = re.sub(r"[éèêë]", "e", texto)
    texto = re.sub(r"[íìîï]", "i", texto)
    texto = re.sub(r"[óòõôö]", "o", texto)
    texto = re.sub(r"[úùûü]", "u", texto)
    texto = re.sub(r"[ç]", "c", texto)
    texto = re.sub(r"[^a-z0-9]+", "-", texto)
    return texto.strip("-")


def moeda_para_decimal(valor):
    if valor is None or valor == "":
        return 0

    try:
        return float(valor)
    except (ValueError, TypeError):
        return 0


@produtos_bp.route("/")
@login_required
def listar():
    produtos = Produto.query.order_by(Produto.data_cadastro.desc()).all()
    return render_template("admin/produtos/listar.html", produtos=produtos)


@produtos_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():

    categorias = Categoria.query.filter_by(ativo=True).order_by(Categoria.nome.asc()).all()

    if request.method == "POST":
        nome = request.form.get("nome")

        slug = gerar_slug(nome)

        contador = 2

        while Produto.query.filter_by(slug=slug).first():
            slug = f"{gerar_slug(nome)}-{contador}"
            contador += 1

        produto = Produto(
            nome=nome,
            slug=slug,
            categoria_id=request.form.get("categoria_id") or None,
            marca=request.form.get("marca"),
            referencia=request.form.get("referencia"),
            descricao=request.form.get("descricao"),
            preco=moeda_para_decimal(request.form.get("preco")),
            preco_promocional=moeda_para_decimal(request.form.get("preco_promocional")),
            custo=moeda_para_decimal(request.form.get("custo")),
            ativo=True if request.form.get("ativo") else False,
            destaque=True if request.form.get("destaque") else False,
            lancamento=True if request.form.get("lancamento") else False,
            mais_vendido=True if request.form.get("mais_vendido") else False,
            frete_gratis=True if request.form.get("frete_gratis") else False,
            peso=request.form.get("peso") or 0,
            altura=request.form.get("altura") or 0,
            largura=request.form.get("largura") or 0,
            comprimento=request.form.get("comprimento") or 0
        )

        db.session.add(produto)
        db.session.flush()

        foto_principal = request.files.get("foto_principal")
        fotos_extras = request.files.getlist("fotos_extras")

        os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)

        if foto_principal and foto_principal.filename:
            nome_seguro = secure_filename(foto_principal.filename)
            filename = f"produto_{produto.id}_principal_{nome_seguro}"

            caminho = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            foto_principal.save(caminho)

            db.session.add(ProdutoImagem(
                produto_id=produto.id,
                imagem=filename,
                principal=True
            ))

        for index, imagem in enumerate(fotos_extras):
            if imagem and imagem.filename:
                nome_seguro = secure_filename(imagem.filename)
                filename = f"produto_{produto.id}_extra_{index}_{nome_seguro}"

                caminho = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
                imagem.save(caminho)

                db.session.add(ProdutoImagem(
                    produto_id=produto.id,
                    imagem=filename,
                    principal=False
                ))

        db.session.commit()

        flash("Produto cadastrado com sucesso.", "success")
        return redirect(url_for("produtos.listar"))

    return render_template(
        "admin/produtos/form.html",
        produto=None,
        categorias=categorias
    )


@produtos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):

    produto = Produto.query.get_or_404(id)
    categorias = Categoria.query.filter_by(ativo=True).order_by(Categoria.nome.asc()).all()

    if request.method == "POST":
        produto.nome = request.form.get("nome")
        novo_slug = gerar_slug(produto.nome)

        existe = Produto.query.filter(
            Produto.slug == novo_slug,
            Produto.id != produto.id
        ).first()

        if existe:
            novo_slug = f"{novo_slug}-{produto.id}"

        produto.slug = novo_slug
        produto.categoria_id = request.form.get("categoria_id") or None
        produto.marca = request.form.get("marca")
        produto.referencia = request.form.get("referencia")
        produto.descricao = request.form.get("descricao")
        produto.preco = moeda_para_decimal(request.form.get("preco"))
        produto.preco_promocional = moeda_para_decimal(request.form.get("preco_promocional"))
        produto.custo = moeda_para_decimal(request.form.get("custo"))

        produto.ativo = True if request.form.get("ativo") else False
        produto.destaque = True if request.form.get("destaque") else False
        produto.lancamento = True if request.form.get("lancamento") else False
        produto.mais_vendido = True if request.form.get("mais_vendido") else False
        produto.frete_gratis = True if request.form.get("frete_gratis") else False

        produto.peso = request.form.get("peso") or 0
        produto.altura = request.form.get("altura") or 0
        produto.largura = request.form.get("largura") or 0
        produto.comprimento = request.form.get("comprimento") or 0

        foto_principal = request.files.get("foto_principal")
        fotos_extras = request.files.getlist("fotos_extras")

        os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)

        if foto_principal and foto_principal.filename:

            ProdutoImagem.query.filter_by(
                produto_id=produto.id,
                principal=True
            ).update({"principal": False})

            nome_seguro = secure_filename(foto_principal.filename)
            filename = f"produto_{produto.id}_principal_{nome_seguro}"

            caminho = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            foto_principal.save(caminho)

            db.session.add(
                ProdutoImagem(
                    produto_id=produto.id,
                    imagem=filename,
                    principal=True
                )
            )

        for index, imagem in enumerate(fotos_extras):

            if imagem and imagem.filename:

                nome_seguro = secure_filename(imagem.filename)
                filename = f"produto_{produto.id}_extra_{index}_{nome_seguro}"

                caminho = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
                imagem.save(caminho)

                db.session.add(
                    ProdutoImagem(
                        produto_id=produto.id,
                        imagem=filename,
                        principal=False
                    )
                )

        db.session.commit()

        flash("Produto atualizado com sucesso.", "success")
        return redirect(url_for("produtos.listar"))

    return render_template(
        "admin/produtos/form.html",
        produto=produto,
        categorias=categorias
    )


@produtos_bp.route("/excluir/<int:id>")
@login_required
def excluir(id):

    produto = Produto.query.get_or_404(id)

    db.session.delete(produto)
    db.session.commit()

    flash("Produto excluído com sucesso.", "success")
    return redirect(url_for("produtos.listar"))


@produtos_bp.route("/imagem/excluir/<int:id>")
@login_required
def excluir_imagem(id):

    imagem = ProdutoImagem.query.get_or_404(id)
    produto_id = imagem.produto_id

    db.session.delete(imagem)
    db.session.commit()

    flash("Imagem excluída com sucesso.", "success")
    return redirect(url_for("produtos.editar", id=produto_id))