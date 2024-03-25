LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'django_logs.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'celery': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'celery.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'filepaths': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'celery': {
            'handlers': ['celery'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
