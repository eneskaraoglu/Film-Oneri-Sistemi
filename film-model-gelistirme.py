import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import numpy as np
import matplotlib.pyplot as plt

# 1. Veri Yükleme ve Hazırlık
def load_data():
    # Veri setlerini yükle
    ratings = pd.read_csv('D:/CODE-BASE/PYTHON/Film Öneri Sistemi/ratings.dat', sep='::', engine='python', header=None)
    movies = pd.read_csv('D:/CODE-BASE/PYTHON/Film Öneri Sistemi/movies.dat', sep='::', engine='python', header=None)

    # Örneğin, sadece ilk 1 milyon satırı kullanarak:
    # ratings = ratings.sample(n=1000000, random_state=42)


    # Kolon isimleri ekleme
    ratings.columns = ['userId', 'movieId', 'rating', 'timestamp']
    movies.columns = ['movieId', 'title', 'genres']

    return ratings, movies

# 2. Veri Hazırlama
def preprocess_data(ratings):
    # Kullanıcı ve Film ID'lerini encode et
    user_encoder = LabelEncoder()
    movie_encoder = LabelEncoder()

    ratings['userId'] = user_encoder.fit_transform(ratings['userId'])
    ratings['movieId'] = movie_encoder.fit_transform(ratings['movieId'])

    # Eğitim ve test setlerini ayırma
    X = ratings[['userId', 'movieId']].values
    y = ratings['rating'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test, len(user_encoder.classes_), len(movie_encoder.classes_)

# 3. Model Tanımlama
class RecommenderModel(tf.keras.Model):
    def __init__(self, num_users, num_movies, embedding_dim=20):
        super().__init__()
        self.user_embedding = tf.keras.layers.Embedding(num_users, embedding_dim)
        self.movie_embedding = tf.keras.layers.Embedding(num_movies, embedding_dim)
        self.dot = tf.keras.layers.Dot(axes=1)

    def call(self, inputs):
        user_vector = self.user_embedding(inputs[:, 0])
        movie_vector = self.movie_embedding(inputs[:, 1])
        return self.dot([user_vector, movie_vector])

# 4. Model Eğitimi
def train_model(X_train, y_train, X_test, y_test, num_users, num_movies):
    # Modeli başlat
    model = RecommenderModel(num_users, num_movies)

    # Modeli derle
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='mean_squared_error',
        metrics=['mean_absolute_error']
    )

    # Modeli eğit
    history = model.fit(
        x=X_train,
        y=y_train,
        batch_size=1024,
        epochs=5,
        validation_data=(X_test, y_test)
    )

    return model, history

# 5. Eğitim Sonuçlarını Görselleştir
def plot_training(history):
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

# 6. Tahmin Yapma
def recommend_movies(model, user_id, num_movies, movies_df):
    user_movies = np.array([[user_id, movie_id] for movie_id in range(num_movies)])
    predicted_ratings = model.predict(user_movies)
    top_movies = predicted_ratings.flatten().argsort()[-10:][::-1]
    print("\nKullanıcı için önerilen filmler:")
    for movie_id in top_movies:
        movie_title = movies_df[movies_df['movieId'] == movie_id]['title'].values[0]
        print(movie_title)

# Main
if __name__ == "__main__":
    # Veri yükleme
    ratings, movies = load_data()

    # Veri hazırlama
    X_train, X_test, y_train, y_test, num_users, num_movies = preprocess_data(ratings)

    # Model eğitimi
    model, history = train_model(X_train, y_train, X_test, y_test, num_users, num_movies)

    # Eğitim sonuçlarını görselleştir
    plot_training(history)

    # Film önerileri
    user_id = 0  # Örneğin, kullanıcı 0
    recommend_movies(model, user_id, num_movies, movies)
