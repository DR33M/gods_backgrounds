from django.urls import path
from . import views

app_name = 'main_api'

urlpatterns = [
    path('image/', views.images),

    path('image/rating/<image_pk>/', views.rating),
    path('image/downloads/<image_pk>/', views.downloads),
]


