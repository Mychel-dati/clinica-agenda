"""Arquivo WSGI para o PythonAnywhere.

NAO rode este arquivo localmente. O conteudo abaixo deve ser COPIADO para o
arquivo WSGI que o PythonAnywhere gera automaticamente, em:

    Web > (sua app) > WSGI configuration file
    (ex.: /var/www/SEUUSUARIO_pythonanywhere_com_wsgi.py)

Troque 'SEUUSUARIO' pelo seu nome de usuario do PythonAnywhere.
"""
import sys

# 1) Caminho do projeto (onde estao app.py, models.py, etc.)
project_home = "/home/SEUUSUARIO/Clinica"
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# 2) Importa a aplicacao Flask ja criada em app.py
from app import app as application  # noqa: E402  (o PythonAnywhere usa 'application')
