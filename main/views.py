from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Image


def home(request):
    return render(request, 'home.html')


def detailed_image_view(request, slug):
    image = get_object_or_404(Image, slug=slug)
    return render(request, 'detailed_image_view.html', {'image': image})


def cabinet(request):
    return render(request, 'cabinet.html', {})


def user_agreements(request):
    return render(request, 'user_agreements.html', {})


def settings(request):
    return render(request, 'settings.html', {})


def page_not_found_error(request, exception):
    return render(request, "errors/404.html", status=404)
