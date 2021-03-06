"""
Module defined send_validation function to verify emails.
"""
from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse


def send_validation(strategy, backend, code):
    """
    Send email validation link.
    """
    # TODO add email validating regex [^@]+@[^@]+\.[^@]+
    url = (reverse('social:complete', args=(backend.name,)) +
           '?verification_code=' + code.code)
    url = strategy.request.build_absolute_uri(url)
    send_mail(
        'Validate your account',
        'Validate your account {0}'.format(url),
        settings.EMAIL_FROM,
        [code.email],
        fail_silently=False
    )
