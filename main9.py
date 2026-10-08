# ============================================================
# CrewAI - Guardrail + revisão + aprovação humana
# ============================================================

from crewai import Agent, Crew, LLM, Process, Task, TaskOutput

# 1. Criar a LLM local
llm = LLM(
    model="ollama/qwen3:4b",
    base_url="http://localhost:11434"
)

# 2. Definir o guardrail
# Seções obrigatórias do material.
SECOES = [
    "objetivos",
    "conceitos",
    "exemplo",
    "atividade",
    "síntese"
]

def validar_material(resultado: TaskOutput) -> tuple[bool, str]:
    """
    Verifica se o material produzido pelo professor
    atende aos critérios mínimos.
    """

    texto = resultado.raw.strip()

    # Verifica as seções obrigatórias.
    ausentes = []
    for secao in SECOES:
        if secao not in texto.casefold():
            ausentes.append(secao)

    if ausentes:
        return (
            False,
            "Inclua as seções obrigatórias: "
            + ", ".join(ausentes)
        )

    # Verifica o tamanho mínimo.
    if len(texto.split()) < 350:
        return (
            False,
            "O material deve ter pelo menos 350 palavras."
        )

    # Resultado aprovado pelo guardrail.
    return True, texto

# 3. Função que constrói a Crew
def construir_crew(feedback: str = "nenhum", arquivo_material: str = "material_professor.md") -> Crew:

    # Agente responsável pela produção do material
    professor = Agent(
        role="Professor conteudista",

        goal=(
            "Produzir material didático completo "
            "e corrigir falhas indicadas"
        ),

        backstory=(
            "Professor de graduação orientado "
            "por critérios verificáveis."
        ),

        llm=llm,
        verbose=True
    )

    # Agente responsável pela revisão
    revisor = Agent(
        role="Revisor pedagógico",

        goal=(
            "Identificar problemas concretos "
            "no material produzido"
        ),

        backstory=(
            "Revisor criterioso que apresenta "
            "correções específicas."
        ),

        llm=llm,
        verbose=True
    )

    # Tarefa 1: produção do material
    producao = Task(
        description=(
            "Produza material sobre {tema} para {publico}. "
            "Use obrigatoriamente as seções Objetivos, "
            "Conceitos, Exemplo, Atividade e Síntese. "
            f"Feedback recebido anteriormente: {feedback}."
        ),

        expected_output=(
            "Material didático em Markdown com todas "
            "as seções solicitadas e pelo menos 350 palavras."
        ),

        agent=professor,

        # Validação automática.
        guardrail=validar_material,

        # Até duas novas tentativas caso o guardrail falhe.
        guardrail_max_retries=2,

        # Salva somente a produção do professor.
        output_file=arquivo_material
    )

    # Tarefa 2: revisão do material
    revisao = Task(
        description=(
            "Revise cuidadosamente o material produzido "
            "pelo professor. Avalie clareza, correção técnica, "
            "sequência didática e adequação ao público. "
            "Indique problemas encontrados e apresente "
            "recomendações específicas."
        ),

        expected_output=(
            "Parecer em Markdown contendo avaliação "
            "do material e recomendações de melhoria."
        ),

        agent=revisor,

        # O revisor recebe a produção do professor.
        context=[producao]
    )

    # Criar a Crew
    return Crew(
        agents=[professor, revisor],
        tasks=[producao, revisao],
        process=Process.sequential,
        verbose=True
    )


# 4. Função auxiliar para mostrar um arquivo
def ler_arquivo(nome_arquivo: str) -> str:
    """
    Lê e retorna o conteúdo de um arquivo textual.
    """

    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        return arquivo.read()


# 5. Dados de entrada
entradas = {
    "tema": "Interrupções no ESP32",
    "publico": "estudantes de graduação"
}

# 6. PRIMEIRA EXECUÇÃO
arquivo_material = "material_professor.md"
arquivo_parecer = "parecer_revisor.md"

crew = construir_crew(arquivo_material=arquivo_material)

resultado = crew.kickoff(inputs=entradas)


# 7. Separar as duas saídas

# Material produzido pelo professor.
#
# Foi salvo automaticamente pela Task usando output_file.

material = ler_arquivo(arquivo_material)


# Parecer do revisor.
#
# Como a revisão é a última Task da Crew,
# resultado.raw corresponde à saída do revisor.

parecer = resultado.raw


# Salvar o parecer separadamente.
with open(arquivo_parecer, "w", encoding="utf-8") as arquivo:
    arquivo.write(parecer)


# 8. Mostrar AO HUMANO as duas saídas

print("\n")
print("=" * 70)
print("MATERIAL PRODUZIDO PELO PROFESSOR")
print("=" * 70)
print(material)


print("\n")
print("=" * 70)
print("PARECER DO REVISOR")
print("=" * 70)
print(parecer)


print("\nArquivos gerados:")
print(f"- {arquivo_material}")
print(f"- {arquivo_parecer}")


# 9. APROVAÇÃO HUMANA

decisao = input(
    "\nApós analisar o MATERIAL e o PARECER, "
    "aprovar o material? [s/n]: "
).strip().casefold()

# 10. Material aprovado

if decisao == "s":
    print("\nMaterial aprovado pelo responsável humano.")
# 11. Material rejeitado
else:
    # Humano fornece o feedback.
    feedback = input("\nInforme as correções necessárias: ").strip()

    # Arquivos da nova versão.
    arquivo_material_revisado = (
        "material_professor_revisado.md"
    )

    arquivo_parecer_revisado = (
        "parecer_revisor_revisado.md"
    )


    # Construir novamente a Crew, agora com feedback.

    crew_revisada = construir_crew(
        feedback=feedback,
        arquivo_material=arquivo_material_revisado
    )


    # Nova execução.

    resultado_revisado = crew_revisada.kickoff(
        inputs=entradas
    )

    # 12. Separar novamente as duas saídas
    # Nova produção do professor.
    material_revisado = ler_arquivo(
        arquivo_material_revisado
    )

    # Novo parecer do revisor.
    parecer_revisado = resultado_revisado.raw


    # Salvar novo parecer.
    with open(arquivo_parecer_revisado, "w", encoding="utf-8") as arquivo:
        arquivo.write(parecer_revisado)

    # 13. Mostrar a nova versão ao humano

    print("\n")
    print("=" * 70)
    print("NOVA VERSÃO DO MATERIAL")
    print("=" * 70)
    print(material_revisado)


    print("\n")
    print("=" * 70)
    print("NOVO PARECER DO REVISOR")
    print("=" * 70)
    print(parecer_revisado)


    print("\nArquivos da nova execução:")
    print(f"- {arquivo_material_revisado}")
    print(f"- {arquivo_parecer_revisado}")