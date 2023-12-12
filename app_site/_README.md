# app_site (v1.0.0)

# DESCRITPION

This app allows to upload very quicly packs of media files (in zip) to serve it immediatly
at the uri /site/<project_name>
(an index.html file must be in the directory)

# Installation

Copy / Paste app_site in your project.

**settings.py**
```python
INSTALLED_APPS = [
    # ...
    'app_site',
]

STATICFILES_DIRS = ['static/', ]

STATIC_URL = 'static/'
MEDIA_URL = 'media/'

if DEBUG:
    STATIC_ROOT = 'staticfiles/'
    MEDIA_ROOT = 'mediafiles/'
else:
    # according to the _deployment config
    STATIC_ROOT = '/vol/web/static/'
    MEDIA_ROOT = '/vol/web/media/'
```

**urls.py**
```python
urlpatterns = [
    # ...
    path('app_site/', include('app_site.urls', namespace="site")),
]
```

Add a link to the app somewhere
```html
<a href="{% url 'site:home' %}">
    sites
</a>
```


# Nginx config for production

Add this in your nginx config
```
    location /site {
        alias /vol/static/media/sitefiles;
    }
```
**Note** that this url will not be available in **dev mode**, just use directly the 'index.html' of your static sites instead of the 'site/[project_name]' url.
