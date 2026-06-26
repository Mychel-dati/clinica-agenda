"""Extensoes compartilhadas (evita import circular)."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
