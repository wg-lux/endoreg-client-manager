import os
from .default_paths import *
from .multilabel_ai import *
from .static import *
from .internationalization import LANGUAGE_CODE, TIME_ZONE, USE_I18N, USE_TZ
from .celery import *
from .logging_conf import LOGGING
from dotenv import load_dotenv
from pathlib import Path
from .utils import env_var_to_list, create_glob_expression
from .celery_schedule import CELERY_BEAT_SCHEDULE
from .caches import CACHES

from .database import (
    DATABASES,
    DATABASE_ROUTERS
)

from .report_reader_config import (
    PDF_TYPE_EXAMINATION,
    PDF_TYPE_HISTOLOGY
)

from .center_info import (
    ENDOREG_CENTER_NAME,
    ENDOREG_PROCESSOR_NAME,
    ENDOREG_CENTER_ID,
    PDF_TYPE_EXAMINATION,
    PDF_TYPE_HISTOLOGY
)

load_dotenv()

# Importing file extensions from environment variables
video_filetypes = env_var_to_list("VIDEO_FILETYPES")
report_filetypes = env_var_to_list("REPORT_FILETYPES")

# Creating glob expressions for each list
video_glob_expression = create_glob_expression(video_filetypes)
report_glob_expression = create_glob_expression(report_filetypes)

# Combining both lists to create a glob expression for all file types
combined_filetypes = video_filetypes + report_filetypes
combined_glob_expression = create_glob_expression(combined_filetypes)

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

    'admin_interface',
    'flat_responsive',  # optional for django-admin-interface
    'flat',  # optional for django-admin-interface
    'colorfield',  # required for django-admin-interface

    "content_management.apps.ContentManagementConfig",
    "agl_monitor_app.apps.AglMonitorAppConfig",
    "case_merger.apps.CaseMergerConfig",
    "data_collector.apps.DataCollectorConfig",
    "report_processor.apps.ReportProcessorConfig",
    "data_validation.apps.DataValidationConfig",
    "video_processor.apps.VideoProcessorConfig",
    "django_redis",
    "django_celery_beat",
    "django_celery_results",
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

