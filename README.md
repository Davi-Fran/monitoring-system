# Monitoring System – TecnoVille
 
## Antes de começar

> **Todos os comandos devem ser executados dentro da pasta `monitoring-system`**, que é a pasta onde ficam o arquivo `manage.py` e o arquivo `pyproject.toml`.
>
> **Os comandos do projeto usam o prefixo `uv run`.** Ele executa o comando dentro do ambiente virtual do projeto, com as dependências corretas, sem a necessidade de ativar o ambiente manualmente.
 
Por exemplo, em vez de `python manage.py migrate`, use:
 
```bash
uv run manage.py migrate
```
 
## Requisitos
 
| Requisito | Versão | Obs. |
|---|---|---|
| [uv](https://docs.astral.sh/uv/) | Atual | Gerenciador de pacotes e ambientes Python. |
| Python | 3.13 ou superior | Não é preciso instalar à parte: o uv baixa a versão correta automaticamente. |
| MySQL | 8.4 ou superior | - |
 
As bibliotecas Python do projeto são instaladas pelo uv a partir do arquivo `pyproject.toml`.
 
## Instalando o uv
 
**Windows (PowerShell):**
 
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
 
**Alternativa com pip**:
 
```bash
pip install uv
```
 
Depois da instalação, feche e abra o terminal e teste:
 
```bash
uv --version
```
 
Documentação oficial do uv: <https://docs.astral.sh/uv/>

Guia de instalação: <https://docs.astral.sh/uv/getting-started/installation/>
 
## Passo a passo para rodar o projeto
 
### 1. Entre na pasta do projeto
 
```bash
cd monitoring-system
```
 
A partir daqui, todos os comandos são executados nessa pasta.
 
### 2. Instale as dependências
 
```bash
uv sync
```
 
O uv cria o ambiente virtual (pasta `.venv`), baixa o Python 3.13 se necessário e instala todas as bibliotecas.
 
### 3. Crie o banco de dados no MySQL
 
```sql
CREATE DATABASE monitoring_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
 
O nome `monitoring_system` é só um exemplo. Use o nome que preferir e o coloque no arquivo `.env` (próximo passo). O conjunto de caracteres `utf8mb4` é necessário para gravar corretamente símbolos como o `°` de `°C`.
 
### 4. Configure as variáveis de ambiente
 
Copie e cole o arquivo de modelo `.env.example` e o renomeie para `.env`.
 
```env
DJANGO_SECRET_KEY="chave-secreta"
DEBUG="true"
 
# Database variables
DB_NAME="monitoring_system"
DB_USER="root"
DB_PASSWORD="senha-do-mysql"
DB_HOST="localhost"
DB_PORT="3306"
```
 
| Variável | Descrição |
|---|---|
| `DJANGO_SECRET_KEY` | Chave secreta do Django. Gere uma com o comando abaixo. |
| `DEBUG` | `true` para desenvolvimento local; `false` em produção. |
| `DB_NAME` | Nome do banco criado no passo 3. |
| `DB_USER` | Usuário do MySQL. |
| `DB_PASSWORD` | Senha do usuário do MySQL. |
| `DB_HOST` | Endereço do servidor MySQL. |
| `DB_PORT` | Porta do MySQL (padrão: `3306`). |
 
Para gerar uma chave secreta:
 
```bash
uv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
 
### 5. Crie as tabelas
 
```bash
uv run manage.py migrate
```
 
### 6. Popule o banco com os dados de exemplo dos CSVs
 
```bash
uv run manage.py populate_db_csv
```
 
Veja mais detalhes em **Populando o banco de dados**.
 
### 7. Inicie o servidor
 
```bash
uv run manage.py runserver
```

Documentação interativa em <http://localhost:8000/api/docs/swagger/>.
 
## Populando o banco de dados
 
Os dados de exemplo ficam na pasta `data` e contêm 6 laboratórios, 3 modelos de microcontrolador, 5 microcontroladores, 5 modelos de sensor, 20 sensores, 145 leituras simuladas e 3 usuários. Há duas formas de carregá-los. **Use apenas uma delas.**
 
### Opção 1: arquivos CSV (recomendada)
 
```bash
uv run manage.py populate_db_csv
```
 
- Lê os arquivos CSV da pasta `data`, valida cada registro e gera o hash das senhas.
- Registros que já existem são ignorados, então o comando pode ser executado mais de uma vez sem duplicar dados.
- **Precisa ser executado dentro da pasta `monitoring-system`**, porque procura os arquivos em `./data`.

### Opção 2: arquivo SQL
 
Importe o arquivo `data/populate.sql` em seu MySQL Workbench e o execute **logo após o `migrate`**.
 
## Usuários de teste
 
Depois de popular o banco, os seguintes usuários estão disponíveis:
 
| Usuário | Senha | Perfil | Permissões |
|---|---|---|---|
| `lin` | `123` | Superusuário | Consultar, cadastrar, editar todos os dados e criar usuários |
| `senai_admin` | `123456` | Administrador | Consultar, cadastrar e editar todos os dados |
| `senai` | `123456` | Usuário comum | Consultar dados e editar o próprio cadastro |

## Obs.
As fotos de usuários enviadas pela API são salvas em uma pasta `public` (ela é criada caso não exista) e acessadas pelo endereço `/public/...`.