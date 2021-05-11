from django.urls import path
from . import views

app_name = 'main_api'

urlpatterns = [
    path('image/get', views.ImageViewSet.as_view({'get': 'get'})),
    path('image/change_rating/<pk>/', views.ImageViewSet.as_view({'patch': 'change_rating'})),
    path('image/add_download/<pk>/', views.ImageViewSet.as_view({'patch': 'add_download'})),
    path('image/mp_get', views.ImageViewSet.as_view({'get': 'mp_get'})),
    path('image/mp_approve/<pk>/', views.ImageViewSet.as_view({'patch': 'mp_approve'})),
    path('image/delete/<pk>/', views.ImageViewSet.as_view({'delete': 'delete'})),

    path('tags/', views.Tags.as_view()),
]


