"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import login_ui, chat_ui, register_ui  #  Added register_ui

urlpatterns = [
    path('admin/', admin.site.urls),

    # UI pages
    path('login/', login_ui, name='login-ui'),
    path('chat-ui/', chat_ui, name='chat-ui'),
    path('register/', register_ui, name='register-ui'),  #  Register UI route

    # API routes
    path('api/users/', include('users.urls')),     # Users app routes
    path('api/chat/', include('chats.urls')),      # Chat app routes
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

