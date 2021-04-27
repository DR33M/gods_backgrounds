from django.urls import path, include
from . import views

app_name = 'main'

urlpatterns = [
    path('add/', views.add_image, name='add_image'),
    path('wallpaper/<slug>/', views.detailed_image_view, name="detailed_image_view"),
    path('wallpaper/<slug>/delete', views.delete_image, name="delete_image"),
    path('user_agreements/', views.user_agreements, name="user_agreements"),

    path('tags-autocomplete/', views.TagsAutocomplete.as_view(), name='tags-autocomplete'),

    path('cabinet/moderator-panel', views.moderator_panel, name='moderator-panel'),
    path('cabinet/<username>', views.cabinet, name='cabinet'),
    path('cabinet/', views.cabinet, name='cabinet'),

    path('api/', include('main.api.urls', namespace='api')),

    path('', views.home, name="home"),
]
