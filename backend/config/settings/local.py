from .base import *
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
SECRET_KEY = env('DJANGO_SECRET_KEY', default='gedqrgbjf6xf^bl^7%riw)euc3_13!2*f6=d=i(kw=zcdbfbxi')
ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
]
