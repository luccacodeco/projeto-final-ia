from app.database import ratings_df
import pandas as pd
import numpy as np

# Carregar filmes já pré-processados
movies_df = pd.read_csv("data/movies_processed.csv")

# Carregar matriz de similaridade já pronta
cosine_sim_movies = np.load("data/cosine_sim.npy")

def hybrid_recommend(user_id, top_n=10):
    print(f"Usuários existentes: {ratings_df['userId'].unique().tolist()[:10]} ...")
    print(f"userId {user_id} está presente? {user_id in ratings_df['userId'].unique()}")

    user_ratings = ratings_df[ratings_df['userId'] == user_id]
    if user_ratings.empty:
        return []

    liked_movies = user_ratings[user_ratings['rating'] >= 3.0]['movieId'].tolist()
    watched_movies = set(user_ratings['movieId'])

    content_scores = np.zeros(len(movies_df))
    for movie_id in liked_movies:
        idx = movies_df.index[movies_df['movieId'] == movie_id]
        if not idx.empty:
            content_scores += cosine_sim_movies[idx[0]]

    if content_scores.sum() > 0:
        content_scores /= content_scores.sum()

    similar_users = ratings_df[
        (ratings_df['movieId'].isin(liked_movies)) & 
        (ratings_df['userId'] != user_id)
    ]['userId'].value_counts().head(100).index.tolist()

    if similar_users:
        collab_ratings = ratings_df[ratings_df['userId'].isin(similar_users)]
        mean_ratings = collab_ratings.groupby('movieId')['rating'].mean()
    else:
        mean_ratings = pd.Series()

    final_scores = []
    for idx, row in movies_df.iterrows():
        mid = row['movieId']
        if mid in watched_movies:
            continue

        content_score = content_scores[idx]
        collab_score = mean_ratings.get(mid, 0) if not mean_ratings.empty else 0
        score = content_score if collab_score == 0 else 0.5 * content_score + 0.5 * collab_score
        final_scores.append((mid, score))

    top = sorted(final_scores, key=lambda x: x[1], reverse=True)[:top_n]
    top_ids = [t[0] for t in top]
    return movies_df[movies_df['movieId'].isin(top_ids)][['movieId', 'title', 'genres']].to_dict(orient='records')
