import uuid
import time
import jwt

from jwt.exceptions import ExpiredSignatureError
from django.shortcuts import get_object_or_404
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
)
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth import get_user_model

from . import config
from .utils import gettext_lazy as _


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            _("Required. 150 characters or fewer. Letters, digits and ./+/-/_ only."),
        ),
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(150)
        ],
        error_messages={
            "unique": _("A user with that username already exists."),
            "max_length": _("Username must be less than 150 characters."),
            "invalid": _("Username must contain only letters, digits and ./+/-/_ characters."),
        },
    )
    email = models.EmailField(_("email address"), unique=True)

    new_email = models.EmailField(blank=True, null=True, unique=False)
    is_confirmed = models.BooleanField(default=False)

    def get_jwt_token(self, expires_in=config.EMAIL_VALID_TIME, action="unspecified"):

        token = jwt.encode(
            {'id': str(self.id), 'exp': time.time()+expires_in, 'action': action},
            settings.SECRET_KEY, algorithm='HS256'
        )
        return token

    @staticmethod
    def verify_jwt_token(token):
        try:
            pk = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256'])['id']
            action = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256'])['action']
        except ExpiredSignatureError:  # invalid token
            return None, None
        return get_object_or_404(get_user_model(), id=pk), action

    def clean(self):
        if "@" in self.username:
            raise ValidationError(
                {'username': _("A username cannot include the symbol '@'.")})
        super().clean()

    def save(self, *args, **kwargs):
        # self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
