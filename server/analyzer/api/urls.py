from django.urls import path

from .views import WordViewSet, TextViewSet

urlpatterns = [
    path('words/', WordViewSet.as_view()),
    path('text/', TextViewSet.as_view())
]
