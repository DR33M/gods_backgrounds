from django.conf.urls import url
from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    url('login', views.sign_in, name='login'),
    url('logout', views.sign_out, name='logout'),
    url('settings', views.settings, name='settings'),
    url('registration', views.registration, name='registration'),

    path('confirm/<uidb64>/<token>/<field>', views.confirm, name='confirm'),
    path('reset_password/', views.reset_password, name="reset_password"),
    path('reset_password_done/', views.reset_password_done, name="reset_password_done"),

    path('api/', include('accounts.api.urls', namespace='api')),
]
