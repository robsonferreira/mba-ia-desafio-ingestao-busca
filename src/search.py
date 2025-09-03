import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_postgres import PGVector
from langchain.prompts import PromptTemplate

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt(question=None):
    # Passo 1: Inicializar modelos
    embedding_model = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001"
    )
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.2
    )

    # Passo 2: Conectar ao banco de dados vetorial

    try:
        vectorstore = PGVector(
            embeddings=embedding_model,
            collection_name=os.getenv("PGVECTOR_COLLECTION"),
            connection=os.getenv("PGVECTOR_URL"),
            use_jsonb=True,
        )
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return
    
    PROMPT = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "user_question"]
    )

    # Buscar documentos relevantes
    try:
        results = vectorstore.similarity_search_with_score(question, k=10)
    except Exception as e:
        print(f"Erro ao buscar no banco de dados: {e}")
    
    if not results:
        print("RESPOSTA: Não encontrei informações relevantes no documento.")

    # Extrair o contexto dos documentos recuperados
    context_text = ""
    for doc, score in results:
        context_text += doc.page_content + "\n\n"
    
    # Preparar o prompt com o contexto e a pergunta
    formatted_prompt = PROMPT.format(
        contexto=context_text,
        pergunta=question
    )
    
    # Gerar resposta usando o LLM
    try:
        response = llm.invoke(formatted_prompt)
        return response.content
    except Exception as e:
        print(f"Erro ao gerar resposta: {e}")