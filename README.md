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
* **Infraestrutura:** Ambiente Conteinerizados (Separação entre App Django e Banco de Dados via Docker).
* **Segurança:** Arquitetura *Zero-Knowledge* (o servidor armazena apenas dados cifrados, sem acesso às senhas originais).

## 🚀 Novidades da Versão (Versão 1.1)
* **Conteinerização com Docker:** Implementação de Dockerfile e Docker Compose para deploy "Run Anywhere".
* **Persistência com PostgreSQL:** Migração do SQLite para SGBD relacional robusto, isolado em rede interna Docker.
* **UX/UI Refinada:** Correção de overflow de tokens, visualização de senha mestra e sistema de scrollbar.
* **Conformidade LGPD:** Página de Termos de Uso e Privacidade integrada com trava de registro e logs de consentimento.
* **Validação de Login em Duas Etapas:** Separação da validação de credenciais (Password check) do desafio de segundo fator (MFA/TOTP).
* **Central de Gestão de Privacidade:** Interface visual (Cards) para exercício pleno dos direitos do titular (LGPD Art. 18).
* **Portão de Reativação de Consentimento:** Sistema de bloqueio automático de processamento de dados em caso de revogação de consentimento.

## 🛡️ Tecnologias Utilizadas
* **Backend:** Django 6.0.4 / Python 3.12 (Ambiente Linux Docker).
* **Banco de Dados:** PostgreSQL 15.
* **Segurança:** AES-256 (Fernet), Argon2 (Hashing), PyOTP (MFA/TOTP).
* **Auditoria:** Sistema de logs interno e `django-axes` para prevenção de Brute Force.
* **Frontend:** Vanilla JS, Fetch API e CSS Moderno.
* O GSencript utiliza Argon2id (vencedor do Password Hashing Competition) para o armazenamento de hashes, configurado para resistir a ataques de canal lateral e força bruta via GPU/ASIC.

## ⚙️ Instalação e Execução (Docker - Recomendado)

O **GSencript** utiliza Docker para garantir que o ambiente de execução seja idêntico em qualquer máquina, isolando o servidor Django e o banco de dados PostgreSQL.

### 1. Pré-requisitos

* [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado.
* Git instalado.

### 2. Clonagem e Configuração

```powershell
# Clone o repositório (v1.1 Main)
git clone https://github.com/coragi-py/psi-gsencript.git
cd psi-gsencript

# Configure as variáveis de ambiente
# Copie o arquivo de exemplo para o arquivo real
cp .env.example .env

```

> **Nota:** Abra o arquivo `.env` e defina suas chaves secretas e senhas do banco de dados antes de prosseguir.

### 3. Build e Inicialização

Execute o comando abaixo para construir as imagens e subir os containers em segundo plano:

```powershell
docker-compose up --build -d

```

### 4. Preparação do Ambiente e Banco

Agora, execute as migrações para estruturar o PostgreSQL e crie o usuário administrador do sistema:

```powershell
# Aplica a estrutura do banco (MFA, Vault, LGPD, etc)
docker-compose exec web python manage.py migrate

# Cria o superusuário administrador
docker-compose exec web python manage.py createsuperuser

```

### 5. Manutenção e Comandos Úteis

* **Acessar o sistema:** `http://localhost:8000`
* **Limpar bloqueios de IP (Axes):** Caso você erre a senha muitas vezes no teste:
`docker-compose exec web python manage.py axes_reset`
* **Ver Logs em tempo real:**
`docker-compose logs -f web`
* **Derrubar os serviços:**
`docker-compose down`

---

## Mapeamento da API (Rotas para Teste)

### Gestão de Identidade (`/accounts/` & `/auth/`)
| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `POST` | `/accounts/registrar/` | Cadastro de usuário com aceite de LGPD e retorno de Segredo 2FA. |
| `POST` | `/auth/login/` | Autenticação com verificação de credenciais e token TOTP. |
| `POST` | `/auth/logout/` | Encerramento seguro da sessão. |
| `POST` | `/auth/validar-credenciais/` | **Pre-auth Check:** Valida usuário/senha antes de solicitar o 2FA.|

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

### Gestão de Privacidade (`/privacidade/`)
| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/privacidade/` | **Dashboard de Privacidade:** Interface de gestão de dados. |
| `GET` | `/privacidade/consultar/` | Retorno de dados em JSON para transparência total. |
| `POST` | `/privacidade/reativar/` | Reativação de consentimento após revogação. |

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

**Orientação:** Prof. Dr. Fabiano Bezerra Menegidio\
**Instituição:** UMC - Universidade de Mogi das Cruzes (2026)
