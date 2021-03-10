from django.shortcuts import render, redirect


def index(request):
    return render(request, 'index.html', {})


def detailed_image_view(request, image_name):
    return render(request, 'detailed_image_view.html', {})


def cabinet(request):
    return render(request, 'cabinet.html', {})


def user_agreements(request):
    return render(request, 'user_agreements.html', {})


def settings(request):
    return render(request, 'settings.html', {})


def page_not_found_error(request, exception):
    return render(request, "errors/404.html", status=404)
