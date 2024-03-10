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

class EndoregDbRouter:
    """
    A router to control all database operations on models in the
    endoreg_db application.
    """

    def db_for_read(self, model, **hints):
        """Send all read operations on endoreg_db app models to `PseudoDb`."""
        if model._meta.app_label == 'endoreg_db':
            return 'PseudoDb'
        return 'default'

    def db_for_write(self, model, **hints):
        """Send all write operations on endoreg_db app models to `PseudoDb`."""
        if model._meta.app_label == 'endoreg_db':
            return 'PseudoDb'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """Allow relations if a model in endoreg_db is involved."""
        if obj1._meta.app_label == 'endoreg_db' or \
           obj2._meta.app_label == 'endoreg_db':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure that the endoreg_db app's models get created on the `PseudoDb`."""
        if app_label == 'endoreg_db':
            return db == 'PseudoDb'
        return None


DATABASE_ROUTERS = [
    'endoreg_client_manager.settings.database.EndoregDbRouter'
]

