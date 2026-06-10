from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("soup/<slug:soup_slug>/", views.index, name="soup-detail"),
]
