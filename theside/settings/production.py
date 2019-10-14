from .base import *

DEBUG = False
if 'DEBUG' in os.environ:
    DEBUG = 'True' == os.environ['DEBUG']

try:
    from .local import *
except ImportError:
    pass

ALLOWED_HOSTS = [

]

SECRET_KEY = os.environ.get('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USERNAME'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOSTNAME'),
        'PORT': os.environ.get('DB_PORT'),
    }
}
