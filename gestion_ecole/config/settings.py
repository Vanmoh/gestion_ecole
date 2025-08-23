from pathlib import Path
import os
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

# Chargement .env
env = environ.Env(
    DEBUG=(bool, False),
)
environ.Env.read_env(BASE_DIR / ".env")

# ⚠️ Utiliser les bons helpers et "default=" !
DEBUG = env.bool("DEBUG", default=True)
SECRET_KEY = env("SECRET_KEY", default="change-this-secret")

ALLOWED_HOSTS = [
    h.strip()
    for h in env("ALLOWED_HOSTS", default="127.0.0.1,localhost").split(",")
    if h.strip()
]

# Base de données MySQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("DB_NAME", default="gestion_ecole"),
        "USER": env("DB_USER", default="ecole_user"),
        "PASSWORD": env("DB_PASSWORD", default="motdepassefort"),
        "HOST": env("DB_HOST", default="127.0.0.1"),
        "PORT": env("DB_PORT", default="3306"),
        "OPTIONS": {
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_ALL_TABLES'",
        },
    }
}

LANGUAGE_CODE = env("LANGUAGE_CODE", default="fr")
TIME_ZONE = env("TIME_ZONE", default="Africa/Bamako")
USE_I18N = True
USE_TZ = True

# Apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Apps projet
    "accounts",
    "catalog",
    "students",
    "core",
    
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
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
                "core.context_processors.active_context",
                
            ],
              # Optionnel : si tu veux éviter {% load core_extras %} dans chaque template
              "builtins": ["core.templatetags.core_extras"],   # ✅ chemin complet
              
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Base de données MySQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
        "OPTIONS": {
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_ALL_TABLES'",
        },
    }
}

# i18n
LANGUAGE_CODE = env("LANGUAGE_CODE", default="fr")
TIME_ZONE = env("TIME_ZONE", default="Africa/Bamako")
USE_I18N = True
USE_TZ = True

# Static & Media
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "base_static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/login/"


TEMPLATES[0]["OPTIONS"].setdefault("builtins", [])
if "core.templatetags.core_extras" not in TEMPLATES[0]["OPTIONS"]["builtins"]:
    TEMPLATES[0]["OPTIONS"]["builtins"].append("core.templatetags.core_extras")
