"""
Django settings for goodfon project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'uec)92b17#1jbl7$c-)@7at=$(qh428a&9_#((=6^ym4!&+q$#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'accounts.com',
]

# Application definition

INSTALLED_APPS = [
    'taggit',
    'taggit_serializer',
    'social_django',
    'dal',
    'dal_select2',

    'main.apps.MainConfig',
    'accounts',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'rest_framework',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'main.middleware.ModeratorOnWorkMiddleware',
]

ROOT_URLCONF = 'goodfon.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [(os.path.join(BASE_DIR, 'templates'))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'goodfon.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        'TIMEOUT': 60,#60 * 60 * 24,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
    }
}

AUTHENTICATION_BACKENDS = (
    'accounts.authentication.EmailAuthBackend',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',  # <--- enable this one
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '809794877796-7k18usfc3vt0nu7skiuh50adgr77q66l.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'p1WTnw_Qnw6GSPox_2STRP88'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/accounts/'
LOGOUT_URL = '/accounts/logout/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

TAGGIT_CASE_INSENSITIVE = True

EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_HOST_USER = '7d13b29f6abc2d'
EMAIL_HOST_PASSWORD = 'd48a53540f7826'
EMAIL_PORT = '2525'


IMAGE_PREVIEW_WIDTH = 500
IMAGE_MAXIMUM_FILESIZE_IN_MB = 15
IMAGE_MINIMUM_DIMENSION = (1024, 1024)
IMAGE_MAXIMUM_COUNT_PER_PAGE = 24
IMAGE_MINIMUM_TAGS = 3
IMAGE_COLUMNS = 4
IMAGE_MINIMUM_PERCENTAGE_OF_DOMINANT_COLORS = 1
SIMILAR_IMAGES_COUNT = 4
DISPLAY_MOST_COMMON_TAGS_COUNT = 10
TAGS_CLOUD_MAX = 24
TAGS_CLOUD_MIN = 16

COLORS = {
    '000000': 'black',
    'ffffff': 'white',
    '808080': 'dark gray',
    'b0b0b0': 'light gray',
    'ff0000': 'red',
    '800000': 'dark red',
    '00ff00': 'green',
    '008000': 'darkgreen',
    '0000ff': 'blue',
    '000080': 'dark blue',
    'ffff00': 'yellow',
    '808000': 'olive',
    'ffa500': 'orange',
    '00ffff': 'cyan',
    'ff00ff': 'magenta',
    '800080': 'purple'
}

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

INTERNAL_IPS = [
    '127.0.0.1',
]

GOOGLE_RECAPTCHA_SECRET_KEY = '6Lecnb0aAAAAAAo5nFN9FA2-lMuZcebcUE3p0jY2'
