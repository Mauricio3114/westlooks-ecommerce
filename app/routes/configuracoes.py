from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from flask_login import login_required

from app import db
from app.models.configuracao import Configuracao


configuracoes_bp = Blueprint(
    "configuracoes",
    __name__,
    url_prefix="/admin/configuracoes"
)


@configuracoes_bp.route(
    "/",
    methods=["GET", "POST"]
)
@login_required
def index():

    config = Configuracao.query.first()

    if not config:
        config = Configuracao()
        db.session.add(config)
        db.session.commit()

    if request.method == "POST":

        config.nome_loja = request.form.get(
            "nome_loja"
        )

        config.whatsapp = request.form.get(
            "whatsapp"
        )

        config.instagram = request.form.get(
            "instagram"
        )

        config.email = request.form.get(
            "email"
        )

        config.tipo_pix = request.form.get(
            "tipo_pix"
        )

        config.chave_pix = request.form.get(
            "chave_pix"
        )

        config.nome_recebedor = request.form.get(
            "nome_recebedor"
        )

        config.mercado_pago_public_key = request.form.get(
            "mercado_pago_public_key"
        )

        config.mercado_pago_access_token = request.form.get(
            "mercado_pago_access_token"
        )

        db.session.commit()

        flash(
            "Configurações salvas.",
            "success"
        )

        return redirect(
            url_for(
                "configuracoes.index"
            )
        )

    return render_template(
        "admin/configuracoes/index.html",
        config=config
    )