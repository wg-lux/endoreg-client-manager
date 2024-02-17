import os
from .default_paths import (
    BASE_DIR,
    DROPOFF_DIR,
    PSEUDO_DIR,
    PROCESSED_DIR,
)
from .static import STATIC_URL, STATIC_ROOT, STORAGES
from .internationalization import LANGUAGE_CODE, TIME_ZONE, USE_I18N, USE_TZ
# from .celery import CELERY_BROKER_URL
import warnings



# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', "django-insecure-#&z!")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost"
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    "whitenoise.runserver_nostatic", # above staticfiles, useful for development
    'django.contrib.staticfiles',
    "rest_framework",
    "django_bootstrap5",

    # 'admin_interface',
    # 'flat_responsive',  # optional for django-admin-interface
    # 'flat',  # optional for django-admin-interface
    # 'colorfield',  # required for django-admin-interface
    # "endoreg_db.apps.EndoregDbConfig",
    "content_management.apps.ContentManagementConfig",
    "case_merger.apps.CaseMergerConfig",
    "data_collector.apps.DataCollectorConfig",
    "report_processor.apps.ReportProcessorConfig",
    "data_validation.apps.DataValidationConfig",
    "video_processor.apps.VideoProcessorConfig",
    "django_celery_beat",
    "celery",

    # agl packages
    "endoreg_db.apps.EndoregDbConfig",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware", # Should be placed directly after the Django Security Middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'content_management.middleware.ThemeMiddleware', # Darkmode
]

ROOT_URLCONF = 'endoreg_client_manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'endoreg_client_manager.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}




# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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



# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
