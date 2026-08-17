from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
)

from database import (
    atualizar_produto,
    buscar_produto,
    criar_tabelas,
    excluir_produto,
    inserir_produto,
    listar_produtos,
)


app = Flask(__name__)
criar_tabelas()


@app.template_filter("brl")
def formatar_brl(valor):
    return f"R$ {valor:.2f}".replace(".", ",")


def atualizar_produto_com_formulario(produto, formulario):
    nome = formulario.get("nome", "").strip()
    categoria = formulario.get("categoria", "").strip()
    sku = formulario.get("sku", "").strip()

    if not nome or not categoria or not sku:
        raise ValueError("Preencha todos os campos obrigatórios.")

    try:
        preco_custo = float(
            formulario.get("preco_custo", "").replace(",", ".")
        )
        preco_venda = float(
            formulario.get("preco_venda", "").replace(",", ".")
        )
    except ValueError:
        raise ValueError("Os preços devem ser números válidos.")

    if preco_custo < 0 or preco_venda < 0:
        raise ValueError("Os preços não podem ser negativos.")

    if preco_venda < preco_custo:
        raise ValueError(
            "O preço de venda não pode ser menor que o preço de custo."
        )

    possui_variacao = formulario.get("possui_variacao") == "sim"
    variacoes = []
    estoques_variacoes = {}

    if possui_variacao:
        entrada_variacoes = formulario.get("variacoes", "")
        variacoes = [
            variacao.strip()
            for variacao in entrada_variacoes.split(",")
            if variacao.strip()
        ]

        if not variacoes:
            raise ValueError("Informe pelo menos uma variação.")

        entrada_estoques = formulario.get("estoques_variacoes", "")

        for item in entrada_estoques.split(","):
            item = item.strip()

            if not item:
                continue

            if ":" not in item:
                raise ValueError(
                    "Informe os estoques assim: Roxo:20, Azul:30"
                )

            variacao, quantidade_texto = item.split(":", 1)
            variacao = variacao.strip()

            if not variacao:
                raise ValueError("O nome da variação não pode ficar vazio.")

            try:
                quantidade = int(quantidade_texto.strip())
            except ValueError:
                raise ValueError(
                    "A quantidade do estoque deve ser um número inteiro."
                )

            if quantidade < 0:
                raise ValueError("O estoque não pode ser negativo.")

            estoques_variacoes[variacao] = quantidade

        variacoes_sem_estoque = [
            variacao
            for variacao in variacoes
            if variacao not in estoques_variacoes
        ]

        if variacoes_sem_estoque:
            raise ValueError("Informe o estoque de todas as variações.")

        estoque = sum(estoques_variacoes.values())

    else:
        try:
            estoque = int(formulario.get("estoque", "0") or 0)
        except ValueError:
            raise ValueError("O estoque deve ser um número inteiro.")

        if estoque < 0:
            raise ValueError("O estoque não pode ser negativo.")

    produto.update(
        {
            "nome": nome,
            "categoria": categoria,
            "sku": sku,
            "possui_variacao": possui_variacao,
            "variacoes": variacoes,
            "estoques_variacoes": estoques_variacoes,
            "preco_custo": preco_custo,
            "preco_venda": preco_venda,
            "lucro": preco_venda - preco_custo,
            "estoque": estoque,
        }
    )


@app.route("/")
def inicio():
    return render_template("index.html", produtos=listar_produtos())


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar_produto_web():
    if request.method == "POST":
        produto = {}

        try:
            atualizar_produto_com_formulario(produto, request.form)
            inserir_produto(produto)
        except ValueError as erro:
            return str(erro), 400

        return redirect(url_for("inicio"))

    return render_template("cadastrar.html")


@app.route("/excluir/<int:indice>", methods=["POST"])
def excluir_produto_web(indice):
    produtos = listar_produtos()

    if indice < 0 or indice >= len(produtos):
        return "Produto não encontrado.", 404

    produto_id = produtos[indice]["id"]
    excluir_produto(produto_id)

    return redirect(url_for("inicio"))


@app.route("/editar/<int:indice>", methods=["GET", "POST"])
def editar_produto_web(indice):
    produtos = listar_produtos()

    if indice < 0 or indice >= len(produtos):
        return "Produto não encontrado.", 404

    produto = produtos[indice]
    produto_id = produto["id"]

    if request.method == "POST":
        produto_atualizado = {}

        try:
            atualizar_produto_com_formulario(
                produto_atualizado,
                request.form,
            )
            atualizado = atualizar_produto(
                produto_id,
                produto_atualizado,
            )
        except ValueError as erro:
            return str(erro), 400

        if not atualizado:
            return "Produto não encontrado.", 404

        return redirect(url_for("inicio"))

    return render_template(
        "cadastrar.html",
        produto=produto,
        indice=indice,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)