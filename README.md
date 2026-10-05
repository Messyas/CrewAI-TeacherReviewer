# CrewAI - Teacher & Reviewer 🎓📝

Micro projeto demonstrativo utilizando [CrewAI](https://github.com/crewAIInc/crewAI) com dois agentes inteligentes trabalhando em conjunto:
- **Professor (Teacher):** Elabora explicações didáticas, analogias e exemplos práticos sobre qualquer assunto.
- **Revisor Pedagógico (Reviewer):** Analisa o conteúdo, garante rigor conceitual, aprimora a clareza e adiciona perguntas de fixação para o aluno.

---

## Pré-requisitos

- **Python:** Versão 3.10, 3.11 ou 3.12 (recomendado 3.11 para estabilidade).
- Uma chave de API de LLM (por padrão, OpenAI: `OPENAI_API_KEY`).

Escolha abaixo o método de sua preferência:
- [Opção 1: Setup Tradicional (venv + pip)](#-opção-1-setup-tradicional-venv--pip)
- [Opção 2: Setup Ultra-Rápido com uv](#-opção-2-setup-ultra-rápido-com-uv-recomendado)

---

## Opção 1: Setup Tradicional (`venv` + `pip`)

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

## Opção 2: Setup Ultra-Rápido com `uv` (Recomendado)

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

## Configuração das Variáveis de Ambiente (`.env`)

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

## Executando o Micro Projeto

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

## Estrutura de Arquivos

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

## Exercícios Práticos - Curso de Agentes Inteligentes (Projeto AXacademy)

> **Contexto:** Este repositório contém as implementações dos exercícios práticos do **curso de Agentes Inteligentes do projeto AXacademy**.
>
> **Instruções:** Resolva os três exercícios abaixo. Se for o caso, faça pesquisas. Entregue os códigos Python e os arquivos gerados para cada um dos exercícios.

---

### Exemplo 4: Terceiro Agente "Revisor"
- **Arquivo base:** `main4.py`
- **Enunciado:** Adicione um terceiro agente **"Revisor"**, que recebe como contexto o material produzido pelo Professor.
- **Entregáveis:** Código Python atualizado e saída gerada salva em `saidas/ex4/aula_revisada.md`.

---

### Exemplo 5: Pré-requisitos e Validação Estrita de Exercícios
- **Arquivo base:** `main5.py`
- **Enunciado:** Adicione ao `PlanoAula` um campo `pre_requisitos` contendo uma lista de strings e imponha que existam exatamente três exercícios (nem mais, nem menos).
- **Entregáveis:** Código Python atualizado com as validações Pydantic e o arquivo gerado `saidas/ex5/plano_aula.txt`.

---

### Exemplo 6: Modificação da Base Institucional
- **Arquivo base:** `main6.py`
- **Enunciado:** Modifique `base_institucional.txt`, execute novamente e identifique quais partes da resposta foram alteradas. Como não há mudanças no código de sala de aula, envie somente o novo arquivo `dados/base_institucional.txt` e os arquivos gerados.
- **Entregáveis:** Novo arquivo `dados/base_institucional.txt` e o arquivo de saída gerado `saidas/ex6/material_diretrizes.txt`.
- **Análise das Alterações Identificadas na Resposta:**
  1. **Seção de Pré-Requisitos e Público-Alvo:** A nova versão incorporou explicitamente os pré-requisitos técnicos (C/C++, ESP32 e tempo real) antes dos objetivos de aprendizagem (atendendo à nova diretriz 1).
  2. **Exemplo Prático com Código Comentado Linha a Linha:** O código de exemplo em C/C++ passou a ser acompanhado da explicação detalhada linha a linha de cada instrução (atendendo à diretriz 2).
  3. **Subseção de Boas Práticas e Segurança de Hardware:** Foi adicionada uma nova subseção dedicada à mitigação de falhas de hardware, proteção contra sobrecorrente e estabilidade da alimentação (atendendo à diretriz 7).
  4. **Atividade de Laboratório Estruturada:** A atividade final foi convertida em roteiro prático de laboratório com número de repetições e observação de consistência (atendendo à diretriz 4).
  5. **Separação Rígida das Seções:** O material gerado organizou o conteúdo estritamente nas 5 seções estipuladas na diretriz 5 (`Introdução e Objetivos`, `Conceitos Teóricos`, `Exemplo Prático com Código`, `Atividade de Laboratório` e `Síntese / Conclusão`).



---

## Como Desativar o Venv

Quando terminar de trabalhar com o ambiente ativado:
```bash
deactivate
```

