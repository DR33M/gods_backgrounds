import json
from io import StringIO
from urllib.parse import urlparse

from django.conf import settings
from django.core import validators
from django.core import exceptions
from django.db.models import Prefetch
from django.core.paginator import Paginator

from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import ImagesSerializer

from ..models import ImageUserActions, Image

from ..utils.DictORM import DictORM

import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([AllowAny])
@throttle_classes([UserRateThrottle, AnonRateThrottle])
def images(request):
    query = request.GET.get('q')

    if query:
        try:
            query_dict = json.load(StringIO(urlparse(query).path))
        except json.decoder.JSONDecodeError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        query = DictORM().make(query_dict)
        try:
            images_list = Image.objects.select_related('author').filter(**query.kwargs).order_by('-created_at').prefetch_related(
                Prefetch('image_user_actions', ImageUserActions.objects.filter(user_id=request.user.pk))
            ).distinct()
            if query.order_list:
                images_list = images_list.order_by(*query.order_list)
        except (validators.ValidationError, exceptions.FieldError):
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        images_list = Image.objects.select_related('author').order_by('-created_at').prefetch_related(
            Prefetch('image_user_actions', ImageUserActions.objects.filter(user_id=request.user.pk))
        ).distinct()

    if images_list:
        paginator = Paginator(images_list, settings.IMAGE_MAXIMUM_COUNT_PER_PAGE)
        images_list = paginator.get_page(request.GET.get('page'))

        images_list = ImagesSerializer(images_list, many=True)
        return Response(data={'images': images_list.data, 'total_pages': paginator.num_pages}, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def rating(request, image_pk=''):
    vote = int(request.data) or None
    if vote == -1 or vote == 1:
        try:
            image = Image.objects.get(pk=image_pk)
        except (Image.DoesNotExist, Image.MultipleObjectsReturned):
            image = None

        if image:
            try:
                actor = ImageUserActions.objects.get(user_id=request.user.pk, image_id=image_pk)
            except ImageUserActions.DoesNotExist:
                image.image_user_actions.add(request.user)
                actor = ImageUserActions.objects.get(user_id=request.user.pk, image_id=image_pk)

            previous_vote = actor.vote

            if actor.vote + vote > ImageUserActions.Vote.UPVOTE:
                actor.vote = ImageUserActions.Vote.DOWNVOTE
                vote = -2
            elif actor.vote + vote < ImageUserActions.Vote.DOWNVOTE:
                actor.vote = ImageUserActions.Vote.UPVOTE
                vote = 2
            else:
                actor.vote = actor.vote + vote

            actor.save()
            if actor.vote == ImageUserActions.Vote.DEFAULT:
                image.rating = image.rating - previous_vote
            else:
                image.rating = image.rating + vote

            image.save()

            return Response(data={'count': image.rating, 'vote': actor.vote}, status=status.HTTP_202_ACCEPTED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def downloads(request, image_pk=''):
    download_number = int(request.data) or None

    if download_number == 1:
        try:
            image = Image.objects.get(pk=image_pk)
        except (Image.DoesNotExist, Image.MultipleObjectsReturned):
            image = None

        if image:
            downloaded = False
            try:
                actor = ImageUserActions.objects.get(user_id=request.user.pk, image_id=image_pk)
                downloaded = actor.downloaded
                if not actor.downloaded:
                    actor.downloaded = True
                    actor.save()
            except ImageUserActions.DoesNotExist:
                image.image_user_actions.add(request.user)
                ImageUserActions.objects.filter(user_id=request.user.pk, image_id=image_pk).update(downloaded=True)

            if not downloaded:
                image.downloads = image.downloads + 1
                image.save()

            return Response(data={'count': image.downloads}, status=status.HTTP_202_ACCEPTED)
    return Response(status=status.HTTP_400_BAD_REQUEST)
