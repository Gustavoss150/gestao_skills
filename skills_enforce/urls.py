"""
URL configuration for skills_enforce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
# skills_enforce/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # Corrigido: Import da view de autenticação

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Inclui as rotas do app core
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Rota para o login do Django
    path('gestor/', include('gestor.urls')),
]


