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
    def send_message(request, user, message_template, field):
        if request.is_secure:
            protocol = 'http'
        else:
            protocol = 'https'

        current_site = get_current_site(request)
        mail_subject = 'Confirm action'
        message = render_to_string(message_template, {
            'protocol': protocol,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
            'field': field,
        })

        email = EmailMessage(
            mail_subject, message, to=[user.email]
        )
        email.send()
