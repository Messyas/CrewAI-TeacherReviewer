# ============================================================
# Exemplo 5: Saída estruturada com Pydantic
# Adicionado campo pre_requisitos e restrição estrita de 3 exercícios
# ============================================================

import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from crewai import Agent, Crew, LLM, Process, Task

load_dotenv()

# Configuração da LLM local (Ollama)
MODEL_NAME = os.getenv("LOCAL_MODEL", "ollama/qwen2.5:7b-instruct-q4_K_M")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Definir a estrutura de cada exercício
class Exercicio(BaseModel):
    enunciado: str
    resposta_esperada: str

# Define a estrutura do plano de aula validada com Pydantic
class PlanoAula(BaseModel):
    titulo: str
    publico: str

    # A duração deve ser maior que zero
    duracao_minutos: int = Field(gt=0)

    # Campo exigido no Exemplo 5: lista de pré-requisitos
    pre_requisitos: list[str] = Field(
        description="Lista de pré-requisitos ou conhecimentos prévios necessários para acompanhar a aula"
    )

    objetivos: list[str]
    conceitos: list[str]
    exemplo_pratico: str

    exercicios: list[Exercicio] = Field(
        min_length=3,
        max_length=3,
        description="Exatamente três exercícios práticos com enunciado e resposta esperada"
    )

# Criar a LLM local
llm = LLM(
    model=MODEL_NAME,
    base_url=OLLAMA_BASE_URL
)

# Criar os agentes
pesquisador = Agent(
    role="Pesquisador técnico",
    goal="Selecionar conceitos corretos, pré-requisitos e conteúdos adequados ao público",
    backstory=(
        "Pesquisador criterioso de computação e sistemas embarcados. "
        "Mapeia fundamentos necessários, pré-requisitos essenciais e tópicos práticos."
    ),
    llm=llm,
    verbose=True
)

professor = Agent(
    role="Professor conteudista",
    goal="Criar planos de aula completos e estruturados com precisão pedagógica",
    backstory=(
        "Professor experiente que transforma pesquisa em uma sequência didática clara, "
        "definindo pré-requisitos adequados e formulando exatamente três exercícios práticos."
    ),
    llm=llm,
    verbose=True
)

# Primeira tarefa: pesquisar
pesquisa = Task(
    description=(
        "Produza notas técnicas essenciais sobre {tema} para {publico}. "
        "Identifique os pré-requisitos necessários para os alunos acompanharem a aula."
    ),
    expected_output="Notas curtas, corretas e organizadas contendo conceitos e pré-requisitos.",
    agent=pesquisador
)

# Segunda tarefa: produzir o plano estruturado
plano = Task(
    description=(
        "Com base na pesquisa, crie um plano sobre {tema} para {publico}, "
        "com duração de {duracao_minutos} minutos. "
        "O plano DEVE incluir a lista de pre_requisitos identificados e "
        "obrigatoriamente e exatamente três exercícios (nem mais, nem menos)."
    ),
    expected_output=(
        "Plano de aula estruturado de acordo com o modelo PlanoAula, "
        "contendo pré-requisitos e exatamente três exercícios."
    ),
    agent=professor,
    context=[pesquisa],
    output_pydantic=PlanoAula
)

# Criar a crew
crew = Crew(
    agents=[pesquisador, professor],
    tasks=[pesquisa, plano],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    # Executar
    resultado = crew.kickoff(
        inputs={
            "tema": "Interrupções no ESP32",
            "publico": "estudantes de graduação",
            "duracao_minutos": 120
        }
    )

    # Acessar a saída estruturada
    plano_gerado = resultado.pydantic

    # Salvar o resultado na pasta de saída correspondente
    os.makedirs("saidas/ex5", exist_ok=True)
    caminho_saida = os.path.join("saidas", "ex5", "plano_aula.txt")
    with open(caminho_saida, "w", encoding="utf-8") as arquivo:
        arquivo.write(plano_gerado.model_dump_json(indent=2))
    print(f"\nResultado salvo com sucesso em {caminho_saida}")