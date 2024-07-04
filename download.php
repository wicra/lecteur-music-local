<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Récupérer l'URL de la playlist et le répertoire de sortie
    $playlist_url = $_POST['playlist_url'];
    $output_dir = $_POST['output_dir'];

    // Vérifier et créer le dossier de sortie s'il n'existe pas
    if (!file_exists($output_dir)) {
        mkdir($output_dir, 0777, true);
    }

    // Fonction pour télécharger la playlist et convertir en MP3
    function downloadPlaylist($playlist_url, $output_dir) {
        // Télécharger la playlist en utilisant youtube-dl
        $command = "youtube-dl --extract-audio --audio-format mp3 --output '{$output_dir}/%(title)s.%(ext)s' '{$playlist_url}'";
        exec($command, $output, $return_code);
        
        if ($return_code !== 0) {
            die("Erreur lors du téléchargement de la playlist.");
        }
    }

    // Appeler la fonction pour télécharger la playlist
    downloadPlaylist($playlist_url, $output_dir);

    // Créer un fichier zip des MP3
    $zipfile = $output_dir . '/playlist.zip';
    $files = glob($output_dir . '/*.mp3');
    $zip = new ZipArchive();
    if ($zip->open($zipfile, ZipArchive::CREATE) === TRUE) {
        foreach ($files as $file) {
            $zip->addFile($file, basename($file));
        }
        $zip->close();
    } else {
        die("Erreur lors de la création du fichier zip.");
    }

    // Télécharger le fichier zip généré
    header('Content-Type: application/zip');
    header("Content-Disposition: attachment; filename='playlist.zip'");
    header('Content-Length: ' . filesize($zipfile));
    readfile($zipfile);

    // Supprimer le fichier zip après le téléchargement
    unlink($zipfile);
}
?>
