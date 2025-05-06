import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Carga el archivo .env
load_dotenv(dotenv_path=BASE_DIR / '.env')

# Security
SECRET_KEY = os.getenv('SECRET_KEY', 'unsafe-secret-key')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1").split(",")

# Version de la API
API_VERSION = "1.0.0"

# Installed apps
INSTALLED_APPS = [
    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Dependencies
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'drf_spectacular',
    'django_filters',

    # Apps locales
    'core',
    'accounts',
    'authentication',
]

# Middleware
MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',

  # Middleware para permitir peticiones de backend a frontend
  "corsheaders.middleware.CorsMiddleware",

  'django.middleware.common.CommonMiddleware',  
  'django.middleware.csrf.CsrfViewMiddleware',

  # 👇 Middleware que dependan de la authentication van despues de este
  'django.contrib.auth.middleware.AuthenticationMiddleware',

  # Middleware para actualizar la actividad del usuario
  'core.middleware.updateRequestInfo.UpdateUserInfoMiddleware',
  # Middleware para obtener el idioma del usuario
  'core.middleware.setLanguage.LanguageFromUserMiddleware',
  # Middleware para guardar el usuario del request
  'core.middleware.updateRequestInfo.ThreadLocalUserMiddleware',
  
  # Para hacer traduccion de los textos
  'django.middleware.locale.LocaleMiddleware',

  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL config
ROOT_URLCONF = 'config.urls'

# Templates
TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {
      'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
      ],
    },
  },
]

# WSGI / ASGI
WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# Database → se sobreescribe en dev.py y prod.py
DATABASES = {}

# Internationalization
LANGUAGE_CODE = 'es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
  ('es', 'Español'),
  ('en', 'English'),
]

LOCALE_PATHS = [
  os.path.join(BASE_DIR, 'locale'),
]

# Permisos definidos por defecto
PROJECT_PERMISSION_APPS = [
  'auth',
  'accounts',
  'core',
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Toma por default el usuario del modelo accounts
AUTH_USER_MODEL = 'accounts.User'

# Configuracion de Rest Framework
REST_FRAMEWORK = {
  'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
  'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication', ),
  'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated', ),
  'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
  'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
  'PAGE_SIZE': 10,
  'EXCEPTION_HANDLER': 'core.utils.handlers.custom_exception_handler',
  'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S %Z',
}

# Configuracion JWT
SIMPLE_JWT = {
  'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
  'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
  'ROTATE_REFRESH_TOKENS': False,
  'BLACKLIST_AFTER_ROTATION': True,
  
  'AUTH_HEADER_TYPES': ('Bearer',),
  'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),

  'TOKEN_BLACKLIST_ENABLED': True,
}

# Cors Headers authorization
# Se le coloca las urls del localhost que podra hacer peticiones
# CORS_ALLOWED_ORIGINS = ['http://localhost:5174']

# Documentation settings
# https://drf-spectacular.readthedocs.io/en/latest/settings.html
SPECTACULAR_SETTINGS = {
  'TITLE': 'MenVitta Backend',
  'DESCRIPTION': 'Bienvenido al backend del sistema MenVitta, una plataforma enfocada en la gestión médica de citas y pacientes.',
  'VERSION': API_VERSION,
  'POSTPROCESSING_HOOKS': [
    'core.base.hooks.add_default_response_envelope',
  ],
}