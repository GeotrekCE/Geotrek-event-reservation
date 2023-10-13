# Manuel de déploiement

## Description de la stack technique

* Backend
  * Flask + SQLAlchemy + Marshmallow + Flask extensions
  * Testé avec Geotrek Admin v2.98.0 et Geotrek Rando 3.13.6
* Frontend
  * Vue 3 + TypeScript + Vite
  * Tailwind CSS
  * Prime Vue pour les composants complexes (datatable, dataview, ...)


## Lien de réservation dans Geotrek Rando

Il faut ajouter le script `install/scriptsFooter.html` dans la customization de Geotrek Rando.
L'emplacement est `<geotrek-rando>/customization/html/scriptsFooter.html`.
## Préparation de la BD

L'outil doit pouvoir se connecter sur la BD Geotrek Admin. La définition des tables et fonctions nécessaires se trouve
dans `./db/create_db_structure.sql`.

Les commandes créent les tables nécessaires (nécessite les privilèges de lecture et référencement de la table
`tourism_touristicevent`) dans le nouveau schéma `animations`.

## Déployer le backend

Le déploiement en prod est plutôt pensé pour utiliser docker, mais il peut être réalisé de façon plus classique. Les fichiers suivants sont fournis :

- docker-compose.yml
- backend/Dockerfile
- backend/docker.env
- backend/entrypoint.sh

Le backend du portail de réservation se connecte directement sur la base de données de Geotrek Admin en lecture seule.

### Configuration

Un exemple de configuration est donné : `backend/config/config.py.sample`.

Certains paramètres n'ont pas de valeur par défaut et doivent obligatoirement être fournis. Il s'agit de :

- PUBLIC_SERVER_NAME
- ADMIN_EMAILS
- SECRET_KEY
- MAIL_DEFAULT_SENDER
- Connexion à la base de données

La description des paramètres et des exemples de valeurs sont dans le fichier `.sample`.

***Configurer les loggers***

Afficher le rendu des emails envoyés : descendre le niveau de log pour le nom `core` et ses descendants.

```python
{
    'loggers': {
        'core': {
            'level': 'DEBUG',
        },
    },
}
```

Attention : l'initialisation du handler `log_file` échouera si le répertoire de destination n'existe pas.

### Installation avec Docker

#### Configurer la connexion à la BD Geotrek
Les éléments de configuration peuvent être écrasés individuellement par des variables d'environnement. Par exemple :

`GEOTREK_DB_PASSWORD=unmotdepasseplussecure`

Voir `backend/config/config.py.sample` pour les autres paramètres.

***la BD se trouve sur le docker host***

Configuration du docker-compose.yml d'exemple : `GEOTREK_DB_HOST` est laissé vide et le `entrypoint.sh` se charge de
trouver l'IP de la passerelle dans le conteneur.

***docker postgres Geotrek BD dans la même stack docker-compose***

Créer un réseau docker et indiquer le nom du service de la BD Geotrek dans le `docker.env`


#### Configurer la timezone

Dans le `Dockerfile` renseigner la variable d'environnement `TZ`, par exemple "Europe/Paris" (par défaut). Il faut
reconstruire l'image pour que le changement soit pris en compte.

#### Lancer le conteneur docker

Il est conseillé de fournir ce fichier en montant un volume dans le conteneur, par exemple :

`docker run -v /path/to/config:/<PATH_TO_Geotrek-event-reservation>/backend/config -p 127.0.0.1:8000:8000 png-resa`

C'est cette approche qui est utilisée dans le `docker-compose.yml` fourni en exemple.


### Installation classique

Une fois le fichier de configuration renseigné

#### Installer les paquets python
```sh
cd <PATH_TO_Geotrek-event-reservation>/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Configuration de systemd

modifier le fichier `installation/reservation_animations.service` : en remplaçant les variables :
* `USER` : Utilisateur courant
* `BASE_DIR` : répertoire où est installé l'application

```sh
sudo cp installation/reservation_animations.service /etc/systemd/system/reservation_animations.service
sudo systemctl daemon-reload
sudo systemctl enable reservation_animations
```


### Configurer l'envoi de l'email de rappel

Un script est disponible qui envoie un mail de rappel à chacun des participants des événements ayant lieu le lendemain :
`backend/send_email_rappel.py`.

L'email est envoyé uniquement aux participants qui ne sont pas sur liste d'attente.

Le script peut être déclenché avec un job cron. Par exemple dans `/etc/crontab` (à ajuster selon son système) :

```shell
# Pour exécuter script.sh tous les jours à 17:10.
10 17  * *  * nomdutilisateur script.sh
```

Pour lancer le script avec docker :

`docker compose run --rm png-web python send_email_rappel.py`

Pour lancer le script en-dehors de docker : pas d'autre pré-requis que d'activer le virtualenv.

```shell
source venv/bin/activate
python send_email_rappel.py
```

## Déployer le frontend

### "Builder" l'application

Une fois la configuration réalisée, il faut construire le projet. Les résultats du build se situe dans le dossier `dist`.

Le contenu de ce dossier peut être déployé via un serveur Apache / Nginx.

Copier les fichiers de customisation et les
```sh
cd front-vite
cp -n .env.sample .env
cp -n public/config/config.js.sample public/config/config.js
cp -n public/css/custom.css.sample public/css/custom.css
cp -n public/public/page_info_admin.md.sample public/public/page_info_admin.md
cp -n public/public/page_reservation.md.sample public/public/page_reservation.md
cp -n public/public/page_accueil.md.sample public/public/page_accueil.md
```

Lancer les commandes
```sh
cd front-vite
nvm use
npm ci
npm run build
```

### Configuration

**Configurer principale (`public/config/config.js`)**

Le build contient un exemple de configuration à adapter à chaque environnement.

```js
const CONFIGURATION = {
  URL_APPLICATION: 'http://localhost:5000',
  URL_GTA: 'http://localhost:8000',
  URL_GTR: 'http://localhost:8000',
  DAY_BEFORE_RESA: -1,
  RESA_NB_DELTA: 3,
  RESA_BEGINNING_DATE: new Date('2023-06-26')
}
```

* `URL_APPLICATION` correspond à l'API du serveur backend Flask
* `URL_GTA` correspond à l'URL du portail Geotrek Admin
* `URL_GTR` correspond à l'URL du portail Geotrek grand public
* `DAY_BEFORE_RESA` nombre de jour avant le début de l'animation où l'inscription est bloquée. Si -1, non pris en compte
* `RESA_NB_DELTA` est une tolérance pour accepter une réservation qui dépasserait la capacité d'accueil de l'animation
* `RESA_BEGINNING_DATE` est la date à partir de laquelle l'outil permet de créer une réservation


**Customiser les fichiers d'informations textuelle (`public/*.md`)**

Afin de permettre une souplesse côté textes affichés à l'utilisateur,
nous avons mis en place plusieurs fichiers Markdown à compléter en fonction de vos besoins.

* `public/page_accueil.md` : affiché sur la page d'accueil du site
* `public/page_reservation.md` : affiché sur la page de listing des réservations de l'utilisateur
* `public/page_info_admin.md` : page d'information réservée aux administrateurs


**Environnement (`.env`)**

Configuration générale de l'application
* `VITE_APP_TITLE` : Titre de la page


**Style (`public/css/custom.css`)**

Vous pouvez customiser l'application en ajoutant du css dans le fichier `public/css/custom.css`


## Monitoring - Sentry

Il est possible d'utiliser Sentry pour suivre l'application. Pour cela il suffit de renseigner la variable `SENTRY_DSN` du fichier de configuration.
