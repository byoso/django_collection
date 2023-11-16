
# _auth (v1.0.0)

Social network or not, login with allauth 0.58

[Official doc](https://docs.allauth.org/en/latest/index.html)

# Installation

[Official Installation](https://docs.allauth.org/en/latest/installation/quickstart.html)

`pip install django-allauth`

**settings.py**
```python

INSTALLED_APPS = [
    # ...
    '_auth',  # before allauth

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # and some social networks or not
    # (official doc: https://docs.allauth.org/en/latest/installation/quickstart.html)

]

MIDDLEWARE = [
    # ...
    "allauth.account.middleware.AccountMiddleware",
]

# EMAIL (assuming you have a .env file)
if os.environ.get('EMAIL_IS_CONFIGURED', '0') == '1':
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', "localhost")
EMAIL_PORT = os.environ.get('EMAIL_PORT', "25")
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', "email@email.com")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', "testpass1")
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', '0') == '1'
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_SSL', '0') == '1'

AUTH_USER_MODEL = '_auth.User'

# allauth configuration & backends
#allauth backends
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]
# allauth configuration
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT = '/'
ACCOUNT_SIGNUP_REDIRECT_URL = "/"
ACCOUNT_EMAIL_REQUIRED = True  # True if verification is 'mandatory'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # 'mandatory' | 'optional' | 'none'

```

**_project.urls.py**
```python
urlpatterns = [
    # ...
    path('accounts/', include('allauth.urls')),
]
```
Don not forget to makemigrations and migrate.

## add some buttons

**_base.html**
```html

<div class="buttons">
    {% if not user.is_authenticated %}
    <a class="button is-primary" href="{% url 'account_signup' %}">
    <strong>Sign up</strong>
    </a>
    <a class="button is-light" href="{% url 'account_login' %}">
    Log in
    </a>
    {% else %}
    <span class="mr-4">{{ user.username }}</span>

    <a href="{% url 'account_logout' %}" class="button is-danger">Logout</a>
    {% endif %}
</div>
```

# Styling templates

You will find in _auth/templates the folder
- 'account' (you should not need to modify it, but you can)
- 'allauth/elements', that
is the one interesting. Here you can add your style to the elements.

To have a better form control, just modifying the elements 'fields.html' and 'field.html' should be enought.


# Social authentication (example with google)

Each provider needs a scpecific setting

[Official doc](https://docs.allauth.org/en/0.58.0/socialaccount/providers/index.html)


## On [google cloud](https://console.cloud.google.com)

- Create a project and go in 'keys' to get properly a client ID, a client key and an API key according to
the documentation prvided by django-allauth


- Add the social [provider](https://docs.allauth.org/en/0.58.0/installation/quickstart.html) to the installed apps.


**settings.py**
```python

INSTALLED_APPS = [
    # ...
    'allauth.socialaccount.providers.google',
]

```


- Add a social application throught the admin or in the settings.py

**settings.py**
```python
# Provider specific settings (possible to add providers through the admin too)
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': 'xxx',
            'secret': 'xxx',
            'key': 'xxx'
        }
    }
}
```
It just works :) !
