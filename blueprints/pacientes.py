"""CRUD de pacientes."""
from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for

from extensions import db
from models import Paciente

bp = Blueprint("pacientes", __name__, url_prefix="/pacientes")


def _parse_data(valor):
    """Converte 'YYYY-MM-DD' (input date) em objeto date, ou None."""
    if not valor:
        return None
    try:
        return datetime.strptime(valor, "%Y-%m-%d").date()
    except ValueError:
        return None


@bp.route("/")
def listar():
    busca = request.args.get("q", "").strip()
    query = Paciente.query
    if busca:
        like = f"%{busca}%"
        query = query.filter(
            db.or_(
                Paciente.nome.ilike(like),
                Paciente.cpf.ilike(like),
                Paciente.telefone.ilike(like),
            )
        )
    pacientes = query.order_by(Paciente.nome).all()
    return render_template("pacientes/list.html", pacientes=pacientes, busca=busca)


@bp.route("/novo", methods=["GET", "POST"])
@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def form(id=None):
    paciente = Paciente.query.get_or_404(id) if id else Paciente()

    if request.method == "POST":
        f = request.form
        if not f.get("nome", "").strip():
            flash("O nome e obrigatorio.", "danger")
            return render_template("pacientes/form.html", paciente=paciente)

        paciente.nome = f["nome"].strip()
        paciente.cpf = f.get("cpf", "").strip()
        paciente.data_nascimento = _parse_data(f.get("data_nascimento"))
        paciente.telefone = f.get("telefone", "").strip()
        paciente.email = f.get("email", "").strip()
        paciente.observacoes = f.get("observacoes", "").strip()

        if id is None:
            db.session.add(paciente)
        db.session.commit()
        flash("Paciente salvo com sucesso.", "success")
        return redirect(url_for("pacientes.listar"))

    return render_template("pacientes/form.html", paciente=paciente)


@bp.route("/<int:id>/excluir", methods=["POST"])
def excluir(id):
    paciente = Paciente.query.get_or_404(id)
    db.session.delete(paciente)
    db.session.commit()
    flash("Paciente excluido.", "success")
    return redirect(url_for("pacientes.listar"))
