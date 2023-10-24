# _users

WIP: 60%
TODO: the API version

Clean django _users app with auth, classic and api included.

# Installation

## First

`pip install PyJWT`

**settings.py**
```
INSTALLED_APPS = [
    # ...
    '_users',
]

AUTH_USER_MODEL = _users.User

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
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', '0') == '1'

```

**_project/urls.py**
```python
urlpatterns = [
    # ...
    path('', include('_users.urls', namespace='_users')),  # the namespace "_users" is required
]
```

## Classic version

Remove `views_api.py`, `serializers.py`, and the API paths in `urls.py`


Choose a BASE_TEMPLATE used in _users and check the configuration at the same time:

**config.py**
```python
BASE_TEMPLATE="_base.html"
```

Include login / sign up / logout buttons in some nav bar:

```html
<div class="buttons">
  {% if user.is_authenticated %}
  <span class="mr-4">{{ user.username }}</span>
  <a class="button is-warning is-small" href="{% url '_users:logout' %}">
    Logout
  </a>
  {% else %}
  <a class="button is-small" href="{% url '_users:signup' %}">
    Sign up
  </a>
  <a class="button is-light is-success is-small" href="{% url '_users:login' %}">
    Log in
  </a>
  {% endif %}
</div>
```


## API version

`pip install django-rest-framework`

Remove `forms.py`, `views.py`, and the classic paths in `urls.py`, chek the `config.py` file.

**settings.py**
```python

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

```

API ENDPOINTS details:

|Endpoint | method | form-data | Permission | Effects |
|---|---|---|---|---|
| `token/login/` | POST | credential, password | - | get an authentication token |
| `login_with_jwt/` | POST | credential, jwt_token | - | login from an email link, sets user.is_confirmed to True |
| `token/logout/` | GET | - | IsAuthenticated | forces delete token |
| `password/request_reset/` | POST | credential | - | sends a reset email |
| `password/change/` | POST | password, password2 | IsAuthenticated | Changes the password |
| `username/change/` | POST | username | IsAuthenticated | Changes the username |
| `email/confirm_email/resend/`| POST | credential | - | resends the confirmation email |
| `email/request_change/` | POST | email | IsAuthenticated | Sends a confirmation email for activating the new email |
| `users/` | POST | username, email, password | - | Create a new user |
| `users/my_infos/` | GET | - | IsAuthenticated | returns the user's infos |
| `users/delete_me/` | DELETE | - | IsAuthenticated | deletes the user |
