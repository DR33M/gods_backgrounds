from ..models import Image


def get_image(image_pk):
    if image_pk:
        try:
            return Image.objects.get(pk=image_pk)
        except Image.DoesNotExist:
            return False


def get_images(kwargs, order):
    try:
        if kwargs:
            return Image.objects.select_related('author').filter(**kwargs).order_by(order).distinct()
        else:
            return Image.objects.select_related('author').order_by(order).distinct()
    except Image.DoesNotExist:
        return False


def between(field, start, end):
    kwargs = {}
    gte = '__gte'
    lte = '__lte'

    if start and end:
        kwargs = {field + gte: start, field + lte: end}
    elif start:
        kwargs = {field + gte: start}
    elif end:
        kwargs = {field + lte: end}

    return kwargs


def bigger_then(fields, operation='__gte'):
    kwargs = {}

    for field in fields:
        if 'name' in field and 'value' in field:
            kwargs[field['name'] + operation] = field['value']

    return kwargs


def in_list(field, key):
    kwargs = {field + '__in': key}

    return kwargs
