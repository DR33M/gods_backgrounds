from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('wallpaper/<slug>/', views.detailed_image_view, name="detailed_image_view"),
    path('user_agreements/', views.user_agreements, name="user_agreements"),

    path('search/', views.images_list, name='search_images_by_tag'),
    path('add/', views.add_image, name='add_image'),

    path('catalog/<tag_slug>/', views.images_list, name='images_list_by_tag'),
    path('', views.images_list, name="home")
]
