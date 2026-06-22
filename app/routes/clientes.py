from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import func
from datetime import date

from app.models.cliente import Cliente
from app.models.pedido import Pedido


clientes_bp = Blueprint(
    "clientes",
    __name__,
    url_prefix="/admin/clientes"
)


@clientes_bp.route("/")
@login_required
def listar():

    clientes = Cliente.query.order_by(
        Cliente.id.desc()
    ).all()

    total_clientes = Cliente.query.count()

    total_com_pedido = (
        Pedido.query.with_entities(Pedido.cliente_id)
        .distinct()
        .count()
    )

    return render_template(
        "admin/clientes/listar.html",
        clientes=clientes,
        total_clientes=total_clientes,
        total_com_pedido=total_com_pedido
    )