from django.urls import path
from . import views

app_name = 'main_api'

urlpatterns = [
    path('images/', views.images),

    path('rating/<image_pk>/', views.rating),
    path('downloads/<image_pk>/', views.downloads),
]


