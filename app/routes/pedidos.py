from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from app import db
from app.models.pedido import Pedido


pedidos_bp = Blueprint(
    "pedidos",
    __name__,
    url_prefix="/admin/pedidos"
)


@pedidos_bp.route("/")
@login_required
def listar():

    status = request.args.get("status", "")

    query = Pedido.query

    if status:
        query = query.filter(
            Pedido.status == status
        )

    pedidos = query.order_by(
        Pedido.id.desc()
    ).all()

    total_pedidos = len(pedidos)

    total_vendido = sum(
        float(p.valor_total or 0)
        for p in pedidos
    )

    ticket_medio = (
        total_vendido / total_pedidos
        if total_pedidos > 0
        else 0
    )

    aguardando = Pedido.query.filter_by(
        status="aguardando_pagamento"
    ).count()

    pagos = Pedido.query.filter_by(
        status="pago"
    ).count()

    preparando = Pedido.query.filter_by(
        status="preparando"
    ).count()

    enviados = Pedido.query.filter_by(
        status="enviado"
    ).count()

    entregues = Pedido.query.filter_by(
        status="entregue"
    ).count()

    cancelados = Pedido.query.filter_by(
        status="cancelado"
    ).count()

    return render_template(
        "admin/pedidos/listar.html",
        pedidos=pedidos,
        total_pedidos=total_pedidos,
        total_vendido=total_vendido,
        ticket_medio=ticket_medio,
        aguardando=aguardando,
        pagos=pagos,
        preparando=preparando,
        enviados=enviados,
        entregues=entregues,
        cancelados=cancelados,
        status_selecionado=status
    )


@pedidos_bp.route("/<int:pedido_id>")
@login_required
def detalhe(pedido_id):

    pedido = Pedido.query.get_or_404(
        pedido_id
    )

    return render_template(
        "admin/pedidos/detalhe.html",
        pedido=pedido
    )


@pedidos_bp.route("/<int:pedido_id>/status/<novo_status>")
@login_required
def alterar_status(pedido_id, novo_status):

    status_permitidos = [
        "aguardando_pagamento",
        "pago",
        "preparando",
        "enviado",
        "entregue",
        "cancelado"
    ]

    if novo_status not in status_permitidos:
        flash("Status inválido.", "danger")
        return redirect(
            url_for(
                "pedidos.detalhe",
                pedido_id=pedido_id
            )
        )

    pedido = Pedido.query.get_or_404(
        pedido_id
    )

    pedido.status = novo_status

    agora = datetime.utcnow()

    if novo_status == "pago" and not pedido.data_pagamento:
        pedido.data_pagamento = agora

    elif novo_status == "preparando" and not pedido.data_preparacao:
        pedido.data_preparacao = agora

    elif novo_status == "enviado" and not pedido.data_envio:
        pedido.data_envio = agora

    elif novo_status == "entregue" and not pedido.data_entrega:
        pedido.data_entrega = agora

    db.session.commit()

    flash(
        "Status do pedido atualizado.",
        "success"
    )

    return redirect(
        url_for(
            "pedidos.detalhe",
            pedido_id=pedido_id
        )
    )


@pedidos_bp.route("/<int:pedido_id>/rastreamento", methods=["POST"])
@login_required
def salvar_rastreamento(pedido_id):

    pedido = Pedido.query.get_or_404(
        pedido_id
    )

    pedido.transportadora = request.form.get(
        "transportadora"
    )

    pedido.codigo_rastreamento = request.form.get(
        "codigo_rastreamento"
    )

    if pedido.status != "enviado":
        pedido.status = "enviado"

    if not pedido.data_envio:
        pedido.data_envio = datetime.utcnow()

    db.session.commit()

    flash(
        "Rastreamento salvo com sucesso.",
        "success"
    )

    return redirect(
        url_for(
            "pedidos.detalhe",
            pedido_id=pedido.id
        )
    )