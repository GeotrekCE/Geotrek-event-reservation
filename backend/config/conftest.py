from datetime import timedelta
import os

TESTING = True
# --- Content settings ---

# Ce texte est placé au début de l'objet dans les emails, par exemple "[Rando Guadeloupe]".
ORGANISM_FOR_EMAIL_SUBJECT = ""


# --- Application settings ---


# Le nombre maximale de personnes que l'on peut mettre en liste d'attente sur un événement.
LISTE_ATTENTE_CAPACITY = 10
# Le nombre maximal d'animations auxquelles une personne peut s'inscrire
NB_ANIM_MAX_PER_USER = 3
# Le nombre maximale de participant pouvant s'inscrire à une animation
NB_PARTICIPANTS_PER_ANIM = 10
# L'adresse où écoute le frontend du portail de réservation, par exemple : 'www.png-resa.fr' ou 'localhost:5000'.
PUBLIC_SERVER_NAME = "http://localhost:5173"

# La liste des emails des administrateurs du portail, par exemple :
# ADMIN_EMAILS = ['admin@png-resa.fr', 'teddy@png-it.fr']
# Ces emails sont utilisés pour donner les permissions admin à l'authentification
ADMIN_EMAILS = ["test.test@test.fr"]


# Ces emails sont utilisés pour recevoir les notifications
# d'annulation de réservations par les utilisateurs.
NOTIFICATION_EMAILS = ["test.test@test.fr"]


# Le path sur le frontend pour générer le lien de confirmation de réservation qui est envoyé par email.
FRONTEND_CONFIRMED_PATHNAME = "/resaconfirm"

# Le path sur le frontend pour générer le lien vers le portail qui est ajouté dans les emails.
FRONTEND_PORTAL_PATHNAME = "/login"

# Le path sur le frontend pour générer le lien de connexion envoyé par email.
FRONTEND_LOGIN_PATHNAME = "/login/callback"

# La durée de vie des tokens de connexion envoyés par email.
LOGIN_TOKEN_LIFETIME = timedelta(hours=5)

# dictConfig Python standard, passé au module `logging` à l'initialisation de l'app Flask.
LOGGING = {
    "version": 1,
    "formatters": {
        "simple": {"format": "%(levelname)s %(asctime)s %(name)s %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "core": {
            "level": "INFO",
        },
        "send_email_rappel": {
            "level": "INFO",
        },
    },
    "root": {
        "handlers": ["console"],
    },
}


# --- Database settings ---

GEOTREK_DB_HOST = os.getenv("GEOTREK_DB_HOST", "127.0.0.1")
GEOTREK_DB_PORT = os.getenv("GEOTREK_DB_PORT", "5432")
GEOTREK_DB_USER = os.getenv("GEOTREK_DB_USER", "geotrek")
GEOTREK_DB_PASSWORD = os.getenv("GEOTREK_DB_PASSWORD", "geotrek")
GEOTREK_DB_NAME = os.getenv("GEOTREK_DB_NAME", "geotrekdb")
SQLALCHEMY_DATABASE_URI = f"postgresql://{GEOTREK_DB_USER}:{GEOTREK_DB_PASSWORD}@{GEOTREK_DB_HOST}:{GEOTREK_DB_PORT}/{GEOTREK_DB_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = False


# --- Flask settings ---

# SECRET_KEY chiffre les cookies de session, il faut indiquer une chaîne de caractères aléatoires à garder hors
# du code source.
# Exemple pour générer une chaîne :
# $ python -c 'import secrets; print(secrets.token_hex())'
# > '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
SECRET_KEY = "192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf"

# Définit la durée de validité du cookie de session qui garde les utilisateurs connectés, 31 jours par défaut.
PERMANENT_SESSION_LIFETIME = timedelta(days=31)

# Définit si le cookie de session doit être prolongé à chaque requête, oui par défaut.
SESSION_REFRESH_EACH_REQUEST = True

# --- Flask Mail settings ---

# MAIL_DEFAULT_SENDER: default None, paramètre obligatoire même en mode dev/test.
MAIL_DEFAULT_SENDER = "test@test.fr"

# MAIL_SUPPRESS_SEND: default app.testing, paramètre utile pour le développement sans serveur SMTP.
# MAIL_SUPPRESS_SEND = True

# MAIL_SERVER: default ‘localhost’
# MAIL_PORT: default 25
# MAIL_USE_TLS: default False
# MAIL_USE_SSL: default False
# MAIL_DEBUG: default app.debug
# MAIL_USERNAME: default None
# MAIL_PASSWORD: default None
# MAIL_MAX_EMAILS: default None
# MAIL_ASCII_ATTACHMENTS: default False

MAIL_SERVER = os.environ.get("MAIL_SERVER")
MAIL_PORT = os.environ.get("MAIL_PORT")
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
