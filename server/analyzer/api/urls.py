from django.urls import path

from server.analyzer.api import views

urlpatterns = [
    path('', views.resp, name='resp'),
]
