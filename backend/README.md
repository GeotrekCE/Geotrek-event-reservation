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
