<section>
    <h1>Téléchargez et convertissez une vidéo YouTube en MP3</h1>

    <!-- Formulaire pour entrer l'URL -->
    <form action="index.php" method="post">
        <label for="url">URL de la vidéo ou de la playlist YouTube :</label><br>
        <input type="text" id="url" name="url" required><br><br>
        <input type="submit" value="Télécharger">
    </form>

    <?php
    // Vérifie si le formulaire a été soumis
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        // Récupère l'URL envoyée par le formulaire
        $url = escapeshellarg($_POST['url']);

        // Chemin vers le script Python
        $pythonScript = 'download_on_terminal.py'; // Assurez-vous que ce fichier est dans le même répertoire

        // Commande pour exécuter le script Python avec l'URL comme argument
        $command = "bash python3 $pythonScript $url";

        // Exécute la commande
        $output = shell_exec($command);

        // Affiche le résultat
        echo "<h2>Résultat de l'exécution :</h2><pre>$output</pre>";
    }
    ?>
</section>
