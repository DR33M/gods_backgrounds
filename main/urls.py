from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'main'

urlpatterns = [
    path('wallpaper/<slug>/', views.detailed_image_view, name="detailed_image_view"),
    path('cabinet/', views.cabinet, name="cabinet"),
    path('user_agreements/', views.user_agreements, name="user_agreements"),
    path('settings/', views.settings, name="settings"),

    path('api/', include('main.api.urls')),

    path('', views.home, name="home")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
