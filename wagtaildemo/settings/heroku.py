import dj_database_url

from .base import *  # noqa


DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# BASE_URL required for notification emails
BASE_URL = 'http://localhost:8000'

DATABASES = {
    'default': dj_database_url.config(
        default='postgres://postgres@localhost:5432/oscarwagtaildemo'
    )
}


try:
    from .local import *  # noqa
except ImportError:
    pass
