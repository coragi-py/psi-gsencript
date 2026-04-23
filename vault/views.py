import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import CredencialCofre

@login_required
def listar_senhas(request):
    # Verifica se o consentimento está ativo
    if not hasattr(request.user, 'consentimento') or not request.user.consentimento.consentimento_ativo:
        return JsonResponse({"erro": "Acesso negado. Consentimento LGPD não está ativo."}, status=403)

    senhas = CredencialCofre.objects.filter(usuario=request.user)
    data = [{
        "id": s.id,
        "titulo": s.titulo,
        "url": s.url_site,
        "username": s.username_site,
        "senha": s.get_senha()  # Descriptografa a senha para exibição
    } for s in senhas]
    
    return JsonResponse(data, safe=False)

@csrf_exempt
@login_required
def adicionar_senha(request):
    if request.method == 'POST':
        # Validação de consentimento LGPD antes de permitir a ação
        if not request.user.consentimento.consentimento_ativo:
            return JsonResponse({"erro": "Ação bloqueada por falta de consentimento LGPD."}, status=403)

        try:
            data = json.loads(request.body)
            
            nova_senha = CredencialCofre(
                usuario=request.user,
                titulo=data.get('titulo'),
                url_site=data.get('url'),
                username_site=data.get('username')
            )
            # Aplica a criptografia AES
            nova_senha.set_senha(data.get('senha'))
            # Salva no banco
            nova_senha.save()

            return JsonResponse({"mensagem": "Credencial armazenada com sucesso!"}, status=201)
        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=400)
    
    return JsonResponse({"erro": "Método não permitido"}, status=405)

@csrf_exempt
@login_required
def editar_senha(request, senha_id):
    if request.method in ['PUT', 'POST']:
        # 1. Validação de Consentimento LGPD
        if not hasattr(request.user, 'consentimento') or not request.user.consentimento.consentimento_ativo:
            return JsonResponse({"erro": "Ação bloqueada. Consentimento LGPD revogado."}, status=403)

        try:
            # 2. Segurança contra IDOR: Garante que o usuário só edite o que é dele
            credencial = CredencialCofre.objects.get(id=senha_id, usuario=request.user)
            
            data = json.loads(request.body)
            
            # Atualiza os campos se eles forem enviados no JSON
            credencial.titulo = data.get('titulo', credencial.titulo)
            credencial.url_site = data.get('url', credencial.url_site)
            credencial.username_site = data.get('username', credencial.username_site)
            
            if 'senha' in data:
                credencial.set_senha(data.get('senha'))  # Aplica a criptografia AES na nova senha

            # 3. O .save() dispara o signal 'post_save' com created=False
            credencial.save()
            
            return JsonResponse({"mensagem": "Credencial atualizada e criptografada com sucesso!"}, status=200)

        except CredencialCofre.DoesNotExist:
            return JsonResponse({"erro": "Credencial não encontrada ou permissão negada."}, status=404)
        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=400)

    return JsonResponse({"erro": "Método não permitido"}, status=405)

@csrf_exempt
@login_required
def excluir_senha(request, senha_id):
    # 
    if request.method in ['DELETE', 'POST']:
        
        # Checagem LGPD
        if not hasattr(request.user, 'consentimento') or not request.user.consentimento.consentimento_ativo:
            return JsonResponse({"erro": "Ação bloqueada. LGPD Revogada."}, status=403)

        try:
            # SEGURANÇA (Prevenção de IDOR): Filtro pelo ID e OBRIGATORIAMENTE pelo usuário logado.
            credencial = CredencialCofre.objects.get(id=senha_id, usuario=request.user)
            
            # Ao chamar o .delete(), o Django vai lá no audit/signals.py e dispara o Item 5.2 automaticamente
            credencial.delete()
            
            return JsonResponse({"mensagem": "Credencial excluída com sucesso do seu cofre."}, status=200)
            
        except CredencialCofre.DoesNotExist:
            return JsonResponse({"erro": "Credencial não encontrada ou você não tem permissão para excluí-la."}, status=404)
            
    return JsonResponse({"erro": "Método não permitido"}, status=405)