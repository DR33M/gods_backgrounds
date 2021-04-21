import json
from io import StringIO

from django.core.cache import cache

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from ..models import UserImage

from .serializers import ImagesSerializer

from ..utils import sort


@api_view(['GET'])
@permission_classes([AllowAny])
def find(request):
    images = {}
    order = request.GET.get('order', default='-tags__name')
    key = json.load(StringIO(request.GET.get('key', default='')))

    if key:
        kwargs = sort.in_list('tags__name', key)
        images = sort.get_images(kwargs, order)

    if images:
        images = ImagesSerializer(images, many=True)
        return Response(images.data, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny])
def sorting(request):
    images = None
    field = request.GET.get('field')
    order = request.GET.get('order', default='-created_at')

    if field == 'created_at' or field == 'downloads' or field == 'rating':
        start = request.GET.get('start', default='')
        end = request.GET.get('end', default='')
        kwargs = sort.between(field, start, end)

        images = sort.get_images(kwargs, order)
    elif field == 'screen':
        fields = json.load(StringIO(request.GET.get('fields')))

        if fields:
            kwargs = sort.bigger_then(fields)
            images = sort.get_images(kwargs, order)

    if images:
        images = ImagesSerializer(images, many=True)
        return Response(images.data, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def rating(request, image_pk=''):
    image = sort.get_image(image_pk)

    if image and request.method == 'PUT':
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
    image = sort.get_image(image_pk)

    if image and not UserImage.objects.filter(user_id=request.user.pk, image_id=image.pk, downloaded=True).exists():
        image.downloads = image.downloads + 1
        image.save()

        UserImage(user=request.user, image=image, downloaded=True).save()
        return Response(image.rating, status=status.HTTP_202_ACCEPTED)
    else:
        return Response(image.rating, status=status.HTTP_208_ALREADY_REPORTED)
