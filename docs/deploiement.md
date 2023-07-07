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

Un fichier de configuration `config.py` est à fournir au backend. Plus d'infos sur `backend/README.md`.

Le backend du portail de réservation se connecte directement sur la base de données de Geotrek Admin en lecture seule.

## Déployer le frontend

### Construire le build

Une fois la configuration réalisée, il faut construire le projet. Les résultats du build se situe dans le dossier `dist`.

Le contenu de ce dossier est le livrable, il peut être déployé sur un serveur Apache / Nginx.

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

**Configurer le front (fichier config.js)**

Le build contient un exemple de configuration à adapter à chaque environnement.

**Configuration principale**
Voici le contenu du fichier `config.js` :

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


**Customiser les fichiers md**

Afin de permettre une souplesse côté textes affichés à l'utilisateur,
nous avons mis en place plusieurs fichiers Markdown
permettant via un montage docker d'écraser le contenu par défaut proposé dans le code source.

* `public/page_accueil.md` : affiché sur la page d'accueil du site
* `public/page_reservation.md` : affiché sur la page de listing des réservations de l'utilisateur
* `public/page_info_adin.md` : page d'information réservée aux administrateurs


**`.env`**

Configuration générale de l'application
* `VITE_APP_TITLE` : Titre de la page


**Style**

Vous pouvez customiser l'application en ajoutant du css dans le fichier `public/css/custom.css`
