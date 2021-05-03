import json
import mimetypes
import os
from io import StringIO
from urllib.parse import urlparse

from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.contrib import messages

from dal import autocomplete
from taggit.models import Tag

from utils.user import is_moderator

from .models import Image, Color
from .forms import ImageUploadForm, EditTagsForm
from .utils.DictORM import DictORM
from .decorators import check_recaptcha

import logging

logger = logging.getLogger(__name__)


class TagsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Tag.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


def home(request):
    query = request.GET.get('q')
    query_dict = {}

    if query:
        try:
            query_dict = json.load(StringIO(urlparse(query).path))
        except json.decoder.JSONDecodeError:
            # return error page
            pass
    else:
        query_dict = {'in': {'status': [Image.Status.APPROVED]}}

    query = DictORM().make(query_dict)

    images_list = Image.objects.select_related('author').filter(**query.kwargs).order_by('-created_at')
    if query.order_list:
        images_list = images_list.order_by(*query.order_list)

    paginator = Paginator(images_list, settings.IMAGE_MAXIMUM_COUNT_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'home.html', {
        'images_list': page_obj,
        #'color': color,
        'common_tags': Image.tags.most_common()[:settings.DISPLAY_MOST_COMMON_TAGS_COUNT],
        'columns': range(0, settings.IMAGE_COLUMNS, 1),
        'messages': messages.get_messages(request),
    })


def detailed_image_view(request, slug):
    image = get_object_or_404(Image, slug=slug)
    images_tags_ids = image.tags.values_list('id', flat=True)
    similar_images = Image.objects.select_related('author').filter(tags__in=images_tags_ids).exclude(id=image.id)
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

    if not user.username == username:
        user = User.objects.get(username=username)

    images_list = Image.objects.select_related('author').filter(author=user).order_by('-created_at')

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
        'columns': range(0, settings.IMAGE_COLUMNS, 1),
        'messages': messages.get_messages(request),
    })


@user_passes_test(is_moderator)
def moderator_panel(request):
    user = request.user

    try:
        image = Image.objects.get(moderator_id=user.id, status=Image.Status.MODERATION)
    except Image.DoesNotExist:
        image = Image.objects.select_related('author').filter(moderator_id=None, status=Image.Status.MODERATION).first()

        if not image:
            messages.add_message(request, messages.ERROR, 'No more pictures for moderation.')
            return redirect('main:cabinet')

        image.moderator_id = user.id
        image.save()

    form = EditTagsForm(instance=image)
    if request.method == 'POST':
        if 'end-work' in request.POST:
            image.moderator_id = None
            image.save()
            messages.add_message(request, messages.SUCCESS, 'You have successfully completed your job.')
            return redirect('main:cabinet')
        if 'edit' in request.POST:
            form = EditTagsForm(data=request.POST, instance=image)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.status = Image.Status.APPROVED
                obj.save()
                form.save_m2m()
                messages.add_message(request, messages.SUCCESS, 'Image has been approved.')
        return HttpResponseRedirect(reverse('main:moderator-panel'))

    return render(request, 'moderator-panel.html', {
        'image': image,
        'colors': image.colors.all(),
        'form': form,
        'messages': messages.get_messages(request),
    })


@check_recaptcha
@login_required
def add_image(request):
    if request.method == 'POST':
        image_form = ImageUploadForm(data=request.POST, files=request.FILES)
        if request.recaptcha_is_valid and image_form.is_valid():
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
    next_redirect = request.POST.get('next', '/')
    if request.method == 'POST' and 'delete' in request.POST:
        image = get_object_or_404(Image, slug=slug)
        if request.user == image.author or is_moderator(request.user):
            image.delete()
            messages.add_message(request, messages.SUCCESS, 'The image has been deleted.')
    return HttpResponseRedirect(next_redirect)


def download_image(request, slug):
    image = get_object_or_404(Image, slug=slug)
    image_url = settings.MEDIA_ROOT + str(image)[7:]
    image_extension = os.path.splitext(image.image.name)[1]
    file = open(image_url, "rb").read()
    content_type = mimetypes.guess_type(image_url)[0]
    response = HttpResponse(file, content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename={image.slug + image_extension}'
    return response


def user_agreements(request):
    return render(request, 'user_agreements.html', {})


def page_not_found_error(request, exception):
    return render(request, "errors/404.html", status=404)
