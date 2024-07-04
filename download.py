import os
import subprocess
import sys
import shutil
import requests
from zipfile import ZipFile
from io import BytesIO
from datetime import datetime

def installer_paquet(package_name):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package_name])
        print(f"{package_name} a été installé avec succès")
    except subprocess.CalledProcessError as e:
        print(f"Échec de l'installation de {package_name}. Erreur : {e}")
        sys.exit(1)

def paquet_installe(package_name):
    try:
        subprocess.check_call([sys.executable, "-c", f"import {package_name}"])
        return True
    except subprocess.CalledProcessError:
        return False
    except ImportError:
        return False

def installer_ffmpeg():
    if shutil.which("ffmpeg") is None:
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

def telecharger_playlist(playlist_url, repertoire_sortie):
    # Vérifier et installer yt-dlp si ce n'est pas déjà fait
    if not paquet_installe('yt_dlp'):
        installer_paquet('yt_dlp')
    
    # Vérifier et installer ffmpeg si ce n'est pas déjà fait
    installer_ffmpeg()

    # Créer le répertoire de sortie s'il n'existe pas
    if not os.path.exists(repertoire_sortie):
        os.makedirs(repertoire_sortie)
    
    # Télécharger et convertir la playlist en MP3
    try:
        commande = [
            "yt-dlp",
            "--extract-audio",
            "--audio-format", "mp3",
            "--output", os.path.join(repertoire_sortie, "%(title)s.%(ext)s"),
            playlist_url
        ]
        subprocess.check_call(command)
    except subprocess.CalledProcessError as e:
        print(f"Échec du téléchargement de la playlist. Erreur : {e}")
        sys.exit(1)

    # Vérifier si des fichiers avec le même nom existent et sauter le téléchargement si c'est le cas
    fichiers_telecharges = os.listdir(repertoire_sortie)
    for nom_fichier in fichiers_telecharges:
        chemin_fichier = os.path.join(repertoire_sortie, nom_fichier)
        if os.path.isfile(chemin_fichier) and nom_fichier.endswith(".mp3"):
            print(f"{nom_fichier} existe déjà. Téléchargement ignoré.")

if __name__ == "__main__":
    playlist_url = input("Entrez l'URL de la playlist YouTube : ")

    # Nom du répertoire de sortie
    repertoire_sortie = os.path.join(os.getcwd(), "playlist")

    print(f"Téléchargement dans le répertoire : {repertoire_sortie}")
    
    telecharger_playlist(playlist_url, repertoire_sortie)
