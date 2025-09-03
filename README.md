# Sistema de Pergunta e Resposta sobre Documentos com LangChain e PGVector

Este sistema permite ingerir um documento PDF em um banco de dados vetorial PostgreSQL + pgVector e fazer perguntas sobre o conteúdo através de um modelo de linguagem (Google Gemini).

## Pré-requisitos

- Python 3.10 ou superior
- Docker e Docker Compose
- Chave de API do Google Gemini

## Estrutura do projeto

```plaintext
/

├── docker-compose.yml      # Arquivo para iniciar o PostgreSQL com pgVector
├── requirements.txt        # Lista de dependências Python
├── .env                    # Arquivo para a chave de API
├── .env.example            # Template para o arquivo .env
├── documents.pdf           # Documento pdf para fazer a ingestão
├── src/
│   ├── ingest.py           # Script para ler, processar e armazenar o PDF
│   ├── chat.py             # Script para a interface de linha de comando(CLI)
│   ├── search.py           # Script de busca
└── README.md               # Instruções de configuração e execução
```

## Configuração do ambiente

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. Crie um ambiente virtual Python:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Linux/macOS
   # OU
   .\venv\Scripts\activate   # No Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure sua chave de API:

   ```bash
   cp .env.example .env
   # Edite o arquivo .env e coloque sua GOOGLE_API_KEY
   ```

5. Coloque seu documento PDF na raiz do projeto com o nome `src/*.pdf`

## Iniciar o banco de dados

```bash
docker compose up -d
```

## Ingerir o documento

```bash
python3 src/ingest.py
```

Este processo irá:

1. Carregar o arquivo `document.pdf`
2. Dividir o documento em chunks de texto
3. Gerar embeddings vetoriais usando o Google Gemini
4. Armazenar os vetores no banco de dados PostgreSQL

## Iniciar o chat

```bash
python3 src/chat.py
```

Use a interface de linha de comando para fazer perguntas sobre o documento. O sistema irá:

1. Buscar as informações mais relevantes no banco de dados vetorial
2. Usar o modelo Gemini para gerar uma resposta baseada apenas no conteúdo do documento
3. Apresentar a resposta na linha de comando

Digite 'sair' para encerrar o programa.

## Observações

- O sistema é configurado para responder apenas com base no conteúdo do documento
- Informações fora do contexto do documento serão respondidas com "Não tenho informações necessárias para responder sua pergunta."
