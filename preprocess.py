# preprocess.py
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Carregar filmes
movies_df = pd.read_csv("data/movie.csv")

# TF-IDF nos gêneros
tfidf = TfidfVectorizer(token_pattern=r"[a-zA-Z0-9\-]+")
tfidf_matrix = tfidf.fit_transform(movies_df["genres"])

# Similaridade de cosseno
cosine_sim = cosine_similarity(tfidf_matrix)

# Salvar arquivos otimizados
np.save("data/cosine_sim.npy", cosine_sim)
movies_df.to_csv("data/movies_processed.csv", index=False)

print("✅ Pré-processamento finalizado e arquivos salvos.")
