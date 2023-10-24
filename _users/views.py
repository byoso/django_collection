from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages

from .config import BASE_TEMPLATE, TEMPLATES_TITLE, INDEX_NAME
from .forms import (
    LoginForm,
    ResetPasswordForm,
    ChangeUsernameForm,
    ChangeEmailForm,
    CredentialForm,
    SignUpForm,
)

from .utils import (
    send_password_reset_email,
    send_confirm_email,
    gettext_lazy as _,
)

User = get_user_model()


@transaction.atomic
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            credential = form.cleaned_data['credential']
            password = form.cleaned_data['password']
            if "@" in credential:
                username = get_object_or_404(User, email=credential).username
                user = authenticate(
                    request, username=username, password=password)
            else:
                user = authenticate(
                    request, username=credential, password=password)
            if user is not None and user.is_confirmed:
                login(request, user)
                return redirect(INDEX_NAME)
            else:
                messages.add_message(
                    request, messages.ERROR,
                    message=_("Incorrect credentials or unconfirmed account."),
                    extra_tags="warning"),
        else:
            context = {
                "form": form,
                "base_template": BASE_TEMPLATE,
                "title": TEMPLATES_TITLE,
            }
            return render(request, "_users/login.html", context)

    form = LoginForm()
    context = {
        "form": form,
        "base_template": BASE_TEMPLATE,
        "title": 'Login',
    }
    return render(request, "_users/login.html", context)


# logout
def logout_view(request):
    logout(request)
    return redirect(INDEX_NAME)


@transaction.atomic
@login_required
def account(request):
    context = {
        "base_template": BASE_TEMPLATE,
        "title": TEMPLATES_TITLE,
    }
    return render(request, "_users/account.html", context)

@transaction.atomic
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User(username=username, email=email, is_active=True)
            user.set_password(password)
            user.save()
            send_confirm_email(request, user)

            message1 = _(
                "Please check your inbox at"
                " '%(email)s' to confirm your account."
            ) % {'email': user.email}
            message = "%(message1)s" % {
                'message1': message1,
            }

            messages.add_message(
                request, messages.INFO,
                message=message,
                extra_tags="info"
            )
            return redirect('_users:login')
        else:
            context = {
                "form": form,
                "base_template": BASE_TEMPLATE,
                "title": TEMPLATES_TITLE,
            }
            return render(request, "_users/signup.html", context)

    form = SignUpForm()
    context = {
        "form": form,
        "base_template": BASE_TEMPLATE,
        "title": TEMPLATES_TITLE,
    }
    return render(request, "_users/signup.html", context)


@transaction.atomic
def request_password_reset(request):
    if request.method == "POST":
        form = CredentialForm(request.POST)
        if form.is_valid():
            credential = form.cleaned_data['credential']
            if "@" in credential:
                user = User.objects.get(email=credential)
            else:
                user = User.objects.get(username=credential)
            # user existence is checked by the form validation #
            if user.is_active:
                messages.add_message(
                    request, messages.INFO,
                    message=(_(
                        "Please check your inbox "
                        "and follow the instructions "
                        "to reset your password."
                        )),
                    extra_tags="info"
                )
                send_password_reset_email(request, user)

            else:
                messages.add_message(
                    request, messages.INFO,
                    message=(_(
                        "Your account is no longer active. Please contact the administrator. "
                        "No email has been sent."
                        )),
                    extra_tags="info"
                )
        else:
            context = {
                "form": form,
                "base_template": BASE_TEMPLATE,
                "title": TEMPLATES_TITLE,
            }
            return render(
                request,
                "_user/request_password_reset.html",
                context
                )
    form = CredentialForm()
    if request.user.is_authenticated:
        form = CredentialForm(initial={'credential': request.user.email})
    context = {
        "form": form,
        "base_template": BASE_TEMPLATE,
        "title": TEMPLATES_TITLE,
    }
    return render(request, "_users/request_password_reset.html", context)


@transaction.atomic
@login_required
def change_password(request):
    user = request.user
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.add_message(
                request, messages.SUCCESS,
                message=_("Your password has been successfully reset. Please log in."),
                extra_tags="success"
            )
            return redirect(INDEX_NAME)
        else:
            context = {
                'form': form,
                "base_template": BASE_TEMPLATE,
                "title": TEMPLATES_TITLE,
            }
            return render(request, "_users/reset_password.html", context)

    form = ResetPasswordForm()
    context = {
        'form': form,
        "base_template": BASE_TEMPLATE,
        "title": TEMPLATES_TITLE,
    }
    return render(request, "_users/reset_password.html", context)


