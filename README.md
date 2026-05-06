# GSencript - Gerenciador de Credenciais & Políticas de Segurança

[![Universidade: UMC](https://img.shields.io/badge/University-UMC-0D47A1.svg)](https://www.umc.br/)
[![Matéria: PSI](https://img.shields.io/badge/Subject-Pol%C3%ADticas_de_Seguran%C3%A7a-7B1FA2.svg)](https://github.com/coragi-py/psi-gsencript)

[![Criptografia: AES256](https://img.shields.io/badge/Encryption-AES--256-orange.svg)](https://github.com/coragi-py/psi-gsencript)
[![Compliance: LGPD](https://img.shields.io/badge/Compliance-LGPD-blue.svg)](https://www.gov.br/esporte/pt-br/acesso-a-informacao/lgpd)
[![Hashing: Argon2](https://img.shields.io/badge/Hashing-Argon2-red.svg)](https://github.com/coragi-py/psi-gsencript)
[![Autenticação: MFA-TOTP](https://img.shields.io/badge/MFA-TOTP-yellow.svg)](https://github.com/coragi-py/psi-gsencript)

[![Python 3.14](https://img.shields.io/badge/python-3.14%2B-blue.svg)](https://www.python.org/)
[![Django 6.0.4](https://img.shields.io/badge/django-6.0.4%2B-092e20.svg)](https://www.djangoproject.com/)

---

O **GSencript** é um projeto de Engenharia de Software desenvolvido para a disciplina de **Políticas de Segurança da Informação** na **UMC**. O sistema é um cofre de senhas (Vault) focado em criptografia de ponta e conformidade rigorosa com a **LGPD**.

## 🚀 Novidades da Versão Atual (Integração Frontend):
* **Fluxo de Cadastro Seguro:** Validação de senha forte em tempo real, confirmação dupla e visualização (toggle eye).
* **MFA com QR Code:** Geração automática de código TOTP compatível com Google Authenticator e Authy, incluindo botão de cópia segura.
* **Gate de Conformidade LGPD:** O botão de registro permanece bloqueado até que o usuário abra e aceite os Termos de Privacidade.
* **Login em Duas Etapas:** Separação visual entre validação de credenciais e inserção do token 2FA.
* **Recuperação de Senha (Recovery):** Sistema de tokens temporários (10 min) com interface dedicada para reset de senha mestra.

## 🛡️ Tecnologias e Segurança
* **Backend:** Django 6.0 / Python 3.14.
* **Criptografia em Repouso:** AES-256 (Fernet) com chaves derivadas da `SECRET_KEY`.
* **Hashing de Senha:** Argon2 (padrão Django) para proteção contra ataques de dicionário e brute-force.
* **Frontend:** Vanilla JavaScript com Fetch API, CSS Moderno (Cyber-Vault Theme) e `qrcodejs` para MFA.

📂 Estrutura do Projeto
```text
.
├── core/                # Configurações globais e Timezone
├── accounts/            # Gestão de Usuários e Separação de Identidade
├── authentication/      # Fluxo de Sessão (Login/Logout) e MFA
├── recovery/            # Gestão de Tokens de Recuperação e Redefinição
├── vault/               # Cofre Criptografado AES-256 e CRUD de Credenciais
├── lgpd/                # Gestão de Consentimento e Termos de Uso
├── templates/           # Interfaces HTML (Base, Vault, Login, Privacy)
└── static/              # Estilos e Scripts (MFA, Validações)
```

## ⚙️ Instalação (Windows 10/11)
1.  **Clone e Entre na Pasta:**
    ```powershell
    git clone -b add-frontend https://github.com/coragi-py/psi-gsencript.git
    cd psi-gsencript
    ```
2.  **Ambiente Virtual:**
    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt
    ```
3.  **Configuração e Migração:**
    ```powershell
    # Configure o .env com sua SECRET_KEY e ENCRYPTION_KEY
    python manage.py migrate
    python manage.py runserver
    ```

## 📡 Endpoints Principais (API & Interface)

### Autenticação & Recuperação
| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET/POST` | `/accounts/registrar/` | Cadastro com geração de QR Code para 2FA. |
| `GET/POST` | `/auth/login/` | Autenticação em dois passos (Senha + Token). |
| `GET/POST` | `/recovery/request/` | Solicitação de token de recuperação de conta. |
| `GET/POST` | `/recovery/reset/` | Redefinição de senha mestra via token válido. |

### Gestão do Cofre
| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/vault/` | Dashboard principal (DashboardView). |
| `POST` | `/vault/adicionar/` | Criptografia e armazenamento de nova credencial. |
| `POST` | `/vault/excluir/<id>/` | Remoção protegida contra IDOR. |

---

## 📡 Documentação de Payloads (JSON)

### Registrar Usuário
**POST** `/accounts/registrar/`
```json
{
  "full_name": "Testa da Silva",
  "username": "teste@exemplo.com",
  "email": "fabio@exemplo.com",
  "senha": "SenhaForte@123",
  "consentimento_lgpd": true
}
```

### Resetar Senha
**POST** `/recovery/reset/`
```json
{
  "token": "TOKEN_GERADO_PELO_SISTEMA",
  "nova_senha": "NovaSenhaForte@2026"
}
```

---

**Equipe de Desenvolvimento:**
&emsp;Anny Gabriely Souza do Nascimento | Antonio Luiz Lins Neto | Fábio Yuuki Saruwataru

**Orientação:** Prof. Dr. Fabiano Bezerra Menegidio
**Instituição:** UMC - Universidade de Mogi das Cruzes
```
