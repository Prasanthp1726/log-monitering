from pathlib import Path
from dotenv import load_dotenv

# =========================
#  # LOAD ENV VARIABLES 
# # =========================
load_dotenv()
# =========================
# BASE DIR
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# SECURITY
# =========================
SECRET_KEY = 'replace-this-with-your-secret-key'
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# =========================
# APPLICATIONS
# =========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'drf_yasg',
    'ingestion',
]

# =========================
# MIDDLEWARE
# =========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# =========================
# URL CONFIG
# =========================
ROOT_URLCONF = 'log_monitoring.urls'

# =========================
# TEMPLATES
# =========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

# =========================
# WSGI
# =========================
WSGI_APPLICATION = 'log_monitoring.wsgi.application'

# =========================
# DATABASE
# =========================
# =========================
# DATABASE
# =========================
import os

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "logdb"),
        "USER": os.getenv("DB_USER", "loguser"),
        "PASSWORD": os.getenv("DB_PASSWORD", "logpass"),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}


# =========================
# LANGUAGE & TIME
# =========================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# =========================
# STATIC FILES
# =========================
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =====================================================
# ✅ EMAIL SETTINGS (GMAIL – TLS FINAL FIX)
# =====================================================

EMAIL_BACKEND = 'log_monitoring.email_backend.DevSMTPEmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587

EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

EMAIL_HOST_USER = 'prasanthp172001@gmail.com'
EMAIL_HOST_PASSWORD = 'iptgurqdobnjfvsz'   # Gmail App Password
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
ALERT_RECEIVER_EMAIL = "prasanthp172001@gmail.com"
# =========================
# ALERT SETTINGS
# =========================
ALERT_RECIPIENTS = [
    'prasanthp172001@gmail.com'
]

# =========================
# REST FRAMEWORK
# =========================
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
CELERY_BEAT_SCHEDULE = {
    "auto-anomaly-check": {
        "task": "ingestion.tasks.auto_anomaly_check",
        "schedule": 60.0,  # every 60 seconds
    },
}
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
