from datetime import date, datetime, timezone

from flask.helpers import flash
from utils import ComentarioForm
from flask import Flask, redirect, url_for, render_template
import repository as repo
from models.comentario import Comentario

application = Flask(__name__)
application.secret_key = "teste"


@application.route("/")
def home():
    dates = repo.get_unique_dates()
    return redirect(url_for("sumula_do_dia", data=str(dates[-1])))


@application.route("/sumulas/<data>", methods=["GET", "POST"])
def sumula_do_dia(data: str):
    form = ComentarioForm()

    if form.validate_on_submit():
        comentario = Comentario(
            conteudo=form.conteudo.data,
            created_at=str(datetime.now(tz=timezone.utc)),
            na_sumula_do_dia=data,
        )
        form.conteudo.data = ""

        repo.adionar_comentario(comentario)
        flash("Comentário foi adicionado")
        
        return redirect(url_for("sumula_do_dia", data=data))

    return render_template(
        "index.html",
        dates=repo.get_unique_dates()[-20::],
        subjects=repo.publicacoes_do_dia_por_escopo(data),
        data=datetime.strptime(data, "%Y-%m-%d").date(),
        comentarios=repo.pegar_comentarios_da_sumula(data),
        form=form,
    )


if __name__ == "__main__":
    # application.run()
    application.run(debug=True)
