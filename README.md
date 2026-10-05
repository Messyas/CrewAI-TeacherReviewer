# CrewAI - Teacher & Reviewer 🎓📝

Micro projeto demonstrativo utilizando [CrewAI](https://github.com/crewAIInc/crewAI) com dois agentes inteligentes trabalhando em conjunto:
- **Professor (Teacher):** Elabora explicações didáticas, analogias e exemplos práticos sobre qualquer assunto.
- **Revisor Pedagógico (Reviewer):** Analisa o conteúdo, garante rigor conceitual, aprimora a clareza e adiciona perguntas de fixação para o aluno.

---

## 📋 Pré-requisitos

- **Python:** Versão 3.10, 3.11 ou 3.12 (recomendado 3.11 para estabilidade).
- Uma chave de API de LLM (por padrão, OpenAI: `OPENAI_API_KEY`).

Escolha abaixo o método de sua preferência:
- [Opção 1: Setup Tradicional (venv + pip)](#-opção-1-setup-tradicional-venv--pip)
- [Opção 2: Setup Ultra-Rápido com uv](#-opção-2-setup-ultra-rápido-com-uv-recomendado)

---

## 🐍 Opção 1: Setup Tradicional (`venv` + `pip`)

### 1. Criar o Ambiente Virtual

Abra o terminal na pasta raiz do projeto:

#### Windows:
```bash
python -m venv .venv
```
*(Se você tiver múltiplas versões do Python instaladas, especifique a 3.11 com: `py -3.11 -m venv .venv`)*

#### Linux / macOS:
```bash
python3 -m venv .venv
```

### 2. Ativar o Ambiente Virtual

#### Windows (PowerShell):
```powershell
.venv\Scripts\Activate.ps1
```
> *Nota: Se houver restrição de script no PowerShell, libere com: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`*

#### Windows (Prompt de Comando / CMD):
```cmd
.venv\Scripts\activate.bat
```

#### Linux / macOS (Bash / Zsh):
```bash
source .venv/bin/activate
```

*(O prefixo `(.venv)` indicará que o ambiente está ativo).*

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

---

## ⚡ Opção 2: Setup Ultra-Rápido com `uv` (Recomendado)

O [uv](https://docs.astral.sh/uv/) é um gerenciador de pacotes e ambientes Python de altíssima velocidade (10-100x mais rápido que o pip).

### 1. Instalar o `uv` (caso ainda não possua)

- **Windows (PowerShell):**
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
  *(Ou via winget: `winget install astral-sh.uv`)*

- **Linux / macOS:**
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

### 2. Criar o Ambiente Virtual com Python 3.11
O `uv` baixa e gerencia a versão do Python automaticamente se necessário:

```bash
uv venv .venv --python 3.11
```

### 3. Instalar as Dependências

```bash
uv pip install -r requirements.txt
```

> **Dica Pro com `uv`:** Você nem precisa ativar o ambiente virtual manualmente! Pode rodar seus scripts diretamente com:
> ```bash
> uv run main.py
> ```

---

## ⚙️ Configuração das Variáveis de Ambiente (`.env`)

Independente do método de instalação escolhido, configure sua chave de API:

1. Duplique o arquivo `.env.example` criando o `.env`:

   - **Windows (PowerShell):**
     ```powershell
     Copy-Item .env.example .env
     ```
   - **Windows (CMD):**
     ```cmd
     copy .env.example .env
     ```
   - **Linux / macOS:**
     ```bash
     cp .env.example .env
     ```

2. Edite o arquivo `.env` inserindo sua chave da OpenAI:
   ```env
   OPENAI_API_KEY=sk-proj-sua-chave-aqui...
   OPENAI_MODEL_NAME=gpt-4o-mini
   ```

---

## 🎯 Executando o Micro Projeto

### Com o ambiente ativado (Opção 1 ou 2):

- **Tópico padrão ("Como funcionam Redes Neurais"):**
  ```bash
  python main.py
  ```

- **Passando um tópico customizado:**
  ```bash
  python main.py "Como funciona a computação quântica"
  ```
  ```bash
  python main.py "Introdução prática a Docker e Containers"
  ```

### Diretamente via `uv run` (sem precisar ativar venv):

```bash
uv run main.py "Arquitetura de Microsserviços para iniciantes"
```

---

## 📁 Estrutura de Arquivos

```
CrewAI-TeacherReviewer/
├── .venv/               # Ambiente virtual isolado (ignorado pelo git)
├── .env                 # Suas chaves de API secretas (ignorado pelo git)
├── .env.example         # Modelo das variáveis de ambiente necessárias
├── .gitignore           # Regras de exclusão do controle de versão
├── main.py              # Código principal com os agentes Teacher & Reviewer
├── requirements.txt     # Dependências Python (crewai, python-dotenv)
└── README.md            # Guia completo de instalação (pip e uv)
```

---

## 💡 Como Desativar o Venv

Quando terminar de trabalhar com o ambiente ativado:
```bash
deactivate
```
