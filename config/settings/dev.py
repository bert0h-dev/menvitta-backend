from .base import *

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
  }
}

# Development database (PostgreSQL local)
# DATABASES = {
#   'default': {
#     'ENGINE': 'django.db.backends.postgresql',
#     'NAME': os.getenv('POSTGRES_DB', 'menvitta_db'),
#     'USER': os.getenv('POSTGRES_USER', 'menvitta_user'),
#     'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'password'),
#     'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
#     'PORT': os.getenv('POSTGRES_PORT', '5432'),
#   }
# }