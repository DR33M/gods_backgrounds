from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class Messages:
    @staticmethod
    def activate(request, user):
        current_site = get_current_site(request)
        mail_subject = 'Activate your account.'
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })

        email = EmailMessage(
            mail_subject, message, to=[user.email]
        )
        email.send()

    @staticmethod
    def new_email(request, to_email):
        user = request.user
        current_site = get_current_site(request)
        mail_subject = 'Confirm your new email address'
        message = render_to_string('acc_new_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
            'email': to_email,
        })

        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
