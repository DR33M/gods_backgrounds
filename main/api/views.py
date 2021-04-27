import json
from io import StringIO
from urllib.parse import urlparse
from django.core.cache import cache

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import ImagesSerializer

from ..models import UserImage, Image

from ..utils.DictORM import DictORM

import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([AllowAny])
def images(request):
    query = request.GET.get('q')
    response = {'status': status.HTTP_200_OK}

    if query:
        query_dict = {}
        try:
            query_dict = json.load(StringIO(urlparse(query).path))
        except json.decoder.JSONDecodeError:
            response['status'] = status.HTTP_400_BAD_REQUEST

        if query_dict:
            query = DictORM().make(query_dict)

            images_list = Image.objects.select_related('author').filter(**query.kwargs).order_by('-created_at')
            if query.order_list:
                images_list = images_list.order_by(*query.order_list)

            if images_list:
                images_list = ImagesSerializer(images_list, many=True)
                response = {'data': images_list.data, 'status': status.HTTP_200_OK}
            else:
                response['status'] = status.HTTP_404_NOT_FOUND

    return Response(**response)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def rating(request, image_pk=''):
    image = Image.objects.get(pk=image_pk)
    if image:
        if 'vote' in request.data:
            if not UserImage.objects.filter(user_id=request.user.pk, image_id=image.pk).exclude(vote=UserImage.Vote.DEFAULT).exists():
                vote = int(request.data['vote'])
                image.rating = image.rating + vote
                image.save()

                UserImage(user=request.user, image=image, vote=vote).save()
                return Response(image.rating, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(image.rating, status=status.HTTP_208_ALREADY_REPORTED)
    else:
        return Response(status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def downloads(request, image_pk=''):
    image = Image.objects.get(pk=image_pk)

    if image and not UserImage.objects.filter(user_id=request.user.pk, image_id=image.pk, downloaded=True).exists():
        image.downloads = image.downloads + 1
        image.save()

        UserImage(user=request.user, image=image, downloaded=True).save()
        return Response(image.rating, status=status.HTTP_202_ACCEPTED)
    else:
        return Response(image.rating, status=status.HTTP_208_ALREADY_REPORTED)
