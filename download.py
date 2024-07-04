import os
import subprocess
import sys
import shutil
import requests
from zipfile import ZipFile
from io import BytesIO

def install_package(package_name):
    if not is_package_installed(package_name):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package_name])
            print(f"{package_name} a été installé avec succès")
        except subprocess.CalledProcessError as e:
            print(f"Échec de l'installation de {package_name}. Erreur : {e}")
            sys.exit(1)

def is_package_installed(package_name):
    try:
        subprocess.check_call([sys.executable, "-c", f"import {package_name}"])
        return True
    except (subprocess.CalledProcessError, ImportError):
        return False

def install_ffmpeg():
    # Vérifier si ffmpeg est déjà dans le PATH
    if shutil.which("ffmpeg") is None:
        try:
            # Vérifier si ffmpeg est dans /usr/local/bin/
            ffmpeg_path = "/usr/local/bin/ffmpeg"
            if not os.path.exists(ffmpeg_path):
                raise FileNotFoundError("ffmpeg n'est pas trouvé dans /usr/local/bin/. Veuillez l'installer manuellement.")

        except FileNotFoundError as e:
            print(f"Échec de l'installation de ffmpeg. Erreur : {e}")
            sys.exit(1)

def download_from_youtube(url, output_dir):
    # Vérifier et installer yt-dlp si ce n'est pas déjà fait
    install_package('yt_dlp')
    
    # Vérifier et installer ffmpeg si ce n'est pas déjà fait
    install_ffmpeg()

    # Créer le répertoire de sortie s'il n'existe pas
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Télécharger la vidéo ou la playlist en MP3
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

        # Supprimer les fichiers d'origine après conversion en MP3
        cleanup_after_conversion(output_dir)
        
    except subprocess.CalledProcessError as e:
        print(f"Échec du téléchargement depuis YouTube. Erreur : {e}")
        sys.exit(1)

def cleanup_after_conversion(directory):
    # Parcourir tous les fichiers dans le répertoire spécifié
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            # Supprimer les fichiers non-MP3 (fichiers d'origine après conversion)
            if not filename.lower().endswith('.mp3'):
                os.remove(filepath)
                print(f"Fichier {filename} supprimé après conversion.")

if __name__ == "__main__":
    url = input("Entrez l'URL de la playlist YouTube ou le lien de la vidéo : ")

    # Nom du répertoire de sortie
    repertoire_sortie = os.path.join(os.getcwd(), "musiques")

    print(f"Téléchargement et conversion dans le répertoire : {repertoire_sortie}")
    
    download_from_youtube(url, repertoire_sortie)
