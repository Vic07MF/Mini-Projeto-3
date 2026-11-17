# Mini Projeto 3 — Gerenciador de Tarefas

Projeto em dupla com uma API REST em Python (FastAPI) e um cliente de terminal separado que consome essa API.

## Estrutura

```text
.
├── client/
│   └── main.py
├── server/
│   └── app/
│       └── main.py
├── tests/
├── requirements.txt
└── README.md
```

## Requisitos

- Python 3.10 ou superior
- Dependências listadas em `requirements.txt`

## Instalação

Na raiz do repositório, crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

Windows (PowerShell):
```powershell
.venv\Scripts\Activate.ps1
```

Linux/macOS:
```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Executar a API

Na raiz do projeto:

```bash
uvicorn server.app.main:app --reload
```

A API ficará disponível em `http://127.0.0.1:8000`.
A documentação interativa do FastAPI fica em `http://127.0.0.1:8000/docs`.

## Executar o cliente

Em outro terminal, com o ambiente virtual ativado:

```bash
python client/main.py
```

O cliente usa por padrão `http://127.0.0.1:8000`. Para apontar para outro endereço, defina a variável `API_URL`.

Windows PowerShell:
```powershell
$env:API_URL = "http://127.0.0.1:8000"
python client/main.py
```

Linux/macOS:
```bash
API_URL="http://127.0.0.1:8000" python client/main.py
```

## Funcionalidades do cliente

- Listar todas as tarefas
- Criar uma tarefa
- Consultar uma tarefa pelo ID
- Editar título e descrição
- Marcar uma tarefa como concluída
- Excluir uma tarefa

## Testes

Na raiz do projeto:

```bash
pytest -q
```

## Endpoints utilizados

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Verificar se a API está funcionando |
| GET | `/tarefas` | Listar tarefas |
| GET | `/tarefas/{tarefa_id}` | Consultar tarefa |
| POST | `/tarefas` | Criar tarefa |
| PATCH | `/tarefas/{tarefa_id}` | Atualizar tarefa |
| DELETE | `/tarefas/{tarefa_id}` | Excluir tarefa |

## Integrantes

- Arthur Lemos
- Victoria Fornel
