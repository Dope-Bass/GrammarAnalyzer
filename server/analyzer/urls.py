from django.urls import path

from . import views

urlpatterns = [
    path('', views.resp, name='resp'),
]
