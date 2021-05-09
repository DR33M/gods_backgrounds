import copy
import json
import mimetypes
import os
from io import StringIO
from urllib.parse import urlparse

from django.core import validators
from django.core import exceptions
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Prefetch
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.contrib import messages


from dal import autocomplete
from taggit.models import Tag

from utils.user import is_moderator

from .models import Color, Image, ImageUserActions, Report
from .forms import ImageUploadForm, EditTagsForm, ReportForm
from .utils.DictORM import DictORM
from utils.mail import Messages as Mail
from .decorators import check_recaptcha

from .api.serializers import ImagesSerializer

import logging

logger = logging.getLogger(__name__)


class TagsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Tag.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


def home(request):
    # images_list = Image.objects.select_related('author').all().prefetch_related(
    #     Prefetch('image_user_actions', ImageUserActions.objects.filter(user_id=request.user.pk))
    # )
    # return HttpResponse(images_list[0].title)
    query = request.GET.get('q')

    if query:
        try:
            query_dict = json.load(StringIO(urlparse(query).path))
        except json.decoder.JSONDecodeError:
            return HttpResponseRedirect('/')
    else:
        query_dict = {'in': {'status': [Image.Status.APPROVED]}}

    query = DictORM().make(query_dict)

    try:
        images_list = Image.objects.select_related('author').filter(**query.kwargs).order_by('-created_at').prefetch_related(
            Prefetch('image_user_actions', ImageUserActions.objects.filter(user_id=request.user.pk))
        ).distinct()
        if query.order_list:
            images_list = images_list.order_by(*query.order_list)
    except (validators.ValidationError, exceptions.FieldError):
        return HttpResponseRedirect('/')

    paginator = Paginator(images_list, settings.IMAGE_MAXIMUM_COUNT_PER_PAGE)
    images_list = paginator.get_page(request.GET.get('page'))

    images_list = ImagesSerializer(images_list, many=True)
    images_list = JsonResponse(images_list.data, safe=False)

    return render(request, 'home.html', {
        'images_list': images_list.content.decode(),
        'number_of_columns': settings.IMAGE_COLUMNS,
        'total_pages': paginator.num_pages,
        'page': request.GET.get('page'),
        #'color': color,
        'common_tags': Image.tags.most_common()[:settings.DISPLAY_MOST_COMMON_TAGS_COUNT],
        'messages': messages.get_messages(request),
    })


def detailed_image_view(request, slug):
    image = get_object_or_404(Image, slug=slug)
    images_tags_ids = image.tags.values_list('id', flat=True)
    similar_images = Image.objects.select_related('author').filter(tags__in=images_tags_ids).exclude(id=image.id)
    similar_images = similar_images.annotate(same_tags=Count('tags')).order_by('-same_tags')[
                     :settings.SIMILAR_IMAGES_COUNT]
    similar_images = ImagesSerializer(similar_images, many=True)
    similar_images = JsonResponse(similar_images.data, safe=False)
    form = EditTagsForm(instance=image)
    report_form = ReportForm()

    if request.method == 'POST':
        if 'edit' in request.POST:
            form = EditTagsForm(data=request.POST, instance=image)
            if form.is_valid() and (request.user == image.author or is_moderator(request.user)):
                obj = form.save(commit=False)
                obj.save()
                form.save_m2m()
                return HttpResponseRedirect(reverse('main:detailed_image_view', kwargs={'slug': obj.slug}))

        report_form = ReportForm(data=request.POST)
        if not Report.objects.filter(image_id=image.pk, user_id=request.user.pk).exists():
            if report_form.is_valid():
                report = report_form.save(commit=False)
                report.user = request.user
                report.image = image
                report.save()

                message = str(
                    'Full name: ' + request.user.first_name + ' ' +
                    request.user.last_name + '\n' +
                    report.body
                )
                Mail.simple_message(
                    report.title,
                    message,
                    request.user.email,
                    [settings.REPORT_EMAIL]
                )
                messages.add_message(request, messages.SUCCESS, 'Report sent')
        else:
            messages.add_message(request, messages.ERROR, 'Report already sent')

    return render(request, 'detailed_image_view.html', {
        'image': image,
        'colors': image.colors.all(),
        'moderator': is_moderator(request.user),
        'form': form,
        'report_form': report_form,
        'images_list': similar_images.content.decode(),
        'number_of_columns': settings.IMAGE_COLUMNS,
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

    query = request.GET.get('q')
    if query:
        try:
            query_dict = json.load(StringIO(urlparse(query).path))
        except json.decoder.JSONDecodeError:
            return HttpResponseRedirect('/')
    else:
        query_dict = {'in': {'author': [request.user.pk]}}

    query = DictORM().make(query_dict)

    try:
        images_list = Image.objects.select_related('author').filter(**query.kwargs).order_by('-created_at').prefetch_related(
            Prefetch('image_user_actions', ImageUserActions.objects.filter(user_id=request.user.pk))
        ).distinct()
        if query.order_list:
            images_list = images_list.order_by(*query.order_list)
    except (validators.ValidationError, exceptions.FieldError):
        return HttpResponseRedirect('/')

    paginator = Paginator(images_list, settings.IMAGE_MAXIMUM_COUNT_PER_PAGE)
    images_list = paginator.get_page(request.GET.get('page'))

    images_list = ImagesSerializer(images_list, many=True)
    images_list = JsonResponse(images_list.data, safe=False)

    return render(request, 'cabinet.html', {
        'user': user,
        'images_display_status': True,
        'moderator': is_moderator(user),
        'messages': messages.get_messages(request),
        'images_list': images_list.content.decode(),
        'number_of_columns': settings.IMAGE_COLUMNS,
        'page': request.GET.get('page'),
        'total_pages': paginator.num_pages,
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


#@check_recaptcha
@login_required
def add_image(request):
    if request.method == 'POST':
        logger.error(request.FILES)
        image_form = ImageUploadForm(data=request.POST, files=request.FILES)
        #if request.recaptcha_is_valid and image_form.is_valid():
        if image_form.is_valid():
            image = image_form.save(commit=False)
            image.author = request.user
            image.save()
            image_form.service.resize_preview_image(image)
            image_form.service.add_colors(image)
            image_form.save_m2m()
            return redirect('main:detailed_image_view', slug=image.slug)
    else:
        image_form = ImageUploadForm()

    return render(request, 'add.html', {
        'image_form': image_form or None,
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
