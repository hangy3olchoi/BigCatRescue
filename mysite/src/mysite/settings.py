from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gj_oaxhff_^fhitiqoyjsd(%nw+cak85dtjf1=gdq*zt^9b6kz'

# SECURITY WARNING: don't run with debug turned on in production!

# 'DEBUG'가 True라면, 개발모드, False면 운영모드
# 운영모드인 경우 'ALLOWED_HOSTS' 리스트에 반드시 서버의 ip 혹은 도메인을 지정해야 함
# 개발모드인 경우는 'ALLOWED_HOSTS' 리스트에 값을 넣지 않아도 'localhost','127.0.0.1'로 간주.
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
# 새로운 앱이 만들어 지면 이 자리에 등록해야 함
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bookmark.apps.BookmarkConfig',
    'blog.apps.BlogConfig',
    'taggit.apps.TaggitAppConfig',
    'taggit_templatetags2',
    'polls.apps.PollsConfig',
    'photo.apps.PhotoConfig',
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

# 프로젝트 템플릿 파일(mvt 패턴)이 위치할 디렉토리를 지정 - 장고의 Model Viewer Templates == 스프링의 Model Viewer Controller
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # "os.path.join(BASE_DIR), 'templates'" 이 부분 입력, 'templates' 임의로 변경 가능, 'os' import 해야함.
            # 'BASE_DIR'는 프로젝트 최상의 폴더를 의미.('src' 폴더)
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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

LANGUAGE_CODE = 'ko-kr' # 'en-us'-> 'ko-kr'로 수정

TIME_ZONE = 'Asia/Seoul' # 'UTC' -> 'Asia/Seoul'로 수정

USE_I18N = False

USE_L10N = True

# 타임존 사용여부를 결정
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# Django에서의 Static의 의미 - 웹사이트를 개발하는 과정에서 저장한 자료
# 'STATIC_URL = '에 경로를 지정해 줘야 함.
STATIC_URL = '/static/'

# 우선적으로 사용할 statics 임의의 경로(필요시 지정)
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# 'MEDIA_URL' 'Media'의 의미 - 사용자가 웹 어플리케이션에 업로드한 파일
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 대소문자를 구분하지 않겠다.
TAGGIT_CASE_INSENSITIVE = True
# 댓글의 글자수를 50자 이내로 제한.
TAGGIT_LIMIT = 50

DISQUS_SHORTNAME = 'chgmysite'
DISQUS_MY_DOMAIN = 'http://192.168.0.24'

#LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
