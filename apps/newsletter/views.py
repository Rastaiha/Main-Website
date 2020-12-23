import django
from django.shortcuts import render

# Create your views here.
from apps.newsletter.models import Subscriber


def unsubscribe(request, uid):
    try:
        s = Subscriber.objects.get(unique_id=uid)
    except Subscriber.DoesNotExist:
        response = render(request, 'base/404.html')
        response.status_code = 404
        return response
    s.unsubscribed = True
    s.date_unsubscribed = django.utils.timezone.now()
    s.save()
    return render(request, 'newsletter/unsubscribe.html')
