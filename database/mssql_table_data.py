import pyodbc
from datetime import date


connection = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=music_app;"
    "UID=sa;"
    "PWD=12345;"
    "trusted_connection=yes"
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
    cursor.execute(f"ALTER TABLE {table} NOCHECK CONSTRAINT ALL;")
    cursor.execute(f"DELETE FROM {table};")
    cursor.execute(f"ALTER TABLE {table} CHECK CONSTRAINT ALL;")


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
cursor.executemany(
    "INSERT INTO [User] (UserUsername, UserEmail, UserPassword, UserSignUpDate, UserNameSurname) VALUES (?, ?, ?, ?, ?)",
    users
)


artists = [
    ("The Beatles",), ("Taylor Swift",), ("Drake",), ("Adele",), ("BTS",),
    ("Ed Sheeran",), ("Coldplay",), ("Lady Gaga",), ("Kendrick Lamar",), ("Imagine Dragons",)
]
cursor.executemany("INSERT INTO Artist (ArtistName) VALUES (?)", artists)


genres = [
    ("Pop",), ("Rock",), ("Hip Hop",), ("Jazz",), ("Electronic",),
    ("Classical",), ("Indie",), ("R&B",), ("Reggae",), ("Blues",)
]
cursor.executemany("INSERT INTO Genre (GenreName) VALUES (?)", genres)


moods = [
    ("Happy",), ("Sad",), ("Energetic",), ("Romantic",), ("Chill",),
    ("Reflective",), ("Angry",), ("Hopeful",), ("Excited",), ("Relaxed",)
]
cursor.executemany("INSERT INTO Mood (MoodName) VALUES (?)", moods)

subscriptions = [
    ("Free", 0.00, 0), ("Basic", 5.99, 30), ("Premium", 9.99, 30),
    ("Family", 14.99, 30), ("Annual Premium", 99.99, 365),
    ("Student Plan", 4.99, 30), ("Duo Plan", 12.99, 30),
    ("Lifetime", 499.99, 0), ("Trial", 0.00, 14), ("Enterprise", 199.99, 365)
]
cursor.executemany(
    "INSERT INTO SubscriptionPlan (SubscriptionPlanName, SubscriptionPlanPrice, SubscriptionPlanDuration) VALUES (?, ?, ?)",
    subscriptions
)


albums = [
    ("Abbey Road", 1969, 1), ("1989", 2014, 2), ("Scorpion", 2018, 3),
    ("25", 2015, 4), ("Map of the Soul: Persona", 2019, 5),
    ("Divide", 2017, 6), ("A Rush of Blood to the Head", 2002, 7),
    ("The Fame Monster", 2009, 8), ("DAMN.", 2017, 9), ("Evolve", 2017, 10)
]
cursor.executemany(
    "INSERT INTO Album (AlbumName, AlbumReleaseYear, ArtistId) VALUES (?, ?, ?)",
    albums
)


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
cursor.executemany(
    "INSERT INTO Song (SongTitle, SongDuration, SongReleaseDate, AlbumId, ArtistId) VALUES (?, ?, ?, ?, ?)",
    songs
)


connection.commit()
cursor.close()
connection.close()
