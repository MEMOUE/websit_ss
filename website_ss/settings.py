"""
Django settings for website_ss project (Dr. Soumahoro Souleymane).
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-8p+32!xx!)bjb-##q==w7d*2c_*hd=-7ry^um3$3_hsj)i+akx'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'website_ss.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'website_ss.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'website_ss',
        'USER': 'root',
        'PASSWORD': '123456789',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─── Internationalisation ────────────────────────────────────────────────────
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE     = 'Africa/Abidjan'
USE_I18N      = True
USE_TZ        = True

# ─── Fichiers statiques ──────────────────────────────────────────────────────
STATIC_URL       = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT      = BASE_DIR / 'staticfiles'

# ─── Fichiers media ──────────────────────────────────────────────────────────
MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─── Email (SMTP) ────────────────────────────────────────────────────────────
EMAIL_BACKEND      = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST         = 'mail.soumahorosouleymane.com'
EMAIL_PORT         = 587
EMAIL_USE_SSL      = False
EMAIL_USE_TLS      = True
EMAIL_HOST_USER    = 'contact@soumahorosouleymane.com'
EMAIL_HOST_PASSWORD = 'Passer@123'
DEFAULT_FROM_EMAIL = 'contact@soumahorosouleymane.com'
CONTACT_EMAIL      = 'contact@soumahorosouleymane.com'

# ─── Facebook Graph API ──────────────────────────────────────────────────────
# Page Access Token obtenu via https://developers.facebook.com/tools/explorer/
# Page cible : Dr. Soumahoro Souleymane (ID: 61579911162838)
# ⚠️  Ce token expire dans ~60 jours — à renouveler ou échanger contre
#     un long-lived token via /oauth/access_token?grant_type=fb_exchange_token
FB_PAGE_ACCESS_TOKEN = (
    "EAAWHEcZCp9B4BRHaC8WvyfHSwV9KZBaaayrq74gFsoNN8STLbh86NbEyZCMdWMRFdSD"
    "pohRZCT8DopPiHOhkf4sh3hFrxgdrB282sGKoaCiiJwHQUNZCR7JVhfPdd8zKv72gOW5"
    "JsPaZCqIyuZB01Sn1XcHyJLSVdrHxab7q1Tskh2SRADUMyPsn3XYfVBP2YAIEsBcCVd9"
    "8jrR4xIt55icIeWsFZBFuoBZBpivIDTRZBJdgZDZD"
)