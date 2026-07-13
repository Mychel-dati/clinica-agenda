"""Arquivo WSGI para o PythonAnywhere.

NAO rode este arquivo localmente. O conteudo abaixo deve ser COPIADO para o
arquivo WSGI que o PythonAnywhere gera automaticamente, em:

    Web > (sua app) > WSGI configuration file
    (ex.: /var/www/SEUUSUARIO_pythonanywhere_com_wsgi.py)

Troque 'SEUUSUARIO' pelo seu nome de usuario do PythonAnywhere e a SENHA_DO_MYSQL
pela senha que voce definiu na aba "Databases".
"""
import os
import sys

# 1) Caminho do projeto (onde estao app.py, models.py, etc.)
project_home = "/home/SEUUSUARIO/Clinica"
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# 2) Credenciais do MySQL do PythonAnywhere (aba "Databases").
#    O config.py monta a URI de conexao a partir destas variaveis.
os.environ["DB_HOST"] = "SEUUSUARIO.mysql.pythonanywhere-services.com"
os.environ["DB_USER"] = "SEUUSUARIO"
os.environ["DB_PASSWORD"] = "SENHA_DO_MYSQL"
os.environ["DB_NAME"] = "SEUUSUARIO$clinica"   # o prefixo 'SEUUSUARIO$' e obrigatorio
os.environ["DB_PORT"] = "3306"

# 3) (Recomendado) Chave secreta de producao.
os.environ["SECRET_KEY"] = "troque-por-uma-chave-bem-grande-e-secreta"

# 4) Importa a aplicacao Flask ja criada em app.py
#    (o create_app cria as tabelas automaticamente na primeira carga).
from app import app as application  # noqa: E402  (o PythonAnywhere usa 'application')
