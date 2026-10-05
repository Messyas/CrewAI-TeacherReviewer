# ============================================================
# Exemplo 6: CrewAI - Agente com ferramenta de leitura de arquivo
# Consulta a base_institucional.txt e gera material alinhado
# ============================================================

import os
from dotenv import load_dotenv
from crewai import Agent, Crew, LLM, Process, Task
from crewai_tools import FileReadTool

load_dotenv()

# Configuração da LLM local (Ollama)
MODEL_NAME = os.getenv("LOCAL_MODEL", "ollama/qwen2.5:7b-instruct-q4_K_M")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

llm = LLM(
    model=MODEL_NAME,
    base_url=OLLAMA_BASE_URL
)

# Criar a ferramenta
# Permite ao agente ler o conteúdo do arquivo de diretrizes institucionais.
caminho_base = os.path.join("dados", "base_institucional.txt")
ferramenta = FileReadTool(
    file_path=caminho_base
)

# Criar o agente
professor = Agent(
    role="Professor orientado por diretrizes institucionais",
    goal="Produzir material estritamente coerente e formatado de acordo com as diretrizes institucionais",
    backstory=(
        "Professor cuidadoso que consulta a fonte institucional antes de escrever "
        "e segue rigorosamente todas as regras estabelecidas nas diretrizes."
    ),
    llm=llm,
    tools=[ferramenta],
    verbose=True
)

# Criar a tarefa
tarefa = Task(
    description=(
        "Leia a base institucional disponível na ferramenta ({caminho_base}) "
        "e produza material sobre {tema}. "
        "Garanta o cumprimento de cada diretriz encontrada. "
        "Ao final, liste explicitamente as diretrizes que foram consultadas e utilizadas."
    ),
    expected_output=(
        "Material em Markdown baseado fielmente nas diretrizes consultadas, "
        "com a seção final listando as diretrizes aplicadas."
    ),
    agent=professor,
    markdown=True
)

# Criar a crew
crew = Crew(
    agents=[professor],
    tasks=[tarefa],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    # Executar
    resultado = crew.kickoff(
        inputs={
            "tema": "Interrupções no ESP32",
            "caminho_base": caminho_base
        }
    )

    # Salva o resultado final na pasta de saída correspondente
    os.makedirs("saidas/ex6", exist_ok=True)
    caminho_saida = os.path.join("saidas", "ex6", "material_diretrizes.txt")
    with open(caminho_saida, "w", encoding="utf-8") as arquivo:
        arquivo.write(resultado.raw)
    print(f"\nResultado salvo com sucesso em {caminho_saida}")