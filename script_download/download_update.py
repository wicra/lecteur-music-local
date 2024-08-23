import os
import subprocess
import sys
import shutil

def install_package(package_name):
    """Assure que le package spécifié est installé."""
    if not is_package_installed(package_name):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package_name])
            print(f"{package_name} a été installé avec succès")
        except subprocess.CalledProcessError as e:
            print(f"Échec de l'installation de {package_name}. Erreur : {e}")
            sys.exit(1)

def is_package_installed(package_name):
    """Vérifie si le package spécifié est installé en essayant de l'importer."""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def install_ffmpeg():
    """Assure que ffmpeg est installé et accessible dans le PATH."""
    if shutil.which("ffmpeg") is None:
        print("ffmpeg n'est pas installé ou introuvable dans le PATH. Veuillez l'installer.")
        sys.exit(1)

def download_from_youtube(url, output_dir):
    """Télécharge une vidéo ou une playlist depuis YouTube et la convertit en MP3."""
    install_package('yt_dlp')
    install_ffmpeg()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        command = [
            "yt-dlp",
            "--extract-audio",
            "--audio-format", "mp3",
            "--output", os.path.join(output_dir, "%(title)s.%(ext)s"),
            url
        ]
        subprocess.check_call(command)
        print("Téléchargement et conversion en MP3 terminés.")
        cleanup_after_conversion(output_dir)
    except subprocess.CalledProcessError as e:
        print(f"Échec du téléchargement depuis YouTube. Erreur : {e}")
        sys.exit(1)

def cleanup_after_conversion(directory):
    """Supprime les fichiers non-MP3 dans le répertoire spécifié."""
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and not filename.lower().endswith('.mp3'):
            os.remove(filepath)
            print(f"Fichier {filename} supprimé après conversion.")

if __name__ == "__main__":
    url = input("Entrez l'URL de la playlist YouTube ou le lien de la vidéo : ")
    repertoire_sortie = os.path.join(os.getcwd(), "playlist")
    print(f"Téléchargement et conversion dans le répertoire : {repertoire_sortie}")
    download_from_youtube(url, repertoire_sortie)
