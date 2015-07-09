"""
This file contains utility functions which will responsible for sending emails.
"""
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.translation import ugettext as _

from edxmako.shortcuts import render_to_string
from microsite_configuration import microsite
from openedx.core.djangoapps.user_api.accounts.api import get_account_settings
from xmodule.modulestore.django import modulestore


log = logging.getLogger(__name__)


def send_credit_notifications(username, course_key, email_type="credit_eligibility"):
    """
    Sends email to the user if he/she became eligible for the course.
    """
    user = None
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        log.debug('No user with %s exist', username)

    account_settings = get_account_settings(user)
    course = modulestore().get_course(course_key, depth=0)
    course_display_name = course.display_name
    # TODO: change context according to email type
    context = {
        'full_name': account_settings['name'],
        'platform_name': settings.PLATFORM_NAME,
        'course_name': course_display_name,
    }

    from_address = microsite.get_value('default_from_email', settings.DEFAULT_FROM_EMAIL)
    to_address = account_settings['email']

    # TODO: change subject and message according to email type
    if email_type == "credit_receipt":
        subject = _("Credit Course Payment Receipt")
        message = render_to_string('emails/credit_payment_receipt.txt', context)
    else:
        subject = _("Course Credit Eligibility")
        message = render_to_string('emails/credit_eligibility_email.txt', context)

    send_mail(subject, message, from_address, [to_address], fail_silently=False)
