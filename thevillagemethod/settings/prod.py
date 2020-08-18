#
# These are settings for Heroku Production Environment
#

from .common import *

import dj_database_url


# We don't want any debug warnings giving
# away unnecessary information to attackers

DEBUG=True

# We grab the secret key from the environment because it is
# our production key and no can know it

SECRET_KEY = os.environ.get('SECRET_KEY')

# We redirect any http requests to their  https equivalents

SECURE_SSL_REDIRECT = True

ALLOWED_HOSTS = ["the-village-method-app.herokuapp.com"]


# We let the dj_database_url package pull the database info from heroku
# https://github.com/kennethreitz/dj-database-url

DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'), conn_max_age=600, ssl_require=True),
    'salesforce': {
        'ENGINE': 'salesforce.backend',
        'CONSUMER_KEY': os.environ.get('CONSUMER_KEY'),                # 'client_id'   in OAuth2 terminology
        'CONSUMER_SECRET': os.environ.get('CONSUMER_SECRET'),             # 'client_secret'
        'USER': os.environ.get('SALESFORCE_USER'),
        'PASSWORD': os.environ.get('SALESFORCE_PW_TOKEN'),
        'HOST': 'https://test.salesforce.com',
    }
}

DATABASE_ROUTERS = [
    "salesforce.router.ModelRouter"
]

# DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
