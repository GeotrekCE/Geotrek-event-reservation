# Reservation des animations dans Geotrek

Application permettant la gestion des réservations des animations publiées sur Geotrek.
Elle permet aux visiteurs d'un portail Geotrek Rando de réserver des places pour les
événements.
Une interface d'administration est disponible pour gérer les réservations.

La gestion de l'authentification est sans mot de passe et fonctionne avec des liens envoyés par email.

Schéma simplifié du fonctionnement pour le grand public
![Fonctionnement pour le grand public](docs/images/schema_grand_public.png)

Schéma simplifié du fonctionnement pour les administrateur
![Fonctionnement pour l'interface d'administrateur](docs/images/schema_admin.png)


# Installation et configuration

## Configuration

 * `backend/config/config.py`
 * `front-vite/public/config/config.js`
 * `front-vite/public/page_accueil.md`
 * `front-vite/public/page_info_admin.md`
 * `front-vite/public/page_reservation.md`

## Déploiement

Les instructions se trouvent à `docs/deploiement.md` et dans les READMEs `backend/README.md` et `front-vite/README.md`.
