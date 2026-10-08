# ============================================================
# CrewAI - Ferramenta personalizada
# Consulta a um catálogo de disciplinas em CSV
# ============================================================

import csv

from pydantic import BaseModel, Field
from crewai import Agent, Crew, LLM, Process, Task
from crewai.tools import BaseTool

# Definir a entrada da ferramenta
# Define quais dados a ferramenta espera receber
class ConsultaDisciplinaInput(BaseModel):
    codigo: str = Field(
        description="Código da disciplina, como SE202"
    )

# Criar a ferramenta personalizada
class CatalogoDisciplinasTool(BaseTool):

    # Nome usado pelo agente para identificar a ferramenta.
    name: str = "consultar_catalogo_disciplinas"

    # Ajuda a LLM a decidir quando deve usar a ferramenta.
    description: str = (
        "Consulta nome, nível, pré-requisitos "
        "e observações de uma disciplina."
    )

    # Define o formato da entrada.
    args_schema: type[BaseModel] = ConsultaDisciplinaInput

    # Método executado quando o agente utiliza a ferramenta.
    def _run(self, codigo: str) -> str:
        with open("dados/catalogo_disciplinas.csv", encoding="utf-8", newline="") as arquivo:
            for disciplina in csv.DictReader(arquivo):
                # Procura a disciplina pelo código.
                if disciplina["codigo"].casefold() == codigo.casefold():
                    # Retorna os dados encontrados para o agente.
                    return "; ".join(
                        f"{campo}: {valor}"
                        for campo, valor in disciplina.items()
                    )
        return f"Disciplina {codigo} não encontrada."


# Criar a llm local
llm = LLM(
    model="ollama/qwen3:4b",
    base_url="http://localhost:11434"
)

# Criar o agente
professor = Agent(
    role="Professor responsável por uma disciplina",

    goal=(
        "Adequar o material ao nível "
        "e aos pré-requisitos registrados"
    ),

    backstory=(
        "Professor que consulta o catálogo "
        "antes de planejar a aula."
    ),

    llm=llm,

    # Disponibiliza a ferramenta personalizada ao agente.
    tools=[CatalogoDisciplinasTool()],

    verbose=True
)

# Criar a tarefa
tarefa = Task(
    description=(
        "Consulte a disciplina {codigo} no catálogo. "
        "Depois prepare uma introdução sobre {tema}, "
        "adequada ao nível, aos pré-requisitos "
        "e às observações encontrados."
    ),

    expected_output=(
        "Material em Markdown e um parágrafo explicando "
        "como o catálogo influenciou a aula."
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

# Executar
resultado = crew.kickoff(
    inputs={
        "codigo": "SE202",
        "tema": "Interrupções no ESP32"
    }
)

# Salvar o resultado em arquivo textual
with open("material_personalizado.txt", "w", encoding="utf-8") as arquivo:
    arquivo.write(resultado.raw)

print("Resultado salvo em material_personalizado.txt")
