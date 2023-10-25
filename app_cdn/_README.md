# app_cdn (v1.0.0)
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
MEDIA_URL = 'cdn/'

if DEBUG:
    STATIC_ROOT = 'staticfiles/'
    MEDIA_ROOT = 'mediafiles/'
else:
    STATIC_ROOT = '/vol/web/static/'
    MEDIA_ROOT = '/vol/web/media/'

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# This reserved names are not allowed for cdn projects
CDN_EXCLUDED_NAMES = [
    'sitefiles',
    'sitesfiles',
]
```

**_project.urls.py**
```python
from django.conf import settings
from django.conf.urls.static import static

urlspattern = [
    # ...
    path('app_cdn/', include('app_cdn.urls', namespace="cdn")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

```

nginx config
```
# ...
    location /cdn {
        alias /vol/static/media;
    }

```

Add a link somewhere in your project:
`<a href="{% url 'cdn:home' %}"></a>`
