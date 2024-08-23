<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $url = escapeshellarg($_POST['url']);
    $pythonScript = '/var/www/html/download_playlist_yt/script_download/download_on_terminal.py';
    $logFile = '/var/www/html/download_playlist_yt/log.txt';

    // Exécuter le script Python en arrière-plan
    $command = "nohup python3 $pythonScript $url > $logFile 2>&1 &";
    shell_exec($command);

    // Réponse AJAX, ne rien afficher ici directement
    exit;
}

// Traitement pour lire le contenu du fichier de log
if (isset($_GET['action']) && $_GET['action'] === 'read_log') {
    $logFile = '/var/www/html/download_playlist_yt/log.txt';
    if (file_exists($logFile)) {
        // Lire le contenu du fichier de log
        $logContent = file_get_contents($logFile);
        echo htmlspecialchars($logContent); // Utiliser htmlspecialchars pour échapper les caractères spéciaux
    } else {
        echo "Le fichier de log n'existe pas encore.";
    }
    exit; // Éviter que le reste de la page soit affiché
}

// Traitement pour nettoyer le fichier de log
if (isset($_GET['action']) && $_GET['action'] === 'cleanup_log') {
    $logFile = '/var/www/html/download_playlist_yt/log.txt';
    if (file_exists($logFile)) {
        // Supprimer le fichier de log
        unlink($logFile);
    }
    exit; // Éviter que le reste de la page soit affiché
}
?>
