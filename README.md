
# Sistema de Recomendação de Filmes com FastAPI

Este projeto implementa um sistema híbrido de recomendação de filmes, utilizando Python, FastAPI, pandas e Docker. Ele expõe uma API REST para interação com o sistema de recomendação, suportando operações como criação de usuários, envio de avaliações e obtenção de recomendações personalizadas.

## Sumário

- [Visão Geral](#visão-geral)
- [Modelo de Recomendação](#modelo-de-recomendação)
- [Instalação Local](#instalação-local)
- [Execução com Docker](#execução-com-docker)
- [Endpoints da API](#endpoints-da-api)
- [Exemplos de Requisição](#exemplos-de-requisição)
- [Estrutura do Projeto](#estrutura-do-projeto)

## Visão Geral

A API oferece funcionalidades para:

- Criar usuários e adicionar filmes.
- Registrar avaliações de filmes por usuários.
- Gerar recomendações híbridas para um usuário com base em preferências anteriores.

## Modelo de Recomendação

O sistema utiliza um **modelo híbrido**, combinando:

- **Filtragem Colaborativa (baseada em usuários):**
  - Identifica usuários similares com base em filmes avaliados em comum.
  - Agrega avaliações médias dos usuários similares.

- **Filtragem Baseada em Conteúdo:**
  - Utiliza TF-IDF sobre os gêneros dos filmes para calcular similaridade entre títulos.

A recomendação final pondera ambos os modelos:

```python
score = 0.5 * score_colaborativo + 0.5 * score_conteúdo
```

Caso não existam usuários similares ou o conteúdo não possa ser avaliado, a recomendação usa fallback para a parte disponível.

## Instalação Local

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

2. Crie o ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate    # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute a API:

```bash
uvicorn app.main:app --reload
```

5. Acesse em `http://localhost:8000/docs`

## Execução com Docker

1. Certifique-se de ter o Docker instalado e em execução.

2. Construa a imagem:

```bash
docker compose build
```

3. Inicie o serviço:

```bash
docker compose up
```

4. Acesse a API em `http://localhost:8000/docs`

## Endpoints da API

| Método | Rota                   | Descrição                                       |
|--------|------------------------|-------------------------------------------------|
| POST   | /usuarios              | Cria um novo usuário (simulado)                |
| POST   | /filmes                | Adiciona um novo filme                         |
| POST   | /avaliacoes            | Registra uma avaliação                         |
| GET    | /recomendacoes/{id}    | Retorna recomendações para um usuário          |

## Exemplos de Requisição

### Criar usuário

Parâmetro query (user_id): 100000 (exemplo)

### Adicionar filme

{
  "movieId": 99999,
  "title": "Exemplo de Filme",
  "genres": "Action|Adventure"
}

### Adicionar avaliação

{
  "userId": 100000,
  "movieId": 99999,
  "rating": 4.5
}

### Obter recomendações

Parâmetro path (user_id): 1
Parâmetro Query (top_n): 5

## Estrutura do Projeto

```
.
├── app/
│   ├── main.py         # Endpoints da API
│   ├── model.py        # Lógica de recomendação híbrida
│   ├── database.py     # Simulação de base de dados em memória
│   └── __init__.py
├── data/
│   ├── movie.csv       # Base de filmes
│   └── rating.csv      # Base de avaliações
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Observações

- Os dados são carregados em memória (sem banco de dados real).
- A criação de usuários é simbólica (não persistida).
- A pasta `data/` deve conter os arquivos `movie.csv` e `rating.csv`.
