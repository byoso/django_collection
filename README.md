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

## __commands

- create_admin : create an admin, can be used in a prod script
- wait_for_db : used in a prod script

## _users (to be deprecated, better use _auth or _auth_api)

Auth system with both email and username, classic and API included.

## _auth

Authentication system based on django-allauth

## _auth_api

Authentication ready to use out of the box for any SPA, it includes verifications
via emails and some 'classic' views needed to handle this.
