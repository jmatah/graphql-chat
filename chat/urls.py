from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('image_upload', csrf_exempt(views.image_upload), name="image-upload"), #ajax
]