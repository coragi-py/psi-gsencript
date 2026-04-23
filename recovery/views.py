from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from accounts.models import User
from audit.models import AuditLog
import secrets
import json

@csrf_exempt
def solicitar_recuperacao(request):
    # Item 2.1 e 2.2: Solicitação e geração de token seguro
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        
        user = User.objects.filter(email=email).first()
        if user:
            # Gera o token e define expiração item 2.3
            user.recovery_token = secrets.token_urlsafe(32)
            user.token_expiration = timezone.now() + timezone.timedelta(minutes=10)
            user.save()
            
            return JsonResponse({
                "mensagem": "Token gerado com sucesso",
                "token": user.recovery_token
            }, status=200)
        
        AuditLog.objects.create(
            usuario=user,
            evento="RECUPERACAO_SOLICITADA",
            ip_origem=request.META.get('REMOTE_ADDR'),
            detalhes="Token de recuperação gerado e enviado ao sistema."
        )
            
        return JsonResponse({"erro": "E-mail não encontrado"}, status=404)

@csrf_exempt
def resetar_senha(request):
    # Item 2.4 e 2.5: Validação de token e alteração da senha
    if request.method == 'POST':
        data = json.loads(request.body)
        token = data.get('token')
        nova_senha = data.get('nova_senha')
        
        user = get_object_or_404(User, recovery_token=token)
        
        # Verifica expiração do token
        if timezone.now() > user.token_expiration:
            return JsonResponse({"erro": "Token expirado"}, status=400)
        
        # Define a nova senha usando o hash do Django (Argon2)
        user.set_password(nova_senha) 
        user.recovery_token = None # Invalida o token item 2.5
        user.token_expiration = None
        user.save()

        AuditLog.objects.create(
            usuario=user,
            evento="RECUPERACAO_SUCESSO",
            ip_origem=request.META.get('REMOTE_ADDR'),
            detalhes="Senha alterada com sucesso via token de recuperação."
        )
        
        return JsonResponse({"mensagem": "Senha atualizada com sucesso"}, status=200)