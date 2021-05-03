from django import template
from django.conf import settings
from django.db.models import Count

register = template.Library()


@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url


def get_weight(num_times_min, num_times_max):
    def weight(tag_num_times, num_times_min=num_times_min, num_times_max=num_times_max):
        if num_times_max == num_times_min:
            factor = 1.0
        else:
            factor = float(settings.TAGS_CLOUD_MAX - settings.TAGS_CLOUD_MIN) / float(num_times_max - num_times_min)

        return settings.TAGS_CLOUD_MAX - (num_times_max - tag_num_times) * factor

    return weight


@register.simple_tag
def get_tag_weight(queryset):
    queryset = queryset.annotate(num_times=Count('image'))
    num_times = queryset.values_list('num_times', flat=True)

    weight = get_weight(min(num_times), max(num_times))

    queryset = sorted(queryset, key=lambda o: o.name)
    for tag in queryset:
        tag.weight = weight(tag.num_times)

    return queryset
