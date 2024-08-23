#!/bin/bash

sudo apt update
sudo apt upgrade -y

# install web server
sudo apt install -y apache2
sudo apt install php -y

sudo chown -R www-data:www-data /var/www/html/download_playlist_yt/
sudo chown -R www-data:www-data /var/www/html/download_playlist_yt/web/pages/add_music_or_playlist.php
sudo chmod -R 755 /var/www/html/download_playlist_yt/
