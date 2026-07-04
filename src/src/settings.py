import os
from pathlib import Path
from decouple import config
from django.utils.translation import gettext_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
# Demo fallback so the prototype boots without a real secret configured.
SECRET_KEY = config('SECRET_KEY', default='django-insecure-demo-key-not-for-real-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# Vercel automatically sets VERCEL_URL to the deployment's own domain.
VERCEL_URL = os.environ.get('VERCEL_URL', '')

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost 127.0.0.1 .vercel.app').split()
if VERCEL_URL and VERCEL_URL not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(VERCEL_URL)

CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='https://*.vercel.app').split()
if VERCEL_URL and f'https://{VERCEL_URL}' not in CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS.append(f'https://{VERCEL_URL}')

# Custom user model
AUTH_USER_MODEL = 'core.User'

# Groq ai
GROQ_API_KEY = config('GROQ_API_KEY', default='')
GROQ_REWRITE_LIMIT = 4
GROQ_CACHE_TIMEOUT = 86400

# Demo mode: without a real email provider configured, don't force email
# verification on signup since verification emails would go nowhere visible.
BREVO_API_KEY = config('BREVO_API_KEY', default='')

# Allauth

ACCOUNT_SIGNUP_FIELDS = [
    'email*',
    'password1*',
    'password2*',
]
ACCOUNT_FORMS = {
    'signup': 'core.forms.SignupForm',
}
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory' if BREVO_API_KEY else 'optional'
ACCOUNT_LOGIN_METHODS = {'email'}
SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_PREVENT_ENUMERATION = False

ACCOUNT_ADAPTER = 'core.adapters.AccountAdapter'
SOCIALACCOUNT_ADAPTER = 'core.adapters.SocialAccountAdapter'
SOCIALACCOUNT_STORE_TOKENS = True

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
            'https://www.googleapis.com/auth/youtube.readonly'
        ],
        'AUTH_PARAMS': {
            "access_type": "offline",
            "prompt": "consent",
        },
        'OAUTH_PKCE_ENABLED': True,
    },
    "discord": {
        "SCOPE": [
            "identify",
            "guilds",
        ],
    }
}


LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',

    # ======================
    # libs
    # ======================

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'auditlog',
    'django_filters',
    'django_tasks',
    'anymail',

    # ======================
    # Oauth providers
    # ======================

    'allauth.socialaccount.providers.google',

    # ======================
    # apps connection
    # ======================

    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.instagram',
    'allauth.socialaccount.providers.twitch',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.twitter_oauth2',
    'allauth.socialaccount.providers.discord',
    'allauth.socialaccount.providers.linkedin_oauth2',


    # ======================
    # apps
    # ======================
    'src.services',
    'core',
    'company',
    'job',
    'message',
    'portfolio',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'src.middleware.UserLanguageMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'auditlog.middleware.AuditlogMiddleware'
]

ROOT_URLCONF = 'src.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


WSGI_APPLICATION = 'src.wsgi.application'


# Database

# Demo fallback: use SQLite in /tmp (the only writable path on Vercel's
# serverless filesystem) when no real Postgres credentials are configured.
DB_HOST = config('DB_HOST', default='')
if DB_HOST:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default=''),
            'USER': config('DB_USER', default=''),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': DB_HOST,
            'PORT': config('DB_PORT', default='5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/tmp/db.sqlite3',
        }
    }

# Background task
TASKS = {
    "default": {
        "BACKEND": "django_tasks.backends.immediate.ImmediateBackend"
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


# Internationalization

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LANGUAGES = [
    ('en', gettext_lazy('English')),
    ('de', gettext_lazy('German')),
    ('fr', gettext_lazy('French')),
    ('ja', gettext_lazy('Japanese')),
    ('ko', gettext_lazy('Korean')),
    ('pt', gettext_lazy('Portuguese')),
    ('hi', gettext_lazy('Hindi')),
    ('ur', gettext_lazy('Urdu')),
    ('es', gettext_lazy('Spanish')),
]

LOCALE_PATHS = (
    BASE_DIR / 'locale',
)

# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static",]
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'


INTERNAL_IPS = [
    '127.0.0.1',
]

# Cache

CACHE_VIEWS_TIMEOUT = {
    'CompanyView': 60 * 15
}


if DEBUG:

    # ======================
    # Caution :: these settings only work in dev mode
    # ======================

    INSTALLED_APPS += [
        'debug_toolbar',
    ]
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

    MEDIA_ROOT = BASE_DIR / 'media'
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = BASE_DIR / 'emails'
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.history.HistoryPanel',
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.alerts.AlertsPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.community.CommunityPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
    ]

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'cache',
        }
    }
else:
    # Serverless filesystem is read-only except /tmp, and collectstatic
    # hasn't run at build time, so use the no-manifest whitenoise storage
    # (it doesn't require a pre-built manifest to resolve {% static %} URLs).
    STATIC_ROOT = Path('/tmp/staticfiles')
    STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

    CLOUD_NAME = config('CLOUD_NAME', default='')
    if CLOUD_NAME:
        CLOUDINARY_STORAGE = {
            'CLOUD_NAME': CLOUD_NAME,
            'API_KEY': config('CLOUDINARY_API_KEY', default=''),
            'API_SECRET': config('CLOUDINARY_API_SECRET', default=''),
        }
        default_storage_backend = "cloudinary_storage.storage.MediaCloudinaryStorage"
    else:
        # Demo fallback: no Cloudinary account configured, store media in /tmp.
        # Uploaded files won't persist across cold starts or be publicly served.
        default_storage_backend = "django.core.files.storage.FileSystemStorage"
        MEDIA_ROOT = Path('/tmp/media')

    STORAGES = {
        "default": {
            "BACKEND": default_storage_backend,
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
        },
    }
    # Cache

    REDIS_CACHE_URL = config('REDIS_CACHE_URL', default='')
    if REDIS_CACHE_URL:
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.redis.RedisCache',
                'LOCATION': REDIS_CACHE_URL,
            }
        }
    else:
        # Demo fallback: no Redis configured, use local in-process cache.
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            }
        }

    if BREVO_API_KEY:
        EMAIL_BACKEND = "anymail.backends.brevo.EmailBackend"
        ANYMAIL = {
            "BREVO_API_KEY": BREVO_API_KEY,
        }
    else:
        # Demo fallback: no email provider configured, just log emails.
        EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DEFAULT_FROM_EMAIL = config('EMAIL_HOST_USER', default='demo@example.com')
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
    SECURE_SSL_REDIRECT = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'