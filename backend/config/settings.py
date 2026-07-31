import os
from pathlib import Path
from datetime import timedelta
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-zq3bzs=j!gib8x2&m6if3f)1+)=^vrjybchd@ytf2z6f5+g2ax'

DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'mentored',
    'payments',
    'school',
]

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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / '../frontend/dist',  # папка со сборкой Vue
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


WSGI_APPLICATION = 'config.wsgi.application'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://localhost:5175",
    "http://127.0.0.1:5175",
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://mentoredgroup.com",
    "https://mentoredgroup.com",
    #""
]
CORS_ALLOW_CREDENTIALS = True

# Мы за nginx-прокси: TLS обрывается на nginx, до Django долетает обычный HTTP.
# Без этой строки request.is_secure() всегда False, и Origin/scheme у Django
# и у браузера расходятся (http vs https).
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Django 4+ на "secure"-запросах сверяет заголовок Origin со списком доверенных
# origin'ов. Без этой настройки POST /admin/login/ с https://mentoredgroup.com
# падает 403 "Origin checking failed - ... does not match any trusted origins."
CSRF_TRUSTED_ORIGINS = [
    'https://mentoredgroup.com',
    'https://www.mentoredgroup.com',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('POSTGRES_HOST', default='db'),
        'PORT': config('POSTGRES_PORT', default='5432'),
    }
}

# Старый sqlite - НЕ удалять файл backend/db.sqlite3, оставлен для отката/справки.
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

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

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'TOKEN_OBTAIN_SERIALIZER': 'mentored.serializers.CustomTokenObtainPairSerializer',
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'mentored.User'

# .env
# Боевые креды Mercado Pago - только через .env, в гит не попадают.
MERCADOPAGO_ACCESS_TOKEN = config('MERCADOPAGO_ACCESS_TOKEN')
MERCADOPAGO_PUBLIC_KEY = config('MERCADOPAGO_PUBLIC_KEY')

# Секрет для проверки заголовка x-signature на вебхуках (Your integrations ->
# приложение -> Webhooks -> Configure notifications -> Secret key). Пока не
# выдан - оставляем пустым, тогда подпись просто не проверяется (см.
# payments/views.py::_verify_mp_signature), но пишется warning в лог.
MERCADOPAGO_WEBHOOK_SECRET = config('MERCADOPAGO_WEBHOOK_SECRET', default='')

# Валюта позиций в preference. ВАЖНО: должна совпадать со страной аккаунта
# Mercado Pago (PEN - Перу), иначе sdk.preference().create() падает с
# ошибкой валидации валюты на стороне Mercado Pago. Покупатель эту валюту
# не выбирает и не может поменять на чекауте - она жёстко привязана к
# стране/валюте продавца в Mercado Pago.
MERCADOPAGO_CURRENCY = config('MERCADOPAGO_CURRENCY', default='PEN')

# Почта для формы обратной связи (страница /contacto). Пока SMTP-креды не
# заданы - EMAIL_HOST_USER пустой, ContactMessageView просто не пытается
# слать письмо (см. mentored/views.py::ContactMessageView), заявка всё равно
# сохраняется в БД и видна в /admin/.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default=EMAIL_HOST_USER)
# Куда падают уведомления о новых заявках с формы контактов.
CONTACT_NOTIFICATION_EMAIL = config('CONTACT_NOTIFICATION_EMAIL', default=EMAIL_HOST_USER)