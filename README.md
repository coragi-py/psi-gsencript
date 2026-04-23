# GSencript - Gerenciador de Senhas Seguro

Este projeto é um **Gerenciador de Senhas (Vault)** desenvolvido em Django, focado em segurança ofensiva, criptografia robusta e conformidade com a **Lei Geral de Proteção de Dados (LGPD)**. Desenvolvido como parte do projeto de Engenharia de Software.

## Diferenciais de Segurança

O sistema foi construído seguindo recomendações da **RFC 9106** e **OWASP**, implementando:

* **Autenticação Primária:** Utilização do algoritmo **Argon2** para o hashing de senhas (superior ao PBKDF2).
* **MFA (Multi-Fator):** Autenticação em duas etapas via **TOTP** (Time-based One-Time Password) com a biblioteca `pyotp`.
* **Criptografia em Repouso:** Senhas de terceiros são armazenadas no banco de dados utilizando criptografia simétrica **AES (Fernet)**.
* **Proteção de Força Bruta:** Integração com `django-axes` para bloqueio de tentativas sucessivas de login.
* **Trilha de Auditoria:** Registro de eventos críticos (logins, alterações de senha, acessos ao cofre).

## Conformidade LGPD

O sistema implementa nativamente os direitos do titular:
* **Gestão de Consentimento:** Registro explícito e possibilidade de revogação de acesso.
* **Portabilidade:** Exportação de dados do usuário em formato JSON.
* **Direito ao Esquecimento:** Exclusão permanente de conta e dados vinculados.

## Tecnologias Utilizadas

* **Backend:** Python 3.14+ / Django 5.x
* **Banco de Dados:** SQLite (Desenvolvimento) / PostgreSQL (Suportado)
* **Criptografia:** Cryptography (Fernet/AES)
* **Ambiente:** Windows 10/11 64bits

---

## 🛠️ Como Instalar e Rodar

### 1. Clonar o repositório e entrar na pasta
```bash
git clone https://github.com/SEU_USUARIO/gsencript_django.git
cd gsencript_django
```

### 2. Configurar o Ambiente Virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente
Crie um arquivo `.env` baseado no `.env.example`:
```bash
cp .env.example .env
# Edite o .env com sua SECRET_KEY e configurações locais
```

### 5. Migrações e Superusuário
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Executar o Servidor
```bash
python manage.py runserver
```

---

## 📂 Estrutura de Apps

* `/accounts`: Gerenciamento de usuários e modelos customizados.
* `/authentication`: Lógica de login, logout e verificação 2FA.
* `/vault`: Armazenamento, cifragem e decifragem de credenciais.
* `/lgpd`: Controle de consentimento e portabilidade de dados.
* `/recovery`: Fluxo de recuperação de conta via tokens seguros.
* `/audit`: Sistema de logs e monitoramento de sinais.

## 📝 Licença

Este projeto foi desenvolvido para fins acadêmicos.
