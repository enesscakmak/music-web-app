import mysql.connector
from datetime import date, timedelta

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="music_app"
)
cursor = connection.cursor()

tables = [
    "UserLike", "UserPlaylist", "UserSubscription",
    "AlbumSong", "ArtistSong", "ArtistAlbum",
    "SongGenre", "SongMood", "PlaylistSong",
    "Playlist", "Mood", "SubscriptionPlan",
    "Genre", "Song", "Album", "Artist", "User"
]

for table in tables:
    cursor.execute(f"SET FOREIGN_KEY_CHECKS = 0;")
    cursor.execute(f"TRUNCATE TABLE {table};")
    cursor.execute(f"SET FOREIGN_KEY_CHECKS = 1;")


users = [
    ("john_doe", "john_doe@example.com", "hashed_password1", date(2023, 5, 15), "John Doe"),
    ("jane_doe", "jane_doe@example.com", "hashed_password2", date(2023, 6, 20), "Jane Doe"),
    ("music_lover", "music_lover@example.com", "hashed_password3", date(2023, 7, 10), "Alex Smith"),
    ("rock_fan", "rock_fan@example.com", "hashed_password4", date(2023, 8, 5), "Emily Davis"),
    ("pop_star", "pop_star@example.com", "hashed_password5", date(2023, 9, 25), "Michael Brown"),
    ("classic_enthusiast", "classic_enth@example.com", "hashed_password6", date(2023, 10, 12), "Sophia Taylor"),
    ("indie_vibes", "indie_vibes@example.com", "hashed_password7", date(2023, 11, 1), "Liam Wilson"),
    ("rap_king", "rap_king@example.com", "hashed_password8", date(2023, 12, 3), "Noah Martinez"),
    ("jazz_blues", "jazz_blues@example.com", "hashed_password9", date(2024, 1, 5), "Olivia Garcia"),
    ("electro_fan", "electro_fan@example.com", "hashed_password10", date(2024, 2, 14), "Isabella Rodriguez")
]
cursor.executemany("INSERT INTO User (UserUsername, UserEmail, UserPassword, UserSignUpDate, UserNameSurname) VALUES (%s, %s, %s, %s, %s)", users)

artists = [
    ("The Beatles",), ("Taylor Swift",), ("Drake",), ("Adele",), ("BTS",),
    ("Ed Sheeran",), ("Coldplay",), ("Lady Gaga",), ("Kendrick Lamar",), ("Imagine Dragons",)
]
cursor.executemany("INSERT INTO Artist (ArtistName) VALUES (%s)", artists)

genres = [
    ("Pop",), ("Rock",), ("Hip Hop",), ("Jazz",), ("Electronic",),
    ("Classical",), ("Indie",), ("R&B",), ("Reggae",), ("Blues",)
]
cursor.executemany("INSERT INTO Genre (GenreName) VALUES (%s)", genres)

moods = [
    ("Happy",), ("Sad",), ("Energetic",), ("Romantic",), ("Chill",),
    ("Reflective",), ("Angry",), ("Hopeful",), ("Excited",), ("Relaxed",)
]
cursor.executemany("INSERT INTO Mood (MoodName) VALUES (%s)", moods)

subscriptions = [
    ("Free", 0.00, 0), ("Basic", 5.99, 30), ("Premium", 9.99, 30),
    ("Family", 14.99, 30), ("Annual Premium", 99.99, 365),
    ("Student Plan", 4.99, 30), ("Duo Plan", 12.99, 30),
    ("Lifetime", 499.99, 0), ("Trial", 0.00, 14), ("Enterprise", 199.99, 365)
]
cursor.executemany("INSERT INTO `SubscriptionPlan` (SubscriptionPlanName, SubscriptionPlanPrice, SubscriptionPlanDuration) VALUES (%s, %s, %s)", subscriptions)

albums = [
    ("Abbey Road", 1969, 1), ("1989", 2014, 2), ("Scorpion", 2018, 3),
    ("25", 2015, 4), ("Map of the Soul: Persona", 2019, 5),
    ("Divide", 2017, 6), ("A Rush of Blood to the Head", 2002, 7),
    ("The Fame Monster", 2009, 8), ("DAMN.", 2017, 9),
    ("Evolve", 2017, 10)
]
cursor.executemany("INSERT INTO Album (AlbumName, AlbumReleaseYear, ArtistId) VALUES (%s, %s, %s)", albums)

