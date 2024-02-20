# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

from .default_paths import (
    BASE_DIR,
    PSEUDO_DB_PATH,
    PROCESSED_DB_PATH
)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'PseudoDb': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': f'{PSEUDO_DB_PATH}.sqlite3',
    }
}

# Example database router
class PseudoDbRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'endoreg_db':
            return 'PseudoDb'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'endoreg_db':
            return 'PseudoDb'
        return 'default'

DATABASE_ROUTERS = [
    'endoreg_client_manager.settings.database.PseudoDbRouter'
]

