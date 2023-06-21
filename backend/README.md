# Préparation de la BD

L'outil doit pouvoir se connecter sur la BD Geotrek Admin. La définition des tables et fonctions nécessaires se trouve
dans `./db/create_db_structure.sql`.

Les commandes créent les tables nécessaires (nécessite les privilèges de lecture et référencement de la table
`tourism_touristicevent`) dans le nouveau schéma `animations`.

# Démarrer le serveur Flask de dev

Serveur sur `http://localhost:5000` :

```
flask run --debug
```

# Démarrer un conteneur docker de prod

Serveur sur `http://localhost:8001` :

```shell
docker build --tag png-resa .
docker run  --rm  --env-file ./docker.env  -p 0.0.0.0:8001:8000  png-resa  
```

Pour faire des tests de configuration sans reconstruire l'image Docker :

```shell
docker run  --rm  --env-file ./docker.env  -p 0.0.0.0:8001:8000  -v $(pwd)/config:/opt/png-resa/config  png-resa
```

# Paquet psycopg2-binary ou psycopg2 ?

Les dépendances dans les fichiers requirements.* sont communes dev et prod et c'est le paquet psycopg2 qui est utilisé
comme recommandé.

Sur un environnement de dev il est plus simple d'utiliser psycopg2-binary qui évite d'installer les paquets nécessaires
pour compiler les sources sur sa machine.


# Déploiement

## Configurer le backend

Un exemple de configuration est donné : `backend/config/config.py.sample`.

Certains paramètres n'ont pas de valeur par défaut et doivent obligatoirement être fournis. Il s'agit de :

- PUBLIC_SERVER_NAME
- ADMIN_EMAILS
- SECRET_KEY
- MAIL_DEFAULT_SENDER

La description des paramètres et des exemples de valeurs sont dans le fichier `.sample`.


## Configurer la connexion à la BD Geotrek

De plus vous aurez certainement besoin de modifier les paramètres par défaut de connexion à la BD. La configuration par
défaut se connecte en HTTP sur le localhost avec le port standard 5432 et les identifiants par défaut de geotrek. Les
éléments de configuration peuvent être écrasés individuellement par des variables d'environnement. Par exemple :

GEOTREK_DB_PASSWORD=unmotdepasseplussecure

Voir `backend/config/config.py.sample` pour les autres paramètres.

Plusieurs configuration sont possibles :

1. dev local
2. la BD se trouve sur un serveur distant 
3. docker png-web + la BD se trouve sur le docker host
4. docker png-web + docker postgres Geotrek BD dans la même stack docker-compose

### 1. dev local

Utiliser la valeurs par défaut de la configuration.

### 2. la BD se trouve sur un serveur distant

Définir variable d'environnement : `GEOTREK_DB_HOST=server.distant.net`

### 3. docker png-web + la BD se trouve sur le docker host

Configuration du docker-compose.yml d'exemple : `GEOTREK_DB_HOST` est laissé vide et le `entrypoint.sh` se charge de
trouver l'IP de la passerelle dans le conteneur.

### 4. docker png-web + docker postgres Geotrek BD dans la même stack docker-compose

Créer un réseau docker et indiquer le nom du service de la BD Geotrek dans le `docker.env`


## Fournir la configuration au conteneur docker

Le backend s'attend à trouver un fichier `./backend/config/config.py` (par rapport au répertoire du projet dans le conteneur docker).

Il est conseillé de fournir ce fichier en montant un volume dans le conteneur, par exemple :

`docker run -v /path/to/config:/opt/png-resa/backend/config` -p 127.0.0.1:8000:8000 png-resa`

C'est cette approche qui est utilisée dans le `docker-compose.yml` fourni en exemple.


## Configurer l'envoi de l'email de rappel

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

## Configurer les loggers

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
