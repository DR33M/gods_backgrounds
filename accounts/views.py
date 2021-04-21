from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_decode

from .mail import Messages

from .forms import LoginForm, UserRegistrationForm, UserEditForm, EmailForm, ProfileEditForm, NewPasswordForm
import logging

logger = logging.getLogger(__name__)


def confirm_fork(request, user, field):
    template = ''
    data = {}

    if field == 'activate':
        user.is_active = True
        user.save()
        return HttpResponseRedirect('login')
    elif field == 'email':
        template = 'reset_password.html'
        if request.POST:
            email_form = EmailForm(instance=user, data=request.POST)
            if email_form.is_valid() and not email_form.cleaned_data['email'] == request.user.email:
                user.email = email_form.cleaned_data['email']
                user.save()
                return HttpResponseRedirect('settings')
        else:
            data = {'email_form': EmailForm(instance=user)}
            template = 'new_email.html'
    elif field == 'password':
        template = 'reset_password.html'
        if request.POST:
            password_form = NewPasswordForm(request.POST)
            if password_form.is_valid():
                user.set_password(password_form.cleaned_data['password2'])
                user.save()
                template = 'reset_password_done.html'
            else:
                data = {'password_form': password_form}
        else:
            data = {'password_form': NewPasswordForm}

    if not template:
        return HttpResponseRedirect('main:cabinet')

    return render(request, template, data)


def sign_in(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    message = ''

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    message = 'Disabled account'
            else:
                message = 'Invalid email or password'
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form, 'message': message})


@login_required
def sign_out(request):
    logout(request)
    return HttpResponseRedirect('login')


def registration(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            Messages.send_message(request, user, 'acc_active_email.html', 'activate')

            return render(request, 'registration.html', {
                'message': 'Please confirm your email address to complete the registration'
            })
    else:
        user_form = UserRegistrationForm()

    return render(request, 'registration.html', {'user_form': user_form})


def confirm(request, uidb64, token, field=''):
    if not field:
        return HttpResponseRedirect('/')

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        return confirm_fork(request, user, field)
    else:
        return HttpResponse('Activation link is invalid!')


def reset_password(request):
    message = ''
    if request.POST:
        email_form = EmailForm(data=request.POST)
        if email_form.is_valid():
            try:
                user = User.objects.get(email=email_form.cleaned_data['email'])
                Messages.send_message(request, user, 'acc_password_reset.html', 'password')
                return render(request, 'reset_password_sent.html')
            except User.DoesNotExist:
                message = 'Email address doesn\'t exist'
    else:
        email_form = EmailForm

    return render(request, 'reset_password_form.html', {'email_form': email_form, 'message': message})


def reset_password_done(request):
    return render(request, 'reset_password_done.html')


@login_required
def settings(request):
    message = ''
    if request.POST:
        if 'change_email' in request.POST:
            Messages.send_message(request, request.user, 'acc_new_email.html', 'email')
            message = 'Check your mail'
            return render(request, 'settings.html', {'message': message})
        else:
            user_form = UserEditForm(instance=request.user, data=request.POST)
            profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
            if user_form.is_valid() and profile_form.is_valid():
                if user_form.cleaned_data['new_password']:
                    user_form.instance.set_password(user_form.cleaned_data['new_password'])
                    logout(request)

                user_form.save()
                profile_form.save()
                return HttpResponseRedirect('settings')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'settings.html', {
        'user': request.user,
        'user_form': user_form,
        'profile_form': profile_form,
        'message': message
    })