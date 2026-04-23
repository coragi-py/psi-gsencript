import base64
from django.db import models
from django.conf import settings
from cryptography.fernet import Fernet

# Geração da Chave Criptográfica Mestre
def get_fernet():
    """Deriva uma chave AES válida de 32 bytes a partir da SECRET_KEY do Django (Item 3.6)."""
    key_bytes = settings.SECRET_KEY.encode('utf-8')
    chave_32_bytes = key_bytes[:32].ljust(32, b'x') # 32 bytes
    chave_b64 = base64.urlsafe_b64encode(chave_32_bytes)
    return Fernet(chave_b64)

class CredencialCofre(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='itens_cofre')
    titulo = models.CharField(max_length=100)
    url_site = models.URLField(blank=True, null=True)
    username_site = models.CharField(max_length=150)
    
    # O campo real no banco de dados que guarda os bytes ininteligíveis (AES)
    senha_site_cifrada = models.CharField(max_length=500)
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    # Criptografia em Repouso
    def set_senha(self, raw_password):
        """Criptografa a senha antes de salvá-la no banco."""
        f = get_fernet()
        # Transforma a senha em bytes cifrados e salva como texto
        self.senha_site_cifrada = f.encrypt(raw_password.encode('utf-8')).decode('utf-8')

    def get_senha(self):
        """Descriptografa a senha para devolver ao usuário legítimo."""
        try:
            f = get_fernet()
            return f.decrypt(self.senha_site_cifrada.encode('utf-8')).decode('utf-8')
        except Exception:
            return "ERRO_DE_DESCRIPTOGRAFIA"

    def __str__(self):
        return f"{self.titulo} - {self.username_site}"