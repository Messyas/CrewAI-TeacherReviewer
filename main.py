# Biblioteca padrão do Python para acessar
# variáveis de ambiente
import os

# load_dotenv permite carregar variáveis
# armazenadas em um arquivo .env
from dotenv import load_dotenv

# Importamos a classe LLM do CrewAI.
from crewai import LLM

# Carrega as variáveis definidas no arquivo .env
load_dotenv()

# Cria o objeto que representa a LLM
llm = LLM(
model=os.getenv

("MODEL", "gemini/gemini-3.6-flash"),

max_retries=3
)

# Define o assunto da pergunta
tema = "Interrupções no ESP32"

# Envia diretamente uma instrução para a LLM
resposta = llm.call(
f"Explique {tema} para estudantes de graduação."
"Inclua um exemplo prático."
)

# Exibe a resposta produzida pela LLM
print(resposta)