songs = [
    ("Here Comes the Sun", "00:03:05", date(1969, 9, 26), 1, 1),
    ("Shake It Off", "00:03:39", date(2014, 8, 18), 2, 2),
    ("God's Plan", "00:03:18", date(2018, 1, 19), 3, 3),
    ("Hello", "00:04:55", date(2015, 10, 23), 4, 4),
    ("Boy With Luv", "00:03:49", date(2019, 4, 12), 5, 5),
    ("Shape of You", "00:03:53", date(2017, 1, 6), 6, 6),
    ("Clocks", "00:05:07", date(2002, 8, 26), 7, 7),
    ("Bad Romance", "00:04:54", date(2009, 10, 26), 8, 8),
    ("HUMBLE.", "00:02:57", date(2017, 3, 30), 9, 9),
    ("Believer", "00:03:24", date(2017, 2, 1), 10, 10)
]
cursor.executemany("INSERT INTO Song (SongTitle, SongDuration, SongReleaseDate, AlbumId, ArtistId) VALUES (%s, %s, %s, %s, %s)", songs)

playlists = [
    ("Morning Motivation", date(2024, 12, 1), 1), ("Chill Vibes", date(2024, 12, 2), 2),
    ("Workout Hits", date(2024, 12, 3), 3), ("Romantic Evenings", date(2024, 12, 4), 4),
    ("Party Anthems", date(2024, 12, 5), 5), ("Study Sessions", date(2024, 12, 6), 6),
    ("Road Trip", date(2024, 12, 7), 7), ("Throwback Classics", date(2024, 12, 8), 8),
    ("Indie Discoveries", date(2024, 12, 9), 9), ("Relax and Unwind", date(2024, 12, 10), 10)
]
cursor.executemany("INSERT INTO Playlist (PlaylistName, PlaylistCreationDate, UserId) VALUES (%s, %s, %s)", playlists)

album_songs = [(i, i) for i in range(1, 11)]
cursor.executemany("INSERT INTO AlbumSong (AlbumId, SongId) VALUES (%s, %s)", album_songs)

playlist_songs = [(i, i) for i in range(1, 11)]
cursor.executemany("INSERT INTO PlaylistSong (PlaylistId, SongId) VALUES (%s, %s)", playlist_songs)

song_genres = [(i, i) for i in range(1, 11)]
cursor.executemany("INSERT INTO SongGenre (SongId, GenreId) VALUES (%s, %s)", song_genres)

song_moods = [(i, i) for i in range(1, 11)]
cursor.executemany("INSERT INTO SongMood (SongId, MoodId) VALUES (%s, %s)", song_moods)

artist_albums = [
    (1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
    (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)
]
cursor.executemany("INSERT INTO ArtistAlbum (ArtistId, AlbumId) VALUES (%s, %s)", artist_albums)

artist_songs = [
    (1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
    (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)
]
cursor.executemany("INSERT INTO ArtistSong (ArtistId, SongId) VALUES (%s, %s)", artist_songs)

user_likes = [
    (1, 1), (1, 2), (2, 3), (2, 4), (3, 5),
    (4, 6), (5, 7), (6, 8), (7, 9), (8, 10),
    (9, 1), (10, 2)
]
cursor.executemany("INSERT INTO UserLike (UserId, SongId) VALUES (%s, %s)", user_likes)

user_playlists = [
    (1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
    (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)
]
cursor.executemany("INSERT INTO UserPlaylist (UserId, PlaylistId) VALUES (%s, %s)", user_playlists)

user_subscriptions = [
    (1, 3), (2, 2), (3, 1), (4, 4), (5, 5),
    (6, 6), (7, 7), (8, 3), (9, 8), (10, 9)
]
cursor.executemany("INSERT INTO UserSubscription (UserId, SubscriptionPlanId) VALUES (%s, %s)", user_subscriptions)

connection.commit()

cursor.close()
connection.close()

