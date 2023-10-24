# Basic settings
SITE_NAME = ""  # name used in emails
INDEX_NAME = "home:index"  # name of the index page
EMAIL_VALID_TIME = 3600  # token validity in secondes
TEMPLATES_TITLE = "Authentication"

# Confirmation by email link method
CONFIRMATION_METHOD = "GET"  # GET (classic) or POST (api)

# Classic only
BASE_TEMPLATE = "_base.html"  # base template used for the auth pages

# API only
API_EMAIL_LOGIN_LINK = "http://example.com/api/email-login/"

# Dev options
EMAIL_TERMINAL_PRINT = False  # force print in terminal even if the email is actualy sent