@transaction.atomic
def reset_password(request, token=None):
    """Receive the token from the confirmation email and reset the password
    or already authenticated user.
    """
    if token:
        user, _action = User.verify_jwt_token(token)
    elif request.user.is_authenticated:
        user = request.user
    else:
        user = None

    if user is None:
        messages.add_message(
            request, messages.INFO,
            message=(_(
                "Token invalid or expired, ask for a new one."
                )),
            extra_tags="danger"
        )
        return redirect('_users:request_password_reset')

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.add_message(
                request, messages.SUCCESS,
                message=_("Your password has been successfully reset. Please log in."),
                extra_tags="success"
            )
            return redirect(INDEX_NAME)
        else:
            context = {
                'form': form,
                "base_template": BASE_TEMPLATE,
                "title": TEMPLATES_TITLE,
            }
            return render(request, "_users/reset_password.html", context)

    form = ResetPasswordForm()
    login(request, user)
    if token:
        messages.add_message(
            request, messages.SUCCESS,
            message=_("You have been logged in via email confirmation. Please reset your password."),
            extra_tags="warning"
        )

    context = {
        'form': form,
        "base_template": BASE_TEMPLATE,
        "title": TEMPLATES_TITLE,
    }
    return render(request, "_users/reset_password.html", context)


@transaction.atomic
@login_required
def change_username(request):
    if request.method == 'POST':
        form = ChangeUsernameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = request.user
            user.username = username
            user.save()
            messages.add_message(
                request, messages.SUCCESS,
                message=_(
                    "New username set: '%(username)s'."
                ) % {'username': username},
                extra_tags="success"
            )
            return redirect("_users:account")
        else:
            context = {
                'form': form,
                "base_template": BASE_TEMPLATE,
                "title": TEMPLATES_TITLE,
            }
            return render(
                request,
                "_users/change_username.html",
                context,
                )

    form = ChangeUsernameForm()
    context = {
        'form': form,
        "base_template": BASE_TEMPLATE,
        "title": TEMPLATES_TITLE,
    }
    return render(request, "_users/change_username.html", context)


@transaction.atomic
@login_required
def change_email(request):
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = request.user
            user.new_email = email
            user.save()
            send_confirm_email(request, user)

            message = _(
                "Please check your inbox to confirm your new "
                "address at '%(email)s'") % {"email": user.new_email}
            messages.add_message(
                request, messages.INFO,
                message,
                extra_tags="info"
            )
            return redirect("_users:account")
        else:
            context = {
                'form': form,
                "base_template": BASE_TEMPLATE,
                "title": TEMPLATES_TITLE,
            }
            return render(request, "_users/change_email.html", context)

    form = ChangeEmailForm()
    context = {
        'form': form,
        "base_template": BASE_TEMPLATE,
        "title": TEMPLATES_TITLE,
    }
    return render(request, "_users/change_email.html", context)


@transaction.atomic
def confirm_email(request, token):
    user, _action = User.verify_jwt_token(token)

    if user is None:
        messages.add_message(
            request, messages.INFO,
            message=(_(
                "Token invalid or expired, ask for a new one."
                )),
            extra_tags="danger"
        )
        return redirect('_users:request_resend_account_confirmation_email')
    if user is not None and user.is_active:
        if not user.is_confirmed:
            user.is_confirmed = True
            user.new_email = None
            msg = _("Your account has been confirmed.")
            user.save()
        elif user.new_email:
            user.email = user.new_email
            user.new_email = None
            msg = _("Your new email has been confirmed.")
            user.save()
        else:
            msg = _("Your account is already confirmed.")
        messages.add_message(
            request, messages.SUCCESS,
            message=msg,
            extra_tags="success"
        )

        return redirect(INDEX_NAME)


@transaction.atomic
def request_resend_account_confirmation_email(request):
    if request.method == 'POST':
        form = CredentialForm(request.POST)
        if form.is_valid():
            credential = form.cleaned_data['credential']
            if "@" in credential:
                user = User.objects.get(email=credential)
            else:
                user = User.objects.get(username=credential)

            # user existence is checked by the form validation #

            if user.is_confirmed:
                messages.add_message(
                    request, messages.INFO,
                    message=(_(
                        "Your account is already confirmed. "
                        "No email has been sent."
                        )),
                    extra_tags="info"
                )
                return redirect("_users:login")

            send_confirm_email(request, user)

            messages.add_message(
                request, messages.INFO,
                message=(_(
                    "Please check your inbox "
                    "to confirm your account."
                    )),
                extra_tags="info"
            )
        else:
            context = {
                "form": form,
                "base_template": BASE_TEMPLATE,
                "title": TEMPLATES_TITLE,
            }
            return render(
                request,
                "_users/request_resend_account_confirmation_email.html",
                context
                )
    form = CredentialForm()
    context = {
        "form": form,
        "base_template": BASE_TEMPLATE,
        "title": TEMPLATES_TITLE,
    }
    return render(
        request,
        "_users/request_resend_account_confirmation_email.html",
        context
        )
