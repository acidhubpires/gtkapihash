Gtk_ApiGeoHash

Uma API desenvolvida com FastAPI para processamento de dados geoespaciais. A aplicação permite o upload de arquivos (como KMZ, GeoJSON, e ZIP com shapefiles) e processa as informações geográficas, gerando nomenclaturas e coordenadas específicas.
Estrutura do Projeto

plaintext

Gtk_ApiGeoHash/
├── .venv/                   # Ambiente virtual com dependências Python
├── app/                     # Diretório principal da aplicação FastAPI
│   ├── __init__.py
│   ├── api/                 # Contém rotas da API
│   ├── models/              # Modelos de dados (Pydantic)
│   ├── services/            # Lógica de processamento e manipulação de dados
│   ├── templates/           # Arquivos HTML para o frontend
│   ├── uploads/             # Diretório onde arquivos enviados são armazenados
│   ├── utils/               # Funções utilitárias
│   └── main.py              # Arquivo principal da aplicação FastAPI
├── frontend/                # Código do frontend da aplicação (React/Vue)
├── output/                  # Resultados processados
├── upload/                  # Diretório com arquivos de upload e extração
├── .gitignore               # Arquivos/pastas ignorados pelo Git
├── Dockerfile               # Instruções para criar imagem Docker
├── requirements.txt         # Dependências do projeto Python
└── README.md                # Documentação da aplicação

Pré-requisitos

    Python 3.8+
    FastAPI e Uvicorn
    Ferramentas opcionais:
        Docker (para contêinerização)
        Git (para versionamento de código)

Instalação

    Clone o repositório:

    bash

git clone https://github.com/seu_usuario/gtk_apigeohash.git
cd gtk_apigeohash

Crie e ative um ambiente virtual:

bash

python -m venv .venv
.\.venv\Scripts\activate  # No Windows
source .venv/bin/activate # No macOS/Linux

Instale as dependências:

bash

    pip install -r requirements.txt

Execução da Aplicação

    Defina o PYTHONPATH (apenas se necessário):

    Caso ocorra algum problema de importação, configure o PYTHONPATH para o diretório raiz:

    bash

# Windows PowerShell
$env:PYTHONPATH = "C:\Users\aaopi\Developer\Ariadny_Technology\Sandbox\Gtk_ApiGeoHash"

# macOS/Linux
export PYTHONPATH=$(pwd)

Inicie a API:

bash

    uvicorn app.main:app --reload

    O servidor deve estar rodando em http://127.0.0.1:8000.

Documentação Interativa

A API conta com uma documentação interativa que permite testar os endpoints diretamente no navegador.

    Swagger UI: http://127.0.0.1:8000/docs
    Redoc: http://127.0.0.1:8000/redoc

Endpoints Principais

    GET /: Página inicial, que renderiza index.html.
    GET /upload: Formulário de upload de arquivos para o processamento de dados geoespaciais.
    POST /upload: Endpoint para processar o upload de arquivos (KMZ, GeoJSON ou ZIP).

Estrutura dos Arquivos

    app/main.py: Ponto de entrada da aplicação, onde as rotas são incluídas.
    app/api/route.py: Define as rotas da API, incluindo upload de arquivos.
    app/services/: Contém lógica de processamento, como file_processing.py e geo_processing.py.

Exemplo de Uso

Após iniciar a aplicação, você pode acessar o Swagger em http://127.0.0.1:8000/docs para fazer uploads de arquivos diretamente e visualizar os dados processados.
Exemplo de Requisição via cURL

Para testar o upload de um arquivo via cURL:

bash

curl -X 'POST' \
  'http://127.0.0.1:8000/upload' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@caminho_do_arquivo.kmz'

Testes

Para rodar os testes, você pode configurar um ambiente de testes ou utilizar pytest:

bash

pip install pytest
pytest

Deploy com Docker (Opcional)

    Build da imagem Docker:

    bash

docker build -t gtk_apigeohash .

Execute o container:

bash

    docker run -d -p 8000:8000 gtk_apigeohash


Contribuição

    Faça um fork do projeto.
    Crie uma branch para sua feature (git checkout -b feature/nova-feature).
    Commit suas mudanças (git commit -m 'Adiciona nova feature').
    Faça o push para a branch (git push origin feature/nova-feature).
    Abra um Pull Request.

Licença

Este projeto é licenciado sob a MIT License.

Esse README.md fornece instruções detalhadas para configurar, executar, e testar a aplicação, além de opções para contêinerização e contribuição. Ajuste conforme necessário para atender às especificidades do seu projeto.