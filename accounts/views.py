from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_decode

from .mail import Messages

from .forms import LoginForm, UserRegistrationForm, UserEditForm, EmailForm, ProfileEditForm
import logging

logger = logging.getLogger(__name__)


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
                    return HttpResponseRedirect('accounts/')
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

            Messages.activate(request, user)

            return render(request, 'registration.html', {
                'message': 'Please confirm your email address to complete the registration'
            })
    else:
        user_form = UserRegistrationForm()

    return render(request, 'registration.html', {'user_form': user_form})


def activate(request, uidb64, token):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponseRedirect('login')
    else:
        return HttpResponse('Activation link is invalid!')


def new_email(request, uidb64, token, email):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.email = email
        user.save()
        return HttpResponseRedirect('settings')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required
def account(request, username=''):
    if not username:
        return HttpResponseRedirect(reverse('accounts:account', kwargs={
            'username': request.user.username
        }))

    user = request.user
    moderator = False

    if not request.user.username == username:
        user = User.objects.get(username=username)

    if user.groups.filter(name='images-moderators').exists():
        moderator = True

    return render(request, 'account.html', {'user': user, 'moderator': moderator})


@login_required
def settings(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        email_form = EmailForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            if user_form.cleaned_data['new_password']:
                user_form.instance.set_password(user_form.cleaned_data['new_password'])
                logout(request)

            if email_form.is_valid() and not email_form.cleaned_data['email'] == request.user.email:
                Messages.new_email(request, email_form.cleaned_data['email'])
                return render(request, 'settings.html', {
                    'message': 'Please confirm your new email address',
                })

            user_form.save()
            profile_form.save()
            return HttpResponseRedirect('settings')
    else:
        user_form = UserEditForm(instance=request.user)
        email_form = EmailForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'settings.html', {
        'user_form': user_form,
        'email_form': email_form,
        'profile_form': profile_form,
    })