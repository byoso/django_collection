# _quick_auth (v1.0.1)

Complete authentication system ready for a SPA or a classic Django project.

It will use a unique username and only one user can have the same email 'verified' at once.

_quick_auth includes both endpoints and the classic views needed to interact with the auth system (mostly confirmation emails).

Only missing a social authentication...

## Installation

pip install:

```sh
django
PyJWT
# if you need DRF
django-rest-framework
```
Then copy/paste the app `_quick_auth` in your django's root directory.

Depending if you want to use _quick_auth with DRF or classic Django, follow
the next instructions.

When you'll be done, remember to makemigrations for _quick_auth and migrate.

## Installation for classic Django

**settings.py**
```python
INSTALLED_APPS = [
    '_quick_auth',
]

# you must have a proper email configuration, for dev let's just say:
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

QUICK_AUTH = {
    'BASE_TEMPLATE': 'you_app/your_base_template.html',
}

```
**urls.py**
```python
urlpatterns = [
    # ...
    path('', include('_quick_auth.urls')),
    # only if you want to try the demo at path '/':
    path('', TemplateView.as_view(template_name='auth/demo.html')),
]

```
Take a look at '_quick_auth/templates/auth/demo.html' to see how you can add the login/signup/logout buttons in your own templates.

**example**
```html

<div class="buttons">
    {% if not user.is_authenticated %}
    <a class="button is-primary" href="{% url 'signup' %}">
        <strong>Sign up</strong>
    </a>
    <a class="button is-light" href="{% url 'login' %}">
        Log in
    </a>
    {% else %}
    <strong class="mr-2">{{ user.username }}</strong>
    <form action="{% url 'logout' %}" method="post">
        {% csrf_token %}
        <button class="button is-warning">
        <strong>Logout</strong>
        </button>
    </form>
    {% endif %}
</div>
```

## Installation for DRF


**settings.py**
```python

INSTALLED_APPS = [
    # ...
    'rest_framework',
    'rest_framework.authtoken',

    '_quick_auth',

]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

# you must have a proper email configuration, for dev let's just say:
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

QUICK_AUTH = {
    'DJANGO_MODE': 'API',
}

```

**urls.py**
```python
urlpatterns = [
    # ...
    path('', include('_quick_auth.urls')),
    # only if you want to try the SPA demo at path '/':
    path('', TemplateView.as_view(template_name='auth/demo_spa.html')),
]
```

Take a look at '_quick_auth/templates/auth/demo_spa.html' to see how you can add the login/signup/logout buttons in your own templates.

## API Endpoints

Only 3 endpoints are absolutly necessary, check `_quick_auth/urls.py` and uncomment the optionnal ones if you want (closed by default)

|uri | Method | form-data | Authorization | effect |
| --- | --- | --- | --- | --- |
| auth/api_signup/ | POST | username, email, password, password2 | - | Create a new user, send a confirmation email |
| auth/api_login/ | POST | credential, password | - | Log in, return a `auth_token` and a `user` |
| auth/api_logout/ | POST | - | Token [the auth_token] | log out, delete the auth token in the database |


## Views

If using DRF, include this views in your project as simple links (GET).

| uri | effect |
| --- | --- |
| auth/password_reset_request/ | to ask for a password reset if the passowrd is forgotten. The user must have an already verified email account |
| auth/change_email/ | to ask for an email change |

The other views are the ones used following the links given in the emails.


## QUICK_AUTH options

A few parameters can be changed through the variable QUICK_AUTH in your settings.py,
here are the default values.

```python
QUICK_AUTH = {
    'DJANGO_MODE': 'CLASSIC',  # 'CLASSIC', 'API' or 'TEST'
    'BASE_TEMPLATE': 'auth/demo.html',  # with CLASSIC mode only, is expected to be changed to your own base.html
    'URL_PREFIX': 'auth/',  # to change the url prefix of all the views and endpoints
    'SITE_NAME': None,  # str: used in email templates instead of host name if you want
    'EMAIL_VALID_TIME': 60 * 60 * 24 * 7,  # 7 days, JWT used in email links expiration time
}
```
