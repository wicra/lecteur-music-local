import os
import subprocess
import sys
import shutil
import argparse
import venv

def create_venv(venv_dir):
    """Crée un environnement virtuel dans le répertoire spécifié."""
    if not os.path.exists(venv_dir):
        print(f"Création de l'environnement virtuel dans {venv_dir}...")
        venv.create(venv_dir, with_pip=True)
    else:
        print(f"L'environnement virtuel existe déjà dans {venv_dir}.")

def install_package(venv_dir, package_name):
    """Assure que le package spécifié est installé dans l'environnement virtuel."""
    pip_path = os.path.join(venv_dir, 'bin', 'pip')
    
    if not is_package_installed(venv_dir, package_name):
        try:
            subprocess.check_call([pip_path, "install", "--upgrade", package_name])
            print(f"{package_name} a été installé avec succès.")
        except subprocess.CalledProcessError as e:
            print(f"Échec de l'installation de {package_name}. Erreur : {e}")
            sys.exit(1)
    else:
        print(f"{package_name} est déjà installé.")

def is_package_installed(venv_dir, package_name):
    """Vérifie si le package spécifié est installé dans l'environnement virtuel."""
    python_path = os.path.join(venv_dir, 'bin', 'python')
    try:
        subprocess.check_call([python_path, "-c", f"import {package_name}"])
        return True
    except subprocess.CalledProcessError:
        return False

def install_ffmpeg():
    """Assure que ffmpeg est installé et accessible dans le PATH."""
    if shutil.which("ffmpeg") is None:
        print("ffmpeg n'est pas installé. Tentative d'installation...")
        try:
            if sys.platform.startswith('linux'):
                # Pour les systèmes basés sur Debian/Ubuntu
                subprocess.check_call(['sudo', 'apt-get', 'update'])
                subprocess.check_call(['sudo', 'apt-get', 'install', '-y', 'ffmpeg'])
            elif sys.platform == 'darwin':
                # Pour macOS
                subprocess.check_call(['brew', 'install', 'ffmpeg'])
            elif sys.platform == 'win32':
                # Pour Windows
                print("Veuillez installer ffmpeg manuellement depuis https://ffmpeg.org/download.html")
            else:
                print("Système d'exploitation non pris en charge pour l'installation automatique de ffmpeg.")
                sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"Échec de l'installation de ffmpeg. Erreur : {e}")
            sys.exit(1)
    else:
        print("ffmpeg est déjà installé.")

def download_from_youtube(venv_dir, url, output_dir):
    """Télécharge une vidéo ou une playlist depuis YouTube et la convertit en MP3."""
    install_package(venv_dir, 'yt_dlp')
    install_ffmpeg()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    yt_dlp_path = os.path.join(venv_dir, 'bin', 'yt-dlp')
    command = [
        yt_dlp_path,
        "--extract-audio",
        "--audio-format", "mp3",
        "--max-filesize", "100M",  # Limite la taille des fichiers à télécharger (à ajuster si nécessaire)
        "--output", os.path.join(output_dir, "%(title)s.%(ext)s"),
        "--match-filter", "duration <= 360",  # Filtre pour ignorer les vidéos de plus de 6 minutes (360 secondes)
        url
    ]

    print(f"Command: {' '.join(command)}")
    
    try:
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

def cleanup_logs(venv_dir):
    """Supprime les logs et l'environnement virtuel."""
    shutil.rmtree(venv_dir, ignore_errors=True)
    print(f"Environnement virtuel {venv_dir} supprimé.")

def main():
    parser = argparse.ArgumentParser(description="Télécharge des vidéos ou des playlists depuis YouTube et les convertit en MP3.")
    parser.add_argument('url', type=str, help="L'URL de la vidéo ou de la playlist YouTube à télécharger.")
    args = parser.parse_args()
    
    venv_dir = '/var/www/html/download_playlist_yt/venv'
    repertoire_sortie = '/var/www/html/download_playlist_yt/playlist'
    
    try:
        create_venv(venv_dir)
        
        print(f"Téléchargement et conversion dans le répertoire : {repertoire_sortie}")
        download_from_youtube(venv_dir, args.url, repertoire_sortie)
        
    except Exception as e:
        print(f"Une erreur s'est produite: {e}")
    finally:
        cleanup_logs(venv_dir)

if __name__ == "__main__":
    main()
