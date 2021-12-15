import json
import os
from typing import List
from model import Publicacao
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import datetime


class SumulaDB:
    def __init__(self) -> None:
        cred = credentials.Certificate(json.loads(os.environ["CRED"]))
        firebase_admin.initialize_app(cred, {"projectId": "sumula-dou"})
        self.db = firestore.client()

    def publicacoes_do_dia_por_escopo(self, data):
        subjects: dict[str, List[Publicacao]] = dict()

        docs = self.db.collection(data).stream()
        for doc in docs:
            pub = Publicacao(**doc.to_dict())
            subjects.setdefault(pub.escopo, []).append(pub)

        for escopo, pubs in subjects.items():
            subjects[escopo] = sorted(pubs, key=lambda pub: pub.titulo)

        return subjects

    def get_unique_dates(self):
        collections = self.db.collections()
        to_date = lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").date()
        return [to_date(collection.id) for collection in collections]
