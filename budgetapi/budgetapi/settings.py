"""
Django settings for budgetapi project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    'BUDGETAPI_SECRET_KEY',
    "django-insecure-*(l7q3av)0!lq)^g#3!++%$l7=67@q5b+qp(a(4n%!a1l9^_-o"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if os.getenv('BUDGETAPI_ALLOWED_HOSTS') else True

# NOTE: https://www.divio.com/blog/django-allowed-hosts-explained/
ALLOWED_HOSTS: list[str] = (
    # provide a comma delimited list of allowed hosts 
    os.getenv('BUDGETAPI_ALLOWED_HOSTS').replace(' ', "").split(',')
    if os.getenv('BUDGETAPI_ALLOWED_HOSTS')
    else []
 )


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "rest_framework",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "corsheaders",
    "django_filters",
    "rest_framework.authtoken",
    "dj_rest_auth.registration",
    "dj_rest_auth",
    "users.apps.UsersConfig",
    "categories.apps.CategoriesConfig",
    "transactions.apps.TransactionsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "budgetapi.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
        },
    },
]

CORS_ALLOWED_ORIGINS = (
    os.getenv('BUDGETAPI_CORS_ALLOWED_ORIGINS').replace(' ', "").split(',')
    if os.getenv('BUDGETAPI_CORS_ALLOWED_ORIGINS')
    else []
 )

# NOTE: https://github.com/adamchainz/django-cors-headers#csrf-integration
CSRF_TRUSTED_ORIGINS = (
    os.getenv('BUDGETAPI_CSRF_TRUSTED_ORIGINS').replace(' ', "").split(',')
    if os.getenv('BUDGETAPI_CSRF_TRUSTED_ORIGINS')
    else [
        f"http://localhost:{os.getenv('BUDGETAPI_NGINX_PORT', '1337')}"
    ]
 )


WSGI_APPLICATION = "budgetapi.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("BUDGETAPI_POSTGRES_DB", "budgetapi"),
        "USER": os.getenv("BUDGETAPI_POSTGRES_USER", "budgetapi"),
        "PASSWORD": os.getenv("BUDGETAPI_POSTGRES_PASSWORD", "budgetapi"),
        "HOST": os.getenv("BUDGETAPI_POSTGRES_HOST") or "postgres" or "localhost",
        "PORT": os.getenv("BUDGETAPI_POSTGRES_PORT", "5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.NumericPasswordValidator"
        ),
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "budgetapi.renderers.MyBrowsableAPIRenderer",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"  # new
SITE_ID = 1  # new

STATIC_ROOT = BASE_DIR / "staticfiles"