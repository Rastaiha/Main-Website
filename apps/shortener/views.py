from django.shortcuts import get_object_or_404, redirect

from apps.shortener.models import Shortener


def redirect_url(request, shortened_url):
    url = get_object_or_404(Shortener, shortened_url=shortened_url)
    url.clicked()
    return redirect(url.main_url)
