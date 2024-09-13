from datetime import timedelta
from pathlib import Path
import environ  # 환경 변수 관리를 위한 django-environ 사용

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 환경 변수 설정을 위한 django-environ 초기화
env = environ.Env()

env_path = BASE_DIR / ".env"
if env_path.exists():
    environ.Env.read_env(env_file=str(env_path))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY", default="your-secret-key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=True)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

# Application definition
INSTALLED_APPS = [
    # Django 기본 앱들
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 로컬 앱들
    "users",
    # 서드 파티 앱들
    "rest_framework",
    'rest_framework_simplejwt.token_blacklist',
    "debug_toolbar",
    "django_bootstrap5",
    "sorl.thumbnail",
    "widget_tweaks",
    "django_ckeditor_5",
    "mptt",
    "django_json_widget",
    "storages",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # CORS 설정을 위한 미들웨어 추가
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "navyProjectBE.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "navyProjectBE.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASES = {
    "default": env.db("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTH_USER_MODEL = 'users.customuser'  # Custom User 모델 설정

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = env.str("LANGUAGE_CODE", default="ko-kr")
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True

# AWS S3
AWS_ACCESS_KEY_ID = env.str('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ACCESS_KEY')
AWS_REGION_NAME = env.str('AWS_REGION_NAME', default='ap-northeast-2')
AWS_STORAGE_BUCKET_NAME = env.str('AWS_STORAGE_BUCKET_NAME')

# Static files (CSS, JavaScript, Images)
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# AWS S3 settings for static and media files
DEFAULT_FILE_STORAGE = env.str('DEFAULT_FILE_STORAGE', default='storages.backends.s3boto3.S3Boto3Storage')
STATICFILES_STORAGE = env.str('STATICFILES_STORAGE', default='storages.backends.s3boto3.S3Boto3Storage')



# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django Debug Toolbar
INTERNAL_IPS = env.list("INTERNAL_IPS", default=["127.0.0.1"])

# CORS 설정
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

# PortOne 설정
PORTONE_SHOP_ID = env.str("PORTONE_SHOP_ID", default="")
PORTONE_API_KEY = env.str("PORTONE_API_KEY", default="")
PORTONE_API_SECRET = env.str("PORTONE_API_SECRET", default="")

# Webhook IPS 설정
ALLOWED_WEBHOOK_IPS = env.list("ALLOWED_WEBHOOK_IPS", default=[])

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=3650),  # 10년 유효기간 설정
    'REFRESH_TOKEN_LIFETIME': timedelta(days=3650),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,  # Django의 SECRET_KEY를 사용
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# CKEditor 설정
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "link",
            "bulletedList",
            "numberedList",
            "blockQuote",
            "imageUpload",
        ],
    },
}