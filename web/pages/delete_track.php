<?php
    if (isset($_POST['track']) && isset($_POST['password'])) {
        $track = $_POST['track'];
        $password = $_POST['password'];

        // Lire le mot de passe depuis le fichier
        $passwordFile = '../secret/word.env.php'; // Mettez à jour ce chemin avec le chemin correct
        $storedPassword = trim(file_get_contents($passwordFile));

        // Vérifier le mot de passe
        if ($password === $storedPassword) {
            // Assurez-vous que le chemin est correct et sécurisé
            $filePath = '/var/www/html/download_playlist_yt/playlist/' . $track;

            if (file_exists($filePath)) {
                if (unlink($filePath)) {
                    echo "Track deleted successfully.";
                } else {
                    echo "Failed to delete the track.";
                }
            } else {
                echo "Track not found.";
            }
        } else {
            echo "Incorrect password.";
        }
    } else {
        echo "No track or password specified.";
    }
?>
