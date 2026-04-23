# GSencript - Gerenciador de Credenciais & Políticas de Segurança

O **GSencript** é um projeto acadêmico desenvolvido para a disciplina de **Políticas de Segurança da Informação (Projeto Integrador)** na **Universidade de Mogi das Cruzes (UMC)**. O objetivo central é a aplicação prática de diretrizes de segurança, controle de acesso e conformidade legal em um ambiente de software.

## Resumo
Este sistema funciona como um cofre de senhas (Vault) que prioriza os pilares da Segurança da Informação: **Confidencialidade, Integridade e Disponibilidade**. Mais do que um simples armazenamento, o projeto implementa controles técnicos rigorosos para mitigar riscos de vazamento de dados e garantir a privacidade do usuário final, alinhando o desenvolvimento de software às exigências da **LGPD (Lei Geral de Proteção de Dados)**.

## Tecnologias Utilizadas
* **Backend:** Python 3.14 / Django 6.0.4
* **Segurança e Criptografia:**
    * **Argon2:** Algoritmo de hashing de última geração para senhas de sistema.
    * **AES-256 (Fernet):** Criptografia simétrica de nível militar para proteção das credenciais em repouso.
    * **MFA (TOTP):** Autenticação de dois fatores implementada com `PyOTP`.
* **Frontend:** Interface responsiva construída com Tailwind CSS e integração via Fetch API.
* **Banco de Dados:** SQLite (persistência de dados criptografados).

## Instalação e Configuração
Para rodar o projeto em seu ambiente local (Windows 10):

## 🔑 Variáveis de Ambiente (.env.example)

Para a correta execução das políticas de segurança e criptografia, o arquivo `.env` deve ser configurado na raiz do projeto seguindo o modelo abaixo:

```text
# Django Settings
SECRET_KEY=sua_chave_secreta_django
DEBUG=True

# Criptografia AES-256 (Gere uma chave válida usando: cryptography.fernet.Fernet.generate_key())
ENCRYPTION_KEY=sua_chave_fernet_32_bytes_base64

# Database
DATABASE_URL=sqlite:///db.sqlite3
```

1.  **Clone o projeto:**
    ```bash
    git clone https://github.com/coragi-py/psi-gsencript.git
    cd psi-gsencript
    ```

2.  **Prepare o ambiente (Virtualenv):**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instale os requisitos:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Sincronize o Banco de Dados:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Inicie a aplicação:**
    ```bash
    python manage.py runserver
    ```

## Políticas Implementadas
Este projeto materializa as seguintes políticas de segurança:
* **Controle de Acesso Lógico:** Implementação de MFA para prevenir acessos não autorizados mesmo em caso de comprometimento da senha principal.
* **Criptografia em Repouso:** Garantia de que dados sensíveis nunca sejam armazenados em texto claro (Plain Text).
* **Privacy by Design (LGPD):** Ferramentas nativas para o exercício dos direitos do titular, como portabilidade (exportação) e direito ao esquecimento (exclusão).
* **Gestão de Consentimento:** Controle rigoroso de processamento de dados baseado no aceite explícito do usuário.

## Mapeamento da API (Rotas para Teste)

### Gestão de Identidade (`/accounts/` & `/auth/`)
| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `POST` | `/accounts/registrar/` | Cadastro de usuário com aceite de LGPD e retorno de Segredo 2FA. |
| `POST` | `/auth/login/` | Autenticação com verificação de credenciais e token TOTP. |
| `POST` | `/auth/logout/` | Encerramento seguro da sessão. |

### Cofre de Credenciais (`/vault/`)
| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `POST` | `/vault/adicionar/` | Criptografa (AES-256) e armazena uma nova senha. |
| `GET` | `/vault/listar/` | Recupera as senhas (decifradas) para o usuário autenticado. |
| `POST` | `/vault/excluir/<id>/` | Remoção definitiva de uma credencial específica. |

### Direitos do Titular - LGPD (`/lgpd/`)
| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/lgpd/exportar/` | **Portabilidade:** Gera JSON com todos os dados pessoais e do cofre. |
| `POST` | `/lgpd/revogar/` | Revogação de consentimento e bloqueio imediato do acesso. |
| `POST` | `/lgpd/excluir/` | **Direito ao Esquecimento:** Exclusão total e irreversível da conta. |

---

## 📡 Documentação de Payloads (JSON)

Abaixo estão os modelos de dados para as operações de criação (Create) e alteração (Alter) via API.

### 1. Operações de Criação (Create)

**Registrar Novo Usuário**
* **Endpoint:** `POST /accounts/registrar/`
```json
{
  "username": "usuario_exemplo",
  "email": "exemplo@dominio.com",
  "senha": "SenhaForte@123",
  "consentimento_lgpd": true
}
```

**Adicionar Credencial ao Cofre**
* **Endpoint:** `POST /vault/adicionar/`
```json
{
  "titulo": "Nome do Site/Serviço",
  "url": "https://www.exemplo.com",
  "username": "meu_usuario",
  "senha": "senha_que_sera_criptografada"
}
```

### 2. Operações de Alteração (Alter)

**Redefinição de Senha (Recovery)**
* **Endpoint:** `POST /recovery/resetar/`
```json
{
  "token": "codigo_recebido_por_email",
  "nova_senha": "Nova@SenhaForte2026"
}
```

**Atualizar Credencial Existente**
* **Endpoint:** `POST /vault/atualizar/<id>/`
```json
{
  "titulo": "Nome Atualizado",
  "url": "https://nova-url.com",
  "username": "novo_usuario",
  "senha": "nova_senha_criptografada"
}
```

### 3. Autenticação e Acesso

**Login com MFA**
* **Endpoint:** `POST /auth/login/`
```json
{
  "username": "usuario_exemplo",
  "password": "SenhaForte@123",
  "token_2fa": "123456"
}
```

---

**Alunos:** \
  Anny Gabriely Souza do Nascimento\
  Antonio Luiz Lins Neto\
  Fábio Yuuki Saruwataru \
**Disciplina:** Políticas de Segurança da Informação  
**Instituição:** UMC - Universidade de Mogi das Cruzes
