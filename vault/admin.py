from django.contrib import admin
from .models import CredencialCofre

@admin.register(CredencialCofre)
class CredencialCofreAdmin(admin.ModelAdmin):
    # O que aparece na lista de itens do admin
    list_display = ('titulo', 'usuario', 'username_site', 'data_criacao')

    # Filtros laterais para facilitar a busca
    list_filter = ('usuario', 'data_criacao')

    # Barra de busca para encontrar itens rapidamente
    search_fields = ('titulo', 'username_site', 'usuario__email')

    # Deixa o campo da senha criptografada e as datas como somente leitura para evitar alterações acidentais
    readonly_fields = ('senha_site_cifrada', 'data_criacao', 'data_atualizacao')

    fieldsets = (
        ('Identificação', {
            'fields': ('usuario', 'titulo', 'url_site')
        }),
        ('Credenciais (Criptografadas)', {
            'fields': ('username_site', 'senha_site_cifrada'),
            'description': "A senha abaixo está protegida por criptografia AES-256."
        }),
        ('Metadados', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',) #Deixa recolhido para não poluir a interface
        }),
    )