from django.conf import settings
from django.contrib import messages
import requests


def check_recaptcha(function):
    def wrapper(request, *args, **kwargs):
        request.recaptcha_is_valid = None
        if request.method == 'POST':
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if result['success']:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False
                messages.add_message(request, messages.ERROR, 'Invalid reCAPTCHA. Please try again.')
        return function(request, *args, **kwargs)

    return wrapper
