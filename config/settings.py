"""
Django settings for web_project project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
import io
from urllib.parse import urlparse

import environ
import google.auth
from google.cloud import secretmanager
import random
import string
from pathlib import Path

from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

from .template import TEMPLATE_CONFIG, THEME_LAYOUT_DIR, THEME_VARIABLES

load_dotenv()  # take environment variables from .env.

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
EMBEDDING_MODEL = "BAAI/bge-small-en" 
FAISS_DB = Path(BASE_DIR) / "DBs/faiss_index_2"
CHUNK_SIZE = 300
CHUNCK_SEPARATOR = ["<END>", "\n\n", "\n"]
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/


# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
# ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]
# API_URL = ""



# # Current DJANGO_ENVIRONMENT
# ENVIRONMENT = os.environ.get("DJANGO_ENVIRONMENT", "local")


## Django Sashi Test Start
# [START cloudrun_django_secret_config]
# SECURITY WARNING: don't run with debug turned on in production!
# Change this to "False" when you are ready for production
env = environ.Env(DEBUG=(bool, True))
env_file = os.path.join(BASE_DIR, ".env")

# Attempt to load the Project ID into the environment, safely failing on error.
try:
    _, os.environ["GOOGLE_CLOUD_PROJECT"] = google.auth.default()
except google.auth.exceptions.DefaultCredentialsError:
    pass

if os.path.isfile(env_file):
    # Use a local secret file, if provided
    print("inside env file: ", env_file)
    env.read_env(env_file)
# [START_EXCLUDE]
elif os.getenv("TRAMPOLINE_CI", None):
    # Create local settings if running with CI, for unit testing

    placeholder = (
        f"SECRET_KEY=a\n"
        "GS_BUCKET_NAME=None\n"
        f"DATABASE_URL=sqlite://{os.path.join(BASE_DIR, 'db.sqlite3')}"
    )
    env.read_env(io.StringIO(placeholder))
# [END_EXCLUDE]
elif os.environ.get("GOOGLE_CLOUD_PROJECT", None):
    # Pull secrets from Secret Manager
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    #project_num  = os.environ.get("GOOGLE_CLOUD_PROJECT_NUM")
    #project_num  = 856106838446
    project_num  = 683505664244
    client = secretmanager.SecretManagerServiceClient()
    settings_name = os.environ.get("SETTINGS_NAME", "django_settings")
    name = f"projects/{project_num}/secrets/{settings_name}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("UTF-8")

    env.read_env(io.StringIO(payload))
else:
    raise Exception("No local .env or GOOGLE_CLOUD_PROJECT detected. No secrets found.")
# [END cloudrun_django_secret_config]


# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = os.environ.get("SECRET_KEY")
SECRET_KEY = env("SECRET_KEY")
if not SECRET_KEY:
    SECRET_KEY = "".join(random.choice(string.ascii_lowercase) for i in range(32))

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = os.environ.get("DEBUG", True)
DEBUG = env("DEBUG")

# Current DJANGO_ENVIRONMENT
#ENVIRONMENT = env("DJANGO_ENVIRONMENT", default="local")
ENVIRONMENT = os.environ.get("DJANGO_ENVIRONMENT", "local")

# [START cloudrun_django_csrf]
# SECURITY WARNING: It's recommended that you use this when
# running in production. The URL will be known once you first deploy
# to Cloud Run. This code takes the URL and converts it to both these settings formats.
CLOUDRUN_SERVICE_URL = env("CLOUDRUN_SERVICE_URL", default=None)
if CLOUDRUN_SERVICE_URL:
    ALLOWED_HOSTS = [urlparse(CLOUDRUN_SERVICE_URL).netloc]
    CSRF_TRUSTED_ORIGINS = [CLOUDRUN_SERVICE_URL]
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
else:
    ALLOWED_HOSTS = ["*"]

#ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]
API_URL = env("CLOUDRUN_SERVICE_URL", default=None)
# [END cloudrun_django_csrf]




# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.sample",
    "apps.hrdata.apps.HrdataConfig",
    "rest_framework",
    "apps.tables.apps.TablesConfig",
    "django.contrib.sites",
    "apps.chat.apps.ChatConfig",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
]

SOCIALACCOUNT_PROVIDERS = { 
    'google': { 
        'SCOPE': [ 
            'profile', 
            'email', 
        ], 
        'AUTH_PARAMS': { 
            'access_type': 'online' 
        } 
    } 
}

SITE_ID = 1
SOCIALACCOUNT_LOGIN_ON_GET=True
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend"
)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "apps.chat.middleware.CurrentUserMiddleware",
    "apps.hrdata.middleware.CurrentUserMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "config.context_processors.language_code",
                "config.context_processors.get_cookie",
                "config.context_processors.environment",
            ],
            "libraries": {
                "theme": "web_project.template_tags.theme",
            },
            "builtins": [
                "django.templatetags.static",
                "web_project.template_tags.theme",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db/db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

# Enable i18n and set the list of supported languages
# LANGUAGES = [
#     ("en", _("English")),
#     ("fr", _("French")),
#     ("de", _("German")),
#     ("pt", _("Portuguese")),
#     ("ar", _("Arabic")),
#     # Add more languages as needed
# ]

# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Set default language
LANGUAGE_CODE = "en"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / "locale",
]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "src" / "assets",
]

# if not DEBUG:
#    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Template Settings
# ------------------------------------------------------------------------------

THEME_LAYOUT_DIR = THEME_LAYOUT_DIR
TEMPLATE_CONFIG = TEMPLATE_CONFIG
THEME_VARIABLES = THEME_VARIABLES

# Your stuff...
# ------------------------------------------------------------------------------

SOCIALACCOUNT_LOGIN_ON_GET=True

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/" 