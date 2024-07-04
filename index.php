<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Télécharger Playlist YouTube en MP3</title>
</head>
<body>
    <h2>Télécharger Playlist YouTube en MP3</h2>
    <form action="download.php" method="post">
        <label for="playlist_url">URL de la playlist YouTube :</label><br>
        <input type="text" id="playlist_url" name="playlist_url" required><br><br>
        
        <label for="output_dir">Répertoire de sortie :</label><br>
        <input type="text" id="output_dir" name="output_dir" required><br><br>
        
        <input type="submit" value="Télécharger">
    </form>
</body>
</html>
