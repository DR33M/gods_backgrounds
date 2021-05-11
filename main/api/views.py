import json
from io import StringIO
from urllib.parse import urlparse

from django.conf import settings
from django.core import validators
from django.core import exceptions
from django.db.models import Prefetch
from django.core.paginator import Paginator

from rest_framework import status, generics, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.decorators import action
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from taggit.models import Tag

from .serializers import ImagesSerializer, EditTagsSerializer, TagsSerializer

from ..models import ImageUserActions, Image

from ..utils.DictORM import DictORM

import logging

logger = logging.getLogger(__name__)


class ImageViewSet(viewsets.ModelViewSet):
    @action(detail=True, methods=['GET'], permission_classes=[AllowAny], throttle_classes=[UserRateThrottle, AnonRateThrottle])
    def get(self, request):
        query = request.GET.get('q')

        if query:
            try:
                query_dict = json.load(StringIO(urlparse(query).geturl()))
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

    @action(detail=True, methods=['PATCH'], permission_classes=[IsAuthenticated], throttle_classes=[UserRateThrottle])
    def change_rating(self, request, pk=''):
        vote = int(request.data) or None
        if vote == -1 or vote == 1:
            try:
                image = Image.objects.get(pk=pk)
            except (Image.DoesNotExist, Image.MultipleObjectsReturned):
                image = None

            if image:
                try:
                    actor = ImageUserActions.objects.get(user_id=request.user.pk, image_id=pk)
                except ImageUserActions.DoesNotExist:
                    image.image_user_actions.add(request.user)
                    actor = ImageUserActions.objects.get(user_id=request.user.pk, image_id=pk)

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

    @action(detail=True, methods=['PATCH'], permission_classes=[IsAuthenticated], throttle_classes=[UserRateThrottle])
    def add_download(self, request, pk=''):
        download_number = int(request.data) or None

        if download_number == 1:
            try:
                image = Image.objects.get(pk=pk)
            except (Image.DoesNotExist, Image.MultipleObjectsReturned):
                image = None

            if image:
                downloaded = False
                try:
                    actor = ImageUserActions.objects.get(user_id=request.user.pk, image_id=pk)
                    downloaded = actor.downloaded
                    if not actor.downloaded:
                        actor.downloaded = True
                        actor.save()
                except ImageUserActions.DoesNotExist:
                    image.image_user_actions.add(request.user)
                    ImageUserActions.objects.filter(user_id=request.user.pk, image_id=pk).update(downloaded=True)

                if not downloaded:
                    image.downloads = image.downloads + 1
                    image.save()

                return Response(data={'count': image.downloads}, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'], permission_classes=[IsAdminUser], throttle_classes=[UserRateThrottle])
    def mp_get(self, request):
        try:
            image = Image.objects.get(moderator_id=request.user.id, status=Image.Status.MODERATION)
        except Image.DoesNotExist:
            image = Image.objects.select_related('author').filter(moderator_id=None, status=Image.Status.MODERATION).first()

            if not image:
                return Response({'message': 'The image does not exist'}, status.HTTP_404_NOT_FOUND)

            image.moderator_id = request.user.id
            image.save()

        return Response(data=ImagesSerializer(image).data, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['PATCH'], permission_classes=[IsAdminUser], throttle_classes=[UserRateThrottle])
    def mp_approve(self, request, pk):
        try:
            image = Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        tags_data = JSONParser().parse(request)
        tags_serializer = EditTagsSerializer(image, data=tags_data)
        if tags_serializer.is_valid():
            tags_serializer.save(status=Image.Status.APPROVED)
            return Response({'message': 'Image has been approved', 'status': 'success'}, status=status.HTTP_202_ACCEPTED)
        return Response(tags_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['DELETE'], permission_classes=[IsAuthenticated], throttle_classes=[UserRateThrottle])
    def delete(self, request, pk):
        try:
            image = Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if image.author.pk == request.user.pk or request.user.is_staff:
            image.delete()
        return Response({'message': 'Image was deleted successfully!', 'status': 'success'}, status=status.HTTP_200_OK)


@throttle_classes([UserRateThrottle, AnonRateThrottle])
class Tags(generics.ListAPIView):
    serializer_class = TagsSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = Tag.objects.all()
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset