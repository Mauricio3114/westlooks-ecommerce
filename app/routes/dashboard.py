from datetime import date, datetime

from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import func

from app.models.produto import Produto
from app.models.categoria import Categoria
from app.models.cliente import Cliente
from app.models.pedido import Pedido
from app.models.pedido_item import PedidoItem
from app.models.estoque import Estoque


dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/admin"
)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():

    total_produtos = Produto.query.count()
    total_categorias = Categoria.query.count()
    total_clientes = Cliente.query.count()
    total_pedidos = Pedido.query.count()

    aguardando = Pedido.query.filter_by(status="aguardando_pagamento").count()
    pagos = Pedido.query.filter_by(status="pago").count()
    preparando = Pedido.query.filter_by(status="preparando").count()
    enviados = Pedido.query.filter_by(status="enviado").count()
    entregues = Pedido.query.filter_by(status="entregue").count()
    cancelados = Pedido.query.filter_by(status="cancelado").count()

    status_faturamento = [
        "pago",
        "preparando",
        "enviado",
        "entregue"
    ]

    pedidos_pagos = Pedido.query.filter(
        Pedido.status.in_(status_faturamento)
    ).all()

    hoje = date.today()

    vendas_total = sum(
        float(p.valor_total or 0)
        for p in pedidos_pagos
    )

    vendas_hoje = sum(
        float(p.valor_total or 0)
        for p in pedidos_pagos
        if p.data_pedido and p.data_pedido.date() == hoje
    )

    vendas_mes = sum(
        float(p.valor_total or 0)
        for p in pedidos_pagos
        if p.data_pedido
        and p.data_pedido.month == hoje.month
        and p.data_pedido.year == hoje.year
    )

    pedidos_pagos_count = len(pedidos_pagos)

    ticket_medio = (
        vendas_total / pedidos_pagos_count
        if pedidos_pagos_count > 0
        else 0
    )

    total_estoque = 0
    estoques = Estoque.query.all()

    for item in estoques:
        total_estoque += item.quantidade or 0

    estoque_baixo = Estoque.query.filter(
        Estoque.quantidade <= Estoque.estoque_minimo,
        Estoque.quantidade > 0
    ).count()

    produtos_zerados = Estoque.query.filter(
        Estoque.quantidade <= 0
    ).count()

    produtos_recentes = Produto.query.order_by(
        Produto.data_cadastro.desc()
    ).limit(5).all()

    pedidos_recentes = Pedido.query.order_by(
        Pedido.id.desc()
    ).limit(5).all()

    produtos_mais_vendidos = db_result = (
        PedidoItem.query
        .join(Produto, Produto.id == PedidoItem.produto_id)
        .join(Pedido, Pedido.id == PedidoItem.pedido_id)
        .filter(Pedido.status.in_(status_faturamento))
        .with_entities(
            Produto.nome.label("nome"),
            func.sum(PedidoItem.quantidade).label("quantidade"),
            func.sum(PedidoItem.subtotal).label("total")
        )
        .group_by(Produto.id, Produto.nome)
        .order_by(func.sum(PedidoItem.quantidade).desc())
        .limit(5)
        .all()
    )

    return render_template(
        "admin/dashboard.html",
        total_produtos=total_produtos,
        total_categorias=total_categorias,
        total_clientes=total_clientes,
        total_pedidos=total_pedidos,

        total_estoque=total_estoque,
        estoque_baixo=estoque_baixo,
        produtos_zerados=produtos_zerados,

        produtos_recentes=produtos_recentes,
        pedidos_recentes=pedidos_recentes,
        produtos_mais_vendidos=produtos_mais_vendidos,

        aguardando=aguardando,
        pagos=pagos,
        preparando=preparando,
        enviados=enviados,
        entregues=entregues,
        cancelados=cancelados,

        vendas_total=vendas_total,
        vendas_hoje=vendas_hoje,
        vendas_mes=vendas_mes,
        ticket_medio=ticket_medio,
        pedidos_pagos_count=pedidos_pagos_count,

        grafico_status=[
            aguardando,
            pagos,
            preparando,
            enviados,
            entregues
        ],

        total_itens_pedidos=sum(
            len(p.itens)
            for p in pedidos_recentes
        ),
    )