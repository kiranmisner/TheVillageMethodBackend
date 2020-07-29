
from .common import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_l-c(gs+#_zf4v#cs!0mzqegv=gc2wa(bgs3b6)-vj5dt0^ne8'


ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


DATABASES = {

    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'thevillagemethod',
        'USER': 'thevillagemethod',
        'PASSWORD': 'thevillagemethod',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}