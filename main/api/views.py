from rest_framework.generics import ListAPIView
from main.api.serializers import ImageSerializer
from main.api.pagination import ImagePageNumberPagination
from main.models import Image


class ImageView(ListAPIView):
    serializer_class = ImageSerializer
    pagination_class = ImagePageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Image.objects.filter(status=Image.Status.APPROVED).order_by("-created_at")
        return queryset_list
