<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Music Player</title>

    <!-- ICON -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">

    <!-- FONT -->
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600&display=swap" rel="stylesheet">

    <!-- STYLES -->
    <link rel="stylesheet" href="styles/styles.css">
</head>

<body>
    <!-- INDEX PAGE -->
    <h1>Music Player</h1>

    <!-- PLAYER PAGE -->
    <?php include("pages/player.php"); ?>
    
    <section>
        <div id="trackTitle">Loading...</div>

        <audio id="audioPlayer" controls></audio>

        <div class="controls">
            <button onclick="previousTrack()"><i class="fas fa-backward"></i> Previous</button>
            <button onclick="nextTrack()"><i class="fas fa-forward"></i> Next</button>
            <button onclick="toggleShuffle()"><i class="fas fa-random"></i> Shuffle: <span id="shuffleStatus">Off</span></button>
            <button onclick="toggleRepeat()"><i class="fas fa-redo"></i> Repeat: <span id="repeatStatus">Off</span></button>
        </div>


        <script>
            var playlist = <?php echo json_encode($playlist); ?>;
            var currentTrack = 0;
            var isShuffle = false;
            var isRepeat = false;
            var audioPlayer = document.getElementById('audioPlayer');
            var trackTitle = document.getElementById('trackTitle');

            // Fonction pour extraire le nom de la piste sans le chemin ni l'extension
            function getTrackName(filePath) {
                return filePath.split('/').pop().split('.').shift();
            }

            // Fonction pour charger et jouer une piste
            function loadTrack(index) {
                currentTrack = index;
                audioPlayer.src = playlist[currentTrack];
                trackTitle.innerText = getTrackName(playlist[currentTrack]); // Met à jour le titre
                audioPlayer.play();
            }

            // Fonction pour jouer la piste suivante
            function nextTrack() {
                if (isShuffle) {
                    currentTrack = Math.floor(Math.random() * playlist.length);
                } else {
                    currentTrack = (currentTrack + 1) % playlist.length;
                }
                loadTrack(currentTrack);
            }

            // Fonction pour jouer la piste précédente
            function previousTrack() {
                currentTrack = (currentTrack - 1 + playlist.length) % playlist.length;
                loadTrack(currentTrack);
            }

            // Fonction pour activer/désactiver le mode aléatoire
            function toggleShuffle() {
                isShuffle = !isShuffle;
                document.getElementById('shuffleStatus').innerText = isShuffle ? 'On' : 'Off';
            }

            // Fonction pour activer/désactiver le mode répétition
            function toggleRepeat() {
                isRepeat = !isRepeat;
                document.getElementById('repeatStatus').innerText = isRepeat ? 'On' : 'Off';
                audioPlayer.loop = isRepeat;
            }

            // Chargement de la première piste
            loadTrack(currentTrack);

            // Passage à la piste suivante lorsque la piste actuelle est terminée
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
