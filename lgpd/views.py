from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from .models import ConsentimentoLGPD
from vault.models import CredencialCofre
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def revogar_consentimento(request):
    try:
        # Busca o consentimento do usuário logado
        consentimento = request.user.consentimento 
        
        if not consentimento.consentimento_ativo:
            return JsonResponse({"mensagem": "O consentimento já está revogado."}, status=400)
        
        # Chama o método para revogar o consentimento
        consentimento.revogar()
        
        return JsonResponse({
            "mensagem": "Consentimento revogado com sucesso. O acesso ao cofre foi bloqueado."
        }, status=200)
        
    except ConsentimentoLGPD.DoesNotExist:
        return JsonResponse({"erro": "Registro de consentimento não encontrado."}, status=404)

@login_required
def consultar_meus_dados(request):
    user = request.user
    
    try:
        consentimento = user.consentimento
        lgpd_info = {
            "aceite_termos": consentimento.aceite_termos,
            "finalidade": consentimento.finalidade,
            "data_aceite": consentimento.data_aceite.strftime("%d/%m/%Y %H:%M:%S"),
            "versao_termo": consentimento.versao_termo,
            "status_consentimento": "Ativo" if consentimento.consentimento_ativo else "Revogado"
        }
    except ConsentimentoLGPD.DoesNotExist:
        lgpd_info = "Registro de consentimento não encontrado."

    # Estrutura completa dos dados do titular
    dados_titular = {
        "perfil": {
            "username": user.username,
            "email": user.email,
            "data_cadastro": user.date_joined.strftime("%d/%m/%Y %H:%M:%S"),
            "ultimo_login": user.last_login.strftime("%d/%m/%Y %H:%M:%S") if user.last_login else "N/A"
        },
        "seguranca": {
            "autenticacao_dois_fatores": "Ativada" if user.two_factor_secret else "Desativada",
        },
        "lgpd": lgpd_info
    }

    return JsonResponse(dados_titular, json_dumps_params={'ensure_ascii': False})

@login_required
def exportar_meus_dados(request):
    user = request.user
    
    # 1. Dados de Identificação
    perfil = {
        "username": user.username,
        "email": user.email,
        "data_cadastro": user.date_joined.isoformat(),
    }
    
    # 2. Histórico de Consentimento (LGPD)
    try:
        consentimento = user.consentimento
        lgpd_info = {
            "aceite_termos": consentimento.aceite_termos,
            "finalidade": consentimento.finalidade,
            "data_aceite": consentimento.data_aceite.isoformat(),
            "versao_termo": consentimento.versao_termo,
            "status_atual": "Ativo" if consentimento.consentimento_ativo else "Revogado"
        }
    except ConsentimentoLGPD.DoesNotExist:
        lgpd_info = "Sem registro de consentimento."

    # 3. Dados do Cofre de Senhas 
    itens_cofre = CredencialCofre.objects.filter(usuario=user)
    cofre_data = []
    for item in itens_cofre:
        cofre_data.append({
            "titulo": item.titulo,
            "url": item.url_site,
            "username": item.username_site,
            # A senha é exportada CRIPTOGRAFADA. O texto claro nunca sai do banco para o JSON.
            "senha_cifrada": item.senha_site_cifrada
        })

    # 4. Estrutura Final do Arquivo
    dados_exportacao = {
        "exportado_em": timezone.now().isoformat(),
        "aplicacao": "Gerenciador de Senhas PI",
        "titular": perfil,
        "conformidade_lgpd": lgpd_info,
        "cofre": cofre_data
    }

    # Retorna o JSON formatado
    response = JsonResponse(dados_exportacao, json_dumps_params={'ensure_ascii': False, 'indent': 4})
    
    # Item 4.9: O cabeçalho 'Content-Disposition' FORÇA o navegador a fazer o download do arquivo
    response['Content-Disposition'] = f'attachment; filename="meus_dados_lgpd_{user.username}.json"'
    
    return response

@csrf_exempt
@login_required
def excluir_minha_conta(request):
    if request.method == 'POST':
        # Recebe o objeto do usuário logado antes de deslogar, para garantir que temos acesso a ele mesmo após o logout.
        user = request.user
        
        try:
            # Faz o logout antes de excluir a conta
            logout(request)
            
            # Delete do usuario
            user.delete()
            
            return JsonResponse({
                "mensagem": "Sua conta e todos os seus dados foram apagados conforme a LGPD. (Direito do esquecimento)"
            }, status=200)
            
        except Exception as e:
            return JsonResponse({"erro": f"Erro ao processar exclusão: {str(e)}"}, status=500)
            
    return JsonResponse({"erro": "Método não permitido. Utilize POST."}, status=405)