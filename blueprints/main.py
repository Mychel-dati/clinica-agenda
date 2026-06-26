"""Dashboard / pagina inicial."""
from datetime import datetime, timedelta

from flask import Blueprint, render_template
from sqlalchemy import func

from extensions import db
from models import (
    Agendamento,
    Paciente,
    Profissional,
    STATUS_ATENDIDO,
    STATUS_CONFIRMADO,
    STATUS_CANCELADO,
)

bp = Blueprint("main", __name__)


@bp.route("/")
def dashboard():
    hoje = datetime.utcnow().date()
    inicio_dia = datetime.combine(hoje, datetime.min.time())
    fim_dia = inicio_dia + timedelta(days=1)
    fim_semana = inicio_dia + timedelta(days=7)

    consultas_hoje = (
        Agendamento.query.filter(
            Agendamento.inicio >= inicio_dia, Agendamento.inicio < fim_dia
        )
        .order_by(Agendamento.inicio)
        .all()
    )

    total_semana = Agendamento.query.filter(
        Agendamento.inicio >= inicio_dia, Agendamento.inicio < fim_semana
    ).count()

    # Contagem por status (apenas hoje), para os cartoes do topo.
    por_status = dict(
        db.session.query(Agendamento.status, func.count(Agendamento.id))
        .filter(Agendamento.inicio >= inicio_dia, Agendamento.inicio < fim_dia)
        .group_by(Agendamento.status)
        .all()
    )

    stats = {
        "consultas_hoje": len(consultas_hoje),
        "total_semana": total_semana,
        "confirmadas_hoje": por_status.get(STATUS_CONFIRMADO, 0),
        "atendidas_hoje": por_status.get(STATUS_ATENDIDO, 0),
        "canceladas_hoje": por_status.get(STATUS_CANCELADO, 0),
        "total_pacientes": Paciente.query.count(),
        "total_profissionais": Profissional.query.filter_by(ativo=True).count(),
    }

    return render_template(
        "dashboard.html", stats=stats, consultas_hoje=consultas_hoje, hoje=hoje
    )
