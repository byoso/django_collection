from django.urls import path
from . import views, views_api

"""
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


"""
prefix = "auth/"

app_name = "_users"

urlpatterns = [
    # Classic routes

    path(f'{prefix}login/', views.login_view, name='login'),
    path(f'{prefix}logout/', views.logout_view, name='logout'),
    path(f'{prefix}signup/', views.signup_view, name='signup'),
    path(f'{prefix}account/', views.account, name='account'),
    path(f'{prefix}request_password_reset/', views.request_password_reset, name='request_password_reset'),
    path(f'{prefix}reset_password/<str:token>/', views.reset_password, name='reset_password'),
    path(f'{prefix}change_password/', views.change_password, name='change_password'),
    path(f'{prefix}change_username/', views.change_username, name='change_username'),
    path(f'{prefix}change_email/', views.change_email, name='change_email'),
    path(f'{prefix}confirm_email/<str:token>/', views.confirm_email, name='confirm_email'),
    path(
        f'{prefix}request_resend_account_confirmation_email/',
        views.request_resend_account_confirmation_email,
        name='request_resend_account_confirmation_email'),

    # API routes

    # path(f'{prefix}token/login/', views_api.LoginWithAuthToken.as_view(), name="token_login"),  # normal login
    # path(f'{prefix}login_with_jwt/', views_api.LoginWithJWTToken.as_view(), name="login_with_jwt"),  # login from email
    # path(f'{prefix}token/logout/', views_api.token_logout, name="token_logout"),
    # path(
    #     f'{prefix}password/request_reset/',
    #     views_api.password_request_reset,
    #     name='password_request_reset'
    # ),
    # path(
    #     f'{prefix}email/confirm_email/resend/',
    #     views_api.email_confirm_email_resend,
    #     name="email_confirm_email_resend"
    # ),
    # path(
    #     f'{prefix}password/change/',
    #     views_api.password_change,
    #     name='password_change'
    # ),
    # path(
    #     f'{prefix}email/request_change/',
    #     views_api.email_request_change,
    #     name='email_request_change'
    # ),
    # path(
    #     f'{prefix}username/change/',
    #     views_api.username_change,
    #     name='username_change'
    # ),
    # path(f'{prefix}users/delete_me/', views_api.users_delete_me, name='users_delete_me'),
    # path(f'{prefix}users/', views_api.UserView.as_view(), name="users"),
    # path(f'{prefix}users/my_infos/', views_api.users_my_infos, name="users_my_infos"),

    # # DO NOT not use this one in production:
    # path(f'{prefix}users/all/', views_api.get_users_all, name="get_users_all"),

]
