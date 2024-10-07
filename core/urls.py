# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Página inicial
    path('login/', views.login_view, name='login'),  # Login normal
    path('login/rh/', views.login_rh, name='login_rh'),  # Login como RH
    path('login/gestor/', views.login_gestor, name='login_gestor'),  # Login como Gestor
]
