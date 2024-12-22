document.addEventListener('DOMContentLoaded', () => {
    const signUpButton = document.getElementById('signUpButton');
    const signInButton = document.getElementById('signInButton');
    const authModal = document.getElementById('authModal');
    const authTitle = document.getElementById('authTitle');
    const authForm = document.getElementById('authForm');
    const closeAuthModal = document.getElementById('closeAuthModal');
    const signUpFields = document.getElementById('signUpFields');
    const authButtons = document.querySelector('.auth-buttons');
    const userContainer = document.getElementById('userContainer');
    const userInfo = document.getElementById('userInfo');
    const signOutButton = document.getElementById('signOutButton');
    const addToPlaylistButtons = document.querySelectorAll('.add-to-playlist-btn');
    const playlistModal = document.getElementById('playlistModal');
    const closePlaylistModal = document.getElementById('closePlaylistModal');
    const selectPlaylistButtons = document.querySelectorAll('.select-playlist-btn');
    const createNewPlaylistButton = document.getElementById('createNewPlaylist');
    const playlistList = document.getElementById('playlistList');
    const removePlaylistButtons = document.querySelectorAll('.remove-playlist-btn');
    let selectedSongId = null;

    function validateInput(input, type, maxLength) {
        if (input.length > maxLength) {
            return false;
        }
        if (type === 'int' && isNaN(parseInt(input))) {
            return false;
        }
        if (type === 'date' && isNaN(Date.parse(input))) {
            return false;
        }
        return true;
    }

    addToPlaylistButtons.forEach(button => {
        button.addEventListener('click', () => {
            selectedSongId = button.getAttribute('data-song-id');
            playlistModal.style.display = 'flex';
        });
    });

    closePlaylistModal.addEventListener('click', () => {
        playlistModal.style.display = 'none';
    });

    selectPlaylistButtons.forEach(button => {
        button.addEventListener('click', () => {
            const playlistId = button.getAttribute('data-playlist-id');
            if (validateInput(playlistId, 'int', 11)) {
                fetch('/add_to_playlist', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ songId: selectedSongId, playlistId: playlistId })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        alert('Song added to playlist successfully!');
                        playlistModal.style.display = 'none';
                    } else {
                        alert('Error adding song to playlist: ' + data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while adding the song to the playlist.');
                });
            } else {
                alert('Invalid playlist ID');
            }
        });
    });

    createNewPlaylistButton.addEventListener('click', () => {
        const playlistName = prompt('Enter new playlist name:');
        if (validateInput(playlistName, 'string', 150)) {
            fetch('/create_playlist', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ playlistName: playlistName })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('Playlist created successfully!');
                    refreshPlaylistList();
                } else {
                    alert('Error creating playlist: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while creating the playlist.');
            });
        } else {
            alert('Invalid playlist name');
        }
    });

    playlistList.addEventListener('click', (event) => {
        if (event.target.classList.contains('select-playlist-btn')) {
            const playlistId = event.target.getAttribute('data-playlist-id');
            if (validateInput(playlistId, 'int', 11)) {
                fetch('/add_to_playlist', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ songId: selectedSongId, playlistId: playlistId })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        alert('Song added to playlist successfully!');
                        playlistModal.style.display = 'none';
                    } else {
                        alert('Error adding song to playlist: ' + data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while adding the song to the playlist.');
                });
            } else {
                alert('Invalid playlist ID');
            }
        }
    });

    document.getElementById('closePlaylistModal').addEventListener('click', () => {
        playlistModal.style.display = 'none';
    });

    function refreshPlaylistList() {
        fetch('/get_playlists')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const playlistList = document.getElementById('playlistList');
                    playlistList.innerHTML = '';
                    data.playlists.forEach(playlist => {
                        const li = document.createElement('li');
                        li.innerHTML = `<button class="select-playlist-btn" data-playlist-id="${playlist.PlaylistId}">${playlist.PlaylistName}</button>`;
                        playlistList.appendChild(li);
                    });
                } else {
                    alert('Error fetching playlists: ' + data.message);
                }
            })
            .catch(error => console.error('Error:', error));
    }

    signUpButton.addEventListener('click', () => {
        authTitle.textContent = 'Sign Up';
        signUpFields.style.display = 'block';
        authModal.style.display = 'flex';
    });

    signInButton.addEventListener('click', () => {
        authTitle.textContent = 'Sign In';
        signUpFields.style.display = 'none';
        authModal.style.display = 'flex';
    });

    closeAuthModal.addEventListener('click', () => {
        authModal.style.display = 'none';
    });

    authForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const formData = new FormData(authForm);
        const action = authTitle.textContent === 'Sign In' ? '/signin' : '/signup';
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        if (validateInput(data.username, 'string', 100) &&
            validateInput(data.email, 'string', 150) &&
            validateInput(data.password, 'string', 255) &&
            validateInput(data.nameSurname, 'string', 100)) {
            fetch(action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('Authentication successful!');
                    authModal.style.display = 'none';
                    if (action === '/signin') {
                        userInfo.textContent = data.nameSurname;
                        userContainer.style.display = 'flex';
                        authButtons.style.display = 'none';
                    }
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        } else {
            alert('Invalid input data');
        }
    });

    signOutButton.addEventListener('click', () => {
        fetch('/signout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Signed out successfully!');
                userContainer.style.display = 'none';
                authButtons.style.display = 'flex';
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    });

    // Check if user is already signed in
    fetch('/check_session')
    .then(response => response.json())
    .then(data => {
        if (data.signed_in) {
            userInfo.textContent = data.nameSurname;
            userContainer.style.display = 'flex';
            authButtons.style.display = 'none';
        }
    })
    .catch(error => console.error('Error:', error));

    removePlaylistButtons.forEach(button => {
        button.addEventListener('click', () => {
            const playlistId = button.getAttribute('data-playlist-id');
            if (validateInput(playlistId, 'int', 11)) {
                if (confirm('Are you sure you want to delete this playlist?')) {
                    fetch('/remove_playlist', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ playlistId: playlistId })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'success') {
                            alert('Playlist removed successfully!');
                            refreshPlaylistList();
                        } else {
                            alert('Error removing playlist: ' + data.message);
                        }
                    })
                    .catch(error => console.error('Error:', error));
                }
            } else {
                alert('Invalid playlist ID');
            }
        });
    });
});