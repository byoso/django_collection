
# Add dotenv to your project

`pip install djang-dotenv`

**manage.py**
```python
import dotenv
# ...
if __name__ == "__name__":
    dotenv.read_dotenv()
    main()
```

# Add the deployment files to the project

Copy/paste the files in COPY_TO_ROOT into the root directory of your project.

- check the 'dependencies.txt', then `pip install -r dependencies.txt` and `pip freeze > requirements.txt`
- The deployment files provide a .env-sample file, use it to create your .env file, but you MUST .gitignore the .env
## Adapt the deployment files to your project name:

- in `scripts/run.sh` :
```sh
# ...
uwsgi --socket :9000 --workers 4 --master --enable-threads --module _project.wsgi
```
change "\_project" to your actual project directory (the one that contains the wsgi.py file).

# Settings.py

Be sure this settings are made properly, according to your project:

**settings.py**
```python
import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'unsafe secret key')

DEBUG = os.environ.get('DEBUG', '0') == '1'

ALLOWED_HOSTS = []
ALLOWED_HOSTS.extend(
    filter(
        None,  # remove empty strings from the list
        os.environ.get('ALLOWED_HOSTS', '').split(',')
    )
)
# necessary for admin login
CSRF_TRUSTED_ORIGINS = [
    f"https://{os.environ.get('DOMAIN')}",
    f"https://www.{os.environ.get('DOMAIN')}",
]

INSTALLED_APPS = [
    # ...
    '_deployment',
]

# Database - DO NOT USE 'postgres' user in prod, set another one in .env
if os.environ.get('USE_POSTGRES', '1') == '1':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB', 'django_pg_db'),
            'USER': os.environ.get('POSTGRES_USER', 'postgres'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
            'HOST': os.environ.get('POSTGRES_HOST', 'db'),
            'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

STATICFILES_DIRS = ['static/', ]

STATIC_URL = 'static/'
MEDIA_URL = 'media/'
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

if DEBUG:
    STATIC_ROOT = 'staticfiles/'
    MEDIA_ROOT = 'mediafiles/'
else:
    STATIC_ROOT = '/vol/web/static/'
    MEDIA_ROOT = '/vol/web/media/'

# EMAIL
if os.environ.get('EMAIL_IS_CONFIGURED', '0') == '1':
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', "localhost")
EMAIL_PORT = os.environ.get('EMAIL_PORT', "25")
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', "email@email.com")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', "testpass1")
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', '0') == '1'

```

## STATIC_URL & MEDIA_URL

If you want to change their urls, change it both in the settings.py, and in configs/nginx/default-ssl.conf.tpl, just the location, not the volume.

## .env

### for development

To run the project in development mode with `./manage.py runserver`, the .env file must be set with this:

**.env**
```sh
DEBUG=1
USE_POSTGRES=0
```

### for production

Just read each line of the .env file carefully and set them wisely.
