# ============================================================
# Exemplo 4: Três Agentes com acesso a uma LLM local (Ollama)
# Pesquisador -> Professor -> Revisor Pedagógico
# ============================================================

import os
from dotenv import load_dotenv
from crewai import Agent, Crew, LLM, Process, Task

load_dotenv()

# Configuração da LLM local (Ollama) com fallback configurável via .env
MODEL_NAME = os.getenv("LOCAL_MODEL", "ollama/qwen2.5:7b-instruct-q4_K_M")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

llm = LLM(
    model=MODEL_NAME,
    base_url=OLLAMA_BASE_URL
)

# 1. Primeiro agente: organiza os conceitos técnicos
pesquisador = Agent(
    role="Pesquisador técnico",
    goal="Organizar conceitos e limitações relevantes para uma aula",
    backstory=(
        "Pesquisador criterioso que organiza informações "
        "técnicas de forma objetiva."
    ),
    llm=llm,
    verbose=True
)

# 2. Segundo agente: transforma a pesquisa em material didático
professor = Agent(
    role="Professor conteudista",
    goal="Transformar pesquisa técnica em material didático claro",
    backstory=(
        "Professor que utiliza explicações curtas "
        "seguidas de prática."
    ),
    llm=llm,
    verbose=True
)

# 3. Terceiro agente (solicitado no Exemplo 4): Revisor Pedagógico
revisor = Agent(
    role="Revisor Pedagógico e de Qualidade Técnica",
    goal="Revisar minuciosamente o material didático gerado pelo Professor para assegurar clareza, correção técnica e rigor pedagógico",
    backstory=(
        "Especialista em revisão de material didático para engenharia e computação. "
        "Seu papel é verificar clareza, eliminar ambiguidades, aprimorar a didática "
        "e garantir que o aluno compreenda o conteúdo com precisão técnica."
    ),
    llm=llm,
    verbose=True
)

# Primeira Tarefa: Pesquisa técnica
pesquisar = Task(
    description=(
        "Organize os conceitos essenciais de {tema} "
        "para {publico}."
    ),
    expected_output=(
        "Notas técnicas com conceitos, limitações "
        "e exemplos possíveis."
    ),
    agent=pesquisador
)

# Segunda Tarefa: Produção didática (usa contexto da pesquisa)
produzir = Task(
    description=(
        "Use a pesquisa anterior para criar uma aula "
        "de {duracao} sobre {tema}. "
        "Inclua explicação, exemplo prático e atividade."
    ),
    expected_output=(
        "Material didático em Markdown pronto para revisão."
    ),
    agent=professor,
    context=[pesquisar],
    markdown=True
)

# Terceira Tarefa (solicitada no Exemplo 4): Revisão pedagógica
revisar_tarefa = Task(
    description=(
        "Revise cuidadosamente a aula produzida pelo Professor sobre {tema} para {publico}. "
        "Aprimore a linguagem, valide a correção técnica dos conceitos e exemplos, "
        "e certifique-se de que a estrutura didática esteja impecável. "
        "Entregue a versão final polida e pronta para publicação."
    ),
    expected_output=(
        "Versão final refinada e revisada do material didático em Markdown, "
        "com alta qualidade técnica e pedagógica."
    ),
    agent=revisor,
    context=[produzir],
    markdown=True
)

# Criar a Crew com os 3 agentes e as 3 tarefas sequenciais
crew = Crew(
    agents=[pesquisador, professor, revisor],
    tasks=[pesquisar, produzir, revisar_tarefa],
    process=Process.sequential,
    verbose=True
)

# Inputs parametrizados
dados = {
    "tema": "Interrupções no ESP32",
    "publico": "estudantes de graduação",
    "duracao": "2 horas"
}

if __name__ == "__main__":
    # Executar a crew
    resultado = crew.kickoff(inputs=dados)

    # Exibe o material final produzido no terminal
    print("\n" + "=" * 60)
    print(" MATERIAL DIDÁTICO FINAL REVISADO ")
    print("=" * 60 + "\n")
    print(resultado.raw)

    # Salva o resultado final na pasta de saída correspondente
    os.makedirs("saidas/ex4", exist_ok=True)
    caminho_saida = os.path.join("saidas", "ex4", "aula_revisada.md")
    with open(caminho_saida, "w", encoding="utf-8") as arquivo:
        arquivo.write(resultado.raw)
    print(f"\nResultado salvo com sucesso em {caminho_saida}")
