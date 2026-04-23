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
**Alunos:** 
  Anny Gabriely Souza do Nascimento
  Antonio Luiz Lins Neto
  Fábio Yuuki Saruwataru  
**Disciplina:** Políticas de Segurança da Informação  
**Instituição:** UMC - Universidade de Mogi das Cruzes
