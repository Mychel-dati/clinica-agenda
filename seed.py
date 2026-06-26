"""Popula o banco com dados de exemplo para testar rapidamente.

Uso:  python seed.py
"""
from datetime import datetime, timedelta

from app import create_app
from extensions import db
from models import Paciente, Profissional, Agendamento

app = create_app()

with app.app_context():
    db.create_all()

    if Profissional.query.first():
        print("Banco ja tem dados. Nada a fazer.")
    else:
        # Profissionais
        dra_ana = Profissional(nome="Dra. Ana Souza", especialidade="Clinica Geral",
                               registro="CRM 12345", cor="#0d6efd")
        dr_bruno = Profissional(nome="Dr. Bruno Lima", especialidade="Cardiologia",
                                registro="CRM 67890", cor="#198754")
        dra_carla = Profissional(nome="Dra. Carla Reis", especialidade="Pediatria",
                                 registro="CRM 54321", cor="#d63384")
        db.session.add_all([dra_ana, dr_bruno, dra_carla])

        # Pacientes
        pacientes = [
            Paciente(nome="Joao da Silva", cpf="111.111.111-11", telefone="(11) 91111-1111",
                     data_nascimento=datetime(1985, 3, 12).date()),
            Paciente(nome="Maria Oliveira", cpf="222.222.222-22", telefone="(11) 92222-2222",
                     data_nascimento=datetime(1992, 7, 25).date()),
            Paciente(nome="Pedro Santos", cpf="333.333.333-33", telefone="(11) 93333-3333",
                     data_nascimento=datetime(2015, 1, 8).date()),
        ]
        db.session.add_all(pacientes)
        db.session.commit()

        # Agendamentos para hoje
        hoje = datetime.utcnow().date()
        base = datetime.combine(hoje, datetime.min.time())
        db.session.add_all([
            Agendamento(paciente_id=pacientes[0].id, profissional_id=dra_ana.id,
                        inicio=base.replace(hour=9, minute=0), duracao_min=30,
                        procedimento="Consulta de rotina", status="confirmado"),
            Agendamento(paciente_id=pacientes[1].id, profissional_id=dr_bruno.id,
                        inicio=base.replace(hour=10, minute=30), duracao_min=30,
                        procedimento="Avaliacao cardiologica", status="agendado"),
            Agendamento(paciente_id=pacientes[2].id, profissional_id=dra_carla.id,
                        inicio=base.replace(hour=14, minute=0), duracao_min=30,
                        procedimento="Puericultura", status="agendado"),
        ])
        db.session.commit()
        print("Dados de exemplo criados com sucesso!")
