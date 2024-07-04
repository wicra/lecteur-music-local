import os
import subprocess
import sys
import shutil

def install_package(package_name):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

def install_ffmpeg():
    if shutil.which("ffmpeg") is None:
        if sys.platform.startswith("linux"):
            subprocess.check_call(["sudo", "apt", "install", "-y", "ffmpeg"])
        elif sys.platform == "darwin":
            subprocess.check_call(["brew", "install", "ffmpeg"])
        elif sys.platform == "win32":
            # On Windows, provide instructions for manual installation
            print("Please install ffmpeg manually from https://ffmpeg.org/download.html")
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
    command = [
        "yt-dlp",
        "-x",
        "--audio-format", "mp3",
        "-o", os.path.join(output_dir, "%(title)s.%(ext)s"),
        playlist_url
    ]
    subprocess.check_call(command)

if __name__ == "__main__":
    playlist_url = input("Enter the YouTube playlist URL: ")
    output_dir = input("Enter the directory where you want to save the MP3 files: ")
    download_playlist(playlist_url, output_dir)
