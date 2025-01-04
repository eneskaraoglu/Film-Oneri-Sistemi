import pandas as pd

# Veri setini yükleyin
ratings = pd.read_csv('D:/CODE-BASE/PYTHON/Film Öneri Sistemi/ratings.dat', sep='::', engine='python', header=None)  # Dosya yolunu doğru girdiğinizden emin olun
movies = pd.read_csv('D:/CODE-BASE/PYTHON/Film Öneri Sistemi/movies.dat', sep='::', engine='python', header=None)

# Ratings dosyasına kolon isimleri ekleme
ratings.columns = ['userId', 'movieId', 'rating', 'timestamp']

# Movies dosyasına kolon isimleri ekleme
movies.columns = ['movieId', 'title', 'genres']

# İlk birkaç satıra göz atma
print("Ratings Dosyasından İlk 5 Satır:")
print(ratings.head())

print("\nMovies Dosyasından İlk 5 Satır:")
print(movies.head())

# Eksik veri olup olmadığını kontrol edin
print("\nEksik Veri Kontrolü (Ratings):")
print(ratings.isnull().sum())

print("\nEksik Veri Kontrolü (Movies):")
print(movies.isnull().sum())

# Veri setlerinin boyutlarını kontrol edin
print("\nRatings Boyutu:", ratings.shape)
print("Movies Boyutu:", movies.shape)

# En çok puan alan filmleri bulalım
most_rated = ratings.groupby('movieId').size().sort_values(ascending=False).head(10)
print("\nEn Çok Puan Alan Filmler:")
print(most_rated)

# Bu filmlerin isimlerini movies veri setinden çekelim
most_rated_titles = movies[movies['movieId'].isin(most_rated.index)]
print("\nEn Çok Puan Alan Filmlerin İsimleri:")
print(most_rated_titles)

# Filmlerin ortalama puanlarını hesaplayalım
avg_ratings = ratings.groupby('movieId')['rating'].mean().sort_values(ascending=False).head(10)
print("\nEn Yüksek Ortalama Puan Alan Filmler:")
print(avg_ratings)

# Bu filmlerin isimlerini movies veri setinden çekelim
top_rated_titles = movies[movies['movieId'].isin(avg_ratings.index)]
print("\nEn Yüksek Ortalama Puan Alan Filmlerin İsimleri:")
print(top_rated_titles)

# Her kullanıcının ortalama puanı
user_avg_rating = ratings.groupby('userId')['rating'].mean()
print("\nKullanıcıların Ortalama Puanları:")
print(user_avg_rating.head())

# Pivot tablo oluşturma
user_movie_matrix = ratings.pivot(index='userId', columns='movieId', values='rating')
print("\nKullanıcı-Film Puan Matrisi:")
print(user_movie_matrix.head())
