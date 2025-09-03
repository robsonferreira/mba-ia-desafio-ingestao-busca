import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# Importar a classe de embeddings do Google
from langchain_google_genai import GoogleGenerativeAIEmbeddings 
from langchain_core.documents import Document
from langchain_postgres import PGVector

load_dotenv()


# Verificar a variável de ambiente do Google
for k in ("GOOGLE_API_KEY", "PGVECTOR_URL","PGVECTOR_COLLECTION"):
    if not os.getenv(k):
        raise RuntimeError(f"Environment variable {k} is not set")


current_dir = Path(__file__).parent.parent
pdf_path = current_dir / "document.pdf"

def ingest_pdf():
    print("Iniciando processo de ingestão do documento...")
    
    # Passo 2: Carregar o documento PDF
    try:
        documents = PyPDFLoader(str(pdf_path)).load()
        print(f"Documento carregado com sucesso! Total de páginas: {len(documents)}")
    except Exception as e:
        print(f"Erro ao carregar o documento: {e}")
        return
    
    # Passo 3: Dividir o documento em chunks
    chunks = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150, add_start_index=False).split_documents(documents)
    if not chunks:
        raise SystemExit(0)
    print(f"Documento dividido em {len(chunks)} chunks")

    enriched = [
        Document(
            page_content=d.page_content,
            metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
        )
        for d in chunks
    ]    

    ids = [f"doc-{i}" for i in range(len(enriched))]
    
    # Passo 4: Inicializar o modelo de embeddings
    embedding_model = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001"
    )
    
    # Passo 5: Conectar e ingerir no banco de dados
    
    try:
        # Ingerir os documentos no banco de dados vetorial
        db = PGVector(
            embeddings=embedding_model,
            collection_name=os.getenv("PGVECTOR_COLLECTION"),
            connection=os.getenv("PGVECTOR_URL"),
            use_jsonb=True,
        )
        db.add_documents(documents=enriched, ids=ids)
        print(f"Ingestão completa! {len(chunks)} chunks inseridos com sucesso no banco de dados.")
        print(f"Coleção '{os.getenv("PGVECTOR_COLLECTION")}' criada com sucesso.")
    except Exception as e:
        print(f"Erro durante a ingestão no banco de dados: {e}")
        return


if __name__ == "__main__":
    ingest_pdf()