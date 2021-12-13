from flask import Flask, redirect, url_for, render_template
from repository import SumulaDB
from datetime import date, datetime
import re

application = Flask(__name__)


def get_subjects_from_date(date):
    _pubs = [pub for pub in pubs if pub.data == date]

    subjects = dict()

    for pub in _pubs:
        try:
            subjects[pub.escopo].append(pub)
        except:
            subjects[pub.escopo] = [pub]

    return subjects


@application.route("/")
def home():
    return redirect(url_for("sumula_do_dia", data=str(dates[-1])))


@application.route("/sumulas/<data>")
def sumula_do_dia(data: date):
    data = datetime.strptime(data, "%Y-%m-%d").date()

    return render_template(
        "index.html",
        dates=dates,
        subjects=get_subjects_from_date(data),
        data=data,
    )


if __name__ == "__main__":
    with SumulaDB() as db:
        _pubs = db.query("SELECT * FROM sumula WHERE data>='2021/11/1'")

        pubs = []

        for pub in _pubs:
            if pub.titulo != None:
                pub.titulo = re.sub(r", DE .+ 2021", "", pub.titulo)

            for i in pub.escopo.split("/")[::-1]:
                if i in [
                    "Banco Central do Brasil",
                    "Ministério da Economia",
                    "Presidência da República",
                    "Conselho de Controle de Atividades Financeiras",
                    "Atos do Poder Legislativo",
                    "Atos do Poder Executivo",
                    "Ministério Público da União",
                    "Ministério do Trabalho e Previdência",
                ]:
                    pub.escopo = i
                else:
                    pub.escopo = "Outros"

                break

            pub.ementa = pub.ementa if pub.ementa else ""
            pubs.append(pub)

        dates = sorted({pub.data for pub in pubs})

        application.run(debug=True)
