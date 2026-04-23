from django.urls import path
from .views import revogar_consentimento, consultar_meus_dados, exportar_meus_dados, excluir_minha_conta

urlpatterns = [
    path('revogar/', revogar_consentimento, name='revogar_consentimento'),
    path('consultar/', consultar_meus_dados, name='consultar_meus_dados'),
    path('exportar/', exportar_meus_dados, name='exportar_meus_dados'),
    path('excluir/', excluir_minha_conta, name='excluir_minha_conta'),
]