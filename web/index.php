<!DOCTYPE html>
<html lang="en">
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">

        <title>Music Player</title>

        <!-- ICON -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">

        <!-- FONT -->
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&family=Montserrat:wght@400;700&display=swap" rel="stylesheet">

        <!-- STYLES -->
        <link rel="stylesheet" href="styles/styles.css">

        <!-- FAVICON -->
        <link rel="icon" href="assets/images/favicon.svg" type="image/svg+xml">
    </head>

    <body>
        <!-- INDEX PAGE -->
        <h1>Music Player</h1>

        <!-- SEARCH SECTION -->
        <section class="search-section">
            <div class="search-bar">
                <input type="text" id="searchInput" placeholder="Search tracks..." oninput="searchTracks()">
            </div>
            <ul id="searchResults"></ul>
        </section>

        <!-- PLAYER PAGE -->
        <?php include("pages/player.php"); ?>
        
        <section>
            <div id="trackTitle">Loading...</div>
            <div id="trackInfo">0 / 0</div>

            <audio id="audioPlayer" controls></audio>

            <div class="controls">
                <button onclick="previousTrack()"><i class="fas fa-backward"></i> </button>
                <button onclick="nextTrack()"><i class="fas fa-forward"></i> </button>
                <button onclick="toggleShuffle()"><i class="fas fa-random"></i>  <span id="shuffleStatus">Off</span></button>
                <button onclick="toggleRepeat()"><i class="fas fa-redo"></i>  <span id="repeatStatus">Off</span></button>
                <button onclick="deleteCurrentTrack()"><i class="fas fa-trash"></i> </button> <!-- Nouveau bouton de suppression -->
            </div>

            <script>
                var playlist = <?php echo json_encode($playlist); ?>;
                var currentTrack = 0;
                var isShuffle = false;
                var isRepeat = false;
                var audioPlayer = document.getElementById('audioPlayer');
                var trackTitle = document.getElementById('trackTitle');
                var trackInfo = document.getElementById('trackInfo');

                function getTrackName(filePath) {
                    return filePath.split('/').pop().split('.').shift();
                }

                function updateTrackInfo() {
                    trackInfo.innerText = (currentTrack + 1) + ' / ' + playlist.length;
                }

                function loadTrack(index) {
                    currentTrack = index;
                    if (playlist.length > 0) {
                        audioPlayer.src = playlist[currentTrack];
                        trackTitle.innerText = getTrackName(playlist[currentTrack]);
                        audioPlayer.play();
                        updateTrackInfo();
                    } else {
                        trackTitle.innerText = "No tracks available";
                        trackInfo.innerText = "0 / 0";
                        audioPlayer.src = "";
                    }
                }

                function nextTrack() {
                    if (isShuffle) {
                        currentTrack = Math.floor(Math.random() * playlist.length);
                    } else {
                        currentTrack = (currentTrack + 1) % playlist.length;
                    }
                    loadTrack(currentTrack);
                }

                function previousTrack() {
                    currentTrack = (currentTrack - 1 + playlist.length) % playlist.length;
                    loadTrack(currentTrack);
                }

                function toggleShuffle() {
                    isShuffle = !isShuffle;
                    document.getElementById('shuffleStatus').innerText = isShuffle ? 'On' : 'Off';
                }

                function toggleRepeat() {
                    isRepeat = !isRepeat;
                    document.getElementById('repeatStatus').innerText = isRepeat ? 'On' : 'Off';
                    audioPlayer.loop = isRepeat;
                }

                function searchTracks() {
                    var searchInput = document.getElementById('searchInput').value.toLowerCase();
                    var searchResults = document.getElementById('searchResults');
                    searchResults.innerHTML = '';

                    if (searchInput) {
                        var results = playlist.filter(function(track) {
                            return getTrackName(track).toLowerCase().includes(searchInput);
                        }).slice(0, 5); // Limit results to 5

                        results.forEach(function(track) {
                            var li = document.createElement('li');
                            li.textContent = getTrackName(track);
                            li.onclick = function() {
                                handleSuggestionClick(track);
                            };
                            searchResults.appendChild(li);
                        });
                    }
                }

                function handleSuggestionClick(track) {
                    // Load the selected track
                    loadTrack(playlist.indexOf(track));
                    
                    // Clear the search input
                    document.getElementById('searchInput').value = '';
                    
                    // Clear the search results
                    document.getElementById('searchResults').innerHTML = '';
                }

                function deleteCurrentTrack() {
                    if (playlist.length > 0) {
                        var trackName = getTrackName(playlist[currentTrack]);
                        var confirmation = confirm("Are you sure you want to delete the current track: " + trackName + "?");

                        if (confirmation) {
                            var password = prompt("Please enter the password to confirm deletion:");
                            if (password !== null && password !== "") {
                                var trackToDelete = playlist[currentTrack];

                                // Requête AJAX pour supprimer le fichier du serveur avec le mot de passe
                                var xhr = new XMLHttpRequest();
                                xhr.open('POST', 'pages/delete_track.php', true);
                                xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                                xhr.onreadystatechange = function() {
                                    if (xhr.readyState === 4 && xhr.status === 200) {
                                        var response = xhr.responseText;
                                        if (response.trim() === "Track deleted successfully.") {
                                            // Retirer la piste de la playlist
                                            playlist.splice(currentTrack, 1);
                                            if (currentTrack >= playlist.length) {
                                                currentTrack = 0;
                                            }
                                            loadTrack(currentTrack);
                                        } else {
                                            alert(response);
                                        }
                                    }
                                };
                                xhr.send('track=' + encodeURIComponent(trackToDelete) + '&password=' + encodeURIComponent(password));
                            }
                        }
                    }
                }

                loadTrack(currentTrack);

                audioPlayer.addEventListener('ended', function() {
                    if (!isRepeat) {
                        nextTrack();
                    }
                });
            </script>
        </section>


        <!-- ADD PLAYLIST PAGE -->
        <section>
            <form id="download-form">
                <label for="url">YouTube Video or Playlist URL:</label>
                <input type="text" id="url" name="url" placeholder="Enter URL" required>
                <input type="submit" value="Download">
            </form>

            <h3>Execution Results:</h3>
            <div id="log-content">Loading results...</div>
        </section>

        <script>
            document.getElementById('download-form').addEventListener('submit', function(event) {
                event.preventDefault();
                var formData = new FormData(this);
                var xhr = new XMLHttpRequest();
                xhr.open('POST', 'pages/add_music_or_playlist.php', true);
                xhr.onreadystatechange = function() {
                    if (xhr.readyState === 4 && xhr.status === 200) {
                        refreshLog();
                    }
                };
                xhr.send(formData);
            });

            function refreshLog() {
                var xhr = new XMLHttpRequest();
                xhr.open('GET', 'pages/add_music_or_playlist.php?action=read_log', true);
                xhr.onreadystatechange = function() {
                    if (xhr.readyState === 4 && xhr.status === 200) {
                        var logContent = xhr.responseText;
                        logContent = logContent.replace(/<[^>]*>/g, '');
                        if (logContent.includes('Téléchargement et conversion en MP3 terminés.')) {
                            document.getElementById('log-content').innerText = 'Download complete. Log file will be deleted.';
                            var cleanupRequest = new XMLHttpRequest();
                            cleanupRequest.open('GET', 'pages/add_music_or_playlist.php?action=cleanup_log', true);
                            cleanupRequest.send();
                        } else {
                            document.getElementById('log-content').innerText = logContent;
                        }
                    }
                };
                xhr.send();
            }

            setInterval(refreshLog, 5000);
            window.onload = refreshLog;
        </script>

    </body>
</html>
