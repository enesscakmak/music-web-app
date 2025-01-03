document.addEventListener('DOMContentLoaded', () => {
    const homeButton = document.getElementById('homeButton');
    const addButton = document.getElementById('addButton');
    const signUpButton = document.getElementById('signUpButton');
    const signInButton = document.getElementById('signInButton');
    const authModal = document.getElementById('authModal');
    const authTitle = document.getElementById('authTitle');
    const authForm = document.getElementById('authForm');
    const homeContent = document.getElementById('homeContent');
    const addContent = document.getElementById('addContent');
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
    const addForm = document.getElementById('addForm');
    let selectedSongId = null;

    if (addForm) {
        addForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(addForm);
            const data = {};
            formData.forEach((value, key) => {
                data[key] = value;
            });

            // Ensure data_type is included in the payload
            data['data_type'] = document.getElementById('dataType').value;

            fetch('/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert(data.message);
                    window.location.reload();
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });
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
            if (selectedSongId && playlistId) {
                fetch('/add_to_playlist', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ songId: parseInt(selectedSongId), playlistId: parseInt(playlistId) })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        alert('Song added to playlist successfully!');
                        window.location.reload();
                    } else {
                        alert('Error adding song to playlist: ' + data.message);
                    }
                    playlistModal.style.display = 'none';
                })
                .catch(error => console.error('Error:', error));
            } else {
                alert('Invalid song or playlist ID');
            }
        });
    });

    createNewPlaylistButton.addEventListener('click', () => {
        const playlistName = prompt('Enter new playlist name:');
        if (playlistName) {
            fetch('/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ data_type: 'playlist', playlistName: playlistName })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('Playlist created successfully!');
                    window.location.reload();
                } else {
                    alert('Error creating playlist: ' + data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        }
    });

    playlistList.addEventListener('click', (event) => {
        if (event.target.classList.contains('select-playlist-btn')) {
            const playlistId = event.target.getAttribute('data-playlist-id');
            if (selectedSongId && playlistId) {
                fetch('/add_to_playlist', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ songId: parseInt(selectedSongId), playlistId: parseInt(playlistId) })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        alert('Song added to playlist successfully!');
                        window.location.reload();
                    } else {
                        alert('Error adding song to playlist: ' + data.message);
                    }
                    playlistModal.style.display = 'none';
                })
                .catch(error => console.error('Error:', error));
            } else {
                alert('Invalid song or playlist ID');
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
                    playlistList.innerHTML = '';
                    data.playlists.forEach(playlist => {
                        const li = document.createElement('li');
                        const button = document.createElement('button');
                        button.className = 'select-playlist-btn';
                        button.setAttribute('data-playlist-id', playlist.PlaylistId);
                        button.textContent = playlist.PlaylistName;
                        button.addEventListener('click', () => {
                            const playlistId = button.getAttribute('data-playlist-id');
                            if (selectedSongId && playlistId) {
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
                                        window.location.reload();
                                    } else {
                                        alert('Error adding song to playlist: ' + data.message);
                                    }
                                    playlistModal.style.display = 'none';
                                })
                                .catch(error => console.error('Error:', error));
                            } else {
                                alert('Invalid song or playlist ID');
                            }
                        });
                        li.appendChild(button);
                        playlistList.appendChild(li);
                    });
                } else {
                    alert('Error fetching playlists: ' + data.message);
                }
            })
            .catch(error => console.error('Error:', error));
    }

    homeButton.addEventListener('click', () => {
        window.location.href = '/';
    });

    addButton.addEventListener('click', () => {
        window.location.href = '/add';
    });

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

        fetch(action, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert(data.message);
                authModal.style.display = 'none';
                authButtons.style.display = 'none';
                userContainer.style.display = 'flex';
                userInfo.textContent = data.nameSurname;
                window.location.reload();
            } else {
                alert(data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    });

    signOutButton.addEventListener('click', () => {
        fetch('/signout', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert(data.message);
                authButtons.style.display = 'flex';
                userContainer.style.display = 'none';
                userInfo.textContent = '';
                window.location.reload();
            } else {
                alert(data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    });

    // Check if user is already signed in
    fetch('/check_session')
    .then(response => response.json())
    .then(data => {
        if (data.signed_in) {
            authButtons.style.display = 'none';
            userContainer.style.display = 'flex';
            userInfo.textContent = data.nameSurname;
        } else {
            authButtons.style.display = 'flex';
            userContainer.style.display = 'none';
        }
    })
    .catch(error => console.error('Error:', error));

    removePlaylistButtons.forEach(button => {
        button.addEventListener('click', () => {
            const playlistId = button.getAttribute('data-playlist-id');
            if (confirm('Are you sure you want to delete this playlist?')) {
                fetch('/remove_playlist', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ playlistId: parseInt(playlistId) })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        alert('Playlist removed successfully!');
                        button.parentElement.remove();
                        window.location.reload();
                    } else {
                        alert('Error removing playlist: ' + data.message);
                    }
                })
                .catch(error => console.error('Error:', error));
            }
        });
    });
});