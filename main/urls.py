from django.urls import path, include
from . import views

app_name = 'main'

urlpatterns = [
    path('add/', views.add_image, name='add_image'),
    path('wallpaper/<slug>/', views.detailed_image_view, name="detailed_image_view"),
    path('wallpaper/<slug>/delete', views.delete_image, name="delete_image"),
    path('catalog/<slug>/', views.home, name='images_list_by_tag'),
    path('search/', views.home, name='search_images_by_tag'),
    path('user_agreements/', views.user_agreements, name="user_agreements"),

    path('tags-autocomplete/', views.TagsAutocomplete.as_view(), name='tags-autocomplete'),

    path('', views.home, name="home"),

    path('cabinet/', views.cabinet, name='cabinet'),
    path('cabinet/<username>', views.cabinet, name='cabinet'),

    path('api/', include('main.api.urls', namespace='api')),
]
