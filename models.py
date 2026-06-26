"""Modelos do banco de dados.

Entidades principais de uma agenda de clinica:
- Paciente      : quem e atendido
- Profissional  : quem atende (medico, dentista, psicologo...)
- Agendamento   : a consulta em si, ligando paciente x profissional x horario
"""
from datetime import datetime, timedelta

from extensions import db


# Status possiveis de um agendamento (fluxo usado nos sistemas de mercado).
STATUS_AGENDADO = "agendado"
STATUS_CONFIRMADO = "confirmado"
STATUS_ATENDIDO = "atendido"
STATUS_CANCELADO = "cancelado"
STATUS_FALTOU = "faltou"

STATUS_CHOICES = [
    STATUS_AGENDADO,
    STATUS_CONFIRMADO,
    STATUS_ATENDIDO,
    STATUS_CANCELADO,
    STATUS_FALTOU,
]

# Cor (badge Bootstrap) usada para cada status na interface.
STATUS_CORES = {
    STATUS_AGENDADO: "secondary",
    STATUS_CONFIRMADO: "info",
    STATUS_ATENDIDO: "success",
    STATUS_CANCELADO: "danger",
    STATUS_FALTOU: "warning",
}


class Paciente(db.Model):
    __tablename__ = "pacientes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(14))
    data_nascimento = db.Column(db.Date)
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    observacoes = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    agendamentos = db.relationship(
        "Agendamento", back_populates="paciente", cascade="all, delete-orphan"
    )

    @property
    def idade(self):
        if not self.data_nascimento:
            return None
        hoje = datetime.utcnow().date()
        return (
            hoje.year
            - self.data_nascimento.year
            - ((hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day))
        )

    def __repr__(self):
        return f"<Paciente {self.nome}>"


class Profissional(db.Model):
    __tablename__ = "profissionais"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    especialidade = db.Column(db.String(80))
    registro = db.Column(db.String(40))  # CRM, CRO, CRP, etc.
    cor = db.Column(db.String(7), default="#0d6efd")  # cor na agenda
    ativo = db.Column(db.Boolean, default=True)

    agendamentos = db.relationship(
        "Agendamento", back_populates="profissional", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Profissional {self.nome}>"


class Agendamento(db.Model):
    __tablename__ = "agendamentos"

    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey("pacientes.id"), nullable=False)
    profissional_id = db.Column(
        db.Integer, db.ForeignKey("profissionais.id"), nullable=False
    )

    inicio = db.Column(db.DateTime, nullable=False)
    duracao_min = db.Column(db.Integer, default=30)
    status = db.Column(db.String(20), default=STATUS_AGENDADO)
    procedimento = db.Column(db.String(120))
    observacoes = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    paciente = db.relationship("Paciente", back_populates="agendamentos")
    profissional = db.relationship("Profissional", back_populates="agendamentos")

    @property
    def fim(self):
        return self.inicio + timedelta(minutes=self.duracao_min or 30)

    @property
    def cor_status(self):
        return STATUS_CORES.get(self.status, "secondary")

    def __repr__(self):
        return f"<Agendamento {self.id} {self.inicio:%d/%m %H:%M}>"
