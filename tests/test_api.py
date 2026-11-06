import pytest
from fastapi.testclient import TestClient
from server.app import main


@pytest.fixture
def cliente(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "DB_PATH", tmp_path / "teste.db")
    return TestClient(main.app)


def test_fluxo_completo(cliente):
    assert cliente.get("/tarefas").json() == []
    criado = cliente.post("/tarefas", json={"titulo": "Estudar APIs", "descricao": "Projeto em dupla"})
    assert criado.status_code == 201
    tarefa = criado.json()
    assert tarefa["titulo"] == "Estudar APIs"
    assert tarefa["concluida"] is False
    identificador = tarefa["id"]
    assert len(cliente.get("/tarefas").json()) == 1
    assert cliente.get(f"/tarefas/{identificador}").status_code == 200
    alterada = cliente.patch(f"/tarefas/{identificador}", json={"concluida": True})
    assert alterada.json()["concluida"] is True
    assert cliente.delete(f"/tarefas/{identificador}").status_code == 204
    assert cliente.get(f"/tarefas/{identificador}").status_code == 404


def test_validacao(cliente):
    assert cliente.post("/tarefas", json={"titulo": ""}).status_code == 422
    assert cliente.patch("/tarefas/999", json={"concluida": True}).status_code == 404
