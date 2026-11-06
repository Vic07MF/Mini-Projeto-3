
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

DEFAULT_DB = Path(__file__).resolve().parents[2] / "tarefas.db"
DB_PATH = Path(os.getenv("DATABASE_PATH", str(DEFAULT_DB)))

app = FastAPI(title="API de Tarefas", description="Mini Projeto 3: Arthur e Victoria", version="1.0.0")


class TarefaCriacao(BaseModel):
    titulo: str = Field(min_length=1, max_length=120)
    descricao: str = Field(default="", max_length=500)


class TarefaAtualizacao(BaseModel):
    titulo: str | None = Field(default=None, min_length=1, max_length=120)
    descricao: str | None = Field(default=None, max_length=500)
    concluida: bool | None = None


class Tarefa(TarefaCriacao):
    id: int
    concluida: bool


@contextmanager
def conexao():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("""CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL DEFAULT '',
            concluida INTEGER NOT NULL DEFAULT 0
        )""")
        yield conn
        conn.commit()
    finally:
        conn.close()


def obter_tarefa(conn, tarefa_id: int):
    linha = conn.execute("SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)).fetchone()
    if linha is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return dict(linha)


@app.get("/")
def inicio():
    return {"mensagem": "API de Tarefas funcionando", "documentacao": "/docs"}


@app.get("/tarefas", response_model=list[Tarefa])
def listar_tarefas():
    with conexao() as conn:
        return [dict(linha) for linha in conn.execute("SELECT * FROM tarefas ORDER BY id")]


@app.get("/tarefas/{tarefa_id}", response_model=Tarefa)
def buscar_tarefa(tarefa_id: int):
    with conexao() as conn:
        return obter_tarefa(conn, tarefa_id)


@app.post("/tarefas", response_model=Tarefa, status_code=status.HTTP_201_CREATED)
def criar_tarefa(dados: TarefaCriacao):
    with conexao() as conn:
        cursor = conn.execute(
            "INSERT INTO tarefas (titulo, descricao) VALUES (?, ?)",
            (dados.titulo, dados.descricao),
        )
        return obter_tarefa(conn, cursor.lastrowid)


@app.patch("/tarefas/{tarefa_id}", response_model=Tarefa)
def atualizar_tarefa(tarefa_id: int, dados: TarefaAtualizacao):
    with conexao() as conn:
        anterior = obter_tarefa(conn, tarefa_id)
        alteracoes = dados.model_dump(exclude_unset=True)
        alteracoes = {k: v for k, v in alteracoes.items() if v is not None}
        if alteracoes:
            atualizado = {**anterior, **alteracoes}
            conn.execute(
                "UPDATE tarefas SET titulo = ?, descricao = ?, concluida = ? WHERE id = ?",
                (atualizado["titulo"], atualizado["descricao"], int(atualizado["concluida"]), tarefa_id),
            )
        return obter_tarefa(conn, tarefa_id)


@app.delete("/tarefas/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_tarefa(tarefa_id: int):
    with conexao() as conn:
        obter_tarefa(conn, tarefa_id)
        conn.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
