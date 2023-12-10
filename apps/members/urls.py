from django.conf.urls import url
from .views import get_members


app_name = "mebers"
urlpatterns = [
    url(r'^$', get_members, name='mebers'),
]