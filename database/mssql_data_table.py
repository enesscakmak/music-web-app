import pyodbc


connection = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'
    'DATABASE=music_app;'
    'UID=sa;'
    'PWD=12345;'
    'Trusted_Connection=yes;'
)

cursor = connection.cursor()


tables = {
    "User": """
        CREATE TABLE [User] (
            UserId INT IDENTITY(1,1) PRIMARY KEY,
            UserUsername NVARCHAR(100),
            UserEmail NVARCHAR(150),
            UserPassword NVARCHAR(255),
            UserSignUpDate DATE,
            UserNameSurname NVARCHAR(100)
        );
    """,
    "Artist": """
        CREATE TABLE Artist (
            ArtistId INT IDENTITY(1,1) PRIMARY KEY,
            ArtistName NVARCHAR(100)
        );
    """,
    "Song": """
        CREATE TABLE Song (
            SongId INT IDENTITY(1,1) PRIMARY KEY,
            SongTitle NVARCHAR(150),
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
            AlbumId INT IDENTITY(1,1) PRIMARY KEY,
            AlbumName NVARCHAR(150),
            AlbumReleaseYear INT,
            ArtistId INT,
            FOREIGN KEY (ArtistId) REFERENCES Artist(ArtistId)
        );
    """,
    "Genre": """
        CREATE TABLE Genre (
            GenreId INT IDENTITY(1,1) PRIMARY KEY,
            GenreName NVARCHAR(100)
        );
    """,
    "Playlist": """
        CREATE TABLE Playlist (
            PlaylistId INT IDENTITY(1,1) PRIMARY KEY,
            PlaylistName NVARCHAR(150),
            PlaylistCreationDate DATE,
            UserId INT,
            FOREIGN KEY (UserId) REFERENCES [User](UserId)
        );
    """,
    "Mood": """
        CREATE TABLE Mood (
            MoodId INT IDENTITY(1,1) PRIMARY KEY,
            MoodName NVARCHAR(100)
        );
    """,
    "SubscriptionPlan": """
        CREATE TABLE SubscriptionPlan (
            SubscriptionId INT IDENTITY(1,1) PRIMARY KEY,
            SubscriptionPlanName NVARCHAR(100),
            SubscriptionPlanPrice DECIMAL(10,2),
            SubscriptionPlanDuration INT
        );
    """,
    "UserLike": """
        CREATE TABLE UserLike (
            LikeId INT IDENTITY(1,1) PRIMARY KEY,
            UserId INT,
            SongId INT,
            FOREIGN KEY (UserId) REFERENCES [User](UserId),
            FOREIGN KEY (SongId) REFERENCES Song(SongId)
        );
    """,
    "UserPlaylist": """
        CREATE TABLE UserPlaylist (
            UserPlaylistId INT IDENTITY(1,1) PRIMARY KEY,
            UserId INT,
            PlaylistId INT,
            FOREIGN KEY (UserId) REFERENCES [User](UserId),
            FOREIGN KEY (PlaylistId) REFERENCES Playlist(PlaylistId)
        );
    """,
    "UserSubscription": """
        CREATE TABLE UserSubscription (
            UserSubscriptionId INT IDENTITY(1,1) PRIMARY KEY,
            UserId INT,
            SubscriptionPlanId INT,
            FOREIGN KEY (UserId) REFERENCES [User](UserId),
            FOREIGN KEY (SubscriptionPlanId) REFERENCES SubscriptionPlan(SubscriptionId)
        );
    """,
    "AlbumSong": """
        CREATE TABLE AlbumSong (
            AlbumSongId INT IDENTITY(1,1) PRIMARY KEY,
            AlbumId INT,
            SongId INT,
            FOREIGN KEY (AlbumId) REFERENCES Album(AlbumId),
            FOREIGN KEY (SongId) REFERENCES Song(SongId)
        );
    """,
    "ArtistSong": """
        CREATE TABLE ArtistSong (
            ArtistSongId INT IDENTITY(1,1) PRIMARY KEY,
            ArtistId INT,
            SongId INT,
            FOREIGN KEY (ArtistId) REFERENCES Artist(ArtistId),
            FOREIGN KEY (SongId) REFERENCES Song(SongId)
        );
    """,
    "ArtistAlbum": """
        CREATE TABLE ArtistAlbum (
            ArtistAlbumId INT IDENTITY(1,1) PRIMARY KEY,
            ArtistId INT,
            AlbumId INT,
            FOREIGN KEY (ArtistId) REFERENCES Artist(ArtistId),
            FOREIGN KEY (AlbumId) REFERENCES Album(AlbumId)
        );
    """,
    "SongGenre": """
        CREATE TABLE SongGenre (
            SongGenreId INT IDENTITY(1,1) PRIMARY KEY,
            SongId INT,
            GenreId INT,
            FOREIGN KEY (SongId) REFERENCES Song(SongId),
            FOREIGN KEY (GenreId) REFERENCES Genre(GenreId)
        );
    """,
    "SongMood": """
        CREATE TABLE SongMood (
            SongMoodId INT IDENTITY(1,1) PRIMARY KEY,
            SongId INT,
            MoodId INT,
            FOREIGN KEY (SongId) REFERENCES Song(SongId),
            FOREIGN KEY (MoodId) REFERENCES Mood(MoodId)
        );
    """,
    "PlaylistSong": """
        CREATE TABLE PlaylistSong (
            PlaylistSongId INT IDENTITY(1,1) PRIMARY KEY,
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
        connection.commit()
        print(f"'{table_name}' table created successfully.")
    except Exception as e:
        print(f"Error creating '{table_name}' table: {e}")


cursor.close()
connection.close()
