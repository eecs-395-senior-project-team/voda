from .base import *
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False
SECRET_KEY = env('DJANGO_SECRET_KEY', default='g*j^js4pj!$m2f-&eh2r7lv)&sbzskb=506ks0s&&x+9qo$(2x')

