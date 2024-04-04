from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from .models import URL
import hashlib


def generate_short_url(original_url, custom_suffix=None):
    if custom_suffix:
        short_url = "short." + custom_suffix
    else:
        hash_object = hashlib.md5(original_url.encode())
        hash_hex = hash_object.hexdigest()
        # Take the first 4 characters of the hash
        short_url = "short." + hash_hex[:4]
    return short_url


def index(request):
    short_url = None

    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        # Get custom suffix from the form
        custom_suffix = request.POST.get('custom_suffix')

        existing_url = URL.objects.filter(original_url=original_url).first()

        if existing_url:
            short_url = existing_url.short_url
        else:
            # Pass custom_suffix to generate_short_url
            short_url = generate_short_url(original_url, custom_suffix)
            URL.objects.create(original_url=original_url, short_url=short_url)

    return render(request, 'url_shortener/index.html', {'short_url': short_url})


def url_mappings(request):
    url_mappings = URL.objects.all()
    return render(request, 'url_shortener/url_mappings.html', {'url_mappings': url_mappings})


def redirect_to_original(request, short_url):
    try:
        mapping = URL.objects.get(short_url=short_url)
        return redirect(mapping.original_url)
    except URL.DoesNotExist:
        return HttpResponseNotFound("Shortened URL not found.")
