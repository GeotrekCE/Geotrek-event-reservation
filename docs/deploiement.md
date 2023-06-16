# Manuel de déploiement

## Description de la stack technique

* Backend
  * Flask + SQLAlchemy + Marshmallow + Flask extensions
  * Testé avec Geotrek Admin v2.98.0 et Geotrek Rando 3.13.6
* Frontend
  * Vue 3 + TypeScript + Vite
  * Tailwind CSS
  * Prime Vue pour les composants complexes (datatable, dataview, ...)

## Déploiement

### Déployer le backend

Le déploiement en prod est plutôt pensé pour utiliser docker. Les fichiers suivants sont fournis :

- docker-compose.yml
- backend/Dockerfile
- backend/docker.env
- backend/entrypoint.sh

Un fichier de configuration `config.py` est à fournir au backend. Plus d'infos sur `backend/README.md`.

Le backend du portail de réservation se connecte directement sur la base de données de Geotrek Admin en lecture seule.
La procédure pour créer le schéma et les tables attendus est détaillée ainsi que les possibilités pour fournir
les infos de connexion au backend.

### Déployer le frontend

**Construire le build**

La commande `npm run build` permet de construire le projet.

Le résultat de cette commande se situe dans le dossier `dist`.

Le contenu de ce dossier est le livrable, il peut être déployé sur un serveur Apache / Nginx.

**Configurer le front (fichier config.js)**

Le build contient un exemple de configuration à adapter à chaque environnement.

Voici le contenu du fichier `config.js` :

```js
// URL_APPLICATION: Url de l'application backend
// URL_GTA: url de l'application geotrek admin
// URL_GTR: url de l'application geotrek
// DAY_BEFORE_RESA: nombre de jours avant la date de debut de l'animation ou l'inscription est possible (si -1 aucune limitation de date)
// RESA_NB_DELTA: nombre de participants surnuméraire acepté en plus du nombre de participants spécifiés dans geotrek
// RESA_BEGINNING_DATE: date à partir de laquelle les réservations sont ouvertes (PNG)

const CONFIGURATION = {
  URL_APPLICATION: 'http://localhost:5000',
  URL_GTA: 'http://localhost:8000',
  URL_GTR: 'http://localhost:8000',
  DAY_BEFORE_RESA: 15,
  RESA_NB_DELTA: 3,
  RESA_BEGINNING_DATE: new Date('2023-06-26')  
}
```

* `URL_APPLICATION` correspond à l'API du serveur backend Flask
* `URL_GTA` correspond à l'URL du portail Geotrek Admin
* `URL_GTR` correspond à l'URL du portail Geotrek grand public
* `DAY_BEFORE_RESA` est une variable précédemment utilisée par les Cévennes. Non utilisée à ce jour (voir `RESA_BEGINNING_DATE`)
* `RESA_NB_DELTA` est une tolérance pour accepter une réservation qui dépasserait la capacité d'accueil de l'animation
* `RESA_BEGINNING_DATE` est la date à partir de laquelle l'outil permet de créer une réservation


**Customiser les fichiers md**

Afin de permettre une souplesse côté textes affichés à l'utilisateur,
nous avons mis en place plusieurs fichiers Markdown 
permettant via un montage docker d'écraser le contenu par défaut proposé dans le code source.

* `public/page_accueil.md` : affiché sur la page d'accueil du site
* `public/page_reservation.md` : affiché sur la page de listing des réservations de l'utilisateur
