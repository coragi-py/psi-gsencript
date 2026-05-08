# GSencript - Gerenciador de Credenciais & Políticas de Segurança

[![Universidade: UMC](https://img.shields.io/badge/University-UMC-0D47A1.svg)](https://www.umc.br/)
[![Matéria: PSI](https://img.shields.io/badge/Subject-Pol%C3%ADticas_de_Seguran%C3%A7a-7B1FA2.svg)](https://github.com/coragi-py/psi-gsencript)

[![Criptografia: AES256](https://img.shields.io/badge/Encryption-AES--256-orange.svg)](https://github.com/coragi-py/psi-gsencript)
[![Compliance: LGPD](https://img.shields.io/badge/Compliance-LGPD-blue.svg)](https://www.gov.br/esporte/pt-br/acesso-a-informacao/lgpd)
[![Hashing: Argon2](https://img.shields.io/badge/Hashing-Argon2-red.svg)](https://github.com/coragi-py/psi-gsencript)
[![Docker: Ready](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)

---

O **GSencript** é um projeto de Engenharia de Software desenvolvido para a disciplina de **Políticas de Segurança da Informação** na Universidade de Mogi das Cruzes (UMC). O sistema é um cofre de senhas (Vault) de "Conhecimento Zero" (Zero-Knowledge Architecture), conteinerizado e focado em criptografia de ponta e conformidade rigorosa com a **LGPD**.

## 🏗️ Arquitetura do Sistema
O projeto foi desenhado seguindo padrões modernos de engenharia:
* **Padrão de Projeto:** MVT (Model-View-Template).
* **Arquitetura de Software:** Monolito Modularizado (apps isolados para Accounts, Vault, Audit e LGPD).
* **Infraestrutura:** Microsserviços Conteinerizados (Separação entre App Django e Banco de Dados via Docker).
* **Segurança:** Arquitetura *Zero-Knowledge* (o servidor armazena apenas dados cifrados, sem acesso às senhas originais).

## 🚀 Novidades da Versão (Branch `docker-postgres`)
* **Conteinerização com Docker:** Implementação de Dockerfile e Docker Compose para deploy "Run Anywhere".
* **Persistência com PostgreSQL:** Migração do SQLite para SGBD relacional robusto, isolado em rede interna Docker.
* **UX/UI Refinada:** Correção de overflow de tokens, visualização de senha mestra e sistema de scrollbar.
* **Conformidade LGPD:** Página de Termos de Uso e Privacidade integrada com trava de registro e logs de consentimento.

## 🛡️ Tecnologias Utilizadas
* **Backend:** Django 6.0.4 / Python 3.12 (Ambiente Linux Docker).
* **Banco de Dados:** PostgreSQL 15.
* **Segurança:** AES-256 (Fernet), Argon2 (Hashing), PyOTP (MFA/TOTP).
* **Auditoria:** Sistema de logs interno e `django-axes` para prevenção de Brute Force.
* **Frontend:** Vanilla JS, Fetch API e CSS Moderno.

## ⚙️ Instalação e Execução (Docker - Recomendado)
O projeto está configurado para subir todo o ambiente (Python + Postgres) com um único comando:

1.  **Clone e Acesse a Branch:**
    ```powershell
    git clone -b docker-postgres [https://github.com/coragi-py/psi-gsencript.git](https://github.com/coragi-py/psi-gsencript.git)
    cd psi-gsencript
    ```
2.  **Configure o Ambiente:**
    * Renomeie o `.env.example` para `.env`.
    * Defina suas chaves (`SECRET_KEY`, `DB_PASSWORD`, etc).
3.  **Suba o Container:**
    ```powershell
    docker-compose up --build -d
    ```
4.  **Aplique as Migrações no Banco:**
    ```powershell
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser
    ```
Acesse em: `http://localhost:8000`

---

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

Abaixo estão os modelos de dados para as operações via API.

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

**Equipe de Desenvolvimento:**
&emsp;Anny Gabriely Souza do Nascimento | Antonio Luiz Lins Neto | Fábio Yuuki Saruwataru

**Orientação:** Prof. Dr. Fabiano Bezerra Menegidio
**Instituição:** UMC - Universidade de Mogi das Cruzes (2026)
