from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)


def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'account.html')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid email or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def sign_out(request):
    logout(request)
    return redirect('login')


def registration(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'account.html')
    else:
        if request.user.is_active:
            return redirect('account')

        user_form = UserRegistrationForm()
    return render(request, 'registration.html', {'user_form': user_form})


@login_required
def account(request):
    if not request.user.is_authenticated:
        return redirect('login')

    template = 'account.html'
    if request.user.groups.filter(name='images-moderators').exists():
        template = 'moderator_account.html'

    return render(request, template, {'user': request.user})


@login_required
def settings(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            if user_form.check_password():
                user_form.instance.set_password(user_form.cleaned_data['new_password'])
                logout(request)
            user_form.save()
            logger.error(profile_form.save())
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'settings.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
