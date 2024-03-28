# Diagrama do fluxo
![image]()

# Resumo das funções
/client_application /app.py 

  * `collectSystemInfo()` - Coleta dados locais do PC e bota numa string hasheada
  * `verify_activation_key(activation_key)` - Verifica se a chave de licença descriptografada retorna os dados corretos do PC local

/license_server /main.py
  * `generate_activation_key(system_info, encode_algorithm)` - gera a chave de ativação com base nas informações do sistema e em um algoritmo de codificação (que vai ser compartilhado com o programa)

