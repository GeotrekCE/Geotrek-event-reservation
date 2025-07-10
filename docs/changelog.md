
# Changelog

**🐛 Corrections**
 - Correction des informations de rendez-vous qui ne sont pas enregistrées.

## 0.4.0 (unreleased)

**🐛 Corrections**
 - Changement du texte "massifs" par "localisation" sur la page du formulaire d'inscription.

## 0.3.0 (2024-06-24)
 
**🚀 Nouveautés**

- Mise à jour vers SQLAlchemy 1.4 (#63)P
- Mise à jour des librairies javascript (#65)
- Utilisation de MenuBar pour la barre de menu (#65)
- Style page des statistiques (#65)
- Utilisation de toast pour afficher les messages d'erreur du formulaire d'inscription aux animations (#66)
- [BACK] Ajout paramètre `NB_PARTICIPANTS_MAX_PER_ANIM_PER_USER` qui permet d'indiquer le nombre maximal de participants que l'on peut enregistrer lors de la création d'une réservation 
- [BACK] Ajout paramètre `NB_ANIM_MAX_PER_USER` qui permet d'indiquer le nombre maximal d'animations auxquelles un utilisateur peut s'inscrire par an.
 


**🐛 Corrections**
 - Ajout de test concernant la capacité de l'événement (`is_reservation_possible_for`) lors de la mise à jour d'une réservation

**⚠️ Notes de version**
 - Les paramètres de configuration css de la barre de menu ont changé. Se référer au fichier `front-vite/public/css/custom.css.sample` pour évaluer les impacts


## 0.2.0 (2024-06-14)

**🚀 Nouveautés**

- Ajout d'un paramètre `USER_CAN_CANCEL` qui permet de configurer si l'utilisateur peut ou non annuler lui même sa réservation

**🐛 Corrections**

- Mise à jour de la version de postgresql utilisée dans les actions de github

## 0.1.0 (2024-06-13)

Outil permettant la gestion des réservations des animations saisies dans Geotrek-admin.

**🚀 Fonctionnalités**

- Interface d'administrateur:
    - Visualiser et rechercher dans les animations publiées sur Geotrek
    - Visualiser le détail d'une animation
    - Gérer des inscriptions
    - Annuler les animations
    - Ajouter un bilan
    - Exporter le bilan des animations et de leur réservation

- Interface grand public:
    - Lien vers le formulaire d'inscription dans Geotrek-rando-v3
    - Formulaire d'inscription
    - Annulation d'une inscription
    - Visualiser ses inscriptions
