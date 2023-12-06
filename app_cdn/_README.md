# app_cdn (v2.0.0)
namespace: 'cdn'

Adds a cdn to the site. Classic views, can be included in a SPA application throught _adminplus.

# Installation

**settings.py**
```python
INSTALLED_APPS = [
    # ...
    'app_cdn',
]

# Statics and CDN
STATICFILES_DIRS = ['static/', ]

STATIC_URL = 'static/'
MEDIA_URL = 'media/'

if DEBUG:
    STATIC_ROOT = 'staticfiles/'
    MEDIA_ROOT = 'mediafiles/'
else:
    STATIC_ROOT = '/vol/web/static/'
    MEDIA_ROOT = '/vol/web/media/'

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

```

**_project.urls.py**
```python
urlspattern = [
    # ...
    path('app_cdn/', include('app_cdn.urls', namespace="cdn")),
]
```

Add a link to the app somewhere

```html
<a href="{% url 'cdn:home' %}">
    cdn
</a>
```

# nginx config
```
# ...
    location /cdn {
        alias /vol/static/media/cdn;
    }
```
