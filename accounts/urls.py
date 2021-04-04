from django.conf.urls import url
from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    url('login', views.sign_in, name='login'),
    url('logout', views.sign_out, name='logout'),
    url('settings', views.settings, name='settings'),
    url('registration', views.registration, name='registration'),

    path('<username>', views.account, name='account'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('new_email/<uidb64>/<token>/<email>', views.new_email, name='new_email'),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="password_reset_form.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"),
         name="password_reset_complete"),
    url('', views.account, name='account'),
]
