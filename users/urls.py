from django.urls import path
from .views import register_user, token_balance

urlpatterns = [
    path('register/', register_user, name='register'),
    path('tokens/', token_balance, name='token_balance'),
]
