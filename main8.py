# ============================================================
# Exemplo 8: CrewAI - Knowledge + Memory + Múltiplos Agentes
# Demonstração em duas execuções usando memória persistente (.crewai/memory_curso)
# ============================================================

import os
import sys
from dotenv import load_dotenv
from crewai import Agent, Crew, LLM, Memory, Process, Task
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource

load_dotenv()

# Configuração da LLM local (Ollama)
MODEL_NAME = os.getenv("LOCAL_MODEL", "ollama/qwen2.5:7b-instruct-q4_K_M")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

llm = LLM(
    model=MODEL_NAME,
    base_url=OLLAMA_BASE_URL
)

# Base de conhecimento institucional
caminho_base = os.path.join("dados", "base_institucional.txt")
conhecimento = TextFileKnowledgeSource(
    file_paths=[caminho_base]
)

# Embeddings locais (usa bge-m3 instalado no Ollama)
embedder = {
    "provider": "ollama",
    "config": {
        "model": "bge-m3",
        "model_name": "bge-m3",
        "url": OLLAMA_BASE_URL
    }
}

# Memória compartilhada e persistente
storage_dir = ".crewai/memory_curso"
memoria = Memory(
    llm=llm,
    embedder=embedder,
    storage=storage_dir
)

# Criar os agentes
pesquisador = Agent(
    role="Pesquisador técnico",
    goal="Selecionar conteúdo correto e adequado ao tema e às preferências pedagógicas da disciplina",
    backstory=(
        "Pesquisador que organiza informações técnicas e adapta o conteúdo "
        "conforme orientações e histórico da disciplina."
    ),
    llm=llm,
    verbose=True
)

professor = Agent(
    role="Professor conteudista",
    goal="Criar material alinhado às diretrizes institucionais e às preferências pedagógicas registradas",
    backstory=(
        "Professor experiente em aprendizagem prática que respeita rigidamente "
        "o estilo pedagógico definido para o curso."
    ),
    llm=llm,
    verbose=True
)

revisor = Agent(
    role="Revisor pedagógico",
    goal="Verificar clareza, correção técnica e conformidade com as diretrizes e preferências pedagógicas",
    backstory=(
        "Revisor criterioso que avalia a qualidade do material e emite parecer detalhado."
    ),
    llm=llm,
    verbose=True
)

# Criar as tarefas com parametrização da instrução_adicional
pesquisa = Task(
    description=(
        "Organize os conceitos essenciais de {tema}. "
        "Considere as seguintes orientações pedagógicas: {orientacao_pedagogica}."
    ),
    expected_output="Notas técnicas verificáveis, concisas e alinhadas às orientações.",
    agent=pesquisador
)

producao = Task(
    description=(
        "Produza o material completo sobre {tema}. "
        "Consulte o conhecimento institucional, utilize as notas de pesquisa e "
        "atenda estritamente à orientação: {orientacao_pedagogica}. "
        "Use as seções: Objetivos, Conceitos, Exemplo Prático, Atividade e Síntese."
    ),
    expected_output="Material didático completo em Markdown com exemplo prático e atividade.",
    agent=professor,
    context=[pesquisa]
)

revisao = Task(
    description=(
        "Revise o material produzido pelo professor sobre {tema}. "
        "Avalie clareza, correção, sequência didática e se atendeu à orientação: {orientacao_pedagogica}. "
        "Emita parecer detalhado e recomendações de melhoria."
    ),
    expected_output="Parecer pedagógico em Markdown avaliando o material.",
    agent=revisor,
    context=[producao],
    markdown=True
)

def criar_crew():
    return Crew(
        agents=[pesquisador, professor, revisor],
        tasks=[pesquisa, producao, revisao],
        process=Process.sequential,
        knowledge_sources=[conhecimento],
        embedder=embedder,
        memory=memoria,
        verbose=True
    )

def executar_rodada(rodada: int, tema: str, orientacao: str, arquivo_saida: str):
    print("\n" + "=" * 70)
    print(f" EXECUÇÃO {rodada}: {tema} ")
    print(f" ORIENTAÇÃO: {orientacao} ")
    print("=" * 70 + "\n")

    crew = criar_crew()
    resultado = crew.kickoff(
        inputs={
            "tema": tema,
            "orientacao_pedagogica": orientacao
        }
    )

    os.makedirs(os.path.dirname(arquivo_saida), exist_ok=True)
    with open(arquivo_saida, "w", encoding="utf-8") as f:
        f.write(resultado.raw)
    
    # Salva também na raiz para compatibilidade caso requisitado
    with open("parecer_revisao.txt", "w", encoding="utf-8") as f:
        f.write(resultado.raw)

    print(f"\nResultado da Execução {rodada} salvo em: {arquivo_saida}")
    return resultado.raw

if __name__ == "__main__":
    pasta_saida = os.path.join("saidas", "ex8")
    os.makedirs(pasta_saida, exist_ok=True)

    # Permite rodar execução 1, execução 2 ou ambas em sequência
    modo = sys.argv[1] if len(sys.argv) > 1 else "todas"

    # EXECUÇÃO 1:
    # Tema: "Agentes inteligentes com n8n"
    # Preferência explícita: "Para esta disciplina, priorize exemplos práticos com ESP32, explicações curtas e uma atividade ao final"
    if modo in ("1", "todas"):
        executar_rodada(
            rodada=1,
            tema="Agentes inteligentes com n8n",
            orientacao="Para esta disciplina, priorize exemplos práticos com ESP32, explicações curtas e uma atividade ao final.",
            arquivo_saida=os.path.join(pasta_saida, "parecer_execucao1_n8n.txt")
        )

    # EXECUÇÃO 2:
    # Tema: "Agentes inteligentes com CrewAI"
    # Não repete a preferência: "Produza o novo material mantendo, quando relevante, as preferências pedagógicas adotadas anteriormente"
    if modo in ("2", "todas"):
        executar_rodada(
            rodada=2,
            tema="Agentes inteligentes com CrewAI",
            orientacao="Produza o novo material mantendo, quando relevante, as preferências pedagógicas adotadas anteriormente.",
            arquivo_saida=os.path.join(pasta_saida, "parecer_execucao2_crewai.txt")
        )