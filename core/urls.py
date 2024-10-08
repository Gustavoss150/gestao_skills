from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Página inicial
    path('login/', views.login_view, name='login'),  # Login normal
    path('login/rh/', views.login_rh, name='login_rh'),  # Login como RH
    path('login/gestor/', views.login_gestor, name='login_gestor'),  # Login como Gestor
    path('dashboard/gestor/', views.dashboard_gestor, name='dashboard_gestor'),  # Dashboard do Gestor
]