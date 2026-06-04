# GSencript - Zero-Knowledge Credential Vault

[![Universidade: UMC](https://img.shields.io/badge/University-UMC-0D47A1.svg)](https://www.umc.br/)
[![Matéria: PSI](https://img.shields.io/badge/Subject-Pol%C3%ADticas_de_Seguran%C3%A7a-7B1FA2.svg)](https://github.com/coragi-py/psi-gsencript)

[![Criptografia: AES256](https://img.shields.io/badge/Encryption-AES--256-orange.svg)](https://github.com/coragi-py/psi-gsencript)
[![Compliance: LGPD](https://img.shields.io/badge/Compliance-LGPD-blue.svg)](https://www.gov.br/esporte/pt-br/acesso-a-informacao/lgpd)
[![Hashing: Argon2](https://img.shields.io/badge/Hashing-Argon2-red.svg)](https://github.com/coragi-py/psi-gsencript)
[![Docker: Ready](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)

---

## 📑 Índice (Table of Contents)

- [1. Visão Geral (Overview)](#1-visão-geral-overview)
- [2. Principais Funcionalidades (Key Features)](#2-principais-funcionalidades-key-features)
- [3. Arquitetura do Sistema (System Architecture)](#3-arquitetura-do-sistema-system-architecture)
- [4. Pré-requisitos (Prerequisites)](#4-pré-requisitos-prerequisites)
- [5. Instalação e Execução (Installation & Quick Start)](#5-instalação-e-execução-installation--quick-start)
- [6. Guia de Endpoints e Payloads (API Reference)](#6-guia-de-endpoints-e-payloads-api-reference--usage)
- [7. Contribuição e Licença (Contributing & License)](#7-contribuição-e-licença-contributing--license)
- [8. Autores e Citação (Authors & Citation)](#8-autores-e-citação-authors--citation)

***

## 1. Visão Geral (Overview)

O **GSencript** é um sistema gerenciador de credenciais (Vault) construído sob os princípios da **Arquitetura de Conhecimento Zero (Zero-Knowledge Architecture)**. O sistema assegura que o servidor e o provedor de serviço armazenem apenas metadados cifrados, inviabilizando o acesso em texto claro às credenciais originais dos usuários. Desenvolvido com rigor acadêmico e técnico para a disciplina de **Políticas de Segurança da Informação** da Universidade de Mogi das Cruzes (UMC), o projeto consolida práticas de engenharia reversa de segurança, criptografia avançada e conformidade absoluta com os padrões de privacidade da legislação brasileira.

***

## 2. Principais Funcionalidades (Key Features)

- 🔒 **Criptografia AES-256 (Fernet):** Proteção de dados em repouso. Todas as senhas do cofre são cifradas localmente antes da persistência no banco de dados.
- 🔑 **Hashing Avançado com Argon2id:** Resistência máxima contra ataques de dicionário e aceleração de hardware (ASICs/GPUs) no armazenamento das senhas mestras.
- ⚖️ **Conformidade Nativa com a LGPD (Art. 18):** Módulos integrados para portabilidade de dados (exportação JSON estruturada), revogação de consentimento e exclusão irreversível (direito ao esquecimento).
- 🛡️ **Autenticação em 2 Fatores (MFA/TOTP):** Validação robusta de identidade configurável via aplicativos autenticadores padrão ou envio de token temporário via e-mail (integração SMTP com Brevo).
- 📜 **Logs de Auditoria (WORM):** Trilha de auditoria inalterável (Write Once, Read Many) que mapeia eventos de ciclo de vida (logins, falhas de autenticação, exclusão de dados) em conformidade com políticas ISO 27001.

***

## 3. Arquitetura do Sistema (System Architecture)

O projeto adota o padrão **Monolito Modularizado**, implementado sobre o framework **Django**. A aplicação é dividida em microsserviços lógicos isolados por responsabilidade:

- `accounts` — Gestão de identidade e ciclo de vida do usuário.
- `authentication` — Camadas de MFA e controle de sessão segura.
- `vault` — Cofre criptográfico, lógica de cifragem/decifragem.
- `lgpd` — Painel de conformidade e gestão de consentimento.
- `audit` — Repositório WORM e monitoramento de eventos de segurança.
- `recovery` — Fluxos assíncronos e seguros de recuperação de acesso.

A segurança no tráfego de entrada é fortificada pelo pacote **django-axes**, implementando barreiras de mitigação (Middlewares) contra ataques de **Força Bruta** e **Denial of Service (DoS)**, impondo limite de taxas (Rate Limiting) e bloqueio temporário de IP após falhas sucessivas.

***

## 4. Pré-requisitos (Prerequisites)

Para provisionar e executar a infraestrutura localmente, os seguintes componentes são necessários no host:

- [Docker Engine](https://docs.docker.com/engine/install/) (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2.0+)
- [Git](https://git-scm.com/downloads)

***

## 5. Instalação e Execução (Installation & Quick Start)

O sistema utiliza orquestração conteinerizada para garantir a reprodutibilidade exata do ambiente de produção, isolando a aplicação Python do SGBD PostgreSQL em uma rede virtual interna (bridge).

### 5.1. Clonagem e Configuração do Ambiente

```bash
# 1. Clone o repositório oficial
git clone https://github.com/coragi-py/psi-gsencript.git
cd psi-gsencript

# 2. Configure as variáveis de ambiente
cp .env.example .env
```

> ⚠️ **AVISO CRÍTICO (SMTP BREVO):** Edite o arquivo `.env` inserindo suas chaves de produção. Preste especial atenção às credenciais de e-mail (`EMAIL_HOST_USER` e `EMAIL_HOST_PASSWORD`). Utilize a chave SMTP designada pela Brevo, e **não** a senha de login do painel.

### 5.2. Build e Orquestração

```bash
# 3. Construa as imagens e levante os contêineres em background
docker-compose up --build -d

# 4. Verifique o status dos serviços (web e db)
docker-compose ps
```

### 5.3. Preparação do Banco de Dados

```bash
# 5. Aplique as migrações estruturais do PostgreSQL
docker-compose exec web python manage.py migrate

# 6. (Opcional) Crie uma conta de superusuário para gestão administrativa
docker-compose exec web python manage.py createsuperuser
```

Acesse a interface da aplicação através do endpoint exposto: [http://localhost:8000](http://localhost:8000).

***

## 6. Guia de Endpoints e Payloads (API Reference / Usage)

Abaixo estão detalhados os principais fluxos de dados e seus respectivos payloads em JSON. As interações com a API pressupõem o envio de requisições sobre **HTTPS** em ambiente de produção.

### 6.1. Gestão de Identidade e Autenticação

**Criar Usuário (Registro com Consentimento LGPD)**

`POST /accounts/registrar/`

> **Nota:** Os campos de identificação sofrem higienização estrita (case-insensitive) antes da validação.

```json
{
  "full_name": "Alan Turing",
  "email": "alan@enigma.com",
  "username": "alan@enigma.com",
  "senha": "PasswordComplex@2026",
  "consentimento_lgpd": true
}
```

**Autenticação MFA (App ou Email)**

`POST /auth/login/`

```json
{
  "username": "alan@enigma.com",
  "password": "PasswordComplex@2026",
  "token_2fa": "123456",
  "tipo_2fa": "app"
}
```

### 6.2. Cofre de Credenciais (Vault)

**Adicionar Nova Credencial Cifrada**

`POST /vault/adicionar/`

> **Nota:** O servidor recebe o payload em texto plano, porém, a persistência na coluna `senha_site_cifrada` ocorre estritamente no formato ciphertext utilizando a chave mestra AES-256.

```json
{
  "titulo": "Acesso Bancário",
  "url": "https://banco.exemplo.com",
  "username": "alan.turing",
  "senha": "MySuperSecretBankPassword123"
}
```

### 6.3. Privacidade e Conformidade (LGPD)

- **Portabilidade de Dados** `GET /lgpd/exportar/` — Retorna um binário de download em formato JSON (Header `Content-Disposition: attachment`) contendo todos os dados do titular e o cofre de senhas cifrado.
- **Revogação** `POST /lgpd/revogar/` — Suspende a capacidade de processamento do software para a referida conta (Art. 8, § 5º da LGPD).
- **Esquecimento** `POST /lgpd/excluir/` — Encerra a sessão atual e executa exclusão permanente (CASCADE) no banco de dados.

***

## 7. Contribuição e Licença (Contributing & License)

Contribuições para o aprimoramento criptográfico, otimizações arquiteturais ou melhorias de documentação são bem-vindas através de Pull Requests (PRs).

1. Realize o **Fork** do projeto.
2. Crie uma **Branch** para sua Feature (`git checkout -b feature/AmazingFeature`).
3. Submeta um **Commit** com suas mudanças (`git commit -m 'Add: AmazingFeature'`).
4. Realize o **Push** para a respectiva Branch (`git push origin feature/AmazingFeature`).
5. Abra um **Pull Request** detalhando as alterações e justificativas técnicas.

Este projeto é disponibilizado primariamente para fins de **pesquisa acadêmica e uso não comercial**.

***

## 8. Autores e Citação (Authors & Citation)

**Equipe de Engenharia:**
- Anny Gabriely Souza do Nascimento
- Antonio Luiz Lins Neto
- Fábio Yuuki Saruwataru

**Supervisão Técnica:**
- Prof. Dr. Fabiano Bezerra Menegidio

**Instituição:**
- UMC - Universidade de Mogi das Cruzes (2026)
