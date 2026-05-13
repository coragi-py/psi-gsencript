import os
from dotenv import load_dotenv
from pathlib import Path
from django.contrib.auth.hashers import Argon2PasswordHasher
import dj_database_url

# Valores baseados nas recomendações da RFC9106 e OWASP
class CustomArgon2Hasher(Argon2PasswordHasher):
  time_cost = 2 # Numero de iterações sobre a memoria
  memory_cost = 65536 # 64mb utilizados na memoria para inviabilizar ataques por hardware
  parallelism = 1 # Numero de threads em paralelo

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/


SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG') == 'True'
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'gsencript.local']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Apps (Microsserviços modulares)
    'accounts',
    'authentication',
    'audit',
    'recovery',
    'lgpd',
    'vault',

    # Bibliotecas de terceiros
    'axes', # Proteção contra força bruta
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600, # Persistência de conexões para melhorar performance
        conn_health_checks=True, # Verificação de saúde das conexões para evitar conexões inválidas
    )
}

# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_USER_MODEL = 'accounts.User'

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

AUTHENTICATION_BACKENDS = [
  'axes.backends.AxesBackend',
  'django.contrib.auth.backends.ModelBackend',
]

PASSWORD_HASHERS = [
    'core.settings.CustomArgon2Hasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]

# Configuração de Sessão item 1.9
SESSION_COOKIE_AGE = 1800  # 30 minutos em segundos
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Configuração do bloqueio
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 0.25 # 15 minutos (em horas)
AXES_LOCK_OUT_AT_FAILURE_LIMIT = True

# Configurações de segurança de transporte
SECURE_SSL_REDIRECT = False # Em produção, deve ser True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = False # Em produção, deve ser True
CSRF_COOKIE_SECURE = False # Em produção, deve ser True
# HSTS é uma política de segurança que instrui os navegadores a se comunicarem apenas por HTTPS. O valor é definido para 1 ano (em segundos) para garantir que os navegadores mantenham essa política por um período prolongado.
SECURE_HSTS_SECONDS = 31536000 # 1 ano em segundos
SECURE_HSTS_INCLUDE_SUBDOMAINS = True # Incluir subdomínios na política HSTS para garantir que todas as partes do site sejam protegidas
SECURE_HSTS_PRELOAD = True #


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
  BASE_DIR / "static",
  ]
STATIC_ROOT = BASE_DIR / "staticfiles"