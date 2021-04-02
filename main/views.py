from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import Count
from taggit.models import Tag
from django.core import serializers

from .models import Image
from .forms import SearchForm


def images_list(request, tag_slug=None):
    object_list = Image.objects.filter(status=Image.Status.APPROVED).order_by('-created_at')
    common_tags = Image.tags.most_common()[:10]
    search_form = SearchForm()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    if 'q' in request.GET and request.GET['q']:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = request.GET['q']
            object_list = object_list.filter(tags__name__iexact=query)

    paginator = Paginator(object_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {
        'images_list': page_obj,
        'tag': tag,
        'common_tags': common_tags,
        'search_form': search_form,
    })


def detailed_image_view(request, slug):
    image = get_object_or_404(Image, slug=slug)
    images_tags_ids = image.tags.values_list('id', flat=True)
    similar_images = Image.objects.filter(tags__in=images_tags_ids).exclude(id=image.id)
    similar_images = similar_images.annotate(same_tags=Count('tags')).order_by('-same_tags')[:4]
    return render(request, 'detailed_image_view.html', {
        'image': image,
        'similar_images': similar_images,
    })


def user_agreements(request):
    return render(request, 'user_agreements.html', {})


def page_not_found_error(request, exception):
    return render(request, "errors/404.html", status=404)
