# Finance App API

REST API para gestão financeira pessoal construída com Django 5 e Django REST Framework. A aplicação permite cadastrar receitas (`incomes`) e despesas (`expenses`), consultar o balanço mensal ou por período, e exportar um resumo financeiro em PDF. A autenticação é feita via JWT com login por e-mail.

## Funcionalidades

- Cadastro e autenticação de usuários (registro, login, logout) via JWT.
- CRUD de receitas e despesas, sempre escopados ao usuário autenticado.
- Cálculo de totais do mês corrente e por intervalo de datas.
- Geração e download de um relatório financeiro em PDF (via `reportlab`).
- Painel administrativo do Django em `/admin/`.

## Stack

- Python 3.10+ (Django 5.1 não suporta Python 3.9)
- Django 5.1 + Django REST Framework
- PostgreSQL 15 (via Docker Compose)
- `djangorestframework-simplejwt` para autenticação JWT
- `reportlab` para geração de PDFs

## Pré-requisitos

| Ferramenta     | Versão mínima | Observação                                   |
| -------------- | ------------- | -------------------------------------------- |
| Python         | 3.10          | Use `python3` em Linux/macOS, `python` em Windows |
| Docker         | 20.10         | Necessário para subir o PostgreSQL           |
| Docker Compose | v2            | Já incluso nas versões recentes do Docker    |
| Make           | qualquer      | Opcional, mas todos os comandos estão no `Makefile` |

> No Windows, recomenda-se usar **WSL2** ou **Git Bash** para executar os alvos do `Makefile`. Alternativamente, é possível rodar os comandos manualmente (ver seção "Sem Make" abaixo).

## Configuração

### 1. Clonar o repositório

```shell
git clone <repo-url>
cd Finance_App-API
```

### 2. Criar o ambiente virtual

**Linux / macOS**
```shell
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell)**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**Windows (CMD)**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

### 3. Instalar dependências

```shell
make install
```

Ou, sem Make:

```shell
# Linux / macOS
python3 -m pip install -r requirements.txt

# Windows
python -m pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

Copie o arquivo de exemplo e preencha os valores:

```shell
# Linux / macOS
cp .env.example .env

# Windows (PowerShell)
Copy-Item .env.example .env
```

Os valores de banco devem bater com o que está em `docker-compose.yml`:

```env
SECRET_KEY=troque-por-uma-chave-secreta
DB_NAME=finance-app-db
DB_USER=finance-user
DB_PASSWORD=fadbp01
DB_HOST=localhost
DB_PORT=5432
```

Para gerar um `SECRET_KEY` rápido:

```shell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Executando a aplicação

```shell
make database     # sobe o container do PostgreSQL
make migrations   # gera as migrações (se houver mudanças nos modelos)
make migrate      # aplica as migrações
make superuser    # cria um usuário admin (opcional)
make run          # inicia o servidor de desenvolvimento em http://localhost:8000
```

A API ficará disponível em `http://localhost:8000/api/` e o admin em `http://localhost:8000/admin/`.

### Sem Make (Windows nativo)

```powershell
docker compose up -d
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Testes

```shell
make test
```

Para rodar os testes de um app específico:

```shell
python manage.py test apps.expenses
```

## Estrutura do projeto

```
finance_hub/        # configurações do projeto Django (settings, urls, wsgi)
apps/
├── users/          # registro, login, JWT customizado, autenticação por e-mail
├── incomes/        # receitas (modelo, viewset, totais mensais)
├── expenses/       # despesas (modelo, viewset, totais mensais)
└── balance/        # balanço agregado, filtro por data e exportação em PDF
manage.py
Makefile
docker-compose.yml
requirements.txt
```

Todas as sub-aplicações compartilham o mesmo registro em `INSTALLED_APPS` (`apps`) e a mesma pasta de migrações (`apps/migrations/`).

## Principais endpoints

| Método | Rota                              | Descrição                                  |
| ------ | --------------------------------- | ------------------------------------------ |
| POST   | `/api/register/`                  | Registro de novo usuário                   |
| POST   | `/api/login/`                     | Login por e-mail e senha                   |
| POST   | `/api/token/`                     | Obter par de tokens JWT                    |
| POST   | `/api/token/refresh/`             | Renovar o access token                     |
| POST   | `/api/logout/`                    | Logout (blacklist do refresh token)        |
| GET/POST | `/api/incomes/`                 | Listar / criar receitas                    |
| GET/POST | `/api/expenses/`                | Listar / criar despesas                    |
| GET    | `/api/incomes/month`              | Total de receitas do mês corrente          |
| GET    | `/api/expenses/month`             | Total de despesas do mês corrente          |
| GET    | `/api/balance/month/`             | Balanço do mês corrente                    |
| GET    | `/api/balance/date/`              | Balanço por intervalo (`start_date`, `end_date`) |
| GET    | `/api/download/balance/date/`     | Download do PDF do balanço por intervalo   |
