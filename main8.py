# ============================================================
# CrewAI - Knowledge + Memory + múltiplos agentes
# Tudo 100% local com Ollama
# ============================================================

from crewai import Agent, Crew, LLM, Memory, Process, Task
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource

# Criar a llm local
llm = LLM(
    model="ollama/qwen3:4b",
    base_url="http://localhost:11434"
)

# Base de conhecimento
# Arquivo que será utilizado como conhecimento da Crew.
conhecimento = TextFileKnowledgeSource(
    file_paths=["dados/base_institucional.txt"]
)

# Embeddings locais
# O modelo de embeddings também é executado pelo Ollama.
# Nenhuma API externa é necessária.
embedder = {
    "provider": "ollama",
    "config": {
        "model_name": "qwen3-embedding:0.6b",
        "url": "http://localhost:11434/api/embeddings"
    }
}

# Memória
# Tanto a análise da memória quanto os embeddings
# são realizados localmente.
memoria = Memory(
    llm=llm,
    embedder=embedder,
    storage=".crewai/memory_curso"
)

# Criar os agentes
pesquisador = Agent(
    role="Pesquisador técnico",
    goal="Selecionar conteúdo correto e adequado ao tema",
    backstory=(
        "Pesquisador que organiza informações técnicas "
        "de forma objetiva."
    ),
    llm=llm,
    verbose=True
)


professor = Agent(
    role="Professor conteudista",
    goal="Criar material alinhado às diretrizes institucionais",
    backstory=(
        "Professor experiente em aprendizagem baseada em prática."
    ),
    llm=llm,
    verbose=True
)


revisor = Agent(
    role="Revisor pedagógico",
    goal=(
        "Verificar clareza, correção, sequência didática "
        "e adequação ao tempo"
    ),
    backstory=(
        "Revisor criterioso que apresenta "
        "justificativas específicas."
    ),
    llm=llm,
    verbose=True
)

# Criar as tarefas
pesquisa = Task(
    description="Organize os conceitos essenciais de {tema}.",
    expected_output="Notas técnicas verificáveis e concisas.",
    agent=pesquisador
)

producao = Task(
    description=(
        "Produza material sobre {tema}. "
        "Consulte o conhecimento institucional "
        "e utilize a pesquisa anterior."
    ),
    expected_output=(
        "Material com objetivos, conceitos, "
        "exemplo, atividade e síntese."
    ),
    agent=professor,
    context=[pesquisa]
)

revisao = Task(
    description=(
        "Revise o material. "
        "Avalie clareza, correção, sequência didática "
        "e adequação ao tempo. "
        "Apresente correções específicas."
    ),
    expected_output=(
        "Parecer em Markdown com avaliação "
        "e recomendações de melhoria."
    ),
    agent=revisor,
    context=[producao],
    markdown=True
)

# Criar a crew
crew = Crew(
    agents=[pesquisador, professor, revisor],

    tasks=[pesquisa, producao, revisao],

    process=Process.sequential,

    # Conhecimento institucional.
    knowledge_sources=[conhecimento],

    # Embeddings totalmente locais.
    embedder=embedder,

    # Memória totalmente local.
    memory=memoria,

    verbose=True
)

# Executar
resultado = crew.kickoff(
    inputs={
        "tema": "Interrupções no ESP32"
    }
)

# Salvar o resultado em arquivo textual
with open("parecer_revisao.txt", "w", encoding="utf-8") as arquivo:
    arquivo.write(resultado.raw)

print("Resultado salvo em parecer_revisao.txt")