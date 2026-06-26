"""Ponto de entrada da aplicacao (app factory).

Local:  python app.py   ->  http://127.0.0.1:5000
PythonAnywhere: o arquivo WSGI importa `create_app` deste modulo.
"""
from flask import Flask

from config import Config
from extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    # Registra os blueprints (cada modulo do sistema).
    from blueprints.main import bp as main_bp
    from blueprints.pacientes import bp as pacientes_bp
    from blueprints.profissionais import bp as profissionais_bp
    from blueprints.agendamentos import bp as agendamentos_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(pacientes_bp)
    app.register_blueprint(profissionais_bp)
    app.register_blueprint(agendamentos_bp)

    # Cria as tabelas na primeira execucao.
    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
