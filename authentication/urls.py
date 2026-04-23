from django.urls import path
from .views import login_usuario, logout_usuario

urlpatterns = [
    path('login/', login_usuario, name='login'),
    path('logout/', logout_usuario, name='logout'),
]