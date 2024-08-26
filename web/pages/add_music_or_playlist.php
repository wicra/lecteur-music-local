<?php
$pidFile = '/var/www/html/download_playlist_yt/python_pid.txt';
$logFile = '/var/www/html/download_playlist_yt/log.txt';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $url = escapeshellarg($_POST['url']);
    $pythonScript = '/var/www/html/download_playlist_yt/script_download/download_on_terminal.py';

    // Exécuter le script Python en arrière-plan et obtenir le PID
    $command = "nohup python3 $pythonScript $url > $logFile 2>&1 & echo $!";
    $pid = shell_exec($command);

    // Enregistrer le PID dans un fichier pour référence future
    file_put_contents($pidFile, $pid);

    // Réponse AJAX, ne rien afficher ici directement
    exit;
}

// Traitement pour lire le contenu du fichier de log
if (isset($_GET['action']) && $_GET['action'] === 'read_log') {
    if (file_exists($logFile)) {
        // Lire le contenu du fichier de log
        $logContent = file_get_contents($logFile);
        echo htmlspecialchars($logContent); // Utiliser htmlspecialchars pour échapper les caractères spéciaux
    } else {
        echo "Le fichier de log n'existe pas encore ou est vide.";
    }
    exit; // Éviter que le reste de la page soit affiché
}

// Traitement pour nettoyer le fichier de log
if (isset($_GET['action']) && $_GET['action'] === 'cleanup_log') {
    if (file_exists($logFile)) {
        // Supprimer le fichier de log
        unlink($logFile);
    }
    exit; // Éviter que le reste de la page soit affiché
}

// Traitement pour arrêter le processus Python
if (isset($_GET['action']) && $_GET['action'] === 'stop_download') {
    if (file_exists($pidFile)) {
        $pid = file_get_contents($pidFile);
        // Tuer le processus Python
        shell_exec("kill $pid");
        // Supprimer le fichier PID
        unlink($pidFile);
        // Supprimer également le fichier de log
        if (file_exists($logFile)) {
            unlink($logFile);
        }
        echo "Le téléchargement a été annulé et les logs ont été supprimés.";
    } else {
        echo "Aucun processus de téléchargement en cours.";
    }
    exit;
}
?>
