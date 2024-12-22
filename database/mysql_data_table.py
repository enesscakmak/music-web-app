import mysql.connector

connection = mysql.connector.connect(
    host="localhost",       # MySQL sunucu adresi
    user="root",            # MySQL kullanıcı adı
    password="12345",       # MySQL şifre
    database="music_app"    # Veritabanı adı
)

cursor = connection.cursor()

tables = {
    "User": """
        CREATE TABLE User (
            UserId INT AUTO_INCREMENT PRIMARY KEY,
            UserUsername VARCHAR(100),
            UserEmail VARCHAR(150),
            UserPassword VARCHAR(255),
            UserSignUpDate DATE,
            UserNameSurname VARCHAR(100)
        );
    """,
    "Artist": """
        CREATE TABLE Artist (
            ArtistId INT AUTO_INCREMENT PRIMARY KEY,
            ArtistName VARCHAR(100)
        );
    """,
    "Song": """
        CREATE TABLE Song (
            SongId INT AUTO_INCREMENT PRIMARY KEY,
            SongTitle VARCHAR(150),
            SongDuration TIME,
            SongReleaseDate DATE,
            AlbumId INT,
            ArtistId INT,
            FOREIGN KEY (AlbumId) REFERENCES Album(AlbumId),
            FOREIGN KEY (ArtistId) REFERENCES Artist(ArtistId)
        );
    """,
    "Album": """
        CREATE TABLE Album (
            AlbumId INT AUTO_INCREMENT PRIMARY KEY,
            AlbumName VARCHAR(150),
            AlbumReleaseYear YEAR,
            ArtistId INT,
            FOREIGN KEY (ArtistId) REFERENCES Artist(ArtistId)
        );
    """,
    "Genre": """
        CREATE TABLE Genre (
            GenreId INT AUTO_INCREMENT PRIMARY KEY,
            GenreName VARCHAR(100)
        );
    """,
    "Playlist": """
        CREATE TABLE Playlist (
            PlaylistId INT AUTO_INCREMENT PRIMARY KEY,
            PlaylistName VARCHAR(150),
            PlaylistCreationDate DATE,
            UserId INT,
            FOREIGN KEY (UserId) REFERENCES User(UserId)
        );
    """,
    "Mood": """
        CREATE TABLE Mood (
            MoodId INT AUTO_INCREMENT PRIMARY KEY,
            MoodName VARCHAR(100)
        );
    """,
    "SubscriptionPlan": """
        CREATE TABLE SubscriptionPlan (
            SubscriptionId INT AUTO_INCREMENT PRIMARY KEY,
            SubscriptionPlanName VARCHAR(100),
            SubscriptionPlanPrice DECIMAL(10,2),
            SubscriptionPlanDuration INT
        );
    """,
    "UserLike": """
        CREATE TABLE UserLike (
            LikeId INT AUTO_INCREMENT PRIMARY KEY,
            UserId INT,
            SongId INT,
            FOREIGN KEY (UserId) REFERENCES User(UserId),
            FOREIGN KEY (SongId) REFERENCES Song(SongId)
        );
    """,
    "UserPlaylist": """
        CREATE TABLE UserPlaylist (
            UserPlaylistId INT AUTO_INCREMENT PRIMARY KEY,
            UserId INT,
            PlaylistId INT,
            FOREIGN KEY (UserId) REFERENCES User(UserId),
            FOREIGN KEY (PlaylistId) REFERENCES Playlist(PlaylistId)
        );
    """,
    "UserSubscription": """
        CREATE TABLE UserSubscription (
            UserSubscriptionId INT AUTO_INCREMENT PRIMARY KEY,
            UserId INT,
            SubscriptionPlanId INT,
            FOREIGN KEY (UserId) REFERENCES User(UserId),
            FOREIGN KEY (SubscriptionPlanId) REFERENCES SubscriptionPlan(SubscriptionId)
        );
    """,
    "AlbumSong": """
        CREATE TABLE AlbumSong (
            AlbumSongId INT AUTO_INCREMENT PRIMARY KEY,
            AlbumId INT,
            SongId INT,
            FOREIGN KEY (AlbumId) REFERENCES Album(AlbumId),
            FOREIGN KEY (SongId) REFERENCES Song(SongId)
        );
    """,
    "ArtistSong": """
        CREATE TABLE ArtistSong (
            ArtistSongId INT AUTO_INCREMENT PRIMARY KEY,
            ArtistId INT,
            SongId INT,
            FOREIGN KEY (ArtistId) REFERENCES Artist(ArtistId),
            FOREIGN KEY (SongId) REFERENCES Song(SongId)
        );
    """,
    "ArtistAlbum": """
        CREATE TABLE ArtistAlbum (
            ArtistAlbumId INT AUTO_INCREMENT PRIMARY KEY,
            ArtistId INT,
            AlbumId INT,
            FOREIGN KEY (ArtistId) REFERENCES Artist(ArtistId),
            FOREIGN KEY (AlbumId) REFERENCES Album(AlbumId)
        );
    """,
    "SongGenre": """
        CREATE TABLE SongGenre (
            SongGenreId INT AUTO_INCREMENT PRIMARY KEY,
            SongId INT,
            GenreId INT,
            FOREIGN KEY (SongId) REFERENCES Song(SongId),
            FOREIGN KEY (GenreId) REFERENCES Genre(GenreId)
        );
    """,
    "SongMood": """
        CREATE TABLE SongMood (
            SongMoodId INT AUTO_INCREMENT PRIMARY KEY,
            SongId INT,
            MoodId INT,
            FOREIGN KEY (SongId) REFERENCES Song(SongId),
            FOREIGN KEY (MoodId) REFERENCES Mood(MoodId)
        );
    """,
    "PlaylistSong": """
        CREATE TABLE PlaylistSong (
            PlaylistSongId INT AUTO_INCREMENT PRIMARY KEY,
            PlaylistId INT,
            SongId INT,
            FOREIGN KEY (PlaylistId) REFERENCES Playlist(PlaylistId),
            FOREIGN KEY (SongId) REFERENCES Song(SongId)
        );
    """
}

for table_name, create_query in tables.items():
    try:
        cursor.execute(create_query)
        print(f"'{table_name}' tablosu başarıyla oluşturuldu.")
    except mysql.connector.Error as err:
        print(f"'{table_name}' tablosu oluşturulurken hata: {err}")

cursor.close()
connection.close()
