from django.urls import path
from . import views

app_name = 'main_api'

urlpatterns = [
    path('find/', views.find),

    path('sort/', views.sorting),

    path('rating/<image_pk>/', views.rating),
    path('downloads/<image_pk>/', views.downloads),
]


