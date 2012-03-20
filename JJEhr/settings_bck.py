#-*- coding: UTF-8 -*-
import os

DEBUG = False

TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

ADMINS = (
# ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db/jjehr_course.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',

        },
    # 'production': {
    #     'ENGINE': 'django.db.backends.mysql', #设置为mysql数据库
    #     'NAME': 'jjehr',
    #     'USER': 'root',
    #     'PASSWORD': '123456',
    #     'HOST': '',
    #     'PORT': '',
    #     }
}

TEMPLATE_STRING_IF_INVALID = ''

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

DEFAULT_CHARSET = 'utf-8'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = './courseware'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Exdamples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    "./static/lesson",
    "./static",
    "./static/yui",
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    )

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    )

# Make this unique, and don't share it with anybody.
SECRET_KEY = '_!%w_nr**%6088+d8-0_v)96@w$)a$18yhi3y20mf!dnlzh4bu'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    )

ROOT_URLCONF = 'JJEhr.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'template'),
    # "./template"
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    )

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #课程模块
    'backoffice',
    'lesson',

    'django.contrib.admin',

    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    )

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': DEBUG,
    'handlers': {
        'mail_admins': {
            'level': 'DEBUG',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            },
        },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'DEBUG',
            'propagate': DEBUG,
            },
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': DEBUG,
            'level': 'DEBUG',
            },
        }
}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'username@gmail.com'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_USE_TLS = True
EMAIL_SUBJECT = ""
EMAIL_BODY = r""