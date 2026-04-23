import json
import pyotp
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from accounts.models import User

@csrf_exempt
def login_usuario(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            token_2fa = data.get('token_2fa')

            # Autenticação Primária item 1.1 / Utiliza o Argon2 automaticamente no password
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Verificação do Segundo Fator item 1.5 e 1.6
                if not user.two_factor_secret:
                    return JsonResponse({"erro": "2FA não configurado para este usuário."}, status=400)
                
                totp = pyotp.TOTP(user.two_factor_secret)
                if totp.verify(token_2fa):
                    # Inicia a sessão item 1.9
                    login(request, user)
                    
                    return JsonResponse({
                        "mensagem": "Login realizado com sucesso!",
                        "usuario": user.username
                    }, status=200)
                else:
                    return JsonResponse({"erro": "Código 2FA inválido."}, status=401)
            else:
                return JsonResponse({"erro": "Credenciais inválidas."}, status=401)

        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=500)

    return JsonResponse({"erro": "Método não permitido"}, status=405)

@csrf_exempt
def logout_usuario(request):
    if request.method == 'POST':
        # Item 1.10 Logout da sessão atual
        logout(request) 
        return JsonResponse({"mensagem": "Sessão encerrada com sucesso."}, status=200)
    
    return JsonResponse({"erro": "Método não permitido"}, status=405)