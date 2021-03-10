from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('wallpaper/<str:image_name>/', views.detailed_image_view, name="detailed_image_view"),
    path('cabinet/', views.cabinet, name="cabinet"),
    path('user_agreements/', views.user_agreements, name="user_agreements"),
    path('settings/', views.settings, name="settings"),

    path('', views.index)
]
