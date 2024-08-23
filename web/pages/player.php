<?php
    // Dossier contenant les fichiers audio
    $dir = '../playlist/';
    $playlist = [];

    // Extensions de fichiers audio prises en charge
    $supported_file_types = array('mp3', 'wav', 'ogg');

    // Ouverture du dossier
    if ($handle = opendir($dir)) {
        // Lecture des fichiers du dossier
        while (false !== ($entry = readdir($handle))) {
            // Obtenez l'extension du fichier
            $file_extension = pathinfo($entry, PATHINFO_EXTENSION);

            // Vérifiez si le fichier est un fichier audio pris en charge
            if (in_array($file_extension, $supported_file_types)) {
                $playlist[] = $dir . $entry;
            }
        }
        closedir($handle);
    }
?>


<section>
    <div id="trackTitle">Chargement...</div>

    <audio id="audioPlayer" controls></audio>
    
    <div class="controls">
        <button onclick="previousTrack()">Précédent</button>
        <button onclick="nextTrack()">Suivant</button>
        <button onclick="toggleShuffle()">Aléatoire: <span id="shuffleStatus">Off</span></button>
        <button onclick="toggleRepeat()">Répéter: <span id="repeatStatus">Off</span></button>
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