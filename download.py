import os
import subprocess
import sys
import shutil
from datetime import datetime

def install_package(package_name):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package_name}. Error: {e}")
        sys.exit(1)

def install_ffmpeg():
    if shutil.which("ffmpeg") is None:
        try:
            if sys.platform.startswith("linux"):
                subprocess.check_call(["sudo", "apt", "install", "-y", "ffmpeg"])
            elif sys.platform == "darwin":
                subprocess.check_call(["brew", "install", "ffmpeg"])
            elif sys.platform == "win32":
                print("Please install ffmpeg manually from https://ffmpeg.org/download.html")
                sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"Failed to install ffmpeg. Error: {e}")
            sys.exit(1)

def download_playlist(playlist_url, output_dir):
    # Install yt-dlp
    install_package('yt-dlp')
    
    # Install ffmpeg
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
