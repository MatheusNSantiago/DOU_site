from datetime import datetime, timezone
from typing import List
from models.publicacao import Publicacao
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from models.comentario import Comentario
import re
import pytz


cred = credentials.Certificate("cred.json")
firebase_admin.initialize_app(cred, {"projectId": "sumula-dou"})
db = firestore.client()


def publicacoes_do_dia_por_escopo(data):
    subjects: dict[str, List[Publicacao]] = dict()

    docs = db.collection(data).stream()
    for doc in docs:
        pub = Publicacao(**doc.to_dict())
        subjects.setdefault(pub.escopo, []).append(pub)

    for escopo, pubs in subjects.items():
        subjects[escopo] = sorted(pubs, key=lambda pub: pub.titulo)

    return subjects


def get_unique_dates():
    collections = db.collections()

    to_date = lambda x: datetime.strptime(x, "%Y-%m-%d").date()

    unique_dates = []
    for collection in collections:
        if collection.id.startswith("20"):
            unique_dates.append(to_date(collection.id))

    return unique_dates


def adionar_comentario(comentario: Comentario):
    db.collection(f"comentarios").document(comentario.na_sumula_do_dia).collection(
        "foo"
    ).document(comentario.uid).set(comentario.to_firestore())


def deletar_comentario(comentario: Comentario):
    db.collection(f"comentarios").document(comentario.na_sumula_do_dia).collection(
        "foo"
    ).document(comentario.uid).delete()


def pegar_comentarios_da_sumula(do_dia: str) -> List[Comentario]:
    docs = db.collection(f"comentarios/{do_dia}/foo").stream()
    comentarios = [Comentario.from_firestore(doc) for doc in docs]

    return sorted(comentarios, key=lambda c: c.created_at)
