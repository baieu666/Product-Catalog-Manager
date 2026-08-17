import sqlite3
from contextlib import contextmanager
from pathlib import Path


CAMINHO_BANCO = Path(__file__).resolve().parent / "pcm.db"


@contextmanager
def abrir_banco():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")

    try:
        yield conexao
        conexao.commit()
    except Exception:
        conexao.rollback()
        raise
    finally:
        conexao.close()


def conectar_banco():
    """Mantém uma função simples para abrir uma conexão manualmente."""
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def criar_tabelas():
    with abrir_banco() as conexao:
        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL,
                sku TEXT NOT NULL,
                possui_variacao INTEGER NOT NULL DEFAULT 0,
                preco_custo REAL NOT NULL,
                preco_venda REAL NOT NULL,
                lucro REAL NOT NULL,
                estoque INTEGER NOT NULL DEFAULT 0
            )
            """
        )

        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS variacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER NOT NULL,
                nome TEXT NOT NULL,
                estoque INTEGER NOT NULL DEFAULT 0,

                FOREIGN KEY (produto_id)
                REFERENCES produtos (id)
                ON DELETE CASCADE
            )
            """
        )


def _montar_produto(conexao, linha_produto):
    if linha_produto is None:
        return None

    linhas_variacoes = conexao.execute(
        """
        SELECT nome, estoque
        FROM variacoes
        WHERE produto_id = ?
        ORDER BY id
        """,
        (linha_produto["id"],),
    ).fetchall()

    produto = dict(linha_produto)
    produto["possui_variacao"] = bool(produto["possui_variacao"])
    produto["variacoes"] = [linha["nome"] for linha in linhas_variacoes]
    produto["estoques_variacoes"] = {
        linha["nome"]: linha["estoque"]
        for linha in linhas_variacoes
    }

    return produto


def listar_produtos():
    with abrir_banco() as conexao:
        linhas = conexao.execute(
            "SELECT * FROM produtos ORDER BY id"
        ).fetchall()

        return [
            _montar_produto(conexao, linha)
            for linha in linhas
        ]


def buscar_produto(produto_id):
    with abrir_banco() as conexao:
        linha = conexao.execute(
            "SELECT * FROM produtos WHERE id = ?",
            (produto_id,),
        ).fetchone()

        return _montar_produto(conexao, linha)


def _inserir_variacoes(conexao, produto_id, produto):
    estoques = produto.get("estoques_variacoes", {})

    for variacao in produto.get("variacoes", []):
        conexao.execute(
            """
            INSERT INTO variacoes (produto_id, nome, estoque)
            VALUES (?, ?, ?)
            """,
            (
                produto_id,
                variacao,
                estoques.get(variacao, 0),
            ),
        )


def inserir_produto(produto):
    with abrir_banco() as conexao:
        cursor = conexao.execute(
            """
            INSERT INTO produtos (
                nome,
                categoria,
                sku,
                possui_variacao,
                preco_custo,
                preco_venda,
                lucro,
                estoque
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                produto["nome"],
                produto["categoria"],
                produto["sku"],
                int(produto["possui_variacao"]),
                produto["preco_custo"],
                produto["preco_venda"],
                produto["lucro"],
                produto["estoque"],
            ),
        )

        produto_id = cursor.lastrowid
        _inserir_variacoes(conexao, produto_id, produto)
        return produto_id


def atualizar_produto(produto_id, produto):
    with abrir_banco() as conexao:
        resultado = conexao.execute(
            """
            UPDATE produtos
            SET nome = ?,
                categoria = ?,
                sku = ?,
                possui_variacao = ?,
                preco_custo = ?,
                preco_venda = ?,
                lucro = ?,
                estoque = ?
            WHERE id = ?
            """,
            (
                produto["nome"],
                produto["categoria"],
                produto["sku"],
                int(produto["possui_variacao"]),
                produto["preco_custo"],
                produto["preco_venda"],
                produto["lucro"],
                produto["estoque"],
                produto_id,
            ),
        )

        if resultado.rowcount == 0:
            return False

        conexao.execute(
            "DELETE FROM variacoes WHERE produto_id = ?",
            (produto_id,),
        )
        _inserir_variacoes(conexao, produto_id, produto)

        return True


def excluir_produto(produto_id):
    with abrir_banco() as conexao:
        resultado = conexao.execute(
            "DELETE FROM produtos WHERE id = ?",
            (produto_id,),
        )

        return resultado.rowcount > 0


if __name__ == "__main__":
    criar_tabelas()
    print("Banco de dados criado com sucesso.")