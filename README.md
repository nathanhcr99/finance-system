# Autenticação de Usuário
    1. Login de Usuário
        URL: /api/auth/login/
        Método HTTP: POST
        Parâmetros de Requisição:
        username (string): Nome de usuário do usuário
        password (string): Senha do usuário
        Formato de Requisição: JSON

    2. Logout de Usuário
        URL: /api/auth/logout/
        Método HTTP: POST
        Parâmetros de Requisição: Nenhum
        Formato de Requisição: N/A
        Formato de Resposta: N/A
        Códigos de Resposta:
        204 No Content: Logout bem-sucedido
        401 Unauthorized: Token de acesso inválido ou expirado

# Gerenciamento de Usuários
    3. Listar Usuários
        URL: /api/users/
        Método HTTP: GET
        Parâmetros de Requisição: Nenhum
        Formato de Requisição: N/A
        Formato de Resposta: JSON


    4. Detalhes do Usuário
        URL: /api/users/{id}/
        Método HTTP: GET
        Parâmetros de Requisição:
        id (integer): ID do usuário
        Formato de Requisição: N/A
        Formato de Resposta: JSON

    5. Criar Usuário
        URL: /api/users/
        Método HTTP: POST
        Parâmetros de Requisição:
        username (string): Nome de usuário do novo usuário
        password (string): Senha do novo usuário
        email (string): Endereço de e-mail do novo usuário


#   Operações Financeiras
    6. Obter Saldo do Usuário
    URL: /api/account/
    Método HTTP: GET
    Parâmetros de Requisição: Nenhum
    Formato de Requisição: N/A
    Formato de Resposta: JSON