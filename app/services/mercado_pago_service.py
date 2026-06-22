import mercadopago


def gerar_pix_pedido(pedido, config):
    if not config or not config.mercado_pago_access_token:
        return None

    sdk = mercadopago.SDK(config.mercado_pago_access_token)

    payment_data = {
        "transaction_amount": float(pedido.valor_total),
        "description": f"Pedido #{pedido.id} - WestLooks",
        "payment_method_id": "pix",
        "payer": {
            "email": pedido.cliente.email or config.email or "cliente@email.com",
            "first_name": pedido.cliente.nome or "Cliente"
        },
        "external_reference": str(pedido.id)
    }

    result = sdk.payment().create(payment_data)
    pagamento = result.get("response", {})

    pedido.mercado_pago_payment_id = str(pagamento.get("id"))
    pedido.pix_copia_cola = (
        pagamento.get("point_of_interaction", {})
        .get("transaction_data", {})
        .get("qr_code")
    )
    pedido.pix_qr_code_base64 = (
        pagamento.get("point_of_interaction", {})
        .get("transaction_data", {})
        .get("qr_code_base64")
    )
    pedido.pix_ticket_url = (
        pagamento.get("point_of_interaction", {})
        .get("transaction_data", {})
        .get("ticket_url")
    )

    return pedido