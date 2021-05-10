from django.urls import path
from . import views

app_name = 'main_api'

urlpatterns = [
    path('image/', views.images),
    path('tags/', views.Tags.as_view()),

    path('moderator-panel/', views.mp_image),

    path('image/rating/<image_pk>/', views.rating),
    path('image/downloads/<image_pk>/', views.downloads),
]


