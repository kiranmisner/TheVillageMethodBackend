"""
Summary:
    Represents the development settings for this project. This file is intended to be used (in conjunction with
    common.py) as the development settings ONLY. This file should never be used for production purposes.
"""
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
    },
    'salesforce': {
        'ENGINE': 'salesforce.backend',
        'CONSUMER_KEY': '3MVG9jBOyAOWY5bX1guqUGLubgfbOz6pig5FWe_DxbQEIpCgJ0EAcO4uGqr9HGvycTLlDEkJwJrfzQqqpRe3R',
        'CONSUMER_SECRET': 'D7D6456030FA54E96D6E2ED786DE953E010B397EA350DD9A1E11E9466A723E64',
        'USER': 'kiran.misner@gmail.com',
        'PASSWORD': 'codeforgood123eMTXXg68orZsNFcTZvZ1Byqc6',
        'HOST': 'https://test.salesforce.com',
    }
}

DATABASE_ROUTERS = [
    "salesforce.router.ModelRouter"
]
