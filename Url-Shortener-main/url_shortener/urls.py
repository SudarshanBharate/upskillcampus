# url_shortener/urls.py
from django.urls import path
from .views import index, url_mappings, redirect_to_original

urlpatterns = [
    path('', index, name='index'),
    path('url-mappings/', url_mappings, name='url_mappings'),
    path('<str:short_url>/', redirect_to_original, name='redirect_to_original'),
]

