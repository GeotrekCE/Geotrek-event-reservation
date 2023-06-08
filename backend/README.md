# Paquet psycopg2-binary ou psycopg2 ?

Les dépendances dans les fichiers requirements.* sont communes dev et prod et c'est le paquet psycopg2 qui est utilisé
comme recommandé.

Sur un environnement de dev il est plus simple d'utiliser psycopg2-binary qui évite d'installer les paquets nécessaires
pour compiler les sources sur sa machine.
