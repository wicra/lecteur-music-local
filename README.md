# Lecteur de Musique Local

## Description

Ce projet permet de créer un lecteur de musique local sur un PC sous Debian. Il vous offre une interface web pour lire et contrôler des playlists audio directement depuis votre navigateur. Vous pouvez ajouter des morceaux ou des playlists depuis YouTube, gérer la lecture, annuler des téléchargements en cours, et plus encore. Le tout est présenté dans une interface utilisateur simple et pratique.

## Fonctionnalités

- **Lecture de Playlist Audio** : Écoutez vos morceaux préférés à partir d'une playlist audio locale.
- **Contrôles Audio** : Lecture, pause, saut de piste, lecture en boucle, lecture aléatoire.
- **Intégration YouTube** : Ajoutez des morceaux ou des playlists YouTube en fournissant simplement un lien. Le téléchargement est géré automatiquement par un script Python.
- **Annulation de Téléchargements** : Possibilité d'annuler les téléchargements de playlists ou de morceaux en cours.
- **Gestion des Logs** : Affichage et suppression des logs directement depuis l'interface web.
- **Gestion des Playlists** : Supprimez des morceaux que vous n'aimez pas de votre playlist.

## Installation

1. **Clonez le dépôt** :
   ```bash
   git clone https://github.com/wicra/download_playlist_yt.git

2. **Installez les dépendances nécessaires**.
3. **Créez un serveur web**.
4. **Déplacez le dépôt dans votre serveur web**.
5. **Donnez les droits nécessaires**.

   Les commandes utilisées sont présentes dans le dossier `install_server`.

### Autres Scripts

- `download_update.py` : Script non utilisé pour télécharger des vidéos YouTube en MP3.
- `uninstall.py` : Script pour désinstaller toutes les dépendances Python liées aux téléchargements YouTube.

## Utilisation

- **Ajouter des Musiques** : Fournissez un lien YouTube pour ajouter des morceaux ou des playlists à votre bibliothèque. Le script Python gère le téléchargement et l'ajout automatique à votre playlist.
- **Contrôler la Lecture** : Utilisez les contrôles intégrés dans l'interface web pour gérer la lecture de la musique (lecture, pause, saut de piste, etc.).
- **Annuler un Téléchargement** : Cliquez sur le bouton d'annulation pour interrompre un téléchargement en cours.
- **Gérer les Logs** : Affichez et supprimez les logs directement depuis l'interface web.
- **Modifier la Playlist** : Supprimez des morceaux que vous n'aimez pas directement depuis l'interface web.
