import os
import re

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app
)

from flask_login import login_required

from werkzeug.utils import secure_filename

from app import db
from app.models.categoria import Categoria


categorias_bp = Blueprint(
    "categorias",
    __name__,
    url_prefix="/admin/categorias"
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


@categorias_bp.route("/")
@login_required
def listar():

    categorias = Categoria.query.order_by(
        Categoria.nome.asc()
    ).all()

    return render_template(
        "admin/categorias/listar.html",
        categorias=categorias
    )


@categorias_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():

    if request.method == "POST":

        nome = request.form.get("nome")
        descricao = request.form.get("descricao")
        ordem = request.form.get("ordem") or 0

        ativo = True if request.form.get("ativo") else False
        destaque = True if request.form.get("destaque") else False

        slug = gerar_slug(nome)

        imagem_nome = None

        imagem = request.files.get("imagem")

        if imagem and imagem.filename:

            filename = secure_filename(imagem.filename)

            imagem_nome = filename

            caminho = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                filename
            )

            os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)
            imagem.save(caminho)

        categoria = Categoria(
            nome=nome,
            slug=slug,
            descricao=descricao,
            ordem=ordem,
            ativo=ativo,
            destaque=destaque,
            imagem=imagem_nome
        )

        db.session.add(categoria)
        db.session.commit()

        flash(
            "Categoria cadastrada com sucesso.",
            "success"
        )

        return redirect(
            url_for("categorias.listar")
        )

    return render_template(
        "admin/categorias/form.html",
        categoria=None
    )


@categorias_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):

    categoria = Categoria.query.get_or_404(id)

    if request.method == "POST":

        categoria.nome = request.form.get("nome")
        categoria.slug = gerar_slug(categoria.nome)

        categoria.descricao = request.form.get("descricao")

        categoria.ordem = request.form.get("ordem") or 0

        categoria.ativo = True if request.form.get("ativo") else False
        categoria.destaque = True if request.form.get("destaque") else False

        imagem = request.files.get("imagem")

        if imagem and imagem.filename:

            filename = secure_filename(imagem.filename)

            categoria.imagem = filename

            caminho = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                filename
            )

            os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)
            imagem.save(caminho)

        db.session.commit()

        flash(
            "Categoria atualizada com sucesso.",
            "success"
        )

        return redirect(
            url_for("categorias.listar")
        )

    return render_template(
        "admin/categorias/form.html",
        categoria=categoria
    )


@categorias_bp.route("/excluir/<int:id>")
@login_required
def excluir(id):

    categoria = Categoria.query.get_or_404(id)

    db.session.delete(categoria)
    db.session.commit()

    flash(
        "Categoria excluída com sucesso.",
        "success"
    )

    return redirect(
        url_for("categorias.listar")
    )