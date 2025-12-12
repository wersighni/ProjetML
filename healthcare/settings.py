from pathlib import Path

# -----------------------------
# PATH PRINCIPAL DU PROJET
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# PARAMÈTRES SÉCURITÉ
# -----------------------------
SECRET_KEY = "django-insecure-oiirdkv+&a0@hwy@de+omax=$&o!h)k54j(=y!bw!cpud3ie8u"
DEBUG = True
ALLOWED_HOSTS = []

# -----------------------------
# APPLICATIONS DJANGO + APP PERSONNELLE
# -----------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "predictor",  # ⭐ TON APPLICATION
]

# -----------------------------
# MIDDLEWARE
# -----------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# -----------------------------
# URL & WSGI
# -----------------------------
ROOT_URLCONF = "healthcare.urls"
WSGI_APPLICATION = "healthcare.wsgi.application"

# -----------------------------
# TEMPLATES
# -----------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [BASE_DIR / 'templates'],  # Django va chercher automatiquement dans predictor/templates/
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# -----------------------------
# BASE DE DONNÉES
# -----------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# -----------------------------
# LANGUE & TIME ZONE
# -----------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# -----------------------------
# 🔥 STATIC FILES (TON BACKGROUND IMAGE)
# -----------------------------
STATIC_URL = "/static/"

# Dossier où Django va chercher les fichiers static (CSS, images…)
STATICFILES_DIRS = [
    BASE_DIR / "predictor" / "static",
]

# Utilisé seulement si on fait `collectstatic` (production)
STATIC_ROOT = BASE_DIR / "staticfiles"

# -----------------------------
# AUTO FIELD
# -----------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
