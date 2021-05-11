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
        MAIN_API_URL = request.path.startswith('/api/')
        ACCOUNTS_API_URL = request.path.startswith('/accounts/api/')
        MEDIA_URL = request.path.startswith(settings.MEDIA_URL)
        STATIC_URL = request.path.startswith(settings.STATIC_URL)
        if request.user.is_authenticated and is_moderator(request.user):
            if not reverse('main:moderator-panel') == request.path and not (MAIN_API_URL or ACCOUNTS_API_URL or MEDIA_URL or STATIC_URL):
                if Image.objects.filter(moderator_id=request.user.id, status=Image.Status.MODERATION).exists():
                    return HttpResponseRedirect(reverse('main:moderator-panel'))
        return response
