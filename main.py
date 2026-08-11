import json

print("Product Catalog Manager")

def carregar_produtos():
    try:
        with open("produtos.json", "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []

def salvar_produtos(produtos):
    with open("produtos.json", "w", encoding="utf-8") as arquivo:
        json.dump(produtos, arquivo, ensure_ascii=False, indent=4)

produtos = carregar_produtos()

def mostrar_menu():
    print("\n1 - Cadastrar Produto")
    print("2 - Listar Produtos")
    print("3 - Editar Produto")
    print("4 - Excluir Produto")
    print("0 - Sair")

def ler_texto_edicao(mensagem, valor_atual):
    texto = input(f"{mensagem} [{valor_atual}]: ").strip()

    if texto == "":
        return valor_atual

    return texto

def ler_preco_edicao(mensagem, valor_atual):
    while True:
        entrada = input(f"{mensagem} [{formatar_preco(valor_atual)}]: ").strip()

        if entrada == "":
            return valor_atual

        try:
            preco = float(entrada.replace(",", "."))
            if preco < 0:
                print("Preço inválido. Digite um valor positivo.")
            else:
                return preco

        except ValueError:
            print("Preço inválido. Digite um valor numérico.")

def ler_estoque_edicao(mensagem, valor_atual):
    while True:
        entrada = input(f"{mensagem} [{valor_atual}]: ").strip()
        if entrada == "":
            return valor_atual

        try:
            estoque = int(entrada)
            if estoque < 0:
                print("Quantidade inválida.")
            else:
                return estoque

        except ValueError:
            print("Quantidade inválida. Digite um valor numérico.")

def ler_sim_nao_edicao(mensagem, valor_atual):
    valor_formatado = "s" if valor_atual else "n"
    while True:
        resposta = input(f"{mensagem} (s/n) [{valor_formatado}]: ").strip().lower()

        if resposta == "":
            return valor_atual  
        elif resposta == "s":
            return True
        elif resposta == "n":
            return False
        else:
            print("Digite apenas 's' ou 'n'.")

def ler_variacoes_edicao(variacoes_atuais):
    valor_atual = ", ".join(variacoes_atuais) if variacoes_atuais else "Não informado."

    while True:
        entrada = input(f"Variações [{valor_atual}]: ").strip()

        if entrada == "":
            return variacoes_atuais

        variacoes = [variacao.strip() for variacao in entrada.split(",") if variacao.strip()]

        if variacoes:
            return variacoes

        print("Digite pelo menos uma variação ou deixe em branco se não houver variações.")

def editar_produto(produtos):
    if len(produtos) == 0:
        print("Nenhum produto cadastrado.")
        return

    listar_produtos(produtos)

    try:
        numero = int(input("\nDigite o número do produto que deseja editar: "))
    except ValueError:
        print("Número inválido. Digite um número válido.")
        return

    if numero < 1 or numero > len(produtos):
        print("Produto não encontrado.")
        return

    produto = produtos[numero - 1]

    print("\nDigite os novos valores para o produto (Caso queira manter o valor atual, deixe em branco.):")

    produto["nome"] = ler_texto_edicao("Nome: ", produto["nome"])
    produto["categoria"] = ler_texto_edicao("Categoria: ", produto["categoria"])
    produto["sku"] = ler_texto_edicao("SKU: ", produto.get("sku", ""))

    produto["possui_variacao"] = ler_sim_nao_edicao("O produto possui variações?", produto.get("possui_variacao", False))
    if produto["possui_variacao"]:
        produto["variacoes"] = ler_variacoes_edicao(produto.get("variacoes", []))
    else:
        produto["variacoes"] = []

    produto["preco_custo"] = ler_preco_edicao("Preço de Custo: ", produto["preco_custo"])
    produto["preco_venda"] = ler_preco_edicao("Preço de Venda: ", produto["preco_venda"])
    while produto["preco_venda"] < produto["preco_custo"]:
        print("O preço de venda não pode ser menor que o preço de custo.")
    produto["preco_venda"] = ler_preco_edicao("Preço de Venda: ", produto["preco_venda"])
    produto["lucro"] = produto["preco_venda"] - produto["preco_custo"]

    produto["estoque"] = ler_estoque_edicao("Quantidade em Estoque: ", produto["estoque"])
    print("Produto atualizado com sucesso!")
    salvar_produtos(produtos)

def excluir_produto(produtos):
    if len(produtos) == 0:
        print("Nenhum produto cadastrado.")
        return

    listar_produtos(produtos)

    try:
        numero = int(input("\nDigite o número do produto que deseja excluir: "))
    except ValueError:
        print("Número inválido. Digite um número válido.")
        return

    if numero == 0:
        print("Voltando ao menu principal.")
        return

    if numero < 1 or numero > len(produtos):
        print("Produto não encontrado.")
        return

    produto = produtos[numero - 1]

    confirmacao = input(f"Tem certeza que deseja excluir o produto '{produto['nome']}'? (s/n): ").strip().lower()

    if confirmacao == "s":
        produtos.pop(numero - 1)
        salvar_produtos(produtos)
        print("Produto excluído com sucesso!")
    else:
        print("Exclusão cancelada.")

def ler_preco(mensagem):
    while True:
        try:
            preco = float(input(mensagem).replace("," , "."))

            if preco < 0:
                print("Preço inválido. Digite um valor positivo.")
            else:
                return preco
            
        except ValueError:
            print("Preço inválido. Digite um valor numérico.")

def ler_estoque(mensagem):
    while True:
        try:
            estoque = int(input(mensagem))
            if estoque < 0:
                print("Quantidade inválida. Digite um valor positivo.")
            else:
                return estoque

        except ValueError:
            print("Quantidade inválida. Digite um valor numérico.")

def ler_texto(mensagem):
    while True:
        texto = input(mensagem).strip()
        if texto == "":
            print("Este campo não pode ficar vazio.")
        else:
            return texto

def ler_sim_nao(mensagem):
    while True:
        resposta = input(f"{mensagem} (s/n): ").strip().lower()

        if resposta == "s":
            return True
        elif resposta == "n":
            return False
        else:
            print("Resposta inválida. Digite 's' para sim ou 'n' para não.")

def ler_variacoes():
    while True:
        entrada = input("Digite as variações do produto separadas por vírgula (ou deixe em branco se não houver variações): ").strip()
        variacoes = [variacao.strip() for variacao in entrada.split(",") if variacao.strip()]
        if variacoes:
            return variacoes
        print("Digite pelo menos uma variação ou deixe em branco se não houver variações.")

def ler_estoque_variacoes(variacoes):
    estoques = {}

    for variacao in variacoes:
        quantidade = ler_estoque(f"Estoque da variação '{variacao}': ")

        estoques[variacao] = quantidade

    return estoques

def cadastrar_produto():
        nome = ler_texto("Digite o nome do produto: ")
        categoria = ler_texto("Digite a categoria do produto: ")
        sku = ler_texto("Digite o SKU do produto: ")

        possui_variacao = ler_sim_nao("O produto possui variações?")
        variacoes = []
        estoques_variacoes = {}
        if possui_variacao:
            variacoes = ler_variacoes()
            estoques_variacoes = ler_estoque_variacoes(variacoes)
            estoque = sum(estoques_variacoes.values())
        else:
            estoque = ler_estoque("Digite a quantidade em estoque do produto: ")

        preco_custo = ler_preco("Digite o preço de custo do produto: ")
        preco_venda = ler_preco("Digite o preço de venda do produto: ")
        while preco_venda < preco_custo:
            print("O preço de venda não pode ser menor que o preço de custo.")
            preco_venda = ler_preco("Digite o preço de venda do produto: ")
        lucro = preco_venda - preco_custo
       
        produto = {
            "nome": nome,
            "categoria": categoria,
            "sku": sku,
            "possui_variacao": possui_variacao,
            "variacoes": variacoes,
            "estoques_variacoes": estoques_variacoes,
            "preco_custo": preco_custo,    
            "preco_venda": preco_venda,
            "lucro": lucro,
            "estoque": estoque
            
        }

        return produto

def formatar_preco(valor):
    preco_formatado = f"{valor:.2f}".replace("." , ",")
    return preco_formatado

def listar_produtos(produtos):
    if len(produtos) == 0:
        print("Nenhum produto cadastrado.")
        return

    print("\nProdutos Cadastrados:")

    for indice, produto in enumerate(produtos, start=1):
        preco_custo_formatado = formatar_preco(produto['preco_custo'])
        preco_venda_formatado = formatar_preco(produto['preco_venda'])
        lucro_formatado = formatar_preco(produto['lucro'])
        estoque_formatado = f"{produto['estoque']}"
        estoques_variacoes = produto.get("estoques_variacoes", {})
        if estoques_variacoes:
            estoques_formatados = "\n".join(f"{variacao}: {quantidade}" for variacao, quantidade in estoques_variacoes.items())
        else:
            estoques_formatados = "Não informado."

        variacao = "Sim" if produto.get('possui_variacao', False) else "Não"
        variacoes = produto.get('variacoes', [])
        
        if variacoes:
            variacoes_formatadas = ", ".join(variacoes)
        else:
            variacoes_formatadas = "Não informado."

        print(
            f"- Produto {indice}: {produto['nome']}\n"
            f"- Categoria: {produto['categoria']}\n"
            f"- SKU: {produto.get('sku', 'Não informado')}\n"
            f"- Possui Variação: {variacao}\n"
            f"- Variações: {variacoes_formatadas}\n"
            f"- Estoque por variação:\n{estoques_formatados}\n"
            f"- Custo: R$ {preco_custo_formatado}\n"
            f"- Venda: R$ {preco_venda_formatado}\n"
            f"- Lucro: R$ {lucro_formatado}\n"
            f"- Estoque: {produto['estoque']} Unidades"
        )
        
while True:

    mostrar_menu()
    
    opcao = input("Escolha uma opção: ")
    if opcao == "1":
       produto = cadastrar_produto()
       produtos.append(produto)
       salvar_produtos(produtos)

    elif opcao == "2":
        listar_produtos(produtos)

    elif opcao == "3":
        editar_produto(produtos)

    elif opcao == "4":
        excluir_produto(produtos)

    elif opcao == "0":
        print("Encerrando o PCM.")
        break
    else:
        print("Opção inválida.")
