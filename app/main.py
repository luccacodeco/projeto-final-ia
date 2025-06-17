from fastapi import FastAPI
from pydantic import BaseModel
from app.model import hybrid_recommend
from app.database import add_user, add_movie, add_rating

app = FastAPI()

class Movie(BaseModel):
    movieId: int
    title: str
    genres: str

class Rating(BaseModel):
    userId: int
    movieId: int
    rating: float

@app.post("/usuarios")
def criar_usuario(user_id: int):
    if add_user(user_id):
        return {"message": f"Usuário {user_id} criado (simulado)"}
    return {"message": f"Usuário {user_id} já existe."}

@app.post("/filmes")
def criar_filme(movie: Movie):
    if add_movie(movie.dict()):
        return {"message": f"Filme {movie.title} adicionado."}
    return {"message": f"Filme {movie.title} já existe."}

@app.post("/avaliacoes")
def avaliar(rating: Rating):
    add_rating(rating.userId, rating.movieId, rating.rating)
    return {"message": f"Avaliação registrada para usuário {rating.userId} no filme {rating.movieId}."}

@app.get("/recomendacoes/{user_id}")
def recomendar(user_id: int, top_n: int = 5):
    recs = hybrid_recommend(user_id, top_n)
    return {"userId": user_id, "recomendacoes": recs}
