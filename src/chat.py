import os
from dotenv import load_dotenv
from search import search_prompt

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Verificar a variável de ambiente do Google
for k in ("GOOGLE_API_KEY", "PGVECTOR_URL","PGVECTOR_COLLECTION"):
    if not os.getenv(k):
        raise RuntimeError(f"Environment variable {k} is not set")
    
def main():

    # Criar o loop de interação (CLI)
    print("\n=== Sistema de Perguntas e Respostas sobre o Documento ===")
    print("Digite 'sair' para encerrar o programa\n")
    
    while True:
        # Obter pergunta do usuário
        user_question = input("\nFaça sua pergunta: ")
        
        # Verificar se o usuário quer sair
        if user_question.lower() in ['sair', 'exit', 'quit']:
            print("Encerrando o programa. Até logo!")
            break
        
        # Buscar e responder à pergunta do usuário
        try:
            response = search_prompt(user_question)
            print(f"\nRESPOSTA: {response}")
        except Exception as e:
            print(f"Erro ao processar pergunta: {e}")

if __name__ == "__main__":
    main()