"""Configuracoes da aplicacao.

O caminho do banco e absoluto para funcionar tanto localmente (Windows)
quanto no PythonAnywhere (Linux), sem depender do diretorio de trabalho.
"""
import os
from urllib.parse import quote_plus

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# --- Conexao padrao com o MySQL local (servico MySQL80) ---------------------
# As credenciais podem ser trocadas por variaveis de ambiente sem editar o codigo.
DB_USER = os.environ.get("DB_USER", "clinica")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "Clinica#2026")
DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_PORT = os.environ.get("DB_PORT", "3306")
DB_NAME = os.environ.get("DB_NAME", "clinica")

# quote_plus escapa caracteres especiais da senha (ex.: '#').
MYSQL_URI = (
    f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
)


class Config:
    # Em producao, defina SECRET_KEY como variavel de ambiente.
    SECRET_KEY = os.environ.get("SECRET_KEY", "troque-esta-chave-em-producao")

    # Usa MySQL por padrao; DATABASE_URL sobrescreve (ex.: SQLite no PythonAnywhere).
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", MYSQL_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Evita erros de "MySQL server has gone away" reciclando conexoes ociosas.
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_recycle": 280, "pool_pre_ping": True}

    # Horario de funcionamento da clinica (usado para montar a grade da agenda).
    HORARIO_ABERTURA = 8   # 08:00
    HORARIO_FECHAMENTO = 19  # 19:00
    INTERVALO_MINUTOS = 30   # tamanho de cada slot
