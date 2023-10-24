# Django Collection

Some ready to use django apps.

- Remember to add the apps to INSTALLED_APPS and make migrations if necessary.

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

## _users

Auth system with both email and username, classic and API included.
