from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings

from dal import autocomplete
from taggit.models import Tag

from utils.user import is_moderator

from .models import Image, Color
from .forms import ImageUploadForm, EditTagsForm
from .utils import sort


class TagsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Tag.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


def home(request):
    color = request.GET.get('color', None)
    tags = request.GET.get('tags', None)

    if request.GET:
        images_list = Image.objects.select_related('author').filter(status=Image.Status.MODERATION).order_by('-created_at')
        if tags:
            tags = tags.split(",")
            kwargs = sort.in_list('tags__name', tags)
            images_list = sort.get_images(kwargs, '-tags__name')

        if color:
            color = get_object_or_404(Color, hex=color)
            images_list = images_list.filter(colors__similar_color=color.similar_color).distinct()
    else:
        images_list = Image.objects.select_related('author').filter(status=Image.Status.APPROVED).order_by('-created_at')

    paginator = Paginator(images_list, settings.IMAGE_MAXIMUM_COUNT_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'home.html', {
        'images_list': page_obj,
        'color': color,
        'common_tags': Image.tags.most_common().order_by('name')[:settings.DISPLAY_MOST_COMMON_TAGS_COUNT],
        'columns': range(0, settings.IMAGE_COLUMNS, 1)
    })


def detailed_image_view(request, slug):
    image = get_object_or_404(Image, slug=slug)
    images_tags_ids = image.tags.values_list('id', flat=True)
    similar_images = Image.objects.filter(tags__in=images_tags_ids).exclude(id=image.id)
    similar_images = similar_images.annotate(same_tags=Count('tags')).order_by('-same_tags')[:settings.SIMILAR_IMAGES_COUNT]
    form = EditTagsForm(instance=image)

    if request.method == 'POST' and 'edit' in request.POST:
        form = EditTagsForm(data=request.POST, instance=image)
        if form.is_valid() and (request.user == image.author or is_moderator(request.user)):
            obj = form.save(commit=False)
            obj.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse('main:detailed_image_view', kwargs={'slug': obj.slug}))

    return render(request, 'detailed_image_view.html', {
        'image': image,
        'colors': image.colors.all(),
        'similar_images': similar_images,
        'moderator': is_moderator(request.user),
        'form': form,
        'columns': range(0, settings.IMAGE_COLUMNS, 1)
    })


@login_required
def cabinet(request, username=''):
    if not username:
        return HttpResponseRedirect(reverse('main:cabinet', kwargs={
            'username': request.user.username
        }))

    user = request.user

    if not request.user.username == username:
        user = User.objects.get(username=username)

    images_list = Image.objects.filter(author=user).select_related('author').order_by('-created_at')

    search_query = request.GET.get('search', '')
    if search_query:
        images_list = images_list.filter(tags__name__iexact=search_query)

    paginator = Paginator(images_list, settings.IMAGE_MAXIMUM_COUNT_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'cabinet.html', {
        'user': user,
        'images_list': page_obj,
        'images_display_status': True,
        'moderator': is_moderator(user),
        'columns': range(0, settings.IMAGE_COLUMNS, 1)
    })


@login_required
def add_image(request):
    if request.method == 'POST':
        image_form = ImageUploadForm(data=request.POST, files=request.FILES)
        if image_form.is_valid():
            image = image_form.save(commit=False)
            image.author = request.user
            image.save()
            image_form.save_m2m()
            return redirect('main:detailed_image_view', slug=image.slug)
    else:
        image_form = ImageUploadForm()

    return render(request, 'add.html', {
        'image_form': image_form,
    })


@login_required
def delete_image(request, slug):
    if request.method == 'POST' and 'delete' in request.POST:
        image = get_object_or_404(Image, slug=slug)
        if request.user == image.author or is_moderator(request.user):
            image.delete()
    return redirect('main:home')


def user_agreements(request):
    return render(request, 'user_agreements.html', {})


def page_not_found_error(request, exception):
    return render(request, "errors/404.html", status=404)
