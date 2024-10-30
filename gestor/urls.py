# gestor/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'gestor'

urlpatterns = [
    path('dashboard/', views.dashboard_gestor, name='dashboard_gestor'),  # Dashboard do gestor
    path('login/', views.login_gestor, name='login_gestor'),  # Rota de login do gestor
    path('logout/', auth_views.LogoutView.as_view(template_name='core/login_gestor.html'), name='logout'),  # Rota de logout do gestor
]
