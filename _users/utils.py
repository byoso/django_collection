from threading import Thread

from django.utils.translation import gettext_lazy
from django.conf import settings
from django.shortcuts import reverse
from django.core.mail import send_mail
from django.template.loader import get_template

from .config import (
    SITE_NAME,
    EMAIL_VALID_TIME,
    EMAIL_TERMINAL_PRINT,
    CONFIRMATION_METHOD,
    API_EMAIL_LOGIN_LINK,
)

# in django.utils.translation:
# gettext_lazy = lazy(gettext, str)

if settings.USE_I18N:
    gettext_lazy = gettext_lazy
else:
    def gettext_lazy(string):
        """So there will be no migration errors with or without i18n.
        """
        return string


def dsa_send_mail(*args, **kwargs):
    send = Thread(target=send_mail, args=args, kwargs=kwargs, daemon=True)
    send.start()


def send_password_reset_email(request, user):
    token = user.get_jwt_token(expires_in=EMAIL_VALID_TIME)
    domain = request.build_absolute_uri('/')[:-1]
    if CONFIRMATION_METHOD == 'GET':
        link = domain + reverse('_users:reset_password', args=[token])
    if CONFIRMATION_METHOD == 'POST':
        link = API_EMAIL_LOGIN_LINK + f"{token}"
    context = {
        'user': user,
        'link': link,
        'site_name': SITE_NAME
    }

    msg_text = get_template("_users/emails/request_password_reset.txt")
    if EMAIL_TERMINAL_PRINT:
        print("from ", settings.EMAIL_HOST_USER)
        print(msg_text.render(context))

    dsa_send_mail(
        'Password reset request',
        msg_text.render(context),
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )


def send_confirm_email(request, user, new_email=False):
    token = user.get_jwt_token(expires_in=EMAIL_VALID_TIME)
    domain = request.build_absolute_uri('/')[:-1]
    # if new_email:
    if CONFIRMATION_METHOD == 'GET':
        link = domain + reverse('_users:confirm_email', args=[token])
    elif CONFIRMATION_METHOD == 'POST':
        link = API_EMAIL_LOGIN_LINK + f"{token}"

    context = {
        'user': user,
        'link': link,
        'site_name': SITE_NAME,
    }

    msg_text = get_template("_users/emails/confirm_email.txt")

    if EMAIL_TERMINAL_PRINT:
        print("from ", settings.EMAIL_HOST_USER)
        print(msg_text.render(context))

    if new_email:
        email = user.new_email
    else:
        email = user.email

    dsa_send_mail(
        'Confirm your new email',
        msg_text.render(context),
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
