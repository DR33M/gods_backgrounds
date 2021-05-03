from django.conf import settings


def site_title_processor(request):
    return {'SITE_TITLE': settings.SITE_TITLE}
