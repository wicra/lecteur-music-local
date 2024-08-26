#!/bin/bash

sudo apt update
sudo apt upgrade -y

# install web server
sudo apt install -y apache2
sudo apt install php -y

sudo chown -R www-data:www-data /var/www/html/download_playlist_yt/
sudo chmod 755 /var/www/html/download_playlist_yt/script_download/download_on_terminal.py

