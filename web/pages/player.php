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
