# Django Collection

Some ready to use django apps.

- Remember to add the apps to INSTALLED_APPS and make migrations when necessary.

# requirements

## dotenv
`pip install django-dotenv`

**manage.py**
```python
# ...
if __name__ == "__main__":
    dotenv.read_dotenv()

```
Make a `.env` file from the provided `.env-sample`.

# content

## _adminplus

Add a page to the admin, that can be used to add easily some controles to the admin.

## _deployment

Everything that is needed to deploy with docker docker-compose

## _users

Minimalist user model with a proper admin model.

## _auth

Authentication system based on django-allauth

## _auth_api

Authentication ready to use out of the box for any SPA, it includes verifications
via emails and some 'classic' views needed to handle this.

## _quick_auth

Authentication ready for both Django classic and DRF, works really good, but no social auth.
It is the best solution here (better than _auth and _auth_api).

## app_cdn

A ready to go CDN app, for the admin.
