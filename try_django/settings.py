import os
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path

IS_DEV=True

if IS_DEV==False:
    dotenv_path = '/home/jenkins/gammatrades_18thAug20/ssh-key/.env'
    load_dotenv(dotenv_path)
else:
    dotenv_path = Path('.') / '.env'
    #dotenv_path = 'D:/test/.env'
    load_dotenv(dotenv_path)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG')

#ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS')

LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# Application definition

INSTALLED_APPS = [ # components
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'corsheaders',                 # Cross-Origin Resource Sharing (CORS) to prevent API security issues with different domains or ports
    'rest_framework',              # rest framework fot creating GET, POST, PUT, DELETE
    'rest_framework.authtoken',    # for token creation when new user is created (shown at admin page under AUTH TOKEN)
    'storages',
    'six',
    'members',
    'customers',
    'listings',
    #'rest_auth',                  # allows for login/logout at http://127.0.0.1:8000/api/v1/api-auth/login/
    #'django.contrib.sites',       # Returns either the current Site object based on the request (for social authentication via FB, google)
    #'allauth',                    # for social authentication via FB, google
    #'allauth.account',            # for social authentication via FB, google
    #'allauth.socialaccount',      # for social authentication via FB, google
    #'rest_auth.registration',     # allows for registration at http://127.0.0.1:8000/api/v1/api-auth/registration/ (for social authentication via FB, google)

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'try_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')
                ],
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

WSGI_APPLICATION = 'try_django.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

if DEBUG==0:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.postgresql"),
            "NAME": os.environ.get("SQL_DATABASE", "btre_prod"),
            "USER": os.environ.get("SQL_USER", "dbadmin"),
            "PASSWORD": os.environ.get("SQL_PASSWORD", "Romans12:1"),
            "HOST": os.environ.get("SQL_HOST", "localhost"),
            "PORT": os.environ.get("SQL_PORT", "5432")
        }
    }





# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE ="Asia/Singapore"

USE_I18N = True

USE_L10N = True

USE_TZ = True



AUTH_USER_MODEL = 'members.Member'

#need to check how to set this for React


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
}


# Sendgrid SMTP system
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'smilingideas'
EMAIL_PORT = 2525
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_API_KEY')

CORS_ORIGIN_WHITELIST = [

    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1",
    "http://localhost:8000",
    "http://localhost",
    "http://gammatrades.com",
    "https://gammatrades.com",
    "http://www.gammatrades.com",
    "https://www.gammatrades.com"

]

#S3 BUCKETS CONFIG

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')


AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATIC_URL = '/static/'
# directory which django looks start to look for static files when using - {% static 'dir/file_name.css' %}
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
# directory which static file (at STATICFILES_DIRS) will be copied when using - python manage.py collectstatic
STATIC_ROOT= os.path.join(BASE_DIR, 'collectstatic')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  #relative path to saving all media file, can set absolute path ie. MEDIA_ROOT = '/TMP/MEDIA'


