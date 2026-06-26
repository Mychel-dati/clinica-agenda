"""Agenda e CRUD de agendamentos (o nucleo do sistema)."""
from datetime import datetime, timedelta

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from extensions import db
from models import (
    Agendamento,
    Paciente,
    Profissional,
    STATUS_CHOICES,
    STATUS_CANCELADO,
)

bp = Blueprint("agendamentos", __name__, url_prefix="/agenda")


def _parse_data(valor, padrao=None):
    try:
        return datetime.strptime(valor, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return padrao or datetime.utcnow().date()


def _tem_conflito(profissional_id, inicio, duracao_min, ignorar_id=None):
    """Verifica se o profissional ja tem agendamento sobrepondo o horario."""
    fim = inicio + timedelta(minutes=duracao_min)
    candidatos = Agendamento.query.filter(
        Agendamento.profissional_id == profissional_id,
        Agendamento.status != STATUS_CANCELADO,
    )
    if ignorar_id:
        candidatos = candidatos.filter(Agendamento.id != ignorar_id)

    for ag in candidatos:
        if ag.inicio < fim and ag.fim > inicio:  # sobreposicao
            return ag
    return None


@bp.route("/")
def agenda():
    """Visao de agenda do dia: grade de horarios x agendamentos."""
    dia = _parse_data(request.args.get("data"))
    profissional_id = request.args.get("profissional_id", type=int)

    profissionais = Profissional.query.filter_by(ativo=True).order_by(
        Profissional.nome
    ).all()

    inicio_dia = datetime.combine(dia, datetime.min.time())
    fim_dia = inicio_dia + timedelta(days=1)

    query = Agendamento.query.filter(
        Agendamento.inicio >= inicio_dia, Agendamento.inicio < fim_dia
    )
    if profissional_id:
        query = query.filter(Agendamento.profissional_id == profissional_id)
    agendamentos = query.order_by(Agendamento.inicio).all()

    # Monta a grade de horarios (slots) conforme config da clinica.
    cfg = current_app.config
    slots = []
    t = inicio_dia.replace(hour=cfg["HORARIO_ABERTURA"])
    fim_grade = inicio_dia.replace(hour=cfg["HORARIO_FECHAMENTO"])
    while t < fim_grade:
        slots.append(t)
        t += timedelta(minutes=cfg["INTERVALO_MINUTOS"])

    # Indexa agendamentos por horario "HH:MM" para casar com a grade.
    por_slot = {}
    for ag in agendamentos:
        chave = ag.inicio.strftime("%H:%M")
        por_slot.setdefault(chave, []).append(ag)

    return render_template(
        "agenda/index.html",
        dia=dia,
        slots=slots,
        por_slot=por_slot,
        agendamentos=agendamentos,
        profissionais=profissionais,
        profissional_id=profissional_id,
        dia_anterior=dia - timedelta(days=1),
        dia_seguinte=dia + timedelta(days=1),
        hoje=datetime.utcnow().date(),
    )


@bp.route("/novo", methods=["GET", "POST"])
@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def form(id=None):
    agendamento = Agendamento.query.get_or_404(id) if id else Agendamento()

    if request.method == "POST":
        f = request.form
        try:
            data = datetime.strptime(f["data"], "%Y-%m-%d").date()
            hora = datetime.strptime(f["hora"], "%H:%M").time()
            inicio = datetime.combine(data, hora)
        except (ValueError, KeyError):
            flash("Data ou hora invalida.", "danger")
            return _render_form(agendamento)

        paciente_id = request.form.get("paciente_id", type=int)
        profissional_id = request.form.get("profissional_id", type=int)
        duracao = request.form.get("duracao_min", type=int) or 30

        if not paciente_id or not profissional_id:
            flash("Selecione paciente e profissional.", "danger")
            return _render_form(agendamento)

        conflito = _tem_conflito(profissional_id, inicio, duracao, ignorar_id=id)
        if conflito:
            flash(
                f"Conflito de horario: o profissional ja tem consulta as "
                f"{conflito.inicio:%H:%M} com {conflito.paciente.nome}.",
                "danger",
            )
            return _render_form(agendamento)

        agendamento.paciente_id = paciente_id
        agendamento.profissional_id = profissional_id
        agendamento.inicio = inicio
        agendamento.duracao_min = duracao
        agendamento.procedimento = f.get("procedimento", "").strip()
        agendamento.observacoes = f.get("observacoes", "").strip()
        if id is None:
            agendamento.status = STATUS_CHOICES[0]
        else:
            agendamento.status = f.get("status", agendamento.status)

        if id is None:
            db.session.add(agendamento)
        db.session.commit()
        flash("Agendamento salvo com sucesso.", "success")
        return redirect(url_for("agendamentos.agenda", data=inicio.date().isoformat()))

    # GET: pre-preenche data/profissional vindos da agenda (links rapidos).
    if id is None:
        data_param = request.args.get("data")
        hora_param = request.args.get("hora")
        if data_param:
            agendamento.inicio = datetime.combine(
                _parse_data(data_param),
                datetime.strptime(hora_param, "%H:%M").time()
                if hora_param
                else datetime.min.time(),
            )
        prof = request.args.get("profissional_id", type=int)
        if prof:
            agendamento.profissional_id = prof

    return _render_form(agendamento)


def _render_form(agendamento):
    pacientes = Paciente.query.order_by(Paciente.nome).all()
    profissionais = Profissional.query.filter_by(ativo=True).order_by(
        Profissional.nome
    ).all()
    return render_template(
        "agendamentos/form.html",
        agendamento=agendamento,
        pacientes=pacientes,
        profissionais=profissionais,
        status_choices=STATUS_CHOICES,
    )


@bp.route("/<int:id>/status", methods=["POST"])
def mudar_status(id):
    """Altera rapidamente o status (botoes na agenda)."""
    agendamento = Agendamento.query.get_or_404(id)
    novo = request.form.get("status")
    if novo in STATUS_CHOICES:
        agendamento.status = novo
        db.session.commit()
        flash("Status atualizado.", "success")
    return redirect(
        request.referrer
        or url_for("agendamentos.agenda", data=agendamento.inicio.date().isoformat())
    )


@bp.route("/<int:id>/excluir", methods=["POST"])
def excluir(id):
    agendamento = Agendamento.query.get_or_404(id)
    data = agendamento.inicio.date().isoformat()
    db.session.delete(agendamento)
    db.session.commit()
    flash("Agendamento excluido.", "success")
    return redirect(url_for("agendamentos.agenda", data=data))
