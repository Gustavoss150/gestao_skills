from django.urls import path
from django.contrib.auth import views
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Página inicial
    path('login/rh/', views.login_rh, name='login_rh'),  # Login como RH
    path('login/gestor/', views.login_gestor, name='login_gestor'),  # Login como Gestor
    path('gestor/dashboard/', views.gestor_dashboard, name='gestor_dashboard'),  # Dashboard do Gestor
    path('notificacoes/', views.notificacoes, name='notificacoes'),
    path('notificacao/<int:notificacao_id>/marcar_lida/', views.marcar_notificacao_lida, name='marcar_notificacao_lida'),
    path('treinamentos/', views.treinamentos, name='treinamentos'),
]