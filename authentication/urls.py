from django.urls import path
from .views import login_usuario, logout_usuario, validar_credenciais

urlpatterns = [
    path('login/', login_usuario, name='login'),
    path('logout/', logout_usuario, name='logout'),
    path('validar-credenciais/', validar_credenciais, name='validar_credenciais'),
]