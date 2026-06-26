"""Configuracoes da aplicacao.

O caminho do banco e absoluto para funcionar tanto localmente (Windows)
quanto no PythonAnywhere (Linux), sem depender do diretorio de trabalho.
"""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Em producao, defina SECRET_KEY como variavel de ambiente.
    SECRET_KEY = os.environ.get("SECRET_KEY", "troque-esta-chave-em-producao")

    # SQLite: arquivo unico, ideal para o plano gratuito do PythonAnywhere.
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "clinica.db"),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Horario de funcionamento da clinica (usado para montar a grade da agenda).
    HORARIO_ABERTURA = 8   # 08:00
    HORARIO_FECHAMENTO = 19  # 19:00
    INTERVALO_MINUTOS = 30   # tamanho de cada slot
