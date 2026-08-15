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
            request.form["preco_custo"]
        )

        preco_venda = float(
            request.form["preco_venda"]
        )

        estoque = int(
            request.form["estoque"]
        )

        if preco_venda < preco_custo:
            return "O preço de venda não pode ser menor que o preço de custo."

        produto = {
            "nome": nome,
            "categoria": categoria,
            "sku": sku,
            "possui_variacao": False,
            "variacoes": [],
            "estoques_variacoes": {},
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