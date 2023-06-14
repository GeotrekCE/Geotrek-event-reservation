# Manuel de déploiement

## Description de la stack technique

* Backend
  * Flask + SQLAlchemy + ?
  * Geotrek vx.x.x ?
* Frontend
  * Vue 3 + TypeScript + Vite
  * Tailwind CSS
  * Prime Vue pour les composants complexes (datatable, dataview, ...)

## Déploiement

### Déployer le backend

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

const CONFIGURATION = {
  URL_APPLICATION: 'http://localhost:5000',
  URL_GTA: 'http://localhost:8000',
  URL_GTR: 'http://localhost:8000',
  DAY_BEFORE_RESA: 15,
  RESA_NB_DELTA: 3
}
```

* `URL_APPLICATION` correspond à l'API du serveur backend Flask
* `URL_GTA` correspond à l'URL du portail Geotrek Admin
* `URL_GTR` correspond à l'URL du portail Geotrek grand public
* `DAY_BEFORE_RESA` est une variable précédemment utilisée par les Cévennes. Non utilisée à ce jour
* `RESA_NB_DELTA` est une tolérance pour accepter une réservation qui dépasserait la capacité d'accueil de l'animation