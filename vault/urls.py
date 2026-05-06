from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='vault_index'),
    
    path('listar/', views.listar_senhas, name='listar_senhas'),
    path('adicionar/', views.adicionar_senha, name='adicionar_senha'),
    path('excluir/<int:senha_id>/', views.excluir_senha, name='excluir_senha'),
    path('editar/<int:senha_id>/', views.editar_senha, name='editar_senha'),
]