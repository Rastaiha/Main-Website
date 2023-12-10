from django.conf.urls import url
from django.urls import path, include
from apps.contact_us.views import get_contact_us


app_name = "contact_us"
urlpatterns = [
    url(r'^$', get_contact_us, name='contact_us'),
]