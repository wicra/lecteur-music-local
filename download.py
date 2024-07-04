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
    # Vérifier si ffmpeg est déjà dans le PATH ou dans le répertoire local
    ffmpeg_dir = os.path.join(os.path.dirname(__file__), "ffmpeg")
    
    if os.path.exists(ffmpeg_dir):
        print("ffmpeg est déjà présent dans le répertoire local.")
    else:
        try:
            # Télécharger et extraire ffmpeg dans le répertoire local
            print("Téléchargement et installation de ffmpeg pour Windows...")
            ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
            response = requests.get(ffmpeg_url)
            with ZipFile(BytesIO(response.content)) as zip_ref:
                zip_ref.extractall(ffmpeg_dir)
            
            # Ajouter le chemin de ffmpeg au PATH s'il n'y est pas déjà
            if ffmpeg_dir not in os.environ["PATH"]:
                os.environ["PATH"] += os.pathsep + os.path.abspath(ffmpeg_dir)
                
        except Exception as e:
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
        
        print("Téléchargement terminé.")

        # Convertir tous les fichiers audio téléchargés en MP3
        convert_to_mp3(output_dir)
    except subprocess.CalledProcessError as e:
        print(f"Échec du téléchargement depuis YouTube. Erreur : {e}")
        sys.exit(1)

def convert_to_mp3(directory):
    # Parcourir tous les fichiers dans le répertoire spécifié
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            # Vérifier si c'est un fichier audio
            if any(filename.lower().endswith(ext) for ext in ['.mp3', '.aac', '.wav', '.flac', '.ogg', '.webm']):
                # Vérifier si le fichier est déjà au format MP3
                if filename.lower().endswith('.mp3'):
                    print(f"{filename} est déjà au format MP3.")
                    continue
                
                try:
                    output_filename = os.path.splitext(filename)[0] + ".mp3"
                    subprocess.check_call(["ffmpeg", "-i", filepath, os.path.join(directory, output_filename)])
                    os.remove(filepath)  # Supprimer le fichier original après conversion
                    print(f"Converti {filename} en MP3 avec succès.")
                except subprocess.CalledProcessError as e:
                    print(f"Échec de la conversion de {filename} en MP3. Erreur : {e}")

if __name__ == "__main__":
    url = input("Entrez l'URL de la playlist YouTube ou le lien de la vidéo : ")

    # Nom du répertoire de sortie
    repertoire_sortie = os.path.join(os.getcwd(), "musiques")

    print(f"Téléchargement dans le répertoire : {repertoire_sortie}")
    
    download_from_youtube(url, repertoire_sortie)
