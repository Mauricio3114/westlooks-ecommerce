from app import create_app, db
from app.models.categoria import Categoria

app = create_app()

categorias = [
    {
        "nome": "Linha Essential",
        "slug": "essential",
        "descricao": "Linha clássica da WestLooks para quem busca conforto e elegância.",
        "ordem": 1,
        "destaque": True,
    },
    {
        "nome": "Linha Minimal",
        "slug": "minimal",
        "descricao": "Visual minimalista, moderno e sofisticado.",
        "ordem": 2,
        "destaque": True,
    },
    {
        "nome": "Linha Sneaker",
        "slug": "sneaker",
        "descricao": "Sneakers premium para o dia a dia.",
        "ordem": 3,
        "destaque": True,
    },
    {
        "nome": "Linha Derby",
        "slug": "derby",
        "descricao": "Sapatos sociais premium para qualquer ocasião.",
        "ordem": 4,
        "destaque": True,
    },
    {
        "nome": "Linha Casual",
        "slug": "casual",
        "descricao": "Conforto e estilo para o dia a dia.",
        "ordem": 5,
        "destaque": False,
    },
    {
        "nome": "Linha Basic",
        "slug": "basic",
        "descricao": "Modelos básicos e versáteis.",
        "ordem": 6,
        "destaque": False,
    },
    {
        "nome": "Slip On",
        "slug": "slip-on",
        "descricao": "Praticidade sem abrir mão do estilo.",
        "ordem": 7,
        "destaque": False,
    },
    {
        "nome": "Slip On Confort",
        "slug": "slip-on-confort",
        "descricao": "Máximo conforto para uso diário.",
        "ordem": 8,
        "destaque": False,
    },
    {
        "nome": "Sider",
        "slug": "sider",
        "descricao": "Linha náutica elegante.",
        "ordem": 9,
        "destaque": False,
    },
    {
        "nome": "Mule",
        "slug": "mule",
        "descricao": "Praticidade e elegância em um só modelo.",
        "ordem": 10,
        "destaque": False,
    },
]

with app.app_context():

    for item in categorias:

        existe = Categoria.query.filter_by(slug=item["slug"]).first()

        if existe:
            print(f"✓ {item['nome']} já existe")
            continue

        categoria = Categoria(
            nome=item["nome"],
            slug=item["slug"],
            descricao=item["descricao"],
            ordem=item["ordem"],
            destaque=item["destaque"],
            ativo=True
        )

        db.session.add(categoria)

    db.session.commit()

    print("\n====================================")
    print("Categorias cadastradas com sucesso!")
    print("====================================")