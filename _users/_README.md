# _users (v1.0.1)

This is just a very basic User.

It does nothing but spares a little time by already configuring a proper admin and a uuid.

# Installation

**settings.py**
```python
INSTALLED_APPS: [
    # ...
    '_users',
]

# ...

AUTH_USER_MODEL = '_users.User'

```

