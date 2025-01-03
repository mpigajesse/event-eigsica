import os
from pathlib import Path
from dotenv import load_dotenv
import pymysql

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Construire les chemins à l'intérieur du projet comme ceci : BASE_DIR / 'sous-dossier'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Paramètres de démarrage rapide - non adaptés à la production
# Voir https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# AVERTISSEMENT DE SÉCURITÉ : gardez la clé secrète utilisée en production secrète !
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-rnwvt=iln^4#@@xx=w@chmzf52a=mpmdcsh^(qskf262stfd%y')

# AVERTISSEMENT DE SÉCURITÉ : ne pas exécuter avec le mode debug activé en production !
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Liste des hôtes autorisés
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# Utiliser PyMySQL comme driver pour MySQL
pymysql.install_as_MySQLdb()

# Définition des applications installées
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tailwind',
    'dashboard',
    'theme',
    'django_browser_reload',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

# Nom de l'application Tailwind
TAILWIND_APP_NAME = 'theme'  # remplacez 'tailwind' par 'theme'

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
]

# Configuration des URL racines
ROOT_URLCONF = 'eigsi_event_manager.urls'

# Configuration des templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),  # Pour des templates globaux
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Application WSGI
WSGI_APPLICATION = 'eigsi_event_manager.wsgi.application'

# Configuration de la base de données
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Moteur de base de données MySQL
        'NAME': os.getenv('DB_NAME'),  # Nom de la base de données
        'USER': os.getenv('DB_USER'),  # Utilisateur de la base de données
        'PASSWORD': os.getenv('DB_PASSWORD'),  # Mot de passe de l'utilisateur
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),  # Par défaut à localhost
        'PORT': os.getenv('DB_PORT', '3306'),  # Par défaut au port MySQL
        # 'OPTIONS': {
        #     'ssl_disabled': True,  # Option pour désactiver SSL (décommenter si nécessaire)
        # },
    }
}

# Validation des mots de passe
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # Pour la connexion locale (nom d'utilisateur et mot de passe)
    'allauth.account.auth_backends.AuthenticationBackend',  # Pour l'authentification via allauth
)


# Internationalisation
LANGUAGE_CODE = 'en-us'  # Code de langue

TIME_ZONE = 'UTC'  # Fuseau horaire

USE_I18N = True  # Utiliser l'internationalisation

USE_TZ = True  # Utiliser le temps universel

# URL des fichiers statiques
STATIC_URL = '/static/'

# Dossier des fichiers statiques
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Fichiers statiques locaux
]

# Configuration pour les fichiers médias
MEDIA_URL = '/media/'  # URL pour accéder aux fichiers médias
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Dossier où sont stockés les fichiers médias

# URL de redirection après connexion
LOGIN_REDIRECT_URL = '/login/'  # Redirection vers la page de connexion par défaut

# Utilisateur personnalisé
AUTH_USER_MODEL = 'dashboard.Utilisateur'  # Modèle utilisateur personnalisé

# Configuration par défaut du champ de clé primaire
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # Champ de clé primaire par défaut

NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"