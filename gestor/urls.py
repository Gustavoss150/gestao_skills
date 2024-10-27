from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_gestor, name='dashboard_gestor'),  # Dashboard do gestor
    path('login/', views.login_gestor, name='login_gestor'),  # Rota de login do gestor
]
