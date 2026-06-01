import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory (adjusted for modular settings structure: music_app/settings/base.py)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Core application secret key
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-)nq#c_as78zm+gf0aa@$_)5eq4mum^v8@idd07m8km#0)u4e=9')

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')

# Application definition
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'cloudinary',
    'cloudinary_storage',

    'orrin.apps.OrrinConfig',
    'users.apps.UsersConfig',
    'library.apps.LibraryConfig',
    'feed.apps.FeedConfig',
    'chat.apps.ChatConfig',
    'stats.apps.StatsConfig',

    'rest_framework',
    'corsheaders',
    'drf_spectacular',
    'drf_spectacular_sidecar',
]

ASGI_APPLICATION = 'music_app.asgi.application'

# Redis channel layer — host is overridden in production.py via REDIS_URL
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [os.environ.get('REDIS_URL', 'redis://redis:6379')],
        },
    },
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'music_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'music_app.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    'users.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# Swagger/Redoc settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'Orrin API',
    'DESCRIPTION': 'API documentation for Orrin music and social platform',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
    'TAGS': [
        {'name': 'Auth',          'description': 'Registration, login, JWT tokens'},
        {'name': 'Users',         'description': 'User profiles, follow/unfollow'},
        {'name': 'Tracks',        'description': 'Music tracks'},
        {'name': 'Artists',       'description': 'Artists and bands'},
        {'name': 'Playlists',     'description': 'User playlists'},
        {'name': 'Library',       'description': 'Liked tracks, followed artists, saved albums'},
        {'name': 'History',       'description': 'Listening history'},
        {'name': 'Feed',          'description': 'Social feed, posts, comments, likes'},
        {'name': 'Chat',          'description': 'Direct messages'},
        {'name': 'Social',        'description': 'Friends activity'},
        {'name': 'Stats',         'description': 'Personal listening statistics'},
        {'name': 'Notifications', 'description': 'In-app notifications'},
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# Email (dev: console backend; prod: replace with SMTP)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "noreply@orrin.app"

# URL of the frontend — used in password reset links
PASSWORD_RESET_FRONTEND_URL = os.environ.get(
    "PASSWORD_RESET_FRONTEND_URL", "http://localhost:5173"
)