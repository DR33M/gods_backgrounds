from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    url('login', views.sign_in, name='login'),
    url('logout', views.sign_out, name='logout'),
    url('settings', views.settings, name='settings'),
    url('registration', views.registration, name='registration'),

    path('<username>', views.account, name='account'),

    path('confirm/<uidb64>/<token>/<field>', views.confirm, name='confirm'),

    path('reset_password/', views.reset_password , name="reset_password"),
    path('reset_password_done/', views.reset_password_done, name="reset_password_done"),

    url('', views.account, name='account'),
]
