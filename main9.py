# ============================================================
# Exemplo 9: CrewAI - Guardrail + Revisão + Aprovação Humana Iterativa
# Permite refações contínuas com salvamento de v1, v2, v3, etc.
# ============================================================

import os
from dotenv import load_dotenv
from crewai import Agent, Crew, LLM, Process, Task, TaskOutput

load_dotenv()

# 1. Configurar a LLM local (Ollama)
MODEL_NAME = os.getenv("LOCAL_MODEL", "ollama/qwen2.5:7b-instruct-q4_K_M")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

llm = LLM(
    model=MODEL_NAME,
    base_url=OLLAMA_BASE_URL
)

# 2. Definir o guardrail
# Seções obrigatórias do material
SECOES = [
    "objetivos",
    "conceitos",
    "exemplo",
    "atividade",
    "síntese"
]

def validar_material(resultado: TaskOutput) -> tuple[bool, str]:
    """
    Verifica se o material produzido pelo professor atende aos critérios mínimos.
    """
    texto = resultado.raw.strip()

    # Verifica as seções obrigatórias
    ausentes = []
    for secao in SECOES:
        if secao not in texto.casefold():
            ausentes.append(secao)

    if ausentes:
        return (
            False,
            "Inclua as seções obrigatórias: " + ", ".join(ausentes)
        )

    # Verifica o tamanho mínimo
    if len(texto.split()) < 350:
        return (
            False,
            "O material deve ter pelo menos 350 palavras."
        )

    # Resultado aprovado pelo guardrail
    return True, texto

# 3. Função que constrói a Crew para cada iteração
def construir_crew(feedback: str = "nenhum", arquivo_material: str = "material_professor.md") -> Crew:
    # Agente responsável pela produção do material
    professor = Agent(
        role="Professor conteudista",
        goal="Produzir material didático completo e corrigir falhas indicadas pelo feedback humano",
        backstory=(
            "Professor de graduação orientado por critérios verificáveis "
            "e altamente responsivo a feedbacks de melhoria pedagógica."
        ),
        llm=llm,
        verbose=True
    )

    # Agente responsável pela revisão
    revisor = Agent(
        role="Revisor pedagógico",
        goal="Identificar problemas concretos no material produzido e validar os ajustes",
        backstory=(
            "Revisor criterioso que apresenta correções específicas e detalha pontos aprimorados."
        ),
        llm=llm,
        verbose=True
    )

    # Tarefa 1: produção do material
    producao = Task(
        description=(
            "Produza material sobre {tema} para {publico}. "
            "Use obrigatoriamente as seções Objetivos, Conceitos, Exemplo, Atividade e Síntese. "
            f"Feedback recebido anteriormente: {feedback}."
        ),
        expected_output=(
            "Material didático em Markdown com todas as seções solicitadas e pelo menos 350 palavras."
        ),
        agent=professor,
        guardrail=validar_material,
        guardrail_max_retries=2,
        output_file=arquivo_material
    )

    # Tarefa 2: revisão do material
    revisao = Task(
        description=(
            "Revise cuidadosamente o material produzido pelo professor. "
            "Avalie clareza, correção técnica, sequência didática e adequação ao público. "
            f"Considere se o feedback humano anterior ('{feedback}') foi devidamente atendido. "
            "Indique problemas encontrados e apresente recomendações específicas."
        ),
        expected_output=(
            "Parecer em Markdown contendo avaliação do material e recomendações de melhoria."
        ),
        agent=revisor,
        context=[producao]
    )

    return Crew(
        agents=[professor, revisor],
        tasks=[producao, revisao],
        process=Process.sequential,
        verbose=True
    )

# 4. Função auxiliar para leitura de arquivo
def ler_arquivo(nome_arquivo: str) -> str:
    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        return arquivo.read()

# 5. Execução principal com ciclo iterativo de aprovação humana
if __name__ == "__main__":
    pasta_ex9 = os.path.join("saidas", "ex9")
    os.makedirs(pasta_ex9, exist_ok=True)

    entradas = {
        "tema": "Interrupções no ESP32",
        "publico": "estudantes de graduação"
    }

    versao = 1
    feedback_acumulado = "nenhum (versão inicial)"
    aprovado = False

    while not aprovado:
        print("\n" + "=" * 70)
        print(f" EXECUÇÃO ITERATIVA - VERSÃO {versao} (v{versao}) ")
        print("=" * 70)

        # Definir nomes dos arquivos versionados
        arquivo_material = os.path.join(pasta_ex9, f"material_professor_v{versao}.md")
        arquivo_parecer = os.path.join(pasta_ex9, f"parecer_revisor_v{versao}.md")

        # Cria e executa a Crew da iteração
        crew = construir_crew(
            feedback=feedback_acumulado,
            arquivo_material=arquivo_material
        )
        resultado = crew.kickoff(inputs=entradas)

        # Grava o parecer da versão atual
        parecer = resultado.raw
        with open(arquivo_parecer, "w", encoding="utf-8") as f:
            f.write(parecer)

        # Salva cópias também na raiz ou arquivos gerais para compatibilidade
        with open("material_professor.md", "w", encoding="utf-8") as f:
            f.write(ler_arquivo(arquivo_material))
        with open("parecer_revisor.md", "w", encoding="utf-8") as f:
            f.write(parecer)

        # Exibe as saídas no terminal para o usuário avaliar
        print("\n" + "=" * 70)
        print(f" MATERIAL PRODUZIDO PELO PROFESSOR (v{versao}) ")
        print("=" * 70)
        print(ler_arquivo(arquivo_material))

        print("\n" + "=" * 70)
        print(f" PARECER DO REVISOR (v{versao}) ")
        print("=" * 70)
        print(parecer)

        print("\nArquivos gerados nesta rodada:")
        print(f"- {arquivo_material}")
        print(f"- {arquivo_parecer}")

        # Solicita aprovação humana iterativa
        decisao = input(
            f"\n[Aprovação Humana] Após analisar o MATERIAL e o PARECER da v{versao}, aprovar o material? [s/n]: "
        ).strip().casefold()

        if decisao == "s":
            aprovado = True
            print(f"\n Parabéns! Material v{versao} APROVADO pelo responsável humano com sucesso.")
            print(f"Ciclo iterativo finalizado. Todas as versões (v1 a v{versao}) estão salvas em '{pasta_ex9}'.")
        else:
            feedback_novo = input(f"\n[Rejeitado] Informe o feedback com as correções necessárias para a v{versao + 1}: ").strip()
            feedback_acumulado = feedback_novo if feedback_novo else "Melhore a clareza e detalhe mais os exemplos."
            print(f"\nFeedback registrado: '{feedback_acumulado}'. Iniciando ciclo de refação para v{versao + 1}...\n")
            versao += 1