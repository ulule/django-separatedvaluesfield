import django

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

SITE_ID = 1
DEBUG = True

INSTALLED_APPS = [
    'separatedvaluesfield.tests',
]

SECRET_KEY = 'blabla'

if django.VERSION <= (1, 6):
    TEST_RUNNER = 'discover_runner.DiscoverRunner'
