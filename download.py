import os
import subprocess
import sys
import shutil
import requests
from zipfile import ZipFile
from io import BytesIO
from datetime import datetime

def install_package(package_name):
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
    except subprocess.CalledProcessError:
        return False
    except ImportError:
        return False

def install_ffmpeg():
    if not shutil.which("ffmpeg"):
        try:
            if sys.platform.startswith("linux"):
                subprocess.check_call(["sudo", "apt", "install", "-y", "ffmpeg"])
            elif sys.platform == "darwin":
                subprocess.check_call(["brew", "install", "ffmpeg"])
            elif sys.platform == "win32":
                print("Téléchargement et installation de ffmpeg pour Windows...")
                ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
                response = requests.get(ffmpeg_url)
                with ZipFile(BytesIO(response.content)) as zip_ref:
                    zip_ref.extractall("ffmpeg")
                
                ffmpeg_bin_path = os.path.join("ffmpeg", "ffmpeg-*-essentials_build", "bin")
                os.environ["PATH"] += os.pathsep + os.path.abspath(ffmpeg_bin_path)
        except subprocess.CalledProcessError as e:
            print(f"Échec de l'installation de ffmpeg. Erreur : {e}")
            sys.exit(1)

def download_playlist(playlist_url, output_dir):
    # Vérifier et installer yt-dlp si ce n'est pas déjà fait
    if not is_package_installed('yt_dlp'):
        install_package('yt_dlp')
    
    # Vérifier et installer ffmpeg si ce n'est pas déjà fait
    install_ffmpeg()

    # Créer le répertoire de sortie s'il n'existe pas
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Télécharger la playlist en MP3
    try:
        command = [
            "yt-dlp",
            "--extract-audio",
            "--audio-format", "mp3",
            "--output", os.path.join(output_dir, "%(title)s.%(ext)s"),
            playlist_url
        ]
        subprocess.check_call(command)
    except subprocess.CalledProcessError as e:
        print(f"Échec du téléchargement de la playlist. Erreur : {e}")
        sys.exit(1)

    # Supprimer tous les fichiers non MP3 téléchargés
    fichiers_telecharges = os.listdir(output_dir)
    for nom_fichier in fichiers_telecharges:
        chemin_fichier = os.path.join(output_dir, nom_fichier)
        if os.path.isfile(chemin_fichier) and not nom_fichier.endswith(".mp3"):
            os.remove(chemin_fichier)
            print(f"Suppression du fichier {nom_fichier} (format non MP3)")

if __name__ == "__main__":
    playlist_url = input("Entrez l'URL de la playlist YouTube : ")

    # Nom du répertoire de sortie
    repertoire_sortie = os.path.join(os.getcwd(), "playlist")

    print(f"Téléchargement dans le répertoire : {repertoire_sortie}")
    
    download_playlist(playlist_url, repertoire_sortie)
