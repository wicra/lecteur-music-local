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
        print(f"Successfully installed {package_name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package_name}. Error: {e}")
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
    if shutil.which("ffmpeg") is None:
        try:
            if sys.platform.startswith("linux"):
                subprocess.check_call(["sudo", "apt", "install", "-y", "ffmpeg"])
            elif sys.platform == "darwin":
                subprocess.check_call(["brew", "install", "ffmpeg"])
            elif sys.platform == "win32":
                print("Downloading and installing ffmpeg for Windows...")
                ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
                response = requests.get(ffmpeg_url)
                with ZipFile(BytesIO(response.content)) as zip_ref:
                    zip_ref.extractall("ffmpeg")
                
                ffmpeg_bin_path = os.path.join("ffmpeg", "ffmpeg-*-essentials_build", "bin")
                os.environ["PATH"] += os.pathsep + os.path.abspath(ffmpeg_bin_path)
        except subprocess.CalledProcessError as e:
            print(f"Failed to install ffmpeg. Error: {e}")
            sys.exit(1)

def download_playlist(playlist_url, output_dir):
    # Check and install yt-dlp if not already installed
    if not is_package_installed('yt_dlp'):
        install_package('yt_dlp')
    
    # Check and install ffmpeg if not already installed
    install_ffmpeg()

    # Create the output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Download and convert the playlist
    try:
        command = [
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "-o", os.path.join(output_dir, "%(title)s.%(ext)s"),
            playlist_url
        ]
        subprocess.check_call(command)
    except subprocess.CalledProcessError as e:
        print(f"Failed to download playlist. Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    playlist_url = input("Enter the YouTube playlist URL: ")

    # Get current date and format it
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Set output directory name
    output_dir = os.path.join(os.getcwd(), f"playlist_{current_date}")

    print(f"Downloading to directory: {output_dir}")
    
    download_playlist(playlist_url, output_dir)
