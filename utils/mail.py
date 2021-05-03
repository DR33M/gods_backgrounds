from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class Messages:
    @staticmethod
    def get_protocol(request):
        if request.is_secure:
            return 'http'
        return 'https'

    @staticmethod
    def activate(request, user, message_template, field):
        protocol = Messages.get_protocol(request)

        current_site = get_current_site(request)
        mail_subject = 'Confirm action'
        message = render_to_string(message_template, {
            'protocol': protocol,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
            'field': field,
        })

        email = EmailMessage(mail_subject, message, to=[user.email])
        email.send()

    @staticmethod
    def simple_message(title, message, from_email, to):
        title = title
        message = message

        email = EmailMessage(title, message, from_email, to=to)
        email.send()
