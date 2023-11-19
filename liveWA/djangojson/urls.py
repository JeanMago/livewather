# djangojson/urls.py

from django.urls import path
from .views import dados_json,micropar,gb_tracker

urlpatterns = [
    path('dados/', dados_json, name='dados_json'),
    path('microparticulas/', micropar, name='dados_json'),
    path('gb_tracker/', gb_tracker, name="json")
]
