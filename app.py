from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import mysql.connector
from datetime import date
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345',
    'database': 'music_app'
}

logging.basicConfig(level=logging.DEBUG)

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Remove the /add route from app.py
@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT SongId, SongTitle FROM Song ORDER BY RAND() LIMIT 5;")
    songs = cursor.fetchall()

    user_id = session.get('user_id')
    if user_id:
        cursor.execute("SELECT PlaylistId, PlaylistName FROM Playlist WHERE UserId = %s;", (user_id,))
        playlists = cursor.fetchall()
    else:
        playlists = []

    cursor.execute("SELECT ArtistId, ArtistName FROM Artist ORDER BY RAND() LIMIT 5;")
    artists = cursor.fetchall()

    cursor.execute("SELECT AlbumId, AlbumName FROM Album ORDER BY RAND() LIMIT 5;")
    albums = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('index.html', songs=songs, playlists=playlists, artists=artists, albums=albums)
@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        data = request.get_json()
        data_type = data.get('data_type')
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            if data_type == 'song':
                # Add song logic
                pass
            elif data_type == 'album':
                # Add album logic
                pass
            elif data_type == 'playlist':
                playlist_name = data.get('playlistName')
                user_id = session.get('user_id')
                if user_id and playlist_name:
                    cursor.execute("INSERT INTO Playlist (PlaylistName, PlaylistCreationDate, UserId) VALUES (%s, %s, %s)",
                                   (playlist_name, date.today(), user_id))
                    playlist_id = cursor.lastrowid
                    response = {'status': 'success', 'message': 'Playlist added successfully!', 'playlistId': playlist_id}
                else:
                    raise ValueError("Invalid user ID or playlist name")
            elif data_type == 'artist':
                # Add artist logic
                pass

            conn.commit()
        except Exception as e:
            conn.rollback()
            response = {'status': 'error', 'message': str(e)}
        finally:
            cursor.close()
            conn.close()
            return jsonify(response)

    return render_template('add.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    name_surname = request.form['nameSurname']
    sign_up_date = date.today()

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO User (UserUsername, UserEmail, UserPassword, UserSignUpDate, UserNameSurname) VALUES (%s, %s, %s, %s, %s)",
                       (username, email, password, sign_up_date, name_surname))
        conn.commit()
        response = {'status': 'success', 'message': 'User signed up successfully!'}
    except Exception as e:
        conn.rollback()
        response = {'status': 'error', 'message': str(e)}

    cursor.close()
    conn.close()
    return jsonify(response)

@app.route('/signin', methods=['POST'])
def signin():
    try:
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM User WHERE UserEmail = %s AND UserPassword = %s", (email, password))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session['user_id'] = user['UserId']
            response = {'status': 'success', 'message': 'User signed in successfully!', 'nameSurname': user['UserNameSurname']}
        else:
            response = {'status': 'error', 'message': 'Invalid email or password!'}
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}

    return jsonify(response)

@app.route('/signout', methods=['POST'])
def signout():
    session.pop('user_id', None)
    return jsonify({'status': 'success', 'message': 'User signed out successfully!'})

@app.route('/check_session')
def check_session():
    user_id = session.get('user_id')
    if user_id:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT UserNameSurname FROM User WHERE UserId = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify({'signed_in': True, 'nameSurname': user['UserNameSurname']})
    return jsonify({'signed_in': False})

@app.route('/add_to_playlist', methods=['POST'])
def add_to_playlist():
    data = request.get_json()
    song_id = data.get('songId')
    playlist_id = data.get('playlistId')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO PlaylistSong (PlaylistId, SongId) VALUES (%s, %s)", (playlist_id, song_id))
        conn.commit()
        return jsonify({'status': 'success', 'message': 'Song added to playlist successfully!'})
    except mysql.connector.Error as err:
        logging.error(f"Error adding song {song_id} to playlist {playlist_id}: {err}")
        return jsonify({'status': 'error', 'message': str(err)})
    finally:
        cursor.close()
        conn.close()

@app.route('/get_playlists', methods=['GET'])
def get_playlists():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'status': 'error', 'message': 'User not signed in'})

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT PlaylistId, PlaylistName FROM Playlist WHERE UserId = %s", (user_id,))
    playlists = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({'status': 'success', 'playlists': playlists})

@app.route('/remove_playlist', methods=['POST'])
def remove_playlist():
    data = request.get_json()
    playlist_id = data.get('playlistId')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Remove relations first
        cursor.execute("DELETE FROM PlaylistSong WHERE PlaylistId = %s", (playlist_id,))
        # Remove the playlist
        cursor.execute("DELETE FROM Playlist WHERE PlaylistId = %s", (playlist_id,))
        conn.commit()
        return jsonify({'status': 'success', 'message': 'Playlist removed successfully!'})
    except mysql.connector.Error as err:
        logging.error(f"Error removing playlist {playlist_id}: {err}")
        return jsonify({'status': 'error', 'message': str(err)})
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)