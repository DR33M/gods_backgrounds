from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'main'

urlpatterns = [
    path('wallpaper/<slug>/', views.detailed_image_view, name="detailed_image_view"),
    path('cabinet/', views.cabinet, name="cabinet"),
    path('user_agreements/', views.user_agreements, name="user_agreements"),
    path('settings/', views.settings, name="settings"),

    path('search/', views.images_list, name='search_images_by_tag'),

    path('catalog/<tag_slug>/', views.images_list, name='images_list_by_tag'),
    path('', views.images_list, name="home")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
