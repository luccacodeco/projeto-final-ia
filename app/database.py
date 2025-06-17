import pandas as pd

# Carregamento dos dados
movies_df = pd.read_csv('data/movie.csv')
ratings_df = pd.read_csv('data/rating.csv')

def add_user(user_id):
    """Verificação simbólica (usuário só existe se tiver avaliação)."""
    global ratings_df
    if user_id in ratings_df['userId'].unique():
        return False
    return True

def add_movie(movie):
    global movies_df
    if movie['movieId'] in movies_df['movieId'].values:
        return False
    movies_df = pd.concat([movies_df, pd.DataFrame([movie])], ignore_index=True)
    print(f"[add_movie] Filme adicionado: {movie}")
    return True

def add_rating(user_id, movie_id, rating):
    global ratings_df
    new_row = pd.DataFrame([{
        'userId': int(user_id),
        'movieId': int(movie_id),
        'rating': float(rating),
        'timestamp': pd.Timestamp.now()
    }])
    ratings_df = pd.concat([ratings_df, new_row], ignore_index=True)
    print(f"[add_rating] Avaliação registrada: {new_row.to_dict(orient='records')}")
    return True

def get_all_users():
    return ratings_df['userId'].unique().tolist()
