<?php
if (isset($_POST['track'])) {
    $track = $_POST['track'];

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
    echo "No track specified.";
}
?>
