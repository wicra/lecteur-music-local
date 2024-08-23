import os
import subprocess
import sys
import shutil

def uninstall_package(package_name):
    subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", package_name])

def uninstall_ffmpeg():
    if shutil.which("ffmpeg") is not None:
        if sys.platform.startswith("linux"):
            subprocess.check_call(["sudo", "apt", "remove", "-y", "ffmpeg"])
        elif sys.platform == "darwin":
            subprocess.check_call(["brew", "uninstall", "ffmpeg"])
        elif sys.platform == "win32":
            print("Please remove ffmpeg manually from your PATH and delete the ffmpeg folder.")

if __name__ == "__main__":
    # Uninstall yt-dlp
    uninstall_package('yt-dlp')
    
    # Uninstall ffmpeg
    uninstall_ffmpeg()

    print("Uninstallation completed.")
