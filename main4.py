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

# 3. Terceiro agente Revisor Pedagógico
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

# Segunda Tarefa: Produção didática (usa contexto da pesquisa e salva em arquivo)
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
    markdown=True,
    output_file=os.path.join("saidas", "ex4", "material_professor.md")
)

# Terceira Tarefa: Revisão pedagógica (recebe como contexto o material do Professor e gera o parecer/versão revisada)
revisar_tarefa = Task(
    description=(
        "Revise cuidadosamente a aula produzida pelo Professor sobre {tema} para {publico}. "
        "Aprimore a linguagem, valide a correção técnica dos conceitos e exemplos, "
        "e certifique-se de que a estrutura didática esteja impecável. "
        "Entregue um parecer pedagógico detalhado com a versão revisada e pronta para publicação."
    ),
    expected_output=(
        "Parecer pedagógico e versão final revisada do material didático em Markdown."
    ),
    agent=revisor,
    context=[produzir],
    markdown=True,
    output_file=os.path.join("saidas", "ex4", "parecer_revisor.md")
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
    # Garante a existência do diretório de saída
    pasta_ex4 = os.path.join("saidas", "ex4")
    os.makedirs(pasta_ex4, exist_ok=True)

    # Executar a crew
    resultado = crew.kickoff(inputs=dados)

    # Exibe o parecer final produzido no terminal
    print("\n" + "=" * 60)
    print(" PARECER / MATERIAL FINAL DO REVISOR ")
    print("=" * 60 + "\n")
    print(resultado.raw)

    # Salva também a versão em .txt do parecer do revisor
    caminho_revisor_txt = os.path.join(pasta_ex4, "parecer_revisor.txt")
    with open(caminho_revisor_txt, "w", encoding="utf-8") as arquivo:
        arquivo.write(resultado.raw)

    # Salva também a versão em .txt da produção do professor se o .md existir
    caminho_prof_md = os.path.join(pasta_ex4, "material_professor.md")
    if os.path.exists(caminho_prof_md):
        with open(caminho_prof_md, "r", encoding="utf-8") as f_in:
            conteudo_prof = f_in.read()
        with open(os.path.join(pasta_ex4, "producao_professor.txt"), "w", encoding="utf-8") as f_out:
            f_out.write(conteudo_prof)

    print("\nArquivos salvos com sucesso:")
    print(f"- Material do Professor: {caminho_prof_md}")
    print(f"- Parecer do Revisor: {os.path.join(pasta_ex4, 'parecer_revisor.md')}")
