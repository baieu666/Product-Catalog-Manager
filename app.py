from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)

from main import carregar_produtos, salvar_produtos


app = Flask(__name__)


@app.route("/")
def inicio():
    produtos = carregar_produtos()

    return render_template(
        "index.html",
        produtos=produtos
    )


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar_produto_web():
    if request.method == "POST":
        nome = request.form["nome"]
        categoria = request.form["categoria"]
        sku = request.form["sku"]

        preco_custo = float(
            request.form["preco_custo"].replace(",", ".")
        )

        preco_venda = float(
            request.form["preco_venda"].replace(",", ".")
        )

        if preco_venda < preco_custo:
            return (
                "O preço de venda não pode ser "
                "menor que o preço de custo."
            )

        possui_variacao = (
            request.form.get("possui_variacao") == "sim"
        )

        variacoes = []
        estoques_variacoes = {}

        if possui_variacao:
            entrada_variacoes = request.form.get(
                "variacoes",
                ""
            )

            variacoes = [
                variacao.strip()
                for variacao in entrada_variacoes.split(",")
                if variacao.strip()
            ]

            entrada_estoques = request.form.get(
                "estoques_variacoes",
                ""
            )

            for item in entrada_estoques.split(","):
                item = item.strip()

                if item == "":
                    continue

                if ":" not in item:
                    return (
                        "Informe os estoques assim: "
                        "Roxo:20, Azul:30"
                    )

                variacao, quantidade_texto = item.split(
                    ":",
                    1
                )

                variacao = variacao.strip()

                try:
                    quantidade = int(
                        quantidade_texto.strip()
                    )
                except ValueError:
                    return (
                        "A quantidade do estoque "
                        "deve ser um número inteiro."
                    )

                if quantidade < 0:
                    return "O estoque não pode ser negativo."

                estoques_variacoes[variacao] = quantidade

            variacoes_sem_estoque = [
                variacao
                for variacao in variacoes
                if variacao not in estoques_variacoes
            ]

            if not variacoes:
                return "Informe pelo menos uma variação."

            if variacoes_sem_estoque:
                return (
                    "Informe o estoque de todas as variações."
                )

            estoque = sum(
                estoques_variacoes.values()
            )

        else:
            estoque = int(
                request.form.get("estoque", 0)
            )

            if estoque < 0:
                return "O estoque não pode ser negativo."

        produto = {
            "nome": nome,
            "categoria": categoria,
            "sku": sku,
            "possui_variacao": possui_variacao,
            "variacoes": variacoes,
            "estoques_variacoes": estoques_variacoes,
            "preco_custo": preco_custo,
            "preco_venda": preco_venda,
            "lucro": preco_venda - preco_custo,
            "estoque": estoque
        }

        produtos = carregar_produtos()
        produtos.append(produto)
        salvar_produtos(produtos)

        return redirect(url_for("inicio"))

    return render_template("cadastrar.html")


if __name__ == "__main__":
    app.run(debug=True)