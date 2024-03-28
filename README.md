# Diagrama do fluxo
![image](https://github.com/Mesheo/activation_keygen/assets/71408872/0bf39e92-b748-45bf-b41d-92c2286e7da5)


# Resumo das funções
/client_application /app.py 

  * `collectSystemInfo()` - Coleta dados locais do PC e bota numa string hasheada
  * `verify_activation_key(activation_key)` - Verifica se a chave de licença descriptografada retorna os dados corretos do PC local

/license_server /main.py
  * `generate_activation_key(system_info, encode_algorithm)` - gera a chave de ativação com base nas informações do sistema e em um algoritmo de codificação (que vai ser compartilhado com o programa)

