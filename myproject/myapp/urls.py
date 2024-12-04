# myapp/urls.py

from django.urls import path
from .views import register, authenticate_user, protected_resource

urlpatterns = [
    path('register/', register, name='register'),
    path('authenticate/', authenticate_user, name='authenticate'),
    path('protected-resource/', protected_resource, name='protected-resource'),
]