"""
Django settings for config project.
TFG Idealista - Álvaro Carrera
Configuración para desarrollo y producción
"""

from pathlib import Path
import os
import dj_database_url
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ SEGURIDAD MEJORADA
SECRET_KEY = config('SECRET_KEY', default='django-insecure-%h92(&0b4af(@i5o^d29it50_q(t##c@x&m#&x*ay6_@q(@ch)')

# ✅ DEBUG DINÁMICO (False en producción)
DEBUG = config('DEBUG', default=True, cast=bool)

# ✅ HOSTS PERMITIDOS CONFIGURABLES
if DEBUG:
    ALLOWED_HOSTS = ['*']  # Solo en desarrollo
else:
    ALLOWED_HOSTS = config(
        'ALLOWED_HOSTS',
        default='tfg-idealista-backend.onrender.com,localhost,127.0.0.1'
    ).split(',')

# ✅ APLICACIONES INSTALADAS CORREGIDAS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'corsheaders',  # ✅ AGREGADO
    
    # Local apps
    'src',
]

# ✅ MIDDLEWARE CORREGIDO CON CORS Y WHITENOISE
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # ✅ AGREGADO - debe ir primero
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ AGREGADO - para archivos estáticos
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'

# ✅ DATABASE CONFIGURACIÓN PARA DESARROLLO Y PRODUCCIÓN
if 'DATABASE_URL' in os.environ:
    # Producción con PostgreSQL en Render
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
else:
    # Desarrollo con SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ✅ CONFIGURACIÓN REGIONAL
LANGUAGE_CODE = 'es-es'  # Español de España
TIME_ZONE = 'Europe/Madrid'  # Zona horaria de Madrid

USE_I18N = True
USE_TZ = True

# ✅ ARCHIVOS ESTÁTICOS PARA PRODUCCIÓN
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ✅ CONFIGURACIÓN DE WHITENOISE PARA ARCHIVOS ESTÁTICOS
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ✅ CONFIGURACIÓN DE CORS PARA VERCEL
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True  # Solo en desarrollo
else:
    CORS_ALLOWED_ORIGINS = [
        "https://tfg-idealista-frontend.vercel.app",
        "https://tfg-alvaro-carrera-idealista.vercel.app",
        "http://localhost:8501",  # Streamlit local
        "http://127.0.0.1:8501",
    ]

# ✅ HEADERS CORS PERMITIDOS
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# ✅ MÉTODOS HTTP PERMITIDOS
CORS_ALLOWED_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# ✅ CONFIGURACIÓN DE DRF (Django REST Framework)
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Permitir acceso público a la API
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,  # Páginas de 100 propiedades
}

# ✅ CONFIGURACIÓN DE SEGURIDAD PARA PRODUCCIÓN
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

# ✅ CONFIGURACIÓN DE LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# ✅ CONFIGURACIÓN ESPECÍFICA DEL PROYECTO TFG
# Rutas para modelos ML y datos
ML_MODELS_PATH = BASE_DIR / 'data' / 'models'
DATA_PATH = BASE_DIR / 'data'

# Configuración de cache (opcional)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
