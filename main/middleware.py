from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from main.models import Image
from utils.user import is_moderator


class ModeratorOnWorkMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        skip_urls = [
            reverse('main:moderator-panel'),
            reverse('main:tags-autocomplete')
        ]
        MEDIA_URL = request.path.startswith(settings.MEDIA_URL)
        STATIC_URL = request.path.startswith(settings.STATIC_URL)
        if request.user.is_authenticated and is_moderator(request.user) and not MEDIA_URL and not STATIC_URL:
            if request.path not in skip_urls and Image.objects.filter(moderator_id=request.user.id,
                                                                      status=Image.Status.MODERATION).exists():
                return HttpResponseRedirect(reverse('main:moderator-panel'))
        return response
