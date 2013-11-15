Installation du serveur CSGO
============================

D'après les articles du wiki Valve suivants :

* https://developer.valvesoftware.com/wiki/SteamCMD
* https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Dedicated_Servers

## Téléchargement et installation SteamCMD

Télécharger la SteamCMD avec wget :

    wget http://media.steampowered.com/client/steamcmd_linux.tar.gz

Décompresser l'archive :

    tar -xvzf steamcmd_linux.tar.gz

Lancer la ligne de commande Steam :

    chmod +x steamcmd.sh
    ./steamcmd.sh

Se connecter de manière anonyme :

    login anonymous

Forcer l'installation du jeu dans le bon dossier :

    force_install_dir /srv/csgo/

Installer le jeu et valider

    app_update 740 validate
