from django.http import Http404
from django.shortcuts import render


SOUP_SLUGS = ("borsch", "solyanka", "ukha", "pumpkin", "broth")


def index(request, soup_slug=None):
    if soup_slug is not None and soup_slug not in SOUP_SLUGS:
        raise Http404("Soup not found")

    return render(
        request,
        "landing/index.html",
        {"initial_soup_slug": soup_slug or ""},
    )
