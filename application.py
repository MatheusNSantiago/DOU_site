import datetime
from re import A
from typing import List
from flask import Flask, redirect, url_for, render_template
from repository import SumulaDB

application = Flask(__name__)


@application.route("/")
def home():
    global dates 
    dates = db.get_unique_dates()
    return redirect(url_for("sumula_do_dia", data=str(dates[-1])))


@application.route("/sumulas/<data>")
def sumula_do_dia(data: str):
    pubs = db.publicacoes_do_dia_por_escopo(data)

    data = datetime.datetime.strptime(data, "%Y-%m-%d").date()

    return render_template(
        "index.html",
        dates=dates[-20::],
        subjects=pubs,
        data=data,
    )


if __name__ == "__main__":
    db = SumulaDB()
    
    dates = db.get_unique_dates()
    
    application.run()