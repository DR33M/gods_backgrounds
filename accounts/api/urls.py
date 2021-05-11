from django.urls import path
from . import views

app_name = 'main_api'

urlpatterns = [
    path('user/<int:pk>/', views.Profile.as_view()),
]


