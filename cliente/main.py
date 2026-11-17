"""Cliente de terminal para a API de Tarefas do Mini Projeto 3."""

import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000").rstrip("/")

def requisicao(metodo, caminho, dados=None):
    corpo = None if dados is None else json.dumps(dados, ensure_ascii=False).encode("utf-8")
    req = Request(
        f"{API_URL}{caminho}",
        data=corpo,
        method=metodo,
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urlopen(req, timeout=10) as resposta:
            if resposta.status == 204:
                return None
            conteudo = resposta.read()
            return json.loads(conteudo.decode("utf-8")) if conteudo else None
    except HTTPError as erro:
        try:
            detalhe = erro.read().decode("utf-8")
        except Exception:
            detalhe = str(erro)
        print(f"Erro da API ({erro.code}): {detalhe}")
    except (URLError, TimeoutError) as erro:
        print(f"Não foi possível conectar à API em {API_URL}.")
        print("Confira se o servidor está em execução.")
        print(f"Detalhe: {erro}")
    return None

def mostrar_tarefa(tarefa):
    estado = "Concluída" if tarefa.get("concluida") else "Pendente"
    print(
        f'#{tarefa["id"]} | {tarefa["titulo"]} | {estado}\n'
        f'   {tarefa.get("descricao", "")}'
    )

def listar_tarefas():
    tarefas = requisicao("GET", "/tarefas")
    if tarefas is None:
        return
    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return
    for tarefa in tarefas:
        mostrar_tarefa(tarefa)

def ler_id():
    try:
        valor = int(input("ID da tarefa: "))
        if valor <= 0:
            raise ValueError
        return valor
    except ValueError:
        print("Digite um ID inteiro positivo.")
        return None

def criar_tarefa():
    titulo = input("Título: ").strip()
    if not titulo:
        print("O título não pode ficar vazio.")
        return
    descricao = input("Descrição (opcional): ").strip()
    tarefa = requisicao("POST", "/tarefas", {"titulo": titulo, "descricao": descricao})
    if tarefa:
        print("Tarefa criada:")
        mostrar_tarefa(tarefa)

def consultar_tarefa():
    tarefa_id = ler_id()
    if tarefa_id is None:
        return
    tarefa = requisicao("GET", f"/tarefas/{tarefa_id}")
    if tarefa:
        mostrar_tarefa(tarefa)

def atualizar_tarefa():
    tarefa_id = ler_id()
    if tarefa_id is None:
        return
    print("Deixe o campo em branco para não alterá-lo.")
    titulo = input("Novo título: ").strip()
    descricao = input("Nova descrição: ").strip()
    dados = {}
    if titulo:
        dados["titulo"] = titulo
    if descricao:
        dados["descricao"] = descricao
    if not dados:
        print("Nenhuma alteração informada.")
        return
    tarefa = requisicao("PATCH", f"/tarefas/{tarefa_id}", dados)
    if tarefa:
        print("Tarefa atualizada:")
        mostrar_tarefa(tarefa)

def concluir_tarefa():
    tarefa_id = ler_id()
    if tarefa_id is None:
        return
    tarefa = requisicao("PATCH", f"/tarefas/{tarefa_id}", {"concluida": True})
    if tarefa:
        print("Tarefa marcada como concluída:")
        mostrar_tarefa(tarefa)

def excluir_tarefa():
    tarefa_id = ler_id()
    if tarefa_id is None:
        return
    confirmacao = input(f"Confirma a exclusão da tarefa #{tarefa_id}? (s/N): ").strip().lower()
    if confirmacao != "s":
        print("Exclusão cancelada.")
        return
    resultado = requisicao("DELETE", f"/tarefas/{tarefa_id}")
    if resultado is None:
        print("Solicitação de exclusão enviada. Se o ID existia, a tarefa foi removida.")

def menu():
    opcoes = {
        "1": listar_tarefas,
        "2": criar_tarefa,
        "3": consultar_tarefa,
        "4": atualizar_tarefa,
        "5": concluir_tarefa,
        "6": excluir_tarefa,
    }
    while True:
        print("\n=== GERENCIADOR DE TAREFAS ===")
        print(f"API: {API_URL}")
        print("1 - Listar tarefas")
        print("2 - Criar tarefa")
        print("3 - Consultar tarefa por ID")
        print("4 - Editar tarefa")
        print("5 - Marcar tarefa como concluída")
        print("6 - Excluir tarefa")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "0":
            print("Até logo!")
            break
        acao = opcoes.get(opcao)
        if acao:
            acao()
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()
