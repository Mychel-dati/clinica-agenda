"""CRUD de profissionais."""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from extensions import db
from models import Profissional

bp = Blueprint("profissionais", __name__, url_prefix="/profissionais")


@bp.route("/")
def listar():
    profissionais = Profissional.query.order_by(Profissional.nome).all()
    return render_template("profissionais/list.html", profissionais=profissionais)


@bp.route("/novo", methods=["GET", "POST"])
@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def form(id=None):
    profissional = Profissional.query.get_or_404(id) if id else Profissional()

    if request.method == "POST":
        f = request.form
        if not f.get("nome", "").strip():
            flash("O nome e obrigatorio.", "danger")
            return render_template("profissionais/form.html", profissional=profissional)

        profissional.nome = f["nome"].strip()
        profissional.especialidade = f.get("especialidade", "").strip()
        profissional.registro = f.get("registro", "").strip()
        profissional.cor = f.get("cor", "#0d6efd")
        profissional.ativo = f.get("ativo") == "on"

        if id is None:
            db.session.add(profissional)
        db.session.commit()
        flash("Profissional salvo com sucesso.", "success")
        return redirect(url_for("profissionais.listar"))

    return render_template("profissionais/form.html", profissional=profissional)


@bp.route("/<int:id>/excluir", methods=["POST"])
def excluir(id):
    profissional = Profissional.query.get_or_404(id)
    db.session.delete(profissional)
    db.session.commit()
    flash("Profissional excluido.", "success")
    return redirect(url_for("profissionais.listar"))
