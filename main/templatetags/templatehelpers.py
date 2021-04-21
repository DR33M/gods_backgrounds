from django import template
from django.conf import settings
from django.db.models import Count

register = template.Library()

T_MAX = getattr(settings, 'TAGCLOUD_MAX', 24.0)
T_MIN = getattr(settings, 'TAGCLOUD_MIN', 50.0)


@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url


def get_weight(t_min, t_max, tags_count_min, tags_count_max):
    def weight(tags_count, t_min=t_min, t_max=t_max, tags_count_min=tags_count_min, tags_count_max=tags_count_max):
        if tags_count_max == tags_count_min:
            mult_fac = 1.0
        else:
            mult_fac = float(t_max - t_min) / float(tags_count_max - tags_count_min)

        return t_max - (tags_count_max - tags_count) * mult_fac

    return weight


@register.simple_tag
def get_tag_weight(queryset):
    queryset = queryset.annotate(num_times=Count('image'))
    num_times = queryset.values_list('num_times', flat=True)

    weight = get_weight(T_MIN, T_MAX, min(num_times), max(num_times))

    for tag in queryset:
        tag.weight = weight(tag.num_times)

    return queryset
