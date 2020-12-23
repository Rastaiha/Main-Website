from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import render


def handler404(request, *args, **argv):
    response = render(request, 'base/404.html')
    response.status_code = 404
    return response

