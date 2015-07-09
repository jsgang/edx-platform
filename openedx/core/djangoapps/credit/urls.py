"""
URLs for the credit app.
"""
from django.conf.urls import patterns, url

from .views import create_credit_request, credit_provider_callback, get_provider_detail

urlpatterns = patterns(
    '',

    url(
        r"^v1/provider/(?P<provider_id>[^/]+)/request/$",
        create_credit_request,
        name="create_request"
    ),

    url(
        r"^v1/provider/(?P<provider_id>[^/]+)/callback/?$",
        credit_provider_callback,
        name="provider_callback"
    ),

    url(
        r"^v1/provider/info/(?P<provider_id>[^/]+)/?$",
        get_provider_detail,
        name="provider_details"
    ),
)
