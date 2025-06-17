
# Documentação Técnica — Sistema de Recomendação de Filmes com FastAPI

Este projeto implementa um sistema híbrido de recomendação de filmes, utilizando Python, FastAPI, pandas e Docker. A aplicação expõe uma API REST que permite interagir com o motor de recomendação por meio de operações como criação de usuários, adição de filmes, envio de avaliações e geração de recomendações personalizadas.

---

## Sumário

- [Visão Geral](#visão-geral)
- [Modelo de Recomendação](#modelo-de-recomendação)
- [Preprocessamento](#preprocessamento)
- [Instalação Local](#instalação-local)
- [Execução com Docker](#execução-com-docker)
- [Endpoints da API](#endpoints-da-api)
- [Exemplos de Requisição](#exemplos-de-requisição)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Observações Finais](#observações-finais)

---

## Visão Geral

A API oferece funcionalidades para:

- Criar usuários e adicionar filmes.
- Registrar avaliações de filmes por usuários.
- Gerar recomendações híbridas com base nas avaliações e gêneros dos filmes.

---

## Modelo de Recomendação

O sistema implementa um **modelo híbrido**, composto por:

### 1. Filtragem Colaborativa (User-Based)
- Considera os usuários que avaliaram os mesmos filmes que o usuário alvo.
- Calcula a média das avaliações feitas por usuários similares.

### 2. Filtragem Baseada em Conteúdo
- Utiliza **TF-IDF** sobre os gêneros dos filmes.
- Calcula a similaridade entre filmes usando **cosine similarity**.

### Combinação Híbrida

O escore final é uma média ponderada dos dois métodos:

```python
score = 0.5 * score_colaborativo + 0.5 * score_conteúdo
```

Caso algum dos componentes esteja indisponível (por exemplo, usuário novo), a recomendação será baseada exclusivamente no método restante.

---

## Preprocessamento

O arquivo `preprocess.py` (opcional e não obrigatório para a execução da API) realiza o cálculo e salvamento antecipado da matriz de similaridade entre filmes (`cosine_sim.npy`). Ele deve ser executado apenas uma vez para gerar essa matriz e economizar tempo de carregamento:

```bash
python preprocess.py
```

Esse script:
- Lê o `movie.csv`
- Calcula o TF-IDF sobre os gêneros
- Salva `cosine_sim.npy` em `data/`

**Nota:** Os arquivos `.csv` e `.npy` foram disponibilizados via [Google Drive](https://drive.google.com/file/d/1WWBC_6zS7bRcVV8ZBy3bVcBzecCYQf3Y/view?usp=sharing) e não são versionados no Git.

---

## Instalação Local

1. Clone o repositório:

```bash
git clone https://github.com/luccacodeco/projeto-final-ia.git
cd seu-repositorio
```

2. Crie o ambiente virtual:

```bash
python -m venv venv
# Ative conforme o sistema operacional
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate       # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute o servidor FastAPI:

```bash
uvicorn app.main:app --reload
```

5. Acesse a documentação Swagger em `http://localhost:8000/docs`

---

## Execução com Docker

1. Certifique-se de ter o Docker instalado e ativo.

2. Construa a imagem:

```bash
docker compose build
```

3. Suba a aplicação:

```bash
docker compose up
```

4. Acesse a API no navegador: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Endpoints da API

| Método | Rota                   | Descrição                                       |
|--------|------------------------|-------------------------------------------------|
| POST   | /usuarios              | Cria um novo usuário (simulado)                |
| POST   | /filmes                | Adiciona um novo filme                         |
| POST   | /avaliacoes            | Registra uma avaliação                         |
| GET    | /recomendacoes/{id}    | Retorna recomendações para um usuário          |

---

## Exemplos de Requisição

### Criar usuário

- Parâmetro de query `user_id`: 100000

Swagger: `POST /usuarios?user_id=100000`

### Adicionar filme

```json
{
  "movieId": 99999,
  "title": "Exemplo de Filme",
  "genres": "Action|Adventure"
}
```

### Adicionar avaliação

```json
{
  "userId": 100000,
  "movieId": 99999,
  "rating": 4.5
}
```

### Obter recomendações

- Parâmetro de path `user_id`: 1
- Parâmetro de query `top_n`: 5

Swagger: `GET /recomendacoes/1?top_n=5`

---

## Estrutura do Projeto

```
.
├── app/
│   ├── main.py         # Endpoints da API
│   ├── model.py        # Lógica de recomendação híbrida
│   ├── database.py     # Simulação de base de dados em memória
│   └── __init__.py
├── data/               # Contém os dados CSV e NPY (não versionados)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── preprocess.py       # Cálculo antecipado da matriz de similaridade (opcional)
└── README.md
```

---

## Observações Finais

- A pasta `data/` foi excluída do versionamento por conter arquivos grandes (>100MB). Baixe separadamente via [Google Drive](https://drive.google.com/file/d/1WWBC_6zS7bRcVV8ZBy3bVcBzecCYQf3Y/view?usp=sharing).
- Usuários não são persistidos — são simulados a partir das avaliações.
- A recomendação usa fallback se não houver dados suficientes para um dos métodos.
