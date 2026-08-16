import sqlite3
from pathlib import Path


CAMINHO_BANCO = Path(__file__).parent / "pcm.db"


def conectar_banco():
    conexao = sqlite3.connect(CAMINHO_BANCO)

    conexao.row_factory = sqlite3.Row

    conexao.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conexao


def criar_tabelas():
    with conectar_banco() as conexao:
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


if __name__ == "__main__":
    criar_tabelas()
    print("Banco de dados criado com sucesso.")