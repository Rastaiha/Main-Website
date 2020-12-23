from django.conf.urls import url
from apps.shortener import views
from django.urls import path

app_name = "shortener"
urlpatterns = [
    path('<str:shortened_url>/', views.redirect_url)
]